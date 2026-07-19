**Fire it — Step 2 is a genuine discriminator, not a foregone escalation.** Your Step-1 pattern (lit huge and λ-scaling, zero dead, shuffle-killed) is exactly what a *surface-dominated yn geometry under a fixed dot-product metric* predicts — and a learned Q/K re-metric is the canonical fix for that specific failure mode. Critically, the mechanism does not require the trunk to transport concept identity across the gap (the established G1 deficit): the lane's attention IS the transport, and the keys sit at concept-line positions where local encoding is near-certain. The open question is only whether a learned projection can read concept identity out of those states and whether the query side encodes "what to fetch." I put the crack prior around 40% — and the kill branch is equally valuable, because with the train-side gate below (T2) a kill becomes the clean terminal cement for the frozen-readout class. Both outcomes pay; the fire is $0. So no terminal argument now — the terminal argument *requires* this experiment's T2 bit.

---

## 1. Lane forward — exact ops

Shapes: `d=3784`, `V=256`, `dh=dv=256` (≥ concept-count headroom, small enough that ~12k docs constrain it; total ~3M params).

```
yn: [T, d]  frozen trunk states (upcast to fp32; lane is fp32 throughout)

Q  = yn @ Wq                    # [T, 256]
K  = yn @ Wk                    # [T, 256]
Vv = yn @ Wv                    # [T, 256]

# eligibility: position t attends i ∈ [0, t−64)   — strictly causal AND a 64-byte
# exclusion window. Excluding t kills the self-read bypass; excluding the last 64
# bytes kills any local-n-gram/smoothing use of the lane entirely. Retrieval targets
# are ≥128 bytes back by construction, so nothing legitimate is lost.
score_ti = (Q_t · K_i) / sqrt(256)          # fixed scaling; NO learnable temperature
A_t      = softmax over eligible i          # if no eligible keys (t < 65): bias_t = 0
ctx_t    = Σ_i A_ti · Vv_i                  # [256]

# gate: sees ONLY the attention distribution, never yn_t (pre-registered exclusion, §2)
H_t = −Σ_i A_ti log A_ti
g_t = sigmoid( a · (log N_t − H_t) / log N_t + b )   # N_t = #eligible keys
                                                     # a, b learnable scalars; init a=1.0, b=−2.0

bias_t   = g_t · τ · tanh( (ctx_t @ Wo) / τ )        # Wo: [256, V]; τ = 8.0 FIXED
logits_t = base_logits_t + bias_t
```

Use the soft `τ·tanh(·/τ)` bound **identically in train and eval** — a hard clip zeroes gradients outside the band and creates train/eval inconsistency. `τ=8` is enough to make a near-zero byte dominant (retrieval needs that) while forbidding unbounded logit surgery.

**Init — resolving the "tie to trunk unembed" question:** don't tie. That advice was for the *non-learned* Step-1 cache, where the value path had to be right at init. For a trained lane, **zero-init `Wo`** strictly dominates: the lane is an exact no-op at step 0 (LoRA-style), no basis mismatch with the conv readout to worry about. `Wq, Wk, Wv ~ N(0, 0.02)`. Only if training stalls (T1 fails after the one lr retry): warm-start via the conv center tap — take `U = roWt[:, :, k//2]` reshaped to `[V, d]`, SVD `U = A·S·Bᵀ`, set `Wv = B[:, :256]·√S`, `Wo = (√S·A[:, :256]ᵀ)`, then force silence at init through the gate (`b = −6`). Don't reach for this first.

## 2. Training

**States.** If you have the torch trunk mirror, run it on-the-fly under `no_grad` fp16 (303M forward for 32×~450-byte docs is sub-second on the 5070); otherwise precompute `yn` + `base_logits` fp16 memmap from the production decode. Either way, **verify state parity once** (max|Δyn| on a probe doc between your training-state source and the production `clm_forward_hidden_logits`) — forward byte-innocence is established, but the lane must transfer to production states at eval, so check it before burning epochs.

**Corpus builder deltas** (keep your 70/30 mix and structure):
1. **Target span = a full keyword, multi-byte — yes, you need this.** A single post-stem byte is dominated by UTF-8 first-byte priors (Korean keyword first bytes cluster in 0xEA–0xEC, English in a–z): the lane gets a cheap unigram shortcut that improves train CE with zero retrieval. Loss masks the whole keyword's byte span.
2. **Show 5 of 8 keywords** in the concept line. Retrieval trial (70%): target = one of the 5 *shown* keywords → copy-across-gap curriculum (teaches WHERE to attend; the span legitimately appears, but only in the pre-gap line, ≥128 bytes back). Associative trial (30%): target = one of the 3 *unshown* keywords → **anti-copy by construction: assert the target span appears nowhere in the doc as a substring.**
3. **Stem must be concept-neutral**: assert no ≥3-byte n-gram of any of the concept's keywords appears in the stem. ~10 stem templates ("다음으로 떠오르는 것은 " / "the next thing that comes to mind is ", etc.).
4. Gap jitter 128–512 bytes; ko + en both (keeps the V3 4-cell fairness gate satisfiable at eval).
5. **Concept split 40 train / 8 lane-val** (concept-level, inside the 48 — never touching the 12 eval concepts). ~300 docs/concept train (≈12k), ~100/concept val.

**Loss.** Apply the lane at all positions `t ≥ gap_start`. Then:

```
L = Σ_{t ∈ target span} CE(logits_t, byte_t)
  + 0.1 · mean_{t ∈ S} KL( softmax(logits_t) ‖ softmax(base_logits_t) )
```

where `S` = 8 randomly sampled non-span positions ≥ gap_start per doc. The KL-silence term is load-bearing: at eval the lane fires at *every* continuation position, and without a trained silence prior it emits garbage bias at irrelevant positions and noise-swamps Δ.

**The gate-smoothing backdoor — three layers of defense:** (i) `g` takes only attention entropy, **never `yn_t`** — it cannot implement "trunk is uncertain → smooth"; it can only implement "attention is peaked → trust retrieval," which is the honest confidence signal. (ii) The KL-silence term makes indiscriminate bias expensive. (iii) Structurally, any content-independent smoothing that leaks through survives the V-permute shuffle at eval and is therefore killed by the `Δ_zero − Δ_shufV` bar — the eval control is the real backstop; the gate restriction just removes the cheapest implementation.

**Optimizer.** AdamW, lr 3e-4 cosine→3e-5, warmup 200 steps, wd 0.01 on matrices (none on `a, b`), batch 32 docs, grad-clip 1.0, ≤20 epochs, eval on lane-val every 500 steps, early-stop patience 3.

**Pre-registered train-side gates (before firing the swap harness):**
- **T1 (optimization sanity):** train-set associative-span CE improves ≥0.3 nats vs base. Fail → one lr retry (1e-4), then INVALID/debug. Not a result.
- **T2 (concept-general circuit — the load-bearing bit):** lane-val (8 held-out concepts) associative CE improves vs base, bootstrap CI > 0. Retrieval trials should improve massively regardless (that's the train-side lit-analog).

## 3. Eval application

Same swap-margin harness. At each continuation position `t`: `Q` from `yn_t` computed on the full `context ⊕ continuation[:t]` production forward; K/V over all `i ∈ [0, t−64)` (context and earlier continuation). Export lane weights to `.npz`; the lane forward is ~20 lines of numpy inside the harness on top of production decode (a_eval_py_canonical). Verify torch↔numpy lane parity (max|Δbias| < 1e-4 on one doc) before the run. Heavy decode on pool, not mini.

**n = 192, not 48 — this is mandatory, not optional.** From your Step-1 numbers: CI half-width ±0.056 at n=48 ⇒ per-pair sd(m_on−m_off) ≈ 0.196. At n=48 the 2σ-detectable effect is ≈ ±0.056 — **n=48 structurally cannot resolve a true effect of the +0.033 scale**, so a null at n=48 wouldn't cement anything. n=192 gives SE ≈ 0.014, resolving ≈ ±0.028. Fixed seed, pre-registered.

**Controls:**
1. off-baseline (lane bypassed), same as Step-1.
2. **Δ_zero** — primary.
3. **Pairing-shuffle for a learned lane = V-row derangement, NOT K-permute.** Keep K rows intact (attention pattern and entropy gate unchanged), apply a fixed-seed random derangement to the V rows among eligible positions. This isolates "does the *content delivered* matter." K-permute is the wrong control here: it scrambles the attention distribution → entropy rises → the gate closes → Δ trivially ≈ 0, telling you nothing.
4. cross-doc — keep (expect negative or ~0; context-specificity).
5. **lit positive control — gate, not just report:** `CI_lo(Δ_lit) > 0` required. If lit dies, the verdict is **INVALID** (plumbing/parity bug), never FAIL. Magnitude needn't match Step-1 (the 64-byte exclusion window may shave it).
6. Optional diagnostic, reported once: gate frozen at g=1.

## 4. Pre-registered crack / kill / terminal

- **CRACK:** `CI_lo(Δ_zero) > 0` (BCa bootstrap, 10k resamples) **AND** `CI_lo(Δ_zero − Δ_shufV) > 0` (paired, same resamples) **AND** lit gate alive.
- **BREAK (wire-candidate):** CRACK **and** point estimate `Δ_zero ≥ +0.10` — roughly the off-baseline `m_lit` scale. A statistically-real +0.03 is a nudge, not a wall-break (a_scale_honest_scope); it would earn 🟡 DIRECTIONAL, not a lane.
- **KILL:** anything else. Decision tree on KILL:
  - **T2 had failed** (train fit fine, held-out-concept val flat) → **terminal, no step-3.** The trained readout is the upper bound of the class; if it can't form a concept-general circuit even *in-distribution on synthetic data*, no fixed-kernel variant can. Cement: frozen-**final**-state readout augmentation = 🧱.
  - **T2 passed but eval killed** → exactly one pre-registered step-3, *corpus realism only*: mine natural-text distant-recurrence spans (rare content word recurring ≥256 bytes later in real corpus), retrain the **same** lane, same eval, zero other knobs. If that kills → terminal. No hyperparameter re-rolls, no architecture variants.
- **Scope honesty on the terminal cement:** `clm_forward_hidden_logits` exposes the *final* hidden state only. Probing literature says topic/concept identity often peaks mid-stack and gets projected out by output-oriented final layers. So the cement, strictly worded, covers the **final-state readout class**. If a mid-stack tap is cheaply exposable from the decode path, run the identical lane once from that tap inside the same campaign (same bars) and the cement covers the full frozen-readout class; if not, write the verdict scoped to final-state with mid-stack named as the residual — noted, not blocking.

One asymmetry worth having in view while you code: the retrieval trials (shown keyword) can be solved by a learned pointer-walk — and your lit control already proves pointer-walking is expressible in this space — so expect those to go green fast. The entire hypothesis lives in the associative trials and in T2. If you watch one curve during training, watch lane-val associative CE: it is the earliest honest readout of whether the wall cracks, days before the swap harness runs.
