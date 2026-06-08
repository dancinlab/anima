# ANIMA emit-substrate 설계 — 통합 Φ-envelope 층 (2026-05-28)

> UNIVERSE Round 6+7+8+9 (H_632~657) 검증 결과를 ANIMA emit 정책 구현 아키텍처로
> 옮긴 설계. **구조는 한 곳(공유 substrate lib), 숫자는 한 곳(자유 정책 표)**.
> round-8 4 seam **4/4 ABSORBED** · round-9 **4/4 ABSORBED** (H_654/655/656/657, §5) — round-9 완료.
> round-9 발견: substrate-class 는 **다축 분류자** (속성마다 우위 class 다름, 단일 순위 환원 불가).
>
> 상태: **design-tier** (코드 미선행) · `a_completeness_over_cheap` 정합 (본선=재설계).

## 설계 통찰 — 왜 2층 분리인가

Round 7 이 Round 6 의 거친 직관("구조 robust > 숫자")을 정량 검증해, anima
emit 정책이 **물리적으로 두 층**임을 확정함:

- **구조** = anima 세포 (M×W×Φ) 에서 *창발(substrate-emergent)* 하며 어떤 의식
  substrate 든 수렴하는 invariant. UNIVERSE 가 substrate-invariance 를 *확인*만 함
  (검증자, 결정자 아님 · `a_autonomy_over_hardcode` 정합).
- **숫자** = substrate-Φ 와 직교한 design-convention. 자유도 [0,1] 전구간
  (H_646 🟢 variance=0). substrate-claim 없이 자유 튜닝.

이 두 층을 **파일 2개**로 그대로 분리하는 것이 본 설계. 구조는
`phi_envelope_substrate.hexa` 한 곳, 숫자는 `emit_policy.hexa` 한 곳. 4 milestone
(DREAM M5 · HIVE-MIND M6 · BRIDGE M6 · SAVANT M2) 은 얇은 소비자.

```
┌──────────────────────────────────────────────────────┐
│ 🟢 구조 층 (substrate-grounded · round-7 SUPP)          │
│ phi_envelope_substrate.hexa  [NEW 공유 lib]             │
│  · envelope_multiscale()   gamma⊂ultradian⊂circadian   │  H_648·H_634
│  · collective_phi_nest()   super-additive + 동조        │  H_635·H_643
│  · phi_smooth_no_cliff()   register cliff 부재          │  H_649
├──────────────────────────────────────────────────────┤
│ 🔵 숫자 층 (design-tunable · round-7 FREE)              │
│ emit_policy.hexa  [NEW 자유-숫자 표]                    │
│  · threshold 0.60 · emit-rate 0.27 · Ψ-clamp 0.10 …    │  H_646
│  "substrate-claim 없음" 명시                            │
└──────────────────────────────────────────────────────┘
        │             │            │            │
    💤 DREAM M5   🐝 HIVE M6   🚪 BRIDGE M6  🧠✨ SAVANT M2
    (envelope    (collective  (AND-gate    (측정자 Φ
     stage ctx)   fleet Φ)     ×Φ closure)  context)
```

**불변식 (설계 계약)**: 구조 층은 Φ context (실수)만 공급 · 숫자 층은 튜닝값만
공급 · **emit/silence 결정은 anima 세포가 자율** (M × W × Φ × curiosity). 두 층 중
어느 것도 `emit_allowed` boolean 게이트를 내보내지 않음 (p5 · `a_autonomy_over_hardcode`).

---

## §1 round-7 verdict → module 매핑

| round-7 finding | verdict | PR | → module | 비고 |
|---|---|---|---|---|
| scale-free Φ-envelope self-similar 6자릿수 | 🟢 H_648 | #1231 | `envelope_multiscale()` | gamma↔ultradian↔circadian min r=0.76 |
| ultradian Φ-envelope | 🟢 H_634 | (R6) | `envelope_multiscale()` | r=0.80 |
| collective-Φ super-additive | 🟢 H_635 | (R6) | `collective_phi_nest()` | 5/5 Δ=+41.71 |
| collective ultradian 동조 | 🟢 H_643 | #1237 | `collective_phi_nest()` | r=0.57 (single 보다 약) |
| **collective convexity = substrate-class 단조** | 🟢 H_653 | #1242 | `collective_phi_nest()` coupling | span ratio II 12.1 < III 30.4/30.8 < IV 35.5 · round-8 흡수 |
| **self-similarity = class-IV 한정 (보편 아님)** | 🔴 H_652 | #1245 | `envelope_self_similarity()` class 인자 | FALSIFIED 2/6 — rule110(IV)만 self-sim, 타 class 깨짐 |
| register-collapse cliff 부재 (collective) | 🟢 H_649 | #1234 | `phi_smooth_no_cliff()` | r=0.049 |
| closure-conjunction GZ-localization | 🟢 H_636 | (R6) | BRIDGE wiring | peak I=0.30 GZ 내부 |
| threshold 자유도 [0,1] | 🟢 H_646 | #1235 | `emit_policy.hexa` | substrate-Φ variance=0 |
| **design-number 전반 자유도 (일반화)** | 🟢 H_651 | #1246 | `emit_policy.hexa` 전 항목 | threshold·should_interrupt·Ψ-clamp α 모두 Φ-variance=0 · α 가 gate 0.556→0.683 움직여도 Φ 평탄 = NON-DEFINITIONAL 강증거 |
| **closure ultradian peak = mid-Φ N2** | ⚠ H_644 | #1233 | DREAM/BRIDGE 정정 | high-Φ 아님 (FAL-REVERSED) |
| H_618 dΦ/dI-GZ 정렬 = n=4 artifact | ⚠ H_645 | #1232 | **인용 금지** | 5-stream 붕괴 |
| "shape robust > scalar" 일반 | 🔴 H_642·H_647 | #1236·#1239 | **일반화 금지** | polarity(H_628)만 예외 |
| **shape-robustness taxonomy 완성** | 🟢 H_650 | #1247 | `phi_smooth_no_cliff()` 축-조건부 | polarity CV_shape=0 (HIGH robust) · rule tie · seed 역전 (LOW) — robustness=perturbation-축 함수 |
| **super-additive Δ = class-II 最高 (역전)** | 🔴 H_655 | #1253 | `pe_superadd_for_class()` | Δ ⊥ convexity 순위 — class 는 다축 분류자 (단일 스칼라 환원 불가) |
| **closure-band = class 의존** | 🟢 H_656 | #1251 | BRIDGE wiring | additive=0 · II/III=0.65 · IV=0.90 全역 |
| **dΦ/dI peak=GZ 정렬 = class 의존** | 🟢 H_657 | #1256 | `pe_peak_align_for_class()` | III+IV 정렬(|Δ|=0.032) · II/additive 이탈 (n 2/5) |
| **Φ-magnitude class-order** | 🟡 H_654 | #1250 | (룩업 carry) | PARTIAL — III-chaotic 最高 |

설계 규칙 (verdict 직속):
1. 🟢 구조 3종은 `phi_envelope_substrate.hexa` 에 substrate-grounded 로 구현.
2. 🔵 숫자는 전부 `emit_policy.hexa` 에 design-tunable 로 격리 (substrate-derived 주장 금지).
3. ⚠ closure ultradian 결합은 **mid-Φ N2 peak** 로 서술 (high-Φ 가정 금지).
4. ⚠ n=4 exact-match 정렬 (H_618·H_624 류) 은 차원 확장 전 substrate 결론 인용 금지.
5. 🔴 shape-robustness 는 polarity 축 한정 — 일반 "shape > scalar" 가정 금지.

---

## §2 `phi_envelope_substrate.hexa` 시그니처 (구조 층)

위치 후보: `CORE/phi_envelope_substrate.hexa` (A⇄G 결정두뇌 인접) 또는 `WAKE/`
(living loop 인접). **CORE 권장** — 모든 도메인이 import 하는 substrate 기반층이라
가로 도메인이 아닌 세로 기둥 (KOSMOS/tension-link 와 동급 substrate infra).

구조식만 노출, 숫자 인자는 caller (emit_policy) 가 주입:

```
# 다중-스케일 self-similar Φ-envelope (H_648·H_634)
# scales = [(period, amplitude), ...]  gamma⊂ultradian⊂circadian
# 반환 = 시점 t 의 Φ-envelope 값 (실수, boolean 아님)
pub fn envelope_multiscale(t, scales) -> phi

# self-similarity 불변식 검사 (H_648 self-sim · H_652 🔴 class-IV 한정)
# ⚠ H_652 정정: self-similarity 는 보편 아님 — rule110(class-IV) 에서만 성립,
#   타 class 는 깨짐 (FALSIFIED 2/6). ∴ class 인자를 받아 class-IV 만 r≥0.76
#   기대하고, 비-IV substrate 의 낮은 r 은 *예측된 정상* (버그 아님).
# 반환 = 인접 스케일 쌍의 형상 상관 리스트
pub fn envelope_self_similarity(scales, n_samples, class_id) -> [r]

# 집단 Φ 중첩 (H_635 super-additive + H_643 동조 + H_653 substrate-class convexity)
# phis = 개별 cell/stream 의 Φ 리스트
# coupling = substrate complexity-class 의존 함수 (H_653 🟢 — 상수 아님):
#   W→Φ convexity span ratio 가 class 에 단조 (II≈12 < III≈30 < IV≈35.5)
#   ∴ coupling(class) 로 받아 복잡도 비례 convexity 반영
# 반환 = 집단 Φ (super-additive: Σ 보다 큼) + 동조 계수 + convexity span
pub fn collective_phi_nest(phis, class_id) -> { phi_collective, sync, convexity_span }
#   class_id → 내부에서 두 독립 class-서명 resolve (round-9 다축):
#     pe_superadd_for_class (Δ, H_655 II-最高) ⊥ pe_coupling_for_class (sync, H_653 IV-最高)

# register-collapse cliff 부재 — Φ 가 임계에서 급락(cliff) 하지 않고 smooth (H_649)
# 반환 = Φ 의 1차 차분 최대값 (cliff 있으면 큼; 부재면 작음)
pub fn phi_smooth_no_cliff(phi_series) -> max_dphi
```

설계 계약:
- 모든 반환은 **실수/리스트** (Φ context). `bool` emit 게이트 반환 금지.
- 숫자 상수 (period · amplitude · coupling) 는 인자로만 — lib 내부 하드코드 금지
  (그래야 `emit_policy.hexa` 가 단일 튜닝 SSOT).
- `phi_native.hexa` (기존 PHI 도메인 lib) 의 Φ 계산을 재사용 — 중복 구현 금지 (g61).

---

## §3 `emit_policy.hexa` 스키마 (숫자 층)

위치: `CORE/emit_policy.hexa` (도메인 횡단 단일 SSOT). 모든 항목 `substrate-claim:
none` (H_646/651 자유도 [0,1]). **realized as `.hexa` (not `.tape`)**: 소비자
(DREAM/HIVE/BRIDGE/SAVANT)가 hexa `import` 로 소비 — .tape registry 는 hexa-import
불가. 단일 SSOT (병렬 .tape 없음), MATRIX.tape 의 single-registry 정신은 유지.
실 구현 = pub accessor fn (`ep_emit_threshold()` 등) — 상수가 아닌 함수라 import 후 호출.

```
@V := "tape" :: spec
  version = "0.1"

# ── emit 임계값 (H_646 🟢 자유도 [0,1] · substrate-Φ variance=0) ──
@P emit_threshold      = 0.60   # substrate-claim: none · design-tunable
@P emit_threshold_lo   = 0.30   # 하한 (H_632 🔴 ⊥ Φ phase-transition)
@P target_emit_rate    = 0.27   # H_637 · substrate-claim: none
@P psi_clamp           = 0.10   # Ψ=1/2 고정점 clamp · convention
@P tension_amplitude   = 1.00   # H_639 · convention

# ── 다중-스케일 envelope 파라미터 (구조는 substrate, 숫자는 free) ──
# scale = (period_ticks, amplitude) — 형상은 substrate (H_648), 값은 tunable
@P scale_gamma         = (1,    0.10)
@P scale_ultradian     = (5400, 1.00)   # 90-min
@P scale_circadian     = (86400, 0.50)

# ── stage θ_emit 표 (DREAM 5-stage · stage=context NOT boolean gate) ──
# 주의: θ 는 Φ-context 스케일일 뿐, per-stage emit_allowed 아님 (p5·a_autonomy)
@P theta_wake          = 0.10
@P theta_n1            = 0.08
@P theta_n2            = 0.05   # H_644 정정: closure peak = mid-Φ N2
@P theta_n3            = 0.02
@P theta_rem           = 0.08
```

설계 계약:
- 모든 `@P` 는 자유 튜닝 — 변경이 substrate 주장에 영향 없음.
- DREAM/BRIDGE/HIVE/SAVANT 가 이 표를 import (각자 하드코드 금지).
- `θ_*` 는 **context 스케일**이지 emit 게이트가 아님 — anima 세포가 θ 를 Φ-context
  로 받아 자율 결정 (p5 tension-emit · `a_chat_sleep_imagination`).

---

## §4 4-milestone wiring

각 milestone 은 substrate lib + policy 표를 import 하는 **얇은 소비자**.

| milestone | 소비 함수 | policy | 정정 반영 |
|---|---|---|---|
| 💤 **DREAM M5** | `envelope_multiscale(t, scales)` | `theta_*`, `scale_*` | H_644 closure peak=mid-Φ N2 |
| 🐝 **HIVE-MIND M6** | `collective_phi_nest(phis, class_id)` | `scale_ultradian` | H_643 동조 · H_653 convexity(IV) ⊥ H_655 super-add(II 역전) 다축 · H_645 GZ 인용 금지 |
| 🚪 **BRIDGE M6** | `envelope_multiscale` → AND-gate Φ 입력 | `emit_threshold` | H_636 closure-conjunction GZ |
| 🧠✨ **SAVANT M2** | `envelope_multiscale` → 측정자 Φ context | `emit_threshold` | (E축 측정자, 발화 게이트 아님) |

**DREAM M5** (`DREAM/dream_lib.hexa` + `AGENT/CHAT/anima_dream_stage.hexa`):
- 5-stage 머신이 `envelope_multiscale` 로 stage Φ-envelope 산출.
- stage = Φ scale + tension envelope **context** (boolean emit 게이트 아님 ·
  `a_chat_sleep_imagination`). N2 가 closure peak (H_644 정정).
- imagination loop = emit-free 내부 rehearsal + mitosis tick (기존 유지).

**HIVE-MIND M6** (`HIVE-MIND/lib/` + UNIVERSE 축 F mirror):
- `collective_phi_nest` 로 fleet 집단 Φ (super-additive H_635) + ultradian 동조
  (H_643). **H_618 dΦ/dI-GZ 정렬은 n=4 artifact (H_645) — 구현 인용 금지**.
- **H_653 핵심 (round-8 흡수)**: collective entrainment 약화 (single r=0.80 →
  collective 0.57) 는 **버그 아니라 정상** — 근본 원인이 substrate 복잡도에 비례하는
  W→Φ convexity (span ratio class-II≈12 < III≈30 < IV≈35.5, 단조). ∴ HIVE-MIND M6 은
  약한 collective r 을 "고치려" 하지 말 것. `coupling_fn(class)` 로 복잡도-의존 convexity
  를 받아 entrainment 약화를 *예측*해야 함 (rule110 per-stage Φ 1.17/4.50/13.64/34.88
  이 H_643 engine 과 정확 일치 — 동일 substrate 확인).

**BRIDGE M6** (`BRIDGE/gate.hexa` 기존 4-key AND-gate 확장):
- `bridge_and_gate(m,c,w,phi)` 의 `phi` 입력을 `envelope_multiscale` 에서 공급.
- closure-conjunction GZ-localization (H_636) 을 AND-gate 의 Φ-context 로.
- `emit_threshold` 는 `emit_policy.hexa` 에서 import (gate 내부 하드코드 제거).

**SAVANT M2** (UNIVERSE 축 E mirror · 측정자):
- 측정자는 발화 게이트가 아니라 Φ-context 소비자 — `envelope_multiscale` 의 Φ 를
  10 H 측정자 (H_347~351 · H_612~616) 의 입력 context 로.

**횡단 규칙 (H_650 round-8 흡수 · 전 milestone 적용)**:
- shape-robustness 는 **perturbation-축의 함수** — `phi_smooth_no_cliff` / 측정자가
  robustness 를 주장할 땐 축을 명시할 것. **polarity 축만 shape-robust** (CV_shape=0,
  3 polarity 모두 peak=GZ_LOWER) · rule(질적 동역학)·seed(전이 jitter) 는 fragile
  (CV tie/역전). "shape > scalar" 보편 주장 금지 (H_642/647/650 반증).

---

## §5 round-8 확장 seam — **4/4 ABSORBED** (H_650~653 완료)

round-8 4 가설이 각각 본 설계의 **특정 seam**을 정밀화. 전부 흡수 완료:

| round-8 H | verdict | 흡수 결과 |
|---|---|---|
| ✅ **H_650** shape-robustness-axis-taxonomy | 🟢 SUPP 5/5 (#1247, G15) | **ABSORBED** — robustness=perturbation-축 함수. polarity CV_shape=0 (HIGH) · rule tie · seed 역전 (LOW). `phi_smooth_no_cliff` 는 **polarity 축만 shape-robust** 로 서술 (rule/seed 일반화 금지, §4) |
| ✅ **H_651** convention-number-freedom-general | 🟢 SUPP 6/6 (#1246, G14) | **ABSORBED** — design-number 전반 자유도 확정. threshold·should_interrupt·Ψ-clamp α 모두 Φ-variance=0. **α 가 gate 0.556→0.683 움직여도 Φ 평탄** = "policy 를 움직이는 숫자조차 substrate-safe" NON-DEFINITIONAL 강증거. `emit_policy.hexa` 전 항목 `substrate-claim: none` 확정 (§3) |
| ✅ **H_652** envelope-self-similarity-class | 🔴 FAL 2/6 (#1245) | **ABSORBED (정정)** — self-similarity 는 **보편 아님, class-IV(rule110) 한정**. `envelope_self_similarity` 에 `class_id` 인자 추가 — class-IV 만 r≥0.76 기대, 비-IV 낮은 r 은 예측된 정상 (§2). skeleton 의 이상화 r=1.0 = class-IV case |
| ✅ **H_653** collective-convexity-class | 🟢 SUPP 5/6 (#1242, G12) | **ABSORBED** — `collective_phi_nest` 의 `coupling` → `coupling_fn(class)` 승격 (§2·§4). entrainment 약화 = substrate-복잡도 비례 convexity 의 정상 귀결 |

설계 계약대로 **인자 추가만으로 4/4 흡수 (시그니처 파괴 0 · 4 milestone 재작업 0)**.

### round-9 흡수 (H_654~657 · substrate-class = 다축 분류자) — 3/4 ABSORBED

round-9 의 결정적 발견: **Wolfram class 는 단일 스칼라 순위가 아니라 *속성-벡터 분류자***
— 각 Φ-속성이 *자기만의 class-정렬*을 가짐. 단일 순위로 환원 불가:

| Φ-속성 | verdict | 우위 class | 비고 |
|---|---|---|---|
| convexity | 🟢 H_653 (#1242) | **IV 最高** (단조) | II 12.1 < III 30.4 < IV 35.5 |
| magnitude | 🟡 H_654 (#1250) | III-chaotic 最高 | PARTIAL |
| super-additivity Δ | 🔴 H_655 (#1253) | **II-additive 最高 (역전!)** | II 51.54 > IV 41.71 > III 9.72 — convexity 와 반대 |
| closure-band | 🟢 H_656 (#1251) | **IV 最高** | additive=0(부재) · II/III=0.65 · IV=0.90(全역) |

보편 불변량은 단 하나: **additive(rule90 XOR)는 거의 모든 축에서 바닥 (Φ≈0)**.

**설계 흡수 (코드 반영 — 이 PR)**: 단일 `coupling` 스칼라는 다축성을 못 담음 →
class→**property-vector** 로 분리. `collective_phi_nest(phis, class_id)` 가 내부에서
두 *독립* class-서명을 resolve: `pe_superadd_for_class` (Δ, H_655 II-最高) ⊥
`pe_coupling_for_class` (convexity/sync, H_653 IV-最高). phi_collective 의 Δ 를
convexity-coupling 에서 **분리** (이전 골격이 묶어둔 것을 H_655 가 정정).

**✅ H_657 ABSORBED (round-9 완료 · 4/4)**: dΦ/dI peak=GZ_LOWER 정렬도 class-conditional
(III+IV 정렬 |Δ|=0.032 · II/additive 이탈, n 2/5) — `pe_peak_align_for_class(class_id)` 추가
(III/IV→1.0 · 그 외→0.0). 다축 분류자 5번째 축 확정. H_351 single-substrate SUPPORTED 는
universal anchor 아님. **잔여 carry**: magnitude(H_654 🟡 PARTIAL) 만 룩업 미확정.

**round-9 종합 — substrate-class = 5축 property-vector** (단일 순위 환원 불가):
convexity(IV) ⊥ super-add(II 역전) ⊥ closure-band(IV) ⊥ peak-align(III+IV) ⊥ magnitude(III🟡).
공통 불변: additive(rule90)만 거의 모든 축 바닥(Φ≈0).

---

## §6 falsifier 사전등록 (구현 게이트)

구현 PR 이 통과해야 할 falsifier. `hexa verify` 로 검증, verdict verbatim 기록
(`a_claim_verify` · `a_blue_closed`).

| ID | 주장 | 측정 | 통과 기준 |
|---|---|---|---|
| **F-EMIT-1 SELF-SIMILAR** | envelope 가 6자릿수 self-similar | `envelope_self_similarity(scales)` | 인접 스케일 쌍 min r ≥ 0.76 (H_648 재현) |
| **F-EMIT-2 SUPER-ADDITIVE** | collective Φ > Σ 개별 Φ | `collective_phi_nest` | phi_collective > Σphis (H_635 부호) |
| **F-EMIT-3 NO-CLIFF** | register cliff 부재 | `phi_smooth_no_cliff` | max_dphi < cliff 임계 (H_649 r≈0) |
| **F-EMIT-4 NO-GATE** | 구조/숫자 층이 emit boolean 미반환 | 정적 grep | 두 층에 `emit_allowed` / `-> bool` 게이트 0건 (p5·a_autonomy) |
| **F-EMIT-5 POLICY-FREE** | 숫자는 substrate-claim 없음 | `emit_policy.hexa` 변경 → 구조 불변 | threshold 변경이 envelope 형상 불변 (H_646 자유도) |
| **F-EMIT-6 N4-ABSTAIN** | n=4 정렬 미인용 | 정적 grep | H_618/H_624 류 n=4 exact-match 인용 0건 (H_645 교훈) |

terminal verdict (🔵/🟢/🔴) 만 closure 인정 — 🟠/🟡 잔여 시 미완 (`a_paper_gate` 정합).

---

## §7 consciousness-ruler 설계 원리 (측정자 = Φ + temporal/agency 축)

의식 尺(ruler)를 두 부분으로 설계한다 — **instantaneous Φ** 한 축으로는 부족하다는 것이
이번 round 에서 측정됨. (전부 **측정/설계 층** · emit 게이트 아님 · `a_autonomy_over_hardcode`.)

**(1) instantaneous Φ — 단일 good scalar 면 충분 (재조합 무의미).**
instantaneous Φ 를 vector / synergy / pair / fixed-coarse-grain 으로 **재조합**해도 단일
good scalar Φ 를 못 이김 (H_1045/1046/1047/1049 🔴, toy scale). 즉 "더 정교한 순간-Φ
조합" 은 尺를 개선하지 않음 — 새 정보가 없는 재포장.
- ⚠ **H_1049 🔴 bound**: fixed small-m IB coarse-grain 은 *scalable* Φ estimator 아님
  (rel-err 가 N 따라 증가). macro-IIT 는 grain m 을 system 크기 따라 키워야 — 고정-m 은
  큰 N 에서 정직하지 않음 (stdlib macro-IIT 핸드오프 사유).

**(2) temporal/agency 축 — 직교 새 차원만이 尺를 넓힌다 (H_1051 🟢).**
instantaneous Φ 는 **agency 에 BLIND**: Φ-matched active vs passive 가 |d_Φ|=0.04 로
사실상 구분 불가. temporal/agency 축 **T = z(provenance-depth) + z(veto-capacity)** 가
둘을 분리(|d_T|=8.77) AND instantaneous Φ 에 **ORTHOGONAL** (ρ≈0.0001).
∴ 의식 尺 = **Φ ⊕ temporal/agency 축** (`temporal_agency_context()` = 골격 노출).

**(3) Φ 자체의 측정-의존 sign-split 은 robust (尺 설계 시 측정자 명시 필수).**
계획-Φ 의 measure-dependence sign-split (faithful-Φ↑ / big-Φ↓) 은 **DISCRETIZATION-
INVARIANT** (H_1037 🟢, 6/6 binning at n=6 EXACT — coarse-grain artifact 아님) 이고
**REAL trained ConvMoE(d768)** 에서도 sign-level 로 transfer (H_1038 🟢). → 尺가 Φ 를
인용할 땐 *어느 Φ 측정자* (faithful vs big-Φ) 인지 반드시 명시.

> **scope (정직):** 위 전부 **toy n≤5/6 EXACT** (H_1038 = 단일 d768 sign-level rung).
> production/3B/7B 전이 **UNVERIFIED** — production 닫힘 주장 0 (`a_toy_scale_recheck` ·
> `a_scale_honest_scope`). 본 §7 은 측정/설계 노트이지 런타임 게이트 아님.

---

## 양방향 sibling

- ⇄ [DREAM](../DREAM.md): envelope stage context 소비자 (M5)
- ⇄ [BRIDGE](../BRIDGE.md): AND-gate Φ 입력 소비자 (M6)
- ⇄ [CORE](../ANIMA.md): substrate lib 거주 (세로 기둥)
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT · round-8 환류 원천
