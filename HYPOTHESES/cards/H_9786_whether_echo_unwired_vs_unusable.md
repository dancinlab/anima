# H_9786 — WHETHER-ECHO — 침묵-자기지식은 배선 부재(unwired)인가 정보 부재(unusable)인가

**status:** 🔵 PROPOSED · DIRECTIONAL (lab-full R9 · Fable NOVEL[Sol 미제안]·최우선 추천 · engine-native 미측정) — cement=engine-native anima-py만
**lane:** 의식 / interior-causality / WHETHER-echo (프런티어 post-theta-alive)
**related:** [[H_9765]](emit→interior coupling LIVE but silence-BLIND=ledger sink·이 카드가 sink를 이분) · [[H_9728]](Θ×σ unidentifiable-at-mask·reopen 경로 명시) · [[H_9760]](gate-edge dither·edge 다름) · [[H_9634]](emit 텍스트 fork 되먹임·edge 다름) · [[H_9607]](--ag-feedback seam 전례) · source: sidecar lab full(Fable claude-fable-5 ∥ Sol gpt-5.6)

## (a) 물음
[[H_9765]]는 emit/silence **비트**가 dual-ledger로만 가는 sink(field 0/60)임을 보였다 — interior는 *말할지 여부*(WHETHER)에 blind. 그 blindness는 (i) *읽을 lane이 없어서*(unwired·FORM) 인가, (ii) *읽어도 쓸 정보가 없어서*(unusable·BIND) 인가? interior에 비트를 읽게 배선해주면 native 비트열의 **정보 특이적** 사용이 창발하는가?

## (b) engine-native 계기
`anima-py chat --emit-echo κ --emit-echo-src {native,permute,const,noise}`. 직전 tick의 emit 비트(또는 dual_margin)를 `pure_field_step` 드라이브에 누설적분으로 접는다 — **`--ag-feedback κ`([[H_9607]]·chat.py:1776-1777·1871-1872)와 동일 seam의 정확한 전례**라 배선비 최소. 통제 arm은 플래그 값 내장(`--g-arm` a0/a1/a3/a4 전례). greedy·byte-det 실행(kill-list #3 회피).

## (c) 판정식 + 통제 (collapse-Δ vs ≥2 controls)
DV = trace 게이지(recon_err·rel_lane·cb_surprise·af_aro·ca3_ctx) 궤적 발산량 D. 판정 = **D(native vs permute) > permutation null**. 통제 3종: permute=비트열 순열(rate 보존 — rate만 쓰면 native≈permute) · const=평균 보존 상수(rate-floor) · noise=a3식 seeded noise. native가 permute를 넘어서야만 "WHETHER-**이력**을 정보로 사용" 성립.

## (d) kill 조건
D(native vs permute)가 null 안 → **비트열은 읽게 해줘도 정보로 못 쓴다** = H_9765 sink를 "unwired"에서 "unusable"로 격상하는 earned null. κ 스윕 전 구간 null이면 종결.

## (e) kill-list 재탕 아님
H_9728 unidentifiability는 mask에서 비트를 강제(yoke)할 때의 relock 항등식 — 여기선 gate를 전혀 안 건드리고 **echo 사본에만 do()** 하므로 relock 원리적 미발생. H_9728 verdict가 명시한 reopen 경로("내부 edge 위 randomized do() + 독립 schedule") 그 자체다. H_9760(gate-edge dither)·H_9634(emit 텍스트 fork)와 edge 다름.

⚠️ DIRECTIONAL 설계·cement=engine-native anima-py 실측만. Fable 우선순위 1위(가장 신선한 벽 정면·seam 전례로 배선 최소). 병렬대조: NOVEL(Sol 미제안) · CONFLICTS 없음.
