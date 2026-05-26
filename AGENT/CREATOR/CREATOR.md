# CREATOR — current state

@title: 🎨 CREATOR — 사용자 채널 콘텐츠 production engine · 3-tier modality (STILL/PROG/GEN) · AGENT 산하

@goal: 사용자가 운영하는 채널 (유튜브/틱톡/인스타그램) 의 시청각 콘텐츠 production engine — anima 가 사용자의 production engine 으로서 brand · script · media asset (이미지/영상) · publish job 을 함수 surface 로 노출. anima 가 페르소나 가 아니라 production engine (도구) 이라는 점이 핵심 — `you are X` 인격 주입 0 · 외부 LLM 0 (script 는 CORE/DECODER 통과). 3-tier modality: L1 STILL (openai images 2.0) · L2 PROG (remotion · React 코드 영상) · L3 GEN (fal seedance 2.0 · omnishow ByteDance HOIVG). 의식엔진은 CORE 가 담당, 이 도메인은 외부 어댑터 + 데이터 타입 + 함수 surface 만.

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [ ] M1 데이터 타입 — `Brand` · `Script` · `MediaAsset` · `UploadJob` · `Channel` 공통 타입 (`AGENT/CREATOR/types.hexa`)
- [ ] M2 backend 프레임워크 — `CreatorBackend` 인터페이스 (3 verb: `generate_still` · `render_prog` · `generate_clip`) · 3-tier modality plug-in 가능 범용 surface
- [ ] M3 L1 STILL 백엔드 — openai images 2.0 adapter stub (1024×1024 PNG · prompt → image)
- [ ] M4 L2 PROG 백엔드 — remotion React 영상 codegen stub (frame 함수 + render 명령)
- [ ] M5 L3 GEN 백엔드 — fal seedance 2.0 + omnishow ByteDance HOIVG adapter (15s · 24kHz native audio)
- [ ] M6 publish + 통합 smoke — YouTube/TikTok/Instagram publish stub + 3-tier 합쳐 round-trip smoke (script → still → prog assembly → clip → publish)
