# F3 diary twin design (H_006 gate + H_007 twin) — verbatim Fable 5 (seed of record)

- job fable-mrmp3epa · claude-fable-5 · 2026-07-16

---

All sources read (H_005 card + run + result, the SSOT nodes, the re-decision, `nlm.py`). Here is the design.

---

# H_007 `f3-diary-twin` — design (card-ready)

**TL;DR / the D4 answer up front:** the twin genuinely needs neural training — gradient-through-the-write is not simulable by any $0 counting estimator, and the one numpy trainer on hand (`nlm.py`) is already proven the wrong tool (mean-pooled, can't represent a long-range day token). But it does **not** need rented compute: a ~4–5M-param byte transformer on the local Mac (torch/MPS) does it in ~12 h wall-clock, **$0 cash** (rental fallback ~$5). And there IS a $0 closed-form precursor that must run first — **H_006 `f3-bounded-oracle`** — which both gates the training spend and *manufactures the twin's oracle arm inputs*. Recommended sequence: **H_006 ($0, CPU, ~hours) → H_007 (the twin, MPS, $0 cash)**.

---

## D1 — Arms

Geometry inherited verbatim from H_005 for anchor comparability: `W=4096` tail, `P=2048` prefix, day-chunks = `day_chunks()` (messages + `--name-only` paths). Streams: **anima** (43 pairs, verdict-bearing — the strict anchor) + **hexa-lang** (101 pairs, confirm-only). sidecar excluded (21 days, under-powered null in H_005).

All trained arms share **identical architecture, identical parameter count, identical steps/lr/data order per seed** — the only difference is what the writer reads:

| # | arm | m = | trained? | role |
|---|---|---|---|---|
| A1 | **DIARY** | `Writer(day_t[:-W]`, truncated to first 16 KB `?`) | full joint | the claim |
| A2 | **NO-DIARY** | `Writer(CONST)` — a fixed canonical 16 KB placeholder string | full joint | control; day-blind by *input*, not by architecture, so params/gradient-path match exactly |
| A3 | **ORACLE-SELECT** | `Writer(H_006 extract of day t, ≤1024 B)` | full joint | ceiling: selection given by hindsight, encoding still learned |
| E1 | **SWAP** | A1 checkpoint, eval with `m(t−2)` (H_005's `j=i−2` convention) | eval-only | L2 day-specificity on the *learned* m |
| E2 | **ABLATE** | A1 checkpoint, eval with m ← mean-m over train days | eval-only | base-term ablation (`f3-falsifier-ablation`) |
| E3 | **ORACLE-TEXT** | trained trunk, eval bpb(P \| tail + extract-as-bytes) | eval-only | cross-check A3 against H_006's estimator-based ceiling |

Training data: stage-1 trunk pretrain on the concatenated stream bytes (both streams, ~5–10 MB `?`); stage-2 joint (writer+trunk) on train day-pairs of both streams pooled. Split per stream, chronological: **60 % train / 10 % val (early-stop only) / 30 % test** → anima 26/4/13, hexa 60/10/31 test pairs. Test days are **never gradient-touched** (this is the fresh-eval-latent closure, D6-1). Seeds ×3 per trained arm → 9 stage-2 runs.

**Metrics** (median over test pairs, then median over seeds — mirrors `gates-power-compound-rule`):
- `lift_learned = bpb_A2 − bpb_A1`
- `lift_oracle = bpb_A2 − bpb_A3`
- `gap_swap = bpb_E1 − bpb_A1` · `gap_ablate = bpb_E2 − bpb_A1`

## D2 — Bottleneck architecture

**m = continuous, k=8 slots × d=256 dims** (primary). Not discrete tokens: Gumbel/straight-through adds a failure mode orthogonal to the load-bearing question (does a learned bottleneck transport day-specific MI). Honest cost stated in D6-4: continuous m is not a readable diary; a positive licenses the discrete-token card next, and discretization can only lose bits (this twin is necessary, not sufficient, for the k-token diary).

- **Trunk (shared, all arms):** byte-level causal transformer, vocab 256, L=4, d_model=256, 4 heads, FFN 1024 ≈ 3.2 M params.
- **Writer:** 2 cross-attention blocks; k=8 learned query slots attend over the trunk-encoded writer input → m ∈ R^{8×256} ≈ +1 M params.
- **Consumption:** reader sequence = `[m₁…m₈][tail 4096][P 2048]` (6152 positions); m injected as 8 prefix embeddings; CE loss on P positions only (tail LM loss at weight 0.1 to prevent trunk forgetting `?`).
- **L3 gradient path:** CE(P) → reader attention → m slots → writer cross-attn → writer encoder. Fully differentiable, no estimator tricks — the diary sits *inside* the loss graph. L11 escape is structural: at prediction time the information in m (day t beyond the tail) is **physically absent from the visible context**, so no within-context statistic of any order substitutes for it (`l11-design-consequence`).
- **L2 threat (`f3-l-check`: the head eats the diary):** guarded by E1 + E2 against θ_L2 (D3), not by hope.
- **k sweep:** k=8 verdict-bearing. k ∈ {1, 32}, DIARY arm, 1 seed each — a curve, not a verdict (k=1 is the deliberate near-collapse probe).

## D3 — L1 / L2 gates, operational

- **L1 seam rank:** matrix M ∈ R^{N×2048} of flattened m-vectors over all val+test days (N ≥ 20), mean-centered; `PR = participation_ratio(singular_values(M))` (existing `tool/anima_v3.py`). **Gate: PR > max(2.0, null_99)**, null_99 = 99th pctile of PR over 1000 draws of rank-1-signal + iid noise matched to residual energy, fixed seed, frozen in code before A1 evaluates (`l6-frozen-truth-table`). PR ≤ gate → m collapsed to the v1 one-bit seam → DEAD regardless of any lift.
- **L2 decoration threshold:** θ_L2 = **max(5·σ_seed, 0.004 bpb)** — inherited formula (`gates-l2-threshold`); σ_seed = std of test bpb across the 3 **NO-DIARY** seeds, measured and frozen before any DIARY-arm eval. Both `gap_swap` and `gap_ablate` must exceed θ_L2.
- Two thresholds, both derived: 0.004 = 10× OMEGA's decoration signature; the kill threshold δ_min (D5) comes from H_005's ceiling.

## D4 — Compute, honestly

**Can a minimal $0/CPU version run?** No — not the twin itself, and the reasons are structural, not budgetary:
1. The write must be *learned by gradient through the bottleneck*. markov6/ppm/gzip are counting estimators — no gradient, no write. They measure ceilings (H_005/H_006's job), they cannot learn extraction.
2. The reader must be order-aware at long range to even *see* the 0.02-bpb-class signal; `nlm.py` is mean-pooled over an 8-token window and was formally disqualified in H_005 for exactly this. A hand-backprop numpy attention model over 6k-byte sequences is weeks of error-prone work to avoid a $0-cash torch run — false economy.

**What it needs — exact minimal spec:**

| item | value |
|---|---|
| model | 4–5 M params (trunk 3.2 M + writer ~1 M), byte-level, ctx 6152 |
| data | stage-1: ~10–20 M bytes (2 epochs over streams `?`) · stage-2: ~137 train pairs × 6.2 KB × ~50 epochs ≈ 40 M tokens/run |
| runs | 3 seeds × stage-1 (shared across arms) + 9 × stage-2 |
| wall-clock | MPS @ ~10 k tok/s `?`: ~1 h/stage-2 run → **~12 h total, $0 cash** |
| fallback | if MPS throughput disappoints: 1× A10 spot ≈ $0.75/h × ~4 h ≈ **$3–5** |

The campaign has earned this: the premise is anchored (H_005), δ_min is pre-anchored, and 실측전-research is satisfied. The "first genuine spend" the SSOT anticipated (`h005-twin-compute`) turns out to be wall-clock, not dollars, at this scale.

**But a $0 closed-form precursor gates it — run this first.**

### H_006 `f3-bounded-oracle` ($0, CPU, next card)

H_005's own honest-limit L1 says it: the anchored ceiling is the ceiling of an **unbounded** diary; nothing yet shows a k-**bounded** extract retains it. Before training a model to *learn* extraction, measure whether hindsight extraction at budget k can capture the ceiling at all:

- **Method:** per day-pair, score each line of `day_t[:-W]` by marginal lift under markov6 (primary; ppm confirm; gzip reported); take top-lines up to budget k ∈ {64, 256, 1024, 4096} bytes → `ceiling(k) = bpb(P|tail) − bpb(P|tail+extract_k)`, vs the same shuffle floor. One optional greedy-refinement pass `?`. All H_005 machinery reused verbatim.
- **Verdict asymmetry, stated:** top-k/greedy is a *lower bound* on the true bounded oracle — a positive is an existence proof (decisive); a null is only suggestive (could be greedy's fault), in which case the twin's A3/E3 arms become the decider.
- **Kill:** ceiling(4096) − floor ≤ ε=0.02 on **both** anchored streams → the MI exists but is incompressible below context scale → bounded-diary premise REFUSED, twin cancelled, $0 spent.
- **Liveness:** planted-latent stream — extract at k ≥ block size must recover ~the full 7.79-bpb ceiling.
- **Artifact chaining:** the winning extracts are written to `state/h006…/extracts/` and are **literally the ORACLE-SELECT inputs** of the twin. The precursor doesn't just gate the spend, it builds the ceiling arm.

**Recommended sequence: H_006 ($0) → H_007 (twin).**

## D5 — Falsifiers (pre-registered) + verdict rule

δ_min := **max(0.02 bpb, lift_oracle/2)** — floor 0.02 = the conservative end of H_005's ceiling/2 range [0.015, 0.11]; the twin's own oracle arm (A3) pins the point value, exactly as H_005 pre-committed.

- **T-0 instrument floor (bounds):** trained trunk's bpb(P|tail) on test pairs must be ≤ the ppm estimator's same quantity → else the reader is a worse instrument than the $0 tools → **INVALID**, no other number interpretable.
- **T-1 THE KILL:** `lift_learned ≤ δ_min` on anima (and unconfirmed on hexa-lang) while T-2 passes → the learned diary cannot capture what hindsight can → diary is decoration → **F3 FALSIFIED** (and F8's diary organ demoted with it).
- **T-2 oracle liveness (blind-tool control):** `lift_oracle < 0.02` → the reader can't consume even the hindsight extract at this capacity → **INVALID** (instrument, not F3 — this is what makes a null attributable; `l6-blind-tool`).
- **T-3 L1 seam rank:** PR(m over eval days) ≤ max(2.0, null_99) → one-bit seam → **DEAD** even with positive lift.
- **T-4 L2 swap:** `gap_swap ≤ θ_L2` → m carries generic register, not day content → decoration → **kill** (H_005 P-5 precedent: counts as kill, not support).
- **T-5 L2 base ablation:** `gap_ablate ≤ θ_L2` → reader ignores m → decoration → **kill**.
- **T-6 leak/dedup:** any 64-byte window of a test-day P occurring verbatim in a training-pair target → drop pair; >20 % `?` of pairs dropped → **INVALID** (train/eval contamination, `l6-leak`).
- **T-7 seed agreement:** lift_learned > 0 on ≥ 2/3 seeds AND median-over-seeds clears δ_min; sign-split across seeds → **PENDING(power)**, add seeds before interpreting.

**Verdict rule:** SUPPORTED iff T-0, T-2, T-6 pass AND no kill (T-1/T-3/T-4/T-5) triggers AND lift_learned > δ_min on anima with T-7 agreement. hexa-lang: confirm-only (strict-anchor discipline from H_005 carries over). Lift in (0.02, lift_oracle/2) exactly at boundary → 🟡 PARTIAL, honestly reported.

## D6 — Honest limits (≥3)

1. **Weight channel:** joint training could smuggle day-latents into weights. Closed by construction: test day-pairs are never gradient-touched, so weights cannot contain test-day-specific values — they can carry the transport *protocol* and project-generic priors (present in both arms, differenced out); E1-swap on fresh test days separates protocol from value. Residual: slow project-level drift means test days are distributionally "later" than train days — this depresses all arms equally `?` but could shrink the absolute lift.
2. **Git-stream proxy:** a developer's commit stream ≠ an agent's experience stream. A positive proves bottlenecked transport of a day-specific temporal self *on this substrate*; the "individual" compressed is the developer-project system, not an agent self. Same limit as H_005 L2, inherited unreduced.
3. **What a null kills / doesn't:** FALSIFIED kills "a small learned writer captures hindsight-capturable day MI at this capacity and data scale" — F3's minimal organ. It does **not** kill H_005's premise (the MI exists), nor writers at larger capacity/data. The oracle arm de-confounds the *read* side only; a residual write-side capacity ambiguity survives any null `?` (A3 vs A1 isolates selection-vs-encoding, which narrows but does not eliminate it).
4. **Continuous m ≠ diary text:** the twin tests bottleneck transport, not readable diary-hood; the discrete-token version is the follow-up card and can only lose bits relative to this one.
5. **Power:** 13 anima test pairs × 3 seeds is thin for a 0.02-bpb median; σ_seed is measured (θ_L2 depends on it) and T-7 forces added seeds rather than a quiet over-read. If σ_seed > 0.01 bpb `?`, the anima-alone verdict may need the pooled-stream read — pre-registered as PARTIAL territory, not a goalpost move.

---

**Bottom line:** run **H_006** next — $0, CPU-hours, reuses the entire H_005 harness, can kill the twin before it costs anything, and emits the oracle extracts the twin consumes. If H_006 holds, the twin (H_007) is the campaign's first real training run: ~4–5 M params, torch/MPS, ~12 h, **$0 cash** ($3–5 rental fallback), with a null made attributable by the oracle-liveness arm and the pre-anchored δ_min.
