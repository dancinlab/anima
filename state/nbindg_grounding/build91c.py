"""Mine each atom's real EOJEOL from the raw corpus, not from the truncated probe contexts.

The previous build read the surface form off gt_prompts, whose contexts are cut right AFTER the
stem — so it recovered the bare stem ('참', '최악이', '아깝') and fed those to render(), producing
ungrammatical carriers ('이 영화 참 => ') that the model never saw. The consequence showed up
exactly where a broken instrument shows up: the shuffle_grid CONTROL out-read both experiment arms.

The eval manifest gets this right because it renders from span_eojeol — the whole word as the corpus
writes it. So mine that: for each atom, take the most frequent eojeol (whitespace token) in the 450k
corpus that contains the stem, then run the canonical render() over it.
"""
import collections, json, os, sys
sys.path.insert(0, os.path.expanduser("~/h9300"))
import gen_nbind as GN
import gen_nbindg_n2 as GN2

rows = GN2.load_corpora()
meta = json.load(open("gt_atoms_n92.json"))["atoms"]
CARRIER = "이 영화"

# most frequent whole word containing the stem — this is the surface the model actually saw
eoj_of = {}
stems = [a["stem"] for a in meta]
cnt = {s: collections.Counter() for s in stems}
for t, _ in rows:
    for w in t.split():
        for s in stems:
            if s in w and len(w) <= 12:
                cnt[s][w] += 1
for s in stems:
    eoj_of[s] = cnt[s].most_common(1)[0][0] if cnt[s] else s

items, out = [], []
for a in meta:
    s, eoj = a["stem"], eoj_of[a["stem"]]
    for fid, flip, kind in GN.NEG_FORMS:
        try:
            surf = GN.render(s, eoj, CARRIER, kind)
        except Exception:
            continue
        if not surf:
            continue
        pid = "R_%s_%s" % (s, fid)
        items.append({"id": pid, "prompt": "%s %s => " % (CARRIER, surf)})
        out.append({"id": pid, "stem": s, "pol": int(a["pol"]) ^ int(flip), "form": fid,
                    "split": a["split"], "eojeol": eoj})

json.dump({"items": items}, open("pos91b_prompts.json", "w"), ensure_ascii=False)
json.dump(out, open("pos91b_meta.json", "w"), ensure_ascii=False)
nh = len({x["stem"] for x in out if x["split"] == "heldout"})
print("built %d prompts · held-out %d atoms / taught %d atoms"
      % (len(items), nh, len({x["stem"] for x in out if x["split"] == "train"})))
print("eojeol e.g.:", [(a["stem"], eoj_of[a["stem"]]) for a in meta[:4]])
print("prompts e.g.:", [i["prompt"] for i in items[:4]])
