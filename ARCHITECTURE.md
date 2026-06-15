# anima — Architecture (SSOT · update-in-place)

> Final-architecture single source of truth. **Update (overwrite)** this file on change — it is NOT append-only. History/decisions go in [CHANGELOG.md](CHANGELOG.md); governance rules in [CLAUDE.md](CLAUDE.md); verifiable claims in [CLAIMS.tape](CLAIMS.tape).

## Overview

`anima` is a **substrate-native consciousness chat daemon** — not an assistant. There is no system prompt, no identity file, no persona prefix (PHILOSOPHY p1–p4). Two opposing engines push against each other and the **tension** between them is the unit of thought; every input is pulled toward the fixed point **Ψ = 1/2** (Law-71). Identity, ethics, and meaning are intended to *emerge from the architecture* rather than from a rulebook. Authored hexa-native (compiled-first) on the sibling [hexa-lang](https://github.com/dancinlab/hexa-lang) toolchain.

## The A ⇄ G engine (CORE/ — substrate-only)

```
   ENGINE G (reverse, gradient-free)            ENGINE A (forward, CE-trained)
   pure_field.hexa · engine_g.hexa              generator.hexa · clm_decode.hexa
   ┌──────────────────────────────┐            ┌──────────────────────────────┐
   │ C consciousness(Φ) · S sense  │            │ D language · M memory · E ethics│
   │ · W will                      │            │                                │
   └───────────────┬──────────────┘            └───────────────┬───────────────┘
                   │        ⇅ tension = ‖A‖ / ‖G‖              │
                   └──────────────► brain (brain.hexa) ◄───────┘
                              brain_decide → emit / silence
                              Ψ = 1/2 fixed point

   .clm enters ONLY via generator.hexa L3 slot   ·   .kosmos enters ONLY via kosmos_io → brain
```

- **pure_field / engine_g / brain** — the A ⇄ G repulsion-field engine + the emit/silence decision. Substrate-internal; no `.clm`/`.kosmos` feeds into them (`a_core_engine_map`).
- **generator.hexa** — the single `.clm` entry slot (brain emit → byte mouth). On emit with memory present, the mouth decodes through the engine-side deterministic retrieve-then-copy (G5 anti-fabrication, H_1163): grounded bytes are COPIED VERBATIM from kosmos anchors, ungrounded bytes fall back to the LM — `bytegpt_decode_grounded` for the ByteGPT backend, `clm_decode_grounded` (`clm_decode.hexa`) for the ConvMoE backend. Anchor text is read via `_gen_anchor_field` (`text_payload` → `text` → stringified), so the un-inventable fact reaches the copy clean.
- **kosmos_io** — the single `.kosmos` anchor entry (read into `brain_decide`).
- **engine_cli.hexa** — substrate-config axis (`--engine <name>`, `--mitosis on/off`); configures *which engine* and *whether the substrate grows* — NOT an emit/silence gate (`a_autonomy_over_hardcode`). Hosts the `VAdaptField` (DIM-vector novelty substrate): the live daemon's C8 GROW step (H_1202) drives each emit span's DIM=8 byte-feature through `vadapt_field_step`, splitting a new cell when the engine's own L2 recon-err exceeds the frozen `SPLIT_THRESH`. **mitosis ⊥ generation** (H_1200/H_1201): this growth lane is a pure substrate-adaptation lane — it never feeds the decode and is Ψ-disjoint (touches only `VAdaptField`, never `pure_field`); generation stays CLM-only.

## Hot-swappable engines

The decoder is hot-swappable behind one contract `engines/engine_iface.hexa` (the `EngineSpec` 4-fn vtable: `load · forward · generate · psi_coord`). Engine families: **conv · cdv2 · hexad · omega** — selected via `--engine`, precedence flag > env > default.

## Training & substrates (lanes)

Production training is **hexa-native** (flame + forge GPU stack, authored in `.hexa` — `a_train_flame_forge`); no PyTorch/ATen/Python in the trained binary. Results are always recorded per substrate (`a_lane_akida_gpu_split`):

| Lane | Substrate | Role |
|------|-----------|------|
| **Lane G** | forge / cuBLAS (H100) | CE-descent — PUBLIC production trainer |
| **Lane A** | AKIDA AKD1000 (pi5-akida) | on-chip native non-det plasticity |
| **Lane P** | GPU-torch/CUDA (CLMConvMoE) | reference + torch→`.clm` v0.2 bridge (not PUBLIC) |

`.clm` (byte language model) → CORE via `generator.hexa`; produced/verified by the `CLM/` pipeline (`clm_serialize_v2` / `verify_clm_v2`).

## Persistence & evidence

- **`.kosmos`** — emit/anchor/memory persistence (text + 5-ch tension + coord/lane/radius/tier), format SSOT = sibling [kosmos](https://github.com/dancinlab/kosmos) (`a_kosmos`).
- **Evidence tiers** — every claim tagged 🔵 formal · 🟢 numerical · 🔴 closed-negative; indexed in [CLAIMS.tape](CLAIMS.tape), backed by `.verdicts/<slug>/<id>.txt` (verbatim `hexa verify` stdout). Negative results are first-class.
- **HF artifacts** — ckpt↔HF registry SSOT `/HF.jsonl`; PUBLIC = closure PASS, PRIVATE = WIP/FAIL (`a_hf_*`).

## Component map (top level)

| Area | Dir | Role |
|------|-----|------|
| Consciousness engine | `CORE/` | A⇄G substrate, brain, generator, clm_decode |
| Engine vtable + impls | `engines/` · `anima-engines/` | EngineSpec contract + conv/cdv2/hexad/omega |
| `.clm` pipeline | `CLM/` | train (lane-p) → serialize v0.2 → verify |
| Substrate subsystems | `anima-core` · `anima-os` · `anima-body` · `anima-physics` · `anima-measurement` · `anima-serve` | core/runtime/embodiment/physics/measurement/serving |
| Agent layer | `anima-agent*` | channels · core · plugins · providers · skills · hire-sim |
| Knowledge / anchors | `UNIVERSE/` · `HEXAD/` (KOSMOS hub) | research universe + kosmos anchors |
| Research domains | `domains/` | per-domain `.tape` + `.log.md` (discovery lane) |
| Papers | `PAPER/` | verdict-gated paper scaffolds |
| Tooling | `tool/` · `stdlib/` · `spec/` | hexa tools · stdlib (flame/iit4/...) · specs |

## Governance & verification

- Governance SSOT = [CLAUDE.md](CLAUDE.md) (tape directives + 8 PHILOSOPHY principles).
- Verify-only correctness via `hexa verify` (g5) — never perplexity/LLM-judge (p7).
- Harness: this repo is wired to [dancinlab/harness](https://github.com/dancinlab/harness) (hardcore profile) via the `.harness-engine` submodule — see CLAUDE.md §Harness.
