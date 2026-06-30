# H_1821 — Homomorphism-Error cheap G1 pre-screen (numpy 진단)

**id:** H_1821
**slug:** homomorphism_error_probe
**tier:** 🔵 BUILT + SELF-VALIDATED (DIRECTIONAL · numpy-only · $0 · p7 proxy · 2026-06-29)
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

---

## Verdict (2026-06-29 · r1 · 기존연구 lane · $0 numpy mac)

**🔵 BUILT + SELF-VALIDATED (DIRECTIONAL)** — `state/g1_homomorphism_error_probe/he_probe.py`
(numpy-only, torch-free, reps from `core/clm_decode.py` byte-faithful CLMConvMoE forward).
실측 stdout = `state/g1_homomorphism_error_probe/RESULT_stdout.txt`, 분석 = `RESULT.md`.

**(self-test) SEPARATES PASS** — additive-homomorphic reps → HE_add=0.000, hadamard-homomorphic
→ HE_hada=0.000, random → HE≈1.42–1.71. 메트릭이 합성보존을 실측(상수 아님).

**(real .clm) 3 ckpt 전부 G1-floor (G1≈0):**

| ckpt | HE_add | shuffle ctrl | HE_hada | 대조(shuffle−true) |
|---|---|---|---|---|
| ce_marginal_seed7 | 1.258 | 1.607 | 6.966 | add +0.349 |
| pc_bind_seed7     | 1.232 | 1.541 | 7.871 | add +0.309 |
| n6n7_seed4307     | 1.381 | 1.736 | 3.140 | add +0.355 |

**controls bar PASS** — shuffle(불일치 타겟) HE 가 true HE 보다 일관 ↑(add +0.31…+0.36, 3/3) =
HE 가 *진짜* 합성구조 측정(스크램블 시 homomorphism fit 악화).

**예측력 bar = UNMEASURABLE-at-floor** — G1-PASS .clm 이 *어디에도 없음*(전 캠페인 floor,
best_distinct≤1). positive class 0개라 AUROC/분리 주장 불가. floor ckpt 들은 HE_add≈1.2–1.4
(homomorphic 0.0 보다 한참 위, random ~1.7 보다 약간 아래 = 약한 additive 합성, G1=0 과 정합).
hadamard HE(3–8)≫additive = additive-residual ConvMoE trunk 의 native 합성은 + 이지 ⊙ 아님
(H_1818 Hadamard-bind NOT-SUPPORTED 과 정합한 directional hint).

**frozen prediction (다음 positive 용):** G1-PASS ckpt 는 HE_add < 0.9 (현 floor band 1.2–1.4
아래)여야 함 — falsifiable, 첫 G1>0 arm 등장 시 검증.

**next round:** HE on combo-c(H_1819 op+recomb-objective) arms post-landing — G1>0 첫 positive 면
HE_add<0.9 frozen pred 검증 → self-validated→predictive-tested 승격. 부차 = clm303_clean.clm
floor 데이터점 추가(positive 아님, direction-only).

⚠️ DIRECTIONAL only (p7) — terminal G1 verdict 아님, engine-native `anima evaluate` 가 SSOT.
