# H_9335 — EN 원자셋 **동결** (사전등록 · 모델 성적을 보기 전에)

- **group**: g1-crack-natural-emergence
- **date**: 2026-07-15
- **tier**: ⏳ **PRE-REGISTERED** (원자셋 동결 · 게이트 6/6 통과 · 학습 0 · 판정 0)
- **surfaces**: `HYPOTHESES/cards/H_9335_en_atomset.md` · `archive/state/scratch/en_arm/`

## 왜 동결이 먼저인가

원자셋은 재조합 레인 **전체의 하중을 받는 입력**이다 — 심는 극성, 빼놓는 어간, 판정이 계산되는
분할이 전부 여기서 온다. **모델 성적을 본 뒤에 원자셋이 바뀔 수 있으면 그건 이미 사전등록이 아니다.**
그래서 학습 **전에** PR 로 박는다.

## 절차 — 설계자가 어간을 고르지 않는다

```
① 채굴   anima-py corpus atoms --mine-lexicon 1400 --corpus <60MB FineWeb> --lang en
         프레임 = 강조부사 뒤(`very X`) ⟹ 영어는 강조부사 뒤에 **형용사만** 허용
         = 품사가 **통사로** 선택된다(취향이 아니라)
         (`is X` 는 헐거웠다 — 실측: 14,069 후보 중 상위 3개가 `the`·`not`·`that`)
② 라벨   빈도 **순위대로** 내려가며 극성 1비트. 모호하면 **폐기**(포함이 아니라).
         폐기는 **전부 사유와 함께 기록** ⟹ 불리한 어간을 조용히 버렸는지 **사후 감사 가능**.
③ 게이트  G-DERIV → G-CARRIER → G-SUBSTR → G-OCCUR → G-BALANCE → G-POWER
```

**p1–p8 정당성**: 금지 대상은 **LLM 이 훈련 바이트를 쓰는 것**이다. 렉시콘은 훈련 바이트를 **0글자**
쓴다 — 훈련 바이트 = 자연 코퍼스 + 결정적 템플릿. 렉시콘이 더하는 정보는 **어간당 1비트**이고,
그건 KO `gt_atoms.json` 의 `pol` 필드가 **원래부터 가졌던 지위**와 같다.

## 실측

| | |
|---|---|
| 채굴 | 4,598 프레임 후보 → 1,400 (노출 ≥150) · **3.4초** |
| 라벨 | 채택 **88** (긍 58 : 부 30) · **폐기 179 (전부 사유 기록)** · 미도달 1,133 |
| 원자셋 | **held-out 40 (긍 20 : 부 20)** · train 20 (10 : 10) |
| 노출 | occ_min **164** · median **605** |
| 검정력 | **우연 sd = 0.0791** (KO 는 n=29 에 0.093 — TOST 불가였다) |

**held-out(40)**: friendly sorry helpful late popular difficult clean painful excellent poor
reliable gross effective narrow famous afraid smart ill rich dead comfortable damaged incredible
limited safe offensive authentic ugly efficient slow peaceful dangerous reasonable weak exciting
stupid accurate wrong flexible sick

**train(20)**: fun boring honest severe proud terrible delicious bad secure impossible bright
expensive wonderful false beautiful empty good awful successful concerned

## 게이트가 실제로 문 것 (문서가 아니라 출력으로)

- **G-SUBSTR** → `dead ⊂ deadly` **잡음.** 내가 못 본 것이다. 규칙은 **기계적**(순위 낮은 쪽 폐기)이라
  게이트 실패가 **선호 어간의 핑계**가 될 수 없다.
- **G-CARRIER** → `positive`/`negative` 는 **라벨 낱말**이라 애초에 폐기 목록에 사유와 함께.
- **G-BALANCE** → FineWeb 은 **긍정 편향**이 심하다(상위 220 중 긍 34 : 부 9) ⟹ **1,400 까지 파야**
  부정 30개가 채워진다. 게이트가 **조용히 통과시키지 않고 이 제약을 드러냈다.**

## ⚠️ tune-to-green 을 피한 지점 (정직)

`--min-occ 300` 으로 처음 돌렸더니 **11개가 낙제**했고 **대부분 부정**(희소한 쪽)이었다.
**결과를 보고 하한을 낮추면 그게 tune-to-green 이다.** 그래서 **유도**했다:

```
요구 = EN C34 에서 어간당 자연문 48개 (KO 실측 48.8/어간 미러)
손실 = 부정형·파생형·길이 필터로 ~1/3 탈락 예상
⟹ 원시 노출 하한 = 48 × 3 = 144  →  150
```

**300 은 근거 없는 둥근 숫자였다.** 150 은 요구에서 나온 값이다. 그리고 **진짜 게이트는 하류**에
있다 — EN C34 표집기가 어간당 깨끗한 문장 48개를 **못 채우면 fail-loud** 로 죽는다.

## NEXT

EN C34 사전학습 코퍼스(KO C34 의 **구조적 쌍둥이**: 화살표 960줄 · SEEN 20 어간만 · 절반 부정형 ·
held-out 자연 노출 어간당 48) → EN 사전학습 → `corpus ground_keep --lang en` → `train` →
`evaluate --xbind`.

**예측(R2 STEM-BOUND)**: 자유 부정어 `not` 은 C1b 가 일반화를 실측한 **슬롯 종류**이므로, R2 가
맞다면 **EN 은 미학습 어간을 넘어 연산자가 돌아야 한다** ⟹ EN flip1 이 우연을 넘는다 ⟹
**BINDING = 형태론이지 기질 아님** ⟹ 레인 재개방.
⚠️ 단 EN 은 **형태론 + 기반모델 + 담체를 한꺼번에** 바꾸므로 양성은 **스크리너(DIRECTIONAL)**다.
