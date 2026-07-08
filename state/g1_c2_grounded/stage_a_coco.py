#!/usr/bin/env python3
"""C2 Stage-A $0 falsifier (Fable design · FROZEN bars in PREREG below).
Does a NON-TEXT world channel carry held-out-pair combination-MI that the TEXT channel lacks?
Proxy world = COCO object annotations (world-authored co-presentations); text = COCO captions.
Pure counting, no GPU, mini-legal. Downloads COCO annotations if absent.

FROZEN BARS (pre-registered before run):
  A1: >= 20 concrete category pairs with img_cooc >= 20 AND cap_cooc == 0
      (world co-presents, text never both-mentions). <20 → escalate Open Images once; still <20 → KILL.
  A2: of A1 survivors, >= 10 pairs with |PMI_img| >= 0.5 nats, permutation p < 0.01 (1000 shuffles).
  PASS-A = A1 AND A2 met → C2 premise (non-text channel has earned held-out joint-MI) survives → Stage B.
  KILL-A = text already subsumes world joints → C2 dead pre-rig (DPI recurses one level up).
"""
import os, json, math, sys, urllib.request, zipfile, random

HERE = os.path.dirname(os.path.abspath(__file__))
ANN = os.path.join(HERE, "coco_ann")
INST = os.path.join(ANN, "annotations", "instances_val2017.json")   # val first (5k, small); train if needed
CAPS = os.path.join(ANN, "annotations", "captions_val2017.json")
URL = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"

def ensure_coco():
    if os.path.exists(INST) and os.path.exists(CAPS): return
    os.makedirs(ANN, exist_ok=True)
    z = os.path.join(ANN, "ann.zip")
    print("downloading COCO annotations (~250MB)...", flush=True)
    urllib.request.urlretrieve(URL, z)
    with zipfile.ZipFile(z) as f:
        f.extractall(ANN)
    os.remove(z)

def run(inst_path, caps_path, split):
    inst = json.load(open(inst_path))
    caps = json.load(open(caps_path))
    cats = {c["id"]: c["name"] for c in inst["categories"]}   # 80 concrete object categories
    # image -> set of category names present (world-authored co-presentation)
    img_objs = {}
    for a in inst["annotations"]:
        img_objs.setdefault(a["image_id"], set()).add(cats[a["category_id"]])
    # image -> concatenated captions (text channel over same world)
    img_caps = {}
    for a in caps["annotations"]:
        img_caps.setdefault(a["image_id"], []).append(a["caption"].lower())
    names = sorted(cats.values())
    from itertools import combinations
    img_cooc = {}; cap_cooc = {}; a_ct = {n: 0 for n in names}
    imgs = list(set(img_objs) | set(img_caps))
    for im in imgs:
        objs = img_objs.get(im, set())
        for n in objs: a_ct[n] += 1
        capt = " ".join(img_caps.get(im, []))
        for A, B in combinations(sorted(objs), 2):
            img_cooc[(A, B)] = img_cooc.get((A, B), 0) + 1
            # cap_cooc: both category words appear in this image's captions
            if A in capt and B in capt:
                cap_cooc[(A, B)] = cap_cooc.get((A, B), 0) + 1
    N = len(imgs)
    # A1
    a1 = [(p, img_cooc[p], cap_cooc.get(p, 0)) for p in img_cooc
          if img_cooc[p] >= 20 and cap_cooc.get(p, 0) == 0]
    # A2: PMI over image co-presence (marginals = a_ct), permutation null
    def pmi(A, B, co):
        pa, pb, pab = a_ct[A]/N, a_ct[B]/N, co/N
        return math.log(pab/(pa*pb)) if pa*pb > 0 and pab > 0 else 0.0
    rng = random.Random(6185)
    a2 = []
    for (A, B), co, _ in a1:
        v = pmi(A, B, co)
        if abs(v) >= 0.5:
            # permutation p: shuffle which images have B among images, preserve marginals
            null = []
            b_imgs = [im for im in imgs if B in img_objs.get(im, set())]
            a_imgs = set(im for im in imgs if A in img_objs.get(im, set()))
            for _ in range(1000):
                s = rng.sample(imgs, len(b_imgs))
                nco = sum(1 for im in s if im in a_imgs)
                null.append(nco)
            p = sum(1 for x in null if x >= co) / len(null)
            if p < 0.01:
                a2.append(((A, B), round(v, 3), co, p))
    out = dict(split=split, n_images=N, n_pairs_cooc=len(img_cooc),
               A1_count=len(a1), A1_bar=20, A1_examples=[(f"{A}|{B}", ic, cc) for (A, B), ic, cc in a1[:15]],
               A2_count=len(a2), A2_bar=10, A2_examples=[(f"{A}|{B}", v, co, p) for (A, B), v, co, p in a2[:15]])
    passA = len(a1) >= 20 and len(a2) >= 10
    out["verdict"] = ("🟢 PASS-A (non-text channel carries held-out joint-MI text lacks → Stage B)" if passA
                      else f"🔴 KILL-A (A1={len(a1)}<20 or A2={len(a2)}<10 → text subsumes world joints, C2 dead pre-rig)")
    return out

if __name__ == "__main__":
    ensure_coco()
    r = run(INST, CAPS, "val2017")
    print(json.dumps(r, indent=2, ensure_ascii=False))
    open(os.path.join(HERE, "stage_a_RESULT.json"), "w").write(json.dumps(r, indent=2, ensure_ascii=False))
