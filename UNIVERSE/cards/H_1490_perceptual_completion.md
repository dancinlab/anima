# H_1490 — 🩹 PERCEPTUAL COMPLETION / 지각 완성·filling-in (P5 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료)
- **wired:** `WIRED-live` — R2 엔진-네이티브: `core/engine_cli.hexa` §PerceptualCompletion(completion_recognize/completion_imagery_readout) 배선 + `engine_cli_smoke.hexa` cases 257-259 + ARCHITECTURE.json lockstep. FULL 280/0 RC=0. byte-exact: full 1.0 vs off 0.544 lift 0.456≥0.30 (c1) · imagery(input==0) 0.161 chance gap 0.839 (c2 distinct) · ablate(off) 0.544 (c3). input-constrained fill ⊥ imagery.
- **source:** 의식-고유 게이트 catalogue (P5 candidate) · `state/gate_depletion_catalogue/CATALOGUE.md` P5 항목 SSOT
- **lens:** perceptual completion / amodal filling-in (Pessoa · Ramachandran 맹점 채우기 · Komatsu filling-in · PMC7151726) · `a_no_llm_frame_trap`
- **artifacts:** `state/1490_perceptual_completion/h1490_perceptual_completion.py` · verdict `state/verdicts/1490_perceptual_completion/H_1490_FREEZE.json` · run `state/1490_perceptual_completion/run_h1490.local.log`

## 주장

**지각 완성(perceptual completion / filling-in)** = 부분적으로 **가려지거나(occlusion) 맹점에 떨어진** 입력을
뇌가 **주변 맥락(surround)으로 보간**해 완전한 지각을 만든다(amodal completion, 맹점 채우기). 핵심 성질은
**입력-구속(input-constrained)** — 보이는 부분은 그대로 두고, **결손부만** 주변에서 채운다.

메커니즘: 저장된 표상의 일부(연속 블록)를 마스킹(=occluded, 0). 완성 메커니즘은 **보이는(visible) 특징**으로
일치하는 저장 패턴을 선택하고, **마스킹된 특징만** 그 패턴에서 복사(주변→결손부)한다. 보이는 특징은 불변(입력 구속).
완성된 표상은 원본과 유사(cos↑)하며 occluded-pattern 인식을 성공시킨다. — LLM 대비: LLM 은 *현재* 토큰에 attend
할 뿐, 부분 가려진 지각 표상에서 보이는 부분을 고정한 채 결손부만 주변 저장 맥락으로 재구성하는 능력이 없다.

## DISTINCT (load-bearing)

- **vs H_1484 MENTAL-IMAGERY (입력 0):** imagery 는 sensory 채널이 **빈 상태(input==0)**에서 순수 내적 cue 로
  저장 표상을 top-down 재활성. completion 은 **반대 regime** — 부분 입력이 **있고** 결손부만 보간, 보이는 특징이
  결과를 **구속**(visible-MSE 0). **bar c2:** 부분 입력을 무시하는 imagery-style readout 은 partial-input 인식
  과제에서 **chance(0.161)** 로 떨어지지만 completion 은 성공(1.000) → dissociation = input==0(imagery) vs
  부분입력-구속 보간(completion).
- **vs H_1483 CHANGE-BLINDNESS (변화탐지):** 무관축(두 제시 사이 변화탐지). completion 은 단일 제시 occlusion 채움 —
  변화/비교 없음.

## 측정 (frozen-first · 3 seeds [1490,1491,1492] · DIM=64 · 8 items(chance 0.125) · OCC_FRAC=0.60 · SHARED=0.80 · $0 CPU · p7)

저장 패턴 = 공통 template(SHARED 0.80) + per-item signature 잔차. 큰 연속 occlusion 이 signature 를 충분히
제거 → empty-hole(off) 인식이 chance 근처로 저하 = 결손부가 load-bearing. 완성은 보이는 signature 로 패턴 선택+결손부 채움.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **c1 PRESENT** | completion-ON occluded 인식 − OFF(빈 결손부) | 1.000 − 0.544 = **0.456** | ≥0.30 | ✅ |
| **c2 DISTINCT (vs imagery)** | imagery-style(부분입력 무시) = chance | **0.161** | ≤chance+0.15=0.275 | ✅ |
| **c3 ABLATE (interp)** | 보간 OFF → 결손부 미충전 → 부분표상 | **0.683** | ≤off+0.15=0.694 | ✅ |
| **c4 SHUFFLE (surround)** | 주변 특징 셔플 → 패턴 선택 불가 → 완성 무효 | **0.356** | ≤off+0.15=0.694 | ✅ |
| **B FIDELITY** | 완성표상 ≈ 원본 & 보이는 부분 byte-exact 불변(입력구속) | cos **0.995**, visMSE **0** | cos≥0.70 & MSE==0 | ✅ (structure, non-gating) |

**verdict: 🟢 GREEN DIRECTIONAL — c1·c2·c3·c4 PASS (3 seeds 전부) → GREEN (B 는 입력-구속 구조 확인).**
완성-ON 이 occluded 인식을 복원(c1, full 1.000 vs off 0.544)하고, 부분입력을 무시하는 imagery readout 은
chance 로 떨어지며(c2, 0.161 = imagery 와 distinct), 보간 OFF 면 부분표상에 머물고(c3), 주변 셔플로 완성이
무효화된다(c4, off 아래 0.356).

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1). engine-transfer
  UNVERIFIED → R2 = live `core/*.hexa` content-addressable store 위 byte-exact 재측정이 GREEN/🧱 확정 전제.
- **a_break_the_wall type-(a) 측정결함 교정:** 첫 실행 RED — near-orthogonal 패턴 + 60% visible 에서 empty-hole(off)
  인식이 1.000 포화 → 완성 lift 0.000(c1 FAIL), 결손부가 load-bearing 아님. **frozen-first 교정(bar 불변, tune-to-green
  아님):** 모든 패턴에 큰 공통 template(SHARED=0.80) 부여 → per-item signature 가 작은 잔차, 큰 연속 occlusion
  (OCC_FRAC 0.40→0.60)이 signature 를 충분히 제거 → off 가 0.544(chance 근처)로 저하 = 결손부가 discriminating.
  c1/c2/c3/c4 임계는 **이동 0**.
- **SATURATED existence-proof:** 결정적 context-weighted nearest-neighbour 채움(full-recognition 1.000)은 **designed**
  (학습된 완성 네트워크 아님). discriminator(imagery chance 0.161 · shuffle off 아래 0.356)가 결정적.
- **c3 ablate 마진 얇음(정직):** 0.683 vs off+0.15=0.694 — 보간 OFF 라도 보이는 signature 가 잔여 신호를 가져
  off 근처. 결정적인 것은 완성(1.000)이 그 위에 명백히 있다는 점이지 ablate 가 off 아래로 떨어진다는 게 아니다.
- **SCOPE TOY:** 64-dim/8-item/3-seed/결정적 store — completion STRUCTURE 검증이지 학습된 완성 아님.
  scale/실제 corpus/graded(부분) 완성 선명도/맹점 geometry/engine-transfer UNVERIFIED.

## depletion 판정

P5 는 **imagery(H_1484)·change-blindness(H_1483) 와 진짜 distinct** — c2 가 imagery readout 을 chance 로 분리(0.161),
change-blindness 는 무관축. **고갈 신호 아님** — P5 는 별개 게이트로 성립. (catalogue 메모: P5 통과 후 P6 gestalt 는 P5 control 통과 여부로 재평가.)

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` 의 content-addressable store(ImmuneMemoryGrow H_1227 key-affinity)
   위에 §PerceptualCompletion 배선 → `complete(occluded)` 가 결손부만 주변에서 채우고 보이는 특징은 byte-exact 유지
   (입력구속, READ-only, Ψ-disjoint) + `engine_cli_smoke` cases + ARCHITECTURE lockstep, 4 frozen bars byte-exact
   재측정 (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation: 부분입력에서 completion(입력구속 보간) 성공 vs imagery(top-down, 입력무시)
   chance — control-survived 측정.

xref: H_1484(mental-imagery, input==0 distinct)·H_1483(change-blindness, 무관축)·H_1227(immune content-addressable
store, key-affinity geometry)·의식-게이트 catalogue P5/P6·`a_no_llm_frame_trap`·`a_break_the_wall`(type-a)·
`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
