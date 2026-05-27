# INDEX.md — moved to [`HEXAD/INDEX.md`](HEXAD/INDEX.md)

> User directive 2026-05-16 reorg: anima architecture index 를 HEXAD/ 트리 안으로 통합.
> 이 root stub 은 backward-compat (다른 tape/memory 에서 `INDEX.md` 경로 가리킬 때 navigate 가능).

## 새 layout

| 항목 | 이전 위치 (root) | 새 위치 (HEXAD/ 트리) |
|---|---|---|
| INDEX | `INDEX.md` | [`HEXAD/INDEX.md`](HEXAD/INDEX.md) |
| 모듈별 spec | `HEXAD-{C,D,S,W,M,E,BRIDGE}.tape` | `HEXAD/{C,D,S,W,M,E,BRIDGE}/HEXAD-<X>.tape` |
| 통합 spec | `HEXAD.tape` | [`HEXAD.tape`](HEXAD.tape) (root 유지 — AGENTS.tape 직접 참조) |
| 성장축 | `MITOSIS.tape` | [`HEXAD/MITOSIS/`](HEXAD/MITOSIS/) (서브폴더 — `MITOSIS.tape` + `mitosis.hexa` scaffold + README) |
| TENSION-LINK | `TENSION-LINK.tape/.log.tape` + `training/tension_link_*.hexa` (5) + `tests/test_tension_link*.hexa` (2) + `bench/bench_tension_link.hexa` + `experiments/verify_tension_link.hexa` + `docs/tension_link_*.md` (4) | [`HEXAD/TENSION-LINK/`](HEXAD/TENSION-LINK/) (17 파일 + README, ASCII topology + 100% verified measured + Noether proof) |
| VOICE | `VOICE.tape/.log.tape` + `.roadmap.voice` + `anima-voice/` (corpus-free 63) + `hexa-senses/voice/` (31) + `tool/anima_voice_*.{hexa,sh}` + `serving/voice_*.hexa` + `tests/test_voice_synth.hexa` + `docs/anima_speak_*.ai.md` | [`HEXAD/VOICE/`](HEXAD/VOICE/) (~2.4M + README — formulaic 발성 도구 NOT 학습 모델, F-VOICE 5/5 + F-VOICE-TOOL 5/5. 학습/eval corpus scrub → `_voice_corpus_local/`) |
| CHAT | `CHAT.tape/.log` + `CHAT-QUALITY.tape/.log` + `.roadmap.chat_cap_emergence_pivot` + `anima_chat.hexa` (2845 LoC) + `anima_chat_aot.hexa` + `anima_chat.py` + `tool/anima_chat_*.hexa` (8) + `tests/test_chat*.hexa` (3) + `docs/anima_chat_*.md` (24) | [`HEXAD/CHAT/`](HEXAD/CHAT/) (44 git mv + README — 6-module 통합 interaction entrypoint, anima_chat 24L 21/21 byte-parity, ★ inter-module wiring 아키텍처 조건 ledger W1-W9 5/9 ✅) |
| SAVANT | `SAVANT.tape` + `SAVANT-TOOL.tape` + 4× `tool/anima_savant_*.hexa` + `anima-engines/savant_phi.hexa` | [`HEXAD/SAVANT/`](HEXAD/SAVANT/) (9 파일 + COMPENDIUM 783L + Π 증명 + H359, PR #85) |

자세한 내용은 [HEXAD/README.md](HEXAD/README.md) + [HEXAD/INDEX.md](HEXAD/INDEX.md) 참고.
