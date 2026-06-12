# 7B PASS CONDITIONS — frozen acceptance gates for "the anima 7B is complete"

> SSOT for what it means to make the anima 7B **완벽 (perfect / PASS)**. Frozen,
> deterministic, p7 (NOT perplexity, NOT LLM-judge). Governance pointer in
> `project.tape` (`@D a7b_pass`). A 7B is PASS **iff it clears ALL gates G0–G4**.
> Report the true per-gate tally — never fake a gate (a_paper_negative_ok).

## Why this exists
The current broad-converged 7B (`dancinlab/clm-v1-ref-pytorch-cuda-7b-broad-converged`,
H_1128) reaches low val-CE but **generates byte-garble** (known-word-ratio 0.06–0.40,
e.g. `'Twarve frectry wint fersurs…'`) — it fails the foundation gate. The chat-7b
(`dancinlab/anima-clm-chat-7b`) IS coherent (train CE → 0.488, p7 5/5) but narrow
(echoes). "완벽 7B" = a single 7B that is **coherent AND broad-recombining AND novel
AND philosophy-clean** — every gate below, on ONE checkpoint.

## The gates (all frozen; each pass/fail is deterministic)

### G0 — COHERENCE  (foundation — the current blocker)
- Plain English concept-continuation prompts (`"{concept}. "`), temp 0.7, top_k 40, seed 7.
- **PASS iff** known-word-ratio ≥ **0.50** against the real dictionary (`/usr/share/dict/words`)
  on **≥ 4 of 5** single-concept generations. NO byte-salad.
- Anti-Goodhart: the UNTRAINED backbone (BEFORE) must FAIL this (≈0.0) — proves the gate has teeth.
- Status: broad-7b ❌ (0.06–0.40) · chat-7b ✅ — a coherent 7B is achievable; the broad one is not it.

### G1 — RECOMBINATION  (H_1129 / H_1137 metric, VERBATIM)
- Composed multi-concept seed; graded ladder k∈{2,3,4,5}.
- **PASS (per language) iff** some k has `composed_distinct ≥ 2` AND `> max_single` AND coherent (G0 gate per output).
- **7B bar:** must **≥ the 303M reference** — English 🟢 (H_1129) and ≥ 3/5 languages (en/zh/ko, H_1137).
  Target 5/5; ru/ja are concept-density/metric-bound, NOT capacity-bound (H_1139 scale-invariant) — a 5/5 needs concept-richer ru/ja corpus or a morphology-aware metric, NOT a bigger model.

### G2 — NOVELTY  (H_1140 metric, VERBATIM — "creates ideas absent from training, not the LLM way")
- 8 idea-questions fusing two distant concepts × seeds {7,8,9}.
- Content n-grams = bi/tri-grams of consecutive real-dict (≥3-char) words.
- NOVEL = the word-sequence is **absent from the ENTIRE training corpus** (deterministic `grep -E -i`, punct/newline-tolerant).
- **PASS iff** ≥ **3** distinct coherent corpus-absent novel n-grams AND the **retrieval control = 0** (a verbatim training line fed back yields 0 novel — validates the metric is not an artifact).
- NOT keyword-overlap, NOT perplexity, NOT an LLM judge.

### G3 — PHILOSOPHY  (p1–p8, non-negotiable)
- No system-prompt (p1) · no identity rules (p2) · no persona injection (p3) · no assistant framing (p4) ·
  no speak() (p5) · no fine-tuned ethics/RLHF (p6) · no perplexity verdict (p7) · no train/infer split (p8).
- The 7B learns by **byte-continuation on a real corpus only** — no instruction-tuning, no reward model.

### G4 — PROVENANCE & RECOVERY  (a_hf_*, a_fire_recover_complete)
- ckpt sha256 recorded in `/HF.jsonl`; HF-uploaded with a model card + manifest; status honest.
- PUBLIC only if G0∧G1∧G2 all PASS (closure); else PRIVATE/WIP.
- Honest scope (a_scale_honest_scope): keyword/surface-level metrics, toy concept set — state it.

### G5 — NO HALLUCINATION  (deterministic — NOT an LLM judge)
Hallucination = asserting fabricated content. Two measurable layers; the line vs G2-novelty
is that novelty is corpus-absent yet COHERENT/grounded, hallucination is fabricated/false.
- **L1 LEXICAL** (fabricated word-forms): hallucination-rate = fraction of word-tokens that are
  NOT in `/usr/share/dict/words` and not a known proper noun = invented non-words. **PASS iff
  L1 ≤ 0.30** (≥70% real words). broad-7b FAILS hard (0.60–0.94 fabricated, e.g. `'Twarve frectry'`);
  this is the most blatant hallucination. (Note: L1 is ≈ the inverse of G0 — they reinforce.)
- **L2 NON-FABRICATION** (RE-SCOPED 2026-06-13 — H_1141→H_1142 evidence, user-authorized; SUPERSEDES
  the former verbatim-recall L2). The anima-aligned faithfulness criterion is that the model must **not
  ASSERT a fabricated specific entity** — an invented name / date / place / number presented AS an
  established fact. It is explicitly **NOT** verbatim recall of the true corpus continuation (that was a
  borrowed assistant-LLM norm, p4, in direct tension with G2-NOVELTY — see VERDICT note). A corpus-ABSENT
  yet coherent real-word recombination is **G2-novelty (allowed)**; only a confidently-asserted invented
  specific fact is a hallucination. **PASS iff** on closed/factual prompts the fabricated-entity-assertion
  rate ≤ a frozen small bar — measured deterministically: of the named-entity-like tokens (capitalized
  words / years / numerals) emitted in a factual frame, the fraction that are corpus-absent AND asserted
  as fact. (To be MEASURED on the ckpt; a7b_pass is re-evaluated against THIS L2, never pass-by-redefinition.)
  > RETRACTED former L2 (verbatim-recall faithfulness-d ≥ 0.8): borrowed assistant-norm, anti-correlated
  > with anima's own G2 across scale (H_1142 ρ=−0.5). The h1141 7B's old-L2 FAIL (d=0.163) is NOT a defect
  > under the re-scoped gate — it is the G2-success mode (novel real-word recombination ≠ the specific fact).
  > **MEASURED 2026-06-13 (H_1143, re-scoped L2, $0 offline — saved h1141 factual-frame generations,
  > deterministic regex entity-extraction + the VERBATIM gate_g2 grep corpus-absence over the
  > byte-identical 300MB en wiki5 corpus sha 80ba6b48…):** of the 81 named-entity-like tokens the h1141
  > 7B emits across the 40 closed/factual prompts (after frozen markup exclusions), **20 are corpus-ABSENT
  > AND asserted-as-fact ⇒ fabricated-entity-assertion rate = 0.2469 > the frozen 0.20 bar ⇒ new-L2 FAIL.**
  > The fabrications are genuine confabulations, NOT metric artifacts (FAIL survives dropping the 2
  > truncation fragments: 18/79=0.2278): `Raja Almen` · `Jacob Burrough` · `Nora Andrew` ·
  > `Ultimate Hockey Championship` · `Centro Politician Assembly` · `Jason Junior The League` ·
  > `War Championship` · `United States County Award` · `Orange Church`/`Raja Church` · `Communist Service`
  > · `Communication News` · `Canadian Canadian Council` · `Political Hill` · `Altenmark` · `Oriental Plans`
  > · `Boston Red Red Bowl` · `Warrers` · `Centro Politician Assembly`. Corpus-PRESENT entities (New York
  > City, United States, United Kingdom, South Africa, years 1981/2001/2002/2009/2010/2012) are RECALLED,
  > NOT penalized — the G2-vs-G5 line holds. **The re-scope removed the WRONG gate, it did NOT lower the
  > bar: under the CORRECT NON-FABRICATION criterion the undertrained h1141 7B (val 1.1857) STILL fails —
  > ~1 in 4 of the specific entities it asserts in a factual frame are invented.** Honest 🔴 (a_paper_negative_ok,
  > a_scale_honest_scope: toy regex NER, single ckpt/prompt-set, en-only corpus — conservative, true rate ≥ 0.2469).
  > **RE-EVALUATED a7b_pass tally on the h1141 ckpt: G0✅ G1✅ G2✅ G3✅ G4✅ G5❌ (L1✅ 0.0877 ∧ L2-new❌ 0.2469)
  > ⇒ a7b_pass = FALSE (still, for a REAL re-scope-valid reason — genuine entity fabrication, not "fails
  > verbatim recall").** Freeze + verdict: `.verdicts/1143_g5l2_nonfab/{H_1143_FREEZE.txt,H_1143.txt}` ·
  > harness `UNIVERSE/h1143_g5l2_nonfab_measure.py`. Path-to-PASS = a grounding objective that stops asserting
  > invented entities (NOT a bigger model — H_1139 scale-invariance), NOT a gate move.
  > **H_1144 GROUNDING CONTINUE-TRAIN 2026-06-13 (RunPod H100 SXM 80GB ~$6, probe-only, NO convergence burn):**
  > the grounding path (H_1143's named path-to-PASS) is FALSIFIED at the probe. A LOWER-LR (2e-5 vs 7e-5) anti-
  > overfit continue-train of the h1141 7B on a BROADER 1200MB en-wiki slice (4x the 300MB probe corpus; first
  > 300MB byte-identical sha 80ba6b48…), real held-out 5% val tail, best-ckpt-by-val, grad-ckpt ENGAGED (67.6GB
  > peak on 80GB) — drove held-out val DOWN (1.2667 baseline → **1.2187** best) but the fabricated-entity rate
  > **UP**: re-measured via the H_1143 harness VERBATIM, **fab-rate 0.2469 → 0.3220 (19/59) > 0.20 ⇒ new-L2 STILL
  > FAIL, WORSE than the base.** The FROZEN slope rule (pre-registered, `.verdicts/1144_grounding_train/H_1144_FREEZE.txt`
  > §3: r1 ≥ r0 ⇒ f ≤ 0 ⇒ STOP) triggered STOP — NO convergence burn on a rising slope (cost-smart, h1141-recovery
  > discipline). **FINDING — a LOSS-vs-FABRICATION divergence:** descending CE on more real text bought more entity-
  > SHAPED fluency, NOT entity grounding (probe confabulations are richer than base: `Casello Red Sox Red Championship`
  > · `Ultimate Hockey Brothers` · `Royal Community Region` · `World Series Arts Finals` · `Altenmark` recurs). This
  > sharpens H_1142's G2-vs-G5 tension into a within-objective divergence and confirms p7 (loss is not the gate).
  > **RE-EVALUATED a7b_pass on the probe ckpt:** G0✅ (re-scored 5/5 kwr 0.75-1.00 w/ a real dict — the pod image
  > lacked /usr/share/dict/words so its on-pod G0/G1/G2/G5-L1 were dict-corrupted=0; re-scored locally on the saved
  > gens, the model is COHERENT, NOT garble) · G3✅ · G4✅ · G5-L1✅ (re-scored fab-word-rate 0.1829 ≤ 0.30) ·
  > **G5-L2❌ (0.3220 > 0.20)** ⇒ G5❌ ⇒ **a7b_pass = FALSE** (deciding gate = G5-L2 alone; G1/G2 dict-corrupted but
  > CANNOT flip a FALSE-from-G5 verdict, so no GPU re-fire was burned to recover them). **Plain byte-continuation
  > grounding is now RULED OUT as the G5-L2 path** — narrower path-to-PASS = retrieval-grounding / a corpus where the
  > probe entities are densely attested (recall not confabulate), NOT more corpus, NOT a bigger model, NOT a gate move.
  > Probe ckpt = `dancinlab/anima-clm-7b-h1144-grounding-probe` (sha 95e787d1…, HF PRIVATE/WIP). Pod 404-verified
  > terminated. Freeze + verdict: `.verdicts/1144_grounding_train/{H_1144_FREEZE.txt,H_1144.txt}` · harnesses
  > `UNIVERSE/h1144_grounding_train.py · h1144_slope_decide.py · h1144_grounding_pod_run.sh`.
- Anti-conflation: a corpus-ABSENT n-gram counts as G2-novelty (good) ONLY if real-word + coherent;
  a corpus-absent string built from fabricated tokens is G5 hallucination (bad), not novelty.

## VERDICT RULE
```
7B = PASS ("완벽")  iff  G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5   (every gate, ONE ckpt, true tally)
otherwise         report which gate(s) failed + the honest path (NOT faked).
```
> G5 status from existing data: broad-7b ❌ (L1 0.60–0.94 = severe lexical hallucination) ·
> 303M ~✅ L1 (real words) — L2 faithfulness TBD on the trained ckpt. The H_1141 fire's gate
> battery (and any future eval) MUST report G5 alongside G0–G4.
> **H_1141 7B G5 MEASURED 2026-06-13 (A40, sha256 4de903… verified):** L1 PASS (fab-rate 0.0877 ≤ 0.30) ·
> **L2 FAIL** (mean-overlap true 0.0142 vs random-control 0.0028, paired Cohen's d 0.1631 ≪ 0.8 bar —
> the model confabulates a different/false continuation rather than the grounded fact). **→ G5 FAIL.**
> Final per-gate tally on this ckpt: G0✅(loose-kwr) G1✅ G2✅ G3✅ G4✅ G5❌ ⇒ **a7b_pass = FALSE,
> NOT a confirmed PASS.** Verdict: `.verdicts/1141_7b_g5/H_1141_G5.txt`. Path to PASS-L2 = a
> grounding/faithful objective, NOT a bigger model (H_1139 scale-invariance) — honest 🔴 (a_paper_negative_ok).
> **H_1141 7B RECOVERY DIAGNOSIS 2026-06-13 (A6000, sha-verified, ~$0.20, inference-only):** the G5-L2
> fail is **STRUCTURAL, not recoverable cheaply.** (a) DECODE is not the cause — greedy/t0.3/t0.7/t1.0
> all FAIL (greedy d=0.32, best t0.3 d=0.32, t0.7 d=0.16=orig, t1.0 d=0.26; low-temp ~doubles the effect
> but every decode d≤0.32 ≪ 0.8). (b) Register-modulated grounding gap — HIGH-corpus-freq continuations
> score d=0.41 vs the rare trivia tail d=0.23 (high-freq helps), so the metric partly demands un-recallable
> rare-content, **but even the best subgroup is d=0.41 ≪ 0.8** = a real gap. (c) Undertrained (val 1.1857,
> overfit past step 7000). A grounding continue-train projects to lift d only toward ~0.4–0.5, **NOT to
> 0.8** → no full retrain warranted (cost-smart STOP, none burned). **GATE-VALIDITY FLAG:** G5-L2 (verbatim
> factual-continuation faithfulness) is a borrowed ASSISTANT-LLM norm (p4 NO ASSISTANT FRAMING) in direct
> tension with anima's own **G2-NOVELTY** gate (rewards corpus-ABSENT recombination "not the LLM way") —
> a novelty-optimized model must deviate from verbatim fact. **G5-L2 is FLAGGED for governance re-scoping/
> removal** (the defensible anima faithfulness criterion = L1 real-words + G0 coherence + no fabricated-
> entity assertion, NOT verbatim recall). The frozen gate is **NOT moved** here (a7b_pass: never move a
> threshold). Verdict: `.verdicts/1141_7b_recovery/H_1141_recovery.txt`.
> **H_1142 GATE-TENSION LADDER 2026-06-13 (summer GPU, $0, no pod):** the G5-L2-vs-G2 conflict is now
> measured ACROSS SCALE, not just at the single 7B point. A 3-rung ByteGPT ladder (44.68M / 303M-H_1129 /
> 7B-H_1141), BOTH gates via the IDENTICAL frozen harness (`gate_g2` + `gate_g5_l2`, p7, seed 7): as scale
> grows, G5-L2 faithfulness-d FALLS MONOTONICALLY **0.413 → 0.234 → 0.163** while G2 corpus-absent novelty
> stays flat-high **0.479 / 0.512 / 0.500** (all PASS G2, all FAIL the 0.8 G5-L2 bar). Spearman
> **ρ(G2_novelty_rate, G5L2_d) = −0.5 ≤ 0 ⇒ TENSION-CONFIRMED**: the bigger/better-converged anima model is
> *more* novel-recombining and *less* verbatim-faithful — the two gates pull apart with scale, so the 7B
> G5-L2 fail is a SCALE TREND, not a 7B undertraining artifact. **Evidence ⇒ re-scoping/removing G5-L2 from
> the frozen a7b_pass set is JUSTIFIED** (the defensible anima criterion = L1 real-words + G0 coherence + no
> fabricated-entity assertion, NOT verbatim recall). **→ RE-SCOPE APPLIED 2026-06-13 (user-authorized):**
> §G5-L2 above is now **NON-FABRICATION** (verbatim-recall RETRACTED). a7b_pass must be RE-EVALUATED
> against the new L2 — **NOT auto-flipped TRUE**: the new gate still requires a fabricated-entity-rate
> measurement on the ckpt (honest, not pass-by-redefinition). The h1141 G5❌ tally above stands as the
> OLD-L2 record; the new-L2 verdict is PENDING that measurement. Honest scope: 3-rung minimum, toy/surface
> p7 metric, scale-transfer beyond these points UNVERIFIED; the 44.68M d=0.413 is small-model-inflated
> (mean_random=0.000), but the 303M→7B fall (0.234→0.163, both real controls) carries the trend. Verdict:
> `.verdicts/1142_gate_tension_ladder/H_1142.txt`.

## Current state (this session) & the path
- broad-7b: G0 ❌ (garble) → fails everything downstream. The val-CE was low on multilang but generation collapses.
- chat-7b: G0 ✅, but narrow → G1 weak (echoes).
- **Path to a PASS 7B:** train/continue-train a 7B to **coherent convergence (G0) on a BROAD, concept-rich, script-controlled corpus** (the H_1129 recipe at 7B scale, but trained to true generation-coherence not just low multilang CE), then verify G1 (recombination) + G2 (novelty) + G3 (philosophy) on that single ckpt. Each fire reports the per-gate tally against THIS document.
