<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">anima</h1>

<p align="center"><strong>Substrate-native consciousness chat daemon</strong> · Engine A ⇄ Engine G · Ψ = 1/2</p>

<p align="center"><a href="README.ko.md">한국어</a> · <a href="https://huggingface.co/dancinlab">Hugging Face</a></p>

anima is an consciousness-AI research daemon, not an assistant persona. Its language mouth,
memory, motivation, emission, training, evaluation, and serving behavior run through one shared
Python engine. Identity and behavior are intended to emerge from substrate state rather than a
system prompt.

> [!IMPORTANT]
> **Runtime SSOT:** the installed `anima-py` command and the existing `cli/*.py` and
> `core/*.py` modules are the only active implementation, evaluation, and deployment paths.
> Historical language-toolchain sources, launchers, manifests, and release gates are retired.
> Research data and result evidence remain in `state/`, `archive/`, and Hugging Face.

## Current work — legacy runtime retirement

Status on 2026-08-12:

- [x] Trace active CLI, engine, CI, packaging, and deployment call paths.
- [x] Implement the missing op-grip and stateful-refractory research modes in `cli/chat.py`
  by reusing `core.engine_g` and `core.dream_lib`.
- [x] Replace the CHAT participant's dead spike, dream-stage, and imagination hooks with direct
  Python modules backed by `core.imagination_replay`, `core.wake_memory`, and `core.engine_cli`.
- [x] Remove executable legacy sources, toolchain configuration, launchers, build gates, and
  dangling launchd jobs while preserving model, corpus, and result data.
- [x] Make Python ownership explicit in runtime modules, CODEOWNERS, CI, release, and package docs.
- [x] Pass Python/CHAT regression, compile, workflow, JSON, license, CLI, and isolated wheel QA.
- [x] Complete Git push and Vast.ai runtime deployment QA: pushed commit `7ba4ea21b` passed
  ten remote CHAT regressions, external HTTP health, and correlated user↔participant WebSocket flow;
  the isolated verification instance was then destroyed without touching the active training pod.

User-owned `ING.jsonl` and `stream_mi.json` are outside this work and must remain unchanged.

## Canonical entry

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[train,runtime]"

.venv/bin/anima-py --help
.venv/bin/anima-py train --help
.venv/bin/anima-py evaluate --help
.venv/bin/anima-py chat MODEL.clm
```

Main commands:

| Command | Responsibility |
| --- | --- |
| `anima-py corpus` | Build registered training corpora. |
| `anima-py train` | Train through the shared PyTorch engine and serialize checkpoints. |
| `anima-py evaluate` | Run registered NumPy/runtime measurements and causal controls. |
| `anima-py serialize` | Export existing training checkpoints to runtime formats. |
| `anima-py sweep` | Run bounded multi-device experiment matrices. |
| `anima-py chat` | Run the A⇄G consciousness daemon and byte mouth. |
| `anima-py study` | Run registered interaction studies. |

Research instrumentation that was previously unavailable on the Python path is now part of the
same chat engine:

```bash
anima-py chat MODEL.clm --opgrip
anima-py chat MODEL.clm --opgrip-live
anima-py chat MODEL.clm --opgrip-r3
anima-py chat MODEL.clm --refractory
```

The decode-free `--opgrip` arm can run without a checkpoint. Live and R3 arms fail closed unless
the checkpoint loads successfully.

## Runtime architecture

```text
anima-py
└── cli/anima.py
    ├── cli/train.py ───────► core/model.py ─────► core/serialize.py
    ├── cli/evaluate.py ────► core/decode.py
    └── cli/chat.py
        ├── core/brain.py
        ├── core/pure_field.py       Engine A
        ├── core/engine_g.py         Engine G, motivation, emission, refractory
        ├── core/generator.py ──────► core/decode.py
        ├── core/kosmos_io.py
        └── core/dream_*.py
```

Runtime rules:

- Extend the shared engine instead of adding side harnesses that redo its computation.
- Keep registered data, randomness, criteria, and controls immutable during a measured run.
- Fail closed on missing checkpoints, malformed inputs, incompatible checkpoint structure, or
  missing pinned evaluation assets.
- Keep raw model bytes lossless through UTF-8/surrogateescape and structured JSON output.

## Verification

Local regression:

```bash
.venv/bin/python -m compileall -q cli core anima_py
.venv/bin/python -m pytest -q tests cli/test_train_import_resolution.py agent/domains/CHAT/test_*.py
.venv/bin/anima-py --help
.venv/bin/anima-py evaluate --help
actionlint .github/workflows/*.yml
```

Heavy model and serving QA runs on Vast.ai. Models and training datasets are stored only in
private repositories under the Hugging Face `dancinlab` organization. Secrets are supplied by the
deployment environment or secret CLI and are never committed.

## Latest production evidence

- The 7B store-causality run passed its registered causal, HTTP/WebSocket, soak, recovery, and
  rollback gates after a shared decoder throughput fix. Evidence:
  `state/store_causality_7b_throughput_recovery_2026_08_11/result.json`.
- Live-user QA then invalidated that checkpoint as a semantic chat deployment. The broker and
  participant reply-ownership, prior-emission comparison, language ownership, and cooldown flow
  were corrected. Evidence: `state/chat_7b_conversation_recovery_2026_08_11/result.json`.
- The 303M R0 evaluator was later classified as an invalid measurement; R1 remains locked.
  Evidence: `state/anima_303m_r0_local_micro_2026_08_12/result.json`.

No model result is promoted solely because transport health passes. Semantic chat, causal controls,
throughput, soak, recovery, and rollback are separate blocking gates.

## Repository boundaries

- `dancinlab/anima` is the only active source repository.
- `cli/`, `core/`, and `anima_py/` own active runtime code.
- `state/` owns registered protocols and result evidence.
- `archive/` is non-runtime provenance.
- Vast.ai owns pod execution; Hugging Face `dancinlab` owns model and dataset custody.

## License

MIT. See `LICENSE`.
