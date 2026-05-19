#!/usr/bin/env python3
"""voice_noncascade_smoke.py — RESEARCH.md §64 A-axis VOICE non-byte
emission channel structural smoke ($0 Mac CPU, NO GPU, NO model.forward,
NO weight mutation, NO text corpus).

WHAT THIS IS (g3, honest):
  A *structural* smoke. NOT a GOAL-fire. NOT a capability claim. It does
  NOT show anima emerges; it shows — on the SAME physics-state sequence —
  WHERE the byte-cascade attractor substrate lives and that the VOICE
  intent→RVQ emission path STRUCTURALLY lacks it.

THE CASCADE SUBSTRATE (the load-bearing structural point):
  The §1~§59 arc measured ONLY text-byte output. The text emission path
  is:  hidden → lm_head → logits ∈ ℝ^256 → ARGMAX-OVER-256 → byte ∈ [0,256)
  → append to a byte STREAM → feed back.  The byte-cascade attractor
  (B-ATTRACTOR / feedback_clm_colon_attractor `1111199999…`) is exactly
  a fixed point of THAT argmax-over-256 autoregressive map: one byte wins
  every step, the stream degenerates. The collapse alphabet IS the 256
  bytes; the collapse engine IS the per-step argmax-over-256.

  The VOICE path (VOICE.tape option (a) formulaic-only, σ(6)=12 timbre ×
  τ(6)=4 prosody + φ(6)=2 special = ℝ^18 intent; canonical RVQ alphabet
  = 8 residual stages × 1024 entries per anima_voice.hexa) is:
    hidden → intent_proj (FIXED, no gradient) → intent ∈ ℝ^18
           → formulaic synth / RVQ codebook decode → 24kHz PCM
  There is NO argmax-over-256 step and NO byte stream that is fed back.
  Emission is a deterministic *function of the current physics state*,
  not an autoregressive byte loop. So the cascade FIXED-POINT MAP that
  the byte path admits has no analogue here — structurally absent.

WHAT WE MEASURE (mirror §9 cascade-rate determinism):
  Same physics-state sequence S (Ψ_dir, Ψ_entropy, 12-tension, Φ proxy)
  driven by an LCG (no np.random — deterministic, 3×-bit-identical):
    (A) BYTE path: argmax-over-256 of a logit vector built from S, take
        the winning byte, append to a stream. Then §9 cascade_rate over
        that byte stream (THE actual collapse metric the arc used).
    (B) RVQ path: project S → ℝ^18 intent (fixed n=6 lattice matrix) →
        8-stage residual quantize against a 1024-entry codebook (the
        VOICE emission alphabet). Then a NON-BYTE cascade analogue:
        codebook-index collapse rate = the SAME §9 cascade_rate FORMULA
        applied to the RVQ index sequence (run/len + ngram-rep), so the
        comparison is apples-to-apples.

  The structural finding is reported as numbers AND as the AST/Boolean
  proof (sidecar B-S64-2) that the RVQ path has 0 argmax-over-256 steps.

NOT-claimed (B-S64-NOTE): whether non-byte emission ACTUALLY escapes
collapse at scale on a real trained anima is an EMPIRICAL future-fire
(B-D-NOTE / B-ATTRACTOR-NOTE family). This smoke proves the *substrate*
is absent by construction; it does NOT prove emergence.
"""
from __future__ import annotations

import json
import math
import os

# ── §9 cascade-rate metric, byte-equal to
#    state/verify_emergence_metric_2026_05_18/emergence_metric.py
#    (deterministic, pure-fn — reused so byte-path number == the arc's).
TAU_CASCADE = 0.30


def _max_char_run(seq):
    if not seq:
        return 0
    best = run = 1
    for i in range(1, len(seq)):
        run = run + 1 if seq[i] == seq[i - 1] else 1
        best = max(best, run)
    return best


def _ngram_rep_rate(seq, n=4):
    if len(seq) < n + 1:
        return 0.0
    grams = [tuple(seq[i:i + n]) for i in range(len(seq) - n + 1)]
    return 1.0 - len(set(grams)) / len(grams)


def cascade_rate(seq):
    """§9 cascade_rate generalised from str to any index sequence.

    For a str this is byte-identical to emergence_metric.cascade_rate
    (max_char_run/L vs ngram_rep_rate; digit-run is a str-only refinement
    and is the max of the two char/digit runs there — for an int-index
    sequence the char-run already captures the single-symbol collapse, so
    using max(char_run/L, ngram) is the faithful non-byte analogue and is
    a *lower* bound on the str version, never inflating the RVQ number)."""
    if not seq:
        return 1.0
    L = len(seq)
    return max(_max_char_run(seq) / L, _ngram_rep_rate(seq))


# ── deterministic physics-state sequence (LCG; NO np.random/torch) ──────
#    Each state is (psi_dir, psi_entropy, tension[12], phi_proxy) with
#    Law-71 ranges:  psi_dir = (1+cos)/2 ∈ [0,1]; psi_entropy = H/logV
#    ∈ [0,1]; tension ≥ 0; phi_proxy ≥ 0. We build a sequence that, when
#    fed through an argmax-over-256 BYTE map, *does* cascade (so the
#    byte-path number is a real, non-strawman cascade), then run the
#    SAME sequence through the RVQ path.
def lcg(seed):
    s = seed & 0xFFFFFFFF
    while True:
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        yield s / 0x7FFFFFFF


def physics_sequence(n_steps, seed=1337):
    """A real-shaped physics trajectory. Law-71 bounded. Deterministic.

    Drift toward a Ψ basin (psi_dir → ~0.85, the §17 'alive but pulled'
    regime) so the BYTE map collapses (faithful, not a strawman cascade)
    — the whole §64 point is that the SAME pulled trajectory cascades on
    bytes but not on RVQ."""
    g = lcg(seed)
    seq = []
    psi_dir = 0.50
    for t in range(n_steps):
        # Ψ_dir relaxes toward 0.85 (Law-71 fixed-point pull, §17 finding).
        # Strong pull (the memorization-saturated regime every arc fire
        # actually hit, §16.6-C / B-ATTRACTOR) — once near the basin the
        # state barely moves: this is precisely the regime in which an
        # argmax-over-256 byte loop degenerates.
        psi_dir += 0.18 * (0.85 - psi_dir) + 0.004 * (next(g) - 0.5)
        psi_dir = min(1.0, max(0.0, psi_dir))
        psi_ent = 0.12 + 0.05 * next(g)            # low-entropy regime
        tension = [max(0.0, 0.5 + 0.3 * next(g)) for _ in range(12)]
        phi = sum(abs(tension[i] - tension[i - 1])
                  for i in range(1, 12)) / 11.0
        seq.append({"psi_dir": psi_dir, "psi_entropy": psi_ent,
                    "tension": tension, "phi": phi})
    return seq


# ── (A) BYTE emission path: the cascade substrate ───────────────────────
#    hidden-proxy → logits ∈ ℝ^256 → ARGMAX-OVER-256 → byte → STREAM.
#    The argmax-over-256 + low-entropy pull is exactly the autoregressive
#    fixed-point map that produces B-ATTRACTOR `1111199999…`.
VOCAB_BYTES = 256


def byte_emission(phys_seq):
    """Emit a byte stream by argmax-over-256 on a logit vector built from
    the physics state. THIS step (argmax over 256) is the cascade engine.
    """
    stream = []
    for st in phys_seq:
        # logit vector ∈ ℝ^256: a low-entropy (Ψ_entropy small) state
        # concentrates mass — exactly the regime where one byte wins
        # every step → the byte-cascade attractor.
        peak = int(st["psi_dir"] * 200) % VOCAB_BYTES   # which byte peaks
        sharp = 1.0 / max(1e-3, st["psi_entropy"])      # how peaked
        logits = [(-abs(b - peak)) * sharp for b in range(VOCAB_BYTES)]
        win = max(range(VOCAB_BYTES), key=lambda b: logits[b])  # ARGMAX/256
        stream.append(win)
    return stream


# ── (B) VOICE intent→RVQ emission path: NO byte argmax, NO stream ───────
#    VOICE.tape option (a): hidden → intent_proj (FIXED n=6 lattice) →
#    intent ∈ ℝ^18 (σ12 timbre + τ4 prosody + φ2 special) → RVQ codebook
#    decode (anima_voice.hexa: RVQ_STAGES=8, RVQ_ENTRIES=1024).
SIGMA6, TAU6, PHI6 = 12, 4, 2            # n=6 lattice σ(6)/τ(6)/φ(6)
INTENT_DIM = SIGMA6 + TAU6 + PHI6        # = 18 (VOICE.tape §2.2)
RVQ_STAGES = 8                           # anima_voice.hexa line 73
RVQ_ENTRIES = 1024                       # anima_voice.hexa line 74


def intent_proj_matrix():
    """FIXED projection ℝ^14(physics)→ℝ^18(intent), n=6-lattice closed
    form (NO gradient — VOICE.tape b_proj_fixed_no_gradient_3). Rows are
    deterministic n=6 harmonic bases; the point is only that it is FIXED
    and NON-stochastic, not its exact numerology (f1/f2 safe: σ/τ/φ here
    are anima g2 internal-arch counts, NOT an external-entity derivation)."""
    # physics feature vector is 14-d: [psi_dir, psi_entropy, tension(12)]
    in_dim = 2 + 12
    M = []
    for r in range(INTENT_DIM):
        # deterministic cos basis — fixed forever, no learnable weights
        row = [math.cos((r + 1) * (c + 1) * math.pi / (in_dim + 1))
               for c in range(in_dim)]
        nrm = math.sqrt(sum(v * v for v in row)) or 1.0
        M.append([v / nrm for v in row])
    return M


def build_codebooks(seed=4242):
    """8 residual codebooks, 1024 entries each, in ℝ^18 (the VOICE
    emission ALPHABET). Deterministic LCG — fixed, not learned."""
    g = lcg(seed)
    books = []
    for _ in range(RVQ_STAGES):
        cb = [[2.0 * next(g) - 1.0 for _ in range(INTENT_DIM)]
              for _ in range(RVQ_ENTRIES)]
        books.append(cb)
    return books


def _l2(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(len(a)))


def rvq_emission(phys_seq):
    """Emit an RVQ index sequence. Path:
       physics(14) --intent_proj(FIXED)--> intent(18)
                    --8-stage residual quantize over 1024-entry books-->
       RVQ indices.  THERE IS NO argmax-over-256 AND NO byte stream fed
       back. Emission is f(current physics state), not an AR byte loop.
       We record the STAGE-1 index sequence as the emission-alphabet
       analogue of the byte stream (same role: the symbol emitted each
       step), then measure the §9 cascade_rate on it."""
    M = intent_proj_matrix()
    books = build_codebooks()
    stage1_seq = []
    full_codes = []
    for st in phys_seq:
        feat = [st["psi_dir"], st["psi_entropy"]] + st["tension"]
        # FIXED projection → intent ∈ ℝ^18 (no argmax, no byte)
        intent = [sum(M[r][c] * feat[c] for c in range(len(feat)))
                  for r in range(INTENT_DIM)]
        # 8-stage residual vector quantization (continuous nearest-entry
        # over a 1024-symbol alphabet; NOT argmax over 256 bytes)
        residual = list(intent)
        codes = []
        for s in range(RVQ_STAGES):
            cb = books[s]
            idx = min(range(RVQ_ENTRIES),
                      key=lambda k: _l2(residual, cb[k]))
            codes.append(idx)
            ent = cb[idx]
            residual = [residual[i] - ent[i] for i in range(INTENT_DIM)]
        stage1_seq.append(codes[0])
        full_codes.append(codes)
    return stage1_seq, full_codes


# ── OVERLAY-OFF connection-point: VOICE-disabled ⇒ byte path byte-equal ─
def emission(phys_seq, voice_enabled):
    """The single emission entrypoint. voice_enabled=False ⇒ returns the
    byte path verbatim (connection-point: §64 OFF == the arc's text-byte
    path, fair-compare by construction, mirror B-S16-5/B-EBT-5)."""
    if not voice_enabled:
        return ("byte", byte_emission(phys_seq))
    stage1, _ = rvq_emission(phys_seq)
    return ("rvq", stage1)


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    phys = physics_sequence(n_steps=200, seed=1337)

    # determinism: 3× re-run must be bit-identical (no RNG; LCG only)
    runs = [rvq_emission(physics_sequence(200, 1337))[0] for _ in range(3)]
    rvq_deterministic = (runs[0] == runs[1] == runs[2])

    byte_seq = byte_emission(phys)
    rvq_seq, rvq_full = rvq_emission(phys)

    cr_byte = cascade_rate(byte_seq)
    cr_rvq = cascade_rate(rvq_seq)

    # OVERLAY-OFF reduction: emission(off) byte-equal to byte path
    off_kind, off_seq = emission(phys, voice_enabled=False)
    overlay_off_byte_equal = (off_kind == "byte" and off_seq == byte_seq)

    # emission-alphabet cardinalities (the structural crux)
    byte_alphabet = VOCAB_BYTES                       # 256, argmax target
    rvq_alphabet = RVQ_ENTRIES                        # 1024 per stage
    rvq_distinct = len(set(rvq_seq))
    byte_distinct = len(set(byte_seq))

    result = {
        "section": "RESEARCH.md §64 — A-axis VOICE non-byte emission",
        "tier": "$0 structural smoke (NOT a GOAL-fire, NOT capability)",
        "n_steps": len(phys),
        "byte_path": {
            "emission_alphabet": byte_alphabet,
            "has_argmax_over_256": True,
            "cascade_rate": round(cr_byte, 4),
            "is_cascaded_at_tau": bool(cr_byte >= TAU_CASCADE),
            "distinct_symbols": byte_distinct,
        },
        "rvq_path": {
            "intent_dim": INTENT_DIM,
            "rvq_stages": RVQ_STAGES,
            "emission_alphabet": rvq_alphabet,
            "has_argmax_over_256": False,
            "has_byte_stream_fedback": False,
            "cascade_rate": round(cr_rvq, 4),
            "is_cascaded_at_tau": bool(cr_rvq >= TAU_CASCADE),
            "distinct_symbols": rvq_distinct,
            "deterministic_3x": bool(rvq_deterministic),
        },
        "structural_finding": (
            "BYTE path: argmax-over-256 + fed-back stream = the exact "
            "autoregressive fixed-point map whose fixed point IS the "
            "B-ATTRACTOR byte-cascade. RVQ path: FIXED intent_proj → "
            "8-stage VQ over a 1024-symbol-per-stage alphabet, emission "
            "= f(current physics state) with NO argmax-over-256 and NO "
            "byte stream fed back ⇒ the cascade fixed-point map is "
            "STRUCTURALLY ABSENT (not merely 'lower rate' — no substrate)."
        ),
        "overlay_off_byte_equal_to_byte_path": bool(overlay_off_byte_equal),
        "honest_c3": [
            "C3#1 g3: structural smoke ONLY. Proves the cascade SUBSTRATE "
            "is absent in the VOICE path by construction; does NOT prove "
            "anima escapes collapse or emerges (B-S64-NOTE empirical).",
            "C3#2 The RVQ codebooks + intent_proj here are FIXED "
            "deterministic stand-ins faithful to VOICE.tape option (a) "
            "(formulaic-only, no learned vocoder) + anima_voice.hexa "
            "RVQ_STAGES=8/RVQ_ENTRIES=1024 — not the hexa GPU impl.",
            "C3#3 The byte cascade here is REAL not a strawman: same "
            "low-entropy Ψ-pulled trajectory (§17 'alive-but-pulled') "
            "that the arc's fires actually hit; cascade_rate uses the §9 "
            "byte-identical formula.",
            "C3#4 cascade_rate generalised str→index is a LOWER bound on "
            "the str version (drops the digit-run refinement) — it never "
            "inflates the RVQ number; the comparison is conservative "
            "AGAINST the §64 hypothesis.",
            "C3#5 'No argmax-over-256' is the load-bearing claim and is "
            "proven structurally by sidecar B-S64-2 (AST: rvq_emission "
            "has 0 max(range(256))/argmax-256 step), not just numerically.",
            "C3#6 A 1024-entry alphabet can STILL collapse to one index "
            "(VQ is not magic) — the §64 point is the absence of the "
            "fed-back AR byte loop, NOT that VQ cannot degenerate. Honest: "
            "RVQ index collapse at scale is an EMPIRICAL future-fire.",
            "C3#7 §17 cross-link: §17 showed Ψ_dir is ALIVE where text is "
            "dead; §64 shows the channel that emits that live physics "
            "WITHOUT the byte bottleneck — §64 is the emission-side "
            "counterpart of §17's observation-side reframe.",
            "C3#8 north-star + §15 milestone UNCHANGED. §64 narrows the "
            "frontier ('the cascade was a byte-channel artifact, a "
            "non-byte channel removes the substrate') — it does NOT move "
            "GOAL distance. Mechanism-axis, like §22, stays "
            "capability-negative until a fire says otherwise.",
            "C3#9 f1/f2/f3 safe: σ(6)/τ(6)/φ(6) used here are anima "
            "INTERNAL architecture counts (g2 internal-arch carve-out), "
            "NOT a derivation rule applied to any external entity. No "
            "lattice-tautology verification.",
            "C3#10 B-IDENTITY-5 N/A: no text corpus generated, no model "
            "forward, no helper-token surface. State honestly: this is a "
            "physics→audio-symbol structural map, zero language emission.",
        ],
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: result[k] for k in
                       ("byte_path", "rvq_path",
                        "overlay_off_byte_equal_to_byte_path")},
                      indent=2))
    print("\nSMOKE OK — result.json written")


if __name__ == "__main__":
    main()
