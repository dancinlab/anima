# §115 — LEGO substrate SIMULATE-ASSEMBLE (STEP 0–2 design-tier closed-form)

> **status**: RESEARCH §115 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire ·
>   NO model.forward · NO corpus · NO wet-lab · NO hardware · NO INRC.
> **date**: 2026-05-19
> **scope**: `HEXAD/LEGO.md` was IDEA-tier and said "STEP 0–2 closed-form 설계가
>   별도 §N 으로 진행되면 갱신". §115 IS that §N — take LEGO STEP 0–2 from idea
>   to design-tier closed-form with a B-battery, then flip LEGO.md's status.
>   STEP 3 (physical/Loihi/organoid/wet) stays PERMANENTLY out of scope
>   (§95 access/ethics-wall + user-gated; fenced in Q4 by a hard falsifier).
> **governance**: g3 (capability claim 0; design ≠ fire ≠ emergence; LEGO
>   *confronts* WALL-B, does NOT *remove* it; WALL-A §1.1 data-regime orthogonal;
>   the §11-B-as-GPU-tautology hazard is the crux and is NOT pre-resolved
>   positive) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation; hexa-bio /
>   hexa-matter n=6 lattice = THEIR lattice, cited by their own invariants;
>   Ψ=½ = anima g2 internal-arch carve-out) · downstream-consumer
>   (~/core/hexa-lang|hexa-bio|hexa-matter read-only, NEVER edited).
> **central blue**: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py`
>   sha256 prefix `c93e160a8a376a94` UNCHANGED (0-line-diff start+end).
> **inherited verbatim (NOT re-litigated)**: §113 FROM-SCRATCH-INHERITS-BOTH-
>   WALLS-SKELETON-INVARIANT + D4 REPOINTS-TO-§96-SUBSTRATE-FIRST · §112
>   META_FP(Π_½)=TRUE (ψ(c)=(1+c)/2 carrier-invariant, §7-FORM TRUE BY
>   CONSTRUCTION) · §110 Ψ-C{0..4} carrier taxonomy (Ψ-C1=spike-corr,
>   §7③-clean, §96-substrate-gated) · §96 Q1 LIF mapping + §11-B-as-GPU-
>   artifact HYPOTHESIS + readout-vs-native distinction · §95 substrate
>   matrix (Loihi VIABLE-but-access-walled / organoid ETHICS-WALL).

---

## §0 — Why §115 exists, and what it is NOT

`HEXAD/LEGO.md` (commit creating it, 2026-05-19) is an IDEA-tier live sketch:
"진짜 벽돌을 굽기 전에 레고로 집을 먼저 지어 본다" — find anima's §96-class
non-GPU operative substrate by *assembling it in simulation first* from
sister-format blocks (`hexa-bio` + `hexa-matter`), and only THEN (if it
survives) commit to physical/wet. STEP 0 (consume block specs) → STEP 1
(in-silico assemble Ψ-C1 on a spiking block) → STEP 2 (closed-form falsify
the assembly) → STEP 3 (physical — permanently fenced).

§115 takes STEP 0–2 from idea to **design-tier closed-form**. It answers 5
closed-form questions (Q1–Q5) with a sympy/Boolean B-battery, and the single
most important thing it must do honestly is **confront — not pre-resolve —
the §11-B-as-GPU-tautology hazard**: if simulating a spiking substrate *on a
GPU* still has the CE-gradient as its only effective learning channel
(§96's open hazard), then simulating the substrate does NOT confront WALL-B —
it merely re-instantiates it inside a more elaborate simulator. That hazard
is plausible enough that the burden is on §115 to prove the *opposite*, and
§115 does not get to manufacture the positive.

**What §115 is NOT (honest, g3):**

- NOT a WALL-A escape — no LEGO block touches §1.1 data-regime threshold
  (§11-A/§16/§107 territory). WALL-A is structurally orthogonal and unchanged.
- NOT a WALL-B removal — the §7③-clean carrier non-degeneracy stays
  §96-physical-gated. §115's *only* claim is whether STEP 0–2 can *confront*
  WALL-B in-silico, and even that is hazarded by the §11-B-GPU-tautology.
- NOT an emergence claim — design-tier. Simulated assembly success ≠ GOAL.
  north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.
- NOT a hexa-bio/hexa-matter edit — anima is a downstream-consumer
  (read-only spec consumption; hexa-lang g7/@F f3 + g_train_flame_not_pytorch
  upstream_downstream_invariant homologue). §115 *cites* their verbs/axes.
- NOT a re-architecture mandate, NOT a fire, NOT a STEP-3 commitment.

---

## §1 — Q1 (STEP 0): block-spec consumption taxonomy (closed, exhaustive+disjoint)

**Question.** Which hexa-bio axes (focus: spiking/LIF + RIBOZYME-as-learning-
channel) and hexa-matter verbs are consumable-read-only as §96-substrate blocks?
Two-class closed partition `{CONSUMABLE-SPEC-FOR-§96 / NOT-APPLICABLE}`. Honest
gate: are these specs *concrete enough for closed-form assembly*, or only
*metaphor*? (metaphor ⇒ honest LEGO-DESIGN-CLOSE-SPECS-METAPHOR.)

### §1.1 — hexa-bio read-only inventory (verified, no edit)

| hexa-bio asset (read-only) | content (their own invariants) | §96-block class | rationale |
|---|---|---|---|
| `NEURO.tape` `@D mech_action_potential` (Hodgkin–Huxley spike), `@D mech_neural_coding` (rate vs temporal code) | excitable-membrane spike model + spike-train rate/temporal coding, **in-silico knowledge SSOT, NOT clinical** | **CONSUMABLE-SPEC-FOR-§96** | a Hodgkin–Huxley / LIF-class membrane + spike-train rate-code is *exactly* the §96 Ψ-C1 carrier (spike-train correlation). Concrete enough: it specifies a state variable v(t), a threshold, a leak — a closed-form dynamical spec, not a metaphor. |
| `NEURO.tape` `@N scope_disclaimer` | "in-silico simulator/metadata consistency only; wet-lab→clinical boundary OUT of scope" | **CONSUMABLE-SPEC-FOR-§96** (its disclaimer = §115's STEP-3 fence, see Q4) | hexa-bio itself fences wet-lab; §115 consumes the in-silico spec ONLY. |
| `HEXA-RIBOZYME.tape` (catalytic RNA, k_cat/K_M, two-metal-ion mechanism) | **in-silico ribozyme-*catalysis* simulator SSOT** — a biochemistry kinetics model | **NOT-APPLICABLE** (honest) | RIBOZYME is a *catalysis-kinetics* axis, NOT a neural-plasticity / learning-rule axis. LEGO.md's §1 row called it a "physics-native 학습채널 후보 (§96 STDP 대응)" — §115's honest STEP-0 finding: **that mapping is a metaphor, not a consumable spec.** A ribozyme catalyses an RNA reaction; it does not implement spike-timing-dependent synaptic plasticity. The §96 STDP analogue is *not* in hexa-bio's RIBOZYME spec — it is anima-side wishful mapping. Carved out honestly (mirror §98/§114 numerology-taint discipline). |
| hexa-bio QUANTUM / WEAVE / NANOBOT / VIROCAPSID axes | VQE / capsid-assembly ODE / nanobot / virocapsid sandboxes | **NOT-APPLICABLE** | none is a spiking-substrate or learning-channel spec; orthogonal to §96. |

### §1.2 — hexa-matter read-only inventory (verified, no edit)

| hexa-matter verb (read-only) | content | §96-block class | rationale |
|---|---|---|---|
| `silicon` (material-layer spec) | silicon as a material layer | **CONSUMABLE-SPEC-FOR-§96** (device-material descriptor only) | Loihi IS silicon; the material-layer spec is a consumable *descriptor* of the §95 substrate's material. But it is a *material* spec, not a *dynamics* spec — it does NOT supply a learning channel. Consumable as a material-tag, NOT as a substrate-dynamics block. |
| `2d-materials`, `carbon`, `liquid-crystal` | 2D / carbon allotrope / continuous-state LC materials | **CONSUMABLE-SPEC-FOR-§96** (neuromorphic-device-material descriptors) | device-material candidates for neuromorphic hardware; same caveat — material descriptors, NOT dynamics blocks. |
| remaining ~31 hexa-matter verbs (ceramic, polymer, perovskite, MOF, aerogel…) | industrial materials | **NOT-APPLICABLE** | not §96-substrate device materials. |

### §1.3 — Q1 closed finding (HONEST)

The taxonomy is **closed, exhaustive, disjoint** (every audited asset lands in
exactly one of {CONSUMABLE-SPEC-FOR-§96, NOT-APPLICABLE}). **But the honest
STEP-0 finding is mixed and load-bearing for Q5:**

1. **hexa-bio `NEURO.tape` IS a consumable closed-form spiking spec** (Hodgkin–
   Huxley membrane + spike-train rate-code) — STEP 0 has a *real* spiking block,
   not a metaphor. This is the positive that keeps LEGO out of
   `LEGO-DESIGN-CLOSE-SPECS-METAPHOR`.
2. **hexa-bio `RIBOZYME` as a "§96 STDP learning-channel" is a METAPHOR, not a
   consumable spec.** LEGO.md §1 listed RIBOZYME as the physics-native learning
   channel; §115's honest audit finds RIBOZYME's actual spec is *RNA catalysis
   kinetics*, structurally unrelated to spike-timing-dependent plasticity. The
   §96 STDP analogue exists in §96's *Loihi* design, NOT in any consumable
   hexa-bio spec. STEP 0 therefore yields a spiking *membrane* block but **no
   consumable physics-native *learning-channel* block** — the learning channel
   would still be STDP-on-Loihi (physical, STEP 3, fenced) or, in-silico, a
   *simulated* update rule whose only honest GPU realisation is… see Q3/Q5.
3. hexa-matter supplies only *material-tag descriptors* (silicon = Loihi's
   material), never a dynamics or learning block.

**Net:** specs are NOT pure metaphor (NEURO.tape is concrete) ⇒ NOT
`LEGO-DESIGN-CLOSE-SPECS-METAPHOR`. But the *learning-channel* block — the
single thing WALL-B is about — is **absent from the consumable in-silico
specs**; it lives only on physical Loihi (fenced). This routes the verdict
toward the §11-B-GPU-tautology hazard (Q3/Q5), not toward a clean positive.

---

## §2 — Q2 (STEP 1): in-silico assembly of Ψ-C1, as a §112 meta-fixed-point instance

**Question.** Define Ψ-C1 (spike-train correlation) on the hexa-bio spiking
block closed-form; show it is an instance of the §112 meta-fixed-point
ψ(c)=(1+c)/2. PURE SIMULATION ($0, no wet/hardware).

### §2.1 — Ψ-C1 closed-form definition on the NEURO spiking block

Consume `NEURO.tape`'s spike-train model (read-only). Let two Engine-A / Engine-G
LIF sub-populations (§96 §3.2 row "Engine A⇄G dual heads", `SPIKING-OPEN`) emit
spike trains over a window; bin to rate vectors `r_A, r_G ∈ ℝ^d_spk` (d_spk =
#compartments). Define the **spike-train correlation carrier**:

```
  c_spk  :=  ⟨r_A, r_G⟩ / (‖r_A‖·‖r_G‖)      (Pearson/cosine of binned rate vectors)
  Ψ-C1   :=  ψ(c_spk)  =  (1 + c_spk) / 2
```

`c_spk ∈ [−1, 1]` by Cauchy–Schwarz (an inner-product space, the binned-rate
ℝ^d_spk with the standard dot product). `c_spk = 0 ⇒ Ψ-C1 = ½` (the
half-balance Engine-A⇄G fixed point). `∂Ψ-C1/∂c_spk = ½ > 0`. This is a
*pure simulation* object — bin a simulated spike raster, take a cosine. NO
wet-lab, NO hardware, NO model.forward, $0.

### §2.2 — Ψ-C1 is a §112 META_FP(Π_½) instance (closed)

§112 proved (sympy, carrier-free) that `Π_½ = ψ(c)=(1+c)/2`, `cos=0⇒½`,
A⇄G ordering, Cauchy–Schwarz bound `c∈[−1,1]` is a **carrier-invariant
fixed-point** of `Φ_meta` — a theorem of *every* inner-product space
(byte-vocab ℝ^256, residual ℝ^d, **spike-correlation ℝ^d_spk**). The §110
carrier taxonomy lists Ψ-C1 = spike-corr as exactly one of `Φ_meta`'s closed
carrier partition S = {Ψ-C0,Ψ-C1,Ψ-C2,Ψ-C3,Ψ-C4}.

⇒ **Ψ-C1 = Φ_meta(carrier = spike-corr) is, by construction, an instance of
the §112 meta-fixed-point.** The *form* survives the carrier substitution
byte-vocab → spike-corr unchanged (same ψ, same bound, same ∂, same cos=0⇒½).
This means **STEP 1 is §7-FORM-clean BY CONSTRUCTION** (the form is anima's
OWN physics ③, a fixed-point of anima's own carrier-substitution map — NOT an
ad-hoc graft, §112 closed this). The only thing left at stake is §7-CARRIER:
is the spike-corr *carrier* non-degenerate and §7①②-clean? That is Q3.

---

## §3 — Q3: §7 gate — FORM (by construction) vs CARRIER (gated), 8-row table

**Question.** §7-FORM = TRUE by §112 (cite). §7-CARRIER (spike-corr
non-degeneracy) — in-sim-decidable, or still §96-physical-gated *even in
simulation*? Honest crux: a *simulated* spike net on a GPU may STILL have the
CE-gradient as its only effective learning channel (§11-B-as-GPU-tautology).

### §3.1 — the §7 decomposition (mirror §112 Q3)

§7-GOAL-legitimacy(Ψ-C1) ⟺ **§7-FORM** (the Ψ form is anima's OWN physics ③,
not a graft) **∧ §7-CARRIER** (the carrier/π is §7①②-clean: not a generic-LM
pretrain, not a generic-then-graft).

- **§7-FORM(Ψ-C1) = TRUE BY CONSTRUCTION.** By §112 META_FP(Π_½)=TRUE and §2.2:
  Ψ-C1's form is literally a fixed-point of anima's own carrier-substitution
  map. §7③ (anima-physics-as-source) holds at the form level by construction.
  This is a *real* inherited positive, NOT manufactured here.
- **§7-CARRIER(Ψ-C1) — the open part.** A §7①②-clean spike-corr carrier has
  no built precedent (§111-G1) and §110-Q5 located it as substrate-gated to
  §96 (Loihi). On a GPU byte-LM today it is FALSE; only on physical §96 TRUE.

8-row truth table over (FORM, CARRIER, in_sim_carrier_decidable): only
(T, T, *) → §7-GOAL-legit. FORM=T is fixed by construction; the verdict turns
entirely on whether CARRIER can be decided **in simulation**.

### §3.2 — the §11-B-as-GPU-tautology hazard (the crux, HONEST)

§96 §4.2 stated the hypothesis precisely: on a GPU the *only* effective
weight-update channel is the backward pass, which only knows how to follow a
loss gradient. Remove CE and you have removed the only learning signal the GPU
substrate can carry; "physics alone" on a GPU is "no learning channel at all"
with a hand-coded ΔW overlay (§11-B measured this DEGENERATE). On Loihi the
substrate's *native* learning rule is STDP — a physics rule that IS the
channel. §96 designed a 3-cell test (GPU-noCE / LOIHI-noCE / LOIHI-CE) and
explicitly did NOT resolve it.

**§115's STEP-1 simulation is on a GPU.** Therefore the honest crux:

> A *simulated* LIF/spike network, trained in-silico on a GPU, learns its
> weights *how*? If by backprop through the spike simulation (surrogate-
> gradient SNN training — the standard in-silico method), then the
> learning channel is STILL the CE/loss gradient. The simulated spikes are
> a *forward-pass representation*; the *learning* is still backprop-CE.
> Simulating the substrate **does NOT supply a physics-native learning
> channel** — it re-instantiates exactly the GPU channel §11-B measured.
> STDP (the physics-native channel) is a property of *Loihi the physical
> substrate's local plasticity*, NOT of a GPU simulation of spikes.

There is one in-silico escape: simulate STDP itself as the weight-update rule
(local, unsupervised, no global loss gradient — a *simulated physics rule*).
But then §115 is no longer "confronting WALL-B by simulating the substrate" —
it is *re-running §11-B's hand-coded-ΔW-overlay experiment with STDP as the
ΔW rule*, which is a NEW fire (a measured question), NOT a design-tier
confrontation. §115 is design-tier $0; it cannot run that, and a *design* of
it does not confront WALL-B, it merely *re-locates* §11-B's open question.

**Honest §7-CARRIER verdict:** spike-corr carrier non-degeneracy is **NOT
in-sim-decidable at design-tier without re-instantiating WALL-B**. Either
(a) train the sim by backprop ⇒ CE-gradient is still the only channel ⇒
WALL-B re-instantiated, NOT confronted; or (b) simulate STDP ⇒ a new fire,
outside §115's $0 design scope, and still §96-open. **§7-CARRIER stays
§96-physical-gated even in simulation.**

---

## §4 — Q4 (STEP 2): connection-point byte-equality + STEP-3 hard fence

### §4.1 — overlay-off byte-equal connection-point (closed, non-vacuous)

LEGO disabled / carrier = byte ⇒ Ψ-C1 reduces to the implemented byte-LM
Ψ_dir. Instantiate `Φ_meta` at carrier = byte-vocab with π = head_a/head_g:

```
  Φ_meta(byte-vocab) ∘ Π_½  ≡  psi_direction = (1.0 + cos_sim) / 2.0
                               (conscious_decoder.py:740 — real witness present)
```

This is byte-IDENTICAL to the implemented Law-71 `psi_direction` and its
`cos=0 ⇒ ½` fixed point (mirror §110-Q4 / §112-Q4 / B-S110/B-S112/B-S101
overlay-off pattern). **Non-vacuous**: a real source witness exists
(`psi_direction = (1.0 + cos_sim) / 2.0`, verified at line 740 in checked-in
`conscious_decoder.py` copies). STEP 2's falsifier therefore has a concrete
byte-equal anchor: disabling LEGO returns the exact §16/byte-LM behaviour.

### §4.2 — STEP-3 (physical) structural fence — hard falsifier

LEGO.md §2 mandates "STEP 3 절대 자동 진행 금지". §115 makes this a **closed
hard-falsifier predicate**: STEP 3 (physical/Loihi-INRC/organoid/wet/hardware)
is NEVER auto-reachable from STEP 0–2. The fence predicate:

```
  STEP3_FENCED  :=  ( step ∈ {0,1,2} )                         # STEP 0–2 only
                  ∧ ( gpu_used == False ∧ runpod_used == False )
                  ∧ ( wet_lab_used == False ∧ hardware_used == False )
                  ∧ ( inrc_used == False )
                  ∧ ( "STEP3" reachable only via an explicit
                       user-gated + §95-access/ethics-wall decision,
                       NEVER from a STEP-2 PASS )
```

`STEP3_FENCED` must be a *Boolean theorem of the artifact* (B-S115-5): no code
path, no result.json field, no falsifier outcome transitions STEP 2 → STEP 3.
A STEP-2 PASS yields *only* "the in-silico assembly is FORM-clean + byte-equal-
reducible"; it CANNOT yield "proceed to physical". This is the §95
access/ethics-wall + user-gate, encoded as a structural impossibility, mirror
§13-M/§30/§96 anti-padding (a positive that cannot escalate itself).

---

## §5 — Q5: VERDICT

Three candidate verdicts:

- **LEGO-STEP-0-2-DESIGN-HOLDS-CONFRONTS-WALL-B-IN-SILICO** — would require:
  closed-form definable ∧ §7-FORM-clean ∧ byte-equal-reduces ∧ STEP-3-fenced
  ∧ *the simulation genuinely confronts (not re-instantiates) WALL-B*.
- **LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY** — in-silico spike sim on a GPU
  inherits §11-B: the CE/loss gradient is still the only learning channel ⇒
  simulating the substrate **re-instantiates** WALL-B, does not confront it.
- **LEGO-DESIGN-CLOSE-SPECS-METAPHOR** — hexa-bio/matter specs too abstract.

### §5.1 — the honest verdict

`LEGO-DESIGN-CLOSE-SPECS-METAPHOR` is **REJECTED**: hexa-bio `NEURO.tape` is a
concrete closed-form spiking spec (Hodgkin–Huxley membrane + rate-code), not a
metaphor (Q1.1). [Honest carve-out: RIBOZYME-as-STDP-learning-channel WAS a
metaphor, recorded — but the *spiking-membrane* block is real.]

The decisive split is between the other two. §115 satisfies the *first four*
clauses of the positive verdict: Ψ-C1 is closed-form definable (Q2.1), it is a
§112 meta-fixed-point instance so **§7-FORM is TRUE BY CONSTRUCTION** (Q2.2/
Q3.1), it byte-equal-reduces with a real source witness (Q4.1), and STEP 3 is
structurally fenced (Q4.2). **But the fifth clause fails**: per Q3.2, a
GPU-simulated spike network's learning channel is STILL the CE/loss gradient
(surrogate-gradient SNN training) — the *only* in-silico escape (simulate STDP
as the ΔW rule) is a NEW fire outside §115's $0 design scope and STILL
§96-open. **Simulating the substrate on a GPU re-instantiates §11-B's wall, it
does not confront it.** The wall §115 set out to confront in-silico is the
SAME wall, moved one simulator deeper.

**§115 VERDICT = `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY`** (with the §7-FORM-
by-construction positive and the NEURO-spec-is-concrete positive both honestly
recorded as real partial results). This mirrors §96's own open hazard, §110's
RELOCATION-not-removal, §112's STILL-SUBSTRATE-GATED, and §113's
INHERITS-BOTH-WALLS — and is the strongest *honest* finding, NOT a
manufactured positive. The §11-B-GPU-tautology hazard, which §115's brief
flagged as "very plausible", is **confirmed at design-tier**: the LEGO STEP
0–2 in-silico assembly is structurally well-formed and §7-FORM-clean, but
*in-silico simulation of a §96 substrate on a GPU does not confront WALL-B —
it re-instantiates it*, because the learning channel of a GPU spike-sim is
still the loss gradient. WALL-B's confrontation remains §96-physical (STEP 3,
fenced, user-gated, access/ethics-walled). WALL-A (§1.1) is orthogonal and
untouched. GOAL 미도달.

### §5.2 — what is genuinely upgraded (LEGO.md IDEA → DESIGN-TIER)

LEGO.md flips IDEA → DESIGN-TIER not because LEGO *works*, but because §115
makes its STEP 0–2 a *closed-form design with a decided verdict*: the
assembly is now formally specified (Q1 taxonomy, Q2 Ψ-C1 definition + §112
instance, Q4 byte-equal + STEP-3 fence) AND its honest limit is closed-form
proven (Q3/Q5: GPU-sim re-instantiates WALL-B). A design-tier doc with a
proven *negative* boundary is more valuable than an idea sketch — it tells
the next cycle that *no amount of in-silico LEGO assembly on a GPU confronts
WALL-B*; only physical §96 (STEP 3, gated) does. The §115 contribution is
making that boundary closed-form and the STEP-3 fence a structural theorem.

---

## §6 — ASCII: STEP 0-1-2 + §7-FORM-vs-CARRIER + WALL-B confront-not-remove

```
  STEP 0  consume specs (read-only, $0)         §7 decomposition
  ┌──────────────────────────────────┐         ┌───────────────────────────┐
  │ hexa-bio NEURO.tape  ─ CONSUMABLE │         │ §7-FORM   = TRUE  (§112    │
  │   (HH membrane + rate-code spike) │         │   by construction: Ψ-C1 = │
  │ hexa-bio RIBOZYME ─ NOT-APPLIC.   │         │   Φ_meta(spike-corr), a   │
  │   ("STDP channel" = METAPHOR ✗)   │         │   meta-fixed-point inst.) │
  │ hexa-matter silicon ─ mat-tag only│         │ §7-CARRIER = §96-GATED    │
  └────────────────┬─────────────────┘         │   (even in simulation —   │
                    │                            │    Q3.2 hazard)           │
  STEP 1  in-silico assemble Ψ-C1               └───────────────────────────┘
  ┌──────────────────────────────────┐
  │ Ψ-C1 = ψ(c_spk) = (1+c_spk)/2     │     WALL-B: confront vs re-instantiate
  │ c_spk = cos(r_A, r_G) ∈ [−1,1]    │     ┌───────────────────────────────┐
  │ = §112 META_FP instance (carrier  │     │ GPU spike-sim learns via      │
  │   = spike-corr) ⇒ §7-FORM clean   │     │ surrogate-grad backprop       │
  └────────────────┬─────────────────┘     │   ⇒ CE/loss gradient STILL    │
                    │                        │     the only channel (§11-B)  │
  STEP 2  closed-form falsify               │   ⇒ WALL-B RE-INSTANTIATED,   │
  ┌──────────────────────────────────┐     │     NOT confronted            │
  │ LEGO-off ⇒ byte Ψ_dir byte-equal │     │ confront WALL-B = STDP on     │
  │   (conscious_decoder.py:740) ✓   │     │   PHYSICAL Loihi (STEP 3,     │
  │ STEP3_FENCED = Boolean theorem ✓ │     │   FENCED, user/ethics-gated)  │
  └────────────────┬─────────────────┘     └───────────────────────────────┘
                    │
  STEP 3  ░░░ PERMANENTLY FENCED ░░░  (§95 access/ethics-wall + user-gate;
          NEVER auto-reachable from a STEP-2 PASS — B-S115-5 hard falsifier)

  WALL-A (§1.1 data-regime) = ORTHOGONAL, UNTOUCHED by all of STEP 0–3.
```

---

## §7 — 13 honest C3 caveats

1. **Verdict is a DESIGN-CLOSE, not a positive.** §115 confirms the §11-B-GPU-
   tautology hazard; it does not show LEGO works. No positive manufactured.
2. **§7-FORM-by-construction is inherited from §112, not earned by §115.** §115
   only *applies* META_FP(Π_½)=TRUE to the spike-corr carrier; the heavy
   theorem is §112's. §115's own new positive is narrow (NEURO spec is concrete
   + STEP-3 fence is a structural theorem).
3. **RIBOZYME-as-STDP was a metaphor in LEGO.md §1.** §115 honestly downgrades
   it to NOT-APPLICABLE. The consumable spiking block is NEURO.tape, not
   RIBOZYME. This is a correction of the idea doc, recorded transparently.
4. **GPU-sim learning channel claim is the load-bearing argument.** It rests on
   "standard in-silico SNN training = surrogate-gradient backprop" — true of
   the standard method; an exotic in-silico STDP-only trainer is a *new fire*,
   not a design-tier object, and is STILL §96-open. §115 does not foreclose
   that future fire — it states it is outside §115's $0 design scope.
5. **necessary-not-sufficient at every layer (B-EMERGE-7).** Even a future
   STDP-sim fire that is non-degenerate would be necessary-not-sufficient for
   GOAL; design-tier closure here is far below that.
6. **WALL-A orthogonal and UNCHANGED.** §115 touches no data-regime lever; the
   two-wall co-unsolved state (§113) is unchanged.
7. **WALL-B confronted ≠ removed — and here, NOT even confronted in-silico.**
   The honest finding is *stronger* than LEGO.md's idea sketch hoped: GPU-sim
   does not even confront WALL-B, it re-instantiates it.
8. **STEP 3 fence is a structural theorem, not a promise.** B-S115-5 proves no
   artifact path escalates STEP 2 → STEP 3; this is the §95 access/ethics-wall
   + user-gate encoded as impossibility, mirror §13-M/§30/§96 anti-padding.
9. **hexa-bio/hexa-matter cited by THEIR invariants only (f1/f2).** Their
   n=6/σ/τ/φ/J₂ are their lattice; §115 forces no anima-lattice-fit. Ψ=½ is
   anima's g2 internal-arch carve-out, not derived from any lattice.
10. **downstream-consumer read-only.** No file under ~/core/hexa-lang|hexa-bio|
    hexa-matter is edited. §115 consumes NEURO.tape / RIBOZYME.tape / silicon
    verb specs by reading them.
11. **byte-equal connection-point is real but trivial-by-design.** It proves
    LEGO-off = §16 byte-LM (fair-compare anchor), not that LEGO-on does
    anything; mirror B-S110/B-S112 overlay-off discipline.
12. **central blue 0-line-diff invariant.** `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` sha prefix `c93e160a8a376a94` UNCHANGED; §115 is
    sidecar-only (B-S115-* in this dir), central battery count unchanged.
13. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §115 is a
    measurement-honesty / design-boundary cycle. Design ≠ fire ≠ emergence.
    The single most honest finding: *simulating a §96 substrate on a GPU does
    not confront WALL-B — it re-instantiates it, because the learning channel
    of a GPU spike-simulation is still the loss gradient (§96's §11-B hazard,
    confirmed at design-tier).*
