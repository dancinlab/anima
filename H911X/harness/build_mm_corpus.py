#!/usr/bin/env python3
"""H_911 MULTIMODAL corpus builder — REAL aligned COCO captions (NO synthesis).
yerevann/coco-karpathy: each image (1 visually-grounded concept) has 5 REAL,
independently human-authored captions = 5 aligned surface forms of one concept.
The image itself is non-text so cannot enter the byte harness; the 5 forms are
the 5 human descriptions (multimodal-GROUNDED paraphrase hub). N=250 images.
Emits concept(image)-major (par) and form(caption-slot)-major (con) corpora.
"""
import json, urllib.request, time, os
BASE = "https://datasets-server.huggingface.co/rows?dataset=yerevann%2Fcoco-karpathy&config=default&split=train&offset={}&length=100"
N = 250
OUT = os.path.join(os.path.dirname(__file__), '..', 'data')

def clean(s):
    return ' '.join(str(s).replace('\t', ' ').split())

def main():
    rows = []; off = 0
    while len(rows) < N and off < 2000:
        try:
            d = json.load(urllib.request.urlopen(BASE.format(off), timeout=30))
        except Exception as e:
            print("retry", off, e); time.sleep(2)
            try: d = json.load(urllib.request.urlopen(BASE.format(off), timeout=30))
            except Exception: off += 100; continue
        for r in d['rows']:
            uniq = []
            for s in r['row']['sentences']:
                cs = clean(s)
                if cs and cs not in uniq: uniq.append(cs)
            if len(uniq) >= 5: rows.append(uniq[:5])
            if len(rows) >= N: break
        off += 100; time.sleep(0.1)
    rows = rows[:N]
    print("images selected", len(rows))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'mm_par.txt'), 'w') as p:
        for caps in rows:
            for c in caps: p.write(c + '\n')
    with open(os.path.join(OUT, 'mm_con.txt'), 'w') as c:
        for fi in range(5):
            for caps in rows: c.write(caps[fi] + '\n')

if __name__ == '__main__':
    main()
