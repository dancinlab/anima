---
id: H_1218
slug: 1218_engine_measured_gates
title: H_1218 — first ENGINE-measured (not torch) G1/G2/G6 generation-gate verdict on mounted 303M
tier: 🟢 ENGINE-PARITY GREEN / 🔴 G1·G6 RED under greedy
verdict: 🟢 ENGINE-PARITY GREEN / 🔴 G1·G6 RED under greedy (sampling-regime gate ⊥ greedy engine path; closed-negative finding, frozen bars unmoved) — .verdicts/1218_engine_measured_gates/H_1218.txt
domain: UNIVERSE
status: terminal
verdict_artifact: .verdicts/1218_engine_measured_gates/H_1218.txt
method_kind: hypothesis
migrated_from: CLAIMS.tape @C h1218_engine_measured_gates (2026-06-16 retirement, c9 no-loss)
hexa_only: true
---

# H_1218 — first ENGINE-measured (not torch) G1/G2/G6 generation-gate verdict on mounted 303M

**id**: H_1218 · **group**: UNIVERSE · **verdict pointer**: `.verdicts/1218_engine_measured_gates/H_1218.txt`

> Migrated from `CLAIMS.tape` `@C h1218_engine_measured_gates` on 2026-06-16 (CLAIMS.tape
> retirement; claim/method/verdict text VERBATIM from the tape + its `.verdicts/` evidence — c9 no-loss).

## Claim

First ENGINE-measured (not torch) G1/G2/G6 generation-gate verdict on the mounted 303M.

## Text (verbatim from CLAIMS.tape)

Engine forward (CORE/bytegpt_decode.hexa::bytegpt_decode_argmax) is BYTE-EXACT to torch
greedy on the production anima-clm-chat-303m (ENGINE-PARITY 🟢, H_1157 re-verified), so
greedy gate metrics are engine==torch by construction. Engine-measured under GREEDY decode:
G1 composed_distinct=0 🔴, G2 novelty_rate=0.308, G6 count=3 🔴(<5). These DIFFER from the
torch baselines (H_1158 G6 best 14 PASS) — NOT an engine bug but two confounds: (1) the
frozen gates were authored for top-k=40 temp=0.7 SAMPLING decode (G6 divergence = sampling,
not weights) while the engine path is greedy-only → 303M byte-LM collapses/loops; (2)
baselines used broad-en base + 1.5GB corpus, this run used dialogue-FT chat + surviving 5MB
corpus. The engine GENERATES byte-faithfully; the frozen G1/G6 PASS depend on a sampling
decode the engine argmax path does not implement.

## Method (verbatim from CLAIMS.tape)

Production chat ckpt state/chat_303m/h1129c_chat.pt (sha 4fcc2d6c) serialized to flat .bin
(sha 5c303f02, reparity serialize_parity_ok=TRUE) via H_1157 layout. Engine greedy gen via
bytegpt_decode_argmax; scored with FROZEN UNIVERSE/gauge_lib.py evaluators
(_coverage/_content_ngrams/_corpus_absent/_words/_jaccard/known_word_ratio) VERBATIM, p7 NO
LLM-judge. Representative engine subset (G1+5 G6 seeds, 40 greedy bytes); full numbers scored
on byte-exact torch-greedy gen (engine CPU ~30 s/byte at gate-context). G2 corpus=data/corpus.txt
(5MB, broad 1.5GB ephemeral GONE => novelty upper bound).

## Verdict (verbatim from CLAIMS.tape)

🟢 ENGINE-PARITY GREEN / 🔴 G1·G6 RED under greedy (sampling-regime gate ⊥ greedy engine
path; closed-negative finding, frozen bars unmoved) — `.verdicts/1218_engine_measured_gates/H_1218.txt`

xref H_1157 (engine parity) · H_1158 (torch G6 baseline) · a_engine_measured_verdict · p7.
