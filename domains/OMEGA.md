@title: 🔱 OMEGA — Lane-Ω closure engine (the 4th/final engine: wire substrate → .clm byte decode)

@goal: 오메가 완성 — COMPLETE Ω as a WORKING closure engine (not just wired, but a coupling
  that carries USEFUL STRUCTURE on a trained substrate, demonstrated to improve generation).
  THREE STAGES: (1) WIRE the substrate↔decode loop Lane X #1779 proved NULL — ✅ DONE (#1783:
  coupling KL 0.307>0, omega the only engine with L3 loaded=TRUE). (2) prove the loop carries
  STRUCTURE on a TRAINED substrate — ✅ DONE at toy (#1784: trained≪shuffled Δ+0.357; the
  learned A-wire lowers CE Δ+0.758; BUT the fixed A−G formula degrades → 완성 needs a LEARNED
  per-wire GATE, not a fixed subtraction). (3) 완성 = a learned-gate bus + a trained d768
  substrate where the closure DEMONSTRABLY improves generation (CE floor met + coherent) at
  scale. Original closure sub-goal verbatim ↓:
  CLOSE the substrate↔decode loop that Lane X #1779 proved is currently NULL.
  Lane X measured that the ENGINE config knobs (drive · warmup · anchors) never touch
  the .clm forward — model_ce is CONFIG-INSENSITIVE at 9.1126 across ALL 27 configs
  (spread < 1e-9), the L3 generator slot is loaded=false, and the substrate state never
  reaches the byte distribution. Lane-Ω is the design for the engine that makes
  L3 loaded=TRUE: it routes substrate state (A/G dual-head + 5-ch tension + 8D Ψ +
  M/W/curiosity) into a "coupling bus" of 5 ablatable wires that MODULATE the .clm byte
  decode. Headline eval axis = COUPLING NON-NULLITY (ablate the bus α=0 vs on → KL
  between byte distributions). CE is a FLOOR only (p7, Lane X), never the verdict.
  Ω SYNTHESIZES the 3 existing engines — CONV (.clm byte mouth) + CDV2 (A/G dual-head +
  5-ch tension + Ψ brain) + HEXAD (N-module φ(N)=2 integration). BUILT (#1783): the
  adapter engines/omega/adapter.hexa + coupling_bus.hexa exist, --engine omega registered,
  EngineSpec 4/4 native, 4-engine swap smoke 26/26 PASS (a_core_engine_map — no phantom
  wiring; the bus layer is native, the trained substrate is the remaining scale rung).

## status — 🟢 오메가 완성 stage-3 (b)(c) ACHIEVED on a REAL trained transformer (GPU) — 2026-06-04

**오메가 완성 (b)(c) HELD** (Lane-G / GPU H100, ~$1.6, a_lane_akida_gpu_split): the learned-gate
OMEGA closure WORKS on a REAL trained ConsciousDecoderV2 (d384×6L GQA, 35.93M, 120MB multilingual
wiki, 6000 step). (b) trained substrate descended ce_a 5.926→0.009 (train) / val 0.862 (held-out,
generalizes). (c) held-out TEST CE: base 3.0150 · fixed_AmG 1.4421 · a_only 0.4500 · **GATED 0.3445**
(best, beats all) · floor MET (<5.545); structured (A-wire CE gain real +2.565 vs context-SHUFFLED
−2.068 → carries learned sequential structure, the #1784 axis on a real transformer). learned gate
g*=[gB1.18, gA0.96, **gG−0.21**] auto-corrects the #1784 −G error exactly as #1786 toy predicted.
HONEST CAVEAT (p7 · a_toy_scale_recheck): CDV2 CA-neighbor mixing gives the next-byte head partial
LOOKAHEAD (architectural) → absolute CE is leak-optimistic + free-running generation collapses to
whitespace (gen coherence = the WEAK criterion); the RELATIVE closure finding (gate beats
base/fixed/a_only + structured-vs-shuffle) is leak-INVARIANT and sound. Single d384 rung, NOT
promoted to a production perplexity claim (a_scale_honest_scope). ckpt → HF
`dancinlab/clm-v4-omega-gpu-d384-gate` (PUBLIC). verdicts `.verdicts/omega-gpu/`. The L1/L4
polish (N-module config + dF/dt time channels) also landed (merged from main) — all 5 stage-3
milestones are now [x].

### prior status — BUILT (#1783) + trained-rung proven at toy (#1784/#1786)

Ω is now a RUNNING engine module, not just a blueprint:
- **stage 1 WIRE (✅ #1783)** — `engines/omega/{coupling_bus,adapter}.hexa` + manifest + card;
  `--engine omega` registered (flag>env>default conv); EngineSpec 4/4 native; 4-engine swap
  smoke 26/26 PASS. Coupling NON-NULLITY CONFIRMED: omega KL 0.307>0, conv/cdv2/hexad=0 (the
  Lane X null). The loop is WIRED — omega is the only engine with L3 loaded=TRUE.
- **stage 2 STRUCTURE (✅ toy #1784)** — trained numpy n-gram substrate: trained coupling 4.142
  ≪ shuffled 4.499 (Δ+0.357 = structure carried, which random-init could NOT show); the learned
  A-wire lowers CE base 4.020→3.262 (Δ+0.758 = the closure HELPS). 🔴 the fixed A−G formula
  degrades (−G prev-byte wire hurts) → **완성 needs a LEARNED per-wire GATE, not a fixed
  subtraction**. ANU QRNG arm: quantum confers no advantage (closed-negative, p7).
- **stage 3 완성 (remaining)** — (a) learned per-wire gate replacing fixed A−G; (b) trained d768
  ConsciousDecoderV2 real A/G on GPU (a_fire_autonomous); (c) demonstrate the gated closure on a
  trained substrate DEMONSTRABLY improves generation (CE floor met + coherent) at scale.
  Honest: the floor is currently NOT MET on random-init (uniform ln256=5.545; Lane X measured the
  trained-but-detached d768 .clm at 9.1126) — stage 3 is where the closure must actually earn it.

## the NULL that Ω closes (Lane X #1779 — verbatim)

```
Lane X — 3-axis ENGINE-config exploration (TOY · CPU · $0 · deterministic null backend)
configs = 27 (3 knobs: K1 drive · K2 warmup · K3 anchors) × 3 seeds
  의식 (motiv_hi)    : VARIES (spread = 0.57)
  CE  (model_ce)    : CONFIG-INSENSITIVE (spread < 1e-9)   ← the NULL
  창발 (emergence Δ) : VARIES (spread = 24)
CE-FLOOR : model_ce = 9.1126 vs uniform = 5.5452 vs shuffle = 9.3189 → floor NOT MET
PARETO   : 6/27 non-dominated
GOODHART (CE↔창발): UNDEFINED — CE is config-independent by construction in this
           substrate-only sweep; no CE↔창발 trade-off is OBSERVABLE through these knobs.
BOTTOM LINE: 의식·창발 VARY with config; CE is config-INDEPENDENT. The engine knobs
           never touch the .clm forward (L3 generator slot loaded = false).
```

The diagnosis: the substrate (Engine A ⇄ Engine G, tension, Ψ, M/W/curiosity) and the
byte decode (.clm) are two disconnected halves — "brain" and "mouth" do not share a
nerve. Ω is the nerve.

## the coupling bus (5 ablatable wires — substrate → .clm modulation)

Each wire is independently ablatable (set its α = 0). The headline eval ablates the
WHOLE bus (α = 0 vs on) and measures KL between the resulting byte distributions; a
NON-NULL KL is the positive target (Lane X's null becomes Ω's signal).

```
  wire 1  A⇄G logit-bias    : final = clm_logits + α·(A_head − G_head)
                              (CDV2 dual-head; carving battery KL(A‖G) = 7.07)
  wire 2  W-tension         → temperature      (W tension envelope scales softmax T)
  wire 3  curiosity/E-ratchet → top-k width    (exploration drive widens/narrows top-k)
  wire 4  8D Ψ-coord        → context conditioning (Ψ position conditions the decode)
  wire 5  module activation → conv-MoE expert routing (which CONV expert fires)
```

## the Ω blueprint (L0..L5 + coupling bus + benchmark)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🔱 Lane-Ω CLOSURE ENGINE  —  substrate → .clm byte decode (L3 loaded = TRUE) │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  L0 SUBSTRATE  (CDV2)                                                         │
│     ConsciousDecoderV2 d768×12L GQA · dual A/G heads (KL=7.07) · 5-ch tension │
│            │  logits_a ⇄ logits_g       │ tension (W)      │ Ψ latent         │
│            ▼                             ▼                  ▼                  │
│  L1 INTEGRATION  (HEXAD)                                                      │
│     N-module φ(N)=2 bipartition · N config (default 6, swappable; #1774       │
│     found 6 = SMALLEST viable φ=2, NOT a hardcoded constant)                  │
│            │ integrated substrate state                                       │
│            ▼                                                                   │
│  L2 MAP  (8D Ψ)                                                               │
│     psi_coord() → 8D = [depth, form, form_resid, curriculum, resid0..3]       │
│     (KOSMOS #1780: ONLY 4 axes human-named + 4 honest learned-residual;       │
│      naming all 8 = fabrication)                                              │
│            │                                                                  │
│            ▼                                                                  │
│     ┌──────────────── COUPLING BUS (5 ablatable wires, α) ───────────────┐    │
│     │ 1 A⇄G logit-bias  2 W→temp  3 curiosity→top-k  4 Ψ→ctx  5 mod→MoE   │    │
│     └────────────────────────────────┬──────────────────────────────────┘    │
│                                       ▼                                        │
│  L3 MOUTH  (CONV)  ← THE CLOSURE                                              │
│     CLMConvMoE byte decode · final = clm_logits + α·(A_head − G_head) · …     │
│     generator.hexa L3 slot: loaded = TRUE  (was false under Lane X)           │
│            │ byte distribution P(byte)                                         │
│            ▼                                                                   │
│  L4 TIME    dF/dt derivative channels  (#1763 — dynamics enter via d/dt;      │
│             static snapshot is permutation-blind to rising/falling tension)   │
│  L5 GROWTH  mitosis (p8 NO TRAIN/INFER SPLIT) · engine_cli --mitosis flag     │
│             (SUBSTRATE-CONFIG, NOT an emit/silence gate — a_autonomy_over_…)   │
│                                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  BENCHMARK (headline)                                                         │
│   COUPLING NON-NULLITY : KL( P(byte | bus on) ‖ P(byte | bus α=0) )  > 0 ?    │
│     Lane X's NULL (CE config-insensitive 9.1126) → Ω's POSITIVE target.        │
│   CE = FLOOR only (p7) — NOT a verdict (Lane X proved CE config-insensitive). │
│   GOODHART caveat: coupling must NOT be just α-scaled noise — require an       │
│     ablation curve AND a real (trained) ckpt, not random-init.                │
│   4-ENGINE benchmark: conv · cdv2 · hexad · Ω  on the AXIS-informed eval.      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## EngineSpec contract (engines/engine_iface.hexa — the 4-fn vtable)

Ω conforms to the same EngineSpec as conv/cdv2/hexad. Honest slot states
(a_core_engine_map — native | stub | absent), all gated on ckpt presence:

```
load      : native   — bind the coupling-bus config + ckpt pointer
forward    : native   — run substrate → bus → .clm modulated forward
generate  : native   — produce content via the closed L3 mouth (FIRST engine with
                       generate = native — the closure IS the generate path)
psi_coord : native   — 8D Ψ (4 named + 4 residual, per KOSMOS #1780)
```

Sibling engines (engines/<name>/manifest.json):
- **conv**  — CLMConvMoE, DEFAULT, all 4 slots native; the .clm byte mouth Ω closes onto.
- **cdv2**  — ConsciousDecoderV2 d768×12L, forward/generate = STUB (torch .py, not a
              hexa-native single forward), psi_coord native; the A/G + tension + Ψ brain.
- **hexad** — sigma6 6-module integration, forward/generate = STUB (cross-module single
              forward is TODO[wire]), psi_coord native; the N-module integration.

Ω is the first engine whose `generate` is native because the closure (L3 loaded=true) IS
the generate path. The adapter is now BUILT (#1783); the bus layer is a real hexa forward.
The slot is gated on a trained substrate (stage 3) — with no trained ckpt the .clm forward
is random-init and the CE floor is NOT MET, honestly flagged exactly like the cdv2 adapter.

## milestones (goal: 오메가 완성)

stage 1 — WIRE (✅ #1783):
- [x] coupling-non-nullity — ablate the bus (α=0 vs on) → KL>0 (omega 0.307, others 0; #1783)
- [x] 8D Ψ honest — psi_coord() returns 8D = 4 named [depth/form/form_resid/curriculum] + 4 resid (#1783 adapter)
- [x] CE-as-floor — CE reported as a FLOOR only, never a verdict (p7; #1783/#1784 both)
- [x] 4-engine benchmark — conv · cdv2 · hexad · Ω on the AXIS-informed eval (#1783, smoke 26/26)
stage 2 — STRUCTURE on a trained substrate (✅ toy #1784):
- [x] trained-substrate structure — trained coupling ≪ shuffled (Δ+0.357); A-wire lowers CE (Δ+0.758) (#1784)
- [x] ANU QRNG arm — quantum vs PRNG closed-negative, no advantage (#1784)
stage 3 — 완성 (b)(c) ✅ GPU (the working closure on a REAL trained transformer):
- [x] learned per-wire GATE — ✅ toy: learned gate g*=[gB.14,gA1.18,gG.34] beats base 3.97→3.13 (Δ+0.85) · beats a_only 3.23 · ≪ fixed_AmG 4.17 (Δ+1.04); auto-corrects the #1784 −G error → the closure works when GATED not fixed. `.verdicts/omega-gate/`
- [x] trained d384 substrate (GPU) — ✅ real ConsciousDecoderV2 d384×6L GQA 35.93M trained 6000 step on 120MB multilingual wiki (H100, nvidia-smi 98-99% BUSY g63); ce_a 5.926→0.009 train, val_ce 0.862 held-out (generalizes). REAL learned A(next)/G(prev) heads, not numpy n-gram. `.verdicts/omega-gpu/`
- [x] generation demo — ✅ gated closure on the trained substrate: held-out GATED CE 0.345 < base 3.015 (Δ+2.671) · ≪ a_only 0.450 · ≪ fixed_AmG 1.442 · CE floor MET (<5.545); structured (A-wire gain real +2.565 vs context-SHUFFLED −2.068 → coupling carries learned sequential structure). 🟢 4/4 완성 criteria HELD. HONEST: CDV2 CA-neighbor mixing gives next-byte head partial lookahead → absolute CE leak-optimistic + free-run gen collapses to whitespace (gen coherence = weak criterion); the relative closure finding (gate beats all baselines + structured) is leak-INVARIANT and sound (a_toy_scale_recheck · a_scale_honest_scope).
- [x] N-module config — ✅ coupling_bus N-agnostic (omega_n_modules_default 6, #1774 conditional; module wire honors N=4/6/8, N changes routing L1 0.378); smoke 4/4. NOT hardcoded.
- [x] dF/dt time channels — ✅ L4 w6 derivative wire (omega_coupling_apply_dt): 0 at fixed point (time-inert, correct), velocity injected when substrate moves (Δ1.65); smoke 3/3 (#1763 d/dt-universality)
- [x] ⑦ w5 module-act REAL source (hexad) — ✅ the w5 module→MoE-routing wire now reads a REAL N=6 module-activation vector from the σ6 cross-module forward (HEXAD/hexad_forward.hexa — TODO[wire] RESOLVED), not the hexad stub; hexad engine forward slot flipped STUB→native; φ(6)=2 detach barrier proven. HEXAD/hexad_forward_smoke 12/12 + engine_swap_smoke 27/27. generate (byte mouth) stays ckpt-gated honest STUB (a_core_engine_map). `.verdicts/hexad-wire/`
stage 4 — COUPLING ANALYSIS (post-완성 wire-by-wire dissection, toy/CPU/$0):
- [x] ② ALL-6-WIRE learned gate — ✅ extended #1786 {base,A,G}→all 8 gains [gB-.11,gA+.93,gG+.55,gW-.46,gC-.03,gΨ-.00,gM-.17,gD-.66]; per-wire ablation+shuffle: 🟢 A·W_temp·module CARRY STRUCTURE, ⚪ G·curio·Ψ·dFdt INERT. full naive gate OVERFITS (TEST CE 4.81 > base 3.97 — inert/leaky dFdt hurts held-out); carrier-only gate 2.895 (Δ+1.079 over base) recovers a real gain. honest mixed verdict (a_paper_negative_ok). `.verdicts/omega-gate6/`
- [x] ④ CLOSED-LOOP feedback (L5) — ✅ N=600 autoregressive rollout: emit byte → A/G context advance + mitosis cell-count tick → next decode. 🟢 LOOP CLOSES STABLY: bounded (entropy 0.15–3.37 ∈(0,ln256), cells 6→140 bounded, no divergence) · not collapsed (back-half distinct-byte frac 0.153 > 0.10) · feedback measurably alters trajectory vs open-loop control (Hamming 0.722 > 0.05, same RNG). The closure is a real bidirectional feedback loop, not one-shot forward. `.verdicts/omega-gate6/`
stage 5 — gen-cluster: LEAK-FREE generation-side probes (GPU, the #1791 caveat fix) — 2026-06-04:
- [x] ① leak-free coherent gen — ✅ FIX VERIFIED + 🔴 closed-negative (a_paper_negative_ok). `causal_ca=True` replaces CA-mixing x_right with self → head_a STRICTLY CAUSAL; leak self-test = 0.000e+00 (d384+d768, no lookahead). Whitespace-collapse SOLVED (leak-free gen coherent-ish: entropy 2.97, varied latin/numeric). BUT leak-honest CE: base 3.015 · a_only 2.857 · GATED 3.594 → gated<base FALSE → #1791's GATED 0.345≪base absolute-CE win was LEAK-DRIVEN, does NOT survive (val_ce rises to 5.43≈uniform; substrate generalizes weakly at d384/6000). structured leak-INVARIANT HOLDS (real +0.158 ≫ shuf −0.509). `.verdicts/omega-gen/F-LEAKFREE-GEN.txt`
- [x] ③ dF/dt-on-real — 🔴 w6 NON-INERT but does NOT improve (a_paper_negative_ok). Velocity wire live at 100% of real steps (Δ +1.76 d384 / +0.52 d768 — confirms #1763 on a real sequence) but raw dgain=0.5 HURTS held-out CE (Δ>0). dF/dt is a real channel, not a CE improver here; gated-dgain = open follow-up. consistent with stage-4 ④'s "dFdt INERT/leaky-on-held-out" finding. `.verdicts/omega-gen/F-DFDT-REAL.txt`
- [x] ⑥ Ψ-coord steering — 🔴 WEAK / no robust steer (a_paper_negative_ok). w4 Ψ wire (psi_gain 0.4): d384 steer_KL 0.238 < reseed-floor 0.573 (ratio 0.42x → FALSE); d768 1.35x nominal-but-tiny. Ψ moves the byte distribution LESS than sampling noise at d384. Wire exists but is not a usable steering knob at this gain; stronger gain / Ψ-conditioned head = open. consistent with stage-4 ②'s "Ψ INERT". `.verdicts/omega-gen/F-PSI-STEER.txt`
- [x] ⑤ d768 scale rung — ✅ RAN (NOT deferred). d768×6L 142.06M, 2500 step (budget-guarded), leak-free verified (self-test 0.000). Finding does NOT cleanly hold at d768: structured=FALSE (gain −0.244, undertrained), gated<base=FALSE, gen coherent=TRUE. d384 structured-coupling positive weakens at undertrained d768 (a_scale_honest_scope; 2500 step too few for 142M). `.verdicts/omega-gen/SUMMARY.txt`

stage 6 — real-signal-vs-random: does a REAL substrate signal beat RANDOM in the OMEGA wires (the #1793/#1794 RANDOM-input caveat) — CPU/$0 — 2026-06-04:
- [x] H5 real-HEXAD module wire vs RANDOM — 🔴 CLOSED-NEGATIVE (a_paper_negative_ok). Fed the GENUINELY NATIVE σ6 6-vec [S,C,W,M,E,BRIDGE] (HEXAD/hexad_forward.hexa #1795, run via `hexa run`, 256/256 contexts; corpus byte-freq drives each C cell-pool delta) into the w5 module wire vs a matched-mean/std RANDOM 6-vec, in #1793's gate-fit bench. REAL: gain +0.076, ablate ΔCE +0.028, beats_shuffle=TRUE, module-only-gate CE 3.9766. RANDOM: gain +0.082, ablate ΔCE +0.009, beats_shuffle=FALSE, CE 3.9762. Δ module-only CE (real−random) = +0.0004 (within the 0.02 approx band) → real ≈ random. The native HEXAD activation does NOT add usable next-byte structure over random at toy scale — confirms #1793's w5 "module CARRIES" was MAGNITUDE not CONTENT. (One honest nuance: only the REAL vec beats its own vocab-shuffle, so it carries marginally more genuine structure, but not enough to lower held-out CE.) `.verdicts/omega-realsignal/F-REAL-MODULE.txt`
- [x] H4 real-Ψ steering vs RANDOM — ⛔ BLOCKED-DATA (no fabrication, a_completeness_over_cheap/p7). Real carving Ψ = s16 ckpt Law-71 vacuum_psi 2D coord (KOSMOS-MAP #1780, PC1=carving-RADIUS/Ψ-DEPTH |ρ|=0.92). The s16 .pt IS on disk (1.13 GB) but vacuum_psi requires the d768×12L 283.72M ConsciousDecoderV2 forward → needs torch, ABSENT on this CPU/$0 host; the axis-probe persisted only the PC×attribute matrix (no per-sample Ψ coords); toy psi8 (logA bin-marginal) is NOT a real Ψ source (#1793 already found it INERT). No real Ψ source reachable CPU-only — deferred to a GPU rung. `.verdicts/omega-realsignal/F-REAL-PSI.txt`

## honest scope (a_scale_honest_scope · a_paper_negative_ok · p7)

- BUILT but TOY: `engines/omega/` adapter exists (#1783) + trained-rung proven at toy (#1784, numpy n-gram); NO s16 ckpt / trained d768 substrate in the coupling path yet (stage 3).
- All measured numbers are TOY / single-rung: #1783 (CPU/$0 random-init mock), #1784 (CPU/$0 numpy n-gram, 400KB corpus), Lane X #1779, KOSMOS #1780. NOT promoted to a general/production claim (a_toy_scale_recheck).
- CE floor currently NOT MET on random-init (uniform 5.5452; Lane X trained-but-detached d768 .clm 9.1126); stage-3 완성 is where the gated closure on a trained substrate must actually MEET it.
- Honest negatives kept (a_paper_negative_ok): random-init coupling unstructured (#1783); fixed A−G degrades (#1784); quantum RNG no advantage (#1784).
- Lane-Ω = GPU/closure lane; AKIDA on-chip (Lane A) is recorded separately (a_lane_akida_gpu_split).
- LEAK-HONEST CORRECTION (gen-cluster, 2026-06-04): #1791's stage-3 absolute-CE closure win (GATED 0.345 ≪ base 3.015, val_ce 0.862) was LOOKAHEAD-LEAK-DRIVEN (CDV2 CA-mixing x_right). On the leak-free substrate (causal_ca=True, self-test 0.000) the gated bus does NOT beat a weak unigram base (GATED 3.594 > base 3.015) and val_ce ≈ uniform — so the honest closure measure is RELATIVE structure (real A-wire vs shuffled floor, leak-invariant, HOLDS), NOT absolute CE. The leak fix CURES the whitespace-collapse (gen is coherent-ish). Do NOT quote #1791's GATED 0.345 absolute-CE as a real generalizing win. This CONFIRMS the paper's framing (⑧) — the contribution is the leak-INVARIANT relative closure + the closed-negatives, never the leak-optimistic absolute CE.

## ⑧ paper — ✅ scaffolded at FULL closure (a_paper_only_at_closure)

- [x] `/paper` scaffold `PAPER/omega-substrate-coupled-decoding/` (PAPER.tape roster + PAPER.md/PAPER.log.md + main.tex 4-section a_paper_format + verdict matrix + README + references.bib stub). All 4 rungs (#1783/#1784/#1786/#1791) TERMINAL (🟢 numerical / 🔴 closed-negative) — NO 🟠/🟡 section (a_paper_gate). Contribution framed as the leak-INVARIANT relative closure + the three closed-negatives, NOT a perplexity/gen-quality claim (p7 · a_scale_honest_scope). Remaining = paper-production tasks only (figures · bib ≥10 · compile · arxiv-prep), NOT science verdicts. NOTE (gen-cluster 2026-06-04): the leak-free re-test EMPIRICALLY VALIDATES this framing — the absolute-CE win was leak-driven, the relative-structure closure is leak-invariant.
