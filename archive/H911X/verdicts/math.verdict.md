# H_911 CROSS-DOMAIN — 🔢 MATH

**Question.** Does one theorem form an amodal hub ACROSS proof-system surface forms? Test = theorem-major (parallel) ordering vs proof-system-major (concat) ordering, on the LEARNED-semantic axis, with within-concept token-order shuffle NULL.

## Data reachability — ✅ REAL aligned data REACHED
- Source: `internlm/Lean-Workbook` (HF datasets-server, public, no auth).
- Per theorem, 5 GENUINELY DISTINCT real surface forms of the SAME theorem:
  1. `natural_language_statement` — English prose + LaTeX
  2. `formal_statement` — Lean 4 theorem source
  3. `state_before` — Lean elaborated proof-state / goal
  4. `tactic` — Lean proof tactic script
  5. `answer` — closed-form answer
- Selection: scanned 3000 rows → 1526 unique theorems → kept the **N=250** theorems whose all-5 forms are non-empty AND mutually distinct. No synthesis — every form is a real field from the dataset.
- Corpora: `H911X/data/math_par.txt` (theorem-major), `H911X/data/math_con.txt` (proof-system-major). 1250 lines each (250×5).

## Harness
Reference harness VERBATIM: `stdlib/flame/clm_h911_scale.hexa` (int4-QAT CLMConvMoE learner → L2-normalized mean-pooled learned hidden; AMODAL anchor = within-concept cross-form cosine MINUS same-form cross-concept baseline; paired bootstrap CI, deterministic LCG, B=2000; within-concept shuffle NULL). Run via env `CLM_SCALE_N=250 / CLM_SCALE_PAR / CLM_SCALE_CON`. NLANG=5.

## Result
```
LEARNED-semantic paired mean = -0.234125
LEARNED 95% CI = [-0.264253, -0.205140]
NULL (within-concept-shuffle) paired mean = -0.052193
NULL 95% CI = [-0.063965, -0.040641]
```

- LEARNED CI is entirely **below 0** → `learned_pos = false`.

## TIER: 🔴 ABSENT
LEARNED CI ≤ 0 (does not straddle — it is negative). Theorem-major (parallel) ordering does NOT yield a positive amodal-hub advantage over proof-system-major ordering on the learned axis. The 5 proof-system representations are so surface-divergent (English prose · Lean Unicode source · elaborated proof-state · tactic script · short answer) that within-concept cross-form cosine does not exceed the same-form cross-concept baseline. Honest negative (g63).

NULL probe is moot for the tier (LEARNED already ≤0), but recorded: NULL CI also negative.

Verdict rule applied: `🔴 ABSENT — LEARNED CI straddles/≤ 0`.
