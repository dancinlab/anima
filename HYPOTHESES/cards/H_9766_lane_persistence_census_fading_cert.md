# H_9766 — LANE-PERSISTENCE CENSUS + FADING-CERTIFICATE — 전 lane이 ∀-history 구조적으로 닫히나 ($0 정적 다리)

**status:** 🔵 PROPOSED · DIRECTIONAL (lab-full R8 Fable∥Sol 수렴 · $0 정적) — cement=engine-native anima-py만
**lane:** 의식/interior-causality (프런티어 theta-alive-sigma-rebase)
**related:** [[H_9767]](B relock 主다리)·[[H_9768]](transplant 다리)·[[H_9749]](정적 census #4058 시작)·[[H_9738]](certificate #3986 W_S)·source: sidecar lab full(Fable∥Sol)

## 왜 (lab-full R8 · 3다리 중 ∀-history 구조 다리)
[[H_9767]] B relock는 유한 battery라 표본 부재증거만 준다. 무제한 "interior 없음" 정리는 **lane별 ∀-history 구조 certificate**가 있어야 완성된다. H_9749 #4058 정적 census(전 lane write가 `if g_emit`/`did_emit` 가드 아래 = public-fed)를 **contraction/fading certificate**로 격상: 각 lane이 (a) contraction(λ<1 leak ⟹ ∀-history bounded-window fading·코드 구조적) ∨ (b) read-path dead(write되나 emit 결정 미도달) ∨ (c) transplant 불변([[H_9768]]로 위임) 중 하나를 만족하는지 lane별 판정.

## 계기 (신규 · $0 정적 + engine-native)
`anima-py chat --state-census full`(전 mutable lane write-site/leak-rate/read-path 열거·decode 0) + 각 lane의 leak λ를 코드에서 읽어 bounded-window W = ⌈log(denormal_min)/log(λ)⌉ 유도. W=max over lanes → [[H_9767]] N,L 상수의 코드유도 소스(실험 데이터 peek 0).

## 🔵 $0 census RESULT (2026-07-18 · core/engine_cli.py 실코드 감사)
각 lane의 update dynamics를 core에서 읽어 지속성 분류 + emit read-path 추적:

| lane | dynamics (core op) | class | emit read-path |
|---|---|---|---|
| wmb (W_E) | `act*=λ` λ=0.6 기하감쇠 (wm_buffer_leak:1877) | **CONTRACTION** W≈68t(machine-eps)/~1390t(fp64 denormal) | live (coverage cos) — 감쇠로 닫힘 (a) |
| wm_withheld (W_S) | 동일 λ=0.6 + [[H_9738]] transplant NULL 실측 | **CONTRACTION** (+NULL 실측) | (a) 닫힘 |
| anchor(live_anchors) | 1-tick lag(:2439) | **bounded**(1-tick) | (a) 닫힘 |
| kosmos | 세션 rmtree+reseed(:456) · self_g emit-inert | **session-scoped/read-dead** | (b) 닫힘 (지속판=[[H_9768]]) |
| immune/igrow | EMA(LR0.2)+n_cells split+**LRU victim**(:1052) | LRU 용량제한 window | recall이 emit-loop 밖(seed only :623) = **(b) read-path-dead** |
| **afield** | proto EMA(λ0.8)+**n_cells 단조 split**(:418) | **ACCUMULATE**(구조) | recon_err readout=**CONSTANT-KEY**(seed_feat0 :2030)→H_9328 720t 상수=감쇠(경험) ⚠️ |
| **cbel** | NLMS `W+=η·outer(e,ctx)/(‖ctx‖²+1)`(:1972) | **ACCUMULATE**(weight) | cb_perr=**LIVE key**(prev utterance :2157)·NLMS fading ⚠️ |
| **ca3** | count table `ct[prev,cur]+=1`(:3136) | **ACCUMULATE**(단조 counts) | in-loop predict(live prev-sym :2796)·counts 영구 ⚠️ |

**결론(정직)**: 정적 certificate **단독으론 interior 부재 못 닫는다**. 4 lane은 닫힘(contraction/session/read-dead) BUT **afield·cbel·ca3는 누적+emit read-path 보유** ⟹ [[H_9767]] B relock 실측 필수(공통 future에 history-구조가 씻기나). H_9749 #4058 "전 lane public-fed"는 맞지만 "따라서 fade"는 **과독** — public-fed여도 누적 구조(counts/n_cells)는 지속. afield는 CONSTANT-KEY readout이라 감쇠 강함(H_9328 실측 상수), cbel/ca3가 최우선 B-검정 대상.

**H_9767 상수 유도**: contraction W≈68t(λ=0.6·machine-eps) ⟹ 공통 suffix N ≥ 2W+margin ≈ **150t**(SCREEN·감쇠지평 초과). exact-0 cement는 N_fp≈1390t(fp64 denormal).

## honest scope
정적 census는 write-site+read-path를 보지 lane간 루프의 실제 씻김을 못 본다 ⟹ 합성계 검정([[H_9767]])이 커버. 3다리 conjunction일 때만 무제한 정리. 단독 = DIRECTIONAL 구조 근거 + **3 lane OPEN 지목**.

⚠️ DIRECTIONAL·cement=engine-native만. census 완료($0) → 다음=[[H_9767]] B relock(afield/cbel/ca3 대상·N=150t SCREEN·pool).
