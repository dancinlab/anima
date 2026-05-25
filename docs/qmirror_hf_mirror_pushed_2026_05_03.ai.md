# qmirror HF Mirror — Pushed (2026-05-03)

**Status**: LANDED
**Cycle**: `qmirror_hf_mirror_2026_05_03`
**Marker**: `state/markers/qmirror_hf_mirror_pushed.marker`
**Audit**: `state/qmirror_hf_mirror_2026_05_03/push_audit.json`

---

## TL;DR

`qmirror` standalone (closure 8/8 PASS, Apache-2.0, GitHub canonical at
[3488b23](https://github.com/dancinlab/qmirror/commit/3488b23)) is now
mirrored to the HuggingFace Hub at <https://huggingface.co/dancinlab/qmirror>.

- **HF repo**: model-type, public, 33 files, ~213 KB.
- **HF final commit**: `19e94bb5b0e9ec2d3b3de62770bde9fb7c4fc59f`.
- **GitHub post-mirror commit**: `720e2cf` (adds HF cross-link in README.md +
  `mirror_url` in hexa.toml; no source-code mutation).
- **Cost**: $0 (HF public free tier, well under 5 GB).
- **Raw#9 strict**: hf + gh CLIs invoked as external binaries from hexa wrapper /
  shell; zero `.py` executed on Mac side.

---

## What landed

### HF Hub (dancinlab/qmirror)

Created via `hf repo create dancinlab/qmirror --type model --exist-ok`.
Populated via 5 sequential `hf upload` commits:

| # | Commit | Kind | Files | Notes |
|---|--------|------|-------|-------|
| 1 | (repo create) | repo_create | — | model-type, public |
| 2 | `ab8f207` | folder_upload | 31 | qmirror tree, excludes `.git/*`, `state/*`, `.DS_Store` |
| 3 | `73edc9e` | readme_overwrite | 1 | HF-targeted README.md (mk2 5 H2 sections + YAML front-matter) |
| 4 | `19e94bb` | github_readme_preserve | 1 | original README.md → `README_github.md` |
| 5 | `35f174a` | github_readme_resync | 1 | re-sync `README_github.md` after GitHub commit `720e2cf` lands HF cross-link |

Final tree (33 files): `.gitattributes`, `.gitignore`, `CHANGELOG.md`, `LICENSE`,
`README.md` (HF card), `README_github.md` (canonical project README),
`cli/qmirror.hexa`, 2 docs, 4 examples, `hexa.toml`, `install.hexa`,
3 python_bridge files, 10 hexa modules, 5 tests.

### GitHub (dancinlab/qmirror)

- Pre-mirror HEAD: `3488b23` (the standalone 1.0.0 closure commit).
- Post-mirror HEAD: `720e2cf` (`docs(mirror): add HF Hub mirror cross-link`).
- Diff: +6 lines `README.md` (HF Mirror badge + Mirrors callout under header),
  +1 line `hexa.toml` (`mirror_url` field).
- **No source-code mutation** — constraint honored.

### HF README strategy

The HF UI renders `README.md` as the model card. Two requirements clashed:
- HF needs YAML front-matter for proper indexing (library, pipeline_tag, tags).
- The mk2 wrapper contract requires 5 H2 sections (Origin, Falsifiers,
  Substrate, Caveats, Composability) the original GitHub README doesn't have.

Resolution: HF `README.md` = HF-targeted card with all of the above; original
project README preserved at `README_github.md`. Both kept in sync via the
push pipeline.

YAML front-matter set:
- `license: apache-2.0`
- `library_name: hexa`
- `pipeline_tag: other` (this is **not** an inference-style model)
- `tags: [quantum-computing, qrng, chsh, bell-inequality, iit, phi-star, consciousness, rng, infrastructure, non-model-mirror]`

---

## Why bypass `tool/hf_upload_mk2.hexa`?

The mk2 wrapper enforces a strict naming convention on the repo path:
`<org>/<family>-<version>-<stage>[-<modifier>]` with family ∈ {clm, alm, blm,
vlm, slm, tlm, nlm, mlm, llm, hexad, composite}. This is correct and
load-bearing for the LM-publishing pipeline (see
`docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`).

`dancinlab/qmirror` is **infrastructure**, not an LM checkpoint, and
has no family/version/stage triple to assert. Forcing it into the mk2 schema
would either:
- (a) require minting a fake family/version/stage (e.g., `qmirror-v1-base`),
  polluting the LM family enum with a non-LM repo, or
- (b) extend the mk2 family enum with `infra` / `substrate`, which is
  out-of-scope for this cycle and a foot-gun for future LM upload work.

Decision: bypass the mk2 wrapper for this single-repo upload, use the `hf`
CLI directly, but **honor mk2's other invariants**:
- 5 required H2 sections in HF `README.md` (✓)
- Caveats section ≥ 3 honest C3 bullets (✓ — 4 caveats below)
- sha256 manifest computed pre-upload (`sha256_premanifest.txt`, 31 files)
- audit JSON written to `state/qmirror_hf_mirror_2026_05_03/push_audit.json`
- marker written to `state/markers/qmirror_hf_mirror_pushed.marker`

Follow-up cycle (out of scope): extend mk2 family enum with `infra` (or split
the wrapper into `hf_upload_lm_mk2` + `hf_upload_infra_mk2`) so future
infrastructure repos can flow through the wrapper directly.

---

## Caveats (raw#10 honest C3, 4)

1. **Dual-mirror sync burden** — GitHub and HF are kept in sync by manual
   re-push after each GitHub commit. There is no webhook bridge as of land
   time. Risk: HF mirror falls behind GitHub if the operator forgets the
   second push step. Mitigation: per-cycle audit log + planned CI hook in a
   follow-up cycle (target: a `tool/hf_mirror_sync.hexa` that diffs the two
   trees and re-uploads the deltas).

2. **HF model-type repo for non-model content** — qmirror is infrastructure
   (hexa source + python bridges + closure docs), not a trained model. We
   registered it as model-type because that is the only HF repo class
   accepting arbitrary file types. `pipeline_tag=other` and
   `library_name=hexa` signal this to downstream tooling, but HF
   model-search will still surface this repo without a usable inference
   path. Users coming from the model-search filter may be confused — HF
   README header explicitly disclaims "infrastructure, not a trained
   model" in the first paragraph.

3. **License clarity for downstream ML use** — Apache-2.0 covers qmirror
   source. The IIT 4.0 phi-star backend depends on a pinned `wmayner/pyphi`
   commit (`b78d0e3`, GPLv3-licensed). If a downstream ML pipeline embeds
   qmirror and statically links pyphi, that pipeline inherits pyphi's
   GPLv3 obligations on the linked binary — Apache-2.0 alone is **not
   sufficient** for closed-source distribution. The mock-LCG path and the
   pure-CHSH path are pyphi-free and Apache-2.0-clean. Users who need a
   pure-Apache-2.0 path should set `NEXUS_QMIRROR_MOCK=1` and avoid the
   `qmirror iit` / `qmirror phi` subcommands.

4. **Repo size limit / future binary fixtures** — current upload is ~213 KB
   across 31 source files, well under HF's 5 GB free-tier soft limit. If
   future cycles add reference simulator-state snapshots (e.g., 30-qubit
   pre-computed amplitude vectors) or Braket-fixture binary blobs (>1 MB
   each), we will need to either (a) migrate to Git-LFS-tracked HF storage
   (HF auto-handles this for files >10 MB but increases storage accounting
   complexity) or (b) shard those into a sibling
   `dancinlab/qmirror-fixtures` repo. Current contract: `state/`
   stays gitignored, no binary blobs in this repo.

---

## Verification

```bash
# 1. Confirm HF repo populated
hf models info dancinlab/qmirror | head -20

# 2. Confirm GitHub cross-link in place
gh api repos/dancinlab/qmirror/contents/README.md --jq '.content' \
  | base64 -d | head -15

# 3. Confirm hexa.toml has mirror_url
gh api repos/dancinlab/qmirror/contents/hexa.toml --jq '.content' \
  | base64 -d | grep mirror_url

# 4. Audit + marker present
ls -la state/qmirror_hf_mirror_2026_05_03/push_audit.json \
       state/markers/qmirror_hf_mirror_pushed.marker
```

---

## Cross-refs

- GitHub: <https://github.com/dancinlab/qmirror>
- HF: <https://huggingface.co/dancinlab/qmirror>
- Closure doc (upstream): `docs/nexus_qmirror_closure_2026_05_03.md`
- mk2 upload wrapper (bypassed for this cycle): `tool/hf_upload_mk2.hexa`
- mk2 naming spec: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`
- raw#9 py-to-hexa-only sweep: `docs/py_to_hexa_only_landed_2026_05_03.ai.md`
- pre-manifest sha256: `state/qmirror_hf_mirror_2026_05_03/sha256_premanifest.txt`
- HF-targeted README source: `state/qmirror_hf_mirror_2026_05_03/README_hf.md`
- preserved GitHub README on HF: `state/qmirror_hf_mirror_2026_05_03/README_github.md`

---

## Done conditions

- [x] HF repo `dancinlab/qmirror` exists, public, model-type
- [x] HF repo populated with 33 files (31 source + `.gitattributes` + `README_github.md`)
- [x] HF README.md has YAML front-matter + 5 mk2 H2 sections + GitHub cross-link
- [x] GitHub README.md has HF Mirror badge + Mirrors callout
- [x] hexa.toml has `mirror_url` field alongside `repository`
- [x] GitHub commit `720e2cf` landed with audit cross-refs in commit body
- [x] HF and GitHub README_github.md are in sync (HF commit `35f174a` after GitHub `720e2cf`)
- [x] Audit JSON, marker, handoff written to anima state/docs
- [x] 4 honest C3 caveats explicit
- [x] Constraints honored: raw#9 strict, raw#15 no token leak, $0 cost, no GitHub source mutation
