# H_9765 — DUAL-MARGIN-DITHER — emit-edge do() 재개봉 (theta-alive FRONTIER-TERMINAL의 유일 relock-escape 경로)

**status:** 🔧 계기 빌드 (engine-native `--dual-margin-dither` · off-by-default byte-identical · 발사 전 · 재설계 lab-full Fable∥Sol 수렴)
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
