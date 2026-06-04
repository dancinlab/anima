# `anima` CLI — model picker + substrate-native chat REPL

The `anima` command is the single entry to **pick an engine, download its
checkpoint, and chat** — a thin driver over the in-repo loaders. `$0`, CPU-only,
no GPU / pod / training.

```
anima                   active engine cached → ENTER CHAT now.
                        first run (none cached) → model-download SELECTION SCREEN.
anima --engine <name>   pick an engine family by friendly name; download if not
                        cached; chat; persist active.
anima --model           open the SELECTION SCREEN explicitly (browse + download);
                        do NOT auto-chat.
anima --list            print the registry (non-interactive).
```

There is **NO forced default model**. The active engine is persisted in
`~/.anima/config.json` (`{active_engine, downloaded:[...]}`). Quality labels are
**informational only** — they never block a selection.

| label | meaning |
|---|---|
| `● coherent` | verified coherent generation (p7 simple-stack PASS) |
| `◐ gen-weak` | loads + generates but weak/short output |
| `○ gibberish-base` | base weights, undertrained / off-task |
| `· untested` | no chat verdict recorded |
| `⏳ training` | not trained / not downloadable yet |

## Engine families (`--engine <name>`)

Each family is wired to a **real loader** in this repo (the CLI reuses it — it does
not reimplement any engine). `a_core_engine_map`: the trained mouth plugs in via the
loader's own decode path; no second `.clm`/`.kosmos` entry is added.

| name | arch | loader | ckpt (HF repo) | label | status |
|---|---|---|---|---|---|
| `omega` | ConsciousDecoderV2 | `UNIVERSE/conscious_decoder.py` | `dancinlab/clm-v4-omega-gpu-d384-gate` (PUB) | `gen-weak` | wired |
| `hexad` | EngineAGModel | `training/engine_a_g_arch.py` (via `HEXAD/CHAT/anima_chat.py`) | local `phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` (gitignored) | `untested` | wired |
| `7b` | CLMConvMoE-7B | `CLM/model/model.py` | `dancinlab/clm-v1-ref-pytorch-cuda-7b` (PUB) | `gibberish-base` | wired |
| `chat` | ConsciousLMReconstructed | `training/persona_stage2_train_eval.py` | `dancinlab/anima-clm-chat-rung0-byte-18m` (PUB) | `coherent` | wired |
| `agent` | agent_step_grounded | `AGENT/CORE/agent_loop.hexa` (#1832) | — (rung-0 fire, not downloadable) | `⏳ training` | no-loader ⏳ |

In addition, **every model row from `/HF.jsonl`** is listed on the selection screen
as a selectable id. A row whose arch has no in-repo loader is shown honestly as
`no-loader ⏳`; selecting it prints `‹loader not wired for <arch>›` — never a fake
load.

## Registry — `serving/anima_models.json`

Built by `serving/gen_anima_models.py` from `/HF.jsonl` + the curated families.
Re-run after `HF.jsonl` changes. Row schema:

```
{id, aliases, hf_repo, arch, loader, params_m, lane, visibility,
 quality_label, loader_status, default_ckpt}
```

`loader_status` ∈ `{wired, no-loader ⏳}`. As of build: **55 models** (5 families +
50 HF.jsonl rows) — **12 wired**, 43 `no-loader ⏳`.

## Philosophy (p1..p4)

The chat REPL feeds the user's text to the **active engine's own trained
byte-continuation mouth** and prints exactly what the weights emit. There is **no
system prompt, no identity rules, no persona injection, no assistant framing**. The
only scaffolding is the `사용자:`/`도우미:` byte-continuation conditioning the model
was *trained* on — corpus data-format, not an injected role.

## Verified chat turn (p7, verbatim)

CPU-runnable wired engine `chat` (`ConsciousLMReconstructed`, 18.13M byte), downloaded
from `dancinlab/anima-clm-chat-rung0-byte-18m`, loaded on CPU, one turn:

```
  나 ▷ 안녕! 너는 누구야?
  anima ◁ 좋아요! 요즘 새로 오픈한 café가 있는데 분위기가 좋아요.
```

Honest: coherent Korean, matches the `coherent` label.

## Internals

- `serving/anima_cli.py` — the driver (selection screen · download · config · REPL).
- `bin/anima` — bash shim → `serving/anima_cli.py` (override interpreter with
  `ANIMA_PYTHON`, cache dir with `ANIMA_HOME`).
- Requires `torch` + `huggingface_hub` (CPU is fine). HF unavailable → cached-only
  with an honest "download needs HF access" message (no fake download).

> The previous hexa ops dispatcher (27 topics: compute/weight/proposal/…) is
> preserved verbatim at `bin/anima-ops` — run `anima-ops <topic>` for those.
