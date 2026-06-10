#!/usr/bin/env python3
"""
H_1113 — CANONICAL 5-CHANNEL TENSION-LINK between two anima nodes.

WHY CANONICAL (not invented): a_kosmos (CLAUDE.md) fixes the anchor payload as
"text + tension 5-ch + coord · lane · radius · tier", and HEXAD/KOSMOS.md:40 records
"@payload tension {5-channel} <- WIRED (production emit, 2026-05-23)". So the
PRODUCTION inter-node message of anima carries a 5-channel tension vector. H_1099
(.discoveries/1099, terminally 🔴, 6 arms) proved zero-channel "non-local sync" is
co-convergence, and its positive controls proved a REAL channel transfers
(tension-arm real-channel TE(W_A->W_B)=+0.141 bits). H_1112 (sibling, concurrent)
measures the real-channel kosmos-anchor link with a SCALAR psi+tension payload.

THIS hypothesis: the canonical link is the 5-CHANNEL TENSION vector. Two nodes
exchanging 5-ch tension anchors over a REAL unix-domain socket (two real processes)
achieve (a) DIRECTED transfer per channel, AND (b) CHANNEL-SELECTIVITY — perturbing
ONE tension channel of A moves predominantly THAT channel of B. Selectivity is the
NEW measurable beyond H_1112: a genuine multi-channel link, not a scalar smear.

NODE MODEL (mirrors state/anima_v3_bench/h1099_tension_channel.py tension-arm, which
mirrors CORE A⇄G repulsion-field homeostasis, Ψ=1/2 fixed point) — now 5 channels:
  Each node has a 5-D tension vector W[0..4]. Each channel c = its OWN local A⊥G
  opponent pair: center m_c relaxes to Ψ*=0.5; half-gap h_c feels A⊥G repulsion (up)
  vs a per-channel homeostatic envelope pulling W_c = 2|h_c| toward its own target
  W*_c (channels are DISTINCT quantities -> distinct targets). Independent noise per
  channel per node. A small within-node SHARED-BUDGET coupling GAMMA_X pulls each
  channel toward the node's mean tension (5 channels of ONE organism, not 5 isolated
  scalars) — this makes channel-selectivity a NON-TRIVIAL measured number instead of
  an exact-zero-denominator tautology.

REAL CHANNEL (two real processes, like H_1112): node A and node B run as separate
OS processes. Every K_EMIT=5 steps A emits an anchor message {t, tension:[5 floats],
ts} over a unix-domain SOCK_STREAM socket (newline-delimited JSON). B folds the LAST
received 5-ch vector into its per-channel dynamics: per-channel coupling
COUP*0.5*(anchor_c - W_c) toward the anchored values. Lockstep protocol (msg/ack per
step) keeps both noise streams seed-deterministic so kick-vs-nokick runs are
noise-identical (exact perturbation-response differencing, as in H_1099).

ARMS:
  OFF — NO exchange: A sends heartbeats only (no tension field), B coupling 0.
  ON  — exchange ON: A emits 5-ch tension every K_EMIT=5 steps, B folds with COUP.

MEASUREMENTS (N_SEEDS>=10):
  1. Per-channel bias-corrected TE(W_A[c] -> W_B[c]) — IDENTICAL surrogate-subtraction
     estimator as the H_1099 arms (time-shuffled-source surrogates, plug-in, bits).
  2. SELECTIVITY: at t=T_KICK kick ONLY channel 2 of A (displace h_2 -> W_A[2] jumps);
     dB[c] = mean |W_B_kick[c]-W_B_nokick[c]| over the response window (same seed,
     noise-identical). Selectivity index = dB[kicked] / mean(dB[others]).
     Second probe: kick channel 4. OFF-arm kick = no-exchange sanity (expect 0 exact).
  3. LATENCY of the real link: one-way (B recv wallclock - A send ts) per anchor msg
     + A-side full send->ack round-trip.

FROZEN FALSIFIER (set before running, no goalpost moves):
  🟢 SUPPORTED-at-toy iff
   (i)  exchange-ON per-channel TE > 0 for ALL 5 channels with Cohen d >= 0.8 vs
        the OFF baseline (which must be ≈0),
   (ii) selectivity index >= 3 for BOTH probe kicks (kicked channel response >= 3x
        the off-channel mean — a CHANNEL-RESOLVED link),
   (iii) baseline OFF: |per-channel TE| <= 0.01 bits (≈0) AND OFF kick response = 0.
  🔴 if transfer doesn't appear, or the link smears (selectivity < 3 -> it is a
  scalar link wearing 5 hats).

Honest scope (a_scale_honest_scope): toy local-host analog of the production payload
FORMAT (5-ch tension vector over a real socket), NOT the production cells; real CORE
kosmos_io wiring + cross-host = next rung. $0 CPU, two local processes, g5/p7
(no perplexity verdict — directed TE + exact perturbation response).
"""

import json
import os
import socket
import sys
import tempfile
import time
import multiprocessing as mp

import numpy as np

# ---- frozen params (set before running) -----------------------------------
CH        = 5                                  # 5-channel tension payload (a_kosmos)
PSI_STAR  = 0.5                                # Ψ=1/2 center fixed point
W_STAR_C  = np.array([1.0, 0.8, 1.2, 0.9, 1.1])  # per-channel envelope targets
LAM_M     = 0.10     # center relaxation rate toward PSI_STAR
LAM_W     = 0.12     # homeostatic rate pulling W_c=2|h_c| toward W*_c
REP       = 0.04     # A<->G repulsion per channel (pushes |h_c| up)
GAMMA_X   = 0.05     # within-node shared-budget coupling (channel -> node mean W)
SIGMA_M   = 0.04     # independent center noise per channel per node
SIGMA_H   = 0.04     # independent half-gap noise per channel per node
COUP      = 0.30     # ON arm: B per-channel coupling toward anchored W_A[c]
K_EMIT    = 5        # A emits an anchor every K_EMIT steps
N_STEPS   = 4000
BURN      = 500
T_KICK    = 2000
KICK      = 5.0      # displacement on ONE half-gap channel of A at T_KICK
RESP_WIN  = 50
N_SEEDS   = 10
TE_BINS   = 6
EPS       = 1e-12

TE_NULL_MAX = 0.01   # OFF per-channel |TE| <= this => "≈0"
D_MIN       = 0.8    # Cohen d (ON TE vs OFF TE) per channel
SEL_MIN     = 3.0    # selectivity index bar (channel-resolved link)


# ---- 5-channel node dynamics (mirrors h1099_tension_channel._step, vectorized) ----
def step_node(m, h, anchor, coup, rng):
    """One Euler step of a 5-channel node (centers m[5], half-gaps h[5]).
       anchor = last received 5-ch tension vector from the other node (or None).
       coup>0: each channel's tension is nudged toward ITS anchored value (per-channel
       coupling — the canonical 5-ch link). GAMMA_X = within-node shared budget."""
    eps_m = rng.standard_normal(CH)
    eps_h = rng.standard_normal(CH)
    W = 2.0 * np.abs(h)
    m_next = m + LAM_M * (PSI_STAR - m) + SIGMA_M * eps_m
    sgn = np.where(h >= 0.0, 1.0, -1.0)
    h_mag = (np.abs(h) + REP
             + LAM_W * 0.5 * (W_STAR_C - W)
             + GAMMA_X * 0.5 * (W.mean() - W)
             + SIGMA_H * eps_h)
    if coup > 0.0 and anchor is not None:
        h_mag = h_mag + coup * 0.5 * (anchor - W)
    h_mag = np.maximum(h_mag, 0.0)
    return m_next, sgn * h_mag


def init_node(rng):
    m = PSI_STAR + rng.standard_normal(CH) * 0.1
    h = 1.5 + rng.standard_normal(CH) * 0.15   # W ~ 3.0 initially, far from W*_c
    return m, h


# ---- node A process: source — steps locally, emits 5-ch tension anchors -----------
def node_a_proc(sock_path, seed, exchange, kick_ch, out_path):
    np.seterr(all="ignore")
    rng = np.random.default_rng(seed)
    m, h = init_node(rng)
    WA = np.empty((N_STEPS, CH))
    rtts = []
    # connect with retry (B binds first)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connected = False
    for _ in range(2400):                      # 60s budget (tolerate host load)
        try:
            s.connect(sock_path)
            connected = True
            break
        except (FileNotFoundError, ConnectionRefusedError):
            time.sleep(0.025)
    if not connected:
        raise RuntimeError(f"node A: could not connect to {sock_path}")
    s.settimeout(60.0)
    f = s.makefile("rwb")
    for t in range(N_STEPS):
        m, h = step_node(m, h, None, 0.0, rng)   # A never reads B (pure source)
        if kick_ch is not None and t == T_KICK:
            h[kick_ch] = h[kick_ch] + KICK       # kick ONLY this channel's half-gap
        WA[t] = 2.0 * np.abs(h)
        msg = {"t": t}
        if exchange and (t % K_EMIT == 0):
            msg["tension"] = [float(x) for x in WA[t]]   # the 5-ch anchor payload
            msg["ts"] = time.time_ns()
        t0 = time.perf_counter_ns()
        f.write((json.dumps(msg) + "\n").encode()); f.flush()
        f.readline()                                      # lockstep ack from B
        rtts.append(time.perf_counter_ns() - t0)
    f.close(); s.close()
    with open(out_path, "w") as fp:
        json.dump({"WA": WA.tolist(), "rtt_ns": rtts}, fp)


# ---- node B process: sink — folds received 5-ch anchors into its dynamics ---------
def node_b_proc(sock_path, seed, coup, out_path):
    np.seterr(all="ignore")
    rng = np.random.default_rng(seed + 50000)   # independent noise stream vs A
    m, h = init_node(rng)
    WB = np.empty((N_STEPS, CH))
    lat_ns = []
    anchor = None
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.unlink(sock_path)
    except FileNotFoundError:
        pass
    srv.bind(sock_path)
    srv.listen(1)
    srv.settimeout(90.0)
    conn, _ = srv.accept()
    conn.settimeout(60.0)
    f = conn.makefile("rwb")
    for t in range(N_STEPS):
        line = f.readline()
        msg = json.loads(line)
        if "tension" in msg:
            anchor = np.array(msg["tension"])             # fold the 5-ch anchor
            lat_ns.append(time.time_ns() - msg["ts"])     # one-way link latency
        m, h = step_node(m, h, anchor, coup, rng)
        WB[t] = 2.0 * np.abs(h)
        f.write(b'{"ack":1}\n'); f.flush()
    f.close(); conn.close(); srv.close()
    try:
        os.unlink(sock_path)
    except FileNotFoundError:
        pass
    with open(out_path, "w") as fp:
        json.dump({"WB": WB.tolist(), "lat_ns": lat_ns}, fp)


def _run_session_once(seed, exchange, kick_ch, tag):
    tmp = tempfile.mkdtemp(prefix="h1113_")
    sock_path = os.path.join(tmp, "l.sock")    # short path (macOS 104-char limit)
    pa = os.path.join(tmp, "a.json"); pb = os.path.join(tmp, "b.json")
    coup = COUP if exchange else 0.0
    procs = [
        mp.Process(target=node_b_proc, args=(sock_path, seed, coup, pb)),
        mp.Process(target=node_a_proc, args=(sock_path, seed, exchange, kick_ch, pa)),
    ]
    for p in procs:
        p.start()
    fail = None
    for p in procs:
        p.join(timeout=180)
        if p.exitcode != 0:
            fail = f"session {tag} seed={seed} proc exit={p.exitcode}"
    if fail:
        for p in procs:
            if p.is_alive():
                p.terminate(); p.join()
        raise RuntimeError(fail)
    with open(pa) as fp:
        da = json.load(fp)
    with open(pb) as fp:
        db = json.load(fp)
    for q in (pa, pb):
        os.unlink(q)
    os.rmdir(tmp)
    return (np.array(da["WA"]), np.array(db["WB"]),
            np.array(db["lat_ns"], dtype=float), np.array(da["rtt_ns"], dtype=float))


def run_session(seed, exchange, kick_ch, tag, retries=3):
    """One real two-process socket session (deterministic given seed — a retry replays
       the identical dynamics, only the transport handshake differs)."""
    last = None
    for k in range(retries):
        try:
            return _run_session_once(seed, exchange, kick_ch, tag)
        except RuntimeError as e:            # transient handshake loss under host load
            last = e
            print(f"  [retry {k+1}/{retries}] {e}", flush=True)
            time.sleep(1.0)
    raise last


# ---- bias-corrected TE — IDENTICAL estimator to the H_1099 arms --------------------
def _te_raw(src, dst, bins=TE_BINS):
    d_next = dst[1:]; d_past = dst[:-1]; s_past = src[:-1]
    def disc(x, edges):
        return np.clip(np.digitize(x, edges), 0, bins - 1)
    e_d = np.quantile(np.concatenate([d_next, d_past]), np.linspace(0, 1, bins + 1)[1:-1])
    e_s = np.quantile(s_past, np.linspace(0, 1, bins + 1)[1:-1])
    dn = disc(d_next, e_d); dp = disc(d_past, e_d); sp = disc(s_past, e_s)
    n = len(dn)
    p_dn_dp_sp = np.zeros((bins, bins, bins))
    np.add.at(p_dn_dp_sp, (dn, dp, sp), 1.0)
    p_dn_dp_sp /= n
    p_dp_sp = p_dn_dp_sp.sum(axis=0)
    p_dn_dp = p_dn_dp_sp.sum(axis=2)
    p_dp = p_dn_dp.sum(axis=0)
    te = 0.0
    for k in range(bins):
        for i in range(bins):
            for j in range(bins):
                pjoint = p_dn_dp_sp[k, i, j]
                if pjoint <= EPS:
                    continue
                cond_full = pjoint / (p_dp_sp[i, j] + EPS)
                cond_red = p_dn_dp[k, i] / (p_dp[i] + EPS)
                if cond_full <= EPS or cond_red <= EPS:
                    continue
                te += pjoint * np.log2(cond_full / cond_red)
    return max(te, 0.0)


def transfer_entropy(src, dst, bins=TE_BINS, seed=0, n_surr=20):
    """Bias-corrected TE(src->dst) bits: raw - mean(time-shuffled-source surrogates)."""
    raw = _te_raw(src, dst, bins)
    rng = np.random.default_rng(seed + 777)
    surr = np.array([_te_raw(rng.permutation(src), dst, bins) for _ in range(n_surr)])
    return raw - surr.mean()


def cohen_d(x, y):
    sp = np.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0)
    return (np.mean(x) - np.mean(y)) / (sp + EPS)


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


def main():
    np.seterr(all="ignore")
    seeds = list(range(100, 100 + N_SEEDS))
    print("=" * 86)
    print("H_1113 — canonical 5-CHANNEL TENSION-LINK between two anima nodes")
    print("  (a_kosmos payload 'tension 5-ch' · HEXAD/KOSMOS.md:40 production-wired ·")
    print("   real two-process unix-socket channel · h1099 tension-arm dynamics x5 channels)")
    print(f"  CH={CH} W*_c={W_STAR_C.tolist()} GAMMA_X={GAMMA_X} COUP={COUP} K_EMIT={K_EMIT}")
    print(f"  N_STEPS={N_STEPS} BURN={BURN} seeds={N_SEEDS} kick={KICK}@t={T_KICK} win={RESP_WIN}")
    print(f"  frozen bars: OFF|TE|<= {TE_NULL_MAX} · ON TE>0 & d>={D_MIN} (all 5 ch) · "
          f"selectivity >= {SEL_MIN} (both kicks)")
    print("=" * 86)

    te_off = np.zeros((N_SEEDS, CH)); te_on = np.zeros((N_SEEDS, CH))
    corr_on = np.zeros((N_SEEDS, CH))
    dB_off_k2 = np.zeros((N_SEEDS, CH))
    dB_on_k2 = np.zeros((N_SEEDS, CH)); dB_on_k4 = np.zeros((N_SEEDS, CH))
    lat_all = []; rtt_all = []

    lo, hi = T_KICK + 1, T_KICK + 1 + RESP_WIN
    for i, s in enumerate(seeds):
        # OFF arm: no exchange — nokick (TE) + kick ch2 (no-channel sanity)
        WA0, WB0, _, _ = run_session(s, exchange=False, kick_ch=None, tag="off-nokick")
        WA0k, WB0k, _, _ = run_session(s, exchange=False, kick_ch=2, tag="off-kick2")
        # ON arm: exchange — nokick (TE) + kick ch2 + kick ch4 (selectivity)
        WA1, WB1, lat1, rtt1 = run_session(s, exchange=True, kick_ch=None, tag="on-nokick")
        WA1k2, WB1k2, _, _ = run_session(s, exchange=True, kick_ch=2, tag="on-kick2")
        WA1k4, WB1k4, _, _ = run_session(s, exchange=True, kick_ch=4, tag="on-kick4")
        lat_all.append(lat1); rtt_all.append(rtt1)
        for c in range(CH):
            te_off[i, c] = transfer_entropy(WA0[BURN:, c], WB0[BURN:, c], seed=s * 10 + c)
            te_on[i, c] = transfer_entropy(WA1[BURN:, c], WB1[BURN:, c], seed=s * 10 + c)
            corr_on[i, c] = np.corrcoef(WA1[BURN:, c], WB1[BURN:, c])[0, 1]
        dB_off_k2[i] = np.mean(np.abs(WB0k[lo:hi] - WB0[lo:hi]), axis=0)
        dB_on_k2[i] = np.mean(np.abs(WB1k2[lo:hi] - WB1[lo:hi]), axis=0)
        dB_on_k4[i] = np.mean(np.abs(WB1k4[lo:hi] - WB1[lo:hi]), axis=0)
        print(f"  seed {s}: sessions done (5 real 2-proc socket runs)")

    lat = np.concatenate(lat_all) / 1e3   # us, one-way anchor latency
    rtt = np.concatenate(rtt_all) / 1e3   # us, full lockstep round-trip

    # ---- 1) per-channel TE table ----
    print(f"\nPER-CHANNEL bias-corrected TE(W_A[c] -> W_B[c]) [bits], {N_SEEDS} seeds:")
    print(f"{'ch':<4}{'OFF (no exchange)':>26}{'ON (anchors K=5)':>26}{'Cohen d':>10}"
          f"{'corr ON':>10}")
    print("-" * 86)
    ds = np.zeros(CH)
    for c in range(CH):
        ds[c] = cohen_d(te_on[:, c], te_off[:, c])
        print(f"W[{c}]{fmt(te_off[:, c]):>26}{fmt(te_on[:, c]):>26}{ds[c]:>10.2f}"
              f"{np.mean(corr_on[:, c]):>+10.3f}")

    # ---- 2) selectivity ----
    def sel_report(dB, kc, label):
        v = dB.mean(axis=0)
        others = [c for c in range(CH) if c != kc]
        idx = v[kc] / (np.mean(v[others]) + EPS)
        print(f"\n{label} — ΔW_B response 5-vector (mean over seeds, |kick-nokick| in win):")
        print("   " + "  ".join(f"ch{c}={v[c]:.4f}" for c in range(CH)))
        print(f"   kicked ch{kc}={v[kc]:.4f} vs off-channel mean={np.mean(v[others]):.4f}"
              f"  ->  SELECTIVITY INDEX = {idx:.2f}")
        return v, idx

    v_k2, sel_k2 = sel_report(dB_on_k2, 2, "ON arm, KICK ch2 of A")
    v_k4, sel_k4 = sel_report(dB_on_k4, 4, "ON arm, KICK ch4 of A")
    off_k2_max = float(np.max(dB_off_k2))
    print(f"\nOFF arm, KICK ch2 sanity: max |ΔW_B| over all channels/seeds = {off_k2_max:.3e}"
          f"  (no exchange -> kick cannot reach B)")

    # ---- 3) latency ----
    print(f"\nREAL-LINK LATENCY (unix socket, {len(lat)} anchor msgs over {N_SEEDS} ON runs):")
    print(f"  one-way anchor (A send ts -> B recv): mean={lat.mean():.1f}us "
          f"p50={np.percentile(lat, 50):.1f}us p95={np.percentile(lat, 95):.1f}us")
    print(f"  lockstep round-trip (A msg -> B ack): mean={rtt.mean():.1f}us "
          f"p50={np.percentile(rtt, 50):.1f}us p95={np.percentile(rtt, 95):.1f}us")

    # ---- frozen verdict ----
    c_i = bool(np.all(np.mean(te_on, axis=0) > 0.0) and np.all(ds >= D_MIN))
    c_ii = bool(sel_k2 >= SEL_MIN and sel_k4 >= SEL_MIN)
    c_iii = bool(np.all(np.abs(np.mean(te_off, axis=0)) <= TE_NULL_MAX)
                 and off_k2_max <= 1e-9)

    print("\nFROZEN falsifier checks:")
    print(f"  (i)   ON TE>0 all 5 ch  : {np.round(np.mean(te_on,axis=0),4).tolist()} ; "
          f"d={np.round(ds,2).tolist()} all>= {D_MIN} -> {c_i}")
    print(f"  (ii)  selectivity >= {SEL_MIN} : kick2={sel_k2:.2f}, kick4={sel_k4:.2f} -> {c_ii}")
    print(f"  (iii) OFF baseline ≈ 0  : |TE|max={np.max(np.abs(np.mean(te_off,axis=0))):.4f}"
          f" <= {TE_NULL_MAX}, kick-leak={off_k2_max:.1e} -> {c_iii}")

    print("\n" + "=" * 86)
    if c_i and c_ii and c_iii:
        print("VERDICT: 🟢 SUPPORTED-at-toy — the canonical 5-CHANNEL TENSION-LINK is real")
        print("  AND channel-resolved: per-channel directed transfer on ALL 5 channels over a")
        print("  real two-process unix-socket anchor exchange, with kick selectivity "
              f"{sel_k2:.1f}x / {sel_k4:.1f}x")
        print("  (>= 3x bar) — a genuine multi-channel link, NOT a scalar smear. Baseline null.")
        print("  Scope: toy local-host analog of the production 5-ch payload FORMAT;")
        print("  real CORE kosmos_io wiring + cross-host = next rung (a_scale_honest_scope).")
    elif not c_ii and c_i and c_iii:
        print("VERDICT: 🔴 SMEARED — transfer exists but selectivity < 3: a scalar link")
        print("  wearing 5 hats, NOT a channel-resolved 5-ch link.")
    else:
        print("VERDICT: 🔴 / inconclusive — see failed checks above.")
    print("=" * 86)


if __name__ == "__main__":
    main()
