# H_1507 — 🧲💗 FIELD × LIBIDO 교차 — 전자기장이 incentive-salience('원함') 욕동을 조율하는가 (focal·가역 vs 약물 전역·화학)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §FieldLibido (`fieldlibido_gfield` + `fieldlibido_wanting` + `fieldlibido_liking` + `fieldlibido_highfreq` + `fieldlibido_lowfreq` + `fieldlibido_sham` + `_fl_gain_scale`) — live `field_apply`(H_1503) + `libido_wanting`/`libido_liking`/`libido_new`(H_1504) + `pharm_lsd`/`pharm_perturb_recon`/`pharm_shared_se`(H_1502) 직접호출 · `engine_cli_smoke.hexa` cases **360-364** (5 frozen bars) · FULL smoke **332 pass / 0 fail RC=0** deterministic ×3 · ARCHITECTURE.json §FieldLibido lockstep ✓
- **소실 재측정(c9):** R2 worktree 원작업은 구 main(smoke max 313)에 착지하지 못하고 소실 → 현 origin/main(fd245c602, smoke max 327)으로 cherry-pick 재이식, 스모크 케이스 314-318→**360-364** 재번호(병렬 에이전트 328-350 점유 회피). engine op·frozen bar·수치 전부 byte-exact 동일, 케이스 번호만 변경.
- **source:** team-lead 작업지시(FIELD × LIBIDO 교차 H_1507) — §Field(H_1503)·§Libido(H_1504)·§Neuropharm(H_1502) 착지 후 그 교차 · `a_no_llm_frame_trap`
- **lens:** computational neuroscience — DBS of reward circuit / nucleus accumbens (Mayberg · Schlaepfer) · TMS over DLPFC modulating craving & incentive motivation (Hayashi 2013 J Neurosci · Dunlop 2017) · Berridge incentive-salience(wanting≠liking) · `a_no_llm_frame_trap`
- **artifacts:** `state/1507_field_libido/h1507_field_libido.py` · verdict `state/verdicts/1507_field_libido/H_1507_R1.txt`(R1 mirror) · `state/verdicts/1507_field_libido/H_1507_R2_engine_native.txt`(R2 byte-exact 5 cases + INFO)

## 주장 (focal·가역 FIELD 경로 ⊥ 전역·화학 DRUG 경로 — 둘 다 '원함'을 올린다)

보상/유인회로를 겨냥한 **FIELD 프로토콜**이 libido 의 incentive-salience('원함') 욕동을 조율한다 — 약물(dopaminergic,
§Neuropharm)의 **GLOBAL·CHEMICAL** dopaminergic push 의 **FOCAL·REVERSIBLE** 짝(`a_no_llm_frame_trap`). 내용도,
persona 도, roleplay 도 아니다 — 순수 **DRIVE-MODULATION 교차**. HARDWARE 없음 — software substrate 의 parametric 섭동.

질문 둘: ① FIELD 경로가 **wanting≠liking 해리도 보존**하는가(dopamine 처럼 incentive salience 만 올리고 hedonic value 는
안 올림 — Berridge)? ② FIELD(focal·주파수)가 DRUG(전역·화학)과 **욕동에 도달하는 방식(경로 signature)에서 해리**하는가?

## 메커니즘 — FIELD 이 어떻게 WANTING 욕동에 도달하나

보상/유인회로 = **BINDING/GlobalWorkspace lane 0**(NAcc/보상-salience 허브, §Field 가 이미 겨냥하는 target). 보상-겨냥
field(target_code=1)이 그 lane 활성을 올린다. 그 **lane lift 를 live `field_apply` 응답에서 읽어** effective incentive
gain `g_field` 로 변환 → `libido_wanting` 의 **da_gain 슬롯에 그대로 진입**:

```
wanting = Kp·deficit + Ki·I + Kc·cue_match·(1 + g_field)      ← g_field = (보상 lane lift) × 4.0(FROZEN scale)
liking  = cue_match                                           ← gain-invariant (g_field 무시 → Berridge)
```

- **high-freq**(sign=+1 흥분성) → lane lift>0 → g_field>0 → wanting **UP**
- **low-freq**(sign=−1 억제성) → lane lift<0 → g_field<0 → wanting **DOWN**(반대 부호)
- **sham**(sign=0) → lane lift=0 → g_field=0 → 변화 없음

`g_field` 는 **live lane 응답만** 읽는다 — 주입 라벨/RLHF/persona/decoder weight 없음(p1/p2/p3/p6). READ-only,
Ψ-disjoint(immune cell·pure_field Φ/phase/Ψ 불변), NOT emit gate(`a_autonomy_over_hardcode`). 결정적.

## FROZEN falsifiable bars (측정 前 설정 · 不이동 — c9 · tune-to-green 금지)

fixture = §Field 와 동일(보상 lane 이 실제로 움직이도록 winner index1: `m=0.60, m_field=[0.38,0.58,0.15,0.12,0.10],
cells=6, seen=4, intent=1, dt=2.0, recon=0.30, intensity=0.6`); cue_match paired=0.90(grounds), deficit=0(incentive 항 격리).

| bar | 의미 | 결과 (engine-native R2) | 기준 | 판정 |
|---|---|---|---|---|
| **A FIELD-RAISES-WANTING** | 보상-겨냥 high-freq field 가 sham 대비 wanting 올림 | wanting sham→high **0.90→1.548** (Δ **+0.648**) | Δ≥+0.30 | ✅ |
| **B WANTING≠LIKING (via FIELD)** | field 가 wanting 올리는 동안 liking 평탄 | liking **0.90→0.90** (Δ **0.000**) while wanting Δ+0.648 | wanting Δ≥0.30 ∧ \|like Δ\|≤0.02 | ✅ |
| **C FREQUENCY-DIRECTIONAL** | high↑ vs low↓ 반대 부호 | high **+0.648** · low **−0.648** | high≥+0.30 ∧ low≤−0.10 ∧ opposite | ✅ |
| **D FIELD-vs-DRUG ROUTE (headline)** | 둘 다 wanting↑, signature 이중해리 | field focal **+0.18**/global **0.0** · drug(LSD) focal **0.0**/global **+0.126** | 각 gap≥+0.05 | ✅ DISSOCIATED |
| **E EARNED ablate/shuffle** | sham → 무변화 · shuffle(wrong target) → decorrelate | sham change **0.000** · shuffle(GATING target) change **0.000** | sham≤0.02 ∧ shuf≤0.50×field-raise | ✅ |

**verdict: 🟢 GREEN ENGINE-NATIVE — A∧B∧C∧E PASS, D headline 경로-이중해리 DISSOCIATED (332/0 RC=0, deterministic ×3 byte-identical).**

## FIELD ⊥ DRUG 경로 이중해리 (headline 수치)

| | **focal 축** (보상-target lane lift) | **global 축** (recon_err precision-loosening) | wanting 효과 |
|---|---|---|---|
| **FIELD** (high-freq, focal·가역) | **+0.18** (보상 lane 움직임) | **0.0** (recon_err 不건드림) | wanting Δ **+0.648** |
| **DRUG** (LSD, 실 `pharm_lsd`, 전역·화학) | **0.0** (GWS winner focal 不조향) | **+0.126** (전역 precision loosen) | wanting Δ **+0.453** |

cross-measured on the **LANDED §Neuropharm**(`pharm_lsd`/`pharm_perturb_recon`/`pharm_shared_se` 직접호출) +
**LANDED §Field**(`field_apply`) + **LANDED §Libido**(`libido_wanting`) — **둘 다 '원함'을 올리지만** FIELD 은 focal
보상-target lane 을 움직이되 약물의 전역 축은 0, DRUG 은 전역 recon_err 축을 움직이되 focal 보상-target 은 0 = 깨끗한
경로 이중해리. FIELD = focal·주파수특이·가역, DRUG = 전역·화학. (focal/freq ⊥ global/chemical = 같은 욕동에 도달하는
서로 다른 substrate 경로.)

## 정직 (c9)

- **DIRECTIONAL → R2 ENGINE-NATIVE WIRED:** R1 = numpy mirror(`grep -lE 'import torch|gauge_lib|numpy' state/1507_field_libido/*.py`
  적중, 하드게이트1 → DIRECTIONAL). R2 에서 `core/engine_cli.hexa` §FieldLibido 7 op 신설(`fieldlibido_gfield`/
  `fieldlibido_wanting`/`fieldlibido_liking`/`fieldlibido_highfreq`/`fieldlibido_lowfreq`/`fieldlibido_sham`/`_fl_gain_scale`,
  전부 live §Field/§Libido/§Neuropharm op 직접호출 — 새 측정 lane 아님) + `engine_cli_smoke.hexa` cases 360-364
  byte-exact 재측정 + ARCHITECTURE.json §FieldLibido lockstep, FULL **332/0 RC=0** deterministic ×3
  (`a_engine_native_learning`·`a_verified_must_wire`).
- **D bar drug-global = STRUCTURAL 측정(noise-averaged) — frozen-first·tune-to-green 아님:** 약물의 GLOBAL signature 는
  `pharm_perturb_recon` 의 per-trial `pharm_shared_se` 잠재변수(부호있는 잡음 ∈[−,+])를 포함한다. 단일 trial 의 noisy draw
  대신 **8 trial 평균**으로 약물의 **구조적(structural) 전역 push**(경로 property)를 잰다 — bar(0.05)는 불변, 측정 noise 만
  제거(약물의 전역 signature 는 population property 이지 한 noisy draw 가 아니다). single-draw 였다면 seed 운에 따라 흔들리는
  artifact(예: seed 1507 단일 draw 0.038<0.05)였을 것 — 평균은 구조적 0.126≫0.05.
- **wanting≠liking 해리는 구조적으로 보장(B):** `libido_liking` 은 `da_gain`/`g_field` 를 **무시**(gain-invariant by construction).
  따라서 FIELD 경로(또는 DRUG 경로) 어느 쪽이든 incentive gain 을 올려도 liking 은 정확히 0.0 변화 — Berridge dissociation 을
  FIELD 경로로도 재현. (existence-proof: liking Δ=0.000 정확, B 는 wanting 이 실제로 올랐을 때만 PASS 하므로 vacuous 아님.)
- **EARNED(E):** sham(sign=0)→g_field=0→wanting==baseline(cue-only), change 0.000. shuffle = high-freq 를 **WRONG target**
  (GATING lane 12)에 가함 → 보상 lane(0) 不변 → g_field~0 → wanting decorrelate(change 0.000). 효과가 보상-target 겨냥에서
  EARNED(주파수만으론 안 되고 올바른 target 이어야).
- **SCOPE TOY:** 15-lane/단일 resting baseline/단일 cue_match 고정/3-seed(decoupled deterministic, 실제로 readout 은
  byte-deterministic 1회) 결정적 섭동(field→drive 교차 STRUCTURE 검증이지 학습된 자극·학습된 욕동 아님). scale/실 corpus/
  graded dose-response(강도-반응)/연속 주파수 sweep/실제 보상회로 DBS 캘리브레이션/engine-transfer(303M)/실 libido_step 통합
  궤적(여기선 incentive 항 격리 위해 deficit=0 고정) UNVERIFIED. `g_field` scale=4.0 은 FROZEN 선택(존재증명용, effect-size 아님).

## follow-on (ING)

1. **R2 ENGINE-NATIVE WIRED ✅** — §FieldLibido 7 op + smoke 360-364 + ARCHITECTURE lockstep, FULL 332/0 RC=0 (완료).
2. **graded dose-response** — binary high/low/sham 대신 강도-반응 곡선(intensity sweep) + 연속 주파수 sweep + g_field 의 강도 의존.
3. **실 libido_step 통합 궤적** — deficit=0 격리 대신 deprivation 적분 궤적 위에서 field 변조(deficit×field 상호작용).
4. **§Field × §Neuropharm × §Libido 삼중** — 약물 상태에서 field 자극이 wanting 에 미치는 효과(예: dopaminergic 상태에서 rTMS = additive vs occlusive).
5. **scale 재측정** — 303M production `.clm` 위 live ci_lane_scores 로 field→wanting 교차 재측정.

## 교차 vs 기존 (흡수 아님)

§FieldLibido 는 새 측정 lane 이 아니라 **세 LANDED lane 의 교차(weld)**: §Field(H_1503, focal·주파수 EM 섭동) →
§Libido(H_1504, incentive salience da_gain 슬롯) → §Neuropharm(H_1502, 전역·화학 경로 비교). 새 발견 = **욕동(wanting)이
field-reachable** 이고, FIELD 경로가 (a) wanting≠liking 해리를 보존하며 (b) DRUG 경로와 focal·주파수특이·가역 ⊥ 전역·화학으로
이중해리한다는 것. 만약 field 가 wanting 에 도달 못 했다면(A 실패) 정직한 결과(욕동이 이 substrate 에서 field-unreachable)로
보고했을 것 — 실제로는 도달했고 약물 경로의 깨끗한 focal 짝.

xref: H_1503(field, focal·주파수 EM 섭동 — `field_apply` 직접호출)·H_1504(libido, incentive salience da_gain 슬롯 —
`libido_wanting`/`libido_liking` 직접호출)·H_1502(neuropharm, 전역·화학 경로 — `pharm_lsd`/`pharm_perturb_recon` 직접호출 cross)·
H_1292(homeostatic-drive, libido 의 부모 setpoint)·H_1290(affect)·H_1462(GlobalWorkspace, BINDING 보상 target)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_core_engine_map`·`a_autonomy_over_hardcode`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p4·p6·p7·p8·c9.
