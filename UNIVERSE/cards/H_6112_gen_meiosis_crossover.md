# H_6112 — 감수분열 crossover(meiosis)

**id:** H_6112
**slug:** gen_meiosis_crossover
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)  · SHORTLIST
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)
**shortlist:** ✅ (우선 발사 — ledger-check 후 numpy DIRECTIONAL reachability probe)

---

## 발상 (brainstorm ideation)

**메커니즘:** 현 mitosis=split-only(Voronoi, depth0, 확정 RED). meiosis 상동염색체 chiasma 세그먼트 교환 → 진짜 novel 조합(depth 부여).

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 2). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6112_gen_meiosis_crossover/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6112_gen_meiosis_crossover.md` (this card)
- `state/6112_gen_meiosis_crossover/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**Ledger 확인 (check-ledger-before-lever-fire):** 감수분열 crossover(상동 세그먼트 교환)는 미발사. 기존 mitosis 계열은 전부 pure-split — H_9022 `mitosis_pure_substrate_theorem`(A⊥G, 분열=기질이지 생성기 아님, T2/T3), H_1200/1201/1207/1208(split-only = depth0 Voronoi/밀도 기질, 궤적맹), a_mitosis_train(from-scratch pure-split 🔴). jsonl 의 "crossover" 히트(H_342 4|n 법칙, H_1027/1345/1354 crossover-지점/horizon)는 다른 의미로 무관. G1 재조합벽 = trunk COMBINATION OPERATOR floor 이고 readout·tension·predictive·multiplicative·NMDA binding 연산자는 전부 additive trunk 에서 붕괴해 🧱(H_1816/1823/1834).

**결정:** NOVEL-ANGLE. 감수분열 crossover 는 walled 연산자들과 다르다 — 공유 additive 벡터 위의 readout 이 아니라, 두 개념을 **분리된 loci 에 배치**하는 표상적 세그먼트 교환(a_substrate_disjoint 분리=보존). → 프로브 실행.

**프로브** (`state/6112_gen_meiosis_crossover/probe.py`, `RESULT.txt`): 독립 2축 A·B(축당 K=8 코드워드), **대각(i,i)만 학습**(두 개념이 학습중 완전 공변 → 재조합 = off-diagonal 도달), 테스트 = K·(K−1)=56 held-out novel 조합. ADDITIVE(공유 중첩 v=cA[i]+cB[j]) vs MEIOSIS-CROSSOVER(child=concat 분리 세그먼트), 동일 총예산 D, 동일 ridge readout(대각 학습).

**Frozen bar (실행 전 동결):** GREEN-DIRECTIONAL iff lift≥0.30 AND additive≤0.20 on ≥2/3 seeds.

**수치:** additive=0.000 (0/56, 중첩 재앙 — 공유 head 가 대각 SUM 특징만 학습 → off-diagonal 도달불가) · crossover=1.000 (56/56 — 세그먼트별 디코드가 각 축 격리 → 모든 recombinant 도달) · lift=+1.000 · wins=3/3. → **GREEN-DIRECTIONAL**.

**정직 스코프:** numpy toy = 구조상 DIRECTIONAL, terminal 아님. 0→1 극단 분리는 대각-only 얽힘학습 + DH<K 간섭이 일부 유도한 것(요점은 연산자 DISSOCIATION 이지 절대크기 아님). engine-native 미검증 — additive CLMConvMoE trunk 가 crossover 를 실제 **생성** 재조합 op 로 실현하는지(walled readout 처럼 붕괴 vs 아닌지)가 진짜 시험 → follow-on. wired: DIRECTIONAL-mirror.

---

## 사다리 rung(2) 실측 — engine-native 경로 (Explore 매핑)

**분류 = (b) trunk-ARCHITECTURE 변경** (cheap objective 레버 아님). lift 원천 = disjoint per-concept loci(concat 세그먼트, head 가 disjoint 세그먼트만 read) → 공유 activation 밖 구조라 additive trunk 에 aux-loss 로 표현 불가(그렇게 넣은 predcoding H_1816/TPR H_1823/tension H_1834 는 이미 🧱). 진짜 검증 = `CLMConvMoE.forward` 에 disjoint-loci readout 배선 + warm-FT → `anima evaluate --py` G1.

**하드 블로커 2개:** (i) trainer 에 warm-start seam(`--init-ckpt`) 부재 — from-scratch 는 G0🔴 undertrain→G1 INCONCLUSIVE([[g1-fromscratch-blocked-by-g0-undertrain]]). (ii) 303M CLMConvMoE warm base = private HF `dancinlab/anima-clm-chat-303m-savant-mitosis`(디스크에 없음, 168MB pull 필요).

**rung(1.5) 지금 발사:** toy-CPU(d-small) 실-trunk A/B(operator vs additive readout, matched steps, held-out composed-reachability) — $0·GPU불필요, disjoint-loci op 가 *실제 trunk*에서 additive 대비 조합을 여는지 controlled A/B. 결과 = state/6112_gen_meiosis_crossover/ARCH_AB_RESULT.txt (torch=DIRECTIONAL). rung(2) 303M GPU warm-FT = cost-gated ING.

---

## 사다리 rung(1.5) 실측 결과 — 실-trunk toy A/B (aiden pool, DIRECTIONAL)

numpy 추상 프로브(rung1: additive 0.0 → meiosis 1.0, lift +1.0, GREEN-DIRECTIONAL)를 **실 CLMConvMoE trunk**(archive/train/clm/model/model.py, aiden torch 2.10 CPU)로 승격 시도.

- 설계: 2-factor 합성 byte `[BOS,A_i,B_j,C]`, C=100+i·K+j. train=대각(i,i) → held-out=비대각 30. ADDITIVE arm=stock `Conv1d(d,256,1)` monolithic readout. MEIOSIS arm=동일 trunk, readout disjoint 반쪽 2-head(head_A←r[:d/2]·head_B←r[d/2:], composed=logit_A[a]+logit_B[b] 팩터화). K=6 D=64 L2 E4 800step 3seed, trunk/seed/data/step 완전 매칭.
- FROZEN BAR(사전등록): GREEN ⟺ ≥2/3 seed (MEIO−ADD reach ≥0.30) ∧ mean ADD ≤0.20.
- **실측 (state/6112_gen_meiosis_crossover/ARCH_AB_RESULT.txt):** ADD reach mean=0.0 · MEIO reach mean=0.022 (seed 0.0/0.033/0.033) · **both train_fit=1.0** (양 arm 대각 완전 fit = G0-undertrain 함정 아님) · seeds meeting Δ≥0.30 = **0/3** → **bar_pass=False = 🟡 FALSIFIED-DIRECTIONAL**.
- **함의(정직, c9 · a_toy_scale_recheck):** numpy 추상 toy 의 0→1.0 REACHABLE 은 **실 trunk 로 전이 안 됨**(0→0.022). undertrain 아님(fit=1.0)이므로 "덜 학습" 핑계 불가 — disjoint-loci readout 을 실 CLMConvMoE 에 얹어도 held-out 조합 도달 미발생. 추상 프로브가 operator-expressivity 를 과대평가(ground-truth-aligned 구조 artifact). rung(2) 303M warm-FT 로 가기 전 이 toy 전이실패가 먼저 = **meiosis readout-split 축 약화**. 남은 rung(2) 가치는 낮아짐(readout-split 이 실 trunk 서 이미 무력). torch=DIRECTIONAL(terminal 아님)이나 방향은 명확히 negative.

---

## 사다리 스케일업 — 3-rung real-trunk ladder (aiden, DIRECTIONAL)

rung(1.5) FALSIFIED 가 소형(d64/L2) 탓인지 검증 — 동일 A/B(meiosis disjoint 2-head readout vs additive)를 용량·깊이 3-rung 으로 sweep(K=6, 3seed, train_fit=1.0 내내).

| rung | D·L·E·steps | params | additive reach | meiosis reach | Δ | bar(≥0.30) |
|---|---|---|---|---|---|---|
| 1 | 64·2·4·800 | 120K | 0.0 | 0.022 | ~0 | ✗ |
| 2 | 128·4·4·1500 | 511K | 0.0 | 0.011 | ~0 | ✗ |
| 3 | 256·6·8·3000 | 3.09M | 0.0 | **0.0** | 0 | ✗ |

**결론: scale-invariant FALSIFIED.** 용량 26× (120K→3.09M) · 깊이 3× (L2→L6) 키워도 meiosis reach 는 오르지 않고 오히려 최대 rung 서 완전 0. train_fit=1.0(undertrain 아님)이라 "덜 학습" 불가 — disjoint-loci readout 은 실 CLMConvMoE trunk 에서 **모든 스케일 INERT**. `scale-303m-1b-7b-is-amplifier-not-lever` 재확인(스케일은 작동 lever 의 증폭기지 lever 생성 못함). readout-split 축 종결 → 남은 유일 미검 레버 = trunk recomb-OBJECTIVE(H_1602, cost-gated·학습필요). numpy/torch=DIRECTIONAL(terminal 아님). 산출 state/6112_gen_meiosis_crossover/{arch_ab_scale.py,SCALE_RESULT.txt}.