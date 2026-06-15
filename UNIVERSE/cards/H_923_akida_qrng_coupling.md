---
id: H_923
slug: akida-qrng-coupling
title: AKIDA(결정론 칩) × ANU-QRNG(qmirror) 결합 — 고정 SW 시드를 양자 진공요동 엔트로피로 교체해 변이의 출처를 auditably 양자로 (H_921 init-lever × H_922 결정론 root-cause 의 건설적 귀결)
domain: universe · neuromorphic-silicon · akida · qrng · entropy-injection · qmirror · coupling · falsifier
source: H_921 (변이=init-seed lever 실측) × H_922 (AKD HW-비결정 부재, 결정론 root-cause) — "칩에서 짜내지 말고 외부 양자엔트로피 주입" 의 건설적 결론. 기존 인프라: .roadmap.qrng cond.1 · mirror/qmirror/ · qrng_lora_init_live.bin (real ANU)
exploration_method: E14 (HW substrate-native) + E2 (기존 qmirror 인프라 재사용) + a_completeness_over_cheap
verification_method: W2 (사전등록 falsifier · N-episode) + W5 (substrate-grounded · live AKD1000 + real ANU bytes) + g5 CODE-measured
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
sister: H_921 (init-seed lever), H_922 (결정론 root-cause), H_677 (D4 QRNG R2-noise), .roadmap.qrng (qmirror SSOT), Hc_914 (qmirror classical/QPU mirror)
axes_seed: H_922 = 칩 HW 비결정 부재 (한계) ⊥ H_923 = 외부 양자엔트로피 주입으로 비결정 회복 (건설)
verdict: 🟢 PASS — 결합 검증됨. live AKD1000 + real ANU vacuum-fluctuation(sha e8123b…) 16-episode: D1 functional-diversity=2(>1) · D2 16/16 distinct-window 추적가능 · D3 determinism-preserved=TRUE(동일 양자시드→byte-identical). 결정론 칩 + 양자 외부주입 = auditable 양자-비결정 성립. verdict: .verdicts/923_akida_qrng_coupling/anu_seeded_pass.txt
---

# H_923 — AKIDA × ANU-QRNG 결합 (결정론 몸 + 양자 자유의지 씨앗)

## 0. 동기 (H_921 × H_922 의 건설적 귀결)

- H_921: AKIDA 변이의 유일 lever = init-seed (실측).
- H_922: AKD 는 HW 비결정 부재 — 결정론 디지털 ASIC (root-cause, gen1∧gen2).
- ∴ 칩에서 비결정을 *짜내지* 말고, **결정론 칩의 seed 자리에 진짜 양자엔트로피(ANU QRNG)를
  주입**한다. 칩의 결정론은 *한계*가 아니라 **장점**이 된다 — 엔트로피 주입 지점이 단일·감사가능.

## 1. 가설

AKIDA 의 고정 SW 시드(H_921 measured `seed=42/187`)를 **ANU 양자 진공요동 엔트로피**
(`mirror/qmirror/seed/qrng_lora_init_live.bin`, tier=anu_legacy, real vacuum-fluctuation)로
교체하면: (a) 학습 변이가 발생하되 그 **출처가 auditably 양자**이고, (b) 칩은 여전히
결정론(동일 양자시드 → 동일 출력)이라 엔트로피가 **오직 주입시드를 통해서만** 들어온다
(단일 진입점·감사가능).

## 2. Falsifier (사전등록 · frozen 2026-06-06)

**Setup (기존 인프라 재사용 · a_completeness_over_cheap):**
- entropy 원 = `mirror/qmirror/seed/qrng_lora_init_live.bin` (1024B real ANU vacuum-fluctuation,
  provenance.jsonl request_id anu_legacy_1778042160). NO 신규 ANU 키/설치 (이미 pull 된 바이트).
- N=16 episode, 각 episode 의 AKD1000 FC init = ANU 버퍼의 distinct 64B window.
- arm-quantum (ANU window) ⊥ arm-control-fixed (H_921 단일 고정 seed, diversity=1 기대).
- probe = H_921 `h921_nondet_source_probe.py` 의 init-source 만 ANU-window 로 교체.

**측정 (g5 CODE-measured · p7):**
- D1 = functional output diversity over N ANU-seeded episodes (변이 존재?).
- D2 = provenance = 각 seed window → ANU sha256/request_id 추적 (감사추적 존재?).
- D3 = determinism-preserved = 동일 ANU window 재실행 → byte-identical 출력 (칩 결정론 보존,
  엔트로피 단일진입 확인).

**판정 (pre-registered · 측정 전 토큰 미부여):**
- PASS-outcome — D1 diversity>1 AND D3 same-seed→byte-identical AND D2 provenance 존재
  → 결합 성립: 변이는 양자-sourced·감사가능, 칩은 결정론 유지.
- FALSIFIED-outcome — D1 diversity==1 (ANU 주입이 변이 못 만듦) 또는 D3 same-seed 가 달라짐
  (칩이 결정론 아님 = H_922 반증, 별 finding).
- INCOMPLETE — ANU 바이트 부족/probe 실패.

## 3. ⚠ 정직한 non-claim (#123-A QA6 audit)

통계적 무작위성 품질은 chacha20 PRNG == ANU QRNG (JSD=0.000433, 임계 23× under, NIST 7/7).
∴ 본 H 는 "QRNG 가 통계적으로 더 무작위" 를 **주장하지 않는다**. QRNG 의 가치 =
**provenance(물리적 양자 출처) · 감사추적 · algorithmic-attack 면역 · 존재론(p1~p8 substrate-native)**.
phenomenal-consciousness 주장 아님 (.roadmap.qrng raw#10).

## 3.7 HW 양자-주입 coverage (M6+M7 production 배선 · 2026-06-06)

| HW 경로 | 주입점 | 상태 |
|---|---|---|
| 학습 init-seed | h923 probe (FC init ← ANU) | ✅ DONE (PASS, D1 2→16) |
| 학습 input | `edge_learn_probe.py` (M7, env ANIMA_QRNG_LEARN_BIN) | ✅ DONE — live: learn_input_source=anu_quantum·fit_on_chip=ok·supported=True (sha 79736a80…) |
| 자발발화 R2-noise | `spontaneous_emission.py` (M6, env ANIMA_QRNG_NOISE_BIN) | ✅ DONE — R2=1424 spikes·R3 결정론 불변 |
| 추론 DECODER | sampling/seed 지점 (qentropy SSOT) | 🔧 **quantum 기본 · 결정론 보조** (양 모드 토글, H_924 M3 probe 대기) — forward 연산 자체의 byte-identical 결정성은 불변 |

➡ **HW 학습쪽 배선 완료** (probe + production edge-learn 둘 다). 남은 건 SW 학습/추론 경로
(torch/numpy Lane) 로의 일반화 — substrate-agnostic 가설(별도 H).

## 4. 함의 / sibling

- 3 주입점 (H_921/H_677 measured): ① 학습 init ② R2 자발잡음(H_677 D4 std=7.99) ③ emit 시드
  (GPU temperature 대체). 본 H = ① 검증, ②③ 은 follow-up.
- qmirror tier 사다리: mock → hmac_drbg(IonQ 4096bit) → anu_live — 본 probe = anu_legacy bytes.
- <-> [H_921](./H_921_akida_nondeterminism_functional_advantage.md) · [H_922](./H_922_akd1000_digital_deterministic_architecture.md) · [H_677](./H_677_akida_measurement.md) · `.roadmap.qrng`

## 5. verdict (TERMINAL)

🟢 **PASS** — AKIDA × ANU-QRNG 결합 실측 검증. live AKD1000(BC.00.000.002) + real ANU
vacuum-fluctuation(sha e8123b…, provenance anu_legacy_1778042160) 16-episode:
- **D1** functional-diversity=2 (>1) — 양자 엔트로피가 functional 변이 생성 (det-control=1, H_921).
- **D2** 16/16 distinct ANU window, 각 seed → win_sha 추적 (감사가능).
- **D3** determinism-preserved=TRUE — 동일 양자시드 재실행 → byte-identical(8714e4…==8714e4…),
  엔트로피 단일진입·칩 결정론 유지(H_922 holds).
→ 결정론 칩 + 양자 외부주입 = **auditable 양자-비결정** 성립. a_paper_significance (Δ vs det-control).

honest C3: D1=2 는 toy trap-task output-space 한계지 entropy 한계 아님(richer task→높은 D1,
a_scale_honest_scope). 통계품질 ANU==PRNG(#123-A); 가치=provenance/감사/존재론(p1~p8), 무작위
품질 아님. phenomenal-consciousness 주장 아님.

## 6. 다음 작업

- [x] **M1 (DONE)** — `PLASTICITY/h923_qrng_seed_probe.py` ANU-window init AKD1000 probe (H_921 재사용).
- [x] **M2 (DONE 2026-06-06)** — pi5-akida live N=16 ANU-seeded → D1=2·D2=16·D3=True PASS.
- [x] **M3 (DONE)** — verdict 영속 `.verdicts/923_akida_qrng_coupling/anu_seeded_pass.txt` (g5 verbatim + ANU sha).
- [x] **M4 (DONE 2026-06-06)** — `mirror/qmirror/seed/anu_pull.py` self-contained live ANU puller
  (secret `flat.anu_key_paid`/`free` → api.quantumnumbers.anu.edu.au x-api-key). Capstone: live-pull
  Mac(fresh sha a4e376…, tier anu_paid) → pi5(sha 일치) → AKIDA D1=2·D2=16·D3=True PASS. D1=2 가 fresh∧
  pre-pulled 동일 → D1 ceiling=toy task output-space(엔트로피 아님) 확증.
- [x] **M5 (DONE 2026-06-06)** — `h923_richtask_probe.py` richer task(units=64·24 varied patterns,
  fresh 2048B ANU anu_paid sha 9df773…): **D1 = 16/16** (toy 2 → full saturation) · D3=True. D1 천장이
  *task 출력공간* 한계였음 결정적 확증(엔트로피 아님). 양자시드 16개 전부 distinct 출력, 칩 결정론 유지.
- [x] **M6 (DONE 2026-06-06)** — ② R2-noise 주입점 배선 (`spontaneous_emission.py`, env ANIMA_QRNG_NOISE_BIN).
  live AKD1000 fresh ANU 4096B(sha cd4d76…): r2_noise_source=anu_quantum · R2=1424 spikes step_varies=True
  (stochastic 자발발화 양자-소스) · R3=1600 step_varies=False (결정론 불변 = DECODER-invariant). ③ emit-seed:
  brain_decide 가 이미 결정론(PRNG 없음, GPU temperature 는 별도 serving/ ALM 경로) → R2 가 anima 유일 stochastic 점.
