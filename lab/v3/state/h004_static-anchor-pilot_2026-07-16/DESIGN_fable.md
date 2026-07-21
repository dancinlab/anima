# H_004 static-anchor-pilot design — verbatim Fable 5 (seed of record, not the SSOT)

- job fable-mrmm7mit · claude-fable-5 · 2026-07-16

---

All sources are in. One fact worth flagging before the card: I measured the actual codec compression on the real generator (frozen codec: 8.68 bytes/token on phase-2, oracle: 11.41), which pins token counts, step counts, and FLOPs — and the FLOPs answer is decisive: **this pilot does not need a rented GPU.** ~0.8 PFLOP/run at 4.9M params × ~28M tokens is 2–8 h overnight on the Mac mini's MPS at $0, with a <$2 RTX-4090 fallback. The ≤$10 envelope holds with an order of magnitude of margin.

Second flag: the "~10M params" label in `rig-model` silently assumed vocab 4–8k. At K=512 the same skeleton (6L·d256·8h) is **4.86M params exactly** — I keep the skeleton and correct the label rather than inflating the model to chase a stale number.

Here is the card-ready design.

---

```markdown
---
id: H_004
slug: f1-static-anchor-pilot
title: The static oracle-vs-frozen pilot at rig scale measures Δ_pilot — the hard upper
  bound on what codec-refit can deliver — anchoring delta_min in-rig so that H_002′ is
  powered by a same-substrate number, or killing the twin before a dollar is spent on it.
domain: write-lever axis (F1 codec-is-the-self) — successor to H_003 (rig = LICENSED 10/10)
status: pre-register-frozen
exploration_method: H_003 LICENSED + rig-pilot spec -> Fable 5 design pass (D1-D6)
verification_method: seeded-GPU training runs (explicit determinism exception per
  rig-determinism-exception) + deterministic harness (tool/anima_v3.py) + 7 pre-registered
  falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16            # ? — set at actual freeze
deterministic: false             # seeded-GPU; fixed seeds, logged env, verbatim stdout binding
llm: none
genspec_sha256: fbcf0c8ad444d0f3c2fa5ad018d12ce8f33ad6bcf8e0f78eb26be5495527ce2b
corpus_sha256: "?"               # sha256 of the canonical 300MB byte stream — frozen at build
config_sha256: "?"               # sha256 of trainer config — frozen after shakedown, before verdict runs
---

# H_004 — f1-static-anchor-pilot

## Hypothesis

The campaign's first non-$0 measurement. NOT a test of F1: both arms are STATIC (no refit
organ, no continual dynamics) — they differ ONLY in which frozen codec tokenizes the same
bytes. It measures:

> **Δ_pilot = F2(ORACLE) − F2(FROZEN)** on held-out-stem × novel-NEG forced-choice flips
> after the phase-2 drift — the ceiling of the codec effect at rig scale (10M-class,
> from-scratch, synthetic drill). ORACLE ≥ refit by construction: the oracle codec has
> phase-2 atomicity from step 0 and pays zero swap cost (`rig-pilot-measures`).

After this card, **no number transfers from MORPH-ATOM** — it survives only as the
existence proof of the mechanism class. `delta_min` for H_002′ is anchored in-rig as
Δ_pilot/2, closing the three gaps of `decision-attributability` (contrast, substrate,
corpus) at once.

Outcome set: **ANCHORED** (Δ_pilot ≥ 0.20 → H_002′ licensed with delta_min = Δ_pilot/2) ·
**TWIN-REFUSED** (Δ_pilot < 0.20 — a result, not a delay) · **PREMISE-DEAD** (oracle at
chance → campaign re-decision) · **INVALID** (liveness/sanity/leak failure — not a Δ=0 reading).

## Why

- H_003 = LICENSED 10/10: anchor green (M=109/120, replicated), generator produces the
  contrast (frozen deficit 1.0, refit 0.0, drift 0.1256, leak 0, 1536 clean items).
- `rig-pilot-kill-power` pre-commits the kill: below Δ_pilot = 0.20, delta_min < 0.10 →
  N > 1178/arm — deliverable only barely by the 1536-item pool and pointless: the ceiling
  is too low to detect the refit increment underneath it at the $25 budget.
- The genuine uncertainty is real, not ceremonial: the FROZEN arm still sees all phase-2
  flip supervision — a transformer can learn "this 6-jamo suffix → NEG" as a multi-token
  sequence. Whether single-token atomicity buys HELD-OUT-STEM recombination on top of that
  is exactly what MORPH-ATOM claims (slot-not-address) and exactly what has never been
  measured at this substrate. Δ_pilot could plausibly be 0.4 or 0.02.
- Per `l4-morph-atom-amplifier` (NAT-ATOM), the stream carries explicit flip marks; an
  oracle-at-chance reading is therefore attributable to the drill-scale premise, not to
  missing supervision — provided the arm demonstrably learned the drill (see F1 gate).

## Arms (D1) — 5 runs

All 5 runs train on the SAME canonical byte stream: phase-1 then phase-2, sequential, no
inter-phase shuffling. Stream = `stream(spec, phase, seed_offset=0)`, cut at first chunk
crossing 150,000,000 bytes per phase → total ≈ 300,000,000 bytes (exact count + sha256
logged and frozen as `corpus_sha256`). Arms differ ONLY in codec; no arm has a refit organ.

| run | arm    | codec                                                       | seed |
|-----|--------|-------------------------------------------------------------|------|
| 1   | ORACLE | `fit_bpe_jamo(sample_p1(10k lines) + sample_p2(10k lines), K=512)` | 101  |
| 2   | ORACLE | same codec (codecs are deterministic; refit once, reuse)     | 202  |
| 3   | FROZEN | `fit_bpe_jamo(sample_p1(20k lines), K=512)` — H_003's frozen codec | 101  |
| 4   | FROZEN | same codec                                                   | 202  |
| 5   | C3′ shared-ID liveness | FROZEN codec + deterministic remap: in every NEG-marked utterance, the affix span (longest-suffix match against all 16 NEG forms: 4 phase-1 + 12 novel) → one reserved token `NEGID`. Both phases. A phase-2 novel allomorph then literally IS the drilled phase-1 token. | 101  |

- Oracle's fit sample = 10k+10k lines so total fit-sample size (20k) matches frozen's —
  the codecs differ in WHAT they saw, not how much.
- Seeds are PAIRED across oracle/frozen: same seed → identical init tensors (V matched at
  543 in all arms, `NEGID` reserved-but-unused outside C3′ for parameter parity) and
  identical intra-phase shuffle → per-seed Δ isolates the codec.
- C3′ remap is definable because the emitted polarity mark is ground truth (`audit.py`
  precedent): only NEG-marked bodies are remapped; suffix match is unambiguous under
  longest-match (novel forms are 2-syllable; tie-break: longest, then lexicographic).

## Model + training (D2)

**Architecture** (identical across all 5 runs): decoder-only transformer, 6 layers,
d_model 256, 8 heads, d_ff 1024, RoPE, RMSNorm, no biases, tied embedding/head,
context 256 tokens, fp32.

- Vocab V = 543 = 30 base symbols (measured: jamo + marks + sentinel actually occurring)
  + 512 merges + 1 `NEGID`. Embedding 543×256 = 139,008.
- Params = 6·(4d²+8d²) + norms + embed = **4,860,928 ≈ 4.9M**. The `rig-model` "~10M"
  label carried a vocab-4–8k assumption; at K=512 the honest count is 4.9M. Skeleton kept,
  label corrected — parameter parity across arms is the load-bearing property, not the total.

**Data**: packed 256-token blocks, next-token CE on all positions, phase-1 blocks then
phase-2 blocks, shuffle within phase by run seed. Token counts FLOAT per codec on the
matched bytes (`rig-budget`) — measured on the real generator: oracle ≈ 11.68/11.41
bytes/token (p1/p2) → ≈ 26.0M tokens `?`; frozen ≈ 12.24/8.68 → ≈ 29.5M tokens `?`.
Exact counts logged; token caches (uint16) built once per codec.

**Optimizer**: AdamW β=(0.9, 0.95), wd 0.1, grad-clip 1.0, peak lr 3e-4 `?`, cosine to
3e-5, warmup 250 steps, batch 16×256 = 4,096 tokens/step → ≈ 6,350 steps (oracle) /
≈ 7,210 (frozen) `?`. One pass; no epochs.

**Hyperparameter discipline** (closes the "under-trained oracle kills the rig for the
wrong reason" hole without contaminating the eval): one designated SHAKEDOWN run (oracle
codec, seed 999, 30M bytes) may tune lr/batch/warmup against training loss and
F1-drilled ONLY — **F2 and every held-out item are never computed on it**. Final config
frozen as `config_sha256` before any verdict run fires.

**l10 check — the wrong-prior tax does NOT apply here, by construction**: every arm
trains from scratch under its own codec; no embedding ever crosses a codec boundary; no
warm-start, no checkpoint reuse, no cross-arm sharing. Embeddings init N(0, 0.02) from
the per-run seeded generator like every other weight. l10 taxes the REFIT organ — that
bill lands on H_002′'s adaptive arm, which is precisely why the oracle is the ceiling.

**Determinism exception** (`rig-determinism-exception`): fixed seeds, fp32,
`torch.use_deterministic_algorithms` where MPS supports it, logged env (torch version,
macOS build, chip), verbatim stdout binding, checkpoints + eval JSONs preserved under
`state/h004_f1-static-anchor-pilot_<date>/`. Bitwise reproducibility is NOT claimed.

## Eval (D3)

**F2** — the recovered H_9288 protocol: forced-choice flip, chance 0.50, teacher-forced
margin on the two label continuations (v1's exact scheme).

- Items: `eval_items(spec)` — all **1536** (128 held-out stems × 12 novel NEG; H_003
  measured n_clean = 1536/1536, ≥ n_required_worst 1178). Use the full pool: the pilot
  estimates a magnitude, so precision is the point (99% band half-width ±0.033 at n=1536).
- Per item: body = `to_jamo(render(stem, [affix if label==neg else plain]))`. Prompt =
  `SENTINEL + body + SENTINEL` (framing == stream framing exactly; v1 instrumentation
  bug #3 was this mismatch). Candidates = `to_jamo(POS_MARK)+SENTINEL` vs
  `to_jamo(NEG_MARK)+SENTINEL`, each encoded by THAT ARM'S codec; score total
  −log₂ P(candidate | prompt); pick the min; correct iff it matches `label`.
- **Codec fairness**: both candidates are 2 jamo + sentinel = 7 bytes — equal byte length
  by construction, so total-log-prob comparison IS the bits-per-byte comparison (salvage
  l6). No per-token quantity is ever compared across codecs. Any cross-arm CE diagnostic
  is reported via `bits_per_byte()` only, and per p7 no bpb number is a verdict.
- C3′ eval: same items; the neg body's affix span → `NEGID` (item metadata gives the
  affix; no ambiguity).

**F1** — drilled-stem sanity, per arm: 256 items, drilled stems × the SAME 12 novel NEG
allomorphs (composition seen verbatim in phase-2 training), same scoring. Gate ≥ 0.90
(expect ≈ 0.99). F1 vs F2 items differ ONLY in stem membership — so F1-high + F2-low
reads cleanly as "learned the drill, cannot recombine".

**Liveness rule**: F2(C3′) ≥ 0.90 (≥ 1383/1536) else the ENTIRE pilot is INVALID — not a
Δ_pilot = 0 reading. v1 precedent: a dead C3 converted four null arms into four
instrumentation bugs. Re-run C3′ whenever eval code changes.

## Criteria — the Δ_pilot decision rule

Exact counts, never rates (`gates-power-quote-counts`). k_X(s) = correct count of arm X
seed s over n = 1536.

- **Δ_pilot = (k_O(101)+k_O(202) − k_F(101)−k_F(202)) / 3072** — identical to the mean of
  paired per-seed deltas.
- **ANCHORED** iff no falsifier triggers AND k_O(101)+k_O(202) − k_F(101) − k_F(202) ≥ 615
  (i.e. Δ_pilot ≥ 0.20). Then, frozen before H_002′: delta_min := Δ_pilot/2;
  N := `two_proportion_n(0.5, 0.5 + delta_min)` — the script's printed value is binding;
  σ_seed(F2) := per-arm |k(101)−k(202)|/(1536·√2), fed to `gates-power-compound-rule`.
  Coherence check the kill was designed around: at Δ_pilot = 0.20 exactly, delta_min =
  0.10 → N = 1178 ≤ 1536 available — anything ANCHORED is powerable from the existing pool.
- Report per-seed F2 for all 5 runs, the paired per-seed Δs, and the 2-seed spread, in the
  verdict verbatim.

## Falsifiers (pre-registered, measurable)

- **P-1 the kill** (`rig-sequence-h004-kills`): k_O(101)+k_O(202)−k_F(101)−k_F(202) ≤ 614
  of 3072 (Δ_pilot < 0.20) → **H_002′ twin REFUSED**. The ceiling cannot power the twin.
- **P-2 drill-scale premise**: pooled oracle k_O(101)+k_O(202) inside the exact 99% chance
  band at n=3072 = **[1465, 1607]** (per-seed band at n=1536 = [718, 818], reported) →
  the mechanism class does not exist at this substrate even with atomicity handed for free
  → **campaign re-decision** (NOT a silent switch to F4). Interpretable only if P-4 passes
  for the oracle arms — chance + failed F1 is a training failure (P-4), not premise-death.
- **P-3 liveness**: k_C3′ < 1383/1536 → pilot **INVALID** (instrument cannot see a handed
  flip; no arm's reading means anything).
- **P-4 drill sanity**: F1 < 231/256 (0.90) in any verdict arm → that arm never learned
  the drill → arm VOID → pilot **INVALID** (Δ needs all four).
- **P-5 leak on the actual trained corpus**: `leak_scan` (all 1536 rendered eval surfaces)
  + `heldout_neg_cooccurrence` re-run at FULL depth on the exact canonical 300MB (H_003
  audited 200k lines/phase; training uses ≈ 3.4M lines/phase) → any hit → **INVALID**
  (the eval would measure memory, not recombination — `l6-leak`).
- **P-6 seed instability**: |k(101)−k(202)| ≥ 154/1536 (spread > 0.10) in oracle or frozen
  → 2-seed mean untrustworthy → pre-registered escalation: add seed 303 to BOTH verdict
  arms (~$0) before reading P-1; if still ≥ 154 → **PENDING(seed-power)**, Δ_pilot not
  quotable.
- **P-7 config identity**: the 4 verdict runs must share `config_sha256` and
  `corpus_sha256`, differing only in {codec, seed}; genspec_sha256 must equal `fbcf0c8…`;
  C3′ differs additionally only in the remap. Any mismatch → **INVALID**.

## Predictions

- **P1**: oracle F2 ≥ 0.70 `?` (anchor analogy M = 0.908; genuinely uncertain at 4.9M
  from-scratch).
- **P2**: frozen F2 above the multi-token floor but well below oracle `?` — the one
  quantity nothing in the record constrains; this is what the pilot is FOR.
- **P3**: F2(C3′) ≈ 1.0; **P4**: F1 ≥ 0.98 all arms; **P5**: σ_seed(F2) < 0.03 `?`.

## Compute path (D5)

- **FLOPs**: 6·P·T ≈ 6 × 4.72e6 × 28e6 ≈ **0.8 PFLOP/run**, ×5 ≈ 4 PFLOP total `?`.
- **Primary: Mac mini MPS, $0.** fp32, ~5–40k tok/s expected `?` → 12 min–1.6 h/run,
  5 runs = 1–8 h → overnight. Data build (one-time): stream gen ~5 min; pure-Python BPE
  encode is the slow step (~10–30 min/codec `?`) — cache uint16 token arrays (~60MB/arm).
- **Fallback: one RTX 4090 via `hexa cloud`** if measured MPS throughput < 5k tok/s or
  fp32-on-MPS misbehaves in the shakedown: all 5 runs < 1 h, **≤ $2**. Either path is
  inside the ≤$10 envelope with ≥5× margin. **There is no honest need for GPU spend; the
  card claims $0 (MPS) with a ≤$2 escape hatch — no $0-pretending required.**
- **Byte budget: keep the full 300M.** A 30M-byte pilot would still fit the codecs
  (≈11k occurrences per novel allomorph) but gives only ≈ 700 optimizer steps — squarely
  in the regime where an oracle-at-chance reading is an optimization artifact, i.e. the
  NAT-ATOM amplifier concern realized as a false P-2. The cost argument for shrinking
  evaporates at $0; the risk argument against it does not. The shakedown run doubles as
  the throughput measurement.
- **Trainer home**: the minimal trainer is a from-scratch decoder-only transformer +
  AdamW + packed-block loader + forced-choice/bpb eval (~350 lines of PyTorch). Per
  demiurge d3 it goes in the **hexa-lang stdlib** (it has ≥3 known consumers: H_004,
  H_002′'s 12 runs, and F3/F5 rigs), consumed here by a thin run script in
  `state/h004_…/run_h004.py` that owns only spec-wiring and the falsifier ledger. If the
  stdlib cannot host a torch dependency, a local `src/trainer/` is acceptable FOR THE
  PILOT with an explicit upstream-fix debt note — do not let the implementation-home rule
  block the campaign's first measurement (l8: rules without escape valves get bypassed).

## Honest Limits (D6)

- **L1 — a ceiling, not the effect.** Δ_pilot is what refit could AT MOST deliver: the
  oracle pays no swap cost, no l10 destroy-and-rebuild tax, no continual-training
  interference. The pilot says nothing about whether the refit organ can harvest any of
  the headroom (H_002′'s question) and nothing about identity ("idiolect = self" —
  the ~300M natural-stream claim).
- **L2 — one designed language.** Δ_pilot is a property of THIS drill: explicit polarity
  marks, NOVEL_NEG_SHARE_P2 = 0.80, 512 stems, K = 512. The genspec hash bounds shopping
  but the spec's author wants F1 to live, and the spec was shaped by reading the anchor's
  protocol (H_003 L4 carries over verbatim).
- **L3 — 2 seeds.** σ_seed from 2 samples/arm has ~±75% relative error on σ itself `?`;
  it enters H_002′'s compound rule as a sanity floor, not a variance estimate. Paired
  seeds shrink the Δ noise but n_seeds = 2 is the pilot's cheapness showing.
- **L4 — scale is 4.9M, measured nowhere else.** Not 10M-as-labeled, not 303M-as-anchored.
  Transfer in either direction is unestablished; `l4-morph-atom-slot-not-address` remains
  an argument, not a measurement.
- **L5 — byte-matching subsidizes frozen.** Same bytes → frozen sees ≈ 13% more tokens
  (8.68 vs 11.41 bytes/token on phase 2) → more gradient steps. Biases Δ_pilot DOWN —
  conservative for the kill (won't overbuy the twin), but a true ceiling modestly above
  the measured one is possible.
- **L6 — receptive metric.** Mark-classification measures the flip relation receptively;
  nothing about generation. The marks are trivially frequent tokens in every arm — all
  item difficulty lives in the held-out body composition, by design, but that design is
  itself part of the rig, not of F1.

## Cross-Links

- **architecture**: `rig-pilot` (+ `-measures`, `-derives`, `-kill-power`) ·
  `rig-sequence-h004` / `-kills` · `rig-liveness-c3-prime` · `rig-drift-breaks-symmetry` ·
  `rig-atomicity-not-induced` (BROKEN) · `gates-power-table` · `rig-determinism-exception` ·
  `l10-codec-swap-costs-the-embedding` (why oracle ≥ refit) · `l4-morph-atom-*`
- **predecessor**: H_003 (rig = LICENSED 10/10) · **successor**: H_002′ (12 runs, ≤$25,
  fires only on ANCHORED)
- **generator**: `src/generator/` (genspec `fbcf0c8…`, K=512) · **harness**:
  `tool/anima_v3.py` (`chance_band`, `two_proportion_n`, `bits_per_byte`)
- **v1 precedent**: `anima/state/nbind_curriculum/MORPHATOM_STAGE2_SPEC.md` (forced-choice
  margin scoring, C3 liveness rule, F1 sanity gate — all inherited here)
```

---

Design notes outside the card, briefly:

- **The one number I could not pre-compute honestly is frozen-arm F2.** The frozen arm still gets full phase-2 flip supervision (multi-token affix → NEG mark), so it is not doomed to chance the way MORPH-ATOM's raw-UTF8 C1 was — a transformer can learn a 6-jamo suffix as a sequence. That makes the 0.20 kill genuinely live rather than ceremonial, and it's why I wrote P2 as the card's declared uncertainty rather than predicting a chance-level frozen arm.
- **Exact count thresholds** all come from the licensed harness: chance band [718, 818]/1536 per seed, [1465, 1607]/3072 pooled; kill at pooled oracle−frozen ≤ 614; liveness ≥ 1383/1536; N(0.10) = 1178 confirming the 0.20 kill line is exactly where the twin becomes powerable from the 1536-item pool.
- **Two additions beyond the task's minimum** that I'd defend: the paired-seed scheme (same seed → identical init + shuffle across oracle/frozen, so each seed yields a clean within-pair Δ), and the shakedown-run rule (hyperparameters may be tuned only against training loss and drilled-stem F1, never F2 — closing the "under-trained oracle fires P-2 falsely" hole without contaminating the held-out eval).
- **Compute conclusion, stated plainly:** no GPU rental is needed. 5 runs ≈ 4 PFLOP total runs overnight on the Mac mini at $0; a ≤$2 4090 fallback exists if MPS throughput measured in the shakedown is under ~5k tok/s. The ≤$10 claim in `rig-sequence-h004` is safe by at least 5×.