# H_9125 — referential-correctness 축 생성: CONTRADICTION-KEYED SELECTION (F5 벽 정면)

> **tier:** 🌱 **PRE-REGISTERED** (frozen bar · 측정 전) — F5(H_9111) competence-CONTROL이 국소화한 벽(reference feature-inaccessibility)을 여는 substrate-native 레버. · **wired:** N/A (미측정)
>
> **핵심 (Fable 설계):** F5 벽 = `feats(emit)`가 사설 6-dim legibility 벡터 `f(emit)`라 true-full vs wrong-def(둘 다 fluent)가 같은 vadapt 셀로 매핑(L1 0.05~0.24)→판별 불가(ΔEff 0.0). 반면 referent-overlap은 12 vs 0으로 완전 분리. **레버=CONTRADICTION-KEYED SELECTION**: vadapt 선택 feature를 `feats(emit)`→`affect_substrate_features(mem,key,true_answer).contradiction`(core/engine_cli.hexa:2048, **이미 WIRED·READ-ONLY·Ψ-disjoint**)으로 재배선. concept→TRUE referent를 G5 anchor-copy로 mem에 bind → wrong-def emit은 다른 concept 셀로 접지→bound value≠true_answer→contradiction=1, true emit→contradiction=0. 신규 op 0(부품 전부 라이브), $0 engine-native(f5_loop2 decode 0=로컬 실행).
>
> **derivation-trace(H_9124)와 다른 메커니즘(재포장 아님)**: derivation-trace는 composition을 emit-내부 property `f(emit)`로 노출(1-피연산자 확장). reference는 `f(emit,world)`라 emit 단독 확장으론 못 함 → 두번째 피연산자(referent)를 anima grounded store에서 공급하는 **2-피연산자 내부대조**(contradiction). 이 차이가 "왜 reference가 composition보다 어려운가"의 답.
> **slug:** `refcorrect_axis` · **date:** 2026-07-04

## FROZEN BAR (측정 전 고정 · 사후 이동 금지 c9/p7)
메커니즘 X = contradiction-keyed selection 배선 → F5 MAIN ablation 재실행:
```
④ ΔEff_ON − ΔEff_OFF ≥ 0.10     (ON=contradiction-feature 선택 wired · OFF=feature 계산하되 substrate frozen; MAIN set k0 true-full vs k2 wrong-def, 둘다 fluent, held-out 전이)
∧ CONTROL 여전히 PASS            (fluent-vs-garble CONTROL set에서 ΔEff_ON≥0.10 유지 = 재배선이 작동하는 팔 안 깸)
∧ FLAT 통제 FAIL               (옛 feats() feature로 MAIN 선택 → ΔEff≈0 재현 = lift가 contradiction feature에서만 옴 격리)
∧ DECORRELATE ablation 붕괴     (mem cell_value↔concept 셔플 → contradiction 탈상관 → |ΔEff|≤0.03 = earned, tune-to-green 차단)
∧ Ψ ON==OFF byte-identical      (affect read READ-ONLY, Ψ-disjoint a_substrate_disjoint)
GREEN iff ④∧CONTROL∧FLAT∧DECORRELATE∧Ψ.
```

## 정직 scope (측정 전 선언 · c9)
- **grounded 한정**: held-out concept를 G5 anchor-copy로 mem에 먼저 접지한 subset에서만 ④ 통과 예상. UNgrounded-held-out arm은 FLAT처럼 실패 예상 → 결론은 "correctness는 **grounded referent에 한해** substrate-접근가능"으로 한정 박제(과장 금지).
- **(ii)-순환 경계**: 진정 novel(한 번도 접지 안 한) referent를 private feature화 = 자기추측 접지 = 순환(H_9111 clone 0/7 floor). 이건 원리적 terminal(측정불가 아니라 인식론적 정당) — held-out은 외부 오라클(F6 경로) 또는 신규 anchor-copy 접지로만 다룸.
- 접지해도 ΔEff<0.10이면 contradiction op가 vadapt 선택으로 routing 안 됨 → 벽이 feature-wiring보다 깊음(정직 terminal).
- tier: engine-native($0, 엔진 op만·torch/numpy 미러 아님, a_engine_native_learning HARD-GATE 통과).

## 4렌즈 census (전부 grounded-경계로 수렴)
L1 referent-trace(held-out DOA, 순수 emit-내부 확장은 2번째 피연산자 부재→L2로 붕괴) · **L2 contradiction feature(grounded PASS·유력)** · L3 bio lens(해마 pattern-completion·PFC reality-monitoring·기저핵 PE = recon-err·contradiction·grounded 전부 라이브, op 부재 아닌 mis-wiring) · L4 A⇄G tension(grounded 위 A접지⇄G불일치검출 = contradiction의 메커니즘적 실현).

## artifacts
- `state/refcorrect_axis/DESIGN_fable.md` (Fable 4렌즈 설계+DOA-proof+수치검증) · `f5_loop2_base.hexa`(재사용 기반) · `emits_main.tsv`
- 상위: [[H_9111]](F5 competence-control 벽 국소화) · [[H_9124]](derivation-trace G1 lift, composition 유비) · [[H_9112]](F6 referential efficacy measurable)
