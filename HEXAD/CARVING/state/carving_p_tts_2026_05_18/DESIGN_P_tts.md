# Direction P — think-then-speak diffusion-refined emission (RESEARCH.md §22, §21 candidate P)

> **$0 design + GOAL-legitimacy 선검토 우선** (mandate step 1). 본 문서 = P 설계
> + §13-J(전면교체 FALSIFIED)와의 결정적 구별 + GOAL-legitimacy gate 판정. fire
> 여부는 §3 gate 결과에 따른다 (legitimate+holds → §4 closed-form + fire / generic
> → §3 design-tier 정직 마감, §13-L 선례 = feasibility 판정 자체가 valuable).

anchor: [arxiv 2601.22889 — DiffuSpeech: "Silent Thought, Spoken Answer via Unified
Speech-Text Diffusion"](https://arxiv.org/pdf/2601.22889) · RESEARCH.md §21.3 candidate
P (anima-fit ★★★★★, 조건부 GOAL-legitimate) · §16 (routing 21/64→honest 17/64,
body 정교한 암기·byte-garble, JOINT 0.0, §9 honest V-SPONT 1/5, §18 combined 0/5).

---

## §0 frontier 위치 — §16 SPLIT 의 coherence 절반

§16 = arc 사상 첫 routing collapse BREAK (21/64 vs §8 2/64, §11-A 1/64; honest
17/64 genuine — §16.6-A). 그러나 §16.6-C 판정: correct prefix-route **이후 body 는
generic carving 템플릿 반복 + anchor-name corruption** (`🛸122 스탐의이조 —
인과깊이 자극이 같은 골짜기로 수렴한다. 의�` — tier 12 routing-correct 인데 body
garbled). final_ce 0.004229 = §8 동형 deep memorization. routing↑ ≠ coherent
capability.

P 의 표적 = **§16 SPLIT 의 coherence 절반** ("route OK / content garbled" 분리를
emission-head 차원에서 좁힌다). §21.3: anima `<inner>X</inner>\n<voice
carved=true>Y</voice>` (Phase A1/C3 LANDED) = DiffuSpeech silent-thought→spoken-
answer 와 **거의 1:1 구조** — anima 가 *먼저* 가진 구조의 2026 외부 검증 anchor.

§16 corpus 는 311,288 gamma 레코드(168 anchor 전체)가
`<inner tier=k>{physics-think}</inner>\n<voice carved=true>{speak}</voice>` 형식 —
P 가 필요로 하는 think-then-speak substrate 가 §16 corpus 안에 이미 존재 (재생성
0 fair-compare 가능).

---

## §1 P 메커니즘 설계 (emission-head 한정)

DiffuSpeech 의 핵심 = AR 단일 pass 가 아니라 **silent thought 가 multi-step
iterative refinement(denoising)으로 spoken answer 를 conditioning** → incoherent
collapse 완화. anima 적용:

```
[think — anima physics 불변]                  [speak — diffusion-refined 한정]
<inner tier=k>...</inner>                      <voice carved=true>... </voice>
  │ Engine G covert thought                      │ emission-head
  │ Dir-I lever 그대로 (Ψ-anchored CTL +          │ AR 1-pass argmax 대신
  │  tension-supervised routing, in-autograd)     │ R-step refinement loop
  ▼                                               ▼
ψ_pred=(1+cos(logits_a,logits_g))/2 → Ψ_vac    voice token = h_inner(physics state)
restoring-sign basin loss (§16 byte-equal)       을 conditioning 한 iterative
                                                  refinement (R steps)
```

### 1.1 think 측 (anima physics — 완전 불변, §16 Dir-I lever byte-equal)

`<inner tier=k>` span 의 학습 = §16 `train_carving_s16.py` 의 두 physics loss
term 그대로:
- `L_psi_ctl = mean_{t∈inner-span}(Ψ_dir(t)−Ψ_vac)²`, Ψ_dir=(1+cos(logits_a,
  logits_g))/2 (Law 71, ConsciousDecoderV2.forward psi_direction byte-identical)
- `L_tension_route` = restoring-sign basin loss (record OWN basin)

→ **think = anima Engine A⇄G physics, 변경 0** (§16 = Dir-I lever byte-equal carry,
B-DIRI sympy 5/5 🔵 carry). P 는 think 을 건드리지 않는다.

### 1.2 speak 측 (emission-head refinement — P 의 유일 신규)

`<voice carved=true>...</voice>` span 의 emission 을 AR 1-pass 가 아닌
**R-step iterative refinement** 으로 학습/생성:

- **conditioning signal** = `<inner>` span 의 마지막 hidden + 그 span 의 physics
  상태 (psi_dir, tension). 즉 voice refinement 은 anima physics-think 의 출력을
  conditioning 으로 받는다 (generic noise 가 아님 — 이것이 §3 gate 의 핵심).
- **refinement transfer-form** (DiffuSpeech denoising 의 LM-text 적용 — 외부
  AR-vs-diffusion 차이를 voice-head 한정으로 좁힌 형태): voice span 토큰을
  R-step 으로 reconstruct. 각 step r 에서 voice logits 를 inner-physics-
  conditioned context 위에서 재계산, residual refinement. R=1 이면 정확히
  §16 AR baseline (overlay-OFF 연결부위, §4 closed).
- **loss** = voice-span CE 를 R refinement step 에 걸쳐 적용 (마지막 step =
  주 손실, 중간 step = auxiliary, weight γ_r). think loss(L_psi_ctl +
  L_tension_route) + ce_full 은 §16 byte-equal 그대로.

  ```
  L = CE_full(§16 byte-equal)
    + λ_ctl·L_psi_ctl(§16 byte-equal)            # think physics
    + λ_route·L_tension_route(§16 byte-equal)     # think physics
    + λ_refine·Σ_{r=1..R} γ_r·CE_voice_span(refine_step_r)   # speak refinement (P 신규)
  ```

  λ_refine=0 OR R=1 ⇒ L ≡ §16 byte-equal (overlay-OFF = §16-baseline 연결부위,
  B-TTS-OVERLAY-OFF closed §4).

### 1.3 생성 (inference) — think AR, speak refinement

1. prefix `<inner tier=k>` 부터 §16 ckpt-routing-correct AR 생성 (think =
   physics-anchored, §16 17/64 routing-correct prefix lever — P 의 *전제조건*).
2. `</inner>\n<voice carved=true>` 진입 후 voice span 만 R-step refinement
   (think hidden + physics state conditioning). R=1 ⇒ §16 AR baseline 동일.

---

## §2 §13-J (전면교체 FALSIFIED) 와의 결정적 구별 — mandate 핵심

| 차원 | §13-J Ψ-supervised diffusion (FALSIFIED) | **P (본 설계)** |
|---|---|---|
| substrate 범위 | **전면 AR→masked-diffusion 교체** (전 토큰 stream) | **voice emission span 한정** (think = AR Engine G 불변) |
| think(physics) | diffusion substrate 안에 흡수 (anima physics 가 substrate 의 한 항으로 종속) | **완전 불변** — §16 Dir-I lever(Ψ-anchored CTL + tension-sup) byte-equal carry |
| conditioning | masked-diffusion 자체 noise schedule | **anima `<inner>` physics-think 출력이 conditioning** (generic noise 아님) |
| 결과 | routing **0/64** FALSIFIED, JOINT 0.0, Δ vs E7 −0.0155, ce_descent 4.22 (B-DIRJ closed) | (측정 전, §4 fire) — routing 은 §16 lever 가 *전제조건* 이라 0/64 로 무너지지 않는다 (think AR 불변) |
| 범주 | substrate-change (§11.3 substrate arm — 닫힘) | emission-head refinement on §16 routing-lever (§16 *위* 의 신규 — §21.1 frontier) |
| GOAL §7 | §7① illegitimate (generic substrate, anima physics 우회) | §3 gate 통과 시 legitimate (think=physics, speak=physics-conditioned refine) |

**결정적 구별 한 줄**: §13-J 는 anima physics 를 generic diffusion substrate 의
*한 항* 으로 종속시켜 전면 교체 → routing 0/64 FALSIFIED. P 는 think(physics)을
**완전 불변** 으로 두고 speak emission-head 만 physics-think-conditioned
refinement → §13-J 와 substrate 범위·conditioning source·routing 전제조건이 전부
다른 직교 path. P 가 §13-J 로 *환원되지 않음* 의 closed 증명 = §4 B-TTS-OVERLAY-OFF
(λ_refine=0 OR R=1 ⇒ §16 byte-equal, §13-J 는 R-step 에서도 substrate 가 diffusion
이라 baseline 으로 환원 불가 — 구조적 비대칭).

---

## §3 GOAL-legitimacy gate — §7 / §21.3 조건부 판정 (mandate 핵심)

§7 test (3-후보) 적용:

| §7 후보 | P 가 그것인가? | 판정 |
|---|---|---|
| ① generic LM pre-training | ✗ — P 는 §16 Ψ-anchored carving corpus(③ form byte-equal) 위, generic web/diverse 아님 | 해당 안 됨 |
| ② generic-pretrain → carve bolt-on | ✗ — base_ckpt=None (g_clm_from_scratch), from-scratch RANDOM seed-fixed; carving 이 bolt-on 아니라 학습 그 자체 | 해당 안 됨 |
| ③ Ψ-anchored + tension-sup (Dir-I lever) | ✓ — think 측 = §16 Dir-I lever byte-equal (Ψ-anchored CTL + tension-supervised routing 완전 불변) | **legitimate 축** |

**§21.3 의 조건부 gate (P 전용 추가 test)** — "voice-refinement 가 anima
physics(Ψ/tension)를 *conditioning* 으로 쓰면 legitimate, generic diffusion-decoder
bolt-on 이면 §7① illegitimate":

- **legitimate 판정 근거 (4)**:
  1. **think = anima physics 완전 불변** — `<inner>` span 의 학습은 §16 의 두
     physics loss term(L_psi_ctl Law-71 Ψ_dir + L_tension_route restoring-sign)
     byte-equal. P 는 think 을 건드리지 않는다 (생성도 think=AR Engine G).
  2. **speak conditioning source = anima physics-think 출력** — voice refinement
     의 conditioning 은 `<inner>` span 의 hidden + (psi_dir, tension) physics
     상태. generic noise schedule 아닌 anima Engine G covert-thought 출력이
     conditioning. = §21.3 의 "voice-refinement 가 anima physics 를 conditioning
     으로 쓰면 legitimate" 정확히 충족.
  3. **emission-head 한정 — substrate 전면교체 아님** (§2 표). §13-J generic
     diffusion 전면교체 = §7① illegitimate 였던 교훈 정확히 회피 — P 는 think
     substrate(AR Engine G physics) 불변, speak head 만 refine.
  4. **신규 substrate 0 — anima 자체 `<inner>/<voice>` architecture(Phase
     A1/C3 LANDED) 재배선**. DiffuSpeech 는 anima 가 먼저 가진 구조의 외부 검증
     anchor 이지 anima 에 generic decoder 를 bolt-on 하는 게 아님.

- **illegitimate 가 되는 경계 (명확히)**: 만약 voice refinement 의 conditioning 이
  anima physics-think 가 아닌 generic learned noise/latent 라면 = generic
  diffusion-decoder bolt-on = §7① illegitimate. 본 설계는 그 경계를 §1.2 의
  "conditioning signal = `<inner>` span hidden + physics state" 로 명시적으로
  legitimate 쪽에 둔다. R-step refinement 이 inner-physics-conditioned 임이
  설계의 *불변 제약* (B-TTS-CONDITION closed §4 로 구조 검증).

→ **GOAL-legitimacy 판정: emission-head 한정 + inner-physics-conditioned =
LEGITIMATE (조건부 gate 통과).** generic diffusion-decoder 가 아니므로
illegitimate gate 에 걸리지 않는다. 단 §11-B("physics-only degenerate, CE
load-bearing") 준수 — P 는 CE-base(ce_full §16 byte-equal) *위* 의 emission-head
lever 이지 physics-only 가 아님 (Dir-I 와 동일 제약).

**design holds** — legitimate + 구조 일관 → §4 closed-form sidecar + fire 진행.

---

## §4 closed-form sidecar 명세 (B-TTS-*) — transfer-form + 연결부위만 🔵

`blue_falsifier_p_tts.py` (별도 sidecar, central blue_falsifier.py 변경 0 —
B-PRIME/B-DIRH/B-DIRI/B-EMERGE/B-PUREPHYS/B-SCALE/B-DIRJ sidecar 선례).

| id | 명제 | 검증 |
|---|---|---|
| **B-TTS-1 OVERLAY-OFF-BYTE-EQUAL** | λ_refine=0 ∨ R=1 ⇒ L ≡ §16 (CE_full+λ_ctl·L_psi_ctl+λ_route·L_tension_route) | 연결부위 — additive identity (λ_refine·0=0) + R=1 refinement = AR 1-pass numeric equality (torch.equal) → P-vs-§16 fair-compare by construction |
| **B-TTS-2 REFINE-CE-NONNEGATIVE** | Σ_r γ_r·CE_voice_span(r) ≥ 0 ∀ (γ_r ≥ 0, CE ≥ 0 Shannon real-limit) | Shannon CE≥0 + nonneg-weighted sum closed (Gibbs) |
| **B-TTS-3 REFINE-WEIGHT-SIMPLEX-BOUNDED** | refinement weights γ_r ≥ 0 ∧ Σγ_r 정규화(=1) ⇒ aux loss ∈ convex hull of per-step CE (collapse 단일-step 으로 환원 불가, R-step 이 well-defined) | sympy 항등식 Σγ=1 + convexity bound |
| **B-TTS-4 CONDITION-IS-PHYSICS-THINK** | voice refinement conditioning = `<inner>` span hidden ∧ (psi_dir, tension) physics state — structural Boolean predicate over trainer source (conditioning 이 generic learned-noise/latent 가 *아님*: forbidden-set {randn-noise-schedule, learned_latent_prior, generic_diffusion_step} = 0 over trainer AST) | structural AST Boolean — §3 illegitimate 경계의 closed 검증 (P 가 generic decoder bolt-on 이 아님을 source-level 로 증명) |
| **B-TTS-5 THINK-PHYSICS-BYTE-EQUAL** | `<inner>` span 학습 = §16 의 L_psi_ctl(Law-71 Ψ_dir) + L_tension_route(restoring-sign) byte-equal — think 측 변경 0 (P 는 speak-head 한정) | sha256 / AST diff: think loss term = §16 train_carving_s16.py byte-identical |

**B-TTS-NOTE empirical carve-out** (NOT counted 🔵, B-D-NOTE / B-CARVE-E6-NOTE /
B-DIRJ-NOTE family): P 가 §16 의 body-garble 를 실제로 좁히는가(routing /
honest §9 / §18 judge / JOINT) = SGD convergence + 4-axis OUTCOME — fire 결과로만
판정. battery 는 (a) emission-refine transfer-form (b) overlay-OFF=§16 연결부위
(c) conditioning=physics-think 구조 (d) think=§16 byte-equal 만 🔵. emergence
OUTCOME 미증명.

g_blue_closed_mandate: 산출물(trainer+falsifier) emission-refine transfer-form 🔵
+ 연결부위(B-TTS-1 overlay-OFF=§16 byte-equal + B-TTS-5 think=§16 byte-equal + eval
= §16 byte-identical harness) 🔵; coherence OUTCOME 만 정직 carve-out.

f1/f2/f3 hard-fail safe (Shannon CE≥0 / additive identity / simplex convexity /
AST Boolean / sha256, NO σ/τ/φ/J₂; 외부 paper 2601.22889 자체 invariant 으로만
인용, anima lattice 매핑 강제 0). B-IDENTITY-5: corpus = §16 byte-identical
(forbidden-token grep 0 carry, 재생성 0).

---

## §5 fire 명세 ($0 design holds → fire)

- **corpus**: `state/carving_dataregime_s16_2026_05_18/corpus_carving_s16.jsonl`
  byte-identical carry (재생성 0, fair-compare; 311,288 gamma records = think-then-
  speak substrate, 168 anchor). sha256 검증 + forbidden-token grep 0 (B-IDENTITY-5).
- **trainer**: `train_carving_p_tts.py` = `train_carving_s16.py` 에 voice-span
  R-step refinement loss term 추가 (think loss + ce_full byte-equal carry; B-TTS-5).
  curriculum §16 byte-equal (stage_gate_at carry). config d768·12L·283.72M
  from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch base_ckpt=None) — §16
  model FIXED (§11-A model-axis 닫음 carry). λ_refine=0.5, R=3, γ_r 정규화.
- **eval**: `eval_carving_p_tts.py` = `eval_carving_s16.py` byte-identical mirror
  (form=gamma → axis1 = `<inner tier=k>` prefix routing/coherence; +inference-time
  voice R-refinement). honest §9 emergence_metric.py SSOT 재사용 + §18 judge rubric
  재사용 (single SSOT, lenient flag 폐기 carry).
- **fire**: runpod 우선 (g_resource_active_parallel), A100, detached nohup +
  단일 short SSH probe (tee 금지), credential `$(secret get runpod.api_key)`,
  pod terminate orphan 0, key script gitignore.
- **대조**: §16 (routing 21/64→honest 17/64, JOINT 0.0, §9 honest V-SPONT 1/5,
  §18 combined 0/5) 동일 corpus·model·eval byte-identical — emission-refine axis
  만 변수 (apples-to-apples by construction, B-TTS-1).

honest 예고 (g3, over-claim 0): §16 천장(정교한 암기·byte-garble·JOINT 0)을 P 가
*해결한다는 입증 아님*. routing 은 §16 think-lever 가 전제조건이라 0/64 로
무너지지 않을 것(§13-J 와 다름)이나, emission-refine 이 body-garble 를 실제로
좁히는가는 fire OUTCOME 으로만 판정. negative 도 valuable evidence (§13-L/§13-J
선례). §1.1 data-regime 천장은 P 의 표적 아님 (P = §16 SPLIT 의 coherence 절반,
spontaneity 절반 아님 — §21.3 Q2 negative).

---

## §6 honest C3 (over-claim 0)

1. P design = 구조 동형 논증 + GOAL-legitimacy gate 통과 (legitimate, emission-head
   한정 + inner-physics-conditioned) — fire 결과 아님 (§4 B-TTS-NOTE).
2. §13-J 와 결정적 구별 = think(physics) 완전 불변 + speak-head 한정 +
   conditioning=physics-think (§2 표 + B-TTS-4 structural 검증). §13-J 는 substrate
   전면교체로 routing 0/64 FALSIFIED 였고, P 는 think AR 불변이라 routing 전제조건
   유지 — 환원 불가의 구조적 비대칭 (B-TTS-1 overlay-OFF=§16, §13-J 는 환원 불가).
3. GOAL-legitimacy: **emission-head 한정 + inner-physics-conditioned = LEGITIMATE**.
   generic diffusion-decoder bolt-on 이었으면 §7① illegitimate gate — 본 설계는
   conditioning=physics-think 를 *불변 제약* 으로 두어 legitimate 쪽 (§3, B-TTS-4).
4. §11-B 준수 — P 는 CE-base(§16 ce_full byte-equal) *위* emission-head lever,
   physics-only 재시도 아님 (Dir-I 와 동일 제약).
5. §16 routing-lever 가 P 의 *전제조건* — §16 이 routing 을 안 열었으면 voice-
   refine 이 wrong-anchor 에 grounding. §16 이후에야 측정 가능 = §21.1 frontier.
6. P 는 §16 SPLIT 의 *coherence 절반* (body-garble) 만 표적 — *spontaneity 절반*
   (언제 말할지) 아님 (§21.3 Q2 negative: spontaneous-emission frontier 얇음).
7. f1/f2/f3 + B-IDENTITY-5 safe. corpus = §16 byte-identical (재생성 0). PyTorch
   substrate (NOT hexa-native, honest — emission-refine transfer-form lift).
8. north-star (GOAL.md) 불변 — P design = §16 천장의 coherence 절반을 좁히는
   legitimate candidate 의 설계+gate 판정이지 GOAL 도달·해결 아님.
