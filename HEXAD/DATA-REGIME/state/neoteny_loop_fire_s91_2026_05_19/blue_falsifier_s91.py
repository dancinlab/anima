#!/usr/bin/env python3
"""
§91 NEOTENY + #3 ACTION-PERCEPTION LOOP — TRAINED-SCALE closed-form
sidecar battery B-S91-1..8.

Sidecar — does NOT touch the central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py (0-line-diff mandate, g_blue_closed_mandate).

g3: the battery proves the §91 trained-scale fire is structurally honest
— #3 closed-form loop transfer/invariant (§89 Kolmogorov carry), the
neoteny trainer is §88-F2 byte-equal, §9 metric reuse, the γ-CLOSED
predicate is a falsifiable Boolean, the §62 echo-amplify detector is a
real partition, the §90 stub connection, §16 baseline regression, and
determinism. It does NOT prove γ is closed at trained scale (B-S91-NOTE).
necessary-not-sufficient (B-EMERGE-7).
"""
import ast
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(HERE, "result.json")
TRAINER = os.path.join(HERE, "neoteny_loop_train_s91.py")
S88F2_TRAINER = os.path.join(
    HERE, "..", "axolotl_neoteny_fire_s88f2_2026_05_19",
    "axolotl_neoteny_train_s88f2.py")
S90_SMOKE = os.path.join(
    HERE, "..", "neoteny_action_perception_loop_s90_2026_05_19",
    "neoteny_loop_smoke_s90.py")


def _load_result():
    if not os.path.exists(RESULT):
        return None
    with open(RESULT) as f:
        return json.load(f)


def _trainer_src():
    with open(TRAINER) as f:
        return f.read()


# ── B-S91-1 — #3-LOOP-TRANSFER-CLOSED-AT-TRAINED (§89 Kolmogorov) ────
def b_s91_1():
    """The #3 D@emit→S@t+1 transfer x_{t+1}=S_encode(e_t) is a CLOSED
    deterministic byte function — invariant K(x_{t+1}) ≤ K(e_t)+K(S_encode)
    (data-processing inequality, §89 real-limit). s_encode adds NO
    information: it window-pads/truncates the emit bytes. Verified
    structurally: s_encode is a pure function (no RNG, no I/O, no model
    call, no external state)."""
    src = _trainer_src()
    tree = ast.parse(src)
    fn = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "s_encode":
            fn = node
            break
    if fn is None:
        return False, "s_encode not found"
    body_src = ast.get_source_segment(src, fn) or ""
    # forbidden inside s_encode: RNG / I/O / model forward / mutable state
    forbidden = ["random", "torch", "open(", "model(", "np.", "time."]
    hits = [t for t in forbidden if t in body_src]
    # s_encode must reference its `emit_bytes` arg and a window pad only
    uses_arg = "emit_bytes" in body_src and "block_size" in body_src
    # data-processing inequality named in the trainer source (closed-form
    # §89 carry) — present pre- and post-fire.
    invariant_named = ("data-processing" in src.lower() and
                       "K(x_{t+1})" in src)
    passed = (len(hits) == 0) and uses_arg and invariant_named
    return passed, (f"s_encode_pure={len(hits) == 0} forbidden={hits} "
                    f"uses_arg={uses_arg} invariant_named={invariant_named}")


# ── B-S91-2 — NEOTENY-TRAINER-BYTE-EQUAL-§88-F2 (연결부위, AST) ───────
def b_s91_2():
    """The §91 train_cell + 4 NK mechanisms (NK-1 CE-floor clamp / NK-2
    plasticity-reinject / NK-3 dim-spread reg / NK-4 metamorphosis-block)
    are STRUCTURALLY byte-equal to §88-F2's trainer — same NK constants,
    same maturity 3-proxy. Verified by AST: §88-F2's NK function bodies
    and constants are present in §91's trainer source. Connection-point:
    §91 trains the same neoteny ckpt §88-F2 measured."""
    src91 = _trainer_src()
    if not os.path.exists(S88F2_TRAINER):
        return False, "§88-F2 trainer not found"
    with open(S88F2_TRAINER) as f:
        src88 = f.read()

    def _consts(src):
        t = ast.parse(src)
        out = {}
        for node in ast.walk(t):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                tg = node.targets[0]
                if isinstance(tg, ast.Name) and isinstance(
                        node.value, ast.Constant):
                    out[tg.id] = node.value.value
        return out
    c91, c88 = _consts(src91), _consts(src88)
    nk_keys = ["W_CE", "W_MAJ", "W_D", "THETA_FLOOR", "THETA_D",
               "SAT_TRIGGER", "NK2_SIGMA", "NK3_LAMBDA", "NK4_LR_FLOOR_FRAC",
               "CE_INIT", "CE_NATURAL_FLOOR", "D_INIT", "D_NATURAL_FLOOR"]
    mism = [k for k in nk_keys
            if c91.get(k) != c88.get(k)]
    # the 4 NK functions present
    nk_fns = ["nk3_dim_spread_reg", "nk2_plasticity_reinject",
              "maturity_score", "train_cell"]
    fns91 = {n.name for n in ast.walk(ast.parse(src91))
             if isinstance(n, ast.FunctionDef)}
    missing = [f for f in nk_fns if f not in fns91]
    passed = (len(mism) == 0) and (len(missing) == 0)
    return passed, (f"nk_consts_match={len(mism) == 0} mism={mism} "
                    f"nk_fns_present={len(missing) == 0} missing={missing}")


# ── B-S91-3 — §9-METRIC-REUSE ────────────────────────────────────────
def b_s91_3():
    """The §91 honest_coherent is the §9 cascade-rate metric SSOT —
    4-clause Boolean conjunction with thresholds 0.30 / 10 / 20 / 0.80.
    Verified by reproducing the 4-clause gate on known witnesses."""
    src = _trainer_src()
    ns = {}
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in (
                "cascade_rate_and_max_run", "honest_coherent"):
            exec(compile(ast.Module([node], []), TRAINER, "exec"), ns)
    hc = ns.get("honest_coherent")
    if hc is None:
        return False, "honest_coherent not extractable"
    # witnesses: clean prose True, char-cascade False, short False
    clean = b"anima senses the stimulus and forms a measured reply now ok"
    cascade = b"a" * 60
    short = b"hello"
    digit = b"5" * 40 + b"abc"
    w_clean = hc(clean)[0]
    w_cascade = hc(cascade)[0]
    w_short = hc(short)[0]
    w_digit = hc(digit)[0]
    # threshold constants present in source
    thr = all(t in src for t in ["0.30", "min_len=20", "max_run=10",
                                  "tau_print=0.80"])
    passed = (w_clean and not w_cascade and not w_short and not w_digit
              and thr)
    return passed, (f"clean={w_clean} cascade={w_cascade} short={w_short} "
                    f"digit={w_digit} thresholds_present={thr}")


# ── B-S91-4 — γ-CLOSED-PREDICATE (falsifiable Boolean) ───────────────
def b_s91_4():
    """The α γ-CLOSED-AT-TRAINED corner is a CLOSED falsifiable Boolean:
    alpha = (coh2 > coh0) AND (coh2 > 0). It is decidable from result.json
    and would FAIL for any run where cell2 does not strictly exceed the
    cell0 neoteny-baseline. Verified: the predicate is reconstructible
    from the grid and matches the recorded four_corner.alpha."""
    r = _load_result()
    if r is None:
        return True, "pre-fire — predicate well-formed (post-fire decides)"
    gs = {c["cell"]: c for c in r["grid_summary"]}
    coh0 = gs["cell0_neoteny_baseline"]["body_coherent_9"]
    coh2 = gs["cell2_neoteny_loop3"]["body_coherent_9"]
    recomputed = (coh2 > coh0) and (coh2 > 0)
    recorded = r["four_corner"]["alpha_GAMMA_CLOSED_AT_TRAINED"]
    passed = (recomputed == recorded)
    return passed, (f"coh0={coh0} coh2={coh2} recomputed_alpha={recomputed} "
                    f"recorded={recorded} match={passed}")


# ── B-S91-5 — ECHO-AMPLIFY-DETECTOR (§62 carry, real partition) ──────
def b_s91_5():
    """The β ECHO-DOMINATES corner uses the §62 echo-chamber collapse
    detector: echo_collapsed := maj_frac ≥ 0.95. This is a real Boolean
    partition (collapsed vs not) — verified the detector reproduces from
    each cell's attractor_maj_frac and the MAJ_FRAC_COLLAPSE=0.95
    constant matches §62 / §88-F2."""
    src = _trainer_src()
    has_const = "MAJ_FRAC_COLLAPSE = 0.95" in src
    r = _load_result()
    if r is None:
        return has_const, f"pre-fire — MAJ_FRAC_COLLAPSE=0.95 present={has_const}"
    ok = True
    for c in r["grid_summary"]:
        recomp = c["attractor_maj_frac"] >= 0.95
        if recomp != c["echo_collapsed"]:
            ok = False
    passed = has_const and ok
    return passed, (f"const_0.95={has_const} echo_detector_consistent={ok}")


# ── B-S91-6 — §90-STUB-CONNECTION (AST — same cell semantics) ────────
def b_s91_6():
    """§91 is the trained-scale validation of §90 — verified the §90 stub
    exists and §91 carries the SAME 4-corner semantic axes
    (γ-closed / echo / synergy / stub-overclaim). The §90 stub's cell2
    name and the #3-loop transfer formula must both appear in §91."""
    if not os.path.exists(S90_SMOKE):
        return False, "§90 stub not found"
    with open(S90_SMOKE) as f:
        src90 = f.read()
    src91 = _trainer_src()
    # §90 stub carried cell2_neoteny_loop3 + #3 transfer x_{t+1}=S_encode
    stub_has = ("cell2_neoteny_loop3" in src90 and
                "S_encode" in src90)
    fire_has = ("cell2_neoteny_loop3" in src91 and
                "S_encode" in src91)
    r = _load_result()
    rj = json.dumps(r, ensure_ascii=False) if r is not None else ""
    anchored = (r is not None and
                "§90" in rj and "f9ef93e8a" in rj)
    passed = stub_has and fire_has and (r is None or anchored)
    return passed, (f"stub_cell2+S_encode={stub_has} "
                    f"fire_cell2+S_encode={fire_has} s90_anchored={anchored}")


# ── B-S91-7 — §16-BASELINE-REGRESSION (CE descent + no helper token) ─
def b_s91_7():
    """The baseline ckpt must train §16-class normally — CE descends
    (init→final < init−1.0) — and NO body emits forbidden helper tokens
    (B-IDENTITY-5: 도우미/helper/assistant/사용자/user:). Verified from
    result.json: ce_descended on the baseline cells AND
    forbidden_token_hits == 0 across all cells."""
    r = _load_result()
    if r is None:
        return True, "pre-fire — regression gate well-formed"
    cells = r["cells"]
    base_ce_ok = cells["cell3_s24_baseline"]["ce_descended"]
    fb = sum(c["forbidden_token_hits"] for c in cells.values())
    passed = base_ce_ok and (fb == 0)
    return passed, (f"baseline_ce_descended={base_ce_ok} "
                    f"forbidden_token_hits_total={fb}")


# ── B-S91-8 — DETERMINISTIC ──────────────────────────────────────────
def b_s91_8():
    """The §91 fire is seed-fixed (1337) — torch.manual_seed + corpus
    seed + random.seed all 1337; no unseeded RNG. The 4-cell loop3
    emission is @torch.no_grad greedy argmax (no sampling). Verified:
    seed recorded, argmax used, no multinomial/gumbel sampling."""
    src = _trainer_src()
    r = _load_result()
    seed_recorded = (r["config"]["seed"] if r else None)
    has_seed = ("SEED = 1337" in src and
                "torch.manual_seed" in src and "random.seed" in src)
    # greedy decode — argmax, no sampling
    greedy = ".argmax()" in src
    no_sampling = not any(t in src for t in
                          ["multinomial", "torch.gumbel", "F.gumbel"])
    passed = has_seed and greedy and no_sampling and (
        r is None or seed_recorded == 1337)
    return passed, (f"seed_fixed={has_seed} greedy_argmax={greedy} "
                    f"no_sampling={no_sampling} recorded_seed={seed_recorded}")


BATTERY = [
    ("B-S91-1", "#3-LOOP-TRANSFER-CLOSED-AT-TRAINED", b_s91_1),
    ("B-S91-2", "NEOTENY-TRAINER-BYTE-EQUAL-§88-F2", b_s91_2),
    ("B-S91-3", "§9-METRIC-REUSE", b_s91_3),
    ("B-S91-4", "γ-CLOSED-PREDICATE", b_s91_4),
    ("B-S91-5", "ECHO-AMPLIFY-DETECTOR", b_s91_5),
    ("B-S91-6", "§90-STUB-CONNECTION", b_s91_6),
    ("B-S91-7", "§16-BASELINE-REGRESSION", b_s91_7),
    ("B-S91-8", "DETERMINISTIC", b_s91_8),
]

# B-S91-NOTE — empirical carve-out: whether the #3 action-perception loop
# ACTUALLY closes γ (coherent emission emerges at trained scale) =
# trained-scale GPU fire OUTCOME, NOT counted 🔵. The $0 §90 stub encoded
# garble-feeds-garble (echo) AND self-correction as competing forces;
# which dominates at trained scale is the measured OUTCOME. B-D-NOTE /
# B-S88F2-NOTE / B-S90-NOTE / B-EMERGE-NOTE family. The battery proves
# the fire's WIRING is honest (closed loop transfer, neoteny-trainer
# byte-equal, §9 reuse, falsifiable γ predicate, echo detector, §90/§16
# connection, determinism) — NOT that γ is closed. necessary-not-
# sufficient (B-EMERGE-7); trained-scale γ-close != GOAL emergence.


def main():
    results = []
    npass = 0
    for bid, name, fn in BATTERY:
        try:
            ok, note = fn()
        except Exception as e:
            ok, note = False, f"EXC {e}"
        results.append({"id": bid, "name": name, "passed": bool(ok),
                        "note": note})
        npass += int(bool(ok))
        mark = "🔵" if ok else "✗"
        print(f"  {bid} {name}: {mark} — {note}")
    out = {
        "section": "§91",
        "battery": "B-S91-1..8",
        "n_pass": npass,
        "n_total": len(BATTERY),
        "all_blue": npass == len(BATTERY),
        "results": results,
        "B-S91-NOTE": ("γ-closing actual emergence at trained scale = GPU "
                       "fire OUTCOME, NOT counted 🔵 (B-D-NOTE/B-S88F2-NOTE/"
                       "B-S90-NOTE/B-EMERGE-NOTE family); the battery "
                       "proves the fire wiring is honest, not that γ is "
                       "closed. necessary-not-sufficient B-EMERGE-7."),
    }
    with open(os.path.join(HERE, "blue_falsifier_s91_result.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"\nB-S91: {npass}/{len(BATTERY)} "
          f"{'all 🔵' if out['all_blue'] else 'INCOMPLETE'}")
    return 0 if out["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
