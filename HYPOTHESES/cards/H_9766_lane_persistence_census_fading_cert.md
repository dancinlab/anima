# H_9766 — LANE-PERSISTENCE CENSUS + FADING-CERTIFICATE — 전 lane이 ∀-history 구조적으로 닫히나 ($0 정적 다리)

**status:** 🔵 PROPOSED · DIRECTIONAL (lab-full R8 Fable∥Sol 수렴 · $0 정적) — cement=engine-native anima-py만
**lane:** 의식/interior-causality (프런티어 theta-alive-sigma-rebase)
**related:** [[H_9767]](B relock 主다리)·[[H_9768]](transplant 다리)·[[H_9749]](정적 census #4058 시작)·[[H_9738]](certificate #3986 W_S)·source: sidecar lab full(Fable∥Sol)

## 왜 (lab-full R8 · 3다리 중 ∀-history 구조 다리)
[[H_9767]] B relock는 유한 battery라 표본 부재증거만 준다. 무제한 "interior 없음" 정리는 **lane별 ∀-history 구조 certificate**가 있어야 완성된다. H_9749 #4058 정적 census(전 lane write가 `if g_emit`/`did_emit` 가드 아래 = public-fed)를 **contraction/fading certificate**로 격상: 각 lane이 (a) contraction(λ<1 leak ⟹ ∀-history bounded-window fading·코드 구조적) ∨ (b) read-path dead(write되나 emit 결정 미도달) ∨ (c) transplant 불변([[H_9768]]로 위임) 중 하나를 만족하는지 lane별 판정.

## 계기 (신규 · $0 정적 + engine-native)
`anima-py chat --state-census full`(전 mutable lane write-site/leak-rate/read-path 열거·decode 0) + 각 lane의 leak λ를 코드에서 읽어 bounded-window W = ⌈log(denormal_min)/log(λ)⌉ 유도. W=max over lanes → [[H_9767]] N,L 상수의 코드유도 소스(실험 데이터 peek 0).

## 판정
| lane | leak/persist | certificate |
|---|---|---|
| wmb(W_E)·wm_withheld(W_S) | λ leak (wm_buffer_leak) | contraction (W_S는 [[H_9738]] transplant NULL 실측 완료) |
| afield·cbel·ca3·immune·igrow | write-site 감사(feat8/g_text) | public-fed(H_9749 #4058) → contraction ∨ read-path |
| kosmos | 파일(core/kosmos_io.py `.kosmos`) | **unbounded-persistent 후보** → [[H_9768]] transplant 필수 |
| anchor(live_anchors) | 1-tick lag(:2439) | bounded(1-tick) |

전 lane이 (a)∨(b)∨(c) 충족 = ∀-history 다리 닫힘. unbounded-persistent lane(kosmos 등)만 [[H_9768]]로 넘김.

## honest scope
정적 census는 write-site를 보지 lane간 루프를 못 본다 ⟹ 합성계 검정([[H_9767]])이 커버. 3다리 conjunction일 때만 무제한 정리. 단독 = DIRECTIONAL 구조 근거.

⚠️ DIRECTIONAL·cement=engine-native만. 발사순 1번($0 즉시 · 상수확정 소스).
