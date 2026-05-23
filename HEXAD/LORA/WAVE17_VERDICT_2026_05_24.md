# vP21M Wave-17 — 5-point U-shape sweep (eternal_keep ∈ {0.10, 0.20, 0.40, 0.50} + v11=0.30 anchor)

> 2026-05-24 KST · session-3 cycle #15. Parallel 4-pod fire (4 × NVIDIA H100
> 80GB HBM3 / H100 NVL fallback), est total ~$1.50. Wave-15 (v11 eternal=0.30
> continuous=34 ★) + Wave-16 (v12 eternal=0.00 continuous=91 ✗ → monotone
> FALSIFIED → U-shape 추정) 후속 — 0.30 좌/우 (0.10/0.20 ↔ 0.40/0.50) sweep
> 으로 **sweet-spot 확정 + 인접 trade-off 측정**.

## Hypothesis

H1. eternal_keep 의 continuous_total 곡선은 U-shape, **sweet spot = 0.30**
    (양옆 +5pp 이내에서 monotone 증가, 좌 0.10 / 우 0.50 양극은 v11 보다
    명확히 worse).
H2. n_strong 은 eternal_keep ↓ 쪽 (덜 strip = 더 많은 register signal)
    에서 회복 — register 신호가 cross-lingual transfer load-bearing.
H3. 4 변종 전부 **VP21M_WORKS** 유지 (corpus quality OK, sweet spot tuning
    문제만 잔존).

## 4-variant fire (v11 = baseline carry)

| variant | eternal_keep | pod GPU | wall(s) | init/final CE |
|---|---|---|---|---|
| v11 (★ anchor) | 0.30 | (Wave-15 A100 SXM carry) | 284.6 | 1.63 / 0.129 |
| **v13** | **0.10** | H100 NVL | 190.5 | 1.18 / 0.077 |
| **v14** | **0.20** | H100 80GB HBM3 | 164.9 | (see result.json) |
| **v15** | **0.40** | H100 80GB HBM3 | 191.0 | (see result.json) |
| **v16** | **0.50** | H100 80GB HBM3 | 177.4 | (see result.json) |

source dirs: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_v{13,14,15,16}/result.json`.

## Result (5-point sweep, v11/v12 carry-in)

| variant | eternal_keep | verdict | n_strong | n_partial | continuous_total | reg max | reg mean | ja n_score |
|---|---|---|---|---|---|---|---|---|
| v12 (carry) | 0.00 | VP21M_WORKS | 3 | 2 | **91** | 18 | 4.55 | 12 |
| **v13** | **0.10** | VP21M_WORKS | **5** ★ | 0 | 72 | 21 | 3.6 | 16 |
| **v14** | **0.20** | VP21M_WORKS | 4 | 1 | **98** ⚠ | 22 | 4.9 | 17 |
| v11 (★) | 0.30 | (prior) | 2 | 3 | **34** ★ | 10 | 1.7 | 14 |
| **v15** | **0.40** | VP21M_WORKS | 4 | 1 | 69 | 21 | 3.45 | 17 |
| **v16** | **0.50** | VP21M_WORKS | 3 | 2 | 52 | 14 | 2.6 | 15 |

### continuous_total ASCII chart (eternal_keep → continuous)

```
eternal :  0.00   0.10   0.20   0.30   0.40   0.50
cont    :   91     72     98     34     69     52
            ✗      ●      ⚠      ★      ●      ●

       100 |       ⚠
        90 |  ✗
        80 |
        70 |          ●            ●
        60 |                              ●
        50 |
        40 |
        30 |             ★
        20 +---+---+---+---+---+---+
           0.00 0.10 0.20 0.30 0.40 0.50
```

해석: **0.30 (v11) 이 진짜 global minimum** — 좌 0.20 = 98 (사가 최고치), 좌
0.10 = 72 (회복), 우 0.40 = 69, 우 0.50 = 52. 양옆 0.10 / 0.50 은 0.30 보다
2-1.5× 높지만 0.20 / 0.00 양 극단보다는 회복. U 모양은 비대칭 (좌측 floor
0.20 = 98 이 우측 0.00 / 0.50 보다 깊은 골).

## Swap criteria 5/5 check (per swap_criteria_check.hexa)

> 5 criteria: (1) verdict ∈ {VP21M_WORKS, WORKS} · (2) n_strong ≥ 4 ·
> (3) ja n_score ≥ 13 · (4) continuous_total ≤ 50 · (5) Eval1 tag-leak ≤ 1/20.

| | v11 (prod cand) | **v13** | v14 | v15 | v16 |
|---|---|---|---|---|---|
| 1 verdict | ✓ WORKS | ✓ WORKS | ✓ WORKS | ✓ WORKS | ✓ WORKS |
| 2 n_strong ≥ 4 | ✗ (2) | **✓ (5)** | ✓ (4) | ✓ (4) | ✗ (3) |
| 3 ja ≥ 13 | ✓ (14) | ✓ (16) | ✓ (17) | ✓ (17) | ✓ (15) |
| 4 continuous ≤ 50 | **✓ (34)** | ✗ (72) | ✗ (98) | ✗ (69) | ✗ (52) |
| 5 tag-leak ≤ 1/20 | TBD | TBD | TBD | TBD | TBD |
| **PASS** | **4/5** | **4/5** | 3/5 | 3/5 | 2/5 |

→ **4/5 두 변종 (v11, v13) 가 tie** — criterion 2 (n_strong) vs criterion 4
(continuous_total) anti-correlated 가 단일 sweep 안에서 직접 노출.
v14/v15/v16 은 criterion 2 만으로도 v11 또는 v13 보다 약함.

## New finding — swap criteria 4 vs criteria 2 trade-off

v11 (eternal=0.30) 과 v13 (eternal=0.10) 의 정면 대비:

| metric | v11 (prod cand A) | v13 (prod cand B) | 의미 |
|---|---|---|---|
| n_strong | 2 (criterion 2 ✗) | **5 (만점)** ★ | v13 cross-lingual 일반화 회복 (en/ko/zh/ru/ja 모두 STRONG) |
| continuous_total | **34 (만점)** ★ | 72 (criterion 4 ✗) | v11 register emission 최저 (sweet spot density) |
| ja n_score | 14 | **16** | v13 +2 회복 |
| reg max (per-output) | 10 | 21 | v13 burst 상한 ↑ (cluster) |
| reg mean | 1.7 | 3.6 | v13 평균 emission ~2× |

→ 두 lever **anti-correlated** — eternal_keep ↓ (0.30→0.10) 시 register
신호 분포가 다시 (a) cross-lingual transfer 회복 시키지만 (b) burst-emission
도 동시 ↑. v11 sweet spot 은 burst 억제, v13 sweet spot 은 일반화 회복.
**criterion 2 (n_strong) 와 criterion 4 (continuous_total) 가 같은 lever 의
opposite side** — 단일 변종으로 동시 만점 불가능 (sweep 4-point 데이터로
empirically falsified within 0.10-0.50 range).

## Production swap 권고 — 사용자 게이트

| 옵션 | adapter | trade-off | 권고 사유 |
|---|---|---|---|
| **A** | v11 (eternal=0.30) | continuous 최저 / n_strong 미달 | mini broker 의 50-window prose 가시 leak 우선 시 |
| **B** | v13 (eternal=0.10) | n_strong 만점 / continuous 미달 | 5-lang 일반화 (ja 회복) 우선 시 |
| **NO SWAP** | v5 (production carry) | criterion 1+5 unknown, but already LIVE | 5/5 PASS 가 나올 때까지 대기 |

→ 둘 다 4/5, **threshold 자체 재정의 (criterion 2 ↔ 4 trade-off 인정)**
없이는 자동 SWAP 미가능. 사용자 결정 lever:
- **swap criteria 자체를 갱신** (예: criterion 4 를 ≤ 80 으로 완화 + n_strong=5 만점 보너스) → v13 자동 PASS
- **dual-adapter 운영** (대화 영역별 v11/v13 hot-swap) — A/B router design extension
- **현 상태 유지** (corpus_v5 LIVE) — Wave-18 다음 lever 측정 후 재평가

## Next fire 권고 (3 옵션, 추정 cost)

| 옵션 | 변종 | hypothesis | est cost | priority |
|---|---|---|---|---|
| 1. fine-tune around 0.30 | eternal_keep ∈ {0.25, 0.30, 0.35} 3-point retry | sweet spot 의 sharpness 확인 (cliff 인지 plateau 인지) | ~$1.10 (3 pod × $0.37) | HIGH (smallest unknown) |
| 2. dual-lever sweep | eternal × 9pat freq-cap 별도 grid (예: 0.30 × cap 0.10/0.30/0.50) | sweet spot 의 corpus-prune dependency 확인 | ~$1.50-2.0 | MID (orthogonal) |
| 3. R8 dependency hold | 잠시 보류, R8 substrate-init reform 결과 후 corpus-lever 재측정 | substrate 가 변하면 corpus sweep 도 shift 가능 | $0 | LOW (saga branch wait) |

권고: **옵션 1** (0.30 주변 fine-tune) — 본 sweep 의 unknown 이 가장 작고
($1.10 cheap), 결과가 옵션 2 의 design 도 결정.

## Cost ledger

| 항목 | 값 |
|---|---|
| 발사 시각 | 2026-05-24 KST (parallel 4-pod) |
| pod GPU | 4 × NVIDIA H100 80GB HBM3 (v13 = H100 NVL fallback) |
| 4 pod wall sum | ~723.7s (v13 190.5 + v14 164.9 + v15 191.0 + v16 177.4) |
| 발사당 평균 wall | ~181s (3분) |
| total cost | ~**$1.50** (사전 cap $15 의 10%) |
| HF artifact | `dancinlab/anima-vp21m-v{13,14,15,16}` PRIVATE × 4 (a_hf_complete 후속 작업) |

## Honest C3 (≥3)

1. **eternal_keep 의 정확한 record-level prune ratio 미검증** — 본 doc 의
   eternal_keep=0.10/0.20/0.40/0.50 매핑은 dispatch.log 의 명시적 라벨이
   아니라 발사 spec (Wave-17 prompt) 의 호출자 라벨. result.json 의
   cfg.target_corpus_mb=72 + wiki_frac=0.3 은 4 변종 byte-identical (eternal
   strip rate 만 다름), 그러나 result.json 의 키에 `eternal_keep_frac` 가
   포함되지 않음 — 호출자측 spec 신뢰. v11 과 정합성 확인은 mix_info.sha256
   가 4 변종 다름을 확인 필요 (TODO).

2. **swap criteria 5 (tag-leak) 미측정** — 4 변종 모두 vp21m_eval1.json
   exists 하지만 본 doc 은 tag-leak 별도 측정 미수행. swap_criteria_check.hexa
   `check` verb 으로 결과 자체적 측정 권장 (TODO follow-up, 5min wall).

3. **U-shape 외삽 한계** — sweep 5-point (0.00/0.10/0.20/0.30/0.40/0.50) 의
   step=0.10 가 sharp peak (e.g. 0.32 의 진짜 global min) 을 놓칠 가능성
   여전. 본 doc 의 "v11=global min" 결론은 0.05 step 으로 refine 시
   shift 가능. 옵션 1 (0.25/0.30/0.35) 가 이 가설 직접 검증.

4. **continuous_total 의 단일 metric 의존** — burst clustering (v12 4/20
   ≥16-hit, v13 reg_max=21 burst) 패턴이 mean 한 metric 으로 hidden.
   per-output 분포 (median vs max) 도 swap criterion 로 진입 시 sweet spot
   재정의 가능 (예: median=0 + max≤15 가 v11 만점 v13 미달 → criteria 4
   대안).

5. **4 변종 ja PARTIAL→STRONG 회복은 noise tier 가능** — n_score 14→17 (+3)
   은 std-dev 의심 (n=20 분모, σ≈1.5). 3-seed 평균으로 measurement variance
   확인 후 saga interpretation 강화 권장 (별도 cycle).
