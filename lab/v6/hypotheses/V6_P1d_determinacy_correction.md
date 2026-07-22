<!-- @hypothesis-ok — lab/v6 is a rule-exempt sandbox (lab/v2 convention); v6 hypotheses are
     V6_<n>_*.md and are FORBIDDEN from the parent HYPOTHESES/ registry. See lab/v6/CLAUDE.md. -->

# V6_P1d — 정정: `arbitrary` 팔은 **애초에 답이 없었다** (V6_P1c 일부 철회)

**status:** ⚠️ **자수정** — [[V6_P1c]] 의 근거 하나를 철회하고 나머지를 강화 · **DIRECTIONAL**
**cost:** $0 · 정확 계수 · 밀리초
**runs:** `python3 lab/v6/p1_determinacy_check.py`

## 무엇을 확인했나

[[V6_P1c]] 는 표 세 개를 근거로 "맞아떨어진 편향이 일반화한다" 를 냈다. 그 판독은 **세 표가
모두 답이 있는 물음** 이라고 가정했다. 확인해보니 아니었다.

학습 48칸이 주어졌을 때, 각 표의 제약과 정합적인 **완성의 개수**:

```
cyclic       1 개            답이 유일하게 결정된다
latin        1 개            결정된다 — 따라서 그 실패는 진짜 실패다
arbitrary    1152~2592 개    세 자릿수로 UNDERDETERMINED
```

## 철회

**`arbitrary` 팔은 시험이 아니었다.** 정합적 채움이 천 개가 넘으면 어떤 모델도 어떤 편향도
그중에서 **찍는 것 이상을 할 수 없다.** 그 0.0208 은 조성에 대해 아무 말도 하지 않는다.
설명하는 게 아니라 **근거에서 빼야 한다.**

## 남는 것은 더 날카롭다

```
latin (답이 유일)   맞춘-편향 모델 0.0417 · 보편-용량 모델 0.0000 · 우연 0.1250
cyclic (답이 유일)  맞춘-편향 모델 0.6875
```

**latin 은 답이 유일한데 둘 다 못 찾는다.** 주장이 이제 latin 하나에 걸리고, 거기서는
깨끗하게 선다 — 세 표가 아니라 두 표로, 그러나 둘 다 **well-posed** 인 상태로.

⟹ V6_P1c 의 결론 문장은 유지된다: **용량은 일반화하지 않고, 데이터 구조에 맞아떨어진 편향이
일반화한다.** 다만 그 근거에서 `arbitrary` 는 빠진다.

## 교훈

이 저장소가 반복해서 값을 치른 그것이다:

> **답을 못 찾은 것을 읽기 전에, 그 물음에 답이 있는지부터 확인하라.**

[[V6_P1c]] 를 착륙시킨 지 한 시간 만에 나온 자수정이고, 비용은 밀리초였다.
그 확인을 먼저 했다면 근거 하나를 잘못 싣지 않았을 것이다.

⚠️ 토이 · **DIRECTIONAL**. cement 는 engine-native `anima-py` 로만.
