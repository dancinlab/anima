# anima CLM cond.2 HF release v1 — audit landing (2026-05-04)

## TL;DR (사용자 친화 요약)

`.roadmap.clm` cond.2 ("HF release v1 — `need-singularity/anima-clm-mk2-v1`") readiness audit + action plan landed. **Overall readiness ~55% READY / 45% GAP.** Hard infra (weights, tokenizer, shim, license, upload pipeline, pre-push hook) all green or near-green. Three blockers concentrate the gap: (1) **naming spec collision** (cond.2 `anima-clm-mk2-v1` violates mk2 EBNF — recommend re-target to `clm-v4-mk2-v1`), (2) **README sync source missing** (`docs/modules/clm.md` does NOT exist; author from scratch), (3) **model card draft not written** (template ready, content not). **Estimated effort to GREEN: 2 BG cycles ~2.5h mac + 1 user decision turn, $0 — no H100 required for v1.** Audit + plan + this handoff are spec-only; no exec, no pod, no HF push, no git commit in this cycle.

## 1. 결정 (사용자 OK 대기 — 4 questions)

| Q | recommended (per completion-quality lens) |
|---|---|
| Q1 (repo name) | **`need-singularity/clm-v4-mk2-v1`** (Option A: re-target cond.2 to mk2-spec-conformant canonical name; omit `-530m` size suffix per spec §3.5 "obvious from base-version") |
| Q2 (chat disclosure wording) | use audit §3 Q2 verbatim block (5-sentence #115 invocation + Stage 2-alt cross-link) for `## Caveats` C1 |
| Q3 (distill dependency) | **release v1 NOW**, do NOT wait for Paradigm D distill (logit-axis BLOCKED on vocab mismatch per `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json`; φ★-axis is v2 follow-on) |
| Q4 (sister substrate co-author) | **CLM-only release with `## Composability` cross-link** (NOT bundled co-authoring; sisters get their own release cycles) |

## 2. 8 sub-task readiness (audit §1 summary)

| # | Sub-task | Status | Critical action |
|---|---|:---:|---|
| 1 | Weight finalization | READY-WITH-MANIFEST-GAP | Generate `manifest.json` with sha256 + reconstructed train config |
| 2 | Tokenizer | READY (SP-direct) / GAP (AutoTokenizer) | Document SP-direct load in README §Substrate |
| 3 | HF format shim (V4-1/2/3 PASS) | READY | Embed F-CLM-RELEASE-1/2/3 in README §Falsifiers |
| 4 | Model card draft | GAP | Author README.draft.md (~60 min mac) |
| 5 | README sync source `docs/modules/clm.md` | **GAP — BLOCKER** | Author from scratch (~30 min mac) |
| 6 | License (MIT) + gating (false) | READY-WITH-PACKAGING-GAP | Bundle `LICENSE` into staging dir |
| 7 | Naming convention | **GAP — DECISION-BLOCKER** | User Q1 decision; Option A `clm-v4-mk2-v1` recommended |
| 8 | Pre-push hook + leak guard | READY | Run `--dry-run` against final name (~1 min) |

## 3. 변경 사항

### 3-1. 신규 파일 (3 개)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_audit_2026_05_04.md` (~3500 words, 10 §, 8 sub-task audit + 4 decision questions + 8 honest C3)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_plan_2026_05_04.md` (10-step ordered checklist; 6 §; 5 honest C3; 10 acceptance criteria)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_landed_2026_05_04.ai.md` (this 1-page handoff)

### 3-2. 기존 파일 (변경 0)
- `.roadmap.clm` (untouched; cond.2 amendment is in plan §1 step 2, NOT this audit cycle)
- `tool/hf_upload_mk2.hexa` (untouched; pipeline is proven by 2026-05-03 `clm-v4-base-mirror` push, no changes needed)
- `tool/hf_readme_template.md` (untouched; template is ready, content drafting is in plan step 5)
- `LICENSE` (untouched; MIT, ready to bundle)
- `tool/transient_py/clm_v4_hf_format_shim.py` (untouched; F-SHIM-V4-3 PASS already landed)
- HF repo `need-singularity/clm-v4-base-mirror` (untouched; predecessor; will be cited in §Composability of cond.2 v1 README)

## 4. 결정 lock-in (이번 cycle)

- audit + plan only — no exec, no pod, no HF push, no git commit
- ranked recommendation: Option A name + audit §3 Q2 disclosure + release-now (skip distill wait) + CLM-only release
- raw#9 준수: 0 .py created (all hexa+md); raw#10 honest C3: 8 in audit + 5 in plan + this handoff (≥3) = 16+ total; raw#15: 0 destructive paths in audit/plan

## 5. 비용 / destructiveness

- spec authoring: $0 mac-local (this audit cycle)
- destructive: 0 (no rename, no delete, no commit, no marker land in this cycle)
- byte-diff to existing artifact: 0
- HF API calls: 0
- ubu1 ssh calls: 0
- estimated effort to GREEN cond.2: 2 BG cycles ~2.5h mac + 1 user turn + 24-48h review window, $0 total (no H100)

## 6. 잔존 작업 (next cycle 후보, plan §1 ordered)

| step | priority | rationale |
|---|---|---|
| User Q1-Q4 decision turn | BLOCKING | unblocks 9 downstream steps |
| `.roadmap.clm` cond.2 amendment | BLOCKING | resolves naming collision (Option A) |
| `docs/modules/clm.md` author | BLOCKING (R1) | sync source exists |
| `manifest.json` generate | NICE-TO-HAVE | release audit-trail |
| README.draft.md author | BLOCKING | model card content |
| Stage upload dir + dry-run | BLOCKING | smoke before push |
| Private upload + user review | BLOCKING | review window |
| Promote to public | BLOCKING | cond.2 visibility |
| cond.2 PASS land + marker | BLOCKING | terminal step |

## 7. honest C3 (raw#10)

- **C1** — audit operates on landed-state snapshots; live state may have drifted during BG concurrency (audit §C1)
- **C2** — naming spec amendment cost is non-zero; downstream cite paths must be grep-rewired (audit §C2)
- **C3** — README sync mechanism is aspirational discipline, NOT enforced by tooling (audit §C3)
- **C4** — F-SHIM-V4-3 PASS is bit-exact `max_abs_diff = 0.0` (suspicious but confirmed deterministic; not a v1 blocker) (audit §C4)
- **C5** — weight provenance has irreducible historical opacity (seed/git_sha/corpus_sha unknown pre-mk2; honest manifest fields) (audit §C5)
- **C6** — Q3 distill-dependency recommendation is conservative; flips if user pivots Paradigm D teacher (audit §C6)
- **C7** — license bundling is operator discipline, NOT auto-staged by `hf_upload_mk2.hexa` (audit §C7)
- **C8** — F-SHIM-V4-4 + φ★ post-load probe NOT verified; v1 ships without; flagged as BG-Σ followup (audit §C8)

## 8. 산출물 (재확인)

- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_audit_2026_05_04.md` (audit, full 3500-word, 10 §)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_plan_2026_05_04.md` (action plan, 10-step ordered)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_landed_2026_05_04.ai.md` (this handoff)

## 9. predecessors_unchanged

- `.roadmap.clm` (read-only this cycle)
- `docs/clm_v4_revival_stages_2026_05_02.md` (cited as #115 source)
- `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (cited as naming SSOT)
- `docs/anima_hf_upload_mk2_spec_2026_05_03.md` (cited as upload pipeline SSOT)
- `tool/hf_upload_mk2.hexa` + `tool/hf_readme_template.md` + `tool/hf_upload_mk2_pre_push_hook.hexa` (untouched)
- `tool/transient_py/clm_v4_hf_format_shim.py` (untouched; F-SHIM-V4-3 PASS preserved)
- `state/clm_v4_tokenizer_restoration_2026_05_03/` (untouched; tokenizer integrity preserved)
- `state/hf_upload_audit/*` + `state/hf_upload_ledger_2026_05.jsonl` (read-only)
- `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json` (read-only; cited for Q3)
- `state/markers/*` (no marker created/touched in this audit cycle)
- `LICENSE` (untouched; will be bundled in plan step 6)
- `HF need-singularity/clm-v4-base-mirror` (untouched; cited as predecessor)

## 10. 다음 사용자 입력 대기

User decision needed on Q1 (repo name) and Q3 (distill dependency wait); Q2 (caveat wording) and Q4 (co-author scope) have safe defaults that can ride if no explicit user pick. Plan step 1 captures the decision turn.
