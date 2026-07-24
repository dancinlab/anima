# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/decode.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ decode.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

"""core/decode.py — UNIFIED PY DECODE ENGINE: byte-faithful 1:1 merge of the two
per-mouth decoder mirrors into ONE module.

  * CONV (CLM ConvMoE) mouth  = the verbatim port of core/clm_decode.hexa
                                (formerly core/clm_decode.py)
  * BYTE (ByteGPT transformer) = the verbatim port of core/decode.hexa
                                (formerly core/bytegpt_decode.py)

Per CLAUDE.md a_engine_native_learning: hexa + py are TWO co-equal production
engines kept at byte-parity. This module is the numpy mirror of the two decode
mouths; it exposes the UNION of both modules' public names so a caller can do
`import decode as clm` OR `import decode as bg` (or `import decode`) with ZERO
call-site churn (drop-in for clm_decode.py + bytegpt_decode.py).

Organization:
  (a) SHARED — imports + the transcendental/PRNG helpers that are BYTE-IDENTICAL
      across both source modules (dt_exp, _MASK, _mix32, _rng_next, _topk_sample).
  (b) CONV (CLM) — the full clm_decode.py public API, verbatim.
  (c) BYTE (ByteGPT) — the full bytegpt_decode.py public API, verbatim, PLUS a
      byte-exact KV-cache fast path that REPLACES the O(gen²) full re-forward
      decode loop (the O(gen²) reference is kept under a `_full` suffix).
  (d) MOUTH DISPATCH — header-sniff (CLM\\x01 magic → conv; 5×u32 → byte),
      mirroring generator.hexa gen_auto_backend.

DIVERGENT SAME-NAMED HELPERS — kept under DISTINCT names, never silently merged:
  * clm's `_gn_sqrt` (gn_lib, 40-iter from g0=x) ⊥ bg's `dt_sqrt` (flame_math,
    24-iter from g0=max(x,1)) — different bodies, both retained (distinct names).
  * clm's `_rd_u32` and bg's `_bg_rd_u32` — IDENTICAL bodies; `_bg_rd_u32` is an
    alias of `_rd_u32` (surface preserved, one definition).
The PRNG trio (_mix32/_rng_next/_topk_sample) + dt_exp were byte-identical across
the two source files (bg imported dt_exp FROM clm), so they are deduped to one
copy in the SHARED section with no behavior change.

KV-CACHE (the ByteGPT fast path, new here): the hexa KV-cache is byte-identical
to its full-forward reference (decode.hexa:919). numpy BLAS GEMM is
M-dependent at the ~1e-15 ULP level (a single-row projection differs from the
same row of an M=T batch), so the py KV logits are NOT bit-identical to the py
full-forward — but the DECODE TOKEN STREAM is identical (argmax/inverse-CDF are
robust to ~1e-13 logit drift), and the cache is fully RE-SYNCED (rebuilt at M=T)
whenever the window slides past `block`. Byte-exactness of the token stream is
gated by state/1815_cls_bytegpt/_decode_selftest.py.
"""

import sys
import math
import os
import struct
import numpy as np

# ════════════════════════════════════════════════════════════════════════
# Session weight cache (perf) — the .clm/.bin is IMMUTABLE for a run, yet every
# decode entry (clm_load_weights / bg_load) re-read + int4-dequantized +
# transposed the FULL 303M checkpoint from disk on EVERY call. In the
# consciousness daemon that is one full re-parse per emit tick (dominant share of
# the ~60-80s/tick wall). Memoize by (abspath, st_mtime_ns, st_size): a hit
# returns the byte-IDENTICAL weight dict (already device-resident if the GPU path
# uploaded it), so decode output is unchanged (max|Δ|=0 — no parity gate needed)
# and the parse is paid ONCE per (file, mtime) per process. Auto-invalidates if
# the file's mtime/size changes. W is read-only during decode (forwards read from
# it; scratch is separate), so returning the shared dict is safe.
_WLOAD_CACHE = {}


def _wload_key(path):
    """Cache key for a weight file: (abspath, mtime-ns, size). None if the path is
    unstattable (e.g. the UNLOADED generator-swap arm passes path="") so a
    missing/degenerate path is never cached."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    return (os.path.abspath(path), st.st_mtime_ns, st.st_size)


# ════════════════════════════════════════════════════════════════════════
# GPU device path (cupy, optional) — a_gpu_default_no_optin: DEFAULT-ON via a
# cuda_available() capability probe, NEVER an opt-in env flag. H_9119 lesson:
# an opt-in gate silently leaves every decode/eval on the scalar CPU path with
# the GPU idle — so there is no env var here at all. cupy is drop-in-compatible
# numpy (same elementwise/reduction/einsum/matmul API), so the SAME formulas
# below run unchanged on either backend; only the array module differs. Byte
# parity: elementwise ops match to the ULP; a GEMM/reduction run on a different
# accumulator (GPU BLAS/tree-reduce vs host pairwise-sum) can differ at the
# ~1e-13..1e-15 ULP level — the SAME class of non-bit-exact-but-decode-
# equivalent drift already documented above for the KV-cache path (module
# docstring): the decode TOKEN STREAM / held-out d_acc is what must match, not
# raw bytes. numpy-only hosts (no cupy installed, or no CUDA device) get an
# unconditional, unchanged numpy fallback — this module never hard-imports
# cupy at the top level failure path.
# Runtime CUDA-lib self-config BEFORE `import cupy` (H_9767 pod-bootstrap-into-main-code):
# make libcublas/libnvrtc loadable without a manual LD_LIBRARY_PATH (see core/cuda_paths.py).
# MUST precede the cupy import (glibc F2: an absolute-path RTLD_GLOBAL preload satisfies
# cupy's later SONAME load). __file__-relative import so it works however decode.py was
# loaded (flat sys.path OR importlib.spec_from_file_location, e.g. pod_bootstrap ⑥). No-op
# on darwin / GPU-less / cupy-less hosts → CPU path byte-identical.
_CUDA_LIB_CFG = {"configured": False, "loaded": [], "dirs": [], "reason": None}
try:
    _here = os.path.dirname(os.path.abspath(__file__))
    if _here not in sys.path:
        sys.path.insert(0, _here)
    from cuda_paths import ensure_cuda_libs as _ensure_cuda_libs
    _CUDA_LIB_CFG = _ensure_cuda_libs()
except Exception as _cfg_err:             # self-config must never break the import
    _CUDA_LIB_CFG = {"configured": False, "loaded": [], "dirs": [],
                     "reason": "cuda_paths unavailable: %r" % _cfg_err}

try:
    import cupy as _cupy
    _CUPY_IMPORT_ERR = None
except Exception as _cupy_err:            # pragma: no cover — numpy-only host
    _cupy = None
    _CUPY_IMPORT_ERR = _cupy_err

_CUDA_AVAILABLE = None       # tri-state probe cache (None = not yet probed)
_CUDA_PROBE_ERR = None       # why the device path was refused (import · no device · kernel)
_GPU_LOG_DONE = False        # print the [GPU-FIRED]/[GPU-FALLBACK] QA line once
# cupy OOM type for graceful device->CPU fallback at weight-residency (a shared
# GPU that is momentarily full must NOT hard-crash the eval — fall back byte-exact).
_CUPY_OOM = _cupy.cuda.memory.OutOfMemoryError if _cupy is not None else ()


def _nvidia_gpu_present():
    """True iff an NVIDIA GPU + driver is physically present, probed WITHOUT importing
    cupy or torch (both optional). A CUDA device exposes /dev/nvidia0 once the kernel
    driver is loaded; nvidia-smi on PATH is the fallback signal. This exists ONLY to tell
    apart the two device-path=CPU cases that _log_gpu_status_once must NOT conflate: a
    genuinely GPU-less host (CPU is expected, no warning) vs a GPU host whose cupy path is
    dead (a paid GPU silently running eval on CPU — the defect this distinguishes)."""
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


def cuda_available():
    """True iff cupy is importable, a CUDA device is present, AND cupy can actually
    COMPILE AND RUN a kernel on it. This is the SOLE gate for the device path anywhere
    in this module — no env flag (a_gpu_default_no_optin).

    The kernel clause is load-bearing, not paranoia. A cupy whose JIT toolchain
    mismatches the host (e.g. cupy-cuda12x on a pod whose nvrtc rejects CUB's reduction
    template) imports cleanly and reports a device, then raises NVRTC_ERROR_COMPILATION
    on the first `.any()` — which lives deep inside `dt_exp`, i.e. inside the decode of
    item 1 of a 174-item eval. Probing only the device count promotes that host to the
    device path and the whole run dies, instead of taking the numpy fallback this module
    already guarantees for GPU-less hosts. So probe what decode actually uses: an
    elementwise op, a CUB reduction, AND a cuBLAS matmul (decode's forward is
    matmul-dominated and cuBLAS is a separate runtime lib — a missing libcublas passes
    the first two and dies at the first forward otherwise), once."""
    global _CUDA_AVAILABLE, _CUDA_PROBE_ERR
    if _CUDA_AVAILABLE is None:
        ok = False
        if _cupy is None:
            _CUDA_PROBE_ERR = _CUPY_IMPORT_ERR
        else:
            try:
                if _cupy.cuda.runtime.getDeviceCount() > 0:
                    probe = _cupy.arange(4, dtype=_cupy.float64)
                    ok = bool((probe * 2.0 > 1.0).any())   # elementwise -> CUB reduce
                    # matmul -> cuBLAS: decode's forward is DOMINATED by matmuls, and cuBLAS
                    # (libcublas.so.<major>) is a SEPARATE runtime lib from the JIT/CUB path
                    # above — a cupy whose cuBLAS is absent/mismatched passes the elementwise
                    # probe, reports GPU, then dies at the FIRST forward `__matmul__` on
                    # `libcublas.so.N: cannot open shared object file` (measured 2026-07-18 on a
                    # rented pod: cupy-cuda13x over a CUDA-12.4 toolkit). Probe the lib class
                    # decode ACTUALLY uses so a missing cuBLAS takes the numpy fallback this
                    # module guarantees, instead of crashing mid-decode on a paid GPU.
                    _mm = _cupy.ones((2, 2), dtype=_cupy.float64) @ _cupy.ones((2, 2), dtype=_cupy.float64)
                    ok = ok and bool(_mm.sum() == 8.0)
                else:
                    _CUDA_PROBE_ERR = RuntimeError("no CUDA device")
            except Exception as e:                # broken JIT/toolchain, driver fault …
                ok = False
                _CUDA_PROBE_ERR = e
        _CUDA_AVAILABLE = ok
    return _CUDA_AVAILABLE


def gpu_status():
    """Diagnostic dict for CLI/QA surfacing (cli/evaluate.py prints this so a
    pool run can confirm the fast path was actually reached, not just present —
    core/CLAUDE.md gotcha: 'decode GPU path 확인 먼저')."""
    if not cuda_available():
        reason = str(_CUDA_PROBE_ERR) if _CUDA_PROBE_ERR is not None else "no CUDA device"
        # gpu_present distinguishes "no GPU at all → CPU is expected" from "GPU present but
        # the cupy device path is dead → a paid GPU is silently running on CPU" (the defect).
        return {"cuda": False, "device_name": None, "cupy": None, "reason": reason,
                "gpu_present": _nvidia_gpu_present(), "lib_config": _CUDA_LIB_CFG}
    try:
        name = _cupy.cuda.runtime.getDeviceProperties(0)["name"]
        if isinstance(name, bytes):
            name = name.decode("utf-8", "replace")
    except Exception:
        name = "unknown"
    # cupy version is part of the diagnosis, not decoration: cupy 14.x is BROKEN on sm_120
    # (its bundled cuda_fp8.hpp does not parse under nvrtc, so every JIT kernel fails to
    # compile). pyproject pins the [gpu] extra to <14, but a pool host carrying an older
    # anima wheel can still be sitting on a cupy the pin never reached — printing the
    # version is how that shows up in the run log instead of as a mid-eval crash.
    try:
        cupy_ver = _cupy.__version__
    except Exception:
        cupy_ver = "unknown"
    return {"cuda": True, "device_name": name, "cupy": cupy_ver, "reason": None,
            "gpu_present": True, "lib_config": _CUDA_LIB_CFG}


def _log_gpu_status_once():
    global _GPU_LOG_DONE
    if _GPU_LOG_DONE:
        return
    _GPU_LOG_DONE = True
    st = gpu_status()
    if st["cuda"]:
        print(f"[GPU-FIRED] decode device path=CUDA ({st['device_name']} · cupy "
              f"{st.get('cupy', '?')})", file=sys.stderr)
    elif st.get("gpu_present"):
        # A GPU IS present but the cupy device path is dead → eval/decode is silently running
        # on CPU-numpy, which on a 303M model is ~10-100x slower (a paid GPU pod burns hours).
        # This is a DEFECT, not the benign GPU-less fallback below — say so loudly with the fix.
        print("[GPU-WASTED] decode device path=CPU-numpy but an NVIDIA GPU IS PRESENT — the "
              "cupy path is dead (%s). eval/decode is running on CPU (SLOW). "
              "Install the GPU extra:  pip install 'anima-python[gpu]'  "
              "(CUDA 13 host: also  pip install 'cupy-cuda13x>=13.0,<14')." % st["reason"],
              file=sys.stderr)
    else:
        print(f"[GPU-FALLBACK] decode device path=CPU-numpy ({st['reason']})", file=sys.stderr)


def get_xp(*arrays):
    """Array-module dispatch a la cupy.get_array_module: returns cupy iff any of
    `arrays` is an actual cupy ndarray, else numpy. With zero arrays, returns
    cupy iff cuda_available() else numpy. Threading this through the hot-path
    functions below means there is ZERO hardcoded np/cupy branching inside the
    math — a numpy-array caller (every pre-existing call site) is byte-for-byte
    unchanged; only the device-resident weight path (see _device_residency)
    causes this to resolve to cupy."""
    if _cupy is not None:
        if arrays:
            return _cupy.get_array_module(*arrays)
        return _cupy if cuda_available() else np
    return np


def to_device(x):
    """Host numpy -> device array iff cuda_available(); no-op otherwise (the
    byte-exact CPU fallback path). Never called per-token in a loop — only once
    at weight-load (_device_residency) or at the rare SLW/CLML host round-trip
    gates inside _fwd_logits."""
    if cuda_available() and isinstance(x, np.ndarray):
        return _cupy.asarray(x)
    return x


def to_host(x):
    """Device array -> host numpy, else no-op passthrough. This is the ONLY
    device->host sync point in the per-token decode hot path (called once at
    the _fwd_logits/_fwd_trunk EXIT, never inside the L-layer/E-expert loop —
    H_9119: a per-op transfer inside the loop would silently re-create the
    scalar-glue bottleneck this whole path exists to remove)."""
    if _cupy is not None and isinstance(x, _cupy.ndarray):
        return _cupy.asnumpy(x)
    return x


def _device_residency(W):
    """One-time host->device upload of the GEMM/elementwise weight tensors —
    called ONCE per clm_load_weights (a full eval/decode session loads weights
    once and reuses them for every token/window), NOT per decode step. slw/clml
    side-lane tensors are left host-resident on purpose: slot_apply/lane_apply
    (core/slw.py, core/clml.py) are host-numpy-only implementations for a rare
    ablation-only lane, so _fwd_logits round-trips through host ONLY at those
    two gates — the common (no-SLW/no-CLML) trunk-conv path, which is the
    profiled ~92%-of-wall-time hot path, stays fully device-resident end to end."""
    # ATOMIC upload (OOM-safe): stage every device tensor into `s` FIRST, then
    # commit to W only once ALL uploads succeed. If any xp.asarray raises
    # cupy.cuda.memory.OutOfMemoryError mid-way, W is left FULLY host-resident
    # (untouched) so the caller can catch OOM and fall back to the byte-exact
    # CPU-numpy path with no mixed host/device weight dict (which would crash the
    # forward). Fixes the summer-GPU-contention OOM crash (a_gpu_default_no_optin
    # dont: a full-device path that hard-crashes on a transient OOM).
    xp = _cupy
    s = {}
    s["ecWt"] = xp.asarray(W["ecWt"]); s["ecB"] = xp.asarray(W["ecB"])
    s["tcWt"] = [xp.asarray(w) for w in W["tcWt"]]
    s["tcB"] = [xp.asarray(b) for b in W["tcB"]]
    s["eWt"] = [xp.asarray(w) for w in W["eWt"]]
    s["eB"] = [xp.asarray(b) for b in W["eB"]]
    s["rWt"] = xp.asarray(W["rWt"]); s["rB"] = xp.asarray(W["rB"])
    s["roWt"] = xp.asarray(W["roWt"]); s["roB"] = xp.asarray(W["roB"])
    s["embed"] = xp.asarray(W["embed"])
    s["tgG"] = [xp.asarray(g) for g in W["tgG"]]
    s["tgB"] = [xp.asarray(b) for b in W["tgB"]]
    s["noG"] = xp.asarray(W["noG"]); s["noB"] = xp.asarray(W["noB"])
    if W.get("bind_type", 0) != 0:
        for _k in ("WaWt", "WbWt", "WaB", "WbB"):
            if _k in W:
                s[_k] = xp.asarray(W[_k])
    W.update(s)                    # commit only if every upload above succeeded
    return W


# ── H_9200 E1 SLW eval-time controls (process-global; set by cli/evaluate.py) ──
# The gated-write forward-slot applies by default whenever a .clm carries an
# "SLW\x01" trailer. These two switches let the pre-registered controls run WITHOUT
# retraining (frozen-first · no tune-to-green): --slot-off forces γ=0 (bit-exact base
# trunk = slot-ablation), --slot-shuffle scrambles the WRITE address (shuffle-bind).
_SLW_GAMMA_OVERRIDE = None   # float 0.0 => ablate the slot lane (γ=0 passthrough)
_SLW_SHUFFLE_SEED = None     # int => permute the write address only (reads unpermuted)


def set_slw_controls(gamma_override=None, shuffle_seed=None):
    """Set the SLW eval-time controls (cli/evaluate.py --slot-off / --slot-shuffle)."""
    global _SLW_GAMMA_OVERRIDE, _SLW_SHUFFLE_SEED
    _SLW_GAMMA_OVERRIDE = gamma_override
    _SLW_SHUFFLE_SEED = shuffle_seed


# ── H_9423 CLMS store-bridge eval-time injection (process-global; set by cli/evaluate.py --store) ──
# The store content (8 entities + polarities + the queried slot) is RUNTIME data, never in the .clm.
# The CLMS lane stays passthrough (byte-identical, C0-f seal) until a store is injected here, so a .clm
# that carries a CLMS trailer decodes identically to base for every prompt outside a --store eval.
# The controls are pure eval-time switches on the injected store (no retraining · no tune-to-green):
# --store-oracle forces a=one-hot(target_slot) (C0-e positive control), --store-lambda overrides λ
# (0.0 = λ0 byte-identical control · 1.0 = store_only). The C2 key-shuffle / wrong-store controls are
# expressed by deranging store["entities"] / flipping store["pols"] in the injected dict.
_CLMS_STORE = None            # dict {"entities","pols","target_slot"} · None => passthrough
_CLMS_ORACLE = False          # --store-oracle (bypass the softmax lookup with the true slot)
_CLMS_LAM_OVERRIDE = None     # --store-lambda (None => file λ)
_CLMS_AUDIT = None            # H_9672 --store-addr-audit: a list store_apply appends addr diagnostics to (None => off)
_MBND_ON = False              # H_9698 --mouth-binder: the lane is opt-in even when the trailer exists
_MBND_ORDER_SCRAMBLE = False  # H_9698 control: derange the causal bank (same multiset, order gone)
_CLMS_QUERY = "qpos"          # H_9695 --store-query: "qpos" (H_9423 literal) | "every-token" (marker-free)
_CLMS_FUSE = "overwrite"      # H_9695 --store-fuse: "overwrite" (store_only) | "gated-add" (perturbation)
_IFAN_MODE = "off"            # H_9803 --fan-branch: "off" (parity) | "live" | "assignment-shuffle"
_IFAN_BRANCH = 0              # H_9803 which of the K proposal latents drives this decode
_IFAN_PERM_SEED = 9803        # H_9803 frozen permutation seed for the assignment-shuffle control


def set_ifan_lane(mode="off", branch=0, perm_seed=9803):
    """H_9803 branch-latent ideation-fan eval-time switch (cli/evaluate.py --fan-branch).

    mode "off" is the DEFAULT and is a hard parity seal: ifan_apply returns the caller's logits
    object unchanged (no copy, no arithmetic), so an IFAN-carrying .clm decodes byte-identically
    to the same .clm without the trailer. The `--fan-branch off` eval arm asserts exactly that."""
    global _IFAN_MODE, _IFAN_BRANCH, _IFAN_PERM_SEED
    _IFAN_MODE = str(mode or "off")
    _IFAN_BRANCH = int(branch)
    _IFAN_PERM_SEED = int(perm_seed)


def set_mouth_binder(on=False, order_scramble=False):
    """H_9698 mouth-binder eval-time switch. Trailer present + on=False ⇒ passthrough (the same
    'trailer有 lane無 = byte-identical' seal CLMS uses), so a binder-carrying .clm still reproduces
    its pre-binder numbers exactly."""
    global _MBND_ON, _MBND_ORDER_SCRAMBLE
    _MBND_ON = bool(on)
    _MBND_ORDER_SCRAMBLE = bool(order_scramble)


_CLMG_STATE = None            # live C-state (PureField c_vec[16]) for the GRAFT gate; None => gate OFF


def set_clmg_state(c_vec=None):
    """Supply the live consciousness state to the CLMG GRAFT gate (core/clmg.py).

    c_vec=None (the default, and the state after every reset) => the gate is OFF and the forward is
    EXACTLY the base ckpt's — the mechanical witness the GRAFT frozen table checks (max|Δlogits| must
    be 0 between gate-OFF and base). A ckpt carrying a CLMG trailer therefore decodes byte-identically
    to its organ until a caller deliberately hands it a C-state, mirroring the CLMS 'trailer有 store無'
    seal. ⚠️ This is an OPT-IN FORWARD WRITE CHANNEL (default-path-census-1): when set, the gate adds a
    continuous residual to the byte embeddings inside _fwd_trunk — count it in any absence-census."""
    global _CLMG_STATE
    _CLMG_STATE = None if c_vec is None else np.asarray(c_vec, dtype=np.float32)


def set_clms_store(store=None, oracle=False, lam_override=None, audit=None,
                   query="qpos", fuse="overwrite"):
    """Set the CLMS store-bridge eval-time injection (cli/evaluate.py --store). store=None => the lane
    is passthrough regardless of a present trailer (the trailer有 store無 byte-identical seal). audit =
    a list (H_9672 addr-audit) that store_apply appends {argmax,a_target,target} per qpos to; None => off
    (byte-identical forward)."""
    global _CLMS_STORE, _CLMS_ORACLE, _CLMS_LAM_OVERRIDE, _CLMS_AUDIT, _CLMS_QUERY, _CLMS_FUSE
    _CLMS_STORE = store
    _CLMS_ORACLE = oracle
    _CLMS_LAM_OVERRIDE = lam_override
    _CLMS_AUDIT = audit
    _CLMS_QUERY = query
    _CLMS_FUSE = fuse


# ── H_9407 consult-decode eval-time window override (process-global; set by cli/evaluate.py
# --consult-decode). None => the decode seed window stays the production literal 24, byte-for-byte.
# int T => clm_decode_topk_sampled_W right-aligns the seed into a T-byte window instead — the ONLY
# behavioural change is how much seed the mouth can see; forward math is untouched (the scoring lane
# already runs T=64). Widening T is un-truncating the seed, not out-of-distribution (conv trunk is
# causal-local, no positional encoding; trained seq_len=1024). ──
_CONSULT_DECODE_T = None


def set_consult_decode_window(T):
    """Set the free-decode seed window (cli/evaluate.py --consult-decode). None = production 24."""
    global _CONSULT_DECODE_T
    _CONSULT_DECODE_T = T


# ════════════════════════════════════════════════════════════════════════
# (a) SHARED — helpers byte-identical across clm_decode.py + bytegpt_decode.py
# ════════════════════════════════════════════════════════════════════════

def dt_exp(x, xp=None):
    """flame_math.hexa::dt_exp — halve until |xr|<=0.25, 12-term Taylor (k=1..11),
    then square r times. Vectorized; halving by 2 is exact in fp64, so the
    per-element halve-count r matches the hexa scalar while-loop exactly.
    (SHARED: bg's top-k sampler softmax uses the SAME dt_exp — was `from
    clm_decode import dt_exp` in bytegpt_decode.py.)
    xp: optional array module (cupy when the caller is device-resident, see
    get_xp/_fwd_trunk); default None infers numpy for every pre-existing
    host-numpy call site (zero behavior change off the GPU path)."""
    if xp is None:
        xp = get_xp(x)
    x = xp.asarray(x, dtype=xp.float64)
    scalar = (x.ndim == 0)
    x = xp.atleast_1d(x)
    xr = x.copy()
    r = xp.zeros(x.shape, dtype=xp.int64)
    mask = xp.abs(xr) > 0.25
    while mask.any():
        xr = xp.where(mask, xr / 2.0, xr)
        r = xp.where(mask, r + 1, r)
        mask = xp.abs(xr) > 0.25
    term = xp.ones_like(xr)
    acc = xp.ones_like(xr)
    k = 1
    while k < 12:
        term = term * xr / float(k)
        acc = acc + term
        k = k + 1
    rmax = int(r.max()) if r.size else 0
    s = 0
    while s < rmax:
        m = r > s
        acc = xp.where(m, acc * acc, acc)
        s = s + 1
    return float(acc[0]) if scalar else acc


# ── seeded top-k temperature sampler PRNG — BYTE-IDENTICAL across both mouths
# (clm_decode.hexa _clmd_mix32/_rng_next ≡ decode.hexa _g6_mix32/_rng_next;
# xorshift32 & 0xFFFFFFFF). Deduped to one copy.
_MASK = 0xFFFFFFFF


def _mix32(s):
    """_clmd_mix32 / _g6_mix32 — SplitMix32-style finalizer."""
    z = (s + 0x9E3779B9) & _MASK
    z = ((z ^ (z // 65536)) * 0x85EBCA6B) & _MASK
    z = ((z ^ (z // 8192)) * 0xC2B2AE35) & _MASK
    z = (z ^ (z // 65536)) & _MASK
    if z == 0:
        z = 0x9E3779B9
    return z


def _rng_next(s):
    """_clmd_rng_next / _g6_rng_next — xorshift32 step -> (state, u in [0,1))."""
    x = s & _MASK
    if x == 0:
        x = 0x9E3779B9
    x = (x ^ (x * 8192)) & _MASK
    x = (x ^ (x // 131072)) & _MASK
    x = (x ^ (x * 32)) & _MASK
    return x, (float(x) / 4294967296.0)


def _topk_sample(logits, vocab, top_k, temp, rng):
    """_clmd_topk_sample / _g6_topk_sample — top-k by repeated argmax (ties:
    first/strict >), /temp, dt_exp softmax (max-sub), inverse-CDF draw. logits:[V].
    (SHARED: both mouths' samplers had byte-identical bodies.)"""
    kcap = top_k if (top_k > 0 and top_k < vocab) else vocab
    taken = np.zeros(vocab, dtype=np.float64)
    sel_idx = []
    sel_val = []
    picks = 0
    while picks < kcap:
        bi = -1
        bv = 0.0
        for k in range(vocab):
            if taken[k] < 0.5:
                v = logits[k]
                if bi < 0 or v > bv:
                    bi = k; bv = v
        if bi < 0:
            picks = kcap
        else:
            taken[bi] = 1.0
            sel_idx.append(bi)
            sel_val.append(bv / temp)
            picks += 1
    nsel = len(sel_idx)
    mx = sel_val[0]
    for i in range(1, nsel):
        if sel_val[i] > mx:
            mx = sel_val[i]
    probs = []
    summ = 0.0
    for j in range(nsel):
        e = float(dt_exp(np.array(sel_val[j] - mx)))
        probs.append(e); summ += e
    s2, u = _rng_next(rng)
    target = u * summ
    acc = 0.0
    pick = sel_idx[nsel - 1]
    for p in range(nsel):
        acc += probs[p]
        if target <= acc:
            pick = sel_idx[p]
            break
    return pick, s2


# ════════════════════════════════════════════════════════════════════════
# (b) CONV (CLM ConvMoE) — verbatim port of core/clm_decode.hexa
#     (formerly core/clm_decode.py). PRNG/dt_exp reused from SHARED above.
# ════════════════════════════════════════════════════════════════════════

# ── primitive math — ported 1:1 from stdlib/flame/*.hexa ──

def dt_ln(x):
    """flame_math.hexa::dt_ln — u=(x-1)/(x+1); 2*Σ_{k=0..23} u^(2k+1)/(2k+1).
    KNOWN-BUGGY for x far from 1 (diverges); reproduced verbatim for parity."""
    x = np.asarray(x, dtype=np.float64)
    scalar = (x.ndim == 0)
    x = np.atleast_1d(x)
    u = (x - 1.0) / (x + 1.0)
    u2 = u * u
    termp = u.copy()
    acc = np.zeros_like(u)
    k = 0
    while k < 24:
        acc = acc + termp / float(2 * k + 1)
        termp = termp * u2
        k = k + 1
    out = 2.0 * acc
    return float(out[0]) if scalar else out


def dt_erf(x, xp=None):
    """flame_math.hexa::dt_erf — Abramowitz&Stegun 7.1.26, exp via dt_exp."""
    if xp is None:
        xp = get_xp(x)
    x = xp.asarray(x, dtype=xp.float64)
    scalar = (x.ndim == 0)
    x = xp.atleast_1d(x)
    sign = xp.where(x < 0.0, -1.0, 1.0)
    z = xp.abs(x)
    t = 1.0 / (1.0 + 0.3275911 * z)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    poly = ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t
    out = sign * (1.0 - poly * dt_exp(0.0 - z * z, xp))
    return float(out[0]) if scalar else out


_INV_SQRT2 = 0.70710678118654752440
_INV_SQRT2PI = 0.39894228040143267794


def _nn_normal_cdf(x, xp=None):
    if xp is None:
        xp = get_xp(x)
    return 0.5 * (1.0 + dt_erf(x * _INV_SQRT2, xp))


def nn_gelu_fwd(g, xp=None):
    """nn_lib.hexa::nn_gelu_fwd — GELU(x)=x*Phi(x), Phi via dt_erf (EXACT erf)."""
    if xp is None:
        xp = get_xp(g)
    g = xp.asarray(g, dtype=xp.float64)
    return g * _nn_normal_cdf(g, xp)


def _moe_exp(x, xp=None):
    """moe_lib.hexa::_moe_exp — ln2 range-reduce, 14-term Taylor, *2^n.
    DISTINCT from dt_exp (used ONLY in the MoE router softmax)."""
    if xp is None:
        xp = get_xp(x)
    x = xp.asarray(x, dtype=xp.float64)
    scalar = (x.ndim == 0)
    x = xp.atleast_1d(x)
    ln2 = 0.6931471805599453
    r = x.copy()
    n = xp.zeros(x.shape, dtype=xp.int64)
    m = r > 0.34657359
    while m.any():
        r = xp.where(m, r - ln2, r)
        n = xp.where(m, n + 1, n)
        m = r > 0.34657359
    m = r < -0.34657359
    while m.any():
        r = xp.where(m, r + ln2, r)
        n = xp.where(m, n - 1, n)
        m = r < -0.34657359
    term = xp.ones_like(r)
    summ = xp.ones_like(r)
    k = 1
    while k < 14:
        term = term * r / float(k)
        summ = summ + term
        k = k + 1
    # *2^n via exact power-of-two scaling (== repeated *2 / /2 in hexa)
    p = summ * xp.power(2.0, n.astype(xp.float64))
    return float(p[0]) if scalar else p


def _gn_sqrt(x):
    """gn_lib.hexa::_gn_sqrt — Newton-Raphson 40 iters from g0=x. scalar.
    (DIVERGENT twin of bg's dt_sqrt — DO NOT merge; distinct name kept.)"""
    if x <= 0.0:
        return 0.0
    g = x
    i = 0
    while i < 40:
        g = 0.5 * (g + x / g)
        i = i + 1
    return g


# ── H_9611 · --gn-freeze (GN-freeze ablation · RF isolation) ─────────────────
# GroupNorm(1) reduces over the WHOLE [T,C] slab, so a byte anywhere in the window
# moves mu/var and therefore EVERY position's output — a sequence-global, permutation-
# invariant O(L)-scalar channel that survives beyond the conv receptive field (H_9560).
# --gn-freeze pins mu/var to constants CALIBRATED ONCE on a pre-registered reference
# forward, making the normalizer input-independent => the trunk becomes strictly RF-local.
# Replaying a cemented score under the freeze isolates whether that global channel ever
# carried anything readout-relevant. Default (None) is BYTE-IDENTICAL to the live path.
# The affine (gamma/beta) is NEVER touched. The reference is an explicit caller argument,
# never swept (a swept constant would be tune-to-green — H_9611 verdict-integrity clause).
_GN_FREEZE = None          # None = live (default) | dict{key -> (mu, var)} = frozen


def gn_freeze_active():
    return _GN_FREEZE is not None


def gn_freeze_set(stats):
    """Pin GN stats. stats = dict{key -> (mu, var)} from gn_freeze_calibrate."""
    global _GN_FREEZE
    _GN_FREEZE = stats


def gn_freeze_clear():
    global _GN_FREEZE
    _GN_FREEZE = None


def gn_freeze_calibrate(W, tok, T):
    """One reference forward with capture ON → dict{key -> (mu, var)} for every GN call.
    The caller pre-registers WHICH reference; this only records what that reference gives."""
    global _GN_FREEZE
    prev = _GN_FREEZE
    cap = {}
    _GN_FREEZE = None                      # calibrate against the LIVE path
    try:
        _gn_capture(cap)
        _fwd_trunk(W, tok, T)
    finally:
        _gn_capture(None)
        _GN_FREEZE = prev
    return cap


_GN_CAP = None


def _gn_capture(sink):
    global _GN_CAP
    _GN_CAP = sink


def nn_groupnorm_fwd(x, gamma, beta, T, C, G, xp=None, gn_key=None, per_position=False):
    """gn_lib.hexa::nn_groupnorm_fwd — eps=1e-5. x:[T,C]. Returns y:[T,C].
    Here G is always 1 (=> normalize over all C per the whole [T,C] group).

    per_position=True (H_9875 · mirrors core/model.py::PerPositionGroupNorm, which reshapes
    (B,C,T) -> (B*T,C,1) before GroupNorm) reduces over the cg channels of ONE row instead of the
    whole [T,cg] block, so m = cg and position t's output depends on position t alone. That is the
    difference between a sequence-global bus and a causal-safe norm: with the default reduction a
    byte at position 0 moves the statistics that every later position — including the query byte —
    is divided by. A ckpt trained with --trunk-norm position scored through the default reduction
    is not that model, which is why the trainer refuses to call such a score engine-native. Default
    False keeps every existing .clm byte-identical.
    The μ/σ² scalar reduction is pulled to a host python float ONCE per group
    (a single device->host sync of one scalar) so the bit-exact 40-iter Newton
    `_gn_sqrt` runs in plain host float64 — identical numerics to the CPU path,
    and avoids one GPU kernel launch per Newton iteration (40x/call)."""
    if xp is None:
        xp = get_xp(x)
    eps = 0.00001
    cg = C // G
    m = float(cg * T)
    x = x.reshape(T, C)
    y = xp.empty_like(x)
    if per_position:
        # Per-row statistics (m = cg). _GN_FREEZE/_GN_CAP are sequence-global instruments and are
        # NOT defined for this reduction, so they are refused rather than silently misapplied.
        if _GN_FREEZE is not None or _GN_CAP is not None:
            raise ValueError("nn_groupnorm_fwd: --gn-freeze / gn-cap are sequence-global "
                             "instruments and have no meaning under per-position normalization")
        mp = float(cg)
        for grp in range(G):
            c0 = grp * cg
            sl = x[:, c0:c0 + cg]
            mu_r = sl.sum(axis=1) / mp
            d_r = sl - mu_r.reshape(T, 1)
            var_r = (d_r * d_r).sum(axis=1) / mp
            inv_r = xp.asarray([1.0 / _gn_sqrt(float(v) + eps) for v in var_r]).reshape(T, 1)
            y[:, c0:c0 + cg] = gamma[c0:c0 + cg] * (d_r * inv_r) + beta[c0:c0 + cg]
        return y
    for grp in range(G):
        c0 = grp * cg
        sl = x[:, c0:c0 + cg]
        # H_9611 --gn-freeze: pinned mu/var (input-independent => trunk is RF-local).
        # Default path (_GN_FREEZE None) is untouched and byte-identical.
        frz = None if _GN_FREEZE is None else _GN_FREEZE.get((gn_key, grp))
        if frz is None:
            mu = sl.sum() / m
            var = ((sl - mu) * (sl - mu)).sum() / m
        else:
            mu, var = frz                      # pre-registered reference constants
        if _GN_CAP is not None:                # calibration pass records what the ref gives
            _GN_CAP[(gn_key, grp)] = (float(mu), float(var))
        inv = 1.0 / _gn_sqrt(float(var) + eps)
        xh = (sl - mu) * inv
        y[:, c0:c0 + cg] = gamma[c0:c0 + cg] * xh + beta[c0:c0 + cg]
    return y


def nn_moe_softmax(logits, T, E, xp=None):
    """moe_lib.hexa::nn_moe_softmax — stable softmax over E via _moe_exp. logits:[T,E]."""
    if xp is None:
        xp = get_xp(logits)
    logits = logits.reshape(T, E)
    mx = logits.max(axis=1, keepdims=True)
    ev = _moe_exp(logits - mx, xp)
    s = ev.sum(axis=1, keepdims=True)
    return ev / s


def nn_moe_router_fwd(logits_r, ex_out, T, E, C, xp=None):
    """moe_lib.hexa::nn_moe_router_fwd — y[t,c]=Σ_e probs[t,e]*ex_out[e,t,c].
    ex_out:[E,T,C]. Returns y:[T,C]."""
    if xp is None:
        xp = get_xp(logits_r, ex_out)
    probs = nn_moe_softmax(logits_r, T, E, xp)          # [T,E]
    ex = ex_out.reshape(E, T, C)
    # y[t,c] = Σ_e probs[t,e]*ex[e,t,c]
    y = xp.einsum('te,etc->tc', probs, ex)
    return y


def nn_ce_loss_allpos(logits, targets, T, V):
    """nn_lib.hexa::nn_ce_loss_allpos — mean over T of -ln(softmax[tgt]).
    Stable softmax via dt_exp, pt_safe floor 1e-6, -ln via dt_ln. logits:[T,V]."""
    logits = logits.reshape(T, V)
    total = 0.0
    for t in range(T):
        row = logits[t]
        mx = row.max()
        tot = float(dt_exp(row - mx).sum())
        tgt = int(targets[t])
        p_t = float(dt_exp(np.array(row[tgt] - mx))) / tot
        pt_safe = p_t if p_t >= 0.000001 else 0.000001
        total = total + (0.0 - float(dt_ln(np.array(pt_safe))))
    return total / float(T)


# ── .clm file parse + int4 dequant — 1:1 from clm_decode.hexa _clmd_load* ──

def _rd_u32(rb, off):
    return rb[off] | (rb[off + 1] << 8) | (rb[off + 2] << 16) | (rb[off + 3] << 24)


def clm_decodable(path):
    """clm_decode.hexa::clm_decodable — CLM\\x01 header AND CLMX v0.2 trailer."""
    try:
        rb = open(path, 'rb').read()
    except Exception:
        return False
    if len(rb) < 5:
        return False
    if not (rb[0] == 67 and rb[1] == 76 and rb[2] == 77 and rb[3] == 1):
        return False
    nblk = rb[4]
    off = 5
    b = 0
    while b < nblk:
        if off + 8 > len(rb):
            return False
        cout = _rd_u32(rb, off)
        rest = _rd_u32(rb, off + 4)
        off = off + 8
        n = cout * rest
        off = off + (n + 1) // 2
        off = off + cout * 4
        b = b + 1
    if off + 5 > len(rb):
        return False
    return rb[off] == 67 and rb[off + 1] == 76 and rb[off + 2] == 77 and rb[off + 3] == 88


def clm_config(path):
    """clm_decode.hexa::clm_config — recover (d,K,V,E,L,nblk) from header."""
    if not clm_decodable(path):
        return {"ok": False}
    rb = open(path, 'rb').read()
    nblk = rb[4]
    d = _rd_u32(rb, 5)
    rest0 = _rd_u32(rb, 9)
    K = rest0 // d
    off = 5
    bi = 0
    E = 2
    V = 256
    while bi < nblk:
        c = _rd_u32(rb, off)
        r = _rd_u32(rb, off + 4)
        if bi == nblk - 2:
            E = c
        if bi == nblk - 1:
            V = c
        n = c * r
        off = off + 8 + (n + 1) // 2 + c * 4
        bi = bi + 1
    L = nblk - E - 3
    return {"ok": True, "d": d, "K": K, "V": V, "E": E, "L": L, "nblk": nblk}


def _load_block(rb, off):
    """_clmd_load_block — int4-sym dequant: w = (nibble-8) * per-channel-scale.
    Returns (w_2d[cout,rest], new_off)."""
    cout = _rd_u32(rb, off); off += 4
    rest = _rd_u32(rb, off); off += 4
    n = cout * rest
    nbytes = (n + 1) // 2
    raw = np.frombuffer(rb, dtype=np.uint8, count=nbytes, offset=off).astype(np.int64)
    off += nbytes
    low = (raw & 0xF) - 8
    high = ((raw >> 4) & 0xF) - 8
    codes = np.empty(2 * len(raw), dtype=np.float64)
    codes[0::2] = low
    codes[1::2] = high
    codes = codes[:n]
    scales = np.frombuffer(rb, dtype='<f4', count=cout, offset=off).astype(np.float64)
    off += cout * 4
    w = codes.reshape(cout, rest) * scales[:, None]
    return w, off


def _load_ext(rb, off):
    """_clmd_load_ext — length-prefixed fp32 tensor (n:u32, then n*f32 LE)."""
    n = _rd_u32(rb, off); off += 4
    vals = np.frombuffer(rb, dtype='<f4', count=n, offset=off).astype(np.float64)
    off += n * 4
    return vals, off


_TRUNK_NORM = "global"     # H_9875 · set per-ckpt by clm_load_weights from the CNRM trailer


def clm_load_weights(path):
    """_clmd_load — full file parse into a weight dict. Conv weights are kept
    pre-transposed as Wt[Kdim,Cout] (the _clmd_scratch_new transpose, applied
    once) since the py forward GEMMs xcol[T,Kdim] @ Wt[Kdim,Cout]."""
    _k = _wload_key(path)
    if _k is not None and _k in _WLOAD_CACHE:
        return _WLOAD_CACHE[_k]
    if not clm_decodable(path):
        return {"ok": False}
    rb = open(path, 'rb').read()
    nblk = rb[4]
    d = _rd_u32(rb, 5)
    rest0 = _rd_u32(rb, 9)
    K = rest0 // d
    # walk to find E (block nblk-2 cout), V (block nblk-1 cout)
    off = 5
    bi = 0
    E = 2
    V = 256
    while bi < nblk:
        c = _rd_u32(rb, off)
        r = _rd_u32(rb, off + 4)
        if bi == nblk - 2:
            E = c
        if bi == nblk - 1:
            V = c
        n = c * r
        off = off + 8 + (n + 1) // 2 + c * 4
        bi = bi + 1
    L = nblk - E - 3

    # ── conv blocks, in order: ec, tc[L], eW[E], rW, roW ──
    off = 5
    ecW, off = _load_block(rb, off)              # [d, d*K]
    tcW = []
    for _ in range(L):
        w, off = _load_block(rb, off); tcW.append(w)   # [d, d*K]
    eW = []
    for _ in range(E):
        w, off = _load_block(rb, off); eW.append(w)    # [d, d*K]
    rW, off = _load_block(rb, off)               # [E, d]
    roW, off = _load_block(rb, off)              # [V, d]
    off = off + 5                                # skip "CLMX" + n_ext byte

    # ── ext tensors, in order ──
    embed, off = _load_ext(rb, off)              # [V*d]
    ecB, off = _load_ext(rb, off)                # [d]
    tcB = []
    for _ in range(L):
        v, off = _load_ext(rb, off); tcB.append(v)     # [d]
    eB = []
    for _ in range(E):
        v, off = _load_ext(rb, off); eB.append(v)      # [d]
    rB, off = _load_ext(rb, off)                 # [E]
    roB, off = _load_ext(rb, off)                # [V]
    tgG = []
    for _ in range(L):
        v, off = _load_ext(rb, off); tgG.append(v)     # [d]
    tgB = []
    for _ in range(L):
        v, off = _load_ext(rb, off); tgB.append(v)     # [d]
    noG, off = _load_ext(rb, off)                # [d]
    noB, off = _load_ext(rb, off)                # [d]

    # ── H_9643 CLMF (optional) — the faction lane. Absent on every pre-H_9643 .clm, in which
    # case n_factions stays 0, GroupNorm keeps G=1 and the bridge is skipped => byte-identical.
    n_factions, fbLam, fbG, fbW, fbB = 0, 0.0, None, None, None
    if off + 4 <= len(rb) and bytes(rb[off:off + 4]) == b"CLMF":
        off = off + 4
        n_factions = int(struct.unpack_from("<I", rb, off)[0]); off = off + 4
        fbLam = float(struct.unpack_from("<f", rb, off)[0]); off = off + 4
        fbG, off = _load_ext(rb, off)            # [d]   pre-sigmoid channel gate
        fbW, off = _load_ext(rb, off)            # [d*d] 1x1 bridge conv (unmasked — the mask is
        fbB, off = _load_ext(rb, off)            # [d]   re-derived from n_factions at forward)

    # pre-transpose conv weights -> Wt[Kdim, Cout] (= w_2d.T)
    W = {
        "ok": True, "d": d, "E": E, "V": V, "K": K, "L": L,
        "n_factions": n_factions, "fbLam": fbLam, "faction_lam": None,
        "fbG": fbG, "fbW": fbW, "fbB": fbB,
        "ecWt": ecW.T.copy(), "ecB": ecB,
        "tcWt": [w.T.copy() for w in tcW], "tcB": tcB,
        "eWt": [w.T.copy() for w in eW], "eB": eB,
        "rWt": rW.T.copy(), "rB": rB,
        "roWt": roW.T.copy(), "roB": roB,
        "embed": embed.reshape(V, d),
        "tgG": tgG, "tgB": tgB, "noG": noG, "noB": noB,
        "bind_type": 0,
    }

    # ── optional CLMB bind-readout section (serialize_v3_bind) ──────────────
    # "CLMB" = bytes 67,76,77,66. Present only when the .clm was serialized
    # with a Hadamard/linear bind readout retained in-forward (H_1818).
    # If absent, bind_type=0 and the standard additive _conv1d readout is used.
    # CLMB layout (after CLMX ext arrays):
    #   CLMB magic  67,76,77,66
    #   bind_type   u8  (1=Hadamard u*v, 2=linear u+v)
    #   Wa block    (k, d) int4-sym conv block
    #   Wb block    (k, d) int4-sym conv block
    #   WaB ext     u32 k + k*f32
    #   WbB ext     u32 k + k*f32
    # In a CLMB file, roW holds Wo (V, k) NOT (V, d); roWt = (k, V).
    if (off + 5 <= len(rb)
            and rb[off] == 67 and rb[off + 1] == 76
            and rb[off + 2] == 77 and rb[off + 3] == 66):
        off += 4                                   # skip "CLMB"
        bind_type = rb[off]; off += 1
        WaW, off = _load_block(rb, off)            # (k, d)
        WbW, off = _load_block(rb, off)            # (k, d)
        WaB_ext, off = _load_ext(rb, off)          # (k,)
        WbB_ext, off = _load_ext(rb, off)          # (k,)
        W["bind_type"] = int(bind_type)
        W["WaWt"] = WaW.T.copy()                   # (d, k)
        W["WbWt"] = WbW.T.copy()                   # (d, k)
        W["WaB"] = WaB_ext
        W["WbB"] = WbB_ext
        # roWt is already Wo.T = (k, V); roB is already WoB (V,) — loaded above.

    # ── optional "SLW\x01" gated-write forward-slot trailer (H_9200 E1) ──────
    # End of the trailer chain (after CLMX ext / CLMB), read at the current `off`.
    # Absent/short => slw=None => forward is byte-identical to today (passthrough).
    # Codec is CORE-owned in core/slw.py (owner directive: core lives in core/).
    from slw import read_slw
    W["slw"], off = read_slw(rb, off)

    # ── optional "CLML" read-side context-pooling lane trailer (fork A · H_9235) ──
    # Appended after the SLW trailer. Absent/short => clml=None => byte-identical forward
    # (lane_apply passthrough). CORE-owned codec in core/clml.py.
    from clml import read_clml
    W["clml"], off = read_clml(rb, off, W["d"], W["V"])

    # ── optional "CLMS" store-bridge lane trailer (H_9423) ──
    # Appended after the CLML trailer (chain end). Absent/short => clms=None; and even when
    # present, the lane is passthrough until a store is injected via set_clms_store (the store is
    # RUNTIME data, never in the .clm) => trailer有 store無 = byte-identical. CORE codec core/clms.py.
    from clms import read_clms
    W["clms"], off = read_clms(rb, off, W["d"], W["V"])
    from mbnd import read_mbnd                                   # H_9698 mouth-binder (absent ⇒ None)
    W["mbnd"], off = read_mbnd(rb, off, W["d"], W["V"])
    from ifan import read_ifan                                   # H_9803 branch-latent fan (absent ⇒ None)
    W["ifan"], off = read_ifan(rb, off, W["d"], W["V"])

    # ── optional "TFLD" write-side tension-field trailer (H_9805 · chain END) ──
    # Appended LAST by cli/train.py, so it is read last. Absent/short => tfld=None => the forward
    # never evaluates the lane => byte-identical to today (the same passthrough seal every lane
    # above uses). Unlike the read-side lanes this one fires PRE-TRUNK, on the embeddings, because
    # the hypothesis IS that the trunk must compute OVER the field rather than read it off the top.
    from tension_field import read_tfld
    W["tfld"], off = read_tfld(rb, off, W["d"])
    # ── optional "CLMG" GRAFT consciousness→language gate trailer (chain END, after TFLD) ──
    # Absent/short => W["clmg"] is None => the embedding residual block below is skipped entirely and
    # the forward is byte-identical. Even WITH the trailer, the gate stays OFF until a live C-state is
    # supplied via set_clmg_state() — so a grafted ckpt decodes exactly like its base by default.
    from clmg import read_clmg
    W["clmg"], off = read_clmg(rb, off, W["d"])

    # ── optional "CNRM" trunk-norm marker (H_9875 · chain END, 1 payload byte) ──
    # Absent => "global" => byte-identical to every .clm written before this lane existed. Present
    # with payload 1 => the trunk was trained with per-position normalization, and the decode above
    # must reduce per row or it is scoring a different model (the trainer used to warn that no such
    # lane existed; this is that lane).
    W["trunk_norm"] = "global"
    if len(rb) - off >= 5 and bytes(rb[off:off + 4]) == b"CNRM":
        W["trunk_norm"] = "position" if int(rb[off + 4]) == 1 else "global"
        off += 5

    # ── GPU device residency (a_gpu_default_no_optin: DEFAULT-ON, no opt-in flag) ──
    # Upload the GEMM/elementwise weight tensors to the device ONCE here (a full
    # eval/decode session loads weights once and reuses them for every token/
    # window) — never per decode step. QA-visible signal: [GPU-FIRED]/[GPU-FALLBACK]
    # on stderr, once per process (core/CLAUDE.md gotcha: confirm the fast path is
    # actually reached before blaming a scalar-glue ceiling).
    _log_gpu_status_once()
    if cuda_available():
        try:
            _device_residency(W)
        except _CUPY_OOM as _oom:          # GPU momentarily full (shared box) —
            global _CUDA_AVAILABLE          # fall back byte-exact to CPU-numpy for
            _CUDA_AVAILABLE = False          # this AND every subsequent load, W is
            try:                             # left fully host-resident (atomic stage).
                _cupy.get_default_memory_pool().free_all_blocks()
            except Exception:
                pass
            print("[GPU-OOM-FALLBACK] weight residency OOM -> CPU-numpy (%s)" % _oom,
                  file=sys.stderr)

    if _k is not None:
        _WLOAD_CACHE[_k] = W
    return W


# ── forward — 1:1 from clm_decode.hexa _clmd_conv1d / _clmd_fwd_logits_sc ──

def _conv1d(x, Wt, b, T, Cin, Cout, K, dil, xp=None):
    """_clmd_conv1d_pre (host path) — causal dilated im2col + matmul + bias.
    x:[T,Cin], Wt:[Cin*K, Cout], b:[Cout]. Returns y:[T,Cout].
    im2col layout: xcol[t, ci*K + k] = x[t - dil*(K-1-k), ci] (0 if p<0).
    xp: array module (cupy when x/Wt are device-resident — see _device_residency);
    this is the profiled hot path (~92% of decode wall time, H_9200 measurement),
    so it is the primary GPU-accelerated op — the matmul `xcol @ Wt` dispatches
    to cuBLAS when xp is cupy, unchanged formula otherwise."""
    if xp is None:
        xp = get_xp(x, Wt)
    Kdim = Cin * K
    x = x.reshape(T, Cin)
    xcol = xp.zeros((T, Cin, K), dtype=xp.float64)
    t_idx = xp.arange(T)
    for k in range(K):
        offset = dil * (K - 1 - k)
        p = t_idx - offset
        valid = p >= 0
        xcol[valid, :, k] = x[p[valid], :]
    xcol = xcol.reshape(T, Kdim)
    mm = xcol @ Wt                                # [T, Cout]
    return mm + b[None, :]


def _apply_edits(xt, edits, li, T, d, xp):
    """H_9331 BIND-LOCUS — apply the causal interventions registered for trunk depth `li`
    IN PLACE inside the canonical forward, then let the SAME ops carry the edited residual
    all the way to the readout. The manipulation happens inside the engine, not beside it
    (`a_experiment_engine_native`); a side-harness that re-implemented this could not
    guarantee the number reproduces on the production path.

    depth convention: li=0 is after the embed-conv, li=k (1..L) is after trunk layer k-1.

    An edit is a dict {layer, t0, t1, mode, ...} over the byte span [t0, t1):
      patch  donor:[t1-t0, d]  — overwrite the span with a donor's hidden (Stage A swap)
      steer  vec:[d], delta    — h += delta * v̂            (fixed-size push)
      mask   chans:[m]         — zero those channels over the span (H_9643 faction lesion:
             kill faction f, read the per-domain ΔCE dissociation)
      proj   vec:[d], target   — h += (target - h·v̂) * v̂   (Stage B projection-MATCH: move
             the span's projection ONTO v̂ to an exact value, so arms are matched on the
             MEDIATING covariate rather than on a nominal norm — control-must-match-
             mediating-covariate; a fixed alpha would leave the realized projection
             different in each arm, which is the confound that rule was earned on)
    """
    for e in edits:
        if int(e["layer"]) != li:
            continue
        t0 = int(e["t0"]); t1 = int(e["t1"])
        if t0 < 0 or t1 > T or t1 <= t0:
            raise ValueError("bind-locus edit span [%d,%d) outside window T=%d" % (t0, t1, T))
        mode = e["mode"]
        if mode == "mask":
            # H_9643 faction lesion — zero a channel set for the span, INSIDE the canonical
            # forward, so the ablated residual flows through the same ops to the readout
            # (a_experiment_engine_native: the manipulation is the engine's, not a harness's).
            chans = xp.asarray(e["chans"], dtype=xp.int64)
            xt = xt.copy()
            xt[t0:t1, chans] = 0.0
            continue
        if mode == "patch":
            donor = xp.asarray(e["donor"], dtype=xt.dtype).reshape(t1 - t0, d)
            xt[t0:t1] = donor
        elif mode == "steer":
            v = xp.asarray(e["vec"], dtype=xt.dtype).reshape(d)
            xt[t0:t1] = xt[t0:t1] + float(e["delta"]) * v
        elif mode == "proj":
            v = xp.asarray(e["vec"], dtype=xt.dtype).reshape(d)
            tgt = float(e["target"])
            p = xt[t0:t1] @ v                                  # [t1-t0] current projection
            xt[t0:t1] = xt[t0:t1] + (tgt - p).reshape(-1, 1) * v.reshape(1, d)
        else:
            raise ValueError("unknown bind-locus edit mode: %r" % (mode,))
    return xt


def _fwd_trunk(W, tok, T, taps=None, edits=None, routes=None, tap_depth=None, tap_out=None):
    """Trunk forward through the FINAL groupnorm — returns yn:[T, d], the pre-readout,
    PRE-E1-slot penultimate hidden (post-MoE, post final-GN). This is the pure-trunk
    concept representation (E1-slot independent, matching the H_1822 β 303M-trunk-penult
    precedent). Extracted from _fwd_logits so the decode path (slot+readout applied) and
    the read-only hidden tap (clm_forward_hidden, ρ·weave / γ binding-lane probe H_9235)
    share ONE byte-identical trunk forward.

    GPU device path: xp is inferred ONCE from W["ecWt"] (device-resident iff
    cuda_available() at load time, see _device_residency) and threaded through
    every op below — the whole L-layer/E-expert loop runs device-resident end to
    end with NO host<->device transfer inside the loop (H_9119 lesson); only the
    token-id upload (entry) crosses the boundary, once per call."""
    d = W["d"]; E = W["E"]; K = W["K"]; L = W["L"]
    xp = get_xp(W["ecWt"])
    # embedding
    ids = tok.astype(np.int64)
    if xp is not np:
        ids = xp.asarray(ids)
    xe = W["embed"][ids]                          # [T, d]
    # ── H_9805 TFLD: the WRITE-SIDE residual, added to the embeddings BEFORE embed_conv ──
    # This mirrors core/model.py's training-time injection exactly (same place, same formula), so a
    # ckpt trained with --tension-field decodes with the field it was trained under. No trailer =>
    # W["tfld"] is None => this block is skipped entirely and the forward is byte-identical.
    # The reduction is host-numpy (it is integer bucket work, not GEMM), so on the device path the
    # embeddings make ONE host round-trip when the lane fires. That is deliberate: keeping the
    # field's arithmetic on a single device removes the cuBLAS-vs-CPU accumulation-order confound
    # that already bit a hidden-reading probe at 2.5e-14 (decode-py-4). Lane-off decodes never pay it.
    _tfld = W.get("tfld")
    if _tfld is not None:
        from tension_field import ARM_NAME, tension_apply
        _arm = ARM_NAME.get(int(_tfld.get("arm_code", 0)), "off")
        if _arm != "off":
            _xh = tension_apply(to_host(xe), tok, _tfld, arm=_arm)
            xe = xp.asarray(_xh) if xp is not np else _xh
    # ── CLMG GRAFT gate (H_GRAFT): the consciousness→language coupling, added to the embeddings
    # BEFORE embed_conv — the SAME site as TFLD, and deliberately NOT a post-trunk lane: every
    # existing lane taps the logits row, where a per-state additive vector is just a per-state BIAS
    # and MI is satisfiable by static unigram tilts that never touch the organ. Here the frozen
    # trunk's full depth transforms the gate, so per-state distributions differ context-dependently.
    # ⚠️ OPT-IN FORWARD WRITE CHANNEL (default-path-census-1): the gate is a real continuous write
    # into the forward pass, but it fires ONLY when the ckpt carries a CLMG trailer AND a live
    # C-state was supplied via set_clmg_state(). No trailer or no C-state ⇒ skipped ⇒ byte-identical.
    _clmg = W.get("clmg")
    if _clmg is not None and _CLMG_STATE is not None:
        from clmg import gate_offset
        _xh = to_host(xe)
        _off = gate_offset(_clmg, _CLMG_STATE, float(np.sqrt(np.mean(_xh * _xh))) + 1e-8)
        if _off is not None:
            _xh = (_xh + _off[None, :]).astype(_xh.dtype)
            xe = xp.asarray(_xh) if xp is not np else _xh
    # ec conv (K, dil=1)
    xt = _conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1, xp)
    if taps is not None:
        taps[0] = to_host(xt).copy()
    if tap_out is not None and tap_depth == 0:                     # H_9720-ⓐ single-activation fresh tap
        tap_out["x"] = to_host(xt).copy()
    if edits is not None:
        xt = _apply_edits(xt, edits, 0, T, d, xp)
    # L trunk layers: xt = xt + gelu(groupnorm(conv(xt)))
    DIL_CAP = 512
    dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = _conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff, xp)
        # H_9643: GroupNorm groups follow the faction split. G=1 pools mean/var over ALL d
        # channels, which is a cross-faction path even when the conv is grouped — the trained
        # model used GN(K), so decoding it with G=1 would silently produce different activations.
        # W["n_factions"] is 0 (absent CLMF) for every pre-H_9643 ckpt => G=1 => byte-identical.
        _gf = W.get("n_factions", 0) or 1
        hn = nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, _gf, xp,
                              per_position=(W.get("trunk_norm", "global") == "position"),
                              gn_key=("trunk", li))
        hg = nn_gelu_fwd(hn, xp)
        xt = xt + hg.reshape(T, d)
        if taps is not None:
            taps[li + 1] = to_host(xt).copy()
        if tap_out is not None and (li + 1) == tap_depth:         # H_9720-ⓐ single-activation fresh tap
            tap_out["x"] = to_host(xt).copy()
        if edits is not None:
            xt = _apply_edits(xt, edits, li + 1, T, d, xp)
        dil = dil * 2
    # H_9643 cross-faction bridge — the trunk-exit debate module, applied BEFORE the MoE
    # (the same position core/model.py's forward uses). Absent CLMF => faction_lam is None =>
    # the golden path is untouched. faction_lam is an explicit override slot: evaluate sets it to
    # 0.0 to run the debate-OFF ablation without editing a single weight.
    xt = _faction_bridge_apply(W, xt, T, d, xp)
    # router conv (K=1, Cout=E)
    logits_r = _conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1, xp)   # [T, E]
    if routes is not None:
        # H_9355 LOCUS-CAUSAL · route audit tap. The SAME nn_moe_softmax the mixer runs
        # (nn_moe_router_fwd recomputes it from the same logits — identical input, identical
        # function, so the tap is byte-identical to the mix the decode consumes). Kept OUT of
        # the mixer's own code path on purpose: the audit must not be able to perturb the
        # production forward, so it costs one extra softmax over [T,E] (E=3) and nothing else.
        routes["probs"] = to_host(nn_moe_softmax(logits_r, T, E, xp)).copy()   # [T, E]
        routes["logits"] = to_host(logits_r).copy()                            # [T, E]
    # E experts: gelu(conv(xt))
    ex_out = xp.empty((E, T, d), dtype=xp.float64)
    for ej in range(E):
        eo = _conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1, xp)
        ex_out[ej] = nn_gelu_fwd(eo, xp).reshape(T, d)
    # MoE router mix
    y = nn_moe_router_fwd(logits_r, ex_out, T, E, d, xp)          # [T, d]
    # final groupnorm — H_9643: G follows the faction split (absent CLMF => 0 => G=1 => unchanged)
    _gf = W.get("n_factions", 0) or 1
    yn = nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, _gf, xp, gn_key=("out",),
                          per_position=(W.get("trunk_norm", "global") == "position"))
    return yn


def _faction_bridge_apply(W, xt, T, d, xp=None):
    """H_9643 cross-faction bridge (core/model.py FactionBridge twin).

    x <- x + lam * sigmoid(gate) * ((M_cross * W_b) x), M_cross zeroing every WITHIN-faction
    entry so only faction->faction terms survive. The mask is RE-DERIVED here from n_factions —
    the serializer deliberately stores W_b unmasked so a reader can tell a structural zero from
    a learned one.

    Returns xt unchanged when the ckpt carries no CLMF section (n_factions absent/0), so every
    pre-H_9643 .clm decodes byte-identically. W["faction_lam"] overrides the trailer's lam when
    present — that is the debate ON/OFF ablation (lam=0.0 is an exact identity).
    """
    K = int(W.get("n_factions", 0) or 0)
    if K <= 0 or "fbW" not in W:
        return xt
    xp = xp if xp is not None else np
    lam = W["faction_lam"] if W.get("faction_lam", None) is not None else W["fbLam"]
    lam = float(lam)
    if lam == 0.0:
        return xt                                  # exact identity — the OFF arm
    per = d // K
    idx = xp.arange(d) // per
    m_cross = (idx[:, None] != idx[None, :]).astype(xt.dtype)     # [d_out, d_in]
    Wb = xp.asarray(W["fbW"], dtype=xt.dtype).reshape(d, d) * m_cross
    gate = 1.0 / (1.0 + xp.exp(-xp.asarray(W["fbG"], dtype=xt.dtype)))   # sigmoid, [d]
    h = xt @ Wb.T + xp.asarray(W["fbB"], dtype=xt.dtype)[None, :]        # [T, d]
    return xt + lam * gate[None, :] * h


def clm_forward_hidden(W, tok, T):
    """Read-only penultimate-hidden tap — the pre-readout, pre-E1-slot yn:[T, d] (post-MoE,
    post final groupnorm) for token ids tok:[T]. Engine-native: the EXACT production trunk
    forward (_fwd_trunk, shared with _fwd_logits), so the dumped representation is
    byte-identical to what the gates decode over. For the ρ·weave held-out-pair
    recombination / γ binding-lane probe (H_9235): dumps the pure-trunk concept
    representation a read-side lane consumes. No decode sampling / readout / perturbation.
    Always returns host numpy (to_host) — external callers (clm_penult_pooled_W) index
    element-by-element in a python loop, which needs host memory."""
    ta = tok if hasattr(tok, "astype") else np.array(tok, dtype=np.float64)
    return to_host(_fwd_trunk(W, ta, T))


def clm_forward_taps(W, tok, T):
    """H_9331 BIND-LOCUS · READ side — every trunk depth's residual for tok:[T], as a dict
    {0: xt_after_embed_conv, 1..L: xt_after_trunk_layer_k}, each host numpy [T, d].

    Same forward as production (_fwd_trunk), just observed. Use it to ask WHERE in
    (depth, byte-position) a polarity is linearly readable — but note a read-only map
    cannot cement a verdict on its own: what a probe can read is not necessarily what the
    operator CONSUMES (the read-side-exhausted lesson). The causal answer comes from
    clm_forward_logits_edited."""
    ta = tok if hasattr(tok, "astype") else np.array(tok, dtype=np.float64)
    taps = {}
    _fwd_trunk(W, ta, T, taps=taps)
    return taps


def clm_forward_routes(W, tok, T):
    """H_9355 LOCUS-CAUSAL — the ConvMoE router's per-position expert distribution for tok:[T],
    as host numpy probs:[T, E] (rows sum to 1) plus the raw router logits:[T, E].

    This is the ONE thing a hidden-space probe cannot tell you: not "what does the model
    represent here" but "WHICH EXPERT COMPUTED IT". The two-lane reading of the binding wall
    (a declarative store and an operator store that never exchange values) makes a physical
    prediction — the two surfaces should be computed by different experts. A shared route
    falsifies the physical form of that model and sends the question to representation
    geometry instead.

    Read-only: the audit tap sits beside the mixer, never inside it (see _fwd_trunk), so the
    decode the gates run on is bit-for-bit what it was without this call.

    ⚠️ device: the router logits come out of _conv1d (cuBLAS dgemm on GPU), so like every other
    hidden-reading probe this is device-sensitive at ~1e-14 (convergence decode-py-4). Compare
    routes only across runs that fired on the SAME device — the caller stamps it."""
    ta = tok if hasattr(tok, "astype") else np.array(tok, dtype=np.float64)
    routes = {}
    _fwd_trunk(W, ta, T, routes=routes)
    return routes


def clm_forward_logits_edited(W, tok, T, edits):
    """H_9331 BIND-LOCUS · CAUSAL side — full production forward (readout + E1 slot included)
    with `edits` applied inside the trunk. Returns logits:[T, V], host numpy.

    This is the decisive instrument: it does not ask "can a probe read the polarity", it
    asks "does the operator's answer MOVE when we write the polarity into the site the
    operator reads". edits=[] is byte-identical to _fwd_logits (the sham arm)."""
    ta = tok if hasattr(tok, "astype") else np.array(tok, dtype=np.float64)
    return _fwd_logits(W, ta, T, edits=edits)


def clm_penult_pooled_W(W, seed):
    """H_9257 lane-23b · py 2-production twin of core/decode.hexa clm_penult_pooled_W. The mounted
    303M's REAL penultimate (pre-readout, pre-slot) pooled rep for `seed`: right-align the last-24
    bytes into the T-window (_seed_to_tok, IDENTICAL to the decode window fill), run the pure-trunk
    forward (clm_forward_hidden = _fwd_trunk, byte-parity with the hexa penult), then MEAN-POOL the
    yn:[T,d] over the T positions → pooled:[d]. Read-only; NO readout / sampling / perturbation."""
    T = 24
    tok = _seed_to_tok(seed, T)
    yn = clm_forward_hidden(W, tok, T)            # [T, d] pre-readout, pre-slot penultimate
    d = W["d"]
    pooled = [0.0] * d
    c = 0
    while c < d:
        s = 0.0
        t = 0
        while t < T:
            s = s + float(yn[t, c])
            t = t + 1
        pooled[c] = s / float(T)
        c = c + 1
    return pooled


def penult_fold8(pooled):
    """H_9257 FROZEN axis reducer (py twin of core/decode.hexa penult_fold8). Sum |pooled[c]| over
    8 CONTIGUOUS buckets of width d//8 → argmax bucket ∈ [0,8). FROZEN: bucket boundaries + abs-sum
    + argmax fixed by the H_9257 pre-registration (no tune-to-green). Remainder → last bucket."""
    d = len(pooled)
    if d <= 0:
        return 0
    bw = d // 8
    if bw <= 0:
        return 0
    sums = [0.0] * 8
    c = 0
    while c < d:
        b = c // bw
        if b > 7:
            b = 7
        v = pooled[c]
        sums[b] = sums[b] + (-v if v < 0.0 else v)
        c = c + 1
    best = 0
    bestv = sums[0]
    k = 1
    while k < 8:
        if sums[k] > bestv:
            bestv = sums[k]
            best = k
        k = k + 1
    return best


def clm_forward_hidden_logits(W, tok, T):
    """Read-only combined tap: (yn_trunk:[T,d], logits:[T,V]) in ONE trunk forward — the pre-slot
    penultimate AND the base (lane-OFF) full-forward logits. Avoids a double _fwd_trunk when a caller
    (the CLML lane trainer, H_9235) needs both the lane input (yn) and the base logits (CE target).
    Always returns host numpy (to_host) — callers are training-side probes expecting numpy."""
    ta = tok if hasattr(tok, "astype") else np.array(tok, dtype=np.float64)
    yn = _fwd_trunk(W, ta, T)
    d = W["d"]; V = W["V"]; x = yn
    xp = get_xp(x)
    if W.get("slw") is not None:
        # slot_apply (core/slw.py) is host-numpy-only (rare SLW ablation lane) —
        # round-trip through host so the common no-SLW path stays device-resident.
        from slw import slot_apply
        x_h = to_host(x)
        x_h = slot_apply(x_h, W["slw"], gamma=_SLW_GAMMA_OVERRIDE,
                       shuffle_perm=(None if _SLW_SHUFFLE_SEED is None
                                     else np.random.RandomState(_SLW_SHUFFLE_SEED).permutation(W["slw"]["n_slot"])))
        x = to_device(x_h) if xp is not np else x_h
    if W.get("bind_type", 0) != 0:
        u = x @ W["WaWt"] + W["WaB"]; v = x @ W["WbWt"] + W["WbB"]
        g = u * v if W["bind_type"] == 1 else u + v
        logits = g @ W["roWt"] + W["roB"]
    else:
        logits = _conv1d(x, W["roWt"], W["roB"], T, d, V, 1, 1, xp)
    return to_host(yn), to_host(logits)


def _seed_to_tok(seed, T):
    """T-window right-aligned byte encoding (1:1 with the decode seed→tok in
    clm_decode_topk_sampled_W): utf-8 surrogateescape bytes, right-aligned into a
    length-T window, left-pad = 32.0 (space). Shared by the hidden-dump probe."""
    seed_b = seed.encode('utf-8', 'surrogateescape')
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    return tok


def _fwd_logits(W, tok, T, edits=None, mbnd_last=False, ifan_fork=None):
    """_clmd_fwd_logits_sc (host path) — full CLMConvMoE forward. tok:[T] ids.
    Returns logits:[T, V] as host numpy (to_host at the exit) — the SOLE
    device->host sync for a full-forward call when GPU-resident (see
    _fwd_trunk/_conv1d): the trunk + expert convs + MoE router run entirely
    on-device, only the final logits (and the rare SLW/CLML side-lanes) cross
    back to host.

    edits (H_9331 BIND-LOCUS, default None ⇒ byte-identical) — causal interventions
    applied INSIDE the trunk (see _apply_edits); the edited residual then flows through
    the SAME MoE / final-GN / slot / readout ops, so what we measure is what production
    would decode (`a_experiment_engine_native`)."""
    d = W["d"]; V = W["V"]
    # H_9720-ⓐ fresh query lane: when the CLMS trailer is lane_type 5 and a store is live, capture the
    # early-layer (fresh_L) activation in ONE pass (single host-copy, not all L layers) to feed the
    # disjoint address query. tap_depth=None for every other lane ⇒ _fwd_trunk byte-identical.
    _fresh_tap = None
    _fresh_penult = False       # H_9720 C1: fresh_L==0 ⇒ the fresh head reads the penult (yn_trunk), not an
                                # early tap — matches model.py (pen_fresh=pen_trunk when fresh_L==0). NB fresh_L==0
                                # is NOT the embedding tap (_fwd_trunk's tap_depth==0 would capture the embed);
                                # for penult we skip the tap entirely and hand yn_trunk to store_apply below.
    _clms_w = W.get("clms")
    if _clms_w is not None and int(_clms_w.get("lane_type", 0)) == 5 and _CLMS_STORE is not None:
        if int(_clms_w["fresh_L"]) > 0:
            _fresh_tap = {}
        else:
            _fresh_penult = True
    # H_9803 IFAN branch-latent fan: the proposal latents read the PRESERVED early (route_L) tap.
    # _fwd_trunk exposes ONE tap slot, so when the CLMS fresh lane already owns it at a DIFFERENT
    # depth the fan falls back to the penultimate (`tap=None` ⇒ ifan_apply reads yn = the `penult`
    # route). Reported honestly rather than silently mixing depths.
    _ifan_w = W.get("ifan")
    _ifan_on = (_ifan_w is not None and _IFAN_MODE != "off")
    _ifan_tap = None
    _tap_depth = int(_clms_w["fresh_L"]) if _fresh_tap is not None else None
    _tap_out = _fresh_tap
    if _ifan_on and int(_ifan_w.get("route_L", 0)) > 0:
        if _tap_depth is None:
            _tap_depth = int(_ifan_w["route_L"]); _ifan_tap = {}; _tap_out = _ifan_tap
        elif _tap_depth == int(_ifan_w["route_L"]):
            _ifan_tap = _fresh_tap                # same depth ⇒ one tap serves both lanes
    yn = _fwd_trunk(W, tok, T, edits=edits,       # [T, d] pre-readout, pre-slot penultimate (device-resident if GPU)
                    tap_depth=_tap_depth, tap_out=_tap_out)
    yn_trunk = yn                                 # keep pre-slot trunk penultimate for the CLML read-side lane
    xp = get_xp(yn)
    # H_9200 E1 — gated-write forward-slot on the post-norm penultimate (before
    # readout), byte-parity with the torch SLWModule + core/decode.hexa. None =>
    # additive golden path untouched. The eval-time controls are process-global
    # (set by cli/evaluate.py set_slw_controls): _SLW_GAMMA_OVERRIDE (--slot-off γ=0
    # ablation) and _SLW_SHUFFLE_SEED (--slot-shuffle: a fixed permutation of the
    # WRITE address only, reads unpermuted, breaks role→slot correspondence).
    if W.get("slw") is not None:
        # slot_apply (core/slw.py) is host-numpy-only (rare SLW ablation lane) —
        # round-trip through host so the common no-SLW path (the profiled hot
        # path) stays fully device-resident with no extra transfer.
        from slw import slot_apply
        perm = None
        if _SLW_SHUFFLE_SEED is not None:
            perm = np.random.RandomState(_SLW_SHUFFLE_SEED).permutation(W["slw"]["n_slot"])
        yn_h = to_host(yn)
        yn_h = slot_apply(yn_h, W["slw"], gamma=_SLW_GAMMA_OVERRIDE, shuffle_perm=perm)
        yn = to_device(yn_h) if xp is not np else yn_h
    # readout: additive Conv1d (standard) OR Hadamard/linear bind (CLMB)
    if W.get("bind_type", 0) != 0:
        # CLMB bind readout: yn → (Wa,Wb) linear projections → Hadamard/+ → Wo
        # WaWt=(d,k), WbWt=(d,k); roWt=(k,V) holds Wo.T; roB=(V,) holds WoB.
        u = yn @ W["WaWt"] + W["WaB"]             # [T, k]
        v = yn @ W["WbWt"] + W["WbB"]             # [T, k]
        g = u * v if W["bind_type"] == 1 else u + v   # Hadamard(1) or linear(2)
        out_logits = g @ W["roWt"] + W["roB"]     # [T, V]  roWt=(k,V)
    else:
        out_logits = _conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1, xp)  # [T, V]
    # fork-A CLML read-side context-pooling lane (H_9235) — reads the pre-slot trunk
    # penultimate, causal-mean-pools the full context, adds a gated tether-clipped logit
    # bias. None/absent => passthrough (byte-identical). DISJOINT (read-only + additive bias).
    if W.get("clml") is not None:
        # lane_apply (core/clml.py) is host-numpy-only — round-trip through host
        # (rare lane, same pattern as SLW above). Fall through to the CLMS lane (no early return):
        # the fixed post-readout order is SLW → readout → CLML(additive) → CLMS(overwrite).
        from clml import lane_apply
        out_logits = lane_apply(to_host(yn_trunk), to_host(out_logits), W["clml"])
    # H_9423 CLMS store-bridge lane — OVERWRITE the answer-position logits row with λ·store_logits
    # (store_only gate: the overwrite erases even CLML's additive delta at that row, so no trunk-lineage
    # logit survives = ② shortcut-cut). Trailer absent OR store un-injected => passthrough (byte-identical,
    # C0-f seal). Query tap = yn_trunk (pre-slot), the SAME tap CLML reads. host-numpy-only (rare lane).
    if W.get("clms") is not None and _CLMS_STORE is not None:
        from clms import store_apply, find_qpos
        qpos = find_qpos(tok)
        # H_9695: the qpos guard is correct for query="qpos" (no marker ⇒ nothing to overwrite),
        # but it would ALSO silence query="every-token" — free ideation never contains "=> ", so
        # find_qpos is empty there BY CONSTRUCTION and the marker-free lane would never fire.
        if qpos or _CLMS_QUERY == "every-token":
            out_logits = store_apply(to_host(out_logits), to_host(yn_trunk), W["clms"],
                                     _CLMS_STORE, qpos, oracle=_CLMS_ORACLE,
                                     lam_override=_CLMS_LAM_OVERRIDE, audit=_CLMS_AUDIT,
                                     query=_CLMS_QUERY, fuse=_CLMS_FUSE,
                                     fresh_yn=(_fresh_tap["x"] if _fresh_tap is not None
                                               else (to_host(yn_trunk) if _fresh_penult else None)))
    # H_9698 MOUTH-BINDER — additive, AFTER CLMS so the documented post-readout order stays
    # SLW → readout → CLML(additive) → CLMS → MBND(additive). Opt-in: trailer present + switch off
    # ⇒ byte-identical (a_substrate_disjoint: the two lanes never read each other).
    if W.get("mbnd") is not None and _MBND_ON:
        from mbnd import mbnd_apply
        out_logits = mbnd_apply(to_host(out_logits), to_host(yn_trunk), W["mbnd"],
                                order_scramble=_MBND_ORDER_SCRAMBLE, last_only=mbnd_last)
    # H_9803 BRANCH-LATENT IDEATION FAN — additive, LAST in the chain
    # (SLW → readout → CLML → CLMS → MBND → IFAN). Opt-in: `_IFAN_MODE == "off"` (the default)
    # makes ifan_apply return the caller's object untouched, so an IFAN-carrying .clm decodes
    # byte-identically to the base — that is the `--fan-branch off` parity arm's whole claim.
    if _ifan_on:
        from ifan import ifan_apply
        out_logits = ifan_apply(to_host(out_logits), to_host(yn_trunk),
                                (to_host(_ifan_tap["x"]) if _ifan_tap is not None else None),
                                W["ifan"], branch=_IFAN_BRANCH, mode=_IFAN_MODE,
                                perm_seed=_IFAN_PERM_SEED, last_only=mbnd_last,
                                fork=ifan_fork)
    return to_host(out_logits)


# ── public CLM decode/CE entries — 1:1 from clm_decode.hexa ──

def clm_forward_ce(path, corpus, nwin_max):
    """clm_decode.hexa::clm_forward_ce — mean CE over nwin_max T=24 causal
    windows; uniform_ce = dt_ln(V); green = model_ce < uniform AND < shuffle."""
    if not clm_decodable(path):
        return {"ok": False, "reason": "not v0.2-decodable", "green": False,
                "model_ce": 0.0, "shuffle_ce": 0.0, "uniform_ce": 0.0, "windows": 0}
    W = clm_load_weights(path)
    d = W["d"]; E = W["E"]; V = W["V"]; K = W["K"]
    bytes_arr = np.frombuffer(open(corpus, 'rb').read(), dtype=np.uint8)
    n_bytes = len(bytes_arr)
    T = 24
    stride = (n_bytes - T - 1) // nwin_max
    if stride < 1:
        stride = 1
    sum_model = 0.0; sum_shuf = 0.0; nwin = 0
    for s in range(nwin_max):
        base = s * stride
        if base + T + 1 <= n_bytes:
            tok = bytes_arr[base:base + T].astype(np.float64)
            tgt = bytes_arr[base + 1:base + T + 1].astype(np.float64)
            logits = _fwd_logits(W, tok, T)
            ce = nn_ce_loss_allpos(logits, tgt, T, V)
            sum_model += ce
            tgt_sh = tgt[::-1]
            sum_shuf += nn_ce_loss_allpos(logits, tgt_sh, T, V)
            nwin += 1
    model_ce = sum_model / float(nwin)
    shuf_ce = sum_shuf / float(nwin)
    uniform_ce = float(dt_ln(np.array(float(V))))
    lt_u = model_ce < uniform_ce
    lt_s = model_ce < shuf_ce
    return {"ok": True, "windows": nwin, "d": d, "E": E, "V": V, "K": K, "L": W["L"],
            "model_ce": model_ce, "shuffle_ce": shuf_ce, "uniform_ce": uniform_ce,
            "lt_uniform": lt_u, "lt_shuffle": lt_s, "green": lt_u and lt_s}


def clm_decode_argmax(path, seed, gen):
    """clm_decode.hexa::clm_decode_argmax — greedy continuation. T=24 window,
    right-aligned seed (pad-left byte 32). argmax ties: first (strict >)."""
    if not clm_decodable(path):
        return {"ok": False, "text": ""}
    W = clm_load_weights(path)
    V = W["V"]
    T = 24
    seed_b = seed.encode('utf-8', 'surrogateescape')
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    for _i in range(gen):
        logits = _fwd_logits(W, tok, T, mbnd_last=True,   # H_9698 perf: gen reads only last row
                             ifan_fork=max(0, T - 1 - _i))   # H_9803 fork slides with the window
        row = logits[T - 1]
        besti = 0
        bestv = row[0]
        for k in range(1, V):
            if row[k] > bestv:
                bestv = row[k]; besti = k
        out.append(besti)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(besti)
    return {"ok": True, "text": out.decode('utf-8', 'surrogateescape')}


def clm_decode_topk_sampled(path, seed, gen, top_k, temp, seed_rng):
    """clm_decode.hexa::clm_decode_topk_sampled — seeded top-k temperature draw."""
    if not clm_decodable(path):
        return {"ok": False, "text": ""}
    W = clm_load_weights(path)
    return clm_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)


def clm_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng):
    V = W["V"]
    T = 24 if _CONSULT_DECODE_T is None else int(_CONSULT_DECODE_T)   # H_9407 consult-decode window (None=prod 24)
    seed_b = seed.encode('utf-8', 'surrogateescape')
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    rng = _mix32(seed_rng)
    for _i in range(gen):
        # H_9803 fork index: the LAST SEED byte starts at T-1 and slides left one place per emitted
        # byte (fixed-T window). Clamped at 0 once the seed has scrolled out — after that the branch
        # latent is grounded on the oldest position still in the window, which is honest (the fork
        # context is genuinely gone) rather than silently re-grounding on generated text.
        logits = _fwd_logits(W, tok, T, mbnd_last=True,   # H_9698 perf: gen reads only last row
                             ifan_fork=max(0, T - 1 - _i))
        nb, rng = _topk_sample(logits[T - 1], V, top_k, temp, rng)
        out.append(nb)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(nb)
    return {"ok": True, "text": out.decode('utf-8', 'surrogateescape')}


# ════════════════════════════════════════════════════════════════════════
# (c) BYTE (ByteGPT transformer) — verbatim port of core/decode.hexa
#     (formerly core/bytegpt_decode.py) + byte-exact KV-cache fast path.
# ════════════════════════════════════════════════════════════════════════

# libm erf, vectorized elementwise (object-ufunc -> float64). The hexa GELU calls
# `extern fn erf` (the C libm scalar erf), so math.erf is the byte-faithful twin.
_erf_vec = np.frompyfunc(math.erf, 1, 1)


def dt_sqrt(x):
    """flame_math.hexa::dt_sqrt — Newton-Raphson 24 iters from g0=max(x,1).
    Scalar. (DIVERGENT twin of clm's _gn_sqrt: 40 iters from g0=x — kept distinct.)"""
    if x <= 0.0:
        return 0.0
    g = x if x > 1.0 else 1.0
    i = 0
    while i < 24:
        g = 0.5 * (g + x / g)
        i = i + 1
    return g


def _bg_gelu(x):
    """decode.hexa::_bg_gelu — 0.5*x*(1+erf(x*0.7071067811865476)).
    erf via libm (math.erf), NOT the dt_erf twin (ING#23 torch-parity)."""
    x = np.asarray(x, dtype=np.float64)
    e = _erf_vec(x * 0.7071067811865476).astype(np.float64)
    return 0.5 * x * (1.0 + e)


def _bg_layernorm_rows(X, g, b, T, d):
    """decode.hexa::_bg_layernorm — per-row LayerNorm over length d.
    biased variance, eps=1e-5, inv = 1/dt_sqrt(var+eps). X:[T,d]. Returns Y:[T,d].
    dt_sqrt is scalar per row (matching the hexa scalar while-loop)."""
    eps = 0.00001
    X = X.reshape(T, d)
    Y = np.empty_like(X)
    for i in range(T):
        row = X[i]
        mean = row.sum() / float(d)
        dv = row - mean
        var = (dv * dv).sum() / float(d)
        inv = 1.0 / dt_sqrt(var + eps)
        Y[i] = g * (dv * inv) + b
    return Y


# ── .bin header + weight load — 1:1 from decode.hexa _bg_rd_u32 / bg_load ──

# _bg_rd_u32 ≡ clm's _rd_u32 (byte-identical). Aliased to the single SHARED def.
_bg_rd_u32 = _rd_u32


def bg_header(path):
    """parse the 5xu32 header [vocab,d,n_layer,n_head,block]. Returns dict."""
    with open(path, 'rb') as f:
        hdr = f.read(20)
    if len(hdr) < 20:
        return {"ok": False}
    vocab = _bg_rd_u32(hdr, 0)
    d = _bg_rd_u32(hdr, 4)
    nlay = _bg_rd_u32(hdr, 8)
    nh = _bg_rd_u32(hdr, 12)
    block = _bg_rd_u32(hdr, 16)
    return {"ok": True, "vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block}


def bg_is_bytegpt(path):
    """mouth-sniff: NOT CLM\\x01 magic AND a sane 5xu32 ByteGPT header.
    Mirrors generator.hexa gen_auto_ideate dispatch (CLM\\x01 -> clm, else bytegpt)."""
    try:
        with open(path, 'rb') as f:
            hdr = f.read(20)
    except Exception:
        return False
    if len(hdr) < 20:
        return False
    # CLM\x01 magic => ConvMoE, not ByteGPT
    if hdr[0] == 67 and hdr[1] == 76 and hdr[2] == 77 and hdr[3] == 1:
        return False
    vocab = _bg_rd_u32(hdr, 0)
    d = _bg_rd_u32(hdr, 4)
    nlay = _bg_rd_u32(hdr, 8)
    nh = _bg_rd_u32(hdr, 12)
    block = _bg_rd_u32(hdr, 16)
    # sane ranges + d divisible by n_head (GPT invariant)
    if not (1 <= vocab <= 1 << 20 and 1 <= d <= 1 << 16 and 1 <= nlay <= 1024
            and 1 <= nh <= 1024 and 1 <= block <= 1 << 20):
        return False
    if d % nh != 0:
        return False
    return True


def _rd_f32(rb, off, n):
    """read n LE f32 from byte buffer at byte offset off -> float64 array[n]."""
    return np.frombuffer(rb, dtype='<f4', count=n, offset=off).astype(np.float64)


def _bg_read_bind_block(rb, off, d):
    """Read ONE BGB injected-bind block from the flat trailer at byte offset off.
    Layout = a base ByteGPT layer's 12 param tensors in bg_load order (LE f32),
    then one LE f32 scalar `gate`. Returns (block_dict, new_off).
    (Shapes match bg_load's per-layer read exactly — reference-matched, no reorder.)"""
    blk = {}
    blk["ln1w"] = _rd_f32(rb, off, d); off += d * 4
    blk["ln1b"] = _rd_f32(rb, off, d); off += d * 4
    blk["inW"] = _rd_f32(rb, off, 3 * d * d).reshape(3 * d, d); off += 3 * d * d * 4
    blk["inB"] = _rd_f32(rb, off, 3 * d); off += 3 * d * 4
    blk["oW"] = _rd_f32(rb, off, d * d).reshape(d, d); off += d * d * 4
    blk["oB"] = _rd_f32(rb, off, d); off += d * 4
    blk["ln2w"] = _rd_f32(rb, off, d); off += d * 4
    blk["ln2b"] = _rd_f32(rb, off, d); off += d * 4
    blk["m0W"] = _rd_f32(rb, off, 4 * d * d).reshape(4 * d, d); off += 4 * d * d * 4
    blk["m0B"] = _rd_f32(rb, off, 4 * d); off += 4 * d * 4
    blk["m2W"] = _rd_f32(rb, off, d * 4 * d).reshape(d, 4 * d); off += d * 4 * d * 4
    blk["m2B"] = _rd_f32(rb, off, d); off += d * 4
    blk["gate"] = float(_rd_f32(rb, off, 1)[0]); off += 4
    return blk, off


def bg_load(path):
    """decode.hexa::bg_load — parse the flat binary ONCE into a weight dict.
    Weight binary layout (LE f32, decode.hexa:29-36):
      [vocab,d,n_layer,n_head,block]  5xu32
      tok[vocab*d]  pos[block*d]
      per layer: ln1.w[d] ln1.b[d] in_proj.w[3d*d] in_proj.b[3d]
                 out_proj.w[d*d] out_proj.b[d] ln2.w[d] ln2.b[d]
                 mlp0.w[4d*d] mlp0.b[4d] mlp2.w[d*4d] mlp2.b[d]
      ln_f.w[d] ln_f.b[d]  head[vocab*d]
    (torch Linear stores W as [out,in] row-major; y = x.Wt + b.)"""
    _k = _wload_key(path)
    if _k is not None and _k in _WLOAD_CACHE:
        return _WLOAD_CACHE[_k]
    rb = open(path, 'rb').read()
    vocab = _bg_rd_u32(rb, 0)
    d = _bg_rd_u32(rb, 4)
    nlay = _bg_rd_u32(rb, 8)
    nh = _bg_rd_u32(rb, 12)
    block = _bg_rd_u32(rb, 16)
    off = 20

    tok = _rd_f32(rb, off, vocab * d).reshape(vocab, d); off += vocab * d * 4
    pos = _rd_f32(rb, off, block * d).reshape(block, d); off += block * d * 4

    ln1w = []; ln1b = []; inW = []; inB = []
    oW = []; oB = []; ln2w = []; ln2b = []
    m0W = []; m0B = []; m2W = []; m2B = []
    for _ in range(nlay):
        ln1w.append(_rd_f32(rb, off, d)); off += d * 4
        ln1b.append(_rd_f32(rb, off, d)); off += d * 4
        inW.append(_rd_f32(rb, off, 3 * d * d).reshape(3 * d, d)); off += 3 * d * d * 4
        inB.append(_rd_f32(rb, off, 3 * d)); off += 3 * d * 4
        oW.append(_rd_f32(rb, off, d * d).reshape(d, d)); off += d * d * 4
        oB.append(_rd_f32(rb, off, d)); off += d * 4
        ln2w.append(_rd_f32(rb, off, d)); off += d * 4
        ln2b.append(_rd_f32(rb, off, d)); off += d * 4
        m0W.append(_rd_f32(rb, off, 4 * d * d).reshape(4 * d, d)); off += 4 * d * d * 4
        m0B.append(_rd_f32(rb, off, 4 * d)); off += 4 * d * 4
        m2W.append(_rd_f32(rb, off, d * 4 * d).reshape(d, 4 * d)); off += d * 4 * d * 4
        m2B.append(_rd_f32(rb, off, d)); off += d * 4
    lnfw = _rd_f32(rb, off, d); off += d * 4
    lnfb = _rd_f32(rb, off, d); off += d * 4
    head = _rd_f32(rb, off, vocab * d).reshape(vocab, d); off += vocab * d * 4

    # ── optional BGB injected-bind trailer (serialize_bind, H_9027) ──────
    # "BGB\x01" = bytes 66,71,66,1, appended AFTER `head`. Carries n_bind appended
    # GATED transformer blocks (each = a standard base layer: the SAME 12 param
    # tensors in the SAME order/layout as above, then one LE f32 gate). Applied
    # after the L base blocks and BEFORE ln_f (mirrors the CLM "CLMB" bind-trailer
    # precedent). ABSENT trailer => bind=[] => forward BYTE-IDENTICAL to plain ByteGPT.
    bind = []
    if (off + 8 <= len(rb)
            and rb[off] == 66 and rb[off + 1] == 71
            and rb[off + 2] == 66 and rb[off + 3] == 1):
        off += 4                                          # skip "BGB\x01"
        n_bind = _bg_rd_u32(rb, off); off += 4
        for _ in range(n_bind):
            blk, off = _bg_read_bind_block(rb, off, d)
            bind.append(blk)

    W = {"ok": True, "vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block,
         "tok": tok, "pos": pos, "ln1w": ln1w, "ln1b": ln1b,
         "inW": inW, "inB": inB, "oW": oW, "oB": oB,
         "ln2w": ln2w, "ln2b": ln2b, "m0W": m0W, "m0B": m0B,
         "m2W": m2W, "m2B": m2B, "lnfw": lnfw, "lnfb": lnfb, "head": head,
         "bind": bind}
    if _k is not None:
        _WLOAD_CACHE[_k] = W
    return W


# bg_load_ranged — byte-identical W-map to bg_load (hexa builds it via ranged
# read_bytes_at to dodge the whole-file boxing OOM; the resulting weights are the
# same, and the py read already mmaps lazily via frombuffer). Aliased for surface
# parity with the hexa public entries (decode.hexa:782).
bg_load_ranged = bg_load


# ── forward — 1:1 from decode.hexa _bg_mha / _bg_linear / bg_forward_last_W ──

def _bg_mha(H, inW, inB, oW, oB, T, d, nh):
    """decode.hexa::_bg_mha — torch nn.MultiheadAttention semantics.
    H:[T,d] pre-normed. in_proj W[3d,d] rows Q|K|V; out_proj W[d,d]+b.
    scale=1/dt_sqrt(hd), causal, libm exp softmax. Returns Aout:[T,d]."""
    hd = d // nh
    scale = 1.0 / dt_sqrt(float(hd))
    # QKV = H[T,d] @ inW.T[d,3d] + inB  -> packed [T,3d]; Q=cols0..d, K=d..2d, V=2d..3d
    QKV = H @ inW.T + inB                                  # [T, 3d]
    Q = QKV[:, 0:d]; K = QKV[:, d:2 * d]; V = QKV[:, 2 * d:3 * d]
    ctx = np.zeros((T, d), dtype=np.float64)
    for hh in range(nh):
        base = hh * hd
        Qh = Q[:, base:base + hd]; Kh = K[:, base:base + hd]; Vh = V[:, base:base + hd]
        for i in range(T):
            L = i + 1
            # scores over keys 0..i, scaled
            sc = (Qh[i] @ Kh[0:L].T) * scale                # [L]
            mx = sc.max()
            e = np.exp(sc - mx)                             # libm-equivalent
            tot = e.sum()
            ctx[i, base:base + hd] = (e / tot) @ Vh[0:L]    # [hd]
    # out proj: Aout = ctx @ oW.T + oB
    return ctx @ oW.T + oB


def _bg_apply_bind(x, bind, T, d, nh):
    """Apply N appended GATED transformer blocks to the full post-base sequence
    x:[T,d], AFTER the L base blocks and BEFORE ln_f. Each block is a STANDARD
    transformer block (reuses _bg_layernorm_rows / _bg_mha / _bg_gelu — the exact
    base-layer ops) plus a scalar gate:
        block(x) = x + mha(ln1(x)) + mlp(ln2(x + mha(ln1(x))))
        x        = x + gate * (block(x) - x)          # gate=0 => identity (exact)
    Mirrors BindAttnByteGPT.forward `x = x + gate*(bind(x)-x)`. Returns x:[T,d]."""
    for blk in bind:
        nrm = _bg_layernorm_rows(x, blk["ln1w"], blk["ln1b"], T, d)
        aout = _bg_mha(nrm, blk["inW"], blk["inB"], blk["oW"], blk["oB"], T, d, nh)
        xa = x + aout                                      # x + mha(ln1(x))
        nrm2 = _bg_layernorm_rows(xa, blk["ln2w"], blk["ln2b"], T, d)
        h4 = _bg_gelu(nrm2 @ blk["m0W"].T + blk["m0B"])    # [T, 4d]
        mlpo = h4 @ blk["m2W"].T + blk["m2B"]              # [T, d]
        blk_out = xa + mlpo                                # = block(x)
        x = x + blk["gate"] * (blk_out - x)                # gate=0 => x unchanged
    return x


def bg_forward_last_W(W, ids, T):
    """decode.hexa::bg_forward_last_W — full forward from a loaded weight
    dict; returns last-position next-byte logits float64[vocab]. ids:[T] int.
    When W["bind"] is non-empty the appended gated blocks run after the L base
    blocks and before ln_f (H_9027); absent/empty => byte-identical to before."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]; vocab = W["vocab"]
    ids = np.asarray(ids, dtype=np.int64)
    # x[T,d] = tok[id] + pos[t]
    x = W["tok"][ids] + W["pos"][0:T]                       # [T, d]
    for Lr in range(nlay):
        # attn sub-block: x = x + MHA(LN1(x))
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        aout = _bg_mha(nrm, W["inW"][Lr], W["inB"][Lr], W["oW"][Lr], W["oB"][Lr], T, d, nh)
        x = x + aout
        # mlp sub-block: x = x + Wd(GELU(W0(LN2(x))))
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = nrm @ W["m0W"][Lr].T + W["m0B"][Lr]            # [T, 4d]
        h4 = _bg_gelu(h4)
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]           # [T, d]
        x = x + mlpo
    # appended injected-bind blocks (H_9027) — after base stack, before ln_f
    if W.get("bind"):
        x = _bg_apply_bind(x, W["bind"], T, d, nh)
    # final LayerNorm on the LAST position only, then tied head
    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]   # [d]
    logits = W["head"] @ lastrow                            # [vocab]
    return logits


def bg_forward_last_hidden(W, ids, T):
    """H_9129 L5 rung-3 — same full forward as bg_forward_last_W but returns the
    final-LN LAST-position hidden state float64[d] (the pre-head representation),
    NOT the tied-head logits. The hippocampal associative store (core/hippo_assoc)
    keys on this hidden, not on logits (design: reps = final-LN hidden). Byte-shares
    the forward body with bg_forward_last_W; the only difference is the return line
    (head @ lastrow omitted). ids:[T] int; W["bind"] handled identically (H_9027)."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    ids = np.asarray(ids, dtype=np.int64)
    x = W["tok"][ids] + W["pos"][0:T]                       # [T, d]
    for Lr in range(nlay):
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        aout = _bg_mha(nrm, W["inW"][Lr], W["inB"][Lr], W["oW"][Lr], W["oB"][Lr], T, d, nh)
        x = x + aout
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = _bg_gelu(nrm @ W["m0W"][Lr].T + W["m0B"][Lr])  # [T, 4d]
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]           # [T, d]
        x = x + mlpo
    if W.get("bind"):
        x = _bg_apply_bind(x, W["bind"], T, d, nh)
    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]   # [d]
    return lastrow                                          # final-LN last-pos hidden


def bytegpt_forward_last(path, ids, T):
    """decode.hexa::bytegpt_forward_last — load + forward (parity probe)."""
    W = bg_load(path)
    return bg_forward_last_W(W, ids, T)


def bg_argmax(a):
    """decode.hexa::bg_argmax — index of max (ties: first, strict >)."""
    bi = 0
    bv = a[0]
    for k in range(1, len(a)):
        if a[k] > bv:
            bv = a[k]; bi = k
    return bi


def _seed_to_ids(seed):
    """string|bytes|list -> list[int] byte ids."""
    if isinstance(seed, (list, tuple)):
        return [int(x) for x in seed]
    if isinstance(seed, str):
        seed = seed.encode('utf-8', 'surrogateescape')
    return list(seed)


# ── KV-cache fast path — NEW (byte-exact TOKEN stream vs full-forward) ───────
#
# The full-forward loop re-forwards ALL T window tokens every decode step
# (O(gen²)). The KV path caches per-layer (K,V) = the in_proj K,V slices from
# _bg_mha and, on each new token, forwards ONLY the new position, attending it
# against the cached K,V of all layers. This mirrors the hexa KV-cache
# (decode.hexa:919, proven byte-identical to full-forward there).
#
# WINDOW-SLIDE RESYNC: ByteGPT indexes the positional embedding by position
# WITHIN the window (pos[0:T]), not by absolute token index. While the window is
# still GROWING (n <= block, start=0) every cached position keeps its window
# index → K,V stay valid → cheap incremental append. Once the window SLIDES
# (n > block, start>0) every token's window position shifts by one → its pos
# embedding (hence K,V) changes → the cache is INVALID and is fully REBUILT at
# M=T (byte-identical to full-forward for that window). So sliding steps cost a
# full forward (correct, not faster); the speedup is the growing-window regime,
# which is the entire eval decode path (seed+gen << block=512 for the 303M).

def _bg_forward_build(W, ids, T):
    """Full-forward over the window (== bg_forward_last_W) that ALSO captures the
    per-layer (K,V) in_proj slices for every position. Returns (logits, cache)
    where cache[Lr] = [K[T,d], V[T,d]]. The last-position logits are byte-
    identical to bg_forward_last_W (same ops, M=T batched)."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    ids = np.asarray(ids, dtype=np.int64)
    x = W["tok"][ids] + W["pos"][0:T]                       # [T, d]
    hd = d // nh
    scale = 1.0 / dt_sqrt(float(hd))
    cache = []
    for Lr in range(nlay):
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        QKV = nrm @ W["inW"][Lr].T + W["inB"][Lr]          # [T, 3d]
        Q = QKV[:, 0:d]; K = QKV[:, d:2 * d]; V = QKV[:, 2 * d:3 * d]
        ctx = np.zeros((T, d), dtype=np.float64)
        for hh in range(nh):
            base = hh * hd
            Qh = Q[:, base:base + hd]; Kh = K[:, base:base + hd]; Vh = V[:, base:base + hd]
            for i in range(T):
                L = i + 1
                sc = (Qh[i] @ Kh[0:L].T) * scale
                mx = sc.max()
                e = np.exp(sc - mx)
                tot = e.sum()
                ctx[i, base:base + hd] = (e / tot) @ Vh[0:L]
        aout = ctx @ W["oW"][Lr].T + W["oB"][Lr]
        x = x + aout
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = nrm @ W["m0W"][Lr].T + W["m0B"][Lr]
        h4 = _bg_gelu(h4)
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]
        x = x + mlpo
        cache.append([K.copy(), V.copy()])
    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]
    logits = W["head"] @ lastrow
    return logits, cache


def _bg_kv_step(W, cache, id_new, win_pos):
    """Forward ONLY the new position (window index win_pos, byte id id_new),
    attending against + appending to the per-layer K,V cache. Returns the new
    position's next-byte logits. cache[Lr]=[K,V] is grown in place by one row.
    Reuses the EXACT _bg_mha attention ops (same scale, libm exp softmax, same
    per-output accumulation order) so the token stream matches full-forward."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    hd = d // nh
    scale = 1.0 / dt_sqrt(float(hd))
    x = (W["tok"][int(id_new)] + W["pos"][win_pos]).astype(np.float64).reshape(1, d)
    for Lr in range(nlay):
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], 1, d)       # [1,d]
        qkv = nrm @ W["inW"][Lr].T + W["inB"][Lr]                             # [1,3d]
        qn = qkv[:, 0:d]; kn = qkv[:, d:2 * d]; vn = qkv[:, 2 * d:3 * d]      # [1,d]
        Kc = np.concatenate([cache[Lr][0], kn], axis=0)                       # [T,d]
        Vc = np.concatenate([cache[Lr][1], vn], axis=0)
        cache[Lr][0] = Kc; cache[Lr][1] = Vc
        ctx = np.zeros((1, d), dtype=np.float64)
        for hh in range(nh):
            base = hh * hd
            qh = qn[0, base:base + hd]              # [hd]
            Kh = Kc[:, base:base + hd]              # [T,hd]
            Vh = Vc[:, base:base + hd]              # [T,hd]
            sc = (qh @ Kh.T) * scale                # [T]
            mx = sc.max()
            e = np.exp(sc - mx)
            tot = e.sum()
            ctx[0, base:base + hd] = (e / tot) @ Vh
        aout = ctx @ W["oW"][Lr].T + W["oB"][Lr]                              # [1,d]
        x = x + aout
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], 1, d)
        h4 = nrm @ W["m0W"][Lr].T + W["m0B"][Lr]
        h4 = _bg_gelu(h4)
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]
        x = x + mlpo
    lastrow = _bg_layernorm_rows(x, W["lnfw"], W["lnfb"], 1, d)[0]
    logits = W["head"] @ lastrow
    return logits


def _bg_step_logits(W, toks, st):
    """One decode step's last-position logits via KV cache. `st` is a mutable
    dict {'cache','start'} carried across steps. Builds (M=T) on the first step
    OR whenever the window slides (start changes = pos-embedding re-index); else
    appends the single new token incrementally."""
    block = W["block"]
    n = len(toks)
    start = n - block if n > block else 0
    T = n - start
    # Injected-bind models (H_9027): the appended blocks have their OWN attention
    # over the full post-base sequence, which the incremental KV step can't supply
    # from base-layer K,V alone — so decode via the full-sequence forward (byte-
    # exact vs the torch reference; gate=0 => identical to the base KV stream since
    # the base forward is unchanged and the bind contribution is exactly zero).
    if W.get("bind"):
        return bg_forward_last_W(W, toks[start:start + T], T)
    if st['cache'] is None or start != st['start']:
        logits, cache = _bg_forward_build(W, toks[start:start + T], T)
        st['cache'] = cache; st['start'] = start
        return logits
    # incremental: the new token is at window position T-1 (= toks[start+T-1]).
    return _bg_kv_step(W, st['cache'], toks[start + T - 1], T - 1)


# ── public decode entries — 1:1 from decode.hexa (KV path wired in) ──

def bytegpt_decode_argmax(path, seed_ids, gen):
    """decode.hexa::bytegpt_decode_argmax — greedy continuation, weights
    loaded ONCE, prompt window grown (capped at block). Returns {ok,text,ids}.
    (Decode loop = byte-exact KV cache; full-forward reference = _decode_argmax_W_full.)"""
    W = bg_load(path)
    return _decode_argmax_W(W, seed_ids, gen)


# bytegpt_decode_argmax_ranged — OOM-safe twin (hexa: bg_load_ranged). Same compute.
def bytegpt_decode_argmax_ranged(path, seed_ids, gen):
    W = bg_load_ranged(path)
    return _decode_argmax_W(W, seed_ids, gen)


def _decode_argmax_W(W, seed_ids, gen):
    """KV-cache greedy decode from an already-loaded weight dict. Token stream is
    byte-exact vs _decode_argmax_W_full (the O(gen²) full-forward reference)."""
    toks = _seed_to_ids(seed_ids)
    outl = []
    st = {'cache': None, 'start': None}
    for _ in range(gen):
        logits = _bg_step_logits(W, toks, st)
        nb = bg_argmax(logits)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


def _decode_argmax_W_full(W, seed_ids, gen):
    """ORIGINAL O(gen²) full-forward greedy decode (KV-cache OFF). Retained as the
    byte-exactness reference for the self-test."""
    vocab = W["vocab"]; block = W["block"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    for _ in range(gen):
        n = len(toks)
        start = n - block if n > block else 0
        T = n - start
        ids = toks[start:start + T]
        logits = bg_forward_last_W(W, ids, T)
        nb = bg_argmax(logits)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


def bytegpt_decode_topk_sampled(path, seed_ids, gen, top_k, temp, seed_rng):
    """decode.hexa::bytegpt_decode_topk_sampled — seeded top-k temp draw."""
    W = bg_load(path)
    return bytegpt_decode_topk_sampled_W(W, seed_ids, gen, top_k, temp, seed_rng)


# OOM-safe twin (hexa: bytegpt_decode_topk_sampled_ranged via bg_load_ranged).
def bytegpt_decode_topk_sampled_ranged(path, seed_ids, gen, top_k, temp, seed_rng):
    W = bg_load_ranged(path)
    return bytegpt_decode_topk_sampled_W(W, seed_ids, gen, top_k, temp, seed_rng)


def bytegpt_decode_topk_sampled_W(W, seed_ids, gen, top_k, temp, seed_rng):
    """KV-cache seeded top-k decode from an already-loaded weight dict (== hexa
    _bg_gen_from_W KV branch). seed_ids = string|bytes|list of byte ids. Token
    stream is byte-exact vs bytegpt_decode_topk_sampled_W_full."""
    vocab = W["vocab"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    rng = _mix32(seed_rng)
    st = {'cache': None, 'start': None}
    for _ in range(gen):
        logits = _bg_step_logits(W, toks, st)
        nb, rng = _topk_sample(logits, vocab, top_k, temp, rng)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


def bytegpt_decode_topk_sampled_W_full(W, seed_ids, gen, top_k, temp, seed_rng):
    """ORIGINAL O(gen²) full-forward seeded top-k decode (KV-cache OFF). Retained
    as the byte-exactness reference for the self-test."""
    vocab = W["vocab"]; block = W["block"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    rng = _mix32(seed_rng)
    for _ in range(gen):
        n = len(toks)
        start = n - block if n > block else 0
        T = n - start
        ids = toks[start:start + T]
        logits = bg_forward_last_W(W, ids, T)
        nb, rng = _topk_sample(logits, vocab, top_k, temp, rng)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


# ════════════════════════════════════════════════════════════════════════
# (d) MOUTH DISPATCH — header-sniff (mirrors generator.hexa gen_auto_backend).
#     CLM\x01 magic + CLMX trailer => conv (.clm); sane 5xu32 header => byte (.bin).
# ════════════════════════════════════════════════════════════════════════

def decode_mouth_kind(path):
    """gen_mouth_kind — 'clm' | 'bytegpt' | 'unknown'. clm checked FIRST (its
    CLM\\x01 magic is what bg_is_bytegpt explicitly rejects)."""
    if clm_decodable(path):
        return "clm"
    if bg_is_bytegpt(path):
        return "bytegpt"
    return "unknown"


def decode_load(path):
    """gen_auto_backend — load the correct weight dict by mouth sniff. Returns
    (kind, W). kind in {'clm','bytegpt'}; raises for an unknown mouth."""
    k = decode_mouth_kind(path)
    if k == "clm":
        return "clm", clm_load_weights(path)
    if k == "bytegpt":
        return "bytegpt", bg_load(path)
    raise RuntimeError("ckpt not decodable (unknown mouth): " + str(path))


def decode_auto_topk_sampled(path, seed, gen, top_k, temp, seed_rng):
    """gen_auto_chat — dispatch a seeded top-k decode to the correct mouth by
    header sniff (conv .clm -> clm_decode_topk_sampled_W; byte .bin ->
    bytegpt_decode_topk_sampled_W, KV cache). seed = string."""
    kind, W = decode_load(path)
    if kind == "clm":
        return clm_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)
    return bytegpt_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)


def decode_auto_argmax(path, seed, gen):
    """gen_auto (greedy) — dispatch argmax decode by header sniff. seed = string.
    (clm uses its T=24 right-aligned window; bytegpt grows the window to block.)"""
    kind, W = decode_load(path)
    if kind == "clm":
        # clm_decode_argmax loads-from-path; re-wrap on the already-loaded W path
        V = W["V"]; T = 24
        seed_b = seed.encode('utf-8', 'surrogateescape')
        slen = len(seed_b)
        tok = np.empty(T, dtype=np.float64)
        for p in range(T):
            si = slen - T + p
            tok[p] = float(seed_b[si]) if si >= 0 else 32.0
        out = bytearray()
        for _ in range(gen):
            logits = _fwd_logits(W, tok, T, mbnd_last=True)   # H_9698 perf: gen reads only last row
            row = logits[T - 1]
            besti = 0; bestv = row[0]
            for k in range(1, V):
                if row[k] > bestv:
                    bestv = row[k]; besti = k
            out.append(besti)
            tok[:T - 1] = tok[1:]
            tok[T - 1] = float(besti)
        return {"ok": True, "text": out.decode('utf-8', 'surrogateescape')}
    return _decode_argmax_W(W, seed, gen)


# ════════════════════════════════════════════════════════════════════════
# (e) GROUNDED anti-fabrication mouths + per-seq CE — P4 port (1:1 from
#     core/decode.hexa). The NORMAL emit path whenever kosmos anchors exist:
#     at each step try a deterministic retrieve-then-copy over the anchor
#     texts (longest ctx suffix ≥ l_min found VERBATIM in an anchor → copy its
#     next byte, G5 ✓ cannot fabricate); else fall through to the mouth argmax
#     (weights loaded ONCE). All grounding/abstain LOGIC is plain-byte python;
#     numpy is reused ONLY through the already-parity-proven forwards
#     (_fwd_logits / bg_forward_last_W) + argmax. Byte-exact target = the hexa
#     `--det` decode token stream. hexa `#{...}` → dict.
#
#     BYTES throughout (hexa strings are byte strings; byte_len/substring/ord/chr
#     are byte ops) — seed/anchors are surrogateescape-encoded so the causal
#     window + anchor scan see the exact same bytes the hexa engine does.
#
#     PARITY (P4 measured, toy ckpts, hexa v0.574.1 `hexa run` golden byte-diff):
#       clm_decode_grounded  grounded-copy + LM-fallback + clm_ce_seq_W (CE ≤3e-16)
#       bytegpt_decode_grounded(_abstain)  grounded/span-copy/LM + abstain(40)/
#       lookahead/confirm/closed-class  — ALL byte-identical to the hexa `--det`
#       token stream on both mouths, with and without anchors.
#     ONE known carve-out: hexa strings CANNOT hold a NUL — `"a"+chr(0)+"b"` has
#     byte_len 2 (the chr(0) is dropped). So if a mouth's argmax ever emits byte 0
#     (NUL), hexa silently omits it while this py path (bytearray, NUL-faithful)
#     keeps it — a 1-byte divergence. This never occurs on real text ckpts (a byte
#     LM over UTF-8 text does not argmax NUL) and matches the pre-existing base
#     `bytegpt_decode_argmax`'s bytearray contract; py is left NUL-faithful (not
#     bug-ported) deliberately.
# ════════════════════════════════════════════════════════════════════════

def _dg_to_bytes(s):
    """string|bytes|list[int] -> bytes (byte-exact seed/anchor coercion)."""
    if isinstance(s, bytes):
        return s
    if isinstance(s, bytearray):
        return bytes(s)
    if isinstance(s, (list, tuple)):
        return bytes(int(x) & 0xFF for x in s)
    return s.encode('utf-8', 'surrogateescape')


def _dg_find(hay, needle):
    """first byte-offset of needle in hay, -1 if absent — mirrors
    _clmd_find ≡ _bg_find (byte-identical). nn==0 or nn>hn ⇒ -1 (hexa guards);
    otherwise identical to the hexa left-to-right first-hit scan."""
    if len(needle) == 0 or len(needle) > len(hay):
        return -1
    return hay.find(needle)


def _dg_find_from(hay, needle, frm):
    """_bg_find_from — first offset of needle in hay at or after frm, -1 if none."""
    if len(needle) == 0 or len(needle) > len(hay):
        return -1
    if frm < 0:
        frm = 0
    return hay.find(needle, frm)


def _dg_anchor_copy(ctx, anchors, l_min, l_max):
    """_clmd_anchor_copy ≡ _bg_anchor_copy — retrieve-then-copy probe. Try the
    longest ctx suffix (l_max..l_min) that occurs VERBATIM in some anchor; on a
    hit return the anchor's NEXT byte, else -1. ctx/anchors are bytes.
    (Uses ONLY the FIRST occurrence per anchor, exactly like hexa's _*_find; a
    match whose next byte is at the anchor end does NOT return — falls through.)"""
    clen = len(ctx)
    L = l_max
    if L > clen:
        L = clen
    while L >= l_min:
        suf = ctx[clen - L:clen]
        for an in anchors:
            pos = _dg_find(an, suf)
            if pos >= 0:
                nxt = pos + L
                if nxt < len(an):
                    return an[nxt]
        L -= 1
    return -1


def _mouth_sample_row(row, V, top_k, temp, rng_state):
    """H_9328 DO-MOUTH — draw from the substrate's OWN posterior instead of rounding it to
    argmax. temp=1.0 IS the posterior (the one non-arbitrary temperature); the LCG keeps the
    draw seeded/reproducible. Callers use this ONLY on a step the engine was already going to
    generate (never on a grounded anchor-copy step, which is the p5 anti-fabrication path)."""
    k = V if top_k <= 0 or top_k > V else top_k
    idx = list(range(V))
    idx.sort(key=lambda i: -float(row[i]))
    idx = idx[:k]
    mx = max(float(row[i]) for i in idx)
    ws = [math.exp((float(row[i]) - mx) / temp) for i in idx]
    tot = sum(ws)
    rng_state[0] = (1103515245 * rng_state[0] + 12345) & 0x7FFFFFFF
    u = (rng_state[0] / 2147483648.0) * tot
    acc = 0.0
    for j, i in enumerate(idx):
        acc += ws[j]
        if u <= acc:
            return i
    return idx[-1]


def clm_decode_grounded(path, seed, gen, anchor_texts, l_min, mouth=None):
    """decode.hexa::clm_decode_grounded — G5 anti-fabrication decode over the
    int4-dequant CLMConvMoE (.clm). At each step try an anchor-copy (grounded);
    else CLMConvMoE argmax over the last T=24 ctx bytes (right-aligned, pad-left
    byte 32 — the SAME causal window clm_decode_argmax builds). Non-decodable
    .clm ⇒ ok=false (caller does its honest substrate fallthrough).
    Returns {ok, text, grounded, lm}."""
    if not clm_decodable(path):
        return {"ok": False, "text": "", "grounded": 0, "lm": 0}
    W = clm_load_weights(path)
    V = W["V"]
    T = 24
    tok = np.empty(T, dtype=np.float64)          # H_1400: reused window
    seed_b = _dg_to_bytes(seed)
    anchors = [_dg_to_bytes(a) for a in anchor_texts]
    out = bytearray()
    grounded = 0
    lm = 0
    # H_9328 DO-MOUTH — mouth=None (default) ⇒ argmax ⇒ BYTE-IDENTICAL to the production path.
    _rng = [int(mouth["seed_rng"]) & 0x7FFFFFFF] if mouth is not None else None
    for _ in range(gen):
        ctx = seed_b + bytes(out)
        cb = _dg_anchor_copy(ctx, anchors, l_min, T)
        if cb >= 0:
            nb = cb                              # GROUNDED: verbatim anchor copy
            grounded += 1                        # ← p5 anti-fabrication path · NEVER sampled
        else:
            cl = len(ctx)
            for p in range(T):
                si = cl - T + p
                tok[p] = float(ctx[si]) if si >= 0 else 32.0
            logits = _fwd_logits(W, tok, T, mbnd_last=True)   # H_9698 perf: gen reads only last row
            row = logits[T - 1]
            # H_9575 · PC2 → mouth (Fable design · owner-approved grounded rewire): the
            # emit-ORTHOGONAL tension axis PC2 as a CONTEXT-PRESENCE logit bias in log-prob
            # units. z>0 (originality pole) subtracts z from every byte already in the
            # model's OWN T-window → the draw moves OFF-context; z<0 (balance/coherence
            # pole) pulls it TOWARD context. lm-branch ONLY — the grounded anchor-copy step
            # (nb=cb above) never reaches here, so p5 anti-fabrication is untouched. "pc2"
            # absent or 0.0 ⇒ row untouched ⇒ byte-identical. New constants 0 (loading is
            # H_9468 frozen, gain=1 = log-prob natural unit).
            _pz = float(mouth["pc2"]) if (mouth is not None and "pc2" in mouth) else 0.0
            if _pz != 0.0:
                row = list(row)
                for _v in set(int(tok[_p]) for _p in range(T)):
                    if 0 <= _v < V:
                        row[_v] = row[_v] - _pz
            if mouth is not None and float(mouth["temp"]) > 0.0:
                # REVEAL: this step the engine was ALREADY going to generate (no anchor
                # covered it). We only stop ROUNDING its own posterior to argmax.
                nb = _mouth_sample_row(row, V, int(mouth["top_k"]),
                                       float(mouth["temp"]), _rng)
            else:
                besti = 0
                bestv = row[0]
                for k in range(1, V):
                    if row[k] > bestv:
                        bestv = row[k]; besti = k
                nb = besti
            lm += 1
        out.append(nb)
    return {"ok": True, "text": bytes(out).decode('utf-8', 'surrogateescape'),
            "grounded": grounded, "lm": lm}


def bytegpt_decode_grounded(path, seed, gen, anchor_texts, l_min):
    """decode.hexa::bytegpt_decode_grounded — SAME grounded loop as
    clm_decode_grounded, but the ungrounded fallback is the ByteGPT argmax over
    the last `block` tokens. Weights loaded ONCE. Returns {ok, text, grounded, lm}."""
    W = bg_load(path)
    vocab = W["vocab"]; block = W["block"]
    seed_b = _dg_to_bytes(seed)
    anchors = [_dg_to_bytes(a) for a in anchor_texts]
    toks = list(seed_b)                          # int token list
    out = bytearray()
    grounded = 0
    lm = 0
    for _ in range(gen):
        ctx = seed_b + bytes(out)
        cb = _dg_anchor_copy(ctx, anchors, l_min, block)
        if cb >= 0:
            nb = cb                              # GROUNDED: verbatim anchor copy
            grounded += 1
        else:
            n = len(toks)
            start = 0
            if n > block:
                start = n - block
            T = n - start
            ids = toks[start:start + T]
            logits = bg_forward_last_W(W, ids, T)
            nb = bg_argmax(logits)               # over vocab (len == vocab)
            lm += 1
        toks.append(nb)
        out.append(nb)
    return {"ok": True, "text": bytes(out).decode('utf-8', 'surrogateescape'),
            "grounded": grounded, "lm": lm}


# ── ByteGPT COPY-THEN-ABSTAIN helpers (H_1163) — 1:1 from decode.hexa ──

def _bg_is_word(b):
    return (65 <= b <= 90) or (97 <= b <= 122)


def _bg_is_upper(b):
    return 65 <= b <= 90


def _bg_lower1(b):
    return b + 32 if (65 <= b <= 90) else b


def _bg_lm_argmax_toks(W, toks, vocab, block):
    """one ByteGPT argmax over the last `block` tokens of toks (int list)."""
    n = len(toks)
    start = 0
    if n > block:
        start = n - block
    T = n - start
    ids = [int(toks[start + p]) for p in range(T)]
    logits = bg_forward_last_W(W, ids, T)
    return bg_argmax(logits)


# closed-class English function words (fixed finite set, p7 — no data tuning)
_BG_CLOSED_CLASS = frozenset(
    w.encode('ascii') for w in (
        "the", "this", "that", "these", "those", "they", "them", "their", "there", "then",
        "than", "a", "an", "and", "but", "or", "if", "is", "it", "its", "i", "we", "you", "he",
        "she", "his", "her", "our", "your", "my", "me", "to", "of", "in", "on", "at", "by", "for",
        "as", "so", "no", "not", "do", "does", "did", "was", "were", "be", "been", "have", "has",
        "had", "will", "would", "can", "could", "should", "may", "might", "with", "from", "when",
        "where", "what", "who", "how", "why", "which", "while", "yes", "ok", "well"))


def _bg_is_closed_class(W, toks, lm_b, vocab, block):
    """roll the LM forward from lm_b to read the whole word (lowercased, ≤13 chars)
    and test closed-class membership — decode.hexa::_bg_is_closed_class."""
    w = bytearray([_bg_lower1(lm_b)])
    ext = [int(t) for t in toks]
    ext.append(lm_b)
    k = 0
    while k < 12:
        nb = _bg_lm_argmax_toks(W, ext, vocab, block)
        if not _bg_is_word(nb):
            k = 12
        else:
            w.append(_bg_lower1(nb)); ext.append(nb); k += 1
    return bytes(w) in _BG_CLOSED_CLASS


def _bg_lookahead_entity(ctx, anchors, l_min, l_max):
    """SEED-SUFFIX look-ahead: longest ctx suffix that occurs in an anchor whose
    NEXT byte STARTS a capitalized word → packed a*100000 + entity-start offset,
    else -1 — decode.hexa::_bg_lookahead_entity."""
    clen = len(ctx)
    L = l_max
    if L > clen:
        L = clen
    while L >= l_min:
        suf = ctx[clen - L:clen]
        for a, an in enumerate(anchors):
            alen = len(an)
            frm = 0
            found = True
            while found:
                pos = _dg_find_from(an, suf, frm)
                if pos < 0:
                    found = False
                else:
                    nxt = pos + L
                    if nxt < alen and _bg_is_upper(an[nxt]):
                        return a * 100000 + nxt
                    frm = pos + 1
        L -= 1
    return -1


def _bg_confirm_lm_byte0(ctx, lm_b, anchors, l_min, l_max, budget):
    """COPY-CONFIRM the LM byte-0: tentatively take lm_b, let the copy ground the
    continuation; if the assembled span is a VERBATIM anchor substring (≥2 bytes,
    ≥1 copied), return it (bytes), else b'' — decode.hexa::_bg_confirm_lm_byte0."""
    if budget < 2:
        return b""
    if not _bg_is_word(lm_b):
        return b""
    span = bytearray([lm_b])
    cur = bytearray(ctx)
    cur.append(lm_b)
    go = True
    while go and len(span) < budget:
        cb = _dg_anchor_copy(bytes(cur), anchors, l_min, l_max)
        if cb >= 0 and _bg_is_word(cb):
            span.append(cb); cur.append(cb)
        else:
            go = False
    if len(span) < 2:
        return b""
    sp = bytes(span)
    for an in anchors:
        if _dg_find(an, sp) >= 0:
            return sp
    return b""


def bytegpt_decode_grounded_abstain(path, seed, gen, anchor_texts, l_min):
    """decode.hexa::bytegpt_decode_grounded_abstain — G5 FINAL anti-fabrication
    decode (H_1163). COPY-THEN-ABSTAIN ordering + span-level entity copy +
    closed-class exclusion: (1) byte-level grounded copy FIRST (never pre-empted);
    (2) span-copy the contiguous entity word-run; (3) on an ungrounded LM-would-
    start-a-capitalized-word step give the copy two more chances — (3a) seed-suffix
    look-ahead span-copy, (3b) copy-confirm the LM byte-0 — only if BOTH fail
    ABSTAIN (emit a HEDGE space); (4) never abstain on a closed-class word.
    Weights loaded ONCE. Returns {ok, text, grounded, lm, abstained}."""
    W = bg_load(path)
    vocab = W["vocab"]; block = W["block"]
    seed_b = _dg_to_bytes(seed)
    anchors = [_dg_to_bytes(a) for a in anchor_texts]
    toks = list(seed_b)
    out = bytearray()
    grounded = 0
    lm = 0
    abstained = 0
    in_abstain = False
    emitted = 0
    while emitted < gen:
        ctx = seed_b + bytes(out)
        # (1) byte-level grounded copy FIRST
        cb = _dg_anchor_copy(ctx, anchors, l_min, block)
        if cb >= 0:
            toks.append(cb); out.append(cb); emitted += 1
            grounded += 1; in_abstain = False
            # (2) SPAN-COPY the contiguous entity word-run from the anchor
            if _bg_is_word(cb):
                cont = True
                while cont and emitted < gen:
                    ctx2 = seed_b + bytes(out)
                    cb2 = _dg_anchor_copy(ctx2, anchors, l_min, block)
                    if cb2 >= 0 and _bg_is_word(cb2):
                        toks.append(cb2); out.append(cb2); emitted += 1
                        grounded += 1
                    else:
                        cont = False
        else:
            # UNGROUNDED — peek LM argmax, decide entity-start
            lm_b = _bg_lm_argmax_toks(W, toks, vocab, block)
            prev = 0x20
            if len(toks) > 0:
                prev = int(toks[-1])
            start_entity = _bg_is_upper(lm_b) and not _bg_is_word(prev)
            continue_entity = in_abstain and _bg_is_word(lm_b)
            # (4) closed-class exclusion
            if start_entity and _bg_is_closed_class(W, toks, lm_b, vocab, block):
                start_entity = False
            if start_entity or continue_entity:
                # (3a) SEED-SUFFIX look-ahead → span-copy
                la = _bg_lookahead_entity(ctx, anchors, l_min, block)
                handled = False
                if la >= 0:
                    ai = la // 100000
                    apos = la - ai * 100000
                    an = anchors[ai]
                    alen = len(an)
                    copied = False
                    go = True
                    while go and emitted < gen and apos < alen:
                        ab = an[apos]
                        if _bg_is_word(ab):
                            toks.append(ab); out.append(ab); emitted += 1
                            grounded += 1; copied = True; apos += 1
                        else:
                            go = False
                    if copied:
                        in_abstain = False; handled = True
                if not handled:
                    # (3b) COPY-CONFIRM the LM byte-0
                    span = _bg_confirm_lm_byte0(ctx, lm_b, anchors, l_min, block, gen - emitted)
                    if len(span) >= 2:
                        q = 0
                        sl = len(span)
                        while q < sl and emitted < gen:
                            bb = span[q]
                            toks.append(bb); out.append(bb); emitted += 1
                            q += 1
                        grounded += (sl - 1)     # byte-0 LM but anchor-CONFIRMED
                        in_abstain = False; handled = True
                if not handled:
                    # ABSTAIN — emit HEDGE space, assert no entity
                    toks.append(0x20); out.append(0x20); emitted += 1
                    abstained += 1; in_abstain = True
            else:
                toks.append(lm_b); out.append(lm_b); emitted += 1
                lm += 1; in_abstain = False
    return {"ok": True, "text": bytes(out).decode('utf-8', 'surrogateescape'),
            "grounded": grounded, "lm": lm, "abstained": abstained}


# ── public per-sequence CE — 1:1 from decode.hexa::clm_ce_seq_W ──
# The seq-input twin of clm_forward_ce: single window T=len(seq)-1, next-byte CE
# (same per-position math as clm_forward_ce). The hexa scratch (clm_scratch_new_pub)
# is a GPU-forge resident-scratch lifecycle that the numpy host path does not need;
# the *_pub scratch entries are kept as no-op stubs for surface parity so a caller
# mirroring the hexa (W, sc, seq) shape works unchanged.

clm_load_W = clm_load_weights                     # decode.hexa::clm_load_W (pub loader alias)


def clm_scratch_new_pub(W, maxT):
    """decode.hexa::clm_scratch_new_pub — no-op on the numpy host path (no resident
    forge scratch); returned handle is unused by clm_ce_seq_W. Surface parity only."""
    return None


def clm_scratch_free_pub(sc):
    """decode.hexa::clm_scratch_free_pub — no-op (host path has no scratch to free)."""
    return None


def clm_ce_seq_W(W, sc, seq):
    """decode.hexa::clm_ce_seq_W — CE over a byte SEQ (list[int]) given a pre-loaded
    W. Single window T=len(seq)-1, next-byte CE. `sc` is accepted for signature
    parity with the hexa scratch API and IGNORED on the numpy host path. n<2 ⇒
    uniform CE = dt_ln(V) (verbatim hexa fallback)."""
    V = W["V"]
    n = len(seq)
    if n < 2:
        return float(dt_ln(np.array(float(V))))
    T = n - 1
    tok = np.array([float(seq[p]) for p in range(T)], dtype=np.float64)
    tgt = np.array([float(seq[p + 1]) for p in range(T)], dtype=np.float64)
    logits = _fwd_logits(W, tok, T)
    return float(nn_ce_loss_allpos(logits, tgt, T, V))


def clm_ce_seq(path, seq):
    """convenience: load-from-path per-seq CE (clm_ce_seq_W with a fresh W)."""
    if not clm_decodable(path):
        return float("nan")
    W = clm_load_weights(path)
    return clm_ce_seq_W(W, None, seq)
