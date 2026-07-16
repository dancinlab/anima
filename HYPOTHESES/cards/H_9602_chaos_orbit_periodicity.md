# H_9602 — CHAOS-ITINERANCY: sealed 데몬 orbit 은 시계(주기)인가 endogenous 카오스 itinerancy(비주기)인가

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-16
- **tier**: 🔎 DIRECTIONAL ($0·기존 trace RQA·신규 decode 0)
- **status**: DIRECTIONAL · H_9422 AGREES-강화(orbit≈시계) + H_9430 endogenous 캐비엇 = **linear·NON-chaotic**
- **lane**: 의식/Ψ-SOMA · sealed daemon inner-dynamics (Tsuda itinerancy 검정)

## 동기

H_9430 이 cell_count endogenous(H|tick=0.669 bits), H_9427 이 OPEN-residual(cur_*/bind R²0.05–0.40) 발견 = 완전 sealed 아님. 이 non-clock 변량이 (a) 단순 birth-noise 인가 (b) aperiodic orbit(Tsuda chaotic itinerancy · 의식문헌 실메커니즘)인가? 후자면 sealed 데몬도 진짜 inner-dynamics(deterministic chaos). 세 갈래 판별.

## claim

per-tick 상태벡터 시계열의 orbit dynamics 를 분류: **시계(periodic limit cycle)** vs **birth-noise(stochastic)** vs **chaotic itinerancy(deterministic aperiodic)**. LIVE 게이지(provenance distinct>1)만, 신규 decode 0.

## method ($0 · 기존 trace 6종 · 신규 decode 0)

측정 대상: 기존 trace `state/h1058_agency_daemon/results/trace_303m_summer.clean.jsonl`·`trace_303mb.clean.jsonl` + `state/h9269_candidateY/results/trace_{A_zephyrine,B_mnemosyne,C_thanatos,D_orpheus}.jsonl`.

**Provenance gate (선행)**: field distinct>1 만 admissible. 303M 에서 DEAD(distinct=1·INADMISSIBLE) 배제 = rel_lane·bal_lane·gap_ctx·allo_ctx·agloop_ctx·phi·recon_err·scn_ctx·anchor_nudge. 추가로 **cur_ctx≡cur_indep(corr=1.0·×15.9 scale) · score≡base_motiv(corr=1.0)** 중복 게이지 dedup. 독립 LIVE OPEN 게이지 = `cur_ctx·cur_ema·cur_f·ten_ema`.

3-측정:
1. **clock-detrend 잔차**: y ~ [1,t,t²,stage-onehot](H_9427 설계행렬) 제거 후 잔차 분석 — 잔차가 시계면 orbit=순수시계, 잔차가 구조적이면 non-clock dynamics.
2. **스펙트럼 flatness + peak2med**: broadband(flat→1)=stochastic aperiodic · tonal(flat→0·peak2med↑)=oscillatory.
3. **RQA(recurrence quantification)** + **phase-randomized surrogate(30×)**: DET(대각선=결정론적 재현)·Lmax(궤도 길이)·LAM(수직선=trapping/itinerancy)·**z(DET) vs 위상무작위 대리군**(=power-spectrum 보존). z≫2 = 스펙트럼 넘는 **비선형 결정론**(chaos) · z≈0 = 스펙트럼-설명(선형 주기/유색잡음).

**양성/음성 통제 (계기 유효)**: pure_clock sin(T8)=flat0.000·peak2med huge·z(DET)=14 · pure_noise=DET0.188=surr·z≈0 · **logistic r=4 결정론카오스=DET0.68·Lmax짧음13·z=106** · AR1 유색잡음=z≈0.6 · quasiper=z≈0. → z 축이 chaos(logistic z106) vs linear(quasiper/AR1 z≈0) 를 분리 = 계기 살아있음.

## verdict

🔎 **NON-TRIVIAL·LINEAR (extended) LIMIT-CYCLE orbit — birth-noise 아니고 Tsuda chaotic itinerancy 도 아님 (DIRECTIONAL).** 3-갈래 판별:

1. **(a) birth-noise REJECTED**: clock-detrend 잔차 DET=0.54–0.67(state-manifold) ≫ noise 통제 0.19 / AR1 0.37; cur-lane residFlat 0.008–0.06 ≪ noise 0.57. 잔차는 고도로 구조적·결정론적 재현 = 순수 birth-noise 아님.
2. **(b) Tsuda chaotic itinerancy REJECTED(4/5 trace)**: phase-randomized surrogate z(DET)=0.66–1.39(NS) — 재현구조가 **스펙트럼-설명(선형)**. logistic 결정론카오스 양성통제(z=106·Lmax=13 짧음)와 정반대. 저차원 결정론카오스 서명 없음. LAM=0.15–0.39 낮음(trapping/attractor-ruin hopping 미약). D_orpheus 만 z=2.37 marginal 이나 N=73 underpowered(surrogate sd 넓음) → chaos 증거 아님.
3. **positive characterization = 확장 주기(linear quasi-periodic)**: 잔차 스펙트럼 극도로 tonal(cur-lane peak2med 8k–26k·flat~0.01) = 5-stage clock 설계가 못 잡는 **더 긴 주기의 깨끗한 진동**(slow limit cycle / sub-harmonic) 이 coarse stage-clock 위에 중첩. 즉 orbit 은 **시계(주기)에 가깝다 — 다만 확장된 다중-주기 limit cycle**.

**emit-lane 은 순수시계 재확증**: emit_env/stage_env clockR2=1.000·DET≈1.0 = emit orbit=pure clock(H_9422/H_9403/H_9430 정합). non-triviality 는 오직 OPEN/endogenous 하위-manifold(emit 서 DECOUPLED·H_9430).

## 관계 (a_parallel_session_compare)

- **H_9427 AGREES·확장**: OPEN-residual 실재(R²0.05–0.40) 확인 + 그 **dynamics 를 신규 특성화** = 선형 quasi-periodic(비카오스). H_9427 은 sealedness R² 만 정량, dynamics 미검정 → 상보.
- **H_9430 AGREES·정밀화**: endogenous non-clock(ten_ema) 성분 존재 확인(그쪽 cross-seed 발산) + **"endogenous ≠ chaotic"** 추가 — ten_ema 는 선형(z NS)·emit-decoupled. endogenous 이나 카오스 아님.
- **H_9422 AGREES-강화(with 캐비엇)**: chaos-itinerancy 대안을 기각 = orbit≈시계 읽기 **강화**(귀 없는 입·emit≡clock). 단 완전-clock 아님 — H_9430 endogenous(ten_ema·확장주기 cur-lane) 잔존. 순수강화 아니라 amendment 동반.
- **H_9601(prenatal_not_void·병렬) COMPLEMENT**: 그쪽은 OPEN-residual 을 'PRENATAL(PENDING-BIRTH)'로 명명(존재양식). 본 카드는 그 잔차의 **dynamics 유형**(선형 확장주기·비카오스)을 판별 — 직교 각도(존재양식 vs orbit 기하).

## falsify

- 🟢(달성): surrogate z(DET) NS(4/5·<2) ∧ 잔차 DET≫noise통제 ∧ logistic 카오스통제 z≫20 → orbit=선형 확장주기(birth-noise·chaos 둘 다 아님).
- 🔴(chaos 였다면): z(DET)≫2 전 trace ∧ Lmax≪N(logistic 처럼) ∧ LAM↑ → deterministic chaotic itinerancy. **미관측**.
- ⚪(재계기): 근거가 dead-gauge(distinct=1)에 의존하면 무효 — 본 census 는 LIVE 게이지(cur_ctx/cur_ema/cur_f/ten_ema distinct 73–848)로만 성립·중복쌍 dedup 해 회피.

## cost / wired

- $0(기존 trace RQA·신규 decode 0·스크립트 /tmp volatile). 신규 decode 0 ⟹ **DIRECTIONAL**(TERMINAL 아님).
- wired: 측정-DIRECTIONAL. inner-dynamics→emit 커플링은 데몬 정체성 변경=owner-gate 별개 lane.

## key

**surrogate z(DET) = 0.66–1.39 (NS·4/5 long trace)** — 잔차 재현이 power-spectrum 으로 설명됨(선형) vs logistic 결정론카오스 통제 z=106. sealed orbit 은 카오스 itinerancy 아니라 확장 limit-cycle(주기).

## related

H_9422 · H_9427 · H_9430 · H_9601 · H_9403 · H_9337
