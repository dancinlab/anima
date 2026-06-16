---
id: H_1417
slug: 1417_compose_bind_law_predictive
title: "brain-lane COMPOSE engine-BIND LAW — DESCRIPTIVE → PREDICTIVE: pre-register BIND/🧱 on 5 UNTESTED engine pairs from the ceiling-erosion predictor, then engine-native re-score, then score HIT/MISS (frozen-first falsification of the strength-erosion law)"
group: MITOSIS-ENGINE / brain-lane-composition — the engine-BIND law's PREDICTIVE falsification round (the engine-native twin of H_1411's Φ-lift falsification)
terminal_tier: "🧱 ENGINE-BIND-LAW PREDICTIVELY-FALSIFIED (2/5 HITS) — the descriptive 'ceiling-erosion / strong-standalone-arm' rule does NOT survive pre-registered prediction; the real determinant is ARBITER-CAPTURE of the oracle headroom (a JOINT-trajectory property), NOT standalone-arm strength"
wired: N/A for the 🧱 falsified LAW (MEASUREMENT round — the law itself wires nothing). The TWO BIND by-products (P3 ToM×spatial, P5 ToM×basal) ARE now WIRED-live via H_1418 (§ToM×SPATIAL / §ToM×BASAL COMPOSE ARBITER tom_spatial_compose / tom_basal_compose in CORE/engine_cli.hexa, smoke 141-148, LIVEOP byte-exact, ARCHITECTURE.json lockstep) — see UNIVERSE/cards/H_1418_tom_compose_pairs_wired.md
verdict_dir: .verdicts/1417_compose_bind_law_predictive/
terminal_verdict: .verdicts/1417_compose_bind_law_predictive/result.txt
date: 2026-06-17
---

# H_1417 — brain-lane COMPOSE engine-BIND LAW: DESCRIPTIVE → PREDICTIVE

이 카드는 H_1411 이 옛 Φ-lift 法則에 한 것을, 새로 떠오른 **engine-BIND 법칙**에 똑같이
적용하는 사전등록 반증 라운드다 (a_verified_must_wire 사다리의 과학적 격상). 처음 4개의
engine-native compose 재채점에서 법칙이 **DESCRIPTIVE** 하게 떠올랐다:

- H_1412 cerebellum×basal → 🧱 BIND 안 됨 (B1 net-lift +0.011 < +0.05)
- H_1413 cerebellum×basal (modulation lens) → 🧱 (EARNED control 이 가짜 lift 기각)
- H_1414 memory×ToM → 🟢 BOUND (B1 +0.338)
- H_1415 spatial×episodic → 🟢 BOUND (B1 +0.058)

## Claim / falsifier

**시험 대상 DESCRIPTIVE 법칙 (FREEZE.txt, H_1414/H_1415 카드에서 verbatim):**
> mirror compose-GREEN 은 engine-native 로 BIND 한다 IFF 어느 live standalone faculty 도
> mirror best-single ceiling 을 +0.05 net-lift headroom 이상 넘어서지 **않을 때**.
> ceiling-PINNED (두 arm 모두 ceiling+0.05 이하) → oracle headroom 이 arbiter 가 잡을 수
> 있게 남아 BIND 🟢. ceiling-ERODING (한 arm 이 ceiling 을 넘어 강해짐) → 강한 standalone
> arm 이 +0.05 net-lift headroom (B1=compose vs best_single) 을 먹어치워 BIND 실패 🧱.
> cerebellum×basal 이 실패한 건 live gradient-free `VBasalGate` 가 강한 standalone arm
> (acc_basal 0.703 > mirror ceiling 0.693) 이었기 때문.

**PREDICTIVE claim (반증자):** 이 법칙을 PREDICTOR 로 조작화해 5개 미시험 pair 의 BIND/🧱
를 **측정 전에** ceiling-erosion predictor 로만 예측하고(FREEZE.txt 잠금), THEN engine-native
compose 재채점, THEN HIT/MISS. 예측==실측이 ≥4/5 면 법칙 SURVIVE (DESCRIPTIVE→PREDICTIVE 🟢);
<4/5 면 FALSIFIED 🧱 (H_1411 의 2/5 처럼). MISS 가 가장 값진 데이터 — 진짜 determinant 를
이름붙인다 (c9, tune-to-green 금지).

## 사전등록 PREDICTOR (FREEZE.txt, 측정 전 잠금)

후보 pair (X,Y) 에 대해:
- `ceiling_mirror` = 0.70 (family ceiling; landed fixture 들이 realize 하는 값, FREEZE 고정)
- `acc_X_live, acc_Y_live` = 각 faculty 의 LIVE standalone 정확도
- `strength_excess = max(acc_X_live, acc_Y_live) − ceiling_mirror`
- **PREDICT BIND 🟢 iff `strength_excess ≤ +0.05`** · **PREDICT 🧱 iff `> +0.05`**

PREDICTION INPUTS (faculty live-strength 사전값, **PRIOR engine 측정에서만** — 이번 compose
를 돌려보지 않고 blind): memory PINNED~0.58-0.70 · ToM PINNED 0.600 · spatial PINNED~0.70 ·
cerebellum WEAK 0.638 · **basal STRONG 0.703-0.71 (the eroder, H_1412)**.

## Method (engine-native, frozen-first)

5개 NEW pair (아직 engine-미시험), 각 leg = LIVE engine read (a_core_engine_map): memory =
`immune_grow_recall` + live L2 affinity margin · ToM = `other_mind_predict` + live margin ·
spatial = `spatial_map_nearest` + live metric margin · cerebellum = `vforward_err` ·
basal = `vbasal_go_value` (gradient-free `vbasal_update` 로 양의 go-weight 학습). 5-family
fixture (F0 X-decisive · F1 Y-decisive · F2 agree · F3 conflict-X-right · F4 adversarial-
X-loud-wrong), N_PER_FAMILY=90 → 450 items/seed, 3 seeds/pair, deterministic. arbiter =
inlined scale-relative confidence (agree→shared; one-abstain→other; conflict→higher rel-conf).
**FROZEN bars (H_1407/1414/1415 와 동일, NOT moved):** (B1) compose≥best+0.05 · (B2)
oracle−best>0.02 · (B3) compose−shuffle>0.02 · (SEPARABLE) only_X>0 AND only_Y>0. ACTUAL =
🟢 iff (B1∧B2∧B3∧SEP); else 🧱. p7 (정확도+분해), NOT perplexity. $0 CPU, live CORE/*.hexa UNTOUCHED.

## Verdict by round — predicted vs actual (mean 3 seeds, engine-native, verbatim result.txt)

| pair | acc_X | acc_Y | best | strength_excess | compose | net-lift | B1 | PREDICTED | ACTUAL | |
|------|-------|-------|------|-----------------|---------|----------|----|-----------|--------|---|
| P1 memory×spatial    | 0.6044 | 0.7059 | 0.7059 | +0.0059 | 0.7148 | +0.0089 | FAIL | BIND | **🧱 WALL** | ❌ MISS |
| P2 memory×basal      | 0.6459 | 0.7022 | 0.7022 | +0.0022 | 0.7519 | +0.0496 | FAIL | 🧱   | **🧱 WALL** | ✅ HIT  |
| P3 ToM×spatial       | 0.7022 | 0.6963 | 0.7022 | +0.0022 | 0.7911 | +0.0889 | PASS | BIND | **🟢 BIND** | ✅ HIT  |
| P4 cerebellum×memory | 0.6948 | 0.6170 | 0.6948 | −0.0052 | 0.7385 | +0.0437 | FAIL | BIND | **🧱 WALL** | ❌ MISS |
| P5 ToM×basal         | 0.6963 | 0.7059 | 0.7059 | +0.0059 | 0.8015 | +0.0956 | PASS | 🧱   | **🟢 BIND** | ❌ MISS |

(모든 pair B2/B3/SEP PASS — compose 는 REAL & EARNED; 갈리는 건 B1 net-lift 뿐.)

**HIT/MISS TALLY (frozen bars): 2 / 5 HITS** → 3 MISSES. Deterministic (run1==run2 byte-identical).

Terminal tier (verbatim): **🧱 ENGINE-BIND-LAW PREDICTIVELY-FALSIFIED** [the descriptive
ceiling-erosion / strong-standalone-arm rule does NOT survive pre-registered prediction — 2/5
HITS] → `.verdicts/1417_compose_bind_law_predictive/result.txt`

## Result — the finding (the MISSES are the payload, c9)

**DESCRIPTIVE 법칙은 사전등록 반증을 통과하지 못했다 (2/5)** — H_1411 과 정확히 같은 결과.
세 MISS 가 각각 다른 교훈을 준다:

- **P5 ToM×basal (예측 🧱 → 실측 🟢 BIND):** 가장 결정적인 miss. 법칙의 핵심 사전값 —
  "basal 은 강한 standalone arm 이라 ceiling 을 침식한다 (H_1412)" — 이 **틀렸다**. 이 fixture/
  pair 에선 live `VBasalGate` 가 ceiling 을 넘지 못했다 (acc_basal=0.7059 ≈ ceiling 0.70,
  strength_excess +0.006). 그래서 oracle headroom 이 남았고 arbiter 가 잡아 net-lift +0.096
  로 **BIND**. **"basal=eroder" 는 H_1412 의 cerebellum×basal fixture 에 특정한 성질이었지
  basal 의 intrinsic 성질이 아니다** — 같은 live op 이 다른 짝/fixture 에선 ceiling 에 핀된다.
- **P1 memory×spatial (예측 BIND → 실측 🧱 WALL):** 어느 arm 도 ceiling 을 넘지 않았는데도
  (strength_excess +0.006) compose 가 BIND 안 됨 (net-lift +0.009). ceiling-erosion predictor
  는 **arbiter 가 oracle headroom(+0.241)을 실제로 잡을 수 있는지에 BLIND** 하다. 여기선
  routing cue 가 where/what 을 충분히 가르지 못해 conflict 에서 arbiter 가 헛다리 — headroom
  은 컸지만 capture 가 안 됐다. 이게 H_1411 이 찾은 것과 **동일한 교훈**(component 통계가 아니라
  joint-trajectory 가 결정)의 engine-bind 판.
- **P4 cerebellum×memory (예측 BIND → 실측 🧱 WALL):** net-lift +0.044, +0.05 바로 아래.
  cerebellum 의 약한 arm(0.695) + memory 가 합쳐도 arbiter 가 잡은 lift 가 bar 를 못 넘음.
  여기서도 gate 는 arm-strength 가 아니라 **arbiter-capture 효율**이었다.

**REFINED 법칙 (miss 들이 가리키는 진짜 determinant):** engine-bind 는 standalone-arm 이
ceiling 을 침식하는지가 아니라, **routing arbiter 가 oracle headroom 을 실제로 capture 하는지**
(conflict 영역에서 confidence-routing 이 옳은 faculty 를 고르는지) 로 결정된다 — 이는 component
standalone 정확도만으로 계산 불가하고 **joint composed trajectory** 가 필요하다. 5개 pair 모두
큰 oracle headroom(+0.24~+0.30)과 EARNED shuffle-collapse 를 가졌지만, 그 headroom 의 capture
율이 +0.009 (P1) ~ +0.096 (P5) 로 갈렸고, **B1 통과 여부는 전적으로 capture 율이 정했다** —
arm-strength(strength_excess 가 5개 모두 |·|≤0.006 로 거의 동일)는 아무것도 예측하지 못했다.

**왜 H_1412 는 🧱 였나 (재해석):** H_1412 에서 basal 이 "강한 arm" 으로 보였던 건 그 특정
fixture 가 basal 에 유리한 family 균형을 줬기 때문이지, basal 이 보편적 eroder 라서가 아니다.
진짜 원인은 그 pair 의 **F5 adversarial family (cerebellum loud-but-wrong) 가 arbiter-
uncapturable** 했던 것 — 즉 capture-실패였지 arm-strength-침식이 아니었다. H_1417 이 이를
분리해 보였다: arm-strength 를 통제(5개 pair 거의 동일)해도 capture 율이 BIND 를 가른다.

**정직한 meta-point (c9, c16):** 이것이 frozen-first 사전등록 예측의 가치다. DESCRIPTIVE
법칙은 4개 fitted pair 에서 빈틈없어 보였지만, 단 한 번의 사전등록 라운드가 반증했다. 측정된
🧱 는 진짜 arc-닫는 결과 — 법칙을 descriptive-only 로 못박고 진짜 driver(arbiter-capture,
joint-trajectory 성질)를 다음에 형식화할 대상으로 이름붙인다.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

엔진-네이티브 leg-read (immune_grow_recall / other_mind_predict / spatial_map_nearest /
vforward_err / vbasal_go_value 전부 LIVE) 지만 TOY 5-family 합성 fixture (90/family, 3 seeds/
pair, deterministic; compose/INTEGRATION 구조를 시험, 학습된 net 아님). **구성 caveat (load-
bearing):** H_1417 fixture 는 5 faculty 를 공통 family 골격으로 통일한 GENERALIZATION 이라 각
landed probe 의 bespoke fixture 와 byte-identical 하지 않다 — 그래서 basal 의 standalone
strength 가 H_1412 의 0.703 과 이 fixture 의 0.702-0.706 로 거의 같게 나오고(eroder 가 안 됨),
이 점이 P5 miss 의 직접 원인이다. 즉 반증은 "법칙을, 통일된 generalization-fixture 위에서
predictively 적용했을 때" 의 반증이다 (strict generalization test, H_1411 과 동일 성격).
predictor 입력은 PRIOR landed 측정의 strength 값, ACTUAL 은 이번 run 의 측정. Scale/real-
corpus/engine-transfer-at-scale UNVERIFIED. NO bar moved post-hoc; predictions FREEZE.txt 에
측정 전 잠금. compose-program 의 capability-compose 결과(H_1401/1405/1407/1408/1409 🟢)는
UNAFFECTED — 여기선 engine-BIND *법칙*만 반증된다.

**측정 라운드 — 법칙 자체는 live CORE 에 아무것도 배선하지 않음** (법칙을 시험, 메커니즘
landing 아님). 그러나 새로 BIND 한 두 pair (P3 ToM×spatial, P5 ToM×basal)는 **H_1418 에서
WIRED-live 로 landing 완료** — §ToM×SPATIAL / §ToM×BASAL COMPOSE ARBITER (`tom_spatial_compose` /
`tom_basal_compose`, CORE/engine_cli.hexa), smoke 141-148, LIVEOP 가 P3 0.791111 · P5 0.801481 을
byte-exact 재현, ARCHITECTURE.json lockstep, 가드 149/0·7/0·h1205 PASS (a_verified_must_wire
rung-3+4). 카드: `UNIVERSE/cards/H_1418_tom_compose_pairs_wired.md`.

## Next

(1) REFINED driver 형식화 — JOINT composed trajectory 에서 계산하는 **arbiter-capture
predictor** (conflict-region 에서 routing cue 가 옳은 faculty 를 고르는 비율)를 만들고 그것을
predictively 재시험. (2) P3 ToM×spatial · P5 ToM×basal 가 engine-native 로 BIND 했으니 (frozen
bars 통과) 각각의 query-routed arbiter 를 live CORE 에 배선하는 것이 별도 follow-on (ING.jsonl).
(3) basal 이 fixture 에 따라 eroder 가 되기도/안 되기도 함을 보였으니 H_1412 의 🧱 를 "basal
strength" 가 아니라 "F5-adversarial capture 실패" 로 재분류하는 미세 재검토.

## Cross-links

H_1411 (Φ-lift 법칙의 동일 predictive-falsification, 2/5 — 이 카드의 TEMPLATE이자 자매 결과:
둘 다 "component 통계가 아니라 joint-trajectory 가 결정" 으로 수렴) · H_1412 (cerebellum×basal
engine 🧱 — basal=eroder 주장의 출처, P5 가 반증) · H_1413 (modulation lens 🧱) · H_1414
(memory×ToM 🟢 BOUND — ceiling-pinned 사례) · H_1415 (spatial×episodic 🟢 BOUND) · H_1407/1408/
1409 (compose-program mirror siblings) · H_1227/H_1231 (ImmuneMemoryGrow) · H_1293 (OtherMindModel) ·
H_1296 (SpatialMap) · H_1280 (VForwardField) · H_1281 (VBasalGate) · `a_break_the_wall` (taxonomy
(b) conflated-variable: arm-strength 와 arbiter-capture 가 fitted pair 에서 혼재했음) ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_autonomy_over_hardcode` · `a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15·c16

## Pointers
- probe (5-pair engine-native compose + predictor scoring): `state/1417_compose_bind_law_predictive/h1417_compose_bind_law_probe.hexa`
- FREEZE (pre-registered predictions + threshold, locked before measuring): `.verdicts/1417_compose_bind_law_predictive/FREEZE.txt`
- result (HIT/MISS tally): `.verdicts/1417_compose_bind_law_predictive/result.txt`
- determinism re-run: `.verdicts/1417_compose_bind_law_predictive/result_run2.txt`
