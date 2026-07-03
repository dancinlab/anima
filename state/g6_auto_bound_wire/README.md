# g6_score_arm_auto_bound — ByteGPT-capable G6-bind twin (core wiring)

GAP closed (code-only): the H_6186 form-priming-resistant `fals_bound` term existed ONLY in
`g6_score_arm_bound` (CLM-only, hard-codes `gen_clm_ideate`/`g6_decode_best_of_k`). The
canonical `anima evaluate` G6 path is mouth-agnostic
(`cli/evaluate.hexa` `g_eval_g6_seeded_W` → `g6_score_arm_auto_W` → `gen_auto_ideate` →
sniffs ckpt → `.clm` OR ByteGPT) but emitted NO `fals_bound`. So on a ByteGPT ckpt no engine
op produced `fals_bound`. This adds the missing bind twin.

## (a) Implementation — additive, `core/g6_ideation.hexa` (117 insertions, 0 deletions)

Three new `pub fn`, all mouth-agnostic (route through the SINGLE typed L3 entry
`gen_auto_ideate` which sniffs `.clm` vs ByteGPT → ByteGPT-capable):

1. **`g6_decode_best_of_k_auto(ckpt, frame, gen, k, base_seed, known) -> string`** —
   mouth-agnostic twin of the CLM-only `g6_decode_best_of_k`. IDENTICAL best-of-K ranking
   (rng offsets `[0,+101,+202]`, keep max `(fals, kwr)`), decode via `gen_auto_ideate`.

2. **`g6_score_arm_auto_bound(ckpt, frames, frame_pairs, gen, k, base_seed, best_of_k, known) -> Map`** —
   `g6_score_arm_bound`'s EXACT DIST/FALS/`fals_bound` logic re-routed through the mouth-agnostic
   decode entries (`g6_decode_best_of_k_auto` / `gen_auto_ideate`). Returns
   `{ dist, fals, fals_bound, coherent, texts }`.

   **fals_bound term (verbatim from `g6_score_arm_bound`, additive):** inside the frozen
   `_g6_is_falsifiable(o)` branch only, when a measured pair exists for the frame:
   ```
   if _g6_is_falsifiable(o, known) {
       fals = fals + 1                                  // frozen term — byte-identical
       if i < len(frame_pairs) {
           let pr = frame_pairs[i]
           let a = to_int(pr[0]); let b = to_int(pr[1])
           if _g6_topic_bound(o, a, b) { fals_bound = fals_bound + 1 }   // H_6186 AND-add
       }
   }
   ```
   `fals_bound ⊆ fals` by construction (the bind term only AND-adds inside the frozen-fals
   branch) → `dist`/`fals`/`coherent`/`texts` are byte-identical to `g6_score_arm_auto`.
   `_g6_is_falsifiable_topic_bound == _g6_is_falsifiable ∧ _g6_topic_bound` is the H_6186 gate;
   the composed conjunction is inlined here per-frame so the frozen `fals` count is kept
   separately alongside the bind-filtered `fals_bound`.

3. **`g6_build_frame_pairs(n_strong) -> list`** — the MEASURED topic-index pairs for the
   composed frames, VERBATIM the `(a=i%n, b=(i+1+i/n)%n)` rule `g6_build_frames` uses. For
   `n_strong=6`, `n=5`: `[[0,1],[1,2],[2,3],[3,4],[4,0],[0,2]]`. Lets a bind driver pass
   `frame_pairs` without re-deriving the rule.

## (b) `anima evaluate` connection point

Canonical wired path today (frozen, untouched):
```
cli/evaluate.hexa
  g_eval_g6(ckpt)            -> g_eval_g6_seeded_W(gen_auto_load(ckpt), gen, known, 7)
  g_eval_g6_seeded_W(h,...)  -> frames = g6_build_frames(6)["composed"]
                                arm = g6_score_arm_auto_W(h, frames, gen, base_seed, known)
                                -> emits { pass, dist, fals, coherent, frame_leaks }   (NO fals_bound)
```
The bind twin plugs in as an ADDITIVE sibling driver (follow-on, NOT written here — decode-axis
re-score is a pool follow-on per the task):
```
pub fn g_eval_g6_bound_seeded(ckpt, gen, known, base_seed) -> Map {
    let frames = g6_build_frames(6)["composed"]
    let pairs  = g6_build_frame_pairs(6)                       // new helper
    let leaks  = g6_frame_guard(frames, known)
    let arm    = g6_score_arm_auto_bound(ckpt, frames, pairs, gen, 3, base_seed, true, known)
    return #{ "pass": to_int(arm["dist"]) >= 5 && to_int(arm["fals"]) >= 1,
              "dist": to_int(arm["dist"]), "fals": to_int(arm["fals"]),
              "fals_bound": to_int(arm["fals_bound"]),           // <-- H_6186 engine-native
              "coherent": to_int(arm["coherent"]), "frame_leaks": len(leaks), "base_seed": base_seed }
}
```
Because `g6_score_arm_auto_bound` is ckpt-based (matching the existing `g6_score_arm_bound`
signature, not the load-once `_W` variant), it wires at the `g_eval_g6_seeded` (ckpt) level. A
load-once `g6_score_arm_auto_bound_W` twin (mirroring `g6_score_arm_auto_W` over a
`gen_auto_load` handle) is the natural companion if the bind gate is added to the load-once
`g_eval_all` driver — same pattern, follow-on.

## (c) Frozen untouched + hexa check

- **Frozen byte-untouched:** `git diff core/g6_ideation.hexa` = 117 insertions, **0 deletions**.
  `g6_score_arm`, `g6_score_arm_bound`, `g6_score_arm_auto`, `g6_score_arm_auto_W`,
  `_g6_is_falsifiable`, `_g6_topic_bound`, `_g6_is_falsifiable_topic_bound` all called verbatim,
  never modified.
- **`hexa check core/g6_ideation.hexa` → 0 E-errors** (parse + typecheck clean), before and
  after. Full output = `hexa_check.txt`. The 14 reported lines are the implicit **I1
  "deny push" invariant lint** (`found 0 @invariant declaration(s); running implicit I1`), NOT
  compile errors — the file already had 11 such push lines (the established codebase pattern);
  the 3 new lines (653/655/696 = `texts.push`/`word_sets.push` in `g6_score_arm_auto_bound` +
  `pairs.push` in `g6_build_frame_pairs`) are the identical benign pattern. Production gate is
  `hexa verify` (harness.config.json); the cli import closure resolves these fns fine.

## (d) Scope / honesty (c9)

- **GAP code only.** Decode-axis engine-native re-score of the 3 arms
  (TARGETED > SHUF `fals_bound`) on the ByteGPT ckpts is the **pool follow-on** (per
  `state/g6_bind_gate_terminal/` — both pool hosts were infra-walled that session; ckpts
  `h1129.bin`/`g6tc_targeted.bin`/`g6tc_shuf.bin` persist on summer, sha256 in
  `state/g6_targeted_corpus/results/ckpt_manifest.json`).
- No bookkeeping touched (HYPOTHESES / cards / CHANGELOG / ARCHITECTURE / commit / PR).
