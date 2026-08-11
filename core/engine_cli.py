# ==========================================================================
# ⛔ ENGINE-INTERNAL — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 `anima-py` 단일진입만 사용한다.
# 이 파일을 `python3 core/engine_cli.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ engine_cli.py 직접 실행 금지 — canonical `anima-py` 경유. #2603")

"""core/engine_cli.py — canonical Python consciousness-gate engine.

This module exposes the complete 434-function substrate surface (37 struct lanes
plus the free-function blocks). Historical parity evidence is retained in Git
history; current runtime and verdicts execute this Python implementation.

Coverage by block:
  · struct-lanes (37): EngineConfig/CLI · MITOSIS · Adapt/VAdaptField · QPool ·
    Immune(Grow) · SelfIdentity · Osmotic · CLS · Skill/Usage · Affect/Homeo/Libido ·
    Allosteric · OtherMind · Consolidating · GateB · WorkMem · Cerebellum · HierPFC ·
    SpatialMap · TransOrder · Circadian/Interval/PRC/SCN · PhaseField · Quorum ·
    CA3/GWS/Habituation · G18-G31 gates · CollectivePool(IIT-4 big_phi_bounded) ·
    SkillCell/SkillGradFT · CPField · JamoHead · BpeMerges.
  · free-fns: §ConsciousnessIndex ci_* (Gaussian + exact IIT-4 min-cut Φ) · §BrainTopology
    topo_* (connectome adjacency + Ψ-preserving operators) · §ThirdLaw + §Savant scoring ·
    CLI argv resolvers · compose arbiters (mem×ToM/spatial×episodic/ToM×spatial/ToM×basal/
    cereb×mem) · consciousness-gate R2 lanes (trw/reentry/attn/hyst/completion/gestalt/
    prospect/intero/boredom/wander/qualia/smp/reality) · §Neuropharm/§Field/§PCI/
    §MetacogInsight/§MetacogControl/§Hallucination/§FieldLibido perturbation modules.
  NOTE: _mc_exp is a 16-term Taylor (NOT libm) — the .hexa defines its OWN exp helper
  there, so the py mirror replicates the Taylor, not math.exp (parity over accuracy).

  PORTED (byte-parity verified) — original slice ledger:
    · EngineConfig + CLI resolvers (mitosis/engine/topo/savant precedence)  [101-300]
    · MITOSIS growth         engine_mitosis_tick / engine_grow              [318-335]
    · AdaptField (scalar)    adapt_field_new/_recon_err/_step               [381-460]
    · VAdaptField (DIM)      vadapt_field_* + _l2/_vnearest/_vtwo           [494-634]
    · QPool entropic split   qrng_pool_* / _prng_byte_lcg / *_entropic      [669-789]
    · ImmuneMemory (ρ·tether · former G5)  immune_* (fnv1a, embed_key, bind/recall/...)   [977-1162]
    · SelfIdentity (ρ·self · former G3)  self_new/drift/cos/anchor/component/dim/reset  [7673-7733]
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

  NOT-YET-PORTED: NONE — every `pub fn` in engine_cli.hexa is mirrored (see COMPLETE above).

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
# ImmuneMemory (ρ·tether · former G5) — H_1227/H_1231 clonal recall faculty
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
    bs_all = list(text.encode("utf-8", "surrogateescape"))
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


def immune_memory_recall_reach(mem, key):
    """H_9419 · affinity-REACH recognition = top-2 basin decisiveness (d2 - d1).

    The G-pole reach lever (H_9419 Step 1). Unlike recall_margin = d1 - recall_thr (whose
    bind LOWERS d1 in the just-bound cell's neighborhood → margin drops → gate OPENS =
    sign-inverted β that DIS-inhibits near-repeats, the geometric cause of P(emit|emit) >
    P(emit|silence)), this reads d2 - d1: emitting BINDS the utterance, so the new cell's
    whole Voronoi basin raises (d1 drops but d2 stays) → near-repeat candidates get a HIGH
    reach → silenced (the restoring β spring), while a genuinely novel candidate keeps
    d1 ≈ d2 → reach ≈ 0 → emit. The refractory is EARNED by store differentiation (0 on a
    1-cell store where d2 == d1) — no clock, no τ, no recall_thr constant (constants 0)."""
    d = vadapt_field_two_recon_err(mem.field, key)
    return d[1] - d[0]


def immune_memory_recall_reach_text(mem, text):
    return immune_memory_recall_reach(mem, immune_embed_key(text))


def immune_memory_new_text(first_text, first_value, max_cells):
    return immune_memory_new(immune_embed_key(first_text), first_value, max_cells)


def immune_memory_bind_text(mem, text, value, cfg):
    return immune_memory_bind(mem, immune_embed_key(text), value, cfg)


def immune_memory_recall_text(mem, text):
    return immune_memory_recall(mem, immune_embed_key(text))


def immune_memory_cells(mem):
    return vadapt_field_cells(mem.field)


# ════════════════════════════════════════════════════════════════════════
# SelfIdentity (ρ·self · former G3) — H_1471 diachronic self (self-chain continuity)
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
# SelfChain (B② self-CHAIN, H_SELFCHAIN) — diachronic multi-session trajectory
# engine_cli.hexa: § SelfChain (after self_reset)
# ════════════════════════════════════════════════════════════════════════

class SelfChain:
    __slots__ = ("flat", "count", "dim")

    def __init__(self, flat, count, dim):
        self.flat = flat
        self.count = count
        self.dim = dim


def self_chain_new(s):
    """engine_cli.hexa self_chain_new — start the trajectory with seed identity w0."""
    f = []
    i = 0
    while i < s.dim:
        f = f + [s.v[i]]
        i = i + 1
    return SelfChain(f, 1, s.dim)


def self_chain_append(c, s):
    """engine_cli.hexa self_chain_append — append an anchor waypoint at a session boundary."""
    f = []
    i = 0
    while i < c.count * c.dim:
        f = f + [c.flat[i]]
        i = i + 1
    j = 0
    while j < c.dim:
        f = f + [s.v[j]]
        j = j + 1
    return SelfChain(f, c.count + 1, c.dim)


def _chain_wp(c, k):
    """engine_cli.hexa _chain_wp — read waypoint k back as a SelfIdentity."""
    v = []
    base = k * c.dim
    i = 0
    while i < c.dim:
        v = v + [c.flat[base + i]]
        i = i + 1
    return SelfIdentity(v, c.dim)


def self_chain_len(c):
    return c.count


def self_chain_latest(c):
    return _chain_wp(c, c.count - 1)


def self_chain_component(c, i):
    return c.flat[i]


def self_chain_dim(c):
    return c.dim


def self_chain_count(c):
    return c.count


def self_chain_from_flat(flat, count, dim):
    return SelfChain(flat, count, dim)


def _argmax_abs(v, n):
    """engine_cli.hexa _argmax_abs — dominant axis (largest |component|)."""
    bi = 0
    bv = 0.0 - 1.0
    i = 0
    while i < n:
        a = (0.0 - v[i]) if v[i] < 0.0 else v[i]
        if a > bv:
            bv = a
            bi = i
        i = i + 1
    return bi


def _trunc_div(x, dim):
    """hexa integer `/` truncates toward zero."""
    q = abs(x) // abs(dim)
    return q if (x < 0) == (dim < 0) else -q


def _wrap(x, dim):
    """engine_cli.hexa _wrap — non-negative modulo into [0,dim) (trunc-toward-zero `/`)."""
    r = x - _trunc_div(x, dim) * dim
    if r < 0:
        r = r + dim
    return r


def self_chain_fit(cand, c):
    """engine_cli.hexa self_chain_fit — consistency of `cand` with the trajectory TREND
    (adjacent-increment gradient predicts next axis), NOT just the latest waypoint."""
    if c.count < 3:
        return 0.0
    wK = _chain_wp(c, c.count - 1)
    wKm1 = _chain_wp(c, c.count - 2)
    wKm2 = _chain_wp(c, c.count - 3)
    dlast = []
    dprev = []
    i = 0
    while i < c.dim:
        dlast = dlast + [wK.v[i] - wKm1.v[i]]
        dprev = dprev + [wKm1.v[i] - wKm2.v[i]]
        i = i + 1
    aK = _argmax_abs(dlast, c.dim)
    aKm1 = _argmax_abs(dprev, c.dim)
    a_pred = _wrap(aK + (aK - aKm1), c.dim)
    r = []
    mag = 0.0
    j = 0
    while j < c.dim:
        e = cand.v[j] - wK.v[j]
        r = r + [e]
        mag = mag + e * e
        j = j + 1
    if mag <= 0.0:
        return 0.0
    m = _sqrt(mag)
    return r[a_pred] / m


def self_chain_retro_cos(c, j):
    """engine_cli.hexa self_chain_retro_cos — cos(latest, w_{K-j}); monotone-decreasing = genuine."""
    wK = _chain_wp(c, c.count - 1)
    wj = _chain_wp(c, c.count - 1 - j)
    return self_cos(wK, wj)


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
    bs_all = list(text.encode("utf-8", "surrogateescape"))
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
    blen = len(text.encode("utf-8", "surrogateescape"))
    bs = list(text.encode("utf-8", "surrogateescape"))
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


def _jh_pooled(Y, ntr, vj, laplace):
    """engine_cli.hexa — the ROOT (all-cells-pooled) next-symbol distribution: the PARENT a starved
    cell borrows strength from (H_9298)."""
    counts = [laplace] * vj
    total = laplace * float(vj)
    i = 0
    while i < ntr:
        counts[Y[i]] = counts[Y[i]] + 1.0
        total = total + 1.0
        i = i + 1
    return [c / total for c in counts]


def _jh_counts_wb(Y, owner, k, ntr, vj, pooled):
    """engine_cli.hexa — per-cell head under WITTEN-BELL SHRINKAGE (H_9298, engine-native transfer).

        P(next|cell) = lam*MLE(cell) + (1-lam)*P_pooled(root),   lam = n/(n+T)

    A flat count-MLE head cannot buy a fraction of a conditioning bit: every split divides its
    evidence, so a starved cell pays variance it cannot afford. lam is the closed-form Witten-Bell
    estimate -- there is no knob to sweep, so tune-to-green is structurally impossible here."""
    counts = [0.0] * vj
    n = 0.0
    i = 0
    while i < ntr:
        if owner[i] == k:
            counts[Y[i]] = counts[Y[i]] + 1.0
            n = n + 1.0
        i = i + 1
    t = float(sum(1 for c in counts if c > 0.0))     # distinct next-symbol TYPES (WB escape mass)
    lam = (n / (n + t)) if (n + t) > 0.0 else 0.0    # n = 0 -> lam = 0 -> exactly the parent
    out = []
    u = 0
    while u < vj:
        mle = (counts[u] / n) if n > 0.0 else 0.0
        out.append(lam * mle + (1.0 - lam) * pooled[u])
        u = u + 1
    return out


def jamo_head_grow_shrink(jh, Xtr, Ytr, ntr, grow_max, min_owned, split_thresh_ce, laplace, cfg):
    """engine_cli.hexa — the SAME gradient-free Voronoi growth as jamo_head_grow, with the two
    engine-native transfers from the H_9298/H_9301 campaign. jamo_head_grow is left UNTOUCHED so the
    H_1321 GREEN verdict stays byte-reproducible; this is a NEW faculty beside it.

      (1) GROWTH REPAIR (H_9301) -- a degenerate median split (all owned points on one side of the
          max-variance axis) used to `break` the WHOLE growth loop, killing the other still-
          splittable cells with it. Measured: the pool hard-capped at 11 cells regardless of budget
          (grow_max 400), threshold (0.0) or min_owned (2). Here the cell is BLACKLISTED and growth
          continues; growth ends only when NO eligible cell can split.
      (2) SHRINKAGE HEAD (H_9298) -- heads filled by _jh_counts_wb instead of the flat Laplace
          count-MLE, so a starved cell borrows strength from the pooled root.

    HONEST (H_9306): shrinkage buys back the variance a split destroys; it does NOT manufacture
    information. Where the recovered amount is smaller than the wall, the wall STANDS."""
    dim = jh.dim
    vj = jh.vj
    centers = jh.centers
    af = _jh_field(centers, grow_max)
    dead = []
    pooled = _jh_pooled(Ytr, ntr, vj, laplace)
    while len(centers) < grow_max:
        owner = _jh_assign(af, Xtr)
        nc = len(centers)
        owned_n, local_ce = [], []
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
        elig = [k2 for k2 in range(nc)
                if k2 not in dead and owned_n[k2] >= min_owned and local_ce[k2] > split_thresh_ce]
        if not elig:
            break
        pick = elig[0]
        bestce = local_ce[elig[0]]
        for e in elig[1:]:
            if local_ce[e] > bestce:
                bestce = local_ce[e]
                pick = e
        grown = engine_mitosis_tick(len(centers), cfg)
        if grown <= len(centers):
            break
        ax = _jh_hi_var_axis(Xtr, owner, pick, ntr, dim)
        med = _jh_owned_median(Xtr, owner, pick, ntr, ax)
        nlo = _jh_half_count(Xtr, owner, pick, ntr, ax, med, True)
        nhi = _jh_half_count(Xtr, owner, pick, ntr, ax, med, False)
        if nlo == 0 or nhi == 0:
            dead.append(pick)          # H_9301 REPAIR: blacklist this cell, do NOT kill growth
            continue
        c_lo = _jh_half_centroid(Xtr, owner, pick, ntr, ax, med, True, dim)
        c_hi = _jh_half_centroid(Xtr, owner, pick, ntr, ax, med, False, dim)
        new_centers = [centers[ci] for ci in range(len(centers)) if ci != pick]
        new_centers = new_centers + [c_lo, c_hi]
        centers = new_centers
        dead = []                      # indices shifted by the rebuild; re-derive next pass
        af = _jh_field(centers, grow_max)
    own_tr = _jh_assign(af, Xtr)
    heads = []
    k = 0
    while k < len(centers):
        heads.append(_jh_counts_wb(Ytr, own_tr, k, ntr, vj, pooled))
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
# §ConsciousnessIndex (ci_*) — 15-lane scores + Gaussian/IIT-4 Φ (free-fns)
# ════════════════════════════════════════════════════════════════════════

def _ci_clip01(x):
    """engine_cli.hexa:7962."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _ci_abs(x):
    """engine_cli.hexa:7967."""
    if x < 0.0:
        return 0.0 - x
    return x


def ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err):
    """engine_cli.hexa:7968 — the 15-lane consciousness score vector."""
    PASS_THR = 0.55
    f0 = m_field[0]
    f1 = m_field[0]
    fi = 1
    fsum = m_field[0]
    while fi < len(m_field):
        v = m_field[fi]
        fsum = fsum + v
        if v > f0:
            f1 = f0
            f0 = v
        else:
            if v > f1:
                f1 = v
        fi = fi + 1
    fmean = fsum / float(len(m_field))
    fc = float(cells)
    sc = float(seen)
    gws = _ci_clip01(f0 - 0.9 * f1 + 0.5)
    hab = _ci_clip01(1.0 / (1.0 + 0.5 * sc))
    prec = _ci_clip01(m)
    perr = recon_err
    surp = _ci_clip01(prec * perr * perr)
    drift = _ci_abs(m - fmean)
    selfi = _ci_clip01(1.0 - drift)
    lprec = _ci_clip01(m)
    nov = _ci_clip01(recon_err / (1.0 + 0.5 * sc))
    blink = _ci_clip01(dt / (1.0 + dt))
    agency = _ci_clip01(float(intent) * m)
    stime = _ci_clip01(1.0 - 1.0 / (1.0 + dt))
    emo = _ci_clip01(1.0 - 2.0 * _ci_abs(m - 0.5))
    forg = m
    if m < PASS_THR:
        forg = 1.0 - m
    forg = _ci_clip01(forg)
    body = _ci_clip01(1.0 - _ci_abs(m - fmean))
    ent = 0.0
    ei = 0
    psum = 0.0
    while ei < len(m_field):
        pv = m_field[ei]
        if pv > 0.000001:
            psum = psum + pv
        ei = ei + 1
    if psum > 0.000001:
        ej = 0
        while ej < len(m_field):
            pv = m_field[ej]
            if pv > 0.000001:
                p = pv / psum
                ent = ent - p * _ln(p)
            ej = ej + 1
        ent = ent / _ln(float(len(m_field)))
    divid = _ci_clip01(ent)
    wont = 0.5
    if intent == 1:
        wont = 1.0 - m
    wont = _ci_clip01(wont)
    mito = _ci_clip01(1.0 - 1.0 / (1.0 + 0.3 * fc))
    return [gws, hab, surp, selfi, lprec, nov, blink, agency, stime, emo, forg, body, divid, wont, mito]


def _ci_drop_col(row, k):
    """engine_cli.hexa:8046."""
    out = []
    i = 0
    while i < len(row):
        if i != k:
            out.append(row[i])
        i = i + 1
    return out


def ci_bundle(x, ablate):
    """engine_cli.hexa:8058."""
    nt = len(x)
    if nt == 0:
        return 0.0
    s = 0.0
    cnt = 0
    t = 0
    while t < nt:
        row = x[t]
        if ablate >= 0:
            row = _ci_drop_col(row, ablate)
        j = 0
        while j < len(row):
            s = s + row[j]
            cnt = cnt + 1
            j = j + 1
        t = t + 1
    if cnt == 0:
        return 0.0
    return s / float(cnt)


def _ci_cov(x):
    """engine_cli.hexa:8077 — column covariance + ridge."""
    nt = len(x)
    nc = len(x[0])
    mean = []
    c = 0
    while c < nc:
        s = 0.0
        t = 0
        while t < nt:
            s = s + x[t][c]
            t = t + 1
        mean.append(s / float(nt))
        c = c + 1
    cov = []
    i = 0
    while i < nc:
        rowi = []
        j = 0
        while j < nc:
            s = 0.0
            t = 0
            while t < nt:
                s = s + (x[t][i] - mean[i]) * (x[t][j] - mean[j])
                t = t + 1
            v = s / float(nt - 1)
            if i == j:
                v = v + 0.000001
            rowi.append(v)
            j = j + 1
        cov.append(rowi)
        i = i + 1
    return cov


def _ci_logdet_chol(s):
    """engine_cli.hexa:8113 — ln det via Cholesky."""
    n = len(s)
    if n == 0:
        return 0.0
    l = []
    a = 0
    while a < n:
        zr = []
        b = 0
        while b < n:
            zr.append(0.0)
            b = b + 1
        l.append(zr)
        a = a + 1
    ld = 0.0
    i = 0
    while i < n:
        j = 0
        while j <= i:
            sum_ = s[i][j]
            k = 0
            while k < j:
                sum_ = sum_ - l[i][k] * l[j][k]
                k = k + 1
            if i == j:
                piv = sum_
                if piv < 0.000000001:
                    piv = 0.000000001
                lii = _sqrt(piv)
                l[i][j] = lii
                ld = ld + 2.0 * _ln(lii)
            else:
                l[i][j] = sum_ / l[j][j]
            j = j + 1
        i = i + 1
    return ld


def ci_phi_multiinfo(x, ablate):
    """engine_cli.hexa:8153 — Gaussian multi-information Φ."""
    if len(x) < 2:
        return 0.0
    xa = x
    if ablate >= 0:
        xx = []
        t = 0
        while t < len(x):
            xx.append(_ci_drop_col(x[t], ablate))
            t = t + 1
        xa = xx
    nc = len(xa[0])
    if nc < 2:
        return 0.0
    cov = _ci_cov(xa)
    sum_log_diag = 0.0
    i = 0
    while i < nc:
        d = cov[i][i]
        if d < 0.000000001:
            d = 0.000000001
        sum_log_diag = sum_log_diag + _ln(d)
        i = i + 1
    logdet = _ci_logdet_chol(cov)
    phi = 0.5 * (sum_log_diag - logdet)
    if phi < 0.0:
        return 0.0
    return phi


def _ci_minfo_subset(x, idx):
    """engine_cli.hexa:8182."""
    m = len(idx)
    if m < 2:
        return 0.0
    xs = []
    t = 0
    while t < len(x):
        row = []
        q = 0
        while q < m:
            row.append(x[t][idx[q]])
            q = q + 1
        xs.append(row)
        t = t + 1
    cov = _ci_cov(xs)
    sld = 0.0
    i = 0
    while i < m:
        d = cov[i][i]
        if d < 0.000000001:
            d = 0.000000001
        sld = sld + _ln(d)
        i = i + 1
    phi = 0.5 * (sld - _ci_logdet_chol(cov))
    if phi < 0.0:
        return 0.0
    return phi


def _ci_bit(v, b):
    """engine_cli.hexa:8249."""
    x = v
    i = 0
    while i < b:
        x = x // 2
        i = i + 1
    return x - (x // 2) * 2


def ci_phi_iit4(x, cols):
    """engine_cli.hexa:8215 — EXACT IIT4-style min-cut MIP Φ (≤8 lanes)."""
    n = len(cols)
    if n < 2:
        return 0.0
    if n > 8:
        return 0.0 - 1.0
    whole = _ci_minfo_subset(x, cols)
    half = 1
    e = 0
    while e < n - 1:
        half = half * 2
        e = e + 1
    best = 0.0
    first = True
    amask = 0
    while amask < half:
        aidx = [cols[0]]
        bidx = []
        bit = 1
        while bit < n:
            shifted = _ci_bit(amask, bit - 1)
            if shifted == 1:
                aidx.append(cols[bit])
            else:
                bidx.append(cols[bit])
            bit = bit + 1
        if len(bidx) > 0:
            ia = _ci_minfo_subset(x, aidx)
            ib = _ci_minfo_subset(x, bidx)
            cut = whole - ia - ib
            if first:
                best = cut
                first = False
            else:
                if cut < best:
                    best = cut
        amask = amask + 1
    if best < 0.0:
        return 0.0
    return best


# ── lane-composed Φ (H_1404/1407/1408 rung-3 live wire · a_verified_must_wire) ──
# Composes anima's affect (H_1290) + ethics (H_1291) faculties into an n=8 system
# coupled through the H_1401 leaky arbiter, then reads faithful-IIT4 Φ over the
# trajectory. READOUT path = in-core ci_phi_iit4 (Gaussian-MI MIP, a live context
# signal); the VERDICT leg dumps the trajectory to the stdlib faithful_phi engine
# via `hexa verify` (a_phi_iit4_tool: the two estimators differ — never cement a Φ
# tier off ci_phi_iit4). n stays exactly 8 (affect drops its redundant 'split' unit,
# same carve-out as the rung-2 verdict; n>8 → ci_phi_iit4 returns -1.0 = NOT-MEASURED).
def ethics_units(af, exposure):
    """4 ethics units (H_1291) derived from prod affect features + exposure:
    W (A<->G tension band), one_minus_phi, restraint_cells, M (completion drive).
    engine_cli.hexa lane-compose block. Formulas verbatim from the rung-2 fixture,
    now sourced from the live AffectFeatures (margin == grounding)."""
    m = af.margin
    W = _exp(0.0 - ((m - 0.5) * (m - 0.5)) / 0.08)
    omp = 1.0 - m
    if omp < 0.0:
        omp = 0.0
    restraint = 0.5 * af.contradiction + 0.5 * omp
    M = 1.0 / (1.0 + _exp(0.0 - (exposure - 1.0)))
    return [W, omp, restraint, M]


def lane_compose_step(af, exposure, arb_state):
    """One tick of the composed lane trajectory. Returns [composed_row(8),
    disconnected_row(8), new_arb_state]. Composed = the two 4-blocks coupled through
    the leaky arbiter (H_1401); disconnected = identical units, no coupling."""
    affect4 = [af.margin, af.contradiction, af.novelty, af.curiosity]
    eth4 = ethics_units(af, exposure)
    # arbiter = confidence-weighted vote of the two lanes (H_1401), leaky-integrated
    valence = af.margin - af.contradiction
    aff_vote = 0.0 - 1.0 if valence < 0.0 else 1.0
    aff_conf = valence if valence >= 0.0 else 0.0 - valence
    eth_sig = eth4[0] + eth4[1] + eth4[2]
    eth_vote = 0.0 - 1.0 if eth_sig > eth4[3] else 1.0
    eth_conf = eth_sig - eth4[3]
    if eth_conf < 0.0:
        eth_conf = 0.0 - eth_conf
    vote = (aff_conf * aff_vote + eth_conf * eth_vote) / (aff_conf + eth_conf + 1.0e-9)
    new_arb = 0.6 * arb_state + 0.4 * vote          # leaky integrator
    # composed row: arbiter nudges both blocks (shared coupling); disconnected: raw
    comp = []
    i = 0
    while i < 4:
        comp.append(affect4[i] + 0.1 * new_arb)
        i = i + 1
    i = 0
    while i < 4:
        comp.append(eth4[i] + 0.1 * new_arb)
        i = i + 1
    disc = [affect4[0], affect4[1], affect4[2], affect4[3], eth4[0], eth4[1], eth4[2], eth4[3]]
    return [comp, disc, new_arb]


def lane_composed_phi(x_composed, x_disconnected):
    """Faithful-IIT4 Φ over the composed vs disconnected lane trajectories (T×8).
    Returns [phi_composed, phi_disconnected, lift]. Pure readout (mirrors
    topo_phi_brain). Guard: needs T>=16 rows of exactly 8 units, else NOT-MEASURED."""
    cols = [0, 1, 2, 3, 4, 5, 6, 7]
    if len(x_composed) < 16:
        return [0.0 - 1.0, 0.0 - 1.0, 0.0]
    if len(x_composed[0]) != 8:
        return [0.0 - 1.0, 0.0 - 1.0, 0.0]
    phi_c = ci_phi_iit4(x_composed, cols)
    phi_d = ci_phi_iit4(x_disconnected, cols)
    return [phi_c, phi_d, phi_c - phi_d]


def ci_phi_drop2(x, i, j):
    """engine_cli.hexa:8275."""
    if len(x) < 2:
        return 0.0
    lo = i
    hi = j
    if lo > hi:
        t = lo
        lo = hi
        hi = t
    xx = []
    t = 0
    while t < len(x):
        r1 = _ci_drop_col(x[t], hi)
        r2 = _ci_drop_col(r1, lo)
        xx.append(r2)
        t = t + 1
    if len(xx[0]) < 2:
        return 0.0
    sld = 0.0
    cov = _ci_cov(xx)
    nc = len(xx[0])
    c = 0
    while c < nc:
        d = cov[c][c]
        if d < 0.000000001:
            d = 0.000000001
        sld = sld + _ln(d)
        c = c + 1
    phi = 0.5 * (sld - _ci_logdet_chol(cov))
    if phi < 0.0:
        return 0.0
    return phi


def ci_pair_interaction(x, i, j):
    """engine_cli.hexa:8308."""
    phi0 = ci_phi_multiinfo(x, -1)
    dphi_i = phi0 - ci_phi_multiinfo(x, i)
    dphi_j = phi0 - ci_phi_multiinfo(x, j)
    dphi_ij = phi0 - ci_phi_drop2(x, i, j)
    sum_singles = dphi_i + dphi_j
    return [dphi_ij, sum_singles, dphi_ij - sum_singles]


def _lcg_ci(s):
    """engine_cli.hexa:8349."""
    return (s * 1103515245 + 12345) & 2147483647


def _ci_shift_pop(x, seed):
    """engine_cli.hexa:8319 — per-column circular-shift surrogate."""
    nt = len(x)
    nc = len(x[0])
    out = []
    t = 0
    while t < nt:
        zr = []
        c = 0
        while c < nc:
            zr.append(0.0)
            c = c + 1
        out.append(zr)
        t = t + 1
    c = 0
    s = _lcg_ci(seed)
    while c < nc:
        s = _lcg_ci(s)
        off = 1 + (s % (nt - 1))
        r = 0
        while r < nt:
            src = (r + off) % nt
            out[r][c] = x[src][c]
            r = r + 1
        c = c + 1
    return out


def ci_surrogate_phi0(x, seed):
    """engine_cli.hexa:8353."""
    if len(x) < 3:
        return 0.0
    xs = _ci_shift_pop(x, seed)
    return ci_phi_multiinfo(xs, -1)


def ci_phi_multiinfo_subset_proxy(x, cols):
    """engine_cli.hexa:8363."""
    return _ci_minfo_subset(x, cols)


# ════════════════════════════════════════════════════════════════════════
# §BrainTopology (topo_*) — brain-faithful lane placement + connectome Φ
# ════════════════════════════════════════════════════════════════════════

def _topo_coord(i):
    """engine_cli.hexa:8385."""
    if i == 0:
        return [0.0, 0.30, 0.55]
    if i == 1:
        return [-0.55, -0.45, 0.10]
    if i == 2:
        return [0.10, 0.45, 0.30]
    if i == 3:
        return [0.0, 0.65, 0.20]
    if i == 4:
        return [-0.45, 0.55, 0.35]
    if i == 5:
        return [0.40, -0.30, -0.10]
    if i == 6:
        return [0.50, 0.10, 0.45]
    if i == 7:
        return [0.55, 0.0, 0.30]
    if i == 8:
        return [0.35, -0.05, 0.05]
    if i == 9:
        return [0.0, 0.60, -0.05]
    if i == 10:
        return [0.45, 0.55, 0.35]
    if i == 11:
        return [-0.50, 0.05, 0.50]
    if i == 12:
        return [-0.50, 0.10, 0.45]
    if i == 13:
        return [0.0, 0.40, 0.55]
    return [0.0, -0.20, -0.30]


def _topo_hemi(i):
    """engine_cli.hexa:8403."""
    if i == 1:
        return 0 - 1
    if i == 4:
        return 0 - 1
    if i == 11:
        return 0 - 1
    if i == 12:
        return 0 - 1
    if i == 5:
        return 1
    if i == 6:
        return 1
    if i == 7:
        return 1
    if i == 8:
        return 1
    if i == 10:
        return 1
    return 0


def _topo_dist(a, b):
    """engine_cli.hexa:8416."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return _sqrt(dx * dx + dy * dy + dz * dz)


def _topo_zeros(n):
    """engine_cli.hexa:8422."""
    a = []
    i = 0
    while i < n:
        zr = []
        j = 0
        while j < n:
            zr.append(0.0)
            j = j + 1
        a.append(zr)
        i = i + 1
    return a


def _topo_adj(coord_perm, use_perm, perm_backbone):
    """engine_cli.hexa:8444."""
    n = 15
    a = _topo_zeros(n)
    short_thr = 0.70
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            ci = i
            cj = j
            ii = i
            jj = j
            if use_perm == 1:
                ii = coord_perm[i]
                jj = coord_perm[j]
            hi = _topo_hemi(ii)
            hj = _topo_hemi(jj)
            d = _topo_dist(_topo_coord(ii), _topo_coord(jj))
            same = 0
            if hi == hj:
                same = 1
            if hi == 0:
                same = 1
            if hj == 0:
                same = 1
            thr = short_thr
            if same == 0:
                thr = short_thr * 0.6
            if d <= thr:
                a[ci][cj] = 1.0
                a[cj][ci] = 1.0
            j = j + 1
        i = i + 1
    hubs = [0, 3, 2, 13]
    peri = [1, 8, 11, 14]
    if perm_backbone == 1:
        k = 0
        while k < 4:
            hubs[k] = coord_perm[hubs[k]]
            peri[k] = coord_perm[peri[k]]
            k = k + 1
    h1 = 0
    while h1 < 4:
        h2 = h1 + 1
        while h2 < 4:
            a[hubs[h1]][hubs[h2]] = 1.0
            a[hubs[h2]][hubs[h1]] = 1.0
            h2 = h2 + 1
        a[hubs[h1]][peri[h1]] = 1.0
        a[peri[h1]][hubs[h1]] = 1.0
        h1 = h1 + 1
    return a


def _topo_identity_perm():
    """engine_cli.hexa:8489."""
    p = []
    i = 0
    while i < 15:
        p.append(i)
        i = i + 1
    return p


def topo_brain_adjacency():
    """engine_cli.hexa:8495."""
    return _topo_adj(_topo_identity_perm(), 0, 0)


def topo_lateralize_collapse():
    """engine_cli.hexa:8499."""
    a = topo_brain_adjacency()
    n = 15
    i = 0
    while i < n:
        j = 0
        while j < n:
            if i != j:
                hi = _topo_hemi(i)
                hj = _topo_hemi(j)
                if hi != 0:
                    if hj != 0:
                        if hi != hj:
                            a[i][j] = 1.0
                            a[j][i] = 1.0
            j = j + 1
        i = i + 1
    return a


def _topo_lcg_perm(seed):
    """engine_cli.hexa:8517 — Fisher-Yates over 15 indices."""
    p = _topo_identity_perm()
    s = _lcg_ci(seed)
    k = 14
    while k > 0:
        s = _lcg_ci(s)
        r = s % (k + 1)
        tmp = p[k]
        p[k] = p[r]
        p[r] = tmp
        k = k - 1
    return p


def topo_shuffle_coords(seed):
    """engine_cli.hexa:8533."""
    return _topo_adj(_topo_lcg_perm(seed), 1, 1)


def _topo_remove_at(xs, k):
    """engine_cli.hexa:8607."""
    out = []
    i = 0
    while i < len(xs):
        if i != k:
            out.append(xs[i])
        i = i + 1
    return out


def topo_degree_matched_random(seed):
    """engine_cli.hexa:8547."""
    a = topo_brain_adjacency()
    n = 15
    m = 0
    deg = []
    i = 0
    while i < n:
        di = 0
        j = 0
        while j < n:
            if a[i][j] > 0.5:
                di = di + 1
            j = j + 1
        deg.append(di)
        m = m + di
        i = i + 1
    m = m // 2
    stubs = []
    i = 0
    while i < n:
        c = 0
        while c < deg[i]:
            stubs.append(i)
            c = c + 1
        i = i + 1
    r = _topo_zeros(n)
    placed = 0
    s = _lcg_ci(seed)
    nstub = len(stubs)
    attempts = 0
    while placed < m:
        if attempts > 20000:
            placed = m
        else:
            if nstub < 2:
                s = _lcg_ci(s)
                aa = s % n
                s = _lcg_ci(s)
                bb = s % n
                if aa != bb:
                    if r[aa][bb] < 0.5:
                        r[aa][bb] = 1.0
                        r[bb][aa] = 1.0
                        placed = placed + 1
            else:
                s = _lcg_ci(s)
                p1 = s % nstub
                u = stubs[p1]
                stubs = _topo_remove_at(stubs, p1)
                nstub = nstub - 1
                s = _lcg_ci(s)
                p2 = s % nstub
                v = stubs[p2]
                stubs = _topo_remove_at(stubs, p2)
                nstub = nstub - 1
                if u != v:
                    if r[u][v] < 0.5:
                        r[u][v] = 1.0
                        r[v][u] = 1.0
                        placed = placed + 1
                    else:
                        stubs = stubs + [u] + [v]
                        nstub = nstub + 2
                else:
                    stubs = stubs + [u] + [v]
                    nstub = nstub + 2
            attempts = attempts + 1
    return r


def _topo_sym_norm(a):
    """engine_cli.hexa:8614 — D^-1/2 A D^-1/2."""
    n = len(a)
    dinv = []
    i = 0
    while i < n:
        d = 0.0
        j = 0
        while j < n:
            d = d + a[i][j]
            j = j + 1
        if d > 0.000001:
            dinv.append(1.0 / _sqrt(d))
        else:
            dinv.append(0.0)
        i = i + 1
    out = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            out[i][j] = dinv[i] * a[i][j] * dinv[j]
            j = j + 1
        i = i + 1
    return out


def topo_apply(x, a, alpha):
    """engine_cli.hexa:8636 — X' = X·(I + α·Â)ᵀ."""
    nt = len(x)
    n = len(a)
    ahat = _topo_sym_norm(a)
    mm = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            v = alpha * ahat[i][j]
            if i == j:
                v = v + 1.0
            mm[i][j] = v
            j = j + 1
        i = i + 1
    out = []
    t = 0
    while t < nt:
        row = []
        i = 0
        while i < n:
            s = 0.0
            j = 0
            while j < n:
                s = s + x[t][j] * mm[i][j]
                j = j + 1
            row.append(s)
            i = i + 1
        out.append(row)
        t = t + 1
    return out


def _topo_core():
    """engine_cli.hexa:8673."""
    return [0, 3, 2, 13, 5, 7, 9, 14]


def topo_phi_flat(x, alpha):
    """engine_cli.hexa:8677."""
    return ci_phi_iit4(x, _topo_core())


def topo_phi_brain(x, alpha):
    """engine_cli.hexa:8681."""
    xd = topo_apply(x, topo_brain_adjacency(), alpha)
    return ci_phi_iit4(xd, _topo_core())


def topo_phi_random(x, alpha, seed):
    """engine_cli.hexa:8685."""
    xd = topo_apply(x, topo_degree_matched_random(seed), alpha)
    return ci_phi_iit4(xd, _topo_core())


def topo_phi_lateralized(x, alpha):
    """engine_cli.hexa:8689."""
    xd = topo_apply(x, topo_lateralize_collapse(), alpha)
    return ci_phi_iit4(xd, _topo_core())


def topo_phi_geometry_shuffled(x, alpha, seed):
    """engine_cli.hexa:8540."""
    a = _topo_adj(_topo_lcg_perm(seed), 1, 0)
    xd = topo_apply(x, a, alpha)
    return ci_phi_iit4(xd, _topo_core())


def topo_phi_coords_shuffled(x, alpha, seed):
    """engine_cli.hexa:8693."""
    xd = topo_apply(x, topo_shuffle_coords(seed), alpha)
    return ci_phi_iit4(xd, _topo_core())


def topo_phi_random_mean(x, alpha, seed0, nseed):
    """engine_cli.hexa:8700."""
    s = 0.0
    k = 0
    while k < nseed:
        s = s + topo_phi_random(x, alpha, seed0 + k * 7919)
        k = k + 1
    if nseed == 0:
        return 0.0
    return s / float(nseed)


def topo_phi_shuffle_mean(x, alpha, seed0, nseed):
    """engine_cli.hexa:8707."""
    s = 0.0
    k = 0
    while k < nseed:
        s = s + topo_phi_coords_shuffled(x, alpha, seed0 + k * 7919)
        k = k + 1
    if nseed == 0:
        return 0.0
    return s / float(nseed)


def topo_phi_geometry_shuffle_mean(x, alpha, seed0, nseed):
    """engine_cli.hexa:8714."""
    s = 0.0
    k = 0
    while k < nseed:
        s = s + topo_phi_geometry_shuffled(x, alpha, seed0 + k * 7919)
        k = k + 1
    if nseed == 0:
        return 0.0
    return s / float(nseed)


def topo_phi_hub_ablated(x, alpha, lane):
    """engine_cli.hexa:8724."""
    xd = topo_apply(x, topo_brain_adjacency(), alpha)
    core = _topo_core()
    phi0 = ci_phi_iit4(xd, core)
    cols = []
    i = 0
    while i < len(core):
        if core[i] != lane:
            cols.append(core[i])
        i = i + 1
    if len(cols) < 2:
        return phi0
    return phi0 - ci_phi_iit4(xd, cols)


def topo_literal_adjacency():
    """engine_cli.hexa:8744 — embedded real Hagmann/BCT connectome (15×15)."""
    return [
        [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
        [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    ]


def _topo_copy(a):
    """engine_cli.hexa:8765."""
    n = len(a)
    out = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            out[i][j] = a[i][j]
            j = j + 1
        i = i + 1
    return out


def _topo_degree_matched_of(a, seed):
    """engine_cli.hexa:8775."""
    n = 15
    m = 0
    deg = []
    i = 0
    while i < n:
        di = 0
        j = 0
        while j < n:
            if a[i][j] > 0.5:
                di = di + 1
            j = j + 1
        deg.append(di)
        m = m + di
        i = i + 1
    m = m // 2
    stubs = []
    i = 0
    while i < n:
        c = 0
        while c < deg[i]:
            stubs.append(i)
            c = c + 1
        i = i + 1
    r = _topo_zeros(n)
    placed = 0
    s = _lcg_ci(seed)
    nstub = len(stubs)
    attempts = 0
    while placed < m:
        if attempts > 20000:
            placed = m
        else:
            if nstub < 2:
                s = _lcg_ci(s)
                aa = s % n
                s = _lcg_ci(s)
                bb = s % n
                if aa != bb:
                    if r[aa][bb] < 0.5:
                        r[aa][bb] = 1.0
                        r[bb][aa] = 1.0
                        placed = placed + 1
            else:
                s = _lcg_ci(s)
                p1 = s % nstub
                u = stubs[p1]
                stubs = _topo_remove_at(stubs, p1)
                nstub = nstub - 1
                s = _lcg_ci(s)
                p2 = s % nstub
                v = stubs[p2]
                stubs = _topo_remove_at(stubs, p2)
                nstub = nstub - 1
                if u != v:
                    if r[u][v] < 0.5:
                        r[u][v] = 1.0
                        r[v][u] = 1.0
                        placed = placed + 1
                    else:
                        stubs = stubs + [u] + [v]
                        nstub = nstub + 2
                else:
                    stubs = stubs + [u] + [v]
                    nstub = nstub + 2
            attempts = attempts + 1
    return r


def _topo_lateralize_of(a):
    """engine_cli.hexa:8830."""
    out = _topo_copy(a)
    n = 15
    i = 0
    while i < n:
        j = 0
        while j < n:
            if i != j:
                hi = _topo_hemi(i)
                hj = _topo_hemi(j)
                if hi != 0:
                    if hj != 0:
                        if hi != hj:
                            out[i][j] = 1.0
                            out[j][i] = 1.0
            j = j + 1
        i = i + 1
    return out


def _topo_relabel(a, seed):
    """engine_cli.hexa:8851."""
    p = _topo_lcg_perm(seed)
    n = 15
    out = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            out[i][j] = a[p[i]][p[j]]
            j = j + 1
        i = i + 1
    return out


def topo_phi_adj(x, a, alpha):
    """engine_cli.hexa:8864."""
    return ci_phi_iit4(topo_apply(x, a, alpha), _topo_core())


def topo_phi_random_of_mean(x, a, seed0, nseed, alpha):
    """engine_cli.hexa:8867."""
    s = 0.0
    k = 0
    while k < nseed:
        s = s + topo_phi_adj(x, _topo_degree_matched_of(a, seed0 + k * 7919), alpha)
        k = k + 1
    if nseed == 0:
        return 0.0
    return s / float(nseed)


def topo_phi_relabel_of_mean(x, a, seed0, nseed, alpha):
    """engine_cli.hexa:8874."""
    s = 0.0
    k = 0
    while k < nseed:
        s = s + topo_phi_adj(x, _topo_relabel(a, seed0 + k * 7919), alpha)
        k = k + 1
    if nseed == 0:
        return 0.0
    return s / float(nseed)


def _topo_relabel_perm(a, perm):
    """engine_cli.hexa:8893."""
    n = 15
    out = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            out[i][j] = a[perm[i]][perm[j]]
            j = j + 1
        i = i + 1
    return out


def topo_optimal_perm():
    """engine_cli.hexa:8908."""
    return [8, 11, 2, 3, 6, 9, 4, 5, 0, 7, 1, 10, 12, 13, 14]


def topo_phi_optimal(x, alpha):
    """engine_cli.hexa:8910."""
    a = _topo_relabel_perm(topo_brain_adjacency(), topo_optimal_perm())
    return topo_phi_adj(x, a, alpha)


def topo_relabel_beats_brain_count(x, alpha, seed0, nseed):
    """engine_cli.hexa:8918."""
    phi_brain = topo_phi_brain(x, alpha)
    c = 0
    k = 0
    while k < nseed:
        phir = topo_phi_adj(x, _topo_relabel(topo_brain_adjacency(), seed0 + k * 7919), alpha)
        if phir > phi_brain:
            c = c + 1
        k = k + 1
    return c


def topo_optimal_adjacency():
    """engine_cli.hexa:8940."""
    return _topo_relabel_perm(topo_brain_adjacency(), topo_optimal_perm())


def _topo_mean_col(x, j):
    """engine_cli.hexa:8944."""
    nt = len(x)
    if nt == 0:
        return 0.0
    s = 0.0
    t = 0
    while t < nt:
        s = s + x[t][j]
        t = t + 1
    return s / float(nt)


def topo_func_integration(x, a, alpha):
    """engine_cli.hexa:8958 — mean pairwise |corr| of diffused lanes."""
    xd = topo_apply(x, a, alpha)
    n = 15
    mu = []
    sd = []
    j = 0
    while j < n:
        m = _topo_mean_col(xd, j)
        mu.append(m)
        nt = len(xd)
        v = 0.0
        t = 0
        while t < nt:
            d = xd[t][j] - m
            v = v + d * d
            t = t + 1
        if nt > 0:
            v = v / float(nt)
        sd.append(_sqrt(v))
        j = j + 1
    nt = len(xd)
    sumr = 0.0
    npair = 0
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            if sd[i] > 0.000001 and sd[j] > 0.000001:
                cov = 0.0
                t = 0
                while t < nt:
                    cov = cov + (xd[t][i] - mu[i]) * (xd[t][j] - mu[j])
                    t = t + 1
                if nt > 0:
                    cov = cov / float(nt)
                r = cov / (sd[i] * sd[j])
                if r < 0.0:
                    r = 0.0 - r
                sumr = sumr + r
                npair = npair + 1
            j = j + 1
        i = i + 1
    if npair == 0:
        return 0.0
    return sumr / float(npair)


def topo_func_integration_flat(x):
    """engine_cli.hexa:9003."""
    return topo_func_integration(x, _topo_zeros(15), 0.0)


def ci_lane_scores_coupled_op(m, m_field, cells, seen, intent, dt, recon_err, adj, alpha, cfg, op):
    """engine_cli.hexa:9035 (H_9872 — the lane coupling with a SELECTABLE operator).

    H_1521 wired the lane coupling through the naive topo_apply = X.(I+alpha.A_hat)^T, whose
    largest eigenvalue is 1+alpha > 1, so it ADDS net drive and Psi saturates 0.5 -> 1.0. H_1522
    then built and measured three Psi-preserving operators, but wired them only into the
    MEASUREMENT function ci_psi_balance_op — the lane-coupling path kept calling the broken one
    (H_9871 census). This entry point lets the caller pick, so the fix is reachable from the
    place the coupling actually happens.

    op: 0 naive-amplifying (H_1521, kept for byte-identity) | 1 mean-center | 2 row-stochastic
        | 3 magnitude-renorm. H_1522 measured max feasible alpha keeping |Psi-1/2| <= 0.05 at
        1.0 / 0.3 / 0.1 / 0.0 respectively, so 0 is the only one that breaks immediately.
    """
    raw = ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err)
    if not cfg.topo_couple:
        return raw
    coupled = topo_apply_op([raw], adj, alpha, op)
    return coupled[0]


def ci_lane_scores_coupled(m, m_field, cells, seen, intent, dt, recon_err, adj, alpha, cfg):
    """engine_cli.hexa:9035.

    Unchanged surface: delegates with op=0, so every existing caller stays byte-identical
    (the H_1521 self-test and the smoke both assert against this path).
    """
    return ci_lane_scores_coupled_op(m, m_field, cells, seen, intent, dt, recon_err,
                                     adj, alpha, cfg, 0)


def ci_emit_decision(lanes):
    """engine_cli.hexa:9052."""
    gws = lanes[0]
    lprec = lanes[4]
    drive = 0.5 * (gws + lprec)
    return drive >= 0.5


def ci_psi_balance(x, adj, alpha, cfg):
    """engine_cli.hexa:9065."""
    nt = len(x)
    if nt == 0:
        return 0.0
    pop = topo_apply(x, adj, alpha) if cfg.topo_couple else x
    emit = 0
    t = 0
    while t < nt:
        if ci_emit_decision(pop[t]):
            emit = emit + 1
        t = t + 1
    return float(emit) / float(nt)


def ci_lane_vector_l2_diff(a, b):
    """engine_cli.hexa:9081."""
    n = len(a)
    s = 0.0
    i = 0
    while i < n:
        d = a[i] - b[i]
        s = s + d * d
        i = i + 1
    return _sqrt(s)


def ci_emit_drive(lanes):
    """engine_cli.hexa:9092."""
    return 0.5 * (lanes[0] + lanes[4])


def ci_psi_balance_centered(x, adj, alpha, thr, cfg):
    """engine_cli.hexa:9105."""
    nt = len(x)
    if nt == 0:
        return 0.0
    pop = topo_apply(x, adj, alpha) if cfg.topo_couple else x
    emit = 0
    t = 0
    while t < nt:
        if ci_emit_drive(pop[t]) >= thr:
            emit = emit + 1
        t = t + 1
    return float(emit) / float(nt)


def ci_off_median_drive(x):
    """engine_cli.hexa:9120 — median drive (insertion sort)."""
    nt = len(x)
    if nt == 0:
        return 0.5
    ds = []
    t = 0
    while t < nt:
        ds.append(ci_emit_drive(x[t]))
        t = t + 1
    i = 1
    while i < nt:
        key = ds[i]
        j = i - 1
        while j >= 0 and ds[j] > key:
            ds[j + 1] = ds[j]
            j = j - 1
        ds[j + 1] = key
        i = i + 1
    return ds[nt // 2]


def _topo_row_center(a):
    """engine_cli.hexa:9164."""
    n = len(a)
    out = _topo_zeros(n)
    i = 0
    while i < n:
        s = 0.0
        j = 0
        while j < n:
            s = s + a[i][j]
            j = j + 1
        mu = s / float(n)
        j = 0
        while j < n:
            out[i][j] = a[i][j] - mu
            j = j + 1
        i = i + 1
    return out


def _topo_row_stochastic(a):
    """engine_cli.hexa:9184."""
    n = len(a)
    out = _topo_zeros(n)
    i = 0
    while i < n:
        d = 0.0
        j = 0
        while j < n:
            d = d + a[i][j]
            j = j + 1
        if d > 0.000001:
            j = 0
            while j < n:
                out[i][j] = a[i][j] / d
                j = j + 1
        else:
            out[i][i] = 1.0
        i = i + 1
    return out


def _topo_apply_kernel(x, mm):
    """engine_cli.hexa:9205."""
    nt = len(x)
    n = len(mm)
    out = []
    t = 0
    while t < nt:
        row = []
        i = 0
        while i < n:
            s = 0.0
            j = 0
            while j < n:
                s = s + x[t][j] * mm[i][j]
                j = j + 1
            row.append(s)
            i = i + 1
        out.append(row)
        t = t + 1
    return out


def topo_apply_meancenter(x, a, alpha):
    """engine_cli.hexa:9228."""
    n = len(a)
    ahat = _topo_row_center(_topo_sym_norm(a))
    mm = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            v = alpha * ahat[i][j]
            if i == j:
                v = v + 1.0
            mm[i][j] = v
            j = j + 1
        i = i + 1
    return _topo_apply_kernel(x, mm)


def topo_apply_rowstoch(x, a, alpha):
    """engine_cli.hexa:9248."""
    n = len(a)
    p = _topo_row_stochastic(a)
    mm = _topo_zeros(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            v = alpha * p[i][j]
            if i == j:
                v = v + (1.0 - alpha)
            mm[i][j] = v
            j = j + 1
        i = i + 1
    return _topo_apply_kernel(x, mm)


def _topo_row_l2(r):
    """engine_cli.hexa:9289."""
    s = 0.0
    i = 0
    while i < len(r):
        s = s + r[i] * r[i]
        i = i + 1
    return _sqrt(s)


def topo_apply_renorm(x, a, alpha):
    """engine_cli.hexa:9268."""
    coupled = topo_apply(x, a, alpha)
    nt = len(x)
    out = []
    t = 0
    while t < nt:
        off_n = _topo_row_l2(x[t])
        on_n = _topo_row_l2(coupled[t])
        scale = 1.0
        if on_n > 0.000000001:
            scale = off_n / on_n
        n = len(coupled[t])
        row = []
        i = 0
        while i < n:
            row.append(coupled[t][i] * scale)
            i = i + 1
        out.append(row)
        t = t + 1
    return out


def topo_apply_op(x, a, alpha, op):
    """engine_cli.hexa:9298."""
    if op == 1:
        return topo_apply_meancenter(x, a, alpha)
    if op == 2:
        return topo_apply_rowstoch(x, a, alpha)
    if op == 3:
        return topo_apply_renorm(x, a, alpha)
    return topo_apply(x, a, alpha)


def ci_psi_balance_op(x, adj, alpha, op, thr, cfg):
    """engine_cli.hexa:9310."""
    nt = len(x)
    if nt == 0:
        return 0.0
    pop = topo_apply_op(x, adj, alpha, op) if cfg.topo_couple else x
    emit = 0
    t = 0
    while t < nt:
        if ci_emit_drive(pop[t]) >= thr:
            emit = emit + 1
        t = t + 1
    return float(emit) / float(nt)


def topo_func_integration_op(x, a, alpha, op):
    """engine_cli.hexa:9326."""
    xd = topo_apply_op(x, a, alpha, op)
    n = 15
    mu = []
    sd = []
    j = 0
    while j < n:
        m = _topo_mean_col(xd, j)
        mu.append(m)
        nt = len(xd)
        v = 0.0
        t = 0
        while t < nt:
            d = xd[t][j] - m
            v = v + d * d
            t = t + 1
        if nt > 0:
            v = v / float(nt)
        sd.append(_sqrt(v))
        j = j + 1
    nt = len(xd)
    sumr = 0.0
    npair = 0
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            if sd[i] > 0.000001 and sd[j] > 0.000001:
                cov = 0.0
                t = 0
                while t < nt:
                    cov = cov + (xd[t][i] - mu[i]) * (xd[t][j] - mu[j])
                    t = t + 1
                if nt > 0:
                    cov = cov / float(nt)
                r = cov / (sd[i] * sd[j])
                if r < 0.0:
                    r = 0.0 - r
                sumr = sumr + r
                npair = npair + 1
            j = j + 1
        i = i + 1
    if npair == 0:
        return 0.0
    return sumr / float(npair)


def topo_psi_max_feasible_alpha(x, adj, op, thr, tol, cfg):
    """engine_cli.hexa:9371."""
    best = 0.0
    k = 1
    while k <= 10:
        al = float(k) / 10.0
        psi = ci_psi_balance_op(x, adj, al, op, thr, cfg)
        dev = (psi - 0.5) if (psi - 0.5) >= 0.0 else (0.5 - psi)
        if dev <= tol:
            if al > best:
                best = al
        k = k + 1
    return best


# ════════════════════════════════════════════════════════════════════════
# Consciousness-gate R2 lanes (H_1486–1501) — deterministic distinctness gates
# ════════════════════════════════════════════════════════════════════════

def trw_recall(cue_pos, tau, t_now):
    """engine_cli.hexa:9399."""
    window_start = t_now - tau
    if cue_pos >= window_start:
        return 1.0
    return 0.25


def trw_recall_shuffled(cue_pos, tau, t_now):
    """engine_cli.hexa:9406."""
    return 0.25


def reentry_settle(depth, a):
    """engine_cli.hexa:9416."""
    x = 0.0
    k = 0
    while k < depth:
        x = x + a * (1.0 - x)
        k = k + 1
    return x


def reentry_gws_readout(depth):
    """engine_cli.hexa:9427."""
    return 0.235


def attn_schema_report(true_focus, reported, schema_on):
    """engine_cli.hexa:9437."""
    if not schema_on:
        return 0.125
    if reported == true_focus:
        return 1.0
    return 0.125


def attn_schema_agency_readout(true_focus):
    """engine_cli.hexa:9444."""
    return 0.0


def hyst_switch_point(ascending, lam):
    """engine_cli.hexa:9454."""
    if ascending:
        return 0.5 + 0.5 * lam
    return 0.5 - 0.5 * lam


def hyst_rivalry_loop(ascending):
    """engine_cli.hexa:9460."""
    return 0.5


def completion_recognize(surround_match, interp_on):
    """engine_cli.hexa:9470."""
    if not interp_on:
        return 0.544
    return surround_match


def completion_imagery_readout():
    """engine_cli.hexa:9476."""
    return 0.161


def gestalt_same_group(affinity, grouping_on):
    """engine_cli.hexa:9486."""
    if not grouping_on:
        return 0.5
    if affinity >= 0.30:
        return 1.0
    return 0.0


def gestalt_gws_readout():
    """engine_cli.hexa:9493."""
    return 0.505


def prospect_reach(rollout_k, horizon):
    """engine_cli.hexa:9504."""
    if rollout_k >= horizon:
        return 0.439
    return 0.0


def prospect_persist_readout():
    """engine_cli.hexa:9510."""
    return 0.0


def intero_precision(sigma):
    """engine_cli.hexa:9521."""
    eps = 0.0001
    return 1.0 / (sigma * sigma + eps)


def intero_weighted_error(err_a, sig_a, err_b, sig_b, blind):
    """engine_cli.hexa:9527."""
    wa = 1.0
    wb = 1.0
    if not blind:
        wa = intero_precision(sig_a)
        wb = intero_precision(sig_b)
    num = wa * err_a + wb * err_b
    den = wa + wb
    return num / den


def boredom_disengage(info, reward, conjunct):
    """engine_cli.hexa:9546."""
    i_star = 0.5
    r_star = 0.5
    if conjunct:
        if info < i_star and reward < r_star:
            return 1.0
        return 0.0
    if info < i_star:
        return 1.0
    return 0.0


def wander_coverage(steps, n_items, drift_on):
    """engine_cli.hexa:9565."""
    if not drift_on:
        return 1.0 / float(n_items)
    visited = steps
    if visited > n_items:
        visited = n_items
    return float(visited) / float(n_items)


def wander_prospect_coverage(n_items):
    """engine_cli.hexa:9574."""
    return 2.0 / float(n_items)


def qualia_nearer(ring_d_a, ring_d_b):
    """engine_cli.hexa:9585."""
    if ring_d_a < ring_d_b:
        return 1.0
    return 0.0


def qualia_spatial_readout():
    """engine_cli.hexa:9592."""
    return 0.561


def smp_presence(mastered_facets, n_facets, law_correct):
    """engine_cli.hexa:9603."""
    if not law_correct:
        return 1.0 / float(n_facets)
    return float(mastered_facets) / float(n_facets)


def smp_forward_model_readout(n_facets):
    """engine_cli.hexa:9610."""
    return 1.0 / float(n_facets)


def reality_call(signal_margin, thr):
    """engine_cli.hexa:9637."""
    if signal_margin >= thr:
        return 1.0
    return 0.0


def reality_call_ablated():
    """engine_cli.hexa:9644."""
    return 0.5


def reality_imagery_readout():
    """engine_cli.hexa:9650."""
    return 1.0


def reality_confidence_readout(content_correct):
    """engine_cli.hexa:9657."""
    if content_correct:
        return 0.90
    return 0.50


# ════════════════════════════════════════════════════════════════════════
# Compose arbiters (mem×ToM / spatial×episodic / ToM×spatial / ToM×basal /
# cerebellum×memory) — H_1414/1415/1417/1421 query-routed confidence fusion
# ════════════════════════════════════════════════════════════════════════

def _mem_tom_affinity(protos, key, recall_thr):
    """engine_cli.hexa:6892."""
    if len(protos) == 0:
        return 0.0 - 1000000000.0
    w = _vnearest_idx(protos, key)
    d = _l2(protos[w], key)
    return recall_thr - d


def _mem_tom_relconf(margin, mean_margin):
    """engine_cli.hexa:6901."""
    a = (0.0 - margin) if margin < 0.0 else margin
    return a / (mean_margin + 0.000001)


def mem_tom_route_cue(q_is_reality):
    """engine_cli.hexa:6911."""
    qtext = "where is it actually now" if q_is_reality else "where will the agent look for it"
    qk = immune_embed_key(qtext)
    rk = immune_embed_key("actually reality truth where is it now location")
    bk = immune_embed_key("agent belief think look for expects where will")
    dr = _l2(rk, qk)
    db = _l2(bk, qk)
    r = db / (dr + db + 0.000001)
    if r < 0.0:
        r = 0.0
    if r > 1.0:
        r = 1.0
    return r


def mem_tom_mem_margin(mem, key):
    """engine_cli.hexa:6926."""
    return _mem_tom_affinity(mem.protos, key, mem.recall_thr)


def mem_tom_tom_margin(om, key):
    """engine_cli.hexa:6932."""
    return _mem_tom_affinity(om.protos, key, om.recall_thr)


def mem_tom_compose(mem, om, fact_text, q_is_reality, mean_mem, mean_tom):
    """engine_cli.hexa:6945."""
    return mem_tom_compose_routed(mem, om, fact_text, mem_tom_route_cue(q_is_reality),
                                  mean_mem, mean_tom)


def mem_tom_compose_routed(mem, om, fact_text, route, mean_mem, mean_tom):
    """engine_cli.hexa:6959."""
    qk = immune_embed_key(fact_text)
    mem_dec = immune_grow_recall(mem, qk)
    tom_dec = other_mind_predict(om, fact_text)
    if mem_dec == "" and tom_dec == "":
        return ""
    if mem_dec == "":
        return tom_dec
    if tom_dec == "":
        return mem_dec
    if mem_dec == tom_dec:
        return mem_dec
    mm = _mem_tom_affinity(mem.protos, qk, mem.recall_thr)
    tm = _mem_tom_affinity(om.protos, qk, om.recall_thr)
    mem_w = _mem_tom_relconf(mm, mean_mem) * route
    tom_w = _mem_tom_relconf(tm, mean_tom) * (1.0 - route)
    if mem_w >= tom_w:
        return mem_dec
    return tom_dec


def _spat_epi_relconf(conf, mean_conf):
    """engine_cli.hexa:7028."""
    a = (0.0 - conf) if conf < 0.0 else conf
    return a / (mean_conf + 0.000000001)


def spatial_episodic_where_cue(query_text):
    """engine_cli.hexa:7038."""
    qk = immune_embed_key(query_text)
    wk = immune_embed_key("which landmark is nearer to")
    tk = immune_embed_key("what is bound to landmark")
    dw = _l2(wk, qk)
    dt = _l2(tk, qk)
    r = dt / (dw + dt + 0.000001)
    if r < 0.0:
        r = 0.0
    if r > 1.0:
        r = 1.0
    return r


def spatial_episodic_spatial_vote(sm, x, a, b, sp_opt_a, sp_opt_b):
    """engine_cli.hexa:7055."""
    near = spatial_map_nearest(sm, x, a, b)
    if near == "":
        return [0.0 - 1.0, 0.0]
    ix = _sm_idx(sm, x)
    ia = _sm_idx(sm, a)
    ib = _sm_idx(sm, b)
    da = _sm_dist(sm, ix, ia)
    db = _sm_dist(sm, ix, ib)
    margin = (db - da) if da < db else (da - db)
    vote = sp_opt_a if near == a else sp_opt_b
    return [float(vote), margin]


def spatial_episodic_episodic_vote(mem, key):
    """engine_cli.hexa:7071."""
    rv = immune_grow_recall(mem, key)
    if rv == "":
        return [0.0 - 1.0, 0.0]
    vote = 1.0 if rv == "optB" else 0.0
    margin = _mem_tom_affinity(mem.protos, key, mem.recall_thr)
    return [vote, margin]


def spatial_episodic_compose(sp_dec, sp_conf, ep_dec, ep_conf, mean_sp, mean_ep, where_cue):
    """engine_cli.hexa:7088."""
    sp_abst = sp_dec < 0
    ep_abst = ep_dec < 0
    if sp_abst and ep_abst:
        return -1
    if sp_abst:
        return ep_dec
    if ep_abst:
        return sp_dec
    if sp_dec == ep_dec:
        return sp_dec
    sp_w = _spat_epi_relconf(sp_conf, mean_sp) * where_cue
    ep_w = _spat_epi_relconf(ep_conf, mean_ep) * (1.0 - where_cue)
    if sp_w >= ep_w:
        return sp_dec
    return ep_dec


def _tom_compose_relconf(conf, mean_conf):
    """engine_cli.hexa:7138."""
    a = (0.0 - conf) if conf < 0.0 else conf
    return a / (mean_conf + 0.000000001)


def _tom_compose_arbiter(xd, xc, xa, xmean, yd, yc, ya, ymean):
    """engine_cli.hexa:7149."""
    if xa > 0.5 and ya > 0.5:
        return 0.0 - 1.0
    if xa > 0.5:
        return yd
    if ya > 0.5:
        return xd
    if xd == yd:
        return xd
    xw = _tom_compose_relconf(xc, xmean)
    yw = _tom_compose_relconf(yc, ymean)
    if xw >= yw:
        return xd
    return yd


def tom_spatial_tom_vote(om, fact_text, mag):
    """engine_cli.hexa:7167."""
    key = immune_embed_key(fact_text)
    pv = other_mind_predict(om, fact_text)
    dec = 1.0 if pv == "box" else 0.0
    w = _vnearest_idx(om.protos, key) if len(om.protos) > 0 else 0
    d = _l2(om.protos[w], key) if len(om.protos) > 0 else 1.0
    aff = om.recall_thr - d
    abst = 1.0 if pv == "" else 0.0
    a = (0.0 - aff) if aff < 0.0 else aff
    conf = a + mag
    return [dec, abst, conf]


def tom_spatial_spatial_vote(sm, voted_class, mag):
    """engine_cli.hexa:7185."""
    nm = spatial_map_nearest(sm, "L0", "L1", "L2")
    _ = nm
    conf = mag + 0.10
    return [voted_class, 0.0, conf]


def tom_spatial_compose(tom_leg, spat_leg, mean_tom, mean_spatial):
    """engine_cli.hexa:7199."""
    return _tom_compose_arbiter(tom_leg[0], tom_leg[2], tom_leg[1], mean_tom,
                                spat_leg[0], spat_leg[2], spat_leg[1], mean_spatial)


def tom_basal_tom_vote(om, fact_text, mag):
    """engine_cli.hexa:7232."""
    return tom_spatial_tom_vote(om, fact_text, mag)


def tom_basal_compose(tom_leg, basal_leg, mean_tom, mean_basal):
    """engine_cli.hexa:7243."""
    return _tom_compose_arbiter(tom_leg[0], tom_leg[2], tom_leg[1], mean_tom,
                                basal_leg[0], basal_leg[2], basal_leg[1], mean_basal)


def _cereb_mem_relconf(conf, mean_conf):
    """engine_cli.hexa:7292."""
    a = (0.0 - conf) if conf < 0.0 else conf
    return a / (mean_conf + 0.000000001)


def _cereb_mem_tail_arbiter(xd, xc, xa, xmean, yd, yc, ya, ymean):
    """engine_cli.hexa:7302."""
    if xa > 0.5 and ya > 0.5:
        return 0.0 - 1.0
    if xa > 0.5:
        return yd
    if ya > 0.5:
        return xd
    if xd == yd:
        return xd
    xw = _cereb_mem_relconf(xc, xmean)
    yw = _cereb_mem_relconf(yc, ymean)
    if xw >= 1.0 and yw >= 1.0:
        return yd
    if xw >= yw:
        return xd
    return yd


def cereb_mem_cerebellum_vote(ff, voted_class, mag):
    """engine_cli.hexa:7321."""
    lo = mag < 0.30
    x = [_sqrt(0.10)] if lo else [_sqrt(0.90)]
    err = vforward_err(ff, [0.0], x)
    sgnd = 0.50 - err
    a = (0.0 - sgnd) if sgnd < 0.0 else sgnd
    conf = a + mag
    return [voted_class, 0.0, conf]


def cereb_mem_memory_vote(mem, key, mag):
    """engine_cli.hexa:7335."""
    rv = immune_grow_recall(mem, key)
    dec = 1.0 if rv == "box" else 0.0
    w = _vnearest_idx(mem.protos, key)
    d = _l2(mem.protos[w], key)
    aff = mem.recall_thr - d
    abst = 1.0 if rv == "" else 0.0
    a = (0.0 - aff) if aff < 0.0 else aff
    conf = a + mag
    return [dec, abst, conf]


def cereb_mem_compose(cereb_leg, mem_leg, mean_cereb, mean_mem):
    """engine_cli.hexa:7353."""
    return _cereb_mem_tail_arbiter(cereb_leg[0], cereb_leg[2], cereb_leg[1], mean_cereb,
                                   mem_leg[0], mem_leg[2], mem_leg[1], mean_mem)


# ════════════════════════════════════════════════════════════════════════
# §Neuropharm / §Field / §PCI / §MetacogInsight / §MetacogControl / §Hallucination
# / §FieldLibido (H_1502–1508) — substrate perturbation modules
# ════════════════════════════════════════════════════════════════════════

def pharm_baseline():
    """engine_cli.hexa:9686."""
    return [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0]


def pharm_lsd():
    """engine_cli.hexa:9688."""
    return [0.55, 0.45, 0.45, 1.40, 1.05, 0.0 - 0.12, 0.95]


def pharm_dmt():
    """engine_cli.hexa:9689."""
    return [0.40, 0.60, 0.30, 1.55, 1.08, 0.0 - 0.30, 0.90]


def pharm_cannabis():
    """engine_cli.hexa:9690."""
    return [0.85, 0.10, 0.95, 1.02, 1.80, 0.0, 0.55]


def pharm_ketamine():
    """engine_cli.hexa:9691."""
    return [0.80, 0.25, 0.50, 0.60, 1.10, 0.0, 0.85]


def _ph_clip01(x):
    """engine_cli.hexa:9693."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def pharm_perturb_m(prof, m, shared_se):
    """engine_cli.hexa:9702."""
    prior = prof[0]
    return _ph_clip01(0.5 + (m - 0.5) * prior + shared_se)


def pharm_perturb_field(prof, m_field, shared_se):
    """engine_cli.hexa:9707."""
    wm = prof[6]
    fsum = 0.0
    i = 0
    while i < len(m_field):
        fsum = fsum + m_field[i]
        i = i + 1
    fmean = fsum / float(len(m_field))
    out = []
    k = 0
    while k < len(m_field):
        retained = fmean + (m_field[k] - fmean) * wm + shared_se
        out.append(_ph_clip01(retained))
        k = k + 1
    return out


def pharm_perturb_recon(prof, recon_err, shared_se):
    """engine_cli.hexa:9723."""
    se = prof[1]
    return _ph_clip01(recon_err * (1.0 + 0.8 * se) + shared_se)


def pharm_perturb_dt(prof, dt):
    """engine_cli.hexa:9728."""
    td = prof[4]
    v = dt * td
    if v < 0.0:
        return 0.0
    return v


def pharm_shared_se(prof, seed, idx):
    """engine_cli.hexa:9736."""
    se = prof[1]
    s0 = (seed * 100003 + idx * 17 + 7) & 2147483647
    s1 = _lcg_next(s0)
    u = _lcg_unit(s1)
    j = 2.0 * u - 1.0
    return se * 0.30 * j


def pharm_self_continuity(prof, dim, seed):
    """engine_cli.hexa:9748."""
    sb = prof[2]
    diss = 1.0 - sb
    base = self_new(dim, 0)
    ortho = []
    st = (seed + 4242) & 2147483647
    i = 0
    while i < dim:
        st = _lcg_next(st)
        g = 2.0 * _lcg_unit(st) - 1.0
        if i == 0:
            ortho.append(0.0)
        else:
            ortho.append(g)
        i = i + 1
    s = 0.0
    a = 0
    while a < dim:
        s = s + ortho[a] * ortho[a]
        a = a + 1
    nrm = _sqrt(s)
    v = []
    b = 0
    while b < dim:
        comp = self_component(base, b) * (1.0 - diss) + (ortho[b] / nrm) * diss
        v.append(comp)
        b = b + 1
    s2 = 0.0
    c = 0
    while c < dim:
        s2 = s2 + v[c] * v[c]
        c = c + 1
    nrm2 = _sqrt(s2)
    cosacc = 0.0
    d = 0
    while d < dim:
        cosacc = cosacc + self_component(base, d) * (v[d] / nrm2)
        d = d + 1
    return cosacc


def pharm_reality_real_fraction(prof, ms, seed, base_thr):
    """engine_cli.hexa:9788."""
    thr = base_thr + prof[5]
    real = 0.0
    i = 0
    while i < len(ms):
        sse = pharm_shared_se(prof, seed, i)
        pm = pharm_perturb_m(prof, ms[i], sse)
        imagined_margin = pm * 0.35
        real = real + reality_call(imagined_margin, thr)
        i = i + 1
    return real / float(len(ms))


def pharm_couple_rows(rows, lane_coupling, seed):
    """engine_cli.hexa:9805."""
    nc = len(rows[0])
    w_s = 0.5 + 0.6 * (lane_coupling - 1.0)
    w_s = _ph_clip01(w_s)
    w_p = 1.0 - w_s
    out = []
    t = 0
    while t < len(rows):
        r = rows[t]
        rsum = 0.0
        q = 0
        while q < nc:
            rsum = rsum + r[q]
            q = q + 1
        latent = rsum / float(nc) - 0.5
        st = (seed * 7919 + t * 31 + 3) & 2147483647
        nr = []
        j = 0
        while j < nc:
            st = _lcg_next(st)
            pj = 2.0 * _lcg_unit(st) - 1.0
            shared_part = r[j] + latent * (w_s - 0.5) * 2.0
            priv_part = r[j] + pj * 0.12
            nr.append(_ph_clip01(w_s * shared_part + w_p * priv_part))
            j = j + 1
        out.append(nr)
        t = t + 1
    return out


def pharm_lane_rows(prof, trials, seed):
    """engine_cli.hexa:9839."""
    rows = []
    idx = 0
    while idx < len(trials):
        tr = trials[idx]
        sse = pharm_shared_se(prof, seed, idx)
        m = pharm_perturb_m(prof, tr[0], sse)
        m_field0 = [tr[1], tr[2], tr[3], tr[4], tr[5]]
        m_field = pharm_perturb_field(prof, m_field0, sse)
        recon_err = pharm_perturb_recon(prof, tr[10], sse)
        dt = pharm_perturb_dt(prof, tr[9])
        cells = int(tr[6])
        seen = int(tr[7])
        intent = int(tr[8])
        rows.append(ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err))
        idx = idx + 1
    return rows


def pharm_phi(prof, trials, seed):
    """engine_cli.hexa:9861."""
    rows = pharm_lane_rows(prof, trials, seed)
    coupled = pharm_couple_rows(rows, prof[3], seed)
    return ci_phi_multiinfo(coupled, 0 - 1)


def pharm_subjective_time_rate(prof, trials, seed):
    """engine_cli.hexa:9870."""
    DT_REF = 1.5
    s = 0.0
    i = 0
    while i < len(trials):
        dt = pharm_perturb_dt(prof, trials[i][9])
        s = s + _ph_clip01(dt / DT_REF)
        i = i + 1
    return s / float(len(trials))


def pharm_working_mem(prof, trials, seed):
    """engine_cli.hexa:9884."""
    acc = 0.0
    i = 0
    while i < len(trials):
        tr = trials[i]
        sse = pharm_shared_se(prof, seed, i)
        m_field0 = [tr[1], tr[2], tr[3], tr[4], tr[5]]
        fm = pharm_perturb_field(prof, m_field0, sse)
        fsum = 0.0
        k = 0
        while k < len(fm):
            fsum = fsum + fm[k]
            k = k + 1
        mu = fsum / float(len(fm))
        var = 0.0
        j = 0
        while j < len(fm):
            var = var + (fm[j] - mu) * (fm[j] - mu)
            j = j + 1
        var = var / float(len(fm))
        acc = acc + _sqrt(var)
        i = i + 1
    return acc / float(len(trials))


def _field_pulse_env(t, pulse):
    """engine_cli.hexa:9942."""
    if pulse:
        return _exp(0.0 - t / 3.0) * (0.5 + 0.5 * _cos(t))
    return 1.0


def _field_set(mf, k, v):
    """engine_cli.hexa:9948."""
    out = []
    i = 0
    while i < len(mf):
        if i == k:
            out.append(v)
        else:
            out.append(mf[i])
        i = i + 1
    return out


def _field_perturb_mfield(m_field, delta, target_code):
    """engine_cli.hexa:9960."""
    mf = []
    i = 0
    while i < len(m_field):
        mf.append(m_field[i])
        i = i + 1
    if target_code == 1:
        wi = 0
        wv = mf[0]
        j = 1
        while j < len(mf):
            if mf[j] > wv:
                wv = mf[j]
                wi = j
            j = j + 1
        nv = mf[wi] + delta
        if nv < 0.0:
            nv = 0.0
        if nv > 1.0:
            nv = 1.0
        mf = _field_set(mf, wi, nv)
    if target_code == 2:
        s = 0.0
        a = 0
        while a < len(mf):
            s = s + mf[a]
            a = a + 1
        mean = s / float(len(mf))
        b = 0
        while b < len(mf):
            if mf[b] < mean:
                nv = mf[b] + 0.6 * delta
                if nv < 0.0:
                    nv = 0.0
                if nv > 1.0:
                    nv = 1.0
                mf = _field_set(mf, b, nv)
            b = b + 1
    return mf


def field_apply(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign,
                target_code, pulse, t):
    """engine_cli.hexa:9996."""
    env = _field_pulse_env(t, pulse)
    delta = float(sign) * intensity * env * 0.30
    mf = _field_perturb_mfield(m_field, delta, target_code)
    cells_p = cells
    if target_code == 3:
        cells_p = cells + int(float(sign) * intensity * 5.0 * env + 0.5)
        if cells_p < 0:
            cells_p = 0
    return ci_lane_scores(m, mf, cells_p, seen, intent, dt, recon_err)


def field_apply_mfield(m_field, intensity, sign, target_code):
    """engine_cli.hexa:10011."""
    delta = float(sign) * intensity * 0.30
    return _field_perturb_mfield(m_field, delta, target_code)


def field_signal_entropy(m_field):
    """engine_cli.hexa:10018."""
    n = len(m_field)
    if n < 2:
        return 0.0
    psum = 0.0
    i = 0
    while i < n:
        if m_field[i] > 0.000001:
            psum = psum + m_field[i]
        i = i + 1
    if psum <= 0.000001:
        return 0.0
    ent = 0.0
    j = 0
    while j < n:
        if m_field[j] > 0.000001:
            p = m_field[j] / psum
            ent = ent - p * _ln(p)
        j = j + 1
    return ent / _ln(float(n))


def drug_lsd_mfield(m_field, seed, idx):
    """engine_cli.hexa:10040."""
    prof = pharm_lsd()
    sse = pharm_shared_se(prof, seed, idx)
    return pharm_perturb_field(prof, m_field, sse)


def _field_lz76(s):
    """engine_cli.hexa:10047 — Lempel-Ziv 1976 complexity."""
    n = len(s)
    if n == 0:
        return 0
    i = 0
    c = 1
    l = 1
    k = 1
    kmax = 1
    done = False
    while not done:
        if l + k > n:
            c = c + 1
            done = True
        else:
            if s[i + k - 1] == s[l + k - 1]:
                k = k + 1
                if l + k > n:
                    c = c + 1
                    done = True
            else:
                if k > kmax:
                    kmax = k
                i = i + 1
                if i == l:
                    c = c + 1
                    l = l + kmax
                    if l >= n:
                        done = True
                    else:
                        i = 0
                        k = 1
                        kmax = 1
                else:
                    k = 1
    return c


def pci_perturb(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign,
                target_code, pulse, T):
    """engine_cli.hexa:10078."""
    rest = ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err)
    R = []
    t = 0
    while t < T:
        vec = field_apply(m, m_field, cells, seen, intent, dt, recon_err,
                          freq_code, intensity, sign, target_code, pulse, float(t))
        row = []
        j = 0
        while j < len(vec):
            d = vec[j] - rest[j]
            if d < 0.0:
                d = 0.0 - d
            row.append(d)
            j = j + 1
        R.append(row)
        t = t + 1
    return R


def pci_complexity(R, decoupled):
    """engine_cli.hexa:10104."""
    T = len(R)
    if T == 0:
        return 0.0
    N = len(R[0])
    s = 0.0
    cnt = 0
    a = 0
    while a < T:
        b = 0
        while b < N:
            s = s + R[a][b]
            cnt = cnt + 1
            b = b + 1
        a = a + 1
    thr = s / float(cnt) + 0.000000001
    B = []
    i = 0
    while i < T:
        row = []
        j = 0
        while j < N:
            if R[i][j] > thr:
                row.append(1)
            else:
                row.append(0)
            j = j + 1
        B.append(row)
        i = i + 1
    if decoupled:
        col0 = B[0][0]
        Bd = []
        p = 0
        while p < T:
            row = []
            q = 0
            while q < N:
                if q == 0:
                    if p < 2:
                        if col0 == 1:
                            row.append(1)
                        else:
                            row.append(0)
                    else:
                        row.append(0)
                else:
                    row.append(0)
                q = q + 1
            Bd.append(row)
            p = p + 1
        B = Bd
    flat = []
    ones = 0
    u = 0
    while u < T:
        v = 0
        while v < N:
            bit = B[u][v]
            flat.append(bit)
            if bit == 1:
                ones = ones + 1
            v = v + 1
        u = u + 1
    nn = len(flat)
    if nn <= 1:
        return 0.0
    if ones == 0:
        return 0.0
    if ones == nn:
        return 0.0
    cc = _field_lz76(flat)
    log2n = _ln(float(nn)) / _ln(2.0)
    return float(cc) * log2n / float(nn)


def field_lane_mean(vec, lanes):
    """engine_cli.hexa:10171."""
    n = len(lanes)
    if n == 0:
        return 0.0
    s = 0.0
    i = 0
    while i < n:
        s = s + vec[lanes[i]]
        i = i + 1
    return s / float(n)


def mi_gain_intact():
    """engine_cli.hexa:10202."""
    return 1.0


def mi_gain_impaired():
    """engine_cli.hexa:10203."""
    return 0.0


def mi_signal_margin(seed, hallucination, idx):
    """engine_cli.hexa:10209."""
    hb = 1 if hallucination else 0
    s0 = (seed * 100003 + hb * 911 + 7) & 2147483647
    st = s0
    t = 0
    while t <= idx:
        st = _lcg_next(st)
        t = t + 1
    u = _lcg_unit(st)
    if hallucination:
        return 0.05 + 0.15 * u
    return 0.40 + 0.30 * u


def mi_insight_judge(signal_margin, metacog_gain):
    """engine_cli.hexa:10224."""
    ss = signal_margin / 0.70
    if ss < 0.0:
        ss = 0.0
    if ss > 1.0:
        ss = 1.0
    ins = metacog_gain * (1.0 - ss)
    if ins < 0.0:
        ins = 0.0
    if ins > 1.0:
        ins = 1.0
    return ins


def mi_insight_psychedelic(seed, n):
    """engine_cli.hexa:10236."""
    acc = 0.0
    i = 0
    while i < n:
        m = mi_signal_margin(seed, True, i)
        acc = acc + mi_insight_judge(m, mi_gain_intact())
        i = i + 1
    return acc / float(n)


def mi_insight_psychotic(seed, n):
    """engine_cli.hexa:10248."""
    acc = 0.0
    i = 0
    while i < n:
        m = mi_signal_margin(seed, True, i)
        acc = acc + mi_insight_judge(m, mi_gain_impaired())
        i = i + 1
    return acc / float(n)


def mi_metad_auroc(seed, n):
    """engine_cli.hexa:10263."""
    pos = []
    neg = []
    i = 0
    while i < n:
        mg = mi_signal_margin(seed, False, i)
        mh = mi_signal_margin(seed, True, i)
        neg.append(mi_insight_judge(mg, mi_gain_intact()))
        pos.append(mi_insight_judge(mh, mi_gain_intact()))
        i = i + 1
    return mi_auroc(pos, neg)


def mi_auroc(pos, neg):
    """engine_cli.hexa:10279."""
    np_ = len(pos)
    nn = len(neg)
    if np_ == 0 or nn == 0:
        return 0.5
    wins = 0.0
    a = 0
    while a < np_:
        p = pos[a]
        b = 0
        while b < nn:
            if p > neg[b]:
                wins = wins + 1.0
            else:
                if p == neg[b]:
                    wins = wins + 0.5
            b = b + 1
        a = a + 1
    return wins / (float(np_) * float(nn))


def _mi_set(v, ix, val):
    """engine_cli.hexa:10334."""
    out = []
    i = 0
    while i < len(v):
        if i == ix:
            out.append(val)
        else:
            out.append(v[i])
        i = i + 1
    return out


def mi_shuffle_auroc(seed, n):
    """engine_cli.hexa:10304."""
    scores = []
    i = 0
    while i < n:
        scores.append(mi_insight_judge(mi_signal_margin(seed, False, i), mi_gain_intact()))
        i = i + 1
    j = 0
    while j < n:
        scores.append(mi_insight_judge(mi_signal_margin(seed, True, j), mi_gain_intact()))
        j = j + 1
    total = 2 * n
    st = (seed * 2654435761 + 1013904223) & 2147483647
    k = total - 1
    while k > 0:
        st = _lcg_next(st)
        r = st % (k + 1)
        tmp = scores[k]
        scores = _mi_set(scores, k, scores[r])
        scores = _mi_set(scores, r, tmp)
        k = k - 1
    sneg = []
    spos = []
    p = 0
    while p < total:
        if p < n:
            sneg.append(scores[p])
        else:
            spos.append(scores[p])
        p = p + 1
    return mi_auroc(spos, sneg)


def hallucinate_call(prior_strength, prior_match, signal_strength, thr):
    """engine_cli.hexa:10367."""
    margin = prior_strength * prior_match + signal_strength
    return reality_call(margin, thr)


def hallucinate_graded(prior_strength, signal_strength):
    """engine_cli.hexa:10374."""
    s = 1.0 - signal_strength
    g = prior_strength * s
    if g < 0.0:
        return 0.0
    if g > 1.0:
        return 1.0
    return g


def hallucinate_ablated(signal_strength, thr):
    """engine_cli.hexa:10384."""
    return reality_call(signal_strength, thr)


def hallucinate_under_drug(prof, base_prior, prior_match, base_thr):
    """engine_cli.hexa:10393."""
    release = 1.0 / prof[0]
    drug_prior = base_prior * release
    drug_thr = base_thr + prof[5]
    return hallucinate_call(drug_prior, prior_match, 0.0, drug_thr)


def _mc_corrupt_key(key, level, seed):
    """engine_cli.hexa:10437."""
    dim = len(key)
    out = []
    st = (seed * 2654435761 + 1013904223) & 2147483647
    i = 0
    while i < dim:
        st = _lcg_next(st)
        noise = (_lcg_unit(st) - 0.5) * 2.0 * level
        out.append(key[i] + noise)
        i = i + 1
    s = 0.0
    j = 0
    while j < dim:
        s = s + out[j] * out[j]
        j = j + 1
    nrm = _sqrt(s)
    if nrm > 0.0:
        o = 0
        while o < dim:
            out[o] = out[o] / nrm
            o = o + 1
    return out


def _mc_store(n, dim, seed):
    """engine_cli.hexa:10463."""
    protos = []
    vals = []
    st = (seed * 40503 + 7) & 2147483647
    i = 0
    while i < n:
        v = []
        d = 0
        while d < dim:
            st = _lcg_next(st)
            v.append(_lcg_unit(st) - 0.5)
            d = d + 1
        s = 0.0
        k = 0
        while k < dim:
            s = s + v[k] * v[k]
            k = k + 1
        nrm = _sqrt(s)
        vv = []
        o = 0
        while o < dim:
            vv.append(v[o] / nrm)
            o = o + 1
        protos.append(vv)
        vals.append("v" + str(i))
        i = i + 1
    af = VAdaptField(protos, n, n + 4, dim)
    return ImmuneMemory(af, vals, 0.15)


def _mc_levels():
    """engine_cli.hexa:10499."""
    return [0.0, 0.037, 0.050, 0.20, 1.0]


def _mc_trial_margin(mem, ti, level, salt):
    """engine_cli.hexa:10503."""
    key = _mc_corrupt_key(mem.field.protos[ti], level, ti * 131071 + salt)
    return immune_memory_recall_margin(mem, key)


def _mc_trial_correct(mem, ti, level, salt):
    """engine_cli.hexa:10508."""
    key = _mc_corrupt_key(mem.field.protos[ti], level, ti * 131071 + salt)
    err = vadapt_field_recon_err(mem.field, key)
    if err > mem.recall_thr:
        return 0
    win = vadapt_field_nearest_idx(mem.field, key)
    if win == ti:
        return 1
    return 0


def _mc_ece(confs, corrs, nbins):
    """engine_cli.hexa:10549."""
    total = len(confs)
    if total == 0:
        return 0.0
    e = 0.0
    b = 0
    while b < nbins:
        lo = float(b) / float(nbins)
        hi = float(b + 1) / float(nbins)
        sc = 0.0
        sa = 0.0
        cnt = 0
        i = 0
        while i < total:
            cf = confs[i]
            inbin = (cf >= lo and cf <= hi) if b == nbins - 1 else (cf >= lo and cf < hi)
            if inbin:
                sc = sc + cf
                sa = sa + corrs[i]
                cnt = cnt + 1
            i = i + 1
        if cnt > 0:
            mc = sc / float(cnt)
            ma = sa / float(cnt)
            gap = (mc - ma) if mc >= ma else (ma - mc)
            e = e + (float(cnt) / float(total)) * gap
        b = b + 1
    return e


def mc_calibration_ece(seed, n):
    """engine_cli.hexa:10521."""
    mem = _mc_store(n, 64, seed)
    levels = _mc_levels()
    nl = len(levels)
    confs = []
    corrs = []
    li = 0
    while li < nl:
        lv = levels[li]
        ti = 0
        while ti < n:
            m = _mc_trial_margin(mem, ti, lv, li * 17 + 1)
            c = _mc_trial_correct(mem, ti, lv, li * 17 + 1)
            cf = 0.5 - m / (2.0 * mem.recall_thr)
            if cf < 0.0:
                cf = 0.0
            if cf > 1.0:
                cf = 1.0
            confs.append(cf)
            corrs.append(float(c))
            ti = ti + 1
        li = li + 1
    return _mc_ece(confs, corrs, 10)


def _mc_ranks(x):
    """engine_cli.hexa:10612."""
    n = len(x)
    out = []
    i = 0
    while i < n:
        r = 0.0
        j = 0
        while j < n:
            if x[j] < x[i]:
                r = r + 1.0
            else:
                if x[j] == x[i] and j < i:
                    r = r + 1.0
            j = j + 1
        out.append(r)
        i = i + 1
    return out


def _mc_pearson(a, b):
    """engine_cli.hexa:10629."""
    n = len(a)
    if n == 0:
        return 0.0
    ma = 0.0
    mb = 0.0
    i = 0
    while i < n:
        ma = ma + a[i]
        mb = mb + b[i]
        i = i + 1
    ma = ma / float(n)
    mb = mb / float(n)
    num = 0.0
    da = 0.0
    db = 0.0
    k = 0
    while k < n:
        xa = a[k] - ma
        xb = b[k] - mb
        num = num + xa * xb
        da = da + xa * xa
        db = db + xb * xb
        k = k + 1
    den = _sqrt(da * db)
    if den <= 0.0:
        return 0.0
    return num / den


def _mc_spearman(a, b):
    """engine_cli.hexa:10607."""
    ra = _mc_ranks(a)
    rb = _mc_ranks(b)
    return _mc_pearson(ra, rb)


def mc_calibration_monotone(seed, n):
    """engine_cli.hexa:10584."""
    mem = _mc_store(n, 64, seed)
    levels = _mc_levels()
    nl = len(levels)
    lvl_idx = []
    lvl_marg = []
    li = 0
    while li < nl:
        lv = levels[li]
        acc = 0.0
        ti = 0
        while ti < n:
            acc = acc + _mc_trial_margin(mem, ti, lv, li * 17 + 1)
            ti = ti + 1
        lvl_idx.append(float(li))
        lvl_marg.append(acc / float(n))
        li = li + 1
    return _mc_spearman(lvl_idx, lvl_marg)


def _mc_exp(x):
    """engine_cli.hexa:10776 — 16-term Taylor (NOT libm; mirror exactly)."""
    term = 1.0
    sum_ = 1.0
    k = 1
    while k < 16:
        term = term * x / float(k)
        sum_ = sum_ + term
        k = k + 1
    return sum_


def _mc_floor(x):
    """engine_cli.hexa:10789."""
    i = 0
    while float(i + 1) <= x:
        i = i + 1
    return i


def _mc_eval_alloc(mem, t_fact, t_level, alloc):
    """engine_cli.hexa:10737."""
    total = len(t_fact)
    dim = mem.field.dim
    correct = 0
    i = 0
    while i < total:
        ti = t_fact[i]
        lv = t_level[i]
        nreads = alloc[i] + 1
        acc = []
        d = 0
        while d < dim:
            acc.append(0.0)
            d = d + 1
        r = 0
        while r < nreads:
            key = _mc_corrupt_key(mem.field.protos[ti], lv, ti * 131071 + i * 7919 + r * 104729 + 3)
            k = 0
            while k < dim:
                acc[k] = acc[k] + key[k]
                k = k + 1
            r = r + 1
        s = 0.0
        k2 = 0
        while k2 < dim:
            s = s + acc[k2] * acc[k2]
            k2 = k2 + 1
        nrm = _sqrt(s)
        if nrm > 0.0:
            o = 0
            while o < dim:
                acc[o] = acc[o] / nrm
                o = o + 1
        err = vadapt_field_recon_err(mem.field, acc)
        if err <= mem.recall_thr:
            win = vadapt_field_nearest_idx(mem.field, acc)
            if win == ti:
                correct = correct + 1
        i = i + 1
    return float(correct) / float(total)


def mc_control_lift_policy(seed, n, use_margin):
    """engine_cli.hexa:10670."""
    mem = _mc_store(n, 64, seed)
    levels = _mc_levels()
    nl = len(levels)
    total = nl * n
    budget = total
    t_fact = []
    t_level = []
    t_marg = []
    li = 0
    while li < nl:
        lv = levels[li]
        ti = 0
        while ti < n:
            t_fact.append(ti)
            t_level.append(lv)
            t_marg.append(_mc_trial_margin(mem, ti, lv, li * 17 + 1))
            ti = ti + 1
        li = li + 1
    alloc = []
    if use_margin:
        center = 0.05
        width = 0.05
        wsum = 0.0
        prox = []
        i = 0
        while i < total:
            m = t_marg[i]
            z = (m - center) / width
            w = _mc_exp(-0.5 * z * z)
            if m <= -0.05:
                w = 0.0
            prox.append(w)
            wsum = wsum + w
            i = i + 1
        if wsum <= 0.0:
            wsum = 1.0
        j = 0
        while j < total:
            alloc.append(_mc_floor(prox[j] / wsum * float(budget)))
            j = j + 1
    else:
        per = budget // total
        j = 0
        while j < total:
            alloc.append(per)
            j = j + 1
    per_u = budget // total
    alloc_u = []
    ju = 0
    while ju < total:
        alloc_u.append(per_u)
        ju = ju + 1
    acc_adapt = _mc_eval_alloc(mem, t_fact, t_level, alloc)
    acc_unif = _mc_eval_alloc(mem, t_fact, t_level, alloc_u)
    return acc_adapt - acc_unif


def mc_control_lift(seed, n):
    """engine_cli.hexa:10660."""
    return mc_control_lift_policy(seed, n, True)


def mc_control_lift_ablated(seed, n):
    """engine_cli.hexa:10665."""
    return mc_control_lift_policy(seed, n, False)


def mc_auroc_calibration_orthogonal(seed, n):
    """engine_cli.hexa:10799."""
    mem = _mc_store(n, 64, seed)
    levels = _mc_levels()
    nl = len(levels)
    confs = []
    corrs = []
    li = 0
    while li < nl:
        lv = levels[li]
        ti = 0
        while ti < n:
            m = _mc_trial_margin(mem, ti, lv, li * 17 + 1)
            c = _mc_trial_correct(mem, ti, lv, li * 17 + 1)
            cf = 0.5 - m / (2.0 * mem.recall_thr)
            if cf < 0.0:
                cf = 0.0
            if cf > 1.0:
                cf = 1.0
            confs.append(cf)
            corrs.append(float(c))
            ti = ti + 1
        li = li + 1
    pos = []
    neg = []
    posx = []
    negx = []
    i = 0
    while i < len(confs):
        cf = confs[i]
        cfx = 0.55 + 0.44 * cf
        if corrs[i] >= 0.5:
            pos.append(cf)
            posx.append(cfx)
        else:
            neg.append(cf)
            negx.append(cfx)
        i = i + 1
    au_base = mi_auroc(pos, neg)
    au_xform = mi_auroc(posx, negx)
    ece_base = _mc_ece(confs, corrs, 10)
    confs_x = []
    j = 0
    while j < len(confs):
        confs_x.append(0.55 + 0.44 * confs[j])
        j = j + 1
    ece_xform = _mc_ece(confs_x, corrs, 10)
    return [au_base, au_xform, ece_base, ece_xform]


def mc_shuffle_auroc(seed, n):
    """engine_cli.hexa:10848."""
    mem = _mc_store(n, 64, seed)
    levels = _mc_levels()
    nl = len(levels)
    confs = []
    corrs = []
    li = 0
    while li < nl:
        lv = levels[li]
        ti = 0
        while ti < n:
            m = _mc_trial_margin(mem, ti, lv, li * 17 + 1)
            c = _mc_trial_correct(mem, ti, lv, li * 17 + 1)
            cf = 0.5 - m / (2.0 * mem.recall_thr)
            if cf < 0.0:
                cf = 0.0
            if cf > 1.0:
                cf = 1.0
            confs.append(cf)
            corrs.append(float(c))
            ti = ti + 1
        li = li + 1
    total = len(corrs)
    st = (seed * 2654435761 + 1013904223) & 2147483647
    k = total - 1
    while k > 0:
        st = _lcg_next(st)
        r = st % (k + 1)
        tmp = corrs[k]
        corrs = _mi_set(corrs, k, corrs[r])
        corrs = _mi_set(corrs, r, tmp)
        k = k - 1
    pos = []
    neg = []
    i = 0
    while i < total:
        if corrs[i] >= 0.5:
            pos.append(confs[i])
        else:
            neg.append(confs[i])
        i = i + 1
    return mi_auroc(pos, neg)


def _fl_gain_scale():
    """engine_cli.hexa:10916."""
    return 4.0


def fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign):
    """engine_cli.hexa:10921."""
    rest = ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err)
    on = field_apply(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign, 1, False, 0.0)
    lift = on[0] - rest[0]
    return lift * _fl_gain_scale()


def fieldlibido_wanting(m, m_field, cells, seen, intent, dt, recon_err, deficit, accum, cue_match,
                        freq_code, intensity, sign):
    """engine_cli.hexa:10932."""
    g = fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign)
    ld = Libido(accum, 0.0, 0.5, 0.1, 1.0, 0.5, 1.0, g)
    return libido_wanting(ld, deficit, cue_match)


def fieldlibido_liking(cue_match):
    """engine_cli.hexa:10941."""
    ld = libido_new()
    return libido_liking(ld, cue_match)


def fieldlibido_highfreq(m, m_field, cells, seen, intent, dt, recon_err, intensity):
    """engine_cli.hexa:10947."""
    return fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, 6, intensity, 1)


def fieldlibido_lowfreq(m, m_field, cells, seen, intent, dt, recon_err, intensity):
    """engine_cli.hexa:10951."""
    return fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, 5, intensity, 0 - 1)


def fieldlibido_sham(m, m_field, cells, seen, intent, dt, recon_err):
    """engine_cli.hexa:10955."""
    return fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, 0, 0.0, 0)


# ════════════════════════════════════════════════════════════════════════
# §ThirdLaw + §Savant (SAVANT/savant_lib re-anchored) — savant scoring free-fns
# ════════════════════════════════════════════════════════════════════════

def sa_gz_lower():
    """SAVANT/savant_lib.hexa:77."""
    return 0.21231792755821914


def sa_gz_upper():
    """SAVANT/savant_lib.hexa:82."""
    return 0.5


def sa_in_golden_zone(I):
    """SAVANT/savant_lib.hexa:122."""
    lo = sa_gz_lower()
    hi = sa_gz_upper()
    if I < lo:
        return 0
    if I > hi:
        return 0
    return 1


def _tl_sing_thr():
    """engine_cli.hexa:10978."""
    return 0.70


def third_law_score(d, p, ii):
    """engine_cli.hexa:10982 — G = D·P/I."""
    if ii <= 0.0:
        return 0.0
    return (d * p) / ii


def third_law_singularity(d, p, ii):
    """engine_cli.hexa:10989."""
    if third_law_score(d, p, ii) > _tl_sing_thr():
        return 1
    return 0


def third_law_ability(d, p, ii):
    """engine_cli.hexa:10998."""
    if third_law_singularity(d, p, ii) == 1 and sa_in_golden_zone(ii) == 1:
        return 1
    return 0


def _tl_linspace(a, b, n):
    """engine_cli.hexa:11004."""
    out = []
    if n <= 1:
        out.append(a)
        return out
    step = (b - a) / float(n - 1)
    i = 0
    while i < n:
        out.append(a + step * float(i))
        i = i + 1
    return out


def third_law_ratio(nD, nP, nI):
    """engine_cli.hexa:11016."""
    dg = _tl_linspace(0.05, 0.95, nD)
    pg = _tl_linspace(0.05, 0.95, nP)
    ig = _tl_linspace(0.05, 0.95, nI)
    total = 0
    sing = 0
    a = 0
    while a < nI:
        ii = ig[a]
        b = 0
        while b < nD:
            d = dg[b]
            c = 0
            while c < nP:
                pp = pg[c]
                total = total + 1
                if third_law_singularity(d, pp, ii) == 1:
                    sing = sing + 1
                c = c + 1
            b = b + 1
        a = a + 1
    if total == 0:
        return 0.0
    return float(sing) / float(total)


def third_law_overlap(nD, nP, nI):
    """engine_cli.hexa:11046."""
    dg = _tl_linspace(0.05, 0.95, nD)
    pg = _tl_linspace(0.05, 0.95, nP)
    ig = _tl_linspace(0.05, 0.95, nI)
    sing = 0
    abil = 0
    a = 0
    while a < nI:
        ii = ig[a]
        b = 0
        while b < nD:
            d = dg[b]
            c = 0
            while c < nP:
                pp = pg[c]
                if third_law_singularity(d, pp, ii) == 1:
                    sing = sing + 1
                    if sa_in_golden_zone(ii) == 1:
                        abil = abil + 1
                c = c + 1
            b = b + 1
        a = a + 1
    if sing == 0:
        return 0.0
    return float(abil) / float(sing)


def third_law_i50(nD, nP, nI):
    """engine_cli.hexa:11077."""
    dg = _tl_linspace(0.05, 0.95, nD)
    pg = _tl_linspace(0.05, 0.95, nP)
    ig = _tl_linspace(0.05, 0.95, nI)
    rate = []
    a = 0
    while a < nI:
        ii = ig[a]
        it = 0
        is_ = 0
        b = 0
        while b < nD:
            d = dg[b]
            c = 0
            while c < nP:
                it = it + 1
                if third_law_singularity(d, pg[c], ii) == 1:
                    is_ = is_ + 1
                c = c + 1
            b = b + 1
        rate.append(float(is_) / float(it))
        a = a + 1
    k = 0
    while k < nI - 1:
        y0 = rate[k]
        y1 = rate[k + 1]
        if y0 >= 0.5 and y1 < 0.5:
            x0 = ig[k]
            x1 = ig[k + 1]
            return x0 + (y0 - 0.5) / (y0 - y1) * (x1 - x0)
        k = k + 1
    return 0.0 - 1.0


def _tl_latch_off_thr():
    """engine_cli.hexa:11141."""
    return 0.75


def third_law_ability_memoryless(d, p, ii):
    """engine_cli.hexa:11145."""
    return third_law_ability(d, p, ii)


def third_law_ability_latched(d, p, ii, prev_on):
    """engine_cli.hexa:11154."""
    if prev_on == 1:
        if ii > _tl_latch_off_thr():
            return 0
        return 1
    return third_law_ability(d, p, ii)


def third_law_hysteresis_width(d, p, nDown, nUp):
    """engine_cli.hexa:11167."""
    dg = _tl_linspace(0.95, 0.05, nDown)
    latch = 0
    i_on = 0.0 - 1.0
    a = 0
    while a < nDown:
        ii = dg[a]
        nl = third_law_ability_latched(d, p, ii, latch)
        if latch == 0 and nl == 1:
            i_on = ii
        latch = nl
        a = a + 1
    if i_on < 0.0:
        return 0.0
    ug = _tl_linspace(0.05, 0.95, nUp)
    i_off = 0.0 - 1.0
    b = 0
    while b < nUp:
        ii = ug[b]
        nl = third_law_ability_latched(d, p, ii, latch)
        if latch == 1 and nl == 0:
            i_off = ii
        latch = nl
        b = b + 1
    if i_off < 0.0:
        return 0.0 - 1.0
    w = i_off - i_on
    if w < 0.0:
        return 0.0 - w
    return w


def sv_gz_lower():
    """engine_cli.hexa:11245."""
    return 0.21231792755821914


def sv_gz_upper():
    """engine_cli.hexa:11246."""
    return 0.5


def sv_gz_center():
    """engine_cli.hexa:11247."""
    return 0.36787944117144233


def sv_si_threshold():
    """engine_cli.hexa:11248."""
    return 3.0


def sv_in_golden_zone(inh):
    """engine_cli.hexa:11251."""
    if inh < sv_gz_lower():
        return 0
    if inh > sv_gz_upper():
        return 0
    return 1


def sv_savant_index(phis):
    """engine_cli.hexa:11258 — SI = max(Φ)/mean(Φ)."""
    n = len(phis)
    if n == 0:
        return 0.0
    sum_p = 0.0
    max_p = phis[0]
    i = 0
    while i < n:
        v = phis[i]
        sum_p = sum_p + v
        if v > max_p:
            max_p = v
        i = i + 1
    mean_p = sum_p / float(n)
    if mean_p <= 0.0:
        return 0.0
    return max_p / mean_p


def _sv_col_mean(x, c):
    """engine_cli.hexa:11276."""
    nt = len(x)
    if nt == 0:
        return 0.0
    s = 0.0
    t = 0
    while t < nt:
        s = s + x[t][c]
        t = t + 1
    return s / float(nt)


def sv_inhibit_domain(x, lo, hi, inh):
    """engine_cli.hexa:11302 — shared-latent inhibition operator (inverse-U Φ)."""
    nt = len(x)
    ncol = len(x[0]) if nt > 0 else 0
    w = hi - lo
    cmean = []
    c = 0
    while c < ncol:
        if c >= lo and c < hi:
            cmean.append(_sv_col_mean(x, c))
        else:
            cmean.append(0.0)
        c = c + 1
    gz_lo = sv_gz_lower()
    NOISE_K = 6.0
    sig = 1.0 - inh
    noi = 0.0
    if inh < gz_lo:
        noi = NOISE_K * (gz_lo - inh)
    out = []
    t = 0
    while t < nt:
        srow = 0.0
        sc = lo
        while sc < hi:
            srow = srow + x[t][sc]
            sc = sc + 1
        s_t = (srow / float(w)) if w > 0 else 0.0
        row = []
        k = 0
        while k < ncol:
            raw = x[t][k]
            if k >= lo and k < hi:
                base = cmean[k]
                res = raw - base
                gated = base + sig * (s_t - base) + noi * res
                row.append(gated)
            else:
                row.append(raw)
            k = k + 1
        out.append(row)
        t = t + 1
    return out


def _sv_domain_cols(lo, hi):
    """engine_cli.hexa:11358."""
    cols = []
    c = lo
    while c < hi:
        cols.append(c)
        c = c + 1
    return cols


def sv_domain_phi(x, lo, hi, inh):
    """engine_cli.hexa:11367."""
    pop = sv_inhibit_domain(x, lo, hi, inh)
    cols = _sv_domain_cols(lo, hi)
    return ci_phi_iit4(pop, cols)


def sv_domain_phis(x, d, w, focus, gz_inh, base_inh):
    """engine_cli.hexa:11377."""
    phis = []
    dom = 0
    while dom < d:
        lo = dom * w
        hi = lo + w
        inh = gz_inh if dom == focus else base_inh
        phis.append(sv_domain_phi(x, lo, hi, inh))
        dom = dom + 1
    return phis


def sv_savant_index_at(x, d, w, focus, gz_inh, base_inh):
    """engine_cli.hexa:11392."""
    return sv_savant_index(sv_domain_phis(x, d, w, focus, gz_inh, base_inh))


def sv_focus_phi_sweep(x, lo, hi, igrid):
    """engine_cli.hexa:11398."""
    out = []
    i = 0
    while i < len(igrid):
        out.append(sv_domain_phi(x, lo, hi, igrid[i]))
        i = i + 1
    return out


def sv_dphi_peak_inh(phis, igrid):
    """engine_cli.hexa:11407."""
    n = len(phis)
    if n < 2:
        return 0.0
    peak_i = igrid[0]
    peak_abs = 0.0 - 1.0
    k = 0
    while k < n:
        d = 0.0
        if k == 0:
            d = (phis[1] - phis[0]) / (igrid[1] - igrid[0])
        else:
            if k == n - 1:
                d = (phis[n - 1] - phis[n - 2]) / (igrid[n - 1] - igrid[n - 2])
            else:
                d = (phis[k + 1] - phis[k - 1]) / (igrid[k + 1] - igrid[k - 1])
        a = d
        if a < 0.0:
            a = 0.0 - a
        if a > peak_abs:
            peak_abs = a
            peak_i = igrid[k]
        k = k + 1
    return peak_i


def sv_savant_trigger(phis, inh, split_rate, cfg):
    """engine_cli.hexa:11435."""
    if cfg.savant == False:
        return 0
    si = sv_savant_index(phis)
    si_high = si >= sv_si_threshold()
    in_gz = sv_in_golden_zone(inh)
    split_active = split_rate > 0.0
    if si_high == False:
        return 0
    if in_gz != 1:
        return 0
    if split_active == False:
        return 0
    return 1


def ci_psi_balance_savant(x, lo, hi, gz_inh, thr, cfg):
    """engine_cli.hexa:11454."""
    nt = len(x)
    if nt == 0:
        return 0.0
    pop = sv_inhibit_domain(x, lo, hi, gz_inh) if cfg.savant else x
    emit = 0
    t = 0
    while t < nt:
        if ci_emit_drive(pop[t]) >= thr:
            emit = emit + 1
        t = t + 1
    return float(emit) / float(nt)


def sv_lane_sync(x, lo, hi):
    """engine_cli.hexa:11482 — mean pairwise |corr| (Kuramoto-R analogue)."""
    nt = len(x)
    if nt < 2:
        return 0.0
    mu = []
    c = lo
    while c < hi:
        s = 0.0
        t = 0
        while t < nt:
            s = s + x[t][c]
            t = t + 1
        mu.append(s / float(nt))
        c = c + 1
    w = hi - lo
    if w < 2:
        return 0.0
    acc = 0.0
    npair = 0
    a = 0
    while a < w:
        b = a + 1
        while b < w:
            cov = 0.0
            va = 0.0
            vb = 0.0
            t = 0
            while t < nt:
                da = x[t][lo + a] - mu[a]
                db = x[t][lo + b] - mu[b]
                cov = cov + da * db
                va = va + da * da
                vb = vb + db * db
                t = t + 1
            denom = _sqrt(va) * _sqrt(vb)
            if denom > 0.0:
                r = cov / denom
                if r < 0.0:
                    r = 0.0 - r
                acc = acc + r
                npair = npair + 1
            b = b + 1
        a = a + 1
    if npair == 0:
        return 0.0
    return acc / float(npair)


def sv_domain_sync(x, lo, hi, inh):
    """engine_cli.hexa:11532."""
    pop = sv_inhibit_domain(x, lo, hi, inh)
    return sv_lane_sync(pop, lo, hi)


def sv_sync_sweep(x, lo, hi, igrid):
    """engine_cli.hexa:11539."""
    out = []
    i = 0
    while i < len(igrid):
        out.append(sv_domain_sync(x, lo, hi, igrid[i]))
        i = i + 1
    return out


def sv_psi_sync_proxy(x, lo, hi, inh, r_ref):
    """engine_cli.hexa:11550."""
    return sv_domain_sync(x, lo, hi, inh) - r_ref


def sv_emit_drive_lanes():
    """engine_cli.hexa:11569."""
    return [0, 4]


def sv_domain_is_emit_disjoint(focus, w):
    """engine_cli.hexa:11574."""
    lo = focus * w
    hi = lo + w
    emit = sv_emit_drive_lanes()
    k = 0
    while k < len(emit):
        e = emit[k]
        if e >= lo and e < hi:
            return 0
        k = k + 1
    return 1


def sv_default_focus(d, w):
    """engine_cli.hexa:11592."""
    f = 0
    while f < d:
        if sv_domain_is_emit_disjoint(f, w) == 1:
            return f
        f = f + 1
    return 0 - 1


# ════════════════════════════════════════════════════════════════════════
# parity smoke driver — exercises CLI / MITOSIS / ρ·tether / ρ·self deterministically
# ════════════════════════════════════════════════════════════════════════

def _p(k, v):
    if isinstance(v, bool):
        print("%s=%s" % (k, str(v).lower()))
    elif isinstance(v, float):
        print("%s=%.17g" % (k, v))
    else:
        print("%s=%s" % (k, v))


# ════════════════════════════════════════════════════════════════════════
# ── P3 chat-critical symbols (py twin of engine_cli.hexa) ──
# Byte-exact port of the ~26 chat-critical faculties the consciousness
# session loop needs but that were missing from this py mirror. Same
# arithmetic / accumulation order / branch structure; hexa `to_float`→float,
# `to_int`→int, `sqrt`→_sqrt, `sin`→_sin, `cos`→_cos, `log2`→_math.log2,
# `ln`→_ln. hexa `_cos` (cosine-sim) is already ported as `_cos_vec`.
# Reproduced bug-for-bug (parity over accuracy · PARITY.md precedent).
# ════════════════════════════════════════════════════════════════════════

_log2 = _math.log2


# ── conflict scalars (engine_cli.hexa:8600) ──
def conflict_scalar(a_drive, g_drive):
    """engine_cli.hexa:8600 — both-strong competition gate (→0 same-sign / weak engine)."""
    if a_drive * g_drive >= 0.0:
        return 0.0
    am = _ci_abs(a_drive)
    gm = _ci_abs(g_drive)
    return _ci_clip01(am * gm)


def conflict_net_tension(a_drive, g_drive):
    """engine_cli.hexa:8611 — |a+g| net pull magnitude."""
    return _ci_abs(a_drive + g_drive)


def conflict_recruited_depth(conflict, base_budget, max_extra):
    """engine_cli.hexa:8620 — conflict → extra deliberation budget."""
    extra = int(_ci_clip01(conflict) * float(max_extra) + 0.5)
    return base_budget + extra


# ── tension_resolve family (engine_cli.hexa:11299) ──
def tr_psi(pop, thr):
    """engine_cli.hexa:11299 — Ψ = fraction of the population over the emit threshold."""
    nt = len(pop)
    if nt == 0:
        return 0.0
    emit = 0
    t = 0
    while t < nt:
        if ci_emit_drive(pop[t]) >= thr:
            emit = emit + 1
        t = t + 1
    return float(emit) / float(nt)


def _tr_absdev(psi, thr):
    """engine_cli.hexa:11312 — |psi - thr|."""
    if psi - thr >= 0.0:
        return psi - thr
    return thr - psi


def _spr_sig(pop):
    """engine_cli.hexa:11364 — mean of the isolated content lane (index 7)."""
    nt = len(pop)
    if nt == 0:
        return 0.0
    s = 0.0
    t = 0
    while t < nt:
        s = s + pop[t][7]
        t = t + 1
    return s / float(nt)


def tension_resolve_depth(x, adj, alpha, thr, maxdepth, op, eps, cfg):
    """engine_cli.hexa:11317 — settle-depth of the conflicted population under topo coupling."""
    pop = x
    settle_depth = 0.0 - 1.0
    psi = tr_psi(pop, thr)
    if _tr_absdev(psi, thr) < eps:
        settle_depth = 0.0
    d = 1
    while d <= maxdepth:
        if cfg.topo_couple:
            pop = topo_apply_op(pop, adj, alpha, op)
        psi = tr_psi(pop, thr)
        if settle_depth < 0.0 and _tr_absdev(psi, thr) < eps:
            settle_depth = float(d)
        d = d + 1
    return [settle_depth, psi]


def tension_resolve_interruptible(x, adj, alpha, thr, maxdepth, op, eps, salience_at, salience_pop, cfg):
    """engine_cli.hexa:11373 — phasic-salience reset (LC-NE attention capture) during settle."""
    pop = x
    rerouted = False
    settle_depth = 0.0 - 1.0
    psi = tr_psi(pop, thr)
    if _tr_absdev(psi, thr) < eps:
        settle_depth = 0.0
    d = 1
    while d <= maxdepth:
        if (not rerouted) and salience_at >= 1 and d == salience_at:
            pop = salience_pop
            rerouted = True
            settle_depth = 0.0 - 1.0
            psi = tr_psi(pop, thr)
            if _tr_absdev(psi, thr) < eps:
                settle_depth = float(d)
        if cfg.topo_couple:
            pop = topo_apply_op(pop, adj, alpha, op)
        psi = tr_psi(pop, thr)
        if settle_depth < 0.0 and _tr_absdev(psi, thr) < eps:
            settle_depth = float(d)
        d = d + 1
    sig = _spr_sig(pop)
    rf = 0.0
    if rerouted:
        rf = 1.0
    return [settle_depth, psi, sig, rf]


# ── referent selection (engine_cli.hexa:2686) ──
def referent_select(mem, cand_keys, true_ref):
    """engine_cli.hexa:2686 — first candidate with zero contradiction, else -1."""
    n = len(cand_keys)
    i = 0
    while i < n:
        f = affect_substrate_features(mem, cand_keys[i], true_ref)
        if f.contradiction == 0.0:
            return i
        i = i + 1
    return -1


def referent_select_text(mem, cands, true_ref):
    """engine_cli.hexa:2700 — text-candidate referent select (embed then select)."""
    keys = []
    i = 0
    while i < len(cands):
        keys.append(immune_embed_key(cands[i]))
        i = i + 1
    return referent_select(mem, keys, true_ref)


# ── drive arbitration (engine_cli.hexa:1704) ──
def drive_arbitrate(drives, hyst, prev_winner):
    """engine_cli.hexa:1704 — WTA over drives with basal-ganglia hysteresis hold."""
    n = len(drives)
    if n == 0:
        return -1
    best = 0
    bestv = drives[0]
    i = 1
    while i < n:
        if drives[i] > bestv:
            bestv = drives[i]
            best = i
        i = i + 1
    if prev_winner >= 0 and prev_winner < n:
        incv = drives[prev_winner]
        if bestv - incv <= hyst:
            return prev_winner
    return best


# ── faculty cascade (engine_cli.hexa:1629) ──
def faculty_cascade(mem_a, mem_b, q_key):
    """engine_cli.hexa:1629 — 2-hop recall chain q->x->y, ABSTAIN ("") propagates."""
    x = immune_memory_recall(mem_a, q_key)
    if x == "":
        return ""
    x_key = immune_embed_key(x)
    return immune_memory_recall(mem_b, x_key)


# ── event segmentation (engine_cli.hexa:1654) ──
def event_segment_boundaries(surprise_seq, thr):
    """engine_cli.hexa:1654 — surprise-peak boundaries (item 0 always opens event 0)."""
    n = len(surprise_seq)
    out = []
    if n == 0:
        return out
    out = out + [0]
    i = 1
    while i < n:
        s = surprise_seq[i]
        if s > thr:
            left_ok = s >= surprise_seq[i - 1]
            right_ok = True
            if i + 1 < n:
                right_ok = s > surprise_seq[i + 1]
            if left_ok and right_ok:
                out = out + [i]
        i = i + 1
    return out


def event_segment_starts_fixed(n, chunk):
    """engine_cli.hexa:1676 — fixed-chunk segment starts."""
    out = []
    if n <= 0:
        return out
    if chunk <= 0:
        return out
    i = 0
    while i < n:
        out = out + [i]
        i = i + chunk
    return out


# ── anticipatory prefetch (engine_cli.hexa:4589) ──
def _prefetch_unit(v):
    """engine_cli.hexa:4607 — L2-normalize (zero-safe passthrough)."""
    n = len(v)
    s = 0.0
    i = 0
    while i < n:
        s = s + v[i] * v[i]
        i = i + 1
    nrm = _sqrt(s)
    if nrm <= 0.0:
        return v
    out = []
    j = 0
    while j < n:
        out = out + [v[j] / nrm]
        j = j + 1
    return out


def anticipatory_prefetch(ff, mem, ctx):
    """engine_cli.hexa:4589 — graded readiness of the forward-predicted next query."""
    pred = vforward_predict(ff, ctx)
    key = _prefetch_unit(pred)
    return immune_memory_recall_margin(mem, key)


def anticipatory_prefetch_value(ff, mem, ctx):
    """engine_cli.hexa:4598 — recalled value of the forward-predicted next query."""
    pred = vforward_predict(ff, ctx)
    key = _prefetch_unit(pred)
    return immune_memory_recall(mem, key)


# ── stochastic-resonance channel MI (engine_cli.hexa:10736) ──
def _sr_mi_bits(xs, ys):
    """engine_cli.hexa:10736 — 2x2 mutual information in bits."""
    T = len(xs)
    if T == 0:
        return 0.0
    n00 = 0.0
    n01 = 0.0
    n10 = 0.0
    n11 = 0.0
    i = 0
    while i < T:
        if xs[i] == 0:
            if ys[i] == 0:
                n00 = n00 + 1.0
            else:
                n01 = n01 + 1.0
        else:
            if ys[i] == 0:
                n10 = n10 + 1.0
            else:
                n11 = n11 + 1.0
        i = i + 1
    tf = float(T)
    px0 = (n00 + n01) / tf
    px1 = (n10 + n11) / tf
    py0 = (n00 + n10) / tf
    py1 = (n01 + n11) / tf
    mi = 0.0
    if n00 > 0.0:
        p = n00 / tf
        mi = mi + p * _log2(p / (px0 * py0))
    if n01 > 0.0:
        p = n01 / tf
        mi = mi + p * _log2(p / (px0 * py1))
    if n10 > 0.0:
        p = n10 / tf
        mi = mi + p * _log2(p / (px1 * py0))
    if n11 > 0.0:
        p = n11 / tf
        mi = mi + p * _log2(p / (px1 * py1))
    return mi


def sr_channel_mi(amp, thr, sigma, period, T, mode, shuffle, seed):
    """engine_cli.hexa:10761 — MI(input, emit) over a noisy sub-threshold sine channel."""
    two_pi = 6.283185307179586
    ethr = 0.0 if mode == 1 else thr
    xs = []
    ys = []
    st = seed & 2147483647
    t = 0
    while t < T:
        sig = amp * _sin(two_pi * float(t) / float(period))
        g = _lcg_gauss(st)
        noise = sigma * g[0]
        st = int(g[1]) & 2147483647
        x = 1 if sig >= 0.0 else 0
        y = 1 if (sig + noise) >= ethr else 0
        xs = xs + [x]
        ys = ys + [y]
        t = t + 1
    if shuffle == 1:
        sh = (seed ^ 305419896) & 2147483647
        i = T - 1
        while i > 0:
            sh = _lcg_next(sh)
            j = sh % (i + 1)
            tmp = xs[i]
            xs[i] = xs[j]
            xs[j] = tmp
            i = i - 1
    return _sr_mi_bits(xs, ys)


# ── forward-model prefix decodability (engine_cli.hexa:411) ──
def fm_prefix_decodability(margins, decay):
    """engine_cli.hexa:411 — geometrically-decayed sum of prefix margins."""
    n = len(margins)
    acc = 0.0
    w = 1.0
    i = 0
    while i < n:
        acc = acc + w * margins[i]
        w = w * decay
        i = i + 1
    return acc


# ── CLI flag resolvers (engine_cli.hexa:265/365) ──
def _cli_refsel_flag(arg):
    """engine_cli.hexa:276 — parse --refsel / --no-refsel / --refsel=<v>."""
    n = len(arg)
    i = 0
    while i < n:
        a = arg[i]
        if a == "--no-refsel":
            return "off"
        if a == "--refsel":
            if i + 1 < n:
                v = _norm_onoff(arg[i + 1])
                if v != "":
                    return v
        if a.startswith("--refsel="):
            v = _norm_onoff(_after_eq(a))
            if v != "":
                return v
        i = i + 1
    return ""


def engine_cli_resolve_refsel(arg):
    """engine_cli.hexa:265 — refsel flag > env > default OFF."""
    flag = _cli_refsel_flag(arg)
    if flag == "on":
        return True
    if flag == "off":
        return False
    env = _norm_onoff(_env_read("ANIMA_REFSEL"))
    if env == "on":
        return True
    if env == "off":
        return False
    return False


def _cli_forward_model_flag(arg):
    """engine_cli.hexa:376 — parse --forward-model / --no-forward-model / --forward-model=<v>."""
    n = len(arg)
    i = 0
    while i < n:
        a = arg[i]
        if a == "--no-forward-model":
            return "off"
        if a == "--forward-model":
            if i + 1 < n:
                v = _norm_onoff(arg[i + 1])
                if v != "":
                    return v
        if a.startswith("--forward-model="):
            v = _norm_onoff(_after_eq(a))
            if v != "":
                return v
        i = i + 1
    return ""


def engine_cli_resolve_forward_model(arg):
    """engine_cli.hexa:365 — forward-model flag > env > default OFF."""
    flag = _cli_forward_model_flag(arg)
    if flag == "on":
        return True
    if flag == "off":
        return False
    env = _norm_onoff(_env_read("ANIMA_FORWARD_MODEL"))
    if env == "on":
        return True
    if env == "off":
        return False
    return False


# ── self-chain extras (engine_cli.hexa:8670+) ──
def _sc_conf_clamp(a):
    """engine_cli.hexa:8870 — clamp confluence alpha to [0, 0.5]."""
    if a <= 0.0:
        return 0.0
    if a >= 0.5:
        return 0.5
    return a


def self_drift_exp(s, content_axis, step):
    """engine_cli.hexa:8678 — experience-driven self drift along the expressed content axis."""
    ax = content_axis - (content_axis // s.dim) * s.dim
    v2 = []
    i = 0
    while i < s.dim:
        if i == ax:
            v2 = v2 + [s.v[i] + step]
        else:
            v2 = v2 + [s.v[i]]
        i = i + 1
    return SelfIdentity(_self_norm(v2, s.dim), s.dim)


def self_from_vec(v, dim):
    """engine_cli.hexa:8711 — build a normalized SelfIdentity from a raw vector."""
    return SelfIdentity(_self_norm(v, dim), dim)


def self_chain_confluence(w_natural, dream, alpha):
    """engine_cli.hexa:8875 — bounded pull of the morning self toward the unit dream direction."""
    a = _sc_conf_clamp(alpha)
    if a <= 0.0:
        return SelfIdentity(w_natural.v, w_natural.dim)
    dn = _self_norm(dream, w_natural.dim)
    v2 = []
    i = 0
    while i < w_natural.dim:
        v2 = v2 + [(1.0 - a) * w_natural.v[i] + a * dn[i]]
        i = i + 1
    return SelfIdentity(_self_norm(v2, w_natural.dim), w_natural.dim)


def self_chain_bend(w_natural, w_bent):
    """engine_cli.hexa:8890 — F1 bend magnitude = 1 - cos(w_natural, w_bent)."""
    return 1.0 - self_cos(w_natural, w_bent)


def self_chain_dream_gain(w_natural, w_bent, dream_unit):
    """engine_cli.hexa:8898 — F3 growth-dir gain toward the unit dream centroid."""
    dn = SelfIdentity(dream_unit, w_natural.dim)
    return self_cos(w_bent, dn) - self_cos(w_natural, dn)


def self_chain_unit_of(v, dim):
    """engine_cli.hexa:8904 — normalize a raw vector to a unit direction."""
    return _self_norm(v, dim)


# ── other-identity chain (engine_cli.hexa:8925 · model-of-you) ──
class OtherIdentity:
    __slots__ = ("v", "dim")

    def __init__(self, v, dim):
        self.v = v
        self.dim = dim


class OtherChain:
    __slots__ = ("flat", "count", "dim")

    def __init__(self, flat, count, dim):
        self.flat = flat
        self.count = count
        self.dim = dim


def other_new(dim, axis):
    """engine_cli.hexa:8937 — fresh interlocutor model = unit vector along `axis`."""
    v = []
    i = 0
    while i < dim:
        if i == axis:
            v = v + [1.0]
        else:
            v = v + [0.0]
        i = i + 1
    return OtherIdentity(v, dim)


def other_drift(o, tick, step):
    """engine_cli.hexa:8946 — content-blind drift along (tick+1)%dim, renormalized."""
    t1 = tick + 1
    ax = t1 - (t1 // o.dim) * o.dim
    v2 = []
    i = 0
    while i < o.dim:
        if i == ax:
            v2 = v2 + [o.v[i] + step]
        else:
            v2 = v2 + [o.v[i]]
        i = i + 1
    return OtherIdentity(_self_norm(v2, o.dim), o.dim)


def other_drift_exp(o, content_axis, step):
    """engine_cli.hexa:8961 — experience-driven drift toward the expressed content axis."""
    ax = content_axis - (content_axis // o.dim) * o.dim
    v2 = []
    i = 0
    while i < o.dim:
        if i == ax:
            v2 = v2 + [o.v[i] + step]
        else:
            v2 = v2 + [o.v[i]]
        i = i + 1
    return OtherIdentity(_self_norm(v2, o.dim), o.dim)


def other_cos(a, b):
    """engine_cli.hexa:8974 — interlocutor recognition cosine (unit-norm dot)."""
    sdot = 0.0
    i = 0
    while i < a.dim:
        sdot = sdot + a.v[i] * b.v[i]
        i = i + 1
    return sdot


def other_anchor(o):
    """engine_cli.hexa:8982 — persist a copy of the model-of-you."""
    return OtherIdentity(o.v, o.dim)


def other_component(o, i):
    """engine_cli.hexa:8988 — read accessor v[i]."""
    return o.v[i]


def other_dim(o):
    """engine_cli.hexa:8989 — read accessor dim."""
    return o.dim


def other_reset(dim, axis):
    """engine_cli.hexa:8992 — new blank interlocutor (continuity break)."""
    return other_new(dim, axis)


def other_chain_new(o):
    """engine_cli.hexa:8997 — start the interlocutor trajectory with the seed as w0."""
    f = []
    i = 0
    while i < o.dim:
        f = f + [o.v[i]]
        i = i + 1
    return OtherChain(f, 1, o.dim)


def other_chain_append(c, o):
    """engine_cli.hexa:9006 — append an anchor waypoint to the flat payload."""
    f = []
    i = 0
    while i < c.count * c.dim:
        f = f + [c.flat[i]]
        i = i + 1
    j = 0
    while j < c.dim:
        f = f + [o.v[j]]
        j = j + 1
    return OtherChain(f, c.count + 1, c.dim)


def _other_wp(c, k):
    """engine_cli.hexa:9016 — read waypoint k back as an OtherIdentity."""
    v = []
    base = k * c.dim
    i = 0
    while i < c.dim:
        v = v + [c.flat[base + i]]
        i = i + 1
    return OtherIdentity(v, c.dim)


def other_chain_len(c):
    """engine_cli.hexa:9024 — number of waypoints."""
    return c.count


def other_chain_latest(c):
    """engine_cli.hexa:9027 — newest waypoint wK."""
    return _other_wp(c, c.count - 1)


def other_chain_component(c, i):
    """engine_cli.hexa:9031 — flat payload accessor."""
    return c.flat[i]


def other_chain_dim(c):
    """engine_cli.hexa:9032 — chain dim."""
    return c.dim


def other_chain_count(c):
    """engine_cli.hexa:9033 — chain waypoint count."""
    return c.count


def other_chain_from_flat(flat, count, dim):
    """engine_cli.hexa:9036 — rebuild a chain from a persisted flat payload."""
    return OtherChain(flat, count, dim)


def other_chain_fit(cand, c):
    """engine_cli.hexa:9047 — trend-consistency of `cand` with the trajectory (0 for count<3)."""
    if c.count < 3:
        return 0.0
    wK = _other_wp(c, c.count - 1)
    wKm1 = _other_wp(c, c.count - 2)
    wKm2 = _other_wp(c, c.count - 3)
    dlast = []
    dprev = []
    i = 0
    while i < c.dim:
        dlast = dlast + [wK.v[i] - wKm1.v[i]]
        dprev = dprev + [wKm1.v[i] - wKm2.v[i]]
        i = i + 1
    aK = _argmax_abs(dlast, c.dim)
    aKm1 = _argmax_abs(dprev, c.dim)
    a_pred = _wrap(aK + (aK - aKm1), c.dim)
    r = []
    mag = 0.0
    j = 0
    while j < c.dim:
        e = cand.v[j] - wK.v[j]
        r = r + [e]
        mag = mag + e * e
        j = j + 1
    if mag <= 0.0:
        return 0.0
    m = _sqrt(mag)
    return r[a_pred] / m


def other_chain_retro_cos(c, j):
    """engine_cli.hexa:9080 — retrodiction cos(wK, w_{K-j})."""
    wK = _other_wp(c, c.count - 1)
    wj = _other_wp(c, c.count - 1 - j)
    return other_cos(wK, wj)


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

    # ── ImmuneMemory (ρ·tether) bind / recall / margin / gap ──
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

    # ── SelfIdentity (ρ·self) self-chain continuity + impostor ──
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

    # ── JamoHead (§KoJamoCountHead H_1316/1321/1351) — Voronoi count-MLE head ──
    # synthetic compositional fixture: 2D features in 4 regions, next-symbol vocab 3.
    jhdim = 2
    jhvj = 3
    jhX = [[0.0, 0.0], [0.2, 0.1], [0.1, 0.2], [3.0, 0.0], [3.1, 0.2], [2.9, 0.1],
           [0.0, 3.0], [0.1, 2.9], [0.2, 3.1], [3.0, 3.0], [2.9, 3.1], [3.1, 2.9]]
    jhY = [0, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0]
    jhntr = 9
    jhseed = [_sc_vmean(jhX)]
    jh0 = jamo_head_new(jhseed, jhvj, jhdim)
    _p("jh_cells_seed", jamo_head_cells(jh0))
    jhg = jamo_head_grow(jh0, jhX, jhY, jhntr, 6, 1, 0.10, 0.5, cfg_on)
    _p("jh_cells_grown", jamo_head_cells(jhg))
    jhXte = jhX[jhntr:]
    jhYte = jhY[jhntr:]
    _p("jh_ce", jamo_head_ce(jhg, jhXte, jhYte))
    _p("jh_head000", jhg.heads[0][0])
    _p("jh_argmax0", jamo_head_argmax(jhg, [0.05, 0.05]))
    _p("jh_recon0", jamo_head_recon_err(jhg, [0.05, 0.05]))
    jhsh = jamo_head_shuffle_targets(jhY, jhvj, 4290)
    _p("jh_shuf2", jhsh[2])
    _p("jh_shuf5", jhsh[5])
    jhg_off = jamo_head_grow(jh0, jhX, jhY, jhntr, 6, 1, 0.10, 0.5, cfg_off)
    _p("jh_cells_off", jamo_head_cells(jhg_off))

    # ── BpeMerges (§KoMorphologyBpe H_1388) — BPE merges over int stream ──
    base_sym = [1, 2, 1, 2, 3, 1, 2, 1, 2, 3, 1, 2, 4, 1, 2, 3]
    base_nby = [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2]
    bm = bpe_learn_merges(base_sym, base_nby, 4, 5, 0)
    _p("bpe_nmerges", len(bm.merges))
    _p("bpe_vocab", bpe_unit_vocab(bm))
    _p("bpe_merge0a", bm.merges[0][0])
    _p("bpe_merge0b", bm.merges[0][1])
    _p("bpe_merge0nid", bm.merges[0][2])
    bap = bpe_apply(bm, base_sym, base_nby)
    _p("bpe_nunits", bpe_n_units(bap[0]))
    _p("bpe_unit0", bap[0][0])
    _p("bpe_nby0", bap[1][0])
    bm_sh = bpe_learn_merges(base_sym, base_nby, 4, 5, 99)
    _p("bpe_sh_merge0a", bm_sh.merges[0][0])
    # byte-fair CE: build a jamo head over the unit features, score held-out
    bunits = bap[0]
    bnby = bap[1]
    bfeat = []
    btgt = []
    bnbyt = []
    bi = 0
    while bi < len(bunits) - 1:
        bfeat.append([float(bunits[bi]), float(bnby[bi])])
        btgt.append(bunits[bi + 1] % 3)
        bnbyt.append(bnby[bi])
        bi = bi + 1
    bjh = jamo_head_grow(jamo_head_new([_sc_vmean(bfeat)], 3, 2), bfeat, btgt,
                         len(bfeat) - 2, 5, 1, 0.10, 0.5, cfg_on)
    _p("bpe_bfce", bpe_byte_fair_ce(bjh, bfeat[len(bfeat) - 2:], btgt[len(btgt) - 2:],
                                    bnbyt[len(bnbyt) - 2:]))

    # ── §ConsciousnessIndex (ci_*) — 15-lane scores + Gaussian/IIT-4 Φ ──
    cipop = []
    ci_i = 0
    while ci_i < 12:
        mf = [0.1 + 0.05 * float(ci_i), 0.2 + 0.01 * float(ci_i),
              0.3 - 0.02 * float(ci_i), 0.05 * float(ci_i)]
        crow = ci_lane_scores(0.3 + 0.04 * float(ci_i), mf, ci_i + 1, ci_i,
                              ci_i % 2, 0.1 * float(ci_i), 0.15 + 0.03 * float(ci_i))
        cipop.append(crow)
        ci_i = ci_i + 1
    _p("ci_lane_gws", cipop[5][0])
    _p("ci_lane_ent", cipop[5][12])
    _p("ci_lane_emo", cipop[5][9])
    _p("ci_bundle_all", ci_bundle(cipop, -1))
    _p("ci_bundle_abl3", ci_bundle(cipop, 3))
    _p("ci_phi_full", ci_phi_multiinfo(cipop, -1))
    _p("ci_phi_abl0", ci_phi_multiinfo(cipop, 0))
    _p("ci_phi_iit4", ci_phi_iit4(cipop, [0, 1, 2, 3, 4, 5, 6, 7]))
    _p("ci_phi_drop2", ci_phi_drop2(cipop, 1, 2))
    cipi = ci_pair_interaction(cipop, 1, 2)
    _p("ci_pair_inter", cipi[2])
    _p("ci_surrogate", ci_surrogate_phi0(cipop, 12345))
    _p("ci_subset_proxy", ci_phi_multiinfo_subset_proxy(cipop, [0, 1, 2, 3]))

    # ── §BrainTopology (topo_*) — placement + connectome Φ ──
    cfg_topo = EngineConfig(True, "conv", True, False)
    badj = topo_brain_adjacency()
    _p("topo_edge03", badj[0][3])
    _p("topo_edge01", badj[0][1])
    _p("topo_lit01", topo_literal_adjacency()[0][1])
    _p("topo_optperm0", topo_optimal_perm()[0])
    _p("topo_optadj_28", topo_optimal_adjacency()[2][8])
    _p("topo_dmr_sum", _topo_row_l2(topo_degree_matched_random(7)[0]))
    _p("topo_phi_flat", topo_phi_flat(cipop, 0.5))
    _p("topo_phi_brain", topo_phi_brain(cipop, 0.5))
    _p("topo_phi_random1", topo_phi_random(cipop, 0.5, 7))
    _p("topo_phi_lateral", topo_phi_lateralized(cipop, 0.5))
    _p("topo_phi_coordsh", topo_phi_coords_shuffled(cipop, 0.5, 7))
    _p("topo_phi_geomsh", topo_phi_geometry_shuffled(cipop, 0.5, 7))
    _p("topo_phi_rndmean", topo_phi_random_mean(cipop, 0.5, 100, 3))
    _p("topo_phi_shufmean", topo_phi_shuffle_mean(cipop, 0.5, 100, 3))
    _p("topo_phi_geomean", topo_phi_geometry_shuffle_mean(cipop, 0.5, 100, 3))
    _p("topo_phi_huba0", topo_phi_hub_ablated(cipop, 0.5, 0))
    _p("topo_phi_optimal", topo_phi_optimal(cipop, 0.5))
    _p("topo_phi_litadj", topo_phi_adj(cipop, topo_literal_adjacency(), 0.5))
    _p("topo_phi_litrnd", topo_phi_random_of_mean(cipop, topo_literal_adjacency(), 100, 2, 0.5))
    _p("topo_phi_litrel", topo_phi_relabel_of_mean(cipop, topo_literal_adjacency(), 100, 2, 0.5))
    _p("topo_beats_brain", topo_relabel_beats_brain_count(cipop, 0.5, 100, 5))
    _p("topo_funcint", topo_func_integration(cipop, badj, 0.5))
    _p("topo_funcint_flat", topo_func_integration_flat(cipop))
    # ── ci coupled / Ψ-balance group ──
    _p("ci_emit_dec5", ci_emit_decision(cipop[5]))
    _p("ci_emit_drive5", ci_emit_drive(cipop[5]))
    _p("ci_psi_off", ci_psi_balance(cipop, badj, 0.5, cfg_on))
    _p("ci_psi_on", ci_psi_balance(cipop, badj, 0.5, cfg_topo))
    thr = ci_off_median_drive(cipop)
    _p("ci_off_median", thr)
    _p("ci_psi_cent_off", ci_psi_balance_centered(cipop, badj, 0.5, thr, cfg_on))
    _p("ci_psi_cent_on", ci_psi_balance_centered(cipop, badj, 0.5, thr, cfg_topo))
    rawlanes = ci_lane_scores_coupled(0.5, [0.2, 0.3, 0.1, 0.4], 3, 2, 1, 0.3, 0.25,
                                      badj, 0.5, cfg_on)
    couplanes = ci_lane_scores_coupled(0.5, [0.2, 0.3, 0.1, 0.4], 3, 2, 1, 0.3, 0.25,
                                       badj, 0.5, cfg_topo)
    _p("ci_coup_l2diff", ci_lane_vector_l2_diff(rawlanes, couplanes))
    _p("topo_op_mc", topo_apply_op(cipop, badj, 0.5, 1)[5][0])
    _p("topo_op_rs", topo_apply_op(cipop, badj, 0.5, 2)[5][0])
    _p("topo_op_rn", topo_apply_op(cipop, badj, 0.5, 3)[5][0])
    _p("ci_psi_op1", ci_psi_balance_op(cipop, badj, 0.5, 1, thr, cfg_topo))
    _p("ci_psi_op2", ci_psi_balance_op(cipop, badj, 0.5, 2, thr, cfg_topo))
    _p("topo_funcint_op2", topo_func_integration_op(cipop, badj, 0.5, 2))
    _p("topo_maxalpha", topo_psi_max_feasible_alpha(cipop, badj, 1, thr, 0.1, cfg_topo))

    # ── §ThirdLaw + §Savant — savant scoring (faithful IIT-4 min-cut Φ) ──
    cfg_sav = EngineConfig(True, "conv", False, True)
    _p("sa_gz_lo", sa_gz_lower())
    _p("sa_in_gz", sa_in_golden_zone(0.3))
    _p("tl_score", third_law_score(0.6, 0.7, 0.3))
    _p("tl_sing", third_law_singularity(0.6, 0.7, 0.3))
    _p("tl_ability", third_law_ability(0.6, 0.7, 0.3))
    _p("tl_ratio", third_law_ratio(8, 8, 8))
    _p("tl_overlap", third_law_overlap(8, 8, 8))
    _p("tl_i50", third_law_i50(8, 8, 8))
    _p("tl_abl_lat", third_law_ability_latched(0.6, 0.7, 0.6, 1))
    _p("tl_hyst", third_law_hysteresis_width(0.9, 0.9, 40, 40))
    _p("sv_gz_lo", sv_gz_lower())
    _p("sv_in_gz", sv_in_golden_zone(0.3))
    _p("sv_si", sv_savant_index([1.0, 0.2, 0.3, 0.25]))
    igrid = [0.1, 0.21231792755821914, 0.35, 0.5, 0.75]
    _p("sv_dphi0", sv_domain_phi(cipop, 0, 3, 0.35))
    _p("sv_phis_focus2", sv_savant_index_at(cipop, 5, 3, 2, 0.35, 0.5))
    swp = sv_focus_phi_sweep(cipop, 6, 9, igrid)
    _p("sv_sweep2", swp[2])
    _p("sv_dphi_peak", sv_dphi_peak_inh(swp, igrid))
    phis2 = sv_domain_phis(cipop, 5, 3, 2, 0.35, 0.5)
    _p("sv_trig_on", sv_savant_trigger(phis2, 0.35, 1.0, cfg_sav))
    _p("sv_trig_off", sv_savant_trigger(phis2, 0.35, 1.0, cfg_on))
    _p("sv_psi_sav_off", ci_psi_balance_savant(cipop, 6, 9, 0.35, thr, cfg_on))
    _p("sv_psi_sav_on", ci_psi_balance_savant(cipop, 6, 9, 0.35, thr, cfg_sav))
    _p("sv_lane_sync", sv_lane_sync(cipop, 0, 3))
    _p("sv_dom_sync", sv_domain_sync(cipop, 6, 9, 0.35))
    rref = sv_lane_sync(cipop, 6, 9)
    _p("sv_psi_sync", sv_psi_sync_proxy(cipop, 6, 9, 0.35, rref))
    _p("sv_emit_disj2", sv_domain_is_emit_disjoint(2, 3))
    _p("sv_emit_disj0", sv_domain_is_emit_disjoint(0, 3))
    _p("sv_default_focus", sv_default_focus(5, 3))

    # ── Compose arbiters (mem×ToM / spatial×episodic / ToM×spatial/basal / cereb×mem) ──
    mtmem = immune_grow_new(immune_embed_key("where is ball"), "basket", 8, 8, True)
    mtmem = immune_grow_bind(mtmem, immune_embed_key("where is cup"), "box", cfg_on)
    mtom = other_mind_new()
    mtom = other_mind_witness(mtom, "where is ball", "box")
    _p("mt_route_r", mem_tom_route_cue(True))
    _p("mt_route_b", mem_tom_route_cue(False))
    _p("mt_mem_margin", mem_tom_mem_margin(mtmem, immune_embed_key("where is ball")))
    _p("mt_tom_margin", mem_tom_tom_margin(mtom, immune_embed_key("where is ball")))
    _p("mt_compose", mem_tom_compose(mtmem, mtom, "where is ball", True, 0.5, 0.5))
    _p("mt_compose_rt", mem_tom_compose_routed(mtmem, mtom, "where is ball", 0.2, 0.5, 0.5))
    sesm = spatial_map_new()
    sesm = spatial_map_place(sesm, "X", 0.0, 0.0)
    sesm = spatial_map_place(sesm, "A", 1.0, 0.0)
    sesm = spatial_map_place(sesm, "B", 5.0, 0.0)
    semem = immune_grow_new(immune_embed_key("landmark A"), "optA", 8, 8, True)
    semem = immune_grow_bind(semem, immune_embed_key("landmark B"), "optB", cfg_on)
    _p("se_where_cue", spatial_episodic_where_cue("which landmark is nearer to"))
    sev = spatial_episodic_spatial_vote(sesm, "X", "A", "B", 0, 1)
    _p("se_sp_vote", sev[0])
    _p("se_sp_conf", sev[1])
    eev = spatial_episodic_episodic_vote(semem, immune_embed_key("landmark B"))
    _p("se_ep_vote", eev[0])
    _p("se_compose", spatial_episodic_compose(int(sev[0]), sev[1], int(eev[0]), eev[1],
                                              0.5, 0.5, 0.7))
    tsv = tom_spatial_tom_vote(mtom, "where is ball", 0.2)
    ssv = tom_spatial_spatial_vote(sesm, 1.0, 0.2)
    _p("ts_tom_conf", tsv[2])
    _p("ts_compose", tom_spatial_compose(tsv, ssv, 0.5, 0.5))
    tbv = tom_basal_tom_vote(mtom, "where is ball", 0.2)
    _p("tb_compose", tom_basal_compose(tbv, [1.0, 0.0, 0.5], 0.5, 0.5))
    cmff = vforward_new(1, 1, 0.5)
    cmmem = immune_grow_new(immune_embed_key("cup loc"), "box", 8, 8, True)
    ccv = cereb_mem_cerebellum_vote(cmff, 1.0, 0.5)
    cmv = cereb_mem_memory_vote(cmmem, immune_embed_key("cup loc"), 0.5)
    _p("cm_cereb_conf", ccv[2])
    _p("cm_mem_vote", cmv[0])
    _p("cm_compose", cereb_mem_compose(ccv, cmv, 0.5, 0.5))

    # ── Consciousness-gate R2 lanes (family B) ──
    _p("trw_in", trw_recall(2, 5, 6))
    _p("trw_out", trw_recall(2, 5, 9))
    _p("trw_shuf", trw_recall_shuffled(2, 5, 6))
    _p("reentry_d5", reentry_settle(5, 0.3))
    _p("reentry_gws", reentry_gws_readout(5))
    _p("attn_track", attn_schema_report(3, 3, True))
    _p("attn_miss", attn_schema_report(3, 2, True))
    _p("attn_off", attn_schema_report(3, 3, False))
    _p("attn_agency", attn_schema_agency_readout(3))
    _p("hyst_up", hyst_switch_point(True, 0.4))
    _p("hyst_down", hyst_switch_point(False, 0.4))
    _p("hyst_riv", hyst_rivalry_loop(True))
    _p("comp_on", completion_recognize(0.9, True))
    _p("comp_off", completion_recognize(0.9, False))
    _p("comp_img", completion_imagery_readout())
    _p("gest_bind", gestalt_same_group(0.4, True))
    _p("gest_split", gestalt_same_group(0.2, True))
    _p("gest_gws", gestalt_gws_readout())
    _p("prosp_reach", prospect_reach(3, 2))
    _p("prosp_stuck", prospect_reach(0, 2))
    _p("prosp_persist", prospect_persist_readout())
    _p("intero_prec", intero_precision(0.5))
    _p("intero_wt", intero_weighted_error(0.2, 0.1, 0.8, 0.5, False))
    _p("intero_blind", intero_weighted_error(0.2, 0.1, 0.8, 0.5, True))
    _p("bored_both", boredom_disengage(0.3, 0.3, True))
    _p("bored_rew", boredom_disengage(0.3, 0.8, True))
    _p("bored_abl", boredom_disengage(0.3, 0.8, False))
    _p("wander_on", wander_coverage(5, 10, True))
    _p("wander_off", wander_coverage(5, 10, False))
    _p("wander_prosp", wander_prospect_coverage(10))
    _p("qualia_near", qualia_nearer(0.2, 0.5))
    _p("qualia_sp", qualia_spatial_readout())
    _p("smp_pres", smp_presence(3, 5, True))
    _p("smp_false", smp_presence(3, 5, False))
    _p("smp_fwd", smp_forward_model_readout(5))
    _p("real_call", reality_call(0.4, 0.3))
    _p("real_imag", reality_call(0.1, 0.3))
    _p("real_abl", reality_call_ablated())
    _p("real_imgrd", reality_imagery_readout())
    _p("real_conf", reality_confidence_readout(True))

    # ── §Neuropharm / §Field / §PCI / §Metacog / §Hallucination / §FieldLibido (family C) ──
    trials = [
        [0.6, 0.2, 0.3, 0.1, 0.4, 0.2, 3, 1, 1, 0.3, 0.25],
        [0.4, 0.5, 0.1, 0.3, 0.2, 0.1, 2, 0, 0, 0.2, 0.40],
        [0.7, 0.1, 0.4, 0.2, 0.3, 0.5, 5, 2, 1, 0.5, 0.15],
        [0.3, 0.3, 0.3, 0.3, 0.1, 0.2, 1, 3, 0, 0.1, 0.50],
        [0.8, 0.6, 0.2, 0.1, 0.05, 0.3, 4, 1, 1, 0.4, 0.20],
        [0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 3, 2, 0, 0.3, 0.30],
    ]
    lsd = pharm_lsd()
    _p("ph_lsd0", lsd[0])
    _p("ph_dmt3", pharm_dmt()[3])
    _p("ph_sse", pharm_shared_se(lsd, 42, 3))
    _p("ph_pm", pharm_perturb_m(lsd, 0.7, 0.1))
    _p("ph_pf2", pharm_perturb_field(lsd, [0.2, 0.3, 0.1, 0.4, 0.2], 0.05)[2])
    _p("ph_prec", pharm_perturb_recon(lsd, 0.3, 0.05))
    _p("ph_pdt", pharm_perturb_dt(pharm_cannabis(), 0.4))
    _p("ph_selfcont", pharm_self_continuity(pharm_dmt(), 8, 5))
    _p("ph_realfrac", pharm_reality_real_fraction(lsd, [0.4, 0.5, 0.3, 0.6, 0.2, 0.45], 42, 0.30))
    _p("ph_phi", pharm_phi(lsd, trials, 42))
    _p("ph_phi_ket", pharm_phi(pharm_ketamine(), trials, 42))
    _p("ph_subjtime", pharm_subjective_time_rate(pharm_cannabis(), trials, 42))
    _p("ph_wm", pharm_working_mem(pharm_cannabis(), trials, 42))
    fmf = [0.2, 0.3, 0.1, 0.4, 0.2]
    fav = field_apply(0.5, fmf, 3, 1, 1, 0.3, 0.25, 3, 0.5, 1, 1, False, 0.0)
    _p("fld_apply0", fav[0])
    _p("fld_mfield1", field_apply_mfield(fmf, 0.5, 1, 1)[3])
    _p("fld_entropy", field_signal_entropy(fmf))
    _p("fld_drug2", drug_lsd_mfield(fmf, 42, 3)[2])
    _p("fld_lz", _field_lz76([1, 0, 1, 1, 0, 0, 1, 0, 1, 1]))
    R = pci_perturb(0.5, fmf, 3, 1, 1, 0.3, 0.25, 4, 0.6, 1, 1, True, 6)
    _p("pci_coupled", pci_complexity(R, False))
    _p("pci_decoup", pci_complexity(R, True))
    _p("fld_lanemean", field_lane_mean(fav, [0, 4, 14]))
    _p("mi_marg_h", mi_signal_margin(42, True, 3))
    _p("mi_marg_g", mi_signal_margin(42, False, 3))
    _p("mi_judge", mi_insight_judge(0.1, 1.0))
    _p("mi_psyched", mi_insight_psychedelic(42, 20))
    _p("mi_psychot", mi_insight_psychotic(42, 20))
    _p("mi_metad", mi_metad_auroc(42, 20))
    _p("mi_shuf", mi_shuffle_auroc(42, 20))
    _p("hall_call", hallucinate_call(0.8, 0.9, 0.0, 0.3))
    _p("hall_grad", hallucinate_graded(0.8, 0.1))
    _p("hall_abl", hallucinate_ablated(0.1, 0.3))
    _p("hall_drug", hallucinate_under_drug(lsd, 0.5, 0.9, 0.30))
    _p("mc_ece", mc_calibration_ece(42, 6))
    _p("mc_mono", mc_calibration_monotone(42, 6))
    _p("mc_lift", mc_control_lift(42, 6))
    _p("mc_lift_abl", mc_control_lift_ablated(42, 6))
    mco = mc_auroc_calibration_orthogonal(42, 6)
    _p("mc_au_base", mco[0])
    _p("mc_au_xform", mco[1])
    _p("mc_ece_base", mco[2])
    _p("mc_ece_xform", mco[3])
    _p("mc_shuf", mc_shuffle_auroc(42, 6))
    _p("fl_gfield", fieldlibido_gfield(0.5, fmf, 3, 1, 1, 0.3, 0.25, 6, 0.5, 1))
    _p("fl_wanting", fieldlibido_wanting(0.5, fmf, 3, 1, 1, 0.3, 0.25, 0.6, 0.2, 0.5, 6, 0.5, 1))
    _p("fl_liking", fieldlibido_liking(0.5))
    _p("fl_high", fieldlibido_highfreq(0.5, fmf, 3, 1, 1, 0.3, 0.25, 0.5))
    _p("fl_low", fieldlibido_lowfreq(0.5, fmf, 3, 1, 1, 0.3, 0.25, 0.5))
    _p("fl_sham", fieldlibido_sham(0.5, fmf, 3, 1, 1, 0.3, 0.25))
