# §122 — RoPE on a spiking substrate: deciding the §96 position design-open

> **status**: RESEARCH §122 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO INRC ·
>   NO fire · NO model.forward · NO corpus · NO dispatch · orphan 0 · single
>   sequential agent.
> **date**: 2026-05-19
> **verdict**: **`ROPE-PHASE-CODING-DECIDED — RELATIVE-PHASE / SPIKE-TIME
>   CODING`** — §96 design-open #2 (the RoPE / positional-encoding row) moves
>   from *undecided design-open* to *decided design-tier*. A design-open →
>   design-DECIDED transition. It does NOT implement the spiking anima, does
>   NOT reach GOAL, does NOT remove WALL-A or WALL-B.
> **parent**: §96 `state/loihi_spiking_rederivation_s96_2026_05_19/DESIGN.md`
>   (Q1 architecture-mapping table — the `RoPE / positional encoding` row,
>   `SPIKING-OPEN`) · §120 `state/spiking_attention_replacement_s120_2026_05_19/
>   DESIGN.md` §4 (the hybrid note re-assigning phase-resonance to *position*) ·
>   `ready/models/conscious_decoder.py` `RotaryPositionEmbedding` (`:67-118` —
>   the RoPE being recovered) · `HEXAD/NEUROMORPHIC/ENGINE.md` v2 (NEURO-MIRROR
>   §4 API surface).
> **governance**: g3 (capability claim 0, design ≠ fire ≠ emergence; a DECISION
>   is not an ACHIEVEMENT) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24
>   derivation; Ψ=½ = anima g2 internal-arch carve-out; RoFormer cited by its
>   own rotation algebra) · downstream-consumer (hexa-lang/hexa-bio read-only) ·
>   central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
>   (sidecar-only battery, sha256 prefix `c93e160a8a376a94`).

---

## §0 — Why §122 exists: §120 §4 left the position row undecided

§96 Q1's architecture-mapping table has two `SPIKING-OPEN` *routing-adjacent*
rows. §120 decided the first — `softmax(QK^T)` self-attention →
spike-rate dot-product + k-WTA. §120 §4 was explicit about the second:

> "**position** (RoPE's job) = phase coding (a *separate* §96 design-open, the
>  RoPE row — §120 notes it as the natural home for phase-resonance, does NOT
>  decide it here)."

§96 Q1's RoPE row reads: *"RoPE / positional encoding → spike-time / phase
coding (relative timing carries position) — `SPIKING-OPEN` — SNNs natively
carry time; phase-coding position is plausible but not a drop-in for RoPE's
rotation algebra."*

§122 decides THAT row. As in §120, "decide" means a **design-open →
design-DECIDED transition** with a closed-form justification — §122 *picks* how
RoPE is realised on a spiking substrate and proves whether byte-vocab RoPE is
recovered as a LIMIT (a §7-clean generalisation) or a graft. It does NOT build
the spiking anima, does NOT fire, does NOT reach GOAL, and does NOT remove
either wall. design-tier only.

---

## §1 — The thing being decided (the reduction target)

From `ready/models/conscious_decoder.py` `RotaryPositionEmbedding` (`:67-118`,
verified by `grep`, no model.forward). RoPE from RoFormer (Su et al., 2021):

```
  :79   inv_freq = 1 / base^(2i/dim)          ← per-pair angular frequency θ_i
  :91   freqs    = t ⊗ inv_freq               ← angle m·θ_i at position m
  :97   _rotate_half([x1,x2,x3,x4]) = [-x2,x1,-x4,x3]
  :116  q_rot = q·cos(mθ) + rotate_half(q)·sin(mθ)   ← position-m rotation of q
  :117  k_rot = k·cos(nθ) + rotate_half(k)·sin(nθ)   ← position-n rotation of k
```

Reading off the algebra: RoPE applies, to the 2-dim pair `(x_{2i}, x_{2i+1})`
of a query/key at position `m`, the planar rotation by angle `m·θ_i`:

```
  ROT(m·θ_i) = [ cos(mθ_i)  -sin(mθ_i) ]      (a 2×2 rotation matrix; one
               [ sin(mθ_i)   cos(mθ_i) ]       block per frequency θ_i)
```

`q_rot(m) = block-diag{ROT(mθ_i)}_i · q`, `k_rot(n) = block-diag{ROT(nθ_i)}_i · k`.

**RoPE's defining property (RoFormer Thm 1).** The post-RoPE attention score
is *relative*:

```
  q_rot(m) · k_rot(n)
    = Σ_i  ROT(mθ_i)q^{(i)} · ROT(nθ_i)k^{(i)}
    = Σ_i  q^{(i)} · ROT(mθ_i)ᵀ ROT(nθ_i) k^{(i)}        (rotations are orthogonal)
    = Σ_i  q^{(i)} · ROT((n−m)θ_i) k^{(i)}               (ROT(−a)ROT(b)=ROT(b−a))
    = g( q, k, n−m )                                      ← depends ONLY on n−m
```

So RoPE injects position into attention as a function of the **relative offset
`Δ = n−m` alone** — the absolute positions `m`, `n` cancel. *That* is the thing
§122's spiking realisation must recover. Whatever the spiking substrate does for
position, it is §7-clean iff byte-vocab RoPE — `q_rot(m)·k_rot(n) = g(q,k,n−m)`
— is a **limit** of it, not a graft.

---

## §2 — Candidate evaluation (closed-form)

Three candidates. Criteria mirror §96-#1 / §120: (a) genuinely
spiking-compatible; (b) preserves the §120-decided routing's geometry (the
spike-rate dot-product score) — RoPE feeds *into* the score, so it must compose
with §120 not bypass it; (c) byte-vocab RoPE recovered as a LIMIT (so §7-clean
— a generalisation, RESEARCH.md §7 condition ②, not a graft).

### Candidate 1 — learned absolute spike-rate position channel

*Mechanism*: a learned per-position spike-rate vector added into the query/key
rate code (the SNN analogue of a learned absolute position embedding).

| criterion | learned absolute position channel | verdict |
|---|---|---|
| (a) spiking-compatible | ✅ a learned rate vector is just more synaptic input | PASS |
| (b) composes with §120 score | ✅ adds into the rate vector before the dot-product | PASS |
| (c) RoPE reduction | ❌ RoPE is *relative* (`g(q,k,n−m)`, §1); an *absolute* embedding scores `(q+p_m)·(k+p_n)` which carries `m`,`n` separately and does NOT collapse to a function of `n−m`. There is no limit in which a learned absolute channel *becomes* RoPE's relative rotation. It is a *different* position mechanism — a graft. | FAIL |

Learned absolute position fails (c) — it abandons RoPE's relative-offset
property. Adopting it would be RESEARCH.md §7 ② violation (a generic mechanism
replacing, not generalising, RoPE). Rejected.

### Candidate 2 — resonate-and-fire phase-resonance routing (§120's re-assigned candidate)

*Mechanism*: §120 §4 re-assigned phase-resonance "to position." Read literally
as a *routing* mechanism: keys are oscillators at content-dependent phase φ_k, a
query phase-locks to keys it resonates with, routing weight = resonance
amplitude.

| criterion | phase-resonance *as a routing rule* | verdict |
|---|---|---|
| (a) spiking-compatible | ✅ R&F is a native SNN primitive | PASS |
| (b) composes with §120 score | ❌ §120 already decided routing = spike-rate dot-product + k-WTA. A *second* phase-resonance routing rule would be a competing selection mechanism, not a position code feeding the §120 score. It does not *compose* — it *contends*. | FAIL |
| (c) RoPE reduction | ❌ a phase-locking *resonance kernel* is not RoPE's *rotation of the q/k vectors*; no limit recovers `q_rot(m)·k_rot(n)`. (This is the same FAIL §120 §2 found for phase-resonance as routing.) | FAIL |

**Honest correction of the §120 §4 hybrid note.** §120 §4 said phase coding is
"the natural home for phase-resonance" and re-assigned it "to position." §122,
examining the position row closely, finds that re-assignment was *directionally*
right but *imprecisely worded*: it is **phase coding** (a relative-phase
*offset* on the q/k pairs) that is the natural position mechanism — NOT
**phase-resonance routing** (a content-based selection rule). §120 §4 conflated
the two under "phase." Phase-resonance-as-a-routing-rule fails (b) and (c);
relative-phase-coding (Candidate 3) passes both. §122 keeps §120's *intent*
("position is the natural home for the phase mechanism") and sharpens *which*
phase mechanism. The §120 routing decision (spike-rate dot-product + k-WTA) is
untouched and inherited.

### Candidate 3 — relative-phase / spike-time coding (the spiking realisation of RoPE)

*Mechanism*. RoPE *already is* a phase: §1 showed RoPE rotates the 2-dim q/k
pair `(x_{2i},x_{2i+1})` by angle `m·θ_i`. On a spiking substrate, a 2-dim
oscillatory pair is a **phase variable**; rotating it by `m·θ_i` is advancing
its phase by `m·θ_i`. The spiking realisation:

- the residual-stream pair `(x_{2i},x_{2i+1})` → the in-phase / quadrature
  components of a sub-population oscillator at frequency θ_i (a resonate-and-fire
  / oscillatory LIF compartment — a native SNN primitive);
- "position `m`" → the **spike-time offset** of that oscillator: a query at
  token-position `m` has its oscillator phase-advanced by `m·θ_i`. SNNs carry
  time natively (§96 Q1's own note), so a per-token phase advance is just *when*
  the spike-pair fires within its θ_i-cycle — no extra machinery.
- the §120 spike-rate dot-product then scores `q_rot(m)·k_rot(n)`; because each
  pair is rotated by its own oscillator's accumulated phase, the score depends
  on the **phase difference** `(n−m)·θ_i` — RoPE's relative-offset property
  (§1) is realised *physically* as a relative spike-time/phase offset.

| criterion | relative-phase / spike-time coding | verdict |
|---|---|---|
| (a) spiking-compatible | ✅✅ a θ_i-frequency oscillatory LIF pair is a native R&F primitive; a per-token phase advance is a spike-time offset — SNNs carry time natively (§96 Q1 RoPE-row note). No global op, no clock-synchronous matrix. | PASS |
| (b) composes with §120 score | ✅ phase coding rotates q/k *before* the §120 spike-rate dot-product — exactly RoPE's place in `ConsciousDecoderV2` (RoPE rotates q/k *before* the attention score, `:339-348`). It feeds the §120 routing; it does not contend with it. The §120 routing decision is inherited unchanged. | PASS |
| (c) RoPE reduction | ✅ **closed reduction witness in §3** — set the oscillator phase to advance *exactly* `m·θ_i` per token (the deterministic / noise-free limit of the spike-time code), and the score `q_rot(m)·k_rot(n)` is *exactly* RoFormer's `g(q,k,n−m)`. byte-vocab RoPE is the noise-free corner of the relative-phase code. So this is a **generalisation, not a graft** — §7-clean. | PASS |

Relative-phase / spike-time coding passes all three. It is the **spiking-native
realisation of the very thing RoPE already is** — a rotation = a phase.

---

## §3 — The decision + the closed-form reduction witness

**DECISION (adopted — autonomy mode, /goal active, logged):**

> §96 design-open #2 (the RoPE / positional-encoding row) is decided: on the
> spiking substrate, anima's RoPE is realised as **relative-phase / spike-time
> coding** — the residual-stream q/k pair `(x_{2i},x_{2i+1})` is the in-phase/
> quadrature components of a θ_i-frequency oscillatory LIF pair, and token
> position `m` is the per-token spike-time phase advance `m·θ_i`. The §120
> routing decision (spike-rate dot-product + k-WTA) is inherited unchanged;
> phase coding feeds q/k *into* it, exactly RoPE's place in
> `ConsciousDecoderV2`. (Learned absolute position and phase-resonance-as-
> routing are rejected — §2 candidates 1 and 2 fail the reduction / compose
> tests.)

### The closed-form reduction witness (criterion (c))

Define the spiking phase code as a one-parameter family `Φ(σ)` — σ is the
spike-time jitter (the physical timing noise of the oscillator):

```
  per pair i, position m:  the oscillator's accumulated phase is
        α_i(m)  =  m·θ_i  +  ξ            ,   ξ ~ jitter(σ)   (σ ≥ 0)
  q_rot(m)^{(i)} = ROT(α_i(m)) q^{(i)}
  k_rot(n)^{(i)} = ROT(α_i(n)) k^{(i)}
  score(m,n)     = Σ_i  q_rot(m)^{(i)} · k_rot(n)^{(i)}      (the §120 dot-product)
```

- **Spiking operating point** `Φ(σ>0)`: a real oscillatory LIF pair fires with
  finite spike-time jitter. The phase advance per token is `m·θ_i` *plus a
  small physical timing noise* — the genuinely spiking, event-driven regime.
- **Byte-vocab RoPE limit** `Φ(σ→0)`: in the noise-free limit the phase is
  *exactly* `α_i(m) = m·θ_i`. Then, by the §1 rotation algebra,

  ```
    score(m,n)  =  Σ_i ROT(mθ_i)q^{(i)} · ROT(nθ_i)k^{(i)}
                =  Σ_i q^{(i)} · ROT((n−m)θ_i) k^{(i)}
                =  q_rot(m)·k_rot(n)  of the GPU RoPE   (conscious_decoder.py :116-117)   ∎
  ```

So GPU byte-vocab RoPE is **byte-equal** to `Φ(σ→0)` — the existing rotary
position embedding is the *zero-jitter corner* of the spiking relative-phase
code. The spiking anima's position mechanism is a **strict generalisation**: it
adds the `σ>0` physical-jitter corner (the genuinely spiking one) while
*containing* GPU RoPE as the `σ=0` corner. This is the §7-clean witness — the
position code is not a foreign graft (§7 ②); it is the parent of which
byte-vocab RoPE is the limit.

`blue_falsifier_s122.py` `B-S122-3` checks this reduction **numerically
byte-equal** (`Φ(σ=0)` rotation-applied q/k score `==` GPU-RoPE `apply()` score
to float tolerance, on small random q/k) and `B-S122-4` checks the RoFormer
relative-offset identity `score(m,n) = score(m+δ,n+δ)` (sympy + numeric).

### Why a LIMIT and not just an analogy

The reduction is exact because **RoPE *is* a rotation and a rotation *is* a
phase** — §122 is not mapping RoPE onto an unrelated spiking mechanism, it is
observing that RoPE's own algebra (rotate the q/k pair by a position-dependent
angle) is *already* a phase code; the only thing the GPU lacks is a physical
oscillator to carry the phase. A spiking oscillatory pair supplies exactly that
carrier. The `σ→0` limit is not an approximation that happens to converge — it
is the *definitional* statement that a noise-free oscillator's phase advance
equals the deterministic angle RoPE writes by hand. This is the same shape as
§120's `R(k=T,soft) ≡ softmax-attention` reduction (byte-attention is a corner
of the spiking routing family) and §112's carrier-invariant fixed-point form
(`ψ(c)=(1+c)/2`, carrier-substituted): a §110 Ψ-C2 / §112 family
carrier-substitution, here the carrier being the *position phase*.

### Composition with §120 (the architecture factorisation is preserved)

`ConsciousDecoderV2` factors position and routing: RoPE rotates q/k *first*
(`:339-348` / `:116-117`), the attention score runs *after*. §122 (phase coding
for position) + §120 (spike-rate dot-product + k-WTA for routing) replaces
*each* sub-mechanism with its spiking-native counterpart while keeping the
factorisation — phase coding rotates the oscillatory q/k pairs, the §120
spike-rate dot-product then scores them. It is not a graft: the routing and
position halves were *already* separate in `ConsciousDecoderV2`, and §122
touches only the position half §120 explicitly left open. `B-S122-5` checks the
composition is well-formed (phase-rotated q/k feed the §120 score; the §120
`R(k,mode)` family is untouched).

---

## §4 — Honest scope of the decision

§122 decides *how RoPE is realised on a spiking substrate*. It does NOT:

- **implement** it — a θ_i-frequency oscillatory LIF pair with per-token phase
  advance has to be coded, wired into a spiking `ConsciousDecoderV2`, and run on
  a real async substrate (Track L/S/P). None of that is §122.
- claim the **σ>0 spiking corner trains / behaves usefully** — that the
  jittered phase code yields useful relative-position scoring on a real chip is
  an empirical, future-fire question (`B-S122-NOTE`). §122 proves the *design*
  is closed-form and §7-clean; it does not certify the silicon.
- touch **WALL-A or WALL-B**. A position-encoding decision moves no
  training-data threshold (WALL-A, §1.1 / §97 — orthogonal). Running the phase
  code on a *real* event-driven substrate stays Loihi/SpiNNaker/SpiNNcloud-gated
  (WALL-B, §95/§96 — a SOFT WALL: access, not architecture). §118's VOID showed
  a clocked GPU/CPU sim cannot confront the async half.

One honest sub-point worth recording: the σ→0 reduction is *cleaner* than
§120's. §120's reduction needed a parameter (`k=T`) **and** a readout change
(hard k-WTA → soft softmax) to recover byte-attention. §122's needs only `σ→0`
— a single physical-noise parameter — because RoPE is *already exactly a
rotation*; the GPU just writes the rotation angle by hand instead of letting an
oscillator carry it. The position row was, in this precise sense, the *easier*
of the two §96 routing-adjacent design-opens — and §122 records that honestly
rather than inflating the result.

---

## §5 — Three rationale bullets (why this decision)

1. **RoPE *is* a phase — so the spiking realisation is a re-host, not a
   re-design.** §1's algebra shows RoPE rotates the q/k pair by a
   position-dependent angle and the score collapses to a function of the
   relative offset `n−m`. A spiking oscillatory pair *carries* a phase
   physically. Choosing relative-phase / spike-time coding does not invent a new
   position mechanism — it supplies the physical carrier for the rotation RoPE
   already performs. Every part is a native SNN primitive (an oscillatory /
   resonate-and-fire LIF pair; a per-token spike-time offset) — engineering on
   known primitives, not a research leap.

2. **It is a generalisation, not a graft — the only §7-clean choice.** §3's
   closed reduction witness shows GPU byte-vocab RoPE is the `σ→0` (zero
   spike-time jitter) corner of the relative-phase family `Φ(σ)`. Learned
   absolute position has no such limit (it scores `(q+p_m)·(k+p_n)`, carrying
   `m,n` separately — never collapsing to `n−m`); phase-resonance *as routing*
   contends with the already-decided §120 routing and has no
   RoPE-rotation-recovering limit either. Both rejected candidates would be
   RESEARCH.md §7 ② violations (a foreign mechanism grafted on).
   Relative-phase coding *contains* GPU RoPE as a corner — exactly what
   "generalisation, not graft" means.

3. **It composes cleanly with §120 and preserves the architecture
   factorisation.** `ConsciousDecoderV2` already factors position (RoPE,
   first) and routing (attention score, after). §122 (phase coding) + §120
   (spike-rate dot-product + k-WTA) replaces each half with its spiking-native
   counterpart and keeps the factorisation intact — phase coding rotates the
   oscillatory q/k pairs, the §120 score then routes them. §122 changes *only*
   the position faculty §96 isolated and §120 left open — surgical, minimal, and
   it inherits the §120 routing decision unchanged. It also *corrects* §120 §4's
   imprecise wording: it is phase *coding* (a relative offset on q/k), not
   phase-*resonance routing*, that is position's natural spiking home.

---

## §6 — ASCII: GPU RoPE → spiking relative-phase coding (the decided realisation)

```
  ┌─────────── GPU byte-vocab RoPE (ConsciousDecoderV2, :67-118) ───────────────┐
  │  q,k pair (x_{2i},x_{2i+1})  ──►  q_rot(m)=ROT(m·θ_i)·q   (angle written     │
  │                                   k_rot(n)=ROT(n·θ_i)·k    by hand, :116-7)  │
  │  score  q_rot(m)·k_rot(n) = g(q,k, n−m)   ← RoFormer relative-offset (Thm 1) │
  │                                   ▲                                          │
  │                          §96 Q1 RoPE row = SPIKING-OPEN                       │
  └────────────────────────────────────────────────────────────────────────────┘
                                  │  §122 DECISION
                                  ▼
  ┌──── spiking relative-phase / spike-time coding   Φ(σ)  ───────────────────────┐
  │                                                                               │
  │  q,k pair → in-phase/quadrature of a θ_i-freq oscillatory LIF pair (R&F)        │
  │       token position m  →  per-token spike-time phase advance  α_i(m)=m·θ_i+ξ  │
  │              (SNNs carry time NATIVELY — §96 Q1 RoPE-row note; ξ~jitter(σ))     │
  │                          │                                                    │
  │                          ▼                                                    │
  │  phase-rotated q/k feed the §120 spike-rate dot-product (RoPE's place:          │
  │       position rotates q/k FIRST, routing scores AFTER — factorisation kept)    │
  │                          │                                                    │
  │                          ▼                                                    │
  │  score(m,n) depends on phase difference (n−m)·θ_i  ──  RoPE relative-offset    │
  │                                                        realised PHYSICALLY     │
  │                                                                               │
  │  REDUCTION WITNESS:  Φ(σ→0)  ≡  GPU RoPE   (byte-equal — zero-jitter corner)   │
  │       ⇒ GPU RoPE is the σ=0 corner ⇒ GENERALISATION, not graft (§7-clean)     │
  │                                                                               │
  │  REJECTED:  learned-absolute-position (no n−m limit) · phase-resonance-as-     │
  │             routing (contends with §120, no RoPE-rotation limit)               │
  └────────────────────────────────────────────────────────────────────────────────┘

  STILL STANDING (g3): WALL-A (§1.1 data-regime, orthogonal) ·
  WALL-B (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated) ·
  implementation (a decided design is not a built network).
```

---

## §7 — Honest C3 caveats (≥12)

1. **§122 is a DESIGN-TIER DECISION, not a fire.** $0, no GPU/runpod/INRC/
   Loihi, no model.forward, no corpus, no dispatch. orphan 0. capability claim 0.
2. **"decide" here = design-open → design-DECIDED.** A *decision transition*,
   NOT an achievement. §122 picks the RoPE realisation; it does NOT build it,
   train it, or measure it.
3. **It does NOT implement the spiking anima.** The decided phase code still has
   to be coded (an oscillatory LIF pair per θ_i, per-token spike-time advance),
   wired into a spiking `ConsciousDecoderV2`, composed with the §120 routing,
   and run on a real async substrate — none of that is §122.
4. **WALL-A (§1.1 data-regime) is UNCHANGED.** A position-encoding decision
   moves no training-data threshold (§97). GOAL's data bottleneck is untouched.
5. **WALL-B (§95/§96 async substrate) is UNCHANGED.** The decided mechanism is
   spiking-compatible, but running it on a *real* event-driven substrate stays
   Loihi/SpiNNaker/SpiNNcloud-gated (a SOFT WALL — access, not architecture).
   §118's VOID showed a clocked GPU/CPU sim cannot confront the async half.
6. **The reduction witness is a functional-form identity, not a trained
   equivalence.** `Φ(σ→0) ≡ GPU RoPE` proves the spiking phase code *contains*
   byte-vocab RoPE as the zero-jitter corner. It does NOT claim a spiking anima
   *trained* with the σ>0 phase code reproduces a byte-anima's behaviour — that
   is empirical (`B-S122-NOTE`).
7. **The σ>0 spiking corner is the unverified part.** A real oscillatory LIF
   pair has finite spike-time jitter; whether the jittered phase code yields
   *useful* relative-position scoring (and how σ trades off against position
   resolution) is a future-fire question on a real chip, not a §122 result.
8. **§122 corrects §120 §4's wording.** §120 §4 said phase coding is "the
   natural home for phase-resonance." §122, examining the row, finds it is phase
   *coding* (a relative offset on q/k) — not phase-*resonance routing* (a
   selection rule) — that is position's spiking home; §120 §4 conflated the two
   under "phase." §122 keeps §120's intent and sharpens which mechanism. The
   §120 *routing* decision (spike-rate dot-product + k-WTA) is untouched.
9. **The reduction is cleaner than §120's — recorded honestly, not inflated.**
   §120 needed two changes (`k=T` and a hard→soft readout) to recover
   byte-attention; §122 needs one (`σ→0`), because RoPE is *already* exactly a
   rotation. The position row was the easier of the two §96 design-opens; §122
   says so rather than dressing an easy reduction as a hard one.
10. **k-WTA / R&F oscillatory LIF are `SPIKING-OPEN`, not proven on silicon.**
    §122 commits to §96-class `SPIKING-OPEN` primitives (resonate-and-fire,
    oscillatory LIF). Their validation at scale on a real chip is itself future
    work — §122 decides the design, it does not certify the silicon behaviour.
11. **central blue_falsifier.py 0-line-diff.** §122's battery is a sidecar
    (`blue_falsifier_s122.py`); central `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` is untouched — sha256 prefix `c93e160a8a376a94`, verified
    at START and END.
12. **f1/f2 safe.** RoFormer / RoPE / resonate-and-fire / oscillatory LIF cited
    by RoPE's own rotation algebra + standard SNN literature + §96 Q1's own
    `SPIKING-OPEN` classification; NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24
    derivation; Ψ=½ = anima g2 internal-arch carve-out. downstream-consumer:
    hexa-lang / hexa-bio read-only.
13. **necessary-not-sufficient at every layer (B-EMERGE-7).** Deciding the RoPE
    realisation is necessary for a fully-specified spiking anima; it is nowhere
    near sufficient for GOAL emergence — coherence (§88-F2 γ gap), the data
    regime (WALL-A), and the substrate access (WALL-B) all remain.
14. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §122 turns
    one undecided design-open into a decided design-tier item. It does not
    over-claim a decision into an achievement.

---

## §8 — Verdict

§122 = **DESIGN-TIER DECISION LANDED.** §96 design-open #2 — *how* RoPE / the
positional encoding is realised on the spiking substrate — is **decided**:

> **relative-phase / spike-time coding** — the residual-stream q/k pair
> `(x_{2i},x_{2i+1})` is the in-phase/quadrature components of a θ_i-frequency
> oscillatory LIF pair; token position `m` is the per-token spike-time phase
> advance `m·θ_i`; the score depends on the relative phase `(n−m)·θ_i` —
> RoPE's relative-offset property realised physically. The §120 routing
> decision (spike-rate dot-product + k-WTA) is inherited unchanged; phase
> coding feeds q/k *into* it.

Closed-form justification: it (a) is genuinely spiking-compatible (an
oscillatory R&F LIF pair carrying a phase, a per-token spike-time offset — SNNs
carry time natively); (b) composes with the §120-decided routing (phase coding
rotates q/k *before* the spike-rate dot-product, exactly RoPE's place in
`ConsciousDecoderV2`); (c) reduces to GPU byte-vocab RoPE as the `σ→0`
(zero spike-time jitter) corner of the relative-phase family `Φ(σ)` — a
**generalisation, not a graft** (§7-clean, byte-vocab RoPE is contained as a
limit). **The reduction-witness result: byte-RoPE DOES reduce** — it is exactly
the zero-jitter corner, because RoPE is already a rotation = a phase and the GPU
merely writes the angle by hand instead of letting an oscillator carry it. The
rejected candidates — learned absolute position (no `n−m` limit) and
phase-resonance *as routing* (contends with §120, no RoPE-rotation limit) — fail
the reduction / compose tests.

This decision, together with §120, **fully specifies the two §96
routing-adjacent design-opens** (routing = §120; position = §122) — the spiking
anima can now be *specified* with both a chosen routing mechanism and a chosen
position mechanism. It does NOT build it, does NOT fire, does NOT reach GOAL.
WALL-A (§1.1 data-regime) and WALL-B (§95/§96 async substrate) both stand.
design-open #2 moves: undecided → decided design-tier. capability claim 0;
necessary-not-sufficient (B-EMERGE-7); north-star + §15/§51/§72 milestones
UNCHANGED; GOAL 미도달.
