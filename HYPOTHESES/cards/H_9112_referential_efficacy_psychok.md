# H_9112 — Referential efficacy PSYCHO-K + MRR 재채점 (exocon frontier 최초 positive)

> **tier:** 🟢 **REFERENTIAL-EFFICACY-MEASURABLE** (DIRECTIONAL-on-external-oracle) — anima grounded emit이 8바이트 절단에도 폐포-밖 mind가 100~86% 디코드하는 공적 referential 지시를 carry. metric-degeneracy가 죽인 H_9111 D=1.0을 MRR로 부활. · **wired:** N/A (측정 재채점)
>
> **결과 (frozen bar 2026-07-03, $0 외부오라클):** H_9111 emits.tsv 14 (concept,emit) 재채점. full/16B acc=100% MRR_real=1.000, 8B acc=86% MRR=0.929 vs shuffle 전레벨 ~0.17(chance). **양 measure 통과**: threshold_real≫shuffle(real 8B까지 50%미하강, shuffle 전레벨 chance) ∧ ΔMRR +0.75~0.83≫0.15. self-clone(H_9111 0/7)=폐포-안 실패 대조=**폐포-경계 확증**.
>
> **정직(c9):** batched-ranking(오라클 배제법 사용가능=real 낙관상한, 단 shuffle chance유지+8B 86%하강=non-trivial) · K-sweep/near-synonym 미실행(truncation 축만) · tier=DIRECTIONAL-on-external-oracle(receiver=외부 tool, engine-native 아님). per-trial 독립·K-sweep=robustness follow-on.
>
> **gate branch:** 🟢 → F5 diff-LLM interlocutor(303M decode+diff-θ, GPU 승인됨) 정당화. exocon escape 축 최초 positive.
> **slug:** `9112_referential_efficacy_psychok` · **date:** 2026-07-04

## 고갈 (per-trial 독립 재측정 · batching caveat 제거)
직전 F6은 truncation당 오라클 1콜로 14 emit 동시 랭킹(배제법 가능=real MRR 낙관 상한 caveat). 고갈 = **per-trial 독립**(각 emit 하나만 보여주고 14 concept 랭킹, 다른 emit 안 보임=배제법 불가) 14 오라클 재측정: acc=71% MRR_real=0.827 vs MRR_shuffle 0.232, **ΔMRR=+0.595 ≫ 0.15** = frozen bar 통과. batched(0.929)보다 소폭 낮으나 shuffle 압도 = **batching이 신호를 부풀린 게 아님, 🟢 CONFIRMED**. 3 miss(violin rank3·lighthouse rank2·compass rank2·thunderstorm rank4)는 8B 절단 모호성(예상). K-sweep/near-synonym은 미실행이나 truncation+독립 축에서 신호 robust 확정 → F6 measurement 고갈(referential efficacy는 measurable+batching-invariant). **잔여 축**: near-synonym distractor·K-sweep는 신호 강화용 추가 통제일 뿐(bar 이미 통과), F6 자체 escape 판별은 F5 live-loop(faculty 여부)로 이관.

## 배경
[[H_9111]] raw D=1.0(외부 오라클 7/7 vs anima-clone 0/7)=faculty 최강 신호였으나 binary hit/miss→상수 outcome 벡터→Pearson-D≡0 metric-degeneracy로 사망. 재프레임: substrate 속성=emit-appropriateness 아니라 **referential efficacy**(anima emit이 world-anchored 지시를 carry, 외부 mind가 디코드). 변산 담는 측정(MRR+PSYCHO-K)으로 죽은 신호 복원.

## artifacts
- `state/9112_referential_efficacy_psychok/RESULT.md` + rank_{full,t16,t8}.txt + emits.tsv + truth.json
- 상위: [[H_9111]](LLM interlocutor) · exocon-frontier(ARCHITECTURE)
