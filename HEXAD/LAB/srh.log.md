# srh — cycle history

Append-only chronological log. `srh.md` 는 latest only — history 는 여기.

---

## Cycle #1 — 2026-05-22

- **focus**: tool primitive (ubm_inject + anima_spike) 작성 + wiring smoke 검증
- **change**:
  - `HEXAD/LAB/tool/ubm_inject.hexa` (167 LoC) — kosmos_parser_lib 위 build
  - `HEXAD/LAB/tool/anima_spike.hexa` (250 LoC) — chat record → spike fingerprint
  - `HEXAD/LAB/tool/lab_smoke.hexa` (240 LoC) — UBM tier=0 → synthetic d=8 chat → spike capture → JSON 저장 → self-diff
  - `HEXAD/LAB/srh.md` + `srh.log.md` skeleton (도메인 컨벤션 시범)
  - falsifier F-SRH-1..5 pre-registered in srh.md §3
- **fire**:
  - `hexa run HEXAD/LAB/tool/lab_smoke.hexa` Mac local $0 wall ~10s
  - artifact: `/tmp/lab_smoke_spike.json` (transient, 672 bytes)
  - commit `eece4fe23`
- **verdict**: **TOOL-READY** (not falsifier evidence)
  - F-LAB-1..6 **15/15 PASS** (tool wiring 검증)
  - 1차 신호 (synthetic noise, **not** F-SRH evidence):
    - UBM tier=0 (synthetic d=8) → 30 split + 2 merge / 210 inv
    - cell_pool 2 → 30 / next_id 32
    - baseline "안녕? 너는 누구야?" 21 split → UBM tier=0 30 split = +43% diff
  - 의미 해석 불가 — synthetic substrate 한계
- **next**: **Cycle #2 — production 332M pilot**
  - 332M ckpt (Phase 1A.1 path, `state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt` 597 MB) load
  - tier=0 UBM × 1 anchor × 1 control (random text length-matched) × 5 seed
  - 측정: F-SRH-1 minimum viable (UBM vs random delta only — tier sweep 은 cycle #3)
  - estimated cost: Mac CPU ~5 min/seed × 2 prompts × 5 seed = ~50 min wall $0
    OR H100 SXM ~$0.02 total (전체 2 min wall)
  - state path: `HEXAD/LAB/state/srh_t0_vs_random_pilot_2026_05_22/`
