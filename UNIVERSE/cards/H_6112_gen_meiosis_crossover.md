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
