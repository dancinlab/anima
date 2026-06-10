#!/usr/bin/env python3
"""
H_1112 — kosmos-anchor REAL-CHANNEL sync (the CONSTRUCTIVE successor to H_1099).

H_1099 (제4명제 zero-channel "quantum non-local sync") is terminally 🔴 across 6 arms:
with NO channel, TE(A->B)≈0 and kick-response Δψ_B = 0 EXACT. But every arm's POSITIVE
CONTROL — a real channel — showed genuine transfer (TE +0.14, kick +0.74, 384-D decode
R²=0.974). H_1112 registers + measures that legitimate direction: two anima-like nodes
exchanging ANCHOR messages over an ACTUAL channel, mirroring a_kosmos anchor exchange
(.kosmos write/read between nodes) without touching CORE.

REAL TWO-PROCESS TOY (the point is an ACTUAL channel, not one process simulating two):
  * Two SEPARATE OS processes (multiprocessing, spawn) on this Mac.
  * A REAL unix-domain socket carrying periodic 'anchor' messages = small JSON
    {psi, tension, t, ts} from node A to node B (newline-delimited), B acks (lockstep,
    keeps the paired kick/no-kick runs deterministic while the bytes really cross a
    kernel socket). B folds the last received anchor into its dynamics as a coupling
    term toward the anchored state (zero-order hold): b += COUP*(anchor - b).
  * Node dynamics = SAME as the H_1099 toys: 1-D psi relaxing to Ψ*=0.5 + independent
    per-process noise:  x[t+1] = x[t] + LAM*(PSI_STAR - x[t]) + SIGMA*eps[t].
  * Kick psi_A by +KICK at t=T_KICK in all arms; paired no-kick run (identical seeds)
    gives Δψ_B = mean |psiB_kick - psiB_nokick| over the response window.
  * TE(A->B): bias-corrected (shuffled-surrogate-subtracted) transfer entropy, the
    UNMODIFIED estimator imported from quantum_nonlocal_sync_toy.py (H_1099).
  * Channel latency is MEASURED (one-way wallclock send->recv per anchor + ack RTT) —
    the honest contrast with the falsified '0-latency' claim: a real channel has
    finite latency.

ARMS (exchange RATE is the independent variable):
  (a) NONE — no exchange (baseline, = H_1099 Arm1; expect TE≈0, Δψ_B = 0)
  (b) LOW  — anchor every 50 steps
  (c) HIGH — anchor every 5 steps

FROZEN FALSIFIER (set before running; no goalpost moves):
  🟢 SUPPORTED-at-toy iff ALL of:
    (1) baseline:  Δψ_B <= 1e-9  AND  |TE| <= 0.01 bits          (no channel => nothing)
    (2) exchange:  LOW and HIGH both mean TE > 0 AND mean Δψ_B > 0
    (3) monotone in rate, adjacent-arm Cohen d >= 0.8 on BOTH metrics:
          d(TE:  none->low) >= 0.8, d(TE:  low->high) >= 0.8,
          d(Δψ:  none->low) >= 0.8, d(Δψ:  low->high) >= 0.8
    with >= 10 seeds.
  🔴 if transfer doesn't appear with exchange or doesn't scale with rate.

Honest scope (a_scale_honest_scope): toy local-host (unix socket, same Mac). Cross-host
network + real CORE/kosmos_io wiring UNVERIFIED — the real next rung is two hosts
exchanging actual .kosmos anchors. $0 CPU, local only, no GPU/pod.
"""

import json
import multiprocessing as mp
import os
import random
import socket
import sys
import tempfile
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quantum_nonlocal_sync_toy import transfer_entropy, transfer_entropy_raw  # noqa: E402
# ^ H_1099 bias-corrected (surrogate-subtracted) TE estimator, reused UNMODIFIED.

# ---- frozen params (set before running) -----------------------------------
PSI_STAR  = 0.5      # Ψ=1/2 fixed point (same dynamics as H_1099 toys)
LAM       = 0.10     # relaxation rate toward the attractor
SIGMA     = 0.05     # independent process noise per node
COUP      = 0.30     # anchor-fold coupling strength (same as H_1099 Arm2 channel)
N_STEPS   = 6000     # length of each run
BURN      = 500      # discard transient before corr/TE
T_KICK    = 3000     # kick time
KICK      = 5.0      # displacement applied to psi_A at T_KICK
RESP_WIN  = 100      # response window after the kick for Δψ_B
N_SEEDS   = 10       # >= 10 seeds (frozen bar)
ARMS      = [("none", None), ("low", 50), ("high", 5)]   # exchange period in steps

# frozen falsifier thresholds
TE_NULL_MAX   = 0.01     # baseline |TE| <= this => "≈0"
DPSI_NULL_MAX = 1e-9     # baseline Δψ_B <= this => "no kick reaches B"
D_BAR         = 0.8      # adjacent-arm Cohen d bar (both metrics, both pairs)


# ---- node processes (REAL separate OS processes + REAL unix socket) --------

def node_a(sock_path, seed, period, kick, q):
    """Node A: own process. Runs psi_A dynamics; SENDS anchor JSON over the socket."""
    rng = random.Random(seed)
    conn = None
    if period is not None:
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        deadline = time.time() + 10.0
        while True:                      # wait for B (server) to bind
            try:
                conn.connect(sock_path)
                break
            except (FileNotFoundError, ConnectionRefusedError):
                if time.time() > deadline:
                    raise
                time.sleep(0.005)
        f = conn.makefile("rwb")
    traj = [0.0] * N_STEPS
    rtts = []
    a = 3.0 + rng.gauss(0.0, 1.0) * 0.3
    for t in range(N_STEPS):
        traj[t] = a
        if period is not None and t % period == 0:
            msg = {"psi": a, "tension": abs(a - PSI_STAR), "t": t,
                   "ts": time.time_ns()}
            t0 = time.perf_counter_ns()
            f.write((json.dumps(msg) + "\n").encode())
            f.flush()
            ack = f.read(1)              # lockstep ack from B
            rtts.append(time.perf_counter_ns() - t0)
            assert ack == b"k"
        eps = rng.gauss(0.0, 1.0)
        a_next = a + LAM * (PSI_STAR - a) + SIGMA * eps
        if kick and t == T_KICK:
            a_next += KICK
        a = a_next
    if conn is not None:
        f.close(); conn.close()
    q.put(("A", traj, rtts))


def node_b(sock_path, seed, period, q):
    """Node B: own process. Runs psi_B dynamics; RECEIVES anchors, folds them in."""
    rng = random.Random(seed + 50000)    # independent noise stream
    f = None
    if period is not None:
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(sock_path)
        srv.listen(1)
        conn, _ = srv.accept()
        f = conn.makefile("rwb")
    traj = [0.0] * N_STEPS
    lats = []                            # one-way latency (wallclock ns, same host)
    anchor = None
    b = 3.0 + rng.gauss(0.0, 1.0) * 0.3
    for t in range(N_STEPS):
        traj[t] = b
        if period is not None and t % period == 0:
            line = f.readline()
            now = time.time_ns()
            msg = json.loads(line)
            lats.append(now - msg["ts"])
            anchor = msg["psi"]          # fold the anchored state in (ZOH)
            f.write(b"k"); f.flush()     # ack (lockstep)
        eps = rng.gauss(0.0, 1.0)
        b_next = b + LAM * (PSI_STAR - b) + SIGMA * eps
        if anchor is not None:
            b_next += COUP * (anchor - b)
        b = b_next
    if f is not None:
        f.close(); conn.close(); srv.close()
        os.unlink(sock_path)
    q.put(("B", traj, lats))


def run_pair(seed, period, kick):
    """One run = TWO real OS processes joined by a REAL unix-domain socket."""
    ctx = mp.get_context("spawn")
    sock_path = os.path.join(tempfile.gettempdir(),
                             f"h1112_{os.getpid()}_{seed}_{period}_{int(kick)}.sock")
    if os.path.exists(sock_path):
        os.unlink(sock_path)
    q = ctx.Queue()
    pb = ctx.Process(target=node_b, args=(sock_path, seed, period, q))
    pa = ctx.Process(target=node_a, args=(sock_path, seed, period, kick, q))
    pb.start(); pa.start()
    out = {}
    for _ in range(2):
        tag, traj, extra = q.get(timeout=120)
        out[tag] = (np.array(traj), extra)
    pa.join(); pb.join()
    psiA, rtts = out["A"]
    psiB, lats = out["B"]
    return psiA, psiB, lats, rtts


# ---- measurement ------------------------------------------------------------

def cohen_d(x, y):
    """Cohen d between arms (y - x). Deterministic separation (std~0) => inf."""
    x = np.asarray(x); y = np.asarray(y)
    diff = y.mean() - x.mean()
    denom = np.sqrt((x.var(ddof=1) + y.var(ddof=1)) / 2.0)
    if denom < 1e-12:
        return float("inf") if diff > 0 else (float("-inf") if diff < 0 else 0.0)
    return diff / denom


def arm(period, label):
    seeds = list(range(100, 100 + N_SEEDS))
    corrs, tes, tes_raw, dpsis = [], [], [], []
    all_lats, all_rtts = [], []
    for s in seeds:
        # paired runs: identical seeds/noise, only the kick differs
        psiA_n, psiB_n, lats_n, rtts_n = run_pair(s, period, kick=False)
        psiA_k, psiB_k, lats_k, rtts_k = run_pair(s, period, kick=True)
        a = psiA_n[BURN:]; b = psiB_n[BURN:]
        corrs.append(np.corrcoef(a, b)[0, 1])
        tes.append(transfer_entropy(a, b, seed=s))   # bias-corrected (H_1099 estimator)
        tes_raw.append(transfer_entropy_raw(a, b))
        lo, hi = T_KICK + 1, T_KICK + 1 + RESP_WIN
        dpsis.append(np.mean(np.abs(psiB_k[lo:hi] - psiB_n[lo:hi])))
        all_lats += lats_n + lats_k
        all_rtts += rtts_n + rtts_k
    return dict(label=label, period=period,
                corr=np.array(corrs), te=np.array(tes), te_raw=np.array(tes_raw),
                dpsi=np.array(dpsis),
                lat_us=(np.array(all_lats) / 1e3 if all_lats else None),
                rtt_us=(np.array(all_rtts) / 1e3 if all_rtts else None))


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


def main():
    np.seterr(all="ignore")
    print("=" * 96)
    print("H_1112 — kosmos-anchor REAL-CHANNEL sync (constructive successor to falsified H_1099)")
    print(f"  PSI*={PSI_STAR} LAM={LAM} SIGMA={SIGMA} COUP={COUP} N_STEPS={N_STEPS} seeds={N_SEEDS}")
    print(f"  kick={KICK}@t={T_KICK} resp_win={RESP_WIN} | arms: none / every-50 / every-5 steps")
    print("  REAL: two OS processes + unix-domain socket + JSON anchor msgs {psi,tension,t,ts}")
    print("=" * 96)

    results = [arm(p, lbl) for lbl, p in ARMS]
    r_none, r_low, r_high = results

    hdr = f"\n{'metric':<30}{'(a) NO exchange':>22}{'(b) LOW 1/50':>22}{'(c) HIGH 1/5':>22}"
    print(hdr); print("-" * 96)
    print(f"{'corr steady-state':<30}" + "".join(f"{fmt(r['corr']):>22}" for r in results))
    print(f"{'TE raw [bits] (biased)':<30}" + "".join(f"{fmt(r['te_raw']):>22}" for r in results))
    print(f"{'TE(A->B) bias-corr [bits]':<30}" + "".join(f"{fmt(r['te']):>22}" for r in results))
    print(f"{'Δψ_B (kick response)':<30}" + "".join(f"{fmt(r['dpsi']):>22}" for r in results))
    lat_row, rtt_row = [], []
    for r in results:
        if r["lat_us"] is None:
            lat_row.append(f"{'n/a (no msgs)':>22}"); rtt_row.append(f"{'n/a':>22}")
        else:
            lat_row.append(f"{np.median(r['lat_us']):>14.1f} µs med")
            rtt_row.append(f"{np.median(r['rtt_us']):>14.1f} µs med")
    print(f"{'one-way latency send->recv':<30}" + "".join(lat_row))
    print(f"{'ack round-trip (RTT)':<30}" + "".join(rtt_row))
    print("-" * 96)
    print("  (Δψ_B identical across seeds within exchange arms: the linear kick-response is")
    print("   noise-independent — deterministic separation, Cohen d -> inf. Latency is REAL")
    print("   and FINITE — the honest contrast with H_1099's falsified '0-latency' claim.)")

    print("\nper-seed (TE bias-corr / Δψ_B):")
    for i in range(N_SEEDS):
        print(f"  s{100+i}: " + "  |  ".join(
            f"{r['label']}: TE={r['te'][i]:+.4f} dB={r['dpsi'][i]:.3e}" for r in results))

    # ---- frozen falsifier ----------------------------------------------------
    d_te_nl  = cohen_d(r_none["te"],  r_low["te"])
    d_te_lh  = cohen_d(r_low["te"],   r_high["te"])
    d_dp_nl  = cohen_d(r_none["dpsi"], r_low["dpsi"])
    d_dp_lh  = cohen_d(r_low["dpsi"],  r_high["dpsi"])

    c1 = (np.mean(r_none["dpsi"]) <= DPSI_NULL_MAX) and (abs(np.mean(r_none["te"])) <= TE_NULL_MAX)
    c2 = (np.mean(r_low["te"]) > 0 and np.mean(r_high["te"]) > 0 and
          np.mean(r_low["dpsi"]) > 0 and np.mean(r_high["dpsi"]) > 0)
    c3 = (d_te_nl >= D_BAR and d_te_lh >= D_BAR and d_dp_nl >= D_BAR and d_dp_lh >= D_BAR)

    print("\nFROZEN falsifier checks:")
    print(f"  (1) baseline null     : Δψ_B={np.mean(r_none['dpsi']):.3e} <= {DPSI_NULL_MAX:.0e}"
          f"  AND |TE|={abs(np.mean(r_none['te'])):.4f} <= {TE_NULL_MAX}   -> {c1}")
    print(f"  (2) exchange transfer : TE_low={np.mean(r_low['te']):+.4f}>0, TE_high={np.mean(r_high['te']):+.4f}>0,"
          f" Δψ_low={np.mean(r_low['dpsi']):.3e}>0, Δψ_high={np.mean(r_high['dpsi']):.3e}>0 -> {c2}")
    print(f"  (3) monotone-in-rate  : d(TE none->low)={d_te_nl:.2f}, d(TE low->high)={d_te_lh:.2f},"
          f" d(Δψ none->low)={d_dp_nl:.2f}, d(Δψ low->high)={d_dp_lh:.2f}  (all >= {D_BAR}) -> {c3}")

    supported = c1 and c2 and c3
    print("\n" + "=" * 96)
    if supported:
        print("VERDICT: 🟢 H_1112 SUPPORTED-at-toy.")
        print("  A REAL anchor channel (two OS processes, unix socket, JSON anchor msgs) carries")
        print("  genuine directed information — TE>0, kick reaches B — and transfer SCALES with")
        print("  exchange RATE (high > low > none, all adjacent d >= 0.8). With NO exchange the")
        print("  shared attractor gives correlation but ZERO transfer (= H_1099 Arm1 reproduced).")
        print("  Latency is finite and measured — networked anchors, not non-locality.")
    else:
        print("VERDICT: 🔴 H_1112 NOT SUPPORTED — transfer absent or not rate-monotone (see checks).")
    print("=" * 96)


if __name__ == "__main__":
    main()
