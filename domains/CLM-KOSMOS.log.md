# CLM-KOSMOS.log.md — progress log

@title: 📓 CLM-KOSMOS log — append-only (newest at bottom)

Sibling of [[CLM-KOSMOS]]. Each entry: date · what moved · verdict ptr.

## 2026-06-01 — e001 seed

도메인 CREATED. CLM(`.clm`) + KOSMOS(`.kosmos`) 메타도메인, 7 필수조건 기록 (C1 AKIDA-learn · C2 ONCHIP-PARADIGM · C3 .clm · C4 .kosmos/limen · C5 H_911-must-hold · C6 additional-hypotheses · C7 record-all). Falsifier **F-CLM-AKIDA-MULTILING-SEMANTIC** pre-registered (OPEN). Seed corpus on HF: `dancinlab/clm-semantic-parallel-corpus` (5-lang parallel · 🟡 CPU-proxy → on-chip 승격 대상). H_911 substrate-proxy 이미 🟢 (UNIVERSE/H_911).

## 2026-06-01 — e002 open work

- [x] 1. 실 5-lang parallel + concat `.kosmos @corpus` 작성 (limen-packed · closed_corpus merkle)
- [x] 2. 백본 → `.clm` int4 byte-identical AKD1000 이식 (H_877)
- [x] 3. `AkidaUnsupervised` on-chip edge-learn (pi5-akida — lock cleared · live)
- [x] 4. F-CLM-AKIDA-MULTILING-SEMANTIC parallel vs concat 측정 → `.verdicts/clm-akida-multiling-semantic/`
- [x] 5. 🔴 closed-negative → verdict+log land only (model NOT uploaded — 🔴 earns no `.clm`)

## 2026-06-01 — e003 on-chip run → 🔴 REFUTED (closed-negative)

**F-CLM-AKIDA-MULTILING-SEMANTIC: 🔴 REFUTED** on REAL AKD1000 silicon (BC.00.000.002 · NSoC_v2 · BackendType.Hardware · akida 2.19.1 · pi5-akida).

- **Stage 0 (gate, PASSED)**: device 가 `devices:[]` + `ERROR (file lock): 11` 였던 원인 = stale `spike_streamer.py` (PID 18439, 17h, `--duration 86400`) 가 `/dev/akida0` (fd 3·4) 점유. 그 holder 종료 → `akida.devices()` 가 real `HardwareDevice` 반환. SW-sim 대체 없음 (g63).
- **Stage 1 (C4)**: 5-lang(ko·en·zh·ru·ja) parallel(concept-major·c>0) + concat(lang-major·c~0) `.kosmos @corpus`, 25 anchor 각, hexa-lang `clm_semantic_{parallel,concat}.txt` 에서 VERBATIM seed. limen 패킹(magic `LIMEN\0\0\0`+ver+count+len-prefixed @anchor recs+merkle root)·profile·closed_corpus·placement(coord)⊥text 완전 준수. byte-identical payload multiset (order 만 차이) 확인.
- **Stage 2 (H_877)**: int4-sym backbone(256×256, sha256=c626c638…) 양 arm byte-identical front-end.
- **Stage 3 (C1·C2)**: `AkidaUnsupervised(num_weights=16, learning_competition=0.1)` · `FC(units=32,weights_bits=1)` · `model.fit()` ON CHIP. `learn_happened_hw=True` — N=12 paired trial 전부 live silicon 학습.
- **Stage 4 (C5)**: paired delta(parallel−concat 통합) = **6 pos / 6 neg · mean −0.00092 · 95%CI [−0.00319,+0.00135] (straddle 0)**. ⚠ 단일 run 은 H_904 stochastic-plasticity 로 🟢(+0.0072)↔🔴(−0.0042) flip → cherry-pick 거부, multi-trial 必. **H_911 의 semantic-linkage 우위가 AKD1000 last-layer Hebbian edge-learn 엔 전이 안 됨** — per-ordering gap 이 칩 noise 안에 묻힘. **closed-negative, publishable** (a_paper_negative_ok).

verdict → `.verdicts/clm-akida-multiling-semantic/` (result.txt · result.json · run.log · prereg.txt · corpus/ · scripts/). claim → CLAIMS.tape `clm_akida_multiling_semantic`. 🔴 이므로 HF 모델 업로드 없음.
