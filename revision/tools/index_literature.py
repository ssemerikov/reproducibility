#!/usr/bin/env python3
"""Provenance-preserving index and explicit discovery rules; not a systematic screen."""
import argparse,csv,hashlib,json,re,unicodedata
from pathlib import Path
from collections import Counter,defaultdict
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[2]

def parse_export(text):
    """Parse literal-field BibTeX exports in linear time; reject unsupported syntax.

    Unlike a bibliography processor this deliberately does not expand macros.
    All supplied exports use braced or quoted literal values (or bare numbers).
    """
    entries=[]
    starts=list(re.finditer(r'(?m)^\s*@([A-Za-z]+)\s*\{',text))
    for n,m in enumerate(starts):
        chunk=text[m.end():starts[n+1].start() if n+1<len(starts) else len(text)]
        ident,sep,body=chunk.partition(',')
        if not sep:raise ValueError('Entry missing identifier delimiter')
        e={'ENTRYTYPE':m.group(1).lower(),'ID':ident.strip()};i=0
        while i<len(body):
            while i<len(body) and (body[i].isspace() or body[i]==','):i+=1
            if i==len(body) or body[i]=='}':break
            f=re.match(r'([\w-]+)\s*=\s*',body[i:])
            if not f:raise ValueError('Unsupported field syntax: '+body[i:i+60])
            key=f.group(1).lower();i+=f.end()
            if body[i]=='{':
                i+=1;begin=i;depth=1
                while i<len(body) and depth:
                    if body[i]=='\\':i+=2;continue
                    if body[i]=='{':depth+=1
                    elif body[i]=='}':depth-=1
                    i+=1
                if depth:raise ValueError('Unbalanced field in '+e['ID'])
                value=body[begin:i-1]
            elif body[i]=='"':
                i+=1;begin=i
                while i<len(body) and body[i]!='"':
                    i+=2 if body[i]=='\\' else 1
                if i==len(body):raise ValueError('Unclosed quoted field')
                value=body[begin:i];i+=1
            else:
                f=re.match(r'[^,}]+',body[i:]);value=f.group(0).strip();i+=f.end()
                if not value.isdigit():raise ValueError('Unsupported macro: '+value)
            e[key]=value
        entries.append(e)
    return entries

def normalize_title(s):
    return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFKC',s).lower()))
def normalize_doi(s):
    s=unquote(s).strip().lower().strip('{}').replace(r'\_', '_')
    s=re.sub(r'^https?://(?:dx\.)?doi\.org/','',s)
    return s.rstrip(' .')
def discovery(text):
    s=text.lower()
    quantum=bool(re.search(r'quantum|квантов',s))
    education=bool(re.search(r'educat|teach|curricul|literac|student|school|навчан',s))
    school=bool(re.search(r'secondary|high.school|lyceum|k.?12|ліце',s))
    social=bool(re.search(r'socio.?scientific|sociotechnical|citizenship|futures thinking|responsible innovation|epistemic trust',s))
    if quantum and school and education:return 'A_quantum_secondary'
    if quantum and education:return 'B_quantum_education'
    if quantum and social:return 'C_quantum_societal'
    if social and education:return 'D_supporting_theory'
    return 'not_selected_by_discovery_rule'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--related-dir',type=Path,default=Path('related_exports'))
    a=parser.parse_args()
    collections=[('legacy_scopus',ROOT/'newdata','*.txt'),('legacy_wos',ROOT/'new_data_2/results','*.bib'),('related_paper_scopus',a.related_dir,'scopus-*.txt')]
    raw=[];files=[];errors=[];counts=Counter()
    for name,folder,pattern in collections:
        for file in sorted(folder.glob(pattern)):
            txt=file.read_text(encoding='utf-8-sig',errors='replace')
            try: entries=parse_export(txt)
            except Exception as exc:errors.append({'file':file.name,'error':str(exc)});continue
            expected=len(re.findall(r'^\s*@(?:article|book|inproceedings|conference|incollection|proceedings|phdthesis|mastersthesis|misc|techreport|review|inbook|unpublished)\s*\{',txt,re.I|re.M))
            if len(entries)!=expected:errors.append({'file':file.name,'error':f'parsed {len(entries)}; counted {expected}'})
            date=re.search(r'EXPORT DATE:\s*([^\n]+)',txt)
            files.append(dict(collection=name,file=file.name,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),entries=len(entries),export_date=date.group(1) if date else 'not_recorded_in_file'))
            counts[name]+=len(entries)
            for e in entries:
                raw.append(dict(doi=normalize_doi(e.get('doi','')),title=e.get('title','').replace('\n',' '),year=e.get('year',''),
                    authors=e.get('author',''),abstract=e.get('abstract',''),journal=e.get('journal',''),
                    bibtex=e,provenance=[dict(collection=name,file=file.name,entry_id=e['ID'])]))
    title_dois=defaultdict(set)
    for r in raw:
        if r['doi']:title_dois[(normalize_title(r['title']),r['year'])].add(r['doi'])
    merged={};possible=[]
    for r in raw:
        ty=(normalize_title(r['title']),r['year'])
        if not r['doi'] and len(title_dois[ty])==1:r['doi']=next(iter(title_dois[ty]))
        key=('doi',r['doi']) if r['doi'] else ('title_year_author',*ty,normalize_title(r['authors'].split(' and ')[0]))
        if key in merged:
            m=merged[key];m['provenance']+=r['provenance']
            if len(r['abstract'])>len(m['abstract']):m['abstract']=r['abstract']
        else:merged[key]=r
    records=[]
    for i,(key,r) in enumerate(sorted(merged.items(),key=lambda kv:str(kv[0])),1):
        r['record_id']=f'L{i:05}'
        r['discovery_class']=discovery(r['title']+' '+r['abstract'])
        r['selection_status']='not_yet_fulltext_assessed'
        records.append(r)
    out=ROOT/'revision/data';out.mkdir(parents=True,exist_ok=True)
    (out/'literature_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    (out/'legacy_file_manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
    summary=dict(raw_entries=len(raw),raw_entries_by_collection=dict(counts),unique_records=len(records),
        unique_with_doi=sum(bool(r['doi']) for r in records),discovery_counts=dict(Counter(r['discovery_class'] for r in records)),parse_errors=errors,
        note='Discovery rules generate candidates; they do not establish relevance, full-text access or quality. Selection is in fulltext_decisions.csv.')
    (out/'literature_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    fields=['record_id','doi','year','title','authors','journal','discovery_class','selection_status','provenance']
    with (out/'literature_index.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
        for r in records:w.writerow({**r,'provenance':json.dumps(r['provenance'],ensure_ascii=False)})
    with (out/'discovery_candidates.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['record_id','class','year','doi','title'])
        for r in sorted(records,key=lambda r:(r['discovery_class'],r['year'],r['title'])):
            if r['discovery_class']!='not_selected_by_discovery_rule':w.writerow([r['record_id'],r['discovery_class'],r['year'],r['doi'],r['title']])
    print(json.dumps(summary))
    if errors:raise SystemExit('Parsing discrepancies require review')
if __name__=='__main__':main()
