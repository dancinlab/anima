# H_9851 — ρ·weave 확장 패널의 원자 노출 감사 (H_9827 선결 과제 해소)

**status:** 🟢 계기 착륙 + 실측 (en-general 60MB) — G1 예산사다리의 선결 통과
**wired:** yes — `anima-py corpus weavepanel --out panel.json --seed 7 --corpus <corpus.txt>`
**source:** [[H_9827]] 이 카드에 남긴 OPEN — "확장 항목의 원자 노출을 코퍼스에서 직접 세는 감사 미구현"

## 왜

[[H_9827]] 이 ρ·weave 패널을 12 → 212 항목으로 늘리며 스스로 남긴 선결 과제:
**모델이 `seventeen` 을 본 적 없다면 그 항목의 실패는 조성 실패가 아니라 원자 부재를 잰 것**이다
(`corpus-py-1` (F): 일반화 주장은 그 축에 노출 0 인 항목에서만 재고, 노출을 **직접 세라**).

## 계기

`--corpus` 를 주면 항목별 원자 출현을 **단어경계**(`\b`)로 센다. 부분문자열 계수 금지 —
`art ⊂ start` · `five ⊂ fives` 이고, 이 결함은 기록된 **다음 날** 새 게이트 안에서 재도입된
전례가 있다(`corpus-py-1` (G)/(I)).

🔑 **두 축을 분리한다**(초판의 결함): 단서의 모든 단어를 원자로 뭉뚱그리면 기능어 하나가 없어도
항목이 죽어 **112/212** 같은 무의미한 수가 나온다. 분리 후:

- **OPERAND** (조성 피연산자 a·b) — 부재 ⟹ 그 항목은 **조성 실패가 아니라 원자 부재**를 잰다 = 판독불가
- **CARRIER** (프레임 단어) — 부재 ⟹ **미훈련 담체 = OOD basin**. 다른 결함, 다른 처방(`corpus-py-1` ⑧/⑫)

## 실측 (en-general · 744,588 문장 · 60MB)

| 축 | 결과 |
|---|---|
| **OPERAND** | **212/212 판독가능** (부재 **0**) |
| **CARRIER** | OOD 프레임 **0** |
| TARGET-WORD | 부재 0 |

⟹ **[[H_9827]] 확장 패널은 원자·담체 축에서 전부 판독가능**하다. G1 예산사다리를 이 패널로 읽어도
되며, [[H_9827]] 이 남긴 선결 과제는 **해소**됐다.

## ⚠️ 정직 고지

1. **TARGET-WORD 계수는 단어 존재이지 조성 사실 부재가 아니다.** `orange` 가 코퍼스에 나오는 것은
   당연하고, ρ·weave 가 요구하는 것은 `빨강+노랑→주황` 이라는 **연관**이 held out 인지다 —
   그 검사는 **이 감사에 없다**. 오독되지 않도록 출력이 스스로 그렇게 말한다.
2. `--corpus` 는 플래그당 파일 1개라 이번 실측은 **en-general 단독**(en-sns 미포함).

## 재생성 커맨드

```
anima-py corpus weavepanel --out wp.json --seed 7 \
  --corpus ~/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-en-general/snapshots/*/anima-corpus-en-general.txt
```

## Cross-links

[[H_9827]] 이 감사를 선결로 지목(동기) · [[H_9828]] 같은 캠페인의 G6 코퍼스 census ·
[[H_9817]] 이 패널로 읽을 예산사다리
