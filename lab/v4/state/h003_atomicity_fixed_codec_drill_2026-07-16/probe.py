import sys, importlib.util, json
sys.argv = ["morph2b.py", "--corpus", "/dev/null"]
spec = importlib.util.spec_from_file_location("morph2b", "/Users/mini/dancinlab/anima/state/nbind_curriculum/morph2b.py")
try:
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
except SystemExit: pass

lines = [l.split("\t")[1] for l in open("/Users/mini/g1_natem/nsmc_ratings_train.txt", encoding="utf-8").read().splitlines()[1:20001] if len(l.split("\t"))>2]
merges = m.train_bpe(lines[:20000], 2048)
merge_rank, tok2id, vocab = m.build_vocab(lines, merges)
out = {"vocab": len(vocab), "merges": len(merges), "stems": {}}
for name, w in [("an","안"),("anh","않"),("mot","못"),("ani","아니")]:
    syms = m.to_jamo(w)
    toks = m.apply_merges(syms, merge_rank)
    out["stems"][name] = {"surface": w, "jamo_n": len(syms), "tokens": toks,
                          "ids": [tok2id.get(t) for t in toks], "atomic": len(toks) == 1}
# Does the (C:ㅇ, V:ㅏ) merge exist, and what else uses it?
out["ca_merge_present"] = ("C:ㅇ\tV:ㅏ" in merge_rank)
json.dump(out, open("/private/tmp/claude-501/-Users-mini-dancinlab-anima-v4/33bbfc0c-35c4-43b3-85b4-abb17a5e233d/scratchpad/probe.json","w"), ensure_ascii=False, indent=2)
print("done")
