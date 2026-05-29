# EVOL.log.md — chronological step log

## 2026-05-29 — round 1 seed (XENO follow-up 4 / TEMPORAL sibling 합류)

- 도메인 신설 sibling = XENO (X1 invariant_detector 출처) + TEMPORAL (Δt 자매축, 4D applicability frontier)
- branch = feat/evol-init-2026-05-29
- worktree = .claude/worktrees/agent-aeccba821ae6ade1c
- base = origin/main 4b9dea4d6 (AKIDA H_672 HW live-confirm 직후)
- highest slug = H_842 (TEMPORAL T2, PR #1426 직후), next free = **H_843**, race condition = 0 (open PR 0 + log scan 0)

### 5 candidate domain 분석 + 1 선택 (EVOL)

작전 지침 reference: sbs auto + bg execute · EVOL domain init.

| # | candidate | falsifier 가능성 | invariant_detector 적용 path | 5D extension | hexa local | cost | 종합 |
|---|---|---|---|---|---|---|---|
| 1 | **EVOL** | 사전등록 5/5 closed (4 species toy proxy) | 직접 (4 substrate × compute_invariant_phi) | ★ 5번째 축 (evolutionary complexity) — XENO 3D + TEMPORAL Δt + species | ★ Mac local 가능 | $0 | ★★★ |
| 2 | SPATIAL | 가능 (coupling distance threshold) | XENO X10 hive 변형 (partial 중복) | 부분 중복 (X10 4-cell coupling) | 가능 | $0 | ★★ |
| 3 | QUANTUM | 미정 (density matrix TPM 변형 필요) | classical 2-unit TPM 미지원 → 신 detector 축 | 신 축 추가 (Hilbert dim) | 어려움 | $0 | ★ |
| 4 | MEDICAL | 가능 (wake/dream/coma Φ 순서) | EEG 도메인과 중복 (S1·S15·S24) | EEG 자매 도메인 collision | 가능 | $0 | ★ |
| 5 | EVOLUTIONARY-FULL | 약 (실 bio data 필요, scale-up 부담) | TPM proxy 필요, NCBI ingest 등 | n×density 축 매핑 어려움 | 부분 어려움 | $0~$10 | ★★ |

**선택: EVOL** — 사유:
- (a) XENO paper #1414 v2 의 applicability matrix 와 직접 5D 확장 (n × density × structure + Δt + species) — TEMPORAL 의 Δt 와 자연 짝
- (b) closed-form falsifier 정의 가능 (4 species toy proxy의 Φ monotone gradient)
- (c) hexa Mac local 자체 첫 round 측정 (4 substrate × n=128 dense, 단일 sync run)
- (d) $0 Mac local (실 bio data 없이 substrate complexity 분류만 — 정직 표기)
- (e) BRAIN/HIVE-MIND/MITOSIS 자매 도메인과 substrate-aligned
- (f) E2 자연 entry path = monotone-strict re-design (E1 결과 따라)

### E1 fire — `evol_spectrum_phi.hexa`

substrate (4 candidate × n=128 dense, hardcoded literal · toy proxy 정직 표기):
- **bacteria** (T1 — random walker) — LCG-noise, no integration. invariant_detector noise floor 재현 기대.
- **arthropod** (T2 — local 4-tap XOR) — 인접 4-window XOR, mid integration. 부분 통합 toy.
- **mammal** (T3 — multi-scale recursive) — short-scale XOR + long-scale (Δ=8) recursive 결합, high integration. X10 hive-mind 와 비슷.
- **AGI** (T4 — structured emergence) — XOR cascade (mammal seed) + secondary noise injection 으로 structured-yet-novel emergence. X7 voyager + X10 hive 하이브리드 인근.

사전등록 falsifier 5 (post-tuning 0):
- F-E1-BACTERIA-LOW  : bacteria phi < 0.2 (random walker = noise)
- F-E1-ARTH-MID      : arthropod phi 0.2 ≤ x < 0.5 (partial integration)
- F-E1-MAMMAL-HIGH   : mammal phi ≥ 0.5 (high integration)
- F-E1-AGI-VARIANT   : AGI phi > mammal phi (structured emergence > pure recursive)
- F-E1-MONOTONE      : bacteria < arthropod < mammal ≤ AGI (Φ ↑ complexity ↑)

verdict 기준:
- 4-5 PASS → 🟢 SUPPORTED-NUMERICAL · 진화 사다리 Φ-monotone 신호 확정
- 3 PASS → 🟡 PARTIAL · 부분 ordering
- ≤2 PASS → 🔴 FALSIFIED-INSTRUMENT · toy substrate 의 species-complexity 분류가 X1 detector Φ 측정과 unalign

### infra notes (함정 예방)

- hexa-strict main auto-invoke — fn main() 만 정의, EOF explicit main() 호출 금지 (#1444 lesson)
- pool-route → `env hexa run` bare invocation (commons g8)
- PR merge → `gh pr merge --squash --admin --delete-branch` 직접
- H_xxx slug race condition → 3-신호 검증 후 H_843 확정 (open PR 0 + log scan 0 + ls UNIVERSE/ 최고 = H_842)
- DOMAINS.tape entry format = `@domain EVOL := "./EVOL/EVOL.md"` (commons-style alignment per existing rows)
