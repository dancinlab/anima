# demiurge materials producer integration — Step 1 (anima 측 bridge LANDED + 첫 composite record drop, D17 consumer-pointer)

> anima `demiurge_materials_bridge.py` 를 demiurge materials verify
> consumer-side composite emitter 로 wire 하고 첫 end-to-end record 를
> demiurge exports/ 에 drop 한 cycle.
> Date: 2026-05-21
> Predecessor: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.1`
> (materials 행이 ⏳ no producer — 라우팅 미스 였던 시점)
> Sibling: `anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
> (brain Step 1 동일 패턴)

## §1 GOAL

demiurge `materials` 도메인의 verify gap 을 anima 측에서 **D17 consumer-
pointer 패턴 composite-emitter** 로 메우는 **Step 1**.

- **Before**: `demiurge cli action verify materials` → "엔진 미배선 ·
  ActionDispatch `(.verify, "matter")` 부재 · `PRODUCERS.demi` 에
  `matter-verify` 항목 없음. D17 = demiurge 는 matter 의 pointer/consumer,
  SSOT 는 `~/core/hexa-matter/`. exports/materials/ 디렉터리 자체 부재."
- **After (this cycle)**: anima 측 composite-emitter skeleton + 첫 record
  dropped under `~/core/demiurge/exports/materials/verify/<UTC>Z/`.
  demiurge `cli action verify materials` 가 본 record 를 **자동 감지·
  파싱·인용** (record_id / gate_state / hexa_matter exit / 모든
  scope_caveats 포함). consumer 엔진 (`MatterVerifyProducer.swift`) 신설은
  별도 cycle.
- **Status delta**: materials row `⏳ no producer (라우팅 미스)` →
  `⏳ GATE_OPEN (anima-bridge + hexa-matter pointer)`.

이번 cycle 은 **(a) D17 consumer-pointer 패턴을 anima 측에서 명시
materialize + (b) 3 anima substrate composite + hexa-matter sibling
pointer 통합 + (c) 첫 record drop + (d) demiurge × anima 양방향 path
검증**까지. 실 material-property 측정·oracle parity 는 hexa-matter 측
별도 cycle (owner SSOT) + demiurge consumer 별도 cycle (gating engine).

## §2 D17 consumer-pointer 패턴 명시

본 cycle 의 핵심 architectural 결정 — **demiurge ≠ hexa-matter** 의
역할 분리:

```
┌─────────────────────────────────────────────────────────────┐
│  hexa-matter (OWNER SSOT)                                    │
│  ~/core/hexa-matter/                                         │
│   - 16/16 verb spec docs (verify/spec_presence.hexa)         │
│   - n=6 lattice closure (verify/lattice_arithmetic.hexa)     │
│   - NIST/CRC/Hales anchors (verify/real_limits_anchor.hexa)  │
│   - scoreboard cross-check (verify/closure_consistency.hexa) │
│   - 모든 material property 의 진실 source                    │
└────────────────────────┬────────────────────────────────────┘
                         │ exit code + closure pass/fail
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  anima-physics (COMPOSITE CONSUMER)                          │
│  ~/core/anima/anima-physics/tool/demiurge_materials_bridge.py│
│   - hexa-matter exit code 인용 (pointer, no auto-run)        │
│   - memristor TiO2 measurement (§188 5/5 PASS)              │
│   - thermodynamic Langevin (5/5 PASS)                       │
│   - superconducting provenance (deprecated honesty)          │
│   - composite record emit → demiurge exports/                │
└────────────────────────┬────────────────────────────────────┘
                         │ record drop
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  demiurge (TYPED-INTERFACE CONSUMER)                         │
│  ~/core/demiurge/                                            │
│   - cli action verify materials → auto-cite anima record     │
│   - MatterVerifyProducer.swift 신설 = 별도 cycle             │
│   - oracle parity gating = 별도 cycle                        │
└─────────────────────────────────────────────────────────────┘
```

이 분리는 brain bridge (anima 가 owner + producer 양쪽) 와의 핵심 차이
— materials 는 anima 가 **owner 가 아님**, hexa-matter 가 owner. anima
는 자신의 consciousness-analog substrate (memristor/thermo/supercond) +
hexa-matter pointer 를 묶어 demiurge consumer 가 인용 가능한 단일
typed-interface record 를 emit.

## §3 integration log (5 step 결과)

### Step 1 — bridge 작성 + py_compile

```bash
python3 -m py_compile /Users/ghost/core/anima/anima-physics/tool/demiurge_materials_bridge.py
# PY_COMPILE_OK
```

- 파일: `anima-physics/tool/demiurge_materials_bridge.py` (~330 LoC).
- `DemiurgeMaterialsBridge` dataclass: backend ∈ {composite, hexa_matter,
  memristor, thermo, supercond} × material_class ∈ {TiO2, Si, Al, Cu, mixed}.
- 4-substrate aggregator: hexa_matter / memristor / thermodynamic /
  superconducting 각 measurement 통합.
- material property registry (4 + composite): NIST/CRC textbook anchors
  (density / bandgap / resistivity / conductivity / specific_heat / 등).
- gate_state(): GATE_OPEN (composite default) / GATE_FAIL (substrate
  실패 시 자동 채집).
- `_main()` argparse: `--backend` / `--material` / `--hexa-matter-exit`
  (override) / `--probe` (stat-only, no exec) / `--seed` / `--output`.
- **PASS**.

### Step 2 — bridge 직접 실행 + composite mode smoke

```bash
python3 /Users/ghost/core/anima/anima-physics/tool/demiurge_materials_bridge.py \
    --backend composite --output /tmp/materials_record.json --probe
```

출력 stderr:
```
[demiurge_materials_bridge] probe: hexa-matter verify/run_all.hexa
  present at /Users/ghost/core/hexa-matter/verify/run_all.hexa
  (skeleton — not auto-run; use --hexa-matter-exit to override)
[demiurge_materials_bridge] wrote /tmp/materials_record.json
```

record JSON 요지:
- `interface=demiurge:materials:composite-record`
- `record_id=materials_composite_TiO2_hxmNone_seed42`
- `producer=anima-materials-hexa-matter-combined-bridge`
- `measurement_gate=GATE_OPEN`, `absorbed=false`
- atlas_cite_block: 3 anima substrate + hexa-matter sibling-repo pointer
- 4 measurement block (hexa_matter pointer / memristor PASS / thermo
  slope / supercond deprecated)
- **PASS**.

### Step 3 — demiurge materials verify dry-run (pre-drop)

```bash
/Users/ghost/core/demiurge/bin/demiurge cli action verify materials
```

출력 요지 (g3 정직):
- "**materials(=matter) 도메인의 검증 엔진은 cockpit에 배선되어 있지 않습니다.**"
- "ActionDispatch.swift — `(.verify, …)` 케이스 17개 중 `matter` 케이스 부재."
- "D17 결정: demiurge 는 matter 의 pointer/consumer, SSOT 는 `~/core/hexa-matter/...`."
- "exports/material_sim/ — 빈 디렉토리."
- "✅ / 측정완료 표기 금지. 정직한 상태표시는 '엔진 미배선'."
- **확인**: gap 표기 정확, no over-claim.

### Step 4 — anima composite record 를 demiurge exports/ 에 drop

```bash
UTC_STAMP=$(date -u +%Y-%m-%dT%H-%M-%SZ)
UTC_FILE=$(date -u +%Y%m%dT%H%M%SZ)
RECORD_DIR="/Users/ghost/core/demiurge/exports/materials/verify/${UTC_STAMP}"
mkdir -p "$RECORD_DIR"
python3 /Users/ghost/core/anima/anima-physics/tool/demiurge_materials_bridge.py \
    --backend composite --material TiO2 --probe \
    --output "${RECORD_DIR}/anima_materials_${UTC_FILE}.json"
```

- 파일: `~/core/demiurge/exports/materials/verify/2026-05-21T09-30-19Z/anima_materials_20260521T093019Z.json` (3223 B).
- demiurge `exports/materials/` 디렉터리 신설 (이전엔 부재; sibling `exports/material_sim/` + `exports/material_verdict/` 는 별도 verdict 경로).
- **PASS**.

### Step 5 — demiurge re-verify with anima record present

```bash
/Users/ghost/core/demiurge/bin/demiurge cli action verify materials
```

출력 요지 (g3 정직):
- "엔진 도구 존재 여부 — ❌ 없음" (변함 없음, consumer cycle 별도).
- "exports/ 측정 레코드 — **1건 있으나 GATE_OPEN** (정직 미달성)"
- 자동 인용된 항목:
  - `exports/materials/verify/2026-05-21T09-30-19Z/anima_materials_20260521T093019Z.json`
  - `record_id=materials_composite_TiO2_hxmNone_seed42`
  - `verdict.gate_state=GATE_OPEN` (PASS 아님)
  - `hexa_matter.exit_code=null` · `closure_pass=null` (실행 안 됨, 스켈레톤)
  - `producer=anima-materials-hexa-matter-combined-bridge` (composite emitter — 측정기 아님)
  - 모든 scope_caveats 7건 인용:
    - "materials producer oracle parity not yet authored"
    - "anima 서브스트레이트 = CONSCIOUSNESS-ANALOG (material spec 아님)"
    - "memristor TiO2 = Strukov HP 아날로그"
    - "thermodynamic = double-well kinetics 아날로그"
    - "superconducting = DEPRECATED (Rigetti 2026-04-27 retired)"
    - "key_properties = NIST/CRC 교과서 디폴트값"
    - "hexa-matter exit code skeleton"
- "✅ / 측정완료 라고 보고하면 안 되는 셀입니다."
- **PARTIAL PASS**: demiurge 가 anima record 자동 감지·파싱·인용 ✅
  (D17 owner SSOT 명시 + composite caveats 7건 모두 출력), consumer 엔진
  부재로 verify 자체는 여전히 ⏳ gap.

## §4 anima 측 LANDED, hexa-matter / demiurge 측 cycle 후보

### 이번 cycle 에서 anima 측에 LANDED

1. **`anima-physics/tool/demiurge_materials_bridge.py`** (~330 LoC) —
   composite-emitter dataclass + 4-backend selector + 5-material registry
   + `--probe` (no auto-run hexa-matter, D17 안전) + `--hexa-matter-exit`
   override.
2. **첫 record drop** —
   `~/core/demiurge/exports/materials/verify/2026-05-21T09-30-19Z/
   anima_materials_20260521T093019Z.json` (3223 B).
3. **doc** — 본 doc + `demiurge_hw_verify_2026_05_21.md §2.1/§2.3` 갱신
   (materials: ⏳ no producer → ⏳ GATE_OPEN, GATE_OPEN count 10 → 11).

### hexa-matter (D17 owner SSOT) 측 cycle 후보 — 별도

- `verify/run_all.hexa` 정기 dispatch → exit code 를 anima bridge
  `--hexa-matter-exit` 로 전달 → record refresh.
- material_class 별 deep-dive verb (현재 4-script 외에 material-specific
  property anchor 신설 시 anima 측 registry 동기화 필요).

### demiurge (typed-interface consumer) 측 cycle 후보 — 별도

`MatterVerifyProducer.swift` 신설 → `ActionDispatch.swift` 의
`(.verify, "matter")` 케이스 등록 → `PRODUCERS.demi` 에
`[matter-verify]` sibling 섹션 추가 → schema decoder
(`demiurge:materials:composite-record`) 추가 → `demiurge cli show
<record>` 가 materials JSON 정상 파싱 → 기존 anima record 가 consumer
측에서도 GATE 평가 받음.

## §5 honest C3 (10)

1. **skeleton only** — `to_record()` 의 측정값은 `--*` 인자 의존
   (기본값 = 3 anima substrate §188/5/5 PASS 인용 + hexa-matter
   exit=None pointer). bridge 자체는 substrate 시뮬을 다시 돌리지
   않으며, caller 가 measurement override 가능.
2. **hexa-matter 실 실행 X** — D17 안전을 위해 `--probe` 는 stat-only
   (no exec). 실 closure verify 결과 인용은 사용자가 별도로 `hexa run
   ~/core/hexa-matter/verify/run_all.hexa; echo $?` → `--hexa-matter-exit
   <rc>` 패턴.
3. **real consumer 부재** — demiurge 측 `MatterVerifyProducer` 가
   없으므로 본 record 는 cli action verify materials 에서 **인용만**
   되고 oracle parity gating 평가는 일어나지 않음 (`gate_state=
   GATE_OPEN` 영구 — consumer cycle 이전).
4. **3 anima substrate = consciousness-analog** — memristor TiO2 는
   Strukov HP 모델 numpy 참조 (실 ionic drift 측정 X), thermodynamic 은
   Langevin double-well 일반 potential (실 화학 species X),
   superconducting 은 deprecated provenance gate (실 QPU 측정 X). 모두
   anima 측 자력 측정 정직성만 보장.
5. **material property registry = textbook defaults** — TiO2/Si/Al/Cu
   density/bandgap/resistivity 는 NIST/CRC 교과서 anchor, per-sample
   측정 X. real STEP geometry + 실측 datasheet import 는 component
   bridge cycle 의 사이드 (별도).
6. **superconducting deprecated 인용 자체가 honest gate** — Rigetti
   2026-04-27 retired 이후 substrate 부재 명시. provenance_gate_pass=
   True 는 "정직한 deprecation" 자체의 5/5 만족 (실 QPU 측정 ≠ 본 gate).
7. **D17 패턴 첫 anima impl** — brain bridge (anima owner) 와 달리
   materials 는 hexa-matter owner + anima consumer 의 분리 패턴.
   aura bridge (stub-only — substrate 부재 명시) 와도 다른 카테고리
   (composite consumer ≠ stub).
8. **schema 버전 0.1** — demiurge 측 schema decoder 가 chip F1F2 shape
   만 알고 materials shape 미등록. demiurge consumer cycle 에서 추가
   필요.
9. **record_id collision risk** — `materials_composite_TiO2_hxmNone_
   seed42` 동일 인자로 재발사 시 record_id 중복 (UTC stamp directory
   가 분리하나 inside-record_id 는 동일). 후속 cycle 에서 ts hash 추가
   고려.
10. **3-substrate weighting 없음** — composite mode 는 4 measurement
    block 을 평탄히 emit (no weighted aggregate). 향후 consumer 엔진이
    GATE 평가 시 weighting policy 정의 필요.

## §6 5-step pattern (brain/firmware/materials 공통) — D17 변형 추가

본 cycle 에서 확정된 **D17 consumer-pointer 변형**은 owner ≠ anima 인
다른 demiurge 도메인 (e.g. hexa-aura → aura, hexa-bio TBD → bio 등)
에도 동일 적용 가능:

1. anima 측에 `<domain>_bridge.py` 추가 — owner sibling-repo path 를
   `--probe` 만 (no exec) 으로 pointer 화 + anima 자체 substrate 측정값
   조합.
2. record JSON 의 `interface` 는 `demiurge:<domain>:composite-record`
   네임스페이스, `provenance.owner_pointer` 필수.
3. `key_properties` 등 textbook anchor 는 NIST/CRC 인용 + caveats 에
   "textbook default, per-sample measurement X" 명시.
4. anima 측에서 직접 `~/core/demiurge/exports/<domain>/verify/<UTC>Z/`
   에 drop (mkdir 자동).
5. demiurge `cli action verify <domain>` 가 record 자동 감지·인용 →
   gap 상태가 `❌/⏳ no producer` → `⏳ GATE_OPEN (composite consumer)`
   로 1-step 전환.
6. demiurge 측 consumer (`<Domain>VerifyProducer.swift` + ActionDispatch
   case + schema decoder) 신설 + owner sibling-repo 측 실 실행 자동화는
   별도 cycle.

## §7 SSOT pointer

- bridge code: `~/core/anima/anima-physics/tool/demiurge_materials_bridge.py`
- record drop: `~/core/demiurge/exports/materials/verify/2026-05-21T09-30-19Z/anima_materials_20260521T093019Z.json`
- owner SSOT (D17): `~/core/hexa-matter/verify/run_all.hexa`
- predecessor doc: `~/core/anima/anima-physics/docs/demiurge_hw_verify_2026_05_21.md` (§2.1 materials 행 갱신됨)
- sibling pattern (anima owner+producer): `~/core/anima/anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
- SW source — anima substrate:
  - `~/core/anima/anima-physics/memristor/self_reference.hexa` (§188 5/5 PASS, TiO2 HP memristor)
  - `~/core/anima/anima-physics/thermodynamic/entropy_dissolution.hexa` (5/5 PASS, Langevin)
  - `~/core/anima/anima-physics/superconducting/cloud_facade_poc.hexa` (deprecated, provenance 5/5)
- demiurge consumer cycle pointer: `~/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ActionDispatch.swift` `(.verify, "matter")` 케이스 신설 + `MatterVerifyProducer.swift` (TODO)
