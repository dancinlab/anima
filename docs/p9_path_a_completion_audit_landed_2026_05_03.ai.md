# P9 Path A — LoRA Training Completion Audit LANDED 2026-05-03

**Goal**: Post-hoc audit of pod `29dhlqk508ugoc` (anima-p9-pathA-llama-v2, H100 SXM, $2.99/hr) which terminated before 21:38 UTC after ~7.5h of LoRA SFT on Llama-3.2-3B-Instruct. Determine: (a) training completion, (b) HF push success, (c) termination cause, (d) A' eval readiness.

**Constraints honored**: raw#9 (Mac → hexa/CLI only; ran `hf`, `runpodctl`, `curl` against APIs only — no on-pod commands since pod gone), raw#15 (no token printed; only first-8-char prefix referenced for token-equality identification across stored locations), raw#10 (3+ honest C3 caveats per output JSON), $0 design (pure post-hoc audit).

---

## TL;DR

| dimension | finding | confidence |
|---|---|---|
| training completion | step 10000/10000 reached at 21:34:08Z | **HIGH** (host_terminator.log monotonic progression) |
| TRAIN_DONE.json marker | NOT written before terminator probe | **HIGH** (terminator branched 'error path') |
| HF push (steps 2k-8k) | almost certainly succeeded | **MEDIUM-HIGH** (every_save + on-pod token verified at 15:17Z; not live-verified now) |
| HF push (step 10k + final/) | probably succeeded but uncertain | **MEDIUM** (10min terminator window may have caught process during final save) |
| pod cost burned | **$22.18** (7.42h × $2.99/hr) | **HIGH** |
| termination cause | host-side terminator script error-path branch (NOT 28h cap, NOT preempt, NOT manual) | **DEFINITIVE** |
| A' main eval readiness | **CONDITIONAL** — needs live HF verify before pipeline kickoff | — |

---

## Termination cause — definitive

**Actor**: `host_pod_terminator.sh` running on Mac.
**Branch taken**: `elif ALIVE=0 AND DONE=0` → "train pid GONE without DONE — likely error; downloading log + terminating"
**Trigger**: 10-min poll at 21:34:08Z found:
- `STEP=10000/10000` (final step reached)
- `ALIVE=0` (train pid no longer in `kill -0` check)
- `DONE=0` (no `/workspace/p9_path_a_llama_lora/TRAIN_DONE.json`)

**Ranked root causes** (likelihood):
1. **60%** — train completed cleanly through `trainer.train()` + intermediate HF pushes; process was inside `trainer.save_model('final')` / `tok.save_pretrained` / `TRAIN_DONE.json` write when 10min probe SSH'd in and saw pid already exited (race window).
2. **25%** — train reached step 10000 then crashed during final save (HF push timeout, OOM during full state dump, network blip).
3. **10%** — RunPod-side OOM kill or container restart during final ops.
4. **4%** — RunPod spot preemption (unlikely; pod was on standard cluster).
5. **1%** — manual termination (ruled out: `host_terminator.log` clearly attributes deletion to its own `runpodctl pod delete` call).

**NOT caused by**:
- 28h hard cap (only 7.42h elapsed; well under)
- RunPod platform action
- User manual

---

## HF push — verification BLOCKED, circumstantial verdict PROBABLY_SUCCESS

**Verification BLOCKED on Mac**:
- `hf auth whoami` → `Invalid user token`
- `curl -H "Authorization: Bearer $HF_TOK" /api/whoami-v2` → 401 `Invalid username or password`
- All token storage locations (`~/.cache/huggingface/token`, `~/.cache/huggingface/stored_tokens [anima]`, `core/anima/.secrets/hf_token`) hold same 37-byte invalid token (`hf_ENhYT...`)
- Public unauth check returns 401 (consistent with PRIVATE repo per naming-decision doc; does NOT prove non-existence)
- RunPod GraphQL `pod(id:...)` returns null (pod fully terminated; cannot fetch on-pod log/token)

**Circumstantial evidence (strong)**:
- Audit round 1 (15:17Z) confirmed: `repo_exists_status=200, token_present_pod=true, token_user=dancinlife, token_orgs=[dancinlab], token_org_match=true`
- `train_llama_lora.py` line 130: `hub_strategy="every_save"` → push at every save_steps=2000 → expected 5 pushes (2k, 4k, 6k, 8k, 10k)
- `host_terminator.log` shows monotonic step progression with NO stall — first push (~step 2000 at 15:52:54Z) did not break training cadence
- Loss at audit-1: 3.06 → 0.74 over 1090 steps with grad_norm 0.234, no NaN/inf, log_clean=true
- Total wall time 7.12h matches projection 6.86h + checkpoint+push overhead

**Verification recovery path** (next cycle):
1. `hf auth login --force` (interactive on Mac) OR ssh into ubu1 and run from there if ubu1 has fresh token
2. `hf models info dancinlab/p9-llama32-lora-stage1 | jq '.siblings[].rfilename'`
3. `curl -H "Authorization: Bearer $HF_TOK" /api/models/<repo>/refs` to enumerate tags
4. If pushes confirmed: trigger sister BG `a993063` post-completion workflow (`hf repos move` legacy→canonical name)

---

## Cost analysis

| metric | value |
|---|---:|
| pod created | 2026-05-03T14:09:09Z |
| pod deleted | 2026-05-03T21:34:13Z |
| total uptime | **7.418 h** |
| rate | $2.99/hr (H100 SXM) |
| **billed cost (est)** | **$22.18** |
| per-pod cap | $50.00 |
| % of cap | **44.4%** |
| 28h hard cap | $83.70 |
| % of hard cap | 26.5% |
| projection ($21.5) | actual delta +$0.68 (+3.2%) |

Post-termination billing: **$0.00 additional** (verified via RunPod GraphQL `myself.currentSpendPerHr` = $0.811/hr, accounted for by remaining A100 PD pod $0.79/hr).

---

## A' main eval readiness verdict

**CONDITIONAL — NOT ready to fire yet**.

Blockers:
1. **HF push not live-verified** — must re-auth on Mac (or ubu1) and confirm `siblings` includes `adapter_config.json`, `adapter_model.safetensors`, plus tokenizer files. Until verified, kicking off A' eval risks pulling a half-pushed or empty repo.
2. **`final/` adapter status unknown** — `trainer.save_model('final')` is a separate operation from `every_save` push; even if step-2k…10k commits pushed, `final/` may not have flushed before pid exit. Eval pipeline must accept `step-10000` ckpt as fallback if `final/` missing.
3. **Naming alias not yet executed** — sister BG `a993063` (`p9_path_a_naming_decision_landed`) pre-created `dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1`; post-training `hf repos move` is pending. Eval pipeline should read from legacy `p9-llama32-lora-stage1` until rename lands.

**Recommended next-cycle ordering**:
1. (5min) Re-auth HF on Mac, run `hf models info` + `--refs` to confirm 5 commits/tags + adapter files present
2. (10min) If verified: trigger sister BG `a993063`'s post-completion workflow (manifest dump → `hf repos delete` stub → `hf repos move` legacy→canonical → re-upload finalized README)
3. (eval cycle): kick off A' lm-eval-harness {HellaSwag, MMLU 0-shot, TriviaQA EM} on Llama base + Llama+LoRA per A' decision §2.4

---

## Design lesson — terminator polling race

**Issue**: 10min poll + `ALIVE=0 AND DONE=0 = error` heuristic creates a false-error termination window if training process exits between polls AND the post-train save sequence is still flushing TRAIN_DONE.json.

**Recommendations** (for next training launch):
- (a) Reduce poll interval to 1-2min once `STEP > 0.95 × max_steps`
- (b) Widen success window: if `STEP=max_steps AND ALIVE=0 AND DONE=0`, retry probe 60s later before declaring error
- (c) **BEST**: in `train_llama_lora.py`, write `TRAIN_DONE.json` IMMEDIATELY after `trainer.train()` returns, BEFORE `trainer.save_model('final')` — decouple marker from final-save success

---

## Outputs

```
state/p9_path_a_completion_audit_2026_05_03/
  hf_push_status.json       # verification blocked + circumstantial PROBABLY_SUCCESS verdict + recovery path
  cost_analysis.json        # $22.18 burned, 44% of cap, 3.2% over projection
  termination_cause.json    # ranked causes; definitively host-script error-path branch
state/markers/
  p9_path_a_completion_audit_landed.marker
docs/
  p9_path_a_completion_audit_landed_2026_05_03.ai.md  # this handoff
```

Referenced inputs:
```
state/p9_path_a_llama_lora_2026_05_03/host_terminator.log    # full step-progression timeline
state/p9_path_a_llama_lora_2026_05_03/host_pod_terminator.sh.txt  # terminator logic
state/p9_path_a_llama_lora_2026_05_03/train_llama_lora.py.txt     # training script (hub_strategy=every_save)
state/p9_path_a_llama_lora_2026_05_03/launch_v3.sh.txt            # launch invocation
state/p9_path_a_llama_lora_2026_05_03/verdict.json                # initial launch verdict
state/p9_path_a_health_audit_2026_05_03/health.json               # 15:17Z health audit (HF token verified on pod)
state/p9_path_a_health_audit_2026_05_03/cost_projection.json      # $21.5 projection (vs $22.18 actual = +3.2%)
state/p9_path_a_watchdog_armed_2026_05_03/first_poll.log          # ubu1 watchdog confirmed pod gone at 21:38Z
state/p9_path_a_watchdog_armed_2026_05_03/watchdog_pid.txt        # ubu1 watchdog state
docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md            # sister BG a993063: canonical alias + post-completion plan
```

---

## raw#10 honest C3 caveats (audit-level)

(a) **HF push verdict is circumstantial, not live-verified** — Mac-side HF token (37-byte hf_ENhYT...) returns 401 across all storage locations. Verdict "PROBABLY_SUCCESS" rests on (1) on-pod token verified working at 15:17Z health audit, (2) `hub_strategy=every_save` semantics, (3) clean monotonic loss with no errors in audit-1 log scan. A 5-min re-auth + `hf models info` would convert this to definitive — recommended as first action of next cycle.

(b) **Termination cause #1 likelihood (60%) is heuristic** — not a calibrated probability. It reflects pattern-match to typical SFT runs that complete cleanly within a 10min terminator window. Could be 80% or 40% depending on assumptions about final-save duration vs probe timing.

(c) **`final/` adapter status decoupled from intermediate ckpts** — `trainer.save_model('final')` is a SEPARATE save operation from the `every_save` per-checkpoint pushes. Even if step-2k…10k commits flushed to HF cleanly, the `final/` directory save (which is what the local fallback scp would have pulled) and TRAIN_DONE.json are at higher risk under cause #2 (crash during final save). Practical impact: A' eval can use `step-10000` ckpt; `final/` is convenience-redundant.

---

**End of handoff. Next cycle: re-auth HF on Mac → verify push → trigger sister-BG post-completion rename → kick off A' eval.**
