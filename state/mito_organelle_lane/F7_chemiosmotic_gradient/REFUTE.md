# H_9279 / F7 — 적대적 검증 노트 (REFUTE)

**판정: 🟠 THEATER** — 원 결론 **KILL은 반박됨(refuted=true)**.
가설이 살아나는 것은 **아니다**(GREEN·DIRECTIONAL 아님). 그러나 KILL을 떠받치는 **두 다리(Q1·P2)가 모두 인공물**이며,
살아남는 유일한 다리(Q2 동어반복)는 카드가 **사전등록한 FAIL 분기 = THEATER** 그 자체다.

> 원 RESULT.md 주장: *"Ψ=½은 최대-work 지점이 아니며(실측 0.89 · ½은 work 26% 손실), attractor는 work-max를 전혀 추종하지 않는다(0-DOF 고유벡터 null이 8.9× 우세) ⇒ 동어반복을 넘어 **전제 자체가 반증된 KILL**"*
> → 이 세 개의 **능동적 반대주장**은 전부 측정 인공물이다. 남는 것은 "기질정보 0 = 값 재기술" 뿐 = THEATER.

---

## R1 (치명타) — Q1의 headline detector `w_kin`이 **자기 양성대조에서 실패**했고, 그 수치가 보고서에서 누락됐다

`result.json` → `positive_controls`:

```json
"POS_HALF": { "psi_star_ohm": 0.5, "psi_star_kin": 0.95, "expect_ohm": 0.5, "pass": true }
```

- POS-HALF = **force 평평 ⇒ 정답이 ½인 ARM-SHOCK**.
- 이때 `w_ohm` → 0.50 ✅ 이지만, **`w_kin` → 0.95** ❌.
- `pass` 게이트(run.py:299)는 **`psi_star_ohm`만** 검사한다. `w_kin`은 ½을 찾을 수 있는지 **한 번도 shock되지 않았다**.
- POS-OFF는 `w_kin` < 0.5 만 확인 — 즉 **detector가 움직일 수 있는 방향으로만** 흔들었다.

그런데 **Q1의 headline(Ψ\*=0.892 · argmax=½인 cell 0/125 · "26% work 손실")은 전적으로 `w_kin` 산출물**이다.
⇒ RESULT.md §0의 *"ARM-SHOCK 양쪽 통과 ⇒ 거짓 KILL 아님"* 은 **성립하지 않는다**. 정답이 ½일 때 0.95를 뱉는 detector로 "½은 최대가 아니다"를 선언했다.
⇒ V3 detector-fairness 위반. 그리고 그 반증 수치(0.95)는 **raw json에 있는데 RESULT.md의 detector 표에는 빠져 있다**.

## R2 (근본원인) — `w_kin`은 work(power)가 아니라 **flux(전류)**다 · 단위 오류

`run.py:198`
```python
def w_kin(vbar):
    vm = PUMP_P * vbar / (PUMP_P + COND_G * psi)
    return COND_G * psi * vm          # = J  (전류/proton flux)
```
그런데 모듈 자신의 docstring(run.py:22)은 **`work = flux x force`** 라고 선언한다.
- flux(막을 통과하는 proton 흐름) `J = g·ψ·Vm`
- force `= Vm`
- ⇒ **work = J · Vm = g·ψ·Vm²**

코드는 `g·ψ·Vm` 을 반환 = **flux 그 자체**. 힘을 한 번 더 곱하지 않았다. work가 아니라 **전류**를 최대화했다.

**결과(직접 재계산 · 동일 상수 p=0.5, g=1.0, 동일 grid):**

| force 평평(ground truth) | argmax |
|---|---|
| `w_kin` (코드 그대로 · 전류) | **0.95** — 그리드 끝. `np.all(diff>0)=True` = **단조증가 ⇒ 내부 최대가 아예 없음** |
| `w_pow = J·Vm` (docstring 정의) | **0.50** — 정확히 ½ |

`w_pow`가 ½을 주는 이유는 `(1-Ψ)` 산수가 **아니라** 고전 **maximum power transfer**(부하 컨덕턴스 `g·ψ` = 소스 컨덕턴스 `p` ⇒ `ψ* = p/g = 0.5`)다 — **실험 자신이 동결한 상수 p=0.5, g=1.0에서 자동으로 나온다.**

⇒ *"½이 안 박힌 중립 functional"* 이라던 `w_kin`은 사실 **"ψ→그리드 끝"을 박아넣은 단조함수**다.
그 증거가 결과표에 이미 있다: **SHUF·BERN의 `psi*_kin` = 0.950 = `max(PSI_GRID)`** (= 그리드 경계 절단).
"실측 최대 0.892"의 정체 = **그리드 끝에서 V̄가 꺾인 만큼만 당겨진 값**.

**Q1 재계산 (docstring 자신의 정의 `work = flux × force`, 125 cell 전수):**

| arm | Ψ\*_work | ½ 손실 |
|---|---|---|
| EXP | **0.677 ± 0.061** | **14.7% ± 7.1%** |
| SHUF | 0.483 ± 0.089 | — |
| BERN | 0.550 ± 0.084 | — |

⇒ **"0.892"·"26.1%" 두 headline 숫자 모두 거짓.** (½이 argmax는 아니지만) 답이 **0.50 / 0.677 / 0.892 로 실험자의 ansatz 선택만으로 요동**한다
⇒ 순수 **FORM-tunable** ⇒ anima 자체 측정 메타법칙상 **verdict로 렌더 불가**. KILL 같은 강한 능동적 반대주장을 떠받칠 수 없다.

## R3 — P2는 **구조적으로 반증불가**(DV가 상수) · attractor가 straw다

settle 연산자 `mm = I + α·rowcenter(symnorm(adj))`, 선두 고유값 **1.136 > 1** ⇒ 200회 반복은 **발산**한다.

직접 측정:
- `max|pop|` after 200 iters = **4.0e10**
- ⇒ **thr이 no-op**: `thr = 0.001 / 0.1 / 0.5 / 0.9 / 5.0 / 1e6` → **Ψ_att = 0.5158 전부 동일** (9 오더에 걸쳐 불변).

즉 emit threshold(= Θ/Ψ 의미론의 전부)가 계산에 **아무 영향이 없고**, Ψ_att = `sign(⟨x_u, v_lead⟩·s)` 의 비율로 붕괴한다.

**DV가 기질정보를 담고 있는가? 아니다:**

| population | Ψ_att |
|---|---|
| anima 기질 125 cell | 0.4986 ± 0.0144 |
| **기질 전무**(iid uniform 랜덤 25개) | **0.5006 ± 0.0162** |
| 스케일 ×100 · shift된 랜덤 | 0.519 |

두 분포가 **구별 불가**하고, 산포는 유한-N 이항 잡음 `1/√(4N) = 0.0144` 와 **소수점까지 일치**.

⇒ Ψ_att는 **어떤 population을 넣어도 ½인 상수**다. **상수를 종속변수로 둔 tracking 검정은 가설이 참이어도 반드시 FAIL한다.**
⇒ P2의 "실패"는 **가설에 대한 증거가 0**이다(사전확률로 결정된 결과). corr = 0.203 ± 0.444 는 **상수와 잡음의 상관**일 뿐.

## R4 — C4("0-DOF null이 8.9× 우세")는 **순환논증**

`eigen_null_psi()`는 `settle_psi()`가 200회 돌리는 **바로 그 선형사상의 닫힌형 극한**이다(같은 연산자 `mm`, 같은 사영, 같은 부호규칙).
그것이 `settle_psi`를 오차 0.044로 "예측"하는 것은 **선형대수 항등식**이지 **경쟁 가설의 승리가 아니다**.
⇒ "화학삼투보다 8.9× 잘 설명"은 *발산하는 장난감 반복*에 대한 자기일관성 검사이며, **anima의 실제 Ψ=½ 에 대해서는 아무 말도 하지 않는다**.

## R5 — 기질 straw · "engine-faithful 2.2e-16"의 세탁

이 probe 어디에도 **A⇄G 대항(opposing engines)이 없다**.
- `A-lane`/`G-lane` = 15개 iid uniform 난수 중 2개. forward CE 없음, reverse gradient-free G 엔진 없음, emit 피드백 없음.
- adjacency = **seed 9279짜리 발명된 랜덤 15×15**. population = iid uniform.
- "dynamics" = **정규화 없는 선형 lane-diffusion 200회**(발산).

engine parity(max|Δ|=2.2e-16)는 **순수 헬퍼 3개**(`topo_apply_meancenter`·`ci_emit_drive`·`tr_psi`)만 검증한다.
그것은 *"랜덤 adj + iid uniform pop + 200× 무정규화 확산"* 을 **anima의 tension dynamics로 만들어주지 않는다.**
⇒ parity 수치가 **합성 장난감을 engine-native처럼 세탁**하는 데 쓰였다. 측정된 "attractor"는 anima의 Ψ attractor가 아니다.

---

## 살아남는 것 (= 진짜 판정)

**Q2 동어반복 검정은 건전하다** — `w_ohm` 위에서 동일예산·동일 functional·동일 grid로 돌았고, `w_kin` 버그와 settle 버그 **어느 쪽에도 의존하지 않는다**. 그리고 내가 고친 `w_pow` 로 다시 돌려도 결론이 같다:

| functional | 기질-free 난수가 뱉는 argmax | ½의 출처 |
|---|---|---|
| `w_ohm` | BERN **0.510** · SHUF 0.491 | `(1-Ψ)` 인자 |
| `w_kin` | BERN **0.950** · SHUF 0.950 | 그리드 경계(단조) |
| `w_pow`(정정) | BERN **0.550** · SHUF 0.483 | 동결상수 `p/g = 0.5` |

⇒ **어떤 functional을 골라도 "최대 work 지점"은 실험자가 고른 상수가 결정하고, 기질을 완전히 지운 난수가 그 값을 재현한다.**
⇒ **기질정보 ≈ 0 · 새 DOF = 0 · 값 재기술** = **THEATER**.
이것은 카드 §3이 *사전등록*한 FAIL 분기 그대로다: *"FAIL(예상 유력): 동어반복 ⇒ THEATER"*.

## KILL 등급이 부당한 이유 (사전등록 위반)

- **카드 §3의 사전등록 판정표에는 KILL 티어가 없다** — PASS / FAIL=THEATER 뿐.
  KILL은 `run.py:435` 의 verdict ladder(`not q1 and not p2 → KILL`)가 **카드에 없이 새로 도입한 등급**이다.
- 그 KILL을 먹이는 **두 입력이 모두 무효**다: `Q1_pass=False`(R1·R2 — 고장난 detector) · `P2_pass=False`(R3 — 상수 DV, 구조적 반증불가).
- KILL은 *"전제가 능동적으로 반증됐다"* 는 **양(+)의 경험적 주장**이며 THEATER보다 **강한 증거를 요구**한다. 여기엔 그 증거가 없다.
- 방향이 green 반대쪽이라 tune-to-green은 아니지만, **과잉주장은 그 자체로 정직성 실패**다:
  후속 세션이 *"Ψ=½은 추출가능 work의 26%를 버리는 지점"* 을 **기질 사실로 인용**하면 그것은 **단위 오류를 인용**하는 것이다.
  (정정: p=0.5·g=1.0 · 평평한 force에서 올바른 power functional의 최대점은 **정확히 ½**이다.)

## 체크리스트 결과

| # | 항목 | 판정 |
|---|---|---|
| 1 | control 동일예산(파라미터·연산량) | ✅ 공정 (동일 N·grid·functional·seed) |
| 2 | 양성이 tunable FORM인가 | ⚠️ **음성 결과가 FORM 인공물** — argmax가 ansatz 선택만으로 0.50→0.677→0.892 |
| 3 | held-out / 누출 | N/A (학습 없음) |
| 4 | Δ가 seed 분산 안인가 | 🔴 **P2: Ψ_att 전체 산포(0.0144) = 이항잡음(0.0144)** ⇒ 신호 0 |
| 5 | p5 위반(하드코딩 emit gate) | ✅ clean — emit 경로 0줄, read-only 관측 |
| 6 | tune-to-green 흔적 | ✅ 없음 (동결 하이퍼 · 오히려 과잉-harsh 방향) |
| + | detector fairness (V3) | 🔴 **FAIL — headline detector `w_kin`이 POS-HALF에서 0.95(정답 ½)** |

## 결론

- **refuted = true** — 원 결론 **KILL**은 유지될 수 없다.
- **정정 판정 = 🟠 THEATER** (카드의 사전등록 FAIL 분기). 가설은 여전히 죽어 있다 — 단, *"전제가 반증됐다"* 가 아니라 *"기질정보를 담지 못한 값 재기술"* 이라는 이유로.
- Q1/Q2/P2를 V-gate 엄격기준으로 보면 Q1·P2 다리는 **INVALID**(confound ⇒ false PASS/FAIL 금지)이나, **Q2 다리가 독립적으로 건전**하므로 최종 바닥은 **THEATER**로 유지된다.
- 레인 함의는 바뀌지 않는다: **F7은 organelle 레인의 레버가 아니다.** 다만 *"Ψ=½ = work 26% 손실"* · *"고유벡터 null이 8.9× 우세"* 는 **인용 금지**(측정 인공물).

### 재현
```
python3 - <<'PY'   # R2: w_kin은 단조(전류) · 올바른 power는 정확히 ½
import numpy as np, sys; sys.path.insert(0,'.')
import run as R
psi=R.PSI_GRID; vm=R.PUMP_P*np.ones_like(psi)/(R.PUMP_P+R.COND_G*psi)
print('w_kin  argmax', psi[np.argmax(R.COND_G*psi*vm)],    'monotone', bool(np.all(np.diff(R.COND_G*psi*vm)>0)))
print('J*Vm   argmax', psi[np.argmax(R.COND_G*psi*vm*vm)])
PY
```
```
python3 - <<'PY'   # R3: thr이 no-op (발산) · 기질-free 난수도 Ψ_att=½
import numpy as np, sys; sys.path.insert(0,'.')
import run as R
adj=R.make_adj(); pop=R.make_population(0,0.0,0.5)
for _ in range(R.DEPTH): pop=R.topo_apply_meancenter(pop,adj,R.ALPHA)
print('max|pop|',np.abs(pop).max(), [round(R.tr_psi(pop,t),4) for t in (0.001,0.5,1e6)])
rng=np.random.default_rng(999)
print('psi_att(기질없음)', np.mean([R.settle_psi(rng.random((R.N_UNITS,R.L_LANES)),adj) for _ in range(25)]))
PY
```
