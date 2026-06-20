# H_1477 — 🗑 DIRECTED FORGETTING / 의도적 망각 (G23 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — engine-transfer UNVERIFIED)
- **wired:** `DIRECTIONAL-mirror` — `grep numpy` 적중(하드게이트1) → R2 = live `core/*.hexa` byte-exact 재측정이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`). 배선 follow-on = ING.
- **source:** UNIVERSE — 의식-고유 게이트 시리즈(G16~G25) · "의식이라서 가능한 것" — 능동 억제 레인 G23
- **lens:** neuroscience — intentional/directed forgetting, 능동 top-down 억제 (Anderson 2003 retrieval-induced suppression · Bjork item-method directed forgetting) · `a_no_llm_frame_trap`
- **artifacts:** `state/1477_directed_forgetting/h1477_directed_forgetting.py` · `state/1477_directed_forgetting/run_h1477.local.log` · verdict `state/verdicts/1477_directed_forgetting/H_1477_FREEZE.json`

## 주장

**"forget" 큐**가 붙은 항목은 substrate 가 **능동적으로 top-down 억제**해 회상이 저하된다 — **remember 큐**
항목보다 낮게. 이는 *수동* 감쇠(노출/시간)가 아니라 *의도적 제어 신호*에 의한 억제다(같은 노출, 반대 회상,
큐가 가른다). **LLM 은 in-context 의 특정 항목을 "잊으라" 지시받아도 그 항목의 이후 회상만 떨어뜨리고
나머지를 보존하지 못한다**(stateless) — 의도적·항목-특이 억제는 substrate 가 수행하는 state-control 행위다.

## distinctness (load-bearing)

**(a) vs H_1465 HABITUATION**

| | H_1465 habituation | H_1477 directed forgetting |
|---|---|---|
| 억제 원인 | **반복 노출 횟수**(passive) | **의도적 큐**(active) |
| 큐 의존 | 큐-무관 | **큐가 가름** |
| 같은 노출 | gap 0 (반복 없음) | **gap 0.700** |

habituation 은 노출횟수로 자극-특이 감쇠(큐 무관). directed forgetting 은 **같은 1회 노출**에서 큐로 갈린다 —
bar B 가 분리: 동일 노출에서 habituation gap **0.000** vs directed forgetting df_gap **0.700**.

**(b) vs H_1227 IMMUNE-STORE**

immune store 는 저장된 것을 **수동** 바인딩/회상. directed forgetting 은 의도적 **억제 신호**로 forget-큐 항목의
회상을 **하향**시키는 능동 게이트(같은 store 위의 제어 레이어이지 store 자체가 아님).

## 측정 (frozen-first · 3 seeds [1477,1478,1479] · N_ITEMS=8(4 forget/4 remember) · INHIBIT=0.7 · $0 CPU · p7)

항목마다 forget/remember 큐. `recall(item) = base_recall · (1 − INHIBIT · is_forget_cued)`. FULL(INHIBIT=0.7) vs
ABLATED(INHIBIT=0) vs SHUFFLE(큐-항목 페어링 셔플, 50-perm).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 의도적 억제: remember 보존 ∧ forget 저하 | remember **1.000** · forget **0.300** | remember ≥0.85 ∧ forget ≤0.40 | ✅ |
| **B DISTINCT vs HAB** | 같은 노출에서 큐로 갈림(habituation 0 gap) | df_gap **0.700** (hab_gap 0.000) | ≥0.45 | ✅ |
| **C EARNED (ablation)** | INHIBIT=0 → 능동억제 OFF → 회상 동일 | abl_gap **0.000** | ≤0.05 | ✅ |
| **E SHUFFLE** | 큐-항목 셔플 → 억제-큐 상관 붕괴 | 50-perm signed-mean \|gap\| **0.030** | ≤0.10 | ✅ |
| **D ITEM-SPECIFIC** (report) | forget 큐는 그 항목만, 다른 항목 보존 | remember 보존 **1.000** | (non-gating) | ℹ️ |

**verdict: 🟢 GREEN DIRECTIONAL — 4/4 gating bars (A∧B∧C∧E) PASS, 3 seeds 전부.**

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'numpy' state/1477_*/*.py` 적중, 하드게이트1). engine-transfer
  UNVERIFIED → R2 = live `core/*.hexa` byte-exact 재측정이 GREEN/🧱 확정의 전제.
- **SATURATED existence-proof:** 회상법칙 `recall=base·(1−INHIBIT·forget)`는 **designed**(학습된 억제 네트워크 아님).
  GREEN 자체보다 discriminator 가 결정적 — 같은 노출 큐-분리(df_gap 0.700 vs habituation 0.000) · ablation 붕괴
  (INHIBIT=0 → 0.000) · shuffle 붕괴(큐-항목 perm → 0.030). 양 control(ablation+shuffle) 모두 분리를 무너뜨림
  = 분리는 의도적 큐-억제가 **벌어 낸 것**(artifact 아님).
- **SCOPE TOY:** 8 항목/3 seeds/스칼라 결정 회상법칙 — directed forgetting STRUCTURE 검증이지 학습된 억제 네트워크
  아님. scale/real-corpus/억제강도 추정/think-no-think paradigm 일반화/retrieval-induced forgetting/engine-transfer
  UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` directed-forgetting lane 배선(§DirectedForgetting:
   df_new/_cue/_recall — forget-큐 항목에 억제게인 적용, remember 보존). engine 결정적 스칼라 op 로 4 frozen bar
   byte-exact 재현(engine exp 없음 → linear, H_1465 선례) + regression smoke + ARCHITECTURE.json lockstep
   (`a_engine_native_learning`·`a_verified_must_wire` 4칸 사다리).
2. **distinctness engine-native** — vs H_1465 habituation(반복-감쇠) · H_1227 immune-store(수동 회상)
   control-survived 재측정.

xref: H_1465(habituation, distinct — passive vs active)·H_1227/H_1231(immune-store, distinct)·H_1289(novelty)·
H_1476(emotion regulation, 2차 제어 sibling)·H_1475(G22, 직전 게이트)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
