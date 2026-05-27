---
spec_id: nexus6_1013lens_f2_null_synthesis_2026_05_12
parent_spec: state/nexus6_1013lens_activation_2026_05_11/spec.md
parent_plan: state/nexus6_1013lens_activation_2026_05_11/cascade_k25_plan_2026_05_12.md
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
status: design-only (NO actual MC/bootstrap run)
cycle: 5 §4 #I
authored: 2026-05-12
authored_by: agent
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# F2 Random-Walk Null Distribution — Synthesis Method Decision

cascade_k25_plan §3.1 (Agent 25) 의 F2 falsifier "random-walk null distribution 합성 방법"
미결정 stub 을 본 spec 에서 정식 결정. cycle 5 §3 #A (Agent 21) TRIVIAL finding — lens 가
input channel 부재 → 본 spec 은 *lens channel reimpl 완료* (Agent #F Phase 1) *후* actionable.

## 0. Context

| ref | finding | impact |
|-----|---------|--------|
| cascade_k25_plan §3 F2 | "K=25 score 분포 vs random null KS-test p ≥ 0.05" trip 조건 | null 합성 미결정 |
| cascade_k25_plan §3.1 | MC/analytic/bootstrap 3 option 열거, default=MC | 본 spec 정식 결정 보강 |
| smoke_k10_caveat §4 | x 입력 채널 부재 → "lens vs random walk" control 정의 불가 | lens reimpl 선결 (L1) |
| numerology simulate.py | seed=0xC0FFEE4E36, K=10_000, per-n deterministic | 본 cycle MC 정합 baseline |

## 1. 3 Path 비교

| path | method | pros | cons | wall (K=25) | prereq | applicable |
|------|--------|------|------|------------:|--------|------------|
| **MC** | shuffled-x 로 lens score N trial 재계산 | non-parametric, actual channel 사용, seed reproducible | K=25 × N=1000 × 19ms ≈ 8min, shuffle 방법 결정 필요 | ~5s (N=100), ~8min (N=1000) | lens channel reimpl | K=25 phase |
| **analytic** | distribution form 가정 (Gaussian/Beta/binomial) | zero run wall, parametric purity, scaling 무한 | form 미지, parametric assumption 의 falsifier 가능 | 0 | empirical pilot (MC) | K=50+ phase |
| **bootstrap** | actual K=25 score resample with replacement | parameter-free, K-monotone 추정 | small-K bias (K=10→10 sample), trivial output 시 의미 무 | <100ms (10_000 resample) | actual score 수집 | K=25/50 phase |

## 2. Recommended Hybrid (Phase A / B / C)

single-path 가 아닌 3 결합 hybrid — 각 phase 는 *서로 다른 question* 에 대응.

| phase | trigger | method | wall | question |
|-------|---------|--------|-----:|----------|
| **A** | lens reimpl 직후 | MC N=100, shuffled-x | ~5s | "lens 가 x 를 읽고 있는가?" — score nontrivial 여부 |
| **B** | K=25 actual run 후 | bootstrap (K=25 score → 10_000 resample) + KS-test vs Phase A null | ~100ms | "K=25 분포 ≠ random null? F2 trip 판정" |
| **C** | K=50+ scaling | analytic Gaussian fit (mean/std from Phase B) | 0 | "K=N (N≫25) null 즉시 평가" |

→ Phase A = channel binding 검증, Phase B = F2 falsifier 실행, Phase C = future scaling.
**cascade_k25_plan §3.1 의 MC default 권고는 Phase A — 본 spec 는 B+C 추가**.

## 3. Implementation Outline

### 3.1 Phase A — MC channel-binding smoke (~25 LOC)

```python
# f2_phase_a_mc.py (future)
import json, numpy as np
from pathlib import Path
SEED, N_TRIAL = 0xF2A001, 100
K25_LENSES = [...]  # cascade_k25_plan §1.1+§1.2+§1.3 → 25 basename
rng = np.random.default_rng(SEED)
x_canonical = load_canonical_x()  # spec §2 D, after Agent #F reimpl
scores_null = np.zeros((N_TRIAL, len(K25_LENSES)))
for t in range(N_TRIAL):
    x_shuffled = rng.permutation(x_canonical)  # row-wise (L2)
    for k, lens in enumerate(K25_LENSES):
        scores_null[t, k] = run_lens(lens, x_shuffled)  # 19 ms
out = {"seed": hex(SEED), "n_trial": N_TRIAL, "mean": scores_null.mean(0).tolist(),
       "std": scores_null.std(0).tolist(),
       "channel_binding_ok": bool(scores_null.std() > 0.01)}
Path("f2_phase_a_null.json").write_text(json.dumps(out, indent=2))
```

### 3.2 Phase B — bootstrap + KS-test (~20 LOC)

```python
# f2_phase_b_bootstrap.py (future)
import json, numpy as np
from scipy.stats import ks_2samp
from pathlib import Path
SEED, N_RESAMPLE = 0xF2B002, 10_000
scores_actual = load_k25_actual_scores()
null_mc = json.loads(Path("f2_phase_a_null.json").read_text())
rng = np.random.default_rng(SEED)
boot_actual = rng.choice(scores_actual, size=(N_RESAMPLE, 25), replace=True).mean(1)
boot_null = rng.choice(null_mc["mean"], size=(N_RESAMPLE, 25), replace=True).mean(1)
ks_stat, p_value = ks_2samp(boot_actual, boot_null)
out = {"seed": hex(SEED), "ks_stat": float(ks_stat), "p_value": float(p_value),
       "f2_trip": bool(p_value >= 0.05), "n_resample": N_RESAMPLE}
Path("f2_phase_b_ks.json").write_text(json.dumps(out, indent=2))
```

### 3.3 Phase C — analytic Gaussian fit (~10 LOC)

```python
# f2_phase_c_analytic.py (future, K=50+)
from scipy.stats import norm
mu_null, sigma_null = phase_b["boot_null_mean"], phase_b["boot_null_std"]
def f2_check(score_kN):
    z = (score_kN - mu_null) / sigma_null
    p = 2 * (1 - norm.cdf(abs(z)))
    return {"z": float(z), "p": float(p), "trip": p >= 0.05}
```

## 4. KS-test Threshold + Alternatives

### 4.1 p ≥ 0.05 정당화

- **direction**: F2 *trip* 조건은 "lens 분포 ≠ null 과 구분 안 됨" = `p ≥ 0.05` (귀무가설 reject 실패). cascade_k25_plan §3 F2 일치.
- **α=0.05**: 통계학 관례. Bonferroni (§2 C4) 와 별 axis — F2 는 single test per cascade.
- **power**: N=100 MC trial KS-test power 는 effect size ≥ 0.3 에서 ≥ 0.8 — L4.

### 4.2 Alternatives

| test | when | rationale |
|------|------|-----------|
| **Anderson-Darling** | tail-sensitive | KS center 민감, AD tail 민감 |
| **Cramér-von Mises** | smooth L2 거리 | sup-norm 대신 L2 — multi-modal null robust |
| **Mann-Whitney U** | rank-based | small-K 에서 power 약하나 robust |

→ default = KS, fallback = AD (tail 의심 시).

## 5. Honest Limits

| ID | limit | 설명 |
|----|-------|-----|
| **L1** | lens reimpl 선결 | smoke_k10_caveat §4 의 "x 입력 채널 부재" 가 현 상태. Agent #F Phase 1 *전* 본 spec Phase A/B/C 모두 actionable 아님. lens 가 x 무시 시 shuffled-x 도 동일 score → F2 영원히 무력화 |
| **L2** | shuffle 방법 미결정 | Phase A shuffled-x default = row permutation. row vs column vs random-replacement (Gaussian noise) axis 미결정. spec §2 D 가 vector/matrix/multi-channel 여부와 paired binding |
| **L3** | small-K bootstrap bias | K=25 bootstrap 은 25-sample → 분산 큼 (BCa correction 미명시). K=50 에서 완화. K=25 Phase B 는 bias-corrected 필요 — 본 spec raw resample 만 outline. `scipy.stats.bootstrap(method='BCa')` 추후 권고 |
| **L4** | power calc 미수행 | N=100 MC KS-test power 가 lens variance 에서 충분한지 미증명. 실측 variance 없음 → N=1000 확장 시 wall 8min. cycle 6 power-analysis sub-task 권고 |

## 6. Cross-Reference

| ref | path | 관계 |
|-----|------|-----|
| cascade plan §3.1 | `cascade_k25_plan_2026_05_12.md` §3.1 | 본 spec 가 보강 (cross-link 1줄 추가) |
| K=10 caveat | `smoke_k10_caveat_investigation_2026_05_12.md` §4 | TRIVIAL — L1 prereq 근거 |
| lens reimpl spec | `lens_channel_reimpl_spec_2026_05_12.md` (Agent #F) | Phase 1 = 본 spec actionable trigger |
| numerology MC | `state/numerology_critique_n6_2026_05_11/simulate.py` | seed mnemonic + MC excl-pool 정합 |
| parent F2 | `spec.md` §5 F2 | F2 original 정의 |
| Hc cluster | Hc_586 (가속), Hc_960 (mislabel), Hc_378 (n=6 basis) | F2 가 falsify 하는 Hcs |
| lock policy | memory: feedback_no_relock.md 2026-05-11 | chflags/chattr 무적용 |
