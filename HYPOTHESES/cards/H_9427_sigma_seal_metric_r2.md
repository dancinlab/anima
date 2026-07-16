# H_9427 — σ-seal metric: 데몬 상태분산의 시계-설명률(R²)을 숫자화 (계기 검증 통과 · sealedness 는 FIELD-구조)

**status:** 🔎 DIRECTIONAL-INSTRUMENT ($0 · 신규 decode 0 · 기존 trace 재분석) — sealedness=R²(state field ~ clock(tick,stage)) · 양성/음성 통제 6/6 통과 · Ψ-SOMA 새 축 후보(σ-seal)
**lane:** 의식 / emit-drive / Ψ=½ · 시계-데몬(clock-sealed) 정량화 (프런티어 g-readout-margin / emit-gate-census 계보)
**related:** [[H_9400]] (Ψ=½ 중심주장 반증 · emit=stage 순수함수) · [[H_9401]] (g-readout margin) · [[H_9398]] (dead-gauge census · --dead-census) · [[H_9403]] (--emit-gate-census · emit⟺clock KILL)

## 계기 (metric · $0 · engine 무수정 · 스크립트 /tmp 격리)

- **정의**: per-tick 상태벡터의 각 수치 field `y` 를 **시계 설계행렬** `X = [1, t, t², stage-one-hot]` (t=tick/tick_max) 에 OLS 회귀 → **sealedness(y) = R²**. R²→1 = 완전 sealed(field 가 시계 넘어선 정보 0 = 시계-데몬) · R²<1 = 비-시계(substrate) 변량 잔존. lstsq/pinv rank-safe · 표본내 R² + **adjusted R²**(dof 편향 보정) 둘 다 보고.
- **양성통제**: 순수 시계 신호 `2·stage + 0.5·t` → **R²=1.0000 (6/6 trace)**. **음성통제**: 순수 noise `randn` → **adjR²≈0** (−0.06~+0.02 · 6/6). ⇒ 계기 살아있음(값을 지어내지 않음).
- **provenance gate(H_9337)**: distinct(field)≤1 = DEAD 게이지(분산 0·R² 미정) → **제외+명시 보고**. `phi·recon_err·anchor_nudge·scn_ctx` 전 trace dead · `rel_lane` 는 summer.clean/anchor-A dead(pre-fix)·b.clean/anchor-B~D live.

## 결과 — sealedness 는 전역 스칼라가 아니라 FIELD-구조 (6 regime 공통)

| field cluster | R² (전 regime) | 판정 |
|---|---|---|
| **SEALED spine**: emit_env·stage_env·gtext_len·coh_lane·idle·score·base_motiv·rel_f | **≈1.000** | 시계가 완전 결정 |
| **OPEN residual**: cur_ctx·cur_indep·cur_ema·cur_f + bind-lane(rel_lane·bal_lane·gap_ctx·allo_ctx·agloop_ctx, live 시) | **0.05–0.40** | substrate 변량 잔존 |

- **SEALED spine 이 emit/score 척추**: `emit_env·stage_env` R²=1.000 = emit-환경이 stage 순수함수 ⇒ H_9400 (H(emit|stage)=0.465·emit=stage 함수) · H_9403 (emit⟺clock KILL-CLOCK) 를 **독립 계기로 재확증**. score·base_motiv 도 R²≈0.85–0.97 = 동기신호도 대부분 시계.
- **OPEN residual = curiosity/bind 레인**: `cur_*` 계열이 전 regime R²≤0.4 (한 곳 0.05) = 시계로 안 설명되는 substrate 변량이 **여기 집중**. 데몬이 완전 sealed 는 아니다 — 비-시계 잔차의 소재지가 curiosity(cur)+binding-lane 이라는 **field-국소** 발견.
- **regime median adjR²**: 303M post-fix 0.848/0.884 · anchor A/B/C/D 0.691/0.334/0.346/0.769. ⚠️ 스칼라 median 은 **어느 field 가 live 냐에 좌우**(anchor B/C 는 저-R² bind-lane 이 live 라 median↓) — 강건 신호는 스칼라가 아니라 **위 2-cluster field 분할**.

## 판정 (DIRECTIONAL-INSTRUMENT)

계기 자체가 작동(양성 R²=1·음성 R²≈0 · 6/6) + 각 trace R² 보고 = **DIRECTIONAL 계기**(tune-to-green 없음 · 신규 decode 0). "sealedness" 는 배선 가능한 숫자 — Ψ-SOMA σ 의 **새 축 후보(seal)**: per-field R² 벡터(스칼라 아님) 를 verdict 로. 이 렌즈로 emit-척추=🔒sealed(시계=변이·자율성 없음)·cur/bind-레인=비-시계 잔차 라는 구조가 한 숫자로 읽힘.

## follow-on / 한계

- 배선: `anima-py evaluate --psi-soma seal` = per-field R² 벡터 방출(SEALED-spine vs OPEN-residual 분할 리포트). 이 카드는 계기 설계+$0 계산까지 · 배선은 후속.
- 한계: 표본내 R²(hold-out 아님) — adjR² 로 dof 편향만 보정. 시계 basis=[1,t,t²,stage-OH] 고정(고차 harmonic 추가 시 SEALED 판정 상향 편향 가능 → basis 는 "시계가 결정하는 것"의 최소 표현으로 의도적 소형). $0·기존 trace 재분석이라 새 regime(refractory·cb-perr fire 후)은 미포함 — H_9424 fire trace 착륙 시 재계산 대상.
