---
id: H_878
slug: clm-mitosis-array
title: MITOSIS multi-chip array dispatch SW-sim — N-chip array partition/scatter/gather; aggregate-emit COHERENCE 🟢 (exact) ⨯ per-chip LOAD-BALANCE 🔴 (router monopoly) → F-CLM-MITOSIS-ARRAY 🔴 CLOSED-NEGATIVE (SW-sim · silicon NOT measured · 사전등록)
domain: clm · universe · neuromorphic-silicon · mitosis · moe-dispatch · load-balance · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group D row H_878 · H_852 expert-COUNT scale axis (DISSOLVE 🔴) · CLM/P4_PRODUCTION_ROADMAP.md @L2 MITOSIS (expert=chip array deploy vision)
status: 🔴 CLOSED-NEGATIVE (SW-sim · 2026-05-31 · aggregate-emit coherence EXACT(logit/argmax/CE = 0 over N∈{2,4,8}) ⨯ per-chip load-balance FAIL(max/min dispatch ratio 1.88→28.8→54.5 vs bound 4.0) · 측정 SW-sim 한정 silicon 미측정 a_scale_honest_scope)
exploration_method: E14 (deploy track substrate-native ⨯ MoE dispatch cross-domain 배선) · E5 (H_852 expert-count axis → deploy partition rung 확장)
verification_method: W2 (사전등록 load-balance ratio bound ∧ coherence tolerance frozen BEFORE run · code-measured g5 · post-tuning 0 · a_paper_negative_ok)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: H_852 (expert-COUNT DISSOLVE 🔴), H_851 (mitosis growth), CLM/P4_PRODUCTION_ROADMAP.md @L2, .verdicts/clm-mitosis-array-sim/
verdict: 🔴 CLOSED-NEGATIVE — N-chip array dispatch SW-sim. aggregate-emit COHERENCE 통과(distributed partition→per-chip emit→gather 가 single-model reference 와 EXACT: max|logit| diff = 0, argmax hamming = 0, |CE| delta = 0, 전 N∈{2,4,8}) — SW scatter/gather contract 정확. 그러나 per-chip LOAD-BALANCE 실패: 학습된 router 가 소수 expert 를 독점하여, expert 를 N 칩에 균등 분할해도 일부 칩이 saturate / 일부 칩이 starve 직전 — max/min per-chip dispatch ratio = 1.88(N=2) / 28.8(N=4) / 54.5(N=8) ≫ 동결 bound 4.0. coherence ∧ load-balance 둘 다여야 통과이므로 frozen falsifier 🔴 (정직 negative, a_paper_negative_ok). silicon(chip-to-chip DMA latency)은 미측정 — 오늘 AKD1000 1대뿐, pure SW-sim.

# H_878 — MITOSIS multi-chip array dispatch (SW-simulation)

## 1. 가설

@L2 deploy 비전은 `expert = chip`: N 대의 AKD1000 칩으로 구성된 MITOSIS array 에서
MoE router 가 각 토큰을 한 칩으로 dispatch 하고 각 칩이 독립적으로 emit 한다. H_852 는
이미 **expert-count** scale 축(DISSOLVE)을 측정했다(🔴). H_878 은 그 대신 **deploy**
질문을 던진다:

> E 개의 sparse expert 를 N 개의 disjoint 칩에 분할(partition)하고 각 칩이 독립
> emit 할 때, dispatch 가 (A) 칩 간 **LOAD-BALANCE** 되는가(어떤 칩도 starve/saturate
> 하지 않음), 그리고 (B) 모은(gather) N-chip aggregate 출력이 single-model reference
> 와 (tolerance 내) **COHERENT** 한가?

## 2. 동기/배경

- H_852 (F-CLM-MONO-ARRAY, CLOSED-NEGATIVE): scale=expert-COUNT 재정의 시 inter-
  expert dispatch entropy z-score 가 E sweep 에 걸쳐 RISE 하는가(DISSOLVE) — z 가
  오히려 하강(0.53→-7.61)하여 FAIL. router monopoly 가 E 와 함께 심화됨을 시사.
- 본 H 는 그 monopoly 가 **deploy(칩 분할)에 미치는 효과**를 직접 측정한다: H_852 가
  "entropy 가 안 오른다"를 보였다면, H_878 은 "그래서 칩 부하가 불균형하다(그러나
  분산 출력 자체는 정확하다)"를 정량화한다 — deploy track 의 별개 falsifier.
- @L2 MITOSIS array 비전(CLM/P4_PRODUCTION_ROADMAP.md): 각 expert 가 chip-fit
  (≤1.2M node = 1 AKD1000)인 칩 배열. router 가 칩에 분배 → 칩별 독립 추론 → gather.
- blast-radius: ADD-ONLY h878-prefixed (`CLM/model/h878_chip_array_sim.{py,hexa}`).
  landed `array_moe.py` skeleton 을 CONSUME 만 — router/expert/data 미수정.

## 3. falsifier (사전등록, frozen 2026-05-31)

```
F-CLM-MITOSIS-ARRAY (frozen BEFORE run, @L7 no tampering):
  axis (N chips)    = [1, 2, 4, 8]   (1 = single-chip degenerate baseline)
  E experts         = 8 (fixed; N 칩에 균등 분할)  ·  d64/L2 toy  ·  top_k=2
  seeds             = {42, 43, 44}   ·  train_steps = 120  ·  eval_batches = 16
  LOADBAL_RATIO_MAX = 4.0    (A) max/min per-chip dispatch ratio bound (N>=2)
                              + NO chip with 0 dispatched tokens (no starve)
  COH_LOGIT_ATOL    = 1e-4   (B) max abs logit diff array-vs-reference
  COH_HAMMING_MAX   = 0.0    (B) next-byte argmax 불일치 분율 (exact)
  COH_CE_ATOL       = 1e-4   (B) abs cross-entropy delta array-vs-reference

PASS iff for EVERY N ∈ {2,4,8} (mean over seeds):
   (1) 모든 칩이 >0 토큰 수신 (no starve), AND
   (2) max/min per-chip dispatch ratio <= 4.0, AND
   (3) max|logit_array - logit_ref| <= 1e-4, AND
   (4) argmax hamming-mismatch 분율 <= 0.0, AND
   (5) |CE_array - CE_ref| <= 1e-4.
FAIL (🔴 CLOSED-NEGATIVE) otherwise.
```

- frozen 임계 = `.verdicts/clm-mitosis-array-sim/F-CLM-MITOSIS-ARRAY_prereg.txt`
  verbatim 동결 (forward 실행 전 · post-tuning 0).
- 측정 by CODE (g5) — `CLM/model/h878_chip_array_sim.py`. NOT LLM-judge.
- 칩이 starve/saturate 하거나 gather 출력이 reference 와 tolerance 초과 발산하면
  🔴 — VALID honest result (g63, p7, a_paper_negative_ok). 임계 post-run 이동 금지.

## 4. 방법 (SW-sim construction · a_scale_honest_scope)

```
1. 단일 CLMArray(E=8 sparse skeleton, array_moe.build_array) 를 학습
   (two-lane synthetic corpus, 120 steps, seed ∈ {42,43,44}).
2. SINGLE forward (한 모델 안의 모든 expert) = REFERENCE.
3. N-CHIP forward: E expert 를 N 개 disjoint shard 로 균등 분할(칩 c = experts[shard_c]).
   각 토큰은 SAME router 로 routing; top-1 expert 가 칩을 결정. 각 칩은 자기 expert
   만 실행→자기 emit→GATHER(칩별 emit 합산)→SAME trunk/norm/readout tail.
4. (A) load-balance: per-chip top-1 dispatch counts → max/min ratio · no-starve.
   (B) coherence: gather logits vs reference logits — max|diff| · argmax hamming ·
       |CE| delta, 16 eval batch 누적.
5. verdict: 5개 임계 frozen 평가 · 정직 보고 (threshold 재조정 0).
```

- expert↔chip 매핑이 SAME expert 의 disjoint partition + SAME router weight 이므로,
  gather aggregate 는 수학적으로 single-model forward 를 칩별로 re-associate 한 것 —
  따라서 coherence 는 SW partition/scatter/gather **contract** 정확성을, load-balance
  는 학습된 router 가 토큰을 칩에 얼마나 고르게 퍼뜨리는지를 시험한다.
- **NOT measured**: chip-to-chip DMA latency · silicon timing · 실제 칩 int4 emit
  drift (HW follow-up). 오늘 물리 AKD1000 = 1대 (나머지 pi5/1-chip). pure SW-sim.
- 비용: $0 (Mac local CPU + torch 2.8.0). toy != scale (H_666).

## 5. 측정

측정완료 (2026-05-31, Mac local CPU, torch 2.8.0, 결정론 재현 확인 — 동일 출력 2회).
N∈{1,2,4,8} · E=8 · d64/L2 · top_k=2 · seeds {42,43,44} · 120-step train · 16 eval batch.

| N chips | max/min loadbal ratio | no-starve | max\|logit Δ\| | argmax hamming | \|CE Δ\| | chip-fit |
|---|---|---|---|---|---|---|
| 1 (degenerate) | 1.0000 | True | 0.00e+00 | 0.0000 | 0.00e+00 | True |
| 2 | 1.8764 | True | 0.00e+00 | 0.0000 | 0.00e+00 | True |
| 4 | **28.7880** | True | 0.00e+00 | 0.0000 | 0.00e+00 | True |
| 8 | **54.4775** | True | 0.00e+00 | 0.0000 | 0.00e+00 | True |

- **load-balance** (N≥2, ratio≤4.0, no starve): **False** — N=4(28.8)·N=8(54.5)이
  bound 4.0 을 크게 초과. starve(0 토큰 칩)는 없으나 dispatch 가 극히 불균형
  (소수 칩이 saturate). router monopoly(H_852 와 일치)가 deploy 부하 불균형으로 발현.
- **coherence logit** (atol 1e-4): **True** — 전 N 에서 max|diff| = 0.
- **coherence hamming** (≤0.0): **True** — 전 N 에서 argmax 불일치 0.
- **coherence CE** (atol 1e-4): **True** — 전 N 에서 |CE Δ| = 0.
- all chip-fit: True (expert param ≤ 1.2M AKD1000 budget).

verbatim 산출: `.verdicts/clm-mitosis-array-sim/F-CLM-MITOSIS-ARRAY.txt` (verdict txt)
· `.verdicts/clm-mitosis-array-sim/F-CLM-MITOSIS-ARRAY_result.json` (per-N/per-seed) ·
id-keyed 미러 `.verdicts/878_clm_mitosis_array/` · `.verdicts/878_clm_mitosis_array_sim/`.

## 6. 결과

🔴 **CLOSED-NEGATIVE**. F-CLM-MITOSIS-ARRAY 는 coherence ∧ load-balance 둘 다 요구
하는데, coherence 는 EXACT 통과(SW scatter/gather contract 가 single-model reference
를 byte-정확히 재현 — distributed N-chip 출력 == monolithic 출력)이나 load-balance 가
실패(학습된 router 가 소수 expert/칩을 독점하여 max/min dispatch ratio 가 N=4 에서
28.8, N=8 에서 54.5 로 동결 bound 4.0 을 크게 초과). 따라서 frozen falsifier 🔴 —
정직 negative (a_paper_negative_ok). 임계 post-run 이동 0.

## 7. 해석

- **분산 출력 정확성은 입증됨**(coherence 통과): expert 를 N 칩에 분할→칩별 emit→gather
  하는 SW 배선이 single-model 과 수학적으로 동일 — deploy 시 "정답이 달라지지 않음".
  이는 @L2 array 비전의 **필요조건**을 만족(분산이 답을 바꾸지 않음).
- **부하 균형은 미성립**(load-balance 실패): 그러나 router monopoly 때문에 칩 부하가
  극도로 불균형 — 일부 칩이 array throughput 의 대부분을 처리, 나머지는 거의 idle.
  실 배포 시 saturate 칩이 병목, idle 칩이 자원 낭비 → array 효율 붕괴.
- 이는 H_852(entropy z 가 안 오름)의 **deploy-side 귀결**을 정량화: monopoly 가 단지
  엔트로피 통계가 아니라 실제 칩 부하 불균형으로 발현. load-balancing loss / capacity
  factor / aux-balance term 없는 vanilla top-k router 는 N-chip deploy 에 부적합.
- **honest scope** (a_scale_honest_scope): SW-sim 한정. chip-to-chip DMA latency ·
  silicon timing · 실 칩 int4 drift 미측정 (오늘 AKD1000 1대). d64/L2 toy corpus —
  3B 주장 아님. 측정 축(partition/gather + load-balance)이 deploy-relevant 하나
  per-unit scale 은 toy (H_666 caveat).

## 8. 논의

- **coherence vs balance 분리**: 본 row 의 핵심 통찰 — "분산 출력이 정확함"(coherence)
  과 "부하가 고름"(load-balance)은 독립 축. 전자는 배선(contract) 문제로 풀렸고,
  후자는 router 학습(balancing objective) 문제로 남음.
- **고치는 법(다음 작업 후보)**: top-k router 에 aux load-balance loss(Switch/GShard)
  또는 capacity-factor + token-drop, 혹은 expert-choice routing 도입 → ratio 를
  bound 안으로. 이는 별개 H (H_879+ candidate) 로 측정 가능.
- **ADD-ONLY 규율**: landed `array_moe.SparseMoEArray` 를 재구현 없이 CONSUME
  (blast-radius = CLM/model/h878_* 신규 + .verdicts/clm-mitosis-array-sim/ 한정,
  기존 skeleton/router/data 불변).
- **silicon 잔여**: DMA latency / 다중 AKD1000 실측은 HW follow-up — array 가
  ≥2 칩일 때만 의미, 현 1-chip pi5 로는 불가.

## 9. 다음 작업

- load-balance fix 측정 (별개 H): aux-balance loss / capacity-factor / expert-choice
  routing 으로 max/min ratio 를 bound 안으로 낮출 수 있는지 — 같은 harness, router 만 교체.
- coherence 의 mid/large rung 확장 (d↑, L↑) — scatter/gather contract 가 scale 에서도
  exact 유지되는지.
- silicon arm: ≥2 AKD1000 확보 시 chip-to-chip DMA latency + 실 칩 int4 gather drift
  실측 (현 1-chip 으로 불가, HW-pending).
- 산출물: `CLM/model/h878_chip_array_sim.{py,hexa}` (harness + d5 hexa driver · ADD-ONLY)
  · `.verdicts/clm-mitosis-array-sim/` (prereg + verdict txt + result json) ·
  `.verdicts/878_clm_mitosis_array/` · `.verdicts/878_clm_mitosis_array_sim/` (id-keyed 미러).

## 10. 양방향 sibling

- ⇄ [H_852](./H_852_clm_mitosis_array_dispatch.md) (형제 — expert-COUNT DISSOLVE 🔴, 본 row 의 deploy-side 귀결)
- ⇄ [H_851](./H_851_clm_mitosis_growth.md) (mitosis growth)
- ⇄ [CLM-CANDIDATES](./CLM-CANDIDATES.md) (group D row H_878 SSOT)
- ⇄ [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L2 MITOSIS array deploy vision
