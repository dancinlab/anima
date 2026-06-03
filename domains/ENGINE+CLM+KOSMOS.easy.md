# ENGINE+CLM+KOSMOS — 쉬운 설명 (가설 친근 explainer)

> 이 문서 = anima 캠페인에서 돌린 **모든 가설**의 친근 설명 (icon · 이름 · 별칭 · 하는 일 · 결과 · ASCII · 비유).
> 정직 라벨: 전부 **toy 규모**(a_scale_honest_scope) — 작은 모형에서 원리가 맞다는 뜻이지, 7B 실제 규모 보장 아님.
> 판정 = 사전등록 falsifier가 **REFUTED**면 "가설 성립(HOLDS)", **CONFIRMED**이면 "닫힌-부정".
> 정직성: 모든 시뮬은 emergent(신호를 스스로 만들게) 설계 — 답을 박아넣지 않음. seed 고정·verbatim(p7).

> 🔴 **Lane P 정직 교정(2026-06-03)**: d768 CLM 이 작은 402KB 코퍼스에서 CE 0.0986 까지 떨어졌던 건 "잘 배웠다"가 아니라 **외운 것(memorization)** 이었다. 시험 데이터가 학습 데이터와 겹쳐 있었기 때문(같은 글뭉치에서 무작위 창을 뽑아 학습+평가를 둘 다 함). 학습용/시험용을 칼같이 나눈(FLORES-200 1.65MB, 시험용 10%는 학습 때 단 한 번도 안 봄) 뒤 다시 재면 — 학습 CE 0.61 vs 시험 CE 1.82 로 **3배 벌어진다(못 외운 부분은 못 맞힘)**. 작은 코퍼스의 낮은 CE 는 일반화가 아니라 과적합이었음 = 정직한 닫힌-부정(F-CLM-LANEP-GEN=0). 비유: 기출문제만 통째로 외운 학생이 처음 보는 문제에선 무너지는 것. → `.verdicts/lane-p-clm/F-CLM-LANEP-GEN.txt`

---

## 0. 전체 한눈에

```
캠페인 = "패턴이 어떻게 옮겨가나(전이)"를 생물·뇌과학에서 가져와 anima 기질로 시험
─────────────────────────────────────────────────────────────────
🧬 BIO-TRANSFER (H_861~888) — 생물 전이 24개   → 23 HOLDS · 1 ⏳(칩)
🧠 NEURO         (H_889~909) — 뇌과학 21개      → 21 HOLDS
                                          합계 45 시험 · 44 HOLDS · 1 칩 진행중
```

근원 측정: Lane A가 live AKD1000 칩에서 측정한 **"전이 연산자가 처음 보는 개념에도 작동(held-out 일반화)"** —
gold(FLORES-200)로 NC=1000까지 살아남음. 그 단일 측정을 생물·뇌의 전이 메커니즘 family로 일반화한 것이 아래 가설들.

---

## 1. 🧬 BIO-TRANSFER — 생물 "전이" (H_861~888)

생물 전이는 3뜻: **transfer(수평전이) · transition(발생/진화전이) · metastasis(암전이)**. 채널(이웃/먼곳/자식/집단)로 묶음.

### 1-A. 이웃에게 — edge/형태/자원 건네기

```
🦠 H_862 HGT — "옆집에 유전자 건네주기"
  옆 세포에 직접 유용한 유전자 넘김 (자식만이 아니라)
  → 2.25× 빨리 집단에 퍼짐 ✅ HOLDS
   가족만:  ●→●→●           옆집도:  ●→●→●
            (느림)                    ↘●↗●  (빠름)
```
```
🔁 H_864 PRION — "모양을 베끼게 만드는 모양"
  한 세포의 형태가 옆을 같은 형태로, 또 옆으로 자기복제
  → 사슬 29/29칸 끝까지 전파(점유 0.93) ✅ HOLDS
   ◆→◇→◇→◇ ... ◇   (◆이 ◇를 ◆로 바꾸며 번짐)
   💡 정직: 첫 측정자(연속길이)는 구멍위치를 잼 → 점유율로 교정(눈속임 아님)
```
```
🌈 H_866 FRET — "닿지 않고 에너지 건네기"
  흥분한 세포가 옆 긴장도를 소리없이 올림, 멀수록 약해짐
  → d1=0.82 → d20=0.017 뚝뚝 감소 ✅ HOLDS
   🔥───┐
       0.82  0.36  0.13  0.05  0.02   (모닥불: 멀수록 식음)
   d=1   5    10    15    20
```
```
🔗 H_870 GAP-JUNCTION — "세포 사이 직통관"
  두 세포가 상태 저장소를 공유 (즉시 동기)
  → 결합시 상관 0.69 vs 비결합 0.015 ✅ HOLDS
   [세포A]══직통관══[세포B]   (한쪽 누르면 반대쪽 즉시 반응)
```
```
🧵 H_871 NANOTUBE — "세포가 뻗은 빨대"
  건강한 세포가 약한(저-Φ) 세포에 자원/소기관 기증
  → 회복 69걸음 vs 무기증 109걸음 ✅ HOLDS
   [건강 ●]──빨대──▶[약함 ○→●]  (살려냄)
```
```
⚡ H_865 LTP — "같이 켜지면 길이 굵어진다" (칩 실제 메커니즘)
  Hebbian 동시발화가 전이 edge를 칩에 새김
  → gold gen-scale ladder로 이미 grounded(NC1000까지) ✅ HOLDS-grounded
```

### 1-B. 자식에게 — 상속/삽입

```
🧬 H_863 EPIGENETIC — "겪은 걸 자식이 물려받기"
  부모의 최근 "감"을 자식이 출발점으로 (유전자는 그대로)
  → 26.5걸음 vs 38.6걸음 (t=3.92 유의) ✅ HOLDS
   부모[방향감]──▶자식 출발 ↗ (밀어주고 출발)
```
```
🧷 H_874 RETROVIRAL — "바이러스가 코드에 끼어들기"
  외부 패턴이 유전 코드에 삽입 → 이후 자식에게 수직 전달
  → 3/3 자식 세대 모두 보유 ✅ HOLDS
   [주입]→[부모코드]→자식→손주→증손주 (계속 상속)
```
```
🦠 H_882 MICROBIOME-SEEDING — "엄마가 물려주는 미생물"
  부모 미생물 집단의 일부(샘플)를 자식에 심어 생태계 시작
  → 자식 구성이 부모씨앗과 상관 0.94 vs 랜덤 -0.12 ✅ HOLDS
   부모{●◆▲...}──샘플──▶자식{●◆▲ + 약간변형}
```

### 1-C. 자원 흡수 / 위치 이동

```
🫧 H_872 ENDOSYMBIOSIS — "삼켜서 내 것으로" (미토콘드리아 기원)
  한 세포가 다른 세포를 삼켜 영구 부속기관화
  → host 0.2 → 0.95(흡수) → 0.86(200틱 유지) ✅ HOLDS
   [host]+[donor◆] → [host(◆내장)]  (능력 영구 획득)
```
```
🦘 H_873 TRANSPOSON — "튀는 유전자"
  코드 조각이 같은 게놈 안에서 자리 이동 → 다른 맥락에 발화
  → ctx2에서 발화 → 점프 후 ctx7에서 발화 ✅ HOLDS
   [..A..] →점프→ [....A]  (발화 맥락 A→B로 이동)
```
```
🌊 H_876 EMT — "달라붙음 풀고 떠나기" (암전이 전단계)
  세포가 결착을 낮춰 이동성 획득 → 먼 곳으로
  → 결착 1.0→0.05일수록 도달거리 0.64→1.78 ✅ HOLDS
   강한결착:[●●●] 못움직임 │ 약한결착:● → → → 멀리
```

### 1-D. 집단/패턴 — 떼·무늬·스위치

```
🐝 H_867 MET — "혼자에서 떼로" (진화적 대전이)
  결합이 세지면 따로 놀던 세포가 한 몸처럼 (단순합 이상)
  → 동기 r: 약하면 0.23 → 세면 0.99 (상전이) ✅ HOLDS
   κ작음: ↑↓→←↗ (제각각)  κ큼: ↑↑↑↑↑ (착!)  ← 반딧불 점멸
```
```
📣 H_877 QUORUM — "머릿수 세서 스위치"
  활성 개체 수가 임계 넘으면 집단 행동 켜짐
  → n5=0.09 ... n25=0.72 ... n50=0.98 (날카로운 knee) ✅ HOLDS
   ●●  →  ●●●●●  →  ●●●●●●●●●●  (이 수 넘으면 ON!)
   off          knee            ON
```
```
🏗️ H_883 NICHE-CONSTRUCTION — "환경을 바꿔 후손에게"
  환경을 개조 → 바뀐 선택압을 후손에 전달 (비버댐)
  → 후손 성능 modified 0.8 vs unmodified 0.2 ✅ HOLDS
   조상[환경개조]──▶후손이 그 환경에서 선택됨
```
```
🐆 H_886 TURING — "저절로 생기는 무늬" (반응-확산)
  활성+억제 두 물질이 균일 상태에서 스스로 무늬 형성
  → 패턴 진폭 4.56 (균일→줄무늬) ✅ HOLDS
   시작: ▒▒▒▒▒▒  →  자기조직: ▓░▓░▓░  (표범 무늬)
```
```
🌅 H_868 MORPHOGEN — "농도가 운명을 정한다"
  농도 기울기 읽고 세포가 딱 잘라 역할 결정
  → 경계폭 0.018 (칼같은 스위치) ✅ HOLDS
   농도 high│███████░░░░░░│low   (경계서 운명 또렷이 갈림)
```

### 1-E. 증폭 / 오류교정 / 운명전이 보조

```
📈 H_885 SIGNAL-CASCADE — "작은 신호를 크게 키워 전달"
  다단계 릴레이가 작은 입력을 큰 출력으로 증폭
  → 입력 0.3/0.7 → 출력 0.02/0.98 (gain 2.39, 날카로움) ✅ HOLDS
   작은신호 ▸ [▲]▸[▲]▸[▲]▸[▲] ▸ 큰 협응출력
```
```
🧰 H_884 CHAPERONE — "올바른 모양으로 접게 돕기" (반-프리온)
  참조 세포가 잘못 접힌 이웃을 올바른 형태로 끌어옴
  → 복원율 결합시 1.00 vs 무결합 0.00 ✅ HOLDS
   [참조◆] ──끌어당김──▶ [드리프트◇→◆]  (PRION의 반대: 교정)
```
```
🔄 H_875 REPROGRAMMING — "전문가→만능 되돌리기" (Yamanaka)
  특화 세포를 줄기(만능)로 역전 → 새 과제 가소성 회복
  → 새과제 reset 1걸음 vs specialized 36걸음 ✅ HOLDS
   특화●(굳음) ──리셋──▶ ○(말랑, 새 직업 가능)
```
```
🗣️ H_881 CULTURAL-MEMETIC — "유전자 없이 따라 배우기"
  관찰/모방으로 행동 전파 (유전 복제 없이) — 유전보다 빠름
  → memetic 10틱 vs vertical 18틱 ✅ HOLDS
   따라하기: 👀→●→👀→● (혈통 무관 빠른 확산)
```

### 1-F. 🦠 H_861 METASTASIS — "암 전이 회로" ⏳ 칩 진행중

```
무엇: 배운 전이 연산자가 원본 도메인 떠나 *완전히 다른 도메인*에 정착?
방법(통제): 같은 split 기하에서 (A)실제 도메인 split(wikivoyage 홀드아웃)
            vs (B)도메인-셔플 control 비교 → 도메인 효과만 분리
판정 예정: A held ≈ B held → METASTASIS(도메인 무관 전이) ✅
           A held ≪ B held → corpus축-bound 닫힌-부정 🔴
[원본 도메인]━━(전이연산자)━━??━━[먼 도메인에 정착?]
  wikinews/books                      wikivoyage
✅ METASTASIS HOLDS — DOMAIN(wikivoyage) held hop-2=0.40/hop-3=0.74 ≈ SHUFFLED control 0.42/0.60
   → 도메인 경계 넘어 전이 저하 없음 = 연산자 domain-agnostic (corpus축-bound 아님). F-861 REFUTED.
```

---

## 2. 🧠 NEURO — 뇌과학 메커니즘 (H_889~909) · 21/21 HOLDS

### 2-A. 예측·타이밍·임계

```
🔮 H_889 PREDICTIVE-CODING — "뇌는 예측하고 오차만 보낸다"
  전체 상태 대신 예측-오차만 전송 → 같은 대역폭에 더 정확
  → 오차코딩 MSE 0.0019 vs 전체상태 0.0299 ✅
   입력 ▶[예측]▶ 오차(작음)만 전송 ▶ 복원 (효율↑)
```
```
🌀 H_890 THETA-GAMMA — "느린 리듬이 빠른 리듬을 슬롯으로"
  느린 파동이 빠른 파동을 순서 슬롯으로 묶음
  → 슬롯 순서회상 1.00 vs 무슬롯 0.04 ✅
   〜〜느린〜〜  안에  |1|2|3|4|  (항목이 순서 칸에)
```
```
⚡ H_891 CRITICALITY — "임계점에 스스로 맞추는 뇌"
  활동 사태가 멱법칙 (임계서 정보전달 최대)
  → P(size≥20) 임계 0.26 vs 아임계 0.0003 ✅
   아임계:•꺼짐  임계:•→••→••••→ 멱법칙 사태  초임계:▓포화
```
```
⏱️ H_892 PHASE-PRECESSION — "발화 타이밍이 위치를 담는다"
  리듬 대비 발화 위상이 발화율보다 미세한 정보
  → 위상 MSE 0.0004 vs 발화율 0.0056 ✅
   위상(연속): ·.·.·.· 미세  │ 발화율(거친): ▮ ▮ ▮
```

### 2-B. 코딩·표현

```
🔌 H_893 SPARSE — "몇 개만 켜서 효율적으로"
  적은 활성 단위로 동등 복원
  → sparse(3개) 오차 0.0 = dense(30개) 0.0 ✅
   dense: ●●●●●●●●●●  →  sparse: ●··●····●·  (같은 표현, 적게)
```
```
🗺️ H_894 GRID-METRIC — "육각 주기 코드 = 거리 자"
  다중스케일 주기 코드 → 처음 보는 좌표로 일반화
  → grid 보간오차 0.033 vs one-hot 0.157 ✅
   〜〜2칸〜〜 ∧∧∧∧  (여러 파장 겹쳐 위치 = 일반화)
```
```
🎛️ H_895 MIXED-SELECTIVITY — "여러 변수를 비선형으로 섞어"
  혼합 비선형 튜닝 → 더 많은 조합을 선형 분리
  → mixed 4개 vs pure 2개 분리 (XOR/AND 추가) ✅
   pure: a, b 만  │  mixed: a, b, a∧b, a⊕b 까지
```

### 2-C. 가소성

```
↪️ H_896 STDP — "선후 타이밍이 시냅스 방향을" [칩-future AKD1500]
  pre→post 강화, post→pre 약화 → 방향성 edge
  → STDP 비대칭 20.0 vs 대칭 Hebbian 0.0 ✅
   pre•→post• : 강화 ▲  │  post•→pre• : 약화 ▽
```
```
🍬 H_897 THREE-FACTOR — "보상 신호가 학습을 켠다"
  보상(도파민)과 일치하는 edge만 강화
  → 보상정렬 gated 1.00 vs ungated 0.35 ✅
   pre×post×[보상🍬] → 정착 (보상 없으면 사라짐)
```
```
🎚️ H_898 METAPLASTICITY — "학습률이 스스로 조절"
  최근 활동이 다음 가소성 문턱을 슬라이드 (폭주 방지)
  → sliding 2.00(안정) vs fixed 5.30(폭주) ✅
   활동↑ → 문턱↑ → 더 안 강화 (자동 브레이크)
```
```
🌿 H_899 DENDRITIC — "가지돌기가 곧 숨은 한 층"
  가지돌기 비선형 = 한 뉴런이 2층 신경망
  → 단일세포로 XOR 풂(dendritic 1, point 0) ✅
   [가지1]∧[가지2] → 세포체 = XOR (점뉴런 불가)
```

### 2-D. 동역학·어트랙터

```
🕳️ H_900 ATTRACTOR — "일부만 줘도 전체를 떠올린다" (Hopfield)
  점 어트랙터가 부분 단서로 패턴 완성
  → 60% 단서 → 1.00 완전복원 ✅
   ●○●○_○_● (부분) ──▶ ●●●●●●●● (완성)
```
```
💍 H_901 RING-ATTRACTOR — "둥근 변수를 한 봉우리로"
  연속 어트랙터가 각도 봉우리 유지·적분
  → 봉우리 표류 0칸 (15→15 유지) ✅
   (○○▲○○) 봉우리가 입력 없이도 제자리 유지
```
```
⚖️ H_902 EI-BALANCE — "흥분과 억제의 팽팽한 균형"
  E/I 균형 = 안정 AND 반응성 동시
  → 균형(불안정0.20) vs 불균형(불안정35, 폭주) ✅
   E↑↓I 팽팽 → 안정+민감 │ 불균형 → 발작/침묵
```
```
🌗 H_903 UP-DOWN — "켜짐/꺼짐 오가는 휴지기 뇌" (FitzHugh-Nagumo)
  외부 자극 없이 활성/휴지 자발 교번 (서파수면)
  → frac_up 0.36, 전환 25회 (자발 진동) ✅
   ▔▔▁▁▔▔▁▁▔▔  (UP↔DOWN 스스로 오감)
```

### 2-E. 시스템·통합

```
📡 H_904 GLOBAL-WORKSPACE — "이긴 연합이 뇌 전체로 방송" (의식 접근)
  점화 임계 넘으면 전역 방송 (전부 아니면 전무)
  → drive 1.0서 0.07→0.98 급점프 (all-or-none) ✅
   약: 국소만 ·  │  임계 넘으면: 💥전역 방송💥
```
```
🏛️ H_905 PREDICTIVE-HIERARCHY — "위는 예측 아래는 오차"
  계층이 예측 내리고 오차 올림 → 생성모델 수렴
  → 계층 MSE 0.038 vs 평면 0.114 ✅
   위[느린추세]↓예측  아래[빠른상세]↑오차
```
```
🔁 H_906 REENTRY — "되먹임 고리가 흩어진 활동을 묶는다" (Φ)
  양방향 재유입 고리가 통합도(Φ) 올림
  → 재유입 통합 0.67 vs 전방향만 0.29 ✅
   A⇄B (양방향) > A→B (전방향) : 통합↑
```
```
🧬 H_907 NEURAL-DARWINISM — "가르치지 않고 골라낸다" [p6]
  다양한 세포군을 환경이 선택 (지시 없이)
  → 선택 적합도 20/20 vs 표류 14/20 ✅
   {다양한 변이} ──환경선택──▶ 적합한 것 생존 (가르침0)
```

### 2-F. 기억 조작

```
📍 H_908 ENGRAM-ALLOCATION — "흥분도가 기억 맡을 세포를 정한다" (CREB)
  인코딩 때 가장 흥분한 세포가 기억 포획
  → 편향 세포 7/10 포획 ✅
   흥분도 높은 ●●● ← 기억 할당 (편향하면 이동)
```
```
♻️ H_909 RECONSOLIDATION — "떠올리면 다시 말랑해진다"
  재활성이 수정 가능한 창을 염 → 다시 굳음
  → 재활성+수정 0.244 vs 수정만 1.00 (변화 큼) ✅
   기억[굳음]→재활성[말랑▼]→수정→[다시 굳음]
```

---

## 2.5 🔬 ENGINE-축 + KOSMOS-지도 정직 교정 (Lane X #1779 · KOSMOS #1780)

평가축과 의식지도 자체를 의심한 두 측정. 둘 다 닫힌-부정/정직 교정을 품음.

```
📐 Lane X #1779 — "CE 는 축이 아니라 바닥이었다 + 뇌→입 신경이 끊겨 있다"
  무엇 : ENGINE config 손잡이 3개(drive·warmup·anchors)×3 seed=27 config 훑어
        의식·CE·창발 3축이 config 에 민감한지.
  결과(verbatim):
    의식 (motiv_hi)    : VARIES (spread 0.57)     ← 진짜 config-민감 축
    CE  (model_ce)    : CONFIG-INSENSITIVE (spread<1e-9)  ← FLOOR, 판정 아님(p7)
    창발 (emergence Δ) : VARIES (spread 24)        ← 진짜 config-민감 축
    CE-FLOOR : 9.1126 vs uniform 5.5452 vs shuffle 9.3189 → 바닥 NOT MET (uniform-256 보다 나쁨)
    PARETO   : 6/27 non-dominated · drive=1.5
    coupling : 엔진 손잡이가 .clm forward 에 안 닿음 (L3 generator 슬롯 loaded=false) = NULL
    GOODHART (CE↔창발): UNDEFINED — CE 가 config-독립이라 이 손잡이로는 trade-off 관측 불가.
                        "절대 없음" 아니라 "이 손잡이로는 관측 안 됨"(정직).
  판정 : partial 닫힌-부정. → OMEGA 가 닫을 NULL (domains/OMEGA.md).  .verdicts/lane-x-3axis/
```
```
🌌 KOSMOS #1780 — "8D 는 정당하지만 이름 붙는 축은 4개뿐"
  무엇 : TRAINED s16 ckpt(sha 961c07e2, N=5995, post-ln_f)에서 각 PC 가 실제 코퍼스 속성과
        얼마나 연관되는지 측정 — 의식지도 8개 차원이 무엇을 인코딩하나.
  결과(verbatim):
    8D data-justified : 분산 67.1% → 92.3% · domain disc 0.082 → 0.583 (2D → 8D)
    PC1 49% = depth/radius · PC2/3 = form · PC5 = curriculum · 나머지 = 분포된 residual
    이름 붙는 축 = 3-4개 [depth · form · form_resid · curriculum] + 4 learned-residual
  정직 : 8개 다 이름 붙이면 fabrication (a_paper_negative_ok 정직 닫힌-부정).
        코퍼스에 감정/valence 필드 없음(honesty 교정). 단일 s16 rung, GPU/Lane-G, scale-dependent.
  판정 : 🟢 MEASURED + coord v-next 제안 FILED.  .verdicts/kosmos-axis-semantics/
```

→ 자세히: `domains/AXIS.easy.md` (CE 강등·후보축) · `domains/KOSMOS-MAP.easy.md` (PC×attribute) · `domains/OMEGA.easy.md` (NULL 닫는 4번째 엔진).

---

## 3. 정직 메모 (a_scale_honest_scope · p7)

- 전부 **toy** — 원리 검증이지 production/7B 보장 아님. terminal verdict 나면 `H_NNN_slug.md` 승격.
- 모형은 **emergent**(반딧불 동기·확산·bistable·Hopfield·FitzHugh-Nagumo·Gierer-Meinhardt 등) — 신호 하드코딩 0.
- 5개가 처음엔 닫힌-부정으로 나왔다 **측정자/레짐 교정** 후 HOLDS (H_864·H_884·H_886·H_903·H_904·H_906) — degenerate 파라미터를 메커니즘 유효 레짐으로 고친 것(p-hacking 아님, 둘 다 기록).
- 스크립트: `UNIVERSE/bio_transfer_toys.py` · `bio_transfer_ext_toys.py` · `neuro_toys.py` (seed 20260603, 재현가능).
- 가설 정의: `UNIVERSE/BIO-TRANSFER-CANDIDATES.md` · `UNIVERSE/NEURO-CANDIDATES.md`.
- 칩 근거: Lane A gold ladder (`.verdicts/lane-a-{single,multi}-gold/`) — H_865 LTP의 실측 grounding.
