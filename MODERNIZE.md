# MODERNIZE — current state

@goal: anima 의 **active** `.hexa` 가 현 hexa-strict 에서 build pass 하도록 stale codegen-break 제거 — explicit `main()` 호출(auto-invoke conflict) · `.length`→`.len()` · `nan`/`inf` reserved-value shadow · `fabs(` broken-builtin 오용(→`abs`) · 기타. archive/legacy/state-snapshot 은 scope 제외 (frozen 이력).

## 왜 (배경)

STDLIB M5/abs_f 루프 중 발견: 레거시 anima `.hexa` 가 **parse 는 되지만 codegen 에서 build-fail** 하는 게 광범위. 근본 = 이번 세션에 **interpreter retire** — interp-era 코드(explicit `main()` + top-level)가 compiled hexa-strict 에서 깨짐. #426/#427 broken `fabs` 출하 (parse≠build, CI 미빌드)를 per-path baseline infra(#801)가 노출.

## Scope

- **in scope**: build-fail 하는 active `.hexa` (lib · tool · serving · training · bench) 를 build pass 시키기. 각 파일의 **모든** break 제거 (복수 동거).
- **out of scope**: `archive/` · `*_legacy*` · state-snapshot · byte-equal frozen 결과 변경.

## 검증 원칙 (per-path baseline)

- 파일별 **build pass** 1차 기준. deterministic 출력은 build-run-diff(fix 전후 stdout byte-identical · `stdlib/verify/byte_equal` #801 기반)로 동작 보존.
- ⚠ **blanket per-class sed 금지** — `.length` 등이 **JS/HTML 문자열 리터럴 안**에 있으면 false-positive (avatar_webtoon `seq.length` 사례). 실 hexa 구문만 수정, 문자열 내용 보존.

## Census

| break-class | raw | active (archive/legacy/state 제외) | fix |
|---|---|---|---|
| explicit `main()` | 807 | **719** | `^main()` 줄 제거 (auto-invoke; `@manual_main` 예외 유지) |
| `fabs(` 오용 | 189 | 188 | `fn fabs` def 없으면 `→abs` |
| `.length` | 6 | 6 | ⚠ 다수 **JS-string false-positive** — 실 hexa `.length`만 `→.len()` |
| `nan`/`inf` shadow | 1 | 1 | reserved → rename |

⚠ active 719 explicit-main = **interp-era 레거시 대량 마이그레이션** (multi-session). 6 `.length` 파일 전부 explicit-main 동반 (single-break 없음 → per-file 단위).

## Progress milestones

- [x] M1 survey — active-dir census (719 explicit-main · 188 fabs · 6 .length · 1 nan) + `.length` false-positive 발견
- [x] M2 (선례) fabs 오용 sweep — #429 (6 files fabs→abs, build-verified)
- [x] M6-first `serving/avatar_webtoon.hexa` — main-fix → build+run PASS (.length=JS-string 보존). per-file modernize 패턴 확립
- [ ] M3 `.length`→`.len()` — 실 hexa `.length`만 (string false-positive 제외, per-file)
- [ ] M4 nan/inf shadow rename (1 file)
- [ ] M5 explicit-main sweep — active 719 (interp-era · per-file build-verify · multi-session batch)
- [ ] M6 per-file 완전-modernize — lib/tool/serving 우선, build pass 까지

## Honest limits

- L1: scope 大 (active 719 explicit-main) — multi-session 캠페인. 단일 턴 소진 불가.
- L2: 한 파일 복수 break 동거 → per-file 단위 (단일-클래스 sweep 만으론 build 안 됨).
- L3: blanket per-class 치환 위험 (문자열-리터럴 false-positive) — per-file 신중 + per-path baseline 가드.
- L4: byte-equal frozen(PHI/LIFE) 값 변경 금지.

## Cross-link

- STDLIB.md — fabs 발견 모태 · `stdlib/verify/byte_equal`(#801) infra
- #429 fabs→abs 선례 · #428 verify byte_equal_f64 retrofit
- hexa-lang #785 (g59) — "CI 가 stdlib/POC 미빌드" 갭 = stale 출하 근본
