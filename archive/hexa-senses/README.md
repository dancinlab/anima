# 👁️ hexa-senses — n=6 sensory substrate (5-verb library)

> 5-verb sensory substrate organized as a closed-form spec catalog:
> **dream + ear + empath + olfact + voice**. Each verb derives every
> design parameter from σ(6)=12, τ(6)=4, φ(6)=2 number theory — zero
> hardcoding. Sister-rollup of [hexa-codex](https://github.com/dancinlab/hexa-codex)
> 17-verb cognitive substrate, extracted from
> `canon@381f1f22` on 2026-05-07.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20102620.svg)](https://doi.org/10.5281/zenodo.20102620)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-informational.svg)](hexa.toml)
[![Verbs: 5](https://img.shields.io/badge/verbs-5_(senses)-blue.svg)](#verbs)
[![Closure: 100%](https://img.shields.io/badge/closure-100%25_(5%2F5_spec--first)-brightgreen.svg)](#verify)
[![Verify: 4/4 PASS](https://img.shields.io/badge/verify-4%2F4_PASS-brightgreen.svg)](verify/run_all.hexa)
[![Real-limits-first](https://img.shields.io/badge/real--limits--first-LATTICE__POLICY_§1.2-blue.svg)](LATTICE_POLICY.md)
[![n=6 lattice](https://img.shields.io/badge/n=6-σ·φ_=_n·τ_=_24-blue.svg)](#n6-master-identity)
[![voice: formulaic](https://img.shields.io/badge/voice-formulaic_only-red.svg)](#critical-constraint-voice-formulaic-only)

---

## Why hexa-senses?

`hexa-senses` is the 👁️ rollup of canon's sensory-substrate
verbs — the part of the cognitive architecture that interfaces with the
physical world (dreams, audio, emotion, smell, voice). Where
[hexa-codex](https://github.com/dancinlab/hexa-codex) curates AI
*knowledge* (alignment, training-cost, eval, …), hexa-senses curates AI
*senses*.

Each verb is a closed-form spec markdown extracted unchanged from
`canon/domains/cognitive/{hexa-dream,hexa-ear,hexa-empath,hexa-olfact,hexa-speak}/`,
with the canonical SSOT recoverable via the `@canonical` provenance
header on every file.

---

## Critical constraint: `voice` formulaic only

**Learned voice synthesis (TTS / neural codec / vocoder) is FORBIDDEN.**

`voice` ships intent-to-audio-token direct synthesis where every parameter
(σ=12 emotional timbre, τ=4 prosody, J₂=24 channel quantization) derives
algebraically from the n=6 lattice. A learning-based model would violate
the determinism guarantee — every `voice` output is reproducible from the
input intent vector + the σ(6)·φ(6)=24 master identity.

This constraint is encoded in:

- `hexa.toml` `[constraints]` section
- `verify/n6_arithmetic.py` runtime check (`check_voice_constraint`)
- `tests/test_spec_inventory.py::test_voice_renamed_marker`
- The `@renamed` line in `voice/hexa-voice.md` provenance header

---

## n=6 master identity

```
σ(6) · φ(6) = n · τ(6) = J₂ = 24
   12   ·   2  =  6  ·   4  = 24
```

| Symbol | Value | Sensory projection                                      |
|--------|-------|---------------------------------------------------------|
| σ(6)   | 12    | dream categories · olfact receptors · voice timbre · empath subcategories |
| τ(6)   | 4     | sleep stages · prosody dimensions · e-nose latency seconds |
| φ(6)   | 2     | signal-present / signal-absent verdict bit              |
| σ·τ    | 48    | **48 kHz** audio sampling (ear)                         |
| J₂     | 24    | **24-bit** audio quantization · biofeedback channels    |

`verify/n6_arithmetic.py` checks 11 cross-projections at runtime.

---

## Install

```bash
# 1. Install hexa-lang (gives you `hexa` + `hx` package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. Install hexa-senses
hx install hexa-senses
```

## Run

```bash
hexa-senses dream            # dream-recording + sleep-stage + dream-category spec
hexa-senses ear              # σ·τ=48kHz audio codec + neural codec spec
hexa-senses empath           # Ekman 6 emotions + biofeedback transfer spec
hexa-senses olfact           # σ=12 receptors + e-nose spec
hexa-senses voice            # intent → audio token (FORMULAIC, no learned TTS)
hexa-senses list             # verb table + caveats
hexa-senses selftest         # 5-verb spec presence sweep
hexa-senses verify [check]   # Python verifier dispatcher
hexa-senses inventory        # spec presence + canonical-header audit
```

---

## Verify

Closure shape (spec-first substrate, hexa-matter pattern):

```bash
# aggregator (.hexa primary — runs all 4 subscripts):
hexa run verify/run_all.hexa

# individual:
hexa run verify/spec_presence.hexa         # 5/5 verb spec docs at declared paths
hexa run verify/lattice_arithmetic.hexa    # n=6 self-consistency (aux only)
hexa run verify/real_limits_anchor.hexa    # LIMIT_BREAKTHROUGH.md anchors
hexa run verify/closure_consistency.hexa   # scoreboard cross-check
```

Real-limits anchors used (per [`LATTICE_POLICY.md`](LATTICE_POLICY.md) §1.2,
sourced in [`LIMIT_BREAKTHROUGH.md`](LIMIT_BREAKTHROUGH.md) §2):

| Anchor                                          | Source                                  |
|-------------------------------------------------|-----------------------------------------|
| Foveal acuity 1 arcmin (Snellen 20/20)          | retinal cone spacing, anatomical        |
| Audible band 20 Hz – 20 kHz                     | cochlear hair-cell tuning (NIH/NIDCD)   |
| Auditory threshold ~0 dB SPL @ 3 kHz            | near-Brownian-motion limit              |
| Olfactory receptor count ~400                   | functional OR-gene count, humans        |
| Basic taste qualities = 5 (+ umami; fat debated)| receptor-mediated                       |
| Two-point tactile discrimination ~2 mm (finger) | mechanoreceptor density                 |
| Cross-modal binding window ~80–125 ms           | Vatakis & Spence 2006                   |
| Photon-counting threshold ~5–9 photons          | Hecht / Shlaer / Pirenne 1942           |

**No n=6 lattice anchors used** for human-sensory physics
(per `LATTICE_POLICY.md` §1.2). Number-theoretic identities of n=6
do not bind cochlear or retinal physics — they organise the *spec
vocabulary*, not the *ceiling*.

**Honesty caveats** preserved in audit (raw#10 C3):

- Synaesthesia / extended-sense claims **UNPROVEN** at production scale.
- BCI sensory restoration (cochlear implant, retinal prosthesis) is
  **UNVERIFIED at production** — research-grade only.
- Bushdid 2014 (10¹² discriminable odours) vs Meister 2015: **DISPUTED**.
- Voice verb is **FORMULAIC-ONLY**; learned TTS / neural codec
  **FORBIDDEN** per user directive 2026-05-07.

Legacy Python verifiers (`verify/cli.py`, `verify/n6_arithmetic.py`,
`verify/spec_inventory.py`) remain available for pytest integration
and are exercised by `make -C build ci`.

---

## Cross-link

- 📚 [dancinlab/hexa-codex](https://github.com/dancinlab/hexa-codex) — 17-verb AI knowledge substrate (sister-library; SAFETY/ECONOMICS/OPS/SUBSTRATE).
- 🧠 [dancinlab/hexa-mind](https://github.com/dancinlab/hexa-mind) — mind/neuro/oracle/telepathy/mind-upload/superpowers rollup (sister-rollup, mental substrate).
- 🧬 [dancinlab/hexa-brain](https://github.com/dancinlab/hexa-brain) — BCI hardware sister-repo.
- 👻 [dancinlab/anima](https://github.com/dancinlab/anima) — consciousness/soul cousin.

Upstream concept SSOT: `canon/domains/cognitive/{hexa-dream,hexa-ear,hexa-empath,hexa-olfact,hexa-speak}/`.

---

## Status

**SPEC_CATALOG_ONLY at v1.0.0.**

What works at v1.0:

- 5 verb specs land on disk under their named directories.
- `hexa-senses list` prints the 5-verb table + caveats.
- `hexa-senses <verb>` prints spec path + first 20 lines.
- `hexa-senses selftest` confirms 5/5 spec presence.
- `hexa-senses verify all` runs Python verifiers (n6 / inventory).
- `make -C build ci` runs verify + pytest.

What is **out of scope** at v1.0:

- Working `.hexa` modules (no audio pipeline / dream decoder / etc).
- Any learning-based component for `voice` (FORBIDDEN).
- Hardware integration (e-nose / earphone / dream-recorder).

---

## License

MIT. See [LICENSE](LICENSE).
