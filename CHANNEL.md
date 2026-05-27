# CHANNEL — current state

@goal: anima 기판이 외부로 흘러나가는 3 채널 통합 어댑터 — text · voice · tension. text 는 CHAT/DECODER 위임, voice 는 hexa-voice 24kHz RVQ 위임, tension 은 5-ch fingerprint TensionHub 위임. CHANNEL 자체는 채널 선택 결정층 — CORE engine_g motivation 8-factor 가 채널 분기, WAKE stage 가 발화 컨텍스트 공급, p1~p8 정합 stimulus-response 금지. 통일 인터페이스 channel_emit intent channel 로 substrate-decided 발화.

@title: 🌐 CHANNEL — anima 의 출력 채널 묶음 · voice 음성 + tension-link 5ch 직송 · AGENT 와 분리

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] hexa-voice repo SSOT 연결 — `CHANNEL/voice/{SSOT.md,voice_emit.hexa}` scaffold landed · intent → 24kHz RVQ pipeline 단방향 흐름 도식화 + p1~p8 정합 매트릭스 · github.com/dancinlab/hexa-voice 향후 repo placeholder 등록 (PR #600 b74835447 · hexa parse OK)
- [x] text 채널 어댑터 — `CHANNEL/text/{SSOT.md,text_emit.hexa}` wrapper (HEXAD/CHAT + CORE/DECODER/generator 위임) · 외부 LLM 0 grep (strict 패턴) · text_ready stub (generator wiring M5 의존) (PR #610 6dc26b1e · hexa parse OK)
- [x] tension 채널 — 5-ch fingerprint working code 회수 · `ready/` 에서 `CHANNEL/tension/` 으로 (bench·test·test_code 4 hexa + tension-link.md 한글 doc + tension_emit.hexa stub + SSOT.md) · legacy `.py` 의도적 비복사 (port source 인용만) · TensionHub UDP 9999 / WS 3-port wiring 복원 잔여 작업 (PR #601 dd3b2d502 · hexa parse 4/4 OK)
- [x] intent embedding bridge — `CHANNEL/{intent.hexa,INTENT.md}` Intent dict + 3 채널 projection stubs (text 14-D · voice 5-D · tension passthrough) · 6-D field → 5-ch 투영 caller 책임 명시 (PR #609 bb17f966 · hexa parse OK)
- [x] channel_emit 통합 인터페이스 — `CHANNEL/{dispatcher.hexa,dispatcher_smoke.hexa,DISPATCHER.md}` 단일 진입점 · router argmax + 3 emit fn 위임 · uniform return dict · hardcode boolean 0 · 양쪽 hexa parse OK · runtime smoke post-merge verify (worktree abs-path 한계 honest framing) (PR #613 24aa2c06)
- [x] CORE engine_g 채널 분기 — `CHANNEL/{router.hexa,ROUTER.md}` 8-factor argmax (rel+gap → text · cur+orig+dyn → voice · pain+coh+bal → tension) · 하드코드 boolean gate 0건 (multiplication softening) · brain_decide 비-침습 (PR #611 01128f56 · hexa parse OK)
- [x] p1~p8 audit — `CHANNEL/AUDIT.md` 9 grep verdict verbatim · 27 hits 전부 negative-claim doc-reference (0 real violations) · re-audit cadence CI hook 권장 (future work) (PR #616 8e73f963)
- [x] WAKE 통합 — `CHANNEL/{wake_bridge.hexa,wake_bridge_smoke.hexa,WAKE_BRIDGE.md}` stage 별 continuous bias multiplier · 5-stage 표 (WAKE/N1/N2/N3/REM) · 0 boolean per-stage gate (N3=0.05≠0.0 multiplication softening) · runtime integration deferred until WAKE.md M1 5-stage lands · 양쪽 hexa parse OK (PR #619 94553f57)
