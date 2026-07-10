# CA-arc Φ verdicts (H_299–H_311) — engine-native re-measurement 2026-07-10

Re-ran the 13 pre-registered CA-arc / bio-emit hypotheses **engine-native** with the
faithful hexa IIT-4 stdlib (`stdlib/consciousness/iit4_bounded.big_phi_bounded` +
`stdlib/consciousness/iit4_eca.eca_tpm`, `a_phi_iit4_tool`) and the self-contained bio
CPG/circadian/dream sims. Each was adjudicated **strictly against its card's frozen
2026-05-26 falsifiers** (no bar moved, p7). Scripts + raw logs: this dir (`run_h*.hexa`,
`out_h*.log`).

- **Engine-native reproduction certified**: gold value rule 90 n=5 st=21 cap=4 =
  **19.49999998874698** reproduced byte-exact today (H_297/H_298/H_300/H_302/H_305 all
  agree), plus rule 60=16.5, rule 30=20.269, rule 110=17.694 — all byte-identical to the
  2026-05-26 faithful-IIT4 panel. Determinism (H_302 Call A==Call B) confirmed.
- **Faithful-IIT4 (bounded lower-bound)**: `big_phi_bounded(cap<n)` = the stdlib faithful
  system-cut engine (NOT a numpy proxy) — TERMINAL-eligible, same tier basis as the
  precedent H_297/H_298 (🟢 SUPPORTED-NUMERICAL). Honest limit: cap-bounded lower bound,
  distinctions/relations deferred; binary (≈0 vs ≫0) robust, exact magnitude is a bound.
- **Toolchain note**: a concurrent session clobbered `~/.hx/bin/build/runtime.a` at 06:07
  (undefined `_rt_format_float_native`); repaired by recompiling `num_float_core_arm64.s`
  into the archive (reversible; backup `runtime.a.bak_caarc`). Pure infra flake, orthogonal
  to the deterministic Φ values.

## ECA-Φ hypotheses (faithful IIT-4, `big_phi_bounded`)

| H | rule/n · statistic | frozen bar | fresh result | verdict |
|---|---|---|---|---|
| H_299 | rule 90 n=7 alt st=85 **cap=3** | F299.1 Φ>1.0 | **6.4999999962** · cross-cap n5=6.0 n6=4.0 | 🟢 SUPPORTED-NUMERICAL (F298.2 recovered; fresh run completes n=7 rule110/anchor panel that 2026-05-26 deferred) |
| H_300 | rule 90 n=5 cap=4 **32-state sweep** | F300.1 ≥26/32 Φ>1 | 32/32 Φ>1 · mean 21.375 · max 27.5 · st21 19.5 · **0/32 Φ=0** | 🟢 SUPPORTED-NUMERICAL (5P/1F · F300.4 FAIL: no zero-Φ fixed-point state) |
| H_301 | rule 60/110/30 n=5 cap=4 32-sweep | F301.1-6 | 6/6 headline PASS · distinct 60=6 110=32 30=29 · rule60 st21=**18.5** (sorted-idx) | 🟢 SUPPORTED-NUMERICAL (7P/1F · F301.8 FAIL = the 18.5 sorted-index artifact → spawned H_302/H_303) |
| H_302 | rule 60 n=5 st21 cap=4 determinism | F302.1-6 | Call A==B=16.5 byte-id · gold 19.5 · true rule60=16.5 · F302.5 locator (none) | 🟢 SUPPORTED-NUMERICAL (engine deterministic; 18.5 = H_301 sort artifact, true 16.5; F302.5 provenance-locator float-fragile) |
| H_303 | true st21 + anchor sweep | F303.1-8 | rule60=16.5 110=17.694 30=20.269 · anchors 204/0 all-zero | 🟢 SUPPORTED-NUMERICAL (7P/1F · F303.5 FAIL reveals rule110 alt=17.694 is outlier-LOW → H_301 alt-fair-110 was tautological) |
| H_304 | rule 110 mean-Φ n=4/5/6 cap=3 ensemble | F304.1-6 | mean 11.95→27.07→**28.48** (n=6 NEW) · alt 7.66→17.69→6.795 | 🟢 SUPPORTED-NUMERICAL (6P/0F · mean trajectory monotone, no dip; alt-state dip was single-point artifact; completes 2026-05-26's truncated n=6 leg) |
| H_305 | 4-rule alt-bias ratio × distinct-count | F305.1-7 | ratios 90=1.096 60=1.098 30=1.165 110=1.530 · rank-monotone | 🟢 SUPPORTED-NUMERICAL (7P/0F) |
| H_311 | rule 110 n=5 cap=4 algebraic symmetry | F311.1-5 (H3 logic) | 110: pairs=0 orbits=2 distinct=32 · 90: pairs=0 orbits=5 distinct=3 | 🟡 PARTIAL (3P/2F · F311.2 rotation-orbit PASS ⇒ H3 "32-distinct=no-symmetry" FALSIFIED; complement absent both rules; F311.4 control FAIL) |

## Bio-emit sims (deterministic hexa · NO Φ · `a_phi_iit4_tool` N/A)

| H | measure | frozen bar | fresh result | verdict |
|---|---|---|---|---|
| H_306 | CPG spontaneous emit | F306.1-6 | idle emit 46 · threshold-monotone · refractory · circadian gate | 🟢 SUPPORTED-NUMERICAL (6P/0F) |
| H_307 | anima emit-anchor vs CPG | F307.1-5 | 14 files · 10 steps · 5 langs · cpg/anima ratio 16.4 | 🟢 SUPPORTED-NUMERICAL (5P/0F) |
| H_308 | smooth circadian finite ratio | F308.1-6 (≥4/6=SUPPORTED) | peak 46 trough 16 ratio **2.875** | 🟢 SUPPORTED-NUMERICAL per frozen ≥4/6 (5P/1F · F308.1 FAIL: 2.875 below biology [3,15]) |
| H_309 | sharper bump biology-range | F309.1-6 | peak 41 trough 0 ratio **∞** | 🔴 FALSIFIED-HEADLINE (5P/1F · F309.1 FAIL: overshoot to trough=0/∞; H_308 undershoot 2.875 + H_309 overshoot ∞ bracket but neither hits [3,15]) |
| H_310 | 5-stage dream emit gating | F310.1-6 (≥4/6=SUPPORTED) | WAKE=18 N1=N2=N3=REM=0 · distinct=2 | 🟡 PARTIAL (4P/2F · frozen ≥4/6 grants SUPPORTED, but F310.1 heterogeneity + F310.4 REM-sparse FAIL — WAKE-dominant ultradian gating confirmed, fine stage structure not) |

## Tally
- Faithful-IIT-4 (bounded) verdicts: **8** (H_299,300,301,302,303,304,305,311).
- Bio-sim deterministic-hexa verdicts: **5** (H_306,307,308,309,310) — no Φ claim.
- numpy-proxy DIRECTIONAL: **0**.
