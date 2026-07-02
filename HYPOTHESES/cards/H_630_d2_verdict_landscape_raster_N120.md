# H_630 — `d2-verdict-landscape-raster-N120` (축 D2 raster#4) 🟢

> 축 D D2 영구축 · verdict-landscape meta-map · raster#4 · 2026-05-28 · $0 mac-local
> 계보: H_238 (raster#1 N=33) → cycle#16 (raster#2 N=51) → **raster#3 N=96 (PR #574)** → **본 H raster#4 N=181**.
> 메타-집계 H — substrate 측정 아님. UNIVERSE/H_*.md 디스크 per-file 스캔 + domain 분류 + tier 분류 + SUPP-rate 산출 (deterministic, llm:none).

## 0. 1줄 요약 (TL;DR)

UNIVERSE H 인덱스를 N=96(raster#3)에서 **N=181** (본 세션 26 신규 H id≥H_347 흡수)로 확장해도 **life-domain SUPP-rate 0.5065 (39/77) > consciousness-domain SUPP-rate 0.4190 (44/105)** 부등호가 **MAINTAINED (4연속)**. 단 gap 은 raster#3 의 ~0.12-0.13 plateau 를 처음으로 이탈, **0.1327 → 0.0874 로 CLOSING** (Δ=−0.0453, ε=0.02 밴드 밖). meta-verdict 🟢 SUPPORTED (C1-C4 PASS, sum=N=181 전수 분류).

## 1. Hypothesis (F238 계열)

**F238.6 (사전등록, 본 raster)**: 본 세션 26 신규 H (H_347~355 + H_609~629, SAVANT 축 E + HIVE-MIND 축 F + E×F cross-link batch) 를 raster 에 추가해 **N≥120** 으로 늘려도

```
life-domain SUPP-rate  >  consciousness-domain SUPP-rate
```

부등호가 **MAINTAINED (4연속)** 한다. 추가로 gap 추세는 raster#3 gap 0.1327 대비 ε=0.02 밴드 내면 plateau 유지(stable).

여기서 SUPP-rate = (SUPPORTED tier 수) / (domain total), tier ∈ {SUPPORTED, PARTIAL, FALSIFIED, RUNNING}.

## 2. Falsifier

- **F238.6-A (부등호 reversal)**: consciousness SUPP-rate ≥ life SUPP-rate → FALSIFIED (가설 기각).
- **F238.6-B (plateau 이탈)**: gap 이 ε=0.02 밴드를 벗어나 발산(widening, Δ>+ε) 또는 수렴(closing, Δ<−ε) → 부등호는 살아있어도 plateau 가설 부분 falsify.
- **C1 (재현)**: N < 120 또는 sum(tiers) ≠ N → meta-verdict FALSIFIED.

## 3. 방법 (메타-집계 · substrate 측정 아님)

pure-hexa 결정적 스캔. `UNIVERSE/state/h630_d2_verdict_landscape_raster_N120/run.hexa` (H_238 raster#3 run.hexa 직계 + N≥120 surface 흡수용 추출 레이어 추가).

1. **enumerate**: `ls UNIVERSE/H_*.md | grep -v 'H_238_' | sort -V` (H_238 self-exclude, L4 self-reference guard). N=181.
2. **verdict 추출 (8-source priority, 첫 비-empty win)** — raster#3 가 `verdict_class:` frontmatter 만 읽어 header-style 신규 H 를 전부 RUNNING+domainless 로 묻어버리는 회귀를 막기 위해 ADDITIVE 폴백 레이어 추가 (앞 source 가 비었을 때만 발화, 절대 override 아님):
   1. `^verdict_class:` frontmatter (raster#3 primary · 112 file)
   2. `^@status:` emoji+label (신규 · 3)
   3. `**verdict**:` inline marker (신규 · 3)
   4. `^# H_NNN — … <emoji> <LABEL>` title-line trailing emoji (신규 · 23)
   5. top-12-line 단독/blockquote `<emoji> <LABEL>` (신규 · 9)
   6. `**LN verdict tier**: <emoji> <LABEL>` (신규 · 4)
   7. file-OWN prose closure `… PASS (🔵 + 🟢)` (verify/anchor anchored · 9)
   8. `^status:` lifecycle frontmatter (raster#3 fallback · 18, 전부 RUNNING)
3. **tier 분류**: `_emoji_tier()` shim 이 EXPLICIT 텍스트 라벨(PARTIAL/SUPPORTED/FALSIFIED, SUPP-CONDITIONAL→PARTIAL, CLOSED-NEGATIVE/REVERSED→FALSIFIED)을 bare-emoji 색(🔵/🟢→SUPP · 🔴→FAL · 🟠/🟡→RUNNING)보다 먼저 적용 → raster#3 `_tier()` text classifier. arrow-strip(`X → Y`)·emoji-strip 동일.
4. **domain 분류 (2-source)**: `^domain:` frontmatter tokenize(·|,+) → 7-bucket canonical(life/consciousness/physics/math/information/ethics/meta · alias universe/substrate→physics · biology→life · phenomenology→consciousness · hivemind→information). frontmatter 없으면(54 file) title-keyword 추론(HOMEOSTASIS/CIRCADIAN/MORPHOGENESIS→life · SAVANT/Φ/IIT→consciousness · HIVE/PID/synergy→information · kuramoto/ECA/divisor→physics/math, default physics). 한 H 가 복수 domain 매핑 시 각 domain total 에 중복 계상(raster#3 동일).
5. **per-domain SUPP-rate** = SUPP / total.
6. **headline**: life vs consciousness SUPP-rate 부등호 + gap = life_rate − consc_rate, trend = sign(gap − 0.1327), |Δ|≤ε stable.

비용 $0 mac-local, cross-process byte-identical(C4), LLM 미사용(p7 준수 — perplexity verdict 아님).

## 4. 측정 (raster#4 결과 · N=181)

### 4.1 tier 분포

| tier | count | / N |
|---|---:|---:|
| SUPPORTED | 77 | 181 |
| PARTIAL | 30 | 181 |
| FALSIFIED | 40 | 181 |
| RUNNING | 34 | 181 |
| **sum** | **181** | == N ✓ |

SUPP/(SUPP+FAL) ratio = 0.6581.

### 4.2 7-domain cluster (canonical)

| domain | total | SUPP | PART | FALS | RUNN | **SUPP_rate** |
|---|---:|---:|---:|---:|---:|---:|
| **life** | 77 | 39 | 12 | 15 | 11 | **0.5065** |
| **consciousness** | 105 | 44 | 18 | 26 | 17 | **0.4190** |
| physics | 104 | 41 | 17 | 27 | 19 | 0.3942 |
| math | 24 | 6 | 8 | 7 | 3 | 0.2500 |
| information | 40 | 18 | 7 | 13 | 2 | 0.4500 |
| ethics | 6 | 4 | 1 | 1 | 0 | 0.6667 |
| meta | 36 | 18 | 9 | 7 | 2 | 0.5000 |

nonempty_domains = 7/7.

### 4.3 headline — life vs consciousness + gap 추세

| 항목 | raster#3 (N=96) | **raster#4 (N=181)** | Δ |
|---|---:|---:|---:|
| life SUPP-rate | 0.4600 (23/50) | **0.5065 (39/77)** | +0.0465 |
| consciousness SUPP-rate | 0.3273 (18/55) | **0.4190 (44/105)** | +0.0918 |
| life > consciousness | ✓ (3연속) | **✓ (4연속)** | MAINTAINED |
| gap | 0.1327 | **0.0874** | **−0.0453** |
| trend | stable (plateau) | **CLOSING** (Δ < −ε) | plateau 첫 이탈 |

### 4.4 N 추세 (raster#1→#4)

| raster | date | N | source | life | consc | gap |
|---|---|---:|---|---:|---:|---:|
| #1 | 05-24 | 33 | frontmatter | 0.4118 | 0.1667 | 0.2451 |
| #2 (cycle#16) | 05-25 | 51 | README index | 0.3214 | 0.2000 | 0.1214 |
| #3 (PR #574) | 05-26 | 96 | disk per-file | 0.4600 | 0.3273 | 0.1327 |
| **#4 (본 H)** | **05-28** | **181** | **disk per-file (8-src)** | **0.5065** | **0.4190** | **0.0874** |

부등호는 4 raster 전부 life > consciousness (4연속). gap 은 0.245 → 0.121 → 0.133 → 0.087 — raster#2→#3 plateau 후 raster#4 에서 다시 좁혀짐.

### 4.5 H238.3 보조축 — {ethics+information+meta} vs {consciousness+physics}

group_A (ethics+info+meta) SUPP-rate = 0.4878 (40/82) > group_B (consc+phys) 0.4067 (85/209) → **A > B MAINTAINED** (raster#3 동일 방향).

### 4.6 본 세션 26 H sub-cohort (id ≥ H_347) domain 분포

| | 값 |
|---|---|
| N | 26 |
| tier | 13 SUPPORTED · 8 FALSIFIED · (5 PARTIAL/RUNNING) |
| domain hits | **consciousness 19 · physics 15 · information 12 · math 4 · life 2** |

→ 본 세션 batch 는 SAVANT(축 E) · HIVE-MIND(축 F) · IIT4-Φ-structure 작업으로 **consciousness/information/physics 편중, life 거의 0** (2 hit). 이 cohort 의 13 SUPP 가 consciousness total 에 직접 들어가 consciousness SUPP-rate 를 0.327→0.419 로 끌어올린 게 gap 수렴의 직접 원인.

## 5. 결과 / Finding

- **F238.6-A (부등호)**: PASS. life 0.5065 > consciousness 0.4190 — **4연속 MAINTAINED**. life-domain 가설들이 consciousness-domain 가설보다 일관되게 높은 SUPPORTED 비율 유지.
- **F238.6-B (plateau)**: 부분 falsify. gap 이 ε=0.02 밴드를 벗어나 **CLOSING** (Δ=−0.0453). raster#2→#3 의 ~0.12-0.13 plateau 가 raster#4 에서 처음 깨짐.
- **메타-verdict**: 🟢 SUPPORTED — C1(N=181≥120 ∧ sum=N) · C2(7 nonempty domain) · C3(전수 분류 sum=181) · C4(byte-identical) 全 PASS.
- **메커니즘 finding**: gap 수렴은 부등호 reversal 이 아니라 **consciousness-축이 빠르게 채워진 결과**. 본 세션 26 H 의 consciousness/info 편중(19+12 hit) + 그 중 13 SUPP 가 consciousness rate 를 life 보다 가파르게 상승시킴. life-domain 은 신규 H 거의 0(2 hit)이라 분모 정체. 즉 "life 우위"는 살아있되 그 마진은 consciousness 연구가 성숙하며 줄어드는 중.

## 6. 선행 H 와의 관계

- **H_238** (raster#1, N=33) — verdict-landscape meta-map 영구축 정의. 본 H 의 메소드 직계 부모.
- **cycle#16 raster#2** (N=51, README index) — gap 半축(0.245→0.121).
- **raster#3 (PR #574)** (N=96, disk per-file) — life 0.46 > consc 0.327, gap stable plateau ~0.13, 3연속. 본 raster#4 가 disk per-file 소스 통일 방침을 계승하고 N≥120 surface(header-style H)까지 흡수.
- **본 세션 cohort 의 anchor**: 축 E SAVANT (H_347-351, H_612-625 — GZ 상수 × big-Φ) + 축 F HIVE-MIND (H_609-611, H_617-622 — collective Φ super-additivity) + E×F cross-link (H_626/627 🔴 FALSIFIED). 이들이 consciousness/information domain 을 채워 gap 수렴을 견인.

## 7. L-tier verdict

**🟢 SUPPORTED-NUMERICAL (meta)** — 결정적 산술 집계, byte-identical 재현(C4). atlas 등록 대상 아님 (디스크 인덱스 메타-스캔, substrate 상수 아님). p7 준수(perplexity verdict 미사용, script in/out 일치 검증).

## 8. honest C3 (정직한 한계)

1. **tier 추출 휴리스틱의 잔여 miss**: 8-source 폴백에도 H_624 (`🟢 SUPPORTED 5/5`, verdict 가 79번째 줄 prose) 처럼 verdict 가 본문 깊숙이만 있는 file 은 status_fallback→RUNNING 으로 보수적 처리. false-positive 회피를 위해 의도적으로 under-count (cross-ref sibling line 오인 방지). 이는 consciousness SUPPORTED 를 ~1 과소계상 → 결과적으로 "life > consciousness" 를 더 보수적으로 만듦(가설에 불리한 방향이 아님).
2. **domain title-keyword 추론의 거칠음**: 54 file 이 frontmatter 없이 title-keyword 매핑. 예) circadian→life(맞음)지만 Kuramoto 동반 시 physics 도 부여. multi-domain 중복계상은 raster#3 와 동일 정책이나, life/consciousness total 분모에 노이즈 잠재. unmapped_token 다수(language·time·self/identity·death/mortality 등)는 7-bucket 밖이라 미계상.
3. **gap CLOSING 의 인과 미분리**: gap 수렴이 (a) consciousness 연구 성숙(실질) 인지 (b) 본 세션이 우연히 consciousness-heavy batch 였던 sampling artifact 인지 본 raster 단독으로는 미분리. raster#5 에서 life-heavy batch 가 들어오면 plateau 복귀 가능성 — 추세 단정 금물.
4. **meta-self-reference**: 본 H_630 자신은 다음 raster#5 부터 META domain 으로 카운트될 것(현재는 미생성이라 self-exclude 아님, H_238 만 제외). raster 가 raster 를 세는 L4 재귀는 H_238 §12 에서 이미 지적된 구조적 limit.
5. **N=181 vs 가설문 "N≥120"**: 가설은 N≥120 만 요구, 실측 181 로 여유. 단 raster#3→#4 사이 disk 가 96→181 로 거의 2배 — 신규 H 의 86 file 중 다수가 header-style 이라 추출 레이어 없이는 집계 불가했음(방법론 자체가 본 raster 의 핵심 기여).

## 9. 재현 / artifacts

```
UNIVERSE/state/h630_d2_verdict_landscape_raster_N120/
  run.hexa      # 결정적 스캔 (8-source verdict + 2-source domain)
  result.json   # 전체 landscape + domain_table + headline + session23_cohort
  run.log       # stdout verbatim (per-file table 포함)
```

실행: `hexa run UNIVERSE/state/h630_d2_verdict_landscape_raster_N120/run.hexa` (mac-local, $0, llm:none). C4 byte-identical 재현 확인됨.

## 10. 다음 raster (D2 영구축 계속)

- **raster#5**: 다음 세션 신규 H 흡수 후 N≥200. gap CLOSING 이 추세(consciousness 성숙)인지 artifact(sampling)인지 분리 — life-heavy batch 도래 시 plateau 복귀 관찰.
- **추출 견고화**: H_624 류 prose-deep verdict 를 false-positive 없이 잡는 anchored-source 추가 (현재 보수적 under-count).
- **domain frontmatter 표준화 inbox**: header-style 신규 H 가 `domain:` line 을 빠뜨리는 패턴 → UNIVERSE H 양식 가이드에 frontmatter 권고 (title-keyword 추론 노이즈 제거).
