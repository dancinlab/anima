# AKIDA AKD1000 — FIRST INFERENCE ON CHIP — 2026-05-22

BrainChip **AKD1000** (silicon rev `BC.00.000.002` = `NSoC_v2`, Akida 1.0 IP)
physically connected to a Raspberry Pi 5 (ubuntu aarch64 @ `192.168.50.155`,
pool roster `pi5-akida`). First neuromorphic inference executed **on the chip**
(`BackendType.Hardware`), $0 (LAN only, no cloud).

---

## 1. venv fix — what was wrong, how fixed

**Symptom**: `day1_install.sh`'s F-AKIDA aggregate log claimed `akida 2.19.1
importable` + `akida.devices() count=1`, yet `~/.venv/anima-akida` did **not
exist** when checked. `import akida` in system `python3` failed (PEP 668; akida
is venv-only).

**Root cause**: the prior `day1_install.sh` was run **under `sudo`** (the
`state/day1_install_2026_05_22/` log dir + `venv.log` are owned by `root`). The
installer resolves the venv path as `VENV_DIR="${HOME}/.venv/anima-akida"`.
Under sudo, `$HOME` resolves to **`/root`**, so the venv was actually created at
**`/root/.venv/anima-akida`** — confirmed present and functional:
`sudo /root/.venv/anima-akida/bin/python3 -c 'import akida' → 2.19.1`. The probe
in the install script therefore passed (it used that root-owned `$PYBIN`), but
the user-facing path `/home/ubuntu/.venv/anima-akida` was never created. A
secondary fallout: `pip install` itself succeeded (`pip_akida.log` →
`Successfully installed akida-2.19.1 numpy-2.4.6`), so the *SDK* was never the
problem — only the **venv location** (sudo-`$HOME` drift).

**Fix** (no sudo — runs as the `ubuntu` user so `$HOME=/home/ubuntu`):

```bash
python3 -m venv ~/.venv/anima-akida
~/.venv/anima-akida/bin/python3 -m pip install --upgrade pip
~/.venv/anima-akida/bin/python3 -m pip install 'akida>=2.0,<3.0'
```

**Acceptance** (Task 1):

```
$ ~/.venv/anima-akida/bin/python3 -c 'import akida; print(akida.__version__, akida.devices())'
2.19.1 [<akida.core.HardwareDevice object at 0x...>]
```

Venv now at `/home/ubuntu/.venv/anima-akida`, owned `ubuntu:ubuntu`, akida
2.19.1, 1 hardware device. No sudo is needed to drive the chip — `/dev/akida0`
is world-rw (`crw-rw-rw-`).

**Installer note for future runs**: `day1_install.sh` must NOT be run under
`sudo` (only its internal `apt-get` steps need root, and those already call
`sudo` themselves). Running the whole script under sudo redirects the venv to
`/root`. Recommended: run as `ubuntu`; the script's `sudo apt-get ...` lines
prompt as needed (or pipe `echo brainchip | sudo -S`).

---

## 2. First inference result

Minimal Akida 1.0 model built programmatically, mapped to the physical device,
weights set deterministically, forward pass run on the chip.
Script: `scripts/first_inference.py`. Raw JSON:
`state/first_inference_result_2026_05_22.json`.

| field | value |
|---|---|
| SDK | akida (MetaTF) **2.19.1**, aarch64 cp312 wheel |
| model | `InputData(1,1,16, input_bits=4)` → `FullyConnected(units=10, weights_bits=1)` (2 layers) |
| device | `BC.00.000.002` / `PCIe/NSoC_v2/0` — `AKD1000()` factory match = **True** |
| IP version | `IpVersion.v1` (Akida 1.0) |
| **mapped backend** | **`BackendType.Hardware`** (ran ON the AKD1000, not CPU) |
| input | random uint8 spikes, `input_sum = 117` |
| weights | all-ones (1-bit), shape `(1,1,16,10)` |
| **output** | `(1,1,1,10)` int32 = **`[117]×10`** — dot(all-ones, input) = sum = 117 ✓ arithmetically correct, non-trivial |
| wall latency | **0.6434 ms / inference** (mean over 100 runs) |
| on-chip clock | `Last inference clock: 748` cycles, `Last program clock: 542` |
| power telemetry | **unavailable** — `INA init failed: bus -2` (ENOENT). The on-board INA current sensor is not wired/exposed on this M.2 form factor; power measurement needs the full PCIe dev-kit board. `power_measurement_supported = False`. Not a chip fault. |

**Verdict**: the chip computed the correct dot-product (`117` per unit) — this
is genuine neuromorphic compute on the AKD1000, not a stub or CPU fallback
(`BackendType.Hardware` confirmed).

---

## 3. Silicon-rev capability matrix

The earlier note (`No AKD1000 (NSoC_v1) device detected … require Akida 1.0
silicon for edge learning`) is a **pack bug, NOT a hardware limitation**.

**Why**: `pack/runtime/metatf_runtime.py::assert_akd1000()` hard-checks
`version == "NSoC_v1"` (`BC.00.000.001`). But the SDK's own AKD1000 virtual-
device factory returns `NSoC_v2`:

```
akida.AKD1000().version == BC.00.000.002 == akida.NSoC_v2   # True
device.version          == BC.00.000.002                    # equal
```

`NSoC_v1` (`BC.00.000.001`) was the **pre-production engineering revision**;
`NSoC_v2` (`BC.00.000.002`) is the **production AKD1000** silicon. Both run
**Akida 1.0 IP** (`IpVersion.v1`), which supports on-chip Hebbian / 1-shot edge
learning. The assert simply checks the wrong enum.

**Edge-learning verified empirically on chip** (`scripts/edge_learn_probe.py`,
`state/edge_learn_probe_2026_05_22.json`): with binary inputs
(`InputData(input_bits=1)` → trainable `FullyConnected`),
`model.compile(AkidaUnsupervised(num_weights=2, learning_competition=0.1))`
succeeded, `model.fit(x)` ran on `BackendType.Hardware`, and
`device.learn_enabled` flipped **`False → True`** after the on-chip learning
step.

| capability | this silicon (NSoC_v2 / BC.00.000.002 / AKD1000) | evidence |
|---|---|---|
| **Inference (`backend=akida_hw`)** | **✓** | `[117]×10` correct output, `BackendType.Hardware`, 0.64 ms |
| **On-chip edge learning (Akida unsupervised / Hebbian)** | **✓** | `compile(AkidaUnsupervised)` ok, `fit()` on HW ok, `learn_enabled True` after fit |
| **Power telemetry (INA current sensor)** | **✗** (on this M.2 board) | `INA init failed: bus -2` — sensor not exposed on this form factor; needs dev-kit board |

**Net**: the original "edge-learning gated by non-1.0 silicon" worry is
**resolved** — both inference and on-chip learning work on this AKD1000.
The only genuinely-unavailable feature is on-board **power measurement**, and
that is a board/sensor-wiring matter, not a silicon-rev capability gate.

**Recommended pack fix** (follow-up, not required for first inference):
`assert_akd1000()` should accept the AKD1000 family by matching the SDK factory
(`dev.version == akida.AKD1000().version`) or `{NSoC_v1, NSoC_v2}` /
`ip_version == IpVersion.v1`, rather than `NSoC_v1` only.

---

## 4. Honest C3 (caveats, corrections, concerns)

1. **Synthetic toy model, not a trained classifier.** First inference uses a
   hand-built `InputData→FullyConnected` with all-ones weights. It proves the
   HW path + correct arithmetic, but is not a real workload. A trained model
   (e.g. via `akida_models` / a `.fbz` from MetaTF) is a separate follow-up;
   `akida_models` is not installed and no `.fbz` ships with the bare `akida`
   wheel.
2. **Power/energy unmeasured.** The headline "~1 mW / ~10000× efficiency" claim
   in `HW_CONNECTED_2026_05_22.md` is **not yet measured** — the INA sensor is
   absent on this M.2 board (`bus -2`). Latency is wall-clock (0.64 ms incl.
   PCIe round-trip + Python overhead) plus the on-chip clock count (748 cycles);
   neither is a Joules figure.
3. **Edge-learning verified at API level, not task level.** `fit()` engaged
   on-chip learning (`learn_enabled True`), but I did not validate that the
   learned weights produce a useful 1-shot classification — only that the
   silicon accepts and runs the unsupervised learning op on hardware.
4. **`learn_enabled` is per-program, not a silicon flag.** It reads `False` on a
   freshly-mapped inference model and `True` only after compiling a learning
   layer + fit. So it is not a standalone "can this chip learn?" probe; the
   positive learning result above is the actual evidence.
5. **Two venvs now exist on the Pi.** The stray root-owned
   `/root/.venv/anima-akida` (from the prior sudo run) still exists alongside
   the correct `/home/ubuntu/.venv/anima-akida`. Harmless but redundant; could
   be removed with `sudo rm -rf /root/.venv` in cleanup.
6. **`day1_install.sh` not re-run end-to-end.** I fixed the venv directly (venv
   + pip) rather than re-running the full installer, because the installer's
   sudo-`$HOME` drift is the very bug that produced the wrong path — re-running
   it the same way would reproduce the problem. The manual path is the
   documented Task-1 alternative.
7. **Single device, single boot.** All results are from one AKD1000 on one Pi 5
   boot session; not replicated across reboots or multiple cards.

---

## Artifacts

- `scripts/first_inference.py` — minimal model → HW map → forward pass + timing
- `scripts/edge_learn_probe.py` — on-chip AkidaUnsupervised fit() probe
- `state/first_inference_result_2026_05_22.json` — raw inference result
- `state/edge_learn_probe_2026_05_22.json` — raw edge-learning result
- Pi venv: `/home/ubuntu/.venv/anima-akida` (akida 2.19.1, 1 HW device)
