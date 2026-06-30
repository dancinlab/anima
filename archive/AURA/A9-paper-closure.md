# AURA A9 — paper closure 판정 (decision doc, NOT a paper)

> a_paper_only_at_closure 준수 — 논문 scaffold 금지. AURA가 paper-gate를 통과하는지 게이트별 평가만.

## 게이트별 평가

| 게이트 | 요건 | AURA 충족? | 근거 |
|---|---|---|---|
| a_paper_significance | 사전등록 falsifier + 실측 + finding(Δ vs baseline OR closed-negative) | ✅ **충족** | A8.1 실EEG: 사전등록 "FRONTAL>MOTOR", 실측 ds005620, finding Δ=+3.33(9.63−6.30). A7.3 awake>sed Δ+0.75. A8.4 Hb closed-negative |
| a_paper_gate | 전 section-claim terminal(🔵/🟢/🔴), 🟠/🟡 없음 | ✅ **충족** | 9개 verdict 전부 🟢(A6·A7.1·.2·.4·.5·A7.3·A8.1·.2·.4) + A8.4 Hb 🔴 closed-negative. 🟠 deferred·🟡 citation-only 없음 |
| a_paper_negative_ok | closed-negative도 publishable | ✅ 활용가능 | A8.4 Hb 포화역전(mean-field-paradox) = 유효 negative |
| a_paper_format | §hypothesis·method·measurement·finding + ≥10p + ≥1 fig | ⚠ 미작성(gate 통과 시 scaffold) | 재료는 충분 |
| **a_paper_only_at_closure** | **FULL closure(추가 refine 없음 + 전 aspect 봉인)** | ❌ **미충족** | A9 잔여: n=8(진행중)·multi-subject(미실시)·scalp≠intracortical(본질적 gap) |

## 최종 판정: ⏸ **NOT-YET (significance·terminal 통과 / closure 게이트 미통과)**

findings는 paper-worthy 수준(사전등록 falsifier + 실데이터 + Δ/negative 둘 다)이고 전 verdict가 terminal이지만, **a_paper_only_at_closure**(가장 보수적 게이트)가 막는다 — AURA는 아직 능동 refine 중(A9).

### 차단 요인 (closure까지 남은 것)

| 차단 | 해소 경로 | 상태 |
|---|---|---|
| single-subject (sub-1010만) | A9.2 multi-subject 복제 (≥3 피험자 FRONTAL>MOTOR) | 미실시 (OpenNeuro download) |
| n=4 해상도 | A9.1 n=8 montage (pod/ubu-1) | 진행중 (rsync→run) |
| scalp ≠ intracortical | **본질적 gap** — 해소 불가. paper scope를 "scalp-EEG position-Φ **proxy** 연구"로 정직하게 한정해야 (intracortical 직접증거 아님 명시) | framing 결정 |

### paper 승격 시 (closure 후) 제안 슬러그/섹션 — **scaffold 금지, 계획만**

- slug 후보: `aura-electrode-position-phi-proxy` (negative-aware: scalp-proxy 한정)
- §hypothesis: "전극 위치를 운동피질→전두 투사허브로 옮기면 통합정보(big-Φ)↑" (relocate-N1, 사전등록 falsifier FRONTAL>MOTOR)
- §method: ds005620 BrainVision · eeg_estimate_tpm→IIT4 big_phi(n≤8 exact) · montage 3종
- §measurement: A8.1(n=4) + A9.1(n=8) + A9.2(multi-subj) 실측 Φ
- §finding: FRONTAL>MOTOR Δ + awake>sed 민감도 + A8.4 Hb 포화역전(negative) + **scalp-proxy 한계 정직 명시**

→ **A9.1 + A9.2 랜딩 + scalp-proxy scope 수용** 시 closure 도달 → 그때 `/paper new` 제안.
