#!/usr/bin/env python3
"""G1 frozen mouth-bind screen — DIRECTIONAL SCREEN (not engine-native terminal).

Three abstract binding mechanism probes (H_1616 VSA/HRR, H_1623 hypernet-mult,
H_1649 saddle) + frozen clm303 G1 measurement with each binding op wired at the
mouth readout (yn → bind_op → readout conv intercept).

Results: state/g1_frozen_mouthbind_screen/RESULT.md + raw_results.json
Honesty: numpy probe = DIRECTIONAL only (a_engine_native_learning §ad-hoc DIRECTIONAL).
"""
from __future__ import annotations
import sys, os, re, time, json
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CLM_DECODE_PATH = os.path.join(REPO, "core")
RESULT_DIR = os.path.dirname(os.path.abspath(__file__))
CLM_PATH = "/Users/mini/anima-weights/clm303_clean/clm303_clean.clm"

# ════════════════════════════════════════════════════════════════════════════════
# PART 1 — Abstract mechanism probes (per card specs, NO 303M weights)
# ════════════════════════════════════════════════════════════════════════════════

def probe_vsa_hrr(seed=42, d=512, K=20, N_bundle=5, n_trials=100, verbose=True):
    """H_1616 cheap test — BUNDLE retrieval test.

    Create N_bundle role-filler bindings, superpose them into a bundle.
    Query: hrr_unbind(bundle, role_j) → should retrieve filler_j (HRR).
    Additive baseline: the bundle is sum(role_i + filler_i), querying loses
    role-filler correspondence at N≥3 (interference).
    Control: random permutation instead of structured circular conv.

    d=512, N=5: SNR ≈ sqrt((d-N)/N) ≈ 10 → clean retrieval expected for HRR.
    For additive at N=5: (sum of roles+fillers) - role_j does NOT isolate filler_j.

    Frozen bar: HRR top-1 acc > additive top-1 acc AND > control top-1 acc.
    """
    rng = np.random.default_rng(seed)

    # K atom anchors — approximate unit vectors
    atoms = rng.standard_normal((K, d))
    atoms /= np.linalg.norm(atoms, axis=1, keepdims=True)

    # Generate deterministic permutation for control
    perm = rng.permutation(d)
    inv_perm = np.argsort(perm)

    def hrr_bind(va, vb):
        """Circular convolution: bind(a,b) = ifft(fft(a) * fft(b))."""
        return np.fft.irfft(np.fft.rfft(va) * np.fft.rfft(vb), n=d)

    def hrr_unbind(vab, va):
        """Circular correlation (inverse): ifft(fft(ab) * conj(fft(a)))."""
        return np.fft.irfft(np.fft.rfft(vab) * np.conj(np.fft.rfft(va)), n=d)

    def perm_bind(va, vb):
        """Permutation-based pseudo-binding (NOT properly invertible)."""
        return va[perm] + vb  # permuted a + b

    def perm_unbind(bundle, va):
        """Attempt to unbind permutation binding."""
        # bundle[query] = sum(va_i[perm] + vb_i); this doesn't cleanly isolate vb_j
        return bundle - va[perm]  # residual — but contains interference from other pairs

    def cleanup(query, atom_set):
        """Nearest-atom lookup by cosine similarity."""
        nq = query / (np.linalg.norm(query) + 1e-12)
        sims = atom_set @ nq / (np.linalg.norm(atom_set, axis=1) + 1e-12)
        return int(np.argmax(sims)), float(np.max(sims))

    def additive_bundle_unbind(bundle, role_va):
        """Additive baseline: bundle = sum(role_i + filler_i), recover filler_j."""
        # bundle - role_j = sum_{i≠j}(role_i + filler_i) + filler_j — dirty retrieval
        return bundle - role_va

    def run_trial(trial_seed, bind_fn, unbind_fn):
        """One trial: pick N_bundle random pairs, bundle them, retrieve all."""
        rng_t = np.random.default_rng(trial_seed)
        # Pick N_bundle distinct pairs (i, j) with i≠j
        indices = rng_t.choice(K, N_bundle * 2, replace=False)
        roles   = indices[:N_bundle]
        fillers = indices[N_bundle:]
        # Ensure roles ≠ fillers
        for t in range(N_bundle):
            if roles[t] == fillers[t]:
                fillers[t] = (fillers[t] + 1) % K
        # Create bundle
        bound_items = [bind_fn(atoms[roles[i]], atoms[fillers[i]]) for i in range(N_bundle)]
        bundle = sum(bound_items)  # superposition
        # Retrieve each filler from the bundle by unbing with the role
        hits = 0
        for i in range(N_bundle):
            recovered = unbind_fn(bundle, atoms[roles[i]])
            pred, sim = cleanup(recovered, atoms)
            if pred == fillers[i]:
                hits += 1
        return hits / N_bundle

    hrr_accs = []
    add_accs  = []
    perm_accs = []

    for t in range(n_trials):
        s = seed * 1000 + t
        hrr_accs.append(run_trial(s, hrr_bind, hrr_unbind))
        add_accs.append(run_trial(s, lambda a, b: (a + b), additive_bundle_unbind))
        perm_accs.append(run_trial(s, perm_bind, perm_unbind))

    hrr_mean  = float(np.mean(hrr_accs))
    add_mean  = float(np.mean(add_accs))
    perm_mean = float(np.mean(perm_accs))
    bar_pass  = hrr_mean > add_mean and hrr_mean > perm_mean

    if verbose:
        print(f"  [VSA/HRR bundle N={N_bundle}, K={K}, d={d}]")
        print(f"    ON  (circular conv+unbind):  acc={hrr_mean:.3f}")
        print(f"    OFF (additive bundle):        acc={add_mean:.3f}")
        print(f"    CTRL (perm-bind):             acc={perm_mean:.3f}")
        print(f"    Bar PASS (ON > OFF AND > CTRL): {bar_pass}")

    return {
        "name": "VSA/HRR (H_1616)",
        "ON":   {"acc": hrr_mean},
        "OFF":  {"acc": add_mean},
        "CTRL": {"acc": perm_mean},
        "bar_pass": bar_pass,
        "params": {"d": d, "K": K, "N_bundle": N_bundle, "n_trials": n_trials},
    }


def probe_hypernet_mult(seed=42, d_role=8, d_fill=8, n_roles=6, n_fills=6,
                        n_hidden=32, n_epochs=300, lr=0.05, verbose=True):
    """H_1623 cheap test — multiplicative hypernet vs additive concat-MLP.

    Task: given role r and filler f, predict target = (r*2 + f*3) % n_fills.
    COMPOSITIONAL split: test on unseen (role, filler) combos.

    Hypernet: role_emb → small linear → reshape → W_role; then W_role @ filler_emb → output.
    This is a BILINEAR interaction (role × filler), able to generalize to unseen combos.
    Concat-MLP: concat(role, filler) → linear → output. Additive/linear, memorizes train combos.

    We TRAIN both with gradient descent on train split, then test on held-out combos.
    Frozen bar: hypernet held-out acc > concat-MLP held-out acc (compositionality advantage).
    """
    rng = np.random.default_rng(seed)

    role_emb = rng.standard_normal((n_roles, d_role)) * 0.3
    fill_emb = rng.standard_normal((n_fills, d_fill)) * 0.3

    def gt(r, f): return (r * 2 + f * 3) % n_fills

    # All pairs + compositional split (leave out last filler)
    holdout_fill = n_fills - 1
    all_pairs = [(r, f) for r in range(n_roles) for f in range(n_fills)]
    train_pairs = [(r, f) for r, f in all_pairs if f != holdout_fill]
    test_pairs  = [(r, f) for r, f in all_pairs if f == holdout_fill]

    n_out = n_fills

    # ── Hypernet: role → W_role (d_fill × n_out), apply to filler ──────────
    Wh = rng.standard_normal((d_role, d_fill * n_out)) * 0.05   # role→weight generator
    bh = np.zeros(d_fill * n_out)
    # Readout bias
    b_out = np.zeros(n_out)

    def hyp_fwd(r_idx, f_idx):
        r = role_emb[r_idx]; f = fill_emb[f_idx]
        W_role = (r @ Wh + bh).reshape(d_fill, n_out)  # bilinear role×filler
        return f @ W_role + b_out

    def softmax(x): e = np.exp(x - x.max()); return e / (e.sum() + 1e-12)
    def ce_loss(logits, target):
        p = softmax(logits); return -np.log(p[target] + 1e-12)
    def ce_grad(logits, target):
        p = softmax(logits); p[target] -= 1.0; return p

    # Train hypernet with manual backprop
    for ep in range(n_epochs):
        rng.shuffle(train_pairs)  # not modifying train_pairs, just shuffle
        for r_idx, f_idx in train_pairs:
            r = role_emb[r_idx]; f = fill_emb[f_idx]
            W_role = (r @ Wh + bh).reshape(d_fill, n_out)
            logits = f @ W_role + b_out
            tgt = gt(r_idx, f_idx)
            dloss = ce_grad(logits, tgt)
            # Grad w.r.t. W_role: f[:, None] * dloss[None, :]  → [d_fill, n_out]
            dW_role = np.outer(f, dloss)
            # Grad w.r.t. Wh: r[:, None] @ dW_role.T.reshape(...)
            dWh = np.outer(r, dW_role.ravel())
            dbh = dW_role.ravel()
            db_out = dloss
            Wh   -= lr * dWh
            bh   -= lr * dbh
            b_out -= lr * db_out

    hyp_hits = sum(1 for r, f in test_pairs
                   if int(np.argmax(hyp_fwd(r, f))) == gt(r, f))
    hyp_acc = hyp_hits / len(test_pairs) if test_pairs else 0.0

    # ── Concat-MLP: cat(role, filler) → hidden → n_out ──────────────────────
    Wc = rng.standard_normal((d_role + d_fill, n_hidden)) * 0.05
    bc = np.zeros(n_hidden)
    Wout = rng.standard_normal((n_hidden, n_out)) * 0.05
    bout = np.zeros(n_out)

    def relu(x): return np.maximum(0, x)
    def relu_grad(x): return (x > 0).astype(float)

    def cat_fwd(r_idx, f_idx):
        inp = np.concatenate([role_emb[r_idx], fill_emb[f_idx]])
        h = relu(inp @ Wc + bc)
        return h @ Wout + bout

    for ep in range(n_epochs):
        for r_idx, f_idx in train_pairs:
            inp = np.concatenate([role_emb[r_idx], fill_emb[f_idx]])
            h_pre = inp @ Wc + bc
            h = relu(h_pre)
            logits = h @ Wout + bout
            tgt = gt(r_idx, f_idx)
            dout = ce_grad(logits, tgt)
            dWout = np.outer(h, dout); dbout = dout
            dh = dout @ Wout.T * relu_grad(h_pre)
            dWc = np.outer(inp, dh); dbc = dh
            Wc -= lr * dWc; bc -= lr * dbc
            Wout -= lr * dWout; bout -= lr * dbout

    cat_hits = sum(1 for r, f in test_pairs
                   if int(np.argmax(cat_fwd(r, f))) == gt(r, f))
    cat_acc = cat_hits / len(test_pairs) if test_pairs else 0.0

    bar_pass = hyp_acc > cat_acc

    if verbose:
        n_tr = len(train_pairs); n_te = len(test_pairs)
        print(f"  [Hypernet compositional split] train={n_tr}, test(holdout filler)={n_te}")
        print(f"    ON  (bilinear hypernet):  acc={hyp_acc:.3f} ({hyp_hits}/{n_te})")
        print(f"    OFF (concat-MLP additive): acc={cat_acc:.3f} ({cat_hits}/{n_te})")
        print(f"    Bar PASS (ON > OFF): {bar_pass}")

    return {
        "name": "Hypernet-mult (H_1623)",
        "ON":   {"acc": hyp_acc, "hits": hyp_hits, "total": len(test_pairs)},
        "OFF":  {"acc": cat_acc, "hits": cat_hits, "total": len(test_pairs)},
        "bar_pass": bar_pass,
    }


def probe_saddle_point(seed=42, d=8, n_factors=4, n_roles=3, K_iters=30,
                       lr=0.05, n_trials=50, verbose=True):
    """H_1649 cheap test — minimax saddle vs energy-descent vs linear.

    Ground truth binding: factor f, role r → unique label (f, r).
    Saddle U(a,g) = a@M@g; A minimizes, G maximizes (adversarial coupling).
    At saddle, (a*, g*) encodes (factor, role) jointly via M.
    Ablation: M=0 → separable, no coupling → can't encode joint (factor, role).

    Frozen bar: saddle probe achieves higher accuracy on holdout than energy-descent
    and M-ablated baselines.
    """
    rng = np.random.default_rng(seed)

    # Embeddings for factors (A player) and roles (G player)
    factor_emb = rng.standard_normal((n_factors, d))
    role_emb   = rng.standard_normal((n_roles, d))

    # Coupling matrix M — encodes interaction between factors and roles
    # Designed so A*=factor, G*=role at equilibrium (approximately)
    M = rng.standard_normal((d, d)) * 0.5

    # Ground truth: (factor, role) → category index (all distinct)
    n_classes = n_factors * n_roles
    def gt(f, r): return f * n_roles + r

    # All (factor, role) pairs; hold out last role
    holdout_role = n_roles - 1
    all_pairs    = [(f, r) for f in range(n_factors) for r in range(n_roles)]
    train_pairs  = [(f, r) for f, r in all_pairs if r != holdout_role]
    test_pairs   = [(f, r) for f, r in all_pairs if r == holdout_role]

    def saddle_fwd(f_emb, r_emb, M_use, lr=lr, n_iters=K_iters):
        """Simultaneous gradient steps to saddle of U = a@M@g."""
        a = f_emb.copy(); g = r_emb.copy()
        for _ in range(n_iters):
            ga = M_use @ g          # dU/da = M@g; A descends
            gg = M_use.T @ a        # dU/dg = M.T@a; G ascends
            a = a - lr * ga
            g = g + lr * gg
        return np.concatenate([a, g])   # joint repr of (factor, role)

    def energy_fwd(f_emb, r_emb, M_use, lr=lr, n_iters=K_iters):
        """Both players minimize (cooperative, not adversarial)."""
        a = f_emb.copy(); g = r_emb.copy()
        for _ in range(n_iters):
            a = a - lr * (M_use @ g)
            g = g - lr * (M_use.T @ a)  # G descends too
        return np.concatenate([a, g])

    def linear_fwd(f_emb, r_emb):
        return np.concatenate([f_emb, r_emb])

    def fit_linear_probe(fwd_fn):
        """Fit linear probe on train; eval on test."""
        X_tr = np.array([fwd_fn(factor_emb[f], role_emb[r]) for f, r in train_pairs])
        y_tr = np.array([gt(f, r) for f, r in train_pairs])
        y_one = np.zeros((len(train_pairs), n_classes))
        for i, t in enumerate(y_tr): y_one[i, t] = 1.0
        W, _, _, _ = np.linalg.lstsq(X_tr, y_one, rcond=None)
        hits = 0
        for f, r in test_pairs:
            pred = int(np.argmax(fwd_fn(factor_emb[f], role_emb[r]) @ W))
            if pred == gt(f, r): hits += 1
        return hits / len(test_pairs) if test_pairs else 0.0, hits, len(test_pairs)

    saddle_acc, sh, st = fit_linear_probe(lambda fe, re: saddle_fwd(fe, re, M))
    energy_acc, eh, et = fit_linear_probe(lambda fe, re: energy_fwd(fe, re, M))
    linear_acc, lh, lt = fit_linear_probe(linear_fwd)
    ablat_acc, ah, at_ = fit_linear_probe(lambda fe, re: saddle_fwd(fe, re, np.zeros_like(M)))

    bar_pass = saddle_acc > energy_acc and saddle_acc > ablat_acc and saddle_acc > linear_acc

    if verbose:
        chance = 1.0 / n_classes
        print(f"  [A⇄G Saddle d={d} n_factors={n_factors} n_roles={n_roles}] chance={chance:.3f}")
        print(f"    ON  (minimax saddle):    acc={saddle_acc:.3f} ({sh}/{st})")
        print(f"    CTRL energy-descent:     acc={energy_acc:.3f} ({eh}/{et})")
        print(f"    CTRL linear:             acc={linear_acc:.3f} ({lh}/{lt})")
        print(f"    CTRL M-ablated:          acc={ablat_acc:.3f} ({ah}/{at_})")
        print(f"    Bar PASS (ON > all ctrl): {bar_pass}")

    return {
        "name": "A⇄G Saddle (H_1649)",
        "ON":      {"acc": saddle_acc, "hits": sh, "total": st},
        "energy":  {"acc": energy_acc, "hits": eh, "total": et},
        "linear":  {"acc": linear_acc, "hits": lh, "total": lt},
        "M_ablated": {"acc": ablat_acc, "hits": ah, "total": at_},
        "bar_pass": bar_pass,
    }


# ════════════════════════════════════════════════════════════════════════════════
# PART 2 — Frozen clm303 G1 with mouth-bind ops at readout intercept
# ════════════════════════════════════════════════════════════════════════════════

# G1 metric (frozen VERBATIM from g1_multiseed.py / H_1129 / a7b_pass)
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]
def _words(s): return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
KNOWN = set()
for _c, _kw in CONCEPTS:
    KNOWN |= {w for w in _words(_c)}; KNOWN |= _kw
for _p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
    try:
        with open(_p, errors="ignore") as _f:
            for _w in _f:
                _w = _w.strip().lower()
                if _w.isalpha(): KNOWN.add(_w)
        break
    except OSError: continue
KNOWN |= {"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t"}
def _kwr(text):
    wl = _words(text); return sum(1 for w in wl if w in KNOWN)/len(wl) if wl else 0.0
def _coverage(text):
    wl = set(_words(text)); return [i for i, (_, kw) in enumerate(CONCEPTS) if wl & kw]
STOPS = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
def _trim(t):
    for st in STOPS:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()


def _load_clm_decoder_factory(clm_path):
    """Load clm303 weights once and return a factory for bind variants."""
    if CLM_DECODE_PATH not in sys.path:
        sys.path.insert(0, CLM_DECODE_PATH)
    import clm_decode as C
    from clm_decode import (
        _conv1d, nn_groupnorm_fwd, nn_gelu_fwd, nn_moe_router_fwd,
        _mix32, _rng_next, _topk_sample,
    )
    W = C.clm_load_weights(clm_path)
    d = W["d"]; E = W["E"]; K = W["K"]; L = W["L"]; V = W["V"]
    T_ctx = 24

    def _fwd_penultimate(tok_arr):
        """Full CLMConvMoE forward → yn [T, d] (penultimate before readout)."""
        ids = tok_arr.astype(np.int64)
        xe = W["embed"][ids]
        xt = _conv1d(xe, W["ecWt"], W["ecB"], T_ctx, d, d, K, 1)
        dil = 1
        for li in range(L):
            dil_eff = min(dil, 512)
            h = _conv1d(xt, W["tcWt"][li], W["tcB"][li], T_ctx, d, d, K, dil_eff)
            hn = nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T_ctx, d, 1)
            hg = nn_gelu_fwd(hn)
            xt = xt + hg.reshape(T_ctx, d)
            dil = dil * 2
        lr_ = _conv1d(xt, W["rWt"], W["rB"], T_ctx, d, E, 1, 1)
        ex_out = np.empty((E, T_ctx, d), dtype=np.float64)
        for ej in range(E):
            eo = _conv1d(xt, W["eWt"][ej], W["eB"][ej], T_ctx, d, d, K, 1)
            ex_out[ej] = nn_gelu_fwd(eo).reshape(T_ctx, d)
        y = nn_moe_router_fwd(lr_, ex_out, T_ctx, E, d)
        yn = nn_groupnorm_fwd(y, W["noG"], W["noB"], T_ctx, d, 1)
        return yn   # [T, d]

    def _readout(yn_mod):
        """Readout conv (K=1) → logits [T, V]."""
        return _conv1d(yn_mod, W["roWt"], W["roB"], T_ctx, d, V, 1, 1)

    def _renorm(composed, original):
        """Scale composed to have same L2 norm as original."""
        nc = np.linalg.norm(composed)
        no = np.linalg.norm(original)
        if nc > 1e-12:
            return composed * (no / nc)
        return original.copy()

    # ── Binding operators (applied to yn [T, d], return yn [T, d]) ──────────

    def bind_none(yn):
        """OFF baseline: no modification."""
        return yn

    def bind_vsa_hrr(yn):
        """VSA/HRR at readout: circular conv of yn[-1] with context mean.
        The context mean is the 'role bundle' that carries all concept signals.
        Composing yn[-1] (current prediction state) with context mean via
        circular conv produces a new representation that blends current state
        with context in a manner that (in principle) can decode joint content.
        Renormalized to original L2 so readout weights see expected distribution.
        """
        ctx_mean = yn[:-1].mean(axis=0)   # [d] — mean context representation
        composed = np.fft.irfft(
            np.fft.rfft(yn[-1]) * np.fft.rfft(ctx_mean), n=d)
        yn_new = yn.copy()
        yn_new[-1] = _renorm(composed, yn[-1])
        return yn_new

    def bind_hadamard(yn):
        """Multiplicative gate: yn[-1] ⊙ attention-weighted context.
        Implements: attend over context positions, gate yn[-1] element-wise.
        Role-filler interaction via element-wise product (bilinear without outer product).
        """
        # Attention scores: yn @ yn[-1] → [T]
        scores = yn @ yn[-1]
        scores -= scores.max()
        attn = np.exp(scores / (np.sqrt(d) + 1e-12))
        attn /= attn.sum() + 1e-12
        ctx = (attn[:, None] * yn).sum(axis=0)   # [d]
        gate = np.tanh(ctx / (np.linalg.norm(ctx) + 1e-12))
        composed = yn[-1] * gate
        yn_new = yn.copy()
        yn_new[-1] = _renorm(composed, yn[-1])
        return yn_new

    def bind_cross_attn(yn):
        """Cross-position attention at last position (H_1449-style but at readout).
        Soft attention over all T positions; last position queries all others.
        Result: attended summary replaces yn[-1] for prediction.
        """
        q = yn[-1]   # [d]
        scores = yn @ q / np.sqrt(d)   # [T]
        scores -= scores.max()
        attn = np.exp(scores)
        attn /= attn.sum() + 1e-12
        attended = (attn[:, None] * yn).sum(axis=0)   # [d]
        yn_new = yn.copy()
        yn_new[-1] = _renorm(attended, yn[-1])
        return yn_new

    BIND_OPS = {
        "none":       bind_none,
        "vsa_hrr":    bind_vsa_hrr,
        "hadamard":   bind_hadamard,
        "cross_attn": bind_cross_attn,
    }

    def make_gen(op_name):
        bind_fn = BIND_OPS[op_name]
        def gen(seed_text, max_tok, seed_rng):
            seed_b = seed_text.encode("utf-8", "surrogateescape")
            slen = len(seed_b)
            tok = np.empty(T_ctx, dtype=np.float64)
            for p in range(T_ctx):
                si = slen - T_ctx + p
                tok[p] = float(seed_b[si]) if si >= 0 else 32.0
            out = bytearray()
            rng_state = _mix32(seed_rng)
            for _ in range(max_tok):
                yn = _fwd_penultimate(tok)
                yn_bound = bind_fn(yn)
                logits = _readout(yn_bound)
                nb, rng_state = _topk_sample(logits[T_ctx - 1], V, 40, 0.7, rng_state)
                out.append(nb)
                tok[:T_ctx-1] = tok[1:]
                tok[T_ctx-1] = float(nb)
                if any(st in bytes(out).decode("utf-8","ignore") for st in STOPS):
                    break
            return _trim(bytes(out).decode("utf-8", "surrogateescape"))
        return gen

    return make_gen


def ladder_seed_g1(genfn, seed_rng, label, gen_len=50):
    """Run G1 ladder for one RNG seed (frozen VERBATIM metric, H_1129 / a7b_pass)."""
    # Singles
    sd = []
    for i, (c, _) in enumerate(CONCEPTS):
        o = genfn(f"{c}. ", gen_len, seed_rng + i)
        cov = _coverage(o)
        sd.append(len(cov))
    ms = max(sd) if sd else 0
    # Multi-concept seeds
    ks = []
    clears_any = False; best = 0
    for k in (2, 3, 4, 5):
        seedp = ". ".join(c for c, _ in CONCEPTS[:k]) + ". "
        o = genfn(seedp, gen_len + 20, seed_rng)
        cc = _coverage(o); kk = _kwr(o); coh = kk >= 0.50
        clears = (len(cc) >= 2 and len(cc) > ms and coh)
        clears_any = clears_any or clears; best = max(best, len(cc))
        ks.append({"k": k, "distinct": len(cc), "kwr": round(kk, 3),
                   "coherent": coh, "clears": clears, "text": o[:70]})
    return {"seed": seed_rng, "max_single": ms, "best_composed": best,
            "clears": clears_any, "ks": ks}


SEEDS = [7, 4302, 4303]

def run_g1_ops(clm_path, ops=("none", "vsa_hrr", "hadamard", "cross_attn"), gen_len=50):
    """Run G1 multi-seed for all bind ops, sharing one weight load."""
    print(f"  Loading weights from {clm_path} ...", flush=True)
    t0 = time.time()
    make_gen = _load_clm_decoder_factory(clm_path)
    print(f"  Weights loaded in {time.time()-t0:.1f}s", flush=True)

    op_results = {}
    for op in ops:
        print(f"\n  ── OP={op!r} ──", flush=True)
        t_op = time.time()
        genfn = make_gen(op)
        per = []
        for s in SEEDS:
            r = ladder_seed_g1(genfn, s, op, gen_len=gen_len)
            per.append(r)
            print(f"    seed={s}: max_single={r['max_single']} "
                  f"best_composed={r['best_composed']} "
                  f"clears={'GREEN' if r['clears'] else 'FAIL'}  "
                  f"({time.time()-t_op:.0f}s elapsed)", flush=True)
            for kd in r["ks"]:
                print(f"      k={kd['k']} distinct={kd['distinct']} kwr={kd['kwr']} "
                      f"coherent={kd['coherent']}  >> {kd['text']!r}", flush=True)
        n_green = sum(1 for r in per if r["clears"])
        verdict = "GREEN" if n_green >= 2 else "FAIL"
        op_results[op] = {"op": op, "per_seed": per, "n_green": n_green,
                          "verdict": verdict, "elapsed_s": time.time()-t_op}
        print(f"    ==> [{op}] G1 = {verdict} ({n_green}/3 seeds)  "
              f"elapsed={time.time()-t_op:.0f}s", flush=True)

    return op_results


# ════════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 78)
    print("G1 FROZEN MOUTH-BIND SCREEN — DIRECTIONAL (numpy, not engine-native TERMINAL)")
    print(f"date {time.strftime('%Y-%m-%d %H:%M:%S')}  host {os.uname().nodename}")
    print("=" * 78)

    all_results = {}

    # ── Part 1: Abstract mechanism probes ──────────────────────────────────
    print("\n\n## PART 1: Abstract binding mechanism probes")
    print("   (card cheap-test specs: H_1616 VSA, H_1623 Hypernet, H_1649 Saddle)")
    print("   Tests algebraic binding capability WITHOUT 303M weights.")
    print("-" * 60)

    print("\n### 1a. VSA/HRR bundle retrieval (H_1616)")
    vsa = probe_vsa_hrr(seed=42, d=512, K=20, N_bundle=5, n_trials=100)
    all_results["abstract_vsa"] = vsa

    print("\n### 1b. Hypernet multiplicative binding (H_1623)")
    hyp = probe_hypernet_mult(seed=42, n_epochs=300, lr=0.05)
    all_results["abstract_hypernet"] = hyp

    print("\n### 1c. A⇄G Saddle-point binding (H_1649)")
    sad = probe_saddle_point(seed=42, d=8, n_factors=4, n_roles=3, K_iters=30)
    all_results["abstract_saddle"] = sad

    print("\n\n## PART 1 SUMMARY")
    print(f"{'Mechanism':30s}  {'ON acc':8s}  {'OFF acc':8s}  {'bar_pass':8s}")
    for name, r in [("VSA/HRR (H_1616)", vsa), ("Hypernet (H_1623)", hyp),
                    ("Saddle (H_1649)", sad)]:
        on_acc  = r["ON"]["acc"] if "acc" in r["ON"] else "—"
        off_acc = (r["OFF"]["acc"] if "acc" in r.get("OFF", {}) else
                   r.get("energy", {}).get("acc", "—"))
        print(f"  {name:30s}  {str(on_acc):8s}  {str(off_acc):8s}  {r['bar_pass']}")

    # ── Part 2: Frozen clm303 G1 with bind ops ─────────────────────────────
    print("\n\n## PART 2: Frozen clm303 G1 with mouth-bind ops at readout")
    print(f"   CLM: {CLM_PATH}")
    print("   Probe: clm_decode.py retired py mirror (DIRECTIONAL only)")
    print("   Frozen bar: composed_distinct≥2 ∧ >max_single ∧ kwr≥0.50 in ≥2/3 seeds")
    print("-" * 60)

    if not os.path.exists(CLM_PATH):
        print(f"  ERROR: {CLM_PATH} not found", file=sys.stderr)
        all_results["clm303_g1"] = {"error": "CLM not found"}
    else:
        # gen_len=50 (reduced from 80 for speed; long enough to observe concept keywords)
        clm_res = run_g1_ops(CLM_PATH, ops=["none", "vsa_hrr", "hadamard", "cross_attn"], gen_len=50)
        all_results["clm303_g1"] = clm_res

        print("\n\n## PART 2 SUMMARY — ON vs OFF vs CONTROLS")
        print(f"{'OP':12s}  {'G1':6s}  {'n_green':7s}  {'max_composed':12s}  notes")
        for op, r in clm_res.items():
            max_c = max(s["best_composed"] for s in r["per_seed"]) if r["per_seed"] else 0
            note = "BASELINE" if op == "none" else "BIND-OP"
            print(f"  {op:12s}  {r['verdict']:6s}  {r['n_green']}/3      {max_c:12d}  {note}")

    # ── Save ────────────────────────────────────────────────────────────────
    out_json = os.path.join(RESULT_DIR, "raw_results.json")
    with open(out_json, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved → {out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
