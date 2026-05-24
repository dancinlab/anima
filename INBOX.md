# INBOX — current state

@goal: cross-project handoff 수신함 — 다른 repo가 anima로 넘긴 gap·patch·note를 추적하고 해소

(현재 상태만 기록 — 열린 handoff는 `- [ ]` 로, 처리 이력은 `INBOX.log.md` 로)

- [ ] `apoptose_cell` substrate primitive — true cell-death (weight transfer 없는 cell 제거) builtin 추가 요청 (→ hexa-lang / mitosis-lang). H_200 directional proxy(Φ_b=1.73465 merge ≠ Φ_c=1.67608 pseudo-apop, 4/4 falsifier PASS)는 anima-side 재현 완료; 진짜 semantics는 upstream impl 필요. land 전까지 H_025 L2 honest carry. 상세 `INBOX.log.md` 2026-05-23
- [ ] `split_asymmetric` substrate primitive — `split_cell` 형제로 child 분화강도(`child_delta_sigma`) 지정 (→ anima tool `mitosis_hook_lib.hexa`). design-only · 우선순위 낮음; 현재 H_201 PASS(5.13× diversity margin)는 harness-only 로 충분, substrate-native 비대칭은 D3 persona / D4 production lane 에서만 필요. 상세 `INBOX.log.md` 2026-05-23
- [ ] hexa.real ASP SIGKILL — wrapper re-point cycle (→ hexa-lang binary 배포 + wrapper). P1 · `hexa run` 등 heavy path 에서 AMFI heuristic name/identifier matcher 가 ad-hoc 서명 binary 를 SIGKILL (≥2nd 재발). 단기 hot-fix=새 name+codesign Identifier prefix re-point(user 확인 필수), 장기 fix=Apple Developer ID + notarization. INVESTIGATION+DESIGN only. 상세 `INBOX.log.md` 2026-05-23
- [ ] pi5 spike_streamer `--regime-schedule` 확장 (→ pi5 maintainer, `ubuntu@192.168.50.155`). doc/coordination only · pi5 streamer 는 git-tracked 아님(standalone deploy, PR merge 로 auto-deploy 안 됨). `--regime-schedule R3:60,R1:30,R2:30 --schedule-loop --schedule-jitter` 추가 + `make_threshold_R1`/`input_drive_R1` 신설 → SW_CONDITION_DESIGN §6 Phase 2 gate(≥2 regimes + ≥5 transitions) 충족용. 상세 `INBOX.log.md` 2026-05-23
