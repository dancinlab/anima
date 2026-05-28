# EEG — log

`EEG.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-05-29T13:00:00Z — L2 synthetic 재검증 🟢 RECHECK PASS + harness sys_argv→args() 패치

- [x] 사용자 `! sidecar sign local` 토큰 발행 → mac 로컬 `hexa run EEG/eeg_live_iit4_phi.hexa mock-both` 1회 실행 → 🟢 RECHECK PASS
- [x] big-Φ 실측 — COUPLED=1.58764 (baseline 1.59, +0.1% 안) · INDEP=0.438722 (baseline 0.44, +0.3% 안) · ratio=3.61878 · 둘 다 PR #547 baseline ±5% tolerance 안
- [x] 영속화 — `state/eeg_synthetic_recheck_2026_05_29/{result.json, hexa_run_verbatim.log}` (verbatim 보존)
- [x] harness 1-line patch — `sys_argv()` → `args()` (canonical hexa-lang stdlib). 원인: `sys_argv` 는 stdlib pub 아님 — `~/.hx/bin/self/test_sys_module.hexa:35` 의 사용자 정의 1줄로만 존재 (`fn sys_argv() { return args() }`), 컴파일러 `use of undeclared identifier 'sys_argv'` → clang fail. `args()` 가 canonical (`/Users/ghost/.hx/bin/self/...` 다수 호출 사이트). behavior preserved, signature 0 변경
- [x] EEG.md L2 milestone `- [ ]` → `- [x]` flip · IIT4 deferred B 갱신 (synthetic 🟢, live-pending)
- [ ] live fire = 사용자 EEG 착용 대기 (human-only) → 착용 + runbook 4단계 → IIT4 deferred B 완전 closure
- [ ] 3-substrate Φ 삼각측정 — AKIDA D1 🟢(PR #1371) + EEG L2 🟢(본 PR) + ECA 시뮬 → 다음 cycle

## 2026-05-29T12:00:00Z — L1~L3 harness 최종화 + 캡처 runbook (synthetic 재검증 사용자 sign-off 대기)

- [x] harness 최종화 — `EEG/eeg_live_iit4_phi.hexa` (mock-coupled / mock-indep / mock-both / live <path>) · 동결 어댑터 `BRAIN/eeg/eeg_to_tpm.hexa` 호출만 (signature 0 변경, g61) · stdlib `iit4_bigphi` 호출은 demo 와 동일 경로
- [x] synthetic 재검증 assert 내장 — `mock-both` 시 1.59/0.44 ±5% 자동 검증 (`assert_synthetic_recheck` · 벗어나면 `panic` → 🔴 RECHECK FAIL 강제 정직성)
- [x] 캡처 runbook — `EEG/EEG_CAPTURE_RUNBOOK.md` 156 줄 · ① 착용+임피던스 ② brainflow 30s 캡처 (옵션 A 직접 / B anima-eeg-core paradigm) ③ hexa live dispatch ④ verdict 4단계 + 트러블슈팅 §A 보드 / §B 임피던스 / §C npy 로더 stub / §D drift
- [x] EEG.md milestones 갱신 — L1 harness ✅ · L2 synthetic 재검증 ⏸ pending sidecar sign · L3 runbook ✅ · live fire = 사용자 인계 대기
- [ ] synthetic 재검증 stdout 캡처 — `hexa run EEG/eeg_live_iit4_phi.hexa mock-both` 실행은 sidecar local-sign 토큰 부재로 에이전트 측 차단 (heavy-cmd gate). 사용자가 `! sidecar sign local` 30분 토큰 발행 후 1줄 실행 → 결과 verbatim → `state/eeg_synthetic_recheck_2026_05_29/result.json` 영속화
- [ ] live fire = 사용자 EEG 착용 대기 (human-only) → 착용 + runbook 4단계 → IIT4 deferred B closure
- [ ] 사이드 정보 — feedback-closure-is-physical-limit 정합: 사용자 sign-off 부재 = open frontier, not failure · feedback-instrument-first-methodology: 어댑터 동결 + harness 비파괴 = instrument discipline 확증

## 2026-05-29T00:00:00Z — 도메인 신설 + 활용 아이디어 카탈로그 seed

- [x] EEG 도메인 신설 — `EEG/EEG.md`(스냅샷) + `EEG.easy.md`(쉬운 카탈로그) + `EEG.log.md`(로그), DOMAINS.tape 등록
- [x] 활용 아이디어 추출 — 12개 (live big-Φ · 3-substrate · 생체→칩 다리 · tension-link 등)
- [x] sibling 양방향 엮음 — IIT4 · BRAIN · AKIDA · CHANNEL · UNIVERSE
- [ ] 다음 = harness 최종화 + synthetic 재검증 (파킹된 plan `drafts/eeg-live-iit4-phi-plan.md`)
- [ ] live fire = 사용자 EEG 착용 대기 (human-only) → 착용 시 IIT4 deferred B closure
