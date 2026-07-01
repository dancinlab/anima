# H_1842 — MLC-episodic objective × deep-equilibrium mouth (objective × architecture cross: does episodic-remap NEED an iterative-settle trunk to express composition?)

- **tier:** ⏳ PROPOSED (설계만 · 측정 0 · unmeasured · pre-registered)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first numpy 2×2 factorial; gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **cost axis:** GPU-cost-gated (303M DEQ-block co-train under episodic objective; $0 toy screens the interaction only).
- **source:** fleet-full 상시 discovery lane — objective-축(H_1841/H_1602) × architecture-축(H_1621 DEQ) **교차 미탐** (두 축 각각만 등록/시험됨, intersection=0 hits).
- **lens:** COGNITIVE × DYNAMICS — MLC episodic-remap objective (H_1841) × deep-equilibrium implicit-coupling mouth (H_1621, root-of-equation binding).
- **artifacts:** [] (미래 slug = `state/1842_mlc_episodic_deq_cross/`)
- **xref:** H_1841 (MLC objective standalone ⏳) · H_1621 (DEQ mouth standalone 🔵 pre-registered, unmeasured) · H_1602 (InfoNCE obj alone 🧱) · H_1449 (attention-block INERT@1blk)
- **key:** `mlc_episodic_deq_cross`

## Motivation

census 는 두 유망 미검 축을 **각각 따로** 남겼다: (1) objective-축 — MLC episodic-remap(H_1841, 암기 불가 데이터생성) · (2) architecture-축 — deep-equilibrium implicit-coupling mouth(H_1621, 조합을 fixed-point 로 표현). 그러나 **교차(objective × architecture)는 어느 카드도 측정 안 함**(ledger grep intersection=0). 가설: **에피소드마다 remap 되는 조합 알고리즘을 표현하려면 finite feedforward trunk 로는 부족하고, root-of-equation 반복정착(DEQ) 아키텍처가 있어야 objective 이득이 발현**된다 — objective 는 신호를 주지만 그 신호를 담을 **표현용량(fixed-point iteration)** 이 필요할 수 있다.

## Hypothesis

MLC episodic-remap objective(H_1841) 를 deep-equilibrium 결합 trunk(H_1621, `z* = f(z*, a, b)` bilinear-coupled Anderson solver) 위에서 학습하면, 두 축이 각각 단독으로는 floor/미검이던 것과 달리 **교차 셀에서만** G1 composed_distinct 가 baseline 을 초과한다. (2×2 factorial 의 결정적 셀: episodic-ON ∧ DEQ-ON.)

## Why orthogonal (재탕 아님 · 교차 미탐)

- H_1602 = InfoNCE objective × vanilla trunk → 🧱 floor.
- H_1621 = DEQ architecture × plain CE → 🔵 미측정(unmeasured).
- H_1841 = MLC episodic objective × vanilla trunk → ⏳ (이 배치에 신규 등록, 측정 전).
- **H_1842 = MLC episodic objective × DEQ architecture** → 교차 셀, ledger 에 실측·설계 모두 0. 이것이 "objective 가 architecture 를 요구하는가" 를 분리하는 유일한 카드.

## Frozen bar (pre-registered · tune-to-green 금지 · p7)

| Gate | Bar (측정 전 고정) |
|------|------|
| G1 RECOMBINATION | `composed_distinct ≥ 2` AND `> max_single` AND coherent, ≥2/3 seeds {7,4302,4303} |
| CROSS (decisive, 2×2) | (episodic-ON ∧ DEQ-ON) **strictly >** each of {episodic-ON∧DEQ-OFF, episodic-OFF∧DEQ-ON, episodic-OFF∧DEQ-OFF} on G1 best_distinct |
| DEQ ABLATION | solver iters=1 로 캡 → G1 collapse (iterative-settle 이 load-bearing double-dissociate) |
| held-out DESCENT | held-out 에피소드 support→query CE < ln256=5.545 |
| G0 pass | ≥4/5 (4000 step 필수) |
| G6 (side) | `dist≥5` AND `fals≥1` (보조) |

**Decisive INTERACTION:** 개별 축(H_1841 단독, H_1621 단독)이 floor 이고 교차 셀만 lift 해야 "objective × architecture 상호작용"이 성립. 교차도 floor 면 objective-lever 가설(레버=OBJECTIVE alone)이 재확정되며 그 자체가 유효 결과(c9).

## Cheap test (frozen-first · $0 · numpy DIRECTIONAL only)

numpy 2×2 toy: {episodic-remap ON/OFF} × {Picard-50-iter coupled-fixed-point / 1-iter feedforward}. held-out 에피소드 novel 조합 query. PRE-REG: 오직 (episodic-ON ∧ 50-iter) 셀만 descend. numpy mirror → **DIRECTIONAL, G1 verdict 아님**(a_engine_native_learning).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

303M canon 의 마지막 4 conv/attn block → 1 DEQ block(Anderson ≤12 iters, bilinear leg-coupling, param-matched, H_1621 recipe) + H_1841 episodic loader. total loss = CE_byte(query|support). arms at eval: episodic OFF, DEQ iters=1. backward = implicit-grad(1-step Neumann, flat memory). engine-native G1/G6 via `anima evaluate --py`. ckpt PULL before teardown. ~1–1.5 H100-day; explicit-go gated.

## Scope / honesty (c9)

설계만 — 측정 0. tier = ⏳ PROPOSED. frozen bar 사후이동 금지(p7). **정직 리스크:** 2-축 교차는 검정력 요구가 큼(4셀 × 3seed) — 교차 이득이 작으면 seed 노이즈에 묻힐 수 있음. 또한 H_1841·H_1621 각각이 단독 floor 면(likely, census objective-lever 수렴 감안) 교차가 초선형 이득을 낼 사전확률은 낮다 — 이 카드는 "objective 가 표현용량을 요구하는가"라는 특정 가설의 **결정적 반증기회**이지 green 예상이 아니다. H_1841 GPU 발사 후 그 결과에 조건부(H_1841 단독 floor 확인 시에만 교차 발사 가치) — sequential-gated. $0 toy 에서 교차셀-only-descend 못 보이면 GPU 미발사.
