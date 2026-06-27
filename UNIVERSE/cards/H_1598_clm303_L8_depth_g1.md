# H_1598 — does L8 depth clear the G1 (C2 RECOMBINE) wall that clm303 L4 failed?
<!-- @canonical-ok task-specified slug "1576_clm303_torch_train" -->

**Question (a_break_the_wall · a4c9/H_1586 depth-is-the-G1-lever):** clm303 **L4** is
G1-RECOMBINATION-blind (frozen wall: 0/3 seeds, max_single=0). Does a **deeper L8** ConvMoE
(d2781, E4, 303M) lift G1 above that wall at the 303M scale? TESTS the depth-lever claim.

**Engine path:** py 2-production engine `core/g_gates.py` driven by `core/clm_decode.py`
(numpy-only; only `torch` strings are a comment stating it is NOT a torch mirror — code path
is torch-free → **TERMINAL** per a_engine_native_learning, not the ad-hoc DIRECTIONAL mirror).
Same engine / seeds {7,4302,4303} / gen=40 as the frozen L4 baseline
(`state/verdicts/1588_g1_multiseed_refmatch/clm303_g0g6.txt`). hexa single-entry not used on
summer (x86_64 codegen blocked, known). nwin=16 descent (frozen bars window-count-invariant).

## Artifact
- `clm303_deep_L8_d2781.pt` (1.2 GB) sha256 `69ac4e34…01b` · **L8 trunk · E4 experts** (mitosis
  E0=2→Emax=4) · d2781 K3 V256 · step 12000/15000 · CE 1.37 val_CE 1.402 gap +0.035.
- `.clm` v0.3 (L8/E4 general grammar) sha256 `5777c506…840c41` · 154.5 MB · round-trip PASS.
- preserved summer→mini `~/anima-weights/clm303_deep_L8/` (HF DNS-blocked on summer).

## STEP 2 — held-out mirror-DESCENT (math.log mirror, dt_ln-immune)  ✅ 2/2 PASS
| lang | held model_ce | uniform | shuffle | DESCENT | train_ce | gap | overfit |
|------|---------------|---------|---------|---------|----------|-----|---------|
| ko   | 1.600         | 5.545   | 11.528  | PASS    | 1.838    | −0.238 | NO |
| en   | 1.942         | 5.545   | 6.970   | PASS    | 1.711    | +0.231 | NO |

Held-out generalizes (gap ko negative, en small positive) — the **opposite of clm303 L4
memorization NO-DESCENT** (H_1579). The deep ckpt is sound, not overfit.

## STEP 3 — engine-native G1 / C2 RECOMBINE multiseed {7,4302,4303}  🧱 FAIL 0/3
<!-- G1_CARD_TABLE -->
py 2-production engine `core/clm_decode.py` (numpy, torch-free → TERMINAL), gen=40, seeds {7,4302,4303},
host=mini (2026-06-27). verdict file `state/verdicts/1598_clm303_L8_depth_g1/1598.txt`.

| seed | max_single | best_composed | clears |
|------|-----------|---------------|--------|
| 7    | 0         | 1             | FAIL   |
| 4302 | 0         | 1             | FAIL   |
| 4303 | 0         | 0             | FAIL   |

**MULTI-SEED G1 = FAIL (0/3 seeds clear).** All seeds: max_single=0, best_composed 0–1, never
≥2 distinct-above-max_single. The L8 model emits coherent generic web/wiki prose (kwr 0.65–0.96,
coherent=True) that **does NOT compose the seeded anima concepts** — its continuations ignore the
concept seed and run into corpus-register prose ("The top example…", "Santa accessibled", "the market
lossions"). Same wall shape as clm303 L4.

### vs frozen L4 wall
clm303 L4 (same engine, gen=40): **G1 = FALSE · 0/3 seeds · max_single=0 · best_distinct=0**.
L8 d2781 (this): **G1 = FALSE · 0/3 seeds · max_single=0 · best_composed≤1** — INDISTINGUISHABLE
from L4 on G1. Depth L4→L8 did NOT move the recombination metric.

## VERDICT
<!-- CARD_VERDICT -->
🧱 **L8 depth does NOT clear the G1 (C2 RECOMBINE) wall** — FALSIFIES the depth-as-G1-lever
hypothesis (a4c9 / H_1394 / H_1586) at the 303M scale. The deep ckpt genuinely generalizes to
held-out ko+en (DESCENT 2/2 PASS, gap ko −0.238 / en +0.231 — NOT the L4 memorization NO-DESCENT)
yet remains G1-recombination-blind, identical to L4. So the G1 wall is **NOT a depth / receptive-field
ceiling** — a sound, generalizing, deeper model still fails to compose seeded concepts. The lever lies
elsewhere (recombination objective / register / decode-frame conditioning), not trunk depth.
Engine path TERMINAL (py 2-production numpy, grep-clean of `import torch|gauge_lib`). Frozen bar
(≥2 distinct ∧ >max_single ∧ coherent) UNMOVED — no tune-to-green.

**wired:** `engine-native (py 2-production, byte-faithful clm_decode.py); FALSIFIES depth-lever; no
core/ change to wire (negative result). follow-on: G1 lever = recombination-objective or frame-prime,
not depth (next H).` ckpt PRESERVED on mini `~/anima-weights/clm303_deep_L8/` (.pt+.clm sha-verified).
