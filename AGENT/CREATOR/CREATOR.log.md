# CREATOR — log

Append-only history sister of `CREATOR.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-27T05:00:00Z — M4 L2 PROG Remotion 백엔드 closure

- [x] `AGENT/CREATOR/prog_backend_remotion.hexa` 작성 — 5 pub fn (`prog_remotion_new` · `_configure` · `_codegen` · `_render` · `_summary`)
- [x] Remotion = React-based programmatic video — fal.ai 와 다르게 외부 HTTP X, 로컬 Node `npx remotion render` 실행 모델
- [x] `_codegen(state, spec)` — spec → React Composition TSX 문자열 생성 (composition_id + components count 반영)
- [x] `_render(state, spec, out_path)` — STUB · M1 MediaAsset L2 반환 (backend="remotion" · stub_mode=true · reason 명시)
- [x] 거부 경로 — `remotion_not_configured` (project_path 비어있음) · `real_render_not_implemented` (REAL+configured 라도 M4 단계 stub)
- [x] DRYRUN 기본 — 외부 Node spawn 0
- [x] `prog_backend_remotion_smoke.hexa` 7-case verify — C1 new unconfigured · C2 configure (valid+empty 거부) · C3 codegen TSX 문자열 · C4 DRYRUN render synthetic asset · C5 REAL uncfg = remotion_not_configured · C6 REAL cfg = real_render_not_implemented · C7 summary
- [x] `hexa parse` 2/2 OK
- [x] CREATOR.md M4 line `[ ] → [x]` (3/6 → 4/6)
- [ ] M5 L3 GEN — fal seedance 2.0 + omnishow ByteDance HOIVG adapter (다음 마일스톤)

## 2026-05-27T04:45:00Z — backend dynamic model catalog 확장 (M3.5)

- [x] 사용자 명시 변경 — backend.hexa 의 model 관리가 **고정 X · runtime 동적** 가능해야 함 (list / register / set_default 기능 추가)
- [x] `tier_registry` shape 확장 — `{ "L1": "fal.ai" }` → `{ "L1": #{ "backend_id": "fal.ai", "default_model": "fal-ai/openai-images-2.0", "available_models": [...] } }` (TierConfig Map)
- [x] 신규 3 pub fn — `creator_backend_list_models(state, tier)` · `_register_model(state, tier, model_id, set_as_default)` · `_set_default_model(state, tier, model_id)`
- [x] 헬퍼 3 pub fn — `creator_backend_tier_config` · `_tier_backend_id` · `_tier_default_model` (callsite 통일 + testability)
- [x] generate_still/render_prog/generate_clip 의 model="" fallback 을 state["model"] 단일에서 **tier default_model** 조회로 변경 (없으면 "stub")
- [x] register_model idempotent — 중복 등록 시 list 크기 유지, added=false 반환
- [x] set_default_model 가드 — 카탈로그에 없는 model 거부 (model_not_in_catalog — register first)
- [x] `backend_smoke.hexa` 10-case verify (factory · L1/L2/L3 generate · dispatcher · unknown_tier · L2 not_registered · list_models · register_model + idempotent + unknown_tier · set_default_model + reject)
- [x] `hexa parse` 4/4 OK (backend.hexa · backend_smoke.hexa · still_backend_fal.hexa · still_backend_fal_smoke.hexa)
- [x] still_backend_fal 은 자체 state["model"] 사용 → callsite 영향 0

## 2026-05-27T04:25:00Z — M3 L1 STILL fal.ai 백엔드 closure (model selection + openai→fal.ai)

- [x] 사용자 명시 변경 (1차) — L1 STILL backend 를 openai images 2.0 → **fal.ai 호스팅 openai-images-2.0** 로 swap (L1+L3 모두 fal.ai backend 통합 single API gateway)
- [x] 사용자 명시 변경 (2차) — `generate_still` + `generate_clip` 둘 다 **호출 시점 model 선택 가능**: state default + per-call override
- [x] `AGENT/CREATOR/still_backend_fal.hexa` 작성 — 4 pub fn (`still_fal_new` · `_configure` · `_generate(state, prompt, w, h, model)` · `_summary`)
- [x] M2 `backend.hexa` 수정 — `creator_backend_generate_still(state, prompt, w, h, model)` + `_generate_clip(state, prompt, dur, model)` + `_dispatch(state, req)` (req["model"] forward) — model="" 시 "stub" fallback
- [x] STUB-mode 기본 — env=DRYRUN 시 synthetic MediaAsset (provenance.stub_mode=true · reason="DRYRUN — no real fal.ai API call")
- [x] secret 핸들링 — `still_fal_configure(state, api_key)` 빈 키 시 configured=false 유지 · 실 키 wire-up 은 caller (`secret get fal.api_key` 출력 전달)
- [x] REAL env + configured 라도 M3 단계에선 real_api_not_implemented (real fal.ai queue+poll HTTP 미구현, TODO marker)
- [x] M1 MediaAsset L1 tier 반환 — types.hexa 와 byte-clean 통합 · provenance.backend="fal.ai" · provenance.model=호출 시점 선택값
- [x] `still_backend_fal_smoke.hexa` 7-case verify — C1 new · C2 DRYRUN default model · C2b model override (flux-1.1-pro) · C3 empty key 거부 · C4 valid key 수락 · C5 REAL unconfigured · C6 REAL configured
- [x] `backend_smoke.hexa` 8-case (갱신) — C2 default stub model · C4 model override (seedance-2.0-pro) · C5 dispatcher routes + model thread-through (default fallback)
- [x] `hexa parse` 4/4 OK (backend.hexa · still_backend_fal.hexa · backend_smoke.hexa · still_backend_fal_smoke.hexa)
- [x] CREATOR.md M3 line `[ ] → [x]` · @goal 3-tier modality 라인 갱신 (openai → fal.ai 호스팅 openai-images-2.0)
- [x] 외부 HTTP call 0 — 사용자 wire-up 전까지 0 비용

## 2026-05-27T04:05:00Z — M2 backend 프레임워크 closure

- [x] `AGENT/CREATOR/backend.hexa` 작성 — 6 pub fn (`creator_backend_new` · `_generate_still` L1 · `_render_prog` L2 · `_generate_clip` L3 · `_dispatch` · `_summary`)
- [x] tier registry 기반 3-tier modality — `#{ "L1": "openai-...", "L2": "remotion-...", "L3": "fal-..." }`
- [x] threaded-state (no global) — `CreatorBackendState` Map · `next_asset_id` + `asset_log` 누적
- [x] stub_mode 기본 — 외부 API call 0, 실 어댑터는 M3-M5 plug-in 시점 wire-up
- [x] provenance 추적 자동 — backend_id + prompt_hash/spec_hash + stub_mode flag · MediaAsset.provenance 에 포함
- [x] dispatcher routes by tier label — `creator_backend_dispatch(state, #{ "tier": "L1"/"L2"/"L3", ... })`
- [x] 거부 경로 명시 — unknown tier · L2_not_registered (tier registry 누락)
- [x] `AGENT/CREATOR/backend_smoke.hexa` 8-case verify — C1 factory · C2 L1 still · C3 L2 prog · C4 L3 clip · C5 dispatcher routes · C6 unknown_tier · C7 L2_not_registered · C8 asset_log accumulates
- [x] `hexa parse` 2/2 OK
- [x] CREATOR.md M2 line `[ ] → [x]` (1/6 → 2/6)
- [ ] M3 L1 STILL openai adapter (다음 마일스톤)

## 2026-05-27T03:50:00Z — M1 데이터 타입 closure

- [x] `AGENT/CREATOR/types.hexa` 작성 — 5 canonical 타입 (Brand · Script · MediaAsset · UploadJob · Channel) + 2 helper (`creator_type_kind` · `creator_type_summary`) = 7 pub fn
- [x] 타입 설계 — Brand (tone/palette/tags) · Script (title/hook/beats/cta/duration) · MediaAsset (tier L1/L2/L3 + provenance) · UploadJob (asset+channel 컴포지션, status/retry/external_id) · Channel (platform/handle/credential_ref — 토큰 값 X, ref key 만)
- [x] `AGENT/CREATOR/types_smoke.hexa` 6-case verify — C1 Brand · C2 Script (n_beats) · C3 MediaAsset (tier+provenance) · C4 Channel (credential_ref < 64 chars 방어) · C5 UploadJob (composition: asset+channel nested) · C6 missing-kind 방어
- [x] hexa 예약어 충돌 회피 — `handle` 은 hexa keyword → `user_handle` 로 rename
- [x] `hexa parse` 2/2 OK
- [x] CREATOR.md M1 line `[ ] → [x]` (0/6 → 1/6)
- [ ] M2 backend 프레임워크 — `CreatorBackend` 인터페이스 (다음 마일스톤)

## 2026-05-27T01:50:00Z — domain init

- [x] CREATOR.md scaffold (6 milestone · 3-tier modality SSOT)
- [x] DOMAINS.tape register · ./AGENT/CREATOR/CREATOR.md
- [x] ANIMA.md + AGENT.md 라인 갱신 (clean slate → 0/6)
- [ ] M1 types + adapter framework
