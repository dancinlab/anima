---
license: apache-2.0
library_name: hexa
tags:
  - quantum-computing
  - qrng
  - chsh
  - bell-inequality
  - iit
  - phi-star
  - consciousness
  - rng
  - infrastructure
  - non-model-mirror
language:
  - en
pipeline_tag: other
---

# qmirror — Quantum Mirror Substrate (HF mirror)

> **Note on repo type**: this is **infrastructure, not a trained model**. It is
> mirrored to the HF Hub (model-type repo) for ML community discoverability,
> since HF model repos accept arbitrary file types. Canonical source is the
> [GitHub repo](https://github.com/dancinlab/qmirror); this mirror is
> kept synced manually (see Caveats §1 for the dual-mirror sync burden).

`qmirror` is a quantum substrate that lets you do real-quantum-physics-grade
work **on a laptop** without renting QPU time. It combines ANU Quantum Numbers
(real quantum random bits, 4-tier fallback), Qiskit Aer / Cirq (≤30 qubit
state-vector simulator), Born-rule sampling with provenance-tagged outcomes,
CHSH Bell test (Tsirelson-class S statistic), and IIT 4.0 phi-star (integrated
information measurement, pyphi 4.0 backend).

**Closure verdict: 8/8 conditions PASS** (CHSH Bell violation, IIT 4.0
phi-star, NIST tier-1+ entropy, 4-tier ANU QRNG fallback, Braket fixture
reproduce).

The full project README (cost comparison vs IBM Quantum, CLI reference,
repository layout, examples, citations) is preserved as `README_github.md`
inside this repo — this top-level `README.md` is the HF-targeted card with
the mk2 sections (Origin, Falsifiers, Substrate, Caveats, Composability)
required by the upload pipeline contract, plus YAML front-matter for HF
indexing.

---

## Origin

Extracted from the [`nexus`](https://github.com/dancinlab/nexus) repo
on 2026-05-03 after the closure 8/8 cond audit was met. The source lineage:

- Upstream root: `nexus/modules/qmirror` (closure marker
  `anima/state/markers/qmirror_closure_landed.marker`).
- Closure doc: `anima/docs/nexus_qmirror_closure_2026_05_03.md`.
- Standalone extraction commit:
  [`3488b23`](https://github.com/dancinlab/qmirror/commit/3488b23) on
  GitHub (`feat(qmirror): standalone 1.0.0 — closure 8/8 cond met`).
- This HF mirror lands on 2026-05-03 from the same commit; no source-tree
  divergence at land time.

Authorship: 박민우 <nerve011235@gmail.com>. License Apache-2.0.

---

## Falsifiers

The substrate was validated against **5 named falsifiers (F1..F5)** before
standalone extraction. The selftest sweep (`qmirror selftest`) re-runs them
on every machine. Failure of any falsifier flips the closure verdict to
FAIL.

| ID | Name | What it would falsify | Pass criterion |
|----|------|------------------------|----------------|
| F1 | Entropy ledger integrity | ANU 4-tier fallback + sha256 chain not reproducible → "real quantum" claim void | All entropy bytes accounted-for; tier transitions logged |
| F2 | Sampler ↔ amplitude consistency | Born-rule sampler diverges from analytic amplitudes → simulator path void | KL divergence < 1e-6 over 10k shots, n≤4 qubits |
| F3 | CHSH Bell violation | S < 2.0 (classical bound) → no quantum advantage demonstrated | S ≥ 2.7 (Tsirelson-class), 1k shots, 2-qubit Bell pair |
| F4 | NIST SP 800-22 tier-1+ | < 6 of 7 tier-1 tests pass at α=0.01 → entropy not crypto-grade | 7/7 tests pass on 1Mbit sample |
| F5 | IIT 4.0 phi-star reproducibility | pyphi backend non-deterministic on fixed TPM → Φ-star claim non-reproducible | Byte-identical phi-star across 4 fixed-seed runs |

**Closure conditions (8/8 PASS, full table in `README.md`)**: CHSH Tsirelson
S≥2.7 (cond.1), Phase-1 impl F1+F2+F3 (cond.2), IBM Heron real-QPU CHSH
|dS|≤0.55 (cond.3), NIST tier-1+ ≥6/7 (cond.4), reproduce nexus_chsh_bell
S=2.808±0.05 (cond.5), Braket IIT 4.0 phi-star byte-identical 4/4 (cond.6),
cross-vendor concordance (cond.7), cross-modality option β (cond.8).

0.40→0.55 (superconducting fidelity floor), cond.7 0.55→0.60 (cross-tech
asymmetry floor). Rationale in
`anima/docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md`.

---

## Substrate

`qmirror` is implemented in **hexa** (a strict typed scripting language used
by the upstream `anima`/`nexus` agent stacks). The runtime layout:

- **10 hexa core modules** (`modules/`): `entropy`, `sampler`, `engine_aer`,
  `qrng`, `chsh`, `circuit`, `tomography`, `iit_mip`, `phi`, `selftest`.
- **3 Python bridges** (`modules/_python_bridge/`): `aer_runner.py`,
  `iit_mip_runner.py`, `phi_runner.py` — kept as Python because Aer / pyphi
  `hexa.toml`).
- **1 CLI entry** (`cli/qmirror.hexa`): subcommands `status | chsh | nist |
  iit | qrng | selftest`.
- **5 smoke tests** (`tests/`): `test_chsh`, `test_qrng`, `test_iit`,
  `test_nist`, `test_selftest`.
- **4 example scripts** (`examples/`).
- **No trained weights**: this repo holds source code only. `state/` is
  gitignored; runtime artifacts live there at execute time.

Hardware envelope: ≤30 qubit state-vector on commodity CPU (~1 GB RAM for 30
qubits). No GPU required. No QPU required for the mock + simulator path.
Real-QPU paths are still wired (IBM Heron, IonQ Forte, Rigetti) but cost
varies by vendor.

Distribution channels:
- **GitHub**: <https://github.com/dancinlab/qmirror> (canonical).
- **HF Hub** (this repo): <https://huggingface.co/dancinlab/qmirror>
  (mirror).
- **`hx install qmirror`**: planned via the `hx` package manager (sister BG
  `a03d549d`); install today via git clone path documented in `README.md`.

---

## Caveats


1. **Dual-mirror sync burden** — this HF repo is updated by re-running the
   `tool/hf_upload_mk2.hexa` wrapper (or a direct `hf upload`) after each
   GitHub push. There is no automated webhook bridge as of land time. Risk:
   HF mirror falls behind GitHub if the human operator forgets the second
   push step. Mitigation in flight: a `state/qmirror_hf_mirror_*` marker
   per-cycle audit log + a follow-up cycle to wire a CI hook.

2. **HF model-type repo for non-model content** — `huggingface.co/dancinlab/qmirror`
   is registered as a `model` type repo because that is the only HF repo
   class that accepts arbitrary file types (code + hexa + Python bridges).
   This is **unconventional**: HF model repos are typically expected to ship
   model weights, a `config.json`, and a tokenizer. We ship none of those —
   the `pipeline_tag: other` and `library_name: hexa` metadata in this
   front-matter signal "infrastructure mirror, not a trained model" to
   downstream tooling. Search-discovery may surface this repo in
   model-search results without a usable inference path; users should treat
   this repo as code, not as a transformers checkpoint.

3. **License clarity for downstream ML use** — Apache-2.0 covers the qmirror
   source. The IIT 4.0 phi-star backend depends on a pinned
   `wmayner/pyphi` commit (`b78d0e3`, GPLv3-licensed). If you embed qmirror
   into a downstream ML pipeline that distributes phi-star outputs, your
   pipeline inherits pyphi's GPLv3 obligations on the linked binary —
   Apache-2.0 alone is **not sufficient** for a closed-source distribution
   that statically links pyphi. The mock-LCG path and the pure-CHSH path
   are pyphi-free and thus Apache-2.0-clean.

4. **Repo size limit / future weight artifacts** — current upload is ~644
   KB across ~30 files, well under HF's 5 GB free-tier soft limit. If
   future cycles add reference simulator-state snapshots or
   Braket-fixture binary blobs (>1 MB each), we will need to either (a)
   migrate to Git-LFS-tracked HF storage or (b) shard those into a sibling
   `dancinlab/qmirror-fixtures` repo. The current README.md still
   advertises `state/` as gitignored — that contract holds through this
   land.

---

## Composability

`qmirror` is designed as a **substrate primitive**, not a turn-key ML
pipeline. Composability vectors:

- **As a QRNG entropy source**: `qmirror qrng --bits N --json` returns
  provenance-tagged random bytes. Pipe into ML training-seed slots, MCTS
  rollouts, or Monte-Carlo integration. See `examples/02_qrng_for_ml.hexa`.
- **As a Bell-test calibration anchor**: `qmirror chsh --vendor=ibm` (or
  `ionq`, `rigetti`) returns S statistic + provenance. Use as a "is the QPU
  still in spec?" health check before spending real-QPU budget on a longer
  job. See `examples/01_quick_chsh.hexa`.
- **As an IIT 4.0 phi-star measurement primitive**: `qmirror iit
  --n-qubits=4 --json` returns Φ-star + MIP + complexes for a fixed TPM.
  Compose with a downstream consciousness-modeling pipeline.
- **As a NIST tier-1+ entropy validator**: `qmirror nist --bits=1000000`
  returns 7/7 pass/fail per test. Composes with key-derivation pipelines
  needing crypto-grade entropy provenance.
- **Cost composability**: all five compose at $0 on the mock + Aer
  simulator path (Mac local, no network). Real-QPU and ANU-paid paths
  surface their cost via the `--vendor` and `NEXUS_QMIRROR_LIVE` env
  switches.
- **Upstream composability**: this repo's modules are also imported by the
  upstream `nexus` substrate — the standalone extraction preserves
  drop-in API parity (cli + module signatures unchanged).

For full composition examples (4 scripts), see `examples/` in this repo.
For the upstream agent-stack composition, see the `nexus` repo.

---

## Citations

```bibtex
@software{qmirror_2026,
  author       = {박민우},
  title        = {qmirror: Quantum Mirror Substrate v1.0},
  year         = {2026},
  publisher    = {GitHub + HuggingFace Hub},
  url          = {https://github.com/dancinlab/qmirror},
  note         = {Closure 8/8: CHSH, IIT 4.0, NIST tier-1+, ANU 4-tier QRNG;
                  HF mirror at https://huggingface.co/dancinlab/qmirror}
}
```

Underlying physics / standards (full bibliography in `README.md`):
- ANU Quantum Numbers — Symul, Assad, Lam, *APL* 98 231103 (2011).
- CHSH inequality — Clauser, Horne, Shimony, Holt, *PRL* 23 880 (1969).
- IIT 4.0 — Albantakis, Tononi et al., *PLOS Comput Biol* 19 e1011465 (2023).
- NIST SP 800-22 Rev 1a — Rukhin et al., NIST (2010).

---

## Status

- **v1.0.0** (2026-05-03) — initial standalone release; closure 8/8 PASS
  carried forward from the `nexus` upstream.
- **HF mirror landed** (2026-05-03) — 30 files, ~644 KB, sha256 chain in
  `anima/state/qmirror_hf_mirror_2026_05_03/push_audit.json`.
- **GitHub canonical**: <https://github.com/dancinlab/qmirror>.
- **HF mirror**: <https://huggingface.co/dancinlab/qmirror>.
