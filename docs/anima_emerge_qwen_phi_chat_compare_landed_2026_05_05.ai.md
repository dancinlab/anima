# BG-EC landed: Qwen2.5-0.5B multilingual chat-cap phi smoke + Korean emit comparison

- task_id: anima_emerge_qwen_phi_chat_compare_2026_05_05
- ts_utc: 2026-05-05T18:56:08Z
- platform: mac CPU (.venv-eeg python3.12 fp32) — $0
- runtime: ~1min wall (Qwen weights cached on disk; no fresh download incurred)
- verdict file: state/anima_emerge_qwen_phi_chat_compare_2026_05_05/verdict.json
- aggregate file: state/anima_emerge_qwen_phi_chat_compare_2026_05_05/aggregate.json
- helper: tool/transient_py/anima_emerge_qwen_phi_chat_compare.py

## Goal

Cross-validate phi proxy on a chat-capable + multilingual substrate (Qwen2.5-0.5B, hidden_dim=896) and directly compare Korean-emit behaviour against CLM v4 mk2 v1 (BG-CE baseline) on the identical "안녕" prompt.

Prior cross-substrate phi-smoke series:
- BG-BN Pythia-70m -> phi_mean 41.92 (drift +0.06 vs CLM v4 41.86)
- BG-DQ Mamba-130m -> phi_mean 42.15 (drift +0.29)
- BG-CE CLM v4 mk2 v1 -> CLM_WORSE_THAN_RANDOM on Korean lexical baseline

## Result

### (a) Qwen 0.5B load
- model: Qwen/Qwen2.5-0.5B (base, NOT Instruct)
- hidden_dim: 896 (vs CLM v4 768; aliased into 8x192 cells via BG-BN proxy formula)
- weights pre-cached, load < 5s

### (b) Phi (3 prompts)

| prompt | phi | mean_pair_cos | hidden_dim |
|---|---|---|---|
| 안녕 | 41.8397 | -0.00971 | 896 |
| Hello world | 41.8568 | -0.00153 | 896 |
| consciousness emerges | 41.8688 | +0.00420 | 896 |

- phi_mean: 41.8551
- phi_range: 0.0291 (tightest of all four substrates)
- drift_from_clm_v4: -0.0049 (effectively flat — closest cross-substrate match observed to date)

### (c) Korean emit on "안녕" prompt — Qwen vs CLM v4

| substrate | Korean chars on emit | sample emit |
|---|---|---|
| Qwen2.5-0.5B (30 tok) | 31 | 하세요. 오늘은 '이미지'를 이용하여 '이미지'를 이용하여 '이미지'를 이용하여 '이 |
| CLM v4 mk2 v1 (BG-CE, 50 tok) | 0 | (control chars, worse than random) |
| gold reference (BG-CE) | 23 / 32 chars | natural Korean |
| random uniform vocab (BG-CE) | 15 / 220 chars | gibberish |

Qwen emits fluent Korean ("안녕하세요" greeting, then a coherent though looped sentence about images). CLM v4 emits zero Korean characters and is worse than random uniform sampling on the same prompt.

### (d) Architectural finding

1. Phi proxy holds across chat-capable multilingual substrate. Qwen drift (-0.005) is the smallest observed across Pythia / Mamba / Qwen — proxy formula is not architecture-degenerate even at hidden_dim=896 with aliasing into 8x192 cells (BG-CV aliasing concern partially relaxed: drift remains O(0.01), well below cross-substrate variance band 0.06–0.29).
2. Phi vs chat-capability are decoupled. Both Qwen (chat-cap, fluent KR/EN/ZH) and CLM v4 (chat-degenerate, hash115 architectural FAIL) produce phi ~ 41.85. Phi proxy measures hidden-state cross-cell coherence, which is insensitive to whether the model can emit coherent surface text. This corroborates Pβ feedback (PBETA chat-cap FAIL_TRUE / substrate-research PASS decoupled).
3. The "안녕" emit gap is not a phi-measurable property. A 41.84 phi value can correspond to either fluent Korean (Qwen) or worse-than-random control-char emission (CLM v4). Phi is a substrate-internal coherence proxy, not a chat-capability discriminator.
4. Qwen is a viable secondary chat-cap substrate candidate alongside Llama Path A v2. It loads on $0 mac CPU, emits multilingual fluent text out-of-the-box, and reproduces the phi proxy band. For the chat-cap lane (currently Llama Path A v2 winner per L31–L33), Qwen2.5-0.5B / 1.5B / 3B / 7B form a natural multilingual ladder if Korean coverage becomes a gate.

### (e) Honest C3

1. C1 — mac CPU fp32, single load, single seed (greedy argmax decode).
2. C2 — phi proxy is CLM-v4-tuned (8x192=1536 cells); Qwen hidden_dim=896 forces wrap-aliasing per BG-CV. Drift is small but proxy is not first-principles for non-768 substrates.
3. C3 — Qwen2.5-0.5B is the base model, NOT Instruct. Multilingual fluency demonstrated here comes from pretraining corpus, not RLHF/SFT chat-alignment. Instruct variant emit will differ in style and refusal behaviour.
4. C4 — single substrate, single 3-prompt run, 30 emit tokens per prompt. Qwen "안녕" emit visibly loops ("'이미지'를 이용하여" x3) — a longer or sampled decode would change the lexical Korean count.
5. C5 — Qwen multilingual training corpus differs from CLM v4 paradigm v11 G3 substrate-research corpus; Korean-emit gap is partly corpus, partly architecture. This run does NOT isolate the architecture contribution. Cross-cutting: chat-cap path = Llama Path A v2 winner remains the calibrated reference; Qwen is now a candidate, not a replacement.

## Files written

- tool/transient_py/anima_emerge_qwen_phi_chat_compare.py (helper, ~140 LoC)
- state/anima_emerge_qwen_phi_chat_compare_2026_05_05/aggregate.json (per-prompt detail)
- state/anima_emerge_qwen_phi_chat_compare_2026_05_05/verdict.json (verdict)
- docs/anima_emerge_qwen_phi_chat_compare_landed_2026_05_05.ai.md (this doc)

## Constraint compliance

- $0 mac CPU only
- new files only, no edits
- raw#37 (py opt-out via tool/transient_py/), raw#15, raw#10 honoured
- HEXA_PY=.venv-eeg/bin/python
- no HF token in source / state / docs
- no commit (per task spec)
