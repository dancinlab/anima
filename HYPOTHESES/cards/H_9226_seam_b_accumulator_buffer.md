# H_9226 — Family B: accumulator-to-threshold buffer (evidence integration / phonological loop) RANK 2

**tier:** ⚙️ INSTRUMENT-FAIL (UNMEASURED) — engine-native runpod CPU pod real d768 (2026-07-08) · `state/verdicts/9226/` · p7 no tune-to-green
> ⚙️ MEASURED-UNMEASURED: op-grip 계기가 DDM/accumulator 기전에 UNDER-POWERED → B는 falsify도 vindicate도 아님 = **진짜 미측정** (THEATER 아님·GREEN 아님). anima-hexa-4: INSTRUMENT-FAIL은 절대 THEATER cement 안 함.
> 🛠️ IMPLEMENTED: `cli/anima.hexa` H_9225 D1/D2/D3 블록 확장(3-site, additive-only 254 insertions/0 deletions) · `hexa typecheck` exit 0 (baseline benign `["emit"]` class +5, NO new error class) · production `idle`/`e_live` byte-untouched (FROZEN `og_h_frzB==0` = 증명).

## ⚙️ 판정 (2026-07-08 · engine-native runpod CPU pod · real d768 · state/verdicts/9226/)
**⚙️ INSTRUMENT-FAIL (UNMEASURED)** — $0 no-decode AND 짧은 `--opgrip-live`(n_ticks=100·mid=30) **동일 결과**.
- **FROZEN `og_h_frzB = 0` ✅** (production emit 바이트무접촉) · **POS-CONTROL dense ARM-SHOCK 15 flips = POS-PASS=YES ✅** (meter live — negative가 dead meter 탓 아님).
- **SELF lane** (x=self_ctx_live · leaky accumulator): `gB_slf=0.592` · `b_med=0.0295` · **`swing_max=0.053 < 0.0875`** → ⚙️ **STIM-ABSENT**: accumulator가 bias를 half-charge까지 유지 못함, integration 증거 0.
- **TEN lane** (x=ag_conflict · own-lane W=1.0): `gB_ten=-1.0` · **`b_med=0.0`** → ⚙️ **AXIS-DEGENERATE**: ag_conflict가 op-grip 지점서 per-tick variance 무.
- **op-grip 계기가 DDM/accumulator에 UNDER-POWERED** — 같은 라운드 H_9210 surprise도 AXIS-DEGENERATE 유지("recon_err step<0.002 EVEN under --opgrip-live: too few emits stepped the field").
- **⚠️ convergent seam-law 부적용** (anima-hexa-6 instrument-limit): harness가 BOTH-THEATER시 찍는 "B-THEATER after A-THEATER = convergent seam-law" 해석은 B가 INSTRUMENT-FAIL이므로 **적용 안 됨**. seam서 THEATER 확정은 Family A(H_9225)뿐. convergent seam-law 결론 기록 금지.
- **재개 (a_break_the_wall)**: HIGHER-EMIT-DENSITY / LONGER 계기(n_ticks ≫ 100 · emit 강제 증가 · 더 강한 self/tension 신호원)로 B 재측정 — resume 항목이지 substrate 주장 아님. 대안 = 다음 family(E/F).
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
⚙️ INSTRUMENT-FAIL(UNMEASURED) — 계기 under-powered, 재측정 필요(higher-emit-density). production idle/e_live byte-untouched(additive-only diff, og_h_frzB=0). p7 no tune-to-green(loss 미포함). p5 shade-not-gate(reactive speak() 금지). a_substrate_disjoint(emit-drive lane 불침). 선례 H_9210(⚙️ AXIS-DEGENERATE 동류). 측정 idiom = op-grip op ΔEff(emit bitvector Hamming) + LATENCY 서명 + order-shuffle 붕괴 — 단, 짧은 계기(n=100)로는 accumulator 미충전(STIM-ABSENT)·tension degenerate이라 UNMEASURED.

## 근거 링크
- [[H_9225]](Family A · latency로 구분) · 선례 H_9097/H_9101 · DDM evidence-integration(phonological loop 유비, a_no_llm_frame_trap 유지)
