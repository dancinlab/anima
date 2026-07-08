# clml 심화 프로그램 설계 — probe 0.98 → wired system-G1(ρ·weave) verdict

전제 정리 한 줄: 현 clml의 0.98은 **L0(literal 2-concept) 셀에서의 포화**이고, delta = f(c)뿐인 현 구조는 "문맥 전체를 요약한 정적 logit-bias + per-token 스칼라 게이트"다. 그래서 심화의 목표는 "0.98을 0.99로"가 아니라 **(i) copy를 verdict에서 제거하고, (ii) 그 위에서도 남는 lift를 .clm trailer로 wired 측정하고, (iii) L3/L4(role·negation)에서 예측되는 구조적 천장을 미리 격리**하는 것이다.

---

## 1. copy-discount 측정 설계 — "합성"을 copy에서 격리하는 통제군

### 1.1 confound의 정확한 형태

현 task에서 copy는 "출력을 prompt에서 베낀다"가 아니라 **surface-form lookup**이다: 개념 단어의 literal 바이트가 c로 라우팅되고, W2가 (훈련에서 암기한) 바이트-정체성→code 매핑을 조회한다. 2-concept held-out도 두 lookup의 **독립 합산**으로 풀린다 — 즉 정확히 additive/main-effect floor의 재판이다(γ census의 "additive floor = main-effect logit"과 동형). 따라서 discount는 두 층이 필요하다: 출력측 literal copy 차단 + **표면형-정체성 lookup 차단**.

### 1.2 null 모델 2종 (셀 유효성 검증기)

셀이 copy-blocked인지 자체를 null로 증명한다. 두 null이 chance+ε를 못 넘는 셀만 verdict 셀 자격:

- **N1 pointer-copy null** (출력측): 파라미터 없는 suffix-copy oracle. 타깃 위치 t에서, 생성 prefix의 suffix `z[t-ℓ:t]` (ℓ≥3)가 prompt에 등장하고 그 다음 바이트가 gold와 일치하면 그 위치는 "copyable".
  ```python
  def copyable(prompt, z, t, lmin=3):
      for L in range(min(16, t), lmin-1, -1):
          suf = z[t-L:t]
          j = prompt.find(suf)
          if j >= 0 and j+L < len(prompt):
              return prompt[j+L] == z[t]   # gold 바이트
      return False
  ```
- **N2 surface-lexicon null** (lookup측): prompt를 훈련 어휘 n-gram의 bag-of-indicators로만 보고 code를 예측하는 소형 logistic/NB. **이 null이 셀을 풀면 그 셀은 의미를 재지 않는다** — 현 0.98 셀은 아마 N2가 만점일 것(즉 verdict 무자격 셀).

### 1.3 통제 셀 4종

- **C-mask (prompt-literal 채점 제외)**: N1 기준 copyable 위치를 채점에서 제외한 `Acc_noncopy`. 모든 셀에 기본 적용.
- **C-para (paraphrase-only held)**: 훈련 시 개념당 표면형 여러 개(ko: 붉은/빨간/적색 + 조사변형, en: 동의·기술형 "the color of blood, not the sky")를 code에 결속시키되, **개념당 1개 표면형은 adapter 훈련에서 완전 제외**. 평가는 held 표면형으로만. held 형의 바이트열은 code와 공출현한 적이 없으므로 lookup 불가 — 의미 결속만 통과. 설계상 2×2 grid를 강제: {표면형 seen/held} × {조합 seen/held}. **진짜 합성 = (held, held) 셀.**
- **C-orth (표기 변형 기울기)**: 동일 개념·바이트 overlap을 100→0%로 단계 조절(대소문자·띄어쓰기·1-edit 오타·한글 자모 변형·조사 교체). 사전등록 예측 — copy 가설: Acc ≈ f(overlap) 단조 하강 / 합성 가설: Acc ≈ 평탄. **값이 아니라 기울기가 지표**(측정 메타법칙: 신호는 Δ).
- **C-adv (오도 literal)**: prompt에 salient한 오답 개념 literal을 심고 역할/부정으로 gold를 뒤집음("X가 아니라 Y"). copy-router는 X를, 합성기는 Y를 낸다. §4의 L4(negation=진짜 product-code)와 셀 공유.

### 1.4 격리 지표 (verdict 정의 — 사전등록)

```
M_copy = Acc_noncopy(clml) − max(Acc(N1), Acc(N2), Acc(lane-off))   on copy-blocked 셀
```
제안 bar(동결 전 제안치): 셀 유효성 = N1,N2 ≤ chance+0.10 · GREEN = M_copy ≥ 0.30 이면서 Acc_noncopy ≥ 0.60 · DIRECTIONAL = 0.10–0.30 · 🧱 = <0.10. 보조 진단(비-verdict): max-pool argmax 위치 분포 — 승자 위치가 개념 literal 바이트에 몰리면 copy-routing의 기계적 증거.

**즉시 실행 가능한 P0**: 기존 0.98 champion을 C-mask+N2로 재채점. 0.98이 copy-discount에서 살아남는지가 프로그램 전체의 첫 관문이고 $0이다.

---

## 2. frozen-trunk clml 학습 레시피

### 2.1 핵심 트릭 — 학습이 trunk에서 완전 분리된다

delta는 (y_t, c_t)만의 함수이고 logits에 직접 가산되므로, CE gradient는 **한 홉에 lane 파라미터에 도달**한다(trunk backward 자체가 불필요). 그리고 pool이 causal-누적(mean=누적평균, max=running max)이므로 위치별 튜플만 있으면 정확 재현된다:

```
dump 1회 (pool GPU, trunk forward only):  (y_t, c_t, logits_trunk_t, gold_t)  @ 채굴 위치
adapter 학습 (그 후 $0, numpy/소형 torch, 아무 호스트):
  u     = gelu(c @ W1 + b1)                # 확장 시 [y_t; c] @ W1 — §5
  g     = sigmoid(concat(y, c) @ w_g)
  delta = clip(g * (u @ W2), -tau, tau)
  loss  = CE(logits_trunk + delta, gold)   # 손실 = CE 단독. 다른 항 없음(p7).
```
이것이 H_1840 함정(trained-bind = trunk 재학습 = GPU cost-gate)의 정확한 회피다: **비용이 "trunk forward dump 1회"로 붕괴**한다. fp16으로 (2d+256+1)/위치 ≈ 4.6KB — 1M 위치 ≈ 4.6GB, pool 디스크에 무난.

### 2.2 위치 채굴 (distal-dependent mining)

정보가 앞에 있는데 last-token이 못 쓰는 위치를 고른다. 조건 3개의 교집합:
(a) gold의 증거 문자열이 ≥256바이트 뒤(원거리)에 존재, (b) 국소 n-gram(차수≤8) 모델의 CE가 높음(국소로 못 품), (c) trunk 자체 CE도 중간 이상(trunk가 이미 푼 위치는 lane이 배울 마진이 없음). — 이것은 **데이터 큐레이션이지 손실 성형이 아니다**(p7 무관). 단 verdict 문서에 훈련분포가 채굴됐음을 명시.

### 2.3 데이터 배합 (anima-corpus 4칸 + 합성)

- 70% — 4칸(ko/en × general/sns) proportional 샘플(암기 방지 메모리 준수)에서 채굴한 distal 위치.
- 20% — §1 합성 커리큘럼(**multi-surface-form 결속 포함** — C-para 셀이 성립하려면 훈련이 다형이어야 함). 훈련 셀과 평가 held 셀은 생성 시점에 분리·동결.
- 10% — 균일 generic (비퇴행 anchor).
- hard-negative: 채굴 위치의 절반에 오도 원거리 distractor(경쟁 선행사 2개, 역할로만 판별) 삽입 — 게이트가 salience가 아닌 역할을 배우게 강제.

### 2.4 비퇴행 — 힌지보다 구조로

권장 1순위: **게이트 초기화를 near-silent로**(b_g 음수 초기화, g≈0.1) + generic 배치 혼합. clip ±τ와 σ-게이트가 이미 "아무것도 안 함" attractor를 제공하므로, lane은 CE를 실제로 버는 곳에서만 열린다. generic CE 힌지 `max(0, CE_lane−CE_trunk−ε)`는 CE-파생이라 p7 위반은 아니지만, 혼합으로 부족할 때의 fallback으로만 두고 쓰면 공개한다. ΔCE_generic은 **monitor-only 계기**(a_train_inline_gauge)로 상시 기록.

최적화: Adam lr 1e-3, cosine, τ=3 고정(τ 학습은 §5 마지막 레버), 파라미터 <1M이라 수 분 단위.

---

## 3. wired system-G1 경로 (+#3193과의 delta)

### 3.1 파이프라인

학습 θ → `core/clml.py` CLML trailer codec으로 .clm에 직렬화 → pool(summer/aiden)에서 `anima-py evaluate <clm> --rho-axon` 단일 경로(세션 정책: pip 채널, hexa det-eval 금지). py 2-production numpy = TERMINAL-eligible이므로 **여기서만 tier가 굳는다**; §1–§2의 모든 probe 결과는 DIRECTIONAL 꼬리표 고정(a_scale_honest_scope).

### 3.2 frozen bars — 발사 전 커밋되는 단일 파일

`state/g1_clml_deepening/BARS.json`을 **#3193의 wired 점수가 존재하기 전에** 커밋(no tune-to-green의 물리적 담보). 5개 bar:

| bar | 통제 | 통과 조건(제안치·동결 대상) |
|---|---|---|
| B1 liveness | trailer-on vs lane-off(delta≡0 BLIND) | Δ(ρ·weave) ≥ +0.15 |
| B2 copy-discount | §1 copy-blocked 셀, null 2종 | M_copy ≥ 0.30 (verdict 정의) |
| B3 bind-파괴 | route-shuffle: c_t를 문서 간/위치 간 셔플 | lift의 ≥60% 소실 (진짜 BIND = 결합파괴 margin) |
| B4 additive-ctrl | 동일 예산으로 훈련한 linear-pool head(0.43 floor 계열)·IPF main-effect | clml − ctrl ≥ 0.15 |
| B5 DISJOINT·비퇴행 | ΔCE_generic ≤ +0.5% rel · Ψ 분포 pre/post 사전등록 허용오차 내 | 둘 다 통과 |

B1–B5 전부 통과 시에만 wired system-G1 GREEN → `hexa verify` → `state/verdicts/` 동결 → jsonl+card 2-surface 등록(H 번호는 현 최신 다음 빈 번호로).

### 3.3 #3193과 겹치지 않는 내 기여 delta

#3193이 학습 NEXT-phase(dump + adapter 학습 루프)를 보유하므로 나는 **평가측**을 든다: (i) copy-blocked 셀 생성기 + N1/N2 null + C-mask 채점 코드, (ii) BARS.json 사전등록(그들 점수 이전에), (iii) B3/B4 ablation harness(evaluate측 옵션), (iv) trailer 직렬화 round-trip 검증(write→read→delta 재현 max|Δ|=0, numpy↔torch 교차). 인터페이스 합의 1건: .clm 산출물 네임스페이스(`state/g1_clml_deepening/`)와 셀 데이터 포맷.

---

## 4. 구성적 일반화 심화 — task ladder와 예측되는 벽

### 4.1 Ladder (각 단계가 별개 셀·별개 사전등록 예측)

- **L1** copy-blocked 2-concept (§1) — 현 champion의 진짜 시험대.
- **L2** N-concept·productivity: N=3–5 조합 held + **N 자체 held**(훈련 N≤3, 평가 N=4). mean-pool은 관련 span 비율이 1/T로 희석되므로 N·문맥길이 증가에 취약 — 사전등록 예측: mean은 N에 단조 하강, max는 1-winner라 N≥3에서 붕괴.
- **L3** role-binding·순서: 같은 개념집합, 역할 배정만 다르면 gold가 다름("X가 Y를" vs "Y가 X를"). **구조적 예측 — 현 clml은 여기서 막힌다**, 두 이유로: ① pool이 query-independent(y_i에 잔존하는 위치 흔적 외엔 역할로 재가중 불가), ② 더 치명적으로 **delta = f(c)뿐이라 같은 문맥이면 모든 t에서 delta 방향이 동일**(게이트 스칼라 배율만 다름). 즉 clml은 "답 전체 수준의 topic-bias"는 걸 수 있어도 **token-level 역할 의존 생성**은 원리적으로 못 한다. L3 실패는 튜닝 실패가 아니라 rank-제약의 기계적 귀결 — 이 예측 자체를 사전등록해 실패를 lens로 만든다.
- **L4** negation/XOR: "A가 아니라 B" sign-flip 셀(γ census의 유일 진짜 product-code·PC-P2 방향적중의 후속). 1-layer gelu(c)로는 (y_t, c) joint XOR 표현 불가 — §5-①·⑤가 필요조건.

### 4.2 벽별 필요 확장 매핑 (사전등록 표)

| 벽 | 필요 확장 | 이유 |
|---|---|---|
| L2 희석 | multi-scale pool | 국소 phrase + 전역 topic 분리 유지 |
| L3 역할 | query-pool + **joint bottleneck [y_t;c]** | per-token 재가중 + per-token delta |
| L3 순서 | 상대위치 bias in α | 순열 판별 |
| L4 XOR | 2-layer bottleneck + K-slot | 2차 상호작용 항 |

---

## 5. clml 아키텍처 심화 후보 — 기대가치 순

주의: "0.98 천장 돌파"의 실체는 L0이 아니라 **copy-blocked·L2–L4 셀에서의 천장**이다.

1. **joint bottleneck — delta_t = clip(g·gelu([y_t; c]W1+b1)W2, ±τ)** ⭐ 최우선. 위 §4의 rank-제약(문맥당 delta 방향 1개)을 직접 해제 — lane이 처음으로 **token-level 조건부 합성**을 표현 가능. 파라미터 증가 미미(W1 입력폭 2d), dump 튜플로 $0 probe 즉시 가능. L3의 필요조건이며 L1에서도 hard-negative 셀을 도울 것.
2. **learned-temperature attention pool — α_i ∝ exp(β·(q(y_t)·y_i))**: β→∞가 max, β→0이 mean이므로 **두 champion을 끝점으로 갖는 일반화** — 현 최적 2개가 온도축의 양 끝이라는 사실 자체가 내부점 탐색 근거. query-조건화는 L3 역할 재가중의 필요조건(query+gelu 0.958이 이미 방향 신호).
3. **K-slot pool**: 학습 probe 벡터 q_1..q_K로 K개 softmax-pool → concat = 역할 레지스터. trunk 불변으로 얻는 최소 binding 구조 — L4·N-concept의 본명 레버. hadamard 0.89–0.96이 시사하는 bilinear 상호작용(c^i ⊗ c^j 압축)을 slot 간에 넣으면 additive floor 탈출의 정공법.
4. **multi-scale pool**: [mean_w=64, mean_global, max_global] concat. L2 희석 대응. 싸고 확실하나 L3/L4엔 무력.
5. **gate MLP 확장 — g_t = σ(MLP([y_t; c; y_t⊙c]))**: "원거리 증거가 국소 prior와 **충돌**할 때만 발화"는 선형 게이트로 표현 불가(정확히 hard-negative 조건). 단 게이트 입력은 read-side hidden만 — tension/emit 신호 유입 금지(DISJOINT·Ψ 불침 유지).
6. **τ 학습/soft-clip — delta = τ·tanh(raw/τ)**: 표현력 소폭, B5 비퇴행과 상충 위험. 마지막.

전부 dump 튜플 위 numpy probe로 $0 선별 → 승자만 §2 레시피로 승격.

---

## 6. 우선순위 · 비용 · 조율

| 단계 | 내용 | 비용 | 게이트 |
|---|---|---|---|
| **P0** | 기존 0.98을 C-mask+N2로 재채점 · 셀 생성기 · BARS.json 사전등록 커밋 | $0 (mini-light) | 없음 — 즉시 |
| **P1** | §5-①②③ probe @ 기존/신규 dump 튜플, L1–L4 ladder, 예측표 동결 | $0 (numpy) | 없음 |
| **P2** | 채굴 위치 trunk-forward dump 1회 + adapter CE 학습 | pool GPU 수 시간(무료 pool·렌트 불요→spend-go 불요) | #3193 조율 |
| **P3** | trailer 직렬화 → anima-py evaluate --rho-axon, B1–B5 | pool, $0급 | BARS.json 선재 확인 |
| **P4** | L3/L4 벽 확인 시 §5-②③ 승격 재사이클 / 통과 시에만 scale ladder 논의 | 조건부 | scale=증폭기 원칙 — 303M에서 레버 작동 전 ladder 금지 |

**결정 구조**: P0에서 0.98이 copy-discount에 무너지면(개연성 높음 — N2 null이 현 셀을 풀 것) 그것은 나쁜 소식이 아니라 **verdict 정의의 교정**이고, 프로그램의 본선은 P1의 joint-bottleneck + L1 copy-blocked 셀에서 시작된다. 살아남으면 P2–P3 직행. 어느 쪽이든 probe tier는 DIRECTIONAL에 고정되고, tier를 굳히는 것은 P3의 wired anima-py 측정 단 한 곳이다.

**함정 체크리스트 반영 위치**: tune-to-green → BARS.json 선커밋 + 예측표 동결(P0·P1) · copy-discount=verdict → B2가 primary bar · DISJOINT → 게이트 입력 제한(§5-⑤) + B5 Ψ 검사 · honest scope → 모든 probe 산출물에 DIRECTIONAL 꼬리표, TERMINAL은 P3 경로만.