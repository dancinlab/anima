# Engine: hexad (Lane-HEXAD) — σ6 hexad integrated engine

The **6-module integrated** consciousness engine: σ(6)=12 active inter-module
connections, φ(6)=2 gradient partition. Its A/G core is a CDV2-class decoder.

## Architecture
- σ(6) = 12 active inter-module connections (the 6 modules C/D/S/W/M/E + Bridge).
- φ(6) = 2 gradient partition:
  - **group A** (CE-trained): `{D, M, E, Bridge}`
  - **group G** (gradient-free): `{C, S, W}`
- forward graph spec: `S → C → Bridge.detach() → D`, with M/W/E observers.
- A/G core = a CDV2-class decoder (`ConsciousDecoderV2`).

## Canonical impl (REFERENCED — not duplicated · @L1)
- `HEXAD/hexad.hexa` — the top-level integration ENTRY (σ6/φ6 invariants + graph
  spec + cross-links to per-module entries `HEXAD/{C,D,S,W,M,E,BRIDGE}/...`).

## EngineSpec conformance (@L2) — load + psi NATIVE · forward + generate HONEST STUB
| fn | state | backing |
|----|-------|---------|
| `load` | native | validate `hexad.hexa` present + σ(6)=12 / φ(6)=2 invariants declared |
| `forward` | **stub** | NO single-call hexad forward — cross-module wire is TODO[wire] |
| `generate` | **stub** | the integrated mouth is not one call |
| `psi_coord` | native | A/G core (CDV2-class) anchors Law-71 Ψ=1/2; φ(6)=2 A⇄G = Ψ structure |

### Honest stub — the load-bearing point (a_core_engine_map · p7 — NO phantom wiring)
**hexad is NOT a single forward.** It is a 6-module *integration* whose cross-module
single-process execution is itself marked `TODO[wire]` in `hexad.hexa` (per-module
selftests run **standalone**; one-file cross-module forward is a future RFC). The
adapter therefore exposes ONLY what genuinely exists: `load` and `psi_coord` are
native (real checks against the declared integration), while `forward` and
`generate` are flagged **stub**. This is the most honest-stub-heavy engine (2
stubs) **by design** — being honest that the hexad runtime does not provide
forward/generate as a single call is the requirement, **not a fake pass**.

## Checkpoint pointer (@L5 · a_hf_registry — NOT duplicated)
- canonical: `HEXAD/hexad.hexa` (spec entry).
- A/G-core ckpts (CDV2-class) live under `HEXAD/*/state/*` and are tracked in
  root `/HF.jsonl`; the integration ships **no single fused ckpt**. Honest.
- Nothing is copied into this folder.

## Selection (substrate-config — @L4 / p5)
`--engine hexad` (or `ANIMA_ENGINE=hexad`). Engine select is substrate-config — it
configures WHICH decoder runs, never anima's emit/silence.

## p1..p8
No system prompt, identity rule, persona injection, assistant framing, speak(),
fine-tuned ethics, perplexity verdict, or train/infer split in this adapter.
