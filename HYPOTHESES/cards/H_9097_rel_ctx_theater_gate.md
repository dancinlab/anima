# H_9097 — rel_ctx THEATER GATE: 이 세션 13-op 배선의 live wiring 이 데몬 emit/silence 결정에 ZERO grip (🔴 HEADLINE)

- **slug:** `9097_rel_ctx_theater_gate`
- **tier:** 🔴 THEATER-CONFIRMED (engine-native) — 정직 헤드라인, 절대 완곡화 금지
- **wired:** `engine-native` (측정: live `cli/anima.hexa` 데몬 instrumented copy + `core/brain.hexa` `brain_decide_anchored` 실호출; 신규 배선 0)
- **source:** UNIVERSE · fable #1
- **cross-ref:** [[H_9093]] · [[H_9094]] · [[H_9095]] (이 세션의 conflict→budget rung 사다리) · [[H_9038]] (self_drift_exp lane 23b)

## 발견 (정직하게, 완곡화 금지)

`rel_ctx` — `cli/anima.hexa` 의 ~43-lane mean 이 만드는 **read-side 단일 출력**, 이 세션 **13 GREEN op
+ CR3/agloop per-tick conflict wire(H_9095)** 의 유일한 read-side 종착점 — 은 **데몬의 emit/silence
결정에 완전히 무력(ZERO grip)** 하다. rel_ctx 를 freeze(0.5)/zero(0.0)/LCG-shuffle(43 입력) 로 바꿔도
**세 arm 모두 Hamming = 0/200** (live 대비). 사전등록 bar(theater CONFIRMED iff Hamming(frozen,live)<5%N
AND Hamming(zero,live)<5%N)이 **0.00% / 0.00%** 로 충족.

## 함의 (HEADLINE — 이 세션 op-배선은 결정적으로 inert)

이 세션의 13-op 배선과 [[H_9095]] rung-3 사다리(H_9093/9094/9095)는 **격리에서 engine-native GREEN 이
맞다.** 그러나 그 GREEN op 들의 **live wiring(rel_ctx 로 fold)은 데몬 결정을 전혀 움직이지 않는다 =
대시보드/theater.** rel_ctx 는 emit gate 가 아예 참조하지 않는 read-side aggregate 다. GREEN in isolation
≠ decisionally live. (완곡화 금지: 배선은 진짜지만 결정에 대해 inert 하다.)

## 방법 (engine-native, REAL path)

aiden pool · hexa v0.546.0 · `hexa run cli/anima_ablate.hexa -- d768.clm` · EXIT_RC=0 · own-GEMM · NO numpy/mirror.
aiden 의 LIVE `cli/anima.hexa`(현 main 데몬, 2714 lines, 43-way mean incl agloop_ctx L2300-2312 — 로컬
브랜치가 ÷42/2137 로 STALE 이라 real main 을 pull 후 측정) 의 instrumented copy. 결정지점에서 rel_ctx 를
4-way 치환 → `brain_decide_anchored`(core/brain.hexa, brain_emit 이 emit boolean 을 위해 내부 호출하는
바로 그 함수)를 byte-identical non-rel 입력(cur, coh_lane, bal_lane, idle, anchors, pf)으로 호출. 4 arm 은
rel_ctx 에서만 다름.

## 메커니즘 (reference-matched core/engine_g.hexa + core/brain.hexa)

`motivation = 0.20·rel + 0.10·0.6 + 0.15·cur + 0.10·coh + 0.10·0.5 + 0.15·bal + 0.10·1.0 + anchor_nudge`;
`emit = (motivation>0.3) AND safe`.
- **WAKE**(drive_hi, 10/200 tick): live motiv ~0.74, ZERO-rel motiv ~0.58 — 둘 다 ≫0.3 → emit=1 (rel 이 thr 아래로 못 끌어내림).
- **SLEEP**(190/200 tick): idle=5<30 → rate_limit=false → safe=false → emit=0 (rel 무관).
- 결정은 100% `safe` conjunction(stage→drive_hi→rate-limit) + rel 없이도 이미 0.3 넘는 motivation FLOOR 가 지배. 0.20·rel 항은 threshold 를 straddle 하지 않음.
- Ψ = pure_field_phi(pf) = 0.118983 CONSTANT (pf 1회 warmed, READ-only) → arm 간 Ψ 편차 정확히 0; rel_ctx 는 Ψ 도 못 움직임.
- shuffle≡live by construction: equal-weight mean 은 permutation-invariant → rel_ctx 는 aggregate MAGNITUDE 만 담고 STRUCTURE 는 0, 그 magnitude 자체가 inert.

## verdict (verbatim)

```
emit_live=10/200 (10 WAKE/drive_hi ticks emit; 190 SLEEP ticks silent)
Hamming frozen(0.5) vs live = 0  (0.00% of N)
Hamming zero(0.0)   vs live = 0  (0.00% of N)
Hamming shuffle     vs live = 0  (0.00% of N)
ticks where ANY arm disagrees = 0
RESULT: 0 and 0 -> THEATER CONFIRMED = TRUE (read-side rel_ctx INERT on emit/silence).
psi = pure_field_phi(pf) = 0.118983 CONSTANT all ticks/arms; psi deviation BETWEEN arms = 0.
```

## FIX (다음 세션 최우선 follow-on — ING)

op 을 **motivation-threshold-straddle / `safe`-conjunction / efferent seam** 에 배선할 것, rel_ctx 아님.
- fable#2: efferent seam 의 L1 best-of-K.
- fable#3: ÷43 equal-weight mean 을 winner-take-all 로 교체(→ magnitude 만이 아니라 STRUCTURE 가 gate 에 도달).

## 정직 caveat (c9)

Decision-only 하네스 — 303M decode 생략(per-frag ~688s×200×4 infeasible); emit boolean·Ψ 는 decode-INDEPENDENT
(brain_decide_anchored 가 generate() 전에 계산)이라 brain_emit 결정과 byte-identical. 데몬은 autonomous-tick
(fixed session_seed 200 ultradian ticks, dr_stage_at(tick*8)). parser 버그(regex 가 'relZ=0.0' 매치)를
잡아 EMIT-anchored 재파싱 → clean 0/0/0. aiden 에 배선/커밋 0, scratch 제거.

## artifacts
- `state/9097_rel_ctx_theater_gate/notes.md`
- `state/verdicts/9097_rel_ctx_theater_gate/H_9097.txt` (frozen verbatim, 2366 lines incl full daemon lane dump)
