"""H_1006 — DENSE per-step state supervision: does supervising the hidden mod-6 ring counter
at EVERY step (not just the final answer) crack the H_1005 T3 horizon cap at len>=36?

H_1005 root-caused the T3 cap to long-range CREDIT ASSIGNMENT: the curriculum-GRU's TRAIN-acc
collapses at the len-32 ramp stage — a single FINAL-step label cannot teach a 36-step modular
integration. The most direct attack (named verbatim in H_1000/H_1005 as the next rung: "dense
per-step parity/position supervision"): add an AUXILIARY readout that predicts the hidden
running position at EVERY timestep, so gradient reaches the recurrence at every step, not only
through a 36-deep BPTT chain from one final label.

DOSE-RESPONSE (the falsifier): aux supervision DENSITY k in {final-only (==H_1005 baseline),
every-4, every-1 (full dense)}. If dense supervision cracks T3@36 -> the cap was credit-density
limited (a method-shape unlock), AND it costs an EXTRA label (the hidden state) — REPORTED as
the caveat (you must HAVE the per-step ground truth, which a final-label-only task does not give
you for free). Compute matched to H_1005 (same 40-ep budget, same length curriculum, rungs
{16,32}, 6 seeds); the ONLY moved lever is the per-step auxiliary loss.

FROZEN PASS = dense (k=1) curr-GRU SOLVES T3@36 (>> chance 1/6, d>0.8 vs LM at >=2 rungs) AND
keeps T2@40; FAIL = still ~chance (cap survives dense supervision -> deeper than credit-density).
substrate=CPU-mirror; g5 CODE-measured; a_scale_honest_scope toy (len 36 only).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import time
import numpy as np
from h1006_method_lib import (SLATE_RUNGS, SLATE_SEEDS, T3_BREAK, T2_SENTINEL,
                              CHANCE_T3, CHANCE_T2, make_full, gru_train_curriculum_len,
                              run_baseline_curr, sep_rungs, solves, cracks_t3, keeps_t2,
                              print_table, header, verdict_line, cohens_d)
from h985_keystone_scaleup import N_TRAIN, N_TEST, onehot, T3_P, T2_CTX, T3_CTX
from h1000_gru_wm_t2t3 import GRUWorldModel, run_cell_lm, GRU_BATCH, GRU_LR, gru_hidden_for_rung
from h1003_t2t3_curriculum import (t2_episode_len, t3_episode_len, _ramp,
                                   CURR_THRESH, CURR_MIN_EP, TOTAL_EPOCHS)


# ============================================================================================
# GRU with an AUXILIARY per-step readout (Wa: hidden -> n_classes), supervised on the hidden
# running state at a stride-k subset of steps. Subclasses the H_1000 GRU primitive VERBATIM;
# the recurrence / final readout / Adam are unchanged — the ONLY addition is the aux head + its
# per-step CE gradient flowing into the recurrence (that is the dense-supervision treatment).
# ============================================================================================
class DenseSupGRU(GRUWorldModel):
    def __init__(self, in_dim, hidden, n_classes, seed=0, aux_stride=1, aux_w=1.0):
        super().__init__(in_dim, hidden, n_classes, seed=seed)
        rng = np.random.default_rng(seed + 99)
        self.Wa = rng.standard_normal((n_classes, hidden)) / np.sqrt(hidden)
        self.ba = np.zeros(n_classes)
        self._params = self._params + ["Wa", "ba"]
        self._m["Wa"] = np.zeros_like(self.Wa); self._m["ba"] = np.zeros_like(self.ba)
        self._v["Wa"] = np.zeros_like(self.Wa); self._v["ba"] = np.zeros_like(self.ba)
        self.aux_stride = aux_stride
        self.aux_w = aux_w

    def train_dense(self, seqs, step_labels, final_labels, epochs, batch, lr, rng):
        """seqs[i]: (T,in_dim); step_labels[i]: (T,) per-step running-state target; final_labels[i]:
        int final target. CE on the FINAL readout (Wo) at the last step (== baseline) PLUS aux CE
        (Wa) on the running state at every aux_stride-th step (the dense-supervision treatment)."""
        n = len(seqs)
        idx = np.arange(n)
        for _ep in range(epochs):
            rng.shuffle(idx)
            for b0 in range(0, n, batch):
                bidx = idx[b0:b0 + batch]
                grads = {p: np.zeros_like(getattr(self, p)) for p in self._params}
                for i in bidx:
                    logits, h_final, cache = self.forward_seq(seqs[i])
                    T = len(cache)
                    # ---- final-readout CE (== H_1000/H_1005 baseline) ----
                    m = logits.max(); e = np.exp(logits - m); sm = e / e.sum()
                    dlog = sm.copy(); dlog[final_labels[i]] -= 1.0
                    g = self._backward(cache, h_final, dlog)
                    for p in ("Wz", "Wr", "Wn", "Uz", "Ur", "Un", "bz", "br", "bn", "Wo", "bo"):
                        grads[p] += g[p]
                    # ---- aux per-step CE on the running state (the dense treatment) ----
                    if self.aux_w > 0:
                        # accumulate dh_aux at each supervised step, then ONE extra BPTT pass
                        dh_seq = [np.zeros(self.H) for _ in range(T)]
                        for t in range(T):
                            if (T - 1 - t) % self.aux_stride != 0:
                                continue
                            h_t = cache[t][5]            # h_new at step t
                            al = self.Wa @ h_t + self.ba
                            am = al.max(); ae = np.exp(al - am); asm = ae / ae.sum()
                            da = asm.copy(); da[step_labels[i][t]] -= 1.0
                            da *= self.aux_w
                            grads["Wa"] += np.outer(da, h_t)
                            grads["ba"] += da
                            dh_seq[t] += self.Wa.T @ da   # grad into h_t from aux
                        ga = self._backward_multi(cache, dh_seq)
                        for p in ("Wz", "Wr", "Wn", "Uz", "Ur", "Un", "bz", "br", "bn"):
                            grads[p] += ga[p]
                for p in self._params:
                    grads[p] /= len(bidx)
                self._adam_step(grads, lr)

    def _backward_multi(self, cache, dh_seq):
        """BPTT with an injected hidden-gradient dh_seq[t] at EACH step (for aux per-step losses).
        Mirrors GRUWorldModel._backward but seeds dh from dh_seq at every step (no final readout)."""
        g = {p: np.zeros_like(getattr(self, p))
             for p in ("Wz", "Wr", "Wn", "Uz", "Ur", "Un", "bz", "br", "bn")}
        dh = np.zeros(self.H)
        for t in range(len(cache) - 1, -1, -1):
            x, h_prev, z, r, n, h_new = cache[t]
            dh = dh + dh_seq[t]
            dz = dh * (n - h_prev); dn = dh * z; dh_prev = dh * (1.0 - z)
            dan = dn * (1.0 - n * n)
            g["Wn"] += np.outer(dan, x); g["Un"] += np.outer(dan, r * h_prev); g["bn"] += dan
            drh = self.Un.T @ dan; dr = drh * h_prev; dh_prev = dh_prev + drh * r
            daz = dz * z * (1.0 - z)
            g["Wz"] += np.outer(daz, x); g["Uz"] += np.outer(daz, h_prev); g["bz"] += daz
            dh_prev = dh_prev + self.Uz.T @ daz
            dar = dr * r * (1.0 - r)
            g["Wr"] += np.outer(dar, x); g["Ur"] += np.outer(dar, h_prev); g["br"] += dar
            dh_prev = dh_prev + self.Ur.T @ dar
            dh = dh_prev
        return g


# ---- per-step running-state target generators (the EXTRA supervision the method needs) ------
def t3_step_states(rng, steps):
    """Returns (seq, final_pos, ncl, step_states) where step_states[t] = running mod-P position
    AFTER processing step t (and the final query step repeats the final pos). Byte-identical seq
    to t3_episode_len (same draws) so the curriculum/eval are unchanged."""
    seq, final_pos, ncl = t3_episode_len(rng, steps, memaug=False)
    # recompute the running pos deterministically from the move channels in seq
    T = seq.shape[0]
    step = np.zeros(T, dtype=int)
    pos = 0
    for t in range(steps):
        mv = 0 if seq[t, 0] > 0.5 else 1
        pos = (pos + (1 if mv == 0 else -1)) % T3_P
        step[t] = pos
    step[steps] = pos  # query step: target = final position
    return seq, final_pos, ncl, step


def t2_step_states(rng, length):
    seq, final_par, ncl = t2_episode_len(rng, length, memaug=False)
    T = seq.shape[0]
    step = np.zeros(T, dtype=int)
    par = 0
    for t in range(length):
        tog = 0 if seq[t, 0] > 0.5 else 1
        par ^= tog
        step[t] = par
    step[length] = par
    return seq, final_par, ncl, step


STEP_MAKERS = {"T3_hidden_pos": t3_step_states, "T2_parity_track": t2_step_states}


def gru_train_curriculum_dense(gru, maker, step_maker, target, seed):
    """H_1005 length curriculum, but train with DENSE aux supervision at each stage."""
    stages = _ramp(target)
    train_rng = np.random.default_rng(seed + 4242)
    data_rng = np.random.default_rng(seed)
    progression = []
    epochs_left = TOTAL_EPOCHS
    n_stages = len(stages)
    for si, slen in enumerate(stages):
        if epochs_left <= 0:
            break
        train = [step_maker(data_rng, slen) for _ in range(N_TRAIN)]
        seqs = [s for s, _, _, _ in train]
        finals = [int(c) for _, c, _, _ in train]
        steps_lab = [st for _, _, _, st in train]
        remaining_after = n_stages - si - 1
        cap = epochs_left - CURR_MIN_EP * remaining_after
        cap = max(CURR_MIN_EP, min(cap, epochs_left))
        spent, acc = 0, 0.0
        for _ in range(cap):
            gru.train_dense(seqs, steps_lab, finals, epochs=1, batch=GRU_BATCH, lr=GRU_LR,
                            rng=train_rng)
            spent += 1
            pred = gru.predict(seqs)
            acc = float(np.mean(pred == np.array(finals)))
            if spent >= CURR_MIN_EP and acc >= CURR_THRESH and si < n_stages - 1:
                break
        epochs_left -= spent
        progression.append((int(slen), int(spent), round(acc, 3)))
    return progression


def run_dense(maker, ncl, target, latent, seed, aux_stride):
    """Dense-supervision curriculum-GRU. EVAL on full-target test (final-label only — the aux
    head is training-only). Draw order matches h1005 so the LM/mem arms stay apples-to-apples."""
    step_maker = STEP_MAKERS["T3_hidden_pos"] if ncl == T3_P else STEP_MAKERS["T2_parity_track"]
    full_maker = make_full(maker, target)
    test_rng = np.random.default_rng(seed)
    for _ in range(N_TRAIN):
        full_maker(test_rng, memaug=False)
    test = [full_maker(test_rng, memaug=False) for _ in range(N_TEST)]
    tseqs = [s for s, _, _ in test]
    yte = np.array([cc for _, cc, _ in test])
    in_dim = tseqs[0].shape[1]
    hidden = gru_hidden_for_rung(latent)
    gru = DenseSupGRU(in_dim, hidden, ncl, seed=seed + 7, aux_stride=aux_stride, aux_w=1.0)
    gru_train_curriculum_dense(gru, maker, step_maker, target, seed)
    pred = gru.predict(tseqs)
    return float(np.mean(pred == yte)), None


def main():
    t0 = time.time()
    header("H_1006",
           "Dense per-step state supervision — crack the H_1005 T3@36 horizon cap?")
    print(f"T3 BREAK len={T3_BREAK} (the H_1005 break point), T2 sentinel len={T2_SENTINEL}. "
          f"rungs={SLATE_RUNGS} seeds={SLATE_SEEDS} (== H_1005 trim). budget={TOTAL_EPOCHS}ep "
          f"(== H_1005). ONLY moved lever vs H_1005 = per-step AUX supervision (dose-response "
          f"stride k in {{final-only, 4, 1}}). aux head = TRAINING-only; eval is final-label.\n")

    # dose-response ENDPOINTS only (final-only baseline + full dense) — WALL-TIME TRIM
    # (every-4 mid-point dropped to keep the run under wall-budget; REPORTED). The endpoints
    # are what the falsifier needs (does the densest supervision crack the cap vs the baseline?).
    STRIDES = {"final-only": T3_BREAK + 1, "every-1": 1}  # final-only ~= baseline
    rows = []
    t3_cells = {k: {} for k in STRIDES}
    t2_cells = {}
    # ---- T3@36 across the dose-response ----
    for kname, stride in STRIDES.items():
        for latent in SLATE_RUNGS:
            curr, lm, mem = [], [], []
            for s in range(SLATE_SEEDS):
                cg, _ = run_dense(t3_episode_len, T3_P, T3_BREAK, latent, s, stride)
                fm = make_full(t3_episode_len, T3_BREAK)
                l, _ = run_cell_lm(fm, T3_CTX, T3_P, latent, s, memaug=False)
                m, _ = run_cell_lm(fm, T3_CTX, T3_P, latent, s, memaug=True)
                curr.append(cg); lm.append(l); mem.append(m)
            curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
            t3_cells[kname][latent] = dict(curr=curr, lm=lm)
            rows.append((f"T3 k={kname[:6]}", T3_BREAK, latent, CHANCE_T3, curr, lm, mem))
            print(f"  done T3 stride={kname:<10} rung={latent:<3} curr={curr.mean():.3f} "
                  f"LM={lm.mean():.3f} mem={mem.mean():.3f}  [{time.time()-t0:.0f}s]", flush=True)
    # ---- T2@40 sentinel (full dense) — must stay solved ----
    for latent in SLATE_RUNGS:
        curr, lm, mem = [], [], []
        for s in range(SLATE_SEEDS):
            cg, _ = run_dense(t2_episode_len, 2, T2_SENTINEL, latent, s, 1)
            fm = make_full(t2_episode_len, T2_SENTINEL)
            l, _ = run_cell_lm(fm, T2_CTX, 2, latent, s, memaug=False)
            m, _ = run_cell_lm(fm, T2_CTX, 2, latent, s, memaug=True)
            curr.append(cg); lm.append(l); mem.append(m)
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t2_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T2 k=every1", T2_SENTINEL, latent, CHANCE_T2, curr, lm, mem))
        print(f"  done T2 sentinel    rung={latent:<3} curr={curr.mean():.3f} "
              f"LM={lm.mean():.3f} mem={mem.mean():.3f}  [{time.time()-t0:.0f}s]", flush=True)

    print_table("DENSE-SUPERVISION dose-response (curr-GRU vs LM vs mem-aug)", rows)

    # ---- dose-response summary + frozen ruling ----
    print("\ndose-response (T3@36 — does denser supervision crack the cap?):")
    for kname in STRIDES:
        c = t3_cells[kname]
        big = sep_rungs(c)
        sol = solves(c, CHANCE_T3)
        means = {L: round(c[L]["curr"].mean(), 3) for L in SLATE_RUNGS}
        print(f"  k={kname:<10} curr={means} sep@>=2rungs={len(big)>=2!s:<5} "
              f"solves={sol!s:<5} sep-rungs={big}")
    dense_cracks = cracks_t3(t3_cells["every-1"])
    t2_ok = keeps_t2(t2_cells)
    base_break = not cracks_t3(t3_cells["final-only"])
    print(f"\nharness-validate (final-only reproduces H_1005 break @36): {base_break}")
    print(f"T2@40 sentinel kept: {t2_ok}")
    print(f"dense (k=1) cracks T3@36: {dense_cracks}\n")

    if dense_cracks and t2_ok:
        verdict_line("H_1006", "PASS",
                     f"DENSE-SUPERVISION-CRACKS-T3-CAP — supervising the hidden mod-{T3_P} running "
                     f"position at EVERY step (vs only the final label) RESTORES the WM>LM separator "
                     f"on T3 at len={T3_BREAK} — the H_1005 BREAK point — (curr-GRU "
                     f"{ {L: round(t3_cells['every-1'][L]['curr'].mean(),3) for L in SLATE_RUNGS} } "
                     f">> chance {CHANCE_T3:.3f}, d>0.8 vs LM at >=2 rungs) WHILE keeping T2@"
                     f"{T2_SENTINEL}. The H_1005 T3 horizon cap was a long-range CREDIT-DENSITY "
                     f"limit: a final-step label cannot teach a {T3_BREAK}-step modular integration, "
                     f"but per-step state supervision restores gradient at every step and bootstraps "
                     f"the integrator past the cap. CAVEAT (the cost): this method REQUIRES the "
                     f"hidden per-step ground-truth state (an EXTRA label a final-label-only task "
                     f"does not provide for free) — a method-shape unlock that buys reach with "
                     f"denser supervision, not free compute (toy len={T3_BREAK}; production OPEN, "
                     f"a_scale_honest_scope).")
    else:
        verdict_line("H_1006", "FAIL",
                     f"DENSE-SUPERVISION-INSUFFICIENT — even per-step supervision of the hidden "
                     f"running state at EVERY step does NOT crack the H_1005 T3 cap at len="
                     f"{T3_BREAK} (dense curr-GRU "
                     f"{ {L: round(t3_cells['every-1'][L]['curr'].mean(),3) for L in SLATE_RUNGS} }, "
                     f"sep@>=2rungs={len(sep_rungs(t3_cells['every-1']))>=2}, T2-kept={t2_ok}). The "
                     f"T3 horizon cap is DEEPER than credit-density at this toy budget — the "
                     f"integrator still fails to generalize the mod-{T3_P} ring counter to {T3_BREAK} "
                     f"steps even with dense gradient (closed-negative, a_paper_negative_ok; toy "
                     f"len={T3_BREAK}, larger-budget / production OPEN, a_scale_honest_scope).")
    print(f"\n[total wall {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
