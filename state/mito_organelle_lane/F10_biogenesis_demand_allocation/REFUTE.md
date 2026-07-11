# REFUTE — H_9282 / F10 적대적 검증 노트

- **대상:** `RESULT.md` (verdict 🟡 DIRECTIONAL-POSITIVE · controls_fair=true · p5_clean=true)
- **검증자 판정:** **REFUTED = TRUE** — 메커니즘(“load 신호는 실제 정보를 나른다”)은 내가 추가한 더 강한 control 앞에서도 **살아남았다**. 그러나 보고서의 **판정 라벨과 두 개의 load-bearing 정량 주장**(“material 이득은 특화에만” · “헤드룸이 구조적으로 극소 ⇒ 승격 근거 약함”)은 **반박된다**.
- **재실험 코드:** `scratchpad/refute_f10.py` (원 `run.py` 기질 1:1 복제 · arm 추가/knob 변형만) · numpy · 결정적 · 동일 seed 0–4 · paired stream.

---

## 0. 체크리스트 1차 통과 항목 (반박 실패 = 원 보고서 정당)

| # | 항목 | 결과 |
|---|---|---|
| 1 | control 동일 예산 | ✅ 코드 확인. `target_from_weights`는 Σ=C_TOTAL 보존, EXP/c1/c2/c3 모두 Σc=19.2. c2/c3는 `apply_matched`로 EXP의 **epoch별 이동질량을 정확히 상속**(`run_arm._exp_masses`, seed마다 `del` 후 EXP 선행 실행 → 누수 없음). floor·renorm 클램프는 convex step이라 실질 no-op. EXP의 유일한 추가 자원 = load 신호. **INVALID 아님.** |
| 3 | held-out / 누수 | ✅ EXP의 EMA는 **서비스 후** 갱신(`ema += EMA_A*(dem[t]-ema)`)되고 재할당은 epoch 경계에서 과거 EMA만 사용 = 인과적. lookahead는 ORACLE(`dem[t:t+EPOCH]`)뿐이고 control이 아니라고 명시. **누수 없음.** |
| 4 | Δ가 seed 분산 안? | ✅ 아님. Δthr=+0.0080±0.0014, per-seed 5/5 양성. |
| 5 | p5 위반 | ✅ 없음. emit/silence/speak/tension에 배선 0 (독립 MoE 토이). 하드코딩 emit gate 부재. |
| 6 | tune-to-green 흔적 | ✅ 없음. sweep에서 static(+0.0165)이 유일 PASS 셀인데 **primary를 static으로 갈아끼우지 않았고** 미달을 그대로 보고. 정직함은 인정. |

### 추가 control로도 못 죽인 것 — c3b (FIXED-PERM shuffled-load)
원 c3는 **매 epoch 새 치환**이라 목표가 thrash → gini 0.049로 붕괴. 즉 “동일 동역학, 대응만 파괴”가 아니라 **지속성까지 파괴**된 약한 control이었다. 그래서 **전 구간 고정 치환**(지속적 misaligned dispersion · 동량 · **gini 0.166 = EXP와 동일**)인 `c3b`를 만들어 붙였다.

| arm | thr | purity | gini |
|---|---|---|---|
| EXP | 0.5667±0.0005 | 0.3302 | 0.166 |
| c1 uniform | 0.5585±0.0017 | 0.2920 | 0.000 |
| c3 shuffled (원) | 0.5586±0.0016 | 0.2933 | 0.049 |
| **c3b fixed-perm (신규)** | **0.5558±0.0016** | 0.2948 | **0.166** |
| ORACLE | 0.5700±0.0004 | 0.3411 | 0.174 |

→ dispersion을 EXP와 **동일하게 맞춘 misaligned arm은 균일보다 오히려 나쁘다**(0.5558 < 0.5585). Δthr vs (3 control + c3b) = **+0.0080 ± 0.0012 그대로**. **⇒ “FORM(차등화 자체)이 아니라 load-정렬만이 성과를 산다”는 원 주장은 내 더 강한 control에서도 유지된다. 체크리스트 2(tunable FORM)로는 죽지 않는다.**

---

## 🔴 1. 반박 1 — 사전등록 THEATER 룰이 **발화했는데** 라벨을 바꿔 달았다 (goalpost move)

`run.py` 헤더의 **실행 전 고정** 룰:
```
PASS   : Δthr(vs best ctrl) mean > +0.010  AND 전 seed > 0
THEATER: |Δthr vs c1_uniform| < 0.010
```
관측: Δthr = **+0.0080** (PASS ❌) · |Δ vs c1| = **+0.0082 < 0.010** → **THEATER 룰 발화(✅)**.

사전등록 룰에는 “단, shuffle control이 붕괴하면 예외” 조항도, “purity가 크면 예외” 조항도 **없다**. 보고서는 판정 후 THEATER를 “실질 정의(ΔEff≈0)”로 **재정의**하고, **사전등록 바가 아예 없는 2차 지표(purity)**를 판정 근거로 승격시켜 DIRECTIONAL-POSITIVE를 회수했다. 이것은 결과를 보고 나서 결정 규칙을 갈아끼운 것 = **사후 목표 이동**이며, `p7`/no-tune-to-green 규율이 금지하는 바로 그 동작이다. 원 코드 헤더를 SSOT로 읽으면 primary metric의 판정은 **THEATER**다.

## 🔴 2. 반박 2 — 유일하게 남은 “material” 근거인 purity 이득의 **과반이 composition(Simpson) 아티팩트**

`purity = Σ_e w_e · p_e` (w_e = expert별 served-mass 지분, p_e = expert 내부 최빈-mode 점유율). EXP는 **hot expert에 용량을 몰아준다 → 애초에 입력이 순수한 expert 쪽으로 served mass가 재가중**된다. 어떤 expert도 더 특화되지 않아도 aggregate purity는 오른다.

seed-paired 분해 (EXP − c1, 5 seed):

| 성분 | 값 | 의미 |
|---|---|---|
| **BETWEEN** (재가중만, p_e 고정) | **+0.0208 ± 0.0032 (6.5σ)** | **composition 아티팩트 — 54%** |
| WITHIN (내부 순도만, w 고정) | **+0.0133 ± 0.0065 (2.0σ)** | 진짜 “특화” — 35% |
| INTER | +0.0042 ± 0.0014 | 11% |
| 합 | +0.0382 | 보고된 “상대 +12%” |

⇒ 보고서의 **“특화 +12% 상대 · 8.0σ · material”**은 **절반 이상이 서비스 질량 재가중**이다. 실제 per-expert 특화(WITHIN)는 **+0.0133 = 상대 +4.6% · 2.0σ**로 격하된다. 게다가 “상대 %” 비교 자체가 분모 트릭이다: 동일한 단일 사건(top-2 spillover 감소)을 baseline 0.29짜리 purity로 재면 +12%, baseline 0.56짜리 throughput으로 재면 +1.4%로 보인다. **두 지표는 독립 축이 아니라 같은 메커니즘의 두 눈금**이다(Δtop1_hit = +0.0154가 둘을 동시에 구동). 사전등록 바를 놓친 primary를, 바가 없고 절반이 confound인 2차 지표로 구제한 셈.

## 🔴 3. 반박 3 — 보고서의 “진짜 발견”(**헤드룸이 구조적으로 극소**)은 **정당화 없는 knob 아티팩트**

보고서 §4: *“벽은 정책이 아니라 헤드룸이다 … oracle조차 +2.1% … F10 단독 GPU spend 권장하지 않는다.”*
그런데 throughput의 하드 천장은 설계상 **C/B = SCARCITY = 0.60**이고, 균일 할당이 이미 그 **93%**를 먹는다. “헤드룸 극소”는 발견이 아니라 **SCARCITY=0.6 + top-2 spillover ON이라는, 사전등록되지 않은 두 상수의 산술적 귀결**이다. 두 상수를 (동등하게 임의적인) 이웃 값으로 바꾸면 **같은 정책 · 같은 control이 사전등록 PASS 바를 넘는다**:

| 셀 (h=400 · seed·control 동일) | Δthr vs best-ctrl | oracle 헤드룸 | 사전등록 판정 |
|---|---|---|---|
| 원 primary (scarcity .6 · spillover ON) | +0.0080 ± 0.0012 | +0.0115 | ⚠️ THEATER-밴드 |
| **spillover OFF** | **+0.0168 ± 0.0015** | +0.0240 | 🟢 **PASS** |
| **scarcity 0.9** | **+0.0118 ± 0.0027** | +0.0199 | 🟢 **PASS** |
| scarcity 0.3 | +0.0011 ± 0.0003 | +0.0017 | 🔴 THEATER |

⇒ **PASS/THEATER 라벨 자체가 tunable하다.** 게다가 원 셀의 사전등록 바(+0.010)는 **lookahead ORACLE 헤드룸(+0.0115)의 87%**를 요구한다 — **어떤 인과적 정책도 도달 불가능한 바**다(scarcity 0.3에선 oracle의 606%). 도달 불가능한 바에 대한 “미달”은 가설에 대한 정보를 **0** 만큼 준다. 결론: “구조적으로 극소”는 substrate 캘리브레이션에 대한 진술이지 **수요주도 biogenesis에 대한 진술이 아니다**. 이 셀은 throughput 축에서 **판정 불능(under-powered)**이고, 그 위에 얹힌 “303M 승격 근거 약함 / F10 단독 spend 비권장”이라는 **정책 권고 역시 근거를 잃는다**(반대 방향 knob에선 PASS가 나온다).

---

## 4. 종합

| 원 결론 조각 | 검증 |
|---|---|
| “THEATER가 아니다 — shuffled-load 붕괴 + null-env Δ→0 ⇒ load 신호가 실제 정보를 나른다” | ✅ **반박 실패(=유지)**. dispersion까지 EXP와 맞춘 신규 c3b(gini 0.166)조차 균일 아래로 떨어짐. 메커니즘은 earned. |
| “사전등록 바 미달(+0.80%p) = throughput은 THEATER-밴드” | ⚠️ 관측은 맞으나 **그 라벨을 붙인 뒤 DIRECTIONAL-POSITIVE로 회수한 것이 규칙 위반**. 또 바 자체가 oracle의 87% = 도달 불가 → 미달이 정보가 아님. |
| “material한 이득은 특화(purity +12% 상대)에만” | 🔴 **반박**. purity Δ의 **54%가 served-mass 재가중(composition)**. 진짜 per-expert 특화는 +4.6% 상대 · **2.0σ**. purity는 throughput과 독립 축도 아님(같은 spillover 사건). |
| “oracle조차 +1.2%p ⇒ 헤드룸이 **구조적으로** 극소 ⇒ 승격/spend 비권장” | 🔴 **반박**. spillover OFF(+0.0168)·scarcity 0.9(+0.0118)에서 **같은 정책이 사전등록 PASS**. 헤드룸은 구조가 아니라 **사전등록되지 않은 knob 2개**. |
| controls_fair=true | ✅ 유지 (c2/c3 이동질량 강제 일치 · 총용량 동일 · paired stream). c3의 “동일 동역학” 문구만 부정확(지속성도 파괴됨 → c3b가 올바른 형태). |
| p5_clean=true | ✅ 유지. emit 배선 0. |

**최종 판정: 🟡 DIRECTIONAL-POSITIVE (tier는 유지) · refuted = TRUE.**
메커니즘(load-정렬 할당 > 균일/랜덤/dispersion-matched-misaligned)은 진짜이고 내 추가 control에도 죽지 않는다. 하지만 **보고서가 그 tier를 얻어낸 경로**(사전등록 THEATER 룰 발화 → 바 없는 2차 지표로 회수)와 **두 개의 정량 결론**(특화 materiality · 구조적 저-헤드룸 ⇒ 비승격 권고)은 각각 **composition confound**와 **knob 아티팩트**로 무너진다. 살아남는 문장은 오직 하나:

> *“이 토이에서 관측 load 신호는 균일/랜덤/동량-misaligned 할당 대비 용량 정렬을 유의하게 개선한다 (Δthr +0.0080±0.0012, 4 control 통과, null-env 0).”*
> 여기에 붙은 “헤드룸은 구조적으로 작다 / 이득은 특화에 있다 / 승격하지 마라”는 **전부 이 기질의 미정당화 상수(SCARCITY·spillover)와 aggregate 가중 정의에서 나온 것이며, 데이터가 뒷받침하지 않는다.**

**후속 필수 조건**(재판정하려면): ① SCARCITY·spillover를 사전등록 축으로 올려 achievable-headroom 대비 **정규화된 바**(예: oracle 회수율 ≥ X%)로 다시 걸 것 — 절대 %p 바는 이 기질에서 무의미. ② purity를 쓸 거면 **WITHIN 성분(w 고정)** 만 사전등록 지표로 쓸 것. ③ c3는 **fixed-perm(c3b)** 로 교체 — 원 c3는 dispersion까지 죽여서 EXP에 유리하게 편향된 약한 control이다(비록 결론은 안 뒤집혔지만).
