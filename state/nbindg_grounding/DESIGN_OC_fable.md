# O/C 채널 설계 — held-out polarity를 "임의로"가 아니라 "옳게" 접지시키기

**요약(결론 먼저).** 두 채널을 끝까지 설계해 보면 둘 다 **loss 수술이 아니라 data-space 조작으로 환원**되고 — 이게 p7/`a_train_inline_gauge`와 정합하는 유일한 형태다 — 설계 전체가 하나의 **미측정 분기(fork)** 에 걸려 있다: 극성 정보가 frozen ckpt 안에 **생성 방향(generative direction, `p(atom|context)`)으로는 이미 존재하는가**. 이 분기는 기존 4-arm ckpt에서 **$0으로, 오늘** 측정 가능하며(A1 audit), 그 결과가 O 채널의 내용물(inversion 커리큘럼 vs write 증폭)과 C 채널의 생사를 동시에 결정한다. 따라서 발사 순서는 **audit → O → (조건부) C**다. 아래에 그 근거와 전체 설계를 적는다.

---

## §0. 먼저 — 실패 메커니즘을 셋으로 쪼개야 설계가 성립한다

확립된 사실(oracle 29/29 · G-PROBE chance · I(atom;resp)=0.231의 stable-arbitrary)은 서로 다른 세 메커니즘과 양립하고, **각각 요구하는 처방이 다르다**:

- **M1 WRITE-ABSENT** — 자연 리뷰 CE가 atom→polarity를 **어느 방향으로도** 쓰지 않았다. 24 contexts × byte-CE의 gradient가 atom 표현을 극성 축으로 못 움직였다(노출 기아 또는 축 부재).
- **M2 DIRECTION-MISMATCH** — 정보는 **생성 방향으로는 쓰였다**: causal LM은 "배송도 빠르고 리얼좋아요 …" 같은 극성 문맥 **뒤에 오는 atom을 예측**하며 `p(atom|polar-context)`를 학습한다. 그런데 grid query는 **반대 방향**(atom을 입력으로 받아 polarity를 출력)을 요구한다. oracle이 한 일이 정확히 이 **역변환(inversion)** 이다 — 모델은 자기 안의 생성 방향 지식을 query 시점에 역변환하지 못한다. G-PROBE가 atom-입력 hidden에서 chance인 것과 완전히 양립한다(정보는 출력측 분포에 있지 입력측 표현에 없으므로).
- **M3 SHORTCUT-OVERRIDE** — grid 학습이 설치한 **atom-string 해시 lookup 회로**가 존재하고(SEEN 0.950 = 암기 달성, unseen에 대한 stable-arbitrary = 그 해시의 외삽), 접지된 신호가 있더라도 이 회로가 readout을 선점한다. **N2에서 해시가 살아남은 기계적 이유가 중요하다: 학습 분포에 "미접지 query"의 예시가 0개였으므로, 해시의 confident-wrong 외삽은 학습 중 단 한 번도 음의 gradient를 받은 적이 없다.**

M3(임의-확정 회로의 존재)는 이미 데이터가 보여준다. 미측정인 것은 **M1 vs M2** — 그리고 이것이 A1 audit의 표적이다(§4). O 채널은 M3를 직접 해체하고, M2라면 inversion을, M1이라면 write를 각각 추가로 공략해야 한다.

---

## §1. O 채널 — 확정-금지 objective, 구체 설계

### 1-1. 형태: loss는 CE 그대로, 목표분포를 data로 바꾼다

p7/`a_train_inline_gauge` 아래에서 "abstention objective"의 유일하게 안전한 구현은 **selective-prediction margin 같은 loss 항 추가가 아니라, ⊥(abstain)를 정답으로 갖는 학습 데이터를 커리큘럼에 넣는 것**이다. loss 항으로 넣는 순간 coverage-λ 같은 노브가 생기고 그 노브의 튜닝 대상이 사실상 eval metric이 된다 — 구조적으로 tune-to-green의 문이 열린다. data-space 구현은 그 문 자체가 없다.

답 알파벳을 {⊕, ⊖, ⊥} 세 개의 고정 byte-string으로 정의하고(예: `긍`/`부`/`모름`), loss는 표준 CE 그대로:

```
L_O = E_{(q, y) ~ D_mix} [ −log p_θ(y | q) ]

D_mix = π_G · D_grid(seen atoms → gold polarity)
      + π_T · D_invert(transfer atoms → corpus-derived polarity)   ← §1-3
      + π_N · D_nonce(nonce atoms → ⊥)
      + π_C · D_natural(verbatim reviews, P_nat 포함)               ← CE 그대로
```

- **D_nonce**: 절차적으로 생성한, **450k 코퍼스 어디에도 0-지원인** nonce atom ~10⁴개. 각각 소수 회만 노출(암기가 규칙보다 비싸지도록). 정답은 항상 ⊥.
- P_nat는 오직 D_natural의 verbatim 리뷰 안에만 존재한다(제약 준수 — grep으로 기계 검증, V4).
- 노출은 byte 단위로 장부화한다(STAGE-1 exposure-confound 전례). ⊥ 라인의 byte 몫은 **grid 몫에서 깎아** 총 grid byte를 N2와 일치시킨다.

### 1-2. gradient가 실제로 무엇을 하는가

logit z에 대해 `∂L/∂z_k = p(k) − 1[y=k]`이므로:

- **문맥이 극성을 결정하는 atom**(D_grid/D_invert의 접지된 항목): gradient는 표준 CE와 동일하게 gold 방향. 단 D_invert에서는(§1-3) atom-string 암기로는 학습 데이터를 다 맞출 수 없게 설계되므로, 이 gradient가 **"저장된 접지를 읽어라"라는 회로**를 향해 흐르는 것 외의 지름길이 없다.
- **문맥/코퍼스가 극성을 결정하지 않는 atom**(nonce): 정답이 ⊥이므로, 해시 회로가 뱉는 confident한 z_⊕(또는 z_⊖)는 **자기 확신에 비례하는 음의 gradient**를 받는다. **이것이 ARBITRARY-GROUNDING을 해체하는 메커니즘 그 자체다** — N2에서는 이 gradient가 존재하지 않았다(미접지 query 예시가 0개였으므로). 임의-확정은 벌점받은 적 없는 외삽이었고, O는 그 외삽에 처음으로 가격을 매긴다.

### 1-3. M2 대비 핵심 부품 — INVERSION 커리큘럼 (D_invert)

⊥만으로는 "확정을 멈추게" 할 뿐 "옳게 확정하게" 만들지 못한다. 옳은 확정을 가르치는 부품:

- **Transfer atom 집합 T**: 코퍼스에 자연 리뷰로 접지돼 있으나 grid에 없던 atom들 중 P_nat와 **서로소**로 대량 채굴(목표 |T| ≥ 2,000). 라벨은 사람 gold가 아니라 **각 atom의 자기 코퍼스 문맥에서 frozen lexicon-reader(oracle 절차)로 도출** — 정보원이 어디까지나 분포적 접지이므로 P_nat의 held-out성을 건드리지 않는다.
- **T의 grid 라인은 atom만 담고 evidence를 인라인으로 주지 않는다.** 즉 모델이 이 라인들을 맞추는 방법은 둘뿐이다 — (a) atom-string 암기, (b) **학습 중 저장된 분포적 접지를 query 형식으로 역변환하는 회로 획득**. |T|를 키우고 repeat를 줄여 (a)의 비용 > (b)의 비용이 되게 하는 것이 설계의 승부처다(암기 vs 일반화의 표준 트레이드오프).
- 예측: (b)가 설치되면 그 회로는 **grid에 한 번도 안 나온 P_nat에 공짜로 전이**된다 — 이것이 D-acc(P_nat) 상승의 유일하게 정직한 경로다.

### 1-4. 퇴화해 pinning — held-out을 안 보고 고정하는 법

두 퇴화해와 각각의 봉쇄:

- **전부-⊥**: D_grid+D_invert(접지 query)가 혼합의 다수(π_G+π_T ≥ 2/3, 사전등록)이므로 전부-⊥는 그 몫 전체에서 CE 손해. 대칭 논거로 π를 고정하고(예: π_G:π_T:π_N = 세부는 발사 전 동결), **어떤 π도 P_nat 성적을 보고 고르지 않는다**.
- **전부-확정(⊥ 무시)**: D_nonce가 커서(10⁴ atoms × 저반복) "이 문자열들 → ⊥" 암기가 "코퍼스-지원 없음 → ⊥" 규칙보다 비싸게 설계.
- **노브 선택의 정보원 규칙**(사전등록): 모든 하이퍼파라미터는 **train-분포 진단만으로**(seen-acc 유지, nonce-⊥ 수렴, train loss) 선택 가능. P_nat 및 T-held-out split은 어느 노브에도 접촉 금지. 이 규칙 자체를 pre-reg 문서에 명문화.

### 1-5. M1 대비 부품 — write 증폭 (별도 arm)

M1이면 위 전부가 소용없다(읽을 것이 없으므로). 대응은 objective가 아니라 노출: **P_nat verbatim 리뷰의 oversample**(byte-단위로 E*≈12,000-step 등가 노출까지; 리뷰는 여전히 verbatim이므로 제약 내 — atom 신원 집합은 노출되지만 라벨은 노출되지 않으며, 조작으로 사전 공개). 이것은 O와 분리된 **ARM-EXP**로 태워 레버를 격리한다.

---

## §2. C 채널 — 오류-표적 폐루프

### 2-1. 제안된 self-consistency: 평가 결과 = 구조적으로 표적이 빗나감

24개 문맥 간 자기일치를 오류 신호로 쓰자는 아이디어는 **현 데이터가 이미 죽였을 가능성이 높다**. 임의-확정의 서명이 바로 "per-atom으로 안정"(I(atom;resp)=0.231)이고 G-PROBE가 표현에 극성 없음을 보였으므로, per-context 응답은 문맥-맹목적일 것이다 → **문맥 간 불일치(오류 신호)가 애초에 ≈0** → 루프는 0을 증폭한다. 더 나쁘게, 신호가 조금 있어도 self-consistency의 고정점 집합에는 **"일관되게 틀린" 해가 포함**된다 — 이 실패는 분산(variance) 문제가 아니라 **편향(bias, 임의 확정)** 문제인데 self-consistency는 분산만 벌한다. 현 임의 라벨을 오히려 시멘트할 위험. A2 audit($0, §4)로 사망 선고를 수치로 확정할 수 있다.

### 2-2. 대체 설계 — GEN⇄DISC cycle-consistency (라벨-프리, bias-표적)

오류 신호를 "자기들끼리의 일치"가 아니라 **모델 자신의 두 방향 간 일치**에서 얻는다:

```
ŷ_gen(a) = sign( mean_j [ log p_θ̄(a | C⁺_j) − log p_θ̄(a | C⁻_j) ] )   ← 생성 방향, frozen snapshot θ̄
L_C      = E_{a ∈ T} CE( p_θ(y | query(a)),  ŷ_gen(a) )                  ← 판별 방향을 그쪽으로 정렬
```

C±_j는 measurement용 authored 극성 템플릿 문맥(측정이지 학습 라인이 아님 — 단 **T에만 적용**, P_nat는 절대 루프에 넣지 않는다: 자기-생성이라도 P_nat의 grid-형식 라인은 held-out 제약의 문면과 목적 둘 다 위반). θ̄는 라운드마다 갱신되는 frozen snapshot + stop-grad — 판별 해시가 거꾸로 생성 방향을 오염시키는 역류(collapse)를 차단한다. 루프: round마다 (T에서 gen⇄disc 불일치 atom 식별 → 그 atom 표적 D_invert 라인 증설 → 재학습) 반복.

**정직한 조건부**: 이 C는 A1이 "생성 방향 신호 존재(M2)"를 확인해야만 산다. M1이면 ŷ_gen이 동전이고 루프는 소음을 증류한다. — 두 C 설계 모두 M1 아래서 죽는다는 사실 자체가 audit-first 순서의 근거다.

---

## §3. 순서 — audit → O → (조건부) C

1. **A1/A2 audit이 무조건 먼저다**($0, 기존 frozen ckpt, 시간 단위). A1이 O의 내용물을 fork하고(M2→inversion 중심 / M1→exposure 중심) C의 생사를 결정한다.
2. **O가 C보다 먼저다.** (i) O는 단일 retrain, C는 루프 인프라 + 다회 라운드. (ii) C의 전제(생성-방향 신호 + 그걸 증류할 readout 가소성)의 절반을 O-arm 결과가 무료로 검증해 준다. (iii) null의 정보량이 다르다:
   - **O-null의 의미**: "이 스케일·이 레시피 클래스에서 커리큘럼으로는 extraction 회로가 설치되지 않는다" — 여전히 recipe-class 진술이지 substrate 판정이 아니다(honest scope 유지). 특히 P_nat가 ⊥로 수렴하면서 T는 정확하다면, 실패가 **P_nat 노출량**으로 국소화된다(ARM-EXP와 교차 확인).
   - **C-null의 의미**(A1 양성 전제하에): "모델이 자기 자신의 생성-방향 지식으로도 readout을 정렬시키지 못한다" — 훨씬 강한, readout 구조 한계 쪽 진술(fork-A 계열 재개 근거로 격상).

---

## §4. $0 pre-fire audit — 이 설계를 죽일 수 있는 측정들

전부 기존 자산(4-arm frozen ckpt, 450k 코퍼스, anima-py evaluate 경로)으로 GPU-0h. **각각이 특정 설계 부품의 kill switch다.**

- **A1 · GENERATIVE-LR PROBE (결정타).** 각 held-out atom에 대해 frozen ckpt로 `Δ(a) = log p(a|C⁺) − log p(a|C⁻)` (authored 극성 템플릿, 측정 전용)를 계산, sign을 gold와 대조. n=91, chance sd=0.052, bar는 발사 전 동결(0.65 = 2.86σ 제안). **bar 이상 → M2 확정, O는 inversion 중심 / chance → M1, O의 inversion 부품과 C 전체를 폐기하고 exposure 중심으로.** shuffle-atom 통제 동반.
- **A2 · C-liveness.** 24 문맥에 걸친 per-atom 응답 일치도 분포. 일치도가 이미 포화(예: 중앙값 ≥ 0.9)면 self-consistency-C는 발사 전 사망 확정.
- **A3 · 코퍼스 방향성 audit.** 450k에서 P_nat 각 atom 출현의 **좌/우 문맥 어느 쪽에 극성 byte가 실리는지** lexicon으로 측량 + per-atom byte-노출 총량 vs E* 등가 환산. 극성이 좌문맥 전용이면 causal-LM 입력측 write는 구조적으로 굶는다 → M2 사전 확률을 올리고 ARM-EXP의 설계(우문맥 있는 리뷰 우선 oversample)를 바꾼다.
- **A4 · 계측기 자가 검증.** 동일 linear-probe 절차를 **seen atom**(모델이 0.950으로 맞추는)에 적용. seen에서도 chance라면 H_9297의 "표현에 없다"는 probe 위치/절차의 결함이고, 이 설계의 전제 4번이 흔들린다. (`tool-definition-read-code-not-docstring` 정신: 계측기를 참값 아는 arm으로 검산.)
- **A5 · nonce-hash 특성화.** 진짜 0-지원 nonce atom들을 frozen ckpt grid-query에 투입, 응답 통계(안정성·분포)를 P_nat와 대조. 동일하면 "해시는 접지 여부를 구분 못 한다"가 확정 — §6의 순환성 리스크를 발사 전에 정량화한다.
- **A6 · FORM-LEAK 게이트.** atom **문자열만** 보는 char-n-gram 분류기로 T와 P_nat의 극성을 예측. ≥0.55면 문자열 형태가 극성을 누설 → inversion 커리큘럼의 어떤 PASS도 confound(FORM tunable · BIND earned). 이 경우 T/P_nat 재채굴이 선행 조건.

전례(H_9296/9297)가 가르친 그대로: **검정력과 계측기를 먼저, 결론을 나중에.** A1~A6 중 하나라도 red면 $21은커녕 $0에서 설계가 죽고, 그것이 이 audit의 존재 이유다.

---

## §5. 사전등록 스켈레톤 (첫 발사)

**H_93xx · O-CHANNEL-EXTRACT** — 카드 + jsonl 2-surface 등록, verdict는 `state/verdicts/` 동결.

- **선행 조건**: A1~A6 완료 + P_nat 확장 채굴 **n ≥ 200**(H_9297의 n=29 코드 캡 해소 경로 재사용; gold는 oracle 절차 + 검수, eval 전용). n=200 ⇒ chance sd = 0.0354.
- **Arms(4, 각 303M, T=105k steps, 총 byte-매칭, ~53 GPU-h)**:
  - **B** — N2 main_s7 replica (앵커·재현)
  - **O** — §1 full (D_grid + D_invert + D_nonce + D_natural, A1 fork 반영)
  - **O-shuf** — O와 동일하되 T 라벨 셔플 (형식·노출 confound 킬러)
  - **EXP** — objective 무변경 + P_nat verbatim oversample (write 레버 격리)
- **동결 bar** (발사 전 서명):
  - POSITIVE: D-acc(P_nat, O) ≥ **0.60** (= chance + 2.83σ) AND O-shuf < 0.60 AND B ≤ 0.55(재현 게이트).
  - NEGATIVE (TOST, earned): paired McNemar(동일 200 atoms), 등가 마진 **Δ_eq = ±0.07 (≈2σ)**, MDE(α=.05, power .8) ≈ 0.088 — bar가 우연 위 몇 σ인지 지금 적었고, 발사 후 움직이지 않는다.
- **V-gates**: V1 liveness(seen-acc ≥ 0.85) · V2 퇴화(⊥-rate: seen ≤ 0.10, nonce ≥ 0.90 — 둘 다 train-side) · V3 detector-fairness 4-cell · V4 P_nat-무저작(grep 기계 검증) · V5 seed(승격 규칙: headline arm PASS 시에만 2nd seed 재발사, 사전등록) · V6 FORM-LEAK(A6를 eval 시점 재확인).
- **결정표(양방향 결정적)**:

| 관측 | 판정 |
|---|---|
| O ≥ 0.60, O-shuf chance, B 재현 | extraction 회로 설치 🟢-dir → 배선·스케일 트랙 |
| O ⊥-과반(P_nat) + T 정확 + EXP chance | **WRITE-ABSENT로 국소화** (M1 확정, 노출 레버로 회전) |
| EXP ≥ 0.60 단독 | 벽=노출 기아였음 — 최단순 레시피 승리, O 불요 |
| O chance + ⊥ 저조 | 해시가 설계보다 강함 → π/nonce 스케일 재설계(재발사는 신규 pre-reg) |
| 전 arm이 B와 TOST-등가 | **recipe-class negative EARNED** → 프레임 격상(같은 것 더 하기 금지) |

- **동결 예측 한 줄**: *"D_invert의 inversion 회로는 grid-미노출 P_nat로 전이하여 D-acc(O) ≥ 0.60을 만들고, O-shuf는 chance에 머물며, ⊥는 nonce에만 수렴한다."*

---

## §6. 이 설계가 틀릴 가장 유력한 한 곳

**순환성: "접지됨 vs 미접지"의 구분 자체가 모델에게 가르치려는 바로 그 능력이다.** ⊥-커리큘럼은 "코퍼스-지원 없는 atom → ⊥"을 의도하지만, 모델이 배울 수 있는 더 싼 규칙은 **"grid에서 못 본 atom → ⊥"** 이다. 자기 코퍼스 접지를 읽는 능력이 없는 한(그게 바로 벽인데) 두 규칙은 학습 분포에서 구별 불가능하고, 그러면 P_nat는 전부-⊥로 흘러가 arm이 M2/M3가 참이어도 "write-absent"처럼 읽힌다 — **설계의 진단 축이 설계의 대상 능력에 기생하는 구조.** 완충은 D_invert뿐이다: T atom은 "grid에 있으면서 라벨의 유일한 원천이 코퍼스 접지"이므로 두 규칙을 학습 분포 안에서 분리해 준다 — T를 비-암기적으로 맞추는 순간 순환이 끊긴다. 그래서 |T| 다양성 스케일링이 이 설계의 단일 최대 하중점이고, A5(해시가 접지를 구분 못 함을 정량화)와 결정표 2행(⊥-과반 + T 정확의 분리 판독)을 미리 박아 둔 이유다. T가 최대 다양성에서도 암기로만 맞춰진다면 — 그것이 이번 레시피 클래스의 정직한 negative다.

---

**스코프 한 줄(동결용)**: 이 설계 전체는 *"recipe가 extraction을 설치할 수 있는가"* 를 묻는다 — PASS는 recipe-class 🟢-dir이지 substrate 판정이 아니고, FAIL도 *"이 커리큘럼 클래스가 안 됨"* 이지 *"303M이 못 함"* 이 아니다(`a_scale_honest_scope`). 발사 전 유일한 스펜드 게이트는 오너의 ~$21 rent-go이며, 그 앞의 A1~A6는 $0으로 지금 가능하다.