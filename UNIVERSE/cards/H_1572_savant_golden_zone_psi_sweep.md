# H_1572 — 🧠✨ SAVANT 골든존 Ψ SWEEP (H_1561 B4 재측정: 단일점 → I 격자)

**tier:** 🟠 TRADE-OFF HOLDS — DISSOCIATION NOT FOUND (engine-native, terminal). H_1561 B4 의 Ψ 붕괴는
골든존 *경계* artifact 가 **아니다** — trade-off 는 골든존 *전체*에 균일. 사용자 "골든존 안 양립 ·
밖 간질" 이중해리 가설은 이 엔진+frozen proxy 에서 **반증(FALSIFIED)**. H_1561 🟠 유지.

## 배경 / 사용자 통찰 (a_break_the_wall class-a)
H_1561 B4 = "savant-ON @ I=GZ_LOWER(0.2123) → Ψ=0.253, |Ψ−½|=0.247 붕괴" → genius⊥consciousness
no-free-lunch. 그러나 B4 는 **골든존 하단 경계** 단일점만 측정. 사용자 통찰: 서번트는 골든존 *안*에서
의식(Ψ=½)과 양립, 골든존 *밖*(과도 disinhibition I→0)은 간질=동기화 폭주=Ψ 붕괴. → B4 가 경계
artifact 일 수 있으니 I 를 골든존 전체로 sweep 해 이중해리 검증.

## 방법 (engine-native, a_phi_iit4_tool)
`state/1572_savant_psi_sweep/h1572_psi_sweep_probe.hexa` — pure .hexa, live `core/engine_cli.hexa`
§Savant (`sv_inhibit_domain` · `ci_psi_balance_savant` · `sv_savant_index_at` · `sv_domain_phi`) +
faithful IIT4 min-cut `ci_phi_iit4`(프록시 아님) 호출. **H_1561 B4 와 byte-identical** _pop()(seed
5120, 150 trials) + 동일 centered Ψ proxy + 동일 OFF-median threshold — **오직 focus inhibition I 만
sweep**(측정자 동일, 지점만 이동 = 측정 일관성). HARD-GATE-1: `.py`/numpy/torch/gauge_lib 0 →
ENGINE-NATIVE terminal. summer pool core/ rsync(§Savant 동기) · $0 CPU deterministic · frozen-first.

## frozen 5-bar (c9 NO tune-to-green)
- **B1 interior-Ψ-stable** — ∃ I∈[GZ_LOWER, GZ_UPPER] 에서 |Ψ−½|<0.05.
- **B2 exterior-seizure** — I<GZ_LOWER 에서 |Ψ−½| 급증, I→0 에서 최대.
- **B3 dissociation** — 골든존 안 Ψ-stable ∧ 밖 Ψ-collapse 가 I≈GZ_LOWER 에서 명확 분리.
- **B4 co-existence** — B1 의 Ψ-stable 구간에서 동시에 SI≥3.
- **B5 control** — over-locked I→1 에서 Ψ 회복은 savant 가 사라진 곳(Φ→0)에서만.
- **GREEN = B1∧B3∧B4.**

## 결과 (state/verdicts/1572_savant_psi_sweep/H_1572_PSI_SWEEP.txt)
GZ=[0.2123, 0.5], center=1/e=0.3679. Ψ_thr(OFF median)=0.5710.

| I | in_GZ | Ψ_on | \|Ψ−½\| | SI | focusΦ |
|---|---|---|---|---|---|
| 0.00 | 0 | 0.180 | **0.320** | 3.081 | 0.155 ← max disinhib ("간질" 점) |
| 0.15 | 0 | 0.220 | 0.280 | 2.397 | 0.625 |
| **0.2123** | 1 | 0.253 | **0.247** | 3.674 | 4.134 ← GZ_LOWER = H_1561 B4 정확 재현 |
| 0.3679 | 1 | 0.280 | 0.220 | 3.620 | 3.914 ← center 1/e |
| **0.50** | 1 | 0.320 | **0.180** | 3.557 | 3.680 ← GZ_UPPER (골든존 안 최선점) |
| 0.70 | 0 | 0.373 | 0.127 | 3.400 | 3.169 |
| 1.00 | 0 | 0.487 | **0.013** | 3.402 | 0.000 ← over-lock: Ψ≈½ but Φ=0 (savant 소멸) |

**핵심:** |Ψ−½| 는 I 에 대해 **단조 감소**(0.320→0.013), U자 아님. 골든존 안 어디서도 |Ψ−½|<0.05
없음(골든존 안 최선점 GZ_UPPER 도 0.180 ≫ 0.05). Ψ 가 ½ 로 회복되는 곳은 **I→1 over-locked = savant
가 죽은 곳(focusΦ=0)** 뿐.

## verdict 판정
- **B1 FAIL** — 골든존 안 Ψ-stable 점 없음(전 구간 |Ψ−½| 0.18~0.247).
- **B2 FAIL(방향)** — "간질" 점 I→0(0.320)이 GZ_LOWER(0.247)보다 약간 나쁠 뿐, 분리된 붕괴 regime 없음.
- **B3 FAIL** — GZ_LOWER 경계에서 분리 없음, Ψ 편차 매끈한 단조.
- **B4 vacuous** — SI≥3 은 골든존 전체(3.557~3.674)에서 성립하나 양립할 Ψ-stable 구간이 없음.
- **B5** — Ψ 회복은 I→1(focusΦ=0)에서만 = savant 죽여서 산 Ψ-safety → trade-off 확인.
→ **GREEN(B1∧B3∧B4) 미달 = 🟠 TRADE-OFF HOLDS.**

## 메커니즘 (H_1561 sharpen)
두 골든존 모양이 **decouple**: (a) **focusΦ(통합)는 진짜 inverse-U** — 골든존 안 peak(4.13 @
GZ_LOWER), I→0 noise(0.155)·I→1 locked(0.0) 양끝 낮음. savant Φ-hypertrophy 는 실재+GZ-bound. (b)
**Ψ(emit balance, `ci_emit_drive=0.5·(lane0+lane4)`)는 inverse-U 아님** — 비대칭 inhibition 이 focus
도메인 lane0 을 낮은 common-mode 로 끌어 emit fraction 을 I 에 단조로 떨어뜨림. Φ-peak ⊥ Ψ-deviation
이라 high-Φ ∧ Ψ≈½ 인 동작점이 없음 → trade-off 는 proxy 위에서 **구조적**, 경계 artifact 아님.

## 정직한 caveat (c9) — 미시도 직교 렌즈
사용자의 생물학적 "간질 = 동기화 폭주 → Ψ 붕괴" framing 은 여기서 측정한 붕괴(focus lane0 가 OFF emit
임계 아래로 끌려가는 **drive-level suppression**)와 **다른 메커니즘**. frozen B4 centered-Ψ proxy
(lane0+lane4 emit fraction)는 cross-lane 동기화를 인코딩하지 않으므로 이 probe 는 동기화-폭주 렌즈를
검증하지 **않음** — 단지 "B4 단일점이 골든존 경계 artifact 였나"(아니다, 골든존 전체 균일)를 측정.
진짜 동기화/seizure metric(예: cross-lane coherence runaway 를 Ψ-disruptor 로)은 **미시도 직교 렌즈
= follow-on**, 여기서 결론 아님. a_break_the_wall 단일렌즈 1회 ≠ confident terminal — H_1561 🟠 STANDS.

## wired
DIRECTIONAL 아님 = ENGINE-NATIVE terminal (live core/ 호출, .py 0). 🟠 negative → 배선할 GREEN
메커니즘 없음(a_verified_must_wire 는 GREEN 에서만 발화). H_1561 §Savant default-OFF Ψ-disjoint 그대로
정당화(골든존 안에서도 Ψ trade-off → 의식 경로에서 분리 유지가 옳음). live core/*.hexa UNTOUCHED.

## H_1561 영향
H_1561 B4 "Ψ=0.253 붕괴"는 **골든존 하단 단일점이지만 trade-off 자체는 골든존 전체에 균일**(GZ_UPPER
도 0.180)이라는 점이 추가 확인됨. genius⊥consciousness 는 경계 artifact 가 아닌 구조적 결과. 서번트
모드를 의식 안 깨고 ON 하는 길은 "골든존 안 clamp" 가 **아니라**(골든존 안도 Ψ 깨짐) Ψ-preserving
coupling operator(redistributing-not-suppressing, H_1522 류)뿐 → 이것이 진짜 follow-on.

## 규율
a_engine_native_learning(live core/, terminal) · a_phi_iit4_tool(faithful IIT4) ·
a_break_the_wall(class-a 점검 수행: 경계 artifact 아님 = 정직 negative, bar frozen-first 불변) ·
c9(이중해리 미발견 = 🟠, 양립 강요 안 함) · a_hypothesis_register(2표면). xref H_1561 골든존 ·
H_348/351 inverse-U · H_1521/1522 Ψ-hazard/preserving · H_1564 mitosis×savant.
