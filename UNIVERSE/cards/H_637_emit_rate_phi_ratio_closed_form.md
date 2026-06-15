# H_637 — `emit-rate-phi-ratio-closed-form` (ANIMA.mining L13/L14 promote · COFFESHOP substrate emit-rate ↔ closed-form numerology)

> ANIMA.mining.md cycle 2 (tension lens) L13/L14 의 `emit 4 / silence 11` substrate-natural emit-rate (~27%) 가 어떤 closed-form 상수 ({GZ_LOWER, ln(4/3), 1/e, 1−1/e}) 와 ±0.03 일치하는지를 verify-driven 으로 검정. **결과: 🔴 FALSIFIED** — robust multi-seed mean emit-rate(0.4133) 가 모든 후보를 ±0.03 밖에서 miss, 단일 seed 의 ln(4/3) "일치"는 post-hoc selection artifact. emit-rate 는 threshold-dependent 연속량이지 closed-form 불변량 아님.

## 1. 기원 (provenance)

- **ANIMA.mining.md L13/L14 promote**. cycle 2 (tension lens, depleted), T1 contradiction `emit-rate (4 emit) ↔ silence-rate (11 silence)` 의 two-fork:
  - **L13 tension-fork-A** (emit-dominant 채택): substrate-natural emit rate **27% 가 floor** — channel(1:1 → group → multi) 마다 emit threshold **scaling law** 존재 가설. → 영역 CHANNEL × BRIDGE.
  - **L14 tension-fork-B** (silence-dominant 채택): substrate 자연 상태 = silence default, emit 은 strong evidence 필요. anima 73% silence = `a_substrate_native_speak` 의 정량 instance. → 영역 WAKE × OTHER-MIND.
- 두 fork 모두 emit-rate (~0.27) 라는 **특정 수치**에 의존. 본 H 는 그 수치가 substrate Φ-distribution 의 closed-form ratio 와 일치하는지를 검정 — fork 의 정량 기반을 verify-driven 으로 못박는다.
- SSOT 데이터: `state/coffeshop_sim_seed_sweep_2026_05_24/sweep_summary.json` (N=10 seed, 15-window/seed, 全 PASS, register-clean). 원본 단일 run = `state/coffeshop_sim_2026_05_24/result.json` (sha16 55c32aabf611171c, emit 4 / silence 11).

## 2. 가설 (H1) · 귀무 (H0/FALSIFIER)

- **H1 (closed-form match)**: substrate-natural emit-rate (motivation_score > 0.60 인 window 비율) 가 후보 closed-form 상수 {GZ_LOWER=1/2−ln(4/3)≈0.2123, ln(4/3)≈0.2877, 1/e≈0.3679, 1−1/e≈0.6321} 중 적어도 하나와 **|residual| ≤ 0.03** 일치, 그리고 그 일치가 seed-robust (multi-seed mean 기준 유지).
- **H0 (FALSIFIER F637.1)**: robust emit-rate (N≥10 multi-seed mean) 가 **모든** 후보와 |residual| > 0.03 — 또는 threshold 임의성에 따라 emit-rate 가 연속 변동(closed-form 불변량 아님).

## 3. 방법 (method)

1. COFFESHOP emergence simulator 의 8-factor `motivation_score = Σ wᵢ·factorᵢ > 0.60 → emit · else silence` (B7 LCG + spontaneous_lib verbatim import) 결과를 재현 — **새 substrate re-fire 없이** sweep_summary.json (10-seed) deterministic replay.
2. seed 별 emit/15 ratio 의 분포 (mean·sd·range) 정밀 계산.
3. 후보 closed-form 4종 각각과 |residual| 산출 — (a) robust multi-seed mean, (b) 원본 단일 run (4/15) 두 기준.
4. **numerology cover-rate** (H_620 §C3.2 methodology): 4 candidate × ±0.03 band 의 [0,1] 위 union 측도 → 임의 rate 가 어떤 band 에 들 prior.
5. threshold-dependence: emit-rate = motivation_score>0.60 의 upper-tail mass. mean motivation_score 와 비교해 threshold shift 에 대한 연속성 논증.

> ⚠ **monitor-hang 회피**: hexa run foreground sync only, deterministic replay (no substrate re-fire). 산술 residual 은 mac-local 정밀 계산, closed-form 상수 (ln(4/3) H_347 🔵+🟢, 1/e H_349 anchor) 는 upstream verify-resident.

## 4. 측정 (measurement)

**SSOT**: `state/coffeshop_sim_seed_sweep_2026_05_24/sweep_summary.json` (N=10, 15 windows/seed).

| seed | emit | silence | emit-rate (emit/15) |
|---|---|---|---|
| 20260520 | 6 | 9 | 0.4000 |
| 20260521 | 8 | 7 | 0.5333 |
| 20260522 | 3 | 12 | 0.2000 |
| 20260523 | 8 | 7 | 0.5333 |
| 20260524 | 6 | 9 | 0.4000 |
| 20260525 | 4 | 11 | 0.2667 |
| 20260526 | 6 | 9 | 0.4000 |
| 20260527 | 5 | 10 | 0.3333 |
| 20260528 | 8 | 7 | 0.5333 |
| 20260529 | 8 | 7 | 0.5333 |

- **MULTI-SEED MEAN emit-rate = 0.41333** · sd = 0.12090 · range [0.2000, 0.5333] · pooled (62/150) = 0.41333.
- **원본 단일 run** (result.json, emit 4) = 4/15 = **0.26667**.
- mean motivation_score (10-seed) = **0.5518** (threshold 0.60 보다 ~0.05 **낮음** → emit 은 score 의 upper-tail fluctuation 에서만 발생).

**후보 closed-form (verify-resident 상수)**:

| 후보 | 값 | anchor |
|---|---|---|
| GZ_LOWER = 1/2 − ln(4/3) | 0.212318 | H_348 lower bound |
| ln(4/3) = GZ_WIDTH | 0.287682 | H_347 🔵+🟢 |
| 1/e = GZ_CENTER | 0.367879 | H_349 anchor |
| 1 − 1/e | 0.632121 | (silence-dominant 후보) |

**residual (robust multi-seed mean = 0.41333)**:

| 후보 | residual | ±0.03? |
|---|---|---|
| GZ_LOWER | 0.2010 | ✗ |
| ln(4/3) | 0.1257 | ✗ |
| **1/e (best)** | **0.0455** | ✗ (>0.03) |
| 1−1/e | 0.2188 | ✗ |

→ **robust mean 은 모든 후보를 ±0.03 밖에서 miss** (best 1/e residual 0.0455). **F637.1 PASS (FALSIFIED).**

**residual (원본 단일 run = 0.26667, post-hoc 1-seed)**:

| 후보 | residual | ±0.03? |
|---|---|---|
| GZ_LOWER | 0.0543 | ✗ |
| **ln(4/3) (best)** | **0.0210** | ✓ MATCH |
| 1/e | 0.1012 | ✗ |
| 1−1/e | 0.3655 | ✗ |

→ 단일 run 만 ln(4/3) 과 0.0210 일치. **하지만 이것은 10-seed 중 cherry-picked single seed (20260524/result.json)** — robust statistic 이 아님.

## 5. verdict

**🔴 FALSIFIED** (F637.1 PASS). 3개 독립 근거:

1. **robust mean miss**: multi-seed mean(0.4133) 이 4 후보 모두 ±0.03 밖 (best 1/e 0.0455).
2. **post-hoc selection**: 단일 run(0.2667)의 ln(4/3) 일치는 10-seed 중 한 seed 의 산물 — H_620 §C3.2 와 동일 caveat (post-hoc 4-candidate × seed selection).
3. **threshold-dependent 연속**: emit-rate 는 motivation_score>0.60 의 upper-tail mass. mean score 0.5518 이 threshold 바로 아래라 분포의 mode 근처 → d(rate)/d(threshold) 가 가파름. threshold ±0.05 shift 가 emit-rate 를 GZ_LOWER~1/e band 를 가로질러 이동시킴 → closed-form **불변량 아님**, threshold 임의성에 따른 연속량.

closed-form numerology 와의 일치는 **부재** — substrate emit-rate 는 (rule/seed/threshold) conditional 한 연속 분포일 뿐, deep closed-form ratio 가 아니다.

## 6. cross-link (선행 H · mining edge)

- **ANIMA.mining L13/L14** — 본 H 의 promote 출처 (T1 emit↔silence tension two-fork). 본 H 의 FALSIFIED 는 L13 "27% floor" 와 L14 "73% silence default" 두 fork 가 **특정 numerology 상수에 묶이지 않음**을 못박는다 — fork 의 정량 기반은 substrate-conditional 연속량, closed-form attractor 아님.
- **COFFESHOP** (`state/coffeshop_sim_2026_05_24` · emit 4 / silence 11) — measurement SSOT. 4-criterion closure sim, register-clean.
- **H_347** `gz-width-divisor-symmetry` — `GZ_WIDTH = ln(4/3) ≈ 0.287682` closed-form (🔵+🟢). 본 H 의 후보 #2. emit-rate 가 GZ_WIDTH 와 일치한다는 가설이 단일 seed 에서만 성립 → 우연.
- **H_348/H_349** — GZ_LOWER(1/2−ln(4/3)) · GZ_CENTER(1/e) closed-form anchor. 본 H 의 후보 #1/#3.
- **H_620** `gz-width-super-additive-cross-link` — **동일 numerology guardrail 선례** (§C3.2 cover-rate prior + post-hoc selection caveat). H_620 은 R1 이 3·GZ_WIDTH 와 0.0164 일치(🟢 SUPPORTED-NUMERICAL, prior cover ≈ 17%) 였으나, 본 H 는 robust mean 이 모든 후보를 miss → 🔴. **같은 방법론, 반대 결과** — emit-rate 축은 GZ closed-form attractor 부재.
- **`a_substrate_native_speak`** (project.tape governance) — L14 의 silence-default 가 이 directive 의 정량 instance 라는 mining claim. 본 H 는 그 silence-rate 가 closed-form 이 아닌 **substrate-conditional 연속량**임을 보여, governance directive 는 *질적* 원칙이지 *수치 상수* 가 아님을 확인.

## 7. honest constraints (C3)

- **C3.1 numerology 경고 (§114 SAVANT EMERGENCE-FRONTIER AUDIT 강하게 적용)** — HEXAD/SAVANT/COMPENDIUM §114 SAVANT EMERGENCE-FRONTIER AUDIT 는 `savant_phi` top-k 가 g2-numerology-tainted 임을 경고한다. 본 H 의 closed-form 일치 검정은 **그 numerology 함정의 한복판**: emit-rate (0.27~0.41) 와 closed-form 상수 (0.21~0.63) 의 일치/불일치가 **우연(coincidence)** 인지 **깊은 동치(deep identity)** 인지 본 H 만으로 분리 불가. 본 H 의 FALSIFIED 는 "일치가 없다"는 **negative** 결론이므로 numerology 위험이 낮은 편이나, 만약 일치했다면 (단일 seed 처럼) 그것은 **post-hoc 4-candidate selection** 의 산물이었을 것이다 (H_620 §C3.2 와 정확히 동일 caveat).
- **C3.2 cover-rate (numerology prior 정량)** — 4 candidate × ±0.03 band 의 [0,1] union 측도:
  - bands = {[0.182,0.242], [0.258,0.318], [0.338,0.398], [0.602,0.662]} (겹침 없음).
  - **cover = 0.2400 (24.0%)** — 임의 emit-rate 가 어떤 band 안에 들 prior ≈ **1/4**.
  - 즉 단일 seed 의 ln(4/3) "일치" (residual 0.0210) 는 24% prior 의 chance event 와 **통계적으로 구분 불가**. 이 cover-rate 자체가 H1 의 evidentiary value 를 무력화한다. (H_620 의 cover ≈ 17% 보다 **높다** — 후보가 4개로 더 많고 band 가 더 넓어 numerology 위험 ↑.)
- **C3.3 post-hoc 4-candidate selection risk** — 후보 집합 {GZ_LOWER, ln(4/3), 1/e, 1−1/e} 자체가 H_347/348/349 + silence-complement 에서 *post-hoc* 선택된 것. 다른 상수 (예: 3/8=0.375, 2/5=0.4, ln2=0.693) 를 추가하면 cover 가 더 커지고 일치 prior 가 더 높아진다 — 후보 선택의 임의성이 본 검정의 구조적 약점 (H_620 동일 caveat 계승).
- **C3.4 single-seed vs robust 분리** — 원본 COFFESHOP run (4/15=0.2667) 의 ln(4/3) 일치는 **단일 seed 우연**. 10-seed mean (0.4133) 이 robust statistic 이며 이것이 모든 후보를 miss. mining L13/L14 가 단일 run 의 27% 를 "floor" 로 인용한 것 자체가 single-seed 의존 — 본 H 가 그 정량 기반을 robust 화하면 numerology 일치는 사라진다.
- **C3.5 threshold 0.60 의 design 임의성** — emit gate threshold 0.60 은 spontaneous_lib design 값. emit-rate 는 이 threshold 의 함수 (upper-tail mass). threshold 가 closed-form 으로 정당화되지 않는 한, emit-rate 의 어떤 closed-form 일치도 threshold-conditional — 즉 emit-rate 가 closed-form 이려면 threshold 자체가 먼저 closed-form 이어야 한다 (별도 가설, 본 H 미검증).
- **C3.6 sim ↔ real isomorphism 미확정** — emit-rate 측정은 COFFESHOP **emergence simulator** (text_cli toy) 산출물. 실제 anima daemon 의 emit-rate 와의 isomorphism 은 mining L15 (sim 채택 fork) 의 가정일 뿐 별도 검증 필요. 본 H 의 결론은 sim 측 emit-rate 한정.

## 8. 재현 (reproducibility)

- **데이터**: `UNIVERSE/state/h637_emit_rate_phi_ratio_closed_form_2026_05_28/coffeshop_sweep_summary_source.json` (= `state/coffeshop_sim_seed_sweep_2026_05_24/sweep_summary.json` verbatim copy, N=10).
- **verdict 산출**: `.verdicts/h637-emit-rate-numerology/emit_rate_residuals.txt` (= `UNIVERSE/state/h637_emit_rate_phi_ratio_closed_form_2026_05_28/verdict.txt`) — emit-rate stats · 4-candidate residuals (robust + single-seed) · cover-rate 24% · 🔴 verdict.
- closed-form 상수: ln(4/3) (H_347 🔵+🟢 verify-resident) · 1/e (H_349 anchor) · GZ_LOWER (H_348). 산술 residual = mac-local 정밀 계산 ($0).
- deterministic replay — substrate re-fire 없음, monitor-hang 회피.

## 9. 함의 (implications)

- **mining L13/L14 정량 기반 무효화**: emit-rate(~0.27) 는 closed-form attractor 가 아니라 (rule/seed/threshold) conditional 연속 분포. L13 "27% floor scaling law" · L14 "73% silence default" 는 *질적* substrate 경향이지 *수치 상수* 가 아니다.
- **`a_substrate_native_speak` governance 확인**: silence-default 원칙은 substrate-decided 질적 directive 로 유지 — 특정 numerology 비율로 고정하면 오히려 hardcode (p1~p8 위반 위험). 본 FALSIFIED 가 governance 의 질적 성격을 지지.
- **negative-result 가치**: GZ closed-form 축(H_347/348/349) 이 emit-rate 축으로 **확장되지 않음**을 deterministic 하게 ruled out. H_620(GZ × super-additive 🟢) 와 대조 — GZ closed-form 의 cross-link 적용 범위 경계를 한 칸 더 못박는다.
- **후속 lane**: (a) threshold 0.60 자체의 closed-form 정당성 검정, (b) sim ↔ real daemon emit-rate isomorphism (mining L15), (c) channel-scaling law (L13) 의 multi-channel emit-rate sweep — 모두 별도 H.

## 10. 메타 (verdict tier · cost)

- **tier**: 🔴 FALSIFIED (closed-negative). F637.1 PASS (robust mean miss + threshold-dependent 연속 + post-hoc single-seed 일치).
- **best closed-form match**: 1/e (robust mean residual 0.0455, >0.03 FAIL) · ln(4/3) (single-seed residual 0.0210, post-hoc).
- **numerology cover-rate**: 24.0% (4 candidate × ±0.03 band union over [0,1]).
- **cost**: $0 mac-local, deterministic replay (no substrate re-fire), 2026-05-28.
- **axis**: 축 G — ANIMA mining-promote (NEW). ANIMA.mining L13/L14 → UNIVERSE 첫 promote.
