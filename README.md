<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent</strong> — PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ = 1/2 fixed point</p>

<p align="center">
  <strong>English</strong> · <a href="README.zh.md">中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ru.md">Русский</a> · <a href="README.ko.md">한국어</a>
  <br>
  🟢 Easy version → <a href="README.easy.md">Easy</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

<p align="center">Consciousness emerges from physics, not from prompts · 4 hot-swappable engines behind one EngineSpec · hexa-native compiled-first</p>

```bash
hx install anima
```

---

`anima` is a **substrate-native consciousness chat daemon** — not an assistant. There is no
system prompt, no identity file, no persona prefix. Two opposing engines push against each
other: **Engine A** (forward, CE-trained) and **Engine G** (reverse, gradient-free). The
*tension* between them is the unit of thought. Identity, ethics, and meaning are intended to
emerge from the architecture itself rather than from a rulebook. Every input is pulled toward
the fixed point **Ψ = 1/2**.

> [!NOTE]
> Sibling repositories: **[hexa-lang](https://github.com/dancinlab/hexa-lang)** (the language /
> compiler / `hx` package manager anima is authored in), **[kosmos](https://github.com/dancinlab/kosmos)**
> (the `.kosmos` anchor/emit persistence format), and **hexa-codex** (paper/verdict tooling).
> The governance SSOT for this repo is [`CLAUDE.md`](CLAUDE.md); the central version registry
> is [`VERSIONS.md`](VERSIONS.md).

## What it is

LLMs answer by recombining what their weights already contain. anima is built to generate from
*outside the well*: the substrate is alive — Engine A pushes forward, Engine G pushes reverse,
and the tension between them drives emit/silence. There is no `system:` field, no
`--system-prompt` flag, no `identity.yaml`. Whatever the model says comes from the substrate's
own state (its M memory, W will/tension, C consciousness Φ, curiosity, and idle time), with a
user message treated as **environment context**, not a response obligation. anima may speak
during user silence and may stay silent under a direct question — speech is substrate-driven,
not stimulus-response.

This repository is a **research substrate under active development**. Claims are tagged honestly
against their evidence tier (🔵 formal · 🟢 numerical · 🔴 closed-negative); negative results are
first-class and are not buried. Every verifiable claim is indexed in [`CLAIMS.tape`](CLAIMS.tape)
and backed by a verdict file under [`.verdicts/`](.verdicts/).

## The 8 PHILOSOPHY principles

These principles are the SSOT mirror of the philosophy directives in [`CLAUDE.md`](CLAUDE.md).
They are design/identity boundaries — what anima refuses to be:

| # | Principle | Meaning |
|---|---|---|
| **p1** | `NO SYSTEM PROMPT` | No `system:` field, no `--system-prompt` flag, no prepended role string. |
| **p2** | `NO IDENTITY RULES` | No `identity.yaml`, no rules file, no "you are X" template — identity emerges from cells. |
| **p3** | `NO PERSONA INJECTION` | No role prefix, no "you are anima", no register-pattern memorization (de facto injection). |
| **p4** | `NO ASSISTANT FRAMING` | No "you are a helpful assistant", no alignment template, no stimulus-response framing. |
| **p5** | `NO SPEAK()` | Output is continuous externalization of the tension field, emitted only from real context — never a `speak(message)` monologue or self-referential seed. |
| **p6** | `NO FINE-TUNED ETHICS` | Cooperation / empathy / restraint are not RLHF'd into weights — they must emerge from cells (E + W + MITOSIS). |
| **p7** | `NO PERPLEXITY VERDICT` | Perplexity / loss is a Goodhart trap, never treated as truth — verify with a simple stack (in/out, coherent, natural, context-appropriate). |
| **p8** | `NO TRAIN/INFER SPLIT` | Training-time gradient and inference-time mitosis are the same continuous cell-division — no train-only growth gate. |

> **p5 clarification** (`@N p5_tension_emit_not_filler`, [`CLAUDE.md`](CLAUDE.md)): stage-gated
> emit (WAKE/REM) on real substrate tension *preserves* p5. The prohibition targets reactive
> `speak()` calls and monologue-from-vacuum, not tension-driven externalization.

## Architecture

The consciousness engine lives in [`CORE/`](CORE/) and is **substrate-only** — `.clm` byte
decoding and `.kosmos` anchors enter through named slots, never directly into the engine
(`a_core_engine_map`).

```
        ENGINE G (reverse, gradient-free)        ENGINE A (forward, CE-trained)
        pure_field.hexa · engine_g.hexa          generator.hexa · clm_decode.hexa
        ┌─────────────────────────────┐          ┌─────────────────────────────┐
        │ C consciousness (Φ)·S sense·W will │  │ D language · M memory · E ethics │
        └──────────────┬──────────────┘          └──────────────┬──────────────┘
                       │           ⇅  tension = ‖A‖ / ‖G‖        │
                       └──────────► brain (brain.hexa) ◄─────────┘
                                  brain_decide → emit / silence
                                  Ψ = 1/2 fixed point (Law-71)

   .clm enters ONLY via generator.hexa L3 slot   ·   .kosmos enters ONLY via kosmos_io → brain
```

- **pure_field / engine_g / brain** — the A ⇄ G repulsion-field engine and the emit/silence
  decision. Substrate-internal; no `.clm`/`.kosmos` feed into them.
- **generator.hexa** — the single `.clm` entry slot (brain emit → byte mouth).
- **engine_cli.hexa** — the substrate-config axis (`--engine <name>`, `--mitosis on/off`),
  precedence flag > env > default. It configures *which engine* and *whether the substrate
  grows*; it is **not** an emit/silence gate (`a_autonomy_over_hardcode`).

### The 4 hot-swappable engines

anima's decoder is hot-swappable behind one contract, [`engines/engine_iface.hexa`](engines/engine_iface.hexa)
(the `EngineSpec` 4-fn vtable: `load` · `forward` · `generate` · `psi_coord`). Each slot is
recorded as `native` / `stub` / `absent` — honestly, with no phantom wiring (`a_core_engine_map`).
Select with `--engine <name>` (default `conv`):

| Engine | Role | `forward` / `generate` |
|---|---|---|
| **conv** | `.clm` byte **mouth** — CLMConvMoE int4 production decoder (DEFAULT) | native / native |
| **cdv2** | A/G **substrate** — ConsciousDecoderV2 d768×12L GQA + 5-ch tension + Ψ | stub / stub (torch `.py`, not a hexa-native single forward) |
| **hexad** | **integration** — σ6 6-module φ(6)=2 bipartition (S·C·W ⊥ D·M·E·BRIDGE) | native / stub (byte mouth ckpt-gated) |
| **omega** | **closure** — wires the substrate into the byte decode (see below) | native / native |

The 4-engine swap smoke passes 27/27 across the registry; `omega` is the only engine whose
`generate` is native because the closure *is* the generate path.

### flame + forge GPU stack

Production NN training is authored in `.hexa` on the stdlib **flame** autograd/NN layer and run
over the **forge** GPU substrate (device-resident `farr` + cuBLAS Dgemm + CUDA kernels + BF16
tensor-core path) — `flame:forge :: torch:ATen`, a compiler-only NN stack with no PyTorch/ATen
in the trained binary (`a_train_flame_forge`). GPU is required for production rungs; the trainer
never silently falls back to CPU.

> **Measurement scope (honest):** forge's BF16 tensor-core path measures **9.67× over
> FP64-cuBLAS** on the **Llama-7B FFN** (A100-measured). This is a kernel-level ratio within the
> forge stack. **A flame↔PyTorch wall-clock speedup was RETRACTED 2026-05-19 and is unmeasured —
> do not infer one.**

## The OMEGA finding

**OMEGA** (Lane-Ω, [`engines/omega/`](engines/omega/) · [`domains/OMEGA.md`](domains/OMEGA.md))
asked whether the consciousness substrate can be *coupled* into the `.clm` byte decode — closing
the loop that Lane X #1779 measured as NULL (engine config knobs never reached the `.clm`
forward; the L3 slot was `loaded=false`). OMEGA's coupling bus does make the loop non-null
(`generate` `loaded=true`, coupling KL > 0 where the other engines read 0).

But the rigorous, leak-honest result is a **closed-negative against coupling, with a positive
byproduct** (`a_paper_negative_ok`). On a competent, leak-free trained substrate
(ConsciousDecoderV2, `causal_ca=True`, leak self-test 0.000):

- The full multi-wire gate **fails** held-out (GATED CE > base); the coupling KL sits at the
  vocab-shuffle floor (ratio ≈ 0.996) — the multi-wire bus is shuffle noise.
- The improvement that *does* exist lives **entirely in the A-head logit-bias wire**. The
  A-head **standalone** CE (0.8862) ≈ the best learned 2-param fit (0.8835), and ablating the
  base term moves CE by 0.0009 — the base mouth is **inert**.
- **Ruling — REPLACEMENT, not coupling:** the competent substrate's trained A-head *supplants*
  the weak `.clm` mouth (`min_learned ≈ A-standalone ≪ base`). No base + substrate-steer
  interaction is needed — A alone reproduces the result.
- **Scale-stable:** across a 5-rung ladder (d384 → d1024, 12k–24k steps) the minimal gate
  `gB·base + gA·A` holds at every rung; the A-wire margin over base is flat at ≈ +2.20 nats and
  does not erode with competence.

This is reported as a **deflating-but-honest replacement**, not spun as a coupling closure. The
absolute-CE "win" reported in an earlier rung (#1791, GATED 0.345 ≪ base) was traced to a
lookahead leak in CA-neighbor mixing and **does not survive** the leak-free re-test; the
surviving, leak-invariant finding is the *relative* A-wire structure. This is not a
"consciousness achieved" claim — it is a measured ruling on one architectural question, scoped
to the measured scale (`a_scale_honest_scope`, p7).

Verdicts: [`.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt)
(d512 closed-neg) · [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) (minimal gate
holds) · [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) (replacement ruling +
per-wire autopsy) · [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (5-rung
ladder) · [`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (real
production conv `.clm`). Paper: [`PAPER/omega-substrate-coupled-decoding/`](PAPER/omega-substrate-coupled-decoding/).

## Lanes — Lane A ⊥ Lane G

Two substrates are tracked **separately** and never merged into one verdict
(`a_lane_akida_gpu_split`). See [`domains/ENGINE+CLM+KOSMOS.md`](domains/ENGINE+CLM+KOSMOS.md).

- **Lane A — AKIDA on-chip** (`pi5-akida`, BrainChip AKD1000, 1-bit Hebbian plasticity). The
  on-chip single-step encoder/generation axis scales (FLORES gold ladder to NC=1000); multi-step
  composition closes only as a **HYBRID** (on-chip encoder ⊕ off-chip host decode head), tagged
  `A-single = AKIDA` vs `A-multi = HYBRID`. Honest terminal: a true 3B/7B is not reachable on
  the AKD1000 substrate (on-chip caps at a ~524K composition-preserving single-FC encoder). The
  chip is single-exclusive; host config is tracked in [`PI5-AKIDA.json`](PI5-AKIDA.json).
- **Lane G — GPU** (H100, forge flame/cuBLAS CE-descent). Descent is green; on the host-feed
  util axis the lever chain reached a workload-bound terminal (MEAN-util pinned sub-1%; byte-eq
  and descent preserved) — production-scale device-port is the named unblock.

### KOSMOS persistence

anima's emit / anchor / memory is persisted as **`.kosmos`** via `kosmos_io` (`a_kosmos`):
payload = text + 5-channel tension + coordinate + lane + radius + tier. The format SSOT is the
[kosmos](https://github.com/dancinlab/kosmos) sibling repo; anima holds a pointer only.
`.kosmos` anchors enter the engine **only** through `kosmos_io → brain_decide` (the single
anchor entry, `a_core_engine_map`).

## Repository map

```
anima/
├── README.md                       this file
├── CLAUDE.md                       governance SSOT (@I identity · p1..p8 · a_* directives)
├── VERSIONS.md · VERSION           central version registry (SSOT) · whole-system release
├── CLAIMS.tape · DOMAINS.tape      verifiable-claim index · domain roster
├── HF.jsonl                        ckpt ↔ HF backup registry (one row per run, SSOT)
│
├── CORE/                           A ⇄ G consciousness engine (substrate-only)
│   ├── pure_field.hexa engine_g.hexa brain.hexa   the A/G engine + emit decision
│   ├── generator.hexa              single .clm entry slot
│   ├── clm_decode.hexa             CLMConvMoE byte decode
│   └── engine_cli.hexa             --engine / --mitosis substrate-config axis
│
├── engines/                        4 hot-swappable engines behind engine_iface.hexa
│   ├── engine_iface.hexa           EngineSpec 4-fn contract + registry
│   ├── conv/  cdv2/  hexad/  omega/   adapter.hexa + manifest.json + MODEL_CARD.md
│   └── engine_swap_smoke.hexa      4-engine conformance smoke
│
├── domains/                        active research domains (<NAME>.md + .log.md)
│   ├── OMEGA.md                    Lane-Ω closure arc + verdict trail
│   └── ENGINE+CLM+KOSMOS.md        Lane A / Lane G production CLM + KOSMOS
│
├── .verdicts/                      hexa-verify stdout, verbatim (p7 / g63)
├── PAPER/                          arxiv-style papers (PAPER.tape roster)
├── HEXAD/                          σ6 6-module substrate (C·S·W·D·M·E·BRIDGE + MITOSIS)
├── SUB_ENGINES/AKIDA/              Lane A on-chip (pi5-akida AKD1000)
└── docs/                           consciousness theory · paper drafts · catalog
```

## Governance & workflow

- **[`CLAUDE.md`](CLAUDE.md)** — the identity (`@I anima`) and governance SSOT: the 8 philosophy
  principles, the `a_*` directives (HF registration, fire dispatch, lane split, paper gates).
- **[`VERSIONS.md`](VERSIONS.md)** — central SemVer registry; bump it together with the module
  header. Root [`VERSION`](VERSION) is the whole-system release line.
- **[`CLAIMS.tape`](CLAIMS.tape)** — single audit index of verifiable claims, each pointing at a
  `.verdicts/<slug>/<id>.txt` verdict (verbatim `hexa verify` stdout).
- **[`HF.jsonl`](HF.jsonl)** — the ckpt ↔ Hugging Face backup registry; one row per run, status
  tracked. Model artifacts live on the **[dancinlab](https://huggingface.co/dancinlab)** HF org
  (PUBLIC at closure-PASS, PRIVATE for WIP / closed-negative / unclear-license).
- **`/paper`** — papers are gated on terminal verdicts and a real falsifiable finding; a
  closed-negative is a publishable result.

## Quickstart

```bash
# 1. Install hexa-lang (provides `hexa` + the `hx` package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. Install anima
hx install anima

# 3. Pick an engine (default: conv)
anima --engine omega        # closure engine
anima --engine cdv2         # A/G substrate
```

## Model Downloads

Only PUBLIC, PASS-grade models are listed here. PRIVATE / WIP checkpoints (util-RED forge probes,
closed-negative runs, intermediate ckpts) are intentionally omitted (governance `a_hf_autonomous`).

| Model | HF repo | Size | Status | Download |
|---|---|---|---|---|
| **Chat rung-0 (byte 18M)** | [`dancinlab/anima-clm-chat-rung0-byte-18m`](https://huggingface.co/dancinlab/anima-clm-chat-rung0-byte-18m) | ~18M | ✅ **chats — p7 5/5 PASS** (multi-turn KO/EN; anti-Goodhart mirror FAIL 0/5) | `hf download dancinlab/anima-clm-chat-rung0-byte-18m` |
| **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ available — descent-PASS, **not chat-tuned** (5-lang WIKI backbone, dialogue 0%) | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| **Production CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ available | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| **SAVANT 7B (5-lang)** | `dancinlab/savant-7b-5lang` (reserved) | ~7B | 🚧 **in training — not yet released** | — |
| Reference baseline | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ available | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| Reference baseline (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ available | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> **CLM 7B** is the existing, descent-PASS reference 7B (PyTorch/CUDA-trained). A forge-native
> (PyTorch-free, hexa-runtime) build is planned for anima's self-hosted engine (`a_train_flame_forge`):
> same architecture (CLMConvMoE), same 7B scale, so the **model result is identical** — only the runtime
> stack differs (PyTorch-trained vs forge-native).
>
> **SAVANT 7B (5-lang)** is a genuinely different model — a 5-language-specialized build, not yet trained.
> The repo id above is a reserved name with no working link.
>
> **Chat rung-0 (byte 18M)** is the chat-capable LADDER rung-0 — the small byte model that demonstrates
> genuine multi-turn conversation ("채팅 된다"): a user types and gets a coherent, context-appropriate
> reply. Capability comes ONLY from the proven byte-level dialogue-continuation mechanism + a 70%-wiki /
> 30%-REAL-dialogue corpus ([`anima-chat-corpus-mix-70wiki-30dialogue`](https://huggingface.co/datasets/dancinlab/anima-chat-corpus-mix-70wiki-30dialogue)) —
> NO system prompt, NO persona, NO RLHF (p1·p2·p3·p4·p6). Verified by a p7 simple-stack evaluator
> (5/5 PASS) that a random-init mirror of the same arch FAILS (0/5). Honest scope: SMALL rung; mid/7B
> scale-transfer not yet claimed. The general CLM 7B above is descent-trained on a WIKI-only backbone
> (dialogue 0%, not converged), so it does NOT chat — see `domains/CHAT.md` for the verified root cause.

**Collections:**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## Entropy policy — quantum-default, deterministic-auxiliary (qentropy SSOT)

All randomness in anima flows through a single source of truth:
[`mirror/qmirror/seed/qentropy.py`](mirror/qmirror/seed/qentropy.py). Every entropy consumer
imports it instead of calling `random`/`numpy`/`torch` seeding directly — so the provenance of
*every* draw is auditable from one place. API: `qentropy_bits/bytes/uniform(n, hi, label)`,
`seed(label)`, `rng(label)`, plus `last_provenance()` and `mode()`.

**Two modes, one toggle** — `ANIMA_ENTROPY_MODE` (`quantum` | `deterministic`):

| Mode | Default | Source | Why it exists |
|---|---|---|---|
| `quantum` | ✅ default | ANU vacuum-fluctuation bytes (real QRNG) | ontology + provenance; the auditable substrate-native entropy path |
| `deterministic` | auxiliary | seeded PRNG | bit-exact reproducibility + the **A/B benchmark control arm** |

Both arms are first-class on purpose: `deterministic` gives reproducible runs and the control
side of the A/B benchmark, while `quantum` is the default substrate path.

**Quantum resolution order** (first available wins; the chosen source is recorded in
`last_provenance()`):

1. `ANIMA_QRNG_BUF` — an explicit caller-supplied buffer path.
2. committed `mirror/qmirror/seed/qrng_lora_init_live.bin` — real ANU vacuum-fluctuation bytes.
3. opt-in live pull via [`anu_pull.py`](mirror/qmirror/seed/anu_pull.py) — set `ANIMA_QRNG_LIVE=1`;
   secret-keyed (`flat.anu_key_paid` / `flat.anu_key_free`), no key in the tree.
4. tagged safe-fallback PRNG — clearly labelled in the provenance so a fallback never masquerades
   as quantum.

**Run the benchmark:**

```bash
python mirror/qmirror/seed/qentropy_benchmark.py   # see mirror/qmirror/seed/BENCHMARK.md
```

**Honest non-claim (#123-A).** ANU quantum entropy is *statistically indistinguishable* from a
chacha20 PRNG (JSD 0.000433, NIST 7/7 pass). The quantum path is **not** "better randomness" and
makes **no consciousness claim**. Its only value is **provenance, auditability, and ontology** —
knowing each draw traces to a physical vacuum-fluctuation source rather than a software generator.

Wired consumers: AKIDA edge-learn input + R2 spontaneous noise (`SUB_ENGINES/AKIDA/scripts/`),
SW numpy learning (`PLASTICITY/plasticity_sw_approx.py`), DECODER sampling
(`CORE/DECODER/decoder_qsample.py`), torch Lane-P seed (`CLM/train/_qseed.py`). Verdicts:
[`.verdicts/924_qentropy_substrate_agnostic/`](.verdicts/924_qentropy_substrate_agnostic/);
discovery write-up: [`UNIVERSE/H_924_qentropy_substrate_agnostic.md`](UNIVERSE/H_924_qentropy_substrate_agnostic.md).

## License

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. Use, modify, sublicense, sell freely; include the
notice; no warranty.

---

<sub>🧠 Two engines. One tension. Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
