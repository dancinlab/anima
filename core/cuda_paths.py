"""Runtime CUDA-lib self-config so cupy finds libcublas/libnvrtc WITHOUT a manual
LD_LIBRARY_PATH — the runtime half of "fold the pod GPU bootstrap into main code"
(owner directive 2026-07-18). Companion to the install-time layer (cli/pod_bootstrap.sh
stage ⑤/⑥, which picks the CUDA-major-matched cupy) and to core/decode.py's
cuda_available() probe (the FINAL device gate — this module only raises the odds that
gate passes; it is NOT a gate and touches no verdict statistic).

WHY (measured 2026-07-18, rented runpod RTX4090): cupy-cudaNNx imports cleanly and reports
a device, then dies at the first forward `__matmul__` on `libcublas.so.<N>: cannot open
shared object file` when the system CUDA toolkit lib dir is not on the loader path. A
manual `export LD_LIBRARY_PATH=/usr/local/cuda-12.4/targets/x86_64-linux/lib` fixed it —
this module does that discovery in-process so no operator step is needed.

MECHANISM (glibc loader facts — the design hinges on these):
  F1. LD_LIBRARY_PATH is snapshotted at exec: mutating os.environ in a live process does
      NOT change THIS process's dlopen search (it only propagates to children). So the fix
      for the current process cannot be an env var — it must be an actual dlopen.
  F2. dlopen(SONAME) reuses an already-loaded link map before searching paths. If we
      ctypes.CDLL the .so by ABSOLUTE PATH with RTLD_GLOBAL first, cupy's later load of the
      same SONAME is satisfied with no path search. (This is exactly torch's
      _load_global_deps() pattern; it lives at the glibc layer, so it is cupy 12x/13x
      agnostic.)
  F3. A preloaded lib's OWN DT_NEEDED still takes the normal search, and system-toolkit
      .so files (unlike pip wheels) have no $ORIGIN RUNPATH — so deps must be preloaded in
      reverse-dependency order (nvrtc/nvJitLink/cublasLt BEFORE cublas).

Idempotent, linux-only, GPU-gated: on darwin / a GPU-less host / a host with no cupy dist,
ensure_cuda_libs() mutates NOTHING (no env, no dlopen, no import) and returns early — so
the CPU numpy path stays byte-identical (regression floor). On an ldconfig-correct host
(pool summer/aiden) the plain-SONAME pre-check succeeds and it also does nothing (delta 0).
"""
import ctypes
import glob
import os
import sys

_RESULT = None   # process-once cache: the diagnostic dict ensure_cuda_libs returns


def _gpu_present():
    """NVIDIA GPU + driver physically present, probed WITHOUT importing cupy/torch.
    Mirrors core/decode.py:_nvidia_gpu_present so the two never disagree. nvidia-smi is the
    LAST resort (a CPU image may carry the CLI without a device)."""
    try:
        for i in range(8):
            if os.path.exists("/dev/nvidia%d" % i):
                return True
        if os.path.exists("/proc/driver/nvidia/gpus"):
            return True
        from shutil import which
        return which("nvidia-smi") is not None
    except Exception:
        return False


def _installed_cupy_major():
    """The CUDA major the INSTALLED cupy wheel needs, read from the dist name
    `cupy-cuda(\\d+)x` — the exact inverse of pod_bootstrap ⑤ (which picks the wheel from
    libnvrtc.so.<major>). Returns int | None (None = no cupy-cudaNNx installed → nothing to
    configure). Never trust nvidia-smi's driver CUDA here (it reports the driver max, not
    the installed runtime — the 2026-07-18 trap)."""
    try:
        import importlib.metadata as _md
    except Exception:
        return None
    import re
    best = None
    try:
        for dist in _md.distributions():
            name = (dist.metadata["Name"] or "") if dist.metadata else ""
            m = re.fullmatch(r"cupy-cuda(\d+)x", name.strip().lower())
            if m:
                v = int(m.group(1))
                if best is None or v > best:
                    best = v
    except Exception:
        return None
    return best


def _candidate_dirs(major):
    """Toolkit lib dirs that actually contain libcublas.so.<major> or libnvrtc.so.<major>,
    in priority order. site-packages/nvidia/*/lib is included last (cupy-12x can be
    satisfied by the pip nvidia wheels if present)."""
    roots = []
    cp = os.environ.get("CUDA_PATH", "")
    if cp:
        roots.append(cp)
    roots.append("/usr/local/cuda")
    roots += sorted(glob.glob("/usr/local/cuda-*"), reverse=True)   # cuda-12.4 before cuda-11.x
    roots.append("/opt/cuda")
    libdirs = []
    for r in roots:
        for sub in ("lib64", "lib"):
            libdirs.append(os.path.join(r, sub))
        libdirs += glob.glob(os.path.join(r, "targets", "*-linux", "lib"))
    # pip nvidia wheels (site-packages/nvidia/<lib>/lib) — for a driver-only host w/o toolkit
    for sp in sys.path:
        libdirs += glob.glob(os.path.join(sp, "nvidia", "*", "lib"))
    seen, out = set(), []
    for d in libdirs:
        rd = os.path.realpath(d)
        if rd in seen or not os.path.isdir(rd):
            continue
        seen.add(rd)
        if (glob.glob(os.path.join(rd, "libcublas.so.%d" % major)) or
                glob.glob(os.path.join(rd, "libnvrtc.so.%d" % major))):
            out.append(rd)
    return out


# reverse-dependency order (F3): a lib's deps must already be loadable when it loads.
# Only the classes decode actually uses: cuBLAS (matmul), nvrtc/nvJitLink (elementwise+CUB
# JIT), curand (cupy.random — pod_bootstrap ⑥ gate). cusolver/cusparse are NOT used.
_PRELOAD_ORDER = (
    "libnvrtc-builtins.so.*", "libnvrtc.so.%d", "libnvJitLink.so.%d",
    "libcublasLt.so.%d", "libcublas.so.%d", "libcurand.so.*", "libcufft.so.*",
)


def ensure_cuda_libs():
    """Make the system CUDA runtime libs loadable for cupy in THIS process, without a manual
    LD_LIBRARY_PATH. Idempotent (process-once). Returns a diagnostic dict:
      {"configured": bool, "dirs": [...], "loaded": [...], "reason": str|None}
    Never raises (caller treats any failure as "leave the CPU fallback to decide")."""
    global _RESULT
    if _RESULT is not None:
        return _RESULT
    res = {"configured": False, "dirs": [], "loaded": [], "reason": None}
    try:
        # (2) platform / GPU early-exit — ZERO mutation on darwin & CPU-only (byte-identical).
        if not sys.platform.startswith("linux") or not _gpu_present():
            _RESULT = res
            return res
        # (3) which major does the installed cupy need? None → nothing to fix.
        maj = _installed_cupy_major()
        if maj is None:
            _RESULT = res
            return res
        # (4) loader pre-check: if the plain SONAME already resolves (ldconfig / an already
        #     correct LD_LIBRARY_PATH — pool hosts), do NOTHING. Keeps delta exactly 0 there.
        try:
            ctypes.CDLL("libcublas.so.%d" % maj, mode=ctypes.RTLD_GLOBAL)
            res["configured"] = True
            res["reason"] = "already resolvable (ldconfig/LD_LIBRARY_PATH)"
            _RESULT = res
            return res
        except OSError:
            pass
        # (5) discover + preload in reverse-dependency order (F2/F3).
        dirs = _candidate_dirs(maj)
        res["dirs"] = dirs
        if not dirs:
            other = _other_major_present(maj)
            res["reason"] = ("cupy-cuda%dx installed but no libcublas.so.%d on this host"
                             % (maj, maj)) + (" (found major %d instead — cupy/toolkit "
                             "MISMATCH)" % other if other else " (no CUDA toolkit found)")
            _RESULT = res
            return res
        for pat in _PRELOAD_ORDER:
            name = pat % maj if "%d" in pat else pat
            loaded_class = False
            for d in dirs:
                for so in sorted(glob.glob(os.path.join(d, name)), reverse=True):
                    try:
                        ctypes.CDLL(so, mode=ctypes.RTLD_GLOBAL)
                        res["loaded"].append(os.path.basename(so))
                        loaded_class = True
                        break   # first (highest) match per class is enough
                    except OSError:
                        continue
                if loaded_class:
                    break
        # (6) env for CHILD processes (spawned cli/*.py train workers re-exec, so F1 helps
        #     them): prepend the dir to LD_LIBRARY_PATH + set CUDA_PATH for cupy's JIT header
        #     search. No effect on THIS process's already-done dlopens; purely for children.
        # Pip CUDA wheels deliberately split libraries into sibling directories
        # (`nvidia/cublas/lib`, `nvidia/cuda_nvrtc/lib`, ...).  Preserve candidate
        # priority while making every discovered class available to child re-execs.
        for d in reversed(dirs):
            _prepend_env("LD_LIBRARY_PATH", d)
        if not os.environ.get("CUDA_PATH"):
            for d in dirs:
                root = d
                for _ in range(3):                  # …/cuda-12.4/targets/x-linux/lib → root
                    root = os.path.dirname(root)
                    if os.path.basename(root).startswith("cuda"):
                        os.environ["CUDA_PATH"] = root
                        break
                if os.environ.get("CUDA_PATH"):
                    break
        res["configured"] = bool(res["loaded"])
        if not res["configured"]:
            res["reason"] = "candidate dirs had no loadable CUDA libs: %s" % dirs
    except Exception as e:                            # self-config must never break import
        res["reason"] = "ensure_cuda_libs raised: %r" % e
    _RESULT = res
    return res


def _other_major_present(maj):
    """If a DIFFERENT CUDA major's libcublas is on the host, return it (mismatch diagnostic)."""
    for root in (["/usr/local/cuda"] + sorted(glob.glob("/usr/local/cuda-*"), reverse=True)):
        for sub in ("lib64", "lib"):
            for so in glob.glob(os.path.join(root, sub, "libcublas.so.*")) + \
                      glob.glob(os.path.join(root, "targets", "*-linux", "lib", "libcublas.so.*")):
                tail = so.rsplit(".so.", 1)[-1].split(".")[0]
                if tail.isdigit() and int(tail) != maj:
                    return int(tail)
    return None


def _prepend_env(key, path):
    cur = os.environ.get(key, "")
    parts = [p for p in cur.split(os.pathsep) if p]
    if os.path.realpath(path) not in [os.path.realpath(p) for p in parts if p]:
        os.environ[key] = os.pathsep.join([path] + parts) if parts else path
