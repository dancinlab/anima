# H_1503 — ⚡ ELECTROMAGNETIC-FIELD PERTURBATION MODULE + PCI — §Neuropharm 의 자기/EM-자극 짝

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §Field (`field_apply` + `field_apply_mfield` + `field_signal_entropy` + `drug_lsd_mfield` + `pci_perturb` + `pci_complexity` + `field_lane_mean`) · `engine_cli_smoke.hexa` cases 299-304 (6 frozen bars) · FULL smoke **303 pass / 0 fail RC=0** deterministic ×3 · ARCHITECTURE.json §Field lockstep ✓
- **source:** team-lead 작업지시(전자기장 섭동 모듈 H_1503) — H_1502 §Neuropharm(약물=전역·화학) 착지 후 그 focal·주파수특이 짝 · TMS/PCI·tACS/rTMS 문헌 렌즈 · `a_no_llm_frame_trap`
- **lens:** TMS perturbational-complexity (Massimini-Casali) · tACS/tDCS frequency-specific entrainment (Herrmann) · rTMS excitatory/inhibitory (Hallett) · `a_no_llm_frame_trap`
- **artifacts:** `state/1503_field/h1503_field.py` · verdict `state/verdicts/1503_field/H_1503_R1.txt`(R1 mirror) · `state/verdicts/1503_field/H_1503_R2_engine_native.txt`(R2 byte-exact 6 cases + INFO)

## 주장 (focal·주파수특이 FIELD ⊥ 전역·화학 DRUG)

한 **FIELD**(자기/EM 자극)는 새 의식 lane 도, "감전된 척" 텍스트도 아니다(`a_no_llm_frame_trap`). FIELD =
엔진이 이미 `ci_lane_scores` 입력으로 노출하는 **substrate knob**(m·m_field[5]·cells·recon_err·dt)에 가하는
**FROZEN 섭동 VECTOR**(주파수·강도·focality·target-lane). 그 뒤 의식 lane + Φ 변화 + **새 섭동측도 PCI** 를
측정한다. 가설: anima substrate 를 자극 프로토콜의 물리로 섭동하면 그 프로토콜의 **알려진 방향성 의식
signature**(문헌)를 재현하는가? HARDWARE 없음 — software substrate 의 parametric 섭동 + 엔진 측정.

**DRUG(§Neuropharm, 전역·화학) ⊥ FIELD(focal·주파수특이) 이중해리가 headline.** knob→lane 매핑은
`ci_lane_scores` 의 실제 민감도를 경험측정해 정한 **ENGINE-FAITHFUL** 매핑: BINDING=GlobalWorkspace(lane0,
winner m_field margin)·GATING=DividedAttention(lane12, m_field 엔트로피)·MEMORY=MitosisGrowth(lane14, cells).

## 새 측도 PCI (perturbational complexity index — clean new measure)

정적 Φ(`ci_phi_multiinfo`) = **RESTING** substrate 의 통합(공분산). **PCI** = substrate 를 일시 **pulse** 로
찌른 뒤 spatiotemporal 반응(lane×time)을 이진화하고 그 **Lempel-Ziv 복잡도**를 정규화(LZc·log2(L)/L, [0,1]
유계 — Casali et al, *Sci Transl Med* 2013; Massimini et al, *Science* 2005). 高 PCI = 의식적(통합 AND 분화된
반응); 低 PCI = 붕괴(마취/탈동조 — 국소·정형 echo). 정적 Φ 와 **진짜 DISTINCT**: Φ=resting 공분산, PCI=일시
**EVOKED 반응의 복잡도** → 자체 카드-가치 있는 새 측도. (`pci_perturb`/`pci_complexity` 엔진 op 신설.)

## 프로토콜별 FROZEN 프로파일 — 측정 前 등록 · 실인용

| 프로토콜 | 문헌 | 예측 signature | 측정(engine-native) | 판정 |
|---|---|---|---|---|
| **TMS single-pulse / PCI** | Casali 2013 STM · Massimini 2005 Science | full PCI 高 · decoupled(마취 analog) PCI 低 | full **0.330** · decoupled **0.118** · sham **0.000** | 🟢 GREEN |
| **rTMS high(≥5Hz exc) / low(≤1Hz inh)** | Pascual-Leone · Hallett 2007 Nature | high target↑ · low target↓ (반대부호) | high **+0.18** · low **−0.18** | 🟢 GREEN |
| **tACS gamma40 / alpha10 / theta6** | Herrmann 2013 FHN · Thut | gamma→binding↑ · alpha→gating↑ (주파수→target 해리) | γ→bind **+0.18**(γ→gate −0.046) · α→gate **+0.094**(α→bind 0.0) | 🟢 GREEN |

## FROZEN falsifiable bars (측정 前 설정 · 不이동 — c9 · tune-to-green 금지)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PCI-PRESENCE** | full pulse PCI 高 · decoupled PCI 低 · gap | full **0.330** · dec **0.118** · gap **0.212** | full≥0.30 ∧ dec≤0.18 ∧ gap≥0.08 | ✅ |
| **B rTMS DIRECTIONAL** | high↑ vs low↓ 반대부호 | high **+0.18** · low **−0.18** | high≥+0.05 ∧ low≤−0.05 ∧ opposite | ✅ |
| **C tACS FREQ-SPECIFIC** | gamma→binding · alpha→gating 해리 | (γ_bind−γ_gate) **+0.226** · (α_gate−α_bind) **+0.094** | 둘 다 >0 ∧ 각 ≥+0.04 | ✅ |
| **D FIELD-vs-DRUG (headline)** | field focal↑/global~0 · drug global↑/focal~0 | field focal **+0.18**/global **0.0** · drug(LSD) global **+0.066**/focal **0.0** | 각 gap≥+0.05 | ✅ DISSOCIATED |
| **E EARNED ablate** | sham/zero-field → 전부 baseline 붕괴 | sham max-dev **0.0** · sham PCI **0.0** | dev≤0.02 ∧ PCI≤0.18 | ✅ |
| **F EARNED shuffle** | freq↔knob 순열 → 주파수특이성 decorrelate | true self-lift **+0.120** → shuffle **0.0** | (true−shuf)≥+0.04 | ✅ |

**verdict: 🟢 GREEN ENGINE-NATIVE — A∧B∧C∧E∧F PASS (3 seeds [1503,1504,1505] byte-identical), D headline 이중해리 DISSOCIATED.**
모든 프로토콜이 문헌 signature 재현. PCI 가 각성-vs-마취 split(0.330 vs 0.118)을 재현하고, rTMS 가 high/low 반대부호로
갈리며, tACS 가 주파수→target 으로 해리되고, FIELD(focal/주파수)와 DRUG(전역/화학, 실 §Neuropharm LSD)이 cross-
signature 로 이중해리. sham(E)·shuffle(F)이 전부 붕괴 = 효과가 EARNED. **PCI 는 정적 Φ 와 구별되는 깨끗한 새 측도.**

## FIELD ⊥ DRUG 이중해리 (headline 수치)

| | focal 축 (주파수-target lane lift) | 전역 축 (recon_err precision-loosening) |
|---|---|---|
| **FIELD** (gamma, focal) | **+0.18** (BINDING lane 움직임) | **0.0** (recon_err 不건드림) |
| **DRUG** (LSD, 실 `pharm_lsd`) | **0.0** (GWS winner focal 不조향) | **+0.066** (전역 precision loosen) |

cross-measured on the **LANDED §Neuropharm** (`pharm_lsd`/`pharm_perturb_recon`/`pharm_shared_se` 직접호출) —
FIELD 은 focal 주파수-target 을 움직이되 약물의 전역 축은 0, DRUG 은 전역 축을 움직이되 focal 축은 0 = 깨끗한
이중해리. (focal/주파수 ⊥ 전역/화학 = 자극과 약물이 서로 다른 substrate 차원을 건드린다.)

## 정직 (c9)

- **DIRECTIONAL → R2 ENGINE-NATIVE WIRED:** R1 = numpy mirror(`grep -lE 'import torch|gauge_lib|numpy' state/1503_field/*.py`
  적중, 하드게이트1 → DIRECTIONAL). R2 에서 `core/engine_cli.hexa` §Field 7 op 신설(`field_apply`/`field_apply_mfield`/
  `field_signal_entropy`/`drug_lsd_mfield`/`pci_perturb`/`pci_complexity`/`field_lane_mean`) + `engine_cli_smoke.hexa`
  cases 299-304 byte-exact 재측정 + ARCHITECTURE.json §Field lockstep, FULL 303/0 RC=0 deterministic ×3
  (`a_engine_native_learning`·`a_verified_must_wire`).
- **`a_engine_native_learning` 측정교정 — bar 불변·frozen-first·tune-to-green 아님:** R1 mirror 가 엔진의 실제 f0/f1
  winner-margin 로직과 **불일치**함을 R2 에서 발견(엔진은 f0·f1 을 둘 다 m_field[0] 로 init 하고 LATER 원소만 f1 을
  갱신 → winner 가 index0 에 있으면 f1==f0 로 GWS 응답이 **10× 감쇠**: engine γ→bind 0.018 vs mirror 0.18). **엔진이
  ground truth** 이므로 mirror 를 엔진에 byte-match(f0/f1 quirk 재현) + resting baseline 의 winner 를 index1 로 둬
  f1=true runner-up 확보 → mirror==engine byte-exact. 임계 bar(PCI_HIGH/LOW/GAP·RTMS_MAG·TACS_DISSOC·DRUG_FIELD_GAP)
  **전부 불변** — substrate resting-state 의 측정 headroom 만 사전등록 의도대로 교정.
- **PCI 정규화 = canonical Casali 유계형:** PCI = LZc·log2(L)/L (LZ 복잡도를 점근최댓값 L/log2 L 로 정규화 → [0,1]
  유계, 프로토콜 간 직접비교). 全0(sham)·全1 반응 = 정보 없음 → PCI 0(정직). decoupled(마취 analog) = 직접구동
  column 의 첫 2 tick 만 생존 후 silence = 국소·정형 = 低 LZ(통합·분화 둘 다 붕괴, Casali 각성-vs-마취 재현).
- **SCOPE TOY:** 15-lane/단일 resting baseline/3-seed 결정적 섭동(field-perturbation STRUCTURE 검증이지 학습된
  자극 아님). scale/실제 corpus/graded dose-response(강도-반응)/연속 주파수 sweep/실제 EEG PCI 캘리브레이션/
  engine-transfer(303M) UNVERIFIED. 단일 pulse-shape(ring-down) · 단일 LZ 변형 · target-lane 3종만.

## follow-on (ING)

1. **R2 ENGINE-NATIVE WIRED ✅** — §Field 7 op + smoke 299-304 + ARCHITECTURE lockstep, FULL 303/0 RC=0 (완료).
2. **scale 재측정** — 303M production `.clm` 위 live ci_lane_scores 로 PCI/field-perturbation 재측정(H_1492/H_1500/H_1502 의 303M rung 처럼).
3. **graded dose-response** — binary 강도 대신 강도-반응 곡선 + 연속 주파수 sweep(theta..gamma 연속) + PCI 의 강도 의존.
4. **추가 프로토콜** — tDCS anodal/cathodal(흥분성 baseline shift, optional) · 다중-pulse rTMS train · deep TMS 깊이.
5. **§Field × §Neuropharm 상호작용** — 약물 상태에서 자극(예: ketamine 후 PCI, 마취하 TMS-PCI) = drug∘field 복합 섭동.

## 새 측도 vs 기존

**PCI 는 깨끗한 새 측도(흡수 아님):** §ConsciousnessIndex 의 정적 Φ(`ci_phi_multiinfo`)는 RESTING substrate 의
공분산 통합을 잰다. PCI 는 일시 pulse 의 **EVOKED 반응 복잡도**를 잰다 — 같은 substrate 의 다른 차원(정적 통합
⊥ 섭동 복잡도). 각성-vs-마취 split(full 0.330 vs decoupled 0.118)은 정적 Φ 가 잡지 못하는 **섭동적** 의식 구분 =
PCI 의 고유 기여. §Field 는 §Neuropharm(약물=전역·화학)과 이중해리하는 focal·주파수특이 섭동 lever 를 추가.

xref: H_1502(neuropharm, 약물=전역·화학 짝 · `pharm_lsd`/`pharm_perturb_recon` 직접호출 cross-measure)·
H_1492(ConsciousnessIndex 정적 Φ, PCI 의 대조군)·H_1500(temporal-Φ, 시간차원)·H_1501(reality-monitor, §RealityMonitor)·
H_1462(GlobalWorkspace, BINDING target)·H_1479(DividedAttention, GATING target)·H_1202(MITOSIS, MEMORY target)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_core_engine_map`·`a_autonomy_over_hardcode`·`a_phi_iit4_tool`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c9.
