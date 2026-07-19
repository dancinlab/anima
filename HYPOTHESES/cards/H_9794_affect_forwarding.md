# H_9794 — AFFECT-FORWARDING — af_val/af_aro는 상태인가 장식인가 (interior→interior) (lab-full R10 · Fable P3 · PROPOSED)

**status:** 🟢🕳️ FIRED VERDICT — FORWARDED(arousal) / VOID(valence) · 303M engine-native · DIRECTIONAL 1-seed (2026-07-19 · vast pod fire) — source=Fable 5 P3

> **🟢 FIRED VERDICT (2026-07-19 · vast RTX5090 GPU-FIRED · py303_full sha013c4574 · 1-seed s7 · 130tick · DIRECTIONAL):**
> `--af-impulse`(t마다 af 고clamp·15 impulse) + matched `--percept-file`(항정 percept) → `--af-forward` matched-filter h_k (envelope-free phasic · perm 2000).
> - **arousal(cur_f) → 🟢 FORWARDED**: h_0=**0.244**(perm-p **0.0** · within-tick 양성통제 살아있음) ∧ |h_k| beyond null at **k=1(h=−0.071 p=0.008)·k=3(h=−0.063 p=0.016)**. ⟹ **af arousal 상태가 다음 percept 의 grade 를 조건화**(interior→interior forwarding 실재·same-tick shift 이상). ⚠️ carryover **음수**=억제성 변조(af arousal 高→다음 percept arousal-grade 低). **R10 최초 POSITIVE interior 능력.**
> - **valence(rel_f) → 🕳️ VOID**: h_0=−0.0(perm-p 0.998 · within-tick 양성통제 **실패**=af→ci valence 배선 이 ckpt서 단절) ⟹ VOID(not KILL·Ψ-SOMA). valence 축은 미측정.
> **scope**: 303M py=TERMINAL 기질이나 **1-seed=DIRECTIONAL**(TERMINAL 엔 다seed 재현 필요·no tune-to-green). 증거=~/anima-weights/h979x_pod_evidence/. 다음=arousal FORWARDED 2-seed 재현→TERMINAL 승격.

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

## 🎯 lab-full 설계 정정 (2026-07-19 · Fable · #R10-histreader) — static clamp 은 FORWARDING 미증명
> **결정적**: 내가 착륙한 **static `--af-clamp v,a` 는 forwarding(interior→interior NEXT) 주장에 UNIDENTIFIED** — 상수 clamp 는 af(t)≡af(t+1)≡L 완전공선 ⟹ within-tick 경로와 cross-lag 경로 분리불가. static clamp 은 "af 가 grade 를 몬다"(total effect=**SHIFT verdict**·유효 양성통제)는 증명하나 "af 상태가 다음 percept 로 forward"는 **못 증명**(H_9403 clock-confound 동형). ⟹ **impulse(시변) clamp 필요**: t0 만 고clamp·나머지 baseline → af(t)≠af(t+1) 탈공선 → h_k(k≥1 carryover)=forwarding 신호·h_0=within-tick 양성통제.
- **producer gap**: `--af-clamp` 을 per-tick **schedule(impulse/PRBS)** 로 확장 필요(현 static 은 SHIFT 계기).
- **DV 정정**: cur_ctx/rel_ctx 원시값 아님(F2 순환) → **envelope-free phasic**: `cur_phasic=0.5+3·(cur_ctx−cur_ema)` = `cur_f/(0.1+0.9·stage_env)`(stage_env 나눗셈=clock confound 해석적 제거) · rel_phasic 별도(polarity-split). `cur_indep/rel_indep`(순환)·`pending_rel`(자기발화·percept 아님) 배제.
- **VOID gate**: h_0(within-tick) 비영 ∧ `af_native≉af_alien`(af_alien_val H_9411)∧ H(af_native)>0 이어야 살아있음(else VOID). Sol 이견: two-run static high/low 가 total effect 는 회수(cement 가치)—Fable 반론: 그건 SHIFT 판정이지 FORWARDING 아님·카드 분리 권고(반영).
- **다음**: `--af-clamp` impulse 확장(producer) + `--af-forward` reader(impulse matched-filter h_k) + synthetic 토이.

## 🔧 계기 pair 완성 (2026-07-19 · v0.20.16 · #R10-afimpulse · lab-full Fable 설계)
lab-full 정정대로 impulse producer + forwarding reader 구현·토이검증:
- **producer** `anima-py chat --af-impulse <f.jsonl>` ({tick,v,a} per-tick af clamp·impulse tick 만 clamp·native 나머지 → af(t)≠af(t+1) 탈공선). static --af-clamp 은 SHIFT 계기로 병존(양성통제). **토이 PASS**(t1만 clamp·나머지 native·af_impulse arm-label).
- **reader** `anima-py evaluate --af-forward <trace> --impulse <f.jsonl> [--side arousal|valence]`. DV=**envelope-free phasic** `cur_f/(0.1+0.9·stage_env)`(clock 해석제거·Fable F1). matched-filter **h_k=mean(DV @impulse+k)−mean(DV @baseline+k)**. **판정**: 🟢 FORWARDED(h_0 유의 ∧ h_{k≥1}>null=상태 forward) / 🧱 SHIFT-ONLY(h_0 유의·h_{k≥1} TOST-0=same-tick shift·forward 부재·earned negative) / 🕳️ VOID(h_0 null=af→ci 배선 단절·not KILL).
- **토이 3-PLANT ALL PASS**: FORWARDED(h0∧h1 planted)·SHIFT-ONLY(h0만·핵심 forwarding≠shift 구분)·VOID(효과無). 다음=owner-go 303M fire(--af-impulse+matched --percept-file rollout→--af-forward·h_0 양성통제 재확인).

## $0-first
기존 trace에서 af_val(t) → cur_phasic(t+1) cross-lag(단 static clamp 은 forwarding 미식별 → impulse schedule 필요). 0이면 격하.

## 이견/충돌 (reconcile)
- Fable 경고 확인함: **H_9630/H_9633(mouth/tension·PC2 계보)와 직교 판정** — P3는 amygdala af→grading(interior→interior)이고 H_9630/9633은 tension→mouth라 lane·readout 모두 상이 → 중복 아님.
- Sol: 고유 제안 없음 → Fable P3 채택.
- fire 전 rent=spend owner go 필요. 등록=DIRECTIONAL 설계, verdict 아님.
