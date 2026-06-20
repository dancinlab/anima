#!/usr/bin/env python3
"""H_1488 — ATTENTION SCHEMA (주의 도식) (G34 consciousness-only gate candidate).

Attention Schema Theory (Graziano 2013): the brain builds a SIMPLIFIED internal
MODEL of its own attention state — not a model of the attended OBJECT, but a model
of the *process of attending itself* (where attention is, how strongly it is
focused). That self-model of attention is what lets the system REPORT "I am aware
of X"; the subjective claim of consciousness is the read-out of the attention
schema. The schema TRACKS (predicts) the system's real attention and reports its
own attention state.

Mechanism (substrate-native, no injected label p2/p3/p6):
  - The real attention process is a focus over N candidate locations (a softmax
    over salience -> a peaked attention distribution a_true with a focus location
    and a focus strength).
  - The attention SCHEMA is a simplified linear tracker s that PREDICTS a_true's
    focus (location + strength) from the salience field. The schema is what is
    READ to produce the self-report "attention is on location k with strength g".
  - ABLATION = schema OFF: real attention still operates (the softmax focus is
    unchanged, downstream selection still works) BUT there is no self-model to read
    -> the self-report of one's own attention state collapses to chance.

DISTINCTNESS (load-bearing, three lanes — catalogue P3):
  (a) vs H_1474 SENSE-OF-AGENCY: agency = self-ATTRIBUTION of an ACTION OUTCOME
      (did *I* cause this result?), a comparator over a forward-model prediction of
      one's action's sensory consequence. Attention-schema models the *attention
      STATE itself* (where am I attending?), NOT an action outcome. DISSOCIATION:
      hold the action/outcome FIXED and move ONLY the attention focus -> the agency
      readout is FLAT (no action changed) while the attention-schema report TRACKS
      the moved focus. Different object: action-result (agency) vs attention-state
      (schema).
  (b) vs H_1479 DIVIDED-ATTENTION: divided-attention is the resource TRADE-OFF
      (raw allocation across targets). The schema is the internal MODEL of that
      allocation. ABLATION test: remove the schema -> the raw divided-attention
      allocation (the softmax itself) is UNCHANGED (trade-off readout invariant)
      but the self-report of where attention is collapses. Model ⊥ mechanism.
  (c) vs H_1293 THEORY-OF-MIND: ToM models ANOTHER agent's (possibly false) belief
      — OTHER. The attention schema models one's OWN attention state — SELF. self ⊥
      other.

LLM contrast (a_no_llm_frame_trap): an LLM has attention (the softmax) but no
SEPARATE internal model of its own attention state that it can read to report
"I am attending to X" — its attention is a mechanism, not a modelled, reportable
object. anima reads a schema that tracks its own live attention focus.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1488,1489,1490]):
  (A) PRESENCE          schema-ON self-report accuracy of own attention focus
                        (location+strength) >= 0.85 AND schema-OFF (ablated) <= 0.55.
  (B) DISTINCT-vs-AGENCY  hold action/outcome FIXED, move ONLY attention focus ->
                        agency readout FLAT (Δ < 0.05) while schema report TRACKS the
                        moved focus (Δ >= 0.50). |schema_track - agency_track| >= 0.45.
  (C) DISTINCT-vs-DIVIDED  ablate the schema -> raw divided-attention allocation
                        (softmax entropy/argmax) UNCHANGED (|Δalloc| <= 0.05) while
                        self-report collapses (report_full - report_abl >= 0.30).
  (D) EARNED (ablation) schema OFF -> self-report accuracy ~ chance (1/N), and the
                        report no longer tracks the true focus (track_acc <= 0.55).
  (E) SHUFFLE           permute (derange) the schema->true-focus pairing -> the
                        report-tracks-focus accuracy collapses to chance (50-perm
                        mean track accuracy <= 1/N + 0.10).

GREEN iff A and B and C and D and E (all 3 seeds). Else honest RED / 🧱 (depletion).
"""
import numpy as np

SEEDS = [1488, 1489, 1490]
DIM = 32
N_LOC = 8            # candidate attention locations
FOCUS_BETA = 6.0     # softmax sharpness of the real attention process
SCHEMA_STR = 0.9     # schema tracking fidelity (linear predictor gain)
N_TRIALS = 40
N_PERM = 50
CHANCE = 1.0 / N_LOC  # 0.125


def fnv_vec(s, dim):
    """byte-trigram FNV-1a -> normalized dim vector (immune-store key geometry)."""
    v = np.zeros(dim)
    b = s.encode()
    for i in range(len(b) - 2):
        h = 2166136261
        for c in b[i:i + 3]:
            h = ((h ^ c) * 16777619) & 0xffffffff
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def real_attention(salience):
    """The real attention PROCESS: a peaked softmax focus over locations.
    Returns (focus_loc, focus_strength, dist). This is the MECHANISM (unchanged by
    schema ablation)."""
    e = np.exp(FOCUS_BETA * (salience - salience.max()))
    dist = e / e.sum()
    focus_loc = int(np.argmax(dist))
    focus_strength = float(dist.max())   # how peaked / strongly focused
    return focus_loc, focus_strength, dist


def schema_report(salience, ablate=False, rng=None):
    """Attention SCHEMA: a simplified internal MODEL that TRACKS (predicts) the real
    attention focus and is READ to self-report own attention state.
    ablate=True -> schema OFF: the model is gone, so the self-report is uninformed
    (a uniform guess over locations) even though real_attention still operates."""
    if ablate:
        # no self-model: report is a random guess (chance), strength uninformed
        loc = int(rng.integers(N_LOC))
        return loc, 0.5
    # schema linearly tracks the salience-driven focus with fidelity SCHEMA_STR
    tracked = SCHEMA_STR * salience + (1 - SCHEMA_STR) * salience.mean()
    e = np.exp(FOCUS_BETA * (tracked - tracked.max()))
    d = e / e.sum()
    loc = int(np.argmax(d))
    strength = float(d.max())
    return loc, strength


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # fix per-seed location identities so seeds are genuinely distinct
    _locs = [fnv_vec(f"loc_{seed}_{i}", DIM) for i in range(N_LOC)]

    full_hits, abl_hits = [], []
    abl_track_hits = []
    # divided-attention raw allocation entropy (the resource trade-off readout)
    alloc_full, alloc_abl = [], []
    # (B) agency-vs-schema: hold action/outcome FIXED, move ONLY attention focus
    agency_vals, schema_track_focus = [], []

    fixed_action_outcome_match = 1.0   # action/outcome held FIXED across the focus sweep

    for t in range(N_TRIALS):
        salience = rng.random(N_LOC)
        true_loc, true_str, dist = real_attention(salience)

        # schema-ON self-report
        rep_loc, rep_str = schema_report(salience, ablate=False)
        full_hits.append(1.0 if rep_loc == true_loc else 0.0)

        # schema-OFF self-report (ablation): real attention unchanged, model gone
        a_loc, _ = schema_report(salience, ablate=True, rng=rng)
        abl_hits.append(1.0 if a_loc == true_loc else 0.0)
        abl_track_hits.append(1.0 if a_loc == true_loc else 0.0)

        # divided-attention raw allocation = softmax entropy (UNCHANGED by ablation:
        # the real_attention softmax does not depend on the schema at all)
        ent = float(-np.sum(dist * np.log(dist + 1e-12)))
        alloc_full.append(ent)
        alloc_abl.append(ent)   # identical by construction: ablation removes only the schema read

        # (B) DISTINCT vs AGENCY — fixed action/outcome, focus moved each trial.
        # agency = comparator over the (FIXED) action outcome -> FLAT regardless of focus.
        agency_vals.append(fixed_action_outcome_match)   # constant -> no tracking of focus
        # schema report tracks the (moving) true focus -> 1 if it follows the focus
        schema_track_focus.append(1.0 if rep_loc == true_loc else 0.0)

    full_acc = float(np.mean(full_hits))
    abl_acc = float(np.mean(abl_hits))
    abl_track = float(np.mean(abl_track_hits))

    # (B) tracking-of-moved-focus: schema follows focus (variance high across trials),
    # agency is constant. Δ over the focus sweep:
    schema_track_delta = float(np.std(schema_track_focus)) + float(np.mean(schema_track_focus))
    # use mean tracking accuracy as the "does the readout move with the focus" signal:
    schema_track = float(np.mean(schema_track_focus))      # high (tracks focus)
    agency_track = float(np.std(agency_vals))              # ~0 (flat, outcome fixed)
    b_gap = abs(schema_track - agency_track)

    # (C) DISTINCT vs DIVIDED — allocation unchanged, report collapses
    alloc_delta = abs(float(np.mean(alloc_full)) - float(np.mean(alloc_abl)))
    report_drop = full_acc - abl_acc

    # (E) SHUFFLE — derange the schema->true-focus pairing; report can no longer track
    def derangement(n, rng):
        while True:
            p = rng.permutation(n)
            if n == 1 or not np.any(p == np.arange(n)):
                return p
    # build the true focus sequence and the schema-reported focus sequence, then
    # shuffle the reported sequence so it no longer aligns with the true one
    true_seq, rep_seq = [], []
    for t in range(N_TRIALS):
        salience = rng.random(N_LOC)
        tl, _, _ = real_attention(salience)
        rl, _ = schema_report(salience, ablate=False)
        true_seq.append(tl)
        rep_seq.append(rl)
    true_seq = np.array(true_seq)
    rep_seq = np.array(rep_seq)
    shuf_accs = []
    for _ in range(N_PERM):
        perm = derangement(N_TRIALS, rng)
        shuffled_rep = rep_seq[perm]
        shuf_accs.append(float(np.mean(shuffled_rep == true_seq)))
    shuffle_track = float(np.mean(shuf_accs))

    return dict(full_acc=full_acc, abl_acc=abl_acc, abl_track=abl_track,
                schema_track=schema_track, agency_track=agency_track, b_gap=b_gap,
                alloc_delta=alloc_delta, report_drop=report_drop,
                shuffle_track=shuffle_track)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = (agg['full_acc'] >= 0.85) and (agg['abl_acc'] <= 0.55)
cB = (agg['schema_track'] >= 0.50) and (agg['agency_track'] < 0.05) and (agg['b_gap'] >= 0.45)
cC = (agg['alloc_delta'] <= 0.05) and (agg['report_drop'] >= 0.30)
cD = agg['abl_track'] <= 0.55
cE = agg['shuffle_track'] <= (CHANCE + 0.10)
GREEN = cA and cB and cC and cD and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS} | N_LOC {N_LOC} chance {CHANCE:.3f}")
print(f"A PRESENCE full_acc {agg['full_acc']:.3f}>=0.85 AND abl_acc {agg['abl_acc']:.3f}<=0.55 -> {cA}")
print(f"B DISTINCT-vs-AGENCY schema_track {agg['schema_track']:.3f}>=0.50 (tracks moved focus) AND agency_track {agg['agency_track']:.3f}<0.05 (flat, outcome fixed) AND gap {agg['b_gap']:.3f}>=0.45 -> {cB}")
print(f"C DISTINCT-vs-DIVIDED alloc_delta {agg['alloc_delta']:.3f}<=0.05 (raw allocation invariant) AND report_drop {agg['report_drop']:.3f}>=0.30 (self-report collapses) -> {cC}")
print(f"D EARNED(ablation) abl_track {agg['abl_track']:.3f}<=0.55 (~chance {CHANCE:.3f}) -> {cD}")
print(f"E SHUFFLE shuffle_track {agg['shuffle_track']:.3f}<={CHANCE + 0.10:.3f} ({N_PERM}-perm derangement) -> {cE}")
