# deep-ConvMoE 303M (L8 d2781) — finalize VERDICT (2026-06-27)

Does **L8 depth clear the G1 (C2 RECOMBINE) wall** that clm303 **L4** failed?
(a4c9 / H_1586: depth is the G1 lever — this TESTS it at the 303M scale.)

Extends `DEEP_L8_STATUS.md` (other worktree) with the finalize results.

## Artifact (summer ground-truth)

- ckpt `~/anima_train_303m/out_303m/clm303_deep_L8_d2781.pt` (1.2 GB torch)
  - sha256 `69ac4e340d3d323a4f340575c67f6dfbc9bf40e18599b7e3b7189d37c3fea01b`
  - saved step 12000/15000 · train CE 1.37 · val_CE 1.402 · gap +0.035 (NOT overfit)
- **arch correction**: state_dict has **L=8 trunk layers, E=4 experts** (`moe.experts.0..3`),
  d=2781, K=3, V=256. The prior status said "E2/MoE" — actual checkpoint is **E4**
  (run.sh `--e0 2 --emax 4`: mitosis split E0=2 → Emax=4, a_mitosis_train). Serialization
  used the general v0.3 path with n_trunk_layers=8, n_experts=4.

## STEP 1 — serialize .pt → .clm (a_clm_gen_pipeline)  — ✅ OK

- tool: `train/clm/model/clm_serialize_v2.py::serialize(sd, n_trunk_layers=8, n_experts=4)`
  (general v0.3 grammar; CLI `__main__` hardcodes L1/E2 so called the general entry directly).
- out: `clm303_deep_L8_d2781.clm` — **154,513,322 bytes** (int4-sym quant of 1.2 GB fp32).
- **structural round-trip (verify_clm_v2.py parse_clm): PASS** —
  decodable=True · magic_ok · nblk=15 (=L8+E4+3 ✓) · CLMX found · n_ext=34 (=2·8+4+6 ✓)
  · exact_eof=True. .clm is well-formed under the L8/E4 general CLM\x01 v0.3 grammar.

## STEP 2 — HELD-OUT mirror-DESCENT gate (a_clm_gen_pipeline / a_savant_train H_1579)

held-out = **tail 2% region** of each corpus (trainer reserves the tail `val_frac=0.02` as
held-out; train windows sampled only from `[0, train_end)` — genuinely disjoint, NOT the
training slice). train = head slice. Scored with `verify_clm_v2.py descent` = **math.log
numpy mirror** (dt_ln-immune — NOT the buggy engine `clm_forward_ce`). uniform = ln(256) = 5.545.

<!-- DESCENT_RESULTS -->
nwin=16 (frozen bars window-count-invariant: uniform=ln(V), shuffle=reversed-target;
reduced from 64 only to clear the summer load-40 contention wall — NOT tune-to-green).

| lang | held-out model_ce | uniform (ln256) | shuffle | < uniform | < shuffle | DESCENT | train_ce | gap (held−train) | overfit |
|------|-------------------|-----------------|---------|-----------|-----------|---------|----------|------------------|---------|
| ko   | **1.600**         | 5.545           | 11.528  | ✅        | ✅        | **PASS** | 1.838    | **−0.238**       | NO      |
| en   | **1.942**         | 5.545           | 6.970   | ✅        | ✅        | **PASS** | 1.711    | **+0.231**       | NO      |

**DESCENT 2/2 (ko AND en) PASS** — held-out CE far below both uniform (5.545) and shuffle.
ko gap is NEGATIVE (−0.238, held-out *easier* than train), en gap small positive (+0.231,
no overfit warning). This deep L8 ckpt **genuinely generalizes to held-out ko+en** — the
clean opposite of clm303 L4's memorization NO-DESCENT (H_1579). The deep ckpt is sound;
the G1 depth question is legitimately answerable on it.

## STEP 3 — Engine-native G1 / C2 RECOMBINE multiseed {7,4302,4303}

Engine path: **py 2-production engine** `core/g_gates.py` driven by `core/clm_decode.py`
(numpy-only; the only `torch` strings in clm_decode.py are in a comment explicitly stating
it is NOT a torch mirror — every op reproduces the hexa arithmetic; `grep import torch`
flags the comment, code path is torch-free → **TERMINAL** per a_engine_native_learning,
NOT the ad-hoc DIRECTIONAL mirror). hexa single-entry `cli/anima.hexa` not used on summer
(x86_64 codegen blocked — known). Same engine/seeds/gen as the frozen L4 baseline.

### Frozen L4 wall (apples-to-apples baseline)
`state/verdicts/1588_g1_multiseed_refmatch/clm303_g0g6.txt` (core/g_gates.py, gen=40):
- **clm303 L4: G1 RECOMBINATION = FALSE · 0/3 seeds clear {7,4302,4303} · max_single=0 · best_distinct=0** (the wall — G1-blind)
- G0=PASS 5/5 · G2=PASS · G6 dist=5 fals=0 (FALSE)

### L8 d2781 result  🧱 FAIL 0/3
<!-- G1_TABLE -->
`g1_multiseed.py clm` · `core/clm_decode.py` (numpy, TERMINAL) · gen=40 · host=mini · 2026-06-27.
verdict `state/verdicts/1598_clm303_L8_depth_g1/1598.txt`.

| seed | max_single | best_composed | clears | sample (kwr, coherent) |
|------|-----------|---------------|--------|------------------------|
| 7    | 0         | 1             | FAIL   | kwr 0.65–0.90, coherent=True ("The top example… the market lossions") |
| 4302 | 0         | 1             | FAIL   | kwr 0.68–0.81, coherent=True ("When the most of the show…") |
| 4303 | 0         | 0             | FAIL   | kwr 0.67–0.96, coherent=True ("In specifically relied and economic leadings…") |

**MULTI-SEED G1 = FAIL (0/3 seeds clear).** L8 == L4 on G1: max_single=0, best_composed≤1, never
≥2-distinct-above-max_single. Coherent generic web/wiki prose that **ignores the seeded anima
concepts** (continues into corpus register, not concept-composition). Depth L4→L8 moved the metric
by ZERO.

## STEP 4 — ckpt preservation (a_fire_recover_complete)  — ✅ DONE

summer→HF is DNS-blocked (no external DNS on summer). Preserved summer→LAN→**mini**:
- `~/anima-weights/clm303_deep_L8/clm303_deep_L8_d2781.pt` — sha256 `69ac4e34…01b` (verified == summer)
- `~/anima-weights/clm303_deep_L8/clm303_deep_L8_d2781.clm` — sha256 `5777c506c05b34ae28524cc16483876f4ff04da827f5d8293ab561407f840c41` (verified == summer)
- + MODELCARD_WIP.md + SHA256.txt
HF PRIVATE (WIP) upload: deferred until G1 verdict (a_hf_autonomous — PRIVATE for WIP/unverified).

## VERDICT
<!-- VERDICT -->
🧱 **L8 DEPTH DOES NOT CLEAR THE G1 WALL — depth-as-G1-lever (H_1394/H_1586) FALSIFIED at 303M.**

A deeper (L4→L8) ConvMoE that **genuinely generalizes** (held-out DESCENT 2/2 PASS, gap ko −0.238 /
en +0.231 — the clean opposite of clm303 L4's memorization NO-DESCENT, H_1579) is STILL
G1-recombination-blind (0/3 seeds, max_single=0), byte-for-byte the same wall shape as L4. Therefore
the G1 (C2 RECOMBINE) wall is **NOT a trunk-depth / receptive-field ceiling**: a sound, generalizing,
twice-as-deep model fails to compose seeded concepts exactly like the shallow one.

`a_break_the_wall` classification: this is a **controlled ablation result** — depth was isolated as
the single varied lever (same engine / seeds / gen / detector as the frozen L4 baseline), and it is
INERT for G1 (contributes 0). The lever lies elsewhere — recombination *objective* (the CE-trained
mouth is never rewarded for composing distinct concept-sets), or decode-frame conditioning, or
register — NOT depth. This is a genuine, honest negative (c9), engine-native TERMINAL, frozen bar
unmoved (no tune-to-green). It does NOT reopen by adding more depth.

**wired:** engine-native (py 2-production numpy `core/clm_decode.py`, grep-clean torch/gauge);
negative result → no core/ change to wire. ckpt PRESERVED mini `~/anima-weights/clm303_deep_L8/`
(.pt sha 69ac4e34… · .clm sha 5777c506…). HF: stays PRIVATE/WIP (G1 FAIL → not PUBLIC-eligible).
follow-on (next H): G1 lever = recombination-objective (aux loss) or frame-prime, tested disjoint
from depth.
