# kuramoto_neuromorphic

> anima-physics HW target #3 — Kuramoto N-oscillator coupling on spiking
> neuromorphic substrate (Intel Loihi 2 + BrainChip Akida).
> SW source `social/kuramoto_coupling.hexa` (§188 PASS 6/6).

## Status (2026-05-21 Mac local Phase 1a)

- ✅ **local numpy sim** — N=8, T=1000, dt=0.01, OMEGA_STD=1.5 → r(K=2.0)
  > 0.7 (locked), r(K=0.1) < 0.3 (desync). F-HW-KU-1..5 verified — see
  `state/sim.log`.
- ✅ **adapter syntax check** — `kuramoto_loihi2_adapter.py` +
  `kuramoto_akida_adapter.py` both `py_compile` PASS (no SDK imports
  attempted — try/except + skeleton pattern).
- ⏳ Phase 1b cloud submit — requires Intel NRC NxSDK access (Loihi 2)
  + BrainChip MetaTF cloud (Akida). Mac 에 실 HW 없음.

## Quick start

```bash
./build.sh sim       # numpy oscillator sim + F-HW-KU-1..5 falsifier
./build.sh adapters  # py_compile both adapters (syntax check only)
./build.sh all       # both
```

Phase 1b (cloud-side, separate dispatch):

```bash
# Intel Loihi 2 (NxSDK on Linux + NRC access):
pip install nxsdk
python3 src/kuramoto_loihi2_adapter.py --submit --n 8 --k 2.0 --steps 1000

# BrainChip Akida (MetaTF):
pip install akida
python3 src/kuramoto_akida_adapter.py --submit --n 8 --k 2.0 --steps 1000
```

## Files

- [DESIGN.md](DESIGN.md) — ASCII architecture + SW↔neuromorphic map + 5 falsifier spec + FPGA-vs-neuromorphic contrast
- `src/kuramoto_local_sim.py` — numpy N=8 Kuramoto sim + F-HW-KU-1..5
- `src/kuramoto_loihi2_adapter.py` — Intel NxSDK skeleton (cloud submit form)
- `src/kuramoto_akida_adapter.py` — BrainChip MetaTF skeleton (cloud submit form)
- `state/sim.log` + `state/adapter_syntax.log` — Mac local artifacts

## Cross-link

- [HW silicon path §2.3](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) (this target)
- [hexa source](../../social/kuramoto_coupling.hexa) — SW substrate (Φ_social ≥ 0.5 gate)
- [strange_loop_ice40](../strange_loop_ice40/DESIGN.md) — HW target #1 (FPGA pattern, synchronous clk)
- [anima-physics PLAN G6](../../PLAN.md) — HW Phase 1 (target #3 = first neuromorphic-substrate design)
