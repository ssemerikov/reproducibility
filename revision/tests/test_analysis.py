from pathlib import Path
import csv,json,subprocess,sys,tempfile,unittest,shutil
ROOT=Path(__file__).resolve().parents[2]
class AggregateAnalysis(unittest.TestCase):
 def test_workbook_recoding_reproduces_scores_from_aggregate_counts(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=subprocess.run([sys.executable,str(ROOT/'revision/tools/analyse_aggregates.py'),'--data',str(ROOT/'revision/data'),'--output',tmp],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   output=Path(tmp)/'workbook_reanalysis.json'
   self.assertTrue(output.exists(),'Workbook aggregate reanalysis is missing')
   result=json.loads(output.read_text())
   self.assertEqual(result['coding_mismatches'],63)
   self.assertEqual(result['changed_scores'],{'2.01':[144,118],'2.02':[156,139],'2.03':[156,131],'2.04':[148,118]})
   self.assertEqual(result['selected_counts'],{'published':30,'recoded_fixed_cutoff':28,'recoded_recomputed_cutoff':44})
   self.assertEqual(result['recomputed_cutoff'],113.15)
 def test_released_aggregates_reproduce_summaries(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=subprocess.run([sys.executable,str(ROOT/'revision/tools/analyse_aggregates.py'),'--data',str(ROOT/'revision/data'),'--output',tmp],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   s=json.loads((Path(tmp)/'analysis_summary.json').read_text())
   self.assertEqual(s['curriculum_selection'],{'rated':64,'cutoff_selected':30,'shaded_selected':41,'shaded_below_cutoff':11})
   self.assertEqual(s['exit_upper_two_counts'],[19,18,15,17,21,10,26,35])
   self.assertEqual(s['excluded_comparison_domains'],[3,4])
 def test_selection_scenarios_cross_coding_weighting_and_fraction(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=subprocess.run([sys.executable,str(ROOT/'revision/tools/analyse_aggregates.py'),'--data',str(ROOT/'revision/data'),'--output',tmp],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   with (Path(tmp)/'selection_scenarios.csv').open() as f:rows=list(csv.DictReader(f))
   counts={(r['coding'],r['weighting'],r['range_fraction']):int(r['selected_n']) for r in rows}
   self.assertEqual([counts['published','self_rated_familiarity',f] for f in ['0.35','0.45','0.55']],[41,30,20])
   self.assertEqual([counts['published','equal',f] for f in ['0.35','0.45','0.55']],[40,29,17])
   self.assertEqual([counts['raw_label','self_rated_familiarity',f] for f in ['0.35','0.45','0.55']],[52,44,34])
   self.assertEqual([counts['raw_label','equal',f] for f in ['0.35','0.45','0.55']],[50,45,31])
   self.assertEqual(counts['raw_label','self_rated_familiarity',''],28)
   status={(r['coding'],r['weighting'],r['range_fraction']):r['item_8_03_selected'] for r in rows}
   self.assertEqual(status['published','self_rated_familiarity','0.45'],'False')
   self.assertEqual(status['published','equal','0.45'],'True')
   self.assertEqual(status['raw_label','self_rated_familiarity','0.45'],'True')
   s=json.loads((Path(tmp)/'selection_sensitivity.json').read_text())
   self.assertEqual((s['factorial_scenarios'],s['selected_in_all'],s['selected_in_none']),(12,15,10))
   self.assertEqual(s['equal_weighting_at_045'],{'added':['6.03','8.03'],'dropped':['5.08','5.09','7.01']})
   self.assertEqual((len(s['judgement_added']),s['judgement_added_scoring_below_8_03']),(11,9))
   self.assertEqual(s['items_6_03_and_8_03_in_final_selection'],[])
 def test_corrupted_count_is_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);(d/'data').mkdir()
   for name in ['student_distributions.csv','curriculum_ratings.csv']:shutil.copyfile(ROOT/'revision/data'/name,d/'data'/name)
   p=d/'data/student_distributions.csv'
   with p.open() as f:rows=list(csv.DictReader(f))
   fields=list(rows[0]);rows[0]['count']='999'
   with p.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
   result=subprocess.run([sys.executable,str(ROOT/'revision/tools/analyse_aggregates.py'),'--data',str(d/'data'),'--output',str(d/'out')],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0)
   self.assertIn('distribution total mismatch',result.stderr)
if __name__=='__main__':unittest.main()
