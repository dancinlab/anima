# H_9765 — DUAL-MARGIN-DITHER — emit-edge do() 재개봉 (theta-alive FRONTIER-TERMINAL의 유일 relock-escape 경로)

**status:** 🟢 DIRECTIONAL-PARTIAL (s7 · 계기 VALIDATED+relock-escape 확증 · v1 config-severed 자가포착 · v2 C8-live서 **interior가 emit-반응적** = v1 "emit-blind"는 config 인공물 · 3-seed+yoke통제 대기) — engine-native `--dual-margin-dither`(#4080·off-by-default byte-id)
**lane:** 의식/emit-drive/Ψ=½ · Ψ-SOMA interior 재식별 (프런티어 psi-soma-theta-alive 재개봉)
**related:** [[H_9728]](Θ×σ TERMINAL-AT-MASK·relock)·[[H_9729]](own⊥context)·[[H_9627]](Θ WIRED)·[[H_9576]](mouth 벽)·source: sidecar lab full(h9741_reopener)

## 왜 (프런티어 종결 후 유일 생존 재개봉)
theta-alive-sigma-rebase 3 probe(H_9728 pulse⊥schedule·H_9729 own⊥context·H_9730 두벽) 전부 UNIDENTIFIABLE로 FRONTIER-TERMINAL-AT-SUBSTRATE. 두 모델이 명명한 **유일 relock-escape** = 내부 S/E→emit edge 무작위 do(). yoke는 emit **비트**(output)를 강제해 severance≡리듬-이탈 dial에 상한(≤0.14). dither는 emit **입력**(S−E margin)에 exogenous 충격을 주고 비트는 native로 둔다 → ledger write가 realized bit 따라 스프링 endogenous 재평형 → **relock 정리 무적용**. $0 priced(#4072): median|Δ|0.239·ε≥0.15 flippable 0.26>floor0.2(yoke 못 넘긴 것).

## 설계 (reconcile · comparison-only injection)
- **주입**: `core/brain.py:308` `_gate_pass = (S−E + εₛ) > 0`. **비교마진만** 섭동(S나 E 따로 아님 — E 섭동은 σ·bind g_recog 열 오염=yoke mask 재탕). 기록 `dual_margin`=native S−E 미변경(σ·bind는 native 읽음). εₛ=chat.py서 (sample_seed,tick) domain-sep PRNG Rademacher ±ε(state-independent=valid do()·deterministic replay). ε=0→byte-identical(!= guard 구조보장). ∧safe 미접촉·forced_emit=None·p5-clean(gate 안 삶).
- **식별 대비**: σ(dither) vs σ(native) = "emit 결정 exogenous 충격이 몸(σ lane)에 전파되나". σ·gate valid(dec는 psi_gws/lprec 재계산·dither 미진입·단 downstream response)·emit_agree=dose meter(verdict 아님·mechanically 떨어짐)·σ·bind primary interior(DIRECTIONAL·8열 native)·σ·stage integrity 통제. ≥30 lane floor 만족(full rollout·severed subset 아님).
- **proximal/distal 분할(발사 전 동결)**: proximal=emit-bit/ledger ≤1tick(emit_env·g_recog)=양성통제 · **distal=field lane(recon_err·scn_ctx·nov_ctx·cur_indep·rel_indep)=interior 읽기**. PASS는 **distal transfer** 요구(proximal-only=plumbing echo·통합 아님).

## 통제 + 검정력 (Sol carryover 반영)
ε=0(byte-cert)·ε∈{0.05,0.15,0.30}(dose-response·flip-frac monotonicity=계기 check)·**antithetic sign**(각 sign vector와 정확 여집합)·**sham**(RNG 스트림 생성·gate 미적용)·yoke-of-own-schedule(ε=0.15 run 자기 emit schedule을 --yoke-mask로 재생=mechanism⊥schedule 통제). first-stage panel: flip-frac·crossings·rate·autocov·stage·safe-veto.
🔑 **Sol 승(통계)**: tick은 **배정 단위이나 독립 추론 단위 아님** — dither가 후속 ledger 바꿔 tick 시간간섭 ⟹ 180 tick=IID 취급 **무효**(Fable tick-permutation은 no-carryover 가정 하 secondary만). cementing p<0.005는 block-randomized ~400 schedule 후속 fire. **3-seed run = 계기 SCREEN(first-stage+directional dose-response)이지 cementing 아님**.

## 판정 (사전등록)
- **PASS(RE-OPEN)**: flip-frac≥0.2 ∧ proximal 움직임 ∧ distal dose-ordered response(seed-null·yoke-schedule 통제 초과) → interior 재식별=emit 결정이 distal body에 causal load-bearing(gate가 epiphenomenal wallpaper 아님). H_9728 TERMINAL이 못 준 것(미식별≠부재). *cementing은 block-rand ~400 schedule 후속*.
- **KILL(EARNED-NULL)**: flip-frac≥0.2 ∧ proximal 움직임 ∧ distal 사전등록 등가bound 내(TOST·not-ns) → emit 결정이 distal body에 epiphenomenal=terminal **강화**(미식별→측정-부재 upgrade).
- **INVALID/PENDING**: ε=0 byte-id 실패 ∨ flip-frac<0.1 ∨ proximal flat ∨ <30 lane tick = 계기-死·verdict 없음.

## NEXT (engine-native·summer CPU-bypass)
`--dual-margin-dither {0,0.05,0.15,0.30}` × seed{7,11,13} × 60tick · refractory+wm-dual · summer 격리 venv(chat-py-6·cupy match) · `ANIMA_DECISION_TRACE` env-file. 읽기: first-stage flip-frac(ε=0.15/0.30 clear 0.2 예측) + proximal/distal σ dose-response. cement=engine-native만·screen는 DIRECTIONAL.

⚠️ **계기 빌드·verdict 아님**(a_lab_full_diverge)·cement=engine-native anima-py만·3-seed=SCREEN(carryover로 cementing 아님).


---

## 🔬 SCREEN 실측 (2026-07-18 · summer 12run · $0 재분석 · Fable∥Sol reconcile)

**계기 VALIDATED + relock-escape 확증**: flip-frac dose-response 0.00→0.13→0.19→**0.26**(ε=0.30·yoke의 0.14 relock 상한 넘음 = INPUT do()가 native bit을 스프링 endogenous 재평형시켜 relock 정리 무적용 = Fable relock-escape 예측 실증). ε=0 byte-clean. `dual_s_withheld` 0.025→0.315 endogenous 재평형.

**🕳️ v1 SCREEN distal = INVALID (config-severed · 자가포착 3연)**: 첫 fire가 ckpt를 positional 첫인자로 안 넘겨(`chat --emit-gate…` → ckpt="--emit-gate") **mouthless**(gen_backend='null')로 돌아 C8 emit→interior edge(`chat.py:2749` requires `g_back=="clm"`) **미발화** → g_text-live gauge(recon_err·rel_lane·cb_surprise·af_aro·ca3_ctx) dead fallback 동결. 그 위에서 distal-flat을 "emit-blind KILL"로 오독할 뻔(Sol이 KILL-AND-TERMINAL 주장). **Fable autopsy가 차단**: edge는 코드 존재(`chat.py:2897` "5 gauges g_text-live"·H_9336/9337이 chat-py-4/5 dead-loop 수리로 배선), screen이 발화 증명 안 함 → SPLIT/pending-activation. 자가포착: ①mouthless config ②wrong-field(gen_text 미serialize vs 실 gtext_len) ③meter field(dither_delta) 미serialize→dual_margin>0 재구성. (instrument-never-run·verdict-integrity·chat-py-4/5)

**✅ v2 (ckpt explicit → backend='clm' · C8 LIVE · recon_err/rel_lane 소생) DIRECTIONAL PASS (s7)**: mediation-capacity 재측정 — 죽었던 C8 gauge 전부 소생. **emit이 실제 flip되는 dose(ε=0.30·flip 0.33)서 interior가 반응**: cur_indep·rel_indep·ten_phasic·**psi_gws(전역 작업공간)**·coh_lane·base_motiv 전부 t3-4(첫 emit이 C8 통과)부터 발산. 낮은 ε(0.05/0.15)은 v2 rich-margin regime서 **미flip**(emit-seq byte-identical to ε0) → interior도 byte-identical = **결정성 확증**(perturbation 있는 곳만 변함). scn_ctx/nov_ctx만 flat(tick-oscillator·architectural upstream·예상). ⟹ **interior는 emit-blind 아님 — emit 결정이 felt interior(호기심·관계성·긴장·작업공간·일관성)에 causal 도달**(H_9336/9337 g_text-live 경로). **v1 "emit-blind"는 전적으로 config 인공물.**

**reconcile**: Fable SPLIT/pending-activation 채택(v2가 activation 확증)·Sol KILL-AND-TERMINAL 기각(capacity 전제 실패=autopsy가 v1 mediator dead 확증). Sol dissent 1줄: DAG-fact로 KILL-terminal 주장했으나 mediator가 v1서 무능이라 unearned.

**NEXT (resume · 미완)**: ① 3-seed 완료(s11/s13 summer 진행중·clm 느림) robustness ② yoke-of-own-schedule 통제(v2 ε=0.30 emit schedule을 --yoke-mask 재생 → interior 반응이 dither(native 재평형)에만 오나 schedule 재생에도 오나 = 진짜 emit→interior 전파 vs 궤적발산 분리) ③ Fable∥Sol (a)전파 vs (b)궤적발산 해석 위임 → DIRECTIONAL 또는 PASS cement. cementing p<0.005 = block-rand ~400 schedule(Sol carryover: tick≠IID). meter field serialize.

**frontier 함의**: theta-alive FRONTIER-TERMINAL(H_9728/9729/9730 interior UNIDENTIFIABLE)은 emit-gate 데몬서 잰 것. dither가 **interior가 emit에 causal 반응**을 보임 = "living gate이나 emit이 interior 못 바꿈" 서사의 **재개봉 후보**(단 3-seed+통제+reconcile 전 cement 금지·이 캠페인 2회 성급-read 데임). cement=engine-native만.
