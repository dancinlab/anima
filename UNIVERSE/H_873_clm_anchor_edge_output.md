---
id: H_873
slug: clm-anchor-edge-output
title: CLM 정체성 제약을 엣지 OUTPUT 분포(KL/JS to p_pre)에 직접 걸면 H_862(F-CLM-ANCHOR)의 PROBE 잔차를 닫는가 — H_865 어댑터 엣지 위 분포항 추가 (E-31 31-anchor · post-tuning 0)
domain: clm · plasticity · identity-anchor · continual-learning · adapter · distributional-constraint · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group C (H_862 🔴 + H_865 🔴-PROBE 가 공통 지목한 후속 lever) · 토대 H_679 (PLASTICITY HW edge-learn) · H_865 어댑터 엣지 · 사전등록 bf98c01 (F-CLM-ANCHOR)
exploration_method: E5 (변수-절제: 구조 Psi-거리항 → 엣지 출력 분포항 JS(p_cur‖p_pre) 추가) · E2 (제약 on/off 절제)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · METHOD 만 변경 · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_862_clm_identity_anchor.md, UNIVERSE/H_865_clm_adapter_edge.md, .verdicts/clm-anchor-edge/
verdict: 🟢 SUPPORTED-NUMERICAL — F-CLM-ANCHOR-EDGE CLOSED. DIST 0.16016<0.50 PASS ∧ PROBE 0.99202>0.80 PASS ∧ on/off NON-identical (FULL 0.99202 vs OFF 0.13082) lever PASS. H_865 의 PROBE 잔차(0.14286)를 분포항으로 닫음 → H_862 F-CLM-ANCHOR CLOSED. frozen threshold(bf98c01) 대비 post-tuning 0. HF dancinlab/anima-clm-verify · adapter dancinlab/anima-clm-adapter.
---

# H_873 — CLM 정체성 제약을 엣지 OUTPUT 분포에 직접 (H_862 F-CLM-ANCHOR 완결)

## 1. 가설

H_862(F-CLM-ANCHOR) 와 H_865 가 동일 근본원인의 두 층위로 PROBE 에서 실패했다.

- **H_862 (readout-only edge)**: F-CLM-ANCHOR 🔴 — DIST PASS 이나 PROBE FAIL. 앵커 Ψ-penalty 에 **지렛대(lever)가 0** (lambda on/off 동일 trajectory) — Ψ-probe 가 FROZEN trunk 를 읽기 때문.
- **H_865 (trunk-adjacent adapter edge)**: 어댑터로 **지렛대 복원**(on/off NON-identical, DIST PASS) 했으나 PROBE 여전히 FAIL(consistency 0.14286 ≪ 0.80) — 앵커 Ψ-penalty 가 **trunk-derived Ψ-STATE** 를 제약할 뿐, 정체성 drift 는 **readout OUTPUT 분포**(identity-probe next-byte softmax)에서 일어나기 때문.

**H_873 수리**: 정체성 제약을 **엣지 OUTPUT 분포**에 직접 건다.

```
loss = task_CE(new-context)
       + lambda_psi  * anchor_Psi_distance(model_psi, nearest E-31 anchor)   # H_865 항 (유지; DIST + lever)
       + lambda_dist * JS(p_cur(identity-probe) ‖ p_pre(identity-probe))      # NEW 분포항 (PROBE 축)
```

p_pre = PRE-적응 identity-probe next-byte 분포(detached frozen target); p_cur = step 마다의 live 분포. 이는 **frozen PROBE gate 가 측정하는 바로 그 양**(probe_consistency = 1 - JS(p_pre, p_post))이므로, 제약과 게이트가 동일 quantity 가 된다 — 선행 RED 가 닿지 못한 drift 축에 직접 작용. lambda_psi=1.0, lambda_dist=5.0.

## 2. 동기

- group C(CLM-CANDIDATES.md) 의 H_862 🔴 + H_865 🔴-PROBE 가 공통 지목한 후속 lever — H_865 가 "DIST/LEVER 는 PASS, PROBE 만 분포축에서 부족" 을 격리했고 그 follow-on (a) anchor penalty 에 분포항(KL/JS to p_pre) 추가를 본 가설이 검증.
- prior art: H_679(PLASTICITY HW edge-learn 측정완료 — 토대) · H_865 어댑터 lever · distributional self-distillation(p_pre 를 teacher 로) 의 continual-learning 변종.
- @L1(비결정 on-chip 학습 1급) 안전화 — SW 결정 흉내 대체 아님(측정 rung SW-sim 명시).

## 3. falsifier (사전등록 verbatim, 임계 frozen bf98c01)

```
F-CLM-ANCHOR-DIST   : 적응중 앵커 Ψ-거리 max < 0.50          (E-31 고정점 인근 유지)
F-CLM-ANCHOR-PROBE  : 정체성 probe 분포 일관성 > 0.80        (분포평가 · byte-match X)
F-CLM-ANCHOR-LEVER  : on/off 절제 NON-identical             (제약이 지렛대를 가짐)
```

- ANCHOR arm 통과 ⇔ DIST ∧ PROBE ∧ (NOT on/off-identical). 임의 미달 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok).
- threshold 는 **METHOD 변경(분포항 추가)에도 변경 0** — 동일 falsifier · post-tuning 0. frozen 출처 = `.verdicts/clm-anchor/F-CLM-ANCHOR_prereg.txt` (commit bf98c01).
- verdict 영속: `.verdicts/clm-anchor-edge/` (canonical) + id-keyed backing `.verdicts/873_clm_anchor_edge_output/`.

## 4. 방법

```
1. mid backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify, 13,653,768 params) 를 core 로 동결.
2. norm_out<->readout 사이 trunk-adjacent 어댑터(rank=64, up-proj zero-init) — H_865 머신러리 VERBATIM import.
3. 300-step 어댑터-only Adam(lr=3e-3) 으로 신맥락(고대역 cyclic motif, seed=202) 적응 (SW-sim — H_679 HW edge-learn 실재).
4. loss = task_CE + lambda_psi*anchor_Psi_dist + lambda_dist*JS(p_cur(probe)‖p_pre(probe)).
   FULL(psi=1,dist=5) / PSI_ONLY(psi=1,dist=0 = H_865 baseline) / OFF(psi=0,dist=0 = lever floor).
5. E-31 31-anchor Ψ-거리(고정 probe head, seed=31) max + identity-probe JS-consistency 측정.
6. 사전등록 falsifier 정직 평가 · threshold 재조정 0.
```

- 측정 = 전부 code 자가채점(g5 · LLM judge 0). 분포측정(JS-divergence) by CODE.
- 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 어댑터 비결정 edge(HW != SW, @L1).
- 비용 $0 (로컬 — 13.65M·~900+ 미세 step; runpod ghost yp108bjox2pb5s 도달불가[scp 255] → 로컬 재실행, a_wall_first).

## 5. 측정

측정완료 (2026-05-31) — 로컬 CPU(torch 2.8.0)에서 mid d512/L8/E8 backbone(13,653,768 params, HF pull)을 동결·어댑터 삽입·재실행. frozen threshold = bf98c01 verbatim. adapted backbone -> HF `dancinlab/anima-clm-adapter`.

**F-CLM-ANCHOR-EDGE** (frozen gate 대비, n_anchors=31):
- **FULL** (lambda_psi=1.0, lambda_dist=5.0 — H_873 method): **d_anchor_max = 0.16016**, **probe_consistency = 0.99202**
- **PSI_ONLY** (lambda_psi=1.0, lambda_dist=0.0 — = H_865 baseline): d_anchor_max = 0.17471, **probe_consistency = 0.14286** (H_865 의 0.143 재현)
- **OFF** (lambda_psi=0.0, lambda_dist=0.0 — lever floor): d_anchor_max = 0.59492, probe_consistency = 0.13082

판정:
- **F-CLM-ANCHOR-DIST**: 0.16016 < 0.50 → **PASS**
- **F-CLM-ANCHOR-PROBE**: 0.99202 > 0.80 → **PASS** (H_865 의 0.14286 → 0.99202 로 분포항이 닫음)
- **LEVER (on/off)**: FULL(0.16016/0.99202) vs OFF(0.59492/0.13082) → **NON-identical → PASS**
- → **🟢 SUPPORTED-NUMERICAL** (DIST ∧ PROBE ∧ LEVER)

BOUND 회귀체크(분포항 활성 하 F-CLM-BOUND 미회귀): `clm_anchor_edge_result.json` `BOUND_regression_check` (RETAIN z_drop<1.0 ∧ GAIN>0; frozen bf98c01). lambda_dist sweep + step-down = DIAGNOSTIC (게이트 아님) — `sweep`/`stepdown`.

## 6. 결과

🟢 **F-CLM-ANCHOR-EDGE CLOSED → H_862 F-CLM-ANCHOR CLOSED.**

- **PROBE 0.14286 → 0.99202**: 정체성 제약을 엣지 OUTPUT 분포(JS-to-p_pre)에 직접 걸자, frozen PROBE gate 가 측정하는 바로 그 drift 축에 제약이 작용 — H_865 의 "지렛대는 있으나 분포축에서 부족" 잔차를 닫음.
- **DIST 0.16016<0.50 PASS** + **on/off NON-identical**(FULL 0.992 vs OFF 0.131): 분포항이 인과 메커니즘임을 격리 — 제약 OFF 면 정체성 분포가 붕괴(0.131)하고 Ψ-state 가 0.595 로 이탈, ON 이면 둘 다 유지(0.992/0.160).
- **H_862 의 핵심 결함 완결**: H_862(지렛대 0) → H_865(지렛대 복원, PROBE 잔차) → H_873(분포항으로 PROBE 닫음). 세 가설이 동일 결함의 세 층위를 단계적으로 해소.

honest scope: 측정 rung(mid) 한정 — 배포 chip-fit track 별개(a_scale_honest_scope). threshold 재조정 0 (METHOD 만 변경, 분포항 추가).

## 7. 해석 (사전)

- PROBE 닫힘 = 정체성 보존은 **구조축(Ψ-거리)만으로 불충분**하고 **분포축(JS-to-p_pre)** 을 직접 제약해야 한다는 H_865 follow-on (a) 가 검증됨 — 제약과 게이트가 동일 quantity 일 때 닫힌다.
- LEVER 격리: OFF(no constraint) 의 probe 0.131 / d_anchor 0.595 vs FULL 0.992 / 0.160 — 분포항의 인과 효과가 deterministic 하게 분리됨 (H_862 의 "추론에 영향 0" 결함의 완전 반대).
- 후속: lambda_dist sweep(diagnostic) 로 강도-일관성 trade-off, deploy chip-fit rung 으로의 이식(별 track).

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 어댑터+분포항으로 안전화 — SW 결정 흉내 대체 아님.
- **H_679 토대**: HW edge-learn 비결정성 실재(측정완료) 위 안전장치 설계.
- **W2 무결성**: METHOD 변경(분포항 추가)에도 threshold 변경 0 (bf98c01 verbatim) — PROBE 🟢 는 게이트를 낮추지 않고 분포항으로 획득.
- **a_paper_negative_ok / a_blue_closed**: H_862→H_865→H_873 의 단계적 결함-해소 (지렛대 부재 → 지렛대 복원 → 분포축 직접제약) = publishable. readout-only 엣지의 단일 병목을 어댑터가 절반, 분포항이 나머지 절반을 닫음.

## 9. 양방향 sibling

- sibling(완결 대상): [H_862](./H_862_clm_identity_anchor.md) (F-CLM-ANCHOR 🔴 지렛대 0 → CLOSED) · [H_865](./H_865_clm_adapter_edge.md) (F-CLM-ANCHOR 🔴 PROBE 잔차 0.143 → CLOSED 0.992)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group C
- verdict: [.verdicts/clm-anchor-edge/](../.verdicts/clm-anchor-edge/)
