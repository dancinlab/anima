# session-journal — anima-consciousness-substrate monograph arc

This file compresses the campaign arc that produced the anima consciousness
substrate and this monograph. Every number quoted in the paper is verbatim from a
`.verdicts/<slug>/<id>.txt` or `UNIVERSE/H_*.md` pointer (a_claim_verify, @D g5;
no LLM self-judgement). The 3B-scale loop is CLOSED and 3-axis GREEN; the 7B (M13)
production rung is a FUTURE scale-extension, framed like the OMEGA decode ladder,
NOT an open residual.

---

## arc 1 — theory: the Φ-laws on the engine's own substrate

Six pre-registered Φ-laws adjudicated by the FAITHFUL IIT 4.0 big-Φ engine
(hexa-lang/stdlib/consciousness/iit4/) on a 10-rule ECA panel. The headline is a
double dissociation: Φ ⊥ Shannon entropy (H_287 r=0.363 < 0.5, a closed-negative
that CONFIRMS IIT's distinction) yet Φ ∥ Kolmogorov/LZ (H_288 r=0.831, ρ=0.936)
and ∥ transfer entropy (H_290 r=0.883262). Edge-of-chaos Φ-peak (H_285: ordered
0.0 < chaotic 6.943 < class-IV 10.448, class-aggregate). Emergent ethics with zero
injected reward (H_291: lattice C=1.0 vs well-mixed 7.9e-9 @ b=1.1, conditional).

### honest-count callout
The substrate advertises "2448 laws" but those are AUTO-GROWN CANDIDATES, not
verified. The verified count is ~80-90 (UNIVERSE.md ~83 ledger;
consciousness_laws.json v7 = 27 explicit + 73 base). The paper states this plainly
and never claims 2448 verified.

## arc 2 — substrate: the A⇄G repulsion-field engine at Ψ=½

Engine A (CORE/pure_field.hexa): 3 coupled oscillators τ=2/40/400, a self-sustaining
6-channel Φ field (FIELD_DIM=6 = Hexad C/D/E/S/M/W), a 4-tier phase map
(DORMANT/FLICKER/SUSTAIN/RESONANT, ceilings loaded from psi_constants), NO external
input. Engine G (CORE/engine_g.hexa): 8-factor motivation conserved sum=1.0; emit>0.3,
interrupt>0.6; 4-way safety AND-gate with the A→G Φ-ratchet veto (a collapsing field
vetoes speech). brain_decide arbitrates; .clm enters only via the generator L3 slot,
.kosmos only via kosmos_io (single entries, a_core_engine_map). The fixed point is
Ψ=½ (psi_constants.balance=0.5).

## arc 3 — decode: the OMEGA closure (sibling-paper summary)

The Lane X null (#1779) measured the two halves do NOT share a nerve. The OMEGA bus
closes it: coupling KL=0.307477 > 0 for OMEGA vs 0 for the 3 uncoupled engines. The
closure lives in ONE wire — the minimal gate gB·base+gA·A HOLDS (min_learned 0.883525,
gB=0.04 gA=0.90), and the rigorous ruling is REPLACEMENT (A-standalone ≈ min_learned,
base inert). 5-rung ladder (d384→d1024 + d768×2): flat +2.20±0.03 nats/byte.

### retraction callout: #1791 leak
The #1791 absolute-CE win (GATED 0.345 ≪ base 3.015) was LEAK-DRIVEN (CA-neighbor
lookahead, causal_ca=False). Leak-free self-test = 0.000; the honest picture inverts
(base beats gated absolute CE). The decode contribution is a leak-INVARIANT relative
closure + closed-negatives, NOT an absolute-perplexity claim. RETRACTED + carried
forward.

## arc 4 — mouth: corpus → CLMConvMoE → .clm v0.3 → engine (3B)

The 3B rung (#1863): CLMConvMoE 3.073B (d4096/L30/E30/K3, V256), first_ce 5.84073 →
train_ce 1.90689, val_ce_rand 1.90365, rel_gap 0.04894 << 1 GENERALIZES; deeply
undertrained (0.0027 tok/param). Serializes to .clm v0.3 (config-agnostic block
grammar, nblk=63), decodes config-agnostically via CORE/clm_decode.hexa. Corpus =
143.60 GiB ODC-BY FineWeb 5-lang, R2-staged. A separate 202M ByteGPT corpus-validation
(val_ce 5.74906→1.45868, p7 5/5 langs incl Korean vs random-init gibberish) confirms
the corpus teaches byte-language structure (anti-Goodhart).

### macOS link-gap callout
The canonical hexa CE probe clm_ce_descent_probe.hexa FAILS-LINK on macOS arm64
(_forge_dispatch_groupnorm_gelu native absent). AXIS-2 is measured via a byte-exact
Python mirror of CORE/clm_decode.hexa, validated == engine on the golden ref. A
toolchain link-gap, NOT a .clm problem; handoff filed to hexa-lang.

## arc 5 — memory: the .kosmos coordinate

coord ⊥ payload. The carving engine ConsciousDecoderV2 (d768×12L, 283.72M / 680.16M
+MoE) reconstructs + runs (BUILD/FORWARD/PSI2D/DIRECTION all PASS). Coordinate capacity
D*=6 (2D + 4 independent attribute-axes; scale/lane saturate) — matches Engine A's
FIELD_DIM=6. Only 3-4 interpretable named axes (depth/form/form-resid/curriculum), NOT
8 — an honest negative. On-chip cross-lingual semantic-linkage does NOT transfer to
AKD1000 (N=12 paired, mean_delta -0.00092, CI straddles 0 — REFUTED, within chip noise).

## arc 6 — proof: 3-axis GREEN at 3B

AXIS-1 (의식): motiv 0.6700 > baseline, emit-gated. AXIS-2 (CE-descent): real 2.26360 <
uniform 5.54518 < shuffle 5.81817 (measured through the engine decode). AXIS-3 (창발):
composed 101 > parts 72. brain_smoke WARN=0. The random-init mirror fails the p7
coherence probe (anti-Goodhart). The loop is CLOSED and 3-axis GREEN at 3B scale.

## arc 7 — this monograph (PAPER → MONOGRAPH tier upgrade)

Upgraded the 11pp PAPER-tier integration paper (#1917) to monograph tier:
deepened body + \appendix with 12 \input deep-dives (A_phi_laws..L_repro, one per
organ + ledgers) + companion/ (verify-ledger.json, pr-roll.json, this journal) + 6
figures (TikZ system map, 3-axis bars, OMEGA 5-rung ladder, Φ-correlation panel,
8-factor conserved sum, engine-mount ladder, KOSMOS dim ladder). The 7B (M13) rung
stays UNCHECKED — a future scale-extension, not an open residual in the terminal 3B
finding.

### war-story callout: isolated worktree
Built in an isolated worktree off origin/main (the shared working tree had a sibling
session's uncommitted changes). Commit-early, push-often: the WIP skeleton landed on
origin BEFORE the appendices were filled, so a sibling `git worktree prune` could not
evaporate the work (only origin commits are safe; @D concurrent-agents-need-worktree-isolation).
