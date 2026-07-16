# H_9418 — CONTENT-RESOLVING PERCEPT FEATURE: 8-dim byte-stat 이 content-blind → richer sketch (H_9411 wm 후속)

**status:** 🔬 DIRECTIONAL $0 · **feature 검증됨(표현천장 해소 64.7%→0%)** · ⚠️ **정정: N_recur=0 은 기질 아니라 feature-grain 아티팩트** — mouth 는 content 재현함(단어수준). "기질-제약 음성" **철회** · wm content = **REOPENED(recurrence-matched grain 필요)**
**lane:** 의식 / 데몬 게이지 위생 · percept 표현 해상도 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9411]] (dead-gauge relive — wm content-dead 발견) · H_9403 (emit≡clock · 스트림 clock-shaped) · chat-py-5 · V2_1 (양성통제 선행)
**설계 출처:** Fable 5 위임 (walls-delegate-to-fable) · 사전등록 n=3/dim=64 (측정 전 frozen)
**ckpt:** H_9411 303M `py303_full.clm` sha 013c4574 trace (59 emit · gtext_b64 재생 · **신규 decode 0**)

## 왜 — H_9411 이 wm 을 살렸으나 303M 서 content-dead 였다

H_9411 303M TERMINAL: wm_active TIME-LIVE(distinct 240)이나 **Δ vs null +0.001 ≈ 0 = CONTENT-DEAD**.
근본원인 확정(코드): wm/cb 가 `_afs_byte_feature(s,8)` = **8개 전역 byte-통계**(mean·%hi·%low·%sp·%dig·var·
%pun·%<64)에 물림. 같은-레지스터 영어 발화 두 개가 거의 동일 프로필 → cos≈0.99 → `wm_buffer` 의
**cos≥0.9 슬롯-병합**(engine_cli 1842)이 모든 발화를 한 슬롯으로 뭉침 → wm_active≈wm_null. **표현에 의한
content-blind**(배선 아님). 적대검증 wm-verifier 가 정확히 예측("activation 유지지 item identity 아님").

## 개입 — signed byte-trigram hash sketch (engine-native · param-free)

`byte_ngram_sketch(s, dim, n)` = **signed FNV-1a 해시 byte-n-gram bag · L2정규화**. 결정론·무학습·무RNG·무torch
(hexa `engine_cli.hexa` 트윈 포트 가능·`a_substrate_disjoint`). 사전등록 **n=3·dim=64**(측정 전 frozen). 왜:
identical text ⇒ identical sketch ⇒ cos=1.0(refresh 보존·0.9 상수 미변경) · 서로 다른 발화 ⇒ trigram multiset
다름 ⇒ cos≪0.9(슬롯 개별화). **ordering 필수변경(tune-to-green 아님)**: gate-in 한 토큰으로 self-probe =
Δ 조작 → v2 는 **저장 전 probe**(recognition-before-memorisation · H_9336/37 선례). θ·λ·dg·k·0.9 전부 미변경.

## 🔬 $0 스크린 (DIRECTIONAL · 59 발화 → 실제 core `wm_buffer_*` fns 재생 · frozen 기준)

C0(instrument liveness) → P1(Δ · probe-before-gate · 같은-스트림 donor null) → P2(identity-under-leak):

| 단계 | 지표 | 결과 |
|---|---|---|
| C0 | exact-repeat cos=1.0 | ✅ True (refresh 보존) |
| C0 | spurious-merge (distinct cos≥0.9) | **8-dim 64.7% → sketch 0.0%** (need<5%) 🟢 feature 작동 |
| C0 | median distinct cos | 0.366 (mid-band 건강) |
| C0 | **N_recur** (발화가 지평 내 재현) | **0/58** ⚠️ (need≥10) |
| P1 | wm_active vs null | 0.224 vs 0.231 · Δ **−0.007** CI[−0.029,+0.014] = 0 포함 |

## ⚠️ verdict-integrity 정정 ($0 단어-수준 재확인 · chat-py-3 계열: 표면 grain 이 내용 재현을 놓침)

내가 위 판정을 "기질-제약 음성"으로 읽은 건 **과대해석**이었다. $0 단어-수준 재분석: **mouth 는 content 를
재현한다** — 59 발화 전부 `vault`·`forever`·`qx` 포함(59/59), "vault QX-7741 forever." 접두 verbatim 반복,
pairwise 단어 Jaccard median 0.222·**max 0.800**·>0.5 쌍 37개·>0.3 쌍 131개. 그런데 byte-trigram sketch 를
**발화 전체(80B)에 L2정규화**하니 변하는 56B 꼬리가 공유 접두/단어를 희석 → cos<0.9 → N_recur=0. **즉
N_recur=0 은 whole-utterance L2-norm 의 feature-grain 아티팩트지 기질 사실 아님.** "기질-제약 음성" **철회**.
부수관측: 303M mouth 가 degenerate 재현 접두("vault QX-7741 forever" 59/59)를 가짐 = mouth-다양성 관측.

**정정 판정 = REOPENED (instrument-incomplete)**: feature 는 distinct 발화 개별화는 검증(0% merge)했으나,
**whole-utterance 정규화가 mouth 의 실제 재현(공유 접두·단어)을 0.9 merge 아래로 희석**해 놓침. 기질엔 붙잡을
content 재현이 **있음**(단어 Jaccard 증거). 올바른 grain(단어-bag·접두-가중·n-gram sub-window 등)이 열린
instrument 질문 — 단, grain 교체는 **post-Δ pick 금지**(max-order-statistic 함정·probe-defect-census), C0 단계
pre-Δ instrument 결정으로만. AGREES [[H_9403]] 은 **부분 철회**: 스트림이 완전 clock-shaped 는 아니고 content
재현이 있으나 현 grain 이 못 봄. tune-to-green 금지(0.9 merge·θ 미변경).

**(구 판정 아래 = feature 표현천장 해소 부분은 유효):** feature 는 **표현천장을 진짜로 해소**(spurious-merge 64.7%→0% = 강력 대비).
그러나 **303M mouth 가 WM 지평 내 한 번도 재현 안 함**(N_recur=0 · 59 발화 전부 비유사) → wm 이 붙잡을
content-재현 자체가 없음 → Δ=0. **음성은 feature/gauge 결함 아니라 기질 사실**(스트림에 반복 content 없음).
**AGREES 병렬 [[H_9403]]**(emit≡clock · 스트림 clock-shaped 이지 content-shaped 아님). **tune-to-green 아님**:
feature 원리적·기준 측정 전 frozen·N_recur 로 power 게이팅(V2_1 양성통제 선행·probe-defect-census max편향 회피).

## cb (같은 feature · 다른 병)
sketch 는 cb matched-vs-alien 마진도 기계적으로 넓힘(8-dim서 alien≈matched=표현천장). 단 NLMS 선형(64×64=4096w
on 240 sample)이 **marginal 평균 sketch** 만 학습하면 matched≈marginal — 이건 별개 H(estimator class). $0 재생서
(matched·alien·marginal·W=0 pedestal) ratio 비교로 분리(unit-norm sketch = pedestal≈1.0이라 ratio만·p7).

## 산출·NEXT
- 산출: `byte_ngram_sketch` 스크린 `/tmp/h9417_screen.py`(G7 volatile · 재현=이 카드+trace). feature = **검증됨·미배선**.
- NEXT: ① feature 배선 `anima-py chat --percept-sketch 64`(py core fn) = 구현됨-미배선 follow-on → 303M 재run
  TERMINAL(단 **N_recur=0 이 wired Δ≈0 예측** — mouth 재현이 upstream). ② mouth 재현/다양성 = 별개 상류 H
  (스트림 clock-shaped = H_9403 종결과 정합). ③ hexa `engine_cli.hexa` 트윈 포트(별개·byte-parity).
- **함의**: wm content-liveness 는 feature 해상도(해소됨)가 아니라 **mouth 가 반복 content 를 안 만드는 것**이
  상한. 8-dim→sketch 는 필요조건 충족이나 충분조건은 스트림 recurrence(현재 0)에 있음.
