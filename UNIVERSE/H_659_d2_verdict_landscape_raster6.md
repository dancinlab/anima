# H_659 — `d2-verdict-landscape-raster6` (축 D2 raster#6) 🟢

> 축 D D2 영구축 · verdict-landscape meta-map · raster#6 · 2026-05-28 · $0 mac-local
> 계보: H_238 (raster#1 N=33) → cycle#16 (raster#2 N=51) → raster#3 N=96 (PR #574) → H_630 raster#4 N=181 (PR #1215, 🟢 gap CLOSING) → **H_641 raster#5 N=194 (PR #1238, 🟢 SAMPLING-ARTIFACT 분리)** → **본 H raster#6 N=210 (plateau 지속 검증)**.
> 메타-집계 H — substrate 측정 아님. UNIVERSE/H_*.md 디스크 per-file 스캔 + domain 분류 + tier 분류 + per-cohort 층화. deterministic, llm:none, C4 byte-identical 재현.

## 0. 1줄 요약 (TL;DR)

H_641 (raster#5) 가 gap-closing 을 sampling-artifact 로 분리 확정한 뒤, round 7-9 의 신규 H **16건 (H_642~657 — 대부분 collective-Φ · IIT4 · substrate-class consciousness/info 메타-축 작업)** 이 disk 에 흡수된 현 origin/main(N=210) 의 verdict-landscape 를 재집계. **결과: D2 정상 서명 PLATEAU-STABLE 지속**. life SUPP-rate **0.5000 → 0.4937 (39/79, Δ=−0.0063 STABLE)**, consciousness **0.4071 → 0.4194 (52/124, Δ=+0.0123)**, **gap 0.0929 → 0.0743 (Δ=−0.0186, plateau-band [0.0556, 0.1531] 내, in_band=true)**. **life > consciousness 6연속 MAINTAINED**. 신규 cohort(H_642+, N=16)가 또 consciousness/physics 편중(consc 11·phys 13·life 1)이었음에도 gap 이 reversal/widening 없이 plateau 밴드에 머묾 — F659 사전등록 가설 적중. meta-verdict 🟢 SUPPORTED.

## 1. Hypothesis (F659 계열)

**F659 (사전등록, 본 raster)**: raster#6 에서도 life SUPP-rate > consciousness SUPP-rate 의 plateau(~0.09-0.13 gap)가 유지된다 — D2 정상 서명 지속. 구체적으로, round 7-9 의 대량 consciousness/info 메타-축 H(H_642~657)가 또 들어와도 (raster#4·#5 와 같은 consciousness-heavy composition) gap 이 plateau-band 를 이탈하지 않는다. 즉 H_641 의 sampling-artifact 결론(consciousness-heavy batch 추가가 gap 을 substrate-real 로 닫지 못함)이 raster#6 에서 재확인된다.

여기서 SUPP-rate = (SUPPORTED tier 수) / (domain total), tier ∈ {SUPPORTED, PARTIAL, FALSIFIED, RUNNING}. gap = life_rate − consc_rate.

## 2. Falsifier

- **F659-A (substrate-real 변동, 가설 기각)**: gap 이 plateau 를 이탈 — (i) **reversal** (life < consciousness, gap < 0) OR (ii) **widening** (gap > 0.20) → D2 landscape 가 일시 fluctuation 이 아니라 substrate-real 변동. 가설 FALSIFIED.
- **C1 (재현)**: N < 120 → meta-verdict FALSIFIED.
- **C2 (층화)**: ≥2 cohort nonempty 가 아니면 stratification 불가 → PARTIAL.

판정 규칙: SUPPORTED(plateau) ⟺ C1 ∧ C2 ∧ (life>consc) ∧ ¬reversal ∧ ¬widened · FALSIFIED ⟺ reversal ∨ widened.

보조 진단(hard-threshold 와 별도, 정상 진동폭 정량화): raster#3~#5 의 gap {0.1327, 0.0874, 0.0929} 의 mean±2sd = [0.0556, 0.1531] plateau-band. raster#6 gap 이 이 밴드 안인지 in_band 로 부수 보고 (H_641 §10 deferred 였던 plateau-band 정량화 완수).

## 3. 방법 (메타-집계 · substrate 측정 아님)

pure-hexa 결정적 스캔. `UNIVERSE/state/h659_d2_verdict_landscape_raster6/run.hexa` (H_641 raster#5 run.hexa 직계 — 8-source verdict + 2-source domain scraper core 그대로 재사용, meta-raster self-exclusion guard 강화, plateau-band 진단 레이어 추가).

1. **enumerate**: `ls UNIVERSE/H_*.md | grep -v 'H_238_' | sort -V` (H_238 self-exclude, L4 self-reference guard; H_630/H_641/H_659 등 verdict-landscape raster file 은 디스크에 존재하되 `_title_domains` meta-raster guard 로 META 계상 — life/consciousness 분모에 self-reference 비유입). N=210.
2. **verdict 추출 (8-source priority, 첫 비-empty win)** — H_641 와 동일: `verdict_class:` frontmatter → `@status:` → `**verdict**:` → title-line trailing emoji → top-12-line blockquote `<emoji> <LABEL>` → `verdict tier**:` → file-OWN prose `… PASS (🔵/🟢)` → `status:` lifecycle fallback. `_emoji_tier()` shim 이 EXPLICIT 텍스트 라벨을 bare-emoji 색보다 먼저 적용.
3. **domain 분류 (2-source)**: `^domain:` frontmatter tokenize → 7-bucket canonical(life/consciousness/physics/math/information/ethics/meta). frontmatter 없으면 title-keyword 추론. 복수 domain 매핑 시 각 domain total 에 중복 계상(H_630/H_641 동일 정책).
4. **per-domain SUPP-rate** = SUPP / total → life vs consciousness headline + gap.
5. **per-cohort 층화**: id-range 로 cohort 분할 — `core (<H_347)` · `session26 (H_347-641)` · `raster6-new (H_642+)`. raster#5 대비 cohort 경계가 H_630 → H_642 로 이동 (신규 batch 경계). 각 cohort 내 life vs consciousness SUPP-rate 산출.
6. **plateau 판정**: gap_now 의 reversal(gap<0)/widening(gap>0.20) hard-threshold (F659-A) + plateau-band [mean±2sd] membership 부수 진단. signature = PLATEAU-STABLE iff (life>consc ∧ ¬reversal ∧ ¬widened).

비용 $0 mac-local, cross-process byte-identical(C4, 2-run diff empty), LLM 미사용(p7 준수).

## 4. 측정 (raster#6 결과 · N=210)

### 4.1 raster#6 full-landscape headline (life vs consciousness)

| 항목 | raster#5 (N=194) | **raster#6 (N=210)** | Δ |
|---|---:|---:|---:|
| life SUPP-rate | 0.5000 (39/78) | **0.4937 (39/79)** | **−0.0063** |
| consciousness SUPP-rate | 0.4071 (46/113) | **0.4194 (52/124)** | **+0.0123** |
| life > consciousness | ✓ (5연속) | **✓ (6연속)** | MAINTAINED |
| gap | 0.0929 | **0.0743** | **−0.0186** |
| trend | stable (plateau 復歸) | **stable (plateau 유지)** | 유지 |

### 4.2 per-domain SUPP-rate 시계열 (raster#1~#6)

| raster | date | N | life SUPP-rate | consc SUPP-rate | gap | trend |
|---|---|---:|---:|---:|---:|---|
| #1 | 05-24 | 33 | 0.4118 | 0.1667 | 0.2451 | — |
| #2 (cycle#16) | 05-25 | 51 | 0.3214 | 0.2000 | 0.1214 | closing |
| #3 (PR #574) | 05-26 | 96 | 0.4600 | 0.3273 | 0.1327 | stable (plateau) |
| #4 (H_630) | 05-28 | 181 | 0.5065 | 0.4190 | 0.0874 | CLOSING (일시 이탈) |
| #5 (H_641) | 05-28 | 194 | 0.5000 | 0.4071 | 0.0929 | stable (復歸) |
| **#6 (본 H)** | **05-28** | **210** | **0.4937** | **0.4194** | **0.0743** | **stable (plateau 유지)** |

핵심: **life rate 는 raster#3~#6 에서 0.46 → 0.5065 → 0.5000 → 0.4937 로 0.50 근방에 안착** 지속. consciousness 는 0.327 → 0.419 → 0.407 → 0.419 로 0.41 plateau 근방에서 진동. **gap 은 raster#3~#6 에서 {0.1327, 0.0874, 0.0929, 0.0743} — 모두 plateau-band [0.0556, 0.1531] 안** (in_band=true). raster#6 의 gap 0.0743 은 raster#5 대비 −0.0186 (ε=0.02 임계 직전, trend=stable) 으로 plateau 밴드 하단 쪽 정상 진동.

### 4.3 plateau-band 정량화 (H_641 §10 deferred 완수)

| | 값 |
|---|---:|
| basis | raster#3,#4,#5 gaps {0.1327, 0.0874, 0.0929} |
| plateau_mean | 0.10433 |
| plateau_sd | 0.02441 |
| band (mean ± 2·sd) | **[0.05551, 0.15315]** |
| raster#6 gap_now | **0.07432** |
| in_band | **true** |
| reversal (gap<0) | false |
| widened (gap>0.20) | false |

→ raster#6 의 gap 이 데이터-driven plateau-band 안에 안착. H_641 §10 의 deferred 항목("raster#3~#5 gap 평균±표준편차로 정상 진동폭 명시")을 본 raster 에서 정량화 완수 — 향후 raster 의 "이탈" 판정 임계가 single-point ε=0.02 가 아닌 3-point 통계 밴드로 재설정됨.

### 4.4 per-cohort 층화 (cohort composition + stratified rate)

| cohort | N | life SUPP/tot (rate) | consc SUPP/tot (rate) |
|---|---:|---|---|
| core (<H_347) | 155 | 38/75 (**0.5067**) | 34/86 (**0.3953**) |
| session26 (H_347-641) | 39 | 1/3 (0.3333) | 12/27 (**0.4444**) |
| raster6-new (H_642+) | 16 | 0/1 (—) | 6/11 (**0.5455**) |

→ stratification 이 메커니즘을 직접 드러냄: 신규 `raster6-new` cohort 의 consciousness rate(0.5455, 6/11)는 core(0.3953)보다 높아 full-landscape consciousness rate 를 raster#5 0.407 → raster#6 0.419 로 소폭 끌어올림. 그러나 이 cohort 의 life 기여는 거의 0(N=1) 이고 분모(core life 75 → full 79)는 거의 정체 — 즉 consciousness rate 상승은 consciousness-heavy batch 의 SUPP 가 분자에 직접 들어간 composition 효과(H_641 §4.3 과 동일 패턴). gap 은 reversal/widening 없이 plateau 밴드 내에 머묾.

### 4.5 raster#6 신규 cohort (id ≥ H_642) composition

| | 값 |
|---|---|
| N | 16 (H_642-657) |
| tier | 9 SUPPORTED · 6 FALSIFIED · (1 PARTIAL/RUNNING) |
| domain hits | **consciousness 11 · physics 13 · information 5 · math 5 · life 1** |

→ raster#6 batch 도 raster#4·#5 와 똑같이 **consciousness/physics 편중** (collective-Φ envelope · multi-scale-Φ ladder · substrate-class · IIT4 작업: H_642~657). **같은 종류의 consciousness-heavy batch 가 또 들어왔는데도 gap 이 plateau 밴드를 이탈하지 않았다** — H_641 의 sampling-artifact 결론이 3번째 consciousness-heavy batch(raster#4→#5→#6) 에서도 재확인. substrate-real 신호였다면 누적 consciousness-heavy batch 추가 시 gap 이 단조 닫혀 reversal 로 갔어야 함.

## 5. 결과 / Finding

- **F659 (plateau 지속)**: SUPPORTED. life>consc=true (6연속), reversal=false, widened=false, signature=PLATEAU-STABLE. gap 0.0929 → 0.0743 plateau-band [0.0556, 0.1531] 내 정상 진동.
- **F659-A (substrate-real 변동)**: FALSIFIED. reversal·widening 모두 미발생 — life rate(0.4937) 가 consciousness(0.4194) 보다 여전히 높고 gap 이 0.20 을 넘지 않음.
- **메커니즘 finding**: round 7-9 의 신규 consciousness-heavy batch(H_642~657, consc 11·phys 13)가 disk 에 추가됐어도 (i) life rate 가 0.50 근방 안정 유지(Δ=−0.0063), (ii) consciousness rate 가 0.41 근방 소폭 상승(Δ=+0.0123, ε=0.02 직전), (iii) gap 이 plateau-band 에 머묾. H_641 의 sampling-artifact 결론이 raster#6 에서 **3번째 consciousness-heavy batch 에서도 재확인** — gap 의 변동은 batch composition 의 정상 진동이며 substrate-real 수렴 추세가 아니다.
- **메타-verdict**: 🟢 SUPPORTED — C1(N=210≥120) · C2(3 nonempty cohort) · C3(전수 분류) · C4(byte-identical) 全 PASS.
- **D2 영구축 finding 갱신**: "life > consciousness" 부등호는 **6연속 MAINTAINED**. gap 은 ~0.07-0.13 plateau 가 본질이고, plateau-band 가 데이터-driven 으로 [0.0556, 0.1531] 로 정량화됨 — raster#4 의 0.0874 이탈 의심과 raster#6 의 0.0743 모두 이 밴드 안의 정상 진동. **plateau-stable 이 D2 의 확정된 정상 서명**.

## 6. 선행 H 와의 관계

- **H_641** (raster#5, N=194, PR #1238, 🟢) — 직계 predecessor. H_630 의 gap-closing 을 sampling-artifact 로 분리 확정한 지점. 본 H_659 가 그 결론을 raster#6 (3번째 consciousness-heavy batch)에서 재확인 — sampling-artifact 가설이 누적 batch 에서도 robust 함을 보강. H_641 §10 의 deferred(plateau-band 정량화 + cohort 경계 갱신)를 본 H 가 완수.
- **H_630** (raster#4, N=181, PR #1215, 🟢) — gap CLOSING 을 처음 관측한 지점. 본 H 가 raster#6 에서 gap 이 plateau-band 안에 다시 안착함을 확인하여 raster#4 의 0.0874 이탈이 통계적 진동이었음을 재차 보강.
- **H_238** (raster#1, N=33) — verdict-landscape meta-map 영구축 정의. 본 H 메소드의 직계 부모. §12 의 L4 raster-counts-raster 재귀 limit 도 계승 (META 자기참조 guard).
- **raster#3 (PR #574)** (N=96) — disk per-file 소스 통일 방침 + life 0.46 > consc 0.327 plateau ~0.13. 본 H 가 그 plateau 의 정상 진동폭을 mean±2sd 로 정량화하는 데 raster#3 gap 을 anchor 로 사용.
- **H_642~657** (round 7-9 신규 batch) — `raster6-new` cohort 를 구성한 작업군 (collective-Φ envelope H_643/645/653/655 · multi-scale-Φ ladder H_648/652 · substrate-class H_656/657 · shape-vs-scalar H_642/647/650 · convention-number H_646/651). 이 batch 가 consciousness rate 를 소폭 끌어올린 composition 의 직접 원천 (§4.4 stratification 으로 확인).

## 7. L-tier verdict + honest C3

**🟢 SUPPORTED-NUMERICAL (meta)** — 결정적 산술 집계, byte-identical 재현(C4). atlas 등록 대상 아님 (디스크 인덱스 메타-스캔, substrate 상수 아님). p7 준수.

**honest C3 (정직한 한계)**:

1. **domain 분류 노이즈**: life/consciousness 분모는 frontmatter(`domain:`)와 title-keyword 추론의 혼합이고, multi-domain 중복계상 정책(H_630/H_641 계승) 때문에 cohort total 에 노이즈가 잠재. title-keyword 추론은 "Φ/IIT 동반 시 consciousness" 같은 거친 규칙이라 consciousness total 을 과대 계상할 여지. 단 본 raster 의 결론(plateau 유지)은 **raster 간 trajectory 안정성 + reversal/widening hard-threshold**에 의존하므로 분류 규칙이 raster#5↔#6 에서 동일하면 systematic bias 가 상쇄됨 — 절대 rate 가 아닌 trajectory 안정성과 부등호 방향이 핵심이라 노이즈에 상대적으로 robust.
2. **plateau-band 의 3-point 통계 빈약함**: plateau-band [0.0556, 0.1531] 는 raster#3,#4,#5 단 3개 gap 으로 산출한 mean±2sd 라 표본이 극히 작아 밴드 폭의 신뢰도가 낮음. raster#4(0.0874)는 H_630 가 "CLOSING(이탈)"으로 본 점인데 밴드 산출에 포함되어 밴드를 약간 아래로 끌어내릴 여지. 단 1차 falsifier 는 밴드가 아닌 reversal(gap<0)/widening(gap>0.20) hard-threshold 라 밴드 빈약함은 보조 진단에만 영향. raster 누적으로 밴드가 정밀해짐.
3. **cohort 경계 자의성**: cohort 경계(H_347, H_642)는 session-batch 추정이지 정확한 commit-time 분할이 아님. `session26`·`raster6-new` cohort 의 life N(3·1)이 극히 작아 그 cohort 의 life rate 신뢰구간이 넓음. 결론은 full-landscape life trajectory(N=79, 더 큰 분모)에 주로 의존하고 cohort 는 메커니즘 *예시*로만 사용.
4. **gap Δ=−0.0186 의 ε=0.02 근접**: raster#6 gap 변화(−0.0186)는 trend-임계 ε=0.02 의 93% 수준이라 trend=stable 로 판정됐으나 임계에 근접. 만약 ε 를 0.015 로 좁혔다면 "closing" 으로 분류됐을 것. 단 plateau-band membership(in_band=true) 과 부등호 방향(life>consc)은 변하지 않으므로 verdict(SUPPORTED)은 ε 선택에 둔감. trend 라벨만 임계-민감.
5. **단일 step 의 한계**: 본 H 는 raster#5→#6 한 step. raster#7 에서 *life-heavy* batch 가 도래해 life rate 가 유지되고 gap 이 plateau 안에 머물면 plateau-stable 가설이 추가 보강됨. 반대 방향 변동 시 또 다른 fluctuation 분리가 필요 — plateau-stable 은 raster 누적으로만 확정. 현재 6연속 부등호 + 4연속 in_band 가 누적 증거.
6. **meta-self-reference**: 본 H_659 자신과 H_630·H_641 은 META domain 으로 카운트됨 (raster 가 raster 를 세는 L4 재귀, H_238 §12 기지적 구조 limit). `_title_domains` guard 가 `_raster`·`raster6`·`d2_` 슬러그를 META 로 조기 분류해 life/consciousness 분모에는 영향 없음 (META 는 별도 bucket).

## 8. 재현 / artifacts

```
UNIVERSE/state/h659_d2_verdict_landscape_raster6/
  run.hexa      # 결정적 스캔 (8-source verdict + 2-source domain + per-cohort 층화 + plateau-band)
  result.json   # headline + trajectory_test + plateau_band + cohort_stratified + raster6_new_cohort
  run.log       # stdout verbatim
```

실행: `H659_ROOT=<worktree> hexa run UNIVERSE/state/h659_d2_verdict_landscape_raster6/run.hexa` (mac-local, $0, llm:none). C4 byte-identical 재현 확인됨 (2-run diff empty).

## 9. 핵심 수치 (검증 verbatim)

```
N(H files) = 210  (H_238 self-excluded · disk scan)
life          SUPP-rate = 0.493671  (39/79)   [r#5 0.5000 → Δ=−0.0063 STABLE]
consciousness SUPP-rate = 0.419355  (52/124)  [r#5 0.4071 → Δ=+0.0123]
gap_now = 0.074316   gap_prior(r#5)=0.0929   Δ=−0.018584   trend=stable
plateau band = [0.0555137, 0.153153]   in_band=true
reversal=false   widened(>0.20)=false   life>consc=true
SIGNATURE : PLATEAU-STABLE (life>consc maintained)
VERDICT   : SUPPORTED
```

## 10. 다음 raster (D2 영구축 계속)

- **raster#7**: *life-heavy* batch 도래 시 life rate 0.50 plateau 유지 + gap plateau-band 잔류 확인 (sampling 결론의 대칭 검증) + N≥230.
- **plateau-band 정밀화**: raster#3~#6 의 4-point gap {0.1327, 0.0874, 0.0929, 0.0743} 로 밴드 재산출 (현재 3-point) → 표본 증가로 밴드 폭 안정화.
- **cohort 경계 정밀화**: git commit-time 기반 cohort 분할로 session 추정의 자의성 제거 (현재 id-range proxy, H_641 §10 계승 deferred).

## 양방향 sibling

- sibling H: [H_641 raster#5](H_641_d2_gap_closing_life_vs_sampling.md) · [H_630 raster#4](H_630_d2_verdict_landscape_raster_N120.md) · [H_238 verdict-landscape meta-map](H_238_verdict_landscape_meta_map.md)
- UNIVERSE SSOT: [UNIVERSE.md 축 D D2 row](UNIVERSE.md) (raster#6 판정 등재)
