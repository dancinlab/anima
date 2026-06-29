# H_9024 — ByteGPT recomb-objective: the OBJECTIVE lever on the ATTENTION trunk

**id:** H_9024  (was mis-filed as H_1832 = id-collision with fragment_train_mitosis_assembly; reassigned 2026-06-30)
**slug:** bytegpt_recomb_objective
**tier:** 🧱 NOT-SUPPORTED (DIRECTIONAL) — recomb-objective does NOT crack G1 on ByteGPT attention trunk. G1 best_distinct=0 ON==OFF (no lift). py byte-parity 2-production engine; terminal hexa-native = ⏳ BLOCKED-INFRA (summer 3× reboot, a_break_the_wall type-c).
**date:** 2026-06-30
**wired:** DIRECTIONAL (py 2-production `cli/evaluate.py` `g_eval_all` — the scorer, formerly `core/g_gates.py`, folded into evaluate.py 2026-06-30; byte-parity mouth `core/bytegpt_decode`, NOT a torch probe). core/CLAUDE.md 2026-06-28 deprecates py mirrors → terminal verdict needs hexa-native `anima evaluate`, which is ⏳ BLOCKED-INFRA (summer 3× reboot this session; needs stable GPU pod, cost-gated). torch trainer = .pt→.bin bridge only.

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
- engine-native eval = `anima evaluate <bin> --corpus … --gen 80` → `cli/evaluate.py` `g_eval_all` (scorer folded from former core/g_gates.py, 2026-06-30) + core/bytegpt_decode (byte-parity). DIRECTIONAL (py); terminal hexa = ⏳ BLOCKED-INFRA.
- `state/1602_bytegpt_recomb_objective/ab_eval.log` (on summer host) — verbatim py G0-G6 both arms (OFF DONE 20:25 UTC · ON DONE 21:18 UTC, both rc=0).

## Prior art (the campaign this gates)

- H_1602: recomb objective alone, **ConvMoE** 9/9 → NOT-SUPPORTED (objective floored on conv).
- H_1819: co-trained bind op × objective, ConvMoE 0/3 → NOT-SUPPORTED.
- h1129 ByteGPT-303M (plain CE): engine-native G1 FAIL (max_single=2, best_distinct=2, no lift).
- This is the **first test of recomb-objective on the ATTENTION trunk** — the last live lever after
  all operator-family (mouth + substrate) and the ConvMoE-objective levers floored.

---

## Verdict

<!-- CARD_VERDICT -->
🧱 **NOT-SUPPORTED (DIRECTIONAL)** — the recombination OBJECTIVE does NOT crack G1 on the ByteGPT
attention trunk. The decisive ON-vs-OFF test FAILS on both conditions (ARM-ON G1 PASS **and** >ARM-OFF).

py byte-parity engine-native eval (`cli/evaluate.py` `g_eval_all`, gen=80, 4-cell corpus), verbatim
`state/1602_bytegpt_recomb_objective/RESULT.md`:

| gate | ARM-OFF `ce_marginal` | ARM-ON `infonce` (★lever) |
|------|------------------------|----------------------------|
| G0 COHERENCE | 🟢 PASS kwr 5/5 | 🟢 PASS kwr 4/5 |
| **G1 RECOMBINATION** | 🔴 best_distinct=0 max_single=0 | 🔴 **best_distinct=0** max_single=0 |
| G2 NOVELTY | 🔴 novel=0 | 🔴 novel=0 |
| G6 IDEATION★ | 🔴 distinct=4 fals=0 | 🔴 distinct=5 fals=0 |
| CLOSURE a7b_pass | 🔴 FAIL | 🔴 FAIL |

**LIFT = 0** (G1 best_distinct 0→0, no lift; G6 fals 0→0). Both arms 4/4 held-out DESCENT (real
generalization, fair models — NOT a crippled-training artifact). So the floor is the *objective lever's*,
not undertraining. Converges with the whole G1 campaign: **H_1602** (recomb-obj on ConvMoE, 9/9) +
**H_1819** (co-trained bind×obj, 0/3) + plain-CE **h1129** (ByteGPT-L24) — every arch AND the objective
lever floor at G1. **The last live lever (objective × attention trunk) also floors → G1 wall confirmed
trunk-objective-bound across arch+objective family** (lit-converged: objective+regularization is the
axis, but THIS objective family is now exhausted).

**Terminal-hexa confirmation = ⏳ BLOCKED-INFRA (2026-06-30):** 4× attempt on pool — det-CPU(non-cuda hexad, cuda_available=0) 303M gen=80 = impractically slow/stall (CPU 0%); det-GPU(stable cuda hexad, cuda_available=1) on aiden = **CUDA-13 runtime.a stall** (hexad CPU 0% + GPU 0%, forge det cuda dispatch bug — CLAUDE.md: "CUDA-13=3 bug, CUDA-12 host required"); summer = frequent reboot (3× this session). Terminal needs a reboot-free **CUDA-12** GPU pod (cost-gated). G1=0 is the ckpt's byte-parity property (hexa⇄py byte-identical proven), so terminal is expected to **confirm, not overturn** — follow-on, not a blocker on the directional conclusion.

**Scope/honesty (c9):** py is byte-parity 2-production (NOT a torch probe), but core/CLAUDE.md (2026-06-28)
deprecates py mirrors → this is **DIRECTIONAL**, not terminal. The hexa-native TERMINAL confirmation is
**⏳ BLOCKED-INFRA** (`a_break_the_wall` type-c): summer rebooted 3× this session mid-eval (det-CPU
`HEXA_DET=1`, GPU 0%, slow for 303M) — NOT a science ceiling, an unstable-host wall. Terminal needs a
reboot-free GPU pod (cost-gated). The G1=0 is the ckpt's property (byte-parity decode), so terminal is
expected to confirm, not overturn — follow-on, not a blocker on the directional conclusion.
