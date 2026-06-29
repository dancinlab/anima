#!/usr/bin/env python3
"""tabulate.py <dir-of-g0g6-txt> — parse anima evaluate G0-G6 outputs into a table.

Reads every *.g0g6.txt produced by cli/evaluate.py (the `anima evaluate` banner +
gate lines) and emits a per-ckpt row: G0 pass, G1 best_distinct/max_single/pass,
G2 pass, G6 dist/fals/pass, closure. Used to build H_1640/1641/1602 RESULT tables.
"""
import os, re, sys, glob, json

def parse(txt):
    r = {}
    m = re.search(r"G0 COHERENCE\s+(\S+ \S+|\S+)\s+kwr.*?on (\d+)/5", txt)
    r["g0_pass"] = "PASS" in (m.group(0) if m else "")
    r["g0_coh"] = m.group(2) if m else "?"
    m = re.search(r"G1 RECOMBINATION\s+(🟢 PASS|🔴 FAIL).*?best_distinct=(\d+) > max_single=(\d+)", txt)
    if m:
        r["g1_pass"] = "PASS" in m.group(1); r["g1_best"] = int(m.group(2)); r["g1_max"] = int(m.group(3))
    else:
        r["g1_pass"] = None; r["g1_best"] = None; r["g1_max"] = None
    m = re.search(r"G2 NOVELTY\s+(🟢 PASS|🔴 FAIL).*?novel=(\d+).*?control=(\d+)", txt)
    if m:
        r["g2_pass"] = "PASS" in m.group(1); r["g2_novel"] = int(m.group(2)); r["g2_ctrl"] = int(m.group(3))
    else:
        r["g2_pass"] = None
    m = re.search(r"G6 IDEATION.*?(🟢 PASS|🔴 FAIL).*?distinct=(\d+).*?falsifiable=(\d+)", txt)
    if m:
        r["g6_pass"] = "PASS" in m.group(1); r["g6_dist"] = int(m.group(2)); r["g6_fals"] = int(m.group(3))
    else:
        r["g6_pass"] = None; r["g6_dist"] = None; r["g6_fals"] = None
    m = re.search(r"CLOSURE.*?(🟢 PASS|🔴 FAIL)", txt)
    r["closure"] = ("PASS" in m.group(1)) if m else None
    return r

def main(d):
    rows = []
    for f in sorted(glob.glob(os.path.join(d, "*.g0g6.txt"))):
        name = os.path.basename(f)[:-len(".g0g6.txt")]
        try:
            r = parse(open(f, encoding="utf-8", errors="replace").read())
        except Exception as e:
            r = {"err": str(e)}
        r["ckpt"] = name; rows.append(r)
    hdr = f"{'ckpt':<32} G0 G0coh | G1 best/max pass | G2 | G6 dist/fals pass | CLOSURE"
    print(hdr); print("-"*len(hdr))
    for r in rows:
        if "err" in r:
            print(f"{r['ckpt']:<32} PARSE-ERR {r['err']}"); continue
        g0 = "✓" if r["g0_pass"] else "✗"
        g1 = f"{r['g1_best']}/{r['g1_max']} {'✓' if r['g1_pass'] else '✗'}" if r["g1_pass"] is not None else "—"
        g2 = "✓" if r.get("g2_pass") else "✗"
        g6 = f"{r['g6_dist']}/{r['g6_fals']} {'✓' if r['g6_pass'] else '✗'}" if r["g6_pass"] is not None else "—"
        cl = "🟢" if r["closure"] else ("🔴" if r["closure"] is not None else "—")
        print(f"{r['ckpt']:<32} {g0}  {r['g0_coh']}/5  | {g1:<16} | {g2}  | {g6:<14} | {cl}")
    print()
    print(json.dumps(rows, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
