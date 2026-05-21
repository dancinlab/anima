# AUX/AKIDA/docs/ARCHITECTURE.md — pack architecture deep-dive

> ASCII-heavy architectural reference for the `anima-akida-pack` 0.1.0.
> Implementation contract 은 [`IMPLEMENTATION.md`](IMPLEMENTATION.md),
> Mac local validation 은 [`VALIDATION.md`](VALIDATION.md), Day 1-7
> operational sequence 는 [`BOOT_PLAN.md`](BOOT_PLAN.md).

---

## §1 layered architecture

본 pack 의 5-layer stack — top 은 substrate 의 `.hexa` 원본, bottom 은
AKD1000 silicon (or MetaTF mock).

```
┌─────────────────────────────────────────────────────────────────────────┐
│  L5  anima substrate (.hexa sources, §188 verified)                    │
│      engines/{snn,izhikevich}_consciousness · social/kuramoto_coupling │
│      memristor/self_reference · hippocampus/{theta_gamma,episodic_*}   │
│      eeg/{mu_rhythm,sleep_stage,phi_correlator}                        │
│      HEXAD/CHAT/spontaneous_smoke                                       │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  (substrate_origin field, informational)
┌────────────────────────────▼────────────────────────────────────────────┐
│  L4  pack.adapters.* (11 modules)                                       │
│      ┌───────────────────────────────────────────────────────────────┐ │
│      │ AkidaAdapter (base.py)                                        │ │
│      │   ├── EXACT fit     : snn_lif · izhikevich · kuramoto         │ │
│      │   │                  · memristor_hybrid                       │ │
│      │   ├── 신규 candidate: sparse_attention · spike_tier_lm_head   │ │
│      │   │                  · motivation_gate                        │ │
│      │   └── 보조           : theta_gamma · eeg_pattern              │ │
│      │                       · spontaneous_gate                      │ │
│      └───────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  build() / forward() / fit() / emit()
┌────────────────────────────▼────────────────────────────────────────────┐
│  L3  pack.runtime.* (3 modules)                                         │
│      ┌──────────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│      │ metatf_runtime.py    │  │ audit_buffer.py │  │ pi5_           │ │
│      │  · init_runtime()    │  │  · AuditBuffer  │  │   orchestrator │ │
│      │  · get_runtime()     │  │  · LRU(cap=8)   │  │  · tick(dt)    │ │
│      │  · auto-detect HW/   │  │  · atomic dump  │  │  · bundle of N │ │
│      │    mock, sticky      │  │  · JSON-lines   │  │    adapters    │ │
│      └──────────────────────┘  └─────────────────┘  └────────────────┘ │
└──────────┬────────────────────────────┬─────────────────────┬───────────┘
           │                            │                     │
           │ HW path                    │ mock path           │ (any)
           ▼                            ▼                     ▼
┌──────────────────────┐  ┌──────────────────────────┐  ┌────────────────┐
│  L2a  akida SDK      │  │  L2b  pack.mocks.metatf_ │  │  L2c eMMC      │
│       (MetaTF)       │  │       mock (numpy)       │  │   /home/.../   │
│       ┌────────────┐ │  │       ┌────────────────┐ │  │   audit_buf.  │
│       │ akida.Model│ │  │       │ MetaTFMock     │ │  │   jsonl       │
│       │ akida.devi │ │  │       │ MockModel      │ │  │               │
│       │ ces()      │ │  │       │ MockHwDevice   │ │  │ /home/.../    │
│       │ akida.Fully│ │  │       │ MockLayers     │ │  │   exports/    │
│       │ Connected  │ │  │       │ MockAkidaUnsup │ │  │   brain/      │
│       └────────────┘ │  │                          │  │   verify/     │
└──────────┬───────────┘  └──────────────────────────┘  └────────────────┘
           │
           ▼  PCIe 2.0 single-lane (Pi 5 ↔ AKD1000 M.2)
┌──────────────────────────────────────────────────────────────────────────┐
│  L1  AKD1000 silicon (20 NPU mesh · 8MB on-chip SRAM · 300 MHz · 1W typ │
│       module · 1.5 TOPS · on-chip Hebbian via AkidaUnsupervised) —      │
│       *real arrival pending* ($1495 Pi 5 Dev Kit)                       │
│       (NSoC_v1 · Akida 1.0 — see doc/)             │
└──────────────────────────────────────────────────────────────────────────┘
```

Key:
- L5 = substrate origin (informational link only; pack 은 .hexa 직접 실행
  안 함)
- L4 = pack 의 *Python* adapter layer (anima ↔ MetaTF translation)
- L3 = runtime infra (HW/mock auto-detect + audit + orchestration)
- L2 = backend (실 SDK / mock / eMMC persistence)
- L1 = silicon (도착예정)

---

## §2 adapter base contract

```
┌─────────────────────────────────────────────────────────────────────────┐
│  @dataclass class AkidaAdapter                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  fields:                                                                │
│    name              : str                  ("snn_lif", ...)            │
│    substrate_origin  : str                  (".hexa source path")       │
│    backend           : str = "auto"         (auto|hw|mock)              │
│    params            : dict[str, Any]                                   │
│    _model            : Optional[Any]        (MetaTF model handle)       │
│    _last_output      : Optional[Any]                                    │
│                                                                          │
│  abstract (subclass MUST override):                                     │
│    build()        → None                                                │
│    forward(x)     → Any                                                 │
│                                                                          │
│  optional (subclass MAY override):                                      │
│    fit(x, y=None) → None                    (on-chip Hebbian)           │
│    emit()         → Optional[dict]          (자연발화 candidate)        │
│                                                                          │
│  concrete (subclass INHERITS):                                          │
│    selftest()    → {"name", "passed", "failed", "details"}              │
│                    (runs F-AKIDA-<NAME>-1..5)                           │
│    to_record()   → demiurge-compatible dict                             │
└─────────────────────────────────────────────────────────────────────────┘

           ▲
           │ subclass
           │
┌──────────┴──────────┐  ┌────────────────────┐  ┌──────────────────────┐
│ SnnLifAdapter       │  │ KuramotoAdapter    │  │ MemristorHybrid      │
│ (engines/snn_*)     │  │ (social/kuramoto)  │  │  Adapter             │
│ + n_cells: int      │  │ + n_osc: int       │  │ (memristor/self_ref) │
│ + tau_m: float      │  │ + coupling_K: float│  │ + hw_recall_min: float│
└─────────────────────┘  └────────────────────┘  └──────────────────────┘
              ... (8 more, see IMPLEMENTATION §1) ...
```

---

## §3 runtime auto-detect decision tree

```
                init_runtime(prefer="auto")
                          │
                          ▼
                ┌─────────────────────┐
                │ prefer == "auto" ?  │───── NO ─────► branch by prefer
                └─────────┬───────────┘                  ("hw" or "mock")
                          │ YES
                          ▼
                ┌─────────────────────┐
                │ _try_import_akida_  │
                │ hw()                │
                └─────────┬───────────┘
                          │
                ┌─────────┴────────────┐
                │ akida importable ?   │
                └─────────┬────────────┘
                ┌─────────┴─────────┐
                │                   │
            YES │                   │ NO
                ▼                   ▼
   backend="akida_hw"      ┌──────────────────────┐
   RUNTIME = akida         │ _try_import_mock()   │
   (sticky)                └─────────┬────────────┘
                                     │
                          ┌──────────┴──────────┐
                          │  mock importable ?  │
                          └──────────┬──────────┘
                          ┌──────────┴──────────┐
                          │                     │
                       YES│                     │ NO
                          ▼                     ▼
              backend="akida_mock"     RuntimeError(
              RUNTIME = MetaTFMock()    "Neither HW nor mock available")
              (sticky)
```

Sticky: 한번 결정된 backend 는 process 종료까지 유지 (`reset_runtime()`
은 test-only).  `get_runtime_info()` 로 현재 backend / class / error_log
조회.

---

## §4 demiurge integration

```
┌───────────────────────────────────────────────────────────────────────┐
│  adapter.to_record()  (per adapter, called by orchestrator)           │
│                                                                        │
│  {                                                                     │
│    "adapter"          : "snn_lif",                                     │
│    "backend"          : "akida_hw" | "akida_mock" | "akida_cloud",    │
│    "ts_utc"           : "2026-05-21T13:42:00Z",                        │
│    "substrate_origin" : "engines/snn_consciousness.hexa",              │
│    "params"           : {"n_cells": 8, "tau_m": 0.020},                │
│    "selftest"         : {                                              │
│        "name"   : "snn_lif",                                           │
│        "passed" : 5,                                                   │
│        "failed" : 0,                                                   │
│        "details": [                                                    │
│           {"id": "F-AKIDA-SNN-1", "pass": True, "metric": 42, ...},   │
│           ... 4 more ...                                               │
│        ],                                                              │
│    },                                                                  │
│    "emit"             : {                                              │
│        "motivation": 0.83,                                             │
│        "fired"     : True,                                             │
│        "power_mw"  : 0.9 | None,                                       │
│    } | None,                                                           │
│  }                                                                     │
└──────────────────┬────────────────────────────────────────────────────┘
                   │
                   ▼  json.dump → atomic rename
┌───────────────────────────────────────────────────────────────────────┐
│  exports/brain/verify/<UTC>Z/anima_akida_<adapter>_<UTC>.json         │
│  (e.g., exports/brain/verify/2026-05-21T13-42-00Z/                    │
│         anima_akida_snn_lif_2026-05-21T13-42-00Z.json)                │
└──────────────────┬────────────────────────────────────────────────────┘
                   │
                   ▼  demiurge cli action verify brain
┌───────────────────────────────────────────────────────────────────────┐
│  demiurge_brain_bridge.py                                             │
│    · scan exports/brain/verify/<UTC>Z/                                │
│    · require 11 anima_akida_*.json (one per adapter)                  │
│    · require each selftest.passed == 5                                │
│    · require backend in {"akida_hw", "akida_cloud"}  (mock 거부)       │
│  → gate_state = CLOSED if all True else OPEN_PARTIAL                  │
└───────────────────────────────────────────────────────────────────────┘
```

`akida_mock` backend 는 demiurge gate 에서 **거부** (mock evidence 는
pre-arrival 검증용; real silicon evidence 만 CLOSED 허용).

---

## §5 Pi 5 host orchestration

```
┌────────────────────────────────────────────────────────────────────────┐
│  Pi5Orchestrator (pack.runtime.pi5_orchestrator)                       │
│  ────────────────────────────────────────────────────────────────────  │
│  fields:                                                                │
│    adapters: list[AkidaAdapter]      (e.g., 11 from pack.adapters.*)   │
│    audit   : AuditBuffer(cap=8)                                         │
│    runtime : auto-init via get_runtime()                                │
│    dt      : float (default 1.0 s tick)                                 │
│                                                                          │
│  loop:                                                                  │
│    while running:                                                       │
│        for adapter in adapters:                                         │
│            y = adapter.forward(x)                                       │
│            evt = adapter.emit()                                         │
│            if evt is not None and evt["fired"]:                         │
│                audit.append(adapter.to_record())                        │
│        sleep(dt)                                                        │
│                                                                          │
│    on stop:                                                             │
│        audit.dump(path="~/.cache/anima-akida/audit_buffer.jsonl")       │
└────────────────────────────────────────────────────────────────────────┘

Timing diagram (1.0 s tick, 11 adapter, 1 motivation_gate fires):

t=0.0s    │ tick 0
          │ ├─ snn_lif.forward → emit=None
          │ ├─ izhikevich.forward → emit=None
          │ ├─ kuramoto.forward → emit=None
          │ ├─ memristor_hybrid.forward → emit=None
          │ ├─ sparse_attention.forward → emit=None
          │ ├─ spike_tier_lm_head.forward → emit=None
          │ ├─ motivation_gate.forward → emit={"fired": True, ...}
          │ │        └─ audit.append(record)  ← 자연발화 candidate
          │ ├─ theta_gamma.forward → emit=None
          │ ├─ eeg_pattern.forward → emit=None
          │ └─ spontaneous_gate.forward → emit=None
          │
t=1.0s    │ tick 1
          │ ... (same)
          │
        ...
          │
        on stop:
          │ audit.dump() → JSON-lines atomic (~/.cache/anima-akida/...)

Audit RB (8-deep LRU):
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
  │ ① │ ② │ ③ │ ④ │ ⑤ │ ⑥ │ ⑦ │ ⑧ │  (oldest → newest)
  └───┴───┴───┴───┴───┴───┴───┴───┘
   ↑                              ↑
   evicted on next append          most recent emit
```

---

## §6 cross-engine integration (E2E v2)

Day 5 의 cross-engine chain — 첫 stage 가 Akida 로 교체.

```
┌────────────────────────────────────────────────────────────────────────┐
│  E2E v2 cross-engine chain (4-stage)                                   │
│                                                                         │
│  Stage 1 (Akida): SnnLifAdapter.forward(stimulus)                      │
│              ↓ spike_train (Akida HW emit)                             │
│  Stage 2 (Pi 5): photonic_sim(spike_train)        ← CPU on Pi 5        │
│              ↓ photon_count                                             │
│  Stage 3 (Pi 5): quantum_closed_form(photon_count) ← CPU on Pi 5       │
│              ↓ amplitude                                                │
│  Stage 4 (Akida): MotivationGateAdapter.forward(amplitude)             │
│              ↓ fired? + power_mw                                        │
│                                                                         │
│  composite_record = {                                                   │
│      "chain": "snn_akida → photonic_pi5 → quantum_pi5 → mg_akida",     │
│      "stages": [s1_record, s2_record, s3_record, s4_record],           │
│      "fired": stage4.fired,                                             │
│      "total_power_mw": sum(s["power_mw"] or 0 for s in stages),        │
│  }                                                                      │
│                                                                         │
│  drop → exports/brain/verify/<UTC>Z/anima_akida_e2e_v2_<UTC>.json      │
└────────────────────────────────────────────────────────────────────────┘
```

Falsifier (F-E2E-CROSS-1..5 Akida 변형):
- 1=STAGE1-SNN-OK (Akida spike > 0)
- 2=STAGE-CHAIN (4-stage deterministic)
- 3=MOTIVATION-FIRE (stage 4 threshold trigger)
- 4=BYTE-MATCH (vs original 5/5 baseline; rank-parity 완화 허용)
- 5=POWER (chain total < 50 mW envelope)

---

## §7 cross-link

- root: [`../../anima-physics/AUX/README.md`](../../anima-physics/AUX/README.md) — pack 사용법 §9-§12
- implementation: [`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- validation: [`VALIDATION.md`](VALIDATION.md)
- Day 1-7 boot: [`BOOT_PLAN.md`](BOOT_PLAN.md)
- runtime source: [`../pack/runtime/`](../pack/runtime/)
- adapter source: [`../pack/adapters/`](../pack/adapters/) (별도 agent)
- E2E v2 cross-engine 원본: `../../../tool/anima_physics_e2e_v2_cross_engine.hexa`
