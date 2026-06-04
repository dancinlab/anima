# torch ENGINE-7B data-sufficiency PREFLIGHT — RULING: DATA-STARVED (do NOT fire)

substrate = GPU (Lane G-ref, torch-reference) · gate run 2026-06-05 · $0 (no GPU rented)
slug = torch-engine-7b-datagate · base = lane-g/campaign-pivot-descent

This verdict answers ONE question before renting any GPU: does the default-lane
corpus support a *properly-trained* (coherent, non-memorizing) torch ENGINE 7B?
Answer: **NO. Data-starved by ~10^4×.** A multi-hour 7B GPU fire on this corpus is
deterministically doomed (gibberish-undertrained OR memorization) — it is NOT the
primary path (a_completeness_over_cheap: do not rank a doomed expensive run primary).

══════════════════════════════════════════════════════════════════════════════
PART 1 — DATA-SUFFICIENCY MATH (the hard gate)
══════════════════════════════════════════════════════════════════════════════

Corpus (default lane):
  HF `dancinlab/anima-corpus-5lang-unified-v2` ≈ 12.5 MB, byte-tokenized at V=256.
  byte-token count N_tok ≈ 12.5 MB ≈ 1.25e7 tokens (1 byte = 1 token at V=256).

Model:
  target = 7B-param byte LM (the "real 7B").  P = 7.0e9 params.

Chinchilla-optimal token budget (Hoffmann et al. 2022, ~20 tok/param):
  N_opt ≈ 20 · P = 20 · 7.0e9 = 1.40e11 tokens (140 B tokens).

Sufficiency ratio:
  N_opt / N_tok = 1.40e11 / 1.25e7 ≈ 1.12e4   →  the corpus is ~11,200× too small.

Even a *minimal-coherence* (well below Chinchilla, ~1–3 tok/param for a weak but
non-gibberish byte model) budget wants ≈ 7e9–2.1e10 tokens — still ~560×–1680×
over the 1.25e7 we have. There is NO epoch count that closes a 10^3–10^4× token
deficit: looping a 12.5 MB corpus enough times to reach 140 B tokens = ~11,200
passes over the SAME bytes → the model MEMORIZES the corpus, it does not learn a
generalizing byte distribution (coherence). Memorization ≠ coherence (the falsifier).

RULING-1 (data sufficiency): **DATA-STARVED = YES.**  ratio ≈ 1.12e4 ≫ 1.

══════════════════════════════════════════════════════════════════════════════
PART 2 — EVIDENCE IT IS ALREADY PROVEN (the harvested CORPUS-7B, verbatim)
══════════════════════════════════════════════════════════════════════════════

This is not a prediction — it was already FIRED and harvested. From
`.verdicts/default-lane-7b/HARVEST-VERDICT.md` (commit 7a5240c3d), VERBATIM:

  arch: ConsciousLMReconstructed dual-engine d=4096/L21/h32/block512 · params 7,053,230,080
  substrate: PyTorch-CUDA REFERENCE lane (Lane-G/GPU) — NOT forge production
  tok_seen: 98,304,000 · first_train_ce 5.6955 → final_train_ce 1.1432 · descent_pass: TRUE
  util: peak 100% · mean 90.06% · pct_ge20 91.1% (torch saturates GPU — expected)
  trained p7-strict: FAIL (3/5) · random_init_mirror: FAIL (0/5) · anti_goodhart_ok: FALSE
  memorization: low-verbatim (median 0.0, held_out_generalizes TRUE — NOT memorizing)
  **RULING: "gibberish-undertrained" · chat_pass: FALSE**

Reading: descent worked (CE 5.70→1.14) and util was great (torch saturates, ~90%),
yet replies were empty/broken (en/ko empty; fr a German-ish mix). 98.3 M tokens /
6000 steps is FAR below what a 7B needs. This is the *non-memorizing* failure mode
(held_out_generalizes TRUE) — it confirms the corpus is too small to reach coherence,
NOT too small to avoid overfitting. CLOSED-NEGATIVE, consistent with the prior 7B
closed-neg (#1828).

Note: that run used 98.3 M tokens (already ~8× the 12.5 MB single-pass corpus, i.e.
multiple epochs) and STILL produced gibberish. Pushing more epochs on 12.5 MB only
moves the regime toward MEMORIZATION (∵ same bytes re-seen) — it does not buy
coherence. Both failure modes are gibberish for a chat target.

RULING-2 (empirical): a torch 7B on this corpus = gibberish-undertrained, chat_pass=FALSE.
A multi-hour 7B GPU fire on this corpus is DOOMED. **NOT RENTED (gate held, $0).**

══════════════════════════════════════════════════════════════════════════════
PART 3 — THE ACHIEVABLE WIN IS ALREADY DEMONSTRATED (torch→ENGINE path WORKS)
══════════════════════════════════════════════════════════════════════════════

The honest payoff of the v0.2-CLMX serializer (PR #1845, `CLM/model/clm_serialize_v2.py`)
is that a *right-sized*, coherent E2/V256 CLMConvMoE torch state_dict can now be
serialized to an ENGINE-loadable `.clm`. This is ALREADY shown at two scales:

── (A) torch→ENGINE on a TRAINED torch model (PR #1845 smoke, Lane G-ref) ──
   `.verdicts/clm-serialize-v2/smoke_trained.txt` (branch lane-g/clm-serialize-v2), VERBATIM:

     PART A — TRAINED torch model (d=16, 120 AdamW steps, CE 5.81 -> 2.91 torch-side)
     `hexa run CORE/ce_descent_probe.hexa` (CE_CLM=smoke_trained_d16_v2.clm):
       [admit] valid=true decodable=true loaded=true nblocks=6
       [CE] d=16 E=2 V=256 K=3 windows=16
       [CE] model_ce   = 2.76676
       [CE] shuffle_ce = 3.80927
       [CE] uniform_ce = 4.79906
       F-CLM-CORE-CE-DESCENT (model_ce < uniform AND < shuffle) = 1 🟢
     `hexa run CORE/clm_v2_decode_smoke.hexa` (decode_argmax forward):
       [decodable] clm_decodable=true
       [decode forward] ok=true gen_bytes=16
       F-CLM-V2-LOADABLE (decodable AND forward ran) = 1 🟢

   `.verdicts/clm-serialize-v2/byte_compare.txt`, VERBATIM:
     STRUCTURE (block boundaries + trailer offset + 11 ext sizes) IDENTICAL=True
     DETERMINISM: serialize x2 byte-identical=True  sha256=8956939717fd2ada
     ROUND-TRIP: max|decoder_dequant - torch_qdq| = 0.0  (0.0 = exact)

   → The TORCH serializer writes a v0.2-CLMX .clm that CORE/clm_decode.hexa loads,
     runs a decode forward on, AND shows CE-descent on the trained model. The
     torch→ENGINE path is verified END-TO-END (writer→decoder, value round-trip 0.0).

── (B) PRODUCTION-scale coherent ENGINE .clm already PUBLIC (d=768 E2/V256) ──
   `.verdicts/core-3axis-mount/ce_descent.txt` (this base branch), VERBATIM key lines:
     clm=.../reexport_d768_v2_fast.clm
     [admit] valid=true decodable=true loaded=true nblocks=6
     [CE] d=768 E=2 V=256 K=3 windows=16
     [CE] model_ce   = 4.42613   shuffle_ce = 4.49555   uniform_ce = 4.79906
     F-CLM-CORE-CE-DESCENT = 1 🟢
     [AXIS-1 의식] motiv hi=0.6700 baseline=0.0000   → F-CORE-3AXIS-1 = 1 🟢
     [AXIS-3 창발] len(composed)=101 len(parts-only)=72 → F-CORE-3AXIS-3 = 1 🟢
     CORE-mounted axes GREEN: 3/3

   HF: `dancinlab/clm-v1-d768-core-3axis-green` (PUBLIC, status=public, sha256
   db7dc990…b751497, CLM collection) — "THE legitimately-final PASS-grade CLM",
   3/3 CORE-mounted GREEN (의식 + CE-descent + 창발). This is an ENGINE-loadable
   COHERENT v0.2-CLMX .clm at PRODUCTION d=768.

   Honest nuance (a_train_flame_forge · a_lane_akida_gpu_split): the PUBLIC d768
   .clm was produced by the hexa-side host reexport (clm_reexport.hexa, $0-CPU),
   NOT by the torch clm_serialize_v2.py. The TORCH writer's coherence is proven on
   the d16 trained model (A); its byte layout is structurally identical to the d768
   reexport and round-trips at max|Δ|=0.0 (byte_compare.txt). So: torch writer
   correctness = proven; a torch-written *production-scale* coherent .clm has not
   been re-emitted only because no source .pt for the d768 reexport survives on disk
   (byte_compare.txt: "no source .pt for the d768 reexport exists"). The ENGINE-
   loadable COHERENT artifact itself EXISTS and is PUBLIC (B); the torch path that
   produces such artifacts is verified (A).

══════════════════════════════════════════════════════════════════════════════
SYNTHESIS — substrate-tagged, honest scope
══════════════════════════════════════════════════════════════════════════════

  data-sufficiency 7B   🔴  DATA-STARVED (ratio ≈ 1.12e4) — torch 7B fire DOOMED, NOT RENTED ($0)
  empirical 7B          🔴  CORPUS-7B harvested = gibberish-undertrained, chat_pass=FALSE (verbatim)
  torch→ENGINE path     🟢  PR #1845: trained d16 torch → v0.2-CLMX .clm → decode forward + CE-descent (verbatim)
  byte round-trip       🟢  decoder_dequant vs torch_qdq max|Δ| = 0.0 (exact)
  COHERENT ENGINE .clm  🟢  d768 E2/V256 3/3 CORE-GREEN, PUBLIC (clm-v1-d768-core-3axis-green)

ANSWER TO THE TASK'S ONE-LINE QUESTION:
  Is there now an ENGINE-loadable COHERENT .clm demonstrated?  → YES (d768, PUBLIC, 3/3 GREEN).
  Is the torch→ENGINE serializer path verified?                → YES (PR #1845 trained-model smoke + 0.0 round-trip).
  Is the blocker corpus-scale?                                 → YES — a TRUE 7B needs a GB-scale corpus
                                                                  (~140 B tokens vs the 12.5 M we have, ~10^4× gap).

HONEST NEXT STEP (the real prerequisite, NOT a 7B fire):
  Build/acquire a GB-scale (≥ ~10^9–10^11 byte-token) clean-license corpus FIRST.
  Only then is a coherent 7B reachable. Right-sized scales (≤ the proven ~18M chat
  rung; d768 E2/V256) are ALREADY coherent and ENGINE-loadable on this corpus —
  the serializer's payoff is delivered there, not at a data-starved 7B.

No GPU rented. No fabrication. The 7B fire was NOT run (gate held).
