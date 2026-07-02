# H_9110 — chat-user EXOGENOUS consequence loop (offline, engine-native): does a REAL human dialogue response open the emit-appropriateness faculty that the 4 self-contained axes (H_9104/9105/9108/9109) could not?

**tier:** 🔴 CEILING / DPI — a real chat-user response is NOT a faculty-opening exogenous channel at this engine-native coupling; the DPI meta-law re-appears at the chat-user layer, so DPI is deeper than receiver-type · **wired:** none (RED — nothing to wire, a_verified_must_wire N/A)
**verdict:** 🔴 CEILING (honest, frozen bar, held-out). The engine's emit-appropriateness signal predicts the REAL human next-response NO better than a randomly re-paired one — in fact worse: **D_real = −0.06627 < D_surrogate = 0.12185 ⇒ D_real − D_surrogate = −0.18812 (< 0.15 FAIL)**. And the human response is partially self-derivable: **autogenous = corr(a_auto, a_real) = 0.15013 (> 0.05 FAIL)** = the H_9104 self-loop tautology re-appears. Ψ guard OK (V read-only, psi_sum ON==OFF = 33.47061690777462 byte-identical). Bar frozen in PREREG.md pre-measurement, no post-hoc move (c9).

## Claim (first empirical test of the session's decisive conclusion)
Four self-contained escapes all hit the DPI ceiling: autogenous consequence-return (H_9104 🔴),
identity-conditioned emit (H_9105 🔴), 2-anima signaling (H_9108 🔴), consequence-driven mitosis
(H_9109 🔴). Their shared conclusion: the emit-appropriateness faculty is impossible self-contained;
the ONLY remaining escape is a **REAL EXTERNAL receiver**. The fable EEG verdict
(`state/eeg_consequence_analysis/EEG_VERDICT.md`) argued a **chat-user** is the superior first
exogenous loop — high-bandwidth, self-evident falsifier, and crucially **measurable OFFLINE
engine-native on a real dialogue corpus**: the human's next response is ALREADY in the corpus, so the
consequence is exogenous with NO live human. H_9110 is that first test.

## Design (engine-native, offline, $0 — `state/9110_chat_user_consequence/consequence_loop.hexa`)
- **Corpus (real human dialogue):** `dancinlab/anima-corpus-ko-sns` (HF cache), turn-structured
  Korean SNS dialogue (`사용자:` human turns alternating with `<persona>:` assistant-emit turns).
  `extract_triples.py` (stdlib data-plumbing only — grep-gate clean) slices it into
  (context C, assistant-emit E, real human next-response R). **R = a real person's reaction to E in
  context C ⇒ EXOGENOUS** (not derivable from anima state). N=119 triples.
- **emit-appropriateness A** (live core): build `immune_memory_new_text(C)`, then
  A = margin(off-topic control emit) − margin(real emit) via `immune_memory_recall_margin_text`
  (core/engine_cli.hexa — engine's OWN L2 affinity). feats (D=4) = [A, emit_len_norm, ctx_len_norm,
  real_margin_norm].
- **consequence a_real** = engagement of the REAL human R = clip01(0.5 + 0.35·len_norm + 0.15·pos −
  0.15·repair), pos/repair = byte-substring marker counts (고마/좋/재밌/ㅋ/!/… vs ?/무슨/모르/…).
- **autogenous a_auto** = H_9104 self-relief: margin drop from binding E into a self store built from
  C (margin_before − margin_after), NO human.
- **V** = `brain.vbasal` delta-rule value lane (READ-only w.r.t. substrate/Ψ, a_substrate_disjoint).
- **Held-out:** first 60% TRAIN (V learns feats→a_real online) → FREEZE → correlations on last 40%.

## Falsifier (PRE-REGISTERED, FROZEN — PREREG.md, no post-hoc move, c9)
- **D_real** = corr(V(feats_test), a_real_test) — real human pairing
- **D_surrogate** = corr(V(feats_test), a_shuf_test) — turn-shuffled human (exogenous coupling destroyed)
- **autogenous** = corr(a_auto_test, a_real_test) — is the human response self-derivable? (floor)
- **PASS 🟢 iff (D_real − D_surrogate ≥ 0.15) AND (|autogenous| < 0.05).** Else 🔴 CEILING (chat-user
  joins the 4 self-contained axes = DPI deeper than receiver-type). Honest both directions.

## Harness (engine-native — grep-gate clean; the only `.py` is stdlib triple-plumbing, NO torch/numpy/gauge_lib)
Imports live `core/pure_field.hexa` (`pure_field_warmup/step/phi`, Φ + Ψ guard) + `core/engine_cli.hexa`
(`immune_memory_new_text/bind_text/recall_margin_text`) + `core/brain.hexa` (`vbasal_new/update/go_value`).
Frozen bars in `PREREG.md` set BEFORE the run (0.15 / 0.05, not moved — c9). A first (buggy) run had
`D_real == D_surrogate` from array-aliasing (`a_shuf_test = a_real_test` shared the array); fixed with
a deep-copy before the Fisher-Yates shuffle (correctness fix, bar unchanged) and re-run.

## Result (engine-native, mini local hexa v0.574.1, `hexa run` RC=0, core/ = origin/main HEAD 59d3fce07, engine_cli sha 7617b135…, NO numpy grep-clean)
`state/verdicts/9110_chat_user_consequence/H_9110.txt` (verbatim) · raw `state/9110_chat_user_consequence/run_mini.log`.

N=119 · n_train=71 · n_test=48. mean emit-appropriateness A = **0.01541** (near-floor). a_real
mean=0.63017 std=0.12538 · a_auto mean=0.91606 std=0.08622.

| quantity | value | bar | pass? |
|---|---|---|---|
| D_real = corr(V(feats_test), a_real_test) | **−0.06627** | — | — |
| D_surrogate = corr(V(feats_test), a_shuf_test) | **0.12185** | — | — |
| **D_real − D_surrogate** | **−0.18812** | ≥ 0.15 | **FAIL** |
| autogenous = corr(a_auto_test, a_real_test) | **0.15013** | \|·\| < 0.05 | **FAIL** |
| Ψ psi_sum ON==OFF | 33.47061690777462 byte-identical | — | OK |

## Honest verdict (c9, bar frozen, NO tune-to-green, NO post-hoc move)
🔴 **CEILING / DPI.** Two converging facts:
1. **D_real − D_surrogate = −0.188 (≪ 0.15).** V's frozen held-out prediction correlates with the
   REAL human response *worse* than with a randomly re-paired one — the real emit→human coupling gave
   NEGATIVE advantage. The engine's emit-appropriateness signal latched onto NO exogenous faculty.
2. **autogenous = 0.150 (> 0.05).** Anima's self-manufactured consequence (no human) already correlates
   0.15 with the real human consequence = the human response is partially self-derivable = the H_9104
   self-loop tautology re-appears at the chat-user layer.

**Caveat (honest, c9 — re-openable, a_break_the_wall):** the emit-appropriateness signal was itself
near-floor (mean A = 0.0154 — a single-context-line ImmuneMemory store barely separated on-topic from
off-topic emits), so there was little engine signal for the faculty to latch onto (structurally like
H_9108's near-floor 2-anima decode). The frozen bar delivers 🔴 regardless. A STRONGER emit↔
appropriateness coupling (multi-turn context store, live-decode-grounded appropriateness read) is a
re-openable angle — the coupling, not the bar, is the lever. But at this cheapest engine-native
coupling, chat-user is a clean ceiling.

**Answer:** a REAL human dialogue response (exogenous), measured offline engine-native, did NOT open
the emit-appropriateness faculty that the 4 self-contained axes could not — at this coupling it FLOORS
just like them. First offline engine-native exogenous-consequence measurement ⇒ **DPI is deeper than
receiver-type**: chat-user joins autogenous (H_9104) · identity (H_9105) · signaling (H_9108) ·
mitosis (H_9109). The escape, if it exists, requires a stronger emit↔appropriateness coupling, not
merely a real external receiver. Ψ preserved (V read-only) ⇒ RED is not a substrate artifact.
wired=none (RED — a_verified_must_wire N/A). follow-on ING: stronger-coupling chat-user loop
(multi-turn context store / live-decode appropriateness) before declaring receiver-type terminal.
