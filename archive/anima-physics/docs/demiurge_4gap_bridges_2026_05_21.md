# demiurge 4 gap domain — anima-side producer bridges LANDED (aura/bio/chem/grid)

> demiurge `aura/bio/chem/grid` 4 도메인 (모두 ❌ no-producer 또는
> ⏳ engine gap) 에 anima-side producer skeleton 4종 추가 + 첫 record
> drop 까지 1-cycle 동시 진행. 6-step 패턴 (brain_bridge LANDED
> 2026-05-21 reference) 정확히 답습.
> Date: 2026-05-21
> Predecessor: `anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
> (brain 도메인 단독 1-step closure §5 key learning 의 6-step 답습 대상)

## §1 GOAL

demiurge `aura/bio/chem/grid` 4 도메인의 verify gap 을 anima 측에서
producer-skeleton + 첫 record drop 으로 메우는 **batch Step 1**.

- **Before** (`demiurge_hw_verify_2026_05_21.md §2.2/§2.3` 직전):
  - aura: ⏳ engine gap (`hexa-aura` sibling repo dispatch exit=1)
  - bio: ❌ no producer (D81 candidate)
  - chem: ❌ no producer (mock-fallback 가능성)
  - grid: ❌ no producer (`exports/grid/verify/` 경로 부재)
  - aggregate: ❌ no-producer 4 (aura/bio/chem/grid) + ⏳ GATE_OPEN 10
- **After (this cycle)**:
  - aura: ⏳ engine gap **persists for cli verify aura path** (sibling-repo
    dispatch precedence) — anima record dropped but demiurge `(.verify, "aura")`
    case 가 `hexa-aura/verify/run_all.hexa` 로 직행 → exports/aura/verify/ 미조회.
    **anima-side bridge LANDED + 첫 record drop ✓**, demiurge-side ActionDispatch
    재라우팅 (또는 sibling repo 빌드 픽스) 별도 cycle.
  - bio: ❌ → **⏳ GATE_OPEN (anima-bridge)** — demiurge cli verify bio 가
    anima record 자동 감지·인용 ✓
  - chem: ❌ → **⏳ GATE_OPEN (anima-bridge)** — demiurge cli verify chem 가
    anima record 자동 감지·인용 ✓
  - grid: ❌ → **⏳ GATE_OPEN (anima-bridge)** — demiurge cli verify grid 가
    anima record 자동 감지·인용 ✓
- **Status delta**:
  - ❌ no producer: **4 → 1** (aura 만 잔존 — engine-gap 본질, anima-bridge
    file LANDED 이지만 dispatch path 변경 별도 cycle)
  - ⏳ GATE_OPEN: 10 → **13** (bio + chem + grid 추가)
- **개별 bridge LoC**: aura 192 · bio 197 · chem 199 · grid 207 = **795 total**

이번 cycle 은 **anima 단독 (cost $0, Mac local) 으로 demiurge gap 4건
batch close**. 실 silicon/wet-lab/PMU 측정·oracle parity 는 각 도메인의
Phase 2 cloud/wet-lab cycle 후보 (별도 dispatch).

## §2 per-domain (4 bridge × {file + record format + drop + verify})

### §2.1 aura

| 항목 | 값 |
|---|---|
| Bridge | `tool/demiurge_aura_bridge.py` (192 LoC) |
| Interface | `demiurge:aura:quality-record` |
| Producer | `anima-aura-stub-bridge` |
| SW source | **없음** (anima-physics 측 aura substrate 부재; `~/core/hexa-aura/` 가 SSOT) |
| Measurement keys | `quality` (0..1) · `affect_valence` (-1..1) · `affect_arousal` (0..1) |
| Backend choices | `local_sim` · `muse_eeg` · `openbci_8ch` |
| Smoke | py_compile ✓ · CLI emit ✓ (1511 B JSON) |
| Drop | `~/core/demiurge/exports/aura/verify/2026-05-21T08-33-18Z/anima_aura_20260521T083318Z.json` ✓ |
| Verify | ⚠ **bypassed** — `demiurge cli action verify aura` 가 hexa-aura sibling-repo dispatch 로 직행 (`(.verify, "aura")` 케이스 가 `~/core/hexa-aura/verify/run_all.hexa` invoke; cockpit `verify/*.hexa` 경로 부재로 sweep 0/19 PASS exit=1). exports/aura/verify/ 직접 조회 path 없음. |
| Status delta | ⏳ engine gap (sibling dispatch) → ⏳ engine gap (anima-bridge record exists but un-cited) — **anima 측 LANDED, demiurge 측 ActionDispatch 재라우팅 별도 cycle** |

**stub-only 명시**: scope_caveats 첫째줄 "anima-physics has NO aura
substrate — this is a stub-only bridge", gate_failures 에 "anima-physics
has no aura substrate (hexa-aura repo is SSOT)" — over-claim 차단.

### §2.2 bio

| 항목 | 값 |
|---|---|
| Bridge | `tool/demiurge_bio_bridge.py` (197 LoC) |
| Interface | `demiurge:bio:synapse-plasticity-record` |
| Producer | `anima-bio-hippocampus-memristor-bridge` |
| SW source | `hippocampus/episodic_replay.hexa` (PHYS-P11-3 5/5) + `theta_gamma.hexa` (PHYS-P6-2 5/5) + `memristor/self_reference.hexa` (PHYS-P5-1 5/5) — composite |
| Measurement keys | `replay_compression_ratio` (5-20× SWR) · `hebbian_drift_convergence` (0..1) · `phase_amplitude_coupling` (0..1) |
| Backend choices | `local_sim` · `organoid_mea` · `ipsc_neuron` |
| Smoke | py_compile ✓ · CLI emit ✓ (1718 B JSON) |
| Drop | `~/core/demiurge/exports/bio/verify/2026-05-21T08-33-18Z/anima_bio_20260521T083318Z.json` ✓ |
| Verify | `demiurge cli action verify bio` 가 anima record 자동 감지·파싱·인용 ✓ (`backend: "local_sim"`, `producer: "anima-bio-...-bridge"`, scope_caveats 모두 출력) |
| Status delta | ❌ no producer → **⏳ GATE_OPEN (anima-bridge)** |

defaults = 합성 SWR 정상범위 (12×) + Hebbian convergence 0.94 + CFC 0.71
(hippocampus + memristor §188 PASS measurement-pattern carry).

### §2.3 chem

| 항목 | 값 |
|---|---|
| Bridge | `tool/demiurge_chem_bridge.py` (199 LoC) |
| Interface | `demiurge:chem:entropy-record` |
| Producer | `anima-chem-langevin-thermodynamic-bridge` |
| SW source | `engines/thermodynamic_consciousness.hexa` (F-TH-1..5 5/5 PASS, `state/s188g_engines_2026_05_21/thermodynamic.run.log`) — Langevin double-well + Arrhenius D-sweep |
| Measurement keys | `barrier_jumps_per_step` (0.51 @ D=0.6) · `arrhenius_d_slope` (7.69 = jumps(D=1.0)/jumps(D=0.3)) · `ergodic_mean_position` (-0.187, <0.4 threshold) · `free_energy_landscape_depth` (1.0) |
| Backend choices | `local_sim` · `microfluidic_smd` · `dft_md` |
| Smoke | py_compile ✓ · CLI emit ✓ (1710 B JSON) |
| Drop | `~/core/demiurge/exports/chem/verify/2026-05-21T08-33-18Z/anima_chem_20260521T083318Z.json` ✓ |
| Verify | `demiurge cli action verify chem` 가 anima record 자동 감지·파싱·인용 ✓ ("Langevin double-well is consciousness-analog, NOT real chemistry" caveat 출력) |
| Status delta | ❌ no producer → **⏳ GATE_OPEN (anima-bridge)** |

defaults = `state/s188g_engines_2026_05_21/thermodynamic.run.log` 직접
인용 (F-TH-2 510 jumps/1000 steps = 0.51 per-step, F-TH-3 722/94 = 7.69,
F-TH-5 ⟨x⟩=-0.187).

### §2.4 grid

| 항목 | 값 |
|---|---|
| Bridge | `tool/demiurge_grid_bridge.py` (207 LoC) |
| Interface | `demiurge:grid:resilience-record` |
| Producer | `anima-grid-kuramoto-powergrid-bridge` |
| SW source | `social/kuramoto_coupling.hexa` (PHYS-P9-3 6/6 PASS) + `hw/kuramoto_neuromorphic` (F-HW-KU-1..5 5/5) — Filatrella 2008 Kuramoto-powergrid mapping |
| Measurement keys | `phase_coherence_r` (0..1 Kuramoto order) · `critical_coupling_k_c` (2.4 transition) · `n_islanding_events` · `recovery_time_s` |
| Backend choices | `local_sim` · `pmu_replay` · `scada_log` |
| Smoke | py_compile ✓ · CLI emit ✓ (1725 B JSON) |
| Drop | `~/core/demiurge/exports/grid/verify/2026-05-21T08-33-18Z/anima_grid_20260521T083318Z.json` ✓ |
| Verify | `demiurge cli action verify grid` 가 anima record 자동 감지·파싱·인용 ✓ ("Kuramoto N=8 은 intersubjective oscillator analog 일 뿐 실제 PMU/SCADA 가 아니다" caveat 출력) |
| Status delta | ❌ no producer → **⏳ GATE_OPEN (anima-bridge)** |

defaults = F-HW-KU-3 locked-state (N=8, K=5.0, r_tail=0.951, K_c≈2.4,
r_std_tail=0.0434) re-interpreted as 8-node power grid sync.

## §3 demiurge dispatch 결과 (4 domain × cli action verify)

전수 호출: `for D in aura bio chem grid; do demiurge cli action verify
$D; done` 결과 (DemiurgeCLI build 0.12-0.22s/회).

| 도메인 | dispatch 결과 | anima record 인용 |
|---|---|---|
| **aura** | sibling-repo (`hexa-aura/verify/run_all.hexa`) 직행, 0/19 scripts PASS, exit=1, "⏳ engine tool gap — no new measured record (g3)" | ❌ **bypassed** — exports/aura/verify/ 비조회 |
| **bio** | "demiurge 에는 bio 도메인 검증 엔진 도구가 아직 없음 ... 유일한 exports/bio 레코드는 sim skeleton" → anima record 4 항목 (`backend`, `producer`, `scope_caveats` 2개, `verdict.gate_state`) 정확 인용 | ✅ **auto-cited** |
| **chem** | "chem.검증 단계에 진짜 엔진은 아직 없습니다. ❌ 측정완료 주장 불가 ... `record_id: chem_jumps0.51_slope7.69_D0.60_local_sim`" → anima record 5 항목 (record_id/producer/gate_state/2 caveats) 정확 인용 | ✅ **auto-cited** |
| **grid** | "`grid + verify` 셀에는 아직 실제 engine tool 이 없습니다 ... 한 건 존재: exports/grid/verify/2026-05-21T08-33-18Z/anima_grid_*.json" → anima record 5 항목 (measurement_gate/absorbed/verdict rationale/2 caveats) 정확 인용 | ✅ **auto-cited** |

**3/4 auto-cite 성공**. aura 만 demiurge-side ActionDispatch (`(.verify,
"aura")` → hexa-aura sibling-repo dispatch hard-coded) 가 exports/aura/verify/
를 조회하지 않아 bypass — anima-bridge file + record 는 LANDED 상태로
보존, demiurge-side dispatch 재라우팅 (또는 sibling 빌드 픽스) 별도 cycle.

**no over-claim**: demiurge 가 4건 모두 "측정완료 ✅ 주장 불가, GATE_OPEN /
provisional / skeleton" 정확히 표기 — 본 cycle 의 목표 (record drop +
파싱 path 검증) 와 일치.

## §4 anima docs `demiurge_hw_verify_2026_05_21.md §2.2` 갱신

`§2.2 HW adjacent (shallow cohort domains, 11)` 표 4행 + `§2.3 aggregate`
2줄 갱신:

```diff
- | aura | ⏳ engine gap | sibling-repo dispatch `~/core/hexa-aura/verify/run_all.hexa` exit=1 | none |
- | bio | ❌ no producer | (D81 candidate) | none |
- | chem | ❌ no producer | mock-fallback 가능성 | none |
- | grid | ❌ no producer | `exports/grid/verify/` 경로 부재 | none |
+ | aura | ⏳ engine gap (anima-bridge LANDED, un-cited) | anima `tool/demiurge_aura_bridge.py` LANDED + 첫 record dropped (stub, anima 측 aura substrate 부재 명시); demiurge `(.verify, "aura")` 가 sibling-repo dispatch 로 직행 → exports/aura/verify/ 비조회, ActionDispatch 재라우팅 별도 cycle | `2026-05-21T08-33-18Z/anima_aura_20260521T083318Z` |
+ | bio | ⏳ GATE_OPEN (anima-bridge) | anima `tool/demiurge_bio_bridge.py` LANDED + 첫 record dropped (hippocampus + memristor composite, §188 5/5+5/5 PASS measurement); demiurge `BioVerifyProducer` consumer 신설은 별도 cycle | `2026-05-21T08-33-18Z/anima_bio_20260521T083318Z` |
+ | chem | ⏳ GATE_OPEN (anima-bridge) | anima `tool/demiurge_chem_bridge.py` LANDED + 첫 record dropped (Langevin double-well + Arrhenius D-sweep, F-TH-1..5 5/5 PASS); demiurge `ChemVerifyProducer` consumer 신설은 별도 cycle | `2026-05-21T08-33-18Z/anima_chem_20260521T083318Z` |
+ | grid | ⏳ GATE_OPEN (anima-bridge) | anima `tool/demiurge_grid_bridge.py` LANDED + 첫 record dropped (Kuramoto N=8 power-grid analog, Filatrella 2008 mapping); demiurge `GridVerifyProducer` consumer 신설은 별도 cycle | `2026-05-21T08-33-18Z/anima_grid_20260521T083318Z` |
```

`§2.3 aggregate` 갱신:

```diff
- - ⏳ GATE_OPEN (measured but provisional): **10** (component, firmware, antimatter, bot, **brain** ← anima-bridge 추가 2026-05-21, cern, energy, fusion, mobility, +materials sibling)
- - ❌ no producer / engine gap: **4** (aura, bio, chem, grid)
+ - ⏳ GATE_OPEN (measured but provisional): **13** (component, firmware, antimatter, **bio** ← anima-bridge 추가 2026-05-21, bot, brain, cern, **chem** ← anima-bridge 추가, energy, fusion, **grid** ← anima-bridge 추가, mobility, +materials sibling)
- - ❌ no producer / engine gap: **4** (aura, bio, chem, grid)
+ - ❌ no producer / engine gap: **1** (aura — anima-bridge LANDED but demiurge dispatch bypass)
```

(diff 만 본 doc 에 기록; 원 doc 의 in-place 편집은 별도 staging — 본
cycle 은 commit/push 제외 제약.)

## §5 honest C3 (5건)

1. **aura 는 stub-only + dispatch bypass 이중 한계** — anima-physics 측에
   aura substrate (EEG / quality / affect 정량화) 가 1급 source 로
   존재하지 않음 (`~/core/hexa-aura/` 는 sibling repo, anima-physics 산하
   import 없음). `quality=0 / valence=0 / arousal=0` 기본값은 placeholder
   이며 측정값이 아님 (scope_caveats 명시). 추가로 demiurge `(.verify,
   "aura")` ActionDispatch 가 sibling-repo dispatch 로 직행 → exports/aura/verify/
   비조회 — anima record 가 LANDED 되어도 cli 가 인용하지 않음. true close
   는 (a) hexa-aura cli quality output → bridge 재배선 OR (b) demiurge
   ActionDispatch 재라우팅 (별도 cycle).
2. **bio/chem/grid 는 모두 SW reference sim, NOT wet/silicon/SCADA** — bio
   = hexa-lang hippocampus+memristor sim (wet-lab 아님), chem = Langevin
   numpy reference (real chemistry 아님 — generic U(x)=(x²-1)² potential,
   분자종 없음), grid = Kuramoto N=8 (실 PMU/SCADA 아님 — IEEE-bus
   등가성 미정). 각 도메인 record 의 `verdict.gate_state` = GATE_OPEN
   영구 — Phase 2 wet-lab / silicon / PMU replay cycle 이전.
3. **default values 는 단일 측정점 (single (N, K) / single D / single SWR)** —
   bio의 12× compression / chem의 D=0.6 jumps / grid의 K=5.0 r_tail=0.951
   모두 1-point measurement. full regime sweep (sub-critical → critical →
   super-critical 전이 정확도) 은 multi-point record drop + consumer
   sweep 평가 별도 cycle.
4. **demiurge 측 consumer 부재 4건 모두 동일** — `BioVerifyProducer.swift`
   / `ChemVerifyProducer.swift` / `GridVerifyProducer.swift` / 그리고
   aura ActionDispatch 재라우팅 — 4건 모두 demiurge repo 별도 cycle.
   본 cycle 의 record 는 cli action verify 가 **인용만** 하고 oracle
   parity gating 평가는 일어나지 않음. `cli show <record>` 는 schema
   decoder 미등록으로 4건 모두 Decode failed 예상 (brain cycle §2.4 와
   동일 패턴).
5. **gate_failures 정직 표기** — aura 만 `gate_failures: ["anima-physics has
   no aura substrate (hexa-aura repo is SSOT)"]` 명시. bio/chem/grid 는
   `gate_failures: []` (substrate 존재 + §188 PASS, oracle parity 만
   미정의). 이는 demiurge consumer 가 future 에 4개 record 의 신뢰도
   차등 평가할 수 있도록 첫 metadata bit.

## §6 SSOT pointer

- bridges (4):
  - `~/core/anima/anima-physics/tool/demiurge_aura_bridge.py` (192 LoC)
  - `~/core/anima/anima-physics/tool/demiurge_bio_bridge.py` (197 LoC)
  - `~/core/anima/anima-physics/tool/demiurge_chem_bridge.py` (199 LoC)
  - `~/core/anima/anima-physics/tool/demiurge_grid_bridge.py` (207 LoC)
- record drops (4, 동일 UTC stamp 2026-05-21T08-33-18Z):
  - `~/core/demiurge/exports/aura/verify/2026-05-21T08-33-18Z/anima_aura_20260521T083318Z.json` (1511 B)
  - `~/core/demiurge/exports/bio/verify/2026-05-21T08-33-18Z/anima_bio_20260521T083318Z.json` (1718 B)
  - `~/core/demiurge/exports/chem/verify/2026-05-21T08-33-18Z/anima_chem_20260521T083318Z.json` (1710 B)
  - `~/core/demiurge/exports/grid/verify/2026-05-21T08-33-18Z/anima_grid_20260521T083318Z.json` (1725 B)
- predecessor doc (6-step pattern 원본):
  - `~/core/anima/anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
- anima docs to be updated (별도 staging):
  - `~/core/anima/anima-physics/docs/demiurge_hw_verify_2026_05_21.md` §2.2 표 4행 + §2.3 aggregate 2줄 (diff §4 참조)
- SW sources:
  - bio: `~/core/anima/anima-physics/hippocampus/{theta_gamma,episodic_replay}.hexa` + `memristor/self_reference.hexa`
  - chem: `~/core/anima/anima-physics/engines/thermodynamic_consciousness.hexa` (+ `state/s188g_engines_2026_05_21/thermodynamic.run.log`)
  - grid: `~/core/anima/anima-physics/social/kuramoto_coupling.hexa` + `hw/kuramoto_neuromorphic/src/kuramoto_local_sim.py`
- demiurge consumer cycle pointer (4건 모두 별도): `~/core/demiurge/cockpit/.../ActionDispatch.swift` 의 `(.verify, "{bio,chem,grid}")` 케이스 신설 + `{Bio,Chem,Grid}VerifyProducer.swift` + schema decoder; aura 는 `(.verify, "aura")` 케이스 의 exports/aura/verify/ 직접 조회 추가 또는 sibling-repo dispatch 의 record-aware fallback.
