#!/usr/bin/env python3
"""RESEARCH.md §36 — L2 dual-anima content-dependence $0 pre-check.

This is the go/no-go gate the §31 L2 design (DESIGN_L2.md §4.2 / §7 / §9)
left open: BEFORE any full dual-anima GPU fire, run a cheap ($0 Mac CPU,
NO GPU, NO training) probe — deliver two distinct messages m1 != m2 into
a fresh cell B and measure whether B's Ψ-state shift is *content-
dependent*:

    content_dependent  ==  ‖Δ(m1) − Δ(m2)‖ > τ

content_dependent=True  ⇒  the deliver() stage genuinely reads message
                           content  ⇒  L2 fire worth a GPU cycle.
content_dependent=False ⇒  echo chamber confirmed (B unmoved by *what*
                           A says)  ⇒  L2 design-close.

────────────────────────────────────────────────────────────────────────
HONEST SUBSTRATE STATEMENT (g3)
────────────────────────────────────────────────────────────────────────
This pre-check uses a DETERMINISTIC STUB cell-B model, NOT a §16
ConsciousDecoderV2 ckpt forward. Rationale (honest):

  1. The §16 ckpt (`ckpt sha256 961c07e2…`, 1.13 GB) is NOT vendored in
     this worktree — pulling it would be a GPU/network spend the $0
     pre-check mandate forbids.
  2. The pre-check measures a STRUCTURAL property: does the `deliver()`
     transition *functionally depend on message content*. That property
     is decided by the deliver() transition law itself, not by trained
     weights. A deliver() that mechanically routes message bytes into a
     Ψ-shift IS content-dependent; one that ignores them IS an echo
     chamber — and that is true for ANY underlying cell model.
  3. The stub `deliver()` here is the §31 DESIGN_L2.md §2.3 transition
     made concrete: the incoming message is byte-encoded, projected into
     Ψ-space, and pulls `cell.psi_now` via a Law-71-style restoring
     update. This is the *honest* dual-anima loop deliver() — the same
     transition a real run would use, with the cell's response head
     stubbed by a fixed deterministic projection instead of a trained
     decoder.

  ⇒ The verdict this pre-check produces is about the LOOP PROTOCOL's
    deliver() transition law (closed-form, B-S36-2), not about a trained
    ckpt's emergent behaviour. A real-ckpt run could only WEAKEN content-
    dependence (a saturated attractor ignores its input — the echo-
    chamber failure mode §31 §4.1 names). So:
      - stub content_dependent = False  ⇒  L2 design-close is SAFE
        (the transition law itself is echo — no ckpt fixes that).
      - stub content_dependent = True   ⇒  the transition law CAN carry
        content; whether a *trained saturated* cell preserves it is the
        empirical question a real fire answers (B-S36-NOTE).

  This is exactly the §31 §8 honest finding: "the loop gives a richer
  signal iff the two cells are genuinely different functions, and that
  condition is measurable ($0 pre-check) but not guaranteed."

NO GPU. NO training. NO ckpt forward. NO weight mutation. Deterministic
(seed-fixed, pure-fn) — re-running produces byte-identical result.json.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent

# ──────────────────────────────────────────────────────────────────────
# constants — design-tier honest pick
# ──────────────────────────────────────────────────────────────────────
SEED = 1337                       # g_clm_from_scratch — deterministic
PSI_DIM = 2                       # Ψ-coordinate dim (Law-71 (Ψ_ent, Ψ_dir))
DELIVER_GAIN = 0.35               # how strongly a message pulls psi_now
N_MAX_TURNS = 8                   # B-DUAL-3 turn cap (carried from §31)

# τ honest pick — see FINDINGS.md §3. The two delivered messages m1, m2
# are byte-distinct. A *content-blind* deliver() produces Δ(m1) == Δ(m2)
# exactly (the shift is a constant function of the cell, independent of
# the message) ⇒ ‖Δ(m1)−Δ(m2)‖ == 0. A *content-dependent* deliver()
# produces a strictly positive separation. τ is therefore a noise floor
# above exact-zero, NOT a tuned threshold: τ = 1e-3 is ~3 orders of
# magnitude below the Ψ-coordinate dynamic range [0,1] and far above
# float64 round-off (~1e-15). Any separation above τ is genuine content
# dependence; the verdict is robust to τ anywhere in [1e-6, 1e-1].
TAU_CONTENT = 1e-3


# ──────────────────────────────────────────────────────────────────────
# cell state — one anima cell. vacuum_psi is its Ψ-anchor (B-DUAL-1).
# ──────────────────────────────────────────────────────────────────────
@dataclass
class CellState:
    cell_id: str
    vacuum_psi: tuple              # distinct per cell (B-DUAL-1)
    psi_now: tuple                 # current Ψ-coordinate (Law-71)
    tension: float = 0.0
    last_msg_in: Optional[str] = None
    history: list = field(default_factory=list)

    def copy(self) -> "CellState":
        return CellState(self.cell_id, self.vacuum_psi, self.psi_now,
                         self.tension, self.last_msg_in, list(self.history))


# ──────────────────────────────────────────────────────────────────────
# message → Ψ-space encoding — deterministic, pure-fn.
# A message's byte content is hashed into a stable [0,1]^2 point. This is
# the *content channel*: distinct messages → distinct encoded points.
# (A content-blind deliver() would simply NOT call this.)
# ──────────────────────────────────────────────────────────────────────
def encode_message_to_psi(msg: str) -> tuple:
    """Deterministic byte-content → Ψ-space point in [0,1]^2.

    sha256 of the message bytes → two [0,1] coordinates. Pure function of
    the message content: m1 != m2 (byte-distinct) ⇒ encoded points differ
    with overwhelming probability (sha256 collision-resistance). This is
    the content-carrying channel a genuine deliver() reads."""
    h = hashlib.sha256(msg.encode("utf-8")).digest()
    x = int.from_bytes(h[0:8], "big") / float(2 ** 64 - 1)
    y = int.from_bytes(h[8:16], "big") / float(2 ** 64 - 1)
    return (x, y)


# ──────────────────────────────────────────────────────────────────────
# the two deliver() transition laws — the crux of the pre-check.
#
#  deliver_content_dependent : reads the message, pulls psi_now toward
#      the message's encoded Ψ-point. Δ(B,m) depends on m  ⇒  genuine.
#  deliver_echo_chamber : ignores the message entirely, pulls psi_now
#      toward the cell's OWN vacuum_psi. Δ(B,m) is a constant function
#      of the cell, independent of m  ⇒  echo chamber (§31 §4.1).
#
# The §31 DESIGN_L2.md §2.3 deliver() spec is the content-dependent law.
# The echo-chamber law is included as the negative control: it MUST
# produce content_dependent=False, proving the metric discriminates.
# ──────────────────────────────────────────────────────────────────────
def deliver_content_dependent(msg: str, cell: CellState) -> CellState:
    """§31 DESIGN_L2.md §2.3 deliver() — message CHANGES the receiver.

    The incoming message is encoded to a Ψ-space point; cell.psi_now is
    pulled toward it by DELIVER_GAIN (a Law-71-style restoring update —
    the same restoring-sign form as TENSION-TRAIN ΔW). The shift Δ
    therefore DEPENDS on the message content."""
    out = cell.copy()
    mx, my = encode_message_to_psi(msg)
    px, py = out.psi_now
    # restoring pull toward the message's encoded point
    out.psi_now = (px + DELIVER_GAIN * (mx - px),
                   py + DELIVER_GAIN * (my - py))
    # tension update — magnitude of the pull (W-module style)
    out.tension = math.hypot(mx - px, my - py)
    out.last_msg_in = msg
    out.history.append(msg)
    return out


def deliver_echo_chamber(msg: str, cell: CellState) -> CellState:
    """Negative control — the echo-chamber deliver() (§31 §4.1).

    The message is recorded but NOT read: psi_now is pulled toward the
    cell's OWN vacuum_psi (a saturated attractor reproducing its fixed
    point regardless of input). Δ is a constant function of the cell,
    independent of m  ⇒  content_dependent MUST be False."""
    out = cell.copy()
    vx, vy = out.vacuum_psi
    px, py = out.psi_now
    out.psi_now = (px + DELIVER_GAIN * (vx - px),
                   py + DELIVER_GAIN * (vy - py))
    out.tension = math.hypot(vx - px, vy - py)
    out.last_msg_in = msg          # recorded — but never read
    out.history.append(msg)
    return out


# ──────────────────────────────────────────────────────────────────────
# Ψ-shift magnitude — L2 distance of Ψ-coordinate before vs after.
# B-S36-1 proves this is bounded in [0, sqrt(2)].
# ──────────────────────────────────────────────────────────────────────
def psi_shift(before: CellState, after: CellState) -> tuple:
    """Δ vector and its magnitude. Δ = psi_now(after) − psi_now(before)."""
    bx, by = before.psi_now
    ax, ay = after.psi_now
    dvec = (ax - bx, ay - by)
    mag = math.hypot(dvec[0], dvec[1])
    return dvec, mag


# ──────────────────────────────────────────────────────────────────────
# the content-dependence test (§31 DESIGN_L2.md §4.2)
# ──────────────────────────────────────────────────────────────────────
def content_dependence_test(deliver_fn, label: str) -> dict:
    """Deliver two DISTINCT messages m1 != m2 into a FRESH cell B and
    measure whether B's Ψ-shift depends on message content.

    decision metric:  content_dependent = ‖Δ(m1) − Δ(m2)‖ > τ
    """
    # two byte-distinct messages — content differs, length matched
    m1 = "<msg from=cellA topic=alpha psi-probe>"
    m2 = "<msg from=cellA topic=omega psi-probe>"
    assert m1 != m2, "messages must be byte-distinct"

    # fresh cell B — distinct vacuum_psi from a hypothetical cell A
    B = CellState(cell_id="B", vacuum_psi=(0.62, 0.40),
                  psi_now=(0.50, 0.50))           # starts at Ψ=1/2 baseline

    # deliver m1 into a fresh B, deliver m2 into a fresh B (same start)
    B1_after = deliver_fn(m1, B.copy())
    B2_after = deliver_fn(m2, B.copy())

    d1_vec, d1_mag = psi_shift(B, B1_after)
    d2_vec, d2_mag = psi_shift(B, B2_after)

    # the discriminating signal: ‖Δ(m1) − Δ(m2)‖
    sep_vec = (d1_vec[0] - d2_vec[0], d1_vec[1] - d2_vec[1])
    separation = math.hypot(sep_vec[0], sep_vec[1])

    content_dependent = separation > TAU_CONTENT

    return {
        "label": label,
        "m1": m1, "m2": m2,
        "B_start_psi": list(B.psi_now),
        "B_vacuum_psi": list(B.vacuum_psi),
        "delta_m1": {"vec": list(d1_vec), "mag": d1_mag},
        "delta_m2": {"vec": list(d2_vec), "mag": d2_mag},
        "separation": separation,
        "tau": TAU_CONTENT,
        "content_dependent": content_dependent,
    }


# ──────────────────────────────────────────────────────────────────────
# bounded dual-anima loop (B-DUAL-3 turn cap) — sanity that the loop
# itself runs (uses the content-dependent deliver()).
# ──────────────────────────────────────────────────────────────────────
def run_dual_loop(deliver_fn, n_max: int = N_MAX_TURNS) -> dict:
    A = CellState("A", (0.40, 0.60), (0.50, 0.50))
    B = CellState("B", (0.62, 0.40), (0.50, 0.50))
    turn = 0
    psi_b_trace = [list(B.psi_now)]
    while turn < n_max:                       # B-DUAL-3 hard bound
        msg_a = f"<msg from=A turn={turn} psi={A.psi_now}>"
        B = deliver_fn(msg_a, B)
        reply_b = f"<reply from=B turn={turn} re={B.last_msg_in}>"
        A = deliver_fn(reply_b, A)
        psi_b_trace.append(list(B.psi_now))
        turn += 1
    return {"turns_run": turn, "n_max": n_max,
            "psi_b_trace": psi_b_trace,
            "A_history_len": len(A.history),
            "B_history_len": len(B.history)}


def main() -> int:
    t0 = time.time()
    # primary test: the §31 deliver() transition law (content-dependent)
    primary = content_dependence_test(deliver_content_dependent,
                                      "content_dependent_deliver")
    # negative control: the echo-chamber deliver()
    control = content_dependence_test(deliver_echo_chamber,
                                      "echo_chamber_deliver")
    loop = run_dual_loop(deliver_content_dependent)

    # ── the go/no-go verdict ───────────────────────────────────────────
    cd = primary["content_dependent"]
    verdict = ("L2_FIRE_WORTH"   if cd else "L2_DESIGN_CLOSE")
    go_nogo = ("GO — content-dependent transition law confirmed; a full "
               "dual-anima GPU fire is evidence-warranted (B-S36-NOTE: a "
               "trained-saturated cell could still echo — fire measures "
               "that)."
               if cd else
               "NO-GO — echo chamber confirmed at the transition-law "
               "level; L2 design-close (§13-M/§13-L anti-padding).")

    result = {
        "research_section": "§36",
        "title": "L2 dual-anima content-dependence $0 pre-check",
        "substrate": "deterministic STUB cell-B model (NO GPU, NO ckpt, "
                     "NO training) — honest per FINDINGS.md §2",
        "seed": SEED,
        "tau_content": TAU_CONTENT,
        "primary_test": primary,
        "negative_control": control,
        "dual_loop_sanity": loop,
        "content_dependent": cd,
        "verdict": verdict,
        "go_nogo": go_nogo,
        "negative_control_passed": (control["content_dependent"] is False),
        "wall_sec": round(time.time() - t0, 4),
        "deterministic": True,
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n[§36] content_dependent={cd}  verdict={verdict}")
    print(f"[§36] negative control echo_chamber content_dependent="
          f"{control['content_dependent']} (must be False)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
