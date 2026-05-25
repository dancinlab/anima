# P9 EXITED Pod Disposition — 2026-05-03

**Scope**: Research-only review of 6 EXITED RunPod pods (~580GB volume + 480GB cdisk → ~$58–106/mo idle storage). Goal: per-pod recommendation so user can decide preserve / partial-preserve / terminate-all after waking. **No pods touched, no podStart/podStop/podTerminate executed.**

**Substrate**: local `docs/`, `state/`, `git log`, sister-repo `anima-tribev2-pilot/`. RunPod inventory taken from earlier-this-session GraphQL snapshot. HF mirror check (per user): no `dancinlab/*` repo for any of these 6 pods; `huggingface-cli` not installed locally so no independent re-confirmation.

---

## 1. Per-pod evidence + recommendation table

| # | name | id | vol | cdisk | evidence summary | likely artifacts on volume | exported? | recovery cost | recommendation | one-line rationale |
|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | hxqwen14b-smoke-20260419 | hhzla1nxmp5019 | **0** | 100 | EXITED **already** by 2026-04-20 (`docs/clm_parallel_track_20260420.md` line 22; `docs/alm_r11_preflight_20260420.md` line 25). 14 hxqwen14b spec/research docs landed locally; pod was the day-1/day-2 smoke target on 2026-04-19 (~3h elapsed at audit). | none on volume (vol=0GB); cdisk=100GB holds container scratch (pip caches, build artifacts) — **non-persistent across pod boot anyway**. | **YES** — research outputs landed as 14 docs `docs/hxqwen14b_*_20260419.md` + `state/hxqwen14b_v5_*` markers. | **$0** — vol=0GB, cdisk is ephemeral; nothing to lose by terminate. | **TERMINATE_OK** | vol=0GB → no persistent volume billing exists; cdisk is ephemeral container scratch with no recoverable artifact. |
| 2 | clm_r5_h100 | 87xscivuggrwvk | **300** | 80 | EXITED by 2026-04-20 already (per same `clm_parallel_track` line 22 + `alm_r11_preflight` line 25). Pod was scheduled to be **restarted** for ALM r11 launch but ALM r11 BLOCKED on BLAS coverage gap (`docs/clm_r5_a6_blas_coverage_20260420.md`). Subsequent ALM r12/r13/r14 cycles produced state locally (`state/alm_r12_*` … `state/alm_r14_*` ≥27 files) → work moved off this pod. No marker, no `state/clm_r5_*` dir. | Plausibly: HF model caches (Llama / Qwen base weights), corpus shards staged for r11 (`training/corpus_auto/` 5.38GB mirror), partial r5 binary builds. **No produced trained ckpts** — r5 launch was BLOCKED before any forward step ran. | **PARTIAL** — research/blocker docs landed; weights cache is replaceable from HF; corpus mirror exists locally (`training/corpus_auto/`). | **LOW–MEDIUM** — re-pull HF weights (~30–60 min) + re-rsync corpus shards (~1h) on next pod boot. **No trained ckpt to lose.** | **TERMINATE_OK** | r5 never produced ckpts (BLOCKED on BLAS gap pre-forward); 300GB volume holds replaceable HF/corpus cache; downstream ALM cycles already moved to other infra. |
| 3 | anima-sae-steer-pilot | bnabak3i4r38bg | **100** | 100 | STOPPED on 2026-04-27 02:35 UTC (`state/runpod_incident_full_closure.json` cycle 65, `state/pod_termination_path_c_landing.json`). Cycle-56 SSH probe **confirmed GPU 0% IDLE**. Earlier sibling run `anima-sae-steer-pilot-retry` (8m5pqy0z9dl6sv, **different pod** `state/runpod_run_sae_steer_pilot_retry.json`) crashed at import (`ModuleNotFoundError: BertForPreTraining`) and self-terminated within 3 min. Local `state/sae_steer_pilot_retry_run/` directory exists but **empty** (just dir, 0 files inside). | Likely: pip cache, transformer_lens install attempts, possibly a partial HF cache. **No measurement output written** — IDLE 0% confirms no inference/training reached; sibling-retry pod's import error confirms code path didn't even load. | **YES (negative)** — failure mode + pod-state captured in `runpod_incident_full_closure.json` + `runpod_run_sae_steer_pilot_retry.json`. No positive artifact to export. | **$0** — IDLE pod, no produced data; recovery = re-debug import error (mac-local, $0). | **TERMINATE_OK** | GPU 0% IDLE confirmed, sibling-retry showed code path failed at import; volume holds only failed install scratch. |
| 4 | anima-gwt-deepseek-c2-long | 1an0fdtr2mrif1 | **100** | 100 | STOPPED on 2026-04-27 02:36 UTC (`runpod_incident_full_closure.json` cycle 66). Pod was **stuck pre-SSH** — `pod_termination_path_c_landing.json` records `uptime_seconds: 0` for **22.5h** (host scheduling failure, billed without runtime). Only mention in `docs/session_handoff_20260427.md` line 171 + `tecs_l_jamba_mixtral_throughput_evidence_20260426.md`. **No state dir**, **no marker**, **no docs** describing this pod's intended workload completion. | Likely: nothing — `uptime=0` for full 22.5h means no install, no model load, no work. Volume may contain a pristine container scratch from initial provision attempt. | **N/A** — nothing produced to export. | **$0** | **TERMINATE_OK** | Pod never reached uptime > 0; stuck-orchestrator burn was a known incident; no recoverable work product possible. |
| 5 | f1-canary-2026-04-29 | r2krrcoosdmccy | **50** | 50 | Mentioned only in `tool/h100_idle_guard.bash` line 9 as the **2026-04-30 incident pod** that "sat idle for 23h burning credits" — the very motivation for the `h100_idle_guard` wrapper. No state dir, no marker, no docs, no other source mentions the pod. Name pattern "f1-canary" suggests an F1 (functor falsifier) canary smoke. | Likely: minimal — 23h idle = pod accepted job but workload never engaged GPU (pattern matches sticky-pod / launchd `--dry-run` gap from `h100_idle_guard.bash` post-mortem). | **YES (negative)** — incident captured in `tool/h100_idle_guard.bash` header comment as the canonical case study. | **$0** | **TERMINATE_OK** | Pod is the documented 2026-04-30 idle-burn incident; no productive work; smallest volume of the six (50GB) → also lowest cost-of-mistake. |
| 6 | anima-pilot-t1-v3 | stldy2ewplkhsj | **30** | 50 | EXITED. Local `state/v11_pilot_t1_llama_3_2_3b_resume/verdict.json` is for a **different pod** (`sowpcnrlsbd0k7` recover-attempt) that never reached SSH. The actual `stldy2ewplkhsj` pod history is in `anima-tribev2-pilot/docs/pilot_t1_v2_pod_status_check_landing.md` + `pilot_t1_full_mode_verdict.md` + `state/pilot_t1_full_mode_result_v1.json` (sha256 `86f6d01d…d591` byte-identical local mirror). v1 result is `T1_DEFERRED_LLAMA_GATED_ACCESS_BLOCKED` (HF gate); v2 install never executed (SSH drop). Decision "kill pod" landed 2026-04-26. | Pod-side cache **was**: 3.6 GiB HF cache (`facebook/tribev2`, `Systran/faster-whisper-large-v3`, spacy `en_core_web_lg`), but **Llama-3.2-3B was NOT cached** (the gating blocker). All replaceable from HF on rebuild. **No trained ckpts, no inference output beyond v1 result already locally mirrored.** | **YES** — `pilot_t1_full_mode_result_v1.json` byte-identical local; v1 + v2 + v3 launcher logs all locally in `anima-tribev2-pilot/state/`. | **LOW** — re-cache 3.6 GiB HF deps on next pod (~10–15 min); Llama-3.2-3B HF gate approval status independent of this pod. | **TERMINATE_OK** | v1 result already byte-identical local; v2 never produced anything; volume contents (HF cache) are 100% replaceable from public HF repos. |

---

## 2. Tier classification

Re-derived from §1 evidence (per user's preferred Tier scheme):

| Tier | Definition | Members | Rationale |
|---|---|---|---|
| **Tier 1 — Zero-loss** | vol=0GB OR no work produced AND no recoverable cache | hxqwen14b-smoke (#1), gwt-deepseek-c2-long (#4), f1-canary (#5) | vol=0 / uptime=0 / 23h-idle-incident — provably nothing to lose |
| **Tier 2 — Likely safe** | Pod-side cache exists but 100% replaceable from public sources (HF/corpus mirror) | sae-steer-pilot (#3), pilot-t1-v3 (#6) | IDLE 0% / v1 already mirrored byte-identical; HF cache replaceable |
| **Tier 3 — Has-replaceable-large-cache** | Large volume holds non-trained-ckpt cache (HF model weights + corpus shards) | clm_r5_h100 (#2) | 300GB cache; r5 BLOCKED before training, so no ckpts to lose; cache replaceable |
| **Tier 4 — High-risk (do NOT terminate without confirm)** | Trained ckpts / unique measurement / un-mirrored data | **(none)** | All six pods either failed pre-forward, exported byte-identical results locally, or hold only replaceable caches |

Net: **all 6 pods are TERMINATE_OK** under the evidence collected. No pod falls into Tier 4.

---

## 3. Final scenario recommendation

**TERMINATE_ALL_SIX** is the evidence-supported recommendation.

Reasoning:
1. **No trained checkpoint exists on any of the 6 volumes.** clm_r5 was BLOCKED pre-forward (BLAS gap); pilot-t1-v3 v1 result is byte-identical locally; pilot-t1-v3 v2 install never ran; sae-steer was IDLE 0%; gwt-deepseek had uptime=0; f1-canary was the documented 23h-idle incident; hxqwen14b-smoke had vol=0GB.
2. **All recoverable artifacts are already exported.** 14 hxqwen14b research docs + r5/ALM cycle docs + pilot-t1 verdict + incident-closure JSONs all landed in local `docs/` + `state/`. Failure modes captured in `runpod_incident_full_closure.json`, `pod_termination_path_c_landing.json`, `runpod_run_sae_steer_pilot_retry.json`.
3. **Recovery cost on regret is bounded by HF re-pull (10–60 min/pod).** Worst case is clm_r5 (300GB) where re-caching HF weights + corpus shards = ~1.5h on a fresh pod. No cost path exceeds 2h wallclock.
4. **Idle storage burn at $58–106/mo on zero work product is a pure loss.**

If user wants a **conservative tiered fallback** despite the above:
- **Tier B (preserve only #2 + #6, terminate #1/#3/#4/#5)** — keeps the two pods with HF cache that *could* be useful for a fast resume (~150GB vol + 130GB cdisk preserved). Saves ~50–60% of monthly idle vs preserve-all.
- **Tier C (preserve only #2, terminate the other five)** — keeps just the largest cache (clm_r5 300GB). Saves ~70% of monthly idle.
- **Preserve-all** — not recommended; no evidence of irrecoverable work justifies $58–106/mo ongoing.

**Strongest single recommendation**: TERMINATE_ALL_SIX.

---

## 4. C3 caveats (raw#10 honest)

What this audit could **not** verify:

1. **No volume introspection performed.** All "likely artifacts on volume" entries in §1 are inferred from local docs + handoff trail; we did not mount, did not boot, did not `ls /workspace` on any pod. **Recovery cost is an upper-bound estimate** — actual contents could be (a) less than predicted (some cache may have been pruned by pod cleanup), or (b) very rarely more than predicted (e.g., a partial R2-pending upload that never completed). The rare (b) case would manifest as a `state/*_pending.json` or an in-flight `rclone copy` log — none found locally for the 6 pod IDs.
2. **HF mirror check not independently re-run.** `huggingface-cli` not installed in this audit environment; relied on user-stated finding ("`dancinlab` org has only 7 `clm-v4-sft-*` repos — none of the 6 EXITED pods have an HF mirror"). If user wants belt-and-suspenders, run `huggingface-cli repo list dancinlab` + `… dancinlife` after waking.
3. **anima-pilot-t1-v3 (`stldy2ewplkhsj`) terminate vs stop ambiguity.** The 2026-04-26 `pilot_t1_v2_pod_status_check_landing.md` says "Decision: kill pod" but the 2026-04-27 `session_handoff_20260427.md` line 169 still lists it as "활성 GPU pod (다른 세션 owned, 보존)". This audit treats current EXITED status (per user-supplied 2026-05-03 RunPod inventory) as authoritative — the kill decision was applied at some point between 04-26 and 05-03.
4. **clm_r5_h100 (300GB) was the largest single line item.** Confidence that "no trained ckpt exists" rests on `clm_r5_a6_blas_coverage_20260420.md` (BLOCKED pre-forward) + absence of any `state/clm_r5_*` dir + absence of any `r5_step_*` artifact name in HF mirror list. If user worries about this one specifically, **a single 5-min `runpodctl start` + `ls /workspace/anima-models/clm1b/r5/` SSH probe + immediate stop** would byte-confirm it. This audit does NOT recommend that probe (incurs ~$0.25 + restart risk) given the evidence chain is already strong.
5. **f1-canary-2026-04-29** has the thinnest local trace (single comment in `h100_idle_guard.bash`). Recommendation rests on (a) name pattern + (b) idle-incident attribution + (c) no state/docs/marker. If user has out-of-band recall of what F1-canary was meant to test, that should override this audit.

---

**Frozen at**: 2026-05-03
**Author**: Claude Opus 4.7 (1M ctx) sub-agent (P9 Phase 1 follow-up #3)
**Substrate**: research-only; zero RunPod mutations; zero pod boots; zero $ incurred.
