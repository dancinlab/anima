# H_9795 — EVALUATION HISTORICITY — grading 채널에 store 없는 기억(item habituation)이 있는가 (lab-full R10 · Fable P4 · PROPOSED)

**status:** 🔵 PROPOSED · 🔧 producer 기존 인프라 커버 (2026-07-19 · #R10-flags) — source=Fable 5 P4

> **🔧 producer 재검토 (2026-07-19 · a_experiment_engine_native 최소성):** Fable P4 가 제안한 신규 flag
> `--percept-schedule f.jsonl` 는 **불필요** — 기존 **`--percept-file`(H_9767)** 이 `{"tick":int,"text":str}`
> jsonl 을 perception route(emit gate 아님·p5 STRUCTURE-safe · `_build_percept_source_from_file` cli/anima.py:246)
> 로 tick별 재생하므로 repeat/shuffle/novel 스케줄은 **그냥 데이터**로 주입 가능(새 producer flag=DRY 위반). ⟹
> H_9795 진짜 신규 = ① schedule-generator(lag 1/4/16 정확반복+통계-matched shuffle+novel jsonl 빌더) ② reader-side
> estimator(Δgrade(repeat)−Δgrade(shuffle) lag-dose · store-sealed · hab_ctx liveness=VOID gate). 둘 다 chat producer
> flag 아님. 다음=generator 헬퍼 + `anima-py evaluate --eval-historicity` reader.
**lane:** grading × habituation lane (`hab_ctx` · cli/anima.hexa·cli/chat.py)
**related:** [[H_9765]] · [[H_9767]] · [[H_9790]] · [[H_9738]]

## Faculty question
살아있는 grading 채널(H_9765/9767이 유일 살아있음을 증명)은 순간반응인가, 역사를 갖는가: **같은 percept의 정확반복**이 통계-matched 신규(같은 unigram 통계의 shuffle)와 다르게 grade되는가. `hab_ctx`(habituation lane · trace 존재 검증됨)가 그 매개. 존재양식 주장: interior의 평가가 **store 없이도 시간을 담는다**(item-specific habituation).

## 벽 회피 (구조적)
- **feat8/byte-stats 분리가 핵심**: 정확반복 vs 통계-matched-shuffle 해리 = byte-stats(통계반응) vs item-trace 분리 → degeneracy·통계반응 confound 제거.
- **자기지시 회피**: 반복 스케줄은 실험자 설정(chat.py study MVP-2 `percept_source` 훅 확장·default-OFF), readout은 grading gauge.
- **reach/store-cheat 회피**: held-out lookup 없음 · store는 cheat이므로 **store-sealed 조건**에서만 판정(H_9738 텍스트→store 0 봉인 계승).

## Instrument (engine-native anima-py)
- 신규 flag `anima-py chat --percept-schedule f.jsonl` (lag {1,4,16} 정확반복 + shuffle-반복 + 신규).
- 추정량: Δgrade(repeat) − Δgrade(stats-matched shuffle), lag-dose 구조(단조성).
- **양성통제/liveness**: `hab_ctx` 자체가 즉시반복에 반응 — 죽었으면 verdict=VOID.
- 통제 ≥2: ① shuffle-반복(통계-matched) ② lag-dose 단조성 ③ alien pedestal.
- **KILL**: 전 lag에서 repeat-Δ = shuffle-Δ TOST 등가.

## $0-first (제한적)
session_seed 앵커가 상수에 가까워 자연반복이 confound → 순수 $0 관측 취약. 사실상 cheap CPU chat run(--percept-schedule) 필요 — pod 아님·저비용.

## 이견/충돌 (reconcile)
- H_9790(sleep store 성장)과 직교(각성·store-sealed).
- Sol: 고유 제안 없음 → Fable P4 채택.
- fire 전 owner go(cheap CPU chat run이나 스케줄 flag 구현 선행). 등록=DIRECTIONAL 설계, verdict 아님.
