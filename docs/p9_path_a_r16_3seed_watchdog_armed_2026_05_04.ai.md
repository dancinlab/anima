# P9 Path A r=16 3-Seed Completion Watchdog Armed (2026-05-04)

## Provenance
- Spec: `docs/p9_path_a_regression_mitigation_spec_2026_05_03.md` Track B (caveat #4: 3-seed amend for landing band)
- Predecessors:
  - `docs/p9_path_a_r16_launched_2026_05_04.ai.md` (s42 single-seed launch)
  - `state/p9_path_a_r16_3seed_2026_05_04/PLAN.md` (3-seed strategy + cost envelope)
  - `state/p9_path_a_r16_multiseed_verify_2026_05_04/verify.json` (s43/s44 RUNNING confirmed at 04:55Z)
- Tool: `tool/p9_path_a_r16_3seed_completion_watchdog.hexa` (666 LoC; selftest PASS)

## Status (2026-05-04T05:22Z)
- 3 retrain pods active (RUNNING):
  - `pvkyhb0lb87ydu` (s42) — preexisting, ~step 80+ at 04:39Z, ETA ~step-10000 at 09:51Z
  - `0jetjpvlm51zoy` (s43) — step 777/10000 at 05:16Z (~30 min in)
  - `nzw0btc8br78yy` (s44) — step 825/10000 at 05:16Z (~30 min in)
- 2 unrelated pods active: `fuewrx9moxe6gz` (D 25K), `8zbf9bfj6c63wg` (base val)
- Burn: $14.95/hr (5 pods × $2.99/hr)
- 3-seed watchdog PID `27807` running via `nohup hexa run --loop --apply`
- First poll: `s42=MISSING s43=MISSING s44=MISSING ready=0/3` (no step-* tags yet — first save at step-2000 in ~1h for s43/s44)
- Old single-seed watchdog PID `49397` still alive (safe; idempotent — only 3-seed watchdog dispatches the 45-eval pipeline)

## ETA to Verdict
| Milestone | ETA from now | Cumulative |
|---|---|---|
| s43/s44 step-2000 | +1.0h | 2026-05-04T06:22Z |
| s43/s44 step-10000 + HF push final | +5.5h | 2026-05-04T10:52Z |
| Slowest seed READY (3/3) | +6.5h | 2026-05-04T11:52Z |
| Eval dispatch fires (45 evals on ubu1 RTX 5070) | +6.5h to +10h | 2026-05-04T15:52Z (high estimate) |
| 3-seed ensemble + mitigation verdict landed | +10h to +12h | 2026-05-04T17:22Z |

## Eval Pod Cost
- **Default (current config)**: ubu1 RTX 5070 — **$0** + ~3-5h for 45 evals serial
- **Opt-in H100 SXM secure**: `ANIMA_EVAL_PROVISION_POD=1` — **~$15 hard cap** + ~1.5h
  - Stage0 caveat: auto-provision NOT implemented — operator must `runpodctl create pod` manually + bash wrapper falls back to ubu1 if env set without operator action
- HARD CAP $20 honored (ubu1 path = $0; pod path = $15 < $20)

## Watchdog Behavior on TRIGGER FIRE
1. **Step 0 — sha integrity check**: verify `tool/p9_a_prime_verdict.hexa` sha256 == `db1b4552...e566eda` (locked from `state/p9_a_prime_verdict_patch_2026_05_04/audit.json`). If drift → ABORT exit=2.
2. **Step 1 — 45 evals on ubu1**: 3 seeds × 5 ckpts (step-2000..step-10000) × 3 tasks (hellaswag, mmlu, triviaqa) @ limit=500. Reuses `eval_llama_lora_ckpt.py` from `p9_a_prime_main_eval_pipeline_2026_05_03/`.
3. **Step 2 — scp results back**: 3 per-seed dirs (`lora_results_s42/`, `lora_results_s43/`, `lora_results_s44/`).
4. **Step 3 — per-seed verdict.json**: loop `tool/p9_a_prime_verdict.hexa` over each seed dir → `verdict_s42.json`, `verdict_s43.json`, `verdict_s44.json`.
5. **Step 4 — ensemble + mitigation**: emits `ensemble.json` (mean ± std + cv per (step, task)) and `mitigation_comparison.json` (vs r=64 baseline F-PATHA-MITIGATION-1) + top-level `verdict.json`.
6. **Step 5 — marker land**: writes `state/markers/p9_path_a_r16_3seed_eval_landed.marker`.

## F-PATHA-MITIGATION-1 Verdict Logic (3-seed amend)
- **MITIGATION_PASS**: `mean_Δ_TriviaQA ≥ 0` AND `ci_lo (normal-approx) ≥ -0.5pt` AND `cv < 0.30 (real lift)` AND (`mean_Δ_HellaSwag ≥ 0` OR `mean_Δ_MMLU ≥ 0`)
- **MITIGATION_PARTIAL**: `mean_Δ_TriviaQA ≥ -1pt` (weaker)
- **MITIGATION_FAIL_NO_LIFT**: primary+cv pass but no secondary lift (Track B insufficient)
- **MITIGATION_FAIL_REGRESSION**: TriviaQA mean delta < -1pt
- **MITIGATION_NO_DATA**: no triviaqa rows in ensemble

## 4 Caveats (raw#10)
- **(a) 3-seed timing window**: s43/s44 launched ~2h45min after s42; dispatch waits for SLOWEST seed (max-of-three completion). If s42 finishes hours earlier, its pod auto-terminated by host_terminator_v2.txt — no idle burn.
- **(b) Eval pod cost**: ubu1 RTX 5070 default = $0 + slower (~3-5h for 45 evals). H100 SXM opt-in = $15 + 1.5h. Auto-provision not in stage0 — operator manual. HARD CAP $20 honored either path.
- **(c) 45 evals 4-bit may differ from production**: anchor methodology = 4-bit nf4 base + LoRA overlay (matches A' decision spec). Production inference may use bf16 → expected 1-3pt drift. Verdict = "4-bit anchor consistency" not "production performance forecast".
- **(d) doc_hash join patch**: ALREADY landed in `tool/p9_a_prime_verdict.hexa` sha256 `db1b4552...e566eda`. Watchdog Step 0 enforces this lock; if drift detected → ABORT exit=2 before eval spend.

## Outputs
- `state/p9_path_a_r16_3seed_2026_05_04/verdict.json` — top-level pass/fail
- `state/p9_path_a_r16_3seed_2026_05_04/ensemble.json` — mean ± std + cv per (step, task)
- `state/p9_path_a_r16_3seed_2026_05_04/mitigation_comparison.json` — vs r=64 baseline + F-PATHA-MITIGATION-1
- `state/p9_path_a_r16_3seed_2026_05_04/eval_dispatch_3seed.json` — dispatch metadata
- `state/p9_path_a_r16_3seed_2026_05_04/watchdog_3seed_log.jsonl` — append-only poll log
- `state/markers/p9_path_a_r16_3seed_completion_watchdog_armed.marker` (this cycle)
- `state/markers/p9_path_a_r16_3seed_eval_landed.marker` (post-trigger)

## Constraints Honored
- raw#9: hexa-only on Mac; ssh/scp/runpodctl/curl shelled out; eval execution remote on ubu1 .py
- raw#15: no token leak (HF repos public-readable refs API; no private credentials in tool)
- raw#10: 4 caveats above
- HARD CAP $20 (eval pod budget): ubu1=$0 default; H100=$15 opt-in
- DO NOT preempt: 3 retrain pods + 2 unrelated pods left RUNNING

## Recovery Modes
- TIMEOUT (16h max-wait, no 3/3 ready): logs `timeout` event, exits 0; manual relaunch needed
- sha drift detected: exits 2 before eval spend; operator re-locks `tool/p9_a_prime_verdict.hexa`
- ubu1 ssh fail: logs `scp_in_fail` or `step1_rc=-1`; safe — no eval cost incurred
- Single seed missing (e.g., s42 HF push fails): 3/3 trigger never fires; 16h timeout
