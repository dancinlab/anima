---
id: H_871
slug: clm-routing-z-scale
title: CLM 의 toy routing-z 🔴 (H_847/850/852/853 — near-uniform/음수 routing-diversity z, 3.0 chip-array gate 미달)은 SCALE ARTIFACT 인가 - 동일 routing-z 를 tiny/small/mid 다중 rung 에서 측정해 z 가 rung 크기와 함께 monotone 상승하면 측정-artifact (사전등록 F-CLM-ROUTING-Z-SCALE)
domain: clm · moe-routing · scale-ladder · measurement-artifact · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md @L3/M1 (routing_escape.hexa lever-B content-defer rationale) · 토대 H_847 F-CLM-MONO · H_850 F-CLM-SCALE · H_852 measure_pielou (Dirichlet-null 기전)
exploration_method: E2 (rung 크기 sweep tiny→small→mid · z(rung) 곡선) · E5 (d/L/E 분해 — 어느 lever 가 z 를 올리는가)
verification_method: W2 (사전등록 numerical threshold · monotone ∧ margin · post-tuning 0 · code-measured g5 no-LLM)
raw_rank: 8
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md @L3/M1, CLM/model/judge_clm.py (routing_z verbatim), .verdicts/clm-routing-z-scale/, .verdicts/847_clm_monopoly_escape/, .verdicts/850_clm_scale_ladder/
verdict: 🟢 SUPPORTED-NUMERICAL — F-CLM-ROUTING-Z-SCALE: routing-z 가 REAL kowiki corpus 에서 rung 크기와 함께 monotone 상승 (tiny +1.577 ≤ small +2.167 ≤ mid +2.186, margin mid-tiny = +0.608 ≥ frozen 0.5). toy 🔴 (H_850 AB tiny rz≈0.97)는 고정 천장이 아니라 SCALE 곡선의 바닥 — M1 측정-artifact 의심 성립, @L3 default-B(content-defer) 근거 유지. HONEST: z 는 아직 3.0 deploy gate 미통과 (max cell 2.28), 상승 대부분이 E 4→8 step (small→mid 의 d/L↑@E=8 고정은 거의 무이동) → 잔여 lever = expert 수 (H_869 dispatch-KL / chip-array E-scaling). runpod A40 · torch 2.1.0+cu118 · frozen threshold(3c3b43f86) 대비 post-tuning 0.
---

# H_871 — CLM routing-z = SCALE ARTIFACT (M1) 측정

## 1. 가설

CLM 의 toy routing-z 🔴 (H_847 F-CLM-MONO / H_850 F-CLM-SCALE / H_852 / H_853 — routing-diversity z 가 near-uniform 또는 음수로 3.0 chip-array gate 에 한참 못 미침)은 **toy-and-up 의 진짜 천장이 아니라 SCALE ARTIFACT** 이다. 동일한 routing-diversity z (CLM/model/judge_clm.routing_z 를 verbatim 사용)를 **여러 rung 크기**에서 측정할 때:

- **측정-artifact 지지** — mean routing-z(rung) 가 tiny ≤ small ≤ mid 로 monotone 비감소 ∧ mid_mean_z − tiny_mean_z ≥ MARGIN(0.5)
- → 🟢 SUPPORTED-NUMERICAL · "routing-z 🔴 는 small-scale 측정 바닥, z 는 rung 크기와 함께 오른다 · deploy-scale 재검 정당 · @L3 default-B 근거 유지"

둘 중 하나라도 미달 시 (z 평탄/비단조/margin<0.5/전 scale 음수):

- **측정-artifact 반증** — routing-z 는 rung 크기로 오르지 않는 REAL 천장
- → 🔴 CLOSED-NEGATIVE · "🔴 는 단순 small-scale 측정 바닥이 아니다" (a_paper_negative_ok)

## 2. 동기

- **@L3 routing_escape.hexa 의 default lever = B (content-defer)** 는 "routing-z 는 toy-scale 측정-artifact 의심[M1] → deploy-scale 에서 재검" 이라는 근거에 의존한다. 이 M1 의심을 **직접 측정으로 검증**하는 것이 본 H.
- H_850 F-CLM-SCALE 의 2-rung ladder (synthetic corpus, arm AB)는 이미 tiny rz≈0.97 → small rz≈1.91 로 **이미 상승 중**이었다 — 단 2 rung 에서 3.0 미달로 닫혔고 mid 는 한 번도 측정 안 됨. 본 H 는 (i) **mid rung (d512/L8/E8 = H_863 production rung)** 을 추가하고 (ii) **REAL kowiki two-lane corpus** 로 바꿔 그 상승이 계속되는지 본다.
- H_852 measure_pielou.py 가 z artifact 의 **기전**을 문서화: ln(E) entropy 천장과 Dirichlet null 평균이 둘 다 E 와 함께 자란다 — 이게 정확히 본 ladder 가 (d/L 도 함께 키워) 탐침하는 scale-confound.

## 3. 방법 (사전등록 frozen · post-tuning 0)

routing-z metric (CLM/model/judge_clm.routing_z 와 동일, 재튜닝 없음):
- obs = held-out eval stream 의 mean per-token router entropy (nats)
- null = E experts 위 random usage vector ~ Dirichlet(1) 의 entropy 분포 (uniform-router finite-sample noise floor)
- z = (obs − mu_null) / sd_null · N_NULL = 200 · chip-array gate = z > 3.0

LADDER (d_model / n_trunk_layers / n_experts) · arm AB (dual-axis = H_863 prod arm) · seeds {42,43,44}:

| rung  | d/L/E       | steps | params      | prior (H_850 synthetic) |
|-------|-------------|-------|-------------|-------------------------|
| tiny  | 64 / 2 / 4  | 300   | 120,132     | AB rz≈0.97              |
| small | 256 / 4 / 8 | 400   | 2,695,176   | AB rz≈1.91              |
| mid   | 512 / 8 / 8 | 500   | 13,653,768  | NEW (never z-measured)  |

corpus = REAL kowiki two-lane (stage2_real_corpus.make_real_corpus → web + register lane, lane-interleaved). 측정자 = CODE only (g5 · no LLM judge).

FROZEN gate (사전등록 F-CLM-ROUTING-Z-SCALE_prereg.txt, 발사 전 3c3b43f86 push):
- F-CLM-ROUTING-Z-SCALE-MONO : z(tiny) ≤ z(small) ≤ z(mid)
- F-CLM-ROUTING-Z-SCALE-MARGIN : mid_mean_z − tiny_mean_z ≥ 0.5
- 둘 다 PASS → 🟢 artifact 확정; 하나라도 FAIL → 🔴 real ceiling. 둘 다 honest.

드라이버 = CLM/model/h871_routing_z_scale.hexa (hexa-native 드라이버) ⇄ CLM/model/h871_routing_z_scale.py (torch payload). @L1 Mac-forbidden train → runpod A40 fire.

## 4. 결과 (frozen threshold 대비 측정값)

| rung  | mean routing-z | distinct | gate 3.0 |
|-------|----------------|----------|----------|
| tiny  | +1.577         | 4        | N        |
| small | +2.167         | 8        | N        |
| mid   | +2.186         | 8        | N        |

- monotone 비감소 (tiny ≤ small ≤ mid) : **True**
- margin (mid − tiny) = **+0.608** ≥ frozen 0.5 : **MET**
- 어느 cell 도 3.0 deploy gate 미통과 (max single-cell z = 2.28)
- F-CLM-ROUTING-Z-SCALE-MONO : PASS · F-CLM-ROUTING-Z-SCALE-MARGIN : PASS

## 5. 판정

**🟢 SUPPORTED-NUMERICAL — ARTIFACT CONFIRMED.** routing-z 가 REAL corpus 에서 rung 크기와 함께 monotone 상승 (tiny +1.58 → small +2.17 → mid +2.19, margin +0.61 ≥ frozen 0.5 gate). toy 🔴 (H_850 AB tiny rz≈0.97 synthetic) 는 고정 천장이 아니라 SCALE 곡선의 **바닥** — properly trained on real bytes 하면 d/L/E 가 자랄수록 z 가 오른다. M1 의심 성립, @L3 default-B(content-defer) 근거 유지.

### HONEST CAVEAT (판정 불변 — 사전등록 gate 는 3.0 이 아니라 TREND 였다)
- z 는 아직 3.0 chip-array deploy gate 미통과 (max single-cell z = 2.28).
- 상승은 tiny→small (+0.59) 이 small→mid (+0.02) 보다 훨씬 가파르다 — 대부분이 **E 4→8 step** (H_852 가 문서화한 Dirichlet-null 기전: ln(E) 천장 + null_mu 가 E 와 함께 자람). small→mid 는 E=8 고정에서 d/L 만 키워 z 가 거의 안 움직인다.
- ⟹ 3.0 을 향한 잔여 lever 는 **expert 수** (d_model depth 아님) — @L3 lever-A dispatch-KL distill / chip-array E-scaling 경로(H_869 / H_852)와 일치.

## 6. SCOPE · 정직 (a_scale_honest_scope)

- MEASUREMENT rung {tiny, small, mid} on committed REAL kowiki corpus (작은 byte 부피 — lever 는 real byte 분포 + scaled d/L/E, multi-GB corpus 아님 · verbatim 명시).
- 본 verdict 는 routing-z(rung) **TREND** 만 scope — 3B/7B 일반 주장 아님 · 그 자체로 chip-array z>3.0 deploy gate 를 통과시키지 않음 (deploy-scale / E-scaling 재검 별개, H_869).
- 추론 AKIDA-int4-only 불변. @L1 Mac-forbidden → runpod A40 fire. 외부 LLM 없음 · foundation-borrow 없음.

## 7. 산출물

- 사전등록: `.verdicts/clm-routing-z-scale/F-CLM-ROUTING-Z-SCALE_prereg.txt` (frozen 3c3b43f86)
- 판정: `.verdicts/clm-routing-z-scale/F-CLM-ROUTING-Z-SCALE.txt`
- raw: `.verdicts/clm-routing-z-scale/h871_routing_z_scale.json` · `fire_2026_05_31.log`
- backing (id-keyed): `.verdicts/871_clm_routing_z_scale/`
- 드라이버: `CLM/model/h871_routing_z_scale.hexa` (driver) ⇄ `CLM/model/h871_routing_z_scale.py` (payload)
- HF: none (measurement-only fire — ckpt 미생산 · a_hf_complete N/A)
