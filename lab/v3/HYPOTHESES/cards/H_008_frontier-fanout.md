---
id: H_008
ssot: ARCHITECTURE.json → verification-h008 (this card is a frozen verdict record; distil FROM here INTO the tree)
slug: frontier-fanout
title: With F1 (write-lever) terminated by L11 and F3 (diary) spent, do ANY of the four remaining live frontier families — F7 owner (clean re-run of H_007's borderline), F5 trajectory, F6 shard-ensemble, F4 corpus-curriculum — carry a $0-measurable premise that ESCAPES the salvage laws? If every branch refuses/decorates at $0, the zero-cost structural-analysis phase of the campaign is complete.
domain: the whole remaining fd-true-axes frontier — owner-substrate (F7/F5/F8) · selection-lineage (F6) · write-lever corpus half (F4)
status: pre-register-frozen
exploration_method: /abg fan-out (one Workflow, 4 isolated worktrees) over the branches the H_006/H_007 terminal left live
verification_method: 4 parallel $0 deterministic conditional-bpb / rank probes (H_005 machinery) — each with its own pre-registered kill + liveness control
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_008 — frontier-fanout

## Hypothesis

The campaign has terminated F1 (write-lever, by the L11 fusability=recoverability theorem) and spent
F3 (diary, H_006). The `fake-diversity-audit` says only four genuinely distinct bets remain, and
three of them (F7/F5/F8 owner, plus F6 lineage and the F4 corpus half of the write-lever) are NOT
compute-blocked — they are $0-checkable on the substrates already in hand. Rather than probe them
serially, fan them out at once and ask each the same question: **does a cheaply-measurable premise
survive the salvage laws, or does it collapse to a v1 failure (one-bit seam / frequency tautology)?**

> Four independent $0 branches, each a falsifiable premise-check with its own liveness control:
> **f7-owner-clean** (redo H_007 with a text-like liveness + per-day grain: is the owner legible AND
> high-dimensional on the SAME grain?) · **f5-trajectory** (is the owner stream a DIRECTED arrow of
> time, or a symmetric topical window?) · **f6-shard-ensemble** (does data-shard specialization beat
> a matched-capacity monolith robustly across capacity?) · **f4-curriculum-headroom** (does a learned
> acquisition policy beat a frozen n-gram retriever, or is corpus selection the L11 tautology?).

Outcome per branch: **ANCHORED** (premise escapes the laws → that family is LIVE, design the organ)
· **REFUSED** (premise collapses to a salvage law at $0) · **BORDERLINE** (small/non-robust). The
campaign-level outcome: **FRONTIER-EXHAUSTED** iff all four refuse/decorate.

## Why

- Institutionalizes the campaign's $0-first discipline at the FRONTIER scale: before any owner-model
  training (F7/F5) or ensemble maintenance (F6) spend, measure the premise the spend rests on.
- H_007 left the owner premise BORDERLINE on a single grain with a broken liveness control. The clean
  re-run (f7) resolves it by (a) rebuilding the liveness text-like so markov works, and (b) measuring
  legibility and dimensionality on BOTH per-session and per-day grains — the v1 l1-one-bit-seam
  predicts they cannot co-occur.
- f4 is the corpus hand of the same write-lever L11 already killed on the codec hand — a direct test
  of whether `fd-write-lever-pair`'s "two hands, same lever" claim holds at $0.

## Predictions

- **P-f7** legibility (over-floor > ε) AND high-dim (PR > 2) on the SAME grain `?` (the anchor).
- **P-f5** direction signal (forward-pred − backward-pred) > ε `?` (a real arrow of time).
- **P-f6** shuffle-corrected shard-specialization benefit > ε and same-sign across capacities `?`.
- **P-f4** oracle-curriculum over-floor vs a frozen n-gram retriever > ε on the INDEPENDENT estimator `?`.

## Variables (frozen)

- **substrate**: genuine owner transcripts `~/.claude/projects/*/*.jsonl` (f7/f5); the anima/hexa-lang
  git day-streams (f4/f6, H_005 chunking). Privacy: only aggregate bpb/rank numbers leave the disk.
- **geometry**: W=4096, P=2048 (H_005 verbatim). ε = 0.02 bpb; PR floor 2.0 (strictly above one-bit).
- **estimators**: markov3 + markov8 (f7 grains), markov6 + ppm (f4/f6 cross-check), gzip reported.
  Each branch carries the pre-registered liveness control REBUILT text-like (the H_007 fix).

## Run Protocol

- **harness**: `tool/anima_v3.py` + `state/h005…/run_h005.py`; per-branch `state/h008_<branch>_2026-07-16/run_h008.py`.
- **fan-out**: one `Workflow` call, 4 worktree-isolated agents (rate-limit-safe · `fanout-workflow`).
- **artifacts**: `state/h008_<branch>_2026-07-16/result.json` (+ run_stdout.txt where captured).
- **deterministic**: stdlib only, $0, GPU 0.

## Criteria

- **verdict_rule (per branch)**: **ANCHORED** iff the branch's premise clears ε (and PR>2 where a rank
  gate applies) with liveness PASS and estimator sign-agreement. **REFUSED** iff the premise ≤ ε or the
  rank collapses ≤ 2.0. **BORDERLINE** iff positive but small/non-robust (sign-flips across capacity).
- **campaign_rule**: **FRONTIER-EXHAUSTED** iff no branch is ANCHORED.

## Falsifiers (pre-registered)

- **F7-kill**: owner legible XOR high-dim (never both on one grain) → owner-substrate (F7/F5/F8) REFUSED
  (the v1 l1-one-bit-seam, re-measured on the real owner).
- **F5-kill**: direction signal ≤ ε → the owner stream is a symmetric topical window, not a directed
  trajectory → F5 adds only a recency-window over F7, no arrow-of-time self.
- **F6-kill**: shard benefit ≤ ε OR sign-flips across capacity → the monolith in-context-adapts to the
  domain (the L11 superset argument) → F6's shard axis does not escape it.
- **F4-kill**: a frozen n-gram retriever ties/beats the hindsight-oracle curriculum on the INDEPENDENT
  estimator → corpus selection is the L11 frequency tautology (the corpus half of the write-lever).
- **liveness (each branch)**: a planted stream carrying the branch's target property MUST read positive
  through that branch's instrument, else that branch is **INVALID(instrument)**.

## Honest Limits

- **L1** each branch is a $0 PREMISE check, not the organ; a REFUSED premise retires the family cheaply,
  an ANCHORED premise only licenses designing the (compute-bearing) organ.
- **L2** f6/f4 use the git day-stream proxy (a developer-project system, not an agent) inherited from H_005.
- **L3** the owner transcript is the DIRECTIVE voice (terse commands); legibility here is a lower bound
  on a richer interaction — a REFUSED still leaves a private richer channel unmeasured (owner's call).
- **L4** byte-class rank features are coarse; a rank collapse is suggestive, a high rank a lower bound.

## Cross-Links

- **architecture**: `verification-h008` (gate) · `components.F7`/`F5`/`F6`/`F4` · `salvage.l1-one-bit-seam`
  · `salvage.l11-fusability-is-recoverability` · `fake-diversity-audit` · `convergence.cr-zero-cost-frontier-exhausted`
- **predecessors**: `H_007` (owner borderline — RESOLVED + corrected by f7) · `H_004`/`H_006` (F1/F3 terminals)
- **substrate**: `~/.claude/projects/*/*.jsonl` (f7/f5) · anima + hexa-lang git streams (f4/f6)

## Verdict

**🧱 FRONTIER-EXHAUSTED — all four branches refuse or decorate at $0** (run 2026-07-16 · one Workflow,
4 isolated worktrees · GPU 0). The zero-cost structural-analysis phase of the campaign is COMPLETE.

### Per-branch results

| branch | verdict | the number that decides it |
|---|---|---|
| **f7 owner-clean** | 🔴 **REFUSED** | legible XOR high-dim, never both: per-session PR **2.29** but over-floor +0.02 (not legible); per-day legible (markov3 **+0.145**, markov8 **+0.176**) but PR **1.75** (one-bit). Liveness now PASSES text-like (markov3 +0.224, markov8 +0.476). |
| **f5 trajectory** | 🟡 **F5-WEAK** | recent past accumulates (growth **+0.106** > ε) BUT time is SYMMETRIC (direction signal **+0.004** ≤ ε) — a topical window, not a directed arrow of time. |
| **f6 shard-ensemble** | 🟡 **BORDERLINE→REFUSED** | shuffle-corrected shard benefit small + NON-ROBUST across capacity (4k **+0.048**, 16k **−0.086**, 64k **+0.050** — sign-flips); raw oracle lift +0.159 exceeds the perfectly-separable ceiling +0.029 = mostly oracle-min artifact. |
| **f4 curriculum-headroom** | 🔴 **REFUSED (L11)** | raw selection headroom real (+0.211) but decoration: markov6 says oracle beats the frozen 6-gram retriever +0.117, the INDEPENDENT ppm says **−0.117** (retriever ties/beats). Corpus selection = the frequency tautology. |

### The finding

Across the four remaining `fd-true-axes` families probed in parallel at $0, **every cheaply-testable
premise fails**: the owner is legible XOR high-dimensional but never both on one grain (the v1
one-bit seam, now re-measured on the REAL owner — the clean resolution of H_007's borderline); the
owner stream is a symmetric topical window, not a directed trajectory (F5); data-shard specialization
does not robustly beat a matched-capacity monolith (F6); and corpus selection is the L11 frequency
tautology in its corpus outfit, exactly as `fd-write-lever-pair` warned (F4).

### Consequence for the campaign

The **$0 structural-analysis phase is COMPLETE** — 7 solo cards + these 4 fan-out probes, GPU 0
throughout. Write-lever (F1/F4) terminated by L11 on both hands; owner families (F7/F5/F8) REFUSED
(owner is not legible-AND-high-dimensional on any one grain); F3 diary spent (H_006); F6 shard axis
borderline-refused. What remains is compute-only residual whose premises the $0 phase measured weak
or refused — not a cheap frontier. The honest next move is a campaign-level re-decision about whether
any compute-bearing residual is worth a real spend, not another $0 card.

_FRONTIER-EXHAUSTED: the zero-cost phase found no surviving premise on the available substrates; the
remaining residue is compute-bearing and premise-weak. Recorded to `cr-zero-cost-frontier-exhausted`._
