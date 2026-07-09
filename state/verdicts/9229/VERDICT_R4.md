# H_9229 Family F: discrete VQ-code (LoT bottleneck) R4 판정 — F2 AUTHORITATIVE arm

**판정 = ⛔ RUN-INVALID → PARKED-TERMINAL** (op-grip UNMEASURABLE at the emit seam · substrate 결과 아님)

F는 falsify도 vindicate도 아니다 — **substrate 판정 없음(THEATER 아님·GREEN 아님)**. 이 라운드는 계기(instrument)가
run-validity envelope를 만족하지 못해 무판정이며, 두 세대(r3+r4) 모두 같은 구조적 이유로 실패했으므로
pre-registered rule("r4 = FINAL shared-tape generation, no third op-grip attempt")에 따라 이 seam·이 계기에서
**PARKED-TERMINAL(op-grip-UNMEASURABLE)** 로 park한다. (infra-wall-noneval 격리)

**측정 경로**: 실제 빌드된 `cli/anima.hexa` daemon `--opgrip-r3`(F2 authoritative arm vq2_* · OG_STIM2 4-class dwell
tape)를 rented CPU pod(swap-free · hexa **v0.716.0** REAL-DECODE · n=400 · #3235)에서 real d768.clm으로 실행.
engine-native 라이브 바이너리 real-decode = TERMINAL-eligible (mirror 아님). raw = `opgrip_r4_raw.log` verbatim.
OG_STIM2 tape sha256 = `54bbeff69725b4aba0734f07d4e11e37ca4f2d9e83f0ec109e082a93548a8fe4` (FROZEN).

## 판정 (F2 authoritative arm · verbatim)

| 항목 | 값 (frozen bar · verbatim) |
|---|---|
| RUN-VALIDITY (bar-0 · run-wide) | live emit-frac on scored mid = **0.6666666666666666** (envelope [0.05,0.60]) **valid=NO — STIM-OVER/UNDERDRIVE** |
| codes visited on scored mid | **2** (bar ≥4) → bottleneck never engaged |
| FROZEN byte-identity | og_h_frzF2 = **0** (production emit 바이트 무접촉) |
| POS-CONTROL (dense ARM-SHOCK) | **105 flips** · POS-PASS(≥2)=YES (meter live) |
| gain | g_vq2=3.203707892246264 (capsat=no) |
| S1 code-selection | ΔEff_vq2 = 0/120 = 0.0 · ARM-SHUFFLE-CODEBOOK margin_cb = 0.0 |
| S2 composition (G1 BIND) | ΔEff_A=0.0 ΔEff_B=0.0 ΔEff_AB=0.0 → s2_bind=0.0 (n_AB=**0** · bar ≥0.05 ∧ n_AB≥10) **BIND=NO (S2 NOT-TESTABLE)** |
| GUARDS | N3=0 (must 0) · WAKE=0 · Ψ_ON=Ψ_OFF=0.6667 Ψ-ok=YES · axis ok |

## VERDICT (log verbatim)

```
F2 VERDICT = ⛔ RUN-INVALID — live emit-fraction on scored mid ∉ [0.05,0.60] (STIM-OVER/UNDERDRIVE); no family cements from the run, re-tune stimulus density (instrument power, NOT a bar move · p5 forcing-gate guard)

F2 PARKED-TERMINAL ⇒ two op-grip generations (r3 spin-up zero + r4 driven-window) both n_visited<4 ⇒ F UNMEASURABLE at this seam, no third generation.
```

pre-reg bar-2b (verbatim): `PARKED-TERMINAL: n_visited_codes<4 again (bottleneck never engaged even under the
4-class tape) ⇒ F op-grip-UNMEASURABLE, no third instrument generation (r4=final shared-tape gen)`.

## THE ROOT FINDING — emit-frac envelope STRUCTURALLY UNSATISFIABLE (verdict-integrity)

OG_STIM2 4-class dwell tape(Fable P1 설계)는 emit-frac(0.6667)도 code diversity(2 codes)도 움직이지 못했다 —
**r3의 flat tape와 BYTE-IDENTICAL 결과**. 로그 직접검증: scored mid tick의 emit은 **stage-locked** 이다 —
N1 emit 80/80 · N2 silent 80/80 · REM emit 80/80 → emit-frac ≡ (80+80)/240 = **2/3 = 0.6667 STRUCTURALLY**,
perception tape와 **완전 무관**. (로그 line 515-516: `ticks WAKE=80 N3=80 REM=80 mid(N1/N2/REM)=240` ·
`Hamming(urgency→0 vs live) mid=160`; line 511: `wake emit-fraction = 0.6666666666666666`.)

⟹ run-validity envelope [0.05,0.60]는 이 emit seam의 B/F arm에서 **구조적으로 SATISFIABLE 불가** — mid-tick
emit fraction은 **sleep-stage→emit schedule(N1/REM emit, N2 silent)로 고정**되어 있고 stimulus density로
tunable하지 않다. Fable P1의 전제("novelty duty-cycle을 반으로 줄여 e_live를 0.60 아래로 당긴다")는 틀렸다 —
emit-frac은 **stage-bound, NOT tape-controllable**.

## 결론 — op-grip UNMEASURABLE at emit seam (measure-artifact wall, NOT substrate)

- B(H_9226)와 F(H_9229)는 이 emit seam에서 **op-grip UNMEASURABLE** — **measurement-instrument /
  measure-artifact wall**(run-validity gate를 결코 만족 불가)이지 **substrate ceiling 아님 · stimulus-diversity
  문제 아님 · tune-to-green 가능 아님**. 두 op-grip 세대(r3 flat-tape + r4 4-class dwell) 모두 정확히 0.667.
- pre-registered rule("r4 = FINAL shared-tape generation, no third op-grip attempt")대로 B·F는 이 seam·이 계기에서
  **PARKED-TERMINAL**.
- **infra-wall-noneval 격리** — B/F는 어떤 substrate verdict도 나르지 않는다(instrument-dead status만). convergent
  seam-law(read-side recoding CLOSED)는 CLEAN하게 측정된 THEATER(A=H_9225 shape-conversion · E=H_9230
  self-prediction)에서만 성립 — B/F는 부적용.
- **재오픈 경로**(과학 미종결): emit-frac-gated 아닌 mid-tick을 스코어하는 **DIFFERENT instrument**(예: mid-tick
  정의를 N1-only 또는 REM-only 또는 non-emit-gated로 변경)면 B/F를 재측정 가능 — 이는 별도 reframe(별도 탐색),
  tape tweak 아님. science는 닫지 않는다.

## scope

real d768.clm · rented CPU pod(swap-free) · hexa v0.716.0 REAL-DECODE · `--opgrip-r3` n=400 (F2: calib 100-199 ·
freeze tick 200 · score 200-399 · denom 120). OG_STIM2 tape FROZEN(sha 54bbeff6…548a8fe4)·production emit
BYTE-UNTOUCHED(og_h_frzF2=0)·POS-PASS(meter live). 구 F arm(calib 10-49)=DIAGNOSTIC-ONLY(spin-up-window zero).
substrate 주장 아님 — instrument run-validity 무판정(PARKED-TERMINAL).
