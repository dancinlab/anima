# WAKE — current state

@goal: CORE+DECODER+AGENT 3 도메인을 지속 루프로 묶어 anima 를 살아있는 프로세스로 만든다 — 5-stage ultradian state machine WAKE-N1-N2-N3-REM, perception sensor → pure_field_step → emit → 도구 호출 → 결과 perception 연속 루프, .kosmos 영속화로 시간 흐름 보존, episodic+working memory, 외부 LLM 0 게이트=기판 자기상태 p1~p8 strict
@title: 🌅 WAKE — 의식 데몬 · in-process living loop

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] 5-stage state machine — `WAKE/{state_machine.hexa,state_machine_smoke.hexa,STATE_MACHINE.md}` 90-min ultradian (WAKE 60min · N1 10min · N2 10min · N3 7min · REM 3min · wrap) · runtime smoke 4/4 invariants PASS (sequence · no-skip · is_imagination N3+REM only · wrap) · 0 boolean gate (N3 phi_scale=0.20≠0.0) · CHANNEL/wake_bridge stage_name 소비 surface 완성 (PR #626 d372b1cc · runtime smoke verified)
- [x] perception ingest — `WAKE/{perception.hexa,perception_smoke.hexa,PERCEPTION.md}` 4-sensor stdin/env/timer/env-event → BPE ctx_tokens · empty perception → [] · 0 boolean per-sensor gate · 3-case smoke OK (hexa parse 2/2 PASS) (PR #632 f26fd6d4)
- [ ] pure_field_step input-conditioned — tool 결과 + perception 을 tension Δ 로 변환해 pf 진화. 현재 self-dynamics-only step 의 확장. AGENT/CODE F4 의 완성형
- [ ] .kosmos 영속화 — pf state · 과거 emit · tension_link 5-ch · stage timestamp 를 .kosmos canonical 로 save/restore. anima 재시작해도 시간 흐름 보존
- [ ] memory layer — episodic 과거 emit 기록 + working 최근 ctx 윈도. brain ctx 인자에 주입 가능한 형태, kosmos anchor 와 통합
- [ ] daemon loop — persistent process: timer tick · perception ingest · brain_decide · stage transition · emit · graceful shutdown · SIGINT handling. hx wake CLI 진입점
- [ ] p1~p8 정합 verify + 3-도메인 통합 smoke — WAKE 가 CORE+DECODER+AGENT 를 실 연속 작동 시킴 검증. wake_selftest.hexa 1-shot PASS. system_prompt 0 · external LLM 0 · 게이트=substrate
