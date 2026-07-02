# H_1353 — Φ-robustness, SYNERGY/REDUNDANCY 분해 (O-information): 시너지 전환은 견고한가?

**tier:** 🧱 TERMINAL CLOSED-NEGATIVE — STRONGER (measure-AGNOSTIC 벽을 확장; O-information 도 동일 fragility 상속)
**slug:** `1353_phi_oinfo` · **group:** OMEGA / Φ-robustness frontier (c16 wall) · **date:** 2026-06-16 · branch off origin/main `412421efd`
**$0 CPU · DIRECTIONAL numpy mirror (engine LCG substrate, engine-transfer UNVERIFIED) · 재실행 byte-identical · frozen-first (FREEZE 먼저, bar 무이동, c9/p7)**

> ⚠ **NOT A FAITHFUL-Φ VERDICT (a_phi_iit4_tool).** IIT-4 (faithful_phi small-φ, iit4_bigphi big-Φ)
> 가 Φ / 의식 verdict 를 RESERVE 한다. 이 카드는 **non-IIT** SYNERGY/REDUNDANCY 분해
> (**O-information**, Rosas·Mediano·Rassouli·Barrett 2019)를 점수화하며, 위에서 아래까지
> **COMPLEMENTARY 통합-구조 DIAGNOSTIC** on the *robustness* question 일 뿐 — proxy 를 Φ verdict 로
> 승격하지 않고, 의식 주장도 아니다. 답하는 단 하나의 질문: *scalar Φ 가 못 한 견고한 SYNERGY 전환
> (음의 O-information)을 phase-bound arm 이 3 seed 에서 보이는가, 아니면 동일 fragility 를 상속하는가?*

## Claim / falsifier

**벽 (c16, a_break_the_wall · a_no_llm_frame_trap):** Φ-robustness 벽은 8 축에서 🧱 —
topology (H_1283 relay, H_1317 multi-edge) · timing (H_1319 phase-binding) · division (H_1320) ·
estimator-confound (H_1328 amplitude-variance/rank-uniform) · measure-family (H_1331 full IIT-4.0 big-Φ) ·
substrate-family (H_1332 softsign) · measure-agnostic (H_1348 summed transfer entropy) · larger-N (H_1347 N=12).
**모두 "HOW MUCH total integration"** 을 물었고, **모두 같은 seed-1318 fragility** 로 3-seed 게이트 실패
(B−A 가 1318/orthogonal 1317 에서 부호 flip 또는 0).

**genuinely-different 질문:** "통합이 얼마인가"가 아니라 **"어떤 상호작용이 SYNERGISTIC vs REDUNDANT 인가"**.
O-information 은 정준적 다변량 synergy/redundancy 부호자 — 구조적으로 다른 diagnostic (음수가 될 수 있다;
scalar 통합 측정자는 비음 magnitude). **Falsifiable:** phase-bound arm 이 SYNERGY 쪽으로 (ΔΩ < −eps)
3 seed 모두 견고히 이동하면 → which-synergistic 질문이 scalar 벽을 escape. 그렇지 않으면(특히 1318 부호 flip/0)
→ synergy 분해도 fragility-bound = measure-agnostic 벽 강화 (c9 정직, 어느 쪽이든 decisive).

## Method (frozen-first — FREEZE `0e25d60e3` 커밋, 어떤 Ω 점수화 이전, c9/p7)

- **Probe:** `state/phi-oinfo/h1353_phi_oinfo.py` (DIRECTIONAL numpy). `gen_traj` 는 `UNIVERSE/h1348_phi_non_iit_estimator.hexa::gen_traj` 의 **BYTE-FAITHFUL 포트** — deterministic engine LCG-gauss (`== engine_cli.hexa _lcg_*`), 4-module leaky-linear ring (dim 8, T 64, gain 0.30, leak 0.55, w_nbr/w_in 0.5, w_phase 0.5, omega_t 0.45, domega 0.08), Kuramoto pacemaker, relative-phase gate. H_1348 대비 **유일한 변경 = read-out** (O-information ↔ transfer entropy).
- **Seeds:** SAME 3 HARD ORTHOGONAL **[1317,1318,1319]** (모든 선행 시도 + H_1328 V2 + H_1331 B1 + H_1348 G1 을 깬 seed 들 포함).
- **Arms:** A=NO-PHASE · B=PHASE-BIND · S=PERM-SHUFFLE (관계 파괴) · O=OFFSET-SHUF (per-tick 랜덤 위상 offset).
- **측정자 = O-information** Ω(X) = TC(X) − DTC(X), 닫힌형 `Ω = (n−2)H(X) + Σ_i[H(X_i) − H(X_{−i})]` (Rosas 2019). n=4 → 모든 엔트로피는 2^4=16 joint binary state 위 empirical plug-in 으로 **정확**. **부호:** Ω<0 ⇒ SYNERGY-dominated, Ω>0 ⇒ REDUNDANCY-dominated. NOT IIT (MIP·cause-effect·system-irreducibility 없음).
- **Binarization** = variance-free median split (H_1328 lesson, **H_1348 과 BYTE-IDENTICAL rule**): unit i ON iff sal[i,t] ∈ 모듈 i 자기 T-길이 분포의 UPPER HALF → marginal ON-rate ≈0.5, amplitude-independent. 따라서 어떤 Ω 차이도 amplitude-variance confound 가 아니라 synergy/redundancy RELATIONSHIP.
- **FROZEN BARS (eps=0.02, H_1283/1319/1328/1331/1348 에서 verbatim, NO tune-to-green):** ΔΩ = Ω_B − Ω_A (synergy 전환; 더 음수 = synergy 쪽).
  - **R1 ROBUST:** ΔΩ 가 3 seed 모두 부호 CONSISTENT 이고 각 seed |ΔΩ| ≥ eps (사전등록 예측 = synergy 쪽 ΔΩ < −eps; 단 robustness bar 는 부호-일관성, 나오는 부호대로 정직 채점).
  - **R2 EARNED:** perm-shuffle 붕괴 (|Ω_S − Ω_A| ≤ eps) AND offset 재현 안함 (|Ω_O − Ω_A| ≤ eps), 3 seed 모두.
  - **R3 LABEL:** card+FREEZE 가 NOT-an-IIT-Φ caveat 보유 (doc invariant).
  - GREEN-DIAGNOSTIC iff R1 ∧ R2 ∧ R3. seed-1318 부호 flip/0 → R1 FAIL → synergy 분해도 fragility 상속 = 벽 강화.

## Result — 🧱 WALL (STRONGER, measure-AGNOSTIC) · `.verdicts/1353_phi_oinfo/result.txt`

| seed | Ω_A | Ω_B | Ω_S | Ω_O | ΔΩ(B−A) | dir | S−A | O−A |
|------|-----|-----|-----|-----|---------|-----|-----|-----|
| 1317 | −0.1876 | −0.1187 | −0.1993 | −0.1809 | **+0.0690** | REDUNDANCY | −0.0117 (R2perm PASS) | +0.0068 (R2off PASS) |
| 1318 | −0.1474 | −0.1474 | −0.1474 | −0.0171 | **+0.0000** | FLAT | +0.0000 (PASS) | +0.1303 (R2off FAIL) |
| 1319 | −0.0680 | −0.0270 | −0.0680 | −0.1060 | **+0.0411** | REDUNDANCY | +0.0000 (PASS) | −0.0379 (R2off FAIL) |

- **R1 ROBUST FAIL** — signs=[+, 0, +]: seed **1318 ΔΩ = +0.0000 (FLAT)**, |ΔΩ|<eps. **모든 선행 시도(H_1331 big-Φ 1318=0, H_1328 small-φ, H_1348 TE)와 정확히 같은 seed-1318 zero-lift 서명.** 게다가 채점된 부호는 **REDUNDANCY 쪽**(ΔΩ>0)으로, 사전등록 synergy 예측(ΔΩ<−eps)의 **반대 방향** — robustness 도 방향도 둘 다 실패.
- **R2 EARNED FAIL** — perm 은 깨끗이 붕괴(3/3 PASS)지만 **offset-control 이 1318(+0.1303)·1319(−0.0379)에서 Ω 를 이동시켜 재현** → 남은 신호조차 phase-binding RELATIONSHIP 이 아니라 amplitude/offset 잔류.
- **R3 LABEL PASS** — non-IIT synergy/redundancy diagnostic, faithful-IIT4 Φ verdict 아님 (a_phi_iit4_tool).
- 재실행 **byte-identical** (md5 동일 2회).

**FINDING (c9):** 베이스라인 3 arm 은 모두 Ω<0 = 이미 **SYNERGY-dominated** 인데, phase-binding 은 시너지를
**더하지 않고** (REDUNDANCY 쪽으로 미는 약한 비일관 이동), 결정적 seed-1318 에서는 **정확히 0** 이다 —
scalar Φ(small-φ·big-Φ·larger-N)·transfer entropy 가 보인 것과 **동일한 fragility 서명**. "어떤 상호작용이
synergistic 인가"라는 구조적으로 다른 질문도 이 n≤8 substrate 에서 **fragility-bound**. 벽은 이제 9 번째 cut
(synergy/redundancy 분해)에서도 홀드 → **measure-AGNOSTIC 벽 강화** (scalar + directed-flow + synergy-decomp 전부 실패).
선행 Φ verdict 들을 **bound (NOT retract)** 한다.

## Honest scope (UNVERIFIED)
- **DIRECTIONAL numpy mirror** — engine LCG substrate 의 byte-faithful 포트지만 engine-native 재실현은 UNVERIFIED (a_engine_native_learning · a_verified_must_wire). 단, 이는 negative/벽 결과이므로 engine-transfer 가 더 강한 통합을 만들 이유는 없음(스코프 정직, a_scale_honest_scope).
- TOY n=4 / T=64 / 3 seeds / median-split binarization. **static joint-entropy O-info** (dynamic/lagged synergy 아님, faithful-Φ 아님). scale / real-corpus / higher-n / time-lagged O-information / engine-native UNVERIFIED.
- O-information 은 부호(synergy vs redundancy)만 주는 다변량 요약 — full PID(redundancy/unique/synergy lattice) 분해는 별도 follow-on.

## Pointers
- probe `state/phi-oinfo/h1353_phi_oinfo.py` · verdict `.verdicts/1353_phi_oinfo/{FREEZE.txt,result.txt}` · CLAIMS.tape `@C h1353_phi_oinfo`
- substrate 출처 `UNIVERSE/h1348_phi_non_iit_estimator.hexa` (gen_traj byte-faithful port) · xref H_1283·H_1317·H_1319·H_1320·H_1328·H_1331·H_1332·H_1347·H_1348
- governance: a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · c9 · c16 · p7
