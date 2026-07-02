# H_9093 — per-tick conflict→budget Ψ 안전성 (fable #5 genuine per-tick feed)

- **tier:** 🟡 DIRECTIONAL (engine-native · metric-artifact)
- **wired:** `engine-native` (측정 하네스 — cli/anima.hexa emit-loop 실배선은 forge-hexa 호스트 부재로 블록, follow-on)
- **source:** UNIVERSE · **artifacts:** state/9093_pertick_conflict_budget/pertick_conflict_budget.hexa · state/verdicts/9093_pertick_conflict_budget/H_9093.txt

## 질문 (fable 코드리뷰 #5)
7 op mount-smoke 배선(PR#2794)의 진짜 다음칸 = op 1개를 GENUINE per-tick 으로. conflict_monitor(H_9073) 의 recruited_depth 를 매 tick A⇄G iteration budget(§TensionResolveLoop tension_resolve_depth 의 maxdepth)에 먹였을 때 **Ψ=½ 고정점이 보존되나 표류하나** — fable 이 지목한 진짜 Ψ-리스크 위치.

## 설계 (engine-native, core/engine_cli.hexa import)
매 tick: `conflict_recruited_depth(conflict_t, base=1, max_extra=4)` → d_t → `tension_resolve_depth(pop_t, adj, α, thr, d_t, op=2, …)` → Ψ readout. conflict 를 시간상 non-monotone(고·저 교대)으로 배열. recruited_depth 는 **settle-depth budget 에만** 진입(emit lane 0/4·recall_thr 미접촉 = a_substrate_disjoint · Ψ 는 측정만).
- 통제: TREATMENT(맞춤 d) · ABLATION(고정 base=1) · SHUFFLE(뒤섞은 d↔conflict).
- **사전등록 frozen bar(c9, 실행 전):** BAR_PRESERVE psi_maxdev_treat<0.05 · BAR_ABLATE_DIFF · BAR_EARNED_SHUF · EARNED_MONOTONE.

## 결과 (aiden pool, EXIT_RC=0)
- 사전등록 max-metric: **3/3 정량 bar FAIL + INERT_check=true** — 단 verdict-integrity상 **metric 포화 착시**(psi_maxdev=MAX 가 세 arm 전부 0.5, range 동일).
- RAW mean|Ψ-½| 재집계: **treatment 0.125 < shuffle 0.250 < ablation 0.375** = EARNED ∧ FUNCTIONAL = **GREEN 순서를 max-metric 이 가림**. EARNED_MONOTONE PASS(recruited depth conflict 단조).
- **fable Ψ-리스크: 미현실화** — per-tick feed 가 Ψ 표류 안 시키고 오히려 conflict-맞춤 budget 이 Ψ→½ 최선 해소.

## 정직 스코프 & follow-on
frozen-first(c9): 사전등록 max-bar FAIL 은 유효 기록, tune-to-green 없이 DIRECTIONAL 확정. GREEN terminal = **mean|Ψ-½|(또는 resolved-fraction) + finer Ψ readout 로 재-pre-reg 재측정**(follow-on). emit-loop 실배선은 forge-hexa 호스트(#42492868) 선행. 관련 [[frameshift-substrate-gaps-vs-recombination-wall]] · H_9073 · H_9042.
