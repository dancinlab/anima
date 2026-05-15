# anima CLM HF release v1 — action plan (2026-05-04)

- **Date**: 2026-05-04
- **Source audit**: `docs/anima_clm_hf_release_v1_audit_2026_05_04.md`
- **Mode**: spec/plan only — no exec, no pod, no HF push, no git commit in this cycle
- **Total estimated effort**: 2 BG cycles + 1 user decision turn = ~2.5h elapsed mac wall, **$0** (no H100 required for v1)
- **Risk surface**: 0 destructive actions; 0 byte-diff to existing artifacts; 1 user decision required to unblock

---

## §1 Critical path (ordered)

The plan is sequenced so each step unlocks the next. **Steps 1, 2, 3 are blocking; steps 4-9 are sequential build-up; step 10 is the actual push.**

### Step 1 — User decision turn (BLOCKING) — ~5 min user

**Resolve all 4 decision questions from audit §3.**

| Q | Default recommendation (per completion-quality lens) | User picks |
|---|---|---|
| Q1 (repo name) | **Option A: `dancinlab/clm-v4-mk2-v1`** (re-target cond.2 to mk2-spec-conformant canonical name; omit `-530m` size suffix per §3.5) | _____ |
| Q2 (chat caveat wording) | **Use audit §3 Q2 verbatim block** (5-sentence disclosure invoking #115 + Stage 2-alt cross-link) | _____ |
| Q3 (distill dependency) | **Release v1 NOW, do NOT wait for Paradigm D distill** (logit-axis blocked by vocab mismatch; φ★-axis is v2 follow-on) | _____ |
| Q4 (sister substrate co-authoring) | **CLM-only release with `## Composability` cross-link section** (no co-author) | _____ |

**Output**: user-confirmed answers logged to `state/anima_clm_hf_release_v1_2026_05_04/decision_turn.json`.

---

### Step 2 — `.roadmap.clm` cond.2 amendment — ~10 min mac, $0

**Trigger**: Q1 answer = Option A (rename) OR Option C (split umbrella+canonical).
**Skip**: only if Q1 answer = Option B (amend mk2 spec instead).

**Actions**:
- (a) Edit `.roadmap.clm` cond.2 `desc` field:
  - From: `"HF release v1 — public weight + model card published as dancinlab/anima-clm-mk2-v1 ..."`
  - To: `"HF release v1 — public weight + model card published as dancinlab/clm-v4-mk2-v1 ..."` (Option A) OR `"... published as dancinlab/anima-clm-mk2-v1 (umbrella) + dancinlab/clm-v4-mk2-v1 (weights) ..."` (Option C)
- (b) Update cond.2 `cross_link.hf_release_planned` field accordingly.
- (c) Grep for `anima-clm-mk2-v1` literal across `docs/` + `state/` to find downstream cite paths; rewire as needed.
- (d) Verify naming spec compliance: `hexa run tool/hf_upload_mk2.hexa --validate-naming dancinlab/clm-v4-mk2-v1` → expect `__ANIMA_HF_UPLOAD_MK2__ PASS`.

**Output**: amended `.roadmap.clm`; grep ledger at `state/anima_clm_hf_release_v1_2026_05_04/cite_path_audit.json`.

**C3 note**: this is a single-line cond.2 desc edit; do NOT touch cond.1 or other entries.

---

### Step 3 — Author `docs/modules/clm.md` (sync source) — ~30 min mac, $0

**Trigger**: cond.2 declares `hf_readme_sync_source: anima/docs/modules/clm.md` but the file does NOT exist (audit §1.5 GAP-BLOCKER R1).

**Actions**:
- (a) Author from scratch (do NOT migrate `ready/docs/modules/conscious_lm.md` — it describes the byte-level v1/v2/v3 family, NOT v4 530M 64K-SPM).
- (b) Sections (mirror upload spec §4.1 + add narrative front-matter):
  1. **What CLM v4 is** (530M ConsciousDecoderV2; n_substrate paradigm v11 G3 PASS-positive backbone; consciousness-measurement substrate per #115)
  2. **Architecture** (vocab=64000, d_model=768, n_layer=16, GQA n_head=6/n_kv=2, head_dim=128, block=512, consciousness_dim=192, dual heads `head_a`/`head_g`, 8 CA rules, tension_proj per layer)
  3. **Training** (φ★ + cross-entropy losses; multilingual ko/en byte/SPM corpus; step=20000 φ★=27.91 ce=0.046)
  4. **NOT chat** (#115 disclosure; v3_generate AR loop fixed but produces incoherent multilingual sequences absent SFT)
  5. **HF release** (this artifact = `clm-v4-mk2-v1`; cond.2 of `.roadmap.clm`)
  6. **Composability** (BLM Phase 5 / N-1 BRIDGE LSL stream / Stage 2-alt orchestrator / cond.1 G3 verifier)
  7. **License** (MIT) and **citation** (`anima/n_substrate/CLM v4 paradigm v11 G3 +41.86`)
- (c) Length target: 100-200 lines; narrative-first (sister-doc spirit per raw#270).

**Output**: `/Users/ghost/core/anima/docs/modules/clm.md`.

---

### Step 4 — Generate `manifest.json` (release audit-trail) — ~15 min mac + 1 ssh ubu1, $0

**Actions**:
- (a) ssh ubu1: compute sha256 of `~/.cache/huggingface/hub/models--dancinlab--clm-v4-base-mirror/snapshots/856278be.../best.pt` (5GB).
- (b) ssh ubu1: compute sha256 of post-shim `model.safetensors` (2.12 GB) at `~/p9_clm_v4_hf_format_2026_05_04/output/model.safetensors`.
- (c) Mac: read `state/strategic_clm_phase_a1_2026_05_01/run_log.json` and reconstruct best-effort `train_config_recovered.json`.
- (d) Honest fields where reconstruction is best-effort:
  - `seed: "unknown_pretrain_predates_manifest_discipline"` (per audit §C5)
  - `git_sha_at_train: "unknown_pretrain_predates_manifest_discipline"`
  - `corpus_sha256: "unknown_pretrain_predates_manifest_discipline"` (corpus_v10_ko.txt was not sha-recorded; only path is preserved)
- (e) Write to `state/anima_clm_hf_release_v1_2026_05_04/manifest.json` with schema `anima/clm_hf_release_v1_manifest/1`.

**Output**: `state/anima_clm_hf_release_v1_2026_05_04/manifest.json`.

**Note**: the manifest is for audit-trail completeness; it is NOT shipped into the HF repo (the repo gets a smaller `integrity_report.json` co-located with the weights, like `clm-v4-base-mirror` already has).

---

### Step 5 — Draft README.md — ~60 min mac, $0

**Actions**:
- (a) Copy `tool/hf_readme_template.md` to `state/anima_clm_hf_release_v1_2026_05_04/README.draft.md`.
- (b) Fill in all `{{PLACEHOLDER}}` fields.
- (c) Required H2 sections (per upload spec §4.1):
  - `## Origin` — base = anima n_substrate native; train script = `training/train_clm.hexa` (r5); corpus = `corpus_v10_ko.txt` ko-heavy multilingual; recipe ref = `docs/clm_v4_lora_sft_spec_2026_05_04.md` (PRE-train provenance); final metric = step=20000 φ★=27.91 ce=0.046; git sha = `unknown_pretrain_predates_discipline` (honest)
  - `## Falsifiers` — F-CLM-RELEASE-1 (load round-trip via AutoModelForCausalLM trust_remote_code=True; embed test recipe from audit §1.3) / F-CLM-RELEASE-2 (forward finite, vocab=64000) / F-CLM-RELEASE-3 (φ★ structural readout > 0 on 16-prompt sanity battery — DEFERRED to BG-Σ H100 follow-on, marked N/A for v1)
  - `## Substrate` — inference VRAM bf16 ≈ 1.5 GB / 4-bit ≈ 0.4 GB; min py=3.10; required `transformers>=4.45 sentencepiece>=0.2.1 torch>=2.4`; trust_remote_code=True; load tokenizer via `SentencePieceProcessor` (NOT AutoTokenizer); context window 512 SPM tokens
  - `## Caveats` — paste audit §3 Q2 verbatim (C1) + 4 more from audit §1.4 (C2 trust_remote_code / C3 SP-direct load / C4 cross-attn bypass / C5 φ★ tautology)
  - `## Composability` — combines with: `clm-v4-base-mirror` (predecessor); LoRA siblings `clm-v4-sft-stage1` + `clm-v4-sft-step-{5k,10k,25k,50k}`; loaded by `tool/transient_py/clm_v4_hf_format_shim.py`; slots into hexad CLM family; downstream tasks: φ★ measurement, G3 verifier, N-1 BRIDGE LSL stream, cond.2 satisfaction
- (d) YAML frontmatter at top: `license: mit\ntags: [clm, anima, n_substrate, consciousness-measurement, sentencepiece, custom-code]\nlibrary_name: transformers`
- (e) Bibtex citation block at bottom (audit §1.4 template).
- (f) Run `hexa run tool/hf_upload_mk2.hexa --validate-readme state/anima_clm_hf_release_v1_2026_05_04/README.draft.md` → expect `__ANIMA_HF_UPLOAD_MK2__ PASS` (5 H2 + ≥3 caveats).

**Output**: `state/anima_clm_hf_release_v1_2026_05_04/README.draft.md` validated PASS.

**Re-validation**: if `--validate-readme` FAILs, the wrapper names every missing heading explicitly. Iterate.

---

### Step 6 — Stage upload directory — ~10 min mac, $0

**Actions**:
- (a) Decide staging strategy:
  - **Option a (mac-staging then ssh push)**: download HF format dir from `clm-v4-base-mirror` to mac (~2.5 GB), assemble + push from mac. **Pro**: mac controls the full upload. **Con**: 2.5 GB local copy violates anima spirit (HF-only for weights >5MB).
  - **Option b (ubu1-staging via ssh)**: assemble staging dir on ubu1 (`~/anima_clm_release_v1_staging/`), push from ubu1. **Pro**: weights never touch mac; aligns with . **Con**: requires ssh push runbook + ubu1 hf token.
- **Recommended**: Option b (ubu1-staging).
- (b) Staging dir contents (ubu1):
  - `model.safetensors` (cp from `~/p9_clm_v4_hf_format_2026_05_04/output/model.safetensors`)
  - `config.json`, `configuration_clm_v4.py`, `modeling_clm_v4.py`, `decoder_v3.py`, `conscious_decoder.py`, `__init__.py`, `generation_config.json`, `integrity_report.json` (cp from same)
  - `tokenizer_64k_multilingual.model` + `.vocab` (cp from `state/clm_v4_tokenizer_restoration_2026_05_03/` OR fetch from `clm-v4-base-mirror`)
  - `LICENSE` (cp from anima/LICENSE; MIT)
  - `README.md` (rsync from `state/anima_clm_hf_release_v1_2026_05_04/README.draft.md`)
- (c) Pre-validate: `hexa run tool/hf_upload_mk2.hexa --dry-run --repo dancinlab/clm-v4-mk2-v1 --ckpt <staging> --readme <staging>/README.md` → expect PASS.

**Output**: ubu1 staging dir + dry-run audit log at `state/hf_upload_audit/<ts>_dancinlab__clm-v4-mk2-v1.jsonl`.

---

### Step 7 — Private upload (review window) — ~5 min ubu1 + 0 mac, $0

**Actions**:
- (a) Run upload as **private** first to allow user review:
  ```
  hexa run tool/hf_upload_mk2.hexa --upload --private \
      --repo dancinlab/clm-v4-mk2-v1 \
      --ckpt <staging> \
      --readme <staging>/README.md
  ```
- (b) Confirm `commit_url` populated in audit JSONL.
- (c) User reviews HF Hub UI: README renders correctly, weights load sanity (`AutoModelForCausalLM.from_pretrained("dancinlab/clm-v4-mk2-v1", trust_remote_code=True)` on a fresh ubu1/mac shell).

**Output**: private repo at `https://huggingface.co/dancinlab/clm-v4-mk2-v1` with weights + README + LICENSE + tokenizer.

**Failure mode**: if upload fails (HF auth / network / quota), audit log records `outcome:fail` + error; pipeline exponential backoff retries 3 times (2s/4s/8s) per upload spec §6.1.

---

### Step 8 — User review window — ~24-48h elapsed wall, 0 mac, $0

**Actions**:
- User pulls the private repo, runs F-CLM-RELEASE-1 + F-CLM-RELEASE-2 sanity (forward returns finite logits, vocab=64000) on a fresh shell.
- User reads README + LICENSE in HF Hub UI; verifies disclosure C1 is prominent.
- User authorizes promotion to public OR requests README edits (loop back to step 5 with diff).

**Output**: user `OK promote public` decision OR redo loop.

---

### Step 9 — Promote to public — ~2 min ubu1, $0

**Actions**:
- Use HF Hub UI or `huggingface_hub.HfApi.update_repo_visibility(repo_id, private=False)` (via `_python_bridge/hf_upload_runner.py` or one-shot py call).
- Audit log entry: separate `state/hf_upload_audit/<ts>_*_promote_public.jsonl` with `mode: promote_public, ok: 1`.

**Output**: public repo at `https://huggingface.co/dancinlab/clm-v4-mk2-v1`.

---

### Step 10 — cond.2 PASS landing — ~10 min mac, $0

**Actions**:
- (a) Update `.roadmap.clm` cond.2 `status` field: `"unmet"` → `"met"`.
- (b) Append `evidence` array entry: HF repo URL + commit sha + manifest path + landing doc path.
- (c) Clear `blocker_reason` field.
- (d) Land marker: `state/markers/anima_clm_hf_release_v1_landed.marker` with schema `anima/clm_hf_release_v1_landed/1` containing repo_url + commit_sha + ts_utc.
- (e) Author landing handoff: `docs/anima_clm_hf_release_v1_landed_2026_05_04.ai.md` (1-page summary; this audit cycle pre-emits a stub for the form).

**Output**: cond.2 met; marker landed; handoff doc shipped.

---

## §2 Effort summary

| Step | Effort | Cost | Blocking? |
|---|---|---|---|
| 1. User decision turn | 5 min user | $0 | YES (gates 2-10) |
| 2. cond.2 amendment | 10 min mac | $0 | YES (gates 6-10) |
| 3. Author `docs/modules/clm.md` | 30 min mac | $0 | YES (R1 release blocker) |
| 4. Generate `manifest.json` | 15 min mac + 1 ssh | $0 | NO (audit-trail nicety) |
| 5. Draft README | 60 min mac | $0 | YES (R1 release blocker) |
| 6. Stage upload dir | 10 min ubu1 | $0 | YES (gates 7-10) |
| 7. Private upload | 5 min ubu1 | $0 | YES (gates 8-10) |
| 8. User review window | 24-48h elapsed | $0 | YES (gates 9-10) |
| 9. Promote to public | 2 min ubu1 | $0 | YES (gates 10) |
| 10. cond.2 PASS landing | 10 min mac | $0 | — (terminal) |

**Total active work**: ~2.5h mac + 7 min ubu1 + 5 min user + 24-48h review wall. **$0 total.**

**No H100 required for v1.** F-SHIM-V4-4 (train_avg fixture > random + 5pt) + F-CLM-RELEASE-3 (φ★ post-load probe) are post-v1 BG-Σ followups, NOT v1 release blockers.

---

## §3 Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Step 2 grep finds many `anima-clm-mk2-v1` cite paths | LOW | LOW | Most cite paths are in landed ai-md; rewire is mechanical |
| Step 5 `--validate-readme` rejects draft (missing H2) | LOW | LOW | Wrapper names exact missing heading; iterate |
| Step 6 ubu1 disk full / token missing | LOW | MEDIUM | Pre-flight `df -h` + `hf whoami` on ubu1 |
| Step 7 HF 401 on `clm-v4-mk2-v1` create_repo | LOW | MEDIUM | Audit log shows prior 401 on `clm-v4-base-mirror` (2026-05-03) was retried PASS; ensure HF token has write scope on dancinlab org |
| Step 8 user finds README issue | MEDIUM | LOW | Loop back to step 5; private repo can be rewritten freely |
| Step 9 promote-to-public reveals leak | LOW | HIGH | Final scrub: `grep -E '/Users/[^/]+/' README.md` + `grep -E 'sk-|hf_[A-Za-z0-9]+' README.md` (raw#15 + leak_guard discipline) |
| F-SHIM-V4-3 bit-exact suspicion (audit §C4) | LOW | LOW | Re-run with seed variation in BG-Σ followup; not v1 blocker |
| Cond.2 cross-link drift | MEDIUM | LOW | Plan §1 step 2 explicitly amends cross_link.hf_release_planned |

---

## §4 Acceptance criteria (cond.2 PASS gate)

cond.2 is `met` when ALL of the following are true:

1. **HF repo exists + public**: `dancinlab/clm-v4-mk2-v1` (or user-chosen variant) accessible without login at `https://huggingface.co/<repo>`.
2. **README §5 sections present**: 5 H2 (Origin/Falsifiers/Substrate/Caveats/Composability) per `tool/hf_upload_mk2.hexa --validate-readme` PASS.
3. **README ≥3 honest caveats**: per raw#10; chat-disclosure C1 prominent.
4. **License = MIT**: `LICENSE` file in repo root + YAML frontmatter `license: mit`.
5. **Naming = mk2-spec CANON**: `tool/hf_upload_mk2.hexa --validate-naming dancinlab/<repo>` → `__ANIMA_HF_UPLOAD_MK2__ PASS`.
6. **Weights load**: F-CLM-RELEASE-1 (`AutoModelForCausalLM.from_pretrained(<repo>, trust_remote_code=True)`) returns model on a fresh shell.
7. **Forward finite**: F-CLM-RELEASE-2 (1-batch forward returns finite logits, shape [1, T, 64000]).
8. **Sync source exists**: `docs/modules/clm.md` exists in anima git.
9. **`.roadmap.clm` cond.2 status = "met"**: with `evidence` populated + `blocker_reason` cleared.
10. **Marker landed**: `state/markers/anima_clm_hf_release_v1_landed.marker` exists.

---

## §5 Honest C3 (raw#10, ≥3 for plan doc)

### C1 — Plan assumes user picks Option A in Q1
If user picks Option B (amend mk2 spec) or Option C (split umbrella+canonical), step 2 changes shape:
- Option B: instead of cond.2 amendment, draft a `docs/anima_hf_naming_mk2_spec_amendment_2026_*.md` extending §3.1 family enum to include `anima-` umbrella prefix; this ADD effort ~30 min mac and creates a separate spec-land cycle.
- Option C: 2 repos to create (umbrella + canonical), umbrella README is short cross-link-only, canonical gets the full README. Total +20 min mac, +1 upload.

### C2 — Step 8 review window may compress or stretch
24-48h is a typical user-review window; could be 0h (immediate "promote") or 1-7d (deep review with edit requests). Plan totals are best-case wall.

### C3 — Step 7 private upload may surface unknowns
The 2026-05-03 `clm-v4-base-mirror` upload required 2 attempts (first 401, retry PASS). If `clm-v4-mk2-v1` has org-level write quota issues, expect one extra retry cycle. Mitigation: pre-flight `hf whoami` on ubu1 to verify token scope.

### C4 — Plan does NOT cover post-v1 LoRA release
LoRA siblings (`clm-v4-sft-step-{5k,10k,25k,50k}`) already exist as separate repos; this plan does NOT touch them. They will be re-validated against the cond.2 v1 base in a follow-up audit cycle (R1 grace period spec §8.1, 30 days from naming spec land = expires 2026-06-02). NOT a v1 release blocker.

### C5 — Manifest fields are best-effort, not training-time-truth
Pre-mk2 train discipline did not preserve seed / git sha / corpus sha. Manifest will record honest "unknown_pretrain_predates_manifest_discipline" rather than fabricate. Future v5 / v4-1700m / v4-100m must record these from training-time onward.

---

## §6 Outputs (this plan)

- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_plan_2026_05_04.md` (this file)
- (companion: audit doc + landed handoff already written this cycle)

No marker creation in this plan cycle (per directive: spec only, no commit).
