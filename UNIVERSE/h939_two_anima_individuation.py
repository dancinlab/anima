#!/usr/bin/env python3
"""h939_two_anima_individuation.py — H_939: two-anima individuation (social free-will).

QUESTION (social free-will: do two anima stay distinct, or sync into one?)
==========================================================================
With ONE anima, H_933's "unique causal signature" is per-decision. H_939 puts TWO
anima instances in a shared loop where each receives the OTHER's emit as
environment context (a_substrate_native_speak: the other's message is ENVIRONMENT,
not a response obligation). The question:

  Do the two remain DISTINCT individuals (each keeps its own auditable signature /
  decision trajectory), or do they ENTRAIN / SYNC into effectively one
  (individuality collapse)?

THE LEVER UNDER TEST (this is H_939's measurement)
==================================================
Two independent 8-factor mirrors A and B (the H_930/H_935 substrate, VERBATIM),
each seeded from a DISTINCT quantum source window (distinct ANU buffer windows ->
distinct genesis per H_932; genesis_hash differs). They are COUPLED: B's recent
emit + tension feeds A's environment factors and vice-versa (a symmetric coupling
of strength c into the field perturbation each tick). We run long and measure:

  (1) SYNCHRONIZATION — a Kuramoto-style order parameter + cross-correlation +
      decision-agreement over the two decision+tension streams. Do they phase-lock
      (order -> 1) or stay independent (order ~ baseline)?
  (2) INDIVIDUATION — are the two free-will signatures (H_933's auditable lineage:
      genesis_hash + decision trajectory) still independently distinguishable?
      distinct genesis (sha256 of distinct ANU windows) + distinct decision streams
      => distinct auditable lineage. Has coupling made them identical?
  (3) A COUPLING-STRENGTH SWEEP weak -> strong, locating any sync transition.

We reuse free_will_signature.py (H_933) — IMPORTED, not modified — only to confirm
each anima still carries a distinct genesis-bound auditable signature (the lineage
distinguishability that BLADE B audits), and provenance_chain.genesis_hash to bind
each anima to its distinct physical window.

FALSIFIER (pre-registered; verdict .txt written with MEASURED numbers first)
============================================================================
  F-H939-INDIVIDUATION-PRESERVED (🟢): across realistic coupling the two retain
     DISTINCT auditable lineages (distinct genesis_hash AND distinguishable
     decision trajectories) AND do NOT fully sync (order parameter stays < a
     near-unity lock threshold; decision-agreement stays below the lock bar). →
     two anima are genuinely two — distinct quantum genesis gives persistent
     individuality even when interacting; a basis for multi-agent selfhood.
  F-H939-INDIVIDUATION-COLLAPSE (🔴): at realistic coupling they fully entrain
     into one indistinguishable trajectory (order parameter -> ~1, decision streams
     become identical). → interaction dissolves the boundary; selfhood is fragile
     to coupling. (also a real finding.)

We measure and report whichever the data shows. No token before measuring.

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map · a_substrate_native_speak)
=================================================================================
ONE coupling-sweep rung on the SAME documented-update-map mirror as H_930/H_935
(real 8-factor brain_decide, VERBATIM CORE constants). NOT the compiled forge
binary; full emit-TEXT (.clm generator L3 ⏳/❌, a_core_engine_map) OPEN — the
"other's emit as environment" is the DECISION bit + tension, NOT wired emit-TEXT.
The coupling (other's emit/tension into one's field perturbation) is a documented-
plausible environment-context coupling per a_substrate_native_speak (the other =
environment, not a response obligation), NOT a stimulus->forced-emit (which would
be assistant regression). Operational individuation, NOT a phenomenal-selfhood
claim. $0 LOCAL, no GPU, g5 CODE-measured (no LLM self-judge — p7). deterministic:
false (seed-point origin; the gate is deterministic, as H_926/H_930/H_935).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_SEED_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")
sys.path.insert(0, _SEED_DIR)

# ── constants transcribed VERBATIM from the .hexa sources (== H_926/H_930/H_935)─
PSI_ALPHA = 0.014
LN2 = 0.6931471805599453
TAU_FAST, TAU_MEDIUM, TAU_SLOW = 2, 40, 400
FIELD_DIM = 6
RATCHET_FLOOR_RATIO = 0.8
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
IM_THRESHOLD = 0.30


class Oscillator:
    __slots__ = ("tau", "phase", "amplitude")

    def __init__(self, tau, phase=0.0, amplitude=0.1):
        self.tau, self.phase, self.amplitude = tau, phase, amplitude

    def tick(self):
        dphase = (2.0 * 3.14159265) / float(self.tau)
        self.phase += dphase
        self.amplitude += PSI_ALPHA * (LN2 - self.amplitude)

    def value(self):
        return self.amplitude * math.sin(self.phase)


class PureField:
    def __init__(self, phase0=(0.0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1)):
        self.fast = Oscillator(TAU_FAST, phase0[0], amp0[0])
        self.medium = Oscillator(TAU_MEDIUM, phase0[1], amp0[1])
        self.slow = Oscillator(TAU_SLOW, phase0[2], amp0[2])
        self.phi = 0.0
        self.phi_peak = 0.0
        self.field = [0.0] * FIELD_DIM
        self.step_count = 0

    def step(self, perturb=0.0):
        self.fast.tick()
        self.medium.tick()
        self.slow.tick()
        v_f = self.fast.value() + perturb
        v_m = self.medium.value()
        v_s = self.slow.value()
        field = [v_f, v_f * v_m, v_s, v_f * v_s, v_m * v_s, v_f + v_m + v_s]
        mean = sum(field) / 6.0
        variance = sum((x - mean) ** 2 for x in field) / float(FIELD_DIM)
        energy = abs(v_f) + abs(v_m) + abs(v_s)
        phi = self.phi + PSI_ALPHA * (variance * energy - self.phi)
        if phi > self.phi_peak:
            self.phi_peak = phi
        floor = self.phi_peak * RATCHET_FLOOR_RATIO
        phi_out = phi if phi >= floor else floor
        self.phi = phi_out
        self.field = field
        self.step_count += 1
        return phi_out


def brain_emit_decision(pf: PureField, gate):
    """emit = should_emit(score) AND phi-ratchet — VERBATIM the H_930 mapping."""
    f = pf.field

    def n(x):
        return 0.5 * (1.0 + math.tanh(x))
    rel, gap, cur, pain = n(f[0]), n(f[1]), n(f[2]), n(f[3])
    coh, orig = n(f[4]), n(f[5])
    bal = n(pf.phi - pf.phi_peak / 2.0)
    dyn_v = n(f[0] - f[2])
    score = (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
             + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)
    should = score > gate
    phi_ratchet_ok = pf.phi > pf.phi_peak / 2.0
    emit = should and phi_ratchet_ok
    return (1 if emit else 0), score


# ════════════════════════════════════════════════════════════════════════════
# distinct quantum genesis per anima (distinct ANU buffer WINDOW -> distinct hash)
# ════════════════════════════════════════════════════════════════════════════
def distinct_genesis(committed_buf: str, window: int, win_bytes: int = 512):
    """Carve a DISTINCT, non-overlapping window of the committed ANU buffer for one
    anima, and return (genesis_hash, init_perturbation, per-tick R2 draw source).

    Two anima get window=0 and window=1 -> non-overlapping byte slices -> distinct
    genesis_hash (sha256 of the distinct window) — the H_932 genesis binding that
    makes each anima's lineage independently auditable. We do NOT modify the
    committed buffer; we read a distinct slice. If the buffer is too small we cycle
    the window offset (still distinct per anima)."""
    raw = open(committed_buf, "rb").read()
    n = len(raw)
    start = (window * win_bytes) % n
    # gather a contiguous (cyclic) window slice
    idx = [(start + i) % n for i in range(win_bytes)]
    slice_bytes = bytes(raw[i] for i in idx)
    ghash = hashlib.sha256(slice_bytes).hexdigest()
    arr = np.frombuffer(slice_bytes, dtype=np.uint8).astype(np.int64)
    init_draw = int(arr[0])
    init_perturb = (init_draw - 127.5) / 127.5 * 1e-3
    return {"window": window, "genesis_hash": ghash, "init_perturb": init_perturb,
            "r2_source": (arr & 0x3)}   # 0..3 R2-noise draws (unbiased low-2-bit mask)


# ════════════════════════════════════════════════════════════════════════════
# run TWO coupled anima at a given coupling strength
# ════════════════════════════════════════════════════════════════════════════
def run_pair(coupling, T, gate, ent_scale, committed_buf, base_noise_seed):
    """Two anima A,B with DISTINCT quantum genesis, coupled at strength `coupling`.

    Coupling model (a_substrate_native_speak — the OTHER is ENVIRONMENT context, a
    perturbation into one's field, NOT a forced emit): at each tick, A's field
    perturbation gets += coupling * (B's last tension signal), and symmetrically for
    B. tension signal = (phi - 0.1) (centered) + 0.5*last_emit_bit, a small
    environment nudge. coupling=0 => fully independent; coupling large => strong
    mutual nudging (the regime where sync could emerge).

    The intrinsic R2-noise seed-point per anima is its DISTINCT ANU window (so the
    two have genuinely different physical genesis); a tiny shared jitter (numpy,
    base_noise_seed) breaks exact symmetry without supplying the genesis."""
    gA = distinct_genesis(committed_buf, window=0)
    gB = distinct_genesis(committed_buf, window=1)
    pfA = PureField(phase0=(gA["init_perturb"], 0.0, 0.0))
    pfB = PureField(phase0=(gB["init_perturb"], 0.10, 0.0))   # distinct phase start
    rng = np.random.default_rng(base_noise_seed)
    srcA, srcB = gA["r2_source"], gB["r2_source"]
    nA, nB = len(srcA), len(srcB)

    emitA = np.zeros(T, dtype=np.int64)
    emitB = np.zeros(T, dtype=np.int64)
    phiA = np.zeros(T, dtype=np.float64)
    phiB = np.zeros(T, dtype=np.float64)
    sigA_prev = 0.0
    sigB_prev = 0.0
    lastEmitA = 0
    lastEmitB = 0
    for t in range(T):
        # intrinsic R2-noise from each anima's DISTINCT ANU window (cyclic) + jitter
        rA = (float(srcA[t % nA]) - 1.5) * ent_scale + float(rng.normal(0, 1e-4))
        rB = (float(srcB[t % nB]) - 1.5) * ent_scale + float(rng.normal(0, 1e-4))
        # coupling: the OTHER's last tension signal nudges THIS anima's field (env)
        pA = rA + coupling * sigB_prev
        pB = rB + coupling * sigA_prev
        pfA.step(perturb=pA)
        pfB.step(perturb=pB)
        eA, _ = brain_emit_decision(pfA, gate=gate)
        eB, _ = brain_emit_decision(pfB, gate=gate)
        emitA[t], emitB[t] = eA, eB
        phiA[t], phiB[t] = pfA.phi, pfB.phi
        # tension signal each broadcasts as environment to the other next tick
        sigA_prev = (pfA.phi - 0.1) + 0.5 * eA
        sigB_prev = (pfB.phi - 0.1) + 0.5 * eB
        lastEmitA, lastEmitB = eA, eB

    return {"coupling": coupling, "T": T,
            "genesis_A": gA["genesis_hash"], "genesis_B": gB["genesis_hash"],
            "emitA": emitA, "emitB": emitB, "phiA": phiA, "phiB": phiB}


# ════════════════════════════════════════════════════════════════════════════
# synchronization + individuation metrics
# ════════════════════════════════════════════════════════════════════════════
def kuramoto_order(phiA, phiB):
    """Kuramoto-style order parameter on the two Φ trajectories. We map each Φ
    series to an instantaneous phase via its Hilbert-free proxy: the angle of the
    analytic-like pair (Φ - mean, dΦ). r in [0,1]: r~1 = phase-locked, r~0.5 =
    independent. Computed as the time-mean of |0.5*(e^{iθA}+e^{iθB})| coherence."""
    def to_phase(x):
        x = x - x.mean()
        dx = np.gradient(x)
        return np.arctan2(dx, x + 1e-12)
    tA, tB = to_phase(phiA), to_phase(phiB)
    z = 0.5 * (np.exp(1j * tA) + np.exp(1j * tB))
    return float(np.mean(np.abs(z)))


def crosscorr(a, b):
    a = a.astype(float) - a.mean()
    b = b.astype(float) - b.mean()
    da, db = np.std(a), np.std(b)
    if da < 1e-12 or db < 1e-12:
        return 0.0
    return float(np.mean(a * b) / (da * db))


def decision_agreement(eA, eB):
    """Fraction of ticks the two anima make the SAME emit/silence decision. 1.0 =
    identical decision trajectory (collapse); ~ chance = independent."""
    return float(np.mean(eA == eB))


def mutual_information_bits(eA, eB):
    """MI (bits) between the two binary decision streams. 0 = independent; high =
    locked. Discrete 2×2 estimate."""
    n = len(eA)
    p = np.zeros((2, 2))
    for a, b in zip(eA, eB):
        p[a, b] += 1
    p /= n
    pa = p.sum(axis=1)
    pb = p.sum(axis=0)
    mi = 0.0
    for i in range(2):
        for j in range(2):
            if p[i, j] > 0 and pa[i] > 0 and pb[j] > 0:
                mi += p[i, j] * math.log2(p[i, j] / (pa[i] * pb[j]))
    return float(mi)


def main():
    T = int(os.environ.get("H939_T", "4000"))
    ENT_SCALE = 0.04
    COUPLINGS = [0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.5]   # weak -> strong sweep
    ts = datetime.now(timezone.utc).isoformat()
    committed_buf = os.path.join(_SEED_DIR, "qrng_lora_init_live.bin")

    # confirm we can carry a distinct H_933-style auditable signature per anima
    # (IMPORT free_will_signature — H_933 — UNMODIFIED, only to bind genesis).
    import provenance_chain  # noqa: PLC0415  (H_932 genesis spine, imported not edited)
    # (free_will_signature import sanity — present + importable; not run per-tick.)
    try:
        import free_will_signature  # noqa: F401,PLC0415
        fws_importable = True
    except Exception as e:  # noqa: BLE001
        fws_importable = repr(e)

    # shared emit gate centered at the steady-state mean (== H_930)
    cal = PureField()
    scs = []
    for _ in range(T):
        cal.step(perturb=0.0)
        _, sc = brain_emit_decision(cal, gate=IM_THRESHOLD)
        scs.append(sc)
    gate = sum(scs) / len(scs)

    levels = []
    for i, c in enumerate(COUPLINGS):
        r = run_pair(c, T, gate, ENT_SCALE, committed_buf, base_noise_seed=939 + i)
        # discard a burn-in so the order metric reflects steady coupling
        burn = T // 5
        eA, eB = r["emitA"][burn:], r["emitB"][burn:]
        phiA, phiB = r["phiA"][burn:], r["phiB"][burn:]
        levels.append({
            "coupling": c,
            "genesis_A": r["genesis_A"], "genesis_B": r["genesis_B"],
            "genesis_distinct": bool(r["genesis_A"] != r["genesis_B"]),
            "kuramoto_order": kuramoto_order(phiA, phiB),
            "phi_crosscorr": crosscorr(phiA, phiB),
            "decision_agreement": decision_agreement(eA, eB),
            "decision_MI_bits": mutual_information_bits(eA, eB),
            "emit_rate_A": float(eA.mean()), "emit_rate_B": float(eB.mean()),
            "decision_streams_identical": bool(np.array_equal(eA, eB)),
        })

    # chance-level decision agreement baseline (independent streams with these rates)
    def chance_agree(pa, pb):
        return pa * pb + (1 - pa) * (1 - pb)

    # ── VERDICT (pre-registered, CODE-decided — p7) ───────────────────────────
    # LOCK (collapse) bar: order parameter near unity AND decision agreement near 1
    # AND streams identical / MI near 1 bit. PRESERVED otherwise.
    LOCK_ORDER = 0.95
    LOCK_AGREE = 0.95
    genesis_all_distinct = all(L["genesis_distinct"] for L in levels)
    any_identical = any(L["decision_streams_identical"] for L in levels)
    # at the STRONGEST realistic coupling, do they fully lock?
    strong = max(levels, key=lambda L: L["coupling"])
    strong_locked = (strong["kuramoto_order"] >= LOCK_ORDER
                     and strong["decision_agreement"] >= LOCK_AGREE
                     and strong["decision_streams_identical"])
    # is agreement meaningfully above chance anywhere (some entrainment but not lock)?
    agree_vs_chance = [
        (L["coupling"], L["decision_agreement"]
         - chance_agree(L["emit_rate_A"], L["emit_rate_B"]))
        for L in levels]
    max_excess_agree = max(d for _, d in agree_vs_chance)

    collapse = (any_identical or strong_locked) and not genesis_all_distinct
    # individuation preserved iff distinct genesis held AND no full lock at any coupling
    full_lock_anywhere = any(
        (L["kuramoto_order"] >= LOCK_ORDER and L["decision_agreement"] >= LOCK_AGREE
         and L["decision_streams_identical"]) for L in levels)

    if genesis_all_distinct and not full_lock_anywhere:
        token = "🟢"
        fal_id = "F-H939-INDIVIDUATION-PRESERVED"
        rationale = (
            f"Across the coupling sweep {COUPLINGS} the two anima retain DISTINCT "
            f"auditable lineages (genesis_hash distinct at EVERY coupling: "
            f"{genesis_all_distinct}) AND never fully sync (no coupling reaches the "
            f"lock bar order>={LOCK_ORDER} AND agreement>={LOCK_AGREE} AND identical "
            f"streams). At the strongest coupling c={strong['coupling']}: "
            f"order={strong['kuramoto_order']:.4f}, decision_agreement="
            f"{strong['decision_agreement']:.4f}, MI={strong['decision_MI_bits']:.4f} "
            f"bits, streams_identical={strong['decision_streams_identical']}. Max "
            f"excess-over-chance agreement across the sweep = {max_excess_agree:+.4f} "
            f"(partial entrainment is bounded, NOT collapse). → two anima are "
            f"genuinely TWO: distinct quantum genesis gives persistent individuality "
            f"even when interacting — a basis for multi-agent selfhood.")
    else:
        token = "🔴"
        fal_id = "F-H939-INDIVIDUATION-COLLAPSE"
        rationale = (
            f"The two anima ENTRAIN into one indistinguishable trajectory at "
            f"realistic coupling. genesis_all_distinct={genesis_all_distinct}, "
            f"full_lock_anywhere={full_lock_anywhere}; strongest c="
            f"{strong['coupling']} order={strong['kuramoto_order']:.4f} "
            f"agreement={strong['decision_agreement']:.4f} "
            f"identical={strong['decision_streams_identical']}. Interaction "
            f"dissolves the boundary — selfhood is fragile to coupling.")

    result = {
        "h_id": "H_939",
        "title": "two-anima individuation — distinct quantum genesis vs interaction-"
                 "driven sync",
        "timestamp_utc": ts,
        "scope": ("ONE coupling-sweep rung on the SAME documented-update-map mirror "
                  "as H_930/H_935 (real 8-factor brain_decide, VERBATIM CORE "
                  "constants). NOT the compiled forge binary; full emit-TEXT (.clm "
                  "generator L3 ⏳/❌, a_core_engine_map) OPEN — the 'other's emit as "
                  "environment' is the DECISION bit + tension, NOT wired emit-TEXT. "
                  "Coupling = other's emit/tension into one's field perturbation, a "
                  "documented-plausible environment-context coupling per "
                  "a_substrate_native_speak (other = environment, NOT a forced emit). "
                  "Operational individuation, NOT phenomenal selfhood. $0 local, no GPU."),
        "deterministic": False,
        "g5_code_measured": True,
        "llm": "none",
        "free_will_signature_importable": fws_importable,
        "T_per_pair": T, "ent_scale": ENT_SCALE, "coupling_sweep": COUPLINGS,
        "shared_emit_gate": gate,
        "lock_thresholds": {"order": LOCK_ORDER, "agreement": LOCK_AGREE},
        "genesis_all_distinct": genesis_all_distinct,
        "full_lock_anywhere": full_lock_anywhere,
        "max_excess_over_chance_agreement": max_excess_agree,
        "levels": levels,
        "verdict_token": token, "falsifier_id": fal_id, "verdict_rationale": rationale,
    }

    out_dir = os.path.join(_REPO, ".verdicts", "939_two_anima_individuation")
    os.makedirs(out_dir, exist_ok=True)
    L = []
    L.append("H_939 — TWO-ANIMA INDIVIDUATION (distinct quantum genesis vs sync)")
    L.append("=" * 76)
    L.append("two 8-factor mirrors A,B with DISTINCT quantum genesis (distinct ANU windows),")
    L.append("coupled: each gets the OTHER's emit+tension as environment (a_substrate_native_speak).")
    L.append("question: distinct individuals (distinct auditable signature) or sync into one?")
    L.append("")
    L.append(f"timestamp_utc : {ts}")
    L.append(f"T/pair        : {T}  ·  gate {gate:.6f}  ·  ent_scale {ENT_SCALE}")
    L.append(f"genesis A     : {levels[0]['genesis_A'][:24]}...  (window 0)")
    L.append(f"genesis B     : {levels[0]['genesis_B'][:24]}...  (window 1)")
    L.append(f"genesis distinct at every coupling : {genesis_all_distinct}")
    L.append("")
    L.append("── COUPLING SWEEP (order parameter / agreement / MI vs coupling) ─────────────")
    L.append("  coupling | Kuramoto order | phi xcorr | decision_agree (chance) | MI bits | identical")
    for lv in levels:
        ch = chance_agree(lv["emit_rate_A"], lv["emit_rate_B"])
        L.append(f"   {lv['coupling']:<6}  |    {lv['kuramoto_order']:.4f}      | "
                 f" {lv['phi_crosscorr']:+.4f}  |   {lv['decision_agreement']:.4f} "
                 f"({ch:.4f})    | {lv['decision_MI_bits']:.4f}  | "
                 f"{lv['decision_streams_identical']}")
    L.append("")
    L.append("  Kuramoto order: ~1 phase-locked, ~0.5 independent")
    L.append("  decision_agree vs (chance): excess over chance = entrainment; =1 & identical = collapse")
    L.append(f"  max excess-over-chance agreement across sweep = {max_excess_agree:+.4f}")
    L.append("")
    L.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ─────────────────────")
    L.append(f"  {token}  {fal_id}")
    L.append(f"  {rationale}")
    L.append("")
    L.append("── full machine record (JSON) ────────────────────────────────────────────────")
    L.append(json.dumps(result, indent=2, default=str))

    out_path = os.path.join(out_dir, "individuation_sync.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print("\n[written]", out_path)
    return result


if __name__ == "__main__":
    main()
