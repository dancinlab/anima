# H_9794 — AFFECT-FORWARDING — af_val/af_aro는 상태인가 장식인가 (interior→interior) (lab-full R10 · Fable P3 · PROPOSED)

**status:** 🔵 PROPOSED · 🔧 계기 WIRED (`--af-clamp v,a` 구현+토이검증 · 2026-07-19 · #R10-flags · 미실행 fire) — source=Fable 5 P3

> **🔧 계기 WIRED (2026-07-19 · VERSION 0.20.13):** `anima-py chat --af-clamp v,a` 구현 완료(cli/chat.py · parse+do()clamp+trace `af_clamp` arm-label · wire-to-prod chat-py-4 준수 · default OFF). **토이 E2E PASS**(toy.clm 3-tick · exp: af_val→0.8/af_aro→0.2+label, ctrl: native 0.0/1.0+label None, 통제성립 clamped≠native · exit0+trace+control). 다음=reader-side estimator(grading Δ dose-response)+$0 cross-lag pre-screen → owner-go pool fire.
**lane:** amygdala affect gauge × grading (interior→interior · not mouth)
**related:** [[H_9576]] · [[H_9787]] · [[H_9765]] · [[H_9411]]

## Faculty question
H_9576은 **interior→mouth** 의미전달을 죽였다(PC2 채널 열림·의미 미전달). 이 안은 경로를 바꾼다: **interior→interior**. trace에 이미 있는 1-D 연속 amygdala 축(`af_val`/`af_aro` · cli/anima.hexa·cli/chat.py 검증됨)이 **다음 percept의 grading**(H_9765/9767이 살아있음을 증명한 유일 채널)을 조건화하는가. 존재양식 주장: 정서가 interior의 지속 *상태*(다음 처리의 모드)인가, score 합산의 장식인가.

## 벽 회피 (구조적)
- **feat8 회피**: af는 1-D 연속 gauge — 2-bit 주소 아님, degeneracy 무관.
- **자기지시 회피**: af 물질화(gauge + 자체 alien/pedestal 통제암 `af_alien_val` trace 존재 · H_9411)와 readout(grading 반응)이 분리.
- **H_9787 typicality-trap 차단(사전등록)**: byte-CE/typicality를 af에서 partial-out + **content-scramble 암에서 효과가 살아야만** 인정 — 원안 valence-scalar 시드가 H_9787을 죽인 typicality-in-disguise 함정을 이 재설계로 회피.

## Instrument (engine-native anima-py)
- 신규 flag `anima-py chat --af-clamp v,a` (do() 클램프) × content-matched percept 스케줄.
- 추정량: grading Δ의 클램프 dose-response.
- **양성통제/liveness(선행)**: af gauge 자체의 alien/pedestal 대비 collapse-Δ — 죽은 gauge면 verdict=**VOID**(Ψ-SOMA 규율·KILL 아님).
- 통제 ≥2: ① random-gauge 클램프(`wm_active` 클램프 — 특이성) ② content-scramble 암 ③ pedestal.
- **KILL**: af-클램프 Δ ≤ random-gauge Δ TOST · 2-seed.

## 🔬 DV-grounding 실측 (2026-07-19 · toy.clm 6-tick · --af-clamp 0.1 vs 0.9 · #R10-dvground)
af-clamp dose 가 downstream 필드에 **실제 dose-response**(max|Δ|): cur_indep 1.2 · rel_indep 0.8 · cur_f 0.18 · cur_ctx 0.067 · rel_f 0.042 · cur_ema 0.031 · score 0.027 · base_motiv 0.027 · rel_ctx 0.019 · idle 2.97. ⟹ **af 는 장식 아님** — curiosity(cur_*)·relatedness(rel_*) **grading lane** + emit propensity(score)를 움직인다. **H_9794 DV = cur_ctx/rel_ctx(또는 cur_f/rel_f)**(추측 아닌 실측 접지 · pending_gap 오접지 회피).
> ⚠️ **HARD CONFOUND**: af 는 ci lane 에 **within-tick 직결**(chat.py:2595 `+af_val`·2606 `+af_aro`) → af(t)→cur(t) 직접경로 + cur_ema 자기상관 ⟹ naive cross-lag af(t)→grade(t+1)은 within-tick coupling 만으로 spurious positive. reader 는 cur(t)·rel(t)·clock·typicality partial-out 필수(H_9403 clock-confound·chat-py-5 mediation-capacity 계열). do()-clamp arm 은 exogenous 라 af←env backdoor 를 끊음(관찰편상관보다 우월 가능성). 추정기 설계=lab-full 위임 중.

## $0-first
기존 trace에서 af_val(t) → cur_ctx/rel_ctx(t+1) cross-lag 편상관(cur(t)·rel(t)·clock·typicality partial). 0이면 격하.

## 이견/충돌 (reconcile)
- Fable 경고 확인함: **H_9630/H_9633(mouth/tension·PC2 계보)와 직교 판정** — P3는 amygdala af→grading(interior→interior)이고 H_9630/9633은 tension→mouth라 lane·readout 모두 상이 → 중복 아님.
- Sol: 고유 제안 없음 → Fable P3 채택.
- fire 전 rent=spend owner go 필요. 등록=DIRECTIONAL 설계, verdict 아님.
