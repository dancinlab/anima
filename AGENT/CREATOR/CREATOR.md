# CREATOR — current state

@title: 🎨 CREATOR — 사용자 채널 콘텐츠 production engine · 3-tier modality (STILL/PROG/GEN) · AGENT 산하

@goal: 사용자가 운영하는 채널 (유튜브/틱톡/인스타그램) 의 시청각 콘텐츠 production engine — anima 가 사용자의 production engine 으로서 brand · script · media asset (이미지/영상) · publish job 을 함수 surface 로 노출. anima 가 페르소나 가 아니라 production engine (도구) 이라는 점이 핵심 — `you are X` 인격 주입 0 · 외부 LLM 0 (script 는 CORE/DECODER 통과). 3-tier modality: L1 STILL (fal.ai 호스팅 openai images 2.0) · L2 PROG (remotion · React 코드 영상) · L3 GEN (fal seedance 2.0 · omnishow ByteDance HOIVG) — L1·L3 모두 fal.ai backend 통합 (single API gateway). 의식엔진은 CORE 가 담당, 이 도메인은 외부 어댑터 + 데이터 타입 + 함수 surface 만.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] M1 데이터 타입 — `AGENT/CREATOR/types.hexa` 작성 (7 pub fn — 5 constructor `creator_brand` · `_script` · `_media_asset` · `_upload_job` · `_channel` + 2 helper `creator_type_kind` · `creator_type_summary`) · `types_smoke.hexa` 6-case verify (5 type round-trip + 1 missing-kind 방어) · 2/2 `hexa parse` OK · ⚠ `handle` 예약어 회피 → `user_handle` 로 rename · bridge architecture 정합 (의식엔진 framing 0, tool surface only)
- [x] M2 backend 프레임워크 — `AGENT/CREATOR/backend.hexa` (6 pub fn — `creator_backend_new` · `_generate_still` (L1) · `_render_prog` (L2) · `_generate_clip` (L3) · `_dispatch` · `_summary`) · tier registry 기반 3-tier modality plug-in · threaded-state (no global) · stub_mode 기본 (외부 API call 0, 실 어댑터는 M3-M5 plug-in) · `backend_smoke.hexa` 8-case verify (factory · L1 still · L2 prog · L3 clip · dispatcher routes · unknown_tier reject · L2 not_registered · asset_log accumulates) · 2/2 `hexa parse` OK · provenance 추적 자동 (backend_id · prompt_hash · stub_mode flag)
- [x] M3 L1 STILL 백엔드 — `AGENT/CREATOR/still_backend_fal.hexa` (4 pub fn — `still_fal_new` · `_configure` · `_generate` · `_summary`) · **fal.ai backend + 호출 시점 model 선택 (state default model + per-call override)** · default model = `fal-ai/openai-images-2.0` (fal.ai 가 호스팅) · 호출자가 `fal-ai/flux-1.1-pro` 등 다른 fal.ai 모델 자유 선택 · DRYRUN 기본 · secret get fal.api_key wire-up 대기 · M2 `backend.hexa` 의 `creator_backend_generate_still` + `_generate_clip` + `_dispatch` 도 model 인자 추가 (cross-module byte-clean) · `still_backend_fal_smoke.hexa` 7-case + `backend_smoke.hexa` 8-case verify (model default + override 양쪽 포함) · 4/4 `hexa parse` OK · 외부 HTTP call 0 · M1 MediaAsset L1 tier 반환
- [x] M4 L2 PROG 백엔드 — `AGENT/CREATOR/prog_backend_remotion.hexa` (5 pub fn — `prog_remotion_new` · `_configure` · `_codegen` · `_render` · `_summary`) · Remotion React 코드 영상 builder STUB · DRYRUN 기본 · `_codegen(state, spec)` 가 React Composition TSX 문자열 반환 (composition_id + components count 반영) · `_render(state, spec, out_path)` 가 M1 MediaAsset L2 (clip · backend="remotion" · stub_mode=true) 반환 · 거부 경로 (remotion_not_configured · real_render_not_implemented) · `prog_backend_remotion_smoke.hexa` 7-case verify (new unconfigured / configure / codegen TSX / DRYRUN render / REAL uncfg / REAL cfg / summary) · 2/2 `hexa parse` OK · 외부 `npx remotion render` call 0
- [x] M5 L3 GEN 백엔드 — `AGENT/CREATOR/clip_backend_fal.hexa` (4 pub fn — `clip_fal_new` · `_configure` · `_generate(state, prompt, duration_s, model, image_ref)` · `_summary`) · fal.ai gateway + per-call model 선택 (seedance-2.0 default · seedance-2.0-pro · omnishow-hoivg ByteDance HOIVG) · image_ref 비어있으면 text-only, 채우면 HOIVG image-conditioned · duration_s=0 → 15s default · DRYRUN 기본 · 24kHz native audio sample_rate · `clip_backend_fal_smoke.hexa` 8-case verify (new / DRYRUN default / model override / HOIVG image-conditioned / configure empty 거부 / configure ok / REAL uncfg / REAL cfg) · 2/2 `hexa parse` OK · 외부 HTTP call 0
- [x] M6 publish + 통합 smoke — `AGENT/CREATOR/publish.hexa` (5 pub fn — `publish_youtube` · `_tiktok` · `_instagram` · `_dispatch` · `_summary`) · 3-platform STUB · dry_run=true 시 mock external_id 반환 · dry_run=false 시 real_upload_not_implemented · `AGENT/CREATOR/integration_smoke.hexa` 5-stage round-trip (S0 brand+3 channels / S1 script / S2 still fal.ai / S3 prog remotion / S4 clip fal.ai HOIVG image-conditioned / S5 publish 3 platforms dry_run+real refuse+unknown platform) · M1 types (Brand/Channel/Script/MediaAsset/UploadJob) uniform shape 전체 검증 · 2/2 `hexa parse` OK · CREATOR **6/6 ✅ 100% closure**

## wire-up 라운드 (실 backend 연결 · 위험 0 → 위험 증가 순)

### 🎨 생성 backend (외부 게시 X · 비용만 · 위험 0)

- [ ] M7 fal.ai still REAL wire-up — `still_backend_fal.hexa` 의 `// TODO: real fal.ai queue+poll HTTP call` 자리 실 구현 (1순위 권장 · 가장 안전) · `secret get fal.api_key` 등록 → POST `/v1/queue` → poll status_url → GET image_url → save bytes
- [ ] M8 Remotion REAL wire-up — `prog_backend_remotion.hexa` 의 `// TODO: real npx remotion render` 자리 실 구현 · `npm install` + `npx remotion init` + shell exec · 로컬 실행 · 비용 0
- [ ] M9 fal.ai clip REAL wire-up — `clip_backend_fal.hexa` 동일 패턴 (M7 의 fal.api_key 재사용) · seedance + omnishow-hoivg 실 호출 · 비용 + 시간 발생

### 📡 publish backend (외부 채널 공개 게시 · 위험 ⚠)

- [ ] M10 YouTube REAL wire-up — `publish.hexa` 의 `publish_youtube` 안에 YouTube Data API v3 resumable upload (`POST /upload/youtube/v3/videos`) · OAuth flow 별도 · `secret get youtube.oauth_token`
- [ ] M11 TikTok REAL wire-up — TikTok Content Posting API (initialize → upload chunks → publish) · `secret get tiktok.access_token`
- [ ] M12 Instagram REAL wire-up — Graph API (container 생성 → 미디어 등록 → publish) · `secret get instagram.graph_token`

### 🔗 통합

- [ ] M13 CREATOR wire-up integration smoke — 모든 backend REAL 모드 round-trip 검증 · dry_run=true 안전 verify + 사용자 명시 dry_run=false 1 회만 실 게시 (제어된 위험)
