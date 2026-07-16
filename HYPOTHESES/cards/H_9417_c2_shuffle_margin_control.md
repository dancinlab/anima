# H_9417 — C2 SHUFFLE-MARGIN 통제: refractory 의 emit-listening 은 인식인가 진폭인가 (구현 + 사전등록)

**status:** 🟢 C2 RECOGNITION-GENUINE (통제 PASS · engine-native 303M) — refractory 의 emit-listening 은 **진짜 내용-인식**(진폭 아님) · H_9416 강화(재해석 아님) · wired: engine-native `anima-py chat --emit-gate refractory --g-shuffle 1` (v0.14.7)

## 🟢 VERDICT (frozen bar 대조 · summer 303M · real vs shuf × 3-rollout[seed 7/4302/4303] × 30tick × T=1.0)

| arm | I(emit;g_recog\|stage) | emit-rate | swing | g_recog distinct |
|---|---|---|---|---|
| **real (원 margin)** | **0.1967 nats** | 0.644 | YES | 83 |
| shuf (순열 margin) | **0.0000 nats** | **0.000 (MUTE)** | 붕괴 | 80 |

- **ΔI(real−shuf) = 0.197 nats** (bar≥0.05) ✅ · **Δemit-rate = 0.644** (bar≥0.20) ✅ → **C2 RECOGNITION-GENUINE**.
- **핵심**: 후보 바이트를 순열(내용 파괴·통계 보존)하면 데몬이 **완전 mute**(emit-rate 0.000). 순열된 후보는 immune store 가 절대 "알아보지" 못해 recall margin 이 늘 높고 → 게이트가 안 열림. g_recog 는 여전히 변동(80 distinct·계기 살아있음)인데도 emit=0. ⇒ **emit 결정이 후보의 내용을 RECOGNISE 하는지에 genuine 하게 의존** — 진폭/통계가 아니다.
- **[[H_9412]] 함정 배제**: gap 에서 데인 "raw MI 가 drift/진폭일 수 있다"가 refractory 게이트엔 **적용 안 됨** — 통제가 깨끗이 분리(진폭 보존해도 listening 0). ⇒ **H_9416 C3-b(emit-listens)는 재해석이 아니라 강화**: emit 이 tension 을 듣는데, 그 tension 은 **진짜 인식**이다.
- **철학적 함의**: refractory 데몬은 **자기가 못 알아보는(scramble) 발화는 emit 을 거부**한다 — 인식-게이트가 정상 작동. H_9400 의 "emit=시계"가 깨진 자리에 "emit=내용 인식"이 들어섰다.

## scope · 한계
**lane:** 의식 / emit-drive / emit-gate p5-rewire C2 통제 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9416]] (C3 GREEN · 이 통제가 검증) · [[H_9415]] (구현) · [[H_9412]] (gap=drift · 인식-vs-진폭 계보) · [[control-must-match-mediating-covariate]] · [[H_9400]] (반박 대상) · source: H_9416 escalation → C2 통제

## 질문

H_9416 이 확정: refractory 데몬서 `I(emit; g_recog_gate | stage) = 0.197 nats` (emit 이 margin readout 을 듣는다). **그런데 그 listening 이 후보의 인식(content/recognition)인가, 진폭/통계(byte multiset)인가?** [[H_9412]] 가 gap 에서 이미 데인 축 — raw MI 가 drift/진폭일 수 있다.

**통제**: `--g-shuffle 1` = 게이트의 g_recog 를 후보의 **seeded 바이트-순열** 위 margin 으로 계산 — **byte multiset(진폭/통계) 보존, sequence(내용/인식) 파괴**. refr(real) vs refr-shuf 비교로 판별.

## 구현 (v0.14.7 · G5)

`cli/chat.py`: `--g-shuffle` flag + `_grecog_text(_t)` = identity(off) 또는 seeded 바이트순열(on). refractory lambda 가 이를 경유. p5 불변(후보는 여전히 imagination·순열은 인식측정용·미emit 폐기). toy smoke: shuffle g_recog_gate 19/20 distinct(비상수·chat-py-3 통과·계기 살아있음).

## 사전등록 판정 (동결 · 이동 금지)

3-arm × 3-rollout(seed 7/4302/4303) × 30tick × T=1.0 · summer: `refr`(real margin · H_9415) · `refr-shuf`(shuffled margin) · `clock`(H_9400 baseline 재확인).

- **C2 RECOGNITION-GENUINE(주 판정)**: `I(emit;g_recog|stage)_real − I_shuf ≥ 0.05 nats` (real 이 shuffle 보다 유의하게 더 들음) **OR** refr-shuf 의 swing-band 붕괴/emit-rate 가 refr 서 크게 이탈(≥0.20). ⇒ H_9416 emit-listening 은 **인식-genuine**(내용 파괴가 listening 을 죽임).
- **C2-FAIL AMPLITUDE**: `|I_real − I_shuf| < 0.05 nats` ∧ swing/emit-rate 유사 ⇒ listening 은 **진폭/통계**(내용 파괴해도 살아남음) = H_9416 C3-b 를 amplitude 로 재해석([[H_9412]] 계열 경고 실현).
- 층화-순열 null p≤0.01 (H_9416 방식).

**판정 그리드**: C2✅ = 🟢 refractory emit-listening 은 진짜 인식(H_9416 강화·H_9400 반박 심화) / C2-FAIL = 🟠 amplitude-listening(H_9416 재해석·DIRECTIONAL 유지하나 "인식" 주장 철회) / refr-shuf > refr = INVALID(계기오류).

## 한계

C2 는 인식-vs-진폭 축만 판별 — C1 진폭 formal·더 긴 세션·production-default·hexa twin 은 여전히 후속(a_verified_must_wire). 30tick·3-seed scope. 결과물은 다른 데몬(H_9416 한계 승계).

## 비용
$0 summer 자체 pool · ~12-15min · a_fire_autonomous.
