# AURA C4 — best 조합 설계 (귀뒤 고밀도 + ML, 목표 %-of-ECoG)

> C3의 5법을 합쳐 "귀뒤 비침습으로 침습급 근접"의 최선 스택 설계. honest: 설계(목표치는 C5 in-silico 천장에 bound).

## best 스택 — 4법 직렬 (5번째=과제별)

```
귀뒤+외이도 고밀도 건식 어레이 (256ch, 능동 graphene)   ← 법1+3+4: SNR·sampling·측두근접 최대
        │ raw scalp
        ▼
ML 역문제 source-recon (deep inverse, DeepSIF류)        ← 법2: 용적전도 부분 deblur
        │ cortical 추정
        ▼
딥 디코더 (self-sup transformer, 과제 fine-tune)        ← 법5: 추정서 task decode
        │
        ▼  목표: % of ECoG decode (천장=C5)
```

| 단 | 법 | 닫는 gap | AURA 7-verb 매핑 |
|---|---|---|---|
| ① 하드웨어 | 1·3·4 | SNR·sampling·측두 | structure/design (귀뒤 256ch 건식, demiurge AURA Class II 강화) |
| ② source-recon | 2 | blur 부분 | analyze (역문제 layer 추가) |
| ③ decoder | 5 | 추출효율 | analyze/synthesize (딥디코더) |

## 설계 결정

| 축 | 선택 | 근거 |
|---|---|---|
| 위치 | 귀뒤+외이도 (cEEGrid+in-ear) | 측두엽 근접(B1) · 착용성 · demiurge AURA 폼팩터 |
| 전극 | 256ch 능동 건식(graphene) | sampling+SNR 동시(법1+4) |
| 알고리즘 | deep inverse → self-sup decoder | blur 부분복원 + 추출효율(법2+5) |
| 목표 metric | **% of ECoG decode** (절대 아님) | 천장 인정(비침습은 근접) |

## 천장 인정 (정직)

- 이 스택도 **두개골 LPF 천장** 아래 — "ECoG 동일" 불가, "최대 근접"이 목표.
- 목표치(예: ECoG decode의 X%)는 **C5 in-silico 천장 측정 후** 확정 (지금 숫자 박으면 날조).
- demiurge AURA(Class II 비침습 하드웨어)가 ①단 실물 · anima AURA가 ②③ 알고리즘 = 분업.

## honest
- 설계 only — 실 256ch 귀뒤 어레이 제작·deep-inverse 학습은 미수행(하드웨어=demiurge, 학습=cloud).
- 목표 %-of-ECoG는 C5가 천장을 정량한 뒤 bound. C5 미완 시 이 설계의 목표치는 미확정(정직).

## 양방향 sibling
- [C(NOVEL 축)](C-postaural-invasive-NOVEL.md) · [C3](C3-noninvasive-methods-sota.md)(5법) · C5(천장) · demiurge `aura.md`(①단 하드웨어)
