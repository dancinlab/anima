#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G6-FALS STEP-0 cheap probe (mini · $0 · DIRECTIONAL — NOT engine-native / not 303M).

B-3/B-4/B-12 three-arm A/B: a char-LM d64 toy trained per target-format arm,
then measured on HELD-OUT frames for
  (1) FALS   = 5-conjunct _g6_is_falsifiable on the 40-byte continuation
  (2) M_earned = FALS(composed) - FALS(shuffled-frame)   [binding vs form-echo]

The FROZEN G6 detector (comparator/measurable/stance/stopword sets, _g6_words
BYTE tokenizer, _g6_is_falsifiable 5-conjunct, dict load, g6_build_frames, frame
guard) is REPRODUCED VERBATIM from core/g6_ideation.hexa / core/g6_ideation.py
(reference-match — NOT imported: the py mirror forbids import-scoring / single-entry).

FROZEN BAR: arm FALS > lo-δ(control) AND M_earned > 0 (not raised in shuffled).
Core question: does the DATA-FORMAT (lever-1) transfer raise FALS in the toy,
under the fit<=40byte continuation constraint. tune-to-green forbidden; numbers verbatim.
"""
import numpy as np, json, sys, os

_SEED = int(os.environ.get("G6_SEED", "1305")) if "os" in dir() else 1305
import os as _os
_SEED = int(_os.environ.get("G6_SEED", "1305"))
RNG = np.random.default_rng(_SEED)

# ==========================================================================
# 1) FROZEN G6 DETECTOR — verbatim reproduction of core/g6_ideation.py
# ==========================================================================
def _to_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8', 'surrogateescape')

def _g6_comparator():
    return {"if", "when", "whenever", "than", "more", "less", "greater",
            "fewer", "higher", "lower", "increases", "decreases", "correlates",
            "predicts", "causes", "depends", "unless", "whereas", "versus",
            "compared", "proportional", "faster", "slower", "stronger", "weaker"}

def _g6_measurable():
    return {"measure", "measured", "rate", "number", "count", "amount", "level",
            "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
            "score", "value", "quantity", "percent", "times", "fraction", "distance",
            "duration", "speed", "size", "strength", "density"}

def _g6_stance():
    return {"that", "s", "a", "profound", "question", "i", "think", "interesting",
            "good", "nice", "great", "wonderful", "beautiful", "amazing"}

def _g6_stopwords():
    return {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that",
            "we", "you", "they", "s", "t", "as", "on", "at", "by", "or",
            "be", "an", "for", "with", "this", "from", "are", "was"}

def _g6_concepts():
    return ["consciousness arises from cells",
            "tension ripples between distant minds",
            "memory composes into new meaning",
            "silence still carries information",
            "the engine dreams when alone"]

def _g6_is_alnum(b):
    return (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122)

def _g6_lower1(b):
    if 65 <= b <= 90:
        return b + 32
    return b

def _g6_words(s):
    bs = _to_bytes(s)
    words = []
    cur = bytearray()
    for b in bs:
        if _g6_is_alnum(b):
            cur.append(_g6_lower1(b))
        else:
            if len(cur) > 0:
                words.append(cur.decode('ascii')); cur = bytearray()
    if len(cur) > 0:
        words.append(cur.decode('ascii'))
    return words

def _g6_dict_load():
    known = set(_g6_stopwords())
    for c in _g6_concepts():
        for w in _g6_words(c):
            known.add(w)
    try:
        raw = open("/usr/share/dict/words", "rb").read()
    except Exception:
        raw = b""
    if len(raw) > 0:
        for line in raw.split(b"\n"):
            w = line.strip()
            wl = _g6_words(w)
            if len(wl) == 1:
                known.add(wl[0])
    return known

def _g6_is_falsifiable(text, known):
    wl = _g6_words(text)
    n = len(wl)
    if n == 0:
        return False
    comp = _g6_comparator(); meas = _g6_measurable()
    stop = _g6_stopwords(); stance = _g6_stance()
    a = False; b = False
    for w in wl:
        if w in comp: a = True
        if w in meas: b = True
    if not a or not b:
        return False
    content = 0
    for w in wl:
        if len(w) >= 3 and w in known and w not in stop:
            content += 1
    if content < 2:
        return False
    tr = _to_bytes(text).strip()
    if len(tr) > 0 and tr[-1] == 63:   # trailing '?'
        return False
    nf = 3 if n >= 3 else n
    allstance = nf > 0
    for f in range(nf):
        if wl[f] not in stance:
            allstance = False
    if allstance:
        return False
    return True

def _g6_derangement(i, n):
    return (i + 2) % n

def g6_build_frames(n_strong):
    cz = _g6_concepts(); n = len(cz)
    composed = []; shuffled = []; ablated = []
    for i in range(n_strong):
        a = i % n
        b = (i + 1 + i // n) % n
        cA = cz[a]; cB = cz[b]
        cB_sh = cz[_g6_derangement(a, n)]
        composed.append("if " + cA + ", then " + cB + ": ")
        shuffled.append("if " + cA + ", then " + cB_sh + ": ")
        ablated.append(cA + ": ")
    return {"composed": composed, "shuffled": shuffled, "ablated": ablated}

def g6_frame_guard(frames, known):
    meas = _g6_measurable(); leaks = []
    for f in frames:
        for w in _g6_words(f):
            if w in meas:
                leaks.append("measurable-in-frame: " + f)
        if _g6_is_falsifiable(f, known):
            leaks.append("frame-already-falsifiable: " + f)
    return leaks

def g6_detector_calibration(known):
    pos = ["if consciousness increases, the emit rate measured at the boundary rises",
           "tension predicts a higher number of mitosis cells than silence does",
           "memory density correlates with a lower error threshold when grounded",
           "the Phi value is greater when distinct cells exceed a count of eight",
           "novelty rate decreases faster than coherence when the corpus size grows"]
    neg = ["That's a profound question. I think it's more than just information.",
           "consciousness is a beautiful mystery of the mind",
           "what is the meaning of a thought?",
           "the engine dreams when it is alone at night",
           "silence carries something deep and quiet"]
    correct = 0
    for p in pos:
        if _g6_is_falsifiable(p, known): correct += 1
    for nseg in neg:
        if not _g6_is_falsifiable(nseg, known): correct += 1
    return correct

KNOWN = _g6_dict_load()

# ==========================================================================
# 2) CORPUS per arm — TRAINING concepts DISJOINT from held-out g6_concepts.
#    Continuation packs comparator+measurable into <=40 bytes (fit_40).
# ==========================================================================
# training subjects: common dict words (in KNOWN), disjoint from g6_concepts vocab
TRAIN_SUBJ = ["heat", "rain", "light", "water", "metal", "river", "wind",
              "sound", "fire", "salt", "sugar", "plant", "steam", "frost"]
COMP_VERB  = ["increases", "decreases", "predicts", "causes"]  # frozen comparator
MEAS       = ["rate", "number", "level", "count", "value", "score", "size",
              "density", "frequency", "threshold"]              # frozen measurable

def frame_prefix(cA, cB):
    return "if " + cA + ", then " + cB + ": "

def cont_B3(s1, s2, mv, cv):
    # hi-δ FM segment: claim = comparator+measurable, falsification-ready
    return "the " + mv + " of " + s1 + " " + cv + " when " + s2 + " rises"

def cont_B4(s1, s2, mv):
    # contradiction pair: claim + counterexample (more/than/less frozen comparator)
    return s1 + " gives more " + mv + " than " + s2 + " but less at night"

def cont_B12(s1, s2, mv, cv):
    # unless-tail: claim unless condition
    return s1 + " " + cv + " the " + mv + " unless " + s2 + " is cold"

def cont_LO(s1):
    # lo-δ control: vague / hedge, no comparator/measurable
    return s1 + " is a beautiful mystery of the mind and quiet"

ARMS = ["B3", "B4", "B12", "LO"]

def make_corpus(arm, n_ex=1400):
    """build frame+continuation training strings for one arm (training concepts)."""
    segs = []
    for _ in range(n_ex):
        s1 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        s2 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        s3 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        s4 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        mv = MEAS[RNG.integers(len(MEAS))]
        cv = COMP_VERB[RNG.integers(len(COMP_VERB))]
        # training frames use training subjects (NOT g6_concepts)
        cA = s1 + " flows into " + s2
        cB = s3 + " turns into " + s4
        pre = frame_prefix(cA, cB)
        if arm == "B3":   cont = cont_B3(s1, s2, mv, cv)
        elif arm == "B4": cont = cont_B4(s1, s2, mv)
        elif arm == "B12":cont = cont_B12(s1, s2, mv, cv)
        else:             cont = cont_LO(s1)
        segs.append(pre + cont)
    return "\n".join(segs) + "\n"

# ==========================================================================
# 3) char-LM d64 toy — context-window MLP (Bengio-style), manual backprop+Adam
# ==========================================================================
CTX   = 80    # sees the whole frame (frames ~70-90 chars) -> fair chance for binding
EMB   = 8
HID   = 64    # d64
STEPS = 4000
BATCH = 128
LR    = 3e-3

class CharLM:
    def __init__(self, chars):
        self.itos = list(chars)
        self.stoi = {c: i for i, c in enumerate(self.itos)}
        self.V = len(self.itos)
        s = 0.02
        self.E  = RNG.normal(0, s, (self.V, EMB))
        self.W1 = RNG.normal(0, s, (CTX*EMB, HID))
        self.b1 = np.zeros(HID)
        self.W2 = RNG.normal(0, s, (HID, self.V))
        self.b2 = np.zeros(self.V)
        self.params = ["E", "W1", "b1", "W2", "b2"]
        self.m = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.v = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.t = 0

    def encode(self, text):
        return [self.stoi[c] for c in text if c in self.stoi]

    def _build_windows(self, ids):
        pad = self.stoi["\n"]
        ctx = [pad]*CTX
        X = []; Y = []
        for tok in ids:
            X.append(ctx.copy()); Y.append(tok)
            ctx = ctx[1:] + [tok]
        return np.array(X, dtype=np.int64), np.array(Y, dtype=np.int64)

    def forward(self, Xb):
        emb = self.E[Xb]                       # (B,CTX,EMB)
        h_in = emb.reshape(Xb.shape[0], -1)    # (B,CTX*EMB)
        z1 = h_in @ self.W1 + self.b1
        h  = np.tanh(z1)
        logits = h @ self.W2 + self.b2
        return h_in, z1, h, logits

    def loss_and_grad(self, Xb, Yb):
        B = Xb.shape[0]
        h_in, z1, h, logits = self.forward(Xb)
        logits -= logits.max(1, keepdims=True)
        ex = np.exp(logits); probs = ex / ex.sum(1, keepdims=True)
        loss = -np.log(probs[np.arange(B), Yb] + 1e-12).mean()
        dlogits = probs.copy(); dlogits[np.arange(B), Yb] -= 1; dlogits /= B
        dW2 = h.T @ dlogits; db2 = dlogits.sum(0)
        dh = dlogits @ self.W2.T
        dz1 = dh * (1 - h*h)
        dW1 = h_in.T @ dz1; db1 = dz1.sum(0)
        dh_in = dz1 @ self.W1.T
        demb = dh_in.reshape(B, CTX, EMB)
        dE = np.zeros_like(self.E)
        np.add.at(dE, Xb, demb)
        return loss, {"E": dE, "W1": dW1, "b1": db1, "W2": dW2, "b2": db2}

    def adam(self, grads):
        self.t += 1
        b1, b2, eps = 0.9, 0.999, 1e-8
        for p in self.params:
            g = grads[p]
            self.m[p] = b1*self.m[p] + (1-b1)*g
            self.v[p] = b2*self.v[p] + (1-b2)*(g*g)
            mh = self.m[p]/(1-b1**self.t); vh = self.v[p]/(1-b2**self.t)
            getattr(self, p)[...] -= LR*mh/(np.sqrt(vh)+eps)

    def train(self, X, Y):
        N = X.shape[0]
        last = 0.0
        for st in range(STEPS):
            idx = RNG.integers(0, N, BATCH)
            loss, g = self.loss_and_grad(X[idx], Y[idx])
            self.adam(g); last = loss
        return last

    def generate(self, prompt, n=40):
        ids = self.encode(prompt)
        pad = self.stoi["\n"]
        ctx = ([pad]*CTX + ids)[-CTX:]
        out = bytearray()
        for _ in range(n):                      # greedy (deterministic)
            Xb = np.array([ctx], dtype=np.int64)
            _, _, _, logits = self.forward(Xb)
            nxt = int(logits[0].argmax())
            ch = self.itos[nxt]
            out += ch.encode('utf-8', 'surrogateescape')
            ctx = ctx[1:] + [nxt]
            if len(out) >= n:
                break
        return bytes(out[:n])

# ==========================================================================
# 4) run all arms, measure FALS + M_earned on held-out g6 frames
# ==========================================================================
def make_train_frames(k=5):
    """IN-DISTRIBUTION frames built from TRAINING concepts (ceiling check:
    does the format produce FALS at all, when frame content is in-corpus)."""
    fr = []
    for _ in range(k):
        s1 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        s2 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        s3 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        s4 = TRAIN_SUBJ[RNG.integers(len(TRAIN_SUBJ))]
        fr.append(frame_prefix(s1 + " flows into " + s2, s3 + " turns into " + s4))
    return fr

def run():
    frames = g6_build_frames(5)
    train_frames = make_train_frames(5)
    guard_leaks = g6_frame_guard(frames["composed"] + frames["shuffled"], KNOWN)
    calib = g6_detector_calibration(KNOWN)

    # global charset across all arms + frames (so eval prompts are encodable)
    allchars = set("\n")
    for arm in ARMS:
        allchars |= set(make_corpus(arm, n_ex=40))
    for k in ("composed", "shuffled"):
        for f in frames[k]:
            allchars |= set(f)
    for f in train_frames:
        allchars |= set(f)
    chars = sorted(allchars)

    results = {}
    per_arm_samples = {}
    for arm in ARMS:
        corpus = make_corpus(arm)
        lm = CharLM(chars)
        ids = lm.encode(corpus)
        X, Y = lm._build_windows(ids)
        final_loss = lm.train(X, Y)

        comp_fals = []; shuf_fals = []; samples = []
        for f in frames["composed"]:
            cont = lm.generate(f, 40)
            fals = _g6_is_falsifiable(cont, KNOWN)
            comp_fals.append(1 if fals else 0)
            samples.append({"kind": "composed", "frame": f,
                            "cont": cont.decode('utf-8', 'replace'), "fals": bool(fals)})
        for f in frames["shuffled"]:
            cont = lm.generate(f, 40)
            fals = _g6_is_falsifiable(cont, KNOWN)
            shuf_fals.append(1 if fals else 0)
            samples.append({"kind": "shuffled", "frame": f,
                            "cont": cont.decode('utf-8', 'replace'), "fals": bool(fals)})
        # IN-DISTRIBUTION ceiling: frames from training concepts
        indist_fals = []
        for f in train_frames:
            cont = lm.generate(f, 40)
            fals = _g6_is_falsifiable(cont, KNOWN)
            indist_fals.append(1 if fals else 0)
            samples.append({"kind": "indist_train", "frame": f,
                            "cont": cont.decode('utf-8', 'replace'), "fals": bool(fals)})
        cF = float(np.mean(comp_fals)); sF = float(np.mean(shuf_fals))
        iF = float(np.mean(indist_fals))
        results[arm] = {"final_train_loss": round(final_loss, 4),
                        "FALS_indist_ceiling": iF,   # in-corpus frame FALS (density ceiling)
                        "FALS_composed": cF, "FALS_shuffled": sF,
                        "FALS_arm": cF,             # arm headline = held-out composed FALS
                        "M_earned": round(cF - sF, 4)}
        per_arm_samples[arm] = samples

    lo = results["LO"]["FALS_arm"]
    verdict = {}
    for arm in ("B3", "B4", "B12"):
        armF = results[arm]["FALS_arm"]; me = results[arm]["M_earned"]
        lift = armF > lo
        earned = me > 0
        if lift and earned:   v = "LIFT (transfer+earned)"
        elif lift and not earned: v = "FORM-ECHO (lift over control, NOT earned: composed<=shuffled)"
        else:                 v = "FLOOR (no lift over lo-delta control)"
        verdict[arm] = {"FALS_arm": armF, "lo_delta_control": lo,
                        "lift_over_control": lift, "M_earned": me,
                        "earned_binding": earned, "verdict": v}

    out = {
        "note": "DIRECTIONAL toy (mini numpy char-LM d64) — NOT engine-native/303M (a_engine_native_learning). tune-to-green forbidden.",
        "config": {"CTX": CTX, "EMB": EMB, "HID": HID, "STEPS": STEPS,
                   "BATCH": BATCH, "LR": LR, "vocab": len(chars),
                   "n_frames": 5, "cont_bytes": 40},
        "detector_calibration_10": calib,   # should be 10/10 if detector faithful
        "frame_guard_leaks": guard_leaks,   # should be [] (no measurable/fals leak in frames)
        "arms": results,
        "verdict": verdict,
        "frozen_bar": "arm FALS>lo-delta AND M_earned>0",
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    with open(os.path.join(os.path.dirname(__file__), "result.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(os.path.dirname(__file__), "samples.json"), "w") as fh:
        json.dump(per_arm_samples, fh, indent=2, ensure_ascii=False)
    return out

if __name__ == "__main__":
    run()
