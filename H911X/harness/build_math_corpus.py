#!/usr/bin/env python3
"""H_911 MATH corpus builder — REAL aligned Lean-Workbook forms (NO synthesis).
Scans internlm/Lean-Workbook (HF datasets-server), keeps N=250 theorems whose
5 forms {nl, formal, state_before, tactic, answer} are all non-empty + distinct.
Emits theorem-major (par) and proof-system-major (con) corpora, 1 form per line.
"""
import json, urllib.request, time, os
BASE = "https://datasets-server.huggingface.co/rows?dataset=internlm%2FLean-Workbook&config=default&split=train&offset={}&length=100"
FORMS = ['nl', 'formal', 'state', 'tactic', 'answer']
KEYMAP = {'nl':'natural_language_statement','formal':'formal_statement',
          'state':'state_before','tactic':'tactic','answer':'answer'}
N = 250
OUT = os.path.join(os.path.dirname(__file__), '..', 'data')

def clean(s):
    return ' '.join((s or '').replace('\t', ' ').split())  # one line per form

def main():
    seen = {}
    for off in range(0, 3000, 100):
        try:
            d = json.load(urllib.request.urlopen(BASE.format(off), timeout=30))
        except Exception as e:
            print("retry", off, e); time.sleep(2)
            d = json.load(urllib.request.urlopen(BASE.format(off), timeout=30))
        for r in d['rows']:
            row = r['row']; tid = row['id']
            if tid not in seen:
                seen[tid] = {k: clean(row.get(KEYMAP[k])) for k in FORMS}
        time.sleep(0.1)
    rows = []
    for tid, f in seen.items():
        vals = [f[k] for k in FORMS]
        if all(vals) and len(set(vals)) == 5:
            rows.append(vals)
    rows = rows[:N]
    print("unique theorems", len(seen), "selected", len(rows))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'math_par.txt'), 'w') as p:
        for vals in rows:
            for v in vals: p.write(v + '\n')
    with open(os.path.join(OUT, 'math_con.txt'), 'w') as c:
        for fi in range(5):
            for vals in rows: c.write(vals[fi] + '\n')

if __name__ == '__main__':
    main()
