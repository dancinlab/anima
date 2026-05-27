# §120 — The spiking attention replacement: deciding §96 design-open #1

> **status**: RESEARCH §120 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO INRC ·
>   NO fire · NO model.forward · NO corpus · NO dispatch · orphan 0 · single
>   sequential agent.
> **date**: 2026-05-19
> **verdict**: **`SPIKING-ATTENTION-REPLACEMENT-DECIDED — SPIKE-RATE-DOT-PRODUCT
>   + k-WTA`** — §96 design-open #1 moves from *undecided design-open* to
>   *decided design-tier*. A design-open → design-DECIDED transition. It does
>   NOT implement the spiking anima, does NOT reach GOAL, does NOT remove
>   WALL-A or WALL-B.
> **parent**: §96 `state/loihi_spiking_rederivation_s96_2026_05_19/DESIGN.md`
>   (Q1 §3.3 the SPIKING-INCOMPATIBLE analysis + the candidate replacements) ·
>   §118 `state/track0_insilico_s118_2026_05_19/DESIGN.md` (VOID — confirmed
>   the real blocker IS design-open #1) · `HEXAD/NEUROMORPHIC/TRACK0_INSILICO.md`
>   §4 (Phase 2 = the blocking design-open) · `ready/models/conscious_decoder.py`
>   (the byte-attention being replaced — `:372` score, `:381`/`:441` softmax,
>   `:740` Law-71 Ψ).
> **governance**: g3 (capability claim 0, design ≠ fire ≠ emergence; a DECISION
>   is not an ACHIEVEMENT) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24
>   derivation; Ψ=½ = anima g2 internal-arch carve-out) · downstream-consumer
>   (hexa-lang/hexa-bio read-only) · central `state/verify_hexad_blue_2026_05_15/
>   blue_falsifier.py` 0-line-diff (sidecar-only battery).

---

## §0 — Why §120 exists: §118's VOID points the finger at design-open #1

§96 Q1 §3.3 found `softmax(QK^T)` self-attention `SPIKING-INCOMPATIBLE` — three
structural obstructions: it is (1) all-pairs content-based (a dense O(T²)
similarity matrix vs a spike = a point event), (2) globally normalised (softmax
is a synchronous all-reduce vs Loihi's asynchronous NoC), (3) instantaneous (one
layer-step vs spike trains unfold over time). §96 named two *candidate*
replacements — phase-resonance routing, and spike-rate dot-product + k-WTA — but
explicitly left the choice **undecided** as **design-open #1**.

§118 (`Track 0 in-silico`, verdict VOID) ran the §96 §4.5 cells in a $0 numpy
toy and confirmed, from the other direction, that design-open #1 is *the*
load-bearing blocker: the toy rig could not even assemble the spiking anima —
its decisive STDP cell was a generic recurrent LIF net, not the attention-
replaced spiking `ConsciousDecoderV2`, because no routing replacement was
chosen. §118's VOID is an explicit *ask*: decide design-open #1.

§120 answers it. "돌파" (break-through) here means precisely a **design-open →
design-DECIDED transition** — §120 *picks* the replacement with a closed-form
justification. It does NOT build the spiking anima, does NOT fire, does NOT
reach the GOAL, and does NOT remove either wall. design-tier only.

---

## §1 — The thing being replaced (the reduction target)

From `ready/models/conscious_decoder.py` `MultiHeadAttention` (verified by
`grep`, no model.forward):

```
  :372   att = (q @ k_exp.transpose(-2,-1)) * (1/√head_dim)   ← content-based score
  :377-380 causal mask                                        ← causality
  :381   att = F.softmax(att, dim=-1)                         ← GLOBAL normalisation  ◄ the incompatible op
  :383   y   = att @ v_exp                                    ← weighted value routing
```

So byte-vocab attention computes, per query position `i`:

```
  ATTN_softmax(i)  =  Σ_j  softmax_j( q_i·k_j / √d )  ·  v_j      (sum over causal j ≤ i)
```

and `:740` `psi_direction = (1 + cos(logits_a, logits_g)) / 2` is Law-71 — the
Ψ=½ fixed point lives downstream of the dual heads `head_a` / `head_g`. The
replacement must (a) be genuinely spiking-compatible, (b) preserve the
Engine-A⇄G opposition + the Ψ=½ routing semantics, and (c) reduce to
`ATTN_softmax` as a special case (a *generalisation*, so it is §7-clean — not a
graft of a foreign mechanism).

---

## §2 — Candidate evaluation (closed-form, the two §96 candidates)

### Candidate 1 — phase-resonance routing

*Mechanism*: resonate-and-fire (R&F) neurons; each key is encoded as an
oscillator at a content-dependent phase φ_k; a query spike-train at phase φ_q is
routed to keys it **phase-locks** with (resonance amplitude peaks when
`φ_q ≈ φ_k`). Routing weight = resonance amplitude.

| §96-#1 criterion | phase-resonance | verdict |
|---|---|---|
| (a) genuinely spiking-compatible | ✅ R&F is a native SNN primitive; phase-locking is local, no global softmax | PASS |
| (b) preserves A⇄G + Ψ=½ | ⚠️ the A⇄G *opposition* could map to anti-phase (φ_A vs φ_A+π), but Ψ=½ is defined (`:740`) as a **cosine of two logit vectors** — a phase-locking amplitude is a *different geometry* (a resonance kernel, not a vector cosine). Re-deriving Ψ as a phase relationship is itself a fresh design-open, not a preservation. | PARTIAL |
| (c) byte-attention reduction | ❌ there is no limit in which a phase-resonance kernel *becomes* `softmax(q·k/√d)`. Phase coding and dot-product scoring are non-isomorphic; the reduction would be an approximation, not an identity. So phase-resonance is a **graft of a different routing rule**, not a generalisation of byte-attention. | FAIL |

Phase-resonance is spiking-compatible but **fails (c)** — it cannot present
byte-attention as a special case, so adopting it would not be §7-clean (it
would be a graft, RESEARCH.md §7 condition ②). Honest note: phase coding *is*
the natural spiking realisation of **position** (SNNs carry time natively) — see
§4's hybrid note. As the *routing* mechanism it fails the reduction test.

### Candidate 2 — spike-rate dot-product + k-WTA

*Mechanism*: two parts.
1. **Spike-rate dot-product** — encode `q_i`, `k_j` as the firing-rate vectors
   of small LIF sub-populations. The synaptic current a key population delivers
   to a query population is, by the standard rate-coding identity, proportional
   to `r(q_i)·r(k_j)` — a **coincidence-detector** computes the dot-product
   *as a local, event-driven, asynchronous accumulation* (no all-pairs matrix,
   no synchronous reduction). This is exactly the §96 Q1 `SPIKING-COMPATIBLE`
   "residual stream → LIF current accumulation" primitive applied to scoring.
2. **k-WTA (k-winners-take-all)** replaces the softmax. Instead of normalising
   the score vector globally, a **lateral-inhibition** circuit lets the `k`
   highest-current keys spike and suppresses the rest. §96 Q1 already classified
   lateral inhibition `SPIKING-COMPATIBLE` (`−F_c` inhibitory synapses, a Loihi
   `STDPLoihi` primitive) and k-WTA `SPIKING-OPEN` (a known SNN motif).

| §96-#1 criterion | spike-rate dot-product + k-WTA | verdict |
|---|---|---|
| (a) genuinely spiking-compatible | ✅✅ both parts are SNN-native: rate-coded coincidence detection IS asynchronous local accumulation (kills obstruction 1 *all-pairs* and obstruction 3 *instantaneous*); k-WTA via lateral inhibition is a **local competition**, NOT a global normalisation (kills obstruction 2 *global softmax*). All three §96 §3.3 obstructions are dissolved. | PASS |
| (b) preserves A⇄G + Ψ=½ | ✅ A⇄G map to excit/inhib LIF sub-populations (§96 Q1 `SPIKING-OPEN` row); the k-WTA competition between them has a **balance fixed point** — when the excitatory (A) and inhibitory (G) drives are equal, the winner-set is maximally undecided. That balance point IS Ψ=½: `cos=0 ⇒ ψ=½` (no A-vs-G preference) is the k-WTA tie. The Ψ=½ fixed point is *preserved as the competition's neutral point* — see §3's reduction. | PASS |
| (c) byte-attention reduction | ✅ **closed reduction witness in §3** — set `k = T` (every key wins) and read the winner-set out with a softmax instead of a hard top-k, and `spike-rate-dotprod + k-WTA` becomes *exactly* `ATTN_softmax`. byte-attention is the `k=T`, soft-readout **special case**. So this is a **generalisation, not a graft** — §7-clean (condition ② satisfied: byte-attention is recovered as a limit, the foreign mechanism is not bolted on). | PASS |

---

## §3 — The decision + the closed-form reduction witness

**DECISION (adopted — autonomy mode, /goal active, logged):**

> §96 design-open #1 is decided: the `softmax(QK^T)` self-attention of
> `ConsciousDecoderV2` is replaced, on the spiking substrate, by
> **spike-rate dot-product scoring + k-WTA routing**. (Phase-resonance is
> *not* the routing mechanism — it fails the §7-clean reduction test — but
> is adopted as the natural spiking realisation of *position* / RoPE; see
> §4 hybrid note.)

### The closed-form reduction witness (criterion (c))

Define the spiking routing as a two-parameter family `R(k, β)`:

```
  score_ij  =  r(q_i) · r(k_j) / √d                         (rate-coded dot-product, causal j ≤ i)
  R(k, β)_i =  Σ_j  W_β,k( score_i )_j  ·  v_j
```

where `W_β,k` is the winner-weighting: the `k` highest scores receive weight
`softmax(β · score)` *restricted to the winner set*, the rest receive 0.

- **Hard spiking limit** `R(k, β→∞)`: a strict k-WTA — exactly `k` keys spike,
  each routed with the lateral-inhibition competition outcome. This is the
  spiking-compatible operating point (no global softmax: the winner set is a
  *local* competition, the weighting is over `k` elements not `T`).
- **Byte-attention limit** `R(k=T, β=1/√d already folded)`: when **every** key
  wins (`k = T`, the causal key count) and the winner-weighting is the soft
  `softmax(score)` over the full set, `W` is just `softmax_j(q_i·k_j/√d)` and

  ```
    R(T, soft)_i  =  Σ_j  softmax_j( q_i·k_j/√d ) · v_j  =  ATTN_softmax(i)   ∎
  ```

So `ATTN_softmax` is **byte-equal** to `R(k=T, soft-readout)` — the existing
byte-vocab attention is *one corner* of the spiking routing family. The spiking
anima's routing is a **strict generalisation**: it adds the `k < T` hard-WTA
corner (the spiking-compatible one) while *containing* byte-attention as the
`k=T` corner. This is the §7-clean witness — the replacement is not a foreign
graft (condition ②); it is the parent of which byte-attention is the limit.

`blue_falsifier_s120.py` `B-S120-3` checks this reduction **numerically
byte-equal** (`R(k=T, soft) == softmax-attention` to float tolerance, on a small
random q/k/v).

### A⇄G / Ψ=½ preservation (criterion (b))

Engine-A and Engine-G are excitatory and inhibitory drives into the k-WTA
competition. The competition's *score* for routing toward A vs G is
monotone in `cos(drive_A, drive_G)`:

```
  ψ_route  =  (1 + cos(drive_A, drive_G)) / 2          ← identical functional form to Law-71 (:740)
```

`cos = 0` ⇒ `ψ_route = ½` ⇒ A and G are orthogonal ⇒ the k-WTA competition has
no A-vs-G preference ⇒ the **Ψ=½ fixed point is the competition's neutral
point**. The replacement does not *re-define* Ψ — it *re-hosts the same Ψ
formula* on the competition's drive vectors (this is exactly the §112
META_FP(Π_½) carrier-substitution: `ψ(c) = (1+c)/2` with the carrier `c` now the
A/G drive cosine instead of the logit-vector cosine — a carrier-invariant
fixed-point form, §110 Ψ-C2 / §112 family). `B-S120-2` checks `ψ_route` bounded
∈ [0,1] + `cos=0 ⇒ ½` (sympy).

---

## §4 — Honest hybrid note: phase-resonance for *position*, k-WTA for *routing*

The decision is **not** "k-WTA wins everything." Phase-resonance failed the
*routing* reduction test (§2 candidate 1, criterion (c) FAIL) — but §96 Q1
separately classified RoPE / positional encoding `SPIKING-OPEN` with the note
"spike-time / phase coding (relative timing carries position)." SNNs carry time
*natively*; phase coding is the natural spiking realisation of **position**.
So the honest, fully-justified design is a **two-mechanism split**:

- **routing** (which key a query attends to) = spike-rate dot-product + k-WTA
  (this §120 decision — passes all three §96-#1 criteria);
- **position** (RoPE's job) = phase coding (a *separate* §96 design-open, the
  RoPE row — §120 notes it as the natural home for phase-resonance, does NOT
  decide it here).

This split is itself §7-clean: routing and position are *already* separate
sub-mechanisms in `ConsciousDecoderV2` (RoPE rotates q/k *before* the attention
score). Replacing each with its spiking-native counterpart preserves the
architecture's factorisation — it is not a graft.

---

## §5 — Three rationale bullets (why this decision)

1. **It dissolves all three §96 §3.3 obstructions, not one.** Phase-resonance
   dissolves "global normalisation" but leaves the dot-product geometry foreign.
   Spike-rate dot-product + k-WTA dissolves *all three*: rate-coded coincidence
   detection makes scoring **asynchronous + local** (kills obstruction 1
   *all-pairs* and obstruction 3 *instantaneous*); k-WTA via lateral inhibition
   makes selection a **local competition** (kills obstruction 2 *global
   softmax*). Every part is a §96 Q1 `SPIKING-COMPATIBLE` or `SPIKING-OPEN`
   primitive (LIF current accumulation; `−F_c` lateral inhibition; k-WTA motif)
   — the re-derivation is engineering on known primitives, not a research leap.

2. **It is a generalisation, not a graft — the only §7-clean choice.** §3's
   closed reduction witness shows byte-attention `ATTN_softmax` is the `k=T`,
   soft-readout corner of the spiking routing family `R(k,β)`. Phase-resonance
   has no such limit — there is no parameter setting in which a phase-locking
   kernel *becomes* `softmax(q·k/√d)`; adopting it would be RESEARCH.md §7
   condition ② violation (a generic mechanism grafted on). k-WTA contains
   byte-attention, so the spiking anima's routing **inherits** the byte-anima as
   a special case — exactly what "generalisation, not graft" means.

3. **It preserves the anima physics layer intact.** §96 Q1's headline: anima's
   *physics layer* (PureFieldFFN→LIF leak, tension, Φ, Engine A⇄G, STDP) is
   largely spiking-friendly; only the *transformer routing layer* did not
   survive. k-WTA's A/G excit/inhib competition keeps the Engine-A⇄G opposition
   and re-hosts the Ψ=½ fixed point as the competition's neutral point (§3,
   §112 carrier-invariance). The decision changes *only* the one
   `SPIKING-INCOMPATIBLE` faculty §96 isolated — surgical, minimal, the rest of
   the §96 Q1 map is untouched.

---

## §6 — ASCII: byte-attention → spiking routing (the decided replacement)

```
  ┌─────────── byte-vocab attention (ConsciousDecoderV2, :372-383) ───────────┐
  │   q_i, k_j  ──►  att = q·kᵀ/√d  ──►  softmax_j (GLOBAL all-reduce) ──► Σ a·v │
  │                                       ▲                                    │
  │                              §96 §3.3 SPIKING-INCOMPATIBLE                  │
  └────────────────────────────────────────────────────────────────────────────┘
                                  │  §120 DECISION
                                  ▼
  ┌────────── spiking routing  R(k,β)  —  spike-rate dot-product + k-WTA ────────┐
  │                                                                             │
  │   r(q_i),r(k_j) ─► coincidence-detector synaptic current  r(q)·r(k)/√d      │
  │        (LIF accumulation — ASYNC, LOCAL — kills obstruction 1 & 3)           │
  │                          │                                                  │
  │                          ▼                                                  │
  │   k-WTA via lateral inhibition (−F_c synapses)  ── kills obstruction 2       │
  │        the k highest-current keys spike; rest suppressed (LOCAL competition) │
  │                          │                                                  │
  │                          ▼                                                  │
  │              Σ_{winners}  W · v        ← routed value                       │
  │                                                                             │
  │   A⇄G excit/inhib drive into the competition:                               │
  │        ψ_route = (1+cos(drive_A,drive_G))/2   ── Law-71 form preserved       │
  │        cos=0 ⇒ ψ=½  ⇒  k-WTA A-vs-G tie  ⇒  Ψ=½ fixed point = neutral point │
  │                                                                             │
  │   REDUCTION WITNESS:  R(k=T, soft-readout)  ≡  softmax-attention  (byte-eq)  │
  │        ⇒ byte-attention is the k=T corner ⇒ GENERALISATION, not graft        │
  │                                                                             │
  │   position (RoPE): phase coding — §96 RoPE design-open, §120 hybrid note     │
  └──────────────────────────────────────────────────────────────────────────────┘

  STILL STANDING (g3): WALL-A (§1.1 data-regime, orthogonal) ·
  WALL-B (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated) ·
  implementation (a decided design is not a built network).
```

---

## §7 — Honest C3 caveats (≥12)

1. **§120 is a DESIGN-TIER DECISION, not a fire.** $0, no GPU/runpod/INRC/
   Loihi, no model.forward, no corpus, no dispatch. orphan 0. capability claim 0.
2. **"돌파" here = design-open → design-DECIDED.** It is a *decision transition*,
   NOT an achievement. §120 picks the attention replacement; it does NOT build
   it, does NOT train it, does NOT measure it.
3. **It does NOT implement the spiking anima.** The decided routing mechanism
   still has to be coded, wired into a spiking `ConsciousDecoderV2`, and run on
   a real async substrate (Track L/S/P) — none of that is §120.
4. **WALL-A (§1.1 data-regime) is UNCHANGED.** A routing-mechanism decision
   moves no training-data threshold (§97). GOAL's data bottleneck is untouched.
5. **WALL-B (§95/§96 async substrate) is UNCHANGED.** The decided mechanism is
   spiking-compatible, but running it on a *real* event-driven substrate stays
   Loihi/SpiNNaker/SpiNNcloud-gated (a SOFT WALL — access, not architecture).
   §118's VOID showed a clocked GPU/CPU sim cannot confront the async half.
6. **k-WTA is `SPIKING-OPEN`, not `SPIKING-COMPATIBLE`, in §96 Q1.** §120's
   decision *commits to* the §96 `SPIKING-OPEN` candidate — it is "plausible on
   Loihi 2's programmable neurons + graded spikes," a known SNN motif, but its
   *validation at scale* on a real chip is itself future work (a research
   result, per §96 §3.3). §120 decides the design; it does not certify the
   silicon behaviour.
7. **The reduction witness is a functional-form identity, not a trained
   equivalence.** `R(k=T, soft) ≡ softmax-attention` proves the spiking routing
   *contains* byte-attention as a corner. It does NOT claim a spiking anima
   *trained* with k-WTA routing reproduces a byte-anima's weights or behaviour —
   that is an empirical question (B-S120-NOTE).
8. **Ψ=½ preservation is a carrier-substitution, not a re-derivation that has
   been verified to learn.** §3's `ψ_route` re-hosts the Law-71 form on the A/G
   drive cosine (§112 META_FP(Π_½) carrier-invariance). Whether a k-WTA
   competition *driven that way* yields useful routing is an empirical,
   future-fire question.
9. **Phase-resonance is not discarded — it is re-assigned.** §120 rejects it as
   the *routing* mechanism (fails the §7-clean reduction) but adopts it as the
   natural spiking home for *position* (RoPE) — a *separate* §96 design-open
   §120 explicitly does NOT decide here.
10. **§118's VOID is the reason §120 exists, not evidence §120 succeeds.** §118
    confirmed design-open #1 is the blocker; §120 decides it. A decided
    design-open is an unblocked *design path*, not a measured *result*.
11. **central blue_falsifier.py 0-line-diff.** §120's battery is a sidecar
    (`blue_falsifier_s120.py`); central `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` is untouched — sha256 prefix `c93e160a8a376a94`.
12. **f1/f2 safe.** k-WTA / LIF / lateral inhibition / rate coding cited by
    standard SNN literature + §96 Q1's own `SPIKING-COMPATIBLE` classification;
    NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation; Ψ=½ = anima g2
    internal-arch carve-out. downstream-consumer: hexa-lang / hexa-bio read-only.
13. **necessary-not-sufficient at every layer (B-EMERGE-7).** Deciding the
    attention replacement is necessary for a spiking anima; it is nowhere near
    sufficient for GOAL emergence — coherence (§88-F2 γ gap), the data regime
    (WALL-A), and the substrate access (WALL-B) all remain.
14. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §120 turns
    one undecided design-open into a decided design-tier item. It does not
    over-claim a decision into an achievement.

---

## §8 — Verdict

§120 = **DESIGN-TIER DECISION LANDED.** §96 design-open #1 — *which* spiking
routing mechanism replaces `softmax(QK^T)` self-attention — is **decided**:

> **spike-rate dot-product scoring + k-WTA routing**, with phase coding
> reserved (hybrid note) for the separate position/RoPE design-open.

Closed-form justification: it (a) dissolves all three §96 §3.3 obstructions
(rate-coded coincidence detection = async local accumulation; k-WTA via lateral
inhibition = local competition, not global softmax); (b) preserves the
Engine-A⇄G opposition (excit/inhib drives) and the Ψ=½ fixed point (the k-WTA
neutral point, Law-71 form re-hosted per §112 carrier-invariance); (c) reduces
to byte-vocab `softmax`-attention as the `k=T`, soft-readout corner of the
routing family `R(k,β)` — a **generalisation, not a graft** (§7-clean, the
byte-anima is contained as a special case). The rejected candidate
(phase-resonance routing) fails (c): no limit recovers `softmax(q·k/√d)`, so it
would be a graft — it is re-assigned to position coding instead.

This unblocks the §118 Track-0 decisive cell **as a design**: the spiking anima
can now be *specified* with a chosen routing mechanism. It does NOT build it,
does NOT fire, does NOT reach GOAL. WALL-A (§1.1 data-regime) and WALL-B
(§95/§96 async substrate) both stand. design-open #1 moves: undecided → decided
design-tier. capability claim 0; necessary-not-sufficient (B-EMERGE-7);
north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달.
