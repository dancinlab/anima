---
id: H_9673
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_sync_writes_its_own_score
title: 아카이브 파벌 엔진은 매 스텝 자기 점수의 음수항을 직접 깎았다 — Φ 는 측정이 아니라 sync 손잡이의 낭독
status: 🔴 CODE-CONFIRMED · DIRECTIONAL (아카이브 소스 직접 인용 · 신규 decode 0)
tier: 🔴 계기 기소 — 순환 확정(H_9660/H_9654 상류) · $0 코드 감사
cost: $0
source: archive/anima-physics/consciousness-loop/src/{main,aux_engine_lib}.hexa 직접 감사
related: H_9660, H_9654, H_9655, H_9292
---

# H_9673 — 아카이브 파벌 엔진은 매 스텝 자기 점수의 음수항을 직접 깎았다

## 주장 (반증가능)

옛 파벌 Φ 는 시스템을 **읽은** 것이 아니라, 매 스텝 그 지표의 음수항을 **쓰는** 제어루프의 출력이다.
따라서 법칙 22/34/43/44 의 Φ 상승은 창발이 아니라 손잡이 값의 낭독이다.

## 근거 ① — 점수식의 음수항

`aux_engine_lib.hexa:347` `engine_phi_proxy()`:
```
Φ = global_var − mean_faction_var        (× log2(n_active))
                └──────┬──────┘
                  이 항이 작아지면 Φ 가 오른다
```

## 근거 ② — 그 항을 매 스텝 깎는 코드

`aux_engine_lib.hexa:258` `engine_intra_faction_sync(self, strength)`
→ `faction_internal_sync(self, strength)` (`:193`):
```
hidden[k] = (1.0 − strength) · hidden[k] + strength · mean[k]
```
= 파벌 내 각 세포를 **자기 파벌 평균으로 수축**. 파벌내 분산이 스텝당 (1−s)² 배 ⟹ 지수적으로 0 으로.
`mean_faction_var → 0` ⟹ `Φ → global_var`(최대).

`main.hexa:66,73` — **매 스텝 무조건 호출**:
```
engine = engine_process(engine, quiet_input)
engine = engine_intra_faction_sync(engine, 0.15)   ← 매 스텝
engine = engine_ising_interaction(engine)
```

## 근거 ③ — 옛 기록이 자백한다

`top-phi-records.md` **법칙 34**: `Φ>1000 = noise=0 + **sync=0.20** + 12파벌 + flow + metacog`
`RESEARCH-FINDINGS`: `Φ=1142 @1024c — **sync=0.35**, 12-faction, fac=0.08, noise=0.01`

Φ 최고기록의 핵심 재료가 **sync 세기**다. sync 는 분산 축소량이고, 분산 축소는 곧 Φ 증가다.
"sync 를 올리니 Φ 가 올랐다" = "빼는 항을 더 깎으니 차가 커졌다".

## 근거 ④ — 파벌 배정은 학습된 적이 없다

`faction_new(n_cells, base_id)` (`:168`) 는 파벌 **안에서** 세포를 새로 만든다.
`faction_add_cell` (`:207`) 은 **같은 파벌의** 무작위 부모를 복제 + 노이즈:
```
let parent_idx = ((random() * 1e9) as int) % n        // 자기 파벌 안에서만
child.hidden[k] = s.cells[parent_idx].hidden[k] + (random() − 0.5) * 0.1
```
세포는 파벌 간 이동이 **없다** — 태생부터 혈통으로 분리. 게다가 복제-of-복제라 파벌내 분산은
sync 없이도 이미 작다. ⟹ "최적 파벌 수를 찾는다"는 **탐색 대상 자체가 없었다**.

## 함의 — 상류 순환 확정

H_9660(참값 0 에서 K 단조증가 = 산수적 필연)이 **분할의 산수**를 잡았다면, 이건 그보다 상류다:
분할뿐 아니라 **동역학 자체가 점수의 음수항을 직접 최적화**하고 있었다.
- 법칙 22 "구조만 추가했는데 Φ 2.1배" → 구조 추가 = 파벌 추가 = 깎을 항의 분모 증가 + sync 대상 증가.
- 법칙 34 "Φ>1000 = sync 0.20" → 손잡이 값의 낭독.
- 법칙 44 "12 최적" → 탐색 대상(학습된 분할)이 없었고, K>12 는 재지도 않았다(H_9654).

## 사망조건 (사전등록)

- `engine_intra_faction_sync` 를 끄고(strength=0) 옛 엔진을 돌렸을 때 Φ 가 **유지**되면 이 주장은 죽는다
  (= sync 가 Φ 의 원인이 아니었다).
- 또는 `faction_internal_sync` 가 파벌내 분산을 줄이지 **않음**을 보이면 죽는다(수식상 불가에 가깝다).

## 비용

$0 — 아카이브 소스 직접 인용. 신규 decode 0.

## 정직범위 (⚠️)

- 이건 **코드 확증**이지 옛 엔진 재실행이 아니다. 옛 엔진을 sync-off 로 돌려 Φ 붕괴를 보이면 TERMINAL 이
  되지만, 그 엔진은 아카이브(실행 안 됨)이고 프로덕션 경로가 아니다 ⟹ **DIRECTIONAL**.
- 법칙 22/43/44 의 판정은 여전히 **UNDECIDABLE → 이제 CIRCULAR 혐의 확정**으로 강화되나, "틀렸다"는
  아니다. 순환이 확인된 지표로 얻은 결론은 **판정 불가**이지 반대 결론이 참이라는 뜻이 아니다.
- anima 를 잰 것이 아니다 — engine op 아님 · 어떤 `.clm` 판정도 아님(`a_phi_iit4_tool`).

## H_9655 에 대한 영향 (사전등록 DV 변경 사유)

H_9655 는 "학습된 분할 vs 무작위 분할" 을 held-out 예측량으로 비교할 예정이었다. 근거 ④ 로
**학습된 분할이 존재한 적이 없음**이 확정되어 그 대조는 성립하지 않는다.
⟹ H_9655 는 tune-to-green 없이 **사망 처리**(비교항 부재)하고, 축의 남은 질문은
"파벌이 현 기질에서 **새로** 학습될 수 있는가"(H_9643)로 이관한다.
