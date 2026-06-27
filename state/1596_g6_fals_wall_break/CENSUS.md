# H_1596 — G6 IDEATION fals=0 wall-break census (6 orthogonal lenses)

**Subject:** h1129 = 303M ByteGPT, 24-layer GPT-2-class (ALREADY DEEP). Established TERMINAL fact
(H_1595, py 2-production engine, NOT artifact): G6 PASS iff `dist>=5 AND fals>=1`; h1129 measured
**dist=6 PASS, coherent=6 (distinct + coherent, NOT garble), fals=0 FAIL — seed-robust 0/3** across
seeds {7,4302,4303}. The wall is SPECIFICALLY the falsifiability sub-metric.

**fals detector** (`core/g6_ideation.py::_g6_is_falsifiable` L111; byte-parity twin
`core/g6_ideation.hexa`). An idea passes iff ALL of: (a) a COMPARATOR word (closed 25–26-word set)
AND (b) a MEASURABLE word (closed 25-word set) AND (c) >=2 content words AND (d) not ending in '?'
AND (e) first 3 words not all stance.

**Engine-native rule (a_engine_native_learning, HARD-GATE):** terminal evidence = the maintained
byte-parity py 2-production engine (`core/bytegpt_decode.py`, torch-free numpy, grep-clean of
`import torch|gauge_lib`) OR the wired hexa single-entry (`cli/anima.hexa eval` → `core/g_gates.hexa`).
Verified this campaign: `grep -lE 'import torch|gauge_lib' core/g6_ideation.py core/bytegpt_decode.py
core/g_gates.py` → EMPTY (grep-clean). Ad-hoc torch/numpy probe = DIRECTIONAL only. **This is a
research/census — NO terminal verdict is banked. Frozen bar UNTOUCHED (no tune-to-green, p7).**

---

## The convergent diagnosis (5 of 6 lenses point at the MEASURABLE word)

Five independent $0-local detector probes (L1, L3, L4, L5, L6) all isolate the SAME single missing
ingredient: on realistic coherent h1129-style continuations the **COMPARATOR word is frequently
present but the MEASURABLE word is ~0%**. The measurable lexicon is 25 words = 0.0107% of the
234,461-word dict — rare quantitative-scientific-register nouns (rate/number/ratio/threshold/
magnitude/frequency…) that a web/SNS-prose LM almost never free-associates. Rephrasing the same
ideas into quant-comparative register flips fals 0→1 with kwr (coherence) unchanged. So fals=0 is
**a register/surface-form gap, not a coherence or depth/capacity deficit** — exactly consistent with
h1129 already being dist=6 coherent=6 and 24-layer deep (depth-as-lever from clm303 L4 is N/A here).

The two candidate ROOT CAUSES for why the measurable word never appears:
- **DETECTOR vocabulary too narrow** (L1, class (a)): the closed whitelists drop common measurable
  nouns (memory/pressure/time/weight) and directional verbs (lowers/raises/reduces/exceeds) — so the
  model may ALREADY emit falsifiable-shaped claims that the detector silently rejects.
- **CORPUS register absent** (L2/L6, class (e)/(b)): CE only rewards the next byte of the training
  register; that register (≈99.7% ko-dominant chat/web/SNS) lacks measurable-claim vocabulary, so the
  measurable token-class has ~0 probability mass at decode.

These two are **not mutually exclusive** and L1 must run FIRST to partition the wall between them.

---

## Lens-by-lens census

### L1 — DETECTOR-VALIDITY (measurement-artifact) · class (a) · run-FIRST
- **Probe (RAN, $0-local):** dict=234461. Of 10 hand-written OBVIOUSLY-falsifiable human claims the
  live frozen `_g6_is_falsifiable` REJECTS 4 (40% false-reject). ALL 4 fail purely on the
  comparator/measurable whitelists, never on content/question/stance: "version B uses less memory
  than version A" (comparator {less,than} but 'memory' not in measurable set → FAIL b); "this engine
  runs slower when the cache is disabled" (FAIL b); "the model predicts rain whenever the pressure
  drops" ('pressure' absent → FAIL b); "aspirin lowers the frequency of heart attacks" (measurable
  {frequency} but 'lowers' not in comparator set → FAIL a).
- **Negative-control (RAN):** 5 non-falsifiable claims (stance/question/vacuous) → 5/5 REJECT. The
  detector is NOT vacuous; its rejections are meaningful.
- **Broadening ablation (RAN):** counterfactual broadened sets (+ measurable {memory,pressure,time,
  length,weight} + comparator {lowers,raises,reduces,improves,exceeds,drops}) admit 0/5 negatives —
  broadening is safe wrt the control (no false positives introduced).
- **Verdict:** the wall is PARTLY a detector-vocabulary artifact. Cheapest + highest-info first fire.
- cost: now-py-engine-summer (scorer-comparison on captured strings is now-$0-local) · predicted: lift · confidence: high

### L2 — CORPUS-REGISTER scarcity · class (e) under-investment/data
- **Probe (RAN, $0-local, grep-clean):** over h1129's own 4-cell corpus (state/clm303_clean_corpus),
  window=18 words (~110-byte gen arm), co-occurrence (comparator AND measurable) pass-rate:
  ko-gen 0.00% (0/679), en-gen 0.50% (52/10331), ko-sns 0.00% (0/1045), en-sns 0.41% (50/12090).
  EXACTLY 0.0% for BOTH Korean cells (Hangul high-byte; ASCII-only detector can NEVER fire on Korean).
  CONTROL claim-dense register: 100% window-pass (198 comp/kw + 158 meas/kw).
- **Propagation:** E[fals hits across 6 ideas] = 0.03 (en upper-bound) → 0.004 (ko-weighted) ⇒
  P(fals=0)=97.0–99.6%, MATCHING the measured 0/3 seed-robust. So fals=0 is the EXPECTED outcome of a
  register-starved corpus, not a capacity ceiling.
- **Test:** add a 5th tiny EN scientific/argumentative claim-register cell (~1-5MB), continue-train a
  few hundred steps, re-run terminal g_eval_g6_multiseed. Controls: (1) size-matched MORE-chat dose
  control; (2) NOT hand-stuffing the exact 25+25 detector tokens (Goodhart guard); (3) ko-cell control
  (Korean augment alone must NOT lift — ASCII detector floor).
- **Verdict:** the plausible TRUE ROOT CAUSE — but the most expensive (needs-train). Run AFTER L1
  partitions out the detector artifact.
- cost: toy-train (continue-train slice) · predicted: lift · confidence: medium

### L3 — FRAME-CONDITIONING (few-shot falsifiable exemplar) · class (b) wrong-direction/latent
- **Probe (RAN, $0-local):** decode returns continuation-only (`bytegpt_decode_topk_sampled_W` text =
  NEW bytes only) so the frame's own 'if' never counts. 6 realistic coherent continuations → fals=0/6
  (comparator 1/6, measurable 0/6, kwr 0.73–1.0); SAME 6 ideas rephrased quant-comparative → fals=6/6
  (kwr unchanged). All 6 composed frames are themselves fals=False (no frame leak in the frozen path).
- **Test:** prepend a 1-shot falsifiable exemplar to each composed frame (decode-only, NO weight
  change), keep g6_frame_guard on the ORIGINAL frames (exemplar trips the measurable-leak guard but
  never enters the scored continuation-only region; frozen bar untouched). Run multiseed {7,4302,4303}.
- **Controls:** (1) length-matched NEUTRAL non-falsifiable prefix — if NEUT lifts as much as EXEM the
  effect is mere priming/length, lens REFUTED; (2) shuffle exemplar words to destroy comparator→
  measurable structure while preserving lexicon — must NOT lift if structure is the lever.
- **Verdict:** if the exemplar lifts fals while the neutral prefix does not, the register is LATENT and
  frame-unlockable (wrong-direction wall, no train, no rent). Decode-side lift NOT yet run (needs summer).
- cost: now-py-engine-summer · predicted: lift · confidence: medium

### L4 — DECODE-BUDGET (gen-length × temperature) · class (a) measurement-harness
- **Probe (RAN, $0 coupon-collector):** gen is in BYTES; default gen=40B ≈ 7–8 English words.
  detector needs comparator∧measurable in that short window. With realistic prose rates pc=0.04,
  pm=0.006: E[fals over 6 frames] = 0.08 at 8w (≈0, matches observed), 0.50 at 24w, 1.03 at ~40w
  (~200B). Binding constraint at 8w is P(meas)≈0.05 ≪ P(comp)≈0.28 → the rare MEASURABLE word is the
  bottleneck; baseline budget simply truncates before it's sampled. temp=0.7 compresses the rare tail.
  multiseed varied ONLY the RNG seed at FIXED gen=40/temp=0.7 → it cannot distinguish capability-wall
  from budget-too-short — a genuinely untested axis.
- **Test:** gen ∈ {40,80,200}B × temp ∈ {0.7,1.0}, SAME frozen detector/frames/seeds. 108 decodes,
  CPU-feasible on summer, $0. Predict fals ≥1 at gen≥200 &/or temp=1.0; stays 0 at gen=40.
- **Controls:** coherence floor (dist≥5 AND coherent≥5/kwr≥0.5 must hold at longer gen — else "lift"
  is longer garble); vary gen at fixed temp (pure budget) vs temp at fixed gen (pure tail) separately;
  report which sub-requirement flips (predict measurable, not comparator).
- **Verdict:** cheap decode-side lever; if fals STILL 0 at gen=200/temp=1.0 with coherence held, the
  capability-wall verdict STRENGTHENS (valuable falsification).
- cost: now-py-engine-summer · predicted: lift · confidence: medium

### L5 — SAVANT / golden-zone disinhibition · class (d) ablation-INERT (predicted null)
- **Code census (RAN):** `grep -n 'savant|sv_inhibit|inhibit_domain'` over bytegpt_decode.py /
  g6_ideation.py / g_gates.py → EMPTY. Savant operator `sv_inhibit_domain` (engine_cli.py:9074) acts
  on a Φ-domain LATENT activation matrix and feeds ci_phi_iit4 / SI — architecturally DISJOINT from
  the G6 ideation text path (bytegpt_decode top_k=40 temp=0.7). Savant lifts Φ-EXPRESSION of a
  deterministic classifier (H_1560/1576/1564, all TOY-scope), not the bytewise logit distribution.
- **Probe (RAN, $0-local):** 4 coherent continuations → fals=0 with comp=1, meas=0 (kwr 0.91–1.00);
  the 1 synthetic claim with 'rate…higher than…threshold' → fals=1. Missing ingredient = MEASURABLE.
- **Test:** toy ByteGPT d256/4L savant-temperature ladder {0.3…1.3}, score with frozen g6_ideation.py.
  3-arm ablation: (A) savant-OFF baseline; (B) golden-zone-ON ladder; (C) DIRECT measurable-injection.
  Ψ=1/2 guard across the ladder (emit-disjoint lanes 0/4 untouched, H_1578).
- **Verdict:** PREDICTED null — savant is INERT for fals (disinhibition mostly raises garble, hurting
  dist/coherent long before landing a 1-in-9000 measurable token). Cheap ablation that, if null,
  cleanly REMOVES the capacity-expression family from the candidate set (a_break_the_wall: ablation
  isolates a non-contributor).
- cost: now-$0-local (toy) · predicted: null · confidence: high

### L6 — OBJECTIVE / AUX-SIGNAL (reranker vs register coverage) · class (b)/(e)
- **Probe (RAN, $0-local):** detector decomposition confirms fals=1 needs comparator∧measurable
  CO-OCCURRING in the continuation alone (frame 'if' does NOT leak; frame_guard=0). On fluent anima
  prose (86 words): comparator-hits 5.81%, measurable-hits **0.000%**. g6 concept-seeds: 0 measurable
  words across all 5. Reranker simulation (seeded, 6 frames): h1129-register (meas=0%) → fals=0/6 at
  k=1, k=8, k=40 (reranker INERT — cannot select a token the model never proposes); curriculum-register
  (meas=3%) → fals=3/6 at k=1, fals=6/6 at k=8/40 (register coverage flips PASS even without rerank).
- **Test:** ARM-1 baseline vs ARM-2 reranker-on (g6_decode_best_of_k, already wired) — predict fals
  stays ~0 (FALSIFIES "reranker alone breaks the wall"); positive arm = in-context register-prime
  (no retrain) — predict fals jumps.
- **Controls:** (1) REGISTER-PRIME control (prime, k=1, no rerank) — lift here ⇒ register is the lever,
  not selection; (2) RERANKER-on-fixed-register negative control — predicted delta 0 (decisive INERT
  ablation); (3) hold dist/coherent constant.
- **Verdict:** reranker is multiplicative WITH register, not a substitute; DATA-curriculum (= L2) is
  the primary p7-legal lever. The in-context register-prime arm is a no-retrain confirmation of L2/L3.
- cost: now-py-engine-summer (reranker INERT sim is now-$0-local) · predicted: lift (prime) / null (rerank-alone) · confidence: high

---

## RANKING (cheapest measurable lift first)

| rank | lens | cost | predicted | why this rank |
|---|---|---|---|---|
| **1 (CHAMPION)** | **L1 detector-validity** | $0-py-summer (scorer step $0-local) | lift | run-FIRST measurement-artifact check; decisively PARTITIONS the wall (artifact vs genuine) and gates the meaning of all 5 others; already shows 40% false-reject on true claims. |
| 2 | L4 decode-budget | $0-py-summer | lift | pure decode-side lever, no train/rent; coupon-collector predicts crossover at ~200B; multiseed never varied this axis. |
| 3 | L3 frame-conditioning | $0-py-summer | lift | decode-only 1-shot exemplar, no weight change; clean neutral-prefix control isolates register-content from priming. |
| 4 | L6 objective-aux | $0-py-summer | lift (prime) / null (rerank) | reranker-INERT prediction is $0-local-decisive; in-context register-prime arm is a no-retrain L2 confirmation. |
| 5 | L5 savant-disinhibition | $0-local (toy) | null | cheapest absolute, but predicted INERT; valuable as the ablation that removes the capacity-expression family. |
| 6 | L2 corpus-register | toy-train | lift | the plausible TRUE root cause, but most expensive (needs continue-train); run AFTER L1/L3/L4 partition the cheap explanations. |

## CHAMPION — fire L1 FIRST
**L1 (detector-validity).** It is the run-FIRST measurement-artifact check and is the cheapest test
that yields the highest information: the decode of ~30 h1129 ideas (summer py-engine) plus a $0-local
two-scorer comparison (live frozen `_g6_is_falsifiable` vs human-tag) decides whether h1129 ALREADY
emits falsifiable-shaped claims that the closed vocabulary drops. The broadening ablation (verified
this turn to admit 0/5 negatives) then isolates vocabulary-from-logic without moving the frozen bar.
Outcome partitions the wall: if human-tagged-fals >> detector-fals → class (a) artifact; if both ~0 →
the wall is genuine register/data (hand off to L3/L4 cheap levers, then L2 train).

## WALL CLASSIFICATION (post-census)
**Mixed, primarily class (a) measurement-artifact compounded by class (e) data-register
under-investment — NOT class (d) true-ceiling.** L1 shows the detector false-rejects 40% of genuine
human claims on its closed comparator/measurable whitelists (a). L2/L6 show the corpus comparator∧
measurable co-occurrence rate is ~0.5% en / 0.0% ko and the measurable token-class has ~0 decode mass
(e). L3 shows the same ideas flip fals 0→1 with kwr unchanged under quant-comparative rephrasing
(b: wrong-direction/latent register). L5 ablation predicts the savant capacity-expression family is
INERT, ruling OUT (d). The fals=0 wall is therefore reopenable by cheap decode-side levers (L3/L4)
and a detector-validity fix (L1) before any train-side data augment (L2) — depth/capacity is NOT the
ceiling (h1129 is already 24-layer deep, dist=6 coherent=6).

**Frozen bar untouched** (`dist>=5 AND fals>=1`, 7B_PASS_CONDITIONS.md). NO tune-to-green. This is a
research/census; no terminal verdict banked. Engine-native scorer closure verified grep-clean.
