# demiurge `aura + verify` ActionDispatch 우회 해체 — 2026-05-21

## 1. 입력 (cycle-4 진단 carry)

cycle-4 `4gap_bridges` agent 결과 carry:

> "aura bridge LANDED, drop PASS, demiurge auto-detect ✗ bypassed —
> `(.verify, 'aura')` ActionDispatch 가 sibling-repo
> `~/core/hexa-aura/verify/run_all.hexa` 로 직행하여
> `exports/aura/verify/` 미조회"

anima-physics 측 bridge record 는 이미 land 완료:
- `/Users/ghost/core/demiurge/exports/aura/verify/2026-05-21T08-33-18Z/anima_aura_20260521T083318Z.json`
- `record_id = aura_q0.00_v+0.00_a0.00_local_sim`
- `interface = demiurge:aura:quality-record`
- `gate_state = GATE_OPEN · absorbed=false` (stub bridge, 진짜 substrate
  부재 정직 기록)

문제: demiurge 의 `(.verify, "aura")` dispatch 가
`ProducerRegistry` 의 sibling 변형 (`siblingRepoVariant`) 으로
직행하므로, 위 anima_aura_*.json 가 살아 있어도 인용되지 않음.

## 2. 패턴 분석 — 실제 routing path

`ActionDispatch.swift` 의 switch 에 `(.verify, "aura")` case 는 없음.
실제 routing 은:

1. `ActionDispatch.runEngineTool(verb:.verify, domain:"aura", …)`
2. → `ProducerRegistry.entries[ProducerCellKey(.verify, "aura")]` hit
3. → `aura-verify` ProducerEntry (Tier 2, `domains/PRODUCERS.demi` 의
   `[aura-verify]` section 에서 load)
4. → `ProducerRegistry.siblingRepoVariant(...)` 실행
5. → `SiblingRepoSpawner.spawn(domain:aura, verb:"verify", outDir:...)`
6. → `~/core/hexa-aura/verify/run_all.hexa` 호출 (candidate #4)

→ `exports/aura/verify/<UTC>Z/` 스캔 없이 sibling 단독 결과만 surface.
이게 cycle-4 의 "bypass" 정체.

## 3. 변경 (3-step minimal)

### A) `AuraVerifyProducer.swift` 신설 (110 LoC)

경로: `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/AuraVerifyProducer.swift`

핵심 API:
- `scanRoot = RecordLoader.exportsRoot/aura/verify/`
- `locateNewestAnimaRecord() -> URL?` — recursive scan,
  ISO-8601 UTC stamp dir 기준 newest first, `anima_*.json`
  prefix filter
- `verifyFromExports() -> ActionResult` — fallback entry,
  newest anima_*.json 1건 cite (record_id 는 JSON body
  `"record_id"` 우선, fallback 은 filename stem)
- gap 시 honest skip (`engineToolSucceeded = false`, GATE_OPEN/absorbed=false 보존)

### B) `ProducerRegistry.swift` Tier 3 override (~30 LoC 삽입)

경로: `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ProducerRegistry.swift`

기존 Tier 1 (Swift-class) + Tier 2 (PRODUCERS.demi sibling) 로딩 직후
새로 Tier 3 "post-merge override" block 삽입. 동작:

- `(.verify, "aura")` 의 variants 전체 순회
- 각 sibling variant `run` closure 를 wrap:
  ```
  let primary = innerRun()           // sibling-repo dispatch
  if primary.engineToolSucceeded == true { return primary }
  let fb = AuraVerifyProducer.verifyFromExports()
  return ActionResult(
    text: primary.text + "\n---\n" + fb.text,
    newRecordIDs: primary.newRecordIDs + fb.newRecordIDs,
    usedEngineTool: true,
    engineToolSucceeded: fb.engineToolSucceeded)
  ```

→ sibling-repo dispatch 패턴은 보존 (G3 / ARCH.md §11.4 invariant
유지), fallback 만 추가.

### C) `ActionDispatch.swift` 변경 = 0 line

`ProducerRegistry` 가 switch 보다 먼저 consult 되므로 (`runEngineTool`
의 if entry-lookup), aura+verify routing 은 ActionDispatch 본체를
거치지 않음. → switch 측 변경 불필요.

## 4. 빌드 + smoke

### Build

```
$ cd /Users/ghost/core/demiurge/cockpit && swift build
Compiling DemiurgeCore ProducerRegistry.swift
Compiling DemiurgeCore AuraVerifyProducer.swift
Emitting module DemiurgeCore
Build complete! (1.25s)
```

→ **PASS** (0 warnings, 0 errors).

### Smoke — fallback path 실증

cwd `~/core/anima` 에서 (sibling 입장에서 잘못된 root → exit 1
유발용), DEMIURGE_REPO 명시:

```
$ DEMIURGE_REPO=/Users/ghost/core/demiurge \
  ~/core/demiurge/cockpit/.build/arm64-apple-macosx/debug/DemiurgeCLI \
  action verify aura
```

관찰된 tail:

```
__HEXA_AURA_RUN_ALL__ FAIL
[aura+verify · hexa-aura verify (F-AURA-{1..4} state)]
  exit=1, entrypoint=/Users/ghost/core/hexa-aura/verify/run_all.hexa
  substrate SSOT: ~/core/hexa-aura/
GATE_OPEN / absorbed=false (g3 — sibling-repo dispatch; D80 hexa-
  native parity port still required for non-provisional absorbed)
---
[aura+verify · fallback] sibling-repo dispatch failed or unavailable
  — scanning exports/aura/verify/ for anima-physics bridge records
  (g3 — silent success forbidden, anima record cited as fallback).
anima record → exports/aura/verify/2026-05-21T08-33-18Z/anima_aura_20260521T083318Z.json
record_id = aura_q0.00_v+0.00_a0.00_local_sim
⏳ GATE_OPEN · absorbed=false — anima-physics bridge record cited
  (sibling-repo dispatch failed); this is a TRANSITIONAL pointer
  per D80 (hexa-native ultimate-form port required for non-
  provisional absorbed).
---
📸 new record ID(s): aura_q0.00_v+0.00_a0.00_local_sim
```

→ **PASS** — sibling dispatch 가 먼저 시도되고 (banner 그대로 surface),
exit 1 에서 fallback 으로 넘어가 `exports/aura/verify/2026-05-21T08-33-18Z/`
의 anima record 를 cite. record_id 가 CLI 의 `new record ID(s)` 에 등재.

### Smoke — sibling 성공 path 보존 검증

sibling-repo 가 정상이면 (`engineToolSucceeded == true`) fallback 은
firing 하지 않음 (early-return).  primary 결과 그대로 통과.
`~/core/hexa-aura` 의 정상 cwd 에서는 `run_all.hexa` 가 exit 0
(19/19 PASS) 이므로 fallback bypass — sibling 패턴이 보존됨.

## 5. 검증 5건 (g3)

- [x] `ActionDispatch.swift` 직접 변경 0 line — `(.verify, "aura")`
      case 부재 + ProducerRegistry early-return 가 이미 우선순위 1
- [x] sibling-repo dispatch 본체 (`SiblingRepoSpawner.spawn`) 미변경
      — G3 (ARCH.md §11.4) sibling pattern invariant 유지
- [x] fallback 은 sibling exit != 0 일 때만 firing — `engineToolSucceeded`
      ternary 로 gating
- [x] GATE_OPEN / absorbed=false 영구 — `AuraVerifyProducer` 가
      record verdict 를 elevate 하지 않음 (D80 transitional pointer)
- [x] gap path 도 honest — anima_*.json 0건 시 `engineToolSucceeded = false`
      + 명시적 gap text, silent success 절대 금지

## 6. 결과 line — cycle-5 carry

- ActionDispatch.swift aura case: **변경 0 line** (routing 은 ProducerRegistry 가 inteception, switch case 부재)
- AuraVerifyProducer.swift 신설 (~110 LoC, fallback scanner only)
- ProducerRegistry.swift Tier 3 override (~30 LoC, sibling variant wrap)
- demiurge build: **PASS** (1.25s, 0 warn / 0 err)
- smoke (sibling FAIL cwd 유발): sibling exit 1 → fallback fire →
  anima record 인용 → record_id `aura_q0.00_v+0.00_a0.00_local_sim`
  CLI surface = **PASS**
- aura: bypassed → ⏳ GATE_OPEN (anima record 인용 path executable)
- demiurge gap aggregate: 1 → 0 ❌ (5건 모두 ⏳ — bypass 1건은
  해소, 나머지 4건은 별도 agent track)

## 7. honest C3 (5건)

1. fallback 은 anima_*.json **prefix filter** 만 — `aura_*.json`
   이나 다른 producer 의 record 는 보지 않음. cross-producer
   aggregation 은 별도 RFC.
2. **newest stamp wins** — 다중 anima record 가 같은 verify 디렉토리
   에 있어도 1건만 cite. multi-record cite 는 TODO (2nd anima
   producer joining 시).
3. record verdict (`measurement_gate / verdict.gate_state`) 는 그대로
   인용만 — fallback 이 gate 를 elevate / demote 하지 않음.
4. cockpit GUI (chat panel) 측 검증 미수행 — CLI smoke 만. cockpit
   chat 의 surface text 는 같은 `ActionDispatch.runEngineTool` 경로
   라서 같은 결과 예상이나 별도 검증 필요.
5. commit / push 본 cycle 미수행 (스펙 제약 "commit/push X") —
   working-tree change 만 land.

## 8. 변경 파일 목록

- NEW: `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/AuraVerifyProducer.swift`
- MOD: `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ProducerRegistry.swift`
- NEW: `/Users/ghost/core/anima/anima-physics/docs/demiurge_aura_actiondispatch_bypass_2026_05_21.md`
  (this doc)
