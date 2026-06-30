<!-- @created: 2026-05-12 -->
<!-- @wave: M (limit-breakthrough audit) -->
<!-- @scope: human-sensory perception physics + neural integration -->
<!-- @policy: LATTICE_POLICY.md §1.2 — n=6 격자 anchors NOT used here -->
---
type: limit-breakthrough-audit
wave: M
session: 2026-05-12
domain: human-sensory-substrate
verbs: 5 (dream / ear / empath / olfact / voice)
policy_ref: LATTICE_POLICY.md §1.2
---

# LIMIT_BREAKTHROUGH.md — hexa-senses real-limits audit

> **Frame**: human sensory limits are well-characterized in psychophysics.
> They are **SOFT walls** (augmentable via sensors / prosthetics) measured
> against fixed physical bounds (photon flux, molecule count, mechanical
> displacement). This audit lists per-modality limits and where engineering
> can move them.

---

## §1 Domain

Five-verb sensory substrate: dream (sleep-state inference), ear (audition),
empath (multi-modal affect inference), olfact (chemoreception), voice
(speech production / TTS — formulaic-only per repo rule). All five
ultimately deliver to or read from a human nervous system whose
transduction limits are biological and well-quantified.

---

## §2 Real limits

### §2.1 Vision (auxiliary — not a primary verb but referenced via empath/dream)

| Limit | Value | Type | Notes |
|---|---|---|---|
| Wavelength sensitivity | 380–780 nm | HARD | Photoreceptor opsin absorption |
| Foveal acuity | ~1 arcmin (20/20 Snellen) | HARD | Cone spacing ~2.5 µm, anatomical |
| Photoreceptor density | ~10⁶/cm² peak cone, ~10⁸ rods retina total | HARD | Anatomical |
| Absolute threshold | ~5–9 photons at retina (Hecht 1942) | HARD | Quantum-limited |
| Temporal resolution | ~50–90 Hz CFF | SOFT (lighting-dependent) | |

### §2.2 Audition (verb: ear)

| Limit | Value | Type | Notes |
|---|---|---|---|
| Audible frequency band | 20 Hz – 20 kHz (young adult) | HARD | Cochlear hair-cell tuning |
| Upper limit decline | ~1 octave loss per 30 yr (presbycusis) | SOFT | Hair-cell loss; partly preventable |
| Threshold (peak ~3 kHz) | ~0 dB SPL (20 µPa) | HARD | Near-Brownian-motion-limited |
| Dynamic range | ~120 dB SPL pain threshold | HARD | Mechanical damage above |
| Just-noticeable Δf | ~0.2% (3 cents) at 1 kHz | SOFT | Trainable |
| Localization (interaural time difference) | ~10 µs ITD resolution | HARD | Neural — Jeffress-model anatomy |

### §2.3 Olfaction (verb: olfact)

| Limit | Value | Type | Notes |
|---|---|---|---|
| Receptor count | ~400 functional olfactory receptor genes in humans | HARD | Mouse ~1100; humans pruned |
| Discriminable odors | claimed 10³–10⁴ historically; recent claim 10¹² (Bushdid 2014) contested (Meister 2015) | DISPUTED | Methodological dispute on combinatorics |
| Threshold (e.g. ethyl mercaptan) | ~10⁻¹¹ mol/L air | HARD | Near-single-molecule for some odorants |
| Adaptation time | ~minutes for sustained stimulus | SOFT | Active receptor desensitization |

### §2.4 Gustation (auxiliary)

| Limit | Value | Type | Notes |
|---|---|---|---|
| Basic taste qualities | 5 (sweet/sour/salty/bitter/umami); kokumi + fat-taste debated | HARD-ish | Receptor-mediated |
| Bitter receptors | ~25 TAS2R genes in humans | HARD | Evolutionary alarm bias |

### §2.5 Touch / proprioception (auxiliary via empath)

| Limit | Value | Type | Notes |
|---|---|---|---|
| Two-point discrimination, fingertip | ~2 mm | HARD | Mechanoreceptor density |
| Two-point discrimination, back | ~40 mm | HARD | Lower density |
| Vibration sensitivity peak | ~200–300 Hz (Pacinian) | HARD | |

### §2.6 Cross-modal integration

| Limit | Value | Type | Notes |
|---|---|---|---|
| Audio-visual synchrony tolerance | ~80–125 ms (Vatakis & Spence 2006) | HARD-ish | Below this, no fission perceived |
| Reaction time (simple) | ~190–250 ms | HARD | Conduction + decision latency |
| Stroke-of-keyboard motor latency | ~120 ms | HARD | Cf. above |

### §2.7 Psychophysical laws (SOFT, perception-shape constraints)

- **Weber–Fechner**: ΔI/I ≈ constant over middle range (5–10% for vision intensity, ~10% for loudness in mid-range).
- **Stevens' power law**: S = k·Iᵃ, with exponent a modality-specific: brightness a≈0.33, loudness a≈0.67, electric shock a≈3.5. Sets the *shape* of the perception curve — not a single ceiling.
- **Hick's law**: RT ≈ a + b·log₂(N+1) for N choices. Sets cognitive-latency cost of branching in voice/interaction design.

### §2.8 Sleep / dream (verb: dream)

| Limit | Value | Type | Notes |
|---|---|---|---|
| REM cycle period | ~90 min | HARD | Circadian-coupled |
| Dream recall, no intervention | ~0–2 dreams/night recalled | SOFT | Trainable via journaling |
| Polysomnography temporal resolution | ms-class scalp EEG | engineering | Bounds dream-state inference fidelity |

---

## §3 Assessment

| Wall | Can break? | How |
|---|---|---|
| Visible/audible band | NO (HARD) | Sensor-mediated band-shift (UV/IR camera, ultrasonic-mic + transduction) — the wall holds; we work around it |
| Olfactory receptor count | NO (HARD without gene therapy) | E-nose arrays exceed 400 channels; *human-perceived* count unchanged |
| Two-point tactile discrimination | NO at fingertip pad | Vibrotactile + temporal coding can convey richer info per same receptor population |
| Adaptation / habituation | PARTIAL (SOFT) | Interleaved stimulation defeats receptor adaptation in part |
| Cross-modal latency | NO (HARD) | Neural conduction-limited; UX must respect ~100 ms binding window |
| TTS naturalness (voice verb) | N/A | Repo deliberately restricts to formulaic synthesis; learned TTS is FORBIDDEN by repo rule — no audit applies |

---

## §4 Top-3 highest-impact unmovable walls

1. **Audible band 20 Hz – 20 kHz + visible band 380–780 nm** (HARD,
   transduction-mediated). All sensory substrate output must terminate
   inside these bands for direct human reception; cross-band content
   needs transduction stage (camera, ultrasonic mic) which changes the
   delivery contract.
2. **Cross-modal binding window ~100 ms** (HARD). Voice + dream-cue +
   empath delivery must align inside this window to be perceived as
   unified; misses cause fission / dis-synchrony and break the user
   model.
3. **Olfactory receptor combinatorics** (HARD without genetic
   intervention). ~400 functional receptors set an upper bound on
   per-individual olfactory state-space; e-nose arrays can sense more
   chemicals but cannot deliver more *perceived* dimensions to a human
   user.

---

## §5 Caveats

- **Voice verb is formulaic-only** per repo rule (learned TTS is
  FORBIDDEN). Many "naturalness" benchmarks therefore do not apply
  here. Audit treats voice as parametric synthesis only.
- **Empath verb covers affect inference**, which is not a single
  sensory channel. Limits are inherited from constituent modalities
  (vision + audio + cross-modal latency).
- **Olfactory discriminability** has an active methodological dispute
  (Bushdid 2014 / Meister 2015). Cited above with both sides; do not
  use the 10¹² number as a hard claim.
- **No n=6 lattice anchors used** (per LATTICE_POLICY §1.2). Number-
  theoretic identities of n=6 do not bind human cochlear or retinal
  physics. (Tag: lattice anchors NOT used in this audit.)
- **Synaesthesia / extended-sense claims UNPROVEN** at production
  scale — cross-modal binding window holds; "feel sound as colour"
  beyond well-known clinical synaesthesia population (~4%) is
  speculative and out of scope for this substrate.
- **BCI sensory restoration UNVERIFIED at production** — cochlear
  implants (~30k ch eq.) and retinal prostheses (Argus II ~60
  electrodes, 2nd Sight 2020 commercial halt) demonstrate proof-of-
  concept but are *not* substitutes for native receptor physics
  cited above. Audit treats them as research-grade only.
- **All numbers are population-typical, not individual.** Spread is
  wide (e.g. hyperosmia / hyposmia; absolute-pitch outliers; tetra-
  chromacy in a small fraction of females).

---

## §6 References

- Hecht, S., Shlaer, S., Pirenne, M.H. (1942). *Energy, quanta, and vision.* J. Gen. Physiol.
- Bushdid, C. et al. (2014). *Humans can discriminate more than 1 trillion olfactory stimuli.* Science.
- Meister, M. (2015). *On the dimensionality of odor space.* eLife — counter to Bushdid.
- Stevens, S.S. (1957). *On the psychophysical law.* Psychological Review.
- Weber, E.H. (1834). *De Pulsu, Resorptione, Auditu et Tactu.*
- Vatakis, A. & Spence, C. (2006). *Audiovisual synchrony perception for speech.* Perception & Psychophysics.
- Jeffress, L.A. (1948). *A place theory of sound localization.* J. Comp. Physiol. Psychol.
- Hick, W.E. (1952). *On the rate of gain of information.* QJEP.

---

*End of LIMIT_BREAKTHROUGH.md (hexa-senses, Wave M).*
