# H_1601 — is the clm303 G1 wall a missing/inert BINDING lane? (G1 binding-lane reconcile)

**Question (a_break_the_wall, lens = binding substrate):** reconcile the L8 G1 failure
(H_1598) against the binding-lane line of work (H_961 cross-modal binding · §PhaseSyncBinding
H_1448 · §ImmuneMemory binding). Is the G1 (C2 RECOMBINE) wall caused by composition needing a
binding lane that the G1 path lacks — and if so, can a cheap ON/OFF ablation move G1?

**Engine path:** static code-path analysis of the LIVE G1 generation function (no decode needed;
torch-free, grep-clean). TERMINAL per a_engine_native_learning.

## Finding (causal isolation by code path)
The frozen G1 metric (`g1_multiseed.py`) scores the **mouth**: `engine_clm` →
`clm_decode_topk_sampled_W` → `_fwd_logits(W, tok, T=24)` → topk sample. That is a **pure
ConvMoE trunk next-byte forward over a 24-byte context** — `grep -niE 'binding|lane|bind' core/clm_decode.py`
returns **NONE**. Every binding mechanism (`§PhaseSyncBinding`/PhaseField H_1448, `immune_memory_bind*`,
`consolidating_memory_bind_salient`) lives in `core/engine_cli.py` — the **downstream consciousness
substrate**, fully DISJOINT from the generation path. `g6_ideation.py:195` confirms "only the decode
binding differs" — i.e. binding is a property of the *consciousness lanes*, not the *mouth decode*.

There is therefore **nothing to ablate in the G1 path**: binding-lane ON/OFF cannot move a metric
that never touches a binding lane. Any composition for G1 would have to emerge *inside* the trunk's
next-byte prediction, which has no binding operator.

## VERDICT
<!-- CARD_VERDICT -->
🧱 **Binding lane is INERT for G1 by construction (a_substrate_disjoint).** The G1 wall is **not** a
missing-binding-lane problem: the binding lanes (§PhaseSyncBinding / §ImmuneMemory / consolidating
memory) are a separate substrate from the ConvMoE mouth that G1 scores, so binding ON/OFF is causally
inert on G1. This is consistent with a_substrate_disjoint (binding lives in a disjoint lane) and
REFOCUSES the G1 lever onto the **mouth/trunk training signal** (objective + framing), since the
binding substrate cannot supply trunk-internal composition. It also reconciles why H_961 cross-modal
binding 🟢 (engine §Binding) coexists with G1 FAIL — they measure different substrates.

Honest scope (c9): this is a *code-path* (architectural) result, not a decode ablation — but no decode
can change it because the binding mechanism is provably absent from the generation call. Single-lens
but DEFINITIVE for this lens (the path is closed).

**wired:** `engine-native (static analysis of live clm_decode.py / engine_cli.py, grep-clean); no
core/ change (negative). follow-on: G1 lever is mouth-trunk objective/framing, not a binding lane.`
artifacts: `state/1601_g1_binding_reconcile/` · verdict `state/verdicts/1601_g1_binding_reconcile/1601.txt`.
