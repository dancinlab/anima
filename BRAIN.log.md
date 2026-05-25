# BRAIN — log

Append-only history sister of `BRAIN.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-26 — BRAIN.md 목적("왜") 섹션 + M3 마일스톤 기록

- [x] BRAIN.md placeholder → "왜(목적)" 섹션: EEG → IIT4 big-Φ = 의식 통합도 정량화 (느낌 아닌 측정 가능한 양). 흐름/엔진⊥어댑터(g61)/기존 EEG 차이/n≤8 제약 정리
- [x] M3 마일스톤 시드 — 상태별 big-Φ 비교 (깨어있음 vs 이완/눈감음 vs 수면 epoch) = "의식의 양" 정량화 검증. M2(live LSL) 이후 후속
- [x] 동기: 사용자 "EEG 로 뭘하는거야" 설명 → 목적을 도메인 SSOT 에 기록 ("마일스톤에도 일단 기록")

## 2026-05-25 — M0 architecture doc + M1 synthetic 16ch demo LANDED
- [x] M0 — `BRAIN/eeg/ARCHITECTURE.md` (5 §, Korean): stack overview · 16→8 region-collapse 전략 · LSL pull 인터페이스 · 4-region carving plan · honest scope C3
- [x] M1 — `BRAIN/eeg/state/brain_m1_synthetic_16ch_2026_05_25/run_m1.hexa` 3-config 합성 16ch EEG (fully-coupled / region-coupled / fully-independent) × 8-region collapse × big-Φ
- [x] result.json — config × big-Φ 표 (deterministic, byte-equal re-run)
- [x] README.md (Korean, IIT4 state §1-§4 template)
- [x] adapter 재사용 — `BRAIN/eeg/eeg_to_tpm.hexa` (PR #547) + stdlib/consciousness/iit4_bigphi (engine ⊥ adapter, g61)
