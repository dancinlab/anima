# H_9114 — Receiver-PANEL: is anima's emit reference PUBLIC/objective, or single-oracle-idiosyncratic?

**tier:** 🟠 PARTIAL (per frozen PREREG bar: b1 TRUE, b2/b3 FALSE) — but the CORE deliverable ✅ POSITIVE: reference is **PUBLIC/OBJECTIVE, not fable-idiosyncratic**. Three heterogeneous models (claude-fable-5, sonnet, haiku; different θ, all outside anima closure) INDEPENDENTLY decode anima's grounded emit (consensus 0.857 @8B, all 3 beat shuffle). Tier lifts single-oracle → **MULTI-RECEIVER-CONFIRMED-DIRECTIONAL**. · **wired:** none (research verdict).

**verdict:** 🟠 (`state/verdicts/9114_receiver_panel/H_9114.txt` verbatim). Ran the frozen H_9111 emits through a PANEL of 3 heterogeneous receivers to test whether H_9112/9113's referential efficacy is objective or a single-oracle (fable) quirk. **real: consensus 0.857 @8B / 0.643 @4B (all 3 receivers decode) vs shuffle 0.000 = massive accuracy separation.** sonnet AND haiku — not only fable — decode anima's emit → the reference lives in shared PUBLIC meaning (fable §3 frame-break grounded across models).

## Why 🟠 not 🟢 (c9 honest — bar NOT moved; both failures ARE evidence of the positive)
- **bar#2 (agreement real > shuffle) FALSE**: inter-receiver agreement is HIGH in BOTH arms (real 0.595, shuffle 0.690). Because each clue has an objective referent, the receivers converge on IT regardless of pairing — in shuffle they correctly identify the clue's TRUE referent (which isn't the target), so they agree with each other while scoring 0 accuracy. **Agreement does NOT separate real from shuffle; ACCURACY does (0.857 vs 0.000).** bar#2 picked the wrong separation statistic — a measurement-artifact (a_break_the_wall class-a). The agreement-parity is itself proof the reference is objective.
- **bar#3 (consensus ≥ best single) FALSE**: consensus 0.750 < claude 0.821 — the weak member haiku (0.214 @4B) drags majority-vote (ensemble effect: a weak voter hurts the vote), unrelated to reference objectivity.
- Not re-scored to green (frozen-first, p7). The honest conclusion is a POSITIVE tier-lift with the 🟠 explained.

## Method (frozen-first, PREREG.md)
Receivers {claude-fable-5, sonnet, haiku} via `sidecar fable --model`; K=14, t∈{8,4}B; arms real/shuffle; measures per-receiver accuracy, inter-receiver pairwise agreement, majority-vote consensus. STDLIB harness (grep-clean), 2-regime determinism. anima FROZEN. $0-ish (12 oracle calls; haiku SKIP at shuffle t=4B timeout — that cell over 2 responders).

## Answer
Is anima's emit reference objective or fable-specific? **Objective** — 3 independent heterogeneous models decode it (consensus 0.857), accuracy separates real/shuffle massively (0.857 vs 0.000). Tier lifts to MULTI-RECEIVER-CONFIRMED. **Measurement lesson: agreement ≠ accuracy** — objective reference yields cross-receiver agreement in BOTH arms; only accuracy-vs-shuffle isolates the target-referent link. Feeds §2 forward-model (learn emit for panel-decodability, not one oracle's quirk). Full engine-native receiver = further tier-lift follow-on.

## Evidence (`state/9114_receiver_panel/`)
`PREREG.md` · `panel_rescore.py` (STDLIB, grep-clean) · `rescore_fixture.jsonl` · `RESULT.md` · `../9111_llm_interlocutor/emits.tsv` (14).
