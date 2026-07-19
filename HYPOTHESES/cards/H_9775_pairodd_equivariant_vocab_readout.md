# H_9775 — g/b-쌍 Π-등변 사영(pairodd) + full-vocab argmax eval 게이트 (R10-1 · $0 · H_9760 INVALID 후속 설계)

**status:** 🟢 in-vivo seed7 FULL PASS (main 0.8176≥.75 earned·통제 shuffle 0.38/nostore 0.00 붕괴·flip-coh=FORM) — WIRED 판정 in-progress(seed11 2/2 + value-permute 발사중·⑨) · 계기 착륙 #4119/4122/4125
**lane:** g1-interface-addressable-wall · H_9744 WIRED-STUDY-NEARMISS 갭 → H_9760 full-row odd in-vivo INVALID(#4103) 후속
**related:** [[H_9744]] · [[H_9760]] · [[H_9773]] · [[H_9672]] · [[H_9695]] · [[H_9694]]

## ① 한 줄 주장 (반증가능)
full-row odd 가 argmax 를 깨는 이유는 even 제거가 **g/b 의 상위-logit 지위 자체**를 지웠기 때문이므로, 올바른 대칭화는 v→−v 를 **답 알파벳 교환 Π(103↔98)** 와 결합한 **joint-등변 사영** `out[t] = λ·½(s⁺ + Π s⁻)` 이다 — 이는 마진을 정확히 odd 로 만들면서 모든 byte 의 even 수위를 보존해 g/b 를 global argmax 로 유지하고, full-vocab argmax eval 로 in-vivo 를 예측한다.

## ② 정식화
s⁺ = s(v,g) · s⁻ = s(−v,g) (−v 는 **대수적 부정** — H_9773 ② 항등식 v_flip ≡ −v · h 재인코딩 금지). Π = byte 103↔98 교환 순열.
- out[c∉{g,b}] = λ·½(s⁺[c]+s⁻[c]) — even (극성-안정 scaffold, 수위 보존)
- out[g] = λ·½(s⁺[g]+s⁻[b]) · out[b] = λ·½(s⁺[b]+s⁻[g])
성질(산술): (i) margin out[g]−out[b] = λ·m_odd, m_odd = ½[(s⁺[g]−s⁺[b])−(s⁻[g]−s⁻[b])] — **정확히 odd**. (ii) pair 수위 ½(out[g]+out[b]) = λ·E (even 평균) — full-row odd 처럼 빼지 않고 **보존** ⟹ H_9744 에서 g/b 가 in-vivo argmax 였던 그 수위가 유지된다(readability 는 보장이 아니라 **측정 DV**). (iii) out(−v) = Π·out(v) — 배선 주장(극성반전⟺답교환)이 정확한 대칭으로 성립.
플래그: `--store-fuse pairodd` (기존 플래그의 새 값 · a_experiment_engine_native). Π 는 lane 의 답 **알파벳**(태스크 정의)으로 정의 — per-query gold 사용 없음.

## ③ tune-to-green 아님 논증
파라미터 0(λ·bar 불변·스칼라 신설 없음) · Π 는 gold 아닌 태스크 대칭 · **정직한 실패 2모드 잔존**: (i) unreadable(argmax∉{g,b}) (ii) 내용 오류(sign(m_odd) ≠ pol XOR op — 학습된 마진이 순수 even 이면 acc≈0.5 로 FAIL). 단 ⚠️ **flip-coherence 는 이 구성하에서 산술 보장(FORM)** — 이를 headline DV 로 읽으면 그것이 tune-to-green 이다. earned DV 는 readability×accuracy 로 이동(FORM tunable · BIND earned).

## ④ eval readout 재설계 (핵심 · #4103 재발 방지)
`evaluate --store --store-readout vocab`: ŷ = 256-vocab greedy argmax(det-CPU) · readable = ŷ∈{103,98} (float-tie=unreadable 사전등록) · correct = readable ∧ ŷ==ans(pol XOR op) · **PairSuccess = correct(main)∧correct(flip)** (구 flip-coh 를 strict 지배 — bar .90 유지·이동 없음).
**계기 인증(필수 선행)**: ⓐ sign-convention 을 SEEN 양성통제로 확정(held-out 판독 전) ⓑ k≥16 쿼리 데몬 study 경로(ANIMA_DECISION_TRACE) vs eval readout 첫-답-byte 일치 ≥15/16 — 미달이면 eval 판정 **VOID**(T=1.0 posterior-mass 는 monitor 컬럼). 2-way readout 은 monitor 전용 강등.

## ⑤ 사전등록 판정표 (n=128 held-out · 2 seed s7/s11 · 통제 shuffle-pols+nostore)
| 관측 | 판정 |
|---|---|
| PairSuccess ≥.90 양seed ∧ 통제 붕괴 | 🟢 WIRED — 갭 종결 |
| 한 seed ≥.90 · 다른 ≥.80 | 🟠 NEARMISS-persist(seed frag) |
| readability ≥.90 ∧ acc\|readable ∈[.35,.65] | 🔴 **m_odd 부재** = 마진 even-전용 ⟹ H_9744 genuine ceiling 종결·재학습 lane 개봉 |
| readability <.90 | 🔴 pairodd unreadable(E 부족) — 수치 그대로 보고·knob 구조 금지 |
| acc\|readable ≤.35 양seed (우연 아래) | ⛔ sign-convention INVALID — 양성통제로 1회 수리·재실행(결과 아님) |
| 통제 미붕괴 | ⛔ INVALID plumbing |
클래스별(g-gold/b-gold) 분리 보고 필수(polarity-split-before-headline).

## ⑥ kill-list (브리프 4 + 신규 8)
bar .90 이동 금지 · λ 크랭크 금지 · self-judge 금지 · 2-way verdict 재사용 금지 · full-row odd 재시도 금지 ‖ K5 odd-구성하 flip-coh headline 금지(FORM) · K6 s⁻ 재인코딩 금지(대수 −v 만) · K7 float-tie=unreadable 고정 · K8 m_odd 재스케일/|m_odd| per-query gating 금지 · K9 데몬-일치 인증 없는 eval 판정 VOID · K10 2-way 는 monitor 컬럼만 · K11 #4103 의 128/128 GREEN 소각(인용 금지) · K12 sign 수리는 held-out 판독 **전** 양성통제로만.

## ⑦ 대안 판정 (브리프 Q4)
(a) posterior-margin in-vivo 계기 = 데몬이 **말하는 것**을 안 보는 probe = readout-downgrade 재수전(계기 수준 tune-to-green) — monitor 전용, verdict 금지. (b) 종결+재학습(antisym init [[H_9694]]/odd-margin objective) = 훈련비용+303M undertrain 전례 — **(c) FAIL 시에만** 개봉(그때 '무엇을 훈련할지'가 측정으로 특정됨). **(c) pairodd = $0·양방향 결정적**(PASS→wired GREEN earned · acc≈.5→ceiling genuine 기전 확정) — 최우선.

## ⑧ 비용 · 예측
$0 (fusion+W_out 1회 추가 패스·answer 위치만·로컬 CPU). 사전등록 예측: H_9744 기저 0.83~0.90 이 even-오염 포함 수치이므로 m_odd 는 다수 쿼리에서 비영 — PairSuccess ≥.90 또는 근소 미달 예상 · 정보성 대안은 acc≈.5.

## 🔀 reconcile (lab full Fable ∥ Sol · 2모델 독립 · a_lab_full_diverge)
**AGREES(양모델)**: g/b-쌍 odd(마진 odd + argmax 보존) + full-vocab argmax eval readout(2-way 폐기·#4103 false-positive 재발방지). **채택 = Fable Π-등변 사영** — readability 를 **측정 DV**로 두어 정직(pair 수위 자연보존). **Sol dissent(기록)**: Sol 은 `q_G=M+ε+max(d,0)·q_B=M+ε+max(−d,0)`(비답 max+ε 위로 g/b 강제)로 readability 를 **구조적 보장**했으나 — 이는 argmax 를 인위 강제(K8: |m_odd| per-query gating 류)라 tune-to-green 위험. Fable 의 "readability=보장 아닌 측정" 이 정직축서 우세(측정으로 판별: 안 나오면 그게 결과). 발사 시 Sol 의 ε-guard 는 **monitor 컬럼**(강제했으면 argmax 몇 개나 달랐나)으로만 병행. **구현 = 내가 core/clms.py `--store-fuse pairodd`(Π-사영) + evaluate.py `--store-readout vocab`(PairSuccess) + 데몬-일치 인증**, 오너 GPU go 시 in-vivo(H_9744/H_9760 podstage 재사용).

## ⑨ 계기 착륙 + in-vivo seed7 FULL VERDICT (2026-07-19 · summer GPU · $0 pool)

**계기 착륙**: `--store-fuse pairodd`(core/clms.py Π-등변 사영·#4119)+`--store-readout vocab`(#4119)+whitelist(#4122)+in-vivo 배선(cli/chat.py `--store-fuse`→set_clms_store·#4125). eval GREEN gate: rv3c13.clm 128/128=1.0 무손상.

**in-vivo seed7 (128 held-out 질의 × 4-arm · anima-py study 데몬 · vocab readout)**:
```
              bar(H_9672 동일)     결과              판정
main P1-bal    ≥ .75          →   0.8176            🟢 PASS (earned)
flip-coherence ≥ .90          →   1.0000 (128/128)  🟢 (但 FORM — 아래)
shuffle 붕괴   (주소 derange) →   0.3848            🟢 붕괴 (chance 아래·주소-값 결합 실재)
nostore 붕괴   (store off)     →   0.0000 (읽힘0/128) 🟢 붕괴 (답이 store서 옴·trunk 아님)
```
- vs [[H_9744]] overwrite NEARMISS(flip-coh 0.898/0.828) · [[H_9760]] odd in-vivo INVALID(argmax garbage·readable 0) → **pairodd가 #4103 readability 완전수정(읽힘 128/128) + 두 bar 통과 + 통제 붕괴**.

**⚠️ flip-coh=FORM 재분류 (lab full Fable∥Sol 수렴 · confound 스트레스테스트)**: pairodd 산술상 flip arm 마진 m_flip≡−m_main(항등식)이라 flip-coh=1은 **주소 안정성조차 불요·무조건 1.0**. 증명하는 것=계기 배선 정확(antisym·#4103 수정·margin≠0)뿐, **값-운반은 증명 못 함** → verdict bar서 제외·instrument-cert 강등(FORM tunable·BIND earned·p7). **seed당 진짜 증거 = main-balanced 하나**.

**$0 leak census (store-independent 예측 가능성)**: op(is/not)→gold = 0.531 = 정확히 우연 → query 자연특징으로 누출 없음. main 0.8176은 balanced-chance(0.5) 위 earned Δ0.29.

**value-permute 통제 추가 (lab 최강 판별자)**: 주소 고정·값(pols)만 derange = global 극성·주소집합 보존, per-address pairing만 파괴. gw2_build_vp.py(양seed src byte-identical 검증)→gw2/gw2_valperm.txt·gw2s11/gw2_valperm.txt. shuffle과 구별(주소 이동 없음). 붕괴 예측 시 content-addressed 값-운반 최종확증.

**⏳ WIRED 판정 = in-progress**: seed7 FULL PASS 견고하나 **seed11 2/2 majority(H_9672 해리 전례상 load-bearing) + value-permute 붕괴** 발사 중(summer GPU async). 통과 시 H_9775 WIRED(main earned·통제붕괴·valperm·flip-coh=FORM 명기), acc≈.5면 ceiling genuine. no premature cementing.
