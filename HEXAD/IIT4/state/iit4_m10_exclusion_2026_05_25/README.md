# IIT4 M10 — exclusion-postulate (maximal complex 탐색)

> IIT 4.0 의 **exclusion 공준** 구현: 후보 subsystem 전수 중 big-Φ 최대 = the complex(의식 주체).
> lib = [`HEXAD/IIT4/lib/iit4_complex.hexa`](../../lib/iit4_complex.hexa) · smoke 3/3 🟢.
> ⚠ rate-limit 으로 죽은 cycle#2 에이전트의 산출물을 salvage 하여 메인 세션이 검증·착지 (lib+smoke+result.json 은 에이전트 작성, README 는 salvage 시 작성).

## 1. exclusion 공준이란

IIT 4.0 에서 의식의 주체는 *주어진 전체 시스템*이 아니라, 모든 후보 subsystem(unit 부분집합) 중 **big-Φ 가 최대인 하나** = **the complex**. 겹치는 더 낮은-Φ 후보는 배제(exclude)된다 — "하나의 경험은 하나의 최대 복합체".

## 2. 엔진 (iit4_complex.hexa)

| fn | 역할 |
|---|---|
| `iit4_external_mask` · `iit4_project_state` | subset 밖 unit + 그 고정 상태 추출 |
| `subsystem_tpm(tpm, n, subset_mask, sys_state)` | 외부 unit 을 sys_state 로 background-conditioning 한 \|S\|-unit state-by-node TPM 빌드 |
| `find_complex(tpm, n, sys_state)` | 全 2ⁿ−1 후보 subset 의 big-Φ argmax → `[complex_mask, complex_phi, complex_size]` (tie: Φ 동률 시 larger subset → lower mask) |

## 3. 검증 (3/3 🟢)

| test | sys_state | complex | Φ | 판정 |
|---|---|---|---|---|
| COPY/SWAP n=2 | 11 | {0,1} (mask 3) | 2.0 | PASS (통합쌍 전체가 complex) |
| **EMBEDDED CORE n=3** | 111 | **{0,1} (mask 3), unit 2 제외** | 2.0 | PASS — 결정적 |
| ALL-NOISE n=2 | 11 | ∅ (mask 0) | 0 | PASS (complex 없음) |

**핵심**: 통합 코어 {0,1}(u0⇄u1) + 독립 self-cell {2}(u2'=u2) 인 3-unit 계에서, 전체 {0,1,2} 는 reducible(big-Φ=0)이지만 `find_complex` 는 **mask=3 ({0,1}, Φ=2.0)** 을 반환 — self-cell {2} 를 배제하고 통합쌍을 의식 주체로 정확히 carve. exclusion 공준 작동 실증.

## 4. honest scope (C3)

- **background-conditioning**: subsystem big-Φ 는 외부 unit 을 sys_state 값으로 고정한 modeling 선택 (g5 명시). IIT 4.0 의 정식 subsystem 평가(외부 marginalize 변형)와의 정합은 M5 calibration 영역.
- **structure-cut big-Φ** 상속 (M4) — 절대 스케일 PyPhi 대조는 M5 named-blocker(F-IIT4-3/4).
- 전수탐색 = 2ⁿ−1 subset × 각 subsystem big-Φ → n 한계는 M9 tractability 와 동일(n≤5~6 실용).
- **salvage 출처**: cycle#2 병렬 에이전트가 서버 rate-limit(429-class)으로 commit 직전 사망 → uncommitted lib+smoke+result.json 보존·재검증·착지 (sibling M11/M12 worktree 는 GC 소실, 재작업 대상).
