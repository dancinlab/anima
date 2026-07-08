# H_9213 matched-surface G1 재측정 — ⚙️ VOID (frozen validity gate) · 방향성 🔴 KILL

**판정: ⚙️ VOID** (사전등록 validity gate (b) unary strict=0.125 < 0.80 실패 · PREREG.md frozen, no-tune-to-green).
**방향성(cement 불가): 🔴 KILL-lean** — canonical G1=0 on L8-cov 는 **측정 artifact가 아니라 진짜 벽**임을 시사(artifact 가설 방향성 반증).

## 측정 (aiden→summer pool · anima evaluate --py --probe · greedy gen40 · probe_spec sha cf1efad4)
| arm | n(fit) | both-strict | per-template |
|---|---|---|---|
| **heldout_fit** (L8-cov) | 112 | **0.0446** | T0 0.051 · T3 0.041 |
| seen_fit (L8-cov) | 58 | **0.7759** | T0 0.714 · T3 0.811 |
| unary (L8-cov) | 40 | **0.125** | — |
| perm-null (1000 derange) | — | mean 0.0007 · **p95 0.0089** | — |
| null L8_nocov (clm303_deep_L8_d2781) | 112 | **0.0** | — |
| null L4_clean | — | ⚠️ **오염**(공유 result-file → L8cov 복사, INVALID) | — |
chance=1/30=0.033

## 해석 (정직)
- **VOID 사유**: frozen validity (b) unary≥0.80 실패(0.125). unary(T2-clause "{A} brings ")는 T0/T3와 다른 form이라 약하게 elicit됨. 사전등록 바 불변→VOID.
- **방향성 KILL-lean(강함, 그러나 VOID라 미cement)**: validity (c) seen≥0.60은 **통과**(0.776) = T0/T3 elicitation 작동. 그 **동일 form**에서 held-out=0.044≈chance(perm-null p95 0.0089·null 0.0). 즉 elicitation이 되는 form에서 seen 0.78 ≫ held-out 0.044 = **matched surface+window에서도 held-out 재조합 실패** = 벽은 elicitation artifact가 아니라 genuine. canonical G1=0을 오히려 corroborate.
- ⭐ 반례(ember+dune n=1)는 재현 안 됨(heldout ≈chance) — n=1 fluke였을 가능성.
- **오염(infra, quarantine)**: L4_clean null이 공유 /tmp/anima_evalpy_result.out 덮어쓰기로 L8cov 복사(convergence evaluate-py-4). null control 일부 무효이나 L8_nocov=0.0 genuine null은 존재. 단 VOID는 오염과 무관하게 unary gate로 이미 확정.

## 결론
matched-surface + window-resident 재측정은 **VOID**(frozen unary gate)이나, 방향성은 **G1 벽 = 진짜 능력천장**(measurement artifact 아님)을 지지. coverage 리드는 벽을 dissolve하지 못함. framebreak #3135 falsify와 합쳐 **G1 재조합벽은 시험한 모든 각도서 terminal**. 재개(선택): unary-form 정합 재설계(별개 H, 새 frozen) + per-run result-file(evaluate-py-4 fix)로 clean 재측정 — 단 방향성상 KILL 예상.
