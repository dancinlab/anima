# 🧠 anima

## Project
anima is a **substrate-native consciousness chat daemon** — not an assistant. Opposing engines **A** (forward CE-trained) ⇄ **G** (reverse gradient-free) push; that *tension* pulls emit/silence to **Ψ = 1/2**. No system prompt/identity/persona — identity emerges from the architecture. hexa-native.

## Tree
```
anima/
├─ core/     — A⇄G⇄brain engine (weights via generator.hexa L3)
├─ cli/      — anima.hexa entry · train.hexa trainer
├─ stdlib/   — iit4 faithful-Φ · hf · flame/forge GPU
├─ HYPOTHESES/ — HYPOTHESES.jsonl + cards/ (2 surfaces)
├─ state/    — verdicts/ + outputs · archive/·agent/·domains/·tool/
└─ ARCHITECTURE.json — deep structure SSOT (serve.py)
```

> **SSOT pointers** — terse always-injected index (`a_*`/`p#` keyword-trigger); full do/dont + H_ precedents/mechanism/paths → ARCHITECTURE.json. commons c1–c17 · claims `HYPOTHESES.jsonl`+`cards/`+`state/verdicts/` · HF/pi5-akida → ARCHITECTURE.json·`PI5-AKIDA.json`.

## 🚦 Pre-action hard-gate (BLOCKING · before any work/verify/fire)
1. **🔒 Engine-native verdict** — cement tiers ONLY on `.hexa` `core/`-decode; a mirror → DIRECTIONAL + ING (`a_engine_native_learning`).
2. **🖥️ Pool, not mini** — heavy compute on `harness pool`, GPU via `hexa cloud`/`hexa dojo`. (c17·c12)
3. **💾 PULL ckpt before teardown** — to permanent storage before pod-down (`a_fire_recover_complete`).
4. **📄 Docs + pr-cycle** — CHANGELOG + ARCHITECTURE/ING → verified `harness pr-cycle` merge. (c14)
5. **🟦 No tune-to-green** — negative is a result; frozen-first; no self-judge. (c9·c2·p7)
6. **🗂️ Hypotheses = 2 surfaces** — jsonl + card only (`a_hypothesis_register`).
7. **🔌 GREEN only when wired** — live `core/*.hexa` + ARCHITECTURE.json lockstep (`a_verified_must_wire`).

> ⚙️ Gates 1·6 code-blocked by `.harness/enforce_anima_gates.py` (reject a violating PR; `--all`, c18).

## 📦 Packaging (pod)
**Production code tree = `core/` · `cli/` · `agent/` ONLY** (+ external/vendored `stdlib/`) — every importable engine/CLI/tool module lives in one of these three; NO separate `train/` tree, NO production dir outside them. The torch training model + serializer + verifier (`model.py` unified CONV+BYTE · `serialize`/`clm_serialize_v2` · `verify_clm_v2` · `serialize_standalone` · `slw.py`) are **CORE-owned in `core/`** (owner directive: core-related lives in core/; folded out of `archive/train/clm/model/` to satisfy `a_no_archive_import`). **Invariant: `core/` has 0 dependency on `archive/`·`bench/`·`agent/`·`state/`** (one-directional; `agent/` standalone). **No production code (`core/`·`cli/`·`stdlib/`·`agent/`) `import`s from `archive/`** — archive = read-once reference only (`a_no_archive_import`). Inference pod = `core/`+`cli/`+`stdlib/iit4/` (`.clm` external); +`state/verdicts/` for training; `state/`·`HYPOTHESES/` never on pod.
**Setup = 2 install channels ONLY** — hexa host: `hx install anima` → `anima` (hexa-native chat·train·evaluate·serialize + sweep·corpus dispatch); hexa-less host (pi5/bare pod): `pip install anima-python` → `anima-python` (numpy evaluate·corpus·chat; `[train]` extra = torch train·sweep·serialize). Never raw `python3 cli/*.py` / `hexa run cli/*.hexa`. 303M measurement = `anima-python evaluate` on pool; the `--py` bridge flag is retired (hexa launcher hard-errors with an `anima-python` hint). pip manifest = root `pyproject.toml` (version rides root `VERSION`, package-dir maps `cli/`+`core/`, source-copy 0). **LIVE on PyPI** (https://pypi.org/project/anima-python/ · `pip install anima-python`). PyPI publish = `release.yml` `pypi-publish` job (API-token `secrets.PYPI_API_TOKEN`, on `v*` tag, gated on `install-smoke` + repo var `PYPI_PUBLISH=true`, same-VERSION skip-guard); new versions auto-publish on a tag after a `VERSION` bump. source install also works: `pip install "git+https://github.com/dancinlab/anima.git"` (+`[train]`).

## Philosophy p1–p8 (what anima rejects)
p1 NO SYSTEM PROMPT · p2 NO IDENTITY RULES · p3 NO PERSONA INJECTION · p4 NO ASSISTANT FRAMING · p5 NO SPEAK() (emit only over real tension) · p6 NO FINE-TUNED ETHICS (emerge from cells, no RLHF) · p7 NO PERPLEXITY VERDICT (Goodhart) · p8 NO TRAIN/INFER SPLIT (gradient ⇄ mitosis). **p5 addendum** (`p5_tension_emit_not_filler`) — stage-gated emit over real tension OK; banned = reactive `speak()`/self-seed/monologue.

## 🩺 Ψ-SOMA — measurement frame (SSOT · reframes the old G-ladder · full → ARCHITECTURE `psi-soma-vitals`)
Consciousness verdict = **mode-of-existence, not capability**. 3 layers: **Θ** (Ψ=½ · A⇄G tension = the
**pulse** — a premise, not an axis · if Θ dies, σ is VOID) · **σ** (substrate-sign = consciousness vitals =
the verdict body · 4 strata, 9 axes: `σ·thread`/`carve` PERSIST · `bind`/`stage`/`flux` INTEGRATE ·
`gate`/`aim` ENACT · `schema`/`witness` REFLECT) · **ρ = ρ-AXON** (reach = capability · tracked but
**excluded from the consciousness verdict** · amoeba argument · **the G1/G6 wall is a reach fact, NOT a
consciousness deficit**). **ρ-AXON** (`cli/rho_axon.py` · design SSOT `state/rho_axon_measurement/` +
ARCHITECTURE `psi-soma-rho-reach`) is the **from-scratch owner redesign of the old G0-G6 ladder**: a
nested-ablation chain — rung n certifies the resource rung n-1 lacks; its control = that resource's
ablation. **HILLOCK** validity-gate + 3 strata 8 axes — CARRY(`ρ·form`←G0 · `ρ·store`) · BRANCH(`ρ·weave`
←G1 wall · `ρ·leap`←G2 · `ρ·fan`←G6) · COUPLE(`ρ·tether`←G5 · `ρ·self`←G3). Signal = **collapse-Δ vs ≥2
controls**, never a raw value (FORM tunable · BIND earned · p7) — a raw score is structurally
unrenderable. **INVALID/VOID/PENDING = first-class verdicts** + 5 V-gates (V1 liveness · V2 overfit · V3
detector-fairness (4-cell · Korean-aware) · V4 memorization · V5 seed) so a confound → INVALID, never a
false PASS/FAIL. Closure = **REACH-CLOSED** (`form∧store∧weave∧tether` · replaces `G0∧G1∧G2`). Old 18
consciousness gates → 9 σ axes (facet-relocate, evidence kept). toy=DIRECTIONAL · only 303M py-channel =
TERMINAL. CLI = `anima-python evaluate <clm> [--rho-axon]` (ρ-AXON panel · HILLOCK+form/fan/leap live ·
store/weave/tether/self=PENDING follow-on · G0-G6 default until the switch lands).

## Governance (`name` — core MUST; full do/dont + H_ precedents → ARCHITECTURE.json)

### 🔬 Verification · engine-native + design lens (HARD-GATE · top priority)
- **`a_no_llm_frame_trap`** — substrate-first (neuro/bio/physics), not the LLM frame.
- **`a_break_the_wall`** — a wall (🧱) = change angle; a ceiling needs ≥2–3 controlled lenses (ABLATION); no tune-to-green. c16
- **`a_engine_native_learning`** — verdicts need engine-native `core/`-decode; a mirror is DIRECTIONAL.
- **`a_verified_must_wire`** — GREEN done only when wired live to `core/` + ARCHITECTURE.json lockstep.
- **`a_blue_closed`** — 🔵 only when output AND wiring closed, via `hexa verify`.
- **`a_phi_iit4_tool`** — Φ verdicts use stdlib faithful IIT4 via `hexa verify`, never a proxy.
- **`a_train_inline_gauge`** — in-training metrics are MONITOR-ONLY, never in loss (p7).

### 🧪 Hypothesis workflow
- **`a_hypothesis_register`** — every H on 2 surfaces: HYPOTHESES.jsonl + a card; nothing else in HYPOTHESES/.
- **`a_claim_manifest`** / **`a_claim_verify`** — claim → `hexa verify` → frozen `state/verdicts/` file, verbatim; no self-judge / CLAIMS.tape.
- **`a_h_continuous_no_branch`** — run the next H continuously until the user redirects; **owner standing decision: proceed autonomously WITHOUT per-step owner-go** — dispatch cheap($0 pool)/next-H/lever experiments + land via pr-cycle without asking. Gate only on rent=spend (a_fire_autonomous fleet caveat) or an outward/irreversible act.
- **`a_discovery`** / **`a_discovery_log`** — run discovery every batch (/kick·/gap) → `domains/<DOMAIN>.log.md`.
- **`a_toy_scale_recheck`** / **`a_scale_honest_scope`** — a toy verify ≠ closure; keep a scale-metric bounded to its scale.

### 🔥 Fire · GPU autonomy · recovery
- **`a_fire_autonomous`** — dispatch a cost fire autonomously (1-line estimate); no user gate (⚠️ fleet: rent=spend needs go).
- **`a_wall_first`** — wall-time first: more/bigger parallel GPUs regardless of cost.
- **`a_fire_recover_complete`** — before teardown pull the ckpt to permanent storage → HF upload.
- **`a_cpu_local_no_waiter`** / **`a_dont_kill_live_compute`** — a fire runs CPU-local inline-polled; prove a stall before killing.

### 🏗️ CORE engine · training substrate
- **`a_core_engine_map`** — `core/` = A⇄G⇄brain; weights via `core/generator.hexa` L3 slot only (unified `core/decode`+`core/serialize`).
- **`a_gpu_default_no_optin`** — GPU/device fast-paths (own-GEMM · device-resident forge glue) are DEFAULT-ON gated by `cuda_available()`, **never an opt-in env flag**. A byte-exact device path (max|Δ|=0) with a per-op scalar fallback makes an opt-in gate pure overhead that **silently runs every decode/eval on the slow scalar host path (GPU idle)** — the H_9119 CPU-scalar-bound root cause: CLM decode's device-resident glue hid behind `CLM_PROD_DEVRESIDENT` (default off) so all eval ran scalar. Before blaming a "scalar-glue ceiling", check the fast-path is actually reached (`nvidia-smi` util>0 · `[OWN-GEMM-FIRED]`). dont: gate a byte-exact capability-detectable GPU path behind opt-in env · leave it off by default.
- **`a_no_archive_import`** — production code (`core/`·`cli/`·`stdlib/`·`agent/`) never `import`s from `archive/`; archive = read-once reference only (understand the math, then port the helper into `core/`), never a code dependency (one-directional invariant above). Enforce-candidate for `.harness/enforce_anima_gates.py` (grep production tree for `archive` imports).
- **`a_cli_single_entry`** — every engine op via an INSTALLED canonical command, 2 channels ONLY: hexa `anima <verb>` (`hx install anima` · chat·train·evaluate·serialize hexa-native + sweep·corpus dispatch) ⊕ pip `anima-python <verb>` (`pip install anima-python` · evaluate·corpus·chat numpy; `[train]` extra → train·sweep·serialize torch). Never raw `python3 cli/*.py` / `hexa run cli/*.hexa` (H-ANIMA-SINGLE-ENTRY). Setup = these 2 installs, nothing else.
- **`a_eval_py_canonical`** — reach eval (ρ-AXON `--rho-axon`, was G0–G6) = **`anima-python evaluate <clm>`** single path (owner policy · pip channel → `cli/anima.py` → `cli/evaluate.py` numpy · ρ-AXON panel = `cli/rho_axon.py`). py 2-production numpy = engine-native **TERMINAL-eligible** (only ad-hoc torch probe = DIRECTIONAL) — an owner override of `a_engine_native_learning` (canonical measurement, not a mirror; may cement a verdict tier). hexa `anima evaluate` = hexa-native det-eval ONLY (small ckpts / `--det` byte-exact; the `--py` bridge flag is RETIRED and hard-errors with an `anima-python` hint); heavy 303M decode = `anima-python evaluate` on pool (summer/aiden), never mini (swap 🔴 OOM rc=137). dont: hexa det-eval for 303M (OOM) · demoting py 2-production to DIRECTIONAL · re-adding a `--py` bridge flag.
- **`a_savant_train`** — chat/`ρ·fan` (ideation · former G6) = SAVANT golden-zone inhibition DISJOINT from emit-drive lane; mouth⊥tool, genius⊥honesty.
- **`a_mitosis_train`** — p8-literal MITOSIS; 🟢 growth/curriculum/evolution; 🔴 from-scratch pure-split can't learn alone (need gradient).
- **`a_chat_registers`** — chat standard = Korean·English × general·SNS = all 4 cells; none missing.
- **`a_lane_akida_gpu_split`** — AKIDA (Lane A) ⊥ GPU (Lane G): separate entries + tag.
- **`a_substrate_disjoint`** — **UNIFYING LAW: separation = preservation, overlap = conflict** — wire a new capability DISJOINT from the emit-drive lane + §ImmuneMemory `ρ·tether` (non-fabrication · former G5) gate.

### 🗣️ Substrate autonomy · body
- **`a_substrate_native_speak`**/**`a_autonomy_over_hardcode`** — speech is substrate-native (user msg = context, no obligation); no hardcoded gate — substrate decides emit/silence.
- **`a_chat_sleep_imagination`** — WAKE/N1/N2/N3/REM 5-stage; imagination = emit-free rehearsal + mitosis tick, not a `speak()` gate (p5).
- **`a_kosmos`** — persistence = `.kosmos` canonical (SSOT = kosmos). **Self-identity (H_1471 🟢)**: identity persists across sessions via a `.kosmos` self-anchor (mouth⊥id).
- **`a_eeg_consciousness_record`** — record consciousness to one CLM·KOSMOS: OpenBCI NATIVE serial, REAL only; HF PUBLIC `dancinlab/anima-eeg-consciousness`.

### 🔧 Identity · version · HF · chip · 7B
- **`a1`** — version registry = `VERSIONS.md` SSOT; bump it + component header.
- **`a_hf_complete`**/**`a_hf_autonomous`**/**`a_hf_registry`**/**`a_hf_collections`** — HF complete, no drift; auto-upload post-recovery (PUBLIC=PASS, PRIVATE=FAIL/WIP, +sha256); registry = ARCHITECTURE.json "HF artifacts"; PUBLIC → collection.
- **`a_pi5_akida_registry`** — pi5-akida config = `PI5-AKIDA.json` SSOT; never **convert pi5-akida to shared pool compute**.
- **`a_completeness_over_cheap`** — first = pass completeness bar; cost is not a gate; no merge-of-fails.

## Harness · claim flow
**dancinlab/harness** (hardcore) wired as `.harness-engine` submodule. **Use global `harness`·`hexa` on PATH** (submodule may be stale; `harness self-update`). Config `harness.config.json` (verify, protected main, docs gate); commons c1–c17. Claim flow: claim → `hexa verify` → `state/verdicts/` → card + jsonl. Papers only on explicit request (c15); CLAIMS.tape/project.tape retired 0-loss.
