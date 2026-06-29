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
    """Extract G0 kwr, G1 composed_distinct/max_single, G6 dist/fals from g0g6.txt."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None
    txt = open(path).read()
    result = {}
    # G0: kwr
    m = re.search(r'G0.*?kwr[=: ]+([0-9.]+)', txt, re.IGNORECASE)
    if m:
        result['g0_kwr'] = float(m.group(1))
    m = re.search(r'kwr[=: ]+([0-9.]+)', txt)
    if m and 'g0_kwr' not in result:
        result['g0_kwr'] = float(m.group(1))
    # G0 pass
    m = re.search(r'G0[^:]*:[^|]*(\d+)/5', txt)
    if m:
        result['g0_pass'] = int(m.group(1))
    # G1: composed_distinct
    m = re.search(r'composed_distinct[=: ]+([0-9.]+)', txt, re.IGNORECASE)
    if m:
        result['g1_composed_distinct'] = float(m.group(1))
    # G1: max_single
    m = re.search(r'max_single[=: ]+([0-9.]+)', txt, re.IGNORECASE)
    if m:
        result['g1_max_single'] = float(m.group(1))
    # G1 best_distinct
    m = re.search(r'best_distinct[=: ]+([0-9.]+)', txt, re.IGNORECASE)
    if m:
        result['g1_best_distinct'] = float(m.group(1))
    # G1 pass
    m = re.search(r'G1[^:]*:\s*(PASS|FAIL|NOT-SUPPORTED)', txt, re.IGNORECASE)
    if m:
        result['g1_verdict'] = m.group(1)
    # G6 dist
    m = re.search(r'G6[^:]*dist[=: ]+([0-9.]+)', txt, re.IGNORECASE)
    if not m:
        m = re.search(r'dist[=: ]+([0-9.]+)', txt)
    if m:
        result['g6_dist'] = float(m.group(1))
    # G6 fals
    m = re.search(r'fals[=: ]+([0-9.]+)', txt, re.IGNORECASE)
    if m:
        result['g6_fals'] = float(m.group(1))
    # a7b_pass
    m = re.search(r'a7b_pass[=: ]+(True|False|1|0)', txt, re.IGNORECASE)
    if m:
        result['a7b_pass'] = m.group(1) in ('True', '1')
    # closure
    m = re.search(r'closure[=: ]+(PASS|FAIL)', txt, re.IGNORECASE)
    if m:
        result['closure'] = m.group(1)
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
