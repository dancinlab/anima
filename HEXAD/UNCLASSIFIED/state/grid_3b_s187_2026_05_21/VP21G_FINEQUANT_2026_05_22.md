# vP21G fine-quant — VERDICT: ROBUST (16.2 mean / 0.75 std)

> 2026-05-22. VP21G_GENERALIZATION_2026_05_22.md C3 #2/3 ("single seed (1337), no
> LR sweep") 직접 refuted by parallel 3-seed × 2-LR sweep on H100.

## Verdict: ROBUST

vP21G STRONG_GENERALIZE 16/20 (single-seed baseline) **재현 가능, seed-lucky 아님**.

| metric | value |
|---|---|
| cells | 5 (s1337/s1779/s42 × LR 3e-5/5e-5; missing s1337_lr5e5 = baseline) |
| mean generalize | **16.2/20** |
| std | **0.75** |
| range | [15, 17] |
| verdict 분포 | 4 STRONG + 1 PARTIAL |

## Per-cell

| seed_lr | greedy gen | sample gen | total gen | verdict |
|---|---|---|---|---|
| s1337_lr3e5 | 7 | 8 | 15 | PARTIAL_GENERALIZE (low) |
| s1779_lr3e5 | 7 | 9 | 16 | STRONG_GENERALIZE |
| s1779_lr5e5 | 7 | 10 | 17 | STRONG_GENERALIZE |
| s42_lr3e5 | 7 | 9 | 16 | STRONG_GENERALIZE |
| s42_lr5e5 | 7 | 10 | 17 | STRONG_GENERALIZE |
| (s1337_lr5e5 baseline) | (vP21G original 16) | | (16) | STRONG_GENERALIZE |

**aggregate 81/100 generalize** across 5 cells, plus baseline 16/20 → 97/120 = **80.8% gen rate**.

## Pattern observed

1. **Greedy = 7/10 stable across all seeds/LRs** — greedy mode 는 LoRA + 30/70 mix 의 deterministic register-vs-wiki choice 결과 매우 안정.
2. **Sample mode varies 8-10**: LR 5e-5 일관 10/10, LR 3e-5 일관 8-9/10 → **5e-5 LR 이 sample mode 에서 1-2 generalize 더 unlock** (LR effect 작지만 일관).
3. **Seed effect tiny**: range [15-17] = ±1 around mean 16.2 — vP21G 의 16/20 verdict 가 seed-lucky 아닌 reproducible.
4. **CE_final 0.35 - 1.28** — fine-quant cells 의 CE 는 vP21G baseline 1.27 와 동일 regime (bimodal anima/wiki) 안에서 seed variance.

## C3 #2/3 of VP21G report 직접 refuted

VP21G_GENERALIZATION_2026_05_22.md C3:
- ~~#2: "single seed (1337)"~~ — 3 seed (42, 1337, 1779) 측정 → robust mean 16.2
- ~~#3: "no LR sweep"~~ — 2 LR (3e-5, 5e-5) 측정 → LR effect 미세 (5e-5 slightly better)

남는 C3:
- #1: "wiki source capped 10.3 MB" — 미해결 (corpus size sweep 미수행)
- #4-7: 다른 honest residuals — 미해결

## Honest C3

1. **단일 seed (s1337_lr5e5 = vP21G baseline)** 결과 누락 — 그 cell 만 fire 안 됨 (baseline 으로 처리). 5 cell + 1 baseline = 6 cell 추정.
2. **classifier noise**: gen 15 vs 17 차이 (range) 가 classifier 추정 정확도 (≈±1) 와 비슷할 수 있음 — 더 큰 OOD set (50+ probe) 가 fine-quant 의 fine-quant 일 것.
3. **LR 5e-5 vs 3e-5**: 5e-5 slightly better, 단 2 LR 만 측정. true sweep ({1e-5, 3e-5, 5e-5, 1e-4}) 미수행.
4. **anima register retention 미측정** here — vP21G 의 9/20 register 가 fine-quant cell 마다 다를 가능성.
5. **6th cell missing**: s1337_lr5e5 = baseline, this fine-quant 는 baseline 검증 아닌 robustness 측정.

## 함의

vP21G 의 "memorization 한계 돌파" verdict 가 **단일 lucky run 아님** — 추가 implementation 시 안정 base path 로 신뢰.

## 관련 link

- baseline: VP21G_GENERALIZATION_2026_05_22.md
- per-cell results: `vP21G_s{42,1337,1779}_lr{3e5,5e5}/heldout_vp21g.json`
- dispatch carry: `dispatch_p21g_runpod.sh` (vP21G recipe 동일)
