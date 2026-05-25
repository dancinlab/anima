# §188 v2 substrate matrix snapshot (2026-05-21)

> v1 (`HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`,
> landed in commit `f74d8a425`) 의 35 substrate / 21 PASS 에서 **+7 engines impl**
> 후 re-snapshot. ⚠ empty 7 stub 모두 ✅ PASS 로 승격 → 21 + 7 = **28 PASS**.
>
> 본 v2 는 v1 dir 을 **건드리지 않고** 새 dir 에 cycle 결과만 stamp. v1 의
> wave2_{analog,izhikevich,oscillator_laser,photonic,quantum,snn,thermodynamic}.log
> 0-byte stub 7개는 그대로 보존되며, v2 의 `<engine>.v2.log` 7개가 sibling
> evidence 로 추가됨.

## §1 v1 → v2 변화

| Category   |  v1 |  v2 | Δ  |
|------------|----:|----:|---:|
| ✅ PASS     |  21 |  28 | +7 |
| 🟡 partial |   2 |   2 |  0 |
| ❌ build err|   4 |   4 |  0 (cl 3-stub + memristor_consciousness carry — 별도 cycle) |
| ⚠ empty (stub) |   7 |   0 | -7 (`engines/` 7개 모두 impl + 5/5 PASS 검증) |
| ⚠ anomaly  |   1 |   1 |  0 (anima_spontaneous selftest carry) |
| **total**  |  35 |  35 |  0 |

핵심 변화: **⚠ empty 7 → 0**, **✅ PASS 21 → 28**. 다른 칸 변화 없음 (별도 cycle).

## §2 새 PASS 7 engines (§188g LANDED, anima-physics commit not-yet-staged)

`anima-physics/state/s188g_engines_2026_05_21/summary.json` 의 **35/35 falsifier
PASS** (7 engine × 5 falsifier) 를 v2 dir 에서 **재실행 stamp**. 모든 binary 는
v2 cycle 내 동일 결과 (re-run determinism 검증).

| Engine (src .hexa)                          | Falsifier suite | v1 stub | v2.v2.log         | Verdict |
|---------------------------------------------|-----------------|---------|-------------------|---------|
| `engines/analog_consciousness.hexa` (385 LoC) | F-ANALOG-1..5  | 0 B ⚠   | analog.v2.log     | ✅ 5/5  |
| `engines/izhikevich_consciousness.hexa` (307) | F-IZ-1..5      | 0 B ⚠   | izhikevich.v2.log | ✅ 5/5  |
| `engines/snn_consciousness.hexa` (349)        | F-SNN-1..5     | 0 B ⚠   | snn.v2.log        | ✅ 5/5  |
| `engines/oscillator_laser_engine.hexa` (331)  | F-OL-1..5      | 0 B ⚠   | oscillator_laser.v2.log | ✅ 5/5 |
| `engines/photonic_consciousness.hexa` (418)   | F-PH-1..5      | 0 B ⚠   | photonic.v2.log   | ✅ 5/5  |
| `engines/quantum_consciousness.hexa` (514)    | F-Q-1..5        | 0 B ⚠   | quantum.v2.log    | ✅ 5/5  |
| `engines/thermodynamic_consciousness.hexa` (416) | F-TH-1..5    | 0 B ⚠   | thermodynamic.v2.log | ✅ 5/5 |

**Aggregate**: 7 engines × 5 falsifier = **35/35 PASS** (wall ≤ 1.82 s per engine on Mac arm64, deterministic — matches §188g summary.json `engines_pass=7 falsifier_pass=35`).

## §3 잔여 결손 (carry from v1)

- **consciousness-loop/src/main, snn_main, main_longrun** (3 build-err) —
  `&var` prefix unary + AOT `record`/`var`/`*Type` mutation 미지원;
  `or`/`and` 키워드는 [PR fix/or-and-keyword-alias-2026-05-21] 적용 후 회복.
  본 cycle 변화 없음.
- **engines/memristor_consciousness** (1 build-err) — 1-line fix 가 일부
  cycle 에 LANDED 로 언급되었으나 본 v2 snapshot 에서는 build PASS 가
  아직 §188g summary 에 포함되지 않았음 (falsifier 미정의). **별도 cycle 권장**.
- **🟡 partial 2** — `anima_engines_osc`, `microtubule_fpga` carry.
- **⚠ anomaly 1** — `tool/anima_spontaneous selftest` (6/9 PASS 가능성, V-SPONT
  scale ladder 연결 sanity 별도 검증 필요).

## §4 binary 정책

- `bin/` 7 engine AOT artifact (각 ~425-442 KB, 총 ~3 MB) 는 본 dir 의
  로컬 `.gitignore` 로 차단. 재실행 evidence 는 `<engine>.v2.log` (텍스트)
  로만 commit.
- Re-build 절차: `anima-physics/engines/<engine>_consciousness.hexa` 를
  `HEXA_MAC_BUILD_OK=1` 환경에서 build → 본 `bin/` 으로 copy →
  `./bin/<engine>` 실행.

## §5 cross-link

- v1 SSOT: [`../spontaneous_substrate_parallel_s188_2026_05_21/FINDINGS.md`](../spontaneous_substrate_parallel_s188_2026_05_21/FINDINGS.md)
- §188g source: `/Users/ghost/core/anima/anima-physics/state/s188g_engines_2026_05_21/summary.json`
- HEXAD/PHYSICS/README.md §2 등급 표 갱신 — 별도 cycle (본 cycle 범위 외)
- anima-physics/PLAN.md §5.x cycle ledger — 별도 cycle

## §6 honest C3

1. **anima-physics/state/s188g_engines_2026_05_21/bin/ untracked** — §188g
   는 아직 commit 되지 않은 상태 (working tree 변경). 본 v2 cycle 은
   §188g 의 binary 를 *복사*하여 재실행했으며, §188g 측 commit 정책은
   별도 결정 (anima-physics 측 cycle).
2. **35 → 35 total 불변** — v2 는 v1 의 35 substrate row count 를 그대로
   유지. 새 substrate 추가가 아닌 **stub → impl** elevation 의 cycle.
3. **memristor_consciousness 1-line fix unverified** — 본 cycle 의 §188g
   summary.json 에는 memristor_consciousness 가 포함되지 않음 (7 engines
   only). "1-line fix LANDED" 주장은 별도 evidence 필요.
4. **Wall 합계 ~5 s** — 7 engine × 평균 0.7 s. AOT compiled, 매우 빠름.
   v1 의 0-byte stub 은 120s timeout 가능성 + silent pass 양쪽 모두였으나
   본 v2 는 명확히 PASS evidence (full falsifier output) 확보.
5. **v1 dir 보존** — 본 cycle 은 v1 의 `wave2_*.log` 0-byte stub 7개를
   replace 하지 않고 **sibling dir 에 v2 evidence 추가** 하는 방식. v1
   commit `f74d8a425` 의 historical snapshot 무결성 유지.
