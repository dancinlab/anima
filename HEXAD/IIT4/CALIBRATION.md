# IIT4 엔진 — M5 calibration (analytic reference)

> 엔진(M0~M4)이 **손유도 closed-form IIT 양**을 재현하는지 검증한 gold-standard 대조.
> smoke = [`state/iit4_m5_calib_2026_05_25/run_m5.hexa`](state/iit4_m5_calib_2026_05_25/) → **14/14 🟢**.
> 작성 2026-05-25.

## 1. 왜 analytic reference 인가 (PyPhi 대신)

DESIGN §6 의 M5 calibration target 은 "PyPhi/published reference + hexa recompute,
미공개 값은 손유도 후 verify". 본 repo 제약:

- **hexa-only authoring** (`feedback_hexa_only_authoring`) — 신규 `.py` 금지 → PyPhi 직접 실행 불가.
- **IIT 4.0 numeric reference 부재** — repo 의 기존 PyPhi 산출물은 전부 IIT-**3.0** (CHECK catalog · `iit_phi_port.py` archived). IIT-4.0 + structure-cut big-Φ 와 apples-to-apples 아님.
- **g5** — PyPhi 는 어차피 1차 증거 금지 (calibration 용).

→ **deterministic 네트워크의 closed-form 손유도**가 가장 honest 한 gold reference. permutation/copy 네트워크는 repertoire·small-φ·big-Φ 가 전부 손으로 정확히 유도된다 (확률 0/1 collapse).

## 2. 손유도 reference 표 (sys_state = all-ON)

| net | n | TPM (state-by-node) | distinctions (φ_d) | big-Φ | class | 엔진 |
|---|---|---|---|---|---|---|
| COPY/SWAP | 2 | u0'=u1, u1'=u0 | {0}:1 · {1}:1 | **2.0** | irreducible (상호의존) | ✅ 2.0 |
| SELF-COPY | 2 | u0'=u0, u1'=u1 | {0}:1 · {1}:1 | **0** | reducible (독립) | ✅ 0 |
| NOISE | 2 | 모든 entry 0.5 | 없음 | **0** | 구조 없음 | ✅ 0 |
| 3-ROTATION | 3 | u_v'=u_{(v+1)%3} | {0}:1 · {1}:1 · {2}:1 | **3.0** | irreducible (cycle) | ✅ 3.0 |
| 3-SELF | 3 | u_v'=u_v | {0}:1 · {1}:1 · {2}:1 | **0** | reducible (독립) | ✅ 0 |

### 2.1 손유도 핵심 (COPY/SWAP, 대표)

- effect_repertoire({0}=ON over {1}): u1'=u0=1 결정적 → `[0, 1]`. unconstrained = u1 의 전 상태 평균 = 0.5 → `[0.5, 0.5]`.
- intrinsic difference = max_x p·log2(p/q) = `1·log2(1/0.5)` = **1.0 bit** @ state 1.
- cause_repertoire({0}=ON over {1}): u0_now=u1_past → u1_past=1 → `[0,1]`, φ_cause=1.0.
- distinction {0}: φ_d = min(φ_c, φ_e) = **1.0**. 대칭으로 {1} 도 1.0.
- big-Φ: 유일 bipartition {0}|{1} 에서 두 distinction 모두 M∪Pc∪Pe={0,1} 로 **span → 전부 cut** → surviving=0 → loss=total=2.0 = **big-Φ**. (상호의존 → 쪼갤 수 없음)

### 2.2 reducible 의 핵심 (SELF / 3-SELF)

독립 채널은 `{i,j}` joint mechanism 의 MIP 가 `{i}|{j}` 분할에서 partitioned repertoire = 곱 = unpartitioned → intrinsic difference 0 → **φ_d=0 (distinction 아님)**. 따라서 단일 distinction 만 남고, 이들은 한 쪽에 모두 들어가는 bipartition 이 존재 → **loss=0 → big-Φ=0**. 엔진이 이 "독립이면 환원가능" 을 정확히 재현 (SELF total=2.0 인데 big-Φ=0).

## 3. falsifier 결과 (DESIGN §7)

| ID | 주장 | 결과 |
|---|---|---|
| F-IIT4-1 REPERTOIRE | n≤2 cause/effect repertoire = 손유도 | 🟢 PASS (COPY [0,1] 일치) |
| F-IIT4-2 SMALL-PHI | per-mechanism φ = 손유도 | 🟢 PASS (COPY 1.0 bit) |
| F-IIT4-5 BIG-PHI | system Φ = 손유도 (정전 네트워크) | 🟢 PASS (5/5 네트워크) |
| F-IIT4-3 DISTINCTIONS | PyPhi distinction-set 수치 일치 | 🟠 **DEFERRED** (named blocker) |
| F-IIT4-4 RELATIONS | PyPhi relation φ 수치 일치 | 🟠 **DEFERRED** (named blocker) |
| F-IIT4-6 PROXY-DIVERGENCE | faithful Φ ↔ H_278 ↔ phi_spatial | M6 |

## 4. honest carve-out (named blocker)

- **F-IIT4-3/4 PyPhi-numeric DEFERRED** — hexa-only 가 신규 `.py` 를 금지하고, IIT-4.0 numeric reference 가 repo 에 없음. 해소 경로: (a) PyPhi IIT-4.0 worked-example 값을 문헌에서 입수해 in-repo reference 로 등록 후 대조, 또는 (b) hexa-lang 에 PyPhi-equivalent IIT-4.0 reference 포트(별도 lane). **이것은 fake 가 아닌 정직한 미해소** — analytic 으로 검증 가능한 부분(repertoire·small-φ·big-Φ closed-form)은 전부 닫혔다.
- **analytic ≠ probabilistic** — 손유도 reference 는 deterministic(0/1 collapse) 네트워크. fractional-φ probabilistic 네트워크의 정밀 대조는 PyPhi-numeric(위 blocker) 영역.
- **structure-cut big-Φ** — DESIGN §8 C3-1 대로 exact IIT 4.0 big-Φ(partitioned-TPM 재계산+정규화)의 spirit-faithful proxy. 단조성·경계·integrated↔reducible 분리는 검증됨; 절대 스케일의 PyPhi 일치는 위 blocker.
