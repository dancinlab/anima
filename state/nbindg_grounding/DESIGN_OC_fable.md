# O/C 채널 설계 — ARBITRARY-GROUNDING 벽 위에서

설계 전에 하나만 분명히 하고 시작합니다. 질문 6개 중 "the question behind the question"이 사실상 설계 전체를 결정하므로 **그것부터 답하고**, 그 위에 O/C를 얹겠습니다.

---

## 0. 진단의 재정식화 — CE가 근거 없는 슬롯에 안정된 임의값을 설치하는 이유

`이 영화 <atom> => ` 다음 위치의 softmax는 **무언가를 반드시 출력해야** 합니다. grid 학습은 이 슬롯에 함수 `f: atom_bytes → {긍정, 부정}`를 설치하는데, taught atom 집합은 닫혀 있고 303M에게 수백 개 lookup은 공짜이므로 CE의 최소해는 **rote lookup**입니다. lookup으로 grid 라인이 전부 fit되는 순간 이 슬롯의 gradient는 0이 되고, 그 이후 자연 코퍼스를 아무리 읽어도(717 contexts, occ≥100) **슬롯을 갱신할 압력이 존재하지 않습니다**. untaught atom에 대한 응답은 학습된 적 없는 입력에 대한 `f`의 generalization — 즉 rote map의 **byte-feature hash**입니다. 결정론적 함수이므로 atom마다 안정적이고(I(atom;resp)=0.231), byte 표면 유사성은 극성과 무상관이므로 gold와는 동전던지기입니다(I(gold;resp)≈0, 12/29).

그러니까 H_9286의 "installed WRONG"은 미스터리가 아니라 **shortcut map의 결정론적 외삽**이고, 벽의 정확한 명제는:

> **자연 노출은 (아마도) atom의 valence 정보를 어딘가에 형성하지만, carrier 슬롯의 학습 신호가 그 정보를 소비할 이유를 한 번도 제공하지 않았다. 슬롯이 계산하는 함수의 입력에 distributional evidence가 없다.**

따라서 "the question behind the question"에 대한 제 답은 **예 — 이것은 loss의 문제가 아니라 코퍼스가 슬롯에서 무엇을 predictable하게 만드느냐의 문제**입니다. 다만 결론이 "O 채널을 버려라"가 아닙니다. O 채널을 **loss 항 추가가 아니라 데이터 분포 설계**로 구현하면 두 관점이 하나가 됩니다. loss 식은 CE 그대로 두고(제약 충족), CE가 최소화하는 **landscape**를 바꿉니다.

단, 위 명제에는 검증 안 된 전제가 하나 있습니다 — "(아마도) 어딘가에 형성" 부분. **valence 표현이 자연 문맥 안에서라도 존재하는가**는 frozen ckpt에서 $0으로 판독 가능하고, 이것이 O-first냐 C-first냐 아니면 둘 다 무의미하냐를 가르는 분기점입니다(§4 AUDIT-A).

---

## 1. O 채널 — 구체 설계

### 1.1 무엇이 바뀌는가 (정확히)

**Loss 식은 바뀌지 않습니다**: `L = Σ_t CE(x_t | x_<t>)`, token-level, weight 없음(자유 하이퍼 0 — mitosis WB-shrinkage 교훈). 바뀌는 것은 `D_train` 세 가지:

**(i) 3-way answer alphabet.** 슬롯 답이 `{긍정, 부정, 모름}` (byte strings). "확정-금지"는 별도 penalty 항이 아니라 **모름이 CE-정답인 라인의 존재**로 구현됩니다. confident-wrong의 초과 penalty = 그 라인들 위에서의 CE 자체.

**(ii) GRID_null — 모름 클래스의 구성 (설계의 급소).** 두 부류, 1:1:
- **NONCE**: 한국어 음운·형태 규칙을 지키는 위조 eojeol (코퍼스 출현 0회). 진짜처럼 보여야 함 — 이상한 byte열이면 모델이 "무근거→모름"이 아니라 "괴상함→모름"을 배움.
- **NEUTRAL**: 코퍼스에서 실제로 캐낸 고빈도 무극성 atom (사전등록 통계로 선별, 예: sentiment-lexicon PMI |·|<τ; **non-held-out에서만** 선별). 이 클래스가 진짜 부담을 짊어집니다 — "자연 노출 있음 + 극성 signature 없음 → 모름"을 가르쳐서, 판별 feature가 **grid-familiarity가 아니라 distributional valence signature**가 되도록 강제.

⚠️ 여기서 치명적 함정: 모름 클래스를 "자연 노출은 있으나 grid에 없는 극성 atom"으로 채우면 **모델에게 distributional evidence를 무시하라고 적극적으로 가르치는** anti-grounding이 됩니다. NEUTRAL은 반드시 극성-부재 atom이어야 합니다.

**(iii) GRID_rot — fold-rotation one-shot stream (코퍼스-predictability 레버의 본체).** 라벨 있는 non-held-out 극성 atom 풀 `P`(가능한 한 크게, 1–2k)를 잡고, 각 atom이 authored grid 라인에 **정확히 k=1회**만 등장하는 스트림을 만듭니다. 스케줄: static taught grid는 E*≈12k step knee까지 기존대로(task 자체를 먼저 설치 — "task-선행"), rotation 라인은 해당 atom의 자연 노출이 축적된 **뒤에** 흘림(per-atom "label-후행" — one-shot 시점에 bind할 distributional summary가 이미 존재해야 하므로).

왜 이게 코퍼스-레벨 fix인가: 반복되는 grid에서 rote lookup은 loss를 0까지 깎지만, **한 번만 나오는 라인의 스트림**에서는 개별 암기가 사후에 무용합니다. 스트림 전체의 기대 loss를 낮추는 유일한 경로는 atom들이 **공유하는** feature — 즉 자연 노출이 만든 valence signature — 에서 답을 계산하는 route이고, 그 route에만 지속적인 양의 gradient가 흐릅니다. **처음으로, "자연 분포에서 극성을 읽어 슬롯에 쓰는 것"이 CE를 낮추는 행위가 됩니다.**

### 1.2 Gradient가 각 atom 유형에서 하는 일

- **Grid-determined taught atom**: gold 극성으로 gradient — N2와 동일하되 경쟁자가 하나 늘어남. `logit(gold) > logit(모름)`이어야 하는데 `logit(모름)`은 무근거-atom들 위에서 default로 훈련되므로, 확정에는 atom-특이적 evidence가 필요해집니다. 모름은 사실상 **학습된 evidence threshold**.
- **Rotation atom (첫·유일 노출)**: gradient 1 step. per-atom 암기 성분은 일회성 소음, route(공유 feature) 성분만 스트림 전체에서 일관 누적.
- **Held-out (natural-only) atom**: **슬롯 direct gradient는 여전히 영원히 0** — 이건 정직하게 못박아야 합니다. O 채널은 held-out을 직접 감독하지 않습니다. 바꾸는 것은 슬롯이 계산하는 **함수의 형태**입니다: N2의 `f(bytes)→{긍,부}` (임의 hash 외삽 강제) 대신 `f(bytes, evidence)→{긍,부,모름}`, 훈련 데이터의 최소해가 "valence evidence 없으면 모름". held-out의 행동은 이 함수의 순수 generalization.

### 1.3 퇴화 모드와 scale 고정 (held-out 안 보고)

- **전부-모름 퇴화**: static taught atom의 gold gradient가 계속 살아 있으므로 전역 abstain은 taught 라인 loss를 폭등시켜 자체 억제됨. V-gate로 확인(taught coverage ≥0.9, §5).
- **모름-무시 퇴화**: 혼합비로 억제. **비율은 사전 고정, 근거는 대칭성**: `긍:부:모름 = 1:1:1` (튜닝 대상 아님 — a-priori 원칙).
- **rotation 스트림 규모**: rotation의 byte-share를 static grid가 knee에 도달했을 때의 byte-share와 일치시킴 — **E*는 이미 측정된 훈련셋 통계**이므로 held-out을 보지 않고 고정됨.
- 유일하게 허용하는 검증 루프: **held-IN 진단** — `P`의 마지막 fold를 rotation에서 빼서 "자연 노출만 받고 grid에 한 번도 안 나온 non-held-out atom"으로 두고, route가 학습됐는지 측정(V-ROUTE). 이건 eval 대상(91 held-out atoms)이 아니라 훈련분포 내부 validation이므로 tune-to-green이 아니며, 그래도 이걸로 hyper를 돌리는 행위 자체를 1회(사전등록된 rescale retry)로 제한.

---

## 2. C 채널 — 구체 설계와 self-consistency 후보의 평가

### 2.1 제시된 후보(자기-일관성)는 그대로는 **불건전** — 이유가 정확히 H_9286

"atom의 717개 자연 문맥에 걸쳐 자기 자신과 일치해야 한다"는 목표는 **이미 달성돼 있습니다**. I(atom;resp)=0.231의 안정적·임의적 commit이 바로 자기-일관성입니다. 일관성은 truth와 stable-wrong을 구별하지 못하므로, within-view consistency를 훈련 신호로 쓰면 **잘못 설치된 극성을 교정하는 게 아니라 시멘트로 굳힙니다** — 교정의 정반대.

살리는 방법은 **비대칭 cross-view**뿐입니다: 두 view가 evidence 접근성에서 달라야 함.
- **context-view** (evidence-rich): 검증된 자연 문맥 + taught carrier를 이어붙인 query — `"<verbatim review>" 이 영화 <atom> => `. 오라클(H_9291 29/29)이 문맥에서 극성이 회수 가능함을 증명했으니, 모델의 context-view가 gold를 추적**한다면** 여기 실제 signal이 있음.
- **atom-view** (evidence-poor): 현행 carrier 단독 query — 임의 hash가 사는 곳.

**C 채널 = 동결-teacher 단방향 distillation**: teacher는 frozen ckpt의 context-view majority vote (atom당 m=25 문맥), student의 atom-view를 teacher 쪽으로만 당김. 절대 co-train 금지(대칭이면 좋은 view가 나쁜 view로 붕괴하는 경로가 열림 — consistency의 최소해는 "둘 다 hash 채택"이기도 하므로).

### 2.2 무엇이 이것을 부수는가 (사전 명시)

1. **context-view가 이미 hash에 오염**: 모델이 문맥을 읽는 게 아니라 자기 prior(atom hash)를 읽으면 teacher = 소음 증폭기. **frozen ckpt에서 $0으로 판독 가능** — AUDIT-B가 발사 여부를 결정(§4).
2. **오류 상관**: 같은 atom의 717 문맥은 같은 hash prior를 공유 → per-context 오류가 독립이 아니어서 majority vote가 오류를 씻어내지 못함. 통제: context-swap arm(같은 문맥, atom을 중립 atom으로 치환)으로 teacher 판정의 문맥-인과성 증명 — V3 detector-fairness의 판박이.
3. **구조적 순수성 문제 (가장 중요)**: student를 held-out atom에 대해 훈련하려면 pseudo-label carrier 라인을 **저작**해야 하는데, 이는 "held-out은 authored grid 라인 금지" 제약과 양립 불가입니다. 문구가 아니라 의미의 문제: C-loop을 돌리는 순간 실험은 "자연 분포가 접지시키는가"가 아니라 **"label-free 자기증류 recipe가 접지시키는가"**를 측정합니다. 이건 우회할 수 없는 구조적 사실이므로, C-arm은 **주장 범위를 사전등록에서 강등**해야 합니다: C-arm은 natural-emergence를 영원히 cement할 수 없고, "label-free correction recipe"라는 별개 claim만 걸 수 있음. (그리고 그 claim도 가치가 있습니다 — H_9286 reopen 조건 "held-out 극성 접지시키는 데이터/objective"의 objective 쪽 후보이므로.)

---

## 3. 순서 — 그리고 각각의 NULL이 뜻하는 것 (비대칭)

**$0 audit 2개(A·B)가 먼저이고, audit 결과가 순서를 결정합니다.** 기본 권고는 **O-first**:

| Audit 결과 | 발사 |
|---|---|
| A+ (weights 어딘가에 held-out valence 존재) | **O-first** — route의 입력이 존재하므로 rotation이 그것을 슬롯에 배선하는지가 정확히 다음 질문 |
| A− ∧ B− | O도 C도 발사 금지 — valence가 어디에도 안 형성됨. **BRIDGE 설계로 전환**(§아래) |
| A− ∧ B+ (저장은 안 됐는데 문맥에서 online 계산은 됨) | **C-first** — 증류가 online 계산을 weights에 저장시키는 게 정확한 처방 |

O를 기본으로 두는 이유: C는 teacher 품질이라는 **지금 측정 가능한** 전제조건에 걸려 있고, 제 예측으로는 B가 죽을 확률이 높습니다(context-view도 hash를 따라갈 것 — 모델은 문맥-판정 task를 배운 적이 없음). O는 전제조건이 더 약하고, 실패해도 더 많은 것을 가르쳐 줍니다.

**NULL의 의미(비대칭의 본체):**
- **O-NULL** (V-ROUTE 통과 — held-in fold에서 route 학습 입증 — 인데 held-out은 bar 미달): "CE에게 distribution→label route를 배우게 만들고 그 route가 훈련분포에서 작동함을 증명해도, grid에 한 번도 안 나온 atom에는 적용되지 않는다" = **task-format 노출이 필요조건**이라는 격상된 벽. 이 recipe 계열에서 natural emergence의 정직한 terminal에 근접. (⚠️ V-ROUTE가 실패하면 NULL이 아니라 **VOID** — 벽 진술 아님.)
- **C-NULL** (AUDIT-B 통과 후 loop 실패): teacher signal이 실재하는데 carrier 슬롯이 안 움직임 = **슬롯 rote-lock** — 가소성/carve 소견으로 σ 쪽에 기록될 별개 발견.
- **C가 AUDIT-B에서 사망**: $0, 예상 범위 — "자연 코퍼스가 연산자를 공급하지 않는다"는 G1 DATA-벽(H_9304) 정합.

**BRIDGE (A−∧B− 시의 코퍼스-predictability 대안)**: 450k 리뷰에 원본 rating/별점 메타데이터가 있다면, rating을 문서의 일부로 포함시켜 **자연 포맷 안에서 valence를 predictable하게** 만듦 — CE가 rating byte를 예측하려면 리뷰 속 atom들이 feature가 되어야 하고, taught atom이 grid-슬롯과 rating-슬롯 양쪽에 등장해 포맷 간 다리를 놓음. 단 이건 distant supervision이라 leak 분석을 사전등록해야 하고("held-out atom의 라벨은 안 주지만 그 atom이 든 문서의 라벨은 줌"), eval gold가 그 rating에서 파생됐다면 회색지대임을 명시. 주장 범위는 "무감독 접지"가 아니라 "자연 약감독 접지"로 강등. rating이 코퍼스에 없으면 이 팔은 사망.

---

## 4. $0 pre-fire audit — 이 계획을 죽일 수 있는 측정

전부 frozen 4 ckpt + 450k 코퍼스, 지출 0. **각각에 KILL 조건이 있습니다 — 이 설계에 불리한 방향으로.**

**AUDIT-A — "weights에 valence가 저장돼 있긴 한가"** (O의 사활).
91개 held-out atom 각각의 자연 출현 위치에서 hidden state를 뽑아 atom별 pool → leave-one-atom-out linear probe로 gold 극성 decode. **결정적 통제 = atom-swap**: 같은 문맥에 길이-정합 중립 atom을 치환해 넣은 표본으로 같은 probe — 이게 같은 점수면 probe는 atom이 아니라 **이웃 감성어를 읽은 것**(문맥엔 당연히 감성어가 있음). 판정은 raw 값이 아니라 `Δ = probe(atom) − probe(atom-swapped)` (FORM tunable·BIND earned). ckpt 4개 전부에서 실행 — base_only에서도 Δ>0이면 valence 형성은 grid 무관, shuffle_grid 대비도 확인. **KILL: 어느 ckpt에서도 Δ가 permutation null을 못 벗어나면 → route에 입력이 없음 → O 단독 발사 금지, BRIDGE로.**

**AUDIT-B — "context-view는 hash보다 나은가"** (C의 사활).
frozen ckpt에 `"<verbatim review>" 이 영화 <atom> => ` query를 atom당 m개 문맥으로 날려, (i) majority의 gold 일치율, (ii) atom-view 응답과의 상관 r. **KILL: gold 일치 ≈ 0.5 ∧ r 높음(문맥이 아니라 자기 prior를 읽음) → C 사망.** 보조 통제 = context-swap(문맥-인과성). n 주의: held-out 91 atoms 기준으로 power 사전계산(power-before-negative-verdict — n=29짜리 판정 반복 금지).

**AUDIT-C — "임의 hash는 무엇의 함수인가"** (설계 정보).
frozen atom-view 응답을 회귀: 최근접 taught-atom byte n-gram 유사도의 라벨 · 형태소 접미(−스럽다/−하다) · 빈도 · 길이. nearest-taught-neighbor가 응답을 설명하면 shortcut-map 외삽 진단이 확정되고, NONCE 설계 요건(taught와의 byte 거리 분포를 실제 held-out과 정합시켜야 함)이 여기서 나옴.

**AUDIT-D — dose-response** (노출-증량류 아이디어의 사활).
held-out atom의 occ 수(100~수천)와 AUDIT-A probe Δ의 관계. **평평하면 "노출을 더 주면 된다"류 팔 전부 사전 사망.**

발사 전 ledger 필수 조회(check-ledger-before-lever-fire): **H_1835 MLC-episodic 🧱**(rotation과 구조 유사 — §6), γ/H_1840 STEP-0 차단, H_9304 G1-DATA. rotation이 MLC와 어떻게 다른 베팅인지(합성 재조합 transfer가 아니라 1차 연상 grounding) 카드에 명기하고 발사.

---

## 5. Pre-registration skeleton

**Arms (4-arm, 단일 seed 1차 발사 ≈ $21; seed-2는 승자 팔에만 조건부 지출):**
| arm | 내용 |
|---|---|
| ARM-O | N2 + rotation + 3-way abstention (full) |
| ARM-ROT | rotation만, 2-way (abstention 기여 분리) |
| ARM-ABS | abstention만, rotation 없음 (rotation 기여 분리) |
| ARM-CTRL | N2 그대로 재훈련, fresh seed s13 (compute-matched baseline) |

**계측 — verbatim 상속** (H_9302/9303 그대로): answer-point read · taught carrier 내부 · raw-corpus 채굴 eojeol · V-LIVE 양성통제 · n=91 · chance sd 0.0524 · bar 0.65 = 2.86σ · form-flip 복원 · 200-draw label-permutation null.

**동결 bar / DV:**
- **P1 (probe)**: held-out probe D-acc ≥ **0.65** ∧ permutation p<0.05 (상속, 이동 불가).
- **P2 (behavioral, abstention 팔만)**: selective accuracy(모름 제외 gold 일치) ≥ **0.75** at coverage ≥ **0.30**. coverage 0.30이면 answered n≈27 → sd≈0.096 → 0.75는 2.6σ. **MDE를 사전 명기**하고 이 미달이면 그 셀은 판정 불가로 기록(NOT NEGATIVE).
- **음성 주장은 TOST**: 등가대역 chance±**0.10** (n=91에서 편측 ~1.9σ) 사전 고정 — "ns라서 벽"은 금지(negative-claims-need-tost).

**V-gates (하나라도 실패 → 해당 수치 INVALID/VOID, FAIL 아님):**
- V-LIVE: taught probe ≥ 0.70 ∧ untaught-control(base_only 상당) 대비 분리 — 아니면 어떤 숫자도 읽지 않음.
- V-DEGEN: taught coverage ≥ 0.9 (abstain 붕괴 검출) ∧ NONCE→모름 ≥ 0.8 ∧ NEUTRAL→모름 ≥ 0.7 (모름 클래스 설치 확인) — 실패 시 사전등록된 rescale retry **1회**(held-in만 사용), 재실패 시 park.
- V-ROUTE: held-in 최종 fold(자연 노출만, grid 미등장, non-held-out) 정답률 ≥ 0.65 — **실패하면 held-out 결과는 VOID**(route 자체가 안 배워졌으므로 벽 진술 불가).
- V-SEED: cement은 seed-2 재현 후에만.

**Decision table (양방향 결정적):**
| 결과 | 판정 |
|---|---|
| ARM-O P1 통과 ∧ V 전부 통과 ∧ ARM-CTRL bar 미달 | 🟢 O-recipe grounding — wire 후 seed-2 |
| P1 미달 ∧ V-ROUTE 통과 ∧ TOST 등가 | 🧱 격상: **task-format 노출 필요조건** — 이 lane의 natural-emergence는 recipe-class 종결, BRIDGE만 잔여 |
| ARM-ROT만 움직이고 ARM-ABS 무변 | abstention은 장식 — 기여는 rotation(코퍼스-predictability 진단 확정) |
| ARM-CTRL이 bar 통과 | 오늘의 벽이 seed 소음 → 계측 재감사 (판정 전부 보류) |
| V-DEGEN 실패 | INVALID (recipe mis-scale), 벽 아님 |

**동결 예측 (1줄):** "ARM-O는 V-ROUTE ≥0.65를 통과하고 held-out의 임의-확정이 모름으로 대거 재배치되나(I(atom;resp|답변) 급감), held-out probe는 AUDIT-A가 양성일 때만 bar를 넘는다; ARM-CTRL은 ≤0.60에 머문다."

---

## 6. 이 설계가 틀릴 가장 유력한 단일 지점

**rotation one-shot stream이 route를 만든다는 가정 자체.** 이건 h1835-MLC-episodic 🧱와 구조적으로 같은 계열의 베팅입니다 — episodic curriculum을 완벽히 마스터해도 held-out transfer가 0이었던 전례가 이 substrate에 이미 있습니다. 제가 기대는 구별점("MLC는 합성 재조합이고 이건 1차 atom→valence 연상이라 bar가 낮다")은 **가설이지 사실이 아닙니다**. 이게 틀리는 구체적 방식: 303M ConvMoE의 expert가 one-shot 라인마저 몇 step 내 국소 암기로 흡수해 first-exposure loss 압력이 route를 만들 만큼 누적되지 않고 — V-ROUTE는 held-in fold의 미묘한 분포 누출(같은 리뷰 도메인, 형태소 겹침)로 **가짜 통과** — held-out만 평평하게 남는 경우입니다. 그러면 $21을 태워 MLC를 재학습한 꼴이 됩니다. 방어선은 두 개뿐입니다: 발사 전 AUDIT-A(route의 입력이 존재하는가)가 음성이면 아예 안 쏘는 것, 그리고 V-ROUTE의 held-in fold를 도메인-분리(리뷰 출처 단위 split)로 구성해 가짜 통과 경로를 좁히는 것.

부차적이지만 기록할 둘째 후보: NEUTRAL 클래스 선별에 쓰는 sentiment-lexicon PMI가 오염돼 있으면(중립이 아닌 atom이 섞이면) 모름 경계가 "무극성"이 아니라 "약극성"에 그어져 abstention이 계통적으로 과확장됩니다 — V-DEGEN의 NEUTRAL 게이트가 이걸 일부 잡지만 전부는 아닙니다.

---

**요약**: loss는 CE 그대로, 바꾸는 건 코퍼스가 answer-slot에서 predictable하게 만드는 것(3-way alphabet + NONCE/NEUTRAL 모름 클래스 + fold-rotation one-shot stream, 자유 하이퍼 0 — 비율 1:1:1과 byte-share는 E*에서 a-priori 고정). C는 within-view self-consistency로는 불건전(임의 hash가 이미 자기-일관적 — H_9286이 그 증거)하므로 동결-teacher cross-view 증류로만 성립하되, held-out 순수성과 구조적으로 양립 불가라 claim이 강등됩니다. 발사 순서는 $0 AUDIT-A/B가 결정하고(기본 O-first), AUDIT-A 음성이면 둘 다 쏘지 말고 BRIDGE(자연 rating 포맷-다리)로 가야 합니다 — 그 경우가 바로 "fix는 loss가 아니라 코퍼스 predictability"가 문자 그대로 참인 세계입니다.