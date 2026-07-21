# TASK: design the ONE-VARIABLE fixed-codec drill (no adversary) — pre-register spec only

You are designing an experiment for the `anima-v4` campaign. Output a **precise, buildable spec**,
not prose. I will implement it directly from your output. Be brutally concrete. No encouragement.

## What already happened (all measured, all $0, do not re-derive)

The campaign's "bet" was **mech-3 codec-war**: A = an LM over a segmentation; G = an adversarial
codec that learns its own merge table against A's loss. It is now dead three times over:

1. **H_001 🟢** — its pre-registered falsifier ("substitute a fixed BPE for G → ΔF2 < 0.1 ⇒ DEAD")
   is VACUOUS. The fixed codec it ablates to *is* v1's arm M, which scores `d_acc` 0.9083/0.9167.
   `d_acc` is a 2-way forced-choice accuracy bounded at 1.0, so max attainable Δ = 0.0833–0.0917
   < 0.1. It returns DEAD for every possible mechanism.
2. **Literature gate** — its objective is TAUTOLOGICAL. MDL's two-part code is
   `L(model) + L(data|model)`, and `L(data|model) = −log P(data|model)` = cross-entropy. So
   "A's future CE + code length (MDL)" is ONE term written twice. No term represents composition.
   Its argmin is a frequency segmenter = the static control it was built to beat (de Marcken
   cmp-lg/9512002, Brent cs/9905007, Creutz & Lagus cs/0205057 Morfessor). Empirically end-to-end
   learned boundaries lose to static Unigram 6/6 (Nawrot 2211.09761) and BLT (2412.09871) uses a
   frozen byte-LM with zero gradient.
3. **H_002 🟢** — L5's premise ("KO `지 않다` is a BOUND suffix, so composition is invisible at the
   token boundary and cannot be learned") is not in the measurement. Split v1's already-computed
   per-item margins by form: the no-codec arm (raw utf-8) shows free−bound margin gap +0.06/−0.06
   nats (no bound penalty); the codec arms lean the OTHER way (−1.11/−0.81, i.e. MORE confident on
   bound). And `지 않다` outnumbers `안` **5.73:1** in the drill's own corpus.

**What survives**: L4b is real and replicated at 2 seeds — a fixed jamo-BPE codec gave `d_acc`
0.9083/0.9167 vs a NO-CODEC (raw utf-8) control at 0.6167/0.5750 on held-out negation
recombination. The surviving explanation is **ATOMICITY of the negator token** — not identity
(C3: collapsing all 4 negators to ONE shared id scores the same, 0.9167), not pretraining exposure
(C2: scrubbing the held-out stem from pretraining entirely scores the same, 0.9167), and NOT
boundary visibility (H_002 just killed that).

## The v1 drill, verbatim (this is what you are modifying)

- **Task**: seed = `이 영화 <surface> => `, model emits `긍정.` or `부정.`. Gold bit =
  `pol(predicate) XOR flip(negation-form)`.
- **Metric `d_acc`**: forced choice — correct iff `NLL(seed+gold) < NLL(seed+counterfactual)`.
  Scored from the FIRST BYTE where gold and cf diverge (긍정./부정. share the `정.` suffix — a
  fixed-length tail scores identical text and yields margins==0 exactly). Left context filled with
  REAL bytes from the training stream (isolated lines are OOD → NLL above uniform).
- **Held out**: a whole STEM. `HELD = 아니`; `DRILLED = 안/않/못`. 아니 appears 0 times in the drill
  grid. Panels: `eval_f1` (drilled sanity, n=100, 60 bound / 40 free), `eval_f2` (held-out stem
  아니, novel conjugations, n=120, **100% bound** — no free/bound contrast exists in it).
- **Codec**: jamo decomposition (distinct cho/jung/jong markers) → frequency BPE over jamo symbols,
  within-eojeol only, K from a ladder {2048,4096,8192,16384}, min pair count 5 → fixed-width 2-byte
  re-encoding. K=2048 chosen as smallest passing a **G-0 audit**: round-trip ≥0.98 + the 4 stems
  pairwise token-DISJOINT. The source comments the contingency: "If 아니 (shares ㅇㅏㄴ prefix with
  안/않) can't fuse even at K=16384 → switch primary held-out to 못". **Atomicity was searched for
  and got lucky, not targeted.**
- **Model**: `CLMConvMoE`, d=3784, L=4, V=256 byte, ~388M params. Base ckpt EXISTS locally:
  `~/anima-weights/clm303_clean/clm303_clean.pt` (1.6G). For codec arms the embed+readout MUST be
  reinit (warm-starting a utf-8 embedding on a re-encoded alphabet is worse than random — it caused
  a false negative that survived two rounds of analysis). CPT 16k steps → drill 2.5k steps.
- **Corpus**: NSMC ratings_train (150k lines), cached at `~/g1_natem/nsmc_ratings_train.txt`.

## Local compute reality

MacBook, 10 cores, 16GB RAM, swap already 4.6G, torch 2.13 + MPS. A 388M ConvMoE at seq_len 1024
for 16k+2.5k steps × several arms is NOT going to fit this box. Assume I must either (a) shrink the
model drastically, or (b) rent GPU via `hexa cloud`. Tell me which, and what the smallest
scientifically valid configuration is.

## YOUR TASK — design the drill, and answer these exactly

### 1. THE ONE-VARIABLE CONTRAST
The claim to test is atomicity: **does giving the negator its own atomic token cause held-out
negation recombination?** Design the minimal arm pair that isolates EXACTLY that, holding the
alphabet, corpus, model, steps, and seed fixed. The v1 M-vs-C1 comparison is NOT it (it varies
whether a codec exists at all). State the arms as a table with the precise corpus/codec delta.
Hint to evaluate, not to accept: the natural pair may be "same jamo-BPE codec, negator forcibly
atomic" vs "same jamo-BPE codec, negator forcibly SHATTERED across token boundaries" — i.e. force
the merge table, don't let frequency decide. Say whether that is right, and how to force it without
perturbing anything else about the vocabulary.

### 2. THE CEILING PROBLEM (this killed the last design)
v1's f2 panel is saturated: M = 0.9083/0.9167 and the C3 leak ceiling = 0.9167. Any falsifier with
a threshold > 0.083 is unreachable. **Harden the task until the CONTROL sits near the 0.5 chance
floor**, leaving real headroom. Specify concretely how: more negation compositions? nested/double
negation? scope ambiguity? longer dependency? Give the exact grid construction. Then state the
expected control score and WHY it lands near 0.5 rather than near 0.9.

### 3. THE OOD BLIND SPOT (a requirement, not a suggestion)
No v1 panel can test bound-vs-free out of distribution: f1 is drilled + near ceiling; f2 is 100%
bound. **The held-out cell MUST carry both bound AND free forms** or the successor inherits the
blind spot. Specify the held-out panel's exact composition, and how you hold predicate identity
constant across the bound/free cells so the contrast is morphology and not vocabulary.

### 4. ADMISSIBILITY (pre-register, and check your own thresholds)
The campaign's gate: a falsifier is admissible only if it can return BOTH answers —
**reachable** (threshold ≤ metric ceiling − control score) · **not-free** (the scaffolding alone
must not clear it) · **one-variable** · **name-the-arm**. Give ≥5 falsifiers, each with its
threshold, and for EACH one show the arithmetic that it is reachable given your expected control
score. Include ≥1 negative control and ≥1 leak-ceiling/liveness arm (v1's C3 caught a dead
measurement twice — do not drop it). Report BPB and the recombination metric SEPARATELY, never
summed (p7: perplexity is never truth).

### 5. COST + THE SMALLEST VALID CONFIG
Give the model size, seq_len, steps, arm count, seed count, and where it runs (local MPS vs rented
GPU). Justify that the small config can still show the effect: note v1's OMEGA showed scale-STABLE
failure d384→d1024, so a small-scale positive is meaningful. State total wall-clock and $ estimate.

### 6. WHAT WOULD MAKE YOU NOT RUN THIS
Be adversarial about your own design. Name the single most likely way it produces a convincing
false positive, and the control that catches it.

## Output format
Terse. Tables and exact values over prose. Mark anything you are unsure of as `?`. Do not hedge and
do not pad. This becomes a pre-registered card, so every number you state will be frozen and
checked against the run.
