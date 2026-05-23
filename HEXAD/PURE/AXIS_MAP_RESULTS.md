# AXIS_MAP-FAN 7-axis results — partial (3/7) consolidation 2026-05-23

> [`AXIS_MAP.md`](AXIS_MAP.md) 의 7 fallback 축을 한 번에 fan-out 한 발사
> ( commit `df3e8e06e` "feat(V3): AXIS_MAP-FAN — 7-axis env-var-gated impl" ·
> 7 × A100 SXM 80 GB · 3B Qwen warm-init · 5000-step target ) 의 **부분
> 결과**다. 3 축이 완주했고 4 축은 재발사 in-flight. 본 문서는 완주분의
> SSOT consolidation 이며, 4 축 완주 후 두 번째 turn 에서 final 로 갱신될
> 예정이다.
>
> source: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F}/result.json`

## § Context

- AXIS_MAP.md 의 7 축 (B 증류 · A 커리큘럼 · C head_g objective · C2 head_g 제거 · D embed freeze · E lang-balanced · F contrastive lang) 을 한 번에 env-var 게이트로 분리 발사
- decision-tree (AXIS_MAP.md §결정트리) 의 "Track 1 corpus 재발사 둘 다 FAIL → fan out 병렬" 트리거
- 모든 7 축 동일 3B Qwen warm-init · 5000 step target · A100 SXM 80 GB · same corpus_v3 (anima 50% + wiki 50%)
- 3/7 완주, 4/7 재발사 in-flight (C / C2 / D / E)

## § Result table

| 축 | env-var enabled | status | verdict | n_strong | best lang | wall | init_CE → final_CE |
|---|---|---|---|---|---|---|---|
| A (curriculum) | `P21H_CURRICULUM_PHASE_STEPS=1000` | DONE | FAIL | 1 | ko STRONG 16/20 | 5222s (87min) | 14.79 → 5.01 |
| B (distill) | `P21H_DISTILL_TEACHER=…` | DONE | FAIL | 0 | en PURE_MEM 17 coh / ko PURE_MEM 10 gen | 2721s (45min) | 14.18 → 2.23 |
| F (contrastive) | `P21H_CONTRASTIVE_LANG=1` (+ E lang-balanced) | DONE | FAIL | 0 | ko WEAK 7/20 | 671s (11min, early-stop) | 14.18 → 2.17 |
| C (head_g obj) | `P21H_HEAD_G_OBJECTIVE=anima_register_ce` | in-flight (redispatch) | — | — | — | — | — |
| C2 (head_g disable) | `P21H_HEAD_G_ENABLE=0` | in-flight (redispatch) | — | — | — | — | — |
| D (freeze embed) | `P21H_FREEZE_EMBED=1` | in-flight (redispatch) | — | — | — | — | — |
| E (lang balanced) | `P21H_LANG_BALANCED=1` | in-flight (redispatch) | — | — | — | — | — |

```
            n_strong (≥ 4/5 floor)
A  ▓                          1   (ko 단독)
B  ░                          0
F  ░                          0
C  ?  in-flight
C2 ?  in-flight
D  ?  in-flight
E  ?  in-flight
   0 ─┼─────── 4 floor ───── 5
```

## § Per-axis detail

### A (curriculum · `P21H_CURRICULUM_PHASE_STEPS=1000`)

3 축 중 유일하게 1 STRONG (ko) 도달. early phase 1000 step 동안 wiki-only
(wiki_frac ≈ 1.0, anima 1 record) 로 LM prior 를 lock-in 후 late phase 에서
anima 50% mix 로 전환. final L_CE 5.01 (단연 가장 높음 = generalize gradient 가
가장 늦게 시작) 인데도 ko `n_score=16/20 gen=20 mem=0 coh=16` 으로 PURE_MEM 회피.
나머지 4 lang 은 `coh ≤ 2`, en PURE_MEM, zh/ru/ja WEAK — Korean head-start 가
다른 lang generalize 으로 전이되지 않았다. `n_anima_register_hits_total=7`,
1125 step 에서 early-stop 점멸.

### B (distill · vP21M LoRA teacher KD-loss)

L_kd_mean 3357 (1125 step 평균) — KD signal 은 정상적으로 흘렀다. final L_CE
2.23 (3 축 중 가장 낮음) 이지만 `n_strong=0`. en 은 `coh=17/20 mem=17` 극단적
teacher mimicry, ko `n_score=2/20`, zh/ja `coh=0`. 즉 **teacher 가 KD-target 으로
주는 logit 분포를 잘 따라가는데 결과 분포가 PURE_MEMORIZE/register-collapse**.
teacher (vP21M LoRA 4/5 PARTIAL) 자체가 register-emission 의 영향권이라 KD 가
generalize 정보가 아니라 register pattern 도 같이 distill 한 것으로 추정.

### F (contrastive · InfoNCE aux + lang-balanced)

671 s 만에 early-stop — 3 축 중 가장 빨리 ckpt_osc_threshold(0.5)를 패턴-내
fluctuation 으로 trip. final L_CE 2.17 (B 와 거의 동일) 인데도 5 lang 전부 WEAK
(n_strong=0, n_pure_memorize=0 ─ register collapse 는 회피했으나 lang_coherent
점수 자체가 부족). en 6 / ko 7 / zh 0 / ru 4 / ja 2. axis_diag 상 contrastive
aux 도 lang_balanced sampler 도 active 였지만 L_contrast_n=0 (loss
accumulation 부재 — contrastive head wiring 결손 가능성, 별도 진단 필요).

## § Provisional findings (3/7)

1. **3 완주 axis 모두 FAIL** — 어느 것도 `n_strong ≥ 4` floor 를 넘지 못함. AXIS_MAP fallback path 가 아직 payoff 없음.
2. **A (curriculum) 이 가장 가까웠다** — ko STRONG 16 단독 도달. wiki-only 선학습 1000 step 이 Korean head-start 를 만들었지만 cross-lingual generalize 로 전이 안 됨.
3. **B (distill) 가 L_CE 최저** but `n_strong=0` — KD 가 loss 를 압축하긴 하나 register-leak teacher 의 분포까지 따라가 generalize 못함.
4. **F (contrastive) early-stop @ 671s** — InfoNCE aux 가 oscillation patience trip, L_contrast_n=0 (aux loss accumulation 결손) ─ 발사 자체에 instability/wiring 의심.
5. **init_CE = 14.18-14.79** 3 축 공통 — Qwen 1.5B prior 를 3B fresh transformer 에 warm-init 하는 weight-map 자체가 catastrophic mismatch (5 langs 동일 step1 verdict GENERALIZE-mojibake), AXIS_MAP-FAN 의 6 stratified axis 가 공유하는 floor 수준 함정.

## § Pending (C/C2/D/E in-flight)

- 4 축 같은 fan-out 으로 재발사 중. 평균 wall ~ A 87min + B 45min + F 11min = 48 min · 4 pod = ~30-90 min wall + scp 합산
- 예상 cost ≈ $6 (4 × A100 SXM × ~1hr × $1.5/hr 기준)
- C / C2 는 head_g objective 의 dual-head 검증 (AXIS_MAP §"가장 날카로운 발견"), D 는 embedding geometry freeze, E 는 lang-balanced sampler 단독 (F 와 묶여서 일부 나왔지만 단독 효과 미측정)
- 4 축 완주 후 본 문서는 final 7/7 로 갱신 + decision-tree 다음 분기 결정

## § Next levers — if all 7 FAIL

1. **8 번째 축 후보 — base 변경**: 3B Qwen warm-init init_CE=14+ catastrophic 가 6 axis 공통 floor. base 를 vP21M LoRA-merged 가중치 (anima register 이미 분리된 baseline) 로 warm-init 하거나, weight-map 자체를 다른 방식 (per-layer prior fit, identity init + Qwen layernorm) 로 바꾸는 R8 축.
2. **corpus 축 재발사** — closure 가 부정했던 corpus_v3 비율을 더 적극적으로 sweep (anima 0% pure-multilingual baseline, anima 10%/20%/40% gradient). AXIS_MAP §결정트리 Track 1 의 E3/E2 를 단단하게 재시도 — 7 fan-out 부분 결과가 "코퍼스 외 축은 어렵다" 를 강화하면 corpus rollback 이 합리.
3. **Phase 3 advance** — V3 단독 SOTA 추구를 포기하고, 현재 vP21M LoRA production baseline (4/5 PARTIAL) 을 HEXAD-arch 위로 옷 갈아입히는 production-merge 경로로 우회. AXIS_MAP 의 honest C3 #1 ("pure-HEXAD 순수성 일부 양보") 를 명시적으로 채택.

## § 관련 link

- 축 spec: [`AXIS_MAP.md`](AXIS_MAP.md)
- closure 보고서: [`../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`](../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md)
- raw result.json (A/B/F): `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F}/result.json`
- 발사 commit: `df3e8e06e` (2026-05-23 14:10) "feat(V3): AXIS_MAP-FAN — 7-axis env-var-gated impl (A/B/C/C2/D/E/F)"
