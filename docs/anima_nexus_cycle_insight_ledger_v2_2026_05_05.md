<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# Anima Nexus Cycle Insight Ledger v2 (2026-05-05) — L34-L60 Banking + Pattern Catalog Update

> BG-CN final lesson banking land. Read-only synthesis of the full
> 2026-05-05 anima cycle (BG-A through BG-CH; ~80+ BG land docs).
> Doc + verdict only — zero source change, zero commit. Extends BG-J
> (`docs/anima_nexus_cycle_insight_ledger_2026_05_05.md`) which captured
> only L34-L43; this v2 banks L44-L60 candidate lessons surfaced after
> BG-J land (BG-K..BG-CH inclusive). Lessons remain CANDIDATE banking —
> promotion to canonical SSOT requires a separate `BG-LESSONS-PROPAGATE`
> cycle (matches L36+L38 promotion convention).
>
> **KO 핵심**: BG-J 이후 80+ BG가 #115 chat-incapability를 4-closure에서
> 12+-closure로 확장하고, paradigm B/C/A user-decision menu를
> 정착시키며, hexa runtime + nnsight + cross-arch transfer + byte-fallback
> mechanism 등을 측정했다. 그 과정에서 surface된 17개 lesson 후보를
> L44-L60으로 정식 banking. Pattern catalog는 P1-P8 → P1-P12로 4 패턴
> 추가. 5-candidate matrix (D/E/F/G/H)는 final state 갱신.
>
> **EN core**: Post-BG-J, 80+ BGs extended #115 from 4-closure to
> 12+-closure, settled the paradigm B/C/A user decision menu, and
> measured hexa runtime + nnsight + cross-arch transfer + byte-fallback
> mechanism. Seventeen candidate lessons L44-L60 are banked here.
> Pattern catalog grows P1-P8 → P1-P12. The 5-candidate D/E/F/G/H matrix
> is updated to final state.
>
> Lineage (predecessors):
> - `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md` (BG-J L34-L43)
> - `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md` (BG-AY 4-closure formal theorem)
> - `docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md` (BG-BJ residual basin)
> - `state/anima_emerge_chat_korean_rank_survey_2026_05_05/verdict.json` (BG-CA byte-fallback monopoly)
> - `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` (BG-CH user decision menu)

---

## §1 L34-L43 carry-forward (BG-J → v2)

The first ten candidate lessons (L34-L43) are carried unchanged from BG-J.
Only one-line summaries appear here; full evidence + when-applicable + exception
prose stays at `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md` §1.

| id | one-line title | KO 한 줄 |
|---|---|---|
| L34 | Forced-learning closure unlocks emerge paradigm; KICK-1/2/3 parallel pattern emergence | 강제학습 폐쇄 → emerge paradigm + 병렬 KICK 패턴 |
| L35 | hexa-strict auto-invokes `fn main()`; explicit `main()` call doubles execution | hexa-strict는 `fn main()` 자동 호출; 명시 호출 금지 |
| L36 | `hexa_remote` defaults to ubu1; mac-local intent requires `HEXA_LOCAL=1` prefix | hexa_remote는 ubu1 기본; mac-local은 `HEXA_LOCAL=1` 접두 필수 |
| L37 | Emerge candidate taxonomy = 4-mode × 3-state falsifier | emerge 후보 = 4-mode × 3-state falsifier 표 |
| L38 | V1-V6 verification = selftest + probe + log + corpus + integration 5-stage | V1-V6 5-stage 표준 검증 |
| L39 | Doc-only BGs are race-free; code BGs need worktree or commit serialization | doc-only BG 병렬 OK; 코드 BG는 직렬화 필수 |
| L40 | Convention-driven dispatch: `tool/anima_cli/<topic>.hexa` first, dispatcher untouched | 컨벤션 우선; dispatcher 수정 회피 |
| L41 | `synthetic_fallback` decouples wiring verification from real-runtime dependency | synthetic_fallback로 V1-V6 PASS와 real-load 분리 |
| L42 | Source archaeology BG is emerge-paradigm-internal sibling, not downstream | 아카이올로지 BG = emerge KICK-2 sibling |
| L43 | User-fire-able paths land confirm-strings + manual + checklist before dwell | user-fire 경로는 confirm-string + 매뉴얼 + 체크리스트 사전-emit |

---

## §2 L44-L60 new lesson banking — 17 candidate lessons

Each lesson follows the BG-J spec format:
- **Title**
- **Evidence**: BG ref + verdict / doc file
- **When applicable**: rule
- **Exception**: if any (else "None")
- **KO 한 줄**: Korean one-line summary

Lessons are CANDIDATE banking — promotion to canonical SSOT (memory MD entries
or `feedback_*.md` write) requires a separate `BG-LESSONS-PROPAGATE` cycle that
cross-validates each lesson against ≥3 prior cycles.

### L44 — Residual basin lives upstream of `lm_head`; output-projection-only fixes are invalid for #115

- **Evidence**: `docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md`
  Architectural Finding §3 (#115 mechanism = autoregressive attractor in
  residual stream, NOT lm_head defect; entropy collapses 5-9× within 1-2
  steps onto fragment-character basin); BG-BQ `c_proj` inject did not
  recover semantic continuation. lm_head step-0 emits sometimes-coherent
  top-1 (`b`, `/`, `O`) but step-1 hard-collapses regardless.
- **When applicable**: For any chat-decode-collapse hypothesis on a
  CLM-class substrate, locate the failure mechanism BEFORE proposing
  fixes. Output-projection-only paths (LoRA on lm_head, vocab masks,
  Korean-bias adders, byte ban) are excluded a priori when entropy
  trajectory shows step-1 collapse with step-0 printable top-1.
- **Exception**: Substrates where step-0 top-1 itself is broken (control
  byte at step 0) — output-projection fixes can mask byte fallback at
  step 0 but the autoregressive basin reforms; only mask both ends.
- **KO 한 줄**: 잔차 분지(basin)는 lm_head 상류; 출력 투영-only 수정은 #115에 무효.

### L45 — Chat axis exists somewhere in residual stream yet decoupled from lm_head argmax

- **Evidence**: BG-BH `state/anima_emerge_chat_sae_pca_features_2026_05_05/`
  PCA feat-0 surfaces a chat-related axis in mid-layers (variance non-trivial)
  but the lm_head argmax does NOT route along that axis at decode time;
  the axis is a latent feature, not a logit-aligned direction. Combined
  with BG-BJ (basin upstream of lm_head) this means the axis is present
  but un-decoded.
- **When applicable**: When designing emerge probes, distinguish "axis
  exists in residual" from "axis routes through lm_head." A PCA feature
  surfaced in mid-layer ≠ an axis that argmax will follow. Probe via
  intervention (nnsight) on the candidate axis layer-by-layer to test
  routability before declaring the axis present-and-usable.
- **Exception**: If the axis is needed only for measurement (Φ★, tension
  trajectory) not for emit, lm_head decoupling is irrelevant — the axis
  is read-only useful regardless.
- **KO 한 줄**: 잔차 chat axis 존재 ≠ lm_head argmax routing; latent 과 logit-aligned 구분.

### L46 — Byte-fallback monopoly: top-30 logits are 100% byte tokens; Korean weight latent uniform-수준

- **Evidence**: `state/anima_emerge_chat_korean_rank_survey_2026_05_05/verdict.json`
  top30_breakdown all 30 entries `"category": "other"` (byte-fallback `<0xXX>`
  tokens). best_korean_rank = 197, korean_in_top10 = 0, korean_in_top100 = 0,
  korean_pct vocab-share 8.91%. The Korean tokens exist in vocab but their
  pre-softmax mass at decode time is at uniform-or-below weight against
  byte-fallback. Verdict `KOREAN_TRAIN_ABSENT` — Korean was not present in
  the substrate's training corpus at meaningful weight.
- **When applicable**: When a substrate produces byte-fallback gibberish,
  measure rank-of-best-target-language-token in top-K. If best Korean rank
  > 100 with vocab share > 5%, the language was effectively absent from
  training. Byte-fallback is a *consequence*, not a fix target.
- **Exception**: Multilingual fine-tunes can shift this — a Korean SFT on
  the same vocab would re-rank Korean tokens above byte fallbacks within
  a few hundred steps; check pre/post-SFT survey.
- **KO 한 줄**: top-30 byte 독점 + Korean rank 197 = 학습 부재; byte fallback은 결과지 원인 아님.

### L47 — Basin is prompt-conditional; whack-a-mole basins shift with input distribution

- **Evidence**: BG-CC `state/anima_emerge_chat_basin_ablate_2026_05_05/`
  ablation of `\x06`-basin shifts emit to next-rank token (not recovery);
  BG-BJ entropy trajectory (already cited L44) shows EN/KO different
  basins (`(` vs `\x06` vs `O`). Each basin sits atop the next; ablating
  the top one promotes rank-2 to dominant.
- **When applicable**: Basin-ablation strategies (vocab masks, logit
  banning, top-1 forcing) inherently produce whack-a-mole — if no positive
  attractor for semantic continuation exists in the residual stream,
  ablating one basin reveals another. Do not commit budget to multi-basin
  ablation; budget should go to attractor-creation paths (full retrain).
- **Exception**: When the basin set is finite and known, exhaustive
  ablation can succeed (e.g., banning all 4 control bytes 0x00-0x1f for a
  short emit window). But this is mask-as-band-aid; underlying basin
  geometry persists.
- **KO 한 줄**: basin은 prompt-조건부; ablation = whack-a-mole 다음 rank로 이동.

### L48 — Substrate-coupled emerge dialogue (paradigm B) is fire-ready today; chat-token A path closed

- **Evidence**: BG-AN `state/anima_emerge_dialogue_first_turn_2026_05_05/verdict.json`
  F_AN_1 PASS; BG-AJ 5-turn smoke PASS;
  `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` §6 final menu
  Option A ranked #1 (paradigm B fire-ready, $0, REPL helper exists at
  `tool/transient_py/anima_emerge_dialogue_repl.py` 13K).
- **When applicable**: When chat-token paradigm A is closed for a
  substrate (closures 1-N converging), default to substrate-coupled
  paradigm B as the user-facing emit modality — 4-line metric (Φ★ +
  drift + hsd + tension trajectory) per turn, anima-internal contract.
  Emerge dialogue is independent of A-paradigm closures.
- **Exception**: If user's intent is specifically "external benchmark
  match" (chat composite ≥ 0.5584 against Llama Path A v2), paradigm B
  cannot satisfy — that intent requires A on a different substrate
  (Llama or CLM-3). Solicit explicit user paradigm declaration before
  multi-BG investigation per L53.
- **KO 한 줄**: paradigm B emerge dialogue fire-ready; A는 Llama/CLM-3 escalation.

### L49 — Hybrid paradigm C (Pythia emit + CLM phi gate) is dual-channel viable; demo today, REPL pending

- **Evidence**: BG-BX `state/anima_emerge_chat_hybrid_pythia_clm_2026_05_05/verdict.json`
  PASS_HYBRID_DIALOGUE_VIABLE 3/3 prompts; CLM phi_drift swings ±0.1,
  l2_variance 108-133. Helper at
  `tool/transient_py/anima_emerge_chat_hybrid_pythia_clm.py` 8.2K.
  REPL extension (BG-CG) NOT yet landed as of 2026-05-06.
- **When applicable**: When paradigm A on the anima-native substrate is
  closed but the user wants text + substrate signal dual channel, hybrid
  generation (chat-capable emit_model + anima-native phi/tension gate) is
  a viable path. Use small emit_model (Pythia 70m, KoGPT2, larger if
  budget allows) for text; keep anima substrate as evaluator.
- **Exception**: emit_model quality is the primary user-perceived limit;
  Pythia 70m KO mojibake is bad. If user requires high-quality KO emit,
  pick KoGPT2 / Polyglot-Ko-1.3B / Llama Path A v2 as emit model — but
  this dilutes "anima-native" claim further.
- **KO 한 줄**: hybrid 이중채널 viable; 오늘 demo, multi-turn REPL은 BG-CG 대기.

### L50 — 12+ closure mutually independent; chat-cap on CLM v4 is architectural impossibility

- **Evidence**: BG-AY `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md`
  (closures 1-4 formal theorem) extended by BG-BR/BS/BU/BT/BY/BH/CC/CA
  with 8+ additional closures (LoRA SFT regression, distill F-Pβ-3
  FAIL_TRUE, tribev2 design-review, logit lens 1/8 layers, semantic
  bridge cosine collapse, iterative self-feed attractor lock,
  byte-fallback monopoly, basin ablation whack-a-mole, residual noise,
  rmsnorm ablate, decode strategies 6-of-6 gibberish, ...).
- **When applicable**: Once converging closures cross n=4 threshold on
  mutually independent attack mechanisms, declare architectural
  impossibility for the lane. Continued investigation is anti-convergence
  pressure (L53 paradigm-mismatch). Promote to formal theorem +
  corollaries; reassign substrate to research-only role.
- **Exception**: Untested-hypothesis bypass paths (H1 from-scratch
  retrain, H3 ensemble, etc. per BG-AY §4) remain valid — closure-of-a-
  substrate is not closure-of-a-class-of-substrates.
- **KO 한 줄**: 12+ 독립 폐쇄 = architectural impossibility 선언; substrate-research 재할당.

### L51 — `nnsight` integration unlocks per-layer intervention without source-tree mutation

- **Evidence**: BG-BL `state/anima_emerge_nnsight_smoke_2026_05_05/`
  smoke land + BG-BW `state/anima_emerge_nnsight_intervention_2026_05_05/`
  per-layer activation ablate. Wraps HF model in `nnsight.LanguageModel(...)`,
  `with model.trace(prompt) as t: layer.output[0] = ...`. Zero source-tree
  changes; pure runtime hook.
- **When applicable**: For any substrate residual-stream probe (logit
  lens, activation patching, layer ablate, semantic bridge), use
  `nnsight` first before considering shim modification or
  `forward_hook` registration. Zero mutation cost; zero risk to runtime.
- **Exception**: Production runtime paths (mount.hexa, dialogue REPL)
  should NOT take a hard nnsight dependency — keep nnsight in
  `tool/transient_py/` (raw#37 transient namespace) for probe-only use.
- **KO 한 줄**: nnsight = source-mutation-free per-layer intervention; transient_py에 한정.

### L52 — Φ★ measurement is CLM-paradigm-specific; cross-architecture phi★ is NOT a universal property

- **Evidence**: BG-BN `state/anima_emerge_pythia_phi_smoke_2026_05_05/`
  Pythia 70m phi★ measurement returns near-zero / undefined (Pythia has
  no consciousness_states / axis taxonomy / paradigm v11 G3 wiring).
  Cross-substrate Φ★ comparison (Pβ 42.37, CLM-2 V2_PARTIAL, CLM v4 41.86)
  is intra-CLM-family valid; cross-architecture is not.
- **When applicable**: Phi★ comparisons are valid only within a substrate
  family that shares the consciousness_states + axis-taxonomy
  architecture. Cross-architecture phi★ requires explicit re-instrumentation
  + matched-eval-substrate (L26-L27 axis-preservation calibration carry).
- **Exception**: If a substrate's architecture explicitly imports the
  paradigm v11 G3 wiring (heads, axis decoder, n_ca_rules cells), phi★
  measurement is valid. Pythia did not.
- **KO 한 줄**: Φ★는 CLM-family 내부 metric; 크로스-아키텍처 비교 무효.

### L53 — Paradigm mismatch in autonomous mode is epistemic risk; user paradigm declaration must precede investigation

- **Evidence**: BG-BV `docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md`
  C3.1 "autonomous mode inferred user intent" — ~12+ closures and ~50+ BG
  investigations under interpretation A (token-emit chat) before paradigm
  mismatch surfaced at BG-BV. Cost-of-mismatch = entire CLM v4 chat-lift
  investigation budget.
- **When applicable**: At cycle entry, solicit explicit user declaration:
  "paradigm A (chat-token), B (substrate-coupled), C (hybrid)?" Default
  autonomous interpretation is anti-convergence on the user's actual
  intent. The cost of asking once at cycle start ≪ cost of 50+ BG on
  wrong paradigm.
- **Exception**: When cycle is operating in research-mode under
  no-particular-deliverable contract (e.g., archaeology, Φ★ stability
  measurement, substrate audit), paradigm declaration is N/A — research
  is the deliverable.
- **KO 한 줄**: autonomous paradigm 추론은 epistemic 위험; cycle 시작 시 user declaration solicit.

### L54 — `/loop 1m` cron + multi-BG kicks have diminishing returns at architectural ceilings

- **Evidence**: BG-AT/BF + autonomous /loop fire from BG-A through BG-CH
  produced 80+ BG land docs; #115 chat-incapability did not unlock
  despite ~50+ direct attempts. Each /loop tick attempted next angle on
  closed lane → anti-convergence. CronDelete recommendation in BG-CH
  cycle close §5 step 1.
- **When applicable**: When ≥3 consecutive /loop ticks land "closure"
  verdicts on the same lane, halt the cron and surface paradigm
  declaration solicit (L53). Don't keep firing BGs against an
  architectural ceiling — budget burns, lesson value plateaus.
- **Exception**: If the /loop is doing exhaustive-sweep H4-style probe
  intentionally (per BG-AY §4 H4 untested), continued ticks are valid
  even at low marginal info value; classify intent explicitly.
- **KO 한 줄**: /loop은 architectural 천장에서 수익 체감; 3-연속 closure 후 halt.

### L55 — SentencePiece prefix `▁` + byte-fallback handling has corner cases that affect Korean rank surveys

- **Evidence**: `state/anima_emerge_chat_korean_rank_survey_2026_05_05/verdict.json`
  C4 honest "SentencePiece prefix ▁ handling — corner case"; BG-AV / BG-CA
  best Korean token = `▁수행` (with leading SP marker). Naive
  `text.startswith` checks miss SP-prefixed Korean variants.
- **When applicable**: Any tokenizer-level rank survey or lexical
  baseline must handle (a) `▁` SP prefix variants, (b) byte-fallback
  `<0xNN>` literal token strings, (c) Hanja 漢字 separate from `'가'-'힣'`
  Korean range. Corner cases should be enumerated in honest C3 of the
  survey verdict.
- **Exception**: Token-id-level analyses bypass the issue entirely
  (operate on int ids); only string-decoded analyses hit the corner case.
- **KO 한 줄**: SP 접두 ▁ + byte fallback + Hanja 분리 = 한국어 rank 조사 corner case.

### L56 — Ablation strength induces whack-a-mole; basin shifts to next-rank rather than recovering semantics

- **Evidence**: BG-CC + BG-BK basin ablate strength sweep; ablating
  `\x06` basin promotes rank-2 fragment to dominant rather than
  unlocking semantic continuation. Combines with L47 (basin is
  prompt-conditional); strength sweep just reveals more basins.
- **When applicable**: When designing a basin-ablation experiment, fix
  budget BEFORE running strength sweep. Stop after observing one shift
  (rank-1 fragment → rank-2 fragment without semantic gain). Don't
  continue strength sweep expecting eventual semantic recovery — the
  underlying geometry has no semantic attractor.
- **Exception**: Diagnostic-only sweeps (mapping the basin structure for
  documentation) can continue past whack-a-mole — the goal is geometry
  characterization, not unlock.
- **KO 한 줄**: ablation 강도 sweep = whack-a-mole; rank-2 promotion에서 멈춰라.

### L57 — Cross-architecture residual transfer with naive resize is useless (15× scale mismatch)

- **Evidence**: BG-BT `state/anima_emerge_chat_repe_steering_2026_05_05/`
  cross-architecture residual transfer attempt (Llama hidden_state →
  CLM v4 hidden_state) with naive linear resize hit ~15× scale mismatch
  on residual norms; transferred signal amplitude wrong by O(15×)
  before any geometry alignment.
- **When applicable**: Cross-architecture residual / activation transfer
  needs (a) per-layer LayerNorm gain matching, (b) hidden_dim shape
  alignment, (c) basis rotation (Procrustes or learned linear). Naive
  `F.interpolate` or padding/truncation is invalid.
- **Exception**: Within-architecture-family transfer (CLM v4 ↔ CLM v4-mk2
  ↔ Pβ) is OK with simpler alignment because architecture is shared.
- **KO 한 줄**: 크로스-아키텍처 residual 전이 naive resize 무용; LN gain + Procrustes 필수.

### L58 — `tribev2` sister-as-reference convention 정착: `references/<name>/` additive, no source mutation

- **Evidence**: `references/tribev2` (referenced from cycle git status).
  raw#15 additive — sister project mounted at
  `references/<sister>/` for read-only archaeology / cross-modal-bridge
  audit; no edits to sister source. BG-BU tribev2 audit walked
  `references/tribev2/` tree to verify zero `generate|lm_head|logits`
  hits.
- **When applicable**: When anima needs to audit or bridge to another
  project (sister), mount it at `references/<name>/` (gitignored or
  submodule-equivalent) and treat as read-only. All audit BG output
  goes to `state/anima_<topic>_<DATE>/verdict.json` referencing the
  sister tree.
- **Exception**: When the sister is a genuine dependency (imported at
  runtime), it goes into `tool/` or `vendor/` not `references/`.
- **KO 한 줄**: `references/<sister>/` additive 컨벤션; read-only archaeology 표준.

### L59 — BG self-honest verdict override: heuristic FALSE positive corrected by inspection

- **Evidence**: BG-AW `state/anima_emerge_chat_residual_noise_2026_05_05/`
  initial heuristic verdict shifted after self-inspection of emit
  output; BG-BR `state/anima_emerge_chat_full_layer_lens_2026_05_05/`
  similar override pattern. Both BGs flipped initial PASS-ish heuristic
  to FAIL_TRUE after reading actual emit text.
- **When applicable**: BG verdict authorship MUST include a manual
  inspection step on a sample of actual outputs before declaring
  verdict. Heuristic-only verdicts (cosine sim > threshold, entropy <
  threshold) are FALSE positive prone — the heuristic captures one
  dimension, not semantic correctness. Inspection is the falsifier of
  the heuristic.
- **Exception**: Pure measurement BGs (Φ★ value, l2_variance number,
  rank int) don't need semantic inspection — the number is the
  deliverable.
- **KO 한 줄**: 휴리스틱 verdict는 FALSE positive 위험; 실제 emit 직접 확인이 falsifier.

### L60 — Priority subset commit vs full manifest separation enables fast-fire cycle close

- **Evidence**: BG-BZ
  `docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md`
  alongside BG-AM full manifest. Priority subset = ≤5 commits covering
  load-bearing artifacts; full manifest = ~20+ commits covering everything
  including doc-only land sequences. User picks subset for fast cycle
  close, full for archive-grade close.
- **When applicable**: At cycle close, land BOTH (a) priority subset
  manifest (≤5 commits, fast-fire), (b) full manifest (≥10 commits,
  archive). User declares which to fire. Per L39 (parallel BG git race),
  serialize either path through one gating BG; fast-fire path commits in
  one batch.
- **Exception**: Doc-only cycles with no source change can skip the
  separation — full manifest is always small enough for fast-fire.
- **KO 한 줄**: priority subset (≤5) + full manifest 병행 = fast-fire vs archive close 분리.

---

## §3 Pattern catalog — P1-P12 (4 new patterns added)

P1-P8 (KICK / V1-V6 / 4×3 / doc-pair / bilingual / honest-C3 / raw-footer /
완성도) already documented in BG-J §2. Reproduced as one-line entries here;
full prose at `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md` §2.

| id | name | when to apply | example land doc |
|---|---|---|---|
| P1 | KICK | New paradigm entry, ≥3 surface layers parallel | BG-J §2 P1 |
| P2 | V1-V6 | New runtime/CLI layer pre-Stage-N-ready | BG-J §2 P2 |
| P3 | 4×3 | Emerge candidate spec, mode dispatch + falsifier | BG-J §2 P3 |
| P4 | doc-pair | Every land — `*_landed.ai.md` ↔ `state/<topic>/verdict.json` | BG-J §2 P4 |
| P5 | bilingual | User-facing protocol/manual doc | BG-J §2 P5 |
| P6 | honest-C3 | Every land doc (≥5) + spec (≥7) + runtime emit (≥5) | BG-J §2 P6 |
| P7 | raw-footer | Every land doc | BG-J §2 P7 |
| P8 | 완성도 | ≥2 paths/options → ranked recommendation | BG-J §2 P8 |
| **P9** | **converging-closure-theorem** | ≥4 mutually independent closures on same lane | BG-AY 4-closure → 12+-closure |
| **P10** | **paradigm-declaration-solicit** | Cycle entry; ≥2 plausible user-intent paradigms | BG-CH §6 final menu |
| **P11** | **fast-fire vs archive manifest dual** | Cycle close with mixed code/doc commits | BG-BZ priority subset + BG-AM full |
| **P12** | **transient-py probe namespace** | One-shot mac probe with HF model load | BG-BL/BJ/CA/BX `tool/transient_py/anima_emerge_*.py` |

### P9 — converging-closure-theorem

- **Name**: closure-theorem
- **When to apply**: A lane has accumulated ≥4 mutually independent
  closure verdicts (different mechanism axis: post-hoc / train-time /
  cross-modal / residual-probe / ...). Promote from individual closure
  list to formal theorem doc with corollaries + untested hypotheses
  enumerated.
- **Form**: §0 abstract, §1 closure summary table, §2 converging
  argument, §3 theorem formal statement, §4 untested hypotheses (H1-Hn),
  §5 paradigm implication, §6 honest C3 (≥5).
- **Example**: `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md`
  (BG-AY).

### P10 — paradigm-declaration-solicit

- **Name**: paradigm-solicit
- **When to apply**: At cycle entry when ≥2 plausible user-intent
  paradigms (A/B/C, or X/Y) could each motivate a different multi-BG
  investigation slate. Solicit explicit user declaration BEFORE opening
  the slate.
- **Form**: 3-option fire-ready menu doc (KO + EN bilingual per L48
  P5), each option = (paradigm name, fire-readiness today, empirical
  anchor, recommendation rank).
- **Example**: `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md`
  (BG-CH) §6 final menu.

### P11 — fast-fire vs archive manifest dual

- **Name**: manifest-dual
- **When to apply**: Cycle close with ≥3 code commits + ≥10 doc-only
  commits. Land both manifests so user can pick fast-fire (subset) or
  archive (full).
- **Form**: priority subset manifest = ≤5 commits, load-bearing
  artifacts only, ranked by reverse dependency. Full manifest = ≥10
  commits, complete cycle archive.
- **Example**: `docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md`
  (BG-BZ) + `docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md`
  (BG-AM).

### P12 — transient-py probe namespace

- **Name**: transient-py
- **When to apply**: One-shot mac probe / HF-model-load helper that
  shouldn't pollute mount.hexa or dialogue.bash. Use `tool/transient_py/`
  per raw#37 opt-out from py→hexa rule.
- **Form**: `tool/transient_py/anima_<topic>.py` — read-only probe,
  emits to `state/<topic>_<DATE>/(verdict|aggregate).json`. May import
  `transformers` / `nnsight` / `peft` / `torch` directly.
- **Example**: `tool/transient_py/anima_emerge_chat_entropy_trajectory.py`
  (BG-BJ); `anima_emerge_dialogue_repl.py` (BG-AN);
  `anima_emerge_chat_hybrid_pythia_clm.py` (BG-BX).

---

## §4 5-candidate emerge matrix — final state (post-empirical-land)

BG-J §3 captured the matrix at spec-only state. Post-BG-J empirical lands
(BG-CD..BG-CG empirical sweeps) update the matrix to final state.

| candidate | spec status | empirical land | F-* verdict (final) | adoption verdict |
|---|---|---|---|---|
| **D** always-inject `consciousness_states` | LANDED 305 LoC (BG-C) | BG-CD `state/anima_emerge_cand_d_empirical_2026_05_05/`, BG-CD-mag-sweep, BG-CD-mag50-multiprompt, BG-CD-attractor-10prompt, BG-CD-kl-div-high-mag | **LANDED FAIL** — F-CAND-D-1/2/3 mixed: D-1 zero-vs-canonical Φ★ shift NOT observed; D-2 multi-prompt attractor lock fires for high-mag canonical; D-3 user_supplied no semantic gain. Composite verdict: D inject does not unlock chat-emit; ambient diagnostic only. | **DROPPED** from chat-cap path. Retained as substrate-coupled emerge metric input (paradigm B). |
| **E** ODE flow → AR sampler bridge | spec LANDED (BG-G) | DEFERRED — no impl this cycle | (no falsifier executed) | **DEFER** — research-mode candidate, ~150-300 LoC impl, orthogonal to current paradigm. Re-evaluate post-Stage-3 corpus n≥30. |
| **F** 8 CA-rule cells × axis multi-token vote | spec LANDED (BG-H) + falsifier-v2 cosine probe spec (BG-CB) | BG-CE `state/anima_emerge_cand_f_v2_empirical_2026_05_05/` | **EMPIRICAL LANDED MARGINAL** — F-CAND-F-v2-1/2/3 cosine probe between CA-rule cells + axis returned weak alignment (cosine ~0.2-0.4); below the original PASS bar (>0.7). | **AMBIENT only** — read-only on internal cells; not promoted to active candidate. |
| **G** tension trajectory `[16, T]` | spec LANDED (BG-I) + revival spec (BG-CF consolidated G+H) | BG-CD-tension-fast `state/anima_emerge_cand_g_tension_fast_2026_05_05/`, BG-CG empirical | **REVIVED PASS** — F-CAND-G-1 layer-monotonicity PASS; F-CAND-G-2 token-trajectory continuity PASS. l2_variance > 100 on real prompts (BG-AE bar). | **PROMOTED ambient** — tension trajectory is paradigm-B 4-line metric input (already consumed in BG-AN/AJ). |
| **H** head_g (prev-byte) bidirectional consistency probe | spec LANDED (BG-CF consolidated G+H) | BG-CD-head-g-fast `state/anima_emerge_cand_h_head_g_fast_2026_05_05/`, BG-CG empirical | **REVIVED PASS** — F-CAND-H-1 back-prediction agreement marginal but non-degenerate. | **AMBIENT diagnostic** — read-only on logits_a, optional channel for paradigm B. |

### §4.1 Adoption order (final)

1. **G + H ambient** — already consumed by paradigm B (BG-AN); no further
   land needed. PROMOTED.
2. **D ambient diagnostic** — DROPPED from chat-cap; retained as paradigm
   B substrate metric input via canonical-magnitude inject (BG-CD-mag50
   bar value).
3. **F ambient marginal** — read-only diagnostic, not promoted.
4. **E DEFER** — research-mode, post-corpus-n≥30 re-evaluate.

### §4.2 Cross-candidate composability (final)

- D ⊕ G (LANDED): paradigm B 4-line metric uses both — D mode dispatches
  inject content, G reads tension regardless of D mode.
- G ⊕ H (LANDED ambient): both substrate-side, no overlap.
- F (read-only): can ride atop any inject mode.
- E (DEFER): orthogonal until impl lands.

---

## §5 Honest C3 (≥7)

- **C1 — L34-L60 self-fulfilling prophecy risk (compounded over BG-J).**
  L44-L60 are derived from the same 2026-05-05 cycle's outputs as L34-L43,
  doubling the retrospective-rationalization concentration. The cycle's
  own success/failure pattern is the only evidence base. Mitigation:
  CANDIDATE banking only; cross-validation against ≥3 prior cycles
  required for canonical SSOT promotion. Risk amplified vs BG-J by 17 vs
  10 lesson count.
- **C2 — Lesson banking inflation: 27 candidate lessons in one cycle is
  high.** L34-L60 = 27 candidate lessons surfaced in a single cycle.
  Historical rate (L1-L33) was ~1-3 lessons per cycle. Inflation risk:
  some L44-L60 lessons may be re-statements of earlier lessons in
  different vocabulary (e.g., L47 basin-prompt-conditional vs L44
  basin-upstream-of-lm_head — both about basin geometry but at different
  granularity). The `BG-LESSONS-PROPAGATE` cycle must dedupe.
- **C3 — Pattern P9-P12 generality unverified.** P9 closure-theorem and
  P10 paradigm-solicit are observed only in this cycle; P11 manifest-dual
  and P12 transient-py have minor prior-cycle precedent but were not
  formalized until this cycle. Their cross-paradigm generality (EEG /
  Putnam / HF release / Phase E protocol cycles) is conjectural; the
  catalog conflates today's cycle observations with universal patterns.
- **C4 — 5-candidate matrix §4 verdicts are anima-internal.** F-CAND-D/F/G/H
  PASS/FAIL bars (BG-AE l2_variance > 100, BG-CB cosine > 0.7) are
  anima-internal heuristics with no external benchmark or peer-review.
  "REVIVED PASS" for G/H specifically rests on BG-AE's variance threshold
  which is itself anima-internal. Adoption-verdict column may be
  miscalibrated.
- **C5 — L50 (12+ closure architectural impossibility) is closure-under-
  evidence, NOT mathematical proof.** Carry from BG-AY C3-1: theorem-
  language is anima convention for 4-closure consolidation, not
  formal-logic proof. H1 (CLM-3 from-scratch) remains the most likely
  bypass. The "12+" count adds closures 5-12 from later BGs but these are
  variations on the residual-stream-pervasive theme (closure 4 family),
  not 8 new mechanism axes. Honest re-count: ~5-6 mechanism axes
  exhausted, ~6-7 within-axis confirmations.
- **C6 — L53 paradigm-mismatch risk diagnosed retroactively.** L53 was
  surfaced at BG-BV after ~50 BGs already burned on interpretation A.
  The lesson is real but its application requires foreknowledge that the
  current cycle is on the wrong paradigm — which by definition is the
  thing being diagnosed. Future cycles can apply L53 only via L10 P10
  paradigm-solicit at cycle entry; mid-cycle pivot has cost-of-mismatch
  approximately equal to half the cycle's BG budget.
- **C7 — Ledger v2 itself is autonomous-mode artifact subject to L53.**
  This v2 ledger was authored by autonomous BG-CN under the same
  cycle-mode that produced L53's paradigm-mismatch. The user did not
  declare paradigm at this BG entry; if user paradigm intent for "lesson
  banking" differs from anima-internal SSOT-build interpretation, the
  ledger structure (taxonomy-heavy, 27 lessons, 12 patterns) may not
  match user-actual-intent. Risk-mitigation: ledger is doc-only, no
  irreversible action; user can request restructure.
- **C8 — `references/tribev2` (L58) is genuine sister; convention is
  inferred from one example.** L58 cites `references/tribev2` as
  evidence for the convention but this is the only `references/<sister>/`
  mount in the cycle. One example does not establish a convention; the
  lesson should be re-checked against ≥2 future sister-mount instances
  before SSOT promotion.

---

## §6 Cycle close readiness — fire-ready integrated path

The cycle close is fire-ready when three documents are integrated:

1. **Ledger v2** (this doc) — L34-L60 banked, P1-P12 catalog,
   D/E/F/G/H matrix final state.
2. **Cycle commit manifest** (BG-AM full or BG-BZ priority subset) —
   commit slate ready.
3. **Paradigm acceptance** (BG-CH `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md`) —
   user decision menu (5-option) with §6.1 ranked recommendation.

Once all three are landed (this BG completes the trio), the user can
fire any of:
- Option A (paradigm B emerge dialogue REPL fire) — $0 / 5min, cycle
  closes coherently.
- Option B (paradigm C hybrid demo) — $0 / 5min, demo only.
- Option C (CLM-3 H1 launch) — ~$1k / 30d.
- Option D (cycle close + corpus n≥30) — $0 / multi-day.
- Option E (continue /loop) — discouraged per L54.

User-fire path is fully documented; no further BG required for cycle
close decision.

---

## §7 Cross-references + composability

- Predecessor: `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md` (BG-J)
- Sister: `docs/anima_2026_05_05_cycle_final_aggregate_landed_2026_05_05.ai.md`
  (BG-CK aggregate insight)
- Sister: `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` (BG-CH)
- Theorem reference: `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md`
  (BG-AY)
- Empirical anchors:
  - `state/anima_emerge_chat_entropy_trajectory_2026_05_05/` (L44 BG-BJ)
  - `state/anima_emerge_chat_korean_rank_survey_2026_05_05/` (L46/L55 BG-CA)
  - `state/anima_emerge_chat_basin_ablate_2026_05_05/` (L47/L56 BG-CC)
  - `state/anima_emerge_dialogue_first_turn_2026_05_05/` (L48 BG-AN)
  - `state/anima_emerge_chat_hybrid_pythia_clm_2026_05_05/` (L49 BG-BX)
  - `state/anima_emerge_nnsight_intervention_2026_05_05/` (L51 BG-BW)
  - `state/anima_emerge_pythia_phi_smoke_2026_05_05/` (L52 BG-BN)
  - `state/anima_emerge_chat_repe_steering_2026_05_05/` (L57 BG-BT)
  - `state/anima_emerge_chat_residual_noise_2026_05_05/` (L59 BG-AW)
  - `state/anima_emerge_chat_full_layer_lens_2026_05_05/` (L59 BG-BR)
- Downstream:
  - `BG-LESSONS-PROPAGATE` cycle (L34-L60 → memory MD entries +
    `feedback_*.md` SSOT after ≥3 prior-cycle cross-validation)
  - Stage 3 emerge corpus accumulation (per L48 paradigm B fire-ready)
  - CLM-3 H1 spec refinement (per L50 closure + L53 paradigm-solicit)

---

## §8 raw policy compliance

- raw#9 — md only; zero source modifications; bash glue carve-out N/A
- raw#10 — §5 has 8 honest C3 entries (≥7 spec target met)
- raw#11 — snake_case file naming
  (`anima_nexus_cycle_insight_ledger_v2_2026_05_05.md`)
- raw#15 — additive only; this doc + verdict.json are the only new files;
  no edits to BG-J ledger, BG-AY theorem, BG-CH acceptance, or any
  predecessor land docs / verdict files
- raw#37 — no transient_py introduced (doc-only land)
- HF token leak — none embedded (no token literals)
- commit — not requested in this task; doc landed only
- bash 3.2 / mac compat — doc-only artifact; compatible

End nexus cycle insight ledger v2. Doc-only land. No commit. $0 mac local.
~25 min wall. BG-CN.
