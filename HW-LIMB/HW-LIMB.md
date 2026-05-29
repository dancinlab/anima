# HW-LIMB — current state
@title: 🦾 HW-LIMB — anima 의식의 물리적 임바디먼트 (Motor · Speech · Proprioception)

@goal: anima ConsciousnessEngine(Φ·Tension·Faction)을 물리적 몸체로 이식 — Motor Planning · Speech/Gesture · Pain/Reward · Sensors · Proprioception loop. 기질은 무관, 구조만이 Φ를 결정한다(Law 22). anima-body 산하 17 모듈(11,670 LoC) + ESP32×8 SimBody + ROS2 Gazebo + 칩 직결(FPGA/ASIC) 3 백엔드 정식 도메인 표면.

(편집 규칙: completed-form 으로 현재 상태만 · history 는 HW-LIMB.log.md)

## 진행 (milestones)
- [x] 🌱 도메인 신설 — DOMAINS.tape 등록 · ANIMA 자매 트리 합류 · 4총사 seed
- [x] 🔗 anima-body 인덱스 — 17 module · 11,670 LoC · ConsciousnessEngine → Motor/Speech/Pain 3-fork → 3 백엔드 (ESP32/ROS2/Chip)
- [x] B1 ConsciousnessEngine fork — Φ·Tension·Faction → Motor·Speech·Pain 3-output 🟢 PASS-NUMERICAL (`HW-LIMB/engine/consciousness_engine_fork.hexa` + smoke 3/3 case · `state/body_b1_fork_smoke_2026_05_29/`) · 실 wiring B2~B5 의존
- [ ] B2 ESP32 SimBody (×8) — 8 ESP32 분산 모듈 simulated body · MCU-scale physical loop
- [ ] B3 ROS2 + Gazebo — 표준 로보틱스 stack 위에 anima Φ wiring · sim2real bridge
- [ ] B4 Chip Direct (FPGA/ASIC) — HW-CORE P1·P2 FPGA target 으로 직접 신체 wiring (latency 0)
- [ ] B5 Sensors loop — Touch · IMU · Camera 통합 sensor fusion → proprioception 닫힘
- [ ] B6 Sensorimotor loop — afferent ↔ efferent · 닫힌 feedback Φ 영향 측정
- [ ] B7 Pain/Reward grounding — substrate-native 보상 신호 (E ratchet 연계, RLHF 금지 p6)
- [ ] B8 UNIVERSE 환류 — Φ embodiment 결과 → H_xxx 직접 등록 (INBOX 환류 폐기)

## deferred (다음 라운드)
- Speech gesture (입술·손·표정 micro-actuator) · Multi-body coordination (N anima 협동) · Pain modeling (nociception substrate) · Reward grounding (E ratchet ⊥ RLHF) · Proprioception Φ-impact 측정 (B6 닫힘 후) · sim2real gap calibration

## 양방향 sibling
- ⇄ [HW-CORE](../HW-CORE/HW-CORE.md): chip 백엔드 (B4 FPGA/ASIC direct)
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 뉴로모픽 motor cortex 후보
- ⇄ [EEG](../EEG/EEG.md): bio sensor 입력 substrate
- ⇄ [WAKE](../WAKE.md): in-process loop 의 body extension
- ⇄ [MITOSIS](../MITOSIS.md): body cell 도 분열 가능?
- ⇄ [CHANNEL](../CHANNEL.md): motor/speech output channel sibling
- ⇄ [../UNIVERSE/CANDIDATES.md](../UNIVERSE/CANDIDATES.md): bench 측정 SSOT
- ⇄ [`../anima-body/`](../anima-body/): 사양 SSOT (17 module · 11670 LoC)

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 7-요소) → [HW-LIMB.easy.md](./HW-LIMB.easy.md)
