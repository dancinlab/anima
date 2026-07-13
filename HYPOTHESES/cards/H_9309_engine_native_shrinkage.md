# H_9309 — engine-native 전이: shrinkage head + 성장 수리를 live `core/` 에 배선

**Tier: 🔵 ENGINE-NATIVE WIRED (E1 ∧ E2 · live `core/engine_cli`) · group MITOSIS-ENGINE · 2026-07-14**

- script/smoke → `state/h9309_engine_shrinkage/{h9309_engine_smoke.py, smoke_run.log, h9309_smoke_result.json}`
- 배선 → `core/engine_cli.hexa` (`_jh_pooled` · `_jh_counts_wb` · `jamo_head_grow_shrink`) + `core/engine_cli.py` 쌍둥이 lockstep
- 선행 → H_9298 🟢 (WB shrinkage) · H_9301 🟢 (성장 수리 + 이중해리) — 둘 다 **mirror = DIRECTIONAL** 이었다
- 경계 → H_9306 🧱 (되산 양 < 벽 높이면 벽은 그대로 선다)

## 왜 이 카드가 필요한가

H_9298/H_9301 은 numpy 미러였다 ⇒ hard-gate 1(`a_engine_native_learning`)에 의해 **DIRECTIONAL**. tier 를 올리는 **유일한 경로**는 live `core/` 배선이다(gate 7 · `a_verified_must_wire`).

## 배선 (기존 검증 경로 보존)

기존 `jamo_head_grow` / `_jh_counts` 는 **손대지 않았다** — H_1321 의 GREEN 수치(engine-native CE 2.82046 · smoke 73/0)가 byte-재현 가능하게 남아야 하므로, **새 faculty 를 그 옆에 병렬 추가**했다.

| 새 faculty | 내용 |
|---|---|
| `_jh_pooled` | 루트(전 셀 풀링) 다음-심볼 분포 = 굶주린 셀이 강도를 빌릴 **부모** |
| `_jh_counts_wb` | `P(next\|cell) = λ·MLE(cell) + (1−λ)·P_pooled`, **λ = n/(n+T)** (Witten-Bell) — 자유 하이퍼 0 ⇒ 스윕할 손잡이가 없으므로 **tune-to-green 이 구조적으로 불가능** |
| `jamo_head_grow_shrink` | 동일한 gradient-free Voronoi 성장 + **성장 수리**(퇴화 median 분할 → 그 셀만 blacklist, 루프 전체를 죽이지 않음) + WB head |

`hexa typecheck core/engine_cli.hexa` → **OK**. py 쌍둥이 lockstep. VERSION 0.13.11 → 0.13.12 (gate G5).

## 동결 bar 2개 (각각 자기 양성대조 보유)

배선만 하고 "됐다"고 하면 `wire-to-prod` 위반이다. **구 faculty 와 구별되지 않는 배선은 배선이 아니고**, 고장난 faculty 도 통과하는 bar 는 theatre 다.

### E1 GROWTH-UNCAPPED — ✅ PASS

| | 기존 `jamo_head_grow` | 수리된 `jamo_head_grow_shrink` |
|---|---|---|
| grow_max=64 에서 도달 셀 | **14** | **22** |

⇒ **엔진의 셀 풀도 퇴화분할 `break` 에 갇혀 있었다**(mirror 에서만이 아니라). 수리가 live 로 발화한다.

### E2 STARVATION-DISSOCIATION — ✅ PASS (head 만 격리)

같은 파티션을 **한 번 성장시킨 뒤** 엔진 자신의 `_jh_counts` / `_jh_counts_wb` 로 head 만 두 번 재구성해 채점 — 중심·소유자·테스트셋 동일, **추정기만 다르다**.

| cells | 셀당 점 | FLAT | SHRINK | Δ |
|---|---|---|---|---|
| 4 | ~500 | 4.83107 | 4.86053 | **+0.029** (넉넉하면 shrinkage 는 순수 희석 = 손해) |
| 16 | ~125 | 4.98423 | 4.95945 | −0.025 |
| 64 | ~31 | 5.04998 | **4.89979** | **−0.150** (굶주릴수록 이득) |
| **스윕 열화** | | **+0.21891** | **+0.03926** | **5.6배 적게 열화** |

⇒ **H_9301 의 이중해리가 엔진 자체 파티션 위에서 재현**된다. 게다가 **부호가 셀 밀도에 따라 뒤집히는 것**까지 보인다 — 법칙이 예측하는 정확한 모양이다(분할비용이 없으면 shrinkage 는 손해, 있으면 이득).

## ⚠️ 계측 가드가 두 번 판독을 막았다 (bar 무이동 · 정직 보고)

E2 의 KILL/UNREADABLE 가드(*"FLAT 이 열화하지 않으면 굶주림이 안 걸린 것 — 판독 금지"*)가 **두 번 발동**했다:

1. **1차** (VJ=12 · coarse=6): FLAT 이 −0.287 **개선**. 문맥이 36개뿐이라 14 셀로는 안 굶었다.
2. **2차** (VJ=12 · coarse=40): FLAT 이 −0.154 **개선**. 9 pts/cell 이어도 **Laplace-12 가 이미 충분**했다.

**진단**: faculty 가 아니라 **어휘 크기가 축을 안 걸었다**. WB 가 살 것이 있으려면 **T(관측 타입 수)가 n(셀당 토큰)에 필적**해야 한다(λ = n/(n+T)). 미러의 영역은 **Vj=323 · ~130 pts/cell** (λ≈0.7) 인데, VJ=12 에서는 굶주림 자체가 없어 **고칠 것이 없었다**. 3차에서 VJ=200 으로 올리자 FLAT 이 +0.219 열화하며 축이 걸렸다.

> **bar 는 한 번도 움직이지 않았다.** 움직인 것은 *스트림이 bar 가 말하는 영역에 도달하게* 하는 계측 파라미터다. "스윕이 flat 하면 효과 없음이 아니라 축이 안 걸린 것" — convergence `mitosis-estimator-1` 의 규칙 ①이 자기 카드에서 두 번 작동했다.

## HONEST (경계 · H_9306 상속)

- **shrinkage 는 분할이 파괴한 분산을 되살 뿐, 정보를 만들지 않는다.** 되산 양이 벽보다 작으면 벽은 그대로 선다(H_9306: 회수 −0.035 < 벽 +0.069 ⇒ H_1310 UPHELD). **이 배선은 추정기 결함을 제거한 것이지 능력 주장이 아니다.**
- toy 합성 스트림 위 smoke (a_scale_honest_scope). 303M 실코퍼스 위 engine-native 재측정 = follow-on.
- 기존 `jamo_head_grow` 경로 **불변** ⇒ H_1321 GREEN 재현성 보존.
