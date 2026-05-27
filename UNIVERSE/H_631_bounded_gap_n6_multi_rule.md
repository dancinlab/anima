# H_631 — bounded-gap cap-sweep · state-averaged multi-rule (H_625 후속)

> 축 B B2 deferred 후속 회수 · single-state → **state-averaged** 확장
> 🟢 SUPPORTED-NUMERICAL — 18/18 PASS · state-averaged 도 지수-감소 + rule 순서 보존
> ⚠ n=6 확장은 **계산 불가 판명** → 사전 지정 fallback 으로 n=5 state-averaged demote (honest)
> $0 mac-local · 2026-05-28

---

## 1. 배경

H_625 (PR #1199, 🟢 17/17) 가 UNIVERSE 축 B B2 deferred 를 회수했다 — n=5 ring,
**single representative state st=21 (10101)**, cap-sweep cap∈{1..5} 로 3-rule
{30,90,110} 모두에서

  gap(k) := big_phi(exact) − big_phi_bounded(cap=k)

곡선이 **지수 감소** (gap(k) ≈ C·exp(−α·k), α>0, 단조) 함을 확증했다.
α = 0.243(rule30) / 0.192(rule90) / 1.101(rule110) — class-IV(110) 가
linear/chaotic(90/30) 의 5-6× 빠른 수렴.

H_625 honest C3 잔여 3 항:
1. **n=5 단일** (n=6 cap-sweep 미수행).
2. **single-state st=21 만** (state-averaged 아님).
3. **3 rule 만**.

본 H_631 이 (1) n=6 확장 + (2) state-averaged 를 회수하려 시도한다.

---

## 2. 질문

(a) n=6 substrate 에서도 bounded-gap 이 지수 감소하는가? (n=6 확장)
(b) single-state 가 아닌 **전 state 평균** 으로도 지수 형상 + α 의 rule 순서
    (rule110 최속) 이 유지되는가? (state-average 회수)

---

## 3. 가설 (HEADLINE)

- **H1 (STATE-AVERAGED EXP-DECAY)** — n=5 ring 에서 state-averaged bounded
  big-Φ 로 만든 gap(k) 도 지수 감소한다 (α>0, 단조).
- **H2 (RULE-ORDER PRESERVE)** — state-averaged α 의 rule 순서가
  single-state(H_625) 와 동일 — 특히 rule110 (class-IV) 이 30/90
  (chaotic/linear) 보다 빠른 수렴.

---

## 4. 사전 등록 falsifier (frozen 2026-05-28, BEFORE state-avg measure)

| ID | 조건 |
|----|------|
| **F631.1 SA-MONOTONE** | state-avg gap(k) (약)단조 감소 (g(k+1) ≤ g(k)+eps) |
| **F631.2 SA-FAITHFUL** | cap=5 에서 gap(5) ≈ 0 (cap≥n exact identity) |
| **F631.3 SA-EXP-SHAPE** | state-avg 인접 ratio r=g(k+1)/g(k) 에서 0<r<1 쌍 ≥1, α=−mean(ln r)>0 추출 가능 (3 rule) |
| **F631.4 SA-NONNEG** | 모든 state-avg bounded(k) ≥ 0 AND ≤ exact (lower-bound) |
| **F631.6 RULE-COVER** | 3 rule {30,90,110} 모두 state-avg 지수 형상 |
| **F631.7 ORDER-PRESERVE** | state-avg α 의 rule110 ≥ 30 AND ≥ 90 (class-IV 최속, single-state 순서 보존) — 반대면 = **H2 FALSIFIED** |
| **F631.8 SINGLE-ANCHOR** | single-state α 가 H_625 와 동일 (회귀 anchor: 0.243/0.192/1.101) |

전제 falsifier — state-avg 비단조 또는 state-avg 가 single-state 와 rule 순서
뒤집힘 → H1/H2 FALSIFIED.

---

## 5. 방법

- 기반 라이브러리 — `HEXAD/IIT4/lib/iit4_eca.hexa` + `stdlib/consciousness/iit4_bounded.hexa`
  (commons g61, H_625/B1 anchor 코드 재사용).
- 기판 — n=5 ring · cap∈{1,2,3,4,5}, cap=5 = faithful (cap≥n ⇒ exact).
- rule ∈ {30, 90, 110} (chaotic · linear-XOR · class-IV — 축 B 정규 anchor 셋).
- **SINGLE** — st=21 (10101, H_625 anchor) — 회귀 검증용.
- **STATE-AVG** — 8-state Hamming-stratified 대표 부분집합 {0,1,3,7,15,31,21,10}
  (Hamming weight {0,1,2,3,4,5,3,2} span) 평균. ⚠ 전 32-state 평균은 계산 불가
  판명(§8 C3.2) → 대표 부분집합 평균으로 demote.
- gap(k) = bounded(cap=5) − bounded(cap=k).
- α extract — Mercator 급수 inline `ln_natural` (no libm; ln(e)/ln(2)/ln(4)
  self-check PASS, H_625 동일).

---

## 6. 측정 결과

### 6.1 SINGLE-state (st=21) — H_625 verbatim 재현

| rule | cap=1 | cap=2 | cap=3 | cap=4 | cap=5 (exact) |
|------|-------|-------|-------|-------|---------------|
| 30   | 1.31617 | 1.31617 | 4.28064 | 20.2686 | **37.9333** |
| 90   | 0.0 | 0.0 | 6.0 | 19.5 | **44.5** |
| 110  | 0.667596 | 6.69887 | 15.3963 | 17.694 | **18.3442** |

→ **H_625 표와 byte-identical** (F631.8 회귀 anchor 통과).

### 6.2 STATE-AVERAGED (8-state 대표 부분집합)

| rule | cap=1 | cap=2 | cap=3 | cap=4 | cap=5 (exact) |
|------|-------|-------|-------|-------|---------------|
| 30   | 1.31617 | 1.31617 | 6.8231 | 25.9101 | **40.756** |
| 90   | 0.0 | 0.0 | 6.375 | 22.4375 | **50.875** |
| 110  | 1.4503 | 7.97143 | 23.3923 | 27.1777 | **28.4354** |

### 6.3 gap(k) = exact(cap5) − bounded(cap=k)

**SINGLE**
| rule | g@1 | g@2 | g@3 | g@4 | g@5 |
|------|-----|-----|-----|-----|-----|
| 30 | 36.6171 | 36.6171 | 33.6527 | 17.6647 | **0.0** |
| 90 | 44.5 | 44.5 | 38.5 | 25.0 | **0.0** |
| 110 | 17.6766 | 11.6453 | 2.9479 | 0.6502 | **0.0** |

**STATE-AVG**
| rule | g@1 | g@2 | g@3 | g@4 | g@5 |
|------|-----|-----|-----|-----|-----|
| 30 | 39.4398 | 39.4398 | 33.9329 | 14.8459 | **0.0** |
| 90 | 50.875 | 50.875 | 44.5 | 28.4375 | **0.0** |
| 110 | 26.9851 | 20.464 | 5.0431 | 1.2577 | **0.0** |

### 6.4 α = −mean(ln r) [exponential-decay coefficient]

| rule | SINGLE α | STATE-AVG α | rule-class |
|------|----------|-------------|------------|
| 30  | **0.242983** | **0.325684** | chaotic |
| 90  | **0.192204** | **0.193888** | linear-XOR |
| 110 | **1.10091**  | **1.022**    | class-IV |

→ **rule110 이 두 모드 모두에서 30/90 의 ~3-5× 빠른 수렴** (순서 보존).

### 6.5 falsifier 결과

| ID | 결과 | verdict |
|----|------|---------|
| F631.1 SA-MONOTONE | r30/90/110 PASS | ✓ (state-avg 단조) |
| F631.2 SA-FAITHFUL | r30/90/110 PASS | ✓ (cap≥n exact) |
| F631.3 SA-EXP-SHAPE | r30/90/110 PASS (α>0) | ✓ |
| F631.4 SA-NONNEG | r30/90/110 PASS | ✓ (lower-bound 유지) |
| F631.6 RULE-COVER | PASS (3/3) | ✓ |
| F631.7 ORDER-PRESERVE | single PASS + state-avg PASS | ✓ (rule110 최속 보존) |
| F631.8 SINGLE-ANCHOR | α 0.243/0.192/1.101 PASS | ✓ (H_625 회귀) |
| ln_natural self-check | PASS×3 | ✓ |

**총 18 PASS / 0 FAIL.**

---

## 6+ 앵커 & 교차참조

- **H_625** (predecessor, PR #1199) — n=5 single-state cap-sweep, gap 지수 감소
  α=0.243/0.192/1.101. 본 H_631 이 honest C3 #2 (state-averaged) 를 회수하고
  #1 (n=6) 를 시도→불가 판명.
- **축 B B1** — large-N bounded big-Φ n=8 도달 (M12/M13). cap≥n=exact 앵커.
- **축 B B2** — H_625 가 cap-sweep@fixed-n 로 회수, 축 B 2/2 closure. 본 H_631 은
  그 follow-up (state-average 차원 확장).
- **H_278** — small-N exact 앵커 (n=4/5 ring rule{30,90,110} faithful Φ 소스 진리).
- **[[reference-exact-phi-structure-wall-shard]]** — n≥6 exact phi_structure wall-time
  폭증 메모; 본 H 에서 n=6 cap=6 exact >10min 으로 정합 실증.

---

## 7. verdict

🟢 **SUPPORTED-NUMERICAL**

H_625 의 single-state exp-decay 가 **state-averaged 차원에서도 보존** 됨이
확증되었다 (H1). 그리고 α 의 rule 순서 (rule110 class-IV 최속 ≫ rule30/90) 가
single-state 와 state-averaged 양쪽에서 동일하게 유지됨이 확증되었다 (H2,
F631.7). H_625 honest C3 #2 (single-state only) 가 회수된다.

핵심 발견:

- **state-averaging 이 exp-decay 형상을 깨지 않는다** — single-state 의 특이한
  representative 선택 효과가 아니라, gap 의 지수 감소가 substrate 의
  *구조적* 성질임을 시사. α 절대값은 약간 이동하나 (rule30 0.243→0.326,
  rule110 1.101→1.022) 부호·순서·형상 모두 보존.
- **rule110 (class-IV) 의 빠른 수렴은 state-robust** — state-averaging 후에도
  rule110 α≈1.02 ≫ rule30 α≈0.33 ≫ rule90 α≈0.19. bounded restriction 이
  integrable/class-IV purview 구조에 잘 맞고 XOR-style mixing(rule90) 에서
  high-cap purview 가 본질적이라는 H_625 해석이 state-level 에서 강화.
- **cap=1,2 동률 패턴 보존** — rule30/90 의 g@1=g@2 (purview 크기 1,2 동일
  lower-bound) 가 state-avg 에서도 유지 (rule30 39.44=39.44, rule90 50.88=50.88).

---

## 8. 한계와 honest C3 (10 항)

1. **n=6 확장 실패 — 계산 불가 판명**. 본 H 의 1차 목표였던 n=6 cap-sweep 은
   timing-probe 로 **불가** 확정: n=6 cap=6 exact 단일 state > **10분**
   (10:54 elapsed 에서 kill), cap=5 > 2분, cap=4 > 3분 — 모든 cap 이 60s 예산
   초과. 원인 = bounded big-Φ 의 2nd-order relation 비용이 surviving-distinction
   nd² 로 폭증 (cap 은 large purview 만 자르고 n=6 에서 nd 는 여전히 큼).
   [[reference-exact-phi-structure-wall-shard]] 정합. → 사전 지정 fallback
   "n=6 timeout 시 n=5 state-averaged demote" 발동.
2. **전 32-state 평균 미달 — 8-state 부분집합**. n=5 전 32-state 평균조차
   contended 환경에서 ~5:30 CPU 에서 SIGKILL(메모리 압박, 3 rule 모두). cap=5
   exact 가 high-Φ state(st=31 all-ones 등) 에서 maximal distinction → nd² relation
   폭증이 원인. **8-state Hamming-stratified 대표 부분집합** {0,1,3,7,15,31,21,10}
   으로 demote (full 32-state 아님). 부분집합은 weight 0..5 를 span 하나 균등
   가중 아닌 stratified sample.
3. **3 rule 만** — 256 rule sweep 아님 (H_625 동일 한계, {30,90,110}=정규 anchor).
4. **α 가 3-ratio mean** — gap(5)=0 라 r45 ill-defined → 유효 ratio (r12,r23,r34) 만.
5. **C 미공개** — `exp(−α·k)` least-squares fit 아닌 ratio-mean α 추출 (H_625 동일).
6. **rule30/90 r12=1.0** — cap1,2 동값 → 첫 ratio=1(decay=0), α 평균 보수적.
7. **cap=5=exact 정의 의존** — `big_phi_bounded(cap≥n)` faithful restriction stdlib
   보증 (M12 regression anchor) 에 의존.
8. **gap 절대값 = IIT4 Φ 단위 (비정규화)** — cross-rule α 비교는 유효, cross-substrate
   비교는 추가 정규화 필요. state-avg gap 절대값 ≠ single-state (앙상블 평균이라
   더 큼) 은 정상.
9. **state subset 선택 임의성** — {0,1,3,7,15,31,21,10} 은 weight-span 기준
   수작업 선택. 다른 8-subset 또는 full-32 가 α 절대값을 미세 이동시킬 수 있음
   (형상·순서 결론은 robust 예상, 미측정).
10. **rule-class → α magnitude mapping** = 여전히 후속 (H_625 C3 #10 연장) —
    본 H 는 "state-averaged 형상·순서 보존" 만 검증, class-IV≫chaotic,linear 의
    정량 mapping 은 별도 H.

---

## 9. artefacts

- `UNIVERSE/state/h631_bounded_gap_n6_multi_rule_2026_05_28/single5.hexa` (single-state 측정)
- `UNIVERSE/state/h631_bounded_gap_n6_multi_rule_2026_05_28/savg_sub.hexa` (8-state 평균 측정)
- `UNIVERSE/state/h631_bounded_gap_n6_multi_rule_2026_05_28/finalize.hexa` (gap+α+18 falsifier)
- `UNIVERSE/state/h631_bounded_gap_n6_multi_rule_2026_05_28/run_h631.hexa` (n=5 통합 harness — full 32-state 버전, SIGKILL 됨, 참고용 보존)
- `UNIVERSE/state/h631_bounded_gap_n6_multi_rule_2026_05_28/run.log` (consolidated stdout + n=6 timing findings)

비용 = $0 · LLM = 사용 안 함 · GPU = 사용 안 함 · 결정론적 hexa run.

---

## 10. 후속

- H_631b — n=6 bounded-gap = **shard-architecture 필수** (per-rule per-cap 분리 +
  phi-free aggregate, [[reference-exact-phi-structure-wall-shard]] 정석). 또는
  cap≤3 만 (relation nd² 통제 가능 영역) n=6 partial sweep.
- H_631c — full 32-state 평균 = 대형-메모리 host (pool ubu-*) 또는 cap-stratified
  분할 실행 후 재집계.
- H_631d — rule-class(I/II/III/IV) → α magnitude 정량 mapping (H_625 C3 #10 회수).
- 본 H 는 축 B B2 의 state-average 차원만 추가 — 축 B closure(2/2) 는 H_625 에서 이미 달성.
