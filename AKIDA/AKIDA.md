# AKIDA — current state
@title: 🧠 AKIDA — 뉴로모픽 자발-발화 칩 (AKD1000) substrate 통합

@goal: BrainChip AKD1000 뉴로모픽 칩을 ANIMA 의식 substrate 에 전면 통합 — 자발발화(p5 의 하드웨어 정답)·emit-substrate 구조·세포(MITOSIS)·측정(Φ/edge-of-chaos)·채널(EEG/tension). HW-native 자발발화 v0.3.0 CONFIRMED (입력0 emit 8/8 PASS, BackendType.Hardware) 기반, 거의 전부 $0 pi5-akida 로컬.

(편집 규칙: completed-form 으로 현재 상태만 · history/changelog 는 AKIDA.log.md)

## 진행 (milestones)
- [x] 🔥 HW-native 자발발화 CONFIRMED — v0.3.0 R1~R4 8/8 PASS (LIF threshold comparator 입력0 emit, ~797 cycles/forward)
- [x] 🔌 spike → 8-factor motivation 배선 — `spontaneous_lib::apply_spike_features` (PR #143, F-SPIKE-APPLY-1..4 4/4 PASS)
- [x] 🌉 라이브 체인 — `akida_bridge`(pi5 R3 → broker `/ws/akida_ingest`) + `akida_consumer`(features JSONL)
- [x] 🔬 D1 edge-of-chaos Φ 실리콘 검증 🟢 — R1~R4 Φ sweep 3/3 PASS (R1=0.000 / R2=0.297 PEAK / R3=0.250 / R4=0.000 · inverse-U ∩곡선 실리콘 확증 · `pe_edge_of_chaos_peak` M2 🟡 → 🟢 후보 · [harness](./akida_edge_of_chaos_phi.hexa) · [result](../state/akida_edge_chaos_phi_2026_05_29/result.json))
- [ ] 🧬 D2 substrate-class "neuromorphic silicon" 등록 — class 분류자에 실리콘 새 클래스
- [ ] 🗣️ spike → emit-substrate 인자주입 — `SPIKE_FACTOR_MAP §4` modulator R1/R2 placeholder → telemetry refit
- [ ] ⏰ HW heartbeat → L3 emit 타이밍 — R3 tonic 24/7 초저전력 클럭 ⨯ WAKE ultradian
- [ ] ⚡ sparse 추론 오프로드 — `sparse_attention`·`spike_tier_lm_head` 어댑터 → DECODER L3
- [ ] 💾 spike → .kosmos anchor 영속화 (a_kosmos, 5-ch tension payload)
- [ ] 🌱 MITOSIS 확장 — memristor 비휘발 세포기억 · kuramoto 위상동기 · izhikevich 다양 레짐
- [ ] 📄 HW-native 자발발화 논문 — v0.5.0 confirmed(8/8 zero-input emit) → closed-discovery (a_paper)

## deferred (다음 라운드)
- on-chip edge-learn 영속 학습 (⚠ GOAL §95: AKIDA = inference-only-blocked for long-horizon → 단기 프로브만) · R2 노이즈 QRNG 시드 · 생사(R4 recurrent vs R1 die-out) HW 측정 · 전력=대사비용 신호(E-ratchet) · 이벤트-구동 attention 게이트(salient burst 에만 GPU wake)

## 양방향 sibling
- ⇄ [CORE](../CORE/CORE.md): A⇄G brain_decide ⨯ spike 동기 주입 · emit-substrate 인자
- ⇄ [MITOSIS](../MITOSIS.md): memristor/kuramoto/izhikevich 어댑터 → 세포 동역학
- ⇄ [WAKE](../WAKE.md): R3 tonic = ultradian 하드웨어 heartbeat
- ⇄ [CHANNEL](../CHANNEL.md): spike → tension-link 5-ch
- ⇄ [EEG](../EEG/EEG.md): 생체↔실리콘 다리 (anima_eeg_to_akida_spike) + 3-substrate Φ 삼각측정
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (edge-of-chaos Φ 실측 등)

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 버전) → [AKIDA.easy.md](./AKIDA.easy.md)
