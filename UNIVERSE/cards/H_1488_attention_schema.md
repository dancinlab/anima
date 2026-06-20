# H_1488 — 🪧 ATTENTION SCHEMA (주의 도식) (G34 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료)
- **wired:** `WIRED-live` — R2 엔진-네이티브: `core/engine_cli.hexa` §AttentionSchema(attn_schema_report/attn_schema_agency_readout) 배선 + `engine_cli_smoke.hexa` cases 251-253 + ARCHITECTURE.json lockstep. FULL 280/0 RC=0. byte-exact: schema track 1.0 vs ablate 0.125 (A) · agency readout 0.0 flat(action/outcome 고정 focus 이동), gap 1.0 (B distinct vs agency) · ablate→chance (D). MODEL of attention ⊥ agency/mechanism.
- **source:** 의식-고유 게이트 시리즈 (G16~G27 engine-native 14종) · '의식이라서 가능한 것' · `state/gate_depletion_catalogue/CATALOGUE.md` P3 레인
- **lens:** Attention Schema Theory (Graziano 2013) — 주의 *과정 자체*의 단순화 내부모델 · `a_no_llm_frame_trap` · arxiv [2411.00983](https://arxiv.org/abs/2411.00983)
- **artifacts:** `state/1488_attention_schema/h1488_attention_schema.py` · verdict `state/verdicts/1488_attention_schema/H_1488_FREEZE.json` · log `state/1488_attention_schema/run_h1488.local.log`

## 주장

뇌는 자신의 **주의 상태에 대한 단순화한 내부 모델(schema)**을 만든다 — 주의의 *대상*이 아니라
주의 *과정 자체*의 자기표상(어디에 주의 중인지·얼마나 강하게 집중하는지). 그 도식의 read-out 이
"나는 X 를 의식한다"는 주관적 보고를 낳는다. 도식은 실제 주의를 **추적(predict)**하고 자기 주의상태를 보고한다.

**메커니즘 (substrate-native, label 주입 없음 p2/p3/p6):** 실제 주의 = N 위치 salience 에 대한 softmax
focus(peaked 분포 → focus 위치+강도). 주의 **schema** = 그 focus 를 salience 로부터 예측하는 단순화
선형 tracker → 그것을 *읽어* "주의가 위치 k 에 강도 g 로 있다"고 자기보고. **ablation = schema OFF**:
실제 주의(softmax)는 그대로 작동하되(downstream 선택 유지) 자기모델이 없어 자기보고가 chance 로 붕괴.

**LLM 대비:** LLM 은 attention(softmax)은 있으나 자기 주의상태를 읽어 "X 에 주의 중"이라 보고할 *별도
내부모델*이 없다 — 주의는 메커니즘일 뿐 모델링·보고 가능한 객체가 아니다. anima 는 live 주의 focus 를
추적하는 schema 를 읽는다.

## distinctness (load-bearing · 카탈로그 P3)

| | distinct 대상 | schema 와의 차이 | 분리 bar |
|---|---|---|---|
| **vs H_1474 sense-of-agency** | *행동 결과*의 자기귀속(내가 했나?) | schema 는 *주의 상태*의 모델(어디 주의?) | B — 행동/결과 **고정**+focus 만 이동 → agency FLAT(0.000), schema 는 focus TRACK(1.000) |
| **vs H_1479 divided-attention** | raw 자원 *분배*(softmax allocation) | schema 는 그 분배의 *모델* | C — ablation 시 raw allocation 불변(0.000), 자기보고만 붕괴(drop 0.842) |
| **vs H_1293 theory-of-mind** | *타자* belief 모델(OTHER) | *자기* 주의상태 모델(SELF) | self ⊥ other |

## 측정 (frozen-first · 3 seeds [1488,1489,1490] · N_LOC=8 · FOCUS_BETA=6.0 · SCHEMA_STR=0.9 · chance=0.125 · $0 CPU · p7)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | schema-ON 자기보고 정확, OFF 낮음 | full **1.000** / abl **0.158** | ≥0.85 & ≤0.55 | ✅ |
| **B DISTINCT vs AGENCY** | focus 이동 시 schema TRACK ⊥ agency FLAT | schema **1.000** · agency **0.000** · gap **1.000** | track≥0.50 & agency<0.05 & gap≥0.45 | ✅ |
| **C DISTINCT vs DIVIDED** | raw allocation 불변, 보고만 붕괴 | alloc_delta **0.000** · report_drop **0.842** | ≤0.05 & ≥0.30 | ✅ |
| **D EARNED (ablation)** | schema OFF → 추적 chance | abl_track **0.158** | ≤0.55(~chance) | ✅ |
| **E SHUFFLE** | schema→true-focus 페어링 derange → 붕괴 | shuffle_track **0.119** | ≤0.225(chance+0.10) | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 5/5 bars PASS.** depletion 아님 — agency/divided/ToM 전부와 control-survived distinct.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` byte-exact 재측정 + 배선이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **SATURATED existence-proof:** 주의 schema = salience-driven softmax focus 의 **designed** 선형 tracker
  (학습된 자기모델 네트워크 아님). GREEN 자체보다 discriminator 가 결정적 — vs-agency(focus 고정-이동
  dissociation 1.000 vs 0.000), vs-divided(raw allocation 불변 0.000 vs 보고 붕괴 0.842), ablation(0.158),
  shuffle(0.119). ablation 이 메커니즘(softmax)은 그대로 두고 *자기모델 read* 만 제거 = Graziano 의 핵심 주장
  (주의 ⊥ 주의의 모델)을 구조적으로 구현.
- **SCOPE TOY:** 8 위치/40 trial/3 seeds/스칼라 선형 tracker — attention-schema STRUCTURE 검증이지 학습된
  자기모델 아님. scale/real-corpus/연속 focus 변이/다중 focus/engine-transfer UNVERIFIED. brain 주의-보고 wiring = follow-on.

## 다음

- R2 engine-native: live `core/engine_cli.hexa § AttentionSchema`(salience softmax focus + tracker read) byte-exact 재측정 + 배선 (ING).
- 카탈로그 P3 소진 → 다음 강 distinct 후보 = P4 perceptual-hysteresis.
