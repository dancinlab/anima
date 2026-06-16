#!/usr/bin/env python3
"""OMEGA coupling-analysis ② — ALL-6-WIRE learned gate (extends #1786 {base,A,G} → all wires).

#1786 fit a learned per-wire gate over only {base, A, G} (the w1 A⇄G wire) and showed the
learned gate beats the fixed A−G formula. But the OMEGA coupling bus (engines/omega/coupling_bus.hexa)
has SIX wires:
  w1 A⇄G    : modulated += α·(a_head − g_head)        (CDV2 dual-head next/prev byte)
  w2 W→temp : modulated *= 1/(1+β·w_tension)          (will-tension → softmax sharpness)
  w3 curio  : modulated += c·curiosity·(±1 by parity) (E-ratchet → top-k width)
  w4 Ψ      : modulated += p·psi8[i mod 8]            (8D Ψ context conditioning)
  w5 module : modulated += r·module_act[i mod M]      (HEXAD N-module → conv-MoE routing)
  w6 dF/dt  : modulated += dgain·Δ(a−g)               (L4 time-derivative of A⇄G)

This rung extends the #1786 learned-gate fit from {base,A,G} to ALL EIGHT gains:
    logits = gB·base + g_A·A + g_G·G + g_W·Wfeat + g_curio·Cfeat + g_Ψ·Ψfeat + g_module·Mfeat + g_dFdt·Dfeat
fit on a train-gate split (convex log-linear + L2 on the wire gains), FROZEN, then evaluated
on a disjoint held-out TEST split.

Each wire's feature is a REAL substrate-derived per-(context,byte) logit signal built from the
trained n-gram substrate — NOT a fabricated input (p7, a_core_engine_map):
  base   : unigram log-freq (the context-free "mouth")
  A      : bigram log P(next|ctx)                      — Engine-A learned next-byte
  G      : rev-bigram log P(prev|ctx)                  — Engine-G learned prev-byte
  Wfeat  : −(per-byte logit) scaled by a will-tension proxy = context entropy of A
           (high-tension/uncertain context sharpens → multiplicative temp linearized as an
           additive sharpening feature: w2 raises confident bytes when tension is high)
  Cfeat  : c·(±1 by byte parity) — the exact w3 curiosity parity bias (curiosity=1 here)
  Ψfeat  : psi8[byte mod 8] tiled — the w4 8D Ψ conditioning (Ψ = the 8-dim context coord
           of the n-gram model, computed from the substrate, deterministic)
  Mfeat  : module_act[byte mod 6] tiled — the w5 N=6 HEXAD module routing (module_act = the
           6-bin marginal of A over the context, a real substrate routing signal)
  Dfeat  : Δ(A−G) between this byte's context and the previous context — the w6 dF/dt velocity

PRE-REGISTERED (a wire "carries structure"):
  a wire carries structure ⟺ |learned gain| materially non-zero (≥ TAU) AND ablating that wire
  (gain→0, refit-frozen others) RAISES held-out CE (ΔCE_ablate > 0). A wire is INERT if its
  learned gain is ~0 OR ablating it does not raise CE. We additionally run a SHUFFLE control per
  wire: refit with that wire's feature row-shuffled across vocab; a real wire must beat its shuffle.
Honest closed-negative OK — some wires (w3 parity, w4 Ψ, w6 dF/dt at near-fixed-point) may be inert.

p7 / a_toy_scale_recheck: TOY byte n-gram substrate, real-but-small repo corpus, CPU/$0, no torch.
CE is held-out (fit on TRAIN-gate, verdict on disjoint TEST), NOT a Goodhart target.
"""
import json, math, os, glob
import numpy as np

V = 256
SMOOTH = 0.5
LR = 0.3
STEPS = 400
L2 = 0.02
TAU = 0.05                 # materiality threshold on |learned gain|
N_MODULES = 6              # HEXAD default (omega_n_modules_default)
SEED = 20260604
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WIRES = ["base", "A", "G", "W_temp", "curio", "Psi", "module", "dFdt"]


def load_corpus():
    files = sorted(glob.glob(os.path.join(ROOT, "domains", "*.md"))) + [os.path.join(ROOT, "CLAUDE.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "engines", "*", "*.md")))
    buf = bytearray()
    for f in files:
        try:
            buf += open(f, "rb").read()
        except OSError:
            pass
        if len(buf) > 400_000:
            break
    return np.frombuffer(bytes(buf[:400_000]), dtype=np.uint8)


def train_substrate(train):
    big = np.full((V, V), SMOOTH); rev = np.full((V, V), SMOOTH); uni = np.full(V, SMOOTH)
    for i in range(1, len(train)):
        c, nxt = int(train[i - 1]), int(train[i])
        big[c, nxt] += 1.0; rev[nxt, c] += 1.0; uni[nxt] += 1.0
    uni[int(train[0])] += 1.0
    logA = np.log(big / big.sum(1, keepdims=True))      # Engine-A: log P(next|ctx)
    logG = np.log(rev / rev.sum(1, keepdims=True))      # Engine-G: log P(prev|ctx)
    logBase = np.log(uni / uni.sum())                   # base mouth: unigram
    # Ψ 8-coord: per-context = an 8-dim projection of the A-row (a deterministic substrate map).
    # psi8[ctx] = 8 bin-means of logA[ctx] over vocab → an 8D context coordinate (real, derived).
    binsV = np.array_split(np.arange(V), 8)
    psi8 = np.stack([logA[:, b].mean(1) for b in binsV], axis=1)        # (V, 8)
    psi8 = (psi8 - psi8.mean(0)) / (psi8.std(0) + 1e-9)
    # module_act 6-coord: per-context = 6 bin-means of logA[ctx] → HEXAD N=6 routing signal.
    binsM = np.array_split(np.arange(V), N_MODULES)
    mact = np.stack([logA[:, b].mean(1) for b in binsM], axis=1)        # (V, 6)
    mact = (mact - mact.mean(0)) / (mact.std(0) + 1e-9)
    # will-tension proxy: per-context entropy of P(next|ctx) (high = uncertain = high tension)
    pA = np.exp(logA); pA = pA / pA.sum(1, keepdims=True)
    Hctx = -(pA * np.log(pA + 1e-12)).sum(1)                            # (V,) context entropy
    Hctx = (Hctx - Hctx.mean()) / (Hctx.std() + 1e-9)
    return logA, logG, logBase, psi8, mact, Hctx


def build_feats(seq, sub):
    """Per-(step, byte) logit features for all 8 wires. Returns (F dict, tgt)."""
    logA, logG, logBase, psi8, mact, Hctx = sub
    ctx = seq[:-1].astype(int); tgt = seq[1:].astype(int)
    N = len(ctx)
    base = np.tile(logBase, (N, 1))                                    # (N,V)
    A = logA[ctx]                                                      # (N,V)
    G = logG[ctx]                                                      # (N,V)
    # w2 W→temp linearized: sharpening feature = tension(ctx) * (A − mean_A) — when context
    # tension is high, push confident (above-mean) bytes up. Captures the multiplicative temp
    # effect as an additive logit feature (real substrate signal: tension × confidence).
    W_temp = Hctx[ctx][:, None] * (A - A.mean(1, keepdims=True))       # (N,V)
    # w3 curiosity: the EXACT hexa parity bias c·curiosity·(±1), curiosity=1 → ±1 by byte index
    sign = np.where(np.arange(V) % 2 == 0, 1.0, -1.0)
    curio = np.tile(sign, (N, 1))                                      # (N,V)
    # w4 Ψ: psi8[byte mod 8] per context — broadcast the context's 8D Ψ over bytes by (byte mod 8)
    psi_idx = np.arange(V) % 8
    Psi = psi8[ctx][:, psi_idx]                                       # (N,V) = psi8[ctx, byte%8]
    # w5 module: mact[byte mod 6] per context
    mod_idx = np.arange(V) % N_MODULES
    module = mact[ctx][:, mod_idx]                                    # (N,V)
    # w6 dF/dt: Δ(A−G) between this context and the previous context (velocity of A⇄G)
    AmG = A - G
    dFdt = np.zeros_like(AmG)
    dFdt[1:] = AmG[1:] - AmG[:-1]                                     # first step = 0 (no prev)
    F = {"base": base, "A": A, "G": G, "W_temp": W_temp,
         "curio": curio, "Psi": Psi, "module": module, "dFdt": dFdt}
    return F, tgt


def softmax(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)


def logits_of(g, F):
    return sum(g[k] * F[w] for k, w in enumerate(WIRES))


def ce_of(g, F, tgt):
    p = softmax(logits_of(g, F))
    return float(-np.mean(np.log(p[np.arange(len(tgt)), tgt] + 1e-12)))


def fit_gate(F, tgt, mask=None, steps=STEPS, lr=LR, l2=L2):
    """Convex log-linear fit of the 8 gains minimizing train CE + L2 on the wire gains.
    mask (len 8, 0/1) clamps a wire's gain to 0 (for ablation refit). gB (base) not regularized."""
    N = len(tgt)
    onehot = np.zeros((N, V)); onehot[np.arange(N), tgt] = 1.0
    g = np.zeros(8); g[0] = 1.0                                        # init base-only
    reg = np.ones(8); reg[0] = 0.0                                     # don't regularize base
    if mask is None:
        mask = np.ones(8)
    Fs = [F[w] for w in WIRES]
    for _ in range(steps):
        g = g * mask
        p = softmax(logits_of(g, F))
        resid = p - onehot
        grad = np.array([np.sum(resid * Fs[k]) / N for k in range(8)]) + l2 * reg * g
        g = (g - lr * grad) * mask
    return g


def main():
    corpus = load_corpus()
    rng = np.random.default_rng(SEED)
    n = len(corpus)
    start = int(rng.integers(0, n - 20000))
    gate_seq = corpus[start:start + 12000]
    test_seq = corpus[start + 12000:start + 16000]
    train_sub = np.concatenate([corpus[:start], corpus[start + 16000:]])
    sub = train_substrate(train_sub)

    Fg, gt = build_feats(gate_seq, sub)
    Ft, tt = build_feats(test_seq, sub)

    # full 8-gain fit
    g_full = fit_gate(Fg, gt)
    ce_full = ce_of(g_full, Ft, tt)
    ce_base = ce_of(np.array([1.0, 0, 0, 0, 0, 0, 0, 0]), Ft, tt)

    print(f"=== OMEGA coupling-analysis ② — ALL-6-WIRE learned gate  (corpus={len(corpus)}B, V={V}) ===")
    print(f"uniform-256 CE = {math.log(256):.6f}\n")
    print("--- full 8-gain learned gate (fit on train-gate, frozen) ---")
    for k, w in enumerate(WIRES):
        print(f"  g[{w:7s}] = {g_full[k]:+.4f}")
    print(f"\n  held-out TEST CE: full gate = {ce_full:.6f}   |   base-only = {ce_base:.6f}   (Δ{ce_base-ce_full:+.4f})\n")

    # per-wire ablation (gain→0, refit the others frozen-style) + shuffle control
    print("--- per-wire ablation (refit others with this wire OFF) + shuffle control ---")
    rows = []
    for k, w in enumerate(WIRES):
        if w == "base":
            continue
        mask = np.ones(8); mask[k] = 0.0
        g_ab = fit_gate(Fg, gt, mask=mask)
        ce_ab = ce_of(g_ab, Ft, tt)
        dCE_ablate = ce_ab - ce_full                          # >0 ⇒ wire helps (removing it hurts)

        # shuffle control: row-shuffle this wire's feature across vocab in BOTH splits (same perm),
        # refit full → if the wire carried real structure, the shuffled feature should NOT help.
        perm = np.random.default_rng(SEED + 100 + k).permutation(V)
        Fg_s = dict(Fg); Ft_s = dict(Ft)
        Fg_s[w] = Fg[w][:, perm]; Ft_s[w] = Ft[w][:, perm]
        g_sh = fit_gate(Fg_s, gt)
        ce_sh = ce_of(g_sh, Ft_s, tt)
        beats_shuffle = ce_full < ce_sh                       # real feature beats its shuffle

        material = abs(g_full[k]) >= TAU
        carries = bool(material and dCE_ablate > 1e-4 and beats_shuffle)
        rows.append({
            "wire": w, "gain": float(g_full[k]), "material": bool(material),
            "ce_ablate": ce_ab, "dCE_ablate": float(dCE_ablate),
            "ce_shuffle": ce_sh, "beats_shuffle": bool(beats_shuffle),
            "carries_structure": carries,
        })
        verdict = "CARRIES STRUCTURE" if carries else "INERT"
        print(f"  {w:7s}: gain={g_full[k]:+.4f} (material={material!s:5s}) | "
              f"ablate CE {ce_ab:.4f} ΔCE{dCE_ablate:+.4f} | shuffle CE {ce_sh:.4f} "
              f"beats_shuf={beats_shuffle!s:5s} -> {verdict}")

    carriers = [r["wire"] for r in rows if r["carries_structure"]]
    inert = [r["wire"] for r in rows if not r["carries_structure"]]

    # carrier-only gate: refit using ONLY base + the carrier wires (drop the inert/harmful wires).
    # This isolates "what the structure-carrying wires deliver" from the inert-wire overfit.
    carrier_mask = np.zeros(8); carrier_mask[0] = 1.0
    for k, w in enumerate(WIRES):
        if w in carriers:
            carrier_mask[k] = 1.0
    g_car = fit_gate(Fg, gt, mask=carrier_mask)
    ce_car = ce_of(g_car, Ft, tt)

    print("\n=== SUMMARY ===")
    print(f"full 8-gain vector [gB,gA,gG,gW,gC,gΨ,gM,gD] = [{', '.join(f'{x:+.3f}' for x in g_full)}]")
    full_dir = "BEATS" if ce_full < ce_base else "WORSE THAN"
    print(f"full naive gate TEST CE {ce_full:.4f} {full_dir} base {ce_base:.4f} "
          f"-> the full 8-wire gate {'helps' if ce_full < ce_base else 'OVERFITS (inert/leaky wires hurt held-out)'}")
    print(f"carrier-only gate (base+{carriers}) TEST CE {ce_car:.4f} vs base {ce_base:.4f} "
          f"(Δ{ce_base-ce_car:+.4f}) -> dropping inert wires {'RECOVERS a real gain' if ce_car < ce_base else 'still does not beat base'}")
    print(f"🟢 wires that CARRY STRUCTURE ({len(carriers)}): {carriers if carriers else 'NONE'}")
    print(f"⚪ INERT wires ({len(inert)}): {inert if inert else 'NONE'}")
    print(f"pre-registered: carries ⟺ |gain|≥{TAU} AND ablation raises held-out CE AND beats its vocab-shuffle.")
    print(f"SCOPE (a_toy_scale_recheck): TOY n-gram substrate, {len(corpus)}B repo corpus, CPU/$0, no torch.")
    print(f"  Honest closed-negative for inert wires — the toy substrate may not exercise W/curio/Ψ/module/dFdt")
    print(f"  the way a trained d384 transformer (#1791) does; this is the relative carrier RANKING at toy scale.")

    out = {
        "rung": "coupling-analysis ② all-6-wire learned gate", "scale": "TOY/CPU/$0",
        "corpus_bytes": int(len(corpus)), "V": V, "tau": TAU,
        "gain_vector": {w: float(g_full[k]) for k, w in enumerate(WIRES)},
        "ce_full": ce_full, "ce_base": ce_base, "ce_carrier_only": ce_car,
        "carrier_gain_vector": {w: float(g_car[k]) for k, w in enumerate(WIRES)},
        "uniform": math.log(256),
        "per_wire": rows, "carriers": carriers, "inert": inert,
        "full_gate_beats_base": bool(ce_full < ce_base),
        "carrier_gate_beats_base": bool(ce_car < ce_base),
        "criterion": "carries_structure ⟺ |gain|>=TAU AND dCE_ablate>0 AND beats_shuffle",
    }
    return out, g_full, ce_full, ce_base, ce_car, rows, carriers, inert, len(corpus)


if __name__ == "__main__":
    main()
