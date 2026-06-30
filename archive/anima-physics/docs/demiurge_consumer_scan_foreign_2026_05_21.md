# Demiurge Consumer scan-foreign Extension — B1 + B2 (2026-05-21)

> FirmwareVerifyProducer + ComponentVerifyProducer 가 anima-side bridge record
> (`anima_*`, `upduino_*`) 를 canonical record 와 나란히 자동 인용하도록
> scan-foreign 패턴 도입. 직전 G5 firmware/component integration cycle 의
> 미인용 gap 해소.

## 1. 동기

직전 G5 cycle 보고:

- `FirmwareVerifyProducer.swift` 의 record-scan filter
  (`hasPrefix("firmware_verify_")`) 가 너무 좁아서, anima-side 가 동일
  `exports/firmware/verify/<stamp>/` 트리에 떨어뜨린
  `anima_sleep_oscillator_*.json` bridge record 가 cockpit 인용 라인
  (`📸 new record ID(s): …`) 에 누락.
- `ComponentVerifyProducer.swift` 는 canonical 만 emit, sibling 디렉터리의
  `upduino_enclosure_thermal_*.json` 같은 anima-bridge thermal record 를
  완전히 무시 (filter 자체가 없는 구조).

→ 두 producer 모두 **scan-foreign** (= 외부 substrate 가 떨어뜨린
known-prefix record 자동 픽업) 패턴이 필요.

## 2. 설계

### 2.1 Single point of extension

각 producer enum 안에 한 줄 prefix 목록을 노출:

```swift
public static let foreignRecordPrefixes: [String] = [
    "anima_",       // anima-side bridge records (HEXAD physics, etc.)
    "upduino_",     // upduino_enclosure_thermal_* (component only)
    // future: "hexa-aura_", "hexa-sense_", ...
]
```

새 bridge substrate 가 생길 때 한 줄 추가만으로 확장 — 인프라 변경 없음.

### 2.2 Result 타입 plural 화

기존:
```swift
public let newRecordID: String?
```
→ 신규:
```swift
public let newRecordIDs: [String]
public var newRecordID: String? { newRecordIDs.first }   // backward-compat
```

`ActionDispatch.swift` wrapper 는 `r.newRecordID.map { [$0] } ?? []` →
`r.newRecordIDs` 로 단순화. CLI / GUI 콜러 (`newRecordIDs.joined(...)`) 는
이미 plural 처리 중이므로 무변경.

### 2.3 Scan 범위

`exports/<domain>/verify/` 루트 아래의 **모든 timestamp dir** 을 shallow walk
(`root/<stamp>/<prefix>*.json`). 이전 cycle 의 bridge record 도 모두 픽업.
`Set` 으로 dedupe + `sorted()` 로 deterministic 출력 (D26 g_swift_native).

## 3. 변경 파일

### 3.1 `cockpit/Sources/DemiurgeCore/Loaders/FirmwareVerifyProducer.swift`

- `FirmwareVerifyResult.newRecordID: String?` → `newRecordIDs: [String]`
  (+ backward-compat computed `newRecordID`).
- `foreignRecordPrefixes` static (anima_ 우선, 미래 확장 주석).
- `scanCanonicalRecords(in:)` 헬퍼 — 현재 run dir 의 `firmware_verify_*`
  만 픽업.
- `scanForeignRecords(under:)` 헬퍼 — `recordsRoot` 전체에서 foreign prefix
  매칭.
- `runVerify()` 끝에 `let cited = canonical + foreign` + scan-foreign 로그
  라인 추가.

총 약 60 line 신규 / 10 line 변경.

### 3.2 `cockpit/Sources/DemiurgeCore/Loaders/ComponentVerifyProducer.swift`

- `ComponentVerifyResult.newRecordID: String?` → `newRecordIDs: [String]`
  (+ backward-compat).
- `foreignRecordPrefixes` static (anima_ + upduino_).
- `scanForeignRecords(under:)` 헬퍼 (FirmwareVerify 와 동일 시그니처).
- 8 곳 `newRecordID: nil` → `newRecordIDs: []` (실패 path).
- 성공 path: `let cited = [recordId] + foreign` 후 `newRecordIDs: cited`
  + scan-foreign 로그 라인.

총 약 50 line 신규 / 9 line 변경.

### 3.3 `cockpit/Sources/DemiurgeCore/Loaders/ActionDispatch.swift`

- `runFirmwareVerify()`: `r.newRecordID.map { [$0] } ?? []` →
  `r.newRecordIDs`.
- `runComponentVerify()`: 동일 단순화.

2 wrapper, 각 1 line 변경.

## 4. Build + Smoke 결과

### 4.1 Build

```
cd /Users/ghost/core/demiurge/cockpit && swift build
→ Build complete! (4.37s)
```

기존 ComponentView3D.swift Sendable 경고 외 신규 경고/에러 없음.

### 4.2 B1 Smoke — firmware verify

```
$ swift run DemiurgeCLI action verify firmware
…
[firmware+verify] scan-foreign cited 1 bridge record(s):
    anima_sleep_oscillator_20260521T083241Z
[firmware+verify] record dir: …/exports/firmware/verify/2026-05-21T09-29-42Z
GATE_OPEN / absorbed=false (g3)
---
📸 new record ID(s): firmware_verify_20260521T092942Z,
                     anima_sleep_oscillator_20260521T083241Z
```

✓ canonical `firmware_verify_*` + foreign `anima_sleep_oscillator_*` 동시 인용.

### 4.3 B2 Smoke — component verify

```
$ swift run DemiurgeCLI action verify component
…
[component+verify] scan-foreign cited 1 bridge record(s):
    upduino_enclosure_thermal_20260521T083931Z
---
📸 new record ID(s): component_verify_20260521T092948Z,
                     upduino_enclosure_thermal_20260521T083931Z
```

✓ canonical `component_verify_*` + foreign `upduino_enclosure_thermal_*`
동시 인용.

## 5. Key learning

1. **scan-foreign 패턴 일반화** — `<Domain>VerifyProducer.foreignRecordPrefixes:
   [String]` static + `scanForeignRecords(under:)` 헬퍼 = 4-line 추가만으로
   임의 도메인 producer 가 외부 substrate 의 bridge record 를 자동 인용 가능.
   (RtscVerifyProducer / SpaceVerifyProducer 등 13 sibling producer 모두
   동일 hex-line 추가로 확장 가능.)

2. **Plural-first API** — `newRecordID: String?` → `newRecordIDs: [String]`
   + computed singular backward-compat. ActionDispatch 가 이미 plural 처리
   하므로 API surface 변경 비용 ≈ 0.

3. **g3 honesty 유지** — scan-foreign 은 bridge record ID 만 surface, 그
   gate/absorbed flip 은 record 자체의 verdict 를 따른다 (producer 코드가
   임의로 closure 안 함). anima_sleep_oscillator + upduino_enclosure_thermal
   모두 `GATE_OPEN absorbed=false` 인 채로 인용됨.

## 6. 다음 follow-up

- **13 sibling producer (Energy/Mobility/Space/Bot/Rtsc/Scope/Fusion/SSCB/
  Cern/Matter/Antimatter/Chip/…) 도 동일 prefix list 추가** — 한 sweep
  PR 로 정리 가능 (each ≈ 10-line diff).
- **`foreignRecordPrefixes`  를 cockpit-wide 공통 상수로 추출** —
  현재는 producer 별 중복; 도메인-특화 prefix (e.g. `upduino_` only for
  component) 때문에 즉시 통합은 보류.
- **anima 쪽 bridge producer convention 명문화** — `exports/<domain>/<verb>/
  <stamp>/<anima|upduino|hexa-*>_<thing>_<utc>.json` schema 를 anima-physics
  side AGENTS.md 에 추가하여 demiurge consumer 와의 contract 를 코드 밖에서
  보장.
- **Test 추가** — `ComponentVerifyProducerTests.swift` 부재. scan-foreign
  unit test (fixture dir + `foreignRecordPrefixes` 분기) 추가 시 회귀 방어.

## 7. 산출 인덱스

- `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/FirmwareVerifyProducer.swift`
  (변경)
- `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ComponentVerifyProducer.swift`
  (변경)
- `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ActionDispatch.swift`
  (변경 — 2 wrapper)
- `/Users/ghost/core/demiurge/exports/firmware/verify/2026-05-21T09-29-42Z/firmware_verify_20260521T092942Z.json`
  (B1 smoke 산출 canonical record)
- `/Users/ghost/core/demiurge/exports/component/verify/2026-05-21T09-29-48Z/component_verify_20260521T092948Z.json`
  (B2 smoke 산출 canonical record)
- 본 doc `/Users/ghost/core/anima/anima-physics/docs/demiurge_consumer_scan_foreign_2026_05_21.md`

## 8. 비용 / Honesty

- Cost: $0 (Mac local swift build + smoke, ~5s build + ~1s × 2 smoke).
- Honesty (g3): scan-foreign 은 record ID 인용 layer 한정 — record 의
  measurement_gate / absorbed flag 는 그대로 보존, demiurge consumer 가
  임의로 closure 하지 않는다.
- working-tree only, commit/push 없음 (anima 측 + demiurge 측 모두).
