---
cycle: p9_paradigm_d_distill_amendment_2026_05_04
ts_utc: 2026-05-04T07:35:00Z
status: AMENDMENT_LANDED
bg_lane: T-1-AMEND
parent_cycle: BG-T-1 (state/p9_paradigm_d_distill_mini_2026_05_04/)
parent_verdict: FAIL_PRELAUNCH_VOCAB_MISMATCH
cost_usd: 0.00
budget_preserved_usd: 15.00
spec_amended: docs/p9_paradigm_d_distill_spec_2026_05_03.md (added §4.5 AMENDMENT)
roadmap_amended: .roadmap.p9_sft (entry p9_sft.cond.paradigm_d_distill → status=blocked_vocab_mismatch, additive_only=true)
recommended_path: P-β Φ★-axis-only pivot
sister_axis_status: UNAFFECTED (state/p9_paradigm_d_distill_2026_05_03/ PARTIAL_PASS preserved)
raw_compliance: ["raw#9 md only", "raw#10 honest C3 ≥5", "raw#15 additive-only roadmap mutation"]
---

# P9 Paradigm D logit-axis distill spec — AMENDMENT LANDED 2026-05-04

## TL;DR

BG-T-1 (Paradigm D logit-axis mini distill exec) was launched 2026-05-04 and FAILED at L9-style pre-flight with verdict `FAIL_PRELAUNCH_VOCAB_MISMATCH` ($0 cost, full $15 budget preserved). Root cause: spec §4.5 claim "CLM v4 inherits Mistral tokenizer" falsified empirically — CLM v4 350M uses a separate 64K multilingual SentencePiece tokenizer (`tokenizer_64k_multilingual.model`), while Mistral-7B-Instruct-v0.3 uses a 32K SentencePiece BPE. Pre-built KL cache (14.2 GB on ubu1) is structurally incompatible with CLM v4's 64K logit axis.

This cycle (T-1-AMEND, $0): amended the spec with §4.5 AMENDMENT section, marked roadmap entry `p9_sft.cond.paradigm_d_distill` as `blocked_vocab_mismatch`, and recommended **P-β Φ★-axis-only pivot** as the path forward. Sister Φ★-axis Paradigm D lineage at `state/p9_paradigm_d_distill_2026_05_03/` (PARTIAL_PASS) is **UNAFFECTED** (Φ★ scalar teacher signal is vocab-axis-agnostic).

## §1 Five-bullet summary

- **(a) What was falsified**: Original spec §4.5 stated "CLM v4 350M uses Mistral-7B-v0.3 tokenizer per `state/p9_sft_spec_2026_05_02/architecture.json` (architecture descends from Mistral)". This was an unverified ancestral inference. Direct re-read shows `architecture.json` lists `tokenizer: data/tokenizer_64k_multilingual.model` and `vocab_size: 64000`, while Mistral-7B-Instruct-v0.3 uses a 32768-vocab SentencePiece BPE. A 3-prompt direct probe (en/ko/en) confirmed 100% non-identical id sequences with different token counts — vocab axes are disjoint.

- **(b) At what cost**: **$0.00**. The vocab-mismatch blocker was caught at L9-style pre-flight (vocab probe + 3-prompt tokenizer comparison) before any H100 boot. Full $15 mini-run budget preserved. This is the best-possible outcome for a falsified spec premise — had BG-T-1 skipped the pre-flight probe, an H100 boot would have burned $5–10 producing predictable garbage logit-KL values from incompatible vocab axes.

- **(c) Recommended path**: **P-β Φ★-axis-only pivot** (완성도 9/10, $0 spec amend). Permanently shelve logit-axis variant; consolidate Paradigm D research arm into the sister Φ★ scalar channel. Existing PARTIAL_PASS at `state/p9_paradigm_d_distill_2026_05_03/` step_1000 already validates the Φ★-axis pipeline; production scale via BG-γ'' shim path (CLM v4 HF format, F-SHIM-V4-3 PASS) is unblocked. Alternatives: (P-α) re-tokenize CLM v4 with Mistral vocab — ~$10-12 + Φ★ re-anchor cost, destroys CLM v4 substrate uniqueness, NOT recommended; (P-γ) permanent shelve NO_OP — acceptable but closes the entire Paradigm D arm unnecessarily.

- **(d) What's preserved**: The sister Φ★-axis Paradigm D lineage is **fully intact**. Specifically: `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (parent Φ★ spec), `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (Mistral-7B teacher build for Φ★ side), `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` (z-score MSE runbook), and `state/p9_paradigm_d_distill_2026_05_03/` (PARTIAL_PASS at step_1000, Φ★-axis 2K steps post-loop verdict). These use a scalar Φ★ teacher signal (1 fp32/record) and are **vocab-axis-agnostic** — the falsification finding here does not propagate. CLM v4 64K multilingual tokenizer and Φ★ baseline (+41.86) anchor remain canonical.

- **(e) Honest C3 (≥5 caveats)**:
  1. **Falsification was foreseeable in-spec** — original §10 caveat #4 explicitly flagged the vocab assumption as "unverified locally". The L9 pre-flight discipline saved $5–10 of predictable burn; this is a process win, not a process failure.
  2. **The 14.2 GB Mistral KL cache is not lost work** — it remains valid for any future Mistral-tokenizer-native student (e.g., hypothetical Mistral-7B → Mistral-1B distill). Lives on ubu1 `/tmp` subject to cleanup; persist if long-term value desired.
  3. **(P-β) Φ★-axis pivot inherits all sister-doc caveats** — static-EMA Φ★ approximation (sister runbook §4), F2 sentinel-floor non-falsifying nature, no phenomenal substrate claim. Pivot replaces a vocab-blocked channel with a vocab-agnostic one; does NOT magically resolve broader Paradigm D distillation gap (350M student vs 7B teacher, 5% compression below DistilBERT regime).
  4. **(P-α) re-tokenize cost ($10-12) is a soft lower bound** — assumes 5K-step head retrain succeeds on first attempt. Re-tokenization with a different SP model can introduce byte-fallback / unknown-token edge cases requiring multiple retrain passes; true cost could reach $20–30 plus Φ★ re-anchor cost. (P-α) is the most expensive path AND least preserves substrate uniqueness.
  5. **Vocab-mismatch is a tokenizer-class issue, not architecture-class** — BG-γ'' F-SHIM-V4-3 PASS (CLM v4 loads as HF AutoModelForCausalLM) does NOT resolve this; shim handles model architecture, not vocab axis. Future P9 specs proposing Mistral-teacher → CLM-v4-student logit-distill MUST verify tokenizer identity at spec-time, not exec-time.
  6. **Roadmap mutation is additive_only** — `status_prior: unmet` preserved alongside `status: blocked_vocab_mismatch`; original entry shape (id, kind, title, desc, verifier, evidence list, cross_link) extended via additional fields (`amendment_*`, `status_prior`, `semantics_preserved`, `additive_only_mutation`), no in-place destructive overwrite of original semantics. raw#15 SSOT discipline maintained.
  7. **Φ★-axis production scale still unproven** — recommended (P-β) pivot relies on Φ★-axis pipeline scaling from PARTIAL_PASS step_1000 to production 50K × 1 epoch. That scaling has not yet been demonstrated; if Φ★-axis production fails for an unrelated reason (e.g., scalar gradient signal too weak at scale), Paradigm D arm collapses entirely. Reasonable contingency: if Φ★-axis production fails, then revisit (P-α) with explicit acceptance of the Φ★ re-anchor cost as a planned spec rewrite.

## §2 Files modified this cycle

| Path | Mutation | Lines added (approx) |
|------|----------|----------------------|
| `docs/p9_paradigm_d_distill_spec_2026_05_03.md` | Appended §4.5 AMENDMENT 2026-05-04 (subsections A4.5.1 – A4.5.7) before final terminator line | +110 LoC |
| `.roadmap.p9_sft` | Entry `p9_sft.cond.paradigm_d_distill` extended additively with `status: blocked_vocab_mismatch`, `status_prior: unmet`, `blocker_reason`, `amendment_*` fields, expanded `evidence` list, expanded `cross_link.*` fields. Original semantics preserved (`semantics_preserved: true`, `additive_only_mutation: true`). | +1 entry-line extension |
| `docs/p9_paradigm_d_distill_amendment_landed_2026_05_04.ai.md` | NEW (this file) | ~120 LoC |

## §3 Files NOT touched (explicit invariants)

- `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md` — prior PARTIAL_PASS Φ★-axis lineage doc, different path, UNAFFECTED.
- `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` — sister Φ★-axis parent spec, UNAFFECTED.
- `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` — sister Φ★-axis T4 build plan, UNAFFECTED.
- `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` — sister Φ★-axis runbook, UNAFFECTED.
- `docs/p9_paradigm_d_spec_landed_2026_05_03.ai.md` — original spec-landed handoff, UNAFFECTED (historical record).
- `state/p9_paradigm_d_distill_2026_05_03/` — Φ★-axis PARTIAL_PASS verdict + adapters, UNAFFECTED.
- `state/p9_paradigm_d_distill_mini_2026_05_04/` — BG-T-1 verdict + preflight log, READ-ONLY (this cycle reads only).
- No `.py` created (raw#9 md-only).
- No git commit (per session memory `feedback_parallel_bg_git_race`; commit deferred to user/me after review).
- No HF push.
- No pod boot.

## §4 Cross-links

- Spec amendment: `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §4.5 AMENDMENT 2026-05-04
- Falsification verdict: `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json`
- Pre-flight log: `state/p9_paradigm_d_distill_mini_2026_05_04/preflight.log`
- Roadmap entry: `.roadmap.p9_sft` entry `p9_sft.cond.paradigm_d_distill`
- Sister Φ★-axis (UNAFFECTED, recommended path): `state/p9_paradigm_d_distill_2026_05_03/` PARTIAL_PASS
- Original spec-landed: `docs/p9_paradigm_d_spec_landed_2026_05_03.ai.md` (historical, pre-amendment)
- Φ★-axis PARTIAL_PASS handoff: `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md`

## §5 Decision summary table

| Question | Decision (this amendment) |
|----------|---------------------------|
| Is logit-axis Paradigm D viable as originally specified? | **NO** — vocab mismatch falsifies §4.5 premise empirically |
| Cost incurred this cycle | **$0** (caught at pre-flight; $15 budget preserved) |
| Recommended forward path | **P-β** Φ★-axis-only pivot (preserves substrate uniqueness, $0 spec amend, sister axis already PARTIAL_PASS) |
| Status of `p9_sft.cond.paradigm_d_distill` | `blocked_vocab_mismatch` (additive mutation; `status_prior: unmet` preserved) |
| Status of sister Φ★-axis Paradigm D | UNAFFECTED — `state/p9_paradigm_d_distill_2026_05_03/` PARTIAL_PASS remains canonical Paradigm D production path |
| User decision required? | YES — accept (P-β) as default OR explicitly authorize (P-α) substrate redesign with separate spec |

## §6 raw compliance

- **raw#9** (md only): NO `.py` created; doc-only amendment + roadmap JSONL line edit + new .ai.md handoff.
- **raw#10** (honest C3 ≥5): 7 caveats listed §1(e); spec amendment §A4.5.6 lists 6 caveats.
- **raw#15** (additive-only roadmap mutation, no destructive paths): `status_prior` preserved; original entry semantics retained; new fields are additive (`amendment_*`, `semantics_preserved`, `additive_only_mutation`).

---

*End of amendment landed handoff. NO commit by this cycle (per session memory `feedback_parallel_bg_git_race`). User/parent agent commits after review.*

---

## §AUTHORIZATION 2026-05-04

**P-β USER_AUTHORIZED + DEFAULT (forward path locked)**

- User authorization message (cycle ce681c40): verbatim "Path P-β (Φ★-axis-only pivot) 권장 (완성도 9/10) — vocab-axis-agnostic, CLM v4 64K substrate uniqueness 보존"
- Forward path: Φ★-axis-only Paradigm D distill, inheriting PARTIAL_PASS step_1000
- Scale-up exec: separate sibling BG (BG-Pβ-SCALE) on H100, ~$5-15 budget cap
- Lane status: T-1-AMEND **CLOSED** (10/10 paper closure with user authorization)
- Sibling Φ★-axis lineage at `state/p9_paradigm_d_distill_2026_05_03/` unaffected
