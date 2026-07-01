# KOSMOS HF Upload — REVIEW PLAN (PREP ONLY, NOTHING UPLOADED)

- date: 2026-06-02
- status: **PREP-ONLY** — manifests + dataset cards + sha256 checksums built locally.
  **NOTHING was uploaded. NO HF collection / repo / collection-item was created or modified.**
- branch: `lane-g/d768-cuda-fire`
- naming spec: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`
- format SSOT (pointer-only, a_kosmos): [github.com/dancinlab/kosmos](https://github.com/dancinlab/kosmos)
- visibility policy: a_hf_autonomous — PUBLIC = closure-PASS / verified / clean-license;
  PRIVATE = WIP / negative / unclear-license. **Conservative: any unclear → PRIVATE.**

> ⚠️ The user is sensitive about HF uploads/collection additions. Do NOT run any
> upload/create/collection-add command until the user gives an explicit **"go"**.

---

## Candidate inventory

| # | repo_id | source dir | files | size | visibility | sha-manifest |
|---|---|---|---:|---:|---|---|
| 1 | `dancinlab/kosmos-anchor-knuth31-carving` | `HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/` | 31 | 124K | **PUBLIC** | `kosmos-anchor-knuth31-carving/SHA256SUMS.txt` |
| 2 | `dancinlab/kosmos-anchor-v3emit-grid3b` | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/{vP21H_alpha,vP21H_gamma}/kosmos_anchors/` | 28 | 112K | **PRIVATE** | `kosmos-anchor-v3emit-grid3b/SHA256SUMS.txt` |
| 3 | `dancinlab/kosmos-anchor-legacy-curation11` | `HEXAD/UNIVERSE-BRAIN-MAP/anchors/*.kosmos` | 11 | 44K | **PRIVATE** | `kosmos-anchor-legacy-curation11/SHA256SUMS.txt` |
| 4 | `dancinlab/kosmos-corpus-clm-p1` | `CLM/corpus/` (manifest + `sample/`) | 4 | 16K | **PRIVATE** | `kosmos-corpus-clm-p1/SHA256SUMS.txt` |

---

## PUBLIC / PRIVATE rationale (a_hf_autonomous)

### 1. kosmos-anchor-knuth31-carving → **PUBLIC**
- closure: E-31 LANDED 2026-05-31; parser validation **31/31 valid**
  (`kosmos_load` + `kosmos_anchor_valid`). closed_anchor present.
- license: anima-authored anchor text, no external corpus embedded → CC-BY-SA-4.0 clean.
- verdict: closure-PASS + verified + clean-license = PUBLIC.

### 2. kosmos-anchor-v3emit-grid3b → **PRIVATE**
- closure: V3 substrate = **CLOSED-FAIL** (`HEXAD/KOSMOS.md` E-MM: "V3 substrate 만 FAIL").
  Emission text degenerate ("the 1955 , 1955 , 1955 ..."). Negative-result regime.
- license: derived from grid_3b multilingual fire; corpus license not asserted clean for this set.
- verdict: negative-result + unclear-license = PRIVATE.

### 3. kosmos-anchor-legacy-curation11 → **PRIVATE**
- closure: the e7_31 31-anchor set is the canonical E7 ground-truth
  (`HEXAD/KOSMOS.md` E-31: "e7_31/ = E7 canonical set"). This 11-anchor set is a
  pre-E7 curation kept for provenance; it carries no closure verdict of its own.
- license: anima-authored (clean); WIP provenance/history artifact.
- verdict: WIP provenance set = PRIVATE (conservative).

### 4. kosmos-corpus-clm-p1 → **PRIVATE**
- closure: sample-only build (16 records, 1656 B); merkle root = all-zero placeholder.
- license: **MIXED** — `web` lane CC-BY-SA-4.0 (clean) but `register` lane scratch (unasserted).
- verdict: unclear-license lane + sample-only = PRIVATE (conservative).

---

## Read-only HF collection cross-check (NO writes)

Read-only HF public API, performed 2026-06-02:
- `GET /api/datasets?author=dancinlab` → only **1** dataset exists: `dancinlab/clm-backbone-5lang-sample`
  (license odc-by, CLM backbone sample — NOT a kosmos dataset, distinct).
- `GET /api/datasets?author=dancinlab&search=kosmos` → **0** results.
- `GET /api/models?author=dancinlab&search=kosmos` → **0** results.
- `HF.jsonl` (local registry) → **0** kosmos rows (28 rows total, none kosmos).

**Conclusion: all 4 candidates are NEW. None already uploaded. No duplicate-add risk.**
(Note: a future `go` must re-verify, since the public API hides PRIVATE repos —
re-list with an authed token before upload to rule out a pre-existing private repo.)

---

## Intended HF.jsonl rows (a_hf_registry) — DO NOT ADD NOW

These rows would be appended to `/HF.jsonl` ONLY AFTER a successful upload
(status flips pending_upload → uploaded once sha256 confirmed). Recorded here, not added:

```jsonl
{"run":"kosmos-knuth31-carving","local_path":"HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/","hf_repo_id":"dancinlab/kosmos-anchor-knuth31-carving","base_model":null,"lineage":"E-31 §UBM-E7","size":"124K","status":"pending_upload","visibility":"public","sha_manifest":"state/hf_kosmos_prep/kosmos-anchor-knuth31-carving/SHA256SUMS.txt"}
{"run":"kosmos-v3emit-grid3b","local_path":"HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/","hf_repo_id":"dancinlab/kosmos-anchor-v3emit-grid3b","base_model":null,"lineage":"grid_3b s187 V3-emit (CLOSED-FAIL)","size":"112K","status":"pending_upload","visibility":"private","sha_manifest":"state/hf_kosmos_prep/kosmos-anchor-v3emit-grid3b/SHA256SUMS.txt"}
{"run":"kosmos-legacy-curation11","local_path":"HEXAD/UNIVERSE-BRAIN-MAP/anchors/","hf_repo_id":"dancinlab/kosmos-anchor-legacy-curation11","base_model":null,"lineage":"pre-E7 legacy curation (superseded)","size":"44K","status":"pending_upload","visibility":"private","sha_manifest":"state/hf_kosmos_prep/kosmos-anchor-legacy-curation11/SHA256SUMS.txt"}
{"run":"kosmos-corpus-clm-p1","local_path":"CLM/corpus/","hf_repo_id":"dancinlab/kosmos-corpus-clm-p1","base_model":null,"lineage":"CLM P1 byte-corpus sample build","size":"16K","status":"pending_upload","visibility":"private","sha_manifest":"state/hf_kosmos_prep/kosmos-corpus-clm-p1/SHA256SUMS.txt"}
```

---

## Exact upload commands that WOULD run on "go" (DO NOT RUN NOW)

Each command uploads the README.md (dataset card) + the source `.kosmos` files +
the SHA256SUMS.txt manifest to a dataset repo. `--private` set per visibility.
**These are recorded for review only. None has been executed.**

```bash
# 1. PUBLIC — knuth31 carving (closure-PASS, clean-license)
huggingface-cli upload dancinlab/kosmos-anchor-knuth31-carving \
  HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/ . --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-anchor-knuth31-carving \
  state/hf_kosmos_prep/kosmos-anchor-knuth31-carving/README.md README.md --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-anchor-knuth31-carving \
  state/hf_kosmos_prep/kosmos-anchor-knuth31-carving/SHA256SUMS.txt SHA256SUMS.txt --repo-type=dataset

# 2. PRIVATE — v3emit grid3b (negative-result)
huggingface-cli repo create dancinlab/kosmos-anchor-v3emit-grid3b --repo-type=dataset --private -y
huggingface-cli upload dancinlab/kosmos-anchor-v3emit-grid3b \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_alpha/kosmos_anchors/ vP21H_alpha/ --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-anchor-v3emit-grid3b \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_gamma/kosmos_anchors/ vP21H_gamma/ --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-anchor-v3emit-grid3b \
  state/hf_kosmos_prep/kosmos-anchor-v3emit-grid3b/README.md README.md --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-anchor-v3emit-grid3b \
  state/hf_kosmos_prep/kosmos-anchor-v3emit-grid3b/SHA256SUMS.txt SHA256SUMS.txt --repo-type=dataset

# 3. PRIVATE — legacy curation 11 (superseded)
huggingface-cli repo create dancinlab/kosmos-anchor-legacy-curation11 --repo-type=dataset --private -y
# (upload the 11 root anchors/*.kosmos EXCLUDING the e7_31/ subdir — use an allow-pattern or a staged copy)
huggingface-cli upload dancinlab/kosmos-anchor-legacy-curation11 \
  state/hf_kosmos_prep/kosmos-anchor-legacy-curation11/README.md README.md --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-anchor-legacy-curation11 \
  state/hf_kosmos_prep/kosmos-anchor-legacy-curation11/SHA256SUMS.txt SHA256SUMS.txt --repo-type=dataset
#   + the 11 anchors/*.kosmos (root only, not e7_31/) — stage them first to avoid pushing e7_31.

# 4. PRIVATE — CLM P1 corpus sample (mixed-license)
huggingface-cli repo create dancinlab/kosmos-corpus-clm-p1 --repo-type=dataset --private -y
huggingface-cli upload dancinlab/kosmos-corpus-clm-p1 \
  CLM/corpus/clm_p1.corpus.kosmos clm_p1.corpus.kosmos --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-corpus-clm-p1 \
  CLM/corpus/sample/ sample/ --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-corpus-clm-p1 \
  state/hf_kosmos_prep/kosmos-corpus-clm-p1/README.md README.md --repo-type=dataset
huggingface-cli upload dancinlab/kosmos-corpus-clm-p1 \
  state/hf_kosmos_prep/kosmos-corpus-clm-p1/SHA256SUMS.txt SHA256SUMS.txt --repo-type=dataset
```

> Preferred path on go: the project wrapper `tool/hf_upload_mk2.hexa`
> (a_hf_registry: "upload via tool/hf_upload_mk2.hexa · ledger state/hf_upload_audit/").
> The raw `huggingface-cli` lines above are the explicit fallback equivalent.

### Post-upload steps a real "go" must also do
1. Append the 4 HF.jsonl rows (flip status → uploaded after sha256 confirmed).
2. Re-list with an AUTHED token first (public API hides private repos) to rule out a pre-existing repo.
3. Attach model/dataset card + manifest (a_hf_complete totality).
4. Collection add (if any) is a SEPARATE explicit user decision — NOT bundled into upload.

---

## Notes
- a_kosmos: spec is NOT duplicated here; cards point to github.com/dancinlab/kosmos.
- a_lane_akida_gpu_split: candidate #2 is Lane G (GPU) only; no AKIDA (Lane A)
  provenance is mixed into any card.
- Datasets are NOT covered by the §2 EBNF (model-name grammar); kosmos dataset
  names use the `dancinlab/` org + descriptive `kosmos-<kind>-<slug>` form and
  the §5 README 5-section template (adapted for datasets).
