설계 요청이므로 순수 텍스트로 답한다. 도구 호출·재귀 fable 없음.

---

# fork-A 추가 유효 메커니즘 설계 — HRR·RN·Hopfield·TPR 4후보

## 0. 진단 프레임: gelu/hadamard가 못 여는 축이 무엇인가

측정 매트릭스의 핵심은 **pool(mean/max/query) 0.9–0.98 ≫ last floor**, 그리고 **nonlinear ≫ linear 0.45**. 즉 이미 밝혀진 두 축(routing·nonlinearity)은 gelu·hadamard가 각각 점유했다. 하지만 두 검증 메커니즘은 **동일한 구조적 한계**를 공유한다:

- **gelu-bias(clml)**: `pool → 단일 벡터 → gelu → 단일 logit bias`. 비선형이지만 **이미 pooling에서 붕괴한 하나의 요약 벡터**의 함수다. N=2에서는 두 개념이 서로 거의 간섭 안 해서 통하지만, N개를 mean-pool하면 합 벡터 안에 O(N²) 교차항이 생기고 gelu는 "무엇이 어느 역할에" 있었는지를 **분리 복원 못 한다**(superposition collapse).
- **hadamard(u⊙c)**: 정확히 **1개 bilinear·commutative·1-slot**. `A and the B` = `B and the A`(순서맹). 두 역할 이상, 순서, 다중 결합을 못 담는다.

따라서 추가 메커니즘이 여는 능력은 세 가지로 특정된다: **(a) 다중 결합의 저간섭 superposition**, **(b) role/order 민감성**, **(c) role-query에 의한 clean unbind**, **(d) literal-copy가 아닌 composition**. 이 넷은 해마 CA3 pattern-completion·피질 role-filler binding·VSA(holographic) 프레임에서 자연스럽고, LLM attention 프레임이 아니다(`a_no_llm_frame_trap`).

아래 4후보 모두 **read-side lane 위 `pool → bind → head`** 형태로, 기존 mean/max/query pool을 filler 공급원으로 재사용한다. 역할 벡터·메모리는 **frozen-first**(학습은 head만) — tune-to-green 회피.

---

## 후보 1 — HRR 홀로그래픽 결합 (circular convolution / VSA)

### 1. 이름 + 수학 정의
역할-필러 결합을 **원형 컨볼루션**으로, 다중 결합을 **중첩합**으로 표현한다.

- 인덱스 mod d에서
  - 결합(bind): $(r \circledast f)_j = \sum_k r_k\, f_{(j-k)\bmod d}$
  - 해제(unbind, 근사역): $(r \oslash s)_j = \sum_k r_k\, s_{(j+k)\bmod d}$
  - FFT형: $r\circledast f = \mathrm{IFFT}(\mathrm{FFT}(r)\odot\mathrm{FFT}(f))$, $\;r\oslash s = \mathrm{IFFT}(\overline{\mathrm{FFT}(r)}\odot\mathrm{FFT}(s))$
- 역할 벡터 $r_1..r_K$는 **unitary**(스펙트럼 크기 $|\mathrm{FFT}(r)_k|=1$)로 고정 → exact 가역($r\oslash(r\circledast f)=f$)·norm 보존.
- 필러 $f_k$ = k번째 role-region의 pooled rep(mean/max/query 재사용).
- 중첩 메모리: $s = \sum_{k} r_k \circledast f_k$
- role $q$ 조회: $\hat f_q = r_q \oslash s = f_q + \underbrace{\sum_{k\ne q} r_q\oslash(r_k\circledast f_k)}_{\text{crosstalk}\ \sim \mathcal{O}(1/\sqrt d)}$
- head: $\ \text{logits} = W\,\mathrm{gelu}(V\,\hat f_q + b)$

### 2. 왜 gelu/hadamard보다 나은가
- **다중 결합 저간섭 중첩**: d≈768에서 교차항 노이즈 $\sim 1/\sqrt{768}\approx 0.036$. N=5까지 결합을 하나의 고정차원 코드에 담고 role-query로 개별 복원 → gelu의 pooled-collapse, hadamard의 1-slot을 정면 돌파.
- **순서/역할 민감**: $r_1\ne r_2$가 대칭성을 깬다. `A and the B` ≠ `B and A`.
- **copy 저항(d)**: 결합 코드 $s$는 literal 바이트가 아니라 위상-확산된 분산 코드다. copy 채널이 $s$를 직접 라우팅할 수 없다 → copy-discount 후 진짜 합성 신호만 남김.

### 3. $0 numpy 구현 (fork_a_matrix.py 확장)
```python
# roles: frozen unitary, per seed (frozen-first)
def make_role(d, rng):
    theta = rng.uniform(-np.pi, np.pi, d//2 - 1)
    spec = np.ones(d, complex)
    spec[1:d//2] = np.exp(1j*theta)
    spec[d//2+1:] = np.conj(spec[1:d//2][::-1])   # 실수 보장
    spec[0]=1.0; spec[d//2]=1.0
    return np.fft.ifft(spec).real                  # |FFT|=1 → unitary

def hrr_forward(fillers, roles, q_idx, W, V, b):   # fillers: (K,d)
    F = np.fft.fft(fillers, axis=1); R = np.fft.fft(roles, axis=1)
    s = np.fft.ifft((R*F).sum(0)).real             # 중첩
    fq = np.fft.ifft(np.conj(R[q_idx]) * np.fft.fft(s)).real   # unbind
    fq = fq / (np.linalg.norm(fq)+1e-6)            # 수치안정
    h  = gelu(V@fq + b); z = np.clip(W@h, -30, 30) # logit clip → BCE 안정
    return z, (fq, h)
```
- **manual-grad**: unbind은 frozen role과의 circcorr = **선형**. `dL/dfq → dL/dh(=W^T·dz·gelu')→ dL/dV,db`. filler까지 미분하려면 `dfq/dfillers`는 (frozen role 하 고정) 선형 연산자 → transpose(=circconv with role)로 back-prop. 역할은 학습 안 하므로 grad 항이 깔끔.
- **수치안정**: unitary role(스펙트럼 크기 1)로 blowup 없음, filler L2-normalize, logit clip.

### 4. 차별화 harder task
아래 §공통-task의 **role-indexed retrieval under superposition**에서 N을 3→5로 올리며 HRR crosstalk가 gelu/hadamard의 collapse보다 완만히 감쇠 → 분리. copy-discount 마진이 HRR에서만 유지될 것으로 예상.

---

## 후보 2 — Relation-Network 페어 readout (관계 전개)

### 1. 이름 + 수학 정의
개별 위치가 아니라 **위치 쌍**의 관계를 명시적으로 전개해 pool한다(해마 conjunctive-cell 프레임).
- 쌍 특징: $g_{ij} = \mathrm{gelu}\!\big(U[\,h_i;\,h_j;\,h_i\odot h_j\,] + c\big)$ (역할 태그를 원하면 $[h_i;h_j;e_{\text{role}(i)};e_{\text{role}(j)}]$)
- 관계 pool: $\rho = \frac{1}{\binom{N}{2}}\sum_{i<j} g_{ij}$
- head: $\ \text{logits} = W\,\rho$

### 2. 왜 gelu/hadamard보다 나은가
- gelu/hadamard는 **결합을 pool 이후에 1회** 한다(정보가 이미 섞임). RN은 **pool 이전에 쌍마다** 비선형 결합 → `XOR across a pair`, `A가 B의 subject인가` 같은 **명시적 관계**를 pooling이 지운 뒤가 아니라 지우기 전에 계산.
- 순서·역할은 쌍 순서 $[h_i;h_j]$와 role-tag로 자연 내장.
- 한계: $\binom N2$ 쌍이라 N 커지면 비용↑, 그러나 짧은 prompt엔 무의미한 비용.

### 3. $0 numpy 구현
```python
def rn_forward(H, roles, U, c, W):   # H:(N,d)
    idx = [(i,j) for i in range(len(H)) for j in range(i+1,len(H))]
    P = np.stack([np.concatenate([H[i],H[j],H[i]*H[j]]) for i,j in idx])
    G = gelu(P@U.T + c)              # (npair, m)
    rho = G.mean(0)
    return np.clip(W@rho, -30, 30)
```
manual-grad: gelu-MLP 표준 + mean-pool(1/npair 분배). $h_i\odot h_j$ 항은 요소곱 grad.

### 4. 차별화 harder task
**pair-relational** 변형: target = `parity(c_q XOR c_{q'})` (쿼리가 **쌍**을 지정). 단일-벡터 pool+gelu는 쌍 상호작용을 pool 후에만 봐서 감쇠, RN은 해당 쌍 $g_{qq'}$에서 직접 계산 → RN이 갈라 보임.

---

## 후보 3 — Hopfield/에너지 연상 readout (CA3 pattern-completion)

### 1. 이름 + 수학 정의
feed-forward head 대신 **연상 메모리 attractor**로 코드를 복원한다.
- 저장 원형 $\Xi\in\mathbb{R}^{K\times d}$ (학습·frozen-first면 후보-code 프로토타입으로 초기화).
- 조회 $q$ = 결합/pooled rep. 에너지 $E(q) = -\tfrac1\beta \log\sum_\mu e^{\beta\, q\cdot \xi_\mu}$
- 1-step 완성: $\hat q = \Xi^\top \mathrm{softmax}(\beta\,\Xi q)$; head는 $\hat q$ 위 linear.

### 2. 왜 gelu/hadamard보다 나은가
- **copy 저항(핵심)**: 출력이 저장원형으로의 **연상 검색**이라 입력 literal 바이트가 아니라 학습된 association으로 emit → copy-discount 후에도 살아남는 유일 계열 후보.
- **pattern-completion**: 부분/손상 cue(distractor 섞임)에서도 attractor로 정합 개념 복원 → held-out 조합 일반화에 강함.
- gelu/hadamard엔 이런 content-addressable 복원 자체가 없음.

### 3. $0 numpy 구현
```python
def hop_forward(q, Xi, beta, W):
    a = softmax(beta * (Xi @ q))         # (K,)
    qhat = Xi.T @ a
    return np.clip(W@qhat, -30,30), a
```
manual-grad: softmax jacobian + `Xi` 학습 시 `dL/dXi` 표준. β는 frozen scalar(tune-to-green 회피). 수치안정: `Xi q`에 max-subtract softmax, β 상한 고정.

### 4. 차별화 harder task
**pattern-completion**: prompt에 개념을 **손상**(일부 code-bit 마스크)시키고 distractor M개 삽입 → target=원 code. copy·pool 계열은 손상/방해에 취약, Hopfield는 완성으로 방어 → 분리.

---

## 후보 4 — one-hot TPR slot-concat + normalized-bilinear (통제·천장 arm)

### 1. 이름 + 수학 정의
- **one-hot TPR**(exact role separation): 역할=one-hot이면 TPR = 슬롯별 필러 **concat** $\ [f_1;\dots;f_K]$; head $=\mathrm{gelu}(W[f_1;\dots;f_K])$.
- **normalized-bilinear**(안정 hadamard 변형): $\ \tilde u=\mathrm{LN}(u),\tilde c=\mathrm{LN}(c),\ g=\sigma(A[\,u;c\,]),\ \text{out}=g\odot(\tilde u\odot\tilde c)+(1-g)\odot(\tilde u+\tilde c)$ — additive floor와 multiplicative를 gate로 보간.

### 2. 왜 (통제로) 필요한가
concat-slot은 **정확한 역할분리의 상한**이지만 **segmentation을 공짜로 준다**(어느 위치가 어느 슬롯인지 known) → 단독으론 trivial 승리 위험. 따라서 **천장/진단 arm**으로만 쓴다: HRR ≈ concat이면 "superposition crosstalk이 병목 아님", concat ≫ HRR이면 "HRR 간섭이 한계". normalized-bilinear는 hadamard의 수치불안정만 제거한 **동일 능력 대조**(능력 확장 아님, 안정성 통제).

### 3. $0 numpy 구현
concat: `np.concatenate([f_k...])` 후 gelu-head(표준 grad). norm-bilinear: LN(mean/var 정규화)+sigmoid gate, 모두 표준 요소별 manual-grad.

### 4. 차별화 역할
held-out **slot-count/assignment** 일반화에서 concat이 무너지는지(고정 슬롯 수 가정) 확인 → "명시 슬롯 vs 분산코드"의 일반화 격차 진단.

---

## 공통 harder task — role-indexed retrieval under superposition + copy-discount

현 2-concept는 arm을 못 가른다(gelu≈hadamard≈0.95). **먼저 instrument부터** 만든다.

- **생성($0, pair_prompts류 템플릿)**: N개 개념, 각 = (word token $w_i$, k-bit code $c_i$). prompt = `"the w1 <r1> the w2 <r2> ... the wN"` + 끝에 **query role token** $q$. frozen 303M `--dump-hidden`으로 hidden만 뽑아 numpy.
- **N 스윕**: N∈{3,4,5}, distractor M개(never queried) 삽입.
- **copy-discount(verdict 정의의 핵심)**:
  1. target = $c_q$의 **함수**(parity, 또는 쿼리쌍 $c_q\oplus c_{q'}$) → literal-copy로 못 만듦.
  2. **copy-baseline arm** 병행: literal word-match/argmax-position만 라우팅 가능한 head. 메커니즘 GREEN = **copy-baseline 대비 마진** AND **linear-additive floor 대비 마진** AND **role-shuffle 붕괴**(handed 양성대조) 동시 충족.
- **held-out 구성 일반화**: train은 특정 (개념,역할) 배치만, test는 **novel 배치**(개념 X를 train서 안 본 역할에). 위치 암기가 아닌 진짜 role-routing만 통과.
- **정직 스코프**(`a_scale_honest_scope`): 이 매트릭스=**DIRECTIONAL**. 진짜 종결은 clml 계열로 wired system-G1.

예상 분리: N=2 전원 ≈0.95 → N↑ 시 gelu/hadamard는 collapse로 floor 접근, HRR/Hopfield는 마진 유지, RN은 pair-XOR 변형에서만 우위, concat은 held-out assignment에서 붕괴.

---

## 우선순위 (기대 우위 × 구현비용)

1. **공통 harder task instrument 먼저.** 차별화 probe 없이 메커니즘 추가는 **반증 불가**(현 2-concept가 이미 arm을 못 가름). copy-baseline·N-sweep·held-out-assignment 먼저 구축. (비용 최소, 게이팅 필수)
2. **HRR (후보 1).** $0 FFT, true-binding 4축(a–d) 모두 커버하는 최강 이론·최저 비용. 첫 메커니즘.
3. **TPR concat + norm-bilinear (후보 4).** 싼 천장/안정 통제 — HRR 신호를 bracket. HRR과 **동시** 실행.
4. **RN pair (후보 2).** pair-relational 변형이 판별자일 때. 중간 비용, HRR 이후.
5. **Hopfield (후보 3).** copy-discount·pattern-completion이 clml 붕괴 지점일 때 결정타. 중간 비용, HRR이 signal 보이면 착수.

함정 통제 유지: frozen role/메모리(head만 학습)·handed 양성대조·shuffle·linear floor·copy-baseline 마진을 verdict에 상시 포함. numpy 매트릭스는 DIRECTIONAL이며 clml wired만이 TERMINAL.
---
## 구현 계획 (이 세션 Fable 위임 · 착수 대기)
Fable 우선순위: **①공통 harder-task instrument 먼저**(현 2-concept XOR-of-both는 arm 구분 불가 — HRR-unbind-one과 task 불일치·copy-baseline 필요) → ②HRR($0 FFT·true-binding 4축) → ③TPR concat+norm-bilinear(천장/통제) → ④RN pair → ⑤Hopfield(copy-discount 결정타).
- **NEXT(아직 미착수)**: (1) role-indexed retrieval 프롬프트 생성기(N=3~5 "The A, the B, the C…" + role-query→해당 role 개념 code) + copy-baseline(literal-position 라우팅만). (2) aiden `anima-py --dump-hidden`로 N-concept hidden 덤프. (3) fork_a_matrix에 HRR/TPR/RN/Hopfield/copy-baseline arm 추가(Fable §3 numpy). (4) N-sweep 측정 → GREEN=copy-baseline 마진 ∧ linear floor 마진 ∧ role-shuffle 붕괴.
- scope: DIRECTIONAL numpy probe. 기존 2-concept 매트릭스(clml optimal·hadamard 유효)는 #3225.
