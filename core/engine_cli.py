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
    · OsmoticStore           osmotic_* + _kl_div                            [839-941]
    · ImmuneMemoryGrow       immune_grow_* + LRU evict (§GrowImmune H_1288) [1212-1353]
    · CLSStore               cls_* + _cls_key16/_cls_coin (§CLS H_1532)     [1399-1719]
    · SkillStore             skill_* (§SkillStore H_1378)                   [1764-1843]
    · UsageStore             usage_* (§UsageStore H_1391)                   [1884-1984]
    · AffectFeatures         affect_* + _lcg_next (§Affect H_1290)          [2032-2131]
    · HomeostaticDrive       homeo_* (§Hypothalamus H_1292)                 [2178-2249]
    · Libido                 libido_* (§Libido H_1504)                      [2304-2407]
    · Allosteric buffer      allo_* + _mi_set (§Allosteric H_1509, exp/sin) [2441-2549]
    · OtherMindModel         other_mind_* (§ToM H_1293 false-belief)        [2598-2649]
    · ConsolidatingMemory    consolidating_* + _lcg_unit/_lcg_gauss         [3015-3234]
    · VAdaptFieldB           vadapt_fieldB_* (§GateB H_1208)                [3264-3343]
    · WorkMemBuffer          wm_buffer_* + _cos_vec (§WorkMem H_1282)       [3407-3564]
    · VForwardField          vforward_* (§Cerebellum H_1280 NLMS)           [3603-3704]
    · HierGoalStack          hier_* + _cos_hier (§HierPFC H_1294)           [3757-3842]
    · SpatialMap             spatial_map_* (§PlaceGrid H_1296)              [3886-3991]
    · TransOrder             trans_order_* (§TransitiveInf H_1429)          [4045-4185]
    · CircadianClock         clock_* (§Circadian H_1298)                    [4234-4277]
    · IntervalTimer          itimer_* (§IntervalTiming H_1299)              [4328-4387]
    · PhaseResetClock        prc_* (§PhaseReset H_1301, sin)                [4439-4499]
    · SCNNetwork             scn_* (§SCN H_1302 Kuramoto, sin/cos/sqrt)     [4549-4700]
    · PhaseField             phasefield_* (§PhaseSyncBinding H_1448)        [4740-4839]
    · QuorumPhase            quorum_* (§Quorum H_1510 decentralized)        [4865-5248]
    · engine_config_summary  introspection string                          [5251]
    · CA3ReplayMemory        ca3_replay_* (§CA3Replay H_1427)               [7403-7496]
    · GlobalWorkspace        gws_* (§GWS H_1462 ignition bottleneck)        [7506-7587]
    · Habituation            hab_* (§Habituation H_1465)                    [7598-7643]
    · PrecisionSurprise+G18-G31 scalar gates  surprise/learned_precision/novelty/
        attn_blink_detect/agency_*/subjective_time/emotion_regulate/directed_forget_recall/
        body_ownership/divided_perf/veto_execute/rivalry_transitions/change_detect/
        imagery_activate/priming_facilitate                                 [7654-7922]

  NOT-YET-PORTED (TODO follow-on — heavy-numerics lanes): CollectivePool/HiveMind-IIT-Φ
    (needs faithful big_phi_bounded port), SkillCell/SkillGradFT (ridge-LSQ + power-iteration),
    CPField, JamoHead/BpeMerges (BPE morphology), §ConsciousnessIndex ci_*/topo_* (covariance/
    Cholesky-logdet/IIT-4 Φ), savant scoring (SAVANT/savant_lib), argv main dispatch.

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
_ln = _math.log
_exp = _math.exp
_sin = _math.sin
_cos = _math.cos
_floor = _math.floor


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
# OsmoticStore — KL>C bottleneck split + value overwrite (H_1569 osmotic)
# engine_cli.hexa:839-941
# ════════════════════════════════════════════════════════════════════════

def _kl_div(p, q):
    """engine_cli.hexa:839 — KL(p||q) with 1e-9 floor (ln=libm in production TU)."""
    n = len(p)
    s = 0.0
    i = 0
    while i < n:
        pi = p[i]
        qi = q[i]
        if pi < 0.000000001:
            pi = 0.000000001
        if qi < 0.000000001:
            qi = 0.000000001
        s = s + pi * _ln(pi / qi)
        i = i + 1
    return s


class OsmoticStore:
    __slots__ = ("field", "vals")

    def __init__(self, field, vals):
        self.field = field
        self.vals = vals


def osmotic_store_new(key0, val0, max_cells):
    return OsmoticStore(vadapt_field_new(key0, max_cells), [val0])


def osmotic_should_split(st, key, val, mode, beta, cap_c, kl_override):
    """engine_cli.hexa:876."""
    SPLIT_THRESH = 0.30
    win = _vnearest_idx(st.field.protos, key)
    d = _l2(st.field.protos[win], key)
    if mode == 0:
        return d > SPLIT_THRESH
    b = beta
    if mode == 2:
        b = 0.0
    if kl_override >= 0.0:
        dkl = kl_override
    else:
        dkl = _kl_div(val, st.vals[win])
    return (d + b * dkl) > cap_c


def osmotic_learn(st, key, val, cfg, mode, beta, cap_c, kl_override):
    """engine_cli.hexa:895."""
    LR = 0.20
    af = st.field
    want_split = osmotic_should_split(st, key, val, mode, beta, cap_c, kl_override)
    if want_split and af.n_cells < af.max_cells:
        grown = engine_mitosis_tick(af.n_cells, cfg)
        if grown > af.n_cells:
            nf = VAdaptField(af.protos + [list(key)], grown, af.max_cells, af.dim)
            return OsmoticStore(nf, st.vals + [list(val)])
    win = _vnearest_idx(af.protos, key)
    p2 = list(af.protos)
    row = list(p2[win])
    i = 0
    while i < af.dim:
        row[i] = row[i] + LR * (key[i] - row[i])
        i = i + 1
    p2[win] = row
    v2 = list(st.vals)
    v2[win] = list(val)
    nf2 = VAdaptField(p2, af.n_cells, af.max_cells, af.dim)
    return OsmoticStore(nf2, v2)


def osmotic_retains(st, key, val, recall_thr):
    """engine_cli.hexa:928."""
    n = st.field.n_cells
    i = 0
    while i < n:
        if _l2(st.field.protos[i], key) <= recall_thr and _l2(st.vals[i], val) <= 0.20:
            return 1.0
        i = i + 1
    return 0.0


def osmotic_cells(st):
    return st.field.n_cells


# ════════════════════════════════════════════════════════════════════════
# ImmuneMemoryGrow (§GrowImmune, H_1288) — grow-under-pressure + LRU evict
# engine_cli.hexa:1212-1353
# ════════════════════════════════════════════════════════════════════════

class ImmuneMemoryGrow:
    __slots__ = ("protos", "cell_value", "last_used", "n_cells", "base_max",
                 "grow_max", "grow_mode", "recall_thr", "split_thr", "tick")

    def __init__(self, protos, cell_value, last_used, n_cells, base_max,
                 grow_max, grow_mode, recall_thr, split_thr, tick):
        self.protos = protos
        self.cell_value = cell_value
        self.last_used = last_used
        self.n_cells = n_cells
        self.base_max = base_max
        self.grow_max = grow_max
        self.grow_mode = grow_mode
        self.recall_thr = recall_thr
        self.split_thr = split_thr
        self.tick = tick


def immune_grow_new(first_key, first_value, base_max, grow_max, grow_mode):
    return ImmuneMemoryGrow([list(first_key)], [first_value], [1], 1,
                            base_max, grow_max, grow_mode, 0.30, 0.30, 1)


def _immune_grow_lru_victim(lu):
    n = len(lu)
    best = 0
    bestv = lu[0]
    i = 1
    while i < n:
        if lu[i] < bestv:
            bestv = lu[i]
            best = i
        i = i + 1
    return best


def immune_grow_bind(mem, key, value, cfg):
    """engine_cli.hexa:1274."""
    t = mem.tick + 1
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    cap = mem.base_max
    if mem.grow_mode:
        cap = mem.grow_max
    if err <= mem.split_thr:
        LR = 0.20
        p2 = list(mem.protos)
        row = list(p2[win])
        d = 0
        while d < len(row):
            row[d] = row[d] + LR * (key[d] - row[d])
            d = d + 1
        p2[win] = row
        nv = list(mem.cell_value)
        nv[win] = value
        lu = list(mem.last_used)
        lu[win] = t
        return ImmuneMemoryGrow(p2, nv, lu, mem.n_cells, mem.base_max,
                                mem.grow_max, mem.grow_mode, mem.recall_thr,
                                mem.split_thr, t)
    if mem.n_cells < cap:
        grown = engine_mitosis_tick(mem.n_cells, cfg)
        if grown > mem.n_cells:
            return ImmuneMemoryGrow(mem.protos + [list(key)],
                                    mem.cell_value + [value],
                                    mem.last_used + [t], grown, mem.base_max,
                                    mem.grow_max, mem.grow_mode, mem.recall_thr,
                                    mem.split_thr, t)
    v = _immune_grow_lru_victim(mem.last_used)
    p3 = list(mem.protos)
    p3[v] = list(key)
    nv2 = list(mem.cell_value)
    nv2[v] = value
    lu2 = list(mem.last_used)
    lu2[v] = t
    return ImmuneMemoryGrow(p3, nv2, lu2, mem.n_cells, mem.base_max,
                            mem.grow_max, mem.grow_mode, mem.recall_thr,
                            mem.split_thr, t)


def immune_grow_recall(mem, key):
    """engine_cli.hexa:1343."""
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    if err <= mem.recall_thr:
        return mem.cell_value[win]
    return ""


def immune_grow_cells(mem):
    return mem.n_cells


# ════════════════════════════════════════════════════════════════════════
# CLSStore (§CLS, H_1532) — AB-AC interference / two-store separation
# engine_cli.hexa:1399-1719
# ════════════════════════════════════════════════════════════════════════

def _cls_key16(text):
    """engine_cli.hexa:1399 — DIM=16 byte-trigram FNV-1a key, L2-norm."""
    dim = 16
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
            idx = _immune_fnv1a(bs_all[i:i + n]) % dim
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


class CLSStore:
    __slots__ = ("protos", "cell_value", "last_used", "n_cells", "max_cells",
                 "abstain", "split_thr", "tick")

    def __init__(self, protos, cell_value, last_used, n_cells, max_cells,
                 abstain, split_thr, tick):
        self.protos = protos
        self.cell_value = cell_value
        self.last_used = last_used
        self.n_cells = n_cells
        self.max_cells = max_cells
        self.abstain = abstain
        self.split_thr = split_thr
        self.tick = tick


def _cls_store_new(max_cells, abstain, split_thr):
    return CLSStore([], [], [], 0, max_cells, abstain, split_thr, 0)


def _cls_write(st, key, value, suppress_retrieval):
    """engine_cli.hexa:1475."""
    t = st.tick + 1
    if suppress_retrieval and st.n_cells < st.max_cells:
        return CLSStore(st.protos + [list(key)], st.cell_value + [value],
                        st.last_used + [t], st.n_cells + 1, st.max_cells,
                        st.abstain, st.split_thr, t)
    if st.n_cells == 0:
        return CLSStore([list(key)], [value], [t], 1, st.max_cells,
                        st.abstain, st.split_thr, t)
    win = _vnearest_idx(st.protos, key)
    err = _l2(st.protos[win], key)
    if err > st.split_thr and st.n_cells < st.max_cells:
        return CLSStore(st.protos + [list(key)], st.cell_value + [value],
                        st.last_used + [t], st.n_cells + 1, st.max_cells,
                        st.abstain, st.split_thr, t)
    if err > st.split_thr and st.n_cells >= st.max_cells:
        ev = _immune_grow_lru_victim(st.last_used)
        p3 = list(st.protos)
        p3[ev] = list(key)
        nv3 = list(st.cell_value)
        nv3[ev] = value
        lu3 = list(st.last_used)
        lu3[ev] = t
        return CLSStore(p3, nv3, lu3, st.n_cells, st.max_cells,
                        st.abstain, st.split_thr, t)
    LR = 0.20
    p2 = list(st.protos)
    row = list(p2[win])
    d = 0
    while d < len(row):
        row[d] = row[d] + LR * (key[d] - row[d])
        d = d + 1
    p2[win] = row
    nv = list(st.cell_value)
    nv[win] = value
    lu = list(st.last_used)
    lu[win] = t
    return CLSStore(p2, nv, lu, st.n_cells, st.max_cells,
                    st.abstain, st.split_thr, t)


def _cls_recall_value(st, key):
    if st.n_cells == 0:
        return ""
    win = _vnearest_idx(st.protos, key)
    err = _l2(st.protos[win], key)
    if err > st.abstain:
        return ""
    return st.cell_value[win]


def _cls_make_abac(n_pairs, n_distract):
    A = []
    B = []
    C = []
    i = 0
    while i < n_pairs:
        A = A + ["key_A" + str(i)]
        B = B + ["val_B" + str(i)]
        C = C + ["val_C" + str(i)]
        i = i + 1
    Dk = []
    Dv = []
    j = 0
    while j < n_distract:
        Dk = Dk + ["key_D" + str(j)]
        Dv = Dv + ["val_D" + str(j)]
        j = j + 1
    return [A, B, C, Dk, Dv]


def _cls_score_one(st, A, B):
    correct = 0
    i = 0
    while i < len(A):
        pred = _cls_recall_value(st, _cls_key16(A[i]))
        if pred == B[i]:
            correct = correct + 1
        i = i + 1
    if len(A) == 0:
        return 0.0
    return (correct + 0.0) / (len(A) + 0.0)


def _cls_score_two(fast, slow, A, B):
    correct = 0
    i = 0
    while i < len(A):
        pf = _cls_recall_value(fast, _cls_key16(A[i]))
        ps = _cls_recall_value(slow, _cls_key16(A[i]))
        if pf == B[i] or ps == B[i]:
            correct = correct + 1
        i = i + 1
    if len(A) == 0:
        return 0.0
    return (correct + 0.0) / (len(A) + 0.0)


def _cls_coin(text):
    blen = len(text.encode("utf-8"))
    bs = list(text.encode("utf-8"))
    return _immune_fnv1a(bs) & 1


def cls_one_store_retention(n_pairs, n_distract, max_cells, split_thr, abstain):
    """engine_cli.hexa:1597."""
    fx = _cls_make_abac(n_pairs, n_distract)
    A, B, C, Dk, Dv = fx[0], fx[1], fx[2], fx[3], fx[4]
    st = _cls_store_new(max_cells, abstain, split_thr)
    i = 0
    while i < len(A):
        st = _cls_write(st, _cls_key16(A[i]), B[i], False)
        i = i + 1
    j = 0
    while j < len(A):
        st = _cls_write(st, _cls_key16(A[j]), C[j], False)
        j = j + 1
    k = 0
    while k < len(Dk):
        st = _cls_write(st, _cls_key16(Dk[k]), Dv[k], False)
        k = k + 1
    return _cls_score_one(st, A, B)


def cls_two_store_retention(n_pairs, n_distract, max_cells, split_thr, abstain,
                            merge, shuffle):
    """engine_cli.hexa:1624."""
    fx = _cls_make_abac(n_pairs, n_distract)
    A, B, C, Dk, Dv = fx[0], fx[1], fx[2], fx[3], fx[4]
    if merge:
        m = _cls_store_new(max_cells, abstain, split_thr)
        a = 0
        while a < len(A):
            m = _cls_write(m, _cls_key16(A[a]), B[a], False)
            a = a + 1
        b = 0
        while b < len(A):
            m = _cls_write(m, _cls_key16(A[b]), C[b], False)
            b = b + 1
        c = 0
        while c < len(Dk):
            m = _cls_write(m, _cls_key16(Dk[c]), Dv[c], False)
            c = c + 1
        return _cls_score_one(m, A, B)
    fast = _cls_store_new(max_cells, abstain, split_thr)
    slow = _cls_store_new(max_cells, abstain, split_thr)
    i = 0
    while i < len(A):
        key = _cls_key16(A[i])
        to_fast = (_cls_coin(A[i]) == 0) if shuffle else True
        if to_fast:
            fast = _cls_write(fast, key, B[i], True)
        else:
            slow = _cls_write(slow, key, B[i], False)
        i = i + 1
    j = 0
    while j < len(A):
        key = _cls_key16(A[j])
        to_fast = (_cls_coin(A[j]) == 0) if shuffle else False
        if to_fast:
            fast = _cls_write(fast, key, C[j], False)
        else:
            slow = _cls_write(slow, key, C[j], False)
        j = j + 1
    k = 0
    while k < len(Dk):
        key = _cls_key16(Dk[k])
        to_fast = (_cls_coin(Dk[k]) == 0) if shuffle else False
        if to_fast:
            fast = _cls_write(fast, key, Dv[k], False)
        else:
            slow = _cls_write(slow, key, Dv[k], False)
        k = k + 1
    if not shuffle:
        r = 0
        while r < len(A):
            key = _cls_key16(A[r])
            vv = _cls_recall_value(fast, key)
            if vv != "":
                slow = _cls_write(slow, key, vv, True)
            r = r + 1
    return _cls_score_two(fast, slow, A, B)


def cls_single_encode_retention(n_pairs, n_distract, max_cells, split_thr, abstain):
    """engine_cli.hexa:1707."""
    fx = _cls_make_abac(n_pairs, n_distract)
    A, B, C, Dk, Dv = fx[0], fx[1], fx[2], fx[3], fx[4]
    st = _cls_store_new(max_cells, abstain, split_thr)
    i = 0
    while i < len(A):
        st = _cls_write(st, _cls_key16(A[i]), B[i], True)
        i = i + 1
    j = 0
    while j < len(A):
        st = _cls_write(st, _cls_key16(A[j]), C[j], True)
        j = j + 1
    k = 0
    while k < len(Dk):
        st = _cls_write(st, _cls_key16(Dk[k]), Dv[k], True)
        k = k + 1
    return _cls_score_one(st, A, B)


# ════════════════════════════════════════════════════════════════════════
# SkillStore (§SkillStore, H_1378) — tool selection that learns via mitosis
# engine_cli.hexa:1764-1843
# ════════════════════════════════════════════════════════════════════════

class SkillStore:
    __slots__ = ("protos", "tool", "n_cells", "max_cells", "recall_thr")

    def __init__(self, protos, tool, n_cells, max_cells, recall_thr):
        self.protos = protos
        self.tool = tool
        self.n_cells = n_cells
        self.max_cells = max_cells
        self.recall_thr = recall_thr


def skill_store_new(first_task, first_tool, max_cells):
    return SkillStore([immune_embed_key(first_task)], [first_tool], 1,
                      max_cells, 0.55)


def skill_recall(store, task):
    key = immune_embed_key(task)
    win = _vnearest_idx(store.protos, key)
    err = _l2(store.protos[win], key)
    if err <= store.recall_thr:
        return store.tool[win]
    return ""


def skill_store_split(store, task, tool, cfg):
    if store.n_cells >= store.max_cells:
        return store
    grown = engine_mitosis_tick(store.n_cells, cfg)
    if grown > store.n_cells:
        return SkillStore(store.protos + [immune_embed_key(task)],
                          store.tool + [tool], grown, store.max_cells,
                          store.recall_thr)
    return store


def skill_store_teach(store, task, correct_tool, cfg):
    selected = skill_recall(store, task)
    if selected == correct_tool:
        return store
    return skill_store_split(store, task, correct_tool, cfg)


def skill_store_cells(store):
    return store.n_cells


# ════════════════════════════════════════════════════════════════════════
# UsageStore (§UsageStore, H_1391) — tool-usage learning (twin of SkillStore)
# engine_cli.hexa:1884-1984
# ════════════════════════════════════════════════════════════════════════

class UsageStore:
    __slots__ = ("protos", "arg", "steps", "n_cells", "max_cells", "recall_thr")

    def __init__(self, protos, arg, steps, n_cells, max_cells, recall_thr):
        self.protos = protos
        self.arg = arg
        self.steps = steps
        self.n_cells = n_cells
        self.max_cells = max_cells
        self.recall_thr = recall_thr


def _usage_key(ctx, tool, observed_err):
    return ctx + "|" + tool + "|" + observed_err


def usage_store_new(first_ctx, first_tool, first_err, first_arg, first_steps, max_cells):
    return UsageStore([immune_embed_key(_usage_key(first_ctx, first_tool, first_err))],
                      [first_arg], [first_steps], 1, max_cells, 0.55)


def usage_recall(store, ctx, tool, observed_err):
    key = immune_embed_key(_usage_key(ctx, tool, observed_err))
    win = _vnearest_idx(store.protos, key)
    err = _l2(store.protos[win], key)
    if err <= store.recall_thr:
        return store.arg[win]
    return ""


def usage_recall_steps(store, ctx, tool, observed_err):
    key = immune_embed_key(_usage_key(ctx, tool, observed_err))
    win = _vnearest_idx(store.protos, key)
    err = _l2(store.protos[win], key)
    if err <= store.recall_thr:
        return store.steps[win]
    return ""


def usage_store_split(store, ctx, tool, observed_err, arg, steps, cfg):
    if store.n_cells >= store.max_cells:
        return store
    grown = engine_mitosis_tick(store.n_cells, cfg)
    if grown > store.n_cells:
        return UsageStore(
            store.protos + [immune_embed_key(_usage_key(ctx, tool, observed_err))],
            store.arg + [arg], store.steps + [steps], grown, store.max_cells,
            store.recall_thr)
    return store


def usage_store_teach(store, ctx, tool, observed_err, correct_arg, correct_steps, cfg):
    proposed = usage_recall(store, ctx, tool, observed_err)
    if proposed == correct_arg:
        return store
    return usage_store_split(store, ctx, tool, observed_err, correct_arg, correct_steps, cfg)


def usage_store_cells(store):
    return store.n_cells


# ════════════════════════════════════════════════════════════════════════
# shared deterministic LCG helpers (engine_cli.hexa:719/2449-helpers)
# ════════════════════════════════════════════════════════════════════════

def _lcg_next(state):
    """engine_cli.hexa:_lcg_next — 31-bit LCG step."""
    return (state * 1103515245 + 12345) & 2147483647


def _mi_set(v, ix, val):
    """engine_cli.hexa — functional [float] element set (returns a new list)."""
    out = []
    i = 0
    while i < len(v):
        if i == ix:
            out = out + [val]
        else:
            out = out + [v[i]]
        i = i + 1
    return out


def _lcg_unit(state):
    """engine_cli.hexa:_lcg_unit — [0,1) draw from a 31-bit LCG state."""
    return float(state) / 2147483648.0


def _lcg_gauss(state0):
    """engine_cli.hexa:_lcg_gauss — Box-Muller gaussian (ln/cos/sqrt=libm)."""
    s1 = _lcg_next(state0)
    s2 = _lcg_next(s1)
    u1 = _lcg_unit(s1)
    u2 = _lcg_unit(s2)
    if u1 < 0.0000001:
        u1 = 0.0000001
    r = _sqrt(-2.0 * _ln(u1))
    z = r * _cos(6.283185307179586 * u2)
    return [z, float(s2)]


def _cos_vec(a, b):
    """engine_cli.hexa:3428 _cos — cosine similarity of two DIM-vectors."""
    n = len(a)
    dot = 0.0
    na = 0.0
    nb = 0.0
    i = 0
    while i < n:
        dot = dot + a[i] * b[i]
        na = na + a[i] * a[i]
        nb = nb + b[i] * b[i]
        i = i + 1
    denom = _sqrt(na) * _sqrt(nb) + 0.000000000001
    return dot / denom


# ════════════════════════════════════════════════════════════════════════
# OtherMindModel (§ToM H_1293) — other-agent belief store (false belief)
# engine_cli.hexa:2598-2649
# ════════════════════════════════════════════════════════════════════════

class OtherMindModel:
    __slots__ = ("protos", "bel_value", "n_bel", "recall_thr")

    def __init__(self, protos, bel_value, n_bel, recall_thr):
        self.protos = protos
        self.bel_value = bel_value
        self.n_bel = n_bel
        self.recall_thr = recall_thr


def other_mind_new():
    return OtherMindModel([], [], 0, 0.30)


def other_mind_witness(om, fact_text, value):
    """engine_cli.hexa:2615."""
    key = immune_embed_key(fact_text)
    if om.n_bel > 0:
        w = _vnearest_idx(om.protos, key)
        if _l2(om.protos[w], key) <= 0.000001:
            nv = list(om.bel_value)
            nv[w] = value
            return OtherMindModel(om.protos, nv, om.n_bel, om.recall_thr)
    return OtherMindModel(om.protos + [key], om.bel_value + [value],
                          om.n_bel + 1, om.recall_thr)


def other_mind_predict(om, fact_text):
    """engine_cli.hexa:2640."""
    if om.n_bel == 0:
        return ""
    key = immune_embed_key(fact_text)
    w = _vnearest_idx(om.protos, key)
    if _l2(om.protos[w], key) > om.recall_thr:
        return ""
    return om.bel_value[w]


def other_mind_count(om):
    return om.n_bel


# ════════════════════════════════════════════════════════════════════════
# ConsolidatingMemory (§SleepReplay H_1228 R3) — salience-gated sleep replay
# engine_cli.hexa:3015-3234
# ════════════════════════════════════════════════════════════════════════

class ConsolidatingMemory:
    __slots__ = ("protos", "cell_value", "last_used", "salience", "n_cells",
                 "max_cells", "recall_thr", "split_thr", "tick")

    def __init__(self, protos, cell_value, last_used, salience, n_cells,
                 max_cells, recall_thr, split_thr, tick):
        self.protos = protos
        self.cell_value = cell_value
        self.last_used = last_used
        self.salience = salience
        self.n_cells = n_cells
        self.max_cells = max_cells
        self.recall_thr = recall_thr
        self.split_thr = split_thr
        self.tick = tick


def consolidating_memory_new(first_key, first_value, first_salience, max_cells):
    return ConsolidatingMemory([list(first_key)], [first_value], [1],
                               [first_salience], 1, max_cells, 0.30, 0.30, 1)


def consolidating_memory_bind_salient(mem, key, value, salient_boost, cfg):
    """engine_cli.hexa:3053."""
    SURPRISE_W = 1.0
    NOVELTY_W = 0.5
    TENSION_W = 0.5
    LR = 0.20
    t = mem.tick + 1
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    was_split = (err > mem.split_thr)
    surprise = err
    if surprise > 1.0:
        surprise = 1.0
    surprise = surprise + salient_boost
    if surprise > 2.0:
        surprise = 2.0
    if was_split and mem.n_cells < mem.max_cells:
        grown = engine_mitosis_tick(mem.n_cells, cfg)
        if grown > mem.n_cells:
            novelty = 1.0
            tag = SURPRISE_W * surprise + NOVELTY_W * novelty
            return ConsolidatingMemory(mem.protos + [list(key)],
                                       mem.cell_value + [value],
                                       mem.last_used + [t], mem.salience + [tag],
                                       grown, mem.max_cells, mem.recall_thr,
                                       mem.split_thr, t)
    if was_split:
        v = _immune_grow_lru_victim(mem.last_used)
        novelty = 1.0
        tag = SURPRISE_W * surprise + NOVELTY_W * novelty
        p3 = list(mem.protos)
        p3[v] = list(key)
        nv = list(mem.cell_value)
        nv[v] = value
        lu = list(mem.last_used)
        lu[v] = t
        sal = list(mem.salience)
        sal[v] = tag
        return ConsolidatingMemory(p3, nv, lu, sal, mem.n_cells, mem.max_cells,
                                   mem.recall_thr, mem.split_thr, t)
    p2 = list(mem.protos)
    row = list(p2[win])
    d = 0
    while d < len(row):
        row[d] = row[d] + LR * (key[d] - row[d])
        d = d + 1
    p2[win] = row
    nv2 = list(mem.cell_value)
    nv2[win] = value
    lu2 = list(mem.last_used)
    lu2[win] = t
    sal2 = list(mem.salience)
    sal2[win] = sal2[win] + TENSION_W
    return ConsolidatingMemory(p2, nv2, lu2, sal2, mem.n_cells, mem.max_cells,
                               mem.recall_thr, mem.split_thr, t)


def consolidating_shuffle_salience(mem, rng0):
    """engine_cli.hexa:3138."""
    n = mem.n_cells
    sal = list(mem.salience)
    st = rng0
    i = n - 1
    while i > 0:
        st = _lcg_next(st)
        j = st % (i + 1)
        tmp = sal[i]
        sal[i] = sal[j]
        sal[j] = tmp
        i = i - 1
    return ConsolidatingMemory(mem.protos, mem.cell_value, mem.last_used, sal,
                               mem.n_cells, mem.max_cells, mem.recall_thr,
                               mem.split_thr, mem.tick)


def consolidating_sleep_replay(mem, budget, rng0, salience_gated):
    """engine_cli.hexa:3166."""
    n = mem.n_cells
    if n == 0:
        return mem
    cdf = []
    acc = 0.0
    k = 0
    while k < n:
        w = 1.0
        if salience_gated:
            w = mem.salience[k]
            if w < 0.000001:
                w = 0.000001
        acc = acc + w
        cdf = cdf + [acc]
        k = k + 1
    lu = list(mem.last_used)
    t = mem.tick
    st = rng0
    b = 0
    while b < budget:
        st = _lcg_next(st)
        target = _lcg_unit(st) * acc
        pick = 0
        while pick < n - 1:
            if cdf[pick] > target:
                break
            pick = pick + 1
        t = t + 1
        lu[pick] = t
        b = b + 1
    return ConsolidatingMemory(mem.protos, mem.cell_value, lu, mem.salience,
                               mem.n_cells, mem.max_cells, mem.recall_thr,
                               mem.split_thr, t)


def consolidating_memory_recall(mem, key):
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    if err <= mem.recall_thr:
        return mem.cell_value[win]
    return ""


def consolidating_memory_cells(mem):
    return mem.n_cells


def consolidating_memory_salience(mem, i):
    return mem.salience[i]


def consolidating_lcg_next(state):
    return _lcg_next(state)


def consolidating_lcg_gauss(state0):
    return _lcg_gauss(state0)


# ════════════════════════════════════════════════════════════════════════
# VAdaptFieldB (§GateB H_1208) — transition-predictability split (order vs shuffle)
# engine_cli.hexa:3264-3343
# ════════════════════════════════════════════════════════════════════════

class VAdaptFieldB:
    __slots__ = ("n_proto", "n_cells", "max_cells", "min_prev", "conf_floor",
                 "last_id", "ctab", "prev_total")

    def __init__(self, n_proto, n_cells, max_cells, min_prev, conf_floor,
                 last_id, ctab, prev_total):
        self.n_proto = n_proto
        self.n_cells = n_cells
        self.max_cells = max_cells
        self.min_prev = min_prev
        self.conf_floor = conf_floor
        self.last_id = last_id
        self.ctab = ctab
        self.prev_total = prev_total


def vadapt_fieldB_new(n_proto, max_cells, min_prev, conf_floor):
    ctab = []
    i = 0
    while i < n_proto * n_proto:
        ctab = ctab + [0]
        i = i + 1
    pt = []
    j = 0
    while j < n_proto:
        pt = pt + [0]
        j = j + 1
    return VAdaptFieldB(n_proto, 1, max_cells, min_prev, conf_floor, -1, ctab, pt)


def vadapt_fieldB_step(afB, cur, cfg):
    """engine_cli.hexa:3306."""
    np_ = afB.n_proto
    cells = afB.n_cells
    prev = afB.last_id
    if prev >= 0:
        tot = afB.prev_total[prev]
        if tot >= afB.min_prev:
            cnt = afB.ctab[prev * np_ + cur]
            p_cur = float(cnt) / float(tot)
            if p_cur >= afB.conf_floor and cells < afB.max_cells:
                grown = engine_mitosis_tick(cells, cfg)
                if grown > cells:
                    cells = grown
    ct = list(afB.ctab)
    pt = list(afB.prev_total)
    if prev >= 0:
        ct[prev * np_ + cur] = ct[prev * np_ + cur] + 1
        pt[prev] = pt[prev] + 1
    return VAdaptFieldB(np_, cells, afB.max_cells, afB.min_prev, afB.conf_floor,
                        cur, ct, pt)


def vadapt_fieldB_cells(afB):
    return afB.n_cells


def vadapt_fieldB_growth(afB):
    return afB.n_cells - 1


# ════════════════════════════════════════════════════════════════════════
# WorkMemBuffer (§WorkMem H_1282) — gated leaky-activation PFC working memory
# engine_cli.hexa:3407-3564
# ════════════════════════════════════════════════════════════════════════

class WorkMemBuffer:
    __slots__ = ("keys", "act", "n_slots", "k", "lam", "dg", "dim")

    def __init__(self, keys, act, n_slots, k, lam, dg, dim):
        self.keys = keys
        self.act = act
        self.n_slots = n_slots
        self.k = k
        self.lam = lam
        self.dg = dg
        self.dim = dim


def wm_buffer_new(k, lam, dg, dim):
    return WorkMemBuffer([], [], 0, k, lam, dg, dim)


def _wm_argmin_act(act):
    n = len(act)
    best = 0
    bestv = act[0]
    i = 1
    while i < n:
        if act[i] < bestv:
            bestv = act[i]
            best = i
        i = i + 1
    return best


def wm_buffer_gate_in(wm, tok, strength):
    """engine_cli.hexa:3469."""
    keys = list(wm.keys)
    act = list(wm.act)
    i = 0
    while i < wm.n_slots:
        if _cos_vec(keys[i], tok) >= 0.9:
            act[i] = max(act[i], strength)
            keys[i] = tok
            return WorkMemBuffer(keys, act, wm.n_slots, wm.k, wm.lam, wm.dg, wm.dim)
        i = i + 1
    if wm.n_slots < wm.k:
        keys = keys + [tok]
        act = act + [strength]
        return WorkMemBuffer(keys, act, wm.n_slots + 1, wm.k, wm.lam, wm.dg, wm.dim)
    j = _wm_argmin_act(act)
    if strength > act[j]:
        keys[j] = tok
        act[j] = strength
    return WorkMemBuffer(keys, act, wm.n_slots, wm.k, wm.lam, wm.dg, wm.dim)


def wm_buffer_leak(wm):
    act = list(wm.act)
    i = 0
    while i < wm.n_slots:
        act[i] = act[i] * wm.lam
        i = i + 1
    return WorkMemBuffer(wm.keys, act, wm.n_slots, wm.k, wm.lam, wm.dg, wm.dim)


def wm_buffer_distractor(wm, tok):
    leaked = wm_buffer_leak(wm)
    return wm_buffer_gate_in(leaked, tok, leaked.dg)


def wm_buffer_probe_score(wm, probe):
    """engine_cli.hexa:3532."""
    if wm.n_slots == 0:
        return 0.0
    best = 0.0
    i = 0
    while i < wm.n_slots:
        c = _cos_vec(wm.keys[i], probe)
        cc = c if c > 0.0 else 0.0
        s = wm.act[i] * cc
        if s > best:
            best = s
        i = i + 1
    return best


def wm_buffer_slots(wm):
    return wm.n_slots


def wm_buffer_total_activation(wm):
    s = 0.0
    i = 0
    while i < wm.n_slots:
        s = s + wm.act[i]
        i = i + 1
    return s


# ════════════════════════════════════════════════════════════════════════
# VForwardField (§Cerebellum H_1280) — NLMS delta-rule forward model
# engine_cli.hexa:3603-3704
# ════════════════════════════════════════════════════════════════════════

class VForwardField:
    __slots__ = ("w", "dim", "ctx_len", "ctx_dim", "eta")

    def __init__(self, w, dim, ctx_len, ctx_dim, eta):
        self.w = w
        self.dim = dim
        self.ctx_len = ctx_len
        self.ctx_dim = ctx_dim
        self.eta = eta


def vforward_new(dim, ctx_len, eta):
    ctx_dim = ctx_len * dim
    w = []
    i = 0
    while i < dim * ctx_dim:
        w = w + [0.0]
        i = i + 1
    return VForwardField(w, dim, ctx_len, ctx_dim, eta)


def vforward_predict(ff, ctx):
    xhat = []
    r = 0
    while r < ff.dim:
        base = r * ff.ctx_dim
        acc = 0.0
        c = 0
        while c < ff.ctx_dim:
            acc = acc + ff.w[base + c] * ctx[c]
            c = c + 1
        xhat = xhat + [acc]
        r = r + 1
    return xhat


def vforward_err(ff, ctx, x):
    xhat = vforward_predict(ff, ctx)
    s = 0.0
    i = 0
    while i < ff.dim:
        e = x[i] - xhat[i]
        s = s + e * e
        i = i + 1
    return s


def vforward_update(ff, ctx, x):
    """engine_cli.hexa:3666 — NLMS delta rule W += eta*outer(e,ctx)/(ctx·ctx+1)."""
    xhat = vforward_predict(ff, ctx)
    denom = 1.0
    c0 = 0
    while c0 < ff.ctx_dim:
        denom = denom + ctx[c0] * ctx[c0]
        c0 = c0 + 1
    scale = ff.eta / denom
    w2 = list(ff.w)
    r = 0
    while r < ff.dim:
        e = x[r] - xhat[r]
        ge = scale * e
        base = r * ff.ctx_dim
        c = 0
        while c < ff.ctx_dim:
            w2[base + c] = w2[base + c] + ge * ctx[c]
            c = c + 1
        r = r + 1
    return VForwardField(w2, ff.dim, ff.ctx_len, ff.ctx_dim, ff.eta)


def vforward_correct(x, xhat, beta):
    n = len(x)
    out = []
    i = 0
    while i < n:
        out = out + [x[i] - beta * (x[i] - xhat[i])]
        i = i + 1
    return out


# ════════════════════════════════════════════════════════════════════════
# HierGoalStack (§HierPFC H_1294) — 2-level goal→subgoal pointer controller
# engine_cli.hexa:3757-3842
# ════════════════════════════════════════════════════════════════════════

def _cos_hier(a, b):
    """engine_cli.hexa:3770 — cosine, 0 if either vector degenerate (no epsilon)."""
    n = len(a)
    dot = 0.0
    na = 0.0
    nb = 0.0
    i = 0
    while i < n:
        dot = dot + a[i] * b[i]
        na = na + a[i] * a[i]
        nb = nb + b[i] * b[i]
        i = i + 1
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / (_sqrt(na) * _sqrt(nb))


class HierGoalStack:
    __slots__ = ("sub_keys", "n_sub", "p", "align_thr")

    def __init__(self, sub_keys, n_sub, p, align_thr):
        self.sub_keys = sub_keys
        self.n_sub = n_sub
        self.p = p
        self.align_thr = align_thr


def hier_new(sub_keys):
    return HierGoalStack(sub_keys, len(sub_keys), 0, 0.85)


def hier_current_target(hs):
    if hs.p >= hs.n_sub:
        return []
    return hs.sub_keys[hs.p]


def hier_grounded_current(hs, mem, cue):
    """engine_cli.hexa:3796."""
    if hs.p >= hs.n_sub:
        return False
    win = _vnearest_idx(mem.protos, cue)
    err = _l2(mem.protos[win], cue)
    if err > mem.recall_thr:
        return False
    return _cos_hier(cue, hs.sub_keys[hs.p]) >= hs.align_thr


def hier_step(hs, mem, cue):
    if hier_grounded_current(hs, mem, cue):
        return HierGoalStack(hs.sub_keys, hs.n_sub, hs.p + 1, hs.align_thr)
    return hs


def hier_pointer(hs):
    return hs.p


def hier_complete(hs):
    return hs.p >= hs.n_sub


def hier_flat_emit(mem, window):
    """engine_cli.hexa:3826."""
    n = len(window)
    best = -1
    best_margin = 0.0
    i = 0
    while i < n:
        win = _vnearest_idx(mem.protos, window[i])
        err = _l2(mem.protos[win], window[i])
        m = 1.0 - err / mem.recall_thr
        if err <= mem.recall_thr and m > best_margin:
            best_margin = m
            best = i
        i = i + 1
    return best


# ════════════════════════════════════════════════════════════════════════
# SpatialMap (§PlaceGrid H_1295/1296) — metric cognitive map (relational query)
# engine_cli.hexa:3886-3991
# ════════════════════════════════════════════════════════════════════════

class SpatialMap:
    __slots__ = ("names", "xs", "ys", "n", "ablate")

    def __init__(self, names, xs, ys, n, ablate):
        self.names = names
        self.xs = xs
        self.ys = ys
        self.n = n
        self.ablate = ablate


def spatial_map_new():
    return SpatialMap([], [], [], 0, False)


def spatial_map_new_ablated():
    return SpatialMap([], [], [], 0, True)


def spatial_map_place(sm, name, x, y):
    px = 0.0 if sm.ablate else x
    py = 0.0 if sm.ablate else y
    return SpatialMap(sm.names + [name], sm.xs + [px], sm.ys + [py],
                      sm.n + 1, sm.ablate)


def _sm_idx(sm, name):
    i = 0
    while i < sm.n:
        if sm.names[i] == name:
            return i
        i = i + 1
    return -1


def _sm_dist(sm, i, j):
    dx = sm.xs[i] - sm.xs[j]
    dy = sm.ys[i] - sm.ys[j]
    return _sqrt(dx * dx + dy * dy)


def spatial_map_count(sm):
    return sm.n


def spatial_map_nearest(sm, x, a, b):
    """engine_cli.hexa:3942."""
    ix = _sm_idx(sm, x)
    ia = _sm_idx(sm, a)
    ib = _sm_idx(sm, b)
    if ix < 0 or ia < 0 or ib < 0:
        return ""
    da = _sm_dist(sm, ix, ia)
    db = _sm_dist(sm, ix, ib)
    if da < db:
        return a
    return b


def spatial_map_shuffle(sm, seed):
    """engine_cli.hexa:3957 — LCG Fisher-Yates over coordinate columns (% 2^31)."""
    perm = []
    q = 0
    while q < sm.n:
        perm = perm + [q]
        q = q + 1
    s = seed
    i = sm.n - 1
    while i > 0:
        s = (s * 1103515245 + 12345) % 2147483648
        j = s % (i + 1)
        tmp = perm[i]
        perm[i] = perm[j]
        perm[j] = tmp
        i = i - 1
    nxs = []
    nys = []
    k = 0
    while k < sm.n:
        nxs = nxs + [sm.xs[perm[k]]]
        nys = nys + [sm.ys[perm[k]]]
        k = k + 1
    return SpatialMap(sm.names, nxs, nys, sm.n, sm.ablate)


def spatial_map_item_nearest(x, a, b):
    return ""


# ════════════════════════════════════════════════════════════════════════
# TransOrder (§TransitiveInf H_1429) — adjacent-premise rank integration
# engine_cli.hexa:4045-4185
# ════════════════════════════════════════════════════════════════════════

class TransOrder:
    __slots__ = ("items", "hi", "lo", "rank", "n_items", "n_prem", "ablate")

    def __init__(self, items, hi, lo, rank, n_items, n_prem, ablate):
        self.items = items
        self.hi = hi
        self.lo = lo
        self.rank = rank
        self.n_items = n_items
        self.n_prem = n_prem
        self.ablate = ablate


def trans_order_new():
    return TransOrder([], [], [], [], 0, 0, False)


def trans_order_new_ablated():
    return TransOrder([], [], [], [], 0, 0, True)


def _to_idx(to, name):
    i = 0
    while i < to.n_items:
        if to.items[i] == name:
            return i
        i = i + 1
    return -1


def trans_order_premise(to, higher, lower):
    """engine_cli.hexa:4078."""
    items = list(to.items)
    if _to_idx(to, higher) < 0:
        items = items + [higher]
    to1 = TransOrder(items, to.hi, to.lo, to.rank, len(items), to.n_prem, to.ablate)
    items2 = list(to1.items)
    if _to_idx(to1, lower) < 0:
        items2 = items2 + [lower]
    return TransOrder(items2, to1.hi + [higher], to1.lo + [lower], to1.rank,
                      len(items2), to1.n_prem + 1, to1.ablate)


def trans_order_integrate(to):
    """engine_cli.hexa:4095 — Trabasso relaxation into a latent 1-D rank."""
    if to.ablate:
        return to
    rank = []
    z = 0
    while z < to.n_items:
        rank = rank + [0.0]
        z = z + 1
    it = 0
    while it < 200:
        moved = False
        k = 0
        while k < to.n_prem:
            ih = _to_idx(to, to.hi[k])
            il = _to_idx(to, to.lo[k])
            if rank[ih] >= rank[il]:
                mid = (rank[ih] + rank[il]) / 2.0
                rank[ih] = mid - 0.5
                rank[il] = mid + 0.5
                moved = True
            k = k + 1
        if not moved:
            it = 200
        else:
            it = it + 1
    return TransOrder(to.items, to.hi, to.lo, rank, to.n_items, to.n_prem, to.ablate)


def _to_observed_higher(to, x, y):
    k = 0
    while k < to.n_prem:
        if to.hi[k] == x and to.lo[k] == y:
            return x
        if to.hi[k] == y and to.lo[k] == x:
            return y
        k = k + 1
    return ""


def trans_order_higher(to, x, y):
    """engine_cli.hexa:4138."""
    ix = _to_idx(to, x)
    iy = _to_idx(to, y)
    if ix < 0 or iy < 0:
        return ""
    if to.ablate:
        return _to_observed_higher(to, x, y)
    if to.rank[ix] < to.rank[iy]:
        return x
    if to.rank[iy] < to.rank[ix]:
        return y
    return ""


def trans_order_item_higher(to, x, y):
    ix = _to_idx(to, x)
    iy = _to_idx(to, y)
    if ix < 0 or iy < 0:
        return ""
    return _to_observed_higher(to, x, y)


def trans_order_shuffle(to, seed):
    """engine_cli.hexa:4164 — LCG-flip a subset of premise directions (% 2^31)."""
    nhi = []
    nlo = []
    s = seed
    k = 0
    while k < to.n_prem:
        s = (s * 1103515245 + 12345) % 2147483648
        if (s // 65536) % 2 == 0:
            nhi = nhi + [to.lo[k]]
            nlo = nlo + [to.hi[k]]
        else:
            nhi = nhi + [to.hi[k]]
            nlo = nlo + [to.lo[k]]
        k = k + 1
    return TransOrder(to.items, nhi, nlo, [], to.n_items, to.n_prem, to.ablate)


def trans_order_count(to):
    return to.n_items


# ════════════════════════════════════════════════════════════════════════
# CircadianClock (§Circadian H_1298) — content-blind phase oscillator
# engine_cli.hexa:4234-4277
# ════════════════════════════════════════════════════════════════════════

class CircadianClock:
    __slots__ = ("t", "period", "offset")

    def __init__(self, t, period, offset):
        self.t = t
        self.period = period
        self.offset = offset


def clock_new():
    return CircadianClock(0, 8, 0)


def clock_new_ablated():
    return CircadianClock(0, 5, 3)


def clock_step(c):
    return CircadianClock(c.t + 1, c.period, c.offset)


def clock_count(c):
    return c.t


def clock_phase(c):
    m = c.t % c.period
    return float(m) / float(c.period)


def clock_fire(c):
    if c.t < c.offset:
        return False
    return ((c.t - c.offset) % c.period) == 0


# ════════════════════════════════════════════════════════════════════════
# IntervalTimer (§IntervalTiming H_1299) — learned-duration timer
# engine_cli.hexa:4328-4387
# ════════════════════════════════════════════════════════════════════════

class IntervalTimer:
    __slots__ = ("elapsed", "t_last", "dhat", "lr")

    def __init__(self, elapsed, t_last, dhat, lr):
        self.elapsed = elapsed
        self.t_last = t_last
        self.dhat = dhat
        self.lr = lr


def itimer_new():
    return IntervalTimer(0, -1, 5.0, 0.5)


def itimer_new_ablated():
    return IntervalTimer(0, -1, 5.0, 0.0)


def itimer_observe(it, t):
    if it.t_last < 0:
        return IntervalTimer(0, t, it.dhat, it.lr)
    gap = float(t - it.t_last)
    nd = (1.0 - it.lr) * it.dhat + it.lr * gap
    return IntervalTimer(0, t, nd, it.lr)


def itimer_step(it):
    return IntervalTimer(it.elapsed + 1, it.t_last, it.dhat, it.lr)


def itimer_dhat(it):
    return it.dhat


def itimer_dhat_ticks(it):
    return int(it.dhat + 0.5)


def itimer_predict_next(it):
    if it.t_last < 0:
        return -1
    return it.t_last + int(it.dhat + 0.5)


def itimer_fire(it):
    return it.elapsed == int(it.dhat + 0.5)


# ════════════════════════════════════════════════════════════════════════
# PhaseResetClock (§PhaseReset H_1301) — Zeitgeber PRC entrainment (sin)
# engine_cli.hexa:4439-4499
# ════════════════════════════════════════════════════════════════════════

class PhaseResetClock:
    __slots__ = ("phi", "tau", "k")

    def __init__(self, phi, tau, k):
        self.phi = phi
        self.tau = tau
        self.k = k


def _prc_frac(phi):
    return phi - float(int(phi))


def _prc_floor(phi):
    return int(phi)


def prc_new():
    return PhaseResetClock(0.0, 24.5, 0.18)


def prc_new_ablated():
    return PhaseResetClock(0.0, 24.5, 0.0)


def prc_step(c, dt):
    return PhaseResetClock(c.phi + dt / c.tau, c.tau, c.k)


def prc_zeitgeber(c):
    two_pi = 6.283185307179586
    frac = _prc_frac(c.phi)
    dphi = c.k * _sin(two_pi * (0.0 - frac))
    return PhaseResetClock(c.phi + dphi, c.tau, c.k)


def prc_phase(c):
    return _prc_frac(c.phi)


def prc_count(c):
    return _prc_floor(c.phi)


def prc_fire(c):
    f = _prc_frac(c.phi)
    eps = 0.02
    return (f < eps) or (f > (1.0 - eps))


# ════════════════════════════════════════════════════════════════════════
# SCNNetwork (§SCN H_1302) — coupled Kuramoto ensemble (sin/cos/sqrt)
# engine_cli.hexa:4549-4700
# ════════════════════════════════════════════════════════════════════════

_SCN_TWO_PI = 6.283185307179586


class SCNNetwork:
    __slots__ = ("phases", "taus", "k", "mode", "n")

    def __init__(self, phases, taus, k, mode, n):
        self.phases = phases
        self.taus = taus
        self.k = k
        self.mode = mode
        self.n = n


def _scn_taus(seed, n, mean, spread):
    taus = []
    x = (seed * 2654435761 + 12345) % 4294967296
    if x < 0:
        x = x + 4294967296
    i = 0
    while i < n:
        x = (1103515245 * x + 12345) % 2147483648
        if x < 0:
            x = x + 2147483648
        u = float(x) / 2147483647.0
        taus = taus + [mean + spread * (2.0 * u - 1.0)]
        i = i + 1
    return taus


def _scn_init_phases(n):
    p = []
    i = 0
    while i < n:
        p = p + [float(i) / float(n)]
        i = i + 1
    return p


def _scn_coupling(mode, i, j, n):
    if i == j:
        return 0.0
    base = 1.0 / float(n - 1)
    if mode == 0:
        return 0.0
    if mode == 1:
        return base
    a = i
    b = j
    if a > b:
        a = j
        b = i
    h = (a * 73856093 + b * 19349663 + 83492791) % 2
    if h == 0:
        return 0.0 - base
    return base


def scn_new(seed, n):
    return SCNNetwork(_scn_init_phases(n), _scn_taus(seed, n, 24.0, 2.0), 0.25, 1, n)


def scn_new_uncoupled(seed, n):
    return SCNNetwork(_scn_init_phases(n), _scn_taus(seed, n, 24.0, 2.0), 0.0, 0, n)


def scn_new_frustrated(seed, n):
    return SCNNetwork(_scn_init_phases(n), _scn_taus(seed, n, 24.0, 2.0), 0.25, -1, n)


def scn_new_ablated(seed, n):
    return SCNNetwork(_scn_init_phases(n), _scn_taus(seed, n, 24.0, 2.0), 0.0, 1, n)


def scn_detune(net, d):
    taus = []
    i = 0
    while i < net.n:
        if i == 0:
            taus = taus + [net.taus[0] + d]
        else:
            taus = taus + [net.taus[i]]
        i = i + 1
    return SCNNetwork(net.phases, taus, net.k, net.mode, net.n)


def scn_step(net):
    newp = []
    i = 0
    while i < net.n:
        dphi = 1.0 / net.taus[i]
        coup = 0.0
        j = 0
        while j < net.n:
            c = _scn_coupling(net.mode, i, j, net.n)
            if c != 0.0:
                coup = coup + c * _sin(_SCN_TWO_PI * (net.phases[j] - net.phases[i]))
            j = j + 1
        dphi = dphi + net.k * coup / _SCN_TWO_PI
        np_ = net.phases[i] + dphi
        np_ = np_ - float(int(np_))
        if np_ < 0.0:
            np_ = np_ + 1.0
        newp = newp + [np_]
        i = i + 1
    return SCNNetwork(newp, net.taus, net.k, net.mode, net.n)


def scn_run(net, steps):
    cur = net
    t = 0
    while t < steps:
        cur = scn_step(cur)
        t = t + 1
    return cur


def scn_order(net):
    cx = 0.0
    sy = 0.0
    i = 0
    while i < net.n:
        cx = cx + _cos(_SCN_TWO_PI * net.phases[i])
        sy = sy + _sin(_SCN_TWO_PI * net.phases[i])
        i = i + 1
    cx = cx / float(net.n)
    sy = sy / float(net.n)
    return _sqrt(cx * cx + sy * sy)


def scn_consensus(net, thr):
    return scn_order(net) >= thr


# ════════════════════════════════════════════════════════════════════════
# PhaseField (§PhaseSyncBinding H_1448) — Kuramoto pacemaker-star binding
# engine_cli.hexa:4740-4839
# ════════════════════════════════════════════════════════════════════════

_PF_TWO_PI = 6.283185307179586
_PF_OMEGA_T = 0.45
_PF_DOMEGA = 0.08


class PhaseField:
    __slots__ = ("theta", "theta_t", "omega", "k", "n")

    def __init__(self, theta, theta_t, omega, k, n):
        self.theta = theta
        self.theta_t = theta_t
        self.omega = omega
        self.k = k
        self.n = n


def _pf_init_theta(seed, n):
    th = []
    st = (seed * 2654435761) & 2147483647
    if st == 0:
        st = 12345
    i = 0
    while i < n:
        st = (st * 1103515245 + 12345) & 2147483647
        th = th + [(float(st) / 2147483648.0) * _PF_TWO_PI]
        i = i + 1
    return th


def _pf_init_theta_t(seed, n):
    st = (seed * 2654435761) & 2147483647
    if st == 0:
        st = 12345
    i = 0
    while i < n + 1:
        st = (st * 1103515245 + 12345) & 2147483647
        i = i + 1
    return (float(st) / 2147483648.0) * _PF_TWO_PI


def _pf_omega(n):
    om = []
    i = 0
    while i < n:
        om = om + [_PF_OMEGA_T + _PF_DOMEGA * (float(i) - (float(n) - 1.0) / 2.0)]
        i = i + 1
    return om


def phasefield_new(seed, n):
    return PhaseField(_pf_init_theta(seed, n), _pf_init_theta_t(seed, n),
                      _pf_omega(n), 0.5, n)


def phasefield_new_desync(seed, n):
    return PhaseField(_pf_init_theta(seed, n), _pf_init_theta_t(seed, n),
                      _pf_omega(n), 0.0, n)


def phasefield_step(pf):
    newth = []
    i = 0
    while i < pf.n:
        newth = newth + [pf.theta[i] + (pf.omega[i] + pf.k * _sin(pf.theta_t - pf.theta[i]))]
        i = i + 1
    mp = 0.0
    i = 0
    while i < pf.n:
        mp = mp + _sin(pf.theta[i] - pf.theta_t)
        i = i + 1
    mp = mp / float(pf.n)
    ntt = pf.theta_t + (_PF_OMEGA_T + pf.k * mp)
    return PhaseField(newth, ntt, pf.omega, pf.k, pf.n)


def phasefield_run(pf, steps):
    cur = pf
    t = 0
    while t < steps:
        cur = phasefield_step(cur)
        t = t + 1
    return cur


def phasefield_coherence(pf):
    cx = 0.0
    sy = 0.0
    i = 0
    while i < pf.n:
        cx = cx + _cos(pf.theta[i])
        sy = sy + _sin(pf.theta[i])
        i = i + 1
    cx = cx / float(pf.n)
    sy = sy / float(pf.n)
    return _sqrt(cx * cx + sy * sy)


def phasefield_bound(pf, thr):
    return phasefield_coherence(pf) >= thr


# ════════════════════════════════════════════════════════════════════════
# QuorumPhase (§Quorum H_1510) — decentralized adjacency-weighted Kuramoto
# engine_cli.hexa:4865-5248
# ════════════════════════════════════════════════════════════════════════

_QP_CLUST_BAND = 0.15


class QuorumPhase:
    __slots__ = ("theta", "omega", "adj", "cid", "nc", "per")

    def __init__(self, theta, omega, adj, cid, nc, per):
        self.theta = theta
        self.omega = omega
        self.adj = adj
        self.cid = cid
        self.nc = nc
        self.per = per


def _qp_init_theta(seed, n):
    th = []
    st = (seed * 2654435761) & 2147483647
    if st == 0:
        st = 12345
    i = 0
    while i < n:
        st = (st * 1103515245 + 12345) & 2147483647
        th = th + [(float(st) / 2147483648.0) * _PF_TWO_PI]
        i = i + 1
    return th


def _qp_cid(nc, per):
    cid = []
    c = 0
    while c < nc:
        j = 0
        while j < per:
            cid = cid + [c]
            j = j + 1
        c = c + 1
    return cid


def _qp_omega_banded(nc, per):
    om = []
    c = 0
    while c < nc:
        base = _PF_OMEGA_T + _QP_CLUST_BAND * (float(c) - (float(nc) - 1.0) / 2.0)
        j = 0
        while j < per:
            om = om + [base + _PF_DOMEGA * (float(j) - (float(per) - 1.0) / 2.0)]
            j = j + 1
        c = c + 1
    return om


def _qp_block_adj(cid, n):
    a = []
    i = 0
    while i < n:
        j = 0
        while j < n:
            if i == j:
                a = a + [0.0]
            else:
                if cid[i] == cid[j]:
                    a = a + [1.0]
                else:
                    a = a + [0.0]
            j = j + 1
        i = i + 1
    return a


def quorum_new(seed, nc, per):
    n = nc * per
    cid = _qp_cid(nc, per)
    return QuorumPhase(_qp_init_theta(seed, n), _qp_omega_banded(nc, per),
                       _qp_block_adj(cid, n), cid, nc, per)


def quorum_with_adj(seed, nc, per, adj):
    n = nc * per
    return QuorumPhase(_qp_init_theta(seed, n), _qp_omega_banded(nc, per),
                       adj, _qp_cid(nc, per), nc, per)


def quorum_step(qp):
    n = qp.nc * qp.per
    newth = []
    i = 0
    while i < n:
        deg = 0.0
        acc = 0.0
        j = 0
        while j < n:
            aij = qp.adj[i * n + j]
            deg = deg + aij
            acc = acc + aij * _sin(qp.theta[j] - qp.theta[i])
            j = j + 1
        if deg == 0.0:
            deg = 1.0
        newth = newth + [qp.theta[i] + (qp.omega[i] + acc / deg)]
        i = i + 1
    return QuorumPhase(newth, qp.omega, qp.adj, qp.cid, qp.nc, qp.per)


def quorum_run(qp, steps):
    cur = qp
    t = 0
    while t < steps:
        cur = quorum_step(cur)
        t = t + 1
    return cur


def quorum_cluster_order(qp):
    n = qp.nc * qp.per
    sumR = 0.0
    c = 0
    while c < qp.nc:
        cx = 0.0
        sy = 0.0
        cnt = 0.0
        i = 0
        while i < n:
            if qp.cid[i] == c:
                cx = cx + _cos(qp.theta[i])
                sy = sy + _sin(qp.theta[i])
                cnt = cnt + 1.0
            i = i + 1
        cx = cx / cnt
        sy = sy / cnt
        sumR = sumR + _sqrt(cx * cx + sy * sy)
        c = c + 1
    return sumR / float(qp.nc)


def _qp_cluster_mean_unit(qp, c):
    n = qp.nc * qp.per
    cx = 0.0
    sy = 0.0
    i = 0
    while i < n:
        if qp.cid[i] == c:
            cx = cx + _cos(qp.theta[i])
            sy = sy + _sin(qp.theta[i])
        i = i + 1
    r = _sqrt(cx * cx + sy * sy)
    if r == 0.0:
        return [1.0, 0.0]
    return [cx / r, sy / r]


def quorum_cross_plv(qp, tail):
    cur = qp
    t = 0
    warm = 64 - tail
    while t < warm:
        cur = quorum_step(cur)
        t = t + 1
    npairs = qp.nc * (qp.nc - 1) // 2
    sumc = []
    sums = []
    p = 0
    while p < npairs:
        sumc = sumc + [0.0]
        sums = sums + [0.0]
        p = p + 1
    steps = 0
    while t < 64:
        cur = quorum_step(cur)
        pi = 0
        a = 0
        while a < qp.nc:
            ua = _qp_cluster_mean_unit(cur, a)
            b = a + 1
            while b < qp.nc:
                ub = _qp_cluster_mean_unit(cur, b)
                cd = ua[0] * ub[0] + ua[1] * ub[1]
                sd = ua[1] * ub[0] - ua[0] * ub[1]
                sumc[pi] = sumc[pi] + cd
                sums[pi] = sums[pi] + sd
                pi = pi + 1
                b = b + 1
            a = a + 1
        steps = steps + 1
        t = t + 1
    tot = 0.0
    denom = float(steps)
    p = 0
    while p < npairs:
        mc = sumc[p] / denom
        ms = sums[p] / denom
        tot = tot + _sqrt(mc * mc + ms * ms)
        p = p + 1
    return tot / float(npairs)


def quorum_within_plv(qp, tail):
    n = qp.nc * qp.per
    cur = qp
    t = 0
    warm = 64 - tail
    while t < warm:
        cur = quorum_step(cur)
        t = t + 1
    npairs = qp.nc * (qp.per * (qp.per - 1) // 2)
    sumc = []
    sums = []
    p = 0
    while p < npairs:
        sumc = sumc + [0.0]
        sums = sums + [0.0]
        p = p + 1
    steps = 0
    while t < 64:
        cur = quorum_step(cur)
        pi = 0
        i = 0
        while i < n:
            j = i + 1
            while j < n:
                if cur.cid[i] == cur.cid[j]:
                    d = cur.theta[i] - cur.theta[j]
                    sumc[pi] = sumc[pi] + _cos(d)
                    sums[pi] = sums[pi] + _sin(d)
                    pi = pi + 1
                j = j + 1
            i = i + 1
        steps = steps + 1
        t = t + 1
    tot = 0.0
    denom = float(steps)
    p = 0
    while p < npairs:
        mc = sumc[p] / denom
        ms = sums[p] / denom
        tot = tot + _sqrt(mc * mc + ms * ms)
        p = p + 1
    return tot / float(npairs)


def quorum_drop_node_order(seed, nc, per, steps):
    n = nc * per
    cid = _qp_cid(nc, per)
    omega = _qp_omega_banded(nc, per)
    theta0 = _qp_init_theta(seed, n)
    keep = []
    seen = []
    c = 0
    while c < nc:
        seen = seen + [0]
        c = c + 1
    i = 0
    while i < n:
        cc = cid[i]
        if seen[cc] == 0:
            seen[cc] = 1
        else:
            keep = keep + [i]
        i = i + 1
    m = len(keep)
    rth = []
    rom = []
    rcid = []
    a = 0
    while a < m:
        rth = rth + [theta0[keep[a]]]
        rom = rom + [omega[keep[a]]]
        rcid = rcid + [cid[keep[a]]]
        a = a + 1
    radj = _qp_block_adj(rcid, m)
    qp = QuorumPhase(rth, rom, radj, rcid, nc, per - 1)
    settled = quorum_run(qp, steps)
    return quorum_cluster_order(settled)


def quorum_star_no_hub_order(seed, nc, per, steps):
    n = nc * per
    cid = _qp_cid(nc, per)
    omega = _qp_omega_banded(nc, per)
    theta = _qp_init_theta(seed, n)
    t = 0
    while t < steps:
        nt = []
        i = 0
        while i < n:
            nt = nt + [theta[i] + omega[i]]
            i = i + 1
        theta = nt
        t = t + 1
    qp = QuorumPhase(theta, omega, _qp_block_adj(cid, n), cid, nc, per)
    return quorum_cluster_order(qp)


def quorum_star_baseline_order(seed, nc, per, steps):
    n = nc * per
    cid = _qp_cid(nc, per)
    omega = _qp_omega_banded(nc, per)
    theta = _qp_init_theta(seed, n)
    tt0 = _qp_init_theta(seed + 1000, 1)
    theta_t = tt0[0]
    k = 0.5
    t = 0
    while t < steps:
        nt = []
        i = 0
        while i < n:
            nt = nt + [theta[i] + (omega[i] + k * _sin(theta_t - theta[i]))]
            i = i + 1
        mp = 0.0
        i = 0
        while i < n:
            mp = mp + _sin(theta[i] - theta_t)
            i = i + 1
        mp = mp / float(n)
        theta_t = theta_t + (_PF_OMEGA_T + k * mp)
        theta = nt
        t = t + 1
    qp = QuorumPhase(theta, omega, _qp_block_adj(cid, n), cid, nc, per)
    return quorum_cluster_order(qp)


def quorum_shuffle_adj(seed, nc, per):
    n = nc * per
    cid = _qp_cid(nc, per)
    nedges = 0
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            if cid[i] == cid[j]:
                nedges = nedges + 1
            j = j + 1
        i = i + 1
    pairs_i = []
    pairs_j = []
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            pairs_i = pairs_i + [i]
            pairs_j = pairs_j + [j]
            j = j + 1
        i = i + 1
    np_ = len(pairs_i)
    order = []
    i = 0
    while i < np_:
        order = order + [i]
        i = i + 1
    st = (seed * 2654435761) & 2147483647
    if st == 0:
        st = 12345
    k = np_ - 1
    while k > 0:
        st = (st * 1103515245 + 12345) & 2147483647
        r = st % (k + 1)
        tmp = order[k]
        order[k] = order[r]
        order[r] = tmp
        k = k - 1
    adj = []
    i = 0
    while i < n * n:
        adj = adj + [0.0]
        i = i + 1
    e = 0
    while e < nedges:
        pid = order[e]
        pi = pairs_i[pid]
        pj = pairs_j[pid]
        adj[pi * n + pj] = 1.0
        adj[pj * n + pi] = 1.0
        e = e + 1
    return adj


# ════════════════════════════════════════════════════════════════════════
# engine_config_summary — introspection string (engine_cli.hexa:5251)
# ════════════════════════════════════════════════════════════════════════

def engine_config_summary(cfg):
    m = "on" if cfg.mitosis else "off"
    tc = "on" if cfg.topo_couple else "off"
    return ("engine_cli · ENGINE CLI control axis (substrate-config, NOT an emit gate, @L4) · "
            + "flags: --mitosis on|off · --no-mitosis · env ANIMA_MITOSIS · --engine conv|cdv2|hexad|omega · env ANIMA_ENGINE · --topo-couple on|off · --no-topo-couple · env ANIMA_TOPO_COUPLE · "
            + "precedence flag>env>default · "
            + "mitosis=" + m + " (ON=substrate grows per inference-time cell-division tick, p8; OFF=no-op split, ablation) · "
            + "engine=" + cfg.engine + " (conv=default .clm decoder; cdv2=ConsciousDecoderV2; hexad=σ6 integration; omega=closure engine, substrate→decode coupling bus; select=substrate-config NOT emit gate) · "
            + "topo_couple=" + tc + " (H_1521 — ON=15-lane state routed through the Φ-optimal cross-lane topology before the emit decision; OFF=DEFAULT, byte-identical pre-H_1521 live path, separation invariant H_1205) · "
            + "extensible: future ENGINE flags (lane select A/G/P/M) ride the same EngineConfig axis")


# ════════════════════════════════════════════════════════════════════════
# CA3ReplayMemory (§CA3Replay H_1427) — transition pattern-completion
# engine_cli.hexa:7403-7496
# ════════════════════════════════════════════════════════════════════════

class CA3ReplayMemory:
    __slots__ = ("n_item", "ctab", "prev_tot", "min_supp")

    def __init__(self, n_item, ctab, prev_tot, min_supp):
        self.n_item = n_item
        self.ctab = ctab
        self.prev_tot = prev_tot
        self.min_supp = min_supp


def ca3_replay_new(n_item, min_supp):
    ct = []
    i = 0
    while i < n_item * n_item:
        ct = ct + [0]
        i = i + 1
    pt = []
    j = 0
    while j < n_item:
        pt = pt + [0]
        j = j + 1
    return CA3ReplayMemory(n_item, ct, pt, min_supp)


def ca3_replay_observe(mem, prev, cur):
    n = mem.n_item
    if prev < 0 or prev >= n or cur < 0 or cur >= n:
        return mem
    ct = list(mem.ctab)
    pt = list(mem.prev_tot)
    ct[prev * n + cur] = ct[prev * n + cur] + 1
    pt[prev] = pt[prev] + 1
    return CA3ReplayMemory(n, ct, pt, mem.min_supp)


def ca3_replay_predict(mem, cur):
    n = mem.n_item
    if cur < 0 or cur >= n:
        return -1
    if mem.prev_tot[cur] == 0:
        return -1
    best = -1
    bestc = 0
    c = 0
    while c < n:
        cnt = mem.ctab[cur * n + c]
        if cnt > bestc:
            bestc = cnt
            best = c
        c = c + 1
    if bestc < mem.min_supp:
        return -1
    return best


def ca3_replay_conf(mem, cur):
    n = mem.n_item
    if cur < 0 or cur >= n:
        return 0.0
    tot = mem.prev_tot[cur]
    if tot == 0:
        return 0.0
    bestc = 0
    c = 0
    while c < n:
        cnt = mem.ctab[cur * n + c]
        if cnt > bestc:
            bestc = cnt
        c = c + 1
    if bestc < mem.min_supp:
        return 0.0
    return float(bestc) / float(tot)


def ca3_replay_marginal(mem):
    n = mem.n_item
    tot = []
    k = 0
    while k < n:
        tot = tot + [0]
        k = k + 1
    p = 0
    while p < n:
        c = 0
        while c < n:
            tot[c] = tot[c] + mem.ctab[p * n + c]
            c = c + 1
        p = p + 1
    best = -1
    bestc = 0
    c2 = 0
    while c2 < n:
        if tot[c2] > bestc:
            bestc = tot[c2]
            best = c2
        c2 = c2 + 1
    return best


# ════════════════════════════════════════════════════════════════════════
# GlobalWorkspace (§GWS H_1462) — winner-take-all ignition bottleneck
# engine_cli.hexa:7506-7587
# ════════════════════════════════════════════════════════════════════════

class GlobalWorkspace:
    __slots__ = ("margins", "n", "cap", "inhibit", "pass_thr")

    def __init__(self, margins, n, cap, inhibit, pass_thr):
        self.margins = margins
        self.n = n
        self.cap = cap
        self.inhibit = inhibit
        self.pass_thr = pass_thr


def gws_new(cap, inhibit, pass_thr):
    return GlobalWorkspace([], 0, cap, inhibit, pass_thr)


def gws_add(gws, margin):
    return GlobalWorkspace(gws.margins + [margin], gws.n + 1, gws.cap,
                           gws.inhibit, gws.pass_thr)


def _gws_argmax(margins, n):
    if n == 0:
        return -1
    best = 0
    bestv = margins[0]
    i = 1
    while i < n:
        if margins[i] > bestv:
            bestv = margins[i]
            best = i
        i = i + 1
    return best


def gws_ignited(gws):
    out = []
    if gws.n == 0:
        return out
    if gws.inhibit:
        w = _gws_argmax(gws.margins, gws.n)
        top = gws.margins[w]
        i = 0
        while i < gws.n:
            s = gws.margins[i]
            if i != w:
                s = s - 0.9 * top
            if s >= gws.pass_thr:
                if len(out) < gws.cap:
                    out = out + [i]
            i = i + 1
    else:
        i = 0
        while i < gws.n:
            if gws.margins[i] >= gws.pass_thr:
                out = out + [i]
            i = i + 1
    return out


def gws_winner(gws):
    ig = gws_ignited(gws)
    if len(ig) == 0:
        return -1
    return ig[0]


def gws_count(gws):
    return len(gws_ignited(gws))


def gws_leak(gws, idx):
    ig = gws_ignited(gws)
    i = 0
    while i < len(ig):
        if ig[i] == idx:
            return True
        i = i + 1
    return False


# ════════════════════════════════════════════════════════════════════════
# Habituation (§Habituation H_1465) — non-associative stimulus-specific decay
# engine_cli.hexa:7598-7643
# ════════════════════════════════════════════════════════════════════════

class Habituation:
    __slots__ = ("counts", "n_slots", "decay_step")

    def __init__(self, counts, n_slots, decay_step):
        self.counts = counts
        self.n_slots = n_slots
        self.decay_step = decay_step


def hab_new(n_slots, decay_step):
    c = []
    i = 0
    while i < n_slots:
        c = c + [0.0]
        i = i + 1
    return Habituation(c, n_slots, decay_step)


def hab_response(hab, slot, base):
    r = base - hab.decay_step * hab.counts[slot]
    if r < 0.0:
        return 0.0
    return r


def _hab_set(counts, slot, v, n):
    out = []
    i = 0
    while i < n:
        if i == slot:
            out = out + [v]
        else:
            out = out + [counts[i]]
        i = i + 1
    return out


def hab_observe(hab, slot):
    c2 = _hab_set(hab.counts, slot, hab.counts[slot] + 1.0, hab.n_slots)
    return Habituation(c2, hab.n_slots, hab.decay_step)


def hab_reset(hab, slot):
    c2 = _hab_set(hab.counts, slot, 0.0, hab.n_slots)
    return Habituation(c2, hab.n_slots, hab.decay_step)


# ════════════════════════════════════════════════════════════════════════
# G18-G31 scalar consciousness-gate free functions (engine_cli.hexa:7654-7922)
# ════════════════════════════════════════════════════════════════════════

def surprise(precision, error):
    return precision * error * error


def surprise_raw_error(precision, error):
    return error


def learned_precision(step, count, pmax):
    p = step * count
    if p > pmax:
        return pmax
    return p


def novelty(seen_count, k):
    return 1.0 / (1.0 + k * seen_count)


def attn_blink_detect(lag, depletion):
    if lag <= 1:
        return 0.94
    if lag >= 6:
        return 0.97
    recov = 0.10 + 0.22 * (float(lag) - 2.0)
    return recov + (1.0 - depletion) * (0.97 - recov)


def agency_attribute(pred, obs, thr):
    d = pred - obs
    if d < 0.0:
        d = 0.0 - d
    mt = 1.0 - d
    if mt >= thr:
        return 1.0
    return 0.0


def agency_other():
    return 0.0 - 1.0


def subjective_time(novelty_events, base, k):
    return base + k * novelty_events


def emotion_regulate(raw, g, strength):
    r = raw * (1.0 - g * strength)
    if r < 0.0:
        return 0.0
    return r


def directed_forget_recall(base_recall, inhibit, is_forget_cued):
    if is_forget_cued:
        r = base_recall * (1.0 - inhibit)
        if r < 0.0:
            return 0.0
        return r
    return base_recall


def body_ownership(sync_strength, base):
    return base * sync_strength


def divided_perf(resource, demand):
    ratio = resource / demand
    if ratio >= 1.0:
        return 0.98
    return ratio


def veto_execute(readiness, thr, veto):
    if readiness >= thr:
        if veto:
            return 0.0
        return 1.0
    return 0.0


def rivalry_transitions(steps, adapt_rate):
    if adapt_rate <= 0.0:
        return 0
    switch_thr = 0.5
    a = 0.0
    transitions = 0
    t = 0
    while t < steps:
        a = a + adapt_rate
        if a >= switch_thr:
            transitions = transitions + 1
            a = 0.0
        t = t + 1
    return transitions


def change_detect(change_mag, is_attended):
    if not is_attended:
        return 0.0
    thr = 0.10
    k = 11.0
    raw = 0.5 + k * (change_mag - thr)
    if raw <= 0.0:
        return 0.0
    if raw >= 1.0:
        return 1.0
    return raw


def imagery_activate(cue_match, topdown_on):
    if not topdown_on:
        return 0.0
    return cue_match


def priming_facilitate(relatedness, prime_residual):
    return relatedness * prime_residual


# ════════════════════════════════════════════════════════════════════════
# AffectFeatures (§Affect H_1290) — Damasio core-affect read over immune store
# engine_cli.hexa:2032-2131
# ════════════════════════════════════════════════════════════════════════

class AffectFeatures:
    __slots__ = ("margin", "contradiction", "novelty", "split", "curiosity",
                 "grounded", "err")

    def __init__(self, margin, contradiction, novelty, split, curiosity, grounded, err):
        self.margin = margin
        self.contradiction = contradiction
        self.novelty = novelty
        self.split = split
        self.curiosity = curiosity
        self.grounded = grounded
        self.err = err


def affect_substrate_features(mem, key, true_answer):
    """engine_cli.hexa:2048."""
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    grounded = (err <= mem.recall_thr)
    margin = 1.0 - err / mem.recall_thr
    if margin < 0.0:
        margin = 0.0
    contradiction = 0.0
    if not grounded:
        contradiction = 1.0
    else:
        if true_answer != "" and mem.cell_value[win] != true_answer:
            contradiction = 1.0
    novelty = err
    if novelty > 1.0:
        novelty = 1.0
    split = 0.0
    if err > mem.split_thr:
        split = 1.0
    under = 1.0 / (1.0 + float(mem.last_used[win]))
    curiosity = novelty * under
    return AffectFeatures(margin, contradiction, novelty, split, curiosity, grounded, err)


def affect_valence(f):
    return f.margin - f.contradiction


def affect_arousal(f):
    return f.novelty + 0.5 * f.split + 0.5 * f.curiosity


def affect_read(mem, key, true_answer):
    f = affect_substrate_features(mem, key, true_answer)
    return [affect_valence(f), affect_arousal(f)]


def affect_emit_decision(f):
    return affect_valence(f) >= 0.0


def affect_shuffle_features(feats, rng0):
    """engine_cli.hexa:2117 — LCG Fisher-Yates permute of the feature list."""
    n = len(feats)
    out = list(feats)
    st = rng0
    i = n - 1
    while i > 0:
        st = _lcg_next(st)
        j = st % (i + 1)
        tmp = out[i]
        out[i] = out[j]
        out[j] = tmp
        i = i - 1
    return out


# ════════════════════════════════════════════════════════════════════════
# HomeostaticDrive (§Hypothalamus H_1292) — setpoint-regulated leaky integrator
# engine_cli.hexa:2178-2249
# ════════════════════════════════════════════════════════════════════════

class HomeostaticDrive:
    __slots__ = ("accum", "last_drive", "setpoint", "leak", "kp", "ki")

    def __init__(self, accum, last_drive, setpoint, leak, kp, ki):
        self.accum = accum
        self.last_drive = last_drive
        self.setpoint = setpoint
        self.leak = leak
        self.kp = kp
        self.ki = ki


def homeo_new():
    return HomeostaticDrive(0.0, 0.0, 0.5, 0.1, 1.0, 0.5)


def homeo_new_ablated():
    return HomeostaticDrive(0.0, 0.0, 0.5, 0.1, 1.0, 0.0)


def homeo_satiation(mem, key):
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    m = 1.0 - err / mem.recall_thr
    if m < 0.0:
        m = 0.0
    if m > 1.0:
        m = 1.0
    return m


def homeo_step(hd, mem, key):
    """engine_cli.hexa:2218."""
    s = homeo_satiation(mem, key)
    deficit = hd.setpoint - s
    if deficit < 0.0:
        deficit = 0.0
    acc = (1.0 - hd.leak) * hd.accum + deficit
    if s >= hd.setpoint:
        acc = 0.0
    drive = hd.kp * deficit + hd.ki * acc
    return HomeostaticDrive(acc, drive, hd.setpoint, hd.leak, hd.kp, hd.ki)


def homeo_last(hd):
    return hd.last_drive


def homeo_drive(hd, mem, key):
    s = homeo_satiation(mem, key)
    deficit = hd.setpoint - s
    if deficit < 0.0:
        deficit = 0.0
    return hd.kp * deficit + hd.ki * hd.accum


def homeo_motivation_bias(hd, mem, key):
    return homeo_drive(hd, mem, key)


# ════════════════════════════════════════════════════════════════════════
# Libido (§Libido H_1504) — cue-conditioned incentive salience (wanting≠liking)
# engine_cli.hexa:2304-2407
# ════════════════════════════════════════════════════════════════════════

class Libido:
    __slots__ = ("accum", "last_want", "setpoint", "leak", "kp", "ki", "kc", "da_gain")

    def __init__(self, accum, last_want, setpoint, leak, kp, ki, kc, da_gain):
        self.accum = accum
        self.last_want = last_want
        self.setpoint = setpoint
        self.leak = leak
        self.kp = kp
        self.ki = ki
        self.kc = kc
        self.da_gain = da_gain


def libido_new():
    return Libido(0.0, 0.0, 0.5, 0.1, 1.0, 0.5, 1.0, 0.0)


def libido_new_da(da_gain):
    return Libido(0.0, 0.0, 0.5, 0.1, 1.0, 0.5, 1.0, da_gain)


def libido_new_ablated():
    return Libido(0.0, 0.0, 0.5, 0.1, 1.0, 0.5, 0.0, 0.0)


def libido_satiation(mem, key):
    win = _vnearest_idx(mem.protos, key)
    err = _l2(mem.protos[win], key)
    m = 1.0 - err / mem.recall_thr
    if m < 0.0:
        m = 0.0
    if m > 1.0:
        m = 1.0
    return m


def libido_cue_match(mem, cue_key):
    return libido_satiation(mem, cue_key)


def libido_wanting(ld, deficit, cue_match):
    return ld.kp * deficit + ld.ki * ld.accum + ld.kc * cue_match * (1.0 + ld.da_gain)


def libido_liking(ld, cue_match):
    return cue_match


def libido_step(ld, mem, key, cue_key):
    """engine_cli.hexa:2381."""
    s = libido_satiation(mem, key)
    deficit = ld.setpoint - s
    if deficit < 0.0:
        deficit = 0.0
    acc = (1.0 - ld.leak) * ld.accum + deficit
    if s >= ld.setpoint:
        acc = 0.0
    cm = libido_cue_match(mem, cue_key)
    stepped = Libido(acc, 0.0, ld.setpoint, ld.leak, ld.kp, ld.ki, ld.kc, ld.da_gain)
    want = libido_wanting(stepped, deficit, cm)
    return Libido(acc, want, ld.setpoint, ld.leak, ld.kp, ld.ki, ld.kc, ld.da_gain)


def libido_last(ld):
    return ld.last_want


def libido_motivation_bias(ld, mem, key, cue_key):
    s = libido_satiation(mem, key)
    deficit = ld.setpoint - s
    if deficit < 0.0:
        deficit = 0.0
    cm = libido_cue_match(mem, cue_key)
    return libido_wanting(ld, deficit, cm)


# ════════════════════════════════════════════════════════════════════════
# Allosteric buffer (§Allosteric H_1509) — tension-gated resistance to deviation
# engine_cli.hexa:2441-2549   (exp/sin = libm in this TU)
# ════════════════════════════════════════════════════════════════════════

def allo_mu(tau, lam, sigma):
    """engine_cli.hexa:2441."""
    dev = tau - 0.5
    dev2 = dev * dev
    return 1.0 + lam * (1.0 - _exp(0.0 - dev2 / (2.0 * sigma * sigma)))


def _allo_drive(t, phase, amp, per, shock_t, shock_len, shock_amp):
    """engine_cli.hexa:2449."""
    two_pi = 6.283185307179586
    frac = float(t + phase) / float(per)
    d = amp * _sin(two_pi * frac)
    if t >= shock_t and t < (shock_t + shock_len):
        d = d + shock_amp
    return d


def allo_defend(g, lam, sigma, seed, mode_shuf):
    """engine_cli.hexa:2464."""
    tt = 200
    amp = 0.30
    per = 17
    shock_t = 100
    shock_len = 20
    shock_amp = 0.35
    phase = seed % per

    mus_perm = []
    if mode_shuf == 1:
        bb = 0.5
        stc = seed & 2147483647
        mus = []
        tc = 0
        while tc < tt:
            stc = _lcg_next(stc)
            noise = (float(stc) / 2147483647.0 - 0.5) * 0.02
            d = _allo_drive(tc, phase, amp, per, shock_t, shock_len, shock_amp) + noise
            mu = allo_mu(bb, lam, sigma)
            mus = mus + [mu]
            restoring = g * mu * (0.5 - bb)
            bb = bb + d + restoring
            if bb < 0.0:
                bb = 0.0
            if bb > 1.0:
                bb = 1.0
            tc = tc + 1
        idx = []
        ii = 0
        while ii < tt:
            idx = idx + [float(ii)]
            ii = ii + 1
        stp = (seed * 2654435761) & 2147483647
        k = tt - 1
        while k > 0:
            stp = _lcg_next(stp)
            r = stp % (k + 1)
            tmp = idx[k]
            idx = _mi_set(idx, k, idx[r])
            idx = _mi_set(idx, r, tmp)
            k = k - 1
        jj = 0
        while jj < tt:
            mus_perm = mus_perm + [mus[int(idx[jj])]]
            jj = jj + 1

    b = 0.5
    st = seed & 2147483647
    sq = 0.0
    t = 0
    while t < tt:
        st = _lcg_next(st)
        noise = (float(st) / 2147483647.0 - 0.5) * 0.02
        d = _allo_drive(t, phase, amp, per, shock_t, shock_len, shock_amp) + noise
        mu = 1.0
        if mode_shuf == 1:
            mu = mus_perm[t]
        else:
            mu = allo_mu(b, lam, sigma)
        restoring = g * mu * (0.5 - b)
        b = b + d + restoring
        if b < 0.0:
            b = 0.0
        if b > 1.0:
            b = 1.0
        ex = b - 0.5
        sq = sq + ex * ex
        t = t + 1
    return _sqrt(sq / float(tt))


def allo_best_fixed_gain(sigma, seed):
    """engine_cli.hexa:2539."""
    grid = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
    best = 1.0e9
    i = 0
    while i < len(grid):
        r = allo_defend(grid[i], 0.0, sigma, seed, 0)
        if r < best:
            best = r
        i = i + 1
    return best


# ════════════════════════════════════════════════════════════════════════
# IIT-4 faithful big-Φ chain (stdlib/consciousness/iit4_*.hexa) — needed by
# CollectivePool. Mirrors iit4_tpm → iit4_distinction → iit4_relation →
# iit4_bigphi → iit4_bounded VERBATIM (a_phi_iit4_tool — faithful, NOT a proxy).
# ════════════════════════════════════════════════════════════════════════

def iit4_pow2(k):
    """iit4_tpm.hexa:53 → pow2_int = 1<<k."""
    return 1 << k


def iit4_bit(state, i):
    """iit4_tpm.hexa:58 → bit_set."""
    if (state & (1 << i)) != 0:
        return 1
    return 0


def iit4_units(mask, n):
    """iit4_tpm.hexa:63."""
    out = []
    i = 0
    while i < n:
        if iit4_bit(mask, i) == 1:
            out.append(i)
        i = i + 1
    return out


def iit4_expand(compact, units):
    """iit4_tpm.hexa:75."""
    out = 0
    b = 0
    k = len(units)
    while b < k:
        if iit4_bit(compact, b) == 1:
            out = out + iit4_pow2(units[b])
        b = b + 1
    return out


def tpm_on(tpm, n, state, unit):
    """iit4_tpm.hexa:88."""
    return tpm[state * n + unit]


def iit4_marginal_on(tpm, n, fix_mask, fix_state, target):
    """iit4_tpm.hexa:96."""
    full = iit4_pow2(n)
    total = 0.0
    count = 0
    s = 0
    while s < full:
        ok = 1
        i = 0
        while i < n:
            if iit4_bit(fix_mask, i) == 1:
                if iit4_bit(s, i) != iit4_bit(fix_state, i):
                    ok = 0
            i = i + 1
        if ok == 1:
            total = total + tpm_on(tpm, n, s, target)
            count = count + 1
        s = s + 1
    if count == 0:
        return 0.0
    return total / float(count)


def effect_repertoire(tpm, n, mech_mask, mech_state, purview_mask):
    """iit4_tpm.hexa:125."""
    units = iit4_units(purview_mask, n)
    k = len(units)
    p_on = []
    j = 0
    while j < k:
        p_on.append(iit4_marginal_on(tpm, n, mech_mask, mech_state, units[j]))
        j = j + 1
    nstates = iit4_pow2(k)
    rep = []
    cs = 0
    while cs < nstates:
        prob = 1.0
        b = 0
        while b < k:
            if iit4_bit(cs, b) == 1:
                prob = prob * p_on[b]
            else:
                prob = prob * (1.0 - p_on[b])
            b = b + 1
        rep.append(prob)
        cs = cs + 1
    return rep


def cause_repertoire(tpm, n, mech_mask, mech_state, purview_mask):
    """iit4_tpm.hexa:158."""
    p_units = iit4_units(purview_mask, n)
    k = len(p_units)
    m_units = iit4_units(mech_mask, n)
    mk = len(m_units)
    nstates = iit4_pow2(k)

    raw = []
    total = 0.0
    cs = 0
    while cs < nstates:
        pv_abs = iit4_expand(cs, p_units)
        like = 1.0
        mi = 0
        while mi < mk:
            mu = m_units[mi]
            p1 = iit4_marginal_on(tpm, n, purview_mask, pv_abs, mu)
            if iit4_bit(mech_state, mu) == 1:
                like = like * p1
            else:
                like = like * (1.0 - p1)
            mi = mi + 1
        raw.append(like)
        total = total + like
        cs = cs + 1

    rep = []
    i = 0
    while i < nstates:
        if total > 0.0:
            rep.append(raw[i] / total)
        else:
            rep.append(1.0 / float(nstates))
        i = i + 1
    return rep


def unconstrained_effect(tpm, n, purview_mask):
    """iit4_tpm.hexa:199."""
    return effect_repertoire(tpm, n, 0, 0, purview_mask)


def unconstrained_cause(purview_mask, n):
    """iit4_tpm.hexa:204."""
    units = iit4_units(purview_mask, n)
    nstates = iit4_pow2(len(units))
    u = 1.0 / float(nstates)
    rep = []
    i = 0
    while i < nstates:
        rep.append(u)
        i = i + 1
    return rep


def intrinsic_difference(p, q):
    """iit4_tpm.hexa:221 — ID = max_x p·log2(p/q), [value, state]."""
    n = len(p)
    ln2 = _ln(2.0)
    best_val = 0.0 - 1.0e308
    best_state = 0
    x = 0
    while x < n:
        px = p[x]
        term = 0.0
        if px > 1.0e-12:
            qx = q[x] + 1.0e-10
            term = px * (_ln(px) - _ln(qx)) / ln2
        if term > best_val:
            best_val = term
            best_state = x
        x = x + 1
    return [best_val, float(best_state)]


def iit4_compact_index(abs_state, units):
    """iit4_distinction.hexa:41."""
    idx = 0
    b = 0
    k = len(units)
    while b < k:
        if iit4_bit(abs_state, units[b]) == 1:
            idx = idx + iit4_pow2(b)
        b = b + 1
    return idx


def iit4_partitioned_effect(tpm, n, mech_state, m1, z1, m2, z2, purview_mask):
    """iit4_distinction.hexa:57."""
    units = iit4_units(purview_mask, n)
    k = len(units)
    p_on = []
    j = 0
    while j < k:
        u = units[j]
        if iit4_bit(z1, u) == 1:
            pj = iit4_marginal_on(tpm, n, m1, mech_state, u)
        else:
            pj = iit4_marginal_on(tpm, n, m2, mech_state, u)
        p_on.append(pj)
        j = j + 1
    nstates = iit4_pow2(k)
    rep = []
    cs = 0
    while cs < nstates:
        prob = 1.0
        b = 0
        while b < k:
            if iit4_bit(cs, b) == 1:
                prob = prob * p_on[b]
            else:
                prob = prob * (1.0 - p_on[b])
            b = b + 1
        rep.append(prob)
        cs = cs + 1
    return rep


def iit4_part_cause(tpm, n, mech_state, mp, zp):
    """iit4_distinction.hexa:92."""
    if mp == 0:
        return unconstrained_cause(zp, n)
    return cause_repertoire(tpm, n, mp, mech_state, zp)


def iit4_partitioned_cause(tpm, n, mech_state, m1, z1, m2, z2, purview_mask):
    """iit4_distinction.hexa:100."""
    cr1 = iit4_part_cause(tpm, n, mech_state, m1, z1)
    cr2 = iit4_part_cause(tpm, n, mech_state, m2, z2)
    zu = iit4_units(purview_mask, n)
    z1u = iit4_units(z1, n)
    z2u = iit4_units(z2, n)
    k = len(zu)
    nstates = iit4_pow2(k)
    rep = []
    cs = 0
    while cs < nstates:
        pv_abs = iit4_expand(cs, zu)
        idx1 = iit4_compact_index(pv_abs, z1u)
        idx2 = iit4_compact_index(pv_abs, z2u)
        rep.append(cr1[idx1] * cr2[idx2])
        cs = cs + 1
    return rep


def iit4_phi_at(p, q, xstar):
    """iit4_distinction.hexa:122."""
    px = p[xstar]
    if px <= 1.0e-12:
        return 0.0
    qx = q[xstar] + 1.0e-10
    phi = px * (_ln(px) - _ln(qx)) / _ln(2.0)
    if phi < 0.0:
        return 0.0
    return phi


def small_phi_effect(tpm, n, mech_mask, mech_state, purview_mask):
    """iit4_distinction.hexa:133."""
    p = effect_repertoire(tpm, n, mech_mask, mech_state, purview_mask)
    unc = unconstrained_effect(tpm, n, purview_mask)
    info = intrinsic_difference(p, unc)
    if info[0] <= 1.0e-12:
        return [0.0, info[1]]
    xstar = int(info[1])

    m_units = iit4_units(mech_mask, n)
    z_units = iit4_units(purview_mask, n)
    nm = iit4_pow2(len(m_units))
    nz = iit4_pow2(len(z_units))
    min_phi = 1.0e308
    mi = 0
    while mi < nm:
        m1 = iit4_expand(mi, m_units)
        m2 = mech_mask - m1
        zi = 0
        while zi < nz:
            z1 = iit4_expand(zi, z_units)
            z2 = purview_mask - z1
            identity = ((m1 == mech_mask) and (z1 == purview_mask)) or ((m1 == 0) and (z1 == 0))
            if identity == False:
                q = iit4_partitioned_effect(tpm, n, mech_state, m1, z1, m2, z2, purview_mask)
                phi_t = iit4_phi_at(p, q, xstar)
                if phi_t < min_phi:
                    min_phi = phi_t
            zi = zi + 1
        mi = mi + 1
    if min_phi > 1.0e307:
        min_phi = 0.0
    return [min_phi, info[1]]


def small_phi_cause(tpm, n, mech_mask, mech_state, purview_mask):
    """iit4_distinction.hexa:169."""
    p = cause_repertoire(tpm, n, mech_mask, mech_state, purview_mask)
    unc = unconstrained_cause(purview_mask, n)
    info = intrinsic_difference(p, unc)
    if info[0] <= 1.0e-12:
        return [0.0, info[1]]
    xstar = int(info[1])

    m_units = iit4_units(mech_mask, n)
    z_units = iit4_units(purview_mask, n)
    nm = iit4_pow2(len(m_units))
    nz = iit4_pow2(len(z_units))
    min_phi = 1.0e308
    mi = 0
    while mi < nm:
        m1 = iit4_expand(mi, m_units)
        m2 = mech_mask - m1
        zi = 0
        while zi < nz:
            z1 = iit4_expand(zi, z_units)
            z2 = purview_mask - z1
            identity = ((m1 == mech_mask) and (z1 == purview_mask)) or ((m1 == 0) and (z1 == 0))
            if identity == False:
                q = iit4_partitioned_cause(tpm, n, mech_state, m1, z1, m2, z2, purview_mask)
                phi_t = iit4_phi_at(p, q, xstar)
                if phi_t < min_phi:
                    min_phi = phi_t
            zi = zi + 1
        mi = mi + 1
    if min_phi > 1.0e307:
        min_phi = 0.0
    return [min_phi, info[1]]


def iit4_popcount(mask, n):
    """iit4_bounded.hexa:36."""
    c = 0
    i = 0
    while i < n:
        if iit4_bit(mask, i) == 1:
            c = c + 1
        i = i + 1
    return c


def mice_effect_bounded(tpm, n, mech_mask, mech_state, cap):
    """iit4_bounded.hexa:50."""
    full = iit4_pow2(n)
    best_phi = 0.0 - 1.0
    best_pv = 0
    best_state = 0.0
    pv = 1
    while pv < full:
        if iit4_popcount(pv, n) <= cap:
            r = small_phi_effect(tpm, n, mech_mask, mech_state, pv)
            if r[0] > best_phi:
                best_phi = r[0]
                best_pv = pv
                best_state = r[1]
        pv = pv + 1
    return [best_phi, float(best_pv), best_state]


def mice_cause_bounded(tpm, n, mech_mask, mech_state, cap):
    """iit4_bounded.hexa:71."""
    full = iit4_pow2(n)
    best_phi = 0.0 - 1.0
    best_pv = 0
    best_state = 0.0
    pv = 1
    while pv < full:
        if iit4_popcount(pv, n) <= cap:
            r = small_phi_cause(tpm, n, mech_mask, mech_state, pv)
            if r[0] > best_phi:
                best_phi = r[0]
                best_pv = pv
                best_state = r[1]
        pv = pv + 1
    return [best_phi, float(best_pv), best_state]


def distinction_bounded(tpm, n, mech_mask, mech_state, cap):
    """iit4_bounded.hexa:94."""
    ce = mice_cause_bounded(tpm, n, mech_mask, mech_state, cap)
    ee = mice_effect_bounded(tpm, n, mech_mask, mech_state, cap)
    phi_c = ce[0]
    phi_e = ee[0]
    phi_d = phi_c if phi_c < phi_e else phi_e
    return [phi_d, float(mech_mask), ce[1], ce[2], ee[1], ee[2], phi_c, phi_e]


def iit4_distinction_side(d, a_mask, n):
    """iit4_bigphi.hexa:45."""
    mech = int(d[1])
    cpv = int(d[2])
    epv = int(d[4])
    in_a = 0
    in_b = 0
    u = 0
    while u < n:
        involved = (iit4_bit(mech, u) == 1) or (iit4_bit(cpv, u) == 1) or (iit4_bit(epv, u) == 1)
        if involved:
            if iit4_bit(a_mask, u) == 1:
                in_a = 1
            else:
                in_b = 1
        u = u + 1
    if (in_a == 1) and (in_b == 1):
        return 0
    if in_a == 1:
        return 1
    return 2


def iit4_overlap_congruent(pv_i, state_i, pv_j, state_j, n):
    """iit4_relation.hexa:37."""
    units_i = iit4_units(pv_i, n)
    units_j = iit4_units(pv_j, n)
    abs_i = iit4_expand(state_i, units_i)
    abs_j = iit4_expand(state_j, units_j)
    overlap = 0
    congruent = 1
    u = 0
    while u < n:
        if (iit4_bit(pv_i, u) == 1) and (iit4_bit(pv_j, u) == 1):
            overlap = overlap + 1
            if iit4_bit(abs_i, u) != iit4_bit(abs_j, u):
                congruent = 0
        u = u + 1
    if (overlap > 0) and (congruent == 1):
        return 1
    return 0


def relation_2nd(d_i, d_j, n):
    """iit4_relation.hexa:60."""
    c = iit4_overlap_congruent(int(d_i[2]), int(d_i[3]), int(d_j[2]), int(d_j[3]), n)
    e = iit4_overlap_congruent(int(d_i[4]), int(d_i[5]), int(d_j[4]), int(d_j[5]), n)
    if (c == 1) or (e == 1):
        if d_i[0] < d_j[0]:
            return d_i[0]
        return d_j[0]
    return 0.0


def big_phi_bounded(tpm, n, sys_state, max_purview_size):
    """iit4_bounded.hexa:109 — [big_phi, total, sum_phi_d, sum_phi_r, n_dist]."""
    full = iit4_pow2(n)
    cap = max_purview_size

    dists = []
    sum_d = 0.0
    m = 1
    while m < full:
        d = distinction_bounded(tpm, n, m, sys_state, cap)
        if d[0] > 1.0e-9:
            dists.append(d)
            sum_d = sum_d + d[0]
        m = m + 1
    nd = len(dists)

    sum_r = 0.0
    i = 0
    while i < nd:
        j = i + 1
        while j < nd:
            r = relation_2nd(dists[i], dists[j], n)
            if r > 1.0e-9:
                sum_r = sum_r + r
            j = j + 1
        i = i + 1
    total = sum_d + sum_r

    if n < 2:
        return [0.0, total, sum_d, sum_r, float(nd)]

    all_mask = full - 1
    min_loss = 1.0e308
    a = 1
    while a < all_mask:
        if iit4_bit(a, 0) == 1:
            sides = []
            surv = 0.0
            k = 0
            while k < nd:
                s = iit4_distinction_side(dists[k], a, n)
                sides.append(float(s))
                if s != 0:
                    surv = surv + dists[k][0]
                k = k + 1
            ii = 0
            while ii < nd:
                jj = ii + 1
                while jj < nd:
                    r = relation_2nd(dists[ii], dists[jj], n)
                    if r > 1.0e-9:
                        si = int(sides[ii])
                        sj = int(sides[jj])
                        if (si != 0) and (sj != 0) and (si == sj):
                            surv = surv + r
                    jj = jj + 1
                ii = ii + 1
            loss = total - surv
            if loss < min_loss:
                min_loss = loss
        a = a + 1
    if min_loss > 1.0e307:
        min_loss = 0.0
    if min_loss < 0.0:
        min_loss = 0.0
    return [min_loss, total, sum_d, sum_r, float(nd)]


# ════════════════════════════════════════════════════════════════════════
# CollectivePool / HiveMind (§CollectivePool H_1295) — faithful collective-Φ
# ════════════════════════════════════════════════════════════════════════

class CollectivePool:
    """engine_cli.hexa:2701."""
    __slots__ = ("rules", "w", "n")

    def __init__(self, rules, w, n):
        self.rules = rules
        self.w = w
        self.n = n


def collective_new(members, w):
    """engine_cli.hexa:2709."""
    return CollectivePool(members, w, len(members))


def _eca_tpm_n3(rule):
    """engine_cli.hexa:2715."""
    nn = 3
    t = []
    s = 0
    while s < 8:
        i = 0
        while i < nn:
            l = iit4_bit(s, (i - 1 + nn) % nn)
            c = iit4_bit(s, i)
            r = iit4_bit(s, (i + 1) % nn)
            idx = 4 * l + 2 * c + r
            t.append(float(iit4_bit(rule, idx)))
            i = i + 1
        s = s + 1
    return t


def _build_tpm_ab(rule_a, rule_b, w):
    """engine_cli.hexa:2736."""
    nn = 6
    full = 64
    omw = 1.0 - w
    t = []
    s = 0
    while s < full:
        b0 = iit4_bit(s, 0)
        b1 = iit4_bit(s, 1)
        b2 = iit4_bit(s, 2)
        b3 = iit4_bit(s, 3)
        b4 = iit4_bit(s, 4)
        b5 = iit4_bit(s, 5)
        i = 0
        while i < nn:
            rule = rule_a
            if i >= 3:
                rule = rule_b
            l_dec = 0
            c_dec = 0
            r_dec = 0
            if i == 0:
                l_dec = b2; c_dec = b0; r_dec = b1
            if i == 1:
                l_dec = b0; c_dec = b1; r_dec = b2
            if i == 2:
                l_dec = b1; c_dec = b2; r_dec = b0
            if i == 3:
                l_dec = b5; c_dec = b3; r_dec = b4
            if i == 4:
                l_dec = b3; c_dec = b4; r_dec = b5
            if i == 5:
                l_dec = b4; c_dec = b5; r_dec = b3
            idx_dec = 4 * l_dec + 2 * c_dec + r_dec
            next_dec = iit4_bit(rule, idx_dec)
            l_cou = 0
            c_cou = 0
            r_cou = 0
            if i == 0:
                l_cou = b5; c_cou = b0; r_cou = b1
            if i == 1:
                l_cou = b0; c_cou = b1; r_cou = b2
            if i == 2:
                l_cou = b1; c_cou = b2; r_cou = b3
            if i == 3:
                l_cou = b2; c_cou = b3; r_cou = b4
            if i == 4:
                l_cou = b3; c_cou = b4; r_cou = b5
            if i == 5:
                l_cou = b4; c_cou = b5; r_cou = b0
            idx_cou = 4 * l_cou + 2 * c_cou + r_cou
            next_cou = iit4_bit(rule, idx_cou)
            t.append(omw * float(next_dec) + w * float(next_cou))
            i = i + 1
        s = s + 1
    return t


def _build_tpm_ring(rules, w):
    """engine_cli.hexa:2788."""
    nblk = len(rules)
    n = 3 * nblk
    full = iit4_pow2(n)
    omw = 1.0 - w
    t = []
    s = 0
    while s < full:
        i = 0
        while i < n:
            g = i // 3
            j = i % 3
            base = g * 3
            rule = rules[g]
            ld = base + (j + 2) % 3
            rd = base + (j + 1) % 3
            idx_dec = 4 * iit4_bit(s, ld) + 2 * iit4_bit(s, i) + iit4_bit(s, rd)
            next_dec = iit4_bit(rule, idx_dec)
            lc = (i - 1 + n) % n
            rc = (i + 1) % n
            idx_cou = 4 * iit4_bit(s, lc) + 2 * iit4_bit(s, i) + iit4_bit(s, rc)
            next_cou = iit4_bit(rule, idx_cou)
            t.append(omw * float(next_dec) + w * float(next_cou))
            i = i + 1
        s = s + 1
    return t


def collective_member_phi(cp, idx):
    """engine_cli.hexa:2822."""
    r = big_phi_bounded(_eca_tpm_n3(cp.rules[idx]), 3, 0, 3)
    return r[0]


def collective_sum_phi(cp):
    """engine_cli.hexa:2828."""
    acc = 0.0
    i = 0
    while i < cp.n:
        acc = acc + collective_member_phi(cp, i)
        i = i + 1
    return acc


def collective_nmax():
    """engine_cli.hexa:2844."""
    return 3


def collective_phi(cp):
    """engine_cli.hexa:2851."""
    if cp.n == 2:
        r = big_phi_bounded(_build_tpm_ab(cp.rules[0], cp.rules[1], cp.w), 6, 0, 2)
        return r[0]
    if cp.n >= 3 and cp.n <= collective_nmax():
        r = big_phi_bounded(_build_tpm_ring(cp.rules, cp.w), 3 * cp.n, 0, 2)
        return r[0]
    return collective_sum_phi(cp)


def collective_excess(cp):
    """engine_cli.hexa:2867."""
    return collective_phi(cp) - collective_sum_phi(cp)


def collective_is_super_additive(cp, margin):
    """engine_cli.hexa:2873."""
    return collective_excess(cp) >= margin


def collective_coherence(cp):
    """engine_cli.hexa:2882."""
    if cp.n == 2:
        tpm = _build_tpm_ab(cp.rules[0], cp.rules[1], cp.w)
        acc = 0.0
        cnt = 0
        s = 0
        while s < 64:
            base = s * 6
            i = 0
            while i < 3:
                d = tpm[base + i] - tpm[base + i + 3]
                if d < 0.0:
                    d = 0.0 - d
                acc = acc + d
                cnt = cnt + 1
                i = i + 1
            s = s + 1
        return 1.0 - (acc / float(cnt))
    if cp.n >= 3 and cp.n <= collective_nmax():
        nblk = cp.n
        n = 3 * nblk
        full = iit4_pow2(n)
        tpm = _build_tpm_ring(cp.rules, cp.w)
        acc = 0.0
        cnt = 0
        s = 0
        while s < full:
            base = s * n
            g = 0
            while g < nblk:
                gn = (g + 1) % nblk
                c = 0
                while c < 3:
                    d = tpm[base + g * 3 + c] - tpm[base + gn * 3 + c]
                    if d < 0.0:
                        d = 0.0 - d
                    acc = acc + d
                    cnt = cnt + 1
                    c = c + 1
                g = g + 1
            s = s + 1
        return 1.0 - (acc / float(cnt))
    return 0.0


# ════════════════════════════════════════════════════════════════════════
# SkillCell (§SkillGrow H_1300) — ridge-LSQ local heads + mitosis Voronoi grow
# ════════════════════════════════════════════════════════════════════════

def _sc_C():
    """engine_cli.hexa:5292."""
    return 4


def _sc_SPLIT_THRESH():
    """engine_cli.hexa:5293."""
    return 0.05


def _sc_GROW_MAX():
    """engine_cli.hexa:5294."""
    return 4


class SkillCell:
    """engine_cli.hexa:5297."""
    __slots__ = ("center", "head_w", "head_b")

    def __init__(self, center, head_w, head_b):
        self.center = center
        self.head_w = head_w
        self.head_b = head_b


def _sc_vmean(rows):
    """engine_cli.hexa:5304."""
    n = len(rows)
    d = len(rows[0])
    out = []
    j = 0
    while j < d:
        s = 0.0
        i = 0
        while i < n:
            s = s + rows[i][j]
            i = i + 1
        out.append(s / float(n))
        j = j + 1
    return out


def _sc_argmax(hw, hb, x):
    """engine_cli.hexa:5320."""
    cc = len(hw)
    d = len(x)
    best = 0
    bestv = 0.0
    c = 0
    while c < cc:
        s = hb[c]
        j = 0
        while j < d:
            s = s + hw[c][j] * x[j]
            j = j + 1
        if c == 0 or s > bestv:
            bestv = s
            best = c
        c = c + 1
    return best


def _sc_gauss_solve(a, b):
    """engine_cli.hexa:5338 — Gauss-Jordan with partial pivoting."""
    n = len(a)
    m = len(b[0])
    aug = []
    i = 0
    while i < n:
        aug.append(list(a[i]) + list(b[i]))
        i = i + 1
    col = 0
    while col < n:
        piv = col
        pv = _absf(aug[col][col])
        r = col + 1
        while r < n:
            av = _absf(aug[r][col])
            if av > pv:
                pv = av
                piv = r
            r = r + 1
        if piv != col:
            tmp = aug[piv]
            aug[piv] = aug[col]
            aug[col] = tmp
        d = aug[col][col]
        k = 0
        while k < n + m:
            aug[col][k] = aug[col][k] / d
            k = k + 1
        r2 = 0
        while r2 < n:
            if r2 != col:
                f = aug[r2][col]
                k2 = 0
                while k2 < n + m:
                    aug[r2][k2] = aug[r2][k2] - f * aug[col][k2]
                    k2 = k2 + 1
            r2 = r2 + 1
        col = col + 1
    out = []
    i2 = 0
    while i2 < n:
        row = []
        j = n
        while j < n + m:
            row.append(aug[i2][j])
            j = j + 1
        out.append(row)
        i2 = i2 + 1
    return out


def skill_fit_head(x, y):
    """engine_cli.hexa:5394."""
    n = len(x)
    d = len(x[0])
    cc = _sc_C()
    lam = 0.001
    xb = []
    yy = []
    i = 0
    while i < n:
        xb.append(list(x[i]) + [1.0])
        oh = []
        c = 0
        while c < cc:
            oh.append(1.0 if c == y[i] else 0.0)
            c = c + 1
        yy.append(oh)
        i = i + 1
    dp = d + 1
    amat = []
    rhs = []
    a = 0
    while a < dp:
        arow = []
        bcol = 0
        while bcol < dp:
            s = 0.0
            k = 0
            while k < n:
                s = s + xb[k][a] * xb[k][bcol]
                k = k + 1
            if a == bcol:
                s = s + lam
            arow.append(s)
            bcol = bcol + 1
        amat.append(arow)
        rrow = []
        c2 = 0
        while c2 < cc:
            s2 = 0.0
            k2 = 0
            while k2 < n:
                s2 = s2 + xb[k2][a] * yy[k2][c2]
                k2 = k2 + 1
            rrow.append(s2)
            c2 = c2 + 1
        rhs.append(rrow)
        a = a + 1
    sol = _sc_gauss_solve(amat, rhs)
    hw = []
    c3 = 0
    while c3 < cc:
        wr = []
        j = 0
        while j < d:
            wr.append(sol[j][c3])
            j = j + 1
        hw.append(wr)
        c3 = c3 + 1
    hb = []
    c4 = 0
    while c4 < cc:
        hb.append(sol[d][c4])
        c4 = c4 + 1
    return SkillCell(_sc_vmean(x), hw, hb)


def _sc_local_err(hw, hb, x, y):
    """engine_cli.hexa:5458."""
    n = len(x)
    if n == 0:
        return -1.0
    bad = 0
    i = 0
    while i < n:
        if _sc_argmax(hw, hb, x[i]) != y[i]:
            bad = bad + 1
        i = i + 1
    return float(bad) / float(n)


def _sc_principal_axis(d):
    """engine_cli.hexa:5472 — top principal axis via power iteration."""
    n = len(d)
    dim = len(d[0])
    cov = []
    a = 0
    while a < dim:
        row = []
        b = 0
        while b < dim:
            s = 0.0
            k = 0
            while k < n:
                s = s + d[k][a] * d[k][b]
                k = k + 1
            row.append(s)
            b = b + 1
        cov.append(row)
        a = a + 1
    v = []
    j = 0
    while j < dim:
        v.append(1.0 / _sqrt(float(dim)))
        j = j + 1
    it = 0
    while it < 50:
        nv = []
        r = 0
        while r < dim:
            s = 0.0
            c = 0
            while c < dim:
                s = s + cov[r][c] * v[c]
                c = c + 1
            nv.append(s)
            r = r + 1
        nrm = 0.0
        q = 0
        while q < dim:
            nrm = nrm + nv[q] * nv[q]
            q = q + 1
        nrm = _sqrt(nrm)
        if nrm < 0.000000000001:
            return v
        w = 0
        while w < dim:
            v[w] = nv[w] / nrm
            w = w + 1
        it = it + 1
    return v


def _sc_own(centers, x):
    """engine_cli.hexa:5519."""
    n = len(x)
    out = []
    i = 0
    while i < n:
        out.append(_vnearest_idx(centers, x[i]))
        i = i + 1
    return out


def _sc_subset_x(owner, x, ci):
    """engine_cli.hexa:5528."""
    out = []
    i = 0
    while i < len(x):
        if owner[i] == ci:
            out.append(x[i])
        i = i + 1
    return out


def _sc_subset_y(owner, y, ci):
    """engine_cli.hexa:5534."""
    out = []
    i = 0
    while i < len(y):
        if owner[i] == ci:
            out.append(y[i])
        i = i + 1
    return out


def skill_grow(x, y, cfg):
    """engine_cli.hexa:5544 — mitosis Voronoi grow of dedicated skill cells."""
    centers = [_sc_vmean(x)]
    while True:
        owner = _sc_own(centers, x)
        cells = []
        errs = []
        ci = 0
        while ci < len(centers):
            sx = _sc_subset_x(owner, x, ci)
            sy = _sc_subset_y(owner, y, ci)
            if len(sx) == 0:
                dim = len(x[0])
                zw = []
                c = 0
                while c < _sc_C():
                    zr = []
                    j = 0
                    while j < dim:
                        zr.append(0.0)
                        j = j + 1
                    zw.append(zr)
                    c = c + 1
                zb = []
                c2 = 0
                while c2 < _sc_C():
                    zb.append(0.0)
                    c2 = c2 + 1
                cells.append(SkillCell(centers[ci], zw, zb))
                errs.append(-1.0)
            else:
                cell = skill_fit_head(sx, sy)
                cells.append(SkillCell(centers[ci], cell.head_w, cell.head_b))
                errs.append(_sc_local_err(cell.head_w, cell.head_b, sx, sy))
            ci = ci + 1
        worst = 0
        wv = errs[0]
        e = 1
        while e < len(errs):
            if errs[e] > wv:
                wv = errs[e]
                worst = e
            e = e + 1
        if wv <= _sc_SPLIT_THRESH() or len(centers) >= _sc_GROW_MAX():
            return cells
        grown = engine_mitosis_tick(len(centers), cfg)
        if grown <= len(centers):
            return cells
        sx = _sc_subset_x(owner, x, worst)
        c0 = _sc_vmean(sx)
        dmat = []
        i = 0
        while i < len(sx):
            row = []
            j = 0
            while j < len(c0):
                row.append(sx[i][j] - c0[j])
                j = j + 1
            dmat.append(row)
            i = i + 1
        axis = _sc_principal_axis(dmat)
        left = []
        right = []
        p = 0
        while p < len(sx):
            proj = 0.0
            j2 = 0
            while j2 < len(axis):
                proj = proj + dmat[p][j2] * axis[j2]
                j2 = j2 + 1
            if proj <= 0.0:
                left.append(sx[p])
            else:
                right.append(sx[p])
            p = p + 1
        if len(left) == 0 or len(right) == 0:
            return cells
        centers[worst] = _sc_vmean(left)
        centers.append(_sc_vmean(right))


def skill_route(cells, perm, x):
    """engine_cli.hexa:5629."""
    if len(cells) == 0:
        return -1
    best = 0
    bestd = _l2(cells[0].center, x)
    i = 1
    while i < len(cells):
        d = _l2(cells[i].center, x)
        if d < bestd:
            bestd = d
            best = i
        i = i + 1
    if len(perm) == len(cells):
        best = perm[best]
    return _sc_argmax(cells[best].head_w, cells[best].head_b, x)


def _sc_softmax_row(z):
    """engine_cli.hexa:5645."""
    n = len(z)
    mx = z[0]
    i = 1
    while i < n:
        if z[i] > mx:
            mx = z[i]
        i = i + 1
    e = []
    s = 0.0
    j = 0
    while j < n:
        v = _exp(z[j] - mx)
        e.append(v)
        s = s + v
        j = j + 1
    out = []
    k = 0
    while k < n:
        out.append(e[k] / s)
        k = k + 1
    return out


# ════════════════════════════════════════════════════════════════════════
# SkillGradFT (§SkillGradFT H_1300) — shared softmax-linear net (forgetting arm)
# ════════════════════════════════════════════════════════════════════════

class SkillGradFT:
    """engine_cli.hexa:5664."""
    __slots__ = ("w", "b")

    def __init__(self, w, b):
        self.w = w
        self.b = b


def skill_gradft_new(d, seed):
    """engine_cli.hexa:5673."""
    cc = _sc_C()
    state = seed + 5000
    w = []
    c = 0
    while c < cc:
        row = []
        j = 0
        while j < d:
            state = (state * 1103515245 + 12345) % 2147483648
            u = float(state) / 2147483648.0
            row.append((u - 0.5) * 0.02)
            j = j + 1
        w.append(row)
        c = c + 1
    b = []
    c2 = 0
    while c2 < cc:
        b.append(0.0)
        c2 = c2 + 1
    return SkillGradFT(w, b)


def skill_gradft_train(net, x, y):
    """engine_cli.hexa:5699."""
    cc = _sc_C()
    d = len(x[0])
    n = len(x)
    lr = 0.20
    steps = 300
    w = net.w
    b = net.b
    t = 0
    while t < steps:
        gw = []
        gb = []
        c = 0
        while c < cc:
            gr = []
            j = 0
            while j < d:
                gr.append(0.0)
                j = j + 1
            gw.append(gr)
            gb.append(0.0)
            c = c + 1
        i = 0
        while i < n:
            z = []
            c2 = 0
            while c2 < cc:
                s = b[c2]
                j2 = 0
                while j2 < d:
                    s = s + w[c2][j2] * x[i][j2]
                    j2 = j2 + 1
                z.append(s)
                c2 = c2 + 1
            p = _sc_softmax_row(z)
            c3 = 0
            while c3 < cc:
                tgt = 1.0 if c3 == y[i] else 0.0
                diff = p[c3] - tgt
                j3 = 0
                while j3 < d:
                    gw[c3][j3] = gw[c3][j3] + diff * x[i][j3]
                    j3 = j3 + 1
                gb[c3] = gb[c3] + diff
                c3 = c3 + 1
            i = i + 1
        c4 = 0
        while c4 < cc:
            j4 = 0
            while j4 < d:
                w[c4][j4] = w[c4][j4] - lr * (gw[c4][j4] / float(n))
                j4 = j4 + 1
            b[c4] = b[c4] - lr * (gb[c4] / float(n))
            c4 = c4 + 1
        t = t + 1
    return SkillGradFT(w, b)


def skill_gradft_pred(net, x):
    """engine_cli.hexa:5759."""
    return _sc_argmax(net.w, net.b, x)


# ════════════════════════════════════════════════════════════════════════
# CPField (§CategoricalPerception H_1325) — RBF Voronoi categorical-perception
# ════════════════════════════════════════════════════════════════════════

class CPField:
    """engine_cli.hexa:5796."""
    __slots__ = ("protos", "labels", "n")

    def __init__(self, protos, labels, n):
        self.protos = protos
        self.labels = labels
        self.n = n


def _cp_centers(dim):
    """engine_cli.hexa:5803."""
    c = []
    i = 0
    while i < dim:
        c.append(float(i) / float(dim - 1))
        i = i + 1
    return c


def cp_embed(x, dim):
    """engine_cli.hexa:5816."""
    centers = _cp_centers(dim)
    width = 0.115
    v = []
    nrm = 0.0
    i = 0
    while i < dim:
        d = x - centers[i]
        e = _exp(-(d * d) / (2.0 * width * width))
        v.append(e)
        nrm = nrm + e * e
        i = i + 1
    nrm = _sqrt(nrm)
    out = []
    j = 0
    while j < dim:
        out.append((v[j] / nrm) if nrm > 0.0 else v[j])
        j = j + 1
    return out


def _cp_owner_idx(cp, key):
    """engine_cli.hexa:5840."""
    return _vnearest_idx(cp.protos, key)


def cp_fit(X, Y, grow_max, passes):
    """engine_cli.hexa:5849."""
    m = len(X)
    dim = len(X[0])
    c0 = []
    q = 0
    while q < dim:
        s = 0.0
        r = 0
        while r < m:
            s = s + X[r][q]
            r = r + 1
        c0.append(s / float(m))
        q = q + 1
    nrm = 0.0
    a = 0
    while a < dim:
        nrm = nrm + c0[a] * c0[a]
        a = a + 1
    nrm = _sqrt(nrm)
    c0n = []
    b = 0
    while b < dim:
        c0n.append((c0[b] / nrm) if nrm > 0.0 else c0[b])
        b = b + 1
    seed_stim = 0
    sd = _l2(X[0], c0n)
    k = 1
    while k < m:
        dd = _l2(X[k], c0n)
        if dd < sd:
            sd = dd
            seed_stim = k
        k = k + 1
    cp = CPField([c0n], [Y[seed_stim]], 1)
    p = 0
    while p < passes:
        if cp.n >= 1 + grow_max:
            return cp
        worst = -1
        worstd = 0.0
        found = False
        s2 = 0
        while s2 < m:
            ow = _cp_owner_idx(cp, X[s2])
            if cp.labels[ow] != Y[s2]:
                dist = _l2(X[s2], cp.protos[ow])
                if (not found) or dist < worstd:
                    worstd = dist
                    worst = s2
                    found = True
            s2 = s2 + 1
        if not found:
            return cp
        cp = CPField(cp.protos + [X[worst]], cp.labels + [Y[worst]], cp.n + 1)
        p = p + 1
    return cp


def cp_regrow(cp, X, Y, grow_max, passes):
    """engine_cli.hexa:5910."""
    m = len(X)
    out = CPField(cp.protos, cp.labels, cp.n)
    base = cp.n
    p = 0
    while p < passes:
        if out.n >= base + grow_max:
            return out
        worst = -1
        worstd = 0.0
        found = False
        s2 = 0
        while s2 < m:
            ow = _cp_owner_idx(out, X[s2])
            if out.labels[ow] != Y[s2]:
                dist = _l2(X[s2], out.protos[ow])
                if (not found) or dist < worstd:
                    worstd = dist
                    worst = s2
                    found = True
            s2 = s2 + 1
        if not found:
            return out
        out = CPField(out.protos + [X[worst]], out.labels + [Y[worst]], out.n + 1)
        p = p + 1
    return out


def cp_posterior(cp, key):
    """engine_cli.hexa:5940."""
    beta = 18.0
    dmin = _l2(cp.protos[0], key)
    i = 1
    while i < cp.n:
        d = _l2(cp.protos[i], key)
        if d < dmin:
            dmin = d
        i = i + 1
    wsum = 0.0
    acc = 0.0
    j = 0
    while j < cp.n:
        d = _l2(cp.protos[j], key)
        w = _exp(-beta * (d - dmin))
        wsum = wsum + w
        acc = acc + w * float(cp.labels[j])
        j = j + 1
    if wsum > 0.0:
        return acc / wsum
    return acc


def cp_discrim_curve(cp, X):
    """engine_cli.hexa:5965."""
    n = len(X)
    out = []
    i = 0
    while i < n - 1:
        d = _absf(cp_posterior(cp, X[i]) - cp_posterior(cp, X[i + 1]))
        out.append(d)
        i = i + 1
    return out


def cp_peak_loc_idx(curve):
    """engine_cli.hexa:5979."""
    best = 0
    bv = curve[0]
    i = 1
    while i < len(curve):
        if curve[i] > bv:
            bv = curve[i]
            best = i
        i = i + 1
    return best


def cp_peak_count(curve):
    """engine_cli.hexa:5994."""
    frac = 0.50
    n = len(curve)
    mx = curve[0]
    a = 1
    while a < n:
        if curve[a] > mx:
            mx = curve[a]
        a = a + 1
    if mx <= 0.0:
        return 0
    thr = frac * mx
    cnt = 0
    t = 0
    while t < n:
        if curve[t] >= thr:
            is_max = False
            if t == 0:
                is_max = curve[t] > curve[t + 1]
            elif t == n - 1:
                is_max = curve[t] > curve[t - 1]
            else:
                is_max = (curve[t] > curve[t - 1]) and (curve[t] > curve[t + 1])
            if is_max:
                cnt = cnt + 1
        t = t + 1
    return cnt


def cp_labels_boundary(positions, boundary):
    """engine_cli.hexa:6023."""
    y = []
    i = 0
    while i < len(positions):
        y.append(1 if positions[i] > boundary else 0)
        i = i + 1
    return y


def cp_labels_shuffle(positions, seed):
    """engine_cli.hexa:6040."""
    y = []
    i = 0
    while i < len(positions):
        h = _immune_fnv1a([seed & 255, i, (seed // 256) & 255, i * 7 + 13])
        y.append((h // 65536) % 2)
        i = i + 1
    return y


def cp_stimuli(n_stim, dim):
    """engine_cli.hexa:6054."""
    X = []
    i = 0
    while i < n_stim:
        X.append(cp_embed(float(i) / float(n_stim - 1), dim))
        i = i + 1
    return X


def cp_tag_vec(lang, gain, tag_dim):
    """engine_cli.hexa:6091."""
    t = []
    i = 0
    while i < tag_dim:
        on = gain if i == lang else 0.0
        t.append(on)
        i = i + 1
    return t


def cp_tagged_key(base, lang, gain, tag_dim):
    """engine_cli.hexa:6104."""
    return list(base) + cp_tag_vec(lang, gain, tag_dim)


def cp_stimuli_tagged(n_stim, dim, lang, gain, tag_dim):
    """engine_cli.hexa:6110."""
    base = cp_stimuli(n_stim, dim)
    X = []
    i = 0
    while i < n_stim:
        X.append(cp_tagged_key(base[i], lang, gain, tag_dim))
        i = i + 1
    return X


def cp_fit_more(cp0, X, Y, grow_max, passes):
    """engine_cli.hexa:6129."""
    m = len(X)
    cp = cp0
    p = 0
    while p < passes:
        if cp.n >= 1 + grow_max:
            return cp
        worst = -1
        worstd = 0.0
        found = False
        s2 = 0
        while s2 < m:
            ow = _cp_owner_idx(cp, X[s2])
            if cp.labels[ow] != Y[s2]:
                dist = _l2(X[s2], cp.protos[ow])
                if (not found) or dist < worstd:
                    worstd = dist
                    worst = s2
                    found = True
            s2 = s2 + 1
        if not found:
            return cp
        cp = CPField(cp.protos + [X[worst]], cp.labels + [Y[worst]], cp.n + 1)
        p = p + 1
    return cp


def cp_within_cross_margin(curve, n_stim, boundary):
    """engine_cli.hexa:6159."""
    np_ = len(curve)
    cross_sum = 0.0
    cross_n = 0
    within_sum = 0.0
    within_n = 0
    i = 0
    while i < np_:
        mid = (float(i) + 0.5) / float(n_stim - 1)
        d = _absf(mid - boundary)
        if d <= 0.12:
            cross_sum = cross_sum + curve[i]
            cross_n = cross_n + 1
        if d >= 0.25:
            within_sum = within_sum + curve[i]
            within_n = within_n + 1
        i = i + 1
    cross = (cross_sum / float(cross_n)) if cross_n > 0 else 0.0
    within = (within_sum / float(within_n)) if within_n > 0 else 0.0
    return cross - within


def cp_coherent_peak_near(curve, n_stim, boundary):
    """engine_cli.hexa:6183."""
    frac = 0.50
    tol = 0.12
    n = len(curve)
    mx = curve[0]
    a = 1
    while a < n:
        if curve[a] > mx:
            mx = curve[a]
        a = a + 1
    if mx <= 0.0:
        return False
    thr = frac * mx
    t = 0
    while t < n:
        if curve[t] >= thr:
            is_max = False
            if t == 0:
                is_max = curve[t] > curve[t + 1]
            elif t == n - 1:
                is_max = curve[t] > curve[t - 1]
            else:
                is_max = (curve[t] > curve[t - 1]) and (curve[t] > curve[t + 1])
            if is_max:
                mid = (float(t) + 0.5) / float(n_stim - 1)
                if _absf(mid - boundary) <= tol:
                    return True
        t = t + 1
    return False


def _cp_source_pos_idx(proto, X):
    """engine_cli.hexa:6253."""
    return _vnearest_idx(X, proto)


def _cp_drift_pos1(cur, p_new, eta):
    """engine_cli.hexa:6259."""
    np_ = cur + eta * (p_new - cur)
    if (p_new - cur) >= 0.0:
        if np_ > p_new:
            np_ = p_new
    else:
        if np_ < p_new:
            np_ = p_new
    return np_


def _cp_advance_pos(pos, p_new, eta, n_phase1):
    """engine_cli.hexa:6326."""
    if eta <= 0.0:
        return pos
    out = []
    i = 0
    while i < len(pos):
        if i < n_phase1:
            out.append(_cp_drift_pos1(pos[i], p_new, eta))
        else:
            out.append(pos[i])
        i = i + 1
    return out


def _cp_repack(cp, pos, p_new, eta, n_phase1, dim):
    """engine_cli.hexa:6341."""
    if eta <= 0.0:
        return cp
    protos = []
    labels = []
    i = 0
    while i < cp.n:
        if i < n_phase1:
            np_ = _cp_drift_pos1(pos[i], p_new, eta)
            protos.append(cp_embed(np_, dim))
            labels.append(1 if np_ > p_new else 0)
        else:
            protos.append(cp.protos[i])
            labels.append(cp.labels[i])
        i = i + 1
    return CPField(protos, labels, cp.n)


def cp_relocate(cp0, X, positions, Y2, p_new, eta, n_phase1, dim, grow_max):
    """engine_cli.hexa:6277."""
    m = len(X)
    pos = []
    ip = 0
    while ip < cp0.n:
        pos.append(positions[_cp_source_pos_idx(cp0.protos[ip], X)])
        ip = ip + 1
    out = CPField(cp0.protos, cp0.labels, cp0.n)
    base = cp0.n
    p = 0
    while p < grow_max:
        if out.n >= base + grow_max:
            return out
        worst = -1
        worstd = 0.0
        found = False
        s2 = 0
        while s2 < m:
            ow = _cp_owner_idx(out, X[s2])
            if out.labels[ow] != Y2[s2]:
                dist = _l2(X[s2], out.protos[ow])
                if (not found) or dist < worstd:
                    worstd = dist
                    worst = s2
                    found = True
            s2 = s2 + 1
        if not found:
            out = _cp_repack(out, pos, p_new, eta, n_phase1, dim)
            return out
        out = CPField(out.protos + [X[worst]], out.labels + [Y2[worst]], out.n + 1)
        pos = pos + [positions[worst]]
        out = _cp_repack(out, pos, p_new, eta, n_phase1, dim)
        pos = _cp_advance_pos(pos, p_new, eta, n_phase1)
        p = p + 1
    return out


# ════════════════════════════════════════════════════════════════════════
# JamoHead (§KoJamoCountHead H_1316/1321/1351) — Voronoi count-MLE next-sym head
# ════════════════════════════════════════════════════════════════════════

class JamoHead:
    """engine_cli.hexa:6401."""
    __slots__ = ("centers", "heads", "vj", "dim")

    def __init__(self, centers, heads, vj, dim):
        self.centers = centers
        self.heads = heads
        self.vj = vj
        self.dim = dim


def _jh_field(centers, max_cells):
    """engine_cli.hexa:6409."""
    return VAdaptField(centers, len(centers), max_cells, len(centers[0]))


def _jh_assign(af, X):
    """engine_cli.hexa:6414."""
    owner = []
    i = 0
    while i < len(X):
        owner.append(vadapt_field_nearest_idx(af, X[i]))
        i = i + 1
    return owner


def _jh_counts(Y, owner, k, ntr, vj, laplace):
    """engine_cli.hexa:6423."""
    counts = []
    v = 0
    while v < vj:
        counts.append(laplace)
        v = v + 1
    total = laplace * float(vj)
    i = 0
    while i < ntr:
        if owner[i] == k:
            counts[Y[i]] = counts[Y[i]] + 1.0
            total = total + 1.0
        i = i + 1
    p = []
    w = 0
    while w < vj:
        p.append(counts[w] / total)
        w = w + 1
    return p


def _jh_owned_ce(Y, owner, k, ntr, p):
    """engine_cli.hexa:6440."""
    s = 0.0
    n = 0
    i = 0
    while i < ntr:
        if owner[i] == k:
            s = s - _ln(p[Y[i]] + 0.000000000001)
            n = n + 1
        i = i + 1
    if n == 0:
        return 0.0
    return s / float(n)


def _jh_owned_count(owner, k, ntr):
    """engine_cli.hexa:6450."""
    n = 0
    i = 0
    while i < ntr:
        if owner[i] == k:
            n = n + 1
        i = i + 1
    return n


def _jh_hi_var_axis(X, owner, k, ntr, dim):
    """engine_cli.hexa:6456."""
    sum_ = []
    sq = []
    d = 0
    while d < dim:
        sum_.append(0.0)
        sq.append(0.0)
        d = d + 1
    n = 0
    i = 0
    while i < ntr:
        if owner[i] == k:
            a = 0
            while a < dim:
                sum_[a] = sum_[a] + X[i][a]
                sq[a] = sq[a] + X[i][a] * X[i][a]
                a = a + 1
            n = n + 1
        i = i + 1
    if n == 0:
        return 0
    fn2 = float(n)
    best = 0
    bestv = -1.0
    a2 = 0
    while a2 < dim:
        mean = sum_[a2] / fn2
        var = sq[a2] / fn2 - mean * mean
        if var > bestv:
            bestv = var
            best = a2
        a2 = a2 + 1
    return best


def _jh_owned_median(X, owner, k, ntr, ax):
    """engine_cli.hexa:6480 — insertion-sort median."""
    vals = []
    i = 0
    while i < ntr:
        if owner[i] == k:
            vals.append(X[i][ax])
        i = i + 1
    n = len(vals)
    if n == 0:
        return 0.0
    a = 1
    while a < n:
        key = vals[a]
        b = a - 1
        while b >= 0 and vals[b] > key:
            vals[b + 1] = vals[b]
            b = b - 1
        vals[b + 1] = key
        a = a + 1
    if n % 2 == 1:
        return vals[n // 2]
    return (vals[n // 2 - 1] + vals[n // 2]) / 2.0


def _jh_half_centroid(X, owner, k, ntr, ax, med, lo, dim):
    """engine_cli.hexa:6495."""
    acc = []
    d = 0
    while d < dim:
        acc.append(0.0)
        d = d + 1
    n = 0
    i = 0
    while i < ntr:
        if owner[i] == k:
            take = (X[i][ax] <= med) if lo else (X[i][ax] > med)
            if take:
                a = 0
                while a < dim:
                    acc[a] = acc[a] + X[i][a]
                    a = a + 1
                n = n + 1
        i = i + 1
    if n == 0:
        return acc
    out = []
    a2 = 0
    while a2 < dim:
        out.append(acc[a2] / float(n))
        a2 = a2 + 1
    return out


def _jh_half_count(X, owner, k, ntr, ax, med, lo):
    """engine_cli.hexa:6516."""
    n = 0
    i = 0
    while i < ntr:
        if owner[i] == k:
            take = (X[i][ax] <= med) if lo else (X[i][ax] > med)
            if take:
                n = n + 1
        i = i + 1
    return n


def jamo_head_new(seed_centers, vj, dim):
    """engine_cli.hexa:6530."""
    return JamoHead(seed_centers, [], vj, dim)


def jamo_head_cells(jh):
    """engine_cli.hexa:6535."""
    return len(jh.centers)


def jamo_head_grow(jh, Xtr, Ytr, ntr, grow_max, min_owned, split_thresh_ce, laplace, cfg):
    """engine_cli.hexa:6541 — error-targeted Voronoi split-grow, mitosis-gated."""
    dim = jh.dim
    vj = jh.vj
    centers = jh.centers
    af = _jh_field(centers, grow_max)
    while len(centers) < grow_max:
        owner = _jh_assign(af, Xtr)
        nc = len(centers)
        local_ce = []
        owned_n = []
        k = 0
        while k < nc:
            cnt = _jh_owned_count(owner, k, ntr)
            owned_n.append(cnt)
            if cnt > 0:
                p = _jh_counts(Ytr, owner, k, ntr, vj, laplace)
                local_ce.append(_jh_owned_ce(Ytr, owner, k, ntr, p))
            else:
                local_ce.append(-1.0)
            k = k + 1
        elig = []
        k2 = 0
        while k2 < nc:
            if owned_n[k2] >= min_owned and local_ce[k2] > split_thresh_ce:
                elig.append(k2)
            k2 = k2 + 1
        if len(elig) == 0:
            break
        pick = elig[0]
        bestce = local_ce[elig[0]]
        ei = 1
        while ei < len(elig):
            if local_ce[elig[ei]] > bestce:
                bestce = local_ce[elig[ei]]
                pick = elig[ei]
            ei = ei + 1
        grown = engine_mitosis_tick(len(centers), cfg)
        if grown <= len(centers):
            break
        ax = _jh_hi_var_axis(Xtr, owner, pick, ntr, dim)
        med = _jh_owned_median(Xtr, owner, pick, ntr, ax)
        nlo = _jh_half_count(Xtr, owner, pick, ntr, ax, med, True)
        nhi = _jh_half_count(Xtr, owner, pick, ntr, ax, med, False)
        if nlo == 0 or nhi == 0:
            break
        c_lo = _jh_half_centroid(Xtr, owner, pick, ntr, ax, med, True, dim)
        c_hi = _jh_half_centroid(Xtr, owner, pick, ntr, ax, med, False, dim)
        new_centers = []
        ci = 0
        while ci < len(centers):
            if ci != pick:
                new_centers.append(centers[ci])
            ci = ci + 1
        new_centers = new_centers + [c_lo, c_hi]
        centers = new_centers
        af = _jh_field(centers, grow_max)
    own_tr = _jh_assign(af, Xtr)
    heads = []
    k = 0
    while k < len(centers):
        heads.append(_jh_counts(Ytr, own_tr, k, ntr, vj, laplace))
        k = k + 1
    return JamoHead(centers, heads, vj, dim)


def jamo_head_ce(jh, Xte, Yte):
    """engine_cli.hexa:6603."""
    if len(jh.heads) == 0:
        return 0.0
    af = _jh_field(jh.centers, len(jh.centers))
    own_te = _jh_assign(af, Xte)
    s = 0.0
    n = 0
    i = 0
    while i < len(Xte):
        s = s - _ln(jh.heads[own_te[i]][Yte[i]] + 0.000000000001)
        n = n + 1
        i = i + 1
    if n == 0:
        return 0.0
    return s / float(n)


def jamo_head_shuffle_targets(Y, vj, seed):
    """engine_cli.hexa:6626 — Fisher-Yates LCG position permutation."""
    n = len(Y)
    perm = []
    q = 0
    while q < n:
        perm.append(q)
        q = q + 1
    s = seed
    i = n - 1
    while i > 0:
        s = (s * 1103515245 + 12345) % 2147483648
        j = s % (i + 1)
        tmp = perm[i]
        perm[i] = perm[j]
        perm[j] = tmp
        i = i - 1
    out = []
    m = 0
    while m < n:
        out.append(Y[perm[m]])
        m = m + 1
    return out


def jamo_head_argmax(jh, feat):
    """engine_cli.hexa:6818."""
    if len(jh.heads) == 0:
        return -1
    af = _jh_field(jh.centers, len(jh.centers))
    owner = vadapt_field_nearest_idx(af, feat)
    if owner < 0 or owner >= len(jh.heads):
        return -1
    row = jh.heads[owner]
    best = 0
    bestp = row[0]
    k = 1
    while k < len(row):
        if row[k] > bestp:
            bestp = row[k]
            best = k
        k = k + 1
    return best


def jamo_head_recon_err(jh, feat):
    """engine_cli.hexa:6842."""
    if len(jh.heads) == 0:
        return 1000000000.0
    af = _jh_field(jh.centers, len(jh.centers))
    return vadapt_field_recon_err(af, feat)


# ════════════════════════════════════════════════════════════════════════
# BpeMerges (§KoMorphologyBpe H_1388) — BPE merges over jamo stream + byte-fair CE
# ════════════════════════════════════════════════════════════════════════

class BpeMerges:
    """engine_cli.hexa:6679."""
    __slots__ = ("merges", "next_id")

    def __init__(self, merges, next_id):
        self.merges = merges
        self.next_id = next_id


def _bpe_pair_counts(sym, n):
    """engine_cli.hexa:6686."""
    pa = []
    pb = []
    pc = []
    i = 0
    while i < n - 1:
        a = sym[i]
        b = sym[i + 1]
        found = -1
        j = 0
        while j < len(pa):
            if pa[j] == a and pb[j] == b:
                found = j
                j = len(pa)
            else:
                j = j + 1
        if found >= 0:
            pc[found] = pc[found] + 1
        else:
            pa.append(a)
            pb.append(b)
            pc.append(1)
        i = i + 1
    return [pa, pb, pc]


def _bpe_apply_one(sym, nby, a, b, nid):
    """engine_cli.hexa:6703."""
    n = len(sym)
    osym = []
    onby = []
    i = 0
    while i < n:
        if i < n - 1 and sym[i] == a and sym[i + 1] == b:
            osym.append(nid)
            onby.append(nby[i] + nby[i + 1])
            i = i + 2
        else:
            osym.append(sym[i])
            onby.append(nby[i])
            i = i + 1
    return [osym, onby]


def bpe_learn_merges(base_sym, base_nby, num_merges, base_vj, rnd_seed):
    """engine_cli.hexa:6724."""
    sym = base_sym
    nby = base_nby
    next_id = base_vj
    merges = []
    s = rnd_seed
    m = 0
    while m < num_merges:
        n = len(sym)
        if n < 2:
            m = num_merges
        else:
            pc = _bpe_pair_counts(sym, n)
            pa = pc[0]
            pbb = pc[1]
            pcc = pc[2]
            if len(pa) == 0:
                m = num_merges
            else:
                pick = 0
                if rnd_seed == 0:
                    bc = pcc[0]
                    ba = pa[0]
                    bb = pbb[0]
                    k = 1
                    while k < len(pa):
                        better = (pcc[k] > bc) \
                            or (pcc[k] == bc and pa[k] > ba) \
                            or (pcc[k] == bc and pa[k] == ba and pbb[k] > bb)
                        if better:
                            bc = pcc[k]
                            ba = pa[k]
                            bb = pbb[k]
                            pick = k
                        k = k + 1
                else:
                    s = (s * 1103515245 + 12345) % 2147483648
                    pick = s % len(pa)
                a = pa[pick]
                b = pbb[pick]
                nid = next_id
                merges = merges + [[a, b, nid]]
                next_id = next_id + 1
                re = _bpe_apply_one(sym, nby, a, b, nid)
                sym = re[0]
                nby = re[1]
                m = m + 1
    return BpeMerges(merges, next_id)


def bpe_apply(bm, base_sym, base_nby):
    """engine_cli.hexa:6770."""
    sym = base_sym
    nby = base_nby
    i = 0
    while i < len(bm.merges):
        mr = bm.merges[i]
        re = _bpe_apply_one(sym, nby, mr[0], mr[1], mr[2])
        sym = re[0]
        nby = re[1]
        i = i + 1
    return [sym, nby]


def bpe_unit_vocab(bm):
    """engine_cli.hexa:6784."""
    return bm.next_id


def bpe_n_units(unit_sym):
    """engine_cli.hexa:6787."""
    return len(unit_sym)


def bpe_byte_fair_ce(jh, Xte, Yte, nby_te):
    """engine_cli.hexa:6795."""
    if len(jh.heads) == 0:
        return 0.0
    af = _jh_field(jh.centers, len(jh.centers))
    own_te = _jh_assign(af, Xte)
    s = 0.0
    tot_bytes = 0
    i = 0
    while i < len(Xte):
        s = s - _ln(jh.heads[own_te[i]][Yte[i]] + 0.000000000001)
        tot_bytes = tot_bytes + nby_te[i]
        i = i + 1
    if tot_bytes == 0:
        return 0.0
    return s / float(tot_bytes)


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

    # ── OsmoticStore (H_1569) ──
    ost = osmotic_store_new([0.0, 0.0, 0.0, 0.0], [0.0, 0.0], 8)
    ost = osmotic_learn(ost, [1.0, 0.0, 0.0, 0.0], [1.0, 0.0], cfg_on, 1, 0.5, 0.35, -1.0)
    ost = osmotic_learn(ost, [0.0, 1.0, 0.0, 0.0], [0.0, 1.0], cfg_on, 1, 0.5, 0.35, -1.0)
    ost = osmotic_learn(ost, [1.0, 0.0, 0.0, 0.0], [0.9, 0.1], cfg_on, 0, 0.0, 0.0, -1.0)
    _p("osm_cells", osmotic_cells(ost))
    _p("osm_split_kl", osmotic_should_split(ost, [0.5, 0.5, 0.0, 0.0], [0.4, 0.6],
                                            1, 0.5, 0.35, -1.0))
    _p("osm_retain_b", osmotic_retains(ost, [0.0, 1.0, 0.0, 0.0], [0.0, 1.0], 0.15))

    # ── ImmuneMemoryGrow (§GrowImmune H_1288) — grow + LRU evict ──
    mg = immune_grow_new(immune_embed_key("alpha fact"), "A", 2, 4, True)
    mg = immune_grow_bind(mg, immune_embed_key("beta fact"), "B", cfg_on)
    mg = immune_grow_bind(mg, immune_embed_key("gamma fact"), "C", cfg_on)
    mg = immune_grow_bind(mg, immune_embed_key("delta fact"), "D", cfg_on)
    mg = immune_grow_bind(mg, immune_embed_key("epsilon fact"), "E", cfg_on)
    _p("mg_cells", immune_grow_cells(mg))
    _p("mg_recall_e", immune_grow_recall(mg, immune_embed_key("epsilon fact")))
    _p("mg_recall_ood", "[" + immune_grow_recall(mg, immune_embed_key("zzz nothing")) + "]")

    # ── CLSStore (§CLS H_1532) — AB-AC interference / two-store ──
    _p("cls_one", cls_one_store_retention(6, 6, 72, 0.30, 0.30))
    _p("cls_two", cls_two_store_retention(6, 6, 72, 0.30, 0.30, False, False))
    _p("cls_merge", cls_two_store_retention(6, 6, 72, 0.30, 0.30, True, False))
    _p("cls_shuffle", cls_two_store_retention(6, 6, 72, 0.30, 0.30, False, True))
    _p("cls_single", cls_single_encode_retention(6, 6, 72, 0.30, 0.30))

    # ── SkillStore (§SkillStore H_1378) — failure-driven teach ──
    ss = skill_store_new("search the web for x", "web_search", 8)
    ss = skill_store_teach(ss, "read a local file", "file_read", cfg_on)
    ss = skill_store_teach(ss, "read a local file", "file_read", cfg_on)
    _p("ss_cells", skill_store_cells(ss))
    _p("ss_recall_file", skill_recall(ss, "read a local file"))
    _p("ss_recall_ood", "[" + skill_recall(ss, "qqq unrelated far task") + "]")

    # ── UsageStore (§UsageStore H_1391) — usage learning twin ──
    us = usage_store_new("write json", "file_write", "syntax error",
                         "indent=2", "open|write|close", 8)
    us = usage_store_teach(us, "send email", "smtp", "auth fail",
                           "use tls", "connect|auth|send", cfg_on)
    _p("us_cells", usage_store_cells(us))
    _p("us_recall_arg", usage_recall(us, "send email", "smtp", "auth fail"))
    _p("us_recall_steps", usage_recall_steps(us, "send email", "smtp", "auth fail"))
    _p("us_recall_ood", "[" + usage_recall(us, "qqq", "qqq", "qqq") + "]")

    # ── Affect / Homeostatic / Libido shared immune store ──
    am = immune_grow_new(immune_embed_key("the sky is blue"), "blue", 8, 8, True)
    am = immune_grow_bind(am, immune_embed_key("grass is green"), "green", cfg_on)

    # ── AffectFeatures (§Affect H_1290) ──
    af_f = affect_substrate_features(am, immune_embed_key("the sky is blue"), "blue")
    _p("aff_val_g", affect_valence(af_f))
    _p("aff_aro_g", affect_arousal(af_f))
    _p("aff_emit_g", affect_emit_decision(af_f))
    af_ood = affect_substrate_features(am, immune_embed_key("zzz unknown thing"), "")
    _p("aff_val_o", affect_valence(af_ood))
    _p("aff_emit_o", affect_emit_decision(af_ood))
    af_rd = affect_read(am, immune_embed_key("the sky is blue"), "blue")
    _p("aff_read0", af_rd[0])
    _p("aff_read1", af_rd[1])
    shuf = affect_shuffle_features([af_f, af_ood], 4290)
    _p("aff_shuf0_val", affect_valence(shuf[0]))

    # ── HomeostaticDrive (§Hypothalamus H_1292) ──
    hd = homeo_new()
    hd = homeo_step(hd, am, immune_embed_key("zzz deprive one"))
    hd = homeo_step(hd, am, immune_embed_key("zzz deprive two"))
    hd = homeo_step(hd, am, immune_embed_key("zzz deprive three"))
    _p("homeo_rise", homeo_last(hd))
    hd2 = homeo_step(hd, am, immune_embed_key("the sky is blue"))
    _p("homeo_reset", homeo_last(hd2))
    _p("homeo_drive_o", homeo_drive(hd, am, immune_embed_key("zzz deprive four")))
    hda = homeo_new_ablated()
    hda = homeo_step(hda, am, immune_embed_key("zzz deprive one"))
    hda = homeo_step(hda, am, immune_embed_key("zzz deprive two"))
    hda = homeo_step(hda, am, immune_embed_key("zzz deprive three"))
    _p("homeo_ablate", homeo_last(hda))

    # ── Libido (§Libido H_1504) — wanting≠liking ──
    cue = immune_embed_key("grass is green")
    ld = libido_new()
    ld = libido_step(ld, am, immune_embed_key("zzz deprive lib"), cue)
    _p("lib_want", libido_last(ld))
    _p("lib_like", libido_liking(ld, libido_cue_match(am, cue)))
    ld_da = libido_new_da(1.0)
    ld_da = libido_step(ld_da, am, immune_embed_key("zzz deprive lib"), cue)
    _p("lib_want_da", libido_last(ld_da))
    _p("lib_like_da", libido_liking(ld_da, libido_cue_match(am, cue)))
    ld_ab = libido_new_ablated()
    ld_ab = libido_step(ld_ab, am, immune_embed_key("zzz deprive lib"), cue)
    _p("lib_want_ablate", libido_last(ld_ab))

    # ── Allosteric buffer (§Allosteric H_1509) — exp/sin/LCG parity ──
    _p("allo_mu_fp", allo_mu(0.5, 1.0, 0.12))
    _p("allo_mu_dev", allo_mu(0.8, 1.0, 0.12))
    _p("allo_rms", allo_defend(0.4, 1.0, 0.12, 42, 0))
    _p("allo_rms_shuf", allo_defend(0.4, 1.0, 0.12, 42, 1))
    _p("allo_best_fixed", allo_best_fixed_gain(0.12, 42))

    # ── OtherMindModel (§ToM H_1293) — Sally-Anne false belief ──
    om = other_mind_new()
    om = other_mind_witness(om, "ball location", "basket")
    _p("om_count", other_mind_count(om))
    _p("om_stale", other_mind_predict(om, "ball location"))
    om = other_mind_witness(om, "ball location", "box")
    _p("om_updated", other_mind_predict(om, "ball location"))
    _p("om_abstain", "[" + other_mind_predict(om, "weather today") + "]")

    # ── ConsolidatingMemory (§SleepReplay H_1228) ──
    cm = consolidating_memory_new(immune_embed_key("fact one"), "one", 1.0, 8)
    cm = consolidating_memory_bind_salient(cm, immune_embed_key("fact two"), "two", 0.5, cfg_on)
    cm = consolidating_memory_bind_salient(cm, immune_embed_key("fact three"), "three", 0.0, cfg_on)
    _p("cm_cells", consolidating_memory_cells(cm))
    _p("cm_sal0", consolidating_memory_salience(cm, 0))
    _p("cm_recall2", consolidating_memory_recall(cm, immune_embed_key("fact two")))
    cm_sh = consolidating_shuffle_salience(cm, 999)
    _p("cm_sh_sal0", consolidating_memory_salience(cm_sh, 0))
    gss = consolidating_lcg_gauss(777)
    _p("cm_gauss_z", gss[0])

    # ── VAdaptFieldB (§GateB H_1208) — ordered-walk predictable split ──
    afb = vadapt_fieldB_new(4, 32, 3, 0.34)
    walk = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    for c in walk:
        afb = vadapt_fieldB_step(afb, c, cfg_on)
    _p("afb_cells", vadapt_fieldB_cells(afb))
    _p("afb_growth", vadapt_fieldB_growth(afb))

    # ── WorkMemBuffer (§WorkMem H_1282) — gated leaky activation ──
    wm = wm_buffer_new(3, 0.8, 0.2, 4)
    wm = wm_buffer_gate_in(wm, [1.0, 0.0, 0.0, 0.0], 1.0)
    wm = wm_buffer_gate_in(wm, [0.0, 1.0, 0.0, 0.0], 1.0)
    wm = wm_buffer_gate_in(wm, [0.0, 0.0, 1.0, 0.0], 1.0)
    _p("wm_slots1", wm_buffer_slots(wm))
    wm = wm_buffer_distractor(wm, [0.0, 0.0, 0.0, 1.0])
    _p("wm_total", wm_buffer_total_activation(wm))
    _p("wm_probe", wm_buffer_probe_score(wm, [1.0, 0.0, 0.0, 0.0]))
    _p("wm_slots2", wm_buffer_slots(wm))

    # ── VForwardField (§Cerebellum H_1280) — NLMS learning curve ──
    ff = vforward_new(2, 1, 0.5)
    _p("vf_err0", vforward_err(ff, [1.0, 0.0], [0.0, 1.0]))
    ff = vforward_update(ff, [1.0, 0.0], [0.0, 1.0])
    ff = vforward_update(ff, [1.0, 0.0], [0.0, 1.0])
    _p("vf_err2", vforward_err(ff, [1.0, 0.0], [0.0, 1.0]))
    vfp = vforward_predict(ff, [1.0, 0.0])
    _p("vf_pred0", vfp[0])
    _p("vf_pred1", vfp[1])
    vfc = vforward_correct([1.0, 1.0], vfp, 0.5)
    _p("vf_corr0", vfc[0])

    # ── HierGoalStack (§HierPFC H_1294) — ordered subgoal pointer ──
    k1 = immune_embed_key("step one")
    k2 = immune_embed_key("step two")
    k3 = immune_embed_key("step three")
    hm = immune_grow_new(k1, "1", 8, 8, True)
    hm = immune_grow_bind(hm, k2, "2", cfg_on)
    hm = immune_grow_bind(hm, k3, "3", cfg_on)
    hs = hier_new([k1, k2, k3])
    hs = hier_step(hs, hm, k3)
    _p("hier_ptr_hold", hier_pointer(hs))
    hs = hier_step(hs, hm, k1)
    hs = hier_step(hs, hm, k2)
    hs = hier_step(hs, hm, k3)
    _p("hier_ptr_done", hier_pointer(hs))
    _p("hier_complete", hier_complete(hs))
    _p("hier_flat", hier_flat_emit(hm, [k2, k1]))

    # ── SpatialMap (§PlaceGrid H_1296) — relational nearest ──
    sm = spatial_map_new()
    sm = spatial_map_place(sm, "home", 0.0, 0.0)
    sm = spatial_map_place(sm, "park", 1.0, 0.0)
    sm = spatial_map_place(sm, "shop", 5.0, 0.0)
    _p("sm_near", spatial_map_nearest(sm, "home", "park", "shop"))
    _p("sm_count", spatial_map_count(sm))
    sm_sh = spatial_map_shuffle(sm, 12345)
    _p("sm_near_sh", spatial_map_nearest(sm_sh, "home", "park", "shop"))
    sm_ab = spatial_map_new_ablated()
    sm_ab = spatial_map_place(sm_ab, "home", 0.0, 0.0)
    sm_ab = spatial_map_place(sm_ab, "park", 1.0, 0.0)
    sm_ab = spatial_map_place(sm_ab, "shop", 5.0, 0.0)
    _p("sm_near_ab", spatial_map_nearest(sm_ab, "home", "park", "shop"))
    _p("sm_item", "[" + spatial_map_item_nearest("home", "park", "shop") + "]")

    # ── TransOrder (§TransitiveInf H_1429) — premise integration ──
    to = trans_order_new()
    to = trans_order_premise(to, "A", "B")
    to = trans_order_premise(to, "B", "C")
    to = trans_order_premise(to, "C", "D")
    to = trans_order_integrate(to)
    _p("to_ac", trans_order_higher(to, "A", "C"))
    _p("to_ad", trans_order_higher(to, "A", "D"))
    _p("to_item_ac", "[" + trans_order_item_higher(to, "A", "C") + "]")
    _p("to_count", trans_order_count(to))
    to_sh = trans_order_integrate(trans_order_shuffle(to, 7))
    _p("to_sh_ac", "[" + trans_order_higher(to_sh, "A", "C") + "]")

    # ── CircadianClock (§Circadian H_1298) ──
    ck = clock_new()
    for _i in range(8):
        ck = clock_step(ck)
    _p("clk_count", clock_count(ck))
    _p("clk_phase8", clock_phase(ck))
    _p("clk_fire8", clock_fire(ck))
    for _i in range(3):
        ck = clock_step(ck)
    _p("clk_phase11", clock_phase(ck))
    _p("clk_fire11", clock_fire(ck))
    cka = clock_new_ablated()
    for _i in range(5):
        cka = clock_step(cka)
    _p("clk_fire_ab", clock_fire(cka))

    # ── IntervalTimer (§IntervalTiming H_1299) ──
    it = itimer_new()
    it = itimer_observe(it, 0)
    it = itimer_observe(it, 13)
    it = itimer_observe(it, 26)
    it = itimer_observe(it, 39)
    _p("it_dhat", itimer_dhat(it))
    _p("it_ticks", itimer_dhat_ticks(it))
    _p("it_predict", itimer_predict_next(it))
    for _i in range(12):
        it = itimer_step(it)
    _p("it_fire", itimer_fire(it))

    # ── PhaseResetClock (§PhaseReset H_1301) — PRC sin ──
    pr = prc_new()
    for _i in range(30):
        pr = prc_step(pr, 1.0)
    _p("prc_phase", prc_phase(pr))
    _p("prc_count", prc_count(pr))
    pr2 = prc_zeitgeber(pr)
    _p("prc_phase_zg", prc_phase(pr2))

    # ── SCNNetwork (§SCN H_1302) — Kuramoto consensus (sin/cos/sqrt) ──
    scn = scn_run(scn_new(4297, 5), 100)
    _p("scn_order", scn_order(scn))
    _p("scn_consensus", scn_consensus(scn, 0.9))
    _p("scn_order_un", scn_order(scn_run(scn_new_uncoupled(4297, 5), 100)))
    _p("scn_order_fr", scn_order(scn_run(scn_new_frustrated(4297, 5), 100)))
    _p("scn_order_det", scn_order(scn_run(scn_detune(scn_new(4297, 5), 2.0), 100)))

    # ── PhaseField (§PhaseSyncBinding H_1448) — Kuramoto star binding ──
    pf = phasefield_run(phasefield_new(4448, 6), 80)
    _p("pf_coh", phasefield_coherence(pf))
    _p("pf_bound", phasefield_bound(pf, 0.9))
    pfd = phasefield_run(phasefield_new_desync(4448, 6), 80)
    _p("pf_coh_desync", phasefield_coherence(pfd))

    # ── QuorumPhase (§Quorum H_1510) — decentralized adjacency Kuramoto ──
    _p("qp_clorder", quorum_cluster_order(quorum_run(quorum_new(1510, 3, 4), 80)))
    _p("qp_cross_plv", quorum_cross_plv(quorum_new(1510, 3, 4), 16))
    _p("qp_within_plv", quorum_within_plv(quorum_new(1510, 3, 4), 16))
    _p("qp_drop", quorum_drop_node_order(1510, 3, 4, 80))
    _p("qp_nohub", quorum_star_no_hub_order(1510, 3, 4, 80))
    _p("qp_starbase", quorum_star_baseline_order(1510, 3, 4, 80))
    sadj = quorum_shuffle_adj(1510, 3, 4)
    _p("qp_shuf", quorum_cluster_order(quorum_run(quorum_with_adj(1510, 3, 4, sadj), 80)))

    # ── engine_config_summary (introspection string) ──
    _p("cfg_summary", engine_config_summary(cfg_on))

    # ── CA3ReplayMemory (§CA3Replay H_1427) ──
    ca = ca3_replay_new(4, 2)
    ca = ca3_replay_observe(ca, 0, 1)
    ca = ca3_replay_observe(ca, 0, 1)
    ca = ca3_replay_observe(ca, 1, 2)
    ca = ca3_replay_observe(ca, 1, 2)
    ca = ca3_replay_observe(ca, 2, 3)
    _p("ca3_pred0", ca3_replay_predict(ca, 0))
    _p("ca3_pred2_abstain", ca3_replay_predict(ca, 2))
    _p("ca3_conf0", ca3_replay_conf(ca, 0))
    _p("ca3_marginal", ca3_replay_marginal(ca))
    _p("ca3_pred_ood", ca3_replay_predict(ca, 9))

    # ── GlobalWorkspace (§GWS H_1462) ──
    gw = gws_add(gws_add(gws_add(gws_new(1, True, 0.3), 0.9), 0.7), 0.2)
    _p("gws_winner", gws_winner(gw))
    _p("gws_count_inh", gws_count(gw))
    _p("gws_leak1", gws_leak(gw, 1))
    gwo = gws_add(gws_add(gws_add(gws_new(3, False, 0.3), 0.9), 0.7), 0.2)
    _p("gws_count_off", gws_count(gwo))

    # ── Habituation (§Habituation H_1465) ──
    hb = hab_new(3, 0.2)
    _p("hab_fresh", hab_response(hb, 0, 1.0))
    hb = hab_observe(hb, 0)
    hb = hab_observe(hb, 0)
    _p("hab_habituated", hab_response(hb, 0, 1.0))
    _p("hab_other", hab_response(hb, 1, 1.0))
    hb = hab_reset(hb, 0)
    _p("hab_reset", hab_response(hb, 0, 1.0))

    # ── G18-G31 scalar gates ──
    _p("g_surprise", surprise(0.8, 0.5))
    _p("g_surprise_raw", surprise_raw_error(0.8, 0.5))
    _p("g_learned_prec", learned_precision(0.1, 5.0, 0.4))
    _p("g_novelty", novelty(3.0, 0.5))
    _p("g_blink2", attn_blink_detect(2, 1.0))
    _p("g_blink1", attn_blink_detect(1, 1.0))
    _p("g_agency", agency_attribute(0.5, 0.5, 0.5))
    _p("g_agency_other", agency_other())
    _p("g_subjtime", subjective_time(11.0, 0.2, 0.06))
    _p("g_emotion", emotion_regulate(0.8, 0.6, 0.8))
    _p("g_forget", directed_forget_recall(1.0, 0.7, True))
    _p("g_body", body_ownership(1.0, 0.95))
    _p("g_divided", divided_perf(1.0, 1.0))
    _p("g_veto", veto_execute(1.0, 0.5, False))
    _p("g_rivalry", rivalry_transitions(10, 0.2))
    _p("g_change", change_detect(0.3, True))
    _p("g_imagery", imagery_activate(0.8, True))
    _p("g_priming", priming_facilitate(0.7, 0.5))

    # ── CollectivePool / HiveMind (§CollectivePool H_1295) — faithful IIT-4 Φ ──
    cp = collective_new([110, 110], 0.6)
    _p("cp_member0_phi", collective_member_phi(cp, 0))
    _p("cp_sum_phi", collective_sum_phi(cp))
    _p("cp_joint_phi", collective_phi(cp))
    _p("cp_excess", collective_excess(cp))
    _p("cp_superadd", collective_is_super_additive(cp, 1.0))
    _p("cp_coherence", collective_coherence(cp))
    cp2 = collective_new([30, 90], 0.4)
    _p("cp2_joint_phi", collective_phi(cp2))
    _p("cp2_coherence", collective_coherence(cp2))

    # ── SkillCell (§SkillGrow H_1300) — ridge-LSQ heads + mitosis Voronoi grow ──
    skx = [[0.0, 0.0], [0.1, 0.1], [3.0, 0.0], [3.1, 0.1],
           [0.0, 3.0], [0.1, 3.1], [3.0, 3.0], [3.1, 3.1]]
    sky = [0, 0, 1, 1, 1, 1, 0, 0]
    skcells = skill_grow(skx, sky, cfg_on)
    _p("sk_ncells", len(skcells))
    _p("sk_route0", skill_route(skcells, [], [0.05, 0.05]))
    _p("sk_route3", skill_route(skcells, [], [3.05, 3.05]))
    _p("sk_center00", skcells[0].center[0])
    _p("sk_headw000", skcells[0].head_w[0][0])
    _p("sk_headb00", skcells[0].head_b[0])
    skcells_off = skill_grow(skx, sky, cfg_off)
    _p("sk_ncells_off", len(skcells_off))
    sol = _sc_gauss_solve([[2.0, 1.0], [1.0, 3.0]], [[1.0], [2.0]])
    _p("sk_solve0", sol[0][0])
    _p("sk_solve1", sol[1][0])

    # ── SkillGradFT (§SkillGradFT H_1300) — shared softmax-linear net ──
    net = skill_gradft_new(2, 7)
    _p("gft_w000_init", net.w[0][0])
    net = skill_gradft_train(net, skx, sky)
    _p("gft_w000_trained", net.w[0][0])
    _p("gft_b0_trained", net.b[0])
    _p("gft_pred0", skill_gradft_pred(net, [0.05, 0.05]))
    _p("gft_pred3", skill_gradft_pred(net, [3.05, 3.05]))

    # ── CPField (§CategoricalPerception H_1325) — RBF Voronoi CP ──
    cpdim = 8
    cpn = 11
    cpX = cp_stimuli(cpn, cpdim)
    cppos = []
    cpi = 0
    while cpi < cpn:
        cppos.append(float(cpi) / 10.0)
        cpi = cpi + 1
    cpYa = cp_labels_boundary(cppos, 0.3333333333333333)
    cpfa = cp_fit(cpX, cpYa, 6, 30)
    _p("cp_fit_n", cpfa.n)
    cpcurve = cp_discrim_curve(cpfa, cpX)
    _p("cp_peak_count", cp_peak_count(cpcurve))
    _p("cp_peak_idx", cp_peak_loc_idx(cpcurve))
    _p("cp_post_mid", cp_posterior(cpfa, cpX[5]))
    _p("cp_curve3", cpcurve[3])
    _p("cp_margin", cp_within_cross_margin(cpcurve, cpn, 0.3333333333333333))
    _p("cp_coh_near", cp_coherent_peak_near(cpcurve, cpn, 0.3333333333333333))
    _p("cp_embed_val", cp_embed(0.4, cpdim)[2])
    cpYsh = cp_labels_shuffle(cppos, 4290)
    cpshsum = 0
    for v in cpYsh:
        cpshsum = cpshsum + v
    _p("cp_shuf_sum", cpshsum)
    # cp_regrow on a moved boundary
    cpYb = cp_labels_boundary(cppos, 0.6666666666666666)
    cprg = cp_regrow(cpfa, cpX, cpYb, 4, 30)
    _p("cp_regrow_n", cprg.n)
    # tagged fit_more (bilingual)
    cpXt = cp_stimuli_tagged(cpn, cpdim, 0, 1.0, 2)
    cpft = cp_fit(cpXt, cpYa, 6, 30)
    cpXt2 = cp_stimuli_tagged(cpn, cpdim, 1, 1.0, 2)
    cpfm = cp_fit_more(cpft, cpXt2, cpYb, 12, 30)
    _p("cp_fitmore_n", cpfm.n)
    _p("cp_tagkey4", cpXt[5][cpdim])
    # cp_relocate (geometric re-pack)
    cprel = cp_relocate(cpfa, cpX, cppos, cpYb, 0.6666666666666666, 0.5, cpfa.n, cpdim, 4)
    _p("cp_reloc_n", cprel.n)
    _p("cp_reloc_post", cp_posterior(cprel, cpX[7]))
