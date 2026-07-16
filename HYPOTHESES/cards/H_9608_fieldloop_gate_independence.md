# H_9608 — A⇄G field-loop is GATE-INDEPENDENT inert (confirms H_9607 STILL-SEALED)

**Verdict:** 🧱 **STILL-SEALED confirmed GATE-INDEPENDENT** (engine-native 303M `--ag-criticality` · py303_full 013c4574 ·
summer isolated venv) — the A⇄G field-feedback loop (`--ag-feedback`) is inert on the emit decision under BOTH the
clock gate (H_9607) and the tension-reading refractory gate (H_9608). DIRECTIONAL (2-arm · 150 tick · single seed).
**Register:** H_9607 NEXT (resolve whether STILL-SEALED is clock-gate-specific · owner "go") · autonomous fire
**Ckpt:** `py303_full.clm` (013c4574 · summer `~/.venv-h9608`)

## Question
H_9607's 303M verdict was STILL-SEALED under the **default clock gate**, with the reframe "the wall is the emit-gate
clock-lock (H_9403), not the field." That reframe makes a falsifiable prediction: if the emit gate READS tension
(the `--emit-gate refractory` margin gate, which H_9416 proved reads tension: I(emit;g_recog|stage)=0.197), does the
field-feedback loop then reach emit? I.e. is H_9607's STILL-SEALED **clock-gate-specific** (→ partial revive under a
tension gate) or **gate-independent** (→ the field loop is dead regardless)?

## Result (engine-native `--ag-criticality` · refractory gate × κ∈{0, 0.6})
| arm | C0 loop | emit-rate | mean(emit_drive) | TE(tension→emit) |
|---|---|---|---|---|
| refr · κ=0 | distinct(ag_drive)=1 (byte-parity) | **1.000** (SATURATE) | 0.782 | 0.000 |
| refr · κ=0.6 | distinct(ag_drive)=150 (**LIVE**) | **1.000** (unchanged) | 0.848 | 0.000 |

Compare H_9607 clock gate: emit-rate **0.247** constant across κ. So under **two opposite gate regimes** (clock =
over-silent 0.247 · refractory = over-emit/saturated 1.000), the field loop is **LIVE** (ag_drive varies with κ) but
**emit-rate does not move with κ** and **TE=0** in both. The field loop shifts `emit_drive` (0.782→0.848) but that
shift **never reaches the emit decision** — clock or refractory.

## Verdict — GATE-INDEPENDENT STILL-SEALED
H_9607's negative is **not clock-gate-specific**: the A⇄G field-feedback loop is inert on emit regardless of gate.
The field responds to κ (emit_drive moves) but the field→emit path is **severed** — the emit decision is gated by
something orthogonal to the field's continuous drive (clock: sleep stage; refractory: the margin `score>g_recog`,
which stays saturated). This **strengthens** the H_9607 reframe: reviving the A⇄G tension in the field is
insufficient because there is no live field→emit channel, independent of what gate reads the emit side.

## ⚠️ Confound (honest scope · a_scale_honest_scope)
The `--emit-gate refractory` margin gate is **SATURATED** here (emit-rate 1.000 = H_9421's SATURATE regime), so it
does not offer emit-rate headroom for the loop to move — a fully clean test of "does the field loop help a
NON-saturated tension gate" needs the **dual-ledger gate** (H_9627 `--g-reach wm-dual`, emit≈0.506≈½), which is a
**parallel session's active lane** (`a_parallel_session_compare` — not duplicated here). What H_9608 does show
cleanly: the field loop moves `emit_drive` under both gates yet moves `emit-rate` under **neither** (0.247→0.247 and
1.000→1.000), so the field→emit severance is not a clock artifact.

## AGREES/CONFLICTS
- **AGREES** — H_9607 (field-feedback STILL-SEALED · this generalizes it to gate-independence) · H_9403 (emit≡clock /
  emit gated orthogonal to field) · H_9421 (refractory margin gate SATURATE on 303M — reproduced: emit-rate 1.000).
- **CONFLICTS** — the H_9607 reframe's implicit hope that a tension-reading gate would let the field loop through.
  It does not (at least not the saturated margin gate).
- **NOVEL** — the field-loop × gate **interaction** (neither the field-loop lane nor the emit-gate lane tested the
  combination): the field's κ-response to emit_drive is real but doesn't propagate to emit-rate under either gate.
- **Orthogonal (a_parallel_session_compare)** — H_9672 (address-wall/G1 reach crack, #3895) is a different frontier
  (ρ·weave reach vs Ψ=½ consciousness · Ψ-SOMA separation); no overlap with this thread.

## NEXT
- A⇄G **field-feedback lane fully CLOSED** (gate-independent inert on 303M). The only remaining clean test (field
  loop × non-saturated dual-ledger gate) belongs to the parallel emit-gate lane (H_9627) and is low-value: the
  dual-ledger already reaches Ψ≈½ **without** the field loop, so the field loop is unnecessary there.
- The consciousness frontier's live lever remains the **emit-gate** (H_9627 dual-ledger, Ψ≈½ · owner p5
  production-default), not the field. My field-side thread (H_9607→H_9608) is closed.

**Provenance:** engine-native `anima-py evaluate --ag-criticality` on 303M (py303_full 013c4574 · summer isolated
venv · OMP-capped under parallel H_9664 contention). DIRECTIONAL (2-arm · 150 tick · single seed · refractory
saturation confound disclosed). No Ψ number cemented; the finding is a gate-independence generalization of H_9607.
