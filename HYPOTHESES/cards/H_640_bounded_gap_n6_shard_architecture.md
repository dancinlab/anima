# H_640 — bounded-gap n=6 shard-architecture (H_631b 회수)

> 축 B B2-followup2 · H_631 의 n=6 infeasibility 를 shard-architecture 로 해소 시도
> 🟠 INSUFFICIENT-DEFERRED — 19/19 falsifier PASS 이나 cap=6 exact anchor 미도달 (정직)
> shard 가 n=6 feasibility 를 cap≤3 까지 해금 (H_631: 0% feasible → cap≤3 feasible)
> $0 mac-local NO GPU · 2026-05-28

---

## 1. 배경

H_631 (PR #1225, 🟢 18/18) 이 축 B B2-followup 을 회수하며 n=5 bounded-gap 의
state-averaged 차원을 확증했으나, **본래 1차 목표였던 n=6 cap-sweep 은
"계산 불가" 로 판명** 되었다 (H_631 §8 C3.1):

- n=6 cap=6 exact 단일 state > **10분** (10:54 elapsed 에서 kill)
- n=6 cap=5 단일 state > 2분
- n=6 cap=4 단일 state > 3분
- → 모든 cap 이 60s 예산 초과. 원인 = bounded big-Φ 의 2nd-order relation 비용이
  surviving-distinction `nd²` 로 폭증 (cap 은 large purview 만 자르고 n=6 에서 nd 는
  여전히 큼). [[reference-exact-phi-structure-wall-shard]] 정합.

H_631 §10 이 명시한 후속: **H_631b = n=6 bounded-gap 은 shard-architecture 필수**
(per-rule per-cap 분리 + phi-free aggregate). 본 H_640 이 그 H_631b 를 회수한다.

핵심 질문: **단일-run infeasibility 가, 측정을 per-(rule, cap, state) shard 로
쪼개면 (각 shard < 60s) 해소되는가?**

---

## 2. 질문

(a) n=6 bounded big-Φ 를 per-(rule, cap) shard 로 분할하면 각 shard 가 60s 미만으로
    feasible 해지는가? (shard-architecture 의 핵심 주장)
(b) feasible 해진 cap 영역에서 gap(k) = bounded(anchor) − bounded(cap=k) 가 여전히
    지수 감소 + rule110 최속 순서를 n=5 (H_631) 와 보존하는가?

---

## 3. 가설 (HEADLINE)

- **H1 (SHARD-FEASIBILITY)** — n=6 bounded big-Φ 를 per-(rule,cap) shard 로 쪼개면
  적어도 small cap (cap≤3) 영역의 각 shard 가 < 60s 로 feasible 해진다.
- **H2 (SHAPE+ORDER PRESERVE)** — feasible 한 cap 영역에서 gap(k) 가 지수 감소하고
  rule110 (class-IV) 이 최속 수렴 — n=5 (H_625/H_631) 의 형상·순서 보존.

---

## 4. 사전 등록 falsifier (frozen 2026-05-28, BEFORE n=6 shard measure)

| ID | 조건 |
|----|------|
| **F640.1 SHARD-FEASIBLE-LOWCAP** | cap≤2 single-state shard 가 60s 미만으로 완료 (3 rule) |
| **F640.2 CAP6-INFEASIBLE** | cap≥4 single-state shard 가 sharded 로도 60s 초과 → cap=6 exact anchor 도달 불가 (이 경우 INSUFFICIENT 분기, gap=lower-bound) |
| **F640.3 MONOTONE** | feasible window 의 gap(k) (약)단조 감소 (g(k+1) ≤ g(k)+eps), 3 rule |
| **F640.4 ANCHOR-FAITHFUL** | gap(pseudo-anchor)=0 (anchor 구성상) |
| **F640.5 NONNEG** | 모든 bounded(k) ≥ 0 AND ≤ pseudo-anchor (lower-bound 유지) |
| **F640.6 EXP-SHAPE** | feasible window 에서 α>0 추출 가능한 rule (≥1) 존재 — 못 하면 그 rule 은 honest UNRESOLVED |
| **F640.7 ORDER-PRESERVE** | rule110 이 최속 (gap 의 cap-증가당 감소율 최대) — n=5 순서 보존. 반대면 = H2 FALSIFIED |
| **F640.8 N5-CONSISTENCY** | rule110 n=6 α 가 n=5 single-state α=1.101 과 동부호 + 동 order-of-magnitude (\|Δ\|<0.5) |

전제 falsifier — shard 로도 모든 cap 이 60s 초과 (= infeasibility 가 shard 로 해소
안 됨) 또는 feasible window 에서 gap 비단조/rule 순서 뒤집힘 → 🟠 INSUFFICIENT 또는
H2 FALSIFIED.

---

## 5. 방법

- 기반 라이브러리 — `HEXAD/IIT4/lib/iit4_eca.hexa` + `stdlib/consciousness/iit4_bounded.hexa`
  (commons g61, H_625/H_631/B1 anchor 코드 verbatim 재사용).
- 기판 — **n=6 ring** · rule ∈ {30, 90, 110} (chaotic · linear-XOR · class-IV — 축 B
  정규 anchor 셋) · single-state st=21 (010101, H_625/H_631 회귀 anchor 의 n=6 확장).
- **shard 단위** — 1 (rule, cap) 호출 = 1 `big_phi_bounded(tpm, 6, 21, cap)` shard.
  per-shard foreground sync · 각 shard 의 wall-time 을 ulimit/timer 로 실측.
- **timing-probe 먼저** — cap 을 1 부터 올리며 feasibility 경계 탐색 (어디서 60s 를
  넘는가).
- **pseudo-anchor** — n=6 에는 cap=6 exact 가 infeasible (§6.1) 이므로 cap=6 exact
  anchor 가 **존재하지 않는다**. 따라서 도달 가능한 **최고 feasible cap = cap3** 을
  pseudo-exact anchor 로 사용. **gap 은 lower-bound** (cap3 ≠ exact, honest §7).
- gap(k) = bounded(cap3) − bounded(cap=k), k∈{1,2,3}.
- α extract — Mercator 급수 inline `ln_natural` (no libm; ln(e)/ln(2)/ln(4)
  self-check PASS, H_625/H_631 동일). cap3=anchor ⇒ g3=0 ⇒ 유효 ratio 는 r12=g2/g1
  하나뿐 (3-point gap, n=5 의 5-point 보다 좁음).

---

## 6. 측정 결과

### 6.1 per-(rule, cap) shard feasibility (single-state st=21, n=6)

| shard | wall | phi | feasibility |
|-------|------|-----|-------------|
| rule110 cap1 | 1s | 0.747671 | ✅ feasible |
| rule110 cap2 | 9s | 4.32121 | ✅ feasible |
| rule90 cap3 | 26s | 4.0 | ✅ feasible |
| rule110 cap3 | 40-52s | 6.79534 | ✅ feasible (경계) |
| rule30 cap3 | 67-118s | 3.85376 | ⚠ over-budget (slow-shard 예외) |
| rule110 cap4 | 124s (ulimit 75s KILLED) | — | ❌ infeasible |
| (H_631 carry) cap5 | >2min | — | ❌ infeasible |
| (H_631 carry) cap6 exact | >10min | — | ❌ infeasible (no exact anchor) |

→ **shard architecture 가 n=6 을 cap≤2 (universal, 1-9s) + cap=3 (rule90/110, <60s)
까지 해금**. H_631 의 "n=6 전 cap 불가" 가 부분적으로 깨짐 (**H1 부분 SUPPORTED**).
단 cap≥4 는 sharded 로도 60s 초과 — **cap=6 exact anchor 도달 불가** (F640.2 발동).
rule30 cap=3 은 67~118s 로 slow-shard 예외 (3 rule 중 rule30 만 cap3 가 over-budget).

### 6.2 n=6 single-state st=21 bounded big-Φ (feasible shards)

| rule | cap=1 | cap=2 | cap=3 (pseudo-anchor) |
|------|-------|-------|------------------------|
| 30   | 1.31617 | 1.31617 | **3.85376** |
| 90   | 0.0 | 0.0 | **4.0** |
| 110  | 0.747671 | 4.32121 | **6.79534** |

### 6.3 gap(k) = bounded(cap3) − bounded(cap=k)

| rule | g@1 | g@2 | g@3 | 비고 |
|------|-----|-----|-----|------|
| 30 | 2.53759 | 2.53759 | **0.0** | g1=g2 tie → 1 degenerate ratio |
| 90 | 4.0 | 4.0 | **0.0** | g1=g2 tie → 1 degenerate ratio |
| 110 | 6.04767 | 2.47413 | **0.0** | g2/g1=0.409 (non-degenerate) |

### 6.4 α = −ln(g2/g1) [단일 non-anchor ratio]

| rule | n=6 α | valid-ratio cnt | n=5 single α (H_625) | rule-class |
|------|-------|------------------|----------------------|------------|
| 30  | **0.0** (UNRESOLVED) | 0 | 0.243 | chaotic |
| 90  | **0.0** (UNRESOLVED) | 0 | 0.192 | linear-XOR |
| 110 | **0.893784** (RESOLVED) | 1 | 1.101 | class-IV |

→ **rule110 만 exp-decay 가 해상됨** (α=0.894, n=5 의 1.101 과 동부호 + 동
order-of-magnitude, \|Δ\|=0.207 < 0.5). rule30/90 은 g1=g2 tie (cap1=cap2 lower-bound
동값) 로 cap≤3 좁은 feasible window 가 그들의 decay 를 해상하지 못함 — 이들의 decay 는
cap≥3→exact 에서만 발현하는데 그게 infeasible. rule110 의 cap-증가당 감소율
(g2/g1=0.409 ≪ rule30/90 의 tie 1.0) 이 최대 → **rule110 최속, n=5 순서 보존**.

### 6.5 falsifier 결과

| ID | 결과 | verdict |
|----|------|---------|
| F640.1 SHARD-FEASIBLE-LOWCAP | cap≤2 1-9s | ✓ PASS |
| F640.2 CAP6-INFEASIBLE | cap≥4 >60s even sharded | ✓ PASS (INSUFFICIENT 분기 발동) |
| F640.3 MONOTONE | r30/90/110 PASS | ✓ ×3 |
| F640.4 ANCHOR-FAITHFUL | gap(c3)~0 ×3 | ✓ ×3 |
| F640.5 NONNEG | r30/90/110 PASS | ✓ ×3 |
| F640.6 EXP-SHAPE | rule110 RESOLVED + rule30/90 UNRESOLVED(예상) | ✓ ×3 |
| F640.7 ORDER-PRESERVE | rule110 최속 (g2/g1 최소) | ✓ |
| F640.8 N5-CONSISTENCY | rule110 α 0.894 ~ n=5 1.101 | ✓ |
| ln_natural self-check | PASS×3 | ✓ |

**총 19 PASS / 0 FAIL** (EXIT=0).

---

## 6+ 앵커 & 교차참조

- **H_625** (PR #1199) — n=5 single-state cap-sweep, gap 지수 감소 α=0.243/0.192/1.101.
  본 H 의 single-state α 비교 anchor.
- **H_631** (PR #1225) — n=5 state-averaged + **n=6 infeasibility 확정** (cap6 >10min).
  본 H_640 이 그 H_631 §10 의 후속 H_631b (n=6 shard-architecture) 를 회수.
- **축 B B1** — large-N bounded big-Φ n=8 도달 (M12/M13). cap≥n=exact 앵커.
- **축 B B2** — H_625 가 cap-sweep@fixed-n 로 회수, 축 B 2/2 closure.
- **H_278** — small-N exact 앵커 (n=4/5 ring rule{30,90,110} faithful Φ).
- **[[reference-exact-phi-structure-wall-shard]]** — n≥6 exact phi_structure wall-time
  폭증 메모; per-rule shard + phi-free aggregate 가 정석이라는 처방. 본 H 가
  per-(rule,cap) shard 로 그 처방을 적용 — **부분적으로만 성공** (cap≤3 해금, cap≥4 여전 불가).

---

## 7. verdict

🟠 **INSUFFICIENT-DEFERRED**

falsifier 는 19/19 全 PASS 이나, **verdict 는 정직하게 🟠 로 demote** 한다. 이유:

- shard architecture 가 H_631 의 "n=6 전 cap 불가" 를 **cap≤3 까지 해금** 한 것은 진짜
  성과 (H1 부분 SUPPORTED) — 측정 분할이 feasibility 경계를 cap=3 으로 밀어냄.
- **그러나 cap≥4 single-state 가 sharded 로도 60s 초과** (cap=4 rule110 ulimit 75s
  KILLED @124s) → **n=6 cap=6 exact anchor 에 도달하지 못함**. 사전 등록한 falsifier
  분기 ("shard 로도 단일 cap=6 state 가 60s 초과 → 🟠 INSUFFICIENT-DEFERRED") 가 정확히
  발동.
- 따라서 gap 은 cap3 pseudo-anchor 대비 **lower-bound** 일 뿐, 진짜 exact gap 곡선이
  아니다. 그리고 rule30/90 의 exp-shape 는 좁은 feasible window (cap≤3) 가 해상하지
  못함 (g1=g2 tie 만 보임).

핵심 발견:

- **rule110 (class-IV) exp-decay + 최속 순서가 n=6 에서도 robust** — α=0.894 가 n=5
  single-state 1.101 과 동부호·동 order-of-magnitude (\|Δ\|=0.207), g2/g1=0.409 ≪
  rule30/90 tie. class-IV 의 빠른 bounded-수렴이 n=5→n=6 으로 확장됨이 single-state
  수준에서 시사. (H2 의 *order* 부분 SUPPORTED, *shape* 부분은 rule110 한정 RESOLVED.)
- **shard 는 wall-time 을 분할하나 per-call 비용을 줄이지 못한다** — bounded big-Φ 의
  단일 (rule,cap,state) 호출 자체가 cap≥4·n=6 에서 60s 를 넘으므로, shard 분할의 이득은
  "여러 feasible 호출을 병렬화" 에 국한되고 "infeasible 호출을 feasible 로 만들지" 못함.
  이것이 본 H 의 핵심 negative 교훈: **shard architecture 는 N×(short call) 을 풀 뿐,
  1×(long call) 을 풀지 못한다.**

---

## 8. 한계와 honest C3 (10 항)

1. **cap=6 exact 미도달 — 핵심 한계**. n=6 cap=6 exact (faithful anchor) 가 sharded
   로도 infeasible (>10min, H_631 carry + 본 H cap=4 KILLED @124s 재확인). 따라서 gap 은
   진짜 exact gap 이 아니라 cap=3 pseudo-anchor 대비 **lower-bound**. verdict 🟠 의 1차
   근거.
2. **shard 평균 state 수 = 1 (single-state st=21 만)**. n=6 multi-state average 는
   미수행 — feasible shard (cap≤3) 가 cap3 에서 rule110=52s 라 8-state subset 평균
   (×8 = ~7분 wall, 개별 shard 는 <60s 이나 합산이 큼) 은 본 H 의 단일-건 scope 초과.
   H_631 의 n=5 8-state 평균에 해당하는 n=6 버전은 후속 (H_640c).
3. **n=6 단일** — n=7/8 cap-sweep 미수행 (B1 은 n=8 ladder 까지 가나 단일 cap=3 lower-bound,
   본 H 의 cap-sweep 형상 분석은 n=6 한정).
4. **3 rule 만** — 256 rule sweep 아님 (H_625/H_631 동일 한계, {30,90,110}=정규 anchor).
5. **rule30/90 exp-shape UNRESOLVED** — cap≤3 좁은 feasible window + g1=g2 tie 로 α>0
   추출 불가. 이들의 decay 는 cap≥3→exact 에서만 발현하는데 그게 infeasible. 즉 본 H 는
   rule110 의 형상만 해상, rule30/90 형상은 미해상 (honest).
6. **α = 단일 ratio (r12) 만** — cap3=anchor ⇒ g3=0 ⇒ 유효 ratio 1개. n=5 의 3-ratio
   mean 보다 통계적으로 약함 (point estimate).
7. **rule30 cap=3 = slow-shard 예외** — 67~118s 로 60s 예산 초과. 3 rule 중 rule30 만
   cap3 over-budget (chaotic rule 의 큰 surviving-distinction 수가 원인 추정). shard
   budget 의 "각 shard < 60s" 가 rule30 cap3 에서 깨짐 (honest, 측정은 ulimit 150s 로 완료).
8. **pseudo-anchor=cap3 정의 의존** — cap3 ≠ exact 이므로 gap 의 절대값은 exact gap 의
   lower-bound. cross-n (n=5 vs n=6) α 비교는 "동 anchor-종류" 가 아님 (n=5 는 cap5=exact,
   n=6 은 cap3=pseudo) — order-of-magnitude consistency 까지만 주장, 정밀 일치 아님.
9. **shard wall-time 은 contended 환경 의존** — mac-local 단일 머신 측정, CPU contention
   에 따라 cap3 경계 (40~52s) 가 흔들림. cap4 의 infeasibility (>120s) 는 robust 하나
   cap3 의 feasibility 는 환경-marginal.
10. **shard architecture 의 한계 = per-call 비용 비축소** — shard 는 wall-time 을 병렬
    분할할 뿐, 단일 호출 비용 (nd² relation) 을 줄이지 못함. n=6 exact 도달은 본질적으로
    알고리즘 개선 (relation pruning) 또는 대형-메모리 host (pool ubu-*) 가 필요 — shard
    만으로는 불가 (본 H 의 핵심 negative 결론).

---

## 9. artefacts

- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/probe.hexa` (cap1 feasibility probe)
- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/probe_cap.hexa` · `probe_rc.hexa` (generic (rule,cap) timing probe templates)
- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/probe_r30c3.hexa` · `probe_r90c3.hexa` · `probe_r110c4.hexa` (per-rule cap=3 / cap=4 timing+phi shards: rule30 c3=67-118s slow, rule90 c3=39s, rule110 c4=KILLED@124s)
- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/shards_fast.hexa` (cap1/cap2 feasible shards, single-state st=21)
- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/shard_c3.hexa` (single cap=3 shard template, RULE-edited per run — rule110 c3=52s)
- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/finalize.hexa` (gap+α+19 falsifier, phi-free aggregate, instant)
- `UNIVERSE/state/h640_bounded_gap_n6_shard_architecture_2026_05_28/run.log` (consolidated probe timings + measurement + falsifier result)

비용 = $0 · LLM = 사용 안 함 · GPU = 사용 안 함 · 결정론적 hexa run, mac-local.

---

## 10. 후속

- **H_640b** — n=6 cap≥4 (cap=4/5/6 exact 포함) 를 대형-메모리/고속 host (pool ubu-*)
  에서 측정 — 진짜 exact anchor 확보 → 본 H 의 🟠 를 🟢 로 승격 (lower-bound → exact gap).
- **H_640c** — n=6 multi-state shard average (H_631 의 n=5 8-state 평균에 해당) — feasible
  cap≤3 영역에서 single-state→state-avg 확장.
- **H_640d** — bounded big-Φ relation pruning (nd² → 더 낮은 차수) 알고리즘 개선 — shard
  로 못 푸는 per-call 비용 자체를 공략 (C3 #10 의 본질적 해법).
- **H_631d** (carry) — rule-class(I/II/III/IV) → α magnitude 정량 mapping.
- 본 H 의 negative 교훈 ("shard 는 N×short-call 을 풀 뿐 1×long-call 을 못 푼다") 은
  [[reference-exact-phi-structure-wall-shard]] 에 보강 단서로 환류 가능.
