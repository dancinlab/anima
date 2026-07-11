# H_9275 / F3 — 미토파지(sub-cell 품질관리) $0 probe 결과

- **일시:** 2026-07-12 · mini CPU-local · numpy only · wall 16.1s · 8 seed
- **산출:** `run.py` · `result.json` · `calib_scan.py`(V1 liveness 스캔)
- **판정:** 🟡 **DIRECTIONAL-POSITIVE** (THEATER 아님 · 단 GREEN도 아님)

---

## 0. 한 줄 결론

**directed 미토파지는 random 제거를 확실히 이긴다(ΔEff = +0.159 ± 0.019, 8/8 seed, oracle 천장의 98%).
카드의 반증조건(directed ≈ random)은 발동하지 않았다 = 손상 정의는 무정보가 아니다.**
단 (a) toy 시뮬레이션이고 core/ 미배선이며, (b) 카드가 명시한 **OR 손상정의의 ROS 항은 잉여(no-op)**,
(c) **ROS 단독은 효율보다 엄격히 열등**(demand confound 실증) — 즉 F4 결합은 F3를 돕지 않고 희석한다.

---

## 1. 무엇을 실제로 측정했나 (안티-토톨로지 설계)

이 probe의 순진한 버전은 **동어반복**이다: 제거자가 잠재 health `h_i`를 직접 보고, 점수도 mean `h_i`면
directed는 자명하게 이긴다. 그래서 여기서는:

- **잠재(latent) health `h_i`** — 아무 arm도 볼 수 없다. (oracle arm만 예외 = 천장 측정용)
- arm이 볼 수 있는 건 카드가 지정한 **두 관측량뿐**, 둘 다 **노이즈 + 교란(confound)** 이 걸려 있다:

| 관측량 | 정의 | 내장된 교란 |
|---|---|---|
| `eff_hat_i` | window EMA of (ATP_out / consumed) | ATP_out 측정노이즈 sd = σ·√load → **저부하 organelle의 효율 추정은 노이즈가 크다** (healthy인데 "손상 의심"으로 보임) |
| `ros_hat_i` | EMA of ROS = load/(cap·h) | 유닛별 수요 `d_i`가 **비균일(AR(1) persistent)** → **healthy인데 고수요면 ROS가 높다** = 거짓 손상 신호 |

즉 "손상의 관측정의가 실제로 잠재 손상을 짚어내는가"는 **진짜 신호추출 문제**이지 거저먹기가 아니다.
demand confound가 지배하면 카드의 손상정의는 실패하고 F3는 THEATER가 된다 — 그걸 시험한 것이다.

**Common random numbers**: 수요 tape·손상 tape·관측노이즈 tape를 seed별로 미리 뽑아 **모든 arm이 공유**.
arm 간 차이는 오직 **제거 결정** 뿐 → paired Δ가 선택규칙만 격리한다.

---

## 2. arm 구성 (예산 동일 · control ≥2)

| arm | 규칙 | 제거수 |
|---|---|---|
| **exp_eff** | argmin `eff_hat` (주 실험 arm) | 24 |
| exp_ros | argmax `ros_hat` (F4 기준) | 24 |
| exp_or | **카드 문자 그대로**: {eff_hat<0.6 **OR** ros_hat>1.3} 마킹 → 마킹 중 worst-eff 제거 (마킹 0이면 무정보 → 랜덤 fallback) | 24 |
| **c1_none** | 제거 없음 (카드가 요구한 null) | 0 |
| **c2_random** | 균일 랜덤 제거 — **동일 개수·동일 스케줄·동일 용량재분배·동일 연산** | 24 |
| c3_anti | argmax `eff_hat` (부호 통제 — 신호가 있으면 random보다 **나빠야** 함) | 24 |
| oracle_h | argmin **진짜 latent h** (천장 · PASS용 control 아님) | 24 |

**controls_fair = TRUE.** c2_random은 실험 arm과 제거 개수/시점/용량재분배/연산예산이 완전히 동일하고,
난수 tape도 공유한다. c1_none만 제거수 0인데 이것은 카드 §3이 명시한 **null baseline**이다.
(그리고 아래 validity check가 보여주듯 c2 ≈ c1이라 null이 불리하지도 않다.)

---

## 3. 📉 v0 = INVALID (숨기지 않고 기록)

첫 실행(사전등록 손상상수 `P_HIT=.004, K_WEAR=.002, ROS0=1.0`)은 **기질 전체 붕괴**였다:

| arm | exp_eff | exp_ros | exp_or | c1_none | c2_random | c3_anti | **oracle_h** |
|---|---|---|---|---|---|---|---|
| eff_final | 0.0501 | 0.0501 | 0.0501 | 0.0501 | 0.0502 | 0.0500 | **0.0502** |

ROS death-spiral이 **모든 유닛을 H_FLOOR(0.05)로** 삼켰다. **latent 진실을 보는 oracle조차 metric을 못 움직인다**
→ 계측기의 dynamic range = 0 → 이 cell에서는 PASS도 THEATER도 읽을 수 없다 = **INVALID**.

**재보정은 arm 기준을 건드리지 않았다** (tune-to-green 아님). 실험 arm을 일절 언급하지 않는
**arm-blind 규칙**만 썼다: *"c1_none(무제거) pool의 최종 latent health mean ∈ [0.35,0.75] AND std ≥ 0.10"*
(= pool이 부분적으로 손상되고 **분산이 실재하는** 유일한 regime — QC가 의미를 가질 수 있는 조건).
`calib_scan.py`가 24 cell 스캔 → LIVE 4개 → **중앙값 cell** 채택: `P_HIT=.0005, K_WEAR=.0005, ROS0=1.5`.
이후 **V1 liveness gate**를 코드에 상주시켰다 (c1 health spread + oracle headroom > 5×margin).

> **부수 발견:** 미토파지에는 **작동 범위(operating envelope)** 가 있다. 손상률이 "용량을 건강한 쪽으로
> 집중시키는 능력"을 앞지르면 QC로도 pool을 구할 수 없다 (v0 = 그 바깥).

---

## 4. 📊 본 결과 (nominal cell · 8 seed · V1 LIVE: c1 mean_h=0.505 std_h=0.273 · oracle Δ=+0.162)

**metric = eff_final** = 최종 300 step(제거 종료 후 정상상태)의 시스템 효율 = Σ(load·h)/Σ(load).

| arm | eff_final | ±std | **Δ vs max(c1,c2)** | seeds+ | 제거된 유닛의 평균 h | oracle 대비 포착률 |
|---|---|---|---|---|---|---|
| **exp_eff** | **0.7110** | 0.0365 | **+0.1590 ± 0.0185** | **8/8** | 0.456 | **98.2%** |
| exp_or (카드 문자) | 0.7115 | 0.0362 | +0.1595 ± 0.0177 | 8/8 | 0.460 | 98.5% |
| exp_ros (F4) | 0.6720 | 0.0374 | +0.1200 ± 0.0237 | 8/8 | 0.521 | 74.1% |
| c1_none | 0.5381 | 0.0373 | — | — | — | — |
| c2_random | 0.5414 | 0.0444 | — | — | 0.696 | — |
| c3_anti (부호통제) | 0.4219 | 0.0506 | **−0.1301** | 0/8 | 0.887 | — |
| oracle_h (천장) | 0.7138 | 0.0373 | +0.1619 | 8/8 | 0.458 | 100% |

**PASS 판정** (사전등록: Δ vs max(c1,c2) > margin 0.02 AND mean−std > 0 AND V1 LIVE):
→ **exp_eff: PASS** (+0.1590, mean−std = +0.1405 > 0, 8/8 seed).

### 결정적 validity check — Δ는 전부 *선택*에서 나온다
```
c2_random − c1_none = +0.0033 ± 0.0308   (≈ 0)
```
**제거 그 자체는 완전히 중립이다.** 랜덤 제거는 무제거와 통계적으로 구별되지 않는다
(용량재분배가 mass-conserving이므로 기대 mean health가 안 변함). 따라서 exp_eff의 +0.159는
"제거/재분배라는 개입"이 만든 게 아니라 **오직 손상신호에 의한 선택**이 만든 것이다.
c3_anti가 −0.130으로 **부호가 뒤집히는 것**도 같은 결론을 이중확인한다 (신호 방향 실재).

### 노이즈 sweep — 효율신호는 견고, ROS는 무관
| σ_obs | 0.00 | 0.15 | **0.30** | 0.60 | 1.20 | 2.40 |
|---|---|---|---|---|---|---|
| Δ exp_eff | +0.161 | +0.159 | **+0.159** | +0.148 | +0.133 | +0.083 |
| Δ exp_ros | +0.120 | +0.120 | **+0.120** | +0.120 | +0.120 | +0.120 |

exp_eff는 관측노이즈가 8배로 커져도 **양수를 유지하며 완만히 열화**(gracefully degrade). ROS는 eff 관측량을
쓰지 않으므로 σ_obs에 불변 — 교차검증으로 두 채널이 독립임을 확인.

### 수요 이질성 sweep — **ROS confound 실증** (사전등록 예측 적중)
| σ_demand | 0.00 | 0.25 | **0.50** | 1.00 |
|---|---|---|---|---|
| Δ exp_eff | +0.163 | +0.162 | **+0.159** | +0.141 |
| Δ **exp_ros** | **+0.168** | +0.147 | **+0.120** | **+0.106** |

수요가 균일하면(σ_d=0) ROS는 **oracle과 사실상 동급(+0.168)** — h의 완벽한 단조 readout이기 때문.
그러나 수요가 비균일해질수록 **단조 감소**: healthy하지만 고수요인 organelle이 높은 ROS를 뿜어
**거짓 양성으로 도살**된다. 이것이 사전등록한 demand confound이며 그대로 관측되었다.

---

## 5. 🔎 카드에 대한 부분 반증 (정직하게)

### (a) 카드 문자 그대로의 OR 손상정의 = **잉여 래퍼(no-op)**
`{eff_hat < θ_e OR ros_hat > θ_r}`의 **마킹 비율 = pool의 43.2%**, 마킹된 event 비율 = 100%.
worst-eff 유닛은 (mean h ≈ 0.5이므로) **사실상 항상 θ_e 아래 = 항상 마킹 집합 안**에 있다.
⟹ **exp_or ≡ exp_eff** (Δ 차이 = 0.0005, margin 0.02의 1/40). **OR의 ROS 항은 아무것도 기여하지 않는다.**

### (b) ROS 단독은 효율보다 **엄격히 열등**
+0.120 vs +0.159 (oracle 포착률 74% vs 98%). 제거된 유닛의 평균 h도 0.521 vs 0.456 —
**ROS는 덜 손상된 유닛을 잘못 고른다**. ⟹ **F4 결합은 F3를 돕지 않는다. 희석한다.**
(divergence 문서의 "F2/F3는 F4에 물려 있다"는 위험 랭킹은 **방향이 반대**였다: F3는 F4 없이 더 잘 산다.)

### (c) 반증조건 충족 여부
카드 §3 FAIL 조건 = "directed ≈ random ⇒ 손상 정의 실패 = theater" → **발동하지 않음**.
세 실험 arm 모두 random을 유의하게 이겼다 (+0.159 / +0.160 / +0.120, 전부 8/8 seed).

---

## 6. 왜 GREEN이 아니라 DIRECTIONAL인가 (THEATER 판정 근거)

**THEATER 아님의 근거:** ΔEff ≈ 0이 아니다. +0.159 ± 0.019, 8/8 seed, **2개 control 모두 대비** 양수,
부호통제가 뒤집히고(−0.130), 랜덤제거는 정확히 중립(+0.003)이라 **lift 전량이 선택에서 유래**함이 분리됨.
self-fold(ΔEff≈0)류의 재기술 theater와는 구조적으로 다르다.

**그럼에도 GREEN 아님 — 4가지 정직한 한계:**

1. **engine-native 아님 · 미배선.** numpy toy 시뮬레이션이고 `core/` decode를 통과하지 않았다.
   `a_engine_native_learning` + `a_verified_must_wire` → toy는 최대 **DIRECTIONAL**.
2. **구조적으로 선택이론의 준-동어반복.** 관측량이 결국 *채점되는 바로 그 양*(h)의 노이즈 readout이므로,
   "노이즈 낀 readout으로 선택하면 랜덤보다 낫다"는 것 자체는 놀랍지 않다. 이 probe가 진짜로 확립한 것은
   **카드의 반증조건이 발동하지 않았다 = 손상정의가 degenerate하지 않다**는 **음성의 부재**이지,
   "미토파지가 anima에게 무언가를 벌어준다"가 아니다.
3. **레인 내부(within-lane) 승리.** metric(용량가중 latent health)은 organelle 레인 안에서 자기참조적이다.
   **reach·σ·emit 어디에도 닿지 않는다.** "organelle health가 anima의 어떤 능력에 binding하는가"는
   F1(용량제약이 실제로 묶이는가)·F6(희소성이 conjunction을 강제하는가)의 몫이며 **여기서 미검증**이다.
   divergence 문서 자신의 경고대로 — *"F6 없는 F1 = bookkeeping"* — F3의 lift는 실재하지만
   **시스템 수준에서는 여전히 bookkeeping일 수 있다.** 이것이 남은 진짜 theater 리스크의 위치다.
4. **작동범위 의존.** v0가 보여주듯 손상률이 임계를 넘으면 oracle조차 무력 → QC의 효과는 regime 조건부.

## 7. p5 경계

**p5_clean = TRUE.** 이 probe에는 **emit이 아예 존재하지 않는다.** emit gate·decode 레인·cell-pool mitosis
레인 어디에도 접촉하지 않았고, ATP/health가 emit 결정으로 흐르는 배선이 0이다
(`speak()` 없음, `if ATP < k: silence` 류 하드코딩 게이트 없음). organelle 레인은 완전 DISJOINT.

## 8. NEXT (F3 자체는 더 팔 게 없다)

- F3의 카드 질문은 **닫혔다**: directed > random 확정, OR/ROS 항은 잉여·열등으로 확정.
- 진짜 load-bearing한 다음 질문은 F3가 아니라 **F1/F6**: organelle 효율이 **downstream 능력(reach/σ)에
  binding하는가**. 거기서 ΔEff≈0이면 organelle 레인 전체(F2/F3/F10 포함)가 시스템 수준 bookkeeping으로
  강등된다. F3의 +0.159는 그 전제조건을 통과시켰을 뿐이다.
- F4는 **격하 권고**: ROS는 F3에 대해 효율보다 열등한 신호임이 실측됨(74% vs 98%, demand confound).
