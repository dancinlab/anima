# H_911 CROSS-DOMAIN EXTENSION — MATRIX

**Hypothesis (per domain, identical shape).** Does the same abstract concept form an amodal hub ACROSS surface forms? Test = **concept-major (parallel) ordering vs representation-system-major (concat) ordering**, measured on a LEARNED-semantic axis (int4-QAT CLMConvMoE → L2-normalized mean-pooled learned hidden; AMODAL anchor = within-concept cross-form cosine − same-form cross-concept baseline; paired bootstrap CI, deterministic LCG, B=2000), with a mandatory **within-concept token-order SHUFFLE NULL**.

**Harness:** `stdlib/flame/clm_h911_scale.hexa` (reference language version), run VERBATIM via env `CLM_SCALE_N / CLM_SCALE_PAR / CLM_SCALE_CON`. NLANG=5 forms per concept. Same model/init/training as the language N-sweep; only the corpus changes.

**Tier rule.** 🟢 SIGNAL = LEARNED CI_lo > 0 AND NULL CI_lo ≤ 0 · 🔴 ARTIFACT = LEARNED CI_lo > 0 BUT NULL CI_lo > 0 · 🔴 ABSENT = LEARNED CI straddles/≤ 0 · ⛔ OPEN-BLOCKED = no reachable aligned data (data-poor; not synthesized).

| Domain | aligned-data-source | N | LEARNED 95% CI | NULL 95% CI | TIER | commit |
|---|---|---|---|---|---|---|
| 🎨 multimodal | `yerevann/coco-karpathy` — 5 real human captions / image | 250 | [0.0201, 0.0331] | [-0.0190, -0.0107] | 🟢 **SIGNAL** | `6c7012d00` |
| 🔢 math | `internlm/Lean-Workbook` — NL · Lean · proof-state · tactic · answer | 250 | [-0.2643, -0.2051] | [-0.0640, -0.0406] | 🔴 **ABSENT** | `dec21c584` |
| 🌌 physics | — (no aligned parallel text; equation/graph non-text or unaligned) | — | — | — | ⛔ **OPEN-BLOCKED** | `664b11628` |
| 🧠 philosophy | — (cross-tradition unreachable; cross-language = the prior LANGUAGE test) | — | — | — | ⛔ **OPEN-BLOCKED** | `0ea919c51` |
| 🔭 cosmology | — (reachable data = PB numeric sims, not parallel text) | — | — | — | ⛔ **OPEN-BLOCKED** | `d8fbb3d26` |

## Reference (language version, for calibration)
The same harness on the 5-language parallel/concat corpus (N=25) reproduces 🟢 GREEN: LEARNED CI [0.301, 0.348], NULL CI [-0.190, -0.163] — confirming the harness + NULL probe behave as designed before any cross-domain run.

## Honest summary
- **Genuinely testable (real aligned data reached):** 🎨 multimodal and 🔢 math. These are the data-rich domains where REAL aligned parallel forms exist on HF (no synthesis).
- **Data-blocked (OPEN-BLOCKED):** 🌌 physics, 🧠 philosophy, 🔭 cosmology. For all three, no reachable corpus carries ONE concept/law/phenomenon in 5 genuinely-aligned parallel TEXT surface forms; manufacturing the alignment is the construct-invalidity trap and was deliberately NOT done.
- **Outcomes:** multimodal = 🟢 SIGNAL (concept-major hub survives the shuffle NULL — semantic, not layout). math = 🔴 ABSENT (the 5 proof-system representations are too surface-divergent for a positive cross-form hub on the learned axis; honest negative).
- **NULL-probe integrity:** in the one domain that passed (multimodal), the NULL CI is properly negative ([-0.0190, -0.0107]) — the effect is NOT a within-concept byte-order / layout artifact. Math's LEARNED CI was already ≤0 so no artifact risk.

## Reproduce
```
# build corpora (real data, no synthesis)
python3 H911X/harness/build_math_corpus.py
python3 H911X/harness/build_mm_corpus.py
# run (from a hexa-lang checkout that has stdlib/flame)
CLM_SCALE_N=250 CLM_SCALE_PAR=$PWD/H911X/data/math_par.txt CLM_SCALE_CON=$PWD/H911X/data/math_con.txt hexa run stdlib/flame/clm_h911_scale.hexa
CLM_SCALE_N=250 CLM_SCALE_PAR=$PWD/H911X/data/mm_par.txt   CLM_SCALE_CON=$PWD/H911X/data/mm_con.txt   hexa run stdlib/flame/clm_h911_scale.hexa
```
