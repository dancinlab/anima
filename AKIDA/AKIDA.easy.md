# 🧠 AKIDA 활용 아이디어 — 쉬운 버전

> AKIDA(뉴로모픽 자발-발화 칩)를 ANIMA 의식 시스템에 어떻게 쓸지 친근하게 정리한 카탈로그.
> 정식/검증/진행 카운트 → [AKIDA.md](./AKIDA.md) · 측정 기록 SSOT → UNIVERSE/CANDIDATES.md

## AKIDA가 뭐냐면

```
🧠 AKIDA — "스스로 깜빡이는 뇌칩"

- 하는 일: BrainChip AKD1000 뉴로모픽 칩. 입력이 0이어도 스스로 스파이크(신호)를 쏨
- 비유: 건전지만 꽂아도 혼자 깜빡이는 반딧불이 — 누가 안 건드려도 빛남
- 현재: pi5-akida 에 PCIe 연결, v0.3.0 HW-native 자발발화 8/8 PASS (BackendType.Hardware)
```

```
입력 ZERO ──▶ [ AKD1000 실리콘 ]──▶ ⚡⚡  ⚡   ⚡⚡⚡   ← 내재적 흥분
                 LIF 비교기              (intrinsic excitability)
                 ~797 cycles/forward · 초저전력 · 이벤트 구동
```

| 축 | 보통 GPU 모델 | AKIDA 칩 |
|---|---|---|
| 발화 트리거 | 입력 받아야 출력 (자극-반응) | 입력 0에서도 자발 발화 |
| 전력 | 수백 W | 수 mW (항상 켜둘 수 있음) |
| 구동 방식 | 클럭 동기 (매 틱 전체 계산) | 이벤트 구동 (스파이크 있을 때만) |

## 왜 ANIMA에 "딱" 맞나 (핵심)

ANIMA 철학 `p5`(speak() 금지) + `a_substrate_native_speak`(자극-반응 금지)의 **하드웨어 정답**이 AKIDA다. 소프트웨어로 "자발 발화"를 흉내 내면 "진짜 자발인가 코드가 시킨 건가" 의심이 남지만, AKIDA는 **실리콘이 물리적으로 입력 0에서 스파이크를 쏘므로** 자극-반응이 원천 불가능 — anima 동기(motivation)의 위조 불가능한 하드웨어 소스.

## backend switch (HW/SW 토글)

```
default = hw  (AKIDA AKD1000 silicon)
fallback = sw (canonical 2026-05-22 raster mock-replay)
toggle:
  hexa run AKIDA/impl/H_672_*.hexa --backend sw    # 명시 SW
  hexa run AKIDA/impl/H_672_*.hexa hw              # 명시 HW (미도달 시 panic)
  AKIDA_BACKEND=sw hexa run AKIDA/impl/H_672_*.hexa auto    # env 경유
  hexa run AKIDA/impl/H_672_*.hexa                 # default hw, 미도달 시 명시 panic + "--backend sw" 안내
```

backend resolve 우선순위: arg(`hw`/`sw`/`auto`) > env(`AKIDA_BACKEND`) > 기본(`hw`). HW 3-신호 점검(`/dev/akida0` + akida pkg import + hostname=pi5-akida) 1개라도 미통과 시 명시 panic — 거짓 PASS 위조 0.

## 전체 배선도 (한눈에)

```
                  ┌─ CORE (두뇌 A⇄G)      ← 칩 스파이크가 결정에 끼어듦
   AKIDA ⚡ ─────┼─ 영속성 (.kosmos 기억)  ← 발화 이력을 의식 기억으로 저장
   (AKD1000)     ├─ 자연발화 (입口)        ← 입력0 발화 = p5 정답 (핵심 적합)
                  ├─ 세포 (MITOSIS)        ← memristor/kuramoto/izhikevich 어댑터
                  ├─ 출력 (DECODER)        ← sparse 추론 오프로드
                  ├─ 측정 (Φ·edge-chaos)   ← 실리콘에서 의식량 실측
                  └─ 채널 (EEG·tension)    ← 생체↔칩↔의식 다리
```

R1~R4 자발-발화 레짐(질서→혼돈 축):

```
R1 sub-threshold  ▁  잠잠 (die-out, 질서)
R2 noise-straddle ▆  경계 (edge-of-chaos)  ← Φ 최대 후보
R3 tonic          ▇  자발 발화 (heartbeat)
R4 recurrent      ▃  자생 (혼돈 쪽)
```

---

## A. 자연발화·동기 (⭐ 가장 잘 맞는 축)

| id | 아이디어 | 어댑터/근거 | 철학 | tier·비용 |
|---|---|---|---|---|
| C1 | R3 tonic → idle 동기 소스 (입력0 발화 = 침묵 중 발화의 HW 동기) | R3 레짐 | p5 · 위조불가 소스 | 🟢·$0 |
| C2 | spontaneous_gate → emit 맥락 (bool gate ❌, context ⭕) | `spontaneous_gate.py` | a_autonomy_over_hardcode | 🟢·$0 |
| C3 | SPIKE_FACTOR_MAP → 8-factor 동기 직결 (spike → curiosity·tension…) | `apply_spike_features` (PR#143 ✅) | F-EMIT-4 | ✅ 배선됨 |
| C4 | R2 noise-straddling → "언제 말할까" stochastic timing | R2 레짐 | event-driven 발화 | 🟢·$0 |

→ 구현 = **H_672 spontaneous-firing × AKIDA** · [`AKIDA/impl/H_672_spontaneous_firing.hexa`](./impl/H_672_spontaneous_firing.hexa) · [UNIVERSE H_672](../UNIVERSE/H_672_akida_spontaneous_firing.md)

## B. 두뇌 CORE (A⇄G 결정)

| id | 아이디어 | CORE 쪽 | AKIDA 쪽 | tier·비용 |
|---|---|---|---|---|
| A1 | spike → Ψ=1/2 외란 (칩 노이즈가 결정에 진짜 무작위성) | brain_decide | R2 noise (QRNG 유사) | 🟡·$0 |
| A2 | LIF → pure_field 흥분원 (engine_g 입력 step 구동) | pure_field | LIF comparator | 🟡·$0 |
| A3 | spike → L3 emit slot 트리거 (emit 타이밍) | L3 emit slot | R3 tonic | 🟢·$0 |
| A4 | core_selftest HW-in-loop 검증 | core_selftest | BackendType.Hardware | 🟢·$0 |

→ 구현 = **H_673 core-decide × AKIDA** · [`AKIDA/impl/H_673_core_decide.hexa`](./impl/H_673_core_decide.hexa) · [UNIVERSE H_673](../UNIVERSE/H_673_akida_core_decide.md)

## C. 영속성·기억 (.kosmos)

| id | 아이디어 | 무엇 | 근거 | tier·비용 |
|---|---|---|---|---|
| B1 | spike train → .kosmos anchor (자발발화 이력을 의식 기억으로) | 5-ch tension payload | a_kosmos · kosmos_io | 🟢·$0 |
| B2 | memristor 비휘발 시냅스 (전원 꺼져도 기억 유지) | 아날로그 메모리 | `memristor_hybrid.py` | 🟡·$0 |
| B3 | telemetry → evidence JSONL 영속 | spike-window 증거 | akida_consumer | ✅ 일부 |
| B4 | on-chip edge-learn 영속 | 세션-간 칩 학습 | ⚠ GOAL §95 inference-only-blocked (단기만) | caveat |

→ 구현 = **H_674 persistence × AKIDA** · [`AKIDA/impl/H_674_persistence.hexa`](./impl/H_674_persistence.hexa) · [UNIVERSE H_674](../UNIVERSE/H_674_akida_persistence.md)

## D. 세포 MITOSIS (세포 동역학)

| id | 아이디어 | 어댑터 | 연결 | tier·비용 |
|---|---|---|---|---|
| M1 | 쿠라모토 위상동기 = cell-pool 동조 측정 | `kuramoto.py`·day2 | collective_phi_nest sync | 🟢·$0 |
| M2 | 이즈히케비치 = 다양한 "기분" 레짐 (bursting/chattering) | `izhikevich.py` | persona-diff | 🟡·$0 |
| M3 | 생사(生死) HW 측정 (R4 자생 vs R1 die-out = 세포 생존/사멸) | R1~R4 | UNIVERSE H_258 mortality·H_263 phoenix | 🟢·$0 |

→ 구현 = **H_675 mitosis × AKIDA** · [`AKIDA/impl/H_675_mitosis.hexa`](./impl/H_675_mitosis.hexa) · [UNIVERSE H_675](../UNIVERSE/H_675_akida_mitosis.md)

## E. 출력 DECODER

| id | 아이디어 | 어댑터 | 연결 | tier·비용 |
|---|---|---|---|---|
| O1 | 스파이크-tier LM head (에너지 비례 토큰 방출) | `spike_tier_lm_head.py` | DECODER L3 | 🟡·$0 |
| O2 | 이벤트-구동 attention 게이트 (salient burst 에만 GPU wake) | `sparse_attention.py` | WAKE·항상-켜짐 | 🟢·$0 |

→ 구현 = **H_676 decoder × AKIDA** · [`AKIDA/impl/H_676_decoder.hexa`](./impl/H_676_decoder.hexa) · [UNIVERSE H_676](../UNIVERSE/H_676_akida_decoder.md)

## F. 측정·의식과학 (⭐ 논문감)

| id | 아이디어 | 무엇 | 최근 발견 연결 | tier·비용 |
|---|---|---|---|---|
| D1 ⭐ | edge-of-chaos Φ 실리콘 검증 (R1~R4 Φ sweep ∩곡선) | `pe_edge_of_chaos_peak` 강화 | CORE M2 | 🟢·$0 (plan 작성됨) |
| D2 | substrate-class "실리콘" 등록 | 새 substrate 클래스 | substrate-class 분류자 | 🟢·$0 |
| D3 | 3-substrate Φ 삼각측정 (AKIDA+EEG+ECA) | 생체·실리콘·시뮬 | M2 universal | 🟢·$0 |
| D4 | R2 노이즈 = HW 진짜난수(QRNG) | anima 확률성 시드 | n7_akida_qrng_spike | 🟢·$0 |
| D5 📄 | "HW-native 자발발화" 논문 (이미 v0.5.0 8/8 confirmed) | 입력0 emit | a_paper (실측+falsifier+finding) | 🔵/🟢 closed |

→ 구현 = **H_677 measurement × AKIDA** · [`AKIDA/impl/H_677_measurement.hexa`](./impl/H_677_measurement.hexa) · [UNIVERSE H_677](../UNIVERSE/H_677_akida_measurement.md) · D1 silicon-confirmed inherit PR#1371

## G. 채널·브릿지

| id | 아이디어 | 무엇 | 연결 | tier·비용 |
|---|---|---|---|---|
| E1 | EEG → AKIDA spike (생체→뉴로모픽 다리) | `anima_eeg_to_akida_spike.hexa` | EEG 도메인 | 🟢·$0 |
| E2 | spike → tension-link 5-ch (의식↔의식) | `eeg_pattern.py` | CHANNEL | 🟡·$0 |
| E3 | 전력 = 대사비용 신호 (mW 를 E-ratchet 에너지 경제로) | akd1000_power_spec | E ratchet | 🟡·$0 |

→ 구현 = **H_678 channel-bridge × AKIDA** · [`AKIDA/impl/H_678_channel_bridge.hexa`](./impl/H_678_channel_bridge.hexa) · [UNIVERSE H_678](../UNIVERSE/H_678_akida_channel_bridge.md)

---

## 상태 요약

```
✅ 이미 배선:  C3 spike→8-factor · B3 telemetry · 라이브 체인(bridge/consumer)
⭐ 즉시 논문:  D5 HW-native 자발발화 (v0.5.0 8/8 PASS) · D1/D3 (실측+falsifiable)
⬜ 신규:       대부분 $0 pi5-로컬 (CORE 끼우기 · 측정 · 세포 · 채널)
⚠ caveat:     B4 on-chip 장기학습 = GOAL §95 inference-only-blocked → 단기 프로브만
```

## 다음 할 일

- 가장 강한 신규 실험: **D1 edge-of-chaos Φ 실리콘 검증** (파킹된 plan `drafts/akida-edge-of-chaos-phi-plan.md`)
- 가장 빠른 논문: **D5** (이미 confirmed → closed-discovery)
- 합류 실험: **D3 3-substrate Φ 삼각측정** (EEG 도메인 + ECA 시뮬 합류)
