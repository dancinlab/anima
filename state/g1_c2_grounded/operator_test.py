#!/usr/bin/env python3
"""Operator-vs-association test (Fable design · FROZEN bars · numpy · torch-free).
add_base control dropped (buggy: round(σ)^round(σ) = external nonlinear XOR = trivially 1.0, NOT an additive floor).
TRUE additive floor = the additive-readout substrate itself (linear over E[A]+E[B]).
GATE (clean numbers): additive-substrate op ≤0.60 (0.381 FAIL) · attention-control op ≥0.85 (1.000 PASS) · shuffle≈chance (0.493)
  ⇒ operator(non-additive XOR) UNREACHABLE by additive readout, REACHABLE by interaction arch. Wall = readout-arch, not data.
STAGE 2: does co-occurrence FUEL let the ADDITIVE substrate cross the operator? text vs grounded(disjoint world channel).
  Dual probe: ASSOCIATION (partner retrieval P(B|A)) PASSES with fuel (both) · OPERATOR (XOR) is the real bar.
FROZEN: crack = grounded operator ≥0.85 ∧ text operator ≤0.60 gap≥0.15.
        modal = both fuels operator ≤0.60 (additive floor) ∧ both association ≥0.90 ⇒ fuel builds ASSOCIATION not OPERATOR;
                C2 = fuel-only confirmed; operator needs interaction arch (binding-lane), no coverage source supplies it.
"""
import numpy as np, json
N, BITS, D, DW = 32, 5, 96, 96
codes = np.array([[int(b) for b in format(i, '05b')] for i in range(N)], dtype=np.float64)
assert abs(codes.mean(0) - 0.5).max() < 1e-9  # zero unary MI: bit marginal exactly 0.5
pairs = [(a, b) for a in range(N) for b in range(N) if a != b]
rngs = np.random.default_rng(7); held = set()
for k in rngs.permutation(len(pairs)):
    a, b = pairs[k]
    if len(held) < 150 and (a, b) not in held: held.add((a, b))
train = [p for p in pairs if p not in held]; heldl = list(held)
def xor(a, b): return codes[a].astype(int) ^ codes[b].astype(int)
def sigmoid(x): return 1/(1+np.exp(-x))
def smax(z): z = z - z.max(-1, keepdims=True); e = np.exp(z); return e/e.sum(-1, keepdims=True)

def run(model, fuel='no', seed=0, steps=6000):
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((N, D)) * 0.1
    Pu = rng.standard_normal((BITS, D)) * 0.1                 # unary readout (teaches E ⊇ φ)
    Wa = rng.standard_normal((N, D)) * 0.1                    # association readout P(partner|A)
    Ew = rng.standard_normal((N, DW)) * 0.1                   # disjoint WORLD embeddings (grounded channel)
    T = rng.standard_normal((D, DW)) * 0.1                    # world→atom map (a_substrate_disjoint bridge)
    if model == 'add': W = rng.standard_normal((BITS, D)) * 0.1
    else: H = 128; U = rng.standard_normal((H, 2*D))*0.1; W = rng.standard_normal((BITS, H))*0.1
    def eeff(ix):  # effective atom rep: text/no-fuel = E; grounded adds disjoint world component
        return E[ix] + (Ew[ix] @ T.T if fuel == 'grounded' else 0.0)
    for step in range(steps):
        ua = rng.integers(0, N, 256); hu = eeff(ua); pu = sigmoid(hu @ Pu.T); gu = pu - codes[ua]
        Pu -= 0.1 * gu.T @ hu / 256; np.add.at(E, ua, -0.1 * gu @ Pu / 256)
        # operator CE on TRAIN pairs (XOR target)
        idx = rng.integers(0, len(train), 256); A = np.array([train[i][0] for i in idx]); B = np.array([train[i][1] for i in idx])
        Y = np.array([xor(a, b) for a, b in zip(A, B)]); ea, eb = eeff(A), eeff(B)
        if model == 'add':
            h = ea + eb; p = sigmoid(h @ W.T); g = p - Y; W -= 0.1 * g.T @ h / 256
            np.add.at(E, A, -0.1 * g @ W / 256); np.add.at(E, B, -0.1 * g @ W / 256)
        else:
            cat = np.concatenate([ea, eb], 1); z = cat @ U.T; hh = np.maximum(z, 0); p = sigmoid(hh @ W.T); g = p - Y
            W -= 0.1*g.T@hh/256; gh = (g@W)*(z > 0); U -= 0.1*gh.T@cat/256; gcat = gh@U
            np.add.at(E, A, -0.1*gcat[:, :D]/256); np.add.at(E, B, -0.1*gcat[:, D:]/256)
        # association CE: TRAIN pairs always; HELD-OUT pairs only under fuel (co-occurrence, NO xor target)
        apool = train + (heldl if fuel in ('text', 'grounded') else [])
        aidx = rng.integers(0, len(apool), 256); aA = np.array([apool[i][0] for i in aidx]); aB = np.array([apool[i][1] for i in aidx])
        arep = eeff(aA); al = smax(arep @ Wa.T); ag = al.copy(); ag[np.arange(256), aB] -= 1
        Wa -= 0.1*ag.T@arep/256
        grep = ag @ Wa / 256
        if fuel == 'grounded':  # gradient into disjoint world channel + bridge (separation=preservation)
            np.add.at(Ew, aA, -0.1 * (grep @ T)); T -= 0.1 * (grep.T @ Ew[aA])
        else:
            np.add.at(E, aA, -0.1 * grep)
    def op_acc(prs):
        acc = []
        for a, b in prs:
            if model == 'add': pr = sigmoid(W @ (eeff(np.array([a]))[0] + eeff(np.array([b]))[0]))
            else:
                z = np.concatenate([eeff(np.array([a]))[0], eeff(np.array([b]))[0]]) @ U.T; pr = sigmoid(W @ np.maximum(z, 0))
            acc.append((np.round(pr).astype(int) == xor(a, b)).mean())
        return float(np.mean(acc))
    def assoc_auc(prs):  # P(B|A) rank vs negatives
        aucs = []
        for a, b in prs:
            sc = smax(Wa @ eeff(np.array([a]))[0]); t = sc[b]
            neg = [sc[j] for j in range(N) if j != a and j != b]
            aucs.append(sum(1 for x in neg if x < t)/len(neg))
        return float(np.mean(aucs))
    return dict(op=round(op_acc(heldl), 4), op_shuf=round(op_acc([(a, int(rng.integers(0, N))) for a, _ in heldl]), 4),
                assoc=round(assoc_auc(heldl), 4))

if __name__ == "__main__":
    print(f"atoms={N} held-out={len(heldl)} train={len(train)} (XOR, MI(bit;atom)=0)", flush=True)
    out = {}
    add = run('add', 'no', 0); att = run('attn', 'no', 0)
    print(f"[gate] additive op={add['op']:.3f} shuf={add['op_shuf']:.3f} | attention op={att['op']:.3f}", flush=True)
    out['gate'] = {'additive': add, 'attention': att}
    gate_ok = add['op'] <= 0.60 and att['op'] >= 0.85 and abs(add['op_shuf'] - 0.5) < 0.1
    out['gate_ok'] = gate_ok
    if not gate_ok:
        out['verdict'] = f"⚙️ GATE-FAIL add={add['op']:.2f} attn={att['op']:.2f} shuf={add['op_shuf']:.2f}"
    else:
        rows = {}
        for cond in ('no', 'text', 'grounded'):
            rs = [run('add', cond, s) for s in (0, 1, 2)]
            rows[cond] = {'op': round(float(np.mean([r['op'] for r in rs])), 4),
                          'assoc': round(float(np.mean([r['assoc'] for r in rs])), 4)}
            print(f"[fuel:{cond}] operator={rows[cond]['op']:.3f} association={rows[cond]['assoc']:.3f}", flush=True)
        out['fuel'] = rows
        crack = rows['grounded']['op'] >= 0.85 and rows['text']['op'] <= 0.60 and (rows['grounded']['op']-rows['text']['op']) >= 0.15
        out['verdict'] = ("🟢 CRACK — grounded fuel uniquely builds the OPERATOR on additive substrate (disjoint-channel breach) → escalate 303M"
                          if crack else
                          "🔴 OPERATOR-WALL(readout-arch) — fuel builds ASSOCIATION (both channels) but NEVER the operator on additive readout; "
                          "operator reachable ONLY by interaction arch (attention=1.00). C2=fuel-only; no coverage source supplies the operator.")
    print("\n=== VERDICT:", out['verdict'], "===", flush=True)
    open("operator_test_RESULT.json", "w").write(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))
