# SYNTHESIS — 미토콘드리아 organelle-lane (F1–F11 · H_9273–H_9283)

작성 2026-07-12 · 입력 = 11 패밀리 × (run RESULT.md → 적대적 REFUTE.md) · 전부 $0 numpy toy · engine-native 0

---

## 1. 한 문장 결론

미토콘드리아 organelle-lane은 anima에 **새 reach 능력을 하나도 더하지 못했고(11/11 GREEN 0 · wired 0)**, 실질적으로 더한 것은 (a) **"에너지 예산/희소성이 결합(conjunction)을 강제한다"는 계열의 사망 진단**(F6 KILL — 캡을 조이면 held-out 재조합이 Δ=−0.192로 오히려 무너짐), (b) **단 하나의 재현된 earned 메커니즘 = 외생 수요 → 용량 배분**(F10 Δthr=+0.0080±0.0012 5.7σ, F4-SECONDARY Δfit=+1.472 t=+5.50 — 서로 다른 코드·fitness·control로 독립 재현), (c) **자기 verdict 3개를 무효화한 프로브 설계 결함 census**(order-statistic max-control 편향 · n=5 검정력 · 항진적 처치 arm · 관측량≡채점량 항등식) 세 가지뿐이다.

---

## 2. 전수 표

| 패밀리 | run | refute | **최종** | 핵심 Δ | 한 줄 근거 |
|---|---|---|---|---|---|
| **F1** ATP 대사경제 (H_9273) | THEATER | REFUTED | **INVALID** | Δacc vs c1 = +0.0085±0.0191 (ns) | 축의 전 동적범위(1.12pp) < 유의 문턱(1.71pp) ⇒ 검출력 0. policy_atp가 batch/loss/model을 안 받는 자율 폐루프(주기-3 클럭) ⇒ 처치=static cap의 결정론적 dither = 항진명제. c1≡c2 (per-seed byte-identical). |
| **F2** 분열·융합 (H_9274) | KILL | REFUTED | **INVALID** | −0.359±0.089 (5/5) → 카드충실 규약 재실행 **+0.179 (0/10 음수)** | 부호가 게놈 대수 규약에 의해 결정됨: AND+copy −0.359 / AND+segregate +0.073 / 평균+sym +0.001 / 평균+segregate(카드 등록값) +0.179. run.py는 카드의 "융합=희석·분열=격리"를 부정으로 코딩(복사 분열 = 격리 수학적 불가). |
| **F3** 미토파지 QC (H_9275) | DIR-POS | REFUTED | **THEATER** | +0.159±0.019 (8/8) — 그러나 메커니즘 삭제 시 +0.1645 재현 | P_HIT=0·K_WEAR=0(손상·마모·ROS 전무)인 정적 pool에서 헤드라인 100% 재현 ⇒ '품질관리' 정보 0비트. eff_hat ≡ h ≡ 채점 metric(corr 0.945) = 관측량=채점량 항등식. V1 게이트가 FAIL cell을 전부 INVALID로 배제 ⇒ 출력이 {PASS, INVALID}뿐. |
| **F4** ROS 역행채널 (H_9276) | THEATER | REFUTED | **DIR-POS (SECONDARY) / KILL (PRIMARY)** | z-tonic −1.006 (t=−3.12) · abs-setpoint **+1.472 (t=+5.50)**, vs 최선 상수 null +1.263 (t=+4.86, 25/30) | 신호≠컨트롤러. z=(R−EMA)/σ는 setpoint 없는 자기추적 항등식 → 만성 4배 과부하를 "정상"으로 고착(사망). 절대 setpoint(load==capacity) 배선은 어떤 open-loop 상수도 못 가는 좌표(n=31.6에서 shortfall 0.071) 도달 = earned. emit ΔEff = −0.0005 (t=−0.12) ⇒ ROS ⊥ emit. |
| **F5** mtDNA 계보 병목 (H_9277) | THEATER | SURVIVED | **THEATER** | EXP−C3 = +0.0088±0.0334 (3/6 동전) · EXP−C2 = −0.263 (0/6) | 계보 FORM 만점(herit 0.769 · host_indep 0.872)인데 held-out Δ=0. 새 lineage-only control(C3-PERM, 값분포·자기상관 보존·계보만 파괴)에서도 +0.0053. 계측기 무죄(floor 0.541→ORACLE 0.805, range 0.28). 선택압 없는 계보 = 노이즈 운반체. |
| **F6** 용량압력→conjunction (H_9278) | KILL | SURVIVED | **KILL** | EXP 0.785 vs C1(무제한) 0.977 ⇒ **Δ=−0.192±0.060 (5/5)** | 캡 sweep k=1→64: 0.674/0.785/0.924/0.955/0.967/0.976/0.977 = **단조 하강**(카드 PASS 조건의 정반대). train acc=1.000 = 완벽 fit 후 held-out 붕괴 = 쌍별 암기. floored regime 구제 = ΔEff≈0. V1 oracle 0.943 = 표현력 문제 아님(발견 실패). |
| **F7** 화학삼투 Ψ=½ (H_9279) | KILL | REFUTED | **THEATER** | Ψ*_work 0.892 → **정정 시 0.677**, 올바른 power functional에선 argmax = 정확히 0.50 | w_kin은 work가 아니라 flux(g·ψ·Vm; 힘을 한 번 덜 곱함). 자기 양성대조에서 psi_star_kin=0.95(=grid 경계)로 실패했는데 게이트가 그걸 검사 안 함 = V3 detector-fairness FAIL. Ψ_att는 상수(0.4986 vs iid uniform 0.5006) ⇒ P2는 구조적 반증불가. 살아남는 것은 Q2 동어반복 다리뿐. |
| **F8** 언커플링 발열 (H_9280) | THEATER | REFUTED | **INVALID** | 사전등록 셀 filler = 0.0±0.0 (병도 약도 없음) | θ=P90 vs p_event=0.12>0.10 = 분위수 항등식으로 filler가 0이 되도록 강제됨. 개입 자체가 null(방출질량 0.332 vs θ=0.637). 자기 판정함수가 tune-path 10셀 중 **7셀에서 DIRECTIONAL-POSITIVE를 출력**했고, 사전등록 KILL 변수(true_recall, 최대 하락 0.0349 < 0.10)를 사후에 n_true로 바꿔치기해 KILL을 만들어냄. |
| **F9** Ca 버퍼 urgency (H_9281) | THEATER | SURVIVED | **THEATER** | exp +0.740 vs 무튜닝 EMA +0.913 (0/6) · 동등튜닝 순이득 **+0.007** | 버퍼는 raw urgency를 6/6 이김(+0.167)지만 1-knob 선형 EMA에 0/6 패(leak-free LOO에서도 EMA 6/6 승, +0.173±0.060). knob sweep TQ range [0.573..0.967] = 달성범위 거의 전부를 knob으로 이동 ⇒ FORM tunable. Ca 고유성분(포화)은 순손해. |
| **F10** 수요주도 biogenesis (H_9282) | DIR-POS | REFUTED(부분) | **DIR-POS** | **Δthr = +0.0080±0.0012 (5.7σ, 5/5)** · null-env +0.0001 | c3 shuffled-load(동일 동역학·동일 이동질량, load 대응만 파괴)가 균일 수준으로 완전 붕괴(0.5584 ≈ c1 0.5585) ⇒ lift 전량이 load 정렬. 내가 추가한 fixed-perm c3b(gini 0.166 = EXP 동일)에서도 우위 불변. 다만 (i) 사전등록 THEATER 밴드가 실제 발화했고 보고서가 사후에 purity로 갈아탐(BETWEEN 54% = composition 아티팩트), (ii) PASS/THEATER 라벨 자체가 SCARCITY·spillover knob로 뒤집힘 ⇒ "헤드룸 극소" 결론은 근거 없음. |
| **F11** 이질세포질 세포내선택 (H_9283) | KILL | REFUTED | **THEATER** | FORM: eff +0.0437 (t=+10.65, 20/20) · conj_index +0.0766 (t=+7.28) — BIND: held_conj pooled Δ = **−0.0088 (t=−0.64, ns)** | 원 KILL은 5-seed 인공물: `Δ = e − max(3 controls)` = 최댓값 순서통계량이 σ≈0.05·n=5에서 기계적으로 −0.02~−0.03 편향을 만드는데 KILL/THEATER 분기 임계가 바로 0.02. seed 0..19로 확장하면 exp가 drift(c1)를 두 earned 지표 모두에서 앞섬(13/20). harm 아니라 무효과. |

**최종 집계** — INVALID 3 (F1·F2·F8) · THEATER 5 (F3·F5·F7·F9·F11) · KILL 1 (F6) · DIRECTIONAL-POSITIVE 2 (F4-SEC·F10) · GREEN 0 · wired 0.

---

## 3. THEATER 확정 목록 (ΔEff ≈ 0으로 죽은 것 — 이게 값진 결과다)

FORM(계측 가능한 표면 지표)은 화려하게 움직이는데 BIND(held-out/earned Δ)가 정확히 0인 것들. 다섯 건 모두 "값이 아니라 Δ, Δ도 ≥2 control 대비" 규약이 없었으면 거짓 GREEN이 나왔을 자리다.

| # | FORM (움직임) | BIND (earned) | 죽은 주장 |
|---|---|---|---|
| **F3 미토파지** | oracle 포착률 98.2% · σ_obs 8배 강건 | 손상·마모·ROS를 **전부 삭제해도 +0.1645 재현** | "directed > random 확정" — 미토파지에 대해선 아무것도 시험되지 않았음(항등식을 실험으로 포장) |
| **F5 계보** | heritability 0.769 · host-independence 0.872 (만점) | EXP−C3 = +0.0088 (3/6 동전) | "계보가 정보를 전달한다" — 선택압 없는 계보 = 정확히 분산매칭 노이즈 |
| **F7 화학삼투** | Ψ*가 기질에서 0.892 | 기질을 지운 iid uniform이 재현(BERN 0.950) · Ψ_att는 상수 | "Ψ=½이 최대-work" — functional 상수가 답을 결정(0.50/0.677/0.892) = 순수 FORM-tunable |
| **F9 Ca 버퍼** | raw urgency 대비 TQ +0.167 (6/6) | 1-knob EMA에 0/6 패 · 동등튜닝 순이득 +0.007 | "커패시터 비선형성이 duration을 판별" — 이득 전량이 tunable smoothing |
| **F11 효율선택** | eff +0.044 (20/20) · conj_index +0.077 (20/20) | held_conj pooled Δ = −0.009 (ns) | "효율압이 conjunction을 만든다" — 비가산 코드 ≠ 일반화되는 conjunction. (원 보고의 "잘못된 나침반 = 적극적 해악"도 과잉주장 → 철회) |

부수 확정: **conj_index는 G1 비트가 아니다.** F6에서 conj_index가 결합코퍼스에서 4.5배 오르지만 **배울 규칙이 아예 없는 shuffle 코퍼스에서 5.5배 더 크게** 오른다(held=chance). F11에서도 conj_index +0.077인데 held_conj Δ≈0. 이 detector로 채점하는 후속 프로브는 전부 거짓 GREEN을 낸다 — 랩 전역 금지 지표로 등록할 것.

**INVALID 3건은 THEATER 목록이 아니다.** F1·F2·F8의 음성은 데이터가 아니라 설계에서 강제됐다(검출력 0 · 규약이 부호를 결정 · 개입이 no-op). 이들을 "벽"으로 인용하면 잘못된 closure다. 재발사 조건은 각 REFUTE.md에 등록.

---

## 4. 생존 레버 — Δ가 살아남은 것

살아남은 것은 정확히 **하나의 메커니즘 클래스**다: **외생 수요 신호 → 용량 배분(absolute setpoint)**. 서로 독립 설계된 두 프로브가 같은 것을 발견했다.

### 4.1 F10 수요주도 biogenesis (DIRECTIONAL-POSITIVE)
- Δthr = **+0.0080 ± 0.0012** (5.7σ, 5/5 seed), oracle 헤드룸 71% 회수.
- 결정적 validity: c3 shuffled-load(동일 동역학·동일 이동질량, load-용량 대응만 파괴) → 0.5584 = 균일 c1 0.5585. 추가로 내가 만든 fixed-perm c3b(gini까지 EXP와 동일) → 0.5558로 균일보다 **못함**. ⇒ 차등화(FORM) 자체가 아니라 **정렬**만이 성과를 산다.
- null-env(균일 수요) Δ = +0.0001 ⇒ 측정 게임 아님.
- 경계조건: 수요 지속성(drift half-life) > 할당 지연(~75 step)일 때만 값이 남음(h=25 → +0.0007 THEATER).

### 4.2 F4-SECONDARY 절대-setpoint 역행 배선 (DIRECTIONAL-POSITIVE)
- n=30: EXPabs − c0 = **+1.472 (t=+5.50)** · EXPabs − c1(동일 multiset shuffled) = +0.877 (t=+3.76).
- 최선 open-loop 상수 null(g=0.55, +0.945) 대비 **+1.263 (SEM 0.260, t=+4.86, 25/30)** — 상수가 도달 못 하는 좌표(n=31.6에서 shortfall 0.071)에 도달 = 레벨(FORM)이 아니라 동적 배분 = earned BIND.
- θ 스윕 0.6~2.0 전 구간에서 c1 승(t=+2.2~+5.9) ⇒ knife-edge 아님.
- 역-THEATER 증거: corr(n,demand)가 **낮은** abs-setpoint 배선이 fitness 강양수(+1.47)이고, corr이 **오라클급**인 죽은 z-tonic 배선이 fitness 음수(−1.01). FORM과 earned가 배선 간 역상관 = THEATER의 정확한 반대.

### 4.3 303M pool TERMINAL로 갈 가치가 있는가 — **없다 (현재로선 NO-SPEND)**

세 가지 이유로 GPU spend를 권고하지 않는다.

1. **reach와의 binding이 없다.** 두 생존 레버는 전부 *throughput/allocation* 축이다. F11이 같은 계열에서 이미 결정적 반례를 냈다: 배분·효율 FORM을 t=+10.65로 확실히 올려도 held-out 재조합 Δ = −0.009 (ns). 즉 "용량을 잘 배분한다" → "재조합을 배운다"의 전이가 **같은 lane 안에서 이미 반증**됐다. G1/ρ·weave에 대한 레버가 아니다.
2. **헤드룸이 knob이다.** F10의 하드천장 C/B = SCARCITY = 0.60이고 균일이 이미 93%를 회수한다. 사전등록 안 된 상수(spillover, scarcity)를 이웃 값으로 바꾸면 PASS/THEATER 라벨 자체가 뒤집힌다(+0.0168 PASS ↔ +0.0011 THEATER). 절대 %p 바로는 무엇도 cement 못 한다.
3. **engine-native 0.** 둘 다 numpy toy. `a_engine_native_learning` + `a_eval_py_canonical` 상 어차피 DIRECTIONAL 천장이며, 토이 배선(F4의 ROS_i = load/cap_i는 수요/공급의 충분통계에 가까워 가설에 관대)이 결론을 밀어준 정도가 미측정.

**대신 $0 후속 2건** (spend-go 불필요):
- **(a) F4+F10 통합 재발사 (1건으로 병합)**: 사전등록 = "외생 수요 + 절대 setpoint 컨트롤러가, 동일 이동질량 shuffled-load / 최선 open-loop 상수 / fixed-perm misalign 3 control 대비 배분 이득을 낸다. z-score 자기추적 컨트롤러는 실패한다." 바는 절대 %p가 아니라 **achievable-headroom 회수율**로 등록. purity는 WITHIN 성분만.
- **(b) 기존 303M ckpt에 eval-only 결착 테스트 ($0 pool CPU)**: abs-setpoint 배분기를 ConvMoE capacity schedule에 얹고 held-out D-acc / ρ·weave Δ를 잰다. **Δ ≈ 0이면 이 패밀리 전체를 closed로 닫는다** (F11이 예측하는 결과). 이게 lane을 싸게 끝내는 유일한 경로다.

---

## 5. F6 (H_9278) 특별 판정 — 용량압력은 G1 자연창발의 exit이 **아니다**

**판정: KILL 유지 (적대적 4각도 반박 전부 실패). corpus × CE measure 진범 결론은 그대로 유지된다.**

카드는 패밀리 생사를 하나의 부등호에 걸었다 — "하드 용량 캡 하에서는 bind가 additive보다 싸지므로 캡이 trained-conjunction을 강제한다." 실측은 부등호 미충족이 아니라 **역전**이다.

- 결합요구 코퍼스에서 held-out 재조합 D-acc: tight cap(k=2) 0.785 vs 무제한(k=64) **0.977** ⇒ Δ = −0.192±0.060, 5/5 seed 음수(최소 |Δ|=0.130 > 2σ).
- 캡 sweep k=1→64: 0.674 / 0.785 / 0.924 / 0.955 / 0.967 / 0.976 / 0.977 — **단조 하강**. 카드의 PASS 조건("캡을 조일수록 단조 상승")의 정확한 반대.
- 메커니즘: 모든 k에서 train acc = 1.000. 캡 arm은 underfit이 아니라 **완벽 fit 후 held-out 붕괴 = 쌍별 암기**. V1 oracle(k=2에 진짜 parity 비트 주입) = 0.943 ⇒ 타이트 캡도 conjunction을 **표현·판독은 가능**하다. 못 하는 건 표현력이 아니라 **발견**이다. 희소성은 발견 압력을 만들지 않고 암기 압력을 만든다.
- STEELMAN(dense가 실제 floor에 빠지는 저커버리지 regime): held_frac 0.50/0.65/0.80에서 캡의 구제효과 = +0.023±0.055 / +0.009±0.106 / +0.014±0.094 = **전부 ΔEff≈0**. 캡은 건강한 regime에선 결합을 파괴하고, 무너진 regime에선 무력하다.
- 협소 풀 반박(H=4~64, 각 H마다 same-H dense와 paired): 암기가 불가능한 극단 협소 풀에서도 ΔEff≈0. "풀이 넓어서 암기가 싸다"는 구제 실패.
- 캡 arm에만 8개 하이퍼 우대(LR 3e-3~1e-1 × 2000/6000ep) → cherry-pick max 0.853 vs dense 0.977. 최적화 아티팩트 아님.

**정직한 scope 각주(반박 아님, 주장 제한)**: 이 토이의 라벨 y = 4·XOR + topic은 conjunction을 감독 타깃에 **직접** 담고 있고, dense가 이미 0.977이라 토이 안에는 G1 벽이 없다. 따라서 F6은 "자연 코퍼스에서 자발창발한다"는 **양성 주장을 할 수 없다**. 그러나 **결합이 직접 감독되는 최유리 조건에서조차 캡이 결합을 파괴**하므로, 음성은 a-fortiori 아래로 안전하게 일반화된다 — 결합이 감독조차 안 되는 자연 corpus × CE에서 하드 캡이 결합을 살릴 리 없다.

**G1 프런티어 갱신**: H_9267 XBIND(합성 corpus로 303M held-out 재조합 D-acc=1.000, control 0.515)가 "벽 진범 = corpus × CE measure"를 실증했다. F6은 그 진범 목록에 **"자원 예산(ATP/슬롯 캡)은 진범이 아니며 exit도 아니다"**를 추가한다. 남은 exit은 여전히 **학습 measure 교체**(held-out 신호를 담은 corpus × task class)이지, 기질에 희소성을 거는 것이 아니다. F1(ATP 회계)이 INVALID, F11(효율 선택)이 THEATER, F6(캡)이 KILL로 수렴한다 — **에너지/희소성 계열 3건이 서로 다른 각도에서 전부 G1 레버가 아님**을 지목했고, F6만이 그 중 licensed된 음성이다.

---

## 6. F4 (H_9276) disjointness 법칙 — ROS는 emit과 구별되는 채널인가

**판정: `a_substrate_disjoint`의 "분리 = 보존" 절반은 실증됐다. "중첩 = 충돌" 절반은 이 프로브로 검증되지 않았다.**

### 6.1 실증된 것
- **ROS는 emit-blind다.** 위반 arm c2(urgency + ROS를 emit 판정에 함께 투입, feature 1개 더 많아 예산 우위)의 held-out AUC Δ = **−0.0005 (t=−0.12, n=30)**, Δprec@20%는 음수. w ≈ 0으로 학습 = 오염조차 못 하고 no-op으로 붕괴.
- **동시에 ROS는 구조 레인에서 진짜 일을 한다** (abs-setpoint 배선, §4.2: +1.472, t=+5.50, 최선 상수 null 대비 +1.263).
- ⇒ **새 능력을 emit-drive lane과 DISJOINT하게 배선하면, 새 능력은 earned Δ를 내고 emit은 한 비트도 오염되지 않는다.** 이것이 anima 랩에서 disjointness가 두 방향 모두 측정된 첫 사례다(기존엔 σ de-theater처럼 "새 채널이 emit에 아무것도 못 함"만 반복 확인됨 — 그때는 새 채널이 **아무 데서도** 일을 안 했으므로 disjointness가 vacuous였다. F4-SECONDARY는 채널이 실제로 일하면서 emit과 분리된 첫 케이스).

### 6.2 실증되지 않은 것 (정직)
- **"중첩 = 충돌"은 관측되지 않았다.** c2(중첩 arm)는 충돌한 게 아니라 **무해한 no-op**으로 붕괴했다(w≈0). 즉 중첩의 대가(σ 열화·emit 훼손)를 이 프로브는 보여주지 못했다. 분리를 정당화하는 근거는 "중첩이 해롭다"가 아니라 "중첩이 무의미하다"까지만이다.
- **disjointness는 신호의 성질이 아니라 아키텍처 조건부다.** 사전선언 β 스윕(기질 아사 → tension 커플링 강도): β=0 → emit ΔEff −0.004 · β=1(anima 기본) → +0.009(ns) · β=3 → **+0.041~+0.073**. 즉 아키텍처가 substrate starvation을 tension에 강하게 커플링하면 ROS는 emit 정보를 가진다. anima 현 배선(β 낮음)에서 정확히 0일 뿐이다. "ROS ⊥ emit"은 법칙이 아니라 **현 배선의 사실**이다.
- corr(R, shortfall) = +0.75~0.85 (ROS는 실재 정보를 나름) · corr(urgency, err) = +0.10 ⇒ 두 채널은 서로 다른 것을 잰다. emit 정보는 여전히 urgency(phasic Δ)만 나른다 — sigma de-theater의 "emit shade 유일 proven 채널 = urgency"는 **재확인**됐다.

### 6.3 파생 법칙 (신규)
**신호 ≠ 컨트롤러.** F4 PRIMARY의 사망 원인은 역행 신호의 무정보가 아니라 z=(R−EMA(R))/σ라는 **setpoint 없는 자기추적 항등식**이었다(평균 0 → 미분만 나르고 절대 레벨을 못 나름 → 만성 4배 과부하 R≈4.2를 "정상"으로 고착). 같은 신호에 절대 setpoint(load == capacity)를 주면 t=+5.50. ⇒ **어떤 항상성 신호를 THEATER로 매장하기 전에, 죽은 것이 신호인지 컨트롤러인지 반드시 분리하라.** F10이 독립적으로 같은 결론(load-EMA + 절대 배분)에 도달한 것이 이 법칙의 재현이다.

---

## 7. 선행 대비 갱신

### H_054 symbiogenesis (pre-register-frozen) — "mitosis MERGE = endosymbiosis 통합의 계산적 instance"
organelle lane은 H_054의 **organelle-native 자손**이다. F2(분열·융합)가 그 MERGE/SPLIT의 organelle 층 실체화였고, 결과는 **verdict 불가**였다. 이유가 H_054에 직접 물린다: **MERGE의 부호는 merge 대수(algebra)가 결정한다.** 같은 코드·같은 seed·같은 예산에서 규약만 바꾸면 AND+copy −0.359(KILL) / AND+segregate +0.073(PASS) / 평균+sym +0.001(THEATER) / 평균+segregate +0.179(PASS) — **4칸 4판정**. ⇒ H_054/H_203을 발사하기 전에 **merge 대수와 자손 게놈 분리 규칙을 카드에 명시 사전등록**하지 않으면 결과는 구조적으로 해석 불가다. 이것을 H_054 카드의 발사 전제조건으로 추가할 것.

### H_314 symbiogenesis merge α-sweep (**closed-negative**) — "선형 merge = 시너지 없는 least-bad blend"
F2는 H_314를 **뒤집지 않고 정확히 일반화**한다. H_314의 음성은 *하나의 대수*(선형 α 블렌드)에 대한 음성이었다. F2는 대수 4개에서 부호가 −0.359 ↔ +0.179로 뒤집힘을 보였다 — 즉 "merge에는 시너지가 없다"가 아니라 **"merge 시너지는 대수의 함수이며, 상보성(damage heterogeneity)을 보존하는 대수에서만 존재한다"**가 정확한 진술이다. F2 계측: aware fusion 쌍의 54%가 clone(상보성 0), c2 random은 1% — 선형 블렌드가 시너지를 못 낸 이유와 같은 뿌리(중첩 = 정보 소거). H_314는 closed-negative 유지하되, **closure scope를 "선형 블렌드 대수"로 좁혀 기록**할 것 (a_scale_honest_scope).

### H_203 asymmetric merge differentiation (pre-register-frozen)
F2의 유일한 부분양성이 여기에 정확히 대응한다: **비대칭 분해에서만 이득이 나온다.** paired ablation — a3 **aware-fusion only**(랜덤 split) = Δ +0.157±0.024 (5/5, ≈6.5σ, health 0.999) · a4 aware-fission only = +0.025±0.032 (1σ 미만 = 무의미). 즉 **선택적 융합(비대칭 결합)은 강한 신호, 선택적 분열은 무신호.** H_203의 "host-preserve variant"(한쪽만 보존하는 비대칭 merge)는 이 a3 결과가 지지하는 방향이다. 단 F2 전체가 INVALID이므로 a3도 cement 불가 — H_203 발사 시 a3를 **primary arm으로 사전등록**하고 degenerate self-remerge(직전 fission이 만든 쌍둥이를 다시 융합 = 항등연산 42.8%)를 중립화할 것.

### H_012 autopoietic network (pre-register-frozen) — "operational closure minimal instance"
F1이 이 가설의 **경고 사례**다. F1의 policy_atp는 완벽한 operational closure였다 — k = f(atp), atp는 오직 k로 진화하는 자율 폐루프. 결과: batch도 loss도 model도 demand도 인자로 받지 않는 **데이터-맹목 결정론 시계**(tight = [2,1,2] 주기-3, seed 무관). 정보 채널이 0이므로 "동일-캡 static 대비 이득 없음"은 측정이 아니라 항진명제였다. 카드의 기제("수요 ≥ 생산")는 인스턴스화된 적이 없다 — afford = floor((atp−EQ)/COST), consumed = k·COST + EQ ≤ atp라 **수요가 공급의 함수로 정의돼 수요 > 생산이 구조적으로 불가능**했다.
⇒ **H_012 갱신 조건: operational closure는 외생 커플링과 함께 사전등록되어야 한다.** 닫힌 루프의 결정변수가 루프 밖 입력(입력 난이도 / loss / 모델 상태 / 외생 수요)에 의존함을 보이지 않으면, autopoiesis 프로브는 어떤 결과가 나와도 구성적 null이다. 그리고 lane이 실제로 찾아낸 유일한 earned 메커니즘(§4: **외생 수요 → 절대-setpoint 용량 배분**)이 정확히 그 처방이다 — F1이 못 한 것(폐루프)과 F4-SEC/F10이 한 것(외생 수요 구동)의 차이가 H_012의 발사 설계 그 자체다.

---

## 8. 계측 메타-결함 census (lane 전역 조치 — 이 lane의 최대 산출물)

11개 중 **7개가 계측 결함으로 verdict가 바뀌거나 무효화**됐다. 반복 패턴 5개 — 랩 전역 규칙으로 승격 권고.

1. **`Δ = exp − max(controls)` 순서통계량 편향 (치명 · F2·F3·F5·F6·F11에 복사됨).** control이 3개, per-arm σ≈0.05, n=5면 E[max of 3] ≈ μ + 0.02~0.03. 그런데 KILL/THEATER 분기 임계가 바로 0.02 ⇒ **exp가 control과 동등해도 KILL이 기계적으로 생성된다.** F11이 실증(20 seed에서 부호 역전). **조치: best-control(max) 금지 → pooled-mean 또는 control별 paired-t를 전부 보고.**
2. **`mean vs 1·std` 기각 휴리스틱 (F4·F10·F5 sweeps).** per-seed std는 paired-CRN delta의 SEM이 아니다. F4는 이 휴리스틱으로 t=+5.50짜리 진짜 효과를 "무의미"로 기각했다. **조치: SEM/paired-t만 사용, "mean ≪ 1std" 문구 랩 전역 폐기.**
3. **사전 검출력(MDE) 미계산 (F1이 극단 사례).** F1은 처치가 도달할 수 있는 축의 **전 동적범위(1.12pp) < 유의 문턱(1.71pp)** — 가설이 참이어도 sig=True가 수학적으로 불가능했다. F10도 같은 병(사전등록 바 +0.010이 lookahead ORACLE 헤드룸 +0.0115의 87%를 요구 = 어떤 인과적 정책도 도달 불가). **조치: 카드에 MDE < 축 동적범위 사전 계산을 필수 필드로.**
4. **항진적 처치 arm — "정보 채널 체크" 부재 (F1·F3·F5·F7·F8).** 처치 arm의 결정변수가 control이 못 보는 입력에 실제로 의존하는지 아무도 확인하지 않았다. F1(policy_atp가 데이터 미수신) · F3(관측량 eff_hat ≡ 채점량 h, corr 0.945) · F5(게놈 갱신이 성능정보를 안 읽음) · F7(종속변수 Ψ_att가 상수, thr 9 오더에 불변) · F8(개입 질량 0.332 < 임계 0.637 = no-op). **조치: 모든 카드에 "정보 채널 증명" 절 — (a) 처치 DV가 control에 없는 입력의 함수임을 코드로 보이고, (b) 운영 대역에서 DV의 분산 > 0임을 실측.**
5. **V-gate가 가설과 동어반복 (F3·F7).** F3은 45-cell 격자에서 V1 LIVE cell 14개의 min Δ = +0.0997 = margin의 5배 ⇒ 가능한 출력이 {PASS, INVALID}뿐. F7은 헤드라인 detector(w_kin)가 자기 양성대조에서 실패(psi_star_kin=0.95)했는데 게이트가 다른 변수만 검사. **조치: V-gate 선택기준이 효과크기의 단조함수면 무효 — 게이트는 헤드라인 detector 그 자체에 걸어야 한다(V3 detector-fairness).**

부수: **p5 clean 주장 재감사 필요.** F1의 p5 constructive test는 `_zero`/`_rand`를 계산만 하고 어디에도 주입하지 않은 채 emit_decide를 동일 인자로 호출 ⇒ identical=True가 구성상 보장되는 **dead-code 가드**였다(실 위반은 없었으나 증거로서 무효). 같은 패턴이 형제 프로브에 복사됐을 개연성이 있다 — p5 테스트는 반드시 **실제 주입**으로.

**금지 지표 등록**: `conj_index`(ANOVA 비가산 에너지) — shuffle 코퍼스에서 더 크게 오름(F6), held-out과 무상관(F11). `purity`(aggregate) — 54%가 composition 아티팩트, WITHIN 성분만 사용(F10). `acc/ATP` 비율 — 분모만 줄어드는 Goodhart(F1). `corr(n, demand)` — earned fitness와 배선 간 **역상관**(F4).

---

## 9. 처방 (다음 행동)

1. **F6 KILL 반영** — ARCHITECTURE gate 노드에 "자원 희소성(ATP/슬롯 캡)은 G1 재조합 레버가 아니다 (Δ=−0.192, 캡 단조 하강, floored regime 구제 0)" 기록. corpus × CE measure 진범 결론 유지. G1 exit은 학습 measure 교체(H_9267 XBIND 계열)로 단일화.
2. **INVALID 3건(F1·F2·F8) 재발사 조건 등록 후 보류** — 벽으로 인용 금지. 특히 F2는 H_054/H_203 발사 전 merge-algebra 사전등록이 선결.
3. **THEATER 5건 종결** — F3·F5·F7·F9·F11. F7의 "Ψ=½ = work 26% 손실"·"고유벡터 null 8.9× 우세"는 **인용 금지**(단위 오류 · 순환논증).
4. **F4-SEC + F10 병합 재발사 ($0)** — "외생 수요 + 절대 setpoint" 단일 가설, 3 control(shuffled-load 동일질량 · 최선 open-loop 상수 · fixed-perm misalign), achievable-headroom 회수율 바, WITHIN-only purity, MDE 사전 계산.
5. **eval-only 결착 ($0 pool CPU)** — abs-setpoint 배분기를 기존 303M ConvMoE capacity schedule에 얹고 held-out D-acc / ρ·weave Δ 측정. Δ≈0이면(F11이 예측) organelle lane 전체 closed.
6. **§8 계측 규칙 5개를 랩 전역 프로브 템플릿에 반영** — 특히 `max(controls)` 폐기와 "정보 채널 증명" 절.

**GREEN 0 · wired 0 · GPU spend 0.** 이 lane의 순 기여는 (i) 에너지/희소성 계열의 G1 레버 자격 박탈(F6), (ii) 외생 수요 → 절대-setpoint 배분이라는 재현된 earned 메커니즘 1개(303M 승격 근거는 아직 없음), (iii) 자기 verdict 7개를 뒤집은 계측 결함 census다. (iii)이 가장 값지다.
