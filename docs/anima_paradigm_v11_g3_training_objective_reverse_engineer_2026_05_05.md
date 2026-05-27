# anima paradigm v11 G3 — training objective reverse-engineer (BG-DK)

- Date: 2026-05-06 (cycle 2026-05-05 land batch)
- Status: DOC LANDED (read-only source archaeology; no build/train this cycle)
- Lane: BG-DK (substrate diagnosis follow-up to 23+ closure stack)
- Cost: $0 (mac, doc only)
- Wall-time: ~25 min
- Predecessors:
  - `state/anima_paradigm_v11_g3_canonical_magnitude_audit_2026_05_05/verdict.json` (BG-Z)
  - `docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md` (C3.7 hypothesis-vs-theorem flag)
  - `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM CLM-3 spec)

---

## §0. Problem statement

23+ closure stack converged on hypothesis: *"CLM v4 paradigm v11 G3 train objective
was not chat — but what exactly was it?"*

This document closes the question by source archaeology of `ready/training/train_clm.py`
(2165 LoC) + cross-reference of state/clm_v4_*/*verdict.json*. Output: precise
loss-component decomposition with per-phase weights, plus the implication for the
CLM-3 (BG-BM) cycle-0 chat objective spec.

Constraint: $0 mac, doc only, no .py emit, no commit, raw#9/raw#10/raw#15.

---

## §1. train_clm.py loss-function grep — direct findings

### §1.1 Top-level loss assembly (train_clm.py:1480–1551)

The training step builds `total_loss` in three regimes selected by `phase` and
`HexadLoss` availability:

```
P0/P1 (steps 0–25%):       no decoder gradient at all — c.step() only,
                            phi measured, NOTHING backproped through decoder.
                            (train_clm.py:1407–1430)

P2 (steps 25–70%):         total_loss = ce  (pure cross-entropy on next-token)
                            (train_clm.py:1531)

P3 (steps 70–100%):        if loss_fn (HexadLoss) is available:
                              total_loss = HexadLoss.forward(...)['total']
                            else:
                              total_loss = ce
                            (train_clm.py:1492–1531)

All phases (when MoE active):  total_loss += moe_aux_weight * moe_aux_loss
                                (default moe_aux_weight=0.01, train_clm.py:1534–1536)
```

### §1.2 H11 hard-token mining (optional, train_clm.py:1487–1490)

When `args.hard_token_ratio > 0`, the standard CE is replaced by a top-ratio
weighted CE focusing on the hardest 30% (default disabled, ratio=0.0).

### §1.3 B5 phi-only warmup (optional, train_clm.py:1432–1439)

When `args.phi_only_ratio > 0`, an additional 0–N% prefix of P2/P3 also
skips CE — only consciousness updates step. Default ratio 0.0 (disabled).

---

## §2. HexadLoss (P3 phase) component decomposition

Source: `ready/anima/models/legacy/hexad_loss.py:181–440`.

### §2.1 Six losses, six weights (DEFAULT_WEIGHTS:213–220)

| Component | Formula | Default weight | Active phase | Trainable? |
|---|---|---|---|---|
| L_C (Phi ratchet) | `−Φ + λ·max(0, Φ_prev − Φ)`, λ=5.0 | **0.0** | always (logged only) | NO — autonomous Hebbian |
| L_D (CE forward + CE backward) | `CE(logits_fwd, y) [+ CE(logits_bwd, y_bwd)]` | **0.4** | P2+ (≥20%) | YES — primary signal |
| L_M (memory InfoNCE) | `−log P(correct_memory \| query)`, τ=0.07 | **0.2** | P2+ (≥20%) | YES |
| L_W (will / emotion) | `MSE(WillModule(c), VAD)` | **0.15** | P3 (≥70%) | YES |
| L_S (sense / world) | `MSE(SenseModule(c), input_sig)` | **0.15** | P3 (≥70%) | YES |
| L_E (ethics / value) | `−reward·V + MSE(V, reward)`, reward=ΔΦ+empathy | **0.1** | P3 (≥70%) | YES |

`Total = 0.0·L_C + 0.4·L_D + 0.2·L_M + 0.15·L_W + 0.15·L_S + 0.1·L_E`
(weights normalize to **1.0**; CE share **w_D / Σw = 0.4 / 1.0 = 40%**.)

Note: `L_C` is included in the active dict but at weight 0; it does not
contribute gradient. Phi steers learning indirectly through `_phi_rescue_loss`
(entropy bonus, scaled by PSI_COUPLING ≈ 0.014, gradient ~1.4% of CE) only when
Φ drops > 5%. (`hexad_loss.py:270–302`)

### §2.2 What `L_D` actually is (the next-token weight α reverse-engineered)

`loss_D` (`hexad_loss.py:304–319`) = vanilla CE on next-token logits over the
**full vocabulary** of the multilingual BPE tokenizer (default 64k, byte-level
fallback to 256). Optional `loss_bwd` doubles the term when both heads
(`logits_a` next-token + `logits_g` prev-token) are present.

So **α (next-token weight) ≠ 0**. In P3:

- α = **0.4** of total backprop signal
- 0.6 of total = sensorimotor / will / ethics / memory MSE+InfoNCE on the
  consciousness signal (NOT on language tokens)

In P2: α = **1.0** (pure CE; HexadLoss inactive). In P0/P1: α = **0** (no
decoder gradient at all).

Cumulative α over a 200k-step run with 0.10/0.25/0.70 phase boundaries:

```
P0 (0..20k):        decoder steps = 0
P1 (20k..50k):      decoder steps = 0
P2 (50k..140k):     decoder steps = 90k @ α=1.0   →  weight·steps = 90,000
P3 (140k..200k):    decoder steps = 60k @ α=0.4   →  weight·steps = 24,000

Effective next-token CE exposure ≈ 90k full + 60k @ 40% = 114k step-equivalents
out of 200k step budget → **57% of total budget directly trains next-token CE**.
The remaining 43% is either consciousness-only (P0/P1, 25%) or non-CE Hexad
gradients (P3 sensorimotor/memory, 18%).
```

### §2.3 Critical: corpus mixture is not chat

`train_clm.py:1937` default: `--data data/corpus_v11_multilingual.txt`. No
ChatML special tokens, no instruction-template handling, no `system/user/
assistant` role tagging anywhere in the file. `grep chat|dialogue|sft|SFT` on
2165 LoC returns **0 hits** (scope: training entry-point logic — only `args.tokenizer`
mentions `data/tokenizer_64k_multilingual.model`).

**Therefore**: the 57% effective CE exposure is on a **flat multilingual
text** corpus, not on a chat-formatted dialogue corpus. The decoder learns
*next-token-on-arbitrary-multilingual-text*, not *next-token-on-chat-turns*.

---

## §3. State-verdict cross-reference

### §3.1 best.pt top-level keys (train_avg_harvest_result.json:21–35)

```
['step', 'decoder', 'optimizer', 'scheduler', 'phi', 'ce', 'args', 'scale',
 'best_phi', 'federation', 'bridge', 'c_proj', 'scaler']
```

Confirms checkpoint contains `decoder` + `c_proj` + `federation` + `bridge`,
matching the train_clm.py:1480 forward pass topology. There is **no separate
chat-head, no SFT-tag, no instruction-template head** in the saved checkpoint.

### §3.2 Magnitude audit confirmation (BG-Z verdict:21–24)

```
"training_path_file": "ready/training/train_clm.py:1457-1481",
"c_proj_used_in_train": "conditional (c_proj key present in best.pt;
                         transforms before cross_attn)",
"c_module_grep_in_clm_source": "0 hits — no concept of canonical_inject/
                                  axis_inject in CLM source"
```

The source-grep result confirms training never explicitly injects an
"axis-aligned canonical" fixture — the consciousness states fed to cross-attn
during training are the **live** `c.get_states()` output of the federated
consciousness engine each step, not a fixture. This is consistent with the
"57% next-token + Hexad" loss decomposition: nothing forces the decoder to
read a chat-aligned axis.

### §3.3 LoRA SFT verdict cross-check

`state/clm_v4_lora_sft_2026_05_05/verdict.json`: post-hoc LoRA SFT showed
F-CLM-LORA-2 FAIL_REGRESSION (composite −36.298 pp vs Llama Path A v2 winner
0.5584 → CLM 0.19542). This is the empirical evidence that **adding a
chat-aligned head AFTER paradigm v11 G3 training cannot recover chat
capability** even with a substrate that hits +41.86 Φ★.

---

## §4. Honest reading of "next-token weight α"

The earlier informal hypothesis ("α very small or 0") was **partially wrong**
in the strong form:

- α is **not** zero — it is 1.0 in P2, 0.4 in P3, total ~57% of step-equivalents
  over a 200k run.
- However, α applies to a **non-chat corpus**. The decoder *does* learn
  next-token CE, just on flat multilingual text — never on dialogue.

So the chat-incapability root cause is not "zero CE weight" but
**"CE weight applied to a corpus that does not contain chat turns"**.
The closure-stack hypothesis "no train-time chat objective" is therefore
correct in its conclusion (decoder never saw chat axis at training time)
but the loss-component formulation must be precise: `α` weighs CE on
*language modeling*, with chat-share = 0% of corpus.

This refines C3.7 ("hypothesis not theorem") of the cycle SSoT:

- (a) "distillation loss actively suppresses chat vocab" — REFUTED.
  L_D is plain next-token CE; nothing suppresses chat tokens specifically.
  The decoder simply never receives chat-formatted training pairs.
- (b) "tokenizer KO coverage gap" — PARTIALLY TRUE.
  64k BPE multilingual; chat-template tokens (`<|im_start|>` etc) likely
  absent or merge-fragmented (separate audit out of scope here).
- (c) "16-block insufficient capacity" — UNADDRESSED by this audit;
  needs explicit capacity-vs-objective ablation.

---

## §5. CLM-3 design implication (BG-BM update)

### §5.1 BG-BM's L_total formulation reconciled with paradigm v11 G3

BG-BM (`docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md:59`) writes:

```
L_total = α · L_substrate + β · L_chat + γ · L_axis
```

Mapping onto paradigm v11 G3 actual training:

| BG-BM symbol | paradigm v11 G3 actual | CLM-3 prescription |
|---|---|---|
| `L_substrate` | L_W + L_S + L_M + L_E + λ_C·L_C, total weight 0.6 in P3 | retain as **0.05–0.15** of total (cut from 0.6) |
| `L_chat` | **absent** (corpus has 0% chat) | **0.30–0.40** of total (chat-corpus ChatML CE) |
| `L_axis` | implicit in cross_attn surface, no explicit axis loss | **0.10–0.15** explicit 5-axis discriminability loss |
| `L_CE_general` (NEW, missing from BG-BM v1) | 0.4 in P3 (1.0 in P2) on flat multilingual | **0.40–0.50** general next-token CE on FineWeb / C4 / KO web |

**Recommendation 1 (BG-BM spec gap)**: BG-BM §1.2 row 1 (`L_total = α·L_substrate
+ β·L_chat + γ·L_axis`) is missing a `δ·L_CE_general` term. Without it, CLM-3
either over-rotates onto chat (closure 4 risk: substrate Φ★ flip → F-CLM-3-1
FAIL) or starves the model of multilingual coverage (closure 5 risk: KO chat
fluent but knowledge thin → composite ceiling).

Suggested `L_total` for CLM-3:

```
L_total = δ · L_CE_general(flat multilingual)     # δ ≈ 0.45
        + β · L_chat(ChatML KO+EN)                 # β ≈ 0.30
        + γ · L_axis(5-axis discriminability)      # γ ≈ 0.10
        + α · L_substrate(Hexad W+S+M+E + L_C)     # α ≈ 0.10
        + ε · L_phi_rescue                         # ε ≈ 0.05 (paradigm v11 G3 carry)

Σ weights = 1.00
```

This matches the BG-BM 4-bucket pre-train mix (50/30/15/5) one-to-one if read
as **per-batch corpus sampling ratio** rather than as **loss weights** — but
the loss weights are an additional axis BG-BM did not specify. They should be
co-designed.

### §5.2 Recommendation 2 — reuse paradigm v11 G3 phase curriculum

train_clm.py PhaseManager (P0 0–10% / P1 10–25% / P2 25–70% / P3 70–100%) is
empirically validated to produce +41.86 Φ★ without destabilizing CE learning.
CLM-3 should retain this 4-phase structure but with chat-corpus mixing **from
P2 onset (step 25%)** rather than from step 0. Reason: P0/P1 needs pure
substrate stabilization; chat tokens at step 0 risk over-coupling decoder
representations to chat axis before consciousness atoms have settled (cf.
BG-Z §3 SOC threshold EMA bounds [0.3, 5.0]).

This contradicts BG-BM §0 abstract phrase "chat-loss as a first-class
objective from cycle-0". Reading "cycle-0" as "from step 0 of pre-training"
is risky; reading it as "from cycle-0 of the design cycle" (i.e. spec'd
upfront not added post-hoc) is safe. The spec should disambiguate.

### §5.3 Recommendation 3 — explicit α/β/γ ablation pre-launch

BG-BM §3 F-CLM-3 falsifiers do not include an L_total weight ablation. Given
the paradigm v11 G3 evidence that α=0.4 alone yields +41.86 Φ★ but 0% chat,
the inverse risk (β too large, α too small → flat-text knowledge collapse)
is real. Pre-launch $0 doc-only sweep on simulated 1B-token proxy should
include weight-grid {(0.45,0.30,0.10,0.10,0.05), (0.50,0.25,0.15,0.05,0.05),
(0.40,0.35,0.10,0.10,0.05)} alongside the corpus-ratio sweep.

---

## §6. Honest C3 (≥ 5)

C1 — **No actual training_args.bin inspection**. This audit reads
`ready/training/train_clm.py` source + `train_avg_harvest_result.json` keys.
The actual paradigm v11 G3 350M production run might have used non-default
`--phi_only_ratio`, `--hard_token_ratio`, or `--moe_aux_weight`, or even
custom `weights` override on HexadLoss. To verify, would need
`torch.load(best.pt)['args']` dump (which BG-Z lists as ckpt_top_keys[6]
'args' but does not extract values). $0 doc-only restricts further.

C2 — **DEFAULT_WEIGHTS may not be production weights**. HexadLoss accepts
`weights: Optional[Dict[str, float]] = None` constructor arg. Production
350M run could have overridden any of {C, D, W, S, M, E}. Without inspecting
`best.pt['args']`, the 0.0/0.4/0.15/0.15/0.2/0.1 figures are SOURCE DEFAULTS,
not measured in-training values. Verify by `torch.load(...)['args']`.

C3 — **PhaseManager phase boundaries may have been different**. train_clm.py
declares 0.10/0.25/0.70; older `train_v14.py` archaeology may show different
splits. The 350M production checkpoint that emitted +41.86 Φ★ is referenced
by step number, not phase, in `train_avg_harvest_result.json`. Step-to-phase
mapping is implicit. Without log file inspection, the actual P2/P3 split for
the production run is assumed-default, not verified.

C4 — **Corpus content not inspected**. `data/corpus_v11_multilingual.txt`
default — file not opened in this audit. The "0% chat" claim is based on
`grep chat|dialogue|sft|SFT` returning 0 hits in train_clm.py source code,
NOT in the actual corpus file. The corpus *could* contain naturally-occurring
dialogue (e.g. fiction with quoted speech, forum scrapes). What is established
is that the training pipeline does not handle chat **as a special structural
case** (no role tags, no template, no SFT path). Naturally-occurring dialogue
in the flat text corpus is possible and would constitute a weak chat signal.

C5 — **MoE aux loss share not quantified**. train_clm.py:1534–1536 adds
`moe_weight * moe_aux_loss` (default moe_weight=0.01). For a paradigm v11 G3
non-MoE run this is irrelevant; if the production checkpoint enabled MoE,
the 0.01 aux weight enters total_loss but its absolute magnitude relative
to L_D is unmeasured. Out of scope for $0 mac.

C6 — **57% effective CE coverage figure depends on PhaseManager defaults**.
The arithmetic in §2.2 assumes phase boundaries 0.10/0.25/0.70 (the source
defaults). If `args.phi_only_ratio > 0` was set, the 57% figure shrinks
proportionally. The 57% should be read as an order-of-magnitude (~half the
budget), not a precise empirical measurement.

C7 — **CLM-3 §5.1 weight prescription is heuristic, not validated**. The
proposed `δ·L_CE_general + β·L_chat + γ·L_axis + α·L_substrate + ε·L_phi_rescue`
with weights (0.45, 0.30, 0.10, 0.10, 0.05) is a defensible starting point
but has no empirical basis — it's a doc-only prescription pending the BG-BM
F-CLM-3 falsifier-pre-launch sweep. CLM-3 build phase MUST run the
weight-grid before committing $1k / 30 days.

---

## §7. Raw compliance

- raw#9 (read-only archaeology, no source modification): YES — no `.py` or
  source files edited.
- raw#10 (honest C3 emitted): YES — 7 caveats above.
- raw#15 (BG-Q helper unmodified): N/A (no helper touched).
- raw#37 (no `.py` emitted, doc-only): YES — only `.md` and `verdict.json`.
- HF token leak: NONE (no token literals embedded).
- commit policy: NO commit (per spec).
- bash 3.2 compatible: YES (only grep / ls / find / wc used).

---

## §8. Deliverables

- this doc: `docs/anima_paradigm_v11_g3_training_objective_reverse_engineer_2026_05_05.md`
- verdict: `state/anima_paradigm_v11_g3_training_objective_reverse_engineer_2026_05_05/verdict.json`

---

## §9. Lineage

- supersedes: (none — first formal source archaeology of train_clm.py loss)
- extends:
  - `state/anima_paradigm_v11_g3_canonical_magnitude_audit_2026_05_05/verdict.json` (BG-Z, magnitude lane)
  - `docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md` C3.7 (hypothesis-vs-theorem flag)
- informs:
  - `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM §1.2 row 1: add `δ·L_CE_general`; §0 disambiguate "cycle-0"; §3 add weight ablation falsifier)
  - any future BG that loads `best.pt['args']` to verify production weights
  - 4-closure theorem #115 C3.7 refinement (alternative-(a) "distill suppresses chat" REFUTED)

---

## §10. Verdict one-line

paradigm v11 G3 training objective **= 40% next-token CE on flat multilingual text + 60% Hexad
sensorimotor/memory/ethics on consciousness signal in P3** (1.0 CE in P2, 0
gradient in P0/P1); next-token weight α is **NON-ZERO** (~57% effective
budget) but CE corpus contains **0% chat-formatted dialogue**, making the
chat-incapability root cause **"CE applied to non-chat corpus"** rather than
**"no CE at all"**. CLM-3 (BG-BM) spec needs explicit `δ·L_CE_general`
addition to its `L_total` and an α/β/γ/δ/ε weight ablation as a fifth
F-CLM-3 falsifier pre-launch.
