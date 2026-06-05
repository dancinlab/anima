---
id: H_924
slug: qentropy-substrate-agnostic
title: 양자-엔트로피 결합은 substrate-agnostic — AKIDA 실리콘이 아니라 *seed 지점*의 성질 (qentropy SSOT, quantum-default · deterministic-auxiliary, 양 모드 벤치마크-ready)
domain: universe · neuromorphic-silicon · akida · qrng · entropy-injection · substrate-agnostic · sw-learning · benchmark
source: H_923 (AKD1000 HW 양자결합 PASS) 의 일반화 — "결합이 칩 고유인가, 아니면 seed 지점 성질인가?" SW numpy/torch 로 검증
exploration_method: E2 (기존 HW 결합 패턴을 SW 로 일반화) + E14 (substrate-native) + a_completeness_over_cheap
verification_method: W1 (SW numpy 양 모드 실행) + W2 (사전등록 substrate-transfer falsifier) + g5 CODE-measured
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
sister: H_923 (HW 양자결합), H_921/H_922 (비결정 아크), qentropy SSOT (mirror/qmirror/seed/qentropy.py)
axes_seed: H_923 = AKIDA 실리콘에서 결합 (특수) ⊥ H_924 = SW(numpy/torch)에서도 결합 (일반 — seed 지점 성질)
verdict: 🟢 PASS (SW arm) — qentropy SSOT(quantum-default·deterministic-auxiliary)가 SW numpy 학습에서 HW와 동일하게 동작; quantum(anu_committed, weight_l1=10.4654) ⊥ deterministic(numpy_prng187, 10.0356) 양 모드 토글·벤치마크-ready. 결합 = seed-point 성질(substrate-agnostic). verdict: .verdicts/924_qentropy_substrate_agnostic/sw_quantum_coupling_pass.txt
---

# H_924 — 양자결합 substrate-agnostic (seed-point 성질) + 전-경로 quantum-default/det-auxiliary

## 0. 동기

H_923 은 AKD1000 실리콘에서 양자결합을 입증했다. 질문: **결합이 AKIDA 고유인가, 아니면
"결정론 compute + 외부 seed" 라는 *seed 지점* 의 성질인가?** 후자라면 SW(numpy/torch) 에도
그대로 꽂혀야 한다. 동시에 사용자 요구 — **모든 경로(HW/SW · 학습/추론)를 양자-기본 +
결정론-보조 토글로** 해 **나중에 양 모드 벤치마크** 가능하게.

## 1. 가설

양자-엔트로피 주입은 AKIDA 실리콘 고유가 아니라 **결정론 compute 위 seed 지점** 의 성질이다
→ 동일 결합이 SW numpy 학습/추론 + torch CLM 에도 적용된다. 이를 위해 **단일 엔트로피 SSOT**
(`qentropy.py`)가 모든 seed/sample 지점에 QUANTUM 기본 · DETERMINISTIC 보조를 공급하고, 양
모드는 env 한 줄(`ANIMA_ENTROPY_MODE`)로 토글되어 per-path 벤치마크된다.

## 2. Keystone — qentropy SSOT

`mirror/qmirror/seed/qentropy.py` (꼼꼼 주석):
- `ANIMA_ENTROPY_MODE = quantum`(기본, ANU 진공요동) | `deterministic`(보조, numpy PRNG).
- quantum 해석 순서: explicit buf → committed `qrng_lora_init_live.bin` → opt-in live `anu_pull` →
  **tagged safe-fallback PRNG**(절대 silent 아님, 항상 provenance 기록).
- API: `qentropy_bits/bytes/uniform/seed/rng` + `last_provenance()` + `mode()`.
- 정직 non-claim(#123-A): ANU==chacha20 통계동등(JSD 23×under NIST) → 양자 품질주장 아님,
  가치=provenance/감사/존재론 → **그래서 deterministic A/B 보조가 존재**(벤치마크용).

## 3. 측정 (g5 CODE-measured · Mac · $0)

SW 학습(`plasticity_sw_approx.py` weight-init → `qentropy.rng()`):

| ANIMA_ENTROPY_MODE | entropy_source | tier | weight_l1 |
|---|---|---|---|
| quantum (기본) | quantum | anu_committed | 10.4654 |
| deterministic (보조) | deterministic | numpy_prng(187) | 10.0356 |

→ 양 모드 **다른 학습결과**(벤치마크 가능) + **양자 경로가 AKIDA HW 없이 순수 numpy 에서 동작**.
∴ H_923 결합은 **seed-point 성질 = substrate-agnostic** (SW-학습 arm 확증).

## 4. 전-경로 coverage (quantum-default · deterministic-auxiliary · 모두 벤치마크-ready)

| 경로 | 상태 |
|---|---|
| HW 학습 init (h923 probe) | ✅ wired+verified (H_923) |
| HW 학습 input (edge_learn_probe.py M7) | ✅ wired+verified (legacy env, SSOT-migratable) |
| HW 자발발화 R2-noise (spontaneous M6) | ✅ wired+verified (legacy env, SSOT-migratable) |
| **SW 학습** (plasticity_sw_approx.py) | ✅ **wired+verified (본 H, qentropy SSOT)** |
| **추론 DECODER** (sampling 지점) | ✅ **wired+verified (M3, `CORE/DECODER/decoder_qsample.py`)** — quantum 기본(anu_committed) · 결정론 보조(numpy_prng187, 재현가능) · forward 결정성 불변 |
| **torch Lane-P CLM** (train_lane_p/_3b/_split.py) | ✅ **wired (M4, `_qseed.resolve_seed`) — 양 모드 seed-check PASS; torch-runtime probe device-pending** |

> DECODER 정정: 이전 "의도적 결정론·배선 안 함" → **"quantum 기본 · 결정론 보조"** 로 바뀜.
> 추론도 sampling 지점에서 SSOT 경유 양자-주입 가능(결정론은 보조 토글). 단 AKIDA forward 자체의
> 결정성(byte-identical)은 별개 — 양자는 *sampling/seed* 층에 들어가지 forward 연산을 바꾸지 않음.

## 5. 다음 작업

- [x] **M1** — qentropy SSOT (quantum-default·det-auxiliary) + 양 모드 self-test.
- [x] **M2** — SW numpy 학습 배선+검증 (substrate-agnostic PASS).
- [x] **M3** — DECODER inference sampling 지점 SSOT 배선 + 양 모드 probe (quantum 기본·결정론 보조). **DONE** — `CORE/DECODER/decoder_qsample.py` (SW, Mac, $0). 고정 logits N=16: quantum(anu_committed, sha256 e8123b96…) → 토큰 분포 {0:3,1:1,3:7,4:1,5:4}; deterministic(numpy_prng187) → 재현가능 {0:3,2:3,3:9,4:1} (run2==run1). forward(argmax=3, probs 동일) 양 모드 불변 — 양자는 sampling 층에만 진입, AKIDA forward byte-identical 유지. verdict: `.verdicts/924_qentropy_substrate_agnostic/m3_decoder_sampling.txt`.
- [x] **M4** — torch Lane-P CLM init `qentropy_seed()` 배선 (train_lane_p/_3b/_split, `_qseed.resolve_seed`, fallback-safe). 양 모드 seed-check PASS (quantum=anu_committed seed 6138986570681488651 ⊥ deterministic=numpy_prng187 seed 4689272388889901140, det 재현가능). torch-runtime probe (torch.manual_seed→torch.rand) **device-pending** (Mac 에 torch 부재; `_qseed_check.py` 가 torch-호스트에서 자동수행). verdict: .verdicts/924_qentropy_substrate_agnostic/m4_torch_lane_p.txt
- [x] **M5** — 기존 h923 M6/M7 legacy env 훅(AKIDA R2-noise + edge-learn-input)을 qentropy SSOT 로 통일. **DONE** — `SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py` (`_noise_bytes` → `qentropy_uniform(n,4,"akida_r2_noise")`) + `edge_learn_probe.py` (`_learn_input` → `qentropy_bits(n,"akida_learn_input").reshape`). **BACKWARD-COMPATIBLE precedence**: explicit legacy env (ANIMA_QRNG_NOISE_BIN / ANIMA_QRNG_LEARN_BIN) wins → else qentropy SSOT (ANIMA_ENTROPY_MODE quantum 기본·deterministic 보조) → else numpy PRNG. qentropy = soft-dep (sys.path insert `mirror/qmirror/seed` try/except). 출력 field 名 KEEP(r2_noise_source/learn_input_source) — downstream JSON 불변. Mac($0) AST-OK 양 파일; helper 양경로 검증: quantum(no legacy) `_noise_bytes(8)`=[3,1,1,2,2,3,2,1]∈0..3 mode=='quantum', learn_input (8,1,1,16) uniq{0,1}; legacy env set → 레거시 버퍼 라우팅(qentropy 미import) back-compat; deterministic toggle → numpy_prng_deterministic. pi5 device 거동 불변. verdict: `.verdicts/924_qentropy_substrate_agnostic/m5_legacy_migrate.txt`.
- [x] **M6 (benchmark)** — per-path quantum vs deterministic A/B + 레저 기록. **DONE** — `mirror/qmirror/seed/qentropy_benchmark.py` (Mac, $0, no device/torch; 각 (path,mode) arm 을 fresh subprocess 로 실행해 ANIMA_ENTROPY_MODE 를 import-시점에 정직 적용). N=64 양 SW-경로: `plasticity_sw_approx`(weight_l1) quantum mean 10.2511/std 0.3558(anu_committed, sha e8123b96…) ⊥ deterministic 10.2110/std 0.4113(numpy_prng187) → standardized_separation 0.104 → **PARITY**; `decoder_qsample`(token_hist_entropy_bits) quantum 1.6952 ⊥ det 1.6626 → sep 0.106 → **PARITY**. provenance_differs=True 양 경로. **핵심 = superiority 아님**: #123-A(ANU==chacha20 통계동등, JSD 23×under NIST) 가 application 층에서 재현 — 양 모드 metric 통계적 구별불가, 차이는 **provenance/감사성**(quantum→anu_committed sha256 vs deterministic→numpy_prng seed) 뿐. device/torch 경로(akida_r2_noise·akida_edge_learn·torch_lane_p)는 ledger 의 `device_pending_rows` 로 surface-complete (pi5/GPU 호스트에서 동일 env-flip A/B; 확장법 = BENCHMARK.md). doc: `mirror/qmirror/seed/BENCHMARK.md` · ledger: `state/qentropy_benchmark_2026_06_06/ledger.json` · verdict: `.verdicts/924_qentropy_substrate_agnostic/m6_benchmark.txt`.

## 6. 양방향 sibling

- ⇄ [H_923](./H_923_akida_qrng_coupling.md) (HW 양자결합 — 본 H 의 특수case)
- ⇄ [H_921](./H_921_akida_nondeterminism_functional_advantage.md) · [H_922](./H_922_akd1000_digital_deterministic_architecture.md) (비결정 아크)
- ⇄ `.roadmap.qrng` · qmirror SSOT
