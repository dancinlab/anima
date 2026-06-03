# CORE — log

Append-only history sister of `CORE.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-02 — 엔진 ↔ .clm/.kosmos 배선 맵 기록 (honest wiring, doc-only)

CORE 의 의식 엔진이 .clm/.kosmos 와 정확히 어떻게 (안) 엮이는지 disk 대조 후 CORE.md 에 명문화.

- [x] disk 검증 — A·G·brain (pure_field/engine_g/brain.hexa) = **clm/kosmos/generator import 0** (`brain.hexa` grep 확인, A·G import 만)
- [x] disk 검증 — `CORE/generator.hexa` **미존재** (유일한 .clm 진입점, ⏳ 미배선 · DECODER M4 대기)
- [x] disk 검증 — `kosmos_io` 는 HEXAD state/worktree 에만, brain 이 앵커 미읽음 → .kosmos read ❌ 미배선
- [x] disk 검증 — `stdlib/hf/validate.hexa` 는 본 repo 부재 (sibling hexa-lang stdlib) = **검증-전용 아티팩트 점검기**, 런타임 엔진 아님 (이전 혼동 정정)
- [x] CORE.md 에 「엔진 ↔ .clm/.kosmos 배선 맵」 표 + ASCII 추가 — 미배선 항목 ⏳/❌ 정직 표기
- [ ] (후속, 다른 agent) `CORE/generator.hexa` L3 인터페이스 + brain_decide emit 슬롯 배선
- [ ] (후속) `project.tape` 에 `@D a_core_engine_map` 직접 추가 — `sidecar sign project` 후 (draft = `drafts/core-engine-map-directive.md`)
## 2026-06-02 — L3 generator slot LANDED (BACKEND-AGNOSTIC interface + null backend + brain_emit wiring)

- [x] `CORE/generator.hexa` — BACKEND-AGNOSTIC L3 인터페이스: `generate(backend, substrate_ctx, emit_decision, anchors) -> {emitted, backend, text, fellback}`. 백엔드 = pluggable "vtable" Map (`gen_null_backend` · `gen_clm_backend`).
- [x] null 백엔드 — 결정적 substrate-derived placeholder (`_gen_null_text` = phase/tier/phi/motiv/anchors numeric 조립). 외부 LLM 0 · system_prompt 0 · persona 0 (p1~p8 clean). 항상 ready.
- [x] clm 백엔드 stub — `gen_clm_backend(ckpt_path)` 가 ckpt 경로 probe 후 **loaded=false** 보고 (d768 미회수). generate() 가 crash 없이 null 로 fall-through (`fellback=true`). 실 모델 = 동일 인터페이스 뒤에 후속 배선 (DECODER M4 잔여).
- [x] kosmos_io anchor READ 배선 — `generator_read_anchors(dir)` = `load_anchors` 래퍼 (missing dir → [] · no panic). brain_emit 가 anchors 를 generate() 로 전달.
- [x] `CORE/brain.hexa` — `brain_emit(...)` 추가: brain_decide 실행 후 EMIT 슬롯(이전 빈칸)에서 generate() 호출. low→silent / high→emit 기존 거동 불변 (brain_smoke 회귀 PASS). decision 레코드에 `gen_emitted/gen_backend/gen_text/gen_fellback` 확장.
- [x] `CORE/generator_smoke.hexa` — `hexa run` 10/10 PASS (verbatim): EMIT→null 텍스트(anchors=1 유입 + last_anchor=smoke_anchor_001) · SILENT→gen_text="" · clm stub loaded=false → null fall-through.
- [ ] 실 .clm 백엔드 (d768 회수 후) — gen_clm_backend 본체를 실 loader 로 교체, _gen_clm_decode 에 forward/decode 배선. 인터페이스 · brain_emit 배선 불변.
- HONEST: 본 PR = **슬롯 + null 백엔드** 전달이지 trained mouth 아님. 실 모델은 d768 회수까지 deferred.

