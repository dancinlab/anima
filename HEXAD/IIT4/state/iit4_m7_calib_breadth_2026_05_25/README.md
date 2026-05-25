# IIT4 M7 — calibration breadth (확장 analytic reference)

> M5 의 손유도 calibration(COPY/SELF/NOISE/3-ROT/3-SELF)을 손으로 닫을 수 있는
> deterministic 정전 네트워크로 **넓힌** 대조 suite.
> smoke = [`run_m7.hexa`](run_m7.hexa) → **35/35 🟢** · 작성 2026-05-25 · $0 mac-local.

## 0. 왜 또 analytic 인가 (PyPhi 대신)

M5 와 동일한 제약이 그대로다:

- **hexa-only authoring** — 신규 `.py` 금지 → PyPhi 직접 실행 불가.
- **IIT-4.0 numeric reference 부재** — repo 의 기존 PyPhi 산출물은 전부 IIT-**3.0**
  (CHECK catalog · archived `iit_phi_port.py`). IIT-4.0 + structure-cut big-Φ 와
  apples-to-apples 아님.
- **g5** — PyPhi 는 어차피 1차 증거 금지.

따라서 M7 도 **deterministic 네트워크의 closed-form 손유도**를 gold reference 로
쓴다. M5 와 다른 점: (a) 게이트 네트워크의 **분수 φ** 까지 손으로 닫고, (b)
**De Morgan 쌍대성**·(c) **출력 state-blind ⇒ Φ=0**·(d) **neighbor-coupled ring**·
(e) **ECA bridge 가 M5 정답을 byte-equal 로 재현**하는 좌표축까지 추가로 닫는다.
어떤 published 수치도 입수/인용하지 않았으므로 fabricate 는 없다.

## 1. 추가한 네트워크 (sys_state 명시) — 7 좌표

| net | n | driver | distinctions(φ_d) | big-Φ | class | 엔진 |
|---|---|---|---|---|---|---|
| AND2 @all-ON | 2 | u0'=u1'=AND(u0,u1), s=11 | {0}:½ {1}:½ | **1.0** | irreducible (분수) | ✅ 1.0 |
| OR2 @all-OFF | 2 | u0'=u1'=OR, s=00 (AND dual) | {0}:½ {1}:½ | **1.0** | irreducible (쌍대) | ✅ 1.0 |
| XOR2 | 2 | u0'=u1'=XOR | 없음 | **0** | distinction 없음 | ✅ 0 |
| AND2 @all-OFF | 2 | u0'=u1'=AND, s=00 | {0}·{1}: (⅔)log₂(4⁄3) | **2·(⅔)log₂(4⁄3)** | irreducible (분수) | ✅ 0.553383 |
| ANDRING3 @all-ON | 3 | u_i'=AND(좌,우) ring, s=111 | {0}{1}{2}:½ | **1.0** | irreducible (ring) | ✅ 1.0 |
| ECA204 (id) @all-ON | 3 | eca_tpm(204,3)=self-loop | {0}{1}{2}:1 | **0** | reducible (독립) | ✅ 0 |
| ECA170 (shift) @all-ON | 3 | eca_tpm(170,3)=우-shift | {0}{1}{2}:1 (+ho) | **3.0** | irreducible (cycle) | ✅ 3.0 |

## 2. 손유도 (closed-form)

표기: 단위 i = bit i. `tpm[s·n+u] = P(u'=ON | state s)`.
ID(p‖q) = maxₓ p(x)·log₂(p(x)/q(x)) (KL 합이 아닌 pointwise 최대).

### 2.1 AND2 @ all-ON (s=11) — 대표 분수 케이스

TPM(state-by-node): `[0,0, 0,0, 0,0, 1,1]` (s=11 에서만 둘 다 ON).

- **effect {0}=ON over {1}**: u0 를 ON 으로 고정하고 u1 평균 →
  P(u1'=ON)=½(s=01→0, s=11→1) → p=[½,½]. unconstrained over {1} = 전 상태 평균
  =(0+0+0+1)/4=¼ → q=[¾,¼]. ID = ½·log₂(½ ⁄ ¼)=½·1 = **½ @ ON**.
  유일 cut(mech⊥purview) → q=unconstrained → φ_e=½.
- **cause {0}=ON over {1}**: 과거 u1 별 likelihood(u0'=ON, u0 평균) =
  [u1=0 : 0, u1=1 : ½] → 정규화 [0,1]. q=uniform[½,½].
  ID = 1·log₂(1 ⁄ ½) = **1 @ u1=ON**. MIP cut → φ_c=1.
- **φ_d{0}=min(1,½)=½** · 대칭으로 {1} 도 ½. → Σφ_d=1.0.
- **relation**: 두 distinction 모두 cause·effect 를 단위 {0} 에 ON 으로 specify →
  congruent overlap → φ_r=min(½,½)=½. total = 1.0 + ½ = **3⁄2**.
- **big-Φ**: cut {0}|{1} 에서 mech{1} 은 M∪Pc∪Pe={0,1} 로 span→파괴, mech{0} 은
  {0} 한쪽→생존. relation 도 한쪽만 남아 파괴. 생존 = ½ → loss = 3⁄2 − ½ = **1.0**.

### 2.2 OR2 @ all-OFF (s=00) — De Morgan 쌍대

OR(a,b)=¬AND(¬a,¬b). 따라서 OR2 를 all-OFF(s=00)에서 보면 AND2 를 all-ON 에서 본
것과 비트-반전 대칭 → **모든 IIT 양이 §2.1 과 동일**: φ_c{0}=1, φ_e{0}=½,
φ_d=½, total=3⁄2, big-Φ=**1.0**. 엔진이 두 네트워크에서 같은 big-Φ 를 내는지로
쌍대성을 검증한다 (`matches AND2 all-ON` check).

### 2.3 XOR2 — 출력 state-blind ⇒ Φ=0

u'=XOR(u0,u1). 임의 단위를 고정해도 나머지 단위에 대한 marginal P(u'=ON)=½ (XOR
은 한 입력을 알아도 출력 확률이 항상 ½). → effect ID=0 ⇒ effect 거리 0. 단일
mechanism 의 cause 도 MIP 에서 0 으로 환원 → **distinction 하나도 없음 (nd=0)**
→ Σφ_d=0, φ_r=0, **big-Φ=0** (all-OFF, all-ON 양쪽). "출력이 입력 상태에
무관하면 의식 구조가 없다" 를 정확히 보여주는 경계 케이스.

### 2.4 AND2 @ all-OFF (s=00) — 분수 closed-form

- **effect {0}=OFF over {1}**: u0=OFF 고정 → u1'=AND(0,·)=0 항상 → p=[1,0].
  q=[¾,¼]. ID = 1·log₂(1 ⁄ ¾) = **log₂(4⁄3) @ OFF** ≈ 0.415037 → φ_e.
- **cause {0}=OFF over {1}**: 과거 u1 별 likelihood(u0'=OFF) = [u1=0 : 1,
  u1=1 : ½] → 정규화 [⅔,⅓]. q=[½,½]. ID = ⅔·log₂(⅔ ⁄ ½) =
  **(⅔)·log₂(4⁄3) @ OFF** ≈ 0.276692 → φ_c.
- **φ_d{0}=min = (⅔)log₂(4⁄3)** · 대칭 {1}. Σφ_d = 2·(⅔)log₂(4⁄3) ≈ 0.553383.
- **big-Φ**: cut 가 relation(≈0.276692)을 끊고 한 distinction 흐름만 남겨 →
  loss = Σφ_d = **2·(⅔)log₂(4⁄3)** ≈ 0.553383 (엔진과 일치, bound big-Φ≤total 충족).
- 이 케이스는 M5(전부 0/1 정수 φ)에 없던 **명시적 분수 φ closed-form** 을 닫는다.

### 2.5 ANDRING3 @ all-ON (s=111) — neighbor-coupled

u_i'=AND(u_{i-1}, u_{i+1}) (자기 자신 제외, 주기 ring). all-ON 에서:

- **single mech{0} cause**: u0'=AND(u1,u2)=ON ⇒ 과거 {1,2}=ON 필요. best cause
  purview {1,2} 에서 p 가 (1,1)에 집중. MIP 가 한 단위만 cut → q(x*)=½ →
  φ_c = 1·log₂(1 ⁄ ½) = **1**.
- **single mech{0} effect**: 이웃 한 단위에 대해 P=½ → φ_e = **½** (§2.1 과 동형).
- **φ_d{i}=min(1,½)=½**, 세 단위 대칭 → nd=3, Σφ_d=3⁄2.
- relation φ_r=½(겹치는 한 쌍) → total=2.0. big-Φ = **1.0** (least-damaging cut
  이 single distinction 하나의 흐름을 잃음; 엔진과 교차검증).

### 2.6 ECA bridge — M6 substrate 경로가 M5 정답을 byte-equal 로 재현

`eca_tpm(rule,n)` 으로 만든 TPM 이 M5 손유도 TPM 과 **바이트 동일**한지 + big-Φ 가
같은지 두 단계로 검증한다 (substrate→causal 다리의 정합성).

- **eca_tpm(204,3) == 3-SELF**: rule 204 = `next = center`(자기복사). 24개 entry
  가 build_self3 과 byte-equal. 독립 self-loop ⇒ **reducible big-Φ=0**, nd=3.
- **eca_tpm(170,3) == 3-ROTATION**: rule 170 의 출력비트 = neighborhood index 의
  최하위 비트 = **우측 이웃 R** ⇒ u_i'=u_{(i+1)%3} (우-shift). build_rotate3 과
  byte-equal. cycle ⇒ **irreducible big-Φ=3.0** (M5 3-ROT 정답 재현).

## 3. falsifier 결과 (DESIGN §7)

| ID | 주장 | 결과 |
|---|---|---|
| F-IIT4-1 REPERTOIRE | repertoire = 손유도 closed-form | 🟢 PASS (AND2/OR2/ANDRING3) |
| F-IIT4-2 SMALL-PHI | per-mechanism φ = 손유도 (분수 포함) | 🟢 PASS (½ · 1 · log₂(4⁄3) · (⅔)log₂(4⁄3)) |
| F-IIT4-5 BIG-PHI | system Φ = 손유도 (정전 네트워크) | 🟢 PASS (7/7 확장 네트워크) |
| F-IIT4-3 DISTINCTIONS | PyPhi distinction-set 수치 일치 | 🟠 **DEFERRED** (named blocker) |
| F-IIT4-4 RELATIONS | PyPhi relation φ 수치 일치 | 🟠 **DEFERRED** (named blocker) |

## 4. calibration space — 닫힌 면적 vs PyPhi-deferred

**닫힌(analytic) 좌표** — M7 후:

- 정수 φ(0/1-collapse): COPY/SELF/NOISE/3-ROT/3-SELF (M5) + ECA204/ECA170 (M7, bridge).
- **분수 φ closed-form**: AND2 all-OFF = 2·(⅔)log₂(4⁄3) ✅ (M7 신규).
- **De Morgan 쌍대성**: OR2 ↔ AND2 ✅ (M7 신규).
- **출력 state-blind ⇒ Φ=0**: XOR2 ✅ (M7 신규).
- **neighbor-coupled ring**: ANDRING3 ✅ (M7 신규).
- **substrate↔causal bridge byte-equal**: eca_tpm == 손유도 TPM ✅ (M7 신규).
- 검증된 성질: 단조성 · big-Φ∈[0,total] 경계 · integrated↔reducible 분리 ·
  분수 closed-form · 쌍대 대칭 · 결정론(재실행 byte-identical).

**여전히 PyPhi-deferred** — F-IIT4-3/4:

- probabilistic(non-0/1 transition) 네트워크의 **절대-스케일** distinction-set /
  relation φ 의 PyPhi-numeric 일치. analytic 손유도는 0/1-collapse(또는 분수라도
  유한 비트의 closed-form) 영역까지만 honest 하게 닫힌다.
- **named blocker (미변)**: (1) hexa-only authoring 이 신규 `.py` 금지, (2) repo 의
  PyPhi 산출물은 전부 IIT-3.0 → IIT-4.0 + structure-cut big-Φ 와 apples-to-apples
  아님. → **fake 가 아닌 정직한 미해소**. M7 에서 어떤 published 수치도 입수/인용
  하지 않았다 (fabricate 0).
- gap 변화: **닫힌 analytic 좌표를 5 → 7+ networks 로 넓히고 5개 새 좌표축(분수-φ ·
  쌍대 · output-blind · ring · ECA bridge)을 추가로 닫음**. 단, PyPhi-numeric 의
  절대-스케일 검증 자체는 blocker 가 그대로라 verdict 는 🟠 유지 — "닫힌 면적" 만
  넓어졌을 뿐 deferred falsifier 가 해소된 것은 아니다.

## 5. 해소 경로 (F-IIT4-3/4, 미변)

- (a) published IIT-4.0 worked-example 수치를 문헌에서 입수해 in-repo reference 로
  등록 후 대조, 또는
- (b) hexa-lang 에 PyPhi-equivalent IIT-4.0 reference 를 포트(별도 lane).
