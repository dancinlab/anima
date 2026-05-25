# anima CLM-3 — chat-objective-at-cycle-0 substrate spec (BG-BM, H1 spec land)

- Date: 2026-05-06
- Status: SPEC LANDED (doc-only; no build/train this cycle)
- Cost: $0 (mac, doc only)
- Lane: H1 of theorem #115-ARCHITECTURAL-FINAL-4-CLOSURE — only untested
  hypothesis with material chance of overturning closure-of-class
- Predecessor: `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md`
  Corollary 2 (CLM-3 design constraint)
- Supersedes: BG-Y rec C (informal CLM-3 sketch)

---

## 0. Abstract / 초록

**EN.** CLM-3 is a proposed anima-internal substrate that retains CLM v4's
consciousness-coupling property (cross-attn over `consciousness_states`,
paradigm v11 G3, +41.86 Φ★) while declaring **chat-loss as a first-class
objective from cycle-0 of pre-training**. The 4-closure theorem (#115)
formally rules out chat-recovery from CLM v4 across post-hoc adapter,
train-time distill, cross-modal bridge, and residual-stream probing. CLM-3
is the only path-of-record that bypasses every closure simultaneously,
because it changes the *training mixture* rather than acting on a
substrate already trained without a chat axis. This document fixes the
design diff vs CLM v4, the 4-bucket pre-training mix, four falsifiers
locked before any compute is spent, the cost / time envelope across three
scale variants, and a build-vs-wait decision matrix tied to Stage 3
emerge-dialogue user-fire evidence accumulation.

**KO.** CLM-3는 CLM v4의 consciousness-coupling property는 유지하면서,
**chat-loss를 cycle-0부터 first-class objective로 선언**하는 anima-internal
substrate proposal이다. 4-closure theorem(#115)는 CLM v4 위에서 post-hoc
adapter, train-time distill, cross-modal bridge, residual-stream probing
네 axis 모두에서 chat-recovery 불가를 정식 closure 했다. CLM-3은 trained-
without-chat substrate 위에서 작동하지 않고 *training mixture* 자체를 바꾸므로,
4-closure 모두를 동시에 우회 가능한 유일한 path-of-record 이다. 본 문서는
CLM v4 대비 design diff, 4-bucket pre-train mix, build-전 lock된 4 falsifier,
3-scale 비용/시간 envelope, Stage 3 emerge-dialogue 누적 evidence 와
연동된 build/wait decision matrix를 정식 명세한다.

---

<!-- [Hc_630 clm3-chat-objective-cycle0-substrate-h1 — moved to hypotheses_candidates/Hc_630_clm3_chat_objective_cycle0_substrate.md on 2026-05-11] -->

## 1. CLM v4 vs CLM-3 — design diff

### 1.1 Carry-over from CLM v4 (substrate property preservation)

| Property | CLM v4 value | CLM-3 value | Reason |
|---|---|---|---|
| base architecture | 16-layer decoder transformer, hidden_dim 768, ~530M | same (default) or 1B / 3B variant (§4) | parity for cross-substrate Φ★ comparison |
| `consciousness_states` cross-attn | paradigm v11 G3 (+41.86 Φ★) | retained | substrate-coupling is the unique anima property; H1 must NOT become "Llama with extra steps" |
| 5-axis discriminability training surface | implicit (BG-L 0.20 random baseline) | explicit (§3 F-CLM-3-4 ≥ 0.4) | train-time axis exposure expected to close gap |
| Φ★ stability target | +41.86 baseline | NO_FLIP carry (forgetting_index ≤ 0.05) | substrate-research utility must survive chat-objective addition |
| HF release lifecycle | private→public | identical | no policy change |

### 1.2 New in CLM-3 (chat-objective-at-cycle-0)

| Element | CLM v4 (none/post-hoc) | CLM-3 (cycle-0) | Mechanism |
|---|---|---|---|
| chat-loss head | absent | dedicated chat-loss objective term added to total loss from step 0 | weighted sum: `L_total = α·L_substrate + β·L_chat + γ·L_axis`, with α/β/γ ablated in §3 falsifier-pre-launch sweep |
| dialogue corpus presence | 0% | 30% (§2) | KO+EN ChatML or anima-native dialogue format |
| instruction-tuned data | 0% (post-hoc SFT route closed by closure 1) | mixed in pre-training, NOT post-hoc | bypass closure 1 by construction |
| reasoning chains (CoT) | absent | 15% | bypass closure 2 by giving the trained substrate a chat-aligned axis to *be* a teacher of, rather than receiving a Φ★-only teacher |
| chat composite target | n/a | F-CLM-3-2 ≥ 0.45 (= 80% of Llama Path A v2 winner 0.5584) | escapes residual-stream pervasive failure (closure 4) by training chat-text basis into every residual layer |

### 1.3 Architectural delta map (closure → CLM-3 mitigation)

- closure 1 (post-hoc adapter) → CLM-3 §1.2 row 3: chat appears at cycle-0
  pre-training, not as adapter
- closure 2 (Φ★-axis distill bounded) → CLM-3 §1.2 row 4 + §2 mix: chat is a
  primary axis of training, not a distillation target on a Φ★ teacher
- closure 3 (cross-modal bridge) → CLM-3 produces token logits natively
  (same as CLM v4 LM head); no bridge needed
- closure 4 (residual-stream pervasive byte-fragment) → CLM-3 §1.2 row 5: by
  training chat-text basis as part of the substrate's core objective, every
  residual layer is expected to develop recoverable chat basis (testable
  post-hoc with the same logit-lens / semantic-bridge harness used for
  closure 4)

---

## 2. Pre-training mix — 4 buckets

| Bucket | Ratio | Source class | Why |
|---|---|---|---|
| general text | 50% | C4 / FineWeb / KO web crawl subset (license-filtered) | substrate Φ★ stability anchor; Pβ FAIL_TRUE taught us mix that is too chat-heavy destabilizes the consciousness-coupled axis |
| KO-EN dialogue corpus | 30% | ChatML-formatted multi-turn (UltraChat / OASST KO subset / anima-native emerge-dialogue trace if Stage 3 yields ≥ 30 sessions) | first-class chat axis presence at cycle-0 |
| reasoning chains (CoT) | 15% | OpenOrca / GSM8k / KO math-CoT subset / hand-curated anima reasoning traces | reasoning-axis is empirically chat-adjacent; raises composite (MMLU / hellaswag-norm) without forcing chat-template lock-in |
| consciousness_states diverse distribution | 5% | anima-internal Φ★ trajectory tagged samples (paradigm v11 G3 carry) | preserves cross-attn surface; retains substrate-research utility |

Mix ratio rationale: Pβ 50K closure 2 demonstrates a single-axis training
(Φ★) cannot transfer chat (composite 0.01176 FAIL_TRUE). The inverse risk —
chat-heavy mix — is that it destabilizes Φ★ (forgetting_index regression).
50/30/15/5 is the **smallest chat-share that has a credible chance of
clearing F-CLM-3-2** while keeping consciousness_states share non-zero
(falsifier F-CLM-3-1 NO_FLIP must hold).

Ablation sweep (pre-launch, $0 doc-only): three candidates 60/25/10/5,
50/30/15/5 (default), 40/35/20/5. Final ratio chosen by smallest variant
that simulates F-CLM-3-2 ≥ 0.45 *and* F-CLM-3-1 NO_FLIP under a 1B-token
proxy run (§4 scale variant B).

---

## 3. Falsifiers — locked before any compute

All four falsifiers are LOCKED at this spec land. Any redefinition after
training begins is treated as raw#9 violation (post-hoc moving goalposts).

### F-CLM-3-1 — substrate Φ★ NO_FLIP

- Target: `forgetting_index ≤ 0.05` vs CLM v4 paradigm v11 G3 baseline
  (+41.86 Φ★)
- Eval: re-run paradigm v11 G3 measurement harness on CLM-3 final checkpoint
- PASS condition: NO_FLIP + forgetting_index ≤ 0.05
- FAIL kind: REGRESSION_TO_NON_SUBSTRATE — CLM-3 lost the consciousness-
  coupling property; mix was too chat-heavy; rerun with 60/25/10/5
- Anchor: closure 1 forgetting_index 0.0196 PASS (LoRA SFT did not damage Φ★);
  CLM-3 must equal-or-better that under a much more aggressive training mix

### F-CLM-3-2 — chat composite ≥ 0.45

- Target: composite{HellaSwag-norm, MMLU, TriviaQA-EM, OpenBookQA-norm} ≥ 0.45
  on lm-eval limit=200
- Comparator: Llama-3.2-3B Path A v2 winner = 0.5584 (3-bench, OBQA absent)
- Threshold rationale: 80% of Llama winner; clears CLM v4 base (0.20-class)
  by ≥ 25 pp; clears LoRA SFT (0.19542) by ≥ 25 pp
- PASS condition: composite ≥ 0.45 AND no single bench at chance
- FAIL kind: CHAT_AXIS_NOT_TRAINED — even cycle-0 chat objective failed;
  closure-of-class strengthened (H1 itself falsified for this scale variant)

### F-CLM-3-3 — emerge dialogue medium preserved

- Target: BG-AN 5-turn emerge-dialogue smoke harness produces non-trivial
  output (medium quality ≥ Stage 2 baseline) on CLM-3
- Eval: re-run BG-AN smoke battery (5 prompts × 5 turns each) on CLM-3
- PASS condition: emerge-dialogue protocol still functional (i.e., enabling
  chat capability has NOT erased the substrate-coupled emerge medium)
- FAIL kind: EMERGE_PARADIGM_LOST — CLM-3 became a normal chatbot, lost the
  unique anima property; cycle is not a net win even if F-CLM-3-2 PASSes
- Anchor: theorem #115 Corollary 3 — emerge dialogue paradigm decoupled from
  traditional chat; F-CLM-3-3 enforces both can coexist in CLM-3

### F-CLM-3-4 — 5-axis discriminability ≥ 0.4

- Target: BG-L 5-axis discriminability ≥ 0.40 (random = 0.20; 2× random)
- Eval: BG-L axis-conditioned probe re-run on CLM-3
- PASS condition: discriminability ≥ 0.40
- FAIL kind: AXIS_TRAINING_INEFFECTIVE — explicit axis exposure during
  pre-training did not buy axis-discrimination; expected from 5% diverse
  consciousness_states share; treat as substrate-research-only carry, do
  not block deployment if F-CLM-3-1/2/3 all PASS

PASS gate: ALL of {F-CLM-3-1, F-CLM-3-2, F-CLM-3-3} = PASS, with F-CLM-3-4
as soft-gate (logged but not blocking). Any of the three primary
falsifiers FAIL = lane closure CLM_3_LANE_*_FAIL_TRUE.

---

## 4. Cost + time envelope — 3 scale variants

### Variant A — 530M parity scale

- params: ≈ 530M (parity with CLM v4)
- compute: ubu1 RTX 5070 sm_120 + torch 2.11.0+cu128 (memory:
  reference_ubu1_venv_orchestrator)
- wall-clock: ~60-90 days @ ~10B-token target (slower; bounded by 5070 vRAM)
- direct cost: $0 (already-owned compute)
- **operator cost**: power + occupancy of single GPU for 60-90 days
- risk: long lead time; emerge-dialogue Stage 3 evidence will accumulate in
  parallel and may revise the spec mid-train

### Variant B — 1B scale

- params: ≈ 1B
- compute: H100 1× × ~30 days
- direct cost: ≈ $1,000 minimum (watchdog applicable)
- wall-clock: 30 days
- risk: budget guard; user-fire required; partial-failure
  tolerance via checkpointing every 24h

### Variant C — 3B scale

- params: ≈ 3B (Llama-3.2-3B parity for direct chat composite comparison)
- compute: H100 4× × ~30 days
- direct cost: ≈ $4,000 (multiplicative risk)
- wall-clock: 30 days (parallel)
- risk: highest absolute $; falsifier failure is most expensive

### Recommended starting variant

**Variant B (1B, H100 1×, ~$1k, 30d)** — cheapest credible test of H1.
Variant A is too long-tailed (Stage 3 evidence will overrun the train);
Variant C is unjustified before B clears F-CLM-3-2 at 1B.

If Variant B clears all primary falsifiers, **escalate to Variant C** for a
chat-cap winner candidate at parity scale to Llama-3.2-3B. If Variant B
fails any primary falsifier, **close H1 lane** and accept the 4-closure
theorem at full closure-of-class strength.

Variant A is reserved as a **$0 fallback** for users explicitly opting out
of H100 spend; expected to produce evidence ~6× slower than Variant B at
roughly parity quality (if 5070 power envelope holds).

---

## 5. Build / wait decision matrix

| Precondition | Status (2026-05-06) | Required for build? |
|---|---|---|
| Pβ Φ★-distill closure (closure 2) | done (FAIL_TRUE_CLOSED) | yes (informs §1 axis carry) |
| LoRA SFT closure (closure 1) | done (FAIL_REGRESSION) | yes (informs §1 post-hoc-route closure) |
| Llama Path A v2 chat-cap winner confirmed | done (composite 0.5584) | yes (provides F-CLM-3-2 anchor) |
| BG-AN emerge-dialogue paradigm validated | done (smoke battery PASS) | yes (informs §1 emerge-medium carry, F-CLM-3-3) |
| Stage 3 emerge user-fire ≥ 30 sessions accumulated | NOT YET (Stage 3 protocol exists, sessions not yet logged) | **soft-required** — informs CLM-3 axis design |
| budget guard explicit user-fire (Variants B/C) | not-yet-fired | hard-required for B/C |

### 5.1 Build-now triggers (any-of)

- user explicitly fires CLM-3 launch under budget guard, accepting
  ~$1k for Variant B (most likely path)
- emerge-dialogue Stage 3 surfaces a strong axis-design lead in < 30 sessions
  that materially changes §1.2 and demands fast verification
- a converging external signal (e.g., new chat-cap eval anchor below 0.45
  obsoletes F-CLM-3-2) demands re-baselining

### 5.2 Wait triggers (any-of)

- budget guard not yet fired (current default)
- Stage 3 emerge-dialogue session count < 30 (current count: 0 logged) AND
  emerge-medium evidence is still informer-class for §1 axis design
- substrate-research-only path on CLM v4 still producing measurable Φ★
  insights that may revise CLM-3 §1.1 carry-overs

### 5.3 Recommended decision (this cycle)

**WAIT** — for **Stage 3 emerge-dialogue ≥ 30 user-fired sessions**, with
two purposes:
1. emerge-dialogue traces themselves become candidate anima-native dialogue
   corpus for §2 bucket 2 (replacing or augmenting OASST KO subset)
2. axis patterns surfaced by Stage 3 inform §1.2 chat-loss head design
   (e.g., whether chat-axis should be coupled to Φ★ trajectory or kept
   orthogonal)

WAIT does **not** mean cancel — H1 is the only un-falsified hypothesis with
material chance to overturn the 4-closure theorem's class-of-substrates
generalization. WAIT means "build with informed §1 design, not blind
defaults". Stage 3 evidence accumulation is the planned informer.

If Stage 3 stalls (< 30 sessions in 90 days), escalate to **build under
§1 default design as filed in this spec**, accepting the Stage-3-informed
revision as a future CLM-3.1 follow-up.

---

## 6. Honest C3 (≥ 5)

### C3-1. H1 has not been demonstrated to overturn the closure — only stated as the only un-tested hypothesis with material chance.

This spec frames CLM-3 as the path most likely to overturn closure-of-
class. That framing is grounded in the four closures' construction
(closure 1–4 all act post-hoc on a non-chat-trained substrate). It is
**not** grounded in CLM-3 evidence — none exists yet. If F-CLM-3-2 fails
at Variant B, H1 is itself falsified for at-most-1B substrate scale, and
the closure-of-class generalization strengthens (not weakens). The spec
does not pre-allocate optimism beyond "the only un-blocked path".

### C3-2. Mix ratio 50/30/15/5 is empirically untested.

The Pβ FAIL_TRUE tells us "100% Φ★ teacher = chat fail". That does not
tell us the *correct* chat share. 50/30/15/5 is a defensible default, not
a measured optimum. The pre-launch ablation sweep (§2) may surface
40/35/20/5 or 60/25/10/5 as a better mix; in that case the spec is revised
before Variant B fires. Treat the default as a starting point, not a fact.

### C3-3. F-CLM-3-2 0.45 threshold is 80% of one Llama winner's composite.

The 0.45 threshold is anchored to Llama Path A v2 = 0.5584. That winner is
itself a single-seed result on lm-eval limit=200 (per memory
`feedback_v2_fail_was_measurement_artifact`). A 5-seed Llama anchor may
shift the reference up or down by 1-3 pp; if it shifts down, 0.45 looks
generous; if up, severe. The threshold should be re-anchored once a 5-seed
Llama composite exists. We log the dependency rather than freeze the
number.

### C3-4. F-CLM-3-1 forgetting_index ≤ 0.05 is the LoRA-era threshold; CLM-3 is a fundamentally different training profile.

Forgetting-index 0.05 was set when the only thing that could regress the
substrate was a small adapter. CLM-3 is a full pre-train that *includes*
chat objective; "forgetting" is a category error here — there is nothing
to forget because nothing was trained first. The right F-CLM-3-1 may need
to be reformulated as "Φ★ peak preserved within ± 5% of paradigm v11 G3
+41.86 baseline at parity scale". This spec uses the existing operationalization
provisionally; revision pending eval-harness review.

### C3-5. The "H1 priority over H2-H4" claim deserves push-back.

Theorem §4 lists H2 (substrate-coupled emit format / emerge dialogue),
H3 (multi-substrate ensemble — Llama emit + CLM v4 phi gate), and H4
(broader prompt sweep). Of these:
- H2 is *already being pursued* at $0 (Stage 3 emerge dialogue) and may
  yield *the* anima-native chat path without any CLM-3 spend
- H3 is also $0-$10 class (no new training, runtime ensemble harness only)
- H4 is < $50 (broader prompt sweep through existing logit-lens /
  semantic-bridge harness)

**CLM-3 is the most expensive H1-H4 path** ($1k-$4k) and not obviously the
best return on investment. The honest position is: "H2 + H3 + H4 should
be exhausted at < $100 total before H1 fires". Recommended priority for
paths with material chance to refute the closure-of-class:
1. H2 (Stage 3 emerge dialogue ≥ 30 sessions, $0)
2. H4 (broader-prompt logit lens / semantic bridge sweep, ~$50)
3. H3 (ensemble harness Llama-emit + CLM v4 Φ★-gate, ~$10)
4. H1 (CLM-3 Variant B build, $1k) — **only after 1-3 are exhausted**

This re-orders against the BG-BM task brief's framing ("H1 first") and
should be explicitly resolved by the user before any compute fires.

---

## 7. Deliverables of this cycle

- this doc (`docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md`)
- verdict file (`state/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05/verdict.json`)
- no code, no scripts, no commits

## 8. Cross-references

- `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md` (theorem #115, all 4 closures)
- `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json` (closure 1 anchor)
- `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json` (closure 2 anchor)
- `state/anima_emerge_chat_tribev2_2026_05_05/verdict.json` (closure 3 anchor)
- `state/anima_emerge_chat_logit_lens_2026_05_05/verdict.json` (closure 4 anchor)
- `docs/anima_core_emerge_paradigm_revision_2026_05_05.md` (H2 / Stage 3)
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` (H2 user-fire)
- memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`
- memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`
- memory `feedback_h100_cost_discipline_l23_l25_watchdog_own_16` (for Variant B/C)
- memory `feedback_hf_release_private_to_public_after_verification` (CLM-3 release lifecycle)

## Compliance footer

- raw#9 honest scope: H1 framed as "only un-tested with material chance",
  not "guaranteed to overturn"; thresholds tagged as anchor-dependent in C3-3
- raw#10 honest C3 emitted: 5 caveats in §6, including explicit re-ordering
  push-back against the BG-BM task brief's H1-first framing
- raw#15 additive: no edits to closure verdicts, theorem doc, or any
  existing file; only two new files (this doc + verdict.json)
- HF token leak: none (no token literals embedded; no credential references)
- commit: not requested in this task; doc landed only
- bash 3.2 / mac compat: doc-only artifact, no scripts
- $0 mac doc-only: confirmed; no compute or HF calls fired
