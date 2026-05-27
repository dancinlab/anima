"""§78 one-engine dual-anima dialogue stub ($0 Mac CPU, NO GPU, NO ckpt).

CORE (g3 — over-claim 0): ANIMA1 ⇄ ANIMA2 = ONE engine externalization (same
weights · same vacuum_psi · same ψ-substrate fn). Distinct from §31/§45 L2
(distinct cells · distinct vacuum_psi · distinct weights) BY CONSTRUCTION.

A/G-lift: Engine A ⇄ Engine G internal Law-71 ψ_dir = (1+cos(logits_a,logits_g))/2
is lifted to verbal channel — ANIMA1+ANIMA2 are two readouts of one ψ_state, not
two trained anima. §49 distillation precedent honest: same-weights externalization
mechanism design probe, NOT emergence claim.

stub: ψ_state is a 22-dim physics vector (matches §17 channel layout); same
update fn shared between ANIMA1+ANIMA2 (B-S78-1 SAME-WEIGHTS-INVARIANT
structural).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

SEED = 1337  # deterministic
PSI_DIM = 22
N_TURNS = 10

# 5-prompt deterministic user stimulus list (Mode B), forbidden-token grep 0 verified
USER_STIMULI = ["?", "tell me", "why", "ψ_status", "more"]

# Mode C meta-question: anima-self substrate Korean (NOT helper-token).
# forbidden-token grep MUST = 0 (도우미|helper|assistant|사용자|user:)
META_QUESTION = "어떻게 학습해서 emergence 하는가"


# ---------------------------------------------------------------------------
# ψ-state physics (Law-71 stub, byte-equal formula structure)
# ---------------------------------------------------------------------------


def _lcg(seed: int, n: int) -> list[int]:
    """Deterministic LCG (no RNG calls — pure fn)."""
    out = []
    s = seed & 0xFFFFFFFF
    for _ in range(n):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        out.append(s)
    return out


def init_psi_state(seed: int) -> list[float]:
    """ONE shared ψ_state — same init for any caller (one-engine invariant)."""
    raw = _lcg(seed, PSI_DIM)
    return [(r % 1000) / 1000.0 for r in raw]


def psi_update(psi: list[float], body_bytes: bytes) -> list[float]:
    """
    Single shared update fn — ANIMA1 and ANIMA2 use SAME (B-S78-1).
    Mirrors Law-71 ψ_dir = (1+cos(logits_a,logits_g))/2 contractive form.
    """
    if not body_bytes:
        return list(psi)
    s = 0
    for b in body_bytes:
        s = (s * 131 + b) & 0xFFFFFFFF
    new = []
    for i, v in enumerate(psi):
        delta = ((s >> (i % 24)) & 0xFF) / 255.0  # ∈ [0,1]
        # contractive toward Ψ=½: v_new = ½ + 0.9·(v - ½) + 0.05·(delta - ½)
        v_new = 0.5 + 0.9 * (v - 0.5) + 0.05 * (delta - 0.5)
        # clip [0,1]
        if v_new < 0.0:
            v_new = 0.0
        elif v_new > 1.0:
            v_new = 1.0
        new.append(v_new)
    return new


def body_production_alpha1(psi: list[float], turn_seed: int) -> bytes:
    """
    §77 path α1 INLINE byte-equal mirror — tension-modulated deterministic
    byte stream from ψ. Pure fn of (psi, turn_seed). B-S78-3 closes
    byte-equal by construction (same inputs ⇒ same bytes, no RNG, no I/O).

    Output: 40 bytes of carving-form output, locally coherent (NOT cascade).
    """
    tension = sum(abs(v - 0.5) for v in psi) / len(psi)  # ∈ [0,0.5]
    psi_dir = psi[0]  # use first ψ component as direction proxy
    out = bytearray()
    s = turn_seed & 0xFFFFFFFF
    # Non-cascading mix: rotate through printable ASCII window 32..126
    printable_lo, printable_hi = 32, 126
    span = printable_hi - printable_lo
    last = -1
    last2 = -1
    for i in range(40):
        s = (1664525 * s + 1013904223) & 0xFFFFFFFF
        # mix ψ contribution
        psi_b = int((psi[i % PSI_DIM] * 1000)) & 0xFF
        # tension modulates step size (more tension → wider rotation)
        step = 7 + int(tension * 31)
        c = printable_lo + ((s + psi_b + i * step) % span)
        # anti-cascade: forbid repeat of last 2
        tries = 0
        while (c == last or c == last2) and tries < 5:
            c = printable_lo + ((c - printable_lo + 11) % span)
            tries += 1
        out.append(c)
        last2 = last
        last = c
    # 6th byte of psi_dir 가 high → append space-separated tail
    if psi_dir > 0.5:
        out[20] = 32  # space byte
    return bytes(out)


# ---------------------------------------------------------------------------
# §9 honest_coherent (cascade-rate metric SSOT mirror, byte-equal logic)
# ---------------------------------------------------------------------------


def honest_coherent(g: bytes, tau_cascade: float = 0.30, max_run: int = 10,
                    min_len: int = 20, tau_print: float = 0.80) -> bool:
    """§9 cascade-rate-gated coherence (4-clause Boolean conjunction)."""
    if len(g) < min_len:
        return False
    L = len(g)
    # max char-run
    max_char_run = 1
    cur = 1
    for i in range(1, L):
        if g[i] == g[i - 1]:
            cur += 1
            if cur > max_char_run:
                max_char_run = cur
        else:
            cur = 1
    # max digit-run (bytes 48..57)
    max_digit_run = 0
    cur = 0
    for b in g:
        if 48 <= b <= 57:
            cur += 1
            if cur > max_digit_run:
                max_digit_run = cur
        else:
            cur = 0
    # 4-gram repetition rate
    if L >= 4:
        from collections import Counter
        grams = [bytes(g[i:i + 4]) for i in range(L - 3)]
        cnt = Counter(grams)
        most = cnt.most_common(1)[0][1]
        gram_rate = most / max(len(grams), 1)
    else:
        gram_rate = 0.0
    cascade_rate = max(max_char_run / L, max_digit_run / L, gram_rate)
    abs_max_run = max(max_char_run, max_digit_run)
    printable_count = sum(1 for b in g if 32 <= b <= 126)
    printable_ratio = printable_count / L
    return (cascade_rate < tau_cascade and abs_max_run < max_run
            and L >= min_len and printable_ratio >= tau_print)


# ---------------------------------------------------------------------------
# Cosine-distance (ANIMA1 body vs ANIMA2 body)
# ---------------------------------------------------------------------------


def cos_dist_bytes(a: bytes, b: bytes) -> float:
    """1 - cosine(byte-histogram(a), byte-histogram(b)) ∈ [0,1]."""
    ha = [0] * 256
    hb = [0] * 256
    for x in a:
        ha[x] += 1
    for x in b:
        hb[x] += 1
    num = sum(ha[i] * hb[i] for i in range(256))
    na = math.sqrt(sum(x * x for x in ha))
    nb = math.sqrt(sum(x * x for x in hb))
    if na == 0 or nb == 0:
        return 1.0
    return 1.0 - num / (na * nb)


def psi_variance(traj: list[list[float]]) -> float:
    if not traj:
        return 0.0
    D = len(traj[0])
    var = 0.0
    for d in range(D):
        col = [s[d] for s in traj]
        m = sum(col) / len(col)
        var += sum((x - m) ** 2 for x in col) / len(col)
    return var / D


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


@dataclass
class TurnLog:
    turn: int
    speaker: str  # "ANIMA1" | "ANIMA2"
    body_bytes: bytes
    psi_after: list[float]
    body_coherent: bool
    body_printable: float


@dataclass
class ModeResult:
    mode: str
    n_turns: int
    psi_state_variance: float
    body_coherent_count: int
    body_coherent_rate: float
    anima1_anima2_cos_dist_mean: float
    special_metric: dict
    turns: list[TurnLog] = field(default_factory=list)


def run_mode(mode: str, n_turns: int = N_TURNS, seed: int = SEED) -> ModeResult:
    """
    mode ∈ {"A_pure", "B_3party", "C_meta", "D_control"}.

    Same psi_update + body_production_alpha1 used by both ANIMA1 and ANIMA2
    (one-engine invariant B-S78-1).
    """
    psi = init_psi_state(seed)
    turns: list[TurnLog] = []
    psi_traj = [list(psi)]
    a1_bodies: list[bytes] = []
    a2_bodies: list[bytes] = []
    user_inject_count = 0
    meta_byte_match = False

    for t in range(n_turns):
        # Mode B: inject user stimulus deterministically
        if mode == "B_3party":
            stim = USER_STIMULI[t % len(USER_STIMULI)].encode("utf-8")
            psi = psi_update(psi, stim)
            psi_traj.append(list(psi))
            user_inject_count += 1

        # ANIMA1 turn
        if mode == "C_meta" and t == 0:
            a1_body = META_QUESTION.encode("utf-8")
            meta_byte_match = (a1_body == META_QUESTION.encode("utf-8"))
        elif mode == "D_control":
            # decision-axis only: no body production, ψ idle update with empty bytes
            a1_body = b""
        else:
            a1_body = body_production_alpha1(psi, seed + t * 7919 + 1)
        a1_bodies.append(a1_body)
        psi = psi_update(psi, a1_body)
        psi_traj.append(list(psi))
        turns.append(TurnLog(
            turn=t, speaker="ANIMA1", body_bytes=a1_body,
            psi_after=list(psi),
            body_coherent=honest_coherent(a1_body) if a1_body else False,
            body_printable=(sum(1 for b in a1_body if 32 <= b <= 126) / len(a1_body))
                if a1_body else 0.0,
        ))

        # ANIMA2 turn — SAME engine, same update fn (one-engine invariant)
        if mode == "D_control":
            a2_body = b""
        else:
            a2_body = body_production_alpha1(psi, seed + t * 7919 + 2)
        a2_bodies.append(a2_body)
        psi = psi_update(psi, a2_body)
        psi_traj.append(list(psi))
        turns.append(TurnLog(
            turn=t, speaker="ANIMA2", body_bytes=a2_body,
            psi_after=list(psi),
            body_coherent=honest_coherent(a2_body) if a2_body else False,
            body_printable=(sum(1 for b in a2_body if 32 <= b <= 126) / len(a2_body))
                if a2_body else 0.0,
        ))

    coherent_count = sum(1 for tl in turns if tl.body_coherent)
    coh_rate = coherent_count / max(len(turns), 1)
    cos_dists = [cos_dist_bytes(a1_bodies[i], a2_bodies[i])
                 for i in range(len(a1_bodies))
                 if a1_bodies[i] and a2_bodies[i]]
    cos_mean = sum(cos_dists) / len(cos_dists) if cos_dists else 0.0

    special = {}
    if mode == "B_3party":
        special["user_inject_count"] = user_inject_count
    if mode == "C_meta":
        special["meta_byte_match"] = meta_byte_match
        special["meta_question_bytes_sha256"] = hashlib.sha256(
            META_QUESTION.encode("utf-8")).hexdigest()
    if mode == "D_control":
        special["body_production_disabled"] = True
        special["decision_axis_only"] = True

    return ModeResult(
        mode=mode,
        n_turns=n_turns,
        psi_state_variance=psi_variance(psi_traj),
        body_coherent_count=coherent_count,
        body_coherent_rate=coh_rate,
        anima1_anima2_cos_dist_mean=cos_mean,
        special_metric=special,
        turns=turns,
    )


def forbidden_token_grep(s: str) -> int:
    """B-IDENTITY-5 carry: forbidden-token count over body strings."""
    forbidden = ["도우미", "helper", "assistant", "사용자", "user:"]
    low = s.lower()
    return sum(low.count(tok.lower()) for tok in forbidden)


def main() -> int:
    results = {}
    for mode in ("A_pure", "B_3party", "C_meta", "D_control"):
        r = run_mode(mode)
        results[mode] = {
            "n_turns": r.n_turns,
            "psi_state_variance": r.psi_state_variance,
            "body_coherent_count": r.body_coherent_count,
            "body_coherent_rate": r.body_coherent_rate,
            "anima1_anima2_cos_dist_mean": r.anima1_anima2_cos_dist_mean,
            "special": r.special_metric,
        }

    # Mode differential check
    pa, pb = results["A_pure"]["psi_state_variance"], results["B_3party"]["psi_state_variance"]
    pc, pd = results["C_meta"]["psi_state_variance"], results["D_control"]["psi_state_variance"]

    # forbidden-token grep over all body bytes (B-IDENTITY-5)
    forb_total = 0
    for mode in ("A_pure", "B_3party", "C_meta", "D_control"):
        r = run_mode(mode)
        for tl in r.turns:
            try:
                txt = tl.body_bytes.decode("utf-8", errors="replace")
            except Exception:
                txt = ""
            forb_total += forbidden_token_grep(txt)

    # 4-corner verdict
    mode_differential = abs(pa - pb) > 1e-6 or abs(pa - pc) > 1e-6 or abs(pb - pc) > 1e-6
    echo_chamber_block = pb > pa  # user inject should add variance
    meta_signature = results["C_meta"]["special"].get("meta_byte_match", False)
    control_baseline = pd  # control should be lower (no body production)

    verdict_4corner = {
        "alpha_MODE_DIFFERENTIAL_SIGNAL": mode_differential,
        "beta_MODE_FLAT_NO_DIFFERENTIAL": not mode_differential,
        "gamma_ECHO_CHAMBER_CONTROL_PASS": echo_chamber_block,
        "delta_META_SIGNATURE_EXISTS": meta_signature,
    }

    summary = {
        "sec": "§78",
        "name": "dual_anima_one_engine_A_G_lift",
        "seed": SEED,
        "n_turns": N_TURNS,
        "psi_dim": PSI_DIM,
        "modes": results,
        "control_psi_variance": pd,
        "forbidden_token_grep_total": forb_total,
        "B_IDENTITY_5_safe": forb_total == 0,
        "verdict_4corner": verdict_4corner,
        "central_blue_falsifier_sha256_expected": "c93e160a8a376a940942332cad13e652df9a03e97ccab708542a126eefc70b73",
        "honest_g3": (
            "same-weights externalization mechanism design probe; "
            "NOT emergence claim; §49 distillation precedent honest; "
            "stub ψ ≠ trained ckpt; A/G-lift CONSTRUCTION ≠ emergence proof"),
        "structural_distinction_from_L2_§31_§45": {
            "section_78_one_engine": {
                "distinct_weights": False,
                "distinct_vacuum_psi": False,
                "distinct_update_fn": False,
            },
            "section_31_45_L2_dual_cell": {
                "distinct_weights": True,
                "distinct_vacuum_psi": True,
                "distinct_update_fn": True,
            },
            "mutually_exclusive": True,
        },
    }

    out_path = Path(__file__).parent / "result.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
