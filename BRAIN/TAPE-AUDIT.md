# TAPE-AUDIT — hexa-brain

Scalp EEG → intracortical-class neural decode + closed-loop BMI. Spun off from `anima/anima-eeg/` + `anima/anima-eeg-core/`. Dual-subsystem (`eeg/` + `core/`) sister of anima. Carries the BCI hardware-side ledgers anima used to hold.

## A. Audit-class ledgers (cargo / migration candidates)

- **`state/markers/`** — hexa hook markers. Standard `state/markers.tape` migration.
- **`state/berger_pass_ledger.jsonl`**, **`state/anima_eeg_impedance_ledger.jsonl`**, **`state/license_firewall_checks.jsonl`** — three append-only domain ledgers. Direct `berger-pass.tape` / `impedance.tape` / `license-firewall.tape` candidates.
- **`state/alpha_eyes_closed_audit/selftest_synth_session.jsonl`** — per-session audit; tape-shaped.
- **`eeg/state/markers/*.marker`** — second marker store (subsystem-local): `phase4_realtime_complete`, `phase4_experiment_complete`, `phase4_closed_loop_complete`, `phase4_calibrate_complete`, `phase4_eeg_recorder_complete`, `phase3_cycle3_bci_control_complete`. Per-phase milestone tape.
- **`eeg/core/quality_audit.hexa`**, **`eeg/protocols/{background_quality_audit,package_num_audit}.hexa`** — audit programs, not ledgers, but their outputs (today scattered) would land cleanly in `quality.tape`.
- **`eeg/doc/{uchg_flag_audit,openbci_ear_pad_audit,openbci_auditory_listening_protocol}_2026_05_03.md`** — per-session protocol audit notes.
- **`eeg/corpora/auditory_listening_v1/manifest.jsonl`** — corpus manifest; per-trial events.

## B. Identity surface

Medium. The hardware identity (substrate config: OpenBCI Cyton+Daisy 16ch + Galea + electrode topology) lives implicitly across `EEG.md`, `GOOGLE_CONSCIOUSNESS_CHIP.md`, `LATTICE_POLICY.md`, `.roadmap.galea`, `.roadmap.eeg`. Could become `hexa-brain/identity.tape` capturing substrate snapshot + capability baselines.

## C. Domain.md files

Present: `AGENTS.md`, `EEG.md`, `GOOGLE_CONSCIOUSNESS_CHIP.md`, `LATTICE_POLICY.md`, `LICENSE_FIREWALL.md`, `LIMIT_BREAKTHROUGH.md`, `SESSION_LOG_2026_05_12.md`. `UPPERCASE.md` convention followed. Sibling `<DOMAIN>.tape` is the natural per-domain run trace (EEG.tape per recording session, LICENSE_FIREWALL.tape per check).

## D. Per-run / per-event history surfaces

`anima-eeg/recordings/` (real recordings), `clm_eeg/` runs, `eeg/state/markers/phase*` milestones, `eeg/corpora/.../manifest.jsonl` trials, `.venv-eeg` -> anima symlink (training env). Every recording session is an event stream → `.tape` per session.

## E. Promotion candidates

- **n6 atoms** — berger-pass empirical thresholds (alpha eyes-closed gate), impedance pass criteria, license-firewall predicates → atlas atoms.
- **hxc wire** — EEG sample streams (the live OpenBCI feed) are the textbook hxc byte-wire use case.
- **n12 cells** — quality metrics × channel × time = clean n12 cube.

**Verdict: HEAVY** (5+ tape surfaces — markers ×2, jsonl ledgers ×3, audit dir, phase milestones, per-recording session, audit-doc set).
