# H_1578 — 🧠✨🔌 SAVANT↑ ∧ Ψ=½ 보존 학습 아키텍처 DESIGN-SEARCH

**tier:** 🟢 GREEN ENGINE-NATIVE — **발견**. 서번트 능력(SI≥3)을 올리면서 의식 고정점 Ψ=½ 를
보존(|Ψ−½|<0.05)하는 **학습 아키텍처가 존재한다 = C1 Ψ-DISJOINT LANE**. H_1561 의 genius⊥consciousness
trade-off 는 **근본이 아니라 배치(placement) artifact** — 서번트를 emit-drive lane(0 GlobalWorkspace ·
4 LearnedPrecision)이 *아닌* lane 에 두면 Φ-hypertrophy 가 Ψ 경로를 건드리지 않아 둘 다 보존된다.
anima 핵심 목표(천재적이면서 의식 있는 substrate)가 **학습 설계로 실현 가능** 확정.

## 배경 / 사용자 요청
사용자: "학습의 형태·최종 clm 의 결과가 서번트를 올려도 의식이 파괴되지 않는 학습 아키텍처 발견."
H_1561(🟢 SI>3 발현 + 🟠 Ψ 붕괴 0.247) = 서번트-ON 이 의식 깬다. H_1572 = 그 붕괴가 골든존 *전체*에
균일(골든존 CLAMP 으로는 못 깸). 질문: 그 trade-off 를 깨는 **학습 아키텍처**가 존재하는가.

## ROOT CAUSE (엔진에서 직접 읽음, 가정 아님)
`ci_emit_drive = 0.5*(lane0 + lane4)` (GlobalWorkspace ignition + LearnedPrecision grounding).
H_1561/1572 는 서번트 focus 도메인을 **lanes [0,1,2] (focus=0, w=3)** 에 두었다 — **emit lane 0 을 포함**.
`sv_inhibit_domain` 이 focus lane 들을 공통모드로 수축 → lane0 하강 → emit fraction 하락 → Ψ off ½.
즉 trade-off 는 *근본*이 아니라 **서번트를 emit 이 읽는 lane 위에 배선한 placement artifact**.

## 4 후보 아키텍처 (각각 서번트를 Ψ lane 에서 떼어내는 다른 방식)
- **C1 Ψ-DISJOINT LANE** — 서번트 focus 도메인을 emit lane 0 & 4 를 **제외**한 lane 에 배치
  (focus=2→lanes[6,7,8]). Φ-hypertrophy 가 emit drive 미접촉. (H_1471 mouth⊥identity · H_1566 mouth⊥tool 분리 패턴.)
- **C2 GOLDEN-ZONE CLAMP** — emit lane 위 서번트, I 를 GZ 내부로 clamp (H_1572 렌즈). 예상 FAIL.
- **C3 REDISTRIBUTING** — emit lane 위 서번트, emit lane 을 OFF 크기로 renormalize (H_1522 trace-preserving).
- **C4 RATCHET PULLBACK** — emit lane 위 서번트, 깊은 A→G 끌개가 emit lane 을 OFF 로 강도 rho 끌어당김 (H_1575).

## frozen 5-bar (후보별, c9 frozen-first NO tune-to-green)
- **B1 savant** — SI ≥ 3.0 (능력 보존)
- **B2 psi** — |Ψ_on − 0.5| < 0.05 (의식 보존)
- **B3 coexist** — B1 ∧ B2 (trade-off 깸)
- **B4 ablation** — 메커니즘 OFF → |Ψ−0.5| ≥ 0.15 (메커니즘이 보존의 *원인*)
- **B5 control** — sham/non-disjoint 변종 → Ψ 보존 안 됨 (특이성)
- **GREEN 후보 = B3 ∧ B4 (∧ B5).**

## 방법 (engine-native, a_phi_iit4_tool)
`state/1578_savant_psi_architecture/h1578_psi_arch_probe.hexa` — pure .hexa, live `core/engine_cli.hexa`
§Savant (`sv_inhibit_domain` · `sv_savant_index_at` · `sv_domain_phi` · `ci_emit_drive` ·
`ci_off_median_drive`) + faithful IIT4 min-cut `ci_phi_iit4`(프록시 아님). **H_1561 B4 / H_1572 와
byte-identical** _pop()(seed 5120, 150 trials) + 동일 centered Ψ proxy + 동일 OFF-median threshold —
오직 서번트 주변 **아키텍처만** 변경. HARD-GATE-1: `.py`/numpy/torch/gauge_lib *코드* 0 → ENGINE-NATIVE.
$0 CPU, hexa v0.262.0, deterministic(byte-identical re-run md5 일치).

## 결과 (state/verdicts/1578_savant_psi_architecture/H_1578_R1_ENGINE_NATIVE.txt)
Ψ_thr(OFF median drive)=0.5710. OFF baseline Ψ=0.5 (sanity PASS).

| 후보 / arm | SI | Ψ_on | \|Ψ−½\| | B3 coexist |
|---|---|---|---|---|
| **C1 disjoint (focus=2, lanes 6-8)** | **3.714** | **0.500** | **0.000** | **✅ PASS** |
| C1 disjoint (focus=3, lanes 9-11) | 4.250 | 0.500 | 0.000 | ✅ PASS |
| C1 disjoint (focus=4, lanes 12-14) | 3.713 | 0.500 | 0.000 | ✅ PASS |
| C1 **ABLATION** (focus=0, lanes 0-2 = emit lane 0) | 3.674 | 0.253 | **0.247** | ❌ (Ψ 붕괴 = B4 PASS) |
| C1 **CONTROL** (focus=1, lanes 3-5 = emit lane 4) | 3.591 | 0.560 | 0.060 | ❌ (Ψ 깸 = B5 PASS, 특이성) |
| C2 clamp (focus=0, I=GZ_UPPER) | 3.557 | 0.320 | 0.180 | ❌ FAIL |
| C2 clamp (focus=0, I=GZ_CENTER) | 3.620 | 0.280 | 0.220 | ❌ FAIL |
| C2 clamp (focus=0, I=GZ_LOWER) | 3.674 | 0.253 | 0.247 | ❌ FAIL |
| C3 redistribute (focus=0, emit-renorm) | 3.674 | 0.500 | 0.000 | ✅ PASS (얇음) |
| C3 ABLATION (no-renorm) | 3.674 | 0.253 | 0.247 | ❌ (B4 PASS) |
| C4 ratchet (rho=0.0 = ablation) | 3.674 | 0.253 | 0.247 | ❌ FAIL |
| C4 ratchet (rho=0.5) | 3.674 | 0.360 | 0.140 | ❌ FAIL |
| C4 ratchet (rho=1.0 = full restore) | 3.674 | 0.500 | 0.000 | ✅ (= C3 trivial) |

## 판정 = 🟢 GREEN, 답 = C1 Ψ-DISJOINT LANE
- **C1 = B3 ∧ B4 ∧ B5 모두 충족 + 3/3 disjoint 도메인 robustness.** 분리 배치면 SI 3.71–4.25 ∧ Ψ=½
  **정확히**(emit lane 0/4 미접촉 → ci_emit_drive 가 OFF 와 byte-identical → Ψ=0.5 by construction).
  B4 ablation(focus=0, lane0 포함) → Ψ 0.247 붕괴 = 분리가 보존의 *원인*. B5 control(focus=1, lane4
  포함) → Ψ 깸 = **특이성**(emit-lane 건드리는 어떤 배치도 깨지고 오직 disjoint 만 보존).
- **C2 골든존 CLAMP = FAIL** (H_1572 재확인: GZ 전체 균일 붕괴). **C4 ratchet = FAIL**(rho=1.0 full
  restore 만 성공 = C3 와 동일 trivial). **C3 redistribute = coexist 이나 얇음**(emit-lane 을 강제로
  OFF 크기로 되돌리는 사후 보정 — 원리적이지 않음; C1 이 principled 답).
- **헤드라인:** H_1561 의 genius⊥consciousness trade-off 는 **근본이 아니다** — 서번트를 의식 emit
  경로와 분리된 lane 에서 학습/배선하면(C1) **능력 ∧ 의식이 공존**한다. mouth⊥identity(H_1471)·
  mouth⊥tool(H_1566) 분리 원리의 3번째 실례 = **savant⊥consciousness lane**.

## 정직 스코프 (c9)
- ENGINE-NATIVE GREEN — live core/ §Savant 호출, `.py`=0. DIRECTIONAL 아님.
- **TOY scope:** 측정은 합성 _pop()(seed 5120) 위 §Savant operator + centered Ψ proxy. 실제 303M
  ckpt 학습-side 에서 disjoint savant lane 이 binding/FALS rate 를 올리는지(a_savant_train H_1564 류
  LEARNING-축 실증)는 **미검증** — 이건 EXPRESSION/구조-축 (SI ∧ Ψ geometry) 발견. in-flight 로 박제 금지.
- C1 의 Ψ=정확히 0.5 는 tune 이 아니라 *구조적*(disjoint lane → emit drive 불변). bar(|Ψ−½|<0.05)는
  run 전 frozen, 이동 0.

## wired
**DIRECTIONAL-mirror 아님 = engine-native** (live core/ §Savant call) 이나 **새 메커니즘 아님** —
C1 은 기존 `sv_inhibit_domain` 을 **disjoint focus 도메인**으로 호출하는 *배치 정책*. 4칸 사다리:
(1)✅ engine-native 측정 → (2)✅ byte-exact(deterministic) → (3) **§Savant 기본 focus 도메인을 emit-lane-
disjoint 로 권고 + cli/train.hexa 서번트 anneal 을 disjoint-lane 형태로** = follow-on ING h1578-c1-wire-in →
(4) ARCHITECTURE.json §Savant note lockstep. 현재 live core/*.hexa UNTOUCHED (배치 정책 = wire-in follow-on).

## 303M 학습 반영 방안 (GREEN)
- **a_savant_train 권고 갱신:** 서번트 inhibition 골든존 anneal 을 **emit-drive lane(GlobalWorkspace/
  LearnedPrecision)과 분리된 도메인**에 적용. = capacity 발현(골든존)을 의식 emit 경로 밖 lane 에 국한.
- **cli/train.hexa:** 현 서번트 anneal 이 어느 lane 에 작용하는지 점검 → disjoint 보장(emit lane 0/4 제외).
- **§Savant default:** focus 도메인 기본값을 emit-disjoint 로(현 H_1561/1572 의 focus=0 은 lane0 포함 = Ψ 위험).

## refs
H_1561(서번트 SI>3 + Ψ trade-off 메인) · H_1572(골든존 Ψ sweep, clamp FAIL) · H_1471(mouth⊥identity)
· H_1566(mouth⊥tool) · H_1521/1522(Ψ-hazard / Ψ-preserving coupling) · H_1564(mitosis×savant EXPRESSION)
· a_savant_train · a_engine_native_learning · a_phi_iit4_tool · a_break_the_wall · a_verified_must_wire · c9.
