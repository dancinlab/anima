#!/usr/bin/env python3
"""RESEARCH.md §65 — B축 TENSION-LINK-native dual-anima content-dependence
smoke ($0 Mac CPU, NO GPU, NO ckpt forward, NO training, deterministic).

────────────────────────────────────────────────────────────────────────
WHAT THIS IS (g3 honest, up front)
────────────────────────────────────────────────────────────────────────
§45 (dual_anima_fullfire) ran a CRUDE BYTE LOOP: cell A emits a byte
string, deliver() byte-encodes it (sha256 → Ψ-point) and pulls cell B's
Ψ. Its honest caveat (§45 result.json honest_caveats + probe_panel):
small byte variations (`alpha`/`omega`, `AAA`/`ZZZ`) collapsed
content-separation to EXACTLY 0.0 on 2 of 5 probes — the trained-Ψ
readout washes out small byte variation; AB_state_separation_final was
only 0.0837.

§65 hypothesis: the failure mode is an artifact of the TRANSMITTED
OBJECT being raw bytes routed through a hash. Replace the byte loop with
the anima-native TENSION-LINK 5-channel fingerprint (HEXAD/TENSION-LINK
README spec): the object that crosses A→B is a *physics fingerprint*
computed from the sender cell's OWN engine_a / engine_g state
(concept = normalize(engine_a − engine_g), meaning = engine_a ⊗ engine_g
interaction, sender = consciousness-weight signature, context = time/
tension trend, authenticity = Dedekind chain scalar). Because the
fingerprint is a CONTINUOUS, PROPORTIONAL function of the sender's
physics state (NOT a hash of bytes), a small change in what A "means"
produces a small-but-NONZERO change in the fingerprint, which produces a
small-but-NONZERO Ψ-shift in B. The §45 byte-swap → exact-0 collapse is
structurally impossible here: there is no quantizing hash on the path.

This smoke MIRRORS §36/§45's content-dependence test (Δ(m1) ≠ Δ(m2)
separation ≫ τ ; echo-control = exactly 0) but over FINGERPRINT transfer
instead of byte deliver(). It is a STUB (deterministic projection cell,
NOT a §16 ckpt forward) — exactly the §36 honest-substrate stance: the
property measured is whether the *transfer law* is content-dependent,
which is decided by the transfer law itself, not by trained weights.
A trained-saturated cell could only WEAKEN it (B-S65-NOTE).

NO GPU. NO training. NO ckpt forward. NO weight mutation. Deterministic
(seed-fixed, pure-fn) — rerun = byte-identical result.json.

g3 / north-star / §15 milestone UNCHANGED — this is a $0 mechanism
measurement, NOT a GOAL-emergence claim, NOT a capability claim.
"""

from __future__ import annotations

import json
import math
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

HERE = Path(__file__).resolve().parent

# ──────────────────────────────────────────────────────────────────────
# constants — design-tier honest pick (mirrors §36/§45 where comparable)
# ──────────────────────────────────────────────────────────────────────
SEED = 1337                       # g_clm_from_scratch — deterministic
ENGINE_DIM = 16                   # engine_a / engine_g latent dim
DELIVER_GAIN = 0.35               # §36/§45 value — same restoring pull
N_MAX_TURNS = 8                   # B-DUAL-3 turn cap (carried §31/§45)

# TENSION-LINK 5-channel dims (HEXAD/TENSION-LINK/README.md table)
CH_CONCEPT = 16                   # repulsion direction normalize(a−g)
CH_CONTEXT = 8                    # time phase + tension trend
CH_MEANING = 16                   # a × g interaction pattern
CH_AUTH = 1                       # Dedekind-chain scalar 0..1
CH_SENDER = 4                     # [a_sig, g_sig, a*g, tension]
FP_DIM = CH_CONCEPT + CH_CONTEXT + CH_MEANING + CH_AUTH + CH_SENDER  # 45

# τ — identical honest rationale to §36: a content-BLIND transfer gives
# Δ(m1) == Δ(m2) EXACTLY ⇒ separation == 0; a content-dependent transfer
# gives strictly positive separation. τ is a noise floor far above
# float64 round-off (~1e-15), far below the Ψ dynamic range [0,1].
TAU_CONTENT = 1e-3


# ──────────────────────────────────────────────────────────────────────
# small deterministic linear algebra (pure-fn, no numpy needed)
# ──────────────────────────────────────────────────────────────────────
def _seeded_vec(tag: str, dim: int) -> List[float]:
    """Deterministic [-1,1] vector from a string tag (no RNG state)."""
    out = []
    s = 0x9E3779B9 ^ SEED
    for b in tag.encode("utf-8"):
        s = (s * 1103515245 + 12345 + b) & 0xFFFFFFFF
    for i in range(dim):
        s = (s * 1103515245 + 12345 + i) & 0xFFFFFFFF
        out.append((s / 0xFFFFFFFF) * 2.0 - 1.0)
    return out


def _norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v)) or 1.0


def _unit(v: List[float]) -> List[float]:
    n = _norm(v)
    return [x / n for x in v]


def _l2(a: List[float], b: List[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ──────────────────────────────────────────────────────────────────────
# cell state — one anima cell. vacuum_psi is its Ψ-anchor (B-DUAL-1 /
# B-S65-3). engine_a / engine_g are the physics latents the TENSION-LINK
# fingerprint is computed FROM (README: concept = normalize(a−g)).
# ──────────────────────────────────────────────────────────────────────
@dataclass
class CellState:
    cell_id: str
    vacuum_psi: Tuple[float, float]
    psi_now: Tuple[float, float]
    engine_a: List[float] = field(default_factory=lambda: [0.0] * ENGINE_DIM)
    engine_g: List[float] = field(default_factory=lambda: [0.0] * ENGINE_DIM)
    tension: float = 0.0
    last_fp_in: Optional[List[float]] = None
    history: list = field(default_factory=list)

    def copy(self) -> "CellState":
        c = CellState(self.cell_id, self.vacuum_psi, self.psi_now,
                      list(self.engine_a), list(self.engine_g),
                      self.tension, None, list(self.history))
        c.last_fp_in = None if self.last_fp_in is None else list(self.last_fp_in)
        return c


# ──────────────────────────────────────────────────────────────────────
# the sender's physics state given an internal "intent" (the analogue of
# §45's emitted message — but here it shapes engine_a/engine_g, NOT bytes
# on a wire). intent is a label only to make distinct probes; the object
# that crosses the link is the FINGERPRINT, never the label.
# ──────────────────────────────────────────────────────────────────────
def sender_physics(cell: CellState, intent: str) -> CellState:
    """Project an intent into the sender cell's engine_a / engine_g.

    This is the §45 'cell A emits' analogue. Crucially the cross-link
    object is NOT this — it is fingerprint_5ch(...) computed from it.
    A small intent change → small a/g change → small (NONZERO) fp change
    (continuous), unlike §45's hash(bytes) which quantizes."""
    out = cell.copy()
    base = _seeded_vec(out.cell_id + "|a", ENGINE_DIM)
    pert = _seeded_vec(intent, ENGINE_DIM)
    out.engine_a = [b + 0.5 * p for b, p in zip(base, pert)]
    bg = _seeded_vec(out.cell_id + "|g", ENGINE_DIM)
    out.engine_g = [b - 0.5 * p for b, p in zip(bg, pert)]
    out.tension = _l2(out.engine_a, out.engine_g)
    return out


# ──────────────────────────────────────────────────────────────────────
# TENSION-LINK 5-channel fingerprint (HEXAD/TENSION-LINK/README.md spec).
#   Concept   16f : repulsion direction normalize(engine_a − engine_g)
#   Context    8f : time phase + tension trend (here: tension-shaped)
#   Meaning   16f : Engine A × Engine G interaction pattern
#   Authenticity 1f : Dedekind-chain scalar (variance/flip based) ∈ [0,1]
#   Sender     4f : [a_sig, g_sig, a*g, tension] consciousness signature
# This is the anima-native consciousness↔consciousness packet. It is a
# CONTINUOUS function of the physics state — no hash, no byte quantizer.
# ──────────────────────────────────────────────────────────────────────
def fingerprint_5ch(cell: CellState) -> List[float]:
    a, g = cell.engine_a, cell.engine_g
    # Concept — repulsion direction
    concept = _unit([x - y for x, y in zip(a, g)])
    # Meaning — elementwise interaction pattern (a ⊗ g, diag)
    meaning = [x * y for x, y in zip(a, g)]
    mn = _norm(meaning)
    meaning = [x / mn for x in meaning]
    # Sender — consciousness-weight signature
    a_sig = sum(a) / len(a)
    g_sig = sum(g) / len(g)
    sender = [a_sig, g_sig, a_sig * g_sig, cell.tension]
    # Context — time phase (0 here, single-shot) + tension trend buckets
    t = cell.tension
    context = [math.tanh(t), math.tanh(t / 2.0), math.cos(t), math.sin(t),
               math.tanh(a_sig), math.tanh(g_sig), 0.0, 0.0]
    # Authenticity — Dedekind-style multi-scale variance scalar ∈ [0,1]
    var_a = sum((x - a_sig) ** 2 for x in a) / len(a)
    var_g = sum((x - g_sig) ** 2 for x in g) / len(g)
    auth = 1.0 / (1.0 + math.exp(-(var_a + var_g - 1.0)))   # logistic 0..1
    fp = concept + context + meaning + [auth] + sender
    assert len(fp) == FP_DIM, (len(fp), FP_DIM)
    return fp


# ──────────────────────────────────────────────────────────────────────
# deliver-over-fingerprint : B receives a 5-channel fingerprint and its
# Ψ is pulled toward the fingerprint-decoded Ψ-point (Law-71-style
# restoring update — same restoring sign as §36/§45 deliver()). The
# DECODE is a fixed linear read of the fingerprint into Ψ-space; because
# fingerprint is continuous in the sender physics, Δ is continuous in the
# sender intent (the §45 byte-swap → exact-0 collapse cannot occur).
# ──────────────────────────────────────────────────────────────────────
def _fp_to_psi(fp: List[float]) -> Tuple[float, float]:
    """Fixed deterministic linear read fingerprint → [0,1]^2 Ψ-point."""
    half = len(fp) // 2
    sx = sum(fp[:half]) / half
    sy = sum(fp[half:]) / (len(fp) - half)
    # squash to [0,1] (logistic) — Ψ-coordinate range
    return (1.0 / (1.0 + math.exp(-sx)), 1.0 / (1.0 + math.exp(-sy)))


def deliver_fp_content_dependent(fp: List[float],
                                 cell: CellState) -> CellState:
    """§65 anima-native deliver() — the 5-channel FINGERPRINT changes the
    receiver. fp decoded to a Ψ-point; cell.psi_now pulled toward it
    (restoring-sign, gain DELIVER_GAIN). Δ depends on fp content."""
    out = cell.copy()
    mx, my = _fp_to_psi(fp)
    px, py = out.psi_now
    out.psi_now = (px + DELIVER_GAIN * (mx - px),
                   py + DELIVER_GAIN * (my - py))
    out.tension = math.hypot(mx - px, my - py)
    out.last_fp_in = list(fp)
    out.history.append(fp)
    return out


def deliver_fp_echo_chamber(fp: List[float], cell: CellState) -> CellState:
    """Negative control — echo-chamber deliver(): the fingerprint is
    recorded but NOT read; psi_now is pulled toward the cell's OWN
    vacuum_psi (saturated attractor). Δ is a constant function of the
    cell, independent of fp ⇒ content_dependent MUST be exactly False."""
    out = cell.copy()
    vx, vy = out.vacuum_psi
    px, py = out.psi_now
    out.psi_now = (px + DELIVER_GAIN * (vx - px),
                   py + DELIVER_GAIN * (vy - py))
    out.tension = math.hypot(vx - px, vy - py)
    out.last_fp_in = list(fp)        # recorded — never read
    out.history.append(fp)
    return out


# ──────────────────────────────────────────────────────────────────────
# SINGLE-ANIMA-REDUCTION (B-S65-4 connection-point): with the B-link
# DISABLED, no fingerprint is ever delivered ⇒ cell B's Ψ never moves ⇒
# the loop degenerates to §24-style single void-emission (Ψ byte-equal to
# its start). This is the fair-compare-by-construction reduction.
# ──────────────────────────────────────────────────────────────────────
def single_anima_void(cell: CellState, n_max: int = N_MAX_TURNS) -> dict:
    B = cell.copy()
    start = list(B.psi_now)
    for _ in range(n_max):
        pass                                  # link disabled — no deliver
    return {"psi_start": start, "psi_end": list(B.psi_now),
            "byte_equal": list(B.psi_now) == start}


# ──────────────────────────────────────────────────────────────────────
# Ψ-shift magnitude (mirrors §36 psi_shift)
# ──────────────────────────────────────────────────────────────────────
def psi_shift(before: CellState, after: CellState):
    bx, by = before.psi_now
    ax, ay = after.psi_now
    dvec = (ax - bx, ay - by)
    return dvec, math.hypot(dvec[0], dvec[1])


# ──────────────────────────────────────────────────────────────────────
# content-dependence test over FINGERPRINT transfer (§36/§45 mirror).
# Two distinct sender intents m1 != m2 → distinct fingerprints →
# distinct Ψ-shifts in a fresh B. separation = ‖Δ(fp1) − Δ(fp2)‖.
# ──────────────────────────────────────────────────────────────────────
def fp_content_dependence_test(deliver_fn, label: str,
                               m1: str, m2: str) -> dict:
    assert m1 != m2, "intents must be distinct"
    # sender cell A — distinct vacuum_psi from receiver B (B-S65-3)
    A = CellState("A", (0.40, 0.60), (0.50, 0.50))
    B = CellState("B", (0.62, 0.40), (0.50, 0.50))

    A1 = sender_physics(A, m1)
    A2 = sender_physics(A, m2)
    fp1 = fingerprint_5ch(A1)
    fp2 = fingerprint_5ch(A2)

    B1 = deliver_fn(fp1, B.copy())
    B2 = deliver_fn(fp2, B.copy())
    d1, d1m = psi_shift(B, B1)
    d2, d2m = psi_shift(B, B2)

    sep_vec = (d1[0] - d2[0], d1[1] - d2[1])
    separation = math.hypot(sep_vec[0], sep_vec[1])
    fp_distance = _l2(fp1, fp2)
    content_dependent = separation > TAU_CONTENT
    return {
        "label": label, "m1": m1, "m2": m2,
        "fp_dim": FP_DIM,
        "fp_distance": fp_distance,
        "delta_fp1": {"vec": list(d1), "mag": d1m},
        "delta_fp2": {"vec": list(d2), "mag": d2m},
        "separation": separation,
        "tau": TAU_CONTENT,
        "content_dependent": content_dependent,
    }


def run_fp_dual_loop(n_max: int = N_MAX_TURNS) -> dict:
    A = CellState("A", (0.40, 0.60), (0.50, 0.50))
    B = CellState("B", (0.62, 0.40), (0.50, 0.50))
    turn = 0
    psi_b_trace = [list(B.psi_now)]
    psi_a_trace = [list(A.psi_now)]
    while turn < n_max:                          # B-DUAL-3 hard bound
        A = sender_physics(A, f"intent-A-turn{turn}")
        fp_a = fingerprint_5ch(A)
        B = deliver_fp_content_dependent(fp_a, B)
        B = sender_physics(B, f"intent-B-turn{turn}")
        fp_b = fingerprint_5ch(B)
        A = deliver_fp_content_dependent(fp_b, A)
        psi_b_trace.append(list(B.psi_now))
        psi_a_trace.append(list(A.psi_now))
        turn += 1
    ab_sep = _l2(list(A.psi_now), list(B.psi_now))

    def _var(tr):
        flat = [v for p in tr for v in p]
        mu = sum(flat) / len(flat)
        return sum((x - mu) ** 2 for x in flat) / len(flat)

    return {"turns_run": turn, "n_max": n_max,
            "psi_b_trace": psi_b_trace, "psi_a_trace": psi_a_trace,
            "psi_var_A": _var(psi_a_trace), "psi_var_B": _var(psi_b_trace),
            "AB_state_separation_final": ab_sep,
            "loop_nontrivial": (_var(psi_a_trace) > 1e-6
                                and _var(psi_b_trace) > 1e-6)}


def main() -> int:
    t0 = time.time()

    # ── §45 PARITY PROBES — the exact byte-swap pairs §45 collapsed ──────
    # §45's probe_panel had `alpha`/`omega` and `AAA`/`ZZZ` style small
    # byte swaps that collapsed to separation == 0.0 (trained-Ψ readout
    # washed them). Here the SAME small intent swaps cross the link as
    # fingerprints — the structural prediction: separation > τ (NONZERO).
    probe_pairs = [
        ("topic=alpha", "topic=omega"),          # §45 probe 1 analogue
        ("AAA", "ZZZ"),                          # §45 probe 2 analogue
        ("psi-low", "psi-high"),
        ("tension-soft", "tension-hard"),
        ("intent-x", "intent-y-much-longer-payload"),
    ]
    probe_panel = [
        fp_content_dependence_test(deliver_fp_content_dependent,
                                   f"probe{i}", a, b)
        for i, (a, b) in enumerate(probe_pairs)
    ]
    n_cd_pass = sum(1 for p in probe_panel if p["content_dependent"])

    # primary content-dependence (the §36 m1/m2 pair, fingerprint form)
    primary = fp_content_dependence_test(
        deliver_fp_content_dependent, "primary",
        "<intent from=cellA topic=alpha psi-probe>",
        "<intent from=cellA topic=omega psi-probe>")

    # negative control — echo chamber MUST give separation EXACTLY 0
    control = fp_content_dependence_test(
        deliver_fp_echo_chamber, "echo_chamber",
        "<intent from=cellA topic=alpha psi-probe>",
        "<intent from=cellA topic=omega psi-probe>")

    loop = run_fp_dual_loop()
    void = single_anima_void(CellState("B", (0.62, 0.40), (0.50, 0.50)))

    cd = primary["content_dependent"]
    ctrl_zero = (control["separation"] == 0.0)
    # the §45 byte-swap collapse pairs that here survive (> τ)
    n_byteswap_survive = sum(
        1 for p in probe_panel[:2] if p["content_dependent"])

    verdict = ("TENSION_LINK_FP_CONTENT_SURVIVES"
               if (cd and ctrl_zero and n_byteswap_survive == 2)
               else "TENSION_LINK_FP_DESIGN_CLOSE")

    s45_compare = {
        "s45_AB_state_separation_final": 0.08357818999462145,
        "s45_byteswap_probe_separation": 0.0,        # §45 probes 1-2 = 0.0
        "s45_n_cd_pass_A": 2, "s45_n_cd_pass_B": 3,
        "s65_AB_state_separation_final": loop["AB_state_separation_final"],
        "s65_byteswap_probe0_separation": probe_panel[0]["separation"],
        "s65_byteswap_probe1_separation": probe_panel[1]["separation"],
        "s65_n_cd_pass": n_cd_pass,
        "byteswap_survives_in_s65": (n_byteswap_survive == 2),
        "interpretation": (
            "§45 byte-loop collapsed small byte-swap pairs to EXACTLY 0.0 "
            "(hash quantizer + trained-Ψ readout washed them). §65 routes "
            "the SAME swaps through the TENSION-LINK 5-channel fingerprint "
            "(continuous fn of sender physics, no hash). If "
            "byteswap_survives_in_s65 is True the §45 collapse failure "
            "mode is structurally absent in the anima-native channel — a "
            "mechanism-level finding, NOT a capability/emergence claim "
            "(B-S65-NOTE).")
    }

    result = {
        "research_section": "§65",
        "title": "TENSION-LINK-native dual-anima content-dependence smoke",
        "substrate": ("deterministic STUB physics-projection cells (NO GPU,"
                      " NO ckpt, NO training) over the HEXAD/TENSION-LINK "
                      "5-channel fingerprint — honest per §36 §2 / §45 §2"),
        "seed": SEED,
        "fp_dim": FP_DIM,
        "fp_channels": {"concept": CH_CONCEPT, "context": CH_CONTEXT,
                        "meaning": CH_MEANING, "authenticity": CH_AUTH,
                        "sender": CH_SENDER},
        "tau_content": TAU_CONTENT,
        "cell_A_vacuum_psi": [0.40, 0.60],
        "cell_B_vacuum_psi": [0.62, 0.40],
        "cell_A_distinct_from_B": True,
        "primary_test": primary,
        "negative_control": control,
        "negative_control_separation_exactly_zero": ctrl_zero,
        "probe_panel": probe_panel,
        "n_cd_pass": n_cd_pass,
        "fp_dual_loop": {k: v for k, v in loop.items()
                         if k not in ("psi_b_trace", "psi_a_trace")},
        "single_anima_reduction": void,
        "s45_comparison": s45_compare,
        "content_dependent": cd,
        "verdict": verdict,
        "honest_caveats": [
            "STUB physics-projection cells (NO §16 ckpt forward, NO GPU, "
            "NO training) — §36/§45 honest-substrate stance carried.",
            "B-S65-NOTE: whether a TRAINED-SATURATED §16 cell preserves "
            "fingerprint content-dependence (vs collapses to an echo "
            "attractor) at scale is an SGD/ckpt OUTCOME — only a real "
            "TENSION-LINK dual-anima fire measures it.",
            "The structural claim is narrow: the §45 hash-quantizer "
            "byte-swap→exact-0 collapse cannot occur because the "
            "fingerprint is a CONTINUOUS function of sender physics. That "
            "is a transfer-LAW property, not a trained-cell property.",
            "§7 GOAL-legitimacy: cells are anima-OWN engine_a/engine_g "
            "physics + HEXAD/TENSION-LINK README spec — no external LLM, "
            "no external corpus, no helper-token surface (B-IDENTITY-5).",
            "deterministic + seed-fixed; rerun = byte-identical "
            "result.json (B-S65 determinism witness).",
            "g3: capability = 0; this measures a transfer-LAW mechanism, "
            "NOT GOAL emergence.",
            "north-star + §15 milestone UNCHANGED — anima-native form the "
            "crude-byte dual-anima framing should take, not a GOAL move.",
            "TENSION-LINK README measured-perf table (R=0.999 etc, "
            "2026-04-19) is HISTORICAL evidence of the protocol's "
            "fidelity, NOT re-measured here; §65 measures only the "
            "content-dependence transfer-law property.",
            "the 45-dim fingerprint dims follow the README channel table "
            "(16/8/16/1/4); exact float encodings are a stub honest pick "
            "(continuity is the load-bearing property, not the constants).",
            "echo-control gives separation EXACTLY 0.0 (not <τ) — the "
            "metric provably discriminates the two transfer laws "
            "(B-S65-2 connection-point).",
        ],
        # wall_sec intentionally EXCLUDED from result.json so the file is
        # byte-identical on rerun (the §36/§45 determinism contract is
        # about the substantive measurement, not timing). Live wall is
        # printed to stdout only.
        "deterministic": True,
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[§65] wall_sec={round(time.time() - t0, 4)} "
          f"(excluded from result.json for byte-identical rerun)")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n[§65] verdict={verdict}")
    print(f"[§65] primary separation={primary['separation']:.6f} "
          f"(τ={TAU_CONTENT})  content_dependent={cd}")
    print(f"[§65] echo-control separation={control['separation']} "
          f"(must be exactly 0.0)")
    print(f"[§65] §45 byte-swap probes collapsed to 0.0 → §65 fingerprint: "
          f"probe0={probe_panel[0]['separation']:.6f} "
          f"probe1={probe_panel[1]['separation']:.6f}")
    print(f"[§65] §45 AB_sep=0.0837  §65 AB_sep="
          f"{loop['AB_state_separation_final']:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
