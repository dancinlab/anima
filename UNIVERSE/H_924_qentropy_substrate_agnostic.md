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
| **추론 DECODER** (sampling 지점) | 🔧 SSOT-ready → **quantum 기본 + 결정론 보조** (probe 대기) |
| torch Lane-P CLM (train_lane_p.py) | 🔧 SSOT-ready → `qentropy_seed()` init (probe 대기) |

> DECODER 정정: 이전 "의도적 결정론·배선 안 함" → **"quantum 기본 · 결정론 보조"** 로 바뀜.
> 추론도 sampling 지점에서 SSOT 경유 양자-주입 가능(결정론은 보조 토글). 단 AKIDA forward 자체의
> 결정성(byte-identical)은 별개 — 양자는 *sampling/seed* 층에 들어가지 forward 연산을 바꾸지 않음.

## 5. 다음 작업

- [x] **M1** — qentropy SSOT (quantum-default·det-auxiliary) + 양 모드 self-test.
- [x] **M2** — SW numpy 학습 배선+검증 (substrate-agnostic PASS).
- [ ] **M3** — DECODER inference sampling 지점 SSOT 배선 + 양 모드 probe (quantum 기본·결정론 보조).
- [ ] **M4** — torch Lane-P CLM init `qentropy_seed()` 배선 + GPU probe.
- [ ] **M5** — 기존 M6/M7/h923 legacy env 훅을 qentropy SSOT 로 통일(중복 제거).
- [ ] **M6 (benchmark)** — per-path quantum vs deterministic A/B (학습수렴·emit다양성·Φ) 기록.

## 6. 양방향 sibling

- ⇄ [H_923](./H_923_akida_qrng_coupling.md) (HW 양자결합 — 본 H 의 특수case)
- ⇄ [H_921](./H_921_akida_nondeterminism_functional_advantage.md) · [H_922](./H_922_akd1000_digital_deterministic_architecture.md) (비결정 아크)
- ⇄ `.roadmap.qrng` · qmirror SSOT
