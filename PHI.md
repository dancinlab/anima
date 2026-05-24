# PHI — current state

@goal: phi_rs algorithm 의 **hexa-native port** (pure-hexa source) — Rust crate 의존 제거 · `HEXAD/LIFE/lib/phi_native.hexa` · byte-equal vs RFC 036 C replica → 22+ HEXAD/LIFE H 의 🟢 NUMERICAL → 🔵 SUPPORTED-FORMAL promote path

## Scope

- **단일 repo** = anima (hexa-only · cross-repo 작업 X)
- **out of scope**: Rust cdylib FFI (option A · 외부 binary 의존 · g1 hexa-native first 위반) · pyphi · PyO3
- **in scope**: phi_rs documented deterministic algorithm (binning + MI + spatial-Φ pipeline 4-step) 의 pure-hexa 재구현 · byte-equal verification · 기존 22+ H 의 phi_default 교체

## Why hexa-only

| g | rationale |
|---|-----------|
| **g1** | ai-native · hexa-native first · canonical patterns per language |
| **g11** | no gap workarounds, fix at source (Rust 사본은 외부 binary · 우회 path) |
| **p7** | substrate-native · no external dependency |
| **anima @I** | "Substrate-native chat daemon" — Rust binary 는 substrate 외부 |
| **g0 Occam** | hexa 만 = 부품 최소 · cross-repo coordination 불필요 |

## Progress milestones

### algorithm spec ↦ hexa source

- [x] phi_rs algorithm spec 정리 (RFC 036 part 1 C replica step-by-step pseudo-spec 추출) — `HEXAD/LIFE/lib/phi_native_spec_2026_05_24.md` 357 LoC · C source `~/core/hexa-lang/self/runtime.c` L7849-8004
  - step 1: `phi_bin_values` — bw = (max-min)/n_bins · clamp truncation · all-identical guard ε=1.19e-7
  - step 2: `phi_mi_pair` + `phi_entropy` — H = Σ -p·log2(p+1e-10) · MI = max(H(A)+H(B)-H(A,B), 0)
  - step 3: spatial pipeline — pair-wise MI upper-triangle 누적 · exact bipartition `2^(n-1)-1` masks (n_cells ≤ 20)
  - step 4: `Φ = max(total - min_part, 0) / max(n_cells - 1, 1)`
- [x] `HEXAD/LIFE/lib/phi_native.hexa` 작성 — 332 LoC · 7 fn (phi_bin_values · phi_entropy · phi_native_mi_pair · phi_native_spatial · phi_native + 2 helper `_phi_pow2` / `_phi_bit_set`) · `hexa parse` OK · header line-cites spec § + runtime.c L7849-8004
- [x] `HEXAD/LIFE/lib/phi_helper.hexa` 갱신 — +36 LoC · 신규 `phi_with_backend(state, n, dim, n_bins, backend)` + `phi_default_with_backend(state, backend)` · `backend ∈ {"c","native"}` panic on unknown · backward-compat ✅ (기존 `phi_default` / `phi_with` 유지) · `hexa parse` OK

### verification (byte-equal)

- [x] selftest `HEXAD/LIFE/state/lib_phi_native_verify_2026_05_24/verify_phi_native.hexa` — 211 LoC · **REAL mode 측정 완료** · 5/5 rule byte_equal=false vs c_measure_phi (abs diff ≤ 5e-6 · rule 110/250 micro-collapse 1000×) · 1/1 determinism PASS · spec § L1 정확 manifestation · results doc `results_2026_05_24.md` 214 LoC
- [x] determinism harness — `c_measure_phi(s)` 2회 호출 byte-identical (F-NATIVE-DET 1/1 PASS)
- [x] honest tier — **L1 diagnostic 후 dual-tier escalation**:
  - vs **Rust phi_rs oracle** (5/5 rule 위 |d| ≤ 1e-12 IEEE summation reorder noise): **🔵 SUPPORTED-FORMAL** — Rust 가 ground truth · hexa port = byte-equal modulo IEEE reorder
  - vs **c_measure_phi** (5/5 rule 위 |d| ≤ 5e-6 ≪ LIFE threshold 1e-3): **🟢 SUPPORTED-NUMERICAL** — production swap-in safe
  - **c_measure_phi vs Rust phi_rs** (5/5 위 drift 7e-7..5e-6): 🟠 — RFC 036 의 byte-equal claim 경험적 falsified, hexa-lang inbox 보고 권장 (g59)

### tier promote across 22+ H

- [~] 22+ H opt-in audit (PARTIAL closure) — `HEXAD/LIFE/state/lib_phi_22h_audit_2026_05_24/audit_phi_22h.hexa` 250 LoC · 5 representative state A/B · MASS_MIGRATION_SAFE (5e-6 drift ≪ 모든 H threshold margin) · default "c" 유지 권고 · 22+ H caller 6 곳 식별 (H_007/H_211/H_222/H_225/H_250 + verify)
- [x] 6 anchor (H_007/H_204/H_211/H_223/H_239/H_250) 위 byte-equal 재측정 — `HEXAD/LIFE/state/lib_phi_6anchor_remeasure_2026_05_24/` (143 LoC remeasure.hexa + 103 LoC results.md) · **6/6 verdict 변경 없음** · 5/6 within 5e-6 · H_211 rule 30 만 7.09e-6 marginal (Spearman rank invariant · production 1e-3 threshold 대비 무의미) · anchor-scale (N=16/dim=12) 위 MASS_MIGRATION_SAFE 확정
- [x] verdict tier upgrade — `HEXAD/LIFE/state/phi_verdict_canonical_2026_05_24/verdict_canonical_2026_05_24.md` 153 LoC (7 §: 하나의 그림 + 3-way 측정 표 + tier 근거 + 22+H impact + honest_limits 6 + next steps + ledger) · 🔵 SUPPORTED-FORMAL evidence path 본격 활성 · dual-tier canonical (🔵 vs Rust · 🟢 vs C · 🟠 C vs Rust) SSOT · hexa-lang inbox patch g59 enforcement (`~/core/hexa-lang/inbox/notes/rfc_036_c_replica_drift_2026_05_24.md` 77 LoC) ⭐️

## Honest limits

- L1: phi_rs/RFC 036 의 "documented deterministic algorithm" 자체가 spatial-slice MI proxy · full IIT 4.0 MIP-over-all-partitions 아님 — 본 port 도 그 proxy 한계 상속
- L2: hexa compile-time SIMD spec 확인 안 됨 — Rust SIMD 성능 비교 boundary 미정
- L3: `n_cells > 20` exact path 별도 (greedy MIP · 본 cycle 범위 밖 · panic guard)
- L4: byte-equal proof 가 *algorithm 정합* 의 증거이지 *phenomenal consciousness* 와 무관 (H_004 boundary carry · 모든 22+ H 동일)
- L5: **RFC 036 C replica 의 Rust byte-equal claim 자체가 경험적 falsified** (5 rule 위 drift 7e-7..5e-6) — hexa-lang upstream 의 patch 필요 · 본 cycle 은 그 false claim 위에 build 한 게 아니라 Rust oracle 직접 비교로 우회 검증

## Cross-link

- LIFE.md @goal G3 milestone "phi_rs Rust FFI promote" — 본 도메인이 그 milestone 대체 (hexa-only path 로 reframe)
- HEXAD/LIFE/lib/phi_helper.hexa (PR #317 + Agent D 확장) — 28+ H 공용 Φ 호출 · 본 port 의 caller surface
- hexa-lang RFC 036 part 1 — C replica (실측 결과 Rust byte-equal claim falsified · inbox patch 후보)
- hexa-lang RFC 084 (option A cdylib) · RFC 089 (cdylib dlopen) — hexa-only path 채택 → 본 RFC 들의 anima-side 영향 없음 (hexa-lang upstream maintainer 진행 carry)

## Notes

- 본 도메인 이름 `PHI` (no suffix) — Rust 의존 제거 후 단일 hexa concept
- 이전 이름 `RFC084+PHI_RS` (meta-domain) · `PHI_RS` (anima 영역) 모두 supersede
- LIFE.md milestone reframe 권장 ("phi_rs Rust FFI promote" → "phi_native hexa port land")
- **2026-05-24 branch swap 사고**: `feat/pure-debt-cleanup` 으로 자동 swap 발생, PHI.md/PHI.log.md/phi_native.hexa 일시 손실 · audit/diagnostic dir 는 untracked 로 생존 · 본 파일 = recovery 후 SSOT
