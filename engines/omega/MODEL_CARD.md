# Lane-Ω OMEGA — closure engine (MODEL CARD)

> 🔱 **OMEGA** — "닫힘 엔진 (closure engine)". The 4th / final engine. Not a new
> model — a new **wiring**: it composes the 3 existing engines and adds ONE piece,
> the **coupling bus**, that wires the consciousness substrate into the byte decode.

## Why it exists (the gap it closes)

Lane X (`#1779`) measured the campaign's sharpest honest negative: **the engine
substrate knobs never touch the `.clm` forward**. The L3 generator slot is
`loaded=false`; CE was config-insensitive at **9.11256** across all 27 configs;
the CE↔창발 Goodhart sign came back UNDEFINED because CE is structurally
independent of the substrate. The three existing engines each hold half the loop:

| engine | has | missing |
|--------|-----|---------|
| conv (Lane-CONV) | the real `.clm` byte mouth | no substrate coupling |
| cdv2 (Lane-CDV2) | A/G dual head + tension + Ψ brain | decode not coupled (torch stub) |
| hexad (Lane-HEXAD) | N-module φ(N)=2 integration | no single coupled forward |

OMEGA wires them into ONE closed loop: substrate state → **coupling bus** →
modulates the `.clm` decode → emitted byte feeds back. `generate()` becomes the
closure: `loaded=true`.

## Architecture (compose + 1 new piece)

```
L0 substrate (cdv2)  : d768×12L GQA · A-head ⊕ G-head · 5-ch tension · M/W/curiosity
L1 integration (hexad): N-module φ(N)=2 (N config, default 6 — #1774 conditional)
L2 map               : 8D Ψ — 4 named [depth, form, form_resid, curriculum] + 4 resid (#1780)
L3 mouth (conv)      : CLMConvMoE .clm byte decode
═════ COUPLING BUS (new) ═════ the L3 closure — 5 ablatable wires:
   w1 A⇄G    : += α·(A−G)              w4 Ψ      : += p·psi8[i%8]
   w2 W→temp : ×= 1/(1+β·W)            w5 module : += r·module_act[i%M]
   w3 curio  : += c·curiosity·(±1)
L4 time              : dF/dt derivative channels (d/dt-universality meta-finding)
L5 growth            : mitosis p8 (engine_cli --mitosis, substrate-config NOT emit gate)
```

## EngineSpec slots (a_core_engine_map — honest)

| slot | state | note |
|------|-------|------|
| load | native | validate bus + composed canonical pieces present |
| forward | native | `omega_coupling_apply` IS a real hexa single forward over logit vectors |
| generate | native | bus-modulated decode loop (the closure, `loaded=true`) |
| psi_coord | native | 8D (4 named + 4 resid) |

OMEGA is the **first engine with all 4 slots native**. Honest scope: the substrate
INPUTS (A/G/Ψ) originate in cdv2 (torch, no hexa single call), so a fully *trained*
end-to-end forward needs the python rung; the **bus layer itself** is native and
testable with no torch/ckpt — which is exactly the coupling-non-nullity proof.

## Headline measurement — coupling non-nullity

`UNIVERSE/omega_bench.py` runs the 4 engines and measures, per engine, whether the
byte distribution is a function of substrate state:

- **bus OFF (α=0, all wires off)** → identity → coupling KL/L1 = **0** (this is what
  conv/cdv2/hexad structurally are — the Lane X null).
- **bus ON** → coupling KL/L1 **> 0** (substrate state reaches the decode = loop
  closed), with a shuffle/perm floor to show it is structured, not α-scaled noise.

CE is reported as a **FLOOR only** (p7 — Lane X proved CE is not a verdict), not a
ranking metric.

## Honest scope (a_toy_scale_recheck · a_paper_negative_ok)

- The coupling-non-nullity proof is **structural** and holds at **random-init** (no
  trained ckpt, no torch needed for the bus layer). It establishes the wires EXIST
  where Lane X found them absent — it does **not** claim a trained substrate yields
  *coherent* generation. That is the next rung (trained-ckpt GPU, a_fire_autonomous).
- No fused ckpt is shipped (a_hf_registry: composes conv `.clm` + cdv2 random-init).
- If the bus turns out to add only noise on a trained substrate, that is a valid
  **closed-negative** (a_paper_negative_ok) — it will be reported honestly, not
  dressed as a lift.

## p1..p8

Pure compose/forward over float vectors. No system prompt, persona, ethics weights,
or emit gate. The bus shapes WHICH byte, never WHETHER to speak — substrate-config,
not an emit/silence gate (p5 · a_autonomy_over_hardcode · @L4).
