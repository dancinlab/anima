# H_9560 — C3 잔차 RF-집중 재분석 — C3 Residue · RF-Concentration Reanalysis (fable A-F4 · R2-measure · 🎨 FORK-RULED)

**status:** 🎨 FORK-RULED (Fable H_9560 설계 판정 · 2026-07-16 · 미실행·run-order 확정) — source=fable A-F4
**lane:** BINDING / two-lane · $0 기록 재분석
**related:** [[H_9359]] · [[H_9559]] · source: lab full R2-measure (fable A-F4)

## 제안 (Fable Lane-A $0 재분석 · R2)
**아이디어**: H_9359 C3 '다리' 분율 23%≈우연으로 읽혔다. 하지만 **균일 우연이 아니라** corpus 공기(co-occurrence) 거리 ≤RF 인 stem 에 **집중**한다면? P(bridge|D≤RF) > P(bridge|D>RF) 이면 벽이 정확히 RF 이고 *어느 stem 이 다리 가능한지* 예측.
**메커니즘**: $0 — 기록된 C3 per-stem 표(H_9359 산출) + corpus 공기거리 → Fisher exact.
**판정**: 집중(p<.05) ⟹ RF-도달성 실재·H_9557 census 점등 예측(prior). 균일 ⟹ KILL prior(그래도 census 는 저렴하니 실행). 어느 결과든 정보.
**verdict-integrity**: co-occurrence 거리 대리(proxy) 정의에 민감 — corpus window 기준 사전고정(사후 튜닝 금지·[[burned-gate-reanchor-is-tune-to-green]] 계열).

## 🎨 FABLE FORK-RULING (2026-07-16 · sidecar lab fable · H_9564 RF≈31 실측 위)
**판정: RF≈31 은 fork 를 날카롭게 할 뿐 벽을 재프레임하지 않는다.** RF-bound 는 오직 story **(a)**("훈련중 joint op×decl feature 가 *형성* 못 됨=co-location 부재")로만 성립 — 런타임 kill(C3 2차-CPT·C5 담체)은 **weight-reading** 이라 RF 가 제약 안 함. (a) vs **(b)**(RF 내 공기해도 다리 없음=더 깊은 store-분리)가 진짜 fork.

**🔥 mis-scope 감사 — 병렬 #42492882(H_1581~1584) RF-bound 프레임 두 번 죽음**: ① 그들 naive RF=9(dilation 무시)는 명명 arch 서도 3.4× 과소([[H_9564]] 정정) ② 벽-재현 arm(conv_L1 reach=0)=H_1394 ConvMoE-L1=어느 two-lane verdict ckpt 도 안 씀 ③ REACHABLE arm(L8/RF≈511)=H_1584 가 engine-native 로 이미 **FALSIFIED**(같은 재조합 floor best_distinct=1). 생존 조각=co-occurrence 버전 (a) 뿐(미측정). ⚠️ H_9359 ckpt=`ho_en_s{7,11}.clm`(CPT init·L 불변→L4 유력)—헤더파싱 1회로 close.

**확정 run-order (사전등록)**:
- **Step 0 — 경험적 RF ($0-ish engine-native·pool CPU eval)**: paired seed(1byte flip@거리 D)의 margin |Δm| through `--xbind`. D>31 서 |Δm|→0 예상. **RF=31 을 정적파싱(DIRECTIONAL mirror)→engine-measured 로 승격**(mirror-claim burn 방전). 초과 영향 시 파싱/식 오류(E=3 expert·router·SLW trailer 미포함)→전 D-anchor 이동.
- **Step 1 — 이 카드(H_9560 co-occurrence census · $0)**: 코퍼스는 기록됨(`cpt_ground_keep_lie_en_s{7,11}.txt`+base). packing 內 거리=trainer concat-pack 시 record 경계서 op·decl 이 31B 內 착지 가능. **packing/shuffle seed 확률적→expected min-distance proxy 를 보기 전 동결**(tune-to-green 회피). Fisher P(bridge|D≤31) vs P(bridge|D>31) + **stem-빈도 매칭 통제**(빈stem=가까운 packing∧강캐시 교란).
- **Step 2 — [[H_9562]] fire**: D-arm 을 **측정 RF(Step0) 기준** 재anchor(RF=9 아님). cheap-CPT+eval on summer(a_fire_autonomous).

**보조 prior**: 집중 p<.05⟹(a)-prior↑·H_9562 자신감 fire · 31B 內 공기 0⟹Fisher moot·(a) 미검존속·H_9562 여전 결정 · (31,511] 공기 존재∧H_1584 L8 floored⟹**(a) 반대 $0 증거**(카드에 기록 후 fire).

## 🔎 STEP-0 경험적 RF 실측 (aiden·clm303_clean L4·2026-07-16 · DIRECTIONAL·engine-native)
Fable run-order Step0 실행 — paired seed(1 marker byte flip A/B @거리 D)의 margin |Δm| = NLL(cf)−NLL(gold) 차. `anima-py evaluate clm303_clean.clm --xbind <manifest> --win 64`(aiden·OMP4·GPU 12GiB 점유→CPU-numpy 폴백 정상).
- **v1(가변길이) = confound**: |Δm| D=2 1.27→D≥12 ~0.01. 하지만 marker 가 짧은seed 1/3·긴seed 1/57 이라 **filler-희석**(margin −0.52→−5.88 단조)—RF 아닌 salience. 폐기.
- **v2(고정길이 58byte·flip 위치만 이동)**: |Δm| **D≤6 강(1.05→0.12)** + D=14~56 **약한 ~0.03 floor(감쇠 안함·깨끗한 RF=31 cutoff 없음)**.
- **판정: RF=31 mirror-claim 미방전.** 기능적 근접장(~D≤6-10)이 수학적 RF=31([[H_9564]] parse)보다 훨씬 tight. ⚠️ **confound(=제3 burn 발생·정직기록)**: marker→answer 는 *미훈련* 연관 → raw 신호전파/recency 를 재는 것이지 학습된 RF-binding 아님 · ~0.03=noise floor 근처. ⟹ crude probe 로 RF 경계 결정 불가.
- ✅ **파이프라인 확증**(aiden engine-native --xbind margin 작동) · ⟹ **결정 테스트는 여전히 [[H_9562]](훈련 개입)** — Fable 판정 재확증(H_9557/ctx-probe 로 RF 못 가름). NEXT(instrument 개선): 훈련된 marker→answer 연관(H_9562 축소판) 또는 hidden-state 직접 영향(엔진 플래그).

## 🔬 STEP-0b 깨끗한 RF = hidden-state diff (association confound 우회 · aiden CPU bit-exact · 2026-07-16)
margin(association) confound 제거 위해 `anima-py evaluate --dump-hidden` 로 **‖Δh_last‖ = 한 byte flip@거리D 의 마지막위치 hidden 차** 측정(clm_forward_hidden CPU=bit-exact·CUDA_VISIBLE_DEVICES='' 강제). null 통제(동일 prompt)=**0.000e+00**(계기 검증)·far D~57=0.30(실신호).
**결과 = ANOMALY(Fable §사전등록):** ‖Δh‖ D≤16 급락(clm303 24→0.42) **후 D16~56 약한 floor 유지·0 안감**(parsed RF=31 초과 영향).
**교차검증(사용자 "구모델·clm 문제?" 정직검정):**

| 모델 | D1 | D8 | D16 | D31 | D56 |
|---|---|---|---|---|---|
| clm303_clean L4 | 24 | 1.5 | 0.42 | 0.47 | 0.34 |
| natem_c34 L4(실 verdict) | 34 | 11.7 | 3.8 | 5.1 | 1.24 |
| clm303_deep_L8 | 15 | 1.4 | 0.47 | 0.48 | 0.40 |
| smoke_d768 | 19 | 0.7 | 0.7 | 0.7 | 0.7(붕괴·상수) |

- **clm303 특유 아님** — L4·L8·natem 전부 floor(smoke 만 별개 붕괴=D8~56 상수 0.705 near-const readout). ⟹ 사용자 "이 구모델 병리?" 반증(arch-general).
- **floor=진짜 RF 아님** — 거리 감쇠 없이 **평평=sequence-global 경로**(거리-의존 conv 아님). 유력=**MoE 라우터**(E3~4 load-balance 전문가선택이 전역통계→어느 flip 이든 상수영향) = Fable §ANOMALY "E/router/SLW 는 closed-form RF 안 덮음" 정확. floor 크기 model-weight 의존(natem 1-5 vs clm303 0.4)=실경로지 numerical bug 아님.
- ⟹ **기능적 binding RF=감쇠부(~D≤16)** · floor=약한 비-binding 전역 leak(근접장 ~2%). **#42492882 "D>RF ⟹ 수학적 독립" 이중 반증**(RF 과소 [[H_9564]] + 라우터 전역경로). 하지만 leak 약해 재조합 binding 엔 local-RF 지배.
- NEXT($0): 라우터 root-cause(E=1 모델 or router-ablation flag 로 floor 소멸 확인). 결정 테스트는 여전히 [[H_9562]] 훈련개입.

## 상태
🔬 STEP-0b EXECUTED (DIRECTIONAL·교차검증) — 깨끗한 hidden-diff: floor 는 arch-general(clm 특유 아님)·MoE 라우터 전역경로 유력(진짜 RF 아님)·기능 binding RF~D≤16. 다음=라우터 root-cause $0 → [[H_9562]] 훈련개입 결정. **distinct-from-kills:** H_9359 재분석이나 '균일 우연' 가정을 깨는 신 질문(집중 구조) — 재run 아님·기록만 · fork=(a)RF-formation vs (b)store-separation.
