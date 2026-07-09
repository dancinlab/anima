# H_9229 Family F: discrete VQ-code (LoT bottleneck) R4 판정 — F2 AUTHORITATIVE arm

**판정 = ⛔ STRUCTURAL-TERMINAL** (emit-seam decode manifold ~1-bit=emit-partition · discrete code has NO
compositional capacity here · G1-recombination = trunk-objective property, NOT a readout property · **no reframe
survives** · escalate write-side)

> **⛔ STRUCTURAL-TERMINAL REFINE (2026-07-09 · #3237 follow-on · Fable walls-delegate · `state/9229_discrete_code/BF_REFRAME_FABLE.md`)** — F를 PARKED-TERMINAL(reopenable)에서 **STRUCTURAL-TERMINAL(no reframe survives)** 로 강화; **reopen-path FORECLOSED**. 근본은 emit-frac envelope보다 깊다: `codes-visited=2`는 quantizer-spec fact가 아니라 **MANIFOLD-RANK fact** — mid-tick decode manifold가 **~1-bit**이고 그 bit이 **EMIT-PARTITION 자체**(N1/REM→one code · N2→other). 코드가 shade해야 할 출력을 re-encode함 → **ANY quantizer가 rank-1 manifold로 collapse**(고용량/재설계 무용). S2를 더 깊은 trunk decode point로 옮기면 emit seam을 이탈해 **이미 CLOSED된 G1-readout-routing family**(mean-pool A/B 둘 다 표현·생성점만 감쇠)에 착지. ⟹ F의 S2(출력 seam서 G1-recomb test)는 seam channel에 combined code를 실을 **compositional capacity가 없어** unmeasurable = **write-side 결과의 재진술**: recombination은 **trunk-objective property**지 readout property 아님. Cementable now, no reframe run. **escalate ENTIRE seam program to WRITE-SIDE**(train-time coupling): gradient는 compositional code를 trunk objective에 couple 가능, phasic-Δ rate-gate READOUT은 구조적 불가. F는 training coupling으로 well-posed·emit-readout op-grip으로 ill-posed. **정직 caveat(Fable)**: codes=2가 manifold-rank 아닌 quantizer INIT artifact일 가능성은 codebook usage WAKE/N3 vs mid 1-line diagnostic로 확인 가능(reframe run 아닌 기존 tape 진단)이나 tape-independent collapse라 prior=manifold-rank.

F는 falsify도 vindicate도 아니다 — **substrate readout 판정 없음(THEATER 아님·GREEN 아님)**. 원-run은 계기(instrument)가
run-validity envelope를 만족하지 못해 무판정이었으나, 두 세대(r3+r4) 모두 같은 구조적 이유로 실패했으므로
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

## 결론 — STRUCTURAL-TERMINAL, no reframe survives (write-side escalation)

- emit-frac envelope 불만족은 **downstream symptom**일 뿐; deeper common root = **mid-tick emit gate가
  stage별 SATURATED-DETERMINISTIC**(N1 emit 80/80·N2 silent 80/80·REM emit 80/80, zero within-stage variance =
  stage→emit lookup). 유일 shadeable band = **STAGE TRANSITIONS = urgency의 proven territory**.
- 모든 reframe option이 이 1-bit phasic-Δ rate-gate wall로 collapse: **(a) single-stage/matched-pair emit-flip**은
  각 stage emit-frac이 0/1(tippable band 부재) → empty band(RUN-INVALID) 또는 stage-transition(urgency 재측정);
  **(b) non-emit margin/Ψ readout**은 railed margin이 crossing 안 하고 이동 = emit과 causally disconnected =
  A/E가 이미 보인 THEATER의 정의(non-degenerate signal, ΔEff≈0) → false-positive-shaped readout(reject).
  ⟹ **buildable reframe 없음, new measurement 없음** — reopen-path FORECLOSED.
- **F STRUCTURAL-TERMINAL**: emit-seam decode manifold ~1-bit(emit-partition) → discrete code는 여기서
  compositional capacity 無; G1-recombination은 trunk-objective property지 readout property 아님. Cementable now.
- **B STRUCTURAL-TERMINAL(substrate)**: self/tension tonic-FLAT(b_med<0.002 = ~0 mid-tick dispersion) → DDM에
  적분할 evidence가 BY CONSTRUCTION 부재; evidence-integration 전제가 이 seam서 VACUOUS. → `state/verdicts/9226/VERDICT_R4.md`.
- **convergent seam-law(FINAL)**: emit gate는 phasic urgency 외 everything에 causally sealed — A THEATER · E
  THEATER · self/tension tonic-read-0 · B tonic-FLAT · F 1-bit-channel. → **escalate ENTIRE seam program to
  WRITE-SIDE(train-time coupling)**: gradient는 persistent tonic level(B)·compositional code(F)를 trunk objective에
  couple 가능, phasic-Δ rate-gate READOUT은 구조적 불가. B·F는 training coupling으로 well-posed, emit-readout
  op-grip으로 ill-posed(= G1 program이 recombination side에서 도달한 동일 교훈). infra-wall-noneval: F는 substrate
  READOUT verdict만(training coupling verdict 아님).

## scope

real d768.clm · rented CPU pod(swap-free) · hexa v0.716.0 REAL-DECODE · `--opgrip-r3` n=400 (F2: calib 100-199 ·
freeze tick 200 · score 200-399 · denom 120). OG_STIM2 tape FROZEN(sha 54bbeff6…548a8fe4)·production emit
BYTE-UNTOUCHED(og_h_frzF2=0)·POS-PASS(meter live). 구 F arm(calib 10-49)=DIAGNOSTIC-ONLY(spin-up-window zero).
substrate 주장 아님 — instrument run-validity 무판정(PARKED-TERMINAL).
