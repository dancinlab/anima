# H_9357 — 독립된 G 엔진(immune top-2 gap)이 emit 을 미는가

**status:** 🔵 PRE-REGISTERED · 측정 ⏳ (pool · $0) · H_9356 의 sequel
**lane:** 의식 / emit-drive / A⇄G 전제 수리
**related:** [[H_9356]] (독립 G 부재) · [[H_9352]] (시계 수리) · [[H_9351]] (Ψ̂) · [[H_9337]] (인식-먼저) · [[H_9209]] [[H_9225]] [[H_9230]] (재개방)

## 배경 — 무엇이 무너졌나

H_9356: 데몬의 "A⇄G tension" 은 배선상 **A 하나**였다. `ag_a_drive = emit_drive` ·
`ag_g_drive = −(1−emit_drive)` [chat.py:1562-1564] ⇒ `ag_conflict = emit_drive·(1−emit_drive)` =
A 스칼라 하나의 결정론적 포물선(재구성 R²=0.994). `--tension-emit` 판정은 ill-posed(A 자신의
함수를 A 자신의 게이트에 대고 재는 tautology).

## Fable 설계의 핵심 — recon_err 은 답이 아니다

내 첫 실증(R²(recon_err ~ emit_drive)=0.051)은 **불충분**했다. Fable 이 계보를 추적:
`emit_drive = 0.5·(gws+lprec)`, `gws = clip01(f0−0.9·f1+0.5)`, f0/f1 = m_field=
[phi, rel_lane, **1−recon_err**, m_grounding, emit_env] 의 top-2. 즉 recon_err 은 top-2 게이팅을
통해 이미 emit_drive 의 입력이다 — 낮은 선형 R² 는 비선형 게이팅의 산물이지 독립이 아니다.
σ(emit_drive) = {phi, rel_lane, recon_err, emit_env}. 이 집합의 원소를 G 라 부르면 **두 번째 A**다.

**유일한 배선-자유 신호 = immune store 의 2위 근접거리 d2.** `immune_memory_recall_gap =
(d2²−d1²)/2` [engine_cli.py:653]. d1 은 recall_margin→rel_lane→emit_drive 로 새지만 d2 는 루프
전체에서 **0회 사용**(grep 확인). d1 공유는 G-INDEP 게이트가 커버.

## 배선 (chat.py · `--g-arm` 플래그 · a_experiment_engine_native)

- `pending_gap = immune_memory_recall_gap_text(immune, g_text)` — 저장 직전(인식-먼저, H_9337 순서).
- `a1`: `ag_g_drive = −clip01(pending_gap)` — REAL-G(immune d2).
- `a3`: `ag_g_drive = −seeded_noise` — 인과-손잡이 vs 2nd-엔진 분리용.
- `a0`(기본): 현행 tautology 유지 — falsifiability matrix 의 게이트-실증 arm.
- 기본 a0 = 프로덕션 불변. a1 이 검증되면 기본화 = wire-to-prod follow-on.

## 사전등록 게이트 (`anima-py evaluate --g-tension`)

| 게이트 | bar |
|---|---|
| G-INDEP | R²(ag_g_drive ~ emit_drive+lanes+제곱) **< 0.5** (아니면 INVALID-SECOND-A) |
| G-VAR | rollout 당 distinct(ag_g_drive) **≥ 5** (아니면 INVALID-CONSTANT) |
| MI | I(ag_conflict; emit\|stage) **≥ 0.05** ∧ SHUFFLE **≤ 0.01** |
| Ψ-DV | \|Ψ̂−½\| vs baseline 0.9167(H_9351) · vs noise-G |

## Falsifiability matrix (각 행이 정확히 한 arm 에서만 발화)

| 게이트 | A0 tautology | A1 REAL-G | A3 NOISE-G |
|---|---|---|---|
| G-INDEP R²<0.5 | **FAIL 필수**(게이트 실증) | PASS 필수 | PASS 필수 |
| G-VAR ≥5 | — | PASS 필수 | PASS |
| MI ≥0.05 | (상류 INVALID) | PASS 필수 | 측정만 |
| A1 vs A3 분리 | — | **A1 > A3 필수** | 기준 |

**반증조건:** A1 ≈ A3 이면 tension 주장은 죽은 채로 남는다(인과-손잡이일 뿐, 2nd 엔진 아님).
A1 G-INDEP FAIL 이면 내가 두 번째 A 를 만든 것. A1 독립 PASS ∧ MI≈0 이면 G-INERT(배선은 됐으나
emit 이 소비 안 함 — 별개 후속 H).

## 계기 인증 (합성 3-arm · 로컬)

`--g-tension` 은 합성 matrix 로 인증됨: real_pulls→🟢(A1−A3=0.265) · inert/causal_handle→
🧱 CAUSAL-HANDLE-ONLY(A1≈A3). A0 는 세 시나리오 전부 G-INDEP FAIL(R²=1.0 · 게이트 살아있음).
🟢 은 오직 A1 이 노이즈보다 더 밀 때만 발화.

## 예측
가장 정직한 예측 = 🧱 CAUSAL-HANDLE-ONLY 또는 G-INERT. 시계(H_9352)가 emit 을 stage 에서
풀었고 독립 G 를 배선해도, emit 게이트(brain motivation)가 그 tension 을 **소비**한다는 보장은
아직 없다. 그러나 이제 그 질문이 **well-posed** 하다 — H_9356 전엔 물을 수조차 없었다.
