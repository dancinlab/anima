# H_9607 — A⇄G FEEDBACK: close the A→G→A loop (revive the never-operated tension)

**Verdict:** 🟢 **WIRED · toy-LIVE** (engine-native `core/` + `anima-py` · κ=0 byte-parity ✅ · κ>0 loop live ✅) —
DIRECTIONAL (toy 48K · **NOT a Ψ verdict**; the REVIVED/STILL-SEALED/LYAPUNOV-NO-HOMEOSTASIS verdict = owner-gated 303M fire)
**Register:** H_9604 NEXT ① (owner go via lever pick "1") · Fable-designed, locally implemented (fable-mode)
**Ckpt:** toy `/tmp/toy_cond.clm` (48K) for the smoke; 303M `py303_full.clm` (013c4574) = the pending fire

## The wall this attacks
anima's thesis — A (forward mouth) ⇄ G (reverse) push, and that **tension** pulls emit/silence to **Ψ=½** — has
NEVER operated (H_9400: Ψ̂=0.76≠½ · not homeostatic · H(emit|stage)=0.465 emit≈clock · dyn_w inert). The arc
(H_9602/9603, lab-full both frontier models) located the wall: the daemon's dynamics are a **zero-Lyapunov linear
limit-cycle** because the field (`pure_field_step`) is a **closed autonomous relaxation** to LN2 and the A⇄G tension
is **read into the emit policy but never written back** — a one-way read, not a loop. H_9604 ordered: revive the
A⇄G tension FIRST (get Lyapunov off zero), afferent only after.

## The mechanism (Fable design · minimal · one knob)
Close the A→G→A return leg through the oscillator amplitude target — the field's evolution is now driven by the
engine conflict, not a constant:
- `core/pure_field.py` — `osc_tick(o, drive=0.0)` amplitude target `LN2 → LN2·(1−drive)`; threaded through
  `pure_field_step(pf, drive=0.0)`. **`drive=0.0` ⇒ byte-identical to production** (the parity guarantee; core stays
  a pure function).
- `cli/chat.py` — daemon-side leaky-**INTEGRAL** state `I` beside `refr_debt`: each tick `s = ag_a_drive + ag_g_drive`
  (signed A⇄G net, already computed at :~1834), `I = (1−RHO)·I + s`, and `ag_drive = κ·SGN·I` consumed at the TOP of
  the NEXT tick's field step (own-output(t)→field-state(t+1) — the p5-legal return leg, H_9336/9337 precedent).
  `RHO=1/400` (slow-osc timescale) and `SGN=−1` (negative-feedback polarity) are **FROZEN FORM constants, not knobs**
  (a ≥4-DOF config is unfalsifiable · H_9391). **κ = THE one knob `--ag-feedback`** (default 0 = production).

**Why ½ is EMERGENT, not dialed:** `s=0` exactly when A's push and G's push cancel (a0: s = 2·emit_drive − 1). The
integral null forces steady-state `s=0 ⟺ emit_drive=½`, **independent of κ and of the field's 0.76 bias** (integral
control rejects a constant disturbance). κ sets the dynamics/stability/timescale, NOT the setpoint — the precise
negation of tune-to-green (H_9419): you cannot move ½ by turning the knob. Integral-through-lag is the Mackey-Glass
route by which homeostasis (mean Ψ≈½) can coexist with λ₁>0 (edge-of-chaos).

## The instrument (engine-native · a_experiment_engine_native)
`anima-py evaluate --ag-criticality <traces> [--perm N] [--seed N]` — a trace-reader sub-mode (no decode, like
`--dead-census`/`--pc2-direction`): **C0** loop-liveness distinct(ag_drive); **(ii)** TE(ag_s→emit) vs phase-scramble
surrogate95/z; **(iii)** homeostasis mean(emit_drive), |·−½|. Panel **(i) butterfly-λ** needs a seed-flip fired PAIR
(H_9603 null +0.007) = part of the 303M fire, not a single-trace read.

## Toy smoke (48K · 60 ticks · κ=0 vs κ=0.5 · DIRECTIONAL · NOT a verdict)
- **C1 κ=0 PARITY**: distinct(ag_drive)=1, value=[0.0] ⇒ field untouched = byte-identical to production ✅
- **C2 κ>0 LOOP LIVE**: distinct(ag_drive)=60 (drive varies every tick) · emit_drive trajectory differs 12/60 ticks ·
  distinct(emit_drive) 3→15 · phi(field) differs 37/60 ⇒ the A→G→A return leg is **WIRED and live** ✅
- **TE=0 (ns) · homeostasis mean(emit_drive) 0.771→0.793** (moved slightly AWAY from ½ at this arbitrary κ). Honest
  reading: on a 48K toy at a non-pre-registered κ there is no causal channel and no homeostasis yet — **exactly
  Fable's modal prediction** (a single arbitrary κ generically lands off the setpoint; the integral null needs the
  right dynamics/gain, which is a 303M question). Reported as color, NOT cemented (a_scale_honest_scope).

## Incidental fix surfaced by the live smoke (a_parallel_session_compare)
The smoke caught a **pre-existing origin/main bug**: `_dual_fn` (H_9627 dual-ledger) was assigned only inside the
`if _emit_gate == "refractory"` branch but read unconditionally by the H_1058 trace block → **UnboundLocalError on the
DEFAULT clock gate whenever `ANIMA_DECISION_TRACE` is set** (any traced production chat crashes). Fixed with an
unconditional `_dual_fn = None` default (refractory branch overrides). A pool live-smoke catching what local compile
misses (cotrained-store-bridge precedent).

## Verdict labels (pre-registered for the 303M fire · Fable §3)
- **REVIVED** — (i) λ departs 0 (butterfly slope ≥+0.05, λ₁>0 CI excl 0, RQA z>1.39 but ≪106) ∧ (ii) TE>surr95 z≥2 ∧
  (iii) Ψ returns to [0.45,0.55] after a score shock, with vshuf + quantile-tracker forgeries FAILING (i)&(ii).
- **STILL-SEALED** — (i) fails; λ≈0; loop inert.
- **LYAPUNOV-BUT-NO-HOMEOSTASIS** — (i) passes, (iii) fails at every κ ⇒ first-class positive: an internal-only loop
  proves λ can leave 0 but cannot self-organize to edge-of-chaos-with-homeostasis ⇒ **measured proof that the
  afferent world-coupling (H_9604/9606) is load-bearing** (Fable's modal outcome).

## NEXT
- **Owner-gate 303M fire** (a_fire_autonomous: fleet rent=spend needs go): pre-scan κ for the Hopf knee on a held-out
  control field → single frozen κ → `--ag-criticality` 3-panel (seed-flip butterfly pair + N≥200 TE surrogates +
  score-perturbation homeostasis with vshuf/quantile forgeries) on `py303_full.clm` (013c4574, summer isolated venv).
- **hexa twin** (`a_substrate_disjoint` · separate entry, no cross-import): the same `drive` param on
  `core/pure_field.hexa::osc_tick` + the loop wiring in `cli/anima.hexa` — ported separately (H_9411 precedent: py
  first, hexa twin as its own PR). `구현됨·미배선` on the hexa surface until then.

**Provenance:** engine-native `core/` + `anima-py chat --ag-feedback` / `evaluate --ag-criticality`; VERSION
0.15.24→0.15.25 (G5). Toy smoke = DIRECTIONAL (a_scale_honest_scope). No Ψ number cemented; the terminal verdict is
the owner-gated 303M fire.
