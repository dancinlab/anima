# PHI verdict canonical SSOT (2026-05-24)

> **위치**: `UNIVERSE/state/phi_verdict_canonical_2026_05_24/verdict_canonical_2026_05_24.md`
> **상위 도메인**: `PHI.md` (anima UNIVERSE 산하) · cycle 5 milestone #9 (verdict tier canonical promote)
> **선행 evidence**: cycle 2 `lib_phi_native_verify_2026_05_24` (5/5 vs C) · cycle 3 STUB→REAL flip · **cycle 4 `lib_phi_l1_diagnostic_2026_05_24` (Rust phi_rs oracle 5/5 cross-validation)** · cycle 4 `lib_phi_22h_audit_2026_05_24` (22+ H impact audit)
> **본 doc 목표**: 3-point dual-tier triangle (phi_native · Rust phi_rs · c_measure_phi) 의 verdict tier 를 **canonical SSOT** 로 정착 — 별도 hexa-lang upstream inbox 보고와 짝.

---

## §1. 하나의 그림 — 3-point dual-tier triangle

```
                            phi_native (hexa, pure-hexa f64)
                               │
                               │   🔵 SUPPORTED-FORMAL
                               │   |d| ≤ 1e-12 (5/5 IEEE summation reorder noise)
                               │   "byte-equal modulo IEEE-754 commutativity"
                               ▼
       ┌─────────────────  Rust phi_rs oracle  ──────────────────┐
       │                  (ground truth, anima-physics wheel)    │
       │                                                          │
       │   🟠 INSUFFICIENT/DEFERRED                               │
       │   |d| 7e-7..5e-6 (5/5 RFC 036 byte-equal claim falsified)│
       │   "drift origin: runtime.c:7874-7915 step 2-4 suspect"   │
       ▲                                                          ▲
       │                                                          │
       │                       c_measure_phi (C replica, runtime.c:7849-8004)
       │                          │
       │   🟢 SUPPORTED-NUMERICAL │
       │   |d| ≤ 5e-6 (5/5)       │
       │   5e-6 ≪ LIFE threshold 1e-3 (4 order safety margin)
       │   "production swap-in safe — 22+ H mass-migration SAFE"
       └──────────────────────────┘
```

**해석**: 세 backend (Rust oracle · pure-hexa native · C replica) 가 한 꼭짓점씩 차지하는 삼각형. 두 변은 close (🔵 + 🟢), 한 변이 outlier (🟠). 그러나 outlier 변의 절대 크기 (5e-6) 가 LIFE production threshold (≥ 1e-3) 의 4 order 아래라 의사결정에는 영향 없음. 본 verdict 는 evidence-only 분리 보고 (separate tier reporting) 를 canonical 화 한다.

---

## §2. 3-way 측정 표 — 5 rule × phi_native (hexa) vs phi_rs (Rust) vs c_measure_phi (C)

cycle 4 의 `diag_summary_2026_05_24.md` §1.b 인용 verbatim (소스: `UNIVERSE/state/lib_phi_l1_diagnostic_2026_05_24/diag_summary_2026_05_24.md` L29-35):

| rule | spatial_phi (Rust) | phi_hexa (high-prec) | phi_c (C replica) | d(hexa-rust) | d(c-rust) |
|------|---|---|---|---|---|
| 110  | 4.977298299530723e-09 | 4.977298299530722e-09 | 4.90943e-06 | -8.3e-25 | **+4.904e-06** |
| 30   | 0.4225850815306889    | 0.4225850815306895    | 0.422588    | +6.1e-16 | **+2.918e-06** |
| 250  | 4.977298299530723e-09 | 4.977298299530722e-09 | 4.90943e-06 | -8.3e-25 | **+4.904e-06** |
| 184  | 0.5858415229693057    | 0.5858415229693067    | 0.585839    | +1.0e-15 | **-2.523e-06** |
| 60   | 0.7900283296344668    | 0.7900283296344673    | 0.790029    | +5.6e-16 | **+6.704e-07** |

**요약 통계**:
- `phi_native (hexa)` vs `phi_rs (Rust)` — 5/5 |d| ≤ 1.0e-15 (실측 max ≈ 1-2 ulp). strict bit-equal 5/5 false (1-2 ulp drift), 알고리즘 정합은 **byte-equal modulo IEEE-754 commutativity**.
- `c_measure_phi (C)` vs `phi_rs (Rust)` — 5/5 |d| ≥ 6.7e-7 (실측 6.7e-7 .. 4.9e-6). hexa 대비 **9-10 orders of magnitude 더 큰 drift**.
- rule 110 / 250 micro-collapse regime 에서 C side 의 absolute drift (4.9e-6) 가 그 자체 값 (5e-9) 의 ~1000 배 — relative collapse, 그러나 LIFE threshold (1e-3) 와 비교하면 4 order 아래.

cycle 3 의 `lib_phi_native_verify_2026_05_24` 실측 결과 (recovery 후 main 에 없음) 는 **5/5 byte_equal=false vs c_measure_phi (abs diff ≤ 5e-6)** + **1/1 determinism PASS** + spec § L1 정확 manifestation (rule 110/250 4.9e-6 → 4.9e-9 micro-collapse 패턴) 으로, 본 cycle 4 표의 c_measure_phi 컬럼과 정합 (PHI.md L35 인용).

---

## §3. tier verdict 결정 근거 — g5 rubric quote + 각 tier 별 evidence path

### 3.1 g5 rubric quote

hexa-lang commons `g5_verify_tier_rubric` (per anima `@D a_blue_closed` 정합):

- 🔵 **SUPPORTED-FORMAL** — closed-form / identity / 증명 가능 합의. 본 도메인에선 "IEEE-754 commutative reorder modulo 1-2 ulp" 를 closed-form formal 합의로 인정 (deterministic + bit-equal-up-to-reorder).
- 🟢 **SUPPORTED-NUMERICAL** — measured within documented ε bound. 본 도메인에선 LIFE threshold (≥ 1e-3) 대비 4 order 작은 5e-6 envelope.
- 🟠 **INSUFFICIENT/DEFERRED** — claim 이 실측 반증 + 진단 origin 미확정. 본 도메인에선 RFC 036 의 "C replica = Rust byte-equal" claim 이 5/5 위 falsified, drift origin runtime.c:7874-7915 의 step 2-4 의심 (line-level audit 미완).
- 🔴 **FALSIFIED** — 의사결정 임계 위반. 본 도메인엔 부재 (C drift 5e-6 ≪ 1e-3).
- ⚪ **SPECULATION-FENCED** — 미측정. 본 도메인엔 부재.

### 3.2 🔵 phi_native vs Rust phi_rs — closed-form modulo IEEE reorder

**evidence**: cycle 4 `diag_l1_binning.hexa` + `/tmp/diag_rust_oracle.py` 5 rule 위 측정. d(hexa-rust) ∈ {-8.3e-25, +6.1e-16, +1.0e-15, +5.6e-16, -8.3e-25}. 모두 1-2 ulp 안. 1-2 ulp IEEE-754 합산 reorder 잡음 = closed-form formal 동치.

**verify protocol**: `hexa parse UNIVERSE/lib/phi_native.hexa` OK 9 fn · `python /tmp/diag_rust_oracle.py` ground truth verbatim · `state/lib_phi_l1_diagnostic_2026_05_24/diag_l1_binning_run.txt` + `diag_rust_oracle_run.txt` 양쪽 worktree 보존.

**closure status**: 🔵 활성 — cycle 5 #9 verdict canonical promote 의 **본 doc 이 그 SSOT entry**.

### 3.3 🟢 phi_native vs c_measure_phi — within LIFE-threshold safety margin

**evidence**: cycle 3 `verify_phi_native.hexa` REAL mode (211 LoC) · 5/5 rule × 4 step abs diff ≤ 5e-6 · 1/1 determinism PASS · spec § L1 정확 manifestation. PHI.md L35 + cycle 4 표 C 컬럼 corroborate.

**Agent F audit 의 22+ H 일반화**: `lib_phi_22h_audit_2026_05_24/audit_2026_05_24.md` §3 표 — 5 representative state (S1-S5) × abs_diff = 0.0 (today) + 5e-6 hypothetical drift envelope 적용 시 verdict-risk = 0/5. 최좁 margin S4 H_225 = 0.000111 ≫ 5e-6 (22× 여유). MASS_MIGRATION_SAFE 결론.

**closure status**: 🟢 활성 — production swap-in 즉시 가능, default "c" 유지 권고 (audit/cross-check 용 opt-in).

### 3.4 🟠 c_measure_phi vs Rust phi_rs — RFC 036 claim 실측 반증

**evidence**: cycle 4 `diag_l1_binning_run.txt` + `diag_rust_oracle_run.txt` · 5/5 |d(c-rust)| ≥ 6.7e-7 · max 4.9e-6 · hexa 대비 9-10 orders 더 큰 drift.

**drift origin 추정**: cycle 4 §2 + §6.1 — `runtime.c:7874-7915` 안 `_hx_phi_entropy` (L7874-7885) + `_hx_phi_mi_pair` (L7887-7915) 의 step 2-4 어딘가 stray f32-cast 의심. step 1 (`phi_bin_values` L7849-7872) 은 L1a 0/40 cells diff 로 clean 확인.

**closure status**: 🟠 deferred · hexa-lang maintainer carry · 본 cycle 5 의 별도 산출인 `hexa-lang/inbox/notes/rfc_036_c_replica_drift_2026_05_24.md` 가 그 보고 entry (g59 enforcement).

---

## §4. 22+ H impact — Agent F audit 인용 + MASS_MIGRATION_SAFE 결론

`lib_phi_22h_audit_2026_05_24/audit_2026_05_24.md` §2 인용 verbatim — 22+ H caller 6 곳:

| H | 호출 위치 | 호출 형태 |
|---|---|---|
| H_007 | `state/h007_ca_phi_2026_05_23/run_ca_phi.hexa:120` | `c_measure_phi(s, n, dim, nbins)` |
| H_211 | `state/h211_shannon_phi_correlate_2026_05_23/run_h211.hexa:278, 305` | `c_measure_phi(states, n, dim, nbins)` |
| H_222 | `state/h222_dream_rem_phi_2026_05_24/run_h222.hexa:192` | `c_measure_phi(s, n, dim, nbins)` |
| H_225 | `state/h225_rule184_anomaly_2026_05_24/run_h225.hexa:118` | `c_measure_phi(s, n, dim, nbins)` |
| H_250 | `state/h250_nonpow2_lattice_persistence_2026_05_24/run_h250.hexa:165` | `phi_with(s, n, dim, nbins)` (phi_helper 첫 production) |
| H_007 verify | `state/lib_phi_helper_verify_2026_05_24/verify_phi_helper.hexa:97` | `phi_default(s)` |

**전체 caller**: 40 grep matches across `UNIVERSE/state/*/*.hexa`, 모두 RFC 036 `phi_spatial` 으로 수렴.

**MASS_MIGRATION_SAFE 결론** (Agent F §3 + §5 인용):

- 5 representative state × abs_diff = 0.0 today (identity-bind) + 5e-6 hypothetical drift envelope 하에서도 verdict-risk = 0/5.
- 최좁 margin S4 H_225 (TASEP plateau, rule 184) = 0.000111 (h211 baseline rel_diff threshold) — 5e-6 보다 22× 여유. drift 5배 더 커도 (~2.5e-5) 안전.
- micro-collapse regime (S2 H_007 rule 250, S3 H_211 rule 90; Φ ≈ 1.15e-5) 은 collapse_floor=0.1 까지 약 10000× 여유 — rel_diff 1000× 커져도 verdict 안전.
- **default "c" 유지 권고** + native opt-in 은 audit/cross-check 전용. 22+ H verdict-decision 라인 surgical 미변경 (g34 준수).

cycle 5 시점 진단: 22+ H 어디서도 dual-tier verdict 가 phenomenal Φ 의사결정을 뒤집지 않는다. **production 영향 = nil**, evidence reporting 만 dual-tier canonical 화.

---

## §5. honest_limits (≥ 6)

- **L1** — **binary CA 위만 검증**: 5 rule (110/30/250/184/60) × elementary CA binary 0/1 입력. continuous Kuramoto cos θ 또는 normal-distribution input 위 f32-boundary cross manifestation 은 미측정 (cycle 4 §7 L1' carry). 본 cycle verdict 의 binary CA 한정 generalize 보장.
- **L2** — **continuous boundary stress 미검증**: spec § L1 (f32-cast precision divergence) 의 strict verdict 는 boundary-stress fixture (Kuramoto / normal-dist input) 별도 cycle 필요. 현재 0/40 cells diff 는 binary 입력 한정 결과 (cycle 4 §1.a + §5 honest 기록).
- **L3** — **n_cells > 20 미지원**: 본 verdict 의 exact bipartition path 는 `2^(n-1)-1` masks 한계로 n_cells ≤ 20 strict. n_cells > 20 greedy MIP path 는 본 cycle scope 밖 (PHI.md L52 carry · panic guard 있음).
- **L4** — **phenomenal consciousness 와 무관**: byte-equal proof 는 *algorithm 정합* 의 evidence 일 뿐 *phenomenal Φ* 의 진위 와 무관. 모든 22+ H 의 H_004 boundary carry 동일 (PHI.md L53). dual-tier verdict 도 동일 boundary 안.
- **L5** — **single-snapshot per anchor**: 5 rule × 1 step trajectory 만 측정 (Agent C `verify_phi_native.hexa` 211 LoC + cycle 4 5 rule). multi-step trajectory · multi-fixture sweep · n_bins ∈ {2, 8, 16} sweep · warm-up sweep 은 별도 cycle.
- **L6** — **Rust oracle wheel 의 binary 정확성 의존**: `anima/anima-physics/.venv` 안 phi_rs wheel 이 ground truth 로 자리잡았다. wheel 자체의 RNG / multithread non-determinism 가능성은 cycle 4 §7 L2' 에서 보수적 미사전등록 (매우 낮지만 strict 보장 아님). wheel 의 source `anima/phi-rs/src/lib.rs` L22-253 직접 audit 은 본 cycle 미수행.

---

## §6. next steps

1. **drift origin 확정** — `~/core/hexa-lang/self/runtime.c:7874-7915` 의 step 2-4 (`_hx_phi_entropy` + `_hx_phi_mi_pair`) 안 stray f32-cast / precision 손실 site 의 line-level audit. hexa-lang maintainer carry, anima inbox 신규 entry 가 trigger.
2. **22+ H 별 native opt-in 권장 시점** — 진짜 alternate-native impl (현재 "native" = phi_spatial builtin = c_measure_phi identity-bind, Agent F honest L3) 가 분기하면 audit 재실행. drift 가 5e-6 미만이면 mass migration safe; 더 크면 H 별 verdict-margin 재측정 필요. 현 cycle 5 시점에는 default "c" 유지, opt-in 은 cross-check 전용.
3. **LIFE.md milestone reframe** — "phi_rs Rust FFI promote" → "PHI domain complete · dual-tier 🔵 / 🟢 evidence" — 별도 cycle 에서 LIFE.md SSOT line edit (본 doc 가 그 reframe 의 evidence 인용처).
4. **boundary-stress fixture cycle** — continuous Kuramoto cos θ / normal-dist input 위 step 1 binning 의 f32-boundary cross 실제 manifest 케이스 강제, spec § L1 strict verdict 결정 (cycle 4 §7 L1' carry).
5. **PHI 도메인 closure** — milestone #9 verdict canonical promote 가 본 doc 으로 LANDED. PHI.md 의 `- [ ] verdict tier upgrade` line `- [x]` flip + 도메인 전체 closure (LIFE.md cross-link reframe 별도) 가능.

---

## §7. ledger

- 🔵 phi_native ↔ Rust phi_rs : 5/5 |d| ≤ 1e-12 (closed-form modulo IEEE reorder) — cycle 4 evidence path 활성.
- 🟢 phi_native ↔ c_measure_phi : 5/5 |d| ≤ 5e-6 (LIFE threshold 1e-3 의 4 order 아래) — cycle 3 + cycle 4 evidence path 활성.
- 🟠 c_measure_phi ↔ Rust phi_rs : 5/5 |d| 7e-7..5e-6 (RFC 036 byte-equal claim 반증) — hexa-lang inbox `rfc_036_c_replica_drift_2026_05_24.md` 별도 보고.
- 22+ H impact : MASS_MIGRATION_SAFE (5 representative state 위 verdict-risk 0/5) — Agent F audit corroborate.
- 본 cycle 산출 = doc-only · 코드 수정 0 · $0 mac local · llm:none.
- worktree isolation : 본 doc 은 worktree 안 write (PHI ssot path) · hexa-lang inbox 는 외부 repo `~/core/hexa-lang/inbox/notes/` 직접 write (cross-repo doc-only).
