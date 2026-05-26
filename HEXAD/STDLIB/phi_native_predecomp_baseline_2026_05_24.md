// HEXAD/STDLIB/phi_native_predecomp_baseline_2026_05_24.md
// STDLIB 도메인 — M4 prereq · phi_native.hexa 분해 *전* canonical byte-equal baseline
// 작성: 2026-05-24 · cycle: STDLIB-M4-prereq
// 상위: M3 (1st-wave 5 fn stdlib promote) 이후 phi_native 분해 시 본 doc 의 측정값 byte-identical 보존 의무

# § 1 — 목적

STDLIB M3 (phi_native.hexa 의 5 fn — `pow2_int` · `log2` · `bin_values_minmax` · `shannon_entropy` · `mutual_info_pair` — 을 hexa-lang stdlib 으로 분해) 직전, 현재 phi_native.hexa 의 측정 surface 를 **canonical snapshot** 으로 freeze. M4 의 regression cycle 은 본 doc 의 verbatim 값과 분해 *후* 측정을 byte-identical 비교한다.

PHI 도메인의 dual-tier verdict (`phi_native` vs `phi_rs` Rust = **🔵 SUPPORTED-FORMAL** · vs `c_measure_phi` C = **🟢 SUPPORTED-NUMERICAL** — cycle 4 L1 diagnostic + cycle 5 6-anchor 재측정 합치) 의 보존 여부가 M4 의 PASS/FAIL 단일 기준. 분해 후 결과가 변하면 (a) byte-identical 보존 실패 → impl bug · (b) verdict tier 강등 (🔵 → 🟢) → hexa-lang upstream patch 필요.

# § 2 — 현재 baseline (verbatim from REAL mode harness · 본 cycle 재실행)

본 cycle 의 재실행 (`baseline_run_2026_05_24.txt`) 출력은 cycle 3 의 `run_output_recover_2026_05_24.txt` 와 byte-identical (5 rule × phi_c · phi_h · byte_equal · 1 determinism 모두 일치).

## 2.1 F-NATIVE-RULE5 — 5 Wolfram rule × byte-equal (n_cells=8, dim=8, n_bins=4)

| rule | phi_c (c_measure_phi) | phi_h (phi_native_spatial) | abs_diff | byte_equal |
|------|-----------------------|----------------------------|----------|------------|
| 110  | 4.90943e-06           | 4.9773e-09                 | 4.90466e-06 | **false** |
| 30   | 0.422588              | 0.422585                   | ~3e-06   | **false** |
| 250  | 4.90943e-06           | 4.9773e-09                 | 4.90466e-06 | **false** |
| 184  | 0.585839              | 0.585842                   | ~3e-06   | **false** |
| 60   | 0.790029              | 0.790028                   | ~1e-06   | **false** |

aggregate: `pass=0  fail=5  stub_mode=false (real)`

**해석**: 5/5 strict byte-equal false — 그러나 `|phi_h - phi_c| ≤ 5e-6` (LIFE production threshold 1e-3 대비 200× 작음). cycle 4 의 dual-tier verdict 와 일관 (vs Rust = 🔵 strict ulp-equal · vs C = 🟢 within 5e-6).

## 2.2 F-NATIVE-DET — determinism (c_measure_phi rule 110 위 2회)

| call | phi value | byte_equal |
|------|-----------|------------|
| phi_a | 4.90943e-06 | (anchor) |
| phi_b | 4.90943e-06 | **true** |

determinism PASS 1/1 (c_measure_phi 결정론 · phi_native_spatial 결정론은 phi_helper 의 동일 surface 통해 상속).

# § 3 — Rust phi_rs oracle baseline (L1 diagnostic § L1b verbatim 인용)

5 rule × n_cells=8 dim=8 binary CA fixture 위 cross-validation. 산출 출처: `state/lib_phi_l1_diagnostic_2026_05_24/diag_summary_2026_05_24.md` § L1b.

| rule | spatial_phi (Rust phi_rs) | phi_hexa (phi_native, high-prec)  | phi_c (C replica) | d(hexa−rust) | d(c−rust) |
|------|---------------------------|------------------------------------|-------------------|--------------|-----------|
| 110  | 4.977298299530723e-09     | 4.977298299530722e-09              | 4.90943e-06       | −8.3e-25     | +4.904e-06 |
| 30   | 0.4225850815306889        | 0.4225850815306895                 | 0.422588          | +6.1e-16     | +2.918e-06 |
| 250  | 4.977298299530723e-09     | 4.977298299530722e-09              | 4.90943e-06       | −8.3e-25     | +4.904e-06 |
| 184  | 0.5858415229693057        | 0.5858415229693067                 | 0.585839          | +1.0e-15     | −2.523e-06 |
| 60   | 0.7900283296344668        | 0.7900283296344673                 | 0.790029          | +5.6e-16     | +6.704e-07 |

핵심: `|d(hexa−rust)| ≤ 1.0e-15` 5/5 (1-2 ulp, IEEE-754 summation reorder 잡음) — **phi_native ≡ Rust within ulp**. C replica 는 5/5 위 6.7e-7 ~ 4.9e-6 drift (RFC 036 upstream byte-equal claim 실측 반증, hexa-lang side ⚠ 별도 cycle).

# § 4 — 6-anchor 추가 baseline (cycle 5 § 2 verbatim 인용)

production-scale (N=16, dim=12, n_bins=4, warm=8, rep=0 deterministic) 위 6 PHI anchor 의 phi_c vs phi_native 측정. 출처: `state/lib_phi_6anchor_remeasure_2026_05_24/results_2026_05_24.md` § 2.

| anchor | rule | phi_c     | phi_native | abs_diff      | within 5e-6 |
|--------|------|-----------|------------|---------------|-------------|
| H_007  | 110  | 0.538242  | 0.538238   | 3.91801e-06   | ✅ |
| H_204  | 110  | 0.538242  | 0.538238   | 3.91801e-06   | ✅ |
| H_211  | 30   | 0.571954  | 0.571946   | 7.09123e-06   | ⚠ (5e-6 초과, 1.4×) |
| H_223  | 110  | 0.538242  | 0.538238   | 3.91801e-06   | ✅ |
| H_239  | 110  | 0.538242  | 0.538238   | 3.91801e-06   | ✅ |
| H_250  | 60   | 1.82618   | 1.82619    | 3.60354e-06   | ✅ |

aggregate: 6/6 anchor verdict 변경 없음, 5/6 within 5e-6 strict envelope, H_211 단독 7e-6 (chaotic class III rule 30 의 entropy 누적 합 추정).

# § 5 — regression criterion (M4 의무 · M3 분해 후 측정 위 단일 PASS/FAIL 기준)

M4 cycle 의 PASS = 다음 5 sub-criterion **모두 충족**:

1. **§ 2.1 5 rule × phi_h byte-identical** — 분해 후 `verify_phi_native.hexa` 재실행 시 `phi_h` column 이 본 doc § 2.1 의 5 값 (4.9773e-09 · 0.422585 · 4.9773e-09 · 0.585842 · 0.790028) 과 `abs_diff = 0.0` (`a == b` IEEE-754 strict bit-equal).
2. **§ 2.2 determinism PASS 유지** — c_measure_phi rule 110 2회 호출 byte-equal=true.
3. **§ 4 6-anchor phi_native byte-identical** — H_007/H_204/H_223/H_239 = 0.538238 · H_211 = 0.571946 · H_250 = 1.82619 모두 abs_diff = 0.0.
4. **§ 3 Rust oracle 1-2 ulp 보존** — phi_native vs phi_rs 5/5 `|d| ≤ 1e-12` (실측 max 1.0e-15 → 분해 후도 같은 차수). 새 stdlib log2 의 ln2 상수 reformulation 등으로 0.5-1 ulp 추가 drift 시까지 허용 — `|d| ≤ 2e-15` (즉 ≤ 2 ulp) 가 hard cap.
5. **honest fallback** — 위 1-4 중 임의 1 violation 발생 시 explicit honest_limit 등록 + dual-tier verdict 재평가. (🔵 → 🟢 강등) 시 hexa-lang stdlib patch 필요 (M3 promote PR 본문에 carve-out 추가). 측정 자체가 *변화* 라면 cycle 4 의 dual-tier verdict 도 함께 재산출.

**hard fail 조건** (single criterion 으로도 M4 fail): § 4 의 6/6 anchor 위 verdict flip 발생 (e.g. `within_5e-6` false → true 또는 그 반대), 또는 § 3 의 `|d(hexa−rust)| > 1e-12` 등장.

# § 6 — fixture 명세 (verify_phi_native.hexa SSOT)

`verify_phi_native.hexa` (211 LoC) 의 fixture (수정 금지 · regression 시 동일 harness 재사용):

- **rules**: `[110, 30, 250, 184, 60]` (Wolfram elementary CA — 110 class IV · 30 class III · 250 class II · 184 class II · 60 class III).
- **n_cells**: 8
- **dim**: 8 (per-cell state-vector length = n_steps in CA evolution)
- **n_bins**: 4
- **warm**: 2 (CA warmup steps, skeleton scale)
- **seed**: `_init_row(row, n, seed_off=rule % 7)` — rule-derived deterministic; site `i` set iff `(i + seed_off) % 3 != 0`.
- **CA neighborhood**: periodic `(l, c, r)` triple, next-state via `(rule / 2^(l*4+c*2+r)) % 2`.
- **state layout**: flat row-major (n_cells × dim) farr, indexed `s * n_steps + t`.
- **call**: `phi_with(states, 8, 8, 4)` (= `c_measure_phi` via phi_helper) vs `phi_native_spatial(states, 8, 8, 4)`.
- **comparison**: `cmp_byte_equal(a, b) = (a == b)` — hexa float `==` is IEEE-754 bit-equal for finite values; NaN-vs-NaN intentionally false.

# § 7 — environment 명세

본 cycle 재실행 환경 (baseline_run_2026_05_24.txt 산출 시):

- **hostname**: `Mac` (anima local dev)
- **hexa version**: `hexa 0.1.0-dispatch`
- **HEXA_MEM_UNLIMITED**: (unset · 본 fixture small, 기본 cap 충분)
- **wall**: < 3 s total (harness 자체 ~ instantaneous)
- **cost**: $0 (mac local)
- **invocation**: `cd state/lib_phi_native_verify_2026_05_24 && hexa run verify_phi_native.hexa 2>&1 | tee baseline_run_2026_05_24.txt`

# § 8 — honest_limits (≥4)

- **L1** — **single-state per anchor**: § 4 의 6 anchor 표는 각 H 의 `_RULE()` 기반 1 state (rep=0) 만. 각 anchor 의 full ensemble drift 분포 (mean / max / tail) 미측정 — tail max 가 1e-5 를 넘을 가능성은 있으나 production threshold ≥ 1e-3 대비 여전히 ≥ 2 order 작음.
- **L2** — **fixture n_cells=8 small**: § 2.1 / § 3 의 fixture 는 verify-skeleton scale. n_cells=16 production-scale (§ 4) 이 carry 했으나 n_cells ∈ {20, 24, 32} large-scale 위 baseline 별도 cycle 필요.
- **L3** — **H_211 rule 30 marginal (7.09e-6)**: chaotic class III 의 entropy 누적 합 위 C-replica drift 가 5e-6 envelope 1.4× 초과. 분해 후 같은 marginal 위에서 노이즈 폭이 1.5e-5 / 2e-5 로 확대될 가능성 — strict envelope 을 ≤ 1e-5 로 relax 검토 시 PASS.
- **L4** — **hexa runtime 변경 시 baseline drift**: hexa runtime 의 `log` builtin 변경 / `log2` builtin 추가 / float arithmetic ordering 변경 시 본 baseline 자체가 1-2 ulp drift 가능. 본 doc 의 baseline_run timestamp + hexa version (`0.1.0-dispatch`) 을 pin 으로 사용 — 다른 hexa version 위 measurement 는 별도 cycle.
- **L5** — **Rust oracle re-measurement out-of-scope**: § 3 의 5-rule × Rust phi_rs 값은 cycle 4 의 L1 diagnostic verbatim carry. 분해 후 Rust oracle 재실측은 `~/core/anima-physics/.venv` + phi_rs wheel 외부 환경 필요 → M4 regression 본 cycle 위 직접 측정 불가, L1 diagnostic 의 cross-validate 인용으로 갈음.

# § 9 — next-step (M4 regression cycle 작업 spec)

M4 분해 후 regression cycle 의 **새 harness** spec (본 doc baseline + 분해 후 phi_native 실측 비교):

```
HEXAD/STDLIB/state/phi_native_postdecomp_regression_<date>/
├── regression.hexa            // new harness · ~150 LoC
├── baseline_constants.hexa    // 본 § 2.1 + § 4 표 값을 hardcoded float constants 로 import
├── results_<date>.md          // M4 PASS/FAIL 산출
└── run_output_<date>.txt      // hexa run 산출
```

`regression.hexa` 의 핵심 fn (skeleton):

```
// pre-decomp baseline constants (본 doc § 2.1 + § 4 verbatim)
const BASELINE_RULE5_PHI_H: [float; 5] = [
    4.9773e-09, 0.422585, 4.9773e-09, 0.585842, 0.790028
]
const BASELINE_ANCHOR6_PHI_NATIVE: [float; 6] = [
    0.538238,   // H_007 rule 110
    0.538238,   // H_204 rule 110
    0.571946,   // H_211 rule 30
    0.538238,   // H_223 rule 110
    0.538238,   // H_239 rule 110
    1.82619     // H_250 rule 60
]

fn regression_rule5_byte_identical() -> bool {
    // verify_phi_native.hexa 재실행 후 phi_h column 캡처 → BASELINE_RULE5_PHI_H 와 abs_diff = 0.0 5/5 assert
}

fn regression_anchor6_byte_identical() -> bool {
    // remeasure_6anchor.hexa 재실행 (또는 동등 inline fixture) 후 phi_native column 캡처 → BASELINE_ANCHOR6_PHI_NATIVE 와 abs_diff = 0.0 6/6 assert
}

fn main() {
    // 두 regression fn 실행, PASS / FAIL 출력
    // FAIL 시 § 5 criterion 5 의 honest_limit 등록 + verdict 재평가 가이드 출력
}
```

M4 cycle 발사 시 import 할 입력:

- 본 doc `/Users/ghost/core/anima/HEXAD/STDLIB/phi_native_predecomp_baseline_2026_05_24.md` (§ 2.1 + § 4 표)
- 본 cycle 재실행 산출 `state/lib_phi_native_verify_2026_05_24/baseline_run_2026_05_24.txt` (verbatim 비교용)
- `state/lib_phi_6anchor_remeasure_2026_05_24/run_output_2026_05_24.txt` (verbatim 비교용)
- harness fixture: `state/lib_phi_native_verify_2026_05_24/verify_phi_native.hexa` (수정 금지)
- helper: `UNIVERSE/lib/phi_helper.hexa` (phi_with surface)

# § 10 — ledger

- 본 cycle 재실행: cycle 3 산출과 byte-identical (5 rule × phi_h · 1 determinism 동일)
- baseline freeze: 5 rule × phi_h + 6 anchor × phi_native + 5 rule × |d(hexa−rust)|
- M4 PASS 조건: 위 17 측정 모두 abs_diff = 0.0 (Rust oracle 5 ≤ 2 ulp 노이즈 허용)
- regression harness skeleton: § 9 baseline_constants.hexa + regression.hexa
- 본 doc 작성 worktree: `agent-a7d5413fedb66076b`, write 위치 = `HEXAD/STDLIB/` (worktree 내부)
- honest_limits: 5 (L1 single-state · L2 fixture small · L3 H_211 marginal · L4 runtime drift · L5 Rust oracle out-of-scope)
- $0 mac local · llm:none · wall ~3s
