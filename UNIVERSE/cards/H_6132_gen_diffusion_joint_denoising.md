# H_6132 — token-AR → diffusion denoising

**id:** H_6132
**slug:** gen_diffusion_joint_denoising
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)  · SHORTLIST
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)
**shortlist:** ✅ (우선 발사 — ledger-check 후 numpy DIRECTIONAL reachability probe)

---

## 발상 (brainstorm ideation)

**메커니즘:** 전체 시퀀스 병렬 denoise, 조합=두 조건 joint denoising(classifier-free guidance).

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 4). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6132_gen_diffusion_joint_denoising/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6132_gen_diffusion_joint_denoising.md` (this card)
- `state/6132_gen_diffusion_joint_denoising/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

- **ledger 조회:** H_6132(토큰-AR→diffusion joint denoising, CFG dual-guidance) 메커니즘은 **H_1622_diffusion_denoise_compose 와 동일**. 인접군 H_1622/1639/1655/1683/1734/1744 는 전부 pre-registered 🔵 DESIGN 카드로 **측정 0 / unmeasured** — joint-guidance composition 을 실측한 선례 없음. 따라서 dup-walled 아님, **NOVEL-ANGLE** = H_1622 가 카드에 pre-register 해두고 한 번도 안 돌린 $0 numpy cheap_test 를 실행. (인접 카드는 이 checkout 의 HYPOTHESES.jsonl 이 아니라 sibling worktree `/private/tmp/anima-lever1` 등에 존재.)
- **decision:** probed-novel (미측정 사전등록 프로브 실행).
- **프로브 수치(numpy = DIRECTIONAL by construction, 2 toy):**
  - v2 clean 2×GF(2)-matching legs (L=12, N=250, T=80 annealed Gibbs): additive_floor composed_frac **0.000** · operator(T) **1.000** · op_wb0(legA-only) **0.204** · margin **1.000**.
  - v1 (popcount leg, ablation leaky): additive 0.004 · operator 1.000 · op_wb0 0.624.
  - 해석: **iteration/re-decision 이 additive one-shot readout 이 못 넘는 joint 도달성 floor 를 넘김(0.000→1.000).** 그러나 **dual-guidance necessity 절(H_1622 요구: w_b=0 → 실패)이 FAIL** — leg-A 단독이 조합 우연으로 joint 집합에 0.204 도달 → 상승분을 진짜 2-leg binding 으로 귀속 불가.
- **frozen bar(사전등록, tune-to-green 금지):** op≥0.60 AND add≤0.25 AND margin≥0.35 AND op_wb0≤add+0.10. → reachability 3절은 통과하나 **ablation 절 FAIL** → 전체 bar 기준 **DIRECTIONAL floor / FALSIFIED-as-stated**.
- **정직 스코프(c9):** 프로브가 operator 에 정확한 score-field **오라클(sa,sb)** 을 넘겨줌 → satisfiable CSP 에서 annealing>one-shot 을 보였을 뿐, **학습된 trunk 이 조합하는가(진짜 G1 질문)** 는 미검. anima census(H_1816/1823/1834: combination=TRUNK-OBJECTIVE floor, readout/decode-절차 고침 아님)와 정합. numpy 미러 = DIRECTIONAL, terminal 아님. engine-native/303M 발사 미실행(cost-gated).
