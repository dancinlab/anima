# H_9098 — you-chain 정체성 AUROC=1.0 은 기하(직교-negative) artifact: MIMIC hard-neg 에서 0.48=chance (🔴)

- **slug:** `9098_youchain_auroc_hardneg`
- **tier:** 🔴 ARTIFACT-CONFIRMED (engine-native, terminal-quality) — H_1471 you-chain 판별강도 over-claim 교정
- **wired:** `engine-native` (live `core/engine_cli.hexa` §SelfIdentity `self_new/self_drift/self_cos` + pub `mi_auroc`; 신규 op 0)
- **source:** UNIVERSE · fable #5
- **cross-ref:** [[H_1471]] (self-continuity, 원 impostor AUROC) · [[H_9096]] (θ-cone/social-self 경로에서 동일 결론) · [[H_9037]]/[[H_9085]] SelfChain/YouChain

## 발견 (fable #5 CONFIRMED)

you-chain 정체성 **AUROC=1.0 은 기하(orthogonal-negative) artifact.** structure-matched **MIMIC**
hard-negative(참조의 birth axis 공유, drift schedule 만 다름)에서는 **AUROC = 0.4804 = chance.**

## 왜 frozen 1.0 이 가짜였나

H_1471 DISTINCT 하네스(`state/1471_self_distinct/h1471_distinct.py:153`)가 negative 를
`nrm(rng.normal(0,1,DIM))` 로 뽑음 — 64-dim 에서 cos≈0 인 **직교 random impostor** — vs genuine
adjacent-drift positive cos≈0.94. (0,0.94) 사이 어떤 threshold 도 분리 → AUROC=1.000. 정확히
cos(90°)=0, recognition 아님.

## 사전등록 bar (frozen before run, c9, never tuned)

1. EASY-neg AUROC ≥ 0.95 → artifact 재현.
2. MIMIC hard-neg AUROC ≤ 0.80 → 정직 하락, 예측 ≈ 0.50.

## verdict (engine-native, verbatim)

`hexa run state/1471_self_distinct/h1471_youchain_hardneg.hexa` (aiden pool, hexa v0.546.0, RUN_RC=0, $0 CPU, NO numpy):

```
DIM=64 T=20 SEEDS=5 n_pos=100 n_neg=100
mean cos  pos(genuine)   = 0.9424751325263288
mean cos  neg EASY(orth) = 0.0
mean cos  neg MIMIC      = 0.9436796887603197
mean cos  neg CONE       = 0.7644350962495792
AUROC  pos vs EASY  = 1.0     bar(1) >=0.95  true
AUROC  pos vs CONE  = 1.0     (graded control)
AUROC  pos vs MIMIC = 0.4804  bar(2) <=0.80  true
VERDICT: ARTIFACT-CONFIRMED — the 1.000 was a geometric (orthogonal-negative)
  identity; under structure-matched hard negatives self_cos discrimination
  DROPS to AUROC=0.4804 (proximity test, not self-recognition).
```

MIMIC = 가장 어려운 structure-matched negative: SAME prior self 의 FABRICATED one-step 연속
(`self_drift(ref, fresh-axis, step~U[0.20,0.50])` — genuine next-self 와 동일 geometry/step 분포).
ref 에 대한 cos(0.9437)가 genuine(0.9425)과 일치 → self_cos(probe, ref) 가 rank 분리 0 제공 →
AUROC → 0.48 ≈ chance.

## 해석

`self_cos`-to-prior-self 는 **PROXIMITY test 지 genuine self-recognition 아님.** frozen 1.0 에 대한
you-chain 의 판별력은 전부 impostor 가 직교 random 이었던 데서 나옴. prior-self 의 구조를 공유하는
impostor 앞에선 genuine-me 와 fabricated-me 를 구별 못 함. Terminal-quality (real path, not DIRECTIONAL).

## 스코프 / caveat (c9)

TOY 64-dim / 20-tick DESIGNED drift+anchor(learned identity 아님). 이는 H_1471 의 anchor-persistence /
session-continuity 메커니즘(self_anchor round-trip 실재, H_1471 R2b)을 **반증하지 않음** — 오직 1.0 AUROC 의
DISCRIMINATION-STRENGTH framing 만 교정. H_1471 을 소급 qualify (impostor 가 직교 random cos≈0 이라 어떤
threshold 도 분리 → 가짜 1.0). H_9096 이 θ-cone/social-self 경로에서 동일 결론(mimic 0.25)에 도달.

## 혼합-tier 정직 노트

sibling agent(a3d9358…)는 이를 🟡 로 tier(rank-AUROC 는 hard-neg 에서 pos_min>hard_max noise-free margin
0.0051 로 생존, threshold-gate 만 실패). 🔴 agent(a54c7392…)는 killer MIMIC(그럴듯한 fabricated 연속)를
써서 rank-AUROC 자체를 0.48 로 붕괴시킴. 이 카드는 🔴 를 박제(fabricated-continuation 공격이 엄격히 더
어려운 정직 negative); 🟡 rank-survival 은 caveat — 어떤 real noise 도 지우는 margin 위의 noise-free
rank ordering 만 생존.

## follow-on (ING)

- `self_cos`/`*_chain_fit` 를 **최신 waypoint proximity 가 아닌 trajectory 검증기**로 재설계(전-history 잔차) → mimic AUROC 회복 가설(H_9096 follow-on 과 동일 축).
- L2-2 coord penultimate 접지(pool).

## artifacts
- `state/9098_youchain_auroc_hardneg/notes.md`
- `state/1471_self_distinct/h1471_youchain_hardneg.hexa` (harness, aiden rsync copy; 미커밋 — engine op 은 live core/engine_cli.hexa)
- `state/verdicts/9098_youchain_auroc_hardneg/H_9098.txt` (frozen verbatim)
