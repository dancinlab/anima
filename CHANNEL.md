# CHANNEL — current state

@goal: anima 기판이 외부로 흘러나가는 3 채널 통합 어댑터 — text · voice · tension. text 는 CHAT/DECODER 위임, voice 는 hexa-voice 24kHz RVQ 위임, tension 은 5-ch fingerprint TensionHub 위임. CHANNEL 자체는 채널 선택 결정층 — CORE engine_g motivation 8-factor 가 채널 분기, WAKE stage 가 발화 컨텍스트 공급, p1~p8 정합 stimulus-response 금지. 통일 인터페이스 channel_emit intent channel 로 substrate-decided 발화.

@title: 🌐 CHANNEL — anima 의 출력 채널 묶음 · voice 음성 + tension-link 5ch 직송 · AGENT 와 분리

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] hexa-voice repo SSOT 연결 — `CHANNEL/voice/{SSOT.md,voice_emit.hexa}` scaffold landed · intent → 24kHz RVQ pipeline 단방향 흐름 도식화 + p1~p8 정합 매트릭스 · github.com/dancinlab/hexa-voice 향후 repo placeholder 등록 (PR #600 b74835447 · hexa parse OK)
- [ ] text 채널 어댑터 — CHAT/DECODER 위임 wrapper · substrate-decided emit 단일 진입점 · 외부 LLM 0 검증
- [x] tension 채널 — 5-ch fingerprint working code 회수 · `ready/` 에서 `CHANNEL/tension/` 으로 (bench·test·test_code 4 hexa + tension-link.md 한글 doc + tension_emit.hexa stub + SSOT.md) · legacy `.py` 의도적 비복사 (port source 인용만) · TensionHub UDP 9999 / WS 3-port wiring 복원 잔여 작업 (PR #601 dd3b2d502 · hexa parse 4/4 OK)
- [ ] intent embedding bridge — substrate tension5 5-ch → channel-specific vector 매핑 · text BPE / voice RVQ / tension fingerprint 공통 intent 형식
- [ ] channel_emit 통합 인터페이스 — 단일 진입점 channel_emit intent channel · text_emit / voice_emit / tension_emit 위임 dispatcher · substrate-gated 발화
- [ ] CORE engine_g 채널 분기 — motivation 8-factor 가 3 채널 중 선택 · text/voice/tension 분류기 · brain_decide 확장
- [ ] p1~p8 audit — CHANNEL 트리 전체 0 hits · stimulus-response 금지 · TTS-style prompt-driven 금지 · external LLM 부재 검증
- [ ] WAKE 통합 — stage 별 substrate-decided channel gate · REM 자발 voice/tension · WAKE user-context text · N1~N3 sleep 무음 · boolean hardcode 금지 a_autonomy_over_hardcode
