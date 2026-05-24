# STDLIB — log

Append-only history sister of `STDLIB.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-24T23:30:00Z — cycle 3 (ship) · hexa-lang PR #712 LAND ⭐️

- [x] hexa-lang PR #712: https://github.com/dancinlab/hexa-lang/pull/712 (review-only · g54)
- [x] commit f6562227 · branch `feat/anima-stdlib-handoff-2026-05-24` off origin/main
- [x] 2 file +171 LoC: `inbox/notes/rfc_036_c_replica_drift_2026_05_24.md` (65 LoC) + `inbox/rfc_drafts_2026_05_24/stdlib_scaffold.md` (106 LoC)
- [x] cred scan PASS (g28) · auto-merge 금지 준수
- [x] cross-repo handoff loop 완성 — anima PHI domain 발견 → hexa-lang upstream 알림
- [ ] maintainer 승인 → M3 (impl phase 1 · 5 module 병렬 land)
- [ ] anima ship PR (Agent A 진행 중) — anima 측 PHI + STDLIB 산출물 main commit

## 2026-05-24T23:00:00Z — cycle 2 (2/2) · M2 design RFC LAND ⭐️

- [x] hexa-lang inbox RFC draft: `~/core/hexa-lang/inbox/rfc_drafts_2026_05_24/stdlib_scaffold.md` 132 LoC · 10 § · YAML frontmatter
- [x] 5 module fn signature: `math/log::log2` · `math/bitops::{pow2_int,bit_set}` · `info/entropy::shannon_entropy` · `info/binning::bin_values_minmax` · `info/mutual_info::mutual_info_pair`
- [x] 의존 그래프 ASCII (§ 4): 순환 0 · breadth 2 (math/bitops ⊥ math/log 병렬 land 가능) · 1st-wave leaf = info/mutual_info
- [x] `iit_ei.hexa::LN2_INV = 1.4426950408889634` 재활용 (log2 implementation)
- [x] g59 enforcement (relates_to: rfc_036_c_replica_drift_2026_05_24 + RFC 036) — RFC 036 byte-equal claim falsification 의 hexa-side fix path 연결
- [x] honest_limits 6 (L1 naming · L2 farr/array dual · L3 cross-repo 순서 · L4 log2 builtin 승격 · L5 maintainer 승인 · L6 LN2_INV 재배치)
- [!] **bottleneck**: hexa-lang maintainer 승인 대기 — M3 (impl) 는 cross-repo · anima 단독 land 불가
- [ ] M3 (impl) — 승인 후 5 module 병렬 stacked PR (hexa-lang 측 fan-out)
- [ ] M4 (verify) — hexa-lang M3 land 후 anima 측 regression harness (baseline 이미 freeze)

## 2026-05-24T22:45:00Z — cycle 2 (1/2) · M4 prereq baseline LAND

- [x] `HEXAD/STDLIB/phi_native_predecomp_baseline_2026_05_24.md` 172 LoC · 10 § (목적 · 5-rule baseline · Rust oracle · 6-anchor · regression criterion · fixture · environment · honest_limits · next-step · ledger)
- [x] `verify_phi_native.hexa` 재실행 — cycle 3 byte-identical (5 rule byte_equal=false + 1 det PASS)
- [x] regression criterion strict: abs_diff = 0.0 (IEEE bit-equal) ∧ Rust oracle |d| ≤ 2e-15 (≤ 2 ulp hard cap)
- [x] 17 측정 freeze (5 rule + 6 anchor + ...) → M4 regression harness hardcoded constants
- [x] honest_limits 5 (L1 single-state · L2 small fixture · L3 H_211 marginal · L4 hexa runtime drift · L5 environment dep)
- [ ] M2 (design RFC) — Agent 1 진행 중
- [ ] M3 (impl phase 1) — 5 fn upstream PR · M2 + M4 baseline land 후

## 2026-05-24T22:00:00Z — cycle 1 · survey LAND 🛸

- [x] `HEXAD/STDLIB/survey_2026_05_24.md` 228 LoC · 9 § (방법 · 카테고리 표 · dup 매핑 · stdlib 제안 구조 · 1st-wave ranking · 2nd-wave · honest_limits · cross-link · next-step)
- [x] 10 카테고리 (math · info · signal · stats · linalg · RNG · consciousness · wolfram-CA · graph · void-safe) · 47 candidate fn
- [x] ~247 dup sites — hot top: abs_f(77) · pow2_int(33) · wolfram_init_row(32) · lcg_next(28) · sqrt_newton(17)
- [x] 1st-wave 5 fn (`pow2_int` · `log2` · `bin_values_minmax` · `shannon_entropy` · `mutual_info_pair`) promote 시 phi_native 200→50 LoC (-75%)
- [x] hexa-lang stdlib 부분 존재 확인: `core/math.hexa` · `core/math/float.hexa` · `iit_ei.hexa` · `rng.hexa` · missing log2/pow2/bit_set 가 sprawl root cause
- [x] `iit_ei.hexa::LN2_INV` 상수 재활용 권장 (M2 phase entropy port)
- [ ] M2 (design) — stdlib 구조 RFC 작성 · hexa-lang upstream filing
- [ ] M3 (impl phase 1) — 1st-wave 5 fn upstream PR
- [ ] M4 (verify) — phi_native byte-equal 보존 regression
- [ ] M5 (migration) — anima 측 import path 교체
- [ ] M6 (phase 3) — 2nd-wave (wolfram_run_ca · pearson · spearman · voss · abs_f upstream)

## 2026-05-24T21:30:00Z — 도메인 신설 + survey 발사

- [x] STDLIB.md scaffold · 9 milestones · 5 honest_limits · cross-repo 양식
- [x] @goal: anima 전반의 general primitive 를 hexa-lang stdlib 으로 promote · anima 는 import-only
- [x] 첫 cycle = anima 전체 grep (survey) → candidate priority 표 + duplicate helper 매핑
- [x] PHI 도메인 (9/9 LAND) 가 첫 사례 source · phi_native.hexa 분해 후 stdlib/info/* + math/* + consciousness/*
- [ ] cross-repo design — hexa-lang 측 stdlib 구조 RFC + anima 측 import path 교체
- [ ] EEG / signal-processing 후속 candidate phase 3
