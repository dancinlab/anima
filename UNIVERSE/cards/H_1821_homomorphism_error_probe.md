# H_1821 — Homomorphism-Error cheap G1 pre-screen (numpy 진단)

**id:** H_1821
**slug:** homomorphism_error_probe
**tier:** 🔵 PRE-REGISTERED (미측정 · cheap numpy 진단 · $0)
**date:** 2026-06-29
**source:** 외부 문헌 2차조사 (An & Du, NeurReps 2025 #142, [[lit-binding-objective-external-arxiv]])

---

## Hypothesis

Homomorphism Error(HE) = 표현이 합성연산을 보존하는 정도(개념쌍 expression-space ↔ trunk
internal-rep 의 근사 homomorphism 편차). An & Du 2025: **HE가 OOD 합성일반화를 R²=0.73으로 예측**.

**예측:** anima .clm trunk penultimate에 HE를 numpy로 계산하면, 비싼 G0-G6 GPU eval 전에
**G1 통과 여부를 예측**할 수 있다(낮은 HE → G1 lift 가능성↑). 흩어진 GPU eval 대신 cheap pre-screen.

---

## Design (numpy · torch-free · $0 · DIRECTIONAL 진단)

1. 개념쌍 {A, B} 코퍼스 표본 → trunk penultimate 표현 r(A), r(B), r(A∘B) 추출.
2. 합성 연산자 ⊕ (additive 또는 bind)에 대한 homomorphism 편차:
   HE = E‖ r(A∘B) − (r(A) ⊕ r(B)) ‖ / E‖r(A∘B)‖ (정규화).
3. 여러 .clm(H_1818 bind/ctrl, H_1819 op_obj, clm303_clean)에 HE 계산 → **HE vs 실측 G1
   distinct 상관**을 본다 (HE가 G1=0 floor를 예측하나?).

**검증 = reference-match:** An & Du의 SCAN-style HE 정의를 그대로(소스 보고 맞춤, byte 아닌 표현
공간). anima는 byte-CLM이라 expression-space = 개념-토큰 span으로 매핑(transcend-axis 명시).

---

## Frozen bar (pre-registered · p7)

| 항목 | bar |
|------|-----|
| 예측력 | HE가 G1-PASS .clm vs G1-floor .clm을 분리 (AUROC≥0.7, ≥4 ckpt) |
| 인과 | HE 낮춘 학습 변종이 실제 G1 lift (H_1820와 결합 검증) |
| controls | shuffle 개념쌍 → HE 무의미(↑) 확인 (진짜 합성구조 측정임을 입증) |

---

## 게이트 & 가치

- **(c)-independent · $0** — GPU 불필요, 기존 .clm으로 즉시. 단 DIRECTIONAL 진단(verdict 아님,
  실 G1은 engine-native eval이 SSOT). HE는 **어디에 GPU를 쓸지 고르는 cheap 나침반**.
- 산출 = state/g1_homomorphism_error_probe/{he_probe.py, RESULT.md} + 이 카드 + jsonl.
- ⚠️ proxy 함정(p7): HE는 G1 *예측자*지 G1 *정의*가 아님 — terminal verdict로 승격 금지.
