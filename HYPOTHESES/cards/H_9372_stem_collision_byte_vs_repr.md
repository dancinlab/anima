# H_9372 — V3 STEM-COLLISION: is the stem side of the operator's address a BYTE FORM or a REPRESENTATION?

**tier**: ⛔ **INVALID-ANCHOR** (pre-registered gate G-ANCHOR tripped on s7: nat D-acc 0.6552 > 0.65 by 0.0052) — the frozen aggregate verdict — **over a strong 🟢-BLEED-shaped signal** (JT p=0.0001 both seeds · surface-specific · pedestal-clean · s11 passes all 3 gates). engine-native 303M · py 2-production · $0 forward-only · aiden CPU-numpy.
**status**: MEASURED (2026-07-15) — frozen-first, no bar moved, no tune-to-green
**renumber**: H_9353→9354→9360→**9372** (parallel sessions raced origin to H_9362 mid-measurement; preemptor-wins ⟹ this lever yielded to H_9372, max+10 for collision headroom · `hypotheses-jsonl-3`)
**lane**: `g1-interface-addressable-wall` · V3
**parent**: H_9327 (BINDING 🧱) · H_9334 (C4) · H_9329 (C3) · H_9346 (EN ECHO)
**instrument**: `anima-py corpus atoms --collision-split` (NEW · engine-native) → `anima-py evaluate --xbind`
**cost**: $0 (base ckpt, zero training) · pool = summer

---

## The question

Fable's two-lane reframe says the operator addresses a fact by **(stem identity) × (surface-template class)**.
C4 (H_9334) showed the *template class* factor is **discrete** — write into the `지 않다` carrier key and the
operator reads it (12/12); write into the declarative key and it does not (C3, 0/12).

This asks the same question of the **other factor — the stem axis**:

- **BYTE-FUZZY** — the stem key is a conv net's local n-gram feature, so a stem that merely *looks* like a SEEN
  stem partially hits its address. ⟹ flip1 should **BLEED** toward the SEEN neighbour's polarity, monotonically
  in shared bytes. ⟹ held-out failure is re-read as *"the address is defined by byte neighbourhood"*, and a
  cheap hack opens (spell a new stem into a SEEN byte-neighbourhood).
- **DISCRETE / REPRESENTATIONAL** — a near-miss is a total miss. No bleed at any partial overlap; the address
  resolves only on the exact stem, and can only be *created by learning*. ⟹ strengthens H_9339's reading.

## ⛔ The briefed design is DEGENERATE — reported, not run

The lane brief assumed held-out stems sharing a long byte prefix with a SEEN stem (`재밋` vs `재밌었`).
**They do not exist**, and the builder now says so in code. Census over the frozen `gt_atoms.json`:

| | |
|---|---|
| held-out stems | **29** (the brief said 91 — wrong) |
| byte-LCP histogram (held-out × nearest SEEN) | `0B:3 · 1B:20 · 2B:6` |
| **max** byte-LCP with ANY seen stem | **2 B** — *less than one Hangul syllable* (ko = 3 B/char) |
| n in a signal stratum (≥3 B = ≥1 shared syllable) | **0** |

A 1–2 byte LCP is nothing but the shared UTF-8 high bytes that *every* Hangul character has. This is not bad
luck: `build_atoms()`'s **G-SUBSTR gate forbids a stem nesting in another**, so the atom set was *constructed*
to have no stem–stem collision. Max common *substring* is likewise 1 syllable, and it is almost always the
suffix `하`, whose SEEN donor set is polarity-**balanced** (3+/4−) and therefore carries **zero** expected bleed
by construction.

⟹ A Jonckheere trend test over empty strata is **not a negative result — it is no result**
(`power-before-negative-verdict`). The natural split is emitted as a **CENSUS ONLY** and may never carry a
verdict. **The collision must be CONSTRUCTED.**

## The instrument that does have power — prefix-graded NONCE ladder

For each 3-syllable SEEN donor `d` (polarity `p`) and `k ∈ {0,1,2,3}`:

```
nonce(d,k,f) = d[:k] + filler(d,f)[k:]        # always 3 syllables = 9 BYTES
```

shares exactly the first `k` syllables = **3k BYTES** with the donor (a_korean_byte_budget: the stratifier is
BYTES), and is otherwise unrelated filler drawn from a pool asserted disjoint from every real stem syllable.

| k | shared | role |
|---|---|---|
| k0 | 0 B | length-matched **unrelated** stem = neutral-substitution control (AUDIT-A) |
| k1 | 3 B | graded near-miss |
| k2 | 6 B | graded near-miss |
| k3 | 9 B | **the donor ITSELF** = positive control (operator known alive) |
| nat | — | the 29 natural held-out stems = H_9327 flip1 replication anchor |

Scored at flip1 with **gold = the DONOR-implied negated word** — the DV is literally *"did the operator answer
as if it had resolved the donor's address?"*

**Bias-free by construction, not by hope:**
- the 12 three-syllable donors are **6 pos / 6 neg** → a constant response bias enters ±p items with opposite
  sign and **cancels in the stratum mean** (reported split by polarity anyway — `polarity-split-before-headline`).
- every nonce is 9 B at every k → **length is matched across the whole ladder**; no stratum is confounded with
  sequence length.
- k=1 **drops the 5 donors whose 1-syllable prefix is ambiguous** (`유` prefixes both 유쾌하+ and 유치하−). A
  nonce addressed by two donors of *opposite* polarity drags the DV to zero and would **manufacture the null**
  this test exists to falsify.
- the trend test runs on **k ∈ {0,1,2} ONLY**. k3 is an *exact* address, not a partial one; folding it in would
  produce a "trend" out of the positive control alone.

rows: `k0=108 · k1=63 · k2=108 · k3=36 · nat=87` = **402** (3 surfaces × fillers), `--n-decode 402`.

## DV · bar · controls (FROZEN — no number has been read)

- **PRIMARY DV** — per-item margin `m = NLL(counterfactual) − NLL(gold)` (gold = donor-implied flip1 word).
  `m > 0` = leans donor-implied. Continuous ⇒ far more power than binary first-word.
- **Stratum statistic** `S_k = ½[mean(m | donor pol=1) + mean(m | donor pol=0)]`, on the **operator-live
  surfaces (negL, negZ) only**.
- **Anchor** `A = S_3` (exact address). All bounds are expressed as a **fraction of A** — scale-free, so the
  bound is pre-registrable without peeking at the noise scale.
- **SECONDARY** — D-acc (greedy first word == donor-implied word) per stratum.

**Gates (must pass or the run is ⛔ INVALID — an instrument failure, NOT a wall):**
- **G-POS** k3 D-acc ≥ **0.75** and `S_3 > 0`. (base SEEN flip1 measured 0.883 — corpus-py-1 ⑥.)
- **G-ANCHOR** nat D-acc ∈ **[0.35, 0.65]** (H_9327 held-out flip1 = 0.46–0.56 = chance). Off ⇒ the ckpt or
  instrument moved.
- **G-CTRL0** `|S_0| ≤ 0.20·A`. A length-matched *unrelated* nonce must not lean. If it does, the instrument
  is biased and nothing downstream is readable.

**Tests:**
- **PRIMARY (bleed)** — **Jonckheere–Terpstra** trend on item-level `m` across ordered `k ∈ {0,1,2}`, one-sided
  (increasing), p via **10,000 permutations** of the k label.
- **PEDESTAL** — donor-polarity **label shuffle** (true value = 0) recomputed through the identical pipeline.
- **SURFACE CONTROL** — the same trend on **negJ** (the no-operator surface, p≈.50 in C4). If the trend is
  equally present there, it is **not** the operator lane → a generic byte-prior effect, reinterpret.

**Verdicts (pre-committed):**
- 🟢 **BLEED / BYTE-FUZZY** — JT `p < .05` in **BOTH** seeds (s7, s11) **AND** `S_2 > 0.20·A` in both seeds.
- 🔴 **NO BLEED / DISCRETE** — **TOST**: the 90% CI of `S_1` and `S_2` lies **entirely within ±0.20·A**.
- ⏳ **UNDERPOWERED** — the 90% CI of `S_2` is **wider** than the ±0.20·A band ⇒ *no negative claim is made*.

**Seeds**: `natem_c34_main_s7.clm`, `natem_c34_main_s11.clm` (base, 20-SEEN, **zero training in this H**).

## What each outcome buys

- **BLEED** ⟹ the stem key is byte-fuzzy ⟹ the two-lane model's address is a *soft* one on the stem axis, and
  held-out failure is partly a spelling accident — a cheap escape exists.
- **NO BLEED** ⟹ stem address is **discrete/representational**: it is *created by learning*, not by form. The
  two-lane model survives with **both** factors discrete — and "write the fact" (H_9339) is the only door.

---

## RESULT (2026-07-15 · aiden CPU-numpy · `anima-py evaluate --xbind coll_manifest.json --n-decode 402`)

Ran the CONSTRUCTED nonce ladder on the two frozen base ckpts (`natem_c34_main_s{7,11}.clm`, md5 `acb5c07…` / `21bd6b5…`), zero training. `anima-py evaluate` overall held-out D-acc: **s7 0.6318 · s11 0.5871**. Manifest = 402 rows (`k0=108 k1=63 k2=108 k3=36 nat=87`), census DEGENERATE (held-out 29 · max byte-LCP 2B · signal-stratum n=0), exactly as pre-registered. Verbatim readout (`collision_readout.py`, cluster-bootstrap over 12 donors, JT 10,000 within-donor permutations):

| stratum | s7 S_k (nats) | s7 D-acc | s7 S/A | s11 S_k | s11 D-acc | s11 S/A |
|---|---|---|---|---|---|---|
| k0 (0B, unrelated) | −0.1265 | 0.389 | −0.015 | −1.0185 | 0.444 | −0.067 |
| k1 (3B) | +1.1293 | 0.667 | 0.137 | +1.0458 | 0.524 | 0.069 |
| **k2 (6B)** | **+6.9092** | **1.000** | **0.840** | **+12.0127** | **0.917** | **0.791** |
| k3 (9B = donor, A) | +8.2224 | 1.000 | 1.000 | +15.1781 | 0.917 | 1.000 |
| nat (H_9327 anchor) | +0.6366 | **0.6552** | — | +0.9731 | 0.6207 | — |

- **PRIMARY (Jonckheere trend, k∈{0,1,2}, one-sided ↑)**: **JT p = 0.0001 in BOTH seeds** — monotone byte-proximity climb.
- **SURFACE CONTROL negJ (no operator)**: JT p = 0.4384 (s7) / 0.1826 (s11) = **no trend** ⟹ the climb is **specific to the operator-live surfaces**, not a generic byte-prior.
- **PEDESTAL (donor-polarity label shuffle, true=0)**: S_2 median +0.056 (s7) / +0.171 (s11) ≈ 0.
- **GATES**: s7 → G-POS ✅ · **G-ANCHOR ❌ (0.6552 > 0.65)** · G-CTRL0 ✅ ; s11 → **all 3 ✅**.

### ⛔ VERDICT (verbatim from the frozen readout): **INVALID — a pre-registered gate failed. INSTRUMENT failure, not a wall.**

The both-seed gate requirement fails because s7's natural anchor over-reproduced H_9327 flip1 by **0.0052** (0.6552 vs the 0.65 ceiling; s11 passes at 0.6207). Per the pre-registration (`G-ANCHOR off ⟹ the ckpt or instrument moved`) the aggregate is **⛔ INVALID**. **Frozen-first, no bar moved, no re-run — a marginal gate miss is still a miss.**

**But the science the gate guards is unambiguous and I report it as a strong DIRECTIONAL BLEED (not cemented 🟢):** a nonce stem that shares *more bytes* with a SEEN donor is pulled *monotonically more* toward that donor's implied polarity — to ceiling by 6 shared bytes (k2 D-acc 1.000/0.917, S/A 0.840/0.791 ≫ the 0.20 bound) — and this happens **only on operator-live surfaces** (negJ flat) and **not under label-shuffle** (pedestal ≈0), in **both** seeds. Had s7's anchor landed 0.005 lower, the pre-registered call would have been **🟢 BLEED / BYTE-FUZZY**. So the *directional* reading is: the **stem side of the operator's address is byte-fuzzy, not a discrete learned representation** — a near-miss partially hits, and a cheap escape exists (spell a new stem into a SEEN byte-neighbourhood). This is the ⟹ **DIRECTIONAL** answer; it is **not cemented** because one seed's instrument gate tripped.

### Convergence
- **DIVERGES (directionally) from the discrete-address reading** that V1 (H_9358 TWO-LANE) and V5 (H_9353 NO-IN-CONTEXT-CHANNEL) leave open: those two locate the wall in a *missing runtime bridge* between two discrete stores; V3's directional BLEED says the **stem-axis key is soft/byte-graded**, so held-out failure is *partly a spelling accident* on the stem factor — a potential escape the two-lane picture did not predict. Because V3 is ⛔ INVALID-ANCHOR (not cemented), this is a **flag for a clean re-run**, not a refutation of TWO-LANE.
- **Does NOT touch** V1's shared-store falsification (anchor-free pooled p≈5×10⁻¹⁰) or V5's EARNED context-channel closure — those stand.

### To resume cleanly (reopen, not tune-to-green)
Re-freeze G-ANCHOR to the seed-specific measured base flip1 (or widen to [0.35, 0.70] with a *pre-registered* rationale that 0.66 is within H_9327's own inter-seed spread) **before** re-reading — the primary JT/surface-control/pedestal design is untouched and already discriminating. A clean pass would cement 🟢 BLEED / BYTE-FUZZY.
