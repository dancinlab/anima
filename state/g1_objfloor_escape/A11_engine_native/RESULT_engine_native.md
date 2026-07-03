# A11 engine-native G1 — mouth-generation determination · FALSIFIED-CEILING

**Fire:** vast pod 43727405 (RTX 5090 32GB, torch 2.11.0+cu128 sm_120), 2026-07-03/04.
Follow-on to `RESULT.md` (this dir), which reached A11 torch-DIRECTIONAL 5/5 (synthetic +
natural signature-decode) but was BLOCKED from the engine-native mouth-generation terminal
by (1) the readout gap (signature-decode != autoregressive mouth) and (2) no torch host /
absent `cli/evaluate.py`. **This pod resolves both** and closes the terminal.

## The engine-native realization of A11

A11 = "TPR forward-slot x contrastive-replace". The WIRE_SPEC bolt-in (a TPR forward-slot
into `core/clm_decode.hexa` + CE-deleted InfoNCE) is one realization; the production trainer
already ships the SAME mechanism family as objectives that sculpt the trunk and **serialize
to a standard-decodable .clm/.bin** (aux params DROPPED at serialize) — so they score through
the real byte mouth via `anima evaluate --py`, which is *strictly more faithful* to
"engine-native mouth generation" than a bolted-on signature-decode readout:

- **`constructive_bind`** = HRR/TPR trained bind (Plate 1995 / Smolensky 1990): learned role
  & filler projections, circular-conv bind c=r(x)f, unbind-recovers-filler + composite-
  predicts-next aux. cli/train.py calls this **"the one untried piece of the substrate
  framebreak"** = the A11 TPR-slot mechanism, trained end-to-end into the trunk.
- **`composed_nce`** = composed-negative InfoNCE (within-window wrong-composition hard
  negatives) = the "contrastive-replace" half of A11.

Both were warm-FT'd from the G0-green ByteGPT 303M (h1129c) on the **en_block combination-
coverage natural corpus** (held-out gate pairs UNEXPOSED), lr 2e-5 / 2000 steps, then scored
by the **frozen gen=40 engine-native `--py` G1** (torch-free numpy, terminal-eligible).
constructive_bind converged cleanly (cbind_unbind 0.34->0.003 = trunk learned a strongly
decomposable bind; composed_nce aux 0.84->0.069).

## Results (frozen gen=40 · all G0-green = valid mouth-generation G1)

| ckpt | objective | G0 | G1 best_distinct | G1 max_single | G1 | G2 | G6 distinct |
|------|-----------|-----|------------------|---------------|-----|-----|-------------|
| base_h1129c | ce (ctrl) | GREEN 4/5 | 1 | 1 | RED floor | GREEN 9 | 6 |
| **cbind_en** | constructive_bind (A11 TPR/HRR) | GREEN 5/5 | **0** | 1 | RED **floor** | GREEN 10 | 6 |
| **cnce_en** | composed_nce (A11 contrastive) | GREEN 5/5 | **1** | 1 | RED **floor** | GREEN 11 | 6 |

G1 escape bar (frozen, verbatim): *some k: best_distinct >=2 AND >max_single AND coherent.*
Every A11 arm: best_distinct <= 1 <= max_single -> **0/1 HIT.**

## VERDICT: FALSIFIED-CEILING — the synthetic REACHABLE does NOT transfer to mouth-gen

- A11's synthetic + natural **signature-decode** 5/5 (prior RESULT.md, torch DIRECTIONAL)
  **does NOT survive** promotion to **autoregressive mouth-generation** on the production
  303M byte mouth scored engine-native. The trained constructive TPR/HRR bind AND the
  composed-contrastive objective both stay at the G1 recombination floor (best_distinct
  0-1, control=1). The signature-decode HIT was a clean-readout property (orthonormal roles
  + shortlist energy), not a mouth-generation capability. **terminal_flip: NO — H_9120 G1
  objective-floor stays CONFIRMED-TERMINAL under engine-native mouth-generation.**
- This is the engine-native confirmation the ledger predicted (additive readout/aux binding
  all 🧱: H_1602/1812/1814/1816/9120; lever = trunk objective, not readout-binding).
  G0-green(5/5) + G2-green(novel 10-11) rule out undertrain — a clean recombination ceiling.

## Honest scope (c9)

- **Additive-aux, not CE-deleted forward-slot.** constructive_bind/composed_nce are
  `ce + lambda*aux` (the H_9120 additive family), decoding via the standard mouth. The
  *pure CE-deleted TPR forward-slot in the byte readout* (WIRE_SPEC steps 2-3, a v0.3 CLMX
  ext-block + role-bind decode ops) is NOT built here. Given (a) this engine-native additive
  result and (b) the whole additive-binding ledger being 🧱, the additive A11 family is
  FALSIFIED-CEILING; the CE-deleted-forward-slot variant remains the single unbuilt cell
  (follow-on: needs the clm_decode.hexa role-bind ops + serializer v0.3, then re-fire).
- **ByteGPT byte mouth** (the only 303M G0-green trunk), full-attention. constructive_bind
  is defined trunk-agnostic (penultimate site), so the bind mechanism is faithfully tested;
  a CLM-MoE variant would need a CLM 303M G0-green base.
- **Single frozen-bar pass** (not 5-seed); best_distinct <=1 leaves no room for a 5/5 flip.
- **Engine-native proof:** cli/evaluate.py `grep -cE 'import torch|gauge_lib'` = 0 (numpy
  byte mouth). Not the WIRE_SPEC hexa decode (that path unbuilt) — but the py 2-production
  `--py` scorer IS terminal-eligible per a_eval_py_canonical.

## Artifacts
- ckpts (engine-native, PULLED pre-teardown, a_fire_recover_complete):
  `~/anima-weights/g1_escape/cbind_en.bin`, `~/anima-weights/g1_escape/cnce_en.bin` (1.213GB each, ByteGPT303 .bin)
- logs: cbind_en_train.log, cnce_en_train.log · verdicts: cbind_en_g1.json, cnce_en_g1.json
- vs session 42871178 (H_1602 objrun composed-nce single-axis): THIS run is A11 = the SAME
  composed_nce PLUS constructive_bind (TPR/HRR bind axis), both engine-native mouth-gen
  scored; H_1602 was the objective-only axis without the TPR-slot bind. Both -> floor.
- cost: shared RTX 5090 session ~2.5-3h, est. ~$1.5-2 total (coverage + A11 + baseline).

> **Follow-on (마지막 escape cell 닫힘, pod43736708):** CE-deleted TPR-forward-slot(WIRE_SPEC v0.3)을 빌드+학습+engine-native `--py` 채점 → CLM 0/5 ∧ ByteGPT(G0🟢) 0/5 = FALSIFIED-CEILING. TPR=W_eff·yn 선형붕괴로 **terminal by construction**. 상세 = [`RESULT_tpr_wire.md`](RESULT_tpr_wire.md).
