"""Build the --ground-probe manifest: the H_9303 stimulus, now fed to the ENGINE.

Same atoms, same taught carrier, same canonical render()/NEG_FORMS, same corpus-mined eojeol —
nothing about the science changes. What changes is WHO reads it: the readout moves out of an
ad-hoc script in state/ and into `anima-py evaluate --ground-probe`, so the whole verdict path
(forward AND readout AND positive control AND null) is engine-native (a_engine_native_learning ·
a_eval_py_canonical · a_verified_must_wire).
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nbind_curriculum"))
sys.path.insert(0, HERE)
import gen_nbind as GN
import gen_nbindg_n2 as GN2

CARRIER = "이 영화"

rows = GN2.load_corpora()
meta = json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
stems = [a["stem"] for a in meta]

# the whole word the corpus actually writes — a bare stem ('이 영화 참 => ') is ungrammatical and
# half-kills the probe (V-LIVE 0.54 -> 0.81 when this was fixed)
cnt = {s: collections.Counter() for s in stems}
for t, _ in rows:
    for w in t.split():
        if len(w) <= 12:
            for s in stems:
                if s in w:
                    cnt[s][w] += 1
eoj = {s: (cnt[s].most_common(1)[0][0] if cnt[s] else s) for s in stems}

items = []
for a in meta:
    for fid, flip, kind in GN.NEG_FORMS:
        try:
            surf = GN.render(a["stem"], eoj[a["stem"]], CARRIER, kind)
        except Exception:
            continue
        if not surf:
            continue
        items.append({"id": "%s_%s" % (a["stem"], fid),
                      "prompt": "%s %s => " % (CARRIER, surf),
                      "stem": a["stem"], "pol": int(a["pol"]) ^ int(flip),
                      "flip": int(flip), "split": a["split"]})

out = os.path.join(HERE, "ground_manifest.json")
json.dump({"win": 64, "bar": 0.65, "items": items}, open(out, "w"), ensure_ascii=False)
n_h = len({i["stem"] for i in items if i["split"] == "heldout"})
n_t = len({i["stem"] for i in items if i["split"] == "train"})
print("wrote %s · %d prompts · held-out %d atoms / taught %d atoms" % (out, len(items), n_h, n_t))
print("e.g.", [i["prompt"] for i in items[:3]])
