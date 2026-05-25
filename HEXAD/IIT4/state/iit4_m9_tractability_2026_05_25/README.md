# IIT4 M9 — tractability profile + bounded-mode lib

**날짜** 2026-05-25 · **비용** $0 mac-local · hexa-only · LLM none · NO GPU · deterministic

faithful IIT 4.0 엔진(`HEXAD/IIT4/lib/`)의 **tractable-n 천장**을 측정·확장한다. 기존
lib 은 한 줄도 수정하지 않는다(신규 lib 1개 + 신규 state 디렉터리만). DESIGN.md §3 의
비용 envelope("relations 가 조합 폭발", exact n≤5 / big-Φ n≤6)를 실측으로 뒷받침하고,
큰 n 을 실행 가능하게 만드는 **bounded-mode 근사**를 제공한다.

---

## 1. 왜 비싼가 (비용 구조)

exact `big_phi(tpm, n, sys_state)` 의 지배적 비용은 distinction 수집 단계에 있다:

- 메커니즘 2ⁿ−1 개 각각에 대해 `mice_cause`/`mice_effect` 가
  **모든 purview 2ⁿ−1 개**를 훑는다(argmax).
- 각 purview 평가(`small_phi_*`)는 그 purview·mechanism 의 directional bipartition
  집합(2^|M| × 2^|Z|)을 다시 enumerate 한다.
- 그 뒤 distinction nd 개에 대해 relation 이 O(nd²) 로 binding 되고(2nd-order),
  system big-Φ 는 2^(n−1)−1 개의 directional bipartition 마다 구조를 재합산한다.

즉 distinction 단계가 대략 **(2ⁿ)² × 분할** 으로 super-exponential 하게 커진다 — n 이
하나 늘 때마다 wall 이 10× 안팎으로 뛴다.

## 2. wall-cost 프로파일 (ECA rule 110, 실측)

`time` 으로 `hexa run` 을 감싼 mac-local 단일 측정(`POOL_DISABLE=1`, 직접 바이너리).
exact = `big_phi`, bounded(cap=3) = `big_phi_bounded(..., 3)`. wall 은 컴파일+실행 포함.

| n | 메커니즘 2ⁿ−1 | exact big-Φ wall | bounded(cap=3) wall | nd (distinctions) | 비고 |
|---|---|---|---|---|---|
| 4 | 15  | **~1.3 s**   | (cap≥n → exact 와 동일) | 12 | mac-local 초 단위 |
| 5 | 31  | **~14.6 s**  | — | 21 | ~11× (n=4 대비) |
| 6 | 63  | **~784 s (13:04)** | **~214 s (3:34)** | 30 / cap3=15 | exact 분 단위 폭발 / bounded ~3.7× 절감 |
| 7 | 127 | (수십 분+ — 본 측정에서 deferred) | bounded 로 접근 가능 | — | exact 비현실적 |

측정값(rule 110): n=4 big-Φ=15.0339 · n=5 big-Φ=36.114 · n=6 exact big-Φ=66.8152
(total=82.8345, nd=30). n=6 exact·bounded 측정은 다른 agent worktree 의 동시 부하와 겹쳐
절대 wall 이 부풀려졌으나(컴파일 포함), **n→n+1 super-exponential 증가**(1.3s→14.6s→784s,
≈11× 후 ≈54×)와 **bounded≪exact** 관계는 그대로 성립한다.

스케일 규칙: exact wall 이 n→n+1 마다 한 자릿수 배수 이상으로 폭증 (초→분). 이것이
DESIGN.md §3 "relations 조합 폭발 · big-Φ n≤6" 경계를 실측으로 확정한다.

## 3. bounded-mode 근사 (`iit4_bounded.hexa`)

`big_phi_bounded(tpm, n, sys_state, max_purview_size)` — MICE argmax 를 **크기(popcount)
≤ max_purview_size 인 purview 로만** 제한한다. 그 외 모든 계산(분할·distinction binding·
relation·system MIP)은 exact `big_phi` 와 **바이트 동일**하다. purview 후보당 상태공간이
2^|purview| 이므로 가장 큰 purview 들을 먼저 잘라내 가장 비싼 평가를 제거한다.

### 3.1 충실한 제한 vs 근사 (정직성 · g5)

- **max_purview_size ≥ n** → cap 이 아무것도 배제하지 않음 ⇒ **충실한 RESTRICTION** 이며
  exact `big_phi` 와 **정확히 일치**한다(M9 smoke 에서 검증, "no-op cap 항등식").
- **max_purview_size < n** → 큰 purview 가 argmax 에서 빠짐. 보고되는 φ_d 는 각 메커니즘의
  참 small-φ 에 대한 **하한(lower bound)** 이다(제약된 argmax ≤ 비제약 argmax). 따라서
  capped 모드는 **명시적 APPROXIMATION** 이며 exact IIT 4.0 big-Φ 가 **아니다**. 큰 n 을
  실행 가능하게 만드는 대가로 고-φ 큰 purview 를 놓칠 수 있는 tractability tradeoff 다.
  본 lib 은 capped 값을 faithful 이라 주장하지 않는다.

### 3.2 bounded-vs-exact 일치 (smoke 결과)

| 케이스 | exact big-Φ | bounded(cap≥n) | 일치? |
|---|---|---|---|
| COPY n=2 (state 11) | 2.0      | 2.0      | ✅ 정확 일치 (ε=1e-6) |
| ECA110 n=4 (state 1010) | 7.5475 | 7.5475 | ✅ 정확 일치 (M6 ref) |

capped(cap=2 < n=4): big-Φ=4.48605, total=6.23624 → Σφ_d·total 이 exact 의 **하한**임을
확인(`capped ≤ exact`). n=6 bounded(cap=3): big-Φ=6.79534, total=12.1123, nd=15 — 유한·
[0,total] 경계 충족(exact n=6 가 분 단위로 폭발하는 지점에서 bounded 는 finite).

## 4. 문서화된 실용 exact-n 천장

- **distinctions(M2)**: exact n≤8 (DESIGN §3 그대로 — 2^n≤256 repertoire 폭, mac-local).
- **relations / full Φ-structure(M3)**: exact **n≤5** · n=6 best-effort · n≥7 deferred.
- **big-Φ(M4) exact**: 실용 천장 **n≤5 가 초 단위, n=6 은 분 단위(경계선)**. n≥7 exact 는
  본 환경에서 비현실적(수십 분+).
- **bounded(M9)**: max_purview_size 를 작게 잡으면(예: 3) **n=6 이 유한·tractable**, n≥7 도
  접근 가능 — 단 capped 일 때는 근사(하한)임을 명시.

요약: **exact 실용 천장 = n≤5 (편안) / n=6 (경계선, 분 단위)**. bounded-mode 는 정확도를
명시적으로 양보(하한 근사)하는 대신 그 천장을 n=6→n≥7 로 밀어 올린다.

## 5. 산출물

- `HEXAD/IIT4/lib/iit4_bounded.hexa` — bounded-mode lib (신규 · import-safe · `iit4_bigphi`
  체인 import).
- `state/iit4_m9_tractability_2026_05_25/run_m9.hexa` — smoke (16/16 PASS): no-op cap 항등식
  (COPY n=2 + ECA110 n=4) · capped 하한성 · n=6 유한성 · 결정론.
- `result.json` — 타이밍 표 + bounded-vs-exact 일치 + verdict.

## 6. 정직한 scope (C3)

- 타이밍은 mac-local 단일 측정(컴파일 포함 wall). 절대치는 머신·부하에 따라 변동하나
  **n→n+1 ≈10× 스케일**과 **bounded≪exact** 관계는 견고하다.
- bounded 의 capped 분기는 **하한 근사**다 — exact 와의 절대 오차는 substrate·state·cap 에
  의존하며, faithful 값으로 사용해선 안 된다(§3.1).
- bounded 는 purview-크기 cap 만 적용한다. relation 차수(2nd-order)·partition scheme 은
  M3/M4 와 동일 상속(추가 근사 없음). 더 공격적인 mechanism-수 cap 은 deferred.
