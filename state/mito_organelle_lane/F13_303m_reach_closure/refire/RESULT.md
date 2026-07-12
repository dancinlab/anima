# H_9285 REFIRE — 결과 · **verdict = INVALID** (사전등록 V2 게이트 발화)

**사전등록**: `PREREG.md` (run_refire.py sha256 `7b1d3760…`, 측정 전 동결 · 실행된 스크립트 sha 일치 확인).
**호스트**: pool `aiden` · ckpt `~/py303_full.clm` (d3784·E3·K3·L4·V256·T24) · **PARITY max|Δ| = 0.0** (프로덕션 `_fwd_logits`와 byte-exact) · wall 154s · 인프라 벽 **없음**(BLOCKED 아님).
**데이터**: fresh-cue 130 items — **verdict set 100 (20 blocks × 5) ⊥ MDE pilot 30 (6 blocks × 5)**.
이전 run과 **(A,B) 재조합쌍 overlap = 0 · 5-tuple overlap = 0 · cue 단어 완전 disjoint** (fresh scramble/arm-shuffle/θ seed).

---

## 1. 한 문장 결론

**KILL은 cement되지 않았다 — 오히려 반증됐다.** 사전등록 헤드라인 `m_B_conj`를 **새 disjoint seed**로 재면,
KILL을 licensing했던 유의 음성(EXP−c0 = −0.209, p=.033)이 **부호를 뒤집고 ns가 된다**(+0.129, t=+1.06, p=.29).
V2 채널가시성 게이트도 함께 부호가 뒤집혀 **FAIL** → 사전등록 분기대로 **verdict = INVALID**.
진단 결과 원인은 "detector 맹목"이 아니라 **MoE capacity 채널이 재조합 마진에 부호-무작위 잡음만 주입**하기 때문이다
(항목당 |Δ| = 0.37~0.80인데 signed mean ≈ 0). ⟹ 이전 KILL·이전 V-gate 유의성 둘 다 **seed 특이적 잡음 draw**였다.

## 2. 사전등록 헤드라인 = `m_B_conj` (순서통계량 아님)

원 F13의 헤드라인 `m_conj = min(m_A_conj, m_B_conj)`는 **그 자체가 순서통계량**(규칙①⑤ 위반)이었고,
검증자가 **사후에** live branch `m_B_conj`로 갈아끼워 KILL을 얻었다 — 그 KILL은 directional일 뿐 licensed가 아니었다.
이번 재발사는 `m_B_conj`를 **데이터 보기 전에** 헤드라인으로 못박고 **새 데이터**로 쟀다.

## 3. arm 표 — 헤드라인 `m_B_conj` (verdict set 100 items · 20 blocks · paired-CRN)

| arm | mean ± SEM | D-acc |
|---|---|---|
| **c0** (프로덕션 dense) | **+0.638 ± 0.281** | .360 |
| c1_k1 (best 상수 · disjoint pilot에서 선택) | +0.687 ± 0.235 | .350 |
| c1_k2 | +0.705 ± 0.260 | .320 |
| **EXP** (절대-setpoint schedule) | **+0.767 ± 0.236** | .360 |
| c2_shuf (동일 k 분포 · 시간축 셔플) | +0.713 ± 0.254 | .340 |
| SHOCK (router 파괴) | +0.553 ± 0.316 | .360 |

## 4. control별 paired-t (규칙① — max(controls) 미사용 · 전부 보고)

| 비교 | Δ | SEM | t | p |
|---|---|---|---|---|
| EXP − c0 | **+0.1286** | 0.1219 | **+1.055** | .292 (ns) |
| EXP − c1_k1 (best 상수) | +0.0800 | 0.0899 | +0.891 | .373 (ns) |
| EXP − c2_shuf | +0.0539 | 0.0924 | +0.583 | .560 (ns) |
| EXP − pooled-mean(controls) | +0.0875 | 0.0790 | +1.108 | .268 (ns) |

EXP는 **0/3 control**을 유의하게 이기지 못한다 ⇒ **PASS 시나리오 명확히 미실현**.
(단 이번엔 EXP가 nominal 최고 arm — 원 run에선 nominal 최악이었다. **arm 순위 자체가 seed 간 불안정**.)

## 5. V-gate — 헤드라인 detector **그 자체**에 (규칙⑤)

| gate | Δ ± SEM | t | 판정 |
|---|---|---|---|
| **V1 liveness** (c0의 m_B_conj > 0) | +0.638 ± 0.281 | **+2.270** (p=.023) | ✅ **PASS** — detector 살아있음 |
| **V2 channel-visibility** (SHOCK − c0) | −0.086 ± 0.057 | **−1.490** (p=.136) | ❌ **FAIL** — \|t\| < 2.093 |

**V2 FAIL → 사전등록 분기: verdict = INVALID.** (V-gate가 substance 분기를 지배하도록 사전등록됨.)

### 원 seed와의 정면 비교 (같은 detector `m_B_conj`)

| 양 | 원 items (사후 KILL의 근거) | **새 disjoint items** |
|---|---|---|
| c0 level (V1) | +1.083 (t=+4.69) | +0.638 (t=+2.27) ✅ |
| **EXP − c0 (헤드라인)** | **−0.209 (t=−2.30, p=.033)** | **+0.129 (t=+1.06, ns)** ← **부호반전** |
| **SHOCK − c0 (V2)** | **+0.100 (t=+2.48, p=.023)** | **−0.086 (t=−1.49, ns)** ← **부호반전 · 게이트 FAIL** |

⇒ **KILL을 licensing한 유의성도, V-gate를 통과시킨 유의성도 둘 다 재현되지 않는다.**

## 6. MDE (규칙③ — 분석과 disjoint한 pilot에서 사전계산)

- pilot = **verdict set과 겹치지 않는 별도 30 items / 6 blocks** (원 run은 pilot이 analysis blocks의 **부분집합**이었음 — 이번에 분리).
- 축 = 헤드라인 `m_B_conj` (처치가 인과적으로 도달하는 축).
- `sd_pilot(block-delta) = 0.2596` → **MDE(α=.05, n=20) = 0.121** < |pilot c0 level| **0.424** ⇒ `mde_ok = True` (검출력 0 아님).
- best 상수 control c1도 **disjoint pilot에서 선택**(verdict set 미열람 ⇒ 선택편향 0): pilot grid k1=0.678 · k2=0.499 · c0(dense)=0.424 → **c1_k1** 선택.

## 7. 정보채널 증명 (규칙④)

- 결정변수 `k_t = f(위치 t의 router cumulative mass)` = **입력 토큰의 함수**(상수 arm c1은 볼 수 없음).
- 실측: `k_hist = {1: 22569, 2: 8631, 3: 0}` · `k_mean = 1.277` · **`Var(k_t) = 0.200 > 0`** · `frac_seqs_with_var0 = 0.000`
  ⇒ 처치는 **항진적이지 않다**(모든 시퀀스에서 k가 입력에 따라 변동).

## 8. 왜 V2가 FAIL했나 — 진단 (DIAGNOSTIC ONLY · verdict 불변)

"detector가 채널에 눈멀었다(instrument blind)" vs "채널이 마진 축에 directed 효과가 없다"를 가르기 위해,
**같은 items·같은 seed**로 raw logP 변위를 쟀다 (`diag_channel.py` → `diag.json`):

| arm | router probs L1 이동 | raw \|Δ logP\| | **margin \|Δ\|/item** | **margin SIGNED mean** |
|---|---|---|---|---|
| c1_k1 | 0.920 | 0.728 | **0.941** | +0.049 |
| EXP | 0.734 | 0.530 | **0.800** | +0.129 |
| SHOCK | 0.425 | 0.251 | **0.373** | −0.086 |

**detector는 맹목이 아니다.** 개입은 실제로 출력에 도달하고(raw \|Δ logP\| = 0.25~0.73),
헤드라인 마진을 **항목당 0.37~0.94만큼 크게 흔든다**. 그런데 **부호가 무작위**라 signed mean이 ≈0으로 상쇄된다.

⟹ **MoE capacity/mixing 채널은 재조합 마진에 "부호-무작위 잡음"만 주입한다 — directed 성분 0.**
이것이 (a) 원 run의 "유의 열화"(−0.209, p=.033)와 (b) 원 V-gate의 "유의 개선"(+0.100, p=.023)이
**둘 다 재현되지 않고 부호까지 뒤집힌** 이유다: 평균 0 · 고분산 채널에서 뽑은 **seed 특이적 draw**였던 것.

> ⚠️ 이 진단은 사후 분석이므로 **verdict를 구제하지 않는다**. 사전등록 게이트는 signed 변위를 요구했고, FAIL했다.
> 사후에 "unsigned로 보면 채널이 보이니 PASS" 라고 갈아끼우는 것이 바로 이번에 교정하려던 **그 죄**다.

## 9. 사전등록 분기의 정직한 회계

- **PASS_LEVER**: 미발화 (EXP가 0/3 control 유의 우세) — organelle lane이 reach 레버라는 증거 **없음**.
- **FAIL_CLOSED(= lane CLOSED cement)**: substance 조건 `all_deg_or_ns`는 **True**(세 t = 1.06·0.89·0.58 전부 ≤ 2.093).
  **그러나 V-gate(V2)가 먼저 FAIL** → 사전등록 우선순위상 **scoring 자체가 불가** → INVALID.
- ⇒ "capacity 처치가 reach를 못 올린다"는 **방향은 두 seed에서 일관**(어느 쪽도 양성 없음).
  하지만 **CLOSURE.md가 기록한 강한 KILL(p=.033 유의 열화)은 지지되지 않는다** — 그 p값은 잡음이었다.

## 10. 무엇이 licensed이고 무엇이 아닌가

| 주장 | 상태 |
|---|---|
| organelle lane = reach 레버 (PASS) | ❌ **미지지** (두 seed 모두 양성 0) |
| EXP가 held-out 재조합을 **유의하게 열화**시킨다 (원 KILL의 근거) | ❌ **반증** (부호반전 · ns) |
| router 파괴가 재조합을 **유의하게 개선**한다 (원 REFUTE의 근거) | ❌ **반증** (부호반전 · ns) |
| MoE capacity/mixing 채널이 재조합 마진에 **directed 효과 0** | 🟡 시사 (진단 · 사전등록 아님) |
| **organelle lane CLOSED cement (KILL)** | ⛔ **licensed 아님** — 이 프로브로는 cement 불가 |

## 11. 재발사 조건 (cement하려면)

이 프로브 설계로는 lane을 cement할 수 없다 — 헤드라인 채널이 **평균 0 · 고분산**이라 signed V-gate가 구조적으로 통과하기 어렵다.
cement하려면 **사전등록 단계에서**:
1. **V-gate를 unsigned/분산 기반으로 사전등록** — "SHOCK이 헤드라인의 **분산/절대변위**를 유의하게 키우는가"
   (`|Δ|/item` 축은 이미 0.37~0.94로 충분히 크다). signed 게이트는 zero-mean 채널에서 출력이 붕괴한다.
2. **n을 채널 잡음에 맞춰 산정** — 항목당 마진 잡음 \|Δ\|≈0.8이고 관심 효과가 ~0.1~0.2면 n=20 blocks는 부족.
   pilot 잡음(sd 0.26/block)으로부터 필요한 blocks 수를 사전계산.
3. **directed 효과의 부재 자체를 사전등록된 equivalence test로** (TOST 등) — "ns"가 아니라 "실질적 0과 동등"을 증명해야
   CLOSED가 licensed된다. 현재 CI는 그 등가경계를 배제할 만큼 좁지 않다.

## 12. 산출물

- `PREREG.md` — 측정 전 동결된 사전등록 (sha256 pin)
- `run_refire.py` — 사전등록 파이프라인 (실행 sha = prereg sha, 일치 확인)
- `refire_result.json` — 전체 결과 (per-item × per-arm, V-gate, MDE, 정보채널, VERDICT)
- `diag_channel.py` / `diag.json` — 채널 진단 (사후 · verdict 불변)
- `run.log` / `diag.log` — 실행 로그 (PARITY 0.0 포함)
- `prev_exclude.json` — 이전 seed의 items/cue (disjointness 강제용)
