"""V6_27 (LANE-BUS Step-1) -- is the bus tension load-bearing, and does it DISCHARGE on emit? ($0)

Step-0 (V6_26) showed the logit-row content tension is ~15-dim (headroom exists). Step-1 tests
whether that tension is (a) LOAD-BEARING (the content lane actually changes the emitted byte vs
the form-only reflex) and (b) has Fable's falsifiable p5 signature: emitting a content-driven
byte should DISCHARGE the residual -- tension drops at the next position.

Two lanes on trained57 (no new training):
  reflex[t]   = logits given only the last W bytes (form-only, local)
  composed[t] = logits given the FULL prefix       (form + content)
  tension[t]  = KL( softmax(composed[t]) || softmax(reflex[t]) )   (a real divergence, nats)
  override[t] = argmax(composed[t]) != argmax(reflex[t])           (content changed the byte?)

Tests:
  1. LOAD-BEARING: override rate; and does tension predict override (AUC-like separation)?
  2. DISCHARGE: E[ tension[t+1] - tension[t] | override at t ]  vs  at non-override positions.
     Fable's prediction: content-driven emits should be followed by a tension DROP (< 0),
     while non-emit positions carry the residual forward (~0 or rising).

Engine-native (decode._fwd_logits). Reuses trained57.clm + natural held-out text.
"""
import sys, os, re, importlib.util
import numpy as np

W_LOC = 8; N_SENT = 80; HELDOUT_FRAC = 0.20
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")
def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 300) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if s.endswith((".","!","?")): yield s

def _decode():
    spec = importlib.util.find_spec("anima_py")
    if spec and spec.submodule_search_locations:
        b = list(spec.submodule_search_locations)[0]
        for c in (os.path.join(b,"core"), b):
            if os.path.isdir(c): sys.path.insert(0, c)
    for c in ("/opt/homebrew/lib/python3.14/site-packages/anima_py/core",):
        if os.path.isdir(c): sys.path.insert(0, c)

def softmax(x):
    m = x.max(); e = np.exp(x - m); return e / (e.sum() + 1e-12)
def kl(p, q):
    return float(np.sum(p * (np.log(p + 1e-12) - np.log(q + 1e-12))))

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "trained57.clm"
    full = open(os.path.expanduser("~/anima-weights/en_general.txt"), encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full)*(1-HELDOUT_FRAC)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_SENT: break
    _decode(); import decode as clm
    W = clm.clm_load_weights(model)

    over_tens, non_tens = [], []          # tension at override vs non-override positions
    d_over, d_non = [], []                # Δtension = tension[t+1]-tension[t], split by override at t
    L, O, D = [], [], []                  # per-position (tension level, override, Δtension) for the control
    n_over = n_tot = 0
    for s in sents:
        b = list(s.encode("utf-8")); T = len(b) - 1
        if T < W_LOC + 3: continue
        comp = clm._fwd_logits(W, np.array([float(x) for x in b[:T]], dtype=np.float64), T)
        tens = np.zeros(T); ovr = np.zeros(T, bool)
        for pos in range(W_LOC, T):
            loc = b[pos-W_LOC:pos+1]; tl = len(loc)-1
            rl = clm._fwd_logits(W, np.array([float(x) for x in loc[:tl]], dtype=np.float64), tl)[tl-1]
            cp = comp[pos]
            tens[pos] = kl(softmax(cp), softmax(rl))
            ovr[pos] = int(np.argmax(cp)) != int(np.argmax(rl))
        for pos in range(W_LOC, T-1):
            n_tot += 1; n_over += int(ovr[pos])
            (over_tens if ovr[pos] else non_tens).append(tens[pos])
            dt = tens[pos+1] - tens[pos]
            (d_over if ovr[pos] else d_non).append(dt)
            L.append(tens[pos]); O.append(float(ovr[pos])); D.append(dt)

    import statistics as st
    orate = n_over / max(n_tot, 1)
    print(f"# V6_27 LANE-BUS Step-1 -- load-bearing + discharge  (model={os.path.basename(model)})")
    print(f"sample: {len(sents)} sentences, {n_tot} positions\n")
    print(f"1. LOAD-BEARING")
    print(f"   override rate (content changes the emitted byte) = {orate:.3f}")
    print(f"   mean tension | override    = {st.mean(over_tens):.4f} nats")
    print(f"   mean tension | no-override = {st.mean(non_tens):.4f} nats")
    sep = st.mean(over_tens) - st.mean(non_tens)
    print(f"   → tension separates override from non ({sep:+.4f} nats): " +
          ("YES, tension is load-bearing" if sep > 0.05 else "weak — tension barely predicts override"))
    print(f"\n2. DISCHARGE (Fable p5 signature: emit should drop the residual)")
    print(f"   Δtension after override    = {st.mean(d_over):+.4f} nats  (n={len(d_over)})")
    print(f"   Δtension after no-override = {st.mean(d_non):+.4f} nats  (n={len(d_non)})")
    disc = st.mean(d_over) - st.mean(d_non)
    print(f"   raw discharge contrast = {disc:+.4f} nats  (CONFOUNDED by tension level — see control)")
    print(f"\n3. MEAN-REVERSION CONTROL (Δtension ~ a + b·tension_level + c·override)")
    Ln, On, Dn = np.array(L), np.array(O), np.array(D)
    # OLS with 2 regressors + intercept
    X = np.column_stack([np.ones_like(Ln), Ln - Ln.mean(), On - On.mean()])
    coef, *_ = np.linalg.lstsq(X, Dn, rcond=None)
    resid = Dn - X @ coef
    dof = len(Dn) - 3
    sigma2 = (resid @ resid) / dof
    XtX_inv = np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(XtX_inv) * sigma2)
    b_lvl, c_ovr = coef[1], coef[2]; z_c = c_ovr / se[2]
    print(f"   b (tension level → Δtension) = {b_lvl:+.4f}   (negative = mean reversion, expected)")
    print(f"   c (override → Δtension, LEVEL-CONTROLLED) = {c_ovr:+.4f}  z={z_c:+.2f}")
    print()
    if b_lvl < -0.1 and abs(z_c) < 2:
        print(f"   → the raw 'discharge' is MEAN REVERSION (b={b_lvl:.3f}); once tension level is")
        print(f"     controlled, override adds NO extra drop (c={c_ovr:+.3f}, z={z_c:.1f}, ns).")
        print("     Fable's p5 discharge signature is NOT established by this observational bus.")
        print("     Next: test discharge CAUSALLY inside a trained emit gate (Step-2), or redefine emit.")
    elif c_ovr < 0 and z_c < -2:
        print(f"   → GENUINE DISCHARGE: override drops tension BEYOND mean reversion (c={c_ovr:.3f}, z={z_c:.1f}).")
        print("     LANE-BUS p5 signature survives the level control — build the emit gate ON.")
    else:
        print(f"   → INCONCLUSIVE: c={c_ovr:+.3f} z={z_c:.1f}.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
