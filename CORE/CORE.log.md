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

