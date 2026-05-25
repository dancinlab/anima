# LIMIT_BREAKTHROUGH.md — hexa-brain

> Real-limits audit (Wave M) per `LATTICE_POLICY.md §1.2`.
> Domain: **neuroscience hardware** — scalp EEG capture, signal
> processing, paradigm design, BCI decode toward intracortical-class
> chronic implants. Honest scope: this audit names the real
> neurophysiological / electrophysical / engineering ceilings the
> repo's pipeline operates against, separated by HARD / SOFT /
> BREAKABLE wall type per LATTICE_POLICY §1.2.

---

## §1 Domain identification

`hexa-brain` v1.1.0 ships a dual-subsystem pipeline:

- **`eeg/`** — 83 hexa files, real-hardware production-ready (OpenBCI
  Cyton+Daisy 16-channel scalp EEG, 250 Hz, ADS1299 24-bit ΣΔ).
- **`core/`** — 68 hexa files, paradigms + metrics + filters +
  artifact detectors.

Scales nominally from $0 scalp EEG → intracortical micro-electrode
arrays → Neuralink-class chronic implants. Current substrate: scalp
EEG. Real ceilings below apply at *that* substrate; intracortical
ceilings are noted where the spec claims to scale toward them.

---

## §2 Real limits applicable

### L1 — Scalp EEG SNR — volume conduction + skull attenuation (HARD_WALL)
- **Bound**: scalp-recorded cortical signal attenuated ~100× by skull
  (σ_skull / σ_brain ≈ 1/80; Oostendorp et al., *IEEE Trans. Biomed.
  Eng.* 2000); typical scalp EEG amplitude 10–100 µV vs. intracortical
  LFP 100 µV – 1 mV.
- **Anchor**: dura + skull + scalp conductivity. Cannot be improved
  by amplifier engineering alone; only inversion (source localization
  with MRI head model) recovers some spatial detail.

### L2 — Spatial resolution of scalp EEG (HARD_WALL)
- **Bound**: ~ 5–9 cm point-spread function on the cortex due to
  volume conduction (Nunez & Srinivasan, *Electric Fields of the
  Brain* 2006); 16 channels at 10–20 montage gives ~ 10–15 cm² per
  channel.
- **Anchor**: physics — there are only ~ 200 spatially independent
  EEG channels physically possible at the scalp before redundancy
  dominates (Freeman 1975 estimate).

### L3 — Action potential refractory period (HARD_WALL)
- **Bound**: absolute refractory ~ 1 ms, relative ~ 2–3 ms
  → maximum firing rate ~ 500–1000 Hz (Hodgkin-Huxley; Kandel
  *Principles of Neural Science* 5e Ch. 7).
- **Anchor**: Na⁺ channel inactivation kinetics. Biophysically
  forbidden to exceed.

### L4 — Synaptic delay (HARD_WALL)
- **Bound**: 0.3–5 ms per chemical synapse (Sabatini & Regehr,
  *Nature* 1996); axonal conduction 0.5–120 m/s depending on
  myelination.
- **Anchor**: vesicle release kinetics + Ca²⁺ influx. Fixed by
  ion-channel physics.

### L5 — BCI information-transfer rate (SOFT_WALL, scales w/ substrate)
- **Bound**: scalp EEG-based BCI ITR typically 10–100 bits/min
  state-of-art P300 / SSVEP (Wolpaw et al., *Clin. Neurophysiol.*
  2002, Chen et al., *PNAS* 2015 for 5.32 bits/sec SSVEP). Utah
  array motor BCI ~ 90 bits/min cursor control (Hochberg et al.,
  *Nature* 2012); recent intracortical handwriting decoder ~ 90
  char/min ≈ 6 bits/s (Willett et al., *Nature* 2021).
- **Anchor**: Shannon channel capacity C = B log₂(1 + SNR);
  raising B (bandwidth) requires more electrodes, raising SNR
  requires invasive recording. Engineering improvable across
  substrates, but each substrate has its own SNR ceiling.

### L6 — Electrode count / chronic-implant stability (SOFT_WALL, BREAKABLE_WITH_TECH)
- **Bound**: Neuralink N1 ≈ 1,024 channels (Musk, *J. Med. Internet
  Res.* 2019, white paper); Utah array 96; ECoG ~ 64–256;
  Neuropixels 384 sites (Jun et al., *Nature* 2017). Chronic
  yield decays ~ 50 % over 6–12 mo from glial encapsulation
  (Polikov et al., *J. Neurosci. Methods* 2005).
- **Anchor**: foreign-body response + electrode impedance drift.
  Engineering vector — flexible probes, mesh electronics
  (Liu et al., *Nat. Nanotechnol.* 2015), wireless miniature
  implants. Theoretical ceiling ~ 10⁶ channels (cortical neuron
  density) but no demonstrated path beyond ~ 10⁴ today.

### L7 — Amplifier thermal noise (HARD_WALL → engineering floor)
- **Bound**: Johnson-Nyquist noise V_n = √(4 k_B T R Δf). For R = 10
  kΩ electrode at 310 K, Δf = 0.5–500 Hz → V_n ≈ 0.3 µV RMS. ADS1299
  input-referred noise ~ 0.14 µV (Texas Instruments datasheet).
- **Anchor**: k_B T at 310 K. Cannot be evaded except by cooling
  (not biologically viable in chronic implant).

### L8 — Volume conduction artifact / EOG / EMG (SOFT_WALL, BREAKABLE)
- **Bound**: ocular artifact 50–500 µV at frontal channels (10× the
  cortical signal); EMG bleed 30–100 µV at temporal sites; line
  noise 50/60 Hz can be 100–500 µV without filtering.
- **Anchor**: source separation is engineering-improvable — ICA
  (Makeig et al., *Adv. NIPS* 1996), ASR (Mullen et al., *IEEE
  Trans. Biomed. Eng.* 2015), DL-based denoisers.

### L9 — Calibration / inter-subject variability (SOFT_WALL)
- **Bound**: typical BCI calibration session 20–60 min per user;
  cross-subject zero-shot decode accuracy < 60 % vs. 85–95 %
  within-subject (Lotte et al., *J. Neural Eng.* 2018).
- **Anchor**: cortical fold variability + EEG cap montage drift.
  Improvable via transfer learning, generic decoders, common
  spatial-pattern adaptive methods.

---

## §3 Per-limit breakthrough assessment

| ID | Limit | Wall type | Repo touch | Breakthrough vector | Verdict |
|----|-------|-----------|------------|---------------------|---------|
| L1 | Skull attenuation ~100× | HARD | eeg/ pipeline | Inverse source localization (MRI head model); intracortical bypass | unbreakable at scalp |
| L2 | EEG ~ 5–9 cm PSF | HARD | eeg/ + neural-mapper, topomap | High-density 256-ch caps reduce but don't break | physical ceiling |
| L3 | AP refractory 1 ms | HARD | sleep staging, BCI control | None; biophysics | unbreakable |
| L4 | Synaptic delay 0.3–5 ms | HARD | closed-loop latency budget | Engineer system latency ≤ neural latency | unbreakable |
| L5 | Scalp BCI ITR 10–100 bits/min | SOFT | bin/hexa-brain BCI | More channels, better decoder, hybrid paradigms | 2–5× improvable scalp; 100× substrate-jump |
| L6 | Chronic electrode count ~10³ | SOFT/BREAKABLE | roadmap (intracortical) | Neuralink-class threading robots, mesh electronics | ~10⁴ near-term, 10⁶ theoretical |
| L7 | Johnson noise 0.3 µV | HARD floor | ADS1299 tuning, eeg_recorder | None at body T | hard floor |
| L8 | EOG/EMG artifact | SOFT | ICA, ASR, artifact detectors | ML-based denoisers | improvable to ~80–90 % SNR recovery |
| L9 | Calibration session 20–60 min | SOFT | calibration tools | Transfer learning, generic decoders | 5–10× reduction realistic |

---

## §4 Top-3 breakthrough opportunities

### #1 — Source-localized scalp EEG with MRI head model (rides L1, L2)
For `eeg/` neural-mapper + topomap pipeline: integrate boundary-element
or finite-element forward model (per-subject MRI when available, or
template MNI head model otherwise) and use sLORETA / eLORETA /
beamformer inverse to recover ~ 2–3 cm cortical resolution from
16-channel scalp EEG. Cannot break L1's 100× attenuation but
exploits *all* available scalp information. Realistic deliverable:
hexa-brain inverse-solver module that takes the existing topomap
output and projects to anatomical ROIs.

### #2 — Hybrid BCI paradigms — SSVEP + motor imagery + P300 (rides L5)
Single-paradigm scalp BCI tops out near Wolpaw's 100 bits/min.
Hybrid fusion (Allison et al., *J. Neural Eng.* 2010) demonstrated
1.5–2× ITR by combining steady-state evoked + endogenous control.
Combined with riemannian-geometry decoders (Barachant et al.,
*IEEE Trans. Biomed. Eng.* 2012), realistic 2–3× ITR over current
hexa-brain BCI control spec. Does **not** approach Neuralink-class
intracortical performance — that requires substrate jump (L6).

### #3 — Transfer-learning generic decoder (rides L9)
For the eeg/ calibration suite: ship a pre-trained subject-pool
decoder (riemannian + deep alignment per Wei et al., *Neurips*
2022) that achieves > 75 % zero-shot accuracy and shrinks per-user
calibration from 20–60 min to 2–5 min. Critical for any
consumer-facing BCI claim.

---

## §5 Honest caveats

1. **Scalp EEG cannot match intracortical performance.** L1 (100×
   skull attenuation) and L2 (~5–9 cm PSF) are biophysics. Any
   spec claim implying "EEG-class consumer BCI = Neuralink" is a
   falsifier trigger.
2. **OpenBCI Cyton+Daisy is a research-grade $1.5k device.** It
   is not FDA-cleared as a clinical EEG. Any clinical claim is
   out of scope and not licensed.
3. **The σ(6)=12 / J₂=24 / n=6 lattice is organising vocabulary
   for axis count and pillar structure** — not evidence about
   the brain. Cortical neurons do not "follow n=6"; this is
   §1.1 self-imposed-ceiling territory if used as evidence.
4. **"Multi-EEG telepathy" (PLV, IBC) protocols** in the repo
   measure inter-brain synchrony — a real, replicated
   neuroscience phenomenon (Hasson et al., *Trends Cogn. Sci.*
   2012). But synchrony ≠ information transfer; do not claim
   thought transmission.
5. **Closed-loop sleep staging** must report Cohen's κ vs.
   AASM-scored polysomnography (consensus standard, ~ 0.7–0.8
   inter-rater human agreement). EEG-only staging caps at
   κ ≈ 0.75 (Phan et al., *IEEE Trans. Biomed. Eng.* 2019).
6. **Consciousness parameters / golden-zone Phi ratchet** —
   IIT-derived Φ is computationally hard (NP-hard for general
   networks) and its measurement on scalp EEG is necessarily
   approximate. Spec must declare which approximation
   (PCI, AIS, Φ*, Φ_R) is used.
7. **Bremmerman / quantum-class limits do not apply to neurons.**
   Cortical computation is firmly classical-statistical at
   body temperature; do not invoke Bekenstein bounds for the
   brain.
8. **L3, L4, L7 are biophysics-forbidden.** L5, L6, L8, L9 are
   engineering-improvable but with declared substrate-dependent
   ceilings.

---

## §6 References

- Oostendorp TF, Delbeke J, Stegeman DF. The conductivity of the
  human skull: results of in vivo and in vitro measurements. *IEEE
  Trans. Biomed. Eng.* 47:1487–92 (2000).
- Nunez PL, Srinivasan R. *Electric Fields of the Brain: The
  Neurophysics of EEG*, 2nd ed., Oxford (2006).
- Kandel ER et al. *Principles of Neural Science*, 5e, McGraw-Hill
  (2013).
- Sabatini BL, Regehr WG. Timing of neurotransmission at fast
  synapses in the mammalian brain. *Nature* 384:170–2 (1996).
- Wolpaw JR et al. Brain-computer interfaces for communication and
  control. *Clin. Neurophysiol.* 113:767–91 (2002).
- Chen X et al. High-speed spelling with a noninvasive brain-computer
  interface. *PNAS* 112:E6058–67 (2015).
- Hochberg LR et al. Reach and grasp by people with tetraplegia using
  a neurally controlled robotic arm. *Nature* 485:372–5 (2012).
- Willett FR et al. High-performance brain-to-text communication via
  handwriting. *Nature* 593:249–54 (2021).
- Jun JJ et al. Fully integrated silicon probes for high-density
  recording of neural activity. *Nature* 551:232–6 (2017).
- Polikov VS, Tresco PA, Reichert WM. Response of brain tissue to
  chronically implanted neural electrodes. *J. Neurosci. Methods*
  148:1–18 (2005).
- Liu J et al. Syringe-injectable electronics. *Nat. Nanotechnol.*
  10:629–36 (2015).
- Makeig S et al. Independent component analysis of
  electroencephalographic data. *Adv. NIPS* 8:145–51 (1996).
- Mullen TR et al. Real-time neuroimaging and cognitive monitoring
  using wearable dry EEG. *IEEE Trans. Biomed. Eng.* 62:2553–67
  (2015).
- Lotte F et al. A review of classification algorithms for EEG-based
  brain-computer interfaces: a 10-year update. *J. Neural Eng.*
  15:031005 (2018).
- Allison BZ et al. Toward a hybrid brain-computer interface. *J.
  Neural Eng.* 7:026007 (2010).
- Barachant A et al. Multiclass brain-computer interface
  classification by Riemannian geometry. *IEEE Trans. Biomed. Eng.*
  59:920–8 (2012).
- Hasson U et al. Brain-to-brain coupling: a mechanism for creating
  and sharing a social world. *Trends Cogn. Sci.* 16:114–21 (2012).
- Phan H et al. Joint classification and prediction CNN framework for
  automatic sleep stage classification. *IEEE Trans. Biomed. Eng.*
  66:1285–96 (2019).
- Texas Instruments. ADS1299 datasheet (2017).

---

*Wave M — real-limits audit; n=6 lattice not used as cortical
evidence. HARD walls L1, L2, L3, L4, L7 are biophysics-forbidden;
SOFT walls L5, L6, L8, L9 admit 2–10× engineering improvement.*
