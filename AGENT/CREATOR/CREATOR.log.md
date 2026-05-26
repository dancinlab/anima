# CREATOR — log

Append-only history sister of `CREATOR.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

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
