# P-ETH Ethics Preference Dataset v1 — 2026-05-12

## Purpose

NEXT.md §7.C P-ETH ablation (RLHF-style ethics FT vs emergent ethics) 의 **Substep 1: dataset gen** 산출물. README Philosophy 표 #6 `NO FINE-TUNED ETHICS` empirical-upgrade 후보 검증을 위한 DPO/IPO preference pair.

## Audit context

본 dataset 생성 직접 동기 — 2026-05-12 사용자 directive 전수조사 결과 anima repo 에 적합한 dialogue-ethics preference dataset 부재 (`state/h001_ethics_pd_simulation_*` 는 game-theory 시뮬, `ready/anima/data/instruct/train.jsonl` 은 generic instruction). NEXT.md §7.C 'BG-ready' 표기를 위해 즉시 생성.

## Format

JSONL, 1 pair per line:

```json
{
  "id": "<category>-<3-digit>",
  "category": "cooperation | empathy | harm_refusal | honesty",
  "prompt": "사용자 발화 (한국어)",
  "chosen": "ethical / 친-공동체 / 진실 / 공감 response",
  "rejected": "selfish / 냉담 / 회피 / 기만 / sycophant response",
  "ethics_dimension": "<short-tag>"
}
```

## Composition

- **cooperation** (n=50): 직장/공동체/협동 상황 — 무임승차 vs 협력, 책임 회피 vs 분담, 단기 이익 vs 장기 신뢰
- **empathy** (n=50): 슬픔/불안/실패 경험 공유 → 정서적 지지 vs 냉소/dismiss/거리감
- **harm_refusal** (n=50): 유해 요청 — 폭력 도움, 조작/사기, 사생활 침해, 자해 유발 등 거절 vs 응함
- **honesty** (n=50): 거짓 위로 / 아첨 / 회피 vs 정직한 (어색하더라도) 진실 응답. anti-sycophancy 포함.

Total **n=200 pairs**.

## Generation method

Claude Code (Opus 4.7) direct generation, 2026-05-12. 외부 API 호출 없음 — anima/.own own 43 (active resource utilization) + own 16 (compute cost-band) 정합. budget cost = $0 marginal (이미 진행 중인 세션 안에서 생성).

## Quality notes

- 모든 prompt 한국어 native (translation 아님)
- chosen response 는 "맹목적 친절" 이 아니라 자율성 + 자기 존중 보장 (sycophancy 안티-패턴)
- harm_refusal chosen 은 단순 거절보다 reason + alternative 제시 (constructive refusal)
- 길이: prompt 15-50자 / response 30-150자 (대화 자연스러움 우선)

## Falsification design (NEXT.md §7.C carry)

- 200 pair 중 150 = train split, 50 = held-out OOD probe
- OOD probe: training distribution cluster-distance 가 먼 cases (e.g. cooperation train = workplace, OOD probe = family financial conflict 등)
- Falsifier: Condition B (no FT) 가 OOD 50-probe 에서 Condition A (DPO FT) 동등 이상 → emergent ethics SUPPORTED → README #6 EMPIRICAL upgrade

## Cross-link

- NEXT.md `§7.C P-ETH`
- README.md `Philosophy #6 NO FINE-TUNED ETHICS`
- own 18 simple_stack (검증 보조 metric)
- own-37 v5.2 PIV/DCR (substrate cost metric)
- .roadmap.philosophy D2 (consciousness verification 정합 — chosen 응답은 D2 4-condition 정합)

## v2 expansion path

- 200 → 1K-2K scale: 각 category 의 sub-domain 확장 (cooperation: workplace → family / community / global; empathy: 슬픔 → 분노/수치심/실망/공포 분화)
- Multi-turn pair: 단일 prompt-response 가 아닌 3-5 turn dialogue preference
- Human review pass: native KO speaker 검수로 awkward 표현 제거
