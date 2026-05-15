# P9 P-β Paradigm D 50K HF upload landed (2026-05-05)

- **Cycle**: BG-PBETA-HF-UPLOAD
- **Date**: 2026-05-05
- **Verdict**: `state/p9_pbeta_hf_upload_2026_05_05/verdict.json`
- **Mac stage**: `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05/` (5 files / 76 MiB)
- **Ubu1 stage**: `/home/aiden/anima_pbeta_50k_step50000/` (rsync mirror of mac stage)
- **Mode**: PRIVATE upload + audit-only landing, NO git commit, NO public promote
- **Cost**: $0 (HF Hub free tier; mac+ubu1 wall ~12 min including 76 MiB rsync)

---

## §1 Outcome

- **Repo created PRIVATE**: `dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1` at https://huggingface.co/dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1
- **Visibility**: `private=true, gated=false, license=mit`
- **Commit sha**: `7643e764488f8e11020a7663c50f2e590b70d10f`
- **Files in repo**: 6 (`.gitattributes` auto-added by HF + 5 staged: README.md, LICENSE, manifest.json, adapter_model.safetensors, adapter_config.json)
- **Upload size**: 76,081,669 bytes (~72.6 MiB; adapter 76,065,712 + 4 small files)
- **sha256 verification**: adapter_model.safetensors `6e49989ab5c72d8e81da789dfe8d4cdb429b98723485c5cd7b75ae253fe29e47` — matches T-2 + T-3 verdict input_artifacts entries exactly.

---

## §2 L1-L5 PASS evidence (verdict §lens_results)

| Lens | Status | Method |
|---|---|---|
| L1 validator | PASS | mac `HEXA_LOCAL=1 hexa run tool/hf_upload_mk2.hexa --validate-naming dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1` → `__ANIMA_HF_UPLOAD_MK2__ PASS` (with §3.7 grace warning); `--validate-readme stage/README.md` → `__ANIMA_HF_UPLOAD_MK2__ PASS` (5 H2 + Caveats >=3, actual 7 bullets) |
| L2 leak guard | PASS | manual egrep against 9 token-shape regex patterns (`hf_*`, `sk-*`, `ghp_*`, `gho_*`, `github_pat_*`, `AKIA*`, `xoxb-*`, `AIza*`, `Bearer *`) over 4 text files in stage; 0 leaks detected |
| L3 dry-run | PASS | sha256 audit pre-computed; 5 files / 76,081,669 bytes; audit at `state/hf_upload_audit/20260505T034329Z_dancinlab__clm-v4-paradigm-d-pbeta-50k-mk2-v1.jsonl` |
| L4 actual upload | PASS | `ubu1 hf 1.13.0 hf upload dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1 /home/aiden/anima_pbeta_50k_step50000/` exit=0; commit `7643e764` |
| L5 post-upload verify | PASS | `curl /api/models/dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1` (via ubu1 cached token) returns `private=true, gated=false, siblings_count=6` matching stage layout |

---

## §3 Review window + promote-to-public recipe

- **Uploaded UTC**: `2026-05-05T03:48:00Z`
- **24h review window ends UTC**: `2026-05-06T03:48:00Z`
- **48h review window ends UTC**: `2026-05-07T03:48:00Z`
- **Enforcement**: convention only — NOT enforced by upload tooling.

**User actions during review window**:
1. Login HF Hub as `dancinlife`, visit https://huggingface.co/dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1
2. Verify README renders correctly (hero substrate-research-only warning + 5 H2 sections + 7-bullet Caveats with §C1 chat FAIL_TRUE disclosure visible)
3. Verify LICENSE = MIT, manifest.json embeds adapter sha256 + Pβ falsifier statuses
4. Run F-load-1: `PeftModel.from_pretrained(base, 'dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1')` on fresh shell (requires HF auth with access to both this PRIVATE repo and the PRIVATE base `dancinlab/clm-v4-mk2-v1`)
5. Confirm chat FAIL_TRUE C1 disclosure intent before any public-promote decision
6. Decision turn — `OK promote public` OR redo loop

**Promote-to-public recipe** (when user authorizes):

```bash
# Preferred (NOT YET IMPLEMENTED at tool/hf_upload_mk2.hexa v2.1.0):
hexa run tool/hf_upload_mk2.hexa --promote-public --repo dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1

# Fallback A (HF Hub UI): Settings → Change visibility → Public

# Fallback B (curl, requires working token; mac secret store currently returns
# stale hf_asc...; use ubu1 ~/.cache/huggingface/token or freshly-rotated token):
TOKEN=$(secret get huggingface.token --raw)  # OR ssh ubu1 'cat ~/.cache/huggingface/token'
curl -sX PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  https://huggingface.co/api/models/dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1/settings \
  -d '{"private": false}'
```

**Promote pre-gate** — public-promote only AFTER:
- README §Caveats §C1 chat FAIL_TRUE disclosure verified visible to non-authenticated readers
- F-load-1 PeftModel round-trip success on fresh shell
- Base model `dancinlab/clm-v4-mk2-v1` public-promote status reviewed (adapter loadability inherits base availability)

---

## §4 Honest C3 (8 caveats per raw#10; full list in verdict.json)

1. **C1** — PRIVATE only at v1; public promotion is a separate sibling cycle. Do NOT promote-public from this BG.
2. **C2** — Pre-push leak-guard tooling deviation: `tool/hf_upload_mk2_pre_push_hook.hexa` is a git pre-push commit-msg validator, NOT a `--stage-dir` scanner. Substituted manual egrep over 9 token-shape regex from `~/.hive/scripts/leak_guard_pretool.bash`. (Carry from CLM v4 release C2.)
3. **C3** — Wrapper hexa run vs raw hf CLI deviation: ubu1 hexa_real differs in `args()` shape; uploaded via raw `hf upload` bash on ubu1, not hexa wrapper. L1 naming + readme validators ran on mac. (Carry from CLM v4 release C3.)
4. **C4** — 24-48h review window is convention only, not enforced by upload tooling. (Carry from CLM v4 release C4.)
5. **C5** — F-load-1 (PeftModel fresh-shell load test) NOT run by this BG; user must run during review window. Loading requires HF auth that has access to BOTH this PRIVATE repo AND the PRIVATE base `dancinlab/clm-v4-mk2-v1`.
6. **C6** — Stage dir `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05/` on mac + `/home/aiden/anima_pbeta_50k_step50000/` on ubu1 left in place during review window; cleanup BG (verb=DELETE_SCRIPT, verify pre+post per `feedback_cleanup_bg_guards.md`) runs post review-window close.
7. **C7** — Mac secret store `huggingface.token` returned `hf_asc...` which **fails** `whoami-v2` against HF API; ubu1 cache `~/.cache/huggingface/token` (`hf_dw...`) works. Upload + L5 verify both proceeded via ubu1 cached token; no blocker for this cycle but mac-side secret store may need re-sync post-rotation per `feedback_secret_cli_credential_ssot`.
8. **C8** — Single-seed eval carry: F-Pβ-2 + F-Pβ-3 both single-seed; the README C3 caveat documents this. Multi-seed scaleup deferred per T-3 reconception.

---

## §5 Cross-links

- **Verdict**: `state/p9_pbeta_hf_upload_2026_05_05/verdict.json`
- **Stage README**: `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05/README.md` (uploaded as `README.md` in repo)
- **Manifest**: `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05/manifest.json` (uploaded as `manifest.json` in repo)
- **Sister release**: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md` (CLM v4 base, PRIVATE)
- **Source training verdict**: `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json`
- **F-Pβ-2 verdict**: `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json`
- **F-Pβ-3 verdict**: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`
- **Wrapper**: `tool/hf_upload_mk2.hexa` v2.1.0
- **Naming spec**: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`
- ** + **: `.own` (HF Hub-only mandate + PRIVATE-first lifecycle)

---

## §6 Next ranked actions

1. **rank-1**: USER REVIEW the private repo (login as dancinlife, verify README + chat FAIL C1 disclosure visible) by 2026-05-07
2. **rank-2**: IF user authorizes, public-promote via curl PUT (gated on C1 chat FAIL visible to non-auth readers + base model promotion status)
3. **rank-3**: cleanup BG for mac stage dir + ubu1 staging dir (verb=DELETE_SCRIPT, verify pre+post)
4. **rank-4**: Mac secret store `huggingface.token` re-sync (current returns `hf_asc...` which fails whoami; ubu1 cache `hf_dw...` works)
5. **rank-5 (deferred)**: Future patch — add `--stage-dir` mode to leak-guard hook + fix mk2 wrapper argv-shape divergence on ubu1 hexa_real
