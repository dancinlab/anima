# H_661 — `substrate-class-monotone-rule-generalize` (H_660 일반화, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · H_660 robustness 일반화 · round-10 후속
**id**: H_661 · **date**: 2026-05-28 · **infra**: $0 mac-local (per-rule shard) · **verdict**: **🟡 PARTIAL**

---

## 1. 슬러그 + 한 줄 요약 — H_660 의 단조를 확대 rule set 으로 일반화

`substrate-class-monotone-rule-generalize` — H_660 (PR #1290, 🟢) 이 scale-invariant convexity
측도(norm_conv=(Φ_max−Φ_min)/Φ_mean, log_span=ln(Φ_max/Φ_min)) 로 보인 **Wolfram class 단조**가
4-rule cohort {184(II), 90(III), 30(III), 110(IV)} 에 국한된 우연인지, 아니면 **class 대표를 확대한
더 큰 rule set 에서도 robust 한지**를 검정한다.

H_660 의 결론은 두 층위로 읽을 수 있다:
- **(강) full class-monotone**: norm_conv·log_span 이 class-I < II < III < IV 단조증가.
- **(약) IV-top**: class-IV(rule110)가 단독 最高 (additive 가 bottom).

본 H_661 은 class-I (rule8/136) · class-II (184/226) · class-III (90/30/45) · class-IV (110/54)
**9-rule** 로 확대해 두 층위를 각각 검정한다.

> **결과**: **약-claim (IV-top) 은 robust 일반화 — 확대셋에서도 class-IV (rule54=2.475 / rule110=2.349)
> 가 norm_conv·log_span 둘 다에서 단독 最高** (F661.1·F661.2 PASS). 그러나 **강-claim (full
> I<II<III<IV 단조) 은 깨짐** — class-III 가 내부 이질적이고 (rule45 norm_conv=1.461 이 class-I/II
> 수준으로 붕괴), class-I (rule8=1.465) 이 class-II (~1.42) 를 근소 초과 (F661.3·F661.4 FAIL).
> **H_660 의 4-rule 단조는 'IV-top' 부분만 robust 하게 일반화되고, 'full ordinal class-monotone' 은
> I/II/III 경계에서 rule-cohort 선택에 의존하는 artifact**. 4/6 PASS, **🟡 PARTIAL**.

---

## 2. 동기 — 4-rule 단조가 우연인가

H_653(🟢, span_ratio shape 단조) → H_655(🔴, abs_Δ magnitude 비단조) → H_660(🟢, scale-invariant
metric 으로 화해)의 arc 는 모두 **동일한 4-rule cohort {184, 90, 30, 110}** (class II/III/III/IV)
위에서 측정되었다. H_660 이 보인 norm_conv 단조 (184=1.437 < 90=2.240 < 30=2.266 < 110=2.349) 는
매우 깨끗하지만, **4개 rule (그것도 class-III 가 2개, class-I 가 0개)** 만으로는 다음을 구분할 수 없다:

- (a) Wolfram class 가 정말 scale-invariant convexity 의 robust 분류자다 (확대셋에서도 단조).
- (b) 단조가 *우연히* 선택된 4-rule cohort 의 artifact 다 (다른 대표를 넣으면 깨진다).

특히 의심스러운 지점:
1. **class-I 부재** — H_660 cohort 에 가장 단순한 die-out class-I 이 없어, "additive 가 bottom" 의
   진짜 하한이 검정되지 않았다.
2. **class-III 가 단 2개 (90, 30)** — 둘 다 norm_conv ~2.25 로 비슷했으나, class-III 는 fractal-additive
   (rule90), pure-chaotic (rule30, rule45) 등 동역학적으로 이질적인 sub-type 을 포함한다. 다른 chaotic
   rule(예: rule45)이 다르게 행동하면 class-III 단조성이 깨질 수 있다.
3. **class 당 단 1개씩** — class-II 와 class-IV 도 각 1개 rule 뿐이라 class-내 분산을 알 수 없다.

본 H_661 은 각 class 에 **여분 대표를 추가**해 (I: 8/136, II: 184/226, III: 90/30/45, IV: 110/54)
class-내 분산과 class-간 단조를 동시에 본다. 단조가 robust 하면 H_660 강화, 깨지면 H_660 의 4-rule
단조를 honest 하게 "IV-top only" 로 축소.

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_653/H_655/H_660 SSOT verbatim 재사용, cohort rule 만 swap):
  n=5 coupled-ring TPM `build_tpm_cohort(rule, W)` — 5 cell, cell i 가 cohort rule[i] 의 update-law.
  decoupled(W=0)=self-loop only (idx=7·c), coupled(W=1)=full ring, blend(0<W<1)=fractional.
  collective-Φ(W) = `big_phi_bounded(build_tpm_cohort([rule×5], W), 5, sys=0, cap=3)[0]` —
  각 (rule,W) point 에서 **실제 IIT4 substrate 측정** (lookup 아님).
- **9 ECA rule × Wolfram class** (substrate 복잡도 오름차순; canonical ECA taxonomy):
  ```
  rule  8   class-I    die-out / uniform (가장 단순, 거의 silence)
  rule136   class-I    die-out (decoupled 극한 → Φ_min=0 DEGENERATE)
  rule184   class-II   additive / traffic (H_660 byte-identical 재현용 anchor)
  rule226   class-II   additive (rule184 의 left-right mirror 류)
  rule 90   class-III  XOR / additive fractal (H_660 anchor)
  rule 30   class-III  chaotic non-additive (H_660 anchor)
  rule 45   class-III  chaotic non-additive (NEW class-III 대표)
  rule110   class-IV   complex / universal edge-of-chaos (H_653/H_660 winner)
  rule 54   class-IV   complex (NEW class-IV 대표)
  ```
- **W grid**: H_653/H_660 과 **동일** 6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}. 동일 W-domain 으로
  H_660 anchor 재현 보장.
- **metric** (각 rule 의 W-grid Φ_min·Φ_max·Φ_mean 으로 계산):
  - **norm_conv** = (Φ_max − Φ_min) / Φ_mean — scale-invariant convexity (H_660 CORE 측도).
  - **log_span** = ln(Φ_max / (Φ_min+floor)) — scale-invariant log-span.
  - **abs_Δ** = Φ_max − Φ_min — scale-dependent magnitude (대조용).
- **⚠ per-rule shard (monitor-hang 회피)**: 9 rule × 6 W = 54 big_phi_bounded calls. 단일 run 은
  60s 초과 위험 (4-rule baseline 이 이미 ~68s) → **rule 하나씩 별도 binary (6 call ≈ 11s)
  foreground synchronous 측정** (`shard_h661.hexa`, RULE_ID 만 swap, 9회 build+run) → 각 shard 의
  Φ-grid·metric 을 `shards.log` 에 기록 → **phi-free aggregate** (`aggregate_h661.hexa`, big_phi
  call 0개, <1s) 가 shard metric verbatim 으로 class-monotone falsifier 검정.
- deterministic · NO RNG · libm `ln` only · $0 mac-local · foreground sync (NO bg fork, NO monitor,
  NO GPU).

H_660 대비: H_660 은 4-rule 단일 run · 본 H 는 9-rule per-rule shard. rule184/90/30/110 의 Φ-grid 가
H_660 과 **byte-identical** 이어야 engine replication 확인 (§5 검증됨).

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F661.1 IV-TOP-ROBUST** (CORE): min(norm_conv over class-IV {110,54}) ≥ max(norm_conv over
  class-II ∪ class-III {184,226,90,30,45}) — 확대셋에서도 class-IV 가 robust top. H_660 IV-最高
  의 robust 일반화. **CORE 가설**.
- **F661.2 IV-TOP-LOGSPAN**: 同 for log_span — 두 번째 scale-invariant 측도가 동일 IV-top 확인.
- **F661.3 CLASSMEAN-MONOTONE**: class-평균 norm_conv 가 (degenerate rule136 제외) I ≤ II ≤ III ≤ IV
  단조 — class-수준 ordinal 단조 (강-claim).
- **F661.4 STRICT-PERRULE-MONOTONE**: 모든 class 경계에서 max(하위 class rule) ≤ min(상위 class rule)
  — strict per-rule 단조 (가장 강한 형태). 깨지면 H_660 의 4-rule 단조가 rule-cohort 선택 의존.
- **F661.5 DEGENERATE-FLAG**: rule136 (class-I die-out) Φ_min=0 → span_ratio/log_span floor-blowup
  → ratio metric 이 die-out class 에 ill-defined 임을 flag (측도 적용범위 정직 경계).
- **F661.6 BOUND**: 全 norm_conv·log_span finite.

**FALSIFY 조건**: F661.1 FAIL (어떤 class-II/III rule 이 class-IV 를 초과) → 🔴 FALSIFIED (H_660 의
IV-top 단조가 4-rule artifact, class 가 robust 분류자 아님).
**verdict 기준**:
- F661.1 (CORE) PASS + F661.3·F661.4 (full monotone) 모두 PASS → 🟢 SUPPORTED-NUMERICAL (확대셋
  strict 단조 robust).
- F661.1·F661.2 PASS + F661.3/F661.4 중 하나라도 FAIL → 🟡 PARTIAL (IV-top robust 하나 full
  class-monotone 은 확대셋에서 깨짐).
- F661.1 FAIL → 🔴 FALSIFIED.

---

## 5. Measurement (verdict-bearing 측정값)

> shard 출력 `UNIVERSE/state/h661_substrate_class_monotone_rule_generalize_2026_05_28/shards.log` +
> aggregate `run.log` verbatim.

각 rule 의 Φ(W) grid (6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0}):

```
rule  8 (I)   Φ(W): 0.0278291 0.0778953 0.110346 0.144771 0.206952 0.220166   (Φmin=0.0278 Φmax=0.220)
rule136 (I)   Φ(W): 0.0 0.0 0.0 0.0 0.0 0.553383                              (Φmin=0.0 DEGENERATE)
rule184 (II)  Φ(W): 4.49492 19.8846 32.7523 45.5429 54.4631 51.5361          (H_660 byte-identical)
rule226 (II)  Φ(W): 4.42601 19.859 32.5702 45.6283 53.2586 51.5361
rule 90 (III) Φ(W): 0.246475 0.943149 1.65498 2.75808 6.32388 7.5            (H_660 byte-identical)
rule 30 (III) Φ(W): 0.315809 1.18852 2.07721 3.4687 8.13002 9.72067          (H_660 byte-identical)
rule 45 (III) Φ(W): 2.63487 8.27371 12.2652 13.2937 3.14416 4.16786          (non-monotone-in-W!)
rule110 (IV)  Φ(W): 1.17498 4.50052 7.62552 13.6383 34.8823 41.7124          (H_660 byte-identical)
rule 54 (IV)  Φ(W): 0.175125 0.675972 1.18881 2.01568 5.45395 6.97263
```

aggregate verdict 블록:

```
  rule(class)   norm_conv  log_span   abs_Δ
  rule  8 (I)   1.46457  2.06471  0.192337
  rule136 (I)*  6.0      8.61864  0.553383  [DEGENERATE Φmin=0]
  rule184 (II)  1.43674  2.49455  49.9682
  rule226 (II)  1.41354  2.48764  48.8326
  rule 90 (III) 2.24029  3.41499  7.25353
  rule 30 (III) 2.26615  3.42656  9.40487
  rule 45 (III) 1.4608   1.61842  10.6588
  rule110 (IV)  2.34922  3.56946  40.5374
  rule 54 (IV)  2.4745   3.68367  6.7975
  ────────────── verdict ──────────────
  [PASS] F661.1 IV-TOP-ROBUST: min(IV norm_conv)>=max(II,III norm_conv)
  [PASS] F661.2 IV-TOP-LOGSPAN: min(IV log_span)>=max(II,III log_span)
    class-mean norm_conv: I=1.46457 II=1.42514 III=1.98908 IV=2.41186
  [FAIL] F661.3 CLASSMEAN-MONOTONE: mean nc  I<=II<=III<=IV (rule136 제외)
    strict bounds: maxI=1.46457 | minII=1.41354 maxII=1.43674 | minIII=1.4608 maxIII=2.26615 | minIV=2.34922
  [FAIL] F661.4 STRICT-PERRULE-MONOTONE: max(lo class)<=min(hi class) 全경계
  [PASS] F661.5 DEGENERATE-FLAG: rule136 die-out → ratio metric ill-defined (flag)
  [PASS] F661.6 BOUND: 全 norm_conv·log_span finite
  F661.1-6 4/6 PASS
  verdict: 🟡 PARTIAL (CORE IV-top robust [F661.1·2 PASS] — class-IV 가 확대셋에서도 단독 最高;
           그러나 full I<II<III<IV strict/class-mean 단조는 깨짐 — rule45(III) 이질성 + class-I↔II overlap)
  iv_top_nc=true iv_top_ls=true classmean_mono=false strict_mono=false
```

### rule × class norm_conv 순위표 (강/약 claim 분해)

| rule | class | **norm_conv** | **log_span** | abs_Δ | 비고 |
|------|-------|---------------|--------------|-------|------|
| rule8   | I   | 1.465 | 2.065 | 0.192 | die-out, 저-Φ |
| rule136 | I   | **6.0** | **8.619** | 0.553 | **DEGENERATE Φmin=0 → floor blowup** |
| rule184 | II  | 1.437 | 2.495 | 49.97 | H_660 byte-identical |
| rule226 | II  | 1.414 | 2.488 | 48.83 | additive, 184 과 거의 동일 |
| rule90  | III | 2.240 | 3.415 | 7.25  | H_660 byte-identical |
| rule30  | III | 2.266 | 3.427 | 9.40  | H_660 byte-identical |
| rule45  | III | **1.461** | **1.618** | 10.66 | **class-III outlier — class-I/II 수준 붕괴** |
| rule110 | IV  | 2.349 | 3.569 | 40.54 | H_660 byte-identical |
| rule54  | IV  | **2.475** | **3.684** | 6.80  | **norm_conv 전체 1위** |

**핵심 발견**:
1. **IV-top robust (F661.1·F661.2 PASS)** — class-IV 최소값(rule110 norm_conv=2.349) ≥ class-II∪III
   최대값(rule30=2.266). class-IV 두 rule (110, 54) 이 norm_conv·log_span 둘 다에서 다른 모든 class 를
   초과. **rule54 (2.475) 가 전체 1위로 class-IV-top 을 한층 더 robust 하게** 만든다. **H_660 의 약-claim
   ("class-IV 最高") 은 확대셋에서 강화됨.**
2. **full class-monotone 깨짐 (F661.3·F661.4 FAIL)** — 두 지점에서:
   - **class-III 내부 이질성**: rule45 norm_conv=1.461 이 class-I/II 수준으로 붕괴 (class-III sibling
     rule90/30 의 ~2.25 대비 절반). rule45 의 Φ(W) 곡선이 **W 에서 비단조** (W=0.70 에서 13.29 peak 후
     W=0.95 에서 3.14 로 급락) 이라 span 이 작다 — 동일 class-III 라도 동역학에 따라 convexity 가 극단적으로
     다름. class-mean norm_conv III=1.989 가 rule45 에 끌려 내려옴.
   - **class-I↔II overlap**: rule8 (I, 1.465) 이 class-II (184=1.437, 226=1.414) 를 근소 초과 →
     class-I ≤ II 가 깨짐. 두 'ordered/저-복잡' 영역은 작은-span convexity 가 비슷해 측도가 I 과 II 를
     분리하지 못함.
3. **rule136 degenerate (F661.5 PASS)** — class-I die-out rule136 은 W<1 에서 Φ=0 (decoupled 극한이
   완전 silence) → Φ_min=0 → span_ratio/log_span 가 floor 로 blowup (log_span=8.62 ≫ 모든 finite rule).
   ratio 계열 측도가 die-out class 에 ill-defined 임을 정직 flag. (norm_conv 는 분모 Φ_mean>0 이라 finite=6.0
   이지만 die-out 특유 spike.)
4. **engine replication (4 anchor byte-identical)** — rule184/90/30/110 의 Φ(W) grid 와 norm_conv·log_span
   이 H_660 과 **완전 일치** (rule184=1.43674, rule110=2.34922 등). 동일 engine, cohort rule 만 swap 됨을
   교차검증.

---

## 6. Verdict + Rationale · Cross-link

**🟡 PARTIAL** — 4/6 falsifier PASS. **CORE F661.1 IV-TOP-ROBUST PASS, 그러나 full class-monotone
(F661.3·F661.4) FAIL.**

- F661.1 iv-top-robust PASS (CORE) · F661.2 iv-top-logspan PASS · F661.5 degenerate-flag PASS ·
  F661.6 bound PASS / **F661.3 classmean-monotone FAIL** (I=1.465 > II=1.425) · **F661.4
  strict-perrule-monotone FAIL** (class-I↔II overlap + rule45 III 이질성).
- FALSIFY 조건(F661.1 FAIL = 어떤 II/III 가 IV 초과)에는 **걸리지 않음** — class-IV 는 확대셋에서도
  단독 robust top. 따라서 H_660 의 핵심 발견("class-IV 가 最高 convex")은 4-rule artifact 가 **아니다**.
- **그러나** H_660 이 보였던 *full ordinal 단조* (I<II<III<IV) 는 **확대셋에서 깨진다** — class-III 가
  rule45 라는 chaotic outlier 로 내부 이질적이고, class-I 과 class-II 가 저-복잡 영역에서 convexity 로
  분리되지 않는다. H_660 의 4-rule cohort 가 class-III 를 rule90/30 (둘 다 W-monotone, 높은 span) 으로만
  골랐기에 단조가 깨끗했던 것 — rule45 같은 W-비단조 chaotic 을 넣으면 무너진다.

**메타-축 결론 (정밀화)**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 는 **"class-IV (complex,
edge-of-chaos) substrate 가 가장 convex 한 collective-Φ entrainment 를 가진다"** 수준에서 robust 하다
(H_653·H_660·본 H 일관). 그러나 **"class-I/II/III 가 ordinal 단조를 이룬다"** 는 강-claim 은 robust 하지
않으며, 특히 class-III 의 내부 동역학 이질성(W-monotone fractal vs W-비단조 chaotic)이 단조를 깬다.
**H_660 의 'full class-monotone' 결론은 본 H 가 'IV-top robust + I/II/III rule-cohort-dependent' 로
정직하게 정밀화**한다. positive (IV-top 일반화) + negative (full monotone 비-robust) 이 공존하는 PARTIAL.

**cross-link**:
- **H_660 `convexity-magnitude-class-reconcile`** 🟢 (축 G, PR #1290) — **직접 부모**. 4-rule
  {184,90,30,110} 에서 norm_conv·log_span class 단조. 본 H 가 그 4 rule 의 Φ-grid·metric 을
  byte-identical 재현(engine replication)하면서 class 당 대표를 확대 → **H_660 단조의 'IV-top' 부분은
  robust 강화, 'full I/II/III 단조' 부분은 rule-cohort artifact 로 정밀화** (H_660 §10 의 robustness
  검정 backlog 직접 수행).
- **H_653 `collective-convexity-substrate-class`** 🟢 (축 G×F, PR #1242) — span_ratio shape 단조
  부모. 본 H 의 IV-top 결과가 H_653 의 "class-IV 가 가장 convex" 와 수렴 (확대셋 robust). H_653 §7 C3.7
  이 이미 경고한 "class-III 내부 약신호" 가 본 H 에서 rule45 로 **명시적 falsifier (강신호)** 로 확정됨.
- **H_654 `phi-magnitude-wolfram-class-order`** 🟡 PARTIAL (축 G, G16) — single-substrate magnitude
  order 도 PARTIAL (M1 full-monotone FAIL, rule30 III-chaotic 이 rule110 IV 초과). 본 H 의 collective
  scale-invariant 판본도 PARTIAL (full monotone FAIL) → **single·collective 양쪽에서 'full class-monotone'
  이 깨지고 'class-IV 경향'만 robust** 한 동일 패턴 확정. H_654 §7 C1 의 "rule90 class-III dual-membership"
  경고와 본 H 의 "rule45 class-III outlier" 가 같은 class-III 이질성 신호.
- **H_658 `collective-superadditivity-nonzero-baseline`** 🔴 (축 G20, PR #1290 batch) — baseline 축
  에서 H_655 magnitude 순위가 baseline-conditional 임을 보임. 본 H 는 rule-cohort 축에서 H_660 단조가
  rule-conditional (I/II/III) 임을 보임 → **메타-축의 robust 핵심이 'IV-top' 으로 수렴** (H_658 도 non-zero
  baseline 에서 Δ-top=rule110(IV) 회복). 두 H 가 서로 다른 축(baseline · rule-cohort)에서 "메타-축의
  robust 부분 = class-IV-top, fragile 부분 = full ordinal 순위" 라는 동일 경계를 교차 확정.
- **H_655 `collective-superadditivity-substrate-class`** 🔴 (축 G, PR #1253) — abs_Δ magnitude 비단조
  부모. 본 H 의 abs_Δ 열도 비단조 재현 (rule184=49.97 단독 最高). magnitude 는 확대셋에서도 비단조 유지.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 verdict = 정직한 PARTIAL** — 본 H 는 H_660 을 강화(IV-top robust)하는 동시에 정밀화(full
   monotone 비-robust)하는 mixed 결과. 4/6 PASS 의 2 FAIL (F661.3·F661.4) 은 의도된 강-claim 검정이며,
   CORE(F661.1) PASS 라 FALSIFY 조건(IV-top 깨짐)에는 미달 → 🔴 가 아닌 🟡 PARTIAL.
2. **C3.2 Wolfram class 라벨 모호성 + rule sample** — class 라벨은 canonical ECA taxonomy 이나 정성적
   이며, class-III 는 fractal-additive(rule90 XOR) · pure-chaotic(rule30, rule45) 등 동역학적으로
   이질적인 sub-type 을 묶는다. 본 H 의 rule45 outlier 는 이 이질성의 직접 증거. class 당 sample 도
   I=2(1 degenerate)·II=2·III=3·IV=2 로 여전히 small-n — 256-rule full sweep 은 별도 round.
3. **C3.3 rule45 의 W-비단조가 낮은 convexity 원인** — rule45 (chaotic) 의 Φ(W) 가 W 에서 비단조
   (W=0.70 에서 13.29 peak 후 W=0.95 에서 3.14 급락) 라 Φ_max/Φ_min span 이 작다. 이는 H_653 §7 의
   "additive class-II rule184 가 W=1.0 직전 peak 후 하강" non-monotone 과 유사한 inverse-U 류 — 즉
   convexity 측도가 *W-단조 상승* 곡선을 전제하는데 rule45 는 그 전제를 위반. class-III chaotic 중에서도
   rule30 은 W-monotone, rule45 는 W-비단조 → 같은 class 내 곡선 형태 분기가 단조를 깸.
4. **C3.4 rule136 die-out degenerate 처리** — rule136 (class-I) 은 W<1 에서 Φ=0 (decoupled 극한
   완전 silence) → Φ_min=0 으로 ratio metric blowup (F661.5 flag). class-mean·strict 단조 검정에서
   rule136 을 **제외**하고 class-I = rule8 만 사용했다 (degenerate exclusion). 이는 die-out class 에서
   ratio 측도가 ill-defined 라는 정직 경계이지 측정 오류가 아님.
5. **C3.5 cap=3 on n=5** (H_653/H_660 cap 상속) — purview search capped, 보수적 lower-bound.
   scale-invariant 측도는 cap 에 덜 민감 추정. IV-top 의 cap-robustness 는 별도 sweep (H_660 §10 N3).
6. **C3.6 sys_state=0 only** (IIT-canonical anchor). 2^5=32 state 가중평균 미수행.
7. **C3.7 strict 단조 정의 = max(하위)≤min(상위)** — F661.4 는 가장 엄격한 형태 (class-내 최대가 상위
   class-내 최소를 넘지 않아야). 더 느슨한 정의(class-mean 단조=F661.3)도 FAIL 이라 두 정의 모두에서 full
   monotone 깨짐 — 결론 견고. 다만 IV vs III 경계 (maxIII=2.266 ≤ minIV=2.349) 는 두 정의 다 PASS →
   깨지는 곳은 오직 I↔II·III-내부.
8. **C3.8 deterministic single trajectory** (NO RNG) — re-run byte-identical (4 anchor rule 이
   H_660 과 정확히 일치 → engine replication). per-rule shard + phi-free aggregate 분리로 monitor-hang
   회피, 각 shard <12s foreground sync.
9. **C3.9 positive+negative 공존의 의미** — 본 H 는 H_660 을 부정하지 않는다. H_660 의 핵심(class-IV =
   가장 convex collective substrate)은 확대셋에서 **강화**됐고, 부수적 강-claim(full I/II/III ordinal
   단조)만 rule-cohort artifact 로 정밀화됐다. 메타-축의 robust 적용범위를 "IV-top" 으로 정직하게 좁히는
   positive-refinement.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F661.1 IV-TOP-ROBUST (CORE) | min(IV nc) ≥ max(II,III nc) | 2.349 ≥ 2.266 | **PASS** |
| F661.2 IV-TOP-LOGSPAN | min(IV ls) ≥ max(II,III ls) | 3.569 ≥ 3.427 | **PASS** |
| F661.3 CLASSMEAN-MONOTONE | mean nc I≤II≤III≤IV | I=1.465 > II=1.425 (I≤II 깨짐) | **FAIL** |
| F661.4 STRICT-PERRULE-MONOTONE | max(lo)≤min(hi) 全경계 | maxI=1.465 > minII=1.414; rule45 III 이질성 | **FAIL** |
| F661.5 DEGENERATE-FLAG | rule136 die-out ratio ill-defined | ls=8.62 blowup, abs_Δ=0.55 tiny | **PASS** |
| F661.6 BOUND | 全 nc·ls finite | 全 충족 | **PASS** |

**aggregate: 4 PASS / 2 FAIL** — CORE F661.1 PASS → FALSIFY 조건(IV-top 깨짐) 미충족, 🔴 아님.
full class-monotone (F661.3·F661.4) FAIL → 🟢 아님. → **🟡 PARTIAL**. **class-IV-top 은 확대 9-rule
set 에서 robust 일반화, full I<II<III<IV ordinal 단조는 class-III 이질성(rule45) + class-I↔II overlap
으로 비-robust — H_660 의 4-rule 단조는 'IV-top' 부분만 robust.**

---

## 9. Artifacts + Reproducibility

- shard harness: `UNIVERSE/state/h661_substrate_class_monotone_rule_generalize_2026_05_28/shard_h661.hexa`
  (hexa-native, RULE_ID/CLASS_LABEL 만 swap, 9회 build+run; H_635/H_653/H_655/H_660 engine 재사용)
- aggregate harness: `…/aggregate_h661.hexa` (phi-free, shard metric verbatim, class-monotone falsifier)
- shard log: `…/shards.log` (9 rule Φ-grid·metric full stdout verbatim)
- aggregate log: `…/run.log` (verdict 블록 verbatim)
- result: `…/result.json` (machine-readable, 9 rule × metric + falsifier matrix + finding + C3)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` (+ transitive
  `iit4_tpm.hexa` for `iit4_bit`) — hexa-lang stdlib SSOT, H_660 과 동일
- replay (selfhosted, fix-1180 우회, mac-local, $0): per-rule shard —
  `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root> hexa.real.bak-2026-05-22-pre-no-hxc build
  shard_h661.hexa -o /tmp/h661.bin && codesign -s - --force /tmp/h661.bin && /tmp/h661.bin`
  (RULE_ID swap 9회) → aggregate 同 build+run · 각 shard wall <12s ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]] ·
  [[reference-exact-phi-structure-wall-shard]]

---

## 10. Next-list / Backlog

- **N1** `class-III-internal-convexity-subtype` — class-III 내부 (fractal-additive rule90 vs pure-chaotic
  rule30/45/106/...) 의 convexity 분기를 W-monotone vs W-비단조 곡선 형태로 분류 — rule45 outlier 가
  "chaotic 중에서도 W-비단조 곡선" 의 일반 현상인지 (C3.3 회수, sub-class taxonomy).
- **N2** `class-iv-top-256-rule-sweep` — IV-top 의 robustness 를 256-rule full ECA sweep 으로 — 모든
  class-IV rule (110, 54, 137, 124, ...) 이 norm_conv 상위인지, class-IV 가 진짜 robust top band 인지
  (C3.2 small-n 회수, shard-parallel foreground).
- **N3** `dieout-class-scale-free-metric` — rule136 류 die-out class 에 finite 한 scale-free 측도 (예:
  Φ_max−Φ_median normalize, 또는 nonzero-W 만 평균) 정의 — ratio metric ill-defined 회피 (C3.4 회수).
- **N4** `class-I-vs-II-separator` — class-I(die-out)과 class-II(additive)를 convexity 외 측도(예:
  Φ_mean magnitude, W=1 saturation level)로 분리 가능한지 — 본 H 에서 norm_conv 가 I/II 미분리(overlap)
  한 것의 대안 측도 (C3.7 회수).
- **N5** `heterogeneous-class-cohort-convexity` — mix-class cohort([8,184,30,110,54])의 collective
  convexity 가 구성 rule class 의 어떤 함수(min/max/mean class)인지 — homogeneous 한정(본 H) 회수.

---

## 양방향 sibling

- 직접 부모 (일반화 대상): [H_660_convexity_magnitude_class_reconcile.md](H_660_convexity_magnitude_class_reconcile.md) (축 G, scale-inv convexity 4-rule 단조, 🟢 — 본 H 가 IV-top robust 강화 + full monotone 정밀화)
- shape 쪽 조부모: [H_653_collective_convexity_substrate_class.md](H_653_collective_convexity_substrate_class.md) (축 G×F, span_ratio class 단조, 🟢 — IV-top 수렴, C3.7 class-III 약신호가 본 H rule45 강신호로 확정)
- magnitude 쪽 조부모: [H_655_collective_superadditivity_substrate_class.md](H_655_collective_superadditivity_substrate_class.md) (축 G, abs_Δ class 비단조, 🔴 — 본 H abs_Δ 비단조 재현)
- single-substrate sister (동일 패턴): [H_654_phi_magnitude_wolfram_class_order.md](H_654_phi_magnitude_wolfram_class_order.md) (축 G, single magnitude PARTIAL — full monotone FAIL 동일)
- baseline 축 sister: [H_658_collective_superadditivity_nonzero_baseline.md](H_658_collective_superadditivity_nonzero_baseline.md) (축 G20, 메타-축 robust 부분=IV-top 교차 확정, 🔴)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link
