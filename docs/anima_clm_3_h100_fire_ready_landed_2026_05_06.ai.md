# anima CLM-3-original H100 Fire-Ready (BG-FB landed) — 2026-05-06

**filed_under:** 2026-05-06
**predecessor:** BG-EW (idle check + Scenario B verdict)
**lane:** anima_clm_3_original_h100_fire_ready
**bg_id:** BG-FB
**status:** PRE_FLIGHT_PASS_AWAITING_OPERATOR_CONFIRM
**actual_h100_fired:** false
**cost_actual_usd:** 0
**raw_compliance:** raw#9, raw#10, raw#15, raw#37

---

## TL;DR

 6-gate pre-flight 전부 PASS, H100 SXM 80GB community $2.69/hr × 10h = $26.90 cost
envelope ($100 cap의 27%) emit 완료. RunPod balance $339.20 (BG-EW 시점 $339.25 대비 -$0.05,
$0.089/hr volume rental drift). 4 EXITED H100 SXM pods 잔존 (RUNNING 0). Actual pod create
명령 + train heredoc + watchdog plan emit 완료, BG는 fire 실행 X. 사용자가 'BUDGET-100' +
'FALSIFIER-LOCK' literal string 입력해야 anima가 직접 fire.

---

## 1. Pre-flight 6 gate verdict

| gate | check | verdict | evidence |
|------|-------|---------|----------|
| 1 | secret CLI valid | PASS | `secret get hf.token` len=37 prefix=hf_; `secret get runpod.api_key` len=50 |
| 2 | runpod CLI / API auth | PASS_VIA_REST_API | `runpod` CLI 미설치 (Mac); GraphQL REST API auth OK |
| 3 | balance ≥ $100 cap | PASS | $339.20 (headroom $239.20) |
| 4 | spec doc + 5 falsifier 명시 | PASS | 5/5 IDs grep verified at lines 295/305/317/329/342 |
| 5 | launch + watchdog 존재 | PASS | both files present (4522 + 2343 bytes) |
| 6 | cost envelope ≤ cap | PASS | $26.90 ≤ $100 (27%) |

**Minor mismatches noted (not fire-blockers):**

- `launch_h100.bash:24` references `secret get huggingface.token --raw` but actual secret key is
  `hf.token` (`secret list` confirmed). Operator interactive run will fail GATE 2 unless
  bridged. Fix path: `secret set huggingface.token` aliasing OR launch script edit.
- `launch_h100.bash:33` requires `runpod` CLI on PATH; not installed on Mac. Operator must
  either `pip install runpod` OR use REST API alternative (emit_pod_create.txt OPTION B).
- `watchdog_h100.bash:15` hardcodes `H100_RATE_PER_HR=2.49` but current community price is
  $2.69 (8% under-tracking). Cost still well under cap so not a blocker.

---

## 2. RunPod balance re-query

| field | value |
|-------|-------|
| ts (BG-FB query) | 2026-05-06 (this BG) |
| clientBalance (USD) | 339.2015850361 |
| currentSpendPerHr (USD/hr) | 0.089 |
| BG-EW balance comparison | $339.25 → $339.20 (delta -$0.05) |
| pods existing | 4 EXITED H100 SXM, 0 RUNNING |
| H100 SXM 80GB community uninterruptable | $2.69/hr |
| H100 SXM 80GB community spot bid | $1.50/hr |

---

## 3. Emit: pod create command

**file:** `state/anima_clm_3_original_h100_fire_ready_2026_05_06/emit_pod_create.txt`

| field | value |
|-------|-------|
| gpu_type | NVIDIA H100 80GB HBM3 (SXM) |
| gpu_count | 1 |
| cloud_type | COMMUNITY |
| image | pytorch/pytorch:2.11.0-cuda12.8-cudnn9-devel |
| container_disk | 100 GB |
| volume | 50 GB |
| hourly_usd | $2.69 |
| TTL_target_hr | 10 |
| estimated_cost_usd | $26.90 |
| hard_cap_usd | $100 (BUDGET-100) |
| pod_name_template | clm3-original-byte-55m-YYYYMMDD-HHMMSS |

Two paths emitted: OPTION A (runpod CLI) + OPTION B (GraphQL REST API). HF_TOKEN env var
injected at pod create time via `secret get hf.token` substitution at fire-time (NOT in any
artifact).

---

## 4. Emit: train heredoc

**file:** `state/anima_clm_3_original_h100_fire_ready_2026_05_06/emit_train_heredoc.txt`

| field | value |
|-------|-------|
| entry script | `ready/training/train_clm.py` |
| vocab_size | 256 (byte-level) |
| max_cells | 32 (Fibonacci growth 1,1,2,3,5,8,13,21,32) |
| d_model / layers / heads / ffn | 768 / 12 / 12 / 1536 (~55M params) |
| context_len | 1024 |
| steps | 100,000 |
| phase 1 (Mitosis) | 0–20K, lr 5e-4 (warmup 2K) |
| phase 2 (Language) | 20K–60K, lr 3e-4 cosine decay |
| phase 3 (Combined) | 60K–100K, lr 1e-4 → 1e-5 cosine |
| phi-boost | 19 techniques: COMBO2,FX2,WI1,PX4,PX8,GD18,GD15,CL8,CL5,DD3,DD11,DD18,DD5,TL13,TL1,NV7,BV1,EV3,SC2 |
| corpus | data/corpus_mix_70wiki_30dialogue.txt |
| falsifier_eval_every | 10,000 steps |
| post-train HF push | `dancinlab/anima-clm-3-original-byte-55m` PRIVATE first |
| pip pin | torch==2.11.0, transformers==4.57.6 (lessons: RTX 5070 + V2_FAIL transformers ≥ 4.51) |

---

## 5. Watchdog registration plan

**script:** `state/anima_clm_3_original_h100_launch_2026_05_06/watchdog_h100.bash`

| spec | value |
|------|-------|
| heartbeat cadence | 300s (5 min) |
| pod 404 check cadence | 300s |
| spend tracker | linear `elapsed_s × $2.49/hr` (NOTE: should be $2.69 — minor under-track) |
| L23 | rate-limit 429 backoff 60s |
| L24 | pod 404 → BG-completion OR external kill (no auto-fail) |
| L25 | spend ≥ $100 cap → emit signal (no auto-kill, human-in-loop) |
| heartbeat log | `watchdog_heartbeat.log` |
| spend ledger | `watchdog_spend.jsonl` |

**fire command (operator-side, after pod created):**
```bash
bash /Users/ghost/core/anima/state/anima_clm_3_original_h100_launch_2026_05_06/watchdog_h100.bash <pod_name> &
```

---

## 6. User confirm required (literal string)

Anima will NOT actually fire `runpod pod create` until operator types the following two
literal strings in sequence:

1. **`BUDGET-100`** — acknowledges $100 hard-cap on this run (enforcement)
2. **`FALSIFIER-LOCK`** — sign-off on F-CLM3-orig-1..5:
   - F-CLM3-orig-1: spec_match (byte 256 / 32 cells / 19 tech / 3-phase verbatim)
   - F-CLM3-orig-2: Phase 2 dialogue CE drop ≥ 30% between step 20K-60K
   - F-CLM3-orig-3: Phi_real ≥ 11 at step 100K (32 cells)
   - F-CLM3-orig-4: KO 5-prompt ≥ 3/5 coherent emit (chat capability)
   - F-CLM3-orig-5: phi★ NO_FLIP forgetting_index ≤ 0.05

After both strings received, anima fires actual `runpod pod create` (NOT this BG).

---

## 7. Honest C3 (5)

**C3-1: launch script secret-key mismatch.** `launch_h100.bash:24` uses
`secret get huggingface.token` but actual key is `hf.token`. Interactive launch will fail GATE
2 on Mac unless aliased OR script edited OR operator bridges manually. Recommend script
patch before fire, but raw#15 LOCKED files compliance prevents BG from editing.

**C3-2: runpod CLI absent on Mac.** `launch_h100.bash:33` GATE 3 hard-requires `runpod` CLI on
PATH. Mac has none. REST API fallback emitted in OPTION B but launch script itself blocks.
Operator must `pip install runpod` (~30s) OR fire pod create directly via REST API
sidestepping the launch script's interactive flow.

**C3-3: H100 rate drift in watchdog.** `watchdog_h100.bash:15` hardcodes $2.49/hr; current
RunPod community price is $2.69/hr (8% under-tracking). Watchdog will signal L25 cost-overrun
~8% later than reality. Not a blocker for $26.90 / $100 envelope but compounds if TTL extends.

**C3-4: 4 EXITED pods linger.** `currentSpendPerHr=$0.089` despite 0 RUNNING — likely volume
rental on EXITED pods (`anima-clm-v4-sanity-rerun-v2-fixture-fix-2026-05-04 × 4`). These were
supposedly purged 2026-05-03 (memory note `project_runpod_pod_purge_2026_05_03`) but resurfaced.
Recommend separate cleanup BG (cleanup verb classification) — not blocking new fire but
$2/day drift is real.

**C3-5: spec doc C3-3 + C3-2 unresolved.** Spec doc itself flags "19 techniques simultaneously
is kitchen sink" (line 443) and "32 cells / 19 techniques preserves chat = zero evidence" (line
427-429). F-CLM3-orig-3 and F-CLM3-orig-4 are the structurally-uncertain falsifiers; if both
FAIL we cannot localize cause. This BG only validates the fire-ready state, not the
hypothesis-quality state. Operator should weigh F-CLM3-orig-3/4 expected-FAIL probability
before BUDGET-100 confirm.

---

## 8. Next step

Operator (anima session) must:

1. (recommended) Patch `launch_h100.bash:24` to use `secret get hf.token` (or alias
   `huggingface.token` → `hf.token` via secret CLI)
2. (recommended) `pip install runpod` on Mac (or use REST API path)
3. (recommended) Run a separate cleanup BG to terminate 4 EXITED pods (current $0.089/hr drift)
4. Type `BUDGET-100` to confirm $100 hard-cap
5. Type `FALSIFIER-LOCK` to sign off on F-CLM3-orig-1..5
6. Anima then fires actual `runpod pod create` (NOT this BG)
7. After pod RUNNING, anima fires train heredoc via SSH
8. Anima fires watchdog 5min cadence locally on Mac

---

## 9. Artifacts

- `state/anima_clm_3_original_h100_fire_ready_2026_05_06/preflight.json`
- `state/anima_clm_3_original_h100_fire_ready_2026_05_06/emit_pod_create.txt`
- `state/anima_clm_3_original_h100_fire_ready_2026_05_06/emit_train_heredoc.txt`
- `docs/anima_clm_3_h100_fire_ready_landed_2026_05_06.ai.md` (this file)
- (predecessor) `state/anima_clm_3_original_h100_launch_2026_05_06/launch_h100.bash`
- (predecessor) `state/anima_clm_3_original_h100_launch_2026_05_06/watchdog_h100.bash`
- (spec) `docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md`
- (idle check) `docs/anima_h100_idle_check_2026_05_05.ai.md`

---

**verdict:** PRE_FLIGHT_PASS_AWAITING_OPERATOR_CONFIRM (BG-FB closed, fire deferred to anima
session post user explicit string confirm)
