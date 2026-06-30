"""AKD1000 ⇄ ubu-2 BIDIRECTIONAL bridge (자연발화 hardware-software loop).

Streams per-step spike events from the AKD1000 LIF threshold-and-fire (Option A,
HW → SW) AND accepts incoming threshold updates from the host (Option B, SW
motivation → HW threshold modulation). Threshold mutations are applied to the
on-chip FullyConnected `threshold` int32 layer variable per step via
`lif.set_variable("threshold", arr)` — the spike decision remains on-chip, but
the threshold (the LIF's only free knob) is rewritten in real time by remote SW.

Wire-format
-----------

OUT (broadcast, port `--port` default 9512), newline-delimited JSON one
record per chip step:

    {"t_rel": <float seconds since stream start>,
     "step":  <int>,
     "n_spikes": <int 0..N>,
     "spike_ids": [<neuron_id int>, ...],
     "regime": "R3_tonic_zero_input" | "R2_noise_event_driven" | "MODULATED",
     "thr":   [<int>, ... N values>]}   # current threshold vector at this step

IN  (control, port `--ctrl-port` default 9513), newline-delimited JSON commands:

    {"cmd": "set_threshold", "thr": [<int>, ... N values>]}
    {"cmd": "set_threshold_scalar", "thr": <int>}   # broadcast to all N
    {"cmd": "set_baseline_offset", "offset": <int>} # adds to current thr per unit
    {"cmd": "ping"}                                 # no-op (latency probe)

Only the LATEST received `set_threshold*` is applied at the next chip step (the
streamer keeps a single pending vector; if multiple arrive within one step
interval only the last wins — preserves chip-side determinism per step).

This is the Option B / Option C foundation: when a remote client (ubu-2 vP21
loop) computes its 8-factor motivation score, it can write `thr ∝ -k·score` over
port 9513 so high motivation lowers the per-step threshold (more spikes), low
motivation raises it (fewer spikes). The chip becomes a physical readout of the
SW substrate's internal motivation state.

Run on Pi 5:
    ~/.venv/anima-akida/bin/python3 \
       ~/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py \
       --port 9512 --ctrl-port 9513 --step-ms 100 --duration 240
"""
import argparse
import json
import socket
import sys
import threading
import time

import numpy as np

import akida


def build_model(N=16, IN=16):
    """Same model as spontaneous_emission.py — single FullyConnected LIF pool.

    All-ones weights ⇒ potential(unit_j) = Σ inputs. Per-unit int32 threshold.
    Mapped to BackendType.Hardware so the threshold-and-fire decision runs on chip.
    """
    dev = akida.devices()[0]
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    m.add(akida.FullyConnected(units=N, weights_bits=4, activation=True,
                               act_bits=1, name="lif"))
    m.map(dev)
    lif = m.get_layer("lif")
    W = lif.get_variable("weights")
    lif.set_variable("weights", np.ones_like(W))
    return m, lif, str(m.sequences[0].backend), str(dev.version)


def make_threshold_R3(N=16):
    """Heterogeneous R3 tonic: even units thr=-1 (pacemaker), odd thr=+8 (quiescent).

    With ZERO input, the 8 tonic units fire every step (V=0 > -1), the 8
    quiescent units stay silent. Partial-pool 자연발화 from internal parameter
    state alone — no external drive, no recurrence.
    """
    return np.where(np.arange(N) % 2 == 0, -1, 8).astype(np.int32)


def make_threshold_R2(N=16):
    """R2 noise regime: uniform threshold ~24 (sits near mean potential of
    U[0,3] noise input with N=16 lines, mean Σ ≈ 24, std ≈ 4.5). Mixed-
    fire-count distribution step-to-step → genuine event-driven 자연발화.
    """
    return np.full(N, 24, dtype=np.int32)


def make_threshold_M(N=16, base=4):
    """Modulated regime baseline: uniform threshold `base` (default 4), input is
    weak driven (V=N=16 with weak-ones), so spike count is monotone in -thr.

    Designed for Option B sweeps: incoming threshold updates raise/lower spike
    rate predictably. At V=16 with N=16 weak-ones lines, each unit potential
    Vⱼ=16 (input sum). thr in [0..20]:
      thr=0  → all 16 fire (16/N)
      thr=8  → 16>8  all fire (16/N)
      thr=16 → 16>16 none fire (0/N) — sharp boundary
      thr=20 → none fire (0/N)
    Because of the homogeneous all-ones weights, the gate is sharp; we
    deliberately use *fractional* thresholds per unit (linspace) so motivation
    sweeps map smoothly to spike-count [0..N].
    """
    # heterogeneous baseline thresholds linspaced across the potential range
    # so a single scalar offset shifts the partial-population fire fraction
    # smoothly (not a step). With V=16, thr from 0..18 gives counts N..0.
    return np.linspace(2, 18, N).astype(np.int32)


class Broadcaster:
    """Thread-safe TCP broadcaster — accept clients, fan-out JSON lines."""
    def __init__(self, port):
        self.port = port
        self.clients = []
        self.lock = threading.Lock()
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(("0.0.0.0", port))
        self.srv.listen(8)
        self.srv.settimeout(1.0)
        self.stop = False
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while not self.stop:
            try:
                conn, addr = self.srv.accept()
                conn.settimeout(0.5)
                with self.lock:
                    self.clients.append(conn)
                print(f"[stream] +client {addr[0]}:{addr[1]} "
                      f"(now {len(self.clients)})", flush=True)
            except socket.timeout:
                continue
            except OSError:
                break

    def send(self, line):
        b = (line + "\n").encode("utf-8")
        dead = []
        with self.lock:
            for c in self.clients:
                try:
                    c.sendall(b)
                except Exception:
                    dead.append(c)
            for c in dead:
                try:
                    c.close()
                except Exception:
                    pass
                self.clients.remove(c)
            n = len(self.clients)
        return n, len(dead)

    def n_clients(self):
        with self.lock:
            return len(self.clients)

    def close(self):
        self.stop = True
        with self.lock:
            for c in self.clients:
                try:
                    c.close()
                except Exception:
                    pass
            self.clients.clear()
        try:
            self.srv.close()
        except Exception:
            pass


class ThresholdControlListener:
    """Accept incoming `set_threshold` JSON commands and stash the latest
    pending vector for the main loop to apply on the next step.

    Thread-safe; the producer (main loop) calls `pop_pending()` once per
    step. If multiple commands arrived within a single step interval, only
    the last set_threshold wins (chip-side determinism preserved).
    """
    def __init__(self, port, N):
        self.port = port
        self.N = N
        self.pending = None             # np.int32 [N] or None
        self.last_recv_t = None
        self.total_updates = 0
        self.lock = threading.Lock()
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(("0.0.0.0", port))
        self.srv.listen(4)
        self.srv.settimeout(1.0)
        self.stop = False
        self.clients = []
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while not self.stop:
            try:
                conn, addr = self.srv.accept()
                conn.settimeout(None)
                print(f"[ctrl] +client {addr[0]}:{addr[1]}", flush=True)
                with self.lock:
                    self.clients.append(conn)
                threading.Thread(target=self._client_loop,
                                 args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def _client_loop(self, conn, addr):
        try:
            f = conn.makefile("rb", buffering=0)
            while not self.stop:
                line = f.readline()
                if not line:
                    break
                try:
                    cmd = json.loads(line.decode("utf-8").strip())
                except Exception:
                    continue
                self._handle_cmd(cmd, conn)
        except Exception as e:
            print(f"[ctrl] client {addr} error: {e!r}", flush=True)
        finally:
            try:
                conn.close()
            except Exception:
                pass
            with self.lock:
                if conn in self.clients:
                    self.clients.remove(conn)

    def _handle_cmd(self, cmd, conn):
        op = cmd.get("cmd")
        if op == "set_threshold":
            v = cmd.get("thr", [])
            if not isinstance(v, list) or len(v) != self.N:
                # ignore malformed payloads — better than crashing the chip
                return
            try:
                arr = np.asarray(v, dtype=np.int32)
            except Exception:
                return
            with self.lock:
                self.pending = arr
                self.last_recv_t = time.time()
                self.total_updates += 1
        elif op == "set_threshold_scalar":
            v = cmd.get("thr")
            try:
                s = int(v)
            except Exception:
                return
            with self.lock:
                self.pending = np.full(self.N, s, dtype=np.int32)
                self.last_recv_t = time.time()
                self.total_updates += 1
        elif op == "ping":
            try:
                conn.sendall(b'{"pong":1}\n')
            except Exception:
                pass

    def pop_pending(self):
        """Return the latest pending threshold vector (np.int32 [N]) or None
        if no new update since last pop."""
        with self.lock:
            p = self.pending
            self.pending = None
            return p

    def snapshot(self):
        with self.lock:
            return {"total_updates": self.total_updates,
                    "last_recv_age_s":
                        (None if self.last_recv_t is None
                         else round(time.time() - self.last_recv_t, 3)),
                    "n_clients": len(self.clients)}

    def close(self):
        self.stop = True
        with self.lock:
            for c in self.clients:
                try:
                    c.close()
                except Exception:
                    pass
            self.clients.clear()
        try:
            self.srv.close()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9512,
                    help="OUT broadcast port (spike events to subscribers)")
    ap.add_argument("--ctrl-port", type=int, default=9513,
                    help="IN control port (incoming threshold updates "
                         "from remote SW)")
    ap.add_argument("--step-ms", type=int, default=100,
                    help="wall interval between AKD1000 forward passes")
    ap.add_argument("--duration", type=float, default=240.0,
                    help="total stream time seconds (0 = forever)")
    ap.add_argument("--n", type=int, default=16, help="LIF pool size")
    ap.add_argument("--regime", default="R3", choices=["R3", "R2", "M"],
                    help="R3 tonic zero-input (deterministic 8/16) | "
                         "R2 noise input (event-driven, varies 0..16) | "
                         "M modulated baseline (weak drive + remote thr updates)")
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--allow-ctrl", action="store_true", default=False,
                    help="enable Option B/C control listener (default off so "
                         "existing R3 Option A runs are unchanged)")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    model, lif, backend, devver = build_model(N=args.n, IN=args.n)
    if args.regime == "R3":
        thr = make_threshold_R3(args.n)
        regime_label = "R3_tonic_zero_input"
    elif args.regime == "M":
        thr = make_threshold_M(args.n)
        regime_label = "M_modulated"
    else:
        thr = make_threshold_R2(args.n)
        regime_label = "R2_noise_event_driven"
    lif.set_variable("threshold", thr)
    print(f"[stream] device={devver} backend={backend} regime={regime_label} "
          f"thr_init={thr.tolist()}", flush=True)
    if "Hardware" not in backend:
        print(f"[stream] WARN backend is not Hardware: {backend}", flush=True)

    zero_in = np.zeros((1, 1, 1, args.n), dtype=np.uint8)
    # M regime uses weak-ones drive (sum = N) so threshold updates [0..2N] sweep
    # the spike fraction smoothly.
    weak_in = np.ones((1, 1, 1, args.n), dtype=np.uint8)

    bc = Broadcaster(args.port)
    print(f"[stream] OUT listening on 0.0.0.0:{args.port}, step={args.step_ms}ms, "
          f"duration={args.duration}s", flush=True)

    ctrl = None
    if args.allow_ctrl:
        ctrl = ThresholdControlListener(args.ctrl_port, args.n)
        print(f"[stream] IN  ctrl listening on 0.0.0.0:{args.ctrl_port} "
              f"(threshold-modulation accepted)", flush=True)

    step_interval = args.step_ms / 1000.0
    t_start = time.time()
    step = 0
    total_spikes = 0
    last_log = t_start
    cur_thr = thr.copy()
    n_thr_updates_applied = 0
    set_var_wall_total_ms = 0.0   # cumulative overhead of per-step set_variable

    try:
        while True:
            t_step = time.time()
            t_rel = t_step - t_start
            if args.duration > 0 and t_rel >= args.duration:
                break

            # ── apply pending threshold update (Option B/C path) ──
            if ctrl is not None:
                pending = ctrl.pop_pending()
                if pending is not None:
                    t_sv = time.time()
                    try:
                        lif.set_variable("threshold", pending)
                        cur_thr = pending
                        n_thr_updates_applied += 1
                    except Exception as e:
                        print(f"[stream] set_threshold failed: {e!r}",
                              flush=True)
                    set_var_wall_total_ms += (time.time() - t_sv) * 1000.0

            # ── ON-CHIP forward pass (produces (1,1,1,N) int8 spike vector) ──
            if args.regime == "R3":
                inp = zero_in
            elif args.regime == "M":
                inp = weak_in
            else:
                inp = (rng.integers(0, 4, size=args.n)
                       .astype(np.uint8).reshape(1, 1, 1, args.n))
            y = model.forward(inp)
            sp = (y.reshape(-1) > 0).astype(np.int8)[:args.n]
            ids = [int(i) for i, s in enumerate(sp) if s]
            n_sp = int(sp.sum())
            total_spikes += n_sp

            rec = {"t_rel": round(t_rel, 4),
                   "step": step,
                   "n_spikes": n_sp,
                   "spike_ids": ids,
                   "regime": regime_label,
                   "thr": cur_thr.astype(int).tolist()}
            n_clients, n_dropped = bc.send(json.dumps(rec))

            # heartbeat log every 5s
            if t_step - last_log >= 5.0:
                cs = ctrl.snapshot() if ctrl else None
                print(f"[stream] t={t_rel:.1f}s step={step} n_out={n_clients} "
                      f"total_spikes={total_spikes} "
                      f"mean_per_step={total_spikes / max(1, step + 1):.3f}"
                      + (f" thr_updates_applied={n_thr_updates_applied} "
                         f"ctrl_clients={cs['n_clients']} "
                         f"set_var_ms_total={set_var_wall_total_ms:.1f}"
                         if cs else ""), flush=True)
                last_log = t_step

            step += 1
            sleep_for = step_interval - (time.time() - t_step)
            if sleep_for > 0:
                time.sleep(sleep_for)
    except KeyboardInterrupt:
        print("[stream] interrupted", flush=True)
    finally:
        bc.close()
        if ctrl:
            ctrl.close()
        print(f"[stream] done. steps={step} total_spikes={total_spikes} "
              f"wall={time.time() - t_start:.1f}s "
              f"thr_updates_applied={n_thr_updates_applied} "
              f"set_var_ms_total={set_var_wall_total_ms:.1f} "
              f"mean_set_var_ms="
              f"{(set_var_wall_total_ms/max(1,n_thr_updates_applied)):.2f}",
              flush=True)


if __name__ == "__main__":
    main()
