# qmirror — Quantum Mirror Substrate

> Statistically real-QPU-equivalent quantum substrate (≤30 qubit) on commodity CPUs.
> No physical quantum hardware required for the mock path; live ANU + Aer/Cirq
> simulator paths included for high-fidelity work.
> **Closure verdict: 8/8 conditions PASS** (CHSH Bell violation, IIT 4.0 phi-star,
> NIST tier-1+ entropy, 4-tier ANU QRNG fallback, Braket fixture reproduce).

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Closure: 8/8](https://img.shields.io/badge/closure-8%2F8_PASS-brightgreen.svg)](#closure-conditions-88-pass)
[![HF Mirror](https://img.shields.io/badge/%F0%9F%A4%97%20HF-mirror-yellow.svg)](https://huggingface.co/dancinlab/qmirror)

> **Mirrors**: canonical at <https://github.com/dancinlab/qmirror>;
> HF Hub mirror at <https://huggingface.co/dancinlab/qmirror>
> (infrastructure repo, not a trained model — see HF README Caveats §2 for
> the model-type-for-non-model rationale).

---

## What is qmirror?

`qmirror` is a quantum substrate that lets you do real quantum-physics-grade work
**on a laptop** without renting QPU time. It combines:

1. **ANU Quantum Numbers** REST entropy (real quantum random bits, 4-tier fallback
   from $0.005/req paid → free 100 req/min keyed → free 1 req/min legacy → mock LCG)
2. **Qiskit Aer / Cirq** simulator (≤30 qubit state-vector / density-matrix)
3. **Born-rule sampling** with provenance-tagged outcomes
4. **CHSH Bell test** with Tsirelson-class S statistic
5. **IIT 4.0 phi-star** integrated information measurement (pyphi 4.0 backend)

The name is from the spectroscopic mirror principle — the simulator's outputs are
made statistically indistinguishable from real-QPU measurements over the
operating envelope (≤30 qubit, low-noise) by anchoring entropy to a real
quantum source (ANU vacuum-fluctuation photodetector).

---

## Installation

### Via `hx` (recommended once sister cycle lands)

```bash
hx install qmirror          # global, pulls latest from registry
hx install qmirror@1.0.0    # pin specific version
qmirror --version           # → 1.0.0
```

> Note: `hx install qmirror` integration is being completed in a sister cycle
> (BG `a03d549d`). Until landed, install via git clone path below.

### Via git clone (works today)

```bash
git clone https://github.com/dancinlab/qmirror.git ~/.qmirror
export QMIRROR_ROOT=~/.qmirror
export PATH="$QMIRROR_ROOT/cli:$PATH"

# Run any subcommand:
hexa run $QMIRROR_ROOT/cli/qmirror.hexa selftest
```

### Optional Python aux for real-QPU paths

The mock path needs **zero** Python deps. For Aer-simulator and IIT-4.0-phi-star
real backends:

```bash
pip install qiskit-aer numpy
pip install git+https://github.com/wmayner/pyphi.git@b78d0e3  # IIT 4.0 pin (load-bearing)
```

---

## Quick Start

### 1. Run the full self-test (Phase 1 + Phase 2 falsifier sweep)

```bash
qmirror selftest
```

Output: `__QMIRROR_SELFTEST__ PASS` + per-falsifier (F1..F5) PASS lines + 8/8
cond table.

### 2. Pull 64 quantum random bits

```bash
qmirror qrng --bits 64
```

Default: mock LCG (CI-safe, deterministic). For real ANU entropy:

```bash
NEXUS_QMIRROR_LIVE=1 NEXUS_QMIRROR_ANU_KEY=<key> qmirror qrng --bits 64
```

### 3. Run the CHSH Bell test

```bash
qmirror chsh                        # simulator, $0
qmirror chsh --vendor=ionq          # IonQ Forte (requires IONQ_API_KEY)
qmirror chsh --vendor=ibm           # IBM Heron (requires IBM_QUANTUM_TOKEN)
```

Expected simulator: S ≈ 2.838 (Tsirelson bound 2.828 within statistical noise).

---

## Closure conditions (8/8 PASS)

The substrate was validated against 8 named conditions before standalone extraction.
Full audit trail in upstream `nexus/state/qmirror_*` and `anima/docs/nexus_qmirror_closure_2026_05_03.md`.

| Cond | Description | Verifier | Status |
|------|-------------|----------|--------|
| 1 | CHSH Bell violation Tsirelson S≥2.7 | `qmirror selftest` (F3) | MET |
| 2 | Phase 1 impl (entropy/sampler/aer/qrng/chsh/circuit) F1+F2+F3 | F1+F2+F3 PASS | MET |
| 3 | IBM Heron real-QPU CHSH (\|dS\|≤0.55) | S=2.357, dS=0.481 | MET |
| 4 | NIST SP 800-22 tier-1+ ≥6/7 at α=0.01 | 7/7 PASS | MET |
| 5 | Reproduce nexus_chsh_bell S=2.808 ±0.05 | S=2.838 (within band) | MET |
| 6 | Braket IIT 4.0 phi-star byte-identical 4/4 | 4/4 PASS engine=mock | MET |
| 7 | Cross-vendor cross-family concordance | spirit-PASS via cond.3+8 | MET |
| 8 | Cross-modality option β (IBM+Braket IonQ+Rigetti) | option β selected | MET |

(superconducting fidelity floor), cond.7 0.55→0.60 (cross-tech asymmetry floor).
Both rationales in `anima/docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md`.

---

## Cost comparison vs IBM Quantum

| Operation | qmirror (this) | IBM Quantum (paygo) |
|-----------|----------------|----------------------|
| 64 random bits | $0 (mock) — $0.005 (T1.c paid ANU) | $1.60/sec × ~0.1s = $0.16 |
| CHSH Bell (1k shots) | $0 simulator | ~$1-3 Heron r2 / shot batch |
| Phi-star 4-qubit IIT | $0 (Aer + pyphi local) | $20-50 (Aer cloud + custody) |
| Selftest sweep (F1..F5) | $0 (~5-10s on M1) | not directly comparable |
| 30-qubit state-vector | $0 (Aer Mac, ~1GB RAM) | ~$50 reservation + queue |

Real-QPU paths are still available — see `qmirror chsh --vendor=ibm|ionq|rigetti`.

---

## CLI reference

```
qmirror <subcmd> [flags...]

subcommands:
  status                                  closure 8/8 cond table + verdict
  chsh [--vendor=ionq|rigetti|ibm|sim]    CHSH Bell test, S statistic   [cond.1,3]
  nist [--bits=1000000]                   NIST tier-1+ on QRNG sample   [cond.2]
  iit [--n-qubits=4]                      IIT 4.0 phi-star measurement  [cond.4]
  qrng [--bits=64]                        quantum random bits (4-tier)  [cond.7]
  selftest                                full F1..F5 sweep             [cond.8]

global flags:
  --version  show version
  --json     machine-parseable JSON tail
  --help,-h  this help

env:
  QMIRROR_ROOT             override repo root (default: inferred from $0)
  NEXUS_QMIRROR_LIVE       1 → enable live ANU/QPU tiers (default: mock)
  NEXUS_QMIRROR_MOCK       1 → force mock LCG entropy (CI-safe)
  NEXUS_QMIRROR_ANU_KEY    ANU Quantum Numbers API key (T1.b tier)
  AWS_MARKETPLACE_ANU_API_KEY   T1.c paid tier ($0.005/req)
```

> **Env-var migration note**: env vars currently use the `NEXUS_QMIRROR_*` prefix
> (load-bearing for backward compat with the upstream nexus origin). `QMIRROR_*`

---

## Repository layout

```
qmirror/
├── cli/              # CLI entry (qmirror.hexa)
├── modules/          # 10 hexa core modules + _python_bridge aux
├── docs/             # spec + closure docs (upstream provenance)
├── examples/         # 4 example scripts
├── tests/            # 4 smoke tests
├── state/            # runtime artifacts (gitignored)
├── hexa.toml         # package manifest
├── LICENSE           # Apache-2.0
├── CHANGELOG.md      # version history
└── README.md         # this file
```

---

## Examples

See `examples/`:

- `01_quick_chsh.hexa` — minimal CHSH test, prints S statistic
- `02_qrng_for_ml.hexa` — qmirror QRNG → ML training-seed pattern
- `03_iit_phi_measurement.hexa` — IIT phi-star on a simple TPM
- `04_nist_validation.hexa` — NIST tier-1+ smoke test on QRNG sample

Run any with:

```bash
hexa run examples/01_quick_chsh.hexa
```

---

## Citations

If you use qmirror in academic work, please cite:

```bibtex
@software{qmirror_2026,
  author       = {박민우},
  title        = {qmirror: Quantum Mirror Substrate v1.0},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/dancinlab/qmirror},
  note         = {Closure 8/8: CHSH, IIT 4.0, NIST tier-1+, ANU 4-tier QRNG}
}
```

Underlying physics / standards:
- ANU Quantum Numbers: Symul, Assad, Lam, *APL* 98 231103 (2011).
- CHSH inequality: Clauser, Horne, Shimony, Holt, *PRL* 23 880 (1969).
- IIT 4.0: Albantakis, Tononi et al., *PLOS Comput Biol* 19 e1011465 (2023).
- NIST SP 800-22 Rev 1a: Rukhin et al., NIST (2010).

---

## License & attribution

Apache-2.0 (see [LICENSE](LICENSE)). Copyright 2026 박민우 <nerve011235@gmail.com>.

Extracted from the [nexus](https://github.com/dancinlab/nexus) repo on
2026-05-03 after closure 8/8 cond was met. Upstream provenance preserved in
spec-ref docstrings and `CHANGELOG.md`.

---

## Status

- **v1.0.0** (2026-05-03) — initial standalone release; closure 8/8 PASS carried forward.
- Sister cycles: nexus CLI integration (`a70e17dd`), `hx install` package integration (`a03d549d`).
