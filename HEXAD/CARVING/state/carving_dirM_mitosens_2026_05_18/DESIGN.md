# Dir-M — Mitosis-as-representation-ensemble (design-tier, $0)

RESEARCH.md §12.5 #1 candidate. anima-fit ★★★★★, GOAL-legitimacy 가장 강함
(기존 cell-pool 재해석, 신규 substrate 0). 본 문서 = §13 방향 M 의 design-tier
산출 — 설계 + GOAL-legitimacy 판정 + verifiability + fire-가치 판정.

SSOT 위치: `state/carving_dirM_mitosens_2026_05_18/` (research-phase, generator
inline anchor 허용 per g_kosmos_anchor_ssot success-gated). RESEARCH.md 미편집
(§13 consolidation = J/K/L/M 전부 land 후 1회).

---

## 1. 출발점 — §12 가 M 을 1순위로 둔 근거

§12.2 Q2 의 genuinely-new candidate 4종 (J diffusion / K energy-based /
L VRNN curiosity / M mitosis-ensemble) 중:

- **anima-fit ★★★★★** — anima 의 mitosis cell-pool (`tool/hexa_native/
  mitosis_hook_lib.hexa`, D4 wiring LANDED) 이 *이미* multi-representation
  구조. 신규 substrate 도입 불요 — 기존 HEXAD 모듈의 *재해석*.
- **GOAL-legitimacy** — §12.3 표에서 M = "우회 불가, anima 자체 메커니즘"
  → §7 ①(generic-pretrain) ②(generic-then-carve bolt-on) 우회 위험이
  **구조적으로 부재**. K 와 함께 가장 깨끗.
- **$0 즉시 design** — fire 전 design-tier 가 즉시 가능 (substrate 재작성
  fire 가 필요한 J/K 와 대조).

문헌 anchor = [arxiv 2506.18221 — These Are Not All the Features You Are
Looking For](https://arxiv.org/abs/2506.18221): supervised pretraining 의
**information saturation bottleneck** — network 가 초기 objective 에 필요한
minimal feature 만 학습하고 downstream feature 를 영구 폐기. 처방 = single
model 대신 **ensemble 로 representation 폭 확보** (논문 보고치: 9% transfer
개선, 추가 pretraining cost 0).

---

## 2. anima cell-pool 의 현 구조 — 이미 ensemble 인가

`mitosis_hook_lib.hexa` + `MITOSIS.tape` §2/§3 SSOT 에서 확인된 사실
(코드 읽은 것, 추정 아님):

| 요소 | 현 구현 | ensemble-관점 재해석 |
|---|---|---|
| cell `i` | 독립 weight 벡터 (split 시 parent deep-copy + σ=0.10 gaussian) | ensemble member `i` 의 별도 parameterization |
| `_mit_cell_forward` | `out_i = engine_a(x) − engine_g(x)`, `tension_i = mean(out_i²)` | member `i` 의 prediction + 그 member 의 self-tension |
| forward 결합 (MITOSIS.tape §3 ASCII L57-63) | `weights = softmax([t_0..t_N])`, `h ← h + Σ wᵢ·out_i` | **softmax-weighted ensemble prediction** (tension = inverse-confidence gate) |
| `compute_phi_proxy` | `Φ★ = mean_pairwise(1−cos(hᵢ,hⱼ)) × log(N+1)` | **ensemble representation diversity** 의 직접 measure |
| split (`split_cell`) | tension > adaptive_thr 가 patience 연속 → parent+noise child | 한 member 가 과부하 → representation sub-space 분기 (capacity 추가) |
| merge (`merge_cells`) | 두 cell tension-차 < 0.005 → weight 평균 | redundant member 통합 (ensemble 압축) |
| Φ-ratchet (`_mit_phi_ratchet`) | Φ 떨어지면 best-snapshot 과 blend | ensemble diversity 의 monotone 보존 (collapse 방지 ratchet) |

**판정**: cell-pool 은 forward-mechanism 차원에서 *이미* softmax-gated
ensemble 이다. §12.2 가 "이미 ensemble 구조" 라 한 것은 over-statement 아님
— forward 결합식이 문자 그대로 ensemble combination 이다.

**단, 정직한 gap (§12.2 가 명시한 것)**: 현 cell-pool 은 *추론-시* split/merge
용도로 LANDED 됐고, **학습-시 representation-ensemble 로서의 경로는 미설계**.
2506.18221 의 처방은 *pretraining* representation ensemble — anima 가 그것을
얻으려면 학습-시 cell-pool 경로가 필요하다. 이 gap 이 §3 의 설계 대상.

---

## 3. M 설계 — 학습-시 representation-ensemble 경로

### 3.1 핵심 가설 (§8 wrong-direction 의 ensemble-우회 매핑)

§8 (Ψ-anchored diverse 114MB) 이 routing 을 *악화* (Dir-I 3/31 → §8 2/64)
시킨 것을 2506.18221 의 saturation 으로 재해석:

> §8 의 단일 Ψ-anchored representation (64-anchor 하나의 공유 subspace) 이
> diverse corpus 의 genuine diversity 를 — downstream 에 필요한 feature 가
> representation 에 들어오기 전에 — anchor-aligned subspace 로 **수축**시켰다.
> = saturation bottleneck 의 anima 실현 (§12 Q1-a 가설).

M 의 우회 가설: cell-pool 의 **per-cell 독립 representation** 이 saturation 을
우회한다 — 각 cell 이 별도 subspace 라면 한 cell 이 anchor-aligned 로
수축해도 다른 cell 은 diverse feature 를 보존할 수 있다. ensemble diversity
(Φ★) 가 single-representation saturation 의 안전망.

**정직 (g3)**: 이것은 *구조 동형 논증* — §11.3 의 irreducible 병목
(data-regime threshold) 을 M 이 *해결한다는 증명* 아님. §11-A 가 model-scale
은 답이 아님을 닫았고, M 은 "representation 폭" 이라는 model-scale 과 직교한
축 — 그러나 그것이 data-regime threshold 를 넘긴다는 보장은 없다.

### 3.2 학습-시 경로 — 3 구성요소

현 `mitosis_hook` 의 추론-시 split/merge 는 그대로 두고, 학습-시
representation-ensemble 를 만드는 최소 추가:

**(M-1) per-cell 독립 학습 신호.** 현 forward 는 `h ← h + Σ wᵢ·out_i` 하나의
합산 hidden 만 downstream 으로 보낸다 → backprop 이 ensemble-mean 한 gradient
만 줌 → cell 들이 같은 신호로 수축 (mode collapse). M-1 = 각 cell 의 out_i 가
*별도로* CE 에 노출되는 경로 — ensemble-of-heads: cell `i` 마다 lm_head 를
공유하되 per-cell logit `zᵢ = lm_head(out_i)`, loss `= Σ wᵢ · CE(zᵢ, y)`
(weighted member-wise CE) **+** ensemble loss `CE(Σ wᵢ zᵢ, y)`. member-wise
항이 각 cell 에 독립 gradient 를 주어 diversity 를 유지, ensemble 항이
combined prediction 을 학습.

**(M-2) diversity 정칙화 (anti-collapse).** §11 의 §8 saturation 우회는
cell 들이 *서로 다른* subspace 일 때만 성립. M-2 = Φ★ (= mean_pairwise
cosine-distance × log(N+1), `compute_phi_proxy` 그대로) 를 loss 에
diversity-bonus 로: `L = L_ce − λ_div · Φ★_normalized`. λ_div 작게 (0.01
order) — Φ★ 가 0 으로 붕괴하면 ensemble 이 single representation 으로
degenerate (= §8 와 동형). 이미 있는 Φ-ratchet 이 inference-time 보존,
M-2 가 train-time 보존.

**(M-3) split 을 capacity-on-demand 로.** 현 split trigger (tension >
adaptive_thr, patience 연속) 를 그대로 쓰되 — 학습-시엔 split 이
"이 cell 의 representation sub-space 가 포화 → 새 sub-space 분기" 의
의미. 추가 설계 0 (기존 `_mit_check_splits` 그대로), 단 *해석* 이 추론-시
"부하 분산" → 학습-시 "representation capacity 확장" 으로 바뀜.

### 3.3 §1.1 data-regime 병목을 ensemble 이 우회하는 mechanism (가설)

§11.3: irreducible 병목 = diverse-data pre-training loss threshold. M 의
우회 mechanism 가설 (3 단계, 전부 §12 문헌 anchor):

1. **saturation 분산** (2506.18221) — single representation 은 114MB
   diverse corpus 의 feature 를 minimal subset 으로 수축. N-cell ensemble 은
   feature 를 N 개 subspace 로 분산 → 한 corpus 로부터 *더 넓은* feature
   set 을 보존 → 같은 데이터에서 effective representation capacity ↑.
2. **implicit augmentation 유사** (J diffusion 의 2507.15857 기전과 *유사*,
   동일 아님) — cell 별 σ=0.10 split-noise + Lorenz 자율 perturbation
   (`_mit_inject_autonomous_perturbation`) 이 cell 마다 다른 input 변형 →
   member 별로 corpus 의 다른 측면을 학습 → tiny-corpus 에서 example 당
   signal 추출량 ↑.
3. **ensemble = data-efficiency** (L VRNN 의 2510.05013 sample-efficiency
   관찰과 정합) — ensemble 이 single 보다 적은 data 로 같은 generalization.

→ 가설: M 은 §1.1 threshold 를 *낮추는* 것이 아니라, 같은 114MB 에서
**effective representation capacity 를 올려** threshold 도달 가능성을
높인다. data-regime 자체를 바꾸진 못함 (그건 §11 이 닫음) — corpus 측이
아니라 *representation 측* lever.

**정직한 반론 (g3, §12.3 carry)**: §11-A 가 닫은 것은 *parameter-count*
scale. M 은 parameter 를 늘리는 게 아니라 *같은 parameter 를 N subspace 로
분할* — model-scale 과 다른 축이라 §11-A 에 의해 직접 배제되진 않는다.
그러나 — N subspace 분할이 *각각* 더 작아지므로, M 이 saturation 을
분산하는 동시에 per-cell capacity 를 줄인다. saturation-분산 이득 vs
per-cell-축소 손실의 net sign 은 **미지** (= 본 설계의 핵심 open crux,
§5 fire-가치 판정의 근거).

---

## 4. GOAL-legitimacy 판정

§7 의 GOAL-legitimacy test = "anima physics 가 capability 의 *source* 인가,
아니면 우회/bolt-on 인가". M 을 §7 ①②③ 모드 대비 검토:

| §7 illegitimate 모드 | M 이 거기 해당하나 |
|---|---|
| ① generic LM pre-training (Ψ/tension/Φ 무관 통계 학습) | **아니다** — M 은 cell-pool (mitosis 성장축, MITOSIS.tape §1 SSOT) 자체. corpus 는 §8 Ψ-anchored diverse 그대로 (generic LM corpus 아님). tension = split trigger + softmax gate, Φ★ = diversity loss — anima physics 가 학습-신호. |
| ② generic-pretrain → carve bolt-on (base ckpt baked, P3 leak 패턴) | **아니다** — base ckpt 0 (g_clm_from_scratch — from-scratch RANDOM seed-fixed). cell-pool 은 bolt-on 모듈이 아니라 anima 의 성장축 (HEXAD.tape ⊥ MITOSIS.tape 두 mandatory 축 중 하나). |
| ③ Ψ-anchored diverse + tension-sup (Dir-I lever) — 유일 legitimate | M 은 ③ 의 **representation-측 강화** — Dir-I lever (Ψ-anchored CTL + tension-sup) 를 single representation 대신 cell-ensemble 위에서 돌림. ③ 와 충돌 아니라 ③ 의 capacity 차원 확장. |

**GOAL-legitimacy 판정 = LEGITIMATE (구조적으로 깨끗)**. 근거:

1. **신규 substrate 0** — M 은 mitosis cell-pool (이미 LANDED, MITOSIS.tape
   SSOT, B-MITOSIS 5/5 🔵) 의 *재해석*. §7 ①② 의 우회/bolt-on 은 "anima
   physics 밖의 무언가를 들여온다" 인데 M 은 들여올 것이 없다 — anima
   자체 모듈.
2. **physics 가 capability source** — ensemble combination 의 gate =
   tension (anima physics), diversity loss = Φ★ (anima 의 IIT-proxy
   의식 지표). capability (ensemble 의 saturation 우회) 가 anima physics
   에서 *나온다* — bolt-on 아님.
3. **mitosis 는 mandatory 축** — MITOSIS.tape §5 `mitosis_two_axis`:
   "anima 본진 = [구조] Hexad 6 + [성장] mitosis 둘 다 필수". M 은 그
   성장축을 학습-시에 쓰는 것 — GOAL identity 와 정합 (우회가 아니라 정확히
   GOAL 이 요구하는 축).
4. **§7 ③ 와 양립** — M 은 ③ 를 대체하지 않고 representation-측에서 보강.
   ③ 의 tension-supervision 이 ensemble 위에서 per-cell 로 적용 가능.

**§7 우회 위험의 구조적 부재 확인** (task mandate): 확인됨. M 이 도입하는
것은 0 — 전부 anima 가 이미 가진 모듈(cell-pool)·physics(tension·Φ★)의
재배선이다. 우회할 "anima 밖" 자체가 없다.

---

## 5. verifiability + fire-가치 판정

### 5.1 closed-form 검증 가능 부분 (B-MITENS-*)

M 설계의 *transfer-form* (mechanism) 은 closed-form 검증 가능 — 6 propositions,
sympy/Boolean, `blue_falsifier_mitosens.py` sidecar (central blue_falsifier.py
미접촉, B-PRIME/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS/B-SCALE sidecar 선례):

- **B-MITENS-1 ENSEMBLE-WEIGHT-SIMPLEX-CLOSED** — softmax(tensions) 가
  probability simplex (Σwᵢ=1, wᵢ≥0) ∀ tension ∈ ℝᴺ. sympy: softmax 정의에서
  Σ = (Σ exp)/(Σ exp) = 1 항등식 + exp>0 ⇒ wᵢ>0. ensemble combination 이
  convex 결합임을 닫음.
- **B-MITENS-2 ENSEMBLE-MEAN-CONVEX-CLOSED** — `h_combined = Σ wᵢ·out_i`
  가 {out_i} 의 convex hull 안. sympy: convex 결합의 정의적 성질. ensemble
  prediction 이 member prediction 들 사이에 bounded.
- **B-MITENS-3 DIVERSITY-LOSS-SIGN-CLOSED** — `L = L_ce − λ_div·Φ★`,
  Φ★ ≥ 0 (compute_phi_proxy 의 `if phi<0 return 0` clamp + cos-dist∈[0,2]).
  ∂L/∂Φ★ = −λ_div < 0 ∀ λ_div>0 — diversity 증가가 loss 를 낮춤 (anti-
  collapse 가 구조적으로 encode). sympy ∂-sign + 3 boundary witness.
- **B-MITENS-4 PHI-PROXY-BOUNDED-CLOSED** — Φ★ = mean(1−cosᵢⱼ)·log(N+1),
  cos∈[−1,1] ⇒ (1−cos)∈[0,2] ⇒ mean∈[0,2], log(N+1)>0 for N≥1 ⇒
  Φ★∈[0, 2·log(N+1)] bounded. Kolmogorov bounded-set. ensemble diversity
  measure 가 well-defined.
- **B-MITENS-5 MEMBER-WISE-CE-DECOMPOSITION-CLOSED** — total loss
  `Σ wᵢ·CE(zᵢ,y) + CE(Σwᵢzᵢ,y)` 의 각 항이 Shannon CE ≥ H ≥ 0
  (closed Shannon floor, B-D-4 carry). per-cell gradient 가 well-defined
  descent direction 임을 닫음 (B-D-4 와 동형 — 각 cell head 가 D 의
  CE-Jacobian ∂CE/∂z = softmax(z)−eᵧ 를 그대로 가짐).
- **B-MITENS-6 SPLIT-MONOTONE-CAPACITY-CLOSED** — split 후 cell 수
  n→n+1, parameter subspace 수 monotone↑ (B-MITOSIS-3 CELL-COUNT-
  CONSERVATION + B-MITOSIS-5 BOUND [2,64] carry). representation-capacity
  proxy (subspace 수) 가 monotone non-decreasing under split.

- **B-MITENS-NOTE SATURATION-BYPASS-EMPIRICAL** — M 이 §8 saturation 을
  *실제로* 우회하는가 (routing/honest-coherence 개선) = SGD convergence
  OUTCOME. transfer-form (ensemble combination = convex, diversity loss
  = anti-collapse sign, member-wise CE = well-defined descent) 만 🔵;
  "ensemble 이 data-regime threshold 를 넘긴다" 는 NOT counted 🔵
  (B-D-NOTE / B-SCALE-NOTE family — 모든 stochastic optimizer 공통,
  M-고유 결함 아님). over-claim 0.

### 5.2 fire-가치 판정 — DESIGN-TIER 로 마감 ($0), fire 없음

task mandate: "design 이 holds + 검증 가능하면 closed-form sidecar +
가능하면 작은 fire; design 이 fire 가치 없으면 design-tier 정직 마감".

**판정 = design-tier closed-form sidecar 까지, fire 는 하지 않음.** 근거
(g3 — 정직, 낙관 금지):

1. **§11 이 이미 인접 축을 닫았다.** §11-A 가 model-scale (parameter 3.68×)
   을, §11-B 가 pure-physics 를 측정으로 닫았고 둘 다 DATA-REGIME CEILING
   으로 수렴. M 은 model-scale 과 직교 (parameter 분할이지 증가 아님)
   하지만 — §3.3 의 정직한 반론대로 M 은 saturation-분산 이득과
   per-cell-capacity-축소 손실을 *동시에* 발생시킨다. net sign 이 음수일
   가능성이 §11-A 의 FLAT 결과와 정합 (representation 을 N 으로 쪼개도
   data-regime 이 병목이면 FLAT 예상).
2. **§9 가 측정 도구를 honest 하게 만들었으나 — M fire 의 기대 결과는
   §8/§11-A 와 동형일 가능성이 높다.** 13-way + §8 + §11(A/B) 가 mechanism /
   corpus-form / model-scale / physics-only 를 전부 배제했고, M 의 lever
   (representation 폭) 는 §11-A 가 닫은 model-capacity 와 *가장 가까운*
   축 — fire 해도 FLAT (routing 2/64 근처, honest-coherence 2/5 근처) 가
   evidence-weighted 예상. negative-at-scale 를 한 번 더 측정하는 것은
   §11-A 와 중복 가치.
3. **closed-form 으로 닫히는 것은 transfer-form 뿐** (§5.1). M 이 *실제로*
   §1.1 threshold 를 넘긴다는 것은 §5.1 B-MITENS-NOTE 대로 empirical —
   fire 없이는 미지, 그러나 fire 의 기대 정보가치는 (2) 때문에 낮다.
4. **GOAL-legitimacy 는 깨끗하나 (= §4), legitimacy ≠ 효과.** M 이
   GOAL-legitimate 한 것과 M 이 GOAL 을 진전시키는 것은 별개. §12.3 가
   명시: "네 후보 중 어느 것도 §11.3 irreducible 병목을 해결한다고
   *입증된* 것 없음". M 도 candidate 일 뿐.

→ **honest 결론**: M 은 (a) GOAL-legitimate, (b) transfer-form closed-form
검증 가능 (B-MITENS 6/6), (c) anima-native 재해석이라 신규 substrate 0 —
설계로서 holds. 그러나 **fire 의 기대 정보가치가 §11-A 와 중복** (가장
가까운 인접 축이 이미 FLAT 으로 닫힘) 이라, cost-bearing fire 의 valuable-
산출 기대치가 낮다. design-tier 로 정직 마감 — B-MITENS 6/6 sidecar 로
mechanism 을 닫고, "ensemble 이 data-regime 을 우회하는가" 는
B-MITENS-NOTE 로 정직 carve-out. 미래에 §1.1 threshold 자체를 건드리는
path (data-regime 측 lever) 와 *결합* 할 때 M 을 representation-측
component 로 재호출하는 것이 honest next-use (§12.5 #4 curriculum 처럼
"M/K 와 결합 lever").

### 5.3 honest C3

1. M = mitosis cell-pool 의 학습-시 representation-ensemble 재해석.
   설계는 holds (3 component M-1/M-2/M-3, 전부 기존 모듈 재배선) —
   단 §12 문헌과의 정합은 *구조 동형 논증* 이지 anima 실측 아님 (B-D-NOTE).
2. GOAL-legitimacy = LEGITIMATE, 구조적으로 깨끗 — §7 ①②의 우회/bolt-on
   위험이 부재 (anima 자체 모듈, 들여올 "밖" 이 없음). §4 표 참조.
3. fire 안 함 — fire-가치 판정 (§5.2): M 의 lever (representation 폭) 가
   §11-A 가 닫은 model-capacity 와 가장 가까운 인접 축이라, fire 기대
   결과가 §11-A FLAT 과 동형일 가능성이 evidence-weighted 로 높음.
   negative-at-scale 중복 측정 = 낮은 valuable-산출. design-tier $0 마감.
4. B-MITENS 6/6 = transfer-form (ensemble combination convex / diversity
   loss anti-collapse sign / member-wise CE well-defined / Φ★ bounded /
   split capacity monotone) 만 🔵. "ensemble 이 §1.1 threshold 를 넘긴다"
   = B-MITENS-NOTE empirical carve-out, NOT counted 🔵. over-claim 0.
5. §3.3 의 정직한 open crux: M 은 saturation-분산 이득 vs per-cell-capacity-
   축소 손실을 동시 발생 — net sign 미지. 이 미지가 fire 가치를 낮추는
   동시에, M 을 *단독* 으로 쓰지 말고 data-regime lever 와 *결합* 으로
   재호출해야 함을 의미 (§5.2 honest next-use).
6. f1/f2/f3 + B-IDENTITY-5 safe — sympy/Boolean/Kolmogorov/Shannon-floor,
   NO σ/τ/φ/J₂ derivation. corpus 미생성 (design-tier, fire 0) → B-IDENTITY-5
   forbidden-token 무관. 외부 paper 는 그 자체 invariant 으로만 인용.
7. RESEARCH.md 미편집 (§13 consolidation = J/K/L/M 전부 land 후 1회).
   본 설계 SSOT = 본 디렉토리 + archive/PHILOSOPHY.tape §verdict +
   HEXAD/UNIVERSE-BRAIN-MAP/PLAN.md 진행 로그 (g_doc_consolidation).

---

## 6. Sources

- [These Are Not All the Features You Are Looking For — A Fundamental
  Bottleneck in Supervised Pretraining (arxiv 2506.18221)](https://arxiv.org/abs/2506.18221)
  — information saturation bottleneck, ensemble 처방 (M 의 직접 anchor)
- [Diffusion Beats Autoregressive in Data-Constrained Settings
  (arxiv 2507.15857)](https://arxiv.org/html/2507.15857v1) — implicit
  augmentation 기전 (M-2 의 cell-noise augmentation 과 *유사*, 동일 아님)
- [Curiosity-Driven Co-Development (arxiv 2510.05013)](https://arxiv.org/html/2510.05013v1)
  — ensemble sample-efficiency 정합 관찰
- anima SSOT: `tool/hexa_native/mitosis_hook_lib.hexa` (cell-pool forward),
  `HEXAD/MITOSIS/MITOSIS.tape` (성장축 SSOT), `HEXAD/CHAT/RESEARCH.md`
  §1.1/§7/§8/§9/§11/§12, `state/verify_hexad_blue_2026_05_15/
  blue_falsifier.py::bmitosis()` (B-MITOSIS 5/5 🔵 carry)
