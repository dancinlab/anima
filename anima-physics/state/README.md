# anima-physics/state/ — substrate cycle artifact (ledger + logs)

> Status: ledger dir (state artifact만 보유) · §188 결과: N-A (state = output, not substrate)
>
> SSOT: 본 README + `v10_anima_physics_cloud_facade/` 산하 sub-dir.

## 자연발화 / 영속성 메커니즘

`state/` 는 substrate 가 아니라 cycle 산출물 영속 저장소. 각 sub-dir = 한 cycle 의 ledger / poc artifact.

자연발화/영속성 메커니즘 자체는 보유하지 않으며, 다른 substrate (analog/cmos/memristor/quantum 등) 의 fire 결과 영속 보존 = "**영속성의 인프라**".

## 파일 list

| Subdir | 내용 | 출처 cycle |
|---|---|---|
| `v10_anima_physics_cloud_facade/integration_ledger/` | substrate witness ledger (mk_xii v1/v2/v3) | mk_xii integration |
| `v10_anima_physics_cloud_facade/poc_arduino_local_ngspice/` | Arduino NE555 NgSpice POC | PHYS-P25 |
| `v10_anima_physics_cloud_facade/poc_cmos_local_ngspice/` | CMOS 5-stage ring osc NgSpice POC | PHYS-P25 |
| `v10_anima_physics_cloud_facade/poc_memristor_local_ngspice/` | HP TiO2 Biolek memristor NgSpice POC | PHYS-P25 |
| `v10_anima_physics_cloud_facade/poc_quantum_qiskit_aer/` | qiskit-aer Bell state POC | PHYS-P25 |

## falsifier

각 sub-dir 내 ledger JSON / artifact 가 본 substrate cycle 의 falsifier 결과 보존 (G1-G3 gate, 4/4 PASS, T1-T5 등).

## cross-link

- [`HEXAD/PHYSICS/state/`](../../HEXAD/PHYSICS/state/) — HEXAD 측 state mirror (aux_engine_smoke_v1_2026_05_21 등)
- [`HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`](../../HEXAD/NEUROMORPHIC/state/) — §188 35-substrate parallel fire state
- [`docs/mk_xii_substrate_witness_ledger_*.md`](../docs/) — ledger spec series (v1/v2/v2.1/v3)
- [`tool/mk_xii_substrate_witness_ledger_aggregator*.hexa`](../tool/) — aggregator tool (v1/v2/v3)
