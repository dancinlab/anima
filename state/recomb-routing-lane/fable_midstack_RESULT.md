Design grounded in the actual production forward now — I read `core/decode.py` (`_fwd_logits`, the same path `clm_forward_hidden_logits` wraps), pulled the real config off the production ckpt (`~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm` → `d=3784, K=3, L=4, E=3, V=256`), and re-read the fork-A ledger (`state/recomb-routing-lane/VERDICT.md`, `fable_forkA_wall.md`, `fable_swapcontrastive_result.md`, `step2_swapcontrastive_result.txt`). Here is the design. Verdict first:

**"Mid-stack K/V" as framed is half-moot — but not fully moot, and the half that survives changes the design.** The trunk has no attention (no K/V anywhere), it is 4 residual dilated conv blocks with a total receptive field of ~35 bytes, and the residual stream makes per-layer states additive increments of each other, not reparameterizations. Crucially, **"the final readout collapses it" is already falsified as the failure mechanism**: concept identity survives *to yn* in pooled form (probe 0.95 / 0.60 held-out, Gate2), and literal content *is* consumable from yn (Step-1 lit copy +1.22→1.66 worked). What a tap can genuinely change is not identity access but **payload basis** — and the decisive, cheapest question is one nobody has probed: whether the **associative payload (concept → unshown-kw)** exists read-side at *any* depth. That's the STEP-0 below. Spec:

---

## 1. Architecture reality — where the tappable intermediates actually are

`_fwd_logits` (core/decode.py:543) for the production 303M:

```
xe  = embed[ids]                      [T,3784]   tap: EMB
xt0 = conv_ec(xe, K=3, dil=1)                    tap: EC     (RF 3)
xt1 = xt0 + gelu(GN(conv(xt0, dil=1)))           tap: T1     (RF 5)
xt2 = xt1 + gelu(GN(conv(xt1, dil=2)))           tap: T2     (RF 9)
xt3 = xt2 + gelu(GN(conv(xt2, dil=4)))           tap: T3     (RF 17)
xt4 = xt3 + gelu(GN(conv(xt3, dil=8)))           tap: T4     (RF 33)
r   = router(xt4)  [T,3]                          tap: RTR
ex  = gelu(conv_e(xt4)) ×3 → MoE mix → y          tap: MOE    (RF 35)
yn  = GN(y)                                       tap: YN  ← fork-A read here; falsified
logits = readout(yn)   (SLW slot applies at yn on the E1-SLW ckpt — taps are all pre-slot)
```

Three consequences you must design around:

1. **No position at any depth ever sees the distal concept.** RF caps at 35 bytes; the corpus GAP is ≥128. The concept exists *only* in cross-position pools, at **every** layer equally. So the transformer intuition "mid-stack K/V is pre-collapse" does not transfer: nothing is collapsed between T2 and YN that the pool didn't already survive.
2. **Residual stream ⇒ taps T1..T4 are nested sums** (`pool(xt4) = pool(xt2) + pool(later increments)`). Linear accessibility will barely differ across T1..T4. The only *representationally distinct* families are: **EMB/EC (literal byte basis)**, **the residual stream (one family)**, **RTR+MOE (the only non-residual computation — the MoE routing state, the nearest analog to "expert K/V")**, and **YN (falsified)**.
3. **The failure signature localizes the wall at the payload/consumption side, not identity access**: identity pools fine at YN; lit copy works at YN; trained contrastive routing at YN lands `Wo≈0`, `on≈shuf`, held-out Δzero∅. The one mechanistic story a tap adds: **YN rows at block positions are next-byte-prediction features of those positions, not a transferable "concept content" code — EMB/EC rows are literal payload; deep pooled rows are address.** fork-A used YN rows as both address and payload.

So: the honest experiment is not "tap layer ℓ instead of yn," it is **split address/payload** — K (address) from pooled deep residual, V (payload) from shallow literal rows — plus one probe column for the MoE routing state. That is the only arm not already morally covered by fork-A.

## 2. Lane design (FULL step — fires only if STEP-0 cracks)

Identical to the hardened swap-contrastive xattn lane (same loss `L = CE_span + 0.1·KL_sil + λc·InfoNCE(Δ_v/T=0.1)`, same Wo σ=0.01 init, same gated tether-clip logit-bias injection at emit, frozen trunk, DISJOINT from emit-drive, read-side only). **Single change — K/V source:**

- **Arm S (split, primary):** K_j from `xt2` rows (address; any residual depth works, T2 chosen as mid), V_j from `EC` rows (literal payload) at the same positions j. Queries from `yn_t` at the emit position, unchanged.
- **Arm U (uniform tap, secondary):** K_j = V_j = `xt2` rows. This is the literal "mid-stack tap" — run it only to complete the family closure if Arm S nulls.

No trunk retraining, no new write path, lane params only (~3M), same 40 train / 8 val / 12 eval concept split, digit-free C-named bank, even per-concept coverage.

## 3. STEP-0 — kill cheaply before any lane training

**Gate-0 (harness validity, blocking):** the last stored eval landed `INVALID lit-dead` (`step2_swapcontrastive_result.txt`). Whatever caused that must be fixed and **Δlit CI_lo > 0 must pass FIRST at the tap** before any null counts. A lit-dead run is INVALID, never 🧱.

**S0-A — association-accessibility probe (the decisive $0 pre-check, no lane, no training beyond ridge).**
The associative bar requires concept → *unshown*-kw mapping. Gate2 only ever probed *identity*. Test directly whether the associative payload exists read-side at any depth:

- For each doc, pooled tap vector `p_ℓ(doc)` (causal mean over block span) at ℓ ∈ {EC, T2, T4, MOE(+RTR), YN}.
- For each keyword, `q_ℓ(kw)` = pooled tap of the kw bytes forwarded in isolation (~150 short forwards, seconds each).
- Train a bilinear map `score = p_ℓ(doc)ᵀ M q_ℓ(kw)` (ridge) on the 40 train concepts: positives = the doc's concept's kws **including the 3 unshown**, negatives = matched distractor kws. Evaluate **held-out-concept AUC on unshown-kws vs matched distractors**, cluster-bootstrap by concept.
- Also record identity-probe acc per ℓ (replicates Gate2; expect ≈flat across T1..T4 per the residual argument — treat as a sanity check of consequence 2, not a verdict).

**Kill rule:** if unshown-kw AUC CI ≤ chance at **every** tap, the associative payload does not exist read-side anywhere in the frozen trunk → the family is 🧱 **without training a single lane**, and the diagnosis upgrades from "readout-routing wall" to "consumable concept→content association absent in the 303M substrate" — read-side rescue impossible at any depth, only trunk training (γ) can add it.

**S0-B — causal floor: oracle-pool + contrastive Wo (the Δzero−ΔshufV analog at the tap).**
This is the pre-registered maximally-favorable family member, moved to the tap: routing handed over for free (fixed uniform pooling over the **known** block span at tap ℓ — no learned attention), train **only Wo** (k×V) with the identical InfoNCE swap-contrastive loss on the existing paired match/swap docs, eval once on the geometry-matched n=132 swap-margin. Run per arm: {EC, T2, split K:T2/V:EC, MOE}. Minutes of CPU training per arm once features are precomputed; the frozen forwards dominate cost.

- If oracle-routed, contrastive-trained readout of tap-ℓ features cannot produce held-out `CI_lo(Δzero)>0 ∧ CI_lo(Δzero−ΔshufV)>0` (lit alive), then no learned-attention lane on that tap can — the lane's only frozen downstream is the emit interface itself.
- Only a S0-B crack unlocks the FULL Arm-S lane.

**The hook (Q5) — new read-only function needed; `clm_forward_hidden_logits` is insufficient** (it exposes only YN). Minimal addition to `core/decode.py` (py channel = canonical measurement path per session policy), mirroring `_fwd_logits` op-for-op:

```python
def clm_forward_taps(W, tok, T, want=("ec", "t2", "t4", "moe", "yn")):
    """Read-only multi-tap forward: returns (taps: {name: [T,d]}, logits: [T,V]).
    Same ops/order as _fwd_logits; taps are copies; production paths untouched."""
    d = W["d"]; E = W["E"]; V = W["V"]; K = W["K"]; L = W["L"]
    taps = {}
    xe = W["embed"][tok.astype(np.int64)]
    xt = _conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    if "ec" in want: taps["ec"] = xt.copy()
    dil = 1
    for li in range(L):
        h = _conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, min(dil, 512))
        hg = nn_gelu_fwd(nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1))
        xt = xt + hg.reshape(T, d)
        if ("t%d" % (li + 1)) in want: taps["t%d" % (li + 1)] = xt.copy()
        dil *= 2
    logits_r = _conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex_out = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        ex_out[ej] = nn_gelu_fwd(_conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)).reshape(T, d)
    y = nn_moe_router_fwd(logits_r, ex_out, T, E, d)
    if "moe" in want: taps["router"] = logits_r.copy(); taps["moe"] = y.copy()
    yn = nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    if "yn" in want: taps["yn"] = yn.copy()
    # readout: reuse the exact SLW/CLMB branch from _fwd_logits on yn → logits
    ...
    return taps, logits
```

Tap copies are negligible next to the GEMMs — **one forward yields every tap**. Storage discipline: dump pooled vectors + block-span rows only (~0.5 MB/doc fp16), never full `[T,d]` all-tap dumps (that's ~20 MB/doc). Use the anima_py package forward (SLW-aware — per the trailer-divergence memory, hexa ignores SLW; taps are pre-slot, base logits must include the slot).

## 4. Pre-registered decision tree (frozen now; no tune-to-green)

```
Gate-0  Δlit CI_lo>0 at tap (oracle lane)          FAIL → INVALID (harness fix; not an attempt)
S0-A    unshown-kw AUC, all taps
        ├─ all ≤ chance ..................... 🧱 TERMINAL-eligible (association absent read-side at all
        │                                       depths; py 2-prod = TERMINAL per a_eval_py_canonical)
        └─ some tap > chance → S0-B on that tap set
S0-B    oracle-pool + contrastive-Wo, n=132, run ONCE per arm
        ├─ all arms: CI_lo(Δzero−ΔshufV) ≤ 0 (lit alive) ... 🧱 family-terminal ACROSS read depths
        └─ any arm: CI_lo(Δzero)>0 ∧ CI_lo(Δzero−ΔshufV)>0
                     ∧ CI_lo(Δzero−Δcrossdoc)>0 ∧ lit alive ... CRACK → FULL Arm-S lane
FULL    same bars; BREAK = Δzero ≥ 0.10 nats/token
        CRACK sustained → 🟡 DIRECTIONAL → 🟢 only when wired live (a_verified_must_wire)
```

Escalations allowed (pre-registered, one each, train-side criteria only): λ_c→3.0 iff contrast top-1 >80% ∧ train swap-margin <0.02. Nothing else moves; eval fires once per arm.

**What a full null means (write it into the card now):** the Δzero−ΔshufV inertness is a property of the **frozen emit interface + missing consumable association**, not of the read location — "fork-A closed at yn" upgrades to **read-side augmentation closed at every depth of the network**. That is the strongest cheap justification for the only remaining exit: γ trained trunk-bind — which per the ledger is NOT a naive refire (H_1840 STEP-0 frozen-gate killed it; the documented reopen condition is exactly this 🧱 + a real-text target redesign, and this experiment's corpus/eval is the real-text target for it).

**Honest prior:** I put ~70–80% on 🧱. Evidence against a crack: identity already survives to YN pooled; lit copy already consumable at YN; trained contrastive found nothing at YN; residual stream ⇒ taps are correlated increments. The purchase is the terminal: this run converts a lane-scoped wall into a family-scoped one for the cost of a few CPU-pod hours, and S0-A alone may deliver that verdict for near-zero.

## 5. Cost (CPU-only, honest numbers)

| item | forwards | cost |
|---|---|---|
| S0-A: match docs (~300) + kw-isolation (~150 short) | ~450 | ~9 core-h → **~1 h wall** on one dedicated 32-core pod (4-way × 8 threads) |
| S0-B: swap/lit/crossdoc variants for train-Wo + n=132 eval | ~1,100–1,400 | ~25 core-h → **~3 h wall** same pod |
| Wo training / probes / bootstrap | — | minutes, laptop-class |
| FULL lane (only on crack) | reuse S0 dumps + per-position rows (~10–18 GB fp16) | GPU-free, hours |

So the "~1 hr budget" buys **S0-A completely** — and S0-A is the experiment most likely to be decisive. One job per host (dedicated-pod rule), OMP threads capped.

Execution notes for whoever fires it (I'm design-only): register as its **own H** with a fresh ledger before firing (pre-registered in `fable_swapcontrastive_result.md` §4 — don't inherit fork-A's), 2 surfaces (jsonl + card, suggested slug `H_92xx_g1_midstack_tap_association_floor`), hook lands as a read-only addition to `core/decode.py` + anima_py, verdict through the frozen `state/verdicts/` flow. Suggested state slug: `state/g1_midstack_tap/`.