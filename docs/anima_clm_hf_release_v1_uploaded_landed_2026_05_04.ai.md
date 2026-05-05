# anima CLM HF release v1 — PRIVATE upload landed (2026-05-04)

- **Cycle**: BG-HF-CYCLE-2-UPLOAD
- **Date**: 2026-05-04
- **Verdict**: `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json`
- **Audit JSONL**: `state/hf_upload_audit/20260504T232612Z_need-singularity__clm-v4-mk2-v1.jsonl`
- **Mac stage mirror**: `state/clm_v4_hf_release_v1_upload_stage_2026_05_04/` (README + LICENSE + manifest copy only — weights stayed on ubu1 per own 14)
- **Mode**: PRIVATE upload + audit-only landing, NO git commit, NO public promote
- **Cost**: $0 (HF Hub free tier; mac wall ~30 min including 5GB LFS push from ubu1)

---

## §1 Outcome

- **Repo created PRIVATE**: `need-singularity/clm-v4-mk2-v1` at https://huggingface.co/need-singularity/clm-v4-mk2-v1
- **Visibility**: `private=true, gated=false, license=mit`
- **Commit sha**: `80440a1d38db9addc4445bb959057558a57f4230`
- **Files in repo**: 15 (`.gitattributes` auto-added by HF + 14 staged: README, LICENSE, manifest.json, best.pt, model.safetensors, config.json, modeling_clm_v4.py, configuration_clm_v4.py, decoder_v3.py, conscious_decoder.py, generation_config.json, __init__.py, integrity_report.json, tokenizer_64k_multilingual.model, tokenizer_64k_multilingual.vocab)
- **Upload size**: 6.98 GB (best.pt 5.37GB + model.safetensors 2.12GB + 12 small files)
- **sha256 verification**: 12/12 manifest weight_files match (best.pt 22f180ef..., model.safetensors 40b3a99f..., tokenizer .model bb851d39..., etc. — full map in audit JSONL)

---

## §2 L1-L5 PASS evidence (verdict §3)

| Lens | Status | Method |
|---|---|---|
| L1 validator | PASS | mac `HEXA_LOCAL=1 hexa run tool/hf_upload_mk2.hexa --validate-naming need-singularity/clm-v4-mk2-v1` → `__ANIMA_HF_UPLOAD_MK2__ PASS` (with §3.7 grace warning); `--validate-readme docs/anima_clm_hf_release_v1_README_draft.md` → `__ANIMA_HF_UPLOAD_MK2__ PASS` |
| L2 leak guard | PASS | manual egrep against 9 token-shape regex patterns from `~/.hive/scripts/leak_guard_pretool.bash` over 11 text files in mac+ubu1 stage; 0 leaks detected |
| L3 dry-run | PASS | sha256 audit pre-computed and matched all 12 manifest weight_files entries before upload (12/12 match) |
| L4 actual upload | PASS | `ubu1 hf 1.13.0 hf upload need-singularity/clm-v4-mk2-v1 ~/anima_clm_release_v1_staging` exit=0; commit_url emitted |
| L5 post-upload verify | PASS | `curl /api/models/need-singularity/clm-v4-mk2-v1` returns `private=true, gated=false, siblings_count=15` matching stage |

---

## §3 Review window + promote-to-public recipe

- **24h_review_window_starts_utc**: `2026-05-04T23:26:12Z`
- **24h_review_window_ends_utc**: `2026-05-05T23:26:12Z`
- **48h_review_window_ends_utc**: `2026-05-06T23:26:12Z`
- **Enforcement**: convention only — NOT enforced by upload tooling.

**User actions during review window**:
1. Login HF Hub as `dancinlife`, visit https://huggingface.co/need-singularity/clm-v4-mk2-v1
2. Verify README renders correctly (5 H2 sections, 9-bullet Caveats including #115 chat disclosure)
3. Verify LICENSE = MIT, manifest.json embeds 12 sha256 entries
4. Run F-CLM-RELEASE-1 (`AutoModelForCausalLM.from_pretrained("need-singularity/clm-v4-mk2-v1", trust_remote_code=True)` on fresh shell)
5. Run F-CLM-RELEASE-2 (1-batch forward returns finite logits shape `[1, T, 64000]`)
6. Decision turn — `OK promote public` OR redo loop (loop back to README edit + re-push)

**Promote-to-public recipe** (when user authorizes):

```bash
# Preferred (NOT YET IMPLEMENTED at tool/hf_upload_mk2.hexa v2.1.0):
hexa run tool/hf_upload_mk2.hexa --promote-public --repo need-singularity/clm-v4-mk2-v1

# Fallback A (HF Hub UI): Settings → Change visibility → Public

# Fallback B (curl):
TOKEN=$(secret get huggingface.token --raw)
curl -sX PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  https://huggingface.co/api/models/need-singularity/clm-v4-mk2-v1/settings \
  -d '{"private": false}'
```

---

## §4 Honest C3 (≥5 per raw#10; full list in verdict.json)

1. **PRIVATE only at v1** — public promotion is a separate sibling cycle. Do NOT promote-public from this BG.
2. **Pre-push leak-guard tooling deviation** — `tool/hf_upload_mk2_pre_push_hook.hexa` is a git pre-push commit-msg validator, NOT a `--stage-dir` file scanner. Substituted manual egrep over 9 token-shape regex patterns from `~/.hive/scripts/leak_guard_pretool.bash`. Future BG should extend the hook with a `--stage-dir` mode or rename the spec step.
3. **Wrapper hexa run vs raw hf CLI deviation** — ubu1 hexa_real binary differs from mac in `args()` shape; `hexa run tool/hf_upload_mk2.hexa --upload` fails on ubu1 with 'unknown command: tool/hf_upload_mk2.hexa'. L1 naming + readme validators ran successfully on mac; upload step bypassed the wrapper and called `hf upload` directly (raw#9 carve-out for upload bash explicitly authorized in the BG spec). Future fix: patch `tool/hf_upload_mk2.hexa` `main()` to detect both argv shapes.
4. **24-48h review window is convention only** — not enforced by upload tooling. Repo CAN be flipped to public any time; user owns decision-turn timing.
5. **HF Hub may rate-limit LFS push for 5GB best.pt** — observed peak upload rate 3.35 GB/s 'Processing Files' + 7.81 MB/s 'New Data Upload'. No 429 hit; `hf` CLI handles backoff internally per upload-spec §6.1.
6. **trust_remote_code=True consumer requirement** — F-CLM-RELEASE-1 fresh-shell load test was NOT run by this BG; user must run during review window.
7. **Manifest pretrain seed/git_sha/corpus_sha256 = unknown_pretrain_predates_manifest_discipline** propagated into uploaded `manifest.json`. Future v5 / v4-1700m / v4-100m must record these from training-time onward.
8. **F-SHIM-V4-3 bit-exact (max_abs_diff=0.0)** flagged 'suspiciously tight' but confirmed deterministic. **F-SHIM-V4-4 train_avg lift validation DEFERRED** to BG-Σ H100 followup.
9. **Staging-dir leftover** — `/home/aiden/anima_clm_release_v1_staging` on ubu1 (~7GB) NOT cleaned up; left in place for review window. Cleanup BG should run post review-window close (verb=DELETE_SCRIPT, verify pre+post per `feedback_cleanup_bg_guards.md`).

---

## §5 Cross-links

- **Audit doc**: `docs/anima_clm_hf_release_v1_audit_2026_05_04.md`
- **Plan doc**: `docs/anima_clm_hf_release_v1_plan_2026_05_04.md`
- **Sync source**: `docs/modules/clm.md` (anima-internal SSOT)
- **HF README draft**: `docs/anima_clm_hf_release_v1_README_draft.md` (uploaded as `README.md` in repo)
- **Manifest**: `state/clm_v4_hf_release_v1_manifest_2026_05_04/manifest.json` (12 sha256 + train config; uploaded as `manifest.json` in repo)
- **Roadmap**: `.roadmap.clm` cond.2 (canonical name = `need-singularity/clm-v4-mk2-v1`; status still `unmet` — flips to `met` only after public promote per plan §1 step 10)
- **Predecessor repo**: `need-singularity/clm-v4-base-mirror` (already PUBLIC with tokenizer + integrity_report; 2026-05-03 commit 10ee03687db312c55bbec5858c814bef28e4d365)

---

## §6 Next ranked actions

1. **rank-1**: USER REVIEW the private repo (login as dancinlife, run F-CLM-RELEASE-1+2, decision turn by 2026-05-06)
2. **rank-2**: User-authorized promote-to-public via curl PUT /api/models/.../settings (honest C1: hexa wrapper `--promote-public` not yet implemented)
3. **rank-3**: cond.2 PASS landing — `.roadmap.clm` cond.2 status `met` + marker + landed handoff (post promote)
4. **rank-4**: Cleanup BG for ubu1 staging dir + mac stage dir (verb=DELETE_SCRIPT, verify pre+post)
5. **rank-5**: Future patch — add `--stage-dir` mode to leak-guard hook + fix mk2 wrapper argv-shape divergence
