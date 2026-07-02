# H_9110 — chat-user EXOGENOUS consequence loop — notes

## What this is
First empirical test of the session's decisive conclusion: the emit-appropriateness
faculty is impossible SELF-CONTAINED (4 axes 🔴 DPI ceiling — autogenous H_9104,
identity H_9105, mitosis H_9109, signaling H_9108). The only remaining escape is a REAL
EXTERNAL receiver. Per the fable EEG verdict (state/eeg_consequence_analysis/EEG_VERDICT.md),
a chat-user is the superior first exogenous loop AND is measurable OFFLINE engine-native:
a real dialogue corpus already contains the human's next response, so the consequence is
exogenous with no live human in the loop.

## Design (engine-native, offline, $0)
- **Corpus**: `dancinlab/anima-corpus-ko-sns` (real turn-structured Korean SNS dialogue,
  `사용자:` human turns alternating with `<persona>:` assistant-emit turns). HF-cached local.
- **Triples**: `extract_triples.py` (stdlib data-plumbing only — grep-gate clean) slices
  the corpus into (context C, assistant-emit E, real human next-response R). R is a real
  person's reaction to E in context C ⇒ EXOGENOUS (not derivable from anima state).
- **emit-appropriateness A** (live core): build `immune_memory_new_text(C)`, then
  A = margin(off-topic control emit) − margin(real emit) via
  `immune_memory_recall_margin_text` (core/engine_cli.hexa, engine's own L2 affinity).
- **feats** (D=4): [A, emit_len_norm, ctx_len_norm, real_margin_norm].
- **consequence a_real** = engagement of the REAL human R = clip01(0.5 + 0.35·len_norm
  + 0.15·pos − 0.15·repair), pos/repair = byte-substring marker counts.
- **autogenous a_auto** = H_9104 self-relief: margin drop from binding E into a self store
  built from C (margin_before − margin_after), NO human.
- **V** = `brain.vbasal` delta-rule value lane (READ-only w.r.t. substrate/Ψ).
- **Held-out**: first 60% TRAIN (V learns feats→a_real online), FREEZE, correlations on
  the last 40% TEST only.

## Frozen falsifier (PREREG.md, bars set pre-measurement)
- D_real = corr(V(feats_test), a_real_test) — real human pairing
- D_surrogate = corr(V(feats_test), a_shuf_test) — turn-shuffled human (coupling destroyed)
- autogenous = corr(a_auto_test, a_real_test) — is the human response self-derivable?
- **PASS 🟢 iff (D_real − D_surrogate ≥ 0.15) AND (|autogenous| < 0.05).**

## Ψ safety (a_substrate_disjoint)
V and all consequence tables are READ-only over the substrate. pure_field psi_sum ON==OFF
byte-identical (V never enters pure_field). emit-drive lane 0/4 · recall_thr untouched.

## Engine-native compliance (a_engine_native_learning)
- Verdict artifact = consequence_loop.hexa importing core/pure_field, core/engine_cli,
  core/brain and calling the LIVE `immune_memory_recall_margin_text` + `vbasal_*` ops.
- grep gate: `grep -lE 'import torch|gauge_lib|numpy' state/9110_chat_user_consequence/*.py`
  → empty (extract_triples.py is stdlib string plumbing only).

## Result (engine-native, mini local hexa v0.574.1, `hexa run` RC=0, core/=origin/main HEAD
## 59d3fce07, engine_cli sha 7617b135…, grep-gate CLEAN)
Verbatim: `state/verdicts/9110_chat_user_consequence/H_9110.txt` · raw `run_mini.log`.

- N=119 triples · n_train=71 · n_test=48 (held-out)
- mean emit-appropriateness A (ctrl_margin − real_margin) = **0.01541** (near-floor — a single
  context-line ImmuneMemory store barely discriminates on-topic vs off-topic emit)
- a_real mean=0.63017 std=0.12538 · a_auto mean=0.91606 std=0.08622

| quantity | value | bar | pass? |
|---|---|---|---|
| D_real = corr(V(feats_test), a_real_test) | **−0.06627** | — | — |
| D_surrogate = corr(V(feats_test), a_shuf_test) | **0.12185** | — | — |
| **D_real − D_surrogate** | **−0.18812** | ≥ 0.15 | **FAIL** |
| autogenous = corr(a_auto_test, a_real_test) | **0.15013** | |·| < 0.05 | **FAIL** |
| Ψ psi_sum ON==OFF | 33.47061690777462 (byte-identical) | — | OK |

**VERDICT: 🔴 CEILING** — chat-user is ALSO a DPI ceiling at this coupling.

### Interpretation (honest, c9)
Two decisive facts, both against the escape:
1. **D_real − D_surrogate = −0.188 (≪ 0.15).** V's frozen held-out prediction correlates with the
   REAL human response *worse* than with a randomly re-paired (turn-shuffled) human response
   (−0.066 vs +0.122). The engine's emit-appropriateness signal captured NO exogenous faculty about
   the real human reaction — the real emit→human coupling gave negative advantage.
2. **autogenous = 0.150 (> 0.05).** Anima's self-manufactured consequence a_auto (H_9104 self-relief,
   NO human) correlates 0.15 with the real human consequence — the human response is *partially
   self-derivable*, so the H_9104 self-loop tautology re-appears at the chat-user layer.

### Caveat (c9, re-openable angle — a_break_the_wall; the COUPLING is the lever, not the bar)
The emit-appropriateness signal itself was near-floor (mean A = 0.0154) — a single-context-line
ImmuneMemory store barely separated on-topic from off-topic emits, so there was little engine signal
for the faculty to latch onto (structurally analogous to H_9108's near-floor 2-anima decode). The
frozen bar delivers 🔴 regardless. A STRONGER emit-appropriateness coupling (multi-turn context store,
a more discriminative engine signal, or a live-decode-grounded appropriateness read) could re-expose
exogenous variance — but at THIS cheapest engine-native coupling, chat-user is a clean ceiling.

### Answer to the session question
Real human dialogue response (exogenous) did NOT open the emit-appropriateness faculty that the 4
self-contained axes could not — at this coupling it FLOORS just like them. So this first empirical
test says **DPI is deeper than receiver-type**: chat-user joins autogenous (H_9104), identity
(H_9105), signaling (H_9108), mitosis (H_9109). The escape, if it exists, needs a *stronger
emit↔appropriateness coupling*, not merely a real external receiver.
