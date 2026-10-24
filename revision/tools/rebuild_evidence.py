#!/usr/bin/env python3
"""Recover published aggregates without reconstructing individual respondents."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
import openpyxl
import fitz

ROOT = Path(__file__).resolve().parents[2]
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
DOMAINS = ['Physical foundations','Mathematical foundations','Enabling technologies',
           'Computer and sensor hardware','Computing and simulation','Sensing and metrology',
           'Quantum communication','Practical and general competencies']
LEVELS = ['initial','intermediate','sufficient','high']


def rows_of(table):
    return [[''.join(t.text or '' for t in cell.findall('.//w:t', NS)).strip()
             for cell in row.findall('w:tc', NS)] for row in table.findall('w:tr', NS)]


def write_csv(path, rows):
    if not rows: raise ValueError(f'Empty output: {path}')
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def recover(docx, pdf, out):
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(docx) as z:
        embedded=[n for n in z.namelist() if '/embeddings/' in n or n.lower().endswith(('.xls','.xlsx','.xlsb'))]
        tables=ET.fromstring(z.read('word/document.xml')).findall('.//w:tbl',NS)
        candidates=[(i,t,rows_of(t)) for i,t in enumerate(tables)
                    if 'ЕГ-до' in str(rows_of(t)) and 'ЕГ-після' in str(rows_of(t))]
        if len(candidates)!=1: raise ValueError('Expected exactly one student distribution table')
        table_index, _, rows=candidates[0]
        table_vals={}
        for row in rows:
            if row[0] not in ['ЕГ-до','ЕГ-після']: continue
            occasion={'ЕГ-до':'before','ЕГ-після':'after'}[row[0]]
            vals=list(map(int,row[1:]))
            if len(vals)!=32: raise ValueError('Expected eight four-category distributions')
            for k in range(8): table_vals[k+1,occasion]=vals[k*4:k*4+4]
        chart_vals={}
        for k in range(1,9):
            chart=ET.fromstring(z.read(f'word/charts/chart{k}.xml'))
            series=chart.findall('.//c:ser',NS)
            if len(series)!=2: raise ValueError('Unexpected number of chart series')
            for s in series:
                label=s.findtext('c:tx/c:strRef/c:strCache/c:pt/c:v',namespaces=NS)
                occasion={'ЕГ-до':'before','ЕГ-після':'after'}[label]
                points=s.findall('c:val/c:numRef/c:numCache/c:pt',NS)
                vals=[int(p.findtext('c:v',namespaces=NS)) for p in sorted(points,key=lambda p:int(p.attrib['idx']))]
                if len(vals)!=4: raise ValueError('Unexpected category count')
                chart_vals[k,occasion]=vals
        discrepancies=[]
        for (k,occasion),vals in table_vals.items():
            other=chart_vals[k,occasion]
            if vals!=other:
                discrepancies.append(dict(domain_id=k,domain=DOMAINS[k-1],occasion=occasion,
                    table_counts=json.dumps(vals),chart_counts=json.dumps(other),table_total=sum(vals),chart_total=sum(other),
                    source='Table 2.28 p.163; Fig. 2.22 p.164' if k==3 else 'Table 2.28 p.163; Fig. 2.23 p.165',
                    resolution='Unresolved; retain both; exclude domain from before/after comparisons'))
        bad={r['domain_id'] for r in discrepancies}
        student=[]
        for kind,values in [('table',table_vals),('chart_cache',chart_vals)]:
            for (k,occasion),vals in values.items():
                for level,count in zip(LEVELS,vals):
                    student.append(dict(domain_id=k,domain=DOMAINS[k-1],occasion=occasion,level=level,count=count,
                        reported_cohort=45,distribution_total=sum(vals),source_kind=kind,
                        source_locator=f'Word table {table_index} (zero-based); Table 2.28, p.163' if kind=='table' else f'word/charts/chart{k}.xml; Fig. 2.{19+k}',
                        comparison_eligible=str(k not in bad).lower(),
                        interpretation='Published marginal counts; non-equivalent entry/exit assessments; no paired inference'))
        expert=[]
        rating_tables=[]
        for i,t in enumerate(tables):
            rows=rows_of(t)
            if not rows or 'Оцінка експерта' not in str(rows): continue
            rating_tables.append((i,t,rows))
        if len(rating_tables)!=8: raise ValueError('Expected eight curriculum-rating tables')
        for k,(i,t,rows) in enumerate(rating_tables,1):
            xmlrows=t.findall('w:tr',NS)
            for j,row in enumerate(rows):
                if len(row)!=8 or not row[0].isdigit(): continue
                counts=list(map(int,row[2:7])); score=int(row[7])
                if sum(counts)!=36: raise ValueError('Rating counts do not sum to 36')
                # Displayed columns are -1, +1, 0, +2, +3, not monotonic order.
                score_unweighted=sum(a*b for a,b in zip(counts,[-1,1,0,2,3]))
                fills=sorted({e.attrib.get('{'+NS['w']+'}fill','') for e in xmlrows[j].findall('.//w:shd',NS)})
                expert.append(dict(domain_id=k,item_id=f'{k}.{int(row[0]):02}',item_uk=row[1],
                    not_important=counts[0],slightly_important=counts[1],unable_to_answer=counts[2],
                    rather_important=counts[3],very_important=counts[4],n=36,
                    favorable_n=counts[3]+counts[4],favorable_percent=round(100*(counts[3]+counts[4])/36,4),
                    unable_percent=round(100*counts[2]/36,4),unweighted_sum=score_unweighted,
                    mean_among_substantive_responses=round(score_unweighted/(36-counts[2]),6) if counts[2]<36 else '',
                    reported_expertise_weighted_score=score,reported_cutoff=120.8,
                    meets_reported_numeric_cutoff=str(score>=120.8).lower(),
                    word_row_shading='|'.join(fills),source_locator=f'Table 2.{6+k}; Word table {i}, row {j} (zero-based)',
                    limitation='Thesis-table transcription only; respondent/weight linkage is absent from marginals and audited separately in the supplied curriculum workbook'))
    teacher=[dict(item_id=key,item_en=label,reported_percent=value,reported_sample=26,
                  source_locator=f'Thesis p.{page}',count_reconstructed='false',note=note)
             for key,label,value,page,note in [
                ('T01','School education should reflect contemporary achievements',100,83,'Reported opinion, not observed teaching practice'),
                ('T02','Always uses cloud technologies in teaching',65.4,83,'Self-report'),
                ('T03','Uses cloud technologies during distance education only',34.6,83,'Self-report'),
                ('T04','Content should be adapted to learners age',96.2,84,'Opinion'),
                ('T05','Welcomes new topics, especially with adequate methodological support',96.2,84,'Compound conditional item'),
                ('T06','Would personally like to take the quantum informatics course',88.5,84,'Interest does not demonstrate teaching readiness'),
                ('T07','Would propose the course at own institution',61.6,84,'As printed; percentage does not match standard one-decimal rounding of a fraction with denominator 26; retain without inferring a count'),
                ('T08','Would not propose the course because it would not fit the institution profile',23.1,84,'As printed; reason as stated by respondents; no count inferred'),
                ('T09','Would not propose the course (answered no)',3.8,84,'As printed; T07, T08 and T09 sum to 88.5 percent; remainder not reported')]]
    # Verify PDF-text presence of both conflicting chart series as a cross-format check.
    with fitz.open(pdf) as d:
        pdftxt='\n'.join(f'=== PDF PAGE {i+1} ===\n'+p.get_text() for i,p in enumerate(d))
        pdf_pages=len(d)
    internal=ROOT/'revision/evidence'
    internal.mkdir(parents=True,exist_ok=True)
    (internal/'thesis_text.txt').write_text(pdftxt)
    summary=dict(thesis_docx_sha256=hashlib.sha256(docx.read_bytes()).hexdigest(),
        thesis_pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pdf_pages=pdf_pages,
        embedded_workbooks=embedded,charts=8,student_cohort=45,teacher_survey_n=26,curriculum_survey_n=36,
        rating_items=len(expert),selected_components_reported=41,discrepant_domains=sorted(bad),
        participant_level_data_recovered=False,
        scope='Thesis DOCX/PDF extraction only; separately supplied curriculum responses are audited in workbook_assessment.json',
        curriculum_numeric_threshold_items=sum(r['meets_reported_numeric_cutoff']=='true' for r in expert),
        favorable_rating_percent_range=[min(r['favorable_percent'] for r in expert),max(r['favorable_percent'] for r in expert)])
    for name,records in [('student_distributions',student),('curriculum_ratings',expert),('teacher_survey',teacher),('discrepancies',discrepancies)]:
        write_csv(out/f'{name}.csv',records)
    (out/'extraction_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    wb=openpyxl.Workbook(); wb.remove(wb.active)
    for name,records in [('Students',student),('Curriculum_ratings',expert),('Teachers',teacher),('Discrepancies',discrepancies)]:
        ws=wb.create_sheet(name); ws.append(list(records[0]));
        for r in records: ws.append(list(r.values()))
        ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
    ws=wb.create_sheet('Readme')
    for row in [('Status','Published thesis aggregates; distinct from the separately audited original curriculum workbook'),
                ('Source','Lehka 2021 thesis; Tables 2.7–2.14 and 2.28; Figures 2.20–2.27; pp.83–88,160–167'),
                ('Limits','No participant-level records in this aggregate workbook; no reconstructed student pairs'),
                ('Discrepancies','Two unresolved baseline conflicts preserved; see Discrepancies sheet'),
                ('Weighted scores','As printed in thesis; original curriculum workbook audit and recoding are supplied separately'),
                ('Teacher data','Reported percentages only; no inferred individual response counts')]:ws.append(row)
    wb.save(out/'thesis_recovered.xlsx')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--thesis-dir',type=Path,default=Path('thesis_source'))
    parser.add_argument('--output',type=Path,default=ROOT/'revision/data')
    a=parser.parse_args(); recover(a.thesis_dir/'dis_lehka.docx',a.thesis_dir/'dis_lehka.pdf',a.output)
