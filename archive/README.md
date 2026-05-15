# archive/ — substrate tapes DEPRECATED (2026-05-16)

> User directive 2026-05-16: `"아카이브 폴더만들어서 보관해줘 AXIS, HYPOTHESIS, PHILOSOPHY, MAIN, CLM, VERIFY, NEXT, REBORN 등"` + 결정게이트 `"deprecate (HEXAD 외 substrate 폐기 신호)"`.

이 디렉토리는 anima architecture 의 **이전 verification substrate** 가 보관된 곳입니다. 2026-05-16 reorg 로 anima 의 primary architecture 가 `HEXAD/` 트리로 통합되면서, 이전 root-level 의 substrate tapes 가 **deprecated** 상태로 전환됨.

## deprecation 의미

- ✅ **historical evidence anchor** — 과거 verdicts, fire cycles, 검증 결과 등은 **그대로 유효**. 인용 + 검토 OK.
- ❌ **future 작업 entry-point 아님** — 새 verdict / 가설 / verification 진행은 `HEXAD/` 트리 안에서 (per-module SSOT + integration entry).
- ⚠️ **AGENTS.tape governance + memory references** — 이 tapes 의 옛 root 경로 가리키는 cross-link 잔존. 텍스트는 valid (historical reference) but path 는 archive/ 로 갱신 필요한 곳도 있음 (점진적 cleanup carry).

## 보관된 파일 (15)

| 파일 | 이전 역할 | superseded by |
|---|---|---|
| `AXIS.tape` + `AXIS.log.tape` + `AXIS-V1.tape` | 9-axis SUPPORTED 150 entries inventory | `HEXAD/<X>/HEXAD-<X>.tape` 모듈별 spec + verification |
| `HYPOTHESIS.tape` | 318 가설 inventory | `HEXAD/<X>/` per-module hypothesis sets (future) |
| `PHILOSOPHY.tape` + `.log.tape` | 8 principles + verdict ledger | `HEXAD/PLAN.md` + 모듈별 principle 매핑 (future) |
| `MAIN.tape` + `MAIN-TEMP.tape` | 가설 verdict 4-class SSOT | `HEXAD/<X>/HEXAD-<X>.tape *_blue_status` per-module verdict |
| `CLM.tape` + `.log.tape` | .clm v1/v2/v3 fire SSOT + §V-CLM-HEXAD-MANDATE | `HEXAD/PLAN.md` Phase 5-6 fire roadmap + autograd RFC trigger |
| `VERIFY.tape` | verification stages | `HEXAD/integ_test.hexa` + Python `state/verify_hexad_*/` battery |
| `NEXT.tape` + `.log.tape` | next-task tape | `HEXAD/PLAN.md` 진행 로그 (append-only) |
| `REBORN.tape` + `.log.tape` | §0.5 학습=분열 단일 연속체 philosophy | HEXAD §hexad_condition_lineup §mitosis_two_axis (HEXAD.tape + HEXAD/MITOSIS.tape) |

## 보존되는 root SSOT (이동 X)

- `HEXAD.tape` — 통합 arch SSOT (AGENTS.tape 직접 참조 + HEXAD/ 트리의 모-spec)
- `AGENTS.tape` — anima governance (project-level CLAUDE.md, symlink target)
- `CLAUDE.md` — symlink → AGENTS.tape
- `/INDEX.md` — redirect stub (HEXAD/INDEX.md 으로 anchor)
- 기타 도메인 tapes (`ANIMA-AGENT`, `ANIMA-SENSES`, `BENCHMARK`, `CHAT`, `CHAT-QUALITY`, `ARCH-CLASS` 등) — 이 reorg 의 명시적 deprecate 대상 아님 (carry)

## 사용 시 가이드 (future sessions)

- **인용**: 과거 verdicts/cycles 참조 시 `archive/<X>.tape` 경로로 명시. evidence anchor 로 valid.
- **신규 작업**: HEXAD/ 트리 안에서 진행. 새 verdict-bearing 가설은 모듈별 (`HEXAD/<X>/HEXAD-<X>.tape *_blue_status` 등) 에 등재.
- **cross-link 점진 cleanup**: 다른 곳에서 이 tape 들의 옛 root 경로 참조 발견 시 archive/ 갱신 또는 HEXAD/ counterpart 로 redirect.

## related PRs

- #78 — HEXAD/ canonical hexa-native tree 신설
- #79 — cross-file wire LANDED + PLAN.md
- #80 — task (c) ckpt fire DEFERRED + hexa-lang autograd RFC trigger spec
- #81 — INDEX.md + 7 HEXAD-<X>.tape + MITOSIS + SAVANT.* → HEXAD/ 안으로
- **#82** (이 PR) — substrate tapes (15) → archive/ deprecate 신호
