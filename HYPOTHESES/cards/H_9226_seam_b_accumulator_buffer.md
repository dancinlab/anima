# H_9226 — Family B: accumulator-to-threshold buffer (evidence integration / phonological loop) RANK 2

**tier:** 🛠️ 구현됨·미측정 (engine-native summer op-grip PENDING) — Fable 설계 · bars frozen · p7 no tune-to-green
> ✅ live next candidate — distinct mechanism (evidence integration over TIME), survives H_9225 currency-conversion falsification.
> 🛠️ IMPLEMENTED: `cli/anima.hexa` H_9225 D1/D2/D3 블록 확장(3-site, additive-only 254 insertions/0 deletions) · `hexa typecheck` exit 0 (baseline benign `["emit"]` class +5, NO new error class) · production `idle`/`e_live` byte-untouched (FROZEN `og_h_frzB==0` = 증명). fire = `$0` op-grip summer(303M job 정리 후 큐), mini 금지.
**scope:** engine→mouth seam missing-intermediate 프로그램 — "buffer between" 가장 문자적 read
**cost:** **$0** op-grip (no decode)
**artifact:** `state/9226_accumulator/OPGRIP_SPEC.md` (구현 SSOT) · `state/seam_missing_intermediate/`

## 인과 척추 (공유)
mouth = RATE-GATE(미분기): urgency만 작동하는 건 이미 phasic Δ이라서(H_9101). self(.kosmos)·A⇄G tension은 TONIC LEVEL로 tick마다 read 후 폐기 → 미분기 기여 0 = ΔEff≈0(self⊥mouth·tension⊥mouth). 벽 = seam에 substrate 신호를 gate의 temporal currency로 변환하는 구조 부재. 오너: "입↔엔진 사이에 뭔가 필요."

## 가설 (missing intermediate)
느린 신호를 tick 넘어 **HOLD**하는 leaky accumulator(누설 적분기). 약하지만 지속적인 self/tension bias가 DDM 방식으로 threshold crossing까지 sum. 벽의 가장 문자적 read: 신호가 tick당 한 번 sampling 후 폐기되므로 작고 일관된 bias가 절대 적분 안 됨 — 부재가 아니라 **un-held(잡히지 않아서)** inert.

## 배선 site (a_substrate_disjoint)
seam lane 위 per-signal leaky integrator, 출력을 accumulated evidence로 gate에 공급, emit 시 reset. urgency와 DISJOINT.

## FROZEN BARS (p7 · verbatim)
- **freeze-self**: → ΔEff>0가 **LATENCY-to-effect signature**와 함께(효과가 N tick 일관 bias 후에만 출현).
- **shuffle 대조**: tick 순서 randomize → 붕괴(적분은 order-dependent).
- **양성 대조**: 작은 상수 self-bias가 결국 반드시 cross.
- **A와의 구분**: latency fingerprint(A는 transition-집중, B는 N-tick 잠복 후).

PASS = freeze-self ΔEff>0(latency 서명) ∧ tick-shuffle 붕괴 ∧ POS cross.

## 구현 (3-site · cli/anima.hexa · H_9225 블록 확장)
- **Site A carriers** (H_9225 Site-A 뒤): `acc_slf/acc_ten` leaky 적분기 · `xB_cal/xB_base/bB_med` calib · `gB_slf/gB_ten` gain · `capsatB` · latency sign-run(`runlenB/runsgnB`) · `swingB_max`(STIM-ABSENT source) · ΔEff/guard 카운터 · `og_h_frzB` · Ψ numerator · latency 버킷(`earlyB/lateB`).
- **Site B in-loop arms** (H_9225 in-loop 뒤, `if og_measure`): tick 50 calib(x_base=median·b_med·gain·capsat) → tick≥50 적분 `acc=0.90·acc+(x−x_base)` + latency sign-run(deadband 0.5·b_med) → shade=clip01(0.5+G·acc) → LIVE/FROZEN decode → mid 스코어·N3/WAKE 가드 → **own-emit HARD reset acc→0**(DDM discharge).
- **Site C post-loop verdict** (H_9225 verdict 뒤, `return` 전): ARM-INPERM order-shuffle 재적분(reset-faithful) margin bar 0.08 · latency ΔEff(late≥3·early ∧ early≤0.05 ∧ n_late≥10) · Ψ-guard · frozen bars → per-lane verdict ladder → 양-lane THEATER시 convergent seam-law INTERPRETATION. `midf`/`pos_pass`/`live_anchors`/`n9`는 H_9209/H_9225 블록서 재사용(재선언 X, scope 충돌 회피).

## 상태 · 제약
🛠️ IMPLEMENTED · 미측정(engine-native summer $0 op-grip PENDING — summer 303M job 경합, 정리 후 큐; mini 금지=OOM). typecheck exit 0. production idle/e_live byte-untouched(additive-only diff). p7 no tune-to-green(loss 미포함). p5 shade-not-gate(reactive speak() 금지). a_substrate_disjoint(emit-drive lane 불침). 승격 선례 H_9097/H_9101. 측정 idiom = $0 no-decode op-grip ΔEff(emit bitvector Hamming) + LATENCY 서명 + order-shuffle 붕괴.

## 근거 링크
- [[H_9225]](Family A · latency로 구분) · 선례 H_9097/H_9101 · DDM evidence-integration(phonological loop 유비, a_no_llm_frame_trap 유지)
