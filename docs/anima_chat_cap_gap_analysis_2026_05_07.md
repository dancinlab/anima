# anima chat-cap 9-axis architecture gap analysis (BG-IT) — 2026-05-07

> **BG-IT — 9-axis architecture sweep synthesis. NO new training; pure synthesis of 22+ landed BGs.**
> Goal: identify the 1–3 unmet axes with highest expected value (EV) toward SIMPLE_STACK_PASS
> (strict V2 ≥ 7/15 + V3 ≥ 5/15 + zero persona-cycle + manual ≥ 10/15 across 5 std + 5 identity + 5 ubm prompts).
> SSOT: `state/anima_model_attempts_ledger.jsonl` (29 entries) + `state/anima_evaluator_v3_retroeval_2026_05_07/retroeval_v3_summary.json` (8-BG V3 retroeval).
> Status of pending BG-IS V3 retroeval extension: **MISSING at synthesis time** (waited 15 min — proceed without per task constraints; this doc may need additive extension if BG-IS lands later, raw#15 additive).

---

## Section 0 · Frame and definitions

**SIMPLE_STACK_PASS criteria (strict)**
- C1.1 length ≥ 10 chars
- C1.2 char diversity (Shannon ≥ 2 bits)
- C2.1 Korean particle count ≥ 3
- C2.2 Korean ending presence ≥ 1
- C2.3 domain keyword overlap ≥ 1
- C2.4 named-speaker leak negative
- C3.1–C3.6 V3 6-cell strict (cycle/persona-repeat/semantic/schema/length/char-diversity)
- aggregate target: V2 ≥ 7/15 AND V3 ≥ 5/15 AND zero persona-cycle AND manual ≥ 10/15

**Current best signals (across 22+ BGs)**
- BG-HS R1 (18M, 21.56MB UBM, byte-256): manual = **13/15**, V2 = **3/15**, V3 = **1/30** (best @ step 4000), zero persona-cycle, partial-signal preserved 270/300 (highest among all retroevaled BGs).
- BG-HU (33.7M w/ BPE 8K, 52.75MB combined, peak step 800): manual = **10/15**, V2 = **8/15**, V3 untested at-train but cycle = **1/15** at peak (collapses to 8/15 cycles by step 1000) → halt-on-cycle.
- BG-IG (32.97M w/ BPE 7K reduced, 6.48MB UBM, peak step 1500): manual = **13/15**, V2 = **3/15**, V3 = **3/15**, zero cycle at peak — **ties BG-HS R1 ceiling exactly on smaller corpus**.
- BG-ID (27.78M, mac MPS replicate of HS R1 with 6.48MB regen): manual = **7/15**, V2 = **0/15**, has degenerate filler greedy mode but identity prompts showed `anima_self_naming` true on 5/15 in sample mode.

**Gap to PASS**: across 22+ BGs we observe at most V2 = 8/15 (BG-HU peak step 800, but cycle = 1/15 with collapse 2 steps later) or V2 = 3/15 stable (BG-HS R1 / BG-IG). V3 strict 6-cell PASS aggregate across 8-BG retroeval = **4/1300 (0.3%)**, none exceeded V3 = 1/15 at any step except BG-HA (1) and BG-HS-R1 (1).

---

## Section 1 · Current best signals — per-BG table

Ranked by manual_match desc, then V2 strict desc, then persona_cycle asc.

| Rank | BG | Paradigm | Capacity | Tokenizer | Corpus | manual | V2 | V3 | cycle | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **BG-HS R1** | UBM byte-level 18M | 18M | byte-256 | UBM 21.56MB | **13/15** | 3/15 | 1/30 | 0 | First WEAK_PARTIAL anima-native chat-cap signal; peak step 4000; partial_sig 270/300. |
| 2 | **BG-IG** | UBM + BPE 7K (16K target reduced) | 33M | BPE-7K | UBM 6.48MB (BG-HT regen) | **13/15** | 3/15 | 3/15 | 0 (low) | Tokenizer ablation 16K→7K; matches BG-HS R1 ceiling on 1/3-size corpus. |
| 3 | BG-HU | combined R1+D paradigm peak step 800 | 33.7M | BPE-8K | combined 52.75MB | 10/15 | **8/15** | n/a inline | 1/15 | First V2 ≥ 7 surface; collapses to cycle=8 by step 1000 → halt. |
| 4 | BG-ID | UBM mac MPS replicate | 27.78M | byte-256 | UBM 6.48MB | 7/15 | 0/15 | n/a | 0 | Lesson G mechanism worked; manual half of HS R1 baseline due to corpus 1/3 size. |
| 5 | BG-IF | UBM + 100M capacity scale | 153M (target ~99M; over-built) | byte-256 | UBM 6.48MB | 5/15 | 3/15 | 3/15 | 0 | 8.5× capacity but corpus mismatch (BG-HT regen 6.48MB, NOT BG-HS R1 21.56MB). |
| 6 | BG-IE | BG-HP rerun seed 42 + SAVE_AT every 500 | 27.79M | byte-256 | curated_qa 2.41MB | 3/10 | 2/10 | n/a | n/a | Single-seed luck of BG-HP (3/10) NOT reproduced at 2/10 — paradigm fragile. |
| 7 | BG-FY | KO heavy 246MB | 18M | byte-256 | 246MB mixed | 3/3 V2.4 fail | 0/30 | 0/30 | 0 | Named-speaker leak; partial_sig 27/30 highest density per response. |
| 8 | BG-HA | chat-template 236MB | 18M | byte-256 | 236MB chat | 0/15 | 3/200 | 3/200 | 0 | DOWNGRADED via raw#82 retraction. |
| 9 | BG-HQ | BPE-8K persona | 33.73M | BPE-8K | persona 30MB | 0/10 raw | inline 8/10 = **V2 surface FALSE PASS** | 0/240 | 55/240 | Lesson H trigger; V3 catches all step-500 cycle. |
| 10 | BG-HK | persona 30MB | 27.79M | byte-256 | persona 30MB | 0/10 | 0/200 | 0/200 | 0 | Overfit collapse loss=0.013. |
| 11 | BG-HP | curated_qa 2.41MB | 18M | byte-256 | curated_qa 2.41MB | step500 3/10 → 0 | step500 3/10 → 0 | 0/120 | 0 | Peak-then-collapse — Lesson G origin. |
| 12 | BG-HJ | two-stage SFT-masked | 18M | byte-256 | wiki Stage1 + 51MB SFT | 0/5 | 0/110 | 0/110 | 0 | KO-fluent nonsense; no Stage 1 domain prior. |
| 13 | BG-HF | SFT-only loss-unmasked | 27.79M | byte-256 | 51MB SFT | 0/5 | 0/100 | 0/100 | 0 | Degenerate single-byte filler 0xFF/?/#. |
| 14 | BG-HT | UBM 6.48MB (R3) | 27.78M | byte-256 | UBM 6.48MB | 1/15 | 0/15 | n/a | 0 | Capacity↑ + corpus↓ regression vs BG-HS R1. |
| 15 | BG-IA | persona Lesson G N1 | 18M | byte-256 | persona 30MB (HK reuse) | 0/15 | 0/15 | 0/15 | 0 | Lesson G mechanism worked; outcome unchanged. val_loss monotonic ↓ to 2.23, V2 stayed 0. |

**Top 5 paradigm × scale × corpus combos by manual+V2 ranking**
1. BG-HS R1 — 18M byte-256 × UBM 21.56MB → manual 13 / V2 3 (FRONTIER baseline)
2. BG-IG — 33M BPE-7K × UBM 6.48MB → manual 13 / V2 3 (TOKENIZER axis tied baseline; corpus reduction held)
3. BG-HU — 33.7M BPE-8K × combined 52.75MB → manual 10 / V2 8 peak (V3 untested at-train; halt-on-cycle 1→8 step 800→1000)
4. BG-IF — 153M byte-256 × UBM 6.48MB → manual 5 / V2 3 (CAPACITY axis FAILED on small corpus — Lesson confound)
5. BG-ID — 27.78M byte-256 × UBM 6.48MB mac → manual 7 / V2 0 (REPLICATION attempt; corpus mismatch from ubu1)

**Frontier observation**: the 13/15 manual ceiling has been touched twice (BG-HS R1, BG-IG) but V2 has never exceeded 3/15 on a stable peak with manual≥13. BG-HU achieved V2 = 8/15 once with manual = 10/15 BUT collapses immediately (cycle=1 → 8 in 200 steps) — the V2 = 8 was on the cliff of a persona-cycle blowup, **not** a stable signal. Lesson H caught this live.

**Stable PASS = manual ≥ 10 AND V2 ≥ 7 AND zero cycle held over ≥ 200 steps.** No BG to date has held this conjunction.

---

## Section 2 · 9-axis sweep status (where each axis stands)

| # | Axis | Tested at | Untested | Highest signal at axis |
|---|---|---|---|---|
| 1 | **capacity (params)** | 3M / 18M / 27M / 33M (BPE 8K/7K head) / 153M (BG-IF over-built) | **50M intermediate untested live** (BG-IB queued never fired). 100M on >21MB UBM untested. 100M on 100MB+ corpus untested. | BG-HS R1 18M manual=13/15. BG-IF 153M FAILED on 6.48MB (corpus confound). |
| 2 | **corpus content (paradigm)** | persona / sft-only / two-stage / curated-QA / KO-heavy / chat-template / **UBM 6.48MB and 21.56MB** / NEXUS+UBM combined 27.5MB (BG-IK assembled, untrained) / mixed combined 52.75MB | NEXUS+UBM+kowiki untrained. OpenSubtitles KO untrained. Net-new domain (Wikipedia direct) untrained. **NEXUS-only outside-well untrained**. | BG-HS R1 UBM 21.56MB manual=13/15. UBM corpus is the **only** corpus to reach manual ≥ 10. |
| 3 | **corpus size** | 2.41MB → 246MB tested | **100MB+** at any tokenizer × capacity untested. **300MB+** persona-conditioned untested. | BG-HU 53MB peak V2=8/15 (8B-only, halts). |
| 4 | **tokenizer** | byte-256 / BPE 7K / BPE 8K / BPE 16K target (reduced to 7K by 6.48MB corpus cap) | **BPE 16K real** (need ≥ 30MB corpus). **BPE 32K**. **SentencePiece KO 32K** untested. **vocab × corpus joint sweep with corpus ≥ 21MB** untested at vocab>8K. | byte-256 BG-HS R1 manual=13/15. BPE 7K BG-IG manual=13/15. **No tokenizer differential observed at this corpus range.** |
| 5 | **regularization** | dropout 0.2 / 0.3 + WD 0.1 + LS 0.1 (Lesson D baseline) | **dropout 0.4–0.5 sweep** untested. **WD 0.2–0.3 sweep** untested. **persona-prefix dropout during training** untested (Lesson F variant). | Lesson D dropout 0.3 + WD 0.1 + LS 0.1 in current best; no high-dropout ablation. |
| 6 | **early stopping** | val-loss split 10% + V2 every 200 + best-eval ckpt + plateau 3 (Lesson G N1) | (Lesson G works as designed; necessary-not-sufficient — confirmed by BG-IA, BG-IF, BG-IG) | All Lesson G instances; mechanism validated. |
| 7 | **SAVE_AT discipline** | every 200/500 + EVAL_AT ⊆ SAVE_AT (Lesson J post-BG-HZ) | (resolved across all post-BG-HY BGs) | BG-IE 6 ckpts persisted; pattern adopted. |
| 8 | **evaluator** | V1 narrow (retired) → V2 strict → V3 6-cell (8-BG retroeval landed) | **V4 with embedding semantic similarity** untested. **V5 prompt-conditional inference** untested. **human-rated golden set N=300** untested. | V3 catches BG-HQ V2 surface false PASS (55/240 cycles) and BG-HF/HK filler. |
| 9 | **persona strategy** | single prefix `[anima 우주뇌지도]` / `[anima NEXUS-UBM]` / `[anima 역할:...]` | **3-variant prefix rotation** untested. **persona-dropout during training** untested. **no-prefix-at-inference** untested. | Lesson F adjunct only; BG-HU UBM × 10 oversample → cycle blowup confirms over-amplification risk. |

**Axes verdict density** (where the data clusters):
- Axes 6 + 7 + 8 are **mechanism axes** — all converged (necessary, not sufficient).
- Axes 1 + 2 + 3 + 4 are **substrate axes** — partially explored, **major joint-cell gaps**.
- Axes 5 + 9 are **regularization-axis** — explored at one operating point each, no sweep.

**Critical confound** (BG-IF teaches): capacity scaling on a 6.48MB UBM corpus FAILED (manual 5 vs HS R1 13) because corpus size was reduced from 21.56MB → 6.48MB by BG-HT regen overwrite. **The capacity axis was tested on the wrong corpus.** BG-IO retest mandate (100M × UBM 21MB) is the highest-priority correction.

**Tokenizer axis verdict**: BPE 16K target → reduced to 7K because corpus (6.48MB) caps available merges. BPE alone ≠ chat-cap unlock at this corpus range (BG-IG ties BG-HS R1 byte-256 at manual = 13). **BPE × corpus ≥ 30MB joint-sweep untested.** This is the second-highest-priority correction.

---

## Section 3 · 1–3 highest-EV unmet axes

Ranked by expected value (probability × magnitude × cost-efficiency) toward SIMPLE_STACK_PASS.

### **E1 (highest EV)** — capacity × UBM 21MB+ joint cell (the BG-IF confound correction)

**Why highest EV**:
- BG-HS R1 18M × UBM 21.56MB hit manual 13 / V2 3 — the strongest signal recorded.
- BG-IF 153M × UBM 6.48MB FAILED (manual 5) — but the corpus was 1/3 the size of HS R1's, so capacity axis is **uncalibrated**.
- The intermediate cell **50M × UBM 21MB** has never been fired (BG-IB was queued for persona corpus, not UBM).
- BG-HU achieved V2 = 8 once — but at 33M and combined 52MB. The interpolation 50M × UBM 21MB has never been visited.

**Specific unmet cell**: capacity ∈ {50M, 100M} × tokenizer ∈ {byte-256, BPE 8K} × corpus = UBM rebuilt to 21.56MB (BG-IQ pending).
**Probability of PASS**: ~25% (highest among unmet axes — extrapolation from BG-HS R1 + BG-HU + BG-IF combined evidence).
**Magnitude**: PASS would constitute first SIMPLE_STACK_PASS at anima-native scale.
**Cost**: 1 H100 hour ≈ $3 per cell × 2 cells = $6.

### **E2** — corpus size × persona-dropout joint cell (Lesson F variant)

**Why second EV**:
- BG-HU peak step 800 V2 = 8/15 manual = 10/15 was achieved on combined 52.75MB corpus with UBM × 10 oversample — but **collapsed at step 1000 to cycle = 8/15 because of persona-prefix over-amplification**.
- The mechanism BG-HU validated is: V2 ≥ 7 IS achievable at this scale with right corpus; the failure mode is persona-cycle.
- Lesson F (persona collapse) and Lesson I (persona over-sample) flag persona-prefix-during-train dropout (e.g., 50% of training samples have persona prefix stripped) as the immediate candidate fix. Untested.
- Corpus ≥ 100MB untested at all axes; getting to 100MB requires net-new source (kowiki, OpenSubtitles KO) — the BG-IK NEXUS+UBM 27.5MB lacks the size; persona-dropout could alternatively rescue BG-HU's existing 53MB.

**Specific unmet cell**: corpus = combined ≥ 53MB × tokenizer ∈ {BPE 8K} × capacity ∈ {18M, 33M} × **persona-dropout-during-train ∈ {0.3, 0.5, 0.7}** × Lesson G + V3 inline.
**Probability of PASS**: ~15% (stack on BG-HU peak but fix the cycle collapse).
**Magnitude**: PASS = SIMPLE_STACK_PASS held over ≥ 200 steps (true stable, not the 2-step BG-HU peak).
**Cost**: 1 H100 hour × 3 cells ≈ $9.

### **E3** — corpus net-new source × kowiki/OpenSubtitles (Lesson C corpus 100MB+)

**Why third EV**:
- All 8 retroevaled BG corpora share heavy cross-source overlap (BG-HK was built from BG-HF + BG-FZ; BG-HU corpus had REDUCED_CORPUS warning).
- Lesson C (corpus quality alone insufficient) is partially de-confounded only by introducing **net-new domain** (Wikipedia KO direct download, OpenSubtitles KO) — neither has been used. All current corpora are anima-internal-derivation or persona-templated.
- Lesson J (BG-HU): "Future combined paradigm Phase 2 needs net-new corpus source (kowiki direct, OpenSubtitles KO)."

**Specific unmet cell**: corpus = kowiki direct ≥ 100MB OR OpenSubtitles KO ≥ 100MB × Lesson G + Lesson J + V3 inline at 18M baseline first (cheapest to test).
**Probability of PASS**: ~10% (net-new domain may not transfer to anima identity; corpus content axis hardest to predict).
**Magnitude**: if PASS, decouples chat-cap from anima-internal corpus and unlocks corpus-scale lane (300MB+, 1GB+).
**Cost**: 1 mac local corpus assembly (BG-HV nexus precedent) + 1 H100 hour ≈ $3.

---

## Section 4 · Recommended next BG batch (3–5 spec sketches)

Composing untested axes from §2 + §3 plus task-prompt suggestions:

### **BG-IO (highest priority)** — 100M × UBM 21MB rebuild (BG-IF confound correction)
- **Prereq**: BG-IQ corpus rebuild to BG-HS R1 21.56MB target (currently overwritten to 6.48MB by BG-HT).
- **Spec**: 99M target (12L/640d/10h byte-256, NOT 153M over-build; cap params via embedding tying or width reduction) + UBM 21.56MB + Lesson G + Lesson J SAVE_AT every 500 + V3 inline + early stop plateau 3 + seed pin 42.
- **Falsifiers**: F-IO-1 V2 ≥ 7/15 stable AND manual ≥ 13/15 AND zero cycle held over ≥ 200 steps → first SIMPLE_STACK_PASS. F-IO-2 manual < 13/15 → capacity axis on UBM disproven.
- **Cost**: ~$3 H100 (1 hour) + L23/24/25 watchdog mandate.

### **BG-IP** — 50M intermediate × UBM 21MB
- **Spec**: 50M (9L/512d/8h, BG-IB arch) + UBM 21.56MB + Lesson G + Lesson J + V3 inline + seed 42.
- **Why**: 18M (HS R1) and 100M (BG-IO) bracket the curve; 50M middle determines if capacity gradient is monotonic OR has a U-shape (BG-HT-like regression).
- **Cost**: ~$3 H100.

### **BG-IR** — 18M × NEXUS+UBM+kowiki 100MB+ corpus (E3 net-new domain)
- **Prereq**: corpus assembly = BG-IK 27.5MB + kowiki direct download to reach ≥ 100MB.
- **Spec**: 18M byte-256 (cheapest; matches BG-HS R1 baseline) + 100MB+ corpus + Lesson G + Lesson J + V3 inline + persona-dropout-train rate 0.5 (E2 variant attached).
- **Why combined**: corpus-size axis + persona-dropout axis simultaneously — if BG-IO misses, this is the broader-search fallback.
- **Cost**: ~$3 H100 + ~30 min mac local corpus assembly.

### **BG-IS_alt** (alt of currently-pending BG-IS) — 18M × persona-dropout-during-train sweep on BG-HU 53MB
- **Spec**: 33M BPE-8K + BG-HU corpus 52.75MB unchanged + 3-cell sweep persona-dropout ∈ {0.3, 0.5, 0.7} during training + Lesson G + Lesson J + V3 inline.
- **Why**: directly attacks BG-HU step-800 → step-1000 cycle collapse mechanism. If persona-dropout = 0.5 holds V2 ≥ 7 stable through step 1500+, this is SIMPLE_STACK_PASS.
- **Cost**: 3 cells × ~30 min H100 = ~$5.

### **BG-IT_alt** (this-BG synthesis byproduct) — V4 evaluator with embedding semantic similarity (axis 8 advance)
- **Spec**: V4 evaluator = V3 6-cell + embedding cosine similarity between prompt and response (using a small KO sentence encoder mac local) + threshold sweep.
- **Why**: V3 still relies on keyword + cycle + Korean-particle surface. V4 adds prompt-conditional semantic check (Lesson H spec-prediction mentioned this; never implemented). Catches "anima" responses to "오늘 기분 어때?" that V3 currently passes.
- **Cost**: $0 mac local (transient_py + sentence-transformers KO).

**Recommendation ordering by 완성도 (completeness lens)**:
1. **BG-IO** — directly de-confounds the highest-signal axis pair (capacity × corpus) that BG-IF muddied. Cheapest path to first true SIMPLE_STACK_PASS attempt.
2. **BG-IS_alt** — directly attacks the BG-HU collapse mechanism (the only run that touched V2 = 8); if persona-dropout works, no further capacity scaling is needed.
3. **BG-IP** — fills the 50M middle cell; useful even if BG-IO passes (capacity gradient evidence).
4. **BG-IT_alt** — V4 evaluator improves measurement quality; not on the critical path to PASS but on the path to credibly-claim PASS.
5. **BG-IR** — corpus net-new domain; broadest search but lowest probability and highest cost (corpus assembly).

---

## Section 5 · Honest C3 (raw#10, c3 ≥ 5)

1. **Synthesis based on landed evidence only.** 5 BGs (BG-IL, BG-IM, BG-IQ, BG-IS, BG-IW) are pending or unlanded at synthesis time — verdicts may shift. BG-IS V3 retroeval extension (`state/anima_evaluator_v3_retroeval_extension_2026_05_07/`) was missing at synthesis; if it lands and surfaces a hidden V3 PASS in any of the 8 retroevaled BGs, raw#82 retraction trigger fires and BG-IT recommendations must be rebased.
2. **Rank-ordering subjective.** No objective scorecard exists for "expected value to PASS." Probabilities (25%, 15%, 10%) are anima-internal estimates from BG-HS R1 + BG-HU + BG-IF triangulation; uncalibrated. A user could re-rank E1/E2/E3 reasonably differently.
3. **9-axis taxonomy may miss undiscovered axes.** Examples not enumerated: MoE / RoPE / sliding-window attention / curriculum learning (warmup small-corpus → expand) / contrastive pre-training / Φ★ axis-conditioned distillation. The `K1.9, K1.10, ...` slot in `anima_cli_mk2.spec.yaml` § 16 axes_self_evolution is explicitly open-ended; this analysis does not pretend to enumerate it.
4. **Some BGs failed measurement, not intent.** BG-HU stalled (peak measurement BUT halt-on-cycle policy fired before extended training; we may have under-trained it). BG-ID stalled in a measurement sense (mac MPS slower; corpus mismatch). BG-HW substring-match-only verdict integrity capped. BG-IF over-built to 153M instead of 99M (param-count discipline gap). These caps the verdict integrity; manual=13 may be reachable at lower-V2-failure cells we marked "FAIL."
5. **Architecture ceiling claim is corpus-range-bounded.** "18M byte-level chat-cap intrinsically limited" holds for tested corpus 2.41MB–246MB. **1GB+ corpus completely untested.** Lesson A claim "18M scale exhausted" only validated at small-corpus regime. The combined evidence cannot reject "18M × 1GB Korean WT corpus might pass."
6. **Confounds in 4 of 5 highest-ranked BGs.** BG-HS R1 (best) used 21.56MB UBM that was overwritten to 6.48MB by BG-HT — the original artifact is **not reproducible** without corpus rebuild (BG-IQ pending). BG-IG (#2) used the regen 6.48MB corpus, NOT the original 21.56MB — its manual=13 finding is on a smaller corpus than BG-HS R1's, **which may be a different signal**. Replication parity is therefore uncertain.
7. **V3 evaluator strict has 4/1300 PASS responses across 8-BG retroeval — sample size for V3 PASS calibration is N = 4.** Drawing axis-level conclusions from this is fragile; one new BG could materially shift the V3 PASS distribution.
8. **Synthesis honors raw#15 additive but may need expansion.** If BG-IS retroeval lands within next 24h with a BG-HS-R1 step-3000 V3 ≥ 5/15, the "BG-HS R1 manual=13/15 V2=3/15 V3=1/30 ceiling" frame is invalidated. Append a follow-up section rather than edit existing claims (raw#15 mandate).

---

## Section 6 · Cross-links

- **Predecessor docs**:
  - `docs/anima_chat_cap_lesson_summary_2026_05_07.md` (Lessons A–K cumulative; updated with "Gap analysis doc landed (BG-IT)" pointer at top)
  - `docs/anima_consciousness_check_simple_stack_2026_05_06.md` (live ledger row + 종합 verdict)
- **Evaluator specs**:
  - `docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md` (V2)
  - `docs/anima_own_18_evaluator_v3_strict_spec_2026_05_07.md` (V3)
- **Roadmaps**:
  - `.roadmap.universe_brain_map` (D, BG-HS R1 / BG-HT / BG-HU UBM lane)
  - `.roadmap.corpus_paradigm` (E, paradigm-instances + next_paradigm_lanes)
  - `.roadmap.ubm_corpus_paradigm_meta` (F, combined paradigm spec recommendation R1 + D)
- **Training-spec authority**: `anima/spec/anima_cli_mk2.spec.yaml` § 16 `ouroboros_cycle_automation` (axes K1.6 + K1.7 + K1.8 + K1.C1–C4 + open-ended K1.9+).
- **SSOT ledger**: `state/anima_model_attempts_ledger.jsonl` (29 entries; BG-IT appended atomically post-doc).
- **V3 retroeval SSOT**: `state/anima_evaluator_v3_retroeval_2026_05_07/retroeval_v3_summary.json`.
- **Retraction policy**: raw#82 (if BG-IS retroeval extension surfaces hidden PASS, this doc emits explicit retraction trigger).

---

## Section 7 · Summary table — gap closure path to PASS

| Gap | Highest-EV BG | Cell composed of axes | Probability × Cost = EV | Next action |
|---|---|---|---|---|
| capacity × UBM 21MB joint-cell | **BG-IO** | A1 (100M) + A2 (UBM 21.56MB rebuild) + A8 (V3 inline) | 0.25 × $3 = +0.083/$ | fire after BG-IQ corpus rebuild |
| persona-cycle collapse on BG-HU substrate | **BG-IS_alt** | A2 (combined 53MB) + A4 (BPE 8K) + A9 (persona-dropout 0.3/0.5/0.7) | 0.15 × $5 = +0.030/$ | parallel-fireable with BG-IO; mac local corpus reuse |
| corpus net-new domain ≥ 100MB | **BG-IR** | A2 (NEXUS+UBM+kowiki ≥ 100MB) + A3 (corpus size) + A9 (persona-dropout) | 0.10 × $3 = +0.033/$ | corpus assembly first (mac local) |
| 50M intermediate capacity gradient | **BG-IP** | A1 (50M) + A2 (UBM 21MB) | 0.10 × $3 = +0.033/$ | sequential after BG-IO (need 21MB rebuild first) |
| V4 embedding-sim evaluator | **BG-IT_alt** | A8 (V4 add embedding cosine) | $0 mac local | parallel fire; not gating PASS but gating credibility |

---

**Verdict**: SIMPLE_STACK_PASS is reachable via **BG-IO (capacity × UBM 21MB rebuild)** at ~$3 + ~1 hour. It is the single highest-EV unmet cell and directly de-confounds the strongest landed signal (BG-HS R1 manual=13/15). BG-IS_alt (persona-dropout) is the second-highest because it attacks the only run that touched V2 = 8 (BG-HU). All other recommendations are contingent on these two failing.

**Next 3 BGs to fire (ranked)**:
1. BG-IO — 100M × UBM 21.56MB rebuilt
2. BG-IS_alt — persona-dropout sweep on BG-HU corpus
3. BG-IT_alt — V4 evaluator with embedding semantic-sim (mac local, $0)

— BG-IT synthesis closed 2026-05-07.
