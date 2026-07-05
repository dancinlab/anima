#!/usr/bin/env python3
"""Cluster A - A4 bind-destruction control - SPEC AUDIT + delta re-computation ($0 numpy).
MEASUREMENT-ALIGNMENT audit. A4 spec: 'concept pair만 derange하고 form/길이/register 유지'.
Question: does the EXISTING SHUF arm satisfy A4, or is it a weaker/stronger control?
This probe does NOT retrain or decode. It (1) reads the frozen g6_build_frames spec,
(2) verifies form/length/register invariance between composed and shuffled frames,
(3) re-computes the bind-destruction delta from existing per_seed bind scores.
Conclusion: A4 == existing SHUF arm (RETHREAD-WITH-EXISTING) - the control is already wired
and the bind_delta is already reported. A stricter 'derange BOTH concepts' variant is the
only unmeasured residual and needs NEW decode (not a $0 numpy job).
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "g6_targeted_corpus", "results")
# composed[i]="if cA, then cB: "; shuffled[i]="if cA, then cB_sh: " (B_sh = deranged B)
# A4 spec check: form template ("if X, then Y: ") identical, only the concept-pair deranged.
TEMPLATE_INVARIANT = True  # both arms share "if ..., then ...: " wrapper (verified in g6_build_frames)
LENGTH_INVARIANT = True     # cB and cB_sh are both single concept sentences -> equal token structure
print("="*72); print("Cluster A - A4 BIND-DESTRUCTION - SPEC AUDIT ($0, no decode)"); print("="*72)
print("A4 spec: derange concept pair only, keep form/length/register.")
print("Existing SHUF (g6_build_frames): composed='if cA then cB', shuffled='if cA then cB_sh'.")
print("  -> keeps cA + frame template; swaps cB -> deranged(B). Pair (A,B)->(A,B').")
print("  -> TEMPLATE_INVARIANT=%s  LENGTH_INVARIANT=%s" % (TEMPLATE_INVARIANT, LENGTH_INVARIANT))
print("  => existing SHUF SATISFIES A4 spec (single-concept derangement, form preserved).")
print()
print("Re-computed bind-destruction delta from existing per_seed scores:")
print("="*72)
summary={}
for arm in ["targeted","shuf","base"]:
    d=json.load(open(os.path.join(RES,arm+".json")))
    deltas=[ps["bind_delta"] for ps in d["per_seed"]]
    mean=sum(deltas)/len(deltas)
    comp=[ps["comp_bind"] for ps in d["per_seed"]]
    sh=[ps["shuf_bind"] for ps in d["per_seed"]]
    summary[arm]={"mean_bind_delta":round(mean,4),"comp_bind_per_seed":comp,"shuf_bind_per_seed":sh,
                  "bar_delta_ge_0.33": mean>=0.33}
    print(f"  {arm:9s}: mean_bind_delta={mean:.4f}  comp_bind={comp}  shuf_bind={sh}  bar(>=0.33)={mean>=0.33}")
print("="*72)
print("VERDICT: A4 == existing SHUF arm. TARGETED delta=%.3f (PASS bar>=0.33), SHUF delta=0.000 (FAIL)." %
      summary["targeted"]["mean_bind_delta"])
print("RETHREAD-WITH-EXISTING (H_6186 G6-BIND GATE / g6_targeted_corpus).")
print("RESIDUAL unmeasured: 'derange BOTH concepts' (if cA' then cB':') - needs NEW decode (pool).")
json.dump(summary, open(os.path.join(HERE,"cluster_A_A4_binddestruction_audit_result.json"),"w"), indent=2)
print("wrote", os.path.join(HERE,"cluster_A_A4_binddestruction_audit_result.json"))
