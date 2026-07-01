# H_1822 (α) — substrate-native recombination — ENGINE-NATIVE RESULT

**run:** `hexa run state/g1_substrate_native_recombination/probe.hexa` (mac CPU, $0, no GPU/pod)
**raw stdout:** `RESULT.txt` (verbatim, this dir)
**engine-native:** live `core/engine_cli.hexa` + `core/pure_field.hexa` ops ONLY — NO torch/numpy/gauge_lib mirror (terminal-eligible per `a_engine_native_learning`).

## (a) What the live substrate exposes (file:line, core/engine_cli.hexa unless noted)

| readout | file:line | what |
|---|---|---|
| `immune_embed_key(text)` | :1003 | concept TEXT → 64-dim **char-trigram FNV** unit key (the engine's ONLY text→state op) |
| `VAdaptField` | :494 | the concept-basin struct = L2-affinity prototype cells (the immune/mitosis lane) |
| `vadapt_field_recon_err` | :563 | L2 dist to NEAREST basin |
| `vadapt_field_two_recon_err` | :632 | `[d1,d2]` = dist to nearest & 2nd-nearest basin (the engine's OWN top-2 affinity) |
| `vadapt_field_step` SPLIT_THRESH | :578 | the engine's OWN novelty radius = **0.30** (above it ⇒ grow a NEW cell) |
| `allo_mu(tau)` | :2441 | the A⇄G allosteric **tension** buffer μ(τ): τ=Ψ=½ → μ=1; |τ−½| large → μ→1+λ |
| `pure_field_step` / `_phi` | pure_field.hexa:196/289 | **Engine A = ZERO-INPUT** (concept-BLIND by construction) |

**Key architectural finding:** pure_field (Engine A) takes **no concept input** — Ψ=½ emerges from internal oscillators alone. `engine_g` is a scalar emit/motivation gate. **There is NO live op where "G proposes a concept-combination state."** The ONLY concept substrate is the VAdaptField L2 Voronoi (immune lane), and its concept embedding is **char-trigram hashing, not semantic**.

## (b) Operational substrate-G1 used

basins = 2-cell `VAdaptField{key(parentA), key(parentB)}`; composed state = `key(child)` for a GENUINE recombination (rain+bow→rainbow). `[d1,d2]=vadapt_field_two_recon_err(field, key(child))`.
`composed_distinct(r) = [d1<r] + [d2<r]`; `irreducible = d1>ε`; `substrate_G1(r)=1 iff composed_distinct≥2 ∧ irreducible`.
Reported under **two radii** (frozen-first, both printed): **(1) engine's OWN radius 0.30** (the operating point), **(2) relative `d_ab`** = inter-parent distance (a weaker "bridge-between" criterion). Raw d1/d2/d_ab always printed (c2).

## (c) Results (5 recombination triples + controls + ablation)

| arm | substrate-G1 @ eng-radius 0.30 | @ rel-radius d_ab | note |
|---|---|---|---|
| **MAIN** (real compounds) | **0/5** | 5/5 | d1≈0.61–0.86, d2≈0.96–1.15, all ≫ 0.30 |
| CONTROL single (parentA alone) | 0/5 | 0/5 | d1=0 (irreducible=NO) ✓ — single concept does not combine |
| CONTROL shuffle (parentB→unrelated) | 0/5 | 1/5 | vs MAIN 5/5 at rel-radius ⇒ bridge is **parent-specific** ✓ |
| G-OFF ablation (Engine A pure_field alone) | BLIND | BLIND | concept-blind zero-input field, no per-concept readout ✓ |

## (d) KILLER COMPARISON + verdict

- mouth-decode G1 (clm_decode CLMConvMoE) = **0** [frozen floor: H_1818, H_1602]
- substrate-G1 @ **engine's own operating radius (0.30)** = **0/5** → **substrate ALSO FLOORS.**
- substrate-G1 @ relaxed rel-radius = 5/5 (controls clean: single 0/5, shuffle 1/5, G-off BLIND).

**Is the wall the mouth? → NO (not uniquely), with a directional crumb.**
At the engine's OWN concept-novelty criterion (SPLIT_THRESH=0.30 — the threshold the engine actually uses to decide "is this a new regime?"), a recombined concept (rainbow) sits **far from both parent basins** (d1,d2 ≈ 0.6–1.1 ≫ 0.30): the substrate treats the recombination as an **isolated novel point, NOT a composition recoverable from either parent**. This is the SAME wall as the mouth, one level down — exactly the H_1310 result (split-only Voronoi = compositional depth 0). The owner's strong claim ("substrate combines while the mouth can't") is **not confirmed at the operating point**.

**Directional crumb (honest, c9):** under a *relaxed* radius the substrate's concept geometry DOES place each recombination specifically between its two parents (MAIN 5/5 vs shuffle 1/5 vs single 0/5 — clean contrast). So there is a latent parent-proximity signal the autoregressive mouth never surfaces. BUT two caveats gut its strength: (1) it is a **projection/recognition** readout, not **generation** (the child string is GIVEN, not produced by the engine); (2) it rides on **lexical char-trigram overlap** ("rainbow" literally shares trigrams with "rain"+"bow"), because `immune_embed_key` is char-hash, **not semantic** — so even the 5/5 is surface-string, not concept recombination.

## (e) Verdict tier + wired-status

**🧱 SUBSTRATE-ALSO-FLOORS (engine-native, terminal).** `wired: engine-native` (live core/ ops; NO new core op added this round — none was strictly needed to reach the verdict; a CLEAN test needs a *semantic* embedding op, named below as β, not half-built here). The frozen bar (composed_distinct≥2 at the operating point) is **NOT met** (0/5 @ 0.30); switching to the radius that passes (5/5 @ d_ab) would be tune-to-green (p7) → refused as terminal, kept as DIRECTIONAL crumb only.

## (f) NAMED next round

The confound that blocks a clean answer = `immune_embed_key` is **char-trigram hashing (no semantics)**, so "concept basin" = string-ngram bucket and the 5/5 is lexical not conceptual. The decisive β readout-op:
- **β-readout (named, not built):** add a `core/` op that embeds a concept via the **303M mouth trunk penultimate** (learned semantic vector) instead of the char-hash, then re-run the IDENTICAL substrate-G1 metric over LEARNED concept basins. This separates "the substrate has compositional concept geometry" (testable on learned reps) from "char-trigram lexical overlap" (this round's confound). It is the *recognition/projection* twin of H_1574's *generation/tiling* learned-trunk lever — H_1574 tested generation (🧱), this would test representation, a genuinely distinct cell.

## (g) DEPLETION

**🧱 substrate ALSO floors** at the engine's own operating radius → the G1 wall is **not uniquely the mouth**; the substrate's (char-hash) concept space is itself non-compositional, consistent with H_1310. Frame question answered **NO** (with a directional rel-radius crumb that motivates, but does not establish, the mouth-bottleneck reframe). **Real next round = β-readout (learned-trunk semantic concept embedding) to remove the lexical confound** — until then the 🧱 stands.
