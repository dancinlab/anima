# anima commit-msg ↔ diff alignment audit (v2: vendor-filter + body-fallback)

- ts: 2026-04-28T14:03:06Z
- repo: /Users/ghost/core/anima
- lint_version: v2 (vendor_filter + body_token_fallback)
- audited: 100 commits
- eligible (excl exempt/no-scope/no-diff): 77
- PASS:           56
- PASS_BODY:      7  (v2 body-token rescue)
- WARN_LOOSE:     10
- WARN_BODY:      0  (v2 body-token weak match)
- FAIL_MISMATCH:  4
- NO_SCOPE:       0
- EXEMPT:         23
- NO_DIFF:        0
- mismatch_rate:  5.19% (4/77 eligible)
- warn_rate:      12.99% (10/77 eligible)

## v1 vs v2 delta

- v1 (pre-filter)  FAIL_MISMATCH: 11/77 (14.29%)
- v2 (post-filter) FAIL_MISMATCH: 4/77 (5.19%)
- delta: 9.09pp reduction
- vendor_prefixes: .venv-eeg/, .venv/, .venv-, .hxc_aot/, node_modules/, references/, .git/, dist/, vendor/, __pycache__/

## FAIL_MISMATCH commits (v2 — true positives surviving filter)

- `ec2ae4b2f` `fix(an11-fire13): pip uninstall + force-reinstall — Mode D fix #3 (con`
  - scope tokens: ['an11', 'fire13']
  - body tokens:  ['uninstall', 'force', 'reinstall']
  - top files:    anima-eeg/full_helmet_view.hexa(+741), anima-eeg/electrode_helper_rich.hexa(+713), anima-eeg/impedance_check.hexa(+708)
- `7bbbf49c1` `docs(session-end): "루프 종료" + "all kick" 응답 — market NO_OFFERS honest d`
  - scope tokens: ['session', 'end']
  - body tokens:  ['"all', 'kick"', 'market', 'offers', 'honest']
  - top files:    state/an11_dispatch/fire_seed4.log(+26), state/an11_dispatch/fire_seed3.log(+26), state/an11_dispatch/fire_seed2.log(+26)
- `ff93121b7` `fix(an11-r39-infra): seed 인자 통합 (env var 통한 LoRA stochastic 통제)`
  - scope tokens: ['an11', 'r39', 'infra']
  - body tokens:  ['lora', 'stochastic']
  - top files:    anima-eeg/electrode_adjustment_helper.hexa(+560), anima-eeg/board_health_check.hexa(+524), state/format_witness/2026-04-28_a26_v2_bounded_first_tick.jsonl(+11)
- `17f524b40` `fix(an11-fire7): vllm GPU memory OOM root-cause — gc + empty_cache + -`
  - scope tokens: ['an11', 'fire7']
  - body tokens:  ['vllm', 'memory', 'root', 'cause', 'empty', 'cache']
  - top files:    anima-cpgd-research/state/cpgd_mcb_real_4bb_v1.json(+2568), anima-cpgd-research/state/cpgd_mcb_4bb_hidden_state_v2.json(+2057), state/hxc/alm_r13_4gate_pass_subset.jsonl.hxc(+1827)
  - vendor_filter: APPLIED (top_raw differed)

## PASS_BODY commits (v2 §4.5 — scope rescued by body match)

- `dbf7af009` `feat(B11): behavioral_correlates_logger — 5 metrics × 5-min sliding wi`  (body→top1: ['behavioral', 'correlates', 'logger'])
- `8e64c5145` `feat(B10): eeg_anomaly_autoencoder — pure-numpy AE state-shift detecto`  (body→top1: ['anomaly', 'autoencoder'])
- `43cc4dcdf` `feat(C19): webcam eye-tracker + EEG cross-modal — gaze/blink/fixation/`  (body→top1: ['webcam', 'tracker'])
- `ac0b1a862` `feat(C18): wearable_health_integrator — Apple Watch / Oura / Whoop × E`  (body→top1: ['wearable', 'health', 'integrator'])
- `3d765697e` `feat(C22): cross-substrate Φ proxy correlator — anima-physics 9 substr`  (body→top1: ['cross', 'substrate', 'correlator', 'anima', 'physics', 'substr'])
- `315b61249` `witness(A24): first-tick verified + dispatcher integration MEASURED — `  (body→top1: ['dispatcher', 'measured'])
- `67e71082a` `omega-cycle(C1): A19 subsequent-tick LIVE FIRE witness — wire-v2 promo`  (body→top1: ['subsequent', 'tick', 'fire'])

## WARN_LOOSE commits

- `e35baa899` `feat(eeg-core): _core/eeg_export — .npy → fif/edf/bdf/csv export — sel`  (matched in top-3: ['eeg', 'core'])
- `a4e33160f` `witness(a29-v2): distance Huffman first-tick — 10/10 selftest + AOT by`  (matched in top-3: ['a29'])
- `5d728705e` `ops(raw1): SCOPE-WIDE batch lock 491 anima/tool/*.hexa — raw#1 89.6% v`  (matched in top-3: ['raw1'])
- `f6a30470c` `witness(a25-d631a902-wire): 6-repo 23.35MB MEASURED 60.79% — DEFER 80%`  (matched in top-3: ['a25', 'd631a902', 'wire'])
- `50002d89f` `fix(an11-fire18): Mode H fix #4 — cuda_max_good>=12.8 복원 + cu118 force`  (matched in top-3: ['an11'])
- `fdf782215` `fix(an11-fire12): torch cu118 wheel — Mode D fix #2 (cuda=12.6 driver `  (matched in top-3: ['an11'])
- `c1ddd0a02` `fix(an11-cuda12.6-fallback): cuda_max_good>=12.6 임계 완화 + own 5 완성도 기준 `  (matched in top-3: ['an11'])
- `34572c088` `fix(an11-multi-axis-env-vars): R38+R39 통합 dispatch 인프라 — LORA_RANK + M`  (matched in top-3: ['an11'])
- `6d9e87fed` `fix(an11-fire10): apt install gcc — Mode F-2 (Triton runtime/build sti`  (matched in top-3: ['an11'])
- `485a7cb51` `fix(an11-fire8): vllm --enforce-eager (Mode F: GCC 누락 / torch.compile `  (matched in top-3: ['an11', 'fire8'])

## WARN_BODY commits (v2)

