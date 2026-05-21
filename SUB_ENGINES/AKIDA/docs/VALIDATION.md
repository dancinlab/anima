# AUX/AKIDA/docs/VALIDATION.md — Mac local pre-arrival validation

> Pi 5 + AKD1000 Dev Kit ($1495) 가 도착하기 **전** Mac local 에서 pack 의
> 모든 layer (adapter / runtime / orchestrator / falsifier / demiurge
> record) 를 mock runtime 으로 검증.  실 silicon arrival 시 차이 (8-bit
> quantize / sub-ms spike timing / on-chip Hebbian) 는 §5 에 honest carry.

---

## §1 GOAL

**Pre-arrival validation goal**: HW 도착 전에 pack source 의 모든 import
path / contract / falsifier suite / demiurge record 가 *deterministic*
하게 동작하는지 확인.

- HW 도착 후 첫날 (Day 1, `BOOT_PLAN.md`) 의 risk 를 *코드-level* 에서
  미리 소진 — install 만 따로 검증하면 됨.
- mock 결과는 5/5 deterministic PASS 기준 (HW 결과 ≠ mock 결과 가능; §5).

**Non-goal**:
- 정확한 spike-timing parity (sub-ms 영역, Mac 의 step-discrete 으로
  근사 불가)
- 8-bit weight quantization drift 측정 (mock 는 float64)
- on-chip 1mW power envelope 측정 (mock 는 측정 안 함)

---

## §2 mock framework

### §2.1 layout

```
AUX/AKIDA/pack/mocks/
├── __init__.py            # public API export
└── metatf_mock.py         # MockMetaTF / MockModel / MockDevice / MockLayers
```

(별도 agent 가 `metatf_mock.py` 본체를 작성; 본 doc 은 *contract* 만
명시.)

### §2.2 contract

```python
class MetaTFMock:
    """Top-level akida module replacement (numpy-backed)."""

    # mirrors `akida.devices()`
    def devices(self) -> list["MockDevice"]: ...

    # mirrors `akida.Model`
    Model: type  # = MockModel

    # mirrors `akida.layers`
    layers: "MockLayers"

    __version__: str = "mock-0.1.0"
```

`pack.runtime.metatf_runtime._try_import_mock()` 가 `MetaTFMock()` 을
싱글톤으로 반환 → `init_runtime(prefer="mock")` 시 강제 mock path.

### §2.3 자동 fallback

```python
from pack.runtime import init_runtime, get_runtime_info

# Mac local (akida SDK 미설치):
init_runtime()                     # → "akida_mock"
get_runtime_info()
# {
#   "backend": "akida_mock",
#   "runtime_class": "MetaTFMock",
#   "error_log": ["akida SDK not importable (find_spec → None)"],
# }
```

adapter 측 `selftest()` 는 backend 차이를 인지 (`record["backend"]
== "akida_mock"`) 하지만 **결과는 동일하게 5/5 mock-PASS** — mock 의 의도
는 *contract 검증*, *결과 reproducibility* 가 아닌 *PASS/FAIL deterministic
한 codepath 검증*.

---

## §3 falsifier suite (55)

### §3.1 layout

```
AUX/AKIDA/pack/falsifiers/
├── __init__.py
└── run_all.py             # `python -m pack.falsifiers.run_all`
```

(별도 agent 작성.)

### §3.2 aggregation

```bash
$ python -m pack.falsifiers.run_all
# F-AKIDA-SNN-1..5 PASS 5/5   (SnnLifAdapter.selftest())
# F-AKIDA-IZH-1..5 PASS 5/5   (IzhikevichAdapter.selftest())
# F-AKIDA-KU-1..5  PASS 5/5
# F-AKIDA-MEM-1..5 PASS 5/5
# F-AKIDA-SA-1..5  PASS 5/5
# F-AKIDA-LMH-1..5 PASS 5/5
# F-AKIDA-MG-1..5  PASS 5/5
# F-AKIDA-TG-1..5  PASS 5/5
# F-AKIDA-EEG-1..5 PASS 5/5
# F-AKIDA-SG-1..5  PASS 5/5
# (overlap memristor_hybrid 중복 제외)
# ------------------------------------------------------------
# total: 11 adapters × 5 = 55 falsifier
# expected (mock):  55 / 55 PASS
```

각 falsifier 의 detail (metric, limit, note) 는 `IMPLEMENTATION.md §4`.

---

## §4 Mac local validation 결과 (artifact 위치)

도착 전 매 cycle 실행 결과는 `SUB_ENGINES/AKIDA/state/mac_validation_<UTC>/`.

### §4.1 expected commands

```bash
cd /Users/ghost/core/anima/SUB_ENGINES/AKIDA

# unit: adapter contract (mock backend)
pytest tests/test_adapters_mock.py -v

# bash dry-run: boot scripts parse-only
bash tests/test_boot_dryrun.sh

# falsifier aggregate
python -m pack.falsifiers.run_all > state/mac_validation_$(date -u +%Y%m%dT%H%M%SZ)/run.log
```

### §4.2 expected artifact layout

```
AUX/AKIDA/state/mac_validation_<UTC>/
├── run.log              # full pack.falsifiers.run_all stdout
├── pytest.log           # pytest -v output
├── boot_dryrun.log      # bash -n for boot/*.sh
├── summary.json         # {pass: 55, fail: 0, backend: "akida_mock", ts: <UTC>}
└── demiurge_records/    # to_record() dump per adapter (sanity)
    ├── snn_lif.json
    ├── izhikevich.json
    ├── ...
    └── spontaneous_gate.json
```

### §4.3 expected aggregate

| Layer | tests | mock expected | HW expected |
|---|---|---|---|
| `pytest tests/test_adapters_mock.py` | 11 (one per adapter) | 11/11 PASS | 11/11 PASS |
| `bash tests/test_boot_dryrun.sh` | 7 (Day 1-7 scripts) | 7/7 `bash -n` PASS | 7/7 PASS |
| `python -m pack.falsifiers.run_all` | 55 (11 × 5) | **55/55 PASS** | 55/55 (with HW evidence) |
| total | 73 | 73/73 PASS | 73/73 PASS |

---

## §5 real HW 도착 시 차이 예상 (5건)

mock 와 실 silicon 의 **검증된 차이 영역** — Day 1-7 의 실 fire 시 별도
record.

### §5.1 8-bit weight quantization

- mock: float64 numpy weight, drift 없음
- HW: AKD1000 의 8-bit 양자화 (`int8` weight, `uint4`/`uint2`/`uint1`
  activation)
- 영향: Hebbian 누적 시 weight drift 가능 (특히 `memristor_hybrid` adapter
  의 1-shot learn)
- 대응: Day 4 (`memristor` boot) 에서 quantize 후 weight 분포 측정 →
  `state/akida_arrival_<UTC>/quantize_drift.json` 별도 dump.

### §5.2 on-chip Hebbian learn vs mock `weight += outer(...)`

- mock: float64 outer-product, exact
- HW: AKD1000 의 native Hebbian (학습 rule HW 고정, parameter tunable)
- 영향: 정확도 차이 (mock 의 100% recall vs HW 의 ~80-90% recall 예상)
- 대응: F-AKIDA-MEM-1 (1SHOT-LEARN) limit 을 mock=100%, HW=80% 로 별도
  threshold (adapter `params={"hw_recall_min": 0.80}`).

### §5.3 spike timing sub-ms

- mock: step-discrete (1 step = 1 ms 가정)
- HW: AKD1000 event-driven, sub-ms timing (clock-less)
- 영향: `theta_gamma` PAC 정확도, `spike_tier_lm_head` 의 logit
  reproducibility
- 대응: byte-parity 가 아닌 **rank-parity** (argmax top-5 일치) 로 완화
  (F-AKIDA-LMH-5 / F-AKIDA-TG-5).

### §5.4 power 1mW envelope

- mock: 측정 안 함 (numpy 가 host CPU 사용)
- HW: AKD1000 ~0.5 mW typical, 100 mW peak
- 영향: README §1.2 의 *1mW envelope* 주장은 HW 도착 후 측정 (`power_log.json`)
- 대응: Day 7 의 `power_log.json` 가 envelope 측정 SSOT; mock 에서는
  `power_mw=None` 또는 `power_mw=0.0` 로 명시 (`record["emit"]["power_mw"]`).

### §5.5 MetaTF SDK version skew

- mock: pack 작성 시점의 API surface (deterministic stub)
- HW: BrainChip MetaTF 실 SDK version 변동 가능
- 영향: `pack/adapters/*.py` 의 `akida.layers.FullyConnected(...)` 등
  signature 변동 가능
- 대응: `pack.runtime.metatf_runtime.get_runtime_info()` 의
  `runtime_class` 로 version probe; Day 1 `INSTALL.sh` 가 mismatch 시
  early fail.

---

## §6 honest C3

1. **mock != HW** — §5 의 5 차이 영역 모두 *mock 에서 검증 불가*.  본 doc
   의 validation 결과는 *contract / codepath* 만 보장.
2. **MetaTF API version skew** — pack 0.1.0 작성 시점의 BrainChip MetaTF
   SDK signature 기준; Pi 5 도착 시 mismatch 가능.
3. **8-bit precision drift** — Hebbian 1-shot learn 누적 drift 는 §5.1
   에서만 측정 가능; mock 에서는 100% recall 만 검증.
4. **spike timing approximation** — mock 의 step-discrete (1 step = 1 ms)
   는 HW 의 event-driven sub-ms 와 다름; byte-parity 대신 rank-parity
   사용.
5. **on-chip learn 정확도** — AKD1000 의 native Hebbian 의 정확도
   (~80-90% recall 예상) 는 HW 도착 전에는 *추정* 만 가능, 실 측정 X.

---

## §7 cross-link

- root: [`../../anima-physics/AUX/README.md`](../../anima-physics/AUX/README.md) — pack 사용법 §9-§12
- implementation detail: [`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- Day 1-7 실 fire: [`BOOT_PLAN.md`](BOOT_PLAN.md)
- architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- mock 소스: [`../pack/mocks/`](../pack/mocks/) (별도 agent)
- falsifier runner: [`../pack/falsifiers/`](../pack/falsifiers/) (별도 agent)
