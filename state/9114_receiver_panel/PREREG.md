# H_9114 — Receiver-PANEL referent-agreement: is anima's emit reference PUBLIC/objective, or single-oracle-idiosyncratic?

**Seed:** H_9112/9113 measured anima's referential efficacy with a SINGLE external oracle (claude-fable-5) → tier stuck at DIRECTIONAL-on-external-oracle (could be fable-idiosyncratic decoding, not objective reference). This experiment runs the SAME frozen H_9111 emits through a PANEL of ≥2 heterogeneous receivers (different θ, all outside anima's closure) and measures whether they INDEPENDENTLY CONVERGE on the same referent. Multiple independent minds agreeing = the reference is **public/objective** (lives in shared referents, fable §3 frame-break) → lifts the tier from single-oracle to panel-consensus. anima side FROZEN, $0-ish (3× oracle calls per config).

## Design (panel; anima FROZEN)
- Receivers = {claude-fable-5, sonnet, haiku} via `sidecar fable --model <m>` (heterogeneous θ, all external to anima). Any receiver that errors/times-out is SKIPPED and logged (agreement computed over responders; ≥2 required for an agreement number).
- Referential game: K=14 (near-synonym distractors), truncation t ∈ {8, 4} bytes (informative 2-point: 8B strong-signal, 4B divergence-onset per H_9113 — not ceiling).
- Arms: real / shuffle (deranged concept↔emit).

## Measures
- **per-receiver accuracy** vs ground-truth (each receiver × t).
- **inter-receiver AGREEMENT** = mean over trials of (fraction of receiver-PAIRS that picked the SAME concept, regardless of correctness) — referent-convergence. Real vs shuffle.
- **consensus accuracy** = majority-vote of receivers vs ground-truth.

## FROZEN BAR (registered BEFORE running — no post-hoc move, c9/p7)
🟢 PUBLIC-REFERENCE (tier-lift to panel-consensus) iff ALL:
1. ≥2 independent receivers each decode real > shuffle at the signal bytes (t≥4), AND
2. mean inter-receiver agreement on REAL ≥ 0.60 at t≥4 AND ≥ 0.20 above shuffle agreement (independent minds converge on the SAME referent), AND
3. consensus (majority-vote) accuracy ≥ single-best-receiver accuracy (panel not worse than its best member).
🟠 SINGLE-ORACLE-IDIOSYNCRATIC iff only ONE receiver decodes well and the others are at chance (reference is fable-specific, not objective) — tier stays DIRECTIONAL-on-external-oracle.
🔴 NO-OBJECTIVE-REFERENCE iff inter-receiver agreement ≈ shuffle across the board (no cross-mind convergence).

## Determinism / provenance
Regime-1 frozen fixture (per pinned model, each trial queried once); regime-2 deterministic stdlib scoring. No anima re-decode, no GPU, no pod. $0-ish. Controls: shuffle (referent link) + cross-receiver heterogeneity.

## Gate branch
🟢 → tier lifts from single-oracle DIRECTIONAL to PANEL-CONSENSUS-DIRECTIONAL (multiple independent minds = reference is objective, fable §3 empirically grounded) → strengthens the H_9112/9113 GREEN and the §2 forward-model justification (learn emit for panel-decodability, not one oracle's quirk).

Bar frozen 2026-07-03 before any oracle query. Data: state/9111_llm_interlocutor/emits.tsv (14). Card: H_9114 on completion.
