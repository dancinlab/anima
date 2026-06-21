# H_1511 — 🫧 OSMOTIC-MITOSIS / KL>C 삼투압 분열 — split-TIMING overwrite-avoidance

- **tier:** 🟢 GREEN-DIRECTIONAL ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact). split-TIMING 결과이며 binding-capacity 천장(H_1456)을 깬다는 주장 아님.
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §OsmoticMitosis (`osmotic_store_new`/`osmotic_should_split`/`osmotic_learn`/`osmotic_retains`/`osmotic_cells`/`_kl_div`) · `engine_cli_smoke.hexa` cases 323-327 · FULL smoke **318 pass / 0 fail RC=0** deterministic ×3 · ARCHITECTURE.json §OsmoticMitosis lockstep ✓
- **source:** **external proposal — Amoeba Protocol (@qingkong66) — "KL>capacity osmotic mitosis"**. anima 의 mitosis(VAdaptField, H_1199)를 정보-이론 trigger 로 확장하자는 외부 제안.
- **artifacts:** `state/1511_osmotic_mitosis/h1511.py` (R1 mirror) · `state/1511_osmotic_mitosis/probe.hexa` (R2 engine probe) · `state/verdicts/1511_osmotic_mitosis/{H_1511_R1.txt,H_1511_R2_engine.txt}`

## 제안 (external — Amoeba Protocol)

anima 의 기본 split trigger(`vadapt_field_step`)는 L2 reconstruction error 가 frozen `SPLIT_THRESH`(0.30)를 넘으면 cell 을 분열시키고, 그 아래면 winner 를 **REFINE** — value 를 운반하는 store(H_1231 immune faculty)에선 winner 의 bound value 를 **OVERWRITE**. 제안은 정보-이론 항을 더해 cell 의 bottleneck 이 Shannon capacity `C` 를 넘치면 grounded fact 를 덮어쓰는 대신 **분열(1→2)**해서 새 truth 를 수용하게 한다:

> **Trigger Mitosis IF  L_recon + β·D_KL(P(Z_cell) ‖ P(Z_prior)) > C**

`P(Z_prior)` = winner cell 의 bound value-distribution, `P(Z_incoming)` = 새 fact 의 value-distribution. metric 으론 **가깝지만**(near-key → standard 가 refine) **의미상 발산**하는(high KL) 새 grounded fact 가 올 때, standard 는 원본을 조용히 덮어쓰는데 osmotic 은 분열로 **둘 다 보존**.

## 무엇을 검증하나 — SPLIT-TIMING, NOT capacity-wall (load-bearing, vs H_1456)

H_1456 은 **BINDING capacity** 천장(WALL=CAPACITY: comparator+measurable 를 falsifiable claim 으로 WELD 못함)을 5개 렌즈로 확정했다. **본 가설은 그것과 별개 축**이다:
- 본 가설은 total binding capacity 가 **오른다고 주장하지 않는다**.
- 모든 arm 의 `max_cells`(capacity cap)는 **동일**하다.
- osmotic trigger 는 grounded fact 를 **적시 분열로 덮어쓰기 회피**할 뿐 — retention gain 은 **timely division** 이지 capacity 증가가 아니다(C-bar honesty 로 명시 측정).

## Frozen 5-bar (측정 前 FREEZE — c9, tune-to-green 금지)

deterministic fixture: 4 grounded fact, 각자 ONE near-key update(2 COLLISION = near key·divergent value·high KL / 2 BENIGN = near key·~same value·KL≈0). cap=6 (ideal osmotic 4 grounded + 2 collision split = 6 fits; 무차별 분열은 cap 소진).

- **A NO-OVERWRITE**: osmotic grounded-fact retention ≥ 0.90.
- **B vs STANDARD**: osmotic − standard ≥ 0.50 (같은 시나리오, KL-trigger 보존 ⊥ error-trigger 망각 = 해리).
- **C CAPACITY-HONEST** (honesty bound, pass/fail 아님): cap 모든 arm IDENTICAL; osmotic cells ≤ cap. retention gain = 적시 분열, capacity 증가 아님 (H_1456 천장과 구별).
- **D EARNED ablate**: β:=0 (pure L_recon) → overwrite 행동으로 복귀, retention_ablate ≤ standard + 0.10.
- **E EARNED shuffle**: Z↔prior 순열로 KL 을 진짜 collision 과 decorrelate → retention_shuffle ≤ standard + 0.10.
- **GREEN iff A ∧ B ∧ D ∧ E** (C 는 정직 bound). KL>C 가 기존 VAdaptField 행동을 **재유도**할 뿐(standard 대비 retention gain 없음)이면 → 정직한 finding: 제안은 새 capability 아닌 re-derivation, 그대로 보고.

## VERDICT 🟢 GREEN-DIRECTIONAL → ENGINE-NATIVE WIRED (re-derivation 아님)

| arm | retention | 해석 |
|---|---|---|
| STANDARD (error-trigger) | **0.500** | collision 2개 전부 OVERWRITE (grounded 원본 소실), benign 2개만 보존 |
| OSMOTIC (KL>C) | **1.000** | collision 마다 SPLIT → 원본+새 fact 둘 다 보존 |
| ABLATE (β=0) | **0.500** | = standard 정확히 복귀 (earned, D PASS) |
| SHUFFLE (KL decorrelated) | **0.500** | = standard (보호 분열 소실, earned, E PASS) |

- **A** osmotic 1.000 ≥ 0.90 PASS · **B** +0.500 ≥ 0.50 PASS · **C** cap=6 동일·osmotic 6 cells(4 grounded+2 split)·standard 4 (capacity 증가 아님) · **D** 0.500 ≤ 0.600 PASS · **E** 0.500 ≤ 0.600 PASS → **GREEN**.
- **R1 numpy mirror** (`h1511.py`, 3 seeds [4511,4512,4513] **byte-identical**) → **R2 engine-native byte-exact** (`probe.hexa` + smoke 323-327, FULL 318/0 RC=0 ×3).
- engine ops 는 **live VAdaptField** key geometry(`_l2`/`_vnearest_idx` — vadapt_field_step 이 쓰는 SAME affinity)+per-cell value table(H_1231 immune idiom)을 READ. Ψ-disjoint, NOT emit gate(a_autonomy_over_hardcode). DEFAULT `vadapt_field_step` 경로는 **UNTOUCHED** (opt-in trigger).

## 정직 (c9)

- **re-derivation 아님**: standard 가 못 지키는 grounded fact 를 osmotic 이 SPLIT-timing 으로 보존하며, KL 항을 ablate(D)/decorrelate(E)하면 그 gain 이 **정확히 사라진다** → gain 은 KL>C 메커니즘에서 **earned**. 즉 제안은 VAdaptField 의 단순 재표현이 아니라 overwrite-avoidance 라는 **새 행동**을 더한다.
- 단 retention 1.000 = **SATURATED = EXISTENCE-PROOF**, effect-size 아님. 시나리오는 osmotic 이 겨냥하는 regime(near-key·divergent-value collision)으로 **설계**됐다 — 공정한 존재증명이되, 일반 corpus 빈도/효과크기 주장 아님.
- **하드게이트1(a_engine_native_learning)**: R1 `h1511.py` 는 numpy → DIRECTIONAL. R2 는 **engine-native WIRED** (`.hexa` via live `core/engine_cli.hexa` §OsmoticMitosis), byte-exact 재측정·smoke 323-327·ARCHITECTURE.json lockstep 완료.

## SCOPE (UNVERIFIED)

TOY 4 grounded/2 collision/2 benign·deterministic fixture(overwrite-avoidance STRUCTURE 검증, 학습된 trigger 아님)·β/C/cap frozen 상수. scale·real-corpus·연속 KL·다중 collision 순서·β·C sweep·brain memory-write 경로 배선·engine-transfer-at-scale **UNVERIFIED**.

xref H_1199(VAdaptField mitosis) · H_1231/H_1227(immune cell-indexed value store) · H_1456(WALL=CAPACITY binding 천장, **별개 축**) · `vadapt_field_step_entropic`(H_1289 split-timing entropy jitter, 다른 메커니즘) · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · p7 · p8 · c9
