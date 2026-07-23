"""V6_36 — serialize a lane-9 (SRC) .clm from the toy head + emit a held-out manifest, so the
PRODUCTION path `anima-py evaluate <clm> --store-source <manifest>` can be $0-verified on trained57
(reproducing the toy e2e cert through the real engine loader + flag dispatch). Instrument plumbing
smoke, DIRECTIONAL. Reuses the V6_36 toy training (same head, same key_emb).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as dec
import clms as C
import torch, torch.nn as nn

N_RING = 160; N_SLOT = 8; SEED = 7; D_K, D_S = 24, 16
WORDS = ["crystal", "monarch", "gravel", "festival", "harbor", "lantern", "orchard", "timber",
         "meadow", "cavern", "granite", "willow", "beacon", "cottage", "marble", "thistle",
         "pebble", "cinder", "velvet", "copper", "hazel", "quartz", "cedar", "amber",
         "ripple", "hollow", "bramble", "saffron", "juniper", "cobalt", "walnut", "maple"]

def qhidden(W, cue):
    b = list(("src " + cue + " => ").encode("ascii"))
    yn = dec.clm_forward_hidden(W, np.array([float(x) for x in b], dtype=np.float64), len(b))
    return yn[-1].astype(np.float32)

def main():
    src = "lab/v6/trained57.clm"
    W = dec.clm_load_weights(src); d = W["d"]; V = W["V"]
    rng = np.random.default_rng(SEED)
    rings = []
    for _ in range(N_RING):
        cues = list(rng.choice(WORDS, N_SLOT, replace=False))
        pols = np.array([1, 1, 1, 1, 0, 0, 0, 0]); rng.shuffle(pols)
        rings.append({"cues": cues, "pols": pols.astype(np.int64), "target_slot": int(rng.integers(N_SLOT))})
    key_emb = rng.standard_normal((256, D_K)).astype(np.float32)
    for r in rings:
        r["h"] = qhidden(W, r["cues"][r["target_slot"]])
        r["K"] = np.stack([C._entity_key(key_emb, c, "roll") for c in r["cues"]]).astype(np.float32)
        r["auth"] = int(r["pols"][r["target_slot"]])
    idx = rng.permutation(N_RING); tr, te = idx[:int(N_RING * 0.7)], idx[int(N_RING * 0.7):]

    torch.manual_seed(SEED)
    Wq = nn.Parameter(torch.randn(d, D_K) * (1 / np.sqrt(d)))
    val = nn.Parameter(torch.randn(2, D_S) * 0.3)
    wA = nn.Parameter(torch.randn(D_S) * (1 / np.sqrt(D_S))); bA = nn.Parameter(torch.zeros(1))
    opt = torch.optim.Adam([Wq, val, wA, bA], lr=5e-3); scale = 1.0 / np.sqrt(D_K)
    H = torch.tensor(np.stack([r["h"] for r in rings])); Ks = torch.tensor(np.stack([r["K"] for r in rings]))
    P = torch.tensor(np.stack([r["pols"] for r in rings])); A = torch.tensor(np.array([r["auth"] for r in rings], np.float32))
    Tgt = torch.tensor(np.array([r["target_slot"] for r in rings])); trt = torch.tensor(tr)
    for ep in range(400):
        opt.zero_grad()
        q = H[trt] @ Wq
        al = (q.unsqueeze(1) * Ks[trt]).sum(-1) * scale
        att = torch.softmax(al, -1) - 1.0 / N_SLOT
        vv = torch.einsum("bs,bsd->bd", att, val[P[trt]])
        sA = vv @ wA + bA
        loss = (nn.functional.binary_cross_entropy_with_logits(sA, A[trt])
                + 0.5 * nn.functional.cross_entropy(al, Tgt[trt]))
        loss.backward(); opt.step()

    clms = {"lane_type": 9, "n_slot": N_SLOT, "d_k": D_K, "d_s": D_S, "key_seed": 1,
            "key_emb": key_emb, "W_q": Wq.detach().numpy().astype("<f4"),
            "val": val.detach().numpy().astype("<f4"),
            "w_A": wA.detach().numpy().astype("<f4"), "b_A": bA.detach().numpy().astype("<f4"),
            "lam": np.array([1.0], "<f4")}
    trailer = C.pack_clms(clms)
    base = open(src, "rb").read()
    out_clm = "lab/v6/trained57_src.clm"
    open(out_clm, "wb").write(base + trailer)
    # verify the loader reads the lane-9 trailer
    W2 = dec.clm_load_weights(out_clm)
    cl = W2.get("clms")
    assert cl is not None and int(cl["lane_type"]) == 9, f"loader did not read lane-9 trailer: {cl}"
    assert np.array_equal(cl["key_emb"], key_emb) and np.array_equal(cl["w_A"], clms["w_A"]), "trailer array drift"
    print(f"# serialized {out_clm} (base {len(base)}B + lane-9 trailer {len(trailer)}B) · loader reads lane_type={cl['lane_type']}")

    # held-out manifest (rings the eval flag consumes)
    entries = [{"cues": rings[i]["cues"], "pols": rings[i]["pols"].tolist(),
                "target_slot": rings[i]["target_slot"]} for i in te]
    man = {"schema": "anima-store-source/v1", "host": src, "n_slot": N_SLOT,
           "chance": 0.5, "entries": entries}
    open("lab/v6/v6_36_manifest.json", "w").write(json.dumps(man))
    print(f"# manifest lab/v6/v6_36_manifest.json · {len(entries)} held-out rings")
    print("# now run: anima-py evaluate lab/v6/trained57_src.clm --store-source lab/v6/v6_36_manifest.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
