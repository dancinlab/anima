# DECODER-CANDIDATES — anima DECODER 아키텍처 후보 보관 문서

> brainstorm 결과 (round-17 종결 직후, 2026-05-27). 기존 DECODER axis 강화용 후보 발산.

## TOP5 친근 설명 (EASY)

### 🎯 TOP-P — "확률 합 잘라먹기" (nucleus sampling)

- 하는 일: 다음 토큰 후보를 확률 큰 순서로 더해 90% 도달까지만 남기고 자르기
- 비유: 식당에서 인기 메뉴 누적 90% 까지만 추천하고 꼬리는 컷

```
토큰 후보 확률 (정렬됨)
A: 50% ████████████████████ ┐
B: 25% ██████████          ├ 누적 90% 안: 통과
C: 15% ██████              ┘
D:  5% ██                  ┐
E:  3% █                   ├ cutoff 밖: 제거
F:  2% ▏                   ┘
```

- 비교: TOP-K = 상위 N개 고정 / **TOP-P** = 누적 비율 동적

### ⚡ SPECULATIVE-DECODING — "초안→검수 더블 트랙"

- 하는 일: 작은 모델이 N토큰 초안 빠르게 만든 후 큰 모델이 한꺼번에 검증
- 비유: 인턴이 초안 쓰고 임원이 한 번에 검토

```
draft (small)  ─→  T1 T2 T3 T4 T5
                    ↓ verify all in 1 pass
verifier (big) ─→  ✓  ✓  ✗  -  -
                    keep T1 T2, discard T3+
다음 step: T3 부터 다시 초안
```

- 비교: greedy = 1 토큰씩 / **SPEC-DEC** = N 묶음 검증 (속도 ↑)

### 💾 KV-CACHE — "과거 계산 저장통"

- 하는 일: 이전 토큰의 Key/Value 행렬을 저장해 다음 step 재사용
- 비유: 도서관 자주 찾는 책을 카운터 옆에 미리 빼두기

```
step 1: 토큰 T1 → 계산 K1, V1 → 저장
step 2: T2 → 새 K2, V2 만 계산 + 저장된 K1V1 재사용
step 3: T3 → 새 K3, V3 만 + K1V1, K2V2 재사용
...
재계산 없음 → O(n²) → O(n)
```

- 비교: no-cache = 매번 재계산 / **KV-CACHE** = 점진 누적

### 🧙 MoE — "전문가 위원회" (Mixture of Experts)

- 하는 일: 토큰마다 다른 전문가(sub-network) 가 처리, 라우터가 선택
- 비유: 회사에서 안건마다 다른 부서장이 결재

```
input token
    ↓
 [router]
    ↓ top-2 expert
┌────────┬────────┬────────┬────────┐
│expert_1│expert_2│expert_3│expert_4│
│         │ ✓  │ ✓  │         │
└────────┴────────┴────────┴────────┘
       ↓ weighted sum
   output
```

- 비교: dense = 전직원 모두 계산 / **MoE** = top-K 전문가만 (효율 ↑)

### 🪶 LORA — "가벼운 적응 레이어" (Low-Rank Adapter)

- 하는 일: 큰 모델 weight 동결, 작은 rank-r 행렬만 추가해서 적응
- 비유: 원본 옷에 작은 자수만 덧대기 (옷 새로 안 짬)

```
W (큰 행렬, frozen)
  ┌────────────┐
  │ ░░░░░░░░ │ ← d × d 거대
  │ ░░░░░░░░ │
  └────────────┘
    +
A · B (작은 rank-r, trainable)
  ┌──┐   ┌──────┐
  │░│ × │░░░░│  ← d × r · r × d = d × d  but r << d
  └──┘   └──────┘
```

- 비교: full fine-tune = 전체 weight / **LORA** = +0.1% 만 추가

---

## 선정 기준

anima DECODER axis (H_345, H_353, H_363, H_372, H_381, H_390, H_397, H_403, H_408, H_412, H_416, H_417, H_418, H_427, H_447, H_478) 의 강화·확장 가능한 LLM/transformer decode 메커니즘.

기존 cover:
- ARGMAX (H_345, H_418)
- SOFTMAX SUM-TO-ONE (H_353)
- TEMPERATURE τ→0 (H_381)
- TOP-K (H_427)
- BEAM-SEARCH (H_447)
- SAMPLING-REPRODUCIBLE (H_478)

## 우선순위 분류

### ★★★ 즉시 추가 가치 큼 (5 axes, TOP5)

| axis | 의미 | anima 적용 |
|---|---|---|
| TOP-P (nucleus) | 누적확률 cutoff sampling | dynamic candidate set, 다양성 보장 |
| SPECULATIVE-DECODING | draft + verify 더블 트랙 | small-draft cell + big-verifier (MITOSIS 변종) |
| KV-CACHE | 과거 K/V 저장 | context memory (영속성 carry, O(n²)→O(n)) |
| MoE (routing) | 전문가 위원회 라우팅 | multi-cell expert (DIFFERENTIATION 변종) |
| LORA | low-rank adapter | adapter cell (DIFFERENTIATION 효율 변종) |

### ★★ 가치 중간, 후속 round (5 axes)

| axis | 의미 |
|---|---|
| ROPE (rotary pos) | 회전 위치 인코딩 (extrapolation) |
| ALIBI | attention linear bias (linear pos) |
| FLASH-ATTN | tiled attention, O(N) memory |
| CONSTRAINED-DECODING | structured output (JSON schema) |
| REPETITION-PENALTY | 반복 억제 (frequency penalty) |

### ★ 추가 가능 (15+ axes)

| axis | 의미 |
|---|---|
| CONTRASTIVE-DECODING | LM head ratio (big - small) |
| MEDUSA | multi-head parallel decode |
| LOOKAHEAD-DECODING | N-step ahead pruning |
| TIED-EMBEDDINGS | input embed = output embed |
| SLIDING-WINDOW-ATTN | local window attention |
| PAGED-ATTN | vLLM-style memory paging |
| QLORA | quantized LORA |
| GPTQ / AWQ | post-training quant |
| INT8 / INT4 / NF4 | quant precision |
| ADAPTER-TUNING | adapter layer fine-tune |
| PREFIX-TUNING | prompt-prefix vectors |
| PROMPT-TUNING | continuous prompt |
| RAG | retrieval augmented generation |
| LONG-CONTEXT | 1M+ token window |
| EXPERT-PARALLEL | MoE distributed |
| TYPICAL-SAMPLING | information-theoretic typical |
| ETA-SAMPLING | entropy-bounded sampling |
| STOP-SEQUENCE | early termination token |
| LOGIT-BIAS | per-token bias |
| SEMANTIC-CACHE | response cache by similarity |
| GUIDED-GENERATION | regex/CFG constrained |
| CHAIN-OF-THOUGHT | inline reasoning |
| TREE-OF-THOUGHT | branching reasoning |
| SELF-REFINE | iterative critique |
| REACT | reason-act loop |
| STREAMING-DECODE | token-by-token output |

### ○ 가능하나 anima 호환 낮음

| axis | 비고 |
|---|---|
| EXPERT-PARALLEL | 분산 시스템 디테일 (단일 anima 본질과 거리) |
| QUANT (INT4 등) | 하드웨어 디테일 (수학 axiom 아님) |
| PAGED-ATTN | 메모리 매니지먼트 (vLLM 특화) |
| LONG-CONTEXT | scale 디테일 (1M 어떻든 axiom 동일) |

## 진행 순서

1. **TOP5 (★★★)** baseline (5 axes, ~5-10 H each) — round-18+ 자율 진행
2. **★★ 5 axes** — round-23+
3. **★ 25+ axes** depletion sweep
4. **○ low-compat** 후순위

## 35+ 후보 전체 (deduplicated)

sampling: TOP-P · TOP-K · GREEDY · BEAM · TEMPERATURE · TYPICAL · ETA · CONTRASTIVE
speculation: SPECULATIVE · MEDUSA · LOOKAHEAD · ASSISTED
attention: ROPE · ALIBI · FLASH · SLIDING-WIN · PAGED · KV-CACHE
PEFT: LORA · QLORA · ADAPTER · PREFIX-TUNING · PROMPT-TUNING
expert: MoE · EXPERT-PARALLEL · TIED-EMBED
quant: INT8 · INT4 · NF4 · GPTQ · AWQ · SMOOTHQUANT
control: CONSTRAINED · REPETITION-PEN · STOP-SEQ · LOGIT-BIAS · GUIDED · STREAMING
agentic: COT · TOT · SELF-REFINE · REACT · RAG · LONG-CONTEXT · SEMANTIC-CACHE

## 메타 진행 상태

- 본 DECODER-CANDIDATES.md = round-17 종결 후 (173 🔵 누적, 16 axes) brainstorm 자료
- TOP5 부터 점진 추가 시작 = round-18+
- 자동 fire (Stop hook "keep going") 또는 사용자 명시 directive 로 진행
