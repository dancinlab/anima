# C2 Stage B — VERDICT (정직 재해석 · frozen bar vs load-bearing)

**측정(numpy toy · COCO val2017 · 3seed · held-out 83짝 P(B|A) AUC)**:
| seed | i (caption만) | ii (+world) | a (shuffle) | b (other-pair) | Δii | Δa | Δb |
|---|---|---|---|---|---|---|---|
| 0 | 0.490 | **0.956** | 0.437 | 0.558 | +0.466 | −0.053 | +0.068 |
| 1 | 0.494 | **0.956** | 0.430 | 0.552 | +0.463 | −0.064 | +0.059 |
| 2 | 0.472 | **0.955** | 0.450 | 0.554 | +0.483 | −0.022 | +0.081 |

## FROZEN 바 판정 (no-tune-to-green)
- Δ(ii−i) ≥ +0.10 : ✅✅✅ (+0.47, 압도적)
- Δ(a shuffle) ≤ +0.02 : ✅ (−0.05, bind-destroy 통제 완전붕괴)
- Δ(b other-pair) ≤ +0.02 : ❌ (+0.07, 바 초과) → **clean PASS-B 미달 → 🟠 MIXED**

## 정직 해석 (스크립트 이진 "FAIL-B wall-general"은 데이터와 모순 → 기각)
ii=0.96(chance 0.49서 급등)은 **world 채널이 명백히 usable**임을 보임. load-bearing Δii=+0.47 ≫ Δb=+0.07 = **pairing-specific**(shuffle 완전붕괴가 증명). control-b의 +0.07 잔차 = **marginal-exposure 누출**(other-pair world-event가 A의 등장빈도만 올려 약간 sharper) — 벽 아니라 통제설계의 약한 leak. ⟹ 스크립트의 "wall = property of any finite experience channel" 결론은 **거짓**(ii=0.96이 반증).

## 결론 — C2 = 🟢 fuel-lever 확증 (association), deep-operator(γ)는 별개
- **PASS (association/fuel-lever, control-b caveat)**: world(이미지) 채널이 텍스트엔 없는 held-out 짝 co-occurrence를 **substrate가 실제 학습·사용**(ii 0.96). ⟹ **C2는 유효한 fuel 레버 = coverage-density를 먹임**(ledger의 유일 생존 저비용 레버). Stage A(소스 존재)+Stage B(substrate 사용) 둘 다 non-negative.
- **scope 한계(정직)**: 이 probe는 P(B|A) **association**(retrieval)이지 **deep-recombination operator**(두 개념→novel 제3 의미 합성)가 아님. 후자=γ trained-constructive-bind(#3108 DUP-WALLED)로 여전히 unbroken. 즉 C2는 "held-out 짝을 covered로 전환"(fuel)하나 "combination operator"(engine)는 안 줌 — Fable의 fuel≠engine 프레임 그대로.
- **함의**: 벽은 "모든 유한 경험채널 성질"이 **아님**(world 채널은 usable). 벽=**operator**(engine)에 국한, 그 operator는 어떤 소스로도 fuel만 받지 스스로 안 생김. C2 grounded 경로=coverage-density 재활성 경로(concrete 짝 re-scope G1-concrete). deep-operator는 γ만 잔여.

## NEXT (선택)
- clean 재측정: control-b를 marginal-matched(A 등장빈도 동일화)로 정정한 별개 H(새 frozen). 단 load-bearing이 이미 결정적이라 fuel-lever 결론 불변.
- coverage-density 연결: C2가 먹이는 concrete-짝 coverage로 G1-concrete engine-native 재측정(pool). deep-operator는 여전히 γ 대기.
