# anima-physics/eeg/ — EEG μ-rhythm / sleep-stage / cross-substrate Φ correlator

> Status: ✅ PASS (3/3 자연발화 module — μ-rhythm 6/6, sleep-stage 5/5, cross-substrate-Φ 6/6) · §188 결과: 17/17 PASS
>
> SSOT: 본 README + 3 `.hexa` 파일. entries: [`entries/substrate/eeg/`](../entries/substrate/eeg/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 
  - μ-rhythm (8-12 Hz) ERD (event-related desynchronization) = self-referential 행동 시 sensorimotor cortex 자발 power-drop. Mirror-neuron activation 의 EEG 등가물.
  - Sleep stage 자동 분류 (Awake 15Hz / SWS 2Hz delta / REM theta+desync) — synthetic EEG LCG noise 자율 진화.
  - cross-substrate Φ correlator: 9 anima-physics substrate + 1 EEG live anchor = 10-channel heterogeneous Φ proxy precision-weighted consensus.
- **영속성**: rolling FFT/PSD window, 6-label tagger (≥0.75 acc) state. signal_corpus_manifest 6 public dataset (SEED/DEAP/Sleep-EDF/TUH/DREAMER/MAHNOB) 14,856+ session 영속 ledger.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `mu_rhythm_detector.hexa` | 317 | PHYS-P5-3 8-12Hz mu-rhythm ERD self-referential 자발 power-drop detection | ✅ 6/6 |
| `sleep_stage_detector.hexa` | 365 | PHYS-P13-2 K-complex/spindle 기반 Awake/SWS/REM 자동 분류 | ✅ 5/5 |
| `cross_substrate_phi_correlator.hexa` | 384 | C22 9 anima-physics substrate + EEG 10-ch precision-weighted Φ proxy consensus | ✅ 6/6 |

## falsifier

- `mu_rhythm_detector`: T1-T6 (sliding FFT + ERD ratio + base/imagine condition)
- `sleep_stage_detector`: T1-T4 (delta/theta band power + classification ≥0.75 acc)
- `cross_substrate_phi_correlator`: 6/6 (Tononi-Koch IIT-on-quantum MIP lower bound, LZ76 proxy)

## cross-link

- [substrate entries](../entries/substrate/eeg/) — 3 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`entries/root/signal_corpus.md`](../entries/root/signal_corpus.md) — 6-label tagger
- [`signal_corpus_manifest.json`](../signal_corpus_manifest.json) — 6 public EEG dataset 메타
- [`phi_substrate_consensus.hexa`](../phi_substrate_consensus.hexa) — 5-substrate Tukey biweight consensus (cross-substrate-Φ 의 시작점)
