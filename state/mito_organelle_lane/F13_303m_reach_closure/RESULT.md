# H_9285 — 절대-setpoint capacity schedule × 303M reach 결착 · 결과

**verdict: 🟥 INVALID (사전등록 V-gate 2개 동시 FAIL) — lane KILL 을 찍지 **않는다**.**
헤드라인 detector 가 죽어 있는 상태에서 나온 Δ≈0 은 "효과 없음"과 "탐지 불가"를 구분하지 못한다.
(단, 사후 live 하위-detector 에서는 처치가 **엄격히 열화**시키는 방향 — H_9283 예측과 일치.)

- 호스트: pool `aiden` (12c/30G, CPU numpy — cupy 미설치) · **학습 0 · GPU 학습비 0 · wall 2941s**
- ckpt: `~/py303_full.clm` → **d=3784 · E=3 · K=3 · L=4 · V=256 · T=24-byte window**
- 엔진: worktree HEAD `core/decode.py`(py 2-production) 프로덕션 forward 그대로
- **PARITY GATE: max|Δ| = 0.0** — split-trunk + dense-mix 재구성이 프로덕션 `_fwd_logits` 와 byte-exact ⇒ engine-native
- 산출: `run.py` · `analyze.py` · `result.json`(item×arm 전량) · `analysis.json`

---

## 0. 측정 전에 드러난 구조적 사실 (카드 전제의 정정)

1. **프로덕션 CLM 에는 expert top-k / capacity 자체가 없다.** router 는
   `nn_moe_router_fwd`: `y[t,c] = Σ_e p[t,e]·ex[e,t,c]` — **E개 전문가 전부를 쓰는 dense soft mixture**.
   카드의 "프로덕션 고정 top-k(c0)" 는 사실과 다르다. ⇒ **c0 = dense = k=E**, 그리고
   **어떤 capacity schedule 도 dense mixture 에서 정보를 '버리는' 연산**이다(상한이 c0).
2. 실제로 **상수 k grid 전수 결과 최선값 = k=3(=dense=c0)**: k1 −0.516 · k2 −0.470 · **k3(c0) −0.422**.
   즉 c1(best constant) 는 c0 와 동일 arm 으로 수렴한다. truncation 은 단조 열화.
3. final GroupNorm(G=1) 이 `[T,C]` 전체를 정규화 ⇒ k_t 는 전 위치 logits 에 결합(닫힌형 oracle 불가 → greedy oracle 사용).

## 1. 사전 MDE (본 측정 전 · pilot 4블록) — **통과**

| 항목 | 값 |
|---|---|
| MDE(α=.05, n=20 blocks, paired) | **0.170** |
| 축 동적범위(greedy per-position oracle 상승폭, k축) | **+4.448** |
| 축 전체 진폭 (oracle hi − lo) | 9.220 |
| **mde_ok** | ✅ **True** (0.170 ≪ 4.448) |

⇒ **검출력은 병목이 아니었다.** k축은 detector 를 움직일 여지가 충분했고(치팅 oracle 기준),
MDE 는 그 범위의 1/26 수준이었다.

## 2. 정보 채널 증명 — **통과 (항진적 arm 아님)**

- (a) 결정변수 = **위치 t 의 누적 router mass**(`softmax(router conv logits)` → 내림차순 누적).
  `k_t = min{k : Σ_{i≤k} p_sorted[t,i] ≥ θ}` — **입력 토큰의 함수**이며 상수 arm(c1)이 구조적으로 볼 수 없다.
- (b) θ(절대 setpoint)=**0.4636** = corpus probe set(576 위치, detector item 을 **한 번도 보지 않음**)의 top-1 mass 중앙값.
  ⇒ tune-to-green 불가 (θ 가 detector 를 못 봄).
- (b) 실측 분산: k_t 히스토그램 **{1: 21121, 2: 7679, 3: 0}** · k̄=1.267 · **Var(k_t)=0.196**
  · 시퀀스 내부 평균 분산 0.187 · **분산 0인 시퀀스 = 0.17%** ⇒ 배분기는 입력마다 실제로 변동한다.
  c1 상수 arm 의 k-분포(점질량)와 겹치지 않는다.

## 3. 사전등록 헤드라인 = `m_conj` (held-out 2-cue 결합 마진) — **V-gate 2개 FAIL**

detector: held-out 쌍(A,B) — corpus 24B 윈도우 안에서 **한 번도 같이 나온 적 없는** 조합.
`lift(x|ctx) = logP(x|ctx) − logP(x|null)`, null = 두 cue 를 **바이트 스크램블**한 동일 길이 비단어 컨텍스트
(길이·거리 confound 0, 오직 cue 의 '정체'만 다름). `m_conj = min(m_A_conj, m_B_conj)` (둘 다 살아야 결합).

| V-gate | 값 (n=20 blocks, paired) | 판정 |
|---|---|---|
| **liveness**: 단일-cue ceiling=min(s_A,s_B) | **−0.543 ± 0.078 (t=−6.94)** | 🟥 **FAIL** |
| ├ s_B (근접 cue 단독) | **+1.075 ± 0.238 (t=+4.52, p=6e−6)** | ✅ 살아있음 |
| └ s_A (원거리 cue 단독, 비단어 1개 건너) | **−0.033 ± 0.035 (t=−0.95, p=0.34)** | 🟥 **죽어있음** |
| **channel visibility**: SHOCK(router 완전 파괴=균등 전문가) vs c0 | **+0.011 ± 0.035 (t=+0.32, p=0.75)** | 🟥 **FAIL** |
| (참고) k=1 최대 truncation vs c0 | −0.094 ± 0.122 (t=−0.77, p=0.44) | ns |

> **왜 INVALID 인가**: (1) 헤드라인의 두 branch 중 **원거리 branch 가 처치 이전, 통제 조건에서 이미 0**이다
> — 경쟁 cue 도 없고 개입 토큰이 무의미 스크램블인데도 원거리 cue 는 **전혀 소비되지 않는다**.
> 결합(conjunction)을 묻기도 전에 채널이 없다. (2) router mixing 을 **완전히 파괴해도** 헤드라인이 안 움직인다
> ⇒ 이 detector 는 처치의 채널(MoE mixing)을 **볼 수 없다**. 이런 detector 위의 Δ≈0 은
> "효과 없음"과 "탐지 불가"를 구분하지 못한다 ⇒ **KILL 로 승격 금지**(카드 §0-5 · 앞선 7/11 뒤집힘의 재발 방지).

### 3-1. 그럼에도 사전등록 arm 수치는 전부 보고한다 (판정 근거로는 쓰지 않음)

| arm | m_conj (mean ± SEM, n=20) | D-acc |
|---|---|---|
| **c0** (프로덕션 dense) | **−0.422 ± 0.218** | 0.433 |
| **c1** best-constant (= grid 전수 → **k=3=c0** 선택) | −0.422 ± 0.218 | 0.433 |
| c1_k1 / c1_k2 (grid) | −0.516 ± 0.215 / −0.470 ± 0.200 | 0.367 / 0.358 |
| **EXP** (절대-setpoint schedule) | **−0.504 ± 0.207** | 0.425 |
| **c2** shuffled-schedule (동일 k 다중집합) | −0.516 ± 0.220 | 0.392 |
| SHOCK (균등 전문가) | −0.411 ± 0.223 | 0.425 |

**control 별 paired-t (max(controls) 금지 · 전부 보고)**
- EXP − c0        = **−0.082 ± 0.074**, t=−1.11, p=0.27
- EXP − c1(best)  = **−0.082 ± 0.074**, t=−1.11, p=0.27  (c1 이 c0 로 수렴)
- EXP − c2_shuf   = **+0.012 ± 0.104**, t=+0.12, p=0.91
- EXP − pooled-mean(controls) = **−0.051 ± 0.066**, t=−0.77, p=0.44
- (2차) D-acc: EXP − c0 = −0.008 ± 0.037, t=−0.22, p=0.82

⇒ 사전 예측대로 **어느 control 대비도 상승 신호 0**. 단, 위 V-gate 실패 때문에 이 null 은 **결착 근거가 못 된다**.

## 4. 사후(POST-HOC) — **살아있는** 하위 detector 위에서의 처치 효과

헤드라인의 근접 branch `m_B_conj` 는 c0 에서 **+1.083 ± 0.231 (t=+4.69, p=3e−6)** — 확실히 살아있고
MDE 0.190 ≪ 동적범위 1.083 ⇒ **검출력 있음**. 이 위에서 arm 들을 다시 재본다(사후·헤드라인 아님):

| 비교 | Δ ± SEM | t | p |
|---|---|---|---|
| **EXP − c0** | **−0.209 ± 0.091** | **−2.30** | **0.021** |
| EXP − c2_shuf | −0.056 (EXP −0.209 vs c2 −0.153) | — | ns |
| EXP − pooled-mean(controls) | −0.098 ± 0.051 | −1.90 | 0.057 |
| c1_k2 − c0 | −0.142 ± 0.044 | −3.20 | 0.001 |
| c1_k1 − c0 | −0.150 ± 0.129 | −1.16 | 0.245 |
| c2_shuf − c0 | −0.153 ± 0.117 | −1.31 | 0.190 |
| SHOCK − c0 | **+0.100 ± 0.040** | +2.48 | 0.013 |

**읽기**: 작동하는 detector 위에서 **모든 capacity truncation 은 열화**이고, **EXP 가 그 중 가장 나쁘다**.
EXP 는 **자기 자신의 시간축 셔플(c2)조차 이기지 못한다** ⇒ 배분기의 '정렬(schedule)' 자체에 정보가 없다.
게다가 router mixing 을 파괴한 SHOCK 가 오히려 **살짝 개선**(+0.100, p=0.013) ⇒ **학습된 router mixing 은
read-side cue→content 소비를 나르는 축이 아니다**. 방향은 전부 음성 — reach lift 의 흔적이 전혀 없다.
(사후 분석이므로 tier 는 DIRECTIONAL 이 최대. 이걸로 lane 을 cement 하지 않는다.)

## 5. 부수 발견 (arm 무관 · 高검출력 · engine-native)

**303M read-side 에는 살아있는 cue 슬롯이 하나뿐이다.**
근접 cue 는 소비되고(+1.075, t=+4.5), **원거리 cue 는 경쟁자가 없어도 전혀 소비되지 않는다(−0.033 ± 0.035, ns)**.
개입 토큰이 의미 없는 스크램블이어서 거리/길이 confound 가 0인데도 그렇다.
⇒ 저장소의 기존 벽(`best_distinct=1` · "concept→content 연상이 causally 소비불가" · depth-RF H_1584)의
**독립적·연속량 재확인**이며, 동시에 **2-cue 결합형 detector 는 이 substrate 위에서 구조적으로 바닥**임을 뜻한다
(결합 실패 때문이 아니라 원거리 채널 자체가 없어서).

## 6. 결론 / 다음

- **H_9285 는 판정 불가(INVALID)** — 인프라 문제가 아니라 **detector-substrate 부적합**(사전등록 V-gate 로 자가검출).
  organelle lane 을 이 카드로 **CLOSED 로 찍지 않는다**(거짓 null 방지).
- 다만 회수된 정보는 전부 lane-closure 방향: (i) 프로덕션에 capacity 축이 아예 없고 dense 가 최적,
  (ii) 살아있는 detector 위에서 setpoint schedule 은 **엄격히 열화**하며 자기 셔플도 못 이기고,
  (iii) router mixing 파괴가 오히려 개선 ⇒ **배분(allocation)은 read-side 축이 아니다**(H_9283 예측과 일치).
- **이 프로브 클래스의 재발사는 무의미**: 원거리 cue 채널이 죽어 있는 한 어떤 2-cue reach detector 도
  eval-only 로는 바닥이다. deep-L8(L=8, RF↑) 변형이 유일한 변수지만 H_1584 가 이미 `best_distinct=1 = L4` 로 floor 확인.
- 유효한 exit 은 여전히 **학습 measure 교체**(H_9267 XBIND 계열)뿐 — capacity/allocation 축이 아니다.

## 재현
```bash
# aiden (pool)
ANIMA_CORE=<HEAD core/> CKPT=~/py303_full.clm CORPUS_DIR=~/anima_train_corpus python3 run.py
python3 analyze.py     # result.json → analysis.json (V-gate + 사후 live-branch)
```
