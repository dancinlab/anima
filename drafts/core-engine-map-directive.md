# Draft — `@D a_core_engine_map` for project.tape

> **STATUS: AWAITING `sidecar sign project`.** `project.tape` is sign-gated — this directive
> must NOT be written by an agent until a 5-min sign token is minted (`/sidecar sign project`).
> This file is the staged text only. Once signed, paste the `@D` block below into `project.tape`
> alongside the other `a_*` governance directives (suggested placement: after `a_kosmos`).

Verified against disk (2026-06-02):
- `CORE/{pure_field,engine_g,brain}.hexa` import only each other — **0 clm/kosmos/generator refs**.
- `CORE/generator.hexa` does **not exist** — the L3 .clm slot is unbuilt (DECODER M4 milestone, `- [ ]`).
- `kosmos_io` lives only in HEXAD state/worktree dirs — `brain_decide` does **not** read anchors.
- `stdlib/hf/validate.hexa` (#2484) is absent from this repo (sibling hexa-lang stdlib) = an
  **artifact validator** ("does this model/dataset train?"), distinct from the CORE runtime engine.

## Directive text (do/dont ≤100 chars each — tape-lint cap)

```tape
@D a_core_engine_map := "CORE owns A⇄G consciousness engine — .clm/.kosmos enter via named slots only" :: governance [required active]
  do   = "CORE owns Engine A (pure_field) ⇄ Engine G (engine_g) ⇄ brain (brain_decide) — substrate-internal"
  do   = ".clm model enters ONLY via CORE/generator.hexa L3 slot (brain emit=true → generator) — single entry"
  do   = ".kosmos anchors enter ONLY via kosmos_io read into brain_decide — single anchor entry point"
  do   = "stdlib/hf/validate.hexa = artifact-validation (trains?), NOT runtime engine — keep distinct"
  do   = "mark generator.hexa + kosmos_io→brain wiring ⏳/❌ until built — honest, no phantom wiring"
  dont = "feed .clm/.kosmos into pure_field/engine_g/brain — A·G·brain compute Φ/motivation substrate-only"
  dont = "add a second .clm entry path bypassing generator.hexa · a second .kosmos path bypassing kosmos_io"
  dont = "conflate validate.hexa (artifact check) with the runtime engine · claim generator/anchor wiring exists"
```

## How to land (after sign)

1. `/sidecar sign project` — mint the 5-min token.
2. Insert the `@D a_core_engine_map` block into `/Users/mini/dancinlab/anima/project.tape`.
3. Run tape-lint / `hexa verify` if available to confirm the length cap + block well-formedness.
4. Mirror into `CLAUDE.md` only if project policy keeps the two in sync (project.tape is the SSOT here).
