#!/usr/bin/env python3
"""H_1840 confirmatory CONTROL — same toy but target keys are ADDITIVE (K=A[i]+B[j])
instead of HRR (K=A[i] conv B[j]).

If the toy is a pure algebra-matching screen (generalization comes only from the arm's
operator matching the target's construction, and says NOTHING about whether NL composites
carry that structure), then with additive targets the ADDITIVE arm should now generalize
and the HRR arm should floor — the mirror image of the main run. This makes the
non-transferability caveat rigorous.
"""
import torch, torch.nn.functional as F, json
D, NA, NB, NC, TEMP, STEPS, LR = 64, 10, 10, 100, 0.07, 3000, 5e-3


def circ_conv(u, v):
    return torch.fft.irfft(torch.fft.rfft(u, dim=-1) * torch.fft.rfft(v, dim=-1), n=u.shape[-1], dim=-1)


def build(seed):
    g = torch.Generator().manual_seed(seed)
    A = F.normalize(torch.randn(NA, D, generator=g), dim=-1)
    B = F.normalize(torch.randn(NB, D, generator=g), dim=-1)
    K = F.normalize(torch.stack([A[i] + B[j] for i in range(NA) for j in range(NB)]), dim=-1)  # ADDITIVE target
    pairs = [(i, j) for i in range(NA) for j in range(NB)]
    perm = torch.randperm(NC, generator=g).tolist()
    tr = set(perm[:70])
    ca, cb = set(), set()
    for idx in tr:
        ca.add(pairs[idx][0]); cb.add(pairs[idx][1])
    for idx in perm:
        i, j = pairs[idx]
        if i not in ca or j not in cb:
            tr.add(idx); ca.add(i); cb.add(j)
    ho = [i for i in range(NC) if i not in tr]
    return A, B, K, pairs, sorted(tr), ho


def run(arm, seed, A, B, K, pairs, tr, ho):
    g = torch.Generator().manual_seed(seed + 999)
    Wa = torch.nn.Parameter(0.3 * torch.randn(D, D, generator=g))
    Wb = torch.nn.Parameter(0.3 * torch.randn(D, D, generator=g))
    opt = torch.optim.Adam([Wa, Wb], lr=LR)
    ea = torch.stack([A[pairs[k][0]] for k in tr]); eb = torch.stack([B[pairs[k][1]] for k in tr])
    y = torch.tensor(tr)

    def q(ea, eb):
        u, v = ea @ Wa.T, eb @ Wb.T
        return (u + v) if arm == "additive" else circ_conv(u, v)
    for _ in range(STEPS):
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(F.normalize(q(ea, eb), dim=-1) @ K.T / TEMP, y)
        loss.backward(); opt.step()

    def acc(idxs):
        e1 = torch.stack([A[pairs[k][0]] for k in idxs]); e2 = torch.stack([B[pairs[k][1]] for k in idxs])
        with torch.no_grad():
            pred = (F.normalize(q(e1, e2), dim=-1) @ K.T).argmax(-1)
        return round(float((pred == torch.tensor(idxs)).float().mean()), 3)
    return {"train": acc(tr), "heldout": acc(ho)}


res = {}
print("=== CONTROL: ADDITIVE target K=A+B (mirror sanity) ===")
for s in [7, 4302, 4303]:
    A, B, K, pairs, tr, ho = build(s)
    res[s] = {a: run(a, s, A, B, K, pairs, tr, ho) for a in ["additive", "hrr_bottleneck"]}
    print(f" seed {s}: additive heldout={res[s]['additive']['heldout']:.3f} | "
          f"hrr heldout={res[s]['hrr_bottleneck']['heldout']:.3f}")
json.dump(res, open("toy_control_result.json", "w"), indent=2)
print("EXPECT (if pure algebra-matching): additive generalizes, hrr floors — mirror of main run")
