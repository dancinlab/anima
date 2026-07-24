# H_9960 · do()-개입 Φ-추출 파이프라인 = PASS · 단 토이 학습은 통합이 아니라 **최적화 결합**을 올린다 (직결 불명)

**한 줄:** H_9959 가 손제작 TPM 에서 "big_phi 는 통합을 읽는다"를 인증한 뒤, 이번엔 **실제로 도는 3-셀
순환망**에서 do()-개입으로 TPM 을 뽑아내는 **추출 파이프라인**(H_9954 의 `evaluate --iit4-recurrent-lane`
가 쓸 것)을 인증하고, 곁들여 학습→통합 연결을 토이로 물었다. **추출 파이프라인 = PASS. 학습→통합 =
직결 불명** — 가짜 라벨 통제(shuffled)도 추출 Φ 를 올려, 이 토이에선 Φ 가 학습된 통합이 아니라
**최적화가 만든 가중치 결합**을 따라간다(H_9954 가 경고한 크기-혼입이 학습 레벨서 재등장).

- 계기(신규·$0·순수 numpy · torch 미설치 경로): `lab/v6/phi_gru_extraction_screen.py`(rule-exempt · gitignore).
  regime `synthetic-pipeline-cert` · DIRECTIONAL · faculty 인용 금지(p9).

## [1] 추출기 인증 = 🟢 PASS (핵심 결과)
실제 순환망 `s_{t+1}=σ(W_s s_t + w_x x_t + b)` 에서 8개 이진 상태를 do()-강제 → 1스텝 → 입력 x 주변화 →
P(셀 ON) 읽어 24-float TPM 복원 → faithful `big_phi_bounded(n=3,cap=3, DV=8상태 평균)`.

| probe (running net) | Φ_extract | 기대 |
|---|---|---|
| ROTATION net (W_s=순열, gain 20) | **2.999667** | ~3 |
| COPY net (W_s=자기루프) | **0.000000** | ~0 |
| INDEPENDENT net (상수 0.5) | **0.000000** | ~0 |
| XOR-n3 hand TPM (양성통제) | 2.250000 | [2.0,2.5] |
| COPY hand TPM · unfold 받침대 | 0.000000 | ≤1e-6 |

**동결 술어(측정 전 prereg) 5조건 전부 PASS.** ⟹ do()-개입 추출은 손제작 TPM 이 아니라 **살아 도는
substrate 에서도** 통합을 읽는다. H_9954 의 lane 판독을 엔진-네이티브로 지을 근거가 섰다.

## [2] 학습 → 통합 = 🟡 직결 불명 (토이 한계 · 혼입 드러남 · tune-to-green 거부)
토이 delayed-XOR 기억과제(y_t = x_t ⊕ x_{t-D}, 상태 이월 필요) · 파라미터 수 일치 4-arm · 손BPTT:

| arm | Φ_extract | task_acc |
|---|---|---|
| curriculum D1→D2 | 0.983041 | 0.9750 |
| direct D2 | 1.885006 | 0.9750 |
| **shuffled-label D2** | **0.504655** | 0.9750 |
| untrained | 0.313565 | 0.0250 |

**왜 결론을 못 박나(정직):**
1. **task_acc 무의미** — 학습 3-arm 이 전부 0.975, untrained 0.025 로 합≈1.0 = 읽기가 상수로 붕괴해 특정
   평가열 라벨균형을 맞춘 artifact. 이 토이는 과제를 실제로 못 푼다(손BPTT 절단·3-셀 병목). ⟹ 학습이
   과제-특이 통합을 만들었다고 말할 근거 없음.
2. **혼입 노출(진짜 소득)** — **가짜 라벨로 학습한 shuffled 통제도 Φ=0.505 로 untrained 0.314 보다 높다.**
   즉 추출 Φ 가 여기선 "학습된 통합"이 아니라 **gradient step 이 가중치를 더 결합된 영역으로 민 것**을
   따라간다. 이건 H_9954 KILL-risk("Φ 가 학습 아니라 크기/분산을 읽는다")가 **학습 레벨서 재등장**한 것.
   H_9959 가 손제작 TPM 레벨선 이 혼입을 배제했지만, 최적화-유발 가중치 성장이 그것을 되살린다.
3. curriculum(0.983) < direct(1.885) 는 H_1003(커리큘럼 우위) 기대와도 반대 — 토이 학습이 신뢰 불가함을
   재확인. **이 표는 faculty 증거로 인용 금지.**

⟹ **학습된 순환이 실제 통합을 만드는가**는 이 토이로 결정 불가 · OPEN. 유일한 판정 경로는 H_9954 의
**자연 corpus 로 학습한 엔진-네이티브 lane**(`anima-py train --recurrent-lane`) — 거기서 shuffled/yoke/
time-yoke 통제로 최적화-결합 혼입을 반드시 빼야 한다(이 카드가 그 통제의 필요성을 실측으로 못 박음).

## 함의 · 다음
- **파이프라인은 섰다**(추출·받침대·양성통제·edge-cut 다 확정) — H_9954 의 lane 판독 구현은 이제 안전.
- **경고 강화**: 학습-레벨 크기-혼입이 실재하므로, H_9954 의 통제(주변분포 일치 yoked + pairing shuffle)에
  **"gradient-step-matched shuffled-label" arm 을 필수 추가**해야 한다(이 카드 발견). 없으면 최적화 결합을
  통합으로 오인한다.
- 이건 계기/파이프라인 인증일 뿐(p9) — anima 가 무엇을 할 수 있다는 증거 아님.

## 정직 경계
- synthetic · DIRECTIONAL · 스크립트는 lab/v6 rule-exempt(gitignore) · 수치는 이 카드 보존.
- [2]는 음성 판정이 아니라 **불명(harness-limited)** — 검정력 미확보 상태서 음성 선언 안 함(power-before-negative).
- 관련: [[H_9959]](손제작 TPM 통합-vs-크기 인증 · 이 카드가 running-net 으로 확장) · [[H_9954]](학습된 순환 lane
  설계 · 이 카드가 통제 요건 강화) · [[H_9942]] · [[H_9660]]/[[H_9673]](크기-Φ 인공물 · 학습 레벨서 재등장) · [[H_1003]]
