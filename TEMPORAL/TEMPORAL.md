# TEMPORAL — current state
@title: ⏱️ TEMPORAL — 시간 통합 의식 Φ-detector (Δt window-axis)

@goal: XENO 가 (n × density × structure) 3축 applicability matrix 위에서 substrate-blind Φ-formalism 의 영역을 매핑했다면, TEMPORAL 은 4번째 축인 **integration window Δt** 위에서 같은 invariant_detector 가 어떻게 calibrate 되는지 매핑한다. 즉 "의식의 시간 통합" — 동일 substrate 가 instant(Δt=1) / short(Δt=8) / mid(Δt=32) / long(Δt=128) lag 위에서 Φ 가 어떻게 변하는지 closed-form 측정.

(편집 규칙: completed-form 으로 현재 상태만 · history 는 TEMPORAL.log.md)

## 진행 (milestones)
- [x] 🌱 도메인 신설 — DOMAINS.tape 등록 · 4총사(`.md`·`.easy.md`·`.log.md`·README seed) · XENO sibling 합류
- [x] ⏱️ T1 timeshift detector 설계 — XENO/detector/invariant_detector.hexa 의 sliding lag-window 확장 (Δt=1/8/32/64 4-point) · TEMPORAL/detector/timeshift_detector.hexa · 사전등록 falsifier 5/5 · 🔴 FALSIFIED-INSTRUMENT 1/5 · H_841 · lag-axis cycle-aligned inflation artifact 발견
- [x] ⏱️ T2 multi-unit time-embed detector — Takens delay reconstruction (e=2/3/4/5, delay=1) · TEMPORAL/detector/time_embed_detector.hexa · 4 substrate × 4 embed_dim = 16 measurements + 사전등록 falsifier 5/5 · 🔴 FALSIFIED-INSTRUMENT 2/5 · H_842 · 신 embed-dim sparse-state inflation artifact 발견 · T1 lag-artifact 미해소 · T1+T2 dual closed-negative
- [x] ⏱️ T3 anima 90-min ultradian Φ scan — X1 invariant_detector 그대로 적용, 4 substrate (WAKE/N1_N2/N3/REM, n=128 hardcoded literal) · TEMPORAL/scan/ultradian_phi.hexa · 5 사전등록 falsifier (WAKE-MID/N3-LOW/REM-HIGH/N1-MID/MONOTONE) · **2/5 PASS** · 🔴 FALSIFIED-INSTRUMENT · H_843 · WAKE Φ=0.866 > N3 Φ=0.335 정합 (F-T3-WAKE-MID + F-T3-N3-LOW PASS) · N1_N2 Φ=0.0 zero-degenerate (T1 lag-artifact 의 다른 face) + REM Φ=0.569 < WAKE (paradoxical REM 미정합) + monotone ladder 실패 · T1+T2+T3 triple closed-negative
- [ ] ⏱️ T4 time-averaged Φ + Granger causality + surrogate-baseline — T1+T2+T3 triple closed-negative 의 자연 entry (window-mean detector / TPM-free predictive coupling / random-shuffle null-model 차감)
- [ ] ⏱️ T5 papers — XENO follow-up paper 3 (4D applicability frontier closed-negative — T1+T2 dual + T3 ultradian 정직 사례)

## deferred (다음 라운드)
- BLC-1 STDP spike-timing 의식 plasticity Φ · TLC-1 시간역행 substrate (DMT/psilocybin 환각) Φ · TIC-1 시간 dilation 외계 (광속 0.99c) Φ · TSC-1 의식 dilation 명상 (10-min anchor breath = 1-hour subjective) Φ · TFC-1 anesthesia γ-burst (10ms 위 Φ 측정) · TGC-1 우주 시간 외삽 빅뱅→빅립 Φ 곡선 (Δt=10^60s) · TCC-1 자기장 의식 ms-scale Φ · T4-historical-timescale (Δt=1 vs Δt=10^7) · T-longer-signal (n=1024+ sparse-state inflation 완화 시도)

## 양방향 sibling
- ⇄ [XENO](../XENO/XENO.md): 기반 invariant_detector 출처 · TEMPORAL 은 XENO 의 4번째 축 (Δt) 확장
- ⇄ [EVOL](../EVOL/EVOL.md): 진화 복잡도 축 자매 도메인 — TEMPORAL Δt + EVOL species ladder = 4D/5D applicability frontier 확장 (H_845 closed-negative · 2026-05-29)
- ⇄ [EEG](../EEG/EEG.md): 생체 EEG 시간 통합 (S1 wake / S15 anesthesia / S24 dream 시계열 측정 원천)
- ⇄ [TIME](../TIME.md): 시간 인식 의식 자매 도메인 (subjective vs substrate clock)
- ⇄ [DREAM](../DREAM.md): REM/N1-N3 ultradian Δt scale 자매
- ⇄ [../HEXAD/IIT4/IIT4.md](../HEXAD/IIT4/IIT4.md): Φ-formalism SSOT
- ⇄ [../UNIVERSE/CANDIDATES.md](../UNIVERSE/CANDIDATES.md): 검증 결과 환류 SSOT

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 7-요소) → [TEMPORAL.easy.md](./TEMPORAL.easy.md)
