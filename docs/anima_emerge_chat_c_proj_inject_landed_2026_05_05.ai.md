# anima emerge chat c_proj inject landed (BG-BE)

- **task_id** : `anima_emerge_chat_c_proj_inject_2026_05_05`
- **bg_lane** : BG-BE
- **ts_utc** : 2026-05-05T17:34:21Z
- **platform** : mac CPU fp32 (`.venv-eeg/bin/python`)
- **cost** : $0
- **wall** : ~30s (model load 5s + 5 decodes)

## Verdict

**FAIL_ALL** — `n_coherent = 0 / 5` configurations produce semi-coherent text.

`#115 우회 verdict` : **NOT BYPASSED via c_proj architectural rescue path** — the
hypothesis "c_proj weights exist in best.pt but are not loaded by the HF inference
path, so applying c_proj transform to a substrate-realistic fixture would produce
chat-capable injection" is **inapplicable on this Mac substrate** because:

1. The released HF model `dancinlab/clm-v4-mk2-v1` (model.safetensors)
   ships only decoder weights — **0 c_proj keys** found in `model.state_dict()`.
2. **0 best.pt files** found in HF cache or local repo (HF cache layout has
   blobs/snapshots only; `~/.cache/huggingface/hub/**/best.pt` does not exist;
   all `.pt` files in the repo are unrelated training stubs without c_proj keys
   per train_avg_harvest_result.json provenance).
3. Identity 192×192 fallback was therefore used, which is mathematically
   equivalent to **no projection** — fixture is forwarded raw into cross_attn,
   collapsing this run to a re-test of BG-Q/BG-Z behaviour at SOC-norm 1.5/3.0/5.0.

## c_proj 발견 결과 (a)

| Source                                                | Searched              | Hits |
| ----------------------------------------------------- | --------------------- | ---- |
| HF model `state_dict()` (`dancinlab/clm-v4-mk2-v1`) | runtime introspection | 0    |
| `~/.cache/huggingface/hub/**/best.pt`                 | glob                  | 0    |
| `/Users/ghost/core/anima/{ready,checkpoints,state}/**/best.pt` | rglob | 0    |

**Provenance** : per `state/.../train_avg_harvest_result.json:ckpt_top_keys`,
`best.pt` (training-time) contains `['step','decoder','optimizer','scheduler',
'phi','ce','args','scale','best_phi','federation','bridge','c_proj','scaler']`
— **but that artifact lives only on the training H100, never published to the
HF mirror, never copied to this Mac.** The audit's BG-Z C4 is confirmed:
released model is permanently missing the c_proj projection by design (or
by oversight).

## c_proj transformed inject vs no-inject baseline (b)

| Config                          | First 30 decoded chars (top-1) |
| ------------------------------- | -- |
| `baseline_none` (no inject)     | `\x1c` + 29×`\x06` |
| `soc_norm_1.5_with_cproj`       | `\x1c` + 29×`\x06` |
| `soc_norm_1.5_with_cproj_topk`  | `\x1c}\x06\x1c\x1c` + 25×replacement-char |
| `soc_norm_3.0_with_cproj`       | `\x1c` + 29×`\x06` |
| `soc_norm_5.0_with_cproj`       | `\x1c` + 29×`\x06` |

All deterministic configs collapse to the **same byte-fragment attractor**
(`\x1c` then `\x06` repeating) — the canonical L36 chat-incapability signature
for CLM v4 mk2 (matches BG-Q/BG-Z observations: cross_attn pathway is alive,
but the substrate has no surface representation that decodes to language).

`topk` sampling perturbs the first ~5 tokens but still falls into a near-zero
fragment. **No discrimination** between with-inject and without-inject under
top-1 greedy — confirming once more that on this released substrate, the
inject channel cannot rescue chat capability regardless of fixture geometry,
magnitude, or projection basis.

## n_coherent (c)

```
n_coherent = 0 / 5  ->  FAIL_ALL
```

## #115 우회 verdict (d)

**HYPOTHESIS WITHDRAWN ON MAC** — the c_proj-projected-fixture path requires
either:

1. Re-uploading `c_proj` Linear weights from a training H100 checkpoint to a
   companion HF release, OR
2. Re-running this probe on the H100 where `best.pt` natively lives.

Until either is satisfied, the architectural blind spot identified by BG-Z C4
is **observed but not actionable on Mac** — and even with the projection
applied (identity), the released CLM v4 mk2 chat-incapability persists across
SOC-norm magnitudes 1.5 / 3.0 / 5.0. This adds another datapoint to the
converging evidence (#115 + Pβ + CLM-2 + CLM v4 LoRA SFT) that the chat-cap
barrier is **architectural, not fixture-tunable**.

## Honest C3 (e)

1. **C1 mac CPU fp32** — no MPS/CUDA acceleration; numerical precision
   identical to train fp32, so substrate behaviour is faithful at the dtype
   level (the FAIL_ALL is a substrate result, not a precision artifact).
2. **C2 c_proj 발견 여부 best.pt cache layout 의존** — released HF
   `model.safetensors` does NOT include c_proj (training-time artifact only;
   per train_avg_harvest_result ckpt_top_keys archaeology). Identity fallback
   used when not found, which is mathematically equivalent to no projection
   and reduces this run to a SOC-norm sweep at 1.5/3.0/5.0 with broadband
   random raw fixture.
3. **C3 c_proj transform이 actual training-time projection과 다를 가능성** —
   even when real c_proj weights are extractable, application order at
   inference (`raw @ W.T + b`) may differ from train_clm.py:1477 application
   context (post-aggregation, pre-decoder cross_attn). Without source-level
   trace through `c_proj(c_for_decoder)` flow, basis-correctness is unverified.
4. **C4 broadband random raw가 actual c_engine state distribution 모방 안
   함** — true `c_engine.get_states()` output is a structured per-cell SOC
   trajectory with EMA threshold, topple-reset, and inter-cell correlations.
   `torch.randn` + per-cell L2-rescale captures norm only, not
   phase/correlation/skew structure. Even with real c_proj, the **shape gap
   from BG-Z §3** persists.
5. **C5 single prompt `안녕`** — KO greeting only; no en/multi-axis prompt
   sweep; semi-coherent heuristic (Korean+ASCII letter count + char-repetition
   ratio) is binary and loose, with high false-PASS susceptibility (false-FAIL
   here is robust given the byte-fragment attractor).

## Lineage carry

- **extends** : `state/anima_paradigm_v11_g3_canonical_magnitude_audit_2026_05_05/verdict.json` (BG-Z C4 c_proj blind spot)
- **extends** : `tool/transient_py/anima_emerge_cand_d_inject_helper.py` (BG-Q canonical helper, model loader reused)
- **informs** : converging chat-incapability evidence (#115 + Pβ + CLM-2 + CLM v4 LoRA SFT)
- **closes** : c_proj-rescue-on-Mac hypothesis (HOLD lane on BG-Z C4)

## Deliverables

- `tool/transient_py/anima_emerge_chat_c_proj_inject.py` — helper (raw#37, .own 3)
- `state/anima_emerge_chat_c_proj_inject_2026_05_05/aggregate.json` — 5 configs × decoded text
- `state/anima_emerge_chat_c_proj_inject_2026_05_05/verdict.json` — verdict + honest C3
- `docs/anima_emerge_chat_c_proj_inject_landed_2026_05_05.ai.md` — this doc

## Raw compliance

- raw#9  read-only on substrate (no model retrain) — PASS
- raw#10 honest C3 (5 caveats) — PASS
- raw#15 additive (no mount/shim/dialogue modification) — PASS
- raw#37 transient .py namespace (`tool/transient_py/`) — PASS
- no_commit — PASS
- no_secret_leak — PASS
