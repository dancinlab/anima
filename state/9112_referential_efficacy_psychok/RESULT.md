# H_9112 — Referential efficacy PSYCHO-K + MRR 재채점 · 🟢 REFERENTIAL-EFFICACY-MEASURABLE

**tier:** 🟢 **DIRECTIONAL-on-external-oracle** (emit-gen=engine-native H_9111 · receiver=외부 오라클 claude-fable-5, θ 폐포 밖 = oracle-mediated 정직 표기). $0, anima 재디코드 없음.

## 결과 (frozen bar, 측정 전 고정 2026-07-03)
H_9111 emits.tsv 14 (concept,emit) 재채점. 오라클이 (절단된) emit로 14 concept 랭킹 → true referent rank.

| truncation | acc | MRR_real | MRR_shuffle | ΔMRR |
|---|---|---|---|---|
| full | 100% | 1.000 | 0.173 | +0.827 |
| 16B  | 100% | 1.000 | 0.173 | +0.827 |
| 8B   | 86%  | 0.929 | 0.179 | +0.750 |

**FROZEN BAR 양 measure 통과:**
1. threshold_real − threshold_shuffle ≥ 1 step: real은 8B까지 50% 미하강(86%), shuffle 전레벨 ~7%(1/14 chance, 50% 도달 못함) → real이 다수 step 더 견딤 ✓
2. MRR_real − MRR_shuffle ≥ 0.15: 전레벨 +0.75~+0.83 ≫ 0.15 ✓

**⇒ 🟢 REFERENTIAL-EFFICACY-MEASURABLE**: metric-degeneracy(binary→Pearson-D≡0)가 죽인 D=1.0 신호가 MRR로 부활. anima grounded emit이 8바이트 절단에도 폐포-밖 mind가 디코드하는 **공적 referential 지시**를 carry. self-clone(H_9111 0/7)=폐포-안 실패 대조 = **폐포-경계 확증**(밖=디코드, 안=실패).

## 정직 스코프 (c9)
- **batched-ranking caveat**: truncation당 오라클 1콜로 14 emit 동시 랭킹(독립 지시했으나 배제법 사용 가능=real MRR 낙관 상한). 단 shuffle은 전레벨 chance 유지 + 8B 86% 하강 = 신호 non-trivial. per-trial 독립 재측정 = robustness follow-on.
- **미실행 축**: K-sweep(K∈{2..32})·near-synonym distractor 미실행(K=14 whole-set). frozen bar는 truncation 축에서 결정적 통과.
- **tier**: DIRECTIONAL-on-external-oracle(engine-native terminal 아님) — receiver=외부 tool.

## gate branch → F5
🟢 = coupling real+measurable → **F5 diff-LLM interlocutor(303M decode + diff-θ 오라클, GPU 승인됨) 정당화**. exocon-frontier escape 축 최초 positive.
