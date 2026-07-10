"""Precision + RAM-guard + lean-load shim for the 3B anima_py.core.decode weight load.

ANIMA_DTYPE in {float64 (canonical, ~24.6GB resident), float32 (~12.3GB), float16 (~6.15GB)}.
  Weights are STORED at the chosen dtype but numpy up-casts fp16/fp32 @ fp64 activations to
  fp64 in every matmul, so ARITHMETIC stays fp64-quality; only weight STORAGE precision drops
  (on top of the int4 quantization already in the .clm — so fp32 storage is within fp32-rounding
  of the fp64 canonical loader, since the .clm weights are int4-code x fp32-scale).

ANIMA_LEAN=1 (default) installs a lean clm_load_weights that loads -> transposes -> FREES each
  conv block in turn, so peak residency ~= the final W dict (no originals+copies doubling). The
  returned W dict is byte-IDENTICAL to the stock loader (same keys, same transposed contiguous
  arrays, same trailer parse via the real read_slw/read_clml) — ONLY the load-time memory profile
  changes. Stock loader peak (both originals + .T.copy() copies alive during the dict literal) is
  ~2x resident (fp64 ~49GB, fp32 ~24.6GB, fp16 ~12.3GB); lean peak ~= resident.

A preflight guard REFUSES a load whose estimated PEAK exceeds available RAM (no swap-wedge)."""
import os, sys, numpy as np
from anima_py.core import decode as dec
# the stock clm_load_weights does bare `from slw import ...` / `from clml import ...`
# (H_9200/H_9235 codecs) — resolvable only with anima_py/core on sys.path. Add it so the
# CANONICAL loader + trailer parse work identically to `anima-py evaluate`.
_CORE = os.path.dirname(dec.__file__)
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

_DT = {"float64": np.float64, "float32": np.float32, "float16": np.float16}
# peak GB estimate: lean ~= resident; stock ~= 2x resident
_RESIDENT = {"float64": 24.6, "float32": 12.3, "float16": 6.15}


def _avail_gb():
    try:
        with open("/proc/meminfo") as f:
            mi = {l.split(":")[0]: int(l.split()[1]) for l in f}
        return mi.get("MemAvailable", 0) / (1024**2)
    except Exception:
        return 999.0


def _lean_load_weights(path, dt):
    """Byte-identical to dec.clm_load_weights but frees each conv block right after its
    transpose-copy (peak ~= resident, not 2x). Mirrors decode.py clm_load_weights exactly."""
    if not dec.clm_decodable(path):
        return {"ok": False}
    rb = open(path, 'rb').read()
    nblk = rb[4]
    d = dec._rd_u32(rb, 5)
    rest0 = dec._rd_u32(rb, 9)
    K = rest0 // d
    off = 5; bi = 0; E = 2; V = 256
    while bi < nblk:
        c = dec._rd_u32(rb, off); r = dec._rd_u32(rb, off + 4)
        if bi == nblk - 2: E = c
        if bi == nblk - 1: V = c
        n = c * r
        off = off + 8 + (n + 1) // 2 + c * 4
        bi = bi + 1
    L = nblk - E - 3

    def _blk_T(off):
        w, off2 = dec._load_block(rb, off)      # fp64 [cout, rest]
        wt = w.astype(dt).T.copy()              # -> dt [rest, cout] contiguous
        del w
        return wt, off2

    off = 5
    ecWt, off = _blk_T(off)
    tcWt = []
    for _ in range(L):
        wt, off = _blk_T(off); tcWt.append(wt)
    eWt = []
    for _ in range(E):
        wt, off = _blk_T(off); eWt.append(wt)
    rWt, off = _blk_T(off)
    roWt, off = _blk_T(off)
    off = off + 5                               # skip "CLMX" + n_ext byte

    def _ext(off):
        v, off2 = dec._load_ext(rb, off)
        return v.astype(dt), off2

    embed, off = _ext(off)
    ecB, off = _ext(off)
    tcB = []
    for _ in range(L):
        v, off = _ext(off); tcB.append(v)
    eB = []
    for _ in range(E):
        v, off = _ext(off); eB.append(v)
    rB, off = _ext(off)
    roB, off = _ext(off)
    tgG = []
    for _ in range(L):
        v, off = _ext(off); tgG.append(v)
    tgB = []
    for _ in range(L):
        v, off = _ext(off); tgB.append(v)
    noG, off = _ext(off)
    noB, off = _ext(off)

    W = {
        "ok": True, "d": d, "E": E, "V": V, "K": K, "L": L,
        "ecWt": ecWt, "ecB": ecB, "tcWt": tcWt, "tcB": tcB,
        "eWt": eWt, "eB": eB, "rWt": rWt, "rB": rB, "roWt": roWt, "roB": roB,
        "embed": embed.reshape(V, d), "tgG": tgG, "tgB": tgB,
        "noG": noG, "noB": noB, "bind_type": 0,
    }
    # optional CLMB bind trailer (H_1818) — same parse as stock
    if (off + 5 <= len(rb) and rb[off] == 67 and rb[off + 1] == 76
            and rb[off + 2] == 77 and rb[off + 3] == 66):
        off += 4
        bind_type = rb[off]; off += 1
        WaW, off = dec._load_block(rb, off)
        WbW, off = dec._load_block(rb, off)
        WaB_ext, off = dec._load_ext(rb, off)
        WbB_ext, off = dec._load_ext(rb, off)
        W["bind_type"] = int(bind_type)
        W["WaWt"] = WaW.astype(dt).T.copy(); W["WbWt"] = WbW.astype(dt).T.copy()
        W["WaB"] = WaB_ext.astype(dt); W["WbB"] = WbB_ext.astype(dt)
    # SLW + CLML trailers via the REAL core codecs (byte-parity)
    from anima_py.core.slw import read_slw
    W["slw"], off = read_slw(rb, off)
    from anima_py.core.clml import read_clml
    W["clml"], off = read_clml(rb, off, W["d"], W["V"])
    return W


def install(require_headroom=True):
    name = os.environ.get("ANIMA_DTYPE", "float64")
    lean = os.environ.get("ANIMA_LEAN", "1") == "1"
    dt = _DT[name]
    if require_headroom:
        # peak = transposed W residency (+15% numpy transient) + rb file buffer(1.6GB) + 2GB margin
        peak = _RESIDENT[name] * (1.15 if lean else 2.0) + 1.6 + 2.0
        avail = _avail_gb()
        if avail < peak:
            raise SystemExit(f"RAM-GUARD ABORT: dtype={name} lean={lean} peak~{peak:.1f}GB "
                             f"> MemAvailable {avail:.1f}GB (would swap-wedge). Free RAM / lower precision.")
    if dt is not np.float64 and not lean:
        _ob, _oe = dec._load_block, dec._load_ext
        def _lb(rb, off):
            w, o = _ob(rb, off); return w.astype(dt), o
        def _le(rb, off):
            v, o = _oe(rb, off); return v.astype(dt), o
        dec._load_block = _lb
        dec._load_ext = _le
    if lean:
        dec.clm_load_weights = lambda path: _lean_load_weights(path, dt)
    return name + ("-lean" if lean else "")
