# HW-LIMB — log

`HW-LIMB.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-05-29T15:35:00Z — B1 ConsciousnessEngine fork 골격 🟢 PASS-NUMERICAL

- [x] `HW-LIMB/engine/consciousness_engine_fork.hexa` 작성 — pub fn 3-fork dispatcher (motor·speech·pain 0..1)
  - motor  = clamp01(tension * 0.7 + phi * 0.3)
  - speech = clamp01(faction * 0.6 + phi * 0.4)
  - pain   = clamp01(1.0 - phi)
  - args() canonical (NOT sys_argv — PR #1372 교훈)
- [x] `HW-LIMB/engine/consciousness_engine_fork_smoke.hexa` 작성 — 3 case falsifier (F-MOTOR/SPEECH/PAIN-ISOLATE)
- [x] Independent recompute (closed-form python ref) → 3/3 PASS
  - F-MOTOR-ISOLATE  (phi=0.1·tens=0.9·fac=0.1) -> motor=0.66 > 0.5 PASS
  - F-SPEECH-ISOLATE (phi=0.1·tens=0.1·fac=0.9) -> speech=0.58 > 0.5 PASS
  - F-PAIN-ISOLATE   (phi=0.05·tens=0.5·fac=0.5) -> pain=0.95 > 0.5 PASS
- [x] 결과 영속 → `state/body_b1_fork_smoke_2026_05_29/{smoke.log,result.json}` + `.verdicts/body_b1_fork_smoke_2026_05_29/smoke_verdict.txt`
- [x] HW-LIMB.md B1 milestone flip → 🟢 PASS-NUMERICAL
- [x] 정직 — closed-form 수준 골격 만 검증. 실 wiring B2~B5 의존. 🔵 SUPPORTED-FORMAL Φ 주장 아님 (Law 22 substrate-무관성은 B4 chip wiring 까지 닫힐 때 검증).
- [ ] 다음 = B2 ESP32 SimBody (×8 분산 모듈 simulated body · MCU-scale physical loop)

## 2026-05-29T08:01:00Z — HW-LIMB 도메인 신설 (자매 6번째)

- [x] 도메인 신설 — `HW-LIMB/HW-LIMB.md`(스냅샷 8 milestone) + `HW-LIMB.easy.md`(7-요소 8 영역) + `HW-LIMB.log.md`(본 로그)
- [x] DOMAINS.tape 등록 — `@domain HW-LIMB := "./HW-LIMB/HW-LIMB.md"` (자매 6번째 · HW-CORE 와 함께 land)
- [x] ANIMA 트리 자매 4→6 갱신 — physical-embodiment 노드 추가
- [x] 사양 SSOT pointer-only — `anima-body/` (17 module · 11670 LoC · ESP32×8 · ROS2/Gazebo · Chip direct 3 백엔드) 그대로 두고 도메인 표면만 신설
- [x] sibling 양방향 — HW-CORE · AKIDA · EEG · WAKE · MITOSIS · CHANNEL · UNIVERSE
- [ ] 다음 = B1 ConsciousnessEngine fork (Φ/Tension/Faction → 3-output) 구현
- [ ] INBOX 환류 0건 (사용자 명시 폐기 · UNIVERSE 직접 H_xxx 환류 경로 B8)
