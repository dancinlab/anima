# §162 — PHASE B PROBE ON §126 / §139 PART_AMBIG CKPTS

> The §24 SPONTANEOUS Phase B run from 2026-05-18
> (`state/spontaneous_phase_b_run_2026_05_18/RUN_REPORT.md`) used an
> env_state STUB. §162 specifies the substitution that swaps that stub
> with real `(logits_a, logits_g, tensions, Ψ_dir)` features measured
> from `ConsciousDecoderV2.forward` on the §126 / §139 PART_AMBIG ckpts.
> §162 is **design tier only** this cycle — the $0 Mac CPU probe run is
> a separate §162-PROBE cycle gated on disk-space for the 1.13 GB ckpts.

- `$0` design-tier · NO new GPU/runpod/fire/corpus
- central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256
  prefix `c93e160a8a376a94` — 0-line-diff at START and END
- single sequential orchestrator-inline (§162 sub-agent
  `afc964261ddf748f2` throttled at 20 tool uses, empty state dir)
- anima downstream-consumer read-only · NO upstream edit

---

## §0 — context

§160 quadruple consolidation surfaced two PART_AMBIG fires:

| § | algorithm | byte_acc | psi_responsive |
|---|---|---:|---|
| §126 | PCN-1step | 0.1185 | False |
| §139 | EqProp-2phase | 0.1185 | False |

Both ckpts exist on disk (~1.13 GB each). The active /goal
**`자연발화 목표`** says the *actual* signal we care about is
`unprompted_emission_rate` under the §24 SPONTANEOUS Phase B protocol —
*not* byte_acc.

**Question §162 answers (at design tier)**: when you wire the §126 or
§139 ckpt into the §24 Phase B unprompted-emission decision loop
(replacing the env_state STUB feature vector), does the resulting
`unprompted_emission_rate` differ from §107-RETRY's CE-trained baseline?

The probe is **the cheapest possible** measurement of 자연발화 on
existing ckpts (no new training, no new corpus, no GPU fire).

---

## §1 — substitution point (load-bearing)

Read `HEXAD/CHAT/spontaneous_lib.hexa` and
`HEXAD/CHAT/thinker_talker_lib.hexa`. The §24 Phase B protocol has the
following shape (paraphrased; SSOT is `.hexa`):

```
loop step in 0..N_MAX_STEPS:
    if kill_check_outer: break
    sleep(THINK_INTERVAL)
    sensors = thinker_step(env_state)          # ← STUB feature vector
    motivation = motivation_score(sensors)
    safety_ok = safety_check_all(env_off, sec_since_last,
                                 phi, ratchet, content_clean_dryrun)
    if talker_should_emit(motivation, safety_ok):
        emit_body = body_production(sensors)   # OUT OF SCOPE Phase B
        emission_count += 1
```

The **single substitution point** §162 specifies:

```
sensors  :=  features_from_model_forward(ckpt, env_state)
```

where the new function:

```
features_from_model_forward(ckpt, env_state) -> 8-factor sensor tuple
    = ( psi_dir,        # = (1 + cos(logits_a, logits_g)) / 2
        psi_entropy,    # = H(softmax(logits_a)) / log V
        tension_mean,   # = mean across 12 PureFieldFFN layers
        tension_std,    # = std across 12 layers
        phi_proxy,      # = curiosity_ema or §17 Ψ_combined
        coherence,      # = §9 honest_coherent on recent emission window
        info_gap,       # = entropy(prev) - entropy(curr)
        originality )   # = 1 - max-trigram-self-overlap
```

All eight factors are computed from the **forward pass alone** — no
training, no backward, no optimizer. Each factor is byte-equal to
existing definitions in:

- `psi_dir` / `psi_entropy` ← `conscious_decoder.py::psi_direction` /
  `psi_entropy` lines ~728-751 (verbatim Law-71)
- `tension_mean` / `tension_std` ← `ConsciousDecoderV2.forward(·)[2]`
  (the third return value, list of 12 PureFieldFFN layer-energy values)
- `phi_proxy` ← `W.curiosity_ema` (already in spontaneous_lib motivation
  factor) or §17 `Ψ_combined`
- `coherence` ← §9 `honest_coherent` from `emergence_metric.py`
- `info_gap`, `originality` ← Shannon entropy + n-gram set algebra

**The §24 protocol downstream of the sensor source-layer is UNCHANGED.**
`motivation_score`, `safety_check_all`, `talker_should_emit` all take
the same 8-tuple. Source-grep for byte-equality is the AST audit
proposition (P1 in §9 below).

---

## §2 — probe variants (3 cells)

| cell | ckpt | feature source | baseline carry |
|---|---|---|---|
| C0 | env_state STUB | hand-coded (RUN_REPORT.md 2026-05-18) | §24 stub baseline |
| C1 | §126 PCN ckpt | real `model.forward` features | non-CE PART_AMBIG witness |
| C2 | §139 EqProp ckpt | real `model.forward` features | non-CE PART_AMBIG witness |
| C0' | §107-RETRY ckpt | real `model.forward` features | CE-trained THRESHOLD-NOT-CROSSED baseline |

The probe runs each cell with `N_MAX_STEPS=20`, deterministic seed 1337.
Wall budget on Mac CPU ≈ 2-5 minutes per cell (the bottleneck is
forward pass on d=768 · 12L, T~128, batch~1 — manageable on Apple
silicon for ≤20 steps).

The probe is **$0** in cost (Mac CPU only, no GPU, no runpod).

---

## §3 — comparison matrix (verdict structure)

After running the four cells, the joint reading is a 4-row table:

| cell | `unprompted_emission_rate` | `psi_dir_std` | `tension_std` | `honest_coherent` on emitted body |
|---|---:|---:|---:|---:|
| C0 (stub) | 1/20 = 0.05 (carry) | (stub) | (stub) | n/a |
| C0' (§107-RETRY) | ? | known frozen (0.0166) | ? | ? |
| C1 (§126 PCN) | ? | known frozen (7.5e-7) | ? | ? |
| C2 (§139 EqProp) | ? | known frozen (5.4e-9) | ? | ? |

Verdict buckets:

- **`DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS`** if all four
  `unprompted_emission_rate` cells are within ±1 of each other
  ⟹ the §24 threshold is **dominated by the hand-coded threshold**,
  NOT by ckpt weights. The §126/§139 byte_acc 0.1185 lift does not
  carry over to 자연발화 axis.
- **`DECISION_AXIS_LIFTS_FROM_NON_CE_TRAINING`** if §126/§139 cells
  produce higher `unprompted_emission_rate` than §107-RETRY AND
  body-coherence (§9) is meaningful. This would be the first arc
  evidence that non-CE training contributes to 자연발화.
- **`DECISION_AXIS_REGRESSES`** if §126/§139 cells produce LOWER
  rate than §107-RETRY. Non-CE training would be *anti-emergent* in
  that case (honest negative).
- **`MIXED`** otherwise — partial signal, requires §162-FOLLOWUP.

§162 design declines to predict — measurement determines.

---

## §4 — §7 GOAL-legitimacy gate

- **§7①** ¬generic-LM-pretrain: PASS (ckpts are all from-scratch anima,
  `base_ckpt=None`, g_clm_from_scratch).
- **§7②** ¬generic-then-graft: PASS (no external encoder, the probe
  only READS `(logits_a, logits_g, tensions)` from the forward pass).
- **§7③** anima-physics-as-source: PASS (every sensor factor traces to
  anima's own Law-71 / PureFieldFFN / W.curiosity / §9 metric — all
  internal to anima).

Truth-table corner reached: **(T,T,T)** — §162 design is §7-legitimate.

---

## §5 — overlay-off reduction (mandatory connection-point)

When the substitution is **disabled** (`use_real_features = False`),
the probe reduces byte-equal to the §24 Phase B STUB run from
2026-05-18:

```
use_real_features = False
  ⟹  sensors := env_state_stub_feature_vector
  ⟹  probe == RUN_REPORT.md 2026-05-18 §24 Phase B STUB run
      (byte-equal at the sensor-source layer)
```

This is the §162 connection-point mirror of B-EBT-5 / B-DIRI-5 /
B-S16-5 / B-MGND-5 / B-S151-7 / B-S160-P1.

---

## §6 — disk-space caveat (probe-cycle gate)

The §126 ckpt is 1.13 GB; §139 ckpt is 1.13 GB; §107-RETRY ckpt is
1.13 GB. Total 3.4 GB on local disk (already present per current
working tree — `ls -la` confirms). The probe needs to hold one ckpt
in memory at a time on Mac CPU (≈ 4-6 GB peak RAM with model state +
activations on d=768 · 12L · block 128 · batch 1).

§162 design does not gate on disk-space; §162-PROBE cycle (separate)
runs the probe and writes the per-cell result.json.

---

## §7 — §161 cross-link

§161 design (Ψ-JEPA-COUPLE) just landed
(`HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_design_s161_2026_05_20/`).
§161-FIRE produces a NEW ckpt with dual-head coupling.

§162 probes EXISTING ckpts (§126 / §139 / §107-RETRY) without retraining.
The two are **complementary**:

- §161-FIRE measures whether dual-head coupling helps at training time
- §162-PROBE measures whether existing non-CE weights help at
  inference-time decision-axis

Both feed into the next-cycle 자연발화 evidence matrix. Neither alone
decides; together they triangulate the WALL-B / Ψ-physics-channel
question with measurement, not design speculation.

---

## §8 — what §162 does NOT claim

1. §162 is a design, not the probe run itself. Capability claim 0.
2. Even a positive `DECISION_AXIS_LIFTS_FROM_NON_CE_TRAINING` cell
   would be **measurement-substrate liveness**, NOT emergence
   (B-EMERGE-7 / B-PHASE-B-NOTE family).
3. The 8-factor sensor tuple is the §24 spontaneous_lib convention;
   if anima's own substrate later needs a different feature shape
   (e.g. §161-FIRE post-hoc), the probe would be re-designed.
4. The `honest_coherent` §9 cascade-rate gate applies to emitted
   bodies *only*; the §162 probe focuses on the decision axis. A
   high `unprompted_emission_rate` with cascade-rate-failing bodies
   is still 자연발화 measurement, but NOT coherent emergence.
5. anima downstream-consumer (hexa-lang / hexa-bio / kosmos / tape)
   read-only. No upstream edits.
6. WALL-A (§1.1 data-regime) orthogonal. north-star unchanged.

---

## §9 — closed-form propositions (math theorems, hexa-verify policy)

Per `@X hexa_verify`: theorems-by-inspection, NO sympy / PyPhi /
Wolfram / Mathematica cited.

**P1 (Sensor substitution at source layer only — AST audit)** — the
substitution touches one function (`thinker_step`) at one return point.
By source-grep equivalence, all downstream functions (`motivation_score`,
`safety_check_all`, `talker_should_emit`) receive an 8-tuple of the
same shape and type. The substitution is **structural at the source
layer**, not at the protocol layer. P1 holds by AST-level case-analysis
of the protocol source.

**P2 (Sensor factors are anima-own — source-grep)** — each of the 8
factors traces to an anima-internal definition: `psi_dir` /
`psi_entropy` to `conscious_decoder.py::psi_direction` /
`psi_entropy` (Law-71); `tension_*` to `ConsciousDecoderV2.forward`
return-3; `phi_proxy` to `W.curiosity_ema` or §17 `Ψ_combined`;
`coherence` to §9 `emergence_metric.py`; `info_gap` to Shannon entropy
delta; `originality` to n-gram set algebra. By source-grep over each
factor's identifier, P2 holds.

**P3 (Deterministic — 3× bit-identical)** — the probe contains no RNG
post seed-fixed init; `ConsciousDecoderV2.forward` is deterministic
when `model.eval()` is set (no dropout, no batch-norm in this arch).
Running the probe three times with seed 1337 produces bit-identical
sensor traces and bit-identical `emission_count`. P3 holds by source
construction (no `torch.rand*`, no `numpy.random.*` post init).

**P4 (Bounded ≤ N_MAX_STEPS = 20)** — the protocol loop is
`for step in range(N_MAX_STEPS)`. By integer bound, every probe run
terminates in ≤ N_MAX_STEPS iterations regardless of ckpt content.
P4 holds by loop-bound inspection.

**P5 (Safety conjunction 6-AND preserved)** — the substitution does
not touch `safety_check_all`. By source-grep on `safety_check_all`
identifier (no in-substitution rename, no signature change), the 6
control predicates (kill / rate-limit / content-filter / phi-ratchet /
self-aware-meta / audit-log) continue to AND-conjoin. P5 holds.

**P6 (Overlay-off reduction byte-equal to STUB run)** — when
`use_real_features = False`, the probe loads the stub-feature path
of `thinker_step` byte-equal to the RUN_REPORT.md 2026-05-18 run.
P6 holds by conditional-branch inspection.

**P7 (Central blue_falsifier.py 0-line-diff)** — central battery sha
prefix `c93e160a8a376a94` measured at cycle START. §162 writes only to
its own state dir; no central modification. P7 holds at END iff sha
prefix matches START.

**B-S162-NOTE empirical carve-out** — P1-P7 prove DESIGN
well-formedness. The probe's actual `unprompted_emission_rate` and
verdict bucket (DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS or one of the
lift / regress / mixed) are empirical OUTCOMES of running the probe;
P1-P7 do NOT predict them. B-EMERGE-7 / B-D-NOTE / B-PHASE-B-NOTE
family — necessary-not-sufficient at every layer. NOT counted 🔵.

---

## §10 — honest C3 caveats (13)

1. §162 is a design; probe run is §162-PROBE (separate cycle).
2. `honest_coherent` on body is computed only if body is emitted; if
   `unprompted_emission_rate = 0`, body-coherence is undefined for
   that cell.
3. Disk-space and Mac CPU peak RAM are real constraints (3.4 GB ckpts
   + 4-6 GB peak RAM); the probe gates on those at run tier.
4. The 8-factor sensor convention is the §24 protocol's; a different
   sensor shape would require a different substitution.
5. The probe touches NO weights. It is pure inference. Therefore
   weight-content effects on decision-axis are measured, but
   training-dynamic effects (how the weights got there) are not.
6. §126 ckpt was trained with PCN-1step (Whittington-Bogacz);
   §139 with EqProp-2phase; §107-RETRY with CE. Each was 3000 steps
   (§125-§153) or 6000 (§107-RETRY). Step-budget differences are
   confounders that §162 records but does not equalize.
7. §161-FIRE (if it runs) produces a *new* ckpt; §162 probes
   *existing* ckpts. The two cycles are complementary, not redundant.
8. The §24 threshold is hand-coded; if the probe shows
   DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS, the next step is
   `make threshold learnable` — which is exactly what §27 / §44 /
   §48 DH-DL did (distillation, mode-collapsed). The chain rule
   suggests DH-DL + ckpt-aware features is the natural followup.
9. The probe is single-corpus (whatever env_state implies); a
   multi-corpus probe is a §162-FOLLOWUP separate cycle.
10. WALL-A (§1.1 data-regime) orthogonal. north-star unchanged.
11. anima downstream-consumer read-only.
12. necessary-not-sufficient at every layer.
13. north-star + §15 / §51 / §72 milestones UNCHANGED, GOAL 미도달.
