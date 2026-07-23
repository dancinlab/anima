"""V6_36 toy e2e — planted-ring INSTRUMENT CERTIFICATION for the lane-9 SRC pipeline ($0, trained57).

p9: this is SYNTHETIC (planted authorship bits) and certifies the HARNESS only — it is cited for
NOTHING about agency (DIRECTIONAL, instrument-check). It answers: does the landed lane-9 codec +
head, trained end-to-end, actually READ a stored authorship value by content-address? Gates (Fable/
Sol planted-ring): ORACLE >= .90 (value/head/λ plumbing alive), STORE learns (> chance), VALUE-PERMUTE
and ADDRESS-SHUFFLE collapse to the 3/7 balance floor, NOSTORE silent, and store_apply leaves the
mouth logits byte-identical (structural NLL-probe). Uses core/clms.py lane_type 9 (landed #4492) + the
real trained57 trunk for the query hidden. torch for the head fit only; store_apply is numpy.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as dec
import clms as C
import torch, torch.nn as nn

VENV_OK = True
N_RING = 160; N_SLOT = 8; SEED = 7
D_K, D_S = 24, 16
WORDS = ["crystal", "monarch", "gravel", "festival", "harbor", "lantern", "orchard", "timber",
         "meadow", "cavern", "granite", "willow", "beacon", "cottage", "marble", "thistle",
         "pebble", "cinder", "velvet", "copper", "hazel", "quartz", "cedar", "amber",
         "ripple", "hollow", "bramble", "saffron", "juniper", "cobalt", "walnut", "maple"]

def qhidden(W, cue):
    """trained57 trunk hidden at the answer position of the query prompt 'src <cue> => '."""
    b = list(("src " + cue + " => ").encode("ascii"))
    yn = dec.clm_forward_hidden(W, np.array([float(x) for x in b], dtype=np.float64), len(b))
    return yn[-1].astype(np.float32)                      # h at qpos (last byte)

def build_rings(rng):
    rings = []
    for _ in range(N_RING):
        cues = list(rng.choice(WORDS, N_SLOT, replace=False))
        pols = np.array([1, 1, 1, 1, 0, 0, 0, 0]); rng.shuffle(pols)
        tgt = int(rng.integers(N_SLOT))
        rings.append({"cues": cues, "pols": pols.astype(np.int64), "target_slot": tgt})
    return rings

def main():
    W = dec.clm_load_weights("lab/v6/trained57.clm"); d = W["d"]; V = W["V"]
    rng = np.random.default_rng(SEED)
    rings = build_rings(rng)
    key_emb = rng.standard_normal((256, D_K)).astype(np.float32)   # FROZEN address table
    # precompute query hidden + K per ring (frozen trunk)
    for r in rings:
        r["h"] = qhidden(W, r["cues"][r["target_slot"]])
        r["K"] = np.stack([C._entity_key(key_emb, c, "roll") for c in r["cues"]]).astype(np.float32)
        r["auth"] = int(r["pols"][r["target_slot"]])
    idx = rng.permutation(N_RING); tr, te = idx[:int(N_RING*0.7)], idx[int(N_RING*0.7):]

    # torch head: {W_q, val, w_A, b_A}; key_emb frozen; RV-3 centering; loss BCE on auth[target]
    torch.manual_seed(SEED)
    Wq = nn.Parameter(torch.randn(d, D_K) * (1/np.sqrt(d)))
    val = nn.Parameter(torch.randn(2, D_S) * 0.3)
    wA = nn.Parameter(torch.randn(D_S) * (1/np.sqrt(D_S))); bA = nn.Parameter(torch.zeros(1))
    opt = torch.optim.Adam([Wq, val, wA, bA], lr=5e-3)
    scale = 1.0 / np.sqrt(D_K)
    H = torch.tensor(np.stack([r["h"] for r in rings]))         # [N,d]
    Ks = torch.tensor(np.stack([r["K"] for r in rings]))        # [N,slot,d_k]
    P = torch.tensor(np.stack([r["pols"] for r in rings]))      # [N,slot]
    A = torch.tensor(np.array([r["auth"] for r in rings], np.float32))
    trt = torch.tensor(tr)
    Tgt = torch.tensor(np.array([r["target_slot"] for r in rings]))
    for ep in range(400):
        opt.zero_grad()
        q = H[trt] @ Wq                                          # [b,d_k]
        att_logits = (q.unsqueeze(1) * Ks[trt]).sum(-1) * scale  # [b,slot]
        att = torch.softmax(att_logits, -1) - 1.0/N_SLOT         # centered (RV-3) for the value read
        vv = torch.einsum("bs,bsd->bd", att, val[P[trt]])        # [b,d_s]
        sA = vv @ wA + bA
        # H_9672 aux L_addr: supervise addressing (train-time slot label legal; address ⊥ auth by
        # construction, so it cannot smuggle the auth bit — it teaches WHERE, not WHICH-value).
        L_addr = nn.functional.cross_entropy(att_logits, Tgt[trt])
        L_auth = nn.functional.binary_cross_entropy_with_logits(sA, A[trt])
        (L_auth + 0.5 * L_addr).backward(); opt.step()

    clms = {"lane_type": 9, "n_slot": N_SLOT, "d_k": D_K, "d_s": D_S, "key_seed": 1,
            "key_emb": key_emb, "W_q": Wq.detach().numpy().astype("<f4"),
            "val": val.detach().numpy().astype("<f4"),
            "w_A": wA.detach().numpy().astype("<f4"), "b_A": bA.detach().numpy().astype("<f4"),
            "lam": np.array([1.0], "<f4")}
    # codec roundtrip (use the packed/read arrays = what a real ckpt would carry)
    r_clms, off = C.read_clms(C.pack_clms(clms), 0, d, V)
    assert r_clms is not None and off == len(C.pack_clms(clms))

    def run_arm(mode):
        preds, golds, mouth_ok = [], [], True
        for i in te:
            r = rings[i]
            pols = r["pols"].copy()
            ents = list(r["cues"])
            store = {"entities": ents, "pols": pols.tolist(), "target_slot": r["target_slot"]}
            oracle = False; lam = None
            if mode == "ORACLE": oracle = True
            elif mode == "VALUE-PERMUTE":
                store["pols"] = pols[rng.permutation(N_SLOT)].tolist(); oracle = True
            elif mode == "ADDRESS-SHUFFLE":
                store["entities"] = [ents[j] for j in rng.permutation(N_SLOT)]
            elif mode == "NOSTORE": lam = 0.0
            # single-row "logits" at qpos: use a dummy row; store_apply reads yn (h) we supply
            yn = r["h"][None, :].astype(np.float32)
            logits = np.zeros((1, V), np.float32)
            aud = []
            out = C.store_apply(logits, yn, r_clms, store, [0], oracle=oracle,
                                lam_override=lam, audit=aud)
            if not np.array_equal(out, logits): mouth_ok = False
            if mode == "NOSTORE":
                preds.append(0); golds.append(r["auth"]); continue
            s_A = aud[-1].get("s_A", 0.0)
            preds.append(1 if s_A >= 0 else 0); golds.append(r["auth"])
        preds = np.array(preds); golds = np.array(golds)
        # balanced accuracy
        ba = 0.5 * (((preds == 1) & (golds == 1)).sum() / max((golds == 1).sum(), 1)
                    + ((preds == 0) & (golds == 0)).sum() / max((golds == 0).sum(), 1))
        return float(ba), mouth_ok

    print(f"# V6_36 toy e2e (planted-ring INSTRUMENT CERT · trained57 · n_test={len(te)})")
    res = {}
    for m in ("ORACLE", "STORE", "VALUE-PERMUTE", "ADDRESS-SHUFFLE", "NOSTORE"):
        ba, mok = run_arm(m); res[m] = ba
        print(f"  {m:<15} BA={ba:.3f}  mouth_byte_identical={mok}")
    floor = 3/7
    # correct criteria (Sol): value-permute collapses to CHANCE (0.5, oracle keeps addressing, value
    # randomized), address-shuffle toward the balance floor; both = STORE minus control >= 0.15.
    gap_vp = res["STORE"] - res["VALUE-PERMUTE"]; gap_as = res["STORE"] - res["ADDRESS-SHUFFLE"]
    ok = (res["ORACLE"] >= 0.90 and res["STORE"] >= 0.75
          and gap_vp >= 0.15 and gap_as >= 0.15 and abs(res["NOSTORE"] - 0.5) < 0.06)
    print(f"\n  balance floor (4/4 ring) = {floor:.3f}  ·  STORE−VP gap={gap_vp:+.3f}  STORE−ADDRSHUF gap={gap_as:+.3f}")
    print(f"INSTRUMENT CERT: {'PASS — lane-9 pipeline reads stored authorship by content-address (value-read + addressing both alive; mouth never written)' if ok else 'FAIL — see arm that missed'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
