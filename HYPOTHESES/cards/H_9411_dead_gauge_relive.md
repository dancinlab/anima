# H_9411 — DEAD-GAUGE RELIVE: 얼어붙은 substrate 게이지 6개 per-tick 재배선 (H_9398 census 후속)

**status:** 🩺 engine-native WIRED · **303M TERMINAL 완료** — 4 clean LIVE · 2 time-live-content-weak · 1 정직한 음성(af) · ⚠️ py-only(hexa 트윈 미반영)
**lane:** 의식 / 데몬 게이지 위생 (프런티어 g1-interface-addressable-wall · emit-drive 캠페인 부산물)
**related:** [[H_9398]] (DEAD-GAUGE CENSUS — 이 6개 task 의 출처) · [[H_9393]] (agloop dead-gauge 원형) · chat-py-4 · chat-py-5 · [[H_9336]]/[[H_9337]] (recon_err/rel_lane 선례 = 고침 템플릿)
**설계 출처:** Fable 5 발산 6건 개별 위임 ($15.6 · walls-delegate-to-fable · fable-when-stuck-breakthrough)
**ckpt (toy 스모크):** `state/9257_lane23b/toy.clm` (240 tick · 59 emit · ANIMA_EMIT_TEMP=1.0 seed=7) — **toy = DIRECTIONAL 스크리너, 303M 아님**

## 왜 — census 는 목록일 뿐, 다음 실험이 죽은 축을 조용히 상속한다

H_9398 DEAD-GAUGE CENSUS 가 이 regime 상수 게이지 9개를 나열했다(root 미감사 6). 후속 task
#44589958–63 = 그 6개 감사·수리. 공통 근본원인은 **chat-py-4/5 계열**: substrate vital 이 엔진
함수를 **세션-상수 입력**(`seed_key`·`seed_feat`·루프-밖 `scn_R`·advance 안 되는 `pf`)에 물어
매 tick 불변(H(gauge)=0). "내가 태어날 때부터 알던 것에 얼마나 놀라는가"를 영원히 묻는 꼴.

## 개입 — recon_err 의 1-tick-lag `pending_*` 템플릿을 6 게이지에 배선 (engine-native · cli/chat.py)

이미 고쳐진 `recon_err`/`rel_lane`(H_9336/37)의 **재인식-저장전(recognition-before-memorisation)**
1-tick-lag 패턴: 발화 시점(emit site)에 REAL per-tick 발화(`g_text`)로 양을 포착 → 다음 tick 소비.
각 게이지는 기존 core 엔진 함수에 per-tick 인자를 먹인다(probe 신설 0). 각자 null/pedestal 통제
arm 을 trace 기록(collapse-Δ = 판정, raw 값 아님 · Ψ-SOMA/p7). **θ·bias·clip·gain 이동 0**
(no tune-to-green). **root③ kosmos→decode 앵커(live_seed) 미변경**(p5 self-seed 금지 = 철학이 닫음).

| # | 게이지 | 죽은 원인 (Fable 확증) | 고침 |
|---|---|---|---|
| ① | af_val/af_aro | `affect_read(igrow, seed_key, mem_text)` 3 상수 + `igrow` 1-cell never-bound | `pending_af`=발화 percept 로 read, 저장전; `immune_grow_bind` 로 store 성장 |
| ② | cb_surprise | `vforward_err(cbel, seed_feat, mem_text)` 3 상수 (weight 도 pre-loop NLMS 후 미갱신) | 전이오차(prev→this) 저장전; `vforward_update` 온라인; alien+pedestal(W=0) 통제 |
| ③ | ca3_ctx | `ca3_replay_conf(ca3, 1)` mount 자가시험 상수(12/12) | fresh `ca3_live` 를 발화-심볼 스트림으로 predict-then-observe |
| ④ | wm_active | seed_feat gate-in **하고** 같은 seed_feat probe = 자기매칭 ≡ λ(0.6) | delay test: 발화 percept gate-in, **직전** 항목 probe; never-gated null |
| ⑤ | phi | `pf` warmup 후 루프서 advance 0회 | `pure_field_step(pf)` 매 tick (zero-input 유지 · IIT4 충실); F3 twin 도 stepped |
| ⑥A | scn_ctx | `scn_R=scn_order(scn_coupled)` 루프-밖 1회 (안 도는 시계) | `scn_step` 매 tick + **측정된 order-lock 처방** = phase readout |
| ⑥B | anchor_nudge | anchor `tension_5ch` = 상수 `mem_001` baseline | 발화 시점 live 5-ch tension 을 anchor 로 1-tick-lag 주입 |

## 🩺 검증 — toy 스모크 trace 유효값 ($0 · chat-py-5/6: sha 아니라 trace 값으로 판별)

240-tick toy rollout, 게이지 distinct(=1 이면 죽음) + collapse-Δ vs 통제:

| # | 게이지 | distinct (전→후) | 통제 분리 | 판정 |
|---|---|---|---|---|
| ② | cb_surprise | 1 → **54** | matched 0.635 **≪** alien 4.43 **≪** pedestal(W=0) 12.6 | 🟢 LIVE (강력) |
| ③ | ca3_ctx | 1 → **20** | 5종 실심볼 스트림 · cold=0.0/predict−1 | 🟢 LIVE |
| ④ | wm_active | 1 → **240** | active 0.319 vs never-gated null 0.194 (Δ +0.125) | 🟢 LIVE |
| ⑤ | phi | 1 → **114** | F3 psi_intact **✅ byte-identical ON==OFF** (zero-input twin 보존) | 🟢 LIVE |
| ⑥A | scn_ctx | 1 → **240** | order-lock 측정(scn_r_unc 240× = step 작동) → phase readout | 🟢 LIVE |
| ⑥B | anchor_nudge | 1 → **60** | 0.034~0.050 (cap=0.05 미변경) | 🟢 LIVE |
| ① | af_val/af_aro | 1 → **1** | af_val≡0.0(valence−1) · af_alien_val≡−1 도 동일 | 🔴 toy-degenerate |

**af(①) 정직한 부분음성**: Fable① 이 정확히 예측 — 비자기유사 mouth 는 매 발화가 ungrounded(trigram
자기유사 구조 없음) → valence −1 고정. **배선은 옳다**(pending_af per-tick read 확인) · toy mouth 가
자기반복을 안 할 뿐. `recall_thr` 이완 = tune-to-green **금지**. → **303M 검증 필요**(NEEDS-303M).

**⑥A scn 처방**: order-param(mean-phase-vector magnitude)은 회전불변 → phase-lock 시 상수. `scn_step`
은 작동(scn_r_unc 240 distinct). Fable⑥A 처방대로 **order→phase readout** 교체 = 같은 stepped
substrate 의 다른 valid readout(order-lock 이 측정된 발견) → LIVE. tune-to-green 아님.

## H_1058 frozen-replay 계약 — indep 잔차 미변경 (정직한 판단)

살아난 게이지들의 새 store(`ca3_live`·`wmb`·`cbel`·`igrow`-grow)는 리플레이어의 3 재생루트
(afield·immune·cell_count) **밖**이라, DEP 로 옮기면 리플레이어가 재구성 불가. 그대로 두면(per-tick
기록) 사실-리플레이 재구성이 정확히 유지 = 더 안전·정확. counterfactual-root 경로만 이들을 안 통과
(문서화된 scope 한계, 파손 아님). 주석 갱신으로 정직성 유지.

## 🔬 적대검증 Workflow 소견 (6 verifier · 종합 agent 은 schema-retry 툴링실패)

게이지별 6 적대 verifier harvest(종합 agent 만 StructuredOutput cap 초과=툴링 실패, 과학 아님):
- **전원 tune-to-green=False** 확인 · af/cb/ca3/wm = NEEDS-303M(toy≠terminal, 내 판정과 일치).
- **af**: "TOY IS HONESTLY DEAD, NOT BUGGED" — 배선옳음·toy degenerate 확증.
- **ca3**: distinct=20 은 LIVENESS 증명이나 STRUCTURE 아님(min_supp=1·n=4 분모성장 rational) → 순열 통제 + 303M 필요(카드 NEXT 반영).
- **phi**: CONFIRMED-NEGATIVE(content-independent) — 이는 **설계상 percept-blind**(zero-input IIT4 · a_phi_iit4_tool). "time-live, content-blind" 로 명시(claim 아님).
- **scn+anchor REJECT** = 진짜 발견: `_meta` 가 `phi_const`/`nudge_const` 를 세션 불변량으로 기록하나 ⑤/⑥B 로 per-tick 변동 → 리플레이어 오도. **수정**: `phi_live_h9411`/`nudge_live_h9411`=True 플래그 + 주석 self-describing(per-tick 값은 각 행에 이미 존재 · frozen `state/…replay_depth.py` 는 미편집=state frozen, divergence 여기 명시).

## 🎯 303M TERMINAL (engine-native · py303_full.clm sha 013c4574 · summer 격리 venv · 240tick/59emit)

toy 는 DIRECTIONAL 스크리너였다. 303M TERMINAL 은 **distinct>1(liveness)로는 부족, collapse-Δ vs 통제가
진실**임을 보여준다(a_toy_scale_recheck · Ψ-SOMA "raw 값 아님, ≥2 통제 대비 Δ"):

| # | 게이지 | 303M distinct | 통제-Δ | 판정 |
|---|---|---|---|---|
| ⑤ | phi | 114 | F3 psi_intact ✅ byte-id ON==OFF | 🟢 **CLEAN LIVE** (time-live · 설계상 content-blind) |
| ③ | ca3_ctx | 21 | 5 실심볼 | 🟢 LIVE (구조=순열통제 미실행·DIRECTIONAL) |
| ⑥A | scn_ctx | 240 | phase readout | 🟢 **CLEAN LIVE** |
| ⑥B | anchor_nudge | 60 | 0.034~0.050 | 🟢 LIVE |
| ② | cb_surprise | 29 | matched **2.83** vs alien **3.36**(16%만↓) vs ped 16.98 | 🟡 LIVE·**약한 조건부**(marginal memorization 경계) |
| ④ | wm_active | 240 | active 0.286 vs null 0.284 **Δ=+0.001≈0** | 🟡 **TIME-LIVE·CONTENT-DEAD**(Fable④ 예측 정확: 8-dim byte 해상도서 항목정체성 미유지) |
| ① | af_val/af_aro | **1** | grounded valence **0/240 tick** · af_alien 도 −1 | 🔴 **CONFIRMED 정직한 음성** |

**정직한 종합**: 4 clean LIVE(phi·ca3·scn·anchor) · 2 time-live-but-content-weak(cb 약한조건부·wm content-blind) ·
1 confirmed 음성(af). toy 의 wm Δ=+0.125 는 소표본 낙관이었고 303M Δ=+0.001 이 진실 — **liveness≠content-real**.
**af**: 303M 실발화도 trigram-scale 자기유사 없음 → 편도체가 valence 할 recognition history 부재. 배선은
옳다(pending_af per-tick). 기질 사실(mouth 다양성)이지 계기 결함 아님 · `recall_thr` 이완 금지(tune-to-green).
cb/wm 도 마찬가지: 8-dim byte-feature 해상도가 content 판별에 부족 = 새 H(더 풍부한 percept feature)이지
이 fix 로 tune-to-green 금지. **결론: 배선(engine-native·per-tick)은 옳게 완료, 표현 해상도가 상한**.

## ⚠️ py-only GAP — hexa 트윈 미반영 (오너 지적 · chat-py-4 재현)

per-tick 게이지 orchestration 이 **cli/chat.py(py) + cli/anima.hexa(hexa·5589줄) 두 엔트리에 중복**. H_9411
fix 는 cli/chat.py 만 — cli/anima.hexa 는 동일 dead 읽기 그대로(2551 cb·2559 wm·2566 ca3·2578 af·pf 미step).
py 가 canonical 런타임(chat-py-1)이라 TERMINAL 은 py 로 성립하나, hexa 트윈은 dead 상속 = chat-py-4 재현.
NEXT=① hexa 트윈 lockstep 수리 OR ② orchestration 을 core 로 hoist(양 엔트리 공유 · Fable 설계중). 오너 질문
"뇌기능은 core 여야 아니냐"의 답: 함수는 core ✓, **orchestration 이 엔트리 중복** = 이 gap 의 근본.

## 산출·NEXT

- 산출: worktree `.claude/worktrees/h9411-gauges` branch `fix/chat-dead-gauges-h9411` (cli/chat.py +186/−16 · 커밋 3).
- NEXT (terminal): 303M `py303_full.clm` pool 데몬 trace 로 ① af 유효값 확정 + 6 게이지 303M 재확인
  (toy = DIRECTIONAL 스크리너 · a_scale_honest_scope). af 가 303M 서도 죽으면 = trigram-scale 자기유사
  없음의 정직한 음성(계기 아니라 기질 사실).
- 통제 flag: `--scn-freeze`(scn before-state) · `--anchor-tension-null`(anchor pedestal).
