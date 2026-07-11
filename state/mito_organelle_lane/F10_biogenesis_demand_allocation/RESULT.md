# H_9282 / F10 — 생합성(PGC-1α) · 수요주도 organelle 할당 · $0 numpy probe 결과

- **tier:** 🟡 **DIRECTIONAL-POSITIVE (약함 · 저-헤드룸)** — toy, engine 미배선 (`a_toy_scale_recheck` → 최대 등급 DIRECTIONAL)
- **run:** `run.py` · numpy only · torch 0 · wall **6.6s** · 5 seed (0–4) · 결정적
- **raw:** `result.json`
- **p5:** ✅ CLEAN — emit gate 무접촉. 이 probe 는 표현형성 단계(어떤 유닛이 발화 가능 = 호흡용량 c_e)만 건드리며 emit/silence/speak() 에 배선 0.

---

## 1. 한 줄 결론

**수요주도 biogenesis 는 THEATER 가 아니다 — load 신호는 실제 정보를 나른다(shuffle 통제로 붕괴, null-env 에서 소멸). 그러나 throughput 레버로서의 총 헤드룸이 구조적으로 극소다: 완벽한 oracle(lookahead)조차 균일 할당 대비 +1.2%p(상대 +2.1%)밖에 못 얻고, 수요주도는 그 헤드룸의 71%를 이미 회수한다. 사전등록 throughput 바(+1%p)는 미달(+0.80%p) = THEATER-밴드. 반면 특화도(purity)는 material 하게 상승(+0.035, 상대 +12%, 전 seed 양성). ⇒ "부하 신호가 유용 할당을 못 알린다"는 Null 은 반증되었으나, 이 기질에서 얻을 게 별로 없다.**

---

## 2. 기질 · arm 설계 (동일 예산)

- E=16 expert(MoE-유사) + 각 옆에 organelle 호흡용량 `c_e`. **Σc_e = C = 0.6·B = 19.2 고정(보존)** → 수요의 60%만 감당 = 용량이 항상 **binding**.
- step 당 B=32 토큰, 잠재 mode π_t(drift AR(1)) → top-1 라우팅, 용량 없으면 **top-2 spillover**, 둘 다 없으면 DROP.
- 재할당 epoch=25 step, EMA(load) half-life=50 step, floor=5%(사멸 방지).

| arm | 할당 규칙 | 총용량 C | 이동질량(turnover) | 쓰는 신호 |
|---|---|---|---|---|
| **EXP** | 관측 demand EMA 에 비례 (PGC-1α) | **동일** | 기준 | load |
| **c1 균일** | c_e = C/E 고정 (동역학 없음) | **동일** | 0 | 없음 |
| **c2 랜덤(동량)** | 매 epoch 랜덤 Dirichlet target | **동일** | **EXP 와 정확히 일치** | 없음 |
| **c3 shuffled-load(동량)** | EXP 와 동일 규칙, load 벡터만 permute | **동일** | **EXP 와 정확히 일치** | 파괴된 load |
| *ORACLE* | 다음 epoch 실제 demand lookahead | 동일 | — | *상한 참조(control 아님)* |

**공정성:** control 3개 전부 EXP 와 **총용량 동일**, c2/c3 는 **이동질량까지 강제 일치**. EXP 가 추가로 쓰는 건 오직 *load 신호*뿐 — 파라미터/예산 우위 없음. 스트림은 arm 간 완전 공유(paired). ⇒ `controls_fair = TRUE`.

---

## 3. PRIMARY CELL (사전등록 조건: drift half-life h=400 = 카드의 "지속 고부하")

mean±std over 5 seeds.

| arm | throughput (BIND) | purity=특화 (BIND) | gini(c) (FORM) | corr(c,demand) |
|---|---|---|---|---|
| **EXP 수요주도** | **0.5667 ± 0.0005** | **0.3302 ± 0.0111** | 0.166 | **+0.396** |
| c1 균일 | 0.5585 ± 0.0017 | 0.2920 ± 0.0148 | 0.000 | +0.000 |
| c2 랜덤(동량) | 0.5581 ± 0.0024 | 0.2950 ± 0.0152 | **0.081** | +0.030 |
| c3 shuffled(동량) | 0.5584 ± 0.0017 | 0.2929 ± 0.0149 | 0.050 | +0.002 |
| *ORACLE (상한)* | *0.5700 ± 0.0004* | *0.3411 ± 0.0111* | *0.174* | *+0.488* |

**Δ (seed-paired)**

| 신호 | Δ vs best-control | Δ vs c1 균일 | 전 seed 양성? | oracle 헤드룸 회수율 |
|---|---|---|---|---|
| throughput | **+0.0080 ± 0.0014** (5.7σ) | +0.0082 ± 0.0013 | ✅ 5/5 | 0.0082/0.0115 = **71%** |
| purity(특화) | **+0.0352 ± 0.0044** (8.0σ) | +0.0382 | ✅ 5/5 | 0.0382/0.0491 = **78%** |

per-seed Δthr = [+0.0084, +0.0081, +0.0102, +0.0058, +0.0077]

### 🔑 FORM vs BIND 해리 (측정 메타법칙 실증)
`c2 랜덤` 은 **gini=0.081 로 "특화된 것처럼 보이지만"**(FORM = 차등 할당 존재) throughput +0.000 / purity +0.003(=노이즈). **차등화 그 자체는 공짜(tunable)이고, load-정렬된 차등화만 성과를 산다(earned).** gini 를 지표로 삼았다면 랜덤 arm 이 "성공"으로 보였을 것 — 값이 아니라 Δ vs control 을 본 이유.

---

## 4. 사전등록 판정 규칙 대조 (tune-to-green 없음 · 규칙은 실행 전 `run.py` 헤더에 고정)

| 규칙 | 기준 | 관측 | 충족 |
|---|---|---|---|
| PASS | Δthr(vs best ctrl) mean > **+0.010** AND 전 seed >0 | **+0.0080**, 5/5 양성 | ❌ **매그니튜드 미달** (방향/일관성은 충족) |
| THEATER | \|Δthr vs c1\| < 0.010 | +0.0082 | ⚠️ **밴드 안** |
| KILL | Δ < −0.010 | +0.0080 | ❌ 해당없음 |
| ARTIFACT-GUARD (NULL-ENV) | 균일수요 환경에서 EXP>ctrl 이면 INVALID | Δthr = **+0.0001 ± 0.0001**, Δpurity = +0.0004 | ✅ **통과 — 특화할 것이 없으면 이득 0** (측정 게임 아님) |

**⇒ throughput 사후판정 = THEATER-밴드(사전등록 바 미달).** 그러나 **THEATER 의 실질 정의("부하 신호가 유용 할당을 못 알린다 / ΔEff≈0")는 반증**된다:
1. **c3 shuffled-load**(동일 동역학·동일 이동질량·load 대응만 파괴)가 c1 균일 수준으로 **완전 붕괴**(0.5584 vs 0.5585) → 이득은 *동역학* 때문이 아니라 **load 신호의 내용** 때문.
2. **NULL-ENV**(균일 수요)에서 Δ→0.0001 → 이득은 측정 아티팩트가 아니라 **실제 수요 비균일성의 활용**.
3. purity Δ 는 8σ, 전 seed 양성, 상대 +12% = **material**.

**진짜 발견: 벽은 정책이 아니라 헤드룸이다.** oracle(완벽 예지)조차 균일 대비 throughput 을 +0.0115(상대 +2.1%)밖에 못 올린다. top-2 spillover 가 용량 부족을 흡수해 `min(load, c)` 의 오목성을 죽이기 때문. 즉 이 기질에서 **할당 최적화의 총 상금이 애초에 작고**, 수요주도는 이미 그 상금의 71–78%를 회수 중이다. 정책을 더 조여도 (tune-to-green 해도) 최대 +0.3%p 남는다.

---

## 5. SWEEP (2차 특성화 · 판정 미사용) — 언제 THEATER 로 붕괴하는가

drift half-life h = demand 지속성. EMA half-life 50 + epoch 25 = **할당 지연 ≈ 75 step**.

| h (demand 지속성) | EXP thr | c1 thr | Δthr vs best-ctrl | Δpurity | 판정(사전등록 바) |
|---|---|---|---|---|---|
| 25 (지연보다 빠른 drift) | 0.5589 | 0.5581 | **+0.0007 ± 0.0005** | +0.006 | 🔴 **THEATER** |
| 100 | 0.5622 | 0.5579 | +0.0042 ± 0.0010 | +0.028 | 🟡 밴드 내 |
| **400 (PRIMARY)** | 0.5667 | 0.5585 | +0.0080 ± 0.0014 | +0.035 | 🟡 밴드 내 |
| 1600 | 0.5702 | 0.5603 | +0.0095 ± 0.0012 | +0.037 | 🟡 밴드 경계 |
| static (drift 없음) | 0.5709 | 0.5540 | **+0.0165 ± 0.0068** | +0.035 | 🟢 **PASS** |

**경계조건(정량화):** 수요주도 biogenesis 는 **demand 지속성 > 할당 지연**일 때만 값을 낳는다. h=25(지연보다 빠름)에서 Δ→+0.0007 = 완전 THEATER. 카드의 "**지속** 고부하" 전제는 장식이 아니라 **작동 필요조건**이었다.
⚠️ 정직 고지: 사전등록 PASS 바(+1%p)를 넘는 셀은 **static(drift 0) 하나뿐**이다. primary 셀을 static 으로 갈아끼우지 **않았다**(= tune-to-green 금지).

---

## 6. 반증조건 충족 여부 (카드 §3)

| 항목 | 카드 기준 | 결과 |
|---|---|---|
| PASS | Δ throughput/특화 > 두 control | throughput: 두 control 모두 초과하나 매그니튜드 미달 / **특화: 두 control 모두 material 초과 ✅** |
| FAIL(theater) | 수요주도 ≈ 균일 | ❌ 해당 안 됨 (5.7σ/8.0σ, shuffle·null 통제 통과) — **단 h≤25 에서는 해당됨** |

**Null("부하 신호가 유용 할당을 못 알린다") = 반증됨.** 신호는 유용하다. 다만 이 기질에서 **유용함의 총량이 작다**.

---

## 7. 판정 및 후속

- **verdict: 🟡 DIRECTIONAL-POSITIVE (low-headroom)** — mechanism 은 진짜(earned, 통제 3종 통과)지만 throughput 임팩트가 사전등록 materiality 바 미달. 특화(ρ·fan/σ·carve 접점)에서만 material.
- **GREEN 아님:** toy · engine 미배선 · 사전등록 throughput 바 미달 (`a_verified_must_wire` 미충족).
- **THEATER 아님:** ΔEff ≉ 0 이고 shuffled-load control 이 붕괴하는 것이 결정적 증거.
- **후속 판단 (스코프 정직):** 이 레인을 303M 으로 승격할 근거는 **약하다** — oracle 상한이 +2% 라면 engine-native 에서도 상금이 작다. F10 의 값어치는 독립 레버가 아니라 **F6(용량제약 결합압력)의 전제 공급자**다: F10 은 "용량 캡을 *어디에* 둘지"를 load-신호로 정하는 게 (랜덤/균일보다) 유의미함을 보였고(특화 +12%), F6 의 진짜 베팅(희소성이 conjunction 을 강제)은 여기서 측정하지 않았다. **F10 단독 GPU spend 는 권장하지 않는다.**
- 재현: `OMP_NUM_THREADS=2 python3 run.py` (6.6s).
