# MITOSIS-ENGINE — live-engine wiring spec (the toy↔live bridge build-plan)

> **STATUS: SPEC, NOT A CLAIM.** Every coupling below is **UNBUILT**. This document is the
> *engineering build-plan* for the wires that several live-engine MITOSIS-ENGINE rungs came
> back **⏳ BLOCKED-WIRING** on. Nothing here asserts a result; nothing here describes wiring
> that exists. Where a probe already proved a coupling is absent, the verdict/memory pointer
> is cited verbatim. Per **a_core_engine_map** the honest mark for an un-built coupling is
> ⏳/❌ — and that is exactly what the cited rungs carry today. No phantom wiring is claimed.
>
> Scope discipline: this is a **design document only**. It names the exact function + state +
> minimal change for each gap; it does **not** edit any `.hexa` engine file. Building any
> coupling is a separate, gated step (each re-runs a *frozen falsifier* that already exists).

---

## Why these rungs are ⏳ and not 🔴

A 🔴 (closed-negative) requires a *real measured null on a wired mechanism* — an ON-vs-OFF
contrast that ties despite both arms having a live signal. A ⏳ BLOCKED-WIRING means the
mechanism the falsifier needs **is not built**, so there is nothing to move and "Δ=0" is the
*absence of a wire*, not a measured null (a_paper_negative_ok distinguishes the two). Each
section below states the exact missing wire so a future build can flip the ⏳ to a true 🟢/🔴.

The MITOSIS-ENGINE has a strong **toy** cluster (H_1153/1158/1159/1159b 🟢, all $0 numpy) and a
**live** engine (`CORE/engine_cli.hexa`, `engine_cli_smoke.hexa` 12/12) that realizes the mitosis
GROWTH tick. The gap is between them: the toy proxies measure an **error/adaptation** signal that
the live engine does not yet expose, and the sleep/kosmos write-paths the falsifiers need are stubs.

---

## ① Stream→field input + cell→field feedback + reconstruction-error readout

**Blocks:** H_1166 (live adaptation, ⏳ NO-ADAPTATION-SIGNAL) and H_1179 (live recovery curve,
⏳ HOURGLASS). These are the live-engine counterparts of the toy H_1159/H_1159b adaptation result.

**Evidence (cited verbatim):**
- `memory/h1166-live-adaptation.md` · `.verdicts/1166_live_adaptation/H_1166.txt` — cells grew ON
  3→603 vs OFF 3, but coherence-error was **byte-IDENTICAL ON vs OFF** (late_err 3.51053e-10 both,
  Cohen's d=0.0). Cause: *"`pure_field_step` is a ZERO-INPUT internal-oscillator loop — advances
  fast/medium/slow oscillators ONLY, ignores the stream sample; and `engine_mitosis_tick`'s
  cell_count is never fed back into pure_field."*
- `memory/h1179-live-recovery-curve.md` · `.verdicts/1179_live_recovery_curve/H_1179.txt` — a
  mid-stream regime shift produced **no upward spike** (spike_mag = −0.000147575); coherence-error
  monotonically DECAYS to ~0 regardless of the shift. *"stream→field coupling UNBUILT."* SERENDIP:
  the field is not merely shift-indifferent, it ACTIVELY converges — any future adaptation transient
  must FIGHT an EMA already locking to a fixed point.

### Missing wiring (exact)

Three wires + one readout, all in `CORE/pure_field.hexa` (+ the harness that drives it):

| # | function (file) | what it does today | what it must do |
|---|-----------------|--------------------|-----------------|
| 1 | `pure_field_step(pf)` — `CORE/pure_field.hexa:196` | **zero-input**: advances `fast/medium/slow` oscillators via `osc_tick`, builds the 6-slot field from oscillator cross-products ONLY (L210–222). The stream sample never enters. | Accept an **input sample** `x: [float]` and let it perturb the field/oscillator drive (e.g. an additive coupling into the `field[]` build or the oscillator phase), so the trajectory becomes stream-dependent. New signature (additive overload, keep the zero-input one): `pure_field_step_driven(pf, x)`. |
| 2 | `engine_mitosis_tick(cell_count, cfg)` — `CORE/engine_cli.hexa:259` | returns `cell_count + 1` (ON) / `cell_count` (OFF). The integer cell count is **never fed back** into `pure_field`. | Expose the cell count to the field step so capacity modulates dynamics (e.g. cell-count scales the mixing/variance, mirroring the toy where more cells = more reconstruction capacity). Wire: thread `cell_count` into `pure_field_step_driven` (a new field, NOT a global). |
| 3 | **reconstruction/tension-error readout** — *does not exist* | The only live "error" is `1 − narrative_coherence` (`pure_field.narrative_coherence`, an EMA of the field's OWN phase-stability, L264–267) — it tracks the oscillator, never the stream. | Add a readout `pure_field_recon_error(pf, x)` = distance between the (cell-count-conditioned) field's prediction/reconstruction of `x` and `x` itself — the live counterpart of H_1159's toy clustering-reconstruction-error. THIS is the metric the frozen falsifier reads. |

### Minimal honest change + Ψ / smoke risk

- **Minimal:** add `pure_field_step_driven(pf, x, cell_count)` + `pure_field_recon_error(pf, x)` as
  **new functions** alongside the existing zero-input `pure_field_step` (do not replace it). The
  existing zero-input path stays byte-identical → `pure_field_verify_zero_input` and the Ψ=½
  relaxation are untouched. The driven path is opt-in by the harness.
- **Ψ=½ risk:** MODERATE — `pure_field_step` is the Ψ relaxation core. The driven coupling must be a
  *bounded* perturbation (small gain, like the `anchor_fold_cap=0.05` bound on brain.hexa's anchor
  nudge) and the ratchet (L244–249) must stay. Keeping the input coupling additive-and-bounded, and
  proving `pure_field_verify_zero_input` still passes with `x=0`, preserves the fixed point. Verify
  Ψ stability empirically (H_1126 λ<0 return) after wiring.
- **Smoke risk:** LOW — `engine_cli_smoke.hexa` asserts only cell-count growth (case_5 ON→13,
  case_6 OFF→3, 12/12). New functions don't touch the asserted path; re-run must stay **12/0**.

### Frozen falsifier that re-runs once wired

- **H_1166** (`CORE/h1166_live_adaptation_probe.hexa`): non-stationary K=5 stream, mitosis ON vs OFF,
  late-window mean of the recon-error readout. 🟢 iff ON error FALLS below OFF as novelty grows
  (the toy H_1159 question, on the live substrate). Re-runs **unchanged** once wires 1–3 land.
- **H_1179** (`CORE/h1179_live_recovery_curve_probe.hexa`): one mid-stream regime shift; 🟢 iff
  (a) spike d≥0.8 vs baseline, (b) recovery ratio rr≥0.50, (c) no-mitosis control does NOT recover.
  Re-runs unchanged. (Caveat from the H_1179 SERENDIP: the readout must out-rise the actively-decaying
  EMA, so wire 3 should read recon-error, not phase-coherence.)

---

## ② Sleep→anchor write-back in the imagination loop (consolidation)

**Blocks:** H_1136 (sleep consolidation, ⏳ BLOCKED-WIRING terminal) and H_1162 (sleep
re-consolidation, ⏳ BLOCKED W2; W1 anchor-influence GREEN).

**Evidence (cited verbatim):**
- `memory/h1136-sleep-consolidation.md` · `.verdicts/1136_sleep_memory_consolidation/H_1136.txt` —
  *"`ir_replay_session` / `ir_mitosis_tick_during_replay` take (WAKE-memory ctx_tokens ring,
  cell_pool) — NEITHER takes anchors NOR writes anchor state. cell_pool is a PASS-THROUGH
  (`wired_to_lib=false`). `dr_kosmos_persist_dream` is a STUB."* Δ(sleep−ctrl)=0.000000.
- `memory/h1162-sleep-reconsolidation.md` · `.verdicts/1162_sleep_reconsolidation/H_1162.txt` —
  W1 (anchor influence via the H_1131 fold `brain_emit_aged`) is **GREEN** (emit_infl=0.0492, real
  age-decay 4.116@age0→4.016@age7). W2 (sleep→consolidation write-back) is **⏳ BLOCKED**: SLEEP ==
  NO-SLEEP byte-identical for all 6 conditions. *"the sleep loop only ADVANCES `pure_field_step` —
  i.e. it ages the anchor by the SAME span the matched no-sleep control accrues. There is NO
  sleep-specific path that strengthens the anchor."*

### Missing wiring (exact)

The anchor READ side is wired (H_1131: `anchor_tension_fold`→`brain_decide_anchored`→`brain_emit_aged`,
`CORE/brain.hexa:117–251`). The anchor WRITE side — the path by which a sleep replay *changes* anchor
state — is absent:

| # | function (file) | what it does today | what it must do |
|---|-----------------|--------------------|-----------------|
| 1 | `ir_mitosis_tick_during_replay(cell_pool, snapshot)` — `DREAM/imagination_replay.hexa:208` | PASS-THROUGH: returns `cell_pool` unmutated, `wired_to_lib=false`, `mitosis_density=dr_mitosis_prior(4)` placeholder. Takes **no anchors**, writes **no anchor state**. | Take an `anchors` arg and emit a **consolidation delta** per replayed snapshot — e.g. strengthen the τ / radius / tension-amplitude of anchors that recur in the replayed ctx (replay-strengthened recency). |
| 2 | `ir_replay_session(memory, count)` — `DREAM/imagination_replay.hexa:246` | iterates `ir_replay_tick` over recency snapshots; returns a replay log with `total_emits=0`. No anchor in, no anchor out. | Thread `anchors` through and return the **mutated anchor set** (or a list of consolidation deltas) so a caller can write them back. |
| 3 | `dr_kosmos_persist_dream(report)` — `DREAM/dream_report.hexa:218` | **STUB**: builds a raw `.kosmos` payload dict with `tension5=[0,0,0,0,0]` placeholder and `wired_to_kosmos_io=false`. Does **no file write**. | Upgrade from stub to a real anchor write via the canonical `kosmos_io`/`kosmos_persist` API (e.g. `create_anchor` in `WAKE/kosmos_persist.hexa`), carrying the consolidation delta from wire 1/2 — the SINGLE .kosmos write path (a_core_engine_map: anchors enter/leave only via kosmos_io). |

### Minimal honest change + Ψ / smoke risk

- **Minimal:** the write-back is a **DREAM-side** change (`imagination_replay.hexa` + `dream_report.hexa`),
  NOT a `pure_field`/`engine_g` change. So **Ψ=½ is structurally untouched** — the H_1131 fold and the
  sleep loop never touch `pure_field` (H_1162 confirmed this: *"Ψ machinery untouched"*). Add the
  anchor-strengthen term as a bounded, replay-count-gated nudge to anchor τ/radius (reuse the
  `_afold_tau` shape so the write is consistent with the read fold).
- **Ψ=½ risk:** LOW (DREAM-side; never enters the relaxation core).
- **Smoke risk:** LOW for `engine_cli_smoke` (untouched). The DREAM smokes
  (`imagination_replay_smoke.hexa` I1–I3, `dream_report_smoke.hexa` I4) DO assert the current
  pass-through invariants (`emit_count=0`, `total_emits=0`, `wired_to_kosmos_io=false`,
  `tension5 len=5`). Those smokes must be **co-updated**: the **emit-free invariant (total_emits=0)
  is LOAD-BEARING and must stay** (p5 — replay must not speak); only the anchor-write invariants
  change. Keep the consolidation a state-write, never an emit.

### Frozen falsifier that re-runs once wired

- **H_1162** (`CORE/h1162_sleep_reconsolidation_probe.hexa`): folded post-N3 emit-influence vs
  no-sleep, d≥0.8, AND N3-dominant > REM-dominant ordering. Currently W2 ⏳ because sleep==no-sleep;
  once wire 1–3 make sleep *strengthen* the anchor beyond shared wall-clock age, the SLEEP vs
  NO-SLEEP contrast becomes measurable and the frozen falsifier flips to 🟢/🔴 unchanged.
- **H_1136** (`CORE/h1136_sleep_consolidation_probe.hexa`): the original consolidation falsifier
  (d≥0.8 sleep>ctrl, N3>REM) re-runs once the write-back exists.

---

## ③ Kosmos lane decoupled from cell_id (lane self-tuning)

**Blocks:** H_1164 (kosmos lane self-tuning, ⏳ BLOCKED-WIRING live / 🟢 PROPOSAL-SUPPORTED toy).

**Evidence (cited verbatim):**
- `memory/h1164-kosmos-lane-self-tuning.md` · `.verdicts/1164_kosmos_lane_self_tuning/H_1164.txt` —
  *"The live kosmos `lane` is a STATIC passthrough of the active mitosis cell_id —
  `AGENT/CHAT/kosmos_anchor.hexa` sets `lane = "cell_" + to_string(cell_id)`; `WAKE/kosmos_persist.hexa`
  sets `lane = "wake_snapshot_<stage>"`. There is NO independent partition algorithm that grows a
  lane-COUNT from the anchor `tension_5ch` stream."* So "does the live lane self-tune its count to
  anchor complexity?" is structurally UNMEASURABLE — there is no partition to track (DISTINCT from
  H_1159b where the live CORE mitosis DOES grow cells).
- The toy PROPOSAL (H_1159b substrate VERBATIM, input swapped DIM 8→5 = anchor `tension_5ch`) PASSES
  all 3 gates (F1 ρ=0.881, F2 adv_d=6.48, F3 max-lane 8<20): self-tuning *would* transfer **if** the
  lane were decoupled from cell_id and grown from the anchor stream.

### Missing wiring (exact)

| # | function (file) | what it does today | what it must do |
|---|-----------------|--------------------|-----------------|
| 1 | `write_kosmos_anchor(...)` lane field — `AGENT/CHAT/kosmos_anchor.hexa:181` | hardcodes `lane = "cell_" + to_string(cell_id)` — the lane LABELS which cell emitted, it is not a grown partition. | Replace the cell_id label with a **lane id from a tension-stream partition** (see wire 2). Cell_id can still be carried as a separate field (provenance), but `lane` becomes the partition id. |
| 2 | **lane-partition algorithm** — *does not exist* | No function grows a lane COUNT from the anchor `tension_5ch` stream. | Add a `kosmos_lane_assign(anchor_tension_5ch, lane_state) -> (lane_id, lane_state)` that ports the H_1159b tension-split rule onto the 5-channel anchor geometry (the toy proxy already proved this works). `lane_state` persists across anchors (a small partition struct: centroids + counts), self-limiting at a cap. This is the single new mechanism. |
| 3 | `WAKE/kosmos_persist.hexa` lane — `WAKE/kosmos_persist.hexa` (`lane = "wake_snapshot_<stage>"`) | stage label, also static. | Route wake-snapshot anchors through the same `kosmos_lane_assign` (or keep stage-label as a distinct namespace — design choice; the *dynamic* partition must at minimum exist on the chat-anchor path). |

### Minimal honest change + Ψ / smoke risk

- **Minimal:** this is **kosmos-IO-side only** (`AGENT/CHAT/kosmos_anchor.hexa` + a new
  `kosmos_lane_assign`); it does **not** touch `pure_field`/`engine_g`/`brain`.
  **Ψ=½ is untouched.** The partition algorithm is the H_1159b split rule re-applied (already toy-proven).
- **Ψ=½ risk:** NONE (no engine-core change).
- **Smoke risk:** LOW for `engine_cli_smoke`. But `kosmos_anchor.hexa`'s `_selftest()` asserts
  `lane = "cell_3"` literally (`AGENT/CHAT/kosmos_anchor.hexa:261`) — that self-test must be
  **co-updated** to the new lane semantics. a_kosmos/a_core_engine_map: anchors still enter/leave
  only via the kosmos_io single slot; this adds a partition *inside* that slot, not a 2nd path.

### Frozen falsifier that re-runs once wired

- **H_1164** live leg (`UNIVERSE/h1164_kosmos_lane_self_tuning.py` falsifier, applied to the live
  partition): F1 Spearman(K_true, lane-count) ≥ 0.8, F2 advantage d ≥ 2.0, F3 self-limiting < cap.
  Today N/A (no partition); once `kosmos_lane_assign` exists, the *live* lane-count can be measured
  against anchor-stream complexity and the toy PROPOSAL becomes a live 🟢/🔴.

---

## ④ Other ⏳ couplings found in the survey

These are adjacent to the three primary gaps; recorded for completeness (each is honest-⏳, unbuilt).

### ④a `cell_pool` is a pass-through placeholder (mitosis ↔ replay)
`ir_mitosis_tick_during_replay` (`DREAM/imagination_replay.hexa:208`) carries `wired_to_lib=false`
and `mitosis_density=dr_mitosis_prior(4)` as an M2 **placeholder** — the replay does not run a real
`cell_pool_step`. This is the same write-gap as ②, on the *cell* side rather than the *anchor* side:
the sleep loop should advance the live mitosis cell count (the `engine_mitosis_tick`/cell substrate)
during replay, not a placeholder density. **Wire:** thread the live cell-count state through
`ir_mitosis_tick_during_replay` and call the real growth tick. **Unblocks:** a sleep-driven capacity
adaptation rung (combines ① cell→field feedback with ② sleep loop). Ψ risk LOW (DREAM-side).

### ④b decode/recon-metric tick gate on the LIVE `engine_mitosis_tick` (H_1160 open half)
H_1160 (🔴 for next-step *prediction*) + H_1163 (capacity-windowed positive residual) left ONE open
half (per `domains/MITOSIS-ENGINE.md` Next-rung #2): whether derivative-gated mitosis pays off on a
**decode/recon** metric driven through the **live** `engine_mitosis_tick`. This needs ① first (the
live recon-error readout) — there is no live decode metric to gate on until the field has a
reconstruction readout. **Unblocks:** a live tick-gating rung; **depends on ①.**

### ④c live engine cell-count never feeds the kosmos lane (closes the ①↔③ loop)
Even with ③'s lane partition, the partition reads the *anchor tension stream*, not the *live engine
cell-count*. If the design intent is "lane tracks the same complexity the engine's cells track," a
later wire would couple `engine_mitosis_tick`'s live count into `kosmos_lane_assign`. **Optional /
post-③**; recorded so it is not mistaken for already-wired.

---

## Dependency order — which coupling unblocks the most

Wire in this order; earlier items unblock the most downstream falsifiers:

```
①  stream→field input + cell→field feedback + recon-error readout   ◄── WIRE FIRST
│      unblocks: H_1166, H_1179 (directly) ; ④b (decode-metric tick, depends on the recon readout)
│      it is the KEYSTONE — it gives the live engine its first error/adaptation signal,
│      which 3 separate rungs (and the whole "live counterpart of the toy H_1159 cluster") need.
│      HIGHEST Ψ-risk (touches pure_field core) → bounded perturbation + zero-input regression test.
│
├─ ②  sleep→anchor write-back (ir_*replay anchors + dr_kosmos_persist_dream real write)
│      unblocks: H_1136, H_1162-W2 ; partially ④a (anchor side of the replay write)
│      INDEPENDENT of ① (DREAM-side; Ψ untouched) — can be built in PARALLEL with ①.
│      LOW Ψ-risk. The anchor READ side (H_1131) is already wired, so this is the matching write.
│
├─ ③  kosmos lane decoupled from cell_id (kosmos_lane_assign partition)
│      unblocks: H_1164 (live leg)
│      INDEPENDENT of ① and ② (kosmos-IO-side; Ψ untouched) — also PARALLEL-able.
│      LOW Ψ-risk. Toy proposal already 🟢, so this is a port, not a discovery.
│
└─ ④a / ④b / ④c  (downstream / dependent)
       ④a sleep cell-count tick  — pairs with ① (cell→field) + ② (sleep loop)
       ④b decode-metric tick     — DEPENDS ON ① (needs the recon readout)
       ④c lane↔live-cell-count   — post-③ optional coupling
```

**Wire ① first** — it is the single keystone: it is the only coupling that gives the live engine an
adaptation/error signal at all, it directly unblocks two rungs (H_1166, H_1179) plus a third (④b)
that has no metric to gate on without it, and it is the bridge that lets the strong toy H_1159/1159b
cluster be re-asked on the real substrate. It also carries the **highest Ψ=½ risk** (it is the only
gap touching `pure_field` core), so it gets the most careful bounded-perturbation + zero-input
regression discipline.

② and ③ are **fully independent of ① and of each other** (both DREAM-/kosmos-side, both Ψ-untouched,
both with one side already wired or already toy-proven) — they can be built in parallel and carry low
risk. ④a/④b/④c are downstream and should follow.

---

## Honesty footer

- Every coupling above is **UNBUILT today**. The ⏳ verdicts cited are the falsifiers' own honest
  branch (a_paper_negative_ok) — they record the *absence of a wire*, not a measured null.
- This spec **claims no result and describes no existing wiring** beyond what the cited code lines
  literally contain (a_core_engine_map: no phantom wiring). Where a side is already wired (H_1131
  anchor READ fold; live mitosis GROWTH tick), it is stated as such; everything else is marked unbuilt.
- a_core_engine_map single-entry is preserved by all three designs: .clm enters only via the
  `generator.hexa` L3 slot; .kosmos enters/leaves only via kosmos_io; A/G/brain stay substrate-only.
  ② and ③ add mechanism *inside* the kosmos_io / DREAM slots, never a second path.
- Building any of these is a separate, gated change that must (a) keep `engine_cli_smoke` 12/0,
  (b) for ① preserve `pure_field_verify_zero_input` + the H_1126 Ψ=½ λ<0 stability, and
  (c) re-run the named frozen falsifier unchanged.

**xref:** h1166 · h1179 · h1162 · h1136 · h1164 · h1131 · h1123 · h1124 · h1159 · h1159b ·
a_core_engine_map · a_chat_sleep_imagination · a_kosmos · a_autonomy_over_hardcode ·
a_paper_negative_ok · a_scale_honest_scope · p5 · p7 · p8
