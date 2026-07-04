# H_9102 — stateful refractory: emit-history recovery-after-firing (the real alchemy of H_9101 item-1)

**tier:** 🟢 F2 NEW-MECHANISM ∧ 🔴 F1 NO-CARRYOVER · **DEPLETED (MIXED honest terminal)** (engine-native) · **wired:** engine-native measured — `an_clock_now` det-seam + `--refractory` harness LANDED in `cli/anima.hexa`; PRODUCTION emit loop keeps H_9101 (WIRED-live), stateful swap = follow-on with its own pre-reg
**verdict:** F2 🟢 refractory-reset holds (40/40 post-emit ticks silent even at max urgency; the H_9101 stateless idle would fire all 40 = stateless-inexpressible) ∧ F1 🔴 H_9101 op-grip does NOT re-establish on its frozen REM bar under stateful dynamics (urgency→0 REM=0/40, grip relocated to WAKE 39/40, N3=0 preserved, no post-hoc bar move). Ψ ON≡OFF ✅. F4 det 2× byte-identical.

## Claim (fable analysis, DESIGN.md §2·§4)
H_9101 item-1's "real-time follow-on" bundled two axes. The wall-clock TIME-SOURCE axis is scientifically INERT (tautology — same input scalar ⇒ same decision, det vs `date +%s` predictable → no experiment). The **real alchemy** is the TIME-STRUCTURE axis: H_9101's `idle = 5+55·clip01(stage_env·(0.5+urgency))` is a per-tick **STATELESS** function — no emit history, so its "refractory" is a momentary *shade*, not recovery-after-firing. A neuron's refractory is "recovery since last spike", not "shade of the present state" (`a_no_llm_frame_trap` bio lens). This H wires the missing emit-history state so `idle` becomes a stateful dynamical variable, then re-tests H_9101's grip (F1) and the genuinely new falsifiable content (F2), all det-clock engine-native.

## Wiring (cli/anima.hexa only — engine FROZEN, H_9101 principle)
- **Clock seam** `an_clock_now(tick, daemon)` (flame_mm.mm pattern — ONE fn, TWO bindings, ONE downstream algebra): det/verdict path = `tick * an_tick_seconds()` (=8.0, matches `dr_stage_at(tick*8)` sampling, byte-identical); daemon path = real `date +%s` (FOLLOW-ON ING — no persistent daemon exists; the loop is bounded 12/200 ticks). Verdict path always det (`refr_daemon=false`) → F4.
- **Emit-history state** (was ABSENT = the core gap): `mut emit_last_t = -1e9`, `mut prev_live_emit`. Per tick: `t_now=an_clock_now(tick,daemon)`; `idle_raw = t_now − emit_last_t` (TRUE seconds-since-last); `mod = clip01(stage_env·(0.5+urgency))` (H_9101 term, unchanged); `idle = idle_raw · mod`; decide; **if did_emit { emit_last_t = t_now }** (the refractory RESET = the heart).
- **Constructive properties:** mod≤1 ⇒ idle≤idle_raw ⇒ gate-pass(≥30) ⟹ real elapsed ≥30 (the FROZEN 30s floor becomes a **theorem**, no longer vacuous — vs H_9101's `5+55·mod` which yields 60 at 0 elapsed) · env=0 ⇒ mod=0 ⇒ idle=0 (N3 preserved by construction) · urgency modulates the gate-open TIME (idle_raw ≥ 30/mod), extending op-grip from "whether" to "when".
- **New measurement mode** `--refractory` (200-tick stage-balanced `tick%5`, decision-only, NO decode, $0). Arms per tick, same emit-history: live, urgency→0 (F1), urgency→max (F2), and the H_9101 stateless-idle counterfactual (F2 contrast).
- **FROZEN (untouched):** engine `safety_rate_limit_ok` (≥30), `phi_r`, `kill`, `content`, 8 weights, 0.3 threshold, Ψ. H_9101's production `idle` (L2381) and its `--opgrip` harness are UNCHANGED (frozen bar not disturbed).

## Result (engine-native, aiden pool `hexa v0.548.0`, `anima ~/anima/d768.clm --refractory`, RC=0, L3 mount mouth=clm loaded=true d768.clm, HEXA_DET=1, NO numpy — pure `.hexa` on live cli, grep gate empty by construction: no `.py` on the measured path)
`state/verdicts/9102_stateful_refractory/H_9102.txt` · raw run1 `state/9102_stateful_refractory/H_9102_refractory_aiden_v0548_run1.txt` · pre-reg `state/9102_stateful_refractory/PREREG.md` (frozen BEFORE run).

Summary (n=200, live_emits=40):

| axis | measurement | pre-reg | outcome |
|---|---|---|---|
| **F1 grip (frozen REM bar)** | Hamming(urgency→0 vs live): REM=**0** N3=**0** WAKE=**39** mid=0 | REM>0 ∧ N3=0 | **🔴 no-carryover** (grip relocated REM→WAKE; N3 preserved) |
| **F2 refractory reset** | window=40 · max-urgency violations=**0** · stateless-would-fire=**40** · umax-nonrefr=80 | violations=0 ∧ nonvac>0 | **🟢 holds** (stateless-inexpressible) |
| **F4 determinism** | HEXA_DET 2× | byte-identical | **🟢** |
| Ψ ON==OFF | refr_psi_sum==refr_psi_off | invariant | **✅** |

- **Mechanism (per-tick trace):** stateful dynamics settle into a periodic emit at **WAKE** (idle_raw=40, mod~0.9, idle~36≥30 → emit → reset), silence at **REM** (idle_raw=32, mod~0.73, idle~23<30 → silent regardless of urgency). So under stateful dynamics REM no longer emits → urgency→0 cannot flip REM (Hamming 0), while WAKE emits and urgency→0 drops idle 40·0.5=20<30 → flips 39/40. The op-grip **carried over but moved stages** — the FROZEN pre-reg bar is REM, so F1 fails honestly (no bar-move to WAKE).
- **F2 = the real alchemy:** every tick right after a live emit has idle_raw=8 (one tick), so idle_umax = 8·mod ≤ 8 < 30 → silent by construction, 0 violations across all 40 windows. The H_9101 stateless idle (`5+55·mod`) at max urgency in the same 40 ticks would emit all 40 (no history to suppress) — the refractory reset is a dynamical property the stateless form **cannot express**. That is precisely what a real seam adds beyond H_9101.

## Honest verdict (c9, no tuning, no bar-move)
The stateful refractory **IS a genuinely new mechanism** (F2 🟢: recovery-after-firing, stateless-inexpressible, + makes the frozen 30s floor a theorem rather than vacuous) — **AND simultaneously** H_9101's op-grip does **NOT** auto-transfer to the stateful regime on its pre-registered REM bar (F1 🔴: the emit-stage relocated REM→WAKE). Both are true; neither is suppressed. Because F1 fails, the stateful refractory does **not** replace H_9101 in the production emit path (that swap would trade H_9101's live REM-grip for WAKE-grip+refractory — a design change needing its own pre-reg, not this task's mandate). Landed: the `an_clock_now` det/daemon seam + emit-history state + `--refractory` measurement, all engine-native.

## Follow-on (ING)
- **Real-clock daemon binding (F3):** wire `an_clock_now(daemon=true)` when a persistent daemon exists → smoke-assert real inter-emit interval ≥30s (world-time safety truth; F3 is a property-smoke, not a byte-exact verdict). Separate ING (daemon loop-closing is prerequisite).
- **Production stateful-swap pre-reg:** if the stateful refractory is to replace H_9101 in production, pre-register a WAKE-anchored (or stage-agnostic) grip bar first — REM-anchored H_9101 does not transfer.

## 고갈 (DEPLETION census · Fable · state/9102_stateful_refractory/DEPLETION_census.md)
**F7 = DEPLETED. MIXED(F2🟢∧F1🔴)가 honest terminal.** 직교 family 전수: (a) WAKE-anchored 同하네스 F1' 재측정=🧱 tautology(결과 WAKE=39/40 이미 stdout, post-hoc 바 이동을 pre-reg로 세탁=비합법) · (b) stage-agnostic 리프레임=합법이나 non-load-bearing(confirmatory·H_9103 노이즈 승격 못함) · (c) 재배치=refractory attractor×frozen stage_env(WAKE=1.0 최고) 구조적 필연, tune-away 불가 · (d) F2가 유일 진짜 알맹이(LANDED). **결정타: grip 자체가 faculty 아님 — H_9103 F3 🟠 NOISE-GRIP(variance-matched noise Δρ=0 EXACTLY·emit-timing byte-identical·urgency std 0.043≪rate-gate band=centering/distribution-driven event).** 재배치된 grip=노이즈 아티팩트지 능력 아니라 어떤 바 리프레임도 clean 🟢 승격 불가. 유일 legitimate 잔여(production stateful-swap+faculty-not-noise pre-reg, ING-b)=설계변경·H_9103 때문 negative 예상·회귀위험=저가치 미발사. **생산적 redirect(다른 축)**: H_9103이 지목한 진짜벽=substrate emit-appropriateness signal 부재(op-grip=centering-noise ⇒ anima에 "언제 emit 적절한가" 판별 substrate 신호 부재), refractory(WHEN-recover)와 직교, consciousness-ops-critique(ops=계기판, 진짜=identity-continuity)와 정합.

## One line
stateless shade → stateful refractory **succeeds as a new mechanism (F2 🟢, stateless-inexpressible)**; and on the same run **H_9101's op-grip does not carry over on its frozen REM bar (F1 🔴, grip relocated to WAKE)** — both honest, no bar move.
