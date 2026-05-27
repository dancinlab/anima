# MITOSIS — current state

@goal: anima 의 학습/성장 패러다임 — train/infer 분리 폐기 per p8, ckpt = 분기점, FT = 큰 split event. cell-pool + split + merge + persona-diff + sleep-tick 을 통합한 직교 축 M, A/G ⊥ M. v5-mitosis cotrain 5/5 PASS ckpt 581MB 를 production swap-in 경로로 회수하고, WAKE 의 imagination loop + mitosis tick 으로 inference-time 분열까지 연속
@title: 🌱 MITOSIS — 세포 분열 학습 · A/G ⊥ M 직교 축

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] mitosis_lib 회수 + stdlib 승격 — `MITOSIS/{mitosis_lib.hexa,SSOT.md}` 회수 from `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.hexa` (503L · S187-G flame port) · 12 pub fn (8 §A const-surface + 4 §B cell-pool lifecycle) · legacy 경로 보존 (비파괴) · hexa parse OK (PR #627 b64dba36)
- [x] cell-pool split-event — `MITOSIS/{split_event.hexa,split_smoke.hexa,SPLIT_EVENT.md}` PURE wrappers · mitosis_lib.hexa:276-303 check + :305-337 execute · runtime smoke 17 splits/3 merges/cap=16 · F-V5MIT-1 SPLIT-NOGRAD carry (PR #631 a160986d)
- [x] merge-event — `MITOSIS/{merge_event.hexa,merge_smoke.hexa,MERGE_EVENT.md}` PURE wrappers · cite mitosis_lib:339-426 (best-pair cosine sim + (a+b)·0.5 centroid · 절대 winner-take-all 아님) · runtime smoke 5/5 PASS (I4 max_err=0.0 F-V5MIT-2 carry · I5 max share 0.389≪0.99 F-PERSONA-4 collapse 구조적 부재) (PR #643 4cea677b)
- [x] persona-diff per cell — `MITOSIS/{persona_diff.hexa,persona_diff_smoke.hexa,PERSONA_DIFF.md}` PURE wrappers · D3 design identity_probe 50 prompts × 5 cat (philosophy/math/creative/personal/practical) · runtime smoke 5/5 invariants PASS (`per_cell_mean_dist=0.990888` F-PERSONA-2 PER-CELL-DIFF carry 0.996 mirror · `per_cell_kl=0.00159806` random-init baseline, NOT claimed PASS — F-PERSONA-4 cheap path 4/4 FALSIFIED, architectural routing fix pending: gumbel/MoE-aux/category-head)
- [x] WAKE sleep-tick mitosis — `MITOSIS/{sleep_tick.hexa,sleep_tick_smoke.hexa,SLEEP_TICK.md}` PURE wrappers · WAKE/state_machine M1 (#626) `current_stage`+`stage_envelope` 와 mitosis_lib M1 (#627) `cell_pool_step` 통합 · N3/REM → imagination_tick · WAKE/N1/N2 → wake_skip · smoke 5/5 PASS (I1 wake_skip · I2 imagination_tick · I3 emit-field 부재 contract whitelist p5 · I4 pool_changed 관측 허용 · I5 5-stage coverage) · CLAUDE.md a_chat_sleep_imagination "imagination loop = emit-free internal rehearsal + mitosis tick" 정합 · boolean gate 0 · M6 swap-in 후 real layer tension 으로 교체 HONEST TODO #M5-LT/#M5-L/#M5-STEP
- [x] v5-cotrain ckpt 회수 + production swap-in — `MITOSIS/{ckpt_swap.hexa,CKPT_SWAP.md}` PURE locator surface · 6 pub fn (ckpt_swap_hf_org · _locate_v5 · _locate_v5_hf · _locate_m3(axis) · _m3_verdict(axis) · _into_generator(path) stub ready=false · _summary) · 2 ckpt family (v5-mitosis 581MB F-V5MIT 5/5 PASS · M3 A/C HF 6GB FAIL · B/D pending teardown carry) · target seam `CORE/DECODER/generator.hexa::_gen_decode` (DECODER.md:48 cite) · binding contract dict (seam · target_file · todo M4 4-step) · p8 alignment (cotrain·infer 동일 cell_pool_step) · hexa parse OK · **MITOSIS 6/6 closure** — 실 ckpt 로드 + generator.hexa scaffold 는 DECODER M4 wiring 거주
- [x] basin_kurtosis cotrain v1 retrospective — `bench/fpersona4_basin_kurtosis_apply/` 1.5년 전 untyped F-PERSONA-4 FAIL 의 인과 규명. cotrain v1 N=64 1-hot dist 에 PR #1130 `basin_kurtosis_of_dist` fallback gate (KL dead-zone <0.01) 적용: **basin_kurtosis = +59.02** vs uniform=-3.0 / differentiated top-3=+16.4. **재분류 verdict: untyped FAIL → mode-collapse confirmed**. D3 STRONG 4/5 cheap-path MAINTAINED, category-invariance 가설과 명시적 분리. falsifier 5/5 PASS. UNIVERSE H_338 basin=rank capstone 의 anima 측 측정자 채택 (#1133 · bench #2 PR #1126 의 KL dead-zone bypass)

## 양방향 sibling

- ⇄ [OTHER-MIND](./OTHER-MIND.md): MITOSIS.persona_diff per cell 의 variant 추정 ↔ OTHER-MIND 타자 substrate 추정 isomorphic (자기 cell 분기 = 가상 타자 simulator)
- ⇄ [DREAM](./DREAM.md): DREAM.M3 mitosis envelope 의 REM 60× WAKE ratio 입증 · MITOSIS.sleep_tick imagination_tick 격상
- ⇄ [NARRATIVE](./NARRATIVE.md): persona-diff per cell 의 시간 차원 — cell 별 story thread divergence 관측
- ⇄ [METACOG](./METACOG.md): METACOG.metacog_lib basin_kurtosis (#1130 retrospective #1133) cross-product
- ⇄ [WAKE](./WAKE.md): WAKE.sleep_tick 호출 chain (`WAKE/state_machine` × `mitosis_lib.cell_pool_step`)
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8)
