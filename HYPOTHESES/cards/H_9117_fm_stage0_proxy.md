# H_9117 — §2 Stage-0: validate the in-engine forward-model proxy before .hexa/GPU ($0)

**tier:** 🔴 LEXICAL-PROXY-WEAK (for the $0 surrogate tested) + VALUABLE REDIRECT to a simpler proxy. · **wired:** none (DIRECTIONAL, $0, no oracle).

**verdict:** 🔴 (`state/verdicts/9117_fm_stage0_proxy/H_9117.txt` verbatim). fable §2 impl (DESIGN_fable_s2impl.md) prescribed validating an in-engine "frozen-listener CONTRASTIVE prefix decodability" proxy d̂ (corr≥0.656 gate) BEFORE .hexa/GPU. I tested a $0 LEXICAL surrogate of that listener (IDF-contrastive prefix margin). **Result: corr(d̂ lexical, oracle-decodability) = −0.21 (FAIL — dominated by total word-mass, not front-loading), but corr(filler_prefix surface baseline, oracle-decodability) = +0.688 (the TRIVIAL front-loading proxy predicts decodability WELL).**

## Reading (c9)
- The lexical surrogate is a bad approximation of fable's contrastive listener; the FAIL does NOT refute fable's actual CLM-listener proxy (the real mouth-backend sees byte-level discriminability the bag-of-words misses) — that remains untested (needs the real backend, heavier).
- REDIRECT (valuable): the SIMPLE surface proxy filler_prefix works (r=0.688). Consistent with H_9116 Screen-A (corr(filler_prefix, gain)=0.656). The SAME cheap front-loading feature is the robust signal across both screens. So Stage-1's mouth-gate rerank can be scored by a **cheap in-engine front-loading measure** — no contrastive CLM-listener pass needed. fable's contrastive elaboration is (as yet) unnecessary.

## Net for §2
Cheap in-engine proxy question RESOLVES toward the simple end: front-loading degree (r≈0.69) is a viable in-engine-computable modulation target. Stage-1 .hexa (rz_forward_model 3-tier resolver + mouth-gate K-rerank scored by front-loading, engine_cli.hexa + emit_policy.hexa + generator L3, byte-identical default) remains the next rung — a real core/*.hexa engine build (multi-turn, surgery) + external b50 re-measure. The proxy is now CHEAPER than designed (no CLM-listener), but the .hexa build + GPU boundary is unchanged.

## Evidence (`state/9117_fm_stage0_proxy/`)
`DESIGN_fable_s2impl.md` (fable §2 impl spec) · `stage0_proxy.py` (STDLIB, grep-clean, $0) · `RESULT.md` · reuses `../9115_forward_model_screen/screenb_fixture.jsonl`.
