---
id: H_004
slug: f1-static-anchor-pilot
title: Measure Δ_pilot = F2(oracle codec) − F2(frozen codec) on held-out-stem × novel-NEG forced-choice flips — the ceiling of the codec effect at rig scale. Δ_pilot ≥ 0.20 licenses the H_002′ twin with delta_min = Δ_pilot/2; below it the twin is REFUSED.
domain: write-lever axis (F1 codec-is-the-self) — successor to H_003 (rig = LICENSED)
status: pre-register-frozen
exploration_method: H_003 LICENSED + rig-pilot spec -> Fable 5 design pass (D1-D6)
verification_method: 5 seeded training runs (fp32 transformer) + forced-choice bpb eval + 7 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: false
llm: none
genspec_sha256: fbcf0c8ad444d0f3c2fa5ad018d12ce8f33ad6bcf8e0f78eb26be5495527ce2b
---

# H_004 — f1-static-anchor-pilot

## Hypothesis

The campaign's first non-$0 measurement. **NOT a test of F1**: both arms are STATIC (no
refit organ, no continual dynamics) — they differ ONLY in which frozen codec tokenizes the
same bytes. It measures:

> **Δ_pilot = F2(ORACLE) − F2(FROZEN)** on held-out-stem × novel-NEG forced-choice flips
> after the phase-2 drift — the CEILING of the codec effect at rig scale (~10M-class,
> from-scratch, synthetic drill). ORACLE ≥ refit by construction: the oracle codec has
> phase-2 atomicity from step 0 and pays zero swap cost (`rig-pilot-measures`).

After this card, **no number transfers from MORPH-ATOM** — it survives only as the
existence proof of the mechanism class. `delta_min` for H_002′ is anchored in-rig as
Δ_pilot / 2, closing the three gaps of `decision-attributability` (contrast, substrate,
corpus) at once.

Outcome set: **ANCHORED** (Δ_pilot ≥ 0.20 → H_002′ licensed, delta_min = Δ_pilot/2) ·
**TWIN-REFUSED** (Δ_pilot < 0.20 — a result, not a delay) · **PREMISE-DEAD** (oracle at
chance → campaign re-decision) · **INVALID** (liveness / sanity / leak failure — not a Δ=0
reading).

## Why

- H_003 = LICENSED 10/10: anchor green (M=109/120, replicated), generator produces the
  contrast (frozen deficit 1.0, refit 0.0, drift 0.1256, leak 0, 1536 clean items).
- `rig-pilot-kill-power` pre-commits the kill: below Δ_pilot = 0.20, delta_min < 0.10 →
  N > 1178/arm — barely deliverable by the 1536-item pool and pointless (the ceiling is too
  low to detect the refit increment underneath it at the $25 twin budget).
- The uncertainty is genuine, not ceremonial: the FROZEN arm STILL sees all phase-2 flip
  supervision — a transformer can learn "this 6-jamo suffix → NEG" as a multi-token
  sequence. Whether single-token atomicity buys HELD-OUT-STEM recombination on top of that
  is exactly `l4-morph-atom-slot-not-address`, never measured at this substrate. Δ_pilot
  could plausibly be 0.4 or 0.02 — that is what the pilot is FOR.
- Per `l4-morph-atom-amplifier` (NAT-ATOM), the stream carries explicit flip marks, so an
  oracle-at-chance reading is attributable to the drill-scale premise, not missing
  supervision — provided the arm demonstrably learned the drill (F1 gate).

## Arms (5 runs · differ ONLY in codec; no refit organ)

All 5 train on the SAME canonical byte stream (phase-1 then phase-2, sequential, no
inter-phase shuffle), cut at 150,000,000 bytes/phase ≈ 300M total (exact count + sha256
frozen as `corpus_sha256`).

| run | arm | codec | seed |
|-----|-----|-------|------|
| 1 | ORACLE | `fit_bpe_jamo(sample_p1(10k)+sample_p2(10k), K=512)` | 101 |
| 2 | ORACLE | same codec | 202 |
| 3 | FROZEN | `fit_bpe_jamo(sample_p1(20k), K=512)` (H_003's frozen) | 101 |
| 4 | FROZEN | same codec | 202 |
| 5 | C3′ liveness | FROZEN codec + deterministic remap: every NEG-marked utterance's affix span (longest-suffix match over the 16 NEG forms) → one reserved token `NEGID` | 101 |

Oracle's fit sample (10k+10k) matches frozen's (20k) in SIZE — the codecs differ in what
they saw, not how much. Seeds are PAIRED across oracle/frozen (same seed → identical init +
intra-phase shuffle → per-seed Δ isolates the codec). `NEGID` is reserved-but-unused
outside C3′ for parameter parity (V=543 in every arm).

## Model + training

- decoder-only transformer, 6 layers, d_model 256, 8 heads, d_ff 1024, RoPE, RMSNorm, no
  biases, tied embedding/head, context 256, fp32. V = 543 (30 base + 512 merges + NEGID).
  **Params ≈ 4.86M** (the `rig-model` "~10M" label assumed vocab 4–8k; at K=512 the honest
  count is 4.9M — skeleton kept, label corrected; parameter parity across arms is the
  load-bearing property).
- data: packed 256-token blocks, next-token CE all positions; token counts FLOAT per codec
  on matched bytes (measured: oracle ≈11.5 B/tok → ≈26.0M tokens; frozen ≈10 B/tok → ≈29.5M
  `?`). AdamW β(0.9,0.95) wd 0.1 clip 1.0, peak lr 3e-4 `?` cosine→3e-5, warmup 250, batch
  16×256, ≈6.4k/7.2k steps, one pass.
- **SHAKEDOWN discipline**: one oracle/seed-999/30M-byte run may tune lr/batch/warmup
  against training loss + F1-drilled ONLY — F2 and every held-out item are NEVER computed on
  it. Final config frozen as `config_sha256` before any verdict run.
- **l10 does NOT apply**: every arm trains from scratch under its own codec; no embedding
  crosses a codec boundary, no warm-start, no checkpoint reuse. l10 taxes the REFIT organ —
  that bill lands on H_002′'s adaptive arm, which is why the oracle is the ceiling.

## Eval

**F2** — recovered H_9288 forced-choice flip, chance 0.50, all **1536** items:
- prompt = `SENTINEL + body + SENTINEL`, body = `to_jamo(render(stem, [affix if label==neg
  else plain]))` (framing == stream framing — v1 bug #3 was this mismatch).
- candidates = `to_jamo(POS_MARK)+SENTINEL` vs `to_jamo(NEG_MARK)+SENTINEL`, each encoded by
  THAT ARM's codec; score total −log₂ P(candidate | prompt); pick min; correct iff matches
  `label`.
- **codec fairness**: both candidates are 2 jamo + sentinel = equal byte length, so
  total-log-prob comparison IS bits-per-byte (salvage l6). No per-token quantity is compared
  across codecs; any cross-arm CE diagnostic is via `bits_per_byte()` and per p7 is never a
  verdict.

**F1** — drilled-stem sanity, 256 items (drilled stems × the same 12 novel NEG allomorphs,
composition seen verbatim in phase-2), same scoring, gate ≥ 0.90. F1 and F2 items differ
ONLY in stem membership, so F1-high + F2-low reads cleanly as "learned the drill, cannot
recombine".

**Liveness**: F2(C3′) ≥ 0.90 (≥ 1383/1536) else the ENTIRE pilot is INVALID (not Δ=0).

## Criteria — the Δ_pilot decision rule

Exact counts, never rates. k_X(s) = correct count of arm X seed s over n=1536.

- **Δ_pilot = (k_O(101)+k_O(202) − k_F(101) − k_F(202)) / 3072**.
- **ANCHORED** iff no falsifier triggers AND k_O(101)+k_O(202) − k_F(101) − k_F(202) ≥ 615
  (Δ_pilot ≥ 0.20). Then frozen before H_002′: delta_min := Δ_pilot/2;
  N := `two_proportion_n(0.5, 0.5+delta_min)` (script's printed value binding); σ_seed(F2)
  := per-arm |k(101)−k(202)|/(1536·√2). Coherence: at Δ_pilot=0.20, delta_min=0.10 → N=1178
  ≤ 1536 available.
- Report per-seed F2 for all 5 runs, the paired per-seed Δs, and the 2-seed spread verbatim.

## Falsifiers (pre-registered)

- **P-1 the kill**: k_O(101)+k_O(202)−k_F(101)−k_F(202) ≤ 614 of 3072 (Δ_pilot < 0.20) →
  **H_002′ REFUSED**.
- **P-2 premise**: pooled oracle inside the exact 99% chance band at n=3072 = **[1465, 1607]**
  → the mechanism class does not exist at this substrate even with atomicity handed free →
  **PREMISE-DEAD**, campaign re-decision (NOT a silent F4 switch). Interpretable only if P-4
  passes for the oracle arms.
- **P-3 liveness**: k_C3′ < 1383/1536 → **INVALID**.
- **P-4 drill sanity**: F1 < 231/256 in any verdict arm → arm VOID → **INVALID**.
- **P-5 leak on the trained corpus**: `leak_scan` (all 1536 surfaces) +
  `heldout_neg_cooccurrence` at FULL 300M depth → any hit → **INVALID** (`l6-leak`).
- **P-6 seed instability**: |k(101)−k(202)| ≥ 154/1536 in oracle or frozen → add seed 303 to
  both verdict arms (~$0) before reading P-1; still ≥ 154 → **PENDING(seed-power)**.
- **P-7 config identity**: the 4 verdict runs share `config_sha256` + `corpus_sha256`,
  differing only in {codec, seed}; genspec = `fbcf0c8…`; C3′ differs additionally only in the
  remap. Any mismatch → **INVALID**.

## Predictions

- **P1** oracle F2 ≥ 0.70 `?` (anchor M=0.908; uncertain at 4.9M from-scratch).
- **P2** frozen F2 above the multi-token floor but well below oracle `?` — the one quantity
  nothing in the record constrains; this is what the pilot is FOR.
- **P3** F2(C3′) ≈ 1.0 · **P4** F1 ≥ 0.98 all arms · **P5** σ_seed(F2) < 0.03 `?`.

## Run Protocol

- **harness**: `tool/anima_v3.py` (`chance_band`, `two_proportion_n`, `bits_per_byte`)
- **generator**: `src/generator/` (spec `fbcf0c8…`, K=512)
- **trainer**: a from-scratch decoder-only transformer + AdamW + packed-block loader +
  forced-choice/bpb eval. Per demiurge d3 its home is the `hexa-lang` stdlib (≥3 consumers:
  H_004, H_002′, F3/F5); a local `src/trainer/` is the fallback FOR THE PILOT with an
  explicit upstream-fix debt note (l8 — do not let the home-rule block the first measurement).
- **compute**: Mac mini MPS, **$0** (≈0.8 PFLOP/run × 5 ≈ 4 PFLOP; 1–8 h overnight). Fallback
  one RTX 4090 via `hexa cloud` ≤ $2 if measured MPS throughput < 5k tok/s. No GPU rental is
  needed; the ≤$10 envelope holds with ≥5× margin.
- **pre-check ($0, already run)**: `run_proxy.py` — a tiny numpy neural LM on the SAME D3
  eval, for a directional Δ_proxy that gates the real spend (research-before-measurement). A
  clear positive is de-risking evidence; a null is not decisive (under-capacity).
- **run script**: `state/h004_static-anchor-pilot_2026-07-16/run_h004.py` (spec-wiring +
  falsifier ledger). **artifacts**: `.../result.json` + per-run ckpts/eval JSONs.
- **determinism exception** (`rig-determinism-exception`): fixed seeds, fp32, logged env,
  verbatim stdout binding; bitwise reproducibility NOT claimed.

## Honest Limits

- **L1 ceiling, not the effect**: Δ_pilot is what refit could AT MOST deliver (oracle pays no
  swap cost, no l10 tax, no continual interference). Says nothing about whether the refit
  organ harvests any headroom (H_002′) or about identity (~300M natural-stream claim).
- **L2 one designed language**: Δ_pilot is a property of THIS drill (explicit marks,
  NOVEL_NEG_SHARE_P2=0.80, 512 stems, K=512). The genspec hash bounds shopping but the spec's
  author wants F1 to live, and the spec was shaped by reading the anchor's protocol.
- **L3 two seeds**: σ_seed from 2 samples has ~±75% relative error `?`; it enters H_002′'s
  compound rule as a sanity floor, not a variance estimate.
- **L4 scale is 4.9M**, measured nowhere else — not 10M-labeled, not 303M-anchored. Transfer
  in either direction unestablished; `l4-morph-atom-slot-not-address` stays an argument.
- **L5 byte-matching subsidizes frozen**: same bytes → frozen sees ≈13% more tokens → more
  steps. Biases Δ_pilot DOWN (conservative for the kill; a true ceiling modestly above the
  measured one is possible).
- **L6 receptive metric**: mark-classification measures the flip relation receptively, not
  generation. Marks are trivially frequent in every arm — all item difficulty lives in the
  held-out body composition by design, but that design is part of the rig, not of F1.

## Cross-Links

- **architecture**: `rig-pilot` (`-arms`/`-measures`/`-derives`/`-kill-power`) ·
  `rig-sequence-h004` · `rig-liveness-c3-prime` · `rig-drift-breaks-symmetry` ·
  `gates-power-table` · `l4-morph-atom-slot-not-address` · `l10-codec-swap-costs-the-embedding`
  · `rig-determinism-exception` · `decision-attributability` (superseded)
- **predecessor**: `H_003` (LICENSED 10/10) · **successor**: `H_002′` (12-run twin)
- **design seed**: `state/h004_static-anchor-pilot_2026-07-16/DESIGN_fable.md`
- **pre-check**: `state/h004_static-anchor-pilot_2026-07-16/run_proxy.py` (numpy $0 proxy)

## Verdict

**⏸️ PRE-CHECK BLOCKED the run** — the seeded torch/MPS pilot is NOT fired. A $0 numpy
pre-check (`run_proxy.py`, 55s) caught a rig-invalidating defect before any spend, which is
exactly what research-before-real-measurement is for.

### The pre-check finding (verified, structural — not model-dependent)

`run_proxy.py` trained a tiny numpy neural LM on this card's exact D3 eval, oracle vs frozen:

- **Δ_proxy = −0.048** — FROZEN F2 = 0.971 slightly BEAT oracle F2 = 0.923; both far above
  chance 0.50. The expected oracle >> frozen did not appear (`proxy_result.json`).

Root cause, confirmed two ways independent of the weak model:
1. The 12 novel NEG allomorphs come from a **disjoint inventory**, so under the frozen codec
   they fragment into 27 tokens that are **all neg-exclusive** (never in any plain affix);
   every allomorph has ≥2 neg-exclusive fragments.
2. The **last token alone** of a neg-body vs a plain-body separates the classes with **0
   overlap**. So the held-out flip is solvable by trivial **fragment-lookup** — no
   recombination, no atomicity — at ANY scale.

Therefore **Δ_pilot ≈ 0 would be a RIG DEFECT (frozen control too strong), not evidence about
F1.** The frozen arm is not a valid no-atomicity control: its fragments leak the NEG class.
This is the MORPH-ATOM story inverted — raw utf-8 (C1 = 0.617) failed because bytes are
maximally shared (no sub-unit carries class); a BPE-jamo frozen codec has class-exclusive
fragments, so it wins.

### What it changes (handed to a reframing analysis — `verification-h004-reframes-f1`)

- The pilot as designed cannot isolate the atomicity lever; the frozen arm needs
  class-AMBIGUOUS fragments (Q2 of the reframing brief) — if that is even constructible under
  BPE.
- It reframes F1 itself: L4(b) may have measured **representation-non-sharing**, not
  single-token **atomicity**. If a frozen BPE already achieves non-sharing, a refit organ may
  buy little — which sharpens, and may pre-empt, Δ_pilot's whole question.

### Resolution: STRUCTURAL TERMINAL — TWIN-REFUSED at $0 (no torch run needed)

The rig defect was repaired (donor-pair allomorphs + frequency balancing, genspec
`75b19bba…`) and the repair WORKED at order-1 — but revealed a deeper terminal. The `$0`
guard battery (`run_guards.py`):

| guard | value | reading |
|---|---|---|
| G-A last-token (order-1) lookup | **0.527** | PASS (≤0.55) — order-1 shortcut closed |
| G-B length-only lookup | 0.551 | marginal |
| **G-C order-2 bigram lookup** | **0.9954** | the frozen ceiling — TRIVIAL bigram path |
| G-D atomicity contrast | frozen 0/12, oracle 12/12 | PASS |
| G-E leak / co-occurrence | 0 / 0 | PASS |

**The theorem (verified 12/12): oracle-fusable ⟺ n-gram-recoverable.** For the ORACLE to
atomize an allomorph it must be a frequent FIXED jamo sequence — but then its terminal
n-gram under the FROZEN codec recovers it. Atomicity is not separable from n-gram binding
for a fixed morpheme; this is a fact about BPE, not a rig defect (Fable's Q2 predicted it).

A transformer binds order-2 with one attention head, so frozen F2 ≈ 0.995 regardless of
training → **Δ_pilot ≥ 0.20 is structurally impossible → TWIN-REFUSED.** Three converging
lenses: Fable's Q5 prediction, the deterministic G-C guard, and the earlier proxy
(frozen 0.971 ≥ oracle 0.923).

**Campaign result** (`verification-h004-campaign-result`, `cr-atomicity-not-isolable`): a
static codec's order-≤2 fragment statistics already deliver the write-lever's RECEPTIVE
value; a refit organ buys nothing measurable here. What the record ever isolated was NOT
atomicity — MORPH-ATOM's raw-utf8 control failed only because its ~18-byte binding span
exceeded the small model's n-gram reach. Per `rig-sequence-h004-kills` this forces a
campaign re-decision: F1's honest question moves to GENERATION / long-range credit /
continual-training interference (none of which a receptive flip-classification pilot can
see), or F1 yields first place — NOT a silent switch.

**No torch/MPS run was fired** — the $0 structural analysis is decisive, which is exactly
what research-before-real-measurement is for. The pilot spend was pre-empted by a guard
battery, not incurred and wasted.

_Terminal reached at $0. The verdict is TWIN-REFUSED-STRUCTURAL; the campaign re-decision is
the live frontier._
