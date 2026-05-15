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
| SAVANT | `SAVANT.tape` + `SAVANT-TOOL.tape` + 4× `tool/anima_savant_*.hexa` + `anima-engines/savant_phi.hexa` | [`HEXAD/SAVANT/`](HEXAD/SAVANT/) (9 파일 + COMPENDIUM 783L + Π 증명 + H359, PR #85) |

자세한 내용은 [HEXAD/README.md](HEXAD/README.md) + [HEXAD/INDEX.md](HEXAD/INDEX.md) 참고.
