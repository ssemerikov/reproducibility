from pathlib import Path
from collections import Counter
import csv,unittest
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'revision/data'
LABELS={'зовсім не важливо':-1,'мало важливо':1,'утруднююсь відповісти':0,'скоріше, важливо':2,'скоріше важливо':2,'дуже важливо':3}
WEIGHTS={'маю початкові уявлення':1,'обізнаний з окремими складовими':2,'глибоко обізнаний з окремими складовими':3}
def read(name):
 with (D/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
class DeidentifiedResponses(unittest.TestCase):
 """The de-identified respondent rows must reproduce every released aggregate."""
 def setUp(self):
  self.wide=read('curriculum_responses_deidentified.csv');self.long=read('curriculum_responses_coded.csv')
  self.items=[r['item_id'] for r in read('curriculum_ratings.csv')]
 def test_only_ratings_and_self_rating_are_released(self):
  expected=['respondent_id','self_rated_competence','expertise_weight']+[f'item_{i}' for i in self.items]+[f'domain_{k}' for k in range(1,9)]
  self.assertEqual(list(self.wide[0]),expected)
  self.assertEqual([r['respondent_id'] for r in self.wide],[f'R{n:02d}' for n in range(1,37)])
  for r in self.wide:
   self.assertEqual(WEIGHTS[r['self_rated_competence']],int(r['expertise_weight']))
   self.assertTrue(all(r[f'item_{i}'] in LABELS for i in self.items))
   self.assertTrue(all(r[f'domain_{k}'] in {'0','1','2','3','4','5'} for k in range(1,9)))
 def test_wide_and_long_files_agree(self):
  self.assertEqual(len(self.long),36*64)
  wide={r['respondent_id']:r for r in self.wide}
  for x in self.long:
   self.assertEqual(wide[x['respondent_id']][f"item_{x['item_id']}"],x['response_label'])
   self.assertEqual(LABELS[x['response_label']],int(x['raw_label_code']))
 def test_rows_reproduce_aggregate_counts_and_published_scores(self):
  raw=Counter((x['item_id'],x['expertise_weight'],x['raw_label_code']) for x in self.long)
  stored=Counter((x['item_id'],x['expertise_weight'],x['stored_code']) for x in self.long)
  for c in read('curriculum_weighted_counts.csv'):
   key=(c['item_id'],c['expertise_weight'],c['rating_code'])
   self.assertEqual((raw[key],stored[key]),(int(c['raw_count']),int(c['stored_count'])),key)
  scores=Counter();[scores.update({x['item_id']:int(x['expertise_weight'])*int(x['stored_code'])}) for x in self.long]
  for r in read('curriculum_ratings.csv'):self.assertEqual(scores[r['item_id']],int(r['reported_expertise_weighted_score']))
  self.assertEqual(sum(x['raw_label_code']!=x['stored_code'] for x in self.long),63)
if __name__=='__main__':unittest.main()
