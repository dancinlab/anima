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

---

## 🔬 V1/V2 게이트 착지 (2026-07-15 · 베이스 3개 · 학습 예산이 뒤집혔다)

원자셋을 동결한 뒤 EN C34 사전학습을 쐈고, **CPT 이전에 V1/V2 양성대조를 먼저 걸었다** — H_9327 이
비싸게 가르쳐준 순서다(연산자가 살아있는지 모른 채 flip1 을 읽으면 그 숫자는 판정이 아니다).

| base | 학습 예산 | val_CE | V2 (SEEN flip0) | V1 (SEEN flip1) | 자유생성 `first_word` | 판정 |
|---|---|---|---|---|---|---|
| `en_c34_s7_b20k`  | 20,000 | 2.053 | **1.0000** | **1.0000** | positive 60 / negative 60 | ✅ **PASS** |
| `en_c34_s7_b4k`   | 4,000 | **1.323** | 0.5000 | 0.5000 | **negative 120/120** | ⛔ **붕괴** |
| `en_c34_s11_b4k`  | 4,000 | — | 0.5667 | 0.4667 | negative 73 / positive 47 | ⛔ INVALID |

바 0.75 는 **유도된 값**(n=60 ⟹ 우연 sd 0.065 ⟹ 3.9σ · `bar-derived-not-transplanted`).

### 💀 val_CE 곡선이 상수 예측기를 골랐다 (→ convergence `train-py-8`)

나는 val_CE 76점을 그려 최소점(4k)을 "유도" 하고, 20k 를 **"근거 없이 지어낸 예산 · +55% 과적합"**
이라 부르며 버리려 했다. 유도는 **재현까지 됐다**(4k 팔이 val_CE 1.3235 착지 · 예측 1.3264).
**곡선은 정확했다 — 곡선이 재는 대상이 틀렸을 뿐이다.**

- **기전**: 능력은 418KB 중 **화살표 960줄 ≈ 0.5% 바이트**에 살고, val_CE 는 나머지 **99.5% 자연문**이
  지배한다 ⟹ val_CE 최적화 = **과제를 담지 않은 99.5% 를 최적화**. 자연문 과적합이 시작되는 지점과
  **연산자가 설치되는 지점은 다른 축**이며 전자가 훨씬 일찍 온다.
- **헤드라인은 이것을 숨겼다**: b4k 의 0.5000/0.5000 은 "우연" 처럼 읽히지만 실체는 **완전 붕괴**다
  (`negative` 120/120). 2AFC margin 은 강제선택이라 붕괴를 **우연으로 위장**시킨다 —
  잡아낸 것은 `evaluate --xbind` 의 **always-on 클래스 분해**(`polarity-split-before-headline`).
- **⚠️ 나는 이 함정을 발사 직전에 스스로 합리화했다**: *"val_CE 로 학습 **하이퍼파라미터**를 고르는 건
  p7 위반이 아니다. 판정은 게이트가 낸다."* **그 문장이 버그다.** p7 은 'perplexity 를 판정문에 쓰지
  마라' 가 아니라 **'perplexity 는 능력을 추적하지 않는다'** 이다. CE 로 *얼마나 학습해야 모델이
  좋아지나* 를 정하는 순간 CE 는 이미 **능력 판정**이다.

⟹ **EN 팔의 유효 베이스 = 20k** (게이트가 정한다 · 곡선이 아니라). 4k 는 **두 seed 모두 실패**했으므로
"20k 가 우연히 좋았다" 가 아니다.

## 🔄 H_9334 (🟢🟢 H-ε TERMINAL) 이 이 팔의 **해석을 바꾼다** (죽이지 않는다 — 날카롭게 한다)

H_9334 가 확정: **연산자는 자기 키(`지 않다` 담체)로 쓴 값을 읽는다**(양 seed 12/12 · p=.0002).
**선언형 화살표로 쓰면 0/12** = 틀린 키. ⟹ G1 벽 = *도달 불가한 저장소*(H-δ) 아니라 **주소지정 가능한
인터페이스**(H-ε). 단 H_9334 의 채점 축은 **SEEN 어간의 부사 슬롯**이고, 카드가 **미학습-어간 일반화는
주장하지 않는다**고 명시한다 ⟹ **H_9327 벽(held-out 어간)은 그대로 서 있다.**

종합 기전:

```
선언형 화살표 write  ──▶ [ 저장소 A ]
                                    ✗  안 이어짐        ← H_9327 벽의 정체
연산자 `지 않다` read ◀── [ 저장소 B ] ◀── 연산자-키 write   ← H_9334: 이건 된다
```

**EN 팔이 묻는 것 = 이 분리가 어디서 오는가.** 한국어 `지 않다` 는 어간에 **붙는 어미**라 별도 키-공간을
만들 수 있다. 영어 `not` 은 **떨어져 서는 자유 단어**다.

| EN held-out flip1 | 함의 |
|---|---|
| **우연 초과** | 두 저장소 분리는 **형태론이 만든 것** ⟹ **BINDING = 형태론**, 기질 아님 ⟹ 레인 재개방 |
| **우연** | 자유 부정어로도 분리가 살아남음 ⟹ **byte-LM×CE 가 표면-키 저장소를 만든다**(아키텍처 성질) ⟹ 벽은 진짜지만 **H_9334 의 처방으로 고칠 수 있다** |

어느 쪽이든 판별이 난다. ⚠️ EN 양성은 여전히 **스크리너(DIRECTIONAL)** — EN 은 형태론 + 기반모델 +
담체를 한꺼번에 바꾼다.

## NEXT (현재 진행)

s11@20k(2번째 seed · 게이트가 인증한 예산) → summer `anima-py` 를 main 으로 올리고 **모든 eval 을 한
코드 버전에서 재측정**(0.13.24 ↔ 0.13.45 사이 GPU parity 경로가 움직였다 · seed 마다 다른 코드로 잰
숫자를 한 표에 올리지 않는다) → CPT `ground_keep --lang en` → **WRITE 게이트**(held-out flip0) →
**DV**(held-out flip1) + LIE 통제군.
