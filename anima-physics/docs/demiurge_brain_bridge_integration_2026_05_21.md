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
3. **1 backend only** — `local_sim` 만 end-to-end 검증. `akida_cloud` /
   `loihi2_nrc` 두 backend code path 는 `gate_state()` switch 등록만
   되어 있고 실제 cloud trial 결과 record drop 은 별도 cycle (cost
   $1-30 user 승인 필요).
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
