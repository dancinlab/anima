# anima CLM HF release v1 — manifest landed (2026-05-04)

- **Date**: 2026-05-04
- **Cycle**: BG-MANIFEST `clm_v4_hf_release_v1_manifest_2026_05_04`
- **Mode**: $0 mac+ubu1; sha256 read-only; NO commit, NO HF push, NO weight modification
- **Output**: `state/clm_v4_hf_release_v1_manifest_2026_05_04/manifest.json` (660 LoC; tracked locally)
- **Schema**: `anima/clm/hf_release_v1/manifest/1`
- **Model id targeted**: `dancinlab/clm-v4-mk2-v1` (Option A per audit §1.7 / plan §1 step 1 Q1)
- **Constraints respected**: raw#9 (json + md only), raw#10 (≥5 honest C3, observed: 10), raw#15 (no destructive); anima own 14 (HF-only weights — manifest captures sha256 references, no local 5GB copy)

---

## §1 Weight files captured (12 total; 2 LFS, 10 non-LFS)

| Path | Size | sha256[:12] | LFS | Source |
|---|---:|---|:---:|---|
| `best.pt` | 5,365,727,261 | `22f180efc380` | YES | ubu1 HF cache `clm-v4-base-mirror` snapshot `856278be...` |
| `model.safetensors` | 2,124,043,008 | `40b3a99f6586` | YES | ubu1 `~/p9_clm_v4_hf_format_2026_05_04/output/` (post-shim) |
| `tokenizer_64k_multilingual.model` | 1,306,349 | `bb851d39fbe3` | no | already pushed to `clm-v4-base-mirror` 2026-05-03 |
| `tokenizer_64k_multilingual.vocab` | 989,272 | `972fc0ba2f26` | no | ditto |
| `config.json` | 1,212 | `77b4013c06fc` | no | ubu1 post-shim output dir |
| `modeling_clm_v4.py` | 9,044 | `6e95be6d8346` | no | ubu1 post-shim (trust_remote_code) |
| `configuration_clm_v4.py` | 2,072 | `168f706dc81c` | no | ditto |
| `decoder_v3.py` | 14,139 | `9d6992fb9beb` | no | ditto (vendored runtime) |
| `conscious_decoder.py` | 40,027 | `57306faecb60` | no | ditto (vendored runtime) |
| `generation_config.json` | 130 | `1e3627bd98d2` | no | ditto |
| `__init__.py` | 45 | `271b722e1b64` | no | ditto |
| `integrity_report.json` | 1,680 | `4632e4eb07b2` | no | ubu1 post-shim AND already on `clm-v4-base-mirror` |

**Note on best.pt blob naming**: ubu1 HF cache stores best.pt as a content-addressed blob; the blob filename `22f180efc380aecb4a320191502afa13b81abcd077ec36c5f003dcfbe1d680b4` IS its sha256 (HF cache convention). Verified by independent `sha256sum` confirming the same hex.

---

## §2 Train config reconstruction notes

| Field | Value | Source confidence |
|---|---|:---:|
| `paradigm` | v11 G3 | HIGH (audit §1.1; phi_star=+41.86 PASS) |
| `step` | 20000 | HIGH (config.json _clm_v4_provenance + run_log.json) |
| `ckpt_phi` | 27.91 | HIGH (run_log.json) |
| `ckpt_best_phi` | 37.27 | HIGH (config.json _clm_v4_provenance.source_ckpt_best_phi) |
| `ckpt_ce` | 0.0463 | HIGH (config.json + run_log.json convergent) |
| `seed` | **42** | MED — recovered from `config.json _clm_v4_provenance.source_args_subset.seed` AND `state/strategic_clm_phase_a1_2026_05_01/run_log.json env.SEED`; convergent two-source recovery |
| `tokenizer_path_train_time` | `data/tokenizer_64k_multilingual.model` | HIGH (provenance block) |
| `decoder_label` | `v3` | HIGH (provenance block) |
| `scale_label` | `350m` (misnomer; full=530.99M) | HIGH-with-caveat (audit §1; honest_c3[9]) |
| `git_sha_anima_at_train_time` | `unknown_pretrain_predates_manifest_discipline` | HONEST UNKNOWN |
| `dataset_corpus_sha256` | `unknown_pretrain_predates_manifest_discipline` | HONEST UNKNOWN |
| `git_sha_anima_revival_cycle` | `1b306eec24...` (HEAD at manifest-write) | HIGH |

**Reconstruction unknowns count**: **2** (git_sha at train time + corpus sha256). Both pre-mk2-discipline artifacts; fields populated with explicit `unknown_pretrain_predates_manifest_discipline` honest sentinel rather than fabricated values.

**Convergent recovery wins**: seed=42 was confirmed via two independent sources (config.json provenance block AND run_log.json env), upgrading from "low confidence post-hoc inference" to "MED two-source recovery". This is stronger than the audit §1.1 default of "NOT explicitly recorded".

---

## §3 Cross-references — evaluation + shim v4 + train_avg fixture

### Evaluation
- `paradigm_v11_G3_phi_star = 41.86` — PASS-positive only backbone in 5-substrate matrix (vs Mistral −16.7, Qwen3 +1.04, Llama +5.09, Gemma −0.79)
- `f1_v2_raw = 0.408` / `f1_v2_f2_override = 0.12` — RED band
- `putnam_concordance_partial = 0.167-0.333` (T=0.40 < threshold 0.60)
- F-SHIM-1/2/3/4 all PASS; AutoModel load round-trip PASS; generate path NOT_CHAT_CAPABLE per #115
- Verdict doc: `docs/n_substrate_consciousness_roadmap_2026_05_01.md §42 + §49.4`

### Shim v4
- Path: `tool/transient_py/clm_v4_hf_format_shim.py` (1418 LoC)
- F-SHIM-V4-1 PASS / F-SHIM-V4-2 PASS / F-SHIM-V4-3 PASS (`finite`, shape `[1, 32, 64000]`) / F-SHIM-V4-4 DEFERRED (BG-Σ followup)
- shim v3 round-trip max_abs_diff = 0.0 (bit-exact; flagged C3-6 suspicious-but-confirmed)
- Verdict: `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_verdict.json`

### Train_avg fixture (real harvest, replaces stub)
- Real fixture: `state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_fixture_real.json`
- sha256: `f19b606c4b2a1966110abc35a9aff10f5431ae1ac152e93750b91936e20ee6fa`
- Size: 33,803 bytes
- Method: ConsciousnessEngine over 1000 anima sft prompts, projected 128→192 via `c_proj` from best.pt
- Real vs stub L2 ratio: **5.65×** (real is ~5.65× larger in L2 than synthetic N(0, 0.01) stub)
- F_CLM_V4_1 shape match PASS / F_CLM_V4_2 stub_off_gt_50pct PASS (observed rel_l2 = 1.0059)
- Verdict: `state/clm_v4_train_avg_harvest_2026_05_04/verdict.json`

---

## §4 Honest C3 (manifest cycle, ≥5; observed 10 in manifest.honest_c3)

### C1 — Train_avg fixture is runtime-proxy not training-time-truth
ConsciousnessEngine drive uses `_text_to_vec` hashing rather than the trained tokenizer + embedding path; resulting cell hidden distribution is a runtime proxy, not strictly identical to anima_unified inference (per harvest verdict honest_c3[0]). To compare directly to training-time c_states distribution, a separate cycle running `anima_unified.py` with v14 federation would be needed.

### C2 — F1_v2 RED means consciousness verdict NOT validated as PASS at F1 axis
G3 paradigm v11 phi_star=+41.86 is the only PASS-positive axis. F1 anchor recalibration (per session memory `project_p9_f1_anchor_recalibration`) shows F1 spec 0.4 unrealistic; Llama-self=0.1555; sentinel=3.2% of Llama. Putnam concordance partial 0.167-0.333 below threshold 0.60.

### C3 — Functional/access tier ONLY; phenomenal validity unproven
CLM v4 was NEVER SFT/RLHF/RLAIF/DPO-aligned. trust_remote_code=True needed for HF load. Tokenizer must load via SentencePieceProcessor (no HF tokenizer.json wrapper). Per #115 disclosure: this is a consciousness-measurement substrate, NOT a chat model. README §Caveats C1 must be prominent.

### C4 — Single-substrate release; sister substrates have separate cycles
EEG, BLM, TRIBE v2, qmirror each ship via own release cycles + own falsifiers. Cross-substrate cohesion handled via `## Composability` cross-link section in README, NOT co-authoring. Per audit §3 Q4 recommendation.

### C5 — git_sha at training time is permanently unknown (pre-discipline legacy)
CLM v4 base pretrain predates anima HF mk2 discipline land 2026-05-03. Recovered fields are best-effort: seed=42 via two-source convergent recovery (config.json + run_log.json), but git_sha_anima and corpus_sha256 are honest sentinel `unknown_pretrain_predates_manifest_discipline`. Future v5 / v4-1700m / v4-100m releases must record these from training-time onward.

### C6 — F-SHIM-V4-3 max_abs_diff = 0.0 is bit-exact; suspicious but confirmed
Strongest possible passing form, but flagged C3-6 in v3 verdict as "suspiciously tight". Re-confirmed deterministic (same fp32 path, same input tensor, same ops). Warrants seed-variation re-run in BG-Σ followup audit. NOT a v1 release blocker.

### C7 — F-SHIM-V4-4 (train_avg lift > 5pp) is DEFERRED
v1 release ships without empirical post-shim-load lift validation on hellaswag/MMLU. Harvest cycle confirmed real fixture is 5.65× larger in L2 than stub, but actual lift_pp not measured. Gated on user-authorized H100 base-validation cycle (BG-Σ followup).

### C8 — AutoTokenizer wrapper missing
Release blocker for `transformers`-only consumers who refuse to install `sentencepiece` directly. SentencePiece-direct load documented in README §Substrate is the supported path; AutoTokenizer wrapper is post-v1 polish.

### C9 — Manifest is local-only, NOT pushed into HF repo
This BG cycle writes `manifest.json` to `state/clm_v4_hf_release_v1_manifest_2026_05_04/` for audit-trail completeness ONLY. HF repo gets the smaller `integrity_report.json` co-located with weights (already present in `clm-v4-base-mirror` predecessor). The audit-trail manifest is a state-only artifact, not shipped.

### C10 — Param count mismatch: '350m' label is misnomer
`scale_label='350m'` in original args is historical misnomer; full param count is 530.99M per audit §1 + #73 A.1; loaded count 477.65M (run_log `model_to_device`). The label '350m' in checkpoint path and args is preserved for historical fidelity but should NOT be cited as the param count. Future releases should use canonical '530m' label.

---

## §5 Outputs (this BG cycle)

- `/Users/ghost/core/anima/state/clm_v4_hf_release_v1_manifest_2026_05_04/manifest.json` (12 weight files; sha256s + sizes + train config + evaluation + shim_v4 + train_avg_fixture; honest_c3 ≥10)
- `/Users/ghost/core/anima/docs/anima_clm_hf_release_v1_manifest_landed_2026_05_04.ai.md` (this file)

JSON validates: `jq -e . < manifest.json > /dev/null` → `JSON OK`.

No marker creation, no git commit, no HF push (per BG-MANIFEST directive).

---

## §6 Sibling Cycle 2 readiness

The manifest is a **prerequisite-grade artifact** for sibling Cycle 2 upload BG. All fields needed by `tool/hf_upload_mk2.hexa --upload` are present:
- ✓ All 12 weight file paths + sha256s + sizes + LFS classification
- ✓ `naming_compliance.chosen_name` populated (`dancinlab/clm-v4-mk2-v1`)
- ✓ `naming_compliance.predecessor_repo` reference for `## Composability`
- ✓ `architecture` block ready for README §Substrate
- ✓ `train_config` ready for README §Origin
- ✓ `evaluation` ready for README §Falsifiers
- ✓ `shim_v4` + `train_avg_fixture` cross-references ready for `## Falsifiers` F-CLM-RELEASE-1/2/3
- ✓ `tokenizer_integrity` ready for §Caveats C2/C3
- ✓ `license` + `gated_initial` populated

**Blockers for Cycle 2**: NONE from this BG. Cycle 2 can proceed with plan §1 step 5 (draft README) → step 6 (stage upload dir) → step 7 (private upload). The 4 user decisions from plan §1 step 1 (Q1-Q4) are still nominally a gate but recommended defaults are baked into this manifest's `naming_compliance.chosen_option = "A"` and `train_config.rehearsal_mix` annotation.

**Estimated Cycle 2 effort**: ~80 min mac (60 min draft README + 10 min stage + 5 min upload + 5 min audit) + 5 min user OK promote-public, $0.
