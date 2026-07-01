# H_1840 — γ trained-constructive HRR bind (circular-convolution as gradient-trained trunk combiner, additive-bypass DENIED)

- **tier:** 🧱 DIRECTIONAL — **STAGE-1 FAIR (non-rigged) cheap-gate FROZEN BAR FAIL 0/3** (2026-07-02, aiden pool CPU $0). The distilled surviving delta — **bypass-denied bilinear bottleneck (invertibility-agnostic)** — is now **measured-FALSIFIED as a G1 lever** on a FAIR operator-agnostic target; STAGE-2 engine-native GPU run **NOT authorized** (pre-registration honored, p7). **G1 recombination wall CONFIRMED (DPI meta-law) — all local + cheap levers exhausted.** Full result = `state/1840_gamma_hrr_constructive_bind/RESULT_fair.md` (prior RIGGED gate = `RESULT.md`).
- **wired:** DIRECTIONAL-mirror (torch toy, a_engine_native_learning — no engine-native measurement, no terminal G1 verdict). STAGE-1 FAIR cheap_test = RAN (FAIL); STAGE-2 gpu_recipe = NOT fired (fair gate denied it). No surviving local lever.
- **STAGE-1 FAIR gate (frozen-first, DIRECTIONAL — supersedes RIGGED PR#2689 gate):** the old toy target `K=circ_conv(A,B)` MATCHED the HRR operator (pure operator↔algebra match, non-transferable). NEW fair target = random NON-additive 2-way latent-interaction table `T[fa,fb]` over random class keys (C=9, chance 0.111) — no arm's operator equals T. 5 arms × seeds {7,4302,4303}, held-out combination retrieval. heldout_acc: (a)additive 0.45/0.47/0.60 · (b)hadamard+bypass-OPEN(=H_1819) 0.66/0.67/0.73 · (c)hrr-⊛-bottleneck 1.00/0.77/0.97 · (d)noninv-freqmasked 0.86/0.83/0.97 · **(e)bilinear_bottleneck (bypass-DENIED, invertibility-agnostic — the decisive arm) 0.55/0.57/0.53**. **Bar FAIL:** (e) does NOT dominate additive by +0.34 (0/3) AND does NOT dominate bypass-open by +0.34 (0/3 — (e) is actually WORSE than bypass-open on all 3 seeds). **Two independent kills:** ① the general bypass-denied bilinear bottleneck is the WORST bottleneck (huge D×D² projection overfits, lacks the circulant inductive bias); ② bypass-OPEN did NOT floor on the fair target (0.66–0.73) → "deny the additive bypass" is NOT the load-bearing lever. γ's last unmeasured delta is negative → GPU floor confirmed, not fired.
- **cost axis:** GPU-cost-gated (real 303M trunk co-train required; $0 toy only screens the mechanism, cannot close G1).
- **source:** fleet-full 상시 discovery lane — G1 재조합벽 census 잔여 직교 레버 ("유일 잔여 진짜 레버" 수렴, memory substrate-framebreak-g1-combination-operator)
- **lens:** BIOLOGY/ALGEBRA — Plate holographic reduced representation (HRR); associative binding via invertible compression.
- **artifacts:** [`state/1840_gamma_hrr_constructive_bind/`] — STAGE-1 FAIR: FREEZE_fair.md · toy_fair_gate.py + toy_fair_result.json · run_fair.log · RESULT_fair.md · (superseded RIGGED PR#2689: FREEZE_toy.md · toy_cheap_gate.py+toy_result.json · toy_control_additive_target.py+toy_control_result.json · RESULT.md)
- **xref:** H_1823 (circconv READOUT 🧱 floored) · H_1819 (Hadamard bind op + InfoNCE, additive-bypass OPEN 🔴 floored) · H_1466 (TPR outer-product 🧱 DIRECTIONAL) · H_1602 (recomb objective alone 🧱) · H_1834 (tension readout 🧱)
- **key:** `gamma_hrr_constructive_bind`

## Motivation

G1 재조합벽 census 의 모든 binding 시도가 floored 했지만 **공통 실패모드는 하나**: additive trunk 가 CE 를 additively memorize 하며 bilinear/binding path 를 **우회**한다 (H_1819 진단 verbatim: "additive trunk memorizes CE bypassing bilinear"; H_1823 readout 은 학습 신호 없음; H_1466 TPR 은 detector pairing-blind). 즉 지금까지 어떤 카드도 **결합 연산자를 composite-예측의 유일 경로로 강제**하지 않았다 — additive skip 이 항상 열려 있었다. 남은 미검 잔여 레버 = **학습된 constructive bind**(memory 가 명시적으로 γ cost-gated 미검으로 보류).

## Hypothesis

circular-convolution(HRR ⊛, Plate 1995)을 **readout 이 아니라 gradient 로 학습되는 trunk 결합 연산자**로 배선하고, composite-token logits 가 오직 `bind(z_a, z_b) = z_a ⊛ z_b` 를 통해서만 흐르도록 **additive skip 을 아키텍처적으로 제거(information bottleneck)** 하면 — CE 가 additively memorize 할 경로가 없어 gradient 가 factored HRR 경로를 사용할 수밖에 없고, G1 composed_distinct 가 baseline 을 초과한다.

핵심 차별점: HRR ⊛ 는 Hadamard ⊙(H_1819)과 달리 **invertible**(circular correlation 으로 unbind) → distributed·compositional 코드; 그리고 composite-logit 병목이 additive-bypass 를 **닫는다**(H_1819 가 열어둔 실패모드를 직접 차단).

## Why orthogonal to the floored axes (재탕 아님)

| floored 카드 | 무엇을 했나 | γ 와의 직교점 |
|---|---|---|
| H_1823 circconv **readout** | circconv 를 frozen readout 로 얹음, 학습신호 0 | γ 는 gradient-trained trunk 결합 (readout 아님) |
| H_1819 Hadamard + InfoNCE | ⊙ element-wise, **additive-bypass OPEN** (aux loss side-channel) | γ 는 invertible ⊛ + composite-logit **bottleneck 이 bypass 를 DENY** |
| H_1466 TPR outer-product | 구조 bind but frozen detector pairing-blind | γ 는 pairing-aware composite target 을 유일경로로 강제 |
| H_1602 recomb-objective alone | objective만, 결합구조 없음 | γ 는 objective × invertible-결합구조 × bypass-차단 3중 |

세 축(invertible-⊛ · bypass-차단 병목 · recomb-objective)이 **한 카드에서도 동시에 만족된 적이 없다** → 미검.

## Frozen bar (pre-registered · tune-to-green 금지 · p7)

| Gate | Bar (사전등록, 측정 전 고정) |
|------|------|
| G1 RECOMBINATION | `composed_distinct ≥ 2` AND `> max_single` AND coherent, ≥2/3 seeds {7,4302,4303} |
| LIFT (decisive) | bind-ON+bypass-OFF arm **strictly >** (a) bind-OFF(additive) AND (b) bind-ON+bypass-ON(H_1819 재현) on G1 best_distinct |
| ABLATION (INVERTIBILITY load-bearing) | ⊛ 를 non-invertible random-mix 로 대체 시 G1 collapse (⊛ 의 invertibility 가 원인임을 double-dissociate) |
| held-out DESCENT | 4/4 register val_CE < ln256=5.545 — overfit=verdict invalid |
| G0 pass | ≥4/5 (4000 step 필수; <4000 = INCONCLUSIVE-at-floor) |
| G6 (side) | `dist≥5` AND `fals≥1` (보조, G1 이 primary) |

**Decisive:** 오직 (bind-ON ∧ bypass-DENIED ∧ invertible-⊛) 셀만 descend/lift → binding 을 additive-bypass 제거 + invertibility 에 double-dissociate.

## Cheap test (frozen-first · $0 · numpy DIRECTIONAL only)

numpy toy: 2-leg held-out conjunction retrieval. 4 arm — (a) additive-sum readout, (b) Hadamard+bypass-open(=H_1819 재현), (c) HRR ⊛ + composite-logit bottleneck(bypass denied), (d) (c) with ⊛→random-non-invertible-mix. PRE-REG: only (c) descends on held-out composites; (a)(b)(d) floor. **이 toy 는 mechanism screen 일 뿐 — numpy mirror 이므로 DIRECTIONAL, G1 verdict 아님**(a_engine_native_learning).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

303M canon (d=3784, L=4, E0=2→E3@2000, k=512, seq=1024, bf16, savant GZ_LOWER≈0.212 cusp anneal, 4-register clean corpus). trunk 마지막 결합 지점에 HRR bind: `z_c_logits = Wo( (Wa z_a) ⊛ (Wb z_b) )`, composite-position 예측은 **이 경로만**(additive residual 로의 skip 을 mask). arms at eval: bypass-open, ⊛→random-mix. Backward = full grad (bind path 가 gradient-required). forge own-GEMM, engine-native G1/G6 via `anima evaluate --py` (session-eval-py-only). ckpt PULL before teardown (a_fire_recover_complete). ~1 H100-day; explicit-go gated (a_fire_autonomous cost 1줄 명시 후 dispatch).

## Scope / honesty (c9)

설계만 — 측정 0. tier = ⏳ PROPOSED. frozen bar 사후 이동 금지(p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다. **정직 리스크:** H_1819 가 이미 co-trained bind op × recomb-objective 를 floored 했다 — γ 의 유일한 미검 델타는 (invertible-⊛ + additive-bypass 아키텍처 차단)이며, 이 델타가 무효하면 γ 도 floor 로 수렴할 가능성 높음(census 전체가 objective-lever 로 수렴 중). 그럼에도 bypass-차단 병목은 census 어느 카드도 시도 안 했으므로 등록 가치 있음. GPU 발사 전 $0 toy 에서 (c)-only-descend 를 못 보이면 GPU 미발사(cheap-gate).
