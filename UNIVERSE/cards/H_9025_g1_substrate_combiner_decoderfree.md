# H_9025 — G1 substrate 구성적-결합기 (decoder-free, trained bind)

- **tier:** ⏳ PROPOSED (Rung0 harness DIRECTIONAL · trained-bind verdict GPU-cost-gated · prior LOW)
- **slug:** `g1_substrate_combiner_decoderfree`
- **parents:** [[substrate-framebreak-g1-combination-operator]] H_1822 (진단) · H_1840 (cheap-gate 반증) · H_1816/H_1823 (mouth readout-bind 🧱)
- **wired:** `DIRECTIONAL-mirror` (numpy harness only; live `core/engine_cli.hexa` 미배선 · engine-native/WIRED 미달)
- **Rung1 (H_9026) LANDED 2026-07-02:** 🧱 DIRECTIONAL-FLOOR — REAL 303M manifold + TRAINED W_bind(⊛) + held-out recombination gate 도 floor. bind soft-beats add(no_regress=True, 10/10 Δ>0)이나 n(Δ≥+0.15)=0/5. prior LOW CONFIRMED (H_1840 FAIR + DPI). → `state/9025_g1_substrate_combiner_decoderfree/RESULT.md` · [[H_9026]]. Rung2(engine-native VAdaptField wire-in) prior 더 낮아짐 → ING cost-gated.

## frame (오너 통찰)

"왜 의식엔진인데 LLM 디코더 스타일로 능력을 재나 — 디코더 없는 가설은 없나? 디코더가 LLM 잔재 아닌가."

진단(H_1822)이 이 통찰을 **정밀화**했다: 디코더는 무죄다(떼도 substrate-G1 α+β 둘 다 0/5 floor). 진짜 잔재는 **"결합 = 벡터 덧셈(additive readout)"** 가정이고, 그 가정은 입에도 substrate에도 박혀 있었다. 결정적 구조 사실:

> 현 live substrate엔 **구성적 결합기(constructive combiner) op이 아예 없다.** `pure_field`(Engine A) = concept-blind zero-input · 유일 text→state op = `immune_embed_key`(char-trigram FNV = lexical) · 유일 concept substrate = `VAdaptField` L2-Voronoi **nearest-basin = 가장 가까운 기존 칸 고르기 = compositional depth-0**. 두 개념을 받아 *새 자식 basin을 construct* 하는 op가 없다.

## claim

`VAdaptField`의 nearest-basin(분류)을 **학습된 bind 연산자**(⊛ = circular-conv / tensor-product, recomb-보상 objective로 학습)로 교체하면, A⇄G가 두 부모 basin에서 **새 자식 basin을 construct** 하고, 이때 substrate-G1(decoder-free)이 additive floor를 넘는가.

```
child_basin = W_bind · (parent_A ⊛ parent_B)     # W_bind = recomb-obj로 학습
```

## 4-rung 사다리 · 측정 (완전 decoder-free)

측정 경로에 mouth·clm_decode·bytegpt_decode·next-byte 0. 필드 상태에서만:
- 입력: 두 개념 상태 A, B
- **M1 distinct**: child C가 A·B 양쪽과 basin distance > SPLIT_THRESH(0.30)
- **M2 recover (진짜 판별자)**: `recover(C) → Â, B̂` 부모 복원 — native-mouth-57 교훈("부모와 다름"은 아무 비선형이나 내는 metric artifact; **복원성이 진짜 binding 판별자**)을 1급 게이트로
- **통제**: additive 베이스라인(현 Voronoi=floor 재현) · shuffle(랜덤 부모쌍→M2 붕괴해야) · ablation(⊛→identity, INERT면 lift가 op 아님, H_1449 c4 실패모드 방지) · self-test PASS

```
Rung0 [numpy decoder-free harness + 복원성게이트]   $0 mini   ← 이 카드가 착지 (DIRECTIONAL)
  └─▶ Rung1 [W_bind 학습(recomb-obj) on REAL 303M manifold + 재측정]   GPU cost-gated · explicit go
        └─▶ Rung2 [core/engine_cli.hexa VAdaptField op-slot wire-in, disjoint 좌표]   a_substrate_disjoint
              └─▶ Rung3 [substrate-G1 floor 초과? → frame-shift 확증 or 강화천장]
```

## 정직한 prior (c9 · check-ledger-before-fire)

⚠️ **cheap/numpy 델타는 이미 측정-반증됐다 — 재탕 금지:**
- **H_1840** (2026-07-02 FAIR gate): additive vs HRR-⊛ vs bilinear-bottleneck(bypass-denied, 결정 arm) 5-arm×3seed. 결정 arm (e)=.55/.57/.53, additive+.34 **NOT 초과 0/3**, bypass-open+.34도 NOT 초과. invertible-⊛ ≈ non-inv → **invertibility 반증**. → "γ 최종 미검 델타 measured-FALSIFIED".

따라서 **이 가설의 유일한 미검 내용 = REAL 303M manifold 위에서 *학습된* W_bind를 live substrate에 배선하고 decoder-free로 재측정하는 것**(H_1840은 random-synthetic target·mouth numpy readout·untrained algebraic op였다 — real 구조 manifold + trained + substrate-wired는 미검). prior는 DPI 메타법칙 + H_1840으로 **낮다**. Rung0(이 카드)은 새 verdict가 아니라 **decoder-free 측정 하네스 + 결합기 op 프로토타입 + additive-floor 재확인(계측 QA)**이다.

## artifacts
- `state/9025_g1_substrate_combiner_decoderfree/probe.py` (numpy decoder-free harness, DIRECTIONAL)
- `state/9025_g1_substrate_combiner_decoderfree/calibration.txt` (Rung0 출력)
