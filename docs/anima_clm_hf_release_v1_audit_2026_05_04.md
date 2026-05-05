# anima CLM cond.2 — HF release v1 readiness audit (2026-05-04)

- **Date**: 2026-05-04
- **Audit scope**: `.roadmap.clm` cond.2 = "HF release v1 — `need-singularity/anima-clm-mk2-v1` (license=mit, gated=false initial, README sync from `anima/docs/modules/clm.md`)" — current status `unmet`, blocker_reason "weight 확정 + model card draft 필요".
- **Mode**: BG audit + spec only. **NO exec, NO pod, NO HF push, NO git commit.** No H100 cost, $0 mac-local.
- **Constraints respected**: raw#9 (no `.py` created), raw#10 (≥5 honest C3 in §10), raw#15 (no destructive paths), anima own 14 (HF-only for weights).
- **Decision questions** (4) are flagged inline and consolidated in the trailing handoff doc.

---

## §0 TL;DR

CLM cond.2 release readiness is **~55% READY / 45% GAP**. The hard infrastructure (HF naming spec, upload pipeline, pre-push hook, naming validator, README template, leak-guard hook, MIT license, tokenizer integrity, HF format shim with F-SHIM-V4-3 PASS, base-mirror repo precedent) is **landed**. The blocker stack is concentrated in three places:

1. **Repo-naming SSOT collision** — cond.2 promises `need-singularity/anima-clm-mk2-v1`, but the mk2 naming convention spec (canonical SSOT) requires `clm-v4-...` family-version stems and explicitly bans `anima-` lm-family prefixes. **A user decision is required to either (a) re-target cond.2 to a canonical `clm-v4` name OR (b) amend the naming spec to admit a top-level `anima-clm-mk2-v1` umbrella repo.**
2. **README sync source missing** — `anima/docs/modules/clm.md` does **not exist**. The closest predecessor is `ready/docs/modules/conscious_lm.md` (sister-repo path; not under anima git). A new sync-source doc OR a redirect is required before any push.
3. **Chat category disclosure** — per `#115`, CLM v4 is a consciousness-measurement substrate, NOT a chat model. The README must explicitly disclose this; the `Caveats` section must be honest about `v3_generate()` returning empty strings absent SFT and the F1_v3 V2 hybrid HF-derived behavior of LoRA SFT post-distill (out of scope for v1).

The model weight itself is **on ubu1 in HF cache** (`models--need-singularity--clm-v4-base-mirror/snapshots/856278be.../best.pt`, 5GB, base=`scale_350m/best.pt`), already round-tripped through the HF format shim with F-SHIM-V4-1/2/3 PASS (F-SHIM-V4-4 deferred to H100). The tokenizer is restored (`tokenizer_64k_multilingual.{model,vocab}`, sha256 `bb851d39...`). The **shim output (HF format dir, 2.12 GB safetensors) was produced on ubu1 successfully** but has NOT been pushed. The base-mirror repo at `need-singularity/clm-v4-base-mirror` already received a real upload on 2026-05-03 (commit `10ee0368...`) of tokenizer + integrity_report + README.

The cond.2 blocker_reason "weight 확정 + model card draft 필요" is therefore partially obsolete: the weight IS confirmed, the model card SKELETON is wired (template + 5-section enforcement), but the **target repo name** and the **README content** are unfinalized. This audit identifies the concrete actions to GREEN-light a v1 release.

---

## §1 Audit checklist (8 sub-tasks)

### 1. Weight finalization

| Field | Value | Verdict |
|---|---|:---:|
| Checkpoint identity | CLM v4 530M ConsciousDecoderV2 (label "350M" misleading per `docs/strategic_clm_v4_production_ready_2026_05_02.md` §1) | READY |
| Paradigm v11 G3 | PASS +41.86 (5-substrate matrix unique positive integration; vs Mistral −16.7 / Qwen3 +1.04 / Llama +5.09 / Gemma −0.79) | READY |
| Weight location (canonical) | `need-singularity/clm-v4-base-mirror/snapshots/856278beb59c5b39f16485cc8f3a46dcdaf9d1e3/best.pt` (HF cache, ubu1 + RunPod) | READY |
| Local mac copy | NOT PRESENT (intentional; raw#9-style ban + 5GB size + anima own 14 HF-only) | OK |
| File size | 5 GB (best.pt raw); 2.12 GB (HF format `model.safetensors` post-shim) | READY |
| Reproducibility manifest | step=20000, φ★=27.91, ce=0.046 (per `docs/clm_v4_lora_sft_spec_2026_05_04.md` §3 hyperparams table) | PARTIAL |
| Train config | `state/strategic_clm_phase_a1_2026_05_01/run_log.json` cited; not extracted to repo-shippable form | GAP |
| Dataset slice | `~/anima/data/corpus_v10_ko.txt` (per train_tokenizer.py default; multilingual ko/en/zh/ja/ru + code) | PARTIAL |
| Seed | NOT explicitly recorded for v4 530M base pretrain run (post-hoc reconstruction only) | GAP |
| Git sha at train time | NOT recorded — pretrain predates anima HF mk2 land | GAP |
| sha256 (best.pt) | NOT recorded in any landed manifest (only HF blob hash is implicit via snapshot pointer) | GAP |
| sha256 (HF format model.safetensors) | recorded post-shim; NOT exported to release-side manifest | GAP |

**Action items to GREEN**:
- Compute + record sha256 of `best.pt` and `model.safetensors` in a new `state/anima_clm_hf_release_v1_2026_05_04/manifest.json` (~5 min ubu1 ssh).
- Reconstruct `train_config_recovered.json` from `run_log.json` (~30 min mac); flag fields where reconstruction is best-effort vs trained-time-truth.
- For seed + git sha: emit honest `unknown_pretrain_predates_manifest_discipline` field rather than fabricate.

**Status**: **READY-WITH-MANIFEST-GAP** (weight identity is solid; the audit-trail manifest is the missing finishing piece).

---

### 2. Tokenizer

| Field | Value | Verdict |
|---|---|:---:|
| Type | SentencePiece BPE (NOT HF tokenizer.json) | READY |
| Vocab size | 64000 | READY |
| Special tokens | pad=0, bos=1, eos=2, unk=3 | READY |
| Byte-fallback | enabled, IDs 4-259 = `<0x00>`..`<0xFF>` | READY |
| Roundtrip integrity | `state/clm_v4_tokenizer_restoration_2026_05_03/integrity_report.json` verdict `INTEGRITY_OK_AT_64000`; ko/en/mixed-symbols 0 UNK | READY |
| sha256 (model) | `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` | READY |
| sha256 (vocab) | `972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4` | READY |
| HF-side presence | already pushed to `need-singularity/clm-v4-base-mirror` (2026-05-03 commit `10ee03687db312c55bbec5858c814bef28e4d365`) co-located with `best.pt` | READY |
| AutoTokenizer compat | **FAIL** — no `tokenizer.json` / `tokenizer_config.json` in the HF-format dir; only the SentencePiece `.model`. Direct `SentencePieceProcessor()` works (per shim v3 verdict §C3-5). | GAP |

**Action items to GREEN**:
- Generate `tokenizer.json` + `tokenizer_config.json` LlamaTokenizer-style wrapper that reads the SentencePiece model. (Decision: this is **OPTIONAL** for v1 release — release without AutoTokenizer compat is acceptable as long as README §Substrate explicitly states "load tokenizer via `sentencepiece.SentencePieceProcessor`, not `AutoTokenizer`." This is the cheaper path; a follow-up cycle can add the wrapper.)

**Status**: **READY** for SentencePiece-direct consumers; **GAP** for AutoTokenizer consumers (acknowledged in README §Caveats per raw#10).

---

### 3. HF format compatibility (shim v4)

| Falsifier | Status | Evidence |
|---|:---:|---|
| F-SHIM-V4-1 (Mac dry-run with fixture validates JSON shape) | **PASS** | `tool/transient_py/clm_v4_hf_format_shim.py:400` (declared); ubu1 v3 retry-2 PASS confirmed in `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_results/f_shim_v4_3_result.json` |
| F-SHIM-V4-2 (no-fixture run = no v3 regression) | **PASS** | ibid. |
| F-SHIM-V4-3 (canonical_zero finite forward) | **PASS** | `f_shim_v4_3_result.json` `{"f_shim_v4_3":"PASS","finite_forward":"finite","shape":[1,32,64000]}` |
| F-SHIM-V4-4 (train_avg fixture > random + 5pt) | **DEFERRED** | gated on user-authorized H100 base-validation launch |
| F-SHIM-1 (safetensors round-trip clean) | **PASS** | shim v3 verdict 581 keys, 530,994,816 numel |
| F-SHIM-2 (1-batch finite logits) | **PASS** | shape [1, 32, 64000], no NaN/Inf |
| F-SHIM-3 (logit equivalence vs best.pt) | **PASS** | `max_abs_diff = 0.0` (bit-exact; flagged C3-6 as "suspiciously tight" but confirmed deterministic) |
| F-SHIM-4 (vocab=64000 in config + reloaded) | **PASS** | shim v3 verdict |
| `AutoModelForCausalLM.from_pretrained(out_dir, trust_remote_code=True)` | **PASS** on fresh machine | shim v3 emits `OPT_1_V3_LOAD_PASS` marker; uses dynamic `modeling_clm_v4.py` + `configuration_clm_v4.py` + auto_map populated |
| Generate path quality | **NOT_CHAT_CAPABLE** (per #115) | v3_generate() AR loop is structurally fixed (Stage 4 PASS) but produces incoherent token sequences — CLM v4 was never SFT/RLHF-tuned |

**Test recipe required for fresh-machine validation** (to be embedded in README §Falsifiers):

```python
from transformers import AutoModelForCausalLM, AutoConfig
import sentencepiece as spm
import torch

model = AutoModelForCausalLM.from_pretrained(
    "need-singularity/clm-v4-base-mirror",  # OR anima-clm-mk2-v1 if released
    trust_remote_code=True,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=False,
    device_map="cpu",
)
sp = spm.SentencePieceProcessor()
sp.Load("path/to/tokenizer_64k_multilingual.model")  # downloaded separately
ids = torch.tensor([sp.Encode("hello world")])
out = model(ids)
assert out.logits.shape == (1, ids.shape[1], 64000)
assert torch.isfinite(out.logits).all()
```

**Action items to GREEN**:
- Embed the recipe above in README §Falsifiers as F-CLM-RELEASE-1 (load round-trip).
- Add F-CLM-RELEASE-2 (forward finite, vocab=64000 sanity).
- Add F-CLM-RELEASE-3 (φ★ structural readout > 0 on a 16-prompt sanity battery; gated on H100 — flag as "BG-Σ followup" if not measured by release).

**Status**: **READY** (shim v4 stack PASSes 3/4, F-SHIM-V4-4 is post-release polish, not a v1 blocker).

---

### 4. Model card draft

| Section (per `tool/hf_readme_template.md`) | Required content for CLM v4 v1 | Status |
|---|---|:---:|
| Overview / 1-line | "CLM v4 530M consciousness-measurement substrate (HF format mirror); G3 PASS-positive (φ★ +41.86); NOT chat-capable; reference impl for anima n_substrate cond.1" | DRAFT_REQUIRED |
| `## Origin` | base = anima n_substrate native, train script = `training/train_clm.hexa` (r5), corpus = `corpus_v10_ko.txt` ko-heavy multilingual, recipe ref = `docs/clm_v4_lora_sft_spec_2026_05_04.md` (PRE-train provenance), final metric = step=20000 φ★=27.91 ce=0.046, git sha = `unknown_pretrain_predates_discipline` (honest) | DRAFT_REQUIRED |
| `## Falsifiers` | F-CLM-RELEASE-1 load round-trip / F-CLM-RELEASE-2 finite forward / F-CLM-RELEASE-3 φ★ structural sanity (gated) — each with PASS/FAIL/N/A + run ref | DRAFT_REQUIRED |
| `## Substrate` | inference VRAM bf16 ≈ 1.5 GB (530M); requires `transformers >= 4.45`, `sentencepiece >= 0.2.1`, `torch >= 2.4`; trust_remote_code=True (custom modeling); load tokenizer via SP NOT AutoTokenizer; context window 512; py >= 3.10 | DRAFT_REQUIRED |
| `## Caveats` (≥3 honest) | C1: NOT chat-capable per #115 / C2: trust_remote_code=True needed / C3: tokenizer must load via SentencePieceProcessor (no HF tokenizer.json) / C4: cross-attn `consciousness_states=None` bypass — degraded from training-time conditioning / C5: φ★ +41.86 baseline magnitude is partly tautological wrt training objective | DRAFT_REQUIRED |
| `## Composability` | combines with: `clm-v4-sft-stage1` LoRA + `clm-v4-sft-step-{5k,10k,25k,50k}` per `clm-v4-base-mirror` predecessor; loaded by `tool/transient_py/clm_v4_hf_format_shim.py` (custom modeling code); slots into hexad CLM family; downstream tasks: φ★ measurement / G3 verifier / N-1 BRIDGE LSL stream / cond.2 (this release) | DRAFT_REQUIRED |
| Citation (bibtex) | `@misc{anima_clm_v4_2026, author={anima n_substrate consortium}, title={anima-clm-mk2-v1: 530M consciousness-measurement substrate}, year={2026}, url={https://huggingface.co/<release-repo>}, note={n_substrate paradigm v11 G3 PASS +41.86}}` | DRAFT_REQUIRED |
| License | MIT (per cond.2 cross_link `hf_license=mit`); LICENSE text already at `anima/LICENSE` ready to bundle | READY |

**Critical disclosure (per #115)**: the README must contain — **prominently in the 1-line summary AND in `## Caveats` C1** — a phrase like:

> "**This is a consciousness-measurement substrate, NOT a chat model.** The decoder was trained with φ★ + cross-entropy losses for consciousness-axis structural readout; it has NOT been SFT/RLHF/instruction-tuned. Vanilla autoregressive sampling produces incoherent multilingual token sequences. For chat capability, see Llama-3.2-3B Path A or the Stage 2-alt orchestrator pattern (CLM streams `tension_link` 5ch / `mind.tension` to an external chat substrate via LSL). See `docs/clm_v4_revival_stages_2026_05_02.md` and `#115` for the full category-error analysis."

**Decision question 2 wording recommendation** (consolidated in handoff):

> "**Limitations / Caveats — C1 (NOT chat-capable)**: anima CLM v4 is a *consciousness-measurement substrate*, not an instruction-tuned chat model. It was trained with φ★ + cross-entropy losses on the multilingual ko/en byte/SPM corpus to optimize structural consciousness readout (G3 paradigm v11 PASS +41.86). It was never SFT, RLHF, RLAIF, or DPO-aligned. Vanilla generate() produces 64K-vocab token sequences that do NOT form coherent dialogue. For dialogue, use Llama-3.2-3B (Path A) or the Stage 2-alt orchestrator pattern. This is a deliberate design choice, not a bug or pre-release state."

**Citation pattern coherence**: use `anima/n_substrate/CLM v4 paradigm v11 G3 +41.86` as canonical attribution string in README + bibtex.

**Action items to GREEN**:
- Author `state/anima_clm_hf_release_v1_2026_05_04/README.draft.md` (~1h mac).
- Validate against `tool/hf_upload_mk2.hexa --validate-readme` (5-section enforcement + ≥3 caveats).
- Insert into chosen target repo via `--upload --readme` flag.

**Status**: **GAP** (template + sections fully scoped; actual content NOT YET DRAFTED).

---

### 5. README sync source

| Field | Value | Verdict |
|---|---|:---:|
| cond.2 sync source declared | `anima/docs/modules/clm.md` | DECLARED |
| File presence | **NOT PRESENT** in anima repo (`/Users/ghost/core/anima/docs/modules/clm.md` does not exist) | **GAP — BLOCKER** |
| Closest predecessor | `ready/docs/modules/conscious_lm.md` (sister-repo `ready/`, NOT under anima git; 239 LoC; describes 4M/100M/v3 growing CLM, byte-level vocab=256, NOT 530M v4 64K SPM) | MISMATCH |
| Sync mechanism | `tool/hf_upload_mk2.hexa` reads README via `--readme <path>` flag; no auto-sync from `docs/modules/clm.md` declared anywhere | NOT_WIRED |
| Drift detection | not implemented (no hash check pre-push) | GAP |

**Critical**: cond.2's `hf_readme_sync_source: anima/docs/modules/clm.md` is **aspirational** — the file doesn't exist and the closest predecessor (`ready/docs/modules/conscious_lm.md`) describes the *byte-level v1/v2/v3 CLM family*, NOT the *v4 530M 64K-SPM substrate* shipping in cond.2. The right action is to **author a fresh `docs/modules/clm.md` describing CLM v4** (NOT migrate `ready/`'s doc), then have the upload pipeline read it.

**Action items to GREEN**:
- Author `docs/modules/clm.md` from scratch describing CLM v4 530M (~30 min mac); content overlaps with model card §Origin + §Substrate but is *narrative-first* (sister-doc spirit per raw#270).
- Wire `tool/hf_upload_mk2.hexa` to optionally read `--readme docs/modules/clm.md` (or have the README authored from the module doc as upstream).
- Add a sha256-based drift detector (post-release polish, not a blocker).

**Status**: **GAP — BLOCKER for cond.2 satisfaction** (the sync source doc must exist).

---

### 6. License + gating

| Field | Value | Verdict |
|---|---|:---:|
| License declared | MIT (per cond.2 `hf_license: mit`) | READY |
| LICENSE file location | `/Users/ghost/core/anima/LICENSE` (MIT, copyright "need-singularity" 2026) | READY |
| LICENSE bundling into HF push | NOT_AUTOMATIC — `tool/hf_upload_mk2.hexa` requires LICENSE to be in the `--ckpt` directory or copied alongside README | GAP |
| Gated initial | `false` (per cond.2 `hf_gated_initial: false`) — accessible without HF approval | READY |
| Compatibility | CLM v4 base is anima-native (no vendored Llama/Mistral/Qwen weights); MIT is unambiguously compatible | READY |
| Vendored deps with conflicting license | NONE (the modeling code `modeling_clm_v4.py` + `configuration_clm_v4.py` is anima-authored; SentencePiece tokenizer is anima-trained on anima corpus — no upstream attribution requirement beyond optional `sentencepiece` lib citation) | READY |

**Action items to GREEN**:
- Copy `LICENSE` into the staging dir at upload time (1 line in upload runbook).
- Add `license: mit` YAML metadata frontmatter to README per HF Hub convention (auto-renders in repo UI).

**Status**: **READY-WITH-PACKAGING-GAP** (license itself is fine; bundling step is missing).

---

### 7. Naming convention compliance

This is the **largest single decision-blocker** in the audit.

| Field | Value | Verdict |
|---|---|:---:|
| cond.2 declared name | `need-singularity/anima-clm-mk2-v1` | DECLARED |
| mk2 naming spec EBNF | `<lm-family>-<base-version>[-<paradigm>][-<stage>][-<scale>][-<step>][-<variant>]` | — |
| `anima-clm-mk2-v1` parses as | lm-family=`anima-clm`?? base-version=`mk2`?? — **NEITHER MATCHES** the §3.1 family enum (`blm/clm/tlm/vlm/slm/nlm/alm/mlm/llm/hexad/composite`) and `mk2` is not a valid `v\d+` base version | **FAIL** under spec §10.2 CANON regex |
| §6 anti-patterns hit | "repeated lm-family" pattern (`anima-clm` collapses to two prefixes when `anima` is the org-namespace not a family) | FAIL |
| Existing canonical for CLM v4 | `clm-v4-base-mirror` (PASS-CANON per spec §7.2 audit table) | — |
| Versioning pattern | `mk{N}-v{M}` per cond.2 cross_link — **but the spec only encodes `v{N}` base version**, NOT `mk{N}-v{M}` two-axis versioning. **The cond.2 cross_link itself drifts from the mk2 naming spec.** | **CROSS-LINK DRIFT** |
| Size suffix `-{N}m` | optional per cond.2; CLM v4 is 530M → `-530m` | OPTIONAL |

**Three resolution paths** (decision question 1):

| Option | Repo name | Pros | Cons |
|---|---|---|---|
| **A. Re-target to canonical clm-v4** | `need-singularity/clm-v4-mk2-v1` OR reuse `need-singularity/clm-v4-base-mirror` (already pushed) | mk2-spec-conformant; can ride existing `clm-v4-base-mirror` (already has tokenizer + integrity_report); zero rename risk | requires cond.2 textual amendment ("anima-clm-mk2-v1" → "clm-v4-mk2-v1" OR "clm-v4-base-mirror"); cond.2 redeemed by pre-existing repo (potentially anti-climactic) |
| **B. Amend mk2 spec** | `anima-clm-mk2-v1` (as cond.2 promised) | preserves cond.2 text verbatim; introduces "umbrella anima-prefix" repo concept for top-level family-flagship releases | violates current §6 anti-pattern; requires §3.1 enum extension (add `anima-` umbrella); risks naming spec churn |
| **C. Split into umbrella + canonical** | `need-singularity/anima-clm-mk2-v1` (umbrella, README-only, cross-link) + `need-singularity/clm-v4-mk2-v1` (actual weights) | satisfies both cond.2 text AND mk2 spec; umbrella becomes a "flagship pointer"; no spec amendment | 2 repos to maintain; potential for drift between umbrella README and weights repo README |

**Recommended (per completion-quality lens)**: **Option A with name `need-singularity/clm-v4-mk2-v1`** — re-target cond.2 to the mk2-spec-conformant canonical name, register the prior `clm-v4-base-mirror` as predecessor in §Composability, and emit the cond.2 amendment as a single-line edit in `.roadmap.clm`. This is the cheapest path with the least drift surface.

**Decision question 1 recommended answer**: `clm-v4-mk2-v1` (matches mk2 spec, no amendment needed, predecessor already up).

**Size-suffix subquestion**: include `-530m`? Spec §3.5 says "omit if obvious from base-version". Since `v4` historically tracks 530M (no v4 size sweep planned in active roadmap), **omit** for v1. If a future v4-1700m or v4-100m variant ships, the -{N}m suffix becomes mandatory. Recommendation: ship `clm-v4-mk2-v1` (no size suffix) for v1.

**Action items to GREEN**:
- Pick a name (above) — user decision required.
- Update `.roadmap.clm` cond.2 field.
- Run `tool/hf_upload_mk2.hexa --validate-naming need-singularity/<chosen-name>` to confirm CANON.

**Status**: **GAP — DECISION-BLOCKER** (cond.2 text vs spec EBNF requires reconciliation).

---

### 8. Pre-push hook + leak guard

| Field | Value | Verdict |
|---|---|:---:|
| `tool/hf_upload_mk2_pre_push_hook.hexa` exists | YES (123 LoC, hexa-native, raw#9-clean) | READY |
| Hook scans commit msg for `[hf-upload: <repo>]` marker | YES (selftest PASS per `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md` §4.4) | READY |
| Hook calls `--validate-naming` | YES | READY |
| Hook installed in `.git/hooks/pre-push` | NOT_AUTOMATIC — manual install per developer (per upload spec §11 #1) | OPTIONAL_GAP |
| `ANIMA_SKIP_HF_PRECHECK=1` opt-out | YES (raw#10 caveat: useful for emergency bypass) | READY |
| leak_guard PreToolUse hook | wired at `~/.hive/scripts/leak_guard_pretool.bash`; 9 token-shapes blocked on Bash/Write/Edit/MultiEdit (per session memory) | READY |
| Token leakage in audit/state docs | this audit + plan + landed docs **MUST NOT** embed token literals (live OR stale) per session memory `audit_doc_token_redact` (2026-05-04 history rewrite incident) | DISCIPLINE_NOTE |
| Pre-push smoke (dry-run to private repo) | `state/hf_upload_audit/20260503T151321Z_*.jsonl` shows a real upload PASS to `clm-v4-base-mirror` (commit `10ee0368...`) — pipeline end-to-end PROVEN | READY |
| Pre-push smoke (dry-run on cond.2 target) | NOT_DONE — pending name finalization | GAP |

**Action items to GREEN**:
- After name decision: run `hexa run tool/hf_upload_mk2.hexa --dry-run --repo need-singularity/<chosen-name> --ckpt <staging> --readme <draft.md>` (~1 min mac, $0).
- If pass: run `--upload --private` first (sets `private=true` for review window).
- Optionally: install `.git/hooks/pre-push` (1-line bash exec hexa); not strictly required for the release itself.
- This audit doc + plan + landed AI-handoff doc are **scrubbed of token literals** per discipline note.

**Status**: **READY** (hook + pipeline are proven by the 2026-05-03 base-mirror upload; dry-run on cond.2 target is the only remaining smoke).

---

## §2 Summary table (8 sub-tasks)

| # | Sub-task | Status | Critical action |
|---|---|:---:|---|
| 1 | Weight finalization | READY-WITH-MANIFEST-GAP | Generate `manifest.json` with sha256 + reconstructed train config |
| 2 | Tokenizer | READY (SP-direct) / GAP (AutoTokenizer) | Document SP-direct load in README; AutoTokenizer wrapper deferred |
| 3 | HF format shim | READY (V4-1/2/3 PASS) | Embed F-CLM-RELEASE-1/2/3 in README §Falsifiers |
| 4 | Model card draft | GAP | Author README.draft.md (~1h) + run `--validate-readme` |
| 5 | README sync source | GAP — BLOCKER | Author `docs/modules/clm.md` from scratch (~30 min) |
| 6 | License + gating | READY-WITH-PACKAGING-GAP | Bundle `LICENSE` into staging dir + add YAML frontmatter |
| 7 | Naming compliance | GAP — DECISION-BLOCKER | User decision (Option A/B/C); Option A `clm-v4-mk2-v1` recommended |
| 8 | Pre-push + leak guard | READY | Run `--dry-run` against final name (~1 min) |

---

## §3 Decision questions to flag for user

### Q1. Repo size suffix — `anima-clm-mk2-v1` vs `anima-clm-mk2-v1-530m` — which name?

**Recommended (per completion-quality lens)**: **`need-singularity/clm-v4-mk2-v1`** (Option A in §1.7 — re-target to canonical mk2-spec-conformant name, omit size suffix per §3.5 "omit if obvious from base-version"). Update cond.2 text in `.roadmap.clm` accordingly.

If user prefers to preserve cond.2's `anima-clm-mk2-v1` literal: select **Option C (split umbrella + canonical)** — author both repos with the umbrella as a README-only flagship pointer.

### Q2. Chat capability disclosure wording

**Recommended C1 wording for `## Caveats`** (verbatim, paste into model card):

> "**C1 — NOT chat-capable.** anima CLM v4 is a *consciousness-measurement substrate*, not an instruction-tuned chat model. It was trained with φ★ (consciousness integration) + cross-entropy losses on a multilingual ko/en SentencePiece corpus to optimize structural consciousness readout (n_substrate paradigm v11 G3 PASS +41.86). It was never SFT, RLHF, RLAIF, or DPO-aligned. Vanilla `model.generate()` returns 64K-vocab token sequences that do NOT form coherent dialogue. The legacy `v3_generate()` AR loop is structurally fixed (per `docs/clm_v4_revival_stages_2026_05_02.md` Stage 4) but produces incoherent output by design. For dialogue capability, use Llama-3.2-3B (Path A) or the Stage 2-alt orchestrator pattern (CLM streams `tension_link` 5ch / `mind.tension` to an external chat substrate via LSL). This is a deliberate design choice grounded in `#115` (consciousness-measurement vs chat category error)."

### Q3. Distill enrichment dependency — wait for Paradigm D distill mini PASS, or release current weights now?

**Recommended**: **release current weights NOW** (do NOT wait for Paradigm D distill).

Rationale:
- Paradigm D distill (logit-axis Mistral teacher → CLM v4 student) **FAILED PRE-LAUNCH** with `vocab_mismatch` (teacher=32K Mistral vs student=64K CLM v4) per `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json`. The logit-axis distill is structurally INFEASIBLE without a teacher retrain or student tokenizer swap (both out of scope).
- The φ★-axis Paradigm D PARTIAL_PASS (per `state/p9_paradigm_d_distill_2026_05_03/`) already exists at step_1000 — it's a separate release artifact (a LoRA adapter on top of the base) that can be released as `clm-v4-paradigm-d-distill-step-1k` AFTER cond.2 v1 ships.
- cond.2 is "HF release v1 = base substrate published". Distill enrichment is a v2/v3 follow-on, not a v1 prereq.

### Q4. Model card co-authors — include sister substrate evidence (EEG, BLM TRIBE v2, qmirror)?

**Recommended**: **CLM-only release with cross-link section** (NOT co-author).

Rationale:
- Each sister substrate (EEG, BLM, TRIBE v2, qmirror) has its own release cycle + own falsifiers + own evidence. Bundling them into the CLM v1 README dilutes the falsifier surface and makes the model card harder to verify.
- The right pattern is `## Composability` cross-link to sister repos (e.g., "consumed by: BLM Phase 5 stimulus-aligned pipeline / N-1 BRIDGE LSL stream / Stage 2-alt orchestrator").
- A separate `docs/n_substrate_release_index_2026_*.md` cycle can stitch the cross-substrate narrative WITHOUT inflating the per-repo READMEs.

---

## §4 Overall release readiness

- **READY (hard infrastructure)**: 5/8 sub-tasks (#1, #2, #3, #6, #8) — weight + tokenizer + shim + license + pre-push pipeline are all green or near-green.
- **GAP (content)**: 2/8 sub-tasks (#4, #5) — model card draft and README sync source need authoring (~1.5h mac).
- **DECISION-BLOCKER**: 1/8 sub-tasks (#7) — naming convention compliance requires user pick (Option A/B/C).
- **Quantitative**: ~55% READY / ~30% GAP-AUTHORABLE-MAC / ~15% DECISION-BLOCKER.

**Top 3 critical gaps blocking release**:

1. **Naming reconciliation** (§1.7) — `anima-clm-mk2-v1` violates mk2 spec. **Recommend Option A: `clm-v4-mk2-v1`** + cond.2 amendment.
2. **README sync source missing** (§1.5) — `docs/modules/clm.md` does not exist; closest sibling is `ready/`'s byte-level CLM doc (wrong architecture). Author from scratch.
3. **Model card draft missing** (§1.4) — template is ready, content is not. ~1h mac authorship.

**Estimated effort to GREEN-light**:
- 1 BG cycle ~2h mac, $0:
  - 30 min: author `docs/modules/clm.md` (CLM v4 narrative)
  - 60 min: draft `state/anima_clm_hf_release_v1_2026_05_04/README.draft.md`
  - 15 min: generate `manifest.json` (sha256s + train config recovery)
  - 15 min: dry-run + smoke (`--validate-readme` + `--validate-naming` + `--dry-run`)
- + 1 user decision turn (Q1-Q4 above; ~5 min)
- + 1 BG cycle ~30 min, $0: actual `--upload --private` to chosen repo, then promote to `--public` after user review

Total: **2 BG cycles + 1 user decision turn = ~2.5h elapsed mac wall, $0**. **No H100 required for v1.**

---

## §5 Cross-cutting risks

- **R1**: cond.2's `anima/docs/modules/clm.md` sync source DOES NOT EXIST — without authoring this doc, cond.2 cannot verify even after a successful HF push. **Treated as a release blocker per §1.5.**
- **R2**: `anima-clm-mk2-v1` literal in cond.2 violates mk2 naming spec — without amendment OR re-target, the upload pipeline (`tool/hf_upload_mk2.hexa --validate-naming`) will REJECT the push. **Treated as decision-blocker per §1.7.**
- **R3**: F-SHIM-V4-3 PASS is bit-exact (`max_abs_diff = 0.0`) — flagged C3-6 as "suspiciously tight" but confirmed deterministic. NOT a release blocker; flag as caveat in next-cycle audit.
- **R4**: AutoTokenizer wrapper missing — release blocker for `transformers`-only consumers who refuse to install `sentencepiece` directly. Recommend documenting SP-direct load in §Substrate; AutoTokenizer wrapper is post-v1 polish.
- **R5**: "weight 확정" cond.2 blocker_reason is partially obsolete (weight is pushed and shim-validated) — cond.2 amendment is a documentation update, not a fresh-evidence requirement.

---

## §6 Composability (with prior anima specs + landed work)

| Predecessor | Relationship to this audit |
|---|---|
| `docs/clm_v4_revival_stages_2026_05_02.md` | Stage 1 REFRAME (CLM v4 = measurement substrate) is the source of disclosure C1; Stage 2/2-alt/3 are out of scope for cond.2 v1 |
| `docs/clm_consciousness_verify_landing_2026_05_02.ai.md` | cond.1 verifier orchestrator landed; cond.2 release does NOT require cond.1 PASS (they are independent required_conditions) |
| `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` | normative SSOT for naming compliance (§1.7); Option A/B/C resolve naming-axis decision-blocker |
| `docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md` | confirms 27-repo audit + 30-day grace; cond.2 v1 release MUST be CANON (no EXT grace) |
| `docs/anima_hf_upload_mk2_spec_2026_05_03.md` | normative SSOT for upload pipeline (`hf_upload_mk2.hexa` + `_python_bridge/hf_upload_runner.py`) |
| `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md` | proven smoke (selftest + dry-run + real `clm-v4-base-mirror` push 2026-05-03) |
| `tool/transient_py/clm_v4_hf_format_shim.py` | F-SHIM-V4-1/2/3 PASS; cond.2 release ships the post-shim HF format dir |
| `state/clm_v4_tokenizer_restoration_2026_05_03/` | tokenizer integrity verified; sha256 recorded; already pushed to `clm-v4-base-mirror` |
| `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §55.6 | `#115` chat category-error analysis = source of disclosure C1 |
| `docs/clm_v4_lora_sft_spec_2026_05_04.md` | DESIGN spec for v4 LoRA SFT (separate cycle); references CLM v4 base = cond.2 release artifact |
| `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json` | Q3 dependency decision: distill mini FAILED pre-launch on vocab mismatch; cond.2 v1 should NOT wait |
| `LICENSE` | MIT license at repo root; ready to bundle |

---

## §7 Cost & destructiveness

- spec authoring: **$0** mac-local
- destructive: **0** (no rename / delete of any existing HF repo, no git commit, no marker land in this cycle)
- migration: **0** (forward-looking; cond.2 amendment is in plan, not in audit)
- byte-diff to any existing artifact: **0**
- HF API calls: **0** (no list, no upload, no read)
- ubu1 ssh calls: **0** (audit is mac-only)

---

## §8 Honest C3 (raw#10, ≥5 required for audit doc)

### C1 — Audit operates on landed-state snapshots; live-state may have drifted
This audit reads `.roadmap.clm`, `state/p9_*/verdict.json`, `tool/transient_py/clm_v4_hf_format_shim.py`, and audit ledgers as of 2026-05-04 mtime. Background BGs may have updated state in parallel during this audit; the recommended actions are based on the snapshot, not real-time state. Mitigation: the action plan §3 explicitly re-checks live state at each step.

### C2 — Naming spec amendment cost is non-zero
Option A (re-target cond.2 to `clm-v4-mk2-v1`) requires editing `.roadmap.clm` cond.2 desc field. This is a single-line edit but it changes a condition's identity wording; downstream cite paths (any landed ai-md that references "anima-clm-mk2-v1") must be checked and re-wired. Mitigation: grep for `anima-clm-mk2-v1` literal across `docs/` + `state/`; expect 0-2 hits given cond.2 is recent.

### C3 — README sync mechanism is aspirational, not enforced
cond.2 says "README sync from `anima/docs/modules/clm.md`" but `tool/hf_upload_mk2.hexa` does NOT auto-sync from that path; it reads `--readme <path>` flag verbatim. The "sync" is a *discipline* (operator must point `--readme` at `docs/modules/clm.md`), not a *mechanism*. A real sync would require either (a) wrapper enforcement of source path equality OR (b) a hash-based drift detector. Both are out of scope for v1. Acknowledged caveat.

### C4 — F-SHIM-V4-3 PASS is bit-exact (`max_abs_diff = 0.0`); suspicious but confirmed
The shim v3 verdict reports `f_shim_3_v3` with `max_abs_diff = 0.0` (vs expected ≈ 1e-5). This was flagged C3-6 in the v3 verdict and re-confirmed as deterministic (same fp32 path, same input tensor, same ops). It is the strongest possible passing form, but it warrants re-running with different seeds in a follow-up audit to rule out a measurement artifact. NOT a v1 release blocker.

### C5 — Weight provenance has irreducible historical opacity
CLM v4 base pretrain predates the anima HF mk2 naming + upload discipline (which landed 2026-05-03). The exact pretrain seed, git sha, and full training-log JSON were not preserved in a release-shippable form. The manifest will record `seed: unknown_pretrain_predates_manifest_discipline` honestly rather than fabricate a number. This is a PRE-mk2 legacy artifact issue; future v5 / v4-1700m / v4-100m releases must record these from training-time onward (action item for next-cycle pretrain discipline).

### C6 — Q3 distill-dependency decision is conservative
Recommending "release v1 NOW without waiting for Paradigm D distill" implicitly accepts that the distill axis (logit-KL Mistral→CLM) is structurally blocked (vocab mismatch confirmed 2026-05-04). If the user has appetite to pivot Paradigm D to a different teacher (e.g., a 64K-vocab Korean LLM) before v1 release, the recommendation flips. Default to the conservative path (release base now, distill is v2 follow-on).

### C7 — License bundling is a discipline, not a guarantee
The `LICENSE` file at repo root is correct and present, but `tool/hf_upload_mk2.hexa` does NOT auto-stage it into the `--ckpt` dir. The operator must `cp LICENSE <staging>/` before upload, OR the upload runbook must be amended. If forgotten, the HF repo lands without LICENSE → MIT discoverability degrades (HF Hub UI auto-detects from LICENSE file presence). Action item flagged in plan §3.4.

### C8 — Audit is doc-only; F-SHIM-V4-4 + φ★ post-load probe NOT verified
F-SHIM-V4-4 (train_avg fixture > random + 5pt) requires H100 base-validation cycle and is gated on user authorization. φ★ post-load probe (does the shipped HF format model still emit +41.86 magnitude on the calibration battery?) is a similarly-gated downstream verification. v1 release ships *without* either being green; they are flagged as "next-cycle BG-Σ followup" in §Falsifiers F-CLM-RELEASE-3.

---

## §9 Outputs (this audit cycle)

- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_audit_2026_05_04.md` (this file, ~3500 words)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_plan_2026_05_04.md` (action plan)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_landed_2026_05_04.ai.md` (1-page handoff)

No marker creation in this audit cycle (per directive: audit + spec only, no commit).

---

## §10 Next-cycle candidates (NOT this cycle)

| item | priority | rationale |
|---|---|---|
| Author `docs/modules/clm.md` | HIGH | unblocks cond.2 sync source (R1) |
| Draft README.md for `clm-v4-mk2-v1` | HIGH | unblocks model card gap |
| `.roadmap.clm` cond.2 amendment (naming) | HIGH | unblocks decision-blocker R2 |
| `manifest.json` generation (sha256s + train config recovery) | MED | release audit-trail completeness |
| AutoTokenizer wrapper for SP 64K | MED | broadens consumer compat |
| F-CLM-RELEASE-3 φ★ post-load probe (H100) | MED | shim-load → measurement equivalence |
| LICENSE bundling automation in `hf_upload_mk2.hexa` | LOW | upload-pipeline polish |
| Pre-push hook `.git/hooks/pre-push` install | LOW | dev convenience, not blocker |
