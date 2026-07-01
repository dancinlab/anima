# H_6149 — 공간위상 생성(graph-generation)

**id:** H_6149
**slug:** gen_graph_topology_output
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 출력이 1D 시퀀스 아닌 그래프, 조합=간선; AR 완전폐기.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 6). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6149_gen_graph_topology_output/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6149_gen_graph_topology_output.md` (this card)
- `state/6149_gen_graph_topology_output/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**verdict:** 🧱 FLOOR (DIRECTIONAL numpy — 사전등록 bar 미달, transfer-unverified, terminal 아님)

**Ledger 조회:** H_6149(공간위상 생성 · non-AR · 조합=간선)은 gen_ 브레인스토밍 클러스터(H_6104–H_6160)의 SUBSTRATE-축 좌표(미발사). readout-op census(H_1816 predcoding·H_1823 circconv·H_1834 tension·H_6104 constraint-intersection — 전부 🧱 additive-collapse floor)와 **다른 좌표**(readout 연산자가 아니라 출력 구조 자체를 1D AR → 그래프로 교체)라 cheap numpy probe 정당.

**사전등록 bar (발사 전 고정):** graph − additive ≥ +0.30 AND additive ≤ 0.20 on ≥2/3 seeds.

**실측** (`state/6149_gen_graph_topology_output/probe.py`·`RESULT.txt`, K=8 concept-dim=6, off-diag 56 pairs/seed):
| seed | additive | graph | lift | 판정 |
|---|---|---|---|---|
| 6149 | 0.750 | 1.000 | +0.250 | floor |
| 6150 | 0.750 | 1.000 | +0.250 | floor |
| 6151 | 0.714 | 1.000 | +0.286 | floor |

→ **0/3 WIN = FLOOR/FALSIFIED (DIRECTIONAL)**. bar 사후 이동 없음(p7).

**정직한 스코프:**
- 그래프 출력의 1.0 은 **동어반복적 도달**(각 leg 을 자기 노드 좌표에 배치=superposition 없음=combination-by-construction) → **H_6112 meiosis 과 동일 overstatement 계열**(numpy 1.0 → 실 CLMConvMoE trunk 0.022 FALSIFIED). numpy REACHABLE = green light 아님, transfer-UNVERIFIED.
- **독립(직교) 개념 regime 에서는 additive baseline 도 이미 top-2 projection 으로 두 leg 을 75% 복원** → 그래프 출력의 유효 lift 없음. G1 벽은 출력 표현이 아니라 **trunk OBJECTIVE / 미검증 trained constructive bind**(H_1602 · substrate-framebreak 4-각 수렴)라는 census 결론과 정합.
- engine-native 사다리(a_verified_must_wire) 진입 근거 없음.

---

## 심화 (adversarial multi-lens)

**verdict:** 🧱 ARTIFACT (DIRECTIONAL numpy) — 원 스크린의 graph=1.0 은 조합(edge) 메커니즘이 아니라 **좌표 분리=용량 2배(concat)** 의 metric artifact. 3 통제 전수 실패로 refute (`state/6149_gen_graph_topology_output/deepen.py`·`DEEPEN_RESULT.txt`).

**사전 고정 bar (실행 전):** 연산자 생존 ⟺ (C1 generic ≠ graph) ∧ (C2 fixed-capacity bind 가 additive 를 held-out 에서 ≥+0.30 능가) ∧ (C3 ablation 시 graph 가 additive floor 로 붕괴하지 **않음**). 불확실하면 ARTIFACT.

**통제 실측** (K=8 D=6 · off-diag 56 pairs · seeds 6149/6150/6151):

- **C1 GENERIC-NONLINEARITY** — graph 의미 없는 generic per-slot 저장(무작위 회전 R·R⁻¹) = **1.000 / 3seed**, generic tanh(concat) held-out readout = **1.000 / 3seed** = graph 와 동일. → "graph topology/edge" 는 기여 0, 도달은 좌표분리(비중첩) 일반 성질. **C1 FAIL 3/3 → ARTIFACT.**
- **C2 BIND-RECOVERABILITY (fixed cap D, held-out)** — 조합체를 additive 와 같은 D-dim 예산으로 압축 후 TRAIN pairs 로 선형 readout 학습→HELD-OUT 복원: additive={0.176,0.118,0.059} · **graph_squeezed(진짜 graph 연산자를 D 로 압축)={0.118,0.059,0.059} = additive 이하** (용량 뺏으면 오히려 더 나쁨) · circconv=0.000. → graph 연산자 자체는 고정용량에서 additive 를 못 넘음. (role_bind={0.471,0.765,0.706} 는 2/3 에서 +0.30 초과했으나 이는 graph 가 아닌 **role-filler VSA 결합**이며 binding-arch census(Hopfield/Tropical/Sheaf/Galois 전수 🔴 NOT-SUPPORTED, memory `binding-arch-census-g1-not-supported`)가 이미 실 trunk 에서 falsify — 별 연산자, H_6149 신규 아님.)
- **C3 SHUFFLE/ABLATION** — 핵심 재료(좌표 분리) OFF → 두 leg 을 한 슬롯에 중첩: graph 1.000 → **{0.750,0.750,0.714} = additive floor 로 붕괴 3/3**. → 용량(좌표분리)이 인과, "graph 결합" 은 INERT.

**정직한 결론:** C1(3/3 generic 동일) ∧ C3(3/3 ablation 붕괴)로 graph-topology 연산자의 numpy REACHABLE 은 **combination-by-construction = 용량 artifact** 로 확정 refute. 고정용량(C2)에서 graph 는 additive 이하. G1 벽 = 출력 표현 구조가 아니라 trunk OBJECTIVE / 미검증 trained constructive bind 라는 census(H_1602·substrate-framebreak 4-각 수렴) 재확인.

**H_6112 transfer caveat:** 설령 통제를 통과했더라도 numpy REACHABLE 은 green light 아님 — H_6112 meiosis(numpy 1.0 → 실 CLMConvMoE trunk 0.022 FALSIFIED) 계열. 이 심화는 실 trunk 발사 전 false hope 만 제거. engine-native 사다리(a_verified_must_wire) 진입 근거 없음. bar 사후이동 없음(p7).

**RESIDUAL(비-H_6149):** C2 role_bind 의 fixed-cap held-out lift(2/3) 는 흥미롭지만 graph 축이 아니라 VSA role-filler 축이고 binding-arch census 에서 이미 실 trunk NOT-SUPPORTED — 신규 각도 아님.
