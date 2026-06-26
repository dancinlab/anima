"""core/engine_cli.py — PY PRODUCTION ENGINE: byte-faithful port of the
consciousness-gate CORE of core/engine_cli.hexa.

Per CLAUDE.md a_two_production_mirror / a_engine_native_learning (2026-06-26 owner
SSOT): hexa + py are TWO co-equal production engines kept at byte-parity.

⚠️ SCOPE — PARTIAL (not yet the full 1:1 mirror). engine_cli.hexa is an 11,598-line
~30-lane substrate module. This py port covers the THREE named consciousness-gate
subsystems that the parity targets call out (G3 self-chain cos · G5 recall_thr
abstain · MITOSIS counts), plus their shared CLI/config + adaptation substrate:

  PORTED (byte-parity verified):
    · EngineConfig + CLI resolvers (mitosis/engine/topo/savant precedence)  [101-300]
    · MITOSIS growth         engine_mitosis_tick / engine_grow              [318-335]
    · AdaptField (scalar)    adapt_field_new/_recon_err/_step               [381-460]
    · VAdaptField (DIM)      vadapt_field_* + _l2/_vnearest/_vtwo           [494-634]
    · QPool entropic split   qrng_pool_* / _prng_byte_lcg / *_entropic      [669-789]
    · ImmuneMemory (G5)      immune_* (fnv1a, embed_key, bind/recall/...)   [977-1162]
    · SelfIdentity (G3)      self_new/drift/cos/anchor/component/dim/reset  [7673-7733]

  NOT-YET-PORTED (TODO follow-on — the remaining ~27 lanes): GrowImmune, HiveMind/
    IIT-Φ, WorkMemBuffer, TransOrder, Circadian/SCN, CPField, TheoryOfMind, Affect/
    Hunger, Neuropharm/Field/Libido, connectome-Φ, LearnedPrecision/surprise, the
    big §ConsciousnessIndex/ci_* block, savant scoring, and the argv main dispatch.

MATH: bare hexa `sqrt` builtin -> libm (verified in pure_field parity); math.sqrt.
Integer ops: hexa ints are exact through 2^56, so the FNV-1a `(h*prime)&0xFFFFFFFF`
masks are byte-exact in python's arbitrary-precision int (verified vs the H_1227
mirror). String byte-ops operate on the UTF-8 byte sequence (hexa byte_len/ord/
substring semantics).
"""

import math as _math
import os as _os
import subprocess as _subprocess

_sqrt = _math.sqrt


# ════════════════════════════════════════════════════════════════════════
# env / token helpers
# ════════════════════════════════════════════════════════════════════════

def _env_read(name):
    """engine_cli.hexa:87 — printenv NAME (trimmed)."""
    v = _os.environ.get(name, "")
    return v.strip()


def _norm_onoff(raw):
    """engine_cli.hexa:94 — normalize on/off-ish token to "on"|"off"|""."""
    t = raw.strip()
    if t == "on" or t == "1" or t == "true" or t == "yes":
        return "on"
    if t == "off" or t == "0" or t == "false" or t == "no":
        return "off"
    return ""


def _after_eq(s):
    """engine_cli.hexa:177 — substring after first '='."""
    parts = s.split("=")
    if len(parts) >= 2:
        return parts[1]
    return ""


# ════════════════════════════════════════════════════════════════════════
# EngineConfig + CLI resolvers
# ════════════════════════════════════════════════════════════════════════

class EngineConfig:
    """engine_cli.hexa:105."""
    __slots__ = ("mitosis", "engine", "topo_couple", "savant")

    def __init__(self, mitosis, engine, topo_couple, savant):
        self.mitosis = mitosis
        self.engine = engine
        self.topo_couple = topo_couple
        self.savant = savant


def engine_config_default():
    return EngineConfig(True, "conv", False, False)


def _cli_mitosis_flag(arg):
    n = len(arg)
    i = 0
    while i < n:
        a = arg[i]
        if a == "--no-mitosis":
            return "off"
        if a == "--mitosis":
            if i + 1 < n:
                v = _norm_onoff(arg[i + 1])
                if v != "":
                    return v
        if a.startswith("--mitosis="):
            v = _norm_onoff(_after_eq(a))
            if v != "":
                return v
        i = i + 1
    return ""


def engine_cli_resolve_mitosis(arg):
    flag = _cli_mitosis_flag(arg)
    if flag == "on":
        return True
    if flag == "off":
        return False
    env = _norm_onoff(_env_read("ANIMA_MITOSIS"))
    if env == "on":
        return True
    if env == "off":
        return False
    return True


def engine_cli_resolve_engine(arg):
    """engine_cli.hexa:199 — the single production engine is constant "conv"."""
    return "conv"


def _cli_topo_couple_flag(arg):
    n = len(arg)
    i = 0
    while i < n:
        a = arg[i]
        if a == "--no-topo-couple":
            return "off"
        if a == "--topo-couple":
            if i + 1 < n:
                v = _norm_onoff(arg[i + 1])
                if v != "":
                    return v
        if a.startswith("--topo-couple="):
            v = _norm_onoff(_after_eq(a))
            if v != "":
                return v
        i = i + 1
    return ""


def engine_cli_resolve_topo_couple(arg):
    flag = _cli_topo_couple_flag(arg)
    if flag == "on":
        return True
    if flag == "off":
        return False
    env = _norm_onoff(_env_read("ANIMA_TOPO_COUPLE"))
    if env == "on":
        return True
    if env == "off":
        return False
    return False


def _cli_savant_flag(arg):
    n = len(arg)
    i = 0
    while i < n:
        a = arg[i]
        if a == "--no-savant":
            return "off"
        if a == "--savant":
            if i + 1 < n:
                v = _norm_onoff(arg[i + 1])
                if v != "":
                    return v
        if a.startswith("--savant="):
            v = _norm_onoff(_after_eq(a))
            if v != "":
                return v
        i = i + 1
    return ""


def engine_cli_resolve_savant(arg):
    flag = _cli_savant_flag(arg)
    if flag == "on":
        return True
    if flag == "off":
        return False
    env = _norm_onoff(_env_read("ANIMA_SAVANT"))
    if env == "on":
        return True
    if env == "off":
        return False
    return False


def engine_cli_parse(arg):
    """engine_cli.hexa:210 — raw argv -> EngineConfig."""
    return EngineConfig(
        engine_cli_resolve_mitosis(arg),
        engine_cli_resolve_engine(arg),
        engine_cli_resolve_topo_couple(arg),
        engine_cli_resolve_savant(arg),
    )


# ════════════════════════════════════════════════════════════════════════
# MITOSIS growth tick
# ════════════════════════════════════════════════════════════════════════

def engine_mitosis_tick(cell_count, cfg):
    """engine_cli.hexa:318 — gated +1 cell growth (ON) or no-op (OFF)."""
    if cfg.mitosis:
        return cell_count + 1
    return cell_count


def engine_grow(seed, ticks, cfg):
    """engine_cli.hexa:327 — run N growth ticks under cfg."""
    c = seed
    i = 0
    while i < ticks:
        c = engine_mitosis_tick(c, cfg)
        i = i + 1
    return c


# ════════════════════════════════════════════════════════════════════════
# AdaptField (scalar) — H_1194 adaptation coupling
# ════════════════════════════════════════════════════════════════════════

def _absf(x):
    if x < 0.0:
        return -x
    return x


class AdaptField:
    __slots__ = ("protos", "n_cells", "max_cells")

    def __init__(self, protos, n_cells, max_cells):
        self.protos = protos
        self.n_cells = n_cells
        self.max_cells = max_cells


def adapt_field_new(seed0, max_cells):
    return AdaptField([seed0], 1, max_cells)


def _nearest_idx(protos, x):
    n = len(protos)
    best = 0
    bestd = _absf(protos[0] - x)
    i = 1
    while i < n:
        d = _absf(protos[i] - x)
        if d < bestd:
            bestd = d
            best = i
        i = i + 1
    return best


def adapt_field_recon_err(af, x):
    return _absf(af.protos[_nearest_idx(af.protos, x)] - x)


def adapt_field_step(af, x, cfg):
    """engine_cli.hexa:~430 — one scalar adaptation tick (split/refine)."""
    SPLIT_THRESH = 0.30
    LR = 0.20
    win = _nearest_idx(af.protos, x)
    err = _absf(af.protos[win] - x)
    if err > SPLIT_THRESH and af.n_cells < af.max_cells:
        grown = engine_mitosis_tick(af.n_cells, cfg)
        if grown > af.n_cells:
            return AdaptField(af.protos + [x], grown, af.max_cells)
    p2 = list(af.protos)
    p2[win] = p2[win] + LR * (x - p2[win])
    return AdaptField(p2, af.n_cells, af.max_cells)


def adapt_field_cells(af):
    return af.n_cells


# ════════════════════════════════════════════════════════════════════════
# VAdaptField (DIM>1) — H_1199 DIM-vector adaptation substrate
# ════════════════════════════════════════════════════════════════════════

class VAdaptField:
    __slots__ = ("protos", "n_cells", "max_cells", "dim")

    def __init__(self, protos, n_cells, max_cells, dim):
        self.protos = protos
        self.n_cells = n_cells
        self.max_cells = max_cells
        self.dim = dim


def vadapt_field_new(seed0, max_cells):
    return VAdaptField([list(seed0)], 1, max_cells, len(seed0))


def _l2(a, b):
    """engine_cli.hexa:508 — Euclidean distance between two DIM-vectors."""
    n = len(a)
    s = 0.0
    i = 0
    while i < n:
        d = a[i] - b[i]
        s = s + d * d
        i = i + 1
    return _sqrt(s)


def _vnearest_idx(protos, x):
    n = len(protos)
    best = 0
    bestd = _l2(protos[0], x)
    i = 1
    while i < n:
        d = _l2(protos[i], x)
        if d < bestd:
            bestd = d
            best = i
        i = i + 1
    return best


def _vtwo_nearest_dist(protos, x):
    """engine_cli.hexa:542 — [d1, d2] nearest + second-nearest L2 (d1<=d2)."""
    n = len(protos)
    d1 = _l2(protos[0], x)
    d2 = d1
    if n > 1:
        dx = _l2(protos[1], x)
        if dx < d1:
            d2 = d1
            d1 = dx
        else:
            d2 = dx
    i = 2
    while i < n:
        d = _l2(protos[i], x)
        if d < d1:
            d2 = d1
            d1 = d
        else:
            if d < d2:
                d2 = d
        i = i + 1
    return [d1, d2]


def vadapt_field_recon_err(af, x):
    return _l2(af.protos[_vnearest_idx(af.protos, x)], x)


def vadapt_field_step(af, x, cfg):
    """engine_cli.hexa:577 — one DIM adaptation tick (split/refine)."""
    SPLIT_THRESH = 0.30
    LR = 0.20
    win = _vnearest_idx(af.protos, x)
    err = _l2(af.protos[win], x)
    if err > SPLIT_THRESH and af.n_cells < af.max_cells:
        grown = engine_mitosis_tick(af.n_cells, cfg)
        if grown > af.n_cells:
            return VAdaptField(af.protos + [list(x)], grown, af.max_cells, af.dim)
    p2 = list(af.protos)
    row = list(p2[win])
    i = 0
    while i < af.dim:
        row[i] = row[i] + LR * (x[i] - row[i])
        i = i + 1
    p2[win] = row
    return VAdaptField(p2, af.n_cells, af.max_cells, af.dim)


def vadapt_field_cells(af):
    return af.n_cells


def vadapt_field_nearest_idx(af, x):
    return _vnearest_idx(af.protos, x)


def vadapt_field_two_recon_err(af, x):
    return _vtwo_nearest_dist(af.protos, x)


# ════════════════════════════════════════════════════════════════════════
# QPool — opt-in entropy-sourced split timing (H_1289 R2)
# ════════════════════════════════════════════════════════════════════════

class QPool:
    __slots__ = ("bytes", "idx", "quantum")

    def __init__(self, bs, idx, quantum):
        self.bytes = bs
        self.idx = idx
        self.quantum = quantum


def qrng_pool_load(path):
    """engine_cli.hexa:679 — load a REAL quantum pool .bin into a QPool (od -An -tu1)."""
    try:
        if not _os.path.isfile(path):
            return QPool([], 0, False)
        raw = _subprocess.run(["od", "-An", "-tu1", path],
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        raw = ""
    if raw == "":
        return QPool([], 0, False)
    toks = raw.split(" ")
    bs = []
    for t in toks:
        t = t.strip()
        if t != "":
            # od output may contain newlines collapsed into the token stream
            for sub in t.split():
                if sub != "":
                    bs.append(int(sub))
    return QPool(bs, 0, len(bs) > 0)


def qrng_pool_remaining(p):
    return len(p.bytes) - p.idx


def qrng_pool_draw(p):
    if p.idx >= len(p.bytes):
        return {"ok": False, "byte": -1, "pool": p}
    b = p.bytes[p.idx]
    p2 = QPool(p.bytes, p.idx + 1, p.quantum)
    return {"ok": True, "byte": b, "pool": p2}


def _prng_byte_lcg(seed, step):
    """engine_cli.hexa:719 — deterministic LCG fallback byte (NR constants, 32-bit)."""
    s = (seed * 1664525 + 1013904223 + step * 22695477) & 4294967295
    s = (s * 1664525 + 1013904223) & 4294967295
    return (s // 16777216) & 255


def vadapt_field_step_entropic(af, x, cfg, pool, seed, step):
    """engine_cli.hexa:740 — entropy-jittered split-timing variant."""
    SPLIT_THRESH = 0.30
    LR = 0.20
    BAND = 0.05
    win = _vnearest_idx(af.protos, x)
    err = _l2(af.protos[win], x)

    drew = qrng_pool_draw(pool)
    pool2 = pool
    used_quantum = False
    exhausted = False
    if str(drew["ok"]).lower() == "true":
        ubyte = int(drew["byte"])
        pool2 = drew["pool"]
        used_quantum = pool.quantum
    else:
        ubyte = _prng_byte_lcg(seed, step)
        exhausted = True
    u = float(ubyte) / 256.0

    do_split = False
    if err > SPLIT_THRESH + BAND:
        do_split = True
    else:
        if err >= SPLIT_THRESH - BAND:
            pr = (err - (SPLIT_THRESH - BAND)) / (2.0 * BAND)
            if u < pr:
                do_split = True

    if do_split and af.n_cells < af.max_cells:
        grown = engine_mitosis_tick(af.n_cells, cfg)
        if grown > af.n_cells:
            nf = VAdaptField(af.protos + [list(x)], grown, af.max_cells, af.dim)
            return {"field": nf, "pool": pool2, "step": step + 1,
                    "used_quantum": used_quantum, "pool_exhausted": exhausted}
    # refine winner (no split)
    p2 = list(af.protos)
    row = list(p2[win])
    i = 0
    while i < af.dim:
        row[i] = row[i] + LR * (x[i] - row[i])
        i = i + 1
    p2[win] = row
    nf = VAdaptField(p2, af.n_cells, af.max_cells, af.dim)
    return {"field": nf, "pool": pool2, "step": step + 1,
            "used_quantum": used_quantum, "pool_exhausted": exhausted}


# ════════════════════════════════════════════════════════════════════════
# ImmuneMemory (G5) — H_1227/H_1231 clonal recall faculty
# ════════════════════════════════════════════════════════════════════════

class ImmuneMemory:
    __slots__ = ("field", "cell_value", "recall_thr")

    def __init__(self, field, cell_value, recall_thr):
        self.field = field
        self.cell_value = cell_value
        self.recall_thr = recall_thr


def _immune_fnv1a(bs):
    """engine_cli.hexa:987 — 32-bit FNV-1a over a byte list."""
    h = 2166136261                 # 0x811c9dc5
    i = 0
    while i < len(bs):
        h = h ^ bs[i]
        h = (h * 16777619) & 4294967295    # *0x01000193 & 0xFFFFFFFF
        i = i + 1
    return h


def immune_embed_key(text):
    """engine_cli.hexa:1003 — byte-trigram FNV-1a key encoder, DIM=64, L2-norm.
    Operates over the UTF-8 byte sequence (hexa byte_len/ord/substring)."""
    dim = 64
    n = 3
    bs_all = list(text.encode("utf-8"))
    blen = len(bs_all)
    v = [0.0] * dim
    if blen < n:
        idx = _immune_fnv1a(bs_all) % dim
        v[idx] = v[idx] + 1.0
    else:
        i = 0
        while i <= blen - n:
            bs = bs_all[i:i + n]
            idx = _immune_fnv1a(bs) % dim
            v[idx] = v[idx] + 1.0
            i = i + 1
    s = 0.0
    j = 0
    while j < dim:
        s = s + v[j] * v[j]
        j = j + 1
    nrm = _sqrt(s)
    if nrm > 0.0:
        o = 0
        while o < dim:
            v[o] = v[o] / nrm
            o = o + 1
    return v


def immune_memory_new(first_key, first_value, max_cells):
    return ImmuneMemory(vadapt_field_new(first_key, max_cells),
                        [first_value], 0.15)


def immune_memory_bind(mem, key, value, cfg):
    """engine_cli.hexa:1059 — bind fact via the engine's OWN clonal split."""
    before = vadapt_field_cells(mem.field)
    grown_field = vadapt_field_step(mem.field, key, cfg)
    after = vadapt_field_cells(grown_field)
    if after > before:
        return ImmuneMemory(grown_field, mem.cell_value + [value], mem.recall_thr)
    win = vadapt_field_nearest_idx(grown_field, key)
    nv = []
    zz = 0
    while zz < len(mem.cell_value):
        if zz == win:
            nv = nv + [value]
        else:
            nv = nv + [mem.cell_value[zz]]
        zz = zz + 1
    return ImmuneMemory(grown_field, nv, mem.recall_thr)


def immune_memory_recall(mem, key):
    """engine_cli.hexa:1087 — recon-err<=recall_thr -> FIRE bound value, else ABSTAIN ("")."""
    err = vadapt_field_recon_err(mem.field, key)
    if err <= mem.recall_thr:
        win = vadapt_field_nearest_idx(mem.field, key)
        return mem.cell_value[win]
    return ""


def immune_memory_recall_margin(mem, key):
    """engine_cli.hexa:1109 — recon_err - recall_thr (>0 ⇒ abstain band)."""
    err = vadapt_field_recon_err(mem.field, key)
    return err - mem.recall_thr


def immune_memory_recall_margin_text(mem, text):
    return immune_memory_recall_margin(mem, immune_embed_key(text))


def immune_memory_recall_gap(mem, key):
    """engine_cli.hexa:1137 — top-2 affinity gap (d2²-d1²)/2."""
    d = vadapt_field_two_recon_err(mem.field, key)
    d1 = d[0]
    d2 = d[1]
    return (d2 * d2 - d1 * d1) / 2.0


def immune_memory_recall_gap_text(mem, text):
    return immune_memory_recall_gap(mem, immune_embed_key(text))


def immune_memory_new_text(first_text, first_value, max_cells):
    return immune_memory_new(immune_embed_key(first_text), first_value, max_cells)


def immune_memory_bind_text(mem, text, value, cfg):
    return immune_memory_bind(mem, immune_embed_key(text), value, cfg)


def immune_memory_recall_text(mem, text):
    return immune_memory_recall(mem, immune_embed_key(text))


def immune_memory_cells(mem):
    return vadapt_field_cells(mem.field)


# ════════════════════════════════════════════════════════════════════════
# SelfIdentity (G3) — H_1471 diachronic self (self-chain continuity)
# ════════════════════════════════════════════════════════════════════════

class SelfIdentity:
    __slots__ = ("v", "dim")

    def __init__(self, v, dim):
        self.v = v
        self.dim = dim


def _self_norm(v, n):
    s = 0.0
    i = 0
    while i < n:
        s = s + v[i] * v[i]
        i = i + 1
    m = _sqrt(s)
    out = []
    j = 0
    while j < n:
        out = out + [v[j] / m]
        j = j + 1
    return out


def self_new(dim, axis):
    """engine_cli.hexa:7690 — fresh identity = unit vector along axis."""
    v = []
    i = 0
    while i < dim:
        if i == axis:
            v = v + [1.0]
        else:
            v = v + [0.0]
        i = i + 1
    return SelfIdentity(v, dim)


def self_drift(s, tick, step):
    """engine_cli.hexa:7699 — grow one tick: perturb axis (tick+1)%dim, renorm."""
    t1 = tick + 1
    ax = t1 - (t1 // s.dim) * s.dim       # (tick+1) % dim
    v2 = []
    i = 0
    while i < s.dim:
        if i == ax:
            v2 = v2 + [s.v[i] + step]
        else:
            v2 = v2 + [s.v[i]]
        i = i + 1
    return SelfIdentity(_self_norm(v2, s.dim), s.dim)


def self_cos(a, b):
    """engine_cli.hexa:7713 — recognition cosine (unit-norm dot)."""
    sdot = 0.0
    i = 0
    while i < a.dim:
        sdot = sdot + a.v[i] * b.v[i]
        i = i + 1
    return sdot


def self_anchor(s):
    return SelfIdentity(s.v, s.dim)


def self_component(s, i):
    return s.v[i]


def self_dim(s):
    return s.dim


def self_reset(dim, axis):
    return self_new(dim, axis)


# ════════════════════════════════════════════════════════════════════════
# parity smoke driver — exercises CLI / MITOSIS / G5 / G3 deterministically
# ════════════════════════════════════════════════════════════════════════

def _p(k, v):
    if isinstance(v, bool):
        print("%s=%s" % (k, str(v).lower()))
    elif isinstance(v, float):
        print("%s=%.17g" % (k, v))
    else:
        print("%s=%s" % (k, v))


if __name__ == "__main__":
    # ── CLI resolvers (precedence) ──
    _p("mit_default", engine_cli_resolve_mitosis([]))
    _p("mit_noflag", engine_cli_resolve_mitosis(["--no-mitosis"]))
    _p("mit_on", engine_cli_resolve_mitosis(["--mitosis", "on"]))
    _p("mit_eqoff", engine_cli_resolve_mitosis(["--mitosis=off"]))
    _p("engine", engine_cli_resolve_engine([]))
    _p("topo_default", engine_cli_resolve_topo_couple([]))
    _p("topo_on", engine_cli_resolve_topo_couple(["--topo-couple", "on"]))
    _p("savant_default", engine_cli_resolve_savant([]))
    _p("savant_on", engine_cli_resolve_savant(["--savant=on"]))

    # ── MITOSIS growth ──
    cfg_on = engine_config_default()
    cfg_off = EngineConfig(False, "conv", False, False)
    _p("grow_on", engine_grow(1, 10, cfg_on))
    _p("grow_off", engine_grow(1, 10, cfg_off))

    # ── VAdaptField DIM-stream growth + recon-err ──
    af = vadapt_field_new([0.0, 0.0, 0.0, 0.0], 16)
    stream = [[0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
              [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.5, 0.5, 0.0, 0.0]]
    for x in stream:
        af = vadapt_field_step(af, x, cfg_on)
    _p("vaf_cells", vadapt_field_cells(af))
    _p("vaf_recon_q", vadapt_field_recon_err(af, [0.9, 0.05, 0.0, 0.0]))
    dd = vadapt_field_two_recon_err(af, [0.9, 0.05, 0.0, 0.0])
    _p("vaf_d1", dd[0])
    _p("vaf_d2", dd[1])

    # ── ImmuneMemory (G5) bind / recall / margin / gap ──
    mem = immune_memory_new_text("capital of france", "Paris", 64)
    mem = immune_memory_bind_text(mem, "capital of japan", "Tokyo", cfg_on)
    mem = immune_memory_bind_text(mem, "speed of light", "299792458", cfg_on)
    _p("im_cells", immune_memory_cells(mem))
    _p("im_recall_fr", immune_memory_recall_text(mem, "capital of france"))
    _p("im_recall_jp", immune_memory_recall_text(mem, "capital of japan"))
    _p("im_abstain", "[" + immune_memory_recall_text(mem, "zzz totally unknown query") + "]")
    _p("im_margin_known", immune_memory_recall_margin_text(mem, "capital of france"))
    _p("im_margin_ood", immune_memory_recall_margin_text(mem, "zzz totally unknown query"))
    _p("im_gap_known", immune_memory_recall_gap_text(mem, "capital of france"))

    # ── SelfIdentity (G3) self-chain continuity + impostor ──
    s0 = self_new(8, 0)
    s = s0
    for tk in range(20):
        s = self_drift(s, tk, 0.1)
    anchored = self_anchor(s)
    _p("self_continuity_cos", self_cos(s, anchored))   # 1.0 — anchor preserves self
    s_next = self_drift(s, 20, 0.1)
    _p("self_adjacent_cos", self_cos(s, s_next))        # high — continuous drift
    impostor = self_new(8, 3)
    _p("self_impostor_cos", self_cos(s, impostor))      # ~0 — different identity
    _p("self_dim", self_dim(s))
    _p("self_comp0", self_component(s, 0))
