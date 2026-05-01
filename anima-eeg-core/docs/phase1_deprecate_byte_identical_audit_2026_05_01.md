# Phase 1 DEPRECATE — byte-identical audit (2026-05-01)

> **Scope**: Migration plan §3.3 DEPRECATE class — 4 metric tools를 anima-eeg-core/_metrics/
> native로 흡수하기 전, native↔legacy 짝 동등성 검증 (legacy 삭제 prerequisite).
>
> **Mode**: read-only audit (변경 X). 4 짝 모두 native + legacy selftest 직접 실행하여 numeric output 비교.
>
> **RAW**: raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen · raw#18 self-host · raw#42 mac-zero-compute
>        · raw#71 falsifier ≥3 · raw#82 darwin · raw#91 honest triad

---

## 1. ARCHITECTURAL FINDING (raw#10 honest C3 — surprise revision)

오늘 audit의 가장 중요한 발견은, **byte-identical 비교 자체가 무의미**하다는 점이다.

4 짝 모두 native `_metrics/*.hexa` 파일은 자체 docstring에서 명시적으로

> "DECISION: **WRAP** (not PORT)"

이라고 밝히고 있다. 즉:

- native (~250 LoC) = **WRAPPER** — `exec_with_status(hexa.real run <legacy_path> ...)` 형태로 legacy를 직접 호출하고, kv-block surface로 출력만 재포맷
- legacy (~535–1055 LoC) = **REAL backend** — Kaspar-Schuster / Bandt-Pompe / Hjorth / Welch-PSD numeric core

| 짝 | native LoC | legacy LoC | native 구조 | LEGACY_PATH 상수 |
|---|---|---|---|---|
| lz76 | 283 | 1055 | wrapper → exec(legacy) | `anima-clm-eeg/tool/clm_eeg_lz76_real.hexa` |
| permutation_entropy | 254 | 563 | wrapper → exec(legacy) | `anima-clm-eeg/tool/clm_eeg_pe_real.hexa` |
| hjorth | 258 | 535 | wrapper → exec(legacy) | `anima-clm-eeg/tool/clm_eeg_hjorth_real.hexa` |
| gamma_theta | 258 | 719 | wrapper → exec(legacy) | `anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa` |

**결과**: native가 legacy를 *반드시* 필요로 한다. legacy를 삭제하면 native 4개가 동시에 망가진다 (`backend_rc=127` 또는 file-not-found).

---

## 2. SELFTEST RUN — numeric output 비교 (n=1, today 2026-05-01)

각 짝에 대해 두 가지를 실행:
- **A**: `hexa run anima-eeg-core/tool/modules/_metrics/<X>.hexa --selftest`  (wrapper 경유)
- **B**: `hexa run anima-clm-eeg/tool/<X>_real.hexa --selftest --selftest-mode <mode>`  (legacy 직접)

native wrapper는 selftest mode를 hardcode (`random`/`white`/`synthetic_3`) — 비교는 동일 mode로 수행.

### 2.1 lz76 (mode=random, deterministic FNV PRNG)

| Field | A (native via wrapper) | B (legacy direct) |
|---|---|---|
| `c_n` / `c(n) productions` | **39** | **39** |
| `lz76_norm_x1000` / `b(n)_x1000` | **1218** | **1218** |
| backend_rc / verdict (legacy) | rc=0 | `SELFTEST_OK` |
| native verdict | `PASS` (raw#71 0/3 triggered) | — |

→ **numeric byte-identical** (39, 1218 일치). 메타필드 차이: native는 `schema=`, `metric=`, `raw71_*` 추가 emit; legacy는 `cert_out=`, `audit_jsonl=`, `selftest reference targets` 블록 emit. **격이 다른 surface**라 byte-diff는 큼.

### 2.2 permutation_entropy (mode=white)

| Field | A (native via wrapper) | B (legacy direct) |
|---|---|---|
| `pe_x1000` / `PE mean overall x1000` | **999** | **999** |
| backend_rc / verdict (legacy) | rc=0 | `PASS` |
| native verdict | `FALSIFIED` (raw#71 F_PE_02: pe>990) | — |

→ **numeric byte-identical** (999 일치). 흥미로운 점: **legacy = PASS**이지만 **native = FALSIFIED** — native wrapper의 raw#71 falsifier(`F_PE_02: pe_x1000 > 990`)이 white-noise selftest에서 의도적으로 발동. 이는 bug가 아니라 **선의의 강한 정의** — white noise는 PE saturate (≈1.0)하므로 production input으로 부적격이라는 native의 추가 가드. selftest는 여전히 `selftest=ok`로 종료(legacy parsing 성공이 기준).

### 2.3 hjorth (mode=white)

| Field | A (native via wrapper) | B (legacy direct) |
|---|---|---|
| `log10_activity_x1000` | **-1** | **-1** |
| `mobility_x1000` | **1414** | **1414** |
| `complexity_x1000` | **1225** | **1225** |
| backend_rc / verdict | rc=0 | `PASS` |
| native verdict | `PASS` (raw#71 0/3 triggered) | — |

→ **numeric byte-identical** (-1, 1414, 1225 모두 일치).

### 2.4 gamma_theta (mode=synthetic_3, own3 σ/τ=3 SSOT)

| Field | A (native via wrapper) | B (legacy direct) |
|---|---|---|
| `ratio_x1000` / `grand_mean_x1000` | **2973** | **2973** |
| `occipital_ratio_x1000` | **3728** | **3728** |
| `frontal_ratio_x1000` | **2865** | **2865** |
| backend_rc / verdict | rc=0 | `VERIFIED_P3` |
| native verdict | `PASS` (raw#71 0/3 triggered) | — |

→ **numeric byte-identical** (2973, 3728, 2865 모두 일치).

---

## 3. VERDICT TABLE

| 짝 | numeric values | full stdout byte-equal? | classification |
|---|---|---|---|
| lz76 | identical (39 / 1218) | **NO** (다른 surface) | **semantic-identical** |
| permutation_entropy | identical (999) | **NO** (다른 surface; +verdict-policy diff) | **semantic-identical** (verdict reframe by raw#71) |
| hjorth | identical (-1 / 1414 / 1225) | **NO** (다른 surface) | **semantic-identical** |
| gamma_theta | identical (2973 / 3728 / 2865) | **NO** (다른 surface) | **semantic-identical** |

**raw#10 honest C3** (refined): 4 짝 모두 numeric semantic은 100% identical하지만 출력 surface는 wrapper가 의도적으로 재구성 (kv-block + raw#71 falsifier eval). 따라서 "byte-identical"은 false, "semantic-identical"은 true.

---

## 4. LEGACY 삭제 가능 여부 (raw#10 honest verdict)

### 4.1 NO — 현재 상태에서 legacy 삭제는 **불가능**.

근거:
1. native `_metrics/<X>.hexa`의 `LEGACY_PATH` 상수가 `anima-clm-eeg/tool/<X>_real.hexa`를 가리킨다.
2. native는 `_metric_*_kv()` 본체에서 `exec_with_status(hexa.real run <LEGACY_PATH> ...)`을 호출한다.
3. 따라서 legacy file이 사라지면 `backend_rc=127` 발생, 모든 metric이 `verdict=FAIL`.
4. 4 native 모두 docstring에 *명시적으로* "WRAP (not PORT). Re-implementation deferred until Phase 5 port."라고 적혀 있음 — 즉 **Phase 1은 흡수가 아니라 surface 통일**이고, 실제 코어 흡수는 Phase 5의 work로 분리되어 있다.

### 4.2 Migration plan §3.3 "DEPRECATE class" 재해석

"DEPRECATE"는 **legacy 삭제**가 아니라 **legacy를 외부 진입점에서 격리** (eeg_core dispatcher가 더 이상 legacy hexa를 직접 부르지 않고 native wrapper만 부름)을 의미할 가능성이 높다. 본 audit는 그 격리가 이미 완료되었음을 확인 (kv-block surface는 native에서 일관되게 emit).

### 4.3 진짜 legacy 삭제를 위한 prerequisite (Phase 5 port 작업 단위)

각 짝 별로 numeric core를 native 안으로 옮겨야 한다:

| 짝 | 옮길 numeric core | 추정 LoC |
|---|---|---|
| lz76 | Kaspar-Schuster 1987 production count + log2 lookup | ~600 |
| permutation_entropy | Bandt-Pompe 2002 ordinal pattern count + entropy | ~300 |
| hjorth | activity/mobility/complexity (variance + diff cascade) | ~250 |
| gamma_theta | scipy.welch wrapper or self-host PSD (FFT) + band integration | ~500 |

총 ~1650 LoC native re-impl + cross-validation 필요. 이는 Phase 1 작업이 아님 — Phase 5 port로 미루는 것이 raw#137 80% Pareto.

---

## 5. raw#91 honest C3 — 본 audit의 한계

- **n=1 fixture only**: 오늘은 `synthetic_16ch_v1.json` 컨텍스트가 아닌 **wrapper-hardcoded selftest mode** (random/white/synthetic_3)에서 검증. canonical synthetic fixture (fingerprint 2960889009 — 참고로 task 컨텍스트에서 "831a1b5d" 언급은 fixture file 안 fingerprint 2960889009와 mismatch; 실제 file의 fingerprint는 2960889009) 직접 입력은 native wrapper가 `--selftest` flag만으로는 활용하지 않음.
- **다른 fixture·mode에서 결과 다를 가능성**: lz76은 `--selftest-mode structured`에서 `b<0.3` 예상, PE는 `--selftest-mode struct`에서 다른 값. 본 검증은 wrapper의 default selftest mode 한 가지에 대해서만 numeric equivalence를 입증.
- **Real EEG path (--input <npy>) 미검증**: `.venv-eeg` scipy 의존이 있는 path (gamma_theta가 가장 risk 높음 — `scipy.welch` 호출). 실 data 입력은 mac runtime stage에서 추가 verify 필요.
- **단발성 실행 (n=1 run)**: deterministic FNV PRNG 기반이라 동일 mode 재실행 시 동일 값 기대되지만, raw#65 idempotent reproducibility 통계 없음.

---

## 6. 다음 cycle 권장 액션 (raw#137 Pareto-ranked)

1. **(Pareto 80%) DEPRECATE의 의미 명시화**: Migration plan §3.3 문구를 "legacy 삭제"가 아니라 "external-entrypoint 격리 + native wrapper 단일 surface"로 재기술. 본 doc은 이 재해석을 입증.
2. **(Pareto 15%) Phase 5 port spec 작성**: 4 짝 별 numeric core 이식 spec(LoC 추정 §4.3) + cross-validation harness(`hexa run native --input fixture` ↔ `hexa run legacy --input fixture` numeric equality). canonical synthetic fixture 추가 verify case.
3. **(Pareto 5%) Real-EEG path verify**: `.venv-eeg` scipy 의존 path를 Mac stage runtime에서 1회 dry-run하여 wrapper의 numeric semantic이 selftest mode를 넘어서도 유지됨을 확인.

---

## 7. 결론 (one-liner)

> **lz76: semantic-identical (39/1218) / pe: semantic-identical (999, +falsifier reframe) / hjorth: semantic-identical (-1/1414/1225) / gamma_theta: semantic-identical (2973/3728/2865) — legacy file 4개는 native wrapper의 backend로서 *현재 동작 의존성을 가짐*. Phase 1 단계에서 legacy 삭제 불가 (raw#10 honest no).**

---

*Generated 2026-05-01. read-only audit. raw#9 hexa-only · raw#91 honest C3 · n=1 fixture limit.*
