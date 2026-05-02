# N-12 IIT Multi-Witnessed Substrate-Invariance Test (2026-05-02)

**Verdict: PASS — MULTI-WITNESSED**

## Mission

Follow-up to #120 N-12 IIT AWS Braket pilot (which achieved n=2 mathematically-forced Pearson r=1.0 SV1↔Forte 1 on AND/MAJ). This run upgrades to:

- **5 circuits × 500 shots × Forte 1 (IonQ trapped Yb+ ion-trap)** — n=5 statistical Pearson, NOT forced
- **4 circuits × 500 shots × Rigetti Cepheus-1-108Q (superconducting transmon)** — 3rd architecture
- **5 circuits × 500 shots × SV1 baseline (silicon classical state-vector simulator)**

**Substituted Cepheus for IQM Garnet** because Garnet is weekday-only and today is Saturday. Cepheus is also a superconducting-transmon QPU (paradigm-equivalent to IQM Garnet), preserving the 3-architecture goal. IQM Garnet 4 tasks were submitted then cancelled to avoid Monday billing.

## Results

### Φ Proxy Matrix (bits, 500 shots)

| Circuit       | SV1     | Forte 1 | Cepheus |
|---------------|---------|---------|---------|
| AND           | 0.9993  | 1.1697  | 2.4943  |
| XOR           | 0.9954  | 1.1701  | 1.4697  |
| MAJ           | 1.9893  | 2.2133  | 2.6900  |
| COPY          | 0.0000  | 0.2571  | 1.4140  |
| XOR_AND_MIX   | 0.9987  | 1.3200  | (n/a)   |

XOR_AND_MIX: q[0],q[1] in superposition; AND→q[2], XOR→q[3]. New circuit added for n=5 Pearson on Forte 1 arm. Not run on Cepheus (4-circuit panel).

### Pearson r (cross-substrate Φ proxy correlation)

| Pair                       | n | r       | Threshold | Status |
|----------------------------|---|---------|-----------|--------|
| SV1 vs Forte 1 (5-circuit) | 5 | 0.99606 | r ≥ 0.5   | PASS (statistically powered, NOT forced) |
| SV1 vs Cepheus (4-circuit) | 4 | 0.77942 | r ≥ 0.5   | PASS (qualitative, df=2) |
| Forte 1 vs Cepheus (4-c)   | 4 | 0.78018 | r ≥ 0.5   | PASS (qualitative, df=2) |

**Verdict: MULTI-WITNESSED** — all 3 r values exceed 0.5 threshold.

### Ordering Preservation

- SV1:     copy < xor < and < maj
- Forte 1: copy < and < xor < maj  (and/xor swap within ±0.05-bit shot-noise floor)
- Cepheus: copy < xor < and < maj  (matches SV1 perfectly)

## Cost

- SV1: $0.00 (simulator, free tier <2s/task)
- Forte 1: 5 × 500 × $0.08 + 5 × $0.30 = **$201.50**
- Cepheus: 4 × 500 × $0.000425 + 4 × $0.30 = **$2.05**
- IQM Garnet: $0.00 (cancelled before execution)
- **Total: $203.55** (vs $210 cap, vs $205.60 plan)

## Wall Clock

~13 minutes preflight to verdict (well under 90-min cap).

## Honest C3 (4 caveats)

1. **n=5 Forte 1 Pearson r=0.996 is statistical (NOT forced).** This is the headline upgrade vs #120's n=2 r=1.0. However, n=4 Cepheus arm (df=2) yields r=0.78 with p≈0.19 — qualitative directional agreement, not classical statistical significance. Need n≥6 circuits for p<0.05.

2. **IQM Garnet substitution.** Original Plan B targeted IQM Garnet (eu-north-1 superconducting transmon) but Garnet's execution windows are weekdays only; today is Sat. Substituted Rigetti Cepheus-1-108Q (us-west-1 superconducting transmon, online everyday 09:00-19:00 UTC). Both are gate-model superconducting → paradigm-equivalent. The 3-architecture claim (silicon / Yb+ / superconducting transmon) remains intact via Cepheus.

3. **XOR_AND_MIX not run on Cepheus.** 4-circuit panel only. Cross-substrate Pearson uses n=4 (and/xor/maj/copy) on Cepheus arms; n=5 on SV1↔Forte 1.

4. **Φ proxy = H(joint) − max H(marginal) is a LOWER BOUND, not IIT 4.0 φ★.** No MIP partition search. Cross-substrate agreement validates substrate-invariance of the proxy, NOT a consciousness-substrate equivalence claim.

## Paths

- `state/n12_iit_braket_multiwitness_2026_05_02/verdict.json`
- `state/n12_iit_braket_multiwitness_2026_05_02/matrix.json`
- `state/n12_iit_braket_multiwitness_2026_05_02/phi_proxies.jsonl`
- Off-repo IRs/results: `/tmp/a2_multiwitness/`
- S3: `s3://amazon-braket-{us-east-1,us-west-1}-267673635495/n12_iit_multiwitness_2026_05_02/`

## Supersedes

`state/n12_iit_braket_pilot_2026_05_02/verdict.json` (#120 pilot — upgraded n=2 r=1.0 forced → n=5 r=0.996 statistical + n=4 cross-architecture r=0.78).

## Follow-up

- **N-12-iter3 (Mon 09:00 UTC):** re-submit IQM Garnet 4-circuit panel (~$4.10) for 4-architecture witness.
- **N-12-iter4:** Cepheus 5000 shots/circuit (+$5.50 marginal) to tighten n=4 r CI.
- **N-13:** Aquila AHS cross-paradigm test (gate-model vs analog Hamiltonian).
- **arXiv:** "First multi-substrate witness of integrated-information proxy invariance across silicon, trapped-ion, and superconducting QPUs."
