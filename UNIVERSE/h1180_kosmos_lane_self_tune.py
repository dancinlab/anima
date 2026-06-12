"""
H_1180 — does the kosmos LANE-count self-tune to anchor-stream COMPLEXITY, with
an EXPLICIT SATURATION knee and a SHUFFLE control (the two clauses H_1164's
proposal did NOT test)?

CONTEXT — what is already known (do NOT re-litigate):
  · H_1164 LIVE-WIRING = ⏳ BLOCKED: the live kosmos `lane` is a STATIC passthrough
    `lane = "cell_" + cell_id` (AGENT/CHAT/kosmos_anchor.hexa) — there is NO live
    partition that grows a lane-COUNT from the anchor tension_5ch stream. That stays
    BLOCKED here (a_core_engine_map · a_kosmos); H_1180 does NOT claim to test it live.
  · H_1164 PROPOSAL = 🟢: the H_1159b tension-split substrate, fed the 5-channel
    anchor geometry, gave Spearman(K,lanecount)=0.881, advantage d>=6.48, max-lane
    bounded. That established monotone-rise + advantage + a max bound.

WHAT H_1180 ADDS (a genuinely new measurement, not a repeat):
  H_1164's proposal showed rise-and-bounded; it did NOT show (a) an explicit
  SATURATION KNEE on a FINER K ladder (does lane-count flatten as K outgrows the
  channel geometry, i.e. self-LIMITING beyond a knee, not merely below a hard cap?),
  nor (b) a SHUFFLE CONTROL (anti-Goodhart: if the partition tracks REAL stream
  complexity it must FAIL to track K when the temporal regime-onset structure is
  destroyed by shuffling — otherwise lane-count is just counting samples, not
  complexity). Both are the missing legs of "tracks complexity, self-limiting".

SUBSTRATE — reuse h1159b VERBATIM (import, do not re-derive): make_stream / run_arm
  / assign / cohen_d / spearman. ONLY change: DIM 8 -> 5 (the kosmos tension_5ch
  geometry, exactly as H_1164's proposal), and a FINER K ladder {2,3,4,5,6,8,10,12}
  to expose a knee. "lane-count" == the MITOSIS-arm final cell-count (the proposed
  lane = a grown partition of the anchor stream).

FROZEN FALSIFIER (pre-registered BEFORE measuring, deterministic 10 seeds, g5/p7):
  F1 TRACKS-COMPLEXITY: Spearman(K_true, lane-count) >= 0.8 on the REAL (onset-
     structured) anchor stream.
  F2 SATURATION/SELF-LIMITING: lane-count is CONCAVE-saturating, not linear — the
     marginal lane gain over the TOP half of the K ladder is < 0.6 x the marginal
     gain over the BOTTOM half (the rise flattens = a knee, self-limiting beyond
     the channel geometry, not runaway). [knee, frozen ratio bar = 0.6]
  F3 SHUFFLE-CONTROL (anti-Goodhart): on a TEMPORALLY-SHUFFLED anchor stream (same
     samples, regime-onset structure destroyed), lane-count must NOT track K —
     Spearman_shuffled < 0.5 AND clearly below F1's real Spearman (real - shuffled
     >= 0.3). If shuffled tracks K just as well, lane-count is counting samples not
     complexity -> the self-tuning claim is Goodharted.
  SUPPORTED (PROPOSAL tier) iff F1 & F2 & F3 -> the proposed kosmos lane-partition
     self-tunes to ANCHOR-STREAM COMPLEXITY (not sample count), saturating.
  CLOSED-NEGATIVE if any gate fails (a_paper_negative_ok).

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map): this is a PROPOSAL test on
  the 5-channel anchor GEOMETRY, NOT the live kosmos lane (which is cell_id
  passthrough = ⏳ BLOCKED, unchanged from H_1164). toy numpy $0 CPU. If F1-F3 pass,
  the finding is "the self-tuning property TRANSFERS to anchor complexity AND is
  shuffle-discriminating + saturating IF the live lane were decoupled from cell_id".
"""
import json, math, sys, os
import numpy as np

# ── reuse h1159b VERBATIM (import, do not re-derive) ──────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h1159b_mitosis_capacity_self_tuning as H59B
from h1159b_mitosis_capacity_self_tuning import run_arm, assign, cohen_d, spearman

# ── kosmos tension_5ch geometry: ONLY change DIM 8 -> 5 (cf H_1164 proposal) ──
H59B.DIM = 5
N_SEEDS = 10
SEEDS = list(range(800, 800 + N_SEEDS))
# finer K ladder to expose a saturation KNEE (H_1164 used only {3,5,8}).
K_LADDER = [2, 3, 4, 5, 6, 8, 10, 12]


def make_anchor_stream(seed, k_true, shuffle=False):
    """h1159b make_stream at DIM=5 (kosmos tension_5ch); shuffle=True destroys the
    temporal regime-ONSET structure (anti-Goodhart control) while keeping the exact
    same samples."""
    X = H59B.make_stream(seed, k_true)   # VERBATIM h1159b stream at DIM=5
    if shuffle:
        rng = np.random.default_rng(seed + 99991)
        idx = rng.permutation(X.shape[0])
        X = X[idx]
    return X


def lane_count_for(seed, k_true, shuffle):
    X = make_anchor_stream(seed, k_true, shuffle=shuffle)
    # MITOSIS arm == the proposed lane-partition; final cell-count == lane-count.
    _, lane_count = run_arm(X, "MITOSIS", seed)
    return lane_count


def main():
    np.seterr(all="ignore")
    print("=== H_1180 — kosmos LANE-count self-tunes to anchor complexity (saturation + shuffle control) ===", flush=True)
    print(f"DIM={H59B.DIM} (kosmos tension_5ch) · K ladder={K_LADDER} · seeds={SEEDS} · MAX_CELLS={H59B.MAX_CELLS}", flush=True)
    print("(PROPOSAL on 5-ch anchor geometry; live lane = cell_id passthrough = BLOCKED, cf H_1164)", flush=True)
    print("", flush=True)

    real_k, real_lc = [], []
    shuf_k, shuf_lc = [], []
    mean_lc_real, mean_lc_shuf = {}, {}

    for k in K_LADDER:
        lcs_r, lcs_s = [], []
        for s in SEEDS:
            lcs_r.append(lane_count_for(s, k, shuffle=False))
            lcs_s.append(lane_count_for(s, k, shuffle=True))
        for v in lcs_r:
            real_k.append(k); real_lc.append(v)
        for v in lcs_s:
            shuf_k.append(k); shuf_lc.append(v)
        mean_lc_real[k] = float(np.mean(lcs_r))
        mean_lc_shuf[k] = float(np.mean(lcs_s))
        print(f"  K_true={k:2d}: REAL lane-count={np.mean(lcs_r):.2f}  SHUFFLED lane-count={np.mean(lcs_s):.2f}", flush=True)

    print("", flush=True)

    # ── F1: tracks complexity on the REAL onset-structured stream ─────────────
    rho_real = spearman(real_k, real_lc)
    f1 = rho_real >= 0.8

    # ── F2: saturation / self-limiting — marginal gain top-half < 0.6 * bottom-half
    ks = K_LADDER
    mid = len(ks) // 2
    lc = [mean_lc_real[k] for k in ks]
    # marginal gain per unit-K over bottom vs top half of the ladder.
    bot_gain = (lc[mid] - lc[0]) / (ks[mid] - ks[0])
    top_gain = (lc[-1] - lc[mid]) / (ks[-1] - ks[mid])
    sat_ratio = (top_gain / bot_gain) if bot_gain > 1e-9 else 99.0
    f2 = sat_ratio < 0.6

    # ── F3: shuffle control (anti-Goodhart) ───────────────────────────────────
    rho_shuf = spearman(shuf_k, shuf_lc)
    f3 = (rho_shuf < 0.5) and ((rho_real - rho_shuf) >= 0.3)

    supported = bool(f1 and f2 and f3)

    print(f"F1 TRACKS-COMPLEXITY  Spearman_real(K, lane-count) = {rho_real:.3f}  (bar>=0.8)  pass={f1}", flush=True)
    print(f"F2 SATURATION         bottom-half gain={bot_gain:.3f}/K  top-half gain={top_gain:.3f}/K  ratio={sat_ratio:.3f}  (bar<0.6)  pass={f2}", flush=True)
    print(f"F3 SHUFFLE-CONTROL    Spearman_shuffled={rho_shuf:.3f} (bar<0.5)  real-shuf={rho_real - rho_shuf:.3f} (bar>=0.3)  pass={f3}", flush=True)
    print("", flush=True)

    verdict = {
        "H": "H_1180",
        "title": "kosmos lane-count self-tunes to anchor-stream complexity — saturation knee + shuffle control (PROPOSAL on 5-ch geometry; live lane = cell_id passthrough = BLOCKED cf H_1164)",
        "live_wiring_verdict": "⏳ BLOCKED-WIRING (unchanged from H_1164): live kosmos lane = 'cell_'+cell_id passthrough (AGENT/CHAT/kosmos_anchor.hexa), no live partition grows a lane-count from the anchor tension_5ch stream (a_core_engine_map · a_kosmos)",
        "dim": H59B.DIM,
        "k_ladder": K_LADDER,
        "mean_lane_count_real": mean_lc_real,
        "mean_lane_count_shuffled": mean_lc_shuf,
        "F1_tracks_complexity": {"spearman_real": rho_real, "bar": 0.8, "pass": bool(f1)},
        "F2_saturation": {"bottom_half_gain_per_K": bot_gain, "top_half_gain_per_K": top_gain, "ratio": sat_ratio, "bar": 0.6, "pass": bool(f2)},
        "F3_shuffle_control": {"spearman_shuffled": rho_shuf, "bar_below": 0.5, "real_minus_shuffled": rho_real - rho_shuf, "bar_gap": 0.3, "pass": bool(f3)},
        "supported_proposal": supported,
        "ruling": ("PROPOSAL-SUPPORTED: the proposed kosmos lane-partition self-tunes its COUNT to anchor-stream COMPLEXITY (not sample count) — tracks K (Spearman>=0.8), SATURATES beyond the channel geometry (concave, top-half marginal gain < 0.6x bottom-half), and is shuffle-DISCRIMINATING (a temporally-shuffled stream does NOT track K), so lane-count reads real regime structure not raw sample count. The H_1159b self-tuning property TRANSFERS to the 5-channel anchor geometry AND survives the two clauses H_1164 left untested. (Live lane stays ⏳ BLOCKED: it is cell_id passthrough; decouple from cell_id to make this live.)"
                   if supported else
                   "CLOSED-NEGATIVE (proposal): the lane-partition does NOT cleanly self-tune+saturate+shuffle-discriminate (see failed gate); a_paper_negative_ok"),
        "scope": "PROPOSAL on the 5-channel anchor GEOMETRY (h1159b substrate VERBATIM, DIM 8->5), NOT the live kosmos lane (cell_id passthrough = BLOCKED). toy numpy $0 CPU 10 seeds. a_scale_honest_scope · a_core_engine_map · a_kosmos.",
    }
    print("=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
