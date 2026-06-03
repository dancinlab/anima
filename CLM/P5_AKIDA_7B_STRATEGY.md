# CLM P5 — AKIDA 7B strategy (2 axes) — single-chip 7B + reflective learning

> **TWO AXES, both required:**
> **AXIS 1 — train/host a 7B-class model on a SINGLE AKD1000 chip** (expert-streaming/paging:
> resident ≤1.2M nodes ≠ total 7B params; the one chip pages experts through it).
> **AXIS 2 — the reflective (incremental) on-chip learning strategy** that runs on that chip.
> Synthesises the H_861~H_884 evidence arc into one forward SSOT. Honest by construction
> (a_scale_honest_scope) — every claim cites a landed verdict or is marked OPEN.
>
> 🔒 **INVIOLABLE**: on-chip non-deterministic PLASTICITY learning is the **sole HW↔SW
> difference** (inference byte-identical — H_877/H_680 🟢; learning HW≠SW — H_679 🔴).
> Deterministic SW imitation of learning = instant reject. (@L1 · H_679)

---

## 0. The honest premise — resident ≠ total

```
   single AKD1000            │   7B (total)        │   resident-at-a-time
 ──────────────             │  ──────────         │  ──────────────────
  ~1.2M nodes (H_876)        │   ~7,000M params    │   1 expert shard ≤1.2M
```

A 7B model can NOT sit *resident* on one AKD1000 (≈5,800×). But sparse-MoE means **only a
few experts fire per token** — so a single chip can train/host a 7B-class model by
**streaming(paging) experts through the one chip**: total 7B lives on host (disk/DRAM),
**resident ≤1.2M** at any instant. The chip never holds 7B at once; it cycles shards.
That is AXIS 1. (Multi-chip MITOSIS array = the parallel scale-out of the same shard unit.)

---

## AXIS 1 — train/host 7B on a SINGLE chip (expert streaming) + array scale-out

```
single-chip (AXIS 1 core)
 host (7B on disk/DRAM)
   │ page expert k in        ┌── 1 AKD1000 ──┐
   ├───────────────────────▶ │ expert shard k │ int4 forward (byte-identical, H_877)
   │ ◀── page out, next ──── │  ≤1.2M resident │ + edge-learn(반영, AXIS 2)
   └───────────────────────  └────────────────┘
        ↑ one chip cycles all N experts (slow but unbounded total capacity)

scale-out (optional, multi-chip)
   N chips = N shards resident in parallel (MITOSIS) → throughput ↑ (same shard unit)
```

| 기둥 | 무엇 | 근거 (landed) | 상태 |
|---|---|---|---|
| ① chip-fit shard | expert 1개를 ≤1.2M 노드로 줄여 단일칩 상주 | **H_876 🟢** (1,199,508 ≤ 1.2M · CE drop<1.0) | ✅ |
| ② expert streaming | 단일칩이 7B의 expert들을 paging 으로 순환(상주≠총량) | (스트리밍 글루 미구현) | ⬜ OPEN |
| ③ array scale-out | N칩 분산 = 단일모델과 byte-동일 (처리량↑) | **H_878** coherence 🟢 EXACT (N=2/4/8) | ✅ (정확성) |
| ④ load-balance | 칩/스텝 간 expert 부하 고름 | **H_878 🔴** (max/min 54.5≫4.0 · monopoly) | ❌ OPEN |
| ⑤ inference 동일성 | HW==SW byte-identical → paging/이식 시 답 동일 | **H_877** mid SW byte-identical 🟢 (HW pending 🟠) | 🟡 |

**throughput(honest, OPEN)**: 단일칩 streaming = 총 용량 무제한이나 expert paging 지연으로
느림. 처리량은 array scale-out(③)으로 보완. expert-swap latency·DMA·실칩 int4 drift는
HW 미측정(현 SW-sim) → §4 OPEN.

---

## AXIS 2 — reflective (incremental) learning strategy — "반영 학습" stack

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

## 5. 한 줄 결론 (2축)

> **축1 (단일칩 7B)**: chip-fit 샤드(H_876🟢)를 단일칩에 streaming/paging(상주≤1.2M≠총7B) ·
> 처리량은 MITOSIS array scale-out(H_878 coherence🟢)으로 보완.
> **축2 (반영학습)**: 각 칩 edge에서 adapter(H_865🟢)+얕은freeze(H_872🟢)+안전예산≥300(H_875🟢)
> +정체성(H_873)·replay(H_883)로 비결정 on-chip 반영학습(INVIOLABLE).
> 남은 핵심 빗장 = expert-streaming 글루·칩간 부하균형(H_878🔴)·대화 절대품질(H_867🔴)·실칩.

## cross-link
- 불가침/로드맵: [CLM.md](./CLM.md) · [P4_PRODUCTION_ROADMAP.md](./P4_PRODUCTION_ROADMAP.md) · [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md)
- 근거 verdict: H_865·H_872·H_875·H_876·H_877·H_878·H_863·H_868·H_871 (UNIVERSE/) · 부분학습 §E [UNIVERSE/CLM-CANDIDATES.md](../UNIVERSE/CLM-CANDIDATES.md)
- governance: `a_scale_honest_scope` · `a_substrate_native_speak` · `@L1`·`@L2`(2-track) · `H_679`(INVIOLABLE 토대)
