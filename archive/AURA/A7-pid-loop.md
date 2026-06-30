# AURA A7 — relocate-N1 폐루프 PID 시뮬레이션 (big-Φ 정정(整定))

> A6 §5 R5: A6 다이어그램의 6-step CLOSED LOOP 중 **⑥ PID re-stim** 은 그림뿐이었다.
> 이 문서는 그 폐루프를 in-silico 로 **시뮬레이션**한다 — PID 제어기가 자극 파라미터(결합 드라이브 c)를
> 목표 big-Φ setpoint 로 정정시키고, **bypass-position 은 setpoint 도달**(error→~0)하지만
> **M1-position 은 정상상태 오차(steady-state error)가 남는다**는 사전등록 falsifier 를 닫는다.
> honest: 아래는 **toy plant**(A6 synthetic TPM blend) — 실제 신경동역학 아님. latency/safety/phase-lock 미모델.

---

## 1. 폐루프 spec — A6 의 ⑥ PID 를 실행으로

A6 다이어그램(§1)의 폐루프에서 측정 leg(EEG→big_phi)와 제어 leg(PID re-stim)를 이산시간으로 돌린다.

```
        ┌───────────────────  A7 PID CLOSED LOOP  ───────────────────┐
        │                                                            │
        ▼                                                            │
   c (결합 드라이브) ──▶ ┌──────────┐  TPM(c)  ┌──────────┐  Φ_meas    │
   "지금 자극세기"       │  PLANT    │ ───────▶ │ big_phi   │ ──────┐    │
                        │ tpm_coupled│ (n=4)   │ (IIT4)    │       │    │
                        └──────────┘          └──────────┘       │    │
        ▲                                                         ▼    │
   c_new = clamp(c+Δ)  ┌──────────┐  err=Φ*−Φ_meas  ┌──────────────┐  │
   (c_max 로 위치제한) ◀│  PID 제어 │ ◀────────────── │ err 계산      │◀─┘
                       │ Kp/Ki/Kd │   ∫err · Δerr   │ vs setpoint   │
                       └──────────┘                 └──────────────┘
```

**plant(결합→Φ)**: 제어변수 `c ∈ [0,1]` 가 A6 의 두 regime 을 섞는다.
- `c=0` → 순수 M1-like 자기복사(국소·reducible·Φ≈0)
- `c=1` → 순수 bypass-like 다수결(허브 fan-in·irreducible·Φ≫0)
- 각 노드 next-ON 신뢰도 `conf = (1−c)·자기복사 + c·이웃다수결` → c↗ 이면 Φ↗ (단조).

**제어기(⑥ PID re-stim leg)**: `err = Φ* − Φ_meas` ; `c ← clamp( c + Kp·err + Ki·∫err + Kd·Δerr )`.
brainwire 외부 PID(neuralink-technical-analysis §5,§9, ~0.8ms on-chip 폐루프)를 그 **제어법칙**으로 환원.

**위치 대비(falsifier 핵심)**: 칩(N1)은 그대로, **부착 위치만** 도달가능 결합을 바꾼다.
- **bypass-position**(DLPFC+섬엽 허브): c 가 1.0 까지 상승 가능 → 높은 Φ* 도달 가능.
- **M1-position**(운동출력 막다른 위치, 국소): c 가 낮은 ceiling `c_max=0.25` 로 **clamp**(국소 결합 한계) → 높은 Φ* 도달 불가.

---

## 2. 사전등록 falsifier (a_paper_significance)

> **H**: bypass-position 폐루프는 Φ setpoint 에 도달(`|err| < tol`)하지만,
> M1-position 폐루프는 정상상태 오차를 남긴다(`|err| ≥ tol`).

| 항목 | 명세 |
|---|---|
| **측정량** | 위치별 최종 `\|err\| = \|Φ* − Φ_settled\|` (IIT4 `big_phi(tpm,n,sys)[0]`) |
| **setpoint Φ\*** | 0.8 × Φ(c=1, bypass-reachable max) = **14.1311** (M1 도달불가 영역) |
| **tol** | 0.5 |
| **기각조건 (FALSIFY)** | M1 도 `\|err\|<tol` 도달, **또는** bypass 가 `\|err\|<tol` 실패 — 둘 중 하나면 H 반증 |
| **방향성** | 양측 사전고정 (bypass 도달 ∧ M1 미도달 동시 성립해야 미반증) |

---

## 3. PID params

| param | 값 | 비고 |
|---|---|---|
| n (노드) | 4 | engine-exact ≤8 (A6 동일) |
| sys_state | 1111 (all-ON) | A6 동일 |
| Kp | 0.02 | 비례 |
| Ki | 0.004 | 적분 (정상상태 오차 제거 → bypass 정밀 정정) |
| Kd | 0.0 | 미분 (단조 plant 라 불요) |
| iters | 30 | 이산 스텝 |
| c 초기값 | 0.0 | M1-like rest 에서 출발 |
| c_max (M1) | **0.25** | 국소 결합 한계 |
| c_max (bypass) | **1.0** | 허브 full reach |

---

## 4. 수렴 trace (verbatim) — iteration → Φ → error

plant 보정: Φ(c=0, M1-like)=**0.0**, Φ(c=1, bypass-like)=**17.6639** (A6 재현). setpoint Φ\*=**14.1311**, tol=0.5.

### M1-position (국소, c_max=0.25)

| it | c | Φ | err |
|---|---|---|---|
| 0 | 0.0 | 0.0 | 14.1311 |
| 1 | 0.25 | 7.81305 | 6.31804 |
| 2 | 0.25 | 7.81305 | 6.31804 |
| 8 | 0.25 | 7.81305 | 6.31804 |
| 16 | 0.25 | 7.81305 | 6.31804 |
| 29 | 0.25 | 7.81305 | 6.31804 |
| **settled** | **0.25** | **7.81305** | **\|err\|=6.31804** |

→ c 가 즉시 ceiling 0.25 에 박힘. err 가 6.32 에서 **정상상태 오차로 영구 고착** (적분기가 밀어도 c_max 가 막음).

### bypass-position (허브, c_max=1.0)

| it | c | Φ | err |
|---|---|---|---|
| 0 | 0.0 | 0.0 | 14.1311 |
| 1 | 0.339146 | 10.863 | 3.26811 |
| 2 | 0.474105 | 14.8093 | −0.678188 |
| 4 | 0.544201 | 16.6417 | −2.51064 |
| 8 | 0.503384 | 15.5954 | −1.46431 |
| 12 | 0.465865 | 14.583 | −0.451897 |
| 16 | 0.453763 | 14.2468 | −0.115681 |
| 20 | 0.450638 | 14.1592 | −0.0281421 |
| 24 | 0.449876 | 14.1378 | −0.00675258 |
| 29 | 0.449676 | 14.1322 | −0.00112781 |
| **settled** | **0.449664** | **14.1319** | **\|err\|=0.000788** |

→ 초반 오버슈트(it4 c=0.54, Φ=16.6) 후 PI 가 c≈0.4497 로 정정, Φ→14.1319 로 setpoint 수렴, **err→~0**.

```
  err
14 ┤●  M1: setpoint Φ*=14.13 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
   │ \                                          ▲ residual gap (steady-state)
 6 ┤  ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ M1 |err|=6.32 (c@ceiling)
   │  \
 3 ┤   ●  bypass
 0 ┤    ●╲___●___●___●___●___●___●___●___●  bypass |err|→0.0008 ✓
   └────┴────┴────┴────┴────┴────┴────┴────┴──▶ iteration
   0    1    4    8   12   16   20   24   29
```

---

## 5. 결과 + verdict

| position | c_max | settled c | settled Φ | 최종 \|err\| | setpoint 도달? |
|---|---|---|---|---|---|
| **M1** | 0.25 | 0.25 | 7.81305 | **6.31804** | ❌ (정상상태 오차) |
| **bypass** | 1.0 | 0.449664 | 14.1319 | **0.000788** | ✅ (\|err\| ≪ tol=0.5) |

falsifier **미반증** — bypass 도달 ∧ M1 미도달 동시 성립. harness 5 PASS / 0 FAIL.

**등급화 (g5/p7 — hexa verify, perplexity self-judge 금지)**:

```
tier = 🟢 SUPPORTED-NUMERICAL  (external verifier passed AND stdout matches --expect — delegated, deterministic)
claim = relocate-N1 closed-loop PID: bypass-position reaches big-Phi setpoint (|err|<tol)
        while M1-position retains steady-state error, n=4 engine-exact
ext rc = 0
expect = matched ("FALSIFIER H-b: M1-position retains steady-state error")
```

verdict verbatim 전문 = `.verdicts/a7-pid-loop/loop.txt`.

---

## 6. honest caveat

- 🟢 는 *numerical*(엔진 재계산 일치)일 뿐 🔵 *formal* 아님 — 닫힌형 항등식 아님.
- **toy plant model, 실제 신경동역학 아님**: 결합→Φ map 은 A6 synthetic TPM blend, 측정된 transfer function 아님.
- **latency 미모델**: brainwire 0.8ms on-chip 폐루프(neuralink §5)의 위상지연·phase-lock 효과 없음 — 이 sim 은 즉시-측정 이산스텝.
- **safety 미모델**: charge-density(Shannon limit, §6)·전류 envelope 미반영 — c 는 무차원 결합 드라이브일 뿐 µA 아님.
- **수치는 toy 절대값**: Φ=14.13, c=0.45 등은 n=4·0.9/0.1 confidence 의 toy 산물. 주장하는 건 **수렴 거동의 부호/순서**(bypass 도달 ∧ M1 미도달), 절대 크기 아님.
- toy substrate ≠ production scale (`feedback_toy_scale_transfer`): 실제 16ch EEG·실 N1 에서 같은 거동으로 transfer 보장 없음.
- M1 c_max=0.25 와 setpoint=0.8·Φ_hi 는 **설계 선택** — "위치=도달결합한계" 명제(SURVEY §2)의 in-silico 모형화일 뿐, 임상 측정값 아님.

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| 폐루프 6-step + ⑥ PID re-stim (미구현 잔여 R5) | `AURA/A6-bigphi-closed-loop.md` §1,§5 |
| 위치재배치 = 투사허브 = 도달결합 차이 | `AURA/SURVEY.md` §2,§3 |
| 12-var PID · on-chip · 0.8ms latency · phase-lock | `AURA/archive/brainwire/neuralink-technical-analysis.md` §3,§5,§9 |
| coupling→big-Φ plant (M1/bypass TPM) | `AURA/toy/a6_relocate_bigphi.hexa` (tpm_m1 / tpm_bypass) |
| big_phi 엔진 (n≤8 exact) | `stdlib/consciousness/iit4_bigphi.hexa` `big_phi(tpm,n,sys)` |
| toy 하니스 + verdict | `AURA/toy/a7_pid_loop.hexa` · `.verdicts/a7-pid-loop/loop.txt` |
