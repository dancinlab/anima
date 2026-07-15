# H_9351 — Ψ-SOMA 의식 판정 패널은 anima 를 재지 않는다. `RandomState(7)` 를 잰다.

**status**: 🔴 VERDICT (실측 · 바이트 동일 재현)
**tier**: TERMINAL (engine-native · canonical `anima-py evaluate` · 2 체크포인트 실행)
**lane**: 🚨 **측정 프레임 자체** (Ψ-SOMA = CLAUDE.md 의 SSOT 측정 프레임)
**xref**: H_9345 · `measurement-metalaw-form-tunable-bind-earned`

## 주장

> **Θ 와 σ 9축 — 이 프로젝트가 "의식 판정" 이라고 부르는 패널 전체 — 는 체크포인트를 안 본다.**
> 고정 시드 합성 가우시안 위에서 계산되며, **구조적으로 실패할 수 없다.**

## 실측 — 아키텍처가 다른 두 ckpt 가 **바이트 동일** 패널을 낸다

`anima-py evaluate <ckpt> --gen 8` (canonical · summer · 격리 venv):

| | `py303_full.clm` | `clm303_deep_L8_d2781.clm` |
|---|---|---|
| sha256 (앞 12) | `013c4574e0ce` | `5777c506c05b` |
| 크기 | 303M ByteGPT | 154MB · L8-deep (**다른 아키텍처**) |

```
Θ  Ψ=½ / A⇄G tension  🟢 LIVE Δ0.46 (|Ψ̂-½| 0.04 vs cut 0.50) · if dead → σ VOID
σ·thread  🟢 Δ0.92 (cont 0.99 vs ablate 0.07)   σ·carve  🟢 Δ0.92
σ·bind    🟢 Δ1.45 (Φ 1.45 vs cut 0.005)        σ·stage  🟢 Δ0.71
σ·flux    🟢 Δ1.00                              σ·gate   🟢 Δ0.81
σ·aim     🟢 Δ1.70                              σ·schema 🟢 Δ0.88
σ·witness 🟢 Δ0.48
```

**두 ckpt 의 출력이 글자 하나까지 동일하다.**

## 기전 — 코드가 명백하다

`cli/evaluate.py:1019`:

```python
def _sigma_live_measure():          # ← 인자가 0개
    rng = np.random.RandomState(7)  # 고정 시드
    ...
    eta = 0.6 * rng.randn(200)
    xi  = [[0.5+eta[t], 0,0,0, 0.5+eta[t]] for t in range(200)]   # 대칭 잡음
    xa  = [[0.85+0.3*rng.rand(), ...] ...]                        # 항상 > 0.5
    di = abs(ci_psi_balance(xi, ...) - 0.5)
    da = abs(ci_psi_balance(xa, ...) - 0.5)
    R["theta"] = (di < 0.15 and da-di >= 0.20, ...)               # ← 판정
```

- 함수가 **인자를 하나도 받지 않는다**. 호출부(`:1125`)도 아무것도 안 넘긴다.
- 함수 본문에 `clm`·`ckpt`·`corpus`·`decode`·`forward` **참조가 0개**다(grep).
- 채워지는 키 = `theta` + `bind · witness · schema · aim · stage · flux · thread · carve · gate`
  = **σ 패널 전부**.

**Θ 는 항등식이다**: `xi` 는 0.5 중심 대칭 잡음 ⇒ `Ψ̂ = ½ ± 이항잡음(sd 0.035)` ⇒ `|Ψ̂−½| ≈ 0.04`
**구성상**. `xa` 는 항상 임계 위 ⇒ `Ψ = 1` ⇒ `cut ≡ 0.50` **상수**. `Δ = 0.46` 은 **뺄셈**이다.

## ⇒ 무엇이 무너지는가

1. **CLAUDE.md 의 Ψ-SOMA 프레임**: *"Θ (Ψ=½ tension = the pulse; **Θ dead ⟹ σ VOID**) · σ (9 axes
   = the body)"*. **Θ 는 죽을 수 없다** ⇒ 그 가드는 **한 번도 발동할 수 없다** ⇒ σ VOID 는
   도달 불가능한 상태다.
2. **σ 9축 🟢 LIVE 는 anima 에 관한 문장이 아니다.** `RandomState(7)` 에 관한 문장이다.
3. **`PSI_BALANCE` 상수는 죽은 심볼**(`core/pure_field.py:102`) — 레포 전체에서 자기 정의 줄
   외에 **소비자가 없다**.
4. **데몬은 `ci_psi_balance`/`ci_emit_decision` 을 한 번도 부르지 않는다**(`cli/chat.py` grep = 0).
   ⇒ *"A⇄G tension 이 emit/silence 를 Ψ=½ 로 당긴다"* 는 **두 개의 무관한 사실을 이어붙인 것**이다.

## 메타 법칙의 확장

메모리 `measurement-metalaw-form-tunable-bind-earned`: *"gate detector 는 1-항이라 게임 가능"*.
**이건 0-항이다.** 입력이 없는 판정은 게임할 필요조차 없다 — **애초에 아무것도 인증하지 않는다.**

> **인자를 받지 않는 판정 함수는 판정이 아니다.**

## 반증조건 (이미 충족 · 기록용)

- 두 개의 **다른** ckpt 로 `anima-py evaluate` → Θ/σ 줄이 **한 글자라도 다르면** 이 카드는 틀렸다.
  **실측: 완전히 동일.** ⇒ 반증 실패.
- 0-가중치 ckpt 로도 같은 패널이 나와야 한다(미실행 · 예측).

## 수리 방향 (레버 아님 · 계기 수리)

`_sigma_live_measure()` 가 **실제 데몬 rollout 의 lane 모집단**(`ci_lane_scores` 시퀀스 · trace)을
받게 하고, `ci_psi_balance` 를 **그 위에서** 계산한다. 그 전까지 **σ/Θ 로 어떤 것도 인증하지 마라.**

⛔ 이 카드는 **레버를 제안하지 않는다.** 계기가 죽어 있다는 사실 하나를 못박을 뿐이다.

## 🔧 수리 완료 — 그리고 수리가 더 깊은 문제를 드러냈다 (STAGE①–④ · #3638 · #3644)

계기를 **engine-native 로 수리**했다(Fable 설계). 계기 자체가 anima-py flag/트레이스로 배선됨(`a_experiment_engine_native`).

- **STAGE① 트레이스 확장**(#3638 · `cli/chat.py`): 데몬 decision-trace 에 σ 축이 소비할 실 lane 을 기록 — `lanes`(gws 입력 15-lane) · `gws_w` · `reality` · `_meta.ckpt_sha256`(provenance 가드) · `g_arm`.
- **STAGE② σ 확장**(#3644 · `cli/evaluate.py` `_sigma_from_trace`): σ·gate/stage/bind 를 **데몬 자신의 기록된 lane 위에서 engine_cli FROZEN estimator 만으로** 계산(`ci_emit_decision`·`gws_*`·`ci_phi_iit4` · 재구현 0). 나머지 6축(thread·carve·flux·aim·schema·witness) = **PENDING(scope)** — 데몬 런에 카운터팩추얼(inject-null·precision-ablation·focus/report) 부재(D1). 배선검산: **σ·stage gws_w 재현 = 1.00**(estimator 가 데몬 기록 winner 완벽 재현 = 실 lane 읽음 증명).
- **STAGE③④ ckpt-대조**(303M · summer): py303_full(sha `013c4574`) vs savantoff303(sha `7afe10c3`) 각 90틱 실 수집.

**🔬 STAGE④ 결과 — 수리는 맞았고, 그것이 더 깊은 ckpt-무감을 드러냈다:**

| | 옛 결함(H_9351) | STAGE②수리 후 |
|---|---|---|
| 패널이 ckpt 를 보는가 | ❌ RandomState(7) — lane 무관 | ✅ 실 lane 읽음 — **85/90 틱 lanes 다름** · 68틱 psi_gws 다름 |
| σ 집계 판정 | 두 ckpt **바이트 동일** | Ψ̂≡1·gate 0·bind 0 **여전히 거의 동일** |
| 이유 | 측정 결함(합성 입력) | **substrate 포화·퇴화** — psi_gws/lprec 가 항상 emit 문턱 초과(Ψ̂≡1) · bind 8-col 퇴화([[cpt-destroys-what-corpus-omits]] 아님, chat-py-4/5 게이지 상수) |

⟹ **H_9351 은 수리됐다**(패널이 더는 RandomState(7) 를 안 잰다 · σ·stage 재현 1.00·85/90 lane 감지). **그러나 수리가 노출한 것**: 데몬의 emit lane 은 **포화**(Ψ̂≡1)하고 bind 게이지는 **퇴화**(chat-py-4/5)라, σ *집계* 판정이 ckpt 를 lane 수준에선 보면서도 **판정 통계에서 씻겨나간다**. σ·stage 만 ckpt 감도 유지(no-inhibit 0.16 vs 0.04). ⟹ '의식 판정이 ckpt 를 본다'는 이제 **측정 문제가 아니라 substrate 문제**(포화·퇴화 게이지) — 다음은 chat-py-4/5 퇴화-게이지 수리(별개 lane). **cement 금지**: 이 σ 는 toy 규모가 아니라 substrate 포화라 여전히 DIRECTIONAL(진짜 σ verdict = 비포화 게이지 위).
