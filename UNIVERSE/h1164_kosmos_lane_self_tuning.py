"""
H_1164 — does the KOSMOS `lane`-partition SELF-TUNE its lane COUNT to the
anchor-stream complexity, the way H_1159b's inference-time mitosis self-tunes
its cell-COUNT to the world's #clusters?

KOSMOS `lane` = the active MITOSIS cell-id (AGENT/CHAT/kosmos_anchor.hexa:20,181:
  `lane = "cell_" + to_string(cell_id)`, default cell_0). The anchor `tension_5ch`
payload is the 5-channel (concept·context·meaning·authenticity·sender) fingerprint
mapped from the 8-factor motivation snapshot.

═══ HONESTY — TWO RESULTS, CLEARLY SEPARATED ═══════════════════════════════════

(A) LIVE-WIRING verdict = ⏳ BLOCKED-WIRING (a_core_engine_map, a_kosmos).
    The live kosmos lane is a STATIC PASSTHROUGH of the mitosis cell_id
    (`lane = "cell_" + cell_id`). There is NO independent partition algorithm that
    grows a lane-COUNT from the anchor `tension_5ch` stream — the lane axis carries
    a cell label, it is not itself a dynamically-grown partition of the anchor
    stream. So "does the LIVE lane self-tune its count to anchor complexity?" is
    structurally unanswerable: the mechanism is not wired. This is NOT a 🔴 "no
    tracking" — it is the absence of a self-tuning partition to measure
    (distinct from H_1159b, where the live CORE mitosis DOES grow cells).

(B) PROPOSAL verdict = the experiment below. We model the PROPOSED dynamic
    lane-partition: the H_1159b tension-split substrate applied VERBATIM to the
    kosmos anchor `tension_5ch` (5-dim) stream instead of the 8-dim toy stream.
    If anchors arrive in K_true distinct tension-cluster regimes, does a
    tension-driven lane-split grow its lane-COUNT to track K_true, stay bounded,
    and beat a fixed-lane control? This tests whether a future lane-partition that
    decoupled the lane axis from cell_id (so lanes could grow from the anchor
    tension stream) WOULD inherit the H_1159b self-tuning property on the real
    5-channel anchor geometry. PROPOSAL only — the live kosmos_io partition is
    UNVERIFIED (a_scale_honest_scope).

═══ SUBSTRATE — H_1159b VERBATIM, only the INPUT swapped ══════════════════════
The split / assign / mitosis / cohen_d / spearman machinery below is copied
VERBATIM from UNIVERSE/h1159b_mitosis_capacity_self_tuning.py. The ONLY change:
DIM 8→5 (kosmos tension_5ch) and make_anchor_stream() emits a 5-channel anchor
tension stream whose clusters are distinct TENSION-REGIMES (e.g. high-curiosity
vs high-pain vs high-context anchors), the kosmos-native analog of H_1159b's
world clusters.

FROZEN FALSIFIER (fresh pre-reg, deterministic, >=8 seeds; sweep K_true∈{3,5,8}):
  F1 SELF-TUNING : Spearman(K_true, final lane-count) >= 0.8  — lanes track stream complexity.
  F2 ADVANTAGE   : at EVERY K_true, SPLIT final err < FIXED-LANE final err, Cohen's d >= 2.0.
  F3 SELF-LIMITING: final lane-count < MAX_LANES at every K_true (no runaway to cap).
  PROPOSAL-SUPPORTED iff F1 & F2 & F3.
toy ($0 numpy CPU). a_scale_honest_scope · a_core_engine_map · a_kosmos.
"""
import json, math
import numpy as np

# ── kosmos tension_5ch geometry (the ONLY substrate change vs H_1159b) ─────────
DIM = 5                       # kosmos anchor tension_5ch: concept·context·meaning·authenticity·sender
T = 4000; WARMUP = 250; N_SEEDS = 10
SEEDS = list(range(800, 800 + N_SEEDS))
THETA = 1.6; WIN = 200; LR = 0.05; MAX_LANES = 20   # MAX_LANES == H_1159b MAX_CELLS
K_TRUES = [3, 5, 8]
CH = ["concept", "context", "meaning", "authenticity", "sender"]


def make_anchor_stream(seed, k_true):
    """K_true distinct anchor TENSION-REGIMES over the kosmos 5-channel
    tension_5ch geometry. Structurally identical to H_1159b make_stream
    (cluster centers + spread-over-time onsets + gaussian jitter); the regimes
    are now points in [0,1]^5 tension space (e.g. a high-curiosity·meaning anchor
    regime vs a high-pain·authenticity anchor regime). Scaled ×4 + jitter 0.6 to
    match the H_1159b cluster separation / overlap geometry VERBATIM."""
    rng = np.random.default_rng(seed)
    centers = rng.standard_normal((k_true, DIM)) * 4.0           # tension-regime centroids
    onsets = np.linspace(0, T * 0.85, k_true).astype(int)        # regimes appear spread over time
    X = np.empty((T, DIM)); active = []; oi = 0
    for t in range(T):
        while oi < k_true and t >= onsets[oi]:
            active.append(oi); oi += 1
        c = active[rng.integers(len(active))]
        X[t] = centers[c] + rng.standard_normal(DIM) * 0.6        # anchor tension_5ch sample
    return X


# ── split/assign/mitosis machinery — VERBATIM from H_1159b ─────────────────────
def assign(lanes, x):
    d = np.linalg.norm(lanes - x[None], axis=1); j = int(np.argmin(d)); return j, float(d[j])


def run_arm(X, mode, seed):
    """mode FIXED = frozen lane set (no split, no adapt-after-warmup == H_1159b FROZEN);
       mode SPLIT = tension-driven lane mitosis (== H_1159b MITOSIS). Lanes start at 2,
       grow when a lane's running tension exceeds THETA (anchor-stream-driven)."""
    rng = np.random.default_rng(seed + 5000)
    lanes = X[:2].copy().astype(float)
    for t in range(WARMUP):
        j, _ = assign(lanes, X[t]); lanes[j] += LR * (X[t] - lanes[j])
    ten = np.zeros(len(lanes)); errs = np.empty(T - WARMUP)
    for i, t in enumerate(range(WARMUP, T)):
        x = X[t]; j, d = assign(lanes, x); errs[i] = d
        if mode == "FIXED":
            continue
        lanes[j] += LR * (x - lanes[j])
        if mode == "SPLIT":
            ten[j] += (d - ten[j]) / WIN
            if ten[j] > THETA and len(lanes) < MAX_LANES:
                daughter = lanes[j] + rng.standard_normal(DIM) * 0.3
                lanes = np.vstack([lanes, daughter[None]])
                ten = np.concatenate([ten, [0.0]]); ten[j] = 0.0
    return float(errs[-WIN:].mean()), len(lanes)


def cohen_d(x, y):
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return (np.mean(x) - np.mean(y)) / sp

def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


def main():
    np.seterr(all="ignore")
    print("=== H_1164 — kosmos lane-partition self-tuning to anchor-stream complexity ===", flush=True)
    print("LIVE-WIRING: ⏳ BLOCKED — kosmos lane == 'cell_'+cell_id passthrough "
          "(no independent lane-growth from anchor tension_5ch; a_core_engine_map)", flush=True)
    print("PROPOSAL TEST: H_1159b tension-split substrate applied to the 5-dim "
          "kosmos anchor tension_5ch stream (clearly a proposal, NOT the live partition)\n", flush=True)
    per_k = {}
    kt_flat, lc_flat = [], []
    for k in K_TRUES:
        split_err, split_lc, fixed_err = [], [], []
        for s in SEEDS:
            X = make_anchor_stream(s, k)
            e, c = run_arm(X, "SPLIT", s); split_err.append(e); split_lc.append(c)
            ef, _ = run_arm(X, "FIXED", s); fixed_err.append(ef)
            kt_flat.append(k); lc_flat.append(c)
        d_adv = cohen_d(np.array(fixed_err), np.array(split_err))
        per_k[k] = {"split_err": float(np.mean(split_err)), "fixed_err": float(np.mean(fixed_err)),
                    "split_lanecount": float(np.mean(split_lc)), "adv_cohen_d": float(d_adv),
                    "max_lc": int(np.max(split_lc))}
        print(f"  K_true={k}: split_lanes={np.mean(split_lc):.1f} split_err={np.mean(split_err):.3f} "
              f"fixed_err={np.mean(fixed_err):.3f} adv_d={d_adv:.2f}", flush=True)

    rho = spearman(kt_flat, lc_flat)
    f1 = rho >= 0.8
    f2 = all(per_k[k]["adv_cohen_d"] >= 2.0 for k in K_TRUES)
    f3 = all(per_k[k]["max_lc"] < MAX_LANES for k in K_TRUES)
    proposal_supported = bool(f1 and f2 and f3)
    verdict = {
        "H": "H_1164",
        "title": "kosmos lane-partition self-tuning to anchor-stream complexity (PROPOSAL test of the H_1159b property on the real 5-channel anchor geometry)",
        "live_wiring_verdict": "⏳ BLOCKED-WIRING",
        "live_wiring_reason": ("the live kosmos `lane` is a STATIC passthrough of the active mitosis cell_id "
                               "(AGENT/CHAT/kosmos_anchor.hexa: lane = 'cell_'+cell_id, default cell_0) — there is "
                               "NO independent partition algorithm that grows a lane-COUNT from the anchor tension_5ch "
                               "stream. The lane axis labels which cell emitted the anchor; it is not itself a "
                               "dynamically-grown partition of the anchor stream. So 'does the live lane self-tune its "
                               "count to anchor complexity?' is structurally unmeasurable — the self-tuning mechanism "
                               "is not wired (a_core_engine_map · a_kosmos). This is NOT a 🔴 no-tracking: there is no "
                               "live partition to track. To make it dynamic, a future lane axis would have to decouple "
                               "from cell_id and grow lanes from the anchor tension stream (unbuilt)."),
        "proposal_per_K_true": per_k,
        "proposal_F1_self_tuning": {"spearman_Ktrue_vs_lanecount": rho, "bar": 0.8, "pass": bool(f1)},
        "proposal_F2_advantage_all_K": {"min_adv_d": min(per_k[k]["adv_cohen_d"] for k in K_TRUES), "bar": 2.0, "pass": bool(f2)},
        "proposal_F3_self_limiting": {"max_lanecount_any_K": max(per_k[k]["max_lc"] for k in K_TRUES), "cap": MAX_LANES, "pass": bool(f3)},
        "proposal_supported": proposal_supported,
        "proposal_ruling": (
            "PROPOSAL-SUPPORTED: a tension-driven lane-partition applied to the real kosmos anchor tension_5ch (5-dim) "
            "stream WOULD self-tune its lane-COUNT to anchor-stream complexity (lane-count tracks #tension-regimes, "
            "Spearman>=0.8), stay self-limiting (no runaway to MAX_LANES), and beat a fixed-lane control at every K_true "
            "(d>=2.0). The H_1159b mitosis self-tuning property TRANSFERS to the 5-channel anchor geometry — so IF the "
            "kosmos lane axis were decoupled from cell_id and grown from the anchor stream, it would inherit self-tuning. "
            "PROPOSAL only — the LIVE lane is a static cell_id passthrough (⏳ above); live kosmos_io partition UNVERIFIED."
            if proposal_supported else
            "PROPOSAL-NOT-SUPPORTED: the tension-split substrate does NOT cleanly self-tune lane-count to anchor-stream "
            "complexity on the 5-channel anchor geometry (see which gate failed) — the H_1159b property does NOT obviously "
            "transfer to the kosmos tension_5ch dimension. PROPOSAL only; live lane is a static cell_id passthrough (⏳)."),
        "verdict": ("⏳ BLOCKED-WIRING (live) + " +
                    ("🟢 PROPOSAL-SUPPORTED" if proposal_supported else "🔴 PROPOSAL-NOT-SUPPORTED")),
        "scope": ("toy numpy $0 CPU 10 seeds, 3-point K_true ladder {3,5,8}; DIM=5 == kosmos anchor tension_5ch. "
                  "(A) LIVE kosmos lane = static cell_id passthrough → ⏳ no self-tuning mechanism wired "
                  "(a_core_engine_map · a_kosmos). (B) PROPOSAL = H_1159b tension-split substrate VERBATIM on the 5-dim "
                  "anchor tension stream — a PROXY for a hypothetical dynamic lane-partition; the live kosmos_io partition "
                  "and scale are UNVERIFIED (a_scale_honest_scope)."),
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1164_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__": main()
