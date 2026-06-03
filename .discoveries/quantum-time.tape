@D quantum_time_orch_or := "ORCH-OR warm-coherence decoheres ~1e9x too fast for the neural window" :: discovery [d=2026-06-04 active]
  seed = "Penrose-Hameroff Orch-OR needs microtubule quantum coherence to survive ~10-25 ms at 310 K brain temperature."
  claim = "warm-wet decoherence ODE gives t_decoher ~1e-11 s vs a generous 25 ms neural window (window/t_decoher ~2.5e9)."
  falsifier = "F-QT1: REFUTED iff t_decoher >= neural_window; CONFIRMED otherwise. Result = CONFIRMED (closed-negative)."
  target = "verdict-tier = 🔴 CLOSED-NEGATIVE (toy decoherence-ODE timescale bound)."
  scope = "TOY CPU $0, a_scale_honest_scope, a_lane_akida_gpu_split CPU toy, p7 direct measurement."
  honest = "Tegmark-style order-of-magnitude estimate, geometric coupling chosen to FAVOUR long coherence; still refutes."
  note = "UNIVERSE/quantum_time_toys.py qt1; .verdicts/quantum-time/F-QT1.txt; dedupe H_183 V8-Q Orch-OR taxonomy."

@D quantum_time_qrng_seed := "QRNG-vs-pseudo noise seed makes no measurable emergence difference (§97-clean)" :: discovery [d=2026-06-04 active]
  seed = "Quantum-collapse-drives-choice: a QRNG-seeded substrate should differ measurably from a pseudo-RNG one."
  claim = "Kuramoto emergence order-r CIs OVERLAP (pseudo 0.983[0.970,0.997] vs qrng-style 0.989[0.974,1.003])."
  falsifier = "F-QT2: REFUTED iff order-r CIs disjoint; CONFIRMED iff overlap. Result = CONFIRMED (closed-negative)."
  target = "verdict-tier = 🔴 CLOSED-NEGATIVE (seed-source identity carries no emergent structure)."
  scope = "TOY CPU $0; §97 QRNG-as-noise-seed only, NOT a command channel; a_scale_honest_scope."
  honest = "no real QRNG hardware; whitened pseudo stream stands in for a QRNG — tests source-identity of equal entropy."
  note = "UNIVERSE/quantum_time_toys.py qt2; .verdicts/quantum-time/F-QT2.txt; connects tool QRNG_SPEC."

@D quantum_time_entanglement := "non-separable coupling integrates more MI than classical-correlated (modelled-only)" :: discovery [d=2026-06-04 active]
  seed = "Entanglement-binds-experience: entangled coupling should beat classical-correlated coupling in big-Phi/MI."
  claim = "non-separable Bell-like joint MI=1.0 bit vs classical common-cause MI=0.098 bit."
  falsifier = "F-QT3: REFUTED iff MI_entangled > MI_classical. Result = REFUTED (HOLDS as modelled)."
  target = "verdict-tier = 🟢 HOLDS (toy MI), with a load-bearing caveat below."
  scope = "TOY CPU $0; a classical sim CANNOT instantiate physical entanglement; a_scale_honest_scope."
  honest = "the entangled arm is a non-separable DISTRIBUTION construct, NOT physical entanglement — not a quantum claim."
  note = "UNIVERSE/quantum_time_toys.py qt3; .verdicts/quantum-time/F-QT3.txt; dedupe H_183 V8-Q complex axis."

@D quantum_time_zeno := "repeated projective measurement freezes substrate drift (mechanistic, not quantum-magic)" :: discovery [d=2026-06-04 active]
  seed = "Quantum-Zeno attention: frequent measurement freezes an evolving state in place."
  claim = "drift falls monotonically free 10.12 -> snap-every-50 1.46 -> every-10 0.28 -> every-2 0.036."
  falsifier = "F-QT4: REFUTED iff drift monotone-down with rate AND frozen<0.5x free. Result = REFUTED (HOLDS)."
  target = "verdict-tier = 🟢 HOLDS (toy projective-snap dynamics)."
  scope = "TOY CPU $0; mechanism is generic repeated-projection, NOT evidence consciousness is quantum; a_scale_honest_scope."
  honest = "the same freezing arises for any repeatedly-projected classical state — measurement dynamics, not quantum."
  note = "UNIVERSE/quantum_time_toys.py qt4; .verdicts/quantum-time/F-QT4.txt."

@D quantum_time_complex_amp := "complex-amplitude rep helps over real-valued on a phase-interference task" :: discovery [d=2026-06-04 active]
  seed = "Superposition-of-percepts: a complex-amplitude state rep should beat a real-valued one where phase matters."
  claim = "complex-amplitude (interference) rep beats real rep by mean +0.439 acc across 3 seeds [0.483,0.43,0.403]."
  falsifier = "F-QT5: REFUTED iff complex_acc - real_acc >= 0.05 over 3 seeds. Result = REFUTED (HOLDS)."
  target = "verdict-tier = 🟢 HOLDS (toy rep ablation)."
  scope = "TOY CPU $0; representation-engineering result (interference features), NOT a quantum-state claim; a_scale_honest_scope."
  honest = "any explicit phase-difference feature captures the same task — not evidence of physical superposition."
  note = "UNIVERSE/quantum_time_toys.py qt5; .verdicts/quantum-time/F-QT5.txt; dedupe H_183 V8-Q complex-valued axis."

@D quantum_time_dilation := "arousal-gain monotonically scales the substrate internal-clock tick rate" :: discovery [d=2026-06-04 active]
  seed = "Subjective-time-dilation: arousal/gain should scale the internal pacemaker clock rate."
  claim = "subjective ticks per fixed objective interval rise monotonically g0.5->64, g1.0->91, g2.0->229."
  falsifier = "F-QT6: REFUTED iff tick-count monotone-up with gain (>=3 levels). Result = REFUTED (HOLDS)."
  target = "verdict-tier = 🟢 HOLDS (toy gain-modulated pacemaker)."
  scope = "TOY CPU $0; classic pacemaker-accumulator interval-timing model, non-paranormal; a_scale_honest_scope."
  honest = "real emergent rate-modulation; toy single-scale, transfer to real ENGINE unverified."
  note = "UNIVERSE/quantum_time_toys.py qt6; .verdicts/quantum-time/F-QT6.txt."

@D quantum_time_phase_clock := "oscillator phase-counting estimates elapsed interval far better than constant-guess" :: discovery [d=2026-06-04 active]
  seed = "Oscillator-phase as internal clock (pure_field): read elapsed time off accumulated phase."
  claim = "phase-inverted estimate MAE=1.696 vs best constant-guess MAE=47.251 (3 seeds)."
  falsifier = "F-QT7: REFUTED iff MAE(phase-clock) < MAE(constant). Result = REFUTED (HOLDS)."
  target = "verdict-tier = 🟢 HOLDS (toy phase-accumulation clock)."
  scope = "TOY CPU $0; ties to pure_field oscillator substrate; a_scale_honest_scope."
  honest = "estimates the MEAN interval well but its error-structure is sub-scalar (see qt11) — both true."
  note = "UNIVERSE/quantum_time_toys.py qt7; .verdicts/quantum-time/F-QT7.txt; counterpoint to qt11."

@D quantum_time_retrocausal := "no future channel — precognition predictor stays at chance (honest paranormal refute)" :: discovery [d=2026-06-04 active]
  seed = "Retrocausal/precognition: information from a strictly-future event should beat a causally-bound predictor."
  claim = "precog accuracy 0.4991[0.4882,0.5100] vs chance 0.5 over 3 seeds of 5000 future coins."
  falsifier = "F-QT8: REFUTED iff precog acc ci_lo > 0.5. Result = CONFIRMED (closed-negative)."
  target = "verdict-tier = 🔴 CLOSED-NEGATIVE (no future channel, as it must be)."
  scope = "TOY CPU $0; the expected honest outcome for a genuine paranormal claim, a_paper_negative_ok."
  honest = "NOT forced to HOLD — chance accuracy is the correct, honest refutation of retrocausation."
  note = "UNIVERSE/quantum_time_toys.py qt8; .verdicts/quantum-time/F-QT8.txt."

@D quantum_time_time_cell := "recurrent leaky-trace state encodes event ORDER above a destroyed-time NULL" :: discovery [d=2026-06-04 active]
  seed = "Time-cell / sequence-memory: a recurrent substrate should encode the ORDER in which events occurred."
  claim = "order-recovery acc 1.0 vs a temporally-destroyed shuffle-NULL 0.165 (~1/6 chance for 6 items)."
  falsifier = "F-QT9: REFUTED iff acc ci_lo > shuffle-NULL hi. Result = REFUTED (HOLDS)."
  target = "verdict-tier = 🟢 HOLDS (toy leaky-trace recurrent state)."
  scope = "TOY CPU $0; ties to clm-time-encoding bench; a_scale_honest_scope."
  honest = "NULL destroys the time->item link so it carries no order — a proper control, not a degenerate one."
  note = "UNIVERSE/quantum_time_toys.py qt9; .verdicts/quantum-time/F-QT9.txt."

@D quantum_time_specious_present := "no clean unimodal optimal integration window — specious-present proxy refutes" :: discovery [d=2026-06-04 active]
  seed = "Specious-present / temporal-integration window: a finite optimal window should beat instantaneous and infinite."
  claim = "matched-filter SNR vs window tau is aliasing-jagged (peak@tau=2, secondary lobe@tau=16, period=20); 0/3 seeds clean."
  falsifier = "F-QT10: REFUTED iff a clean UNIMODAL interior peak in >=2/3 seeds. Result = CONFIRMED (closed-negative)."
  target = "verdict-tier = 🔴 CLOSED-NEGATIVE (no clean optimum in this proxy)."
  scope = "TOY CPU $0; box-average vs sine has aliasing side-lobes — proxy-limited; a_scale_honest_scope."
  honest = "unimodality gate correctly rejects the artifact peak; a band-power/Lomb proxy is the re-design path."
  note = "UNIVERSE/quantum_time_toys.py qt10; .verdicts/quantum-time/F-QT10.txt; links H_213 specious-present analogy."

@D quantum_time_pacemaker := "pacemaker-accumulator reproduces the scalar property (Weber CV) better than oscillator" :: discovery [d=2026-06-04 active]
  seed = "Pacemaker-accumulator vs oscillator models of interval timing: which gives the scalar property (constant CV)?"
  claim = "pacemaker CV near-constant ~0.10 (var 1.88e-5) vs oscillator CV shrinking 0.034->0.008 (var 8.77e-5)."
  falsifier = "F-QT11: REFUTED iff pacemaker CV flatter (lower CV-variance) than oscillator. Result = REFUTED (HOLDS)."
  target = "verdict-tier = 🟢 HOLDS for pacemaker (toy CV comparison)."
  scope = "TOY CPU $0; multiplicative-rate-noise accumulator vs additive-phase oscillator; a_scale_honest_scope."
  honest = "counterpoint to qt7 — phase-clock estimates mean interval well but its error is sub-scalar; both true."
  note = "UNIVERSE/quantum_time_toys.py qt11; .verdicts/quantum-time/F-QT11.txt."
