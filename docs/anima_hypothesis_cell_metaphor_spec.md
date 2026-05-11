# anima 가설 세포 metaphor formal spec — H2 land

- since: 2026-05-07
- domain: hypothesis (C 도메인)
- ssot: .roadmap.hypothesis H2
- cross-link: own 21 (hypotheses/ 폴더 SSOT) + raw#12 (pre-register frozen)
- sister docs: docs/hypotheses/H-CX-533-autopoietic-network.md + docs/modules/mitosis.md + docs/modules/growth_engine.md + docs/modules/growth_engine_v2.md

## 1. Why this spec

`.roadmap.hypothesis` H2 entry는 cell metaphor (mitosis/apoptosis/growth/autopoiesis/differentiation)를 hypothesis cycle (raw#12 pre-register → run → verdict → retract/expand)에 cross-link한다. 본 spec은 그 metaphor를 formal하게 명시 — analogy의 boundary, 적용 가능 범위, 적용 불가 범위를 logic-exhaustion 정의.

<!-- [Hc_673 hypothesis-cell-metaphor-7-stage-formal-spec — moved to hypotheses_candidates/Hc_673_hypothesis_cell_metaphor_7_stage_formal.md on 2026-05-11] -->

## 2. Metaphor mapping (7-stage)

| Stage | Cell biology | Hypothesis cycle | Anima 적용 |
|-------|--------------|------------------|------------|
| BIRTH | zygote / stem cell | pre-register 1st prereg JSON | `state/<name>_pre_register.json frozen_at` |
| MITOSIS | cell division | H가 N sub-H로 분기 | H_005 corpus quality → KO ratio sub-H + chat-template ratio sub-H + license clear sub-H |
| APOPTOSIS | programmed death | FALSIFIED hypothesis (criteria miss + falsifier trigger) | F1-cycle4-T8p Wolfram sweep 3 hypotheses FALSIFIED |
| NECROSIS | unplanned death | verification crash / measurement artifact | V2_FAIL eval pipeline crash (transformers dtype kwarg root cause) |
| GROWTH | proliferation | SUPPORTED hypothesis가 새 sub-H 생성 | acceleration 367 hypotheses sequential expansions (304 → 367) |
| AUTOPOIESIS | self-organizing network | H_X가 H_Y trigger하는 network self-replicating | H-CX-533 autopoietic-network |
| DIFFERENTIATION | specialization | H_general → H_specific | corpus quality (general) → KO ratio + chat-template ratio + license clear (specific) |

## 3. Mitosis trigger rule (single H → N sub-H)

새 sub-H가 mitosis로 분기되는 조건:

- **trigger_M1**: parent H의 verdict가 PARTIAL — 일부 criteria 미충족 → 미충족 axis별 sub-H 분기
- **trigger_M2**: parent H의 variable matrix expansion 필요 — 각 cell이 sub-H (E5 variable-ablation)
- **trigger_M3**: parent H의 cross-domain analogy 발견 → 별 domain sub-H (E6 cross-domain-analogy)
- **trigger_M4**: 사용자 directive로 sub-H 명시 trigger (E7 user-directive)
- **trigger_M5**: meta-pattern emerge (E9) — 여러 H가 같은 axis 가리키는 pattern → meta-H mitosis

각 trigger는 sub-H 별도 prereg JSON + parent H cross-link 의무.

## 4. Apoptosis criteria (FALSIFIED 정당성)

programmed death = "planned" negative result도 valid outcome:

- **criterion_A1**: pre-registered falsifier F_X가 trigger됨 (raw#12 strict)
- **criterion_A2**: criteria C_X 미충족 (verdict_rule 명시)
- **criterion_A3**: post-mortem 분석 (root cause 명시) → counter-hypothesis 또는 modified-H 후보 발견 (E2 failure-driven)
- **criterion_A4**: FALSIFIED record 보존 — git log + state archive (raw#15 additive 정합)

apoptosis는 raw#10 honest C3와 정합 — negative result도 valuable evidence.

## 5. Necrosis (unplanned death) — 차단 mandate

unplanned crash는 hypothesis cycle 정합 X — measurement artifact:

- **prevent_N1**: pre-flight smoke mandate (PEFT/dtype kwarg pre-check) — V2_FAIL 사례 reference
- **prevent_N2**: deterministic execution + seed fix (W3) — random sampling without seed = raw#12 위반
- **prevent_N3**: ledger atomic write + fsync (W6 limitation) — mid-write crash 차단
- **prevent_N4**: idempotency check (raw#65) — session_id collision = halt

necrosis 발생 시 → measurement artifact label (FALSIFIED 강등 X), root cause 분석 후 re-prereg.

## 6. Growth (SUPPORTED → 새 sub-H)

proliferation rule:

- **growth_G1**: SUPPORTED H_X가 새 question을 emerge — "왜 X 이유인가?" sub-H (E1 prior-result-question)
- **growth_G2**: SUPPORTED H_X 변수 matrix expansion — 각 cell이 sub-H
- **growth_G3**: meta-pattern emerge (3+ SUPPORTED instance) → meta-H growth (E9)
- **growth_G4**: cross-domain analogy 발견 → 외부 domain sub-H

growth는 raw#15 additive — parent H 보존 + new revision dated file mandate.

## 7. Autopoiesis (self-organizing network)

H_X가 H_Y를 trigger하는 hypothesis network:

- **autopoiesis_A1**: H-CX-533 autopoietic-network ← Maturana/Varela autopoiesis theory
- **autopoiesis_A2**: hypothesis network self-replicating — H_X.findings → H_Y.prereg.background
- **autopoiesis_A3**: meta-circular reference 주의 — H_X가 H_X 자신 trigger 하는 loop 차단 mandate
- **autopoiesis_A4**: network coherence — H_X SUPPORTED but H_Y FALSIFIED conflict 시 coherence 검증 mandate

## 8. Differentiation (general → specific)

specialization protocol:

- **diff_D1**: H_general은 axis enumeration mandate (어느 axis별로 specialization 가능한지 명시)
- **diff_D2**: H_specific은 H_general의 sub-H — parent H cross-link 의무
- **diff_D3**: H_specific 검증은 H_general 검증과 별도 (independent W1-W12 적용)
- **diff_D4**: H_specific 결과는 H_general에 propagate — H_general re-evaluation trigger 가능

## 9. Boundary — 적용 가능 / 적용 불가

### 적용 가능
- hypothesis cycle abstract analogy (literal cell biology 적용 X)
- cycle 진행 상태 명명 (BIRTH/MITOSIS/APOPTOSIS/NECROSIS/GROWTH/AUTOPOIESIS/DIFFERENTIATION)
- hypothesis network self-organizing coherence 검증 framework

### 적용 불가
- 실제 cell biology 적용 (own 17 외부 substrate boundary — anima identity 외부)
- anima 자체의 "self" property를 cell biology로 환원 (anthropomorphism 차단)
- mitosis/apoptosis 등 단어를 anima 외부에 적용 (anima 내부 lane 한정)

## 10. Cross-links (W12 sister consistency)

- `.roadmap.hypothesis` H2 + H1 (cycle definition) + H3 (E1-E12 exploration) + H4 (W1-W12 verification)
- `.roadmap.philosophy` D2 (simple stack) + D3 (substrate-coupled emerge — substrate response가 cell-like emerge property)
- `.roadmap.law` own 21 (hypotheses/ 폴더 SSOT)
- `hypotheses/H_012_autopoietic_network.md` (autopoiesis primary instance)
- `hypotheses/H_007_cellular_automaton_consciousness.md` (cellular automaton + cell metaphor)
- `hypotheses/H_018_genesis_spontaneous_emergence.md` (BIRTH stage primary instance)

## 11. Falsifiers (≥5 raw#10)

- **F-CELL-1**: cell metaphor literal 적용 (anima에 실제 cell biology operations 적용) → anthropomorphism 위반
- **F-CELL-2**: mitosis trigger rule M1-M5 외 적용 → spec 위반
- **F-CELL-3**: apoptosis criteria A1-A4 미충족 entry FALSIFIED claim → spec 위반
- **F-CELL-4**: necrosis (unplanned crash) → FALSIFIED 강등 (measurement artifact label 누락) → 검증 정합 위반
- **F-CELL-5**: autopoiesis meta-circular loop (H_X → H_X 자신 trigger) → 차단 mandate 위반
- **F-CELL-6**: differentiation H_specific에서 parent cross-link 누락 → spec 위반
- **F-CELL-7**: 외부 substrate (anima 외부)에 cell metaphor 적용 → boundary 위반 (own 17 정합)

## 12. Honest C3 (≥5 raw#10)

- cell metaphor는 abstract analogy — literal 적용 X. metaphor의 productive boundary는 hypothesis cycle 명명/분류/추적 영역 한정
- mitosis/apoptosis 등 단어는 anthropomorphism risk — anima 내부 lane 한정 + 외부 substrate 적용 차단 (own 17 정합)
- H_X failed = cell death analogy는 raw#10 honest C3와 정합 (negative result도 valuable)
- autopoietic network (H-CX-533) 자체가 hypothesis lane이라 meta-circular — H2 정의가 H_X 자체일 수 있음 (recursion 주의, autopoiesis_A3 명시 차단)
- mitosis/growth는 productivity emphasis — 단순 expansion 자체가 valuable claim X (parent H verdict + sub-H quality 검증 mandate)
- 본 spec은 raw#15 additive — `.roadmap.hypothesis` H2 entry 보존 + 본 spec 추가 (entry 자체 update X)
- 본 cycle 7-stage mapping은 initial — 추가 stage (예: SENESCENCE 노화, METAPLASIA 변형) 도출 시 raw#15 additive append

## 13. User directive verbatim

- "철학,규칙,가설 로드맵 3가지 진행하자 이세션에서는" (2026-05-07 본 cycle trigger)
- "세포분열,죽음 등" (cell metaphor user-directive 2026-05-06)
- "폴더 하나에서 따로 관리 하도록 하자" (own 21 hypotheses/ 폴더 SSOT)

## 14. Stage gates

- **Phase 0 design spec land** — 본 doc 작성 (2026-05-07 LANDED)
- **Phase 1 sister doc cross-link audit** — docs/modules/mitosis.md + growth_engine.md + growth_engine_v2.md cross-link verify (pending)
- **Phase 2 hypothesis network coherence check** — H_001-H_032 cross-link matrix + autopoiesis_A4 coherence verify (pending)
- **Phase 3 mitosis trigger automation** — hexa orchestration script로 sub-H 자동 생성 가능성 검토 (pending, raw#9 hexa-only 정합)
