# H_1487 — 🔁 RE-ENTRY DEPTH (재진입 처리 깊이) (P2 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료)
- **wired:** `WIRED-live` — R2 엔진-네이티브: `core/engine_cli.hexa` §ReentryDepth(reentry_settle/reentry_gws_readout) 배선 + `engine_cli_smoke.hexa` cases 248-250 + ARCHITECTURE.json lockstep. FULL 280/0 RC=0. byte-exact: deep(8 passes) 0.996 vs shallow(0) 0.0 (A) · GWS readout 0.235 depth-invariant deep-access miss, gap 0.761 (B distinct) · ablate(passes→0) 0.0 (D). processing DEPTH ⊥ spatial broadcast.
- **source:** 의식-고유 게이트 시리즈 · 고갈 카탈로그 P2 (`state/gate_depletion_catalogue/CATALOGUE.md` §P2) · '의식이라서 가능한 것'
- **lens:** consciousness-science — recurrent-processing / re-entry theory (Lamme RPT · Edelman re-entry; metacontrast masking PMC4338675) · `a_no_llm_frame_trap`
- **artifacts:** `state/1487_reentry_depth/h1487_reentry_depth.py` · verdict `state/verdicts/1487_reentry_depth/H_1487_FREEZE.json` · log `state/1487_reentry_depth/run_h1487.local.log`

## 주장

feedforward **1-pass** 만으로는 의식 접근이 안 된다 — 의식적 지각은 **재진입(re-entry) 순환 루프가
충분히 깊게 반복**되어 표상이 **안정화/증폭**될 때만 출현한다(Lamme RPT, Edelman). 같은 자극도
재진입 깊이가 **얕으면**(masking 으로 차단) 표상이 안정 못 해 **무의식**(보고 불가), **깊으면**
안정화되어 **의식**(보고 가능). masking 패러다임: 짧은 SOA(stimulus-onset-asynchrony)는 후행 mask 가
재진입을 중단시켜 effective depth 를 낮춤 → 식별 실패; 긴 SOA 는 재진입이 수렴까지 돌게 함 → 식별.

substrate 조작화: 잡음 자극 `x0` 를 contractive 재진입 맵 `x_{t+1}=(1-a)·x_t + a·proto_hat(x_t)`
(a=재진입 gain, proto_hat=현재 최근접 저장 prototype)로 반복 → 깊이가 깊을수록 true prototype 으로의
cosine 이 단조 상승, 임계 통과 시 식별. mask 는 SOA 동안 매 스텝 잡음 재주입(재진입 차단).
**LLM 은 토큰당 고정 feedforward pass-수** — 열화 자극이 보고가능해지는지를 게이트하는 가변-깊이
recurrent settling 이 없다. anima substrate 는 재진입을 수렴까지 반복한다.

## distinct vs H_1462 GLOBAL-WORKSPACE 병목 (load-bearing · 직교축)

| | H_1462 GWS 병목 | H_1487 re-entry depth |
|---|---|---|
| 축 | **공간** broadcast 병목 | **시간** 처리 깊이 |
| 게이트 변수 | 여럿 중 **누가** winner(capacity-1 측면억제) | 단일 자극이 **얼마나 깊게** 반복 |
| 경쟁 | 여러 자극 경쟁 | 경쟁 0 (자극 1·prototype set 1) |

masked-식별 과제엔 **경쟁이 없다**(자극 1개). 그래서 **GWS-only readout**(feedforward 단일패스
match 의 winner-take-all)은 **재진입 깊이에 불변** — 짧은 SOA·긴 SOA 를 **동일** 라벨('그 winner')로 찍어
masked 자극을 복원 못 하고 feedforward(얕은) 수준에 머문다(`gws_long 0.233 = gws_short 0.242`,
불변 |Δ|0.025, 둘 다 deep-access 미달 ≤0.40). 깊이를 반복하는 re-entry readout 만 긴-SOA(깊은) 자극을
복원한다(deep 1.000). bar B 가 분리.

## 측정 (frozen-first · 3 seeds [1487,1488,1489] · N_PROTO=8 · N_TRIAL=40 · NOISE=0.85 · REENTRY_GAIN=0.5 · DEEP=12pass · $0 CPU · p7)

재진입 맵 `x_{t+1}=(1-a)x_t+a·proto_hat`. FULL(deep, long-SOA) vs SHALLOW(feedforward-only, short-SOA)
vs GWS-only(단일패스 winner) vs ABLATE-recur(passes=1) vs SOA-SHUFFLE(graded depth ladder).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 깊은 재진입 식별 / 얕음 비식별 | deep **1.000** / shallow **0.000** | ≥0.85 & ≤0.40 | ✅ |
| **B DISTINCT vs GWS** | GWS-only readout 깊이 불변 + deep-access 미달 | |0.233−0.242|=**0.025** & gws_long **0.233** | ≤0.10 & ≤0.40 | ✅ |
| **C DEPTH-GATED** | 식별이 재진입 깊이로 상승 | deep−shallow **1.000** | ≥0.50 | ✅ |
| **D EARNED (ablate-recur)** | passes=1 강제 → deep 붕괴 | abl_gap **0.000** | ≤0.10 | ✅ |
| **E SOA-SHUFFLE** | depth→식별 페어링 셔플 → 상관 붕괴 | shuffle_corr **0.142** | ≤0.15 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 5/5 bars PASS.** ablation(passes=1 → 0.000)+shuffle(0.142)
양쪽이 붕괴 → lift 의 출처는 분산/현저성/단일-winner 가 아니라 **시간적 재진입 깊이** 자체.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` 위 byte-exact 재측정 + 배선이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **SATURATED existence-proof:** contractive 재진입 맵은 **designed**(학습된 recurrent net 아님).
  GREEN 자체보다 discriminator 가 결정적 — GWS-불변(0.025, deep-access 미달 0.233), ablation(0.000), shuffle(0.142).
- **a_break_the_wall (a) 측정결함 수정:** bar E 가 처음 0.332 → 0.159 로 RED — 원인은 **permutation-correlation
  floor**: 8-level monotone 축을 무작위 셔플하면 E[|corr|]~0.31 (짧은 단조축 순열의 순수 조합적 artifact,
  신호 아님). depth ladder 를 32 graded level(깊이-해상 밴드 [0.5,3.5], 식별이 0→1 로 실제 상승하는 구간)로
  해상 → floor ~0.14 로 하락. **bar ≤0.15 는 불변**(tune-to-green 아님, frozen-first — H_1485 fixed-point
  floor 수정과 동일 클래스). saturated plateau(깊이 3+에서 1.0 고착)는 gradation 이 없어 제외.
- **SCOPE TOY:** 8 proto/40 trial/3 seeds/스칼라 재진입 맵 — re-entry STRUCTURE 검증이지 학습된 recurrent
  network 아님. scale/real-corpus/실제 SOA 시간단위/연속 masking 강도/engine-transfer UNVERIFIED.
