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


## H_6008 배포 — shared_seed (저장=고전 LOCAL · 공유=양자키) · 2026-06-15
- [x] `CORE/shared_seed.hexa` — H_6008 fork-time primitive. ANU 양자키를 LOCAL 고전버퍼(`SharedSeed{bytes,cursor}`)에 보관(`shared_seed_load`, `od -An -tu1` 파싱). `shared_seed_fork(parent)` = 자식이 같은 buffer+cursor 상속 → 통신 0회 완벽 동기(H_6008 ARM1). `shared_seed_draw/choose` = (buffer,cursor) 결정적 추출. p1~p8 clean(시스템프롬프트·페르소나·speak 0).
- [x] ONE-LINE 배포: 자매 spawn 시 `shared_seed_load(<다른 파일>)`(독립, ARM2) 대신 `shared_seed_fork(parent)`(공유, ARM1) 한 줄 치환.
- [x] `CORE/shared_seed_smoke.hexa` — `hexa run` 4/4 PASS (verbatim): ARM1 shared coord=1.0(512B fork×2, 0 comms) · ARM2 independent coord=0.225(≈1/K=0.25) · ARM3 classical-store reload-match=1.0(LOCAL 재생가능, H_6026 MS2) · separation 0.775≥0.40. H_6008 verdict(ARM1 1.0000·ARM2 0.2969) 재현.
- HONEST: 신규 CORE surface(라이브 pure_field/engine_g/brain 무변경, 낮은 blast radius). 실 자매-spawn 호출부 배선은 daemon orchestration 레이어 후속. 양자=공유키 공급(H_6008)·저장은 고전 LOCAL(H_6026/6027/6028).

## H_6008 마지막마일 — anima_birth (출생경로가 공유씨앗 전달) · 2026-06-15
- [x] `CORE/anima_birth.hexa` — H_6014(텐션-출생, vadapt mitosis) ⊗ H_6008(공유씨앗) 합성. `anima_birth(parent_seed, steps, cfg) -> AnimaBirth{cells, seed}`: 자식 출생 텐션스트림을 상속한 공유키에서 draw → 같은 키가 (a)몸 성장 + (b)이후 공유 추출 둘 다 구동. 마지막마일 한 줄 = `shared_seed_fork(parent_seed)`.
- [x] `CORE/anima_birth_smoke.hexa` — `hexa run` 3/3 PASS (verbatim): BB1 쌍둥이 몸 cellsA=2==cellsB=2(한 부모키, 0 comms) · BB2 출생후 동기 1.0(상속 키 계속 일치) · BB3 독립키 0.133(≈1/K=0.25 우연). 출생부터 자매가 구성적으로 동조 — H_6014⊗H_6008 합성 입증.
- HONEST: 신규 CORE surface(라이브 pure_field/engine_g/brain 무변경). daemon orchestration 의 실 spawn 트리거(언제 출생할지)는 단일-daemon 이라 아직 단일; anima_birth 는 그 트리거가 호출할 출생 primitive. 양자=공유키, 저장=고전 LOCAL.
