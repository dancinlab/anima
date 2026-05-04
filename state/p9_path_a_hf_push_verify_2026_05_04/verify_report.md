# P9 Path A — HF Push Live Verification (post HF auth refresh)

**Cycle**: `p9_path_a_hf_push_verify_2026_05_04`
**Parent BG**: `p9_path_a_llama_lora_complete_2026_05_04` (BG-ι, COMPLETE_PROBABLE)
**Auth state**: HF token PASS, write scope, `dancinlife` / `need-singularity` admin (post `eea009b40`)
**Mode**: READ-ONLY HF API (no upload, no delete, no rename)

---

## TL;DR

- **HF target identified**: `need-singularity/p9-llama32-lora-stage1` (legacy, training-time push target). Canonical post-rename target `need-singularity/llm-llama32-3b-paradigm-a-prime-sft-stage1` exists as PRIVATE empty stub (sha `5161b80883`); rename never executed.
- **Live state**: 11 files present at last commit `5a9b4584` dated 2026-05-03T20:06:18Z. Adapter weights present: `adapter_model.safetensors` 389MB LFS, oid `f12f31d8…3336`.
- **CRITICAL**: Last HF commit is **"Training in progress, step 8000"**, NOT step 10000 nor `final`. Steps 8001–10000 + final adapter never reached HF. F-PA-HF-1 status emit = **PARTIAL** (step-8000 weights live; step-10000 / `final` lost).
- **Verdict**: `PROBABLE_HF_PARTIAL`. The COMPLETE_PROBABLE → COMPLETE_VERIFIED transition does NOT fire — instead, COMPLETE_PROBABLE → **PARTIAL_VERIFIED_8K** (more honest).
- **F-NAME-1 status emit**: **FAIL** at the live repo (`p9-llama32-lora-stage1` violates mk2 EBNF — no `v<N>`, `p9` not in family allowlist). Canonical stub exists per naming-decision but is unpopulated.
- **F1_v3 readiness flipped**: NO. The 2000 lost steps + missing `final` adapter mean the eval anchor is step-8000 LoRA, not step-10000 as preregistered. Phi-star layer 14 + F1_v3 verdict can still proceed but with a footnote that the eval used the 80%-trained adapter, not the 100%-trained one.

---

## 1. HF target identification

Two candidate repos were resolved from on-disk state:

| repo | role | source |
|---|---|---|
| `need-singularity/p9-llama32-lora-stage1` | actual push_to_hub target during training | `verdict.json:training.push_to_hub` (line 44); `train_llama_lora.py.txt --push-to-hub` arg in `verdict.json:host_terminator.log` |
| `need-singularity/llm-llama32-3b-paradigm-a-prime-sft-stage1` | canonical mk2-compliant rename target | `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md` §"Post-training scheduled actions" |

The naming-decision doc scheduled a post-training `hf repos move` from legacy → canonical. That move was NEVER executed because `verdict_complete.json` records the pod was terminated at step 10000 with TRAIN_DONE.json missing, after which the rename workflow was deferred pending HF auth recovery.

**Verified targets queried**: both. Live state below.

---

## 2. Live HF state — `p9-llama32-lora-stage1` (the populated repo)

### Repo metadata

```
id:           need-singularity/p9-llama32-lora-stage1
private:      true
sha (HEAD):   5a9b458467589b82a69f0108fd2af3e519c45286
lastModified: 2026-05-03T20:06:18.000Z
library_name: transformers
tags:         [transformers, safetensors, generated_from_trainer, sft, trl,
               base_model:meta-llama/Llama-3.2-3B-Instruct, ...]
```

### Commit history (oldest → newest)

| commit | date (UTC) | message |
|---|---|---|
| `0a4b60b6` | 2026-05-03T14:28:51Z | initial commit |
| `f6916247` | 2026-05-03T15:52:19Z | Training in progress, step 2000 |
| `fe83e989` | 2026-05-03T17:16:35Z | Training in progress, step 4000 |
| `f7712e3a` | 2026-05-03T18:41:24Z | Training in progress, step 6000 |
| `5a9b4584` | 2026-05-03T20:06:18Z | **Training in progress, step 8000** ← HEAD |

**Tags / branches**: `tags=[]`, only `main` branch. The mk2 spec C2 caveat (every_save → step-Nk tags) DID NOT MATERIALIZE — TRL/HF Trainer's `every_save` strategy creates new commits, NOT tags. Per-step revisions must be pinned via commit sha.

### File tree (all 11 files at HEAD `5a9b4584`)

| path | type | size | LFS | oid (sha256 for non-LFS) | x-linked-etag (LFS sha256) |
|---|---|---:|---|---|---|
| `.gitattributes` | text | 1570 | no | `52373fe24473b1aa44333d318f578ae6bf04b49b` | — |
| `README.md` | text | 1476 | no | `566b64c19b112ac9f946ccf3475b7cb0a31cee4b` | — |
| `adapter_config.json` | json | 1111 | no | `f86e27159a66b9dabdb9738071d933687dc7245f` | — |
| `adapter_model.safetensors` | bin | 389074464 | **yes** | `7ae32cc24fb493fd950d54a5276ffd1b1e6c2df1` (git oid) | `f12f31d8104900cba5f60ad2010dc0bed0ec5c466e2838c88378fa5c9c2d3336` |
| `chat_template.jinja` | text | 3827 | no | `1bad6a0f648dccdbec523ca79ba90fbcfc806af0` | — |
| `config.json` | json | 727 | no | `74cbee180bd0afb40a31fde375fcde2f535b42ec` | — |
| `tokenizer.json` | json | 17209920 | **yes** | `1c1d8d5c9024994f1d3b00f9662b8dd89ca13cf2` | `6b9e4e7fb171f92fd137b777cc2714bf87d11576700a1dcd7a399e7bbe39537b` |
| `tokenizer_config.json` | json | 354 | no | `a3ccf3ae76b530b318a3d7fdc3d27ab2a0d39531` | — |
| `train.log` | log | 790884 | no | `8d9f631a765383e634a06e1c396e3db41eadcb27` | — |
| `train.pid` | text | 5 | no | `438db35afa0f9f1a25b69d310f434acfd0cdfe15` | — |
| `training_args.bin` | bin | 5368 | **yes** | `2af4f18f6d96f1417471015a9ca30af2bcf28f76` | `0a48289c43a41109c03744096889c5c6c3571e3936a4335dfe1eeb21a40f7389` |

**LFS HEAD probe** (per `reference_hf_gotchas.md`): `x-repo-commit: 5a9b458467589b82a69f0108fd2af3e519c45286` confirms the LFS pointers resolve to the same HEAD as the tree listing.

### adapter_config.json (full content)

```json
{
  "base_model_name_or_path": "meta-llama/Llama-3.2-3B-Instruct",
  "peft_type": "LORA",
  "peft_version": "0.19.1",
  "task_type": "CAUSAL_LM",
  "r": 64,
  "lora_alpha": 64,
  "lora_dropout": 0.05,
  "target_modules": ["q_proj", "down_proj", "k_proj", "gate_proj", "up_proj", "v_proj", "o_proj"],
  "bias": "none",
  "fan_in_fan_out": false,
  "init_lora_weights": true,
  "inference_mode": true,
  "use_dora": false,
  "use_rslora": false
}
```

All hyperparams match `verdict.json:training` exactly: `r=64`, `lora_alpha=64`, `lora_dropout=0.05`, target_modules ⊇ {q,k,v,o,gate,up,down}\_proj, base = Llama-3.2-3B-Instruct. **adapter integrity check: PASS.**

### train.pid

`1291` — matches `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md` Verification log (`root  1291  1  99 14:27 ?  python3 -u /workspace/train_llama_lora.py …`). **pod-side process identity: PASS.**

### train.log tail (last 4KB)

Final visible step in HF-uploaded log: **step 8008** with loss `0.2748`, lr `9.939e-06`, mean_token_acc `0.9348`. The log was uploaded as part of the step-8000 save commit; subsequent in-pod log progression (step 8001–10000) is NOT in the HF mirror copy. Loss trajectory shows healthy convergence: 3.06 (step 10) → 0.27 (step 8000), with `mean_token_accuracy` rising 0.50 → 0.93.

---

## 3. Live HF state — `llm-llama32-3b-paradigm-a-prime-sft-stage1` (the canonical stub)

```
id:           need-singularity/llm-llama32-3b-paradigm-a-prime-sft-stage1
private:      true
sha:          5161b80883bb602df532d13ab2a322211a6ee3af
createdAt:    2026-05-03T15:26:52.000Z
lastModified: 2026-05-03T15:28:12.000Z
siblings:     [.gitattributes, README.md]   ← only 2 files; no adapter
usedStorage:  0
```

This is the pre-created stub from `p9_path_a_naming_decision_2026_05_03`. It has the mk2-conformant README (per `state/p9_path_a_naming_2026_05_03/README_canonical.md`) but ZERO adapter artifacts. The post-training `hf repos move` step (4 of 5 in the naming-decision doc) was never executed.

---

## 4. Local-vs-HF cross-validation

**Local-side manifests checked**:
- `state/p9_path_a_llama_lora_2026_05_03/verdict.json` — pre-training; no checkpoint sha
- `state/p9_path_a_llama_lora_2026_05_03/verdict_complete.json` — post-completion; states `checkpoint_local_path: null` because the pod's error-branch host_pod_terminator scp failed (artifacts/ dir missing) before any sha could be captured
- `state/p9_path_a_llama_lora_2026_05_03/F1_v3_pending.json` — eval-target placeholder; no sha
- `state/hf_upload_audit/` — no Path A audit entries (only base-mirror + sft-stage1-CLM entries from 2026-05-03T15:13Z)

**Conclusion**: NO local sha256 manifest exists for any Path A trained adapter (whether step-2k/4k/6k/8k or 10k/final). The pod-side `final/` directory was never scp'd to Mac before pod termination (host_terminator.log line 46: `scp: open local "/Users/ghost/core/anima/state/p9_path_a_llama_lora_2026_05_03/artifacts/train.log": No such file or directory`).

Cross-validation against HF live is therefore **constructive only via training-config consistency** (adapter_config matches verdict.json hyperparams) and **commit-message progression** (step 2k→4k→6k→8k commits monotonic and 1.4h-spaced, consistent with host_terminator probe cadence). No bytewise sha256 cross-check possible.

**adapter_model.safetensors authoritative sha256** (LFS): `f12f31d8104900cba5f60ad2010dc0bed0ec5c466e2838c88378fa5c9c2d3336` — record this as the canonical anchor for all future eval cycles since no local copy exists.

---

## 5. Naming convention compliance — F-NAME-1

Per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (committed `441ffe732`, swap correction `abfbb182e`):

EBNF: `<org>/<family>-v<N>-<stage>[-<mod>]`
Allowlisted families: `{clm, blm, vlm, slm, tlm, mlm, alm, hexad, composite}`

| repo | family | v<N> | stage | mod | EBNF match | F-NAME-1 |
|---|---|---|---|---|---|---|
| `p9-llama32-lora-stage1` | `p9` (NOT in allowlist) | absent | `stage1` (with `lora` mod-like prefix) | `llama32` (loose) | NO | **FAIL** |
| `llm-llama32-3b-paradigm-a-prime-sft-stage1` | `llm` (NOT in mk2 §3.1 allowlist; new C1 extension per naming-decision) | absent (vendor-base passthrough per C3) | `sft-stage1` | `paradigm-a-prime` (loose) | partial (extension + base-passthrough deviations) | **FAIL_PER_LITERAL** / **PASS_PER_DECISION_DOC** |

**Effective verdict**: F-NAME-1 = **FAIL** at the LIVE populated repo. The canonical stub passes per-decision-doc but holds no artifacts, so eval consumers must read from the FAILing legacy URL until the rename executes. The naming-decision doc explicitly documented this as a deferred action.

---

## 6. Verdict

```
verdict: PROBABLE_HF_PARTIAL
```

**Rationale**:

(a) Adapter weights ARE on HF (this confirms the COMPLETE_PROBABLE training-side claim was correct: training did run, did push to HF, did produce a usable LoRA adapter at step 8000).

(b) But the FINAL adapter (step 10000) is NOT on HF — only step 8000 is. The remaining 2000 steps (~30 minutes of training, observed in host_terminator.log lines 41-44) were lost during the final-save/push race (verdict_complete.json rank-1 cause, p=0.6).

(c) The COMPLETE_PROBABLE → COMPLETE_VERIFIED transition would require step-10000 weights or `final` weights present at HF. Neither exists. **Strict verdict transition: COMPLETE_PROBABLE → PARTIAL_VERIFIED_8K** (more accurate than COMPLETE_VERIFIED).

(d) Path A is salvageable for eval purposes — step-8000 LoRA on a 5-epoch (epoch=5.118 at step 8000) trained adapter, with loss converged to 0.27, is eval-viable. Phi-star and F1_v3 cycles can run.

---

## 7. F1_v3 readiness update (BG-ι unblock check)

BG-ι (`docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md`) listed three `f1_v3_eval_blockers`:

1. ~~HF auth recovery on Mac~~ — UNBLOCKED (verified by this BG: token works, whoami-v2 returns 200, write scope present)
2. `cond.benchmark_a_prime_base_validation = PASS` — separate BG (BG-ν owns `state/p9_base_validation_prep_2026_05_04/`); not this BG's scope
3. `F1_v3_pending.json must be re-emitted with v3 semantics` — local doc edit, deferrable to eval cycle

**Does this BG flip `f1_v3_eval_ready`?** Partially:
- HF auth blocker: CLEARED
- Adapter availability: PARTIAL (step-8000, not step-10000) → eval-viable but with footnote
- Base-validation blocker: still owned by BG-ν

**Net flip**: `f1_v3_eval_ready` goes from `false` → `false_with_caveat` (blockers reduced from 3 to 1.5). Strict boolean flip = **NO**. The eval cycle can be PRE-AUTHORIZED conditional on BG-ν completing base-validation, with the explicit caveat that the eval anchor is step-8000 LoRA not step-10000.

---

## 8. Honest C3 (raw#10)

1. **Step-10k vs step-8k anchor drift**: Verdict_complete.json claimed COMPLETE_PROBABLE based on host_terminator.log STEP=10000/10000 marker. HF mirror reveals only step-8000 was committed. The pod-side `step 10000` ckpt + `final/` directory either (a) never wrote to disk before crash, (b) wrote but failed to push (HF push timeout/401), or (c) wrote and pushed but in a transaction that never finalized. Cannot disambiguate from HF state alone — pod is terminated and unreachable. Eval consumers MUST treat step-8000 as the anchor.

2. **HF Trainer `every_save` does NOT create git tags**: `refs` API returns `tags: []` despite 4 step-Nk save events. Mk2 spec C2 caveat predicted potential tag loss on `hf repos move`; reality is tags were never created at all. The TRL/Trainer documentation suggests `hub_strategy=every_save` makes commits with messages containing the step, but no tags. This means per-step revision pinning requires commit sha (e.g., `5a9b458467` for step-8000), not a `step-8k` tag. The naming-decision doc Step §4 line 73 (`hf models info … | jq .siblings`) cannot recover tags that never existed.

3. **adapter_model.safetensors HEAD returns x-linked-etag (sha256), not git oid**: The git tree API returns `oid=7ae32cc24fb493fd950d54a5276ffd1b1e6c2df1` (40-char hex = git blob oid, not sha256). The actual sha256 of the LFS payload is `f12f31d8104900cba5f60ad2010dc0bed0ec5c466e2838c88378fa5c9c2d3336` from the HEAD `x-linked-etag` header. Same applies to tokenizer.json and training_args.bin. Eval-cycle integrity manifests should record `x-linked-etag` (true sha256), not the tree-API oid (git pointer hash).

4. **No local sha256 manifest exists for any Path A adapter**: cross-validation in §4 is configuration-consistency only, not bytewise. If the HF mirror were corrupted post-upload (HF-side bug or admin action), this verification would NOT detect it. Mitigation: download adapter_model.safetensors locally and verify its sha256 = `f12f31d8…3336` before any irreversible eval commitment. (Out of scope for this BG since it would consume bandwidth + 389MB local storage.)

5. **Naming-decision rename was scheduled to run from a separate post-training BG that never fired**: per `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md` §"Post-training scheduled actions", a 5-step `hf repos delete` + `hf repos move` sequence was specified. None of those steps appear in any subsequent landing doc or roadmap status emit. The repo continues to live at the FAILing legacy URL. This BG explicitly does NOT execute the rename (read-only constraint), but flags it as the next required action.

6. **Repo README is auto-generated TRL boilerplate, not mk2-compliant**: HF mirror's `README.md` (1476 bytes, oid `566b64c1`) is the TRL/Transformers default ("This model is a fine-tuned version of meta-llama/Llama-3.2-3B-Instruct"). It lacks the 5 required H2 sections (Origin / Falsifiers / Substrate / Caveats / Composability) per mk2 spec §5. The mk2-compliant README staged at `state/p9_path_a_naming_2026_05_03/README_canonical.md` was uploaded to the canonical stub repo, NOT to this populated legacy repo. Until rename + README upload, F-NAME-1 + mk2 §5 compliance both FAIL on the live evaluable repo.

---

## 9. Roadmap update proposal

For `.roadmap.p9_sft` (DO NOT edit — proposal only, parent serializes commits):

```jsonl
{"id":"p9_sft.cond.path_a_lora_train_complete","status":"COMPLETE_PROBABLE → PARTIAL_VERIFIED_8K","ts":"2026-05-04T<now>Z","cycle_ref":"p9_path_a_hf_push_verify_2026_05_04","reason":"HF live-verified step-8000 commit `5a9b4584` with adapter_model.safetensors sha256 f12f31d8…3336; step-10000 + final adapter NOT on HF mirror (not pushed before pod termination); eval anchor must be step-8000 not step-10000"}
{"id":"p9_sft.cond.path_a_hf_naming_rename","status":"DEFERRED → PENDING","ts":"2026-05-04T<now>Z","reason":"hf repos move from p9-llama32-lora-stage1 → llm-llama32-3b-paradigm-a-prime-sft-stage1 still required per naming-decision doc §Post-training scheduled actions; HF auth now PASS so action is unblocked"}
{"id":"p9_sft.cond.f1_v3_eval_ready","status":"false → false_with_caveat","ts":"2026-05-04T<now>Z","reason":"HF auth blocker CLEARED; adapter blocker PARTIAL (step-8k available, step-10k missing); base-validation blocker remains under BG-ν"}
```

The first item explicitly REJECTS the proposed `COMPLETE_PROBABLE → COMPLETE_VERIFIED` transition. Step-8000 is materially different from step-10000 (2000 steps + 30min of training + epoch 5.12 vs ~6.4 not present in HF state), so a CONFIRMED transition would mis-state reality.

---

## 10. Constraint compliance log

- raw#9: pure curl + python3 -c json parsing only; no .py written; hexa not invoked (no eligible hexa for this read-only HF API audit)
- raw#10: 6 honest C3 caveats above
- raw#15: all paths repo-relative or `~/.cache/huggingface/` (HF tooling default)
- raw#37: ubu1 not used; HF API directly callable from Mac
- raw#71: read-only HF API; no upload, no delete, no rename, no chflags
- git ops in this cycle: NONE
- HF mutations in this cycle: NONE
- Files written this cycle:
  - `state/p9_path_a_hf_push_verify_2026_05_04/verify_report.md` (this file)
  - `state/p9_path_a_hf_push_verify_2026_05_04/verdict.json`

---

**End of report.**
