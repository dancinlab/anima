# H_001 design — verbatim Fable 5 output (seed of record, not the SSOT)

- job: fable-mrmhpft7 · model: claude-fable-5 · date: 2026-07-16
- brief: pick ONE family + design its minimal falsification (D1-D7)
- distilled into: ARCHITECTURE.json + HYPOTHESES/cards/H_001*.md

---

# H_001 design — anima-v3 first pre-registered falsification card

## D1 — Which family: F1 alone. The composed F1+F3 bet is confounded — split it.

**The composed card is confounded twice over, so it is disqualified as a first card regardless of its merits as a campaign bet.**
1. Classic confound: two levers (adaptive codec, diary bottleneck) move at once. A null cannot say which failed; a win cannot assign credit. You would have to run the factorial (fixed/adaptive × diary/no-diary = 4 arms) to un-confound it, which is two cards' cost pretending to be one.
2. A structural interaction the divergence text glosses over: F3's diary `m` lives in **token space**. If F1's codec refits mid-training, the diary's alphabet changes under it — the diary-swap control and the scramble floor both become non-stationary, and every F3 metric inherits F1's L6 comparability trap squared. Composing them isn't just confounded, it needs machinery neither family's solo card needs. The campaign bet stays "F1 substrate + F3 objective," but it must be bought as two sequential cards: F1 mechanism first, then F3 on whatever codec regime survives.

**F1 vs F3 as the solo first card — F1 wins on both halves of the belief-per-dollar criterion:**

*Belief killed if FALSIFIED.* A null on F1's twin (adaptive refit buys nothing over a frozen codec, net of swap cost) kills: (a) F1 itself; (b) F6's entire variation axis — "reproduce = distill winner + **mutate the codec**" presupposes codec change is a live lever; (c) it bounds L4(b), the campaign's *only* green causal measurement, from "the codec is architecture" down to "one-time static codec choice matters" — which guts `thesis.claim`'s strongest evidence and leaves F4 as the write-lever axis's sole survivor. That is roughly half the campaign's prior mass, dead, for ~$25 (D2). A null on F3's cheap rig kills much less, because it isn't attributable (next point).

*Attributability of a null.* F1 has an existence proof of detectability at small scale: MORPH-ATOM measured the codec→recombination effect green (+0.291) at synthetic-drill scale. A drill-scale F1 null is therefore attributable to the *mechanism* (refit-during-training), not to under-scale — the static half of the effect is already known to show up at this scale. F3 has no such anchor: a cheap F3 null is ambiguous between "diary carries no load" and "this corpus has no cross-day mutual information for the diary to carry" — and the literature pass (D3) shows the generic mechanism question ("do forced bottleneck summaries carry load?") is *already answered yes* (gisting/AutoCompressors), so F3's cheap card buys information the field already has, while its campaign-specific question (self-history → own-future prediction as identity) needs a temporally structured stream, i.e. weeks of wall-clock. F3 is the right *second* card, not the first.

*Axis audit.* This card buys information on the **write-lever axis (F1/F4)** — the right axis to buy first because (a) it is the only axis with measured green causality, hence the only one where a cheap rig has known power; (b) two other axes lean on it (F6 structurally, F4 as the same lever's data-hand — one verdict informs both); (c) the prediction-error-action axis's cheap questions are literature-answered and its campaign questions are wall-clock-bound (F7 weeks, F5 four weeks by construction — note F5's latency is calendar, not compute, so it can be *started* cheaply later without competing for this slot).

## D2 — The smallest rig that can still kill the claim

The "~300M LM, 1 GPU, days" figure is the rig for the *identity* claim (idiolect on a natural experience stream). The *mechanism* claim — "a codec refit to the drifted experience distribution, trained through, beats a frozen codec on held-out recombination, net of swap cost" — is killable at MORPH-ATOM scale, because that is exactly the scale where the codec→recombination causal link was measured to exist:

- **Model:** twins of ~10M params (6 layers, d256, 8 heads), vocab 4–8k. 3 arms (frozen / adaptive-refit / scramble-refit control) × 3 seeds, +2 extra frozen seeds for the null-spread estimate = **11 runs**.
- **Corpus:** synthetic agglutinative "jamo-drill" language — ~512 stems × ~64 affixes (including a *bound* negation-style suffix per L5), jamo-decomposable; **drift schedule**: phase 2 rotates in a new affix inventory and shifts collocation statistics. Generator parameters frozen in H_001 before any training exists.
- **Budget:** **matched byte budget** (~300M bytes/arm; token counts float and are logged — matching tokens instead of bytes would hand the higher-compression codec free data, a silent confound).
- **Compute:** ≈6·10M·85M ≈ 5×10¹⁵ FLOPs/run → minutes per run on one rented GPU, ~1–1.5 h per run on this Mac mini's MPS `?` (settle by timing one warm-up run). **Wall-clock ≤2 days including analysis; cost $0 local / ≤$25 rented.** GPU-*hours*, not GPU-days.

**The killer question, answered honestly:** at this scale a null **is attributable to the hypothesis**, on three conditions that H_001 (D3) exists to secure: the stream demonstrably drifts the codec (else no lever moved), the drill has closed-form power for the pre-registered effect size (else underpowered), and the estimators pass known-effect fixtures (else the tool is blind — L6's positive-control lesson). With those secured, a null kills the mechanism, and mechanism is *necessary* for the family — **pre-commit now, in the card: a drill-scale null = F1 family-dead; "maybe it emerges at 300M" is not an appeal the campaign will entertain.** What a drill-scale *win* does NOT establish: the identity claim. That still costs the full 300M/natural-stream rig later (~$300–1000 `?`), and this design does not pretend otherwise.

## D3 — Research-before-real-measurement, applied

Literature pass (done, 2026-07): the exact twin — *from-scratch continual training through periodic codec refits on a drifting stream vs frozen codec, matched byte budget, held-out compositional recombination* — **has not been run**. Adjacent results, and what each contributes:

- Vocabulary/tokenizer adaptation for domain shift ([AdaptBPE](https://arxiv.org/abs/2410.03258), [Teaching Old Tokenizers New Words](https://arxiv.org/abs/2512.03989), [tokenizer optimization for pre-training](https://arxiv.org/html/2402.01035v2)): refit-to-domain reliably helps *downstream/compression* — raises F1's prior, but all measure one-shot adapt-then-finetune, never a continual refit organ, and none measures recombination.
- [ZeTT](https://arxiv.org/abs/2405.07883): codec swap on a trained LM costs ~1–3% with hypernetwork embeddings — swap cost is survivable, bounding F1's main failure mode from above `?` (at 7B scale; the 10M-scale swap cost is unmeasured — our rig measures it, F-6 below).
- [Byte Latent Transformer](https://arxiv.org/abs/2412.09871): learned dynamic patching beats BPE at scale — boundary-learning is beneficial, but per-input/inference-time, not experience-accumulated with persistence; doesn't answer F1.
- Gist/compression bottlenecks ([comprehensive study](https://arxiv.org/abs/2412.17483)): bottleneck tokens carry load **but show steep singular-value decay — near-rank-1 redundancy**. Two consequences: F3's generic mechanism question is pre-answered (part of why F3 isn't first), and L1-style rank collapse is documented *even on the write side* — the L1 gate below is not paranoia.

**Recommendation: H_001 = the deterministic gating/power card, and H_002 (the twin run) pre-registered immediately behind it, its thresholds frozen from H_001's outputs.** This is not timidity: H_001 is $0, fits `tool/anima_v3.py`'s stdlib/deterministic discipline exactly, is mandated by the campaign's research-before-measurement rule, and is what makes H_002's null attributable (D2). It has real teeth of its own — G-4 below can retroactively indict salvage L4(b). One discipline note (L8-aware): H_002 will be seeded-GPU, not stdlib-deterministic — extend the card rules *explicitly* (fixed seeds, logged env, verbatim stdout still binding) rather than letting the first real card silently violate `deterministic: true` and start the --no-verify death spiral again.

## D4 — The two inherited gates, made operational for F1

**L1 — seam and effective rank.** The mechanism's seam is the **refit channel**: what actually changes when experience rewrites the codec. Tensor: the boundary-delta matrix **B ∈ {0,1}^(N_p × L)** — for each of N_p frozen probe strings (byte-aligned, so codec-independent dimensions), the per-byte-position indicator of "token boundary changed between codec_t and codec_(t+1)". Estimator: **participation ratio PR = (Σσᵢ²)²/Σσᵢ⁴** of the singular values of mean-centered B. Derivation of thresholds: an exact rank-1 B (all boundary changes generated by one merge-rule family — the F1 analogue of v1's gate learning "one bit: itself") has PR = 1 exactly; **hard floor PR ≥ 2.0** = "at least two orthogonal change-directions with comparable energy," the minimum that is *strictly more* than v1's death mode; noise inflates PR above 1 even for rank-1 truth, so the binding threshold is **PR > null₉₉**, the 99th percentile of PR under a single-pattern-drift null (one merge family + observed marginal noise), B=1000 draws with a fixed documented seed. Gate: **PR ≤ max(2.0, null₉₉) → the refit channel is rank-1 → F1 dead by L1-recurrence, regardless of any metric win.**

**L2 — ablation.** Honest structural point: you cannot ablate a codec out of a trained model the way you drop a conditioning vector — the vocabulary *is* the input space. For F1 the channel ablation is therefore **between-arm by construction**: frozen twin = channel absent, adaptive twin = channel present. Quantity: **Δbpb = bpb_frozen − bpb_adaptive on the post-drift frozen byte probes**. Threshold, derived not vibed: **θ_L2 = max(5·σ_seed, 0.004 bpb)** where σ_seed = std of post-drift bpb across the 5 frozen-arm seeds (pure null calibration, measured and *frozen in code before any adaptive arm runs* — L6's frozen-truth-table rule), and 0.004 bpb = 10× the OMEGA decoration floor converted to this rig's units (0.0009 nats/token ≈ 0.0013 bits/token ÷ ~3.5 bytes/token ≈ 0.0004 bpb; one order of magnitude above the measured signature of "decoration"). Gate: **Δbpb < θ_L2 → the refit channel is load-free decoration → dead**, exactly the measurement whose absence let OMEGA live six months too long.

## D5 — Pre-registered falsifiers

**H_001 (gating card, deterministic, $0) — verdict = "rig licensed / rig refused":**
- **G-1 drift existence:** refit BPE-jamo on phase-1 vs phase-2 generator output; if boundary-shift rate on frozen probes < 5% of positions `?` (calibrate against MORPH-ATOM's jamo-vs-BPE segmentation distance if recoverable), the stream can't move the lever → refuse rig.
- **G-2 closed-form power:** two-proportion test at α=0.01, power 0.99, effect δ=+0.15 (half of MORPH-ATOM's +0.291 — it was 1 seed; halving is the hedge) around p≈0.62/0.77 → **N ≥ ~400 drill items per eval set**. If the generator can't emit 400 *non-overlapping* held-out recombination items → refuse rig.
- **G-3 estimator fixtures (positive control):** PR estimator must return 1±0.1 on a constructed rank-1 B and k±20% on rank-k fixtures; bpb accounting must reproduce a closed-form reference to 1e-9. Fails → tool is blind (L6's disambiguation lesson) → nothing downstream is interpretable.
- **G-4 salvage bounds check:** compute the closed-form chance band (binomial) for the drill format; **if MORPH-ATOM's control score 0.617 sits inside the 99% chance band, L4(b) itself was never above floor** — a campaign-level finding that would demote the whole write-lever axis. (This is the gating card's own kill-power.)
- **G-5 protocol reconstruction:** the "H_9288 held-out recombination protocol" is cited in the SSOT but **specified nowhere in this repo** (v1 is discarded; `state/` has only the divergence seed). The metric must be restated in full in the card; if it cannot be reconstructed unambiguously → refuse rig rather than eyeball it.

**H_002 (twin run) — SUPPORTED only if none trigger:**
- **F-1 main kill:** median-over-seeds recombination F-score, adaptive − frozen, on the post-drift held-out set < δ_min = +0.15 → mechanism dead.
- **F-2 = L1 gate** (PR ≤ max(2.0, null₉₉), D4).
- **F-3 = L2 gate** (Δbpb < θ_L2, D4).
- **F-4 negative control — scramble-refit arm:** identical refit schedule, but the codec is refit on a **permuted** stream (drift decoupled from content). If scramble-refit matches the adaptive arm within θ_L2 / δ_min, the "win" is generic segmentation-perturbation regularization (BPE-dropout effect), not experience alignment → dead.
- **F-5 bounds check:** every arm's bpb on the pre-drift frozen probes must land inside [closed-form entropy rate of the synthetic generator, closed-form unigram-model bpb]. Any arm outside → run invalid (not "F1 falsified" — rig-invalid, distinct verdict).
- **F-6 swap-cost bound:** adaptive arm's *retention* loss on pre-drift probes > its post-drift gain (both in bpb) → the organ is net-negative → dead.
- **F-7 leak audit:** n-gram overlap between held-out drill items and any training phase > pre-registered ceiling (0 for the composed stem×affix pairs) → run invalid (the L6 CA-lookahead precedent).

**The L6 measurement trap, handled:** all cross-arm numbers are **bits-per-byte** — Σ(−log₂ p(token)) ÷ raw byte count of the probe — so the denominator never moves when the codec does; probes are **frozen byte strings** (generated, hashed, and committed before any training run; hash in the card); byte budget matched, token counts logged. The named held-out metric: **post-drift held-out recombination F-score on ≥400 never-co-occurring stem×affix items (reconstructed H_9288 protocol), with post-drift frozen-probe bpb as the L2 load measure.** Per p7, no bpb number is ever the *verdict* — bpb serves only the L2/decoration gate; the verdict metric is recombination.

## D6 — Honest limits

1. **Synthetic ≠ experience.** A drill win establishes mechanism, not "idiolect = identity." The identity claim remains unbought until the 300M natural-stream rig; this card only decides whether that rig deserves to exist.
2. **The power calc is anchored on the weakest green in salvage.** MORPH-ATOM is 1 seed, synthetic; if +0.291 was luck, δ_min = 0.15 is miscalibrated. Hedges: halved effect size, 3 seeds/arm, and G-4 can catch the worst case (control-at-floor).
3. **Scale transfer is unknown in both directions.** Swap cost at 10M (embedding mass fraction ≫ 300M's) may overstate F-6; codec effects could also shrink with scale. The pre-commitment (drill null = family dead) is a campaign *choice*, stated now so it can't be relitigated after results.
4. **Designer degrees of freedom in the drift schedule.** The generator is built by the same party that wants F1 to live; freezing generator params in H_001 before training bounds but does not eliminate this.
5. **σ_seed from 5 seeds is a rough null-spread estimate** (~±35% error on σ itself); θ_L2's 5× multiplier absorbs some of this, and the 0.004 bpb absolute floor backstops it.
6. Representative-not-measured numbers in this document: MPS wall-clock, boundary-shift-rate floor (5%), bytes/token (3.5) — all marked `?`, all settled by H_001 or the warm-up run, none load-bearing for the verdict logic.

## D7 — How this card self-deceives

**The single most likely SUPPORTED-but-wrong path:** the adaptive arm wins F-1 not because experience-aligned boundaries expose compositional structure, but because *any* periodic codec perturbation regularizes segmentation (the BPE-dropout effect) — "refit-as-noise" wearing "refit-as-self" as a costume. It survives F-1, F-2 (perturbation noise inflates PR past the threshold for free), and F-3 (regularization moves real bpb). **The one measurement that catches it is the scramble-refit arm (F-4)** — which is also the arm most tempting to cut, since it's 33% of compute and "only a control." It is therefore non-negotiable in the pre-registration: a two-arm version of H_002 is not a smaller version of this card, it is a different and self-deceiving card. Secondary trap, named for completeness: a construction leak where post-drift drill items are reachable from training collocations (the L6 lookahead precedent) — caught by F-7's zero-overlap audit.

---

**Bottom line:** split the composed bet; F1 alone, write-lever axis first. H_001 = the deterministic gating card above ($0, fits `tool/` as-is, teeth of its own via G-4); H_002 = the 11-run twin at 10M/synthetic — GPU-hours and ≤$25, *not* GPU-days — pre-registered behind it with thresholds frozen from H_001's outputs, and a drill-scale null pre-committed as family-death. No repo files written; the card contents above are ready to be transcribed into `HYPOTHESES/cards/H_001*.md` + `REGISTRY.jsonl`.

Sources: [AdaptBPE](https://arxiv.org/abs/2410.03258) · [Teaching Old Tokenizers New Words](https://arxiv.org/abs/2512.03989) · [Getting the most out of your tokenizer](https://arxiv.org/html/2402.01035v2) · [Zero-Shot Tokenizer Transfer](https://arxiv.org/abs/2405.07883) · [Byte Latent Transformer](https://arxiv.org/abs/2412.09871) · [Gist-token compression study](https://arxiv.org/abs/2412.17483)
