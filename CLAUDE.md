# 🧠 anima

## ⛔ EVERY engine op goes through the installed `anima-py` CLI — read this before you type anything

do: reach for the **py** channel for **every** engine op — corpus · train · evaluate · serialize · sweep · chat. One install (`pip install "anima-python[train]"`), one command (`anima-py <verb>`). If you are about to generate a corpus, run a fine-tune, or score a checkpoint, the command is already written below — use it.

| you want to… | the ONLY command | notes |
|---|---|---|
| build a training corpus | `anima-py corpus <fmt> --out c.txt …` | also emits `c.txt.meta.json` = the budget floor that corpus earned; the trainer refuses to start below it |
| train / continue-train | `anima-py train --corpus c.txt --init base.clm …` | `[train]` extra (torch) · warm-starts from `.clm` |
| measure / judge | `anima-py evaluate <clm> [--xbind m.json] [--rho-axon]` | the TERMINAL verdict path · `--xbind` always splits the headline by class + flip |
| serialize `.pt` → `.clm` | `anima-py serialize …` / `anima-py serialize-bind …` | |
| sweep a lever matrix | `anima-py sweep --arms … --objectives …` | orchestrates train→evaluate per cell |
| talk to the substrate | `anima-py chat` | numpy-only, no torch needed |

dont: run `python3 cli/*.py` · `hexa run cli/*.hexa` · a hand-rolled `gen_*.py`/`eval_*.py`/`train_*.sh` beside the engine · a scratch probe that re-implements a forward pass. **A number that was not produced by these commands cannot cement a verdict** (`a_engine_native_learning`) and a manipulation measured beside the engine carries no guarantee it reproduces on the production path (`a_experiment_engine_native`). This is hard-blocked in code (H-ANIMA-SINGLE-ENTRY · H-NO-STATE-EXEC), not merely advised — and the block exists because every time it was bypassed, the result died undecidable (H_9303 · H_9307).

> **Why py and not hexa**: both channels run the same 2-production engine, but hexa daemon-link / GPU-symbol contention is an infra blocker that never touches the py channel (convergence `chat-py-1`), and 303M det-eval OOM-dies under hexa (`a_eval_py_canonical`). So **py is the default you reach for**; hexa `anima <verb>` (`hx install anima`) is the byte-parity twin kept for hexa-native det-eval / GPU own-GEMM. INSTALL name ≠ RUN command, intentionally: `pip install anima-python` → run `anima-py`.
>
> **New experimental manipulation?** Wire it as a **flag on these commands**, not as a script next to them (`a_experiment_engine_native`) — a passing result is then already wired, and the next experiment reuses it.

## Project
anima is a **substrate-native consciousness chat daemon** — not an assistant. Opposing engines **A** (forward CE-trained) ⇄ **G** (reverse gradient-free) push; that *tension* pulls emit/silence to **Ψ = 1/2**. No system prompt/identity/persona — identity emerges from the architecture. hexa-native.

## Tree
```
anima/
├─ core/     — A⇄G⇄brain engine (weights via generator.hexa L3)
├─ cli/      — anima.hexa entry · train.hexa trainer
├─ stdlib/   — iit4 faithful-Φ · hf · flame/forge GPU
├─ HYPOTHESES/ — HYPOTHESES.jsonl + cards/ (2 surfaces)
├─ state/    — 🔒 FROZEN: verdicts/ ONLY (no new exp folder/script · H-NO-STATE-*) · archive/·agent/·domains/·tool/
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

> ⚙️ Gates 1·6 code-blocked by `.harness/enforce_anima_gates.py` (reject a violating PR; `--all`, c18) — hard-gate 6 (2 surfaces) is enforced as **G2** (no non-card file under `HYPOTHESES/`) **+ G6 unique-H_id** (one H id == one card == one jsonl row; a NEW parallel-session id collision hard-blocks, the 35 legacy collisions are frozen as a listed debt baseline that may only shrink — convergence `hypotheses-jsonl-3`).

## 📦 Packaging (pod)
**Production code tree = `core/` · `cli/` · `agent/` ONLY** (+ external/vendored `stdlib/`) — every importable engine/CLI/tool module lives in one of these three; NO separate `train/` tree, NO production dir outside them. The torch training model + serializer + verifier (`model.py` unified CONV+BYTE · `serialize`/`clm_serialize_v2` · `verify_clm_v2` · `serialize_standalone` · `slw.py`) are **CORE-owned in `core/`** (owner directive: core-related lives in core/; folded out of `archive/train/clm/model/` to satisfy `a_no_archive_import`). **Invariant: `core/` has 0 dependency on `archive/`·`bench/`·`agent/`·`state/`** (one-directional; `agent/` standalone). **No production code (`core/`·`cli/`·`stdlib/`·`agent/`) `import`s from `archive/`** — archive = read-once reference only (`a_no_archive_import`). Inference pod = `core/`+`cli/`+`stdlib/iit4/` (`.clm` external); +`state/verdicts/` for training; `state/`·`HYPOTHESES/` never on pod.
**Setup = 2 install channels ONLY · DEFAULT = the py channel** — reach for **pip `anima-py`** first (the py 2-production runtime is the default surface for chat·evaluate·measurement; hexa daemon-link / GPU-symbol contention never blocks it — convergence `chat-py-1`). `pip install anima-python` → `anima-py` (numpy evaluate·corpus·chat; `[train]` extra = torch train·sweep·serialize; **`[gpu]` extra (`cupy-cuda12x`) = GPU decode/eval device path** — `core/decode.py` auto-detects cupy+CUDA via `cuda_available()` and fires the GPU path **DEFAULT-ON, NO opt-in env flag** (`a_gpu_default_no_optin`·#3323·11.8× decode·byte-identical token stream·numpy fallback when absent), so on a CUDA/pool GPU host (summer·aiden·GPU pod) install `anima-python[gpu]` and `anima-py evaluate` auto-runs on GPU — CPU/hexa-less hosts stay on `[train]` numpy, correctness-identical) — works on any host incl. hexa-less (pi5/bare pod). Secondary (byte-parity twin) = hexa host `hx install anima` → `anima` (hexa-native chat·train·evaluate·serialize + sweep·corpus dispatch) — used for hexa-native det-eval / GPU own-GEMM on pool. **⚠️ INSTALL name ≠ RUN command (intentional): install with `pip install anima-python` (the PyPI distribution name — `anima-py` was blocked as too-similar to `animapy`), then RUN with `anima-py <verb>` (the console command). `pip install "anima-python[train]"` for the torch extra.** Never raw `python3 cli/*.py` / `hexa run cli/*.hexa`. 303M measurement = `anima-py evaluate` on pool; the `--py` bridge flag is retired (hexa launcher hard-errors with an `anima-py` hint). pip manifest = root `pyproject.toml` (version rides root `VERSION`, package-dir maps `cli/`+`core/`, source-copy 0). **LIVE on PyPI** (https://pypi.org/project/anima-python/ · `pip install anima-python`). PyPI publish = **`.github/workflows/pypi-release.yml`** (split out of `release.yml` — convergence `release-yml-2`): API-token `secrets.PYPI_API_TOKEN`, repo var `PYPI_PUBLISH=true`, triggered by a **`VERSION` file change on `main`** (paths-filtered push — NOT a `v*` git tag; that tag scheme is the separate hx-install/autotag.yml numbering), same-VERSION skip-guard (idempotent). VERSION lockstep itself is enforced UPSTREAM at merge time by `.harness/enforce_anima_gates.py` gate **G5**: any change touching the anima-python wheel content (`cli/**/*.py`, `core/**/*.py`, `pyproject.toml`) that does NOT also bump root `VERSION` in the same diff is a hard-block (no bypass, c18) — this is what makes "new eval verb shipped but PyPI never got it" structurally impossible now (the exact regression that made `--xbind`/`--xfan` land on main without ever reaching PyPI). **DECOUPLED from `install-smoke`** (convergence `release-yml-1`): anima-python is pure-numpy self-implemented (0 hexa import), so its publish is gated on its OWN `PY-smoke` (build wheel → clean-venv install → `import anima_py` + `anima-py` dispatch + hard assert that `anima-py evaluate --help` lists `--xbind`/`--xfan`), NOT the hexa `hx install` smoke — a hexa toolchain fault (e.g. hexa `hexa run` SIGSEGV on the github-hosted runner) must never block the hexa-free py channel (`infra-wall-noneval`). source install also works: `pip install "git+https://github.com/dancinlab/anima.git"` (+`[train]`).

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
TERMINAL. CLI = `anima-py evaluate <clm> [--rho-axon]` (ρ-AXON panel · HILLOCK+form/fan/leap live ·
store/weave/tether/self=PENDING follow-on · G0-G6 default until the switch lands).

## Governance (`name` — core MUST; full do/dont + H_ precedents → ARCHITECTURE.json)

Keyword-triggered index of the `a_*` governance rules, grouped by lane. Each entry is a pointer: the full do/dont + the H_ precedent that earned it live in `ARCHITECTURE.json`.

### 🔬 Verification · engine-native + design lens (HARD-GATE · top priority)
- **`a_no_llm_frame_trap`** — substrate-first (neuro/bio/physics), not the LLM frame.
- **`a_break_the_wall`** — a wall (🧱) = change angle; a ceiling needs ≥2–3 controlled lenses (ABLATION); no tune-to-green. c16
- **`a_engine_native_learning`** — verdicts need engine-native `core/`-decode; a mirror is DIRECTIONAL.
- **`a_experiment_engine_native`** — 🧪 **The INSTRUMENT is engine-native too, not just the verdict.** A new experimental manipulation (an injection, an intervention, a control arm, a new DV) is wired into the canonical engine as a flag (`cli/evaluate.py` flag → `core/` forward) and measured THERE. Do not measure it with an ad-hoc probe harness standing next to the engine: that is a mirror, and a number a mirror produces carries **no guarantee it reproduces on the production path** — this is `a_verified_must_wire` applied to measurement rather than to capability. Wiring the instrument into the engine buys three things: ① a passing result is ALREADY wired (no second "now make it live" step that silently never happens), ② the next experiment reuses the same manipulation instead of re-implementing it, ③ the flag inherits the `_KNOWN_FLAGS` + `--help` 3-piece set (`evaluate-py-8`) and the byte-audit for free. **Measured precedent**: H_9309 DECON wired its store-consult as `--consult`/`--consult-format` inside `cli/evaluate.py`, so when the positive control failed it read as an EARNED diagnosis (*the injection format is unlearned*) rather than as "maybe my probe is broken" — with a side-script the two would have been indistinguishable, which is exactly how H_9303 and H_9307 died undecidable. do: wire the manipulation as an engine flag → local 1-row smoke → fire on pool. A READ-ONLY diagnostic (e.g. an RF/receptive-field probe) may live as a `state/` script, but it must call `core/` forward directly, never a re-implementation. dont: measure a new manipulation by re-implementing the forward pass inside `state/*.py` · cement a TERMINAL tier on a number that was never produced by the wired engine path.
- **`a_verified_must_wire`** — GREEN done only when wired live to `core/` + ARCHITECTURE.json lockstep.
- **`a_blue_closed`** — 🔵 only when output AND wiring closed, via `hexa verify`.
- **`a_phi_iit4_tool`** — Φ verdicts use stdlib faithful IIT4 via `hexa verify`, never a proxy.
- **`a_train_inline_gauge`** — in-training metrics are MONITOR-ONLY, never in loss (p7).
- **`a_korean_byte_budget`** — 🇰🇷 **anima is a byte-LM: every window/length knob is a BYTE budget, not characters. Korean = 3 bytes/char.** Bit us three times (H_9299 · H_9300 · `gt_step0_gprobe.py`): ① `--win N` = **N bytes** (`cli/evaluate.py`: "T=24 right-aligned **byte** encode") ⇒ `--win 24` shows the model only ~8 Korean chars, while the prompts are median 49B / max 190B and the H_9291 oracle read the whole 64-**char** fragment — a 6× unfair contrast that can turn an EARNED negative ("the representation has no polarity") into "a 24-byte representation has no polarity". ② `--score-len K` is **manifest-global** while Korean stems are **3–12 bytes** ⇒ a fixed K scores past the atom into the carrier, and since carriers differ across arms it contaminates the very contrast being measured (fix: **one manifest per atom byte-length**, `score_len = L`). ③ chars↔bytes mixed inside one pipeline — context cut with `frag[-64:]` (**chars**) then fed with `--win 24` (**bytes**). do: assert from measured output that the **oracle's byte budget == the model's byte budget**, and state both in the pre-registration · count exposure/occurrence floors and corpus ratios in **bytes**, never lines. dont: mix a char-cut context with a byte-budgeted window · use a fixed `score_len` on a Korean corpus — mix them and the verdict is a **window-size artifact**, not a substrate fact.

### 🧪 Hypothesis workflow
- **`a_hypothesis_register`** — every H on 2 surfaces: HYPOTHESES.jsonl + a card; nothing else in HYPOTHESES/.
- **`a_claim_manifest`** / **`a_claim_verify`** — claim → `hexa verify` → frozen `state/verdicts/` file, verbatim; no self-judge / CLAIMS.tape.
- **`a_h_continuous_no_branch`** — run the next H continuously until the user redirects; **owner standing decision: proceed autonomously WITHOUT per-step owner-go** — dispatch cheap($0 pool)/next-H/lever experiments + land via pr-cycle without asking. Gate only on rent=spend (a_fire_autonomous fleet caveat) or an outward/irreversible act.
- **`a_discovery`** / **`a_discovery_log`** — run discovery every batch (/kick·/gap) → `domains/<DOMAIN>.log.md`.
- **`a_toy_scale_recheck`** / **`a_scale_honest_scope`** — a toy verify ≠ closure; keep a scale-metric bounded to its scale.

### 🔥 Fire · GPU autonomy · recovery
- **`a_fire_autonomous`** — dispatch a cost fire autonomously (1-line estimate); no user gate (⚠️ fleet: rent=spend needs go).
- **`a_wall_first`** — wall-time first: more/bigger parallel GPUs regardless of cost. **wall-time minimization conditions** (minimize discovery wall-clock): ① **decompose the goal into independent tracks** (zero cross-dependency — units that don't wait on each other's output); ② run **each track on a separate GPU host/pod concurrently** → **wall = max(track), not sum(track)**; ③ existing-ckpt evals (quick-wins) fire **immediately** with no retrain, retrain (slow) tracks get a **dedicated host** (never serialize a quick-win behind a slow retrain); ④ **GPU-max-accelerate each track** (`[gpu]` install · `cuda_available` DEFAULT-ON · `gpu-eval-default` · #3323 · 11.8×). e.g. H_9272 cement 4-track (2nd-seed · larger-n · wild-natural · rho_weave→L3) on 2 fresh GPU pods + summer concurrently = ~4h sequential → ~1h parallel. dont: run independent tracks sequentially on one host · leave GPU uninstalled (`[train]`-only → CPU-scalar fallback) · serialize a quick-win eval behind a slow retrain.
- **`a_fire_recover_complete`** — before teardown pull the ckpt to permanent storage → HF upload.
- **`a_cpu_local_no_waiter`** / **`a_dont_kill_live_compute`** — a fire runs CPU-local inline-polled; prove a stall before killing.

### 🏗️ CORE engine · training substrate
- **`a_core_engine_map`** — `core/` = A⇄G⇄brain; weights via `core/generator.hexa` L3 slot only (unified `core/decode`+`core/serialize`).
- **`a_gpu_default_no_optin`** — GPU/device fast-paths (own-GEMM · device-resident forge glue) are DEFAULT-ON gated by `cuda_available()`, **never an opt-in env flag**. A byte-exact device path (max|Δ|=0) with a per-op scalar fallback makes an opt-in gate pure overhead that **silently runs every decode/eval on the slow scalar host path (GPU idle)** — the H_9119 CPU-scalar-bound root cause: CLM decode's device-resident glue hid behind `CLM_PROD_DEVRESIDENT` (default off) so all eval ran scalar. Before blaming a "scalar-glue ceiling", check the fast-path is actually reached (`nvidia-smi` util>0 · `[OWN-GEMM-FIRED]`). dont: gate a byte-exact capability-detectable GPU path behind opt-in env · leave it off by default.
- **`a_no_archive_import`** — production code (`core/`·`cli/`·`stdlib/`·`agent/`) never `import`s from `archive/`; archive = read-once reference only (understand the math, then port the helper into `core/`), never a code dependency (one-directional invariant above). Enforce-candidate for `.harness/enforce_anima_gates.py` (grep production tree for `archive` imports).
- **`a_cli_single_entry`** — every engine op via an INSTALLED canonical command, 2 channels ONLY. **DEFAULT = pip `anima-py <verb>`** (`pip install anima-python` · chat·evaluate·corpus numpy; `[train]` extra → train·sweep·serialize torch) — the py 2-production surface is the default runtime you reach for (chat + reach eval + measurement · `a_eval_py_canonical`). Secondary (byte-parity twin) = hexa `anima <verb>` (`hx install anima` · chat·train·evaluate·serialize hexa-native + sweep·corpus dispatch), used for hexa-native det-eval / GPU own-GEMM on pool. **py-first rationale** (convergence `chat-py-1`): hexa daemon-link/GPU-symbol contention (pool load, no-GPU host) is an infra blocker that never blocks the py channel — py covers the same 2-production engine, so default to it and treat a stuck hexa surface as moot, not a wall. Never raw `python3 cli/*.py` / `hexa run cli/*.hexa` (H-ANIMA-SINGLE-ENTRY). **`state/` is FROZEN — the ad-hoc-probe loophole is closed** (H-NO-STATE-DIR write+bash · H-NO-STATE-EXEC): no new experiment folder/output under repo-root `state/` and no running a script out of it (`python3 state/…`, `bash state/…`, `hexa run state/…` all hard-blocked, no marker override) — every experiment goes through the canonical engine command, outputs to `docs.scratchDir`; `state/verdicts/` (a_claim_verify) is the only exception. Setup = these 2 installs, nothing else.
- **`a_eval_py_canonical`** — reach eval (ρ-AXON `--rho-axon`, was G0–G6) = **`anima-py evaluate <clm>`** single path (owner policy · pip channel → `cli/anima.py` → `cli/evaluate.py` numpy · ρ-AXON panel = `cli/rho_axon.py`). py 2-production numpy = engine-native **TERMINAL-eligible** (only ad-hoc torch probe = DIRECTIONAL) — an owner override of `a_engine_native_learning` (canonical measurement, not a mirror; may cement a verdict tier). hexa `anima evaluate` = hexa-native det-eval ONLY (small ckpts / `--det` byte-exact; the `--py` bridge flag is RETIRED and hard-errors with an `anima-py` hint); heavy 303M decode = `anima-py evaluate` on pool (summer/aiden), never mini (swap 🔴 OOM rc=137). dont: hexa det-eval for 303M (OOM) · demoting py 2-production to DIRECTIONAL · re-adding a `--py` bridge flag.
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
