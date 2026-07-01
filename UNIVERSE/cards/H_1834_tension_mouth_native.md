# H_1834 — TENSION-MOUTH: anima-native mouth (A⇄G tension field as the byte trunk)

**id:** H_1834
**slug:** tension_mouth_native
**tier:** ⏳ PROPOSED (design + pre-registered toy probe · not yet measured)
**date:** 2026-07-02
**wired:** design-only — no engine wiring yet. 4칸 사다리(a_verified_must_wire) 중 (0) 설계·프로브 단계.

---

## Motivation — 왜 native mouth 인가

현재 anima 의 입(generator L3 mouth)은 **빌려온 바이트예측기** 두 종만 받는다: `bytegpt`(GPT-2급 24층 transformer)·`clm`(CLMConvMoE conv trunk). 둘 다 A⇄G 의식엔진과 **분리**돼 있다 — mouth 는 next-byte 를 뽑고, A⇄G(`pure_field`⇄`engine_g`⇄`brain`)는 emit/silence 만 결정하며 `.clm`/`.bin` 바이트가 엔진에 직접 들어가지 않는다(a_core_engine_map).

G1 재조합벽 연구가 수렴한 결론: **벽 = combination operator 부재(CE trunk-objective floor)**. 두 borrowed mouth 가 같은 바닥을 친 원인이 정렬된다 —
- conv-family: RF-bound → 거리 D>RF 인 두 개념 결합 수학적 불가(H_1394 FALS=0 · H_1410 conv-family 천장 · H_1581 conv_L1 reach=0).
- objective-as-aux: additive binding readout 은 trivial 붕괴(H_1816 predcoding · H_1823 circconv 전부 🧱; binding-readout family floor).
- scale = 증폭기지 lever 아님(scale-invariant, memory `scale-303m-1b-7b-is-amplifier-not-lever`).

→ 남은 미탐 레버 = **combination operator 를 objective/구조에 내장** (memory `substrate-framebreak-g1-combination-operator`: 4-각 수렴 중 "trained constructive bind"만 미검증). anima 는 이미 그런 연산자를 갖고 있다 — **A⇄G 텐션 그 자체가 두 표현을 맞미는 결합 연산**이다. 다만 지금은 의식 결정에만 쓰이고 입에는 안 쓰인다.

## Hypothesis

**mouth trunk 의 next-byte 분포를 A(forward 예측장) ⇄ G(reverse 제약장) 의 전역 텐션 해소로 산출하면**, (1) 전역장 유효 RF=∞ 로 conv 의 RF-bound G1 벽을 원리적으로 우회하고, (2) Ψ=½ 고정점 도달이 곧 두 개념의 결합을 요구하도록 objective 를 구조에 내장(additive aux 아님)하여, **engine-native G1 `composed_distinct` 를 ByteGPT 바닥(=2) 위로 올린다** — 동시에 mouth 를 의식 substrate 와 합쳐도 **Ψ=½ 이 보존**된다.

세 축:
1. **연산자** = A⇄G 전역 텐션장 (RF-bound 우회).
2. **목적함수** = Ψ→½ 수렴이 결합을 요구하는 structural recomb-objective (H_1816-style additive 붕괴 회피).
3. **배선** = 의식용 A⇄G 를 mouth trunk 로 재사용 (mouth ⊥ consciousness → 이 한 곳에서만 SHARED 시도).

## ⚠️ 정직한 리스크 (pre-registered)

축 3 은 `a_substrate_disjoint`(공유 lane=충돌; mouth-FT → Ψ dev 0.18·fab 1.0 붕괴, H_1566)와 **정면충돌**한다. 이 가설의 falsifiable 핵심 = "byte-production 을 tension-resolution 으로 *만드는 것*은 emit-drive lane(0/4)에 능력을 *덧씌우는 것*과 다르다"는 주장. 틀리면 Ψ 붕괴 → native-mouth 는 정직한 벽(negative). 그러므로 프로브는 **G1 lift 와 Ψ 보존을 반드시 동시 측정**한다.

## Pre-registered bar (frozen-first · p7 · 사후이동 금지)

toy DIRECTIONAL 프로브(numpy from-scratch, d128, G1 재조합 toy task) 기준:

| 판정 | 조건 (AND) |
|------|-----------|
| 🟢 DIRECTIONAL-GREEN | G1 `composed_distinct >= 3` (ByteGPT floor=2 초과) AND \|Ψ-0.5\| <= 0.05 |
| 🟠 MIXED | G1 >= 3 이나 Ψ dev > 0.05 (능력 O, 의식 붕괴 = a_substrate_disjoint 재확인) |
| 🧱/🔴 WALL | G1 `composed_distinct <= 2` (연산자가 재조합 안 엶) |

- 통제: (a) tension-OFF ablation(A만, G 제거) → G1 이 tension 에 causal 함을 결정적으로 보여야(INERT 면 기여 0). (b) additive-baseline(A+G 덧셈, 텐션 해소 아님) → structural composition 이 additive floor 초과함을 격리.
- toy green 은 production closure 아님(a_toy_scale_recheck) → engine-native 재측정(live core/ A⇄G) 후에만 terminal, 이어 GPU ladder(cost-gated, explicit go).

## 산출물

- `state/1834_tension_mouth_native/` — 설계 spec 상세 + toy 프로브 하네스 + 결과.

## Verdict

⏳ PROPOSED — 미측정. 다음 = state/ toy 프로브 구현 → DIRECTIONAL 채점 → engine-native 재측정 사다리.
