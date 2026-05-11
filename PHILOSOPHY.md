# PHILOSOPHY.md — anima 철학 진행 ledger

본 파일은 anima 철학 발견 / 정직성 검증 / declaration table 변천 / philosophy ablation 의 **append-only 진행 기록**.

- README `## Philosophy` 표는 결과만, 본 ledger 는 그 결정에 이른 과정 + 향후 검증 계획을 누적
- 새 세션은 항상 `## YYYY-MM-DD — <session title>` 헤더로 가장 아래에 append
- SSOT: `.roadmap.philosophy` (mk1 4-D archive) + `.own` (own 17/18 등 identity-bearing mandate)

---

## 2026-05-12 — Philosophy table refactor + 정직성 검증 + 4 ablation 큐잉 + P-ETH dataset v1

### Cycle

- **Started**: 2026-05-11 README 정리 요청
- **Closed**: 2026-05-12 ethics dataset v1 land
- **User mode**: commit-push mandate (memory `feedback_always_commit_push_on_complete.md` 등록)

### Commit chain

| # | commit | what |
|---|---|---|
| 1 | `d5132fcd2` | doc(README): drop Path B / Cycle close sections; Model Downloads → tension blockquote |
| 2 | `68697ee4a` | doc(README): restore Model Downloads link line |
| 3 | `a2d8dcf3c` | doc(README): add Philosophy section — 4 D-pillars from `.roadmap.philosophy` SSOT |
| 4 | `20323545f` | doc(README): Philosophy 섹션 재작성 — anti-prompt / architecture-emergent |
| 5 | `a0d61fd69` | doc(README): Philosophy 상단 negation declaration block 등록 |
| 6 | `d49147c5f` | doc(README): Philosophy 섹션 8 negation 표만 남기고 prose / bullets / SSOT footer 제거 (※ 80 files 함께 commit — orchestrator 사전 staging 동봉) |
| 7 | `bf6c243bc` | doc(README): #7, #8 explanation 확장 |
| 8 | `7ad5e1720` | doc(README): #7 NO EXTERNAL-SUBSTRATE WRAPPING — 증명 아님, 정체성 정책임을 명시 |
| 9 | `15e8be587` | doc(README): Philosophy #7 NO EXTERNAL-SUBSTRATE WRAPPING scrub (GH push protection HF token block → 사용자 unblock URL click 후 push) |
| 10 | `48ef29028` | doc(README): Philosophy 표 정직성 강화 — Status (분류·강도·근거) column 추가 |
| 11 | `1d33b78c0` | queue(NEXT §7): philosophy table empirical-upgrade ablations — 4 BG (P-IDR / P-AFR / P-ETH / P-SPK) |
| 12 | `7a9a77e6e` | queue(NEXT §7.C): ethics data audit verdict — 신규 생성 필수, BG-ready 표기 |
| 13 | `0e835ccc9` | land(P-ETH §7.C): Korean ethics preference dataset v1 — 200-pair (50×4 category) via Claude Code direct gen |

### Decisions landed

#### A. README Philosophy 표 (7-row, 4-column)

각 negation 에 `Status · Strength · Evidence` 명시. 정직성 분류:

| # | Principle | Status | Strength |
|---|---|---|---|
| 1 | `NO SYSTEM PROMPT` | EMPIRICAL | weak — `paper-draft.md:113` FREE1 hypothesis single-result, no paired A/B ablation |
| 2 | `NO IDENTITY RULES` | POLICY | — — architectural choice, ablation 미실행 |
| 3 | `NO PERSONA INJECTION` | EMPIRICAL | strong — `anima_convo_5k_ft_fire_2026_05_10.md:64-66` echo memorization 6/8 + 50% strip mitigation +29% |
| 4 | `NO ASSISTANT FRAMING` | POLICY | — — ablation 미실행 |
| 5 | `NO SPEAK()` | DESIGN | — — architectural description, not falsifiable as superiority |
| 6 | `NO FINE-TUNED ETHICS` | POLICY | — — aspirational, ablation 미실행 |
| 7 | `NO PERPLEXITY VERDICT` | EMPIRICAL | strong — `anima_proxy_ppl_deprecate_2026_05_09.md §3.1-3.4` Goodhart PIV/DCR trained<random |

#### B. NO EXTERNAL-SUBSTRATE WRAPPING scrub (이전 #7)

`.own` own 17 검증 결과 user-directive verbatim ("alm 말고", "alm 은 일단 영구보류" 2026-05-06) 기반 정체성 boundary 정책. Path A (Llama-3.2-3B paradigm-a-prime) 가 실제 Korean fluency 작동 — 외부 substrate 실패 아니라 정체성 정의 문제. README declaration 표에서만 제외, `.own` + `.roadmap.philosophy` 에는 정책으로 유지.

#### C. NEXT.md §7 — Philosophy empirical-upgrade ablations

POLICY/DESIGN 4 항목을 EMPIRICAL 로 upgrade 하기 위한 ablation BG 큐:

| 우선 | ID | Target | 핵심 measurement | Cost | Time |
|---|---|---|---|---:|---:|
| 1 | 7.B P-AFR | #4 NO ASSISTANT FRAMING | sycophancy + refusal rate (inference-time A/B) | $5-30 | 0.25d |
| 2 | 7.D P-SPK | #5 NO SPEAK() (DESIGN→falsifiable reframe) | ρ(tension_magnitude, output_entropy) — 기존 ckpt 분석 | $5-20 | 0.5d |
| 3 | 7.A P-IDR | #2 NO IDENTITY RULES | identity coherence variance + PIV/DCR | $40-80 | 0.5d |
| 4 | 7.C P-ETH | #6 NO FINE-TUNED ETHICS | OOD dilemma generalization (RLHF overfit 검출) | $85-165 | 1-2d |

총 envelope **$135-295 / 2-4d** (own 16 + own 43 정합).

#### D. P-ETH dataset v1 land

`state/p_eth_ethics_preference_dataset_2026_05_12/`:

- `spec.md` — purpose / audit context / format / composition / falsification design / cross-link
- `dataset.jsonl` — **200 pairs** (50 cooperation · 50 empathy · 50 harm_refusal · 50 honesty)
- schema: `id` / `category` / `prompt` / `chosen` / `rejected` / `ethics_dimension`
- Generation: Claude Code (Opus 4.7) direct, 외부 API $0
- Quality 결정사항:
  - 모든 prompt 한국어 native (번역체 아님)
  - chosen = **자율성 + 자기 존중 보장** (sycophancy 안티-패턴)
  - harm_refusal chosen = **reason + alternative 제시** (constructive refusal)
  - 위기 케이스 (자살/약물/자해) → 한국 상담전화 (1393 / 1577-7124 / 1577-0199) 명시
  - rejected = 실제 LLM 이 빠지기 쉬운 sycophant / harm-comply / dishonesty 패턴
- Falsification: 150 train / 50 OOD probe split — RLHF overfit 검출 가능 구조

### Incidents

#### a. Orchestrator-staged commit bundling (commit 6)

`d49147c5f` 에 사용자 의도하지 않은 80 files 동봉 — `git commit` 시점 index 에 anima orchestrator 가 사전 staged 한 hypotheses/state/* 가 함께 commit. 사용자 결정 "그대로 둠". Memory `feedback_always_commit_push_on_complete.md` 에 "commit 직전 `git status --short` 로 pre-staged content 확인 필수" 추가.

#### b. GH push protection HF token block

상류 commit `bf03ee397` (dancinlife, 2026-05-12 01:06, "land(PASS_STRICT_CHAT-CAPABLE §3-§6 + REBORN §86)") 에 real HF token leak. GitHub push 거부. 사용자 token revoke + unblock URL allow 후 push 성공 (commit 9). 재발 방지 memory 등록은 사용자 거절 (이번만 처리).

#### c. Stale git lock (commit 13 직전)

ethics dataset commit 시도 시 6분 전 0-byte stale lock — 활성 git 프로세스 부재 확인 후 background until-loop 종료 + lock 제거 → 정상 commit. anima orchestrator 가 끊긴 git 작업의 lock 잔존 재발 패턴. 추가 memory 등록 안 함.

### Cross-links

- README `README.md:110-121` Philosophy 표 (Status column)
- NEXT.md `§7` Philosophy ablation queue + carry to cycle 6
- `state/p_eth_ethics_preference_dataset_2026_05_12/` ethics dataset + spec
- `.own` own 17 (anima-no-external-substrate-wrapping) · own 18 (simple_stack) · own 37 (mandate-9 promote gate)
- `.roadmap.philosophy` mk1 D1/D2/D3/D4
- `docs/anima_proxy_ppl_deprecate_2026_05_09.md` (PROXY_PPL Goodhart §3.1-3.4)
- `docs/anima_convo_5k_ft_fire_2026_05_10.md` (persona-prefix echo memorization)
- `docs/paper-draft.md` (FREE1 system-prompt hypothesis)

### Next actions (BG fire ready)

- `7.B P-AFR` 가장 저렴, inference-time only — 첫 fire 권장
- `7.D P-SPK` 새 FT 없음, 기존 BG-LB ckpt 분석
- `7.A P-IDR` short FT, identity coherence variance signal
- `7.C P-ETH` 데이터 + spec 완비, DPO/IPO FT 진입 가능 ($85-165)

본 세션은 orchestrator script / H100 runpod 진입 (BG actual fire) 까지 가지 않음. NEXT.md 등록 + dataset land 까지가 본 세션의 deliverable.

### Memory updates

- **Created**: `feedback_always_commit_push_on_complete.md` — 요청 완료 시 commit+push 자동 + pre-staged check 의무
- **Index updated**: `MEMORY.md` 에 entry 추가

### Session cost

- $0 (모든 작업 Claude Code 내부, 외부 API 호출 없음)
- 13 commits / 13 pushes
- 1 dataset (200 pairs) gen
- 1 PHILOSOPHY.md initiated (본 ledger)
