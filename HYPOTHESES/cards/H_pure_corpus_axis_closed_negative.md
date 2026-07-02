---
id: H_pure_corpus_axis_closed_negative
slug: pure-corpus-axis-closed-negative
title: PURE corpus-dilution axis alone cannot close multilingual register-coherence — ruled out across the full wiki_frac sweep
tier: 🔴 CLOSED-negative
verdict: 🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted) — .verdicts/pure-corpus-axis-closed-negative/{closure,register}.txt
domain: PURE
status: terminal
verdict_artifact: .verdicts/pure-corpus-axis-closed-negative/closure.txt
method_kind: run
migrated_from: CLAIMS.tape @C pure_wiki_sweep + pure_register_orthogonal + pure_wikifrac03_closed_negative (2026-06-16 retirement, c9 no-loss — 3 sub-claims consolidated)
hexa_only: true
---

# PURE — corpus-axis ⊥ multilingual closure (closed-negative)

**slug**: `pure-corpus-axis-closed-negative` · **group**: PURE · **verdict pointer**:
`.verdicts/pure-corpus-axis-closed-negative/{closure,register}.txt`

> Migrated from `CLAIMS.tape` on 2026-06-16 (CLAIMS.tape retirement). This card consolidates the
> THREE PURE-group `@C` run-claims that shared the slug `pure-corpus-axis-closed-negative` and had
> no card/jsonl home (verdicts VERBATIM from the tape + the `.verdicts/` evidence — c9 no-loss).
> Closed-negative (a_paper_negative_ok): the corpus-dilution axis ALONE cannot close multilingual
> register-coherence — ruled out across the full wiki_frac sweep {0.0, 0.3, 0.5, 1.0}.

## Sub-claim 1 — `pure_wiki_sweep` (run)

**Claim**: wiki_frac sweep {0.0,0.5,1.0} — multilingual closure 4/5 ≥ PARTIAL never reached.
**cmd**: `hexa run HEXAD/PURE/eval/closure_auto_judge.hexa (E2 · E3 · v3)`
**raw**: `.verdicts/pure-corpus-axis-closed-negative/closure.txt`
**src**: PURE.log.md 2026-05-25 · state/pure_phase_d_v3_result_2026_05_24/
**verdict**: 🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted)

## Sub-claim 2 — `pure_register_orthogonal` (run)

**Claim**: register_hits=0 at wiki_frac=0 (TTR 0.34) yet coherence stays WEAK — corpus-axis ⊥
multilingual closure.
**cmd**: `hexa run HEXAD/PURE/eval/multilingual_probe.hexa (v3 ckpt)`
**raw**: `.verdicts/pure-corpus-axis-closed-negative/register.txt`
**src**: UNIVERSE/cards/H_242 §A2 (H242.1 FULL-COLLAPSE falsify)
**verdict**: 🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted)

## Sub-claim 3 — `pure_wikifrac03_closed_negative` (run)

**Claim**: wiki_frac=0.3 — register_collapse PASS (0 hits) yet all 5 langs WEAK · closure FAIL 1/4.
**cmd**: `hexa run HEXAD/PURE/eval/closure_auto_judge.hexa state/p21h_v3_recover_2026_05_25/out_main/result.json`
**raw**: `state/p21h_v3_curricula_recover_2026_05_25/closure_verdict_wiki03_verbatim.txt`
**src**: state/p21h_v3_recover_2026_05_25/ · HF dancinlab/anima-p21h-v3-wikifrac03-recovered-2026-05-25 (PRIVATE)
**note (verbatim from tape)**: wiki_frac=0.3 intermediate point (P21H V3, recovered SIGHUP-orphan
run). closure_auto_judge 1/4 PASS · FAIL: register_collapse PASS (0 hits) yet all 5 langs WEAK.
Adds the 0.3 sweep point → closed-negative now holds at {0.0, 0.3, 0.5, 1.0}.

## Consolidated verdict (verbatim)

🔴 CLOSED-negative — the corpus-dilution (wiki_frac) axis is ORTHOGONAL to multilingual closure:
register collapse (hits=0) does NOT cause coherence to emerge; multilingual closure 4/5 ≥ PARTIAL
is never reached across {0.0, 0.3, 0.5, 1.0}. Frozen evidence:
`.verdicts/pure-corpus-axis-closed-negative/closure.txt` + `register.txt`.

xref H_242 (register-collapse wiki_frac sigmoid) · a_paper_negative_ok · a_scale_honest_scope · p7.
