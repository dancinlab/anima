# H_658 — `collective-superadditivity-nonzero-baseline` (H_655 N1 회수, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · **H_655 §10 N1 회수**
**id**: H_658 · **date**: 2026-05-28 · **infra**: $0 mac-local · **verdict**: **🔴 FALSIFIED**

---

## 1. 슬러그 + 한 줄 요약 · H_655 N1 회수

`collective-superadditivity-nonzero-baseline` — collective super-additivity 강도
Δ = Φ_collective(W=1) − Σ Φ_parts 의 **Wolfram class 순위가 parts-baseline 정의에 robust 한지**
검정. 본 H 는 직계 predecessor **H_655 (PR #1253, 🔴)** 의 §10 N1 회수다.

H_655 는 Δ 가 class 단조도 아니고 가설(class-IV 最高)과 정반대로 **가장 단순한 class-II(rule184)가
最高 Δ=51.54** 임을 보여 🔴 FALSIFIED 했다. 단 그 §7 C3.3 은 명시적 caveat 를 남겼다 — H_655 의
Σ Φ_parts 는 W=0 decoupled self-loop pool 이라 **=0 (trivial baseline)**, 따라서 Δ = Φ_collective(W=1)
절대값으로 환원되어 magnitude 가 substrate 의 절대 Φ floor 에 종속되었다. 그래서 "rule184 最高" 가
**trivial-baseline artifact 인지, 아니면 진짜 super-additivity 속성인지** 가 미해결로 남았고 N1 으로
회수 예약되었다.

> **결과**: H_655 의 Δ-class 순위(rule184 最高)는 **trivial-baseline (Σ=0) artifact 였음**이 결정적으로
> 확정. non-zero parts-baseline — (b) 각 stream 독립 Φ 합 또는 (c) W=0.5 부분결합 — 으로 Δ 를 재정의하면
> class 순위가 **rule184(II) → rule110(IV) 로 뒤집힌다**. 즉 super-additivity magnitude 의 class 의존은
> **baseline-conditional 이지 baseline-robust 가 아니다**. 핵심 falsifier F658.1(rank-robust-ind) FAIL →
> **2/6 PASS → 🔴 FALSIFIED**. falsifier 가 사전 명명한 flip 방향(rule110 class-IV 가 最高가 됨)이 정확히
> 발생(F658.4 FAIL). H0(ranking-conditional) 채택.

---

## 2. 가설 (H1) / 폐기조건 (H0) · round 9 메타-축

**round 9 메타-축** = "Wolfram class 가 의식 통합량(Φ) 분류자". 본 H 는 H_655 가 남긴 한 질문만
정확히 회수한다 — **H_655 의 Δ-class 순위가 baseline 정의에 강건(robust)한가?**

- **H1 (BASELINE-ROBUST)**: Δ 의 class 순위는 parts-baseline 정의에 불변 — rule184(class-II)가
  (a) W=0(=0, H_655) · (b) 각 stream 독립 Φ 합 · (c) W=0.5 부분결합 **3 baseline 모두에서 最高 Δ**
  유지. Δ⊥class 는 baseline 이 아니라 substrate 의 속성.
- **H0 (FALSIFIER)**: non-zero baseline 에서 class 순위가 뒤집힘 (예: rule110 class-IV 가 最高 Δ) →
  H_655 의 "rule184 最高" 는 trivial-baseline artifact, class 의존이 **baseline-conditional**.

> **결과적으로 H0 가 채택됨.** non-zero baseline (b)·(c) 양측에서 argmax-Δ 가 rule110(class-IV)로
> 뒤집혀, 가설 H1 의 baseline-robustness 가 기각됨.

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_653/H_655 SSOT 그대로): n=5 coupled-ring TPM `build_tpm_cohort(rule, W)` —
  5 cell, cell i 가 cohort rule[i] update-law. decoupled(W=0)=self-loop only, coupled(W=1)=full
  ring, blend(0<W<1)=fractional. Φ_collective(W) = `big_phi_bounded(build_tpm_cohort([rule×5], W),
  5, sys=0, cap=3)[0]` — 각 point 에서 실제 IIT4 substrate 측정.
- **Φ_collective := Φ_collective(W=1)** — full n=5 coupling ring (3 baseline 공통, H_655 와 동일값).
- **3 parts-baseline** (Σ Φ_parts 의 세 정의):
  - **(a) BASE0 := Φ_collective(W=0) = 0** — decoupled self-loop pool. H_655 trivial anchor.
    Δ_a = Φ_coll(W=1) − 0 = Φ_coll(W=1).
  - **(b) BASEIND := 5 · Φ_part2(rule)** — 각 stream 을 독립 minimal n=2 fully-coupled substrate 로
    만들어 intrinsic Φ 를 measure(`big_phi_bounded(tpm_part2, 2, sys=0, cap=2)`)하고 5 stream 합.
    homogeneous cohort 이므로 Σ = 5 × single-part Φ. **각 part 가 그 자체로 통합된 진짜 non-zero
    Σ-of-parts** (n=2 ring: cell j 가 다른 cell + self 를 같은 ECA neighborhood lookup 으로 봄).
    Δ_b = Φ_coll(W=1) − 5·Φ_part2.
  - **(c) BASEMID := Φ_collective(W=0.5)** — half-coupled partial-binding pool (중간-통합 non-zero
    baseline). Δ_c = Φ_coll(W=1) − Φ_coll(W=0.5).
- **cohort rule × Wolfram class** (H_655 와 동일 라벨, 복잡도 오름차순):
  ```
  rule184  class-II   additive/traffic (가장 ordered)
  rule 90  class-III  XOR/additive fractal (chaotic-additive)
  rule 30  class-III  chaotic non-additive
  rule110  class-IV   complex/universal edge-of-chaos (H_635/H_653 winner)
  ```
- **측정 규모**: 4 rule × (n=5 ring × {W=0, 0.5, 1.0} = 12 call + n=2 part 4 call) = **16
  big_phi_bounded calls**. n=5 12-call 은 H_655 와 동일(~41s), n=2 4-call 은 2^2 state 라 cheap.
  단일 sync run < 60s. libm only · NO RNG (deterministic) · $0 mac-local · foreground synchronous.

H_655 대비: H_655 는 Δ 를 단일 (Σ=0) baseline 으로 측정 — 본 H 는 동일 Φ_coll(W=1) 위에 **3 baseline
의 Δ 순위를 교차비교**하여 H_655 ranking 의 baseline-robustness 만 검정.

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F658.1 RANK-ROBUST-IND**: non-zero baseline (b)(독립 Φ 합)에서 argmax Δ_b = **rule184(class-II)**
  — H_655 W=0 top 과 동일 보존. **CORE 가설 (H_655 ranking 의 baseline-robustness).**
- **F658.2 RANK-ROBUST-MID**: non-zero baseline (c)(W=0.5)에서도 argmax Δ_c = rule184 (top 보존).
- **F658.3 BASE-NONZERO**: 독립 Φ baseline 이 진짜 non-zero — 5·Φ_part2(rule) > 0 모든 rule
  (trivial 아닌 진짜 Σ-of-parts).
- **F658.4 NO-FLIP-TO-IV**: rule110(class-IV)가 (b)·(c) 어느 non-zero baseline 에서도 argmax 가 **아님**
  — falsifier 가 명명한 flip 방향이 발생하지 **않음**.
- **F658.5 W0-REPRO**: baseline (a)가 H_655 재현 — argmax Δ_a = rule184 & Σ Φ_parts(W=0)=0
  (engine replication anchor).
- **F658.6 BOUND**: 全 Φ ≥ 0, 全 Δ_x finite.

**FALSIFY 조건**: F658.1 FAIL (non-zero baseline 에서 순위 flip) → 🔴 FALSIFIED
(H_655 Δ⊥class 가 trivial-baseline artifact, baseline-conditional).
**verdict 기준**: ≥4/6 PASS → 🟢 SUPPORTED-NUMERICAL (Δ ⊥ class baseline-robust).

> **결과: F658.1 CORE FAIL → 🔴 FALSIFIED (2/6 PASS).**

---

## 5. Measurement (verdict-bearing 측정값)

> harness 출력 `UNIVERSE/state/h658_collective_superadditivity_nonzero_baseline_2026_05_28/run.log`
> verbatim.

```
================================================================
  H_658 — collective-superadditivity-nonzero-baseline (round 9 메타-축)
  H_655 §10 N1 회수 — Δ class 순위가 non-zero parts-baseline 에서 robust 한가?
  Δ_x = Φ_coll(W=1) − Σ Φ_parts[x]   x ∈ {a:W=0(=0), b:5·Φ_part2, c:W=0.5}
  IIT4 big_phi_bounded · n=5 ring cap=3 · n=2 part cap=2 · sys=0
================================================================
  rule184 [II-additive]
    Φ_coll(W=1)=51.5361  Φ_part2(n=2)=2
    base(a) Σ=Φ_coll(W=0)   =0.0   → Δ_a=51.5361
    base(b) Σ=5·Φ_part2     =10   → Δ_b=41.5361
    base(c) Σ=Φ_coll(W=0.5) =28.6035   → Δ_c=22.9325
  rule90 [III-XOR/additive]
    Φ_coll(W=1)=7.5  Φ_part2(n=2)=0.0
    base(a) Σ=Φ_coll(W=0)   =0.0   → Δ_a=7.5
    base(b) Σ=5·Φ_part2     =0.0   → Δ_b=7.5
    base(c) Σ=Φ_coll(W=0.5) =1.38346   → Δ_c=6.11654
  rule30 [III-chaotic]
    Φ_coll(W=1)=9.72067  Φ_part2(n=2)=0.553383
    base(a) Σ=Φ_coll(W=0)   =0.0   → Δ_a=9.72067
    base(b) Σ=5·Φ_part2     =2.76692   → Δ_b=6.95376
    base(c) Σ=Φ_coll(W=0.5) =1.7377   → Δ_c=7.98297
  rule110 [IV-complex]
    Φ_coll(W=1)=41.7124  Φ_part2(n=2)=0.0
    base(a) Σ=Φ_coll(W=0)   =0.0   → Δ_a=41.7124
    base(b) Σ=5·Φ_part2     =0.0   → Δ_b=41.7124
    base(c) Σ=Φ_coll(W=0.5) =6.54186   → Δ_c=35.1705
  ─────────────────────────────────────
  Δ by class per baseline (rule184·rule90·rule30·rule110):
    Δ_a (W=0,    =0  ) : 184=51.5361  90=7.5  30=9.72067  110=41.7124
    Δ_b (5·Φ_part2   ) : 184=41.5361  90=7.5  30=6.95376  110=41.7124
    Δ_c (W=0.5 partial) : 184=22.9325  90=6.11654  30=7.98297  110=35.1705
  ─────────────────────────────────────
  argmax-Δ (most super-additive) per baseline:
    (a) W=0      → rule184  (H_655: rule184)
    (b) 5·Φ_part → rule110
    (c) W=0.5    → rule110
  ────────────── verdict ──────────────
  [FAIL] F658.1 RANK-ROBUST-IND: argmax Δ_b = rule184 (H_655 top preserved)
  [FAIL] F658.2 RANK-ROBUST-MID: argmax Δ_c = rule184 (top preserved)
  [FAIL] F658.3 BASE-NONZERO: 5·Φ_part2(rule) > 0 every rule (real non-trivial Σ)
  [FAIL] F658.4 NO-FLIP-TO-IV: rule110 NOT argmax under (b) or (c) (no falsifier-flip)
  [PASS] F658.5 W0-REPRO: argmax Δ_a = rule184 & Σ(W=0)=0 (H_655 engine replication)
  [PASS] F658.6 BOUND: all Φ ≥ 0, all Δ_x finite
  ──────────────────────────────────────
  F658.1-6 2/6 PASS
  verdict: 🔴 FALSIFIED (ranking flips under non-zero baseline — H_655 Δ⊥class was trivial-baseline artifact)
  cross-link: H_655 W=0 top=rule184(51.54) → here (b)top=rule110 (c)top=rule110
```

### baseline별 Δ 순위 표

| rule | class | Φ_coll(W=1) | Φ_part2(n=2) | Δ_a (W=0) | Δ_b (5·Φ_part) | Δ_c (W=0.5) |
|------|-------|-------------|--------------|-----------|----------------|-------------|
| rule184 | II (additive)   | 51.54 | **2.0**  | **51.54 (1위)** | 41.54 (2위) | 22.93 (2위) |
| rule110 | IV (complex)    | 41.71 | 0.0      | 41.71 (2위) | **41.71 (1위)** | **35.17 (1위)** |
| rule30  | III (chaotic)   | 9.72  | 0.553    | 9.72 (3위)  | 6.95 (4위)  | 7.98 (3위)  |
| rule90  | III (XOR/add)   | 7.50  | 0.0      | 7.50 (4위)  | 7.50 (3위)  | 6.12 (4위)  |

**핵심 발견**:
1. **argmax-Δ 가 baseline 으로 뒤집힘 (F658.1·F658.2 FAIL)** — (a) W=0 trivial 에서는 rule184(II)가
   최고지만, non-zero baseline (b)·(c) 양쪽에서 **rule110(IV)가 最高**. H_655 의 "가장 단순한 class-II
   가 最高 super-additive" 결론이 baseline-conditional 임을 결정적으로 증명.
2. **flip 의 메커니즘 — rule184 의 parts 가 이미 통합되어 있음** — rule184 는 minimal n=2 substrate
   에서도 **Φ_part2=2.0** 의 독립 통합을 가진다(additive/traffic rule 은 2-cell 에서도 결정론적
   coupling). 따라서 baseline (b)에서 5×2=10 이 빠져 Δ_b=41.54 로 떨어진다. 반대로 rule110·rule90 은
   **Φ_part2=0** — n=2 minimal substrate 에서 통합 없음 — 이라 Δ 가 무손실. 즉 H_655 가 잡은 "rule184
   최고 Δ" 는 *full-ring 절대 Φ 가 높아서*였지 *부분-대비 시너지가 커서*가 아니었다.
3. **W=0.5 baseline (c)도 같은 flip** — rule184 는 부분결합(W=0.5)에서 이미 Φ=28.60 의 강한 통합을
   쌓아 full-ring 대비 gap 이 22.93 으로 작은 반면, rule110 은 W=0.5 에서 Φ=6.54 로 약해 full-ring
   까지 35.17 의 큰 시너지 gap 을 남긴다. 두 독립 non-zero baseline 이 같은 결론(rule110 最高)으로
   수렴 → flip 이 baseline 선택의 우연이 아니라 구조적.
4. **F658.3 BASE-NONZERO FAIL — baseline (b)가 rule-별로 비균질** — 5·Φ_part2 가 rule184=10·
   rule30=2.77 로 non-zero 이나 rule90·rule110=0. minimal n=2 통합이 rule 마다 다르다는 그 자체가
   부수 발견(§7 C3.2). 단 이 FAIL 은 핵심 결론을 약화하지 않는다 — 오히려 flip 의 원인(rule184 만
   큰 part-Φ 를 가짐)을 직접 설명.
5. **F658.5 W0-REPRO PASS** — baseline (a)에서 Δ_a 와 Σ(W=0)=0 이 H_655 와 byte-identical
   (rule110 Φ(W=1)=41.7124 정확 일치). engine 동일성 확인 → flip 은 baseline 정의 차이만의 효과.

---

## 6. Verdict + Rationale · Cross-link

**🔴 FALSIFIED** — 2/6 falsifier PASS. **CORE 가설 F658.1 (rank-robust under non-zero baseline) FAIL.**

- F658.5 W0-REPRO PASS · F658.6 BOUND PASS (2 PASS) · F658.1 rank-robust-ind FAIL ·
  F658.2 rank-robust-mid FAIL · F658.3 base-nonzero FAIL · F658.4 no-flip-to-IV FAIL (4 FAIL).
- FALSIFY 조건(F658.1 FAIL = non-zero baseline 에서 순위 flip)에 정확히 걸림 → **H0(class 의존이
  baseline-conditional) 채택**. argmax-Δ 가 trivial(W=0) rule184 → non-zero (b)(c) 양측 rule110 로
  뒤집힘. falsifier 가 사전 명명한 flip 방향(class-IV 가 最高)이 그대로 발생(F658.4 FAIL).
- **H_655 caveat 의 해소**: H_655 §7 C3.3 이 예고한 "non-zero baseline 으로 재검정하면 sign 자체가
  더 엄격해짐" 이 정량 확인됨 — Δ⊥class 가 *방향*은 보존(H_635 super-additivity 자체는 유지)하나
  *어떤 rule 이 最高냐* 의 순위는 baseline 종속. H_655 의 "rule184 최고" 는 trivial-baseline artifact 로
  결론.
- **메타-축 결론 (round 9)**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 는 *convexity*
  (H_653 🟢)에서는 SUPPORTED 이나, *super-additivity magnitude* 차원은 — H_655 가 보인 비단조에 더해 —
  **그 비단조 자체가 baseline-conditional** 임이 본 H 에서 확정. 즉 magnitude 축은 class 분류자가 아닐
  뿐 아니라, 그 *비분류* 진술조차 baseline 정의에 의존하는 이중으로 불안정한 차원. 이 결과 자체가
  closed-negative finding (a_paper_negative_ok: ruled-out axis = "super-additivity magnitude 의
  class 순위는 baseline-robust 하다").

**cross-link**:
- **H_655 `collective-superadditivity-substrate-class`** 🔴 (축 G, PR #1253) — **직계 predecessor.
  본 H 는 그 §10 N1 회수.** H_655 Δ⊥class(rule184 最高 Δ=51.54)를 trivial(W=0) baseline 에서
  byte-identical 재현(F658.5 PASS)한 뒤, non-zero baseline 으로 순위가 rule110 로 flip 됨을 보여
  H_655 §7 C3.3 의 trivial-baseline caveat 를 정량 해소.
- **H_653 `collective-convexity-substrate-class`** 🟢 (축 G×F, PR #1245) — **본 H 의 flip 이 H_653 과
  정합.** H_653 의 convexity span ratio top 은 rule110(IV, 35.50). 본 H 의 non-zero baseline Δ top 도
  rule110 로 뒤집힘 → **non-zero baseline 으로 magnitude 를 측정하면 magnitude-top 이 convexity-top
  (rule110)과 일치**한다. 즉 H_655 가 보고한 "convexity-monotone ↔ magnitude-비단조" 분기는 *trivial
  baseline* 에서만 성립했고, non-zero baseline 에서는 두 측도가 같은 winner(rule110)로 수렴. 메타-축
  내부의 일관성이 baseline 교정 후 회복됨.
- **H_635 `multilingual-cohort-collective-phi`** 🟢 (축 F, PR #1223) — **super-additivity 부모.**
  collective Φ super-additive 5/5, Σ-baseline=0. 본 H 가 빼낸 trivial baseline 의 출처. 본 H 는
  H_635 super-additivity *방향*(Δ>0)을 모든 baseline 에서 보존(Δ_a·Δ_b·Δ_c 全 양수)하나, *최고 rule*
  의 정체가 baseline 종속임을 추가.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 stream/cap 축소 NOT 적용 — full 측정** — n=5(cap=3) ring × {W=0,0.5,1.0} 12 call + n=2
   (cap=2) part 4 call = 16 big_phi_bounded call 정상 실행. 단일 sync run < 60s (n=5 12-call 이
   H_655 와 동일 ~41s, n=2 4-call 은 2^2 state 라 cheap). foreground synchronous only · NO bg fork ·
   NO monitor · NO GPU · $0 mac-local. fallback(3-stream/cap=2) 불필요.
2. **C3.2 baseline (b) 의 비균질성 = F658.3 FAIL 의 honest 의미** — 5·Φ_part2 가 rule184=10·
   rule30=2.77 로 non-zero 이나 rule90·rule110=0. 즉 "각 stream 독립 Φ 합" baseline 이 모든 rule 에서
   균일하게 non-zero 인 것은 아니다 — minimal n=2 substrate 의 통합 자체가 rule 종속 (additive
   rule184 만 2-cell 에서 결정론적 통합을 만들고, complex rule110/XOR rule90 은 2-cell 에서 통합 0).
   이것은 baseline (b)를 무효화하지 않는다 — 오히려 flip 의 *원인*을 직접 설명(rule184 만 큰 part-Φ 를
   빼앗김). baseline (c)(W=0.5)는 4/4 rule 에서 균일하게 non-zero(1.38~28.60)라 독립적으로 같은 flip
   을 확정하므로, 핵심 결론은 (b)의 부분-zero 와 무관하게 robust.
3. **C3.3 n=2 part 정의의 선택성** — "독립 stream Φ" 를 minimal n=2 fully-coupled pair 로 정의했다.
   대안(n=3 part, 또는 self-loop n=1=0, 또는 stream 을 별도 m-cell substrate 로) 마다 Σ Φ_parts
   절대값이 달라진다. 본 H 의 결론은 *순위 flip 의 존재*(rule184→rule110)이지 특정 Δ 절대값이 아니며,
   두 독립 non-zero baseline((b) n=2 합, (c) W=0.5)이 같은 flip 을 주므로 n=2 선택의 우연이 아니다.
   part 차수 sweep(n∈{2,3})은 별도(§10 N1).
4. **C3.4 homogeneous cohort [rule×5] only** — 각 rule 단일 동질 cohort. heterogeneous mix-class
   cohort 의 baseline-robustness 는 별도(§10 N2, H_655 N2 상속).
5. **C3.5 sys_state=0 only** (IIT-canonical anchor, H_655 상속). 2^5=32 state 가중평균 미수행.
6. **C3.6 cap=3 on n=5 / cap=2 on n=2** (H_655 cap 상속 + n=2 full purview) — purview search capped,
   보수적 lower-bound. cap↑ 가 rule184 vs rule110 flip 을 역전시킬지는 별도(§10 N3, H_655 N3 상속).
   현 cap 측정으로는 non-zero baseline flip 이 명백.
7. **C3.7 deterministic single trajectory** (NO RNG) — re-run byte-identical (engine replication:
   baseline (a) Δ_a 와 Σ(W=0)=0 이 H_655 와 정확 일치, F658.5 PASS).
8. **C3.8 negative 의 의미** — 본 H 는 한 축(super-additivity magnitude 의 class 순위가 baseline-robust
   하다)을 deterministic 하게 ruled-out 하는 closed-negative. H_655 의 "rule184 最高" 가 trivial-baseline
   artifact 였음을 확정하고, non-zero baseline 에서는 magnitude-top 이 convexity-top(H_653 rule110)과
   수렴함을 보여, 메타-축의 내부 일관성을 baseline 교정 후 회복. round 9 메타-축의 magnitude 차원
   해석을 정직하게 정밀화하는 결과.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F658.1 RANK-ROBUST-IND | argmax Δ_b = rule184 | argmax Δ_b = rule110 (41.71 > 41.54) | **FAIL** |
| F658.2 RANK-ROBUST-MID | argmax Δ_c = rule184 | argmax Δ_c = rule110 (35.17 > 22.93) | **FAIL** |
| F658.3 BASE-NONZERO | 5·Φ_part2 > 0 ∀ rule | rule90·rule110 Φ_part2=0 (2/4 zero) | **FAIL** |
| F658.4 NO-FLIP-TO-IV | rule110 NOT argmax (b)·(c) | rule110 IS argmax 양측 (named flip 발생) | **FAIL** |
| F658.5 W0-REPRO | argmax Δ_a=rule184 & Σ(W=0)=0 | rule184 (51.54) & Σ=0.0 4/4 (H_655 재현) | **PASS** |
| F658.6 BOUND | Φ ≥ 0, Δ_x finite | 全 충족 | **PASS** |

**aggregate: 2 PASS / 4 FAIL** — CORE F658.1 FAIL → FALSIFY 조건 충족 → 🔴 FALSIFIED.
non-zero parts-baseline 에서 argmax-Δ 가 rule184(II)→rule110(IV)로 flip → H_655 의 Δ-class 순위는
trivial-baseline artifact, super-additivity magnitude 의 class 의존은 baseline-conditional.
H_635 의 super-additivity *방향*(Δ>0)은 全 baseline 보존되나, *최고 rule* 의 정체는 baseline 종속.

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h658_collective_superadditivity_nonzero_baseline_2026_05_28/run_h658.hexa`
  (hexa-native, deterministic; H_635/H_653/H_655 engine 재사용, 3-baseline Δ 비교로 확장)
- log: `UNIVERSE/state/h658_collective_superadditivity_nonzero_baseline_2026_05_28/run.log` (full stdout verbatim)
- result: `UNIVERSE/state/h658_collective_superadditivity_nonzero_baseline_2026_05_28/result.json` (machine-readable)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` · `iit4_tpm.hexa`
  (hexa-lang stdlib SSOT, H_635/H_653/H_655 와 동일)
- replay (selfhosted, fix-1180 우회, mac-local, $0): `HEXA_MAC_BUILD_OK=1
  HEXA_LANG=<hexa-lang-root> hexa.real.bak-2026-05-22-pre-no-hxc build run_h658.hexa -o /tmp/h658.bin
  && codesign -s - --force /tmp/h658.bin && /tmp/h658.bin` — wall ~41s ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]]

---

## 10. Next-list / Backlog

- **N1** `collective-superadditivity-part-order-sweep` — 독립 part 를 n∈{2,3} substrate 로 sweep —
  n=2 minimal 의 비균질 Φ_part2(rule90·rule110=0)가 n=3 에서 non-zero 가 되어 flip 강도가 바뀌는지
  (C3.2·C3.3). part 차수가 baseline 의 rule-균질성을 결정하는 closed-form 경계.
- **N2** `collective-superadditivity-heterogeneous-baseline` — mix-class cohort([110,30,90,184,110])의
  non-zero baseline Δ 순위 (C3.4, H_655 N2 상속).
- **N3** `collective-superadditivity-cap-baseline-robustness` — cap∈{2,3,4}에서 non-zero baseline
  flip(rule184→rule110)의 robustness — cap↑ 가 flip 을 보존/역전하는지 (C3.6, shard-parallel).
- **N4** `magnitude-convexity-baseline-convergence` — 본 H 가 발견한 "non-zero baseline 에서
  magnitude-top 이 convexity-top(rule110)과 수렴" 을 정량 — 어떤 baseline 정의에서 magnitude↔convexity
  순위가 일치하는지의 closed-form 경계 (메타-축 내부 일관성 정밀화, H_655 N4 상속·정밀화).
- **N5** `collective-superadditivity-state-marginal-baseline` — sys_state=0 anchor → 2^5 state
  가중평균 Δ 의 baseline-robustness (C3.5, H_655 N5 상속).

---

## 양방향 sibling

- 직계 predecessor (N1 회수): [H_655_collective_superadditivity_substrate_class.md](H_655_collective_superadditivity_substrate_class.md) (축 G, 🔴, trivial-baseline Δ⊥class)
- sister 메타-축 (flip 수렴): [H_653_collective_convexity_substrate_class.md](H_653_collective_convexity_substrate_class.md) (축 G×F, 🟢, convexity monotone, top=rule110)
- super-additivity 부모: [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md) (축 F, 🟢, super-additive 5/5, Σ-baseline=0)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link
