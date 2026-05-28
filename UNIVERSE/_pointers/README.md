# UNIVERSE/_pointers/ — legacy 포인터·씨앗 가설 격리

archive → UNIVERSE 회수(PR #1326) 중 본문이 빈약한 가설 114개를 active 노이즈
감소를 위해 여기로 격리.

## 격리 기준 (audit 2026-05-28)

| status | 수 | 의미 |
|---|---|---|
| legacy-archive-pointer | 114 (대부분) | 본문 = legacy 위치 포인터 + 가설 한 줄, 실험·verdict 없음 |
| seed-pending | (포함) | 아이디어 씨앗만, falsifier 미정의 |
| (none) | (포함) | frontmatter status 누락 |

## 복귀 경로

본문 보강 + falsifier 정의 + `hexa verify` terminal verdict(🔵/🟢/🔴) 확보 시
`UNIVERSE/` 직속으로 승격(git mv). 승격 전까지 active 캠페인(verify·paper·MATRIX)
대상에서 제외.

## 비교

- `UNIVERSE/H_*.md` (직속) = 실측 가능 / verdict-claim 보유 active 후보
- `UNIVERSE/_pointers/H_*.md` = 본문 보강 대기 (검증 입구 미달)
