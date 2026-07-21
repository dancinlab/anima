Registry and template checked — this becomes card `H_003` in the existing pre-register format. Spec follows.

---

# H_003 — atomicity-fixed-codec-drill (pre-register spec)

**Claim**: an atomic negator token in a fixed jamo-BPE codec *causes* held-out negation recombination. One variable: the encoder's span policy. No adversary, no learned codec, $0 target.

---

## 1. THE ONE-VARIABLE CONTRAST

The hint is **right in mechanism, wrong in construction**. Two forced merge *tables* = two vocabularies = two variables (alphabet + atomicity). Instead: build **ONE shared vocabulary V\***, vary only the **encode-time span policy**. Merge table, token ids, vocab size, corpus text, model, steps, seed: byte-identical across arms.

**V\* construction (once):**
1. Jamo-decompose NSMC (distinct cho/jung/jong markers), within-eojeol frequency BPE, min pair count 5, K=2048 (v1's audited K).
2. Replace the 5 lowest-frequency merges with **forced atomic tokens**: `안`(free eojeol), `못`(free eojeol), `않`, `못하`, `아니` (no-op where frequency already fused them). |V\*| stays 2048.
3. Fixed-width 2-byte re-encode, as v1.

**Encode-time policy (THE variable):**

| arm | vocab | negator-span encoding | everything else |
|---|---|---|---|
| **A-atom** | V\* | standard greedy merge → atomic tokens fire | identical |
| **A-shat** | V\* | spans matched by the negator span-matcher are emitted as **base jamo singletons** (all merges suppressed inside the span; within-eojeol BPE already prevents cross-span merges) | identical |

- Span-matcher (pre-registered, applied to jamo stream): free = whole eojeol ∈ {안, 못}; bound = jamo runs of 않 / 못하 / 아니 within an eojeol. Exact jamo strings `?` — G-0 audit must print matched-span counts per form before freeze.
- Policy applies to **CPT corpus, drill corpus, and eval panels alike** within an arm (encoder consistency; v1's false-negative rule: embed+readout init from scratch in both arms — moot here, both are codec arms trained from scratch, see §5).
- Corpus delta between arms: **only** tokens inside matched spans differ. Expected fraction of corpus tokens affected ≈ 3–5% `?` — audit prints the exact number; if >10%, flag.
- v1 M-vs-C1: confirmed NOT the contrast (varies codec existence). This pair holds codec fixed.

Why atomic tokens sit in V\* even for A-shat: identical alphabet is the point. In A-shat those 5 ids occur 0 times (audit assertion) — untrained embeddings, never scored.

**Secondary dose arm** (run only if F1 passes): `C-syl` = same V\*, negator spans encoded at syllable granularity (2–3 tokens). Predicts monotonicity atom ≥ syl ≥ shat.

---

## 2. THE CEILING PROBLEM

v1's panel died because the control (a codec arm) sat at 0.90 with ceiling 0.9167. Fix: make the panel **heuristic-neutral by construction** so any non-individuating strategy scores exactly 0.5, via depth-parity minimal pairs.

**Gold bit**: `pol(V) XOR (negator_count mod 2)`. Every negator form flips once. Depth-2 = net no-flip.

**The anti-heuristic construction**: D1 and D2 items are **minimal pairs sharing the same template tail**, differing only in presence of the inner negator:

| depth | template (past-decl conj shown) | gold |
|---|---|---|
| D1 | `이 영화 {V}지는 않았다 => ` | ¬pol |
| D2 | `이 영화 {NEG} {V}지는 않았다 => ` | pol |

Template shape does not reveal parity — the `…지는 않았다` tail appears in both. Discriminating D1 from D2 requires **detecting and individuating the inner negator token**. Consequences:

- **Presence heuristic** ("any negator ⇒ flip"): right on D1, wrong on D2 → **0.500 exactly** on a 50/50 D1/D2 panel. Verified closed-form in the panel audit (F7), before any training.
- **Template-shape heuristic**: D1/D2 share shape → 0.500.
- **Expected control (A-shat)**: 0.50–0.60. Grounds: (i) v1's shattered-negator representation (raw utf-8, arm C1, `vC1_f2` record) scored 0.5750/0.6167 on the *easier* D1-only panel; (ii) on this panel every strategy short of instance-level negator individuation is pinned to 0.5 by construction. It does not land near 0.9 because the 0.9 arms in v1 all had atomic negators — that is precisely the hypothesis.
- **Headroom**: operational ceiling = f1′(A-atom), expected ≥0.90 (v1 precedent). 0.90 − 0.55 = **0.35 headroom** vs v1's 0.083.

**Drill grid** (못 appears 0 times anywhere in it):

| cell | surface | gold | forms drilled |
|---|---|---|---|
| D0 | `{V}{conj}` | pol | — |
| D1-free | `{V-nom} 안 했{conj}` / `안 {V}{conj}` | ¬pol | 안 |
| D1-bound | `{V}지 않았{conj}` | ¬pol | 않 |
| D1-long | `{V}지는 않았{conj}` | ¬pol | 않 |
| D1-아니 | `{V}ㄴ 것은 아니다` | ¬pol | 아니 |
| D2-a | `안 {V}지는 않았{conj}` | pol | 안+않 |
| D2-b | `안 {V}ㄴ 것은 아니다` | pol | 안+아니 |

16 verb stems (8 pos / 8 neg, see §3) × 3 conjugations ({했다, 했어요, 했음} register set) × 7 cells ≈ 336 lines, interleaved into the NSMC stream (interleave ratio as v1 `?`), real-byte left context as v1. Drill 2.5k steps ≈ 60+ epochs.

**Eval scoring**: unchanged v1 discipline — forced choice `긍정.` vs `부정.`, NLL from first divergence point **in the arm's own encoding**, real-byte left context.

---

## 3. THE OOD BLIND SPOT

**Held-out negator switches from 아니 to 못.** Grounds: 못 has natural free (`못 {V}` / `{V-nom} 못 했다`) *and* bound (`{V}지 못했다`) forms; 아니's free form (`아니 {V}다`) is archaic → OOD garbage in the panel. v1's own source pre-registered this contingency verbatim. DRILLED = {안, 않, 아니}; HELD = 못 (0 occurrences in drill grid; present in NSMC CPT corpus — that is where atomicity acts, per C2 pretraining-exposure null).

**f2′ panel — 4 cells, fully crossed, same 16 verbs in every cell** (predicate identity constant; the bound/free contrast is morphology only):

| cell | depth | form | surface | gold | n |
|---|---|---|---|---|---|
| A | D1 | **free** | `{V-nom} 못 했{conj}` | ¬pol | 48 |
| B | D1 | **bound** | `{V}지 못했{conj}` | ¬pol | 48 |
| C | D2 | **free** | `못 {V}지는 않았{conj}` | pol | 48 |
| D | D2 | **bound** | `{V}지 못한 것은 아니다` | pol | 48 |

16 verbs × 3 conj = 48/cell, **n=192 total**. 50/50 label balance per cell (8 pos / 8 neg stems). D1:D2 = 50:50 → presence heuristic = 0.5. Outer negators in C/D (않, 아니) are drilled; the *recombination* is the held-out 못 in the inner/only slot.

**f1′ sanity panel**: same 4-cell structure with 안/않 in the held-out slot positions, held-out 4th conjugation (`-네요`), 16 verbs × 4 cells = 64.

**Verb inventory** (must survive G-1 grammar audit — 못 requires volitional verbs; every stem × template cell judged natural by operator pre-freeze, else stem dropped; minimum 12 survivors, n scales down accordingly):
- pos: 웃다? , 즐기다, 몰입하다, 집중하다, 공감하다, 추천하다, 이해하다, 기대하다?
- neg: 졸다, 하품하다, 딴생각하다, 딴짓하다, 후회하다?, 딴청부리다?, 중간에 끄다?, 돌려보다?
`?` = polarity-in-review-context or 못-compatibility unverified. 하다-compounds use the split form `{N} 못/안 했다` for free cells (uniform template).

---

## 4. ADMISSIBILITY — falsifiers (frozen)

Expected values used in arithmetic: control (A-shat f2′) **E=0.55**; operational ceiling (f1′ A-atom) **E=0.90**; metric ceiling 1.0; chance 0.5; n=192 → 95% binomial CI ±0.071; per-cell n=48 → ±0.14.

| id | condition (trigger = FALSIFIED / DEAD) | threshold | reachability arithmetic |
|---|---|---|---|
| **F1** primary | Δ = d_acc(A-atom, f2′) − d_acc(A-shat, f2′). SUPPORTED iff Δ ≥ **0.15** at both seeds; DEAD iff Δ < 0.05 at both; else PARTIAL | 0.15 | 0.15 ≤ ceiling−control = 0.90−0.55 = 0.35 ✓. Worst admissible case (ceiling 0.85, control 0.60): 0.25 ≥ 0.15 ✓. v1's dead gate had 0.083 < 0.1 ✗ — this one is 2.3× inside headroom. Both answers reachable: Δ<0.05 needs only A-atom ≈ A-shat. |
| **F2** liveness/ceiling | f1′(A-atom) < **0.85** ⇒ measurement DEAD, no F1 verdict issued (v1 C3 role) | 0.85 | v1 codec-arm f1 precedent ≥0.90; failure reachable (v1 no-codec f1 was far lower). |
| **F3** not-free | f2′(C-scaf: CPT only, **no drill**) > **0.60** ⇒ grid leaks, scaffolding alone clears | 0.60 | expected 0.50; 0.60 = chance + 3.4σ (σ=0.029 at n=192) — clears only by real leak, not luck. |
| **F4** negative control | f2′(C-perm: drill with permuted gold bits) ∉ **[0.40, 0.60]** ⇒ harness/label leak | ±0.10 band | band = chance ± 3.4σ; both exits reachable trivially. |
| **F5** OOD bound/free | given F1 passes: per-cell Δ(atom−shat) < **0.10** in any of cells A–D, consistent in sign across both seeds ⇒ verdict restricted to passing morphology (PARTIAL, not full SUPPORTED) | 0.10/cell | per-cell headroom 0.35 ≥ 0.10 ✓; per-cell CI ±0.14 > 0.10 → single-seed underpowered, hence the both-seeds-same-sign requirement `?` (power is the honest limit here). |
| **F6** placebo | d_acc(A-atom, f2′) − d_acc(C-plc, f2′) > **0.05** ⇒ effect is generic encode-disruption, F1 pass VOID | 0.05 | C-plc = V\*, shatter policy on a frequency-matched non-negator morpheme (candidate 진짜 `?`; audit must show freq within 2× of total negator-span freq, label-correlation ≈ 0). |
| **F7** panel bounds (pre-training, closed-form) | presence-heuristic simulated score on frozen f2′ ≠ **0.500 ± 0.02**, or per-cell label balance ≠ 50/50 | exact | deterministic audit in `tool/anima_v4.py` before any training; if it fails, grid is rebuilt, nothing runs. |
| **F8** exposure match | \|BPB(A-atom) − BPB(A-shat)\| on held-out NSMC > **0.15** `?` ⇒ arms not difficulty-matched, confound flag | 0.15 | BPB and d_acc reported **separately per arm, never summed** (p7). |

Every reported number carries `(arm, seed, panel, state-path)` — e.g. `A-shat s0 f2′ state/h003_.../result.json#arms.A-shat.s0.f2` (name-the-arm).

**Arms roster** (per seed): A-atom, A-shat, C-plc, C-scaf, C-perm, [C-syl conditional]. CPTs needed: 3 (atom-encoding shared by A-atom/C-scaf/C-perm; shat; placebo).

---

## 5. COST + SMALLEST VALID CONFIG

**Answer: (a) shrink, run local MPS. Do not rent for the first pass.**

| param | value | note |
|---|---|---|
| model | CLMConvMoE **d=384, L=4, V=256** (2-byte codes) | v1 OMEGA measured **scale-STABLE** behavior d384→d1024 → a d384 positive/negative is meaningful; the L4b effect size (0.90 vs 0.60) is not a subtle-margin effect (H_002 confirmed margins are gross) |
| params | ~15–25M `?` | exact count printed at init, frozen into result.json |
| base ckpt | **none — from scratch** | 388M clm303 is unusable (d mismatch; embed+readout reinit was mandatory for codec arms anyway); C2 verdict (pretraining exposure irrelevant, 0.9167 unchanged after scrub) licenses from-scratch |
| seq_len | 512 | |
| CPT | 8k steps, batch 16 | NSMC 150k lines, per-arm encoding |
| drill | 2.5k steps | v1 value kept |
| seeds | 2: {0, 1} | v1 replication standard |
| steps/seed | 3×8k + 4×2.5k = 34k | +10.5k if C-syl triggers |
| wall-clock | ~3–5 it/s on MPS `?` → **3–4 h/seed, 6–8 h total** | 25M @ 16GB RAM: no swap pressure, unlike 388M |
| $ | **$0** | |

**Escalation trigger (pre-registered, not discretionary)**: if F2 fails at seed 0 (f1′ < 0.85 at d384), the small model can't learn the drilled task → rent 1× A10/4090 via `hexa cloud`, rerun at d=1024 only, est. ~3 GPU-h, **<$5** `?`. No other condition justifies renting.

---

## 6. WHAT WOULD MAKE ME NOT RUN THIS

**Most likely convincing false positive**: A-shat loses **not** because atomicity enables composition, but because shattering *any* high-frequency morpheme into shared jamo singletons degrades its representation generically (embedding interference: the negator's jamo tokens carry thousands of unrelated contexts). Δ appears, replicates at both seeds, looks exactly like the predicted result — and would appear identically if we had shattered 진짜. **Catch: C-plc / F6** — placebo-shatter a frequency-matched non-negator; if A-atom − C-plc > 0.05, the F1 pass is void by pre-registration, not by post-hoc judgment. This arm is not optional.

Don't-run gates (any → stop before training): F7 panel audit fails; G-0 codec audit fails (round-trip <0.98, negator tokens not pairwise disjoint, atomic ids nonzero in shat-encoded corpus); G-1 grammar audit leaves <12 verbs; matched-span count for 못 in NSMC < 500 `?` (too rare → atom embedding undertrained for a different reason than the hypothesis).

Known residual weakness (accepted, logged as honest limit): A-shat's unmerged jamo runs are distributionally anomalous — a "neon sign" marking negators. Sign points the *helpful* direction (would shrink Δ, biasing toward DEAD, i.e., conservative), and C-plc carries the same anomaly. Second limit: F5 per-cell power (±0.14 CI vs 0.10 threshold) — bound/free verdict is 2-seed-sign-gated, weaker than F1.

---

Card skeleton: `HYPOTHESES/cards/H_003_atomicity_fixed_codec_drill.md`, status `pre-register-frozen`, registry tier `⚪ PRE-REGISTERED`; audits + panel construction in `tool/anima_v4.py`; run artifacts under `state/h003_atomicity_fixed_codec_drill_<date>/`. Everything marked `?` must be resolved and frozen **before** `frozen_at` is stamped; nothing marked `?` is a tunable after that.