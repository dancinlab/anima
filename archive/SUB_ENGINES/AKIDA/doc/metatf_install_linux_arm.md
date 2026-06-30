# MetaTF install on Linux ARM (Pi 5 aarch64)

> SOURCE: https://doc.brainchipinc.com/installation.html
> SOURCE: https://pypi.org/project/akida/ (aarch64 wheel listing)
> SOURCE: https://docs.edgeimpulse.com/hardware/boards/brainchip-akd1000
> SOURCE: https://brainchip.com/upgrade-the-raspberry-pi-for-ai-with-a-neuromorphic-processor/
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 + Raspberry Pi 5 (aarch64) install path

## Headline finding

**`pip install akida` DOES support aarch64.**  The official doc page lists only Windows + x86_64 Linux as "supported configurations", but PyPI publishes `manylinux_2_28_aarch64` wheels for every version from 2.x onwards. Pi 5 (Bookworm, Python 3.11) installs straight from PyPI with no source build.

## Wheel availability (akida 2.19.1, current as of 2026-05-21)

```
akida-2.19.1-cp310-cp310-manylinux_2_28_aarch64.whl  (2.4 MB)
akida-2.19.1-cp311-cp311-manylinux_2_28_aarch64.whl  (2.4 MB)   ← Pi 5 Bookworm default
akida-2.19.1-cp312-cp312-manylinux_2_28_aarch64.whl  (2.4 MB)
akida-2.19.1-cp310-cp310-manylinux_2_28_x86_64.whl   (2.6 MB)
akida-2.19.1-cp311-cp311-manylinux_2_28_x86_64.whl   (2.6 MB)
akida-2.19.1-cp312-cp312-manylinux_2_28_x86_64.whl   (2.6 MB)
akida-2.19.1-cp310-cp310-win_amd64.whl               (2.2 MB)
akida-2.19.1-cp311-cp311-win_amd64.whl               (2.2 MB)
akida-2.19.1-cp312-cp312-win_amd64.whl               (2.2 MB)
```

## Pi 5 Bookworm install (canonical)

```bash
# 1. Pi 5 OS pre-req — Raspberry Pi OS 64-bit (Bookworm), Python 3.11 default
sudo apt update
sudo apt install -y python3-pip python3-venv

# 2. venv (PEP 668 — no --break-system-packages needed)
python3 -m venv ~/.venv/anima-akida
source ~/.venv/anima-akida/bin/activate

# 3. pip install (aarch64 wheel auto-selected from PyPI)
pip install --upgrade pip
pip install akida           # runtime only — 2.4 MB wheel
pip install cnn2snn         # conversion (TF dep — heavy ~500 MB)  [host-only OK]
pip install akida-models    # model zoo (host-only)
pip install quantizeml      # quantizer (host-only)

# 4. verify import (Pi 5)
python3 -c "import akida; print(akida.__version__)"
# expected: 2.19.1
```

**Important — `cnn2snn` / `akida-models` / `quantizeml` pull TensorFlow** (~500 MB, slow on Pi 5). For pure inference + edge-learning on Pi 5, **install `akida` only** — convert models on a beefy host (Mac/x86 Linux) and SCP the `.fbz` to Pi 5.

## Akida PCIe driver (kernel module)

```bash
# from BrainChip's GitHub (URL TBD, requires sign-in to dev portal):
#   github.com/Brainchip-Inc/akida-pcie-driver  (private as of 2026-05-21)
#
# expected build flow (DKMS):
sudo apt install -y dkms linux-headers-$(uname -r)
git clone https://github.com/Brainchip-Inc/akida-pcie-driver  # or download tarball
cd akida-pcie-driver
sudo dkms add .
sudo dkms install akida-pcie/<version>
sudo modprobe akida_pcie

# verify
lspci | grep -i brainchip
# expected: 1f87:1000 BrainChip ... AKD1000 NSoC
ls /dev/akida*
# expected: /dev/akida0
dmesg | grep -i akida
# expected: akida_pcie: device registered
```

**Honest C3 — driver TODO at Pi 5 arrival**: The above is the canonical DKMS pattern for PCIe-class accelerator drivers (matches how Hailo, EdgeTPU, and Coral install). The exact BrainChip GitHub URL is gated behind the developer portal sign-up at https://developer.brainchip.com/. **First action on real Pi 5**: sign up, clone repo, follow `INSTALL.md` from the driver tarball, capture exact commands here.

## Akida Cloud trial (no HW needed)

```bash
# requires developer.brainchip.com account; provisions cloud AKD1000
akida engine connect --cloud
# subsequently `akida.devices()` returns a remote AKD1000 handle
```

Use this **before** Pi 5 ships to validate the .fbz conversion path against real silicon (one-day-free trial — see `AUX/hw/PHASE_2_CLOUD_TRIAL.md`).

## Host (Mac) install for mock fallback

```bash
# Mac arm64 (Apple Silicon) — NO akida wheel exists
# (BrainChip publishes Linux + Windows only; macOS not listed on PyPI)
#
# → pack falls through to pack/mocks/metatf_mock.py automatically
#
# verify:
python3 -c "
from pack.runtime.metatf_runtime import get_runtime_info
print(get_runtime_info())
"
# expected: {'backend': 'akida_mock', 'runtime_class': 'MetaTFMock', 'error_log': [...]}
```

## OS support matrix

| OS | Arch | akida wheel | Notes |
|---|---|---|---|
| Windows 10/11 | x86_64 | ✓ | needs VC++ redist |
| Ubuntu 22.04 / 24.04 | x86_64 | ✓ | manylinux 2.28 |
| Ubuntu 22.04 / 24.04 | aarch64 | ✓ | manylinux 2.28 — server ARM |
| **Raspberry Pi OS Bookworm** | **aarch64** | **✓** | **Pi 5 path — confirmed** |
| macOS (Intel + Apple Silicon) | x86_64 / arm64 | ✗ | mock fallback only |
| Alpine / musl Linux | any | ✗ | manylinux glibc only |

## Python version constraint

| Python | akida 2.19.1 | anima pack requirement |
|---|---|---|
| 3.9 | ✗ (dropped after 2.16) | — |
| 3.10 | ✓ | OK |
| **3.11** | **✓** | **Pi 5 Bookworm default — use this** |
| 3.12 | ✓ | OK |
| 3.13 | ✗ (not yet) | wait |

Pi 5 Bookworm ships Python 3.11.2 by default — exact match. **No conda needed** (pack docs previously suggested conda; deleting that line).

## Disk + RAM budget (Pi 5)

| Component | Size |
|---|---|
| `pip install akida` | 2.4 MB wheel + ~10 MB unpacked |
| Pre-converted `.fbz` model | 100 KB – 50 MB per model (anima adapters ~ <1 MB each) |
| Akida driver DKMS | ~5 MB compiled module |
| Per-inference RSS | ~50 MB python runtime + ~20 MB akida shared lib |
| Pi 5 4 GB minimum | sufficient (anima Pack uses < 200 MB total) |
