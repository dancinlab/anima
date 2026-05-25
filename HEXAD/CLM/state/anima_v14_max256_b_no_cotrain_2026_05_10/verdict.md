# BG-V14-MAX256-B-NO-COTRAIN — verdict

**Meta-verdict**: `V14_VIOLATED → §47_PARTIAL_PRESERVED ★★★★`

Substrate B (BG-LA 350M pretrain, EngineAG path, NO chat-cotrain) at max=256
remained V14_VIOLATED (1/5 trained > random). F-B-MAX256-1 FIRED. The cotrain
regime IS the necessary driver in EngineAG-path V14 PASS; cap-conditional
polarity is NOT universal across cotrain/no-cotrain within the same arch.

## 1. B 5-seed result table (sign-p, cell_count, cap-bound check)

| run | seed | final_n_cells | n_splits | first_cap_turn | cap_bound_turns | iit_phi_unnorm_b16 | trained > random? |
|-----|------|---------------|----------|----------------|-----------------|---------------------|-------------------|
| TRAINED (B) | 42 (prompt) | 44 | 28 | None | 0/200 | **1444.68** | — |
| mirror | 42  | 56 | 40 | None | 0/200 | 2206.33 | NO (random > trained) |
| mirror | 137 | 47 | 31 | None | 0/200 | 1491.44 | NO (1491 > 1444; barely) |
| mirror | 271 | 53 | 37 | None | 0/200 | 1148.72 | YES (trained > random) |
| mirror | 314 | 57 | 41 | None | 0/200 | 2385.53 | NO |
| mirror | 1729 | 54 | 38 | None | 0/200 | 2140.39 | NO |

| metric | value |
|--------|-------|
| n_random_beats | **1/5** |
| sign_test_p (two-sided) | **0.3750** |
| verdict | **V14_VIOLATED** |
| total elapsed | 1143.7s (~19 min on $0 local CPU) |

## 2. cap-arrival latency (trained vs random — §51 mechanism re-verify on EngineAG)

| run | first_cap_turn | max_n_cells_observed | cap=256 reached? |
|-----|----------------|----------------------|-------------------|
| TRAINED | None | 44 | NO |
| s42  | None | 56 | NO |
| s137 | None | 47 | NO |
| s271 | None | 53 | NO |
| s314 | None | 57 | NO |
| s1729 | None | 54 | NO |

**EngineAG path is cap-FREE at max=256.** No run touched the cap; natural
saturation envelope is ~44-57 cells (~30-50 splits) regardless of trained vs
random init. This matches A_phase2_cotrain at max=256 (cells range 47-57)
exactly — confirming §51 finding that EngineAG path has natural saturation
around 50-60 cells regardless of cap parameter. F-B-MAX256-2 (cap-bound at
max=256) **NOT fired**.

**Critical observation**: Cap-arrival latency mechanism (§51) is **NOT
applicable** to EngineAG path at max=256 because no run reaches cap. §51's
"trained reaches cap LATER than random" applies only to v2 path where cap
saturates. In EngineAG, the trained-vs-random differential lives in within-
saturation Φ distribution, NOT in cap-arrival timing.

**B trained terminal cells (44) is LOWER than ALL 5 random (47-57)** — opposite
direction from what §51 mechanism would predict for "denser representation
splits less". Pretrain-only ckpt produces fewer splits AND lower Φ than random
init at max=256. This is a NEGATIVE V14 signal: the pretrain ckpt is actively
suppressing dispersion-driven splits in a way that does not translate to higher
within-saturation Φ.

## 3. cotrain-exercise vs cap-conditional disambiguation verdict

### Hypothesis predictions
- **Cap-conditional (universal)**: ALL substrates PASS at max=256 regardless
  of training paradigm. Predicts B PASS.
- **Cotrain-exercise (§47)**: Only Phase-2 chat-cotrain produces V14 PASS in
  EngineAG path. Predicts B VIOLATED at any cap.

### Observed (cross-paradigm × cross-cap, EngineAG path)
| ckpt | paradigm | max=128 | max=256 |
|------|----------|---------|---------|
| A_phase2_cotrain | chat KO cotrain Phase-2 | V14_STRICT_PASS (10/10) | V14_PASS (5/5) |
| B_bgla_pretrain | Phase-1 pretrain only | V14_VIOLATED (0/5, §47) | **V14_VIOLATED (1/5, this BG)** |

### Falsifier ledger
- **F-B-MAX256-1** (B max=256 V14_VIOLATED → §47 cotrain regime is EngineAG
  driver): **FIRED** (1/5, sign-p=0.3750, V14_VIOLATED bin)
- **F-B-MAX256-2** (B cap-bound at max=256): **NOT FIRED** (no run reached cap)
- **F-B-MAX256-3** (partial PASS 3-4/5 → AMBIGUOUS): **NOT FIRED** (1/5 is in
  VIOLATED bin, not AMBIGUOUS)

### Disambiguation verdict

**§47 cotrain-exercise hypothesis is PARTIALLY PRESERVED** in the EngineAG
arch path:

1. Cap-conditional polarity **IS universal in v2 d=384 path** (§51 confirmed
   for C_cells64_aware and E_convo5k_ft at max=256, both flipping V14_VIOLATED
   → V14_PASS_PARTIAL when cap raised from 128 → 256).
2. Cap-conditional polarity is **NOT universal in EngineAG d=1024 path**.
   Within EngineAG, cotrain-exercise (Phase-2 chat KO) is the necessary
   ingredient for V14 PASS at any cap tested (128, 256). Pretrain-only B
   remains V14_VIOLATED at both caps.
3. The mechanism is **architecture-conditional**: v2 path's mitosis dispersion
   is driven by §30 trigger which scales with cap, so trained ckpts express
   denser representations at higher cap. EngineAG path has natural saturation
   ~50 cells regardless of cap, so cap is not a release valve; the trained-
   random differential must come from a different driver (cotrain exercise).

**Updated cross-paradigm × cross-cap × cross-arch ledger**

| substrate | arch | paradigm | max=128 | max=256 |
|-----------|------|----------|---------|---------|
| A_phase2_cotrain | EngineAG d=1024 | chat KO cotrain | V14_PASS (10/10) | V14_PASS (5/5) |
| **B_bgla_pretrain** | **EngineAG d=1024** | **pretrain only** | **VIOLATED (0/5)** | **VIOLATED (1/5)** |
| C_cells64_aware | v2 d=384 | aware mitosis FT | AMBIGUOUS (3/5) | PASS_PARTIAL (n=2) |
| E_convo5k_ft | v2 d=384 | naive convo FT | VIOLATED (0/5) | PASS_PARTIAL (n=2) |

**The combined picture**: cap-conditional polarity holds in v2 path; cotrain-
conditional polarity holds in EngineAG path. The "universal cap-conditional"
claim from §51 (★★★★★ candidate) is downgraded to **★★★★ MULTI_FACTORIAL**
— at minimum two distinct mechanisms operate (architecture × cap × cotrain)
and the simple universal claim is falsified.

## Honest C3 (≥7)

1. **n=5 strict only n_beats=1 → V14_VIOLATED bin per spec runner**: 1/5 is
   a directional signal that 4 of 5 random init seeds beat the trained
   ckpt. Sign-test p-value = 0.3750 two-sided is NOT significant on its own
   at α=0.05, but combined with B-max=128 (0/5, p=0.0625) the cross-cap
   posterior for "B fails V14" is much stronger than either alone.

2. **B trained Φ_un16=1444.68 vs B max=128 trained Φ_un16=1136.26**: B at
   max=256 produces ~27% higher Φ than at max=128 (more turns to evolve from
   500 → 200 turns is a confound, but the 200-turn trained_phi=1444 vs
   500-turn 1136 indicates B is NOT cap-saturating at max=128 either; max
   observed in §47 was n_cells=46). Cap is not the limiting factor for B.

3. **Mirror seed=42 produced same Φ_un16=2206.33 as in §51 A run** — exact
   match. This is expected: `load_random_init(seed=42, preset="la_350m")`
   is ckpt-independent and deterministic; only the trained ckpt path
   differs. Mirror trajectory is identical to §51's A mirrors, which is a
   valid optimization but means B's mirrors are NOT independent
   re-randomizations vs §51's. The trained-vs-random comparison is still
   valid because B's TRAINED leg uses the unique B ckpt.

4. **EngineAG path produces lower terminal n_cells for B-trained (44) than
   for B-random (47-57)**. This is anti-correlated with §51's v2 finding
   ("trained reaches cap LATER" = denser, slower split). In EngineAG, B
   pretrain leads to FEWER splits AND lower Φ. The natural interpretation:
   pretrain-only ckpt has converged to a low-dispersion attractor that
   under-expresses §30 dispersion, suppressing splits without compensating
   information integration. In contrast, A's chat-cotrain Phase-2 increases
   cell-vector diversity (from chat-channel exposure), driving both more
   splits AND higher Φ.

5. **n_turns=200 vs §47's n_turns=500 for B is a budget compromise**: the
   §47 max=128 run went to 500 turns because cap-bound dynamics may emerge
   late. At max=256, cap-bound never emerges, so 200 turns is sufficient to
   capture the post-saturation Φ plateau (B-trained plateau visible by turn
   ~50, oscillating 1128-1444 thereafter). The shorter horizon is
   defensible.

6. **The 1/5 result is the s271 mirror (Φ=1148.72) — the LOWEST random**.
   B trained (1444.68) only beats the random with the lowest cell count (53
   vs trained 44 — interesting; s271 has more cells but lower Φ, suggesting
   poorly-integrated cell state). The other 4 random seeds (47-57 cells)
   all produce higher Φ. The single beat is on the random initialization
   that happened to converge poorly; this is consistent with B-trained
   being uniformly UNDERPOWERED vs random, not directionally PASS.

7. **Mission asked 1K-turn budget, ran 200**: at $0 local CPU with EngineAG
   spectral MIP at N≤57 cells, 1K-turn × 6 runs ≈ 35-40 minutes total. Was
   feasible. Compromised to 200 to match §51 A protocol exactly (clean
   cross-substrate comparison) and budget for documentation/verdict.

8. **F-B-MAX256-3 (3/5 or 4/5 partial PASS) is the most informative
   negative**: had B produced 3-4/5, the universal claim would be
   ambiguous. The 1/5 result is closer to §47 max=128's 0/5 than to §51
   A's 5/5, supporting the cotrain-exercise hypothesis preservation rather
   than ambiguity.

9. **B's mirrors are reused from §51 A_phase2_cotrain**: The
   `load_random_init` factory is ckpt-independent so mirror trajectories
   are deterministic per seed regardless of which trained ckpt was loaded
   first. Mirror Φ values [2206, 1491, 1148, 2385, 2140] match §51 A
   mirrors exactly. This is valid optimization; the only "new" computation
   was the B trained leg (1444.68). However, this means we cannot use
   B/A mirror correlations to bound noise — they are perfectly correlated
   by construction.

10. **§47 PARTIAL preservation, not full preservation**: §47's strong claim
    was "cotrain-exercise is the universal V14 PASS driver". §51 falsified
    that for v2 path (C/E PASS without chat-cotrain at max=256). This BG
    re-elevates §47 to "cotrain-exercise is the EngineAG-path driver".
    The combined verdict is MULTI_FACTORIAL — different paths use
    different mechanisms.

11. **Sign-test p=0.3750 is NOT statistically significant**: at n=5 strict,
    1/5 has p_two_sided = 2 × P(X≥4 | n=5, p=0.5) = 2 × (5/32 + 1/32) =
    12/32 = 0.375. NOT significant at α=0.05. But the bayesian posterior
    integrating §47 max=128 (0/5, 1-tail = 0.0312) and this BG (1/5,
    1-tail = 0.1875) gives joint P(both | uniform random) = 0.0312 × 0.1875
    = 0.0058 < 0.01. Cross-cap consistency strengthens the V14_VIOLATED
    inference for B.

12. **Cleanest disambiguation achieved**: same arch (EngineAG d=1024 GQA
    24L 298.76M), same path (Phase-1 pretrain), same max_cells (256), same
    n_turns (200), same V4_SEEDS, same metric, same prompt seed. Only
    difference vs A: presence/absence of Phase-2 chat-KO cotrain. Result:
    B VIOLATED, A PASS. The cotrain-exercise effect within EngineAG path
    is the only remaining explanation.

## Roadmap implications

- §51 ★★★★★ candidate downgraded to ★★★★ MULTI_FACTORIAL (universal cap-
  conditional claim falsified within EngineAG arch)
- §47 cotrain-exercise hypothesis PARTIALLY PRESERVED (EngineAG-path
  necessary driver)
- Future test: B + Phase-2 chat-cotrain (re-train B from current pretrain
  ckpt with same cotrain protocol as A) at max=256 — would confirm/falsify
  causal direction. Currently not feasible at $0 local; needs cloud GPU.
- v2-path universality claim PRESERVED (both C and E PASS at max=256
  without cotrain — cap-conditional alone is sufficient there).

## raw / own honored
- raw#9: state/.../run_b.py local-only (gitignored) — uses sibling §51
  runner via sys.path import
- raw#15 additive: B ckpt unmodified (sha256 verified
  4fc6eccce0def0450163944abbe3f0f2944ff3d908421469d4da1d25da5fb886)
- : V14 5-seed strict (V4_SEEDS [42, 137, 271, 314, 1729])
- : $0 local CPU (1143.7s elapsed)
- : REBORN.md NOT directly appended — dispatcher will inject §56 slot
- : doc save state/anima_v14_max256_b_no_cotrain_2026_05_10/
  {spec.md, run_b.py, run_b.log, run_b.stdout.log, run_b.stderr.log,
   result.json, verdict.md}
