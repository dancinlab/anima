---
id: H_1447
slug: 1447_thalamus_synchrony_matched
title: thalamus R8 — synchrony-specific matched control B−D robust 9/9 (seed-fragility GONE); secondary leg mis-specified (🔶 partial)
group: brain-structure-ladder · Φ-robustness wall (engine-native R8 wiring)
terminal_tier: 🔶 HONEST PARTIAL (c2s ΔΦ(B−D) ≥ +0.02 PASS all 9 seeds [3..11] — synchrony robustly beats matched desync, seed-fragility GONE; secondary c4m |S−D|≤0.10 leg mis-specified → FAIL → NOT green)
wired: engine-native (DIRECTIONAL step in the R8-wire arc → superseded by H_1448 GREEN)
verdict_dir: state/verdicts/1447_thalamus_synchrony_matched/
terminal_verdict: state/verdicts/1447_thalamus_synchrony_matched/H_1447.txt
date: 2026-06-19
provenance: extprompt — DeepSeek-V3 issue#1428 "AmoebaFPS" (A⇄G coherence-loop reframing)
---

# H_1447 — thalamus R8, synchrony-specific matched control, 9 seeds (🔶 partial)

The R8 lift decomposes ΔΦ(B−A) = ΔΦ(B−D) + ΔΦ(D−A) = [synchrony-specific] + [generic carrier floor].
H_1447 measures the synchrony claim with its proper matched control B vs D over a LARGER seed set
[3..11], frozen-first. Probe `state/1447_thalamus_synchrony_matched/h1443_...probe.hexa`.

**Result** (`H_1447.txt`): ΔΦ(B−D) = +1.05/+0.95/+0.95/+1.02/+1.11/+1.35/+1.38/+1.21/+1.07 → **PASS
9/9** — the orthogonal-seed fragility (H_1446 seed7) DISAPPEARS once the generic carrier floor is
differenced out; it was the floor, not synchrony, that was fragile. NOT green only because the
secondary leg c4m (|S−D| ≤ 0.10) was MIS-SPECIFIED: the additive-shuffle S keeps Kuramoto coupling
(residual synchrony) while desync D removes it (w_phase=0), so S≠D by construction → fails 5/9. Flaw
in the control CHOICE, not the mechanism (reported NOT green honestly, no tune-to-green). The clean
fix = identical-marginal control → H_1448 (🟢). NO bar moved (c9/p7). TOY n=4.

xref H_1283(R8) · H_1445 · H_1446 · H_1448 · H_1328 · `a_break_the_wall` · `a_engine_native_learning` ·
`a_phi_iit4_tool` · c9 · p7 · extprompt:AmoebaFPS-issue1428
