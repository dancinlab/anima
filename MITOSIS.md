# MITOSIS — current state

@goal: anima 의 학습/성장 패러다임 — train/infer 분리 폐기 per p8, ckpt = 분기점, FT = 큰 split event. cell-pool + split + merge + persona-diff + sleep-tick 을 통합한 직교 축 M, A/G ⊥ M. v5-mitosis cotrain 5/5 PASS ckpt 581MB 를 production swap-in 경로로 회수하고, WAKE 의 imagination loop + mitosis tick 으로 inference-time 분열까지 연속
@title: 🌱 MITOSIS — 세포 분열 학습 · A/G ⊥ M 직교 축

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] mitosis_lib 회수 + stdlib 승격 — `MITOSIS/{mitosis_lib.hexa,SSOT.md}` 회수 from `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.hexa` (503L · S187-G flame port) · 12 pub fn (8 §A const-surface + 4 §B cell-pool lifecycle) · legacy 경로 보존 (비파괴) · hexa parse OK (PR #627 b64dba36)
- [x] cell-pool split-event — `MITOSIS/{split_event.hexa,split_smoke.hexa,SPLIT_EVENT.md}` PURE wrappers · mitosis_lib.hexa:276-303 check + :305-337 execute · runtime smoke 17 splits/3 merges/cap=16 · F-V5MIT-1 SPLIT-NOGRAD carry (PR #631 a160986d)
- [x] merge-event — `MITOSIS/{merge_event.hexa,merge_smoke.hexa,MERGE_EVENT.md}` PURE wrappers · cite mitosis_lib:339-426 (best-pair cosine sim + (a+b)·0.5 centroid · 절대 winner-take-all 아님) · runtime smoke 5/5 PASS (I4 max_err=0.0 F-V5MIT-2 carry · I5 max share 0.389≪0.99 F-PERSONA-4 collapse 구조적 부재) (PR #643 4cea677b)
- [x] persona-diff per cell — `MITOSIS/{persona_diff.hexa,persona_diff_smoke.hexa,PERSONA_DIFF.md}` PURE wrappers · D3 design identity_probe 50 prompts × 5 cat (philosophy/math/creative/personal/practical) · runtime smoke 5/5 invariants PASS (`per_cell_mean_dist=0.990888` F-PERSONA-2 PER-CELL-DIFF carry 0.996 mirror · `per_cell_kl=0.00159806` random-init baseline, NOT claimed PASS — F-PERSONA-4 cheap path 4/4 FALSIFIED, architectural routing fix pending: gumbel/MoE-aux/category-head)
- [ ] WAKE sleep-tick mitosis — REM/N3 stage 에서 imagination loop 가 emit-free internal rehearsal + mitosis tick 수행. WAKE 도메인의 5-stage state machine 과 통합. inference-time 분열의 자연 거주지
- [ ] v5-cotrain ckpt 회수 + production swap-in — H100 cotrain 5/5 PASS ckpt 581MB 를 generator.hexa 의 _gen_decode seam 에 swap-in 경로 확립. F5 갭 채움, DECODER 의 ckpt 대기 해결
