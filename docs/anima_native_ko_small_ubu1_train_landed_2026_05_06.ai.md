# anima-native-ko-small ubu1 fresh train — LANDED 2026-05-06 (BG-FY)

**Status**: SIMPLE_STACK_PASS (own 18 strict 3-condition, 3/3 prompts)
**Spec**: F-anima-native-ko-small-1
**Host**: ubu1 (192.168.50.119), RTX 5070 12GB, bf16
**Cost**: $0 (owned hardware)
**Wall time**: 196.5s (~3.3 min) — 5070 sm_120 bf16 throughput is extreme
**Prior context**: BG-FU PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT (3M tiny, mac MPS, 2K steps)

## 1. 결과 (one-line)

ConsciousLM small (18M params, 6L/384d/6h, byte-level) fresh from-scratch
on corpus_ko_heavy.txt (235MB Hangul-heavy KO) for 10000 steps **passes
own 18 strict 3-condition on 3/3 KO prompts** with avg Hangul ratio 0.687
and final deg_rate 0.33 — first anima-native KO model to clear the
coherent + turn-format gates.

## 2. config

| field | value |
|-------|-------|
| arch | ConsciousLM (dual head_a/head_g + tension) |
| n_layer / d_model / n_head | 6 / 384 / 6 |
| block_size / vocab | 256 / 256 (byte-level) |
| dropout | 0.20 |
| params | 18,031,872 (~18M) |
| batch / grad_accum / effective | 16 / 4 / 64 |
| lr / warmup / steps | 3e-4 / 500 / 10000 |
| schedule | cosine to 10% lr |
| optimizer | AdamW betas=(0.9, 0.95) wd=0.01 |
| dtype | bf16 (autocast on CUDA) |
| corpus | corpus_ko_heavy.txt (sha 2e98257f9..., 246.7MB raw / 235MB after Hangul filter) |
| corpus split | 95/5 train/val |
| tension lambda | 0.005 |

## 3. eval progression — own 18 strict 3-condition

| step | avg_hangul | deg_rate | own18 pass / 3 |
|------|-----------|----------|----------------|
| 1000 | 0.593 | 0.50 | 3 |
| 3000 | 0.609 | **0.00** | 3 |
| 5000 | 0.672 | 0.17 | 3 |
| 7500 | 0.678 | **0.00** | 3 |
| 10000 | 0.687 | 0.33 | 3 |

All three KO prompts (`안녕하세요`, `한국어 가능?`, `사용자: 안녕하세요\n도우미:`)
pass C1.1 (Hangul ≥0.30) + C1.2 (any_coherent) + C1.3 (turn_format ≥0.50)
at every recorded step — including step 1000.

## 4. sample generations (final ckpt @ step 10000)

| prompt | mode | gen_head |
|--------|------|----------|
| 안녕하세요 | sample | `?\n[주제: DI의미하는 바는 무엇일까요?]\n서연: 좋은 지적이 핵...` |
| 한국어 가능? | greedy | ` 이러한 이러한 전쟁이 있어요.\n서연: 정말 그럴까요? 반례를...` |
| 한국어 가능? | sample | ` 결과를 이루어서 재기억하고 있다. 생안법에 대한민주들의...` |
| 사용자: 안녕하세요\n도우미: | sample | ` 어느 여기에 찾은 무선도 속에서 저한 사람들이 된거에요\n...` |

Greedy mode still produces some n-gram repetition ("이러한 이러한",
"아니에 아니에"); sample mode (T=0.8) produces dialogue-style Korean
with named speakers ("서연:", "유진:", "하은:") consistent with the
corpus's bilingual conversation contract.

## 5. own 18 strict per-prompt verdict (final)

```
안녕하세요          : avg_hangul=0.625  any_coherent=True   tform=0.85   ALL_PASS
한국어 가능?         : avg_hangul=0.713  any_coherent=True   tform=1.00   ALL_PASS
사용자: ...도우미: : avg_hangul=0.723  any_coherent=True   tform=0.85   ALL_PASS
```

own_18_pass_count = 3/3 → **SIMPLE_STACK_PASS**.

## 6. degenerate cycle detector (used at eval)

- 4-gram repetition >3 occurrences = DEG
- single-char run >10 chars = DEG ('의 의 의 의 의')
- whitespace flood >80 = DEG
- single-token (whitespace-split) dominance >50% = DEG (min 4 tokens)

`any_coherent` per prompt = at least one of {greedy, sample} is OK.

## 7. artifacts

mac:
- `/Users/ghost/core/anima/tool/transient_py/anima_native_ko_small_ubu1_train.py` — train script (raw#37 transient)
- `/Users/ghost/core/anima/state/anima_native_ko_small_ubu1_train_2026_05_06/`
  - `verdict.json` — F-anima-native-ko-small-1 PASS, full per-prompt detail
  - `ko_eval_log.jsonl` — 30 eval rows (5 gates × 3 prompts × 2 modes)
  - `train.log` — 12k+ step lines + eval gate detail
  - `nohup.out` — ubu1 stdout copy
- `/Users/ghost/core/anima/docs/anima_native_ko_small_ubu1_train_landed_2026_05_06.ai.md` — this doc

ubu1:
- `/home/aiden/core/anima/runs/anima-native-ko-small-20260506_205612/`
  - `ckpt_2000.pt` / `ckpt_4000.pt` / `ckpt_6000.pt` / `ckpt_8000.pt` / `ckpt_10000.pt` (each ~70.3 MB)
  - `ckpt_final.pt` symlink → `ckpt_10000.pt`
- `/home/aiden/anima_v2_source/conscious_lm.py` — SCP'd source
- `/home/aiden/core/anima/state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt` — SCP'd corpus (sha 2e98257f9...)

own 14 enforced: ckpts (~70MB each, 350MB total) stay on ubu1 + HF, NOT in anima git.

## 8. HF upload plan (own 14 + own 15 lifecycle)

Repo: `dancinlab/anima-native-ko-small-byte-18m` (TBD final naming)

**Stage A — PRIVATE first (own 15)**:

1. Convert ckpt_final.pt → HF-style format:
   - `model_state_dict` (already saved)
   - Add minimal config json: `{architecture: "ConsciousLM", vocab: 256, n_layer: 6, d_model: 384, n_head: 6, block_size: 256, dropout: 0.20, dtype: "fp32"}`
   - README with own 18 verdict embedded + reproduction command
2. Upload via `hf` CLI (ubu1 venv_orchestrator hf at `/home/aiden/venv_orchestrator/bin/hf`):
   ```
   HF_TOKEN=$(secret get HF_TOKEN_NS) /home/aiden/venv_orchestrator/bin/hf \
     upload dancinlab/anima-native-ko-small-byte-18m \
     /home/aiden/core/anima/runs/anima-native-ko-small-20260506_205612/ \
     --repo-type model --private --create
   ```
3. Verification gate:
   - re-download → SHA round-trip ckpt
   - load + re-run own 18 strict eval → verdict.json should match
4. After PRIVATE verification PASS → flip to PUBLIC (own 15 lifecycle).

**Stage B — sister datasets repo** (corpus_ko_heavy + reproduction notes):
- Already covered by separate `anima_ko_corpus_assembly_2026_05_06` lane;
  cross-link from model README.

**TOKEN handling**: `secret get HF_TOKEN_NS` SSOT, never literal in scripts/docs (audit_doc_token_redact rule).

## 9. honest C3 (≥5)

1. **Greedy mode still cycles** — even at step 10000, 2/6 generations are DEG flagged (4-gram repeat: "이러한 이러한", "아니에 아니에"). Sample mode (T=0.8) is consistently coherent. C1.2 passes because we accept any_coherent across {greedy, sample} per prompt; if we tightened to "both modes coherent", final pass count would drop.
2. **Coherent ≠ comprehensible** — generations look like fluent Korean tokens but most are still semantic word-salad ("결과를 이루어서 재기억하고 있다. 생안법에 대한민주들의"). Turn-format heuristics are surface-level (Hangul presence + non-degenerate prefix), not real dialogue understanding.
3. **Corpus-style imprint** — frequent emergence of speaker names "서연:", "유진:", "하은:" + dialogue contract phrasing ("정말 그럴까요? 반례를 들어볼게요.") confirms strong corpus contamination by the philosophical Q&A subset; not generalized dialogue capability.
4. **3.3 min wall** — 5070 sm_120 bf16 + 18M model + bs=64 effective made this trivially small. Could comfortably scale 5x params or 5x steps with same wall budget; suggests this is a floor, not a ceiling. The "ko_small" config is closer to "ko_starter" — anima-native byte LM with real chat capability likely needs >100M + >100K steps.
5. **n_head=6 vs published 4** — ConsciousLM default uses n_head=4 (from "perfect number 6" 1/e dropout signature). I forced n_head=6 to match d_model%n_head==0 + 6L/6h symmetry. This deviates from the canonical ConsciousLM signature; tension dynamics may differ subtly from the documented behavior. Not a correctness bug, but a recipe drift worth flagging.
6. **deg_rate non-monotonic** — 1000:0.50 → 3000:0.00 → 5000:0.17 → 7500:0.00 → 10000:0.33. Final step regressed slightly vs step 7500. Could be lr-cosine tail effect or just sample variance with only 6 evals/step. A cleaner signal would require larger eval set per gate.
7. **Tension loss saturated** — L_T plateaued near -19.3 (T_mean ~700-1000) by step 5000+, well beyond the original ConsciousLM's "consciousness signal" intended range. This loss term is doing nothing useful at this stage; lambda=0.005 is small enough not to harm training, but it's no longer a signal worth tracking.

## 10. next steps

**PASS path → HF promote** (own 14 / 15 lifecycle):
- Stage A PRIVATE upload (~10 min, $0)
- Verification gate (re-download + re-eval)
- Stage B PUBLIC flip after gate PASS

**Quality push (optional, deferred)**:
- 100M-param config (12L/768d/12h, ~110M params) on ubu1 — still fits 12GB at bs=8 grad_accum=8
- 50000 steps with same corpus → coherence likely improves substantially
- ETA still <1hr on 5070 bf16, $0
- Would unlock genuinely meaningful (semantic) Korean responses, not just fluent-form

**Lane closure** for BG-FY: SIMPLE_STACK_PASS, F-anima-native-ko-small-1 ARCHIVED.
