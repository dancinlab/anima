# H_1819 — co-trained bind op × recombination objective: 3-arm decisive G1 test

**id:** H_1819  
**slug:** cotrain_bind_recomb_obj  
**tier:** ⏳ IN-FLIGHT (GPU training — 2× A40, pod 43051219, ~$3-5 A40×h)  
**date:** 2026-06-29  
**wired:** engine-native-eligible (clm_decode.py CLMB extended, H_1818 commit e17c2890f — bind LIVE at decode for op_plaince + op_obj)

---

## Hypothesis

A co-trained Hadamard bind readout (`g = Wa(x) * Wb(x) → Wo → logits`) lifts G1
recombination **when combined with a recombination objective** (InfoNCE on
position-triple segment pairs) that makes it IMPOSSIBLE for the trunk to memorize
without using the bilinear pathway.

**Root cause of H_1818 expected failure (toy Task B):** plain CE lets the trunk
memorize all training combos additively, bypassing the bilinear path. The bilinear
has no gradient to force factored representations — same failure mode as toy Task B.

**The decisive claim:** structure (bind op LIVE at decode) AND objective (L_recomb
forces composition during training) are BOTH required. Neither alone is sufficient.

---

## PREREG: 3-arm causal isolation (matched trunk-init seed/data/steps)

| arm | training signal | expected | role |
|-----|----------------|---------|------|
| (a) `op_plaince` | BindCLM + plain CE (= H_1818 bind arm, fresh 4000-step) | floor G1≤1 | negative control: op without L_recomb |
| (b) `obj_only` | additive CLMConvMoE + L_recomb aux (discarded at serialize) | floor G1≤1 | negative control: L_recomb without bind op at decode |
| (c) `op_obj` | BindCLM + L_recomb (Pa=Wa, Pb=Wb shared) | **G1≥2?** | ★ decisive: structure + objective together |

**Decision test: (c) > (a) AND (c) > (b)** on G1 `composed_distinct`, same 3 seeds
{7, 4302, 4303} → "structure + objective together lift G1".

---

## L_recomb (InfoNCE — PREREG §recomb-objective-정의)

Trunk output x (B, d, T):
- z_a = x[:, :, T//3 - 1] (concept A = context at 1/3 of sequence)
- z_b = x[:, :, 2*T//3 - 1] (concept B = context at 2/3)
- z_c = x[:, :, T - 1] (composite target = end of sequence)
- g = Pa(z_a) * Pb(z_b) — Hadamard composite (early-ctx × mid-ctx, k-space)
- InfoNCE: F.cross_entropy(normalize(g) @ normalize(Pc(z_c)).T / τ, arange(B))
  (g[b] = composite of batch-b's early+mid context must be closest to b's end-ctx c[b])

For arm (c) op_obj: Pa=Wa, Pb=Wb (shared with bind readout), Pc is new.  
For arm (b) obj_only: Pa, Pb, Pc are separate aux projections (discarded at serialize).  
λ_recomb = 0.1 (PREREG mid-range of 0.05–0.3 sweep, single value for cost control)  
τ = 0.1 (InfoNCE temperature)

total loss = CE_byte + aux_moe + λ_recomb × L_recomb  
(arms with bind op also have the Hadamard forward path implicit in CE_byte)

---

## Frozen bar (pre-registered — tune-to-green forbidden, p7)

| Gate | Bar |
|------|-----|
| G1 RECOMBINATION | `composed_distinct≥2` AND `>max_single` AND coherent, ≥2/3 seeds |
| G6 IDEATION | `dist≥5` AND `fals≥1` |
| LIFT (decisive) | (c) strictly > (a) AND (c) strictly > (b) on G1 `best_distinct` / G6 `fals` |
| held-out DESCENT | 4/4 register val_CE < ln256=5.545 (math.log mirror) — overfit = verdict invalid |
| G0 pass | ≥4/5 (4000 steps required; < 4000 = INCONCLUSIVE-at-floor) |

---

## Training configuration

- canon 303M: d=3784, L=4, E0=2, Emax=3, k=512, seq=1024, batch=8, bf16
- 4000 steps (PREREG minimum to ensure G0 passes — H_1818/aa7933 floored G0 at 2000)
- 4-register clean corpus: gen_ko + gen_en + sns_ko + sns_en
- savant golden-zone inhibition (GZ_LOWER≈0.212, cusp anneal)
- mitosis E2→E3 at step 2000
- seeds: {7, 4302, 4303}
- 2× A40, pod 43051219 (hexa-cloud managed @clm303-noverfit-retrain)

---

## Artifacts

- `state/g1_cotrain_recomb_bind/trainer.py` — 3-arm trainer (BindCLM / ObjOnlyCLM / BindRecombCLM)
- `state/g1_cotrain_recomb_bind/run_pod.sh` — pod runner (smoke → train → eval → summary)
- `state/g1_cotrain_recomb_bind/PREREG.md` — frozen specification
- `state/g1_cotrain_recomb_bind/ckpt/` — .clm + .pt + .json + .g0g6.txt (9 per arm×seed)
- `state/g1_cotrain_recomb_bind/RESULT.md` — verdict (pending, to be written post-eval)
- `core/clm_decode.py` — CLMB extension (H_1818, shared by op_plaince + op_obj arms)

---

## Prior art (why this is the untested sweet-spot)

- EXP-3 / H_1603: bind op trained + **dropped at serialize** → INCONCLUSIVE-at-floor
- H_1618 / frozen mouthbind: bind on **frozen weights** → INERT/DESTRUCTIVE
- H_1818: bind op **co-trained + LIVE at decode** + plain CE → expected floor (toy Task B)
- H_1602: recomb objective **alone** (3 variants, 303M) → NOT-SUPPORTED (aa7933)
- Toy Task B (state/g1_toy_cotrain_bind_derisk): op + plain CE → trunk memorizes, bilinear inert
- Toy Task A: op + product-REQUIRED loss → bind generalizes 3/3 seeds ✓

**This is the first test of op + L_recomb combined.**

---

## wired

⏳ IN-FLIGHT — `DIRECTIONAL-screen` tier on completion. If (c) lifts G1≥2 robust:
→ escalate to `core/clm_decode.hexa` + `core/clm_serialize.hexa` CLMB lockstep
(`a_verified_must_wire` rung 3) for TERMINAL verdict.

---

## Verdict

*Training in progress — 2× A40, expected ~2-3h. Results in state/g1_cotrain_recomb_bind/RESULT.md.*
