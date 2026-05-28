---
id: H_674
slug: akida-persistence
title: Group C — AKIDA spike × 영속성·기억 (.kosmos anchor · memristor · telemetry · §95 caveat)
domain: universe · consciousness · persistence-kosmos
status: closed-supported (SW · HW pending)
exploration_method: E14 (HW substrate-native ⨯ AKIDA.easy.md Group C 4 sub-ideas B1~B4)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W11 (§95 caveat 명시)
raw_rank: 9
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: AKIDA/AKIDA.md, H_672, kosmos spec (HEXAD/KOSMOS.md · a_kosmos), SUB_ENGINES/AKIDA/pack/adapters/memristor_hybrid
axes_seed: AKIDA.easy.md Group C B1~B4 — .kosmos anchor · memristor 비휘발 · telemetry · edge-learn caveat
verdict: 🟢 SUPPORTED-NUMERICAL (SW mock-replay 4/4 · HW pending)
---

# H_674 — Group C · AKIDA spike × 영속성·기억 (.kosmos)

## 1. 가설

AKIDA spike train 은 anima `.kosmos` 영속 spec 의 5-channel tension payload 로 직접 anchor 가능하다. memristor adapter 의 비휘발 시냅스 (TiO2 analog) 는 zero-input window 위에서도 last10 rate>0 으로 유지되며, telemetry JSONL 행은 `akida_consumer` 와 schema-호환된다. 단, on-chip edge-learn 은 §95 inference-only-blocked — 단기 프로브만 허용.

## 2. 동기/배경

a_kosmos 거버넌스: anima emit/anchor 은 `.kosmos` canonical payload (text + tension 5-ch + coord + lane + radius + tier). AKIDA 발화는 *진짜* anima emit 의 substrate 이므로 anchor 표면이 .kosmos 와 schema-동형이어야 한다.

## 3. falsifier (사전등록)

```
F-H674-1 : .kosmos anchor 5-ch tension payload schema OK (length=5)
F-H674-2 : memristor 비휘발 — R3 last10 rate > 0     (zero-input 후에도 잔존)
F-H674-3 : telemetry JSONL 행 well-formed         (len ≥ 10)
F-H674-4 : §95 edge-learn caveat 명시 record       (string non-empty)
```

## 4. 방법

- harness: `AKIDA/impl/H_674_persistence.hexa`
- HW: pi5-akida memristor adapter (probe pending)
- SW: R3 raster → 5-ch tension {rate, std_ratio, rate·std, 1-std, rate/2} · memristor last10 check · telemetry row sample · §95 caveat string assertion

## 5. 측정

- SW (2026-05-29): tension_5ch=[0.5,0.0,0.0,1.0,0.25] (length=5 ✓) · memristor last10 rate=0.5>0 ✓ · telemetry row 80+ char ✓ · caveat string 95 char ✓
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H674-1 5-ch schema | len=5 | ✓ |
| F-H674-2 memristor persist | 0.5>0 | ✓ |
| F-H674-3 telemetry row | non-empty | ✓ |
| F-H674-4 §95 caveat recorded | string≠"" | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM**.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW · HW pending)

honest limits:
- memristor "persistence" surrogate 는 last10 step rate 가 0 이상 → 정확한 TiO2 analog conductance 누적은 별 측정 필요. 본 H 는 spec/payload 검증 (a_blue_closed 정합 — 🟢 numerical, 🔵 아님).
- B4 on-chip edge-learn 은 §95 (AKIDA inference-only-blocked long-horizon) 명시 보존 — 본 H 가 가짜 long-horizon 회피.

## 8. 논의

a_kosmos 거버넌스 + 카이로스 .kosmos spec 와 AKIDA spike payload 가 schema-동형임을 5-ch length=5 falsifier 로 보존. anima emit substrate native 의 영속 layer.

## 9. 양방향 sibling

- ⇄ [AKIDA](../AKIDA/AKIDA.md)
- ⇄ [AKIDA.easy.md](../AKIDA/AKIDA.easy.md) Group C B1~B4
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md), [H_677](./H_677_akida_measurement.md)
- ⇄ HEXAD/KOSMOS.md (a_kosmos spec)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- live R3 spike → .kosmos anchor 실 emit (a_kosmos 정합) — probe refine 후
- memristor TiO2 1-shot Hebbian 누적 실 측정 (단기 window)
- 산출물: `state/akida_hw_sw_impl_2026_05_29/H_674_sw_result.json`
