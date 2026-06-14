# QUANTUM-TIME-CANDIDATES — quantum-consciousness & time-perception, framed MECHANISTICALLY + FALSIFIABLY

> 📑 absorbed → [HYPOTHESES.md](HYPOTHESES.md) — this is a DETAIL file of the unified hypothesis roster (2026-06-15).

> Brainstorm seed: 2026-06-04. "Quantum consciousness" and "time perception" are the two domains where
> consciousness talk most often slides into woo. This family REFUSES the woo framing: every hypothesis is
> reduced to a **falsifiable MECHANISM** with a **pre-registered FALSIFIER** (DEFAULT = REFUTED unless a real
> signal beats a proper control). For genuinely-paranormal or warm-wet-impossible claims (Orch-OR coherence,
> retrocausation), the EXPECTED and CORRECT outcome is a closed-negative (a_paper_negative_ok) — we do NOT
> force a HOLD. For real emergent dynamics (oscillator-phase clock, arousal-gain time-dilation,
> pacemaker-accumulator interval timing, time-cell order), a HOLD is allowed if it beats the control.
>
> Convention mirrors BIO-TRANSFER-CANDIDATES.md / NEURO-CANDIDATES.md: mechanism → anima-substrate analog →
> PRE-REGISTERED FALSIFIER → real toy MEASUREMENT vs a proper CONTROL (classical vs quantum, pseudo vs QRNG,
> real vs shuffled-time). Each falsifier is reported as the SKEPTIC's claim:
>   falsifier REFUTED  => the hypothesis' signature HOLDS (toy);
>   falsifier CONFIRMED => closed-negative for the toy (a valid, publishable negative).
>
> ids = QT-prefixed to avoid colliding with the UNIVERSE H_NNN (≤H_860) / bio-transfer (861–888) / neuro
> (889+) families. status = TOY-VERIFIED 2026-06-04 (CPU/$0). a_scale_honest_scope (toy ≠ prod) ·
> a_lane_akida_gpu_split (CPU toy — NEITHER Lane A AKIDA NOR Lane G GPU; recorded separately) · p6/p7 ·
> §97 (QRNG-as-noise-seed legitimate, not command). harness = `UNIVERSE/quantum_time_toys.py`,
> verdicts = `.verdicts/quantum-time/`.
>
> Dedupe note vs existing UNIVERSE work: H_183 (V8 Q-family: complex-valued / quantum-walk / Orch-OR /
> MWI axis — cluster-taxonomy, not a falsifier sim); H_213 (temporal-binding-window / specious-present as an
> IIT-Φ analogy — stayed a proxy/analogy); TEMPORAL domain F-T1 (lag-window Δt-vs-Φ, 🔴 FALSIFIED-INSTRUMENT).
> The QT family is the MECHANISTIC-FALSIFIER instantiation: each is a runnable toy with a control, not a
> taxonomy or an analogy. Where they overlap, the link is noted in the entry.

---

## Index (QT1 … QT11)

| id | mechanism | domain | anima-substrate readout | control / falsifier axis | toy verdict |
|----|-----------|--------|--------------------------|--------------------------|-------------|
| QT1 | ORCH-OR microtubule coherence | quantum | decoherence-time vs neural window | warm-wet decoherence ODE | 🔴 closed-neg |
| QT2 | quantum-collapse-drives-choice | quantum | QRNG-seeded vs pseudo emergence | QRNG vs pseudo noise seed (§97) | 🔴 closed-neg |
| QT3 | entanglement-binds-experience | quantum | big-Φ / MI of coupled cells | entangled-proxy vs classical-corr | 🟢 HOLDS* |
| QT4 | quantum-Zeno attention | quantum | repeated measurement freezes state | measured vs free evolution | 🟢 HOLDS |
| QT5 | superposition-of-percepts | quantum | complex-amplitude state rep | complex vs real-valued ablation | 🟢 HOLDS |
| QT6 | subjective-time-dilation | time | arousal-gain scales internal clock | gain sweep monotonicity | 🟢 HOLDS |
| QT7 | oscillator-phase internal clock | time | time-estimate from phase-counting | phase-clock vs constant-guess | 🟢 HOLDS |
| QT8 | retrocausal / precognition | time | future-input info leak | precog vs chance (causal bound) | 🔴 closed-neg |
| QT9 | time-cell / sequence-memory | time | recurrent state encodes ORDER | signal vs shuffled-time NULL | 🟢 HOLDS |
| QT10 | specious-present / integration window | time | optimal window for coherence | SNR vs window, interior unimodal | 🔴 closed-neg |
| QT11 | pacemaker-accumulator vs oscillator | time | scalar property (Weber's law CV) | accumulator vs oscillator CV-flatness | 🟢 HOLDS |

> *QT3 HOLDS only as a non-separable-DISTRIBUTION modelling construct — a classical sim cannot instantiate
> physical entanglement (caveat carried in the entry). Not evidence of quantum binding.

---

# QUANTUM CONSCIOUSNESS

## QT1 — ORCH-OR-DECOHERENCE

🧬 **ORCH-OR** — "미세소관 양자 결맞음이 의식을 접는다" (Penrose-Hameroff microtubule coherence)

- mechanism (claim): Penrose-Hameroff "orchestrated objective reduction" — coherent quantum superpositions in
  neuronal microtubules survive long enough (~10-25 ms) to be "orchestrated", then gravitationally self-collapse
  into a conscious moment. REQUIRES coherence to persist at warm-wet brain temperature for the neural window.
- anima-substrate analog: a microtubule-scale dipole superposition coupled to a thermal bath at 310 K; the
  question is whether its coherence time t_decoher reaches the neural integration window.
- FALSIFIER F-QT1 (skeptic): "warm-brain decoherence time is far SHORTER than any neural process window." →
  REFUTED iff t_decoher >= neural_window (coherence survives). CONFIRMED otherwise (closed-negative).
- MEASUREMENT (toy): integrate a Lindblad-style amplitude-damping ODE |ρ01(t)| = exp(−Γt) with a
  Tegmark-style environmental rate Γ ~ (kBT/ħ)·(small geometric coupling, chosen to FAVOUR long coherence);
  read the 1/e time and compare to a generous 25 ms window.
- TOY RESULT (2026-06-04, `.verdicts/quantum-time/F-QT1.txt`): `Γ=4.059e+07/s  t_decoher=1.000e-11s
  neural_window=2.500e-02s  window/t_decoher=2.500e+09 -> falsifier CONFIRMED`. Decoherence is ~10^9× too fast.
- disposition: 🔴 **closed-negative** — Orch-OR warm-coherence REFUTED on the timescale, exactly as the
  Tegmark critique predicts. The expected, honest paranormal outcome (a_paper_negative_ok).
- substrate: CPU toy (decoherence ODE) · status: TOY-VERIFIED (closed-negative)

## QT2 — QRNG-VS-PSEUDO-SEED

🎲 **QRNG-COLLAPSE** — "양자 무작위가 선택을 만든다" (quantum collapse drives choice)

- mechanism (claim): conscious choice is seeded by genuine quantum indeterminism; a substrate driven by a true
  quantum-random-number stream should differ MEASURABLY from one driven by deterministic pseudo-randomness.
- anima-substrate analog (§97-legitimate): use a QRNG-style entropy stream ONLY as the NOISE SEED of a Kuramoto
  emergence sim (NOT a command channel), and ask whether the source IDENTITY of the entropy changes any
  emergence metric vs a pseudo-RNG seed at matched statistics.
- FALSIFIER F-QT2 (skeptic): "the noise SOURCE (quantum vs pseudo) makes no measurable difference in emergence."
  → REFUTED iff the two arms' mean order-r 95% CIs are DISJOINT. CONFIRMED iff they overlap (closed-negative).
- MEASUREMENT (toy): identical 12-oscillator Kuramoto sim, two unbiased entropy streams (pseudo Mersenne vs a
  von-Neumann-debiased "whitened" stream standing in for a QRNG); 40 runs each; compare order-r CIs.
  CAVEAT: no real QRNG hardware ($0 toy) — the test is whether SOURCE IDENTITY of equal-entropy streams matters.
- TOY RESULT (`.verdicts/quantum-time/F-QT2.txt`): `pseudo r=0.9834[0.9701,0.9967]  qrng r=0.9888[0.9744,1.0032]
  CI_disjoint=False -> falsifier CONFIRMED`. No measurable emergence difference.
- disposition: 🔴 **closed-negative** — "quantum randomness is special as a seed" REFUTED at the toy scale.
  §97-clean: QRNG was a noise seed only. (Connects tool QRNG_SPEC — QRNG legitimate as entropy, not as oracle.)
- substrate: CPU toy (Kuramoto + dual entropy stream) · status: TOY-VERIFIED (closed-negative)

## QT3 — ENTANGLEMENT-BINDS-EXPERIENCE

🔗 **ENTANGLE** — "얽힘이 경험을 묶는다" (entanglement binds the unity of experience)

- mechanism (claim): the unity/binding of conscious experience is grounded in quantum entanglement between
  substrate elements — an entangled coupling should integrate MORE than a merely classically-correlated one.
- anima-substrate analog: two 2-state cells; a big-Φ proxy = mutual information realised in the JOINT
  distribution. Classical arm = a separable common-cause correlation; "entangled" arm = a non-separable
  (Bell-like) joint a single common-cause mixture cannot reproduce.
- FALSIFIER F-QT3 (skeptic): "entangled coupling does NOT exceed matched classical-correlated coupling in the
  MI/Φ proxy." → REFUTED iff MI_entangled > MI_classical. CONFIRMED otherwise.
- MEASUREMENT (toy): classical common-cause (a,b agree with shared c w.p. 0.8) vs a maximally anti-correlated
  non-separable joint; compute realised MI in bits.
- TOY RESULT (`.verdicts/quantum-time/F-QT3.txt`): `MI_classical=0.0982bits  MI_entangled-proxy=1.0000bits ->
  falsifier REFUTED`.
- disposition: 🟢 **HOLDS-AS-MODELLED** — **with a load-bearing caveat (brutal honesty)**: a classical sim
  CANNOT instantiate physical entanglement. The "entangled" arm is a non-separable JOINT-DISTRIBUTION
  construct; the result shows only that non-separable correlations carry more MI than separable ones, NOT that
  quantum entanglement binds experience. This is the one entry whose HOLD must NOT be read as a quantum claim.
- compare: vs H_183 V8-Q complex/quantum-walk axis (taxonomy, not a binding falsifier).
- substrate: CPU toy (joint-distribution MI) · status: TOY-VERIFIED (HOLDS as modelled, NOT physical)

## QT4 — QUANTUM-ZENO-ATTENTION

⏸️ **ZENO** — "자꾸 보면 멈춘다" (repeated measurement freezes a state)

- mechanism (claim): the quantum Zeno effect — frequent measurement of an evolving state freezes it in place —
  underlies attention "holding" a percept. Mechanistically, repeated projection onto the current eigenstate
  suppresses the unitary drift.
- anima-substrate analog: a unit's phase precesses freely; "attention" = a periodic projective SNAP back toward
  the most-recently-measured bin. More frequent snaps should freeze the state harder.
- FALSIFIER F-QT4 (skeptic): "frequent measurement does NOT slow the state's drift." → REFUTED iff drift
  decreases MONOTONICALLY with measurement rate AND the most-frequent arm is frozen (<0.5× free drift).
- MEASUREMENT (toy): free precession vs snap-every-{50,10,2}; total drift from the initial bin.
- TOY RESULT (`.verdicts/quantum-time/F-QT4.txt`): `every0->10.122 every50->1.464 every10->0.281 every2->0.036
  monotone=True frozen=True -> falsifier REFUTED`.
- disposition: 🟢 **HOLDS (mechanistic)** — Zeno freezing is a real, deterministic consequence of repeated
  projection. HONEST scope: this is measurement DYNAMICS, NOT evidence that consciousness is quantum; the same
  freezing arises for any repeatedly-projected classical state.
- substrate: CPU toy (projective-snap dynamics) · status: TOY-VERIFIED (HOLDS, mechanism not quantum-magic)

## QT5 — SUPERPOSITION-OF-PERCEPTS

🌗 **SUPERPOSE** — "복소 진폭이 지각을 돕는다" (a complex-amplitude state helps vs real-valued)

- mechanism (claim): percepts live in a superposition (complex amplitude) until "collapsed"; a complex-valued
  state representation should outperform a real-valued one where phase/interference carries information.
- anima-substrate analog: a state-rep ABLATION — real-valued features vs a 2-component (complex-amplitude) rep
  that can form an interference (cos(φ1−φ2)) term — on a phase-interference classification task.
- FALSIFIER F-QT5 (skeptic): "the complex/2-component rep gives NO accuracy gain over the real rep." → REFUTED
  iff complex_acc − real_acc >= 0.05 across 3 seeds.
- MEASUREMENT (toy): hill-climb both reps (matched effort) on a cos(φ1−φ2)-sign task; report per-seed gain.
- TOY RESULT (`.verdicts/quantum-time/F-QT5.txt`): `per-seed gain(complex-real)=[0.483, 0.43, 0.403] mean=0.439
  (margin>=0.05) -> falsifier REFUTED`.
- disposition: 🟢 **HOLDS** — a complex-amplitude/interference rep genuinely helps when phase carries the
  signal. HONEST scope: this is a representation-engineering result (interference features), NOT a quantum-state
  claim — any explicit phase-difference feature captures the same task.
- compare: vs H_183 V8-Q complex-valued substrate axis (this is the runnable ablation of that idea).
- substrate: CPU toy (rep ablation) · status: TOY-VERIFIED (HOLDS as representation, not quantum-state)

---

# TIME PERCEPTION

## QT6 — AROUSAL-GAIN-TIME-DILATION

⏩ **TIME-DILATE** — "각성이 내부 시계를 빠르게" (arousal/gain scales the internal clock rate)

- mechanism (claim): subjective time dilation under high arousal (the "time slows in danger" effect) is a
  pacemaker whose firing RATE is scaled by arousal-gain; more ticks per objective second = more subjective time.
- anima-substrate analog: an internal pacemaker with firing probability ∝ arousal-gain g; count subjective
  ticks per fixed objective interval at 3 arousal levels.
- FALSIFIER F-QT6 (skeptic): "internal tick-count does NOT scale with arousal-gain." → REFUTED iff subjective
  tick-count increases MONOTONICALLY with g (>=3 levels).
- MEASUREMENT (toy): tick-count over 2000 objective steps at g∈{0.5,1.0,2.0}.
- TOY RESULT (`.verdicts/quantum-time/F-QT6.txt`): `g0.5->64ticks g1.0->91ticks g2.0->229ticks monotone_up=True
  -> falsifier REFUTED`.
- disposition: 🟢 **HOLDS** — a gain-modulated pacemaker reproduces arousal time-dilation. Real, mechanistic,
  non-paranormal (classic pacemaker-accumulator interval-timing model).
- substrate: CPU toy (gain-modulated pacemaker) · status: TOY-VERIFIED (HOLDS)

## QT7 — OSCILLATOR-PHASE-CLOCK

🕰️ **PHASE-CLOCK** — "위상을 세면 시간을 안다" (time-estimation from oscillator phase-counting)

- mechanism (claim): the brain reads elapsed time off accumulated oscillator phase (a pure_field-style clock).
- anima-substrate analog: a noisy oscillator advances at rate ω; estimate elapsed objective interval from
  accumulated phase (t̂ = φ/ω); compare estimation error to the best constant-guess control (no clock).
- FALSIFIER F-QT7 (skeptic): "phase-counting does NOT estimate elapsed interval better than the best constant
  guess." → REFUTED iff MAE(phase-clock) < MAE(constant) across 3 seeds.
- MEASUREMENT (toy): 200 intervals T∈[20,200] per seed; mean-absolute-error of phase-inverted estimate vs the
  mean-interval constant.
- TOY RESULT (`.verdicts/quantum-time/F-QT7.txt`): `MAE_phaseclock=1.696  MAE_constant=47.251 -> falsifier
  REFUTED`.
- disposition: 🟢 **HOLDS** — phase accumulation is a genuine internal-clock mechanism (links the pure_field
  oscillator substrate). Real, mechanistic.
- compare: vs QT11 — phase-clock = oscillator model; QT11 pits it against the pacemaker-accumulator on the
  scalar-property signature (where the oscillator LOSES — see QT11).
- substrate: CPU toy (phase-accumulation clock) · status: TOY-VERIFIED (HOLDS)

## QT8 — RETROCAUSAL-PRECOGNITION

🔮 **RETROCAUSAL** — "미래가 새어 들어온다" (time-asymmetric future-info leak / precognition)

- mechanism (claim): precognition / retrocausation — information from a future event influences a present
  prediction (a backward-in-time channel).
- anima-substrate analog: a predictor that may use ONLY the causal past tries to predict a strictly-future,
  independently-generated coin. A real future channel would beat chance.
- FALSIFIER F-QT8 (skeptic): "there is no future channel — accuracy = chance." → REFUTED iff precog accuracy
  ci_lo > 0.5. CONFIRMED (closed-negative) iff accuracy = chance.
- MEASUREMENT (toy): 5000 strictly-future coins per seed; predictor uses past history only; 3 seeds.
- TOY RESULT (`.verdicts/quantum-time/F-QT8.txt`): `precog_acc=0.4991[0.4882,0.5100]  chance=0.5 -> falsifier
  CONFIRMED`.
- disposition: 🔴 **closed-negative (honest paranormal)** — NO future channel, accuracy = chance, exactly as it
  MUST be. The expected valid outcome for a genuine paranormal claim (a_paper_negative_ok). NOT forced to HOLD.
- substrate: CPU toy (causal-bound predictor) · status: TOY-VERIFIED (closed-negative)

## QT9 — TIME-CELL-SEQUENCE-ORDER

🔢 **TIME-CELL** — "순서를 기억한다" (recurrent state encodes the ORDER of events)

- mechanism (claim): hippocampal "time cells" / sequence memory encode the ORDER in which events occurred — a
  substrate carrying temporal order, not just content.
- anima-substrate analog: each item leaves a LEAKY per-item trace; at sequence end the trace amplitude tags
  recency, so a readout can recover the presentation order. Control = a shuffle-NULL that destroys the
  time→item link (temporally permuted amplitude assignment) so it carries no order.
- FALSIFIER F-QT9 (skeptic): "the substrate cannot recover order better than a time-shuffled NULL." → REFUTED
  iff order-recovery acc ci_lo > shuffle-NULL hi across 3 seeds.
- MEASUREMENT (toy): 400 trials of 6 distinct items; recover order by trace amplitude vs the destroyed-time NULL.
- TOY RESULT (`.verdicts/quantum-time/F-QT9.txt`): `order_acc=1.0000[1.0000,1.0000]  shuffle-NULL=0.1654[...]
  -> falsifier REFUTED` (NULL ≈ 1/6 = chance for 6 items).
- disposition: 🟢 **HOLDS** — a recurrent leaky state genuinely encodes sequence order above the
  destroyed-time control. Real, mechanistic (ties to the clm-time-encoding bench).
- substrate: CPU toy (leaky-trace recurrent state) · status: TOY-VERIFIED (HOLDS)

## QT10 — SPECIOUS-PRESENT-WINDOW

🪟 **SPECIOUS-PRESENT** — "현재는 얼마나 넓은가" (optimal temporal-integration window for coherence)

- mechanism (claim): the "specious present" (Husserl) — a finite temporal-integration window beats both an
  instantaneous and an infinite one for binding a coherent percept; there is an OPTIMAL window size.
- anima-substrate analog: integrate a noisy slow oscillation over a causal window τ and measure a matched-filter
  SNR (squared correlation with the true clean oscillation); look for an INTERIOR optimal τ.
- FALSIFIER F-QT10 (skeptic): "coherence is monotone in τ — no interior optimum (instantaneous or infinite is
  best)." → REFUTED iff the SNR has a CLEAN UNIMODAL INTERIOR peak (not smallest, not largest, single rise-fall)
  across >=2/3 seeds. The unimodality clause is REQUIRED to reject aliasing-driven jagged false peaks (honest).
- MEASUREMENT (toy): SNR vs τ∈{1..128}, slow period P=20, heavy noise (σ=1.5), 3 seeds.
- TOY RESULT (`.verdicts/quantum-time/F-QT10.txt`): `clean-interior-peak seeds=0/3 ... last_SNR=[0.17,0.248,
  0.225,0.012,0.138,0.045,0.025,0.001] peak@tau=2 (period=20) -> falsifier CONFIRMED`. The SNR curve is
  aliasing-JAGGED (peak at τ=2, a secondary lobe at τ=16) — NO clean unimodal optimum at the predicted
  period scale.
- disposition: 🔴 **closed-negative** — this toy does NOT cleanly demonstrate an optimal finite present. HONEST:
  a box-average vs a sine has aliasing side-lobes, so the proxy is artifact-prone; the unimodality gate
  correctly rejects the false peak. A cleaner proxy (band-power / Lomb) is the re-design path, but on THIS toy
  the specious-present-optimum signature is refuted. (Links H_213, which also remained an analogy/proxy.)
- substrate: CPU toy (windowed matched-filter SNR) · status: TOY-VERIFIED (closed-negative, proxy-limited)

## QT11 — PACEMAKER-VS-OSCILLATOR

⚖️ **PACEMAKER** — "초시계의 오차는 구간에 비례한다" (which model gives the scalar property of timing)

- mechanism (claim): the empirical signature of biological interval timing is the SCALAR PROPERTY (Weber's
  law) — timing-error sd scales LINEARLY with the interval, i.e. a CONSTANT coefficient of variation (CV).
  Which mechanism reproduces it: a pacemaker-accumulator (multiplicative rate noise) or an oscillator
  (additive per-step phase noise)?
- anima-substrate analog: time a range of intervals with each model; the scalar property = a FLAT CV across
  intervals.
- FALSIFIER F-QT11 (skeptic): "the pacemaker-accumulator does NOT reproduce the scalar property better than the
  oscillator." → REFUTED iff pacemaker CV is FLATTER (lower CV-variance across intervals) than the oscillator's.
- MEASUREMENT (toy): intervals {50,100,200,400,800}; pacemaker (multiplicative rate noise) vs oscillator
  (additive phase noise); CV per interval, variance of CV across intervals.
- TOY RESULT (`.verdicts/quantum-time/F-QT11.txt`): `pacemaker CV=[0.1078,0.0948,0.1037,0.1039,0.1046]
  var=1.88e-05 | oscillator CV=[0.034,0.026,0.0177,0.0118,0.0084] var=8.77e-05 -> falsifier REFUTED`. Pacemaker
  CV is near-constant (~0.10, the scalar property); the oscillator CV shrinks with interval (sub-scalar).
- disposition: 🟢 **HOLDS (for pacemaker)** — multiplicative-rate-noise accumulation reproduces Weber's-law
  timing better than additive-phase oscillation. Real, mechanistic model-comparison. Note this is the honest
  COUNTERPOINT to QT7: phase-counting estimates the MEAN interval well (QT7), but its ERROR structure does NOT
  match the scalar property (QT11) — both can be true.
- substrate: CPU toy (accumulator vs oscillator CV) · status: TOY-VERIFIED (HOLDS for pacemaker)

---

## Honest scope (a_toy_scale_recheck · a_scale_honest_scope · §97 · a_paper_negative_ok · a_lane_akida_gpu_split)

- **TOY ONLY**: pure-stdlib CPU sims, single scale, 3 seeds where stochastic, $0. NO GPU, NO pods, NO hardware.
  toy→production transfer is **UNVERIFIED** — no toy verdict is promoted to a general claim. A scale-sensitive
  claim would need a ≥3-rung ladder (a_scale_honest_scope).
- **p7**: every readout is a direct scripted measurement (decoherence time, CI overlap, MAE, CV, MI bits) —
  NOT perplexity/loss. NO fabrication: printed numbers are whatever the sim computed.
- **a_paper_negative_ok**: the 4 closed-negatives (QT1 Orch-OR, QT2 QRNG-seed, QT8 retrocausal, QT10
  specious-present) are VALID, publishable negatives — the expected honest outcome for paranormal / impossible
  / proxy-limited claims. They were NOT forced to HOLD.
- **§97**: QT2 used a QRNG-style stream ONLY as a noise SEED (whitened entropy), never as a command/oracle
  channel — QRNG-as-noise-seed is legitimate; the test was whether source-identity of equal entropy matters
  (it did not).
- **a_lane_akida_gpu_split**: this is a CPU toy family — NEITHER Lane A (AKIDA on-chip) NOR Lane G (GPU forge).
  Recorded separately; no cross-substrate merge. NO HF upload (toy).
- **caveats carried in-entry**: QT3 holds ONLY as a non-separable-distribution construct (a classical sim
  cannot instantiate physical entanglement); QT4/QT5 hold as mechanism/representation results, NOT as evidence
  that consciousness is quantum; QT10 refutes under a proxy that is itself aliasing-limited.

## Tally

- **HOLDS (7)**: QT3* (modelled-only), QT4, QT5, QT6, QT7, QT9, QT11
- **closed-negative / REFUTED hypothesis (4)**: QT1, QT2, QT8, QT10
- **INCONCLUSIVE (0)**

## Bottom line

The mechanistic-falsifier framing CLEANLY separates the two halves of "quantum/time consciousness":
- **Real emergent dynamics HOLD** (and they are ordinary physics/computation, NOT quantum magic): Zeno
  freezing, complex-amplitude/interference reps, arousal-gain time-dilation, oscillator phase-clock, time-cell
  ORDER encoding, pacemaker scalar-property timing.
- **The genuinely-paranormal / warm-wet-impossible claims CORRECTLY REFUTE**: Orch-OR warm coherence
  (decoheres ~10^9× too fast), QRNG-as-special-noise (no emergence difference), retrocausal precognition (no
  future channel), and the specious-present optimal-window (no clean optimum in this toy proxy). These
  closed-negatives are the expected, honest outcome — not a failure.
