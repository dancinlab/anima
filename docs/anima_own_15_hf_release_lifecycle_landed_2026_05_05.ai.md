---
title: anima HF release lifecycle PRIVATE→PUBLIC LANDED — 1-page summary (2026-05-05)
cycle: 2026-05-05
ts: 2026-05-05T00:00:00Z
status: LANDED
bg_lane: BG-OWN-UPDATE-HF
type: ai_native_landed
own_entry: anima/.own hf-release-private-then-public-after-verification
memory_entry: feedback_hf_release_private_to_public_after_verification.md
sister_own: (HF Hub mandate for models + datasets)
precedent: docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md
authorization: user directive 2026-05-04 + 2026-05-05 ("HF 관련 own 추가 — 과정은 PRIVATE, 최종은 PUBLIC, 단 벤치마킹+테스트+모든 검증과정 통과 필수")
---

# anima — HF release lifecycle PRIVATE→PUBLIC after verification (LANDED 2026-05-05)

- ** added to anima/.own** (additive, raw#15 monotonic-additive — all earlier ..14 entries preserved verbatim). Slug: `hf-release-private-then-public-after-verification`. Status: `new`. 6th anima autonomy mandate joining quintet (/ 5 / 6 / 11 / 12 / 14).
- **Memory entry written** at `~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_hf_release_private_to_public_after_verification.md` (session-scoped mirror of SSOT). MEMORY.md appended one line (additive, prior entries untouched).
- **Sister to ** — = WHERE (HF Hub only for models + datasets, never anima git, capacity reason). = HOW (PRIVATE first → 6 verification gates → PUBLIC promote via separate BG). Together: HF triad covering location + lifecycle.
- **Precedent: clm-v4-mk2-v1** (commit 80440a1d, uploaded 2026-05-04T23:26:12Z PRIVATE, 48h review window ends 2026-05-06T23:26:12Z) is the first application instance — public promote queued NOT yet executed pending gates (b.1-b.6) PASS verdict.json.
- **Honest C3 caveats (≥5 per raw#10)**:
  1. **Tool-side enforcement vs human discipline trade-off**: `--private` flag MANDATE is advisory in current `tool/hf_upload_mk2.hexa` (no validator-warn yet); follow-up `tool/hf_public_promote_lint.hexa` PROPOSED but not implemented. 24-48h review window is human convention, not tool-enforced.
  2. **"All verification" is project-specific NOT universal** — CLM v4 declared F-SHIM-V4-1/2/3/4 gates; BLM / EEG / SLM / qmirror substrates declare own equivalent compatibility gates per substrate spec at frozen-spec time (raw#12). Rule body specifies 6 canonical gates but acknowledges per-project gate suite declaration.
  3. **PRIVATE → PUBLIC revert technically possible** but external clones / HF discovery indexing creates reputational cost — prefer never-premature-promote over revert. Rule does not BAN revert, but treats it as pathological.
  4. **24-48h review window not auto-enforced** — relies on human discipline (raw#91 honest C3). No daemon polls private repos for staleness; depends on cycle owner remembering to launch promote BG after window.
  5. **Bench suite expected MAY drift over time** — e.g., add MT-Bench post-2026, deprecate hellaswag if saturated. Rule expects current-canonical-at-upload-time, NOT static historical set; future cycles may declare different canonical bench at frozen-spec time.
  6. **PRIVATE upload still consumes HF Hub bandwidth** — LFS for >10MB. No quota issues at anima scale 2026-05 (single-org under free tier limits), but rule is silent on multi-tenant scaling.

## Verification of additive land

- `wc -l anima/.own` before: 512 → after: 568 (+56 lines, all appended after block).
- `grep -c "^own " anima/.own` before: 14 → after: 15 (added).
- ..14 entries unchanged (verified by line-range read prior to edit).
- MEMORY.md before: 19 lines → after: 20 lines (+1 line for memory link).

## Cross-link

- Sister memory: `feedback_anima_models_datasets_hf_only.md` (— HF Hub mandate, capacity reason)
- Precedent doc: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md` (CLM v4 mk2-v1 first PRIVATE upload, 48h review window in progress)
- Path decision: `docs/clm_v4_release_path_decision_2026_05_04.md` (Path 1 = release v1 NOW)
- Tool: `tool/hf_upload_mk2.hexa` (enforcement layer attaches to `--private` flag)
- Audit ledger: `state/hf_upload_audit/20260504T232612Z_dancinlab__clm-v4-mk2-v1.jsonl` (visibility=private captured)

## Follow-ups

- `tool/hf_upload_mk2.hexa` validator-warn when `--upload` invoked without `--private` on never-uploaded repo
- `tool/hf_public_promote_lint.hexa` (PROPOSED) — gates (b.1-b.6) PASS evidence required before `gh repo edit --visibility public`
- 30d post review — measure PRIVATE-first compliance + PUBLIC-promote gate-cite compliance; if <0.80 escalate advisory→block
- clm-v4-mk2-v1 PUBLIC promote BG — pending verdict.json with gates (b.1-b.6) PASS evidence (review window ends 2026-05-06T23:26:12Z)
