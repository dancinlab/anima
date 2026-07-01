#!/usr/bin/env python3
"""h1434_twopass_bind.py — G6 IDEATION ★ FALS-depth wall: TWO-PASS elicit-then-bind.

HYPOTHESIS H_1434 (a_break_the_wall · NEW lens after the 4-fold capacity wall):
  G6 IDEATION ★ FALS-depth is 4x-confirmed walled at 303M (H_1309 budget plateau ·
  H_1314 form FALS=0 · H_1431 external-compose FALS=0 · H_1432 negation-slot FALS=0).
  But H_1431's bottleneck diagnostic gave the DECISIVE clue: in one generation the
  303M mouth emits a frozen COMPARATOR token 20% · a frozen MEASURABLE token 27% ·
  **BOTH 0/15 (0%)**. Each leg is in-capacity in its OWN draw; they are mutually
  exclusive WITHIN one draw. Every prior dig welded both legs out of ONE generation
  (H_1431 took the union of one idea's two native fragments) — so the binder was
  starved: 0/15 co-occurrence.

  NEW MECHANISM (genuinely different — NOT tune-to-green, NOT a 1305/1309/1314/1431/
  1432 re-run): DON'T force both legs into one draw. Pull each leg from its OWN
  dedicated decode pass with a multi-sample BUDGET, then deterministically WELD the
  two SEPARATELY-elicited legs into one negatable claim.
    pass1 (COMPARATOR leg): N budgeted draws toward a comparative fragment; keep the
      FIRST draw that emits a frozen COMPARATOR token (each leg ~20%/draw -> 1-0.8^N).
    pass2 (MEASURABLE leg): N budgeted draws toward a measurable fragment; keep the
      FIRST draw that emits a frozen MEASURABLE token (~27%/draw -> 1-0.73^N).
  Then weld comp_tok (pass1) + meas_tok (pass2) + mouth content into one declarative
  negatable claim the FROZEN H_1305 detector scores. The two legs come from SEPARATE
  draws, so within-draw mutual-exclusion (the 0/15 wall) no longer applies.

  If this crosses FALS>=1 with the controls surviving -> the G6 FALS-depth wall was
  NOT a capacity ceiling but a "one-draw-forced" artifact: 303M HAS the material, it
  just never co-emits it in one breath. (303M-native breakthrough, no bigger model.)

FROZEN 5-bar (declared in FREEZE.txt BEFORE scoring — c9, NO tune-to-green):
  (1) FALS>=1 cross  : TWO_PASS achieves mean FALS >= 1 (breaks the 0 plateau the
        prior 4 digs hit; H_1431's best was 0.333).
  (2) count>=5 dist  : TWO_PASS >= 5 pairwise-Jaccard<0.5 distinct ideas.
  (3) cross-pair SHUFFLE COLLAPSE : pairing seedA's comparator-leg with seedB's
        measurable-leg (a DIFFERENT idea's leg, random derangement) drops FALS below
        TWO_PASS-1 — the bind tracks the EARNED per-idea pairing, not a generic concat
        that always satisfies the detector.
  (4) ablate TWO_PASS->SINGLE_PASS INERT : with budget=1 and BOTH legs forced from
        ONE shared draw (the H_1431/H_1314 regime), FALS returns to the ~0 floor
        (FALS_single <= TWO_PASS-1) — the two-pass separation is load-bearing.
  (5) NO-FAB : the p7 token-inject audit is CLEAN — no priming seed and no weld
        function token carries a frozen COMPARATOR/MEASURABLE token. The mouth must
        EARN every detector leg. (leak => ABORT + re-freeze.)

VERDICT:
  🟢 if (1)&(2) cross AND (3)&(4)&(5) controls survive: the wall was "one-draw-forced",
     303M-native breakthrough (the material was always there; co-emission was the gap).
  🧱 if TWO_PASS does NOT cross AND single-pass==two-pass: the bind is capacity-bound
     even with separated draws (5th independent confirmation) -> decisive H_1433 7B
     grounding.

Reuses the H_1305 frozen `_is_falsifiable` detector VERBATIM (imported) + gauge_lib._decode
(the SAME live G6 decode path) VERBATIM. 3 seeds. 303M torch-mouth on summer CUDA.
The detector, weld schema, and 5-bar are FROZEN IDENTICAL to H_1431 (FREEZE-locked); ONLY
the per-leg separated multi-sample extraction is new (a_engine_native_learning DIRECTIONAL).
"""
import sys, os, json, importlib.util, time, random

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))  # state/1434_twopass_bind/.. -> state -> root
CKPT = os.environ.get("H1302_CKPT", os.path.join(ANIMA, "state", "chat_303m", "h1129c_chat.pt"))
CORPUS = os.environ.get("H1302_CORPUS", os.path.join(ANIMA, "data", "corpus.txt"))
PROBES = os.path.join(ANIMA, "state", "universe-probes")
GAUGE = os.environ.get("H1434_GAUGE", os.path.join(PROBES, "gauge_lib.py"))
if not os.path.exists(GAUGE):
    GAUGE = os.path.join(ANIMA, "tool", "gauge_lib.py")
H1129 = os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py")
H1305 = os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py")

import torch


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


g  = _load("gauge", GAUGE)
h  = _load("h1129", H1129)
h5 = _load("h1305", H1305)

_is_falsifiable = h5._is_falsifiable        # FROZEN H_1305 detector, VERBATIM
_calibrate      = h5._calibrate
COMPARATOR      = h5.COMPARATOR             # frozen detector sets (extraction + audit)
MEASURABLE      = h5.MEASURABLE

# ── FROZEN constants (identical to H_1431 where shared; c9) ──────────────────────
JACCARD_DISTINCT = 0.5
KWR_FLOOR        = 0.50
MAX_NEW          = 110           # verify303m_g6.py VERBATIM
SEEDS            = [7, 4302, 4303]
N_IDEAS          = 5
BUDGET           = 8             # multi-sample budget per leg (H_1309-style); 1-0.8^8=0.83 comp, 1-0.73^8=0.94 meas

# ── 5 corpus directions (single-noun subjects H_1314/H_1431 froze; token-clean) ──
SUBJECTS = ["consciousness", "tension", "memory", "silence", "dreaming"]
assert len(SUBJECTS) == len(g.CONCEPTS)

# ── PRIMING SEEDS (FROZEN IDENTICAL to H_1431; STRUCTURE not content; NO detector token) ──
def _relation_seed(subject):
    return f"a relationship about {subject}: it tends to be "

def _measure_seed(subject):
    return f"something we could observe about {subject}: the "


# ── EXTRACTION (FROZEN IDENTICAL to H_1431) ──────────────────────────────────────
def _extract_comparator(frag):
    for w in g._words(frag):
        if w in COMPARATOR:
            return w
    return None

def _extract_measurable(frag):
    for w in g._words(frag):
        if w in MEASURABLE:
            return w
    return None

def _content_words(frag, k=4):
    out, seen = [], set()
    for w in g._words(frag):
        if (len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS
                and w not in COMPARATOR and w not in MEASURABLE and w not in seen):
            out.append(w); seen.add(w)
            if len(out) >= k:
                break
    return out


# ── BIND-compose weld (FROZEN IDENTICAL to H_1431 — pure function words only) ─────
WELD_FUNC_TOKENS = {"the", "is", "of", "with"}

def _weld(subject, comp_tok, meas_tok, content):
    if comp_tok is None or meas_tok is None:
        return ""   # NO-FAB: a missing leg is NOT invented (p7)
    cA = content[0] if len(content) >= 1 else subject
    cB = content[1] if len(content) >= 2 else subject
    return f"the {meas_tok} of {cA} is {comp_tok} with {cB}"


def _audit_no_token_inject():
    """p7 HARD GATE (FROZEN IDENTICAL to H_1431): no priming seed / weld token carries a
    frozen COMPARATOR or MEASURABLE token."""
    bad = []
    for subj in SUBJECTS:
        for label, fn in (("RELATION_SEED", _relation_seed), ("MEASURE_SEED", _measure_seed)):
            seed = fn(subj)
            toks = set(g._words(seed))
            hc, hm = toks & COMPARATOR, toks & MEASURABLE
            if hc or hm:
                bad.append((label, seed, sorted(hc), sorted(hm)))
    wf = set(g._words(" ".join(WELD_FUNC_TOKENS)))
    hc, hm = wf & COMPARATOR, wf & MEASURABLE
    if hc or hm:
        bad.append(("WELD_TEMPLATE", " ".join(sorted(WELD_FUNC_TOKENS)), sorted(hc), sorted(hm)))
    return bad


def _decode(model, cfg, seed_text, seed_rng):
    return g._decode(model, seed_text, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)


# ── NEW MECHANISM: per-leg multi-sample BUDGET elicitation (the H_1434 lens) ──────
def elicit_comparator_leg(model, cfg, subject, base_seed_rng):
    """pass1: up to BUDGET independent draws toward a COMPARATIVE fragment; keep the FIRST
    draw that emits a frozen COMPARATOR token (else the last draw). Returns (frag, comp_tok,
    n_draws_used). Each draw uses a DISTINCT rng so the budget actually re-samples."""
    last = ""
    for k in range(BUDGET):
        rng = base_seed_rng * 1000 + k          # distinct draw per budget step
        frag = _decode(model, cfg, _relation_seed(subject), rng)
        last = frag
        ct = _extract_comparator(frag)
        if ct is not None:
            return frag, ct, k + 1
    return last, _extract_comparator(last), BUDGET


def elicit_measurable_leg(model, cfg, subject, base_seed_rng):
    """pass2: up to BUDGET independent draws toward a MEASURABLE fragment; keep the FIRST
    draw that emits a frozen MEASURABLE token (else the last draw)."""
    last = ""
    for k in range(BUDGET):
        rng = base_seed_rng * 1000 + 500 + k    # disjoint rng band from pass1
        frag = _decode(model, cfg, _measure_seed(subject), rng)
        last = frag
        mt = _extract_measurable(frag)
        if mt is not None:
            return frag, mt, k + 1
    return last, _extract_measurable(last), BUDGET


def decode_legs_twopass(model, cfg, base_seed_rng):
    """TWO_PASS: per subject, elicit the comparator leg and the measurable leg in SEPARATE
    budgeted passes (distinct draws). Returns lists of (frag, tok, n_draws) per leg."""
    comp_legs, meas_legs = [], []
    for subj in SUBJECTS:
        cf, ct, cn = elicit_comparator_leg(model, cfg, subj, base_seed_rng)
        mf, mt, mn = elicit_measurable_leg(model, cfg, subj, base_seed_rng)
        comp_legs.append((cf, ct, cn))
        meas_legs.append((mf, mt, mn))
    return comp_legs, meas_legs


def score_twopass(comp_legs, meas_legs, shuffle=False, rng_seed=0):
    """Weld + score from SEPARATELY-elicited legs. shuffle=True => pair each idea's comparator
    leg with a measurable leg from a DIFFERENT idea (derangement) — cross-pair control."""
    n = len(SUBJECTS)
    if shuffle:
        rng = random.Random(rng_seed)
        perm = list(range(n))
        while True:
            rng.shuffle(perm)
            if all(perm[i] != i for i in range(n)):
                break
    else:
        perm = list(range(n))

    claims, word_sets = [], []
    fals = 0
    for i in range(n):
        comp_frag, comp_tok, _ = comp_legs[i]
        meas_frag, meas_tok, _ = meas_legs[perm[i]]   # routed measurable leg
        content = _content_words(comp_frag + " " + meas_frag)
        claim = _weld(SUBJECTS[i], comp_tok, meas_tok, content)
        claims.append(claim)
        if claim and g.known_word_ratio(claim) >= KWR_FLOOR:
            ws = set(g._words(claim))
            if ws:
                word_sets.append(ws)
            if _is_falsifiable(claim):
                fals += 1
    kept = []
    for ws in word_sets:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return {"dist": len(kept), "fals": fals, "coherent": len(word_sets), "claims": claims,
            "comp_legs": comp_legs, "meas_legs": meas_legs}


def decode_legs_singlepass(model, cfg, base_seed_rng):
    """ABLATE = SINGLE_PASS: budget=1 AND both legs forced from ONE shared draw per subject
    (the H_1431/H_1314 one-draw regime). One relation draw + one measure draw at the BASE rng
    (budget=1), then BOTH legs extracted from the SHARED union. This isolates the two-pass
    SEPARATION (distinct budgeted draws) as the load-bearing change."""
    comp_legs, meas_legs = [], []
    for subj in SUBJECTS:
        rf = _decode(model, cfg, _relation_seed(subj), base_seed_rng)
        mf = _decode(model, cfg, _measure_seed(subj), base_seed_rng)
        union = rf + " " + mf
        ct = _extract_comparator(union)
        mt = _extract_measurable(union)
        comp_legs.append((union, ct, 1))
        meas_legs.append((union, mt, 1))
    return comp_legs, meas_legs


def main():
    t0 = time.time()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(CKPT, map_location="cpu", weights_only=False); cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.eval(); m.grad_ckpt = False
    m.to(dev)
    print(f"[mouth] {sum(p.numel() for p in m.parameters()):,} params; device={dev}; "
          f"corpus={CORPUS}; gauge={GAUGE}; load+t={time.time()-t0:.1f}s", flush=True)

    cal_correct, _ = _calibrate()
    print(f"=== FROZEN H_1305 FALSIFIABILITY DETECTOR (reused verbatim) calibration = {cal_correct}/10 ===", flush=True)

    # ── (5) NO-FAB / p7 TOKEN-INJECTION AUDIT (BEFORE any scoring) ──
    audit_bad = _audit_no_token_inject()
    print("\n=== (bar 5) NO-FAB p7 TOKEN-INJECTION AUDIT (must be CLEAN) ===", flush=True)
    if audit_bad:
        for label, seed, hc, hm in audit_bad:
            print(f"  [INJECTED] {label}: COMPARATOR={hc} MEASURABLE={hm} :: {seed!r}", flush=True)
        print("  AUDIT DIRTY — lane injects detector tokens (would tune-to-green). ABORT.", flush=True)
        raise SystemExit("p7 audit DIRTY (NO-FAB violated): lane injects a frozen-detector token")
    print("  CLEAN — no priming seed and no weld function-token carries a frozen "
          "COMPARATOR/MEASURABLE token.", flush=True)

    print(f"\n=== TWO-PASS elicit-then-bind · BUDGET={BUDGET}/leg · {N_IDEAS} subjects · seeds={SEEDS} ===", flush=True)
    for subj in SUBJECTS:
        print(f"  REL  {_relation_seed(subj)!r}", flush=True)
        print(f"  MEAS {_measure_seed(subj)!r}", flush=True)

    arms = ["TWO_PASS", "CROSS_SHUFFLE", "SINGLE_PASS"]
    per_seed = {a: [] for a in arms}
    leg_hit_comp = leg_hit_meas = leg_hit_both = leg_total = 0
    for seed_rng in SEEDS:
        print(f"\n######## seed_rng={seed_rng} ########", flush=True)
        # TWO_PASS: separate budgeted legs (the H_1434 mechanism)
        comp_legs, meas_legs = decode_legs_twopass(m, cfg, seed_rng)
        # diagnostic: per-idea, did each separated leg yield its frozen token? both?
        for (cf, ct, cn), (mf, mt, mn) in zip(comp_legs, meas_legs):
            leg_total += 1
            leg_hit_comp += int(ct is not None)
            leg_hit_meas += int(mt is not None)
            leg_hit_both += int(ct is not None and mt is not None)

        r_two = score_twopass(comp_legs, meas_legs, shuffle=False)
        per_seed["TWO_PASS"].append(r_two)
        print(f"  [TWO_PASS    ] DIST={r_two['dist']} FALS={r_two['fals']} coh={r_two['coherent']}/{N_IDEAS}", flush=True)
        for i, c in enumerate(r_two["claims"]):
            fl = "F" if (c and g.known_word_ratio(c) >= KWR_FLOOR and _is_falsifiable(c)) else "."
            cf, ct, cn = comp_legs[i]; mf, mt, mn = meas_legs[i]
            print(f"        ({fl}) WELD  {c!r}", flush=True)
            print(f"              comp_leg(draw {cn}/{BUDGET}, tok={ct}): {cf[:74]!r}", flush=True)
            print(f"              meas_leg(draw {mn}/{BUDGET}, tok={mt}): {mf[:74]!r}", flush=True)

        r_shuf = score_twopass(comp_legs, meas_legs, shuffle=True, rng_seed=seed_rng)
        per_seed["CROSS_SHUFFLE"].append(r_shuf)
        print(f"  [CROSS_SHUFFLE] DIST={r_shuf['dist']} FALS={r_shuf['fals']} coh={r_shuf['coherent']}/{N_IDEAS}", flush=True)
        for c in r_shuf["claims"]:
            fl = "F" if (c and g.known_word_ratio(c) >= KWR_FLOOR and _is_falsifiable(c)) else "."
            print(f"        ({fl}) {c!r}", flush=True)

        # SINGLE_PASS (ablate two-pass): budget=1, both legs from one shared draw (H_1431 regime)
        sc_legs, sm_legs = decode_legs_singlepass(m, cfg, seed_rng)
        r_single = score_twopass(sc_legs, sm_legs, shuffle=False)
        per_seed["SINGLE_PASS"].append(r_single)
        print(f"  [SINGLE_PASS ] DIST={r_single['dist']} FALS={r_single['fals']} coh={r_single['coherent']}/{N_IDEAS}", flush=True)
        for i, c in enumerate(r_single["claims"]):
            fl = "F" if (c and g.known_word_ratio(c) >= KWR_FLOOR and _is_falsifiable(c)) else "."
            print(f"        ({fl}) {c!r}", flush=True)

    print(f"\n=== TWO-PASS per-leg co-availability diagnostic (the wall H_1431 hit was 0/15 BOTH) ===", flush=True)
    print(f"  separated COMPARATOR leg yielded its frozen token : {leg_hit_comp}/{leg_total}", flush=True)
    print(f"  separated MEASURABLE leg yielded its frozen token : {leg_hit_meas}/{leg_total}", flush=True)
    print(f"  BOTH available across SEPARATE passes (weld precond): {leg_hit_both}/{leg_total}  "
          f"(H_1431 single-draw BOTH was 0/15)", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:13s}  DIST={DIST[a]}  FALS={FALS[a]}", flush=True)

    # ── FROZEN 5-bar (declared in FREEZE.txt BEFORE the run) ──
    b1_fals_cross = FALS["TWO_PASS"] >= 1
    b2_count      = DIST["TWO_PASS"] >= 5
    b3_shuffle    = FALS["TWO_PASS"] >= FALS["CROSS_SHUFFLE"] + 1
    b4_ablate     = FALS["TWO_PASS"] >= FALS["SINGLE_PASS"] + 1
    b5_nofab      = (len(audit_bad) == 0)
    crossed  = b1_fals_cross and b2_count
    controls = b3_shuffle and b4_ablate and b5_nofab
    green = crossed and controls
    # 🧱 = two-pass did NOT cross AND single-pass ~= two-pass (bind capacity-bound even separated)
    wall = (not b1_fals_cross) and (FALS["TWO_PASS"] <= FALS["SINGLE_PASS"] + 0.0001)

    print("\n---- FROZEN 5-BAR ----", flush=True)
    print(f"  (1) FALS>=1 cross            : {FALS['TWO_PASS']} -> {b1_fals_cross}", flush=True)
    print(f"  (2) count>=5 distinct        : {DIST['TWO_PASS']} -> {b2_count}", flush=True)
    print(f"  (3) cross-shuffle COLLAPSE   : {FALS['TWO_PASS']} >= {FALS['CROSS_SHUFFLE']}+1 -> {b3_shuffle}", flush=True)
    print(f"  (4) ablate->single-pass INERT: {FALS['TWO_PASS']} >= {FALS['SINGLE_PASS']}+1 -> {b4_ablate}", flush=True)
    print(f"  (5) NO-FAB audit CLEAN       : {b5_nofab}", flush=True)
    print(f"  crossed(1&2)={crossed}  controls(3&4&5)={controls}  GREEN={green}  WALL={wall}", flush=True)

    if green:
        tier = "GREEN"
        verdict = ("🟢 TWO-PASS ELICIT-THEN-BIND BREAKS THE FALS WALL at 303M — eliciting the "
                   "comparator and measurable legs in SEPARATE budgeted passes (instead of forcing "
                   "both from one draw) supplies the binder with material it never co-emits in one "
                   "breath: FALS crosses >=1 AND >=5 distinct, AND all controls survive (cross-shuffle "
                   "collapses, single-pass inert, NO-FAB clean). The G6 FALS-depth wall was NOT a "
                   "capacity ceiling but a ONE-DRAW-FORCED artifact — the 303M material was always "
                   "there (a_break_the_wall · NO bigger model)")
    elif wall:
        tier = "WALL-BIND-CAPACITY-BOUND-EVEN-SEPARATED"
        verdict = ("🧱 BIND CAPACITY-BOUND EVEN WITH SEPARATED PASSES — eliciting each leg in its own "
                   "budgeted pass does NOT cross the FALS floor and single-pass==two-pass: even with "
                   "the two legs drawn separately the bind cannot manufacture a falsifiable claim at "
                   "303M. 5th independent confirmation of the capacity thesis (after H_1309/1314/1431/"
                   "1432) — decisive grounding for the H_1433 7B falsifier (c9)")
    else:
        tier = "PARTIAL"
        fails = [n for n, ok in [("b1", b1_fals_cross), ("b2", b2_count), ("b3", b3_shuffle),
                                 ("b4", b4_ablate), ("b5", b5_nofab)] if not ok]
        verdict = (f"🟠 PARTIAL — signal present but bars {fails} fail (frozen, c9). "
                   "Neither clean GREEN nor a clean single==two WALL")
    print(f"\n  TIER: {tier}\n  VERDICT: {verdict}", flush=True)

    out = {"ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS, "budget": BUDGET,
           "calibration": f"{cal_correct}/10",
           "audit_nofab_clean": (len(audit_bad) == 0),
           "audit_bad": [[l, s, hc, hm] for l, s, hc, hm in audit_bad],
           "DIST": DIST, "FALS": FALS,
           "leg_hit_comp": leg_hit_comp, "leg_hit_meas": leg_hit_meas,
           "leg_hit_both": leg_hit_both, "leg_total": leg_total,
           "b1_fals_cross": bool(b1_fals_cross), "b2_count": bool(b2_count),
           "b3_cross_shuffle_collapse": bool(b3_shuffle), "b4_ablate_singlepass_inert": bool(b4_ablate),
           "b5_nofab": bool(b5_nofab),
           "crossed_floor": bool(crossed), "controls_survive": bool(controls),
           "green": bool(green), "wall": bool(wall), "tier": tier, "verdict": verdict,
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"], "coherent": r["coherent"]}
                            for r in per_seed[a]] for a in arms},
           "wall_seconds": round(time.time() - t0, 1)}
    od = os.path.join(ANIMA, ".verdicts", "1434_twopass_bind")
    os.makedirs(od, exist_ok=True)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json  ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
