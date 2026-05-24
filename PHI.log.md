# PHI — log

Append-only history sister of `PHI.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-24T21:00:00Z — cycle 5 · #9 verdict tier canonical promote LAND ⭐️

- [x] PHI canonical verdict SSOT: HEXAD/LIFE/state/phi_verdict_canonical_2026_05_24/verdict_canonical_2026_05_24.md (~153 LoC, 7 §: 하나의 그림 + 3-way 측정 표 + tier 근거 + 22+ H impact + honest_limits ≥6 + next steps + ledger)
- [x] hexa-lang upstream inbox: ~/core/hexa-lang/inbox/notes/rfc_036_c_replica_drift_2026_05_24.md (g59 enforcement · YAML frontmatter slug/kind/filed_from/filed_at/priority/status · ~77 LoC · 5 rule 측정 표 + drift origin 추정 + 4-step proposal + cross-link 9 row)
- [x] 🔵 SUPPORTED-FORMAL evidence path 본격 활성 — phi_native ↔ Rust phi_rs 5/5 |d| ≤ 1e-12
- [x] dual-tier reporting canonical — 🔵 vs Rust · 🟢 vs C · 🟠 C vs Rust
- [ ] LIFE.md milestone reframe ("phi_rs Rust FFI promote" → "PHI domain complete · dual-tier 🔵/🟢 evidence") — 별도 cycle
- [ ] runtime.c:7874-7915 line-level audit — hexa-lang maintainer 진행 carry

## 2026-05-24T20:30:00Z — cycle 4 · L1 diagnostic + 22+H audit LAND + SSOT recovery 🛸

### Agent E (L1 root cause diagnostic + Rust phi_rs cross-validate) ✅

- [x] `HEXAD/LIFE/state/lib_phi_l1_diagnostic_2026_05_24/diag_l1_binning.hexa` + `diag_summary_2026_05_24.md` + 2 run.txt
- [x] **L1a (step 1 binning)**: 0/40 cells diff vs C f32-cast sim — binary CA 위 step 1 split 없음. spec § L1 prediction "loose confirmed" (binary 입력은 분기 안 보임, 연속 입력 boundary stress 위는 미검증)
- [x] **L1b (Rust phi_rs oracle, wheel `anima/anima-physics/.venv`)**: 5 rule × 4 step 위
  - hexa phi_native vs Rust phi_rs: 5/5 |d| ≤ 1e-12 (IEEE summation reorder noise · byte-equal modulo reorder)
  - c_measure_phi vs Rust phi_rs: 0/5 within 1e-12 · drift 7e-7..5e-6 (relative 1e6× larger than hexa)
- [x] **drift origin**: step 2-4 (entropy/MI/partition) of `runtime.c:7874-7915` 의 stray f32-cast 의심 — step 1 binning 은 clean
- [x] **spec § L5 정확 적중**: "RFC 036 C replica 의 Rust byte-equal claim 상속 한계" 가 실제 결함 위치 — vague catch-all 이 아니라 진짜 분기점

### Agent F (22+ H opt-in A/B audit) ✅ PARTIAL

- [x] `HEXAD/LIFE/state/lib_phi_22h_audit_2026_05_24/audit_phi_22h.hexa` 250 LoC + `audit_2026_05_24.md` 한글 ~120 LoC + `result.json`
- [x] **22+ H caller 매핑** 6 곳 (40 grep matches across `HEXAD/LIFE/state/*/*.hexa`):
  - H_007: `run_ca_phi.hexa:120` — c_measure_phi
  - H_211: `run_h211.hexa:278,305` — c_measure_phi
  - H_222: `run_h222.hexa:192` — c_measure_phi
  - H_225: `run_h225.hexa:118` — c_measure_phi
  - H_250: `run_h250.hexa:165` — phi_with (phi_helper 첫 production)
  - verify: `verify_phi_helper.hexa:97` — phi_default
- [x] **5 representative state A/B 측정**: abs_diff = 0.0 모두 (Agent F 의 "native"=phi_spatial builtin = c_measure_phi identity-bind 해석)
- [x] **MASS_MIGRATION_SAFE 결론**: 5e-6 hypothetical drift envelope (Agent C 실측) 적용 시도 모든 5 state margin ≥ 0.000111 ≫ 5e-6 → verdict-risk 0/5
- [x] **default "c" 유지 권고** · "native" opt-in 은 audit/cross-check 전용

### Agent F vs Agent D phi_helper "native" dispatch 의 disconnect

- [!] Agent F worktree 의 "native" = `phi_spatial` builtin (= c_measure_phi byte-equal by construction) · Agent F honest L3 명시
- [!] Agent D main 의 "native" = `phi_native.phi_native_spatial` (pure-hexa, f64-faithful, 5e-6 vs C)
- [x] reconcile: Agent F audit verdict (MASS_MIGRATION_SAFE) 가 Agent D 의 실 native dispatch 에도 generalizes — 5e-6 ≪ 0.000111 margin
- [x] main 의 phi_helper.hexa = Agent D version 유지 · Agent F 의 phi_helper override 미반영

### branch swap chaos & SSOT recovery

- [!] **사고**: 백그라운드 agent 의 git operation 이 main repo 의 working tree 를 `feat/pure-debt-cleanup` 으로 swap — PHI.md / PHI.log.md / `lib/phi_native.hexa` 손실 (이 branch 에 미존재)
- [x] **생존**: untracked dir 들 `lib_phi_l1_diagnostic_2026_05_24/` · `lib_phi_22h_audit_2026_05_24/` · `lib_phi_native_verify_2026_05_24/` · `lib/phi_native_spec_2026_05_24.md` 보존 (untracked 는 branch swap 시 working tree 잔류)
- [x] **recovery**: PHI.md + PHI.log.md = Write 로 재작성 (memory 기반 full state) · `lib/phi_native.hexa` = Agent E 의 worktree `agent-a07653c5889f742f6/HEXAD/LIFE/lib/phi_native.hexa` 에서 copy 예정
- [ ] **branch 정상화**: main working tree 의 branch 가 원래 세션 branch `docs/lora-vp21m-wave-16-corpus-v12` 또는 새 PHI-dedicated branch 로 복귀 필요 (별도 cycle)
- [ ] **hexa-lang upstream inbox**: RFC 036 C replica 의 Rust byte-equal claim falsification (5 rule 위 drift 7e-7..5e-6, drift origin runtime.c:7874-7915 step 2-4 의심) → `hexa-lang/inbox/notes/rfc_036_c_replica_drift_2026_05_24.md` 신규 (g59)

## 2026-05-24T19:55:00Z — cycle 3 · #5+#6 STUB→REAL flip + tier verdict LAND (Agent C) 🟠 (→ 🔵 후속 escalation)

- [x] STUB→REAL flip 3 hunk (line 31-33 import 활성 · 40 `_USE_STUB()` → false · 152-155 phi_native_spatial 실호출)
- [x] 실측 5 rule × 4 step + 1 determinism · verbatim output in `results_2026_05_24.md` + `run_output_2026_05_24.txt`
- [x] **tier 판정 🟠 INSUFFICIENT/DEFERRED** vs c_measure_phi (cycle 3 시점) — 5/5 byte_equal=false (abs diff ≤ 5e-6) · rule 110/250 micro-collapse relative ~1000× · 1/1 determinism PASS
- [x] **spec § L1 CONFIRMED** — C f32-cast vs hexa f64 분기 manifestation rule 110/250 의 4.9e-06 → 4.9e-09 collapse 패턴
- [x] worktree → main promote · import path fix · main 재실행 byte-identical reproduce
- [x] **cycle 4 에서 🟠 → 🔵/🟢 dual-tier escalation 완료**: Rust phi_rs 가 ground truth · hexa = byte-equal modulo IEEE reorder · C replica 가 outlier

## 2026-05-24T19:35:00Z — cycle 3 · #3 phi_helper backend select LAND (Agent D)

- [x] `phi_helper.hexa` +36 LoC (worktree → main promote, parse OK 9 fn 총)
- [x] 신규 `phi_with_backend(state, n, dim, n_bins, backend)` + `phi_default_with_backend(state, backend)` · backend ∈ {"c","native"} · unknown → panic exit=1
- [x] backward-compat verified — `phi_default ≡ phi_default_with_backend(_, "c")` byte-equal · `phi_with ≡ phi_with_backend(_, "c")` byte-equal
- [x] native opt-in drift 1 micro 측정: |7.40584e-09| f64-ulp (spec § L1 carve-out 양상 일치)
- [x] caller 2 H 식별: `run_h250.hexa:165` · `verify_phi_helper.hexa:97` (zero-touch)
- [x] 22+ H migration (#7) — opt-in 추가, default 는 "c" 유지 권고 (Agent F audit 확정)

## 2026-05-24T19:20:00Z — cycle 2 · #2 phi_native.hexa + #4 verify harness LAND

- [x] `HEXAD/LIFE/lib/phi_native.hexa` 332 LoC · 7 fn (phi_bin_values · phi_entropy · phi_native_mi_pair · phi_native_spatial · phi_native wrapper · 2 helper)
- [x] `hexa parse HEXAD/LIFE/lib/phi_native.hexa` → OK (clean)
- [x] `HEXAD/LIFE/state/lib_phi_native_verify_2026_05_24/verify_phi_native.hexa` 211 LoC · STUB mode 6/6 vacuous PASS (5 rule × byte_equal + 1 determinism)
- [x] caller surface 정확 — `phi_with(state, n, dim, n_bins)` + `phi_default(state)` 둘 다 phi_helper.hexa SSOT
- [x] Agent A worktree isolation bypass 관측 (main 에 untracked 로 직접 land) — file 자체는 spec-true (header line-cited)
- 🔥 **byte-equal 반전 발견** — phi_native(3-cell dim=8) vs **phi_rs Rust oracle** = diff **0.0** (byte-equal) · vs c_measure_phi (C replica) = |8.17e-7| · spec § L1 (C f32-cast 가 hexa 에 부재) 정확 예측 — hexa port 가 C 보다 Rust 에 더 가까움. cycle 4 의 L1 diagnostic 으로 5 rule 위 generalize 완료.
- [x] Agent B worktree → main 으로 promote (verify dir 2 file 복사 · 양쪽 parse OK)

## 2026-05-24T19:00:00Z — cycle 1 · #1 spec 추출 LAND

- [x] RFC 036 C replica 4-step pseudo-spec 추출 → `HEXAD/LIFE/lib/phi_native_spec_2026_05_24.md` (357 LoC)
- [x] C source 위치 확정: `~/core/hexa-lang/self/runtime.c` L7849-8004 (5 fn)
- [x] Rust 원본 위치 확정: `anima/phi-rs/src/lib.rs` L22-253
- [x] 4 step 핵심 수식 line-cited (bin/MI/spatial/scalar)
- [x] hexa primitive mapping 18 row · 없는 4 op 우회 path 명시
- [x] honest_limits 6
- [x] phi_native.hexa LoC 추정: ~205 pure-hexa (4 fn)

## 2026-05-24T18:30:00Z — hexa-only pivot · 도메인 rename PHI_RS → PHI

- [x] domain rename: `PHI_RS` → `PHI` (Rust suffix `_rs` 제거, hexa-only 정합)
- [x] scope reframe: Rust cdylib FFI (option A) DROP · hexa-native pure-hexa port (option B) 채택
- [x] @goal reframe: phi_rs algorithm 의 hexa-native port (HEXAD/LIFE/lib/phi_native.hexa) · byte-equal vs RFC 036 C replica
- [x] cross-repo coordination 제거 (anima 단일 repo · hexa-lang upstream RFC 084/089 carry only)

## 2026-05-24T18:00:00Z — meta-domain 생성 (superseded)

- [x] anima session 산하 `+` meta-domain scaffold (cross-repo joint tracking: anima/phi-rs + hexa-lang/RFC084)
- [SUPERSEDED] 본 entry 다음 hexa-only pivot 이 scope 폐기 · Rust cdylib path 드롭
