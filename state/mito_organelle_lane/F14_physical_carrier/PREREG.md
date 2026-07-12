# PREREG — H_9287 / F14 · Ω 물리담체 **확증 런** (6th fire)

**동결 시각**: 2026-07-12 (데이터 보기 전 · 실행 전)
**코드 sha256** (`run.py`, 동결본):

```
21ca4d1cf742d3a9b52f680e9204159a78536d928d27457d4854e5131671dec3
```

이 sha 이후 detector·판정변수·마진·arm·seed 를 바꾸지 않는다(계측규칙 ⑨). 실행 후 재-sha 로 일치 확인.

---

## 0. 물음

**재조합(merge) 대수가 *물리* 정보를 더하는가 — 그리고 그것은 *국소* 관측으로 도달가능한가?**
(H_054 symbiogenesis · H_203 asym-merge 의 미답 물음. F2 에서 5발 전부 INVALID.)

5차 = **존재 증명**(오라클이 LIVE 에서 총 supply 를 실제로 올린다). 6차 담체 도출(Fable, `DERIVATION.md`)
= **정리 + TOP-1 담체**. 이 런은 그 담체가 **확증 seed 에서 재현되는가**를 사전등록으로 묻는다.

## 1. 담체 (DERIVATION.md TOP-1 · `Ω_k` RELAX-k)

```
Ω_k(i,j) = R_k(cap_i+cap_j, L_i+L_j, Λ_ij ; S_i+S_j) − R_k(cap_i,L_i,Λ_i;S_i) − R_k(cap_j,L_j,Λ_j;S_j)
R_k :  S ← S0, k회 반복   S ← cap·c / ( r(Λ, L/S) + c )
r(Λ,st) = Λ·(1 + B1·clip(st−1, 0, EXC)) ,  c = G·(1 − e^−repair) ,  Λ_ij = (L_iΛ_i + L_jΛ_j)/(L_i+L_j)
```

- **국소**: `(cap,L,S,Λ)_{i,j}` 만. 전역상태·미래 미사용. `min()` **없음** ⇒ 장부 껍질 없음, DV 에 직접 정렬.
- **정리**: 융합은 `S=cap−D` 를 정확히 보존 ⇒ `ΔS|_t ≡ 0` ⇒ **순간 관측 담체는 정의상 장부의 함수**.
  ⇒ **`Ω_0 ≡ 0`, `Ω_1` 이 첫 비소멸 차수.** (코드가 `Ω_0` max|·| 을 실측 출력해 정리를 자체검사한다.)
- 장부 비항등식은 **정의역**으로 증명: `detgrad`는 `(L,S)`만의 함수(`∂/∂Λ ≡ 0`), `Ω`는 Λ 의존
  ⇒ `Ω = λ·detgrad` 인 λ 부재.

## 2. DV (규칙 ⑪ — 장부형 DV 금지)

| | DV | 방향 |
|---|---|---|
| **PRIMARY (헤드라인)** | warm-mean **supply** = `Σ(cap−D)` — 파티션-불변 물리량 | ↑ |
| **SECONDARY** | warm-mean **overload** = `(stress>1)` 비율 | ↓ |
| ~~제외~~ | 장부 **ATP** = `Σ min(L,S)` — **보고만, PASS 조건 제외** | — |

**`ΔATP > 0` 을 PASS 에서 삭제한다** (5차 대비 변경 ③). HET 에선 Ω 가 **장부를 잃으면서(ΔATP<0)
물리를 딴다**는 것이 도출의 핵심 반례이므로, ATP 부호를 요구하면 참인 담체를 죽인다.
**PASS = `Δsupply > δ` ∧ `Δoverload ≤ 0`** 만.

## 3. ARM (9 필수 + frozen 기저)

| arm | 정책 | 역할 |
|---|---|---|
| `c1_frozen` | 분열/융합 없음 | 기저 |
| `c2_blind` | 균등랜덤 쌍 | 주 control |
| **`a_omega1`** | **Ω_1** | ★ PRIMARY (TOP-1) |
| `a_omega3` | Ω_3 | 차수 |
| `a_omega8` | Ω_8 | **DV-정렬 국소 상한 = 도달성 게이트** (오라클 아님 · 변경 ①) |
| `s_lamperm` | Ω_1(Λ̃) | **Λ-순열 sham**: site `f` 동결순열 `f̃=f[π]` → 동일 질량가중 규칙으로 `Λ̃_i = Σ d_s f̃_s / L_i` 재계산. 융합불변 · 동일 함수형 · 동일 주변분포 · **인과만 절단** (변경 ②) |
| `s_stressshuf` | Ω_1(셔플 상태) | **응력-셔플 sham**: `(cap,L,S)` 삼중항을 eligible 안에서 순열(Λ 는 참) ⇒ 응력-중항 채널 절단. 두 채널 분리 확인 |
| `a_detgrad` | 순간 ΔATP argmax | **장부 기울기 control** |
| `a_comp` | slack 극단매칭 | **반정렬 양성대조** — 5차 PRIMARY. **overload 를 *올려야* 정상** (변경 ④) |
| `o6_oracle` | 평형장부 `min(L,S_eq)` argmax | **비교용 · 상한 아님** |
| `a_omega1_mis` | Ω_1, 상수 오설정 (B1×3, EXC×0.5, c×4) | **모델-전지 배제** 강건성 |

## 4. Seed (오염 0)

- **확증 main = 200–219** · **MDE pilot = 600–619** (분석과 disjoint).
- Fable 파일럿 seed **950–985 와 서로소** ⇒ 파일럿 오염 0. Ω 계열 arm 은 200–219 에서 **未觀測**이다
  (5차는 Ω arm 자체가 없었다).

## 5. MDE (규칙 ③ · 사전계산 · 미달 abort)

- pilot(600–619)에서 `sd(Ω_1 − c2_blind)_supply` → `MDE = (t.975 + t.80)/√20 · sd`.
- **도달성 축 = `Ω_8`** (오라클 금지 — HET 에서 오라클은 눈이 먼다).
- **ABORT**: pilot `(Ω_8 − blind)_supply ≤ 3·MDE` ⇒ `V_POWER=False` ⇒ **INVALID**.

## 6. 게이트 (hard · 헤드라인 detector 그 자체에)

`G1` pump_max ≤ 1e-9 (연산자 자원보존 ⑧) · `G2` self_remerge = 0 · `G3` LIVE band(control 만으로 선등록)
· cap 보존 · n_units 고정 · **`V_info`** (Ω pool std > 0 ∧ 선택쌍 z > 1.0 — 처치 DV 가 control 이 못 보는
입력의 함수 ④) · **`V_sham_valid`** (`pair_match(s_lamperm, Ω_1) < 0.5` — sham 이 진짜로 다른 쌍을 고름)
· **`V_POWER`** (§5) · **`V_REACH`** (`Ω_8 − blind` supply > 1.0 ∧ p<.05).

## 7. 판정 분기 (실행가능 코드 · 데이터 보기 전 확정)

```
hard 실패                                        -> INVALID
PASS := (Ω_1 supply Δ > 1.0 ∧ p<.05) vs **c2_blind ∧ s_lamperm ∧ a_detgrad 셋 다**   (규칙①: control별 paired-t 전부)
        ∧ OVL_OK   (overload vs blind: mean ≤ 0  또는  p ≥ .05  — 즉 악화 없음)
        ∧ SIGN     (부호보존 8축 전 셀에서 Ω_1−blind, Ω_1−lamperm 의 Δsupply > 0)     (규칙⑥ PASS 내장)
        ∧ detgrad_capture(Ω_1) < 0.90                                              (규칙⑪ 장부 항등식 배제)
PASS                                             -> DIRECTIONAL-POSITIVE
¬PASS ∧ TOST(δ=1.0) 등가 (vs blind ∧ vs lamperm)  -> EQUIVALENT-NULL  (담체 부재)     (규칙⑩)
¬PASS ∧ (supply Δ vs blind < −1.0 ∧ p<.05)        -> KILL
그 외                                             -> THEATER
```

**부호보존 8축**: `repair`(live band) · `sigma{0,.5,1}` · `capsplit{sym,load}` · `rho{.7,.85,1}` ·
`frag_sigma{.5,.9}` · `EXC{1,2,6}` · `B1{1.5,3,6}` · `feedback{LIVE,HET}`(두 블록 자체).

**마진**: `DELTA_S = 1.0` (supply · TOST 등가마진 동일) · `DELTA_O = 0.02` (overload) · `ALPHA = 0.05`
· `CAPTURE_MAX = 0.90`.

## 8. 사전 예측 (파일럿 = DIRECTIONAL · 재현 안 되면 정직하게 보고)

- Fable 파일럿(950–985): LIVE `Ω_3` supply **+25.3** (t=20.1), overload **−0.149**; 오라클 +11.9.
  HET `Ω_3` supply +14.05, **ΔATP = −3.08**(장부를 잃으며 물리를 딴다).
- `Ω_1 ≈ Ω_3 ≈ Ω_8` 예측(닫힌 루프가 이완을 대신 iterate). `a_comp` 는 **overload 를 올린다**(반정렬).
- `Ω_1` detgrad-capture ≈ 0.02 (vs `a_comp` ≈ 0.98). capture > 0.90 이면 **장부 항등식**으로 해석.
- 이 lane 은 **파일럿이 seed 특이적이었던 전례**가 있다. 확증 seed 에서 재현 실패 시 그대로 보고한다.
  tune-to-green / tune-to-red 둘 다 금지. 음성·INVALID 도 정당한 결과다.

---

# 개정 (REGATE) — 사전등록 개정판 · **원 런 결과를 본 뒤 · 실행 전 동결**

**개정 코드 sha256** (`run_regate.py`):

```
e5f5e0e3231b7e31d97ef885c0244315e87e8019c71a42ee6800eaaa1adf7f07
```

## 왜 개정하는가 (정직 공시)

원 런(`run.py` sha `21ca4d1c…`, seeds 200–219) 판정 = **INVALID**. 사유는 **교란이 아니라 내가 못박은
hard-gate `V_info` 의 임계값 오설정**이다:

- 사전등록 `V_info = (Ω pool std > 0) ∧ (om_sel_z > 1.0)`. 실측 `om_sel_z = 0.93` ⇒ 미달 ⇒ INVALID.
- 진단(계측기 측 · DV 무관): 짝-pool 크기 ≈ **51쌍**(상한 `√(N−1)≈7.2`)이므로 구조적 불가능은 **아니다**.
  실제 원인은 **Ω 짝-점수 분포의 두꺼운 좌측 꼬리**(나쁜 융합이 크게 음수) — 완벽한 argmax 조차
  pool 평균의 ~0.93σ 위에만 앉는다. **z 임계는 선택강도가 아니라 점수분포의 왜도를 재고 있었다.**
- 원 런 판정 **INVALID 는 그대로 기록에 남는다**(`result.json` · 헤드라인 조건은 전부 충족했으나
  hard-gate 실패 ⇒ 규칙⑨에 따라 사후 완화 금지).

## 무엇만 바꾸는가

**`V_info` 게이트 사양 하나뿐** (규칙④의 본래 의도 = "처치 DV 가 control 이 못 보는 입력의 함수 · 분산>0"):

```
V_info = (Ω pool std > 0)                                # 정보축에 분산이 있다
       ∧ paired-t( selz[Ω_1] − selz[c2_blind] ) > 0, p<.05   # 처치가 그 축에서 비랜덤 선택
       ∧ pair_match(s_lamperm, Ω_1) < 0.5                # 점수가 Λ(=control 이 못 보는 입력)의 함수
```

**바꾸지 않는 것 (한 글자도)**: 헤드라인 DV(supply) · 보조 DV(overload) · 장부 ATP 제외 · 대조군
`{c2_blind, s_lamperm, a_detgrad}` · 마진 `DELTA_S=1.0`/`DELTA_O=0.02`/`ALPHA=.05`/`CAPTURE_MAX=.90`
· TOST 등가마진 · 부호보존 8축 · PASS/EQUIVALENT-NULL/KILL/THEATER 분기 · arm 집합 · 기질 상수.

## tune-to-green 방지

원 런의 seed(200–219) 결과를 **이미 보았으므로** 그 seed 에서 게이트만 갈아끼워 재판정하지 않는다.
개정 런은 **THIRD-disjoint 확증 seed 300–319** (MDE pilot **700–719**)에서 돈다 — 미관측이며
Fable 파일럿 950–985 및 원 런 200–219 / pilot 600–619 와 모두 서로소.
개정 게이트가 완화가 아님을 명시: 새 게이트는 **3조건 결합**(분산 · 비랜덤성 유의 · Λ-의존)으로
원 게이트(단일 z 임계)보다 **검사 내용이 더 많다**.
