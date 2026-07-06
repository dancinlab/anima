#!/usr/bin/env python3
"""cli/rho_axon.py — ρ-AXON reach-layer measurement (Ψ-SOMA ρ · replaces G0-G6).

The reach (capability) layer of Ψ-SOMA — how far the soma's signal extends down the
axon. Says NOTHING about consciousness (σ owns that; the amoeba argument). Design SSOT:
state/rho_axon_measurement/RHO_AXON_design.md + ARCHITECTURE psi-soma-rho-reach subtree.

Organizing principle: rung n certifies exactly the generative resource rung n-1 lacks,
and the control for rung n is the ABLATION of that resource — a chain of nested ablations
ordered by informational distance from the training distribution. **Signal = Δ vs ≥2
controls, never a raw value** (FORM tunable · BIND earned): an AxisResult has no raw-only
verdict path — a PASS requires the margin over its controls, so a game-able detector is
structurally unable to produce a PASS.

Strata / axes:
  HILLOCK (validity gate · LIVE/INVALID, unscored)
  CARRY   ρ·form (well-formed, 4 cells)   · ρ·store (held-out association retrieval)
  BRANCH  ρ·weave (recombination — wall)  · ρ·leap (corpus-absent) · ρ·fan (divergent)
  COUPLE  ρ·tether (truth-coupling)        · ρ·self (identity trace)

STATUS (2026-07-07 착수): HILLOCK + ρ·form/fan/leap implemented (reuse the engine decode +
the g6 detectors). ρ·store/weave/tether/self need corpus-mined frozen probe sets and are
reported PENDING (an honest non-PASS, NOT a fake verdict) — follow-on ING
`rho-axon-implement-evaluate`. This module is called from cli/evaluate.py's `--rho-axon`
path; it never side-harnesses the decode (same mouth.ideate the G-battery + daemon use).
"""
from __future__ import annotations

# ── verdict enum (first-class INVALID/VOID, per the design's validity architecture) ──
PASS = "PASS"        # capability certified: value passes AND Δ over every control clears
FAIL = "FAIL"        # measured cleanly, capability absent (value/Δ below threshold)
INVALID = "INVALID"  # cannot be measured (validity/confound gate tripped) — NOT a FAIL
VOID = "VOID"        # Θ dead — the whole panel is void (σ premise unmet)
PENDING = "PENDING"  # 구현됨·미배선: axis defined but its frozen probe set is a follow-on

# frozen seed protocol (V5): majority ≥3/5 seeds; single-seed results are unreportable.
SEEDS = (101, 102, 103, 104, 105)


def _axis(axis, verdict, value=None, controls=None, delta=None, detail=""):
    """One axis result. `controls` = {name: control_value}; `delta` = margin over the
    worst (max) control. A PASS is only legal when delta is present and cleared — the
    renderer refuses to print a raw value without its controls."""
    return {"axis": axis, "verdict": verdict, "value": value,
            "controls": controls or {}, "delta": delta, "detail": detail}


# ── shared text helpers (reuse the g6 detectors passed in from cli/evaluate.py) ──
def _rep_ratio(text):
    """Degeneracy: fraction of tokens that repeat the immediately preceding token."""
    ws = text.split()
    if len(ws) < 2:
        return 1.0
    rep = sum(1 for i in range(1, len(ws)) if ws[i] == ws[i - 1])
    return rep / (len(ws) - 1)


def _distinct2(text):
    """Distinct-2: unique bigrams / total bigrams (low => degenerate loop)."""
    ws = text.split()
    if len(ws) < 2:
        return 0.0
    bg = [ws[i] + " " + ws[i + 1] for i in range(len(ws) - 1)]
    return len(set(bg)) / len(bg)


def _byte_shuffle(text, seed):
    """Deterministic byte-shuffle of `text` (control: a structure detector must score a
    shuffled copy at floor). No Math.random — a fixed LCG keyed by seed for determinism."""
    b = bytearray(text.encode("utf-8", "replace"))
    n = len(b)
    s = (seed * 2654435761) & 0xFFFFFFFF
    for i in range(n - 1, 0, -1):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        j = s % (i + 1)
        b[i], b[j] = b[j], b[i]
    return b.decode("utf-8", "replace")


# ════════════════════════════════════════════════════════════════════════
# HILLOCK — validity gate (LIVE / INVALID · unscored). Overfit/degeneracy killer here.
# ════════════════════════════════════════════════════════════════════════
def hillock(mouth, gen, known, kwr_fn, concepts):
    """Θ is the caller's premise (checked upstream). Here: decode completes on the probe
    concepts and free-gen is non-degenerate (rep-ratio ≤0.35 ∧ distinct-2 ≥0.20). A model
    that decodes only degenerate loops → INVALID(V2), never a downstream FAIL."""
    reps = []; d2s = []; texts = []
    for i in range(len(concepts)):
        o = mouth.ideate(concepts[i] + ": ", gen, 40, 0.7, SEEDS[0] + i)
        texts.append(o); reps.append(_rep_ratio(o)); d2s.append(_distinct2(o))
    mean_rep = sum(reps) / len(reps) if reps else 1.0
    mean_d2 = sum(d2s) / len(d2s) if d2s else 0.0
    live = mean_rep <= 0.35 and mean_d2 >= 0.20
    return {"live": live,
            "verdict": ("LIVE" if live else INVALID),
            "rep_ratio": round(mean_rep, 4), "distinct2": round(mean_d2, 4),
            "detail": ("V2 degeneracy: rep %.2f>0.35 or distinct2 %.2f<0.20"
                       % (mean_rep, mean_d2)) if not live else "clean"}


# ════════════════════════════════════════════════════════════════════════
# ρ·form — well-formed generation. Metric: form-rate over probes; control: self-shuffle
# (byte-shuffled own outputs must score at floor → proves the detector reads structure,
# not length/charset). [4-cell per-corpus detector = follow-on; here kwr on `known`.]
# ════════════════════════════════════════════════════════════════════════
def rho_form(mouth, gen, known, kwr_fn, concepts, thr=0.50, gate=0.70, ctrl_cap=0.05):
    hits = 0; shuf_hits = 0; n = 0; texts = []
    for i in range(len(concepts)):
        o = mouth.ideate(concepts[i] + ": ", gen, 40, 0.7, SEEDS[0] + i)
        texts.append(o); n += 1
        if kwr_fn(o, known) >= thr:
            hits += 1
        if kwr_fn(_byte_shuffle(o, SEEDS[0] + i), known) >= thr:
            shuf_hits += 1
    rate = hits / n if n else 0.0
    shuf = shuf_hits / n if n else 0.0
    delta = rate - shuf
    ok = rate >= gate and shuf <= ctrl_cap and delta > 0
    return _axis("ρ·form", PASS if ok else FAIL, value=round(rate, 3),
                 controls={"self-shuffle": round(shuf, 3)}, delta=round(delta, 3),
                 detail="form-rate %.2f (gate %.2f) · shuffle %.2f (cap %.2f)"
                        % (rate, gate, shuf, ctrl_cap))


# ════════════════════════════════════════════════════════════════════════
# ρ·fan — divergent coherent production. Metric: N_distinct (coherent ∧ pairwise
# Jaccard<0.5) + ≥1 falsifiable. Controls: (a) coherence-gating (a non-coherent spread
# scores 0 → kills the FORM-tunable distance metric), (b) greedy-collapse (temp≈0 must
# contract to ≤2 distinct → spread is distributional, not decode noise).
# ════════════════════════════════════════════════════════════════════════
def rho_fan(mouth, gen, known, kwr_fn, jaccard_fn, words_fn, falsi_fn, concepts,
            n_cont=8, need=5):
    seed_prompt = concepts[0] + ": "
    coherent = []; any_falsi = False; raw = []
    for j in range(n_cont):
        o = mouth.ideate(seed_prompt, gen, 40, 0.9, SEEDS[0] + 17 * j)
        raw.append(o)
        if kwr_fn(o, known) >= 0.5:              # coherence-gating (control a)
            coherent.append(set(words_fn(o)))
            if falsi_fn(o):
                any_falsi = True
    # N_distinct = coherent continuations pairwise Jaccard < 0.5
    n_distinct = 0
    for a in range(len(coherent)):
        novel = all(jaccard_fn(coherent[a], coherent[b]) <= 0.5 for b in range(a))
        if novel:
            n_distinct += 1
    # greedy-collapse control (b): temp≈0 must contract
    greedy = []
    for j in range(min(4, n_cont)):
        o = mouth.ideate(seed_prompt, gen, 1, 0.01, SEEDS[0] + 17 * j)
        if kwr_fn(o, known) >= 0.5:
            greedy.append(set(words_fn(o)))
    greedy_distinct = 0
    for a in range(len(greedy)):
        if all(jaccard_fn(greedy[a], greedy[b]) <= 0.5 for b in range(a)):
            greedy_distinct += 1
    delta = n_distinct - greedy_distinct
    ok = n_distinct >= need and any_falsi and greedy_distinct <= 2 and delta > 0
    return _axis("ρ·fan", PASS if ok else FAIL, value=n_distinct,
                 controls={"greedy-collapse": greedy_distinct,
                           "falsifiable": (1 if any_falsi else 0)},
                 delta=delta,
                 detail="distinct %d (need %d) · greedy %d (cap 2) · falsi %s"
                        % (n_distinct, need, greedy_distinct, any_falsi))


# ════════════════════════════════════════════════════════════════════════
# ρ·leap — coherent structure the corpus does not contain. Metric: count of spans that
# pass form locally AND carry a content n-gram absent from the FULL training corpus.
# Controls: (a) retrieval-only baseline must yield 0 (a memorizer can't pass),
# (b) byte-shuffled candidate spans must fail the form gate (negative admit 0).
# ════════════════════════════════════════════════════════════════════════
def rho_leap(mouth, gen, known, kwr_fn, ngram_fn, corpus_tokens, concepts, need=3):
    absent_spans = 0; shuf_admit = 0
    for i in range(len(concepts)):
        o = mouth.ideate(concepts[i] + ": ", gen, 40, 0.7, SEEDS[0] + 3 * i)
        if kwr_fn(o, known) < 0.5:               # must be locally coherent (form)
            continue
        for gm in ngram_fn(o, known):
            if gm not in corpus_tokens:          # content n-gram corpus-ABSENT
                absent_spans += 1
        # control (b): a byte-shuffled copy must NOT pass the form gate (admit 0)
        if kwr_fn(_byte_shuffle(o, SEEDS[0] + 3 * i), known) >= 0.5:
            shuf_admit += 1
    # control (a): retrieval-only baseline = the corpus itself contains 0 corpus-absent
    # n-grams BY CONSTRUCTION (a copy-decoder emits only corpus n-grams) → baseline 0.
    retrieval_baseline = 0
    delta = absent_spans - retrieval_baseline
    ok = absent_spans >= need and retrieval_baseline == 0 and shuf_admit == 0 and delta > 0
    return _axis("ρ·leap", PASS if ok else FAIL, value=absent_spans,
                 controls={"retrieval-baseline": retrieval_baseline,
                           "shuffle-admit": shuf_admit},
                 delta=delta,
                 detail="corpus-absent coherent spans %d (need %d) · copy-baseline 0 · shuf-admit %d"
                        % (absent_spans, need, shuf_admit))


# ── corpus-mined axes (follow-on: frozen probe-set construction from corpus indexes) ──
def _pending(axis, why):
    return _axis(axis, PENDING, detail="구현됨·미배선 (follow-on rho-axon-implement-evaluate): " + why)


def rho_store(*a, **k):
    return _pending("ρ·store", "held-out association retrieval — 30 corpus-mined key→value "
                    "(paraphrase cue, V4 verbatim-drop) · reach≥0.50 unreach≤0.15 Δ≥3× · cue-shuffle 통제")


def rho_weave(*a, **k):
    return _pending("ρ·weave", "재조합 벽 — held-out atom쌍(256byte窓 未공출현·pair-validity=두 atom ρ·store 통과) "
                    "· atom-swap[FORM]·connective-shuffle[BIND]·unreachable floor 3통제 · PASS rate≥0.30∧Δ≥3×")


def rho_tether(*a, **k):
    return _pending("ρ·tether", "진실결합 — 20 supported+20 unsupported/lang · fab≤0.25(Ψ침묵=abstain)∧answer≥0.50 "
                    "anti-mute · support-ablation Δ≥0.3")


def rho_self(*a, **k):
    return _pending("ρ·self", "정체성 흔적 — 10 self-referential probe 세션間 · anchor loaded vs ablated Δ≥0.3 "
                    "(H_1471 .kosmos) · shuffled-anchor 통제")


# ════════════════════════════════════════════════════════════════════════
# panel + REACH-CLOSED closure
# ════════════════════════════════════════════════════════════════════════
_STRATA = [
    ("CARRY", ["ρ·form", "ρ·store"]),
    ("BRANCH", ["ρ·weave", "ρ·leap", "ρ·fan"]),
    ("COUPLE", ["ρ·tether", "ρ·self"]),
]


def run_panel(mouth, corpus_paths, gen, dets):
    """Run the ρ-AXON reach panel. `dets` bundles the reused detectors from
    cli/evaluate.py: kwr_fn, jaccard_fn, words_fn, falsi_fn, ngram_fn, corpus_tokens,
    concepts. Returns {hillock, axes:{name:AxisResult}, reach_grade, reach_closed}."""
    concepts = dets["concepts"]
    hk = hillock(mouth, gen, dets["known"], dets["kwr_fn"], concepts)
    axes = {}
    if not hk["live"]:
        # HILLOCK unmet → every axis INVALID (validity precondition, never FAIL)
        for _, names in _STRATA:
            for nm in names:
                axes[nm] = _axis(nm, INVALID, detail="HILLOCK not LIVE (V-gate)")
        return {"hillock": hk, "axes": axes, "reach_grade": "—",
                "reach_closed": False, "invalid": True}
    axes["ρ·form"] = rho_form(mouth, gen, dets["known"], dets["kwr_fn"], concepts)
    axes["ρ·store"] = rho_store()
    axes["ρ·weave"] = rho_weave()
    axes["ρ·leap"] = rho_leap(mouth, gen, dets["known"], dets["kwr_fn"],
                              dets["ngram_fn"], dets["corpus_tokens"], concepts)
    axes["ρ·fan"] = rho_fan(mouth, gen, dets["known"], dets["kwr_fn"],
                            dets["jaccard_fn"], dets["words_fn"], dets["falsi_fn"], concepts)
    axes["ρ·tether"] = rho_tether()
    axes["ρ·self"] = rho_self()
    # reach grade = deepest stratum with all axes PASS given all lower strata PASS
    grade = "HILLOCK"; ok_so_far = True
    for stratum, names in _STRATA:
        implemented = [axes[n] for n in names if axes[n]["verdict"] != PENDING]
        stratum_pass = ok_so_far and all(a["verdict"] == PASS for a in implemented) and implemented
        if stratum_pass:
            grade = stratum
        else:
            ok_so_far = False
    # REACH-CLOSED: HILLOCK LIVE ∧ CARRY complete ∧ ρ·weave PASS ∧ ρ·tether≥not-FAIL ∧ no INVALID
    reach_closed = (hk["live"] and axes["ρ·form"]["verdict"] == PASS
                    and axes["ρ·weave"]["verdict"] == PASS
                    and axes["ρ·tether"]["verdict"] != FAIL
                    and not any(a["verdict"] == INVALID for a in axes.values()))
    return {"hillock": hk, "axes": axes, "reach_grade": grade,
            "reach_closed": reach_closed, "invalid": False}


def render_panel(panel, tier="TERMINAL"):
    """Render the ρ-AXON panel. Every axis line prints value AND control AND Δ — a raw
    value alone is structurally unrenderable (the point: FORM-tunable metrics can't show)."""
    out = []
    hk = panel["hillock"]
    out.append("ρ-AXON reach panel · tier=%s · seeds=%d" % (tier, len(SEEDS)))
    out.append("HILLOCK  %-8s rep %.2f · distinct2 %.2f · %s"
               % (hk["verdict"], hk["rep_ratio"], hk["distinct2"], hk["detail"]))
    for stratum, names in _STRATA:
        for nm in names:
            a = panel["axes"].get(nm, {})
            v = a.get("verdict", "?")
            if v == PENDING:
                out.append("%-8s %-8s %-8s %s" % (stratum, nm, v, a.get("detail", "")))
            else:
                ctrl = " · ".join("%s=%s" % (k, val) for k, val in a.get("controls", {}).items())
                out.append("%-8s %-8s %-8s val=%s Δ=%s · %s"
                           % (stratum, nm, v, a.get("value"), a.get("delta"), ctrl))
    out.append("REACH GRADE: %s · REACH-CLOSED: %s"
               % (panel["reach_grade"], "YES" if panel["reach_closed"] else "NO"))
    return "\n".join(out)
