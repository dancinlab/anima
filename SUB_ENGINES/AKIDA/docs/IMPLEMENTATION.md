# AUX/AKIDA/docs/IMPLEMENTATION.md — 11 adapter + runtime 구현 detail

> Pack module: `anima-akida-pack 0.1.0` (`pack/__init__.py`).
> Implementation surface = **11 adapters** (`pack/adapters/`) + **3 runtime**
> modules (`pack/runtime/`) + **mocks** (`pack/mocks/`) +
> **falsifier runner** (`pack/falsifiers/`).
>
> 본 doc 은 *구현 detail* (어떤 클래스 / 어떤 contract / 어떤 falsifier).
> Architecture diagram 은 `ARCHITECTURE.md`, validation 결과는
> `VALIDATION.md`, Pi 5 도착 후 Day-by-day 는 `BOOT_PLAN.md` 참조.

---

## §1 adapter family (11)

11 adapter 는 `pack/adapters/` 산하 module 별 단일 파일.  3 group 으로
나뉘며 모두 `base.AkidaAdapter` 상속, `selftest()` 에서 F-AKIDA-<NAME>-1..5
5 falsifier 자체 실행.

### §1.1 EXACT Akida fit (4 core)

AKD1000 의 1024 NPU + LIF spike primitive 와 **1:1 native fit** 인 adapter.

| File | Class | Substrate origin | Akida primitive |
|---|---|---|---|
| `pack/adapters/snn_lif.py` | `SnnLifAdapter` | `engines/snn_consciousness.hexa` (§188g 5/5, 349 LoC) | LIF neuron + 8-bit weight (`akida.layers.FullyConnected`) |
| `pack/adapters/izhikevich.py` | `IzhikevichAdapter` | `engines/izhikevich_consciousness.hexa` (§188g 5/5, 307 LoC) | 2-var spike model → `akida.layers.InputData` + custom param |
| `pack/adapters/kuramoto.py` | `KuramotoAdapter` | `social/kuramoto_coupling.hexa` (§188 6/6, 509 LoC) | spike-coupled oscillator pool → 1024 NPU mapped phase array |
| `pack/adapters/memristor_hybrid.py` | `MemristorHybridAdapter` | `memristor/self_reference.hexa` (§188 5/5) | TiO2 memristor SW analog → AKD1000 on-chip Hebbian 1-shot learn |

### §1.2 신규 candidates (4 new from README §4)

README §4 의 N1-N4 신규 보조엔진 — **현재 SW 없음** (Akida 의 강점을 활용한
신규 spike-tier engine).

| File | Class | README §4 ref | 역할 |
|---|---|---|---|
| `pack/adapters/sparse_attention.py` | `SparseAttentionAdapter` | N1 | anima `sparse_attention` pattern → MetaTF quantize → AKD1000 sparse compute |
| `pack/adapters/spike_tier_lm_head.py` | `SpikeTierLmHeadAdapter` | N2 | anima Tier 1 모델 `lm_head` 분기 → Akida small-model spike head |
| `pack/adapters/motivation_gate.py` | `MotivationGateAdapter` | N4 | `spontaneous_smoke` threshold compare → Akida native event-fire (1mW) |
| (overlap) | (—) | N3 = `memristor_hybrid.py` (§1.1) | hybrid substrate 는 §1.1 의 MemristorHybridAdapter 와 동일 file |

### §1.3 보조 (3 support)

EXACT fit 은 아니지만 Akida 의 event-driven trigger 와 자연 매핑되는 보조
adapter.

| File | Class | Substrate origin | 역할 |
|---|---|---|---|
| `pack/adapters/theta_gamma.py` | `ThetaGammaAdapter` | `hippocampus/theta_gamma.hexa` (§188 5/5) | cross-freq θ-γ spike coupling pool |
| `pack/adapters/eeg_pattern.py` | `EegPatternAdapter` | `eeg/{mu_rhythm,sleep_stage,phi_correlator}` (§188 17/17) | Akida 의 native 강점 — EEG-style spike pattern recognition |
| `pack/adapters/spontaneous_gate.py` | `SpontaneousGateAdapter` | `HEXAD/CHAT/spontaneous_smoke` | 자연발화 candidate emit (motivation gate 의 audit-buffer 측 mirror) |

**총 11**: 4 EXACT + 3 신규 (N3 overlap 제외) + 3 보조 + (N4 = 신규).
실제로는 EXACT(4) + 신규(3) + 보조(3) + 1 hybrid-overlap = **11 module
files**.

---

## §2 base class contract (AkidaAdapter)

`pack/adapters/base.py` 가 모든 adapter 의 공통 base.

```python
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class AkidaAdapter:
    """Common base for all 11 adapters.

    Lifecycle: __init__ → build() → fit?() → forward() → to_record()
    """
    name: str                          # e.g. "snn_lif", "kuramoto", ...
    substrate_origin: str              # source .hexa path (informational)
    backend: str = "auto"              # auto | hw | mock
    params: dict[str, Any] = field(default_factory=dict)
    _model: Optional[Any] = None       # MetaTF model handle
    _last_output: Optional[Any] = None

    # ------- abstract surface (subclasses MUST override) ----------------
    def build(self) -> None: ...
    def forward(self, x) -> Any: ...

    # ------- optional surface (Hebbian / event emit) --------------------
    def fit(self, x, y=None) -> None: ...     # on-chip 1-shot learn
    def emit(self) -> Optional[dict]: ...     # 자연발화 candidate

    # ------- concrete contract (subclasses INHERIT, do not override) ----
    def selftest(self) -> dict:
        """Run F-AKIDA-<NAME>-1..5; return aggregate.

        Returns
        -------
        dict
            {"name": str, "passed": int, "failed": int,
             "details": list[dict]}
        """
        ...

    def to_record(self) -> dict:
        """demiurge-compatible record (mirrors demiurge_brain_bridge.py).

        Returns
        -------
        dict
            {"adapter": name,
             "backend": "akida_hw" | "akida_mock",
             "ts_utc": ISO8601,
             "substrate_origin": str,
             "params": dict,
             "selftest": dict,           # from selftest()
             "emit": Optional[dict]}     # from emit() if available
        """
        ...
```

**Dataclass fields**: 6 (`name`, `substrate_origin`, `backend`, `params`,
`_model`, `_last_output`).  Sub-adapter 들은 typed sub-dataclass 로 추가
field 만 더한다 (e.g., `SnnLifAdapter` 는 `n_cells: int`, `tau_m: float`
추가).

`to_record()` 의 format 은 §5 demiurge integration 에서 상세.

---

## §3 runtime layer

3 module, 모두 `pack/runtime/` 산하.

| Module | LoC | 역할 |
|---|---|---|
| `pack/runtime/metatf_runtime.py` | 156 | HW (`import akida`) vs mock (`pack.mocks.metatf_mock`) auto-detect + sticky cache + `init_runtime(prefer=...)` |
| `pack/runtime/audit_buffer.py` | 149 | 8-deep LRU ring buffer; atomic `dump()` to `~/.cache/anima-akida/audit_buffer.jsonl`; thread-safe (Lock) |
| `pack/runtime/pi5_orchestrator.py` | TBD | Pi 5 host orchestrator — adapter bundle 실행, audit buffer write, motivation gate emit cadence |

### §3.1 metatf_runtime — auto-detect priority

```
                ┌──────────────────────────┐
                │  init_runtime(prefer)    │
                └────────────┬─────────────┘
                             │
              prefer == "auto" (default)
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
     _try_import_akida_hw()    _try_import_mock()
            │                            │
            │ success → backend="akida_hw"│
            │                            │ success → backend="akida_mock"
            ▼                            ▼
        RUNTIME = real akida         RUNTIME = MetaTFMock()
```

`prefer="hw"` 또는 `prefer="mock"` 으로 강제 가능 (테스트 시 mock 강제).
`reset_runtime()` 은 test-only.

### §3.2 audit_buffer — 8-deep LRU

- capacity 기본 8 (pack spec).  > 32 kB 미만 보장 → eMMC 친화.
- `append()` O(1), `dump()` atomic (`tempfile.mkstemp` → `os.replace`).
- JSON-lines on-disk (partial read crash-safe).
- `threading.Lock` 보호 (orchestrator 측 read/write 분리 thread).
- `autoload=True` 로 시작 시 disk → buffer 로 복원.

### §3.3 pi5_orchestrator — bundle driver

```
Pi5Orchestrator
  ├── adapters: list[AkidaAdapter]
  ├── audit: AuditBuffer (capacity=8)
  ├── runtime: get_runtime() (HW or mock)
  ├── tick(dt) → for each adapter: forward → emit? → audit.append
  └── stop() → audit.dump() (eMMC 영속)
```

Day 5 E2E v2 chain 에서 첫 stage Akida 로 교체 시 orchestrator 가 chain
조립.

---

## §4 falsifier convention

각 adapter 는 `selftest()` 내에서 F-AKIDA-<NAME>-1..5 5 falsifier 실행.
**총 11 × 5 = 55 falsifier**.

| Adapter | Falsifier prefix | 5 falsifier 예시 |
|---|---|---|
| `snn_lif` | `F-AKIDA-SNN-` | 1=SPIKE-COUNT, 2=THRESHOLD-FIRE, 3=8BIT-CLAMP, 4=POWER-1MW, 5=BYTE-PARITY |
| `izhikevich` | `F-AKIDA-IZH-` | 1=2VAR-DYNAMICS, 2=BURST-EMIT, 3=PARAM-RANGE, 4=POWER, 5=PARITY |
| `kuramoto` | `F-AKIDA-KU-` | 1=R-COHERENCE(>0.7), 2=K-CRITICAL, 3=SPIKE-COUPLE, 4=POWER, 5=PARITY |
| `memristor_hybrid` | `F-AKIDA-MEM-` | 1=1SHOT-LEARN, 2=WEIGHT-PERSIST, 3=POWER-CYCLE, 4=POWER, 5=PARITY |
| `sparse_attention` | `F-AKIDA-SA-` | 1=SPARSITY-RATIO, 2=ATTN-MAX, 3=8BIT, 4=POWER, 5=PARITY |
| `spike_tier_lm_head` | `F-AKIDA-LMH-` | 1=LOGIT-SHAPE, 2=ARGMAX-STABLE, 3=QUANT-OK, 4=POWER, 5=PARITY |
| `motivation_gate` | `F-AKIDA-MG-` | 1=THRESHOLD-FIRE, 2=EMIT-CADENCE, 3=POWER-1MW, 4=AUDIT-WRITE, 5=PARITY |
| `theta_gamma` | `F-AKIDA-TG-` | 1=PAC, 2=THETA-LOCK, 3=GAMMA-NEST, 4=POWER, 5=PARITY |
| `eeg_pattern` | `F-AKIDA-EEG-` | 1=PATTERN-MATCH, 2=MU-RHYTHM, 3=SLEEP-STAGE, 4=POWER, 5=PARITY |
| `spontaneous_gate` | `F-AKIDA-SG-` | 1=EMIT-RATE, 2=GATE-CLOSED, 3=AUDIT-LINK, 4=POWER, 5=PARITY |
| (overlap) | (—) | (N3 memristor_hybrid 동일) |

`selftest()` 반환:
```python
{
    "name": "snn_lif",
    "passed": 5,
    "failed": 0,
    "details": [
        {"id": "F-AKIDA-SNN-1", "pass": True, "metric": 42, "limit": 40, "note": "spike_count >= limit"},
        ...
    ],
}
```

aggregate runner = `pack/falsifiers/run_all.py` (별도 agent).
`python -m pack.falsifiers.run_all` → `state/mac_validation_<UTC>/run.log`.

---

## §5 demiurge integration

각 adapter 의 `to_record()` → demiurge brain producer 가 인용.

### §5.1 record format

`demiurge_brain_bridge.py` 의 기존 backend dict 와 자리-호환:

```python
{
    "adapter": "snn_lif",
    "backend": "akida_hw" | "akida_mock",
    "ts_utc": "2026-05-21T13:42:00Z",
    "substrate_origin": "engines/snn_consciousness.hexa",
    "params": {"n_cells": 8, "tau_m": 0.020},
    "selftest": { ... aggregate from §4 ... },
    "emit": {"motivation": 0.83, "fired": True, "power_mw": 0.9} | None,
}
```

### §5.2 drop path

```
AUX/AKIDA/pack/adapters/<X>.py
    → adapter.to_record()
    → exports/brain/verify/<UTC>Z/anima_akida_<adapter>_<UTC>.json
    → demiurge cli action verify brain
    → GATE_CLOSED if all 11 records present + selftest 5/5 PASS each
```

Path convention 은 `../../anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`
의 기존 `local_sim` / `akida_cloud` / `loihi2_nrc` backend 와 동일 directory
구조 답습.

### §5.3 backend label

| Source | `backend` 값 |
|---|---|
| 실 AKD1000 silicon | `"akida_hw"` |
| Mac local mock | `"akida_mock"` |
| Akida Cloud trial (Phase 2) | `"akida_cloud"` (별도 path) |

demiurge gate 는 `akida_hw` 만 fresh evidence 로 인정; `akida_mock` 은
pre-arrival validation 표식.

---

## §6 향후 확장 후보

본 pack 0.1.0 이후의 spec-tier roadmap (구현 X).

### §6.1 AKD2000 / AKD3000 transition

- AKD2000: 4M neuron, FP16 지원, on-chip Vision Transformer
- AKD3000: 1.2B param spike-tier LLM (BrainChip 2026 roadmap)
- migration: `pack.runtime.metatf_runtime` 의 `_try_import_akida_hw()`
  추가 device probe 만 변경, adapter layer 무영향.

### §6.2 IBM TrueNorth fallback

- 1M neuron / 256M synapse, IBM Research only
- adapter base 의 `backend` field 만 추가, `"truenorth_research"` label.
- spec-tier only (research access 없음).

### §6.3 ESP32 + AKD1000 (M.2 PCIe → ESP32 SDIO bridge)

- Pi 5 없이 ESP32 host 가 AKD1000 driving (BOM $20 vs $1495)
- PCIe → SDIO bridge IC 필요 (e.g., RTS5260)
- Phase 3 spec-tier; Pi 5 도착 후 별도 평가.

### §6.4 Akida Cloud (Phase 2 trial)

- `backend="akida_cloud"` 로 별도 path.
- `AUX/hw/PHASE_2_CLOUD_TRIAL.md §2.1` 참조.
- 본 pack 의 mock fallback 과 orthogonal — cloud trial 은 실 silicon
  evidence 이므로 `akida_hw` 동급 (별도 label 로만 분리).

---

## §7 cross-link

- root: [`../../anima-physics/AUX/README.md`](../../anima-physics/AUX/README.md) — pack 사용법 §9-§12
- validation 결과: [`VALIDATION.md`](VALIDATION.md)
- Day 1-7 boot: [`BOOT_PLAN.md`](BOOT_PLAN.md)
- architecture diagram: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- runtime source: [`../pack/runtime/`](../pack/runtime/)
- mock source: [`../pack/mocks/`](../pack/mocks/)
- demiurge bridge (기존 pattern): `../../../anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`
