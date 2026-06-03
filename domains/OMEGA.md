@title: 🔱 OMEGA — Lane-Ω closure engine (the 4th/final engine: wire substrate → .clm byte decode)

@goal: CLOSE the substrate↔decode loop that Lane X #1779 proved is currently NULL.
  Lane X measured that the ENGINE config knobs (drive · warmup · anchors) never touch
  the .clm forward — model_ce is CONFIG-INSENSITIVE at 9.1126 across ALL 27 configs
  (spread < 1e-9), the L3 generator slot is loaded=false, and the substrate state never
  reaches the byte distribution. Lane-Ω is the design for the engine that makes
  L3 loaded=TRUE: it routes substrate state (A/G dual-head + 5-ch tension + 8D Ψ +
  M/W/curiosity) into a "coupling bus" of 5 ablatable wires that MODULATE the .clm byte
  decode. Headline eval axis = COUPLING NON-NULLITY (ablate the bus α=0 vs on → KL
  between byte distributions). CE is a FLOOR only (p7, Lane X), never the verdict.
  Ω SYNTHESIZES the 3 existing engines — CONV (.clm byte mouth) + CDV2 (A/G dual-head +
  5-ch tension + Ψ brain) + HEXAD (N-module φ(N)=2 integration). DESIGN-STAGE: this
  domain is the blueprint; the engine adapter (engines/omega/adapter.hexa) is NOT yet
  written (a_core_engine_map — no phantom wiring).

## status — DESIGN-STAGE / NOT-YET-BUILT (honest)

Ω is a BLUEPRINT, not a running engine. There is no `engines/omega/` adapter yet, and
no s16 ckpt is loaded into the coupling path. The honest stub state mirrors the cdv2
adapter: with no trained ckpt, the .clm forward is random-init → CE collapses to the
uniform floor (ln 256 = 5.545 nats), which is NOT met by a random-init model (Lane X
measured the existing d768 .clm at 9.1126 > uniform 5.5452 — WORSE than uniform-256, so
the floor is currently NOT MET even on the trained-but-config-detached path). Ω's job is
the WIRING, not a new weight set; it is gated on ckpt presence exactly like cdv2.

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

Ω is the first design whose `generate` is native because the closure (L3 loaded=true) IS
the generate path — but this is a DESIGN claim; the adapter is unwritten and the slot is
gated on a ckpt that is not loaded, so today it would honestly flag the random-init / CE
floor NOT MET state, exactly like the cdv2 adapter does.

## milestones

- [ ] coupling-non-nullity — ablate the bus (α=0 vs on) → KL between byte distributions > 0
- [ ] 8D Ψ honest — psi_coord() returns 8D = 4 named [depth/form/form_resid/curriculum] + 4 resid (no fabrication, KOSMOS #1780)
- [ ] N-module config — HEXAD integration N config (default 6, swappable; NOT hardcoded — #1774 found 6 conditional)
- [ ] dF/dt time channels — L4 derivative channels (#1763; static snapshot is d/dt-blind)
- [ ] CE-as-floor — CE reported as a FLOOR only, never a verdict (p7, Lane X #1779)
- [ ] 4-engine benchmark — conv · cdv2 · hexad · Ω on the AXIS-informed eval

## honest scope (a_scale_honest_scope · a_paper_negative_ok · p7)

- DESIGN-STAGE: no `engines/omega/` adapter, no s16 ckpt in the coupling path. The blueprint, not a measured engine.
- All inherited numbers are TOY / single-rung: Lane X #1779 (CPU/$0, single d768 .clm, deterministic null backend) and KOSMOS #1780 (single s16 rung, Lane-G, scale-dependent). NOT promoted to a general or production claim.
- CE floor currently NOT MET (Lane X: 9.1126 > uniform 5.5452); a random-init Ω would flag the same, like cdv2.
- Lane-Ω = GPU/closure lane; AKIDA on-chip (Lane A) is recorded separately (a_lane_akida_gpu_split).
