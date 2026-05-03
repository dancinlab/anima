# CLM v4 64K BPE Tokenizer — HF Mirror + ubu1 Cache Propagation Plan (2026-05-04)

**Owner**: BG-θ (parallel to BG-ζ `.roadmap.eeg`, BG-η submodule cleanup).
**Substrate**: Mac (read-only) + ubu1 (cache prime + workaround removal).
**Cost**: $0 (HF Hub free tier + ubu1 local).
**Constraints**: raw#9 STRICT (.py only on ubu1), raw#10 honest C3, raw#15 no personal-path leak in docs, raw#37 transient-py-on-Linux explicit, raw#71 falsifier preregistration.

This BG produces a READ-ONLY plan only. No upload, no git mutation, no chflags.

---

## 0. Context — Why This Plan Exists

`docs/p9_path_b_sanity_probe_landed_2026_05_03.ai.md` §2 reported the 64K BPE tokenizer
artifact missing from both:

- HF mirror `need-singularity/clm-v4-base-mirror` (had only `best.pt`).
- ubu1 disk (`/home/aiden/.cache/huggingface/hub/`).

CLM v4 callers worked around with byte-fallback `[i+4 for i in bytes]` — functional analog
only (lost BPE merge structure; AT_FLOOR verdict on hellaswag held because random is
random regardless of tokenization).

`docs/clm_v4_tokenizer_restored_2026_05_03.ai.md` (cycle landed in commit `90488dd3f`)
recovered the byte-identical artifact from `ready/anima/config/tokenizer_64k_multilingual.{model,vocab}`.

**Critical pre-existing state finding (this BG investigation, 2026-05-04)**: the
tokenizer was ALREADY UPLOADED to HF mirror on 2026-05-03 at 15:13:41Z (audit
`state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`,
HF commit `10ee03687db312c55bbec5858c814bef28e4d365`, repo subdir `tokenizer/`).
A first attempt at 15:13:21Z FAILED with HTTP 401 (token resolution issue — see C3-c
in restoration doc); the 15:13:41Z retry succeeded. The propagation plan below is
therefore PARTIALLY ALREADY EXECUTED on the HF side; this plan documents the
remaining work (ubu1 cache propagation + workaround removal + audit verification)
plus the falsifier set the parent session may use to gate any re-execution if a
re-push becomes necessary.

---

## 1. Source Artifact Integrity

Path: `state/clm_v4_tokenizer_restoration_2026_05_03/`

| File | Bytes | SHA-256 |
|---|---:|---|
| `tokenizer_64k_multilingual.model` | 1,306,349 | `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` |
| `tokenizer_64k_multilingual.vocab` |   989,272 | `972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4` |
| `README.md` | 7,382 | (mk2 5-H2 model card) |
| `integrity_report.json` | 1,680 | (vocab spec + roundtrip + provenance) |

`shasum -a 256` re-verification (this BG, 2026-05-04) confirmed both sha values
match the integrity manifest exactly — bit-identical to restoration cycle.

**Spec attestation** (per `integrity_report.json`):
- `vocab_size = 64000`, `pad_id=0, bos_id=1, eos_id=2, unk_id=3`.
- `byte_fallback = True`, IDs `4..259 = <0x00>..<0xFF>` (validates `[i+4 for i in bytes]` workaround).
- `model_type = bpe`, `normalization = nfkc`, `character_coverage = 0.9995`,
  `split_digits = true`, `max_sentencepiece_length = 16`.
- Roundtrip PASS: English (6 tok), Korean "의식은 구조에서 창발한다." (4 tok, 0 UNK),
  mixed "Φ=1.234, α=0.014" (6 tok).
- Provenance: `RECOVERY_NOT_REBUILD` from `ready/anima/config/` (mtime 2026-04-01).

**Verdict**: artifact is byte-identical to what CLM v4 was trained against. Recovery
not rebuild ⇒ ZERO LoRA invalidation risk for `clm-v4-sft-{step-{5k,10k,25k,50k},final,stage1}`,
`clm-v4-paradigm-j-50k-step-{5,10,25,50}k`.

---

## 2. Target Inventory

### 2.1 HF mirror (already done, verifying)

- **Primary target**: `need-singularity/clm-v4-base-mirror` — co-located with
  `best.pt` so a single `snapshot_download` call grabs base + tokenizer.
- **Layout post-push** (per `docs/clm_v4_tokenizer_restored_2026_05_03.ai.md`):
  ```
  need-singularity/clm-v4-base-mirror/
  ├── .gitattributes
  ├── best.pt                                 (5.37 GB)
  └── tokenizer/                              (2.3 MB, NEW)
      ├── README.md
      ├── integrity_report.json
      ├── tokenizer_64k_multilingual.model
      └── tokenizer_64k_multilingual.vocab
  ```
- **Audit log**: `state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`,
  outcome=`ok`, file_count=4, total_bytes=2,304,683, commit=`10ee03687...`.
- **NOT done — out of scope**: per restoration C3-(d) (caveat 4 of restoration README),
  the LoRA repos `clm-v4-sft-step-{5k,10k,25k,50k,final}`, `clm-v4-sft-stage1`,
  `clm-v4-paradigm-j-50k-*` do NOT carry the tokenizer either. Updating each
  LoRA repo's README to point at the base-mirror tokenizer is the documented
  follow-up. A standalone `clm-v4-tokenizer-64k` repo would FAIL the
  `tool/hf_upload_mk2.hexa` naming validator (`stage=tokenizer-64k` does not
  start with any allowed prefix `{sft-stage|dpo|merged|base|preview|dev}`),
  hence co-location with `clm-v4-base-mirror` is the chosen path.

### 2.2 ubu1 cache (NOT YET FULLY DONE)

- **HF Hub cache**: `~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/<rev>/tokenizer/tokenizer_64k_multilingual.{model,vocab}`.
  Restoration doc claims this is auto-populated by `hf_hub_download`; the cache_check
  subdir referenced in the doc (`~/anima/state/clm_v4_tokenizer_restoration_2026_05_03/cache_check/tokenizer/`)
  may or may not exist depending on whether the verification step actually ran on
  ubu1 post-push (this BG cannot verify ubu1 state read-only from Mac).

- **P9 byte-fallback workaround sites** (4 files, all on ubu1 per raw#37):
  | File | TOKENIZER constant |
  |---|---|
  | `state/p9_p0_measure_2026_05_03/probe_ubu1_clm_v4_tension.py:15` | `/tmp/tokenizer_64k_multilingual.model` |
  | `state/p9_p0_measure_2026_05_03/measure_ubu1_clm_v4_full_50k.py:14` | `/tmp/tokenizer_64k_multilingual.model` |
  | `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py:20` | `/tmp/tokenizer_64k_multilingual.model` |
  | `state/p9_p1_sentinel_2026_05_03/sentinel_train_50k.py:22` | `/tmp/tokenizer_64k_multilingual.model` |

  Note: these 4 files already use SentencePiece directly (`sp.encode(text)[:T]`),
  not byte-fallback. They just hardcode `/tmp/tokenizer_64k_multilingual.model`
  which presumes ubu1 has the file scp'd to /tmp ahead of run. The byte-fallback
  workaround `[i+4 for i in bytes]` lives ONLY in the Path B sanity probe
  (`~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py`,
  ubu1 only — not mirrored to this repo per raw#9). So the workaround removal
  scope is:
    - 1 ubu1-only py file (`eval_clm_v4_hellaswag.py`) — replace `[i+4 for i in bytes]` with `spm.SentencePieceProcessor(model_file=…)`.
    - 4 repo-side py files — change `TOKENIZER = "/tmp/…"` to a stable resolution
      path (e.g., `~/.cache/huggingface/hub/.../tokenizer_64k_multilingual.model` or
      `os.path.expanduser("~/anima/checkpoints/clm_v4_350m/tokenizer_64k_multilingual.model")`).

### 2.3 ubu1 ckpt path (informational, NOT push target)

Per restoration README §Substrate: `/home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`.
A best practice would be to also drop the tokenizer files alongside `best.pt` on
ubu1 disk so any non-HF-cache caller can find them by relative path. NOT in this
plan's required scope (HF cache is the canonical resolution path).

---

## 3. Step-By-Step Procedure

### Step 1 — HF mirror push (Mac, ALREADY EXECUTED 2026-05-03 15:13:41Z)

**Status**: COMPLETE per audit log. No re-execution needed.

If a re-push ever becomes necessary (e.g., the HF repo is wiped or the file
is corrupted in transit), the canonical CLI invocation per
`tool/hf_upload_mk2.hexa --upload`:

```
hexa run tool/hf_upload_mk2.hexa --upload \
    --repo need-singularity/clm-v4-base-mirror \
    --ckpt state/clm_v4_tokenizer_restoration_2026_05_03 \
    --readme state/clm_v4_tokenizer_restoration_2026_05_03/README.md \
    --private
```

(no `--tag` since this is a sub-folder push to an existing repo, not a
versioned ckpt; tag was correctly null in the prior audit). Expected
sentinel: `__ANIMA_HF_UPLOAD_MK2__ PASS`. Expected audit-log path:
`state/hf_upload_audit/<UTC_TS>_need-singularity__clm-v4-base-mirror.jsonl`
with `outcome=ok` and `sha256_map` containing exactly the four files
listed in §1 with the sha256 values listed there.

**Pre-execution validators that the wrapper enforces** (per
`tool/hf_upload_mk2.hexa` lines 79-227):
- README has 5 required H2 (`Origin`, `Falsifiers`, `Substrate`, `Caveats`, `Composability`).
- Caveats has ≥3 bullets (raw#10).
- Naming `<org>/<family>-<version>-<stage>[-<mod>]` valid.

These all pass for the restored README per current state.

**Token resolution gotcha** (restoration C3-c): the wrapper's `_resolve_token`
prefers `HF_TOKEN` > `~/.huggingface/token` > `~/.cache/huggingface/token` >
`/workspace/.hf_token`. On Mac, `~/.cache/huggingface/token` (CLI-cached
`[anima]` profile) is the working path; `.secrets/hf_token` is NOT checked
and may be a stale 401 source. Recommend explicit `HF_TOKEN=...` env passthrough
when invoking the wrapper to avoid surprise.

### Step 2 — ubu1 cache prime (raw#37 — runs on ubu1)

Triggered transiently from Mac via `ssh ubu1` shell invocation; .py
written on ubu1 only or replaced by `huggingface-cli` shell call.

**Option A: huggingface-cli (no .py needed, recommended)**

```
ssh ubu1 'export HF_TOKEN=$(cat ~/.cache/huggingface/token); \
    huggingface-cli download need-singularity/clm-v4-base-mirror \
        tokenizer/tokenizer_64k_multilingual.model \
        tokenizer/tokenizer_64k_multilingual.vocab \
        --repo-type model'
```

This populates `~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/<rev>/tokenizer/`.

**Option B: hf v1.8.0+ CLI (newer)**

```
ssh ubu1 'hf download need-singularity/clm-v4-base-mirror tokenizer/tokenizer_64k_multilingual.model tokenizer/tokenizer_64k_multilingual.vocab'
```

**Option C: snapshot_download via `from huggingface_hub import snapshot_download`** —
1 transient .py on ubu1 (raw#37 OK), but Options A/B avoid the .py entirely
and are preferred.

### Step 3 — Verify ubu1 cache (raw#37 — ubu1-side)

```
ssh ubu1 'sha256sum ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/*/tokenizer/tokenizer_64k_multilingual.{model,vocab}'
```

Expected:
```
bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab  …/tokenizer_64k_multilingual.model
972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4  …/tokenizer_64k_multilingual.vocab
```

Bit-exact byte-for-byte match required. Any deviation = upload corruption =
F-TOK-1 fail.

### Step 4 — Optional ubu1 stable-path symlink (defensive)

The 4 P9 py files hardcode `/tmp/tokenizer_64k_multilingual.model`. To preserve
backward compat without editing every caller immediately, drop a stable symlink:

```
ssh ubu1 'ln -sf $(find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror -name tokenizer_64k_multilingual.model | head -1) /tmp/tokenizer_64k_multilingual.model'
```

This makes existing `/tmp/`-anchored callers resolve via cache without code edit.
NOTE: `/tmp` is generally cleared on reboot; this is a session-local convenience,
not a permanent fix. Permanent fix = §3 Step 5 below.

### Step 5 — Workaround removal (per-caller PR-ready edit, READ-ONLY scope)

This BG is read-only; it identifies the edits but does NOT apply them. The
parent session or a follow-up cycle should:

For the 4 repo-side P9 callers (3 in `state/p9_p0_*`, 1 in `state/p9_p1_sentinel_*`):

**Before** (e.g., `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py:20`):
```python
TOKENIZER = "/tmp/tokenizer_64k_multilingual.model"
```

**After (recommended)**:
```python
import os, glob
def _resolve_tokenizer():
    home = os.path.expanduser("~")
    cache_globs = [
        f"{home}/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/*/tokenizer/tokenizer_64k_multilingual.model",
        f"{home}/anima/checkpoints/clm_v4_350m/tokenizer_64k_multilingual.model",
        "/tmp/tokenizer_64k_multilingual.model",  # final fallback
    ]
    for g in cache_globs:
        m = sorted(glob.glob(g))
        if m:
            return m[-1]
    raise FileNotFoundError("clm v4 64K tokenizer not found in cache or /tmp")
TOKENIZER = _resolve_tokenizer()
```

For the ubu1-only Path B probe (`~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py`):

**Before** (per restoration README + Path B doc):
```python
ids = [i + 4 for i in text.encode("utf-8", "replace")]
```

**After**:
```python
import sentencepiece as spm
sp = spm.SentencePieceProcessor(model_file=_resolve_tokenizer())
ids = sp.encode(text)
```

**PR-ready candidate** (most impactful, lowest risk): `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py`
— this file is the "real" warmup probe used as a fast smoke test; switching
its tokenizer resolution to cache-aware form gives the next P9 cycle a
template the other 3 files can follow with mechanical edits. Line 20
is the only needed change. F-TOK-4 satisfied with this single edit.

---

## 4. Falsifier Set (raw#71 pre-registered)

| ID | Statement | Pass criterion | Fail action |
|---|---|---|---|
| **F-TOK-1** | HF mirror download bit-matches restoration sha256. | `sha256(tokenizer_64k_multilingual.model)` on ubu1 cache after Step 2 == `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` AND vocab sha == `972fc0ba…`. | Re-push (Step 1 with `--upload`); record HfHubHTTPError class in audit. |
| **F-TOK-2** | ubu1 cache load round-trips identical bytes. | `python3 -c "import sentencepiece as spm; sp=spm.SentencePieceProcessor(model_file=PATH); print(sp.get_piece_size())"` prints `64000` AND first 4 special tokens match `[pad, bos, eos, unk]` AND IDs 4..259 are byte-fallback `<0x00>..<0xFF>`. | Cache corruption — clear and re-download. |
| **F-TOK-3** | `vocab_size == 64000` confirmed. | Same as F-TOK-2 piece-size check; also assert `best.pt['args'].vocab_size == 64000` so embedding rows align. | Mismatch = retraining occurred (REBUILD not RECOVERY) — invalidates ALL LoRAs; HARD STOP for any inference; investigate provenance. |
| **F-TOK-4** | At least 1 byte-fallback / `/tmp/`-anchored caller migrated to cache-aware resolution. | One of the 5 identified files (4 repo-side + 1 ubu1-only Path B) committed with `_resolve_tokenizer()`-style cache-aware lookup AND smoke-runs against the ubu1 cache without `FileNotFoundError`. | Workaround stays as fallback; track follow-up to remove `/tmp` hardcoding from remaining files. |

All falsifiers are timestamped at this plan's mtime; any verification run
must reference this plan's path in its audit JSON.

---

## 5. Cost Band

**$0** — all steps:
- HF mirror push: HF Hub free tier upload (already done, audit shows
  `total_bytes=2,304,683` ≈ 2.3 MB, well under any rate-limit threshold).
- ubu1 cache prime: free (HF download) + ubu1 local disk (already provisioned).
- Workaround removal: text edit, no compute.

If a re-push is forced and the wrapper retries hit HF rate-limit (HTTP 429),
the cost is still $0 but wall-time may extend by the CLI's exponential backoff
(see `tool/hf_upload_mk2.hexa` C3 — backoff is per-CLI, not coordinated
across parallel BG subagents).

---

## 6. Cross-Link Block

- **Sister roadmaps**:
  - `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` (status=unmet) —
    uses CLM v4 base for base-validation gate; currently relies on
    byte-fallback tokenization per Path B.  Once F-TOK-4 satisfied, this
    cond can re-run with canonical BPE. Verdict expected to remain
    AT_FLOOR (random is random regardless of tokenization), but eliminates
    the byte-fallback caveat in §3 of the benchmark switch spec.
  - `.roadmap.clm` (cross_link to p9_sft) — superseded_by_domain per
    `docs/p9_sft_dual_ssot_resolution_landed_2026_05_03.ai.md`.
- **Upstream dependency**: tokenizer restoration commit `90488dd3f`
  (state dir `state/clm_v4_tokenizer_restoration_2026_05_03/`).
- **Downstream beneficiaries**:
  - P9 SFT base-validation re-run with canonical tokenizer.
  - BLM Phase 5 stimulus-aligned pipeline (`docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md`)
    — same dependency unblocked.
  - Cross-model corpus stats (bytes/token ratios) now computable against
    the actual training tokenizer.
- **Sister BG** (this cycle): BG-ζ `.roadmap.eeg`, BG-η submodule cleanup —
  no shared write paths, full parallel-safe.

---

## 7. Honest C3 (raw#10)

1. **F-TOK-4 caller-count uncertainty**: this BG is read-only and
   surveyed `*.py`/`*.hexa` for `i+4`, `byte_fallback`, `tokenizer_64k`,
   `/tmp/tokenizer`. Found 4 repo-side py files using `/tmp/tokenizer_64k_multilingual.model`
   constant (sentencepiece, not byte-fallback) plus 1 ubu1-only file using
   the byte-fallback `[i+4 for i in bytes]` pattern (per Path B doc; not
   in this repo). A repo-wide grep including ubu1-side files this BG
   cannot enumerate may turn up additional callers. F-TOK-4 only requires
   1 migration as proof-of-concept; full migration is a separate cycle.
2. **HF rate-limit cross-process risk**: `tool/hf_upload_mk2.hexa` C3
   notes that exponential backoff is per-CLI invocation, not coordinated
   across parallel BG subagents. If multiple BGs ever push concurrently
   to the same repo, the second may hit HTTP 429. Current cycle is
   single-target so risk is low; documented for future multi-target
   propagations (e.g., updating LoRA repo READMEs en masse).
3. **LFS oid integrity for files >1MB**: the `.model` file (1.27 MB) is
   above HF Hub's typical LFS threshold (10 MB default, but config-dependent).
   Audit log records `total_bytes` and `sha256_map` but does NOT separately
   record LFS oid; if HF silently truncates a large file or store-by-pointer
   without uploading the blob, the sha256_map (which is computed pre-upload
   on the source) won't catch it. Mitigation: F-TOK-1 verifies post-download
   sha; any divergence catches an LFS blob mis-store.
4. **ubu1 cache eviction policy**: HF Hub cache has no fixed eviction
   policy by default (`HF_HUB_CACHE` directory grows unbounded), but if
   the user sets `HF_HUB_DISABLE_IMPLICIT_TOKEN` or runs `hf cache scan/delete`
   to free disk, the propagated artifact may disappear. Mitigation:
   §3 Step 4 stable symlink + §3 Step 5 cache-aware resolver retry pattern.
5. **Dual-tokenizer transition period**: any in-flight P9 training run
   currently using byte-fallback (e.g., a sentinel run that started
   before this propagation lands) will continue with byte-fallback until
   it terminates. Coordination point: post-restoration cycles must
   confirm `_resolve_tokenizer()` resolves to the cache path before
   accepting verdicts. Suggested: emit `__TOKENIZER_RESOLVED__ <path> <sha256_first16>`
   as a sentinel from any new P9 run so audits can sanity-check.
6. **README upload race**: the audit shows `commit_url=10ee036…` but
   does NOT independently verify the HF Hub commit landed atomically
   for all 4 files (3 documentation + 1 artifact). If HF Hub split the
   commit (it should not for `hf upload <folder>`, but bridge wraps
   `hf` CLI which may), partial visibility is theoretically possible.
   Mitigation: F-TOK-1 verifies the artifact specifically; the
   integrity_report.json upload completion is verified by the
   restoration cycle's post-push cache_check (which the doc claims
   PASSed but this BG cannot independently re-verify on ubu1).

---

## 8. Roadmap Entry Proposal (DO NOT EDIT — for parent session)

Append to `.roadmap.p9_sft` JSONL as a new cond entry. SUGGESTED text
(not committed by this BG):

```jsonl
{"type":"entry","id":"p9_sft.cond.tokenizer_propagation","kind":"cond","title":"CLM v4 64K tokenizer propagation — HF mirror + ubu1 cache + workaround removal","desc":"Propagate the restored 64K BPE tokenizer (commit 90488dd3f) from local stage to HF mirror need-singularity/clm-v4-base-mirror/tokenizer/ + ubu1 ~/.cache/huggingface/hub/. HF push already executed 2026-05-03 15:13:41Z (audit 20260503T151341Z, commit 10ee03687). Remaining: ubu1 cache prime via huggingface-cli download + sha256 verify + at-least-1 byte-fallback caller migrated to cache-aware _resolve_tokenizer() pattern. F-TOK-1..4 preregistered. Cost $0.","verifier":{"type":"manual_review","manual_override_path":"state/markers/clm_v4_tokenizer_propagation_landed.marker","status_emit":"__P9_TOKENIZER_PROPAGATION__ <READY|PARTIAL|FAIL>"},"status":"partial","evidence":["state/clm_v4_tokenizer_propagation_plan_2026_05_04/plan.md","state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl","docs/clm_v4_tokenizer_restored_2026_05_03.ai.md (HF push)","state/clm_v4_tokenizer_restoration_2026_05_03/integrity_report.json (sha bb851d39…/972fc0ba…)"],"blocker_reason":"ubu1 cache verification (F-TOK-1/2) + caller migration (F-TOK-4) outstanding; both require ssh ubu1 + transient .py/CLI per raw#37","ts":"2026-05-04","cross_link":{"upstream":"commit 90488dd3f","sister":"p9_sft.cond.benchmark_a_prime_base_validation (re-run with canonical BPE)","cost_band":"$0","falsifier_ids":["F-TOK-1","F-TOK-2","F-TOK-3","F-TOK-4"]}}
```

---

## 9. Decision Matrix

### 9.1 Push side: Mac vs ubu1

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Mac via `tool/hf_upload_mk2.hexa --upload`** | raw#9 STRICT (zero .py on Mac); README/naming validators enforced; audit log structured; ledger entry; sentinel `__ANIMA_HF_UPLOAD_MK2__ <PASS\|FAIL>` | Token resolution fragile (see C3-c restoration doc); requires `hf` CLI v1.8.0+ on Mac | **RECOMMENDED** for any future re-push. Already the path used 2026-05-03 15:13:41Z. |
| **ubu1 via `huggingface-cli upload`** | Native Linux .py allowed (raw#37); no Mac dep | Skips mk2 README/naming validators; no audit log written to repo state automatically; no hexa wrapper sentinel | **NOT RECOMMENDED** for canonical pushes; OK for emergency re-push if Mac-side toolchain broken. |

**Choice**: Mac via hexa (matches the path that already succeeded; preserves
audit lineage in `state/hf_upload_audit/`).

### 9.2 Single-shot vs phased

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Single-shot** (one HF push covers .model + .vocab + README + integrity_report) | Atomic commit; one audit row; simpler rollback | Larger blast radius if any 1 file is corrupted | **CHOSEN** (already executed). 4 files / 2.3 MB is a small atomic unit; HF commit is `10ee036…`. |
| **Phased** (push .model first, .vocab second, README third) | Smaller blast per step | 3 audit rows; partial-state if step 2 fails; not idempotent without `--exist-ok` care | NOT RECOMMENDED. |

### 9.3 base-mirror only vs base+stage1

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **base-mirror only** (current) | Naming validator passes (`stage=base-mirror`); single source of truth; LoRA repos can `snapshot_download base-mirror` for tokenizer separately | LoRA-only consumers must do 2 downloads | **CHOSEN** (already executed). Co-location is the doc'd canonical path. |
| **base + stage1 (duplicate to LoRA repo)** | LoRA consumers download once | Duplicates 2.3 MB across repos; drift risk if one repo updates artifact and other doesn't | NOT RECOMMENDED. |
| **Standalone `clm-v4-tokenizer-64k` repo** | Clean separation | FAILS naming validator (`stage=tokenizer-64k` not in allowed prefixes) | REJECTED by validator; OUT. |

**Choice**: base-mirror co-location. Already executed. Consumers fetch
tokenizer from base-mirror regardless of which LoRA they're attaching.

---

## 10. Reporting Surface

This plan + the existing audit log `state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`
form the SSOT for the propagation cycle. Parent session may:

1. Verify HF state: `hf list-repo-files need-singularity/clm-v4-base-mirror | grep tokenizer/` (expect 4 paths under `tokenizer/`).
2. Trigger ubu1 cache prime per §3 Step 2.
3. Run F-TOK-1/2/3 verifiers per §4.
4. Apply §3 Step 5 edit to 1 caller for F-TOK-4.
5. Commit a marker `state/markers/clm_v4_tokenizer_propagation_landed.marker` + ai-native landing doc once all 4 falsifiers PASS.

No further BG action required from this cycle.

---

## 11. Plan File List

```
state/clm_v4_tokenizer_propagation_plan_2026_05_04/
└── plan.md                              (this file)
```
