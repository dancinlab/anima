# AUX/AKIDA/boot/ — Day 1-7 boot scripts

Sequential boot sequence for the Pi 5 + AKD1000 Dev Kit ($1495 도착예정).
See [parent README §5](../../anima-physics/AUX/README.md) for the canonical plan.

## scripts

| Day | Script | Purpose | Pi 5 expectation | Mac local behaviour |
|---|---|---|---|---|
| 1 | `day1_install.sh` | brew/apt + pip + akida SDK + INSTALL.sh chain | `import akida` PASS | mock fallback path |
| 2 | `day2_kuramoto.sh` | kuramoto adapter N=8 K=5.0 | r > 0.5 at K=2 cap | adapter selftest proxy |
| 3 | `day3_snn.sh` | SNN LIF deploy + byte-compare vs Mac sim | F-SNN-1..5 5/5 | deterministic sha256 of selftest |
| 4 | `day4_memristor.sh` | Hebbian 1-shot + power-cycle persistence | weights persist across reboot | weights persist across new process |
| 5 | `day5_e2e.sh` | E2E v2 first stage → Akida adapter | F-E2E-CROSS Akida 5/5 | hexa runtime deferred |
| 6 | `day6_demiurge.sh` | demiurge brain backend=akida_cloud | gate_state CLOSED | gate_state PENDING (honest ⏳) |
| 7 | `day7_summary.sh` | Day 1-6 aggregate → summary.md + power_log.json | dual-role 16/16 + HW 1c | DESIGN_SPEC power envelope only |

## usage

```bash
# full sequence:
cd /Users/ghost/core/anima/SUB_ENGINES/AKIDA
./BOOT.sh                # Day 1-7

# specific range:
./BOOT.sh 2 4            # Day 2-4

# single day (direct):
bash boot/day3_snn.sh
```

Each script emits a log directory under `state/dayN_<topic>_<YYYY_MM_DD>/`.

## honest C3

1. Day 1-7 scripts assume Pi 5 hardware + AKD1000 Dev Kit silicon for
   their final-tier verification. On Mac local they all run, but the
   `[VERIFY]` lines that depend on real spikes / on-chip Hebbian flips
   degrade gracefully to mock-deterministic proxies.
2. `day1_install.sh` calls `sudo apt-get` on Linux hosts (Pi 5 path);
   on Mac the apt branch is skipped — manual brew install handled outside.
3. `day6_demiurge.sh` `gate_state CLOSED` only when the real `akida` SDK
   import succeeds; mock-mode emits `gate_state PENDING` (⏳) per design.
