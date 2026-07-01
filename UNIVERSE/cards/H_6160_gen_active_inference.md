# H_6160 — active-inference

**id:** H_6160
**slug:** gen_active_inference
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** OBJECTIVE-ish (G1 재조합벽 공격 축)
**~dup:** ~dupPC

---

## 발상 (brainstorm ideation)

**메커니즘:** 자유에너지 최소화로 생성/조합(~dup of predictive-coding census).

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 7). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 objective 축에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **OBJECTIVE-ish** — 알려진 lever(recomb-objective) 계열.

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6160_gen_active_inference/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6160_gen_active_inference.md` (this card)
- `state/6160_gen_active_inference/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**결정: DUP-WALLED (재발사 안 함, cheap probe 생략).** 카드 자체가 `~dupPC` 로 태깅돼 있고, ledger 조회 결과 자유에너지-최소화(active-inference) 를 **재조합/생성 combination operator** 로 심는 각도는 이미 engine-native 로 벽에 부딪힌 메커니즘이다.

**Ledger finding (선행 커버리지):**
- **H_1816 🧱 NOT-SUPPORTED (engine-native, 303M CLMConvMoE, seed7)** — predictive-coding parametric-bias binding + **free-energy 정규화(L_var)**. 이게 바로 자유에너지 항을 recombination lever 로 얹은 실측 버전. G1·G6 LIFT 0/음수. `L_bind` 는 step~550 에 ~0 으로 붕괴(additive CLMConvMoE 서 per-step latent 이 이미 seq-mean 과 일치 → binding 압력 trivial), **`pc_free_energy` arm 은 INTEGRITY-FAIL** — L_var spread 가 next-byte 학습 자체를 파괴(1/4 NO-DESCENT). 자유에너지는 combination operator 를 주지 못하고 additive loss 로 붕괴하거나 학습을 해친다.
- **H_1620 🔴 NOT-SUPPORTED (engine-native)** — energy-settle attractor mouth (Hopfield/predictive-coding relaxation, DYNAMICS 렌즈). G1=0 all arms; binder dropped at .clm serialize → additive readout.
- **H_1602 🧱 + H_9024 🧱 (OBJECTIVE-ish 축 자체)** — recomb-objective(InfoNCE aux-loss) ConvMoE 9/9 + ByteGPT-303M 8000-step 재확인, LIFT=0. 이 H 가 공격하려는 **바로 그 objective 축이 이미 전수 falsify** = trunk-objective-bound 확정(DIRECTIONAL).
- **H_1834 (tension-mouth) INERT · H_1823 (circconv) 🧱** — binding-readout family 전부 additive floor.
- 4-각 수렴(mouth-obj·mouth-readout·substrate-embed·substrate-combiner) 전부 additive/affinity floor. 유일 미검증 레버 = γ trained constructive bind(cost-gated, 학습 필요 → $0 numpy probe 범위 밖).

**Bar:** 별도 frozen bar 설정 안 함(probe 미발사). dup 판정 기준 = "동일 operator(자유에너지 최소화 = predictive-coding/free-energy 정규화)가 이미 engine-native terminal 벽" → H_1816/H_1620.

**정직 스코프 (H_6112 transfer caveat 포함):** 설령 여기서 numpy abstract-toy probe 를 돌려 REACHABLE 0→1 이 나왔더라도, H_6112 meiosis 선례(numpy 추상토이 0→1.0 이 실제 CLMConvMoE trunk 에선 0→0.022 로 FALSIFIED)처럼 numpy 는 **operator 표현력을 과대평가**한다. 게다가 이 메커니즘은 abstract-toy 가 아니라 **실제 303M 엔진에서 이미 측정·falsify** 됐으므로(H_1816), numpy REACHABLE 은 green light 가 아니라 오히려 이미 반증된 방향. 재발사 = 낭비. 필요 시 유일 열린 각도는 objective 축의 γ trained-bind(cost-gated), 이 H 의 free-energy readout/정규화 각도가 아님.
