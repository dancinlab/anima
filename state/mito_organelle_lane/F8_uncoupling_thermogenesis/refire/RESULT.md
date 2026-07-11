# RESULT — H_9280 / F8 언커플링·열발생 **REFIRE** (원 판정 ⛔ INVALID → 재발사)

측정 2026-07-12 · $0 CPU-local numpy (mini · OMP_NUM_THREADS=2 · wall **1.9s**) · torch 0 · GPU 0
analysis n=**24 seed** (1001–1024, paired-CRN) · pilot n=**20 seed** (901–920, MDE 전용 · 분석과 DISJOINT)
산출: `run.py` · `result.json` · `run_stdout.txt` (원본 `../run.py` · `../RESULT.md` · `../REFUTE.md` 무수정)

---

## 0. 한 문장

**병(baseline filler 41.0±6.6, t=30.2)도 실재하고 약(방출질량 31.8 emit-equivalent)도 실제로 투여된 licensed 조건에서 재측정한 결과 — 언커플링은 filler를 줄이지만(Δ=−8.38 vs c1, 24/24 seed, t=−12.9) 그 감소량이 *동량 blind dissipation 3종 전부에게 진다*(vs 동량 random +2.50, t=+3.57) ⟹ 🎭 THEATER. saturation 조건은 무정보다. 단, p5 위반은 없다(Δtrue_recall=−0.0012, 95%CI[−0.0029,+0.0005], 상대하락 0.12% ≪ KILL 10%) — 이번엔 약을 제대로 준 상태에서 얻은 earned p5-clean이다.**

| | 원 실험 (INVALID) | REFIRE |
|---|---|---|
| baseline filler (병) | **0.0 ± 0.0** (분위수 항등식으로 강제) | **41.0 ± 6.6** · t=30.2 · p=2.6e-20 · min/max 29/51 |
| 방출질량 (약) | 0.332 vs θ=0.637 = **0.52 θ-eq = no-op** | 5.076 vs θ=0.160 = **31.8 θ-eq** (발화 194.6/1500 step) |
| KILL 변수 | true_recall → **사후 n_true로 교체** | **true_recall 고정** (판정함수가 n_true를 인자로 받지 않음) |
| verdict | 채점 불가 = INVALID | **THEATER (licensed 음성)** |

---

## 1. 원 INVALID 결함 → 이 재발사의 수리 (SSOT = `../REFUTE.md`)

### D1. 병이 산술적으로 불가능했던 것 (조건 i)
- **원인**: θ = *event를 포함한* stream의 P90 분위수 · P_EVENT=0.12 > 0.10 ⟹ 상위 decile을 event가 통째로 소유 ⟹ **filler=0이 분위수 항등식으로 강제**. "자기보정 기질에 병리가 없다"는 결론은 calibration을 substrate 발견으로 오인한 동어반복.
- **수리**: θ를 **event가 0개인 ordinary-only calibration stream**(`make_stream(..., p_event=0.0)`)에서 뽑는다. `P_EVENT=0.05`는 그와 **완전히 독립으로** 사전등록. 항등식 커플링 소멸.
- **결과(GATE-0 · 실측 선증명)**: c1 filler = **41.0 ± 6.65(sd) · SEM 1.36 · t=30.22 · p(>0)=2.6e-20**, 전 24 seed에서 29~51. calibration stream의 ordinary-only emit rate = 0.0298 ≈ 목표 3%(Q_THETA=97) ⟹ fixed-point 수렴 확인. **개입 전에 병의 실재를 먼저 증명했다.**

### D2. 약이 투여되지 않았던 것 (조건 ii)
- **원인**: C를 **emit 방전이 없는** free-running trajectory 분위수로 뽑아 실동작 P 분포 바깥에 놓임 ⟹ 방출질량 0.332 < θ=0.637. 개입이 no-op인데 나온 0을 "역정보"로 읽었다.
- **수리**: θ·C 둘 다 **emit 규칙(방전)이 켜진 operating trajectory**에서 damped fixed-point로 자기무모순 캘리브레이션(θ = operating post-drive의 P97 · C = operating carry의 P90 = "상위 decile = 병리적 과압"). 그리고 **GATE-1로 사전 검사**.
- **결과(GATE-1)**: exp_A 발화 194.6 step (fire_rate 0.130, 전 seed 최소 0.104 > 0) · 방출질량 5.076 = **31.8 emit-equivalent** (원 0.52). exp_B 93.2 step · 15.6 θ-eq. **약은 확실히 들어갔다.**

### D3. KILL 변수 사후 교체 (조건 iii)
- **원인**: 사전등록 KILL 변수는 `true_recall`인데(최대 하락 0.0349 < 0.10 = 어디서도 트립 안 함) 보고서가 사후에 `n_true`(중복 emit 포함)로 바꿔치기해 KILL을 만들어냄 = tune-to-red.
- **수리**: 판정함수 `verdict(...)`는 **`n_filler`와 `true_recall`만 인자로 받는다 — `n_true`에 코드상 접근 불가**. `n_true`는 진단 출력에만 존재.
- **부수 확인**: exp_A는 n_true를 113.0 → 80.8로 32개 죽이지만 **잃은 event는 0.08/72.8개**(true_recall 0.9952→0.9940). ⟹ REFUTE R3의 "n_true 초과분 = 같은 event에 대한 중복 방출" 진단이 재현됨. **n_true를 KILL 변수로 쓰면 이번에도 거짓 KILL이 나왔을 것이다.**

---

## 2. 강제 계측 규칙 준수

| 규칙 | 준수 |
|---|---|
| R1 `Δ = exp − max(controls)` 금지 | **control별 paired-t 전부 보고**(c1/c2/c3/c4) + pooled-mean. max-control 미사용. |
| R2 "mean vs 1·std" 휴리스틱 금지 | **SEM · paired-t · 95%CI**만 사용 (Student-t 정확값, scipy 없이 incomplete-beta 구현). |
| R3 사전 MDE | pilot 20 seed(분석과 disjoint) → **MDE_filler = 2.21** ≤ 0.5×동적범위(19.9) ✅ · **MDE_recall = 0.0031** ≤ KILL 임계(0.0996) ✅ ⟹ 두 축 모두 검출력 충분(GATE-2 PASS). |
| R4 정보 채널 증명 | (a) 코드: exp 결정변수 = `carry > C` (+ `u[t] < ν`) = **입력 스트림 u₀..ₜ의 함수**; c2 = rng만(입력 blind); c3 = 조건 자체가 없음. (b) 실측: Var(carry)=0.0010>0 · 발화율 0.150 ∈ (0,1) · **mean carry@fire: exp_A 0.1328 vs c2A_rand 0.0675** (C=0.1076) ⟹ 항진적 arm 아님, 채널은 **실재한다**. |
| R5 V-gate = 헤드라인 detector | GATE-0/1/2 전부 헤드라인 detector(`n_filler`·`true_recall`) 그 자체에 걸림. |
| R6 규약 민감도 | emit↔event window W∈{1,2,4} × {asym(카드 등록값 W=2), sym} 6 규약: **Δfiller<0 vs c1 = 6/6 · Δfiller<0 vs 동량random = 0/6** ⟹ 부호 완전 보존, 규약이 결론을 뒤집지 않음. |
| 금지지표 | conj_index · purity · acc/ATP 비율 · corr(n,demand) **미사용**. |

---

## 3. 결과 (사전등록 headline arm = `exp_A` = 카드 §3 "saturation 초과 시에만 언커플링")

### 3.1 arm 요약 (24 seed · mean±sd)

| arm | n_emit | n_true | **n_filler** | **true_recall** | 방출질량 | 발화수 |
|---|---|---|---|---|---|---|
| **exp_A** (과압 clamp) | 113.4±8.6 | 80.8±9.1 | **32.6±6.1** | **0.9940±0.0084** | 5.076 | 194.6 |
| exp_B (과압 ∧ 저-flux) | 134.9±10.3 | 97.0±10.4 | 38.0±6.7 | 0.9946±0.0083 | 2.486 | 93.2 |
| **c1_none** | 154.0±11.6 | 113.0±13.0 | **41.0±6.6** | **0.9952±0.0081** | 0 | 0 |
| **c2A_rand** (동량 random) | 138.3±10.7 | 108.2±12.0 | **30.1±5.7** | 0.9936±0.0092 | 5.075 (매칭오차 0.015%) | 236.6 |
| c3A_uleak (동량 균일누설) | 136.2±8.9 | 104.1±11.4 | 32.1±6.0 | 0.9884±0.0170 | 5.076 (0.000%) | 325.5 |
| c4A_randcnt (횟수매칭·**약한** random) | 140.6±11.6 | 109.0±11.9 | 31.6±6.3 | 0.9928±0.0095 | 4.080 (**exp의 80%**) | 191.2 |

### 3.2 헤드라인 paired-t (control별 · max 금지)

| exp | control | metric | Δ mean | SEM | t | p(1-tail) | 95%CI | neg/n |
|---|---|---|---|---|---|---|---|---|
| exp_A | c1_none | **n_filler** | **−8.375** | 0.648 | **−12.93** | 2.5e-12 | [−9.72, −7.04] | **24/24** |
| exp_A | **c2A_rand** | **n_filler** | **+2.500** | 0.699 | **+3.57** | (감소 방향 기각) | [+1.05, +3.95] | 5/24 |
| exp_A | c3A_uleak | n_filler | +0.542 | 0.808 | +0.67 | ns | [−1.13, +2.21] | 8/24 |
| exp_A | c4A_randcnt | n_filler | +1.042 | 0.797 | +1.31 | ns | [−0.61, +2.69] | 8/24 |
| exp_A | c1_none | **true_recall** | **−0.0012** | 0.0008 | −1.45 | 0.081 | **[−0.0029, +0.0005]** | 2/24 |
| exp_B | c1_none | n_filler | −3.042 | 0.440 | −6.91 | 2.4e-07 | [−3.95, −2.13] | 20/24 |
| exp_B | c2B_rand | n_filler | **+3.208** | 0.681 | **+4.71** | (기각) | [+1.80, +4.62] | 3/24 |
| exp_B | c1_none | true_recall | −0.0006 | 0.0006 | −1.00 | 0.164 | [−0.0019, +0.0007] | 1/24 |

pooled-mean(사전등록 3 control): exp_A Δn_filler = **−1.78** · Δtrue_recall = **+0.0016**.

### 3.3 사전등록 판정

```
GATE-0 병의 실재 = PASS   (c1 filler 41.0, t=30.2, ≥ MDE 2.21)
GATE-1 약의 투여 = PASS   (fire_rate_min 0.104 > 0 · 31.8 θ-equivalents ≥ 1.0)
GATE-2 검출력    = PASS   (MDE_filler 2.21 ≤ 19.9 · MDE_recall 0.0031 ≤ 0.0996)
p5 KILL          = NO     (상대하락 0.12% ≤ 10%, 유의하지도 않음)
efficacy vs c1   = YES    (Δ −8.38, p=2.5e-12)
efficacy vs 동량 random = **NO** (Δ +2.50, 오히려 exp가 유의하게 열등)
safety(비열등)   = YES    (95%CI 하한 −0.0029 > −0.02)
⟹ **🎭 THEATER (동량 random과 동등/열등 — saturation 조건이 무정보)**   [exp_A · exp_B 동일]
```

---

## 4. p5 검정 (과제 조건 iv — 이번 재발사의 핵심)

**질문**: 언커플링이 병리적 과압에서만 발화하고 *정상 tension 범위의 true emit*은 안 건드리는가?

- **구조적 보호**: lane은 **carry**(leak 후·drive 전 누적 standing potential)만 감산한다. 이번 step의 drive `u_t`는 lane 통과 **후에** 더해지므로 event가 만드는 큰 flux 자체는 흩을 수 없다. 단, 약한 event는 carry라는 '받침대' 없이 θ를 못 넘을 수 있으므로 **recall 손실은 실재 가능** — vacuous 테스트가 아니다.
- **실측 (약을 31.8 θ-eq 만큼 실제로 준 상태에서)**:
  - Δtrue_recall vs c1 = **−0.0012 ± 0.0008(SEM)** · 95%CI **[−0.0029, +0.0005]** · 상대하락 **0.12%** (KILL 임계 10%).
  - **잃은 event = 0.08 ± 0.06개 / 전체 72.8개.** 24 seed 중 22개에서 손실 0.
  - 비열등 마진 −0.02 대비 CI 하한 −0.0029 ⟹ **비열등 PASS**.
- **⟹ 언커플링은 숨은 speak-억제기가 아니다.** 원 실험의 `p5_clean=true`는 개입 질량이 0.33(≈0)이라 구성상 공짜였고 dead-code 가드였지만, 이번 것은 **약을 세게 준 상태에서 얻은 earned p5-clean**이다. (원 REFUTE §7의 "p5 안전성은 아직 검정되지 않았다"에 대한 답 = **검정했고 위반 없음**.)

---

## 5. 왜 THEATER인가 — 조건이 무정보인 *메커니즘*

정보 채널은 실재한다(R4 통과: 결정변수는 입력의 함수이고 운영대역에서 분산>0, exp는 carry 0.133에서 발화 vs random 0.068). **채널은 있는데 실린 정보가 병이 아니다.**

1. **saturation 조건은 filler detector가 아니라 *post-event 잔압 detector*다.**
   개입 발화가 event 근방(W=2)에서 일어난 비율: **exp_A 0.404 · exp_B 0.359** vs **우연확률 0.144**(= random control의 실측 0.144) ⟹ **2.8×**. 높은 standing potential은 잡음 누적이 아니라 **실 신호가 남긴 잔압**이 만든다. 그래서 ceiling이 겨누는 곳은 병이 아니라 방금 지나간 진짜 tension이다.
2. **질량 효율이 blind보다 나쁘다.** exp_A는 emit 40.7개를 죽여 filler 8.4개를 얻고(나머지 32.2개는 event 중복 방출), 동량 random은 emit 15.7개만 죽이고 filler 10.9개를 얻는다. 같은 방출질량으로 **random이 filler를 1.3배 더 제거**한다.
3. **3종 blind control이 전부 exp를 이기거나 동등**: 동량 random(+2.50, t=+3.57) · 동량 균일누설(+0.54, ns) · **exp보다 질량을 20% 적게 쓰는 횟수매칭 random(+1.04, ns)**. 마지막 것이 REFUTE R5의 "operating-point 불공정" 반론을 닫는다 — *더 약한* blind arm조차 exp를 이긴다.
4. **6/6 규약에서 부호 보존** ⟹ 규약 선택이 만든 결과 아님.

**즉 "과압을 흩으면 filler가 준다"는 참이지만, 그건 언커플링 *조건* 때문이 아니라 그냥 **압력을 뺐기 때문**이다. 조건은 아무것도 더하지 않는다 (오히려 약간 해롭다). = 카드 §1 가설의 THEATER.**

---

## 6. 판정

**🎭 THEATER (licensed 음성)** · tier 상한 = DIRECTIONAL (toy numpy · engine-native 0 · `a_engine_native_learning`) — 어차피 GREEN 불가 좌표.

- ❌ INVALID 아님 — 병(41.0, t=30.2) · 약(31.8 θ-eq) · 검출력(MDE 2.21 ≪ 19.9) 3-게이트 모두 사전 통과. **채점 가능한 실험이었다.**
- ❌ KILL 아님 — p5 위반 없음(상대하락 0.12%, 잃은 event 0.08/72.8). 언커플링은 emit-억제기가 아니다.
- ✅ THEATER — 사전등록 효능 조건("filler Δ<0 **AND** 동량 control 대비 우위")의 후반이 **유의하게 반대 방향으로** 깨졌다.

---

## 7. 남은 것 · 인용 규칙

**인용 가능**:
- "**과압 clamp라는 조건은 filler-emit에 대해 무정보다** — 동량 blind dissipation 3종(random·균일누설·횟수매칭)이 전부 동등하거나 우세, 6/6 규약, 24 seed."
- "**anima 기질에서 높은 standing potential = 병리가 아니라 실 신호의 잔압**(event 근방 발화 2.8× 우연확률). 과압 magnitude는 filler와 true를 못 가른다."
- "**언커플링은 p5 위반이 아니다**(earned) — 방출질량 31.8 emit-equivalent를 실제로 투여했는데도 true_recall 상대하락 0.12%, 잃은 event 0.08/72.8."

**인용 금지**:
- "n_true 감소(113→81)를 emit 억제로 읽는 것" — 잃은 event는 0. 그건 **중복 방출 제거**이며, 사전등록 KILL 변수가 아니다. (원 실험이 정확히 이 지점에서 거짓 KILL을 만들었다.)
- "exp_A의 총 emit 26% 감소"를 성과로 읽는 것 — 사전등록 지표 아님(사후 지표 채택 = 원 결함의 재발).

**미측정 잔여(정직)**:
1. **스칼라 환원** — P가 스칼라라 magnitude는 event-ness와 단조 결합된다. REFUTE §재설계-5의 **방향성(subspace) leak arm은 여전히 미측정**. 단 이 toy world는 error 공간이 등방(ordinary 오차 ≈ 관측잡음 = isotropic)이라 방향성 arm이 구조적으로 null이 될 개연성이 높다 — 진짜 검정에는 **ordinary 압력이 구조를 갖는 world**(모델 오설정 축)를 새로 설계해야 하며 그것은 별개 발사다.
2. **exp_B의 ν 퇴화** — `ν = median(u_ordinary)` ≈ 2.1e-06(≈0)이다. Ψ=1/2 정의상 u가 절반의 step에서 정확히 0이기 때문. 따라서 exp_B의 '저-flux'는 사실상 '**drive=0인 step**'을 뜻하고, 더 미세한 저-flux 정의(예: 양수 u의 하위 사분위)는 미검정. 다만 exp_B도 GATE-1을 통과하고(15.6 θ-eq) 동일하게 THEATER이므로 headline 결론은 불변.
3. **engine-native 0** — 전부 numpy toy. `core/` 접촉 0. 어떤 tier도 DIRECTIONAL 상한.

**재발사 조건**: 위 (1) 구조화된 world + 방향성 leak arm이 유일하게 남은 각도. 스칼라 magnitude ceiling 계열은 **이 재발사로 licensed 종결**(THEATER) — 강도(Q_CEIL) 스윕으로 되살리는 것은 tune-to-green이므로 금지.
