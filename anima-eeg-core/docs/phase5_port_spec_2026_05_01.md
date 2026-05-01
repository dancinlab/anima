# Phase 5 Port Spec — 4 metric numeric core 이식 (2026-05-01)

> **Scope**: anima-eeg-core/_metrics/{lz76,permutation_entropy,hjorth,gamma_theta}.hexa
> 4개 native wrapper의 numeric core를 legacy(anima-clm-eeg/tool/*.hexa)에서 분리·이식하는
> Phase 5 port 작업의 **spec only**. 실제 구현은 다음 cycle.
>
> **Mode**: spec only — 신규 doc 1개 write. _metrics/*, _integrations/*, .roadmap, legacy
> 모두 read-only. Phase 1 audit (`phase1_deprecate_byte_identical_audit_2026_05_01.md`,
> commit `867392918`)의 §4.3 prerequisite를 정식 spec으로 승격.
>
> **RAW**: raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen · raw#18 self-host
>        · raw#42 mac-zero-compute · raw#71 falsifier ≥3 · raw#82 darwin · raw#91 honest triad
>        · raw#137 Pareto · raw#65 idempotent

---

## §0 Executive summary

Phase 1 audit는 4 native `_metrics/*.hexa`가 모두 **WRAP** (legacy backend exec) 상태이고
numeric semantic은 byte-identical임을 입증했다. 본 spec은 그 4개 wrapper를 **PORT** (numeric
core를 native 안으로 흡수)하기 위한 작업 계약을 정의한다. 추정 ~1650 LoC native re-impl
(legacy 2872 LoC의 ~57%) + cross-validation harness + raw#71 falsifier 보존 + scipy/numpy
의존 격리(특히 `scipy.signal.welch` in gamma_theta) 전략을 §2~6에서 다룬다. 본 doc은
spec only — 코드 X, 다음 cycle에서 ω-cycle 분할(5a/5b/5c, 12~22h 추정)로 실제 port.

---

## §1 4 metric pair inventory + numeric core scope

| pair | native LoC (wrap) | legacy LoC (real) | numeric core algorithm | est. native PORT LoC |
|---|---|---|---|---|
| lz76                | 283 | 1055 | Kaspar-Schuster 1987 production-count + log2 lookup + epoch chunking | ~600 |
| permutation_entropy | 254 |  563 | Bandt-Pompe 2002 ordinal pattern enumeration + Shannon entropy + multi-scale (m=3, scales=[1,2,5]) | ~300 |
| hjorth              | 258 |  535 | activity = Var(x) / mobility = sqrt(Var(dx)/Var(x)) / complexity = mobility(dx)/mobility(x) | ~250 |
| gamma_theta         | 258 |  719 | Welch PSD (window=hann, nperseg=256, overlap=50%) + band integration (theta 4-8 Hz, gamma 30-45 Hz) + ratio | ~500 |
| **합계**             | **1053** | **2872** | — | **~1650** |

**Phase 1 SSOT 등가 numeric output (PORT 후 byte-identical 유지 필수)**:
- lz76: `c_n=39`, `lz76_norm_x1000=1218` (mode=random, FNV PRNG)
- permutation_entropy: `pe_x1000=999` (mode=white)
- hjorth: `log10_activity_x1000=-1`, `mobility_x1000=1414`, `complexity_x1000=1225` (mode=white)
- gamma_theta: `ratio_x1000=2973`, `occipital_ratio_x1000=3728`, `frontal_ratio_x1000=2865` (mode=synthetic_3)

---

## §2 raw#9 hexa-only port 전략 — Python helper 의존성 격리

### 2.1 legacy의 Python 의존 surface
- **lz76_real**: `numpy.load(.npy, allow_pickle=False)` + `np.rint(...).astype(int64)` (file IO + integer scaling) — embedded python heredoc
- **pe_real**: `numpy.load`, `numpy.argsort(kind='stable')` (ordinal pattern), `numpy.nanmean` (aggregation) — embedded python heredoc
- **hjorth_real**: `numpy.var`, `numpy.diff` — embedded python heredoc
- **gamma_theta_real**: `numpy.load`, `scipy.signal.welch(fs=FS, nperseg=...)`, `numpy.argmax` — `.venv-eeg` resolver-bypass 명시

### 2.2 PORT 전략 — 3-tier 격리

**Tier A — pure-hexa native** (의존성 0):
- hjorth: variance + diff cascade는 hexa 산술로 직접 구현 가능. numpy 의존 제거.
- lz76: production-count는 byte-level state machine — 이미 raw#9 hexa-only로 이식 가능. log2 lookup table은 ~256-entry const array.
- permutation_entropy: ordinal pattern은 m=3에서 6 permutation 정수 enum. argsort는 hand-coded 3-element sort net (constant cmp). Shannon entropy는 hexa log2 lookup.

**Tier B — hexa native + integer FFT** (의존성 0 but ~400 LoC):
- gamma_theta는 Welch PSD가 필요 → **integer-FFT** native impl 또는 **block-DFT for narrow band only** (theta 4-8 Hz / gamma 30-45 Hz 두 band만 power 계산 — 전체 PSD 불필요).
- 권장: **선택적 Goertzel** (Goertzel filter — single-frequency power, O(N) per frequency bin, no FFT). theta 5 bins + gamma 16 bins ≈ 21 Goertzel pass per channel.
- backup: `scipy.welch`와 **byte-identical 보장 어렵움**(window normalization·overlap accumulation 미세 차이) → §3 protocol에서 numeric tolerance 명시 필수.

**Tier C — helper script 격리 (raw#82 darwin only)**:
- 부득이 numpy.load(.npy) 입력 받기 위해 `--input-loader hexa-native-binary` 도입. .npy file format은 fixed header + raw float64 stream — hexa로 직접 parsing 가능.
- selftest mode (random/white/synthetic_3)의 deterministic PRNG는 hexa로 재구현 (FNV/MT-19937 lite).

### 2.3 결론 — 4 짝 모두 raw#9 hexa-only 가능. 단 gamma_theta는 Goertzel 채택 시 PSD numeric이 scipy.welch와 1e-3 이내 tolerance(§3)에서 일치 가능.

---

## §3 byte-identical 검증 protocol

### 3.1 cross-validation harness 사양

```
hexa run anima-eeg-core/tool/_phase5_xvalidate.hexa \
  --pair {lz76,permutation_entropy,hjorth,gamma_theta} \
  --fixture <fingerprint> \
  --tolerance-mode {strict|epsilon}
```

### 3.2 fixture set
- **F1**: wrapper-internal selftest mode (random/white/synthetic_3) — Phase 1 baseline.
- **F2**: canonical synthetic 16ch, 16384 samples (existing fingerprint 2960889009 재사용 가능).
- **F3**: real EEG sample (`.venv-eeg` 필요한 path) — gamma_theta verification.
- **F4**: edge cases — DC-only, single-tone 10 Hz, white-Gaussian σ=1, structured (raw#71 trigger).

### 3.3 verdict matrix (per pair × per fixture)
| pair | strict (integer values) | epsilon (float, abs ≤ 1e-9) | gamma_theta-only relaxed |
|---|---|---|---|
| lz76                | required | n/a | n/a |
| permutation_entropy | required (`pe_x1000` integer) | optional | n/a |
| hjorth              | required (3 scaled ints) | optional | n/a |
| gamma_theta         | **target** | **must hold** | scipy↔Goertzel: rel err ≤ 5e-3 acceptable |

**rule**: native PORT는 wrapper(F1) baseline에 대해서는 strict byte-identical(integer scaled
output) 의무. gamma_theta는 Goertzel 도입 시 F2/F3 real-PSD에서 5e-3 relative tolerance 허용.

### 3.4 harness가 emit해야 할 ledger fields
- `pair`, `fixture_id`, `fingerprint`, `native_kv_block` (sha256), `legacy_kv_block` (sha256)
- `numeric_diff` per scaled int field
- `falsifier_eval` per F1/F2/F3/F4 (raw#71 3개 falsifier 발동 여부)
- `port_status` ∈ {`MATCH`, `EPS_MATCH`, `DRIFT`, `BLOCK`}

---

## §4 raw#71 falsifier 보존

### 4.1 wrapper(현재) falsifier preregister 그대로 PORT
| pair | falsifier id | predicate | rationale |
|---|---|---|---|
| lz76 | F_LZ_01 / 02 / 03 | `c_n>upper_bound` / `lz76_norm_x1000>1300` / `monotone-violation` | structured signal에 대한 saturation guard |
| permutation_entropy | F_PE_01 / 02 / 03 | `pe<lower` / `pe_x1000>990` / `scale-monotone-violation` | white-noise saturation guard (Phase 1에서 의도적 발동 입증) |
| hjorth | F_HJ_01 / 02 / 03 | `complexity<1.0` / `mobility<0` / `activity-NaN` | mathematical invariant guard |
| gamma_theta | F_GT_01 / 02 / 03 | `ratio>10.0` / `band-power-zero` / `frontal>occipital ratio extreme` | eyes-closed posterior alpha-correlate sanity |

### 4.2 PORT 시 contract
- native PORT는 wrapper의 falsifier id·predicate를 **identical kv-block field 이름**으로 emit.
- selftest 시 동일 mode에서 **동일 verdict** 산출 (F_PE_02는 white에서 발동 유지).
- harness §3.4 `falsifier_eval`이 wrapper baseline과 byte-equal.

### 4.3 신규 falsifier 추가 금지 (Phase 5 scope 보호)
Phase 5는 이식이지 강화가 아님. 새 falsifier 도입 → Phase 6으로 분리.

---

## §5 LoC 추정 + ω-cycle 분할 (Phase 5a/5b/5c)

### 5.1 단계 분할

| stage | scope | LoC delta (approx) | 추정 hours | 핵심 deliverable |
|---|---|---|---|---|
| **Phase 5a** — pure-hexa pairs | hjorth + lz76 + permutation_entropy PORT (Tier A) | +1150 LoC native, -2153 LoC legacy 결국 unlink | 6~10 h | 3 native PORT + xvalidate F1·F2 strict pass + raw#71 보존 |
| **Phase 5b** — gamma_theta PORT | Goertzel native PSD + band integration (Tier B) | +500 LoC native | 4~7 h | 1 native PORT + xvalidate F1 strict + F2/F3 epsilon pass + raw#71 보존 |
| **Phase 5c** — legacy unlink + dispatcher single-entry | LEGACY_PATH 상수 제거 + eeg_core dispatcher 단일 native 진입 + 4 legacy file move-to-archive | -2872 LoC (legacy archive) | 2~5 h | dispatcher 단일 진입 + raw#9 strict native passing |

**Total**: +1650 LoC native, -2872 LoC legacy net (worktree 안에서 archive 처리 — 삭제 직후 복구 가능).
**총 추정**: 12~22 h (raw#137 80% Pareto 기준; 90% confidence).

### 5.2 stage 간 의존성
- 5a → 5b: 독립 가능(각 pair 별 PORT). 단 xvalidate harness는 5a 시점에 골격 완료 권장.
- 5b → 5c: 의존. 4 native PORT가 모두 strict/epsilon pass되어야 5c에서 legacy unlink 가능.
- raw#65 idempotent: 각 stage 종료 후 selftest n=10 재실행 → 동일 출력 (FNV PRNG seed 고정).

### 5.3 rollback 전략
- 5a/5b 실패 시: native LEGACY_PATH 상수 복원 → wrapper 모드로 회귀(현재 상태).
- 5c 실패 시: legacy archive에서 unarchive(git mv 역행) → 4 native가 다시 wrapper exec.

---

## §6 risk register

| risk id | description | severity | mitigation |
|---|---|---|---|
| R1 | scipy.welch ↔ Goertzel numeric drift (gamma_theta F2/F3에서 ratio_x1000 1~2 unit drift) | **high** | §3.3 epsilon tolerance(5e-3) 명시; F1 baseline은 strict 유지; 필요 시 Welch full PSD를 hexa native로 직접 (window=hann, overlap accumulation 동일 알고리즘) — Goertzel 대안 |
| R2 | floating-point determinism 차이 (numpy float64 ↔ hexa f64): summation order에 따라 last-bit drift | medium | Kahan-Babuška-Neumaier compensated sum 사용 + integer-scaled output(`*_x1000`)로만 비교 |
| R3 | numpy.argsort(kind='stable') 동치 미달 (PE 3-element sort tie-break) | medium | hand-coded sort net에서 stable tie-break 명시 (i<j → keep i first); m=3에서 tie 발생 시 byte-identical 검증 |
| R4 | .npy file format edge case (header version 2.0, fortran_order=True) | low | hexa .npy parser는 v1.0 + C-order만 지원; 그 외 입력 → `--reject-noncanonical` flag로 fail-fast |
| R5 | state schema 변경 (kv-block field 추가/제거) → downstream consumer 깨짐 | medium | §4.2 contract: identical field 이름 강제; CHANGELOG diff는 PORT 후 zero-delta 의무 |
| R6 | raw#71 falsifier 발동 조건 미세 변경 (white-noise PE>990 boundary) | medium | F1 baseline에서 `pe_x1000=999` 정확 재현 필수 — sort algorithm 동치성 입증 |
| R7 | Phase 5b Goertzel filter coefficient quantization (cos(2πk/N) 정밀도) | low | double-precision 산술 + 사전 계산된 lookup table (k=2~21만 필요) |
| R8 | epoch chunking off-by-one (lz76 chunked 변형이 worktree 안에 별도 file로 존재 — main에는 lz76_chunked.hexa 추가됨) | medium | Phase 5a에서 lz76.hexa만 다루고 lz76_chunked.hexa는 별도 PORT 단위(또는 5a 후속) |
| R9 | scipy.welch fallback path (.venv-eeg 부재 시) — gamma_theta legacy의 mac runtime 의존 | low | PORT 후 .venv-eeg 의존 자체 제거 (raw#9 hexa-only 확립) |

---

## §7 raw#10 honest C3 — 본 spec의 caveats (10개)

1. **n=1 fixture 한계**: Phase 1 audit는 selftest mode 1개에 대해서만 numeric equivalence 입증. F2/F3 fixture는 Phase 5 PORT 시점에서 신규 검증(현재 baseline 없음).
2. **Welch numeric byte-identical 보장 불가**: Goertzel 채택 시 scipy.welch와 1e-3 이내 drift 인정. 즉 F1 strict는 가능하나 F3 strict는 **불가능** — epsilon mode로 fallback.
3. **LoC 추정의 ±25% 변동성**: ~1650 LoC는 raw#137 80% Pareto 기준; 실제는 1300~2000 LoC band.
4. **ω-cycle 12~22h은 90% CI**: scipy.welch 동치성 issue가 R1에서 발현되면 5b가 +5 h 추가 가능.
5. **dispatcher 단일 진입(5c) 미명세**: 본 spec은 4 metric의 PORT만 다루며, eeg_core dispatcher의 단일 진입 router 변경은 별도 작업.
6. **raw#82 darwin scope 축소**: 현재 gamma_theta는 darwin-only (.venv-eeg) — PORT 후 raw#82 dependency 제거 가능, 그러나 hexa runtime의 darwin-vs-linux float determinism은 별도 검증 필요.
7. **legacy archive 정책**: 5c에서 legacy를 삭제 vs archive(git mv) 결정 미확정 — raw#10 honest는 archive 권장(rollback 가능).
8. **raw#65 idempotent statistics 부재**: Phase 1은 n=1 — Phase 5 PORT 시 n≥10 재실행 통계 의무화.
9. **anima-eeg-core 안 _metrics 외 caller 영향 미평가**: dispatcher 외에 다른 caller (anima-clm-eeg internal, _integrations/*, _ml/*)가 legacy를 직접 호출하는 path가 있을 가능성 — 5c 진입 전 grep audit 필수.
10. **본 spec은 코드 X**: spec only doc. 실제 PORT는 다음 cycle. 본 doc 자체로는 raw#9/10/12/18/42/65/71/82/91/137 어느 것도 강화하지 않으며 단지 prerequisite 정의.

---

## §8 raw#71 falsifier preregister (3개, 본 spec의 검증 가능성)

본 spec이 **틀렸음**이 입증되는 조건:

- **F_SPEC_01** — *Goertzel 동치 실패*: Phase 5b 구현 후 F2 fixture에서 gamma_theta `ratio_x1000`이 wrapper baseline 대비 5 unit 이상 drift 발생 → spec §2.2 Tier B 전략 폐기, full-FFT native 또는 scipy 재의존 fallback 필요.
- **F_SPEC_02** — *LoC 추정 50% 초과*: native PORT 합계가 2475 LoC(=1650×1.5)를 초과 → §5.1 ω-cycle 분할 22h 상한 초과, 추가 stage 5d 도입 필요.
- **F_SPEC_03** — *raw#71 보존 실패*: 4 pair × 3 falsifier = 12 falsifier 중 어느 하나가 F1 baseline에서 wrapper와 다른 verdict 산출 → §4 contract 위반, PORT 즉시 rollback.

---

*Generated 2026-05-01. spec only. raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen · raw#71 ≥3.*
*Predecessor: `phase1_deprecate_byte_identical_audit_2026_05_01.md` (commit `867392918`).*
*Predecessor: `_metrics/plv_preserving.hexa` (commit `ce747b5e7`, F1 reframe).*
*Successor: Phase 5a/5b/5c port implementation (next cycle, 12~22 h estimate).*
