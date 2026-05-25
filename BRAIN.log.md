# BRAIN — log

Append-only history sister of `BRAIN.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-25 — M0 architecture doc + M1 synthetic 16ch demo LANDED
- [x] M0 — `BRAIN/eeg/ARCHITECTURE.md` (5 §, Korean): stack overview · 16→8 region-collapse 전략 · LSL pull 인터페이스 · 4-region carving plan · honest scope C3
- [x] M1 — `BRAIN/eeg/state/brain_m1_synthetic_16ch_2026_05_25/run_m1.hexa` 3-config 합성 16ch EEG (fully-coupled / region-coupled / fully-independent) × 8-region collapse × big-Φ
- [x] result.json — config × big-Φ 표 (deterministic, byte-equal re-run)
- [x] README.md (Korean, IIT4 state §1-§4 template)
- [x] adapter 재사용 — `BRAIN/eeg/eeg_to_tpm.hexa` (PR #547) + stdlib/consciousness/iit4_bigphi (engine ⊥ adapter, g61)
