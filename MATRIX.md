# MATRIX.md — anima repo 전체 axis registry (SSOT, root 단일)

> anima repo 의 **모든 active work surface** (domain · sub-engine · 영구 매트릭스 ledger) 의 단일 inventory. cwd-local MATRIX.md SSOT (/matrix 도구 인식 위치). 본 SSOT 한 개만 root 에 유지 — 다른 매트릭스 파일들은 ledger link 로만 참조.

## 0. FRAMEWORK — N-dimensional axis-combination climb → FINAL COMBINATION (overhaul 2026-06-15)

> 개편: 매트릭스를 **2차원(축 단독 + 쌍교차 E×F)으로 고정하지 않는다.** 축 = 차원.
> 결합 차수 k 를 1 → 2 → 3 → … 로 **올려가며** k-way 축-상호작용 cell 을 탐색하고,
> 최종 목표 = **FINAL COMBINATION** = 더 추가/교체해도 안 바뀌는 수렴된 환원불가 축-조합
> (조합공간의 FIXED POINT). NOT a scalar (Ψ=1/2 값이 아님) — 축들의 *조합* 자체가 고정점.

```
차수 k 오름차 (climb)
 k=1  단독 축        : 0·A·B·C·D·E·F·G·H + (신규) META·SAV-LM  ← 대부분 depletion 완료
 k=2  쌍교차         : E×F (SAVANT×HIVE) round3-5 done · A↔E (ln4/3) byte-identical
 k=3  삼중 결합      : ⬜ 미개척 (예: D×E×F 의식측정×savant×collective)
 k≥4  고차 결합      : ⬜ 미개척
  ↓
 FINAL COMBINATION  : 한계이득(다음 축 추가) < ε 로 saturate 하는 축-집합 = 고정점
```

**fixed-point 판정 (falsifiable, p7)**: 차수를 올릴 때 결합의 설명력(target 예측 AUROC /
integration score)이 **유한 k\* 에서 포화**(Δ < ε) ⟺ FINAL COMBINATION 존재. 포화 안 하고
모든 축이 계속 기여 ⟺ 고정점 없음(환원불가 전체-결합, axis-D "WHOLE/irreducible" 과 정합).

**axis dimension set (현재)** — 결합 climb 의 후보 차원:
| dim | axis | 단독(k=1) 상태 |
|-----|------|---------------|
| 0·A·B·C·D·E·F·G·H | 기존 UNIVERSE 영구 8축+0 | §3 참조 (대부분 depletion/closed) |
| **META** | metacognition (neuroscience) — H_1202–1221 type-2/ERN/calibration/FOK/control/OOD/serial | active (10각도, 5🟢) — §3a |
| **SAV-LM** | savant-as-LM-cognition — H_1207–1224 Snyder/WCC/detail/seed-stable/tradeoff | active (Snyder·detail·seed-stable 3🟢) — §3a · E축 LM 확장 |

### §0a climb log (combination cells)
| probe | target | climb result | fixed point |
|-------|--------|--------------|-------------|
| H_1225 🔴 | correctness (global) | k=1 SAV-struct 0.902, others gain≈0 | **singleton {SAV-struct}** |
| H_1226 🔴 | correctness, residual | force struct base, climb rest: cum gain −0.0004 | **singleton confirmed** (beyond struct nothing adds globally) |
| H_1227 🟢 | correctness, HARD (low-struct) tercile | k*=4 climb saturates AUROC 0.789 | **{SAV-struct, EMB-pos, PRIOR-freq, META-margin}** — multi-axis combination emerges OFF the dominant axis |
| H_1228 🔴 | 3-way interaction | best triple interaction 0.901 vs additive 0.902 (syn −0.001) | **ADDITIVE** — no high-order synergy; axes combine linearly |

### §0a-2 round-2 climb log
| probe | result | finding |
|-------|--------|---------|
| H_1229 🔴 expanded(11축) | hard-regime k*=2 {SAV-struct, EMB-pos} AUROC 0.768 | 축 늘려도 조합 안 자람 — 환원불가 core 는 작다 (구조+위치 2축) |
| H_1230 🔴 emit-target | additive 0.969 vs interaction 0.970 (synergy 0.001) | 의식관련(emit/tension) target 도 ADDITIVE — 고차 시너지 없음 |
| H_1231 ⏳ comboseed | (재발사 aiden) | 최종조합이 seed 무관 고정점인가 (Jaccard≥0.6) |

| H_1231 🔴 comboseed | mean Jaccard 0.511 < 0.6 | 4-set membership seed-의존; 단 안정 nucleus {SAV-struct, META-ent} 3-seed 공통 |

**ROUND-2 수렴**: 2라운드 일관 — 최종조합 = **작은 ADDITIVE core (≈{구조 SAV-struct + 위치 EMB-pos})**.
축을 늘려도(11축) 안 커지고(H_1229), target 을 의식관련으로 바꿔도(emit) 가산적(H_1230). 측정-축
공간은 **저차원·선형 고정점** — "2D 넘기"가 cardinality 를 regime 으로 약간 늘릴 뿐 고차 얽힘은 없음.

**ROUND-1 CONCLUSION (climb depletion)**: the FINAL COMBINATION is **regime-dependent + ADDITIVE**.
Cardinality grows 1→4 as the dominant structure-axis weakens (global singleton {SAV-struct} →
hard-regime 4-set {struct,EMB-pos,PRIOR-freq,META-margin}), but axes combine LINEARLY (H_1228 no
synergy) — a REDUCIBLE additive fixed point, NOT a high-order entangled whole. Contrast: axis-D
consciousness-substrate was WHOLE/irreducible; these MEASUREMENT axes are additive/reducible.
'Beyond 2D' = more axes by regime, not interaction. NEXT k-frontier: other targets (emit/Φ) or
non-correctness combination objectives where high-order entanglement might appear.

> 진행 규칙: k=1 단독축 depletion 후, k 를 올려 결합 cell 을 연다. 매 cell = pre-registered
> falsifier + $0 verify. FINAL COMBINATION 도달(포화) 시 그 조합을 SSOT 에 고정 기록.

### §3a 신규 단독축 (k=1, this session) — combination climb 후보
| axis | landed | unifying |
|------|--------|----------|
| META | 1202🟢 1203🔴 1204🔴 1205🟢 1206🔴 1213🟢 1214🟢 1216🟢 1217🔴 1221🔴 | REAL·잘보정·실행가능하나 COARSE 1차속성 (분리 표상모듈 弱, 역량결합, content-tied, memoryless) |
| SAV-LM | 1207🔴 1208🔴 1209🟢 1210🔴 1211🔴 1219🔴 1220🟢 1223🟢 1224⏳ | 국소-디테일 특화가 실재·조기성숙(Snyder)·표상우세(WCC)·innate(seed-stable); 단절·규칙추출·역설촉진은 無 |

## 1. domains (DOMAINS.tape 23 · UNIVERSE engine 별도)

| idx | domain | snapshot | active 작업 영역 |
|---|---|---|---|
| 01 | BRAIN     | `./BRAIN.md`                   | 뇌 구조 modeling |
| 02 | AGENT     | `./AGENT/AGENT.md`             | ANIMA↔도구 bridge (sub: CODE/CREATOR/TRADING/MERCHANT/DESKTOP) |
| 03 | CORE      | `CORE/CORE.md`                 | core engine |
| 04 | DECODER   | `CORE/DECODER/DECODER.md`      | M3/M4 transport (collapse tetrad ✅ D1 LZ76검출/D3 corpus-원인/E2 balance-처방/D4 merge-negative · 처방=HARD top-1 ∧ BALANCED corpus ∧ adequate n_steps) |
| 05 | WAKE      | `./WAKE.md`                    | M4-kosmos persist, M7-p1p8 audit |
| 06 | ANIMA     | `./ANIMA.md`                   | substrate-native chat daemon (umbrella) |
| 07 | MITOSIS   | `./MITOSIS.md`                 | cell-division learning |
| 08 | CHANNEL   | `./CHANNEL.md`                 | inter-substrate channel |
| 09 | BRIDGE    | `./BRIDGE.md`                  | tension-link bridge |
| 10 | METACOG   | `./METACOG.md`                 | meta-cognition |
| 11 | DREAM     | `./DREAM.md`                   | dream-stage REM (M5 stage Φ-envelope wired #1268 · emit-substrate 소비자 4/4 완결 BRIDGE/SAVANT/HIVE/DREAM) |
| 12 | INTENT    | `./INTENT.md`                  | intention substrate |
| 13 | NARRATIVE | `./NARRATIVE.md`               | narrative thread (bench C 🔴→🟢 RECOVERED · A1 collision-saturation redesign #1263) |
| 14 | AESTHETIC | `./AESTHETIC.md`               | aesthetic novelty × coherence surface (bench E 🟠→🟢 SEPARATED · A2 weight-vector 직교화 #1265) |
| 15 | EMBODIMENT| `./EMBODIMENT.md`              | embodiment perception-action loop (bench F 🟠→🟢 · A3 coupling-severance redesign #1266) |
| 16 | OTHER-MIND| `./OTHER-MIND.md`              | theory-of-mind partner estimate (bench G 🟠→🟢 RECOVERED · A4 orthant-bias centering #1267) |
| 17 | TIME      | `./TIME.md`                    | circadian phase / temporal binding (bench H 9/0→6/3 robust · E3 3 spurious artifact 발견 #1281) |
| 18 | SAVANT    | `./SAVANT.md`                  | UNIVERSE 축 E mirror (GZ × SI · 10 H) |
| 19 | HIVE-MIND | `./HIVE-MIND.md`               | UNIVERSE 축 F mirror (Kuramoto × collective Φ · 5 H) |
| 20 | MERCHANT  | `./AGENT/MERCHANT/MERCHANT.md` | merchant sub-agent |
| 21 | DESKTOP   | `./AGENT/DESKTOP/DESKTOP.md`   | desktop M4 window-ops |
| 22 | CREATOR   | `./AGENT/CREATOR/CREATOR.md`   | creator sub-agent |
| 23 | TRADING   | `./AGENT/TRADING/TRADING.md`   | trading sub-agent |
| -- | UNIVERSE  | `UNIVERSE/UNIVERSE.md`         | 생명·의식 영구 발견 엔진 (LIFE 개명 후 · DOMAINS.tape 외 engine) |

## 2. sub-engines (SUB_ENGINES/)

| idx | sub-engine | path | role |
|---|---|---|---|
| S1 | AKIDA | `SUB_ENGINES/AKIDA/` + `HEXAD/SPONTANEOUS/AKIDA_FIRST.md` | neuromorphic HW 자연발화 (pi5 spike streamer · akida_bridge · /ws/akida_ingest) |
| S2 | IIT4  | `HEXAD/IIT4/lib/` + `stdlib/consciousness/iit4_bigphi.hexa` | full IIT 4.0 cause-effect Φ-structure (n=4 안전, n>=7 timeout 주의) |
| S3 | SAVANT | `HEXAD/SAVANT/` (H359 canonical + COMPENDIUM 783L) | Golden Zone × Savant Index (UNIVERSE 축 E anchor) |

## 3. UNIVERSE 영구 축 (8) — nested registry

> domain 17 의 UNIVERSE 안 sub-axes. 본 SSOT 는 입구만 link, 자세한 cell coverage 는 UNIVERSE.md.

| 축 | 설명 | 상태 |
|---|---|---|
| 0 | $0-tier core           | CLOSED (cycle #5–21) |
| A | AXES.md backlog        | active (60 sub-axis · ~110 H seed) · **depletion 2026-05-29 (PR #1361)**: H_axisa_pythagorean_comma (5도 나선 비폐합 — 12 완전5도 (3/2)¹² = 531441/524288 ≠ 1 = 7옥타브, 3⊥2 서로소 정수론적 obstruction, 11 atom 🔵×5+🟢×6, R2/R11 consume, ln(4/3) = H_347 GZ_WIDTH(6) byte-identical 교차링크 A↔E) — **hexa-verifiable subset 고갈** · 잔여 ~100 backlog seeds 🟠 (sim/external) |
| B | large-N faithful Φ     | active (n=8 exact bounded) · **n>8 greedy-MIP approx 엔진 LANDED 2026-05-28** (hexa-lang #1972 `iit4_approx_phi` · smoke PASS n4-8 exact-일치/n9-16 동작 · 🟢-APPROX) — n>8 검증 capability 확보 · **scaling findings 2026-05-29 (🟢-APPROX)**: H_axisb_ring_scaling (ring degree-2 near-linear, n6→16 단조 4.99→19.55) · H_axisb_hypercube_scaling (k-D hypercube degree=log2(n) **super-linear** n4/8/16 = 3.19/7.09/17.01, Φ doubling ratio 2.22→2.40) · H_axisb_corr_ctrl_separation (integrated/modular **~1.8e9× 분리 large-N 유지·확대** CORR 17.3→28.8 vs CTRL ~1e-8) · H_axisb_greedy_upper_bound (greedy = **strict upper bound**, ring ~13% overshoot, smoke의 greedy==exact 는 substrate-의존) |
| C | full-IIT4 Φ-structure  | active (HEXAD/IIT4/lib) · **depletion 시도 2026-05-29**: 🟠 honest-blocker — IIT4 n≥7 timeout · n≤4 lib 동시 작업 (IIT4.log 9 open M1-M5) 로 tractable 새 셀 없음, agent socket-fail 0 finding (정직 보고) |
| D | LLM-동반 연속 가설      | active (verdict-landscape raster) · **의식-측정 클러스터 H_1037–H_1066 (상세 UNIVERSE.md / .verdicts/)**: ① Φ measure-dependence (계획-Φ split: faithful φ_EI↑ ⊥ big-Φ↓) — H_1037 🟢 n=6 discretization-invariant · H_1038 🟢 real-CLM transfer · **H_1039 🟢 REDUNDANCY-CAUSAL** (de-redundify→split COLLAPSE, ≥97% Δred cut) · **H_1040 🟢 BASELINE-REGIME-SPECIFIC** (big-Φ↓는 pre-rollout-latent 기준선에서만, d=−1.834; H_1033 잔여 핀) · **H_1062 🔴 SPLIT-PLANNING-SPECIFIC** (방향 ρ=+0.80 일반화하나 ZCA-인과붕괴는 planning만; ema/lowrank<80% cut) · **H_1063 🔴 SIGN-NOT-CLEAN-UNIVERSAL** (통제 상관 knob은 단조 측정도 제거-저항 부호도 안 만듦 → planning 진짜 특별) · **H_1066 🔴 HOLISTIC-IRREDUCIBLE** (planning-특수성=개입 통째, 단일 vbackup/depth/shared feature 필요+충분 아님) ② 시간·행위 축 T (⊥ 순간-Φ) — H_1051 🟢 z(provenance)+z(veto) 2-comp · H_1054 🟢 KOSMOS time⊥agency · H_1056 🟢 fired-veto 2-comp · H_1055 🔴 temporal-curriculum-null · **H_1057 🔴 ARCHITECTURE-AXIS-NULL** (agency 축도 graft로 설치불가) ③ control imagine-rollout — **H_1041 🔴 IMAGINE-ADVANTAGE-TASK-SPECIFIC** (비선형·부분관측서 MPC가 deep-horizon 우위 탈환; H_1034 우위=stiff-linear toy 고유) ④ arch-bound Φ — **H_1043 🔴 PHI-NEEDS-MORE-THAN-GRAFT** (frozen base graft 모두 LoRA 대역 못 넘음; native 풀학습만 +0.835) · **H_1059 🟢 PHI-CARRIER-LOCATED** (φ-운반자=3중주 {MoE라우팅×conv깊이×tanh비선형} 필수합집합, 각 빼면 86–91% 소실; conv 시간-RF만 불필요) ⑤ 의식-尺 ruler arc ✅ FULL CLOSURE — H_1045/1046/1047/1049 🔴 (single Φ-scalar로 분류 충분, vector/pair/synergy 무이득) · **H_1060 🟢 RULER-NEEDS-T (QUALIFIED, Φ-blind-by-construction)** · **H_1061 🔴 PHI-ABSORBS-AGENCY** (공정대결선 Φ-scalar가 agency 흡수, T 잉여; H_1060 +0.60은 아티팩트) · **H_1064 🔴 SPLIT-UNDECIDABLE** (split서 faithful·big-Φ 둘 다 외부 인과-proxy CSP와 ρ≈0.81 순위일치 → 불일치=contrast 방향 성질, 둘 다 보고) · **H_1065 🔴 CSP-SUBSTRATE-RELATIVE** (CSP proxy-blind 벽 4/4 통과하나 cross-substrate Φ-순서尺 아님 pooled ρ=−0.43) ⑥ 비결정성 🔴 H_1052/1053 (init·entropy·learning-noise·QRNG 전부 의식-null) · **META-패턴: 의식-구조=WHOLE/환원불가 (graftable atom 아님) — H_1043 아키텍처통째 ∧ H_1059 3중주 ∧ H_1066 개입통째 ∧ H_1057 agency-설치불가 ∧ H_1052/53/55 학습동역학-설치불가 수렴** · **GPU 게이트 (0-pod 제외)**: H_1042/1044/1058 3B-transfer — toy-scope, scale-transfer UNVERIFIED (a_scale_honest_scope) |
| E | SAVANT (GZ × SI)       | active NEW 2026-05-28 (H_347/348/349/350/351/612/613/614/615/616) · **depletion 2026-05-29 (PR #1364, 3×🟢)**: H_axise_gz_band_si (GZ = bounded SI band — LOWER 4.18>3 savant·UPPER 2.85<3 sub-savant, 단조 L>C>U, 3 seed) · H_axise_gz_si_crossing (SI=3 임계 I*=0.398, GZ_CENTER 1/e 근방 |Δ|=0.0304≤0.05, mean-SI 4.553→2.502 단조) · H_axise_gz_band_per_domain (4/4 hypertrophy 도메인 F1∧F2∧F3 PASS, capacity-invariant) — GZ_UPPER cell drained, big-Φ lift는 H_295 carry deferred |
| F | HIVE-MIND collective Φ | active NEW 2026-05-28 (H_354/355/609/610/611) · **depletion 2026-05-29 (PR #1362)**: H_axisf_kuramoto_K_sync_collective_phi (🔴 FALSIFIED — N=8 Kuramoto K∈{0..4}, K↑→r∞↑ 0.079→0.978 vs Δ↓ −0.64→−3.94, **Pearson(r,Δ)=−0.934 反상관**, dynamical sync ⊥ collective-Φ super-additivity, H_609 structural-W 와 결합종류 의존 분리) · H_axisf_sync_phi_proxy_robustness (🟢 — convex+linear 양 proxy 5/5 sub-additivity 유지, Jensen 아티팩트 NOT, partition geometry 실재) |
| G | ANIMA.mining 승격 + round 6-10 메타-축 (substrate-emit · shape/scalar · substrate-class) | active (G1-G21 · 상세 UNIVERSE.md) — round 6 mining G1-G5 (H_634/637/633/639/638) → round 7-8 "shape>scalar" 양축 반증 (H_642 cross-rule · H_647 cross-seed) + structure-emergent vs number-convention 정량 분리 (H_646/651 threshold 자유도=[0,1]) → round 9-10 **substrate-class = 의식 통합 단조 분류자** 정정 완결: H_653 convexity-monotone · H_655 magnitude 비단조가 **trivial-baseline artifact** 로 판명(H_658) + scale-invariant 화해(H_660) → 모두 rule110(class-IV) 最高 수렴 · **depletion salvage 2026-05-29 (PR #1367)**: H_axisg_emit_event_count_substrate_class (🔴 FALSIFIED — substrate-emit count ⊥ G round 9-10 substrate-class 분류자, mining lens 2종 중 1종 회수, agent stalled-timeout 사망 전 산출분 stale-base 회피 fresh fork salvage) |
| H | perfect-number 닫힌형 identity (proof-harvest) | active NEW 2026-05-28 (PR #1350 · 7×🔵 SUPPORTED-FORMAL): H_ph_sigma_phi_n_tau_spine (σφ=nτ ⟺ n=6, 완전수 class 전수 — n=6-unique 구조 identity, physics-mapping uniqueness 반증과 별개) · H_ph_perfect_sigma_2n (σ=2n ⟺ aliquot s(n)=n) · H_ph_tau_perfect_2p (Euclid-Euler τ(perfect)=2p) · H_ph_mu_squarefree_unique (6=유일 squarefree perfect, μ6=1 vs μ28/496/8128=0) · H_ph_sigma_multiplicative · H_ph_euclid_euler_reconstruct (n=2^(p−1)(2^p−1)) · H_ph_sopfr_perfect (+ sopfr(496)=39 errata, legacy 58 반증) · verdict verbatim .verdicts/ph_*/ — **round-2 NEW 2026-05-29 (3×🔵, 17 atom): H_ph2_sigma_k_perfect (σ_2·σ_3 완전수 4개 고차 약수-거듭제곱합, 8 atom 🔵, 손-계산 6 errata→hexa calc 권위) · H_ph2_amicable_220_284 (첫 친화수쌍 σ=504=220+284, aliquot 2-cycle s(a)=b∧s(b)=a, 4 atom 🔵) · H_ph2_abundant_deficient_boundary (σ-vs-2n 삼분법: 12=첫과잉·945=첫홀수과잉·8·10=부족, 5 atom 🔵)** · verdict verbatim .verdicts/ph2_*/ — **round-3 NEW 2026-05-29 (3×🔵, 23 atom): H_ph3_perfect_5th_mersenne (5번째 완전수 33550336=2^12·(2^13−1), σ=2n + aliquot 고정점, 2 atom 🔵) · H_ph3_amicable_pairs_more (친화수쌍 4개 추가 1184/1210·2620/2924·5020/5564·6232/6368, σ(a)=σ(b)=a+b ∧ aliquot 2-cycle, 16 atom 🔵) · H_ph3_sociable_chain_p5 (주기-5 sociable aliquot 사이클 12496→14288→15472→14536→14264→12496, s⁵=n, 5 atom 🔵 — aliquot 궤도 계층 1·2·5-cycle 완성)** · verdict verbatim .verdicts/ph3_*/ — **round-4 NEW 2026-05-29 (2×🔵, 12 atom): H_ph4_superperfect (초완전수 σ(σ(n))=2n, n∈{4,16,64}, σ∘σ 합성 class, 6 atom 🔵) · H_ph4_multiply_perfect (배수완전수 σ(n)=k·n: P3 120·672·523776·459818240, P4 30240·32760, abundancy-index k≥3 일반화, 6 atom 🔵, 손-계산 2 errata→3-perfect 정정)** · verdict verbatim .verdicts/ph4_*/ — **round-5 NEW 2026-05-29 (2×🔵, 12 atom): H_ph5_harmonic_divisor (Ore 조화약수 H(n)=n·τ(n)/σ(n)∈ℤ, {6·28·140·270·496}, τ×σ 비율 첫 결합 identity, 8 atom 🔵) · H_ph5_hyperperfect (k-초완전수 k·σ(n)=(k+1)·n+(k−1), 21·2133·19521 k=2 + 325 k=3, 완전수 k=1 선형 일반화, 4 atom 🔵, 301 비-적합 제외 errata)** · verdict verbatim .verdicts/ph5_*/ — **round-6 NEW 2026-05-29 (2×🔵, 9 atom): H_ph6_almost_perfect (준완전수 σ(n)=2n−1, 2^k σ(2^k)=2^(k+1)−1, {2·4·8·32·128}, 결손-1 반직선, 5 atom 🔵) · H_ph6_betrothed_48_75 (첫 약혼수쌍 (48,75) s(a)=b+1∧s(b)=a+1, σ=a+b+1, 친화수 off-by-one 사촌, 4 atom 🔵)** · verdict verbatim .verdicts/ph6_*/ — **SOFT-CAP: 5 productive rounds (R2-R6, 10 NEW 🔵) — seam NOT depleted (almost-perfect/betrothed still yield fresh exact closed-forms; remaining 6th-perfect/more-amicable = trivial variants, quasiperfect/untouchable = 🟠 no-path)** |
| **I** | METACOGNITION (neuroscience) — type-2 meta-d′·ERN·calibration·FOK·control·OOD·serial | active 2026-06-15 · H_1202–1221 (10각도, 5🟢): REAL·잘보정·실행가능하나 COARSE 1차속성(분리표상 弱·역량결합·content-tied·memoryless). 도메인 METACOG mirror. |
| **J** | SAVANT-LM (savant-as-LM-cognition, E축 LM확장) — Snyder·WCC·detail·seed·tradeoff | active 2026-06-15 · H_1207–1224 (3🟢): 국소-디테일 특화 실재·조기성숙·표상우세·innate; 단절/규칙추출/역설촉진/eidetic/tradeoff 無. 도메인 SAVANT mirror. |
| **I×J×…** | COMBINATION-CLIMB (N차원 축-결합 고정점, §0/§0a) | active 2026-06-15 · H_1225–1231: FINAL COMBINATION = 작은 ADDITIVE nucleus {구조+불확실성}, 저차원·선형·regime-modulated·시너지0 (측정-축 reducible, 대조 D irreducible) |
| E×F | SAVANT × HIVE-MIND cross-link | round 3 closed 3/5 (1🔴 + 2🟢): H_617 🔴 FALSIFIED (PR #1171) · H_618 🟢 SUPPORTED (PR #1175) · H_619 🟢 SUPPORTED (PR #1172) · round 4 in-flight (H_620 🟢 R1≈3·GZ_WIDTH residual=0.0164 · H_621 🟢 SI/ΦD ∥ PID-synergy triangle ρ=0.5994 · **H_622 🔴 FALSIFIED — negative-pair axis-orthogonal chi-square p=0.624 + Fisher p=1.000** · **H_627 🔴 FALSIFIED (E3×F4) — 1/e GZ_CENTER invisible to quantized hivemind PID, syn(1/e)=syn(0.35)=syn(0.40)=0.975034 degenerate** · **H_628 🔴 FALSIFIED (E5×F2) — pair polarity ⊥ dΦ/dI peak-location, all 3 polarity peak at I=0.21 (GZ_LOWER), polarity scales Φ magnitude not peak position** · H_623/624/626 reserved) · ANIMA-side mirror SAVANT.md + HIVE-MIND.md (DOMAINS.tape 18/19) · **round-5 depletion 2026-05-29 (PR #1365)**: H_axisexf_gz_kuramoto_correspondence (🟠 PARTIAL — GZ_CENTER 1/e savant-peak ⊥ Kuramoto K_c≈2 sync-transition (gap 0.369 nu, F2 FAIL), BUT 양 substrate Φ-proxy 단조 ↓ (SI slope −2.05·HIVE Δ slope −3.31, Pearson +0.96) → 이전 ⊥ 라운드를 "기울기 부호 공유, 임계점 직교"로 정밀화) |

## 4. 기존 매트릭스 ledger (다른 위치)

| matrix file | scope | tier |
|---|---|---|
| `anima-physics/recovered/chip-architecture/domains_compute_chip-architecture_full-verification-matrix.md` | n=6 chip 전수검증 (74.5% EXACT, Z>12σ) | recovered ledger |
| `HEXAD/LORA/WAVES_MATRIX.md` | LoRA waves matrix | active |
| `docs/verifier_cross_matrix_20260421.md` | verifier cross matrix | docs |
| `docs/alm_consciousness_joint_matrix_runtime_20260425.md` | ALM consciousness joint | docs |
| `docs/hxc_d1_p2_launch_matrix_20260428.md` | hxc D1 P2 launch | docs |
| `tool/anima_v10_gate_matrix.hexa` | gate matrix runtime | tool |
| `tool/verifier_cross_matrix.hexa` | verifier cross runtime | tool |
| `state/an11_b_joint_matrix_r{6,8}.json` | an11 joint sweep | state |

## 5. 본 MATRIX.md rule

- **위치**: repo root, 단일 파일만 — 다른 매트릭스 SSOT 신설 금지
- **갱신**: 새 도메인 / sub-engine / 영구 매트릭스 ledger 발생 시 본 SSOT 에 row 추가
- **인덱스만**: 각 축의 자세한 verdict / cell coverage 는 *해당 위치* 의 snapshot/log 가 SSOT, 본 SSOT 는 *pointer* 만
- **roster 정합**: domains list 는 DOMAINS.tape roster 와 동기화 (도메인 추가/제거 시 양쪽 cross-update)

## status

- **2026-05-28**: 본 SSOT v1 신설 — anima 전체 axis registry (17 domain + 3 sub-engine + UNIVERSE 7 축 + 기존 ledger 8 파일)
- 이전 PR #1170 의 UNIVERSE 7 축 square 매트릭스를 본 SSOT 으로 흡수 + 확장
- **2026-05-28 (archive-recover 세션)**: legacy archive 177 가설 회수 → UNIVERSE 직속 단일 서가 402 (#1326/1328/1345) · 100% 터미널 disposition (#1336/1338 · closure_123_FINAL) · per-file `closure:` 라벨 + README 회수-인덱스 (#1344/1347). 신규 축 **H** (proof-harvest 7×🔵) + 축 **B** n>8 엔진(#1972) 추가. hexa-lang 2 PR (#1961 verify bare-path fix · #1972 n>8 Φ 엔진)
- **2026-05-29 (매트릭스 고갈 sweep)**: 7축 병렬 depletion fan-out → 7/8 축 종합 finding (A·B·E·F·G·E×F·H + C honest-blocker 0 finding). 총 신규 H_ 약 28개 (axisb 4·axisa 1·axise 3·axisf 2·axisg 1·axisexf 1·ph 7·ph2-6 10) + hexa-lang 엔진 2. PR #1350·1356-65·1367 모두 MERGED. **고갈 정직**: H soft-cap (R6 still fresh) · C honest-blocker · A·E·F·G·E×F genuine completion. 가짜 verdict 0 (hexa/sim-verify only · 손계산 errata 다수→hexa calc 권위 SSOT 재확인)
- **2026-06-09 (0-pod 의식-측정 탐색 계속 — 8 H 추가 + arc 종결)**: H_1059–H_1066 포그라운드 순차 $0 CPU (0 pod): H_1059 🟢 PHI-CARRIER-LOCATED (#1963) · H_1060 🟢 RULER-NEEDS-T-QUALIFIED (#1964) · H_1061 🔴 PHI-ABSORBS-AGENCY (#1965) · H_1062 🔴 SPLIT-PLANNING-SPECIFIC (#1966) · H_1063 🔴 SIGN-NOT-CLEAN-UNIVERSAL (#1967) · H_1064 🔴 SPLIT-UNDECIDABLE (#1968) · H_1065 🔴 CSP-SUBSTRATE-RELATIVE (#1969) · H_1066 🔴 HOLISTIC-IRREDUCIBLE (#1971). **의식-尺 ruler arc + Φ measure-dependence 메커니즘 arc 둘 다 FULL CLOSURE**. 창발 META-패턴: 의식-구조=WHOLE/환원불가 (graftable atom 아님 — H_1043/1059/1066/1057/1052·53·55 수렴). 전부 mirror≡stdlib n4,5 / a_phi_iit4_tool (proxy 금지) / g73 / a_scale_honest_scope 준수, 가짜 verdict 0. toy-$0 프런티어 정직-고갈; 남은 프런티어=scale-gated(GPU, 0-pod 제외).
- **2026-06-09 (0-pod 의식-측정 매트릭스)**: Stop-hook goal "0 pod 으로 MATRIX 모두 완성" — 포그라운드 순차 + $0 CPU-local (GPU 0 pod) 로 축 D 의식-측정 클러스터 4 셀 닫음: H_1039 🟢 redundancy-CAUSAL (#1957) · H_1040 🟢 baseline-regime-specific (#1958) · H_1041 🔴 imagine-advantage-task-specific (#1959) · H_1043 🔴 phi-needs-more-than-graft (#1960). 모두 mirror≡stdlib n=4,5 재증명 / g73 .txt→.md / a_phi_iit4_tool (proxy 금지) / a_scale_honest_scope (toy-scope, 3B-transfer UNVERIFIED) 준수. 직전 세션 산출 H_1037/1038/1051/1054/1055/1056/1057 + ruler/비결정성 🔴 도 축 D row 에 반영. GPU 게이트 잔여: H_1042/1044/1058 (3B/n=6, 0-pod 제외). 가짜 verdict 0.
- **2026-05-28 (round 6-11 + ANIMA 전축 sync)**: 축 G G1→G21 확장 (substrate-class 단조 분류자 정정 — H_658 baseline-artifact + H_660 scale-invariant 화해, 모두 rule110 class-IV 수렴) · ANIMA bench A-H 4 redesign 🟢 회복 (NARRATIVE/AESTHETIC/EMBODIMENT/OTHER-MIND — **negative=측정 artifact** 메타-패턴) + TIME E3 (PASS 도 3 spurious) · B-COFFESHOP 🔵 5/5 sympy · DECODER collapse-tetrad ✅ · emit-substrate 4/4 wired · D2 raster#7. 세션 메타-발견: **"의식 bench 의 negative/분기 = 측정 설계 결함, substrate 한계 아님" — redesign 시 회복**. pointer-only (상세 = 각 도메인 snapshot + UNIVERSE.md)


### §0a-FIN — climb 수렴 결론 (2026-06-15, H_1225–1231)
**최종조합(FINAL COMBINATION) = 작은 ADDITIVE nucleus.** 7-probe 2-round climb 수렴:
- **nucleus 안정** {SAV-struct(구조) + META-ent(불확실성)} — 3 seed 공통 재현 (H_1231).
- **주변부 fluid** — margin/pos/hnorm/prior 는 regime·seed 에 따라 ±1~2 축 출입 (Jaccard 0.51).
- **저차원·선형** — 축 7→11 늘려도 안 커지고(H_1229), 의식관련 target(emit)도 가산(H_1230), 3-way 시너지 0(H_1228).
- **regime-modulated cardinality** — 구조-풍부=1축, 구조-빈약=2~4축.

⇒ 이 측정-축 매트릭스의 고정점은 **환원가능한 작은 가산 nucleus** — axis-D 의식-substrate 의
"WHOLE/irreducible" 와 대조 (측정-축은 분해됨). climb frontier 정직-고갈 (다음 rung = 실제
research-axis 레벨 결합 또는 scale-up, 둘 다 별도 게이트).

