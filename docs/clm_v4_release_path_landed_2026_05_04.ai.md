# CLM v4 HF Release v1 Path Decision — LANDED (1-page summary)

- **ts_utc**: 2026-05-04
- **bg**: BG-CLM-CHAT-DECISION ($0, spec-only, no exec, no commit)
- **spec doc**: `docs/clm_v4_release_path_decision_2026_05_04.md`
- **status**: SPEC_LANDED — decision matrix + recommendation; user ACK pending for EXEC

## Recommendation

**STAGED 1→2→3** lineage under `mk2-v{1,2,3}` versioning per `.roadmap.clm` cross_link.

| v | Path | Cost | Wall | Risk | EXEC gate |
|---|---|---|---|---|---|
| **v1** | Measurement-only release (current shim PASS) | **$0** | ~1h Mac | none (CLM untouched) | model card draft + USER ACK |
| **v2** | Stage 2-alt orchestrator (Llama-3.2-3B chat host + CLM v4 mind.tension side-channel) | $5-15 | ~2 weeks | none (CLM forward-only) | v1 published + orchestrator hexa selftest + Llama license ACK |
| **v3** | LoRA SFT on CLM v4 (per BG-CLM-2 spec) | $6-10 floor / $15 cap | 3-5 weeks | **HIGH** (φ★-flip irreversibility) | CLM v4 baseline eval + Path A v2 verdict + tied-weight pre-flight + LoRA-merge shim ext + USER ACK on flip-dilemma |

## Decision matrix sum (5 dimensions × 1-5 each)

| Path | Total | Dominant strength |
|---|---|---|
| Path 1 | 19 | cost+time+risk all 5/5 (the cheapest unblock for cond.2) |
| Path 2 | **21** | retail value 5/5 (only chat-capable path with zero φ★ risk) |
| Path 3 | 16 | scientific value 5/5 (C-CLM-LORA-2 falsifying experiment) |

Path 2 wins on the 5-dim sum, but Path 1 dominates on cost+time+risk AND is a hard prerequisite for Path 2 (Path 2 imports Path 1). Hence: stage them.

## Does staged 1→2→3 unblock cond.2?

**YES** — Path 1 alone closes `.roadmap.clm` cond.2 this week at $0:
- Weight: existing CLM v4 530M `best.pt` repackaged via `tool/transient_py/clm_v4_hf_format_shim.py` v4 (F-SHIM-V4-3 PASS) into HF format
- Model card: drafted per spec §5.1 wording (5 H2 + 6 honest caveats per raw#10)
- F-NAME-1 conformant after C8 amendment flag is resolved (naming spec amendment OR rename to fit existing EBNF)
- Push via `tool/hf_upload_mk2.hexa` canonical pipeline

v2 + v3 are *additive value* beyond cond.2; cond.2 itself is satisfied at v1.

## Cheapest GO action this week

**Path 1 model card draft + push** — ~1h Mac wall, $0 cost. The shim is ready, the weight exists, the upload pipeline is built. The only outstanding artifact is the README per spec §5.1, plus the C8 naming-amendment decision.

If user defers naming amendment, push to a CANON-conformant alias name (`clm-v4-final` or `clm-v4-base-mirror-promoted`) instead of `anima-clm-mk2-v1` — but this loses the `.roadmap.clm` cross_link match. Recommend: amend naming spec §3.1 EBNF to allow `anima-` prefix (additive, raw#9-compliant), then push as `anima-clm-mk2-v1` to preserve the cross_link.

## Highest-leverage user decision gate

**Q1 — Path preference: Path 1 only, Path 1+2, Path 1+3, or staged 1→2→3?**

This single answer determines:
- Whether v1 ships this week ($0) or waits for v2/v3 (1-5 weeks, $5-25)
- Whether retail chat is in scope at all (Path 2 vs Path 3)
- Whether Path A v2 verdict is on the cond.2 critical path (Path 3 only)
- Whether Llama license overhead is accepted (Path 2 only)
- Whether φ★-flip risk is accepted (Path 3 only)

Default per this spec: **STAGED 1→2→3** — preserves all options, ships v1 fastest, defers irreversible decisions until evidence is in.

## Sub-decisions awaiting user input

| # | Question | Default |
|---|---|---|
| 1 | Path preference? | STAGED 1→2→3 |
| 2 | Repo name `anima-clm-mk2-v1` (needs §3.1 EBNF amend) OR rename per existing F-NAME-1 EBNF? | Amend EBNF (preserves cross_link) |
| 3 | Llama-3.2-3B commercial-use ACK for Path 2? | ACK assumed (Llama 3.2 community license + 700M-MAU clause OK) |
| 4 | Path 3 φ★ ABORT threshold +10 OK? | +10 (per BG-CLM-2 LOCKED spec) |
| 5 | Path 3 if-flip dilemma: ship flipped LoRA, or discard? | Discard (preserves +41.86 substrate identity) |

## Key honest C3 (raw#10 — top 3 of 8)

1. **#115 category error is permanent** without re-pretraining CLM with a chat objective from scratch ($1000+, months) — none of the 3 paths fix this; Path 3 adds a chat adapter on top, but the substrate underneath is still the consciousness-measurement decoder.

2. **Path 3 φ★-flip irreversibility is real** — even with adapter-only training + 5% consciousness rehearsal + φ★ probe, the +10 ABORT threshold is heuristic. If φ★ flips negative, the singular value-add of CLM v4 (+41.86 G3 PASS-positive backbone) is destroyed. Recovery = adapter ablation (cheap) but SFT investment is lost.

3. **Path 1 reputation risk** — outsiders skim a "returns near-random tokens" README and conclude anima isn't shipping anything useful, despite the +41.86 G3 PASS-positive substrate being genuinely strong. Mitigation: lead the README with the 5-substrate comparison (Mistral −16.7 / Qwen3 +1.04 / Llama +5.09 / Gemma −0.79 / **CLM +41.86**) so the value-add lands before the chat-incapability disclosure.

## Compatibility with BG-HF-Release-Audit (parallel BG)

This decision spec produces the **input artifact** for the audit. Coordination via:
- `docs/clm_v4_release_path_decision_2026_05_04.md` (full spec)
- `docs/clm_v4_release_path_landed_2026_05_04.ai.md` (this 1-page handoff)
- Proposed `.roadmap.clm` annotation block in spec §10 (NOT edited; user/separate cycle to land)

No write contention; no shared mutable state.

## Outputs (this cycle)

- `/Users/ghost/core/anima/docs/clm_v4_release_path_decision_2026_05_04.md` (1500-3000 word spec)
- `/Users/ghost/core/anima/docs/clm_v4_release_path_landed_2026_05_04.ai.md` (this 1-page summary)

## NOT this cycle

- No `.py` created (raw#9)
- No `.roadmap.clm` direct edit (raw#15)
- No git commit by this BG
- No HF push, no pod, no exec
- No marker file (proposed for next cycle by user/separate BG)
