# core hexa⇄py 2-production 트레일러 발산 (SLW·CLML) — 발견 + 배선 스펙

**날짜:** 2026-07-10 · **출처:** Fable 5 `core/` 심화 분석(47턴, worktree `coredeep`) + 로컬 직접 검증 · **verdict-integrity:** fable 주장 3건을 `grep`/소스대조로 실측 확인함(추측 아님).

## 확정된 발산 (실측)

`core/decode.hexa` 는 `.clm` 트레일러 체인 `CLMX → CLMB → SLW → CLML` 에서 **CLMB 까지만 파싱**하고 **SLW·CLML 을 묵살**한다.

- 실측: `grep -ciE 'slw|clml' core/decode.hexa` = **0**. py 는 `core/decode.py:545`(`read_clml`)·`:680,719`(`slot_apply`)·`:739`(`lane_apply`)에서 읽고 적용.
- 함의: canonical `e1_slw_303m.clm` 은 SLW 트레일러를 가진 모델. `clm_decodable`(`core/decode.hexa:73`)은 CLMX 까지만 검사하므로 트레일러를 조용히 통과 → **같은 파일에 대해 `anima-py evaluate`(TERMINAL 표면, slot-ON)와 hexa `anima chat`/det-eval(slot-OFF)이 서로 다른 forward 함수를 계산한다.** hexa 는 py 의 "byte-parity twin" 이 아니라 다른 모델이었다.
- Gate4(fork-A CLML lane) 가 🟢 로 착지해 lane `.clm` 이 생기면 CLML 로 **같은 발산이 확대**된다.

교차검증: 이 발산은 메모리 `hexa-py-trailer-divergence-slw-clml` 로도 독립 기록돼 있어 fable 이 같은 지점을 재발견 = 실물 신호.

## 코덱 SSOT (byte-parity 대상)

- **SLW** `core/slw.py` — magic `"SLW\x01"`=`[83,76,87,1]`. header `<III` = `n_slot·k·d_s`. 배열순서 `K_slots[n_slot·k] · W_r[k·d] b_r[k] · W_q[k·d] b_q[k] · W_v[d_s·d] b_v[d_s] · W_o[d·d_s] b_o[d] · w_g[d] b_g[1] · gamma[1]`, row-major LE f32. forward(`slot_apply` `:51-91`) = per-token 상태 슬롯: write-addr `a=softmax((W_r·h+b_r)·Kᵀ·scale)`, filler `v=W_v·h+b_v`, gate `g=σ(w_g·h+b_g)`, erase-then-write `S=(1-ga)S+ga·v`, read-addr `b=softmax((W_q·h+b_q)·Kᵀ·scale)`, `m=Σ b·S`, `out=h+γ(W_o·m+b_o)`. `scale=1/√k`. **γ=0 ⇒ exact passthrough**.
- **CLML** `core/clml.py` — magic `"CLML"`=`[67,76,77,76]`. header `<BIf` = `lane_type·r·tau`. 배열순서 `W1[d·r] · b1[r] · W2[r·V] · w_g[2d] · b_g[1]`, LE f32. forward(`lane_apply` `:42-64`) = causal cumulative-mean `c_t=cumsum(yn)/counts`, gate `g=σ([yn_t;c_t]·w_g+b_g)`, `z=gelu(c·W1+b1)`, `delta=clip((z·W2)·g, ±tau)`, `logits+=delta`. **lane_type=0/부재 ⇒ exact passthrough**. `yn` = pre-SLW-slot penultimate(`decode.py:711` 에서 slot 적용 전 캡처).

## hexa 배선 지점 (🟢/live-clm 시 · a_verified_must_wire 충족점)

1. **로더** `_clmd_load`(`core/decode.hexa:343-429`): CLMB 파싱(`:408-422`) 뒤에 `"SLW\x01"`→`"CLML"` 순서로 트레일러 파싱 추가. absent/short → `lane_type=0`(py `read_clml:91` 관용구). `clm_decodable`(`:73`)은 불변 — "트레일러 부재 ⇔ byte-identical" 계약 유지.
2. **scratch** `_clmd_scratch_new`(`:555`): SLW 슬롯 상태 `S[n_slot·d_s]` + CLML `c[T·d]`/`z[T·r]`/`delta[T·V]` resident 버퍼 + pre-transposed `W1t/W2t`(기존 `tcWt` 관용구 `:448-458`).
3. **streaming forward** `_clmd_fwd_logits_sc`(`:695`): 최종 GN 출력 `sc["yn"]`(`:752-755`)을 `yn_trunk` 로 스냅샷(**SLW 를 함께 들이면 slot 적용 전에 떠야 함** — py `:711` 순서), readout(`:759-778`) 후 CLML delta 가산. SLW 는 slot_apply 를 readout 이전 penultimate 에.
4. **per-call forward** `_clmd_fwd_logits`(`:785`)에도 동일 — `clm_forward_ce`/`clm_omega_closure` 측정 경로가 lane/slot .clm 을 정직하게 재도록.
5. **GEMM**: 두 lane GEMM(`c·W1`,`z·W2`; SLW 사영들)은 `_clmd_conv1d_pre(K=1)`/`mm()` 로 forge 시임에 태워 `cuda_available()` **default-on**(`a_gpu_default_no_optin` — env 게이트 금지, `_clmd_devres :685-693` 선례).

## 검증 게이트 (TERMINAL — pool 필요)

- `core/verify_clm_v2.py` 에 SLW·CLML 구조체크 + **parity 게이트**: "hexa slot/lane-ON logits vs py `slot_apply`/`lane_apply` max|Δ|" (f64 기준 0 또는 ≤2e-16 — CONV 미러 정밀도 급).
- 303M canonical `e1_slw_303m.clm` 로 실측 = **pool(summer/aiden), mini 금지**(swap OOM). typecheck 는 로컬 통과했으나(hexa v0.574.1 `OK`) SLW 상태루프 바이트-parity 는 typecheck 무관 — 반드시 런타임 대조.

## DISJOINT 보장 (a_substrate_disjoint)

(i) emit/silence 는 `brain_decide` 에서 logits **이전에** 완결, lane 은 EMIT 확정 후 바이트함수만 변경 — mouth⊥decision. (ii) Ψ 경로(`tr_psi`·`ci_emit_drive`)는 decode logits 미독. (iii) bias 유계(학습 gate×±tau clip). (iv) 부재 ⇒ exact passthrough. 회귀가드 = `psi_intact` ON==OFF Φ-checksum(`cli/chat.py:1958-1964`). ⚠️ `clm_decode_grounded` LM-argmax fallback(`decode.py:1522-1560`)은 lane 영향권 — ρ·tether 측정 시 ON/OFF 명시.

## 추가 발견 (별도 후속 · 이번 착지 범위 아님)

- **train lane opt-in GPU env (a_gpu_default_no_optin 패턴 · H_9119 계열)**: `cli/train.hexa:165-166`(`CLM_PROD_DEVFEED`/`HEXA_FUSE_ALL`)·`:448`(`CLM_PROD_DEVRESIDENT`/`HEXA_FUSE_ALL`)가 GPU device 경로를 opt-in env 뒤에 두고 default OFF. 참작: mac prebuilt 에 fused 커널 심볼 부재(link-capability 게이트 성격) + train 은 verdict 표면 아님. fix = `cuda_available()`+심볼가용 가드로 default-on 전환, **pool 검증 별도 필요**. `.harness/enforce_anima_gates.py` enforce-후보.
- **결합 무결성은 건강**: `core/`→`archive/bench/agent` import **0건**(실측), decode lane GPU 경로 default-on(`_clmd_devres=cuda_available()`, 구 `CLM_PROD_DEVRESIDENT` 게이트 제거됨). 단방향 불변식 위반 없음.
- **PSI 상수 3분열**(fable §1): `PSI_BALANCE`(`core/pure_field.hexa:90`) 로드만·prod 사용 0건, live Ψ 는 `tr_psi` thr/eps 호출부 리터럴(`cli/chat.py:1432`), `ep_psi_clamp` smoke-only — 설계("숫자 emit_policy 한 곳")와 어긋남. 별도 정합 후속.

## 상태

`구현예정·미배선` — hexa 배선은 위 스펙대로, **바이트-parity pool 검증 후** production 착지. Gate4(aiden 계산중, `state/recomb-routing-lane/`)가 🟢 면 CLML 포함, 🧱 면 SLW 만(이미 canonical .clm 에 실재하는 발산이므로 Gate4 무관하게 선행).
