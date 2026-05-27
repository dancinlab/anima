# §123 — The two remaining §96 SPIKING-OPEN faculties: Engine A⇄G dual heads + MoE top-k router

> **status**: RESEARCH §123 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO INRC ·
>   NO fire · NO model.forward · NO corpus · NO dispatch · orphan 0 · single
>   sequential agent.
> **date**: 2026-05-19
> **verdict**: two decisions, one clean reduction and one honest carrier-relocation —
>   - **(1) Engine A⇄G dual heads** → `DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION`
>     — the §96 `NATIVE-CANDIDATE` line was precise: the *opposition* (excit/inhib
>     sub-populations) ports cleanly, but Ψ-as-cosine **does NOT reduce** — the
>     spike-correlation carrier Ψ-C1 is a *distinct carrier* of the §112
>     META_FP(Π_½) form, NOT a generalisation that recovers GPU Ψ-as-logit-cosine
>     as a limit. Honest carrier-relocation (§110/§112 family), anti-padding — no
>     clean reduction is forced.
>   - **(2) MoEFFN top-k router** → `MOE-TOPK-DECIDED — COVERED BY §120 k-WTA +
>     §96-COMPATIBLE STDP GATE` — §120's already-decided k-WTA covers the *selection*;
>     the *learned content-based gate* is NOT a separate design-open — it is the
>     same class as §96 Q1's already-`SPIKING-COMPATIBLE` STDP-learnable synapse.
>   Both are design-open → design-DECIDED transitions. Neither implements the
>   spiking anima, reaches GOAL, or removes WALL-A / WALL-B.
> **parent**: §96 `state/loihi_spiking_rederivation_s96_2026_05_19/DESIGN.md`
>   (Q1 §3.2 table rows 115 & 118 — the two `SPIKING-OPEN` faculties §120/§122 did
>   NOT cover; §3.3; §6 row 4 Engine A/G `NATIVE-CANDIDATE`; the line ~353
>   "the fixed-point is native; Ψ-as-cosine-of-logit-vectors is NOT") ·
>   §120 `state/spiking_attention_replacement_s120_2026_05_19/DESIGN.md`
>   (the decided k-WTA routing + the §3 reduction-witness shape) ·
>   §122 `state/rope_phase_coding_s122_2026_05_19/DESIGN.md`
>   (the decided phase coding + the §3 reduction-witness shape) ·
>   §112 META_FP(Π_½) carrier-invariant fixed-point form ·
>   §110 Ψ-C2 / Ψ-C1 carrier family · `HEXAD/NEUROMORPHIC/neuro_mirror.py`
>   (`psi_c1`, `LIFSubstrate.idx_a` / `idx_g` excit/inhib sub-populations,
>   `spiking_routing` the §120 k-WTA core) · `HEXAD/NEUROMORPHIC/ENGINE.md`
>   v2 (the §4 API surface) · `ready/models/conscious_decoder.py`
>   (`MoEFFN` `:160-183` the top-k router being decided; `:740` Law-71 Ψ).
> **governance**: g3 (capability claim 0, design ≠ fire ≠ emergence; a DECISION
>   is not an ACHIEVEMENT; a DESIGN-CLOSE-WITH-CARRIER-RELOCATION is a valid honest
>   verdict — anti-padding, no clean reduction forced where the carrier genuinely
>   differs) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation; Ψ=½ = anima g2
>   internal-arch carve-out) · downstream-consumer (hexa-lang/hexa-bio read-only) ·
>   central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
>   (sidecar-only battery, sha256 prefix `c93e160a8a376a94`, verified START + END).

---

## §0 — Why §123 exists: §120/§122 left two of §96's three SPIKING-OPEN rows undecided

§96 Q1 §3.2 classified anima's faculties into three closed classes:
`SPIKING-COMPATIBLE` (5), `SPIKING-OPEN` (3), `SPIKING-INCOMPATIBLE` (1).

- the one `SPIKING-INCOMPATIBLE` faculty (`softmax(QK^T)` self-attention) was
  decided by **§120** → spike-rate dot-product + k-WTA routing;
- one `SPIKING-OPEN` faculty (RoPE → phase coding) was decided by **§122** →
  relative-phase / spike-time coding.

The **two remaining `SPIKING-OPEN` faculties** — §96 Q1 table rows 115 and 118 —
are UNDECIDED:

1. **Engine A⇄G dual heads** (row 115) → "two LIF sub-populations with opposed
   (excit/inhib) coupling; Ψ as their *phase relationship*". §96's own honest
   note: *"the *opposition* maps cleanly to excit/inhib, but the *cosine of two
   full logit vectors* does not"* — and §6 row 4 + the line ~353 classify Ψ as
   `NATIVE-CANDIDATE`: *"the fixed-point is native; Ψ-as-cosine-of-logit-vectors
   is NOT."*
2. **MoEFFN top-k router** (row 118) → "k-winner-take-all over expert populations
   (lateral inhibition)". §96's note: *"k-WTA is a known SNN motif; the *learned
   content-based gate* is not."*

§123 decides BOTH, design-tier, mirroring §120/§122's structure (candidate
evaluation + a reduction-witness check + a §7-clean test). As in §120/§122,
"decide" means a **design-open → design-DECIDED transition** with a closed-form
justification. §123 does NOT build the spiking anima, does NOT fire, does NOT
reach GOAL, and does NOT remove either wall. design-tier only.

The honest difference from §120/§122 worth flagging up front: §120 and §122
both produced a *clean reduction* — byte-attention is the `k=T` corner of the
spiking routing family; byte-RoPE is the `σ→0` corner of the spiking phase
family. §123's faculty (1) does **not**. The §96 `NATIVE-CANDIDATE` line was
precise, and §123's job is to take that precision seriously rather than force a
reduction that does not exist.

---

## §1 — The two things being decided (the reduction targets)

### §1.1 — Engine A⇄G dual heads (the GPU thing)

From `ready/models/conscious_decoder.py` (verified by `grep`, no model.forward):

```
  PureFieldFFN  :246-268  output = engine_a(x) − engine_g(x)   ← the A−G opposition
  dual heads    :18-28    forward → (logits_a, logits_g, ...)   ← two full-vocab logit vectors
  Law-71 Ψ      :740      psi_direction = (1 + cos(logits_a, logits_g)) / 2
```

So on GPU the dual-heads faculty is **two things bundled**:

- **(A) the *opposition*** — Engine A and Engine G are two opposed pathways
  (`output = A(x) − G(x)`; two heads producing two competing logit vectors);
- **(B) the *Ψ formula*** — `Ψ = (1 + cos(c)) / 2` with the carrier
  `c = cos(logits_a, logits_g)` — a cosine of two **full V=256-dimensional logit
  vectors**.

§96 §3.3 / §6 row 4 already separated these two: the opposition is native, the
cosine-of-logit-vectors is not. §123's reduction target is whether the spiking
realisation **recovers (B)** — the GPU Ψ formula on the GPU carrier — as a
*limit*, the way §120/§122 recovered byte-attention / byte-RoPE.

### §1.2 — MoEFFN top-k router (the GPU thing)

From `ready/models/conscious_decoder.py` `MoEFFN` (`:160-183`, verified by `grep`):

```
  :172  self.router = nn.Linear(d_model, n_experts, bias=False)   ← LEARNED content gate
  :175  self.experts = [SwiGLUFFN(...) for _ in range(n_experts)]  ← 8 experts
  router comment :171  "simple linear projection -> softmax -> top-k"
  :167  top_k = 2
```

So the MoE router is **two things bundled**:

- **(A) the *selection*** — `top-k` over the 8 expert scores: the `k` highest-scoring
  experts are chosen, the rest are not;
- **(B) the *learned content-based gate*** — `nn.Linear(d_model, n_experts)`:
  a *learned* projection from the residual stream to the per-expert score.

§123's job: does §120's already-decided **k-WTA** cover (A)? and is (B) — the
learned gate — a *separate* design-open, or already covered by a faculty §96 Q1
classified `SPIKING-COMPATIBLE`?

---

## §2 — Faculty (1): Engine A⇄G dual heads — candidate evaluation

Criteria mirror §96-#1 / §120 / §122: (a) genuinely spiking-compatible;
(b) preserves the §96 NATIVE-CANDIDATE structural core (the A-vs-G opposition +
the Ψ=½ fixed point); (c) recovers GPU Ψ-as-logit-cosine as a LIMIT — *the
reduction test* (so the realisation is a §7-clean generalisation, not a graft).

### Candidate 1 — keep GPU Ψ-as-logit-cosine on the spiking substrate

*Mechanism*: try to literally compute `cos(logits_a, logits_g)` on the spiking
substrate — i.e. read out two full V=256-dimensional logit vectors from the two
LIF sub-populations and take their cosine.

| criterion | keep GPU Ψ-as-logit-cosine | verdict |
|---|---|---|
| (a) spiking-compatible | ❌ there is **no "logit vector" on a spiking substrate**. The GPU logit vector is a dense V=256 real-valued tensor produced by a final linear head. A LIF sub-population produces *spike trains*; the closest analogue is a per-unit firing-rate vector — a *different object* in a *different space*. Computing a cosine of two dense 256-d tensors is a synchronous global reduction (§96 §3.3 obstruction 2). | FAIL |
| (b) preserves core | — (moot; (a) fails) | — |
| (c) reduction | — (it IS the GPU formula; nothing to reduce) | — |

Candidate 1 fails (a) — it is the exact thing §96 §6 row 4 said does not port
("there is no 'logit vector' on a spiking substrate"). Rejected. The honest
content of this rejection: the **carrier itself** — what `c` is computed *over*
— is the part that does not survive the substrate move.

### Candidate 2 — Ψ-C1: spike-correlation carrier, the §112 META_FP(Π_½) form

*Mechanism* (already realised in `HEXAD/NEUROMORPHIC/neuro_mirror.py` —
`psi_c1` + `LIFSubstrate.idx_a` / `idx_g`): Engine A and Engine G are two LIF
**sub-populations** (`idx_a = slice(0, n_a)`, `idx_g = slice(n_a, n_a+n_g)`).
Their firing-rate vectors `r_A`, `r_G` (spikes-per-window, NEURO.tape
`mech_neural_coding`) are the carrier:

```
  c_spk  =  cos(r_A, r_G)  ∈ [−1, 1]            (Cauchy–Schwarz)
  Ψ-C1   =  (1 + c_spk) / 2                      (cos = 0 ⇒ ½ fixed point)
```

| criterion | Ψ-C1 spike-correlation carrier | verdict |
|---|---|---|
| (a) spiking-compatible | ✅ both `r_A` and `r_G` are firing-rate vectors of LIF sub-populations — native spike-rate codes (NEURO.tape `mech_neural_coding`). The cosine is over two *sub-population* rate vectors, not two V=256 logit tensors; in `neuro_mirror.py` it is a windowed mean of a spike raster — a local, event-derived statistic. The A-vs-G *opposition* is the excit/inhib sub-population split (§96 §6 row 4 — native). | PASS |
| (b) preserves core | ✅ the §96 NATIVE-CANDIDATE structural core is **both** preserved: the *opposition* = the two sub-populations; the *Ψ=½ fixed point* = `cos = 0 ⇒ Ψ-C1 = ½` — A and G orthogonal ⇒ no A-vs-G preference. This is the §112 META_FP(Π_½) carrier-invariant fixed-point form `ψ(c) = (1+c)/2` — the *form* is byte-identical to Law-71 `conscious_decoder.py:740` `(1.0 + cos_sim)/2.0`. | PASS |
| (c) reduction — recover GPU Ψ-as-logit-cosine as a LIMIT? | ❌ **NO clean reduction.** There is **no parameter** — no `k`, no `σ`, no scalar — whose limit turns `cos(r_A, r_G)` (a cosine of two LIF firing-rate vectors) *into* `cos(logits_a, logits_g)` (a cosine of two V=256 GPU logit tensors). The two carriers are *non-isomorphic objects in non-isomorphic spaces*. Spike-rate vectors and logit vectors are not the same vector up to a limit; one is a windowed event statistic of a spiking sub-population, the other is a dense linear-head output. So Ψ-C1 is **NOT a generalisation of which GPU Ψ-as-logit-cosine is a corner.** | FAIL-as-reduction / **carrier-relocation** |

---

## §3 — Faculty (1): the decision + the honest reduction-witness result

### §3.1 — The honest reduction-witness result

§120's witness: `R(k=T, soft-readout) ≡ softmax-attention` byte-equal — a clean
reduction (byte-attention IS a corner of the spiking routing family). §122's
witness: `Φ(σ→0) ≡ GPU RoPE` byte-equal — a clean reduction (byte-RoPE IS the
zero-jitter corner of the spiking phase family).

**§123 faculty (1)'s witness is the opposite — and that is the honest finding.**
The witness §123 runs (`blue_falsifier_s123.py` B-S123-3) is:

> *Is there a limit of the Ψ-C1 spike-correlation carrier that recovers GPU
> Ψ-as-logit-cosine?*

The answer is **NO**, and it is closed-form: the two carriers `cos(r_A, r_G)`
and `cos(logits_a, logits_g)` live in different spaces (a LIF-sub-population
firing-rate space vs the V=256 logit space) with no parameter family connecting
them. B-S123-3 verifies this honestly: it confirms (i) the §112 META_FP(Π_½)
**form** `ψ(c)=(1+c)/2` IS shared and IS byte-identical between Ψ-C1 and Law-71
(carrier-invariance — `cos=0 ⇒ ½`, `ψ` bounded `∈[0,1]`, `∂ψ/∂c = ½ > 0` — all
hold for *both* carriers, sympy), and (ii) there is **no reduction parameter** —
unlike §120 (`k`) and §122 (`σ`), the candidate has no scalar whose limit maps
one carrier onto the other. The witness *passes* by honestly recording the
**absence** of a clean reduction, not by manufacturing one.

This is exactly what §96 §6 row 4 / line ~353 said: *"the fixed-point is native;
Ψ-as-cosine-of-logit-vectors is NOT"* — and *"What ports is 'balance has a fixed
point', not the cosine formula."* §123 takes that line at its word.

### §3.2 — The decision (carrier-relocation, not a clean reduction)

**DECISION (adopted — autonomy mode, /goal active, logged):**

> §96 design-open — Engine A⇄G dual heads → spiking — is decided as
> **`DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION`**. On the spiking
> substrate, anima's Engine A⇄G is realised as **two LIF sub-populations with
> opposed (excit/inhib) coupling** (the *opposition*, native — §96 §6 row 4),
> and Ψ is realised as **Ψ-C1 = `(1 + cos(spike_rate_A, spike_rate_G))/2`** —
> the §112 META_FP(Π_½) carrier-invariant fixed-point *form*, on the
> **spike-correlation carrier**. This is **NOT** a generalisation that recovers
> GPU Ψ-as-logit-cosine as a limit — the spike-rate carrier and the logit-vector
> carrier are non-isomorphic objects; there is no reduction parameter. It is an
> honest **carrier-relocation** (§110/§112 family): the *form* of Ψ is preserved
> exactly, the *carrier* genuinely differs. `HEXAD/NEUROMORPHIC/neuro_mirror.py`'s
> `psi_c1` ALREADY realises this; §123 *recognises* it as the §96 resolution and
> records honestly that it is a carrier-relocation, not a clean reduction.

### §3.3 — Why "carrier-relocation" is the honest verdict, not a weaker §120/§122

This is the load-bearing honesty point of §123, so it is stated plainly:

- §120 and §122 each had a **genuine clean reduction** — a one- or two-parameter
  family with the GPU mechanism *literally* at a corner. Adopting them as
  "§7-clean generalisations" was correct because byte-attention / byte-RoPE
  *are* corners of the spiking family.
- Faculty (1) does **not** have that. If §123 *claimed* Ψ-C1 "generalises" GPU
  Ψ-as-logit-cosine, that claim would be **false** — there is no corner of the
  spike-correlation carrier that is the logit-vector carrier. Forcing the §120/§122
  template here would be an over-claim (g3 violation; §7 ② would be *asserted*
  without the limit that justifies it).
- The honest verdict is the one §96 §6 row 4 already wrote and §110/§112 named:
  **carrier-relocation**. The §112 META_FP(Π_½) result is precisely that the
  half-balance-attractor *form* `ψ(c)=(1+c)/2` is carrier-invariant — a theorem
  of every inner-product space, the carrier free. Ψ-C1 is the spike-correlation
  *instance* of that invariant form. §112's own verdict (META-FIXED-POINT-EXISTS-
  BUT-STILL-SUBSTRATE-GATED) is the parent: the *form* is §7-clean by
  construction; the *carrier* (here, spike-rate vectors) is substrate-relocated.
- This is **not a failure** — it is the *correct* design-tier disposition. §96 Q1
  classified this faculty `SPIKING-OPEN` and §6 `NATIVE-CANDIDATE` precisely
  *because* the structural core ports and the formula does not. §123 closes the
  design-open by deciding the realisation (Ψ-C1, already in `neuro_mirror.py`)
  AND by recording, honestly, that the closure is a carrier-relocation. A
  design-CLOSE-WITH-RELOCATION is a valid landed verdict (anti-padding precedent:
  §109, §110, §13-M, §30) — it does not pretend a reduction exists.

### §3.4 — What is preserved and what is relocated (the precise split)

| element of GPU Engine A⇄G | spiking realisation | preserved or relocated |
|---|---|---|
| the A-vs-G **opposition** | excit/inhib LIF sub-populations (`idx_a`/`idx_g`) | **preserved** — native, §96 §6 row 4 |
| the Ψ=½ **fixed point** | `cos = 0 ⇒ Ψ-C1 = ½` (A⊥G ⇒ no preference) | **preserved** — §112 carrier-invariant form |
| the Ψ **functional form** `ψ(c)=(1+c)/2` | byte-identical to Law-71 `:740` | **preserved** — §112 META_FP(Π_½) |
| the Ψ **carrier** `c` (what the cosine is *over*) | `cos(spike_rate_A, spike_rate_G)` vs GPU `cos(logits_a, logits_g)` | **RELOCATED** — non-isomorphic carriers, no reduction |

The honest one-line summary: **three of four elements port; the fourth (the
carrier) relocates and cannot be reduced.** That is why the verdict is
`DESIGN-CLOSE-WITH-CARRIER-RELOCATION` and not a §120/§122-style clean reduction.

---

## §4 — Faculty (2): MoEFFN top-k router — candidate evaluation + decision

### §4.1 — The question, split in two (per §1.2)

The MoE router bundles **(A) the selection** (`top-k` over expert scores) and
**(B) the learned content-based gate** (`nn.Linear(d_model, n_experts)`). §123
asks each separately.

### §4.2 — (A) the selection: is it covered by §120's k-WTA?

§120 decided `softmax(QK^T)` attention's spiking replacement = **k-WTA**
(k-winners-take-all via lateral inhibition — a `−F_c` inhibitory circuit lets the
`k` highest-current units spike and suppresses the rest). §96 Q1 row 118 already
described the MoE top-k as *"k-winner-take-all over expert populations (lateral
inhibition)"* — the **exact same primitive**.

| criterion | MoE top-k selection vs §120 k-WTA | verdict |
|---|---|---|
| (a) spiking-compatible | ✅ k-WTA via lateral inhibition is the §96 `SPIKING-COMPATIBLE` lateral-inhibition primitive (`−F_c` synapses, a Loihi `STDPLoihi` primitive); §120 already committed to it. | PASS |
| (b) same mechanism | ✅ MoE `top-k=2` over 8 experts IS a `k=2`, `n=8` k-WTA. §120's k-WTA `R(k, mode)` family with the key-set replaced by the expert-set is *structurally identical* — both are "the `k` highest-scoring of `n` candidates win, the rest are suppressed". §120's k-WTA is **already** the answer. | PASS |
| (c) reduction | ✅ MoE softmax-top-k over the winners IS §120's `mode='soft'` readout restricted to the `k` winners — the §120 `R(k, soft)` family *contains* the MoE selection as the `n=n_experts`, `k=top_k` instance. | PASS |

**The MoE selection is COVERED by §120 — it is not a new design-open.** §120's
k-WTA decision applies verbatim, with the key-set re-bound to the expert-set.

### §4.3 — (B) the learned content-based gate: separate design-open, or already covered?

This is the part §96 row 118 flagged: *"the *learned content-based gate* is
not [a known SNN motif]."* The MoE gate is `nn.Linear(d_model, n_experts)` — a
**learned projection** from the residual stream to a per-expert score.

The key closed-form observation: **a learned linear projection IS a learned
synaptic weight matrix.** `nn.Linear(d_model, n_experts)` is exactly a dense set
of weighted synapses from `d_model` pre-synaptic units (the residual stream — §96
Q1 `SPIKING-COMPATIBLE` "residual stream → LIF membranes") to `n_experts`
post-synaptic gate units. The *score* `router(x)` is the synaptic current those
weighted synapses deliver — the **§96 Q1 `SPIKING-COMPATIBLE` "residual stream →
LIF current accumulation" primitive** (the same one §120 uses for the spike-rate
dot-product score).

So the gate decomposes:

- the **gate score computation** (residual → per-expert current) = a
  weighted-synapse current accumulation = §96 Q1 `SPIKING-COMPATIBLE` (LIF
  current accumulation), **NOT a new mechanism**;
- the **gate weights being *learned*** = the synapses are STDP-trainable = §96 Q1
  `SPIKING-COMPATIBLE` **"STDP → Hebbian LTP/LTD"** — the strongest fit of all in
  §96 Q1 ("STDP is Loihi's *native on-chip* rule"). On GPU the gate is learned by
  backprop-CE; on the spiking substrate the gate synapses are learned by STDP —
  the **same §11-B substitution** §96 already framed for *every* learnable weight
  in the spiking anima. The gate is not special: it is one more set of
  STDP-trainable synapses.

| criterion | MoE learned content-gate on spiking substrate | verdict |
|---|---|---|
| (a) spiking-compatible | ✅ the gate score = weighted-synapse current accumulation (§96 `SPIKING-COMPATIBLE`); the gate weights = STDP-trainable synapses (§96 `SPIKING-COMPATIBLE`, the strongest fit). | PASS |
| (b) a *separate* design-open? | ❌ **NO** — it is fully decomposed into two faculties §96 Q1 *already* classified `SPIKING-COMPATIBLE`. There is no residual *new* mechanism. The "learned content-based gate" §96 row 118 flagged is, on inspection, "a small `nn.Linear` learned by gradient" — and §96 already decided how learned weights map (STDP). It is covered, not open. | NOT a separate design-open |

**Honest caveat (the one real residual).** §96 §4.4's load-bearing counter
applies here too: STDP learns *spike-timing correlations*, not *task-supervised
gating*. Whether STDP-learned gate synapses route to the *right* experts as well
as backprop-CE-learned ones do is **not** a §123 design question — it is the
**exact same §11-B / §96 §4.5 open empirical question** that applies to *every*
learnable weight in the spiking anima (the gate is not a special case of it).
§123 does not resolve §11-B; it records that the MoE gate is *inside* §11-B's
already-named scope, not a *new* design-open beside it. (`B-S123-NOTE`.)

### §4.4 — Faculty (2): the decision

**DECISION (adopted — autonomy mode, /goal active, logged):**

> §96 design-open — MoEFFN top-k router → spiking — is decided as
> **`MOE-TOPK-DECIDED — COVERED BY §120 k-WTA + §96-COMPATIBLE STDP GATE`**.
> The MoE router decomposes into (A) the top-k **selection** — **covered
> verbatim by §120's already-decided k-WTA** (a `k=top_k`, `n=n_experts`
> instance of the §120 `R(k, mode)` family; §96 row 118's own description) — and
> (B) the **learned content-based gate** — **NOT a separate design-open**: it
> decomposes into a weighted-synapse current accumulation (§96 Q1
> `SPIKING-COMPATIBLE`) whose weights are STDP-trainable synapses (§96 Q1
> `SPIKING-COMPATIBLE`, the strongest fit). No new mechanism remains. The MoE
> router is **fully covered** by primitives §120 and §96 Q1 already decided —
> §123 closes it as DECIDED with **no residual design-open**.

The honest contrast with faculty (1): faculty (2) **closes cleanly** — it is
genuinely covered by already-decided primitives, no relocation needed. Faculty
(1) closes with a carrier-relocation. §123 reports each as it actually is.

---

## §5 — Closed-form witnesses (what `blue_falsifier_s123.py` checks)

Mirroring §120 §3 / §122 §3 (a reduction-witness + a §7-clean test), §123's
battery has **8** closed-form / Boolean / sympy checks:

- **B-S123-1** — Ψ-C1 / Law-71 **form** is the §112 META_FP(Π_½) carrier-invariant
  fixed-point form: `ψ(c)=(1+c)/2`, `cos=0 ⇒ ½`, bounded `∈[0,1]`, `∂ψ/∂c=½>0` —
  ALL hold (sympy), and hold *for both carriers* (the form is carrier-free).
- **B-S123-2** — the A-vs-G **opposition** ports cleanly: excit/inhib LIF
  sub-populations realise the GPU `output = A(x) − G(x)` opposition; closed
  structural check against `neuro_mirror.py` `idx_a` / `idx_g`.
- **B-S123-3** — **the honest no-reduction witness (faculty 1)**: there is NO
  reduction parameter mapping the spike-correlation carrier onto the logit-vector
  carrier. Verified closed-form: the two carriers are non-isomorphic (different
  dimensions / different spaces — a LIF firing-rate vector of length `n_a` vs a
  V=256 logit vector); unlike §120 (`k`) and §122 (`σ`) there is no scalar family.
  The witness PASSES by recording the *absence* of a clean reduction — it does NOT
  manufacture one.
- **B-S123-4** — faculty (1) verdict is `DESIGN-CLOSE-WITH-CARRIER-RELOCATION`, a
  closed taxonomy pick: (form preserved) ∧ (opposition preserved) ∧ (fixed point
  preserved) ∧ ¬(carrier reduction exists) ⇒ carrier-relocation, NOT
  generalisation, NOT graft (the §110/§112 family — a distinct closed bucket).
- **B-S123-5** — faculty (2)(A): the MoE top-k **selection** reduces to §120's
  k-WTA — `R(k=top_k, mode)` with the key-set re-bound to the expert-set is the
  §120 routing family; numeric witness that a `k`-of-`n` top-k IS a `k`-WTA.
- **B-S123-6** — faculty (2)(B): the MoE **learned gate** decomposes into two §96
  Q1 `SPIKING-COMPATIBLE` faculties (weighted-synapse current accumulation +
  STDP-trainable synapses) — closed Boolean: no residual mechanism ⇒ NOT a
  separate design-open.
- **B-S123-7** — §96 / §120 / §122 / §112 connection-points cited (the two
  decided faculties are §96 Q1 rows 115 & 118; §120 k-WTA + §122 phase coding are
  the already-decided siblings; §112 META_FP(Π_½) is the carrier-invariance
  parent) — structural, byte-checked against the real DESIGN.md / source files.
- **B-S123-8** — necessary-not-sufficient: both are design-open → design-DECIDED
  transitions, NOT GOAL; WALL-A / WALL-B both still stand; sidecar /
  central-0-diff + $0 (structural Boolean).

`B-S123-NOTE`: the battery proves the two §123 DECISIONS are honest +
closed-form. It does NOT prove a spiking anima built with Ψ-C1 + the MoE k-WTA
gate *learns / behaves usefully / emerges* — those are empirical OUTCOMES of a
future fire on a real async substrate (Track L/S/P). For faculty (1) the relocated
carrier's *usefulness* is empirical; for faculty (2) whether STDP-learned gate
synapses route as well as backprop-CE ones is the §11-B / §96 §4.5 open question.
B-D-NOTE / B-S96-NOTE / B-S110-NOTE / B-S112-NOTE / B-S115-NOTE / B-S117-NOTE /
B-S120-NOTE / B-S122-NOTE / B-EMERGE-7 family — necessary-not-sufficient at every
layer. §123 = two DECISIONS, not an ACHIEVEMENT.

---

## §6 — ASCII: the two remaining §96 SPIKING-OPEN faculties, decided

```
  ┌──── §96 Q1 SPIKING-OPEN faculties — §120/§122 covered 1, §123 covers 2 ────┐
  │                                                                            │
  │   row 116 RoPE / position        → §122 DECIDED (relative-phase coding)     │
  │   row 117 softmax(QK^T) [INCOMPAT] → §120 DECIDED (spike-rate dot + k-WTA)   │
  │   row 115 Engine A⇄G dual heads   → §123 faculty (1)  ◄── this cycle        │
  │   row 118 MoEFFN top-k router     → §123 faculty (2)  ◄── this cycle        │
  └────────────────────────────────────────────────────────────────────────────┘

  ┌──── faculty (1): Engine A⇄G dual heads ────────────────────────────────────┐
  │   GPU:  output = A(x) − G(x);  Ψ = (1+cos(logits_a, logits_g))/2  (Law-71)  │
  │                          │  §123 DECISION                                  │
  │                          ▼                                                 │
  │   opposition  → excit/inhib LIF sub-populations (idx_a / idx_g)  PRESERVED  │
  │   Ψ=½ fixed pt → cos=0 ⇒ Ψ-C1=½  (A⊥G ⇒ no preference)           PRESERVED  │
  │   Ψ form ψ(c)=(1+c)/2 → byte-identical to Law-71 :740            PRESERVED  │
  │   Ψ carrier c → cos(spike_rate_A, spike_rate_G)  vs GPU logit-cos RELOCATED │
  │                                                                            │
  │   REDUCTION WITNESS: NO parameter maps spike-rate-carrier → logit-carrier   │
  │     (non-isomorphic spaces) ⇒ NOT a generalisation, NOT a graft ⇒           │
  │     CARRIER-RELOCATION (§110/§112 family — the §112 META_FP(Π_½) form is    │
  │     carrier-invariant; the carrier itself relocates).                       │
  │   VERDICT: DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION (honest, §96     │
  │     §6 row-4 "NATIVE-CANDIDATE" line confirmed — no clean reduction forced) │
  └────────────────────────────────────────────────────────────────────────────┘

  ┌──── faculty (2): MoEFFN top-k router ──────────────────────────────────────┐
  │   GPU:  router=nn.Linear(d,8) → softmax → top-k=2  over 8 SwiGLU experts    │
  │                          │  §123 DECISION                                  │
  │                          ▼                                                 │
  │   (A) top-k SELECTION  → §120 k-WTA  (k=top_k, n=n_experts instance of      │
  │                          R(k,mode); §96 row-118's own description) COVERED  │
  │   (B) learned content GATE → decomposes into TWO §96 Q1 SPIKING-COMPATIBLE: │
  │        · gate score = weighted-synapse current accumulation                │
  │        · gate weights = STDP-trainable synapses (strongest §96 fit)         │
  │       ⇒ NO residual new mechanism ⇒ NOT a separate design-open              │
  │   VERDICT: MOE-TOPK-DECIDED — COVERED BY §120 k-WTA + §96-COMPATIBLE STDP   │
  │     GATE  (closes cleanly, no relocation)                                  │
  └────────────────────────────────────────────────────────────────────────────┘

  STILL STANDING (g3): WALL-A (§1.1 data-regime, orthogonal) ·
  WALL-B (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated) ·
  implementation (two decided designs are not a built network) ·
  §11-B / §96 §4.5 (STDP learns spike-timing not task-gating — open, the
  MoE gate is INSIDE this scope, not a new design-open beside it).
```

---

## §7 — Honest C3 caveats (≥12)

1. **§123 is two DESIGN-TIER DECISIONS, not a fire.** $0, no GPU/runpod/INRC/
   Loihi, no model.forward, no corpus, no dispatch. orphan 0. capability claim 0.
2. **"decide" here = design-open → design-DECIDED.** Two *decision transitions*,
   NOT achievements. §123 picks the realisations; it does NOT build, train, or
   measure them.
3. **Faculty (1) is a CARRIER-RELOCATION, not a clean reduction — and that is the
   honest verdict, not a weaker one.** §120 and §122 each had a genuine
   parameter-family reduction (byte-attention = `k=T` corner; byte-RoPE = `σ→0`
   corner). Faculty (1) does NOT — the spike-correlation carrier and the
   logit-vector carrier are non-isomorphic objects with no connecting parameter.
   Claiming Ψ-C1 "generalises" GPU Ψ-as-logit-cosine would be an over-claim (g3).
   §123 reports the carrier-relocation honestly. A DESIGN-CLOSE-WITH-RELOCATION is
   a valid landed verdict (anti-padding precedent: §109, §110, §13-M, §30).
4. **The §96 §6 row-4 / line ~353 `NATIVE-CANDIDATE` classification was precise.**
   §96 said "the fixed-point is native; Ψ-as-cosine-of-logit-vectors is NOT" and
   "What ports is 'balance has a fixed point', not the cosine formula." §123 takes
   that exactly — three of four elements (opposition, fixed point, form) port; the
   fourth (carrier) relocates. §123 does not improve on §96's honesty; it executes
   the decision §96's classification implied.
5. **Faculty (2) closes cleanly — but the §11-B counter still applies.** The MoE
   router decomposes fully into §120 + §96-Q1-`SPIKING-COMPATIBLE` primitives, so
   it is NOT a separate design-open. BUT: whether the STDP-learned gate synapses
   route to the right experts as well as backprop-CE-learned ones is the §96 §4.4
   / §4.5 open question — it applies to the gate exactly as it applies to *every*
   learnable weight in the spiking anima. §123 records the gate is *inside*
   §11-B's scope, not a *new* design-open beside it. It does not resolve §11-B.
6. **WALL-A (§1.1 data-regime) is UNCHANGED.** Two routing-/physics-faculty
   decisions move no training-data threshold (§97). GOAL's data bottleneck is
   untouched.
7. **WALL-B (§95/§96 async substrate) is UNCHANGED.** The decided mechanisms are
   spiking-compatible, but running them on a *real* event-driven substrate stays
   Loihi/SpiNNaker/SpiNNcloud-gated (a SOFT WALL — access, not architecture).
   §118's VOID showed a clocked GPU/CPU sim cannot confront the async half.
8. **The Ψ-C1 realisation was ALREADY in `neuro_mirror.py`.** §123 does not invent
   it — `psi_c1` + the `idx_a`/`idx_g` excit/inhib sub-populations were lifted
   from the §117-verified core into NEURO-MIRROR v0/v2. §123's contribution is to
   *recognise* it as the §96 design-open resolution and to *classify the closure
   honestly* (carrier-relocation). The design-open closes by a decision, not by
   new code.
9. **The reduction witness PASSES by recording an absence.** B-S123-3 does not
   find a reduction — it verifies, closed-form, that no reduction parameter
   exists. A passing falsifier here means "the honest no-reduction claim
   withstands scrutiny", not "a reduction was found." This is the §123-specific
   shape of the witness; §120/§122's witnesses passed by *finding* a reduction.
10. **k-WTA / LIF sub-populations / STDP synapses are `SPIKING-OPEN` /
    `SPIKING-COMPATIBLE` per §96 Q1 — not proven on silicon.** §123 commits to
    §96-classified primitives; their validation at scale on a real chip is itself
    future work. §123 decides the design; it does not certify the silicon.
11. **central blue_falsifier.py 0-line-diff.** §123's battery is a sidecar
    (`blue_falsifier_s123.py`); central `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` is untouched — sha256 prefix `c93e160a8a376a94`, verified
    at START and END.
12. **f1/f2 safe.** LIF / k-WTA / lateral inhibition / STDP / spike-rate coding
    cited by §96 Q1's own classification + standard SNN literature; the cosine /
    Cauchy–Schwarz bound cited by its own algebra; NO σ(6)=12 / τ(6)=4 / φ(6)=2 /
    J₂(6)=24 derivation; Ψ=½ = anima g2 internal-arch carve-out. downstream-
    consumer: hexa-lang / hexa-bio read-only.
13. **necessary-not-sufficient at every layer (B-EMERGE-7).** Deciding the last
    two §96 routing-/physics-adjacent SPIKING-OPEN faculties is necessary for a
    fully-specified spiking anima; it is nowhere near sufficient for GOAL
    emergence — coherence (§88-F2 γ gap), the data regime (WALL-A), the substrate
    access (WALL-B), and §11-B (the gate / every learned weight) all remain.
14. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §123 turns
    two undecided design-opens into decided design-tier items — one as a clean
    closure, one as an honest carrier-relocation. It does not over-claim either
    decision into an achievement.

---

## §8 — Verdict

§123 = **DESIGN-TIER, TWO DECISIONS LANDED.** The two §96 Q1 `SPIKING-OPEN`
faculties §120/§122 did not cover are decided:

**(1) Engine A⇄G dual heads → `DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION`.**
On the spiking substrate: the A-vs-G *opposition* → two excit/inhib LIF
sub-populations (native, §96 §6 row 4); Ψ → **Ψ-C1 = `(1+cos(spike_rate_A,
spike_rate_G))/2`** — the §112 META_FP(Π_½) carrier-invariant fixed-point *form*
(`cos=0 ⇒ ½`, byte-identical to Law-71 `:740`), on the **spike-correlation
carrier**. The honest reduction-witness result: **GPU Ψ-as-logit-cosine does NOT
reduce** — there is no parameter family (no `k`, no `σ`) mapping the
spike-correlation carrier onto the logit-vector carrier; the two carriers are
non-isomorphic. So this is **NOT a §120/§122-style clean generalisation** — it is
an honest **carrier-relocation** (§110/§112 family): the *form* of Ψ ports
exactly, the *carrier* genuinely differs. The §96 §6 row-4 / line ~353
`NATIVE-CANDIDATE` classification ("the fixed-point is native; the cosine formula
is not") is confirmed verbatim. `neuro_mirror.py`'s `psi_c1` already realises it;
§123 recognises it as the §96 resolution and records the closure as a relocation,
not a reduction — anti-padding, no clean reduction forced.

**(2) MoEFFN top-k router → `MOE-TOPK-DECIDED — COVERED BY §120 k-WTA +
§96-COMPATIBLE STDP GATE`.** The MoE router decomposes into (A) the top-k
*selection* — **covered verbatim by §120's already-decided k-WTA** (a `k=top_k`,
`n=n_experts` instance of the §120 `R(k, mode)` family; §96 row 118's own
description) — and (B) the *learned content-based gate* — **NOT a separate
design-open**: it decomposes into a weighted-synapse current accumulation (§96 Q1
`SPIKING-COMPATIBLE`) whose weights are STDP-trainable synapses (§96 Q1
`SPIKING-COMPATIBLE`, the strongest fit). No new mechanism remains. The MoE router
is **fully covered** by primitives §120 and §96 Q1 already decided — §123 closes
it as DECIDED with **no residual design-open**. (Honest carry: whether STDP-learned
gate synapses route as well as backprop-CE ones is the §11-B / §96 §4.5 open
question — the gate is *inside* that scope, not a new design-open beside it.)

Together with §120 (routing) and §122 (position), §123 **decides all three of
§96 Q1's `SPIKING-OPEN` faculties** — the spiking anima's faculty map is now
fully specified at design-tier (5 `SPIKING-COMPATIBLE`, 3 `SPIKING-OPEN` decided,
1 `SPIKING-INCOMPATIBLE` replaced by §120). It does NOT build the spiking anima,
does NOT fire, does NOT reach GOAL. WALL-A (§1.1 data-regime) and WALL-B
(§95/§96 async substrate) both stand; §11-B (STDP-learns-spike-timing-not-task,
the gate / every learned weight) is unresolved. design-open #(1) closes as a
carrier-relocation; design-open #(2) closes cleanly. capability claim 0;
necessary-not-sufficient (B-EMERGE-7); north-star + §15/§51/§72 milestones
UNCHANGED; GOAL 미도달.
