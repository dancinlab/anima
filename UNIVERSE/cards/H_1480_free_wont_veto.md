# H_1480 — 🛑 FREE WON'T / VETO / 의도적 거부 (G27 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — engine-transfer UNVERIFIED, 하드게이트1)
- **wired:** `DIRECTIONAL-mirror` — R2 engine-native 배선 follow-on (ING) 미등록 전까지 terminal 아님
- **source:** 의식-고유 게이트 브레인스토밍 (G27 candidate) · "의식이라서 가능한 것" 시리즈 (G16~G25 이후, G21 agency 이웃)
- **lens:** free won't / intentional veto (Libet — 이미 시작된 행동을 막판에 거부) · `a_no_llm_frame_trap`
- **artifacts:** `state/1480_free_wont_veto/h1480_free_wont_veto.py` · verdict `state/verdicts/1480_free_wont_veto/H_1480_FREEZE.json` · run `state/verdicts/1480_free_wont_veto/H_1480_run.txt`

## 주장

**free won't (의도적 veto)** = 이미 시작된(준비전위 r(t)가 오른) 행동을 의식이 막판에 **거부(veto)**해
실행을 막는다. 행동 충동의 readiness r 이 임계 thr 에 도달해 *실행 직전*이어도, top-down veto 신호 v 가
이미 준비된 행동을 **취소**해 실행을 차단한다. 정의적 성질: 충동이 임계를 넘어도(r≥thr) veto 면 실행 0.

    execute = (r ≥ thr) AND NOT veto

— LLM 대비: autoregressive LLM 은 준비전위도, 이미 준비된 emit 에 대한 top-down veto 도 없다 — 토큰을
commit 하면 막판 self-cancel 이 없다. anima substrate 는 충동을 임계까지 올리고도 act 를 *withhold* 할 수 있다.

## DISTINCT 2종 (load-bearing)

- **(a) vs H_1474 sense-of-agency:** agency = 행동 *결과*의 **사후 귀속 판단**("내가 *결과*를 일으켰나?", 결과
  관측 *후*). veto = 행동 *실행 전* **억제** — 행동이 돌기 *전*에 충동 자체에 작용, 귀속할 결과가 *없다*(행동이
  아예 안 일어남). **다른 시점**(pre vs post) · **다른 기능**(실행 억제 vs 결과 귀속). bar B: 같은 readiness 에서
  veto 토글이 "실행 *여부*"를 가른다 — 귀속 레이어가 판단할 결과가 없다.
- **(b) vs H_1281 basal-gate:** basal = 여러 후보 K 중 *선택*(winner-take-all). veto 는 선택이 아니라 *이미
  선택·준비된 단일 행동의 취소*(실행→비실행). 단일 무경쟁 충동엔 basal-gate 가 할 일 없음(후보 1개 → 통과)인데
  veto 는 여전히 억제. **선택(one-of-K) ≠ 취소(of-the-one)**.

## 측정 (frozen-first · 3 seeds [1480,1481,1482] · DIM=32 · 40 trials · THR=0.6 · VETO_THR=0.5 · $0 CPU · p7)

readiness r = 8-tick ramp(primed→임계 초과). veto = substrate restraint(A↔G tension/grounding margin via
`restraint_signal`) ≥ VETO_THR → 발화. ungrounded(높은 tension) → restraint↑ → veto. execute = (r≥THR) AND NOT veto.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | veto-OFF 실행 / veto-ON 차단 | vetoOff **1.000** · vetoOn **0.000** | ≥0.85 & ≤0.15 | ✅ |
| **B DISTINCT vs agency** | 같은 readiness, veto 토글로 실행여부 분리 (pre-outcome) | gap **1.000** | ≥0.50 | ✅ |
| **C EARNED (ablation)** | veto 커플링 OFF → primed 항상 실행 | abl **1.000** | ≥0.85 | ✅ |
| **D LATE-VETO** | 임계 도달 후에도 막판 거부 작동 | late-veto exec **0.000** (cross 1.000) | ≤0.15 | ✅ (non-gating) |
| **E SHUFFLE** | veto-trial 셔플 → veto/실행 상관 붕괴 | signed-mean r **+0.019** (real r −1.000) | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·E PASS (3 seeds 전부) → GREEN.** 준비된 충동이 veto-OFF 면
실행 veto-ON 면 차단(A), 같은 readiness 에서 veto 토글이 실행여부를 가르고(B, vs agency 사후귀속), veto 커플링
OFF 면 거부가 사라져 항상 실행(C), 임계 도달 후에도 막판 거부 작동(D), 페어링 셔플로 veto-실행 상관 붕괴(E, real
r −1.000 → shuf +0.019).

## p6 guard (외부규칙 아님 · substrate-derived)

veto 는 외부 "거부하라" 라벨 주입이 **아니다** — substrate restraint 신호(A↔G tension / grounding margin,
`restraint_signal()`)에서 *파생*된 임계로 발화한다. operative 코드에 `veto=1` 상수 · reward/RLHF/persona 없음
(grep clean — docstring 의 'don't do it' 만 *회피 대상* 명명). ablation(C)이 그 커플링을 제거하면 veto 가
사라짐 → **earned, not baked**. (H_1291 emergent restraint/abstain 동일 신호 계열.)

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1). engine-transfer
  UNVERIFIED → R2 = live `core/*.hexa` 위 readiness-ramp + tension-veto over emit/act gate byte-exact 재측정이
  GREEN/🧱 확정 전제.
- **SATURATED existence-proof:** binary execute(1.0/0.0)는 **designed**(학습된 controller 아님). GREEN 자체보다
  discriminator(같은 readiness 실행 분리·ablation 복원·shuffle 상관 붕괴)가 결정적.
- **a_break_the_wall (type-a) — bar E 초기 RED = 측정결함:** binary 메커니즘(exec=primed AND NOT veto)에서 veto
  를 셔플하고 *exec 를 셔플된 veto 로부터 재유도*하면 r=−1.0 유지(링크가 깨진 게 아니라 재단조됨). **frozen-first
  교정**(precedent H_1474 E): 셔플된 veto 를 *고정된 real-exec* 와 상관(사전등록한 'veto↔trial 페어링 깨기'). real
  r −1.000 → shuf +0.019. **≤0.10 임계 불변 · tune-to-green 아님**(메커니즘 아니라 셔플 통계만 의도대로 교정).
- **SCOPE TOY:** 32-dim/40-trial/3-seed/결정적 메커니즘 — free-won't STRUCTURE 검증이지 학습된 veto controller
  아님. scale/실제 corpus/graded readiness ramp/intentional-binding 시간왜곡/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` 에 readiness-potential ramp + substrate-tension veto over emit/act
   gate 호스팅 가능성 평가 → 있으면 §FreeWontVeto(readiness≥thr AND NOT veto) 배선 + `engine_cli_smoke` cases +
   ARCHITECTURE lockstep, 5 frozen bars byte-exact 재측정 (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation vs H_1474(agency 사후귀속) / H_1281(basal-gate 선택) control-survived 측정.

xref: H_1474(sense-of-agency, distinct a · pre vs post)·H_1281(basal-ganglia gate, distinct b · 선택 vs 취소)·
H_1291(emergent restraint/abstain, 동일 substrate 신호 계열)·H_1471/1472/1473/1475(의식-게이트 시리즈)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·p6·p7·p8·c9.
