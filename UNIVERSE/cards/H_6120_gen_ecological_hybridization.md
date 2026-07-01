# H_6120 — 생태 hybridization

**id:** H_6120
**slug:** gen_ecological_hybridization
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** disjoint lane 둘의 hybrid lane 이 부모에 없던 형질(조합) 담당.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 2). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6120_gen_ecological_hybridization/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6120_gen_ecological_hybridization.md` (this card)
- `state/6120_gen_ecological_hybridization/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**Ledger 조회 (check-ledger-before-lever-fire):** H_6120 "생태 hybridization" 의 메커니즘 = *disjoint lane 둘의 hybrid lane 이 부모에 없던 조합 형질 담당* 은 이미 측정된 **disjoint-loci / segment-concat 조합 연산자 family** 와 동일 좌표다:

- **H_6112 감수분열 crossover** — 두 개념을 분리 loci(concat 세그먼트)에 배치 → numpy 추상 toy REACHABLE 0→1.0, **그러나 실 CLMConvMoE trunk A/B(`state/6112_gen_meiosis_crossover/arch_ab.py`·`ARCH_AB_RESULT.txt`) = 🟡 FALSIFIED-DIRECTIONAL: disjoint-loci 2-head readout reach 평균 0.022 ≪ 0.30 frozen bar, 0/3 seed, train_fit=1.0(undertrain 아님)**. H_6112 verdict 가 명시: "arch-변경 계열(H_6139 suture-VDJ)도 동일 전이위험 재평가 필요".
- **H_6139 봉합-VDJ** — 이산 select+splice, toy 18/18 REACHABLE 이나 transfer-unverified(같은 disjoint-구조 family).
- **H_6104 A⇄G 제약 교집합** — 독립(직교) 개념 regime 에서 constraint-conjunction = additive 와 대수적으로 동일 → INERT 🧱 floor.
- 상위 진단: G1 재조합벽 = **trunk COMBINATION OBJECTIVE floor**, readout/decode-절차 고침 아님(H_1816/1823/1834; `substrate-framebreak-g1-combination-operator`). a_substrate_disjoint "분리=보존" 을 combination 에 적용해도 trunk objective 를 안 바꾸므로 벽 상속.

**결정: DUP-WALLED.** hybrid-lane = 두 disjoint 부모 lane 을 읽어 조합코드를 담는 세 번째 lane = by-construction concat/disjoint-read = **H_6112 meiosis 와 동일 연산자 class**. 신규 numpy 프로브를 돌리면 (concat 은 자명히 compositional) ~1.0 toy 를 재생산 → H_6112 가 이미 반증한 "추상 toy 과대평가" 함정 재발. 따라서 **재발사 안 함**(sweep 빈칸 아님, 측정된 family).

**Bar (참조, H_6112 frozen):** GREEN-DIRECTIONAL iff ≥2/3 seed delta≥0.30 AND additive≤0.20 — 실 trunk 에서 0.022 로 미달.

**정직 스코프 (H_6112 transfer caveat):** numpy 추상 toy 는 구조상 disjoint-concat 조합을 항상 REACHABLE 로 과대평가한다(H_6112 = toy 1.0 → real-trunk 0.022). 이 축의 fresh numpy REACHABLE 은 green light 가 아니라 weak screen 일 뿐이고, 이미 real-trunk 반증이 존재하므로 신규 프로브 가치 없음. 진짜 레버는 hybrid-lane readout 배치가 아니라 trunk recomb-objective(H_1602 영역, 이미 🧱) / 미검증 γ trained-constructive-bind(cost-gated). numpy=DIRECTIONAL, terminal 아님(엔진-native 벽은 trunk-objective floor 로 유효).

---

## 심화 (adversarial multi-lens)

**대상 연산자 재도출:** hybrid-lane = "두 disjoint 부모 lane 을 읽어 부모에 없던 조합코드를 담는 세 번째 lane" = by-construction `concat(parentA, parentB)` + per-segment readout = **H_6112 meiosis-crossover 와 byte-동일 연산자 class**(`state/6112_gen_meiosis_crossover/probe.py`: child=concat(cA[i],cB[j]), headA←seg1·headB←seg2). dup 포인터 검증됨.

**controls (`state/6120_gen_ecological_hybridization/deepen.py`·`DEEPEN_RESULT.txt`, numpy, 3 seed, off-diag/seed=56):**

| 렌즈 | reach | 판정 |
|---|---|---|
| ADD baseline (shared 중첩) | 0.000 | floor |
| HYBRID (concat/disjoint-read) | 1.000 | target REACHABLE |
| **C1** generic tanh over **같은 disjoint** | **1.000** | ⚠️ 동률 MATCH |
| **C1** random-proj MLP that **MIXES** segments | **0.000** | 붕괴 |
| **C1** elementwise A*B (shared) | 0.000 | floor |
| **C2** bind-recoverability (C→A_idx, C→B_idx, held-out) | 1.000 | trivial (=hybrid readout) |
| **C3** disjointness-ablation (segment→shared 합) | 0.000 | 붕괴 |

**frozen bar(실행 전 동결):** 연산자 SURVIVE ⟺ (generic NOT match) ∧ (recov lift≥0.30 nontrivial) ∧ (ablation collapse). → **C1 generic tanh 가 hybrid 와 1.000 동률 = generic MATCH → bar FAIL.**

**정직한 결론 — ARTIFACT (+ DUP-CONFIRMED):** numpy REACHABLE(0→1.0)은 "생태 hybrid-lane" 메커니즘이 아니라 **disjoint-partition STORAGE** 의 성질이다 — 같은 disjoint 좌표 위 아무 generic 비선형(tanh)이 동일하게 도달한다. 결정적 대조: 세그먼트를 **실제로 섞는**(=진짜 binding/composition 이 하는 일) random-MLP-mix 는 0.000 으로 붕괴하고, disjointness 를 끄는 ablation(C3)도 0.000. 즉 **도달성은 '부모를 섞지 않고 분리 보관' 할 때만 살고, 섞는 순간(=조합) 죽는다** → concat 은 조합 연산자가 아니라 partitioned 저장. C2 recoverability=1.0 도 저장이라 trivial(necessary-not-sufficient). 이는 H_6112 가 실 CLMConvMoE trunk(conv-mix + shared readout = 섞는 구조)에서 reach 0.022(0/3 seed, train_fit=1.0)로 FALSIFIED 된 것과 정확히 정합 — 실 trunk 는 mix 하므로 storage 트릭이 안 통한다.

**H_6112 transfer caveat:** numpy 추상 toy 는 disjoint-concat 을 항상 1.0 으로 과대평가한다(H_6112 toy 1.0 → real-trunk 0.022). 본 심화는 그 과대평가가 *왜* vacuous 한지를 controls 로 규명(storage≠composition). 따라서 재발사 무가치, DUP-WALLED 결정 유지·강화. 진짜 G1 레버는 lane 배치가 아니라 trunk recomb-objective(H_1602, 이미 🧱) / 미검증 γ trained-constructive-bind(cost-gated). numpy=DIRECTIONAL, terminal 아님(엔진-native 벽=trunk-objective floor).

**RESIDUAL(잔여):** 없음 — hybrid-lane 축이 시험할 수 있는 disjoint-loci readout 은 H_6112 가 실-trunk 에서 이미 소진. 미검증으로 남는 것은 이 축이 아니라 trunk-objective 축(H_1602 영역).
