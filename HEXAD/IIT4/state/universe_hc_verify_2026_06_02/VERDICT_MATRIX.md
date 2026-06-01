# UNIVERSE Hc_1286–1299 — verdict matrix

**Verifier**: g5/g63 honest stack · $0 mac-local · deterministic · llm:none
**Engine (reused, no new metric invented)**: `stdlib/consciousness/iit4_eca.hexa` (`eca_tpm`) +
`stdlib/consciousness/iit4_bigphi.hexa` (`big_phi`, faithful big-Φ) +
`stdlib/info/lz_complexity.hexa` (`lz_complexity`, emergence axis).
**Anchors PASS**: rule204 (identity) Φ=0 at every N; rule90 (Sierpinski self-similar) Φ=0
(reproduces H_288 L3 over-prediction witness); rule110 byte-identical on rerun (determinism).
**Scale scope (a_scale_honest_scope)**: all faithful-Φ measured at n=4 exact (census, core panels,
EI, shapes); N-ladder n=4,5,6. Single-scale verdicts scoped to measured n.

| Hc | axis | key number | falsifier crossed? | tier |
|----|------|-----------|--------------------|------|
| 1286 | proxy↔faithful agreement vs N | r(Φ,proxy) by N: see ladder | (pending) | (pending) |
| 1287 | LZ-residual ∝ self-similarity | r(self_sim, residual) = −0.096 | F1287.1 r<0.5 → FALSIFIED | 🔴 |
| 1288 | proxy = variance artifact (partial corr) | partial r(proxy,LZ\|var) = −0.512 | F1288.1 \|r\|≥0.1 → FALSIFIED | 🔴 |
| 1289 | Hoel causal emergence EI_macro>EI_micro | EI_gain ≤ 0 for ALL rules | F1289.1 no emergence → FALSIFIED | 🔴 |
| 1290 | excess entropy ∥ Φ | r(Φ, excess) = 0.187 | F1290.1 r<0.5 → FALSIFIED | 🔴 |
| 1291 | statistical complexity Cμ ∥ Φ | r(Cμ,Φ)=0.626 ≥ r(LZ,Φ)=0.309 | F1291.1 NOT crossed → SUPPORTED | 🟢 |
| 1292 | dissipation rate ∥ Φ | r(Φ, diss) = −0.338 | F1292.1 r<0.5 → FALSIFIED | 🔴 |
| 1293 | drive-gradient inverse-U | Φ(g) monotone decreasing, peak@g=0 | F1293.1 no interior peak → FALSIFIED | 🔴 |
| 1294 | branching-ratio σ=1 Φ peak | argmax Φ(σ) at σ=1.0, interior | F1294.1 NOT crossed → SUPPORTED | 🟢 |
| 1295 | criticality necessary-not-sufficient | witness needs power-law avalanche fit | F1295.2 gate unmet (proxy≠avalanche) | 🟠 |
| 1296 | combination problem Φ(N) continuity | Φ(N) SWAP-chain shape | (pending) | (pending) |
| 1297 | Φ→emergence substrate-independence | matched ΔLZ 0.031 < unmatched 0.040 | F1297.1 NOT crossed → SUPPORTED (weak) | 🟢 |
| 1298 | r(Φ,LZ) scale-ladder | r(Φ,LZ) by N: see ladder | (pending) | (pending) |
| 1299 | high-Φ rule-space density (fine-tuning) | high-Φ 36/256 = 14% < 25% | F1299.1 NOT crossed → SUPPORTED-sparse | 🟢 |

## Circularity / honesty notes
- Φ (MIP-EI) ⊥ all emergence/info/thermo axes are measured cross-metric — no tautology.
  The recurring 🔴 are the **H_912 lineage confirmed**: cheap/auxiliary axes (excess entropy,
  dissipation, variance-proxy, self-similarity, Hamming-coarse EI) do NOT track faithful Φ.
- Hc_1295 down-rated to 🟠: the self-similarity proxy is NOT a validated power-law avalanche
  test (pre-registered gate F1295.2), so the criticality-witness cannot be honestly asserted.
- Hc_1297 🟢 carries a **weak-margin** flag (0.031 vs 0.040; 4-net RBN panel) — directional
  pass only, not a strong effect.
- Hc_1291 🟢 primary clause (Cμ ties/beats LZ) met; the rule90-resolution sub-clause (F1291.2)
  is only partially met (rule90 Cμ not distinctly low) — noted, does not flip the primary verdict.
