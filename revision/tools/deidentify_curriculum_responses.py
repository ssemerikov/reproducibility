#!/usr/bin/env python3
"""Write de-identified respondent-level files from the restricted curriculum-survey workbook.

Released by author decision (1 November 2026) in response to the journal's request for raw data.

Kept: the 64 item ratings (verbatim response labels), the eight domain-importance ratings
(0-5) and the self-rated competence label.
Removed: the timestamp, the eight free-text questions, position, length of service and the
e-mail/comments field (12 columns).

Rows are ordered by response content, not by submission time, and then receive sequential
identifiers R01-R36. No row can therefore be linked to the submission order, and the output is
reproducible from the same workbook.

Outputs:
  curriculum_responses_deidentified.csv  wide, one row per respondent, verbatim labels (raw)
  curriculum_responses_coded.csv         long, respondent x item, raw-label and stored codes (processed)
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
LABELS = {'зовсім не важливо': -1, 'мало важливо': 1,
          'утруднююсь відповісти': 0, 'скоріше, важливо': 2,
          'скоріше важливо': 2, 'дуже важливо': 3}
WEIGHTS = {'маю початкові уявлення': 1,
           'обізнаний з окремими складовими': 2,
           'глибоко обізнаний з окремими складовими': 3, 'експерт': 4}
ITEM_PREFIX = 'Оцінить важливість'
DOMAIN_PREFIX = 'Оцініть за шкалою від 0 до 5'
EXPERTISE = 'Оцініть свій рівень компетентності у квантовій інформатиці'
DROPPED = ['Timestamp', 'Ваша посада', 'Стаж Вашої роботи',
           'Ваша контактна адреса електронної пошти, побажання та зауваження']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workbook', type=Path, default=ROOT / 'Квантову інформатику - в школу! (Responses).xlsx')
    parser.add_argument('--data', type=Path, default=ROOT / 'revision/data')
    parser.add_argument('--output', type=Path, default=ROOT / 'revision/data')
    args = parser.parse_args()
    digest = hashlib.sha256(args.workbook.read_bytes()).hexdigest()
    audit = json.loads((args.data / 'workbook_assessment.json').read_text())
    assert digest == audit['sha256'], 'Workbook differs from the audited original'
    book = openpyxl.load_workbook(args.workbook, read_only=True, data_only=True)
    sheet = list(book['Form Responses 1'].values)
    header = sheet[0]
    rows = [(i, r) for i, r in enumerate(sheet[1:], 2) if any(v is not None for v in r)]
    digits = list(book['digits'].values)
    items = [c for c, v in enumerate(header) if str(v).startswith(ITEM_PREFIX)]
    domains = [c for c, v in enumerate(header) if str(v).startswith(DOMAIN_PREFIX)]
    expertise = header.index(EXPERTISE)
    kept = set(items) | set(domains) | {expertise}
    dropped = [str(header[c]) for c in range(len(header)) if header[c] is not None and c not in kept]
    free_text = [h for h in dropped if h.startswith('Які додаткові')]
    assert len(rows) == 36 and len(items) == 64 and len(domains) == 8
    assert len(dropped) == 12 and len(free_text) == 8 and set(dropped) - set(free_text) == set(DROPPED)
    with (args.data / 'curriculum_ratings.csv').open(encoding='utf-8') as stream:
        item_ids = [r['item_id'] for r in csv.DictReader(stream)]
    assert len(item_ids) == 64 and all(header[c] == digits[0][c] for c in items)

    records = []
    for i, row in rows:
        labels = [row[c] for c in items]
        ratings = [row[c] for c in domains]
        assert all(label in LABELS for label in labels)
        assert all(isinstance(v, (int, float)) and v == int(v) and 0 <= v <= 5 for v in ratings)
        assert row[expertise] in WEIGHTS and WEIGHTS[row[expertise]] == digits[i - 1][expertise]
        records.append({'expertise': row[expertise], 'weight': WEIGHTS[row[expertise]],
                        'labels': labels, 'stored': [int(digits[i - 1][c]) for c in items],
                        'domains': [int(v) for v in ratings]})
    records.sort(key=lambda r: (r['weight'], r['labels'], r['domains'], r['stored']))

    wide, long = [], []
    for n, r in enumerate(records, 1):
        rid = f'R{n:02d}'
        line = {'respondent_id': rid, 'self_rated_competence': r['expertise'], 'expertise_weight': r['weight']}
        line.update({f'item_{item}': label for item, label in zip(item_ids, r['labels'])})
        line.update({f'domain_{k}': v for k, v in enumerate(r['domains'], 1)})
        wide.append(line)
        for item, label, stored in zip(item_ids, r['labels'], r['stored']):
            long.append({'respondent_id': rid, 'item_id': item, 'expertise_weight': r['weight'],
                         'response_label': label, 'raw_label_code': LABELS[label], 'stored_code': stored})

    # The released rows must reproduce the released aggregate cells exactly.
    with (args.data / 'curriculum_weighted_counts.csv').open(encoding='utf-8') as stream:
        cells = list(csv.DictReader(stream))
    raw = Counter((x['item_id'], x['expertise_weight'], x['raw_label_code']) for x in long)
    stored = Counter((x['item_id'], x['expertise_weight'], x['stored_code']) for x in long)
    for c in cells:
        key = (c['item_id'], int(c['expertise_weight']), int(c['rating_code']))
        assert raw[key] == int(c['raw_count']) and stored[key] == int(c['stored_count']), key
    assert sum(x['raw_label_code'] != x['stored_code'] for x in long) == audit['raw_numeric_response_mismatches']

    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in [('curriculum_responses_deidentified.csv', wide), ('curriculum_responses_coded.csv', long)]:
        with (args.output / name).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
    assert hashlib.sha256(args.workbook.read_bytes()).hexdigest() == digest
    print(json.dumps({'respondents': len(wide), 'item_ratings': len(long), 'dropped_columns': len(dropped),
                      'coding_mismatches': sum(x['raw_label_code'] != x['stored_code'] for x in long)}))


if __name__ == '__main__':
    main()
