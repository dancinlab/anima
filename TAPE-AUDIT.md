# TAPE-AUDIT — anima

The canonical Class-T tape baseline (`.tape` HXC spec cites anima's r29 measurement). Multi-thousand-file convergence ledger / honesty triad / witness state. This repo is the single largest audit-surface in the cognition family.

## A. Audit-class ledgers (cargo / migration candidates)

- **`state/markers/` — 38,245 `*.marker` files** + ~2,123 entries under `state/` total. Hexa hook artifacts (`clm_v4_mount_*`, `hxc_a*`, `runpod_credit_check_*`, `verify_hc_*`). Pure cargo; per wilson's audit-scrub finding these are exactly the class to delete or migrate to `state/markers.tape` (append-only `@H` host events, grade ok/err).
- **`state/*.jsonl` — 860 jsonl total** under tree; the audit-class subset: `cert_incremental_log.jsonl`, `h100_alert_ledger_2026_05.jsonl`, `hf_upload_ledger_2026_05.jsonl`, `log_rotation_zstd_log.jsonl`, `vlm_invocation_seam_log.jsonl`, `vlm_latency_profile_log.jsonl`, `dist_native_build_periodic_log.jsonl`. Strong fit for `<DOMAIN>.tape` per ledger.
- **`.raw-audit-shadow/`, `.raw-exemptions/`, `.raw-ref`, `.hook-commands/`, `.hook-advice.md`** — shadow + policy. Could fold into `governance.tape`.
- **`state/*_audit*/` dirs** — `jaw_clench_emg_audit`, `cyborg_eeg_audit`, `mk_xii_eeg_audit`, `rsn_audit`, `eeg_artifact_audit`, `eeg_claude_cli_audit`, `eeg_feedback_audit`, `eye_blink_detect_audit`, `external_session_audit_2026_05_04`, `p300_visual_audit`, `hf_workflow_audit_2026_05_04`, `p9_path_a_corpus_audit_2026_05_04`, `braket_qa6_qrng_audit_2026_05_02`, `atp_transpile_audit_2026_05_03`, `anima_alm_teacher_pending_audit_2026_05_05`, `clm_v4_hf_format_shim_v5_opt_c_2026_05_05` — each a per-experiment audit ledger; one tape file per audit run.

## B. Identity surface

Strong. `PERSONA.md`, `REBORN.md`, `SAVANT.md`, `MEMORY.md`, `PHILOSOPHY.md` carry the agent's selfhood narrative; `IMPORTED_FROM_CANON.md` carries provenance. Together they form a natural `anima/identity.tape` (`@I` identity events + `@D` decision points, immutable history of self-redefinition).

## C. Domain.md files

`UPPERCASE.md` convention present: 20 top-level mds (`AGENTS.md`, `CHAT.md`, `DOWNLOADS.md`, `HEXA_NATIVE_INFERENCE.md`, `LATTICE_POLICY.md`, `LIMIT_BREAKTHROUGH.md`, `NEXT.md`, `PASS_STRICT_SPONTANEOUS_CHAT.md`, `URGENT_ACTION_LIST.md`, plus the identity set). No cross-product `A+B.md` meta-domains. Each domain.md gets a sibling `<DOMAIN>.tape` (`@T` topic events + `@K` knowledge atoms + `@R` references).

## D. Per-run / per-event history surfaces

`state/format_witness/*.jsonl` (per-day witness logs, e.g. `2026-04-28_a16_base94_wire_encoding_decision.jsonl`). `convergence/*.convergence` (per-session convergence reports). `state/markers/*.marker` (per-tool-call hook events). `state/<experiment>_*_2026_*/` (sim outputs, axis runs). `training/corpus_*.jsonl` (per-iteration corpus shard logs). All are append-only event streams → direct `.tape` fit.

## E. Promotion candidates

- **hxc wire** — `.hxc_aot/`, `.hxc_bench_a29_v3/` already binary; promote in-place.
- **n12 cube cells** — convergence metrics (φ, tension, curiosity time-series) → n12 cells; format_witness latency profiles → n12.

**Verdict: HEAVY** (5+ tape surfaces — markers, raw-audit, witness, convergence, identity, domain).
