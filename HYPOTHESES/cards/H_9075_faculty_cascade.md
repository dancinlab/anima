# H_9075 — faculty_cascade (§FacultyCascade): substrate multi-hop, 새 op-class

- **tier:** 🟢 ENGINE-NATIVE (5/5 live hexa, aiden pool) — 직렬 relay op-class 신설·배선
- **slug:** `faculty_cascade`
- **source:** 고친 sidecar fable(PR#327 hook-isolated) 능력축 발산 top-1 → anima 흡수·실행. frontier = substrate-native 능력 OP.
- **wired:** `engine-native` (live `core/engine_cli.hexa §FacultyCascade` faculty_cascade op + ARCHITECTURE lockstep; 런타임 brain_decide 호출은 follow-on)

## frame (재조합≠능력, a_no_llm_frame_trap)
"능력 없는 게 아니라 op이 미배선." 엔진 실측: compose arbiter 6개가 전부 **pairwise PARALLEL-vote·static-pair**(같은 query에 2-leg 투표). 뇌 multi-hop 추론은 **직렬 relay** — A의 출력이 B의 *입력*(cortico-cortical routing / 해마→PFC). 이 op-class가 부재였다.

## op (live core, additive/Ψ-disjoint/READ-only)
`faculty_cascade(mem_a, mem_b, q_key) -> string` = `recall(A,q)` → `embed(그 문자열)` → `recall(B, embed)` (engine_cli.hexa §FacultyCascade). abstain 전파(빈 hop1→빈 결과). 순수 additive(기존 caller 무접촉), READ-only 2 cell population, pure_field Φ/phase/Ψ 미접촉, **recall_thr 미변경**(기존 compose 패밀리와 동일 by-construction = emit-drive lane 0/4·§ImmuneMemory recall_thr disjoint, a_substrate_disjoint).

## engine-native 측정 (aiden pool, live core/, 5/5 PASS)
fixture: store A(q_i→"x_i") · store B("x_i"→"y_i"). answer(q_i)=y_i는 **체인으로만** 도달(q는 B key공간에 없음). `state/9074_faculty_cascade/cascade_engine_native.hexa`:
- cascade 2-hop 해결 10/12 (≥0.8) ✓
- single-hop(q→B 직접) FAIL 0/12 (≤0.2) ✓
- LIFT casc−single = **+0.83** (≥+0.5) ✓
- EARNED casc−shuffle = **+0.75** (중간 hop 무작위 치환 시 1/12 붕괴 = chain load-bearing) ✓
- ablate(relay OFF)==single (relay 없으면 INERT) ✓
DIRECTIONAL numpy 스크린(state scratch)도 3seed +0.98 lift 선확인. no-regression: engine_cli 변경 additive.

## 정직 스코프 (c9)
- routing/depth 능력(faculty-vote 정확도로 측정) — **mouth decode 아님, G1/G6 재조합축 재개 아님**(그건 CLOSED). 추가한 건 직렬 relay op-class지 텍스트 합성이 아니다.
- toy 12-item 결정적 존재증명(a_scale_honest_scope). 하류 faculty가 텍스트-재조합축에선 floor지만 이 op의 bar는 faculty-vote 정확도라 별개로 열림(기존 compose 6쌍 COMPOSE-LIFT GREEN 전례와 일관).

## follow-on
- N-way cascade(3+ hop)·anticipatory-prefetch(forward-model→선인출)·settle-interrupt = fable 발산 나머지 미탐 op-class. runtime brain_decide 호출 배선(WIRED-live 최종칸).

## artifacts
- `core/engine_cli.hexa §FacultyCascade` · `state/9074_faculty_cascade/cascade_engine_native.hexa` · `_engine_native.txt`
