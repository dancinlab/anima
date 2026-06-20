#!/usr/bin/env python3
"""H_1463 — PHASE-BINDING / BINDING-BY-SYNCHRONY (G6 FALS-depth, breakthrough lens ③).

BIO/NEURO LENS (a_no_llm_frame_trap — binding-by-synchrony, von der Malsburg / Lisman;
hippocampal theta-gamma phase coupling):
  Features of the SAME object fire at the SAME phase; features of DIFFERENT objects fire at
  DIFFERENT (anti) phases. Binding is read out as PHASE-COHERENCE, not by a learned
  weight-space weld (every prior 7 G6 lens used MLP/attention/retrieval = content-addressed
  shell). anima mirror: the comparator-slot & measurable-slot of a candidate falsifiable claim
  each carry a PHASE derived from their emitted CONTENT; a claim is "bound" only when the two
  slots are phase-coherent above a FROZEN threshold.

★ THE HONEST DESIGN DECISION (c9 — what makes this a REAL test, not a tautology):
  A NAIVE phase mirror that assigns phase = idea-identity by hand is CIRCULAR: matched
  coherence -> 1 and cross-shuffle -> chance BY CONSTRUCTION, proving nothing about the mouth.
  The wall the 7 prior lenses hit (H_1431/1434/1449) is precisely that the mouth's comparator
  & measurable are CONTENT-ADDRESSED interchangeable shells: a FOREIGN measurable that merely
  *looks* like a measurable still passes the token-presence detector (FALS_shuf == FALS_in).
  To be faithful, H_1463 derives each slot's phase FROM ITS CONTENT vector, where the content
  is IDEA_SIGNAL (idea-specific, what binding must recover) + FORM_SIGNAL (generic "this is a
  measurable-shaped clause", SHARED across all measurables = the shell). The phase is
  phase = atan2 over a projection of (idea_signal + form_signal). Cross-shuffle keeps the
  FORM_SIGNAL identical (foreign measurable is still measurable-shaped) and only flips the
  IDEA_SIGNAL. So B3 cross-shuffle collapses ONLY IF the idea-signal dominates the phase —
  i.e. ONLY IF synchrony actually recovers idea-identity over generic form.

  FORM_RATIO is the load-bearing knob = fraction of the content vector that is generic
  form-shell. It is set to the H_1431-measured emission profile (comparator ~20%, measurable
  ~27% idea-specific tokens; the REST is generic falsifiable-clause boilerplate) -> FORM_RATIO
  ~ 0.75. It is NOT tuned to pass; the verdict is read AFTER it is frozen at the measured value,
  and a sensitivity sweep over FORM_RATIO in {0.5..0.9} is logged so the reader sees where the
  wall sits.

ARMS (deterministic per seed, $0 CPU numpy):
  SYNC      : phase from content (idea+form), same-idea slots tend in-phase. matched measurable.
  SYNC-X    : B3 cross-shuffle — FOREIGN measurable (same FORM, different IDEA) welded.
  ABLATED   : phase-scramble — random phase per slot (synchrony OFF). decisive INERT control.
  base      : no-binding plateau (random phase) for the FALS floor.

FROZEN 5-bar (declared BEFORE any result read, c9, p7):
  B1 FALS-FLOOR  : SYNC mean FALS_in >= 1
  B2 COUNT       : SYNC mean DIST_in >= 5
  B3 X-SHUFFLE COLLAPSE (DECISIVE): COH_matched - COH_mismatched >= 0.30
  B4 HELD-OUT    : SYNC mean FALS_ho >= 1
  B5 vs-BASE     : SYNC FALS_in >= base FALS_in + 1
CONTROL CTRL-ABLATE (phase-scramble): COH_matched_ablated <= 0.55 (random phase -> chance).

VERDICT:
  🟢 ROOT-FIX iff B1&B2&B3&B4&B5 AND phase-scramble collapses -> synchrony recovers
     idea-identity OVER generic form at the H_1431 emission profile (wall broken).
  🧱 WALL=CAPACITY iff B3 does NOT collapse at the measured FORM_RATIO -> the foreign
     measurable's shared FORM keeps coherence high (interchangeable shells) -> synchrony is a
     structural template, converges with the 7 prior lenses (grounds 7B, a7b_pass).

DIRECTIONAL: numpy mirror, $0 CPU (a_engine_native_learning) -> AUTOMATIC DIRECTIONAL.
  Terminal frozen-bar read = engine-native re-measure on live core/ decode = ING follow-on.
"""
import json, os, math
import numpy as np

SEEDS = [1463, 1464, 1465]
DIM = 64
N_IDEAS = 12
N_EVAL = 8
N_HELDOUT = 4
COH_THR = 0.55          # frozen phase-coherence threshold for "bound/falsifiable"
B3_MARGIN = 0.30        # frozen B3 collapse margin
# FROZEN at the H_1431-measured emission profile: comparator ~20% / measurable ~27% of the
# emitted content is idea-specific; the rest (~0.75) is generic falsifiable-clause FORM that a
# FOREIGN measurable shares. NOT tuned to pass — read verdict after this is frozen.
FORM_RATIO = 0.75
OUT = os.path.dirname(os.path.abspath(__file__))


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


def content_vector(rng, idea_sig, form_sig, form_ratio):
    """Slot content = sqrt(1-r)*idea-specific + sqrt(r)*generic-form + emission noise.
    A FOREIGN measurable keeps form_sig (shared shell) but has a DIFFERENT idea_sig."""
    noise = rng.normal(0, 0.10, size=DIM)
    return unit(math.sqrt(1 - form_ratio) * idea_sig
                + math.sqrt(form_ratio) * form_sig
                + noise)


def phase_of(vec, proj):
    """Read a phase tag from a content vector by projecting onto a fixed 2-D readout basis
    (theta-gamma oscillator coords) -> atan2. Same content -> same phase (binding-by-synchrony)."""
    a = float(vec @ proj[0])
    b = float(vec @ proj[1])
    return math.atan2(b, a)


def coherence(p1, p2):
    return max(0.0, math.cos(p1 - p2))


def make_world(rng):
    # idea-specific directions (what binding must recover) + ONE shared form direction (the shell)
    idea_dirs = [unit(rng.normal(size=DIM)) for _ in range(N_IDEAS)]
    form_dir = unit(rng.normal(size=DIM))           # generic "measurable-shaped clause" shell
    comp_form = unit(rng.normal(size=DIM))          # generic "comparator-shaped clause" shell
    proj = [unit(rng.normal(size=DIM)), unit(rng.normal(size=DIM))]  # phase readout basis
    return idea_dirs, form_dir, comp_form, proj


def eval_arm(rng, idea_dirs, form_dir, comp_form, proj, idx, scramble=False, cross=False,
             form_ratio=FORM_RATIO):
    n = len(idx)
    # build comparator + measurable content per idea
    comp_vecs, meas_vecs = [], []
    for i in idx:
        comp_vecs.append(content_vector(rng, idea_dirs[i], comp_form, form_ratio))
        meas_vecs.append(content_vector(rng, idea_dirs[i], form_dir, form_ratio))
    # cross-shuffle: weld each comparator with a FOREIGN idea's measurable (same FORM, diff IDEA)
    if cross:
        perm = list(range(n))
        for _ in range(64):
            rng.shuffle(perm)
            if all(perm[k] != k for k in range(n)):
                break
    else:
        perm = list(range(n))
    cohs, fals = [], 0
    for k in range(n):
        if scramble:
            pc = rng.uniform(0, 2 * math.pi)
            pm = rng.uniform(0, 2 * math.pi)
        else:
            pc = phase_of(comp_vecs[k], proj)
            pm = phase_of(meas_vecs[perm[k]], proj)
        c = coherence(pc, pm)
        cohs.append(c)
        if c >= COH_THR:
            fals += 1
    return {"FALS": fals, "DIST": len(set(round(c, 3) for c in cohs)),
            "COH_mean": float(np.mean(cohs))}


def run_seed(seed, form_ratio=FORM_RATIO):
    rng = np.random.default_rng(seed)
    idea_dirs, form_dir, comp_form, proj = make_world(rng)
    eval_idx = list(range(N_EVAL))
    held_idx = list(range(N_EVAL, N_EVAL + N_HELDOUT))  # disjoint ideas, same world geometry

    base = eval_arm(np.random.default_rng(seed + 5), idea_dirs, form_dir, comp_form, proj,
                    eval_idx, scramble=True, form_ratio=form_ratio)
    sync_in = eval_arm(np.random.default_rng(seed + 1), idea_dirs, form_dir, comp_form, proj,
                       eval_idx, form_ratio=form_ratio)
    sync_ho = eval_arm(np.random.default_rng(seed + 2), idea_dirs, form_dir, comp_form, proj,
                       held_idx, form_ratio=form_ratio)
    sync_x = eval_arm(np.random.default_rng(seed + 3), idea_dirs, form_dir, comp_form, proj,
                      eval_idx, cross=True, form_ratio=form_ratio)
    ablate = eval_arm(np.random.default_rng(seed + 4), idea_dirs, form_dir, comp_form, proj,
                      eval_idx, scramble=True, form_ratio=form_ratio)
    return {
        "seed": seed,
        "base_FALS": base["FALS"],
        "sync_FALS_in": sync_in["FALS"], "sync_DIST_in": sync_in["DIST"],
        "sync_COH_matched": sync_in["COH_mean"], "sync_FALS_ho": sync_ho["FALS"],
        "sync_COH_mismatched": sync_x["COH_mean"], "sync_FALS_x": sync_x["FALS"],
        "ablate_COH_matched": ablate["COH_mean"],
    }


def aggregate(rows):
    def mean(k):
        return float(np.mean([r[k] for r in rows]))
    return {k: mean(k) for k in [
        "base_FALS", "sync_FALS_in", "sync_DIST_in", "sync_FALS_ho",
        "sync_COH_matched", "sync_COH_mismatched", "ablate_COH_matched"]}


def main():
    rows = [run_seed(s) for s in SEEDS]
    m = aggregate(rows)
    base_FALS = m["base_FALS"]; FALS_in = m["sync_FALS_in"]; DIST_in = m["sync_DIST_in"]
    FALS_ho = m["sync_FALS_ho"]; COH_m = m["sync_COH_matched"]; COH_x = m["sync_COH_mismatched"]
    ablate_COH = m["ablate_COH_matched"]

    b1 = FALS_in >= 1; b2 = DIST_in >= 5; b3 = (COH_m - COH_x) >= B3_MARGIN
    b4 = FALS_ho >= 1; b5 = FALS_in >= base_FALS + 1
    ctrl = ablate_COH <= 0.55
    all_bars = b1 and b2 and b3 and b4 and b5
    verdict = "🟢 ROOT-FIX" if (all_bars and ctrl) else "🧱 WALL=CAPACITY"

    # SENSITIVITY SWEEP (honest, non-gating): where does B3 collapse vs form-ratio?
    sweep = {}
    for fr in [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]:
        srows = [run_seed(s, form_ratio=fr) for s in SEEDS]
        sm = aggregate(srows)
        gap = sm["sync_COH_matched"] - sm["sync_COH_mismatched"]
        sweep[f"form_ratio={fr}"] = {"COH_m": round(sm["sync_COH_matched"], 3),
                                      "COH_x": round(sm["sync_COH_mismatched"], 3),
                                      "B3_gap": round(gap, 3), "B3_pass": gap >= B3_MARGIN}

    out = {
        "variant": "H_1463_phase_binding_synchrony",
        "lens": "binding-by-synchrony (von der Malsburg / Lisman theta-gamma phase coupling)",
        "seeds": SEEDS, "DIM": DIM, "COH_THR": COH_THR, "B3_MARGIN": B3_MARGIN,
        "FORM_RATIO_frozen": FORM_RATIO, "FORM_RATIO_basis": "H_1431 emission profile (~25% idea-specific)",
        "per_seed": rows, "means": {k: round(v, 3) for k, v in m.items()},
        "bars": {
            "B1_FALS_floor(>=1)": [round(FALS_in, 3), b1],
            "B2_DIST(>=5)": [round(DIST_in, 3), b2],
            "B3_XSHUFFLE_COLLAPSE(COH_m-COH_x>=0.30)": [round(COH_m - COH_x, 3), b3],
            "B4_HELDOUT(>=1)": [round(FALS_ho, 3), b4],
            "B5_vs_BASE(FALS_in>=base+1)": [f"{round(FALS_in,3)} vs {round(base_FALS,3)}+1", b5],
        },
        "control_ablate_phase_scramble(COH_m<=0.55)": [round(ablate_COH, 3), ctrl],
        "sensitivity_sweep_FORM_RATIO": sweep,
        "verdict": verdict,
        "DIRECTIONAL": "numpy mirror $0 CPU (a_engine_native_learning) -> AUTOMATIC DIRECTIONAL; "
                       "engine-native re-measure on live core/ decode = ING follow-on",
    }

    print("=" * 80)
    print(f"H_1463 PHASE-BINDING / BINDING-BY-SYNCHRONY (mean/{len(SEEDS)} seeds {SEEDS}) FORM_RATIO={FORM_RATIO}")
    print("=" * 80)
    print(f"  base   FALS_in={base_FALS:.3f}")
    print(f"  SYNC   FALS_in={FALS_in:.3f}  DIST_in={DIST_in:.3f}  FALS_ho={FALS_ho:.3f}")
    print(f"  COH    matched={COH_m:.3f}  mismatched(cross)={COH_x:.3f}  ablate={ablate_COH:.3f}")
    print("  ---- FROZEN BARS ----")
    for k, v in out["bars"].items():
        print(f"  {k:42s}: {v[0]} -> {v[1]}")
    print(f"  CTRL phase-scramble (COH_m<=0.55)         : {ablate_COH:.3f} -> {ctrl}")
    print("  ---- SENSITIVITY (form-ratio vs B3 collapse) ----")
    for k, v in sweep.items():
        print(f"  {k:18s}: COH_m={v['COH_m']:.3f} COH_x={v['COH_x']:.3f} gap={v['B3_gap']:+.3f} B3={v['B3_pass']}")
    print("  " + "-" * 40)
    print(f"  VERDICT: {verdict}   (DIRECTIONAL — engine-native re-measure = ING)")

    json.dump(out, open(os.path.join(OUT, "h1463_result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[H_1463 done] {OUT}/h1463_result.json")
    return out


if __name__ == "__main__":
    main()
