#!/bin/bash
export PATH=$PATH:$HOME/.local/bin
{ if ! python3 -m pip --version >/dev/null 2>&1; then
    python3 -m ensurepip --upgrade 2>/dev/null || { curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/gp.py && python3 /tmp/gp.py; }
  fi
  python3 -m pip install --break-system-packages "anima-python[train,gpu]" nvidia-cublas-cu12 nvidia-cuda-runtime-cu12
} > /workspace/ma/install.log 2>&1
RC=$?
command -v anima-py >> /workspace/ma/install.log 2>&1 && python3 -c "import numpy,torch" 2>>/workspace/ma/install.log && RC=0 || RC=1
echo $RC > /workspace/ma/INSTALL_DONE
