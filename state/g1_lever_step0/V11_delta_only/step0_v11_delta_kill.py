#!/usr/bin/env python3
"""G1 LEVER-1 family / V11 delta-only (delta-encoding) — STEP-0 CHEAP ENGINE-NATIVE KILL.

Lever-1 axis = TARGET FORMAT (data-format), NOT the trunk combiner (combiner held ADDITIVE
for all arms; DPI meta-law says operator-shape is invariant). Each arm changes only how the
held-out recombination target is STAGED, then trains a control-gated slot-readout on the SAME
additive fusion c = Wa@E[i] + Wb@E[j] with plain CE / BCE (NOT recomb-rigged). torch-free numpy.

Arms (3, per FROZEN BAR: probe + 2 controls):
  ADD   : additive-control. Single multi-label readout over c -> top-2 (gamma-shape floor).
          target = {i,j} in one softmax/sigmoid step. No slot staging.
  DERIV : derivtrace baseline (bd=2 reference). Two slot-gated decode steps with distinct
          learned controls gA,gB. logits_A->i, logits_B->j. Staging turns joint-decode into two
          shared per-slot linear rules (rho~=0) -> generalizes to held-out.
  V11   : delta-only. Step1 slot-gated decode of i (gI). Step2 decodes a DELTA token
          d=(j-i) mod N over a separate delta head (gD). Reconstruct j = (i + d) mod N.
          Difference operator actively REMOVES the echo of state (rho down) but the target is
          short (M small) so the memorization-disadvantage margin is small -> predicted margin < DERIV.

FROZEN BAR (pre-registered, no post-hoc move): real-G1-homomorphic toy N=24 D=64 heldout~0.45
  4000 step seeds {7,4302,4303}. Metric = held-out mean distinct-correct constituents per pair
  (in [0,2]) = best_distinct(bd); bd2_rate secondary. max_single = single-concept mean distinct.
  Lever PASS iff bd_lever > bd_ADD  AND  bd_lever > max_single  AND
                 margin(lever - ADD) > margin(DERIV - ADD).
  KILL iff bd_lever <= bd_ADD  OR  margin(lever-ADD) <= margin(DERIV-ADD).
Pre-registered prediction (V2 > DERIV > V11): V11 rho down (<= DERIV) but M small -> margin < DERIV
  -> V11 = KILL vs DERIV baseline (does NOT beat derivtrace, not a GPU-escalation candidate).
DIRECTIONAL only (numpy toy, a_engine_native_learning: 303M engine-native not run, NOT terminal).
"""
import json, time
import numpy as np

N = 24; D = 64; H = 96; HELDOUT = 0.45; STEPS = 4000; LR = 3e-3
SEEDS = [7, 4302, 4303]; ARMS = ["ADD", "DERIV", "V11"]


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3)))


def dgelu(x):
    c = 0.7978845608; u = c * (x + 0.044715 * x ** 3); t = np.tanh(u)
    du = c * (1.0 + 3 * 0.044715 * x ** 2)
    return 0.5 * (1.0 + t) + 0.5 * x * (1.0 - t ** 2) * du


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True); e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


class Model:
    def __init__(self, arm, rng):
        s = 1.0 / np.sqrt(D); self.arm = arm; self.rng = rng
        self.P = {
            "E":  rng.standard_normal((N, D)) * s,
            "Wa": np.eye(D) + rng.standard_normal((D, D)) * 0.05,
            "Wb": np.eye(D) + rng.standard_normal((D, D)) * 0.05,
            "W1": rng.standard_normal((H, 2 * D)) * (1.0 / np.sqrt(2 * D)),
            "b1": np.zeros(H),
            "Wc": rng.standard_normal((N, H)) * (1.0 / np.sqrt(H)),
            "bc": np.zeros(N),
            "Wd": rng.standard_normal((N, H)) * (1.0 / np.sqrt(H)),
            "bd": np.zeros(N),
            "gADD": rng.standard_normal(D) * s,
            "gA":   rng.standard_normal(D) * s,
            "gB":   rng.standard_normal(D) * s,
            "gI":   rng.standard_normal(D) * s,
            "gD":   rng.standard_normal(D) * s,
        }

    def context(self, ii, jj):
        a = self.P["E"][ii]; b = self.P["E"][jj]
        pa = a @ self.P["Wa"].T; pb = b @ self.P["Wb"].T
        return pa + pb, (ii, jj, a, b)

    def read(self, c, g, head):
        B = c.shape[0]; gb = np.broadcast_to(g, (B, D))
        x = np.concatenate([c, gb], axis=1)
        z1 = x @ self.P["W1"].T + self.P["b1"]
        z = gelu(z1)
        Wh, bh = ("Wc", "bc") if head == "concept" else ("Wd", "bd")
        logits = z @ self.P[Wh].T + self.P[bh]
        return logits, (x, z1, z, Wh, bh, g)

    def read_bwd(self, dlogits, cache, grads):
        x, z1, z, Wh, bh, g = cache
        grads[Wh] += dlogits.T @ z; grads[bh] += dlogits.sum(0)
        dz = dlogits @ self.P[Wh]; dz1 = dz * dgelu(z1)
        grads["W1"] += dz1.T @ x; grads["b1"] += dz1.sum(0)
        dx = dz1 @ self.P["W1"]
        dc = dx[:, :D]; dg = dx[:, D:].sum(0)
        return dc, dg

    def ctx_bwd(self, dc, cctx, grads):
        ii, jj, a, b = cctx
        grads["Wa"] += dc.T @ a; grads["Wb"] += dc.T @ b
        da = dc @ self.P["Wa"]; db = dc @ self.P["Wb"]
        np.add.at(grads["E"], ii, da); np.add.at(grads["E"], jj, db)

    def loss_grad(self, batch, grads):
        ii = batch[:, 0]; jj = batch[:, 1]; B = len(ii)
        c, cctx = self.context(ii, jj)
        loss = 0.0
        if self.arm == "ADD":
            logits, ca = self.read(c, self.P["gADD"], "concept")
            p = sigmoid(logits); y = np.zeros((B, N))
            y[np.arange(B), ii] = 1.0; y[np.arange(B), jj] = 1.0
            loss = -(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9)).sum() / B
            dlogits = (p - y) / B
            dc, _ = self.read_bwd(dlogits, ca, grads)
            self.ctx_bwd(dc, cctx, grads)
        elif self.arm == "DERIV":
            for gkey, tgt in [("gA", ii), ("gB", jj)]:
                logits, ca = self.read(c, self.P[gkey], "concept")
                p = softmax(logits)
                loss += -np.log(p[np.arange(B), tgt] + 1e-9).sum() / B
                dl = p.copy(); dl[np.arange(B), tgt] -= 1.0; dl /= B
                dc, dg = self.read_bwd(dl, ca, grads); grads[gkey] += dg
                self.ctx_bwd(dc, cctx, grads)
        else:  # V11 delta-only
            logits, ca = self.read(c, self.P["gI"], "concept")
            p = softmax(logits)
            loss += -np.log(p[np.arange(B), ii] + 1e-9).sum() / B
            dl = p.copy(); dl[np.arange(B), ii] -= 1.0; dl /= B
            dc1, dg = self.read_bwd(dl, ca, grads); grads["gI"] += dg
            self.ctx_bwd(dc1, cctx, grads)
            dtok = (jj - ii) % N
            logits2, ca2 = self.read(c, self.P["gD"], "delta")
            p2 = softmax(logits2)
            loss += -np.log(p2[np.arange(B), dtok] + 1e-9).sum() / B
            dl2 = p2.copy(); dl2[np.arange(B), dtok] -= 1.0; dl2 /= B
            dc2, dg2 = self.read_bwd(dl2, ca2, grads); grads["gD"] += dg2
            self.ctx_bwd(dc2, cctx, grads)
        return loss

    def decode_bd(self, i, j):
        c, _ = self.context(np.array([i]), np.array([j]))
        if self.arm == "ADD":
            logits, _ = self.read(c, self.P["gADD"], "concept")
            rec = set(np.argsort(logits[0])[-2:].tolist())
        elif self.arm == "DERIV":
            la, _ = self.read(c, self.P["gA"], "concept")
            lb, _ = self.read(c, self.P["gB"], "concept")
            rec = {int(np.argmax(la[0])), int(np.argmax(lb[0]))}
        else:
            li, _ = self.read(c, self.P["gI"], "concept")
            ld, _ = self.read(c, self.P["gD"], "delta")
            pi = int(np.argmax(li[0])); pd = int(np.argmax(ld[0]))
            rec = {pi, (pi + pd) % N}
        return len({i, j} & rec)


def make_data(rng):
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    rng.shuffle(pairs)
    ncut = int(len(pairs) * (1 - HELDOUT))
    return pairs[:ncut], pairs[ncut:]


def train_arm(arm, seed):
    rng = np.random.default_rng(seed); m = Model(arm, rng)
    trp, tep = make_data(rng)
    singles = [(i, i) for i in range(N)]
    data = np.array(singles + trp, dtype=np.int64)
    P = m.P; mom = {k: np.zeros_like(v) for k, v in P.items()}
    vel = {k: np.zeros_like(v) for k, v in P.items()}
    b1a, b2a, eps = 0.9, 0.999, 1e-8
    for step in range(1, STEPS + 1):
        idx = rng.permutation(len(data)); batch = data[idx]
        grads = {k: np.zeros_like(v) for k, v in P.items()}
        m.loss_grad(batch, grads)
        for k in P:
            g = grads[k]; mom[k] = b1a * mom[k] + (1 - b1a) * g
            vel[k] = b2a * vel[k] + (1 - b2a) * (g * g)
            mh = mom[k] / (1 - b1a ** step); vh = vel[k] / (1 - b2a ** step)
            P[k] -= LR * mh / (np.sqrt(vh) + eps)
    return m, trp, tep


def eval_arm(m, trp, tep):
    tr = np.mean([m.decode_bd(i, j) for (i, j) in trp])
    te = np.mean([m.decode_bd(i, j) for (i, j) in tep])
    te2 = np.mean([1.0 if m.decode_bd(i, j) == 2 else 0.0 for (i, j) in tep])
    sa = np.mean([m.decode_bd(i, i) for i in range(N)])
    return tr, te, te2, sa


def gradient_check():
    out = {}
    for arm in ARMS:
        rng = np.random.default_rng(123); m = Model(arm, rng)
        batch = np.array([(0, 3), (1, 5), (2, 7)], dtype=np.int64)
        grads = {k: np.zeros_like(v) for k, v in m.P.items()}
        m.loss_grad(batch, grads)
        worst = 0.0
        keyset = ["W1", "Wc", "Wa", "E",
                  "gA" if arm == "DERIV" else ("gD" if arm == "V11" else "gADD")]
        for k in keyset:
            arr = m.P[k]; flat = arr.reshape(-1); gflat = grads[k].reshape(-1)
            for t in range(min(6, flat.size)):
                orig = flat[t]; h = 1e-5
                flat[t] = orig + h
                lp = m.loss_grad(batch, {kk: np.zeros_like(vv) for kk, vv in m.P.items()})
                flat[t] = orig - h
                lm = m.loss_grad(batch, {kk: np.zeros_like(vv) for kk, vv in m.P.items()})
                flat[t] = orig
                num = (lp - lm) / (2 * h); ana = gflat[t]
                rel = abs(num - ana) / (abs(num) + abs(ana) + 1e-9)
                worst = max(worst, rel)
        out[arm] = float(worst)
    return out


def predictors(seed=7):
    from collections import defaultdict
    rng = np.random.default_rng(seed); trp, tep = make_data(rng)
    res = {}
    res["ADD"] = {"rho": 1.0, "sigma": 1, "kappa": 0.0, "delta_copy": 0, "RF": 999,
                  "M": 2.0 / 2.0, "note": "no slot staging; joint-decode floor"}
    sigA = len({i for (i, j) in trp} | set(range(N)))
    sigB = len({j for (i, j) in trp} | set(range(N)))
    res["DERIV"] = {"rho": 0.0, "sigma": int(min(sigA, sigB)), "kappa": 1.0, "delta_copy": 1,
                    "RF": 999, "M": 4.0 / 2.0,
                    "note": "2 slot-reads; both kappa=1 read-from-ctx; |tau|=4/desc2"}
    dpart = defaultdict(set)
    for (i, j) in trp:
        dpart[(j - i) % N].add(i)
    train_dvals = set(dpart.keys())
    heldout_dvals = {(j - i) % N for (i, j) in tep}
    residual_d = heldout_dvals - train_dvals
    rho_v11 = 0.5 * (len(residual_d) / max(1, len(heldout_dvals)))
    sig_v11 = min(len(v) for v in dpart.values()) if dpart else 1
    res["V11"] = {"rho": round(rho_v11, 3), "sigma": int(sig_v11), "kappa": 0.5, "delta_copy": 1,
                  "RF": 999, "M": 2.0 / 2.0,
                  "note": "read i + computed delta; echo removed rho down; short tau -> M small"}
    return res


def main():
    t0 = time.time()
    gc = gradient_check()
    preds = predictors()
    res = {a: {"tr": [], "te": [], "te2": [], "sa": []} for a in ARMS}
    for seed in SEEDS:
        for arm in ARMS:
            m, trp, tep = train_arm(arm, seed)
            tr, te, te2, sa = eval_arm(m, trp, tep)
            res[arm]["tr"].append(tr); res[arm]["te"].append(te)
            res[arm]["te2"].append(te2); res[arm]["sa"].append(sa)
            print("[seed %d] %-5s train_bd=%.3f HELDOUT_bd=%.3f bd2_rate=%.3f max_single=%.3f"
                  % (seed, arm, tr, te, te2, sa), flush=True)
    summ = {a: {
        "held_out_best_distinct_mean": float(np.mean(res[a]["te"])),
        "held_out_bd_seeds": [round(x, 3) for x in res[a]["te"]],
        "held_out_bd2_rate_mean": float(np.mean(res[a]["te2"])),
        "train_bd_mean": float(np.mean(res[a]["tr"])),
        "max_single_mean": float(np.mean(res[a]["sa"])),
    } for a in ARMS}
    add_bd = summ["ADD"]["held_out_best_distinct_mean"]
    dev_bd = summ["DERIV"]["held_out_best_distinct_mean"]
    v11_bd = summ["V11"]["held_out_best_distinct_mean"]
    max_single = summ["V11"]["max_single_mean"]
    deriv_margin = dev_bd - add_bd
    v11_margin = v11_bd - add_bd
    lever_pass = (v11_bd > add_bd) and (v11_bd > max_single) and (v11_margin > deriv_margin)
    kill = not lever_pass
    predicted_pass = False
    verdict = (
        "KILL (V11 delta-only margin <= DERIV baseline margin => derivtrace NOT beaten; "
        "delta-encoding removes echo (rho down) but short target (M small) starves the margin => "
        "NOT a GPU-escalation candidate. DIRECTIONAL numpy toy, engine-native 303M NOT run.)"
        if kill else
        "ESCALATE (V11 delta-only margin > DERIV baseline margin => STEP-1 303M engine-native.)")
    out = {
        "experiment": "G1 lever-1/V11 delta-only STEP-0 cheap engine-native kill (DIRECTIONAL)",
        "config": {"N": N, "D": D, "H": H, "HELDOUT": HELDOUT, "STEPS": STEPS, "LR": LR, "seeds": SEEDS},
        "frozen_bar": ("held-out mean distinct-correct constituents (bd in [0,2]); lever PASS iff "
                       "bd_lever>bd_ADD AND bd_lever>max_single AND margin(lever-ADD)>margin(DERIV-ADD)"),
        "gradient_check_worst_rel_err": gc,
        "arms": summ,
        "ADD_held_out_bd": add_bd, "DERIV_held_out_bd": dev_bd, "V11_held_out_bd": v11_bd,
        "max_single": max_single,
        "DERIV_baseline_margin": deriv_margin, "V11_lever_margin": v11_margin,
        "lever_minus_deriv_margin": v11_margin - deriv_margin,
        "LEVER_PASS": lever_pass, "KILL": kill,
        "predicted_pass": predicted_pass,
        "prediction_hit": (lever_pass == predicted_pass),
        "predictors": preds,
        "VERDICT": verdict,
        "honesty": ("DIRECTIONAL only - numpy toy sequential slot-readout, real-G1-homomorphic. "
                    "a_engine_native_learning: 303M engine-native NOT run; terminal only after "
                    "anima evaluate --py on live core/ decode. No tune-to-green; bar frozen pre-run."),
        "wall_sec": round(time.time() - t0, 1),
    }
    print(json.dumps(out, indent=2))
    dst = "/Users/mini/dancinlab/anima/state/g1_lever_step0/V11_delta_only/result.json"
    open(dst, "w").write(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
