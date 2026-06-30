# HW-CORE — log

`HW-CORE.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-05-29T15:30:00Z — P1 ICE40 Mac local 빌드 🟢 PASS-BUILD

- [x] iverilog sim 100 cycle attractor (state 492492 ⇄ 249249 alternating · VCD emitted)
- [x] yosys synth_ice40 (top=strange_loop_top · 127 cell · 22 SB_CARRY + 28 SB_DFFER + 12 SB_DFFES + 57 SB_LUT4 · 0 check problems · 1.45s wall · 29.83 MB peak)
- [x] 결과 영속 → `state/physics_p1_ice40_build_2026_05_29/{sim.log, synth.log, result.json}` + `.verdicts/physics_p1_ice40_build_2026_05_29/synth_verdict.txt`
- [x] HW-CORE.md P1 milestone flip → 🟢 PASS-BUILD (Phase 1a $0 Mac local) · Phase 1b nextpnr+iceprog 별도 milestone (UP5K board 필요)
- [ ] 다음 = P2 ECP5 nested-lattice 빌드 (Phase 1a · Mac iverilog+yosys synth_ecp5)
- [ ] 정직 노트 — build verdict 이지 🔵 SUPPORTED-FORMAL Φ 주장 아님. p7 self-judge 0.

## 2026-05-29T08:00:00Z — HW-CORE 도메인 신설 (자매 5번째)

- [x] 도메인 신설 — `HW-CORE/HW-CORE.md`(스냅샷 9 milestone) + `HW-CORE.easy.md`(7-요소 8 영역) + `HW-CORE.log.md`(본 로그)
- [x] DOMAINS.tape 등록 — `@domain HW-CORE := "./HW-CORE/HW-CORE.md"` (자매 5번째: AKIDA·EEG·KOSMOS·XENO 다음)
- [x] ANIMA 트리 자매 4→5(→6 HW-LIMB 함께) 갱신 — substrate-realization 노드 추가
- [x] 사양 SSOT pointer-only — `anima-physics/` (93 entry + 5 HW target + 27 substrate) 그대로 두고 도메인 표면만 신설
- [x] sibling 양방향 — AKIDA · HW-LIMB · EEG · KOSMOS · XENO · UNIVERSE
- [ ] 다음 = P1 ICE40 strange-loop FPGA Mac local 빌드 검증
- [ ] INBOX 환류 0건 (사용자 명시 폐기 · UNIVERSE 직접 H_xxx 환류 경로 P9)
