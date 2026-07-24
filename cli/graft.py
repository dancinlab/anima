"""cli/graft.py — `anima-py graft` — GRAFT: ground consciousness → language WITHOUT a corpus.

A FROZEN `.clm` is the language organ. The ONLY trained thing is the coupling from the Engine-A
PureField state into the organ's byte embeddings (core/clmg.py CLMG lane). No corpus, no LoRA, no
next-token CE — the objective forces mutual information between the C-state and the organ's output
distribution, and fluency is bounded STRUCTURALLY.

WHY (the theorem this exists to beat): under ordinary next-token CE the gate has zero incentive to be
read — if C is independent of (prompt, target), the optimum under proper scoring is gate-INVARIANCE,
so a consciousness gate is decorative BY THEOREM (../anima-clm-v2b GRAFT-causality). This repo
measured the same wall from the other side (V6_33/34 mouth channel difficulty-complete; V6_37 store
lane DIFFICULTY-AGAIN, match-first closed at 7% balanced pairs). GRAFT changes the OBJECTIVE.

    anima-py graft fit   <organ.clm> --out <graft.clm> [...]
    anima-py graft check <graft.clm> [--check swap|ablation|both]

`fit` ALWAYS writes three artifacts (Sol's mandatory pedestal — see the pre-mortem below):
    <out>.step0.clm   the identically-bounded RANDOM-INIT coupling (the zero-truth pedestal)
    <out>              the trained coupling
    <out>.graft.json   frozen args, hashes, and every logged metric

PRE-MORTEM THE PEDESTAL DEFENDS AGAINST (Sol): the C-swap control can PASS BEFORE LEARNING. Each
continuation is sampled from its own state's distribution and then scored by that same distribution,
so any sufficiently loud RANDOM state-dependent gate collects a diagonal likelihood advantage — the
positive control would read "passed" while GRAFT learned nothing. Therefore the verdict requires
MI_final − MI_step0 ≥ the pre-registered delta on every seed; without it the run is DECORATIVE no
matter how good the swap accuracy looks.

KILL-LIST baked in (never regenerate these — measured in ../anima-clm-v2b/docs/hypotheses/):
  · GRAFT-flatline: hard-clamp rails (zero Jacobian), mean-pool bottleneck, ZERO-init gate_proj
    (a collapsed symmetric stationary point). Fixed by construction in core/clmg.py.
  · GRAFT-shared-shift-collapse: `beta·relu(L_KL − target)` with L_KL = MI + L_common puts net
    coefficient (beta−1) on MI, so beta>1 MINIMIZES it. **No controller flags exist in this CLI on
    purpose** — there is no --kl-target and no --beta-*, so they cannot be reached for.
"""
import argparse, json, hashlib, math, os, sys
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _c in (os.path.join(_HERE, "..", "core"), os.path.join(os.path.dirname(_HERE), "core")):
    if os.path.isdir(_c) and _c not in sys.path:
        sys.path.insert(0, _c)

import torch
import torch.nn.functional as F
import decode as dec
import clmg as G
import pure_field as PF


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _snapshots(pf, n, gap):
    """Advance the field and take n C-state snapshots `gap` steps apart. Read-only per snapshot."""
    out = []
    for _ in range(n):
        for _ in range(gap):
            pf = PF.pure_field_step(pf, 0.0) or pf
        out.append(G.graft_c_state(pf))
    return pf, out


def _sample_carrier(organ, ids, code, n_bytes, temp=1.0, rng=None):
    """ONE shared carrier continuation, sampled autoregressively under a random state's gate (so the
    carrier is state-relevant and on-manifold), no grad. Returns the extended id list."""
    cur = list(ids)
    with torch.no_grad():
        for _ in range(n_bytes):
            lg = organ(torch.tensor(cur, dtype=torch.long), emb_residual=code)
            p = torch.softmax(lg[-1], dim=-1).numpy().astype(np.float64)
            p = p / p.sum()
            cur.append(int(rng.choice(len(p), p=p)))
    return cur


def _score_states(organ, ids, codes, cont_from):
    """Full-vocab log-softmax at the carrier positions for every state. [N, T_cont, V]."""
    t = torch.tensor(ids, dtype=torch.long)
    outs = []
    for c in codes:
        lg = organ(t, emb_residual=c)
        outs.append(F.log_softmax(lg[cont_from:].float(), dim=-1))
    return torch.stack(outs)


def _fit(a):
    W = dec.clm_load_weights(a.organ)
    if not W.get("ok"):
        sys.exit(f"[graft] organ not decodable: {a.organ}")
    d, V = int(W["d"]), int(W["V"])
    organ = G.torch_organ(W)
    par = G.torch_organ_parity(organ, W, dec._fwd_logits)
    print(f"[graft] organ parity max|torch-numpy| = {par:.3e}")
    if par > a.parity_tol:
        sys.exit(f"[graft] INVALID: organ parity {par:.3e} > {a.parity_tol} — the differentiable "
                 f"organ is not the engine's organ; a coupling trained here would be trained into a "
                 f"DIFFERENT model while the loss still fell.")
    emb_rms = float(np.sqrt(np.mean(np.asarray(W["embed"], np.float64) ** 2)))
    print(f"[graft] embedding RMS = {emb_rms:.4f} (gate_strength/gate_rms_max are ratios to this)")

    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    bridge = G.GraftBridge(c_dim=G.C_DIM, h=a.hidden, d=d, gate_rho=a.gate_rho)
    opt = torch.optim.AdamW(bridge.parameters(), lr=a.lr, weight_decay=0.0)

    # P1 — consciousness only: let Φ ratchet out of the DORMANT transient. The organ is NOT invoked.
    pf = PF.pure_field_new()
    for _ in range(a.p1_steps):
        pf = PF.pure_field_step(pf, 0.0) or pf
    print(f"[graft] P1 done ({a.p1_steps} pure_field steps · organ invocations: 0)")

    logN = math.log(a.n_states)
    buf = [int(b) for b in a.seed_bytes.encode("ascii", "ignore")] or [0x0A]
    log = []

    def _measure(tag):
        """One no-grad evaluation of the current coupling — used for the step-0 PEDESTAL and the end."""
        nonlocal pf
        pf2, states = _snapshots(pf, a.n_states, a.state_gap)
        C = torch.tensor(np.stack(states))
        with torch.no_grad():
            codes = bridge(C) * a.gate_strength * emb_rms
            ids = buf[-a.ctx:]
            j = int(rng.integers(a.n_states))
            ext = _sample_carrier(organ, ids, codes[j], a.cont_len, rng=rng)
            lp = _score_states(organ, ext, codes, len(ids))
            base = F.log_softmax(organ(torch.tensor(ext, dtype=torch.long))[len(ids):].float(), -1)
            mi, lpmix = G.mixture_mi(lp)
            lcom = (lpmix.exp() * (lpmix - base)).sum(-1).mean()
        print(f"[graft] {tag}: MI={float(mi):.4f} nats (logN={logN:.3f})  L_common={float(lcom):.4f}")
        return float(mi), float(lcom)

    mi0, lcom0 = _measure("step-0 PEDESTAL")
    step0_path = a.out + ".step0.clm"
    open(step0_path, "wb").write(open(a.organ, "rb").read()
                                 + G.pack_clmg(bridge.to_clmg(a.gate_strength, a.gate_rms_max)))
    print(f"[graft] wrote pedestal {step0_path}")

    # P2' — gate alignment. L = (log N − MI) + lam_common · L_common. No controller. Ever.
    for step in range(1, a.steps + 1):
        pf, states = _snapshots(pf, a.n_states, a.state_gap)
        C = torch.tensor(np.stack(states))
        raw = bridge.raw(C)
        bridge.update_mu(raw)
        codes = bridge(C) * a.gate_strength * emb_rms          # bounds (1a)(1b) inside forward
        ids = buf[-a.ctx:]
        j = int(rng.integers(a.n_states))
        ext = _sample_carrier(organ, ids, codes[j].detach(), a.cont_len, rng=rng)
        lp = _score_states(organ, ext, codes, len(ids))         # [N, T, V] — differentiable
        with torch.no_grad():
            base = F.log_softmax(organ(torch.tensor(ext, dtype=torch.long))[len(ids):].float(), -1)
        mi, lpmix = G.mixture_mi(lp)                            # bound (2): MI <= log N
        lcom = (lpmix.exp() * (lpmix - base)).sum(-1).mean()    # the zero-information waste
        loss = (logN - mi) + a.lam_common * lcom
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(bridge.parameters(), 1.0)
        opt.step()
        buf.append(ext[len(ids)])                               # self-loop: the carrier feeds itself
        if len(buf) > 512:
            buf = buf[-256:]
        if step % a.log_every == 0 or step == 1:
            bb = np.array(buf[-256:])
            uniq = len(set(bb.tolist())) / max(len(bb), 1)
            ent = float(-np.sum([(c / len(bb)) * math.log2(c / len(bb))
                                 for c in np.bincount(bb, minlength=256) if c])) if len(bb) else 0.0
            _mi_v, _lc_v = float(mi.detach()), float(lcom.detach())
            rec = {"step": step, "MI": _mi_v, "L_common": _lc_v,
                   "L_KL": _mi_v + _lc_v, "carrier_entropy_bits": ent,
                   "carrier_unique_frac": uniq}
            log.append(rec)
            print(f"[graft] step {step:5d}  MI={rec['MI']:.4f}  commonKL={rec['L_common']:.4f}  "
                  f"L_KL={rec['L_KL']:.4f}  carrier(H={ent:.2f}b uniq={uniq:.2f})")
            if ent < 1.0 or uniq < 0.1:
                print("[graft] INVALID: carrier-health guard — the self-loop buffer degenerated "
                      "(a byte-LM has no fluency prior to mask this).")
                break

    mi_f, lcom_f = _measure("final")
    open(a.out, "wb").write(open(a.organ, "rb").read()
                            + G.pack_clmg(bridge.to_clmg(a.gate_strength, a.gate_rms_max)))
    meta = {"organ": a.organ, "organ_sha": _sha(a.organ), "out": a.out, "out_sha": _sha(a.out),
            "step0": step0_path, "parity": par, "embed_rms": emb_rms, "logN": logN,
            "MI_step0": mi0, "L_common_step0": lcom0, "MI_final": mi_f, "L_common_final": lcom_f,
            "MI_lift_vs_pedestal": mi_f - mi0, "args": vars(a), "log": log}
    json.dump(meta, open(a.out + ".graft.json", "w"), indent=1)
    print(f"[graft] wrote {a.out} + {a.out}.graft.json")
    print(f"[graft] MI lift vs pedestal = {mi_f - mi0:+.4f} nats "
          f"({'>= delta' if (mi_f - mi0) >= a.pedestal_delta else 'BELOW delta -> DECORATIVE'})")
    return 0


def _check(a):
    """C-swap + ablation. swap: K states, sample each state's OWN continuation, cross-score, InfoNCE
    bound + accuracy + permutation null + norm-matched noise. ablation: KL(ON||OFF) vs KL(NOISE||OFF)
    — the GRAFT-causality discriminator (decorative signature = the two are equal)."""
    W = dec.clm_load_weights(a.organ)
    cl = W.get("clmg")
    if cl is None:
        sys.exit("[graft] --check needs a ckpt carrying a CLMG trailer (run `graft fit` first)")
    organ = G.torch_organ(W)
    rng = np.random.default_rng(a.seed)
    pf = PF.pure_field_new()
    for _ in range(a.p1_steps):
        pf = PF.pure_field_step(pf, 0.0) or pf
    pf, states = _snapshots(pf, a.k, a.state_gap)
    emb_rms = float(np.sqrt(np.mean(np.asarray(W["embed"], np.float64) ** 2)))
    codes = [torch.tensor(G.gate_offset(cl, c, emb_rms)) for c in states]
    probes = [p.encode("ascii") for p in ("the ", "a ", "when ", "in ", "we ", "it ", "there ", "one ")]
    K = a.k

    # sample each state's OWN continuation, then cross-score every (state i, continuation j)
    f = np.zeros((K, K))
    uniqY = set()
    for pb in probes[:a.probes]:
        ids0 = [int(b) for b in pb]
        Y = []
        for i in range(K):
            Y.append(_sample_carrier(organ, ids0, codes[i], a.cont_len, rng=rng)[len(ids0):])
            uniqY.add(tuple(Y[-1]))
        for i in range(K):
            for j in range(K):
                seq = ids0 + Y[j]
                with torch.no_grad():
                    lg = organ(torch.tensor(seq, dtype=torch.long), emb_residual=codes[i])
                    lp = F.log_softmax(lg[len(ids0) - 1:-1].float(), -1)
                    f[i, j] += float(lp.gather(1, torch.tensor(Y[j]).unsqueeze(1)).sum())
    col = torch.log_softmax(torch.tensor(f), dim=0)
    mi_swap = float(col.diag().mean() + math.log(K)) / math.log(2)      # InfoNCE bound, bits
    acc = float((np.argmax(f, axis=0) == np.arange(K)).mean())
    perm = 0
    for _ in range(a.perms):
        pi = rng.permutation(K)
        c2 = torch.log_softmax(torch.tensor(f[pi]), dim=0)
        if float(c2.diag().mean() + math.log(K)) / math.log(2) >= mi_swap:
            perm += 1
    perm_p = (perm + 1) / (a.perms + 1)
    print(f"[graft] SWAP: MI_swap={mi_swap:.3f} bits (ceiling log2 K={math.log2(K):.3f}) · "
          f"acc={acc:.3f} (chance {1.0/K:.3f}) · perm_p={perm_p:.4f} · uniqueY={len(uniqY)}/{K*a.probes}")

    # ablation: KL(ON||OFF) vs KL(NOISE||OFF), averaged over EVERY state and several carriers.
    # A single (state, carrier) draw is far too noisy to read: on a gate_strength sweep it produced a
    # non-monotone KL(ON||OFF) (0.150 / 0.571 / 1.507 / 0.355 / 2.048) whose dip is variance, not
    # signal — and that dip alone would have licensed a "decorative exactly where it passes" story.
    ons, kls = [], []
    with torch.no_grad():
        for ci in range(min(a.abl_carriers, len(probes))):
            pb = [int(b) for b in probes[ci]]
            ids = pb + _sample_carrier(organ, pb, codes[ci % K], a.cont_len, rng=rng)[len(pb):]
            t = torch.tensor(ids, dtype=torch.long)
            off = F.log_softmax(organ(t).float(), -1)
            for c in codes:                                  # every state, not just codes[0]
                on = F.log_softmax(organ(t, emb_residual=c).float(), -1)
                ons.append(float((on.exp() * (on - off)).sum(-1).mean()) / math.log(2))
            for _ in range(a.noise_reps):
                nz = torch.tensor(rng.standard_normal(codes[0].shape).astype(np.float32))
                nz = nz / (nz.pow(2).mean().sqrt() + 1e-8) * codes[0].pow(2).mean().sqrt()
                ln = F.log_softmax(organ(t, emb_residual=nz).float(), -1)
                kls.append(float((ln.exp() * (ln - off)).sum(-1).mean()) / math.log(2))
    kl_on = float(np.mean(ons)); q95 = float(np.quantile(kls, 0.95))
    print(f"[graft] ABLATION: KL(ON||OFF)={kl_on:.4f} bits (mean of {len(ons)} state×carrier, "
          f"sd {np.std(ons):.4f}) · KL(NOISE||OFF) q95={q95:.4f} (n={len(kls)}) · "
          f"ratio={kl_on/max(q95,1e-9):.2f}x  "
          f"({'gate is distinguishable from noise' if kl_on >= 3*q95 else 'DECORATIVE signature (ON≈NOISE)'})")

    if a.fluency_corpus:
        _fluency(a, organ, codes, emb_rms, rng)
    return 0


def _fluency(a, organ, codes, emb_rms, rng):
    """FLUENCY PRICE — what the gate costs the frozen organ's language, on natural held-out text.

    MI alone cannot decide whether the capacity ceiling is a defect or a declared trade-off: a
    wider channel that wrecks the organ is not a win. DV = the organ's NLL per byte on natural
    text, gate ON vs OFF.

    The load-bearing arm is NOISE, not OFF. An offset of ANY kind at this RMS perturbs the
    embeddings, so `ON - OFF` alone cannot separate "this gate costs fluency" from "an offset of
    this size costs fluency". The norm-matched noise arm is that separation, and it is the same
    control the ablation block above already uses.

    Alignment is pinned by construction and cross-checkable: row i of the organ's logits predicts
    t[i+1] (the same convention _check's cross-scoring uses), so OFF NLL is the organ's ordinary
    held-out CE. On trained57 that independently measured 2.076 nats/byte — if OFF lands far from
    the organ's known CE, the readout is mis-aligned and the arms below are meaningless.
    """
    txt = open(os.path.expanduser(a.fluency_corpus), encoding="utf-8", errors="ignore").read()
    b = txt[int(len(txt) * 0.8):].encode("utf-8")[:a.fluency_bytes]      # held-out tail
    t = torch.tensor([int(x) for x in b], dtype=torch.long)
    tgt = t[1:]

    def nll(resid):
        with torch.no_grad():
            lg = organ(t, emb_residual=resid).float()
            lp = F.log_softmax(lg[:-1], -1)
            return float(-lp.gather(1, tgt.unsqueeze(1)).mean())

    off = nll(None)
    on = [nll(c) for c in codes]
    noise = []
    for _ in range(a.noise_reps):
        nz = torch.tensor(rng.standard_normal(codes[0].shape).astype(np.float32))
        nz = nz / (nz.pow(2).mean().sqrt() + 1e-8) * codes[0].pow(2).mean().sqrt()
        noise.append(nll(nz))
    # ---- FORM MARGIN — the arm that keeps the NLL reading honest (Sol, 2026-07-24) ----
    # Unconditional NLL punishes the C-dependent content shift that GRAFT is TRYING to produce, so
    # "MI up => NLL up" is nearly definitional and would manufacture a fluency trade-off out of the
    # measurement's own definition. The discriminator: does the organ still PREFER natural text over
    # a word-order scramble by the same margin under the gate? The scramble holds the word multiset
    # EXACTLY fixed, so content/unigrams are matched by construction and only order (form) differs.
    #   margin = NLL(scrambled) - NLL(natural)   ·   dMargin = margin_OFF - margin_ON
    # dMargin ~ 0 with dNLL > 0  =>  distribution SHIFT, not fluency loss.
    # THREE corruption families, not one. A panel resting on a single corruption is the same
    # single-draw defect the ablation arm just had to be repaired for: if dMargin is read off one
    # family, a family-specific quirk becomes "form is/isn't damaged". Each family breaks a
    # DIFFERENT axis of form, and every one preserves the multiset by construction (global word
    # order / local word order / within-word spelling), so content is matched and only form moves.
    words = txt[int(len(txt) * 0.8):].split()[:1200]

    def _shuffle(ws):                       # global word order — syntax at long range
        s = list(ws); rng.shuffle(s); return s

    def _adjswap(ws):                       # adjacent pairs only — local order, a much milder blow
        s = list(ws)
        for i in range(0, len(s) - 1, 2):
            s[i], s[i + 1] = s[i + 1], s[i]
        return s

    def _spell(ws):                         # within-word letters — orthography, word order intact
        out = []
        for w in ws:
            if len(w) > 3:
                mid = list(w[1:-1]); rng.shuffle(mid); w = w[0] + "".join(mid) + w[-1]
            out.append(w)
        return out

    FAMILIES = (("word-order", _shuffle), ("adj-swap", _adjswap), ("spelling", _spell))
    b_nat = " ".join(words).encode("utf-8")[:a.fluency_bytes]

    def nll_of(bs, resid):
        tt = torch.tensor([int(x) for x in bs], dtype=torch.long)
        with torch.no_grad():
            lp = F.log_softmax(organ(tt, emb_residual=resid).float()[:-1], -1)
            return float(-lp.gather(1, tt[1:].unsqueeze(1)).mean())

    nat_off = nll_of(b_nat, None)
    nat_on = [nll_of(b_nat, c) for c in codes]
    fam = {}
    for fname, fn in FAMILIES:
        b_c = " ".join(fn(words)).encode("utf-8")[:a.fluency_bytes]
        off_m = nll_of(b_c, None) - nat_off
        on_m = float(np.mean([nll_of(b_c, c) - n for c, n in zip(codes, nat_on)]))
        fam[fname] = (off_m, on_m)
    m_off = float(np.mean([v[0] for v in fam.values()]))
    m_on = float(np.mean([v[1] for v in fam.values()]))

    d_on = float(np.mean(on)) - off
    d_nz = float(np.mean(noise)) - off
    off_rms = float(codes[0].pow(2).mean().sqrt())
    print(f"[graft] FLUENCY ({len(b)}B natural held-out · offset RMS={off_rms:.4f} = "
          f"{off_rms/emb_rms:.3f}x embedding RMS)")
    print(f"[graft]   NLL gate-OFF   = {off:.4f} nats/byte   <- the frozen organ's own language")
    print(f"[graft]   NLL gate-ON    = {np.mean(on):.4f}  (dNLL {d_on:+.4f}, per-state sd {np.std(on):.4f})")
    print(f"[graft]   NLL noise-matched = {np.mean(noise):.4f}  (dNLL {d_nz:+.4f})  <- the control that matters")
    verdict = ("gate costs LESS fluency than a size-matched perturbation — the offset is structured"
               if d_on < d_nz else
               "gate costs AT LEAST as much as size-matched noise — no fluency credit for structure")
    print(f"[graft]   price ratio dNLL(ON)/dNLL(NOISE) = {d_on/max(d_nz,1e-9):+.3f}   ({verdict})")
    print(f"[graft]   FORM panel (3 corruption families · multiset preserved by construction):")
    for fname, (o, n) in fam.items():
        flag = "  ⚠️ family invalid (organ does not prefer natural)" if o <= 0.02 else ""
        print(f"[graft]     {fname:<11} margin OFF {o:+.4f}  ON {n:+.4f}  dMargin {o-n:+.4f}"
              f"  ({100*(o-n)/max(o,1e-9):+.1f}%){flag}")
    spread = max(v[0] - v[1] for v in fam.values()) - min(v[0] - v[1] for v in fam.values())
    print(f"[graft]   FORM mean: margin OFF = {m_off:+.4f}  ON = {m_on:+.4f}  dMargin = {m_off-m_on:+.4f}"
          f"  (across-family spread {spread:.4f})")
    if m_off <= 0.02:
        print("[graft]   ⛔ FORM PANEL INVALID: the organ does not prefer natural text to begin with "
              "— dMargin is unreadable, do not quote it.")
    elif abs(m_off - m_on) < 0.02 <= d_on:
        print("[graft]   ⚠️ dNLL is a DISTRIBUTION SHIFT, not fluency loss: the organ's preference "
              "for natural word order survives the gate intact. Do not call this a fluency price.")
    else:
        print(f"[graft]   → form preference is degraded by {100*(m_off-m_on)/max(m_off,1e-9):.1f}% "
              f"— the fluency reading survives the content-shift confound.")


def main():
    ap = argparse.ArgumentParser(description="GRAFT: no-corpus consciousness→language grounding")
    ap.add_argument("verb", choices=["fit", "check"])
    ap.add_argument("organ", help="the FROZEN language organ (.clm); for `check`, the grafted ckpt")
    ap.add_argument("--out", default="", help="output grafted .clm (fit)")
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--p1-steps", type=int, default=2000, dest="p1_steps")
    ap.add_argument("--n-states", type=int, default=8, dest="n_states")
    ap.add_argument("--state-gap", type=int, default=13, dest="state_gap")
    ap.add_argument("--ctx", type=int, default=128)
    ap.add_argument("--cont-len", type=int, default=32, dest="cont_len")
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--lam-common", type=float, default=1.0, dest="lam_common")
    ap.add_argument("--gate-rho", type=float, default=1.0, dest="gate_rho")
    ap.add_argument("--gate-strength", type=float, default=0.1, dest="gate_strength")
    ap.add_argument("--gate-rms-max", type=float, default=4.0, dest="gate_rms_max")
    ap.add_argument("--pedestal-delta", type=float, default=0.08, dest="pedestal_delta")
    ap.add_argument("--parity-tol", type=float, default=1e-3, dest="parity_tol")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--seed-bytes", default="\n", dest="seed_bytes")
    ap.add_argument("--log-every", type=int, default=50, dest="log_every")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--probes", type=int, default=4)
    ap.add_argument("--perms", type=int, default=999)
    ap.add_argument("--noise-reps", type=int, default=16, dest="noise_reps")
    ap.add_argument("--abl-carriers", type=int, default=4, dest="abl_carriers",
                    help="carriers averaged in the ablation arm (x every state) — 1 is too noisy to read")
    ap.add_argument("--fluency-corpus", default=None, dest="fluency_corpus",
                    help="natural text; measure the gate's fluency price (NLL ON vs OFF vs size-matched noise)")
    ap.add_argument("--fluency-bytes", type=int, default=4000, dest="fluency_bytes")
    a = ap.parse_args()
    if a.verb == "fit":
        if not a.out:
            sys.exit("[graft] fit needs --out <graft.clm>")
        if a.state_gap <= 0 or a.n_states < 2:
            sys.exit("[graft] --n-states >= 2 and --state-gap > 0")
        return _fit(a)
    return _check(a)


if __name__ == "__main__":
    sys.exit(main() or 0)
