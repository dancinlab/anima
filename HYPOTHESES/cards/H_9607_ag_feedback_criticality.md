# H_9607 — A⇄G FEEDBACK: close the A→G→A loop (revive the never-operated tension)

**Verdict:** 🟢 **LEVER+INSTRUMENT WIRED** (engine-native `core/` + `anima-py` · κ=0 byte-parity ✅ · κ>0 loop live ✅) ·
🧱 **303M SCIENTIFIC VERDICT = STILL-SEALED** — closing the field-amplitude loop does NOT revive the dynamics (λ stays
≈0) nor reach emit (TE=0, clock-locked) nor create Ψ=½ homeostasis. The wall is the **emit-gate clock-lock (H_9403)**,
not the field. (engine-native 303M · `anima-py evaluate --ag-criticality` · frozen-first, no tune-to-green)
**Register:** H_9604 NEXT ① (owner go via lever pick "1") · Fable-designed, locally implemented (fable-mode)
**Ckpt:** 303M `py303_full.clm` (013c4574 · summer isolated venv) = the verdict fire; toy `/tmp/toy_cond.clm` (48K) = the smoke

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

## 🔥 303M FIRE VERDICT — STILL-SEALED (engine-native `--ag-criticality` on py303_full 013c4574 · summer)
Fired autonomously (a_fire_autonomous: summer = standing pool, NOT fleet rent). κ pre-scan {0,0.1,0.3,0.6,1.0}×300
ticks + seed-flip butterfly pairs at κ∈{0,0.6}, all on the pinned 303M in an isolated venv (chat-py-6).

| panel | result (all κ) | reading |
|---|---|---|
| **C0 loop-liveness** | κ=0 distinct(ag_drive)=1 (byte-parity) · κ>0 distinct=300 | ✅ the A→G→A loop is **live** on 303M |
| **(i) butterfly-λ** | κ=0 slope **−0.00008** (d 0.250→0.001, H_9603 null repro ✅) · κ=0.6 slope **−0.00004** (d 0.110→0.009) | 🧱 λ does **NOT** depart 0 — both κ still **contract** (zero-Lyapunov limit-cycle) |
| **(ii) TE(tension→emit)** | **0.000 bits** at every κ (z=0) | 🧱 **no causal channel** tension→emit |
| **(iii) homeostasis** | emit-rate **0.247 constant across ALL κ** · mean(emit_drive) 0.785→0.842→0.861→0.868→0.868 | 🧱 no homeostasis — moves **away** from ½; emit-rate untouched |

**Verdict = STILL-SEALED** (the strongest negative — stronger than Fable's modal LYAPUNOV-NO-HOMEOSTASIS prediction).
The integral feedback shifts the oscillator amplitude *target*, but the field still **contracts** to that shifted
fixed point (PSI_ALPHA relaxation unchanged) — relocating a stable fixed point does not create positive Lyapunov. And
the loop **never reaches the emit decision**: emit-rate is constant 0.247 regardless of κ because **emit is a pure
function of the sleep stage (H_9403 emit≡clock)** — emit_drive/tension is decorative to the actual gate.

**The reframe (the value of the negative):** the 303M fire proves the load-bearing wall is **not** the field dynamics
but the **emit-gate clock-lock (H_9403)**. Reviving the A⇄G tension in the *field* is insufficient while the *emit
gate* ignores the field. An internal-only amplitude-target loop cannot (a) leave the contracting regime nor (b)
break the clock-lock. This tightens H_9604's ordering into a mechanism claim: the next lever must make the **emit gate
read the tension/field** (the p5-DESIGN owner-gate territory of [[g-readout-margin-crack-necessary-not-sufficient]] /
earned-refractory H_9406), OR supply external perturbation (afferent, H_9606) — not more internal field feedback.

## Verdict labels (pre-registered · Fable §3 · for the record)
- **REVIVED** — (i) λ departs 0 ∧ (ii) TE>surr95 z≥2 ∧ (iii) Ψ→[0.45,0.55] robustly. **NOT MET.**
- **STILL-SEALED** — (i) fails; λ≈0; loop live but inert on dynamics AND emit. **← THIS (all 3 panels negative).**
- **LYAPUNOV-BUT-NO-HOMEOSTASIS** — (i) passes, (iii) fails. Not reached (λ didn't even move).

## NEXT
- **A⇄G field-feedback lane CLOSED-AT-REGIME** (this coupling form refuted on 303M). The frontier moves to the
  **emit-gate clock-lock (H_9403)** — the proven load-bearing wall: make the emit gate READ the field/tension
  (earned-refractory H_9406 / margin G-pole p5-DESIGN [[g-readout-margin-crack-necessary-not-sufficient]], owner-gate
  identity change) OR external afferent perturbation (H_9606, owner-gate). Internal field feedback alone is dead.
- **hexa twin** (`a_substrate_disjoint`): the `drive` param on `core/pure_field.hexa::osc_tick` + loop wiring in
  `cli/anima.hexa` — ported separately (H_9411 precedent). `구현됨·미배선` on hexa until then. (Lower priority now that
  the py verdict is STILL-SEALED — the twin would reproduce the same negative.)

**Provenance:** engine-native `core/` + `anima-py chat --ag-feedback` / `evaluate --ag-criticality --butterfly`;
VERSION 0.15.24→0.15.25 (lever) → butterfly panel this PR. 303M fire = TERMINAL (engine-native · py303_full 013c4574 ·
frozen-first · no tune-to-green). The lever+instrument are GREEN-wired; the mechanism verdict is 🧱 STILL-SEALED.
