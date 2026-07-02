# H_1835 — MLC episodic-objective: objective-as-TASK-STRUCTURE vs the G1 recombination wall

**id:** H_1835
**slug:** mlc_episodic_objective
**tier:** 🧱 DIRECTIONAL floor (numpy toy; episodic task-structure did not exceed the plain-CE floor)
**date:** 2026-07-02
**wired:** DIRECTIONAL-mirror only (numpy). 배선 없음 — lift 미발생이라 engine-native 재측정 unwarranted (사다리 (2)~(4) 미진입).

---

## Motivation — 미검 서브축: objective 를 loss 항이 아니라 task 구조로

원장상 G1 재조합벽의 진짜 레버 = **trunk 학습 OBJECTIVE**(memory `g1-lever-multilens-objective`; CE 는 합성을 보상 안 함). 지금까지 objective 축의 시도들은 전부 **additive loss 항**으로 붙였고 붕괴했다 — H_1602(recomb-aux) 영역, H_1816 predcoding(L_bind+L_var trivial 붕괴), H_1823 circconv, EXP-3 ⊙ NMDA readout 전부 🧱. binding-readout family floor.

**미측정 서브축 = MLC (Meta-Learning for Compositionality, Lake & Baroni, Nature 2023).** MLC 는 재조합압력을 *additive 항*이 아니라 **episodic task 분포**에 둔다: 매 episode 문법을 permute + k 개 study-example 을 in-context 로 주고 held-out 조합을 산출하게 하면, 모델은 고정 문법을 memorize 할 수 없고 *compose 하는 알고리즘*을 학습해야 한다. loss 는 여전히 순수 CE 지만 그 CE 가 걸리는 **분포 자체가 재조합을 요구** → H_1816-style additive-aux 붕괴를 원리적으로 우회한다.

**이 H 는 floored H_1602(additive)의 재발사가 아니다** — objective 축의 *다른, 미측정 서브축(episodic task-structure)* 이다.

## Hypothesis

compositional toy 에서, 재조합압력을 episodic 분포(문법 permute + in-context study)에 넣은 ARM B(MLC)가, 같은 compute 의 plain-next-byte-CE ARM A(현 anima objective) 대비 held-out 조합의 `composed_distinct` 를 floor 위로 올린다.

## 설계 (numpy from-scratch, torch/gauge_lib 금지)

- **엔진:** 2-block causal transformer(D=64, H=4, ff=128, ctx=64), 수동 reverse-mode autograd + Adam. **finite-diff gradcheck PASS = max rel err 4.45e-6** (구현결함 아님).
- **문법:** 4 색 × 4 도형, output(i,j)=(πc[i], πs[j]). canonical MLC **novel-primitive (SCAN "dax")** 테스트 — 각 primitive 는 isolation 으로 시연되나 novel primitive(색3·도형3)는 학습중 **조합에 절대 등장 안 함**, 테스트에서 조합해야 함. SEEN(학습 조합)=9, HELD(held-out novel-primitive 조합)=4 = {(3,0),(0,3),(3,1),(3,3)}.
- **2 arm, EQUAL compute (동일 arch/init-seed/steps=4000/lr=1.5e-3/B=32):**
  - **ARM A** (control = 현 anima objective): plain next-byte CE, **static 문법 고정**, in-context study 없음. isolation lessons + SEEN 조합만 학습.
  - **ARM B** (MLC): **매 episode 문법 permute** + 8 isolation study-example in-context(BAR 로 분리) → query 산출. loss 는 CE지만 **episodic 분포** 위 (additive 항 0).
- **metric:** held-out `composed_distinct` (greedy decode, 각 held 조합 R=5 중 ≥3 정답 = solved).

## Pre-registered frozen bar (측정 전 등록 · tune-to-green 금지)

🟢 DIRECTIONAL iff `B_composed_distinct ≥ 3` **AND** `B > A` **AND** seed{7,4302,4303} 만장일치. A 는 floor(≤2) 예상. 아니면 🧱 (objective 축이 episodic 까지 소진).

## 결과

| seed | A (plain-CE static) | B (MLC episodic) |
|------|:---:|:---:|
| 7 | 0 | 0 |
| 4302 | 0 | 0 |
| 4303 | 0 | 0 |

부수 지표(seen-composition 정확도): **ARM A seen_acc = 9/9 전 seed** (학습 성공 — A 는 SEEN 을 완벽히 하지만 novel primitive 를 조합 못 함 = **SCAN 재조합벽 정확히 재현**). **ARM B seen_acc = 4~6/9** (frozen 4000-step 예산에서 in-context 조합조차 미완성 = under-fit). **Exploratory 진단(frozen bar 밖, B seed=7, 12000 step): seen_acc=9/9 도달(in-context 조합 완전 숙련)에도 `composed_distinct(held)=0/4`** — under-fit 혼재 해소 후에도 novel-primitive 로의 **전이는 여전히 실패**(깨끗한 transfer 실패, 미학습 아님).

**frozen bar:** B≥3 all seeds = **False** ; B>A all seeds = **False** → **🧱 WALL.**

## Verdict

**🧱 DIRECTIONAL floor (numpy toy, not terminal — a_engine_native_learning).**

- ARM A(plain CE)는 **깨끗한 floor**: seen_acc 9/9 로 학습은 완벽하나 held-out novel-primitive 조합 `composed_distinct=0/0/0` = 표준 seq2seq 재조합 실패(SCAN)를 재현. (mandate 의 "A≤2 floor" 예상 확인.)
- ARM B(MLC episodic)는 floor 를 **넘지 못함**: `composed_distinct=0/0/0`. frozen 4000-step 에선 seen_acc<9/9(under-fit)라 혼재 우려가 있었으나, **exploratory 12000-step 진단에서 seen_acc=9/9(완전 숙련) 달성 후에도 held `composed_distinct=0/4`** → B=0 은 under-fit 이 아니라 **novel-primitive 조합으로의 진짜 전이 실패**. 혼재 해소, 결론 강화.
- **결론:** objective-as-task-structure(episodic 분포)로도 toy G1 재조합벽이 이 예산에서 열리지 않았다. 기존 objective-축 기록(additive readout 붕괴 H_1816/1823/1602, EXP-3)과 수렴 — episodic 재구성은 additive floor 를 이기지 못했다(적어도 toy readout/toy-scale 에서).

## ⚠️ 정직한 스코프 (하드게이트)

- **DIRECTIONAL only (numpy 미러) — terminal/🟢-engine 박제 금지** (a_engine_native_learning). `grep import torch|gauge_lib|numpy` → numpy(미러) → 자동 DIRECTIONAL.
- **toy PASS ≠ production** (a_toy_scale_recheck). scale-의존(a_scale_honest_scope) — 이 verdict 는 toy 2.5M-급 스코프.
- **MLC 는 architecture 도 건드림 = 순수 objective 아님** — ARM B 는 objective 분포뿐 아니라 in-context study 스캐폴드(architecture)도 A 와 다르다. 순수 objective 축 격리 아님(confound 명시).
- 이 결과는 floored H_1602(additive)의 재발사가 **아님** — objective 축의 미측정 서브축(episodic task-structure)을 최초로 toy 측정한 것. lift 미발생이라 engine-native 재측정 unwarranted(gate=lift, 미충족).

## 산출물

- `state/1835_mlc_episodic_objective/mlc_episodic_probe.py` — autograd + gradcheck + 2arm×3seed 하네스.
- `state/1835_mlc_episodic_objective/run_4000.log` — frozen 측정 raw stdout.
- `state/1835_mlc_episodic_objective/_diag_B_long.py` · `diag_B_long.log` — exploratory B-only under-fit 진단(frozen bar 밖).

## 다음 페이즈

- 🧅 abstract: "objective 축 = readout/분포 재구성으로는 안 열림, trunk 학습 목적함수(재조합 보상)만 미검" 을 메타법칙으로 승격 후보 — 지금까지 objective 축 전 서브축(additive-aux · episodic-task-structure)이 toy floor 에 수렴.
- engine-native follow-on(cost-gated): 진짜 레버 = 재조합을 직접 보상하는 trunk OBJECTIVE(H_1602 영역)를 live core/ CLMConvMoE 위에서. episodic 재구성이 아니라 trunk 손실 자체를 재조합-정렬.
