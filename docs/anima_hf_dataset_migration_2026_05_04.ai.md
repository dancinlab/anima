---
schema: anima/docs/hf_dataset_migration/ai-native/1
last_updated: 2026-05-04
ssot:
  hf_dataset_repo: need-singularity/anima-sft-data
  hf_url: https://huggingface.co/datasets/need-singularity/anima-sft-data
  initial_commit: c76663148e97a243b6d2d2e1db75d40dc6dc9380
  initial_file: sft_data_llama_template.jsonl
  initial_size_bytes: 71918520
  initial_sha256: f257d7b342f2d675412396dd3f530b7f7ee79b263696de37686becb03a7dbb75
  privacy: private (org-only)
trigger:
  github_lfs_warning: "File state/p9_path_a_r16_2026_05_03/sft_data_llama_template.jsonl is 68.59 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB"
  source_commit: 346e8503 (anima main)
status: LANDED (HF upload + anima git removal + gitignore)
policy:
  destructive_ops: 1 (git rm --cached for sft_data_llama_template.jsonl)
  hf_resource_only: enforced (HF as canonical large-data SSOT)
omega_cycle: 4-step (audit -> upload -> verify -> migrate)
---

# anima HF dataset migration — sft_data_llama_template.jsonl (2026-05-04)

> **TL;DR**
>
> 68.59 MB `sft_data_llama_template.jsonl` migrated from anima git tree → `huggingface.co/datasets/need-singularity/anima-sft-data`. anima git now references via path constant; gitignore prevents re-commit. sha256 verified post-upload (f257d7b3...).

## §1 Problem

GitHub LFS warning emitted on commit `346e8503` (anima main, 2026-05-04):
```
remote: warning: File state/p9_path_a_r16_2026_05_03/sft_data_llama_template.jsonl
is 68.59 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB
```

GitHub limits:
- 50 MB → warning
- 100 MB → hard cap (push rejected)

68.59 MB SFT training data file = git tree bloat + clone slowdown + future cap risk.

## §2 Solution: HF dataset migration

| Layer | Before | After |
|---|---|---|
| anima git | tracks 71.9 MB jsonl (clone bottleneck) | references HF dataset path only |
| HF | none | `need-singularity/anima-sft-data` private dataset |
| Access | `git clone` (slow) | `hf download need-singularity/anima-sft-data` (LFS auto) |

## §3 Migration steps (executed 2026-05-04)

1. **Auth**: `HF_TOKEN=$(secret get huggingface.token --raw)` (token via secret CLI; user `dancinlife` / org `need-singularity` confirmed)
2. **File audit**: `shasum -a 256 sft_data_llama_template.jsonl` → `f257d7b3...` (71918520 bytes)
3. **Repo create**: `hf repos create need-singularity/anima-sft-data --type dataset --private`
4. **Upload**: `hf upload need-singularity/anima-sft-data <local-path> sft_data_llama_template.jsonl --repo-type dataset`
   - Commit: `c76663148e97a243b6d2d2e1db75d40dc6dc9380`
   - Throughput: 7.82 MB/s
5. **Verify**: `hf download need-singularity/anima-sft-data sft_data_llama_template.jsonl --local-dir /tmp/hf_verify` → sha256 match (`f257d7b3...`)
6. **Migrate**: `git rm --cached state/p9_path_a_r16_2026_05_03/sft_data_llama_template.jsonl`
7. **Gitignore**: pattern `state/p9_path_a_*/sft_data_*.jsonl` added to `.gitignore`
8. **Doc**: this handoff doc

## §4 Access pattern (forward usage)

### Download in code:
```python
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id="need-singularity/anima-sft-data",
    filename="sft_data_llama_template.jsonl",
    repo_type="dataset",
)
```

### Download via CLI:
```bash
HF_TOKEN=$(secret get huggingface.token --raw) hf download \
    need-singularity/anima-sft-data sft_data_llama_template.jsonl \
    --repo-type dataset \
    --local-dir state/p9_path_a_r16_2026_05_03/
```

### Reference in tooling:
```yaml
# anima/config/datasets.yaml (if/when emitted)
sft_data_llama_template:
  hf_repo: need-singularity/anima-sft-data
  filename: sft_data_llama_template.jsonl
  sha256: f257d7b342f2d675412396dd3f530b7f7ee79b263696de37686becb03a7dbb75
  size_bytes: 71918520
```

## §5 Future migrations (deferred)

Files in anima git tree that may benefit from HF migration when they grow:
- `state/p9_base_validation_h100_2026_05_04/clm_v4_hf/tokenizer_64k_multilingual.{model,vocab}` (tokenizer artifacts)
- `state/p9_a_prime_main_eval_2026_05_03_lora_results/step_*_*.json` (eval result jsons; small individually but accumulating)
- `state/vlm_stage1_2026_05_04/*.json` (vlm stage 1 artifacts)

Trigger threshold: file size >50 MB OR cumulative state dir >500 MB.

## §6 raw#10 honest caveats

1. Private dataset — requires `HF_TOKEN` for download. Public alternative possible if data not sensitive (consciousness training data may be — keep private).
2. HF free tier sufficient for current workload. Future scaling may require Pro plan ($9/mo) if >many private repos.
3. `git rm --cached` removes from index but file still exists locally (safe; user can delete locally if disk pressure).
4. Forward references in code (e.g. tools that load from `state/p9_path_a_r16_2026_05_03/sft_data_llama_template.jsonl` directly) MAY break — search and replace with HF download pattern in follow-up cycle.
5. No automatic re-upload on local file change — manual `hf upload` cycle if data updates.

## §7 File index

| Path | Role |
|---|---|
| `https://huggingface.co/datasets/need-singularity/anima-sft-data` | HF dataset SSOT (canonical) |
| `state/p9_path_a_r16_2026_05_03/sft_data_llama_template.jsonl` | local cache (gitignored; download on demand) |
| `.gitignore` | extended with `state/p9_path_a_*/sft_data_*.jsonl` pattern |
| `docs/anima_hf_dataset_migration_2026_05_04.ai.md` | this handoff doc |

End of doc.
