# anima HF Promote Watchdog Audit — landed 2026-05-05

**Audit ID**: BG-E-HF-PROMOTE-WATCHDOG-2026-05-05
**Audit UTC**: 2026-05-05T13:00:00Z
**Now UTC at audit start**: 2026-05-05T12:48:43Z
**Scope**: 36-40h dwell-time validation of HF clm-v4-mk2-v1 + Pβ PUBLIC promote auto-fire infrastructure
**raw**: 9 (md+bash carve-out OK), 10 (honest C3 inline), 15 (no promote-script mutation)
**own**: 15 (HF release lifecycle PRIVATE→PUBLIC after verification)

---

## TL;DR

| Sub-task | Result |
| --- | --- |
| Sub-1 — `--check-only` dry-run | **PASS** (GATE 1 fails correctly: pre-window) |
| Sub-2 — HF state pre-check | **PASS** (clm 16/sha80440a1d/private; pbeta 6/sha7643e764/private) |
| Sub-3 — README audit | **PASS** (clm 6 caveats, pbeta 7 caveats; #115 + license + chat-incapability all present) |
| Sub-4 — uchg/chflags + git state | **PARTIAL** (uchg deprecated; SHA256 baseline captured instead) |
| Sub-5 — time-to-fire manual | **PASS** (clm T-34.6h, pbeta T-39.0h; commands + confirm-strings verified) |

**Overall**: ready for unattended 36-40h dwell. 5 honest C3 issues documented.

---

## Sub-1 — `--check-only` dry-run

`bash state/anima_hf_promotes_2026_05_06_auto_fire.bash --check-only` exit non-zero (expected; GATE 1 short-circuits). Output shows:

- Now UTC: `2026-05-05T12:48:43Z`
- clm window ends: `2026-05-06T23:26:12Z` → `clm fire-able now: NO`
- pbeta window ends: `2026-05-07T03:48:00Z` → `pbeta fire-able now: NO`
- clm dry-run: `[promote ERR] GATE 1 FAIL: review window not yet elapsed`
- pbeta dry-run: `[promote ERR] GATE 1 FAIL: review window not yet elapsed`
- both promote scripts +x verified

`bash state/anima_hf_cleanups_2026_05_07_auto_fire.bash --check-only` exit non-zero (expected):

- clm cleanup: `[cleanup ERR] GATE 1 FAIL: review window not yet elapsed`
- pbeta cleanup: `[cleanup ERR] GATE 1 FAIL: review window not yet elapsed`

Window-enforcement gates working as designed. GATE 2 (HF state) + GATE 3 (manual sign-off) not exercised because GATE 1 fast-fails before then; that is correct fail-fast behaviour.

---

## Sub-2 — HF state pre-promote verification

### `dancinlab/clm-v4-mk2-v1`

| Field | Expected | Actual | Match |
| --- | --- | --- | --- |
| siblings_count | 16 | 16 | yes |
| commit_sha | `80440a1d38db9addc4445bb959057558a57f4230` | same | yes |
| private | True | True | yes |
| gated | False | False | yes |
| lastModified | 2026-05-04T23:26:12Z | 2026-05-04T23:26:12.000Z | yes |

16 siblings: `.gitattributes`, `LICENSE`, `README.md`, `__init__.py`, `best.pt`, `config.json`, `configuration_clm_v4.py`, `conscious_decoder.py`, `decoder_v3.py`, `generation_config.json`, `integrity_report.json`, `manifest.json`, `model.safetensors`, `modeling_clm_v4.py`, `tokenizer_64k_multilingual.model`, `tokenizer_64k_multilingual.vocab`.

Note: `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json` field `siblings_count: 15` is stale (off-by-one bug). Enumerated `siblings_list` in same verdict has 16 entries, matching HF API and the promote script's `EXPECTED_SIBLINGS=16`. The promote script uses the correct 16; only the verdict count field is wrong.

### `dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1`

| Field | Expected | Actual | Match |
| --- | --- | --- | --- |
| siblings_count | 6 | 6 | yes |
| commit_sha | `7643e764488f8e11020a7663c50f2e590b70d10f` | same | yes |
| private | True | True | yes |
| gated | False | False | yes |

6 siblings: `.gitattributes`, `LICENSE`, `README.md`, `adapter_config.json`, `adapter_model.safetensors`, `manifest.json`.

**Verdict**: both repos PRIVATE + intact + sha-stable. No silent mutation since upload.

---

## Sub-3 — README audit (PUBLIC release fitness)

### `docs/anima_clm_hf_release_v1_README_draft.md`
- 211 lines / 17,092 bytes
- 6 caveats (C1-C6): not chat-capable, F1_v2 RED, functional/access tier only, train_avg runtime proxy, single-substrate release, bit-exact shim suspiciously tight
- `#115` chat-incapability category-error language present (line 91)
- substrate-research-vs-chat-NLP disclosure: explicit
- random-floor benchmark disclosure: present
- forgetting_index 0.0196 + φ★ NO_FLIP: present (line 115-116)
- License clause present
- 2-cycle empirical chat-capability falsification (Pβ + CLM-2 LoRA): present (lines 98-123)

5+ caveat threshold: **PASS** (6 ≥ 5).

### `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05/README.md`
- 179 lines / 9,128 bytes
- 7 caveats (C1-C7): chat FAIL_TRUE composite 0.01176, substrate-research artifact ONLY, single-seed eval, holdout-500 limited n, Φ★ 41.86 anima-internal axis, PEFT-loadable but NOT instruct-following, base PRIVATE during window
- `#115` mention: present
- chat-FAIL_TRUE explicit (BLEU/ROUGE/chrF cited)
- substrate-research disclosure: present
- φ★ 42.37 baseline: present
- License clause present

5+ caveat threshold: **PASS** (7 ≥ 5).

Both README artifacts honest-C3 compliant for PUBLIC promote.

---

## Sub-4 — uchg + git state (silent-mutation detection)

`uchg ls` does not exist as a CLI on this mac; `uchg` is the macOS `chflags uchg` immutable flag. Per `docs/uchg_dance_deprecation_20260422.md`, anima formally deprecated the uchg dance pattern. `ls -lO` confirms no `uchg` flag set on any of:

- `state/clm_v4_hf_release_v1_upload_2026_05_04/{public_promote,cleanup}_2026_05_07.bash`, `verdict.json`
- `state/p9_pbeta_hf_upload_2026_05_05/{public_promote,cleanup}_pbeta_2026_05_08.bash`, `verdict.json`
- `state/anima_hf_promotes_2026_05_06_auto_fire.bash`
- `state/anima_hf_cleanups_2026_05_07_auto_fire.bash`

So uchg ls cannot be used as the silent-mutation watchdog. Replacement: SHA256 baseline + git status snapshot.

### SHA256 baseline (re-shasum at fire-time and diff)

```
f1933930c4b671e030fa4323044141c73c5466355ad7dc3ea8c08cd7bd35f5e8  state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash
c0e83446ddba2438ad3bf411074402c1a507ba89f749f7e77a555aebeb115d66  state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash
6021c206a2cef770ac6823c41d07dd70f9e41379cd2d80393c89cc5138858d7b  state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json
d6c736e4cb6f9934d23f0509ec9bc55866f7f8dffd69b427cf8894344a362d8d  state/p9_pbeta_hf_upload_2026_05_05/public_promote_pbeta_2026_05_08.bash
3e00113df8e1be35bc4bf3e0c620d412e92ef58baaf932d0369b6960dba4dab9  state/p9_pbeta_hf_upload_2026_05_05/cleanup_pbeta_2026_05_08.bash
86ff7812aec42e25f694d405b627b2a8c872c182ab17c1031d151ea5b9a427bd  state/p9_pbeta_hf_upload_2026_05_05/verdict.json
440c85f4a0abbd508fa3561fcd3c18ad87cb809c4c925b7264832979a7755a9b  state/anima_hf_promotes_2026_05_06_auto_fire.bash
9646dc4d7793fef9c2468b9e2c9c4f0663931a393f198c9ce7380f7b568d06e8  state/anima_hf_cleanups_2026_05_07_auto_fire.bash
```

### Git tree status

- `state/clm_v4_hf_release_v1_upload_2026_05_04/` — clean (committed in 7808f3d7, 0f60c26a, 7b394095)
- `state/p9_pbeta_hf_upload_2026_05_05/` — clean (committed in 0f60c26a, 7b394095)
- `state/anima_hf_promotes_2026_05_06_auto_fire.bash` — **untracked (??)**
- `state/anima_hf_cleanups_2026_05_07_auto_fire.bash` — **untracked (??)**

**Recommendation**: commit the two auto-fire scripts before sleep so they have a git audit trail; otherwise SHA256 is the only post-mutation detection layer.

---

## Sub-5 — time-to-fire user manual

### Fire phase (after review windows)

```
# CLM PUBLIC promote — eligible after 2026-05-06T23:26:12Z (T-34.6h from 2026-05-05T12:48:43Z):
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-clm
# When prompted, type EXACTLY: PROMOTE-clm-v4-mk2-v1

# Pβ PUBLIC promote — eligible after 2026-05-07T03:48:00Z (T-39.0h):
# IMPORTANT: clm-v4-mk2-v1 must already be PUBLIC first (PEFT base inheritance)
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-pbeta
# When prompted, type EXACTLY: PROMOTE-pbeta-50k

# Both sequential (clm then pbeta, with abort-on-clm-fail):
bash /Users/ghost/core/anima/state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-all
```

### Cleanup phase (after additional 24h consumer-download grace)

```
# CLM staging cleanup — eligible >= 2026-05-07T23:26:12Z (24h after PUBLIC promote):
bash /Users/ghost/core/anima/state/anima_hf_cleanups_2026_05_07_auto_fire.bash --fire-clm

# Pβ staging cleanup — eligible >= 2026-05-08T03:48:00Z:
bash /Users/ghost/core/anima/state/anima_hf_cleanups_2026_05_07_auto_fire.bash --fire-pbeta

# Both sequential:
bash /Users/ghost/core/anima/state/anima_hf_cleanups_2026_05_07_auto_fire.bash --fire-all
```

### Confirm-strings (extracted from `read -rp` lines in promote scripts)

- clm: `PROMOTE-clm-v4-mk2-v1` (line 114 of `public_promote_2026_05_07.bash`)
- pbeta: `PROMOTE-pbeta-50k` (line 115 of `public_promote_pbeta_2026_05_08.bash`)

Note: the user's BG-E request specified `PROMOTE-pbeta-...` as a placeholder; actual confirm-string is `PROMOTE-pbeta-50k`.

### Pre-fire checklist (operator)

1. Re-shasum the 8 files in §Sub-4 baseline; diff against verdict.json `sha256_baseline`. Any mismatch → ABORT + investigate.
2. Re-affirm G1-G6 of own 15 (the script will print and ask, but pre-affirm before typing confirm-string).
3. Confirm `secret get huggingface.token --raw` returns `hf_*` token.
4. For pbeta: confirm clm is already PUBLIC by `curl -sS -H "Authorization: Bearer $TOKEN" "https://huggingface.co/api/models/dancinlab/clm-v4-mk2-v1" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("private"))'` returns `False`.

---

## Honest C3 (5)

- **C1 — uchg/chflags absent.** anima formally deprecated the uchg dance 2026-04-22, so promote/cleanup scripts have no immutable-flag protection. SHA256 baseline + git status are the only mutation-detection layers during the 36-40h dwell. If a process mutates these files outside git, only re-shasum at fire-time catches it. **Mitigation**: re-shasum + diff against §Sub-4 baseline before each fire.
- **C2 — auto-fire scripts untracked.** `state/anima_hf_promotes_2026_05_06_auto_fire.bash` and `state/anima_hf_cleanups_2026_05_07_auto_fire.bash` are git `??` status, not committed. They could be deleted/modified silently. **Mitigation**: commit them before sleep, OR rely solely on SHA256 baseline. (This audit captures them in baseline.)
- **C3 — verdict.json off-by-one.** `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json` `siblings_count: 15` is stale; enumerated list has 16; HF API returns 16; promote script `EXPECTED_SIBLINGS=16`. **No fire-time risk** because script uses 16; only the verdict field is wrong.
- **C4 — silent HF-side mutation covered by GATE 2.** The promote script's GATE 2 re-fetches HF API at fire-time and asserts sha + private + siblings against expected. If anyone re-pushes to either repo during the dwell, GATE 2 fails and aborts. **Local script tampering is the residual risk class C1+C2 cover.**
- **C5 — Pβ depends on clm PUBLIC first.** G5 base-model-promotion check requires clm public before pbeta promote (PEFT base-model inheritance — non-auth readers cannot load adapter without base access). `--fire-all` enforces this via the `bash CLM_SCRIPT || { exit 1 }` guard line 95. If operator manually runs `--fire-pbeta` while clm is still PRIVATE, the pbeta promote technically succeeds at the visibility flip but creates a broken consumer experience. **Mitigation**: prefer `--fire-all`, OR manually verify clm PUBLIC before `--fire-pbeta`.

---

## Outputs

- `state/anima_hf_promote_watchdog_audit_2026_05_05/verdict.json` — full audit verdict (machine-readable)
- `docs/anima_hf_promote_watchdog_audit_landed_2026_05_05.ai.md` — this document
