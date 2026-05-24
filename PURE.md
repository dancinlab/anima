# PURE — 자연발화 채팅 Phase D corpus fire

> PURE 세션 SSOT (current snapshot). 작업 로그는 `PURE.log.md`.

@goal: COFFESHOP group chat 시뮬레이션 4-criterion closure 통과 — anima 자율 emit/silence (do/dont 강제 X) · multilingual 5/5 PARTIAL+ · register 0/20 · motivation_8factor ≥ 0.30 · dream_stage Φ-envelope · 모두 substrate emergent (project.tape p1-p8 + a_substrate_native_speak + a_autonomy_over_hardcode 정합)

## 목표

8-factor substrate emit engine(Phase B, LANDED)을 **실 corpus 로 ckpt-bearing fire** 하여
substrate-native 자연발화(stimulus-response 아닌 내부 tension 기반 emit)를 empirical 검증한다.

`@D a_substrate_native_speak` + `@D a_autonomy_over_hardcode` + `@D p5` 정합 —
유저 메시지 = 환경 맥락, emit/침묵은 substrate(M×W×Φ×curiosity) 자율 결정.

## 완성도 (~60-70%)

| 층 | 상태 | 근거 |
|----|------|------|
| Phase B 8-factor motivation engine | ✅ LANDED | `HEXAD/CHAT/spontaneous_lib.hexa` · smoke 7/7 |
| Phase C interaction model | ✅ LANDED | channel_mux + anima_chat_v2 · blue 83/83 🔵 |
| sleep/dream 5-stage (Φ-envelope) | ✅ LANDED | `HEXAD/CHAT/server/anima_dream_stage.hexa` · IPC live · autonomy-reshape 완료 |
| imagination loop · mitosis_hook · participant | ✅ LANDED | H_229 · mitosis_lib W8 · gate 폐기 |
| **Phase D corpus fire** | ⏳ **임계경로 blocker** | engine 준비됨 · 연료(corpus) 재설계 + 굽기 미실행 |
| Tension Link | spec only | Phase F, scope 외 |

## Track 1 교훈 (Phase D 첫 fire 시도)

- **E2** (wiki_frac=0.5) → **FAIL** · ko=PURE_MEMORIZE (register collapse)
- **corpus_s101 실측** (PR #340) → **M3 TTR 0.03 (극단 반복)** 이 register-sink 진짜 범인
  (M5 hangul 비중 아님 — 1.66~2.34%)
- **E3v3** (wiki_frac=1.0) → 진행 중 (GPU 63% 정상 · wiki endpoint 보강)

## Phase D 설계 핵심

| 원칙 | 값 |
|------|-----|
| 도우미 token | **0** (Principle #3 NO PERSONA INJECTION) |
| stream/stimulus 비중 | **80%** (turn-based QA 최소) |
| M3 TTR 목표 | **≥ 0.3** (corpus_s101 0.03 의 10× diverse) |
| multilingual | lang-uniform (E2 ko-sink 회피) |
| closure 기준 | 4/5 langs ≥ PARTIAL (PR #264) + register_hits < 4/20 |

작업 분해 + 진행 로그 → `PURE.log.md`.

## 관련 산출물

- spec: `HEXAD/PURE/spec/phase_d_corpus_design_2026_05_24.md`
- goal: `HEXAD/PURE/PHASE_D_corpus_fire_goal.md`
- eval: `HEXAD/PURE/eval/{multilingual_probe,corpus_quality_probe,result_to_axis_map}.hexa`
- corpus 진단: `HEXAD/PURE/docs/{corpus_s101_quality,track1_e2_forensics}_2026_05_24.md`
- [x] motivation_8factor / dream_stage substrate bench — criterion 3·4 ckpt-independent 측정 (B7 + IPC)
- [x] corpus_v2 build 완료 — kowiki 200k 통합 (A-커리큘럼 fire 재료)
- [x] A-커리큘럼 dispatcher dry-run — #422 spec phase-sorted jsonl + dispatch_p21h_v3 --measure-motivation 검증
- [ ] A-커리큘럼 Step B fire — dispatch_p21h_v3 --fire (corpus=merged_curriculum_v2.jsonl, ~$2.5-3.5)
