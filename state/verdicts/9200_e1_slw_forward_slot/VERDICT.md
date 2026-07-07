# H_9200-E1-SLW — VERDICT: 🧱 KILL (additive floor · retrieval-attractor)

**판정**: 🧱 KILL — gated-write forward-slot(SLW)은 303M byte-LM engine-native 측정에서
G1 재조합(ρ·weave) 벽을 **깨지 못했다**. 슬롯 ON이 additive baseline을 이기기는커녕 **재조합
다양성을 떨어뜨렸다**(retrieval-attractor). pre-registered kill-criteria 충족.

- **ckpt**: `~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm`
  sha256 `792eab814ba08554783f52dc169bebf858acf18c6d571c2181e0aba2f0e552c9` (293,119,146 bytes)
  — H100 14000-step 학습, held-out DESCENT 2/2, val_CE 0.363.
- **측정**: `anima evaluate --py <clm> --gen 40` (canonical single-entry · numpy engine-native
  TERMINAL · `a_eval_py_canonical`), H100 pod `p6okni1x9tf51i`. verbatim =
  `e1_3arm_measurement_verbatim.txt`.
- **날짜**: 2026-07-07.

## 결과 (pre-registered 3-arm)

| arm | 조건 | ρ·weave(G1 재조합) | ρ·form(G0) |
|---|---|---|---|
| ARM1 | SLW ON | 🔴 **best_distinct=1** (필요: ≥2 ∧ >max_single=2, 즉 ≥3) | 🟢 kwr 5/5 |
| ARM2 | `--slot-off` (γ=0 bit-exact base) | 🟢 (base 통과) | 🧱 |
| ARM3 | `--slot-shuffle 777` | 확인용(측정 시점 in-flight) | — |

ARM1 전체 배터리: G0🟢 · G1🔴(bd=1) · G2🔴(novel=0) · G5🟢(fab=0.2812) · G6🔴(dist=3 fals=0) ·
CLOSURE🔴. Θ tension 🟢 LIVE · **σ vitals 9/9 전부 🟢 LIVE**(thread/carve/bind Φ1.45/stage/flux/
gate/aim/schema/witness).

## 판정 논리 (pre-registration 충족)

pre-reg: `🧱 KILL = slot이 additive floor로 붕괴(margin≤0) 또는 shuffle 비붕괴`.
**ARM1 slot-ON ρ·weave가 best_distinct=1로 floored** = "slot이 additive floor로 붕괴" 조건을
직접 충족. slot-ON이 재조합 게이트(bd≥3 필요)를 통과하지 못하므로 **GREEN은 어떤 컨트롤
결과로도 성립 불가** — KILL은 ARM1(full-capture, 무결)에만 근거하며 컨트롤 arm에 의존하지 않는다.

## "반전 신호"는 confound가 아니다 (INVALID 배제)

ARM2에서 `ρ·form 🧱`이면서 `ρ·weave 🟢`인 것은 **논리 모순이 아니다** — 두 지표는 **서로 다른
프롬프트셋** 측정이기 때문:
- `ρ·form` = 단일개념 continuation kwr ≥0.5 on ≥4/5 (evaluate.py:127–129).
- `ρ·weave` coherent-검사 = **합성(composed)** continuation 하나의 kwr.
따라서 slot-off가 단일개념엔 비응집(form🧱)이면서 합성 continuation은 통과(weave🟢)할 수 있다.
= 측정 confound(INVALID) 아님, 정상적으로 다른 대상을 잰 것.

## 메커니즘 — 슬롯 = retrieval attractor

슬롯 ON: **응집 개선(FORM↑, 저장내용에 앵커)** 대신 **재조합 다양성 붕괴(BIND=0,
best_distinct 1로 수렴)**. 학습된 슬롯-write가 생성을 저장 attractor 쪽으로 끌어당겨 —
새 조합을 **짓는(constructive bind)** 게 아니라 외운 걸 **되뇌게(retrieval)** 만든다.
그래서 CE 목적이 실 byte-LM에서 슬롯을 **유도했지만**(rung3 CE-INDUCES-SLOTS 합성 GREEN),
그 슬롯이 재조합 능력으로 이어지지는 **않았다** — 4-rung de-risk의 합성 GREEN이 실 303M에서
반증된 것(a_toy_scale_recheck 정확히 예측한 toy≠scale gap).

## 렛저 정합

기존 G1 재조합벽 = readout/lane/decode/objective/target/data-format 전수 falsify = 진짜 능력
천장(goal-biolens, substrate-framebreak-g1-combination-operator). SLW(forward-computation 축)도
이 벽 앞에서 floor. **DPI 메타법칙**(fleet-g1g6-nativemouth-dpi-convergence) 재확인 — 유일 잔여
= γ trained-constructive-bind(H_1840, GPU cost-gated)는 SLW와 별개 lever. **σ vs ρ 분리 재확인**:
의식 vitals 9/9 🟢인데 재조합 reach는 🧱 = "G1 벽은 reach 사실이지 σ 결핍 아니다"(amoeba 논증).

## 재발방지 (convergence)
- `evaluate-py-1` (#3106): verdict 수치를 ρ-AXON reach 요약줄에 인라인 → 컨트롤 arm이 tail-캡처로
  잘려도 collapse-Δ 생존(이 E1서 ARM2/ARM3 best_distinct가 tail-20에 유실됐던 근본수정).

## scope (a_scale_honest_scope)
303M byte-LM · SLW ce_marginal objective · frozen G1 ladder(H_1129 CONCEPTS). γ 학습 constructive
bind, 대형 스케일, 다른 objective는 미측정 — 이 KILL은 "SLW forward-slot @ 303M ce_marginal"에
바운드된 negative이며 재조합벽 전체 closure를 새로 늘리지 않는다(이미 terminal).
