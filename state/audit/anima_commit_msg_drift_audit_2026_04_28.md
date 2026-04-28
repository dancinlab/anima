# anima commit-msg ↔ diff alignment audit

- ts: 2026-04-28T12:09:09Z
- repo: /Users/ghost/core/anima
- audited: 100 commits
- eligible (excl exempt/no-scope/no-diff): 71
- PASS:           48
- WARN_LOOSE:     13
- FAIL_MISMATCH:  10
- NO_SCOPE:       0
- EXEMPT:         29
- NO_DIFF:        0
- mismatch_rate:  14.08% (10/71 eligible)
- warn_rate:      18.31% (13/71 eligible)

## FAIL_MISMATCH commits

- `ec2ae4b2f` `fix(an11-fire13): pip uninstall + force-reinstall — Mode D fix #3 (con`
  - scope tokens: ['an11', 'fire13']
  - top files:    anima-eeg/full_helmet_view.hexa(+741), anima-eeg/electrode_helper_rich.hexa(+713), anima-eeg/impedance_check.hexa(+708)
- `315b61249` `witness(A24): first-tick verified + dispatcher integration MEASURED — `
  - scope tokens: ['a24']
  - top files:    state/format_witness/2026-04-28_full_6repo_aggregate_post_a19_dispatcher_measured_per_file.json(+2234), docs/hxc_cumulative_milestone_2026-04-28.md(+79), state/format_witness/2026-04-28_full_6repo_aggregate_post_a19_dispatcher_measured.jsonl(+9)
- `7bbbf49c1` `docs(session-end): "루프 종료" + "all kick" 응답 — market NO_OFFERS honest d`
  - scope tokens: ['session', 'end']
  - top files:    state/an11_dispatch/fire_seed4.log(+26), state/an11_dispatch/fire_seed3.log(+26), state/an11_dispatch/fire_seed2.log(+26)
- `67e71082a` `omega-cycle(C1): A19 subsequent-tick LIVE FIRE witness — wire-v2 promo`
  - scope tokens: ['c1']
  - top files:    state/format_witness/2026-04-28_a19_subsequent_tick_live_fire.jsonl(+14)
- `ff93121b7` `fix(an11-r39-infra): seed 인자 통합 (env var 통한 LoRA stochastic 통제)`
  - scope tokens: ['an11', 'r39', 'infra']
  - top files:    anima-eeg/electrode_adjustment_helper.hexa(+560), anima-eeg/board_health_check.hexa(+524), state/format_witness/2026-04-28_a26_v2_bounded_first_tick.jsonl(+11)
- `17f524b40` `fix(an11-fire7): vllm GPU memory OOM root-cause — gc + empty_cache + -`
  - scope tokens: ['an11', 'fire7']
  - top files:    .venv-eeg/lib/python3.12/site-packages/numpy/__init__.pyi(+6202), .venv-eeg/lib/python3.12/site-packages/pip/_vendor/certifi/cacert.pem(+4494), .venv-eeg/lib/python3.12/site-packages/numpy/ma/core.pyi(+3733)
- `53c711ebc` `omega-cycle(C1+raw137 v6): A25 v2 FULL DEPLOYMENT 6-repo LIVE FIRE — 7`
  - scope tokens: ['c1', 'raw137', 'v6']
  - top files:    tool/anima_law64_rule110_generalization.hexa(+433), state/law64_rule110_gen/run_20260428T031853Z.log(+39)
- `1bd4b7e01` `feat(F1-cycle4-T8n-rule110-gen): rule-110 elementary CA generalization`
  - scope tokens: ['f1', 'cycle4', 't8n', 'rule110', 'gen']
  - top files:    docs/hxc_cumulative_milestone_2026-04-28.md(+60), state/format_witness/2026-04-28_a25_v2_full_deployment_6repo_80pct_measured.jsonl(+10)
- `153645959` `feat(own11): NEW parallel-loop-mandate — independent forward steps MUS`
  - scope tokens: ['own11']
  - top files:    .own(+30), state/audit/anima_own_strengthen_audit.jsonl(+1)
- `5797ac2c0` `strengthen(own6): RunPod → RunPod + vast.ai multi-vendor — user direct`
  - scope tokens: ['own6']
  - top files:    .own(+38), state/audit/anima_own_strengthen_audit.jsonl(+1)

## WARN_LOOSE commits

- `5d728705e` `ops(raw1): SCOPE-WIDE batch lock 491 anima/tool/*.hexa — raw#1 89.6% v`  (matched in top-3: ['raw1'])
- `f6a30470c` `witness(a25-d631a902-wire): 6-repo 23.35MB MEASURED 60.79% — DEFER 80%`  (matched in top-3: ['a25', 'd631a902', 'wire'])
- `50002d89f` `fix(an11-fire18): Mode H fix #4 — cuda_max_good>=12.8 복원 + cu118 force`  (matched in top-3: ['an11'])
- `fdf782215` `fix(an11-fire12): torch cu118 wheel — Mode D fix #2 (cuda=12.6 driver `  (matched in top-3: ['an11'])
- `c1ddd0a02` `fix(an11-cuda12.6-fallback): cuda_max_good>=12.6 임계 완화 + own 5 완성도 기준 `  (matched in top-3: ['an11'])
- `34572c088` `fix(an11-multi-axis-env-vars): R38+R39 통합 dispatch 인프라 — LORA_RANK + M`  (matched in top-3: ['an11'])
- `6d9e87fed` `fix(an11-fire10): apt install gcc — Mode F-2 (Triton runtime/build sti`  (matched in top-3: ['an11'])
- `485a7cb51` `fix(an11-fire8): vllm --enforce-eager (Mode F: GCC 누락 / torch.compile `  (matched in top-3: ['an11', 'fire8'])
- `8871288a0` `feat(F1-cycle4-T8j-coupling): Conway 40x40 train-volume sweep — AMBIGU`  (matched in top-3: ['t8j'])
- `c55fd8403` `fix(an11-fire): SSH timeout root-cause — detach pip install via nohup `  (matched in top-3: ['an11', 'fire'])
- `95b43ddb1` `feat(F1-cycle4-T8g+T8h): Conway 40x40 + 80x80 physical-limit kick — CO`  (matched in top-3: ['f1', 'cycle4', 't8h'])
- `5e711ffb6` `feat(F1-cycle4-T8f): 20x20 density sweep — SWEET SPOT SHIFTS UP with g`  (matched in top-3: ['f1', 'cycle4', 't8f'])
- `3099a1363` `feat(F1-cycle4-T8e): density-controlled Conway sweep — DENSITY HYPOTHE`  (matched in top-3: ['f1', 'cycle4', 't8e'])

## raw#10 honest C3 — real-time self-witness

**Live drift event during this very lint's landing**:

The files for this lint (`anima-eeg/tool/commit_msg_diff_alignment_lint.hexa` +
docs + audit md) were silently absorbed into commit `e5e37cc66`
("feat(eeg-t4-auditory-oddball): P300 ERP paradigm runner ...") by a
parallel agent.  Top-1 file in that commit's diff is
`anima-eeg/tool/eeg_feedback_loop.hexa` (+528 LoC) — P300 auditory work
declared in subject is NOT the dominant change.

### Lint verdict on `e5e37cc66`
Verdict: **PASS** (false-negative).
Reason: scope token `eeg` matches `anima-eeg/...` path; broad-token
substring match is too lenient when the scope's *specific* tokens
(`t4`, `auditory`, `oddball`) are absent from all top-3 paths.

### Limitation surfaced (raw#10)
The current substring heuristic over-credits broad infrastructure tokens
(`eeg`, `an11`, `f1`, `cycle4`).  v2 candidate: weight tokens by inverse
document frequency over recent commits (rare tokens count more).  Logged
for next cycle, NOT fixed in v1 (frozen criteria, raw#12).

### Witness implication
Lint detected ≥10 FAIL_MISMATCH (14.08%) and ≥13 WARN_LOOSE (18.31%)
across the recent 100 anima commits — an empirical baseline for the drift
phenomenon raw#85 strengthening targets.
