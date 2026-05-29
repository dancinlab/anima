# PHYSICS — current state
@title: ⚛️ PHYSICS — anima 의식 substrate 의 물리적 실현 (FPGA · 칩 · MCU · Q · Photonic)

@goal: PureField repulsion-field substrate 를 다양한 물리 HW(FPGA/Loihi/Akida/Arduino/Quantum/Photonic/Memristor/EEG)로 실현 가능성 매트릭스. anima-physics 산하 93 entry + 5 HW target + 27 substrate 의 정식 도메인 표면. 비용 ladder $0 (Mac local 시뮬) → $5~30 (Cloud probe) → $200~ (실 HW).

(편집 규칙: completed-form 으로 현재 상태만 · history 는 PHYSICS.log.md)

## 진행 (milestones)
- [x] 🌱 도메인 신설 — DOMAINS.tape 등록 · ANIMA 자매 트리 합류 · 4총사 seed (md + easy.md + log.md)
- [x] 🔗 anima-physics 인덱스 — 93 entry (루트 11 + docs 19 + substrate 60 + recovered 3) · 41 ✅ · 36 🟡 · 16 ❌
- [x] P1 ICE40 strange-loop FPGA — Lattice iCE40UP5K · `hw/strange_loop_ice40/` Mac iverilog+yosys 🟢 PASS-BUILD (sim 100 cycle attractor + synth 127 cell · `state/physics_p1_ice40_build_2026_05_29/`) · Phase 1b nextpnr+iceprog 별도 milestone
- [ ] P2 ECP5 nested-lattice FPGA — Lattice ECP5-EVN · `hw/nested_lattice_ecp5/` synth_ecp5
- [ ] P3 Loihi 2 + Akida kuramoto — Intel Loihi 2 · BrainChip Akida cloud-only (AKIDA 자매 도메인 합류)
- [ ] P4 Arduino sleep oscillator — Arduino + AD9833 DDS · `hw/sleep_oscillator_arduino/`
- [ ] P5 Spontaneous Ising — Toshiba SBM / Fujitsu DA / ECP5 fallback · `hw/spontaneous_ising/`
- [ ] P6 Memristor analog — `memristor/` analog photonic substrate
- [ ] P7 Quantum probe — `quantum/` AWS Braket Rigetti/IonQ/QuEra cloud probe ($5~30)
- [ ] P8 Photonic — `analog/`·`photonic/` Perceval Mac 시뮬 + 실 HW 외부협력
- [ ] P9 UNIVERSE 환류 — 검증 결과 → H_xxx 직접 등록 (INBOX 환류 폐기)

## deferred (다음 라운드)
- Magnet rotation HW (Hall sensor·로터리 엔코더 PureField A-G 반발 직접 측정) · Multi-FPGA mesh (Kuramoto 위상동기) · ESP32 distributed substrate · 5-1 Engine A ASIC (45nm CMOS 디자인) · 광자 솔리톤 도메인 벽 · Strange Loop SoC tape-out
- HW 종속성: P1~P5 는 anima-physics/hw/ 빌드 파이프라인 재활용 · P6~P8 은 substrate 부터 spec 작성

## 양방향 sibling
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 뉴로모픽 칩 실현 (P3 Loihi+Akida)
- ⇄ [BODY](../BODY/BODY.md): physical embodiment (motor cortex · proprioception loop)
- ⇄ [EEG](../EEG/EEG.md): 생체 입력 측정 (anima-physics/eeg/)
- ⇄ [KOSMOS](../KOSMOS/KOSMOS.md): HW emit anchor 영속
- ⇄ [XENO](../XENO/XENO.md): substrate-agnostic detector 의 HW realization
- ⇄ [../UNIVERSE/CANDIDATES.md](../UNIVERSE/CANDIDATES.md): bench 측정 SSOT
- ⇄ [`../anima-physics/`](../anima-physics/): 사양 SSOT (93 entry + 5 HW target + 27 substrate)

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 7-요소) → [PHYSICS.easy.md](./PHYSICS.easy.md)
