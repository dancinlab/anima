# H_6113 — 화학 결합가(valence)

**id:** H_6113
**slug:** gen_chemical_valence_bond
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 개념=결합가 보유 원자, 조합=상보 valence 결합, 생성=반응 네트워크.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 2). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6113_gen_chemical_valence_bond/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6113_gen_chemical_valence_bond.md` (this card)
- `state/6113_gen_chemical_valence_bond/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**decision: DUP-WALLED (probe 미발사).**

**ledger finding:** H_6113(상보 valence 결합 → 반응 네트워크 생성)의 조합 연산자는 *구성적/typed binding-operator* 계열이다. 이 계열은 이미 engine-native 로 walled:
- **H_1823 circconv**(구성적 circular-convolution bind) = 🧱 NOT-SUPPORTED
- **H_1816 predictive-coding binding** = 🧱 NOT-SUPPORTED
- **H_1834 TENSION-MOUTH** = 🧱 DIRECTIONAL floor — H_6113 과 **동일 세션·동일 발상 출처**(anima-native mouth, Round 2). substrate-level 연산자도 composed_distinct=0, 연산자 INERT(FULL=OFF=ADDITIVE).
- **framebreak 4-각 수렴**(substrate-framebreak 메모리): mouth-objective·readout-op·substrate-embed·substrate-combiner **넷 다 additive/affinity floor**. 유일 미검증 레버 = *학습된* constructive bind + **trunk recomb-OBJECTIVE**(γ, cost-gated, 학습 필요 → $0 numpy 로 판정 불가).

**decision 근거:** 상보-valence를 **고정 규칙**으로 심으면 walled binding-operator 계열에 그대로 포함되고(readout/substrate 좌표 무관 — H_1834 가 substrate 좌표도 floor 임을 이미 측정), **학습 objective**로 승격하면 cost-gated γ 레버(OFF-TRUNK, numpy screen 불가)로 붕괴한다. 어느 쪽도 새 $0 신호 없음.

**bar / 수치:** probe 미발사(수치 없음). frozen bar 는 선행 walled 측정에 위임.

**정직 스코프 (H_6112 transfer caveat):** 설령 numpy 추상 toy 를 돌렸어도 상보-valence 는 구성적 binding 이라 REACHABLE(0→~1.0) 이 거의 확실하지만, **H_6112 meiosis 가 정확히 그 패턴(numpy 0→1.0 REACHABLE → 실 CLMConvMoE trunk 0→0.022 FALSIFIED)** 을 보였으므로 numpy REACHABLE 은 green light 가 아니라 **추상 toy 과대평가**의 재현일 뿐이다(a_toy_scale_recheck). 따라서 WEAK screen 조차 무의미 → dup-pointer 로 기록. terminal 아님(numpy=DIRECTIONAL by construction).

---

## 심화 (adversarial multi-lens)

**타깃:** H_6113 상보-valence 결합 = 구성적/typed binding-operator (개념=원자, 조합=상보 valence 결합, 생성=반응 네트워크). 카드 verdict = 🟡 DIRECTIONAL — DUP-WALLED (probe 미발사).

**심화 목적 (a_break_the_wall):** numpy REACHABLE 은 대안을 죽이기 전엔 confident 아님. H_6112 선례(numpy 0→1.0 REACHABLE 이 실 CLMConvMoE trunk 에서 0→0.022 붕괴)를 근거로 이 신호가 metric artifact 인지 adversarial control 로 반증 시도.

**probe:** `state/6113_gen_chemical_valence_bond/deepen.py` (numpy toy, D=64, 400 pairs, seed=6113, OMP=4, <1s). valence-bind = circconv(donor(A),acceptor(B)) + circconv(donor(B),acceptor(A)) — H_1823 의 순환합성곱 primitive 그대로. FROZEN bar (실행 전 고정): 생존 iff B1∧B2∧B3∧B4.

**측정 (verbatim):**

| op | distinct | recover_R2 |
|---|---|---|
| valence | 0.9241 | **−0.4653** |
| valence_ABL (상보 OFF) | 0.9124 | −0.4389 |
| additive (floor) | 0.2907 | +0.2566 |
| tanh(A+B) | 0.2896 | +0.2567 |
| A*B | 0.8912 | −0.4553 |
| randproj | 0.9384 | +0.3664 |

**controls:**
- **C1 GENERIC-NONLINEARITY — FAIL (¬B1):** 일반 randproj(0.9384)·A*B(0.8912) 가 valence(0.9241) 의 composed_distinct 를 그대로 매칭/초과. → 높은 distinct 는 상보-valence 메커니즘이 아니라 *비선형/랜덤 믹싱 일반*의 성질 (gap=−0.0143).
- **C2 BIND-RECOVERABILITY — FAIL (¬B2):** held-out 에서 C→A, C→B 선형 복원 R2 = valence **−0.4653** (평균예측보다 나쁨) vs additive +0.2566. 부모를 valence 합성에서 되찾을 수 없음 = 정보 파괴 = **anti-compositional** (gap=−0.7219, 요구 +0.15).
- **C3 SHUFFLE/ABLATION — FAIL (¬B3):** 핵심 성분(상보 donor↔acceptor pairing)을 끄면(donor-donor) distinct 0.9124 ≈ FULL 0.9241, additive floor(0.2907)로 붕괴 안 함(|Δ|=0.6217). → distinctness 는 상보성이 아니라 circconv 스캐폴드에서 나옴 = INERT (FULL==OFF).

**정직한 결론:** 세 축 전부 신호를 반증 — composed_distinct REACHABLE 은 순수 metric artifact (비선형-일반 + 부모정보 파괴 대가). 내가 쓴 순환합성곱 primitive 는 **H_1823 circconv 와 동일**(engine-native 🧱 NOT-SUPPORTED). dup pointer(H_1823 circconv · H_1816 predictive-coding binding · H_1834 tension-mouth, 공유 실패모드 = "operator INERT: FULL==OFF==ADDITIVE floor on real CLMConvMoE trunk") **성립 → DUP-CONFIRMED**. RESIDUAL 없음: 유일 미검증 레버(학습된 constructive bind + trunk recomb-OBJECTIVE γ)는 이미 family-wide 로 flag 됐고 학습 필요 → $0 numpy 로 판정 불가.

**H_6112 transfer caveat:** 설령 이 numpy 가 clean 0→1.0 을 냈어도 그건 green light 가 아니라 H_6112 meiosis 가 보인 추상 toy 과대평가(numpy 0→1.0 → 실 trunk 0→0.022)의 재현일 뿐. 여기선 adversarial control 이 numpy 단계에서 이미 artifact 를 잡아냄 — 실 trunk rung 발사 불필요. terminal 아님(numpy=DIRECTIONAL by construction)이나 dup 은 engine-native 선행 측정에 위임되어 확정.
