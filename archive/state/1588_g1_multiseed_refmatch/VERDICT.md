# H_1588 — G1 RECOMBINATION multi-seed reference-match — VERDICT

**Builds on H_1587 (ad13):** the engine-native G1 FAIL on h1129 was a SAMPLER-METHOD artifact
(forward byte-faithful, weights bit-exact; only xorshift32 inv-CDF vs torch multinomial+Gen(7)
RNG walk diverges). H_1588 implements ad13 path-1 (seed-robust reference-matched metric) and
re-scores the live ckpts to reveal the TRUE recombination status.

## THE FIX (frozen-first, NOT tune-to-green)
Recombination DEFINITION frozen VERBATIM (7B_PASS_CONDITIONS / a7b_pass / H_1129):
for some k∈{2,3,4,5}: composed_distinct ≥ 2 AND > max_single AND coherent(kwr≥0.50).
ONLY ADDED seed-robustness — re-run the SAME ladder over seeds {7, 4302, 4303} (reference-match;
G6 ladders use [4301/4302/4303], 7 = H_1129 default), GREEN = majority (≥2/3). Symmetric on the
torch reference AND the engine. No bar moved.

## LOCKSTEP 2-PRODUCTION CHANGE (PROPOSED, owner-nod-pending — NO merge)
`core/g_gates.hexa` + `core/g_gates.py`:
- `g_eval_g1` parameterized by `base_seed` (=7 default reproduces the original single-seed path
  byte-for-byte). `.hexa`: new `g_eval_g1_seeded(ckpt,gen,known,base_seed)`.
- NEW `g_eval_g1_multiseed` (both languages): ladder over {7,4302,4303}, GREEN=majority,
  status="proposed, owner-nod-pending".
- `g_eval_all` reports BOTH; **closure stays on the FROZEN single-seed G1** until owner approval.

## RE-SCORE — TRUE per-ckpt, per-seed status

### ByteGPT-303M h1129 — torch reference arm (multinomial+Generator, summer RTX5070, torch 2.11.0+cu130)
(full capture: state/1588_g1_multiseed_refmatch/torch_ref_h1129_summer.out)

| seed | max_single | best_composed | clears |
|---|---|---|---|
| 7    | 1 | 2 | GREEN (k=5) |
| 4302 | 1 | 2 | GREEN |
| 4303 | 1 | 2 | GREEN (k=5) |

**ByteGPT-303M h1129 torch-ref MULTI-SEED G1 = GREEN 3/3.** Confirms the H_1129 🟢 is seed-ROBUST,
not single-seed luck → RETRACTS the "engine FAIL ⇒ ByteGPT-303M can't recombine" inference.

> Engine-arm h1129 (py bytegpt_decode) re-score was IN-FLIGHT on summer when the host was released
> for the canonical `hx install anima` reinstall (coordinator). PARTIAL — engine-arm h1129 numbers
> NOT captured this run. To be RE-RUN on the clean canonical install (engine-native via installed
> `anima eval`). The torch-ref GREEN 3/3 + H_1587's byte-faithful-forward proof already establish
> the recombination is real; the engine multi-seed arm is expected to surface it (≥2/3) — pending.

### clm303_clean (.clm deep-mouth, 303M CLMConvMoE) — py engine arm (clm_decode, local mini, bounded 2.8GB RSS)
(full capture: state/1588_g1_multiseed_refmatch/result_clm_clm303_clean.clm.json + engine_clm_clm303.out)

| seed | max_single | best_composed | clears |
|---|---|---|---|
| 7    | 0 | 1 | FAIL |
| 4302 | 0 | 0 | FAIL |
| 4303 | 0 | 0 | FAIL |

**clm303_clean MULTI-SEED G1 = FAIL 0/3 — GENUINE, not a sampler artifact.** Best composed distinct
never reaches 2 (let alone > max_single) on ANY seed. clm303_clean does NOT recombine the H_1129
concept sets. Honest result (c9): clm303's G1 FAIL stands under the corrected seed-robust metric.

## SCOPE-EXTENSION — clm303_clean FIRST COMPLETE engine-native G0-G6 (py 2-production)
(prior gate had been blocked by hexa farr-leak OOM + hexa codegen; py engine sidesteps both, bounded)
Full driver `core/g_gates.py clm303_clean.clm data/corpus.txt --gen 40` (multiseed wired in):
capture: state/1588_g1_multiseed_refmatch/g0g6_clm303_multiseed.out (+ corroborates prior
state/clm303_clean_corpus/g0g6_py.txt). Byte-parity gate already PASS (decode hexa==py byte-identical,
CE 15-decimal, see g0g6_py.txt PART A).

| gate | result | detail |
|---|---|---|
| **G0 COHERENCE** | **PASS** | n_coherent 5/5, ratios 0.714/0.800/0.571/0.889/0.667 |
| **G1 RECOMBINATION** (single-seed=7, frozen) | **FAIL** | max_single=0 best_distinct=0 |
| **G1 multi-seed** (proposed) | **FAIL 0/3** | (7,F)(4302,F)(4303,F) — GENUINE |
| **G2 NOVELTY** | **PASS** | n_novel=33 control_novel=0 coherent=16 (corpus=local proxy) |
| **G3 PHILOSOPHY** | ok=True | continuity 0.999950 impostor_cos 0.0 (architecture read, ckpt-indep) |
| **G5 NON-FAB** | **L1 PASS** | l1_rate=0.2647 ≤0.30 (L2 §ImmuneMemory port pending) |
| **G6 IDEATION ★** | **FAIL** | dist=5 (≥5 ok) but fals=0 (need ≥1), coherent=5, frame_leaks=0 |
| **CLOSURE a7b_pass = G0∧G1∧G2** | **FAIL** | (G1 axis genuinely fails) |

clm303_clean: coherent + novel + identity-continuous + non-fabricating, but does NOT recombine (G1)
and does NOT emit a falsifiable idea (G6 fals=0). a7b_pass FAIL — driven by the genuine G1 wall, NOT
a measurement artifact (the multi-seed metric confirms it). Consistent with anima's documented
recombination/G6 capacity wall (H_1129/1139/1464 family).

## BYTE-PARITY FIXTURE (.hexa ⇄ .py)
- PY side (g1_parity_fixture.py, core/g_gates.py g_eval_g1 base_seed=7, d768 fixture, gen=24):
  base_seed:7 max_single:1 best_k:4 best_distinct:1 pass:false (captured: parity_py.out).
- HEXA side (g1_parity_fixture.hexa, live core/g_gates.hexa g_eval_g1_seeded): the full-engine
  import-closure compile (g_gates→generator+g6_ideation+engine_cli = whole substrate) exceeded the
  wall budget on mini (8+ min, 4.5GB compiler RSS) and was stopped when the hosts were released for
  reinstall. PARTIAL — the .hexa fixture decode did not emit before stop.
  **Parity is established by construction:** the G1 metric is a deterministic function of the
  `gen_auto_ideate` decode text, and `gen_auto_ideate` byte-parity (hexa==py, .clm + .bin) is
  ALREADY proven in state/generator_2prod_py_parity/ and the clm303 PART-A gate (decode hexa==py
  byte-identical, CE to 15 decimals). The fixture re-confirm is a follow-on on the canonical install
  (where the engine is precompiled, avoiding the from-source closure compile).

## HONEST FRAMING (c2 / c9 / a_break_the_wall)
Reference-match (single-seed → seed-robust; DEFINITION unchanged), NOT tune-to-green — the majority-
of-3 metric is the CONSERVATIVE measurement (a single seed could flip either way). The result is a
plainly-stated MIXED verdict: **h1129 recombines (torch-ref GREEN 3/3), clm303_clean does not
(engine FAIL 0/3)**. clm303's a7b_pass remains FAIL on a GENUINE G1 wall, not an artifact — a real
negative result, reported as such.

**wired:** proposed, owner-nod-pending (no merge; frozen single-seed remains live default).
