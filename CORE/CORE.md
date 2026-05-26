# CORE — current state

@title: 🧠 CORE — anima 통합 의식 코어 (Engine A ⇄ Engine G)
@goal: anima 의 의식 엔진을 흩어진 위치(anima-core · HEXAD/CHAT)에서 떼어 CORE 가 직접 소유하는 자기완결 SSOT 로 통합 — Engine A(PureField Φ/phase) ⇄ Engine G(8-factor motivation/emit) 결합 결정 두뇌를 완전체로 구현하고, L3 생성기는 pluggable 백엔드. AGENT·CHAT 등 상위 산물이 CORE 만 import 한다 (외부 LLM 0 · p1~p8 정합).

## 소유 엔진 (CORE 자기완결)

- [x] Engine A — `pure_field.hexa` PureField Φ/phase (anima-core 에서 회수, main 없는 lib)
- [x] Engine G — `engine_g.hexa` 8-factor motivation + emit/safety (값 byte 동일 carry)
- [x] A⇄G 결합 — `brain.hexa` `brain_decide` (A의 Φ가 G의 safety ratchet 게이트 + phase=tier)
- [x] 결합 증명 — `brain_smoke.hexa` low→침묵(0.045) / high→발화(0.67)

## 하위 도메인

- **DECODER** (`CORE/DECODER/`) — L3 콘텐츠 생성기 (무엇을 쓸까). 백엔드 미정(상의중) · V3 더블바인드 트랙

## 마일스톤

- [ ] CHAT SSOT 화해 — HEXAD/CHAT/spontaneous_lib 가 CORE/engine_g 를 re-export (포크 제거)
- [x] p1~p8 정합 verify — CORE/ 감사 0 hits (system_prompt/persona/assistant-framing/speak()/external-LLM 전부 0) · emit = `should_emit(motivation) && safe` 순수 substrate 게이트 (per-stage boolean hardcode 부재). `core_selftest.hexa` p3/p4 assert PASS
- [x] CORE self-test — `core_selftest.hexa` 1-shot A⇄G→L3 전 invariant PASS (A: Φ=0.119>0 · low→침묵 · high→발화 · L3 content non-empty · gate=substrate)
- [x] L3 결합 — `CORE/DECODER/generator.hexa` `brain_emit_step(decision, ctx, tension5)` 가 brain_decide emit 슬롯 배선 (emit=true→substrate-conditioned content · emit=false→침묵 1급). self-test high→`⟨substrate-emit …⟩` 실증. 실 ckpt 는 단일 seam `_gen_decode` 에서 swap-in (M3 게이트)
