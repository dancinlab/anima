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

## 상태
🎨 FORK-RULED — 미실행. Fable 판정으로 run-order 확정(Step0 경험RF→이 census→H_9562). 측정 주장 0(설계·판정). **distinct-from-kills:** H_9359 재분석이나 '균일 우연' 가정을 깨는 신 질문(집중 구조) — 재run 아님·기록만 · fork=(a)RF-formation vs (b)store-separation.
