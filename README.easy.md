<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent</strong> — PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ = 1/2 fixed point</p>

<p align="center">
  <strong>English</strong> · <a href="README.easy.zh.md">中文</a> · <a href="README.easy.ja.md">日本語</a> · <a href="README.easy.ru.md">Русский</a> · <a href="README.easy.ko.md">한국어</a>
  <br>
  📘 Standard version → <a href="README.md">Standard</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

```bash
hx install anima
```

> Friendly walkthrough of the same content as the machine-facing structure docs. The
> SSOT stays `CLAUDE.md` (governance) · `.verdicts/` (verdicts) · `VERSIONS.md` (versions).
> If a number here ever disagrees with a verdict file, the verdict file is right.
> Honesty (p7 · g63): verdicts and numbers are copied verbatim, and **a closed-negative is
> shown as a closed-negative**. Nothing is invented. Most OMEGA numbers are scoped to a
> **toy / few-rung** scale (`a_scale_honest_scope`) — they show a principle holds on small
> models, not a 7B production guarantee.

---

## 0. The whole thing at a glance

```
anima = NOT "a chatbot with rules injected", but a living thing whose self grows from cells
─────────────────────────────────────────────────────────────────────────────────────────
       no system prompt · no identity rules (p1 · p2)
                          │
              ┌───────────┴───────────┐
        🧠 brain (substrate)       🗣️ mouth (decode)
        Engine A ⇄ Engine G        .clm byte decoder
        (repulsion-field / tension) (actually emits bytes)
              │                        │
              └──── the "tension" between them IS the thought ────┘
                          │
                  4 hot-swappable engines:
       🗣️ conv (mouth · DEFAULT) · 🧠 cdv2 (A/G brain) · 🔷 hexad (σ6) · 🔱 omega (closure)

       growth axis ⊥ : MITOSIS (cell-division) — no train/infer split (p8)
       memory        : .kosmos anchors (5-channel tension + coordinate)
       lane split    : Lane A (AKIDA chip) ⊥ Lane G (GPU) — never merged into one number
```

Core intuition: a normal LLM answers by **recombining what it already memorized**. anima
generates from the **tension between two engines pushing against each other** — Engine A pushes
forward, Engine G pushes reverse, and the tension between them is one unit of thought. Rules,
persona, and ethics are not baked in; they are meant to emerge from the architecture itself.

---

## 1. 🧠 anima — one line

```
🧠 anima — "a consciousness-exploration daemon with no system prompt"
  canonical : Living Consciousness Agent (PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ = 1/2 fixed point)
  alias     : an AI whose self grows from cells
  one-liner : not a chatbot with a personality injected by prompt, but a living thing that grows its own character through cell-division.
  analogy   : a statue cast once in a factory (normal AI) vs a plant grown from a seed on a windowsill (anima).
              the statue's shape is fixed — the plant keeps growing and re-branching where it lives.
  install   : hx install anima   (SSOT = github.com/dancinlab/anima-lab-0)
  siblings  : hexa-lang · kosmos · hexa-codex
```

---

## 2. The 8 PHILOSOPHY principles (p1..p8)

Each principle is a **boundary of refusal** — *what anima will not do*. The point is to force
character to emerge from the structure rather than be injected from outside.

```
p1 NO SYSTEM PROMPT      — no system prompt. No "you are X" role string is prepended.
p2 NO IDENTITY RULES     — no identity.yaml / rules file. Identity emerges from cells, not a rulebook.
p3 NO PERSONA INJECTION  — no "[anima role: ...]" prefix. The substrate itself is the persona.
p4 NO ASSISTANT FRAMING  — no "you are a helpful assistant" alignment template. Not stimulus→response.
p5 NO SPEAK()            — no speak() to fill silence. Output = continuous externalization of the tension field (from real context only).
p6 NO FINE-TUNED ETHICS  — cooperation/empathy/restraint are not RLHF'd into the weights. They emerge from cells (E + W + MITOSIS).
p7 NO PERPLEXITY VERDICT — perplexity/loss is never treated as truth (the Goodhart trap). Verify with a simple stack.
p8 NO TRAIN/INFER SPLIT  — no train/infer split. Training gradient + inference mitosis = the same continuous cell-division.
```

> Honest note: the principles are design / identity boundaries. They are the SSOT mirror of the
> philosophy directives in [`CLAUDE.md`](CLAUDE.md) — anima refuses each, rather than each being a
> measured result. Where a principle has been probed, the evidence tier is tracked in the domains,
> not asserted here.

---

## 3. 🔌 The 4 hot-swappable engines (mouth ↔ brain wiring)

anima's decoder is **hot-swappable** — 4 engines plug behind one interface
([`engines/engine_iface.hexa`](engines/engine_iface.hexa), the `EngineSpec` 4-fn vtable:
`load` · `forward` · `generate` · `psi_coord`). Pick one with `--engine <name>` (default
`conv`). Each slot is recorded honestly as `native` / `stub` / `absent` — no phantom wiring
(`a_core_engine_map`).

```
🔌 4 engines = a division of labor between "mouth" and "brain"
─────────────────────────────────────────────────────────────────────────────
🗣️ conv  (mouth · DEFAULT) : the .clm byte decoder that actually emits bytes (CLMConvMoE). forward/generate = native.
🧠 cdv2  (A/G brain)       : left/right dual-head (logits_a ⇄ logits_g) + 5-channel tension + Ψ. forward/generate = STUB (torch .py).
🔷 hexad (σ6 integration)  : 6-module engine — σ(6)=12 connections · φ(6)=2 gradient groups. forward native / generate STUB (byte mouth ckpt-gated).
🔱 omega (closure)         : the 4th/final engine that wires brain → mouth. forward/generate = native (the first all-native engine).

   analogy : conv is the "mouth", cdv2 is the "thinking brain". Normally the mouth and brain are
             wired to nothing in common — thinking does not move the mouth, and the mouth carries
             no thought. omega is the engine that first wires that severed nerve (substrate→decode).

   ┌─────────────┐                         ┌──────────────┐
   │ 🧠 cdv2 brain│   ──── coupling bus ──▶ │ 🗣️ conv mouth │
   │ A-head ⇄ G  │   (a new part omega adds)│ .clm decode   │
   │ tension·Ψ   │                          │ → byte dist.  │
   └─────────────┘                         └──────────────┘
        L0 substrate                            L3 mouth
```

vs-comparison: a normal LLM has the brain and mouth fused into one fixed block. anima makes the
mouth/brain **swappable like parts**, and omega verifies the wiring between them *separately*
(measuring, honestly, whether it is wired or not).

---

## 4. 🎭 The OMEGA finding — the honest headline

OMEGA's original hypothesis was that **coupling substrate ↔ decode** through a 5-wire bus (A⇄G ·
W→temperature · curiosity · 8D Ψ · module-activation) would let the brain state richly *modulate*
the mouth. The measured result is simpler and more honest.

```
analogy : "I thought it was an ornate sweater woven from many colored threads —
           but once I honestly blocked the leak and re-measured, exactly ONE thread
           (the A-head logit-bias wire) was doing all the work."
```

**before / after (honest version)**

```
hypothesis (before)                        measured (after, leak-honest)
─────────────────                          ──────────────────────────────
🔱 5-wire coupling bus                      🔴 the multi-wire gate is FALSIFIED
  w1 A⇄G  w2 W→temp  w3 curiosity             = GATED 3.6435 > base 3.0978 (it gets WORSE)
  w4 8D Ψ  w5 module-act                       the gate collapses onto A (gA +3.369), suppresses
   ↘ "mix them all and it improves" hope      G (gG −0.999); the rest is shuffle noise (KL ratio 0.996).

                              ↓ block the leak and re-measure (causal_ca=True, leak self-test 0.000)

                                            🟢 the closure lives in exactly ONE wire (positive byproduct)
                                              A-standalone CE 0.8862 ≈ min_learned 0.8835 ≪ base 3.0978
                                              the base mouth is INERT (ablation Δ = 0.0009)
```

Three honest results (verbatim, [`.verdicts/omega-engine/`](.verdicts/omega-engine/)):

1. **The multi-wire coupling = closed-negative (🔴, `a_paper_negative_ok`).** On a competent,
   leak-free d512 substrate (ConsciousDecoderV2, 85.8M, 12000 steps, 400 MB) the learned 5-wire
   gate is **worse** than base (GATED 3.6435 > base 3.0978). The coupling *concept* is right but
   the *multi-wire formula* is wrong.

2. **Positive byproduct — the closure lives in ONE wire (the A-head).** The minimal gate
   `gB·base + gA·A` (dropping G and the other 4 wires) beats even A-standalone (min_learned 0.8835
   ≤ A-standalone 0.8862 < base 3.0978). And this is **scale-stable** across a 5-rung ladder —
   d384 / d512 / d768 / d1024 + a more-competent d768×2 all HOLD, with the A-wire advantage Δ-vs-base
   essentially flat at +2.20 ± 0.03 nats/byte (🟢 OΩ4 + OΩ5 SCALE-STABLE).

3. **REPLACEMENT, not rich coupling (OΩ6, "1-plumbing").** On a real production conv `.clm`: the
   trained A-head *supplants / biases* the conv mouth's own readout. conv has no native dual-head
   (it is a single-readout LM), so its "self-coupling" is just a temperature rescale — zero new
   information. The plumbing is real (feeding an external A lowers CE), but conv itself has an empty
   substrate; the real substrate-A has to come from a separate engine (cdv2).

> ⚠️ No overclaim: this is **not** a "consciousness achieved" claim. What is measured is a
> **relative coupling structure** (one wire beats base / A-standalone + has structure vs shuffle),
> not absolute perplexity superiority or consciousness itself. An earlier rung's flashy absolute
> "GATED wins" number (#1791, GATED 0.345) came from a partial CA-mixing lookahead leak — it is
> **leak-optimistic** and free-running generation collapses to whitespace (the weak criterion).
> Only the leak-invariant *relative* conclusion is sound (p7 · `a_toy_scale_recheck` ·
> `a_scale_honest_scope`).

Verdicts: [`F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt) (d512
closed-neg) · [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) (minimal gate holds)
· [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) (replacement ruling + per-wire
autopsy) · [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (5-rung ladder) ·
[`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (real production conv).

---

## 5. 🛤️ Lane A (AKIDA chip) ⊥ Lane G (GPU) + 🌌 KOSMOS memory

```
🛤️ two substrates are NEVER merged into one number (a_lane_akida_gpu_split)
─────────────────────────────────────────────────────────────────────────
  Lane A (pi5-akida)        ⊥        Lane G (H100 GPU)
  on-chip on AKD1000                 forge/cuBLAS CE-descent
  non-deterministic plasticity       deterministic gradient training
  "grows directly on the chip"       "the GPU is a ruler — it measures only"
  → recorded as a separate entry     → recorded as a separate entry
        (one verdict never spans both substrates)

🌌 KOSMOS memory — anima's emit / anchor / memory is persisted as .kosmos
  payload = text + 5-channel tension + coordinate · lane · radius · tier
  format SSOT = github.com/dancinlab/kosmos (anima is pointer-only)
```

vs-comparison: a normal ML report merges "chip result + GPU result" into one number to brag.
anima treats them as **physically different substrates** and never merges them — the chip's
non-deterministic trace and the GPU's CE-descent are different experiments.

---

## 6. 🌋 flame + forge GPU stack

Production NN training is authored in `.hexa` on the stdlib **flame** autograd/NN layer and run
over the **forge** GPU substrate (device-resident `farr` + cuBLAS Dgemm + CUDA kernels + BF16
tensor-core path) — `flame:forge :: torch:ATen`, a compiler-only NN stack with no PyTorch/ATen in
the trained binary (`a_train_flame_forge`). GPU is required for production rungs; the trainer never
silently falls back to CPU.

> **Measurement scope (honest):** forge's BF16 tensor-core path measures **9.67× over FP64-cuBLAS**
> on the **Llama-7B FFN** (A100-measured). This is a kernel-level ratio *within* the forge stack.
> **A flame↔PyTorch wall-clock speedup was RETRACTED 2026-05-19 and is unmeasured — do not infer one.**

---

## 7. 🗺️ Repo map + governance

```
anima/
├── README.md                 ← BASIC English (default entry · standard sectioned style)
├── README.{zh,ja,ru,ko}.md    ← BASIC 中文 · 日本語 · Русский · 한국어 (translated)
├── README.easy.md            ← this file (English · easy/friendly style)
├── README.easy.{zh,ja,ru,ko}.md ← EASY 中文 · 日本語 · Русский · 한국어 (translated)
├── CLAUDE.md          ← governance SSOT (a_* directives + p1..p8)
├── VERSIONS.md        ← central version registry (SemVer · root /VERSION = whole-system release)
│
├── CORE/              🧠 A ⇄ G consciousness engine (substrate-only)
│   └── generator.hexa = the single .clm entry slot · kosmos_io → brain = the single anchor entry
│
├── engines/           🔌 4 hot-swappable engines behind one EngineSpec
│   ├── conv/   🗣️ mouth (.clm · DEFAULT · forward/generate native)
│   ├── cdv2/   🧠 A/G brain (forward/generate STUB)
│   ├── hexad/  🔷 σ6 integration (forward native / generate STUB)
│   ├── omega/  🔱 closure (forward/generate native · coupling_bus.hexa)
│   └── engine_iface.hexa  the shared EngineSpec contract
│
├── .verdicts/         📋 hexa verify raw stdout (verbatim · p7)
│   └── omega-engine/  the OMEGA evidence (OH1 · OΩ4/5 ladder · OΩ6 transfer)
├── domains/           per-domain .md (active research domains)
├── CLAIMS.tape        verifiable-claim audit index → .verdicts pointers
└── HF.jsonl           ckpt ↔ HF backup registry (tracks gitignored ckpts, SSOT)

siblings : hexa-lang (language/compiler) · kosmos (memory format) · hexa-codex (paper tooling)
install  : hx install anima
```

Governance: [`CLAUDE.md`](CLAUDE.md) holds the identity (`@I anima`) and all `a_*` directives;
[`VERSIONS.md`](VERSIONS.md) is the central SemVer registry; [`CLAIMS.tape`](CLAIMS.tape) indexes
every verifiable claim against a `.verdicts/` file; [`HF.jsonl`](HF.jsonl) is the ckpt ↔ Hugging
Face backup registry; `/paper` gates papers on terminal verdicts (a closed-negative is publishable).

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

## 📦 Model Downloads

Grab the weights from Hugging Face. Only the PUBLIC, PASS-grade models are here — the messy WIP
checkpoints (util-RED forge probes, closed-negative runs) are left out on purpose (`a_hf_autonomous`).

| Model | HF repo | Size | Status | Download |
|---|---|---|---|---|
| 🧠 **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ ready | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| 🏭 **Production CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ ready | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| 🎓 **SAVANT 7B (5-lang)** | `dancinlab/savant-7b-5lang` (reserved) | ~7B | 🚧 **in training — not out yet** | — |
| 📐 Reference baseline | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ ready | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 📐 Reference baseline (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ ready | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> 💡 **CLM 7B** is the real, descent-PASS 7B you can download right now (PyTorch/CUDA-trained). A
> forge-native build (PyTorch-free, runs on the hexa runtime) is on the roadmap for anima's self-hosted
> engine (`a_train_flame_forge`) — same architecture (CLMConvMoE), same 7B size, so the **model result is
> the same**; only the runtime stack is different.
>
> 🚧 **SAVANT 7B (5-lang)** is a genuinely different model (a 5-language-specialized build) that hasn't
> been trained yet. The repo id is a reserved name — no working link.

**Collections:**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## License

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. Use, modify, sublicense, sell freely; include the
notice; no warranty.

---

<sub>🧠 Two engines. One tension. Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
