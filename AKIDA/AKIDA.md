# AKIDA — current state
@title: 🧠 AKIDA — 뉴로모픽 자발-발화 칩 (AKD1000) substrate 통합

@goal: BrainChip AKD1000 뉴로모픽 칩을 ANIMA 의식 substrate 에 전면 통합 — 자발발화(p5 의 하드웨어 정답)·emit-substrate 구조·세포(MITOSIS)·측정(Φ/edge-of-chaos)·채널(EEG/tension). HW-native 자발발화 v0.3.0 CONFIRMED (입력0 emit 8/8 PASS, BackendType.Hardware) 기반, 거의 전부 $0 pi5-akida 로컬.

(편집 규칙: completed-form 으로 현재 상태만 · history/changelog 는 AKIDA.log.md)

## 진행 (milestones)
- [x] 🔥 HW-native 자발발화 CONFIRMED — v0.3.0 R1~R4 8/8 PASS (LIF threshold comparator 입력0 emit, ~797 cycles/forward)
- [x] 🔌 spike → 8-factor motivation 배선 — `spontaneous_lib::apply_spike_features` (PR #143, F-SPIKE-APPLY-1..4 4/4 PASS)
- [x] 🌉 라이브 체인 — `akida_bridge`(pi5 R3 → broker `/ws/akida_ingest`) + `akida_consumer`(features JSONL)
- [x] 🔬 D1 edge-of-chaos Φ 실리콘 검증 🟢 — R1~R4 Φ sweep 3/3 PASS (R1=0.000 / R2=0.297 PEAK / R3=0.250 / R4=0.000 · inverse-U ∩곡선 실리콘 확증 · `pe_edge_of_chaos_peak` M2 🟡 → 🟢 후보 · [harness](./akida_edge_of_chaos_phi.hexa) · [result](../state/akida_edge_chaos_phi_2026_05_29/result.json))
- [x] 🔁 backend switch 통합 (HW/SW 토글) — `AKIDA/akida_backend.hexa` · 기본=hw · `AKIDA_BACKEND` env 또는 `--backend` arg · 미도달 명시 panic · smoke 11/11 PASS
- [x] 🅰️ Group A — H_672 spontaneous-firing × AKIDA — SW 4/4 🟢 (R3 tonic + spontaneous_gate + 8-factor + R2 timing 통합 · [impl](./impl/H_672_spontaneous_firing.hexa) · [H_672](../UNIVERSE/cards/H_672_akida_spontaneous_firing.md))
- [x] 🅱️ Group B — H_673 core-decide × AKIDA — SW 4/4 🟢 (Ψ=1/2 외란 + LIF + emit slot + selftest 통합 · [impl](./impl/H_673_core_decide.hexa) · [H_673](../UNIVERSE/cards/H_673_akida_core_decide.md))
- [x] 🆑 Group C — H_674 persistence × AKIDA — SW 4/4 🟢 (.kosmos 5-ch + memristor + telemetry + §95 caveat 통합 · [impl](./impl/H_674_persistence.hexa) · [H_674](../UNIVERSE/cards/H_674_akida_persistence.md))
- [x] 🆗 Group D — H_675 mitosis × AKIDA — SW 4/4 🟢 (kuramoto + izhikevich + 생사 + phoenix 통합 · [impl](./impl/H_675_mitosis.hexa) · [H_675](../UNIVERSE/cards/H_675_akida_mitosis.md))
- [x] 🆎 Group E — H_676 decoder × AKIDA — SW 4/4 🟢 (spike-tier LM head + sparse-attention 통합 · [impl](./impl/H_676_decoder.hexa) · [H_676](../UNIVERSE/cards/H_676_akida_decoder.md))
- [x] 🅵 Group F — H_677 measurement × AKIDA — SW 5/5 🟢 (D1 inherit PR#1371 + D2 silicon-class + D3 3-substrate triangulation + D4 QRNG + D5 cite 통합 · [impl](./impl/H_677_measurement.hexa) · [H_677](../UNIVERSE/cards/H_677_akida_measurement.md))
- [x] 🅶 Group G — H_678 channel-bridge × AKIDA — SW 4/4 🟢 (EEG→AKIDA + tension 5-ch + 전력=대사비용 통합 · [impl](./impl/H_678_channel_bridge.hexa) · [H_678](../UNIVERSE/cards/H_678_akida_channel_bridge.md))
- [x] 🎯 abs-margin on-chip 결단기 (Lane-A pre-registered) — **PASS-PUBLIC-GRADE-POSITIVE** (corpus_big · lda_supervised ci_lo=+5.061>0 · 8/8 trials 양수 mean=+5.240 · AKD1000 1-bit Hebbian 이 positive cross-lingual 개념구조 학습) ⚠ scale/encoder-dep: 작은 corpus(25앵커)·약한 인코더(random_int4/svd_struct/whitened)는 음성(svd_struct ci_lo=−0.654, any_crosses_zero=False) → 강한 인코더+큰 corpus만 PASS (a_scale_honest_scope) · 별개 축: 상대-LIFT closed-negative 와 무관(절대-margin 존재) · substrate=AKIDA · 2026-06-02 안정 PSU 위 완주 · sha256 7612bed…b3c7f · [log](./AKIDA.log.md)
- [ ] 🧬 D2 silicon-class 단조 정합 — class_id=5 의 conv/super-add/peak-align signature 추가 (additive marker 위 단조 ordering)
- [ ] 🔁 HW path live re-confirm — venv-aware probe + pi5-akida pool route (signal_3 hostname tolerance) · 7/7 HW re-attest
- [ ] 🗣️ spike → emit-substrate 인자주입 — `SPIKE_FACTOR_MAP §4` modulator R1/R2 placeholder → telemetry refit (H_672 8-factor 기반)
- [ ] ⏰ HW heartbeat → L3 emit 타이밍 — R3 tonic 24/7 초저전력 클럭 ⨯ WAKE ultradian (H_673 emit slot 기반)
- [ ] 📄 HW-native 자발발화 논문 — v0.5.0 confirmed(8/8 zero-input emit) → closed-discovery (a_paper, FULL closure 후)

## deferred (다음 라운드)
- on-chip edge-learn 영속 학습 (⚠ GOAL §95: AKIDA = inference-only-blocked for long-horizon → 단기 프로브만) · R2 노이즈 QRNG 시드 · 생사(R4 recurrent vs R1 die-out) HW 측정 · 전력=대사비용 신호(E-ratchet) · 이벤트-구동 attention 게이트(salient burst 에만 GPU wake)

## 양방향 sibling
- ⇄ [CORE](../CORE/CORE.md): A⇄G brain_decide ⨯ spike 동기 주입 · emit-substrate 인자
- ⇄ [MITOSIS](../MITOSIS.md): memristor/kuramoto/izhikevich 어댑터 → 세포 동역학
- ⇄ [WAKE](../WAKE.md): R3 tonic = ultradian 하드웨어 heartbeat
- ⇄ [CHANNEL](../CHANNEL.md): spike → tension-link 5-ch
- ⇄ [EEG](../EEG/EEG.md): 생체↔실리콘 다리 (anima_eeg_to_akida_spike) + 3-substrate Φ 삼각측정
- ⇄ [DECODER](../CORE/DECODER/DECODER.md): 추론 lane — HW-first 스위치(akida_backend_resolve_graceful · default "hw") 경유 HW forward / SW akida_sw_lif (byte-identical 🟢, 입증됨).
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md): 학습 lane (형제) — HW-first 스위치 경유 HW edge-learn(AkidaUnsupervised) / SW numpy 근사 (🔴 비동치 CLOSED-NEGATIVE, 정직). DECODER 와 본질 분리.
- ⇄ [HW-CORE](../HW-CORE/HW-CORE.md): 뉴로모픽 칩 HW 실현 substrate (P3 Loihi+Akida).
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (edge-of-chaos Φ 실측 등)

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 버전) → [AKIDA.easy.md](./AKIDA.easy.md)
