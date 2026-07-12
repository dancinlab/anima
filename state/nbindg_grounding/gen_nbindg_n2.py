#!/usr/bin/env python3
"""gen_nbindg_n2.py — NBIND-G N2 grounding corpus + PRE-FIRE audit gate ($0 before pool spend).

N2 = the GROUNDING body of NBIND-G (H_9286). N1 (🟢-dir CARRIER-ROBUST) proved the grid-learned
XOR operator is carrier-general on GROUNDED grid atoms. N2 asks the frontier question: does that
operator apply to atoms whose polarity is grounded ONLY in natural distributional usage — never
stamped in any authored grid cell?

Design (Fable arbitration §3.1/§3.4, frozen):
  · P_grid  = the 20 H_9272 grid predicates → authored XOR grid teaches the flip OPERATOR.
  · P_nat   = held-out grounding predicates → appear ONLY inside verbatim natural NSMC reviews
              (filler); NEVER in an authored `이 영화 <surf> => token` line (V-F byte-scan).
  · 3 arms (collapse-Δ, not raw):
      main         = authored grid(P_grid) + natural NSMC mix (P_nat grounded distributionally)
      base-only    = identical natural mix, NO grid   (what nature alone installs — the crux;
                     subtracts generic negation-handling a plain LM gives for free)
      shuffle-grid = grid with per-cell coin (XOR destroyed, continuation FORMAT preserved) + mix
                     (separates "grid taught the answer format" from "grid taught the operator")
  · eval = P_nat × 6 forms held-out (p,n), XBIND-isomorphic `이 영화 <surf> => 긍정/부정`; gold =
    xor(pol(p), flip(n)) derivable ONLY by (a) extracting pol(p) from natural usage + (b) applying
    the grid-learned flip. Same in-distribution readout as the grid.

PRE-FIRE AUDIT GATE ($0, before ANY pool spend — frozen-first):
  For every p in P_nat, distributional polarity must be model-free decidable AND p must be
  renderable in all 6 forms (non-past stem for 지않다, sentiment-pure). Frozen bars:
    · per-atom: purity >= 0.85 over >= 100 non-negated NSMC occurrences; not-past-stem; syll<=3.
    · inventory: >= 10 renderable P_nat per polarity (else INVALID — the natural sentiment-atom
      inventory is too sparse/noisy for a clean grounding test; a legitimate $0 finding, NOT a
      dressed-up wall).
    · eval n = |P_nat_viable| * 6 >= 120 (paired-t MDE on Δ(main-base-only) ~ 0.13 @ n=120).
  INVALID => corpus NOT built, pool spend BLOCKED. No tune-to-green: bars frozen here.

Usage:
  python3 gen_nbindg_n2.py --out-dir . [--nsmc <path>] [--seed 7] [--audit-only]
"""
import collections
import json
import os
import random
import sys

_NBIND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nbind_curriculum")
sys.path.insert(0, _NBIND_DIR)
import gen_nbind as GN

PURITY_NAT = 0.85          # relaxed vs grid 0.90 (Fable §3.1) — grid exhausts the 0.90 tier
MINOCC_NAT = 100
K_MIN_PER_POL = 10         # inventory floor (else INVALID)
REP_GRID = GN.REP          # authored grid rep (match H_9272)

# Fable N2 recipe (exposure-matched · avoids the STAGE-1 exposure-confound INVALID):
# exposure is a BYTE phenomenon, not a line count. The old NSMC_FILLER_MULT=8 (lines) gave
# grid byte-fraction f_grid≈0.059 → at 20k steps grid exposure≈1.2k ≪ E*=12k = a pre-built
# STAGE-1 INVALID. Fix: denominate filler in BYTES (target f_grid=0.25), bias fill toward
# P_nat-bearing reviews (grounding-per-byte), enforce a per-atom occurrence floor, and derive
# train steps T = ceil(T_MARGIN * E_STAR / f_grid) from the BUILT corpus's actual bytes.
FILLER_BYTE_RATIO = 3.0    # filler bytes = 3x grid bytes → f_grid = 1/(1+3) = 0.25
E_STAR = 12000             # STAGE-1 measured exposure knee (grid held-out D-acc 8k→12k)
T_MARGIN = 1.25            # margin over E* (sharp knee + mixed-corpus interference slack)
ATOM_OCC_CAP = 60          # max P_nat-bearing reviews admitted per atom (fill balance)
ATOM_OCC_FLOOR = 30        # min occurrences of each atom in the BUILT corpus (else drop atom)

# external Korean sentiment corpora (public · $0) — enlarge the purity-certified atom pool
# beyond NSMC's ~13 clean non-grid predicates (N2 pre-fire INVALID at NSMC-only scale).
_NATEM = os.path.expanduser("~/g1_natem")
POOL_CORPORA = {"naver_shopping": _NATEM + "/naver_shopping.txt",   # <rating 1-5>\t<text>
                "steam": _NATEM + "/steam.txt"}                    # <label 0/1>\t<text>


def load_corpora(nsmc_path=None, extra=True):
    """Unified (text, label 0/1) rows. NSMC(movies) + naver_shopping(products·rating) +
    steam(games·label). Domain diversity → new sentiment predicates the grid never saw."""
    rows = list(GN.load_nsmc(nsmc_path))
    if not extra:
        return rows
    ns = POOL_CORPORA["naver_shopping"]
    if os.path.exists(ns):
        for line in open(ns, encoding="utf-8"):
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 2 and pp[0].isdigit():
                r = int(pp[0])
                if r <= 2:
                    rows.append((pp[1], 0))
                elif r >= 4:
                    rows.append((pp[1], 1))
    st = POOL_CORPORA["steam"]
    if os.path.exists(st):
        for line in open(st, encoding="utf-8"):
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 2 and pp[0] in ("0", "1"):
                rows.append((pp[1], int(pp[0])))
    return rows


def audit_pnat(rows, grid_stems, seed):
    """Certify each candidate P_nat: purity/occ/renderable. Returns (viable list, audit dict)."""
    preds = GN.mine_predicates(rows, MINOCC_NAT, PURITY_NAT)
    cand = {p: d for p, d in preds.items()
            if p not in grid_stems and not GN.is_past_stem(p) and GN.syll(p) <= GN.MAX_SYLL}
    pos = sorted([p for p, d in cand.items() if d["pol"] == 1], key=lambda p: -cand[p]["n"])
    neg = sorted([p for p, d in cand.items() if d["pol"] == 0], key=lambda p: -cand[p]["n"])
    k = min(len(pos), len(neg), 15)
    viable = pos[:k] + neg[:k]
    n_eval = len(viable) * len(GN.NEG_FORMS)
    audit = {
        "purity_bar": PURITY_NAT, "minocc_bar": MINOCC_NAT,
        "n_cand_pos": len(pos), "n_cand_neg": len(neg), "k_per_pol": k,
        "n_pnat_viable": len(viable), "n_eval_items": n_eval,
        "GATE_k_per_pol_ok": k >= K_MIN_PER_POL,
        "GATE_n_eval_ok": n_eval >= 120,
        "viable": [{"stem": p, "pol": cand[p]["pol"], "n": cand[p]["n"],
                    "purity": cand[p]["purity"]} for p in viable],
    }
    audit["PREFIRE_PASS"] = audit["GATE_k_per_pol_ok"] and audit["GATE_n_eval_ok"]
    return viable, cand, audit


def build_n2(nsmc_rows, pool_rows, seed):
    B = GN.build(nsmc_rows, seed)                   # H_9272 grid (NSMC-only · P_grid frozen)
    grid_stems = set(B["plist"])
    viable, cand, audit = audit_pnat(pool_rows, grid_stems, seed)
    if not audit["PREFIRE_PASS"]:
        return None, audit, B
    NF = dict((f[0], f[2]) for f in GN.NEG_FORMS)
    rng = random.Random(seed)

    # authored grid lines (verbatim H_9272 main + shuffle) — teaches the operator on P_grid only
    grid_main = B["main_lines"][:]
    grid_shuf = B["ctrl_lines"][:]
    grid_bytes = len("\n".join(grid_main).encode())

    # V-F pre-filter: drop any P_nat atom whose stem appears as a SUBSTRING in an authored grid
    # line (e.g. "좋" nests inside a P_grid predicate surface). Such an atom would be partly
    # grounded BY THE GRID, contaminating the pure-nature grounding claim. Exclude → recheck.
    _authored = "\n".join(grid_main + grid_shuf)
    _collide = [p for p in viable if p in _authored]
    viable = [p for p in viable if p not in _collide]
    audit["V_F_authored_collision_dropped"] = _collide
    if len(viable) * len(GN.NEG_FORMS) < 120:
        audit["n_eval_items"] = len(viable) * len(GN.NEG_FORMS)
        audit["GATE_n_eval_ok"] = False
        audit["PREFIRE_PASS"] = False
        return None, audit, B

    # --- Fable §1: BIASED byte-target fill toward P_nat-bearing reviews ---
    # per-atom round-robin over reviews containing that atom (cap ATOM_OCC_CAP/atom), then top
    # up with general (atom-free) reviews to hit filler byte target = FILLER_BYTE_RATIO*grid.
    vset = set(viable)
    by_atom = {p: [] for p in viable}
    general = []
    for text, _lab in pool_rows:
        t = text.strip()
        if not t or "=>" in t or "긍정" in t or "부정" in t:
            continue
        hit = [st for st in vset if st in t]
        if hit:
            for st in hit:
                if len(by_atom[st]) < ATOM_OCC_CAP:
                    by_atom[st].append(t)
        elif len(general) < 200000:
            general.append(t)
    # round-robin the per-atom pools (dedup) for a balanced grounding channel
    seen_lines, grounding = set(), []
    for i in range(ATOM_OCC_CAP):
        for p in viable:
            if i < len(by_atom[p]):
                ln = by_atom[p][i]
                if ln not in seen_lines:
                    seen_lines.add(ln)
                    grounding.append(ln)
    target_bytes = int(grid_bytes * FILLER_BYTE_RATIO)
    rng.shuffle(general)
    nat_filler = grounding[:]
    gi = 0
    while len("\n".join(nat_filler).encode()) < target_bytes and gi < len(general):
        nat_filler.append(general[gi]); gi += 1
    rng.shuffle(nat_filler)

    # --- Fable §1: per-atom corpus-occurrence floor (drop under-floor atoms, recheck n_eval) ---
    filler_blob = "\n".join(nat_filler)
    occ = {p: filler_blob.count(p) for p in viable}
    viable = [p for p in viable if occ[p] >= ATOM_OCC_FLOOR]
    vset = set(viable)
    audit["atom_occ_in_corpus"] = {p: occ[p] for p in occ}
    audit["n_pnat_after_floor"] = len(viable)
    audit["n_eval_items"] = len(viable) * len(GN.NEG_FORMS)
    audit["GATE_n_eval_ok"] = audit["n_eval_items"] >= 120
    audit["PREFIRE_PASS"] = audit["GATE_k_per_pol_ok"] and audit["GATE_n_eval_ok"]
    if not audit["PREFIRE_PASS"]:
        return None, audit, B

    def corpus(grid_lines, extra=None):
        lines = grid_lines + nat_filler + (extra or [])
        random.Random(seed + 5).shuffle(lines)
        return "\n".join(lines) + "\n"

    main_txt = corpus(grid_main)
    # base_only: NO grid — pad with general reviews to byte-match main within +-2% (Fable §2)
    pad = []
    while (len(("\n".join(nat_filler + pad)).encode()) < len(main_txt.encode()) * 0.98
           and gi < len(general)):
        pad.append(general[gi]); gi += 1
    base_txt = corpus([], extra=pad)
    shuf_txt = corpus(grid_shuf)

    # --- Fable §2: exposure-matched steps from BUILT corpus bytes ---
    main_bytes = len(main_txt.encode())
    f_grid = grid_bytes / main_bytes
    t_required = int(-(-(T_MARGIN * E_STAR) // f_grid))     # ceil
    audit["grid_bytes"] = grid_bytes
    audit["f_grid_bytes"] = round(f_grid, 4)
    audit["T_required"] = t_required
    audit["GATE_exposure_ok"] = t_required * f_grid >= T_MARGIN * E_STAR

    # N2 eval manifest: P_nat x 6 forms held-out XOR (same readout as grid)
    er = random.Random(seed + 97)
    NFk = NF
    items = []
    for p in viable:
        span_list = cand[p]["spans"]
        for fid in [f[0] for f in GN.NEG_FORMS]:
            span = er.choice(span_list) if span_list else (None, p)
            surf = GN.render(p, span[1], span[0], NFk[fid])
            bit = cand[p]["pol"] ^ GN.FLIP[fid]
            items.append({"p": p, "form": fid, "a": p, "b": fid,
                          "pol": cand[p]["pol"], "flip": GN.FLIP[fid], "xor": bit,
                          "surf": surf, "seed": "이 영화 " + surf + " => ",
                          "gold": ("긍정." if bit else "부정."),
                          "counterfactual": ("부정." if bit else "긍정."),
                          "gold_word": "긍정" if bit else "부정"})
    manifest = {"format": "nbind-eval-v1", "task": "NBIND-G N2 grounding (P_nat held-out XOR)",
                "gen": 8, "win": 64, "heldout": items, "seen": []}

    # V-F byte-scan: (1) no viable P_nat stem in any AUTHORED grid line (main or shuffle);
    #                (2) no eval seed appears verbatim in any training line.
    authored = grid_main + grid_shuf
    leak_atom = sum(1 for ln in authored for st in vset if st in ln)
    eval_seeds = set(it["seed"] for it in items)
    all_train = authored + nat_filler
    leak_seed = sum(1 for ln in all_train if any(s in ln for s in eval_seeds))
    audit["V_F_pnat_in_authored"] = leak_atom
    audit["V_F_eval_seed_in_train"] = leak_seed
    audit["V_F_pass"] = (leak_atom == 0 and leak_seed == 0)
    audit["n_grid_main_lines"] = len(grid_main)
    audit["n_nat_filler_lines"] = len(nat_filler)
    audit["n_grounding_reviews"] = len(grounding)
    audit["bytes"] = {"main": len(main_txt.encode()), "base_only": len(base_txt.encode()),
                      "shuffle_grid": len(shuf_txt.encode())}
    audit["byte_match_base_vs_main"] = round(len(base_txt.encode()) / len(main_txt.encode()), 3)
    corp = {"main": main_txt, "base_only": base_txt, "shuffle_grid": shuf_txt}
    return {"manifest": manifest, "corpora": corp}, audit, B


def main():
    args = sys.argv[1:]

    def val(flag, default, cast):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    out_dir = val("--out-dir", ".", str)
    nsmc = val("--nsmc", None, str)
    seed = val("--seed", 7, int)
    audit_only = "--audit-only" in args
    multi = "--corpora" in args          # add external naver_shopping + steam to the atom pool

    nsmc_rows = GN.load_nsmc(nsmc)        # grid always NSMC-only (H_9272 P_grid frozen)
    pool_rows = load_corpora(nsmc, extra=multi)   # P_nat mining + grounding filler pool
    if audit_only:
        B = GN.build(nsmc_rows, seed)
        viable, cand, audit = audit_pnat(pool_rows, set(B["plist"]), seed)
        audit["n_pool_rows"] = len(pool_rows)
        audit["multi_corpus"] = multi
        with open(out_dir + "/N2_PREFIRE_AUDIT.json", "w") as f:
            json.dump(audit, f, ensure_ascii=False, indent=1)
        print(json.dumps({k: audit[k] for k in
                          ("purity_bar", "n_cand_pos", "n_cand_neg", "k_per_pol",
                           "n_pnat_viable", "n_eval_items", "GATE_k_per_pol_ok",
                           "GATE_n_eval_ok", "PREFIRE_PASS")}, ensure_ascii=False, indent=1))
        return 0

    out, audit, B = build_n2(nsmc_rows, pool_rows, seed)
    audit["n_pool_rows"] = len(pool_rows)
    audit["multi_corpus"] = multi
    with open(out_dir + "/N2_PREFIRE_AUDIT.json", "w") as f:
        json.dump(audit, f, ensure_ascii=False, indent=1)
    if out is None:
        print(json.dumps(audit, ensure_ascii=False, indent=1))
        print("N2 PRE-FIRE GATE FAILED — POOL SPEND BLOCKED (natural atom inventory insufficient)",
              file=sys.stderr)
        return 1
    for arm, txt in out["corpora"].items():
        with open(out_dir + "/n2_%s_train.txt" % arm, "w") as f:
            f.write(txt)
    with open(out_dir + "/n2_eval_manifest.json", "w") as f:
        json.dump(out["manifest"], f, ensure_ascii=False, indent=1)
    print(json.dumps(audit, ensure_ascii=False, indent=1))
    if not audit["V_F_pass"]:
        print("V-F LEAK — corpus invalid, do NOT spend", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    main()
