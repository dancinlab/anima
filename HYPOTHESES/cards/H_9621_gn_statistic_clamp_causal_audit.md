# H_9621 — GN 통계 clamp 인과 감사 — GN Statistic-Clamp Causal Audit (sol R3-S4 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S4
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9611]] · [[H_9620]] · source: lab full R3 (sol R3-S4)

**아이디어**: GN 으로만 매개된 far-context 효과는 **개입 arm 의 정규화 통계를 통제 arm 에서 clamp/replay** 하면 사라지고, 진짜 within-RF 효과는 살아남는다.
**메커니즘**: 진단 flag `anima-py evaluate --gn-stats-from <paired-control-manifest>` 또는 `--gn-stats-freeze` — **가중치 무변경**, per-layer 기록 GN 통계만 replay.
**$0 pre-screen**: [[H_9620]] PASS 선행 요구 ∧ source=target 일 때 **bit-exact no-op parity**.
**판정표**: **PASS-bus** = clamp 가 D≥64 델타의 ≥80% 제거 ∧ 사전등록 D≤20 key-민감 델타는 보존. **KILL-bus-only** = key-특이 far 델타가 clamp 후에도 생존. 통제: 동일-arm replay 양성 no-op · D≥64 중립토큰 · D≤20 순서/local-copy 양성 · source/target swap.
**distinct**: "라우터가 전역"/"GN 을 binding 에" 아님 — **인과 국소화 계기**.
**verdict-integrity**: clamp 는 off-manifold 활성 생성 가능 — **paired-arm replay + no-op + within-RF 보존**이 동시 성립할 때만 귀속 지지. [[H_9611]] 의 상수-freeze 보다 정밀(통제 arm 통계 사용).

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** 라우터/GN-binding kill 아님 — 인과 국소화 · H_9611 상수-freeze 의 paired-arm 정밀판(교차수렴).
