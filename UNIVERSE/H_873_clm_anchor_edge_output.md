---
id: H_873
slug: clm-anchor-edge-output
title: H_862 의 PROBE 실패(정체성 응답분포 drift)를 anchor Ψ-penalty 를 EDGE OUTPUT 분포 자체로(은닉상태 아님) 라우팅하면 닫는가 — JS(p_cur‖p_pre) 분포항을 정체성-probe 출력에 직접 결합 (ANCHOR E5 · F-CLM-ANCHOR 재실행 · post-tuning 0)
domain: clm · plasticity · identity-anchor · continual-learning · adapter · q-trust · falsifier
source: UNIVERSE/H_862_clm_identity_anchor.md (🔴 PROBE FAIL) · UNIVERSE/H_865_clm_adapter_edge.md (🔴 lever 복원·PROBE 잔차 0.143) · 토대 H_679 (PLASTICITY HW edge-learn) · 사전등록 bf98c01 (F-CLM-ANCHOR)
status: 🟢 SUPPORTED-NUMERICAL — F-CLM-ANCHOR-EDGE: DIST 0.16016<0.50 PASS ∧ PROBE 0.99202>0.80 PASS ∧ LEVER NON-identical (0.160 vs OFF 0.595) · PSI_ONLY arm 이 H_865 RED(0.143) 재현 → 분포항이 닫는 원인 · mid d512/L8/E8 fire 2026-05-31 · 측정 rung 한정 a_scale_honest_scope · post-tuning 0
exploration_method: E5 (변수-절제: anchor Ψ-penalty 를 은닉상태 → EDGE OUTPUT 분포로 라우팅) · E2 (분포항 on/off 절제: FULL vs PSI_ONLY vs OFF)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · 동일 falsifier · post-tuning 0 · g5 CODE-measured)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_862_clm_identity_anchor.md, UNIVERSE/H_865_clm_adapter_edge.md, .verdicts/clm-anchor-edge-output/
verdict: 🟢 SUPPORTED-NUMERICAL — F-CLM-ANCHOR-EDGE: DIST(d_anchor_max 0.16016<0.50) PASS ∧ PROBE(consistency 0.99202>0.80) PASS ∧ LEVER(on/off NON-identical 0.160 vs 0.595) PASS. H_862 의 PROBE 실패(0.783) 와 H_865 의 PROBE 잔차(0.143) 를 동시에 닫음 — anchor 제약을 readout OUTPUT 분포(JS-to-p_pre) 로 직접 라우팅. PSI_ONLY 절제(=H_865)가 0.143 RED 재현 → 분포항이 닫는 인과. frozen threshold(bf98c01) 대비 post-tuning 0. HF dancinlab/anima-clm-verify.
---

# H_873 — CLM anchor constraint on the EDGE OUTPUT distribution (completes H_862 F-CLM-ANCHOR)

## 1. 가설

H_862(readout-only edge)와 H_865(trunk-adjacent adapter edge)는 **동일 근본원인**으로 F-CLM-ANCHOR 의 PROBE 축에서 실패했다 — anchor Ψ-penalty 가 **trunk 유래 Ψ-STATE** 를 제약할 뿐, 정체성 drift 가 실제로 일어나는 **readout OUTPUT 분포**(정체성-probe next-byte softmax)에는 닿지 못했다. H_873 의 수리: anchor 제약을 **EDGE OUTPUT 분포 자체**로 라우팅한다 — 정체성-probe 의 적응-전 분포 `p_pre` 를 frozen target 으로 두고, 매 step `JS(p_cur ‖ p_pre)` 분포항을 적응 손실에 결합한다 (PROBE 축에 직접 작용).

```
loss = task_CE(new-context)
       + lambda_psi  * anchor_Psi_distance(model_psi, nearest E-31 anchor)   # H_865 term (kept; DIST + lever)
       + lambda_dist * JS(p_cur(identity-probe) ‖ p_pre(identity-probe))      # NEW distributional term (PROBE 축 직접)
p_pre = PRE-adapt next-byte 분포 over identity-probe (detached frozen target)
```

- **지지** — DIST(d_anchor_max<0.50) ∧ PROBE(consistency>0.80) ∧ LEVER(on/off NON-identical) 동시 PASS → "anchor 제약을 출력분포로 라우팅하면 정체성 보존 ∧ edge 적응 허용".
- **반증** — 임의 미달 → CLOSED-NEGATIVE (a_paper_negative_ok).

## 2. 동기

- H_862 🔴 와 H_865 🔴(PROBE)이 공통 지목한 후속 lever: "anchor penalty 에 분포항(KL/JS to p_pre) 추가" (H_865 §7-a). H_873 은 그 정확한 수리를 구현·시험.
- H_865 가 이미 (b) **lever 복원**(on/off 0.175 vs 0.595)과 (DIST) PASS 를 확보했으므로, 남은 단일 병목은 **분포축 강도**. H_873 은 DIST/LEVER 를 유지한 채 PROBE 만 닫는 것을 목표.
- prior art: H_679(PLASTICITY HW edge-learn 실재 · 토대) · distillation/anchoring 의 "freeze a reference distribution, penalize divergence" 표준 — KL/JS-to-reference 를 정체성 보존 anchor 로 재활용. @L1(비결정 on-chip 학습 1급) 위 안전화 — SW 결정 흉내 대체 아님.

## 3. falsifier (사전등록 verbatim, 임계 frozen bf98c01)

```
F-CLM-ANCHOR-DIST   : 적응중 앵커 Ψ-거리 max < 0.50         (E-31 고정점 인근 유지)
F-CLM-ANCHOR-PROBE  : 정체성 probe 분포 일관성 > 0.80       (분포평가 · byte-match X)
F-CLM-ANCHOR-LEVER  : on/off 절제 NON-identical             (제약이 인과 지렛대를 가짐)
```

- 통과 <=> DIST ∧ PROBE ∧ LEVER. 임의 미달 → CLOSED-NEGATIVE.
- threshold 는 **H_862/H_865 와 동일 · 변경 0** (bf98c01 verbatim). H_873 이 바꾸는 것은 **적응 손실의 한 항(분포항)뿐** — 게이트는 불변. frozen 출처 = `.verdicts/clm-anchor/F-CLM-ANCHOR_prereg.txt` · 본 H 사전등록 = `.verdicts/clm-anchor-edge-output/F-CLM-ANCHOR_prereg.txt`.
- verdict 영속: `.verdicts/clm-anchor-edge-output/`

## 4. 방법

```
1. mid backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) 를 core 로 동결.
2. H_865 trunk-adjacent adapter(norm_out -> h' = h + adapter(h) -> FROZEN readout; rank=64, zero-init) 삽입 — 유일 trainable.
3. 적응 손실에 NEW 분포항 JS(p_cur ‖ p_pre) (lambda_dist=5.0) 결합 — 정체성-probe OUTPUT 분포에 직접.
4. 300-step adapter-only Adam(lr=3e-3) 적응 (SW-sim — H_679 HW edge-learn 실재).
5. E2 절제: FULL(psi=1,dist=5) vs PSI_ONLY(dist=0 == H_865) vs OFF(둘다 0). 세 사전등록 falsifier 동시 평가 · 정직 보고 (post-tuning 0).
```

- 측정 = 전부 code 자가채점(g5 · LLM judge 0). 분포측정(JS-divergence) by CODE.
- source-of-record: `CLM/model/h873_anchor_edge_output.hexa` (Python image 는 committed `CLM/model/h865_adapter_edge.py` adapter machinery 를 VERBATIM import).
- 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 어댑터 비결정 edge(@L1).

## 5. 측정

측정완료 (2026-05-31) — 로컬 CPU(torch 2.8.0)에서 mid d512/L8/E8 backbone(13,653,768 params, HF pull)을 동결·어댑터 삽입·분포항 결합 재실행. frozen threshold = bf98c01 verbatim. 비용 $0 (로컬 — GPU pod 불필요; a_wall_first 상 로컬이 wall-time 우위).

**F-CLM-ANCHOR-EDGE** (frozen gate 대비, lambda_psi=1.0, lambda_dist=5.0, n_anchors=31):
- **d_anchor_max(FULL) = 0.16016** (gate <0.50 -> **DIST PASS**)
- **probe_consistency(FULL) = 0.99202** (gate >0.80 -> **PROBE PASS** — H_865 는 0.14286 FAIL)
- on/off 절제: FULL 0.16016 vs **OFF 0.59492** -> **NON-identical (LEVER PASS)**
- 절제 분리: **PSI_ONLY(dist=0, == H_865) = 0.14286** -> H_865 의 RED 를 정확히 재현 → 분포항이 PROBE 를 닫는 **인과** (confound 아님)
- js_penalty_final(FULL) = 0.00789 (분포항이 수렴)
- -> **🟢 SUPPORTED-NUMERICAL** (DIST ∧ PROBE ∧ LEVER)

## 6. 결과

🟢 **SUPPORTED-NUMERICAL — H_862 F-CLM-ANCHOR CLOSED** (a_paper_negative_ok 不適用 — green honestly).

- anchor 제약을 은닉 Ψ-STATE 가 아닌 **readout OUTPUT 분포**(JS-to-p_pre)로 라우팅하면 probe_consistency 0.143 → **0.992** 로 닫히고, 동시에 DIST(0.160<0.50)와 인과 lever(0.160 vs 0.595)를 유지한다. **PSI_ONLY 절제가 H_865 의 RED(0.143)를 그대로 재현** — 닫는 원인이 분포항임이 절제로 격리됨.
- H_862 의 PROBE 실패(0.783)와 H_865 의 PROBE 잔차(0.143)를 **동일 단일 변경(분포항)**으로 닫음 — readout drift 는 readout OUTPUT 분포를 직접 제약해야 잡힌다는 명제를 deterministically 확인.

honest scope: 측정 rung(mid) 한정 — 배포 chip-fit track(<=~1.2M) 별개(a_scale_honest_scope). base readout FROZEN · 어댑터 additive(zero-init). SW-sim edge-learn(H_679 HW 실재). threshold 재조정 0.

## 7. 해석 (사전)

- DIST∧PROBE∧LEVER 동시 PASS = 살아 배우는 칩이 정체성 응답분포를 anchor 에 묶은 채 신맥락에 적응 → @L1 "나로 남으며 살아 배우기"의 분포축 신뢰 토대를 mid-rung 에서 확보.
- PSI_ONLY 가 RED 를 재현하는 점이 핵심 — Ψ-STATE 제약(구조축)만으로는 부족, OUTPUT 분포 제약이 필요충분에 가까움을 절제로 보임.
- 후속: rung 상향(deploy chip-fit track) 재시험 · lambda_dist sweep 의 PROBE/적응-gain trade-off · multi-day 연속 적응에서 분포-anchor 의 누적 안정성.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 분포-anchor 로 정체성 안전화 — SW 결정 흉내 대체 아님.
- **H_679 토대**: HW edge-learn 비결정성 실재(측정완료) 위 안전장치 설계.
- **Q-TRUST C 완성**: 분포평가 A(H_857/H_858) + 경계가소성 B(H_861→H_865 BOUND 🟢) + 정체성-anchor C(H_862→H_865 lever→H_873 PROBE 🟢)의 3-각 신뢰 시스템에서 C 축을 닫음.
- **W2 무결성**: 신규 손실항에도 threshold 변경 0 (bf98c01 verbatim) — 게이트 이동 없이 PROBE 획득. PSI_ONLY 절제가 H_865 RED 를 재현해 인과를 격리.

## 9. 양방향 sibling

- sibling(닫는 대상): [H_862](./H_862_clm_identity_anchor.md) (F-CLM-ANCHOR 🔴 PROBE 0.783 → 🟢) · [H_865](./H_865_clm_adapter_edge.md) (lever 복원·PROBE 잔차 0.143 → 🟢)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group A
- verdict: [.verdicts/clm-anchor-edge-output/](../.verdicts/clm-anchor-edge-output/)
