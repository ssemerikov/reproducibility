#!/usr/bin/env python3
"""Reproduce descriptive summaries from released thesis aggregates using Python's stdlib."""
import argparse,csv,json
from pathlib import Path
from collections import defaultdict

def read(path):
 with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def analyse_workbook(data,out,ratings):
 """Reproduce both score versions from unlinked item/category/weight counts."""
 path=data/'curriculum_weighted_counts.csv'
 if not path.exists():return
 cells=read(path);groups=defaultdict(dict)
 for r in cells:
  weight,code=int(r['expertise_weight']),int(r['rating_code'])
  raw,stored=int(r['raw_count']),int(r['stored_count'])
  if weight not in [1,2,3] or code not in [-1,0,1,2,3] or min(raw,stored)<0:
   raise ValueError('Invalid workbook aggregate cell')
  if (weight,code) in groups[r['item_id']]:raise ValueError('Duplicate workbook aggregate cell')
  groups[r['item_id']][weight,code]=(raw,stored)
 expected={r['item_id']:r for r in ratings}
 if set(groups)!=set(expected):raise ValueError('Workbook item set differs from thesis')
 rows=[];changed={};mismatches=0
 for item,c in sorted(groups.items()):
  if set(c)!={(w,k) for w in [1,2,3] for k in [-1,0,1,2,3]}:
   raise ValueError('Incomplete workbook aggregate cells')
  for w,n in [(1,17),(2,15),(3,4)]:
   if any(sum(c[w,k][v] for k in [-1,0,1,2,3])!=n for v in [0,1]):
    raise ValueError('Workbook expertise denominator mismatch')
   if any(c[w,k][0]!=c[w,k][1] for k in [-1,0,1]):
    raise ValueError('Unexpected recoding outside rather/very important')
   delta=c[w,2][0]-c[w,2][1]
   if delta<0 or delta!=c[w,3][1]-c[w,3][0]:raise ValueError('Inconsistent recoding counts')
   mismatches+=delta
  scores=[sum(w*k*count[v] for (w,k),count in c.items()) for v in [0,1]]
  if scores[1]!=int(expected[item]['reported_expertise_weighted_score']):
   raise ValueError('Stored workbook score differs from thesis')
  for key,code in zip(['not_important','slightly_important','unable_to_answer','rather_important','very_important'],[-1,1,0,2,3]):
   if sum(c[w,code][1] for w in [1,2,3])!=int(expected[item][key]):
    raise ValueError('Stored workbook category counts differ from thesis')
  if scores[0]!=scores[1]:changed[item]=[scores[1],scores[0]]
  rows.append(dict(item_id=item,published_score=scores[1],recoded_score=scores[0]))
 published=[r['published_score'] for r in rows];recoded=[r['recoded_score'] for r in rows]
 original_cutoff=min(published)+.45*(max(published)-min(published))
 cutoff=min(recoded)+.45*(max(recoded)-min(recoded))
 result=dict(respondents=36,items=len(rows),coding_mismatches=mismatches,
  changed_scores=changed,published_cutoff=round(original_cutoff,2),recomputed_cutoff=round(cutoff,2),
  selected_counts=dict(published=sum(s>=original_cutoff for s in published),
   recoded_fixed_cutoff=sum(s>=original_cutoff for s in recoded),
   recoded_recomputed_cutoff=sum(s>=cutoff for s in recoded)),
  scope='Aggregate reconstruction of existing curriculum responses; no independent sample, student data or respondent linkages')
 write(out/'workbook_scores.csv',rows)
 (out/'workbook_reanalysis.json').write_text(json.dumps(result,indent=2)+'\n')
 analyse_selection(groups,out,ratings,original_cutoff)
def analyse_selection(groups,out,ratings,fixed_cutoff):
 """Cross response coding, respondent weighting and range fraction; descriptive scenarios, not recommendations."""
 shaded={r['item_id'] for r in ratings if r['word_row_shading']=='F2F2F2'};scenarios=[];chosen={}
 for coding,v in [('published',1),('raw_label',0)]:
  for weighting in ['self_rated_familiarity','equal']:
   scores={item:sum((w if weighting!='equal' else 1)*k*count[v] for (w,k),count in c.items()) for item,c in groups.items()}
   rules=[(f,min(scores.values())+f*(max(scores.values())-min(scores.values()))) for f in [.35,.45,.55]]
   if coding=='raw_label' and weighting!='equal':rules.append(('fixed',fixed_cutoff))
   for f,cut in rules:
    sel={item for item,s in scores.items() if s>=cut}
    if f!='fixed':chosen[coding,weighting,f]=sel
    scenarios.append(dict(coding=coding,weighting=weighting,rule='range_fraction' if f!='fixed' else 'fixed_published_cutoff',
     range_fraction=f if f!='fixed' else '',min_score=min(scores.values()),max_score=max(scores.values()),cutoff=round(cut,2),
     selected_n=len(sel),selected_and_shaded_n=len(sel&shaded),item_8_03_selected='8.03' in sel,item_6_03_selected='6.03' in sel,
     factorial=f!='fixed'))
 published=chosen['published','self_rated_familiarity',.45];robust=[]
 for r in ratings:
  n=sum(r['item_id'] in sel for sel in chosen.values())
  robust.append(dict(item_id=r['item_id'],domain_id=r['domain_id'],published_score=r['reported_expertise_weighted_score'],
   shaded=r['item_id'] in shaded,published_selection=r['item_id'] in published,factorial_scenarios_selected=n,
   factorial_scenarios=len(chosen)))
 write(out/'selection_scenarios.csv',scenarios);write(out/'item_selection_robustness.csv',robust)
 summary=dict(factorial_scenarios=len(chosen),selected_in_all=sum(r['factorial_scenarios_selected']==len(chosen) for r in robust),
  selected_in_none=sum(r['factorial_scenarios_selected']==0 for r in robust),
  item_8_03_selected_scenarios=next(r['factorial_scenarios_selected'] for r in robust if r['item_id']=='8.03'),
  equal_weighting_at_045=dict(added=sorted(chosen['published','equal',.45]-published),dropped=sorted(published-chosen['published','equal',.45])),
  judgement_added={r['item_id']:int(r['reported_expertise_weighted_score']) for r in ratings if r['item_id'] in shaded-published},
  judgement_added_scoring_below_8_03=sum(int(r['reported_expertise_weighted_score'])<int(next(x for x in ratings if x['item_id']=='8.03')['reported_expertise_weighted_score']) for r in ratings if r['item_id'] in shaded-published),
  items_6_03_and_8_03_in_final_selection=sorted({'6.03','8.03'}&shaded),
  scope='Descriptive sensitivity of selection to coding, self-rated familiarity weights and range fraction; weights are self-ratings, not measured expertise')
 (out/'selection_sensitivity.json').write_text(json.dumps(summary,indent=2)+'\n')
def analyse(data,out):
 out.mkdir(parents=True,exist_ok=True)
 students=read(data/'student_distributions.csv');ratings=read(data/'curriculum_ratings.csv')
 groups=defaultdict(list)
 for r in students:groups[(int(r['domain_id']),r['occasion'],r['source_kind'])].append(r)
 for key,rows in groups.items():
  if sum(int(r['count']) for r in rows)!=int(rows[0]['distribution_total']):raise ValueError('distribution total mismatch: '+str(key))
  if len(rows)!=4 or len({r['level'] for r in rows})!=4:raise ValueError('Unexpected category structure')
 bad=[]
 for k in range(1,9):
  for when in ['before','after']:
   t={r['level']:int(r['count']) for r in groups[k,when,'table']};c={r['level']:int(r['count']) for r in groups[k,when,'chart_cache']}
   if t!=c:bad.append(k)
 bad=sorted(set(bad));exitrows=[]
 for k in range(1,9):
  rows=groups[k,'after','table'];n=sum(int(r['count']) for r in rows if r['level'] in ['sufficient','high'])
  if sum(int(r['count']) for r in rows)!=45:raise ValueError('Unexpected exit denominator')
  if {r['level']:r['count'] for r in rows}!={r['level']:r['count'] for r in groups[k,'after','chart_cache']}:raise ValueError('Exit sources disagree')
  exitrows.append(dict(domain_id=k,domain=rows[0]['domain'],sufficient_or_high_n=n,denominator=45,percent=round(100*n/45,1),baseline_conflict=k in bad,interpretation='Exit classification only; not a gain estimate'))
 categories=['not_important','slightly_important','unable_to_answer','rather_important','very_important']
 for r in ratings:
  if sum(int(r[c]) for c in categories)!=36:raise ValueError('Curriculum denominator mismatch')
  if int(r['favorable_n'])!=int(r['rather_important'])+int(r['very_important']):raise ValueError('Favorable count mismatch')
 selected=[r for r in ratings if float(r['reported_expertise_weighted_score'])>=120.8];shaded=[r for r in ratings if r['word_row_shading']=='F2F2F2']
 domainrows=[]
 for k in range(1,9):
  a=[r for r in ratings if int(r['domain_id'])==k]
  domainrows.append(dict(domain_id=k,rated_items=len(a),numeric_cutoff_items=sum(float(r['reported_expertise_weighted_score'])>=120.8 for r in a),shaded_selected_items=sum(r['word_row_shading']=='F2F2F2' for r in a),favorable_min_percent=min(round(100*int(r['favorable_n'])/36,4) for r in a),favorable_max_percent=max(round(100*int(r['favorable_n'])/36,4) for r in a)))
 sensitivity=[dict(range_fraction=c,cutoff=92+c*64,items_meeting_cutoff=sum(float(r['reported_expertise_weighted_score'])>=92+c*64 for r in ratings),interpretation='Sensitivity of the thesis-reported scores; separate workbook audit reproduces stored scores and reports raw-label recoding') for c in [.35,.45,.55]]
 summary=dict(curriculum_selection=dict(rated=len(ratings),cutoff_selected=len(selected),shaded_selected=len(shaded),shaded_below_cutoff=sum(float(r['reported_expertise_weighted_score'])<120.8 for r in shaded)),exit_upper_two_counts=[r['sufficient_or_high_n'] for r in exitrows],excluded_comparison_domains=bad,participant_level_data_used_by_this_command=False,inference='Thesis aggregate reproduction only; no equivalent student entry/exit measure or paired student records; curriculum workbook audited separately')
 for name,rows in [('student_exit_summary',exitrows),('curriculum_domain_summary',domainrows),('threshold_sensitivity',sensitivity)]:write(out/(name+'.csv'),rows)
 (out/'analysis_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
 analyse_workbook(data,out,ratings)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--data',type=Path,default=Path('data'));p.add_argument('--output',type=Path,default=Path('derived'));a=p.parse_args();analyse(a.data,a.output)
