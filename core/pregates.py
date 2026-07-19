"""core/pregates.py — H_9808 PRE-REGISTRATION GATES, CORE-owned SSOT.

WHY THIS EXISTS, in one line: every one of the four gates below would have REFUSED a spend that
actually happened, and none of them existed anywhere in this repo — `trained-control-ceiling` has
zero hits in HYPOTHESES.jsonl and in ARCHITECTURE.json.

These are **$0 closed-form referees**. They read numbers and structure, never a checkpoint, never a
forward pass. They are engine-native in the only sense that matters for an instrument
(`a_experiment_engine_native`): they are flags on the installed `anima-py` commands, not a script
beside the engine.

The contract, for all four
--------------------------
A gate returns one of three verdicts and the CLI maps them onto exit codes:

    PASS    → 0   the spend is admissible on this axis
    REFUSE  → 3   ABORT BEFORE SPEND — the number this run would produce carries no bits
    ERROR   → 2   the gate could not be evaluated (malformed input); NEVER silently a PASS

A gate that can only PASS is theatre. Each function below documents the concrete input that makes
it REFUSE, and `cli/` demonstrates that input in the toy e2e.

The four gates and the measured failure each one is paid for
------------------------------------------------------------
1. `trained_control_ceiling` + `anchor_admissible`  (lab/v4 H_007)
   H_007 pre-registered F1 = Δ(A-tug − C-dup) ≥ 0.15 with an E-anchor E[C-dup] = 0.62 INHERITED from
   another experiment's band. At target scale the unaided control measured 0.8073 (C-scaf) and 1.0000
   (C-dup) ⇒ headroom 0 ⇒ Δ≈0 was the FORCED outcome under both "mechanism alive" and "mechanism
   dead". ~7h of GPU produced zero bits. The rule: run the compute-matched control ALONE at TARGET
   scale FIRST, require control ≤ 1 − 2×bar, and refuse any anchor not measured on THIS panel at
   THIS scale — a d=64 smoke INVERTED at d=384 (+0.073 → −0.010).

2. `falsifier_headroom`  (lab/v4 H_001)
   mech-3's clause-(2) falsifier ablated to a codec already scoring 0.9083–0.9167 against a 0.1 bar.
   d_acc is bounded at 1.0, so the largest attainable Δ was 0.0917 < 0.1: the verdict DEAD was fixed
   before the experiment existed. The rule: bar ≤ (ceiling − control), with ≥2× headroom. H_001's own
   F-001-4 is carried here as a mandatory NEGATIVE CONTROL — the same arithmetic must find a genuinely
   reachable comparison REACHABLE, else the audit is condemning everything and its verdict is worthless.

3. `free_slot_audit`  (lab/v4 H_008 / H_004)
   H_004's K=6 codebook was GF(2) rank-4 ⇒ teacher-forcing completed the 2 parity slots ⇒ a
   FIELD-BLIND ceiling of 0.667 that reached held-out and inflated EVERY arm equally. The rule: the
   free-slot set is RECOMPUTED from the codebook per panel (GF(2)-rank + prefix-determinism +
   length-parity), never inherited. Supplying an inherited free-slot set that disagrees is itself a
   refusal.

4. `leak_probe`  (lab/v5 H5_001)
   v4's H_005 K3 was measured under a register whose φ→hon probe read 1.0 held-out: the drill loss
   admitted every field that fit the leaky surface, so K3 falsified only the LEAKY VARIANT of the
   question. The rule: a held-out surface→target probe at chance+ε or above voids any "learned"
   claim on that panel, before the claim is made.

Determinism
-----------
Pure stdlib. No randomness, no network, no numpy, no torch. Every number here is a closed-form
function of the input file, so two runs on the same input are byte-identical by construction.
"""

# ── exit-code contract (see module docstring) ──────────────────────────────────────────────────
PASS = 0
ERROR = 2
REFUSE = 3

# ── defaults, all overridable per call; every one of them is a CONVENTION, not a measurement ──
CEILING_DEFAULT = 1.0     # d_acc is an accuracy — bounded above at 1.0 (definitional, not measured)
CHANCE_DEFAULT = 0.5      # 2-way forced choice (definitional). Per-metric chance is re-derived where
                          # the realized partition allows it (chance-level-must-be-derived-per-metric).
HEADROOM_MULT = 2.0       # H_001/H_007: a bar needs ≥2× headroom, not merely ≥1×
CONTROL_FLOOR_MARGIN = 0.05   # a control AT chance is a dead instrument, not a clean control (H_008)
LEAK_EPS_DEFAULT = 0.05       # v5 A1 surface census: predictiveness must sit at chance + ε or below
LEAK_BAR_DEFAULT = 0.90       # at or above this, the register is a CERTAIN leak (H_005 read 1.0)


class GateError(Exception):
    """Malformed gate input — maps to exit 2, never to a PASS."""


def _num(d, key, where):
    if key not in d:
        raise GateError("%s: missing required key %r" % (where, key))
    v = d[key]
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise GateError("%s: key %r must be a number, got %r" % (where, key, v))
    return float(v)


def _fmt(x):
    return "%.4f" % float(x)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
#  GATE 1 — TRAINED-CONTROL CEILING  (lab/v4 H_007 · `anima-py train --trained-control-ceiling`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════

ANCHOR_REQUIRED_KEYS = ("measured", "panel", "arm", "scale", "seeds", "source")


def anchor_admissible(anchor, panel, scale):
    """Is this control anchor allowed to certify a run on `panel` at `scale`?

    THE WHOLE POINT: an anchor is refused unless it was MEASURED, on THIS panel, at THIS scale.
    H_007 froze E[C-dup] = 0.62 taken from H_003/H_004's band — a different panel, a different
    task, never a trained control here. Truth was 1.00. Separately, its own d=64 smoke read +0.073
    and INVERTED to −0.010 at d=384, so a smaller-scale measurement of the RIGHT panel is refused
    too.

    `scale` is the caller's OWN resolved target scale (trainer args), not a user restatement of it.
    Comparison is over the keys the anchor itself declares, so an anchor may pin a subset
    ({d, L, steps}) without having to enumerate every trainer argument — but every key it DOES
    declare must match exactly.

    Returns (ok: bool, reasons: list[str]).  reasons is empty iff ok.

    REFUSES on:  measured != true · panel mismatch · any declared scale key mismatch ·
                 empty seed set · a missing required key.
    """
    reasons = []
    if not isinstance(anchor, dict):
        raise GateError("control anchor must be a JSON object")
    for k in ANCHOR_REQUIRED_KEYS:
        if k not in anchor:
            reasons.append("MALFORMED: anchor is missing required key %r "
                           "(required: %s)" % (k, ", ".join(ANCHOR_REQUIRED_KEYS)))
    if reasons:
        return False, reasons

    if anchor["measured"] is not True:
        reasons.append("NOT-MEASURED: anchor.measured is %r, not true — an estimate, a prior, or a "
                       "summary is not a trained-control anchor (H_007: E[C-dup]=0.62 was fiction, "
                       "truth was 1.00)" % (anchor["measured"],))

    if anchor["panel"] != panel:
        reasons.append("PANEL-MISMATCH: anchor was measured on panel %r, this run declares %r — an "
                       "anchor from another panel is INHERITED and refused"
                       % (anchor["panel"], panel))

    a_scale = anchor["scale"]
    if not isinstance(a_scale, dict) or not a_scale:
        reasons.append("MALFORMED: anchor.scale must be a non-empty object "
                       "(e.g. {\"d\": 384, \"L\": 4, \"steps\": 4000})")
    else:
        for k, v in sorted(a_scale.items()):
            if k not in scale:
                reasons.append("SCALE-UNVERIFIABLE: anchor pins %r=%r but this run does not expose "
                               "%r — the gate cannot certify the scale matched" % (k, v, k))
            elif scale[k] != v:
                reasons.append("SCALE-MISMATCH: anchor %s=%r vs this run %s=%r — a smaller-scale "
                               "smoke is NOT an anchor (H_007: d=64 read +0.073, d=384 read −0.010; "
                               "the sign inverted)" % (k, v, k, scale[k]))

    seeds = anchor["seeds"]
    if not isinstance(seeds, dict) or not seeds:
        reasons.append("MALFORMED: anchor.seeds must be a non-empty object {seed: control_score}")
    else:
        for s, v in sorted(seeds.items()):
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                reasons.append("MALFORMED: anchor.seeds[%r] = %r is not a number" % (s, v))

    return (not reasons), reasons


def trained_control_ceiling(bar, control, chance=CHANCE_DEFAULT,
                            margin=CONTROL_FLOOR_MARGIN, headroom_mult=HEADROOM_MULT,
                            ceiling=CEILING_DEFAULT):
    """The H_007 G-1.5 arithmetic on ONE control reading.

    Two ways to fail, and BOTH are real refusals measured in lab/v4:

      SATURATED — control > ceiling − headroom_mult×bar.  The band above the control is narrower
                  than the bar, so Δ ≥ bar is unattainable and Δ≈0 is forced regardless of the
                  mechanism. H_007: bar 0.15 ⇒ cap 0.70; C-scaf measured 0.8073. REFUSE.
      DEAD      — control < chance + margin.  A control sitting at chance is not a clean control,
                  it is a broken instrument, and the mechanism arm would be scored against noise.
                  H_008 G-1.5a: C-dup measured 0.5104/0.50/0.4948/0.5156 at every budget on
                  SWAP-XOR-B (a mis-specified audit had forced a parity trap). REFUSE.

    Returns a dict; `ok` is True only when the control sits strictly inside the band.
    """
    bar = float(bar)
    control = float(control)
    if bar <= 0.0:
        raise GateError("--trained-control-ceiling bar must be > 0 (got %r)" % bar)
    cap = ceiling - headroom_mult * bar
    floor = chance + margin
    saturated = control > cap
    dead = control < floor
    return {
        "bar": bar, "control": control, "ceiling": ceiling, "chance": chance,
        "cap": cap, "floor": floor,
        "headroom": ceiling - control,
        "headroom_required": headroom_mult * bar,
        "saturated": saturated, "dead": dead,
        "ok": (not saturated) and (not dead),
    }


def trained_control_gate(bar, anchor, panel, scale, **kw):
    """Full gate 1: provenance + arithmetic over EVERY seed in the anchor.

    Multi-seed reading is conservative in both directions — the WORST (max) control decides
    saturation and the BEST-case (min) decides deadness — because a single saturated seed already
    means that seed's arm carries no bits, and a split verdict is INCONCLUSIVE, never a green
    (v4's standing anti-fishing rule).
    """
    ok_prov, reasons = anchor_admissible(anchor, panel, scale)
    out = {"provenance_ok": ok_prov, "reasons": list(reasons), "per_seed": [], "ok": False}
    if not ok_prov:
        return out
    per = []
    for s in sorted(anchor["seeds"]):
        r = trained_control_ceiling(bar, anchor["seeds"][s], **kw)
        r["seed"] = s
        per.append(r)
    out["per_seed"] = per
    sat = [r for r in per if r["saturated"]]
    dead = [r for r in per if r["dead"]]
    for r in sat:
        out["reasons"].append(
            "SATURATED: seed %s control=%s > cap %s (= %s − %s×bar %s) — the band above the control "
            "is narrower than the bar; Δ≈0 is FORCED whether the mechanism works or not (H_007)"
            % (r["seed"], _fmt(r["control"]), _fmt(r["cap"]), _fmt(r["ceiling"]),
               _fmt(kw.get("headroom_mult", HEADROOM_MULT)), _fmt(r["bar"])))
    for r in dead:
        out["reasons"].append(
            "DEAD-CONTROL: seed %s control=%s < floor %s (chance %s + margin %s) — a control at "
            "chance is a broken instrument, not a clean control (H_008 G-1.5a)"
            % (r["seed"], _fmt(r["control"]), _fmt(r["floor"]), _fmt(r["chance"]),
               _fmt(kw.get("margin", CONTROL_FLOOR_MARGIN))))
    out["ok"] = not out["reasons"]
    return out


# ═══════════════════════════════════════════════════════════════════════════════════════════════
#  GATE 2 — FALSIFIER HEADROOM  (lab/v4 H_001 · `anima-py evaluate --falsifier-headroom`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def max_attainable_delta(ceiling, control):
    """The largest Δ ANY mechanism — working, broken, or imaginary — can show over `control`."""
    return float(ceiling) - float(control)


def falsifier_reachable(bar, control, ceiling=CEILING_DEFAULT, headroom_mult=HEADROOM_MULT):
    """Can the pre-registered `bar` be attained at all, with the required headroom?"""
    d = max_attainable_delta(ceiling, control)
    return {
        "bar": float(bar), "control": float(control), "ceiling": float(ceiling),
        "max_attainable_delta": d,
        "required": headroom_mult * float(bar),
        "attainable": d >= float(bar),
        "reachable": d >= headroom_mult * float(bar),
    }


def falsifier_headroom_gate(spec):
    """Full gate 2: reachability arithmetic + H_001's own mandatory negative control.

    Spec (JSON):
        {"bar": 0.10, "ceiling": 1.0, "headroom_mult": 2.0,
         "controls":         [{"arm": "M_s4302", "score": 0.9083, "source": "..."} , ...],
         "negative_controls":[{"arm": "C1_s4302", "score": 0.6167, "source": "..."}, ...]}

    `controls` are the arms the falsifier will actually be scored against — EVERY one must clear
    the bar with ≥headroom_mult× room, or the falsifier is VACUOUS and the run is refused.

    `negative_controls` carry F-001-4 verbatim: an audit that condemns EVERY comparison is not
    detecting vacuity, it is condemning arithmetic itself, and its own verdict is worthless. At
    least one negative control must come back REACHABLE. Omitting the section is an ERROR, not a
    pass — a one-sided audit is exactly the failure this gate exists to catch.

    REFUSES on:  H_001's real numbers — bar 0.10 against control 0.9083 gives max Δ 0.0917 < 0.10,
                 so DEAD is returned unconditionally before the experiment exists.
    """
    if not isinstance(spec, dict):
        raise GateError("--falsifier-headroom spec must be a JSON object")
    bar = _num(spec, "bar", "spec")
    if bar <= 0.0:
        raise GateError("spec.bar must be > 0 (got %r)" % bar)
    ceiling = float(spec.get("ceiling", CEILING_DEFAULT))
    hm = float(spec.get("headroom_mult", HEADROOM_MULT))
    controls = spec.get("controls")
    negs = spec.get("negative_controls")
    if not isinstance(controls, list) or not controls:
        raise GateError("spec.controls must be a non-empty list of {arm, score, source}")
    if not isinstance(negs, list) or not negs:
        raise GateError(
            "spec.negative_controls must be a non-empty list — H_001's F-001-4 is MANDATORY: an "
            "audit that finds every comparison unreachable is condemning arithmetic, not detecting "
            "vacuity, and its verdict is worthless. Supply at least one comparison this gate is "
            "expected to find REACHABLE.")

    def _rows(items, where):
        out = []
        for it in items:
            if not isinstance(it, dict):
                raise GateError("%s entries must be objects {arm, score, source}" % where)
            if "arm" not in it or "source" not in it:
                raise GateError("%s entry %r must cite arm AND source — a bare number is a number "
                                "that lost its experiment (v4 d_acc discipline)" % (where, it))
            sc = _num(it, "score", "%s[%s]" % (where, it["arm"]))
            if not (ceiling - 1.0 - 0.5 <= sc <= ceiling):
                raise GateError("%s[%s] score %r is out of range (0, %r] — a mis-transcribed number "
                                "voids the audit (H_001 F-001-6 bounds check)"
                                % (where, it["arm"], sc, ceiling))
            r = falsifier_reachable(bar, sc, ceiling, hm)
            r["arm"] = it["arm"]
            r["source"] = it["source"]
            out.append(r)
        return out

    rows = _rows(controls, "controls")
    nrows = _rows(negs, "negative_controls")
    reasons = []
    for r in rows:
        if not r["attainable"]:
            reasons.append(
                "VACUOUS: arm %s scores %s, so the largest attainable Δ is %s − %s = %s, strictly "
                "BELOW the pre-registered bar %s. The falsifier returns its verdict unconditionally, "
                "before the experiment exists (H_001).  src: %s"
                % (r["arm"], _fmt(r["control"]), _fmt(ceiling), _fmt(r["control"]),
                   _fmt(r["max_attainable_delta"]), _fmt(bar), r["source"]))
        elif not r["reachable"]:
            reasons.append(
                "NO-HEADROOM: arm %s scores %s ⇒ max Δ %s ≥ bar %s but < %s×bar = %s. The bar is "
                "attainable only at the metric's absolute ceiling, so measurement noise alone "
                "decides the verdict.  src: %s"
                % (r["arm"], _fmt(r["control"]), _fmt(r["max_attainable_delta"]), _fmt(bar),
                   _fmt(hm), _fmt(r["required"]), r["source"]))
    if not any(n["reachable"] for n in nrows):
        reasons.append(
            "AUDIT-VOID: NO negative control came back reachable — this gate is condemning every "
            "comparison it is shown, so it is not detecting vacuity and its own verdict carries no "
            "bits (H_001 F-001-4).")
    return {"bar": bar, "ceiling": ceiling, "headroom_mult": hm,
            "controls": rows, "negative_controls": nrows,
            "reasons": reasons, "ok": not reasons}


# ═══════════════════════════════════════════════════════════════════════════════════════════════
#  GATE 3 — FREE-SLOT SCORE  (lab/v4 H_004/H_008 · `anima-py evaluate --free-slot-score`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def gf2_rank(rows):
    """GF(2) rank of a 0/1 matrix given as a list of row-lists. Pure integer bit arithmetic."""
    if not rows:
        return 0
    width = len(rows[0])
    vecs = []
    for r in rows:
        v = 0
        for j, b in enumerate(r):
            if b:
                v |= (1 << j)
        vecs.append(v)
    rank = 0
    pivots = []
    for j in range(width):
        bit = 1 << j
        pick = None
        for i in range(len(vecs)):
            if vecs[i] & bit and i not in pivots:
                pick = i
                break
        if pick is None:
            continue
        pivots.append(pick)
        rank += 1
        for i in range(len(vecs)):
            if i != pick and (vecs[i] & bit):
                vecs[i] ^= vecs[pick]
    return rank


def _gf2_dependent_columns(codewords):
    """Which SLOTS (columns) are a GF(2) combination of the slots to their left?

    Left-to-right greedy: a column already inside the span of its predecessors is DEPENDENT — its
    value is recoverable from the prefix without reading the field. That is exactly H_004's defect:
    a K=6 rank-4 codebook has 2 such columns, teacher-forcing completes them for free, and every
    arm is inflated equally.
    """
    if not codewords:
        return []
    n = len(codewords[0])
    cols = [[cw[j] for cw in codewords] for j in range(n)]
    dep = []
    kept = []
    for j in range(n):
        trial = kept + [cols[j]]
        r_before = gf2_rank([list(x) for x in zip(*kept)]) if kept else 0
        r_after = gf2_rank([list(x) for x in zip(*trial)])
        if r_after == r_before:
            dep.append(j)
        else:
            kept.append(cols[j])
    return dep


def free_slot_audit(codebook, bar=None, inherited_free_slots=None):
    """Recompute the free-slot set from the codebook and derive the FIELD-BLIND ceiling.

    Spec (JSON):
        {"panel": "...", "slots": ["s0","s1",...],
         "codewords": [[0,1,0,1,1,0], ...],
         "bar": 0.15,                       # optional pre-registered bar to check reachability
         "inherited_free_slots": [0,1,2,4]} # optional — supplying it is how you get REFUSED

    A slot is DETERMINED (i.e. NOT free) when a field-blind reader can fill it from the prefix:
      (a) prefix-determinism — every codeword sharing a prefix agrees on this slot, so under
          teacher-forcing the true prefix hands the slot over; or
      (b) GF(2) dependence — for a binary codebook, the column is an XOR of columns to its left.
          This is H_004's parity-completion route.

    FIELD-BLIND CEILING = mean over slots of (1.0 if determined else 1/|choices at that slot|).
    On a K=6 binary codebook of GF(2) rank 4 that is (2×1 + 4×0.5)/6 = 0.6667 — H_004's measured
    0.667 falls straight out of the definition, which is why this is the definition used.

    CHANCE is re-derived from the realized partition (mean of 1/|choices|), never assumed
    (chance-level-must-be-derived-per-metric): a codebook with unequal alphabet sizes per slot has
    a chance floor that is NOT 0.5.

    REFUSES on:  any determined slot (ceiling above chance) · a length-parity violation · a
                 supplied inherited free-slot set that disagrees with the recomputed one · a bar
                 that does not clear the recomputed ceiling with 2× headroom.
    """
    if not isinstance(codebook, dict):
        raise GateError("--free-slot-score codebook must be a JSON object")
    cws = codebook.get("codewords")
    if not isinstance(cws, list) or len(cws) < 2:
        raise GateError("codebook.codewords must be a list of ≥2 codewords")
    n = len(cws[0])
    if n < 1:
        raise GateError("codebook.codewords[0] is empty")
    reasons = []

    # ── length parity: unequal codeword length is itself a field-blind cue ─────────────────────
    bad_len = [i for i, cw in enumerate(cws) if not isinstance(cw, list) or len(cw) != n]
    length_parity = not bad_len
    if bad_len:
        reasons.append("LENGTH-PARITY: codewords %s do not have the common slot count %d — an "
                       "unequal length is a field-blind cue and voids every slot-wise number"
                       % (bad_len[:6], n))
        return {"ok": False, "reasons": reasons, "n_slots": n, "length_parity": False}

    slots = codebook.get("slots") or ["s%d" % j for j in range(n)]
    if len(slots) != n:
        raise GateError("codebook.slots has %d names for %d slots" % (len(slots), n))

    # symbol-level length parity (a longer gold form is readable without the field)
    sym_len_mismatch = []
    for j in range(n):
        lens = set(len(str(cw[j])) for cw in cws)
        if len(lens) > 1:
            sym_len_mismatch.append(slots[j])
    if sym_len_mismatch:
        reasons.append("LENGTH-PARITY: slots %s carry symbols of differing rendered length — form "
                       "length alone discriminates the answer (v4 A4 length-parity audit)"
                       % (sym_len_mismatch,))

    # ── (a) prefix-determinism ────────────────────────────────────────────────────────────────
    prefix_det = []
    for j in range(n):
        groups = {}
        for cw in cws:
            groups.setdefault(tuple(cw[:j]), set()).add(cw[j])
        if all(len(v) <= 1 for v in groups.values()):
            prefix_det.append(j)

    # ── (b) GF(2) dependence (binary codebooks only) ──────────────────────────────────────────
    is_binary = all(cw[j] in (0, 1) for cw in cws for j in range(n))
    gf2_dep = _gf2_dependent_columns(cws) if is_binary else []
    rank = gf2_rank([list(cw) for cw in cws]) if is_binary else None

    determined = sorted(set(prefix_det) | set(gf2_dep))
    free = [j for j in range(n) if j not in determined]

    choices = [len(set(cw[j] for cw in cws)) for j in range(n)]
    ceiling = sum(1.0 if j in determined else 1.0 / max(1, choices[j]) for j in range(n)) / n
    chance = sum(1.0 / max(1, c) for c in choices) / n

    if determined:
        reasons.append(
            "REDUNDANT-CODEBOOK: slots %s are field-blind determinable (%s) ⇒ FIELD-BLIND ceiling "
            "%s vs chance %s. Teacher-forcing completes them for free and inflates EVERY arm "
            "equally (H_004: K=6 codebook, GF(2) rank 4, ceiling 0.667 reached held-out)."
            % ([slots[j] for j in determined],
               "prefix-determined" if prefix_det and not gf2_dep else
               ("GF(2)-dependent" if gf2_dep and not prefix_det else "prefix-determined + GF(2)-dependent"),
               _fmt(ceiling), _fmt(chance)))

    if inherited_free_slots is None:
        inherited_free_slots = codebook.get("inherited_free_slots")
    if inherited_free_slots is not None:
        if sorted(inherited_free_slots) != free:
            reasons.append(
                "INHERITED-FREE-SLOT-SET: the supplied set %s disagrees with the set recomputed "
                "from THIS codebook %s. A free-slot set is recomputed per panel, never inherited "
                "(v5 G3) — the inherited set would score slots this codebook hands over for free."
                % (sorted(inherited_free_slots), free))

    if bar is None:
        bar = codebook.get("bar")
    if bar is not None:
        bar = float(bar)
        room = CEILING_DEFAULT - ceiling
        if room < HEADROOM_MULT * bar:
            reasons.append(
                "BAR-UNREACHABLE-OVER-CEILING: bar %s needs %s of room above the FIELD-BLIND "
                "ceiling %s, but only %s exists. The bar is measuring codebook redundancy, not the "
                "mechanism." % (_fmt(bar), _fmt(HEADROOM_MULT * bar), _fmt(ceiling), _fmt(room)))

    return {"ok": not reasons, "reasons": reasons,
            "n_slots": n, "slots": slots, "n_codewords": len(cws),
            "length_parity": length_parity and not sym_len_mismatch,
            "binary": is_binary, "gf2_rank": rank,
            "prefix_determined": [slots[j] for j in prefix_det],
            "gf2_dependent": [slots[j] for j in gf2_dep],
            "determined": determined, "free_slots": free,
            "choices": choices,
            "field_blind_ceiling": ceiling, "chance": chance}


# ═══════════════════════════════════════════════════════════════════════════════════════════════
#  GATE 4 — REGISTER-LEAK PROBE  (lab/v5 H5_001 · `anima-py evaluate --register-leak-probe`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def leak_probe(items, nmax=4, bar=LEAK_BAR_DEFAULT, eps=LEAK_EPS_DEFAULT):
    """Held-out surface→target probe. If the register reads the answer off the surface, REFUSE.

    Spec (JSON):
        {"panel": "...", "nmax": 4, "bar": 0.90, "eps": 0.05,
         "items": [{"surface": "…", "target": "hon", "split": "fit"},
                   {"surface": "…", "target": "pln", "split": "heldout"}, ...]}

    The probe is a closed-form EXACT-COUNT census, deliberately not a trained classifier: for every
    byte-level n-gram (n ≤ nmax) occurring in the FIT split, the rule "surface contains g ⇒ predict
    the fit-majority target for g, else predict the global fit-majority" is evaluated on the
    HELD-OUT split. The reported leak is the max held-out accuracy over all such rules. A trained
    probe would certify the probe; an exact count certifies the SURFACE.

    Chance is re-derived as the held-out majority-class rate — the accuracy of the best rule that
    ignores the surface entirely — so the comparison is against what a surface-blind reader already
    gets, not against a nominal 0.5.

    REFUSES on:  leak > chance + eps.  Reads at or above `bar` are additionally labelled a CERTAIN
                 leak — that is the 1.0 that v4's G3-0d probe returned and that made H_005's K3
                 falsify only the leaky variant of its question (v5 H5_001).
    """
    if not isinstance(items, list) or not items:
        raise GateError("--register-leak-probe spec.items must be a non-empty list")
    fit, held = [], []
    for it in items:
        if not isinstance(it, dict) or "surface" not in it or "target" not in it:
            raise GateError("each item must be {surface, target, split}")
        sp = it.get("split", "heldout")
        if sp not in ("fit", "heldout"):
            raise GateError("item split must be 'fit' or 'heldout' (got %r)" % sp)
        (fit if sp == "fit" else held).append((str(it["surface"]), str(it["target"])))
    if not fit or not held:
        raise GateError("spec.items needs BOTH a 'fit' and a 'heldout' split — a probe scored on "
                        "its own fit data measures memorisation, not leak")

    def _majority(pairs):
        c = {}
        for _, t in pairs:
            c[t] = c.get(t, 0) + 1
        return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

    global_major = _majority(fit)
    # held-out majority-class rate = the surface-BLIND accuracy = this metric's realized chance
    held_counts = {}
    for _, t in held:
        held_counts[t] = held_counts.get(t, 0) + 1
    chance = max(held_counts.values()) / float(len(held))

    grams = set()
    for s, _ in fit:
        b = s.encode("utf-8", "surrogateescape")
        for n in range(1, int(nmax) + 1):
            for i in range(len(b) - n + 1):
                grams.add(b[i:i + n])

    # Each n-gram defines a two-cell DECISION STUMP fit by exact count on the fit split:
    #   contains g      ⇒ predict the fit-majority target among fit items that contain g
    #   does not contain⇒ predict the fit-majority target among fit items that do not
    # (an earlier version predicted the GLOBAL majority off-cell and skipped any gram whose
    # in-cell majority equalled it — which silently skipped the leaking gram whenever the leak
    # was carried by the majority class. Caught by the selftest before this gate was ever used.)
    best = (chance, None, global_major)
    for g in sorted(grams):
        hit, miss = [], []
        for s, t in fit:
            (hit if g in s.encode("utf-8", "surrogateescape") else miss).append((s, t))
        if not hit:
            continue
        maj_in = _majority(hit)
        maj_out = _majority(miss) if miss else global_major
        acc = 0
        for s, t in held:
            pred = maj_in if g in s.encode("utf-8", "surrogateescape") else maj_out
            acc += (pred == t)
        acc /= float(len(held))
        if acc > best[0]:
            best = (acc, g, maj_in)

    leak, gram, maj = best
    # The probe works on BYTES, so a winning n-gram is often a fragment of a multi-byte character
    # and does not decode. Render it as hex in that case rather than as a replacement char — a
    # U+FFFD in a gate report tells the reader nothing about which bytes leaked.
    if gram is None:
        gram_s = None
    else:
        try:
            gram_s = gram.decode("utf-8")
        except UnicodeDecodeError:
            gram_s = "<bytes %s>" % gram.hex(" ")
    reasons = []
    certain = leak >= float(bar)
    if leak > chance + float(eps):
        reasons.append(
            "REGISTER-LEAKS: a held-out surface n-gram probe reads the target at %s vs a "
            "surface-blind chance of %s (+%s > eps %s)%s. The surface hands the answer over, so "
            "the drill loss admits EVERY field that fits the surface and no 'learned' claim on "
            "this panel is about learning (v5 H5_001; v4 H_005's K3 probe read 1.0 and falsified "
            "only the leaky variant of its question).%s"
            % (_fmt(leak), _fmt(chance), _fmt(leak - chance), _fmt(eps),
               ("  worst n-gram: %r ⇒ %r" % (gram_s, maj)) if gram else "",
               "  READ ≥ bar %s ⇒ CERTAIN LEAK." % _fmt(bar) if certain else ""))
    return {"ok": not reasons, "reasons": reasons,
            "leak": leak, "chance": chance, "eps": float(eps), "bar": float(bar),
            "certain_leak": certain,
            "worst_ngram": gram_s,
            "worst_ngram_predicts": (maj if gram else None),
            "n_fit": len(fit), "n_heldout": len(held), "nmax": int(nmax)}


# ═══════════════════════════════════════════════════════════════════════════════════════════════
#  shared CLI rendering — one verdict shape for all four gates
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def render(title, res, notes=()):
    """Print a gate result and return its exit code (0 PASS / 3 REFUSE)."""
    print("=" * 78)
    print(title)
    print("=" * 78)
    for line in notes:
        print("  " + line)
    ok = bool(res.get("ok"))
    if ok:
        print("\n  🟢 GATE PASS — admissible on this axis. This is NOT a result and NOT a "
              "prediction that the run will be green.")
    else:
        print("\n  ⛔ GATE REFUSE — ABORT BEFORE SPEND. Reasons:")
        for r in res.get("reasons", ()):
            print("    · " + r)
    print("\nVERDICT: " + ("PASS" if ok else "REFUSE"))
    return PASS if ok else REFUSE


def selftest():
    """Closed-form self-test: every gate is exercised on BOTH a passing and a refusing input.

    The refusing inputs are the REAL measured numbers from the lab/v4 and lab/v5 failures, so this
    also serves as a regression test that each gate would have caught the spend it was paid for.
    """
    checks = []

    def ck(name, cond):
        checks.append((name, bool(cond)))

    # ── gate 1 ────────────────────────────────────────────────────────────────────────────────
    scale = {"arch": "clm", "d": 384, "L": 4, "steps": 4000}
    good = {"measured": True, "panel": "swap_xor_f2", "arm": "C-dup",
            "scale": {"d": 384, "L": 4, "steps": 4000}, "seeds": {"0": 0.62},
            "source": "state/.../verdict.json"}
    ck("g1 pass: control 0.62 under bar 0.15",
       trained_control_gate(0.15, good, "swap_xor_f2", scale)["ok"])
    sat = dict(good, seeds={"0": 0.8073}, arm="C-scaf")   # H_007's measured C-scaf
    ck("g1 REFUSE: H_007 C-scaf 0.8073 saturates cap 0.70",
       not trained_control_gate(0.15, sat, "swap_xor_f2", scale)["ok"])
    dead = dict(good, seeds={"0": 0.5104})                # H_008 G-1.5a C-dup at chance
    ck("g1 REFUSE: H_008 C-dup 0.5104 is a dead control",
       not trained_control_gate(0.15, dead, "swap_xor_f2", scale)["ok"])
    smoke = dict(good, scale={"d": 64, "L": 4, "steps": 2000})
    ck("g1 REFUSE: d=64 smoke anchor for a d=384 run",
       not trained_control_gate(0.15, smoke, "swap_xor_f2", scale)["ok"])
    ck("g1 REFUSE: anchor from another panel",
       not trained_control_gate(0.15, dict(good, panel="other_f2"), "swap_xor_f2", scale)["ok"])
    ck("g1 REFUSE: measured != true",
       not trained_control_gate(0.15, dict(good, measured=False), "swap_xor_f2", scale)["ok"])

    # ── gate 2 (H_001's verbatim arithmetic) ──────────────────────────────────────────────────
    neg = [{"arm": "C1_s4302", "score": 0.6167, "source": "~/anima-weights/morphatom/vC1_f2.json"}]
    vac = falsifier_headroom_gate({"bar": 0.10, "controls": [
        {"arm": "M_s4302", "score": 0.9083, "source": "~/anima-weights/morphatom/vM_f2.json"},
        {"arm": "M_s7", "score": 0.9167, "source": "cement_result/vM_s7_f2.json"}],
        "negative_controls": neg})
    ck("g2 REFUSE: H_001 mech-3 clause (2) is vacuous", not vac["ok"])
    ck("g2 arithmetic: max Δ over M_s4302 = 0.0917",
       abs(vac["controls"][0]["max_attainable_delta"] - 0.0917) < 1e-9)
    ck("g2 negative control 0.6167 IS reachable (F-001-4)", vac["negative_controls"][0]["reachable"])
    ck("g2 pass: bar 0.10 vs control 0.6167",
       falsifier_headroom_gate({"bar": 0.10, "controls": neg, "negative_controls": neg})["ok"])

    # ── gate 3 (H_004's K=6 rank-4 codebook reproduces the 0.667 ceiling) ─────────────────────
    # 6 binary slots; slots 4,5 are XOR-parities of slots 0..3 ⇒ GF(2) rank 4.
    import itertools
    cws = []
    for bits in itertools.product((0, 1), repeat=4):
        p1 = bits[0] ^ bits[1]
        p2 = bits[2] ^ bits[3]
        cws.append(list(bits) + [p1, p2])
    r = free_slot_audit({"codewords": cws})
    ck("g3 REFUSE: rank-4 K=6 codebook", not r["ok"])
    ck("g3 gf2_rank == 4", r["gf2_rank"] == 4)
    ck("g3 field-blind ceiling == 0.667 (H_004's number falls out)",
       abs(r["field_blind_ceiling"] - 2.0 / 3.0) < 1e-9)
    full = [list(b) for b in itertools.product((0, 1), repeat=4)]
    rf = free_slot_audit({"codewords": full})
    ck("g3 pass: full-rank codebook, ceiling == chance == 0.5",
       rf["ok"] and abs(rf["field_blind_ceiling"] - 0.5) < 1e-9)
    ck("g3 REFUSE: inherited free-slot set that disagrees",
       not free_slot_audit({"codewords": full}, inherited_free_slots=[0, 1, 2])["ok"])

    # ── gate 4 ────────────────────────────────────────────────────────────────────────────────
    leaky = ([{"surface": "the LEAK cat sat", "target": "hon", "split": "fit"} for _ in range(4)]
             + [{"surface": "the cat sat", "target": "pln", "split": "fit"} for _ in range(4)]
             + [{"surface": "a LEAK dog ran", "target": "hon", "split": "heldout"} for _ in range(4)]
             + [{"surface": "a dog ran", "target": "pln", "split": "heldout"} for _ in range(4)])
    ck("g4 REFUSE: surface carries the answer token", not leak_probe(leaky)["ok"])
    # DELEAKED: every surface form occurs with BOTH targets equally often, so no n-gram — of any
    # length — is predictive, and the best stump can only match the surface-blind majority rate.
    # (The first draft of this fixture used "alpha 0..7" with target = i%2; the DIGIT carried the
    # target and the gate correctly refused it. The fixture was wrong, not the gate.)
    clean = []
    for split in ("fit", "heldout"):
        for form in ("xx qq", "yy qq"):
            for tgt in ("hon", "pln"):
                for _ in range(2):
                    clean.append({"surface": form, "target": tgt, "split": split})
    ck("g4 pass: deleaked register sits at chance", leak_probe(clean)["ok"])

    return checks
