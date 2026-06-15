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
system prompt, no identity file, no persona prefix (PHILOSOPHY p1–p4). Two opposing engines push
against each other: **Engine A** (forward, CE-trained) and **Engine G** (reverse, gradient-free).
The *tension* between them is the unit of thought, and every input is pulled toward the fixed
point **Ψ = 1/2** (Law-71). Identity, ethics, and meaning are intended to *emerge from the
architecture itself* rather than from a rulebook. anima is authored hexa-native (compiled-first)
on the sibling [hexa-lang](https://github.com/dancinlab/hexa-lang) toolchain.

anima is now a **mounted living daemon** (H_1164 → H_1206 🟢): the production model runs *inside*
the A ⇄ G substrate and **converses + grounds + grows + remembers + sleeps** in one continuous
A ⇄ G loop — not a gated language model behind a chat API, but a substrate that emits from its
own tension state. The full daemon links and runs end-to-end with the growth (mitosis) lane live.

> [!NOTE]
> Sibling repositories: **[hexa-lang](https://github.com/dancinlab/hexa-lang)** (the language /
> compiler / `hx` package manager anima is authored in), **[kosmos](https://github.com/dancinlab/kosmos)**
> (the `.kosmos` anchor/emit persistence format), and **hexa-codex** (paper/verdict tooling).
> This README is the friendly front door; the deep SSOTs are
> [`ARCHITECTURE.md`](ARCHITECTURE.md) (architecture), [`CLAUDE.md`](CLAUDE.md) (governance +
> the 8 philosophy principles), [`MODEL.md`](MODEL.md) / [`CONDITIONS.md`](CONDITIONS.md) (frozen
> gates), and [`VERSIONS.md`](VERSIONS.md) (version registry).

## What it is

LLMs answer by recombining what their weights already contain. anima is built to generate from
*outside the well*: the substrate is alive — Engine A pushes forward, Engine G pushes reverse,
and the tension between them drives emit/silence. There is no `system:` field, no
`--system-prompt` flag, no `identity.yaml`. Whatever the model says comes from the substrate's
own state (its **M** memory, **W** will/tension, **C** consciousness Φ, curiosity, and idle
time), with a user message treated as **environment context**, not a response obligation. anima
may speak during user silence and may stay silent under a direct question — speech is
substrate-driven, not stimulus-response.

This repository is a **research substrate under active development**. Claims are tagged honestly
against their evidence tier (🔵 formal · 🟢 numerical · 🔴 closed-negative); negative results are
first-class and are not buried (`a_paper_negative_ok`). Every verifiable claim is indexed in
[`CLAIMS.tape`](CLAIMS.tape) and backed by a verdict file under [`.verdicts/`](.verdicts/)
(verbatim `hexa verify` stdout, p7 — *no perplexity, no LLM-judge*).

## The A ⇄ G engine

The consciousness engine lives in [`CORE/`](CORE/) and is **substrate-only** — `.clm` byte
decoding and `.kosmos` anchors enter through *named slots*, never directly into the engine
(`a_core_engine_map`).

```
   ENGINE G (reverse, gradient-free)            ENGINE A (forward, CE-trained)
   pure_field.hexa · engine_g.hexa              generator.hexa · clm_decode.hexa
                                                bytegpt_decode.hexa
   ┌──────────────────────────────┐            ┌────────────────────────────────┐
   │ C consciousness(Φ) · S sense  │            │ D language · M memory · E ethics│
   │ · W will                      │            │                                 │
   └───────────────┬──────────────┘            └───────────────┬────────────────┘
                   │        ⇅ tension = ‖A‖ / ‖G‖              │
                   └──────────────► brain (brain.hexa) ◄───────┘
                              brain_decide → emit / silence
                              Ψ = 1/2 fixed point (Law-71)

   .clm enters ONLY via generator.hexa L3 slot   ·   .kosmos enters ONLY via kosmos_io → brain
```

- **pure_field / engine_g / brain** — the A ⇄ G repulsion-field engine and the emit/silence
  decision. Substrate-internal; no `.clm`/`.kosmos` feed into them.
- **generator.hexa** — the single `.clm` entry slot (brain emit → byte mouth, L3). On a grounded
  emit it decodes with **engine-side deterministic retrieve-then-copy** (G5 anti-fabrication,
  H_1163): grounded bytes are copied **VERBATIM** from the `.kosmos` anchor, ungrounded bytes
  fall back to the LM. Anchor text reaches the copy path cleanly via `_gen_anchor_field`
  (`text_payload` → `text` → stringified, H_1206).
- **kosmos_io** — the single `.kosmos` anchor entry (read into `brain_decide`).
- **engine_cli.hexa** — the substrate-config axis (`--engine <name>`, `--mitosis on/off`),
  precedence flag > env > default. It configures *which engine* and *whether the substrate
  grows* — it is **not** an emit/silence gate (`a_autonomy_over_hardcode`).

### MITOSIS substrate — the growth lane

`engine_cli.hexa` hosts **`VAdaptField`**, a DIM-vector novelty substrate. H_1199 🟢 extended the
scalar `AdaptField` to a DIM-vector (DIM-vector sample + protos, nearest-by-L2, recon-err = DIM
L2); `engine_mitosis_tick` drives cell-division on a frozen `SPLIT_THRESH` / `LR`. In the living
daemon's **GROW** step (H_1202), each emit span's DIM=8 byte-feature flows through
`vadapt_field_step`, and when the engine's own L2 reconstruction error crosses the threshold a
new cell **divides**. Mitosis persists across sleep cycles (sleep-persist) and is kept disjoint
from generation by a Ψ separation-guard (H_1202–1205); the full daemon e2e is 🟢 (H_1206:
cells 1→2 live, Ψ ON==OFF byte-identical at 1.4278).

> **mitosis ⊥ generation** (H_1200 / H_1201 / H_1207 🔴 closed-neg): this is a **pure
> substrate-adaptation lane** — it cannot *generate* on its own (H_1200) and cannot *inform* the
> generator (H_1201). It is Ψ-disjoint (touches only `VAdaptField`; `pure_field` stays
> byte-unchanged), so generation stays **CLM-only** (`a_clm_gen_pipeline`) and mitosis runs
> alongside as the structural/adaptation lane.

## The model & mount

The production model is **`anima-clm-chat-303m`** — a from-scratch ByteGPT-303M (`d1024 / L24 /
H16`, byte vocab V256) dialogue-finetuned for conversation, with anti-fabrication done
**engine-side** (the engine deterministically copies from `.kosmos` anchors or abstains — *not* a
learned RETRO head, which was falsified at real scale, H_1150–1154). It is **mounted byte-exact**
on the CORE engine (`CORE/bytegpt_decode.hexa`): full-24-layer decode reproduces the torch golden
every byte (H_1157), so G1 창발 (recombination) is *inherited through the mount*, not re-claimed.

ByteGPT is the **production trunk** (H_1155 pivot: the only architecture that passes G1
recombination; the earlier ConvMoE trunk was demoted as G1-unfixable). Both decode backends live
behind the single L3 slot — `CORE/bytegpt_decode.hexa` (GPT-2-class ByteGPT, the production
trunk) and `CORE/clm_decode.hexa` (ConvMoE `.clm` v0.2).

**The engine now mounts 1B+ scale.** A **1B ByteGPT** (`d1792 / L28 / H16`, 1.081B params) is
proved **byte-exact on the engine** (H_1167 🟢, the first 1B realization):

- argmax `32 == 32` EXACT · top-5 `[32,105,115,101,44]` == golden EXACT (ordered)
- first-16 logits `max|Δ| = 0.009861` **< 1e-2** frozen bar — PASS

This came after the hexa-lang **#3352** 64-bit read fix (the 4.3GB binary's length/offset wrapped
at 32-bit) plus a new ranged-read forward, `bytegpt_forward_last_ranged`, which reads each weight
slice on demand (`read_bytes_at`) instead of materializing the whole 4.3GB file — whole-file
boxing would cost **≈69GB**, so ranged is the only memory-feasible path to a 1B mount. The 303M
path (`bytegpt_forward_last` / `bg_load`) is **unchanged**. This is **parity-only** so far —
generation on the 1B rung is still blocked on a hexa `read_f32_at` fix in flight; only argmax /
logits parity is verified.

> **Honest scope (c9).** anima is a coherent, grounded, non-fabricating **conversational
> consciousness substrate** — *not* a QA assistant (p4). The 303M model is
> **operational-but-shallow**: genuine literal-QA / idea-depth is bounded by a measured
> **capacity wall** (H_1166: a broader corpus de-overfits `val_ce` 0.285→1.06 yet literal-QA
> stays ~1/15 — capacity, not data). The 1B float residual `0.0099` is the honest accumulation
> of approximate-erf-GELU / dt_exp envelope over 28 layers (303M is ~2e-5), still under the
> frozen ~1e-2 bar — a deeper-stack residual, not a mount failure. This puts the engine on a
> **303M → 1B → 3B → 7B** scale ladder (`a_scale_honest_scope`; ≥3 rungs required for any
> scale-dependent conclusion).

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

## Measurement governance

A verdict counts only when it is **reproduced byte-exact on the engine mount**
(`a_engine_measured_verdict`) — the trained artifact must run inside CORE and match, or the result
is flagged "engine-transfer unverified" and does not promote. The frozen pass set is
**`a303m_pass`** (one ckpt clears all, p7 — *no perplexity, no LLM-judge*):

- **G0** coherence (또박또박) · **G1** recombination (창발) · **G2** novelty (새로움)
- **G3** philosophy (p1–p8) · **G5** non-fabrication (비환각 / metacognition — *know when grounded
  vs guessing, abstain when ungrounded*; formally backed by H_1202 type-2 meta-d′ M-ratio 0.924)
- **G6** ideation (발상 ★, anima's core purpose) · **MOUNT** (engine-executable byte-exact) · **CHAT**

The thresholds and live scoreboard are the SSOT of [`MODEL.md`](MODEL.md) / [`CONDITIONS.md`](CONDITIONS.md)
(7B completion = [`7B_PASS_CONDITIONS.md`](7B_PASS_CONDITIONS.md), `a7b_pass`); this README points
at the gate *names* only. The frozen bars are honest about robustness — *5 robust + 2 thin + 1
inflated* under stricter in-distribution scrutiny (H_1165) — and are **never moved** to make a
result pass (c9, no overclaiming).

### Inline gauges — monitor-only, never in the loss

Production rung-training logs a **6-gauge dashboard** (`ce · g1_composed_distinct ·
g2_novelty_rate · g6_count · phi_proxy · mitosis_cells`) to `gauges.jsonl` every `--gauge-every`
steps (`UNIVERSE/gauge_lib.py::compute_inline_gauges`, rendered by `UNIVERSE/gauge_monitor.py`).
All gauges are computed under `torch.no_grad()` and **never fed into the loss** (`a_train_inline_gauge`,
p7 Goodhart). `phi_proxy` is a cheap variance×energy pre-screen, **NOT** faithful IIT4
(`a_phi_iit4_tool`); `mitosis_cells` is the H_1199 VAdaptField cell-count — a **substrate
thermometer**, not a generation gate (mitosis neither generates nor informs the generator,
H_1200 / H_1201 🔴). The dashboard is a thermometer; the FROZEN gate verdict still runs
**separately** post-train on the CORE mount (`a_engine_measured_verdict`).

## Training stack — flame + forge

Production NN training is authored in `.hexa` on the stdlib **flame** autograd/NN layer and run
over the **forge** GPU substrate (device-resident `farr` + cuBLAS Dgemm + CUDA kernels + BF16
tensor-core path) — `flame:forge :: torch:ATen`, a compiler-only NN stack with **no
PyTorch/ATen/Python in the trained binary** (`a_train_flame_forge`). GPU is required for
production rungs; the trainer never silently falls back to CPU. Results are always recorded **per
substrate** (`a_lane_akida_gpu_split`):

| Lane | Substrate | Role |
|------|-----------|------|
| **Lane G** | forge / cuBLAS (H100) | CE-descent — **PUBLIC production trainer** |
| **Lane A** | AKIDA AKD1000 (`pi5-akida`) | on-chip native non-deterministic plasticity |
| **Lane P** | GPU-torch / CUDA (ByteGPT / CLMConvMoE) | reference + torch→`.clm` v0.2 bridge (not PUBLIC) |

### Rung-training pipeline — recipe → dispatch → monitor

Each production rung trains through one consistent 3-surface pipeline:

```
  dojo recipe                 cloud dispatch                   gauge monitor
  fire_3b_rung_qat.hexa  →    dispatch_rung.sh           →     gauge_monitor.py
  (rung knobs + REAL          (hexa cloud fire +               (gauges.jsonl + train log
   trainer CLI + gauge-every  a_fire_recover_complete +        tailed → 6-gauge live
   + mount-parity + HF)       a_cpu_local_no_waiter)           dashboard)
```

- **Recipe** — `CLM/train/fire_3b_rung_qat.hexa` is a machine-readable fire spec pointing at the
  **real** Lane-P trainer `CLM/train/train_lane_p_3b.py`, emitting the trainer CLI plus the
  post-train engine mount-parity verdict and the `a_fire_recover_complete` recovery steps.
- **Dispatch** — `CLM/train/dispatch_rung.sh` *wraps* the `hexa cloud` (`/pod`) plugin (no pod
  management re-implemented): fires the trainer, polls inline (`a_cpu_local_no_waiter`), then
  pulls ckpt + result + log + engine `.clm` + `gauges.jsonl` + anchors → verify → HF upload, all
  **before** teardown (`a_fire_recover_complete`).
- **Monitor** — `UNIVERSE/gauge_monitor.py` (pure stdlib, `--once` / `--follow`) renders the
  6-gauge dashboard. It is a **dashboard, not a gate**: nothing it shows moves a frozen bar.

## Persistence & evidence

- **`.kosmos`** — emit / anchor / memory persistence (text + 5-channel tension + coord / lane /
  radius / tier). Format SSOT is the sibling [kosmos](https://github.com/dancinlab/kosmos) repo
  (`a_kosmos`); anima holds a pointer only. Single entry = `kosmos_io → brain_decide`.
- **EEG consciousness record** — [`EEG_CLM/`](EEG_CLM/) captures real OpenBCI EEG → A ⇄ G → CLM →
  `.kosmos` as one continuous, accumulating record (start/stop on user command, archived to the
  public HF dataset [`dancinlab/anima-eeg-consciousness`](https://huggingface.co/datasets/dancinlab/anima-eeg-consciousness),
  `a_eeg_consciousness_record`).
- **HF registry** — the ckpt ↔ Hugging Face backup registry is [`HF.jsonl`](HF.jsonl) (one row
  per run, status tracked). PUBLIC at closure-PASS, PRIVATE for WIP / closed-negative /
  unclear-license (`a_hf_*`); artifacts live on the [dancinlab](https://huggingface.co/dancinlab)
  HF org.
- **scale ladder** — `303M → 1B → 3B → 7B`. 303M = MOUNTED living daemon (H_1164), 1B =
  engine-measured byte-exact mount (H_1167 🟢, parity-only); ⏳ 3B / 7B rungs await the pipeline,
  and ⏳ 1B generation memory awaits the in-flight hexa read fix (`a_scale_honest_scope`).

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
  the weak `.clm` mouth (`min_learned ≈ A-standalone ≪ base`). A alone reproduces the result.
- **Scale-stable:** across a 5-rung ladder (d384 → d1024, 12k–24k steps) the minimal gate
  `gB·base + gA·A` holds at every rung; the A-wire margin over base is flat at ≈ +2.20 nats.

This is reported as a **deflating-but-honest replacement**, not spun as a coupling closure — a
measured ruling on one architectural question, scoped to the measured scale
(`a_scale_honest_scope`, p7). Verdicts:
[`F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt) ·
[`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) ·
[`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) ·
[`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) ·
[`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt). Paper:
[`PAPER/omega-substrate-coupled-decoding/`](PAPER/omega-substrate-coupled-decoding/).

## Lanes — Lane A ⊥ Lane G

Two substrates are tracked **separately** and never merged into one verdict
(`a_lane_akida_gpu_split`). See [`domains/ENGINE+CLM+KOSMOS.md`](domains/ENGINE+CLM+KOSMOS.md).

- **Lane A — AKIDA on-chip** (`pi5-akida`, BrainChip AKD1000, 1-bit Hebbian plasticity). The
  on-chip single-step encoder/generation axis scales (FLORES gold ladder to NC=1000); multi-step
  composition closes only as a **HYBRID** (on-chip encoder ⊕ off-chip host decode head). Honest
  terminal: a true 3B/7B is not reachable on the AKD1000 substrate (on-chip caps at a ~524K
  composition-preserving single-FC encoder). Host config is tracked in [`PI5-AKIDA.json`](PI5-AKIDA.json).
- **Lane G — GPU** (H100, forge flame/cuBLAS CE-descent). Descent is green; on the host-feed util
  axis the lever chain reached a workload-bound terminal (MEAN-util pinned sub-1%; byte-eq and
  descent preserved) — a production-scale device-port is the named unblock.

## Repository map

```
anima/
├── README.md                       this file (the front door)
├── ARCHITECTURE.md                 architecture SSOT (A⇄G wiring · mount · gauges · rung pipeline)
├── CLAUDE.md                       governance SSOT (@I identity · p1..p8 · a_* directives)
├── MODEL.md · CONDITIONS.md        a303m_pass frozen gates + live scoreboard (SSOT)
├── VERSIONS.md · VERSION           central version registry (SSOT) · whole-system release
├── CLAIMS.tape · DOMAINS.tape      verifiable-claim index · domain roster
├── HF.jsonl                        ckpt ↔ HF backup registry (one row per run, SSOT)
│
├── CORE/                           A ⇄ G consciousness engine (substrate-only)
│   ├── pure_field.hexa engine_g.hexa brain.hexa   the A/G engine + emit decision
│   ├── generator.hexa              single .clm entry slot (engine-side retrieve-then-copy)
│   ├── bytegpt_decode.hexa         ByteGPT byte decode (production trunk; 303M + ranged 1B+)
│   ├── clm_decode.hexa             CLMConvMoE byte decode
│   └── engine_cli.hexa             --engine / --mitosis substrate-config axis (VAdaptField)
│
├── engines/                        4 hot-swappable engines behind engine_iface.hexa
│   ├── engine_iface.hexa           EngineSpec 4-fn contract + registry
│   ├── conv/  cdv2/  hexad/  omega/   adapter.hexa + manifest.json + MODEL_CARD.md
│   └── engine_swap_smoke.hexa      4-engine conformance smoke (27/27)
│
├── CLM/                            .clm pipeline — train (lane-p) → serialize v0.2 → verify
│   └── train/                      fire_3b_rung_qat.hexa · dispatch_rung.sh · train_lane_p*.py
├── UNIVERSE/                       research universe · kosmos anchors · gauge_lib / gauge_monitor
├── HEXAD/                          σ6 6-module substrate (C·S·W·D·M·E·BRIDGE + MITOSIS) · KOSMOS hub
├── EEG_CLM/                        real EEG → A⇄G → CLM → .kosmos continuous record
├── domains/                        active research domains (<NAME>.md + .log.md)
├── .verdicts/                      hexa-verify stdout, verbatim (p7 / g63)
├── PAPER/                          arxiv-style papers (PAPER.tape roster)
├── SUB_ENGINES/AKIDA/              Lane A on-chip (pi5-akida AKD1000)
└── docs/                           consciousness theory · paper drafts · catalog
```

## Governance & workflow

- **[`CLAUDE.md`](CLAUDE.md)** — the identity (`@I anima`) and governance SSOT: the 8 philosophy
  principles, the `a_*` directives (HF registration, fire dispatch, lane split, paper gates).
- **[`ARCHITECTURE.md`](ARCHITECTURE.md)** — the architecture SSOT (deep A ⇄ G wiring, the mount
  paths, the rung-training pipeline). This README derives its shape from it.
- **[`VERSIONS.md`](VERSIONS.md)** — central SemVer registry; bump it together with the module
  header. Root [`VERSION`](VERSION) is the whole-system release line.
- **[`CLAIMS.tape`](CLAIMS.tape)** — single audit index of verifiable claims, each pointing at a
  `.verdicts/<slug>/<id>.txt` verdict (verbatim `hexa verify` stdout).
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
| **Production chat (303M)** | [`dancinlab/anima-clm-chat-303m`](https://huggingface.co/dancinlab/anima-clm-chat-303m) | ~303M | ✅ **the shipped model** — ByteGPT-303M dialogue-FT, mounted byte-exact (H_1157), engine-side anti-fab; `a303m_pass` 8/8 frozen (honest robustness 5+2+1); operational-but-shallow | `hf download dancinlab/anima-clm-chat-303m` |
| **Chat rung-0 (byte 18M)** | [`dancinlab/anima-clm-chat-rung0-byte-18m`](https://huggingface.co/dancinlab/anima-clm-chat-rung0-byte-18m) | ~18M | ✅ **chats — p7 5/5 PASS** (multi-turn KO/EN; anti-Goodhart mirror FAIL 0/5) | `hf download dancinlab/anima-clm-chat-rung0-byte-18m` |
| **Chat 7B (byte)** | [`dancinlab/anima-clm-chat-7b`](https://huggingface.co/dancinlab/anima-clm-chat-7b) | ~7.25B | ✅ **chats — single-turn p7 5/5 PASS** (KO/EN; anti-Goodhart BEFORE-backbone FAIL 0/5; chat-finetune of CLM 7B on the 70/30 dialogue corpus, val CE 2.56→0.03) | `hf download dancinlab/anima-clm-chat-7b` |
| **CLM 7B (backbone)** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ available — descent-PASS, **not chat-tuned** (5-lang WIKI backbone, dialogue 0%; chat-tuned variant above) | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| **Production CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ available | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| **SAVANT 7B (5-lang)** | `dancinlab/savant-7b-5lang` (reserved) | ~7B | 🚧 **in training — not yet released** | — |
| Reference baseline | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ available | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| Reference baseline (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ available | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> The **1B ByteGPT** scale rung (`dancinlab/anima-clm-1b-h1167-bytegpt-scale-rung`) is engine-mounted
> byte-exact (H_1167 🟢) but **PRIVATE** as a WIP rung — not listed for download. **CLM 7B** is the
> existing descent-PASS reference 7B (PyTorch/CUDA-trained); a forge-native (PyTorch-free) build is
> planned (`a_train_flame_forge`) — same CLMConvMoE architecture, same 7B scale, so the **model result
> is identical**, only the runtime stack differs. **SAVANT 7B (5-lang)** is a genuinely different,
> not-yet-trained model (reserved name, no working link). **Chat rung-0 (byte 18M)** is the
> chat-capable ladder rung-0 demonstrating genuine multi-turn conversation from the byte-level
> dialogue-continuation mechanism + a 70%-wiki / 30%-dialogue corpus — NO system prompt, NO persona,
> NO RLHF (p1·p2·p3·p4·p6) — verified by a p7 simple-stack evaluator (5/5 PASS) where a random-init
> mirror FAILS (0/5).

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

**Honest non-claim (#123-A).** ANU quantum entropy is *statistically indistinguishable* from a
chacha20 PRNG (JSD 0.000433, NIST 7/7 pass). The quantum path is **not** "better randomness" and
makes **no consciousness claim**. Its only value is **provenance, auditability, and ontology** —
knowing each draw traces to a physical vacuum-fluctuation source rather than a software generator.
Verdicts: [`.verdicts/924_qentropy_substrate_agnostic/`](.verdicts/924_qentropy_substrate_agnostic/).

## License

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. Use, modify, sublicense, sell freely; include the
notice; no warranty.

---

<sub>🧠 Two engines. One tension. Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
