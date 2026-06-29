# H_1832 — ByteGPT recomb-objective: the OBJECTIVE lever on the ATTENTION trunk

**id:** H_1832
**slug:** bytegpt_recomb_objective
**tier:** _(to fill from state/verdicts/1602_bytegpt_recomb_objective verbatim)_
**date:** 2026-06-30
**wired:** engine-native (py 2-production cli/evaluate.py → core/g_gates.py → core/bytegpt_decode.py byte-parity mouth; NOT a torch probe). torch trainer = .pt→.bin bridge only.

---

## Hypothesis

The recombination OBJECTIVE (InfoNCE aux-loss alongside next-byte CE) lifts engine-native G1
`composed_distinct≥2` **on a ByteGPT (24-layer attention) trunk**, where it floored on ConvMoE
(H_1602 9/9; H_1819 op×obj 0/3). Attention = content-addressed fetch-and-bind (H_1394 isolates
G6 on ByteGPT where conv blurs); the surviving un-tested cell is objective × attention.

**Honest prior (UNIVERSE/CLAUDE.md lesson #7):** plain-CE ByteGPT-303M (h1129), torch-G1-GREEN,
is ALSO engine-native G1 FAIL (max_single=2, best_distinct=2, no lift; G6 fals=0). So ByteGPT alone
does NOT pass — the bet is strictly the objective lever ON vs OFF on the same attention trunk.

---

## PREREG: A/B causal isolation (PREREG_FREEZE.md · frozen before measurement)

| arm | training signal | role |
|-----|----------------|------|
| ARM-OFF `ce_marginal` | standard next-byte CE | control (CE never rewards conjunction) |
| ARM-ON `infonce` | CE + λ·InfoNCE (λ=1.0, neg=64) | ★ decisive: predictive-coding separation pressure |

Identical seed=7 / steps=2000 / corpus / data-RNG; ONLY the loss differs.
**Decision test:** ARM-ON G1 PASS **AND** ARM-ON best_distinct > ARM-OFF → "objective lever cracks G1".
Frozen H_1129 bar VERBATIM: ∃k∈{2..5} `composed_distinct≥2 ∧ >max_single ∧ coherent kwr≥0.50` at the
native 80/120 ladder. tune-to-green forbidden (p7).

---

## Training configuration

- ByteGPT **d=1024 L=24 H=16 block=512** (== h1129 shape, 303,097,856 params); savant golden-zone
  cusp-anneal ON (GZ_LOWER=0.21231792755821914, latched step 1).
- balanced 4-cell corpus (HF anima-corpus-{ko,en}-{general,sns}; ~23.5MB ≈ 0.35 epochs — NOT the
  clm303 memorization regime). proportional sample, seq_len=512, batch=8, bf16, lr=3e-4, val_frac=0.05.
- host = summer pool RTX 5070 sm_120 (cuda_available=1, GPU 98-99%), ~639s/arm, cost ≈ $0 (LAN pool).

## held-out DESCENT (FINAL per-register val_CE · uniform=ln256=5.5452)

| register | ARM-OFF | ARM-ON |
|----------|---------|--------|
| ko-general | 2.246 D | 2.035 D |
| en-general | 2.520 D | 2.494 D |
| ko-sns | 2.195 D | 1.981 D |
| en-sns | 3.039 D | 2.989 D |
| pooled | **2.500 (4/4 DESCENT)** | **2.375 (4/4 DESCENT)** |

Both arms 4/4 held-out DESCENT — REAL generalization, NOT memorization. ARM-ON marginally
better-trained (lower CE) → fair model, not crippled.

---

## Frozen bar (pre-registered — tune-to-green forbidden, p7)

| Gate | Bar |
|------|-----|
| G1 RECOMBINATION | ∃k∈{2..5} `composed_distinct≥2` AND `>max_single` AND coherent kwr≥0.50 (native 80/120) |
| G6 IDEATION★ | `dist≥5` AND `fals≥1` |
| LIFT (decisive) | ARM-ON best_distinct strictly > ARM-OFF |
| held-out DESCENT | 4/4 register val_CE < ln256=5.545 — overfit = verdict invalid (both PASS) |
| closure a7b_pass | G0 ∧ G1 ∧ G2 |

---

## Artifacts

- `state/1602_bytegpt_recomb_objective/trainer.py` — ByteGPT recomb-obj trainer (ce_marginal / infonce arms; savant schedule + InfoNCE head reference-matched from cli/train.py + state/1602_recomb_objective)
- `state/1602_bytegpt_recomb_objective/PREREG_FREEZE.md` — frozen spec (before measurement)
- `state/1602_bytegpt_recomb_objective/RESULT.md` — verdict (G0-G6 table)
- `~/anima-weights/bytegpt_recomb_303m/{off,on}_seed7.{bin,pt,json}` — ckpts PULLed (a_fire_recover_complete);
  off sha256 b55f731d3d89be774a04549d2e3d93df6bf063b53b9047b12975ed2877b851be · on sha256 5c93b11b20d8f5e6bfd6018d018cf64f0634f2693ce9c33faa8c7c3e61a979c1
- engine-native eval = `cli/evaluate.py <bin> --corpus … --gen 80` → core/g_gates.py + core/bytegpt_decode.py

## Prior art (the campaign this gates)

- H_1602: recomb objective alone, **ConvMoE** 9/9 → NOT-SUPPORTED (objective floored on conv).
- H_1819: co-trained bind op × objective, ConvMoE 0/3 → NOT-SUPPORTED.
- h1129 ByteGPT-303M (plain CE): engine-native G1 FAIL (max_single=2, best_distinct=2, no lift).
- This is the **first test of recomb-objective on the ATTENTION trunk** — the last live lever after
  all operator-family (mouth + substrate) and the ConvMoE-objective levers floored.

---

## Verdict

<!-- CARD_VERDICT -->
_(to fill from eval — frozen-first, c9 honest either way)_
