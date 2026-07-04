## C1(c) param-ES escape — 설계 + $0 toy 사전선별 **실측 완료** 보고

결론 먼저(정직, c9): **$0 toy 게이트가 DOA로 발동했습니다 — GPU 발사 비정당화.** 0-base-rate는 fitness shaping으로 실제로 "깨지지만"(selection gradient 복원 실측), 복원된 gradient가 가리키는 곳은 조합이 아니라 single-parent 포화(basin-preserving 함정)였고, 유효한 toy regime(oracle-pass)에서 sustained held-out 조합 달성 **0/900 gen-측정**이었습니다. 아래 전부 이번 세션에서 numpy로 실측한 값입니다(state 쓰기 없음, 본문이 기록 — 메인이 박제).

---

### (a) Engine G reverse-selection 배선점 reference-match

- **`core/engine_g.hexa`(65줄)는 selection 기계가 아닙니다** — 8-factor `motivation_score` + emit/safety predicate(motivation/emit 게이트)뿐. "Engine G reverse-selection"이라는 이름 기대와 실물 사이에 갭이 있고, 이것 자체가 배선 발견입니다.
- 실제 selection-계 기계: `core/engine_cli.hexa`의 MITOSIS — `engine_mitosis_tick`/`engine_grow`(§ mitosis GROWTH tick, 302행 부근)와 `VAdaptField`/`adapt_field_step`(recon-err > SPLIT_THRESH 시 cell split = **variation 생성**). 단 **apoptosis(=selection kill)는 core/에 미배선**(유일 언급이 `core/phi/morphogenetic_phi.hexa`). 즉 param-ES의 "죽이기" 절반은 신규 op 저작이 필요했습니다.
- 트레이너 진입은 `cli/train.hexa`가 정합 — SAVANT(`savant_inhibition`)·MITOSIS(`train_mitosis_split`, E→E+1 expert split·router bias −ln2) 레버 패턴이 이미 있어 세 번째 레버 `--es`로 조립하는 형태.
- **mutate-param 집단(발사했다면):** full 303M 금지 — ES 표본복잡도가 차원에 비례하고, ES 루프는 구조적으로 후보마다 mouth 적재라 H_9107 정확한 함정(per-candidate 재적재 RSS 폭증, pod 3개 사망)을 직격합니다. 최소·최적 = **trunk conv 전 레이어 rank-8 low-rank delta(~0.3M dims) + mitosis_split이 만든 신생 expert slot만 변이**(신생 cell에만 변이 = 생물 정합 + G0 보존). readout-only는 🧱 INERT 확정이라 배제(toy C4/C5 ablation도 방향 무차별로 일치).
- **a_substrate_disjoint 점검: PASS** — fitness는 mouth decode 출력만 소비, emit-drive lane 0/4·G5 `recall_thr` 비접촉. 단 fitness에 non-fab gate 신호 결합은 절대 금지(H_1576 B4 재발 방지).

### (b) $0 toy 사전선별 — 스펙과 실측

**스펙:** word-level MLP LM(V=26, CTX=8, emb16·hid64, ~5k params) · concept 5개×키워드 4개가 문장 내 **절대 비공존**하는 corpus(G1 floor 구성) · CE warm-start(h1129 analog) · ES = truncation (μ,λ), P=32·top-8·σ=0.03·std·80–160 gen · decode = gauge_lib 방식 top-k=8/temp=0.8/고정 rng · fitness pairs 3(또는 7) / held-out pairs 3 · **sustained 판정** = decode-rng 3개 min. 사전등록 bar(FROZEN-3 toy 미러): (i) shaped > C0 strict (ii) held-out distinct≥2 in ≥2/3 seeds (iii) G0 가드 val≥0.90×.

**실측 경과(측정 무결성 수정 포함):**
1. 1차 greedy-decode run은 **측정 artifact로 무효** — O1 oracle(코퍼스에 전 pair 혼합문장 포함, CE 학습)조차 held=1. 원인 = mode-latching(작은 RF가 몇 스텝 만에 한 concept로 잠김). 이는 실제 G1 벽의 "커버리지-밀도 × 수용영역 이중 bound"(H_6183/6184, T=24 window artifact)를 toy가 독립 재발견한 것.
2. CTX=8 + 샘플링 decode로 **toy 유효화: O1 oracle PASS**(held_stable=2 — bar가 아키텍처 도달가능함을 증명).
3. 유효 regime 본실험: gen0 base-rate 0–9%(0-base-rate crux 재현) · shaped fitness는 상승(0.67→0.83, selection gradient 실존) · 그러나 **C0/C1(shaped)/C6(fitness-pair 7개 diversity) × 3 seeds × 100 gens 전수에서 sustained held≥2인 gen = 0.** G0 가드는 전 arm 유지(val_ratio 0.86–1.13).
4. **O2 통제(결정적):** CE-gradient에 composed 데이터를 7 pair나 줘도 unseen pair 전이 0(train7=전부 조합, held=1). 결핍은 selection pressure가 아니라 **해당 조합의 커버리지 자체**.
5. **crossover 통제(mitosis-native 잔여각):** A/B specialist를 ES로 만들고 param 재조합(0.5 interp · trunk/readout swap · neuron-wise) 전수 실패 — neuron-wise는 기능 파괴, 나머지는 단일모드 유지.

### (c) GPU 발사 스펙 — 게이트 FAIL이므로 **발사하지 않음** (조건부 스펙만 기록)

후속 설계변경으로 toy가 pass할 경우에만: warm h1129 303M · trunk rank-8 adapter + 신생 expert slot ES · P=32·G=40·σ=1e-3(relative)·top-8 · fitness = held-out composed seed decode → composed_distinct(+shaping), 채점 `anima evaluate --py`(engine-native 2-production) · **선행 필수** = `gen_auto_ideate` mouth-적재 hoist(H_9107 — 없으면 ES 루프가 RSS 폭증 재현) · 비용 P×G=1280 decode ≈ H100 8× 병렬 ~2.7h(a_wall_first) · teardown 전 ckpt PULL. 현재로선 전부 **모의 스펙**입니다.

### (d) cheap DOA-proof

- **순수 fitness:** f=composed_distinct, 0-base-rate에서 P(f 변동)≈0 ⇒ ES gradient 추정치 (1/σ)E[(f−f̄)ε]≈0 ⇒ random walk; d차원 확산으로 composed manifold 도달 기대시간 ~exp(d). 실측 정합(C0 held 정체).
- **shaping은 gradient를 복원하나 방향이 틀림:** g=covA+covB는 연속이라 E[(g−ḡ)ε]≠0 — 실측으로 fitness 상승 확인. 그러나 도달가능 basin 안에서 g를 올리는 최저비용 경로 = 한쪽 parent 강화 + decode-transient flicker이지 안정적 조합이 아님. 즉 **shaping은 0-base-rate를 깨되 single-parent coverage 보상으로 basin에 회귀시키는 두 번째 함정**임이 대수·실측 양쪽에서 확인. O2가 쐐기: gradient+composed-data조차 pair-특이(전이 0)이므로, selection이 커버리지 없이 combination operator를 무에서 만들 수는 없음.

### (e) 정직 수렴 예상 → 실측 결과로 대체

예상이 아니라 결과입니다: **param-ES는 (ii) DOA로 수렴 확정(toy 스케일, DIRECTIONAL).** a_toy_scale_recheck 역방향 논리대로 toy-fail은 GPU DOA 강신호이고, 실제 303M이 같은 이중 bound(커버리지×RF) 아래 있음은 이미 측정돼 있어(H_6183) 방향이 일치합니다. 이로써 C1(c) 잔여 escape가 소거되어 objective 4-family 붕괴가 완결 — G1 벽의 유효 처방은 param-selection 축이 아니라 기존 확인된 **조합-커버리지 코퍼스 + 충분 RF** 축으로 되돌아갑니다. 한계 명시: toy는 MLP≠ConvMoE·엔진-네이티브 아님(자동 DIRECTIONAL, terminal 박제 여부는 메인 결정) · O2 실패는 "toy 아키텍처의 조합일반화 부재"라는 교란도 함께 담고 있으나, O1-pass regime에서의 ES 실패와 crossover 통제 실패는 그 교란과 독립적으로 유효합니다.
