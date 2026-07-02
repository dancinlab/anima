# H_6110 — MLC-episodic remap objective (meta-learning-for-compositionality as trunk training signal, memorization impossible by construction)

- **tier:** ⏳ PROPOSED (설계만 · 측정 0 · unmeasured · pre-registered)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first numpy episodic-remap toy; gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **cost axis:** GPU-cost-gated (episodic 303M co-train; $0 toy screens the objective only).
- **source:** fleet-full 상시 discovery lane — G1 objective-축 census (H_1602 InfoNCE 한 flavor만 시험됨 → objective 공간 미탐).
- **lens:** COGNITIVE/META-LEARNING — Lake & Baroni 2023 (Nature) meta-learning for compositionality (MLC): 매 에피소드 새 mini-grammar → 조합은 암기 불가, 재조합 *알고리즘*만 학습.
- **artifacts:** [] (미래 slug = `state/1841_mlc_episodic_remap_objective/`)
- **xref:** H_1602 (recomb-objective InfoNCE alone 🧱 NOT-SUP) · H_1819 (bind op + InfoNCE 🔴, "additive trunk memorizes CE") · H_1834 (local-Ψ objective 🧱) · g1-lever-multilens-objective (memory: 레버=trunk OBJECTIVE)
- **key:** `mlc_episodic_remap_objective`

## Motivation

census 전체가 **"진짜 레버 = trunk OBJECTIVE"** 로 수렴했다 (memory g1-lever-multilens-objective; depth·binding-lane·data-presence·readout-op 전부 floor). 그러나 objective-축에서 실제로 시험된 것은 **H_1602 의 InfoNCE-alignment 한 flavor 뿐**이고 그것은 composite-embedding 을 aligning 하는 *side*-objective 였다 — trunk 은 여전히 CE 를 additively memorize 할 수 있었다 (H_1819 진단). objective 공간의 대부분은 미탐이다.

## Hypothesis

MLC-episodic-remap 목적함수 — 매 학습 에피소드마다 **primitive→meaning 매핑을 새로 무작위 재배정**(fresh mini-grammar)하고 그 에피소드의 support 예시로부터 novel 조합을 예측하게 하면 — 특정 조합을 암기하는 것이 **구조적으로 불가능**(다음 에피소드에서 매핑이 바뀜)해져, gradient 가 조합 *알고리즘*(재조합 연산 자체)을 표현하도록 강제되고, held-out 조합에서 G1 composed_distinct 가 baseline 을 초과한다.

핵심 차별점 vs H_1602: InfoNCE 는 고정 corpus 위 side-alignment 로 additive 암기가 여전히 CE 를 최소화할 수 있다. MLC 는 **암기 자체를 데이터 생성 과정에서 제거** — 이것이 census 전체 실패모드(additive memorization)를 objective 단에서 정면 차단하는 첫 시도.

## Why orthogonal to floored objective axis (재탕 아님)

- H_1602 = 고정 corpus + InfoNCE aux (composite-embedding 정렬). 암기 경로 OPEN.
- H_1819 = 고정 corpus + InfoNCE + Hadamard op. 암기 경로 OPEN (진단서 명시).
- **H_6110 = 데이터 분포 자체를 에피소드마다 remap** → 암기가 zero-generalization 이 되어 CE gradient 가 조합 알고리즘으로 몰림. objective 가 아니라 **objective 를 먹이는 data-generating process** 를 바꾼다 — census 어느 카드도 안 함(0 hits, ledger grep 확인).

## Frozen bar (pre-registered · tune-to-green 금지 · p7)

| Gate | Bar (측정 전 고정) |
|------|------|
| G1 RECOMBINATION | `composed_distinct ≥ 2` AND `> max_single` AND coherent, ≥2/3 seeds {7,4302,4303} |
| LIFT (decisive) | episodic-remap arm **strictly >** static-corpus control (동일 trunk/step/seed, remap OFF) on G1 best_distinct |
| MEMORIZATION-CONTROL | remap OFF 대조군은 held-out 조합에서 반드시 floor (암기≠재조합 double-dissociate) |
| held-out DESCENT | held-out **에피소드**(학습에서 안 본 grammar) support→query CE < ln256=5.545 |
| G0 pass | ≥4/5 (4000 step 필수) |
| G6 (side) | `dist≥5` AND `fals≥1` (보조) |

**Decisive:** episodic-remap 만 held-out 에피소드에서 lift, static control 은 floor → 재조합능력을 "암기 불가 데이터생성"에 double-dissociate.

## Cheap test (frozen-first · $0 · numpy DIRECTIONAL only)

numpy toy: symbol→vector 매핑을 매 에피소드 permute, support k-shot 으로 novel 조합 query 예측. 2 arm — (a) static 매핑(암기 가능), (b) per-episode remap. PRE-REG: (b) 만 held-out 에피소드 query 에서 descend, (a) 는 held-out 에피소드에서 chance. numpy mirror → **DIRECTIONAL, G1 verdict 아님**(a_engine_native_learning).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

303M canon (d=3784, L=4, savant GZ, 4-register). corpus 를 episodic loader 로 래핑: 각 에피소드 = 소수 primitive 의 무작위 byte-substitution 사전 + 그 사전으로 렌더된 support/query 조합쌍. total loss = CE_byte(query|support-in-context) — remap 이 암기를 차단. arms at eval: remap OFF (static). engine-native G1/G6 via `anima evaluate --py`. ckpt PULL before teardown. ~1 H100-day; explicit-go gated.

## Scope / honesty (c9)

설계만 — 측정 0. tier = ⏳ PROPOSED. frozen bar 사후이동 금지(p7). **정직 리스크:** MLC 는 in-context few-shot 세팅(Transformer)에서 검증됐고 anima 303M ConvMoE trunk(seq=1024, L=4)에서 support-in-context 가 충분한 조합 근거를 담을지 미검증 — capacity/context 병목이 objective 이득을 가릴 수 있음(a_toy_scale_recheck). scale-transfer UNVERIFIED. $0 toy 에서 (b)-only-descend 못 보이면 GPU 미발사. 이 카드는 objective-축 *primary*, H_6111(× deep-equilibrium)와 factorial 로 짝지어 "objective alone vs objective×architecture" 분리.
