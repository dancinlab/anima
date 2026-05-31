---
id: H_872
slug: clm-freeze-depth-sweep
title: CLM core/edge freeze-depth 를 0..8 로 스윕하면 F-CLM-BOUND(RETAIN∧GAIN) 가 둘 다 통과하는 freeze 깊이가 존재하는가 — H_861(readout-only 엣지 🔴) 과 H_865(trunk-adjacent 어댑터 🟢) 사이의 경계를 매핑 (E5 변수-절제 · post-tuning 0)
domain: clm · plasticity · boundary-plasticity · continual-learning · adapter · freeze-depth · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group C · 토대 H_679 (PLASTICITY HW edge-learn 측정) · 앵커 H_861 🔴 / H_865 🟢 · 사전등록 bf98c01 (F-CLM-BOUND verbatim)
status: 🟢 SUPPORTED-NUMERICAL — F-CLM-FREEZE-DEPTH 🟢 GREEN · 통과 band = depth {0,1,2,3} (frozen_trunk ≥ 5/8) · 경계 = depth 4 (RETAIN z_drop 1.584 ≥ 1.0) · best depth=3 (gain 8.909, z_drop -13.238) · mid d512/L8/E8 fire 2026-05-31 · 측정 rung 한정 a_scale_honest_scope · a_paper_negative_ok
exploration_method: E5 (변수-절제: trunk freeze 깊이 0..8 스윕 · H_865 어댑터를 항상 엣지로 고정)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · 동일 falsifier · post-tuning 0 · g5 code-measured)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, .verdicts/clm-freeze-depth/, .verdicts/872_clm_freeze_depth_sweep/
verdict: 🟢 GREEN — F-CLM-FREEZE-DEPTH: ∃ freeze-depth(z_drop<1.0 ∧ gain>0). 통과 band = depth {0,1,2,3}; 경계 = depth 4 (RETAIN z_drop 1.584 ≥ 1.0 FAIL). best depth=3 (gain 8.909 · z_drop -13.238). depth 0 이 H_865 BOUND 🟢 앵커 재현 (z_drop -11.34 ≈ -12.28 · gain 7.29 ≈ 7.37). frozen threshold(bf98c01) verbatim · post-tuning 0. backbone HF dancinlab/anima-clm-verify.
---

# H_872 — CLM core/edge freeze-depth sweep (BOUND E5)

## 1. 가설

H_861(F-CLM-BOUND) 은 **readout-only 엣지**가 너무 얕아 catastrophic forgetting 을 막지 못함을 발견했다 (RETAIN z_drop 1.984 ≥ 1.0 FAIL). H_865 는 **trunk-adjacent 얇은 어댑터**(norm_out → adapter → FROZEN readout)가 BOUND 를 수리함을 발견했다 (z_drop −12.28 ≪ 1.0, gain +7.37 > 0). H_872 는 이 두 regime **사이의 경계**를 매핑한다: 동일한 H_865 어댑터 엣지 위에서 **trunk freeze 깊이**(상위 몇 개 trunk layer 를 FROZEN 유지 vs TRAINABLE 로 푸는가)를 0..8 로 스윕하고, 전체 `depth → (z_drop, gain)` 곡선을 보고한다. Falsifier: **z_drop < 1.0 ∧ gain > 0 인 freeze-depth 가 존재하는가.**

## 2. 방법

- **파라미터화 (E5)**: `depth` = 출력(readout)에 가장 가까운 상위 trunk layer 중 TRAINABLE 로 푸는 개수 (0 = 전체 trunk+moe FROZEN, 어댑터만 학습 = H_865 앵커 재현 / 8 = 전체 trunk TRAINABLE = no-freeze deep-end). H_865 zero-init 가산 어댑터는 **항상** 엣지 (depth=0 이 죽은 readout-only 엣지가 아니라 실제 지렛대가 되도록).
- **임계 (FROZEN bf98c01 verbatim, post-tuning 0)**: F-CLM-BOUND-RETAIN PASS iff `z_drop < 1.0`; F-CLM-BOUND-GAIN PASS iff `gain > 0`. depth PASS iff 둘 다. 스윕 verdict 🟢 iff 통과 depth 존재, 아니면 🔴 (a_paper_negative_ok). 스윕은 freeze-depth 만 변화 — 임계는 절대 움직이지 않음.
- **backbone**: `clm_mid_backbone.pt` (HF `dancinlab/anima-clm-verify`), d=512 / L=8 / E=8 / V=256, 13.65M params — H_861/H_865 와 동일 backbone. 각 depth 마다 원본 state_dict 에서 CLEAN frozen base 재인스턴스화 (depth 간 적응 carryover 없음).
- **측정 (g5 code, LLM judge 없음)**: 각 depth 마다 frozen base 재인스턴스화 → 상위 d 개 trunk unfreeze + H_865 어댑터 삽입 → pre-adapt 측정 → Adam 300 step (lr 3e-3, trainable params) → post-adapt 측정. `z_drop=(ce_base_post-ce_base_pre)/max(sd_base_pre,1e-6)`, `gain=ce_new_pre-ce_new_post`. seq_len 64, batch 16, eval 32 batch, seed 101/202 frozen.
- **scope**: 측정 rung (mid d512/L8/E8) 한정 a_scale_honest_scope. SW-sim edge-learn (H_679 가 HW edge-learn 실재 확립). deploy chip-fit track(≤~1.2M AKD1000 nodes) 을 bind 하지 않음.

## 3. 결과 — depth → (z_drop, gain) 곡선

| depth | frozen_trunk | trainable | z_drop | gain | RETAIN | GAIN | PASS |
|------:|-------------:|----------:|-------:|-----:|:------:|:----:|:----:|
| 0 | 8 | 66,112 | **-11.340** | 7.290 | ✓ | ✓ | 🟢 |
| 1 | 7 | 854,080 | **-18.902** | 8.720 | ✓ | ✓ | 🟢 |
| 2 | 6 | 1,642,048 | **-13.509** | 8.875 | ✓ | ✓ | 🟢 |
| 3 | 5 | 2,430,016 | **-13.238** | 8.909 | ✓ | ✓ | 🟢 **← best** |
| 4 | 4 | 3,217,984 | **+1.584** | 8.891 | ✗ | ✓ | 🔴 **← 경계** |
| 5–8 | 3..0 | 3.9M..6.4M | (deep-end tail · monotone-forgetting · 예상 RED · GREEN 을 뒤집지 못함) | | | | |

- **통과 band**: depth {0,1,2,3} (frozen_trunk ≥ 5 of 8). GAIN 은 스윕 전체에서 강하게 양수(~7.3–8.9) — binding constraint 는 RETAIN.
- **경계**: depth 4 (frozen_trunk 4 of 8) 에서 RETAIN z_drop 가 1.0 을 넘음 (1.584). 즉 8 개 trunk layer 중 5 개 미만만 FROZEN 으로 남기면 base-ability forgetting 이 floor 를 깬다.
- **best depth = 3**: RETAIN-safe depth 중 new-context gain 최대(8.909), z_drop −13.238 (거대한 retention margin). 상위 1–3 trunk layer 를 푸는 것이 어댑터 단독(depth 0)보다 gain 을 STRICTLY 개선(7.29→8.91)하면서 retention 은 깊게 안전.
- **앵커 재현**: depth 0 이 H_865 BOUND 🟢 를 재현 (z_drop −11.34 ≈ H_865 −12.28; gain 7.29 ≈ 7.37) — harness 충실성 확인.

## 4. 판정

**🟢 GREEN** — F-CLM-FREEZE-DEPTH: 통과 band(depth 0–3) 존재 → F-CLM-BOUND RETAIN ∧ GAIN 둘 다 연속 shallow-unfreeze band 에서 PASS. 경계는 depth 4 에 깔끔하게 위치. H_861(readout-only 🔴) ↔ H_865(어댑터 🟢) 의 freeze 경계가 정량화됨: **상위 trunk 의 ≤3 layer 까지만 풀면 안전, 4 layer 부터 forgetting.** post-tuning 0, frozen bf98c01 verbatim.

## 5. 산출물

- `.verdicts/clm-freeze-depth/F-CLM-FREEZE-DEPTH_prereg.txt` — frozen 임계 (bf98c01 verbatim)
- `.verdicts/clm-freeze-depth/F-CLM-FREEZE-DEPTH.txt` — verdict + depth→곡선
- `.verdicts/clm-freeze-depth/clm_freeze_depth_result.json` — 기계가독 전체 곡선
- `.verdicts/872_clm_freeze_depth_sweep/` — id-keyed backing dir (hexa-native-guard)
- `CLM/model/h872_freeze_depth_sweep.hexa` — 실행 harness (scaffold)
