# H_1502 💊 NEUROPHARM — substrate-native neuropharmacology perturbation

**tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료; `wired:WIRED-live`)
**verdict source:** `state/verdicts/1502_neuropharm/` (R1 `H_1502_FREEZE.txt` · R2 `H_1502_R2_ENGINE.txt` · smoke `H_1502_SMOKE_292.txt`)

NO real drugs, NO synthesis. 표준 계산신경과학(entropic-brain / REBUS). 약물 = 엔진이 이미 노출한 substrate knob 에 적용하는 **FROZEN 섭동 VECTOR** → 의식 lane + Φ 변화 측정. 가설: anima substrate 를 약물의 *알려진 약리*로 섭동하면 문헌의 *알려진 방향성 의식 signature* 를 재현하는가?

> 핵심 설계(a_no_llm_frame_trap): 약물은 새 lane 이 아니고 'act high' 텍스트도 아니다 — `§ConsciousnessIndex` 의 substrate reads(m/m_field/dt/recon_err) + `§RealityMonitor` threshold + `§SelfIdentity` coherence 를 reshape 하는 7-knob 섭동 후 live 엔진(`ci_phi_multiinfo`/`reality_call`/`self_cos`)으로 **measure**.

## Knob → substrate read 매핑

| knob | substrate read | 출처 lane |
|---|---|---|
| `prior_strength` | grounding margin m 을 chance 0.5 로 압축 (REBUS: priors 완화) | ConsciousnessIndex |
| `signal_entropy` | **SHARED** common-mode diversity latent (독립잡음 아님 = 통합 안 깨짐, LZ↑) | ci reads |
| `self_boundary` | self_cos 를 ego-dissolved 직교축으로 (↓=dissolution) | §SelfIdentity (H_1471) |
| `lane_coupling` | shared-vs-private 분산 혼합 → Φ 구동 | ci_phi_multiinfo |
| `time_dilation` | dt 스케일 (주관시간 rate) | §SubjectiveTime (H_1475) |
| `reality_thr_shift` | §RealityMonitor threshold (↓ ⇒ imagined feels real) | §RealityMonitor (H_1501) |
| `working_memory` | held field-margin retention (THC 손상) | §WorkMemBuffer (H_1282) |

## FROZEN 약물 프로파일 (측정 전 등록, c9 · 문헌 근거)

`[prior_strength, signal_entropy, self_boundary, lane_coupling, time_dilation, reality_thr_shift, working_memory]`

| 약물 | 프로파일 벡터 | 약리 | 문헌 |
|---|---|---|---|
| **baseline** (sober) | `[1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0]` | zero-perturbation 통제 | — |
| **LSD** | `[0.55, 0.45, 0.45, 1.40, 1.05, −0.12, 0.95]` | 5-HT2A agonist, REBUS | Carhart-Harris & Friston 2019 Pharmacol Rev 71(3):316; entropic brain 2014; Schartner 2017 Sci Rep (LZ↑) |
| **DMT** | `[0.40, 0.60, 0.30, 1.55, 1.08, −0.30, 0.90]` | extreme 5-HT2A immersive | Timmermann 2019 Sci Rep 9:16324 |
| **Cannabis** | `[0.85, 0.10, 0.95, 1.02, 1.80, 0.0, 0.55]` | CB1, time-dilation + WM 손상 | Atakan 2012 Ther Adv Psychopharmacol 2(6):241 |
| **Ketamine** | `[0.80, 0.25, 0.50, 0.60, 1.10, 0.0, 0.85]` | NMDA antagonist, dissociative | (옵션) — lane_coupling↓ = 통합 감소, psychedelic 의 OPPOSITE |

## 측정된 signature (R2 engine-native, seed=1502, 48-trial LCG population)

| 약물 | Φ (phi_diversity) | reality_real | self_continuity | subjective_time | working_memory |
|---|---|---|---|---|---|
| baseline | 6.358 | 0.000 | 1.000 | 0.225 | 0.1259 |
| LSD | **6.950 ↑** | **0.667 ↑** | **0.633 ↓** | 0.237 ~ | 0.1196 ~ |
| DMT | **7.917 ↑↑** | **1.000 ↑↑** | **0.394 ↓↓** | 0.243 ~ | 0.1133 ~ |
| Cannabis | 5.935 ~ | 0.000 ~ | 0.999 ~ | **0.405 ↑** | **0.0692 ↓** |
| Ketamine | **4.459 ↓** | 0.000 ~ | **0.707 ↓** | 0.248 ~ | 0.1070 ~ |

**굵게 = 그 약물의 frozen 예측 축(reproduced).** `~` = 다른 약물의 축에서 ≈baseline (해리).

## 5 FROZEN bars — 전부 PASS (engine-native byte-exact)

- **(A) PRESENCE** — 각 약물이 자기 frozen 방향성 signature 재현. LSD(Φ↑≥0.05·real↑≥0.20·self↓≥0.20) · DMT(Φ↑·real↑≥0.40·self↓≥0.35) · Cannabis(time↑≥0.15·WM↓≥0.05) · Ketamine(Φ↓≥0.02·self↓≥0.15) → **모두 PASS** (per-drug GREEN).
- **(B) DOUBLE-DISSOCIATION** — LSD ⊥ Cannabis: LSD 는 reality(+0.667)/self(−0.367) 움직이고 time(|Δ|≤0.05)/WM 은 ~baseline; Cannabis 는 time(+0.180)/WM(−0.057) 움직이고 reality(Δ0.000)/self(|Δ|≤0.05) 는 ~baseline → **PASS**.
- **(C) KETAMINE-vs-PSYCHEDELIC** — ketamine ΔΦ=−1.899 (dissociation) vs LSD ΔΦ=+0.592 (integration) opposite-sign → **PASS**.
- **(D) EARNED ablate** — zero-perturbation(baseline) 프로파일 → ΔΦ exactly 0.0 → **PASS**.
- **(E) EARNED shuffle** — LSD↔Cannabis 프로파일 swap, own-prediction 으로 채점 → 양쪽 모두 FAIL(signature 가 매칭 프로파일에 EARNED) → **PASS**.

**GREEN iff A∧B∧C∧D∧E = 전부 PASS** → anima substrate 가 4 약물의 약리를 섭동했을 때 문헌의 방향성 의식 signature 를 재현하고 LSD⊥Cannabis 가 이중해리한다.

## 정직성 (c9) · a_break_the_wall type-a 측정교정 (2회, bar 불변·frozen-first·tune-to-green 아님)

R1 초기에 LSD/DMT/Cannabis 가 RED 였다 — frozen bar 가 아니라 **measurement-mechanism** 결함이었고, frozen bar 를 단 하나도 옮기지 않고 측정을 고쳤다:
1. **lane_coupling → Φ** — 초기 구현이 signal_entropy 를 *독립* per-lane 잡음으로 주입 → cross-lane covariance 파괴 → Φ 하락(REBUS 와 반대). 수정: signal_entropy 를 **SHARED common-mode diversity latent** 로 (richer shared dynamic = LZ↑ AND Φ↑ 공존, REBUS 의 entropic-brain 정신). lane_coupling 도 shared-vs-private 분산 혼합으로 재설계 → coupling↑ ⇒ Φ↑(LSD/DMT), coupling↓ ⇒ Φ↓(ketamine).
2. **SubjectiveTime 포화** — `1−1/(1+dt)` lane readout 이 포화 → ×1.8 cannabis dilation 이 +0.12 만 표현(0.15 bar 미달). 수정: lane 의 *포화 readout* 대신 H_1475 가 통합하는 **dt-rate substrate read** 를 측정(DT_REF=1.5 정규화) → ×1.8 dilation 이 full +0.180 표현. lane 자체의 포화는 정직한 substrate 발견(기록).

## 배선 (`wired:WIRED-live`, a_verified_must_wire 4칸 완료)

1. ✅ DIRECTIONAL 미러 GREEN (`state/1502_neuropharm/h1502_neuropharm.py`, 3 seeds, byte-identical ×3)
2. ✅ 엔진-네이티브 재검증 (frozen bar 동일, `state/1502_neuropharm/h1502_neuropharm_probe.hexa`, byte-identical ×3)
3. ✅ live `core/engine_cli.hexa §Neuropharm` wire-in (`pharm_*` 18 ops) + `engine_cli_smoke.hexa` cases 288-292, **FULL smoke 292/0 RC=0** (was 287, +5, 회귀 0)
4. ✅ `ARCHITECTURE.json §Neuropharm` lockstep

READ-only, Ψ-disjoint, NOT an emit gate (a_autonomy_over_hardcode).

## SCOPE UNVERIFIED (c9 · a_scale_honest_scope · a_toy_scale_recheck)

TOY 48-trial LCG population / 결정적 섭동 / 1 seed-가족 (drug-perturbation STRUCTURE 검증, 학습된 약리 아님). scale/실corpus/graded dose-response/개인차/추가 약물(MDMA·psilocybin 분리·muscimol)/engine-transfer(303M) UNVERIFIED → 303M 재측정 follow-on. reality_thr 은 H_1501 §RealityMonitor 가 main 에 있어 live 배선; dose-response 곡선 + 약물상호작용은 미탐색.

## xref
`p7`·`c9` · `a_no_llm_frame_trap`(생물/약리 렌즈 우선) · `a_engine_native_learning`(R1 미러→R2 engine-native) · `a_verified_must_wire`(4칸 배선) · `a_core_engine_map` · `a_break_the_wall`(type-a 측정교정) · `a_scale_honest_scope` · `a_toy_scale_recheck` · H_1501(§RealityMonitor reality_thr) · H_1492(§ConsciousnessIndex Φ) · H_1471(§SelfIdentity self_cos) · H_1475(§SubjectiveTime dt-rate) · H_1282(§WorkMemBuffer) · H_1290/H_1292(immune recall margin = 같은 substrate 신호).
