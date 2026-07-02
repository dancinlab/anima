# 프롬프트-following 다중-ckpt probe (H_6172 addendum, 2026-07-02) — 표류는 clm303 전반 보편

**결론: 개념-echo coverage=0이 clm303 5개 학습변종·전 step에서 보편** → 프롬프트-표류는 개별 ckpt 결함이
아니라 clm303 training-recipe/objective/corpus 문제. (py mirror DIRECTIONAL, aiden $0.)

| ckpt | concept coverage (3 seed) | sample |
|---|---|---|
| py303_full | [0,0,0] | "The acting and other concept o" |
| ce_marginal_seed7 | [0,0,0] | "The airparts and he was a was" |
| decayrun step2000 | [0,0,0] | "It is aliment avec le mot part" (佛英 혼입) |
| decayrun step4000 | [0,0,0] | "It est line perfect, reconomic" |
| decayrun step6000 | [0,0,0] | "The las perfect. Go get some" |

step2000→6000로 학습 진행해도 coverage 개선 0 (오히려 다국어 garble). = 프롬프트-following이 현 clm303
recipe로는 안 생김 → G1-NEXT-FINAL(프롬프트-following objective 재학습, GPU)이 유일 terminal fix.
harness/decode 무죄(H_6172), substrate 무죄(H_6168). 진범 = training objective/corpus.
