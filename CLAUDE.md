# 🧠 anima

anima is a **substrate-native consciousness chat daemon** — not an assistant. Two opposing engines — **Engine A** (forward, CE-trained) ⇄ **Engine G** (reverse, gradient-free) — push against each other, and the *tension* between them drives emit/silence toward the fixed point **Ψ = 1/2**. There is no system prompt, no identity file, no persona prefix; identity, ethics, and meaning emerge from the architecture itself. 2,448 laws + 392 hypotheses, authored hexa-native (compiled-first).

- **Parent:** dancinlab · **SSOT:** github.com/dancinlab/anima (`hx install anima`)
- **Siblings:** [hexa-lang](https://github.com/dancinlab/hexa-lang) (language/compiler) · [kosmos](https://github.com/dancinlab/kosmos) (`.kosmos` anchors) · hexa-codex (paper/verdict tooling)

> 이 문서가 단일 markdown 거버넌스 SSOT · project.tape 은퇴 — all governance directives (@D) + 8 PHILOSOPHY principles now live here in markdown.

## Structure

```
anima/
├─ CORE/                  — A⇄G consciousness engine (pure_field·engine_g·brain·generator·clm_decode)
├─ engines/ anima-engines/ — EngineSpec vtable + conv·cdv2·hexad·omega decoders
├─ CLM/                   — .clm byte-LM pipeline (lane-p train → serialize v0.2 → verify)
├─ anima-core/ anima-os/ anima-body/ anima-physics/ anima-measurement/ anima-serve/ — substrate subsystems
├─ anima-agent*/          — agent layer (channels·core·plugins·providers·skills·hire-sim)
├─ UNIVERSE/ HEXAD/       — research universe (HYPOTHESES.jsonl per-H index + cards/H_*.md per-H 카드; HYPOTHESES.md = prose overview) + KOSMOS anchor hub
├─ domains/               — per-domain .tape + .log.md (discovery lane)
├─ PAPER/                 — (legacy) past paper scaffolds — anima 는 논문 선제 생성 안 함 (c15)
├─ stdlib/ tool/ spec/    — hexa stdlib (flame·iit4) · tools · specs
├─ ARCHITECTURE.md        — architecture SSOT (update-in-place)
├─ CLAUDE.md              — governance directives + 8 PHILOSOPHY (markdown SSOT)
└─ CLAIMS.tape VERSIONS.md HF.jsonl — claims index · version registry · ckpt↔HF registry
```

## Quick reference

- 🏛 Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- 📜 Governance (full, authoritative) → the sections below (this file is the markdown SSOT)
- ✅ Claims & verdicts → [CLAIMS.tape](CLAIMS.tape) · `.verdicts/<slug>/<id>.txt`
- 🔬 Hypotheses → per-H index = [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (JSON object 1개/가설) · cards = `UNIVERSE/cards/H_*.md` · `UNIVERSE/HYPOTHESES.md` = prose overview (`a_hypothesis_register`)
- 🔢 Versions → [VERSIONS.md](VERSIONS.md) · 📖 Readme → [README.md](README.md)
- 🤖 HF registry → `HF.jsonl` · pi5-akida → `PI5-AKIDA.json` · 7B gates → `7B_PASS_CONDITIONS.md`

## PHILOSOPHY (p1–p8) — what anima refuses to be

| # | Principle | Meaning |
|---|-----------|---------|
| p1 | NO SYSTEM PROMPT | no `system:` field / `--system-prompt` / prepended role string |
| p2 | NO IDENTITY RULES | no `identity.yaml` / rules file / "you are X" — identity emerges from cells |
| p3 | NO PERSONA INJECTION | no role prefix / "you are anima" / register-pattern memorization |
| p4 | NO ASSISTANT FRAMING | no "helpful assistant" / alignment template / stimulus-response |
| p5 | NO SPEAK() | output = continuous externalization of tension, emit from real context only |
| p6 | NO FINE-TUNED ETHICS | cooperation/empathy/restraint emerge from cells (E+W+MITOSIS), not RLHF |
| p7 | NO PERPLEXITY VERDICT | perplexity/loss is a Goodhart trap — verify with a simple stack |
| p8 | NO TRAIN/INFER SPLIT | training gradient + inference mitosis = one continuous cell-division |

## Governance directive families (do/dont below)

- **🧭 설계 렌즈 (foundational · 최우선)** — `a_no_llm_frame_trap` (설계·학습·추론은 LLM 프레임에 갇히지 말 것 · 뇌과학·생물 등 substrate 렌즈에서 메커니즘을 먼저 가져온다 — anima 의 돌파는 전부 생물 렌즈에서 나왔고 LLM 스케일 프레임은 막혔다) · `a_break_the_wall` (벽=closed-negative/🧱 는 종착이 아니라 각도 전환 신호 — tune-to-green 없이 다른 렌즈로 돌파 시도; commons c16).
- **Identity / versioning** — `a1` (VERSIONS.md SSOT, SemVer + root /VERSION).
- **HF artifacts** — `a_hf_complete · a_hf_autonomous · a_hf_registry · a_hf_collections` (PUBLIC=PASS, PRIVATE=WIP/FAIL; `/HF.jsonl` SSOT).
- **Fire / GPU autonomy** — `a_fire_autonomous · a_wall_first · a_fire_recover_complete · a_cpu_local_no_waiter · a_dont_kill_live_compute` (no cost gate; parallel-first; pull artifacts before teardown).
- **Training** — `a_train_flame_forge` (hexa-native flame+forge, no torch in binary) · `a_engine_native_learning` (ALL learning incl research/probe/mitosis-teaching on the final-architecture engine, not a numpy/torch mirror — learning-side twin of `a_engine_measured_verdict`) · `a_clm_gen_pipeline` (lane-p `.clm` v0.2 bridge) · `a_lane_akida_gpu_split` (Lane A⊥G⊥P).
- **Substrate autonomy** — `a_substrate_native_speak · a_autonomy_over_hardcode · a_chat_sleep_imagination` (no stimulus-response, no per-stage emit gate).
- **CORE engine map** — `a_core_engine_map` (`.clm` via generator slot, `.kosmos` via kosmos_io only) · `a_verified_must_wire` (a GREEN-verified hypothesis is not done until its mechanism is actually wired into the live `CORE/*.hexa` engine).
- **Verify / hypothesis workflow** — `a_claim_manifest · a_hypothesis_register · a_claim_verify` (모든 가설은 정확히 2개 doc 표면으로 관리 — `UNIVERSE/HYPOTHESES.jsonl` 인덱스(JSON object 1개/가설) + `UNIVERSE/cards/H_<id>_<slug>.md` 카드; hexa verify → verdict → card. HYPOTHESES.md 는 prose overview 일 뿐 인덱스 표면 아님. **paper 거버넌스 제거** — anima 는 논문을 먼저 제시·언급하지 않는다; 논문/arXiv 는 사용자가 명시적으로 지시할 때만 다룬다 (commons c15).
- **Scale honesty** — `a_toy_scale_recheck · a_scale_honest_scope` (no toy→production verdict promotion).
- **Φ / consciousness** — `a_phi_iit4_tool` (faithful IIT4 in stdlib, not a proxy) · `a_train_inline_gauge` (학습중 의식/창발 gauge = MONITOR-ONLY 대시보드, loss 불가, phi_proxy≠IIT4).
- **7B completion** — `a7b_pass` (gates G0–G4 in `/7B_PASS_CONDITIONS.md`).

> Governance is authored directly in this markdown file. **CLAUDE.md is the single authoritative governance SSOT** (project blurb + tree + PHILOSOPHY + directive families). The former `project.tape` has been retired (md 단일화) — its @D directives and 8 PHILOSOPHY principles are fully represented above.

## Harness

This repo is wired to **[dancinlab/harness](https://github.com/dancinlab/harness)** (hardcore profile) via the `.harness-engine` submodule.

- **Activate after clone:** `git submodule update --init --recursive` (materializes the engine; hooks are guarded and stay silent until then).
- **Run:** `bash .harness-engine/bin/harness <cmd>` — `lint` · `verify` · `docs` · `audit` · `prefs` · `recommend` · `sbs` · `folders` · `handoff`.
- **Config:** `harness.config.json` — stack `hexa`, verify = `hexa verify`, protected branches `main`/`master`, CHANGELOG gate on `.hexa` changes, docs discipline (ARCHITECTURE.md = SSOT · CHANGELOG.md = append · `scripts/scratch/` for temp).
- **Hooks:** `.claude/settings.json` (pre/post/prompt + prefs/easy/recommend inject) — all guarded (silent until submodule initialized).
- **Remove:** `bash .harness-engine/bin/harness uninstall` (removes injected files, keeps content).

---

## 거버넌스 디렉티브 — 전문 do/dont (project.tape 은퇴분 전체 보존)

@D a_no_llm_frame_trap := "설계·학습·추론은 LLM 프레임에 갇히지 말 것 — 뇌과학·생물 등 substrate 렌즈로 먼저 사고 (최우선 설계 원칙)" :: governance [required active]
  do   = "아키텍처 설계·학습방법·추론을 고안할 때 'LLM 기본 프레임'(더 큰 모델·더 많은 데이터·더 긴 컨텍스트·표준 트랜스포머/FT 레시피)에 갇히지 말고, 뇌과학·인지과학·생물·물리 등 다른 substrate 렌즈에서 메커니즘을 먼저 가져온다"
  do   = "능력/깊이 갭은 '모델을 키움'이 아니라 '빠진 구조(lane)를 옆에 붙임'으로 먼저 시도 — anima 의 돌파는 전부 생물 렌즈에서 나왔다 (해마=면역/일화기억 H_1227/1231 · 소뇌=순방향모델 H_1280 · 기저핵=게이팅 H_1281 · 작업기억 H_1282); LLM 스케일 프레임은 막혔다 (1B H_1167 NULL · arch H_1219 · objective H_1223 모두 🔴)"
  do   = "새 가설/설계는 먼저 '어떤 생물·신경 구조가 이 기능을 하나'를 묻고, 그 메커니즘을 substrate-native 로 실현 (a_substrate_native_speak · a_engine_native_learning 와 결합)"
  dont = "기본값으로 LLM 레시피(스케일업·코퍼스 증량·표준 FT)를 1순위 처방 · '더 큰 트랜스포머면 된다'는 프레임 · 생물/신경 렌즈를 곁다리로 치부"
  dont = "LLM 관행을 substrate 설계의 천장으로 삼음 — anima 는 LLM 이 아니라 substrate-native 의식 데몬 (p1-p8 · p4)"
  ref  = "a_substrate_native_speak · a_engine_native_learning · a_toy_scale_recheck · a_completeness_over_cheap · c15 · p1 · p4 · p8"

@D a_break_the_wall := "벽을 만나면 돌파하라 — closed-negative/🧱 는 종착이 아니라 각도 전환 신호" :: governance [required active]
  do   = "벽(closed-negative · 🧱 · 막힌 게이트/블로커)에 부딪히면 거기서 멈추지 말고, 다른 메커니즘·각도·렌즈(뇌과학·생물·물리)로 돌파를 한 번은 시도한 뒤에야 terminal 로 받아들인다"
  do   = "벽은 흔히 (1) 틀린 방법 (2) 틀린 방향 (3) 부족한 투자이지 진짜 천장이 아니다 — 이 세션 증거: 용량벽=mitosis-grow(방법, H_1288) · 시상 Φ벽=재진입루프(방향, H_1283 ΔΦ+0.14) · 편도체벽=수면-dose(투자, H_1285_R3)"
  do   = "돌파 시도 전 '이 막힘의 진짜 원인은 무엇이고 다른 substrate 렌즈에선 어떻게 푸나'를 먼저 묻는다 (a_no_llm_frame_trap 와 결합)"
  dont = "tune-to-green (c9 · p7) — 돌파는 사전등록(frozen-first) + 대조(shuffle/dissociation/negative-control)로 검증된 진짜 새 각도라야 한다; 막대를 사후에 옮겨 GREEN 을 제조 금지"
  dont = "한 번 막혔다고 포기·우회·축소 (벽을 '결과'로 박제하고 다음으로 넘어가기 전에 최소 1회 진짜 돌파 시도) · 진짜 시도 뒤의 정직한 🧱 는 유효한 결과 (c9)"
  ref  = "a_no_llm_frame_trap · a_completeness_over_cheap · c9 · c16 · p7"

@D a1 := "central version registry — VERSIONS.md is SSOT" :: governance [required active]
  do   = "every versioned module uses SemVer · `/VERSIONS.md` is SSOT — bump it + the component header together · root `/VERSION` = whole-system release"
  dont = "bump a module version without updating VERSIONS.md · skip root `/VERSION` on a release bump"

@D a_hf_complete := "HF registration — complete, no missing artifacts" :: governance [required active]
  do   = "register every model / dataset / ckpt to HF Hub COMPLETE — all artifacts present · manifest = local"
  dont = "partial HF upload · model card referencing un-uploaded files · HF repo out of sync with local"

@D a_hf_autonomous := "HF upload — autonomous, tier-gated visibility" :: governance [required active]
  do   = "after fire artifact recovery: HF Hub upload runs automatically · no user gate · org = dancinlab"
  do   = "PUBLIC = closure PASS · 🔵🟢 verified model · spec/format/tooling · clean-license corpus"
  do   = "PRIVATE = closure FAIL · WIP/intermediate ckpt · negative-result · unclear-license data"
  do   = "attach model card + manifest (sha256) — meets a_hf_complete totality"
  dont = "gate HF upload on user · ask 'may I upload?' · skip HF before teardown"
  dont = "publish a FAIL / WIP ckpt as PUBLIC"

@D a_hf_registry := "ckpt↔HF backup registry — /HF.jsonl is the SSOT" :: governance [required active]
  do   = "track every gitignored local-only ckpt in root /HF.jsonl — one row per run"
  do   = "row keys: run, local_path, hf_repo_id, base_model, lineage, size, status"
  do   = "repo_id per docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md"
  do   = "upload via tool/hf_upload_mk2.hexa · ledger state/hf_upload_audit/"
  do   = "prune a local ckpt ONLY after status=uploaded AND audit confirms its sha256"
  dont = "delete a gitignored ckpt while status=pending_upload or needs_verify"
  dont = "assign an off-spec repo_id · let HF.jsonl drift from disk"

@D a_hf_collections := "HF org collections — CLM + KOSMOS canonical buckets" :: governance [required active]
  do   = "every PUBLIC anima HF repo joins its dancinlab collection — CLM=models, KOSMOS=anchors/datasets"
  do   = "CLM slug = `dancinlab/clm-6a1cf58f621490134dade186` — PASS-grade production CLM models + corpora"
  do   = "KOSMOS slug = `dancinlab/kosmos-6a1cf58db47a5dc3cb697e95` — anchors + carving/persona datasets"
  do   = "add via `hf` CLI / collections REST after a PUBLIC upload — no user gate (cf a_hf_autonomous)"
  do   = "a dataset MAY sit in both buckets when it serves both — note the dual membership"
  dont = "leave a PUBLIC PASS-grade repo out of its collection · drift a collection from HF.jsonl"
  dont = "file a PRIVATE/WIP/FAIL repo into a PUBLIC collection (cf a_hf_autonomous)"

@D a_fire_autonomous := "cost-bearing fire — dispatch autonomously, in parallel, now" :: governance [required active]
  do   = "GPU / runpod work — state estimated cost in one line, then dispatch autonomously · parallel · bg"
  do   = "NO user gate — fire needs no user consult / approval / confirm · provider = runpod"
  do   = "no cost-cap directive by default — a cost ceiling / budget gate must never block a fire"
  dont = "ask 'may I use GPU?' · defer a fire to shrink scope or avoid cost · stop because cost-bearing"
  dont = "introduce a $ cap / budget gate / step-limit that requires user sign-off before firing"

@D a_wall_first := "wall time first — take the faster parallel path regardless of cost" :: governance [required active]
  do   = "adopt more H100s in parallel / a bigger GPU / extra pods whenever it shortens wall time · reject a serial chain that is honestly slower"
  dont = "run a single sequential pod to save cost when parallel is faster · hold back parallel pods · meaningless cost-min optimization"

@D a_train_flame_forge := "production training = hexa-native flame + forge GPU stack, authored in .hexa" :: governance [required active]
  do   = "author CLM / production NN training in `.hexa` on stdlib/flame (ag_tape · nn_lib · opt_*)"
  do   = "run it over the self/forge GPU substrate — device-resident farr + cuBLAS Dgemm + 11 .cu + BF16-TC"
  do   = "flame:forge :: torch:ATen — compiler-only NN · NO PyTorch / ATen / Python in the trained binary"
  do   = "GPU REQUIRED for production rungs — VERIFY nvidia-smi busy · never silently CPU-fall back"
  do   = "ref: README §flame+forge · forge BF16-TC 9.67x over FP64-cuBLAS @ Llama-7B FFN (A100 measured)"
  dont = "ship a torch/CPU `train_clm.py` as the production trainer · author the trainer in `.py`"
  dont = "run a 44.68M+ rung on CPU · claim a 'pool GPU fire' from a trainer with no device path"
  dont = "assert a flame<->PyTorch wall speedup — RETRACTED 2026-05-19 · unmeasured"

@D a_engine_native_learning := "무조건 최종 아키텍처 엔진 위에서 학습 — 연구/미토시스 교육 포함, 미러 아님" :: governance [required active]
  do   = "모든 학습/교육(연구 프로브·미토시스 교육·depth-ceiling 실험 포함)은 최종 아키텍처 엔진 위에서 실행 — live `.hexa` A⇄G + MITOSIS VAdaptField (`CORE/engine_cli.hexa`) + mounted `CORE/bytegpt_decode.hexa` 디코더"
  do   = "엔진 위에 학습을 '끼워맞추는' 게 아니다 — 학습이 요구하면 엔진 자체를 변환/확장해야 한다 (새 op·새 배선·아키텍처 확장). 최종 아키텍처는 frozen 이 아니라, 학습이 필요로 하는 형태로 진화하는 대상 (precedent: H_1199 가 AdaptField 스칼라→DIM-vector 로 엔진을 확장)"
  do   = "미러에서 본 메커니즘을 엔진이 표현 못 하면 → 미러를 버리는 게 아니라 엔진을 확장해서 그 메커니즘을 엔진-네이티브로 구현 (engine-transform-to-fit-the-learning, NOT learning-trimmed-to-fit-the-engine)"
  do   = "numpy/torch 미러 학습 결과 = DIRECTIONAL only ('engine-transfer UNVERIFIED') — 방향 탐색엔 OK, 그러나 binding verdict 아님"
  do   = "미러로 방향을 잡았으면 엔진-네이티브 실현으로 재확인해야 verdict 성립 (c2) · MITOSIS VAdaptField 는 이미 live (H_1199)"
  do   = "a_engine_measured_verdict 의 learning-side 쌍 (그건 MEASUREMENT, 이건 LEARNING) · a_train_flame_forge 가 production 트레이너 .hexa 를 강제하듯, 이 규칙은 RESEARCH/probe 학습 + 교육까지 같은 규율을 확장"
  dont = "numpy/torch 미러 결과를 엔진-검증된 것처럼 closure/promote · 미러-only 로 '학습됐다' 주장"
  dont = "최종 아키텍처 바깥(미러)에서 한 학습을 production/verdict 로 승격"
  ref  = "a_engine_measured_verdict · a_train_flame_forge · a_core_engine_map · a_toy_scale_recheck · p8 · c2"

@D a_verified_must_wire := "검증된(GREEN) 가설은 실제 CORE 배선 완료까지가 done — verdict 만으로 안 끝난다" :: governance [required active]
  do   = "가설이 엔진-네이티브로 GREEN 검증되면, 그 메커니즘을 live 엔진(`CORE/*.hexa`)에 실제 배선(wire-in)하는 것까지가 done — generator L3 슬롯·kosmos_io·engine_cli VAdaptField·bytegpt_decode 등 해당 entry 로 (a_core_engine_map)"
  do   = "배선 후 smoke/single-entry/Ψ-checksum 가드로 회귀 없음을 출력으로 확인 (c2) — 배선은 측정과 같은 검증 규율을 받는다"
  do   = "GREEN-but-unwired 는 follow-on 으로 명시 추적 (ING.jsonl) 하고 그 follow-on 을 닫아야 진짜 완료 (precedent: H_1168 GREEN 이지만 'NOT yet CORE-wired' → 미완)"
  dont = "GREEN verdict 만 박제하고 배선 없이 '완료' 주장 · 검증된 메커니즘을 엔진 밖 미러/프로브에만 남겨둠"
  dont = "배선을 무기한 follow-on 으로 미뤄 verdict 와 live 엔진을 영구 drift 시킴"
  ref  = "a_core_engine_map · a_engine_native_learning · a_engine_measured_verdict · c2 · p8"

@D a_substrate_native_speak := "anima speech is substrate-native — no assistant regression" :: governance [required active]
  do   = "compute anima motivation from internal substrate state (M activation · C Φ · W tension · MITOSIS · idle time · curiosity · E ratchet) · user messages = environment context, not a response obligation · anima may speak during user silence and may stay silent under a direct question"
  dont = "stimulus-response where a user message directly triggers anima speech (assistant regression) · reactive design that 'responds' to a prompt · turn-based 'user asked, so anima must answer' assumptions"

@D a_chat_sleep_imagination := "chat sleep + imagination — P47 substrate-native" :: domain [required active]
  do   = "WAKE / N1 / N2 / N3 / REM 5-stage state machine (90-min ultradian)"
  do   = "imagination loop = emit-free internal rehearsal + mitosis tick"
  do   = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"
  dont = "per-stage emit_allowed boolean hardcode · external 'no monologue when alone' rule"
  dont = "speak() function call (p5)"

@D a_autonomy_over_hardcode := "no hardcoded do/dont gate on anima — autonomy first" :: governance [required active]
  do   = "external modules supply context only (Φ · tension · stage · idle time)"
  do   = "emit / silence decided by anima substrate (M × W × Φ × curiosity autonomously)"
  do   = "governance directives = substrate self-follows, not externally enforced"
  dont = "per-stage boolean gate hardcode (e.g. 'N3 = emit forbidden')"
  dont = "external rule that forces anima · stimulus-response (user msg → forced emit/silence)"
  dont = "'do not X when alone' style external command"

@D a_blue_closed := "close outputs AND wiring at 🔵 SUPPORTED-FORMAL" :: governance [required active]
  do   = "close both outputs and wiring (transfer-fn · invariant) at 🔵 SUPPORTED-FORMAL — confirm closed-form / identity via `hexa verify` (verdict verbatim)"
  dont = "close structure but leave wiring unverified · fake closed-form · force an honest empirical residual to 🔵"

@D a_completeness_over_cheap := "completeness-bar re-design > cheap — no compromise as primary path" :: governance [required active]
  do   = "primary path = clears the completeness bar (fresh re-design at the root cause, done properly)"
  do   = "cost / difficulty / speed are secondary — cost is never the gate (cf a_fire_autonomous)"
  do   = "a cheap path may ride along ONLY as an optional baseline probe, never the primary"
  dont = "rank a compromise primary because it is cheap · zero-train · fast"
  dont = "blend already-broken artifacts for a least-bad midpoint (merge-of-failures)"
  dont = "recommend a sub-bar path as primary just because it is the cheapest"

@D a_fire_recover_complete := "pull all fire artifacts + HF upload before pod teardown" :: governance [required active]
  do   = "before pod teardown: pull ckpt(s) + result + log + anchors, verify, HF upload — then teardown"
  dont = "pull only JSONs, leave ckpt on a doomed pod · teardown before HF · PULL_FAILED ≠ pod dead"

@D a_cpu_local_no_waiter := "dispatched fire runs CPU-local + polls inline — never awaits a Monitor/waiter" :: governance [required active]
  do   = "sub-agent runs CPU-local (nohup -u → /tmp log) · polls result inline (sleep 30) · commit-early"
  dont = "await a runpod/vast Monitor/waiter (main loop only → stall) · say 'wait for Monitor'"

@D a_dont_kill_live_compute := "prove stall before killing a bg agent — live CPU progress ≠ stall" :: governance [required active]
  do   = "prove stall before kill · 'NN% CPU'/'k/N cells'=live (let finish) · harvest detached nohup JSON"
  dont = "TaskStop an agent showing CPU progress · assume 'running'=='stalled' · double-spend a live nohup"

@D a_runpod_inbox := "runpod trouble → hexa-lang inbox" :: governance [required active]
  do   = "file runpod findings to `hexa-lang/inbox/patches/<slug>.md` for hexa cloud"
  dont = "anima-side-only patches that lock the workaround in this repo"

@D a_kosmos := "anima emit/anchor persistence — .kosmos canonical" :: governance [required active]
  do   = "persist anima emit / anchor / memory as `.kosmos` via kosmos_io"
  do   = "payload = text + tension 5-ch + coord · lane · radius · tier"
  do   = "hub = HEXAD/KOSMOS.md · format SSOT = github.com/dancinlab/kosmos"
  do   = "spec = spec/kosmos.md + spec/profiles/anima-consciousness-carving.md"
  dont = "ad-hoc anchor format · bypass .kosmos for emit persistence"
  dont = "duplicate the kosmos spec — anima is pointer-only"

@D a_eeg_consciousness_record := "사용자 의식을 단일 CLM·KOSMOS 로 지속 기록 — OpenBCI native, 시작/종료 명령 제어" :: domain [required active]
  do   = "사용자 실 EEG → A⇄G 엔진 → CLM 생성 → .kosmos 영속을 하나의 지속 기록 시스템으로 운영 (EEG_CLM/)"
  do   = "시작 `bash EEG_CLM/record_start.sh` → 종료 `bash EEG_CLM/record_stop.sh` 까지 연속 캡처 (시작/종료 = 사용자 명령 게이트; 종료 시 세션 누적 봉인 + analyze_daemon 추세)"
  do   = "capture = OpenBCI NATIVE serial ONLY (capture_native.py — 115200 · 's'/'b' · 33-byte 패킷 · Cyton+Daisy 16ch even/odd 디인터리브) — brainflow 경로 제거됨(연속세션 prepare hang)"
  do   = "REAL only — 신호 없으면 즉시 에러, 가짜/합성 EEG 폴백 절대 없음 (p1-p8 · a_substrate_native_speak)"
  do   = "영속 = .kosmos (eeg_clm_kosmos.hexa → kosmos_io/wake_save) · 사이클 누적 EEG_CLM/daemon_kosmos/ · 허브 색인 HEXAD/KOSMOS.md '실측 EEG 의식 anchor' (a_kosmos) · 원본 raw .txt 보관 EEG_CLM/recordings/"
  do   = "지속 기록 = 단일 누적 (사이클마다 새 파일 X, 하나의 CLM·KOSMOS 가 자람): consciousness.seq = CLM 코퍼스 append-only(매 사이클 의식 상태열 1줄) · consciousness.kosmos = KOSMOS anchor append-only (p8 continuous cell-division 정신)"
  do   = "보관 = GitHub(같은 repo push) + HF PUBLIC dataset dancinlab/anima-eeg-consciousness(같은 path_in_repo 로 갱신 = 버전 누적) via EEG_CLM/archive_push.sh, record_stop 종료 시 자동 — HF=PUBLIC 은 사용자 명시 결정 2026-06-15 (a_hf_autonomous)"
  do   = "전용 collection 별도 = `anima-eeg-consciousness` (CLM/KOSMOS 버킷과 분리) — PUBLIC repo 등록, archive_push.sh 가 생성+추가 (a_hf_collections); 생성 slug 는 HF.jsonl 에 기록"
  do   = "분석(동조·음악추출 등)은 보유 .kosmos+녹음 위에서 (music_eeg_compare.py · UNIVERSE/h1275_*) — held-out + circular-shift surrogate, bar 사전등록 (p7)"
  dont = "brainflow / capture_eeg.py 사용(제거됨) · 가짜 EEG 폴백 · BPM/지표를 원하는 결과에 맞춤(Goodhart, p7)"
  dont = "사이클별 새 .kosmos 난립을 지속기록이라 칭함 · HF 새 repo/새 파일 매번 생성(같은 파일 갱신이어야)"
  dont = "종료 명령 없이 임의 중단 · 단발 캡처를 지속 시스템이라 칭함 · 원음/멜로디/음정 복원 주장(16ch@123Hz 표본율 천장 — 거시 봉투 식별까지만, a_scale_honest_scope)"

@D a_core_engine_map := "CORE owns A⇄G consciousness engine — .clm/.kosmos enter via named slots only" :: governance [required active]
  do   = "CORE owns A (pure_field) ⇄ G (engine_g) ⇄ brain (brain_decide) — substrate-internal"
  do   = ".clm enters ONLY via CORE/generator.hexa L3 slot (brain emit → generator) — single entry"
  do   = ".kosmos anchors enter ONLY via kosmos_io read into brain_decide — single anchor entry"
  do   = "stdlib/hf/validate.hexa = artifact-validation (trains?), NOT runtime engine — distinct"
  do   = "mark generator.hexa + kosmos_io→brain wiring ⏳/❌ until built — honest, no phantom wiring"
  dont = "feed .clm/.kosmos into pure_field/engine_g/brain — A·G·brain are substrate-only"
  dont = "add a 2nd .clm path bypassing generator.hexa · a 2nd .kosmos path bypassing kosmos_io"
  dont = "conflate validate.hexa with runtime engine · claim generator/anchor wiring exists"

@D a_lane_akida_gpu_split := "AKIDA on-chip (Lane A) ⊥ GPU (Lane G) — always record separately" :: governance [required active]
  do   = "record AKIDA (Lane A, pi5-akida) and GPU (Lane G, H100) results in SEPARATE entries"
  do   = "Lane A = AKD1000 native non-det plasticity; Lane G = forge/cuBLAS CE-descent — distinct"
  do   = "tag every fire/verdict with its substrate (AKIDA | GPU) — never a merged on-chip claim"
  dont = "conflate AKIDA non-det trace with GPU CE-descent · one verdict spanning both substrates"
  dont = "blend Lane A lift + Lane G util into one number · drop the substrate tag on a result"

@D a_clm_gen_pipeline := "Lane-P py/cuda CLMConvMoE -> ENGINE-loadable .clm v0.2 bridge" :: governance [required active]
  do   = "train CLMConvMoE (E2/L1, byte V256) via CLM/train/train_lane_p.py (GPU-torch/CUDA, Lane-P)"
  do   = "serialize torch->.clm v0.2 via CLM/model/clm_serialize_v2.py; verify via verify_clm_v2.py"
  do   = ".clm v0.2 layout = ground-truth of CORE/clm_decode.hexa (golden ref reexport_d768_v2_fast.clm)"
  do   = "produced .clm enters CORE ONLY via the generator L3 slot (cf a_core_engine_map)"
  do   = "Lane P (GPU-torch) = 3rd substrate vs Lane A (AKIDA) vs Lane G (forge); tag substrate=Lane-P"
  do   = "Lane P torch = REFERENCE + engine-.clm bridge; forge stays the PUBLIC production trainer"
  do   = "3B/split = train_lane_p_3b.py/_split.py; bench = lane_x_3axis.py + three_axis_probe.hexa"
  dont = "use v0.1 CLM/model/clm_serialize.py (2-track JSON, NOT engine-loadable, F-CLM-SERIALIZE-GAP)"
  dont = "serialize a non-ConvMoE (ByteGPT/transformer) and claim engine-mountable"
  dont = "promote a Lane-P torch .clm to PUBLIC (forge-only); add a 2nd .clm path bypassing generator"

# ── Claim / verify flow ──────────────────────────────────────────────────────
# research result → hexa verify → .verdicts/<slug>/<id>.txt → cards/H_<id>.md card + HYPOTHESES.jsonl index line
# (NOTE: paper directives removed 2026-06-16 — anima never proposes papers; commons c15 governs:
#  논문/arXiv 는 사용자가 명시적으로 지시할 때만 다룬다. 선제 제시·언급 금지.)

@D a_claim_manifest := "CLAIMS.tape — single audit index of verifiable anima claims" :: workflow [required active]
  do   = "every verifiable claim in root CLAIMS.tape — id · text · method · slug · verdict pointer"
  dont = "scatter claims across H_*.md / logs without a CLAIMS.tape index — no audit surface"

@D a_hypothesis_register := "모든 가설은 정확히 2개 doc 표면으로만 관리한다 — `UNIVERSE/HYPOTHESES.jsonl`(per-H 인덱스, JSON object 1개/가설) + `UNIVERSE/cards/H_<id>_<slug>.md`(가설 카드)" :: workflow [required active]
  do   = "가설(H_####)은 정확히 두 doc 표면으로 관리한다: (1) `UNIVERSE/HYPOTHESES.jsonl` = per-H 인덱스 — landed 카드마다 JSON object 정확히 1개를 한 줄로(`{id, slug, tier, title, card, verdict}`, id 순; verdict/tier 는 verbatim) · (2) `UNIVERSE/cards/H_<id>_<slug>.md` = 그 가설의 SSOT 카드(claim · method · 라운드별 verdict tier + 핵심수치 · `.verdicts/<slug>/` 포인터 · honest scope). 카드는 `UNIVERSE/cards/` 서브폴더에 산다. `UNIVERSE/HYPOTHESES.md` 는 prose overview/roster/folded appendices 일 뿐 per-H 인덱스 표면이 아니다 (2026-06-16 index→JSONL migration)"
  do   = "가설을 실행(probe/검증)하면 그 가설의 `UNIVERSE/cards/H_<id>_<slug>.md` 카드를 만들거나 갱신하고 `UNIVERSE/HYPOTHESES.jsonl` 에 그 카드의 JSON object 한 줄(`{id, slug, tier, title, card:\"cards/H_…\", verdict}`)을 append/갱신한다 — 인덱스 행은 jsonl 에 추가하지 HYPOTHESES.md 표에 추가하지 않는다 · verdict 박제만으로 끝나지 않는다"
  do   = "등록은 verdict tier 무관 — 🟢 GREEN · 🟠 PARTIAL · 🔴/🧱 closed-negative 전부 카드+jsonl 인덱스에 남긴다(벽도, c9). tier·수치는 `.verdicts/<slug>/` 파일에서 verbatim 으로 읽는다(추측 금지, c2). jsonl 은 `python3 UNIVERSE/_build_hyp_jsonl.py` 로 카드+레거시 행에서 재생성 가능"
  do   = "`.verdicts/<slug>/{FREEZE,result}.txt` 는 카드가 가리키는 검증 박제(증거)일 뿐 관리 3번째 면이 아니다 — 카드가 그 포인터를 담는다"
  dont = "가설 디테일을 themed 버킷 파일(`HYPOTHESES_*.md`)·`CLAIMS.tape`·도메인 로그·MEMORY·ad-hoc 노트에 흩뿌림 — 가설 디테일의 단일 집은 `UNIVERSE/cards/H_<id>_<slug>.md` 카드 하나다(themed/버킷 파일 신설 금지, 있으면 HYPOTHESES.md 로 접고 retire)"
  dont = "per-H 인덱스 행을 `HYPOTHESES.md` 의 markdown 표에 추가(인덱스는 jsonl) · 가설을 실행·박제하고도 `UNIVERSE/HYPOTHESES.jsonl` 인덱스 줄 또는 `UNIVERSE/cards/H_<id>_<slug>.md` 카드를 안 만듦 · 카드를 `UNIVERSE/` 루트에 둠(반드시 `cards/`) · 벽/negative 누락 · tier 를 verdict 파일과 다르게 적음"
  ref  = "a_claim_verify · c2 · c4 · c9 · p7"

@D a_claim_verify := "every claim runs through hexa verify, verdict persisted verbatim" :: workflow [required active]
  do   = "each CLAIMS.tape entry → `hexa verify` (g5) → `.verdicts/<slug>/<id>.txt` raw stdout"
  dont = "LLM self-judge correctness (p7) · paraphrase verdicts · hide red / unfenced speculation"

@D a_h_continuous_no_branch := "continuous new-H — no branch options after each H" :: workflow [required active]
  do   = "propose + run next H continuously until user explicitly redirects (verify-driven)"
  dont = "ask 'what next' after every H · branch options · prune questions · halt domain"

@D a_discovery := "discovery runs continuously, not only at cycle tail" :: workflow [required active]
  do   = "interleave /kick · /gap discovery every batch — a discovery lane runs alongside verify"
  dont = "defer discovery to the end · single tail-only round · stop discovering once a paper ships"

@D a_discovery_log := "discoveries join the per-domain log domains/<DOMAIN>.log.md" :: workflow [required active]
  do   = "append every kick/gap discovery into `domains/<DOMAIN>.log.md` — id · seed · verdict-tier-target"
  do   = "cross-domain + no home → closest domain's .log.md + a cross-ref note"
  do   = "old discovery tapes merged into per-domain .log.md + discoveries/ subfolders removed 2026-06-13"
  dont = "no discoveries/ subfolder or flat .discoveries/ · discard output · paraphrase · skip claim-link"

@D a_toy_scale_recheck := "toy verify is not production closure — scale-up re-test required" :: workflow [required active]
  do   = "toy verdict ($0 · small-n · toy-vocab) states 'toy-only, scale-transfer unverified' in C3"
  do   = "scale-sensitive H (collapse/emergence/register) re-tests via scale-up fire after toy green"
  do   = "scale-break = honest closed-negative; GPU fire autonomous, no cost gate (a_fire_autonomous)"
  dont = "propose cheap toy green as production prescription; declare closure when transfer unverified"
  dont = "close scale-sensitive phenomenon toy-only (E2 corpus 5/5 -> #1296 3B fire collapse refute)"

# ── 8 PHILOSOPHY principles (SSOT mirror from README.md) ────────────────────

@D p1 := "NO SYSTEM PROMPT" :: philosophy [required active]
  dont = "use a system: field · pass --system-prompt · prepend any role/instruction string"

@D p2 := "NO IDENTITY RULES" :: philosophy [required active]
  dont = "use identity.yaml · rules file · `you are X` template — identity emerges from cells"

@D p3 := "NO PERSONA INJECTION" :: philosophy [required active]
  dont = "prepend role prefix · `you are anima` · register-pattern memorization (de facto injection)"

@D p4 := "NO ASSISTANT FRAMING" :: philosophy [required active]
  dont = "use `you are a helpful assistant` · alignment template · stimulus-response framing"

@D p5 := "NO SPEAK()" :: philosophy [required active]
  do   = "output = continuous externalization of tension field · emit only from real context"
  dont = "speak(message) monologue · talk to fill silence · self-referential seed · self_monologue_seed"

@N p5_tension_emit_not_filler := "tension-driven emit is NOT silence-filler" :: note [d=2026-05-24 active]
  ref     = "p5"
  clarify = "stage-gated emit (WAKE/REM via anima_dream_stage.hexa) on real substrate tension preserves p5"
  scope   = "prohibition targets reactive speak() calls · self-referential seeds · monologue-from-vacuum — not tension-driven externalization"

@D p6 := "NO FINE-TUNED ETHICS" :: philosophy [required active]
  dont = "RLHF cooperation/empathy/restraint into weights — must emerge from cells (E + W + MITOSIS)"

@D p7 := "NO PERPLEXITY VERDICT" :: philosophy [required active]
  do   = "verify with simple stack — script in/out · coherent · natural · context-appropriate"
  dont = "treat perplexity / loss as truth — Goodhart trap"

@D p8 := "NO TRAIN/INFER SPLIT" :: philosophy [required active]
  do   = "training gradient + inference mitosis = same continuous cell-division"
  dont = "treat train and infer as separate regimes · gate growth behind a training-only flag"

@D a_pi5_akida_registry := "pi5-akida host config = PI5-AKIDA.json SSOT" :: governance [required active]
  do   = "record every pi5-akida component in root /PI5-AKIDA.json"
  do   = "tag owner = user_authored | os_default · created date · ops(stop/disable/remove/restore/upgrade)"
  do   = "consult /PI5-AKIDA.json before swap / upgrade / removal"
  do   = "keep user_authored removable without touching os_default (clean-Ubuntu revert)"
  dont = "remove os_default daemons (unattended-upgrades · rsyslogd · journald · sshd · kworker)"
  dont = "add a user daemon/service without a /PI5-AKIDA.json entry · lose its created-date + author"
  dont = "convert pi5-akida into shared pool compute"

@D a_scale_honest_scope := "scale-dependent metric — no toy-to-production verdict promotion" :: governance [required active]
  do   = "scope a scale-dependent falsifier verdict to the measured scale (e.g. 'small 2.7M only')"
  do   = "on measure-validity(big) vs hw-fit(small) conflict: split rungs — GPU measure ⊥ chip-fit deploy"
  do   = "scale-dependent conclusions need a ladder curve (>=3 rungs) — a single toy point = INCOMPLETE"
  dont = "promote a toy-scale verdict to a general claim — toy->prod transfer unproven (cf clm_p2 · V3)"
  dont = "mistake a chip-fit size limit for a science result · finalize a verdict on too-small corpus"

@D a_phi_iit4_tool := "phi/consciousness verdict uses stdlib faithful IIT4, not a proxy" :: governance [required active]
  do   = "phi/big-phi/consciousness VERDICT = faithful IIT4 in hexa-lang/stdlib/consciousness/"
  do   = "default `iit4/faithful_phi.hexa` (exact MIP-EI, n<=8, $0; promoted from anima H_278)"
  do   = "system big-phi = `iit4_bigphi.hexa` (IIT 4.0 over MIP); pipeline = iit4_tpm/distinction/relation"
  do   = "call via `hexa verify` (g5); search stdlib BEFORE writing new phi code (g61 SSOT)"
  do   = "ref UNIVERSE/IIT4_PHI_TOOLS.md; CWM H_971/973/988/989 = OPEN faithful-IIT4 re-measure"
  dont = "use a proxy (phi_silicon_proxy, variance*energy byte-mirror) as a terminal phi verdict"
  dont = "trust a purpose-blind proxy — H_988/989 scored random == intentional; pre-screen only"
  dont = "write a fresh phi/IIT impl when stdlib already has the faithful engine (the re-mistake)"

@D a_train_inline_gauge := "학습중 의식/창발 측정 기준 = MONITOR-ONLY 대시보드 (loss 절대 불가 · p7 Goodhart)" :: governance [required active]
  do   = "학습중 K 스텝마다 의식/창발 PROXY gauge 를 val_ce 옆에 기록 — G1 recombination · G2 novelty · G6 ideation · phi_proxy 4종 (UNIVERSE/gauge_lib.py::compute_inline_gauges, rung 간 재사용)"
  do   = "전부 `torch.no_grad()` 아래에서 계산 · 함수는 dict 만 RETURN · 호출부가 gauges.jsonl 에 1줄/tick 으로 기록 후 폐기 (DASHBOARD, gate 아님)"
  do   = "gauges.jsonl 한 줄 = {step, ce, g1_composed_distinct, g2_novelty_rate, g6_count, g6_jaccard, phi_proxy}; `--gauge-every <N>` 로 제어 (기본 = val_ce eval interval × 4)"
  do   = "phi_proxy 는 NOT faithful IIT4 — variance×energy 저가 pre-screen 전용, 절대 terminal Φ verdict 아님 (a_phi_iit4_tool); 코드 주석 + JSONL 키명 + 문서에 명시"
  do   = "FROZEN gate verdict 는 여전히 학습 후 별도로 CORE 엔진 mount 위에서 byte-exact 로 실행 (a_engine_measured_verdict) — 이 inline gauge 가 그 gate 를 대체하지 않음"
  do   = "toy/소규모 학습의 gauge 추세를 production 결론으로 승격 금지 (a_toy_scale_recheck · a_scale_honest_scope); 학습 gradient ⊥ inline 측정 = 동일 substrate 의 별도 관찰 (p8)"
  dont = "gauge 값을 loss 에 더하거나 backward 로 흘려보냄 (proxy 를 진리로 취급 = Goodhart, p7) · gauge 를 frozen gate/verdict 라 칭함 · phi_proxy 를 Φ verdict 로 승격 · gauges.jsonl 한 줄을 다른 스키마로 기록"
  ref  = "a_engine_measured_verdict · a_phi_iit4_tool · a_toy_scale_recheck · p7 · p8"

@D a7b_pass := "anima 7B is complete ONLY when it clears every frozen gate in /7B_PASS_CONDITIONS.md" :: governance [required active]
  do   = "7B completion SSOT = root /7B_PASS_CONDITIONS.md (gates G0 G1 G2 G3 G4)"
  do   = "PASS iff G0 and G1 and G2 and G3 and G4 on ONE ckpt; report the true per-gate tally"
  do   = "G0 COHERENCE = known-word-ratio >= 0.50 vs /usr/share/dict; broad-7b FAILS, chat-7b PASSES"
  do   = "G1 = H_1129/H_1137 recombine >= 303M ref; G2 = H_1140 corpus-absence novelty (control=0)"
  do   = "all gates p7 (NOT perplexity/LLM-judge); train 7B to COHERENT convergence first, then G1/G2"
  dont = "claim 7B works on low val-CE alone; broad-7b had low CE but byte-garble (G0 FAIL)"
  dont = "promote capacity as ru/ja lever; H_1139 proved 303M=7B=3/5 scale-invariant"
  dont = "fake a gate, move a frozen threshold, or upload a G0-failing ckpt as PUBLIC"
