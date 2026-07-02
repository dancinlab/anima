# H_1817 — G1 floor 판별: undertrain vs 구조적 천장 (step-sweep + 정규화)

**Status:** 🔒 **PRE-REGISTERED · COST-GATED · DO NOT FIRE** — recipe + frozen prediction 등록, 미실행. 303M step-sweep = pool/rent GPU → team-lead cost-gated(explicit-go).

## 동기 (objrun H_1602 직속 follow-on)
g1-lever 4 직교렌즈(depth H_1598 · binding H_1601 · data H_1599 · objective H_1602)가 **전부 G1 floor**(composed_distinct=0). 하지만 전부 **2000-step·작은 코퍼스** = INCONCLUSIVE-at-floor. 핵심 미해결: **이 floor 가 (a) undertrain(학습 부족) 인가 (b) 구조적 천장(binding operator 부재) 인가?** 둘은 처방이 정반대 — (a)면 더 학습/정규화, (b)면 mouth-내 binding 구조 신설(H_1603 방향). 외부 문헌(Doshi/Gromov 2310.13061): weight-decay/dropout 가 grok 전이 강제, 정규화 없으면 memorization floor. → **step+정규화 sweep 이 (a)/(b) 판별자**.

## 설계 (frozen)
- arch = objrun 동형(CLMConvMoE L4·d3784·E2→E3, savant golden-zone) = `cli/train.hexa --canon`. objective = ce_marginal(objrun best, contrastive 무이득 확인됨).
- **sweep**: steps {2000(objrun baseline), 8000, 20000} × weight-decay {0, 0.1} × dropout {0, 0.1} (grokking 정규화). seed {7,4302,4303}. 코퍼스 = 4-cell(objrun 동일) — 코퍼스 교란 배제, step·정규화만 변수.
- 측정 = **engine-native** `anima evaluate <clm> --gen 80` (hexa 단일, g_eval_g1) — py 폐기 후 hexa terminal. held-out mirror-DESCENT(a_clm_gen_pipeline) 통과 ckpt만.

## Frozen prediction (측정 전 등록 · tune-to-green 금지)
- **(a) undertrain 가설 SUPPORTED iff**: G1 composed_distinct 가 step↑(+정규화)에 따라 단조 상승, ≥1 셀이 composed_distinct≥2 도달(H_1129 bar VERBATIM) majority ≥2/3 seed. → 벽 = 학습부족, lever = 정규화+step.
- **(b) 구조적 천장 SUPPORTED iff**: 전 sweep(20000-step·정규화 포함) G1 composed_distinct=0 flat. → undertrain 배제 = 구조적, lever = mouth-내 binding operator(H_1603 EXP-bind 방향) 필수, 학습량 아님.
- 어느 쪽이든 **결정적 판별** (현 INCONCLUSIVE-at-floor 해소). bar 무이동.

## 가드
- ckpt PULL before teardown(a_fire_recover_complete) · engine-native 재측정(torch-probe 단독 verdict 금지) · held-out gate 필수 · DO NOT auto-fire(cost-gated, explicit-go). est ~6 run × (2k~20k step) on pool/rent GPU.
- 참조: 메모리 `g1-lever-multilens-objective`·`frontier-novel-levers-untried`(N6 step+정규화·N7 dict-aux) · objrun `state/1602_recomb_objective/RESULT.md`.
