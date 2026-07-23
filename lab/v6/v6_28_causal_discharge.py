"""V6_28 (LANE-BUS Step-2) -- CAUSAL discharge: does emitting the CONTENT byte discharge the
residual more than emitting the FORM byte? ($0, counterfactual intervention)

V6_27 showed observationally that override positions discharge beyond mean reversion. Step-2
tests it CAUSALLY with a within-position counterfactual on the same model (no confound of which
positions are chosen): at a divergent position t, actually EMIT each candidate and measure the
next residual.

  tension[t]   = KL(softmax(composed[t]) || softmax(reflex[t]))
  c = argmax(composed[t])   (content-resolved byte)
  r = argmax(reflex[t])     (form-resolved byte)   -- only positions with c != r
  emit c: prefix+[c] -> tension_c = KL at the new position
  emit r: prefix+[r] -> tension_r = KL at the new position
  discharge_content = tension[t] - tension_c ;  discharge_form = tension[t] - tension_r

Fable's p5 (causal): emitting the CONTENT resolution should discharge the residual MORE than
emitting the FORM resolution -> discharge_content > discharge_form (paired, same t).

Engine-native (decode._fwd_logits). Reuses trained57. Positions subsampled for speed.
"""
import sys, os, re, importlib.util, statistics as st
import numpy as np

W_LOC = 8; N_SENT = 40; STRIDE = 2; HELDOUT_FRAC = 0.20
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")
def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 220) or _YEAR.search(s): continue
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
    m = x.max(); e = np.exp(x - m); return e/(e.sum()+1e-12)
def kl(p, q):
    return float(np.sum(p*(np.log(p+1e-12)-np.log(q+1e-12))))

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

    def tens_at(seq):
        """KL(composed||reflex) at the LAST position of seq (predicting the next byte)."""
        T = len(seq)
        comp = clm._fwd_logits(W, np.array([float(x) for x in seq], dtype=np.float64), T)[T-1]
        loc = seq[-W_LOC:]; tl = len(loc)
        refl = clm._fwd_logits(W, np.array([float(x) for x in loc], dtype=np.float64), tl)[tl-1]
        return kl(softmax(comp), softmax(refl)), int(np.argmax(comp)), int(np.argmax(refl))

    dc, df = [], []
    for s in sents:
        b = list(s.encode("utf-8"))
        for t in range(W_LOC+1, len(b)-1, STRIDE):
            pre = b[:t]
            t_now, c, r = tens_at(pre)
            if c == r:
                continue
            t_c, _, _ = tens_at(pre + [c])       # emit content byte
            t_r, _, _ = tens_at(pre + [r])       # emit form byte
            dc.append(t_now - t_c)               # discharge from emitting content
            df.append(t_now - t_r)               # discharge from emitting form
    n = len(dc)
    diff = [a-b for a, b in zip(dc, df)]
    md, sd = st.mean(diff), (st.pstdev(diff) or 1e-9)
    z = md / (sd/ (n**0.5))
    print(f"# V6_28 LANE-BUS Step-2 -- CAUSAL discharge (content vs form emit)  model={os.path.basename(model)}")
    print(f"sample: {N_SENT} sentences, {n} divergent positions (paired counterfactual)\n")
    print(f"discharge | emit CONTENT byte = {st.mean(dc):+.4f} nats")
    print(f"discharge | emit FORM byte    = {st.mean(df):+.4f} nats")
    print(f"paired diff (content − form)  = {md:+.4f} nats   z={z:+.2f}  (n={n})")
    print()
    if md > 0 and z > 2:
        print("→ CAUSAL DISCHARGE CONFIRMED: emitting the content-resolved byte discharges the")
        print("  residual MORE than the form byte. p5's 'emit discharges tension' is CAUSAL here.")
        print("  LANE-BUS emit-gate premise validated — build the trained gate (Step-3).")
    elif md > 0:
        print(f"→ DIRECTIONAL (z={z:.1f}): content emit discharges more, not yet significant.")
    else:
        print(f"→ NO CAUSAL EFFECT (diff={md:+.3f} z={z:.1f}): which byte is emitted does not change")
        print("  the discharge. V6_27's observational drop was not the emit's DOING — rethink emit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
