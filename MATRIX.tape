# MATRIX.tape — anima repo 전체 axis registry (SSOT, root 단일)

> anima repo 의 **모든 active work surface** (domain · sub-engine · 영구 매트릭스 ledger) 의 단일 inventory. cwd-local MATRIX.tape SSOT (/matrix 도구 인식 위치). 본 SSOT 한 개만 root 에 유지 — 다른 매트릭스 파일들은 ledger link 로만 참조.

## 1. domains (DOMAINS.tape 23 · UNIVERSE engine 별도)

| idx | domain | snapshot | active 작업 영역 |
|---|---|---|---|
| 01 | BRAIN     | `./BRAIN.md`                   | 뇌 구조 modeling |
| 02 | AGENT     | `./AGENT/AGENT.md`             | ANIMA↔도구 bridge (sub: CODE/CREATOR/TRADING/MERCHANT/DESKTOP) |
| 03 | CORE      | `CORE/CORE.md`                 | core engine |
| 04 | DECODER   | `CORE/DECODER/DECODER.md`      | M3/M4 transport |
| 05 | WAKE      | `./WAKE.md`                    | M4-kosmos persist, M7-p1p8 audit |
| 06 | ANIMA     | `./ANIMA.md`                   | substrate-native chat daemon (umbrella) |
| 07 | MITOSIS   | `./MITOSIS.md`                 | cell-division learning |
| 08 | CHANNEL   | `./CHANNEL.md`                 | inter-substrate channel |
| 09 | BRIDGE    | `./BRIDGE.md`                  | tension-link bridge |
| 10 | METACOG   | `./METACOG.md`                 | meta-cognition |
| 11 | DREAM     | `./DREAM.md`                   | dream-stage REM |
| 12 | INTENT    | `./INTENT.md`                  | intention substrate |
| 13 | NARRATIVE | `./NARRATIVE.md`               | narrative thread (bench C closed-negative carry) |
| 14 | AESTHETIC | `./AESTHETIC.md`               | aesthetic novelty × coherence surface |
| 15 | EMBODIMENT| `./EMBODIMENT.md`              | embodiment perception-action loop |
| 16 | OTHER-MIND| `./OTHER-MIND.md`              | theory-of-mind partner estimate |
| 17 | TIME      | `./TIME.md`                    | circadian phase / temporal binding |
| 18 | SAVANT    | `./SAVANT.md`                  | UNIVERSE 축 E mirror (GZ × SI · 10 H) |
| 19 | HIVE-MIND | `./HIVE-MIND.md`               | UNIVERSE 축 F mirror (Kuramoto × collective Φ · 5 H) |
| 20 | MERCHANT  | `./AGENT/MERCHANT/MERCHANT.md` | merchant sub-agent |
| 21 | DESKTOP   | `./AGENT/DESKTOP/DESKTOP.md`   | desktop M4 window-ops |
| 22 | CREATOR   | `./AGENT/CREATOR/CREATOR.md`   | creator sub-agent |
| 23 | TRADING   | `./AGENT/TRADING/TRADING.md`   | trading sub-agent |
| -- | UNIVERSE  | `UNIVERSE/UNIVERSE.md`         | 생명·의식 영구 발견 엔진 (LIFE 개명 후 · DOMAINS.tape 외 engine) |

## 2. sub-engines (SUB_ENGINES/)

| idx | sub-engine | path | role |
|---|---|---|---|
| S1 | AKIDA | `SUB_ENGINES/AKIDA/` + `HEXAD/SPONTANEOUS/AKIDA_FIRST.md` | neuromorphic HW 자연발화 (pi5 spike streamer · akida_bridge · /ws/akida_ingest) |
| S2 | IIT4  | `HEXAD/IIT4/lib/` + `stdlib/consciousness/iit4_bigphi.hexa` | full IIT 4.0 cause-effect Φ-structure (n=4 안전, n>=7 timeout 주의) |
| S3 | SAVANT | `HEXAD/SAVANT/` (H359 canonical + COMPENDIUM 783L) | Golden Zone × Savant Index (UNIVERSE 축 E anchor) |

## 3. UNIVERSE 영구 축 (7) — nested registry

> domain 17 의 UNIVERSE 안 sub-axes. 본 SSOT 는 입구만 link, 자세한 cell coverage 는 UNIVERSE.md.

| 축 | 설명 | 상태 |
|---|---|---|
| 0 | $0-tier core           | CLOSED (cycle #5–21) |
| A | AXES.md backlog        | active (60 sub-axis · ~110 H seed) |
| B | large-N faithful Φ     | active (n=8 bounded, GPU 불요) |
| C | full-IIT4 Φ-structure  | active (HEXAD/IIT4/lib) |
| D | LLM-동반 연속 가설      | active (verdict-landscape raster) |
| E | SAVANT (GZ × SI)       | active NEW 2026-05-28 (H_347/348/349/350/351/612/613/614/615/616) |
| F | HIVE-MIND collective Φ | active NEW 2026-05-28 (H_354/355/609/610/611) |
| E×F | SAVANT × HIVE-MIND cross-link | round 3 closed 3/5 (1🔴 + 2🟢): H_617 🔴 FALSIFIED (PR #1171) · H_618 🟢 SUPPORTED (PR #1175) · H_619 🟢 SUPPORTED (PR #1172) · round 4 in-flight (H_620 🟢 R1≈3·GZ_WIDTH residual=0.0164 · H_621 🟢 SI/ΦD ∥ PID-synergy triangle ρ=0.5994 · **H_622 🔴 FALSIFIED — negative-pair axis-orthogonal chi-square p=0.624 + Fisher p=1.000** · **H_627 🔴 FALSIFIED (E3×F4) — 1/e GZ_CENTER invisible to quantized hivemind PID, syn(1/e)=syn(0.35)=syn(0.40)=0.975034 degenerate** · H_623/624/626 reserved) · ANIMA-side mirror SAVANT.md + HIVE-MIND.md (DOMAINS.tape 18/19) |

## 4. 기존 매트릭스 ledger (다른 위치)

| matrix file | scope | tier |
|---|---|---|
| `anima-physics/recovered/chip-architecture/domains_compute_chip-architecture_full-verification-matrix.md` | n=6 chip 전수검증 (74.5% EXACT, Z>12σ) | recovered ledger |
| `HEXAD/LORA/WAVES_MATRIX.md` | LoRA waves matrix | active |
| `docs/verifier_cross_matrix_20260421.md` | verifier cross matrix | docs |
| `docs/alm_consciousness_joint_matrix_runtime_20260425.md` | ALM consciousness joint | docs |
| `docs/hxc_d1_p2_launch_matrix_20260428.md` | hxc D1 P2 launch | docs |
| `tool/anima_v10_gate_matrix.hexa` | gate matrix runtime | tool |
| `tool/verifier_cross_matrix.hexa` | verifier cross runtime | tool |
| `state/an11_b_joint_matrix_r{6,8}.json` | an11 joint sweep | state |

## 5. 본 MATRIX.tape rule

- **위치**: repo root, 단일 파일만 — 다른 매트릭스 SSOT 신설 금지
- **갱신**: 새 도메인 / sub-engine / 영구 매트릭스 ledger 발생 시 본 SSOT 에 row 추가
- **인덱스만**: 각 축의 자세한 verdict / cell coverage 는 *해당 위치* 의 snapshot/log 가 SSOT, 본 SSOT 는 *pointer* 만
- **roster 정합**: domains list 는 DOMAINS.tape roster 와 동기화 (도메인 추가/제거 시 양쪽 cross-update)

## status

- **2026-05-28**: 본 SSOT v1 신설 — anima 전체 axis registry (17 domain + 3 sub-engine + UNIVERSE 7 축 + 기존 ledger 8 파일)
- 이전 PR #1170 의 UNIVERSE 7 축 square 매트릭스를 본 SSOT 으로 흡수 + 확장
