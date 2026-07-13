#!/bin/bash
# install anima-python[train,gpu] on a fresh pod. Directory-RELATIVE (writes install.log + INSTALL_DONE
# next to itself) so it works from any /workspace/<dir>. Hardcoding /workspace/ma broke the NAT-ATOM fire
# (/workspace/na): the redirect went to a nonexistent path, install died silently with no log, and the
# driver polled 'installing' forever on a zombie. (convergence install-ma-sh-1)
export PATH=$PATH:$HOME/.local/bin
D="$(cd "$(dirname "$0")" && pwd)"
{ if ! python3 -m pip --version >/dev/null 2>&1; then
    python3 -m ensurepip --upgrade 2>/dev/null || { curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/gp.py && python3 /tmp/gp.py; }
  fi
  python3 -m pip install --break-system-packages "anima-python[train,gpu]" nvidia-cublas-cu12 nvidia-cuda-runtime-cu12
} > "$D/install.log" 2>&1
RC=$?
command -v anima-py >> "$D/install.log" 2>&1 && python3 -c "import numpy,torch" 2>>"$D/install.log" && RC=0 || RC=1
echo $RC > "$D/INSTALL_DONE"
