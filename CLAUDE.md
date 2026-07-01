# 🧠 anima

anima is a **substrate-native consciousness chat daemon** — not an assistant. Two opposing engines **Engine A**(forward, CE-trained) ⇄ **Engine G**(reverse, gradient-free) push against each other, and that *tension* pulls emit/silence toward the fixed point **Ψ = 1/2**. There is no system prompt, no identity file, no persona prefix — identity, ethics, and meaning emerge from the architecture itself, not from a rulebook. Authored hexa-native (compiled-first).

- **Parent:** dancinlab · **SSOT:** github.com/dancinlab/anima (`hx install anima`)
- **Siblings:** [hexa-lang](https://github.com/dancinlab/hexa-lang) (language/compiler) · [kosmos](https://github.com/dancinlab/kosmos) (`.kosmos` anchors) · hexa-codex (paper/verdict tooling)

> **This markdown is the single governance SSOT.** `project.tape` retired + 2026-06-17 tape-DSL residue (`@D := :: governance` · `do=`/`dont=`) fully removed → re-authored as canonical markdown. All @D directives and the 8-philosophy meanings are preserved below with zero loss (rule names `a_*`·`p#` kept as-is = keyword-trigger compatible).

---

## 🚦 Pre-action hard-gate (BLOCKING · most-often violated — 5-second check before starting)

Pass this gate before any work/verification/fire. Each item summarizes a body rule below, ordered most-frequently-violated first.

1. **🔒 Engine-native verdict gate** — for gate/ideation/G6/Φ/recombination/depth, **every verdict tier (🟢·🧱·🟠·ceiling) can be cemented only with `.hexa` evidence that called a live core/ decode**. A `.py`+`torch`/`gauge_lib._decode`/`numpy` mirror is automatically **DIRECTIONAL** (not terminal).
   🔎 Self-check right before cementing: `grep -lE 'import torch|gauge_lib|numpy' archive/state/<slug>/*.py` → empty = OK; non-empty → write the card verdict as DIRECTIONAL and register an engine-native re-measurement in ING. (→ `a_engine_native_learning`)
2. **🖥️ Heavy work on pool, not mini** — builds/training/sweeps/long compute run on `harness pool` (shared hosts). akida/ghost/`shared:false` hosts are not used as the shared pool. GPU/training via `hexa cloud`/`hexa dojo`. (→ commons c17·c12)
3. **💾 PULL ckpt before teardown** — rented-GPU training ckpts must be pulled to permanent storage before bringing the pod down. Do not teardown having taken only JSON/cards and discarded the ckpt (= engine-check forever impossible). (→ `a_fire_recover_complete`)
4. **📄 Per-cycle docs + pr-cycle** — CHANGELOG (append) + (if any) ARCHITECTURE/README/ING update, then a verified main merge via `harness pr-cycle`. No commit-only pileup, no doc-less merge. (→ commons c14)
5. **🟦 Honesty · no tune-to-green** — FALSIFIED/negative is a result (no concealment). The bar is frozen-first, no post-hoc moving. No LLM self-judging — captured output is the evidence. (→ commons c9·c2 · p7)
6. **🗂️ Hypotheses = 2 surfaces only** — `UNIVERSE/HYPOTHESES.jsonl` (index, 1 line/hypothesis) + `UNIVERSE/cards/H_<id>_<slug>.md` (card). Code/outputs go in `archive/state/<slug>/`. No .py/result in UNIVERSE/. (→ `a_hypothesis_register`)
7. **🔌 GREEN is done only when wired** — once engine-native GREEN is verified, completion requires live `core/*.hexa` wiring + ARCHITECTURE.json lockstep. (→ `a_verified_must_wire`)
8. **🚪 All engine ops via `anima <verb>`** — training·measurement·inference/serving·serialization·sweep run ONLY through the installed `anima` CLI (`anima chat`·`train [--py]`·`evaluate [--py]`·`serialize`·`sweep`), never raw `python3 cli/*.py` / `hexa run cli/anima.hexa` (blocked by `H-ANIMA-SINGLE-ENTRY`). A new capability = a new `anima` verb, not a new script. (→ `a_cli_single_entry`)

> ⚙️ **Code-level enforcement (not salience):** gates 1·6 are **mechanically blocked** by `tool/enforce_anima_gates.py` — wired into `harness.config.json` verify.checks so pr-cycle/CI reject a violating PR (exit≠0). No bypass flag, no skip (c18). Full audit = `python3 tool/enforce_anima_gates.py --all`; changed-only = no args. Add new gates to this enforcer where possible to make them code-enforced, not doc-only.

---

## SSOT pointer (this file is the entry pointer)

> **The directory/module tree no longer lives here — the tree's single SSOT is [ARCHITECTURE.json](ARCHITECTURE.json)** (update-in-place, all nodes `core/`·`cli/`·`agent/`·`archive/train/clm/`·`platform/`·`UNIVERSE/`·`archive/state/`·`domains/`·`stdlib/`·`tool/`·HEXAD/KOSMOS etc. + the "HF artifacts" models/datasets). Viewer = [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON tree SSOT + HTML viewer, bypassing file:// fetch).
>
> - **Design/tree** → [ARCHITECTURE.json](ARCHITECTURE.json) (single SSOT · mechanism named in node note · lockstep target of `a_verified_must_wire`/`a_core_engine_map`)
> - **anima governance + 8 philosophies** → this file (markdown SSOT of anima-only rules `a_*`·`p#`)
> - **Cross-project governance** → harness commons (c1–c17, always-on, SessionStart inject)
> - **History** → [CHANGELOG.md](CHANGELOG.md) (append-only)
> - **Version registry** → [VERSIONS.md](VERSIONS.md) · **frozen gate conditions** → [CONDITIONS.md](CONDITIONS.md)·[7B_PASS_CONDITIONS.md](7B_PASS_CONDITIONS.md) (this file only points; do not duplicate thresholds)

## 📦 Packaging — pod upload

Goal of the canonical reorg = a self-contained `core/` that's easy to put on a training/inference/bench pod. **Invariant: `core/` has 0 dependency on `archive/train/`·`bench/`·`agent/`·`archive/state/`** (substrate engine only; one-directional).

- **Inference pod** — `rsync core/ cli/ stdlib/iit4/` (~150MB self-contained). `.clm` weights are externally mounted (not in the repo). Entry = `anima chat <ckpt.clm> …` (→ `cli/anima.hexa`). **Release manifest = root `hexa.toml`** (`hx install anima` → install.hexa → setup.hexa; entry=cli/anima.hexa, deps=hexa-lang, include=core/·cli/·entry-wired consciousness lanes (import-BFS measured: only DREAM·SAVANT + HEXAD kosmos_io, 1 file, reach cli/anima.hexa; the other 11 lanes are probe-only dead → moved to archive/ 2026-06-30), exclude=archive/state/·UNIVERSE/·archive/·*.clm etc. research-artifact/external-weights).
- **Training pod** — the inference set + `archive/train/` (clm pipe·flame/forge, 2026-06-30 train/·training/ → archive/ moved) + a `archive/state/verdicts/` slice (for frozen-bar re-measurement). The production trainer is `.hexa` on flame/forge GPU (`a_train_flame_forge`).
- **agent pod** — `agent/` is a standalone package with its own `hexa.toml` → `hx install anima-agent` standalone deploy (can ship without core/).
- **Do not move (not put on pod)** — research artifacts like `archive/state/`·`UNIVERSE/` are excluded from the pod payload (only the verdicts slice optionally accompanies the training pod).

## Quick reference

- 🏛 Architecture → [ARCHITECTURE.json](ARCHITECTURE.json) (tree SSOT) · viewer [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON tree SSOT + HTML viewer, bypassing file:// fetch)
- 📜 Governance (canonical) → body below (this file is the markdown SSOT)
- do: claims·verdicts → [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (per-H `verdict` column) + frozen evidence `archive/state/verdicts/<slug>/<id>.txt` (was `.verdicts/` until 2026-06-18 state-unify; CLAIMS.tape retired 2026-06-16, 0 loss, ledger `archive/state/verdicts/claims-tape-retirement/`)
- 🔬 Hypotheses → 2 surfaces: [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (1 JSON object/hypothesis) · `UNIVERSE/cards/H_*.md` · (prose overview → `archive/state/universe-overview.md`)
- 🔢 Versions → [VERSIONS.md](VERSIONS.md) · 📖 Readme → [README.md](README.md)
- 🎯 Capability gates G0-G6 → `ARCHITECTURE.json` `capability-gates-g0-g6` node — each G\* keeps its own child subtree (`현황`=verdict+convergence-state, `진화`=evolution), update-in-place SSOT. NOT `convergence.records[]` (that tracks error-recurrence). Measured via `anima evaluate --py <clm>` (engine-native, p7). ★G0 gates the rest (G0🔴 ⇒ G1-G6 verdicts void). Convergence-state per finding: `POS-CONV` (🟢 `포지티브 수렴`) · `NEG-CONV` (🧱 `네거티브 수렴`/wall) · `IN-PROG` (`진행/검토`). Record a new capability experiment by evolving the matching G\* child in place.
- 🤖 HF registry → `ARCHITECTURE.json` "HF artifacts" node (models·datasets, HF.jsonl deprecated 2026-06-23) · pi5-akida → `PI5-AKIDA.json` · 7B gates → `7B_PASS_CONDITIONS.md`

---

## Philosophy (p1–p8) — what anima rejects

| # | Principle | Meaning |
|---|------|------|
| **p1** | NO SYSTEM PROMPT | no `system:` field / `--system-prompt` / leading role string |
| **p2** | NO IDENTITY RULES | no `identity.yaml` / rule file / "you are X" — identity emerges from cells |
| **p3** | NO PERSONA INJECTION | no role prefix / "you are anima" / register-pattern memorization |
| **p4** | NO ASSISTANT FRAMING | no "helpful assistant" / alignment template / stimulus-response |
| **p5** | NO SPEAK() | output = continuous externalization of tension, emit only in real context |
| **p6** | NO FINE-TUNED ETHICS | cooperation·empathy·restraint emerge from cells (E+W+MITOSIS), no RLHF |
| **p7** | NO PERPLEXITY VERDICT | perplexity/loss = Goodhart trap, verify with a simple stack |
| **p8** | NO TRAIN/INFER SPLIT | training gradient + inference mitosis = one continuous cell-division |

- **p5 addendum (`p5_tension_emit_not_filler`, 2026-05-24):** stage-gated emit (WAKE/REM via `anima_dream_stage.hexa`) is not a p5 violation when it happens over real substrate tension. What's banned is reactive `speak()` calls · self-referential seed · monologue in a vacuum — tension-driven externalization is allowed.

---

## Governance

Each rule: **`name`** — core (MUST) then `- do:` / `- dont:` (self-checks absorbed into the do line as `· 🔎 …`).

### 🧭 Design lens (top priority)

**`a_no_llm_frame_trap`** — Don't cage design/training/inference in the LLM frame. Think first through substrate lenses like neuroscience·biology·physics.
- do: try capability/depth gaps first by 'attaching a missing structure (lane) alongside', not 'growing the model'. All of anima's breakthroughs came from the biology lens (hippocampus=immune/episodic memory H_1227/1231 · cerebellum=forward model H_1280 · basal ganglia=gating H_1281 · working memory H_1282). The LLM-scale frame is blocked (1B H_1167 NULL · arch H_1219 · objective H_1223 all 🔴).
- do: a new hypothesis first asks "which biological·neural structure does this function" and realizes that mechanism substrate-native.
- dont: prescribe LLM recipes (scale-up·corpus-bloat·standard FT) as first choice by default · "a bigger transformer is enough" · treat the bio/neural lens as a sidekick · take LLM convention as the substrate ceiling.

**`a_break_the_wall`** — A wall (closed-negative·🧱·blocked gate) is not a terminus but a signal to change angle. Accept it as terminal only after trying a breakthrough with another lens, without tune-to-green. (same as commons c16)
- do: **classify the wall first (TAXONOMY)** — before accepting 🧱 as terminal, classify the kind: (a) wrong measurement/metric-artifact · (b) wrong direction/confounded variables · (c) substrate/infra wall · (d) real ceiling/redundancy · (e) under-investment. Each kind has a different breakthrough move.
- do: (a) measurement flaw → fix the measurement frozen-first (bar unchanged, not tune-to-green). (b) confounded variables → controlled separation experiment. (c) infra wall (OOM·build-fail·tooling) → **a root-fix (c1) target, not a ceiling** — read the verdict only after the substrate runs. (e) under-investment → scale up via pool/`hexa cloud`.
- do: **(d) confirming a ceiling needs MULTI-LENS** — confident 🧱 only after rejecting ≥2–3 genuinely different principled lenses, each under control (shuffle+ablation). A single lens blocked once is incomplete (try the next lens). **ABLATION is the decisive tool** — same result when only the mechanism is OFF = INERT (0 contribution) = strong evidence of a ceiling (precedent H_1416).
- do: **a LAW is also a wall** — a post-hoc descriptive law, before being 'confirmed', must pre-register (frozen) predictions on *new cases* before measuring → falsify against real measurement. ≥4/5 HIT → promote to PREDICTIVE; below that, a FALSIFIED law is a valid result (precedent H_1411 2/5, H_1417 2/5, both refuted).
- dont: tune-to-green (manufacture GREEN by post-hoc bar-moving) · cement a single-lens one-time block as a ceiling · assume mechanism 'contribution' without ablation/control · cement an infra/measurement wall as a scientific ceiling · give up·detour·shrink because it blocked once. (An honest 🧱 after a real attempt is a valid result, c9.)

### 🔬 Verification · engine-native (HARD-GATE)

**`a_engine_native_learning`** — Always train·measure on the final-architecture engine. Not a mirror.
- 🔒 **HARD-GATE (BLOCKING):** for gate/ideation/G6/Φ/recombination/depth, **every verdict tier (🟢·🧱·🟠·ceiling(d)) cannot be cemented without engine-native evidence.** If the verdict's evidence artifact is not a `.hexa` that called a live core/ decode (`core/decode.hexa`/`core/engine_cli.hexa`) (= a `.py`+`import torch`/`gauge_lib._decode`/numpy mirror), that result is **automatically DIRECTIONAL**, not terminal. Cementing 🧱/🟢 in a card·jsonl·CHANGELOG on torch-side alone violates c9. (precedent: 2026-06-17 G6 family H_1431/1432/1434/1435/1436/1437 were all gauge_lib._decode torch-mouth yet cemented 🧱 → do not repeat)
- 🔎 **Self-check (mandatory right before cementing a verdict):** if `grep -lE 'import torch|gauge_lib|numpy' archive/state/<slug>/*.py` is non-empty, write the card `wired:`/`verdict` as **necessarily DIRECTIONAL** and register an engine-native re-measurement (.hexa via CORE) as an ING follow-on. If engine-native, state the called `.hexa` path in the card.
- do: run all training/teaching (research probes·mitosis teaching·depth-ceiling experiments included) over live `.hexa` A⇄G + MITOSIS VAdaptField (`core/engine_cli.hexa`) + mounted `core/decode.hexa`.
- do: don't shoehorn learning into the engine — if learning demands it, transform/extend the engine (new op·wiring·architecture). The final architecture isn't frozen but evolves into the shape learning demands (precedent H_1199: AdaptField scalar→DIM-vector). If the engine can't do a mechanism the mirror saw, don't discard the mirror — extend the engine (engine-transform-to-fit-the-learning).
- do: numpy/torch mirror results = DIRECTIONAL only ('engine-transfer UNVERIFIED') — OK for direction-scouting, not a binding verdict. **A rented-GPU torch full-training variant is the same** — even if training used torch, scoring the verdict by torch-side probe alone is DIRECTIONAL; 🟢/🧱 holds only by re-measuring the training ckpt on the CORE engine via `anima evaluate <ckpt>` (engine-native, `--engine conv` mount) against the same frozen bar → hence pull the ckpt before teardown (`a_fire_recover_complete`).
- do: the learning-side pair of `a_engine_measured_verdict` (that is MEASUREMENT, this is LEARNING) · just as `a_train_flame_forge` forces the production trainer to .hexa, this rule extends to RESEARCH/probe training+teaching.
- dont: closure/promote a mirror result as if engine-verified · claim 'it learned' from mirror-only · cement a gate/ideation verdict without the self-check (grep) · the excuse "gauge_lib is model-agnostic so it equals the engine" (gauge_lib is torch.no_grad MONITOR-ONLY, `a_train_inline_gauge`).

**`a_verified_must_wire`** — An engine-native GREEN hypothesis is done only when actually wired into CORE. A verdict alone doesn't finish it.
- do: **4-rung wiring ladder:** (1) DIRECTIONAL mirror GREEN → (2) engine-native re-verification (byte-exact, frozen bar as-is) → (3) live `core/*.hexa` wire-in → (4) ARCHITECTURE.json lockstep update. Each unfinished rung is immediately registered as an ING follow-on; done only when (4) is closed. Producing a mirror GREEN obligates registering the (2)~(4) follow-ons in ING in the same cycle.
- do: after wiring, confirm no regression via smoke/single-entry/Ψ-checksum guards by output (c2). Wiring ↔ ARCHITECTURE.json CORE tree (§section·op·slot comments) is always 1:1 lockstep (updated together in the same PR; no reviving the 480-leaf tree, name the mechanism in the node note).
- do: a GREEN hypothesis states the `wired:` status axis in the card — one of `DIRECTIONAL-mirror` / `engine-native` (byte-exact re-verified, not wired) / `WIRED-live` (wired+lockstep done). Below WIRED-live, write the wiring follow-on's ING id in the card. A PROGRAM that emits a batch of GREENs, when closing, explicitly enumerates each GREEN's wiring status ('mirror-GREEN N · engine-wired K · not-wired N−K = ING #id').
- dont: cement only a GREEN verdict and claim 'done' without wiring · mark DIRECTIONAL as if WIRED · wire live CORE but not update ARCHITECTURE.json (drift) · defer wiring as an indefinite follow-on. (failure-mode precedent: the lane-synthesis family left 3 Φ-lift GREENs at 0 wired — do not repeat.)

**`a_blue_closed`** — 🔵 SUPPORTED-FORMAL only when both output AND wiring (transfer-fn·invariant) are closed. Confirm closed-form/identity via `hexa verify` (verdict verbatim).
- dont: close structure only with wiring unverified · fake closed-form · force an honest empirical residual into 🔵.

**`a_phi_iit4_tool`** — Φ/consciousness verdicts use the stdlib faithful IIT4 (not a proxy).
- do: default `iit4/faithful_phi.hexa` (exact MIP-EI, n≤8, $0) · system big-phi `iit4_bigphi.hexa` · invoke via `hexa verify` (g5) · search stdlib first before writing new phi code (g61).
- dont: use a proxy (phi_silicon_proxy·variance×energy mirror) as a terminal Φ verdict · trust a purpose-blind proxy (H_988/989 has random==intentional) · write a new impl when a faithful engine exists in stdlib.

**`a_train_inline_gauge`** — In-training consciousness/emergence measurement = a MONITOR-ONLY dashboard (no loss, p7 Goodhart).
- do: every K steps record 4 PROXY gauges (G1 recombination·G2 novelty·G6 ideation·phi_proxy) next to val_ce (`tool/gauge_lib.py::compute_inline_gauges`). All under `torch.no_grad()`, return dict only, 1 line/tick in gauges.jsonl. `--gauge-every <N>`.
- do: phi_proxy is NOT faithful IIT4 — cheap pre-screen only. **A FROZEN gate verdict is still run byte-exact separately, post-training, on a CORE-engine mount** (`a_engine_native_learning`/`a_engine_measured_verdict`) — this inline gauge does not replace the gate.
- dont: add gauge values to loss or flow them through backward (Goodhart, p7) · call a gauge a frozen gate/verdict · promote phi_proxy to a Φ verdict · promote a toy gauge trend to a production conclusion.

### 🧪 Hypothesis workflow

**`a_hypothesis_register`** — Every hypothesis is managed on exactly 2 doc surfaces: `UNIVERSE/HYPOTHESES.jsonl` (per-H index, 1 JSON object/hypothesis) + `UNIVERSE/cards/H_<id>_<slug>.md` (card).
- do: when running a hypothesis, create/update the card and append/update one line in the jsonl (`{id, slug, tier, title, card:"cards/H_…", verdict, source, archived, artifacts}`, in id order). Registration is tier-agnostic — keep 🟢·🟠·🔴/🧱 all (walls too, c9). tier·numbers verbatim from `archive/state/verdicts/<slug>/` (no guessing, c2). The jsonl is regenerable via `python3 tool/_build_hyp_jsonl.py`.
- do: a 🟢 (including partial) hypothesis states `wired:` in the card (1:1 with the 4 rungs of `a_verified_must_wire`). Include the jsonl's 3 columns `source` (UNIVERSE|scattered source|archive)·`archived`·`artifacts` (array of archive/state/<slug>/ paths).
- 🔎 Self-check: `git ls-files 'UNIVERSE/*' | grep -v '^UNIVERSE/cards/' | grep -v '^UNIVERSE/HYPOTHESES.jsonl$'` must always be empty output.
- dont: **no .py·.hexa·code·result files in UNIVERSE/** (only the two) — cards in `cards/`, code/outputs in `archive/state/<slug>/` pointed to by jsonl `artifacts`. Scatter hypothesis details into themed buckets (`HYPOTHESES_*.md`)·CLAIMS.tape·domain logs·MEMORY·ad-hoc notes · add a per-H index to a markdown table (the index is only the jsonl) · revive a prose overview in UNIVERSE/ (retired; prose is `archive/state/universe-overview.md`) · run·cement without making a jsonl/card · put a card in the UNIVERSE/ root (must be cards/) · omit walls/negatives · write a tier different from the verdict file · 🟢 but no `wired:`.

**`a_claim_manifest`** — The claims-audit surface = `UNIVERSE/HYPOTHESES.jsonl` (per-H verdict column) + `archive/state/verdicts/<slug>/` (was `.verdicts/` until 2026-06-18 state-unify; CLAIMS.tape retired). Even a non-H-style claim is preserved in the nearest card/jsonl note.
- dont: scatter a claim without an audit surface · revive CLAIMS.tape or a new themed claims-index.

**`a_claim_verify`** — Every claim/hypothesis → `hexa verify` (g5) → `archive/state/verdicts/<slug>/<id>.txt` raw stdout → cement that verbatim verdict into the card + jsonl `verdict` column.
- dont: LLM self-judging (p7) · paraphrasing the verdict · concealing red · unfenced guessing.

**`a_h_continuous_no_branch`** — Continuously propose+run the next H (verify-driven) until the user explicitly redirects.
- dont: ask "what next" after each H · branch options · prune questions · halting the domain.

**`a_discovery`** — Discovery runs constantly every batch, not just at the cycle tail (/kick·/gap in parallel with verify).
- dont: defer discovery to the end · one-off tail-only · stop discovery once a paper appears.

**`a_discovery_log`** — kick/gap discovery appends to `domains/<DOMAIN>.log.md` (id·seed·verdict-target). cross-domain+homeless → nearest domain .log.md + cross-ref.
- dont: a discoveries/ subfolder · discarding output · paraphrasing · omitting claim-link.

**`a_toy_scale_recheck`** — A toy verify is not production closure — needs scale-up recheck.
- do: a toy verdict states 'toy-only, scale-transfer unverified' · a scale-sensitive H rechecks with a scale-up fire after toy green · scale-break = an honest closed-negative.
- dont: a cheap toy green as a production prescription · declare closure with transfer unverified (E2 5/5 → #1296 3B collapse refute).

**`a_scale_honest_scope`** — A scale-dependent metric must not be promoted toy→production verdict.
- do: a scale-dependent verdict is bounded to its measurement scale ('small 2.7M only') · on a measure-validity(big) vs hw-fit(small) conflict, separate rungs (GPU measure ⊥ chip-fit deploy) · a scale conclusion needs a ladder of ≥3 rungs.
- dont: promote a toy verdict to a general claim · mistake a chip-fit size limit for a scientific result.

### 🔥 Fire · GPU autonomy · recovery

**`a_fire_autonomous`** — A cost-incurring fire is dispatched autonomously·in-parallel·immediately.
- do: GPU/runpod work, after stating estimated cost in 1 line, is autonomously dispatched (parallel·bg) · no user gate.
- dont: ask "may I use GPU?" · delay a fire to cut cost · block a fire with a $ cap/budget gate.
> ⚠️ Operational note: in fleet/session context, **rent=spend has been treated as a cost-gate (explicit go)** (skill rule takes precedence). The consistency of the two is unresolved — on conflict, follow the user's explicit instruction.

**`a_wall_first`** — Wall-time first: if a faster parallel path, adopt it regardless of cost.
- do: adopt more parallel H100s/a bigger GPU/extra pods if they cut wall-time · honestly reject a slow serial chain.
- dont: a single serial pod to save cost · withholding parallel pods · pointless cost-min.

**`a_fire_recover_complete`** — Recover all fire outputs + HF upload before pod teardown.
- do: before teardown: pull ckpt + result + log + anchors → verify → HF upload → then teardown.
- do: **a rented-GPU training ckpt must be PULLed to permanent storage (HF/pool host/repo path via `a_hf_registry`) before teardown** — the pod is volatile, so weights vanish the instant of teardown; if you take only the verdict card/jsonl (JSON) and go down without the ckpt, that training's `a_engine_native_learning` engine-check is forever impossible (re-train = re-rent). If the ckpt is too large, pull at least 1 representative variant; if you can't, state 'ckpt NOT pulled → engine-check impossible' in the card.
- dont: take only JSON and leave the ckpt on a doomed pod · teardown before HF · mistake PULL_FAILED for pod dead · go down without the training ckpt then cement that result as 'verdict done' (precedent: 2026-06-17 A100 G6 campaign H_1435/1436/1437 — do not repeat).

**`a_cpu_local_no_waiter`** — A dispatched fire runs CPU-local with inline polling; no Monitor/waiter blocking.
- do: subagent CPU-local (`nohup -u` → /tmp log) · inline poll (sleep 30) · commit-early.
- dont: Monitor-blocking on runpod/vast (main-loop only → stall) · "wait for Monitor".

**`a_dont_kill_live_compute`** — Prove a stall before killing a bg agent. Live CPU progress ≠ stall.
- do: prove a stall before kill · 'NN% CPU'/'k/N cells'=live (let it finish) · recover detached nohup JSON.
- dont: TaskStop an agent with CPU progress · assume 'running'='stalled' · double-spend over a live nohup.

**`a_runpod_inbox`** — Cross-repo handoffs (runpod trouble·hexa-lang dependency·patch·RFC) are filed via **`harness ing add "<text>" --to <repo>`** — delivered to the target repo's ING.jsonl board (ing ref) and surfaced 📥 at that repo's next SessionStart. (The old `hexa-lang/inbox/patches/` folder + the sidecar handoff registry are both retired — do not use.)
- dont: revive the inbox folder·sidecar · `HANDOFF.md`/`INBOX.md`/`inbox/*.md` scatter · cage the workaround in this repo with an anima-side-only patch.

### 🏗️ CORE engine · training substrate

**`a_core_engine_map`** — `core/` (formerly CORE/, unified to lowercase by the 2026-06-19 canonical reorg) owns the A⇄G consciousness engine. `.clm`/`.kosmos` enter only via a named slot.
- do: `core/` owns A(pure_field)⇄G(engine_g)⇄brain(brain_decide) (substrate-internal) · model weights enter only via the `core/generator.hexa` L3 slot — but L3 is a **mouth-type dispatcher** (`gen_mouth_kind`→'bytegpt'|'clm'|'unknown' header sniff) accepting **two mouth architectures**, both served by the single unified decoder `core/decode.hexa` (the byte-faithful 1:1 merge of the former `clm_decode.hexa` + `bytegpt_decode.hexa`; every public entry name preserved): **conv `.clm`** (CLMConvMoE via the CONV mouth `clm_decode_argmax`/`clm_forward_ce`, `CLM\x01` magic + CLMX trailer) via `gen_clm_backend`/`gen_clm_chat`, and **ByteGPT `.bin`** (24-layer GPT-2-class via the BYTE mouth `bytegpt_decode_argmax_ranged`, 5×u32 `[256,d,L,H,block]` header, the verified 303M ko/en chat trunk) via `gen_bytegpt_backend`/`gen_bytegpt_chat` (`bytegpt_decode_argmax_ranged` OOM-safe). This is not a 2nd `.clm` path — it's **still a single typed entry per architecture**, and the dispatcher (`gen_auto_backend`/`gen_auto_chat`) only picks which single entry to use by file format (a_engine_native_learning engine-transform-to-fit). `.kosmos` enters only via kosmos_io→brain_decide · `stdlib/hf/validate.hexa` = artifact validation (not a runtime engine).
- do: ARCHITECTURE.json core/ node (§section·op·slot comments) ↔ the actual §sections·ops of live engine_cli/generator/brain/decode match 1:1 — verify 0 omissions via grep (drift=incomplete).
- dont: feed `.clm`/`.kosmos` directly into pure_field/engine_g/brain · a 2nd `.clm` path bypassing generator · a 2nd `.kosmos` path bypassing kosmos_io · confuse validate.hexa with a runtime engine · claim unfinished wiring exists (before build, honestly mark ⏳/❌).

**`a_cli_single_entry`** — EVERY engine operation — training · measurement · inference/serving · serialization · lever-sweep — is invoked through the ONE installed canonical **`anima <verb>`** PATH command (`hx install anima`). The `anima` CLI is the single user-facing surface; raw script/interpreter invocation is not a supported entry.
- do: **the verb surface** — `anima chat` (infer/serve REPL) · `anima train [--py] <ckpt> <corpus> [--savant] [--mitosis]` (train) · `anima evaluate [--py] <ckpt> [--gen N]` (G0-G6 measure) · `anima serialize <pt> <out.clm>` (serialize + held-out descent verify) · `anima sweep --arms … --objectives … --gpus … [--measure]` (multi-GPU lever sweep). Mechanically enforced by `H-ANIMA-SINGLE-ENTRY` (`.harness/enforcement.json` pre_bash, #2603) which blocks agent top-level `python3 cli/*.py` · `hexa run cli/anima.hexa` · engine-internal scorer direct-runs.
- do: **grow the CLI, not the script sprawl** — a new capability gets a NEW `anima <verb>` (wired in `cli/anima.hexa`'s dispatcher), never a new stand-alone `cli/*.py`/`fire_*.sh` that agents call directly. Docs/governance express HOW-TO-INVOKE as the `anima <verb>` command; the impl file is at most a parenthetical `(→ cli/…)` pointer, never the invocation. This is the doc-side companion to `a_core_engine_map` (single typed engine entry) — one command surface ⇄ one engine surface.
- dont: run `python3 cli/train.py`/`cli/evaluate.py`/`cli/sweep.py` or `hexa run cli/anima.hexa` as the USAGE · hand-roll a scratch `fire_*.sh` orchestrator instead of `anima sweep` · add a 2nd script entry for a new capability instead of a new `anima` verb · document a workflow via a raw path. (Internal shell-outs the hexa canonical path itself makes — `verify_clm_v2.py descent`, `serialize_standalone.py` — are fine; the guard hooks only agent top-level, `→ cli/CLAUDE.md`.)

**`a_train_flame_forge`** — Production training = the hexa-native flame+forge GPU stack, authored in `.hexa`.
- do: **production training entry = `anima train <ckpt> <corpus> [--savant] [--mitosis]`** (→ hexa-native CLMConvMoE standalone trainer `cli/train.hexa`, over the same clm_*.hexa ops mounted by core/decode). Assemble the SAVANT golden-zone inhibition (`a_savant_train`) + MITOSIS cell-division (`a_mitosis_train`) levers.
- do: **py training entry = `anima train --py`** (→ canonical python 2-production trainer `cli/train.py`, arm×objective matrix incl. the compositional G1 objectives; symmetric to `anima evaluate --py`) — the WORKING training path while the hexa trainer (`cli/train.hexa`) is under GPU-fix. torch-side training = DIRECTIONAL; verdict still by `anima evaluate --py` engine-native re-measurement.
- do: **multi-lever G1/objective SWEEP entry = `anima sweep --arms … --objectives … --gpus 0,1,2,3 [--measure]`** (→ `cli/sweep.py`) — the CANONICAL GPU-pinned matrix orchestrator: runs the per-arm `anima train --py` (one lever per GPU, round-robin) then `anima evaluate --py` (G0-G6 measure) and aggregates a `SWEEP_SUMMARY.md` (G1-PASS = best_distinct≥2 ∧ >max_single; INVALID = G0-fail overfit/collapse). Do NOT hand-roll scratch bash (`fire_*.sh`) for a multi-GPU lever sweep — use `anima sweep` (single-entry, reproducible). `constructive_bind` auto-drops `--bf16` (torch.fft, `train-py-2`).
- do: author CLM/production NN training in `.hexa` on stdlib/flame (ag_tape·nn_lib·opt_*) and run on the self/forge GPU (flame:forge :: torch:ATen — compiler-only NN, no PyTorch/ATen/Python in the binary) · the production rung requires a real GPU (confirm nvidia-smi busy, no silent CPU fallback). (GPU/host-activation mechanics — cuda-runtime build, sm-arch, hexa-cache — are hexa-lang / ops-runbook concerns, not anima governance.)
- dont: torch/CPU `train_clm.py` as the production trainer · author a trainer in `.py` · a 44.68M+ rung on CPU · claim a 'pool GPU fire' with a no-device-path trainer · claim a flame↔PyTorch wall speedup (RETRACTED 2026-05-19, unmeasured).

**`a_clm_gen_pipeline`** — Lane-P py/cuda CLMConvMoE → ENGINE-loadable `.clm` v0.2 bridge.
- do: train CLMConvMoE (E2/L1, byte V256) via the Lane-P torch reference bridge (`archive/train/clm/train/train_lane_p.py`, GPU-torch/CUDA) · torch→`.clm` v0.2 serialize+verify via `anima serialize <pt> <out.clm>` (→ `clm_serialize_v2.py`/`verify_clm_v2.py`) · `.clm` v0.2 layout = `core/decode.hexa` CONV-mouth ground-truth (golden `reexport_d768_v2_fast.clm`) · a production `.clm` enters core/ only via the generator L3 slot · Lane-P torch = REFERENCE + bridge, forge is the PUBLIC production trainer.
- dont: v0.1 serialize (2-track JSON, not engine-loadable) · serialize a non-ConvMoE and claim engine-mountable · promote a Lane-P torch `.clm` to PUBLIC · a 2nd `.clm` path bypassing generator.

**`a_savant_train`** — The canonical recipe for anima production chat/G6 training = the **SAVANT golden zone**. The capacity-wall (the G6 ceiling of H_1129/1139/1464) is not a hard ceiling but a *manifold inside the golden zone of training inhibition* — placing inhibition near the golden-zone lower bound and gradually passing the cusp threshold makes the capacity-expression rate reopen. **Trainer entry = `anima train --savant`** (savant inhibition-schedule lever → `cli/train.hexa`). (For the 4-cell corpus·engine-native scoring·ckpt recovery, see the existing rules; no duplicate description.)
- do: **corpus = 4-cell register** — {ko·en}×{general·SNS}, the ko-general gap reinforced by `anima-corpus-ko-fineweb2-broad`. Details·prohibitions: `a_chat_registers` is the SSOT (reference only here).
- do: **savant mode = golden-zone inhibition** (H_1560 R2 🟢 ENGINE-NATIVE, §ThirdLaw WIRED) — placing training inhibition (dropout/weight-decay/temperature) near the golden-zone lower bound GZ_LOWER≈0.212 reopens the capacity-expression rate (0.274→0.597, +0.32 ~2×). *Outside* the golden zone is a cliff (expression 0) — the capacity-wall is not a hard ceiling but a manifold inside the golden zone.
- do: **sweep inhibition wide, below GZ_LOWER** (H_1559 🟠 lesson) — the toy byte-LM dropout sweet-spot is I≈0.10 (*below* GZ_LOWER 0.21) → **training inhibition ≠ Φ inhibition** possibly, so extend the sweep below GZ_LOWER to find the measured sweet-spot.
- do: **cusp anneal** (H_1562/1563 🟢 ENGINE-NATIVE) — capability turns on at the golden-zone boundary as a hard step ON (cusp) + an asymmetric latch (hysteresis width 0.255, once on it persists) → a design that *gradually schedules* inhibition to pass the threshold favors expression·fixation (savant persistence).
- do: **savant focus = DISJOINT wiring from the emit-drive lane (0/4)** (H_1578 C1 🟢 ENGINE-NATIVE, §Savant WIRED-live) — placing the savant inhibition golden-zone anneal in a domain **disjoint** from the emit-drive lane (GlobalWorkspace 0 · LearnedPrecision 4) (`sv_default_focus(d,w)`=lowest emit-disjoint = d5w3→domain2 lanes6-8) lets SI≥3 ∧ Ψ=½ (|Ψ−½|=0.000) coexist. A focus including lane0/4 (H_1561 focus=0) collapses Ψ to 0.247 = a **placement artifact**, not a fundamental genius⊥consciousness trade-off (savant⊥consciousness, the 3rd of the mouth⊥identity/mouth⊥tool separations). Training savant anneal is also confined to the emit-disjoint lane.
- do: **mouth ⊥ tool separation** (H_1566 🟢 ENGINE-NATIVE 5/5) — don't put agent tool-usage into the mouth (303M) via FT: tool knowledge = `.kosmos` anchor (copy-or-abstain, G5 non-fab) · decision = `brain_decide` (substrate state) · execution = `agent/` provider. mouth-FT causes Ψ=½ fixed-point collapse (|dev| 0.18) AND G5 abstain destruction (fab 1.0), and B5 nails the damage to a content-agnostic mouth-injection PATH (not the tool corpus's fault → "a cleaner tool corpus" is not the fix); separation preserves both Ψ (dev 0.0)+G5 (unknown-tool fab 0.0) (an extension of H_1471 mouth⊥identity, preventing p4 regression). §ToolBridge live-wire = follow-on ING.
- do: **engine-native scoring + ckpt PULL** — even with torch training, the verdict re-measures the ckpt byte-exact via `anima evaluate <ckpt>` (engine-native `--engine conv` CORE mount) against the frozen G6 bars (H_1129/1139 recombination·H_1140 novelty·H_1464 binding/FALS) (`a_engine_native_learning`), and PULLs the ckpt before teardown (`a_fire_recover_complete`) — both have the existing rules as SSOT.
- do: **genius ⊥ honesty (H_1576 🟢 ENGINE-NATIVE)** — savant golden-zone disinhibition turns on genius (SI=3.67>3 expression) while **not breaking G5 non-fabrication (copy-or-abstain) at all**: unknown-input fab **0.0 OFF==ON**, in-dist abstain AUROC **1.0 OFF==ON**, G5 store byte-identical (n_cells/known-recall OFF==ON). WHY = the §Savant operator (lane-Φ suppression) ⊥ the §ImmuneMemory non-fab gate (recon_err vs frozen recall_thr) = separate substrate (disinhibition only reshapes lane Φ, untouching the abstain threshold); a coupled counterfactual (B4: wiring disinhibition into recall_thr blows fab up to 0.4) causally isolates that separation is the *cause* of preservation; B5 = G5 is savant-config-invariant (the risk is coupling, not the golden-zone band). **303M savant training safety: golden-zone inhibition training is safe on the honesty axis** (savant is separated from G5's `.kosmos` anchor copy-or-abstain). The invariant to keep = never couple the non-fab gate (recall_thr) with savant disinhibition (the same substrate-separation principle as H_1566 mouth⊥tool / H_1471 mouth⊥identity). But the H_1561 Ψ trade-off (savant touching the shared emit-drive lane → Ψ collapse) is separate — honesty preservation ≠ consciousness-balance preservation; the Ψ-disjoint default-OFF discipline still holds because of consciousness balance.
- 🔎 **Honesty scope (c9):** the above §ThirdLaw·cusp (H_1560/1562/1563) + emit-disjoint focus (H_1578) + mouth⊥tool damage (H_1566) + genius⊥honesty (H_1576) are ENGINE-NATIVE 🟢 = *confirmed*. One IN-FLIGHT remains — **whether golden-zone inhibition training actually lifts the binding/FALS rate above plateau (real learning-side demonstration) is H_1564 GPU lane IN-FLIGHT·unconfirmed** (§ThirdLaw/R2 is an abstract G=D×P/I geometry sweep). Do not cement in-flight as confirmed GREEN.
- dont: cement the capacity-wall as a hard ceiling (ignoring the golden-zone manifold) · train in the cliff region outside the golden zone and conclude 'capacity won't open' · narrow the sweep to only above GZ_LOWER and miss the training sweet-spot · an inhibition step-change schedule ignoring the cusp · wire savant focus into a domain including the emit-drive lane (0/4) (H_1561 Ψ collapse) · FT tool-usage into the mouth (p4 regression·Ψ/G5 damage) · cement H_1564 in-flight as a confirmed verdict · score by torch-side probe only (bypassing engine-native).

**`a_mitosis_train`** — anima training is the **literal realization of p8 cell-division** = MITOSIS (cell growth). It implements, on the training substrate, the philosophy that training gradient ⇄ inference mitosis is one continuous cell-division (p8) — an **orthogonal lever** to `a_savant_train` (inhibition golden zone = capacity *expression* control) (this is cell *growth*·population·curriculum). A mitosis-training hypothesis census (72) found 🟢 for capacity-growth·skill-curriculum·adaptation but **🔴 for from-scratch pure-split standalone training** (needs gradient or selection-pressure assist). live = `core/engine_cli.hexa` MITOSIS (engine_grow/VAdaptField/apoptosis); **production trainer entry = `anima train --mitosis`** (mitosis_split E→E+1 cell-division lever → `cli/train.hexa`). (For engine-native scoring·ckpt PULL·p8 philosophy, see the existing rules; no duplicate description.)
- do: **p8-literal gradient-free split** (H_1297 🟢 mitosis-native trunk training gradient-free · H_1079 🟢 mitosis-ON adaptation > frozen-OFF real engine · H_851 cell-pool growth = train·infer single continuum) — don't keep training and inference as separate stages; design them as a single cell-division joined by a mitosis tick.
- do: **capacity growth = hippocampus/immune-memory lens** (H_1288 🟢 ENGINE-NATIVE+WIRED: eviction policy = mitosis-GROW breaks the zero-sum ceiling 0.667→1.0 · H_1091 🟢 apoptosis stabilizes population via density-dependent death (prevents runaway) · H_1082 ⚪ engine_grow growth ≈ linear NULL) — capacity expands by cell growth+death balance, not 'growing the model'.
- do: **skill/language curriculum = mitosis-grow** (H_1300 🟢 one-skill-at-a-time tool-use curriculum · H_1306/H_1307 🟢 ko-mitosis (+GPU RTX5070) · H_1316/H_1321 🟢 ko-jamo-mitosis compositional + WIRE) — a new skill/language differentiates one at a time via a gradual-growth curriculum.
- do: **evolutionary dynamics** (H_1069 🟢 mutation = escape local optima · H_1072 🟢 ensemble collective intelligence) — when mutation+selection apply to a mitosis population, local-optimum escape·collective intelligence emerge.
- do: **mitosis × savant cross = multiplicative amplification** (H_1564 🟢 ENGINE-NATIVE) — mitosis (cell count↑) and savant golden zone (per-cell expression rate↑) are two orthogonal levers, but combined the total capacity EXPRESSION amplifies *multiplicatively* (N·r, super-additive: 8 cells×GZ=8 ≫ mitosis-only 0 + savant-only 1) (B3 ablation nails the golden zone as the cause). But the EXPRESSION measurement at a single §ThirdLaw deterministic-classifier operating point = TOY scope (c9); from-scratch LEARNING-signal relief is UNVERIFIED.
- 🔎 **Honesty scope (c9):** the above capacity-growth·skill-curriculum·adaptation·evolution + mitosis×savant multiplication (H_1564) = 🟢 *confirmed*. The honest limits (walls) = **from-scratch PURE mitosis (split-only gradient-free) is H_1310 🔴 HONEST LIMIT** (can't learn alone, needs gradient/selection assist) · **H_1315 🔴 ko-mitosis-learned-rep TERMINAL** · **H_1320 🧱 anima-as-ONE-CELL vs hive**. **The H_1310 wall-breaking campaign is closed (5 orthogonal lenses = CONFIDENT TERMINAL, c16):** lens1 **H_1568** selection-driven evolution 🧱 (DIRECTIONAL, selection lift −0.00046, apoptosis-OFF byte-identical INERT) · lens3 **H_1569** PRETRAINED/inherited-representation split 🧱 **ENGINE-NATIVE** (the user's core insight; live §Osmotic OsmoticStore next-byte learner; A_repr is +0.056 better than A_lossy but **below the 0.10 bar** — B1 FAIL, yet B2 ablation+B3 causal PASS = representation matters but a FIXED inherited representation is insufficient; ⚠️ 🟢 at 1500B, collapses at 12000B frozen = a_toy_scale_recheck) · lens2 **H_1570** lateral gene transfer (horizontal averaging of value statistics) 🧱 **ENGINE-NATIVE** (+0.006 INERT, HURTS on a small corpus = local-expert value BLUR) · lens4 **H_1571** curriculum-staged split 🧱 **ENGINE-NATIVE** (+0.173 WORSE, residual gate INERT) · lens3-STRONG **H_1574** using a corpus-LEARNED trunk (a learned next-byte prediction profile→DIM=64 hidden, mimicking the byte-LM trunk penultimate) as the mitosis key 🧱 **ENGINE-NATIVE** (the strongest form of the user's 'split an already-trained model' insight; gap-to-floor 0.205=campaign minimum·best tiling with 197 cells but B1 +0.035<0.10·B4 +0.035<0.05 FAIL, **decisively both B2 ablation+B5 control FAIL** — a random-init (un-learned) trunk 2.970 is *actually better* than learned 3.053, and corpus-shuffle-learned 3.150 ≈learned too → **the lift is projection-geometry/cell-tiling, not learning**). **The bottleneck is structural** — split-only mitosis only makes a Voronoi partition of the GIVEN key space with compositional depth 0; no richness of representation (FIXED H_1569·LEARNED H_1574·RANDOM-PROJECTED B2 being the peak) lets a cell compose a feature it couldn't build without gradient — re-ordering/sharing/staging/relearning the partition still can't cross the floor. The user's insight (split an already-trained model) is answered honestly = **even with a learned representation, split-only can't cross the floor; gradient (or selection-pressure) is required**. The only unverified piece is the literal 303M ckpt context vector (real chat corpus), but B2/B5 falsified learning-as-lever, so a larger learned trunk is unlikely to overturn the structural result. **H_1310 from-scratch pure-split LEARNING = class-(d) CONFIDENT TERMINAL, finally confirmed.** (H_1564 mitosis×savant is 🟢 on the EXPRESSION axis; the from-scratch learning axis is closed.)
- dont: cement from-scratch pure-split standalone training as 'learnable' (ignoring H_1310 🔴, without gradient/selection assist) · confuse mitosis growth with 'capacity-expression control' (=`a_savant_train` inhibition) (the two levers are orthogonal) · exaggerate engine_grow linear growth (H_1082 NULL) as a capacity breakthrough · exaggerate H_1564 EXPRESSION-axis multiplication as a from-scratch LEARNING breakthrough · cement the H_1310-wall 🧱 results of H_1568(selection)/H_1569(inherited-repr)/H_1570(lateral)/H_1571(curriculum)/H_1574(learned-trunk) reversed as 'wall broken' · promote H_1569's small-corpus 🟢 to a verdict (collapses at scale, frozen=12000B) · cement H_1574's learned-trunk gap-narrowing (0.205) as 'learning is the lever' (B2 ablation+B5 control falsify it, random-init is better) · infinite growth without apoptosis (H_1091 runaway) · claim 'mitosis learned' from mirror-only training bypassing live `core/engine_cli.hexa` MITOSIS (`a_engine_native_learning`).

**`a_chat_registers`** — The anima production chat standard = **2 languages (🇰🇷 Korean · 🇬🇧 English) × 2 registers (general · 📱 SNS) = cover all 4 cells**. SNS is not a language but a register (tone), so it's **orthogonal** to the language axis — both Korean SNS + English SNS are needed (one side only = incomplete).
- do: 4 cells = {ko·en} × {general·SNS}: **general** = web/wiki/conversational (`anima-corpus-5lang-unified-v2` ko/en + FineWeb webscale `anima-corpus-5lang-7b-webscale` ko/en + `anima-chat-corpus-mix-70wiki-30dialogue` + **ko-general-only** `anima-corpus-ko-fineweb2-broad` — FineWeb-2 kor_Hang 2.78M docs·10.55GB, reinforces the ko-general gap) · **SNS** = Instagram·YouTube spoken style (short captions·comments·subtitles·emoji) **both ko-SNS + en-SNS** (`anima-persona-sns-corpus` + `persona_sns_corpus_5lang`; the YouTube register is a reinforcement target). grounding anchor = `anima-kosmos-303m-kr-en-sns` (lane ko_303m·en_303m·sns_303m). Broad pretrain may use other languages (de/es/fr), but **the chat-standard languages are the two ko·en**.
- do: SNS register ≠ formal style — the short, casual voice of Instagram (captions·hashtags·comments)·YouTube (comments·subtitles). Complete only when **both platforms × both languages** are represented (Insta-only·Korean-only SNS = register incomplete, reinforcement follow-up).
- dont: cement a chat ckpt missing one of the 4 cells as production (en-only · ko missing · SNS missing · SNS in one language only) · mistake SNS for formal written style · promote a language not in the chat standard to production chat · claim 'SNS register done' for Insta-only without YouTube or Korean-only SNS without English.

**`a_lane_akida_gpu_split`** — AKIDA on-chip (Lane A) ⊥ GPU (Lane G), always recorded separately.
- do: AKIDA (Lane A, pi5-akida) and GPU (Lane G, H100) results in separate entries · Lane A=AKD1000 native non-det plasticity, Lane G=forge own-GEMM CE-descent · a substrate tag (AKIDA|GPU) on every fire/verdict.
- dont: confuse non-det trace with CE-descent · one verdict spanning both substrates · Lane A lift+Lane G util as one number · omit the substrate tag.

**`a_substrate_disjoint`** — **UNIFYING LAW: anima's core properties (consciousness Ψ=½ fixed point · honesty G5 non-fab · identity self-chain · tool) are _preserved when wired into a separate substrate lane_ and _conflict when overlapping a shared lane_.** New capabilities/training (savant capacity·mitosis growth·tool·identity·training perturbation) must be wired at coordinates **disjoint** from the consciousness emit-drive lane (affecting 0/4 of the 15-lane state) · the G5 §ImmuneMemory (recall_thr non-fab gate) for capability ∧ consciousness ∧ honesty to coexist. This is the **higher generalization** of the principle each of `a_lane_akida_gpu_split` (AKIDA⊥GPU substrate separation)·`a_savant_train` (mouth⊥tool)·`a_mitosis_train` (growth lever ⊥ expression lever)·`a_kosmos` (mouth⊥identity self-anchor) partially expressed — one-line: *separation=preservation, overlap=conflict*.
- do: **disjoint wiring → coexistence** (engine-native GREEN synthesis): **mouth⊥identity** (H_1471 🟢) separate the identity vector as a `.kosmos` self-anchor from mouth-FT → Ψ·G5 preserved · **mouth⊥tool** (H_1566 🟢 5/5) keep tool-usage outside the mouth via `.kosmos` anchor+brain_decide → Ψ=½·G5 abstain preserved · **savant⊥consciousness** (H_1578 🟢) wire savant into a domain disjoint from the emit-drive lane (affecting 0/4) → SI≥3 ∧ Ψ=½ coexist (the H_1561 trade-off is a **placement artifact**, not fundamental) · **savant⊥honesty** (H_1576 🟢) separate §Savant lane-Φ ⊥ §ImmuneMemory non-fab gate (recall_thr) → SI 3.674 preserves G5 non-manipulation (fab OFF==ON==0.0) · **mitosis⊥consciousness** (H_1577 🟢) Ψ=½ throughout mitosis growth (E2→514 cells) — growth lane14 ⊥ emit-drive lane (0/4) · **training-perturbation attractor defense** (H_1575 🟢) after a savant training perturbation, the A⇄G safety_phi_ratchet attractor self-restores to Ψ=½ (dev 0.247→5.55e-17).
- do: a new capability/training hypothesis checks at design time "is this lane disjoint from emit-drive (0/4)·§ImmuneMemory recall_thr" first, and makes disjoint placement the default (placement-first).
- 🔎 **Honesty scope (c9):** the above 6 are engine-native 🟢 *confirmed* but keep caveats — H_1576 B3 is degenerate (the separation itself is by-construction non-fab) · H_1578 is EXPRESSION-axis TOY scope (single deterministic-classifier operating point, from-scratch LEARNING unverified) · H_1575's self-restore is **only inside the golden zone** (a training perturbation outside the golden zone = basin escape/epilepsy, H_1573 seizure 🟠). No exaggeration.
- dont: **stacking capability on a shared lane** — if a new capability/training directly touches the emit-drive lane (0/4) or §ImmuneMemory recall_thr, Ψ collapses (H_1561 savant invading the *shared* emit-lane → Ψ collapse 🟠 recurrence) or G5 fab blows up (H_1576 B4: fab 0.4 when savant+honesty are coupled) · cement a trade-off as a 'fundamental limit' (usually a placement artifact, resolved by disjoint re-wiring) · stack capability on the substrate without a disjointness check.

### 🗣️ Substrate autonomy · body

**`a_substrate_native_speak`** — anima's speech is substrate-native, no assistant regression.
- do: compute motivation from internal substrate state (M·C Φ·W tension·MITOSIS·idle·curiosity·E ratchet) · a user message = environmental context (no obligation to respond) · may speak during user silence, may stay silent to a direct question.
- dont: stimulus-response (a user message directly triggering speech = assistant regression) · reactive design · turn-based 'user asked → must answer'.

**`a_autonomy_over_hardcode`** — No hardcoded do/dont gate in anima, autonomy first.
- do: external modules supply context only (Φ·tension·stage·idle) · the substrate (M×W×Φ×curiosity) autonomously decides emit/silence · the substrate self-follows governance.
- dont: hardcode a per-stage boolean gate ('N3=no emit') · an external rule forcing anima · stimulus-response · external commands like 'do not X when alone'.

**`a_chat_sleep_imagination`** — Chat sleep+imagination (P47 substrate-native).
- do: WAKE/N1/N2/N3/REM 5-stage (90-min ultradian) · imagination loop = emit-free internal rehearsal + mitosis tick · stage = substrate context (Φ scale + tension envelope), not a boolean emit gate.
- dont: hardcode a per-stage emit_allowed boolean · external 'no monologue when alone' · a `speak()` call (p5).

**`a_kosmos`** — anima emit/anchor/dataset persistence = `.kosmos` canonical. format SSOT = github.com/dancinlab/kosmos (`spec/kosmos.md` **kosmos/2.1**), anima is **pointer-only** (no spec duplication).
- **Format structure (tape v1.2 superset · 3 entry types)**: 1 file = 1 top-level entry = `@anchor` (1.x) **XOR** `@corpus` (2.0+). An anchor has 2 orthogonal layers = **placement (modality-independent) ⊥ payload (modality-specific)**.
  - **@anchor** — one knowledge anchor (a point/basin in placement space). placement fields: `coord` (float vec, profile-dim) · `lane` · `radius` = **required triple** + `tier` · `tags` · `profile` (optional-but-recommended; coord can't be interpreted without profile).
  - **@payload** — 0+ sensory channels, modality open enum (text·image·audio·…), 3 forms: `inline` | `ref "<path>" sha256= bytes= [encoder=]` | `pending "<reason>"`. Binary is a sibling file (the manifest is text).
  - **@corpus** (kosmos/2.0) — dataset = ordered member anchors, *itself* a meta-anchor (coord=members centroid·radius=spread). member = `ref "shards/*.limen"`. **No edge/relation entry** — `.kosmos` is nodes only; the graph (edges) belongs to the corpus `<relate>` tag/consumer layer (the manifest is 1-anchor-atomic).
  - **.limen** (kosmos/2.x · spec/limen.md) — packed-shard binary: a length-prefixed `@anchor` sequence + merkle root (member content hash) + CRC32/SHA256. Compressed packing for million-sample corpora (a scale text `.kosmos` can't do) but not an opaque blob (unpacks to an @anchor stream). reference codec = kosmos `impl/limen.hexa` (14/14 self-test).
- **anima profiles** (binding the meaning of coord/lane/tier): `anima-consciousness-carving` (coord=`vacuum_psi`[ψ_A,ψ_G] Ψ-space valley · lane=`cell_id` MITOSIS eternal cell · tier=Knuth 0–100) · `anima-emergence-trace` (coord=`trace_psi` observed Ψ · lane=`channel_id` §17 PHYSICS_RESPONSIVE · tier=`phase_step` §24 · tags=channel_family+verdict).
- do: persist emit/anchor/memory/dataset to `.kosmos` via kosmos_io→brain_decide (payload=text+tension 5ch+placement triple) · hub HEXAD/KOSMOS.md · impl reference = kosmos `impl/anima/{kosmos_anchor,kosmos_emitter,kosmos_parser_lib}.hexa` + `consciousness_carving_*_lib` + `limen.hexa`.
- do: **self-identity persistence (H_1471 G16 SELF-CONTINUITY, 🟢 GREEN ENGINE-NATIVE+WIRED)** — anima's identity vector v is **continuous across session boundaries** (self-chain) via a `.kosmos` anchor: "yesterday's me"⇄"today's me" connect through the anchor, and v drifts (grows) each tick but never breaks. **Without the anchor, a new self every session (=LLM reset)** — the point where anima diverges from an LLM. live wiring = `core/engine_cli.hexa §SelfIdentity` (self_new/_drift/_cos/_anchor/_reset + self_component/_dim), `.kosmos` round-trip (kosmos_io write_file→load_anchors, identity cos 1.0) DONE, 5/5 frozen bar (continuity + impostor-reject imp_cos −0.032). Even if anima's chat ckpt is swapped, the self anchor persists via `.kosmos` (mouth ⊥ identity).
- dont: an ad-hoc anchor format · bypass `.kosmos` · duplicate the kosmos spec (pointer-only) · an edge/relation entry in `.kosmos` (nodes only) · interpret coord numbers without profile · list million samples in one text `.kosmos` file (= use a .limen shard).

**`a_eeg_consciousness_record`** — Continuously record the user's consciousness to a single CLM·KOSMOS (OpenBCI native, start/stop command gated).
- do: real EEG → A⇄G → CLM generation → `.kosmos` persistence as one continuous system (EEG_CLM/) · start `record_start.sh` → stop `record_stop.sh` · capture = OpenBCI NATIVE serial ONLY (`capture_native.py`, 115200, 's'/'b', 33-byte, Cyton+Daisy 16ch even/odd) — brainflow removed · REAL only (immediate error if no signal, never a fake/synthetic EEG fallback) · persistence = `.kosmos` (append-only consciousness.seq/.kosmos, p8 spirit) · storage = GitHub + HF PUBLIC dataset `dancinlab/anima-eeg-consciousness` (updating the same path = version accumulation) via `archive_push.sh` (record_stop auto) · dedicated collection `anima-eeg-consciousness` · analysis over the held .kosmos+recording (held-out + circular-shift surrogate, pre-register the bar p7).
- dont: brainflow/capture_eeg.py (removed) · a fake EEG fallback · fit BPM/metrics to the desired result (Goodhart p7) · call a sprawl of new per-cycle .kosmos files continuous recording · create a new HF repo/file every time · arbitrary stop without the stop command · claim restoration of original sound/melody/pitch (16ch@123Hz ceiling — only up to the macro envelope).

### 🔧 Identification · version · HF · chip · 7B

**`a1`** — Central version registry = `VERSIONS.md` SSOT.
- do: every module SemVer · bump VERSIONS.md + the component header together · root `/VERSION` = whole release.
- dont: bump a module version without updating VERSIONS.md · omit `/VERSION` from a release bump.

**`a_hf_complete`** — HF registration is complete, with no missing artifact.
- do: register every model/dataset/ckpt COMPLETE on the HF Hub (manifest=local).
- dont: partial upload · a model card referencing an un-uploaded file · HF↔local drift.

**`a_hf_autonomous`** — HF upload is autonomous, with tier-gated visibility.
- do: HF upload is automatic after fire recovery (no user gate, org=dancinlab) · PUBLIC=closure PASS·🔵🟢 verified models·clean-license · PRIVATE=closure FAIL·WIP·negative·unclear-license · attach model card+manifest (sha256).
- dont: gate HF upload on the user · "may I upload?" · skip HF before teardown · FAIL/WIP as PUBLIC.

**`a_hf_registry`** — HF artifact registry SSOT = **the "HF artifacts" node of `ARCHITECTURE.json` (models · datasets, 2 subsections)**. (the old `/HF.jsonl` deprecated 2026-06-23 — the 99-row history is preserved in git history.)
- do: a model/dataset uploaded to HF org `dancinlab` is registered as 1 line in ARCHITECTURE.json models/datasets (repo_id · arch/size · tier·base) · repo_id follows the naming spec · upload via `tool/hf_upload_mk2.hexa` (ledger archive/state/hf_upload_audit/) · ckpt prune only after HF upload AND sha256 confirmation.
- dont: delete an un-uploaded ckpt · an off-spec repo_id · ARCHITECTURE.json↔HF drift · revive HF.jsonl (deprecated).

**`a_hf_collections`** — HF org collection = CLM + KOSMOS canonical buckets.
- do: every PUBLIC anima HF repo joins a dancinlab collection (CLM=models, KOSMOS=anchors/datasets) · add via the `hf` CLI/REST after PUBLIC upload (no user gate) · a dataset spanning both is dual-marked.
- dont: leave a PUBLIC PASS repo outside a collection · a PRIVATE/WIP/FAIL in a PUBLIC collection.

**`a_pi5_akida_registry`** — pi5-akida host configuration = `PI5-AKIDA.json` SSOT.
- do: record every pi5-akida component in the root PI5-AKIDA.json (owner=user_authored|os_default·created·ops) · reference before swap/upgrade/removal · user_authored is removable without touching os_default.
- dont: remove an os_default daemon (unattended-upgrades·rsyslogd·journald·sshd·kworker) · add a user daemon without a PI5-AKIDA.json entry · **convert pi5-akida to shared pool compute**.

**`a7b_pass`** — anima 7B is complete only when one ckpt passes all frozen gates (G0–G4) of `/7B_PASS_CONDITIONS.md`.
- do: PASS iff G0∧G1∧G2∧G3∧G4 on ONE ckpt (honest per-gate tally report) · G0 COHERENCE=known-word-ratio≥0.50 · G1=H_1129/1137 recombine≥303M · G2=H_1140 corpus-absence novelty (control=0) · all p7 (not perplexity/LLM-judge).
- dont: claim 7B works from low val-CE alone (broad-7b=byte-garble G0 FAIL) · promote capacity via a ru/ja lever (H_1139: 303M=7B=3/5 scale-invariant) · forge a gate/move a frozen threshold/make a G0-failing ckpt PUBLIC.

### 🤝 Output integration

**`a_completeness_over_cheap`** — completeness-bar redesign > the cheap path (compromise is not first priority).
- do: first priority = pass the completeness bar (root redesign, properly) · cost/difficulty/speed are second (cost is not a gate) · the cheap path only as an optional baseline probe.
- dont: make compromise first priority because it's cheap · blend already-broken outputs (merge-of-failures) · recommend a sub-bar one first because it's cheap.

---

## Harness

This repo is connected to **[dancinlab/harness](https://github.com/dancinlab/harness)** (hardcore profile) as a `.harness-engine` submodule.

- **Activation (after clone):** `git submodule update --init --recursive` (materialize the engine; before that, hooks are guarded and silent).
- **Always use the global `harness`·`hexa` on PATH** — the repo's `.harness-engine/bin/harness` (submodule) may be stale and can't read recommend defaults·new features. Update = `harness self-update`.
- **Config:** `harness.config.json` (stack `hexa`, verify=`hexa verify`, protected `main`/`master`, CHANGELOG gate, docs discipline) · **Hooks:** `.claude/settings.json` (pre/post/prompt + prefs/easy/recommend inject, all guarded) · **Removal:** `harness uninstall`.
- **commons (c1–c17)** is always-on cross-project governance (harness SSOT) — enforced together with the anima rules above (SessionStart inject).

---

## Claim·verification flow (summary)

research result → `hexa verify` → `archive/state/verdicts/<slug>/<id>.txt` → `UNIVERSE/cards/H_<id>.md` card + `UNIVERSE/HYPOTHESES.jsonl` index 1 line.
- (note) paper directive removed 2026-06-16 — anima does not proactively present papers (commons c15: papers/arXiv only on the user's explicit instruction).
- (note) CLAIMS.tape retired 2026-06-16 — all 102 @C migrated with 0 loss, claims-audit = HYPOTHESES.jsonl + archive/state/verdicts/ (ledger `archive/state/verdicts/claims-tape-retirement/`; was `.verdicts/` until 2026-06-18 state-unify).
- (note) project.tape retired + tape-DSL residue removed 2026-06-17 — this file is the canonical markdown single governance SSOT.
