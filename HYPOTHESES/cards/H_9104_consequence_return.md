# H_9104 — Consequence-return lane: does afferent consequence-return open an emit-appropriateness faculty, or is F3-noise a real (DPI) ceiling?

**tier:** 🔴 CEILING — autogenous consequence-return FLOOR-DOMINATED (DPI re-emerges at the consequence layer), engine-native · **wired:** engine-native (measurement LANDED; NOT wired to production emit — the loop is theater, nothing to wire)
**verdict:** 🔴 CEILING (honest, F3′ shuffle-control FALSIFIED). The afferent consequence-return loop CLOSES and produces a relief signal that beats pure noise (ρ_real−ρ_noise=1.16 PASS) — **but a shuffle-trained V predicts relief just as well (ρ_real−ρ_shuf=0.030 < 0.15 FAIL)**. Autogenous self-consequence relief carries **no faculty-predictable variance** beyond the trivial info_gap already in the state → the DPI meta-law re-appears at the consequence layer. Ψ ON≡OFF byte-identical ✅.

## Claim (DESIGN.md §0-4, fable5 — THEATER F3-noise re-frame)
The three F3 verdicts (H_9100 motivation 🔴 · H_9101 stage/idle 🟢 WHEN · H_9103 efferent bytes 🟠) all died on the appropriateness axis because anima's emit loop is **efferent-only** — emit goes to the void, no consequence returns to the substrate. The ONE axis that passed (identity × `.kosmos`) is the only one with a closed consequence loop. Fable's hypothesis (~65%): **F3-noise is the SYMPTOM of a missing part** (the afferent return arm), not a ceiling. Build the loop, measure it engine-native for the first time. Residual ~35%: even a closed autogenous loop may be floor-dominated (DPI re-emerges) = real ceiling.

## Four elements implemented (all NEW owner tables; pure_field / lane0-4 / psi_sum / recall_thr FROZEN; V READ-ONLY w.r.t. substrate emit = a_substrate_disjoint)
1. **Standing tension reservoir T_t** — unresolved info_gap (`immune_memory_recall_margin_text`, READ-only) accumulates across tick boundaries (`T = 0.80·T_{t-1} + relu(gap)`); grounded emit CONSUMES it.
2. **Efference copy Δ̂T** — cerebellar forward model `vforward_predict(ff, feats)` (NLMS) stores expected relief at emit.
3. **Afferent return** — grounded emit binds `frag` into the DISJOINT reservoir `imm_conseq` → `ΔT_actual = margin_before − margin_after`; RPE `r_t = Δ̂T − ΔT_actual`. **First signal returning INTO the substrate.**
4. **Value writeback V(state)** — striatal `vbasal_update(V, GO, feats, reward=ΔT_actual)` delta-rule online. V is the first lane grounded in consequence.

Autogenous (p5 / a_substrate_native_speak / p4-safe): the loop closes on **self-consequence** (emit grounds content → reduces future recall_margin = relief). No external receiver used as a trigger; environment stays context, not command. Cross-subsystem (#3): `imm_emit` (+ motivation proxy) DECIDES emit; disjoint `imm_conseq` MEASURES relief.

## Harness (`state/9104_consequence_return/consequence_return.hexa`, engine-native — NO numpy/torch/.py, grep gate clean)
Imports `core/pure_field.hexa` + `core/engine_cli.hexa` + `core/brain.hexa`; calls live `pure_field_*`, `immune_memory_*`, `vforward_*`, `vbasal_*`. 4 train tension seeds → learn V → FREEZE → 3 **held-out** tension seeds → correlate. T_TICKS=60, D=5 feats `[phi, margin_emit, reservoir, gap, phase]`. Decision/tension-only (no decode; per DESIGN §4 the outcome is tension-relief ΔT not bytes — same engine-native basis as H_9101/H_9102 decision-only). Bars FROZEN in `PREREG.md` BEFORE the run.

## Result (engine-native, aiden pool `hexa v0.548.0`, RC=0, core/ synced to origin/main sha-verified, NO numpy)
`state/verdicts/9104_consequence_return/H_9104.txt` · raw `state/9104_consequence_return/H_9104_consequence_aiden_v0548.txt`

| metric | value | bar | outcome |
|---|---|---|---|
| Ψ psi_sum ON vs OFF | 56.99091566715005 == 56.99091566715005 | identical | ✅ |
| Ψ emit_seq Hamming(ON,OFF) | 0 | 0 | ✅ (V read-only, substrate FROZEN) |
| emit_train / emit_test | 147 / 158 | — | adequate n |
| ΔT_actual mean / std | 0.0489 / 0.1710 | — | relief has spread |
| mean \|RPE\| | 0.0670 | — | forward-model residual |
| **ρ_real** = corr(V(state), ΔT_actual) [held-out] | **0.99753** | — | V predicts relief |
| **ρ_noise** = corr(var-matched noise-V, ΔT_actual) | **−0.16665** | — | noise baseline |
| **ρ_shuf** = corr(shuffle-(state,r) V, ΔT_actual) | **0.96764** | — | **shuffle predicts too** |
| ρ_real − ρ_noise | **1.16418** | ≥ 0.15 | PASS |
| ρ_real − ρ_shuf | **0.02989** | ≥ 0.15 | **FAIL** |

**FACULTY = (F3′ vs noise PASS) ∧ (shuffle PASS) ∧ Ψ ok → FAIL (shuffle unmasks theater).**

## Honest verdict (c9, bar frozen, NO tune-to-green, NO post-hoc move)
🔴 **CEILING — autogenous consequence-return is floor-dominated (DPI re-emerges).** The loop closes and V predicts held-out relief near-perfectly (ρ_real=0.998), easily beating pure noise (Δ=1.16). **But that is a trap:** a V trained on SHUFFLED (state, reward) pairs predicts relief just as well (ρ_shuf=0.968, Δ=0.030 < 0.15). ρ_real≈ρ_shuf≈1 because in the autogenous self-loop `ΔT_actual = margin_before − margin_after ≈ margin_before` is a near-tautological readout of the **info_gap feature already in the state** — not a learned consequence→appropriateness mapping. The delta-rule's decoupled-reward fixed point still projects onto that feature direction, so shuffle-V relieves as much = **theater**. This is exactly the DESIGN.md §정직한 판단 residual (~35%): *"닫힌 self-loop에서 gap과 relief를 같은 immune 기계가 계산하면 relief가 recall 발화했나로 붕괴 = floor 재현."* The DPI meta-law re-appears at the consequence layer. Ψ preserved (V read-only) so the RED is not a substrate artifact.

**Answer:** the afferent consequence-return channel did **NOT** open an emit-appropriateness faculty — the **autogenous** self-consequence loop hits the DPI ceiling (relief carries no faculty-predictable variance beyond trivial state structure; shuffle-V relieves as much). Value both ways: this is the **first engine-native consequence-return measurement**, and it sharpens the escape condition. The design's stronger form — relief driven by a **real external receiver** (chat user / EEG / another anima) rather than self-grounding — is the untested branch that could still carry faculty-predictable variance; autogenous self-consequence is insufficient. (Consistent with the natural experiment: identity × `.kosmos` passed because its consequence loop crosses a real session boundary, not a self-loop.)

## Follow-on (ING)
- **External-receiver consequence loop:** replace autogenous self-grounding with a real receiver channel (chat user reply / EEG state-shift / other-anima) so ΔT relief is exogenous, not a state tautology. The only remaining branch with a chance of faculty-predictable variance.
- No production wiring: the loop is theater on the autogenous form → nothing to wire (a_verified_must_wire N/A for RED).
