# demiurge brain producer integration — Step 1 (anima 측 bridge LANDED + 첫 record drop)

> anima `demiurge_brain_bridge.py` 를 demiurge brain verify producer 로 wire
> 하고 첫 end-to-end record 를 demiurge exports/ 에 drop 한 cycle.
> Date: 2026-05-21
> Predecessor: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.2`
> (brain 행이 ❌ no producer 였던 시점).

## §1 GOAL

demiurge `brain` 도메인의 verify gap 을 anima 측에서 producer-skeleton + 첫
record drop 으로 메우는 **Step 1**.

- **Before**: `demiurge cli action verify brain` → "engine tool 미구현 (⏳ gap),
  `(.verify, "brain")` 케이스 + `BrainVerifyProducer` 신설 선행" (생산자도,
  소비자도 없음).
- **After (this cycle)**: anima 측 producer skeleton + 첫 record dropped
  under `~/core/demiurge/exports/brain/verify/<UTC>Z/`. demiurge `cli action
  verify brain` 이 본 record 를 **자동 감지·인용** (provenance/backend/gate
  까지 출력). consumer 엔진 (BrainVerifyProducer.swift) 신설은 별도 cycle.
- **Status delta**: brain row `❌ no producer` → `⏳ GATE_OPEN` (record
  exists, consumer engine TODO).

이번 cycle 은 **(a) anima 측 producer skeleton 패턴 확정 + (b) 첫 record
실재 + (c) demiurge × anima 양방향 path 검증**까지. 실 silicon 측정·oracle
parity 는 Phase 2 cloud trial cycle 후보.

## §2 integration log (4 step 결과)

### Step 1 — bridge 직접 실행 + JSON output

```bash
cd /Users/ghost/core/anima/anima-physics/hw/kuramoto_neuromorphic/src/
python3 demiurge_brain_bridge.py --backend local_sim --output /tmp/brain_record.json
```

- 추가 사항: bridge 의 `_main()` argparse CLI 추가 (`--backend` /
  `--n` / `--k` / `--steps` / `--r-tail` / `--r-std-tail` / `--seed` /
  `--output`). 기본값은 `state/sim.log` F-HW-KU-3 locked-state
  measurement (N=8, K=5.0, steps=1000, r_tail=0.951, r_std_tail=0.0434).
- 결과 JSON: `interface=demiurge:brain:kuramoto-record`, `record_id=
  kuramoto_n8_k5.00_local_sim`, `producer=anima-kuramoto-loihi-akida-bridge`,
  `measurement_gate=GATE_OPEN`, `absorbed=false`, atlas_cite_block 포함.
- **PASS**.

### Step 2 — demiurge brain verify dry-run (pre-drop)

```bash
demiurge cli action verify brain
```

출력 요지 (g3 정직):
- "엔진 툴: 없음. `ActionDispatch.swift` 의 `(.verify, …)` switch 에
  brain 케이스가 등록돼 있지 않습니다."
- "측정 record: 없음. `exports/brain/` 디렉터리 자체가 존재하지 않습니다."
- "결론: 측정완료 ✅ 주장 불가. 도메인 `brain` + stage `verify` 조합은
  engine tool 미구현 (⏳ gap)."
- **확인**: gap 표기 정확, no over-claim.

### Step 3 — anima record 를 demiurge exports/ 에 drop

```bash
RECORD_DIR="/Users/ghost/core/demiurge/exports/brain/verify/2026-05-21T08-22-26Z"
mkdir -p "$RECORD_DIR"
python3 .../demiurge_brain_bridge.py --backend local_sim \
    --output "$RECORD_DIR/anima_kuramoto_20260521T082226Z.json"
```

- 파일: `~/core/demiurge/exports/brain/verify/2026-05-21T08-22-26Z/
  anima_kuramoto_20260521T082226Z.json` (1308 B).
- demiurge `exports/brain/` 디렉터리 신설 (이전엔 부재).
- **PASS**.

### Step 4 — demiurge re-verify with anima record present

```bash
demiurge cli action verify brain
```

출력 요지:
- "기존 측정 레코드: **1건 존재** —
  `exports/brain/verify/2026-05-21T08-22-26Z/anima_kuramoto_20260521T082226Z.json`
  - `record_id`: `kuramoto_n8_k5.00_local_sim`
  - `producer`: `anima-kuramoto-loihi-akida-bridge` (demiurge 외부)
  - `backend`: `local_sim` (numpy 참조 시뮬, 실리콘 스파이크가 아님)
  - `gate_state`: GATE_OPEN (skeleton emit · provisional)
  - 자기 기재 caveats: 'brain producer oracle parity not yet authored
    (TODO: demiurge rfc)'"
- "demiurge 내부에 brain:verify 를 직접 돌릴 엔진은 **아직 없습니다**."
- **PARTIAL PASS**: demiurge 가 anima record 를 자동 감지·파싱·인용 ✅,
  그러나 consumer 엔진 부재로 verify 자체는 여전히 ⏳ gap.

추가 sanity: `demiurge cli show <record>` 는 **Decode failed** — chip
F1F2 record 와 brain record 의 schema 가 달라 `show` 가 reject. 별도
brain schema decoder 가 demiurge 측 consumer cycle 의 일부.

## §3 anima 측 LANDED, demiurge 측 cycle 후보

### 이번 cycle 에서 anima 측에 LANDED

1. **`anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`** —
   CLI argparse + 기본값 = sim.log F-HW-KU-3 measured.
2. **첫 record drop** —
   `~/core/demiurge/exports/brain/verify/2026-05-21T08-22-26Z/
   anima_kuramoto_20260521T082226Z.json` (1308 B).
3. **doc** —
   `anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
   (본 doc) + `demiurge_hw_verify_2026_05_21.md §2.2/§2.3/§3` 갱신
   (brain: ❌ no producer → ⏳ GATE_OPEN, gap count 5 → 4, open count
   9 → 10).

### 후속 cycle 2026-05-21 — akida_cloud branch 실 SDK 정합 LANDED

bridge v0.2 (SCHEMA_VERSION 0.1 → 0.2 additive):

1. **`submit_to_akida_cloud(n, k, steps, r_tail, ...)` driver 신설** —
   `import akida` try ⊥ `akida.devices()` discovery ⊥ `_build_akida_kuramoto_model()`
   (InputData + FullyConnected + AkidaUnsupervised.compile) ⊥
   `model.map(devs[0])` + `model.forward(uint8)` flow. `SUB_ENGINES/AKIDA/doc/
   metatf_api_{model,devices,layers}.md` 와 byte-equal.
2. **graceful 3-tier fallback** — (i) Mac local SDK 부재
   (`akida_unavailable_reason` = ImportError), (ii) SDK 있지만
   `akida.devices()==[]` (no AKD1000), (iii) `.map()` / `.forward()` raise —
   3 tier 모두 동일 record shape 유지 (record_id 에 `_akida_cloud_unavailable`
   flag, scope_caveats 자기 기재).
3. **record format v0.2 신규 root fields 3건** —
   `power_estimate_mW` (idle 50 mW + spike × 0.5 mW), `npu_count_used`
   (20 NPU mesh 중 mapped sequence component 집계), `latency_us_estimate`
   (300 MHz clock × cycles_per_spike). akd1000_power_spec.md / hardware_spec.md
   datasheet 기반. local_sim/loihi2_nrc backend 은 0.0 (additive).
4. **provenance.akida_sdk_*** — `available` / `version` / `hw_device_count` /
   `unavailable_reason` / `spike_train_len` 5 fields 추가, mock vs HW path
   self-disclosure.
5. **demiurge cli verify brain 자동 인용 재확인** — exports/brain/verify/<UTC>Z/
   anima_kuramoto_akida_cloud_*.json drop 후 `demiurge cli action verify brain`
   이 latest record = akida_cloud record 로 정확히 pick (record_id =
   `kuramoto_n8_k5.00_akida_cloud_akida_cloud_unavailable` 명시 인용,
   `⏳ GATE_OPEN · absorbed=false`).

bridge 는 여전히 `pack.runtime.metatf_runtime` 의존 X (stand-alone
`import akida` try) — sibling 관계 보존, anima-physics 만으로
mac local + Pi5 + cloud 3 환경 동일 record schema 보장.

### demiurge 측 별도 cycle 후보 (consumer)

`BrainVerifyProducer.swift` 신설 → `ActionDispatch.swift` 의
`(.verify, "brain")` 케이스 등록 → `exports/brain/verify/` path 표준
(이미 anima 측에서 establish 완료) → schema decoder 추가 → `demiurge
cli show <brain-record>` 가 brain JSON 을 정상 파싱 → 기존 anima record
가 consumer 측에서도 GATE 평가 받음. 이 후속 cycle 의 PR 은 demiurge
repo 측에서 별도 dispatch.

### 추가 후속 (Phase 2 cloud trial)

- BrainChip Akida Cloud trial ($1-30) → `--backend akida_cloud` 실측 →
  새 record drop → demiurge consumer 가 oracle parity 정의 후
  GATE_CLOSED_MEASURED upgrade.
- Loihi 2 Hala Point trial (신청 후 대기) → `--backend loihi2_nrc` 동일
  pattern.

## §4 honest C3

1. **skeleton only** — `to_record()` 의 측정값은 `--r-tail` / `--r-std-tail`
   인자 의존 (기본값 = sim.log F-HW-KU-3 인용). bridge 자체는 numpy
   sim 을 다시 돌리지 않으며, caller 가 measurement 를 주입해야 함. 실
   silicon 측정 자동화는 별도 hexa 측 producer 신설 작업.
2. **real consumer 부재** — demiurge 측 `BrainVerifyProducer` 가 없으므로
   본 record 는 cli action verify brain 에서 **인용만** 되고 oracle parity
   gating 평가는 일어나지 않음 (`gate_state=GATE_OPEN` 영구 — Phase 2 이전).
3. **2 backend end-to-end verified** — `local_sim` 와 `akida_cloud` 모두
   record drop + demiurge cli verify brain 자동 인용 확인. `akida_cloud`
   는 (a) Mac local SDK 없음 path = graceful skeleton (`record_id` 에
   `_akida_cloud_unavailable` flag) (b) Pi5+AKD1000 OR Akida Cloud Trial
   path = 실 silicon spike measurement — 두 경로 동일 `submit_to_akida_cloud()`
   진입. `loihi2_nrc` 단독 미검증 (Loihi 2 NRC 신청 후 대기).
4. **`cli show` decode fail** — demiurge 측 schema decoder 가 chip F1F2
   shape 만 알고 brain shape 미등록. anima 측 schema 는 `interface=
   demiurge:brain:kuramoto-record` SCHEMA_VERSION=0.1 — demiurge consumer
   cycle 에서 decoder 추가 필요.
5. **single (N, K) point** — F-HW-KU-3 의 K=5.0 단일 측정만 record 화.
   full K-sweep regime claim (subcritical → critical → supercritical
   전이 정확도) 은 multi-point record drop + consumer 측 sweep 평가
   별도 cycle.

## §5 key learning — anima-side producer skeleton 패턴

본 cycle 에서 확정된 패턴은 **다른 demiurge engine-gap 도메인
(aura/bio/chem/grid)** 도 동일하게 적용 가능:

1. anima 측에 `<domain>_bridge.py` 추가 (skeleton dataclass + `to_record()` +
   `_main()` argparse + `--output`).
2. record JSON 의 `interface` 는 `demiurge:<domain>:<measurement>-record`
   네임스페이스.
3. provenance 에 `producer`, `backend`, `measurement_gate`, `consumer_target=
   demiurge:<domain>:verify`, `scope_caveats`, `gate_failures` 필수.
4. anima 측에서 직접 `~/core/demiurge/exports/<domain>/verify/<UTC>Z/`
   에 drop (mkdir 자동).
5. demiurge `cli action verify <domain>` 가 record 자동 감지·인용 →
   gap 상태가 `❌ no producer` → `⏳ GATE_OPEN` 으로 1-step 전환.
6. demiurge 측 consumer (`<Domain>VerifyProducer.swift` + ActionDispatch
   case + schema decoder) 신설은 demiurge repo 별도 cycle.

이 6-step skeleton 으로 anima 측 단독 (cost $0, Mac local) 으로 demiurge
gap 4건 (aura/bio/chem/grid) 도 같은 패턴으로 1-step씩 메울 수 있음 — 단,
각 도메인의 atlas-registered SW source (anima-physics 의 어느 hexa
substrate 가 producer 의 측정 단위인지) 확정이 선행 조건.

## §6 SSOT pointer

- bridge code: `~/core/anima/anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`
- record drop: `~/core/demiurge/exports/brain/verify/2026-05-21T08-22-26Z/anima_kuramoto_20260521T082226Z.json`
- predecessor doc: `~/core/anima/anima-physics/docs/demiurge_hw_verify_2026_05_21.md` (§2.2 brain 행 갱신됨)
- SW source: `~/core/anima/anima-physics/social/kuramoto_coupling.hexa` §188 PASS 6/6
- local sim source: `~/core/anima/anima-physics/hw/kuramoto_neuromorphic/src/kuramoto_local_sim.py` (F-HW-KU-1..5 5/5)
- demiurge consumer cycle pointer: `~/core/demiurge/cockpit/.../ActionDispatch.swift` `(.verify, "brain")` 케이스 신설 + `BrainVerifyProducer.swift` (TODO)

### SUB_ENGINES/AKIDA cross-link (bridge ↔ pack sibling 관계)

bridge 는 `SUB_ENGINES/AKIDA/pack/` 의 sibling — 동일 SDK target (AKD1000
NSoC_v1) + 동일 `import akida` try 패턴, 하지만 의존성 X. 각자 stand-alone.

| 측면 | anima-physics bridge | SUB_ENGINES/AKIDA pack |
|---|---|---|
| 책임 | producer (substrate measurement → record JSON) | runtime infra (mock + HW path init, 10 adapter) |
| code path | `submit_to_akida_cloud()` 직접 try | `metatf_runtime.get_runtime()` lazy init |
| consumer | demiurge `cli action verify brain` | pack 자체 falsifier suite (`pack/falsifiers/`) |
| layer build | `_build_akida_kuramoto_model()` (8-cell pool) | `pack/adapters/kuramoto_adapter.py` (대응 8-cell) |
| spec source | `metatf_api_{model,devices,layers}.md` 직접 인용 | 동일 doc + `mocks/metatf_mock.py` 거울 |
| target host | Mac local (mock) + Pi5+AKD1000 (real) + Cloud trial | 동일 |

bridge 는 **pack 미인스톨 상태에서도** `import akida` 만으로 작동 — 양쪽
모두 BrainChip MetaTF SDK 가 SSOT, intermediary 없음. 향후 pack 의 10
adapter 갱신 cycle (별도 BG) 과 file overlap 0 (bridge 단독 소유).

cross-link doc:
- `~/core/anima/SUB_ENGINES/AKIDA/doc/metatf_api_model.md` (Model API + edge learning)
- `~/core/anima/SUB_ENGINES/AKIDA/doc/metatf_api_devices.md` (devices() + HwVersion + MapMode)
- `~/core/anima/SUB_ENGINES/AKIDA/doc/metatf_api_layers.md` (InputData/FullyConnected V1)
- `~/core/anima/SUB_ENGINES/AKIDA/doc/akd1000_hardware_spec.md` (20 NPU mesh, 300 MHz, 1 W TDP)
- `~/core/anima/SUB_ENGINES/AKIDA/doc/akd1000_power_spec.md` (PowerMeter API, ClockMode)
- `~/core/anima/SUB_ENGINES/AKIDA/doc/akd1000_onchip_learning.md` (AkidaUnsupervised + add_classes)

### key learning — bridge ↔ pack 의존성 패턴

**의존성 0 = robust separation**. bridge 가 `pack.runtime.metatf_runtime`
import 를 한 줄도 안 함 → pack 의 mock 구현 변경/falsifier sweep 이
bridge record 형식에 영향 X, 역방향도 마찬가지. SSOT 는 둘 모두 BrainChip
MetaTF SDK (`import akida`) + cached doc spec — 양쪽 다 동일 doc 인용,
intermediary 없음.

이 패턴은 다른 demiurge gap bridge (aura/bio/chem/grid) 도 동일하게 적용
— anima-physics 측 bridge 가 SUB_ENGINES/<HW>/pack/ 와 sibling 으로
서있으면서 SDK 만 공유, code 의존성 0. anima-physics 가 demiurge 측
producer (record JSON shape SSOT) + SUB_ENGINES 가 HW SDK runtime
(adapter + mock + falsifier) — 역할 분리가 명확해야 future cycle 에서
양쪽이 독립적으로 진화 가능.
