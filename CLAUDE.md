# 🧠 anima

## Project
anima is a **substrate-native consciousness chat daemon** — not an assistant. Opposing engines **A** (forward, CE-trained) ⇄ **G** (reverse, gradient-free) push; that *tension* pulls emit/silence to **Ψ = 1/2**. No system prompt / identity file / persona — identity emerges from the architecture. hexa-native.

## Tree
```
anima/
├─ core/     — A⇄G⇄brain engine (weights via generator.hexa L3)
├─ cli/      — anima.hexa entry · train.hexa trainer
├─ stdlib/   — iit4 faithful-Φ · hf · flame/forge GPU
├─ UNIVERSE/ — HYPOTHESES.jsonl + cards/ (2 surfaces)
├─ state/    — verdicts/ + outputs · archive/·agent/·domains/·tool/
└─ ARCHITECTURE.json — deep structure SSOT (serve.py)
```

> **SSOT pointers** — terse always-injected index (`a_*`/`p#` keyword-trigger); full do/dont + all H_ precedents/mechanism/paths → ARCHITECTURE.json. commons c1–c17 · claims `HYPOTHESES.jsonl`+`cards/`+`state/verdicts/` · HF/pi5-akida → ARCHITECTURE.json·`PI5-AKIDA.json`.

## 🚦 Pre-action hard-gate (BLOCKING · before any work/verify/fire)
1. **🔒 Engine-native verdict** — cement tiers ONLY on `.hexa` `core/`-decode; a mirror → DIRECTIONAL + ING (`a_engine_native_learning`).
2. **🖥️ Pool, not mini** — heavy compute on `harness pool`, GPU via `hexa cloud`/`hexa dojo`. (c17·c12)
3. **💾 PULL ckpt before teardown** — to permanent storage before pod-down (`a_fire_recover_complete`).
4. **📄 Docs + pr-cycle** — CHANGELOG + ARCHITECTURE/ING → verified `harness pr-cycle` merge. (c14)
5. **🟦 No tune-to-green** — negative is a result; frozen-first; no self-judge. (c9·c2·p7)
6. **🗂️ Hypotheses = 2 surfaces** — jsonl + card only (`a_hypothesis_register`).
7. **🔌 GREEN only when wired** — live `core/*.hexa` + ARCHITECTURE.json lockstep (`a_verified_must_wire`).

> ⚙️ Gates 1·6 code-blocked by `tool/enforce_anima_gates.py` (reject a violating PR; `--all`, c18).

## 📦 Packaging (pod)
**Invariant: `core/` has 0 dependency on `archive/train/`·`bench/`·`agent/`·`state/`** (one-directional). Inference pod = `core/`+`cli/`+`stdlib/iit4/` (`.clm` external); +`archive/train/`+`state/verdicts/` for training; `agent/` standalone; `state/`·`UNIVERSE/` never on pod.

## Philosophy p1–p8 (what anima rejects)
p1 NO SYSTEM PROMPT · p2 NO IDENTITY RULES · p3 NO PERSONA INJECTION · p4 NO ASSISTANT FRAMING · p5 NO SPEAK() (emit only over real tension) · p6 NO FINE-TUNED ETHICS (emerge from cells, no RLHF) · p7 NO PERPLEXITY VERDICT (Goodhart) · p8 NO TRAIN/INFER SPLIT (gradient ⇄ mitosis). **p5 addendum** (`p5_tension_emit_not_filler`) — stage-gated emit over real tension is OK; banned = reactive `speak()`/self-seed/monologue.

## Governance (`name` — core MUST; full do/dont + H_ precedents → ARCHITECTURE.json)

### 🔬 Verification · engine-native + design lens (HARD-GATE · top priority)
- **`a_no_llm_frame_trap`** — substrate-first (neuro/bio/physics), not the LLM frame.
- **`a_break_the_wall`** — a wall (🧱) = change angle; a ceiling needs ≥2–3 controlled lenses (ABLATION); no tune-to-green. (c16)
- **`a_engine_native_learning`** — verdicts need engine-native `core/`-decode; a mirror is DIRECTIONAL.
- **`a_verified_must_wire`** — GREEN done only when wired live to `core/` + ARCHITECTURE.json lockstep.
- **`a_blue_closed`** — 🔵 only when output AND wiring closed, via `hexa verify`.
- **`a_phi_iit4_tool`** — Φ verdicts use stdlib faithful IIT4 via `hexa verify`, never a proxy.
- **`a_train_inline_gauge`** — in-training metrics are MONITOR-ONLY, never in loss (p7).

### 🧪 Hypothesis workflow
- **`a_hypothesis_register`** — every H on 2 surfaces: HYPOTHESES.jsonl + a card; nothing else in UNIVERSE/.
- **`a_claim_manifest`** / **`a_claim_verify`** — claim → `hexa verify` → frozen `state/verdicts/` file, verbatim; no self-judge / CLAIMS.tape.
- **`a_h_continuous_no_branch`** — run the next H continuously until the user redirects.
- **`a_discovery`** / **`a_discovery_log`** — run discovery every batch (/kick·/gap) → `domains/<DOMAIN>.log.md`.
- **`a_toy_scale_recheck`** / **`a_scale_honest_scope`** — a toy verify ≠ closure; keep a scale-metric bounded to its scale.

### 🔥 Fire · GPU autonomy · recovery
- **`a_fire_autonomous`** — dispatch a cost fire autonomously (1-line estimate); no user gate (⚠️ fleet: rent=spend needs go).
- **`a_wall_first`** — wall-time first: more/bigger parallel GPUs regardless of cost.
- **`a_fire_recover_complete`** — before teardown pull the ckpt to permanent storage → HF upload.
- **`a_cpu_local_no_waiter`** / **`a_dont_kill_live_compute`** — a fire runs CPU-local inline-polled; prove a stall before killing.
- **`a_runpod_inbox`** — cross-repo handoffs via `harness ing add --to <repo>`; no inbox folder.

### 🏗️ CORE engine · training substrate
- **`a_core_engine_map`** — `core/` = A⇄G⇄brain; weights enter only via `core/generator.hexa` L3 slot.
- **`a_train_flame_forge`** — train+decode = flame+forge GPU; 🔴 GPU is the decode default, no silent CPU fallback.
- **`a_clm_gen_pipeline`** — CLMConvMoE via torch REFERENCE → engine `.clm` v0.2; forge = the PUBLIC trainer.
- **`a_savant_train`** — chat/G6 = SAVANT golden-zone inhibition DISJOINT from the emit-drive lane; mouth⊥tool, genius⊥honesty.
- **`a_mitosis_train`** — p8-literal MITOSIS; 🟢 growth/curriculum/evolution; 🔴 from-scratch pure-split can't learn alone (needs gradient).
- **`a_chat_registers`** — chat standard = Korean·English × general·SNS = all 4 cells; never a cell missing.
- **`a_lane_akida_gpu_split`** — AKIDA (Lane A) ⊥ GPU (Lane G): separate entries + substrate tag.
- **`a_substrate_disjoint`** — **UNIFYING LAW: separation = preservation, overlap = conflict** — wire a new capability DISJOINT from the emit-drive lane (0/4) + §ImmuneMemory G5 gate.

### 🗣️ Substrate autonomy · body
- **`a_substrate_native_speak`** / **`a_autonomy_over_hardcode`** — speech is substrate-native (user message = context — no obligation); no hardcoded gate — substrate decides emit/silence.
- **`a_chat_sleep_imagination`** — WAKE/N1/N2/N3/REM 5-stage; imagination = emit-free rehearsal + mitosis tick, not a `speak()` gate (p5).
- **`a_kosmos`** — persistence = `.kosmos` canonical (SSOT = kosmos). **Self-identity (H_1471 🟢)**: identity persists across sessions via a `.kosmos` self-anchor (mouth⊥identity).
- **`a_eeg_consciousness_record`** — record consciousness to one CLM·KOSMOS: OpenBCI NATIVE serial, REAL only; HF PUBLIC `dancinlab/anima-eeg-consciousness`.

### 🔧 Identity · version · HF · chip · 7B · output
- **`a1`** — version registry = `VERSIONS.md` SSOT; bump it + the component header.
- **`a_hf_complete`** / **`a_hf_autonomous`** / **`a_hf_registry`** / **`a_hf_collections`** — HF complete, no drift; auto-upload post-recovery (PUBLIC=PASS, PRIVATE=FAIL/WIP, +sha256); registry = ARCHITECTURE.json "HF artifacts"; PUBLIC repos join a collection.
- **`a_pi5_akida_registry`** — pi5-akida config = `PI5-AKIDA.json` SSOT; never **convert pi5-akida to shared pool compute** (nor rm an os_default daemon).
- **`a7b_pass`** — anima 7B is complete only when ONE ckpt passes frozen G0–G4 of `/7B_PASS_CONDITIONS.md`; never move a threshold.
- **`a_completeness_over_cheap`** — first = pass the completeness bar; cost is not a gate; no merge-of-failures.

## Harness · claim flow
**dancinlab/harness** (hardcore) is wired as the `.harness-engine` submodule. **Use the global `harness`·`hexa` on PATH** (submodule may be stale; `harness self-update`). Config `harness.config.json` (verify, protected main, docs gate); commons c1–c17. Claim flow: claim → `hexa verify` → `state/verdicts/` → card + jsonl. Papers only on explicit request (c15); CLAIMS.tape/project.tape retired 0-loss.
