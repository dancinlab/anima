# H_653 — `collective-convexity-substrate-class` (H_643 정밀화, 축 G×F)

**축**: G (ULTRADIAN / 시간동조) × F (HIVE-MIND / collective Φ) cross-link — H_643 정밀화
**id**: H_653 · **date**: 2026-05-28 · **infra**: $0 mac-local · **verdict**: **🟢 SUPPORTED-NUMERICAL**

---

## 1. 슬러그 + 한 줄 요약

`collective-convexity-substrate-class` — H_643 (PR #1237, 🟢 6/6) 이 collective-Φ 의 ultradian
동조가 단일 substrate(H_634 r=0.802)보다 약함(r=0.568)을 보이며 그 원인을 H_635 의 W→Φ
super-linear/convex curve(~30× span)가 pure cosine 에서 더 벗어나기 때문이라 진단했다. 본 H 는
그 **convexity 가 substrate 복잡도(ECA rule class)에 어떻게 의존하는지** 정량한다. cohort rule 을
{184, 90, 30, 110} 로 바꿔(Wolfram class II→III→III→IV) W∈{0.15..1.0} sweep → 각 rule 의
span ratio Φ_max/Φ_min = convexity 측정, rule class 단조성 검정.

> **결과**: convexity span ratio 가 rule class 에 **단조 의존** — rule184(II)=**12.12** <
> rule90(III)=**30.42** < rule30(III)=**30.77** < rule110(IV)=**35.50**. class-IV(rule110)
> 가 단독 最高 convex, class-II(additive)가 가장 linear. **5/6 PASS** (F653.1 core monotone-in-class
> PASS). rule110 컬럼이 H_643 per-stage 값(N3=1.17·N2=4.50·N1=13.64·REM=34.88)과 정확히 일치 →
> engine replication 검증. **H_643 의 ~30× span 은 cohort artifact 가 아니라 substrate-class 속성**.
> H1 SUPPORTED.

---

## 2. 동기

H_643 (PR #1237, 🟢) 는 5-stream collective-Φ 가 90-min ultradian phase 에 동조(r=0.568)하나
단일 substrate(H_634 r=0.802)보다 **약하게** 동조함을 보였다. H_643 §5 의 진단: H_635 의 W→Φ_collective
곡선이 super-linear/convex(N3 1.17 → REM 34.88 = ~30× span)라서 순수 cosine 에서 더 벗어나
r 이 낮아진다 — 반면 H_634 단일 substrate stage projection 은 near-linear(~7× span)라 cosine 에
잘 맞는다. H_643 cohort 는 C1 = [110×5] (rule110, class-IV) 1종뿐이었다.

본 H 는 이 진단의 핵심 미해결점을 정량한다: **그 convexity 는 rule110 cohort 의 우연한 특성인가
(cohort artifact), 아니면 substrate 복잡도(rule class)의 단조 함수인가?** 만약 후자라면 H_643 의
~30× span 은 class-IV 에서 가장 크고 단순 additive class 로 내려갈수록 작아져야 한다 — 즉 collective
entrainment 의 약화 정도 자체가 substrate 복잡도에 의해 결정된다는 더 강한 구조적 발견이 된다.

핵심 정합점: H_635 의 "collective-Φ 는 sync_factor W 에 단조증가"는 W→Φ curve 의 *방향* 발견이고,
본 H 는 그 curve 의 *곡률(convexity)* 이 substrate class 에 어떻게 의존하는지를 정밀화한다 —
H_643 이 진단만 하고 닫지 못한 "convexity 의 origin" 을 substrate-class 축에서 정량.

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_643 SSOT 재사용, cohort rule 만 swap): n=5 coupled-ring TPM
  `build_tpm_cohort(rule, W)` — 5 cell, cell i 는 cohort rule[i] 의 update-law. decoupled(W=0)=
  self-loop only (idx=7·c), coupled(W=1)=full ring. collective-Φ(W) =
  `big_phi_bounded(build_tpm_cohort([rule×5], W), 5, sys=0, cap=3)[0]` — 각 (rule,W) point 에서
  **실제 IIT4 substrate 측정** (lookup 아님).
- **4 ECA rule × Wolfram class** (substrate 복잡도 오름차순):
  ```
  rule184  class-II   additive/traffic (가장 ordered)
  rule 90  class-III  XOR/additive fractal (chaotic-additive)
  rule 30  class-III  chaotic non-additive
  rule110  class-IV   complex/universal edge-of-chaos (H_643 winner)
  ```
- **W grid**: H_643 ultradian-stage sync_factor set {0.15, 0.40, 0.70, 0.95, 1.0} + 0.55 mid-point
  = 6 points. H_643 이 ride 하는 동일 W-domain.
- **convexity(rule)** = span ratio Φ_max / (Φ_min + 0.0001 floor) over the W grid. Φ_min≈0 floor
  guard. 단조성 부호 추출용 proxy (정확한 곡률 적분 아님, C3.6).
- **measurement 규모**: 4 rule × 6 W = **24 big_phi_bounded calls** (H_643 36-call 예산 내) ·
  단일 run <60s · libm `cos/sqrt` only · NO RNG (deterministic) · $0 mac-local.

H_643 / H_618 anchor 대비:
- H_643 은 rule110 단일 cohort 의 ultradian 동조 — 본 H 는 그 convexity 의 substrate-class 의존을 정량.
- H_618 (collective gz inverse-U) 는 collective-Φ 의 비단조 구조 anchor — 본 H 의 rule184 W-non-monotone
  (F653.4 FAIL) 과 연결.

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F653.1 CONVEXITY-MONOTONE**: span_ratio(rule110) ≥ span_ratio(rule30) ≥ span_ratio(rule90)
  ≥ span_ratio(rule184) — convexity 가 rule class 단조증가 (class-IV 最高 convex). **core 가설.**
- **F653.2 CLASS-IV-MOST-CONVEX**: span_ratio(rule110) = max over 4 rules (class-IV 단독 最高).
- **F653.3 ADDITIVE-MORE-LINEAR**: span_ratio(rule184) < span_ratio(rule110) (단순 additive class-II
  가 strictly 더 linear).
- **F653.4 W-MONOTONE-EACH-RULE**: 모든 rule 에서 collective-Φ 가 W 단조비감소 (H_635 monotone-in-W
  가 rule swap 후에도 보존).
- **F653.5 H643-REPLICATE**: span_ratio(rule110) ≥ 10 (H_643 ~30× span 이 substrate-class 속성으로
  재현).
- **F653.6 BOUND**: 全 collective-Φ ≥ 0, span ratio finite.

**FALSIFY 조건**: F653.1 FAIL (convexity ⊥ rule class) → 🔴 FALSIFIED (H_643 ~30× span 이 cohort artifact).
**verdict 기준**: ≥4/6 PASS → 🟢 SUPPORTED-NUMERICAL.

---

## 5. Measurement (verdict-bearing 측정값)

> harness 출력 `UNIVERSE/state/h653_collective_convexity_substrate_class_2026_05_28/run.log` verbatim.

```
================================================================
  H_653 — collective-convexity-substrate-class (H_643 정밀화)
  W→Φ_collective convexity (span ratio) vs ECA rule class?
  IIT4 big_phi_bounded · n=5 homog cohort · cap=3 · sys=0
  4 rules × 6-pt W grid · convexity = Φ_max / Φ_min
================================================================
  W grid: [0.15, 0.40, 0.55, 0.70, 0.95, 1.0]  (H_643 stage W + mid)
  ─────────────────────────────────────
  rule184 [II-additive]
    Φ(W): 4.49492 19.8846 32.7523 45.5429 54.4631 51.5361
    Φ_min=4.49492 Φ_max=54.4631 span_ratio=12.1163 W-monotone=NO
  rule90 [III-XOR/additive]
    Φ(W): 0.246475 0.943149 1.65498 2.75808 6.32388 7.5
    Φ_min=0.246475 Φ_max=7.5 span_ratio=30.4167 W-monotone=yes
  rule30 [III-chaotic]
    Φ(W): 0.315809 1.18852 2.07721 3.4687 8.13002 9.72067
    Φ_min=0.315809 Φ_max=9.72067 span_ratio=30.7705 W-monotone=yes
  rule110 [IV-complex]
    Φ(W): 1.17498 4.50052 7.62552 13.6383 34.8823 41.7124
    Φ_min=1.17498 Φ_max=41.7124 span_ratio=35.4975 W-monotone=yes
  ─────────────────────────────────────
  span ratios by class (ascending complexity):
    rule184 (II-additive)      : 12.1163
    rule90  (III-XOR/additive) : 30.4167
    rule30  (III-chaotic)      : 30.7705
    rule110 (IV-complex)       : 35.4975
  ────────────── verdict ──────────────
  [PASS] F653.1 CONVEXITY-MONOTONE: sr(110)>=sr(30)>=sr(90)>=sr(184)
  [PASS] F653.2 CLASS-IV-MOST-CONVEX: sr(110) = max over 4 rules
  [PASS] F653.3 ADDITIVE-MORE-LINEAR: sr(184) < sr(110)
  [FAIL] F653.4 W-MONOTONE-EACH-RULE: Φ_coll non-decreasing in W, all rules
  [PASS] F653.5 H643-REPLICATE: sr(rule110) >= 10 (H_643 ~30x span replicated)
  [PASS] F653.6 BOUND: Φ_coll ≥ 0, span ratios finite
  ──────────────────────────────────────
  F653.1-6 5/6 PASS
  verdict: 🟢 SUPPORTED-NUMERICAL
  cross-link: H_643 cohort=rule110 span≈30x → here rule110 span_ratio=35.4975
```

### rule-class별 span / convexity 표

| rule | Wolfram class | Φ_min | Φ_max | **span ratio (convexity)** | W-monotone |
|------|---------------|-------|-------|----------------------------|-----------|
| rule184 | II (additive) | 4.495 | 54.463 | **12.12** | **NO** (W=1.0 dip) |
| rule90  | III (XOR/additive) | 0.246 | 7.500 | **30.42** | yes |
| rule30  | III (chaotic) | 0.316 | 9.721 | **30.77** | yes |
| rule110 | IV (complex) | 1.175 | 41.712 | **35.50** | yes |

**핵심 발견**:
1. **convexity 가 rule class 에 단조 의존 (F653.1 PASS)** — span ratio 가 class II(12.12) < III-XOR(30.42)
   < III-chaotic(30.77) < IV(35.50) 으로 단조증가. class-IV(rule110)가 단독 最高 convex,
   class-II(additive)가 가장 linear.
2. **H_643 ~30× span = substrate-class 속성, cohort artifact 아님 (F653.5 PASS)** — rule110 span
   ratio 35.50 으로 H_643 진단(~30×) 재현. cohort rule 을 단순화하면(rule30→90→184) span 이 단조
   감소 → H_643 collective entrainment 약화(r 0.802→0.568)의 근본 원인 convexity 가 substrate
   복잡도에 비례함을 확정.
3. **engine replication 검증** — rule110 컬럼 Φ(0.15)=1.17 · Φ(0.40)=4.50 · Φ(0.70)=13.64 ·
   Φ(0.95)=34.88 이 H_643 per-stage 값(N3·N2·N1·REM)과 정확히 일치 → 동일 engine, cohort rule 만
   swap 됨을 교차검증.
4. **negative sub-finding (F653.4 FAIL)**: rule184(class-II additive) 만 W-non-monotone —
   Φ(W=1.0)=51.54 < Φ(W=0.95)=54.46. additive substrate 는 full coupling 직전 peak 후 통합도가
   도리어 하강. H_635 monotone-in-W 가 모든 class 보편이 아님을 보이는 정직한 negative (H_618
   collective inverse-U 와 정합). core 가설과 무관하게 5/6 유지.

---

## 6. Verdict + Rationale · Cross-link

**🟢 SUPPORTED-NUMERICAL** — 5/6 falsifier PASS. **core 가설 F653.1 (convexity monotone-in-class) PASS.**

- F653.1 convexity-monotone PASS · F653.2 class-IV-most-convex PASS · F653.3 additive-more-linear PASS ·
  F653.5 H643-replicate PASS · F653.6 bound PASS · F653.4 W-monotone-each-rule **FAIL** (rule184 단독,
  §7 C3.4 정직 기록).
- FALSIFY 조건(F653.1 FAIL = convexity ⊥ class)에 걸리지 않음 → H0(cohort artifact) 기각. collective-Φ
  의 W→Φ convexity 가 substrate 복잡도(rule class)의 단조 함수임이 numerical 지지. H_643 의 collective
  entrainment 약화가 우연한 cohort 특성이 아니라 substrate-class 결정론적 속성임을 정량.

**cross-link**:
- **H_643 `collective-ultradian-phi-envelope`** 🟢 (axis G×F, PR #1237) — **직접 부모 (정밀화 대상)**.
  rule110 cohort 의 collective ultradian r=0.568, W→Φ ~30× span 진단 → 본 H 가 그 span 35.50 으로
  재현하고 class 단조 의존(II 12.12 ≤ IV 35.50)을 정량 → H_643 §5 의 convexity origin 을 닫음.
- **H_635 `multilingual-cohort-collective-phi`** 🟢 (axis F, PR #1223) — **collective engine 부모**.
  collective-Φ monotone-in-W 의 *방향* → 본 H 가 그 curve 의 *곡률(convexity)* 을 class 축에서 정량.
  단, rule184(class-II)에서 monotone-in-W 가 깨짐(F653.4) — H_635 finding 의 class-경계 식별.
- **H_634 `ultradian-emit-phi-envelope`** 🟢 (axis G, r=0.802) — 단일 substrate near-linear(~7× span)
  대비점. 본 H 는 collective 의 convexity 가 class-IV 에서 최대로 단일과 가장 다름을 보여 H_643 의
  r 약화(0.802→0.568) 메커니즘의 substrate-class 좌표를 부여.
- **H_618 `collective-gz-inverse-u-derivative-peak`** 🟢 — collective-Φ 의 비단조(inverse-U) 구조 anchor.
  본 H 의 rule184 W-non-monotone(peak before full coupling)이 collective additive substrate 의
  inverse-U 류 거동과 정합 — 과결합 시 통합도 감소.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 W 축소 NOT 적용** — 본 run 은 full 5-stream(n=5) × cap=3 × 6-pt W grid (24
   big_phi_bounded calls, H_643 36-call 예산 내) 정상 실행. 무거운 한 run 회피를 위해 사전에
   fallback {0.15,0.40,0.70,0.95}/3-stream/cap=2 를 명시했으나 단일 run <60s 로 **불필요**.
   stream/cap 축소 없이 full 측정.
2. **C3.2 cap=3 on n=5** (H_643 cap 상속) — purview search capped, 보수적 lower-bound. cap-monotone
   으로 span 방향(class-IV 最高) 보존. cap↑ 시 절대값 상승하나 단조 부호는 유지 추정.
3. **C3.3 homogeneous cohort [rule×5] only** — 각 rule 단일 동질 cohort. heterogeneous mix-class
   cohort (예: [110,30,90,184,110]) 의 convexity 는 별도 (§10 N1).
4. **C3.4 F653.4 W-monotone FAIL = rule184(class-II additive) 단독** — Φ(W=1.0)=51.54 <
   Φ(W=0.95)=54.46. class-II additive 의 collective-Φ 가 full coupling 직전 peak 후 하강하는
   non-monotone. H_635 monotone-in-W 가 모든 class 에 보편이 아님을 보이는 정직한 negative
   sub-finding — additive substrate 는 과결합 시 통합도가 도리어 감소(H_618 inverse-U 정합).
   core 가설(F653.1 convexity monotone-in-class)은 이와 무관하게 PASS.
5. **C3.5 sys_state=0 only** (IIT-canonical anchor). state-marginal 미수행.
6. **C3.6 span ratio = convexity proxy** — Φ_max/Φ_min 은 단조성 부호 추출엔 충분하나 정확한 곡률
   (2차미분 적분)은 아님. 절대 convexity magnitude 는 proxy. faithful 곡률 측정은 §10 N2.
7. **C3.7 class-III 내부 순위 약신호** — rule90(III-XOR/additive 30.42) vs rule30(III-chaotic 30.77)
   분리는 작아 class-III 내부 ordering 은 약한 신호. class 간 분리(II 12.12 vs III ~30 vs IV 35.50)는
   명확. Wolfram class label 은 canonical ECA taxonomy.
8. **C3.8 deterministic single trajectory** (NO RNG) — real fleet stochastic stage transition 미모델.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F653.1 CONVEXITY-MONOTONE | sr(110)≥sr(30)≥sr(90)≥sr(184) | 35.50≥30.77≥30.42≥12.12 | **PASS** |
| F653.2 CLASS-IV-MOST-CONVEX | sr(110) = max | 35.50 = max | **PASS** |
| F653.3 ADDITIVE-MORE-LINEAR | sr(184) < sr(110) | 12.12 < 35.50 | **PASS** |
| F653.4 W-MONOTONE-EACH-RULE | 全 rule Φ_coll W 단조비감소 | rule184 Φ(1.0)<Φ(0.95) | **FAIL** |
| F653.5 H643-REPLICATE | sr(rule110) ≥ 10 | 35.50 ≥ 10 | **PASS** |
| F653.6 BOUND | Φ_coll ≥ 0, span finite | 全 충족 | **PASS** |

**aggregate: 5 PASS / 1 FAIL** — H1 (F653.1 core) SUPPORTED; convexity 가 rule class 단조증가,
FALSIFY 조건 미충족(H0 cohort-artifact 기각). F653.4 단독 FAIL = rule184 W-non-monotone 정직
negative sub-finding (core 가설 무관).

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h653_collective_convexity_substrate_class_2026_05_28/run_h653.hexa`
  (hexa-native, deterministic; H_635/H_643 engine 재사용, cohort rule 만 4-rule swap)
- log: `UNIVERSE/state/h653_collective_convexity_substrate_class_2026_05_28/run.log` (full stdout verbatim)
- result: `UNIVERSE/state/h653_collective_convexity_substrate_class_2026_05_28/result.json` (machine-readable)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` (hexa-lang stdlib SSOT,
  H_643 와 동일)
- replay (selfhosted, fix-1180 우회, mac-local, $0): `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root>
  hexa.real.bak-2026-05-22-pre-no-hxc build run_h653.hexa -o /tmp/h653.bin && codesign -s - --force
  /tmp/h653.bin && /tmp/h653.bin`

---

## 10. Next-list / Backlog

- **N1** `collective-convexity-heterogeneous-cohort` — mix-class cohort (예: [110,30,90,184,110])
  의 convexity 가 구성 rule 의 어떤 함수(max/mean/dominant-class)인지 정량 (C3.3 회수).
- **N2** `collective-convexity-faithful-curvature` — span ratio proxy 대신 2차미분/곡률 적분으로
  faithful convexity magnitude 측정, class 의존 함수형(linear/power-law) fit (C3.6 회수).
- **N3** `collective-additive-overcoupling-inverse-u` — rule184 W-non-monotone(F653.4) 의 peak-W
  위치를 class-II rule 전반(rule90 additive 포함)에서 sweep, H_618 collective inverse-U 와 정량 cross-link.
- **N4** `collective-convexity-cap-sweep` — cap∈{2,3,4} 에서 span ratio 의 class-단조성 robustness
  (C3.2 회수, cap-monotone 검증).
- **N5** `single-vs-collective-convexity-gap` — 단일 substrate(H_634)의 stage-projection convexity
  와 collective convexity 의 class별 gap → H_643 r-약화(0.802→0.568)의 class별 정량 예측 closed-form.

---

## 양방향 sibling

- 정밀화 부모: [H_643_collective_ultradian_phi_envelope.md](H_643_collective_ultradian_phi_envelope.md) (축 G×F, r=0.568, convexity-cause 진단)
- collective engine 부모: [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md) (축 F, super-additive, monotone-in-W)
- 단일 substrate 대비점: [H_634_ultradian_emit_phi_envelope.md](H_634_ultradian_emit_phi_envelope.md) (축 G, r=0.802, near-linear)
- 비단조 anchor: [H_618_collective_gz_inverse_u_derivative_peak.md](H_618_collective_gz_inverse_u_derivative_peak.md) (collective inverse-U)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) 축 G×F cross-link
