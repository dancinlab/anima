# A11 — TPR forward-slot × contrastive-replace, SCALE-TRANSFER test (H_9121)

**The one open escape cell.** E1 (contrastive-replace on ADD/no-slot arch) = AT-FLOOR
(5/5, margin −0.47 → floor is ARCHITECTURAL). E2 (TPR under CE) = FLOORED via engine
ledger H_1813/H_1623 (CE-basin swallows the TPR slot, INERT-under-CE). **A11 = TPR
multiplicative binding-slot × contrastive-replace (non-CE) objective SIMULTANEOUSLY** —
the only cell where the objective escapes the CE-basin *and* a binding slot exists.
E1 side-probe found A11 TOY-REACHABLE (margin +3.30, reach 1.0). H_9121 left it
**303M-unmeasured** with an explicit `a_toy_scale_recheck` overstate warning (E2
precedent: TPR toy unbind 1.0 → real CE 0.022).

## Ledger check (check-ledger-before-lever-fire) — FRESH, not dup
- `H_1441`/`H_1464` = contrastive objective **engine-native**, but for **G6 falsifiability**
  on a **no-slot** arch (pos=falsifiable claim, neg=blanked-leg) → 🧱 WALL=CAPACITY.
  NOT G1-recombination, NOT combined with a TPR forward slot.
- `H_1813` = TPR expert-weight reparam **under CE** → NOT-SUPPORTED at floor.
- `H_9120` = recomb-objective *additive-aux* (`CE + γ·L_recomb`) → FALSIFIED.
- **A11 (TPR-slot × contrastive-REPLACE, G1 target) has NO engine-native or scaled
  precedent.** H_9121 verdict verbatim: "A11 … TOY REACHABLE … 303M 미측정". → genuinely fresh.

## What this run adds (a_toy_scale_recheck)
The E1/E2 toys used a **FREE LOOKUP** table `C[filler]` (24 concepts, D=96). This run
REPLACES it with a **REAL DEEP CONV BYTE TRUNK** — the production CLMConvMoE E=2/L1
encoder (inlined `archive/train/clm/model/model.py`: embed → causal-dilated conv →
conv-MoE → GroupNorm). Each filler is a distinct 4-byte string; `C[filler]` = the
trunk's pooled last-position code. Trunk + signature embeds are trained **end-to-end by
the contrastive-replace objective (InfoNCE, NO CE)**. ADD (additive readout, = E1 arch)
vs TPR (role-filler tensor product, = A11) under the SAME objective on the SAME trunk.
This isolates the scale variable: does a real deep conv-byte-trunk representation still
compose under TPR+contrastive on **held-out (novel) filler pairs**?

**Config:** d_model=768 (production golden width), n_experts=2, L=1, k=3, V=256,
**7.30M params**, n_fill=24, held-out 20% (110 novel pairs never composed in training),
300 epochs InfoNCE, 5 seeds. Host: aiden (RTX 5070, torch 2.10+cu128). Cost = **$0**
(pool GPU, no rent).

## FROZEN bar (pre-registered, NOT moved)
A seed HITs iff on held-out pairs: `reach_novel (cov==2 ∧ cov>max_single) ≥ 0.5` **AND**
`margin>0` **AND** `SCRAMBLE ≤ 0.2`. `≥4/5 HIT → DIRECTIONAL-REACHABLE`; `<4/5 → FALSIFIED`.

## Result (d=768, 7.30M params) — mirrors E1's toy A11 side-probe at real-trunk scale
| seed | ADD margin | ADD reach_novel | ADD | TPR margin | TPR reach_novel | TPR scr | TPR |
|------|-----------|-----------------|-----|-----------|-----------------|---------|-----|
| 7    | −1.7509   | 0.00            | floor | +99.335 | 1.00 | 0.01 | **HIT** |
| 11   | −1.8953   | 0.00            | floor | +99.380 | 1.00 | 0.02 | **HIT** |
| 23   | −0.8889   | 0.00            | floor | +104.056| 1.00 | 0.00 | **HIT** |
| 42   | −1.1900   | 0.00            | floor | +108.744| 1.00 | 0.01 | **HIT** |
| 101  | −2.2628   | 0.00            | floor | +100.511| 1.00 | 0.02 | **HIT** |

**TALLY: TPR (A11) HIT 5/5 · ADD (E1 control) HIT 0/5** · d=768 · 7.30M params · $0 (aiden).
InfoNCE on TPR → 0.0000 (perfect fit, generalizes to held-out); ADD plateaus ~1.2–1.4.
JSON: `a11_d768.json`; raw log: `a11_d768.log`.

## Verdict — A11 = DIRECTIONAL-REACHABLE (torch; does NOT cement a tier)
**≥4/5 rule met (5/5).** The toy A11 reachability (E1 side-probe margin +3.30) is **NOT a
free-lookup-table artifact — it survives a real deep conv byte trunk** (7.30M CLMConvMoE
E2/L1 at d=768, trunk trained end-to-end by contrastive-replace). The E1/E2 attribution
holds at scale: floor = ARCHITECTURAL (ADD/no-slot floors 0/5 under the *same* objective),
and CE-basin is the trap (E2/H_1813 TPR-under-CE floored) — remove CE **and** add the TPR
slot together and held-out recombination reaches (5/5). A11 stays the **live escape**;
H_9120 objective-floor-terminal is **NOT flipped** (that is engine-native + natural corpus).

**Scope / honesty (c9, a_toy_scale_recheck, a_engine_native_learning):**
- **torch, not live core/ decode → DIRECTIONAL.** A HIT here does NOT flip H_9120's
  objective-floor terminal and does NOT claim production G1 is solved.
- **Clean SYNTHETIC compositional corpus**, roles=orthonormal identity → TPR reads each
  role slot independently BY CONSTRUCTION; the escape *hypothesis itself* is that removing
  CE lets that independent-slot readout survive. This run shows the mechanism survives a
  **real deep conv byte trunk** (not just a free lookup table) — the toy reachability is
  NOT a lookup-table artifact. It does NOT show a natural-corpus byte mouth binds.
- **The terminal test remains engine-native:** TPR forward-slot wired into
  `core/clm_decode.hexa` + serializer, trained contrastive-replace on the real corpus,
  scored via `anima evaluate --py`. That is out of scope for a state-only run (core/
  off-limits) and is the registered follow-on.
