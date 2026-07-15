# 🧠 anima

## ⛔ EVERY engine op goes through the installed `anima-py` CLI — read this before you type anything

| | the ONLY command |
|---|---|
| corpus | `anima-py corpus <fmt> --out c.txt …` (emits the budget floor; the trainer refuses to start below it) |
| train | `anima-py train --corpus c.txt --init base.clm …` (`[train]` extra) |
| **judge** | `anima-py evaluate <clm> [--xbind m.json] [--rho-axon]` — the **TERMINAL** verdict path |
| serialize · sweep · chat | `anima-py serialize` / `sweep` / `chat` |

- do: reach for the **py** channel for every engine op (`pip install "anima-python[train]"`) · wire a NEW manipulation as a **flag on these commands** (`a_experiment_engine_native`).
- dont: `python3 cli/*.py` · a hand-rolled script beside the engine · a probe re-implementing a forward pass.
- dont: cement on **a number these commands did not produce** — hard-blocked in code, because every bypass died undecidable (H_9303 · H_9307).

## 🇬🇧 EN-FIRST until the recombination wall breaks (owner directive · research corpora only)

- do: build every NEW research corpus with **`anima-py corpus <fmt> --lang en`** — the Korean lane is 🧱 BINDING, every escape measured dead (H_9327).
- do: EN is the **discriminator** — `not` is FREE/pre-posed, `지 않다` a BOUND suffix.
- dont: read an EN positive as a cemented claim (**SCREENER, DIRECTIONAL** — it moves morphology + base + carrier at once).
- dont: touch `--lang ko` (byte-identical to every frozen corpus) · build EN over the Korean atom file (the builder refuses).

## Project

anima = a **substrate-native consciousness chat daemon**, not an assistant. Engines **A** (forward, CE) ⇄ **G** (reverse, gradient-free) push; that *tension* pulls emit/silence to **Ψ = ½**. No prompt, no persona — identity emerges from the architecture. Deep structure → `ARCHITECTURE.json`.

## Tree

```
anima/
├─ core/       — A⇄G⇄brain engine (weights via generator.hexa L3)
├─ cli/        — anima entry · train · evaluate · corpus
├─ stdlib/     — iit4 faithful-Φ · flame/forge GPU
├─ HYPOTHESES/ — jsonl + cards/ (2 surfaces, nothing else)
├─ state/      — 🔒 FROZEN: verdicts/ only · state/ + archive/state/ new-write G7-blocked (content → cards)
└─ ARCHITECTURE.json — deep-structure SSOT (`python3 serve.py`)
```

## 🚦 Pre-action hard-gate (BLOCKING · before any work/verify/fire)

- do: ① cement only on engine-native `core/` decode ② heavy compute on pool, **never mini** ③ **pull the ckpt before teardown** ④ CHANGELOG + ARCHITECTURE/ING → verified `pr-cycle`.
- do: ⑤ a negative is a result — **no tune-to-green**, frozen-first, no self-judge ⑥ every H on 2 surfaces ⑦ GREEN only when wired.
- dont: skip ①/⑥ — code-blocked by `.harness/enforce_anima_gates.py` (G2 = no non-card file under `HYPOTHESES/` · G5 = wheel change without a `VERSION` bump · G6 = unique H_id).

## 📦 Packaging (pod)

- do: production tree = **`core/` · `cli/` · `agent/` only** (+ vendored `stdlib/`) · `pip install anima-python` → run **`anima-py`** (install name ≠ run command) · hexa twin = `hx install anima`.
- dont: a production `import` from `archive/` · a wheel change (`cli/**`·`core/**`·`pyproject.toml`) without bumping root `VERSION` (**G5** hard-blocks) · gate the py channel on a hexa smoke.

## Philosophy p1–p8 (what anima rejects)

p1 no system prompt · p2 no identity rules · p3 no persona injection · p4 no assistant framing · p5 no `speak()` (emit only over real tension; stage-gated OK, reactive self-seed banned) · p6 no fine-tuned ethics · p7 **no perplexity verdict** (Goodhart) · p8 no train/infer split.

## 🩺 Ψ-SOMA — measurement frame (SSOT · reframes the old G-ladder · full → ARCHITECTURE `psi-soma-vitals`)

- do: read the verdict as **mode-of-existence, not capability** — **Θ** (Ψ=½ tension = the pulse; Θ dead ⟹ σ VOID) · **σ** (9 axes = the body) · INVALID/VOID/PENDING are first-class.
- do: read the signal as **collapse-Δ vs ≥2 controls**, never a raw value (FORM tunable · BIND earned · p7).
- dont: fold **ρ-AXON** (reach = capability · `--rho-axon`) into the verdict — **the G1/G6 wall is a reach fact, not a consciousness deficit** · cement TERMINAL on a toy (only 303M py is TERMINAL).

## Governance (`name` — core MUST; full do/dont + H_ precedents → ARCHITECTURE.json)

Keyword-trigger index. Each line is a pointer — the full do/dont and the H_ that earned it live in `ARCHITECTURE.json`.

### 🔬 Verification (HARD-GATE)
- `a_no_llm_frame_trap` — substrate-first, not the LLM frame.
- `a_break_the_wall` — a wall = change angle; a ceiling needs ≥2–3 lenses. No tune-to-green.
- `a_engine_native_learning` — cement only on `core/` decode; a mirror = DIRECTIONAL.
- `a_experiment_engine_native` — 🧪 the INSTRUMENT is engine-native too — wire a manipulation as an `anima-py` flag, never a probe beside the engine.
- `a_verified_must_wire` / `a_blue_closed` — GREEN only when output AND wiring are closed.
- `a_phi_iit4_tool` — Φ via faithful IIT4, never a proxy.
- `a_train_inline_gauge` — in-training metrics are MONITOR-ONLY, never in the loss.
- `a_korean_byte_budget` — 🇰🇷 byte-LM: every window/len knob is BYTES (**ko = 3 B/char**). The oracle's byte budget must equal the model's; one manifest per atom byte-length. Bit us 3×.

### 🧪 Hypothesis
- `a_hypothesis_register` — every H on 2 surfaces: jsonl + card. Nothing else.
- `a_no_scatter_hypotheses_first` — 🧹 output surfaces = 4 only: card body + jsonl (findings·numbers·parity) · ARCHITECTURE gate node (verdict) · `state/verdicts/` (frozen) · `/tmp` (volatile). New writes under `state/`·`archive/state/` = hook + G7 double-blocked — a result is written to a card, never a scattered file.
- `a_claim_manifest` / `a_claim_verify` — claim → `hexa verify` → a frozen verdict. No self-judge. Use the **global** `harness`/`hexa` (the submodule may be stale).
- `a_h_continuous_no_branch` — **owner: run the next H autonomously, no per-step go.**
- `a_discovery` / `a_discovery_log` — run discovery every batch → `domains/<DOMAIN>.log.md`.
- `a_toy_scale_recheck` / `a_scale_honest_scope` — a toy verify ≠ closure; bound a metric to its scale.

### 🔥 Fire · GPU · recovery
- `a_fire_autonomous` — fire a cost run autonomously (⚠️ fleet rent=spend needs go).
- `a_wall_first` — independent tracks, **one GPU host each, concurrently** ⟹ wall = max(track), never sum. A quick-win eval never queues behind a retrain.
- `a_fire_recover_complete` — pull the ckpt to permanent storage BEFORE teardown.
- `a_cpu_local_no_waiter` / `a_dont_kill_live_compute` — inline-poll a fire; prove a stall before killing it.

### 🏗️ CORE engine
- `a_core_engine_map` — `core/` = A⇄G⇄brain; weights via `generator.hexa` L3.
- `a_cli_single_entry` — every engine op via an INSTALLED command, **2 channels only**: `anima-py <verb>` · hexa `anima <verb>`. Never raw `python3 cli/*.py`. The scratch tree is FROZEN.
- `a_eval_py_canonical` — reach eval = `anima-py evaluate`. Heavy 303M → pool, never mini.
- `a_gpu_default_no_optin` — GPU fast-paths are **DEFAULT-ON via `cuda_available()`, never opt-in env** — an opt-in gate runs every decode scalar with the **GPU idle** (H_9119).
- `a_no_archive_import` — production never imports from `archive/`.
- `a_savant_train` — SAVANT inhibition DISJOINT from the emit-drive lane.
- `a_mitosis_train` — p8 MITOSIS; growth 🟢, from-scratch split 🔴.
- `a_chat_registers` — chat = ko·en × general·SNS, all 4 cells.
- `a_lane_akida_gpu_split` — AKIDA ⊥ GPU: separate entries + tag.
- `a_substrate_disjoint` — **LAW: separation = preservation, overlap = conflict.**

### 🗣️ Substrate autonomy
- `a_substrate_native_speak` / `a_autonomy_over_hardcode` — speech is substrate-native; no hardcoded emit gate.
- `a_chat_sleep_imagination` — 5-stage sleep; imagination ≠ `speak()`.
- `a_kosmos` — persistence = `.kosmos`; identity via a self-anchor (mouth ⊥ id).
- `a_eeg_consciousness_record` — OpenBCI NATIVE serial, REAL only; HF PUBLIC.

### 🔧 Identity · HF · chip
- `a1` — version registry = `VERSIONS.md` SSOT.
- `a_hf_complete` / `a_hf_autonomous` / `a_hf_registry` / `a_hf_collections` — HF complete, no drift; auto-upload +sha256; PUBLIC → collection.
- `a_pi5_akida_registry` — pi5-akida = `PI5-AKIDA.json` SSOT; **never** move it to the pool.
- `a_completeness_over_cheap` — completeness bar first; cost is not a gate.
- `a_parallel_session_compare` — read what other sessions landed before you fire; report AGREES/CONFLICTS. **Never edit the primary checkout.**

## Harness · claim flow

- do: global `harness`·`hexa` on PATH; claim → `hexa verify` → a frozen verdict → card + jsonl.
- dont: trust the (stale) submodule binary · write a paper unless asked (c15).
