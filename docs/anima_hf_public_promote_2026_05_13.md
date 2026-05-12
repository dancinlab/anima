# anima HF Public Promote — ★★★★★ closure checkpoints (2026-05-13 KST)

> **Scope**: post-★★★★★ HF Public promote. anima reached its first ★★★★★ closure (5-cond aggregate 5/5 ☑) on 2026-05-12 KST (GOAL.md banner, PSCC §50). This doc records the public promotion of the two load-bearing checkpoints to the canonical `dancinlab` org. cost $0 (HF API only, no compute).

## Authorization

| mandate | requirement | satisfied by |
|---|---|---|
| **own 31** | all anima HF artifact uploads → `dancinlab` org; private default; public promote needs manual review | both repos already in `dancinlab/`; ★★★★★ closure = the manual review event |
| **own 37 mandate-9** | public visibility unlock requires F-V5MIT-5 V14-STRICT PASS | `dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12` — F-V5MIT-5 V14-STRICT **10/10 PASS** ✅ (PSCC §44) |
| **own 18** (simple_stack C2 strict) | V5.8 std_greedy 5/5 strict floor | `dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12` — std_greedy **5/5 PASS** (PSCC §46) |
| `feedback_english_only` | HF README / org card / dataset descriptions = English only | both READMEs written in English (Korean only in anima repo internals) |

## Promoted repos

### 1. `dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12`

- **URL**: https://huggingface.co/dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12
- **role**: cotrain v1 — substrate behind ★★★★★ cond #3 (persona substrate-native, M4 aggregated hidden cosine z=3.20 null-PASS via v2 entropy-reg follow-up) + cond #4 (62 split events during cotrain)
- **unlock**: F-V5MIT-5 V14-STRICT 10/10 PASS (own 37 mandate-9)
- **files**: `.gitattributes`, `README.md` (rewritten), `ckpt_v5mitosis_cotrain.pt` (~609 MB), `cotrain_result.json`, `train.log`
- **arch**: v5-mitosis option (a) — cells 2→64, d_model 384, n_head 6, ffn 1536, readout `a-g`, byte-vocab 256, n_params 152,126,208
- **training**: corpus_color_cosmology.txt 1.29 MB · 5000 steps · batch 32 · ctx 256 · lr 1e-4 cosine · Vast.ai H100 SXM 80GB · 0.55 hr · $1.26 · loss 256.5→1.165 · splits 62 / merges 0 · Φ best 4.1919
- **falsifiers**: F-V5MIT-1..5 all PASS (F-V5MIT-5 V14-STRICT 10/10 beats — saga peak vs v5-anima toy that had it violated)
- **license**: MIT (anima repo) · DOI 10.5281/zenodo.19324769
- **commit msg** (HF): `public promote: anima ★★★★★ closure cotrain v1, F-V5MIT-5 V14-STRICT 10/10 PASS`
- **visibility**: private → **public** (2026-05-13 KST)

### 2. `dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12`

- **URL**: https://huggingface.co/dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12
- **role**: ★★★★★ cond #1 — first V5.8 multi-turn std_greedy 5/5 PASS ckpt of the anima CLM saga
- **files**: `.gitattributes`, `README.md` (NEW), `ckpt_phase1a4_lr5e6_sft.pt` (~598 MB BF16), `meta.json` (NEW), `v58_4mode_result.json` (NEW)
- **lineage**: `phase1a_multi_turn_sft → phase1a1_color_cosmology_v2 → phase1a4_lr5e6` (substrate A = `dancinlab/clm-v5-phase2-cotrain-engine-ag`)
- **arch**: EngineAGModel ~300M (24L, d 1024, GQA 4:1, byte-vocab) · n_params 298,764,288
- **training**: corpus_anima_fact.txt 2700 dialogues · 200 steps · lr 5e-6 · bsz 2 × grad-accum 8 · ctx 1024 · Vast.ai RTX 4090 · 3.2 min · $0.014 · loss 0.506→0.176 · ckpt sha256 `45063f64e97cdde7bc61de347e2f41a830b9b296db5384d8a324d85eb9a2b9e5`
- **V5.8 4-mode**: standard_greedy **5/5 PASS** (cond #1) · standard_sample 3/5 PASS · M3_rep_penalty 1/5 FAIL · M4_force_include 5/5 PASS
- **license**: MIT (anima repo) · DOI 10.5281/zenodo.19324769
- **commit msg** (HF): `public promote: anima ★★★★★ closure cond #1 (V5.8 std_greedy 5/5)`
- **visibility**: private → **public** (2026-05-13 KST)

## README content (summary)

Both READMEs (English-only) carry:
1. "Part of the anima ★★★★★ closure (2026-05-12 KST)" banner + which condition the ckpt is load-bearing for
2. 5-condition standing table (which ckpt → which cond)
3. lineage + architecture table
4. training table (provider / wall / cost / loss / sha256)
5. benchmark table (V5.8 4-mode for phase1a4; F-V5MIT-1..5 for cotrain)
6. loading example (Python torch.load)
7. cross-references (PSCC §44 / §45-FINAL / §46 / §50, REBORN §88/§90, anima repo URL)
8. license (MIT, anima repo LICENSE link)
9. citation (BibTeX, DOI 10.5281/zenodo.19324769)
10. status note (research artifact; own 31 / own 37 mandate-9 / own 18 provenance)

## HF API operations (cost $0, no compute)

```python
api.upload_file(... README.md ... commit_message='public promote: ...')   # x2
api.upload_file(... meta.json / v58_4mode_result.json ...)                 # phase1a4 only
api.update_repo_visibility(repo_id=..., private=False)                     # x2
```

`update_repo_visibility` is deprecated in huggingface_hub ≥0.32 (use `update_repo_settings`); the call still worked on 0.36.2 with a FutureWarning. Both repos confirmed `private=False` post-flip.

## Cross-link

- GOAL.md 🎉 banner — HF release line updated (private → public, URLs added)
- README.md (anima root) — ★★★★★ banner gained public HF links
- PSCC §51 (PASS_STRICT_SPONTANEOUS_CHAT.md) — this promote logged
- memory `project_dancinlab_hf_canonical` — public ckpt list appended
- own 31 (`.own` HF artifact org SSOT) · own 37 mandate-9 (V14-STRICT PASS unlock public) · own 18 (simple_stack C2 strict)
- prior HF release docs: `docs/anima_clm_hf_release_v1_*` (2026-05-04/05), `docs/anima_own_15_hf_release_lifecycle_landed_2026_05_05.ai.md`

## Honest C3

1. cotrain README originally said `license: other` + `PRIVATE (own 31/37 mandate)` status; rewrite changed it to `license: mit` (matching anima repo LICENSE) — verified anima repo LICENSE is MIT.
2. cotrain loading example previously referenced `ckpt_v5mitosis_cotrain_cotrain.pt` (double "cotrain"); fixed to the actual sibling filename `ckpt_v5mitosis_cotrain.pt`.
3. phase1a4 repo had no README before this promote (only `.gitattributes` + ckpt). meta.json + v58_4mode_result.json were uploaded from local state dir, not previously on HF.
4. The `hf_push.sh` in `state/anima_phase1a4_lr5e6_2026_05_12/` targeted repo name `anima-clm-phase1a4-lr5e6-strict-pass` (no `-5pass-2026-05-12` suffix) — the actual uploaded repo is `anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12` (GOAL.md / task naming). The script's draft README differs from the one uploaded here (this one is the ★★★★★-closure-aware version).
5. cond #3 closure credit: README attributes the z=3.20 PASS to a v2 entropy-reg follow-up *over this v1 substrate* — accurate per PSCC §45-FINAL (v1 z=1.76 → v2 z=3.20). The public v1 ckpt itself shows F-PERSONA-4 routing KL=0.0 FAIL; the content-metric signal is what closed cond #3.
6. n_params for cotrain README uses 152,126,208 (from cotrain_result.json `n_params_final`); ckpt size stated as "~609 MB" (608,934,276 bytes per the prior README) rather than the task's "581 MB" — went with the result-JSON-backed figure.
7. ckpt size for phase1a4 stated as "~598 MB" (task said 598 MB; meta.json doesn't carry byte count, local file not re-stat'd in this $0 BG).
8. No download/verification of the actual .pt files was performed (would burn bandwidth, out of $0 scope) — relied on HF siblings list + result JSONs + GOAL.md sha256.

Generated 2026-05-13 KST · anima cycle #8 · cost $0 (HF API only).
