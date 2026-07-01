#!/usr/bin/env python3
"""
Parse g0g6.txt files from H_1818 and H_1819 evaluations.
Run locally after pulling results from pod:
  scp -P 11218 root@ssh1.vast.ai:'/root/anima/state/g1_cotrain_recomb_bind/ckpt/*.g0g6.txt' state/g1_cotrain_recomb_bind/ckpt/
  scp -P 11218 root@ssh1.vast.ai:'/root/anima/state/g1_cotrain_live_bind/ckpt/*.g0g6.txt' state/g1_cotrain_live_bind/ckpt/

Usage: python3 state/g1_cotrain_recomb_bind/parse_results.py [--h1818] [--h1819]
"""
import os, sys, re, glob, json

ARMS_1819 = ["op_plaince", "obj_only", "op_obj"]
SEEDS = [7, 4302, 4303]

def parse_g0g6(path):
    """Extract G0/G1/G2/G6/closure metrics from g0g6.txt.

    Output format (from cli/evaluate.py):
      G0 COHERENCE     🟢 PASS  kwr>=0.50 on 4/5 (need >=4)
      G1 RECOMBINATION 🔴 FAIL  best_distinct=1 > max_single=1 (need >=2 & >max_single)
      G2 NOVELTY       🔴 FAIL  novel=0 (need>=3) · control=0 (need 0) · coherent=0
      G6 IDEATION ★    🔴 FAIL  distinct=5 (need>=5) · falsifiable=0 (need>=1) · frame-leaks=0
      CLOSURE (a7b_pass = G0 ∧ G1 ∧ G2): 🔴 FAIL
    """
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None
    txt = open(path).read()
    result = {}

    # G0: n_coherent from "kwr>=0.50 on X/5"
    m = re.search(r'G0 COHERENCE.*?on\s+(\d+)/5', txt)
    if m:
        result['g0_n_coherent'] = int(m.group(1))
        result['g0_pass_bool'] = result['g0_n_coherent'] >= 4
    # G0 PASS/FAIL emoji
    m = re.search(r'G0 COHERENCE\s+(🟢 PASS|🔴 FAIL)', txt)
    if m:
        result['g0_verdict'] = 'PASS' if '🟢' in m.group(1) else 'FAIL'

    # G1: best_distinct and max_single
    m = re.search(r'G1 RECOMBINATION.*?best_distinct=(\d+).*?max_single=(\d+)', txt)
    if m:
        result['g1_best_distinct'] = int(m.group(1))
        result['g1_max_single'] = int(m.group(2))
    m = re.search(r'G1 RECOMBINATION\s+(🟢 PASS|🔴 FAIL)', txt)
    if m:
        result['g1_verdict'] = 'PASS' if '🟢' in m.group(1) else 'FAIL'

    # G2: novel, control, coherent
    m = re.search(r'G2 NOVELTY.*?novel=(\d+).*?control=(\d+).*?coherent=(\d+)', txt)
    if m:
        result['g2_novel'] = int(m.group(1))
        result['g2_control'] = int(m.group(2))
        result['g2_coherent'] = int(m.group(3))
    m = re.search(r'G2 NOVELTY\s+(🟢 PASS|🔴 FAIL)', txt)
    if m:
        result['g2_verdict'] = 'PASS' if '🟢' in m.group(1) else 'FAIL'

    # G5: fab rate
    m = re.search(r'G5 NON-FAB.*?L1 fab=([0-9.]+)', txt)
    if m:
        result['g5_l1_fab'] = float(m.group(1))
    m = re.search(r'G5 NON-FAB\s+(🟢 PASS|🔴 FAIL)', txt)
    if m:
        result['g5_verdict'] = 'PASS' if '🟢' in m.group(1) else 'FAIL'

    # G6: distinct and falsifiable (anchored to G6 line to avoid matching G1 best_distinct)
    m = re.search(r'G6 IDEATION.*?distinct=(\d+).*?falsifiable=(\d+)', txt)
    if m:
        result['g6_dist'] = int(m.group(1))
        result['g6_fals'] = int(m.group(2))
    m = re.search(r'G6 IDEATION', txt)
    if m:
        g6_line = txt[m.start():m.start()+200]
        m2 = re.search(r'(🟢 PASS|🔴 FAIL)', g6_line)
        if m2:
            result['g6_verdict'] = 'PASS' if '🟢' in m2.group(1) else 'FAIL'

    # CLOSURE: match "🟢 PASS" or "🔴 FAIL" after CLOSURE line
    m = re.search(r'CLOSURE.*?:\s*(🟢 PASS|🔴 FAIL)', txt)
    if m:
        result['closure'] = 'PASS' if '🟢' in m.group(1) else 'FAIL'
        result['a7b_pass'] = result['closure'] == 'PASS'

    return result if result else None


def parse_h1819():
    ckpt_dir = "state/g1_cotrain_recomb_bind/ckpt"
    print("=== H_1819: 3-arm co-trained bind op × recomb objective ===")
    print()
    table = []
    for arm in ARMS_1819:
        for seed in SEEDS:
            g0g6 = os.path.join(ckpt_dir, f"{arm}_seed{seed}.g0g6.txt")
            parsed = parse_g0g6(g0g6)
            table.append((arm, seed, parsed))

    print("| arm | seed | G0 kwr | G1 composed_dist | G1 max_single | G6 dist | G6 fals | a7b? |")
    print("|-----|------|--------|-----------------|---------------|---------|---------|------|")
    for arm, seed, p in table:
        if p is None:
            print(f"| {arm} | {seed} | (pending) | — | — | — | — | — |")
        else:
            kwr = p.get('g0_kwr', '—')
            cd = p.get('g1_composed_distinct', p.get('g1_best_distinct', '—'))
            ms = p.get('g1_max_single', '—')
            dist = p.get('g6_dist', '—')
            fals = p.get('g6_fals', '—')
            a7b = p.get('a7b_pass', p.get('closure', '—'))
            print(f"| {arm} | {seed} | {kwr} | {cd} | {ms} | {dist} | {fals} | {a7b} |")

    print()
    print("=== PREREG DECISION TEST ===")
    # Collect op_obj, op_plaince, obj_only per seed
    results = {}
    for arm, seed, p in table:
        if p is not None:
            if seed not in results:
                results[seed] = {}
            results[seed][arm] = p

    decided = []
    for seed in SEEDS:
        if seed not in results:
            continue
        sr = results[seed]
        c_cd = sr.get('op_obj', {}).get('g1_composed_distinct', sr.get('op_obj', {}).get('g1_best_distinct', None))
        a_cd = sr.get('op_plaince', {}).get('g1_composed_distinct', sr.get('op_plaince', {}).get('g1_best_distinct', None))
        b_cd = sr.get('obj_only', {}).get('g1_composed_distinct', sr.get('obj_only', {}).get('g1_best_distinct', None))
        if c_cd is not None and a_cd is not None and b_cd is not None:
            lift = (c_cd > a_cd) and (c_cd > b_cd)
            print(f"  seed {seed}: op_obj={c_cd} vs op_plaince={a_cd} vs obj_only={b_cd} → LIFT={'YES' if lift else 'NO'}")
            decided.append(lift)
        else:
            print(f"  seed {seed}: PENDING (missing data)")

    if decided:
        wins = sum(decided)
        print(f"\nDecision test: {wins}/{len(decided)} seeds LIFT (need ≥2/3)")
        if wins >= 2:
            print("→ SUPPORTED: op_obj lifts G1 composed_distinct > both controls")
            print("→ NEXT: escalate to core/clm_decode.hexa CLMB lockstep wiring (a_verified_must_wire)")
        else:
            print("→ NOT-SUPPORTED at PREREG bar")


def parse_h1818():
    ckpt_dir = "state/g1_cotrain_live_bind/ckpt"
    print("=== H_1818: co-trained LIVE bind op (bind vs ctrl) ===")
    print()

    table = []
    for arm in ["bind", "ctrl"]:
        for seed in SEEDS:
            g0g6 = os.path.join(ckpt_dir, f"{arm}_seed{seed}.g0g6.txt")
            parsed = parse_g0g6(g0g6)
            table.append((arm, seed, parsed))

    print("| arm | seed | G0 kwr | G1 composed_dist | G1 max_single | G6 dist | G6 fals | a7b? |")
    print("|-----|------|--------|-----------------|---------------|---------|---------|------|")
    for arm, seed, p in table:
        if p is None:
            print(f"| {arm} | {seed} | (pending) | — | — | — | — | — |")
        else:
            kwr = p.get('g0_kwr', '—')
            cd = p.get('g1_composed_distinct', p.get('g1_best_distinct', '—'))
            ms = p.get('g1_max_single', '—')
            dist = p.get('g6_dist', '—')
            fals = p.get('g6_fals', '—')
            a7b = p.get('a7b_pass', p.get('closure', '—'))
            print(f"| {arm} | {seed} | {kwr} | {cd} | {ms} | {dist} | {fals} | {a7b} |")

    print()
    # Check if bind > ctrl
    results = {}
    for arm, seed, p in table:
        if p is not None:
            if seed not in results:
                results[seed] = {}
            results[seed][arm] = p
    for seed in SEEDS:
        if seed not in results:
            continue
        sr = results[seed]
        b_cd = sr.get('bind', {}).get('g1_composed_distinct', sr.get('bind', {}).get('g1_best_distinct', None))
        c_cd = sr.get('ctrl', {}).get('g1_composed_distinct', sr.get('ctrl', {}).get('g1_best_distinct', None))
        if b_cd is not None and c_cd is not None:
            print(f"  seed {seed}: bind G1={b_cd} vs ctrl G1={c_cd} → {'bind>ctrl' if b_cd > c_cd else 'bind≤ctrl'}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or '--h1818' in args:
        parse_h1818()
        print()
    if not args or '--h1819' in args:
        parse_h1819()
