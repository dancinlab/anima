"""H_966 + H_974 — SUBSTRATE-axis SW-ARM PARTIALS (substrate=CPU-mirror; a_lane_akida_gpu_split).

THESE ARE NOT THE FALSIFIER. The frozen falsifiers for H_966 (SW-vs-CHIP behavior parity)
and H_974 (SW->chip transfer) BOTH require a live AKD1000 (BackendType.Hardware) CHIP arm,
which is NOT reachable from this Mac host (no akida pkg, Darwin; the chip lives on pi5-akida).
The H decisions are therefore ⚠ INCOMPLETE-BLOCKED + a sidecar handoff.

This script runs ONLY the SW arm (Lane G/P) that each falsifier needs, so the chip arm later
has a matched SW reference. It NEVER claims an on-chip result (a_lane_akida_gpu_split): the CHIP
distance / transfer-retained-fraction CANNOT be computed without the chip and are reported as
BLOCKED. We DO establish:
  * H_966 SW arm: the within-SW run-to-run behavior band (D3 control) + the SW action/return
    distribution that the chip will be compared against.
  * H_974 SW arm: the SW-trained world-model SOURCE return (D1 numerator) + the scrambled-mapping
    control's SW analogue, so retained-fraction = return_CHIP/return_SW awaits only return_CHIP.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, boot_ci, header, verdict_line

ODIM = 2
NACT = 4
T = 20
N_TRAIN = 400
N_EP = 200
THRUSTS = np.array([[np.cos(2 * np.pi * k / NACT), np.sin(2 * np.pi * k / NACT)] for k in range(NACT)])
VSTEP = 0.4


def step_env(pos, v, a, rng):
    v = v + 0.6 * THRUSTS[a]
    pos = pos + VSTEP * v + 0.02 * rng.standard_normal(2)
    return pos, v, -np.linalg.norm(pos)


def optimal(pos, v):
    best, ba = 1e9, 0
    for a in range(NACT):
        vn = v + 0.6 * THRUSTS[a]; pn = pos + VSTEP * vn
        if np.linalg.norm(pn) < best:
            best, ba = np.linalg.norm(pn), a
    return ba


def gen_demo(rng):
    pos = rng.standard_normal(2) * 2; v = rng.standard_normal(2) * 0.5
    obs, acts = [pos.copy()], []
    for _ in range(T - 1):
        a = optimal(pos, v); acts.append(a); pos, v, _ = step_env(pos, v, a, rng); obs.append(pos.copy())
    acts.append(optimal(pos, v))
    return np.array(obs), np.array(acts)


def run_sw(sim, Whead, rng, scramble=False):
    pos = rng.standard_normal(2) * 2; v = rng.standard_normal(2) * 0.5
    obs = [pos.copy()]; total = 0.0; actions = []
    W = Whead if not scramble else Whead[:, ::-1]   # scrambled-mapping control (D3/H_974)
    for t in range(T - 1):
        z = sim.embed(np.array(obs))[-1]
        a = int((_aug(z[None, :]) @ W).argmax())
        actions.append(a); pos, v, r = step_env(pos, v, a, rng); obs.append(pos.copy()); total += r
    return total / (T - 1), actions


def main():
    header("H_966+H_974", "SUBSTRATE-axis SW-ARM partials (CHIP arm BLOCKED on Mac)",
           substrate="CPU-mirror (numpy) — NOT on-chip")
    print("a_lane_akida_gpu_split: this is the SW (Lane G/P) reference ONLY; the AKD1000 CHIP")
    print("arm is UNREACHABLE here -> H_966/H_974 = INCOMPLETE-BLOCKED + handoff.\n")
    rng = np.random.default_rng(0)
    demos = [gen_demo(rng) for _ in range(N_TRAIN)]
    sim = LDSWorldModel(ODIM, delay=3).fit([o for o, a in demos])
    Z, Y = [], []
    for o, a in demos:
        z = sim.embed(o)
        for t in range(2, T):
            Z.append(z[t]); Y.append(np.eye(NACT)[a[t]])
    Whead = _ridge(_aug(np.array(Z)), np.array(Y), 1e-2)

    # H_966 SW arm: within-SW run-to-run band (D3) + return distribution (chip will match this)
    sw_returns = []
    for i in range(N_EP):
        r, _ = run_sw(sim, Whead, np.random.default_rng(1000 + i)); sw_returns.append(r)
    sw_returns = np.array(sw_returns)
    lo, hi = boot_ci(sw_returns)
    # within-SW behavior band: split into two halves, compare
    half = N_EP // 2
    band = abs(sw_returns[:half].mean() - sw_returns[half:].mean())
    print(f"H_966 SW arm: return = {sw_returns.mean():.4f} ± {sw_returns.std():.4f}  CI=[{lo:.4f},{hi:.4f}]")
    print(f"H_966 SW within-substrate run-to-run band (D3 control) = {band:.4f}")
    print(f"H_966 CHIP arm: BLOCKED (needs live AKD1000) -> behavior-distance SW-vs-CHIP UNCOMPUTABLE\n")

    # H_974 SW arm: SW-trained SOURCE return (D1 numerator) + scrambled-mapping SW control
    src = sw_returns.mean()
    scr_returns = np.array([run_sw(sim, Whead, np.random.default_rng(2000 + i), scramble=True)[0]
                            for i in range(N_EP)])
    print(f"H_974 SW arm: SW-train SOURCE return = {src:.4f}")
    print(f"H_974 scrambled-mapping SW control return = {scr_returns.mean():.4f} "
          f"(bounds 'any mapping works'; real return clearly beats scramble: "
          f"{src > scr_returns.mean()})")
    print(f"H_974 CHIP arm: BLOCKED -> return_CHIP UNCOMPUTABLE -> retained-fraction "
          f"return_CHIP/return_SW awaits the chip deploy.\n")

    verdict_line("H_966", "INCOMPLETE-BLOCKED",
                 f"SW arm measured (return {sw_returns.mean():.3f}, within-SW band {band:.3f}); "
                 f"CHIP arm needs a live AKD1000 (BackendType.Hardware) unreachable on this Mac — "
                 f"behavior-distance SW-vs-CHIP UNCOMPUTABLE. substrate=CPU-mirror (a_lane_akida_gpu_split). HANDOFF filed.")
    verdict_line("H_974", "INCOMPLETE-BLOCKED",
                 f"SW SOURCE return {src:.3f} measured + scrambled-control {scr_returns.mean():.3f}; "
                 f"return_CHIP (deployed) needs the chip -> retained-fraction UNCOMPUTABLE here. "
                 f"substrate=CPU-mirror (a_lane_akida_gpu_split). HANDOFF filed.")


if __name__ == "__main__":
    main()
