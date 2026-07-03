# Escape-2 — TPR forward-invariant hard-wire (H_9121)

**Claim under test:** a Smolensky tensor-product (TPR) binding slot HARD-WIRED into
the mouth forward circuit (filler⊗role outer product, multiplicative — not additive
concat/mean), trained with **CE unchanged** (pure forward hard-wire, no objective
term → sidesteps the H_1816 objective-form rejection), opens G1 recombination that
the additive baseline cannot.

## (1) IMPLEMENT — forward structure understood
- Mouth forward = `core/decode.hexa` `bg_forward_last_W` / `_bg_mha` (BYTE mouth) and
  `_clmd_fwd_logits_sc` (CONV mouth). Existing injected-bind (H_9027/H_1818,
  `_bg_apply_bind`) is **additive** (`x = x + gate·(block(x)−x)`) — the escape's
  proposed TPR slot is the multiplicative complement.
- No `.hexa` wiring landed: gated by the TOY discriminator below (per task step 3).

## (2) TOY discriminator (mini, $0 numpy) — `toy_tpr_invariant.py`, `toy_run.txt`
Two probes, 3 seeds {7, 4302, 4303}:

**(M) Mechanism** (fixed random codes, outer-product bind + role-unbind vs flat sum):
- TPR-unbind acc = **1.000**  vs  ADDITIVE-flat acc = **0.242**  (chance 1/8 = 0.125).
- Reproduces H_1466 binding-leg REACHABLE and H_1623 Part-1 (ON 1.0 / OFF chance).

**(C) CE-trained recombination** (end-to-end learned embeds+readout, plain CE only,
held-out = novel (a,b) recombination of KNOWN fillers in KNOWN roles):
- held-out recomb:  **ADD = 0.191 · TPR = 1.000 · ABL(slot-bypass→additive) = 0.191**
- TPR−ADD lift = **+0.809** (> +0.10);  ABL returns to ADD floor (|ABL−ADD| = 0.000).
- Outer product is **causal** (ablation floor-return) → **RESULT: REACHABLE**.

## (3)/(4) 303M + engine-native G1 — NOT refired (BLOCKED), refuted by ledger

The REACHABLE toy is the **documented toy-overstate regime**, not a green light:

1. **This exact escape is already walled.** `H_6123` (`gen_tpr_architectural_invariant`,
   "재조합을 아키텍처 불변식으로(TPR)") = 🧱 **DUP-WALLED**, pointing to:
2. **Abstract probe REACHABLE, 303M FAIL** — the known pattern:
   - `H_1466` TPR symbolic binder: binding leg acc 1.0 vs additive-flat = chance, but
     🧱 WALL (numpy DIRECTIONAL).
   - `H_1623` hypernet-multiplicative tensor bind: abstract ON=1.0/OFF=chance, but
     **frozen clm303 G1 = FAIL 0/3 seeds** (`g1_frozen_mouthbind_screen/RESULT.md`).
   - `H_1813` TPR expert-weight reparam, **engine-native 303M trained under CE
     (`anima evaluate --py`)** = 🧱 **NOT-SUPPORTED (INCONCLUSIVE-at-floor)**: all arms
     fail the G1 bar (best_distinct max 1 < 2, none > max_single). ≈ 0–1/5 HIT.
3. **Toy-overstate precedent** (`a_toy_scale_recheck`): sibling `H_6112` meiosis went
   numpy toy 0→1.0 REACHABLE → real CLMConvMoE trunk 0→0.022 FALSIFIED. Same transfer
   failure risk applies verbatim here.

Refiring a fresh $ pod would (a) need explicit-go rent (absent for this subagent) and
(b) violate `check-ledger-before-lever-fire` (the engine-native answer already exists).

## Verdict — **FALSIFIED**
Per escape rule (4): the engine-native 303M measurement of a TPR-invariant-under-CE
architecture already exists (**H_1813 <4/5, at-floor**), and the fresh toy REACHABLE is
precisely the CE-basin toy-overstate trap. **The architecture is swallowed by the
CE-basin — the G1 recombination ceiling is HARDENED, not escaped.** The multiplicative
outer product is load-bearing in a toy where the task is *designed* to require clean
role-filler unbinding; under real CE on the 303M trunk, CE does not drive the slot to
be used compositionally (same INERT-under-CE mechanism as H_1816/H_1813).

- **cost:** $0 (mini numpy toy only; no rent).
- **scope:** toy = DIRECTIONAL numpy by construction; 303M leg rests on prior
  engine-native H_1813/H_1623 (not a fresh refire). No HYPOTHESES/card/frozen touched.
