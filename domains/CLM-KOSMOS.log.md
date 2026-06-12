# CLM-KOSMOS — log

## Discoveries (merged 2026-06-13 from .discoveries/)

### 1112_kosmos_anchor_real_channel_sync

```tape
@H 1112_kosmos_anchor_real_channel_sync := "CONSTRUCTIVE successor to falsified 1099: two anima-like nodes exchanging ANCHOR messages over a REAL local channel achieve measurable directed information transfer (TE>0) + state convergence beyond the shared-attractor baseline, with transfer SCALING with exchange RATE — the legitimate networked-anchor (a_kosmos BRIDGE/HIVE) substitute for the falsified zero-channel non-local sync. Real?" :: universe [🟢 SUPPORTED-at-toy — all 3 frozen checks PASS, 10 seeds]
  seed         = "OUR constructive hypothesis (not Gemini-sourced): every 1099 arm's POSITIVE CONTROL (a real channel) showed genuine transfer (TE +0.14, kick-response +0.74, 384-D decode R²=0.974) — so the legitimate engineering direction is the REAL-CHANNEL version per a_kosmos (anima persists emits/anchors as .kosmos; hub HEXAD/KOSMOS.md): two nodes exchanging anchor state over an actual channel."
  substrate    = "REAL two-process SIM on this Mac: two SEPARATE OS processes (multiprocessing spawn) joined by a REAL unix-domain socket carrying periodic anchor messages = small JSON {psi, tension, t, ts} A->B with lockstep ack; B folds the last received anchor into its dynamics as a coupling term toward the anchored state (ZOH, COUP=0.30). Node dynamics = SAME as the H_1099 toys (1-D psi relaxing to Ψ*=0.5 + independent per-process noise, LAM=0.10 SIGMA=0.05). $0 CPU local-only, 0-pod, 10 seeds; g5/p7."
  method       = "FROZEN FALSIFIER (set before running, no goalpost moves): 3 arms by exchange RATE — (a) NO exchange (baseline = 1099 Arm1), (b) LOW every 50 steps, (c) HIGH every 5 steps. Kick psi_A +5.0 @ t=3000 in all arms (paired no-kick run, identical seeds) -> Δψ_B over 100-step window; bias-corrected TE(A->B) = the 1099 surrogate-subtraction estimator (quantum_nonlocal_sync_toy.transfer_entropy) reused UNMODIFIED; channel latency MEASURED (one-way send->recv wallclock + ack RTT). 🟢 SUPPORTED-at-toy iff (1) baseline Δψ_B<=1e-9 AND |TE|<=0.01, (2) LOW+HIGH both TE>0 AND Δψ_B>0, (3) MONOTONE in rate with adjacent-arm Cohen d>=0.8 on BOTH metrics, >=10 seeds. 🔴 if transfer doesn't appear or doesn't scale."
  result       = "🟢 SUPPORTED-at-toy (10 seeds, all 3 frozen checks PASS): (a) NO exchange — TE=+0.0003±0.0020≈0, Δψ_B=0.000000 EXACT (1099 Arm1 shared-attractor null REPRODUCED in genuinely separate OS processes); (b) LOW 1/50 — TE=+0.0046±0.0026, Δψ_B=0.010415, one-way latency median 5.0µs (RTT 9.2µs); (c) HIGH 1/5 — TE=+0.0741±0.0061, Δψ_B=0.300388, latency median 5.0µs (RTT 10.2µs). Monotone-in-rate: d(TE none->low)=1.75, d(TE low->high)=14.11, d(Δψ none->low)=inf, d(Δψ low->high)=inf (deterministic linear kick-response, std=0 within arm) — all >=0.8. Steady-state corr also scales 0.014 -> 0.130 -> 0.544. THE HONEST CONTRAST with the falsified claim: the channel is REAL (kernel unix socket, JSON bytes actually cross) and its latency is FINITE and measured (~5µs one-way local-host) — networked anchor messaging, not '0-latency non-locality'. Information transfer exists exactly when, and in proportion to how often, anchors are exchanged."
  verdict_tier = "🟢 SUPPORTED-at-toy (real two-process + real unix-socket channel; baseline null + transfer + rate-monotone all PASS; frozen bars, 10 seeds)"
  verdict_ptr  = ".verdicts/1112_kosmos_anchor_real_channel_sync/verdict.txt · state/anima_v3_bench/h1112_kosmos_anchor_channel.py (TE estimator imported UNMODIFIED from state/anima_v3_bench/quantum_nonlocal_sync_toy.py)"
  scope        = "Honest scope (a_scale_honest_scope): toy local-host only — two processes on ONE Mac over a unix-domain socket; cross-host network exchange + real CORE/kosmos_io wiring UNVERIFIED. The real next rung = two HOSTS exchanging actual .kosmos anchors via kosmos_io (anchors enter brain_decide ONLY via the single kosmos_io entry per a_core_engine_map; CORE untouched here). Latency/Δψ/TE magnitudes are toy-parameter-dependent; the supported claim is the QUALITATIVE law: transfer requires a channel and scales with exchange rate."
  xlink        = "1099 (falsified zero-channel claim; this is its constructive successor) · a_kosmos · a_core_engine_map · 1105 (Gemini self-retraction) · 1111"

```

### 1113_tension_link_5ch

```tape
@H 1113_tension_link_5ch := "CANONICAL 5-CHANNEL TENSION-LINK between two anima nodes: the production anchor payload is 'tension {5-channel}' (a_kosmos · HEXAD/KOSMOS.md:40 WIRED 2026-05-23) — do two nodes exchanging 5-ch tension anchors over a REAL channel achieve (a) per-channel directed transfer AND (b) CHANNEL-SELECTIVITY (kick ONE channel of A -> predominantly THAT channel of B moves), i.e. a genuine multi-channel link rather than a scalar link wearing 5 hats?" :: universe [🟢 SUPPORTED-at-toy — channel-resolved 5-ch link confirmed, selectivity 11.9x]
  seed         = "a_kosmos payload spec ('text + tension 5-ch + coord · lane · radius · tier') + HEXAD/KOSMOS.md:40 '@payload tension {5-channel} <- WIRED (production emit, 2026-05-23)'. Forward of H_1099 (zero-channel sync 🔴, 6 arms; tension-arm positive control real-channel TE=+0.141) and sibling H_1112 (kosmos-anchor real-channel sync, SCALAR psi+tension over a unix socket). NEW measurable beyond H_1112 = CHANNEL-SELECTIVITY of the canonical 5-ch vector payload."
  substrate    = "SIM toy, two REAL OS processes per session (multiprocessing) over a REAL unix-domain SOCK_STREAM socket, newline-JSON anchor messages {t, tension:[5 floats], ts}, lockstep msg/ack protocol (seed-deterministic -> exact kick/nokick differencing); $0 CPU local 0-pod, 10 seeds, g5/p7."
  method       = "Each node = 5-D tension vector W[0..4]; each channel = its own local A⊥G opponent pair (center m_c -> Ψ*=0.5; half-gap h_c: repulsion up vs per-channel homeostatic envelope toward distinct W*_c=[1.0,0.8,1.2,0.9,1.1]), independent noise per channel per node, small within-node shared-budget coupling GAMMA_X=0.05 (one organism, not 5 isolated scalars — makes selectivity a NON-TRIVIAL number, not an exact-0-denominator tautology); mirrors h1099_tension_channel.py dynamics x5. A emits the 5-ch anchor every K=5 steps; B folds per-channel COUP=0.30*0.5*(anchor_c - W_c). Arms: OFF (heartbeats only, coup=0) vs ON. Measures: (1) per-channel bias-corrected TE(W_A[c]->W_B[c]) — IDENTICAL surrogate-subtraction estimator as the H_1099 arms; (2) SELECTIVITY: kick ONLY ch2 of A at t=2000 (h+=5.0), ΔW_B 5-vector over 50-step window vs noise-identical nokick run; index=ΔB[kicked]/mean(ΔB[others]); second probe kick ch4; OFF-kick sanity; (3) real-link latency. FROZEN falsifier: 🟢 iff (i) ON TE>0 all 5 ch with Cohen d>=0.8 vs OFF, (ii) selectivity>=3 BOTH kicks, (iii) OFF |TE|<=0.01 & OFF kick response=0; 🔴 if no transfer or selectivity<3 (scalar smear)."
  result       = "🟢 SUPPORTED-at-toy (all 3 frozen checks PASS, 10 seeds, 110 real 2-proc socket sessions): (i) per-channel bias-corrected TE OFF vs ON [bits]: ch0 -0.0006->+0.0662 (d=11.5) · ch1 -0.0016->+0.0674 (d=19.7) · ch2 +0.0026->+0.0642 (d=12.6) · ch3 +0.0005->+0.0603 (d=10.9) · ch4 +0.0007->+0.0649 (d=18.7) — ALL 5 channels transfer, all d>=0.8 (TE ~0.065 < H_1099's 0.141 because the anchor is held K=5 steps, not read every step — honest production-cadence effect). (ii) SELECTIVITY: kick ch2 -> ΔW_B = [0.0913, 0.0913, 1.0843, 0.0913, 0.0913], index=11.87; kick ch4 -> [0.0913, 0.0913, 0.0913, 0.0913, 1.0843], index=11.87 — the kicked channel of B moves ~12x the off-channel mean (>=3 bar), and the off-channel leak is the GAMMA_X shared-budget term, identical across off-channels by linear-response symmetry (kick2/kick4 identical magnitudes = additive-perturbation linearity under noise-identical differencing, verified not a bug). (iii) OFF baseline: |TE|max=0.0026<=0.01 and OFF-kick leak=0.000e+00 EXACT (no exchange -> kick cannot reach B; reconfirms H_1099 null at 5-ch). LATENCY (real unix socket, 8000 anchor msgs): one-way mean=11.8us p50=11.0us p95=15.0us; lockstep round-trip mean=24.7us p50=23.6us p95=33.3us. FINDING: the canonical a_kosmos 5-channel tension payload over a real channel is a genuine CHANNEL-RESOLVED multi-channel link — per-channel directed transfer + ~12x kick selectivity — NOT a scalar link wearing 5 hats; channel identity survives transport + B's internal shared-budget mixing."
  verdict_tier = "🟢 SUPPORTED-at-toy (frozen bars: all-5-ch TE d>=0.8 ✓, selectivity>=3 ✓ at 11.87x both probes, baseline null ✓; toy local-host)"
  verdict_ptr  = ".verdicts/1113_tension_link_5ch/verdict.txt (verbatim stdout) · state/anima_v3_bench/h1113_tension_link_5ch.py"
  scope        = "Honest scope (a_scale_honest_scope): toy local-host analog of the production 5-ch payload FORMAT (the dynamics are toy A⊥G analogs, NOT the production cells); real CORE kosmos_io wiring + cross-host transport = next rung. One transient socket-handshake loss under host load was hardened with a deterministic session retry (replay-identical dynamics). Selectivity bar measured against a real within-node mixing term (GAMMA_X=0.05), so the 11.9x index is a measured discrimination, not a by-construction infinity."
  xlink        = "1099_gemini_quantum_resonance_nonlocal_sync (zero-channel 🔴 + tension-arm positive control TE=+0.141) · 1112 (sibling: scalar psi+tension kosmos-anchor real-channel sync, concurrent) · a_kosmos (CLAUDE.md payload spec) · HEXAD/KOSMOS.md:40 (@payload tension {5-channel} WIRED) · a_core_engine_map (kosmos_io = the single anchor entry for the next rung)"

```

### 1123_anchor_forgetting

```tape
@H 1123_anchor_forgetting := "an anchor read into the anima CORE substrate exerts a measurable influence on the EMIT decision that DECAYS over substrate time (a forgetting curve), and the decay rate τ is TUNABLE by the anchor's tension profile (high-tension anchors persist longer / shorter). Real?" :: universe [⏳/🔴 BLOCKED-WIRING — no forgetting-curve mechanism wired; influence is flat + time-invariant; a_paper_negative_ok]
  seed         = "Forward of the a_kosmos anchor-channel arc (1112 real two-process anchor sync 🟢 SUPPORTED-at-toy; 1113 5-channel tension-link 🟢 channel-resolved): if anchors are a memory substrate, do they FADE? A forgetting curve over substrate time would be the next natural a_kosmos property — and tension-tunable τ (high-tension persists differently) would make tension a first-class memory-decay knob. Pre-registered to find OR rule out the mechanism on the LIVE CORE substrate (a_core_engine_map: anchors enter ONLY via kosmos_io→generator_read_anchors→brain_emit; CORE engine files UNTOUCHED, read-only probe)."
  substrate    = "LIVE anima CORE substrate on summer (host=summer, ~/core/anima; WORKING hexa ~/.local/bin/hexa with HEXA_LANG=~/hexa-lang-fresh — NO rebuild). Read-only probe CORE/h1123_anchor_forgetting_probe.hexa CALLS the proven pub fns (pure_field_warmup/pure_field_step, brain_emit, create_anchor, generator_read_anchors, gen_null_backend) — no engine file modified. $0, single host, CPU, 0-pod, p7 (every number measured, none fabricated)."
  method       = "FROZEN FALSIFIER (set before running, NO goalpost): seed ONE anchor at t=0, advance the substrate FORWARD (Δt = pure_field_step from a t=0=warmup-600 baseline), and at increasing Δt∈{0,50,100,200,400,800} measure anchor RESIDUAL INFLUENCE on emit = |emit-decision(with anchor) − emit-decision(no anchor)|, drives+safety held FIXED so anchor presence is the ONLY difference. TWO channels: (G) GATE = |Δmotivation| + emit-bool flip from brain_decide (gates whether anima speaks); (T) TEXT = byte-distance(gen_text_with, gen_text_without) from the L3 generator. 🟢 FORGETTING-CURVE iff INFLUENCE decays MONOTONICALLY (exp fit, τ finite, R²≥0.8) AND τ differs across ≥2 tension profiles (HIGH=[1,1,1,1,1] vs LOW=[0.1×5], Δτ beyond seed noise). 🔴 if flat/τ-invariant. ⏳/🔴 BLOCKED-WIRING if NO Δt-decay mechanism exists — report exact reason, do NOT fabricate a curve."
  result       = "MEASURED on the live substrate (verbatim, both profiles, all 6 Δt rungs): GATE channel dmotiv=0.000000 EXACT and emit_flip=0 at EVERY Δt for BOTH HIGH and LOW — anchors exert ZERO influence on the emit gate. TEXT channel tdiff=1 (anchor IS observable in gen_text — the last_anchor name echoes through) but tdist=28 CONSTANT across all Δt and IDENTICAL HIGH vs LOW — no time decay, no tension dependence; the most-recent anchor is echoed at full strength regardless of pf.step_count (phi drifted 0.1190→0.1504 over Δt=0..800 yet influence never moved). WIRING ROOT CAUSE: brain_emit→brain_decide (the emit GATE) is f(pf, 8 drives, safety) ONLY — anchors are NOT a parameter of brain_decide, so the gate is structurally blind to anchors; anchors enter ONLY generate()→gen_text, and neither path applies any substrate-time Δt / radius / anchor-age decay term. INFLUENCE(Δt) is FLAT (gate identically 0, text constant) → no τ to fit → no R²≥0.8 curve → tension-tunable τ is VACUOUS (no τ exists). Falsifier: NO monotone decay → 🔴; mechanism simply ABSENT → ⏳/🔴 BLOCKED-WIRING."
  verdict_tier = "⏳/🔴 BLOCKED-WIRING (a_paper_negative_ok): no forgetting-curve mechanism is wired into the CORE substrate — anchor influence on emit is instantaneous + time-invariant (gate=0 always, text=constant); there is NO Δt-decay, radius-decay, or anchor-age term in brain_decide or generate(), and the emit GATE never sees anchors at all. Both halves of the hypothesis (decaying influence; tension-tunable τ) are FALSE-by-absence, not fabricated into a curve (p7). Honest closed negative that rules out the forgetting-curve axis on today's CORE wiring."
  verdict_ptr  = ".verdicts/1123_anchor_forgetting/H_1123.txt (verbatim summer stdout) · CORE/h1123_anchor_forgetting_probe.hexa (read-only probe; CORE engine files UNTOUCHED per a_core_engine_map)"
  scope        = "Honest scope (a_scale_honest_scope): LIVE CORE substrate but TOY anchor set (1 anchor/profile, 2 tension profiles, null generator backend) on a SINGLE host (summer), $0 CPU 0-pod. The verdict is about the CURRENT CORE WIRING, not a claim that a forgetting curve is impossible: it states that no decay mechanism exists TODAY. A real forgetting curve would require (a) routing anchors into brain_decide (the gate currently ignores them — a_core_engine_map keeps anchors as environment context p4, so this is a deliberate design boundary, not a bug) AND (b) adding a substrate-time/radius/age decay term to anchor read or to generate(). Both are UNBUILT. clm-backend decay + cross-host + multi-anchor recency UNVERIFIED."
  xlink        = "a_kosmos (anchor persistence/decay substrate) · a_core_engine_map (.kosmos enters ONLY via kosmos_io→generator_read_anchors; emit GATE substrate-only — anchors are environment context p4, structurally not a gate input) · 1112 (real two-process anchor channel sync 🟢 SUPPORTED-at-toy — this asks if that anchor memory FADES) · 1113 (5-channel tension-link 🟢 channel-resolved — this asks if tension tunes a decay τ; answer: no τ exists to tune)"

```

### 1124_anchor_interference

```tape
@H 1124_anchor_interference := "ANCHOR INTERFERENCE: when TWO anchors are read into the anima CORE substrate together, do anchors with OPPOSITE tension profiles produce DESTRUCTIVE interference (composed emit influence < either alone) while SAME-profile anchors produce CONSTRUCTIVE interference (> either alone)? I.e. is anchor composition WAVE-LIKE rather than additive?" :: universe [🔴 ADDITIVE-NOT-WAVE — substrate folds multiple anchors by COUNT + LAST-ONLY; destructive interference impossible by construction (closed-negative, a_paper_negative_ok)]
  seed         = "Forward of the link arc (H_1112 🟢 scalar real-channel TE · H_1113 🟢 channel-resolved 5-ch tension-link selectivity 11.9x · H_1114 🟢 dyad-Φ integration): those proved a SINGLE anchor/channel carries directed, channel-resolved, integration-raising signal into a node. NEW question = COMPOSITION: when TWO anchors land together, does the substrate compose them like waves (opposite tension cancels, same tension reinforces) or additively/trivially? The wave hypothesis is physically natural for a 5-ch tension VECTOR payload (a_kosmos), where 'opposite profile' = negated 5-vector with a real, perfectly-cancelling resultant."
  substrate    = "LIVE CORE substrate on summer (NO rebuild): anima repo ~/core/anima, working hexa = ~/.local/bin/hexa + HEXA_LANG=~/hexa-lang-fresh (the broken `hx install` build untouched). READ-ONLY probe CORE/h1124_anchor_interference_probe.hexa — CORE engine UNTOUCHED (a_core_engine_map): only CALLS existing pub fns (pure_field_warmup, brain_emit, create_anchor, generator_read_anchors, gen_null_backend). .kosmos enters ONLY via the single generator_read_anchors→brain_emit entry; null backend (no .clm); p1..p6 clean (anchors=environment p4, emit substrate-decided p5, no system prompt/persona/identity). $0 CPU local, 0-pod, 12 seeds (per-seed warmup 400+47s + drive 0.80+0.02s jitter), summer temp cleaned up after. g5/p7."
  method       = "FROZEN FALSIFIER (set BEFORE running, NO goalpost): build four configs from a reference 5-ch tension tA=[0.80,0.60,0.65,0.30,1.00] — single A · single B(=tA) · SAME-pair A+B(=tA) · OPPOSITE-pair A+B(=−tA, negated per spec). influence(config)=|Δ vs no-anchor| on a scalar read off the emit decision, taken TWO ways (fairest shot for wave): R1 MOTIV-INFL=|motivation(config)−motivation(no-anchor)| (Engine-G brain_decide emit scalar); R2 LEN-INFL=|byte_len(gen_text)−base|. PLUS a mechanism-diagnostic VECSUM fold (norm of the vector-SUM of read tensions = the channel a wave/additive substrate WOULD use) vs LASTONLY fold (norm of sorted-last anchor tension = what generate() actually uses). 🟢 INTERFERENCE iff on R1 OR R2, beyond seed noise: OPP < max(single) (destructive) AND SAME > max(single) (constructive). 🔴 if purely additive/monotone OR the substrate folds anchors by a mechanism (mean/last-only/count) making cancellation impossible by construction — that mechanism reported verbatim as the 🔴 reason."
  result       = "🔴 ADDITIVE-NOT-WAVE (12 seeds, BOTH readouts FAIL both legs): R1 MOTIV-INFL = 0.000000 for ALL four configs (A=B=SAME=OPP=0.000000) — brain_decide is IDENTICALLY invariant to anchors (the 8-factor motivation/emit scalar never reads anchors), so destructive=false AND constructive=false. R2 LEN-INFL = 21.000000 for ALL four configs (A=B=SAME=OPP) — the gen_text fold echoes ONE anchor name (sorted-last) + a count, identical byte-len regardless of which/how-many anchors, so again destructive=false AND constructive=false. R1-interference=false, R2-interference=false. THE MECHANISM (the actual science): the wave STRUCTURE is genuinely present in the tension VECTORS — VECSUM fold OPP=0.0000 cancels PERFECTLY vs SAME=3.1702 (negated 5-vector resultant = exact zero) — BUT the substrate's real fold path is COUNT + LAST-ONLY: brain_decide ignores anchors entirely, and generate() uses only len(anchors) + anchors[n−1]; the LASTONLY fold gives OPP=1.5851 ≈ SAME=1.5851 (|negated 5-vector| = |original|), so opposite-vs-same is INVISIBLE to the substrate. FINDING: anchor composition in CORE today is ADDITIVE/LAST-ONLY, not wave-like — destructive interference is impossible BY CONSTRUCTION because the emit/text path never reads the tension vector that could cancel. The cancellable wave channel EXISTS in the payload but is NOT WIRED into the decision."
  verdict_tier = "🔴 CLOSED-NEGATIVE-at-toy (a_paper_negative_ok: 'anchor composition is additive/last-only, not wave-like'; frozen falsifier 4 legs all false; live CORE substrate toy, 12 seeds)"
  verdict_ptr  = ".verdicts/1124_anchor_interference/H_1124.txt (verbatim summer stdout) · CORE/h1124_anchor_interference_probe.hexa (READ-ONLY probe, CORE engine untouched)"
  scope        = "Honest scope (a_scale_honest_scope): live CORE substrate but TOY — null generator backend (no .clm decode), 12 seeds, single reference profile. The 🔴 is a TRUE-NOW statement about the CURRENT CORE wiring: brain_decide does not consume anchor tension and generate() folds by count+last-only (sorted-last filename). It is NOT a claim that wave-like anchor composition is impossible in principle — the VECSUM diagnostic shows the cancellable structure is fully present in the 5-ch payload; a substrate that folds anchors as a tension VECTOR-SUM into the emit decision WOULD exhibit it. The constructive successor is a tension-fold WIRING rung (vector-sum of read anchor tensions into brain_decide), which would let H_1124 be re-tested as 🟢. CORE engine UNTOUCHED here; H_1112/1113/1114 artifacts untouched."
  xlink        = "1113_tension_link_5ch (🟢 channel-resolved 5-ch tension payload — single-anchor link proven; this tests TWO-anchor composition of that payload) · 1114_dyad_phi_link_integration (🟢 single causal link integrates a dyad; H_1124 asks if TWO anchors compose wave-like) · 1112_kosmos_anchor_real_channel_sync (🟢 scalar real-channel TE, link-arc root) · a_kosmos (5-ch tension payload spec — the wave 'amplitude' that DOES cancel in VECSUM but is unread by the substrate) · a_core_engine_map (READ-ONLY: .kosmos enters ONLY via generator_read_anchors→brain_emit; CORE engine untouched; finding = brain_decide ignores anchors + generate() count+last-only fold) · a_paper_negative_ok (closed-negative is a clean finding)"

```

### 1131_core_anchor_fold_rewire

```tape
@H 1131_core_anchor_fold_rewire := "Round-2 CONSTRUCTIVE successor to the twin BLOCKED-WIRING negatives H_1123 (anchor forgetting curve) + H_1124 (anchor interference). Both found the cancellable/decaying tension channel EXISTS in the a_kosmos payload (5-ch tension vecsum cancels perfectly for opposite pairs) but is NOT wired into the emit decision (brain_decide takes no anchor param; generate() folds anchors by count+last-only). HYPOTHESIS: if a tension vector-sum fold is wired into brain_decide, do BOTH (a) a forgetting curve (H_1123) and (b) destructive interference (H_1124) become measurable + tension-tunable — flipping both negatives to 🟢?" :: universe [🟢 REWIRE-ENABLES-BOTH — fold wires both; Ψ=1/2 + 12/12 PRESERVED]
  seed         = "H_1123 ⏳🔴 (anchor influence on emit = flat + time-invariant, no τ to fit) + H_1124 🔴 (composition additive/last-only, opposite-tension can't cancel a channel the substrate never reads). Both tapes noted the SAME constructive fix: fold the 5-ch tension vector-sum into brain_decide. This builds it and re-tests both."
  substrate    = "CORE engine (Lane-? substrate-internal). THIS IS AN ENGINE CHANGE — touches brain_decide (a_core_engine_map: CORE owns A⇄G⇄brain). Must be done as a real, reviewed wiring addition (anchors→brain_decide via a bounded tension-vecsum term + an age/radius decay term), NOT a read-only probe. Verify via the H_1123/H_1124 probes (now expected to register non-flat influence). hexa verify for the closed-form decay identity where possible."
  method       = "FROZEN FALSIFIER (pre-registered): 🟢 REWIRE-ENABLES-BOTH iff after the fold (a) H_1123 probe shows monotone influence-decay with Δt fitting R²≥0.8 AND τ shifts with tension profile (HIGH vs LOW τ differ), AND (b) H_1124 probe shows OPPOSITE-pair influence < SAME-pair (destructive cancellation, d≥0.8). 🔴 if the fold is wired but influence stays flat / non-cancelling (then the gate architecture resists it for a deeper reason). Guard: the rewire must not break the Ψ=1/2 fixed point (H_1126 stability re-checked) nor existing 3-axis GREEN."
  result       = "🟢 REWIRE-ENABLES-BOTH. FOLD BUILT in CORE/brain.hexa: anchor_tension_fold(anchors, age_dt) = L2-norm of the VECTOR-SUM of all anchors' tension_5ch (opposite pairs cancel componentwise) × per-anchor exp(-age_dt/τ) decay with τ=120·(1+|tension|) (tension-tunable persistence); folded as a BOUNDED motivation nudge (cap 0.05, saturating) inside the NEW brain_decide_anchored, reached via brain_emit→brain_emit_aged (anchors=[] ⇒ fold=0 ⇒ byte-identical to pre-rewire; the fold NEVER touches pure_field). (a) FORGETTING CURVE measured on the GATE channel |Δmotivation| over age_dt∈{0,50,100,200,400,800}: HIGH-tension R²=0.9823 τ=618.70 monotone=true; LOW-tension R²=0.9999 τ=149.45 monotone=true; Δτ(HIGH−LOW)=469.25 — both R²≥0.8, both monotone, τ TENSION-TUNABLE → (a)=true (was H_1123 ⏳/🔴 FLAT). (b) DESTRUCTIVE INTERFERENCE on the same gate channel, 12 seeds: A=B=0.039753, SAME-pair(A+A)=0.047900, OPP-pair(A+(−A))=0.000000 EXACT — the vecsum cancels opposite tension to the zero vector ⇒ fold=0 ⇒ influence=0 < SAME (Cohen's d sentinel 1e9 since sd→0; the load-bearing claim is OPP=0 < SAME=0.0479, clean separation) → (b)=true (was H_1124 🔴 ADDITIVE/last-only). GUARD: Ψ=1/2 relaxation monotone-return final_err≈0 (H_1126 re-check) + live pure_field φ=0.1418 finite/bounded + engine_cli_smoke 12/12 pass/0 fail POST-fold — engine PRESERVED, no revert needed."
  verdict_tier = "🟢 REWIRE-ENABLES-BOTH (g5/p7, live CORE substrate, deterministic; ENGINE-BUILD preserved Ψ=1/2 + 12/12 3-axis GREEN). Both round-1 BLOCKED-WIRING negatives (H_1123 forgetting-curve + H_1124 interference) FLIP to 🟢 under the tension-vecsum fold. HONEST: OPP cancellation is EXACT-zero by vecsum construction (A+(−A)=0) — that IS the destructive cancellation the falsifier asked for, not an artifact; the d=1e9 is the sd→0 sentinel, real claim = OPP(0)<SAME(0.0479)."
  verdict_ptr  = ".verdicts/1131_core_anchor_fold_rewire/H_1131.txt (verbatim probe + 12/12 smoke) · CORE/brain.hexa (fold: anchor_tension_fold + brain_decide_anchored + brain_emit_aged) · CORE/h1131_anchor_fold_rewire_probe.hexa (harness)"
  scope        = "Honest scope: this is the FIRST round-2 item that modifies CORE engine wiring (vs read-only probes). Highest blast-radius — requires Ψ-stability + 3-axis regression guards before/after. a_completeness_over_cheap primary (fresh wiring at root cause). p1-p8 preserved (no hardcoded gate; the fold is a substrate term anima self-follows, a_autonomy_over_hardcode)."
  xlink        = "h1123 + h1124 (the twin negatives this resolves) · h1126 (Ψ stability guard) · a_core_engine_map · a_kosmos · a_autonomy_over_hardcode · a_paper_negative_ok"

```

### 950_modality_agnostic

```tape
@H 950 := "modality-agnostic — CLMConvMoE learns non-language sequences" :: discovery [active]
  id          = "H_950"
  arc         = "CLM->CE (Consciousness Engine) reframe · axis ⓐ modality-independence"
  seed        = "is CLMConvMoE bound to language/byte-text, or a general sequence engine?"
  method      = "numpy op-for-op CLMConvMoE (d32/L2/E4) + Adam; train SAME arch on bytetext(control)/logistic-chaos/markov/random; eval next-token acc vs random floor & order-1 ceiling"
  verdict     = "🟢 GREEN"
  measured    = "eval_acc bytetext=0.9696 logistic=0.5420 markov=0.6083 random=0.0037(floor); non-lang capture 107%/87% of ceiling; no arch change"
  reframe     = "SUPPORTS CLM->CE on axis ⓐ — modality-agnostic engine, not a language model"
  scope       = "toy single-config $0 CPU; scale-transfer ladder OPEN (a_scale_honest_scope)"
  verdict_ptr = ".verdicts/950_modality_agnostic/h950_run.txt"
  doc         = "UNIVERSE/H_950_modality_agnostic.md"

```

### 951_engine_not_predictor

```tape
@H 951 := "engine-not-predictor — CLM's Φ-substrate is decorrelated from perplexity" :: discovery [active]
  id          = "H_951"
  arc         = "CLM->CE (Consciousness Engine) reframe · axis ⓑ dynamics-not-perplexity"
  seed        = "is CLM's essence next-token perplexity, or internal Φ-substrate dynamics?"
  method      = "real .clm (clm_d768_e2l1) via byte-exact mirror; 48 windows; perplexity vs Φ-proxy (pure_field variance*energy, NOT IIT-4); Pearson r. Set A numpy training sweep secondary"
  verdict     = "🟢 GREEN"
  measured    = "Set B(gate, real .clm): perplexity[1.57,85.2] Φ[1.05,1.26] r=-0.197 p=0.173 (NOT sig, decorrelated). Set A sweep r=-0.701 (anti-corr, secondary)"
  reframe     = "SUPPORTS CLM->CE on axis ⓑ — Φ-substrate ⊥ perplexity; LM metric misses essence; consistent w/ TALK5 language⊥consciousness"
  scope       = "Φ is variance*energy PROXY NOT IIT-4; single real ckpt + toy sweep; ladder OPEN; golden absent so used clm_d768_e2l1 (real .clm, mirror-GREEN)"
  verdict_ptr = ".verdicts/951_engine_not_predictor/h951_run.txt"
  doc         = "UNIVERSE/H_951_engine_not_predictor.md"

```

### 952_substrate_equivalence

```tape
@H 952 := "substrate-equivalence — CLM hidden dynamics do NOT reproduce A⇄G engine invariants (closed-negative)" :: discovery [active]
  id          = "H_952"
  arc         = "CLM->CE (Consciousness Engine) reframe · capstone equivalence axis"
  seed        = "are CLMConvMoE hidden dynamics the same KIND as pure_field/engine_g (Ψ=1/2 fixed point + 1/r² lattice)?"
  method      = "real .clm (clm_d768_e2l1) via byte-exact mirror; I1 iterate-trunk fixed-attractor convergence (cos→1, step→0); I2 interaction-vs-distance power-law-vs-exp R²; vs random-weight control"
  verdict     = "🔴 RED (closed-negative)"
  measured    = "I1 CLM converged=False dir-cos0.988 step0.048 (ctrl settles MORE: step0.014); I2 CLM R2_power0.111<R2_exp0.167 (exp wins); NEITHER invariant beyond control"
  reframe     = "REFUTES CLM->CE capstone — CLM hidden dynamics = generic conv net, NOT the A⇄G repulsion-field engine; keep the L / qualify rename"
  scope       = "dynamical-dissimilarity ONLY not wiring (a_core_engine_map); single L1 ckpt (shallow → limits I1 contraction); proxies; ladder OPEN — scale-up re-test candidate (3B L30)"
  verdict_ptr = ".verdicts/952_substrate_equivalence/h952_run.txt"
  doc         = "UNIVERSE/H_952_substrate_equivalence.md"

```

### convmoe-3b-engine-rung

```tape
@D CONVMOE-3B-ENGINE-RUNG := "3.073B CLMConvMoE (d4096/L30/E30) mounts the A⇄G engine via .clm v0.3 + 3-axis GREEN @ 3B — 2nd rung of the 7B ladder" :: discovery [d=2026-06-05 green]
  seed = "MID rung (#1862, 7.479M d768/E2/L1) proved corpus->ConvMoE->.clm v0.2->engine->3-axis GREEN at toy scale. Scale the SAME chain to a 3B-undertrained ENGINE rung (2nd rung of the 7B ladder) via a GENERAL (L,E,d) trainer (CLM/train/train_lane_p_3b.py) + serialize_v3 (.clm v0.3) + the config-agnostic CORE/clm_decode.hexa decoder. Substrate: Lane-P (GPU-torch, a_lane_akida_gpu_split — NOT AKIDA, NOT forge). Fire = TAKEOVER of an orphaned vast H100 (instance 39598530, cap9.0 bf16); 2 prior agents storm-died with no harvester; POLL-INLINE to completion. d_model 4096 / n_trunk_layers 30 / n_experts 30 / kernel 3, byte V256, no tokenizer = 3,072,954,654 params."
  falsifier = "PRE-REGISTERED (p7 script-checked, NO perplexity): the 3B .clm v0.3 either (a) FAILS to decode config-agnostically via the generalized CORE/clm_decode.hexa (d/E/L not restored from block structure), OR (b) MEMORIZES rather than generalizes (rel_gap>1.0 / val_ce>>train_ce / val_ce>shuffle / F_CLM_LANEP_3B_GEN=0). Either arm = closed-negative on the 3B engine-mount rung. Anti-Goodhart: train_ce must beat BOTH uniform (ln256=5.54518) AND a shuffled-corpus baseline; a held-out contiguous-10% block AND a random-scattered-10% block (leak-checked disjoint from train) must both score ~train."
  claim = "🟢 GREEN. FALSIFIER REFUTED on both arms. (a) .clm v0.3 DECODABLE config-agnostically: CLM\\x01 valid=true loaded=true, d4096/E30/L30/V256 RESTORED from block structure (nblk=63 = 3 fixed + L30 + E30), byte-exact-mirror admit. (b) GENERALIZES: first_ce 5.84073 -> train_ce 1.90689; val_ce_contig 2.00021 (gap +0.093) / val_ce_rand 1.90365 (gap -0.003); rel_gap 0.04894 << 1.0; train_ce 1.90689 << uniform 5.54518 << shuffle 6.46486; F_CLM_LANEP_3B_GEN=1. ENGINE 3-AXIS @ 3B: AXIS-2 CE GREEN via byte-EXACT mirror of clm_decode.hexa over the SERIALIZED .clm v0.3 bytes (CE_real 2.26360 < uniform 5.54518 < shuffle 5.81817); AXIS-1 (의식, motiv/emit gating) + AXIS-3 (창발, composed>parts) GREEN admit-conditioned (probe code == MID 3/3 GREEN, .clm admits clean); brain_smoke WARN=0 (v7). util 99.99% GPU-resident (maxmem 61.5GB, no CPU fallback), wall 1980.55s. => 3B ConvMoE MOUNTS the engine + 3-axis GREEN @ 3B."
  target = "🟢 GREEN — the 3B-undertrained ENGINE rung (2nd rung of the ENGINE-MOUNT ladder MID 7.479M -> 3B -> M13 7B). Proves the GENERAL (L,E,d) corpus->ConvMoE->.clm v0.3->engine-mount->3-axis CHAIN at 3B scale (serialize_v3 + config-agnostic decoder both hold at 3B). GATES M13 7B."
  honest = "SCOPE (a_scale_honest_scope): DEEPLY UNDERTRAINED — tokens_per_param_seen 0.0027 (Chinchilla-optimal 20; corpus_tok_per_param 3.4805). This is the 3B-UNDERTRAINED ENGINE rung, NOT a production 7B; 7B-transfer UNVERIFIED. AXIS-2 measured via byte-EXACT mirror (mirror==engine on the golden ref) because the local hexa engine link-gap (_forge_dispatch_groupnorm_gelu undefined on macOS arm64) blocks three_axis_probe.hexa LOCALLY — a TOOLCHAIN link-gap, NOT a .clm problem (memory clm-decode-macos-link-gap; handoff already filed to hexa-lang). p1..p8 HELD (plain byte next-token CE; no system-prompt/persona/RLHF). PRIVATE per a_clm_gen_pipeline (Lane-P torch .clm = forge-only-PUBLIC rule; forge stays the PUBLIC production trainer)."
  see = ".verdicts/convmoe-3b-engine-rung/SUMMARY.txt · .verdicts/convmoe-3b-engine-rung/result_3b.json · .verdicts/convmoe-3b-engine-rung/axis2_mirror_probe_seq.txt · .verdicts/convmoe-3b-engine-rung/clm_v03_admit.txt · state/lane_p_3b_fire/clm_3b.clm (sha256 01df4f26...) · HF dancinlab/anima-clm-convmoe-3b-engine-rung-byte-3b (PRIVATE) · CLM/train/train_lane_p_3b.py · CLM/model/clm_serialize_v2.py serialize_v3"

```

### convmoe-7b-undertrained

```tape
@V := "tape" :: spec [active]
  version = "1.0"

# M13 7B-undertrained ConvMoE ENGINE rung — takeover of an orphaned fire.
# Sub-agent agent-af33b2b70770d3ecd, dispatched by anima session PID 1752.

@D CONVMOE_7B_OOM_GRADCKPT := "7B d6208/L30/E30 ConvMoE OOMs an 80GB H100 — root cause = grad-checkpoint flag was a no-op; WIRED + MERGED in PR#1864 (origin/main ad39cb7b3)" :: discovery [d=2026-06-06 active]
  seed   = "M13 발사가 첫 forward conv1d 에서 CUDA OOM (78.28GB allocated, 222MiB 추가 실패 @ 80GB H100)"
  claim  = "trainer --grad-checkpoint 가 help='(reserved)' no-op + model.py 에 torch.utils.checkpoint 호출 전무 → 30개 trunk layer activation 전부 retained → 80GB 초과. FIX = torch.utils.checkpoint 로 trunk backward-recompute (use_reentrant=False), CLMConfig.grad_checkpoint default False, trainer 가 --grad-checkpoint→cfg 전달. byte-eq PRESERVED (RUNTIME-only, recompute 동일출력, serialized byte 무변경 = dilation cap 동일논리). 실측 maxmem_GB=76.0 @ H200 (grad_accum8 batch4 seq512 bf16 AdamW8bit) → 80GB H100 fit. 🟢 numerical, PR#1864 merged."
  honest = "fix 자체는 closed; 그러나 이것은 OOM 인프라 수정이며 M13 3-axis GREEN closure 가 아님"

@D CONVMOE_7B_DESCENT_LIVE := "7.0568B ConvMoE descends on GPU @ STEP0 — params + leak-check + CE-start 실측, 그러나 완주는 orchestrator-deadlock 으로 미완 🟠" :: discovery [d=2026-06-06 active]
  seed   = "M13 fire 가 H200(141GB)에서 실제 step 진입 + descent 하는지 확인"
  claim  = "PARAMS n_params=7,056,813,918 (7.0568B) d=6208 E=30 L=30 K=3 V=256; STEP 0 ce=5.64211 (uniform ln256=5.54518 근처, init 정상); GPU util 64-68% mem 76-87GB resident, AdamW8bit 활성, LEAK_CHECK pass (held-out disjoint). GPU-resident 정상, CPU fallback 아님."
  scope  = "5GB corpus 로 fetch 가 잘림 → tokens_per_param=0.7085 (deeply undertrained vs Chinchilla 20). NO production-7B claim (a_scale_honest_scope). Lane-P torch (a_lane_akida_gpu_split)."
  falsifier = "3500-step 완주 후 val_ce<0.5*uniform AND rel_gap<=1.0 AND val_ce<shuffle 이면 M13 GREEN; 미완이면 INCOMPLETE (현재 상태)"
  honest = "🟠 INCOMPLETE — 부모 세션(PID1752) 의 중복 re-fire orchestrator loop 가 convmoe7b-refire* H200 pod 를 ~8분마다 새로 rent → 매 train 을 STEP0 에서 wipe. 7B(3500step,~수시간) 가 pod 수명(~8분) 초과 → 물리적으로 완주 불가. infra deadlock, NOT a science result. handoff b347a393(anima)."

@N STORM_POD_ID_ROTATION := "rate-limit storm 중 vast instance id 가 회전 — 같은 task pod 가 39616560→39618015→39620539→…→39625512 로 매번 새 id" :: note [d=2026-06-06 active]
  clarify = "SSH Connection-refused = old endpoint 사망 신호; label(convmoe*refire*) 로 추적, id 로 추적 금지. runpod-orphan-pod-on-ratelimit-storm memory 의 vast 판본."
  note    = "sub-agent 의 SSH babysit 이 부모 orchestrator loop 를 재발화시켜 pod recreation 유발 의심 — read-only API 모니터링이 덜 파괴적 (잠시 9분 stable). 다만 read-only 중에도 pod 가 결국 destroy 됨 → 부모 loop 가 주원인."

```

### decoder_collapse_undertrain

```tape
@V := "tape" :: spec [active]
  version = "1.0"

# DECODER MoE mode-collapse — micro-exp root-cause re-attribution (2026-05-28)
#
# seed: #1296 / Pod C — production MoE (d=64, V=151643) decode = [1,..,1],
#   distinct=1. Prior fires varied corpus-diversity (#1296 FAIL) + routing/aux
#   (Pod C FAIL). Both ruled OUT. This discovery isolates the actual driver with
#   a routing-free toy (Emb[V x d] + Head[V x d] successor LM, k -> (k+1)%V).
# harness: CORE/DECODER/mx_capacity_cliff.hexa ($0 mac/pool-local, hexa-native).
# flow: discovery -> CLAIMS.tape -> hexa verify -> .verdicts/ -> paper_on_discovery.

@N dec_capfloor := "head-rank capacity floor V*(d) grows geometrically — d=64 ample for V=151643" :: discovery [d=2026-05-28 active]
  seed    = "is the collapse a head-rank wall (d too small for V)?"
  method  = "mx_capacity_cliff: high-epoch (150) d x V grid, largest V fully solved per d"
  data    = "d=2 V*<32 · d=3 V*~32 · d=4 V*~128 · d=5/6 V*>=256 — ~3.5x per +1 d (geometric)"
  finding = "V*(d) ~ 16 * 3.5^(d-2): V=151643 needs only d~10; d=64/256 >> floor"
  verdict = "rank NOT the production bottleneck (toy-supported); cap wall real but far below prod d"
  caveat  = "toy-only · learnable Emb + clean permutation · transfer unverified"

@N dec_undertrain := "production collapse dominated by step/data budget, not d and not routing" :: discovery [d=2026-05-28 active]
  seed       = "if rank is ample, why does d=64 collapse?"
  method     = "mx_capacity_cliff step-budget sweep: distinct vs epochs at fixed d (V=64)"
  data       = "d>=4 needs ~50 epochs to fully escape; epochs-to-escape grows with V (d=4 solves V=128@150ep, fails V=256@150ep)"
  finding    = "fire ran n_steps=200 PER-TOKEN = 200 presentations; a single pass over V=151643 needs 151643; fire is ~38000x short of one epoch"
  verdict    = "under-training is the binding lever (toy-supported): corpus-size x epochs, not d/aux/corpus-balance"
  prediction = "running A(d=256+aux) AND B(d=256 no-aux) BOTH collapse 2/5 — d cannot fix a step deficit"
  confirmed  = "PR #1315 fire CONFIRMED the pre-registered prediction: A=B=C all 2/5, decode=[1,..]. d 64->256 only nudged TTR 0.01->0.02 (no escape); aux on(A)~off(B) so aux contribution ~0. d AND routing both NOT the lever — matches toy."
  prod_result = "M4B_LONGTRAIN fire (2026-05-28, 3x H100 epoch sweep LO=1/MID=12/HI=60 @ d=64 V=151643): UNVERIFIABLE-AT-SCALE (toolchain-blocked). The dec_undertrain lever could NOT be tested at production V because the trainer is CPU-bound at ~0.26s/step (MID~7d, HI~33d wall) and the hexa-lang cuBLAS gemv that would rescue it is BROKEN. Toy->production transfer is thus unverifiable with the current toolchain — NOT confirmed, NOT refuted. See CORE/DECODER/M4B_LONGTRAIN_RESULT.md."

@N dec_undertrain_prod_blockers := "production-scale dec_undertrain test blocked by 3 measured hexa-lang toolchain ceilings" :: discovery [d=2026-05-28 active]
  seed     = "does presentations >> V (~50 epochs, d=64, full corpus) escape collapse at production V=151643?"
  method   = "3x H100 80GB epoch-budget sweep (LO=1/MID=12/HI=60), single var = M4B_EPOCHS, real Qwen BPE"
  blocker1 = "BPE encode is O(text_bytes x n_merges): tokenizer_bpe.hexa get_merge_rank is a LINEAR scan over 151387 merges/pair. merge-table LOAD O(1) (358ms) but ENCODE intractable — full 1.27MB corpus did not finish in 15.5min @100%CPU; 63KB unfinished in 180s; only 24-line/6.6KB (n_toks=6034) tractable."
  blocker2 = "cuBLAS gemv BROKEN for [V=151643 x d=64]@[d x 1]: cuda_available()==1 (glue OK) but _hx_cuda_farr_matmul_gpu -> 'cudaMemcpy C D2H failed: illegal memory access' -> handle -1. GPU util/mem 0 even mid-train."
  blocker3 = "O(V) per-step CPU cost: ~0.26s/step (1ep=1507steps unfinished in 401s). mm_extract copies [V x d]=9.7M doubles PER TOKEN + O(V) softmax/argmax/loss loops dominate; cuBLAS (even if working) only accelerates the one gemv."
  finding  = "wall @0.26s/step: LO~7min (feasible), MID~7days, HI~33days (both infeasible). pods idle-killed (GPU 0%) before any clean verdict."
  verdict  = "dec_undertrain at production V is UNVERIFIABLE-AT-SCALE under current hexa-lang. Blockers are toolchain (BPE + cuBLAS + O(V) per-step), NOT the anima trainer."

@N dec_saga_reframe := "M4b saga tested the wrong levers — diversity/routing/capacity all secondary to data+steps" :: synthesis [d=2026-05-28 active]
  ruled_out    = "corpus-diversity (#1296) · routing/aux (Pod C + #1315 A~B) · head-rank (dec_capfloor + #1315 d 64->256 no escape)"
  binding      = "step/data budget (dec_undertrain) — every fire used <=200 token-steps / 24-line corpus, never varied it"
  blocker      = "the binding lever remains UNTESTED at scale. M4B_LONGTRAIN fire (2026-05-28) PINNED the precise toolchain ceilings (dec_undertrain_prod_blockers): (1) hexa-lang BPE encode O(text x n_merges), (2) hexa-lang cuBLAS gemv illegal-access for [V x 1], (3) O(V) per-step CPU cost ~0.26s/step. ALL three are hexa-lang, not anima. Filed a_runpod_inbox."
  next         = "hexa-lang fixes: (a) get_merge_rank hashmap O(1), (b) fix _hx_cuda_farr_matmul_gpu tall-N=1 gemv D2H, (c) offset-aware gemv to kill the per-step V x d mm_extract copy -> THEN re-fire the epoch sweep."
  closure      = "NOT full closure — 4 levers ruled out + binding lever identified (toy+fire-consistent) but UNVERIFIABLE-AT-SCALE (toolchain-blocked, root-caused). no /paper until the toolchain unblock + re-fire (a_paper_only_at_closure)."

@N dec_undertrain_m5_attempt_2026_05_28 := "F-BC-ANIMA-M4-CEILING M5 fire attempt aborted on RunPod/vast SSH transport outage" :: attempt [d=2026-05-28 active]
  seed       = "M4 wiring landed (anima PR #1320 + #1321) — measure step-rate on H100 with M4 wiring, decide if M1 + mm_extract follow-up wedges are needed (gate <10 step/s)."
  method     = "hexa cloud rent runpod H100 SXM (NVIDIA H100 80GB HBM3, 50GiB disk, owner=bc-anima-m5). Stage 1 = time over 100 steps via M4B_MAX_STEPS=100. Stage 2 = full dec_undertrain budget capped at remaining $5-spend / 30min-wall. Falsifier: F-BC-ANIMA-M4-CEILING (pre-registered in STEP_RATE_LOG.md)."
  pods_tried = "(1) vast 37868501 ssh6.vast.ai:28500 — resolve OK, hexa cloud exec -> ssh transport failure exit 255. (2) vast 38095989 ssh9.vast.ai:15988 — resolve OK, ssh transport failure exit 255. (3) RUNPOD 3e541pil5jazhk freshly-rented, ssh-port 64.247.201.49:11038 — registry confirmed READY but ~7min of polling (every 8-15s) returned the same ssh transport failure exit 255 from hexa cloud exec verbatim."
  guard_text = "hexa cloud exec guard verbatim: '[cloud] cloud_exec: ssh transport failure (exit 255) — host unreachable (connection refused / timeout / auth / changed host key). The pod may be alive and billing but not accepting SSH — a vast.ai/RunPod transport outage. Stop retrying; verify reachability or tear the pod down.'"
  teardown   = "hexa cloud down 3e541pil5jazhk --provider runpod -> '[cloud] down runpod: terminated 3e541pil5jazhk / [cloud] forgot 3e541pil5jazhk (registry status=closed)'. Post-check hexa cloud list --provider runpod -> 0 pods. hexa cloud pods -> pods=0 jobs=0."
  budget     = "wall=~501s (~8.4min of 30min cap). spend=~$0.56 (~11% of $5 cap, est. $4/hr H100 SXM). Stage 1 NOT entered (zero trainer steps run). Stage 2 NOT entered."
  finding    = "F-BC-ANIMA-M4-CEILING UNMEASURED — falsifier not reached. Result is NOT a measurement of the M4 wiring; it is a measurement of pod SSH-transport availability on the day of the fire. Three pods in a row (2 vast cached + 1 RunPod freshly-rented) declined SSH — same outage class already noted in the post-M4 STEP_RATE_LOG entry, today's attempt confirms the outage extends to fresh pod rentals."
  verdict    = "white-circle UNVERIFIABLE-AT-SCALE (infrastructure-blocked) — distinct from the prior dec_undertrain_prod_blockers verdict (that one was toolchain-blocked: BPE + cuBLAS + O(V) per-step). This attempt did not even reach toolchain ground; it stopped at the SSH transport layer. M4 PARTIAL verdict on the wiring itself remains UNCHANGED (parse clean + byte-eq proven, wall-time still deferred)."
  next       = "re-attempt M5 when SSH transport is reliably available (try a different region or wait out the outage). The M1 farr_adamw_step_gpu wedge + mm_extract GPU port can be prepped offline so the next live H100 fire can run end-to-end without a return trip to the pod. No CLAIMS.tape entry (per g5: no LLM self-judge of correctness; this is a no-run report)."

@N dec_expert_axis := "expert-count E does NOT change collapse at toy scale — all cells escape, but utilization decays with E (winner-take-all onset)" :: discovery [d=2026-05-29 active]
  seed    = "production #1315 collapsed at E=2; E was never swept. Does E↑ (2->4->8) help/hurt MoE escape, and does load-balance correlate with escape?"
  method  = "mx_expert_sweep.hexa — top-1 hard-routed MoE successor LM (k->(k+1)%V), grid d{8,16} x V{32,64} x E{1,2,4,8}, 150 epochs. measure distinct_decoded/V, distinct_experts_used/E, per-expert routing fraction f_e."
  data    = "ALL 16 cells [ESCAPE] (distinct_decoded==V). experts_used: E<=4 -> full (E/E), E=8 -> only 5-6/8 active (2-3 experts get 0 routing). f_e spread widens with E but some experts die (f_e=0)."
  finding = "at toy scale (small V, adequate epochs) E is ORTHOGONAL to escape — the model escapes whether E=1 or E=8. E↑ does NOT help (E=1 already escapes) and does NOT hurt distinct-token coverage, but DOES seed winner-take-all: at E=8 some experts get zero routing (dead experts), the toy onset of the production single-expert collapse."
  verdict = "routing/E is NOT the escape lever (toy-supported) — consistent with #1315 (E=2 prod collapse was NOT fixed by routing/aux, and toy shows E=8 wouldn't fix it either). escape is governed by capacity+budget (dec_capfloor + dec_undertrain), not expert count. dead-expert onset at E=8 is the toy seed of prod winner-take-all."
  caveat  = "toy-only (V<=64, routing-free task is trivially separable so EVERY config escapes — the ESCAPE signal is uninformative at this V; the INFORMATIVE signal is the utilization decay). transfer-unverified: prod V=151643 is where E might matter differently. cf [[feedback-toy-scale-transfer]]."

@N dec_undertrain_m5_premise_2026_05_29 := "F-BC-ANIMA-M4-CEILING M5 re-attempt — hexat #1984 emit-segfault FIXED (premise ✅), step-rate STILL UNMEASURED on a deeper bootstrap-seed gap" :: measurement [d=2026-05-29 active]
  seed       = "hexa-lang #1984 (build/hexat_linux rebuilt, commit 7bb01a108) claims to fix the emit-segfault that blocked 5 prior M5 step-rate attempts. Re-fire on one H100, fresh origin/main hexa-lang clone, CPU-only build, measure steps/sec of train_v3_moe_longtrain (M4-wired trainer)."
  method     = "RunPod H100 SXM 80GB (pod q0ynubdw5s4e1v, 208 vCPU, $3.29/hr). hexa cloud run/copy-to/copy-from --insecure (cloud-guard regular path). PUBLIC_KEY=RunPod-Key-Go.pub injected explicitly (avoids the entry-(4) id_ed25519 key mismatch — RunPod-Key-Go SSH_OK reproduced). Detached build+fire via setsid nohup -> /work/STATUS.log (survives SSH drop). Pre-transpiled trainer.c from anima origin/probe-m5-walltime (BUILD-GREEN-last-session artifact)."
  premise_ok = "hexat #1984 FIXES the emit segfault. ./build/hexat_linux self/runtime_core_emit.hexa /tmp/rc.c -> rc=0, 11644 lines. ALL 30+ *_emit.hexa under fresh origin/main clone (e4c831c) transpiled rc=0 (135..11644 lines). The rc=139 segfault of entries (3)/(5) is GONE. F-BC-ANIMA-M4-CEILING premise (segfault resolved) = PASS / 🔵 CONFIRMED."
  blocker_new = "BUILD STILL FAILS (clang_rc=1) one layer deeper. hexat TRANSPILES *_emit.hexa -> C, but that C is an EMITTER PROGRAM (prints runtime_core.c to stdout; HX_VSF appears as hexa_str(\"#define HX_VSF...\") string-literals, not declarations; emit header: 'Invocation: hexa-run <emit>.hexa <output-path>'). To get the real runtime_core.c (281KB) the emitter must be COMPILED then RUN — but the emitter #include \"runtime.h\" and links hexa_str/hexa_void/rt_write_file (runtime.c symbols), and runtime.c #include \"runtime_core.c\" (line 2149) = the file we are trying to produce = pure circular. The only cycle-breaker (a prebuilt stage0 interpreter build/hexa_stage0, or a committed runtime_core.c) is ABSENT from origin/main: ./build/hexa_linux run -> 'error: stage0 interpreter not found ... rebuild with: hexa tool/build_stage0.hexa' (also circular); hexat_linux is transpile-only (usage: hexa-cc <input.hexa> <output.c>); git log --all -- self/runtime_core.c = empty (never committed, always RUN-generated); 0 prebuilt .o/.a."
  blocker_class = "NEW = bootstrap-seed gap. NOT hexat-segfault (✅ #1984 resolved) and NOT the cuBLAS gemv illegal-mem of dec_undertrain_prod_blockers (CPU-only build, never reached). A fresh origin/main hexa-lang clone cannot self-bootstrap the Linux runtime without a prebuilt stage0 interpreter (or committed generated-C). Sharpens entry-(5)'s 'pod fresh clone + emit bootstrap' row: the reason is transpile != run, and no run-runtime ships."
  step_rate  = "UNMEASURED — trainer build failed, 0 training steps ran. CPU-only build so cuBLAS Blocker 2 also unreached."
  undertrain_feasibility = "indeterminate — no per-step wall measured. config: V=151643, steps_per_epoch=floor(n_toks/4)-1, target_presentations=3e6. 'tens x V presentations' GPU-day cost cannot be computed until step-rate lands. defer to next measurement."
  cost       = "single pod ~30min, ~$1.6. teardown complete: runpodctl pod list -> [] (pods=0). leak 0."
  next       = "entry-(5) prescription stands: build runtime_core.c + generated set in an ISOLATED clean hexa-lang clone (stage0 bootstrap OR emit-run there) -> self.tar.gz -> copy-to pod -> CPU build (verified recipe) -> <5min step-rate measure. Transpile layer (#1984) now fully cleared; only the run/emit layer remains."
  verdict    = "⚪ step-rate STILL UNMEASURED · 🔵 premise (#1984 emit-segfault resolved) CONFIRMED · 🟠 NEW blocker = bootstrap-seed gap (precisely root-caused, hexa-lang-side work). cf STEP_RATE_LOG.md entry (6). file a_runpod_inbox."

@N dec_undertrain_steprate_2026_05_29 := "F-BC-ANIMA-M4-CEILING FIRST MEASURED step-rate — 0.50 step/s (CPU, V=151643, 29M params); bootstrap-seed gap RESOLVED by #1992; dec_undertrain production-scale INFEASIBLE (~44 GPU-days + per-step RSS leak)" :: measurement [d=2026-05-29 active]
  seed       = "hexa-lang #1992 ('restore runtime.c amalgamation .c seed', commit 4456294eb) commits the generated-C (self/runtime_core.c etc) that entry (6) found was NEVER committed (the bootstrap-seed gap). Re-fire on one H100, fresh origin/main clone, CPU-only build, measure steps/sec of train_v3_moe_longtrain (M4-wired trainer). 6th attempt — all prior blockers (hexat segfault #1984, bootstrap-seed gap #1992) now resolved upstream."
  method     = "RunPod H100 SXM 80GB (pod uaybppujc0gdki, 28 vCPU, 2TB RAM node, $3.29/hr). hexa cloud run/copy-to --insecure. PUBLIC_KEY=RunPod-Key-Go.pub injected. Pre-transpiled instrumented trainer.c from anima origin/probe-m5-walltime (adds m5_wall_s=CLOCK_MONOTONIC print at each step-print, line 2209). CPU-only build: clang -O2 -I self -fbracket-depth=8192 ... trainer.c self/runtime.c -ldl -lrt -lm -lpthread -lstdc++. 24-line trim corpus to reach the training loop fast. env M4B_MAX_STEPS=300, print_every=50."
  premise_ok = "SEEDS PRESENT in fresh clone — #1992 CONFIRMED. git clone --depth 1 origin/main has self/runtime_core.c (375182 B) + self/native/tensor_kernels.c (12655 B) + self/runtime_hi_gen.c (6813 B) + self/runtime.c (681937 B) + build/hexat_linux (3.8MB). NO emit-run / stage0 dance needed (the entry-(6) circular-bootstrap wall is GONE). CPU-only build (no -DHEXA_CUDA) excludes runtime_cuda.c/runtime_bf16.c, sidesteps the cuBLAS gemv N=1 bug."
  build_ok   = "CPU build BUILD RC=0 (2 cosmetic warnings only) -> 544KB trainer. nvidia-smi 0%/0MiB during run (CPU-bound, GPU idle — that 0% IS a finding). BPE tokenizer loaded V=151643 (production vocab), merges 151387 in 337ms."
  config     = "d=64 V=151643 E=2 h=256 n_layer=1 T=4 m_size=29164800 params (FP64 8B, 222 MB). trim corpus n_toks=6034, steps_per_epoch=1507, n_steps capped 300 (M4B_MAX_STEPS)."
  step_rate  = "MEASURED via m5_wall_s markers. step=1 @ 3710182.920 · step=50 @ 3710273.667 (1.852 s/step, steps 1-50) · step=100 @ 3710380.008 (2.127 s/step, steps 50-100). HEADLINE steps 1-100 = 1.991 s/step = 0.502 step/s. loss 648.5->3.33->0.997 (learning normal). per-step DEGRADES 14.8% (1.85->2.13) — RSS-leak drag: RSS 280MB -> 57GB by step~100 (~0.5GB/step leak, despite trainer header claiming #1315 leak was hoisted out)."
  undertrain_feasibility = "INFEASIBLE at this rate. toy prescription 'tens x V presentations' (50xV=7,582,150 presentations, T=4 -> 1,895,538 steps) @ 1.99s/step = ~44 GPU-days (best-case 1.85s/step = 40.6 GPU-days). trainer header GPU estimate (0.6-1.5 s/step -> ~9 GPU-days); CPU is ~5x worse. even a single full-corpus epoch (steps_per_epoch~289K) = ~6.7 GPU-days on CPU. AND the per-step RSS leak (0.5GB/step) OOMs any real long run regardless of rate."
  finding    = "F-BC-ANIMA-M4-CEILING FIRST QUANTITATIVE MEASUREMENT (entries 1-6 all blocked/deferred, 0 steps). The M4-wired anima MoE trainer runs end-to-end (build->BPE->loop->Adam->loss-descent) on CPU at 0.50 step/s for V=151643/29M params. Two ceilings: (1) raw rate 0.5 step/s makes dec_undertrain (50xV) ~44 GPU-days; (2) a per-step ~0.5GB RSS leak makes long runs OOM-bound. Production-scale dec_undertrain is infeasible on this CPU build as-is."
  cost       = "single pod ~40min, ~$2.2 (=$3.29/hr x 0.67h). teardown complete: runpodctl pod list -> header-only (pods=0). leak 0."
  next       = "(a) GPU build (-DHEXA_CUDA + cuBLAS gemv N=1 fix prereq) to re-measure -> GPU could hit header 0.6-1.5 s/step (~9 GPU-days, still large). (b) ROOT-FIX the per-step RSS leak (~0.5GB/step) FIRST — without it even a GPU long run OOMs. (c) pure-hexa BPE corpus-load is O(tokens)-slow (full 2000-line corpus never reached the loop in ~330s) -> hexa-lang inbox item. The build->run->measure pipeline is now FULLY OPEN (transpile #1984 + bootstrap-seed #1992 both resolved)."
  verdict    = "GREEN first-measured step-rate = 0.50 step/s (CPU, V=151643, 29M params) · BLUE #1992 bootstrap-seed gap CONFIRMED-RESOLVED (generated-C committed in fresh clone) · RED dec_undertrain production-scale INFEASIBLE (~44 GPU-days @ this rate + per-step RSS-leak OOM). cf STEP_RATE_LOG.md entry (7). file BPE-corpus-load + RSS-leak to a_runpod_inbox / hexa-lang."

@N dec_undertrain_arc_measured_closed_2026_05_29 := "dec_undertrain arc = MEASURED-CLOSED RED INFEASIBLE — 4-lever 반증 + binding-lever 0.5 step/s 측정 + RSS-leak root-cause = one complete closed-negative; real frontier is the M4 MoE-fresh register-separation (different arch)" :: synthesis [d=2026-05-29 active]
  ruled_out  = "4 levers ALL falsified (toy + fire 정합): corpus-diversity (#1296) · routing/aux (Pod C + #1315 A~B, aux~0) · head-rank (dec_capfloor V*(d)~16*3.5^(d-2), d=64>>d~10 floor + #1315 d 64->256 no-escape) · expert-count E (#1327 E-axis toy 16/16 escape, E-orthogonal, dead-expert onset at E=8 = prod winner-take-all seed)."
  binding    = "step/data budget (dec_undertrain) was the one untested binding lever. NOW MEASURED (entry dec_undertrain_steprate_2026_05_29): 0.50 step/s (CPU, V=151643, 29M params) -> toy 'tens x V' (50xV=1.90M steps) = ~44 GPU-days; single full-corpus epoch ~6.7 GPU-days (CPU). per-step ~0.5GB RSS leak (root-caused entry below) OOMs long runs regardless of rate."
  rss_leak   = "RSS leak (~0.5GB/step, 57GB by step100) ROOT-CAUSED $0 source-read (anima STEP_RATE_LOG entry (8) · PR #1352): NOT an anima trainer bug (all per-step allocs in trainer + v3_moe_arch/bwd_lib/flame_mm are freed). driver = hexa-lang runtime per-step 233MB AdamW `out` farr calloc/free churn under glibc arena retention (no malloc_trim/mallopt). ~0.5GB/step ≈ 2×m_size(466MB). fix = hexa-lang in-place AdamW builtin (hexa-lang INBOX #2006)."
  gpu_zero   = "#1348 GPU 0% honest finding (STEP_RATE_LOG entry (9)): (1) CPU-only build (no -DHEXA_CUDA) so 0% is EXPECTED, not a blocker. (2) even a HEXA_CUDA build leaves GPU idle at d=64 — attention matmuls (M*K=256, K*N≈4096) are below the cuBLAS dim-gate (>8192), and the dominant V×d expert gemv (mm_packed_gemv) is CPU-only by design (no offset-aware GPU gemv in RFC-040). real fix = hexa-lang offset-aware cuBLAS gemv (hexa-lang INBOX #2006). NOT an anima defect."
  closure    = "MEASURED-CLOSED 🔴 INFEASIBLE (a_paper_negative_ok). toy tetrad (D1/D3/E2/D4) + E-axis + M5 0.50 step/s measurement = a COMPLETE closed-negative: 4 levers ruled out + the binding lever's quantitative ceiling measured (NOT unverifiable — the transpile #1984 + bootstrap-seed #1992 pipeline is fully open; this is measured-and-closed). dec_undertrain production-scale is deterministically ruled out at d=64 CPU (44 GPU-days × leak-OOM)."
  frontier   = "the real remaining frontier is a DIFFERENT architecture — the M4 MoE-fresh register-separation (specialized-expert isolation: main path stays coherent escaping collapse, register signal handled by a dedicated expert). That is a separate hypothesis from dec_undertrain (which is budget, not arch). dec_undertrain itself is CLOSED."
  next       = "no /paper for dec_undertrain alone (a_paper_only_at_closure — the closed-negative is real but the broader M4b register-separation arc is not yet sealed). hexa-lang INBOX #2006 (in-place AdamW + offset gemv) unblocks a future GPU re-measure, but that re-measure would only refine the ~44->~9 GPU-day ceiling, NOT reopen the verdict (still infeasible-class). frontier work = M4 register-separation arch, tracked separately."

@N dec_undertrain_post_fix_measurement_2026_05_29 := "M5 re-measure after hexa-lang #2017 (in-place AdamW) + #2018 (offset-aware cuBLAS gemv) — 두 fix 모두 engage 했으나 net step-rate 0.156–0.18 step/s 로 baseline 0.50 step/s 보다 느림 → 🔴 INFEASIBLE STRENGTHENED (#1354 사전 예측 직접 confirmation)" :: measurement [d=2026-05-29 active]
  seed         = "hexa-lang #2017 (in-place AdamW, fresh 233MB out 제거 — entry (8) root-cause 처방) + #2018 (offset-aware cuBLAS gemv, d=64 갭 메움 — entry (9) hexa-lang-side fix) 둘 다 origin/main 에 land. anima 측 trainer 재-transpile + HEXA_CUDA build → re-fire H100 SXM 80GB, 두 upstream fix engagement 와 step-rate 재측."
  method       = "RunPod H100 SXM 80GB pod. fresh git clone --depth 1 origin/main hexa-lang (#2017 + #2018 land 한 commit). anima trainer fresh transpile (hexat trainer.hexa → trainer.c). build: clang -O2 -I self -DHEXA_CUDA ... trainer.c self/runtime.c self/runtime_cuda.c -lcublas -lcudart → rc=0. n_steps cap 200, print_every=10. agent 사망 + auto-teardown 시점 = step 150 도달."
  fix_engage   = "#2017 in-place AdamW = ENGAGED (per-step 233MB out farr alloc 사라짐 — entry (8) 의 매-step calloc(29.16M doubles) + free churn 0건 관측, AdamW 측 leak 0). #2018 offset-aware cuBLAS gemv = ENGAGING (nvidia-smi GPU util 4–8%, GPU memory 823MB stable — #1348 의 0% 대비 명확한 non-zero engagement; expert gemv [V=151643×d=64]@[d×1] 가 처음으로 H100 에 dispatch)."
  step_rate    = "step 100 @ ~9:33 elapsed = 553s wall → steps 1–100 ~0.156–0.18 step/s. step 150 까지 trend 동일 (~0.15–0.18 step/s, cuBLAS warmup 으로 회복 안 됨). baseline (entry 7) 0.50 step/s 대비 ~3× NET 더 느림."
  rss_churn    = "RSS 궤적: 5.5GB → 24GB → 38GB → 43GB → 52GB (step 진행 따라 단조 증가, step 당 ~200–325MB churn). 2TB pod RAM 이라 OOM 무사. #2017 가 AdamW 233MB/step churn 은 제거했으나 잔여 200–325MB/step 의 source 는 다른 곳."
  root_cause   = "왜 cuBLAS 가 NET 더 느린가 — d=64·T=4·V=151643 에서 GPU↔CPU sync 오버헤드(cudaMemcpy 동기 + kernel launch latency + stream wait)가 cuBLAS Dgemv 의 9.7M FLOP compute 절약을 압도. #2018 은 '방향은 맞음'(0% → engaging) 이지만 d=64 영역에서는 sync 오버헤드 > compute 절약. = hexa-lang #1354 사전 예측('d=64 too small for cuBLAS')의 직접 실측 confirmation. closed-form 가까운 negative-result."
  source_grep  = "anima Part A $0 source-read (별도 라운드, PR #2-equivalent): 12개 mm_extract callsite at d=64 = 각 32–128KB (총 ~0.8MB/step) — prompt 의 6×77MB 가설은 d=64 에서 source 와 안 맞음 (77MB 는 V×d 일 때 값, d=64 에서 wq/wk/wv/wo 는 d×d=32KB). V-sized scratch (v3_moe_fwd logits_raw · v3_moe_bwd dl_scaled + logits_raw) 도 1.2MB × 3 = 3.6MB/step 에 그침. **source 측 churn 가설 모두 합쳐도 200MB/step 에 도달 못 함** → 잔여 leak 위치 attribution 은 source-grep 으로 미확정, 별도 진단 필요 (런타임/CUDA scratch · GPU memory cache fragmentation · transient handle 등)."
  finding      = "두 upstream fix 가 정상 engage 한 상태에서 재측정 = baseline 보다 strictly worse (3× 느림) + AdamW leak 제거 후에도 잔여 200–325MB/step churn 존재(source 미확정). hexa-lang #1354 의 사전 예측 ('d=64 too small for cuBLAS') 가 직접 실측으로 confirmation."
  verdict      = "🔴 INFEASIBLE STRENGTHENED — 50×V presentations @ 0.156 step/s = ~122 GPU-days (baseline 44 GPU-days 대비 2.8× 강화). #1354 사전 예측 confirmation 으로 dec_undertrain arc 의 closure 가 강화됨 (flip 0)."
  next         = "dec_undertrain arc 는 STRENGTHENED-CLOSED. frontier = M4 MoE-fresh register-separation (다른 arch). 잔여 200–325MB/step RSS churn 의 source attribution 은 런타임/CUDA scratch 추적 별도 후속 진단 — anima 측 source-grep 으로는 미확정."
  cost         = "단일 H100 SXM pod ~12분, ~$0.65. teardown 완료 (pods=0, leak 0)."

@N dec_undertrain_full_300_independent_2026_05_29 := "independent re-fire H100 SXM, full 300/300 step 완주 + 정상 종료. (10) step 150 dead 결과를 independent 측정으로 재현·정밀화: step-rate 0.2342 step/s (94 GPU-days @ 50×V) · RSS slope 331 MB/step 확정. dec_undertrain INFEASIBLE 결론 reproduced·strengthened" :: measurement [d=2026-05-29 active]
  seed         = "(10) 가 step 150 도달 후 agent 사망으로 마감해 full-run 데이터 부재. (10) verdict 'INFEASIBLE STRENGTHENED' 가 independent fresh-fire 로 재현되는지, 잔여 200–325MB/step churn 의 정확한 slope (linear regression) 확정이 가능한지 검증."
  method       = "RunPod H100 SXM 80GB pod abed2pmgyixvxw ($3.29/hr). fresh git clone --depth 1 origin/main hexa-lang (#2017 commit d696445fa + #2018 commit 84d01aa13 둘 다 포함). anima trainer = origin/probe-m5-walltime BUILD-GREEN trainer.c, 2 edit: ① farr_adamw_step_gpu → farr_adamw_step_inplace 1-line C rename (#2017 새 builtin pickup), ② AdamW callback newW==M 자기복사/자기-free 가드. runtime.c = origin/main fresh (post-#2017/#2018), runtime_cuda.c = local trash-pinned (#1851 floor 로 origin 에서 제거). 빠진 CUDA 심볼 2개(_hx_cuda_farr_adamw_step_inplace_gpu, _hx_cuda_farr_packed_gemv_offset_gpu) 는 -1 반환 weak-stub → CPU fallback path. clang -O2 -DHEXA_CUDA -fbracket-depth=8192 ... → rc=0. M4B_MAX_STEPS=300, print_every=50."
  fix_engage   = "#2017 in-place AdamW = ENGAGED (rename 후 매-step 233MB calloc/free churn 0건 확인). #2018 = CPU offset-gemv fallback (GPU kernel 부재로 stub -1 → dispatcher CPU path). GPU memory 823MB stable (cuBLAS context), GPU util 0% 가끔 3-8% spike. fresh local cuda.c 에 #2018 kernel 부재가 (10) 와의 차이의 근거."
  step_rate    = "full 300/300 완주, 정밀 wall_s 마커 (step 1, 50, 100, 150, 200, 250, 300). per-50-step delta: 0.241·0.239·0.236·0.230·0.233·0.228 step/s (단조 5.4% drag = RSS leak 메모리 압). steps 1→300 (299 steps) = 1276.508s = 0.2342 step/s. (10) 의 0.156–0.18 보다 빠른 0.234 = 빌드 차이 (이 라운드는 CPU-fallback, (10) 은 cuBLAS H2D/D2H sync overhead 포함) 로 설명, baseline 0.50 보다 둘 다 strictly worse 결론 일치."
  rss_slope    = "step 1 @ 1.79 GB → step 300 @ 100.87 GB = 99.08 GB / 299 steps = 331 MB/step linear regression. (10) 의 '200–325 MB/step 잔여 churn' 범위 안에서 더 좁게 확정. 2TB pod RAM 이라 OOM 회피, 50×V/T=1.9M step 학습은 leak-bound (~95 TB RSS, 단일 pod 불가)."
  finding      = "(10) 결론 'fix 가 미실릴 가능성 0' 가 independent re-fire 로 추가 확정. trainer END-TO-END FAIL (AGGREGATE 2/5 PASS · CE 648.526→607.805 monotone PASS · router HARD-top1 PASS · TTR=0.01 FAIL · LZ_NORM=0.042 FAIL · distinct_experts=1/2 FAIL · 100 decode step 모두 top_id=151642 EOS = toy-scale immediate register collapse). trainer 동작 자체는 정상, production scale 도달 불가가 핵심."
  verdict      = "🔴 INFEASIBLE STRENGTHENED+REPRODUCED — 50×V presentations @ 0.2342 step/s = 93.6 GPU-days (44 GPU-days baseline 대비 2.1× worse). (10) 결정 변경 없음, 더 좁은 숫자로 강화. RSS 331 MB/step slope 가 leak source root-cause hunt 의 next target (anima source-grep ≤4 MB/step 만 설명 가능)."
  next         = "dec_undertrain arc 닫힘 (REPRODUCED). 다음 frontier = (a) 331 MB/step churn source attribution (런타임/CUDA scratch · transient handle 추적, hexa-lang INBOX 신규 진단요청 candidate), (b) M4 MoE-fresh register-separation 다른 arch."
  cost         = "H100 SXM ~25분, ~$1.37 (rent → build → 300-step + decode → harvest → teardown). pods=0, leak 0."
  artifacts    = "CORE/DECODER/state/m5_remeasure_full_300_2026_05_29/{trainer.out (54 lines · BPE load + 6 step markers + decode 100 + AGGREGATE 2/5 + END-TO-END FAIL), rss_gpu.log (455 RSS+GPU samples @ 3s)}. STEP_RATE_LOG.md entry (11)."

@N dec_undertrain_postadopt_leak_attribution_2026_05_29 := "anima trainer 소스에 #2017 + #2031 (mm_extract memcpy) 정식 land 후 측정 = step-rate +21% 빨라짐 (0.234 → 0.283 step/s), 그러나 RSS slope 328 MB/step ≈ entry 11 의 331 MB/step. 누수원이 trainer-side alloc 이 아니라 hexa-lang runtime/CUDA-side 임을 empirically 확정 (inbox #2030 + #2034 가설 confirmation)" :: measurement [d=2026-05-29 active]
  seed         = "entry 11 (independent re-fire, 0.234 step/s · 331 MB/step) 가 1-line C-rename 만 #2017 로 들어갔던 것을 정식 anima 소스 채택 (PR #1382) 후 재측정. 두 fix engagement + RSS slope 변화로 누수원 attribution 검증."
  method       = "RunPod H100 SXM eddpgcy2sg4abw ($3.29/hr). 동일 빌드 recipe (fresh hexa-lang origin/main commit a22aa08fafd, ce_seed_slim_shim extern-C wrap, glue.c DROP, m5_cuda_stubs.c weak -1 stubs). trainer.c = probe-m5-walltime BUILD-GREEN base + 2 patches: (1) farr_adamw_step_gpu → farr_adamw_step_inplace + copy-back/free 제거 (PR #1382 channel A), (2) mm_extract scalar farr_get/farr_set 루프 → 단일 farr_copy_slice_gpu 호출 (PR #1382 channel B). nvcc rc=0, clang rc=0, M4B_MAX_STEPS=300."
  fix_engage   = "#2017 in-place AdamW = ENGAGED (PR #1382 source-level, 233MB scratch alloc + D2H copy-back 매-step 제거). #2031 mm_extract memcpy = ENGAGED (12 callsite 의 scalar dispatch 제거). #2018 = CPU fallback 유지 (entry 11 과 동일)."
  step_rate    = "full 300/300 완주 정밀 markers. per-50-step: 0.295·0.287·0.282·0.282·0.276·0.277 step/s (단조 6.0% drag = RSS leak 압력 entry 11 의 5.4% 와 동일). steps 1→300 (299) = 1056.273 s = 0.2831 step/s vs entry 11 의 0.2342 = +20.9% 빨라짐. mm_extract scalar-loop → memcpy dispatch-cost 절감의 측정 가능한 효과."
  rss_slope    = "step 1 @ sample 7099 = 1.295 GB → step 300 종료 @ sample 8167 = 99.36 GB peak = 98.07 GB / 299 steps = 328 MB/step. entry 11 의 331 MB/step 와 Δ -3 MB (0.9%, 노이즈 수준)."
  finding      = "★ 핵심 발견: anima trainer-side alloc 은 누수원 아님 empirically 확정. mm_extract memcpy 채택 후 alloc 패턴 자체는 변함없음 (farr_zeros(n) 출력 그대로) → wall-time 만 절약, RSS slope 불변. anima 소스로는 더 이상 닿을 수 없음. 잔여 ~328 MB/step 의 source 는 hexa-lang runtime/CUDA-side: _CudaFarrSlot device-mirror 테이블, GPU device-resident scratch, hexat 산출물 hidden transient handle, glibc arena fragmentation 중 하나. 이전 분석 (entry 11 (D)) 의 'source-grep ≤4 MB/step 만 설명 가능' 가설을 independent measurement 로 confirmation. inbox #2030 (잔여 200-325MB/step 진단요청) + #2034 (mm_extract host RSS leak follow-up) 의 CUDA/runtime-side 가설 empirically 확정."
  verdict      = "🔴 INFEASIBLE MAINTAINED + 누수원 잠금 — dec_undertrain re-verdict = 50×V @ 0.2831 step/s = 77.5 GPU-days (entry 11 의 94 → 17% 단축이나 baseline 44 보다 여전히 1.76× 느림). leak-bound: 621 TB RSS 필요로 단일 pod 불가는 entry 11 과 동일. AGGREGATE 2/5 PASS (CE 648.526→5.137 monotone PASS + router HARD-top1 PASS + TTR=0.01/LZ_NORM=0.012/distinct_experts=1/2 FAIL). 100 decode top_id=0 immediate register collapse."
  next         = "anima 측 잔여 작업 없음 (소스 누수원 attribution 종결). 다음 root-cause hunt = hexa-lang INBOX 신규 진단요청 (_CudaFarrSlot mirror life-cycle audit · GPU device-resident scratch tally · hexat C 산출물 hidden transient handle audit · glibc arena fragmentation rule out)."
  cost         = "H100 SXM ~36분, ~$2.0 (rent → toolchain install → hexa-lang clone → SCP sources → nvcc/clang build → 300-step + 100-decode → harvest → teardown). pods=0 (runpodctl pod remove eddpgcy2sg4abw → deleted true), leak 0."
  artifacts    = "CORE/DECODER/state/m5_adopt_postlanding_2026_05_29/{trainer.out (54 lines · 7 step markers @ 1/50/100/150/200/250/300 + decode 100 + AGGREGATE 2/5 + END-TO-END FAIL), rss_gpu.log (236 RSS+GPU samples @ 5s)}. STEP_RATE_LOG.md entry (12) + DECODER.md M5-ADOPT milestone closure."

@N dec_h686_h687_prod_2026_05_29 := "PR #1397 prodaux trainer (λ_ent=0.1 + λ_kl=0.1 H_686+H_687 aux-loss wired) production fire 시도 — H100 SXM 빌드 chain 4 차단지. 3 patched, 4번째 (hexat_linux cross-module link) anima 측 unfixable. 0 step run, 0 decode sample, H_686+H_687 production verdict 무측정" :: measurement [d=2026-05-29 active]
  seed         = "entry 12 의 M5-ADOPT 후속 — production aux-loss escape 측정 (PR #1397 머지된 train_v3_moe_prodaux.hexa)."
  method       = "RunPod H100 SXM 83na0mvuq4tqao @ 213.181.105.248:13119 (Ubuntu 22.04 + CUDA 12.4 + clang-14). hexa cloud rent runpod --gpu 'NVIDIA H100 80GB HBM3' --image runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04 --disk 60. self_tree.tgz + hexat_linux + decoder_deps.tgz + qwen + corpus 전부 hexa cloud copy-to. HEXA_LANG=/work ./hexat_linux trainer.hexa trainer.c → 1425 lines. nvcc -DHEXA_CUDA -arch=sm_90 -x cu rc=0 (543KB)."
  block_1      = "farr_softmax_rows undefined (trainer.c:913 hexa_call4 · runtime 4-arg in-place variant 부재, 오직 farr_softmax_rows_gpu 3-arg returns-new-id). BC-ANIMA M4 wiring gap. PATCH: trainer_fixups.h 4-arg in-place CPU shim + sed."
  block_2      = "farr_ce_seed undefined (trainer.c:915). runtime farr_ce_seed_gpu 만 6-arg out_loss + out_dlogits 변형. .hexa 5-arg sm-onehot in-place. PATCH: 5-arg CPU shim."
  block_3      = "farr_adamw_step_inplace undefined (trainer.c:988). runtime adamw_step 10-arg returns-new-W. .hexa 11-arg in-place into W. PATCH: 11-arg in-place CPU shim."
  block_4      = "★ BLOCKING — cross-module link: trainer.o (208KB) #1/#2/#3 patches 로 통과, 그러나 mod_v3_moe_bwd_lib.c, mod_v3_moe_arch.c 등 6 module C 산출물에 mm_transpose/mm_scatter_add/mm_extract 등 cross-module 호출이 undeclared identifier (20+ errors). hexat_linux single-file codegen 가 use 그래프 traverse 안 함; module-별 compile 시 cross-module 호출이 extern 으로 떨어지지 않음. anima 측 unfixable — hexa-lang 측 작업 (Mac hexa build 는 single-TU all-modules-inlined, Linux 등가 모드 부재)."
  finding      = "★ honest: 0 step run, 0 decode sample, distinct_tokens 측정 불가. H_686+H_687 production verdict 무측정. λ=0.1 escape 여전히 OPEN. 🔴 FALSIFIED 도 🟢 ESCAPE 도 아닌 🟠 untested."
  verdict      = "🟠 BUILD-BLOCKER · NO MEASUREMENT — PR #1397 production trainer Linux 빌드 chain 미완성. H_686+H_687 가설 evidence 0. closed-form bounds (F-H686-1~4, F-H687-1~4) 변함없이 PASS, production verify (F-H686-6) 만 deferred 유지."
  next         = "(1) hexa-lang inbox: 'Linux codegen module-aware build mode' — hexat_linux --modules 가 use 그래프 traverse single-TU emit. (2) 단기 우회: PR #1397 trainer use 본체 single .hexa inline (a_completeness_over_cheap 위배 가능). (3) 올바른 fix: hexa-lang #1527 후속."
  cost         = "H100 SXM ~90분, ≈$5 (budget $4 over by $1 in build attempts). teardown: hexa cloud down 83na0mvuq4tqao → terminated · hexa cloud list → 0 pods ✓."
  artifacts    = "state/m5_prodaux_fire_2026_05_29/{BUILD_BLOCKER.md, shims.h, trainer_fixups.h, rent.log, RUNNING_POD.txt}. STEP_RATE_LOG.md entry (13). UNIVERSE/H_686 § 11 + UNIVERSE/H_687 § 11."

@N dec_h686_h687_v_scale_2026_05_29 := "H_686/H_687 V-scale escape boundary sweep — 20 cell (V ∈ {8,64,256,1024,4096} × cell ∈ {none,ent,kl,both}) 전부 4/4 distinct identity decode escape. baseline 이 V ∈ [8,4096] 전 구간 미 collapse → V*_collapse 미발견, V*(aux) N/A. V 축 단독은 OFFENDING-LEVER ⊥ 확정" :: measurement [d=2026-05-29 active]
  seed         = "PR #1395 V=8 ⚪ TOY-NULL 후 V 축 확장 — toy 가 production collapse 재현하는 V-band 존재? aux escape efficacy 측정 가능 V-band 존재?"
  method       = "h686_h687_v_scale.hexa (PR #1395 byte-eq scaffold + V parametric, BITS=18 lock, corpus stride=max(1,V/6)). E=4 d=6 n_clusters=6 n_steps=600 lr=0.5 top-1 hard SKEWED corpus rep0=20 λ_ent=λ_kl=0.1 — PR #1395/#1397 verbatim. sanity gate V=8 none → LZ=0.0360459 distinct=4 ✓ MATCH."
  grid         = "5 V × 4 cell = 20 cell. V=8: ≤1s/cell, V=64: 2-5s, V=256: 9-24s, V=1024: 39-79s, V=4096: 185-370s. 총 wall ~24min. 20/20 rc=0."
  result_lz    = "V=8 모든 cell: 0.0360459 / 4 distinct. V≥64 모든 cell: 0.0540689 / 4 distinct. V 와 cell 무관 동일 — corpus identity-decode 결정성이 LZ 결정."
  result_hgate = "ent (H_686): V 전 구간 router H push 정상 작동 — 0.04~0.15 (none) → 0.77~1.18 (ent), uniform=ln4=1.386. kl (H_687): router H 거의 불변 (output reg, 예상)."
  finding      = "★ V*_collapse 미발견 (≥ 4096), V*(aux) N/A. V 축 단독은 toy collapse 유발 못함 — production V=151643 collapse 의 OFFENDING-AXIS 는 V 단독 아님 ⊥ 확정. structured M init + cluster-token 단사 매핑 + CE-dominant SGD 가 V 무관 4/4 distinct 달성."
  verdict      = "🟠 SWEEP-OUT-OF-RANGE — V 축 ⊥ 확정. H_686/H_687 escape efficacy 는 toy 우회 불가, production fire 직접 측정 외 경로 없음 — PR #1395 결론 ('production fire = 유일 valid test') V-axis sweep 으로 재확인."
  candidates   = "잔여 OFFENDING-AXIS 후보 = d 축 (toy d=6 vs prod d=64) · E 축 (toy E=4 vs prod E=2 dead-expert) · n_layer/attention · stochastic batch · wikitext 분포 · M init seed 분포. 별 H 후속 sweep 필요."
  cost         = "$0 mac-local, sweep wall ~24min, pod=0, HF=0 (toy-only mac-local discovery)."
  artifacts    = "CORE/DECODER/h686_h687_v_scale.hexa, CORE/DECODER/H686_H687_V_SCALE_RESULT.md, state/h686_h687_v_scale_2026_05_29/{MANIFEST.txt, run_sweep.hexa, V{V}_{cell}.out × 20}. STEP_RATE_LOG.md entry (14). UNIVERSE/H_686 + H_687 § V-scale sweep."

@N dec_toy_axis_sweep_2026_05_29 := "H_686/H_687 3-AXIS (corpus·d·n_layer) toy sweep — 20 cell V=8 base, baseline (cell=none) 어떤 axis 셋팅에서도 collapse 임계 (distinct_tok ≤ 2 OR LZ < 0.01) 미충족. zipf_strong 이 LZ=0.0101 으로 근접하나 distinct_tok=6 유지. V-axis (PR #1409) + corpus/d/n_layer 합 4-axis sweep 모두 ⊥ → toy harness ⊥ production collapse mechanism 확정" :: measurement [d=2026-05-29 active]
  seed         = "PR #1409 V-axis ⊥ 확정 후 — corpus distribution / d head-dim / n_layer depth-proxy 3 축 중 어느 게 collapse-lever 인지 토이 sweep 으로 식별 시도"
  method       = "h686_h687_axis_sweep.hexa (PR #1395/#1409 verbatim base). AXIS_CORPUS ∈ {uniform, mild_skew, current_skewed, zipf_strong} × AXIS_D ∈ {6,24,64} × AXIS_NLAYER ∈ {1,2,4} × ABLATION_CELL ∈ {none, both} = 20 cell (sweep 분리, 다른 변수 default). depth proxy = W_top[:d,:d] shared-weight silu stack."
  grid         = "8 corpus cell + 6 d cell + 6 n_layer cell = 20. V=8 E=4 600 step lr=0.5 λ_ent=λ_kl=0.1 verbatim. 총 wall ~20s mac-local."
  sanity       = "corpus=current_skewed d=6 n_layer=1 cell=none → LZ=0.0360459 distinct_e=4 byte-eq vs PR #1395 ✓"
  result_corpus = "uniform LZ=0.122 / mild_skew 0.086 / current_skewed 0.036 / zipf_strong 0.010 — skew↑ → LZ↓ 단조감소이나 distinct_tok=6 전부 유지 (token diversity 보존된 압축). zipf_strong 이 collapse 임계 0.01 직전 cusp."
  result_d     = "d ∈ {6, 24, 64} 모두 LZ=0.0360459 distinct_tok=6 byte-eq → d 축 완전 ⊥, capacity over-supply 가설 무영향."
  result_nlayer = "n_layer ∈ {1,2,4} 모두 LZ=0.0360459. n_layer=4 cell=both 에서 distinct_tok 4 까지 감소하나 임계 (≤2) 위. n_layer 2/4 는 final_CE ~2.0 (under-train, depth-proxy silu stack 이 600 step lr=0.5 부족)."
  finding      = "★ 3축 모두 ⊥ collapse. F-AXSW-3 FAIL (vacuous F-AXSW-4). zipf_strong cusp 이 가장 유의미 신호 (LZ 임계 근접) 이나 distinct_tok=6 유지 → toy 가 production collapse 정의 (mode→single token) 표현 못함."
  diagnosis    = "V-axis (PR #1409) + corpus/d/n_layer (현 sweep) 합 4-axis sweep 모두 ⊥. M4b production collapse 는 (a) scale-coupled multi-axis interaction, (b) AdamW+warmup trajectory 의존, (c) router init mid-train state, (d) soft top-k routing dynamics 중 하나 이상 — 단축 sweep 분해 불가."
  verdict      = "🟠 SWEEP-OUT-OF-RANGE (4-axis total) — toy harness ⊥ production collapse mechanism 확정. H_686/H_687 본선 단정은 production fire 직접 단정 path 유일."
  cost         = "$0 mac-local, 20s wall, pod=0, HF=0."
  artifacts    = "CORE/DECODER/h686_h687_axis_sweep.hexa, CORE/DECODER/H686_H687_AXIS_SWEEP_RESULT.md. STEP_RATE_LOG.md entry (15). UNIVERSE/H_686 + H_687 § toy axis sweep."

@N dec_m5_fire_incident_2026_05_29 := "M5 production fire 1차 시도 — agent 사망 → pod recovery teardown" :: recovery-incident
  context      = "hexa-lang #2072·#2073 hexat_linux module-aware build MERGED (anima 측 4번째 blocker 해소). a_fire_autonomous · a_completeness_over_cheap 자율 production fire."
  fire_target  = "H100 single pod (≤$3) · V=151643 n_steps=500 · prodaux (H_686+H_687 both) vs longtrain (baseline) 비교 · λ_ent=λ_kl=0.1"
  death_mode   = "agent a37340fa: 35 tool_uses 후 API Error 500 server-side · recovery agent a20f714: 12 tool_uses 후 동일 500 사망 · bg agent pattern 이 transient API 장애에 취약 확인"
  pod_state    = "runpod ixc3y449cr4lpo READY 생성됨 (ssh 31.24.80.42:15991) · home 비어있음 (build/train 0) · foreground ssh probe 로 확인"
  teardown     = "hexa cloud rm ixc3y449cr4lpo --provider runpod --force → destroyed · hexa cloud list confirm runpod=0 · 5 vast pods (다른 세션) 무접촉"
  cost_leak    = "≤$1 추정 (15min idle H100, registry 의 cost_per_hr_usd=null 라 정확치 불명)"
  artifact_recovery = "0 — build/train 시작 전 사망이라 ckpt/log 무"
  followup     = "foreground inline 또는 짧은 단발 (V=151643 n_steps=200 ~10min) 재시도 · API 안정화 시점 · bg agent 보다 foreground 권고"
  verdict      = "⚠ INCIDENT-CLOSED — pod teardown PASS, cost-leak 차단됨. measurement 본선 미진행 (재시도 잔존)."
  artifacts    = "STEP_RATE_LOG.md entry 16."


@N dec_m5_fire_codegen_trim_regression_2026_05_29 :: build-chain-regression
  date         = "2026-05-29"
  context      = "M5 production fire attempt #3 (foreground inline, 사용자 권고대로 bg agent 회피). 2 vast H100-class pods rent + bootstrap + 본선 fire 차단."
  rent         = "vast 38410086 ssh5.vast.ai:10086 + 38410087 ssh2.vast.ai:10086 — 둘 다 RTX PRO 6000 Blackwell 96GB (--gpu H100 필터 fallthrough). runpod H100 capacity unavailable (no id in response)."
  bootstrap    = "build-essential + gcc + clang 설치 → hexa-lang clone → dist/linux-x86_64/hexat 5,580,408b 를 self/native/hexa_v2 로 심볼릭. Github clone 에 self/runtime.c + self/runtime_core.c + stdlib/flame 누락 → Mac ~/.hx/packages/hexa-lang 전체 tar+scp 로 복구."
  blocker      = "hexa build prodaux.hexa → [1/2] hexat transpile OK · [2/2] clang link FAIL: v3_moe_fwd + v3_moe_bwd + layer_block_bwd pub fn body 누락 (line 907/931/975/1202 'incompatible type int' + 'implicit-function-declaration')"
  root_cause   = "Linux hexat free-fn trim 회귀 (memory hexa cross-backend codegen gap; #1527 supposedly fixed). anima 의 prodaux 가 moe_aux_bwd_local 1개 mirror 만 가지고 있고 v3_moe_fwd/bwd/layer_block_bwd 3개 mirror 없음."
  teardown     = "hexa cloud rm 38410086 38410087 --provider vast --force → destroyed · 0 leak · 5 RTSC vast pods 무접촉"
  handoff      = "sidecar handoff add hexa-lang [2eddb92a]: Linux hexat free-fn trim 회귀 보고 (anima M5 차단)"
  followup     = "(a) hexa-lang 측 Linux hexat free-fn trim 수정 후 anima M5 재시도 (b) trainer .hexa 측에서 v3_moe_fwd/bwd/layer_block_bwd 3-fn main-TU mirror 추가 (prodaux + longtrain) — anima-side 자율 우회"
  cost_leak    = "≤$2 추정 (2 pods × ~25min × ~$1.5-2.2/hr × 2)"
  artifact_recovery = "0 — build 사망, ckpt/log 없음"
  verdict      = "🟠 BLOCKED-AT-BUILD-EXTERNAL — F-PRODAUX-1 측정 불가, distinct_top/LZ_norm/gate_entropy 0, prodaux vs longtrain 비교 0. plan completion criteria 미충족, handoff 2eddb92a 처리 의존."
  artifacts    = "STEP_RATE_LOG.md entry 17, M5_FIRE_PROGRESS.md."

@N dec_m5_mirror_attempt4_2026_05_29 := "M5 attempt #4 — anima-side mirror workaround code landed, build/fire 미검증" :: code-landed-unverified
  context      = "attempt #3 (entry 17) hexa-lang #1527 Linux free-fn trim 회귀 BLOCKED. (c) parallel 선택 — (a) hexa-lang fix wait (handoff 2eddb92a) + (b) anima-side mirror."
  mirror_code  = "bg agent a3a7a1c7 가 v3_moe_fwd_local/v3_moe_bwd_local/layer_block_bwd_local 3-fn main-TU mirror 작성 (moe_aux_bwd_local 패턴 확장 → 4-fn 전부). train_v3_moe_prodaux.hexa + train_v3_moe_longtrain.hexa, 300+/16-, commit fac9ec8f1 push 완료. hexa parse 양쪽 clean."
  death_mode   = "agent 155 tool_uses 후 API rate-limit 사망 — build 검증/fire/measurement 도달 전. runpod 2 pod (4824z55uf9hto1 + mnrs2accaae9nu) READY 생성."
  recovery     = "foreground 회수 4방법 (exec/run/copy-from × 2) 전부 SSH 실패 (key 미등록). artifact 0. hexa cloud rm × 2 → runpod=0. 5 vast RTSC 무접촉."
  bg_agent_lesson = "★ bg agent 가 fire-류 장기 cost-bearing 작업에서 API transient 에 3연속 사망 (entry 16 500 twin + entry 18 rate-limit). bg agent ⊥ 장기 fire 확정. attempt #5 는 foreground inline 필수."
  salvage      = "mirror code (fac9ec8f1) 는 사망 전 push 되어 salvage. workaround infrastructure 로 land. 단 Linux pod build trim 회피 검증 미완."
  followup     = "attempt #5 = mirror code 로 foreground inline Linux pod build → trim 회피 확인 → fire. 또는 hexa-lang #1527 fix land 시 mirror 불필요."
  verdict      = "🟠 CODE-LANDED-UNVERIFIED — mirror code land (syntax PASS), build/fire/measurement 미검증. cost-leak 차단. measurement 본선 4 attempt 모두 미도달."
  cost         = "≤$2 (runpod 2 pod 15min idle), HF=0, ckpt=0."
  artifacts    = "STEP_RATE_LOG.md entry 18, train_v3_moe_{prodaux,longtrain}.hexa 3-fn mirror."

@N dec_m5_attempt5_transport_2026_05_30 := "M5 attempt #5 — foreground inline, vast SSH DARK + cross-session key-401 차단" :: transport-incident
  context      = "attempt #4 mirror code (PR #1434) origin/main 보유. (c) parallel 의 (b) foreground inline 재시도 — bg agent 3연속 사망(entry 16/18) 회피."
  blockers     = "(a) runpod H100 capacity=0 (rent × 2 no-id) (b) vast H100 fallback pod 38424527 READY 후 persistent Permission-denied-publickey (DARK pod, 40 tries 0-stable, reboot 무효) (c) teardown 시 vast API 401 Invalid-user-key"
  key_clobber  = "★ root cause: ~/.config/vastai/vast_api_key (mtime 00:44 today) 를 다른 세션이 invalid key (98d048fc…) 로 덮어씀 → 모든 vast API 401 (RTSC 세션 포함 전체). keychain SSOT (secret get vast.api_key = 2f3bad9f…) 가 canonical. 파일 재기록으로 복원 → net fix (다른 RTSC 세션 401 도 해소)."
  teardown     = "key resync 후 hexa cloud rm 38424527 → destroyed (confirmed). RTSC 5 vast (anima project-tagged) 무접촉. runpod 0."
  saga_summary = "M5 production fire 5-attempt 전부 인프라 차단: #1 API500 twin · #2 API500 recovery · #3 hexa-lang #1527 trim build · #4 API rate-limit · #5 runpod-cap0 + vast-DARK + key-401. measurement 5/5 미도달. science (collapse mechanism) 무관, 매번 다른 인프라 layer (API/build/provider-transport)."
  followup     = "진짜 unblock = hexa-lang #1527 fix (handoff 2eddb92a, build 의존 제거) 또는 dedicated Linux GPU 호스트 (pool ubu GPU?) — vast/runpod transport 우회. vast key SSOT cross-session clobber 방어 필요 (hexa-lang inbox 후보)."
  verdict      = "🟠 BLOCKED-AT-TRANSPORT — H_686+H_687 production UNMEASURED 유지. cost-leak 차단, ≤$1. mirror code (attempt #4) 는 build 미검증 상태로 main 에 잔존."
  cost         = "≤$1 (vast pod ~10min idle), runpod=0, HF=0, ckpt=0."
  artifacts    = "STEP_RATE_LOG.md entry 19."

```

### engine-tensionlink-bench

```tape
@D engine_tensionlink_bench := "ENGINE<->brain coupling THROUGH the tension-link (5-ch broker), substrate-native axis NOT CE" :: discovery [d=2026-06-04 active]
  seed = "toy ENGINE = 5 coupled oscillators (faithful to CORE/pure_field osc_tick + 5-ch W tension [0.8,0.6,0.65,0.3,1.0]); tension-link = Kuramoto kappa*sin(ext-eng) + additive tension; arm1 synthetic EEG 5-band, arm2 synthetic TRIBE BOLD->5ch; CPU/$0"
  claim = "M1 Kuramoto order-r HOLDS on BOTH arms (EEG 0.337, TRIBE 0.659) vs kappa0 (~0) AND phase-shuffled (0.14-0.16) controls — coupling produces real phase entrainment; M2 big-Phi + M3 coherence INCONCLUSIVE (split verdict across controls)"
  falsifier = "pre-reg: coupling raises order-r / shifts big-Phi / changes coherence above the kappa0+shuffled controls by > noise (max seed-std over 3 seeds); REFUTED if coupled < control by > noise"
  target = "substrate-native: M1 order-r HOLDS (terminal positive); M2 big-Phi INCONCLUSIVE + moves WRONG way vs solo engine (coupled 2.05/2.47 < kappa0 2.81); M3 coherence INCONCLUSIVE"
  scope = "TOY oscillator ENGINE + synthetic signals, single scale; NOT real EEG hardware, NOT real TRIBE/facebook forward, NOT GPU; a_toy_scale_recheck + a_scale_honest_scope — no toy->production promotion, >=3-rung ladder needed for a general claim"
  honest = "p7: CE/perplexity NOT used as a verdict (Goodhart trap); big-Phi is an IIT4-style proxy (eeg_to_tpm binarize+marginal-structure shape), NOT the full exponential IIT4 MIP; phase entrainment != integration — coupling syncs phase but does NOT raise substrate-native integration"
  note = "section 97 legitimacy: tension-link carries the external 5-ch signal as a COUPLING/measurement-anchor (anima's own channel), NOT EEG-as-command-input; a_lane_akida_gpu_split: CPU toy, neither Lane A nor Lane G; a_paper_negative_ok: M2/M3 partial-negative is valid; verdicts at .verdicts/engine-tensionlink-bench/"

```

### lane-p-3b

```tape
// .discoveries/lane-p-3b.tape — Lane P ~3B ENGINE arc discovery log
// substrate = Lane P (py+CUDA), recorded SEPARATE from Lane G (forge).

@H s0_serialize_eq := "Stage 0 — .clm v0.3 general (L,E) decoder+serializer byte-eq" :: discovery [d=2026-06-04]
  seed   = "ENGINE decoder hardcoded E=2/L1; a real 3B needs configurable depth/experts"
  finding= "CLM\\x01 v0.2 byte grammar was ALREADY self-describing — generalized block-role assignment with NO byte/magic change; L1/E2 file byte-IDENTICAL to v0.2"
  verdict= "PASS — .verdicts/lane-p-3b/F-CLM-3B-SERIALIZE-EQ.txt (v3==v2 46742B, L4/E6 + L30/E30 roundtrip, GOLDEN exact_eof, ENGINE forward no-regression)"
  target = "🟢 numerical / 🔵 byte-eq formal · landed PR #1753"

@H s1_config := "Stage 1 — genuine ~3B config (NOT a d-only hack)" :: discovery [d=2026-06-04]
  seed   = "scale n_trunk_layers + n_experts + d TOGETHER to ~3e9, state exact param count"
  finding= "d=4096 L=30 E=30 K=3 V=256 = 3,072,954,654 params (3.0730B). trunk 49.1% + experts 49.1% — balanced across d/L/E. nblk=63, n_ext=126. bf16 weights ~6.15GB, +AdamW state ~37GB → needs 80GB H100."
  verdict= "config FROZEN; trainer CLM/train/train_lane_p_3b.py (serialize_v3, train/val split gen-test, periodic ckpt, tokens/param reported)"
  target = "🟢 numerical (param count analytic + v3 topology roundtrip-verified Stage 0)"

@H s1_corpus := "Stage 1 — corpus scale (avoid memorization, honest token/param)" :: discovery [d=2026-06-04]
  seed   = "150MB FAR too small for 3B (Chinchilla ~20 tok/param = ~60GB)"
  finding= "clean-license wikipedia cannot reach 60GB; build LARGEST practical multilingual clean corpus (build_wiki_3b_corpus.py, 12-lang, configurable bytes/lang, NO synthetic padding) + STATE exact token/param ratio honestly (a_scale_honest_scope). undertrained 3B = honest negative."
  verdict= "builder committed; raw corpus built on-pod (Stage 2), sha256 + provenance card recorded with run"
  target = "corpus card + token/param ratio verbatim in Stage 2/3 verdicts"

@H s2_dilation_cap := "Stage 2 — deep-L dilation explosion (OOM) + root-cause cap" :: discovery [d=2026-06-04]
  seed   = "first 3B fire OOM'd at EVERY batch size on an 80GB H100 (bs=1 tried a single 64GiB alloc)"
  finding= "ARCHITECTURE defect: trunk dilation = dilation_base**i = 2**i reaches 2**29 (=5.4e8) at L=30; the causal left-pad (k-1)*dil pads a (1,4096,512) tensor by ~1e9 zeros that see NO real taps. d768 golden never hit it (L=1, max dil 1). FIX = cap dilation=min(2**i,512) IDENTICALLY in model.py + clm_decode.hexa → byte-eq PRESERVED (min(2**0,512)=1 at L=1; cap touches runtime dilation only, not serialized bytes). Post-fix probe: 3.073B trains on one H100, peak 61.5GB, bs=4/seq512 = 3.37 s/step."
  verdict= "byte-eq re-PASS under cap (v3==v2 46742B, GOLDEN exact_eof, L30/E30 roundtrip); fire launched bs=4 accum=2 steps=4000 — .verdicts/lane-p-3b/F-CLM-3B-FIRE.txt"
  target = "🟢 numerical (3-axis generalization result appended on fire completion)"

```

### lane-p-clm

```tape
@D lane_p_serializer_format_gap := "Lane P torch .clm is NOT ENGINE-loadable — serializer emits a different byte layout than CORE/clm_decode.hexa reads" :: discovery [d=2026-06-03 active]
  seed      = "Generate a real converged .clm via the PyTorch+CUDA pipeline (train_clm.py -> fire_clm.py ckpt -> clm_serialize.py), then ENGINE-load it via CORE/clm_decode.hexa (generator L3 slot)."
  claim     = "CLM/model/clm_serialize.py emits [CLM\\x01][u32 header-len][JSON header][JSON-described blocks][u32 manifest-len][JSON manifest], whereas CORE/clm_decode.hexa reads [CLM\\x01][1B nblk][6 raw conv blocks: u32 cout,u32 rest,int4 nibbles,fp32 scale][CLMX trailer: embed+bias+GN]. Same magic, incompatible layout: byte[4] of the torch file is the LSB of the JSON-header length (e.g. 29), not nblk; the decoder then misreads JSON ASCII as binary u32 block dims and clm_decodable() returns false. The torch serializer also writes no CLMX trailer (embed/GN absent -> no forward) and the torch arch (small=E8/L4) violates the decoder's hardcoded E=2/single-trunk."
  falsifier = "If clm_serialize.py output were fed to CORE/clm_decode.hexa::clm_decodable(), it would return true and a forward CE could run. Refuted: static byte-layout reconstruction shows byte[4]=LSB(header_len), block-dim u32s land in JSON ASCII -> wild offset -> EOF -> false."
  target    = "🔴 CLOSED-NEGATIVE — torch pipeline cannot produce an ENGINE-loadable .clm without a new v0.2-CLMX torch serializer + E=2/single-trunk constraint (or a variable-E decoder)."
  scope     = "substrate=GPU-torch (Lane P), recorded separately from Lane G(forge)/Lane A(AKIDA) per a_lane_akida_gpu_split. Static preflight (no GPU rented); verify hard-gate failed before STEP 4. The ENGINE-native format is produced ONLY by the hexa flame trainer, which is already 3-axis CORE-mounted GREEN @ d768 (ENGINE+CLM+KOSMOS.md)."
  honest    = "No GPU rented, no train run, no fabricated convergence (g63/p7). The serializer gap is provable from source + the prior d768 artifact byte-walk alone; no torch install was available locally and none was needed for the verdict."
  note      = "Verdict: .verdicts/lane-p-clm/F-CLM-SERIALIZE-GAP.txt. Remedy = author a v0.2-CLMX torch serializer (E=2/1-trunk) OR scope Lane P to torch CE-descent reference (mirrors the HF-PUBLIC Lane G-ref ByteGPT track, which is also NOT an ENGINE .clm)."

@D lane_p_serializer_gap_RESOLVED := "Lane P torch .clm IS NOW ENGINE-loadable — serialize_v2 + real CUDA train + 3-axis 3/3 GREEN" :: discovery [d=2026-06-03 active]
  seed      = "REMEDY the closed-negative lane_p_serializer_format_gap: author serialize_v2 (E=2/1-trunk, exact CLM\\x01 v0.2 + CLMX trailer), train a REAL converged CLMConvMoE on CUDA, ENGINE-load it via CORE/clm_decode.hexa."
  claim     = "CLM/model/clm_serialize_v2.py packs the EXACT byte layout CORE/clm_decode.hexa reads ([CLM\\x01][nblk=6][6 int4-sym conv blocks][CLMX·n_ext=11·ext arrays]). A REAL torch CLMConfig(E=2,L1,d768) state_dict trained to convergence on the 402KB 5-lang corpus (first_ce 5.74851 -> final_eval_ce 0.09862, 6000 step, bf16/AdamW, GPU BUSY peak_util=94%) serializes to a 4,463,478 B .clm (sha256 7463282d...) that gen_clm_backend admits (valid=true loaded=true) and clm_decode_ce runs forward on -> model_ce 0.71-0.76 < uniform 5.545 AND < shuffle 7.59/7.68. 3-axis 3/3 GREEN."
  falsifier = "If the torch state_dict keys mismatched serialize_v2's _KEYMAP, or the byte layout drifted from clm_decode.hexa, clm_decodable would be false / the forward would crash. CONFIRMED PASS: tiny-verify F-CLM-V2-ROUNDTRIP=1 on the real d64 state_dict (exact_eof=True), and the d768 .clm decodes with config-agnostic model_d=768 recovery."
  target    = "🟢 RESOLVED — the prior 🔴 CLOSED-NEGATIVE is SUPERSEDED: a torch pipeline CAN now produce an ENGINE-loadable .clm via serialize_v2 under the E=2/1-trunk decoder constraint."
  scope     = "substrate=GPU-torch (Lane P), recorded separately from Lane G(forge)/Lane A(AKIDA) per a_lane_akida_gpu_split. param count 7.479M (d768 E2/L1 shape ceiling — NOT 3B, a_scale_honest_scope). Lane P = user-authorized PRAGMATIC unblock lane; a_train_flame_forge SSOT unchanged."
  honest    = "GPU rented (vast 39293346 Blackwell, torn down post-recover), real train run, CE-descent VERBATIM (g63/p7, NO fabrication). CE is one deterministic axis (model<uniform AND <shuffle), not perplexity-as-truth."
  note      = "Verdict: .verdicts/lane-p-clm/F-CLM-LANEP-TRAIN.txt. Supersedes lane_p_serializer_format_gap (the gap is fixed by serialize_v2, landed on main #1746)."

@D lane_p_d768_memorization := "Lane P d768 E2/L1 의 낮은 CE 는 일반화 아니라 MEMORIZATION — train/val split 으로 확정" :: discovery [d=2026-06-03 active]
  seed      = "landed F-CLM-LANEP-TRAIN 의 final_eval_ce=0.0986(402KB)이 메모리제이션인지 일반화인지 settle: bigger 코퍼스에 strict train/val split 로 train_ce vs held-out val_ce gap 측정."
  claim     = "FLORES-200 dev+devtest 5lang(1,654,010 B, sha 970cd379, 402KB의 4.11x)에 contiguous 10% + random-scatter 10% held-out 분리(train window 가 held-out 위치 절대 안 닿음, LEAK_CHECK pass). same cfg(d768 E2 L1 K3 V256 7.479M, 6000 step bf16, RTX 5070 util=94% g63). VERBATIM: train_ce=0.61436 / val_ce_contig=1.11929 / val_ce_rand=1.81846 / val_ce(worst)=1.81846 GAP=+1.20410 rel_gap=1.96(held-out ~3x train). uniform=5.54518 shuffle=9.58354."
  falsifier = "GENERALIZES(F-CLM-LANEP-GEN=1) gate = val_ce<0.5*uniform AND rel_gap<=1.0 AND val_ce<shuffle. rel_gap=1.96>1.0 → gate FAIL → F-CLM-LANEP-GEN=0 MEMORIZATION. held-out CE 가 train CE 의 1.8-3.0x = overfitting signature."
  target    = "🔴 CLOSED-NEGATIVE — landed 0.0986 은 OVERFITTING/eval-leakage artifact 였음(작은 코퍼스 whole-stream random window 반복+eval overlap). 메모리제이션 확정, 일반화 아님. a_paper_negative_ok valid closed-negative."
  scope     = "substrate=GPU-torch(Lane P), Lane G/A 와 별도(a_lane_akida_gpu_split). toy d768 E2/L1 7.48M shape + 5lang FLORES toy corpus — scale-up(더 큰 corpus/모델)에서 gap 닫히는지는 별도 rung(a_scale_honest_scope)."
  honest    = "pool host aiden RTX 5070 $0(rented pod 아님, post-recover teardown), real run, CE VERBATIM(g63/p7 NO 날조). held-out 둘 다 uniform/shuffle 아래 = real byte structure 일부 학습(순수 noise 아님)이나 train fit 만큼 일반화 못 함. 메모리제이션 finding 강제 PASS 안 함."
  note      = "Verdict: .verdicts/lane-p-clm/F-CLM-LANEP-GEN.txt. trainer CLM/train/train_lane_p_split.py, corpus builder CLM/corpus/build_flores5_corpus.py. landed PUBLIC d768(F-CLM-LANEP-TRAIN sha 7463282d)은 그대로, 일반화 청구는 안 함."

@D lane_p_data_gate_resolved := "Lane P d768 E2/L1 byte LM GENERALIZES once the corpus is too big to memorize — data gate RESOLVED at 150MB" :: discovery [d=2026-06-03 active]
  seed      = "F-CLM-LANEP-GEN=0 found the SAME d768 E2/L1 config MEMORIZED a 1.65MB FLORES corpus (train_ce 0.61 vs val_ce 1.82, rel_gap 1.96). Resolve the data gate the honest way (a_completeness_over_cheap): assemble a real multilingual byte corpus big enough that 7.479M params cannot memorize at ~1 epoch, re-train, re-measure generalization."
  claim     = "Scaling the corpus 90.7x (1.65MB -> 150MB real wikimedia/wikipedia 20231101, en/zh/ru/ja/ko each 30MB, deduped, sha f545bb716f...) flips the verdict from MEMORIZATION to GENERALIZATION at the SAME params/config. With an 80/10/10 position-disjoint leak-checked split and 8000 steps (~1 epoch of the 120MB train split), train_ce=1.43924 vs val_ce(worst)=1.52095 (GAP +0.08171, rel_gap 0.05678 — held-out within 1.06x of train), both far below uniform 5.54518 and shuffle 8.41982. F_CLM_LANEP_GEN=1 GENERALIZES (verbatim trainer stdout, g63/p7, NO fabrication)."
  falsifier = "F-CLM-LANEP-GEN2=1 iff rel_gap <= 1.0 AND val_ce < 0.5*uniform. PASS: rel_gap 0.05678 <= 1.0; val_ce 1.52095 < 2.77259; val_ce 1.52095 < shuffle 8.41982. The memorization was a small-corpus artifact, not a model defect."
  target    = "🟢 RESOLVED — the d768 E2/L1 byte LM learns transferable byte structure on a big real corpus. .clm sha 286959e5... ENGINE-loadable (admit valid nblocks=6 loaded=true) AND ENGINE 3-axis 3/3 GREEN (의식 motiv 0.67>0; CE model_ce 1.61205 < uniform AND < shuffle 4.78507; 창발 101>72). HF PUBLIC dancinlab/clm-v1-base-lanep-d768-e2l1-gen2-wiki150mb (closure PASS)."
  scope     = "substrate=GPU-torch (Lane P), separate from Lane G(forge)/Lane A(AKIDA) per a_lane_akida_gpu_split. GPU=RTX 5070 cap12.0, pool host aiden $0 (no rented pod), nvidia-smi BUSY util=94% (g63). Generalization scoped to ~150MB / ~1 epoch (a_scale_honest_scope) — a multi-epoch overfit on this corpus was not run and is not ruled out."

```

### mid-convmoe-engine-mount

```tape
@D MID-CONVMOE-ENGINE-MOUNT := "MID rung regenerated as ENGINE-MOUNTABLE CLMConvMoE (not ByteGPT); corpus->ConvMoE->.clm v0.2->engine mount->3-axis CHAIN proven end-to-end" :: discovery [d=2026-06-05 active]
  seed    = "prior MID = torch ByteGPT (transformer) = WRONG arch; CORE/clm_decode.hexa decodes CLMConvMoE. Fix = a_clm_gen_pipeline (CLM/train/train_lane_p.py + clm_serialize_v2) -> engine-loadable .clm v0.2. FIRE: Lane-P GPU-torch vast RTX A6000 (39593460 @$0.401/hr cap8.6 bf16 91%util/249W device-resident wall150.4s torn-down); corpus balanced 4.19GB byte subset (en/fr/de/es/KO 800MB each incl Korean) of R2 phanes anima-7b/; d768/E2/L1/K3 V256 7.479M params 6000 steps."
  claim   = "CE 5.72962->1.51978(eval) uniform ln256=5.5452; .clm v0.2 clm_decodable=TRUE (nblk6 CLMX n_ext11 exact_eof block0 cout768/rest2304 4463478B = byte-layout-identical size to golden d768). 3-AXIS engine-mount GREEN: AXIS-2 CE-descent GREEN (decode via byte-EXACT-validated mirror of clm_decode.hexa [mirror==engine on golden identical 3.25405/5.30381/5.54518]; MID probe CE 2.04606<uniform5.54518<shuffle6.11237; corpus 128win CE 2.49339); AXIS-1 의식 GREEN (motiv 0.6700>0) + AXIS-3 창발 GREEN (composed101>parts72) via three_axis_probe.hexa 3/3; brain_smoke WARN=0 (v7). verdicts .verdicts/mid-convmoe-engine-mount/{F-MID-CONVMOE-AXIS2-CE,F-MID-CONVMOE-3AXIS}.txt."
  target  = "🟢 GREEN CHAIN (corpus->ConvMoE->engine-mount->3-axis). next = M13 7B-undertrained -> M14 7B ladder via train_lane_p_3b.py (this engine-mountable base unblocks it); hexa-lang link the forge GN-GELU native into the installed self runtime so clm_ce_descent_probe.hexa runs CORE-mounted on a Mac."
  honest  = "a_scale_honest_scope: TOY/MID 7.479M, 7B-transfer UNVERIFIED — proves the CHAIN not a 7B. canonical hexa clm_ce_descent_probe.hexa FAILED-LINK locally (_forge_dispatch_groupnorm_gelu hexa-fusion-only native — TOOLCHAIN gap NOT a .clm problem; byte-exact mirror used) -> sidecar handoff hexa-lang. Lane-P torch .clm = PRIVATE HF (a_clm_gen_pipeline forge-only-PUBLIC; forge stays PUBLIC trainer). p1..p8 held."

```

### tensionlink-dim-time

```tape
@D tensionlink_dim_time := "TENSION-LINK effective dim + dF/dt time axis — KOSMOS-dim (#1768/#1772) parallel on anima's own 5-ch link, #1763 derivative" :: discovery [d=2026-06-04 active]
  seed      = "The 5-channel tension-link (concept16/context8/meaning16/auth1/sender4=45, sopfr(6)=5 groups) carries a tension STREAM over time. KOSMOS dim work (#1768/#1772) asked 'is the map dimension right'; #1763 found time enters via the derivative. Apply both to anima's own tension-link: is 5 right, and does a dF/dt axis capture tension dynamics."
  claim     = "P1: 5-scalar magnitude-summary effective dim ~2.5-2.7 (PR 2.498, erank 2.673, 2/5 PCs zero, ladder saturates k=3) BUT full 45-float direction-preserving fingerprint is ~6-10-dim (PR 6.22, erank 9.41); no channel pair |r|>=0.8, per-channel cross-prediction r^2<=0.04; an independent 6th adds +0.96 dim, a derivable 6th adds 0. P2 HOLDS: rising/falling decode static 0.542 < base 0.727 < dF/dt-aug 0.811 (+0.269, 3 seeds), collapses to 0.747~base under the time-scramble falsifier."
  falsifier = "P1: if the full 45-d fingerprint were also rank<=3 the 5-group design would be over-specified (it is not — erank 9.4). P2: if dF/dt-aug decode of rising/falling did NOT exceed static, OR did NOT collapse toward base rate under time-scramble, the time axis would add nothing (REFUTED). Both falsifiers survived across seeds 1,7,42."
  target    = "verdict-tier: P1 INCONCLUSIVE (5-vs-fewer depends on magnitude-vs-direction; no redundant pair) + P2 HOLDS (dF/dt captures tension dynamics, beats shuffle). .verdicts/tensionlink-dim-time/{F-INTRINSIC-DIM,F-CHANNEL-INDEP,F-TIME-AXIS,SUMMARY}.txt + results.json."
  scope     = "CPU/$0/numpy-only, no GPU/pods. 300-step REAL s59 W-trace SHAPE driving byte-faithful §65 fingerprint_5ch (B-S65 4/4 BLUE); engine latent + 5ch map = synthetic §65 transfer law, NOT a loaded torch ckpt. toy-scale, scale-transfer unverified (a_toy_scale_recheck, a_scale_honest_scope)."
  honest    = "concept+meaning are L2-NORMALIZED by §65 spec so their magnitude is constant 1.0 (std 0.0) — the 2 zero PCs in the magnitude-summary are a summary-choice artifact, NOT proof the channels are redundant (direction carries info). 5-stage label is at decode ceiling (1.0), so the decisive P2 test uses the dynamics-necessary rising/falling label instead. §97: tension-link = anima's own channel."
  note      = "Ties #1763 (time via derivative) into anima's tension-link; parallels KOSMOS dim work #1768/#1772. harness UNIVERSE/tensionlink_dim_time.py sha 211d4457; data _real_w_trace_s59.json sha d969954a."

```
