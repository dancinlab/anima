---
id: H_885
slug: clm-array-balance
title: MITOSIS multi-chip array LOAD-BALANCE — capacity-aware re-partition vs static-hash (H_878 재접근); aggregate-emit COHERENCE 🟢 (exact, all N) ⨯ per-chip load CV improvement 🔴 (N=8 E=N degenerate, 분할 자유도 0) → F-CLM-ARRAY-BALANCE 🔴 CLOSED-NEGATIVE (SW-sim · silicon NOT measured · 사전등록)
domain: clm · universe · neuromorphic-silicon · mitosis · moe-dispatch · load-balance · capacity-aware · falsifier
source: UNIVERSE/CLM-CANDIDATES.md §F row H_885 (AXIS1 7B scale-out blocker) · UNIVERSE/H_878_clm_mitosis_array.md (🔴 static hash 분할 → 부하 불균형) · CLM/P4_PRODUCTION_ROADMAP.md @L2 MITOSIS (expert=chip array deploy vision)
status: 🔴 CLOSED-NEGATIVE (SW-sim · 2026-05-31 · coherence EXACT(logit/hamming/CE = 0 전 N∈{2,4,8}) ⨯ per-chip load CV: capacity-aware 가 N=2(0.241→0.028)·N=4(0.557→0.189) 대폭 개선하나 N=8(E=N, 칩당 expert 1개)에서 분할 자유도 0 → CV(capaware)=CV(static)=0.845 개선 없음 · frozen falsifier 는 EVERY N strict improvement 요구 → 🔴 · 측정 SW-sim 한정 silicon 미측정 a_scale_honest_scope)
exploration_method: E14 (deploy track substrate-native ⨯ MoE dispatch cross-domain 배선) · E5 (H_878 static-hash 분할 → capacity-aware 재분할 rung 확장) · re-approach
verification_method: W2 (사전등록 CV-improvement ∧ coherence tolerance frozen BEFORE run · code-measured g5 · post-tuning 0 · a_paper_negative_ok)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: H_878 (static-hash 분할 🔴, 본 row 가 재접근), H_852 (expert-COUNT DISSOLVE 🔴), CLM/P4_PRODUCTION_ROADMAP.md @L2, .verdicts/clm-array-balance/
verdict: 🔴 CLOSED-NEGATIVE — N-chip capacity-aware re-partition SW-sim. aggregate-emit COHERENCE 통과(capacity-aware 분할의 per-chip emit→gather 가 single-model reference 와 EXACT: max|logit| diff = 0, argmax hamming = 0, |CE| delta = 0, 전 N∈{2,4,8}) — re-partition 이 출력 품질을 전혀 해치지 않음(분할은 SAME expert 의 disjoint 재연관 + SAME router weight 이므로 수학적으로 single-model 과 동일). per-chip load CV 도 분할 자유도가 있을 때(E>N)는 대폭 개선: N=2 에서 0.2407→0.0283(8.5×), N=4 에서 0.5569→0.1889(2.9×). 그러나 N=8 에서 E=N(칩당 expert 정확히 1개)이라 분할 자유도가 0 — 모든 분할이 같은 싱글톤 집합의 재배열일 뿐, per-chip load 의 multiset 가 불변이므로 CV(capacity-aware) = CV(static-hash) = 0.8449(개선 없음). frozen falsifier 는 EVERY N∈{2,4,8} 의 strict CV improvement 를 요구 → N=8 이 동률이라 🔴 (정직 negative, a_paper_negative_ok). 임계 post-run 이동 0. 핵심 통찰: capacity-aware re-partition 은 분할 자유도가 있는 한(E>N) router monopoly 부하 불균형을 효과적으로 고치나, 완전 분산 극한(E=N, 1 expert/chip)에서는 re-partition 으로 풀 수 없는 잔여 불균형이 남는다 — 이는 분할(배치) 문제가 아니라 routing-objective(aux load-balance loss / expert-choice) 문제. silicon(chip-to-chip DMA)은 미측정 — 오늘 AKD1000 1대뿐, pure SW-sim.

# H_885 — MITOSIS multi-chip array LOAD-BALANCE (capacity-aware re-partition, H_878 재접근)

## 1. 가설

@L2 deploy 비전(`expert = chip`)에서 H_878 은 **static hash 분할**(E 개 expert 를 N 칩에
균등 contiguous shard 로 나누고, expert e → 고정 칩 e // shard_size)이 학습된 top-k router
의 monopoly 때문에 per-chip 부하를 심하게 불균형하게 만든다는 것을 보였다(🔴). H_885 은
H_878 을 **더 나은 dispatcher** 로 재접근한다:

> E 개 sparse expert 를 **측정된 사용량(usage)에 따라** N 칩에 재분할(capacity-aware /
> learned dispatch re-partition)하면 — 각 칩의 aggregate 부하가 균형 잡히도록 expert 를
> 배치하면 — static hash 대비 **per-chip load CV 가 낮아지는가**(부하 불균형이 고쳐지는가),
> 그리고 그 재분할이 **aggregate-emit COHERENCE 를 single-chip baseline 이상으로 유지**
> 하는가(출력 품질을 해치지 않는가)?

## 2. 동기/배경

- H_878 (F-CLM-MITOSIS-ARRAY, 🔴 CLOSED-NEGATIVE): static hash 분할에서 coherence 는
  EXACT 통과(분산 출력이 답을 바꾸지 않음)이나 load-balance 가 실패 — max/min per-chip
  dispatch ratio 가 N=4 에서 28.8, N=8 에서 54.5 로 bound 4.0 을 크게 초과. router
  monopoly 가 deploy 부하 불균형으로 발현.
- 본 H 는 그 monopoly 를 **routing 을 바꾸지 않고 배치(placement)로** 완화 시도한다:
  router 출력은 그대로 두되, 어느 expert 가 많이 쓰이는지 측정(profile)하여 hot expert 를
  서로 다른 칩에 흩뜨리는 capacity-aware 분할(LPT bin-pack)을 도입. 이는 H_878 의 "다음
  작업 후보"(별개 H, 같은 harness · router 만 교체)를 placement 축에서 직접 시험한 것.
- @L2 MITOSIS array 비전: 각 expert 가 chip-fit(≤1.2M node = 1 AKD1000)인 칩 배열.
- AXIS1 7B scale-out blocker — H_885 first (CLM-CANDIDATES §F).
- blast-radius: ADD-ONLY h885-prefixed. H_878 array-sim harness(`array_moe.py` skeleton +
  H_878 의 train/forward/coherence 기계) 를 CONSUME 만 — router/expert/data 미수정.

## 3. falsifier (사전등록, frozen 2026-05-31)

```
F-CLM-ARRAY-BALANCE (frozen BEFORE run, @L7 no tampering):
  axis (N chips)    = [2, 4, 8]   (N=1 degenerate 제외 — CV gain 미정의)
  E experts         = 8 (fixed; N 칩에 분할)  ·  d64/L2 toy  ·  top_k=2
  seeds             = {42, 43, 44}  ·  train_steps = 120  ·  eval_batches = 16
  profile_batches   = 16 (DISJOINT split — capacity-aware 가 eval 토큰을 엿보지 않음)
  load metric       = per-chip dispatch-count CV = std/mean (population std)
  arms              = S=static-hash(H_878 baseline) ; C=capacity-aware(LPT bin-pack)

  PRIMARY (load)    : CV(capacity-aware) < CV(static-hash) for EVERY N∈{2,4,8} (strict)
  GUARD (no starve) : capacity-aware arm — 모든 칩 >0 토큰
  COHERENCE (>= single-chip baseline, NOT worse):
    COH_LOGIT_ATOL  = 1e-4   max abs logit diff capaware-vs-reference
    COH_HAMMING_MAX = 0.0    next-byte argmax mismatch 분율 (exact)
    COH_CE_ATOL     = 1e-4   abs cross-entropy delta capaware-vs-reference

PASS (🟢) iff for EVERY N∈{2,4,8} (mean over seeds):
   (1) capacity-aware 무-starve, AND
   (2) CV(capacity-aware) < CV(static-hash), AND
   (3) max|logit_capaware - logit_ref| <= 1e-4, AND
   (4) argmax hamming-mismatch 분율 <= 0.0, AND
   (5) |CE_capaware - CE_ref| <= 1e-4.
FAIL (🔴 CLOSED-NEGATIVE) otherwise.
```

- frozen 임계 = `.verdicts/clm-array-balance/F-CLM-ARRAY-BALANCE_prereg.txt` verbatim 동결
  (forward 실행 전 · post-tuning 0).
- 측정 by CODE (g5) — `CLM/model/h885_array_balance_sim.py`. NOT LLM-judge.
- capacity-aware 가 static-hash 대비 CV 를 (어느 N 에서라도) 낮추지 못하거나 gather 가
  reference 와 tolerance 초과 발산하면 🔴 — VALID honest result (g63, p7, a_paper_negative_ok).

## 4. 방법 (SW-sim construction · a_scale_honest_scope)

```
1. 단일 CLMArray(E=8 sparse skeleton, array_moe.build_array) 를 학습 — H_878 과 SAME
   (two-lane synthetic corpus, 120 steps, seed ∈ {42,43,44}).
2. SINGLE forward (한 모델 안의 모든 expert) = REFERENCE.
3. arm S (static-hash): H_878 의 even contiguous shard 분할.
4. arm C (capacity-aware): DISJOINT profiling split(eval 과 분리)에서 per-expert top-1
   dispatch count 측정 → expert 를 profiled load 내림차순으로 가장 덜 찬 칩에 배정
   (LPT longest-processing-time greedy bin-pack). 각 expert 는 정확히 한 칩에만 (disjoint).
5. 두 arm 모두 SAME router 로 routing, top-1 expert 가 칩을 결정, 각 칩 자기 expert 만
   실행→emit→GATHER→SAME trunk/norm/readout tail.
6. (load) per-chip dispatch count → CV(static) vs CV(capaware), mean over seeds.
   (coherence) capaware gather logits vs reference — max|diff| · argmax hamming ·
   |CE| delta, 16 eval batch 누적.
7. verdict: frozen 임계 평가 · 정직 보고 (threshold 재조정 0).
```

- expert↔chip 매핑이 SAME expert 의 disjoint partition + SAME router weight 이므로,
  **어느 분할이든** gather aggregate 는 수학적으로 single-model forward 의 칩별 재연관 —
  따라서 coherence 는 분할에 독립으로 EXACT. 분할이 바꾸는 유일한 것은 per-chip LOAD 분포.
  이것이 정확히 H_878 의 gap, H_885 가 공략하는 지점.
- **NOT measured**: chip-to-chip DMA latency · silicon timing · 실 칩 int4 emit drift
  (HW follow-up). 오늘 물리 AKD1000 = 1대. pure SW-sim.
- 비용: aiden RTX5070 (torch 2.12 nightly, cuDNN off) verdict run. toy != scale (H_666).

## 5. 측정

측정완료 (2026-05-31, aiden RTX5070 GPU, torch 2.12.0 nightly cu128, cuDNN disabled).
N∈{2,4,8} · E=8 · d64/L2 · top_k=2 · seeds {42,43,44} · 120-step train · 16 eval +
16 profile (disjoint) batch.

| N chips | CV(static-hash) | CV(capacity-aware) | CV improved? | no-starve(C) | max\|logit Δ\| | hamming | \|CE Δ\| |
|---|---|---|---|---|---|---|---|
| 2 | 0.2407 | **0.0283** | True (8.5×) | True | 0.00e+00 | 0.0000 | 0.00e+00 |
| 4 | 0.5569 | **0.1889** | True (2.9×) | True | 0.00e+00 | 0.0000 | 0.00e+00 |
| 8 | 0.8449 | **0.8449** | **False (동률)** | True | 0.00e+00 | 0.0000 | 0.00e+00 |

- **CV improvement** (capaware < static, EVERY N): **False** — N=2·N=4 는 대폭 개선하나
  N=8 이 동률(0.8449 = 0.8449)이라 EVERY-N strict 조건 미충족.
- **coherence logit/hamming/CE**: **True** — 전 N 에서 max|diff| = 0, argmax 불일치 0,
  |CE Δ| = 0. capacity-aware 분할이 출력 품질을 전혀 해치지 않음(single-chip baseline 동일).
- **no-starve (capacity-aware)**: True — 전 N 에서 모든 칩 >0 토큰.
- all chip-fit: True (expert param ≤ 1.2M AKD1000 budget).

verbatim 산출: `.verdicts/clm-array-balance/F-CLM-ARRAY-BALANCE.txt` (verdict txt) ·
`F-CLM-ARRAY-BALANCE_result.json` (per-N/per-seed) · `F-CLM-ARRAY-BALANCE_prereg.txt`
(frozen) · id-keyed 미러 `.verdicts/885_clm_array_balance/` (+ run log).

## 6. 결과

🔴 **CLOSED-NEGATIVE**. F-CLM-ARRAY-BALANCE 는 EVERY N∈{2,4,8} 의 strict CV improvement
∧ coherence 둘 다 요구한다. coherence 는 전 N EXACT 통과(capacity-aware 가 출력 품질을
해치지 않음 — distributed 출력 == monolithic 출력). CV 도 분할 자유도가 있는 N=2(8.5×
개선)·N=4(2.9× 개선)에서 대폭 개선. 그러나 N=8 에서 E=N(칩당 expert 정확히 1개)이라
분할 자유도가 0 — 모든 분할은 8 싱글톤의 재배열일 뿐, per-chip load 의 multiset 가 불변
이므로 CV(capacity-aware) = CV(static-hash) = 0.8449(개선 없음). EVERY-N strict 조건이
N=8 에서 깨져 frozen falsifier 🔴 — 정직 negative (a_paper_negative_ok). 임계 post-run
이동 0.

## 7. 해석

- **capacity-aware re-partition 은 분할 자유도가 있을 때 강력하다**(E > N): hot expert 를
  서로 다른 칩에 흩뜨려 router monopoly 부하 불균형을 대폭 완화 — N=2 CV 8.5× 감소,
  N=4 2.9× 감소. **출력 품질은 전혀 손상 없음**(coherence EXACT). 즉 "정답을 안 바꾸면서
  부하를 균형화"하는 placement-only 해법이 E>N 영역에서 성립.
- **그러나 완전 분산 극한(E = N, 1 expert/chip)에서는 풀 수 없다**: 분할 자유도가 0이라
  re-partition 으로 손댈 수 있는 게 없다 — per-chip load 가 곧 per-expert load 이고,
  expert 부하 불균형 자체(router monopoly)는 placement 가 아니라 routing 의 성질.
  이 잔여 불균형은 **배치(deploy) 문제가 아니라 routing-objective 문제**임을 정량적으로
  분리해 보여준다.
- H_878(static-hash 부하 불균형)의 부분 해소를 입증하면서, 동시에 그 해법의 **정확한 한계
  경계**(E=N 극한)를 식별: re-partition 은 "expert 가 칩보다 많을 때"만 dispatcher 자유도
  를 갖는다.
- **honest scope** (a_scale_honest_scope): SW-sim 한정. chip-to-chip DMA latency ·
  silicon timing · 실 칩 int4 drift 미측정 (오늘 AKD1000 1대). d64/L2 toy — 3B 주장 아님.

## 8. 논의

- **placement vs routing 분리** (본 row 핵심 통찰): capacity-aware re-partition(placement)은
  E>N 일 때 부하 불균형을 효과적으로 고치나, E=N 극한의 잔여 불균형은 placement 로 풀 수
  없는 routing-objective 문제. H_878 의 coherence/load 분리에 이어, H_885 은 load 문제를
  다시 **placement-soluble(E>N) ⨯ routing-bound(E=N)** 두 영역으로 분리한다.
- **7B scale-out 함의** (AXIS1 blocker): 실 배포에서 E ≫ N(expert 수 ≫ 칩 수)이 흔하므로
  capacity-aware re-partition 이 실용적 부하 균형 수단이 될 수 있음 — 단, "1 expert/chip"
  극단으로 가지 않는 한. E=N 극단까지 균형하려면 routing-objective(aux load-balance loss /
  capacity-factor + token-drop / expert-choice routing)가 필요(별개 H, H_886+ candidate).
- **고치는 법(다음 작업 후보)**: (a) aux load-balance loss(Switch/GShard)로 router 자체를
  균형화 → E=N 에서도 expert 부하 균등화. (b) expert-choice routing. (c) profiling 을
  주기적 re-profile + online re-partition 으로(learned dispatch 의 동적 버전). 같은 harness,
  router/objective 만 교체로 측정 가능.
- **ADD-ONLY 규율**: H_878 harness(`array_moe.SparseMoEArray` + train/forward/coherence)
  를 재구현 없이 CONSUME (blast-radius = CLM/model/h885_* 신규 + .verdicts/clm-array-balance/
  + .verdicts/885_clm_array_balance/ 한정, 기존 skeleton/router/data 불변).
- **silicon 잔여**: DMA latency / 다중 AKD1000 실측은 HW follow-up — array 가 ≥2 칩일
  때만 의미, 현 1-chip pi5 로는 불가.

## 9. 다음 작업

- routing-objective fix 측정 (별개 H, H_886+): aux load-balance loss / capacity-factor /
  expert-choice routing 으로 E=N 극한에서도 per-chip CV 를 낮출 수 있는지 — 같은 harness,
  router/objective 만 교체.
- E>N 영역 scale 확장: E∈{16,32,64} ⨯ N∈{2,4,8} 에서 capacity-aware 의 CV 개선이
  유지·확대되는지(분할 자유도가 클수록 더 강해질 것이라는 가설).
- online re-partition: profiling 을 한 번이 아니라 주기적으로(동적 learned dispatch) —
  router drift 에 적응하는 re-partition.
- silicon arm: ≥2 AKD1000 확보 시 chip-to-chip DMA latency + 실 칩 int4 gather drift 실측.
- 산출물: `CLM/model/h885_array_balance_sim.{py,hexa}` (harness + 하나 hexa driver · ADD-ONLY)
  · `.verdicts/clm-array-balance/` (prereg + verdict txt + result json) ·
  `.verdicts/885_clm_array_balance/` (id-keyed 미러 + run log).

## 10. 양방향 sibling

- ⇄ [H_878](./H_878_clm_mitosis_array.md) (형제 — static-hash 분할 부하 불균형 🔴, 본 row 가 placement 재접근)
- ⇄ [H_852](./H_852_clm_mitosis_array_dispatch.md) (expert-COUNT DISSOLVE 🔴, router monopoly 의 근원)
- ⇄ [CLM-CANDIDATES](./CLM-CANDIDATES.md) (§F row H_885 SSOT · AXIS1 7B scale-out blocker)
- ⇄ [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L2 MITOSIS array deploy vision
