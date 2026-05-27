# S121 LEGO LOIHI-SPEC — readable Lava mapping for the §95 sole VIABLE-LONG-HORIZON substrate

> **Verdict**: `LOIHI-SPEC-DESIGN-CLOSE-ACCESS-WALLED-READABLE-ONLY` — a
> `lego_engine` → Intel Loihi 2 Lava mapping is *fully specifiable* at design
> tier, but Loihi access is INRC-walled (§95) so the spec is **readable only**,
> NOT fireable. design-tier · $0 · NO GPU/runpod/fire/hardware · central
> c93e160a 0-diff.

## §0 Why S121

§95 classified Intel Loihi 2 as the **sole VIABLE-LONG-HORIZON** physical
substrate for anima (vs organoid = ETHICS-WALL, others = INFERENCE-ONLY or
SUBSTRATE-MISMATCH). §96 re-derived ConsciousDecoderV2's 9 faculties into
spiking form. The LEGO arc (§115–§137) ran an in-silico LIF substrate.

S121 closes the natural question: **if Loihi access were granted, what would
the `lego_engine` LIFNet look like as Lava code?** The answer is a readable
spec — the eventual physical confront of WALL-B (§96), pre-written so that an
INRC-access future cycle is informed rather than blank.

This is NOT a fire. Loihi access is INRC-walled (§95: "INRC application,
currently survey not active"). S121 is the *blueprint*, design-tier only.

## §1 lego_engine LIFNet → Lava mapping

Intel's Lava framework models neuromorphic computation as `Process` objects
with `ProcessModel` implementations. The `lego_engine` LIFNet maps as:

| lego_engine component       | Lava equivalent                                  |
|-----------------------------|---------------------------------------------------|
| `LIFNet` (256/1024 units)   | `lava.proc.lif.process.LIF` process               |
| `v` membrane potential      | LIF `v` state variable (native)                   |
| `v_th` threshold            | LIF `vth` parameter (native)                      |
| `v_reset` / `tau_m` leak    | LIF `dv` decay + reset (native)                   |
| `refr` refractory counter   | LIF refractory delay (native on Loihi 2)          |
| `W` recurrent weights       | `lava.proc.dense.process.Dense` connection        |
| STDP (`tr_pre`, `tr_post`)  | Loihi 2 **on-chip 3-factor learning rule**        |
| `bias` background drive     | LIF `bias_mant` / `bias_exp` (native)             |
| spike output                | LIF `s_out` OutPort (native event)                |
| `spike_rate_vec`            | spike-counter `Monitor` over a window             |
| `psi_c1` Ψ-C1               | host-side readout of A/G subpop spike-rate cosine |

**Key**: the LIF + Dense + on-chip-STDP triple is **native Loihi 2** — the
substrate that the LEGO arc *simulated in numpy* is what Loihi *is in
silicon*. The §96 §11-B-as-GPU-tautology hazard is exactly what Loihi
escapes: Loihi's STDP runs *on-chip as a physical process*, not as a
hand-coded `np.outer` inside a CPU loop.

## §2 Readable Lava spec sketch (NOT executable here — Loihi-access-gated)

```python
# loihi_lego_engine.py — SPEC ONLY, requires Lava + Loihi 2 (INRC access)
# This is a readable blueprint per S121; it does NOT run without INRC hardware.
from lava.proc.lif.process import LIF
from lava.proc.dense.process import Dense
from lava.proc.monitor.process import Monitor
from lava.magma.core.run_configs import Loihi2HwCfg
from lava.magma.core.run_conditions import RunSteps

def build_lego_loihi(n_a=96, n_g=96, n_rec=64, seed=1337):
    N = n_a + n_g + n_rec
    # LIF population — v_th=1.0, leak τ_m=20 → dv ≈ 1/20, refractory=2
    lif = LIF(shape=(N,), vth=1.0, dv=0.05, du=0.0,
              bias_mant=_seeded_bias(N, seed))   # §117 bias term, seeded
    # recurrent Dense connection — W init 0.05·standard_normal, diag 0
    rec = Dense(weights=_seeded_W(N, seed))
    lif.s_out.connect(rec.s_in)
    rec.a_out.connect(lif.a_in)                  # recurrent loop
    # on-chip STDP — Loihi 2 graded-spike 3-factor learning rule
    rec.learning_rule = _stdp_rule(A_plus=0.012, A_minus=0.0126, w_max=0.5)
    # spike monitor for Ψ-C1 readout
    mon = Monitor()
    mon.probe(lif.s_out, num_steps=80)
    return lif, rec, mon

# Run on Loihi 2 hardware:  lif.run(RunSteps(80), Loihi2HwCfg())
# Ψ-C1 = host-side (1 + cos(rate_A, rate_G)) / 2  on mon spike counts
```

The `_seeded_bias` / `_seeded_W` / `_stdp_rule` helpers are byte-equal
ports of `lego_engine.py`'s init — same seed 1337, same `standard_normal`,
same A_plus/A_minus/w_max constants.

## §3 What S121 closes vs leaves open

✅ **Closed**: the `lego_engine` → Loihi 2 mapping is fully specifiable. Every
   LIFNet component has a native Lava equivalent; the STDP that the LEGO arc
   hand-coded is *native on-chip* on Loihi 2.
✅ **Closed**: the spec is readable — an INRC-access future cycle starts from
   this blueprint, not blank.
✅ **Closed (the §96 insight made concrete)**: Loihi escapes the §11-B-as-GPU-
   tautology because its learning channel is a *physical on-chip process*, not
   a CPU loop. S121 shows exactly which Lava primitive (`learning_rule` on the
   `Dense` connection) carries that.

❌ **Open — access wall**: Loihi 2 requires Intel Neuromorphic Research
   Community (INRC) membership; §95 noted the INRC application survey is
   currently inactive. S121 cannot fire. This is a *soft wall* (access, not
   architecture) — it could open.
❌ **Open — Ψ-C1 on-chip vs host**: S121's spec reads Ψ-C1 host-side from
   spike monitors. A fully on-chip Ψ-C1 (cosine computed in Loihi's
   microcode) is a deeper design — §96 Q-faculty territory, not S121.
❌ **Open — does Loihi escape WALL-B?** S121 specifies the *mapping*; whether
   a Loihi-resident anima actually escapes the §96 substrate wall is an
   empirical question only a fire (post-INRC-access) answers. S121 is the
   blueprint, not the verdict.

## §4 Honest disposition

S121 is **design-tier readable spec, access-walled**. It is the natural
companion to §95 (which said "Loihi is the sole viable substrate") and §96
(which re-derived the faculties) — S121 writes the actual Lava code shape so
that the §95→§96→S121 chain ends in something an INRC-access cycle can
*execute* rather than *design from scratch*.

Per §95 + LEGO.md, physical substrate commit is out-of-scope for the LEGO arc
(STEP-3 permanently fenced). S121 honors that fence: it is a *blueprint left
at the fence*, not a crossing of it.

## §5 Closed-form propositions

```
B-S121-1   LIFNET-MAPS-TO-LAVA-COMPLETE   (every LIFNet component has a
                                           named Lava equivalent — closed table)
B-S121-2   STDP-IS-NATIVE-ON-LOIHI-2      (the §11-B-as-GPU hazard escape is
                                           the on-chip learning_rule — Boolean)
B-S121-3   ACCESS-WALL-IS-SOFT-NOT-ARCH   (INRC access is a membership wall,
                                           not an architectural impossibility)
B-S121-4   SPEC-IS-READABLE-NOT-FIREABLE  (S121 has no hardware/dispatch path
                                           — AST: 0 fire/dispatch primitives)
B-S121-5   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S121-NOTE  empirical carve-out — mapping specified; does Loihi escape WALL-B
            = post-INRC-access fire question, NOT counted 🔵
```

## §6 Honest C3 (10)

1. S121 is a *readable spec*, not executable code — the Lava snippet in §2
   requires INRC hardware + the Lava framework, neither present.
2. The mapping table (§1) is the substantive content — it shows the LEGO
   arc's numpy LIFNet has a 1:1 native Loihi correspondence.
3. The §11-B-as-GPU-tautology escape claim is §96's insight made concrete:
   Loihi's `learning_rule` is a physical on-chip process. S121 names the
   Lava primitive; it does NOT prove the escape works (that needs a fire).
4. INRC access wall is *soft* (membership/survey) not *hard* (ethics, like
   organoid) — §95's classification. S121 could become fireable if access
   opens.
5. S121 honors LEGO.md's STEP-3 fence — it is a blueprint at the fence,
   not a crossing.
6. anima is hexa-lang/hexa-bio downstream-consumer; Lava is an Intel
   framework consumed read-only as a target spec, not edited.
7. The seed-1337 byte-equal init port (§2 `_seeded_*` helpers) ensures a
   Loihi run would be comparable to the numpy `lego_engine` reference.
8. g3: spec ≠ implementation ≠ fire ≠ emergence; capability claim 0.
9. necessary-not-sufficient (B-EMERGE-7) — a Loihi mapping spec does not
   move GOAL.
10. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
