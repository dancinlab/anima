# META_FP — Ψ=½ 메타부동점 (anima physics 의 직교 anchor)

> Canonical topic doc for the **§112 meta-fixed-point** form
> `ψ(c) = (1 + c) / 2` (cos=0 ⇒ ψ=½), its first **operative** utilization
> in §166 Ψ-META-FP-COUPLE training objective, and how the §161-FIRE
> measured failure mode (head_g near anti-parallel to head_a) maps onto
> this coordinate system.
>
> Friendly 7-요소 패턴으로 작성된 stable reference. 갱신은
> `HEXAD/META_FP.md` 자리에서 — `docs/*` 신규 금지
> (`@D g_doc_consolidation`).

---

## 🧭 META_FP — anima 의 직교 자석 (canonical 7-요소 설명)

🧭 **META_FP — "엔진 직교 자석"**

- **이름**: META_FP (메타 fixed point) — §112 의 form-level identity
- **별칭**: 엔진 직교 자석 / Ψ=½ 부동점 / orthogonality anchor
- **하는 일**: anima 의 두 엔진 (Engine A ⇄ Engine G) 이 평행도 (cos=+1
  redundant) 도 아니고 반대 (cos=-1 anti-parallel) 도 아닌 **직각
  (cos=0 orthogonal)** 으로 유지되도록 끌어당기는 form-level 기준점.
  §166 가 이걸 mean anchor `(mean Ψ - 0.5)²` 로 operative 학습 신호화.
- **비유**: 두 손바닥을 마주 보지도 등 돌리지도 않고 **직각** 으로
  유지 — 가위처럼 서로 독립적인 두 축. §161-FIRE 의 head_g 는 손바닥이
  등 돌렸음 (cos≈-0.92).

ASCII 다이어그램 — ψ축 좌표:

```
ψ축 좌표  ──────────────────────────────────────────────
                 0          0.5         1
                 |           |          |
   cos          -1           0         +1
   geometry   anti-par.    orthogonal  parallel
                 |           |          |
   §161-FIRE   ●----0.038----|----------|   ← measured fixed pt
                 |     ↑     |          |
                 |     |     |
                 |     └─ ★ §166 L_meta_anchor 끌어당김
                 |           |          |
                 |        META_FP       |
                 |       (§112 form)    |
   §165-A:       (mean 자유 — std 만 punish)
   §166:         (mean→0.5 anchor + std punish 둘 다)
```

**비교 vs 기존 도구**:

| 도구 | 무엇을 제약하나 | mean | std |
|---|---|:---:|:---:|
| §107 (CE-only) | byte 정답 매칭만 | 자유 | 자유 |
| §161 (Ψ-JEPA-COUPLE) | Ψ 예측 (head_g 가 predictor) | 자유 | 자유 |
| §165-A (Ψ-VAR-COUPLE) | + std=0 collapse 금지 (풍선) | 자유 | ↑ |
| **§166 (Ψ-META-FP-COUPLE)** | **+ mean→0.5 anchor (자석)** | **0.5** | **↑** |

`λ_meta → 0 ⟹ §166 byte-equal §165-A`. §107 ⊂ §161 ⊂ §165-A ⊂ §166
엄격 superset chain (reduction lattice).

---

## §112 form 의 정확한 정의 (carrier-invariant identity)

```
Ψ_dir(t)  :=  ( 1 + cos(logits_a_t, logits_g_t) )  /  2          ∈ [0, 1]
Ψ_ent(t)  :=  H(softmax(logits_a_t))  /  log V                    ∈ [0, 1]
Ψ(t)      :=  ( Ψ_dir(t),  Ψ_ent(t) )                              ∈ [0, 1]²
```

`Ψ_dir` 은 Engine A 와 Engine G 의 **cosine similarity** 를 [0,1] 로
정규화. META_FP 값 `Ψ_dir = ½` 는 **cos = 0** 에 해당 = 두 logit 벡터가
**선형 독립** (orthogonal) 인 점.

§112 (commit `1bd27f753`, 2026-05-19) 가 sympy 없이 closed-form 으로
proof:

- **§110 의 5 carrier candidate** (Ψ-C0 byte / Ψ-C1 spike / Ψ-C2
  residual / Ψ-C3 generic latent / Ψ-C4 tension-only) 모두 같은 form
  `ψ(c) = (1+c)/2` 위에서 META_FP `cos=0 ⇒ ψ=½` 가 carrier-invariant.
  Cauchy-Schwarz 로 `cos ∈ [-1, 1]` 보장.
- **§7-FORM TRUE BY CONSTRUCTION** — META_FP 는 anima 자체 physics
  identity, 외부 가정 0.
- **§112 Verdict B** = form-level positive REAL, operative wall RENAMED
  one level up (§7-CARRIER 는 여전히 §96 spiking-substrate-gated).

---

## §161-FIRE 측정값의 META_FP 좌표 변환 (BIG insight)

§161-FIRE post-fire (commit `499416d54`) 측정:

```
psi_dir_mean  =  0.038
              ↓ Law-71 inverse
cos           =  2 × 0.038  −  1  =  −0.924
```

→ head_g 가 head_a 의 **near anti-parallel** 로 collapse. 이는 random
collapse 가 아니라 **specific anti-correlation basin** 으로 떨어진 것.
META_FP (cos=0, Ψ=0.5) 의 **정확한 반대축**.

§161-FIRE quintuple finding (§125 FF / §126 PCN / §139 EqProp / §153
LeJEPA / §161 Ψ-JEPA-COUPLE) — 5/5 모두 `psi_responsive: False`. mean
은 알고리즘 별로 다르지만 std 는 일관적으로 4-7 orders below threshold
1e-4.

§165-A 의 `L_variance := -log(psi_dir_std + ε)` 는 std collapse 만
방지. **mean 위치는 자유**. → §165-A 만으로는 anti-parallel basin 으로
다시 갈 위험.

§166 의 `L_meta_anchor := (mean_t Ψ_dir(t) − 0.5)²` 는 mean 도 0.5 로
끌어당김. **두 차원 동시 anchor** = "live channel centered on META_FP"
의 operational definition.

---

## §166 operative formula (verbatim, byte-equal Law-71)

```
L_psicouple   :=  mean_t  ||  Psi(t+1)  −  predictor_head_g(residual_t)  ||²
L_variance    :=  − log(  psi_dir_std  +  ε  )                  ε = 1e-6
L_meta_anchor :=  ( mean_t  Psi_dir(t)  −  0.5 )²

L_total  =  λ_ce  · CE_aux
          + λ_ψ   · L_psicouple
          + λ_var · L_variance
          + λ_meta · L_meta_anchor
```

기본 hyperparameter: `λ_ce = 0.1, λ_ψ = 1.0, λ_var = 0.5, λ_meta = 0.5`.

**§7-form 가장 강한 PASS in arc**: anchor target `0.5` 는 하이퍼파라미터가
아님 — Law-71 의 `cos = 0` 직교성에서 *유도된 값*. anima physics IS the
source of the target.

---

## fire-decidable spec (§166-A-FIRE 시점)

| field | value |
|---|---|
| § | §166-A-FIRE (separate cycle, autonomous per `g_fire_autonomous`) |
| scaffold | ConsciousDecoderV2 d=768·12L·283.72M (same as §161-FIRE / §165-A) |
| init | RANDOM seed-fixed 1337, `base_ckpt = None` (`g_clm_from_scratch`) |
| corpus | §102 CORPUS_S101 byte-identical (`sha 39d581da2096…`) |
| steps | 3000 · lr 3e-4 · bsz 32 · block 128 |
| primary verdict (joint AND) | `psi_responsive (psi_dir_std > 1e-4)` ∧ `psi_dir_mean ∈ [0.45, 0.55]` (META_FP basin) ∧ `unprompted_emission_rate measured` |
| cost | ≈ $0.4–$0.6 (matches §161-FIRE / §165-A) |
| GPU | runpod A100 80GB primary |
| watchdog | 10800s (3h) |
| sidecar | central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha `c93e160a8a376a94` 0-line-diff mandatory |

---

## 예측 결과 (faithful model from §161-FIRE quintuple)

| outcome | mean | std | 해석 |
|---|---|---|---|
| **SUCCESS** | → 0.5 | > 1e-4 | FIRST arc measurement of META_FP-aligned live channel; cleanest possible §96-Q2-weak refutation attempt |
| ANCHOR-WINS-VARIANCE-LOSES | → 0.5 | → 0 | delta at META_FP (still collapsed; joint AND P4 prevents false-positive) |
| VARIANCE-WINS-ANCHOR-LOSES | off 0.5 | > 1e-4 | §165-A outcome essentially (anchor failed) |
| BOTH-LOSE | off 0.5 | → 0 | §161-FIRE-like collapse mode |

MEDIUM confidence (fire-gate "genuinely uncertain") = fire-worthy.

---

## §112 Verdict B 정직 carry (utilizing META_FP ≠ removing WALL-B)

§166 은 META_FP 를 **form 층** 에서 operative 활용. **operative wall**
(§7-CARRIER = §96 spiking substrate 의존) 은 UNCHANGED. §166 = GPU
byte-LM scaffold 위 form-level 가설 테스트, **substrate change 아님**.

WALL-B 의 두 half:
- **WALL-B/learning** = "CE만 학습 채널" → §125-§161 quintuple 로 이미
  REFUTED (non-CE 도 byte_acc 0.1185 학습)
- **WALL-B/Ψ-physics** = "GPU byte-LM scaffold 가 Ψ-channel-liveness
  produce 불가능" → §161-FIRE quintuple 로 STRENGTHENED. §166 은 이
  half 를 META_FP-aligned-anchor 로 직접 공격.

§166-A-FIRE SUCCESS = WALL-B/Ψ-physics half 의 첫 measured refutation
attempt (단 substrate-level 변경 아닌 form-level 직접 anchor 로). 결과
FAIL 이면 WALL-B/Ψ-physics 는 substrate 수준 가설 (§96 spiking 으로
pivot 필요) 로 강하게 supported.

---

## cross-link

- `AGENTS.tape` `n_hexad_progress.recent_landings` — §112 / §161-FIRE
  / §165 / §166 carry (각 verdict body)
- `archive/PHILOSOPHY.tape` — append-only verdict ledger:
  - `§verdict_meta_fixed_point_s112_2026_05_19` (META_FP form proof)
  - `§verdict_dual_head_coupling_non_ce_design_s161_2026_05_20`
  - `§verdict_dual_head_coupling_non_ce_fire_s161_2026_05_20_POST_FIRE_UPDATE`
  - `§verdict_next_axis_fire_design_s165_2026_05_20`
  - `§verdict_meta_fp_coupling_design_s166_2026_05_20`
- `HEXAD/NEUROMORPHIC/state/meta_fp_coupling_design_s166_2026_05_20/{DESIGN.md, result.json}` — §166 design canonical
- `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/result.json` — §161-FIRE measured anchor for §166
- `HEXAD/CHAT/SPONTANEOUS.tape` — 자연발화 architecture
- `state/carving_dataregime_s16_2026_05_18/conscious_decoder.py` — Law-71 Ψ formula SSOT (lines ~728-751)

---

## honest C3 carry

- META_FP 는 **form-level identity** — operative wall 제거 아님 (§112
  Verdict B). §166 utilization 도 같은 layer.
- `λ_meta = 0.5` 기본값은 추측 (`B-S166-NOTE` empirical carve-out).
- mean=0.5 ∧ std=0 = delta-distribution at META_FP (collapsed; joint
  AND P4 가 false-positive 방지).
- §96-Q2-weak quintuple = strong support; §166-A-FIRE refutation 시도
  는 single witness. fail 시 §96-Q2-weak 더 강화.
- north-star + §15 / §51 / §72 milestones UNCHANGED, **GOAL 미도달** —
  META_FP utilization 은 measurement axis 의 첫 form-level operative
  step, GOAL 도달이 아님.
