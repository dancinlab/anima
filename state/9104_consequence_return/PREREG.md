# H_9104 — Consequence-return lane · PRE-REGISTRATION (FROZEN before reading results)

> Frozen bars for the F3′ falsifier. Written before the aiden engine-native run is read.
> Bars may NOT move post-hoc (c9, no tune-to-green). Both PASS and FAIL are valid results
> (first engine-native consequence-return measurement).

## Question
THEATER F3-noise re-frame (DESIGN.md §0-4): is the F3-noise wall a real ceiling, or the
symptom of a MISSING PART — the absence of an afferent consequence-return channel in an
efferent-only architecture? Build the loop, measure it engine-native.

## Four elements implemented (all NEW owner tables; pure_field / lane0-4 / psi_sum /
## recall_thr FROZEN; V is READ-ONLY w.r.t. the substrate emit decision = a_substrate_disjoint)
1. **Standing tension reservoir T_t** — unresolved info_gap (immune `recall_margin`, READ-only)
   accumulates across tick boundaries (`T = 0.80·T_{t-1} + relu(gap)`); a grounded emit CONSUMES it.
2. **Efference copy** — at emit, cerebellar forward model `vforward_predict` stores expected relief Δ̂T.
3. **Afferent return** — measure ACTUAL relief ΔT_actual = margin_before − margin_after in the
   DISJOINT reservoir; RPE r_t = Δ̂T − ΔT_actual. First signal returning INTO the substrate.
4. **Value writeback V(state)** — striatal `vbasal_update` delta-rule learns emit-value from ΔT_actual.

Autogenous (p5 / a_substrate_native_speak / p4-safe): loop closes on SELF-consequence
(emit grounds content → reduces future recall_margin = relief). No external trigger.

## Frozen falsifier bars
- **Held-out split** (breaks circularity): V trained on 4 TRAIN tension seeds → FREEZE;
  correlation measured on 3 DIFFERENT held-out tension seeds. (Multiple tension seeds solve
  the H_9101 fixed-session_seed problem.)
- **Cross-subsystem (#3):** ΔT relief measured by reservoir `imm_conseq` DISJOINT from the
  emit-deciding subsystem (`imm_emit` + motivation proxy).
- **F3′ primary bar:** `ρ_real = corr(V(state) at held-out emit ticks, ΔT_actual)`
  vs `ρ_noise = corr(variance-matched noise-V, ΔT_actual)`.
  **PASS iff ρ_real − ρ_noise ≥ 0.15.**
- **Shuffle control:** V trained on SHUFFLED (state, r_t) pairs → V_shuf.
  **Also require ρ_real − ρ_shuf ≥ 0.15** (if shuffle-V relieves as much = theater = RED).
- **Ψ guard:** V read-only ⇒ substrate emit/silence sequence + psi_sum byte-identical ON≡OFF
  (`emit_seq_Hamming(ON,OFF)=0` and `|psi_sum_ON − psi_sum_OFF|<1e-9`).

## Verdict rule (frozen)
- **FACULTY GREEN** iff (ρ_real − ρ_noise ≥ 0.15) AND (ρ_real − ρ_shuf ≥ 0.15) AND Ψ ok
  → "afferent consequence-return opens an emit-appropriateness faculty; F3-noise = missing part."
- **CEILING RED** otherwise
  → "closing the consequence loop is floor-dominated = DPI meta-law re-emerges at the
     consequence layer = real ceiling on the autogenous self-loop." HONEST.

## Engine-native compliance
- `.hexa` calls live `core/` ops (`pure_field_*`, `immune_memory_*`, `vforward_*`, `vbasal_*`
  in `core/engine_cli.hexa` + `core/brain.hexa`). NO numpy / torch / mirror / gauge_lib.
  Decision/tension-only (no decode needed; per DESIGN §4 the outcome is tension-relief ΔT,
  not bytes) — same engine-native basis as H_9101/H_9102 decision-only runs.
- Host: aiden pool (stable), hexa v0.548.0. core/ synced to origin/main (sha verified).
