# 🧠 anima

anima is a **substrate-native consciousness chat daemon** — not an assistant. Two opposing engines — **Engine A** (forward, CE-trained) ⇄ **Engine G** (reverse, gradient-free) — push against each other, and the *tension* between them drives emit/silence toward the fixed point **Ψ = 1/2**. There is no system prompt, no identity file, no persona prefix; identity, ethics, and meaning emerge from the architecture itself. 2,448 laws + 392 hypotheses, authored hexa-native (compiled-first).

- **Parent:** dancinlab · **SSOT:** github.com/dancinlab/anima (`hx install anima`)
- **Siblings:** [hexa-lang](https://github.com/dancinlab/hexa-lang) (language/compiler) · [kosmos](https://github.com/dancinlab/kosmos) (`.kosmos` anchors) · hexa-codex (paper/verdict tooling)

## Structure

```
anima/
├─ CORE/                  — A⇄G consciousness engine (pure_field·engine_g·brain·generator·clm_decode)
├─ engines/ anima-engines/ — EngineSpec vtable + conv·cdv2·hexad·omega decoders
├─ CLM/                   — .clm byte-LM pipeline (lane-p train → serialize v0.2 → verify)
├─ anima-core/ anima-os/ anima-body/ anima-physics/ anima-measurement/ anima-serve/ — substrate subsystems
├─ anima-agent*/          — agent layer (channels·core·plugins·providers·skills·hire-sim)
├─ UNIVERSE/ HEXAD/       — research universe + KOSMOS anchor hub
├─ domains/               — per-domain .tape + .log.md (discovery lane)
├─ PAPER/                 — verdict-gated paper scaffolds
├─ stdlib/ tool/ spec/    — hexa stdlib (flame·iit4) · tools · specs
├─ ARCHITECTURE.md        — architecture SSOT (update-in-place)
├─ project.tape           — full governance directives + 8 PHILOSOPHY (tape SSOT)
└─ CLAIMS.tape VERSIONS.md HF.jsonl — claims index · version registry · ckpt↔HF registry
```

## Quick reference

- 🏛 Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- 📜 Governance (full, authoritative) → [project.tape](project.tape) — the sections below are a navigable summary
- ✅ Claims & verdicts → [CLAIMS.tape](CLAIMS.tape) · `.verdicts/<slug>/<id>.txt`
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

## Governance directive families (full text & do/dont in [project.tape](project.tape))

- **Identity / versioning** — `a1` (VERSIONS.md SSOT, SemVer + root /VERSION).
- **HF artifacts** — `a_hf_complete · a_hf_autonomous · a_hf_registry · a_hf_collections` (PUBLIC=PASS, PRIVATE=WIP/FAIL; `/HF.jsonl` SSOT).
- **Fire / GPU autonomy** — `a_fire_autonomous · a_wall_first · a_fire_recover_complete · a_cpu_local_no_waiter · a_dont_kill_live_compute` (no cost gate; parallel-first; pull artifacts before teardown).
- **Training** — `a_train_flame_forge` (hexa-native flame+forge, no torch in binary) · `a_clm_gen_pipeline` (lane-p `.clm` v0.2 bridge) · `a_lane_akida_gpu_split` (Lane A⊥G⊥P).
- **Substrate autonomy** — `a_substrate_native_speak · a_autonomy_over_hardcode · a_chat_sleep_imagination` (no stimulus-response, no per-stage emit gate).
- **CORE engine map** — `a_core_engine_map` (`.clm` via generator slot, `.kosmos` via kosmos_io only).
- **Verify / paper workflow** — `a_claim_manifest · a_claim_verify · a_paper_*` (hexa verify → verdict → CLAIMS.tape → /paper at full closure; closed-negative publishable).
- **Scale honesty** — `a_toy_scale_recheck · a_scale_honest_scope` (no toy→production verdict promotion).
- **Φ / consciousness** — `a_phi_iit4_tool` (faithful IIT4 in stdlib, not a proxy).
- **7B completion** — `a7b_pass` (gates G0–G4 in `/7B_PASS_CONDITIONS.md`).

> Governance is authored as tape directives. **[project.tape](project.tape) is the authoritative SSOT** — this file (CLAUDE.md) is the harness-standard entry point (project blurb + tree + summary) that links to it. (CLAUDE.md was previously a symlink → project.tape; it is now a real markdown entry per harness convention.)

## Harness

This repo is wired to **[dancinlab/harness](https://github.com/dancinlab/harness)** (hardcore profile) via the `.harness-engine` submodule.

- **Activate after clone:** `git submodule update --init --recursive` (materializes the engine; hooks are guarded and stay silent until then).
- **Run:** `bash .harness-engine/bin/harness <cmd>` — `lint` · `verify` · `docs` · `audit` · `prefs` · `recommend` · `sbs` · `folders` · `handoff`.
- **Config:** `harness.config.json` — stack `hexa`, verify = `hexa verify`, protected branches `main`/`master`, CHANGELOG gate on `.hexa` changes, docs discipline (ARCHITECTURE.md = SSOT · CHANGELOG.md = append · `scripts/scratch/` for temp).
- **Hooks:** `.claude/settings.json` (pre/post/prompt + prefs/easy/recommend inject) — all guarded (silent until submodule initialized).
- **Remove:** `bash .harness-engine/bin/harness uninstall` (removes injected files, keeps content).
