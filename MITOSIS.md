# MITOSIS — current state

@goal: anima 의 학습/성장 패러다임 — train/infer 분리 폐기 per p8, ckpt = 분기점, FT = 큰 split event. cell-pool + split + merge + persona-diff + sleep-tick 을 통합한 직교 축 M, A/G ⊥ M. v5-mitosis cotrain 5/5 PASS ckpt 581MB 를 production swap-in 경로로 회수하고, WAKE 의 imagination loop + mitosis tick 으로 inference-time 분열까지 연속
@title: 🌱 MITOSIS — 세포 분열 학습 · A/G ⊥ M 직교 축

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] mitosis_lib 회수 + stdlib 승격 — `MITOSIS/{mitosis_lib.hexa,SSOT.md}` 회수 from `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.hexa` (503L · S187-G flame port) · 12 pub fn (8 §A const-surface + 4 §B cell-pool lifecycle) · legacy 경로 보존 (비파괴) · hexa parse OK (PR #627 b64dba36)
- [ ] cell-pool split-event — tension 임계 초과 시 cell 자동 분열. v5-mitosis cond.5 의 2→64 cells step 150 saturate 메커니즘 검증된 패턴. F-V5MIT-1 SPLIT-NOGRAD 보존
- [ ] merge-event — winner-take-all collapse 회피. 다중 cell 의 weighted average 또는 selective merge. F-V5MIT-2 MERGE-WEIGHT max_err 0.0 보존, F-PERSONA-4 KL=0 회피
- [ ] persona-diff per cell — 같은 substrate 다른 cell = 다른 persona. D3 design: identity_probe 50 × 5 cat verify. F-PERSONA-2 PER-CELL-DIFF mean cos dist 0.996 PASS 검증 carry, cotrain v2 entropy-reg 또는 architectural routing fix 로 F-PERSONA-4 cotrain 진입
- [ ] WAKE sleep-tick mitosis — REM/N3 stage 에서 imagination loop 가 emit-free internal rehearsal + mitosis tick 수행. WAKE 도메인의 5-stage state machine 과 통합. inference-time 분열의 자연 거주지
- [ ] v5-cotrain ckpt 회수 + production swap-in — H100 cotrain 5/5 PASS ckpt 581MB 를 generator.hexa 의 _gen_decode seam 에 swap-in 경로 확립. F5 갭 채움, DECODER 의 ckpt 대기 해결
