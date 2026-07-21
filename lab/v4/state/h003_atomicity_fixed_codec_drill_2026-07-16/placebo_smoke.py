import importlib.util, sys, os, json
d="/Users/mini/dancinlab/anima-v4/state/h003_atomicity_fixed_codec_drill_2026-07-16"
sys.path.insert(0,d)
import span_policy_encode as sp
m=sp.load_codec()
lines=[l.split("\t")[1] for l in open(os.path.expanduser("~/g1_natem/nsmc_ratings_train.txt"),encoding="utf-8").read().splitlines()[1:20001] if len(l.split("\t"))>2]
merges=m.train_bpe(lines[:20000],2048); merge_rank,tok2id,vocab=m.build_vocab(lines,merges)
JINJJA=m.to_jamo("진짜")  # placebo morpheme jamo
print("진짜 jamo:", JINJJA)
# C-plc vs A-atom: must differ ONLY where 진짜 appears; and NOT differ on 진짜-free lines
has_j=[l for l in lines[:5000] if "진짜" in l][:400]
no_j=[l for l in lines[:5000] if "진짜" not in l and not any(x in l for x in ["안","않","못","아니"])][:400]
d_has=sum(1 for l in has_j if sp.encode(m,l,merge_rank,tok2id,True,placebo_jamo=JINJJA)!=sp.encode(m,l,merge_rank,tok2id,False))
same_noj=all(sp.encode(m,l,merge_rank,tok2id,True,placebo_jamo=JINJJA)==sp.encode(m,l,merge_rank,tok2id,False) for l in no_j)
# CRUCIAL: C-plc must NOT shatter negation (a 진짜-free negation line must be identical A-atom vs C-plc)
neg_lines=[l for l in lines[:5000] if ("지 않" in l or "지않" in l) and "진짜" not in l][:200]
plc_leaves_neg=all(sp.encode(m,l,merge_rank,tok2id,True,placebo_jamo=JINJJA)==sp.encode(m,l,merge_rank,tok2id,False) for l in neg_lines)
print(f"진짜 lines (n={len(has_j)}): C-plc differs from A-atom in {d_has}")
print(f"진짜-free non-neg lines (n={len(no_j)}): all identical = {same_noj}")
print(f"negation-but-진짜-free lines (n={len(neg_lines)}): C-plc leaves them untouched = {plc_leaves_neg}")
ok = d_has>0 and same_noj and plc_leaves_neg
print("VERDICT:", "C-plc placebo CLEAN — shatters 진짜 only, leaves negation and everything else" if ok else "BROKEN")
json.dump({"jinjja_jamo":JINJJA,"jinjja_lines_differ":d_has,"nonneg_free_identical":same_noj,"placebo_leaves_negation":plc_leaves_neg,"clean":ok},
          open(os.path.join(d,"placebo_smoke.json"),"w"),ensure_ascii=False,indent=2)
