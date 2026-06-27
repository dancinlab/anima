# $0 결정 스크린 — 곱셈 vs 덧셈 binding operator (DIRECTIONAL)

archbrainstorm 82 카드(H_1604–H_1685)를 가로지른 **수렴명제** = "binding 결손의 빠진 operator는 곱셈형(Hadamard/coincidence/AND); 덧셈(conv·attention의 sum)은 못 한다"(H_1603 진단 · TOP-3 H_1617/1605/1606 공유). 이를 무료 numpy 토이로 선별 검정. **DIRECTIONAL only**(numpy toy, engine-native 아님 — `a_engine_native_learning`).

코드: `binding_op_screen.py` · 토이: 2 슬롯 feature-binding(shape×color), label="red square 있음".

## 결과 (정직 · frozen-first, tune-to-green 금지)
| 측정 | additive(sum) | bind(Hadamard) | frozen bar | 판정 |
|------|--------------|----------------|-----------|------|
| full-set acc | **0.876** | 1.000 | add ≤0.65 ∧ bind ≥0.95 | **bar 미충족** (NOT-SUPPORTED) |
| ambiguous subset (binding 필수) | **0.50** (강제) | **1.00** | add=0.50 ∧ bind=1.00 | 진단 확인 |

- **강한 명제 반증**: "덧셈 항상 실패"는 거짓 — 덧셈은 marginal 지름길(red 있음∧square 있음 상관)로 full-set 0.876 획득. bar 안 옮김(honest, c9).
- **약하지만 결정적**: binding이 *진짜 요구되는* ambiguous pair에서 덧셈 rep은 양/음 **동일**(`[1,1,1,1]==[1,1,1,1]`) → 증명적 0.50, Hadamard rep 분리(`[1,0,0,1]≠[0,1,1,0]`) → 1.00.
- **G1≡G6 기전 일치(H_1603)**: 덧셈의 0.876 = "coherent-but-not-composed"의 정체(co-occurrence 통계로 유창해 보임) · ambiguous 0.50 = 실제 재조합/착상 실패. 모델이 binding op 없이 통계 지름길로 fluent한 게 정확히 G1/G6 벽.

## 함의 (GPU 결정용)
- 82 카드 중 **곱셈/coincidence operator family**(H_1617 nmda·H_1605 dendritic·H_1606 cerebellar-expansion·H_1466 TPR·H_1514 HRR)가 1순위 — 덧셈 trunk(conv/attention)에 빠진 바로 그 op.
- 단 marginal 지름길 경고: GPU ARM-BIND 검증은 **ambiguous(binding-required) 케이스를 분리 측정**해야 함 (full-set acc는 덧셈도 통계로 부풀려짐 = G1 bar가 max_single 비교인 이유와 동형).
- 다음 = H_1603 EXP-3 ARM-BIND를 **Hadamard binding op**로 구체화 → 303M cost-gated GPU(frozen G1 multiseed + G6 dist≥5∧fals≥1 + held-out DESCENT + engine-native 재측정 + ckpt PULL).
