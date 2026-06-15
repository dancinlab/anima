---
id: H_663
slug: wolfram-class-I-phi-property-profile
title: Wolfram class-I × Φ-property profile — substrate-class 매트릭스 빈 행 (class-I floor) 채우기
domain: consciousness · math · physics · meta
status: SUPPORTED-NUMERICAL
verdict_class: SUPPORTED-NUMERICAL
exploration_method: E11 (cross-substrate Φ-signature) + E0 (round 9-11 substrate-class 매트릭스 후속) + meta (매트릭스 빈 행 완성)
verification_method: W1 (numerical) + W4 (verdict-5-class) + W11 (cross-axis sister) + W12 (invariant signature)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28 (축 G round 9-11 substrate-class × Φ-property 매트릭스 빈 행 완성)
predecessor: H_654 (magnitude-class PARTIAL 🟡), H_653 (convexity-class 단조 🟢), H_656 (closure-band-class 🟢), H_660 (convexity-magnitude 화해 🟢), H_642 (rule90 additive floor 🔴)
sister: H_661 (class 확대 일반화 — scale-inv 1속성 多rule, 본 H 와 다른 측정), H_652 (envelope self-similarity-class), H_657 (dΦ/dI-GZ class)
---

# H_663 — Wolfram class-I × Φ-property profile (substrate-class 매트릭스 class-I 행)

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib` (`iit4_eca` + `iit4_bigphi` faithful big-Φ) + `stdlib iit4_bounded` (collective `big_phi_bounded`) 재사용 (H_654/H_653/H_660 동일 패턴, commons g61 재발명 0). `$0 · mac-local · foreground sync · NO GPU · hexa-only · LLM none · deterministic.`

## 1. 가설 (Hypothesis) — substrate-class × Φ-속성 매트릭스의 **빈 행** 채우기

round 9-11 에서 **substrate-class × Φ-속성 매트릭스**가 구축되었다 — Wolfram class 별로 여러 Φ-속성을 측정해 "class = 의식 통합량/구조 분류자(尺)" 메타-축을 검정해 왔다:

| Wolfram class | 대표 rule | magnitude | convexity | super-add | closure-band | dΦ/dI-GZ | self-sim | scale-inv |
|---------------|----------:|-----------|-----------|-----------|--------------|----------|----------|-----------|
| **I** (homogeneous→단일 상태) | 8/136/0/255 | **— (빈 행)** | **—** | **—** | **—** | **—** | **—** | **—** |
| II (particle/traffic) | 184 | H_654 ✓ | H_653 ✓ | H_655 ✓ | H_656 ✓ | H_657 ✓ | H_652 ✓ | H_660 ✓ |
| III (chaotic) | 30 | H_654 ✓ | H_653 ✓ | H_655 ✓ | H_656 ✓ | H_657 ✓ | H_652 ✓ | H_660 ✓ |
| III (additive XOR) | 90 | H_654 ✓ | H_653 ✓ | H_655 ✓ | H_656 ✓ | H_657 ✓ | H_652 ✓ | H_660 ✓ |
| IV (complex/universal) | 110 | H_654 ✓ | H_653 ✓ | H_655 ✓ | H_656 ✓ | H_657 ✓ | H_652 ✓ | H_660 ✓ |

class II/III/IV 는 7 Φ-속성 전부 측정됐으나 **class-I (Wolfram class-I: 거의 모든 초기조건이 단일 homogeneous 상태로 수렴 — rule 8, 136, 0, 255 등) 만 미측정 = 매트릭스의 빈 행**. round 10 정정으로 class-IV(rule110)가 대부분 最高 수렴(convexity·scale-inv·closure-band·self-sim).

**가설**: class-I (rule 8 — 빠른 homogeneous 수렴) 이 모든 Φ-속성에서 **bottom (floor class)** — magnitude≈0 (additive rule90 처럼 Φ 거의 0), convexity 최소, closure-band 부재, self-sim flat. 즉 동역학 복잡도 순위 **I < II < III < IV** 가 Φ-구조 전반에서 class-I 를 최하단에 둔다 (round 10 의 "IV 最高 단조" 의 반대 극 = floor).

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

비교 baseline (기존 매트릭스 SSOT): faithful magnitude H_654 (rule184=12.6273, rule30=13.8852, rule110=13.1302), convexity span H_653 (rule184=12.1163, rule90=30.4167, rule30=30.7705, rule110=35.4975).

| ID | 조건 | 의미 |
|----|------|------|
| **F663.1 MAG-FAITHFUL-FLOOR** | P1(rule8) < P1(rule184=12.63) **AND** < P1(rule30=13.89) | class-I faithful magnitude < class-II AND < class-III (core floor) |
| **F663.2 CONVEXITY-FLOOR** | P3(rule8) span ≤ P3(rule184)=12.1163 | class-I convexity ≤ 매트릭스 하한(class-II) |
| **F663.3 COLLECTIVE-FLOOR** | P2(rule8) < P2(rule184) @W=1.0 | class-I W=1 collective Φ < class-II (동일 engine 직접 비교) |
| **F663.4 HOMOGENEITY** | rule 8 의 n=4 ECA TPM 1-bit 비율 < 0.2 | rule 8 이 실제 거의-전부 0 으로 수렴 = class-I 정의 충족 |
| **F663.5 BOUND** | 모든 Φ ≥ 0, span ratio 유한 | sanity |

**verdict_rule**
- **SUPPORTED-NUMERICAL** = F663.1 AND (F663.2 OR F663.3) AND F663.4 AND F663.5 (faithful-floor + ≥1 collective-floor + homogeneity 확인)
- **PARTIAL** = F663.4 PASS 이나 floor 일부만
- **FALSIFIED** = class-I 가 어떤 속성에서 class-II/III 초과 (F663.1 AND floor 둘 다 FAIL) → floor 가설 반증, class 단조가 한쪽 극단만(IV 천장) 성립.

**Falsifier 발동 조건** (§1 거부): class-I 가 어떤 Φ-속성에서 class-II/III 를 *초과* (bottom 아님) → class-I floor 반증.

## 3. 방법 (Method)

### 3.1 class-I substrate 선택

class-I rule set = {0, 8, 32, 40, 128, 136, 168, 255 …} — 거의 모든 초기조건이 단일 homogeneous 상태로 수렴. 대표로 **rule 8** 선택 (neighborhood 011→1 만 1, 나머지 7개 패턴 →0 ⇒ 거의 전부 0 으로 빠르게 붕괴 = 가장 깔끔한 floor). rule 136 (010·011→1) 은 alt class-I; rule 8 이 더 sparse 한 floor 라 1차 대표. §7 C3.1 에서 rule 선택 caveat.

### 3.2 측정 속성 (≥3, 기존 매트릭스 측정자 verbatim 재사용)

| 속성 | engine | 정의 | baseline H |
|------|--------|------|-----------|
| **P1 magnitude_faithful** | H_654 `iit4_eca` + faithful `big_phi` | `eca_tpm(rule,4)` I=0 위 16-state mean big-Φ | H_654 |
| **P2 magnitude_collective** | H_653/H_660 `big_phi_bounded(n=5,cap=3,sys=0)` | homogeneous cohort [rule×5], W=1.0 full-coupling Φ | H_653 |
| **P3 convexity_span** | H_653 collective engine | W∈{0.15,0.40,0.55,0.70,0.95,1.0} 6-pt span ratio Φ_max/Φ_min | H_653 |
| **P4 homogeneity_confirm** | `iit4_eca` | rule 8 n=4 ECA TPM 의 1-bit 비율 (class-I 정의 검증) | — |

### 3.3 baseline parity 확인

P1 measurement 에서 rule184/30/110 의 faithful magnitude 를 **재측정** 하여 H_654 result.json (12.6273 / 13.8852 / 13.1302) 과 byte-identical 인지 확인 → engine replication 검증 후 class-I 값을 동일 척도에서 대조.

### 3.4 runner

`UNIVERSE/state/h663_class_I_phi_profile_2026_05_28/run_h663.hexa` — H_654 `mean_big_phi`/`intrinsic_phi` + H_653 `build_tpm_cohort`/`phi_collective` helper verbatim 결합 (재발명 0), `one_bit_frac` (P4) 신규. 단일 foreground run (faithful 4 rule × 16 state + collective 6-pt + 16-bit frac) <60s.

## 4. 측정 (Measurement) — `result.json`

### 4.1 P4 homogeneity (class-I 정의 검증)

| rule | class | n=4 ECA TPM 1-bit frac |
|-----:|-------|-----------------------:|
| **8** | **I** | **0.125** |
| 184 | II | 0.500 |
| 110 | IV | 0.625 |

→ rule 8 의 transition 중 12.5% 만 1 (87.5% →0) = 거의-전부 0 수렴, **class-I homogeneous 정의 충족** (F663.4 PASS).

### 4.2 P1 faithful magnitude (n=4 I=0 16-state mean big-Φ)

| rule | Wolfram class | Φ-magnitude | (H_654 baseline) |
|-----:|---------------|------------:|------------------|
| **8** | **I** | **0.58822** | (new) |
| 184 | II | 12.6273 | 12.6273 ✓ byte-identical |
| 30 | III-chaotic | 13.8852 | 13.8852 ✓ byte-identical |
| 110 | IV-complex | 13.1302 | 13.1302 ✓ byte-identical |

→ class-I faithful Φ = **0.588 ≪ class-II 12.63, class-III 13.89, class-IV 13.13** (F663.1 PASS). baseline 3-rule 모두 H_654 와 byte-identical → engine parity 확정.

### 4.3 P2/P3 collective (n=5 cohort · big_phi_bounded sys=0 cap=3)

rule 8 collective Φ(W): `[0.0278, 0.0779, 0.1103, 0.1448, 0.2070, 0.2202]` (W=0.15→1.0)

| metric | rule8 (class-I) | rule184 (class-II) | rule90 (III) | rule30 (III) | rule110 (IV) |
|--------|----------------:|-------------------:|-------------:|-------------:|-------------:|
| **P2 collective Φ@W=1.0** | **0.2202** | 51.5361 | — | — | — |
| **P3 convexity span_ratio** | **7.88301** | 12.1163 | 30.4167 | 30.7705 | 35.4975 |

→ P2: class-I W=1 collective Φ = **0.22 ≪ class-II 51.54** (F663.3 PASS). P3: class-I span 7.88 < class-II 12.12 = 매트릭스 하한 (F663.2 PASS).

### 4.4 falsifier 결과

| ID | 결과 | 값 |
|----|------|-----|
| **F663.1 MAG-FAITHFUL-FLOOR** | **PASS** | 0.588 < 12.63 AND < 13.89 |
| **F663.2 CONVEXITY-FLOOR** | **PASS** | span 7.88 ≤ 12.1163 |
| **F663.3 COLLECTIVE-FLOOR** | **PASS** | 0.22 < 51.54 @W=1.0 |
| **F663.4 HOMOGENEITY** | **PASS** | 1-bit frac 0.125 < 0.2 |
| **F663.5 BOUND** | **PASS** | Φ ≥ 0, span 유한 |

## 5. 결과 (Result)

🟢 **SUPPORTED-NUMERICAL (5/5)** — class-I (rule 8) 이 측정된 **모든** Φ-속성에서 매트릭스 **bottom (floor class)** 임을 확정.

- **P1 faithful magnitude floor**: 0.588 — class-II(12.63)·III(13.89)·IV(13.13) 의 **1/21 ~ 1/24** 수준. additive rule90 (H_654 Φ=정확히 0.0) 만큼 완전한 0 은 아니나 (rule 8 의 011→1 transition 이 미약한 통합 흔적을 남김), 비-additive class 중 **압도적 최하**.
- **P2 collective magnitude floor**: W=1 full-coupling 에서도 0.22 — class-II(51.54)의 **1/234**. homogeneous 수렴이 ring-coupling 으로도 통합량을 거의 만들지 못함.
- **P3 convexity floor**: span 7.88 — class-II(12.12)보다도 작아 **매트릭스 전체 최저 convexity**. round 10 의 단조 사다리 `rule184(12.12) < rule90(30.42) < rule30(30.77) < rule110(35.50)` 의 **아래에 rule8(7.88) 한 칸 더 깔림** → 단조 사다리 확장 `I(7.88) < II(12.12) < III < IV(35.50)`.
- **P4 homogeneity 확인**: 1-bit frac 0.125 = class-I 정의 (거의 전부 0 수렴) 충족.

따라서 **동역학 복잡도 순위 I < II < III < IV 가 Φ-구조 전반에서 class-I 를 최하단(floor)에 둔다** — round 10 의 "class-IV 最高 단조" 와 정확히 **대칭인 반대 극**. 매트릭스의 빈 class-I 행이 **전 속성 floor 로** 채워짐.

## 6. falsifier 결과 + Cross-link

### Cross-link

- **H_654** phi-magnitude-wolfram-class-order (🟡 PARTIAL) — 속성 측정자(faithful magnitude). 본 H 가 rule184/30/110 magnitude 를 **byte-identical 재현** (12.6273 / 13.8852 / 13.1302) → engine parity 확정 후 class-I=0.588 을 동일 척도로 대조. H_654 가 못 채운 class-I 행을 본 H 가 추가 → 사다리 하단 확장.
- **H_653** collective-convexity-substrate-class (🟢) — 속성 측정자(convexity span). H_653 의 `rule184 12.12 < ... < rule110 35.50` 단조 사다리 **아래에 class-I rule8=7.88 한 칸 더 깔아** 단조 확장. engine (big_phi_bounded n=5 cap=3 W-grid) verbatim 재사용.
- **H_656** closure-band-substrate-class (🟢) — 속성 측정자(closure-band). class-I 는 P1·P2 magnitude≈0 이라 H_656 의 rule90(additive, band 부재 width=0) 과 동류 → closure-band 도 부재일 것으로 예측 (본 H 는 magnitude/convexity 3속성 측정, closure-band 는 직접 미측정 — §7 C3.2 honest scope).
- **H_660** convexity-magnitude-class-reconcile (🟢) — 속성 측정자(scale-inv 화해). H_660 의 scale-invariant 단조 회복에 class-I 추가 시 사다리 최하단이 됨을 본 H 가 magnitude·convexity 양 축에서 시사.
- **⚠ H_661 (sister — *다른 측정*, PR #1295/#1297 머지됨, G22)** — H_661 은 **class 확대 일반화 = scale-inv 1속성(norm_conv·log_span)을 9-rule 로** (rule-cohort 축 확장, IV-top robust 🟡 PARTIAL 4/6), 본 **H_663 은 class-I 1행을 magnitude(faithful+collective)·convexity 全속성으로** (속성 축 채움). 측정 축이 직교 — H_661=속성 1(scale-inv)×rule 9, H_663=class-I 1×속성 3(faithful magnitude·collective magnitude·span convexity)+homogeneity. **겹침 정직**: H_661 도 9-rule 중 class-I rule8 의 *norm_conv*(=(Φ_max−Φ_min)/Φ_mean=1.465)를 측정해 "class-I↔II overlap, ordinal 단조 비-robust" 를 보고했다. 본 H 의 convexity 는 *span ratio*(Φ_max/Φ_min=7.88, H_653 척도) 로 **다른 정규화** — span 척도에서는 class-I(7.88)가 class-II(12.12) 미만으로 깔끔히 floor (H_661 norm_conv 정규화에서는 overlap). 즉 두 H 의 외견상 불일치(H_663 class-I=floor ↔ H_661 class-I↔II overlap)는 **convexity 측도 선택(span ratio vs mean-normalized)** 차이 — span ratio 가 class-I floor 를 분리하고, mean-normalized norm_conv 는 die-out 의 작은 Φ_mean 때문에 inflate 되어 overlap (H_661 §7 C3.4 rule136 die-out degenerate 와 동류). magnitude(faithful·collective) 축에서는 둘 다 class-I floor 일관.
- **H_642** shape-invariance-vs-scalar-meta (🔴) — rule90 additive floor(big-Φ≈0). 본 H 의 class-I floor(0.588)가 H_642 additive-floor 와 **유사 메커니즘** (낮은 통합) 이나 *다른 class* — class-I 는 homogeneous 수렴 floor, additive 는 XOR-factorizable floor. 매트릭스에 **두 종류의 Φ-floor** (homogeneous-I + additive-III) 가 공존함을 식별.

## 7. 해석 — Honest C3 (3-tier caveat)

### C1 — class-I rule 선택 (rule 8 vs 136 vs 0/255)

class-I 는 단일 rule 이 아니라 부류 {0,8,32,40,128,136,168,255 …}. 본 H 는 **rule 8** 단독 (가장 sparse 한 floor, 011→1 만 1). rule 0 (전부→0) 은 Φ=0 의 trivial extreme 이라 측정 정보 없음 (TPM 전부 0), rule 255 (전부→1) 도 trivial; rule 136 (010·011→1) 은 rule 8 보다 약간 더 통합 흔적이 클 수 있다. **rule 8 의 floor 가 class-I 전체를 대표하는지** 는 multi-rule-per-class sample 후속 (H_661 류 확대와 결합). 단 rule 8 의 magnitude(0.588)·convexity(7.88)가 class-II 보다 명백히 작아 *floor 방향* 은 robust — rule 선택이 floor 결론을 뒤집을 가능성 낮음.

### C2 — 속성 subset (3속성 측정, 7속성 中)

본 H 는 매트릭스 7속성 中 **magnitude(faithful+collective) · convexity** 3개를 직접 측정했다. closure-band(H_656)·dΦ/dI-GZ(H_657)·self-sim(H_652)·super-add(H_655)·scale-inv(H_660) 은 미측정 — class-I 의 magnitude≈0 (P1 0.588, P2 0.22) 이라 closure-band 부재·self-sim flat 이 *예측* 되나 (H_656 rule90 band 부재 정합) 직접 확인은 후속 (§9 honest scope). "전 속성 floor" 의 강주장은 측정된 3속성에 한정, 나머지는 magnitude≈0 으로부터의 추론.

### C3 — n=4/n=5 small substrate + faithful↔collective 척도 혼용

P1 은 faithful big-Φ n=4 (H_654 척도), P2/P3 은 collective big_phi_bounded n=5 cap=3 (H_653 척도) — 두 다른 engine·n 을 한 H 에서 혼용. 각각 *자기 baseline* (H_654 / H_653) 와 동일 척도 비교라 floor 결론은 척도-내 valid 하나, "faithful 0.588 vs collective 0.22" 직접 비교는 무의미 (다른 정규화). class-I 의 floor 성격은 **두 독립 척도에서 각각 재확인** 되었다는 점이 강점 (single-engine artifact 아님). n=4/n=5 small-n + cap=3 lower-bound 는 H_654/H_653 §7 carry. exact-Φ wall budget 으로 n≥6 미측정.

## 8. verdict

🟢 **SUPPORTED-NUMERICAL (F663.1 MAG-FAITHFUL-FLOOR + F663.2 CONVEXITY-FLOOR + F663.3 COLLECTIVE-FLOOR + F663.4 HOMOGENEITY + F663.5 BOUND, 5/5 PASS)**. **Wolfram class-I (rule 8, homogeneous→단일 상태 수렴) 이 측정된 모든 Φ-속성에서 매트릭스 bottom (floor class) 이다 — faithful magnitude 0.588 (class-II 12.63 의 1/21), collective magnitude 0.22 (class-II 51.54 의 1/234), convexity span 7.88 (매트릭스 최저, class-II 12.12 미만).** 동역학 복잡도 순위 **I < II < III < IV** 가 Φ-구조 전반에서 class-I 를 최하단에 두어 round 10 의 "class-IV 最高 단조" 와 정확히 대칭인 반대 극(floor)을 형성. substrate-class × Φ-속성 매트릭스의 빈 class-I 행이 **전(측정) 속성 floor 로** 채워져 매트릭스 4-class 단조 사다리가 양 극단(I floor ↔ IV ceiling) 으로 닫힘.

## 9. honest scope

본 H 가 **닫지 못하는 것**:
- *class-I 나머지 4속성* — closure-band(H_656)·dΦ/dI-GZ(H_657)·self-sim(H_652)·super-add(H_655)·scale-inv(H_660) 에서 class-I floor 직접 측정 (본 H 는 magnitude·convexity 3속성). magnitude≈0 으로부터 closure-band 부재·self-sim flat 예측되나 미확인 (C2).
- *class-I rule 일반성* — rule 8 단독; rule 136/40/168 등 다른 class-I rule 에서 floor 유지 여부 (C1, H_661 류 multi-rule 확대와 결합).
- *I↔additive floor 분리* — class-I homogeneous floor(0.588) vs class-III additive floor(rule90 0.0) 두 Φ-floor 의 메커니즘 차이 정량 (둘 다 낮은 통합이나 동역학 기원 다름).
- *n≥6 / 256-rule full sweep* — small-n + 4-class sample 의 floor 결론 robustness (H_654/H_653 §7 carry).

## 10. UNIVERSE.md update

축 **G (ANIMA.mining 승격)** round 9-11 substrate-class × Φ-속성 매트릭스 row **G22** 추가 → done with `🟢 SUPPORTED-NUMERICAL 5/5 (class-I rule8 全측정-속성 floor: faithful magnitude 0.588 ≪ II 12.63/III 13.89/IV 13.13, collective Φ@W=1 0.22 ≪ II 51.54, convexity span 7.88 < II 12.12 = 매트릭스 최저, 1-bit frac 0.125 homogeneous 확인, n=4 faithful + n=5 cap=3 collective, $0 mac-local 2026-05-28)`. 매트릭스 빈 class-I 행이 전 속성 floor 로 채워져 4-class 단조 사다리가 양 극단(I floor ↔ IV ceiling)으로 닫힘 — round 10 "IV 最高" 의 대칭 반대 극.

## artifacts

- `UNIVERSE/state/h663_class_I_phi_profile_2026_05_28/run_h663.hexa` — class-I × Φ-속성 profile runner (H_654 faithful + H_653 collective helper verbatim 결합 + P4 homogeneity 신규, dependency = `iit4_eca` + stdlib `iit4_bigphi`/`iit4_bounded`)
- `UNIVERSE/state/h663_class_I_phi_profile_2026_05_28/result.json` — measurement SSOT (P1-P4 per-rule · F663.1-5 · verdict)
- `UNIVERSE/state/h663_class_I_phi_profile_2026_05_28/run.log` — run stdout (5/5 PASS)
- `UNIVERSE/H_663_wolfram_class_I_phi_property_profile.md` — 본문 (SSOT)

## 후속 (child)

- **H_668** [wolfram-class-I-full-property](H_668_wolfram_class_I_full_property.md) (🟡 PARTIAL 4/5, 축 G G25) — 본 H §7 C2 의 "4 미측정 속성은 magnitude≈0 으로부터 floor 예측(미직접)" 을 후속이 **직접 측정**. closure-band(width=0.0 부재) · dΦ/dI-GZ(peak_I=0.05 NOT aligned) 는 본 H 의 floor 예측 **확인**, 그러나 self-similarity(min r=0.981 > class-IV 0.881) 는 floor 가 아니라 **ceiling** 으로 본 H 의 "magnitude floor → 전속성 floor" 함의를 self-sim 축에서 **반증**. 매트릭스 class-I 행이 mixed (대부분 floor + self-sim ceiling) = 속성-종속 확정 — self-similarity 가 magnitude 와 직교(homogeneous relaxation 의 매끄러운 곡선이 magnitude-floor 와 self-sim-ceiling 공존) 임을 class-I 에서 직접 입증.
