# STDLIB — log

Append-only history sister of `STDLIB.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-25T18:30:00Z — /cycle 1: phase1+2 완료 재확인 + phase3 survey + install 동기화 ⭐️

- [x] /cycle 3-agent fan-out (M5 migration · phi_spatial · phase3 survey) — 전부 착지
- [x] M5 migration **already-done 재확인** (#424+#428): phi_native.hexa 332→56 LoC shim, stdlib import, **byte-equal 5/5 MATCH** (phi_h = frozen baseline § 2.1 bit-identical)
- [x] phi_spatial **already-done 재확인** (#780+#792): `phi_spatial_native` (builtin 충돌 회피), info/* thin 합성, 빌드+테스트 PASS
- [x] phase3 survey LANDED — `HEXAD/STDLIB/phase3_survey_2026_05_25.md` (#449): signal/DSP 60+ fn (window 26 dup) = 다음 promote · clustering NONE · MITOSIS/CHAT phase-1 dup
- [x] **로컬 hexa-lang install 동기화** — `~/core/hexa-lang` detached → `origin/main` (#846; #769/#792/#801/#829/#830/#839 포함). stale 브랜치 `chore/abolish-inbox-folder` WIP 는 stash 보존 (복구가능). override 없이 `hexa run verify_phi_native` → byte-equal 5/5 재확인 (stale-install 의 phi_spatial_native undeclared 에러 해소)
- [!] **hexa-lang 컴파일러 fix 세션 부산물** (STDLIB 의존 upstream): #829 const-fold cross-scope silent-wrong-answer · #830 runtime.h rt_read prototypes · #839 immutable-let-reassign — 전부 MERGED. commons.tape **@D g61** (stdlib SSOT governance) 신설 (sidecar 0.10.3)
- [ ] **다음**: signal/ DSP promote (phase3 M1) — 6-module hexa-lang stdlib land + window 26-dup sweep

## 2026-05-25T01:30:00Z — M5 migration LANDED + #780 collision fix · byte-equal 확정 🛸

- [x] **anima #424 MERGED** — `phi_native.hexa` 332→52 LoC shim 분해, stdlib 위임 (phi_native_spatial→phi_spatial_native · phi_bin_values→bin_values_minmax). surface 보존 (phi_helper · verify · diag_l1 무변경).
- [x] **byte-equal 검증 (verify_phi_native, full cross-import flatten)**: phi_h = [4.9773e-09, 0.422585, 4.9773e-09, 0.585842, 0.790028] == frozen baseline § 2.1 **5/5 bit-match**. cross-import 체인 (verify→phi_native→phi_spatial_native→mutual_info→binning+entropy+bitops) end-to-end 작동.
- [!] **M5가 적발한 실버그 1 — PR #780 BROKEN (name collision)**: stdlib `phi_spatial` 이 `phi_spatial` **builtin** (codegen→hexa_phi_spatial, runtime.c:7941) 과 충돌 → import 시 redefinition. CI stdlib 미테스트 + agent sc_ self-contained 검증으로 미탐지, M5 통합서 노출. **fix: hexa-lang #792 MERGED — `phi_spatial`→`phi_spatial_native` rename** (flatten-build 4/4 PASS 검증).
- [!] **M5가 적발한 실버그 2 — builtin DRIFT 실측 확증 (rfc_036_c_replica_drift)**: phi_spatial **builtin** 이 frozen baseline 에서 이탈 (rule110 4.9773e-09 → 4.90943e-06, 3 orders). 그래서 M5 는 builtin 이 아닌 **stdlib pure-hexa replica** 에 위임 (frozen 보존). verify 의 phi_c≠phi_h byte_equal=false 는 이 drift 이지 M5 회귀 아님.
- [x] g59 #785 (CI stdlib 미테스트 갭) 가 실제로 문 비용을 냄 — #780 collision 이 그 사례. #792 commit 이 #785 참조.
- [ ] cycle-full 2nd-wave 잔여 (wolfram/ca #782 · stats/correlation #781 · signal/voss #783 도 LANDED — 위 M3 와 별개 4 module, 총 8 stdlib module)
- [ ] phase 3 — abs_f(77)/sqrt_newton(17)/lcg_next(28) anima-side sweep (전부 builtin/import 치환, 대규모 별도 cycle)

## 2026-05-25T00:10:00Z — M3 (impl phase 1) · hexa-lang stdlib 4 module LAND ⭐️

- [x] hexa-lang PR #769 MERGED (2026-05-24T12:01:44Z UTC) — https://github.com/dancinlab/hexa-lang/pull/769 · CI 3-platform bootstrap + grace-consent PASS
- [x] 4 module +232 LoC: `stdlib/math/bitops.hexa` · `stdlib/info/binning.hexa` · `stdlib/info/entropy.hexa` · `stdlib/info/mutual_info.hexa` + `scaffold_phase1_test.hexa`
- [x] byte-equal algorithm port: phi_native 의 `phi_bin_values`/`phi_entropy`/`phi_native_mi_pair` 그대로, entropy 는 `log(x)/log(2.0)` 유지
- [x] verify: 5/5 parse clean · 알고리즘 10/10 PASS (self-contained build) · cross-import flatten 은 M5 재부트스트랩에서 행사
- [!] **RFC 수정 (실측)**: `stdlib/math/log.hexa::log2` DROP — `log2` 는 이미 builtin (`runtime_core.c::hexa_log2` → libm). RFC "missing" 전제 오류 (5 → 4 module). bitops 는 native shift/and (phi_native mult-workaround 불필요).
- [!] **hexa-lang 측 발견 (g59 후보 INBOX)**: (1) CI bootstrap 이 stdlib 모듈 미테스트 — compiler bootstrap 만 검증 (2) 단일파일 `hexa build` 이 import flatten 안 함 — `module_loader` 선행 필요 (3) `log2` builtin 존재로 RFC 갱신 필요
- [ ] M4 (verify) — anima phi_native byte-equal regression (baseline freeze 이미 완료)
- [ ] M5 (migration) — anima `phi_native.hexa` 분해 → stdlib import 로 교체 (200→50 LoC) · 여기서 cross-import flatten 실제 검증
- [ ] phi_spatial (RFC §5 2nd-wave) — info/* 합성 wrapper 별도 cycle

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
