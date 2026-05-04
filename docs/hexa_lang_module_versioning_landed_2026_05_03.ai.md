# hexa-lang module versioning + capability governance landing — 2026-05-03

## TL;DR

hexa-lang stdlib P0/P1 4-module set (`proc`, `json`, `http`, `bytes`)에
governance header (`@version` / `@capabilities` / `@stability` / `@since` /
`@maintainer` / `@priority`) 추가 + Phase 1 spec 작성 완료.
순수 comment-only additive (총 42 LoC 추가, 모듈 로직 0 byte 변경).
F-VERSION-1 falsifier 4/4 PASS (6/6 필드 each).

---

## 1. 결정 — Phase 1 scope lock

| 항목 | 선택 | 거부 |
|---|---|---|
| 적용 범위 | P0/P1 4-module set | 전체 30+ 모듈 (Phase 2로 deferred) |
| 헤더 메커니즘 | comment-only `// @field` | 런타임 `@module(version=...)` attr (Phase 3 speculative) |
| 검증 | manual shell pipeline (F-VERSION-1) | validator 자동화 (Phase 2로 deferred) |
| CHANGELOG | 안 추가 (Phase 1 모두 1.0.0 신규) | 빈 CHANGELOG 블록 추가 |
| 마이그레이션 | 0 (additive comment only) | — |

**근거**: raw#9 STRICT (Mac → hexa only, .py 0 생성) + 모듈 로직 0 변경 +
Phase 1 reviewable diff 유지.

---

## 2. 변경 사항

### 2-1. `/Users/ghost/core/hexa-lang/stdlib/proc.hexa` (P0)

추가된 헤더 (line 6-15):

```hexa
// ── module governance metadata (hexa-lang module versioning spec 2026-05-03) ──
// @version 1.0.0
// @capabilities [proc_spawn_supervised, proc_lease_renew, proc_deregister, proc_kill, proc_alive, proc_reap, proc_run_with_stdin, proc_run_json_bridge]
// @stability stable
// @since 2026-04-25
// @maintainer anima-core
// @priority P0
// Versioning policy: docs/hexa_lang_module_versioning_spec_2026_05_03.md
// Breaking-change rule: bump @version major iff any name in @capabilities is
// removed, renamed, or changes its parameter arity / return-type contract.
```

8개 capability — qmirror engine_aer + anima orchestrator의 known callers.

### 2-2. `/Users/ghost/core/hexa-lang/stdlib/json.hexa` (P1)

```hexa
// @version 1.0.0
// @capabilities [json_stringify_value, json_dump_pretty, json_object_set, json_array_push]
// @stability stable
// @since 2026-05-03
// @maintainer anima-core
// @priority P1
```

4개 capability — write-side helpers only (read-side는 별도 모듈
`stdlib/json_object.hexa`).

### 2-3. `/Users/ghost/core/hexa-lang/stdlib/http.hexa` (P1)

```hexa
// @version 1.0.0
// @capabilities [http_get_with_headers, http_get_with_headers_status]
// @stability stable
// @since 2026-05-03
// @maintainer anima-core
// @priority P1
```

2개 capability — header-required GET path only (no-headers는 별도 모듈
`stdlib/net/http_client`).

### 2-4. `/Users/ghost/core/hexa-lang/stdlib/bytes.hexa` (P1)

```hexa
// @version 1.0.0
// @capabilities [bytes_to_uint64, bytes_to_uint64_le, bytes_to_uint32, int_from_hex, hex_encode_bytes, uint64_to_unit_float]
// @stability stable
// @since 2026-05-03
// @maintainer anima-core
// @priority P1
```

6개 capability — qmirror sampler.hexa per-shot fold path 사용.

### 2-5. `/Users/ghost/core/anima/docs/hexa_lang_module_versioning_spec_2026_05_03.md`

11 sections, 347 LoC. 핵심:

- §2 Header Format — 7 필드 schema + comment-only invariant
- §3 Versioning Rules — semver bump table (minor: add fn / patch: bug fix /
  major: rename·remove·narrow type)
- §4 Capability Discovery — Phase 1 manual grep / Phase 2 validator /
  Phase 3 speculative import-time check
- §5 Deprecation Lifecycle — `experimental → beta → stable → deprecated →
  removed` 5-state
- §6 CHANGELOG Convention — per-module reverse-chrono inline block
- §7 Falsifier F-VERSION-1 — shell pipeline with explicit pass criterion
- §9 Caveats (raw#10 honest C3) — 4-caveat block (§5 below)
- §11 Out-of-Scope — 6개 명시적 non-goals

---

## 3. F-VERSION-1 검증 (Phase 1 falsifier)

### 명령

```bash
for f in proc.hexa json.hexa http.hexa bytes.hexa; do
  echo "=== $f ==="
  grep -cE '^// @(version|capabilities|stability|since|maintainer|priority)' \
    /Users/ghost/core/hexa-lang/stdlib/$f
done
```

### 결과

```
=== proc.hexa ===
6
=== json.hexa ===
6
=== http.hexa ===
6
=== bytes.hexa ===
6
```

**판정**: PASS (4/4 모듈 × 6/6 필드 — 모두 양성)

---

## 4. 정합 결과

| 항목 | Pre | Post |
|---|---|---|
| stdlib P0/P1 governance header 보유 모듈 | 0 | 4 |
| spec 문서화 | 없음 | 347-LoC spec + 11 sections |
| 모듈 로직 변경 byte | — | **0** (pure comment additions) |
| 총 추가 LoC (4 모듈 합산) | — | 42 |
| 마이그레이션 | — | 0 |
| 신규 .py 생성 | — | 0 (raw#9 STRICT) |
| Validator | — | deferred to Phase 2 |

---

## 5. caveats (raw#10 honest C3)

- **C1** — semver subjective on early-stage stdlib. §3.1 bump rules는
  contract surface가 안정된 stdlib를 가정하지만 hexa-lang stdlib는
  6개월 미만의 신생. 첫 실제 "API mistake to correct" 이벤트에서
  major bump (규칙대로, but disruptive) vs patch + 문서화 (실용적, but
  rule violation) 사이의 judgment call이 발생할 것. Phase 2 cycle에서
  실제 첫 major-bump 이벤트로 worked example 추가 예정.

- **C2** — capabilities list may drift from actual public surface.
  Phase 1은 validator 0 — `@capabilities`는 maintainer 수동 관리.
  새 `pub fn` 추가 + `@capabilities` 업데이트 누락 = silent drift.
  Phase 2 validator (§4.2)가 gap을 닫을 때까지 list는 **advisory,
  not authoritative**. ground truth가 필요한 consumer는 source file의
  `pub fn`을 직접 grep해야 함.

- **C3** — validator deferred to Phase 2. spec을 "convention"에서
  "enforced contract"로 전환하는 단일 자동화 (`tool/hexa_module_version_validate.hexa`)
  는 Phase 1 diff를 pure header-additions로 reviewable 유지하기 위해
  defer. Phase 2가 land될 때까지 F-VERSION-1은 manual shell pipeline
  (§7)으로 검증. 영구 상태 X — 다음 cycle의 #1 deliverable.

- **C4** — ratification with hexa-lang core team pending. spec은
  anima/qmirror consumer 관점에서 작성. hexa-lang core maintainer 팀의
  ratification 미수신. 구체적 pending 항목: (a) `@version`/`@capabilities`
  네이밍 합의 (vs `@semver`/`@exports`), (b) comment-only 수용 여부
  (vs 미래 runtime `@module(version=...)` attr 확장), (c) §5 deprecation
  lifecycle (대안: deprecated import hard-fail vs soft-warn). Phase 1은
  단독 ship — core team이 다른 schema로 ratify하면 sed 1-pass로 4개
  헤더 마이그레이션 가능 (comment-only delta).

---

## 6. 잔존 작업 (next cycle 후보)

| 항목 | priority | rationale |
|---|---|---|
| Phase 2 — `tool/hexa_module_version_validate.hexa` | HIGH | C2 + C3 동시 해결, F-VERSION-1 자동화 |
| Phase 2 — P2 모듈 헤더 확장 (~26 modules) | MEDIUM | optim, qrng_anu, collections, parse, math, string, yaml, portable_fs, consciousness, nn, … |
| Phase 2 — `state/hexa_stdlib_manifest.json` 자동 생성 | MEDIUM | validator side-effect, downstream tooling 입력 |
| hexa-lang core team ratification 요청 | MEDIUM | C4 close, schema 잠금 |
| 첫 실제 major-bump worked example 문서화 | LOW | C1 close, post-event 진행 |
| Phase 3 — `use ... require version >= ...` 런타임 hook | LOW | speculative, runtime.c 변경 필요 |

---

## 7. 산출물 (artifact ledger)

| 산출물 | 경로 |
|---|---|
| 수정된 stdlib P0 모듈 | `/Users/ghost/core/hexa-lang/stdlib/proc.hexa` (+11 LoC) |
| 수정된 stdlib P1 모듈 1 | `/Users/ghost/core/hexa-lang/stdlib/json.hexa` (+10 LoC) |
| 수정된 stdlib P1 모듈 2 | `/Users/ghost/core/hexa-lang/stdlib/http.hexa` (+10 LoC) |
| 수정된 stdlib P1 모듈 3 | `/Users/ghost/core/hexa-lang/stdlib/bytes.hexa` (+11 LoC) |
| Spec 문서 | `/Users/ghost/core/anima/docs/hexa_lang_module_versioning_spec_2026_05_03.md` (347 LoC) |
| Marker | `/Users/ghost/core/anima/state/markers/hexa_lang_module_versioning_landed.marker` |
| Handoff (이 문서) | `/Users/ghost/core/anima/docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md` |

---

## 8. raw 준수 status

- **raw#9 STRICT** (Mac → hexa only): 통과 — 신규 `.py` 0, 4개 `.hexa`
  순수 comment additions, 1 `.md` spec, 1 `.marker`, 1 `.md` handoff
- **raw#10** (honest C3): 통과 — §5 4-caveat 블록 (C1 semver / C2 drift /
  C3 validator defer / C4 ratification pending)
- **raw#15**: 통과 — Mac 로컬 $0, fail-fast 패턴 영향 없음 (comment additions only)
- **$0 cost**: 통과 — Mac local edits만, RunPod / API 호출 0
