#!/usr/bin/env bash
# run_qmirror_live.sh — invoke qmirror with venv python on PATH so the iit
# subcmd uses live pyphi (engine=pyphi) instead of mock fixture reproduce.
#
# Resolves the PEP 668 install-blocker by routing all qmirror python3 calls
# through ~/core/qmirror/.venv/bin/python3 (where pyphi b78d0e3 is installed).
#
# Usage:
#   ./run_qmirror_live.sh iit --n-qubits=4 --json
#   ./run_qmirror_live.sh selftest
#   ./run_qmirror_live.sh qrng --bits 64
#
# Env knobs forwarded:
#   NEXUS_QMIRROR_LIVE=1            ANU live entropy (qrng)
#   NEXUS_QMIRROR_ANU_KEY=<key>     ANU API key
#   NEXUS_QMIRROR_IIT_LIVE=1        opt-in iit live (pyphi engine)
#   NEXUS_QMIRROR_MOCK=1            force mock (CI safety)

set -euo pipefail

QM="${QMIRROR_ROOT:-$HOME/core/qmirror}"
VENV_BIN="$QM/.venv/bin"

if [[ ! -x "$VENV_BIN/python3" ]]; then
    echo "ERROR: qmirror venv not found at $VENV_BIN" >&2
    echo "  bootstrap: python3 -m venv $QM/.venv && $QM/.venv/bin/pip install 'git+https://github.com/wmayner/pyphi.git@b78d0e3' 'pyphi[parallel]'" >&2
    exit 2
fi

export QMIRROR_ROOT="$QM"
export PATH="$VENV_BIN:$PATH"
export PYPHI_WELCOME_OFF=1
export HEXA_FORK_CAP="${HEXA_FORK_CAP:-64}"

exec hexa run "$QM/cli/qmirror.hexa" "$@"
