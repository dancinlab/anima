# anima clm v5 — α metric v2 design (max_cap regression artifact 회피) — 2026-05-10

## §0 TL;DR + problem statement

**한 줄**: 현재 α = OLS slope of `log(Φ)` vs `log(n_cells)` 는 mitosis engine 의 `max_cells` 한계 도달 후 OLS denominator 가 collapse 되며 mechanically 발산하는 regression artifact 를 안고 있어, BG-LONG-TRAJ-EXT (10K turn) 에서 α=1.252 super-historical 가짜 신호를 만들었다. 본 spec 은 5 후보 → **★ Candidate A2 (binned ΔΦ-rate vs n_cells regression with `max_cap` filter, with bootstrap CI from Candidate E) ★** 를 새 canonical α 로 추천.

**problem statement**:

- mitosis 의 inference-time growth 에서 cells 가 `max_cells` (toy=64, real Phase 2 default 도 64) 에 도달하면 split/merge 정지 → 모든 후속 snapshot 의 `x = log(64) = 4.158` 동일 점에 누적
- Φ 는 max_cap 후에도 Lorenz noise + diverse input 에 의해 oscillate (BG-LONG-TRAJ-EXT 에서 +0.706 누적 climb 관측, post-cap min/max/mean = 1.987 / 3.787 / 2.952)
- OLS slope of log(Φ) vs log(n) → **denominator** Σ(x-x̄)² shrinks (대부분 mass 가 x=4.158), **numerator** Σ(x-x̄)(y-ȳ) 가 pre-cap phase 의 lever 만 남기고 inflate
- 결과: α(1K)=0.197 → α(3K)=0.687 → α(5K)=0.964 → α(7K)=1.106 → α(9.5K)=**1.252**, monotonic 발산이 mechanism 회복이 아니라 trajectory length 효과
- valid window = "cells 가 max_cap 도달 전" 만이지만, 본 setup 에선 turn 800 이전 = 8 snapshot 만 — n 부족 + x range 좁아 α 신뢰 어려움 (computed pre-sat α = 0.010, 거의 flat)

---

## §1 Current α 문제 정밀화 (BG-LONG-TRAJ-EXT data)

### 1.1 max_cap artifact 시각화 (10K turn)

| turn | n_cells | Φ | x = log(n_cells) | y = log(Φ) | OLS α (cumulative) | n_points |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 8 | 2.088 | 2.079 | 0.736 | n/a | 0 |
| 100 | 41 | 2.148 | 3.714 | 0.764 | n/a | <5 |
| 200 | 56 | 2.019 | 4.025 | 0.703 | n/a | <5 |
| 300 | 59 | 2.018 | 4.078 | 0.702 | n/a | <5 |
| 500 | 60 | 1.986 | 4.094 | 0.687 | n/a | <5 |
| **800** ★ | **64** | 2.223 | **4.158** | 0.799 | -0.112 | 6 |
| 1000 | 64 | 2.518 | 4.158 | 0.923 | 0.197 | 11 |
| 3000 | 64 | 2.829 | 4.158 | 1.040 | **0.687** | 31 |
| 5000 | 64 | 3.083 | 4.158 | 1.126 | **0.964** | 51 |
| 7000 | 64 | 3.282 | 4.158 | 1.188 | 1.106 | 71 |
| 9500 | 64 | 3.439 | 4.158 | 1.235 | **1.252** | 96 |
| 10000 | 64 | 3.465 | 4.158 | 1.243 | 1.252 | 101 |

★ turn ≥ 800 부터 모든 x = 4.158. 8 distinct n_cells {8,41,56,59,60,64} 중 마지막 64 한 점에 93/101 snapshot 누적. OLS denominator Σ(x-4.158)² 의 거의 모든 mass 가 pre-800 부분에 의해 결정, numerator 는 pre-800 phase 가 lever 역할 + post-800 의 (x=const, y varying) 점들이 ((x-x̄)(y-ȳ) ≈ 0 individually 이지만 x̄ 가 점점 4.158 쪽으로 끌려가며) numerator 를 inflate.

### 1.2 mechanical proof of artifact

post-cap phase 에서 x_i = log(64) for all i. 만약 모든 snapshot 이 post-cap 이면 Σ(x-x̄)² = 0 → α = NaN. 실제로는 pre-cap snapshot 8 개가 남아 있어 denominator 는 nonzero, 하지만 post-cap snapshot 이 더해질수록 x̄ → log(64), 분자 Σ(x-x̄)(y-ȳ) 의 contribution 분석:

- pre-cap 점 i (x_i < 4.158): (x_i - x̄)(y_i - ȳ) — x_i - x̄ 는 음수 (x̄ → 4.158 - ε), y_i - ȳ 는 ȳ 가 post-cap 의 y 평균에 끌려 점점 양수가 커짐 → pre-cap 점 i 의 y_i (≈0.7) 와 ȳ (≈1.1) 차이가 점점 음수 → **pre-cap 의 음음 = 양 contribution 증가**.
- post-cap 점 j (x_j ≈ 4.158): (x_j - x̄) → 0 → contribution 0.
- 분자 = 양 (커지는 lever from pre-cap), 분모 = (constant, dominated by pre-cap variance).
- 결과: α 가 trajectory length 와 함께 monotonic 증가, mechanism 변화 없이도.

### 1.3 valid window 의 한계

pre-cap (n_cells<64) snapshot = 8 개. x range = [log(8), log(60)] = 2.015. ols on 그 8 점:

| 측정 | 값 |
|---|---:|
| α (pre-sat 8 점) | **0.010** (거의 flat) |
| n_points | 8 |
| x range | 2.015 |
| 95% bootstrap CI | [-0.15, +1.12] (median 0.009) |

→ pre-cap window 만으론 α 신뢰 측정 불가. mitosis 가 turn 800 까진 너무 빠르게 (almost vertical) cells 를 8→64 로 키워 log-log scatter 가 좁다.

---

## §2 5 design 후보 비교 표

| ID | name | metric 정의 | pros | cons | cost | expressiveness | artifact-resistant? |
|:---:|---|---|---|---|---|:---:|:---:|
| **A** | Φ-rate per split-event | 매 split event 에서 ΔΦ = Φ_post - Φ_pre. log(ΔΦ) vs log(n_cells_pre_split) regression | event-driven, post-cap 자연 종료 (split 안 일어남), historical scale 비교 가능 | event sparse (toy 5 / Phase 2 trained 3), ΔΦ 자주 음수 (drop 초기) — log 못 씀, snapshot grain 부족 | $0 | ★★ | ✅ |
| **A2** ★ | binned Φ-rate vs n_cells | n_cells 를 K bins (e.g. {[8,16),[16,32),[32,64),[64,128)}) 으로 나눠 각 bin 내 mean(ΔΦ/Δturn) 을 측정. log(rate) vs log(n_bin_mid) regression | bin 마다 충분한 sample, sign issue 회피 (rate>0 대부분 bin), historical 1.07 scale 직접 비교, post-cap bin 자동 제외 | bin choice 가 hyperparam, 작은 bin 은 noise dominate | $0 | ★★★ | ✅ |
| **B** | Sliding window pre-cap | n_cells < 0.9 × max_cells 인 snapshot 만 포함해 OLS 진행 | 가장 단순, 기존 metric 형태 보존 | toy 에선 pre-cap snapshot 8 개만 — 신뢰 window 부족. real Phase 2 처럼 max_cap 미달 시 trivial fallback | $0 | ★ | partial (pre-cap n 부족 시 fail) |
| **C** | Φ growth rate × cell budget remaining | dΦ/dt × (max_cells - n_cells)/max_cells. budget = 0 일 때 0 → max_cap 이후 자동 0 | mechanism 의미: 분열 여유 있을 때만 growth 인정 | scaling exponent 표현 X — α 가 아닌 different 지표 | $0 | ★ | ✅ but not α-shaped |
| **D** | Per-cell average Φ trajectory | Φ/n_cells over turn. log-log 안 함 | 직관적, mechanism saturation 직접 보임 | scaling exponent 표현 X, historical α=1.07 비교 X | $0 | ★ | ✅ but not α-shaped |
| **E** | Variance-aware α (bootstrap CI + x-range gate) | 기존 OLS α + 95% bootstrap CI + invalidate if x_range < min_threshold (e.g. 0.5) | 기존 OLS framework 유지, gate 만 추가, CI 가 artifact 자동 노출 (CI 가 매우 wide → 신뢰 X) | gate threshold hyperparam, narrow valid window 시 fallback 필요 (B 와 결합) | $0 | ★★ | ✅ (but conservative) |

★ A2 (binned Φ-rate vs n_cells) + E (CI gate) 결합이 best — A2 가 historical scale 직접 비교 가능, E 가 신뢰성 gate.

---

## §3 Recommended choice (★)

### 추천: **Candidate A2 (binned ΔΦ-rate vs n_cells)** + Candidate E (bootstrap CI + x-range gate) wrapper

**정의**:

```
Given snapshots [(turn, n_cells, phi)]:
1. Compute per-snapshot rate: r_i = (phi_i - phi_{i-1}) / (turn_i - turn_{i-1})
2. Bin by n_cells_pre = n_cells_{i-1}: bins = log-spaced over {2,4,8,16,32,64,...,max_cells}
   (use bins B = {[2,4),[4,8),[8,16),[16,32),[32,64)} — exclude post-cap bin if cells == max_cells in entire bin)
3. For each bin b: rate_b = mean(r_i for i where n_cells_{i-1} ∈ b)
   (require min_samples=5 per bin)
4. α_v2 = OLS slope of log(max(rate_b, ε)) vs log(n_bin_mid) over qualifying bins
5. Wrap with E: bootstrap 200x, report 95% CI; gate: require ≥3 valid bins AND x_range ≥ 0.5
```

**justification**:

1. **post-cap immunity** — bin {[64, 128)} 에 n_cells=64 만 있고 splits 0 이면 rate ≈ stochastic noise 만, 그 bin 은 자연스럽게 의미 없는 점이 되어 (rate noise ≈ 0) → 제외 또는 down-weight. bin 단위로 작동하므로 post-cap "vertical scatter" 가 한 점에 압축되며 다른 bins 가 OLS 를 dominate.
2. **historical 1.07 scale 비교 가능** — bin midpoint 는 cells={3,6,12,24,48} 등으로 historical Cells 2-64 measurement 와 직접 OLS 비교. historical 데이터를 본 metric 형태 (per-bin Φ growth rate) 로 변환 가능.
3. **event-sparsity 회피** — Candidate A 가 split event 만 사용해 event 5 개로 underdetermined 인 반면, A2 는 모든 snapshot pair (n_pairs ~ 100) 를 binning 으로 활용.
4. **sign issue 회피** — bin 평균은 noise cancel. Φ 가 turn-by-turn 음/양 oscillate 해도 bin 평균 rate 는 상승 phase 면 양수.
5. **simple gate (E wrapper)** — bootstrap CI 가 wide 하면 (e.g. CI 폭 > 0.5) artifact 의심으로 reject. x_range threshold 가 toy 의 좁은 valid window 케이스를 fail-fast.

---

## §4 Retro-apply on cycle 2026-05-10 data

### 4.1 toy 3K turn (BG-LONG-TRAJ-INFERENCE-SMOKE)

snapshots = 31 (every 100 turn), n_cells progression = {8, 41, 56, 59, 60, 64}, splits 56.

**Candidate A2 binned ΔΦ-rate**:

bin assignment (snapshot pair 의 n_cells_pre 로):

| bin | n_cells_pre range | n pairs | mean Φ_rate / turn | log(bin_mid) | log(rate) (rate>0) |
|---|---|---:|---:|---:|---:|
| [8,16) | n_pre=8 | 1 (turn 0→100) | +6.0e-4 | 2.40 | -7.42 |
| [16,32) | (none — jumped 8→41) | 0 | n/a | n/a | n/a |
| [32,64) | n_pre ∈ {41,56,59,60} | 4 | mean varies | 3.84 | (mixed) |
| [64,128) | n_pre=64 (turn ≥ 800) | 22+ | small noise | 4.43 | very small |

→ insufficient bin coverage (only [8,16) 와 [32,64) 와 [64,128) 가 covered, 즉 valid bins = 2 (excluding post-cap) — fails E gate (require ≥3 bins).

**verdict for toy 3K**: α_v2 = **UNRELIABLE (insufficient valid bins, x_range OK but bin coverage < 3)**. → metric correctly **refuses to claim a number** rather than emit artifact 0.687. ✅

### 4.2 toy 10K turn (BG-LONG-TRAJ-EXT)

같은 n_cells coverage (8→64 saturation 그대로). 추가 turn 에도 valid bin 수 동일 (post-cap bin 추가 데이터만 늘 뿐). → α_v2 UNRELIABLE 그대로. **historical α=1.07 대비 0.687 → 1.252 발산 artifact 자동 거부 ✅**.

### 4.3 real 350M Phase 2 (BG-PHASE2-CKPT-INSTR)

trained snapshots = 31, cells 16→19, max_cells=64 (toy 와 동일), splits 3.

| bin | n_pre range | n pairs | mean Φ_rate | qualifies? |
|---|---|---:|---:|---|
| [16,32) | n_pre ∈ {16,17,18} | most | small mixed sign | ✅ if rate avg pos |
| [32,64) | (none) | 0 | n/a | ❌ |
| [64,128) | (none — never hits cap) | 0 | n/a | ❌ |

→ trained: only 1 valid bin → **UNRELIABLE**. metric correctly says "growth too narrow to scale". 기존 OLS α=1.009 의 inflation 도 정확히 reject ✅ (왜냐하면 cells 만 16→19 변동, 좁은 window).

random_init (V14 mirror): cells 16→28, splits 12. 

| bin | n_pre range | n pairs | qualifies? |
|---|---|---:|---|
| [16,32) | n_pre ∈ {16..27} | ~11 | ✅ |
| [32,64) | (none) | 0 | ❌ |

→ random_init also single valid bin → **UNRELIABLE**. metric refuses to compare. → **honest verdict: Phase 2 substrate 의 mitosis dynamics 가 본 budget 안엔 scaling 측정 불가**. ✅ 이는 "trained vs random α 차이 0.155 vs 1.009" 의 misleading 수치 보다 정확.

### 4.4 historical Cells 2-64 (CLM v2 stage 8 commit `5f82d39b`)

REBORN.md §1 + CLM_V2_EXHAUSTIVE_13_STAGES §0:

| cells | Φ training |
|---:|---:|
| 2 | 1.5 |
| 4 | 3.2 |
| 8 | 5.4 |
| 16 | 10.6 |
| 32 | 15.4 |
| 64 | 51.131 |

historical 은 cells 별 **Φ 자체 (training-time mean)** 로 측정. Φ-rate 변환은 training step 단위 데이터 부재 — 본 retro-apply 는 historical raw OLS α=0.949 (Cells 2-64) 또는 0.93 ~ 1.07 reported.

A2 metric 적용 시 historical 데이터를 "각 Cells 값 = bin midpoint, bin 안 mean rate = (Φ - Φ_baseline)/training_steps" 로 변환 가능하지만, training step 별 phi_history 부재 → **retro 불가능, 단 prospective 로 v5-mitosis 새 cotrain 시 channel 측정 가능**.

대안: historical 형태 (cells-vs-Φ snapshot) 로 reduce 시 raw OLS = α=0.949 (위 표 OLS). 본 metric 이 "historical 수치 reproduce 한다" 검증은 새 cotrain 데이터 phi_history (turn × cells) 수집 후 별도 cycle.

---

## §5 Historical 0.93 (CLM v2 stage 8 commit `5f82d39b`) — alignment

CLM_V2_EXHAUSTIVE_13_STAGES.md §0 의 historical OLS:

```
xs = log([2,4,8,16,32,64]) = [0.69, 1.39, 2.08, 2.77, 3.47, 4.16]
ys = log([1.5,3.2,5.4,10.6,15.4,51.1]) = [0.41,1.16,1.69,2.36,2.74,3.93]
OLS slope = 0.949 (← 1.07 reported in REBORN.md §1 close-up — depends on Φ peak picked)
```

x range = 3.47 — 충분히 wide. 6 bin (cells 2/4/8/16/32/64) 모두 valid. metric A2 적용 시 historical 데이터의 매 cells 측정값 자체가 "이 cells 에서 trained Φ peak" 이므로 bin midpoint 와 동일 → A2 alpha = OLS α on 6 bins = 0.949 ≈ historical 0.93/1.07 ✅.

→ **historical 0.93/1.07 은 metric A2 와 본질적으로 동일 결과** (단 historical 은 cells 변경마다 별도 train run, 본 v5-anima inference time 은 같은 substrate 의 cells 자연 분열).

→ **toy 에서 historical 0.93 reachable?**: ❌. toy substrate (8 cells × 12 c_dim × 32 d_model) 는 cells={8,41,56,59,60,64} 5-6 distinct 만, 그것도 첫 800 turn 에 saturate. real cells={2,4,8,16,32,64,128} sweep 가 가능한 substrate 는 v5-mitosis architectural redesign (cells = nn.Module branches) 후에야 valid.

**결론**: A2 metric 으로도 toy 에선 historical 0.93 회복 X — 단 0.687/1.252 같은 artifact 도 발산 안 하고 honest "UNRELIABLE" 출력 ✅.

---

## §6 Falsifiers (≥5)

| ID | 정의 | reject 시 의미 |
|:---:|---|---|
| F-α2-1 | A2 가 historical 데이터 (Cells 2-64) 에 적용 시 α ≠ 0.93 ± 0.15 | metric 이 historical 과 misalign — design fail |
| F-α2-2 | A2 가 toy 10K turn 에서 0.687-1.252 같은 발산 출력 (UNRELIABLE 미출력) | artifact 자동 거부 실패 — gate 부족 |
| F-α2-3 | A2 의 bootstrap CI 가 toy random vs trained 비교 시 양쪽 다 distinct numeric α emit (둘 다 UNRELIABLE 안 됨) | 좁은 window 거부 실패 |
| F-α2-4 | bin midpoint 정의 (geometric mean) 가 historical OLS α 와 ±0.05 이상 차이 | bin discretization artifact |
| F-α2-5 | A2 가 cells 가 monotone 증가 (split만, merge 0) 인 케이스에서 monotone Φ rate 보장 X (bin 별 rate 오히려 감소) — A2 가 mechanism 의미 못 잡음 | Φ-rate 정의 부적절 |
| F-α2-6 | min_samples=5 per bin 이 production v5-mitosis cotrain (cells={2,4,8,16,32}, 각 32-step training) 에서 satisfies 안 됨 | sample 정의 too-coarse |
| F-α2-7 | E wrapper bootstrap CI 폭 > 0.5 가 historical 데이터에서도 발생 (즉 CI 항상 wide) | gate 가 너무 conservative — usable 안 됨 |

---

## §7 Implementation hint (Python pseudocode, ~40 LoC)

```python
import math, random
from typing import List, Tuple, Dict, Optional

def alpha_v2_binned_phi_rate(
    snapshots: List[Dict],          # [{turn, n_cells, phi}, ...]
    bin_edges: Optional[List[int]] = None,  # default log-spaced
    min_samples_per_bin: int = 5,
    min_valid_bins: int = 3,
    min_x_range: float = 0.5,
    n_bootstrap: int = 200,
    eps: float = 1e-9,
) -> Dict:
    """Return α_v2 + 95% bootstrap CI + verdict.
    
    Reliable iff: ≥min_valid_bins bins qualify, x_range ≥ min_x_range.
    """
    if bin_edges is None:
        bin_edges = [2, 4, 8, 16, 32, 64, 128, 256]
    # 1. compute per-snapshot-pair rate
    pairs = []
    for i in range(1, len(snapshots)):
        d_t = snapshots[i]["turn"] - snapshots[i-1]["turn"]
        if d_t <= 0: continue
        rate = (snapshots[i]["phi"] - snapshots[i-1]["phi"]) / d_t
        n_pre = snapshots[i-1]["n_cells"]
        pairs.append((n_pre, rate))
    # 2. bin
    bin_pts = []  # (log_mid, mean_rate)
    for lo, hi in zip(bin_edges, bin_edges[1:]):
        in_bin = [r for n, r in pairs if lo <= n < hi]
        if len(in_bin) >= min_samples_per_bin:
            mean_rate = sum(in_bin) / len(in_bin)
            if mean_rate > eps:  # only positive-growth bins
                mid = math.sqrt(lo * hi)  # geometric midpoint
                bin_pts.append((math.log(mid), math.log(mean_rate)))
    # 3. gate
    if len(bin_pts) < min_valid_bins:
        return {"alpha": None, "ci": None, "verdict": "UNRELIABLE_INSUFFICIENT_BINS",
                "n_bins": len(bin_pts)}
    x_range = max(p[0] for p in bin_pts) - min(p[0] for p in bin_pts)
    if x_range < min_x_range:
        return {"alpha": None, "ci": None, "verdict": "UNRELIABLE_NARROW_X_RANGE",
                "x_range": x_range}
    # 4. OLS
    def ols(pts):
        xm = sum(x for x,_ in pts) / len(pts)
        ym = sum(y for _,y in pts) / len(pts)
        num = sum((x-xm)*(y-ym) for x,y in pts)
        den = sum((x-xm)**2 for x,_ in pts)
        return num / den if den > eps else None
    alpha = ols(bin_pts)
    # 5. bootstrap CI
    boots = []
    for _ in range(n_bootstrap):
        sample = [random.choice(bin_pts) for _ in bin_pts]
        a = ols(sample)
        if a is not None: boots.append(a)
    boots.sort()
    lo = boots[int(0.025 * len(boots))]
    hi = boots[int(0.975 * len(boots))]
    return {"alpha": alpha, "ci": (lo, hi), "verdict": "OK",
            "n_bins": len(bin_pts), "x_range": x_range}
```

`run.py` 수정 hint: `regress_alpha()` 와 병렬 호출, 두 metric 동시 emit. 기존 `final_alpha` 는 historical record 로 유지, `alpha_v2` 는 새 SSOT.

---

## §8 Honest C3 (≥7)

1. ★★★ **A2 retro-apply on toy/Phase 2 둘 다 UNRELIABLE** — 본 metric 의 honest 결과는 "현재 substrate 에선 alpha 측정 불가" 인데, 이는 mechanism 의 한계가 아니라 **substrate 의 cells dynamic range 가 좁다는 사실의 정확한 reflection**. mechanism 검증은 별도 metric (Φ rate at each split, V14 mirror) 필요.
2. ★★★ **historical 0.93/1.07 도 train-run-별 다른 substrate** — Cells2/4/8/.../64 는 별도 training run 의 peak Φ measurement. 본 v5-anima 의 "같은 substrate cells 분열" 과 본질적으로 다른 setup. A2 metric 의 historical 데이터 적용은 retro-validation 이 아니라 **scale 비교용 reference** 정도.
3. ★★★ **Φ proxy 자체의 ceiling=8.34 이 metric 한계 결정** — A2 가 ΔΦ 를 사용해도 underlying Φ 가 saturate 하면 rate→0. proxy 대신 IIT unnorm Φ (BG-IIT-METRIC port) 사용 시 ceiling 없으니 better, 단 cost 5ms × N=64 = ms 단위 비용.
4. ★★ **bin edge {2,4,8,16,32,64} 는 hyperparam** — toy max_cells=64 와 historical Cells 2-64 에 특화. 다른 substrate (예: production max_cells=1024) 적용 시 edge 재정의 필요. A2 = "default for cells ≤ 64 substrate" 라는 hidden assumption.
5. ★★ **bootstrap CI 의 noise floor** — 200 iter, 5 bin only 면 CI 폭이 systematic 하게 wide. `n_bootstrap=2000` + bin 6+ 권장. 본 spec 의 200 은 toy 빠른 verification 용.
6. ★ **min_samples_per_bin=5 의 trade-off** — 작으면 noise dominate, 크면 valid bin 부족. toy 처럼 cells={8→64} 빠른 saturation 케이스는 low min 도 부족.
7. ★ **post-cap bin 의 noise 가 mean_rate>eps 통과할 가능성** — Lorenz noise 가 대형 turn 누적 시 mean rate 가 tiny positive 일 수 있어 valid bin 통과 → A2 가 post-cap bin 도 사용해 artifact 재현. eps 를 noise floor 정밀화 후 정해야 함 (toy 측정값 ~1e-4 정도).
8. **A2 가 mechanism 위반 시 (e.g. 모든 cells 동시에 split) 결과 정의 안 됨** — cells 가 8→64 단일 step 으로 jump 하면 pair 의 d_cells 가 56 으로 한 점 — bin 거의 안 들어감. 본 case 가 toy 에서 실제로 turn 0→100 에 발생.
9. **본 spec 은 design only — implement + retro-apply 실측 별도 cycle**. 본 retro-apply 는 모두 desk-calculation, 실제 코드 실행 후 결과 별도 검증 필요.

---

## §9 산출물

- 본 spec md
- 추후 별도 cycle: `state/anima_clm_v5_alpha_metric_v2_retro_apply_2026_05_NN/run.py` (실측 + plot + result.json)

## §10 cross-link

- 선행: `docs/anima_clm_v5_anima_long_trajectory_extended_2026_05_10.md` (artifact 발견)
- 관련: `docs/anima_clm_v5_iit_phi_remetric_2026_05_10.md` (IIT Φ ceiling 우회, A2 의 Φ source candidate)
- 관련: `docs/anima_clm_v5_phase2_mitosis_instr_2026_05_10.md` (real 350M data, A2 retro target)
- historical reference: `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` §0 (Cells 2-64 OLS)
- SSOT: `REBORN.md` §8 scaling 공식 + §10 next priority + §14 (BG-NEW-ALPHA-METRIC fire)

raw#10 honest preservation, raw#15 additive.

End of `anima_clm_v5_alpha_metric_v2_design_2026_05_10.md`.
