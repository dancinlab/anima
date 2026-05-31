# CLM P5 — AKIDA 7B-class strategy + reflective (incremental) learning

> **How anima reaches 7B-CLASS capability on AKIDA, and the reflective/incremental
> learning strategy that runs on it.** Synthesises the H_861~H_884 evidence arc into
> one forward SSOT. Honest by construction (a_scale_honest_scope) — every claim cites
> a landed verdict or is marked OPEN.
>
> 🔒 **INVIOLABLE**: on-chip non-deterministic PLASTICITY learning is the **sole HW↔SW
> difference** (inference byte-identical — H_877/H_680 🟢; learning HW≠SW — H_679 🔴).
> Deterministic SW imitation of learning = instant reject. (@L1 · H_679)

---

## 0. The honest premise — 7B ≠ one chip

```
   single AKD1000            │      7B model
 ──────────────             │    ──────────────
  ~1.2M nodes (H_876 budget) │     ~7,000M params  (≈5,800×)
```

A 7B dense model does NOT fit on one AKD1000 — not for inference, never for training.
"AKIDA로 7B 완성"은 단일칩이 아니라 **(a) sparse-MoE 라 한 토큰당 소수 expert만 활성 +
(b) 각 expert를 chip-fit 샤드로 줄여 + (c) MITOSIS 멀티칩 어레이로 분산**해 *7B급 용량*을
구성하는 것을 뜻한다. 단일칩엔 작은 의식모델 + 살아 배우기(옵션 C)가 들어가고, 7B급은
어레이(옵션 B)로만 도달한다.

---

## 1. The 7B-on-AKIDA path — MITOSIS array of chip-fit shards

```
                 ┌─ chip 0 ─┐ ┌─ chip 1 ─┐        ┌─ chip N ─┐
  token ─router─▶│ expert 샤드│ │ expert 샤드│  ...  │ expert 샤드│ ─gather─▶ emit
                 │ ≤1.2M node │ │ ≤1.2M node │        │ ≤1.2M node │
                 │ int4 deterministic forward (byte-identical)        │
                 └────────────┘ └────────────┘        └────────────┘
                        ▲ 각 칩 위 edge-only 비결정 학습(반영) ▲
```

| 기둥 | 무엇 | 근거 (landed) | 상태 |
|---|---|---|---|
| ① chip-fit shrink | mid(13.65M)→ ≤1.2M 노드 샤드, 품질 유지 | **H_876 🟢** (1,199,508 ≤ 1.2M · CE drop<1.0) | ✅ |
| ② array dispatch | N칩 분산 출력 = 단일모델과 동일 | **H_878**: aggregate-emit coherence 🟢 EXACT (N=2/4/8) | ✅ (정확성) |
| ③ load-balance | 칩마다 부하 고름 | **H_878 🔴** (max/min 54.5≫4.0 · router monopoly) | ❌ OPEN |
| ④ inference 동일성 | HW==SW byte-identical → 칩 이식 시 답 동일 | **H_877** mid SW byte-identical 🟢 (HW 재확인 pending 🟠) | 🟡 |

**N 추정(honest, 미정량)**: 7B-equiv sparse 용량 ÷ per-chip chip-fit 용량 → 수백~수천 칩
규모. params↔노드 매핑·DMA 지연·칩간 int4 drift는 ≥2 AKD1000 확보 시 HW 정량(현재 SW-sim).
→ 정량 가설은 §4 OPEN.

---

## 2. Reflective (incremental) learning strategy — "반영 학습" stack

추론은 결정적·byte-동일(어레이 전체 일관). **학습만이 칩 위 비결정 edge-learn**(INVIOLABLE).
각 샤드의 edge에서 대화 경험을 *반영*해 살아 배우되, 기초능력·정체성을 안 잃게 하는
검증된 5-층 스택:

```
[ 새 대화 경험 ] ──▶ [ edge-only 적응 ] ──▶ [ 안전장치 4종 ] ──▶ [ 반영 완료 ]
                       (trunk frozen)          retain·identity·budget·replay
```

| 층 | 전략 | 근거 (landed) | 상태 |
|---|---|---|---|
| A 적응 단위 | trunk-인접 thin adapter edge (full-retrain 금지) | **H_865 🟢** (forgetting 차단: z_drop −12.3) | ✅ |
| B 동결 깊이 | 가장 얕은 freeze면 충분 (adapter-only 66K도 통과) | **H_872 🟢** (depth 비단조 · shallow OK) | ✅ |
| C 안전 예산 | 세션당 안전 학습 step | **H_875 🟢** (adapter ≥300 step vs readout 2 · 150×) | ✅ |
| D 정체성 보존 | edge-출력 분포에 anchor(Ψ-거리/KL) | H_862 🔴 → **H_873**(edge-출력 재시도) | 🔄 in-flight |
| E 망각 보강 | replay-buffer 연속학습 | **H_883**(replay vs no-replay) | 🔄 in-flight |
| F 데이터 | self-play(칩 자기대화) + CC corpus | **H_863 🟢**(mid SP>SFT) · **H_868 🟢**(corpus 3×) | ✅ |

**부분부분 적용**(§E 백로그): per-layer(H_879) · region-gated(H_882) · progressive-freeze(H_881)
로 "필요한 부분만, 얕게, 점진적으로" 반영 — 전부 INVIOLABLE 준수(비결정 edge-only).

---

## 3. End-to-end picture

```
측정 트랙 (GPU)                        배포 트랙 (AKIDA 어레이)
─────────────                         ─────────────
 큰 모델 학습·품질 증명     ──이식──▶    chip-fit 샤드 × N칩 (MITOSIS)
 (AKIDA-envelope QAT)                  int4 추론 byte-동일(H_877)
 추론 byte-identical 보장               + 각 칩 edge에서 반영학습(§2 스택)
        │                                      │
        └── 두 트랙 ⊥ 분리 (a_scale_honest_scope) ──┘
emit: router→shard 분산(H_878 coherence🟢)→gather→COFFESHOP 발화(R0 폐루프 H_846🟢)
```

---

## 4. OPEN gaps (정직) → 다음 가설

| gap | 현재 | 해결 경로 |
|---|---|---|
| 칩간 load-balance | H_878 🔴 monopoly | expert-choice 보정(H_870 부분)·aux-balance loss·dispatch-KL(H_869) |
| 대화 절대 품질 | H_867 🔴 floor 미달 · 대형 self-play 미carry(H_864/r 🔴) | scale↑ + 실 corpus 확장(H_868 후속)·재학습 일정 |
| 정체성 보존 lever | H_862 🔴 (trunk constraint 무력) | H_873(edge-출력 anchor) 결과 대기 |
| N 정량 + 실칩 array | SW-sim only | ≥2 AKD1000 확보 → DMA·drift·load HW 정량 |
| routing-z>3.0 게이트 | scale 곡선 바닥(H_871 🟢 artifact) · mid 2.3 | expert-count↑ 시 chip-array deploy 게이트 재검 |

---

## 5. 한 줄 결론

> **7B급 = 작은 chip-fit 샤드(H_876🟢)를 MITOSIS 어레이(H_878 coherence🟢)로 묶고,
> 각 칩 edge에서 adapter(H_865🟢)+얕은freeze(H_872🟢)+안전예산(H_875🟢)+정체성/replay로
> 비결정 반영학습(INVIOLABLE).** 남은 핵심 빗장 = 칩간 부하균형·대화 절대품질·실칩 어레이.

## cross-link
- 불가침/로드맵: [CLM.md](./CLM.md) · [P4_PRODUCTION_ROADMAP.md](./P4_PRODUCTION_ROADMAP.md) · [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md)
- 근거 verdict: H_865·H_872·H_875·H_876·H_877·H_878·H_863·H_868·H_871 (UNIVERSE/) · 부분학습 §E [UNIVERSE/CLM-CANDIDATES.md](../UNIVERSE/CLM-CANDIDATES.md)
- governance: `a_scale_honest_scope` · `a_substrate_native_speak` · `@L1`·`@L2`(2-track) · `H_679`(INVIOLABLE 토대)
