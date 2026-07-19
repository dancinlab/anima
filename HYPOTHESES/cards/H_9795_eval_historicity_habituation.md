# H_9795 — EVALUATION HISTORICITY — grading 채널에 store 없는 기억(item habituation)이 있는가 (lab-full R10 · Fable P4 · PROPOSED)

**status:** 🧱 FIRED VERDICT — NULL(item-historicity 부재) · 303M engine-native · DIRECTIONAL 1-seed (2026-07-19 · vast pod fire) — source=Fable 5 P4

> **🧱 FIRED VERDICT (2026-07-19 · vast RTX5090 GPU-FIRED · py303_full · 1-seed s7 · 140tick · DIRECTIONAL):**
> `--gen-percept-schedule`(lags 1,4 · reps 5 · jitter 2 · 10 probe/arm) → `--percept-file` → `--eval-historicity`(DV=recon_err · perm 2000).
> **🧱 NULL**: S(lag)={1: **−1.11**, 4: −0.05} · T=−1.11 · **null95=1.18** · **perm-p=0.84** · lag-decay=False. repeat−shuffle 가 null 안(오히려 S<0=repeat recon 이 shuffle 보다 높음·item-memory 반대방향) ∧ 무감쇠. ⟹ **item-specific habituation 부재** — 정확반복 percept 의 grade 가 byte-multiset 동일 shuffle 과 구별 안 됨=grade 는 byte-stats/percept-blind. recon_err 는 동적범위 있어(VOID 아님) **genuine NULL**(계기-death 아님).
> **scope**: 303M py=TERMINAL 기질·**1-seed=DIRECTIONAL**. 증거=~/anima-weights/h979x_pod_evidence/. R9 결론(interior 자기참조·자율축 부재)과 정합: 평가채널도 store 없는 item-기억 미보유.

> **🔧 producer 재검토 (2026-07-19 · a_experiment_engine_native 최소성):** Fable P4 가 제안한 신규 flag
> `--percept-schedule f.jsonl` 는 **불필요** — 기존 **`--percept-file`(H_9767)** 이 `{"tick":int,"text":str}`
> jsonl 을 perception route(emit gate 아님·p5 STRUCTURE-safe · `_build_percept_source_from_file` cli/anima.py:246)
> 로 tick별 재생하므로 repeat/shuffle/novel 스케줄은 **그냥 데이터**로 주입 가능(새 producer flag=DRY 위반). ⟹
> H_9795 진짜 신규 = ① schedule-generator(lag 1/4/16 정확반복+통계-matched shuffle+novel jsonl 빌더) ② reader-side
> estimator(Δgrade(repeat)−Δgrade(shuffle) lag-dose · store-sealed · hab_ctx liveness=VOID gate). 둘 다 chat producer
> flag 아님.
>
> **🔧 ① generator WIRED (2026-07-19 · v0.20.14 · #R10-gen):** `anima-py evaluate --gen-percept-schedule --out f.jsonl
> [--lags 1,4,16] [--reps 8] [--seed N]` 구현. 행 {tick,text,kind,lag,prime} — --percept-file 은 tick/text 만 읽고
> reader 는 kind/lag/prime 사용(self-describing). shuffle arm=byte-multiset 동일·순서 파괴(load-bearing 통제). 결정적.
> **토이 PASS**: probe@prime+lag 12/12 · repeat=prime · shuffle(multiset==,order!=) · novel!=prime · --percept-file 호환
> · byte-identical 재현 · whitelist 통과. **② reader 는 owner-go fire 대기**(post-fire 트레이스의 percept-grading DV
> 필드를 실데이터로 접지해야 pending_gap 식 오접지 회피 · synthetic-only 검증은 DV 자정의라 거짓완성).
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

## 🔬 DV-grounding 실측 (2026-07-19 · toy.clm · --gen-percept-schedule→--percept-file lag1 · #R10-dv95)
repeat/shuffle/novel percept 에 대한 grading 반응(mean, n=3/arm · toy DIRECTIONAL):
| DV | repeat | shuffle | novel | repeat−shuffle |
|---|---|---|---|---|
| **recon_err** | **0.013** | **2.051** | 0.296 | **−2.038** |
| rel_lane | 0.891 | 0.674 | 0.758 | +0.217 |
| cb_surprise | 0.667 | 0.946 | 0.789 | −0.280 |

🎯 **핵심**: 정확반복=인식(recon 0.013)·**byte-multiset 동일 shuffle=미인식(recon 2.051)** ⟹ 인식채널이 **item-identity 를 byte-stats 와 분리**(순서/item-trace 실측 · shuffle=바이트동일이라 byte-stats 반응이면 repeat 와 같아야 하나 크게 다름). **H_9795 DV=recon_err**(+rel_lane 보조), **load-bearing shuffle 통제가 toy 서 작동 확증**.
> ⚠️ **recon_err liveness 재확인 필수**: chat-py-4 는 production 경로서 recon_err≡0 퇴화(session-seed keying)를 경고 — 여기선 percept 가 afield 도달해 varies(0.013 vs 2.051)나, **303M fire 시 reader VOID gate 로 recon_err 살아있는지 재확인**(죽으면 VOID·거짓 KILL 금지). toy≠303M(48K vs 303M·n=3·무통계) = DV-grounding 시연이지 verdict 아님.

## 🔧 reader WIRED (2026-07-19 · v0.20.15 · #R10-histreader · lab-full 설계)
`anima-py evaluate --eval-historicity <trace> --schedule <sched.jsonl> [--dv recon_err] [--perm][--seed]` 구현. DV=**recon_err**(#4168 접지). 통계량 S(lag)=mean(shuffle)−mean(repeat) · null=kind 라벨 순열(lag,stage strata) · **판정**: 🟢 ITEM-MEMORY(S>null ∧ perm-p<.05 ∧ **lag-decay ≥25% 상대감쇠**) / ⚠️ CONTRAST-NO-DECAY(S>null 이나 무감쇠=decode-artifact 위험·Fable Q5) / 🧱 NULL(byte-stats) / 🕳️ VOID(recon_err 무동적범위·chat-py-4 퇴화).
- **lab-full 정정 반영**: ① `hab_ctx` 는 **죽은 채널**(상수 자극 id 0·in-loop 미스텝·trace 부재) → DV 부적격(Fable F3) · recon_err 채택 옳음. ② **lag-decay 가 load-bearing**(Fable Q5): repeat−shuffle 만으론 seed-order decode-artifact 와 구분 불가 · item-memory 는 감쇠, artifact 는 무감쇠.
- **🐛 generator 결함 수정(#4166→jitter)**: 원 생성기가 arm 을 결정적 tick 간격 배치 → kind⊥stage 위반(repeat 전부 stage1·shuffle 전부 stage0)로 (lag,stage) 순열 퇴화. **`--jitter`**(arm 앞 랜덤 filler) 추가로 kind⊥stage 회복(토이서 확증).
- **토이 4-PLANT ALL PASS**: ITEM-MEMORY(planted+decay)·NULL(repeat≈shuffle)·VOID(무동적범위)·CONTRAST-NO-DECAY(무감쇠 artifact) 전부 정확판정. 다음=owner-go 303M fire(recon_err liveness=VOID gate 재확인).

## $0-first (제한적)
session_seed 앵커가 상수에 가까워 자연반복이 confound → 순수 $0 관측 취약. 사실상 cheap CPU chat run(--percept-file 스케줄) 필요 — pod 아님·저비용.

## 이견/충돌 (reconcile)
- H_9790(sleep store 성장)과 직교(각성·store-sealed).
- Sol: 고유 제안 없음 → Fable P4 채택.
- fire 전 owner go(cheap CPU chat run이나 스케줄 flag 구현 선행). 등록=DIRECTIONAL 설계, verdict 아님.
