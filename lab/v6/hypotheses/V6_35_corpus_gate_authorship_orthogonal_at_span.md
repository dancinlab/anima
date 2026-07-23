<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_35 — the $0 ABORT gate PASSES: a difficulty-orthogonal authorship signal EXISTS at the SPAN level

**origin:** V6_34 closed the mouth/emit channel (difficulty-complete) and named the one live path —
route a faculty through the NON-mouth content-addressed store lane (H_9775, WIRED in-vivo). Before
spending a 303M pool fire, this card runs the $0 precondition gate that decides whether the fire is
even warranted. DIRECTIONAL. Reconciled Fable+Sol (lab full):
- Fable: the store only helps if the SELF/OTHER authorship tag is difficulty-orthogonal; else it
  re-encodes difficulty (= V6_33 rebuilt). This is a $0 CORPUS question with ABORT authority over the
  fire. ADOPTED (minus the vacuous toy-KV-store step).
- Sol (dissent, recorded): a toy KV-store passes by construction (H_9775 proved addressed bits
  travel), so only a 303M fire is decisive — but Sol's own pre-mortem concedes even a clean pass is
  "episodic source-memory," not agency, and V6_32 already read authorship-beyond-difficulty at ΔAUC
  +0.041 (immaterial). So the $0 orthogonality gate legitimately gates the spend.

## Gate (all $0, natural held-out, reuses V6_32/33 SELF/OTHER spans)
SELF span = trained57's temperature-sampled continuation of a natural prefix (auth=1); OTHER = the
true natural continuation (auth=0). Per span: difficulty features [mean NLL, entropy, margin, len]
and the mean trunk hidden (content ceiling). A1 NLL-balance TOST · A2 orthogonality
ΔAUC = AUC(content) − AUC(difficulty) · A3 the DECISIVE arm: re-measure ΔAUC on a
**difficulty-matched** subsample (bin by NLL decile, equalize SELF/OTHER per bin) — does the
orthogonal signal survive matching (Fable's pre-mortem: the address itself may leak difficulty)? +
a label-shuffle control (verdict-integrity: a spend-authorizing positive needs its null).

## RESULT — 🟢 GATE-PASS (matched-ΔAUC +0.161, shuffle-clean)
| test | value |
|---|---|
| A1 NLL-balance | self 1.818 vs other 1.927, diff −0.109 → NOT balanced (SELF spans easier) |
| A2 orthogonality | AUC(difficulty) 0.646 · AUC(content) 0.784 · ΔAUC **+0.138** |
| **A3 difficulty-MATCHED** (n=498, NLL diff −0.019 balanced) | AUC(diff) 0.596 · AUC(content) 0.757 · **matched-ΔAUC +0.161** |
| shuffle control | matched-ΔAUC(shuffled labels) **−0.010 → CLEAN (collapses)** |

After difficulty-matching (SELF/OTHER NLL balanced to 0.019 nat), the trunk-hidden content ceiling
still decodes authorship at 0.757 vs difficulty-only 0.596 — a **material +0.161 difficulty-orthogonal
authorship signal SURVIVES**, and the label-shuffle null collapses it to −0.010 (clean). So the
signal is real, not a difficulty confound or a capacity artifact.

## Reading — the mouth couldn't use it, but it EXISTS at span level
This is the OPPOSITE of the mouth-channel reads: V6_32 measured authorship-beyond-difficulty at the
POSITION level (ΔAUC +0.041, immaterial — where the emit gate decides), and V6_34 showed the emit
channel is difficulty-complete. But aggregated over a whole SPAN (the mean trunk hidden across ~80
bytes), authorship carries a material orthogonal signal (+0.161). The mouth reads position-by-position
and erases it; a content-addressed store reads back a span-level VALUE by address — exactly the shape
that could carry this signal. **So the redesign arc does NOT end in universal closure:** the mouth
channel is closed, but a real difficulty-orthogonal authorship signal exists at the span level that
the store lane might route. The $0 gate did its job — it neither rubber-stamped nor auto-rejected; it
found real orthogonal signal that survives matching + shuffle, so the **303M store fire is WARRANTED.**

## Scope + the honest caveat (both models)
$0 numpy, trained57 byte-LM, span-level. DIRECTIONAL. GATE-PASS warrants ONE bounded 303M pool fire
(Sol's STORE-SOURCE: warm-start H_9775 ckpt, freeze trunk+mouth, train a store agency head, arms
STORE/DRIVER-HIST/TIMER/ADDRESS-ONLY/VALUE-PERMUTE/ADDRESS-SHUFFLE/NOSTORE/ORACLE-SLOT; ~$6.20 rental
cap / $0 owned-pool; DRIVER-HIST the load-bearing null; value-permute necessary-but-insufficient;
NLL-probe must FAIL). Caveat both insisted on: the content signal here is likely model-style vs
natural-style = SOURCE identity; even a clean fire PASS proves "store-routed source memory," NOT
action-selection/ownership/agency — a later unlabeled causal-credit test is required before claiming
AGENCY. But the precondition is met: the label is not a pure difficulty shadow. Artifact:
`v6_35_corpus_gate.py`. Next: the gated 303M STORE-SOURCE fire (engine-native, anima-py, pool).
