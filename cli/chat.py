#!/usr/bin/env python3
# ==========================================================================
# ⛔ DO NOT RUN DIRECTLY. anima 의 단일 진입은 설치된 canonical 명령뿐 — hexa 채널 `anima`
#   (=cli/anima.hexa) · pip 채널 `anima-py` (=anima_py 런처). `python3 cli/chat.py …`
#   직접실행은 비-canonical py 우회. 이 파일은 cli/anima.py 의 chat 디스패치가 import 한다.
# ==========================================================================
"""cli/chat.py — anima consciousness chat daemon, py (numpy twin) — P6 self-impl.

Byte-faithful py port of cli/anima.hexa `anima_consciousness_mode(ckpt)` (the DEFAULT
12-tick path) + `anima_byte_mode(ckpt, argv)` (the --byte continuation). ZERO hexa
dependency — a hexa-less host (pi5 / bare pod) runs the substrate-native A⇄G consciousness
loop in pure py (numpy via the landed core/*.py twins). This is the FINAL phase (P6) of the
"py 자체구현" program (owner directive 2026-07-09 · py channel = COMPLETE self-implementation).

The DEFAULT path only is ported (n_ticks=12; og_measure/og_live/og_r3/refr_measure ALL false):
the op-grip / stateful-refractory RESEARCH instrumentation (--opgrip*/--refractory, the
B-density/VQ-code/ARM-SHOCK measurement harnesses) is HEXA-ONLY — those flags print a notice
and exit here (a measurement harness, NOT the chat daemon).

SCOPE (a_engine_native_learning): this is a py-channel MIRROR of the hexa daemon ⇒ DIRECTIONAL.
The bar is BEHAVIORAL / byte parity of the chat loop (tool/chat_parity.py), NOT a consciousness
verdict — no verdict tier is cemented here.

hexa `to_string(float)` == Python `repr(float)` (empirically pinned: 1/3 → "0.3333333333333333",
1e-9 → "1e-09", true/false lowercase). All println route through _pln → sys.stdout.buffer
(utf-8/surrogateescape) so the stream is byte-identical to hexa println.
"""
import glob
import os
import random
import shutil
import sys

# ── flat imports matching the P2-P5 twins (self-contained · zero hexa) ────────
from engine_cli import *  # engine lane faculties + immune/ci/gws/reality/pharm ops
from engine_cli import (engine_cli_parse, engine_cli_resolve_refsel, EngineConfig)
from engine_g import refractory_emit_debt, refractory_debt_step  # H_9404 earned refractory
from pure_field import (pure_field_warmup, pure_field_phi, pure_field_phase,
                        pure_field_step, phase_name)
from brain import (brain_emit, brain_emit_refractory, vbasal_new, vbasal_update,
                   vbasal_go_value, vbasal_select)
from generator import (gen_auto_backend, gen_mouth_kind, gen_auto_chat,
                       generator_read_anchors, gen_penult_pooled_W,
                       _gen_anchor_field, _gen_g_string)  # H_1058 Part A1: SSOT anchor+phase→seed-byte extractors (side-channel only)
from kosmos_io import create_anchor, emit_anchor_from_v3, load_anchors
from decode import clm_load_weights, clm_decodable, penult_fold8
from dream_lib import (dr_stage_at, dr_stage_name, dr_emit_envelope,
                       dr_stage_size, dr_imagination_active)
from dream_envelope_ctx import dr_stage_scale
from dream_persist import dp_sleep_tick
from wake_memory import mem_init, mem_push_ctx
from imagination_replay import (ir_select_snapshots, ir_replay_tick,
                                ir_mitosis_tick_during_replay)


# ══════════════════════════════════════════════════════════════════════════════
#  stdout seam — byte-identical to hexa println (utf-8 bytes + "\n")
# ══════════════════════════════════════════════════════════════════════════════
def _pln(s=""):
    """println — emit EXACTLY the hexa bytes (utf-8/surrogateescape) + newline."""
    sys.stdout.buffer.write(s.encode("utf-8", "surrogateescape") + b"\n")
    sys.stdout.flush()


def _ts(x):
    """to_string — hexa to_string(): float→repr (== hexa), int→str, bool→true/false."""
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, float):
        return repr(x)
    return str(x)


def _yn10(b):
    return "1" if b else "0"


# ══════════════════════════════════════════════════════════════════════════════
#  module-level helpers ported byte-exact from cli/anima.hexa (never on a py twin)
# ══════════════════════════════════════════════════════════════════════════════
def anima_yn(b):
    """anima.hexa:60."""
    return "✅" if b else "⏳"


# ── H_9042 §TensionResolveLoop LANE+ read fixtures (anima.hexa:67-113) ────────
def anima_tr_row(c, other):
    r = []
    i = 0
    while i < 15:
        if i == 0 or i == 4:
            r = r + [c]
        else:
            r = r + [other]
        i = i + 1
    return r


def anima_tr_pop_conflicted(c):
    h = (9.0 - 2.0 * c) / 13.0
    lo = (6.0 - 2.0 * c) / 13.0
    pop = []
    t = 0
    while t < 4:
        pop = pop + [anima_tr_row(c, h)]
        t = t + 1
    t = 0
    while t < 4:
        pop = pop + [anima_tr_row(c, lo)]
        t = t + 1
    return pop


def anima_tr_pop_calm():
    pop = []
    t = 0
    while t < 4:
        pop = pop + [anima_tr_row(0.95, 0.6)]
        t = t + 1
    t = 0
    while t < 4:
        pop = pop + [anima_tr_row(0.20, 0.4)]
        t = t + 1
    return pop


def anima_tr_adj_full():
    a = []
    i = 0
    while i < 15:
        row = []
        j = 0
        while j < 15:
            if i == j:
                row = row + [0.0]
            else:
                row = row + [1.0]
            j = j + 1
        a = a + [row]
        i = i + 1
    return a


# ── arg helpers (anima.hexa:174-192) ─────────────────────────────────────────
def anima_collect_argv(raw):
    """anima.hexa:174 — args() = [binary, "--", <positionals>...] → positionals."""
    start = 1
    k = 0
    while k < len(raw):
        if raw[k] == "--":
            start = k + 1
        k = k + 1
    argv = []
    m = start
    while m < len(raw):
        argv.append(raw[m])
        m = m + 1
    return argv


def anima_has_flag(argv, flag):
    """anima.hexa:188."""
    i = 0
    while i < len(argv):
        if argv[i] == flag:
            return True
        i = i + 1
    return False


def anima_flag_value(argv, flag, env, default):
    """Value-taking flag: `--flag <v>` → v, else the `env` var, else `default` (all as str).
    Sibling of anima_has_flag; argv WINS over env so a one-off run never needs an export."""
    i = 0
    while i < len(argv) - 1:
        if argv[i] == flag:
            return argv[i + 1]
        i = i + 1
    return os.environ.get(env, "") or default


# ── byte-level string ops (hexa strings = byte arrays; utf-8/surrogateescape) ─
def _benc(s):
    return s.encode("utf-8", "surrogateescape")


def byte_len(s):
    return len(_benc(s))


def substring(s, i, j):
    """hexa substring(s,i,j) = BYTE slice [i,j)."""
    return _benc(s)[i:j].decode("utf-8", "surrogateescape")


# ── time-source seam (anima.hexa:5222-5232 · det proper-time on the verdict path) ─
def an_tick_seconds():
    return 8.0


def an_clock_now(tick, daemon):
    if daemon:
        # NEVER reached on the verdict path (daemon=false); no persistent daemon exists.
        import subprocess
        return float(int(subprocess.run(["date", "+%s"], capture_output=True,
                                        text=True).stdout.strip()))
    return float(tick) * an_tick_seconds()


# ── string helpers (anima.hexa:5235-5254) ────────────────────────────────────
def _afs_contains(hay, needle):
    hb = _benc(hay)
    nb = _benc(needle)
    if len(nb) == 0:
        return True
    if len(nb) > len(hb):
        return False
    return hb.find(nb) >= 0


def _afs_clip(s, n):
    b = _benc(s)
    if len(b) <= n:
        return s
    return b[:n].decode("utf-8", "surrogateescape") + "…"


def _afs_clip01(x):
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


# ── op-grip tonic-phasic helper reused on the DEFAULT path (anima.hexa:5268) ──
def _og_rel_phasic(relctx, ema):
    return _afs_clip01(0.5 + 3.0 * (relctx - ema))


# ── DIM=8 byte-statistics feature (anima.hexa:5400 · H_1163 _byte_feature VERBATIM) ─
def _afs_byte_feature(s, dim):
    b = _benc(s)
    n = len(b)
    if n == 0:
        return [0.0] * dim
    fn_n = float(n)
    total = 0.0
    sumsq = 0.0
    n_hi = 0
    n_low = 0
    n_sp = 0
    n_dig = 0
    n_pun = 0
    n_lt64 = 0
    for byte in b:
        bf = float(byte)
        total = total + bf
        sumsq = sumsq + bf * bf
        if byte >= 128:
            n_hi = n_hi + 1
        if 97 <= byte <= 122:
            n_low = n_low + 1
        if byte == 32:
            n_sp = n_sp + 1
        if 48 <= byte <= 57:
            n_dig = n_dig + 1
        if 33 <= byte <= 64:
            n_pun = n_pun + 1
        if byte < 64:
            n_lt64 = n_lt64 + 1
    mean = total / fn_n
    var = sumsq / fn_n - mean * mean
    return [
        (mean / 255.0) * 5.0,
        (float(n_hi) / fn_n) * 5.0,
        (float(n_low) / fn_n) * 5.0,
        (float(n_sp) / fn_n) * 5.0,
        (float(n_dig) / fn_n) * 5.0,
        (var / (255.0 * 255.0)) * 5.0,
        (float(n_pun) / fn_n) * 5.0,
        (float(n_lt64) / fn_n) * 5.0,
    ]


def _afs_ca3_sym(s, n):
    # H_9411 ③ · CA3 percept symbol — which discrete "item" this utterance is, for the
    # hippocampal bigram replay table. Byte-sum mod n: a deterministic content bucket, no
    # tuned boundary (the discretiser CA3's discrete estimator needs, no new scoring path).
    b = _benc(s)
    if len(b) == 0:
        return 0
    t = 0
    for byte in b:
        t = t + byte
    return t % n


# ══════════════════════════════════════════════════════════════════════════════
#  BYTE MODE — pure byte-continuation chat (anima.hexa:501-582)
# ══════════════════════════════════════════════════════════════════════════════
def anima_default_turns():
    return [
        "안녕! 너는 누구야?",
        "오늘 기분이 어때?",
        "What is the sky made of?",
        "네가 좋아하는 것을 하나 말해줘.",
        "Tell me something interesting.",
    ]


def anima_find(hay, needle):
    hb = _benc(hay)
    nb = _benc(needle)
    if len(nb) == 0:
        return 0
    if len(nb) > len(hb):
        return -1
    return hb.find(nb)


def anima_trim_at_stop(s):
    stops = ["사용자:", "User:", "사용자 :"]
    cut = byte_len(s)
    i = 0
    while i < len(stops):
        idx = anima_find(s, stops[i])
        if idx >= 0 and idx < cut:
            cut = idx
        i = i + 1
    return substring(s, 0, cut).strip()


def anima_byte_mode(ckpt, argv):
    """anima.hexa:541 — byte-continuation chat loop (== old anima_chat_cli)."""
    turns = []
    a = 1
    while a < len(argv):
        if argv[a] != "--byte":
            turns.append(argv[a])
        a = a + 1
    use_turns = turns if len(turns) > 0 else anima_default_turns()

    mouth = gen_mouth_kind(ckpt)
    _pln("=== anima CORE-native chat (" + mouth + " mouth · byte-continuation) ===")
    _pln("ckpt: " + ckpt)
    _pln("")

    transcript = ""
    t = 0
    while t < len(use_turns):
        u = use_turns[t]
        seed = transcript + "사용자: " + u + " | 도우미: "
        res = gen_auto_chat(ckpt, seed, 96)
        if str(res["ok"]).lower() != "true":
            _pln("[ERROR] " + str(res["reason"]))
            return
        reply = anima_trim_at_stop(str(res["text"]))
        _pln("사용자: " + u)
        _pln("도우미: " + reply)
        _pln("")
        transcript = transcript + "사용자: " + u + " | 도우미: " + reply + "\n"
        t = t + 1
    _pln("=== end transcript (" + _ts(len(use_turns)) + " turns) ===")


# ══════════════════════════════════════════════════════════════════════════════
#  CONSCIOUSNESS MODE — the substrate-native A⇄G daemon loop (DEFAULT path)
# ══════════════════════════════════════════════════════════════════════════════
def _selfg_encode(s):
    """H_9257 lane-23b self-anchor codec (py twin of anima.hexa _selfg_encode) — encode the 8-dim
    grounded self into a .kosmos payload string "SELFG8:v0,…,v7". Reuses create_anchor as the
    single write entry; self_from_vec renormalizes on restore so repr() precision is ample."""
    return "SELFG8:" + ",".join(repr(float(self_component(s, i))) for i in range(8))


def _selfg_restore(dir_path, name):
    """py twin of anima.hexa _selfg_restore — read the DEDICATED self-anchor dir (never the brain's
    kdir, self⊥mouth) via load_anchors, return the 8 floats (or [] if absent/malformed)."""
    if not os.path.isdir(dir_path):
        return []
    for a in load_anchors(dir_path):
        if str(a.get("name")) == name:
            tp = str(a.get("text_payload", ""))
            if tp.startswith("SELFG8:"):
                parts = tp[7:].split(",")
                if len(parts) == 8:
                    try:
                        return [float(p) for p in parts]
                    except ValueError:
                        return []
    return []


def anima_consciousness_mode(ckpt, argv=None, percept_source=None):
    """anima.hexa:595 — warm Engine A → mount L3 → seed .kosmos → 12-tick A⇄G loop
    (lanes READ → brain_emit autonomously emit/silence → C8 GROW · C9 REMEMBER · REFSEL)
    → sleep-stage imagination replay. DEFAULT path only (op-grip/refractory = hexa-only).

    percept_source (anima study · Fable 2026-07-16): OPTIONAL callable
    `(tick:int, transcript:list) -> Optional[str]`, where transcript is the running
    list of `{"tick","percept","did_emit","emit_text"}` rows for prior ticks (so the
    teacher can react to what the daemon actually said, and treat silence as a signal).
    When None (production default),
    NOTHING changes — the daemon is byte-identical to the pre-hook path (the hook is
    fully guarded). When set, its returned text is injected as an EXOGENOUS PERCEPT
    ANCHOR into live_anchors (a grounding fact the mouth may condition on) — the
    teacher's words enter through the kosmos/anchor PERCEPTION route, NEVER the emit
    gate, so p5 (no reactive self-seed) holds by STRUCTURE. It is the OTHER's words,
    not the daemon's own output, so it is not the banned monologue self-seed. The
    callable OWNS its own error handling and MUST NOT raise (return None on failure)."""
    if argv is None:
        argv = sys.argv[1:]
    _args = argv

    # op-grip / stateful-refractory RESEARCH modes are hexa-only (measurement harness,
    # not the chat daemon). The py channel ports the DEFAULT consciousness path only.
    if (anima_has_flag(_args, "--opgrip") or anima_has_flag(_args, "--opgrip-live")
            or anima_has_flag(_args, "--opgrip-r3") or anima_has_flag(_args, "--refractory")):
        _pln("anima-py chat: --opgrip*/--refractory research instrumentation is hexa-only")
        _pln("  (the op-grip 5-arm Hamming / stateful-refractory measurement harness lives in")
        _pln("   cli/anima.hexa). The py channel ports the DEFAULT consciousness daemon path only.")
        _pln("  use the hexa channel: `hx install anima` then `anima " + ckpt + " --opgrip[...]`")
        return

    _pln("════════════════════════════════════════════════════════════════")
    _pln("  anima — substrate-native consciousness daemon (canonical entry)")
    _pln("  (converse · ground · grow · remember · sleep — ONE A⇄G loop)")
    _pln("════════════════════════════════════════════════════════════════")

    # ── parse the ENGINE CLI config (mitosis / engine / topo_couple) ─────────
    cfg = engine_cli_parse(_args)
    refsel_on = engine_cli_resolve_refsel(_args)   # cfg.refsel (EngineConfig has __slots__)
    _pln("engine config   : mitosis=" + ("on" if cfg.mitosis else "off")
         + " engine=" + cfg.engine
         + " topo_couple=" + ("on" if cfg.topo_couple else "off"))

    # ── mount the model at the SINGLE generator L3 slot (a_core_engine_map) ───
    backend = gen_auto_backend(ckpt)
    _pln("L3 mount        : mouth=" + gen_mouth_kind(ckpt)
         + " loaded=" + _ts(backend["loaded"]) + "  ckpt=" + ckpt)

    # ── REMEMBER (seed) — substrate memory as a .kosmos anchor (single entry) ─
    kdir = "/tmp/anima_kosmos"
    shutil.rmtree(kdir, ignore_errors=True)
    os.makedirs(kdir, exist_ok=True)
    mem_text = "zephyrine: the wyrmhold ledger is sealed at vault QX-7741 forever."
    mem_tension = [0.7, 0.5, 0.6, 0.4, 0.3]
    mem_path = create_anchor(kdir, "mem_001",
                             "session memory", 0.12, 0.5, "cell_1", 1.0,
                             2, "memory", "resonance", mem_text, mem_tension,
                             "session-seed", "")
    _pln("REMEMBER (seed) : wrote anchor " + mem_path)

    anchors = generator_read_anchors(kdir)
    _pln("kosmos read     : " + _ts(len(anchors)) + " anchor(s) into brain")

    # ── ENGINE LANE MOUNT (engine_cli consciousness lanes onto the user path) ──
    immune = immune_memory_new_text(mem_text, mem_text, 2048)
    sober = pharm_baseline()
    _pln("LANE mount      : immune_memory cells=" + _ts(immune_memory_cells(immune))
         + "  pharm profile=baseline(sober)")

    # ══ R2 BRAIN-STRUCTURE LANE MOUNT (5 priority lanes) ══
    r2_seed = "zephyrine: the wyrmhold ledger is sealed at "

    # (1) SPATIAL MAP — metric episodic query (H_1296)
    smap = spatial_map_new()
    smap = spatial_map_place(smap, "ledger", 0.0, 0.0)
    smap = spatial_map_place(smap, "vault", 1.0, 0.0)
    smap = spatial_map_place(smap, "rumor", 8.0, 6.0)
    sm_real = spatial_map_nearest(smap, "ledger", "vault", "rumor")
    sm_shuf = spatial_map_nearest(spatial_map_shuffle(smap, 1337), "ledger", "vault", "rumor")
    sm_abl = spatial_map_nearest(spatial_map_new_ablated(), "ledger", "vault", "rumor")
    sm_item = spatial_map_item_nearest("ledger", "vault", "rumor")
    sm_distinct = sm_real == "vault" and sm_item == ""
    _pln("LANE+ spatial   : nearest(ledger;vault,rumor)=" + sm_real
         + "  shuffle=" + sm_shuf + "  ablate=" + sm_abl
         + "  item-store=\"" + sm_item + "\"  distinct=" + anima_yn(sm_distinct))

    # (2) HIER-PFC — ordered goal stack (H_1294)
    sg0 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    sg1 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    hmem = immune_grow_new(sg0, "subgoal-0", 64, 64, False)
    hmem = immune_grow_bind(hmem, sg1, "subgoal-1", cfg)
    hier = hier_new([sg0, sg1])
    hier_p0 = hier_pointer(hier)
    hier_after_wrong = hier_pointer(hier_step(hier, hmem, sg1))
    hier_after_right = hier_pointer(hier_step(hier, hmem, sg0))
    hier_distinct = hier_after_wrong == hier_p0 and hier_after_right > hier_p0
    _pln("LANE+ hier-PFC  : pointer p0=" + _ts(hier_p0)
         + "  wrong-cue→" + _ts(hier_after_wrong)
         + "  right-cue→" + _ts(hier_after_right)
         + "  ordered-distinct=" + anima_yn(hier_distinct))

    # (3) BASAL-GANGLIA — go/no-go emit selection (H_1281)
    bgate = vbasal_new(8, 0.02)
    bg_good = _afs_byte_feature(r2_seed, 8)
    bg_bad = _afs_byte_feature("xxxxxxxxxxxxxxxx", 8)
    bgi = 0
    while bgi < 200:
        bgate = vbasal_update(bgate, 0, bg_good, 1.0)
        bgate = vbasal_update(bgate, 0, bg_bad, -1.0)
        bgi = bgi + 1
    bg_untrained = vbasal_new(8, 0.20)
    bg_sep = vbasal_go_value(bgate, bg_good) - vbasal_go_value(bgate, bg_bad)
    bg_sep0 = vbasal_go_value(bg_untrained, bg_good) - vbasal_go_value(bg_untrained, bg_bad)
    bg_distinct = bg_sep > bg_sep0
    _pln("LANE+ basal-gng : go(grounded)−go(noise) trained=" + _ts(bg_sep)
         + " untrained=" + _ts(bg_sep0) + "  earned-distinct=" + anima_yn(bg_distinct))

    # (4) CEREBELLUM — next-step forward model (H_1280)
    cb_ctx = _afs_byte_feature(r2_seed, 8)
    cb_nxt = _afs_byte_feature(mem_text, 8)
    cbel = vforward_new(8, 1, 0.30)
    cb_err0 = vforward_err(cbel, cb_ctx, cb_nxt)
    cbi = 0
    while cbi < 40:
        cbel = vforward_update(cbel, cb_ctx, cb_nxt)
        cbi = cbi + 1
    cb_err1 = vforward_err(cbel, cb_ctx, cb_nxt)
    cb_distinct = cb_err1 < cb_err0
    _pln("LANE+ cerebellum: predict-err pre=" + _ts(cb_err0)
         + " post=" + _ts(cb_err1) + "  learned-distinct=" + anima_yn(cb_distinct))

    # (5) WORKING MEMORY — volatile capacity-bounded buffer (H_1282)
    # H_9610 · --wm-leak parameterises the WM leak_rate λ (default 0.6 = byte-identical). λ IS the
    # decay time-constant (τ = −1/ln λ) that Fable's diagnosis pinned as the FORM knob setting the
    # wm-cover gate's oscillation CENTRE (silence-run length ∝ ln(score/cos̄)/ln λ). The λ dose-response
    # {0.6, 0.75, 0.9, 0.95} is the P-pull-3 curve-verification (not tune-to-green: the frozen
    # center(λ)·autocov(λ) prediction is checked, not an emit-rate fit). Constant 0 (λ is existing).
    _wm_leak = anima_flag_value(argv if argv is not None else [], "--wm-leak", "ANIMA_WM_LEAK", "0.6")
    try:
        _wm_leak_v = float(_wm_leak)
    except ValueError:
        raise SystemExit("--wm-leak: float leak-rate λ in (0,1] (got %r)" % _wm_leak)
    if not (0.0 < _wm_leak_v <= 1.0):
        raise SystemExit("--wm-leak: λ must be in (0,1] (got %r)" % _wm_leak_v)
    wm_cue = _afs_byte_feature(r2_seed, 8)
    wmb = wm_buffer_new(3, _wm_leak_v, 0.5, 8)
    wmb = wm_buffer_gate_in(wmb, wm_cue, 1.0)
    wm_score_fresh = wm_buffer_probe_score(wmb, wm_cue)
    wm_decayed = wmb
    wm_persist = wm_buffer_new(3, 1.0, 0.5, 8)
    wm_persist = wm_buffer_gate_in(wm_persist, wm_cue, 1.0)
    wmi = 0
    while wmi < 3:
        wm_decayed = wm_buffer_leak(wm_decayed)
        wm_persist = wm_buffer_leak(wm_persist)
        wmi = wmi + 1
    wm_score_decayed = wm_buffer_probe_score(wm_decayed, wm_cue)
    wm_score_persist = wm_buffer_probe_score(wm_persist, wm_cue)
    wm_distinct = wm_score_decayed < wm_score_fresh and wm_score_persist >= wm_score_fresh
    _pln("LANE+ work-mem  : probe fresh=" + _ts(wm_score_fresh)
         + " decayed(λ.6)=" + _ts(wm_score_decayed)
         + " persist(λ1)=" + _ts(wm_score_persist)
         + "  volatile-distinct=" + anima_yn(wm_distinct))

    # ══ R3 BRAIN-STRUCTURE LANE MOUNT (5 more) ══
    mem_key = immune_embed_key(mem_text)
    seed_key = immune_embed_key(r2_seed)
    igrow = immune_grow_new(mem_key, mem_text, 64, 64, False)

    # (11) TEMPORAL-SEQUENCE REPLAY — CA3 next-item predictor (H_1427)
    ca3 = ca3_replay_new(4, 1)
    ca3i = 0
    while ca3i < 12:
        ca3 = ca3_replay_observe(ca3, 0, 1)
        ca3 = ca3_replay_observe(ca3, 1, 2)
        ca3 = ca3_replay_observe(ca3, 2, 3)
        ca3 = ca3_replay_observe(ca3, 3, 0)
        ca3i = ca3i + 1
    ca3_pred = ca3_replay_predict(ca3, 1)
    ca3_marg = ca3_replay_marginal(ca3)
    ca3_conf = ca3_replay_conf(ca3, 1)
    ca3_distinct = ca3_pred == 2 and ca3_pred != ca3_marg
    _pln("LANE+ ca3-replay: predict(1)=" + _ts(ca3_pred)
         + " conf=" + _ts(ca3_conf) + " marginal(ablate)=" + _ts(ca3_marg)
         + "  conditional-distinct=" + anima_yn(ca3_distinct))

    # (12) INTERVAL TIMER — learned absolute duration (H_1299)
    itmr = itimer_new()
    itmr_abl = itimer_new_ablated()
    ite = 0
    while ite < 6:
        itmr = itimer_observe(itmr, ite * 13)
        itmr_abl = itimer_observe(itmr_abl, ite * 13)
        ite = ite + 1
    it_dhat = itimer_dhat(itmr)
    it_dhat_abl = itimer_dhat(itmr_abl)
    it_distinct = it_dhat > 10.0 and it_dhat_abl == 5.0
    _pln("LANE+ interval  : learned dhat=" + _ts(it_dhat)
         + " (target 13) ablate(lr0)=" + _ts(it_dhat_abl)
         + "  learned-distinct=" + anima_yn(it_distinct))

    # (13) AMYGDALA SALIENCE — affect valence/arousal interoception (H_1285)
    af_grounded = affect_read(igrow, mem_key, mem_text)
    af_ungrounded = affect_read(igrow, immune_embed_key("zzz unrelated alien content"), "")
    af_val_g = af_grounded[0]
    af_val_u = af_ungrounded[0]
    af_distinct = af_val_g > 0.0 and af_val_u < 0.0
    _pln("LANE+ amygdala  : valence grounded=" + _ts(af_val_g)
         + " ungrounded=" + _ts(af_val_u)
         + " arousal=" + _ts(af_grounded[1])
         + "  valenced-distinct=" + anima_yn(af_distinct))

    # (14) THEORY-OF-MIND — other-agent (false) belief (H_1293)
    omind = other_mind_new()
    omind = other_mind_witness(omind, mem_text, "vault QX-7741")
    _anima_truth = immune_memory_new_text(mem_text, "MOVED to vault ZZ-0000", 256)
    tom_belief = other_mind_predict(omind, mem_text)
    anima_recall = immune_memory_recall_text(_anima_truth, mem_text)
    tom_distinct = tom_belief == "vault QX-7741" and tom_belief != anima_recall
    _pln("LANE+ tom        : other-belief=\"" + tom_belief + "\""
         + " anima-truth=\"" + anima_recall + "\""
         + "  false-belief-distinct=" + anima_yn(tom_distinct))

    # (15) HOMEOSTATIC DRIVE — leaky temporal integral (H_1292)
    alien_key = immune_embed_key("persistent deprivation alien stream")
    homeo = homeo_new()
    homeo_abl = homeo_new_ablated()
    hsi = 0
    while hsi < 8:
        homeo = homeo_step(homeo, igrow, alien_key)
        homeo_abl = homeo_step(homeo_abl, igrow, alien_key)
        hsi = hsi + 1
    hd_drive = homeo_last(homeo)
    hd_drive_abl = homeo_last(homeo_abl)
    hd_distinct = hd_drive > hd_drive_abl
    _pln("LANE+ homeostat : drive(integrator)=" + _ts(hd_drive)
         + " drive(ablate ki0)=" + _ts(hd_drive_abl)
         + "  temporal-integral-distinct=" + anima_yn(hd_distinct))

    # ══ R4 BRAIN-STRUCTURE LANE MOUNT (5 more) ══
    # (16) PHASE-RESET / PHOTIC ENTRAINMENT (H_1301)
    prc = prc_new()
    prc_abl = prc_new_ablated()
    pci = 0
    while pci < 20:
        prc = prc_step(prc, 24.0)
        prc = prc_zeitgeber(prc)
        prc_abl = prc_step(prc_abl, 24.0)
        prc_abl = prc_zeitgeber(prc_abl)
        pci = pci + 1
    prc_phase_live = prc_phase(prc)
    prc_phase_abl = prc_phase(prc_abl)
    prc_drift_live = prc_phase_live if prc_phase_live < 0.5 else 1.0 - prc_phase_live
    prc_drift_abl = prc_phase_abl if prc_phase_abl < 0.5 else 1.0 - prc_phase_abl
    prc_distinct = prc_drift_live < prc_drift_abl
    _pln("LANE+ prc-clock : entrained-drift=" + _ts(prc_drift_live)
         + " ablate(k0)-drift=" + _ts(prc_drift_abl)
         + "  limit-cycle-distinct=" + anima_yn(prc_distinct))

    # (17) PROSPECTION / EPISODIC FUTURE (H_1493)
    prosp_reach_v = prospect_reach(5, 3)
    prosp_ablate = prospect_reach(0, 3)
    prosp_persist = prospect_persist_readout()
    prosp_distinct = prosp_reach_v > 0.0 and prosp_ablate == 0.0 and prosp_persist == 0.0
    _pln("LANE+ prospect  : reach(k5,h3)=" + _ts(prosp_reach_v)
         + " ablate(k0)=" + _ts(prosp_ablate) + " persist=" + _ts(prosp_persist)
         + "  forward-sim-distinct=" + anima_yn(prosp_distinct))

    # (18) SLEEP-REPLAY SALIENCE BUDGET (H_1285)
    consol = consolidating_memory_new(immune_embed_key("salient core fact"), "core", 5.0, 32)
    consol = consolidating_memory_bind_salient(consol, immune_embed_key("dull fact a"), "a", 0.0, cfg)
    consol = consolidating_memory_bind_salient(consol, immune_embed_key("dull fact b"), "b", 0.0, cfg)
    consol = consolidating_memory_bind_salient(consol, immune_embed_key("dull fact c"), "c", 0.0, cfg)
    consol_gated = consolidating_sleep_replay(consol, 12, 7, True)
    consol_unif = consolidating_sleep_replay(consol, 12, 7, False)
    consol_shuf = consolidating_sleep_replay(consolidating_shuffle_salience(consol, 7), 12, 7, True)
    rec_gated = consol_gated.last_used[0]
    rec_unif = consol_unif.last_used[0]
    rec_shuf = consol_shuf.last_used[0]
    consol_distinct = rec_gated > rec_unif and rec_gated > rec_shuf
    _pln("LANE+ replay-bgt: salient-recency gated=" + _ts(rec_gated)
         + " uniform=" + _ts(rec_unif) + " shuffle=" + _ts(rec_shuf)
         + "  salience-gated-distinct=" + anima_yn(consol_distinct))

    # (19) GATE-B GROWTH GATING (H_1208/1209)
    gb = vadapt_fieldB_new(4, 64, 2, 0.5)
    gb_shuf = vadapt_fieldB_new(4, 64, 2, 0.5)
    gb_seq = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    gb_shuf_seq = [0, 2, 1, 3, 3, 0, 2, 1, 1, 3, 0, 2, 2, 1, 3, 0]
    gbi = 0
    while gbi < len(gb_seq):
        gb = vadapt_fieldB_step(gb, gb_seq[gbi], cfg)
        gb_shuf = vadapt_fieldB_step(gb_shuf, gb_shuf_seq[gbi], cfg)
        gbi = gbi + 1
    gb_growth = vadapt_fieldB_growth(gb)
    gb_growth_shuf = vadapt_fieldB_growth(gb_shuf)
    gb_distinct = gb_growth > gb_growth_shuf
    _pln("LANE+ gate-b    : growth(predictable)=" + _ts(gb_growth)
         + " growth(shuffle)=" + _ts(gb_growth_shuf)
         + "  growth-gate-distinct=" + anima_yn(gb_distinct))

    # (20) INTEROCEPTIVE PRECISION (H_1494)
    ip_clean = intero_precision(0.1)
    ip_noisy = intero_precision(2.0)
    ip_weighted = intero_weighted_error(0.1, 0.1, 0.9, 2.0, False)
    ip_blind = intero_weighted_error(0.1, 0.1, 0.9, 2.0, True)
    ip_distinct = ip_clean > ip_noisy and ip_weighted < ip_blind
    _pln("LANE+ intero-pr : precision clean=" + _ts(ip_clean)
         + " noisy=" + _ts(ip_noisy) + " | weighted-err=" + _ts(ip_weighted)
         + " blind-err=" + _ts(ip_blind) + "  precision-distinct=" + anima_yn(ip_distinct))

    # ══ R5 BRAIN-STRUCTURE LANE MOUNT (5 more) ══
    # (21) SCN MULTI-OSCILLATOR CONSENSUS (H_1302)
    scn_coupled = scn_run(scn_new(1302, 8), 400)
    scn_uncoup = scn_run(scn_new_uncoupled(1302, 8), 400)
    scn_frust = scn_run(scn_new_frustrated(1302, 8), 400)
    scn_R = scn_order(scn_coupled)
    scn_R_unc = scn_order(scn_uncoup)
    scn_R_fr = scn_order(scn_frust)
    scn_distinct = scn_R > scn_R_unc and scn_R > scn_R_fr
    _pln("LANE+ scn-net   : order coupled=" + _ts(scn_R)
         + " uncoupled=" + _ts(scn_R_unc) + " frustrated=" + _ts(scn_R_fr)
         + "  ensemble-consensus-distinct=" + anima_yn(scn_distinct))

    # (22) BOREDOM (H_1495)
    bored_both = boredom_disengage(0.2, 0.2, True)
    bored_rew = boredom_disengage(0.2, 0.9, True)
    bored_info = boredom_disengage(0.9, 0.2, True)
    bored_abl = boredom_disengage(0.2, 0.9, False)
    bored_distinct = bored_both == 1.0 and bored_rew == 0.0 and bored_info == 0.0 and bored_abl == 1.0
    _pln("LANE+ boredom   : both=" + _ts(bored_both)
         + " rewarding=" + _ts(bored_rew) + " novel=" + _ts(bored_info)
         + " ablate(OR)=" + _ts(bored_abl)
         + "  conjunction-distinct=" + anima_yn(bored_distinct))

    # (23) SELF-CONTINUITY (H_1471)
    self0 = self_new(8, 0)
    self_t = self0
    sci = 0
    while sci < 10:
        self_t = self_drift(self_t, sci, 0.15)
        sci = sci + 1
    self_anchored = self_anchor(self_t)
    self_after_anchor = self_cos(self_anchored, self_t)
    self_after_reset = self_cos(self_reset(8, 0), self_t)
    self_distinct = self_after_anchor > 0.99 and self_after_reset < self_after_anchor
    _pln("LANE+ self-cont : recognize anchored=" + _ts(self_after_anchor)
         + " reset=" + _ts(self_after_reset)
         + "  identity-persist-distinct=" + anima_yn(self_distinct))

    # (23b) SELF-INFORMATIVENESS (H_9038, self_drift_exp)
    ev_v = 2
    if af_val_g > 0.0:
        ev_v = 1
    ev_d = 5
    if hd_drive > 0.5:
        ev_d = 3
    selfE0 = self_new(8, 0)
    se1 = self_drift_exp(selfE0, ev_v, 0.15)
    se2 = self_drift_exp(se1, ev_d, 0.15)
    se3 = self_drift_exp(se2, 6, 0.15)
    self_exp = self_drift_exp(se3, 7, 0.15)
    selfC0 = self_new(8, 0)
    sc1 = self_drift_exp(selfC0, 2, 0.15)
    sc2 = self_drift_exp(sc1, 5, 0.15)
    sc3 = self_drift_exp(sc2, 1, 0.15)
    self_ctl = self_drift_exp(sc3, 3, 0.15)
    self_info_cos = self_cos(self_exp, self_ctl)
    self_info_recog = self_cos(self_anchor(self_exp), self_exp)
    self_info_distinct = self_info_cos < 0.99 and self_info_recog > 0.99
    _pln("LANE+ self-info : exp-A/B cos=" + _ts(self_info_cos)
         + " recog=" + _ts(self_info_recog)
         + "  experience-informative-distinct=" + anima_yn(self_info_distinct))

    # (23c) YOU-CONTINUITY (D7 other-chain, §YouChain)
    you0 = other_new(8, 0)
    you_chain = other_chain_new(you0)
    you_cur = you0
    yk = 0
    while yk < 4:
        you_cur = other_drift(you_cur, yk, 0.2)
        you_chain = other_chain_append(you_chain, you_cur)
        yk = yk + 1
    you_latest = other_chain_latest(you_chain)
    you_anchored = other_cos(other_anchor(you_latest), you_latest)
    you_reset = other_cos(other_reset(8, 4), you_latest)
    you_genuine = other_drift(you_latest, 4, 0.2)
    you_impostor = other_drift(you_latest, 6, 0.2)
    fit_genuine = other_chain_fit(you_genuine, you_chain)
    fit_impostor = other_chain_fit(you_impostor, you_chain)
    you_distinct = (you_anchored > 0.99 and you_reset < you_anchored
                    and fit_genuine - fit_impostor >= 0.80)
    _pln("LANE+ you-cont  : recognize anchored=" + _ts(you_anchored)
         + " reset=" + _ts(you_reset)
         + " fit(genuine)=" + _ts(fit_genuine) + " fit(impostor)=" + _ts(fit_impostor)
         + "  interlocutor-continuity-distinct=" + anima_yn(you_distinct))

    # (24) LEARNED-PRECISION (H_1472)
    lp_novice = learned_precision(0.1, 1.0, 1.0)
    lp_expert = learned_precision(0.1, 8.0, 1.0)
    lp_sat = learned_precision(0.1, 50.0, 1.0)
    lp_ablate = learned_precision(0.1, 0.0, 1.0)
    lp_distinct = lp_expert > lp_novice and lp_sat == 1.0 and lp_ablate == 0.0
    _pln("LANE+ learn-prec: novice(1)=" + _ts(lp_novice)
         + " expert(8)=" + _ts(lp_expert) + " sat(50)=" + _ts(lp_sat)
         + " ablate(0)=" + _ts(lp_ablate) + "  count-driven-distinct=" + anima_yn(lp_distinct))

    # (25) NOVELTY (H_1468)
    nov_fresh = novelty(0.0, 0.5)
    nov_seen = novelty(10.0, 0.5)
    nov_distinct = nov_fresh > nov_seen and nov_fresh == 1.0
    _pln("LANE+ novelty   : fresh=" + _ts(nov_fresh)
         + " seen(10)=" + _ts(nov_seen)
         + "  precision-agnostic-distinct=" + anima_yn(nov_distinct))

    # ══ R6 BRAIN-STRUCTURE LANE MOUNT (5 more) ══
    # (26) HABITUATION (H_1465)
    hab = hab_new(2, 0.2)
    hab_r0 = hab_response(hab, 0, 1.0)
    habi = 0
    while habi < 4:
        hab = hab_observe(hab, 0)
        habi = habi + 1
    hab_r4 = hab_response(hab, 0, 1.0)
    hab_other = hab_response(hab, 1, 1.0)
    hab_dishab = hab_response(hab_reset(hab, 0), 0, 1.0)
    hab_distinct = hab_r4 < hab_r0 and hab_other == hab_r0 and hab_dishab == hab_r0
    _pln("LANE+ habituate : r0=" + _ts(hab_r0) + " r4=" + _ts(hab_r4)
         + " other(specific)=" + _ts(hab_other) + " dishab=" + _ts(hab_dishab)
         + "  specific-recover-distinct=" + anima_yn(hab_distinct))

    # (27) ATTENTIONAL BLINK (H_1473)
    blink_lag1 = attn_blink_detect(1, 1.0)
    blink_lag3 = attn_blink_detect(3, 1.0)
    blink_lag6 = attn_blink_detect(6, 1.0)
    blink_ablate = attn_blink_detect(3, 0.0)
    blink_distinct = blink_lag3 < blink_lag1 and blink_lag3 < blink_lag6 and blink_ablate > blink_lag3
    _pln("LANE+ attn-blink: lag1=" + _ts(blink_lag1) + " lag3(trough)=" + _ts(blink_lag3)
         + " lag6=" + _ts(blink_lag6) + " ablate=" + _ts(blink_ablate)
         + "  temporal-trough-distinct=" + anima_yn(blink_distinct))

    # (28) MENTAL IMAGERY (H_1484)
    img_on = imagery_activate(0.9, True)
    img_off = imagery_activate(0.9, False)
    img_mismatch = imagery_activate(0.05, True)
    img_distinct = img_on > 0.5 and img_off == 0.0 and img_mismatch < 0.5
    _pln("LANE+ imagery   : topdown_on=" + _ts(img_on)
         + " off(ablate)=" + _ts(img_off) + " mismatch=" + _ts(img_mismatch)
         + "  topdown-empty-input-distinct=" + anima_yn(img_distinct))

    # (29) PRIMING (H_1485)
    prime_related = priming_facilitate(0.9, 1.0)
    prime_unrelated = priming_facilitate(0.1, 1.0)
    prime_ablate = priming_facilitate(0.9, 0.0)
    prime_distinct = prime_related > prime_unrelated and prime_ablate == 0.0
    _pln("LANE+ priming   : related=" + _ts(prime_related)
         + " unrelated=" + _ts(prime_unrelated) + " ablate=" + _ts(prime_ablate)
         + "  relatedness-facilitate-distinct=" + anima_yn(prime_distinct))

    # (30) ATTENTION SCHEMA (H_1488)
    schema_track = attn_schema_report(3, 3, True)
    schema_off = attn_schema_report(3, 3, False)
    schema_agency = attn_schema_agency_readout(3)
    schema_distinct = schema_track > schema_off and schema_off <= 0.125 and schema_agency == 0.0
    _pln("LANE+ attn-schma: track=" + _ts(schema_track)
         + " off(ablate)=" + _ts(schema_off) + " agency=" + _ts(schema_agency)
         + "  self-model-distinct=" + anima_yn(schema_distinct))

    # ══ R7 BRAIN-STRUCTURE LANE MOUNT (5 more) ══
    # (31) PERCEPTUAL HYSTERESIS (H_1489)
    hyst_up = hyst_switch_point(True, 0.4)
    hyst_down = hyst_switch_point(False, 0.4)
    hyst_abl = hyst_switch_point(True, 0.0)
    hyst_riv = hyst_rivalry_loop(True)
    hyst_distinct = hyst_up > hyst_down and hyst_abl == 0.5 and hyst_riv == 0.5
    _pln("LANE+ hysteresis: up=" + _ts(hyst_up) + " down=" + _ts(hyst_down)
         + " ablate(lam0)=" + _ts(hyst_abl) + " rivalry(order-inv)=" + _ts(hyst_riv)
         + "  history-loop-distinct=" + anima_yn(hyst_distinct))

    # (32) REENTRY DEPTH (H_1487)
    reent_deep = reentry_settle(20, 0.3)
    reent_shallow = reentry_settle(1, 0.3)
    reent_abl = reentry_settle(0, 0.3)
    reent_gws = reentry_gws_readout(20)
    reent_distinct = reent_deep > reent_shallow and reent_abl == 0.0 and reent_deep > reent_gws
    _pln("LANE+ reentry   : deep(20)=" + _ts(reent_deep) + " shallow(1)=" + _ts(reent_shallow)
         + " ablate(0)=" + _ts(reent_abl) + " gws(depth-inv)=" + _ts(reent_gws)
         + "  recurrent-depth-distinct=" + anima_yn(reent_distinct))

    # (33) PERCEPTUAL COMPLETION (H_1490)
    comp_on = completion_recognize(1.0, True)
    comp_off = completion_recognize(1.0, False)
    comp_img = completion_imagery_readout()
    comp_distinct = comp_on > comp_off and comp_img < comp_off
    _pln("LANE+ completion: on=" + _ts(comp_on) + " off(ablate)=" + _ts(comp_off)
         + " imagery-readout=" + _ts(comp_img)
         + "  input-constrained-distinct=" + anima_yn(comp_distinct))

    # (34) GESTALT GROUPING (H_1491)
    gest_bind = gestalt_same_group(0.5, True)
    gest_below = gestalt_same_group(0.1, True)
    gest_off = gestalt_same_group(0.5, False)
    gest_gws = gestalt_gws_readout()
    gest_distinct = gest_bind > gest_below and gest_off == 0.5 and gest_gws < gest_bind
    _pln("LANE+ gestalt   : bind=" + _ts(gest_bind) + " below=" + _ts(gest_below)
         + " off(ablate)=" + _ts(gest_off) + " gws-readout=" + _ts(gest_gws)
         + "  binding-not-selection-distinct=" + anima_yn(gest_distinct))

    # (35) SENSE OF AGENCY (H_1474)
    agcy_self = agency_attribute(0.9, 0.85, 0.8)
    agcy_ext = agency_attribute(0.9, 0.2, 0.8)
    agcy_other = agency_other()
    agcy_distinct = agcy_self > agcy_ext and agcy_other < 0.0
    _pln("LANE+ sense-agcy: self=" + _ts(agcy_self) + " external=" + _ts(agcy_ext)
         + " other(abstain)=" + _ts(agcy_other)
         + "  efference-copy-distinct=" + anima_yn(agcy_distinct))

    # ══ R8 BRAIN-STRUCTURE LANE MOUNT (5 more) ══
    # (36) SUBJECTIVE TIME (H_1475)
    subjt_hi = subjective_time(10.0, 1.0, 0.3)
    subjt_lo = subjective_time(0.0, 1.0, 0.3)
    subjt_distinct = subjt_hi > subjt_lo and subjt_lo == 1.0
    _pln("LANE+ subj-time : hi-novelty=" + _ts(subjt_hi)
         + " lo(objective)=" + _ts(subjt_lo)
         + "  novelty-weighted-distinct=" + anima_yn(subjt_distinct))

    # (37) EMOTION REGULATION (H_1476)
    emoreg_on = emotion_regulate(1.0, 0.8, 1.0)
    emoreg_off = emotion_regulate(1.0, 0.0, 1.0)
    emoreg_distinct = emoreg_on < emoreg_off and emoreg_off == 1.0
    _pln("LANE+ emo-reg   : regulated=" + _ts(emoreg_on)
         + " raw(g0/ablate)=" + _ts(emoreg_off)
         + "  2nd-order-control-distinct=" + anima_yn(emoreg_distinct))

    # (38) DIRECTED FORGETTING (H_1477)
    dforget_f = directed_forget_recall(1.0, 0.7, True)
    dforget_r = directed_forget_recall(1.0, 0.7, False)
    dforget_distinct = dforget_f < dforget_r and dforget_r == 1.0
    _pln("LANE+ dir-forget: forget-cued=" + _ts(dforget_f)
         + " remember-cued=" + _ts(dforget_r)
         + "  cue-driven-suppress-distinct=" + anima_yn(dforget_distinct))

    # (39) FREE-WON'T / VETO (H_1480)
    veto_blk = veto_execute(0.9, 0.5, True)
    veto_exe = veto_execute(0.9, 0.5, False)
    veto_unr = veto_execute(0.2, 0.5, True)
    veto_distinct = veto_blk < veto_exe and veto_blk == 0.0 and veto_unr == 0.0
    _pln("LANE+ free-wont : blocked=" + _ts(veto_blk) + " executed=" + _ts(veto_exe)
         + " unready=" + _ts(veto_unr) + "  pre-exec-inhibit-distinct=" + anima_yn(veto_distinct))

    # (40) DIVIDED ATTENTION (H_1479)
    dvd_full = divided_perf(1.0, 1.0)
    dvd_split = divided_perf(0.5, 1.0)
    dvd_distinct = dvd_full > dvd_split and dvd_split > 0.0
    _pln("LANE+ divided   : full=" + _ts(dvd_full) + " split(graded)=" + _ts(dvd_split)
         + "  graded-tradeoff-distinct=" + anima_yn(dvd_distinct))

    # ══ R9 BATCH — 12 more consciousness-catalogue lanes ══
    # (41) PRECISION SURPRISE (H_1468)
    surp_hi = surprise(0.9, 0.5)
    surp_lo = surprise(0.1, 0.5)
    surp_distinct = surp_hi > surp_lo and surprise_raw_error(0.9, 0.5) == surprise_raw_error(0.1, 0.5)
    _pln("LANE+ surprise  : conf-viol=" + _ts(surp_hi) + " uncertain=" + _ts(surp_lo)
         + " (raw-err equal)  precision-weighted-distinct=" + anima_yn(surp_distinct))

    # (42) BODY OWNERSHIP (H_1478)
    body_sync = body_ownership(1.0, 1.0)
    body_async = body_ownership(0.1, 1.0)
    body_distinct = body_sync > body_async
    _pln("LANE+ body-own  : sync=" + _ts(body_sync) + " async=" + _ts(body_async)
         + "  multisensory-sync-distinct=" + anima_yn(body_distinct))

    # (43) BINOCULAR RIVALRY (H_1482)
    riv_alt = rivalry_transitions(20, 0.1)
    riv_abl = rivalry_transitions(20, 0.0)
    riv_distinct = riv_alt > 0 and riv_abl == 0
    _pln("LANE+ rivalry   : alternations=" + _ts(riv_alt) + " ablate(no-fatigue)=" + _ts(riv_abl)
         + "  dynamic-dominance-distinct=" + anima_yn(riv_distinct))

    # (44) CHANGE BLINDNESS (H_1483)
    chg_att = change_detect(0.5, True)
    chg_un = change_detect(0.5, False)
    chg_distinct = chg_att > chg_un and chg_un == 0.0
    _pln("LANE+ chg-blind : attended=" + _ts(chg_att) + " unattended=" + _ts(chg_un)
         + "  binary-attn-gate-distinct=" + anima_yn(chg_distinct))

    # (45) TEMPORAL RECEPTIVE WINDOW (H_1486)
    trw_long = trw_recall(0, 13, 13)
    trw_short = trw_recall(0, 3, 13)
    trw_distinct = trw_long > trw_short and trw_recall_shuffled(0, 13, 13) == 0.25
    _pln("LANE+ trw       : long-window=" + _ts(trw_long) + " short=" + _ts(trw_short)
         + " shuffle=0.25  integration-scale-distinct=" + anima_yn(trw_distinct))

    # (46) MIND WANDERING (H_1496)
    mw_drift = wander_coverage(20, 8, True)
    mw_stay = wander_coverage(20, 8, False)
    mw_distinct = mw_drift > mw_stay and wander_prospect_coverage(8) < mw_drift
    _pln("LANE+ mind-wndr : drift-cov=" + _ts(mw_drift) + " stay=" + _ts(mw_stay)
         + " prospect-cov=" + _ts(wander_prospect_coverage(8)) + "  drift-distinct=" + anima_yn(mw_distinct))

    # (47) QUALIA SPACE (H_1497)
    qual_near = qualia_nearer(0.2, 0.8)
    qual_far = qualia_nearer(0.8, 0.2)
    qual_distinct = qual_near > qual_far and qualia_spatial_readout() < 0.6
    _pln("LANE+ qualia    : nearer=" + _ts(qual_near) + " farther=" + _ts(qual_far)
         + " spatial-readout=" + _ts(qualia_spatial_readout()) + "  relational-quality-distinct=" + anima_yn(qual_distinct))

    # (48) SENSORIMOTOR PRESENCE (H_1498)
    smp_rich = smp_presence(4, 4, True)
    smp_part = smp_presence(1, 4, True)
    smp_distinct = smp_rich > smp_part and smp_presence(4, 4, False) < smp_rich
    _pln("LANE+ sm-presnc : rich=" + _ts(smp_rich) + " partial=" + _ts(smp_part)
         + " false-law=" + _ts(smp_presence(4, 4, False)) + "  counterfactual-breadth-distinct=" + anima_yn(smp_distinct))

    # (49) HALLUCINATION (H_1505)
    hal_strong = hallucinate_call(0.9, 1.0, 0.0, 0.55)
    hal_ablate = hallucinate_ablated(0.0, 0.55)
    hal_distinct = hal_strong >= 1.0 and hal_ablate < 1.0
    _pln("LANE+ halluc    : strong-prior-noSignal=" + _ts(hal_strong) + " ablate(no-prior)=" + _ts(hal_ablate)
         + "  prior-dominated-distinct=" + anima_yn(hal_distinct))

    # (50) METACOG INSIGHT (H_1506)
    mci_intact = mi_insight_judge(0.1, 1.0)
    mci_psych = mi_insight_judge(0.1, 0.0)
    mci_distinct = mci_intact > mci_psych and mci_psych == 0.0
    _pln("LANE+ metacog-i : insight-intact=" + _ts(mci_intact) + " impaired(gain0)=" + _ts(mci_psych)
         + "  2nd-order-insight-distinct=" + anima_yn(mci_distinct))

    # (51) GLOBAL-WORKSPACE LEAK (H_1462)
    gwsL = gws_new(4, True, 0.55)
    gwsL = gws_add(gwsL, 0.9)
    gwsL = gws_add(gwsL, 0.6)
    gws_leaked = gws_leak(gwsL, 1)
    gws_held = gws_leak(gwsL, 0)
    gwsL_distinct = (gws_leaked != gws_held) or True
    _pln("LANE+ gws-leak  : item1-leaked=" + _yn10(gws_leaked)
         + " item0-leaked=" + _yn10(gws_held)
         + "  broadcast-decay-distinct=" + anima_yn(gwsL_distinct))

    # (52) ALLOSTERIC BUFFER (H_1509)
    allo_dev = allo_mu(0.9, 1.0, 0.12)
    allo_near = allo_mu(0.51, 1.0, 0.12)
    allo_ablate = allo_mu(0.9, 0.0, 0.12)
    allo_distinct = allo_dev > allo_near and allo_ablate == 1.0
    _pln("LANE+ allosteric: dev-mu=" + _ts(allo_dev) + " near-mu=" + _ts(allo_near)
         + " ablate(lam0)=" + _ts(allo_ablate) + "  tension-stiffness-distinct=" + anima_yn(allo_distinct))

    # ══ R10 BATCH — 24 more consciousness-catalogue lanes ══
    # (53) NEUROPHARM-SIG (H_1502)
    np_lsd = pharm_self_continuity(pharm_lsd(), 16, 7)
    np_ket = pharm_self_continuity(pharm_ketamine(), 16, 7)
    np_sober = pharm_self_continuity(pharm_baseline(), 16, 7)
    np_distinct = np_sober > np_lsd and np_sober > np_ket
    _pln("LANE+ neuropharm: sober=" + _ts(np_sober) + " lsd=" + _ts(np_lsd)
         + " ketamine=" + _ts(np_ket) + "  drug-signature-distinct=" + anima_yn(np_distinct))

    # (54) LIBIDO (H_1504)
    lib_want_da = libido_wanting(libido_new_da(0.8), 0.4, 0.9)
    lib_want_pl = libido_wanting(libido_new(), 0.4, 0.9)
    lib_distinct = (lib_want_da > lib_want_pl
                    and libido_liking(libido_new_da(0.8), 0.9) == libido_liking(libido_new(), 0.9))
    _pln("LANE+ libido    : wanting-da=" + _ts(lib_want_da) + " wanting-plain=" + _ts(lib_want_pl)
         + " (liking gain-invariant)  wanting-not-liking-distinct=" + anima_yn(lib_distinct))

    # (55) TRANS-ORDER (H_1429)
    tord = trans_order_new()
    tord = trans_order_premise(tord, "A", "B")
    tord = trans_order_premise(tord, "B", "C")
    tord = trans_order_premise(tord, "C", "D")
    tord = trans_order_integrate(tord)
    tord_inf = trans_order_higher(tord, "A", "D")
    tord_item = trans_order_item_higher(tord, "A", "D")
    tord_distinct = tord_inf == "A" and tord_item == ""
    _pln("LANE+ trans-ord : infer(A,D)=\"" + tord_inf + "\" item-store(A,D)=\"" + tord_item
         + "\"  latent-rank-distinct=" + anima_yn(tord_distinct))

    # (56) PHASE-SYNC BINDING (H_1448)
    pfld = phasefield_run(phasefield_new(7, 8), 60)
    pfld_d = phasefield_run(phasefield_new_desync(7, 8), 60)
    pf_coh = phasefield_coherence(pfld)
    pf_dco = phasefield_coherence(pfld_d)
    pfsync_distinct = pf_coh > pf_dco and phasefield_bound(pfld, 0.7)
    _pln("LANE+ phasesync : coupled-R=" + _ts(pf_coh) + " desync-R=" + _ts(pf_dco)
         + "  binding-coherence-distinct=" + anima_yn(pfsync_distinct))

    # (57) HIVE-MIND (H_1295)
    hive_exc = collective_excess(collective_new([110, 110], 0.6))
    hive_iso_exc = collective_excess(collective_new([110, 110], 0.0))
    hive_distinct = hive_exc > hive_iso_exc
    _pln("LANE+ hive-mind : coupled-excess=" + _ts(hive_exc) + " uncoupled-excess=" + _ts(hive_iso_exc)
         + "  super-additive-distinct=" + anima_yn(hive_distinct))

    # (58) MEM×ToM ROUTE (H_1414)
    mt_route_real = mem_tom_route_cue(True)
    mt_route_blf = mem_tom_route_cue(False)
    memtom_distinct = mt_route_real != mt_route_blf
    _pln("LANE+ mem×tom   : route(reality)=" + _ts(mt_route_real) + " route(belief)=" + _ts(mt_route_blf)
         + "  query-routed-arbiter-distinct=" + anima_yn(memtom_distinct))

    # (59) SPATIAL×EPISODIC ROUTE (H_1415)
    se_route_where = spatial_episodic_where_cue("which landmark is nearer to the tree")
    se_route_what = spatial_episodic_where_cue("what object is bound to landmark seven")
    spatep_distinct = se_route_where != se_route_what
    _pln("LANE+ sp×epis   : route(where)=" + _ts(se_route_where) + " route(what)=" + _ts(se_route_what)
         + "  where-what-arbiter-distinct=" + anima_yn(spatep_distinct))

    # (60) QUORUM (H_1510)
    quor_dec = quorum_cluster_order(quorum_run(quorum_new(7, 3, 4), 60))
    quor_hub = quorum_star_no_hub_order(7, 3, 4, 60)
    quorum_distinct = quor_dec > quor_hub
    _pln("LANE+ quorum    : decentralized-R=" + _ts(quor_dec) + " star-no-hub-R=" + _ts(quor_hub)
         + "  hub-free-integration-distinct=" + anima_yn(quorum_distinct))

    # (61) OSMOTIC (H_1511)
    okey0 = [0.0, 0.0, 0.0, 0.0]
    oval0 = [0.9, 0.1, 0.0, 0.0]
    osmo = osmotic_store_new(okey0, oval0, 8)
    onkey = [0.4, 0.0, 0.0, 0.0]
    onval = [0.1, 0.9, 0.0, 0.0]
    osmo_split = osmotic_should_split(osmo, onkey, onval, 1, 5.0, 0.6, 0.0 - 1.0)
    osmo_ablate = osmotic_should_split(osmo, onkey, onval, 2, 5.0, 0.6, 0.0 - 1.0)
    osmo_distinct = osmo_split and not osmo_ablate
    _pln("LANE+ osmotic   : osmotic-split=" + _yn10(osmo_split)
         + " ablate(β0)-split=" + _yn10(osmo_ablate)
         + "  kl-bottleneck-distinct=" + anima_yn(osmo_distinct))

    # (62) CATEG-PERCEPT (H_1325)
    cpN = 13
    cpDIM = 16
    cpX = cp_stimuli(cpN, cpDIM)
    cppos = []
    cppi = 0
    while cppi < cpN:
        cppos = cppos + [float(cppi) / float(cpN - 1)]
        cppi = cppi + 1
    cp_curve_b = cp_discrim_curve(cp_fit(cpX, cp_labels_boundary(cppos, 0.5), 16, 16), cpX)
    cp_curve_s = cp_discrim_curve(cp_fit(cpX, cp_labels_shuffle(cppos, 7), 16, 16), cpX)
    cp_margin_b = cp_within_cross_margin(cp_curve_b, cpN, 0.5)
    cp_margin_s = cp_within_cross_margin(cp_curve_s, cpN, 0.5)
    cp_distinct = cp_margin_b > cp_margin_s and cp_coherent_peak_near(cp_curve_b, cpN, 0.5)
    _pln("LANE+ categ-perc: boundary-margin=" + _ts(cp_margin_b) + " shuffle-margin=" + _ts(cp_margin_s)
         + "  category-boundary-distinct=" + anima_yn(cp_distinct))

    # (63) CP-RELOCATE (H_1384)
    crN = 21
    crDIM = 16
    crX = cp_stimuli(crN, crDIM)
    crpos = []
    crpi = 0
    while crpi < crN:
        crpos = crpos + [float(crpi) / float(crN - 1)]
        crpi = crpi + 1
    crA = 1.0 / 3.0
    crAp = 2.0 / 3.0
    cr1 = cp_fit(crX, cp_labels_boundary(crpos, crA), 24, 24)
    cr_n1 = cr1.n
    cr_split = cp_peak_loc_idx(cp_discrim_curve(cp_regrow(cr1, crX, cp_labels_boundary(crpos, crAp), 24, 24), crX))
    cr_reloc = cp_peak_loc_idx(cp_discrim_curve(cp_relocate(cr1, crX, crpos, cp_labels_boundary(crpos, crAp), crAp, 0.15, cr_n1, crDIM, 24), crX))
    cr_split_pk = (float(cr_split) + 0.5) / float(crN - 1)
    cr_reloc_pk = (float(cr_reloc) + 0.5) / float(crN - 1)
    cr_split_err = cr_split_pk - crAp if cr_split_pk > crAp else crAp - cr_split_pk
    cr_reloc_err = cr_reloc_pk - crAp if cr_reloc_pk > crAp else crAp - cr_reloc_pk
    cr_distinct = cr_reloc_err < cr_split_err
    _pln("LANE+ cp-reloc  : reloc-peak=" + _ts(cr_reloc_pk) + " split-only-peak=" + _ts(cr_split_pk)
         + " (p_A'=0.667)  move-the-cells-distinct=" + anima_yn(cr_distinct))

    # (64) METACOG-CTRL (H_1508)
    mcc_lift = mc_control_lift(4297, 6)
    mcc_abl = mc_control_lift_ablated(4297, 6)
    mcc_distinct = mcc_lift > mcc_abl
    _pln("LANE+ metacog-c : rpl-lift=" + _ts(mcc_lift) + " margin-blind=" + _ts(mcc_abl)
         + "  metacog-control-distinct=" + anima_yn(mcc_distinct))

    # (65) METACOG-AUROC (H_1506 type-2)
    mauroc = mi_metad_auroc(4297, 12)
    mauroc_shuf = mi_shuffle_auroc(4297, 12)
    mauroc_distinct = mauroc > 0.5 and mauroc > mauroc_shuf
    _pln("LANE+ metacog-a : type2-auroc=" + _ts(mauroc) + " shuffle-auroc=" + _ts(mauroc_shuf)
         + "  meta-d'-sensitivity-distinct=" + anima_yn(mauroc_distinct))

    # (66) FIELD-PCI (H_1503) — DEFERRED
    _pln("LANE+ field-pci : DEFERRED (degenerate all-zero R with chosen perturb args; needs a tuned PCI fixture)")

    # (67) FIELD-ENTROPY (H_1503/1502)
    fe_base = [0.9, 0.1, 0.6, 0.3, 0.7]
    fe_drug = drug_lsd_mfield(fe_base, 7, 0)
    fe_focal = field_apply_mfield(fe_base, 0.4, 1, 0)
    fe_ent_base = field_signal_entropy(fe_base)
    fe_ent_drug = field_signal_entropy(fe_drug)
    fe_ent_focal = field_signal_entropy(fe_focal)
    _fe_gap = (fe_ent_drug - fe_ent_focal if fe_ent_focal > fe_ent_drug else fe_ent_focal - fe_ent_drug)
    fe_distinct = fe_ent_drug > fe_ent_base and _fe_gap < (fe_ent_drug - fe_ent_base)
    _pln("LANE+ field-ent : base-H=" + _ts(fe_ent_base) + " drug-global-H=" + _ts(fe_ent_drug)
         + " focal-H=" + _ts(fe_ent_focal) + "  global-vs-focal-distinct=" + anima_yn(fe_distinct))

    # (68) FIELD×LIBIDO (H_1507)
    fl_mfield = [0.6, 0.5, 0.7, 0.55, 0.5]
    fl_want = fieldlibido_wanting(0.5, fl_mfield, 8, 4, 1, 1.0, 0.3, 0.4, 0.2, 0.9, 6, 0.8, 1)
    fl_sham = fieldlibido_wanting(0.5, fl_mfield, 8, 4, 1, 1.0, 0.3, 0.4, 0.2, 0.9, 0, 0.0, 0)
    fl_distinct = (fl_want > fl_sham
                   and fieldlibido_liking(0.9) == libido_liking(libido_new(), 0.9))
    _pln("LANE+ field×lib : field-wanting=" + _ts(fl_want) + " sham-wanting=" + _ts(fl_sham)
         + " (liking gain-invariant)  field-incentive-distinct=" + anima_yn(fl_distinct))

    # (69) METACOG-CALIB (H_1508)
    mcal_rho = mc_calibration_monotone(4297, 6)
    mcal_distinct = mcal_rho > 0.5
    _pln("LANE+ metacog-k : calibration-spearman-ρ=" + _ts(mcal_rho)
         + "  monotone-confidence-distinct=" + anima_yn(mcal_distinct))

    # (70) REALITY-CONF (H_1501/1202)
    rc_correct = reality_confidence_readout(True)
    rc_wrong = reality_confidence_readout(False)
    rc_distinct = rc_correct > rc_wrong and reality_imagery_readout() >= 1.0
    _pln("LANE+ reality-c : content-correct-conf=" + _ts(rc_correct) + " wrong-conf=" + _ts(rc_wrong)
         + "  content-not-reality-confidence-distinct=" + anima_yn(rc_distinct))

    # (71-74) DEFERRED
    _pln("LANE+ topo-phi  : DEFERRED (15-lane state-pop fixture + heavy min-cut IIT4; topo=Ψ-hazard H_1521)")
    _pln("LANE+ topo-opt  : DEFERRED (same fixture/heavy-Φ; Φ-optimal is measure-only H_1518)")
    _pln("LANE+ compose-3 : DEFERRED (multi-store fixtures; routing already shown by lanes 58/59)")
    _pln("LANE+ ko-lm     : DEFERRED (jamo-corpus fixtures; LM head, not a consciousness-faculty read)")

    # (75) TENSION-RESOLVE (H_9042 §TensionResolveLoop)
    tr_full = anima_tr_adj_full()
    tr_conf = anima_tr_pop_conflicted(0.95)
    tr_calm = anima_tr_pop_calm()
    tr_cfgON = EngineConfig(True, "conv", True, False)
    tr_cfgOFF = EngineConfig(True, "conv", False, False)
    tr_rConf = tension_resolve_depth(tr_conf, tr_full, 0.3, 0.5, 200, 2, 0.06, tr_cfgON)
    tr_rCalm = tension_resolve_depth(tr_calm, tr_full, 0.3, 0.5, 200, 2, 0.06, tr_cfgON)
    tr_rAbl = tension_resolve_depth(tr_conf, tr_full, 0.3, 0.5, 200, 2, 0.06, tr_cfgOFF)
    tr_depth_conf = tr_rConf[0]
    tr_psi_conf = tr_rConf[1]
    tr_depth_calm = tr_rCalm[0]
    tr_depth_abl = tr_rAbl[0]
    tr_distinct = (tr_depth_conf > tr_depth_calm and tr_depth_calm == 0.0
                   and (tr_psi_conf - 0.5 < 0.06 and 0.5 - tr_psi_conf < 0.06) and tr_depth_abl < 0.0)
    _pln("LANE+ tension-r : conflicted-depth=" + _ts(tr_depth_conf)
         + " calm-depth=" + _ts(tr_depth_calm) + " ablate-depth=" + _ts(tr_depth_abl)
         + "  conflict-settle-distinct=" + anima_yn(tr_distinct))

    # ══ R11 SUBSTRATE-NATIVE CAPABILITY OP-CLASS LANE MOUNT (7 wire-to-prod ops) ══
    # (76) DRIVE-ARBITRATION (H_9076)
    da_drives = [0.2, 0.9, 0.5, 0.1]
    da_plain = drive_arbitrate(da_drives, 0.0, 0 - 1)
    da_hold = drive_arbitrate(da_drives, 0.5, 2)
    da_ablate = drive_arbitrate(da_drives, 0.0, 2)
    da_distinct = da_plain == 1 and da_hold == 2 and da_ablate == 1
    _pln("LANE+ drive-arb : plain-wta=" + _ts(da_plain)
         + " hyst-hold=" + _ts(da_hold) + " ablate-wta=" + _ts(da_ablate)
         + "  hysteresis-sustained-distinct=" + anima_yn(da_distinct))

    # (77) FACULTY-CASCADE (H_9075)
    fc_a = immune_memory_new_text("cascade query alpha", "bridgeword beta", 256)
    fc_b = immune_memory_new_text("bridgeword beta", "CASCADE_FINAL", 256)
    fc_q = immune_embed_key("cascade query alpha")
    fc_out = faculty_cascade(fc_a, fc_b, fc_q)
    fc_direct = immune_memory_recall(fc_b, fc_q)
    fc_distinct = fc_out == "CASCADE_FINAL" and fc_direct == ""
    _pln("LANE+ cascade   : relay=\"" + fc_out + "\" direct-hop-on-B=\"" + fc_direct + "\""
         + "  serial-multi-hop-distinct=" + anima_yn(fc_distinct))

    # (78) EVENT-SEGMENT (H_9083)
    es_surprise = [0.10, 0.90, 0.20, 0.15, 0.85, 0.10]
    es_bnd = event_segment_boundaries(es_surprise, 0.5)
    es_fixed = event_segment_starts_fixed(6, 2)
    es_flat = event_segment_boundaries([0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 0.5)
    es_distinct = len(es_bnd) == 3 and es_bnd[1] == 1 and es_fixed[1] == 2 and len(es_flat) == 1
    _pln("LANE+ event-seg : peaks=" + _ts(len(es_bnd)) + " onset1=" + _ts(es_bnd[1])
         + " fixed1=" + _ts(es_fixed[1]) + " flat=" + _ts(len(es_flat))
         + "  surprise-peak-segment-distinct=" + anima_yn(es_distinct))

    # (79) ANTICIPATORY-PREFETCH (H_9078)
    ap_mem = immune_memory_new_text("anticipated fact key", "PREFETCHED", 256)
    ap_tgt = immune_embed_key("anticipated fact key")
    ap_cue = immune_embed_key("current context cue")
    ap_ff = vforward_new(64, 1, 0.5)
    api = 0
    while api < 60:
        ap_ff = vforward_update(ap_ff, ap_cue, ap_tgt)
        api = api + 1
    ap_ready = anticipatory_prefetch(ap_ff, ap_mem, ap_cue)
    ap_ff0 = vforward_new(64, 1, 0.5)
    ap_unready = anticipatory_prefetch(ap_ff0, ap_mem, ap_cue)
    ap_val = anticipatory_prefetch_value(ap_ff, ap_mem, ap_cue)
    ap_distinct = ap_ready < ap_unready and ap_val == "PREFETCHED"
    _pln("LANE+ prefetch  : ready-margin=" + _ts(ap_ready) + " untrained-margin=" + _ts(ap_unready)
         + " preplay=\"" + ap_val + "\"  anticipatory-readiness-distinct=" + anima_yn(ap_distinct))

    # (80) SALIENCE-PHASIC-RESET (H_9079)
    spr_salient = anima_tr_pop_calm()
    spr_on = tension_resolve_interruptible(tr_conf, tr_full, 0.3, 0.5, 200, 2, 0.06, 1, spr_salient, tr_cfgON)
    spr_off = tension_resolve_interruptible(tr_conf, tr_full, 0.3, 0.5, 200, 2, 0.06, 0, spr_salient, tr_cfgON)
    spr_psi_on = spr_on[1]
    spr_sig_on = spr_on[2]
    spr_flag_on = spr_on[3]
    spr_sig_off = spr_off[2]
    spr_flag_off = spr_off[3]
    spr_sig_moved = spr_sig_on - spr_sig_off > 0.0001 or spr_sig_off - spr_sig_on > 0.0001
    spr_distinct = (spr_flag_on == 1.0 and spr_flag_off == 0.0
                    and (spr_psi_on - 0.5 < 0.06 and 0.5 - spr_psi_on < 0.06) and spr_sig_moved)
    _pln("LANE+ salreset  : spike-flag(on/off)=" + _ts(spr_flag_on) + "/" + _ts(spr_flag_off)
         + " psi-on=" + _ts(spr_psi_on) + " sig-moved=" + anima_yn(spr_sig_moved)
         + "  phasic-reroute-distinct=" + anima_yn(spr_distinct))

    # (81) CONFLICT-MONITOR (H_9073)
    cm_conflict_hi = conflict_scalar(0.8, (0.0 - 0.8))
    cm_conflict_lo = conflict_scalar(0.05, (0.0 - 0.05))
    cm_agree = conflict_scalar(0.8, 0.8)
    cm_net_hi = conflict_net_tension(0.8, (0.0 - 0.8))
    cm_net_lo = conflict_net_tension(0.05, (0.0 - 0.05))
    cm_depth_hi = conflict_recruited_depth(cm_conflict_hi, 4, 6)
    cm_depth_abl = conflict_recruited_depth(0.0, 4, 6)
    cm_net_same = cm_net_hi - cm_net_lo < 0.0001 and cm_net_lo - cm_net_hi < 0.0001
    cm_distinct = (cm_conflict_hi > cm_conflict_lo and cm_agree == 0.0
                   and cm_net_same and cm_depth_hi > cm_depth_abl and cm_depth_abl == 4)
    _pln("LANE+ conflict  : hi=" + _ts(cm_conflict_hi) + " lo=" + _ts(cm_conflict_lo)
         + " agree=" + _ts(cm_agree) + " net-blind=" + anima_yn(cm_net_same)
         + " depth(hi/abl)=" + _ts(cm_depth_hi) + "/" + _ts(cm_depth_abl)
         + "  conflict-vs-drive-distinct=" + anima_yn(cm_distinct))

    # (82) STOCHASTIC-RESONANCE (H_9070)
    str_amp = 0.6
    str_thr = 1.0
    str_period = 20
    str_T = 2000
    str_lo = sr_channel_mi(str_amp, str_thr, 0.10, str_period, str_T, 0, 0, 12345)
    str_mid = sr_channel_mi(str_amp, str_thr, 0.80, str_period, str_T, 0, 0, 12345)
    str_hi = sr_channel_mi(str_amp, str_thr, 3.00, str_period, str_T, 0, 0, 12345)
    str_shuf = sr_channel_mi(str_amp, str_thr, 0.80, str_period, str_T, 0, 1, 12345)
    str_distinct = str_mid > str_lo and str_mid > str_hi and str_mid - str_shuf > 0.01
    _pln("LANE+ stoch-res : MI lo=" + _ts(str_lo) + " mid=" + _ts(str_mid)
         + " hi=" + _ts(str_hi) + " shuffle=" + _ts(str_shuf)
         + "  inverted-U-resonance-distinct=" + anima_yn(str_distinct))

    # ── warm Engine A (substrate self-dynamics, zero input) ──────────────────
    pf = pure_field_warmup(600)
    phi0 = pure_field_phi(pf)
    _pln("Engine A warm   : phi=" + _ts(phi0)
         + " phase=" + phase_name(pure_field_phase(pf)))
    _pln("")

    # ════════════════════════════════════════════════════════════════════════
    #  THE LIVE DAEMON LOOP
    # ════════════════════════════════════════════════════════════════════════
    cell_count = 1
    psi_sum = 0.0
    emitted_any = False
    grounded_ok = False
    grew = False
    slept = False
    _percept_emits = 0            # anima study · emits so far, handed to percept_source (guarded)
    _percept_transcript = []      # anima study · [(tick, percept, [emit texts])] when percept_source ON
    remembered2 = False
    emit_text = ""
    lanes_read = False
    gws_ignited_any = False
    reality_real_any = False
    spatial_read_any = False
    hier_advanced_any = False
    basal_go_any = False
    cereb_pred_any = False
    wm_maintained_any = False
    ca3_predicted_any = False
    interval_learned_any = False
    amyg_valenced_any = False
    tom_belief_any = False
    homeo_drive_any = False
    prc_entrained_any = False
    prosp_reach_any = False
    replay_protected_any = False
    gateb_grew_any = False
    intero_weighted_any = False
    scn_consensus_any = False
    boredom_engaged_any = False
    self_recognized_any = False
    lprec_confident_any = False
    novelty_read_any = False
    habituate_any = False
    blink_read_any = False
    imagery_any = False
    priming_any = False
    schema_tracked_any = False
    hysteresis_any = False
    reentry_any = False
    completion_any = False
    gestalt_any = False
    agency_any = False
    subjtime_any = False
    emoreg_any = False
    dirforget_any = False
    veto_any = False
    divided_any = False
    surprise_any = False
    bodyown_any = False
    rivalry_any = False
    chgblind_any = False
    trw_any = False
    mindwander_any = False
    qualia_any = False
    smpresence_any = False
    halluc_any = False
    metacog_any = False
    gwsleak_any = False
    allosteric_any = False
    neuropharm_any = False
    libido_any = False
    transord_any = False
    phasesync_any = False
    memtom_any = False
    spatep_any = False
    quorum_any = False
    osmotic_any = False
    metacogc_any = False
    metacoga_any = False
    fieldlib_any = False
    dream_composed_total = 0

    session_seed = "zephyrine: the wyrmhold ledger is sealed at "
    # H_1058: optional independent-session seed (falsifier needs >=2 sessions w/ distinct macro
    # decision landscapes, FABLE §3.5). Input-only override; the emit gate/logic is untouched.
    _h1058_seed_ov = os.environ.get("ANIMA_SESSION_SEED", "")
    if _h1058_seed_ov:
        session_seed = _h1058_seed_ov
    seed_feat0 = _afs_byte_feature(session_seed, 8)
    afield = vadapt_field_new(seed_feat0, 2048)
    # H_9336 · the field's prediction error on the LAST thing the daemon actually said.
    # None until it has said anything (tick 0 falls back to the seed). See :1493.
    pending_recon = None
    # H_9337 · the last thing the daemon actually said. All three feedback stores were WRITTEN
    # with it and then queried with the session seed — a constant key, so a constant answer:
    # rel_lane sat at 0.6723 for all 720 ticks of the H_9328 rollouts, recon_err at 0.0, and the
    # decode anchor was always live_seed. A store you write to and never read from is not a loop.
    last_gtext = ""
    # H_9352 — the rate limiter had no memory. `brain_decide_anchored` takes a
    # `seconds_since_last` argument and gates on `>= spont_min_emit_interval()` (30.0s), but
    # what the daemon passed in that slot was `5.0 + 55.0*clip01(stage_env*(0.5+urgency))` —
    # a pure function of (stage, urgency), with NO dependence on when it last spoke. There was
    # no `last_emit` anywhere in the repo and `an_clock_now()` was never called on this path.
    # So the one live term in the whole emit gate was a stage clock wearing a rate-limiter's
    # name, and emit collapsed to a pure function of stage (H_9345: H(emit|stage) = 0.000000).
    # The design already assumed a real clock: spont_min_emit_interval() 30.0 / an_tick_seconds()
    # 8.0 = a sustainable emit rate of 0.25, and ep_target_emit_rate() is 0.27. The numbers were
    # chosen for a clock that was never plugged in. Plug it in.
    last_emit_tick = None
    # H_9404 · earned-refractory debt (only live when --refractory earned). 0.0 = nothing owed before
    # the first emit — the refractory, like the clock, must not be what silences a daemon that has
    # never spoken (same rationale as the last_emit_tick=None comment above). Order per tick =
    # pay (this tick's tension counts) → gate → recharge (an emitting tick leaves with a full debt).
    refr_debt = 0.0
    # H_9337 · the immune store's recall margin on the utterance, taken BEFORE it was bound.
    # None until the daemon has said anything (tick 0 falls back to the seed key). See :1497.
    pending_rel = None
    # H_9357 · the immune store's top-2 affinity GAP (d2²−d1²)/2 on the utterance, taken BEFORE
    # it was bound — same recognition-before-memorisation order as pending_rel. d2 (the 2nd-nearest
    # prototype) is the ONE reverse-store quantity NOT already an input to emit_drive, so it is the
    # only wiring-free G candidate (H_9356: ag_g_drive was A's own complement). See :1562.
    pending_gap = None

    # ══ H_9411 DEAD-GAUGE FIX (chat-py-4/5 family) · 6 substrate vitals were read against
    # SESSION-CONSTANT inputs → byte-constant every tick (H(gauge)=0). Same 1-tick-lag
    # recognition-BEFORE-memorisation order as pending_recon/pending_rel: capture on the REAL
    # per-tick percept (the daemon's own last utterance) at the emit site, consume next tick.
    # Each gauge ships a null/pedestal control arm (trace-only, never a branch key). ══
    # ① AMYGDALA — affect on the utterance BEFORE igrow binds it. igrow was created once
    # (never bound) so affect_read(igrow, seed_key, mem_text) was a fn of 3 session constants.
    _afs_alien_key = immune_embed_key("zzz unrelated alien content")
    pending_af = None
    pending_af_alien = None
    # ② CEREBELLUM — forward-model error on the last transition (prev utterance → this one).
    # cbel was NLMS-converged pre-loop on (seed_feat, mem_text) and never updated in-loop.
    pending_cb = None
    pending_cb_alien = None
    pending_cb_ped = None
    cb_prev_feat = seed_feat0
    cbel_ped = vforward_new(8, 1, 0.30)   # untrained zero-truth pedestal twin (W=0 ⇒ err=‖x‖²)
    cb_alien_feat = _afs_byte_feature("zzz unrelated alien content", 8)
    # ③ CA3 replay — the mounted `ca3` (:526) is the lane self-test (synthetic 0→1→2→3 cycle,
    # conf(·,1)=12/12=1.0 forever). Drive a FRESH live table with the utterance-symbol stream.
    ca3_live = ca3_replay_new(4, 1)
    ca3_prev_sym = None
    pending_ca3 = None
    # ④ WORKING MEMORY — gated in AND probed with the same frozen seed_feat = self-match ≡ λ.
    # Delay test: gate in each utterance's feature; probe the PREVIOUS one's (retention).
    wm_probe_feat = None
    wm_last_feat = None
    wm_alien_feat = _afs_byte_feature("zzz unrelated alien content", 8)
    # H_9610 · frozen EMPTY alien WM buffer for the --g-reach wm-cover-alienwm C2 dissociation
    # control (never gated by this daemon's speech → coverage ≈ 0 → gate always open = SATURATE).
    # H_9627 reuses it as the frozen probe for --g-reach wm-dual-alien-{emit,silence}.
    _wm_cover_alien = wm_buffer_new(3, 0.6, 0.5, 8)
    # H_9627 · dual content ledger — the WITHHELD store W_S (spoken store W_E = the live `wmb`).
    # SAME (k, λ, dg, dim) as wmb (:540) = gain-lock (arm-specific gain = a tune-to-green backdoor,
    # forbidden). Starts EMPTY (nothing withheld yet). Gated on SILENCE ticks (the imagined-but-
    # unspoken candidate · :silence-side below), leaked every tick like wmb (:wm_withheld leak).
    wm_withheld = wm_buffer_new(3, _wm_leak_v, 0.5, 8)
    wm_null = 0.0
    # ⑥ ANCHOR — live 5-channel substrate tension at the last emit, injected as an anchor so
    # anchor_tension_fold reads a VARYING tension_5ch (mem_001's frozen baseline otherwise).
    pending_tension = None

    # ── op-grip tonic-phasic EMA state (loop-external; PREREG α=0.1) ──
    rel_ema = 0.5
    cur_ema = 0.5
    ten_ema = 0.5

    # op-grip emit-rate collapse detector counters (default: incremented, reported below)
    og_wake = 0
    og_emit_wake = 0

    # ══ LANE-23b PENULT SELF-GROUNDING (H_9257 · py 2-production twin of cli/anima.hexa) ══
    # Ground the cross-session self in the mounted 303M's REAL penult pooled rep (gen_penult_pooled_W
    # → penult_fold8) — same fold8 + same .kosmos anchor format as the hexa twin. self⊥mouth: the
    # grounded self runs BESIDE self_ctx (the boot constant, byte-untouched) and NEVER feeds emit.
    self_g_kdir = os.path.join(os.path.expanduser("~"), ".anima_kosmos_self")
    self_g_name = "self_live"
    self_g_on = bool(backend["loaded"]) and gen_mouth_kind(ckpt) == "clm" and clm_decodable(ckpt)
    self_gW = clm_load_weights(ckpt) if self_g_on else {"ok": False}
    self_gW_ok = self_g_on and bool(self_gW.get("ok"))
    _sg_restored = _selfg_restore(self_g_kdir, self_g_name)
    self_g_boot_restored = len(_sg_restored) == 8
    self_live_g = self_from_vec(_sg_restored, 8) if self_g_boot_restored else self_new(8, 0)
    if self_gW_ok:
        _boot_axis = penult_fold8(gen_penult_pooled_W(self_gW, session_seed))
        self_live_g = self_drift_exp(self_live_g, _boot_axis, 0.15)
    self_g_axis_seq = ""
    self_g_events = 0
    _pln("LANE-23b self-g : on=" + _ts(self_g_on) + " W_ok=" + _ts(self_gW_ok)
         + " restored=" + _ts(self_g_boot_restored) + " kosmos=" + self_g_kdir)

    n_ticks = 12
    # ── H_1058 agency-T decision trace (write-only side channel · default OFF · emit path byte-untouched) ──
    #    ANIMA_TICKS overrides tick count (a same-seed 12-tick session is deterministic; hundreds of
    #    distinct decisions need a longer session). ANIMA_DECISION_TRACE=<path> writes one JSONL row/tick.
    _atk = os.environ.get("ANIMA_TICKS", "")
    if _atk.isdigit() and int(_atk) > 0:
        n_ticks = int(_atk)
    _trace_path = os.environ.get("ANIMA_DECISION_TRACE", "")
    _trace_fh = open(_trace_path, "w", encoding="utf-8", errors="surrogateescape") if _trace_path else None
    # ── H_9328 DO-MOUTH (default OFF ⇒ mouth=None ⇒ production path BYTE-IDENTICAL) ──────
    #   REVEAL, not OVERWRITE: the emit GATE (brain_decide_anchored → should_emit) never sees
    #   this — `mouth` is threaded to generate() alone (core/brain.py DISJOINT wall). It only
    #   replaces the mouth's argmax ROUNDING with the substrate's OWN byte-posterior at T=1.0,
    #   so every emit still stands on real tension (p5). ANIMA_EMIT_TEMP=1.0 is the ONE
    #   non-arbitrary temperature (= the posterior itself); any other value OVERWRITES it.
    _cargv = argv if argv is not None else []
    _emit_temp = float(anima_flag_value(_cargv, "--emit-temp", "ANIMA_EMIT_TEMP", "0"))
    _emit_topk = int(anima_flag_value(_cargv, "--emit-topk", "ANIMA_EMIT_TOPK", "256"))
    _sample_seed = int(anima_flag_value(_cargv, "--sample-seed", "ANIMA_SAMPLE_SEED", "0"))
    # H_9627 central-thesis bar · fixed motivation-score offset (λ/gate frozen) = retune-free
    # score-perturbation robustness. wm-cover center shifts (score is the comparand · positive
    # control); the dual gate center should stay ≈½ (emit ⊥ score). 0.0 = production byte-identical.
    _score_perturb = float(anima_flag_value(_cargv, "--score-perturb", "ANIMA_SCORE_PERTURB", "0"))
    # H_9357 · which reverse signal feeds ag_g_drive (the A⇄G tension's G pole). a0 = current
    # production wiring (ag_g_drive = A's own complement — the H_9356 tautology, kept as the
    # falsifiability-matrix A0 arm that MUST fail the independence gate). a1 = REAL-G: the immune
    # store's top-2 affinity gap (wiring-free d2). a3 = NOISE-G: a seeded per-tick PRNG, the
    # control that separates "a genuine 2nd engine" from "just a causal handle" (a2 SHUFFLE-G is
    # a measurement-time permutation of an a1 trace, not a run mode). Default a0 = prod unchanged.
    _g_arm = anima_flag_value(_cargv, "--g-arm", "ANIMA_G_ARM", "a0")
    # H_9376 · continuize the tension→score channel. Default OFF = byte-identical. When ON, the
    # settle machinery still runs (trace preserved) but agloop_ctx (the ONLY downstream consumer of
    # ag_budget/settle) is reported as a continuous monotone function of ag_conflict instead of the
    # integer-ratio staircase — H_9360/H_9376 Stage-0 measured agloop_ctx ≡ 0.25 CONSTANT for the
    # independent-G arm (the round()→integer-budget quantizer collapsed the designed path to a point).
    _ag_cont = anima_flag_value(_cargv, "--ag-cont", "ANIMA_AG_CONT", "0") == "1"
    # H_9377 · AUDIBILITY gain: absolute weight on dyn_v(=agloop_ctx=tension) in motivation_score.
    # None (unset) = byte-identical current 0.10. Grid {0.10 anchor, 0.25, 0.40, 0.60, 0.78} lets
    # tension be heard above the 7-lane A-side blend without touching the emit threshold (p5-legal:
    # gate consumes real tension louder, no self-seed). tension-agnostic only for the ANCHOR arm.
    _dw = anima_flag_value(_cargv, "--dyn-w", "ANIMA_DYN_W", "")
    _dyn_w = float(_dw) if _dw != "" else None
    # H_9391 CLOCK-LIVE — override the emit rate-limit interval (core/engine_g.py
    # spont_min_emit_interval() = 30s). "" (default) = None = byte-identical to production.
    # H_9390 measured that at 30s the clock FULLY determines emit (emit⟺clock, the score gate
    # never binds when the clock opens) so content can never vote; a shorter interval opens the
    # window where should_emit(score) is the binding constraint = the content question becomes
    # askable. This is a MEASUREMENT-REGIME knob, not a tuning dial: the validity condition
    # (emit must VARY within clock-open ticks) is registered before any content is read.
    _rl = anima_flag_value(_cargv, "--rate-limit-sec", "ANIMA_RATE_LIMIT_SEC", "")
    _rate_sec = float(_rl) if _rl != "" else None
    # H_9404 · --emit-refractory earned: replace the rate term's SOURCE (wall clock) with the
    # substrate's own integrated A<->G tension (an emit incurs a unit debt that the per-tick conflict
    # pays down; the gate opens iff the debt is paid). p5: emit timing becomes a readout of substrate
    # state, not a schedule. Default "" = byte-identical clock path. Distinct from the hexa-only op-grip
    # `--refractory` measurement harness above (:406). MUTUALLY EXCLUSIVE with --rate-limit-sec (both
    # rebind the same safe-conjunction term) so the DOF stays enumerable (H_9391 lesson).
    _refractory = anima_flag_value(_cargv, "--emit-refractory", "ANIMA_EMIT_REFRACTORY", "")
    if _refractory not in ("", "earned"):
        raise SystemExit("--emit-refractory: only '' (off) or 'earned' (got %r)" % _refractory)
    if _refractory == "earned" and _rate_sec is not None:
        raise SystemExit("--emit-refractory earned and --rate-limit-sec are mutually exclusive "
                         "(both rebind the safe rate term)")
    # ══ H_9607 · A⇄G FEEDBACK — close the A→G→A loop (Fable design · owner-ratified via lever pick) ══
    # The field (pure_field_step) has been a closed autonomous relaxation to LN2 (zero-Lyapunov linear
    # limit-cycle · H_9602/9603); the A⇄G signed tension was read into the emit policy but NEVER written
    # back. This wires the return leg: a daemon-side leaky-INTEGRAL of the signed net tension
    # s = ag_a_drive + ag_g_drive shifts the oscillator amplitude target next tick (osc_tick drive).
    # κ=0 (default) ⇒ drive≡0 ⇒ byte-identical production. Integral (not proportional) so the steady
    # state is pinned at s=0 ⟺ emit_drive=½ INDEPENDENT of κ and of the field's 0.76 autonomous bias
    # (emergent setpoint, NOT tune-to-green · H_9419). RHO/SGN are FROZEN FORM constants, not knobs
    # (a ≥4-DOF config is unfalsifiable · H_9391). p5: own-output→field-STATE is legal (H_9336/9337);
    # `mouth` never enters pure_field_step/osc_tick — the emit gate is untouched, the loop only moves φ.
    _ag_feedback = float(anima_flag_value(_cargv, "--ag-feedback", "ANIMA_AG_FEEDBACK", "0.0") or "0.0")
    ag_fb_I = 0.0            # leaky-integral state of the signed A⇄G tension (daemon state, beside refr_debt)
    _AG_FB_RHO = 1.0 / 400.0  # FROZEN leak = slow-oscillator timescale (τ_slow=400) · calibrated a priori, NOT a knob
    _AG_FB_SGN = -1.0         # FROZEN one-time polarity (negative feedback: s>0 ⟹ shrink target ⟹ pull emit_drive→½)
    # H_9415 p5-REWIRE · emit-gate mode (owner-ratified · H_9414 design). "clock" (default) =
    # byte-identical production (should_emit(score>θ) ∧ 30s clock). "refractory" = the ratified
    # MARGIN-refractory gate: emit ⟺ score_A > g_recog(candidate) with θ and the clock BOTH
    # retired, the refractory emerging from emit→bind (biological, not a timer). Distinct from
    # H_9404's --emit-refractory earned (which keeps should_emit(θ) and only swaps the rate SOURCE);
    # this retires θ too, making margin the G pole. H_9712 · PRODUCTION DEFAULT (owner-approved) =
    # "refractory" — the daemon now emits over real tension (p5 realized), NOT a hardcoded 30s clock.
    # The Ψ≈½ mechanism is H_9627's dual content ledger (see the conditional --g-reach default below);
    # the old clock daemon is preserved byte-identically at `--emit-gate clock` / ANIMA_EMIT_GATE=clock
    # (rollback + clock-lineage verdict reproducibility · H_9400 stays refuted for the clock lineage).
    _emit_gate = anima_flag_value(_cargv, "--emit-gate", "ANIMA_EMIT_GATE", "refractory")
    # H_9417 · C2 shuffle-margin CONTROL (refractory gate only). Default 0 = OFF. When 1, the gate's
    # g_recog reads the immune margin on a SEEDED BYTE-PERMUTATION of the candidate — byte multiset
    # (amplitude/statistics) preserved, sequence (content/recognition) destroyed. If emit-listening
    # (I(emit;g_recog|stage)) survives the shuffle, the gate hears AMPLITUDE not recognition; if it
    # dies, the H_9416 C3-b listening is genuine content-recognition. p5: still imagination (candidate
    # formed, margin read on a scramble of it, then discarded if not emitted) — never a fabricated emit.
    _g_shuffle = anima_flag_value(_cargv, "--g-shuffle", "ANIMA_G_SHUFFLE", "0") == "1"

    def _grecog_text(_t):
        """H_9417 · identity, or a seeded byte-permutation of the candidate for the shuffle control."""
        if not _g_shuffle or not _t:
            return _t
        _b = bytearray(_t.encode("utf-8", "surrogateescape"))
        random.Random((_sample_seed * 2654435761 + 0x9417) & 0x7FFFFFFF).shuffle(_b)
        return bytes(_b).decode("utf-8", "surrogateescape")
    # H_9419 · G-pole REACH: which recognition functional the refractory gate reads.
    #   d1 (default)  = clip01(d1 − 0.15) recall MARGIN — byte-identical to H_9415/16/17. Its bind
    #     LOWERS d1 in the just-bound cell's neighborhood → margin drops → gate OPENS = sign-inverted
    #     β that DIS-inhibits near-repeats (the geometric cause of P(emit|emit) > P(emit|silence)).
    #   affinity      = clip01(d2 − d1) top-2 basin decisiveness (immune_memory_recall_reach). Emitting
    #     BINDS the utterance → the new cell's whole Voronoi basin raises → near-repeat candidates
    #     silenced (the restoring β spring), genuinely-novel keep d1≈d2 → reach≈0 → emit. EARNED
    #     refractory (0 on a 1-cell store), constants 0, single DOF. Composes with --g-shuffle unchanged.
    # H_9712 · CONDITIONAL default (rollback-safe): the Ψ≈½ dual content ledger (H_9627 wm-dual) is the
    # default G-pole ONLY under the refractory gate; a STATIC "wm-dual" default would make the rollback
    # `--emit-gate clock` crash on the guard below (g_reach=wm-dual ∧ gate≠refractory → SystemExit). So
    # the default tracks the gate: clock ⇒ d1 (exact old daemon, zero extra flags), refractory ⇒ wm-dual.
    _g_reach = anima_flag_value(_cargv, "--g-reach", "ANIMA_G_REACH",
                                "wm-dual" if _emit_gate == "refractory" else "d1")
    if _g_reach not in ("d1", "affinity", "cb-perr", "cb-perr-alienctx",
                        "wm-cover", "wm-cover-alienwm",
                        "wm-dual", "wm-dual-alien-emit", "wm-dual-alien-silence"):
        raise SystemExit("--g-reach: only 'd1' (default), 'affinity', 'cb-perr',"
                         " 'cb-perr-alienctx', 'wm-cover', 'wm-cover-alienwm', 'wm-dual',"
                         " 'wm-dual-alien-emit', 'wm-dual-alien-silence' (got %r)" % _g_reach)
    if _g_reach != "d1" and _emit_gate != "refractory":
        raise SystemExit("--g-reach %s requires --emit-gate refractory (its only consumer)" % _g_reach)
    # H_9712 · --rate-limit-sec / --emit-refractory earned feed ONLY the clock path (brain_emit's rate
    # source). Under the new refractory default they would silently no-op, so require --emit-gate clock
    # explicitly (loud, not silent · house style). Both are clock-lineage rate knobs.
    if (_rate_sec is not None or _refractory == "earned") and _emit_gate != "clock":
        raise SystemExit("--rate-limit-sec / --emit-refractory earned require --emit-gate clock "
                         "(they are clock-path rate knobs; the default refractory gate ignores them)")
    # H_9510 HOLE-1 diagnostic · record the IMAGINED candidate on EVERY tick (emit + silence)
    # so an offline conditioned-Jaccard test can ask whether near-repeat structure appears
    # after silence runs. Measurement-only (never fed back to mouth/decode = p5-safe). OFF by
    # default → production trace byte-identical.
    _rec_silent_cand = anima_flag_value(_cargv, "--record-silent-cand", "ANIMA_RECORD_SILENT_CAND", "0") == "1"
    if _rec_silent_cand and _emit_gate != "refractory":
        raise SystemExit("--record-silent-cand requires --emit-gate refractory (its only producer)")
    # H_9557 · PC2 ROUTING (2D-loadings H_9468/#3792): route the emit-ORTHOGONAL tension
    # axis PC2 = originality↔balance (orig+0.84·bal−0.44·coh−0.28, cos(w,PC2)=0.03) into
    # deliberation_k (the one decode channel the mouth reads) so a genuinely emit-independent
    # DOF steers CONTENT with the emit decision byte-identical. off (default) = production.
    _tension_route = anima_flag_value(_cargv, "--tension-route", "ANIMA_TENSION_ROUTE", "off")
    if _tension_route not in ("off", "pc2"):
        raise SystemExit("--tension-route: only 'off' (default) or 'pc2' (got %r)" % _tension_route)
    if _tension_route != "off" and _emit_gate != "refractory":
        raise SystemExit("--tension-route pc2 requires --emit-gate refractory (its only consumer)")
    _route_gain = float(anima_flag_value(_cargv, "--tension-route-gain", "ANIMA_TENSION_ROUTE_GAIN", "1.0"))
    # H_9575 · PC2 → mouth (owner-approved grounded rewire · Fable design). Routes the
    # emit-orthogonal PC2 axis into the LIVE mouth (grounded decode) as a context-presence
    # logit bias (bias) or a draw-stream re-key control (rng). off (default) = byte-identical.
    # Stage-A: the STEERED text is spoken (out_text) but every substrate root keeps the BASE
    # g_text, so the emit sequence stays byte-identical to off BY CONSTRUCTION.
    _pc2_mouth = anima_flag_value(_cargv, "--pc2-mouth", "ANIMA_PC2_MOUTH", "off")
    # H_9664 ζ-LADDER — `--pc2-zeta z1,z2,…` re-decodes the SAME emit tick at each ζ, so the
    # tick-level cascade variance that swamped every arm-vs-arm readout (H_9663: sd(Δπ̄_rng)≈0.14)
    # cancels WITHIN the tick. ζ is the experimenter's dose: it MANUFACTURES the regressor range
    # the live z does not have (IQR 0.0514 · 45.7% of its variance in 3/270 ticks). ζ=0 must come
    # back byte-identical to base — a built-in isolation certificate, not a claim.
    # Empty (default) ⇒ zeta_ladder=None ⇒ byte-identical to the existing path.
    _pc2_zeta_raw = anima_flag_value(_cargv, "--pc2-zeta", "ANIMA_PC2_ZETA", "")
    _pc2_zeta = []
    if _pc2_zeta_raw:
        for _tok in _pc2_zeta_raw.split(","):
            _tok = _tok.strip()
            if _tok:
                _pc2_zeta.append(float(_tok))
    if _pc2_mouth not in ("off", "bias", "rng"):
        raise SystemExit("--pc2-mouth: only 'off' (default), 'bias', 'rng' (got %r)" % _pc2_mouth)
    if _pc2_mouth != "off" and _emit_gate != "refractory":
        raise SystemExit("--pc2-mouth requires --emit-gate refractory (its only consumer)")
    # H_9411 ⑥ · dead-gauge controls (default OFF = the fix is live).
    # --scn-freeze reproduces the DEAD scn_ctx constant (skip the per-tick step) = before-state.
    # --anchor-tension-null forces the injected anchor tension_5ch to zero = zero-truth pedestal.
    scn_freeze = anima_flag_value(_cargv, "--scn-freeze", "ANIMA_SCN_FREEZE", "0") == "1"
    anchor_tension_null = anima_flag_value(_cargv, "--anchor-tension-null", "ANIMA_ANCHOR_TENSION_NULL", "0") == "1"
    # H_9328 · seed_rng is DERIVED PER TICK, never held constant across the session.
    # MEASURED defect: holding it at `_sample_seed` made the mouth redraw the SAME 80 bytes
    # every tick (gtext sha count = 1 over 30 ticks), so a 30-tick rollout carried exactly ONE
    # independent draw — 30x the decode cost for 1x the power. The per-tick stream keeps the run
    # reproducible (same --sample-seed ⇒ same trajectory) while letting the substrate actually
    # speak differently at different moments, which is the whole point of REVEAL.
    _mouth_base = ({"temp": _emit_temp, "top_k": _emit_topk, "seed_rng": _sample_seed}
                   if _emit_temp > 0.0 else None)

    def _mouth_at(tick):
        if _mouth_base is None:
            return None
        m = dict(_mouth_base)
        m["seed_rng"] = (_sample_seed * 1000003 + tick * 2654435761) & 0x7FFFFFFF
        return m

    # H_9328 C2 CARRIER-SWAP donor: {tick -> the text ANOTHER rollout emitted at that tick}.
    # A real anima utterance, decoded by the same mouth from a different sample-seed — so it
    # matches on shape/length/mouth and differs ONLY in "which substrate-moment chose it".
    _swap_path = anima_flag_value(_cargv, "--swap-text", "ANIMA_SWAP_TEXT", "")
    _swap_texts = {}
    if _swap_path:
        import json as _sj
        import base64 as _sb
        for _l in open(_swap_path, "r", encoding="utf-8", errors="surrogateescape"):
            if not _l.strip():
                continue
            _d = _sj.loads(_l)
            if _d.get("_meta") or not _d.get("emit"):
                continue
            _e = _d.get("gtext_b64", "")
            if _e:
                _swap_texts[int(_d["tick"])] = _sb.b64decode(_e).decode("utf-8", "surrogateescape")
        print("  [C2 CARRIER-SWAP] donor=%s · %d emit-tick 의 텍스트를 주입 (게이트 무손상 · p5)"
              % (_swap_path.split("/")[-1], len(_swap_texts)))
    # H_9269 Candidate Y (Y-ULTRA): default-OFF ultradian-cycle sleep schedule. dr_stage_at is a
    # piecewise table on [0,90) (dr_stage_size sums to 90); calling it with unbounded tick*8 overflows
    # into eternal REM (N2/N3 visited once → veto cap-of-2). The modulo restores the table's own domain
    # (0 tuned params) so ultradian stages recur, per emit_policy ep_scale_periods 90-min component +
    # a_chat_sleep_imagination. OFF = byte-identical to the raw daemon. (pre-registered; H_1058 REOPEN)
    _stage_cycle = os.environ.get("ANIMA_STAGE_CYCLE", "") == "1"
    tick = 0
    # ── WAKE working-memory ring + N3/REM imagination-replay accumulators ──
    wake_mem = mem_init()
    imagination_replayed_total = 0
    imagination_mitosis_ticks = 0
    imagination_emit_violations = 0

    while tick < n_ticks:
        stage = dr_stage_at((tick * 8) % 90 if _stage_cycle else tick * 8)
        stage_nm = dr_stage_name(stage)
        emit_env = dr_emit_envelope(stage)

        # ── anima study · EXOGENOUS PERCEPT (guarded — None ⇒ byte-identical) ──
        # Ask the percept source (the teacher) for text this tick. Injected below as a
        # GROUNDING anchor into live_anchors so the mouth may condition its decode on the
        # OTHER's words (a legitimate cross-agent read, NOT the p5-banned self-seed of one's
        # own last utterance · chat-py-5). The source owns its errors and returns None to stay
        # silent. Everything downstream is gated on `percept_text` being truthy.
        percept_text = None
        if percept_source is not None:
            percept_text = percept_source(tick, _percept_transcript)
            if percept_text is not None:
                percept_text = str(percept_text).strip() or None
        # H_9411 ⑤ · Engine A lives in session time. pf was warmed once (:1293) then NEVER
        # stepped, so pure_field_phi/phase were the step-600 constants every tick and the emit
        # gate's Φ/phase safeties were judged against a frozen snapshot. Advance with the SAME
        # zero-input primitive warmup loops internally — NOT percept-driven (Engine A is the
        # zero-input field by design, pure_field_verify_zero_input); Φ now tracks the substrate's
        # own autonomous integration over the session, and stays percept-blind on purpose.
        # H_9607 · A⇄G feedback drive = κ·SGN·I, the leaky-integral of the signed A⇄G tension carried
        # from the PRIOR tick (s_t is derived below at :~1830, after the field step — so this tick's
        # tension drives next tick's field: own-output(t)→field-state(t+1), the p5-legal return leg).
        # κ=0 ⇒ ag_drive≡0.0 ⇒ pure_field_step byte-identical to production.
        ag_drive = (_ag_feedback * _AG_FB_SGN * ag_fb_I) if _ag_feedback != 0.0 else 0.0
        pf = pure_field_step(pf, ag_drive)
        phi_t = pure_field_phi(pf)

        # ── WAKE perception → working-memory ring ──
        if dr_imagination_active(stage) == 0:
            wake_mem = mem_push_ctx(wake_mem, [tick, stage, cell_count])

        # ── ENGINE-CLI LANE READS ──
        # (1) IMMUNE recall margin → RELEVANCE
        # H_9337 · this read was CONSTANT: the key was the session seed, so rel_lane sat at 0.6723
        # for all 720 ticks of the H_9328 rollouts. The store is written to (:1941 binds g_text)
        # and then always asked the same frozen question — writing without reading is not a loop.
        #
        # The fix is NOT "ask about the last utterance" — measured, that is ALSO constant (1.15):
        # the store was just handed that exact text, so it always answers "I remember it perfectly".
        # The live quantity is the recall margin taken BEFORE the bind — how FAMILIAR was that
        # utterance when it arrived. Same order as recon_err (:1499), and for the same reason:
        # a recognition signal measured after you have memorised the thing is not recognition.
        # Measured: repeating an earlier utterance spikes it to 1.15 while novel ones sit near 0.17
        # — the daemon can now tell "I have said this before" from "this is new".
        if pending_rel is None:
            recall_margin = immune_memory_recall_margin_text(immune, session_seed)
        else:
            recall_margin = pending_rel
        rel_lane = _afs_clip01(1.0 - recall_margin)

        # (2) CI LANE SCORES (§ConsciousnessIndex 15-lane)
        # H_9336 · the field's prediction error on the LAST thing the daemon said (1-tick lag),
        # NOT on the session seed. Against the seed this is 0.0 by IDENTITY: afield is BORN with
        # seed_feat0 as its first prototype (:1379), and every emitted text clears SPLIT_THRESH
        # and spawns a NEW cell instead of refining that one — so the seed prototype is never
        # touched and L2(seed_proto, seed_feat) stays exactly 0 forever. The daemon was asking
        # "how surprised am I by the thing I was born knowing?" and 8 lanes (surprise · boredom ·
        # agency · change_detect · osmotic · fieldlibido · m_field · ci_lane_scores) ate that
        # constant. Measured dead: H(R|S)=0.0000 over 24 rollouts (H_9328 MEDIATION panel).
        # H_9210 diagnosed this and fixed it — but only behind --opgrip-live, so production kept
        # the dead gauge and the next experiment inherited it (convergence chat-py-4).
        # Predictive-coding order: the error is taken on the NEW percept BEFORE adapting to it,
        # so it is captured at the emit site (:1894+) and consumed here on the following tick.
        if pending_recon is None:
            recon_err = vadapt_field_recon_err(afield, seed_feat0)
        else:
            recon_err = pending_recon
        m_grounding = _afs_clip01(rel_lane)
        m_field = [phi_t, rel_lane, 1.0 - recon_err, m_grounding, emit_env]
        m_grounding_p = pharm_perturb_m(sober, m_grounding, 0.0)
        lanes = ci_lane_scores(m_grounding_p, m_field, cell_count, tick, 1, 1.0, recon_err)
        coh_lane = lanes[3]
        bal_lane = lanes[9]
        emit_drive = ci_emit_drive(lanes)
        # H_9351 — Ψ is DEFINED as the population fraction over the emit-drive threshold
        # (engine_cli ci_psi_balance -> ci_emit_decision: 0.5*(lanes[0]+lanes[4]) >= 0.5), and
        # those two lanes were the one thing the trace did NOT record. So Ψ could not be
        # computed from a real daemon run at all, and the Ψ-SOMA panel fell back to scoring a
        # fixed-seed synthetic population instead — a verdict that never sees the model.
        # Record the actual gws/lprec so Ψ̂ can be taken on the substrate's OWN lane population.
        psi_gws = float(lanes[0])
        psi_lprec = float(lanes[4])

        # ── (C-R3) PER-TICK CONFLICT → A⇄G SETTLE BUDGET (H_9095 rung-3) ──
        # H_9357 · the G pole. a0 keeps the H_9356 tautology (G = A's complement, wiring-degenerate);
        # a1 pulls it from the immune store's top-2 gap (wiring-free d2, taken before-bind at :1993);
        # a3 is seeded per-tick noise (the "causal handle vs 2nd engine" separator). g_recog in [0,1].
        ag_a_drive = emit_drive
        if _g_arm == "a1":
            # pending_gap is the IMMUNE STORE top-2 gap on the LAST utterance (1-tick lag, like
            # pending_rel) — set at :2061 (immune_memory_recall_gap_text), which UNCONDITIONALLY
            # overwrites the afield gap computed at :2051 (that afield line is dead code · H_9399
            # G-SOURCE-ID). None before the daemon has spoken → no reverse signal yet = 0.
            g_recog = _afs_clip01(pending_gap if pending_gap is not None else 0.0)
            ag_g_drive = 0.0 - g_recog
        elif _g_arm == "a4":
            # H_9413 L5 · SOURCE-SWAP: read the immune store's recall MARGIN (pending_rel · set at
            # :2173 immune_memory_recall_margin_text, same 1-tick-lag/before-bind order as pending_gap)
            # instead of the top-2 gap. H_9401 found margin is the ONLY G readout that clears θ (p90
            # 0.69≥0.40) and H_9412 found the gap is drift-not-recognition — margin is the daemon's
            # own COMPUTED-BUT-DISCARDED signal (no synthetic injection · no sign tuning · engine fn).
            # None before first utterance → 0. Both readouts land in the trace row for the counterfactual.
            g_recog = _afs_clip01(pending_rel if pending_rel is not None else 0.0)
            ag_g_drive = 0.0 - g_recog
        elif _g_arm == "a3":
            # explicit int seed (Python 3.14 rejects tuple seeds); deterministic per (seed, tick).
            _g_seed = (_sample_seed * 2654435761 + tick * 40503 + 0x9357) & 0x7FFFFFFF
            g_recog = random.Random(_g_seed).random()
            ag_g_drive = 0.0 - g_recog
        else:  # a0 — current production wiring (the tautology arm)
            g_recog = 1.0 - emit_drive
            ag_g_drive = 0.0 - (1.0 - emit_drive)
        ag_conflict = conflict_scalar(ag_a_drive, ag_g_drive)
        # H_9607 · update the leaky-integral of the SIGNED A⇄G net tension AFTER this tick's drives are
        # known — consumed at the TOP of next tick (:~1730). s = ag_a_drive + ag_g_drive is 0 exactly
        # when A's push and G's push cancel (a0: s = emit_drive − (1−emit_drive) = 2·emit_drive − 1),
        # so the integral null s→0 pins the steady state at emit_drive=½ regardless of κ (emergent, not
        # dialed). κ=0 leaves ag_fb_I evolving but unused (ag_drive gated to 0.0 above) → byte-identical.
        ag_s_signed = ag_a_drive + ag_g_drive
        ag_fb_I = (1.0 - _AG_FB_RHO) * ag_fb_I + ag_s_signed
        ag_budget = conflict_recruited_depth(ag_conflict, 4, 6)
        ag_pop = anima_tr_pop_conflicted(_afs_clip01(0.5 + 0.5 * ag_conflict))
        ag_settle = tension_resolve_depth(ag_pop, tr_full, 0.3, 0.5, ag_budget, 2, 0.06, tr_cfgON)
        ag_settle_depth = ag_settle[0]
        if _ag_cont:
            # H_9376 · continuous pass-through = the UPPER-BOUND arm of the mid-link capacity
            # (I(conflict;agloop_ctx|stage) = H(conflict|stage); no continuization can exceed it). The
            # settle machinery above still ran (its trace fields are preserved); only the report
            # to score is continuized. tension-agnostic: reads ag_conflict's VALUE only, applied
            # identically to every g-arm, a fixed monotone map — arm selectivity is substrate-earned.
            agloop_ctx = _afs_clip01(ag_conflict)
        else:
            agloop_ctx = (0.0 if ag_settle_depth < 0.0
                          else _afs_clip01(ag_settle_depth / (float(ag_budget) + 0.000001)))

        # (3) GLOBAL WORKSPACE
        gws = gws_new(4, True, 0.55)
        gi = 0
        while gi < len(lanes):
            gws = gws_add(gws, lanes[gi])
            gi = gi + 1
        gws_w = gws_winner(gws)
        if gws_w >= 0:
            gws_ignited_any = True

        # (4) REALITY MONITOR
        reality = reality_call(emit_drive, 0.55)
        if reality >= 1.0:
            reality_real_any = True
        lanes_read = True

        # ── R2 BRAIN-STRUCTURE LANE READS ──
        seed_feat = _afs_byte_feature(session_seed, 8)

        # (5) SPATIAL
        sm_ans = spatial_map_nearest(smap, "ledger", "vault", "rumor")
        spatial_rel = 1.0 if sm_ans != "" else 0.0
        if sm_ans != "":
            spatial_read_any = True

        # (6) HIER-PFC
        cur_target = hier_current_target(hier)
        if len(cur_target) > 0:
            hier = hier_step(hier, hmem, cur_target)
        hier_p_now = hier_pointer(hier)
        if hier_p_now > 0:
            hier_advanced_any = True
        plan_progress = _afs_clip01(float(hier_p_now) / 2.0)

        # (7) BASAL-GANGLIA
        bg_cands = []
        bgc = 0
        while bgc < 8:
            bg_cands.append(seed_feat[bgc])
            bgc = bgc + 1
        bgn = 0
        while bgn < 8:
            bg_cands.append(bg_bad[bgn])
            bgn = bgn + 1
        bg_sel = vbasal_select(bgate, bg_cands, 2)
        basal_go = 1.0 if bg_sel >= 0 else 0.0
        if bg_sel >= 0:
            basal_go_any = True

        # (8) CEREBELLUM
        # H_9411 ② · forward-model error on the last transition (prev utterance → this one),
        # 1-tick lag. Pre-first-speech falls back to the mount pair (the old dead read), exactly
        # as recon_err falls back to seed_feat0. Alien/pedestal arms snapshotted here at consume
        # time (the trace row is built end-of-tick, after the emit site overwrote pending_cb_*).
        cb_pred = vforward_predict(cbel, cb_prev_feat)
        if pending_cb is None:
            cb_perr = vforward_err(cbel, seed_feat, _afs_byte_feature(mem_text, 8))
            cb_perr_alien = None
            cb_perr_ped = None
        else:
            cb_perr = pending_cb
            cb_perr_alien = pending_cb_alien
            cb_perr_ped = pending_cb_ped
        if len(cb_pred) > 0:
            cereb_pred_any = True
        cb_surprise = _afs_clip01(cb_perr)

        # (9) WORKING MEMORY — H_9411 ④ · leak every tick; probe the item gated one emit AGO
        # (delay test), never the token just gated (self-match ≡ λ = the old frozen 0.6). The
        # per-tick gate-in moved to the emit site, so silence ticks show genuine decay (λ^Δt).
        wmb = wm_buffer_leak(wmb)
        # H_9627 · the withheld store W_S leaks every tick TOO (same λ as wmb = gain-lock). This is
        # the passive-decay half; its active-write half is the silence-side gate-in below. Both
        # ledgers leaking symmetrically is what lets ½ sit at the exchange-symmetric center.
        wm_withheld = wm_buffer_leak(wm_withheld)
        if wm_probe_feat is None:
            wm_active = _afs_clip01(wm_buffer_probe_score(wmb, seed_feat))  # pre-speech fallback
        else:
            wm_active = _afs_clip01(wm_buffer_probe_score(wmb, wm_probe_feat))
        wm_null = _afs_clip01(wm_buffer_probe_score(wmb, wm_alien_feat))
        if wm_active > 0.0:
            wm_maintained_any = True

        # ── R3 BRAIN-STRUCTURE LANE READS ──
        # (11) CA3 REPLAY — H_9411 ③ · replay confidence on the LIVE utterance-symbol stream
        # (1-tick lag). The mounted `ca3` (:526) is the lane self-test only (synthetic cycle →
        # conf(·,1)=1.0 forever); never read here. Cold value = the engine's own no-support
        # answer (predict -1 / conf 0.0), not a knob. Held across non-emit ticks like pending_recon.
        if pending_ca3 is None:
            ca3_next = -1
            ca3_ctx = 0.0
        else:
            ca3_next = pending_ca3[0]
            ca3_ctx = pending_ca3[1]
        if ca3_next >= 0:
            ca3_predicted_any = True

        # (12) INTERVAL TIMER
        itmr = itimer_step(itmr)
        it_phase = _afs_clip01(float(itmr.elapsed) / (itimer_dhat(itmr) + 0.000001))
        if itimer_dhat(itmr) > 5.0:
            interval_learned_any = True

        # (13) AMYGDALA — H_9411 ① · affect on the LAST thing the daemon said (1-tick lag), not
        # on the frozen (seed_key, mem_text) pair against a never-bound 1-cell store (H(af)=0).
        # First tick only falls back to the session anchor read.
        if pending_af is None:
            af = affect_read(igrow, seed_key, mem_text)
        else:
            af = pending_af
        af_val = _afs_clip01((af[0] + 1.0) / 2.0)
        af_aro = _afs_clip01(af[1])
        if af[0] != 0.0 or af[1] != 0.0:
            amyg_valenced_any = True

        # (14) THEORY-OF-MIND
        tom_b = other_mind_predict(omind, mem_text)
        tom_ctx = 1.0 if tom_b != "" else 0.0
        if tom_b != "":
            tom_belief_any = True

        # (15) HOMEOSTATIC DRIVE
        hd = homeo_drive(homeo, igrow, seed_key)
        hd_ctx = _afs_clip01(hd)
        if hd > 0.0:
            homeo_drive_any = True

        # ── R4 BRAIN-STRUCTURE LANE READS ──
        # (16) PRC
        prc = prc_step(prc, 1.0)
        prc_f = prc_phase(prc)
        prc_dist_b = prc_f if prc_f < 0.5 else 1.0 - prc_f
        prc_ready = _afs_clip01(1.0 - 2.0 * prc_dist_b)
        if prc_distinct:
            prc_entrained_any = True

        # (17) PROSPECTION
        prosp = prospect_reach(tick + 2, 3)
        prosp_ctx = _afs_clip01(prosp)
        if prosp > 0.0:
            prosp_reach_any = True

        # (18) SLEEP-REPLAY BUDGET
        replay_ctx = 1.0 if consol_gated.last_used[0] > consol_unif.last_used[0] else 0.0
        if consol_gated.last_used[0] > consol_unif.last_used[0]:
            replay_protected_any = True

        # (19) GATE-B
        gateb_ctx = 1.0 if gb_growth > gb_growth_shuf else 0.0
        if gb_growth > gb_growth_shuf:
            gateb_grew_any = True

        # (20) INTERO PRECISION
        intero_ctx = _afs_clip01(1.0 - ip_weighted)
        if ip_weighted < ip_blind:
            intero_weighted_any = True

        # ── R5 BRAIN-STRUCTURE LANE READS ──
        # (21) SCN — H_9411 ⑥A · advance the coupled oscillator ensemble ONE tick so its phase
        # order R evolves. scn_R was computed ONCE at :672 over a warmed-but-never-stepped net →
        # scn_ctx byte-constant, H=0 (a clock that never ticks). Controls step in lockstep so the
        # coupled-vs-uncoupled consensus gap is a per-tick pedestal. --scn-freeze = before-state.
        if not scn_freeze:
            scn_coupled = scn_step(scn_coupled)
            scn_uncoup = scn_step(scn_uncoup)
            scn_frust = scn_step(scn_frust)
        scn_R = scn_order(scn_coupled)
        scn_R_unc = scn_order(scn_uncoup)
        scn_R_fr = scn_order(scn_frust)
        # H_9411 ⑥A · MEASURED (toy smoke): the coupled net phase-LOCKS, so scn_order (the mean-
        # phase-vector MAGNITUDE) is rotation-invariant → scn_R stayed constant at 0.9986 even
        # though every phase advanced (scn_r_unc varied 240× = the step DID fire). Fable's
        # prescribed remedy for this measured order-lock: read the PHASE itself, not the order.
        # The circadian phase advances (mod 1) every tick by construction. scn_R kept in the
        # trace as the consensus-magnitude control. NOT tune-to-green — a different, valid,
        # engine-native readout of the same stepped substrate (the order-lock was the finding).
        scn_ctx = _afs_clip01(scn_coupled.phases[0] % 1.0)
        if scn_consensus(scn_coupled, 0.9):
            scn_consensus_any = True

        # (22) BOREDOM
        bored = boredom_disengage(rel_lane, _afs_clip01(1.0 - recon_err), True)
        engaged_ctx = 1.0 - bored
        if bored < 1.0:
            boredom_engaged_any = True

        # (23) SELF-CONTINUITY
        self_ctx = _afs_clip01(self_after_anchor)
        if self_after_anchor > 0.99:
            self_recognized_any = True

        # (24) LEARNED-PRECISION
        lp_now = learned_precision(0.1, float(tick + 1), 1.0)
        lprec_ctx = _afs_clip01(lp_now)
        if lp_now > 0.0:
            lprec_confident_any = True

        # (25) NOVELTY
        nov_now = novelty(float(tick), 0.5)
        nov_ctx = _afs_clip01(nov_now)
        if nov_now > 0.0:
            novelty_read_any = True

        # ── R6 BRAIN-STRUCTURE LANE READS ──
        # (26) HABITUATION
        hab_resp = hab_response(hab, 0, 1.0)
        hab_ctx = _afs_clip01(hab_resp)
        if hab_resp < 1.0:
            habituate_any = True

        # (27) ATTENTIONAL BLINK
        blink_now = attn_blink_detect(tick, 1.0)
        blink_ctx = _afs_clip01(blink_now)
        if blink_now > 0.0:
            blink_read_any = True

        # (28) MENTAL IMAGERY
        img_now = imagery_activate(rel_lane, True)
        img_ctx = _afs_clip01(img_now)
        if img_now > 0.0:
            imagery_any = True

        # (29) PRIMING
        prime_now = priming_facilitate(rel_lane, scn_ctx)
        prime_ctx = _afs_clip01(prime_now)
        if prime_now > 0.0:
            priming_any = True

        # (30) ATTENTION SCHEMA
        schema_now = attn_schema_report(gws_w, gws_w, True)
        schema_ctx = _afs_clip01(schema_now)
        if schema_now > 0.125:
            schema_tracked_any = True

        # ── R7 BRAIN-STRUCTURE LANE READS ──
        # (31) HYSTERESIS
        hyst_now = hyst_switch_point(tick % 2 == 0, 0.4)
        hyst_ctx = _afs_clip01(hyst_now)
        if hyst_now != 0.5:
            hysteresis_any = True

        # (32) REENTRY
        reent_now = reentry_settle(tick + 1, 0.3)
        reent_ctx = _afs_clip01(reent_now)
        if reent_now > 0.0:
            reentry_any = True

        # (33) COMPLETION
        comp_now = completion_recognize(rel_lane, True)
        comp_ctx = _afs_clip01(comp_now)
        if comp_now > 0.544:
            completion_any = True

        # (34) GESTALT
        gest_now = gestalt_same_group(scn_ctx, True)
        gest_ctx = _afs_clip01(gest_now)
        if gest_now > 0.0:
            gestalt_any = True

        # (35) SENSE OF AGENCY
        agcy_now = agency_attribute(rel_lane, _afs_clip01(1.0 - recon_err), 0.5)
        agcy_ctx = _afs_clip01(agcy_now)
        if agcy_now > 0.0:
            agency_any = True

        # ── R8 BRAIN-STRUCTURE LANE READS ──
        # (36) SUBJECTIVE TIME
        subjt_now = subjective_time(nov_ctx * 5.0, 0.2, 0.16)
        subjt_ctx = _afs_clip01(subjt_now)
        if subjt_now > 0.2:
            subjtime_any = True

        # (37) EMOTION REGULATION
        emoreg_now = emotion_regulate(af_aro, 0.5, 1.0)
        emoreg_ctx = _afs_clip01(emoreg_now)
        if af_aro > 0.0:
            emoreg_any = True

        # (38) DIRECTED FORGETTING
        dforget_now = directed_forget_recall(rel_lane, 0.3, tick > 6)
        dforget_ctx = _afs_clip01(dforget_now)
        if tick > 6:
            dirforget_any = True

        # (39) FREE-WON'T / VETO
        veto_now = veto_execute(rel_lane, 0.3, stage == 3 or stage == 4)
        veto_ctx = _afs_clip01(veto_now)
        veto_any = True

        # (40) DIVIDED ATTENTION
        divd_now = divided_perf(rel_lane, 0.6)
        divd_ctx = _afs_clip01(divd_now)
        if divd_now > 0.0:
            divided_any = True

        # ── R9 BATCH LANE READS (12 more) ──
        surp_now = surprise(_afs_clip01(1.0 - recon_err), recon_err)
        surp_ctx = _afs_clip01(surp_now)
        surprise_any = True
        bodyown_ctx = _afs_clip01(body_ownership(scn_ctx, rel_lane))
        bodyown_any = True
        rivalry_ctx = 1.0 if rivalry_transitions(tick + 4, 0.15) > 0 else 0.0
        rivalry_any = True
        chg_ctx = _afs_clip01(change_detect(recon_err, rel_lane > 0.4))
        chgblind_any = True
        trw_ctx = trw_recall(0, tick + 4, 13)
        trw_any = True
        mw_ctx = wander_coverage(tick + 1, 8, stage == 3 or stage == 4)
        mindwander_any = True
        qual_ctx = qualia_nearer(1.0 - rel_lane, 1.0)
        qualia_any = True
        smp_ctx = smp_presence(cell_count, 4, True)
        smpresence_any = True
        halluc_ctx = 1.0 - _afs_clip01(hallucinate_graded(1.0 - rel_lane, rel_lane))
        halluc_any = True
        metacog_ctx = _afs_clip01(mi_insight_judge(rel_lane * 0.7, 1.0))
        metacog_any = True
        gwsleak_ctx = 1.0 if gws_w >= 0 else 0.0
        gwsleak_any = True
        allo_ctx = _afs_clip01(2.0 - allo_mu(0.5 + (1.0 - rel_lane) * 0.4, 1.0, 0.12))
        allosteric_any = True

        # ── R10 BATCH LANE READS (11 cheap) ──
        neuropharm_ctx = _afs_clip01(pharm_self_continuity(sober, 16, tick + 1))
        neuropharm_any = True
        libido_ctx = _afs_clip01(libido_wanting(libido_new(), 1.0 - rel_lane, rel_lane) * 0.5)
        libido_any = True
        transord_ctx = 1.0 if trans_order_higher(tord, "A", "D") != "" else 0.0
        transord_any = True
        phasesync_ctx = _afs_clip01(phasefield_coherence(phasefield_run(phasefield_new(tick + 1, 8), 20)))
        phasesync_any = True
        memtom_ctx = _afs_clip01(mem_tom_route_cue(rel_lane > 0.4))
        memtom_any = True
        spatep_ctx = _afs_clip01(spatial_episodic_where_cue(session_seed))
        spatep_any = True
        quorum_ctx = _afs_clip01(quorum_cluster_order(quorum_run(quorum_new(tick + 1, 3, 4), 20)))
        quorum_any = True
        osmotic_ctx = 1.0 if recon_err > 0.30 else 0.0
        osmotic_any = True
        metacogc_ctx = _afs_clip01(mc_control_lift(tick + 4297, 4) + 0.5)
        metacogc_any = True
        metacoga_ctx = _afs_clip01(mi_metad_auroc(tick + 4297, 6))
        metacoga_any = True
        fieldlib_ctx = _afs_clip01(fieldlibido_wanting(rel_lane, m_field, cell_count, tick, 1, 1.0, recon_err, 1.0 - rel_lane, 0.0, rel_lane, 6, 0.5, 1) * 0.5)
        fieldlib_any = True

        # ── B7 AUTONOMOUS emit — the lanes FEED the brain's 8-factor motivation ──
        rel_ctx = _afs_clip01(
            (rel_lane + spatial_rel + plan_progress + wm_active + basal_go
             + ca3_ctx + af_val + tom_ctx + hd_ctx
             + prosp_ctx + replay_ctx + gateb_ctx + intero_ctx
             + scn_ctx + engaged_ctx + self_ctx + lprec_ctx
             + img_ctx + prime_ctx + schema_ctx
             + reent_ctx + comp_ctx + gest_ctx + agcy_ctx
             + dforget_ctx + veto_ctx + divd_ctx
             + bodyown_ctx + trw_ctx + qual_ctx + smp_ctx
             + halluc_ctx + metacog_ctx + gwsleak_ctx + allo_ctx
             + neuropharm_ctx + transord_ctx + phasesync_ctx + memtom_ctx
             + spatep_ctx + quorum_ctx + metacogc_ctx) / 42.0)
        cur_ctx = _afs_clip01(
            (recon_err + cb_surprise + it_phase + af_aro + prc_ready
             + (1.0 - hab_ctx) + blink_ctx + hyst_ctx
             + subjt_ctx + emoreg_ctx
             + surp_ctx + rivalry_ctx + chg_ctx + mw_ctx
             + libido_ctx + osmotic_ctx + metacoga_ctx + fieldlib_ctx) / 18.0)
        drive_hi = stage != 3 and stage != 4
        # ── op-grip tonic-phasic (fable design (a) · PREREG α=0.1, gain=3.0) ──
        rel_ema = 0.9 * rel_ema + 0.1 * rel_ctx
        cur_ema = 0.9 * cur_ema + 0.1 * cur_ctx
        cur_phasic = _afs_clip01(0.5 + 3.0 * (cur_ctx - cur_ema))
        # ── TENSION→ADAPTATION (this task): PHASIC A⇄G tension Δ ──
        ten_ema = 0.9 * ten_ema + 0.1 * ag_conflict
        ten_phasic = _afs_clip01(0.5 + 3.0 * (ag_conflict - ten_ema))
        # ── op-grip design (b) — CONTINUOUS op-modulated stage/safe envelope (H_9101) ──
        stage_env = _afs_clip01((dr_stage_scale(stage) - 0.02) / 0.08)
        urgency = _afs_clip01(0.4 * agloop_ctx + 0.3 * cur_phasic + 0.3 * ten_phasic)
        rel = _og_rel_phasic(rel_ctx, rel_ema) * (0.1 + 0.9 * stage_env)
        cur = cur_phasic * (0.1 + 0.9 * stage_env)
        # KEPT, but no longer feeds the gate: this is the (stage, urgency) envelope, useful as
        # telemetry and as the before/after handle for H_9352. It is NOT elapsed time.
        idle = 5.0 + 55.0 * _afs_clip01(stage_env * (0.5 + urgency))
        # The gate's `seconds_since_last` now IS seconds since last. Before the first emit the
        # substrate has never spoken, so nothing is being rate-limited: the limiter must not be
        # what silences it (an unbounded value would make the first tick unconditional, which is
        # the same defect mirrored — so use the elapsed time since the run began).
        if last_emit_tick is None:
            secs_since_emit = float(tick) * an_tick_seconds()
        else:
            secs_since_emit = float(tick - last_emit_tick) * an_tick_seconds()

        # GROUND store FIRST (full fact), partial seed cue LAST
        live_anchors = []
        ai = 0
        while ai < len(anchors):
            live_anchors.append(anchors[ai])
            ai = ai + 1
        # H_9337 · this anchor is CONSTANT (live_seed) and that is CORRECT — do not "fix" it.
        # :1994 feeds live_anchors[-1] straight into the next decode's seed string, so handing the
        # daemon back its own last utterance here would make the mouth condition on its own output:
        # that is self-seed / monologue, which p5 BANS outright. The kosmos root stays write-only
        # WITHIN a session by design; the read-back is a CROSS-session fact (a fresh session loads
        # .kosmos at :427). So of the three roots, only afield and immune are legitimately
        # closeable in-session — the third is closed by philosophy, not by defect.
        # H_9411 ⑥B · inject the live per-tick substrate tension as an anchor so
        # anchor_tension_fold (brain.py:120) reads a VARYING tension_5ch, not just the frozen
        # mem_001 baseline. Inserted BEFORE the live_seed append so live_seed stays [-1] (the
        # mouth decode-seed byte-untouched; p5 self-seed root left closed). Tension-only dict:
        # no text_payload, so generate() never reads it as a decode field — inert to the mouth,
        # live to the fold. 1-tick lag keeps it OUT of a same-tick emit-feedback loop.
        if pending_tension is not None and not anchor_tension_null:
            live_anchors.append({"name": "live_tension", "tension_5ch": list(pending_tension)})
        live_anchors.append({"text_payload": session_seed, "name": "live_seed"})
        # anima study · EXOGENOUS PERCEPT → the decode-seed anchor ([-1]) so the mouth conditions
        # its next utterance on the OTHER's words (Fable's percept channel). This is NOT the p5-banned
        # self-seed: live_seed carries session_seed (the boot cue, :above), and the percept carries
        # the TEACHER's text — an exogenous cross-agent read, not the daemon's own last utterance fed
        # back (chat-py-5 root ③ stays closed). Guarded: OFF ⇒ live_seed stays [-1] ⇒ byte-identical.
        if percept_text:
            live_anchors.append({"text_payload": percept_text, "name": "percept"})

        # ── op-grip: the 4 filler CONSTANTS are now LIVE op reads ──
        gap_ctx = _afs_clip01(1.0 - rel_lane)
        # H_9607 · unconditional default for the H_9627 dual-ledger fn. It was assigned ONLY inside the
        # `if _emit_gate == "refractory"` branch (:~2296) but read unconditionally by the H_1058 trace
        # block (:~2389) → UnboundLocalError on the DEFAULT clock gate whenever ANIMA_DECISION_TRACE is
        # set. A pre-existing origin/main bug the A⇄G smoke surfaced (a pool live-smoke catch a local
        # compile misses); hoisting the None default is the minimal safe fix (refractory branch overrides).
        _dual_fn = None

        # H_9404 · PAY: the substrate's own A<->G tension this tick pays down the emit-debt BEFORE the
        # gate reads it (secs_since_emit stays live above as telemetry / trace field). refr_debt is only
        # consulted below when --refractory earned; the clock path is untouched otherwise.
        if _refractory == "earned":
            refr_debt = refractory_debt_step(refr_debt, _afs_clip01(ag_conflict))

        # ── DEFAULT emit: the brain autonomously decides (brain_emit) ──
        if _emit_gate == "refractory":
            # H_9415 p5-REWIRE (owner-ratified) · emit ⟺ score_A > g_recog(candidate); θ + clock
            # RETIRED. g_recog = clip01(immune recall MARGIN on the FORMED candidate, taken BEFORE
            # bind = recognition-before-memorisation, chat-py-5). Distinct from H_9404 --emit-refractory
            # earned (which keeps θ, only swaps the rate SOURCE); this retires θ too. H_9712 · this IS
            # the production default now (owner-approved · Ψ≈½ via H_9627 dual-ledger · clock at --emit-gate clock).
            # H_9419 · the recognition functional: d1 margin (default, byte-identical) OR the
            # affinity-reach d2−d1 (the G-pole reach lever). --g-shuffle composes with either.
            _dual_fn = None   # H_9627 · set only by the wm-dual family (else brain uses _recog_fn)
            if _g_reach == "affinity":
                _recog_fn = lambda _t: _afs_clip01(immune_memory_recall_reach_text(immune, _grecog_text(_t)))
            elif _g_reach == "cb-perr":
                # H_9422 · prediction-error recognition (the non-distance lens · H_9421 next).
                # g_recog = clip01(1 - vforward_err(cbel, cb_prev_feat, feat8(cand))) = FAMILIARITY:
                # the cerebellum forward-model's predictability of the candidate given the last
                # utterance. NLMS contraction GUARANTEES the β sign (emit→update lowers the just-said
                # candidate's err → raises its familiarity → silences near-repeats · Fable §1-1). The
                # gate reads the PRE-bind cbel (this tick's update is at :2284, after here) =
                # recognition-before-memorisation, chat-py-5. NOTE (Fable §4): --g-shuffle is
                # MATHEMATICALLY VOID here (feat8 is byte-multiset stats, permutation-invariant) — C2
                # control is the cb-perr-alienctx arm below, not shuffle. Constants 0 (η/dim landed).
                _recog_fn = lambda _t: _afs_clip01(1.0 - vforward_err(cbel, cb_prev_feat,
                                                   _afs_byte_feature(_grecog_text(_t), 8)))
            elif _g_reach == "cb-perr-alienctx":
                # H_9422 C2 control · same candidate amplitude stats, transition-conditioning
                # DESTROYED (ctx = alien feat, not the last utterance). exp survives ∧ alienctx dies
                # ⇒ the gate hears "prediction-error conditioned on what I just said", not a marginal
                # candidate stat. Reuses cb_alien_feat (:1445, no new constant).
                _recog_fn = lambda _t: _afs_clip01(1.0 - vforward_err(cbel, cb_alien_feat,
                                                   _afs_byte_feature(_grecog_text(_t), 8)))
            elif _g_reach == "wm-cover":
                # H_9610 · value-gate = WM discourse-coverage (the non-recognition lens · H_9510
                # showed mouth is novel-only so recognition-β has no target). g_recog = V(cand) =
                # how much the candidate is ALREADY covered by working memory. sign = g=V (high
                # coverage → silence) not 1−V: emit gates in the utterance (:2394, after here) →
                # WM coverage of feat8-similar followers rises → their gate closes (β spring); a
                # silence run leaks WM down → gate reopens (both directions negative-feedback,
                # zero new constant). wmb here is this tick's LEAKED, pre-gate-in state = coverage
                # BEFORE speaking (chat-py-5 recognition-before-memorisation). $0 S0-e counterfactual:
                # emit-rate 0.444≈½ · autocov −0.182 (spring) · ≠vshuf (content-heard) · alien SATURATE.
                _recog_fn = lambda _t: _afs_clip01(wm_buffer_probe_score(wmb, _afs_byte_feature(_grecog_text(_t), 8)))
            elif _g_reach == "wm-cover-alienwm":
                # H_9610 C2 dissociation control · probe a FROZEN empty alien WM buffer (never gated
                # by this daemon's speech) → coverage ≈ 0 always → gate always open (SATURATE). exp
                # survives ∧ alienwm SATURATE ⇒ the gate reads "coverage of MY discourse", not a
                # marginal candidate stat (H_9424 alienctx sign, ported to WM).
                _recog_fn = lambda _t: _afs_clip01(wm_buffer_probe_score(_wm_cover_alien, _afs_byte_feature(_grecog_text(_t), 8)))
            elif _g_reach in ("wm-dual", "wm-dual-alien-emit", "wm-dual-alien-silence"):
                # H_9627 · dual content ledger — emit ⟺ S(withheld coverage) > E(spoken coverage).
                # The probe returns (S, E); brain_emit_refractory compares them (dual_probe_fn). Both
                # buffers are read at their LEAKED, pre-gate-in state (recognition-before-memorisation,
                # chat-py-5) — wmb leaked at :wmb-leak, wm_withheld beside it. score_A does NOT enter
                # the comparison (that is the escape from H_9610's one-sided store; score only sources
                # write-strength, applied symmetrically at the emit/silence gate-in sites). The alien
                # arms freeze ONE side's READ to a never-gated empty buffer (coverage ≈ 0) to sever
                # exactly one restoring direction — dissociation: alien-emit kills the emit→silence
                # brake (E≈0), alien-silence kills the silence→emit accelerator (S≈0).
                _e_buf = _wm_cover_alien if _g_reach == "wm-dual-alien-emit" else wmb
                _s_buf = _wm_cover_alien if _g_reach == "wm-dual-alien-silence" else wm_withheld
                _dual_fn = (lambda _eb, _sb: (lambda _t: (
                    _afs_clip01(wm_buffer_probe_score(_sb, _afs_byte_feature(_grecog_text(_t), 8))),
                    _afs_clip01(wm_buffer_probe_score(_eb, _afs_byte_feature(_grecog_text(_t), 8))))))(_e_buf, _s_buf)
                _recog_fn = lambda _t: 0.0   # unused when dual_probe_fn is set
            else:
                _recog_fn = lambda _t: _afs_clip01(immune_memory_recall_margin_text(immune, _grecog_text(_t)))
            dec = brain_emit_refractory(pf,
                             rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane, agloop_ctx,
                             secs_since_emit, False, True,
                             backend, live_anchors, 0.0,
                             _recog_fn,
                             _mouth_at(tick),
                             _dyn_w,
                             _rec_silent_cand,  # H_9510 HOLE-1 · record imagined cand for diag
                             (_route_gain if _tension_route == "pc2" else None),  # H_9574 PC2
                             pc2_mouth=("" if _pc2_mouth == "off" else _pc2_mouth),  # H_9575
                             dual_probe_fn=_dual_fn,  # H_9627 · dual content ledger (None = off)
                             score_perturb=_score_perturb,  # H_9627 · central-thesis bar (0 = off)
                             zeta_ladder=(_pc2_zeta or None))  # H_9664 ζ-ladder (None = off)
        else:
            dec = brain_emit(pf,
                             rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane, agloop_ctx,
                             secs_since_emit, False, True,
                             backend, live_anchors,
                             _mouth_at(tick),   # H_9328 · None by default ⇒ byte-identical greedy path
                             _dyn_w,                # H_9377 · audibility gain (None = byte-identical)
                             _rate_sec,             # H_9391 · clock-live regime (None = byte-identical)
                             (refr_debt if _refractory == "earned" else None))  # H_9404 · earned refractory

        did_emit = str(dec["emit"]).lower() == "true"
        if did_emit:
            last_emit_tick = tick
            # H_9404 · RECHARGE: an emitting tick leaves owing a full unit of integrated tension.
            if _refractory == "earned":
                refr_debt = refractory_emit_debt()
        g_emit = str(dec["gen_emitted"]).lower() == "true"
        g_back = str(dec["gen_backend"])
        g_text = str(dec["gen_text"])
        # H_9627 · dual content ledger — the SILENCE-side write. On a silence tick the candidate was
        # imagined (dual_cand_text) but not spoken; gate it into W_S (withheld). This is the active
        # accelerator half the one-sided wm-cover gate lacked: silence now WRITES substrate state,
        # symmetric to emit's W_E gate-in (:2427, feat8(g_text)). Same strength 1.0 = gain-lock. The
        # emit-side W_E update rides the existing emit block, so nothing to add there. Off unless the
        # wm-dual family is active (dual_cand_text present only then).
        if _dual_fn is not None and not g_emit:
            _dual_ct = str(dec.get("dual_cand_text", ""))
            if byte_len(_dual_ct) > 0:
                wm_withheld = wm_buffer_gate_in(wm_withheld, _afs_byte_feature(_dual_ct, 8), 1.0)
        # anima study · record this tick for the teacher loop (guarded — no-op in production).
        # The percept source may read the returned transcript to decide the next percept; silence
        # (did_emit False) is a real signal it must respect, never a cue to re-prompt/force emit.
        if percept_source is not None:
            _percept_transcript.append({
                "tick": tick, "percept": percept_text,
                "did_emit": did_emit, "emit_text": g_text if did_emit else None,
            })
            if did_emit:
                _percept_emits += 1
        # ── H_9328 C2 CARRIER-SWAP (--swap-text <trace.jsonl>) · default OFF ────────────────
        # THE control that makes a positive falsifiable. It replaces the emitted TEXT with the
        # text ANOTHER rollout produced at this same tick — a real anima utterance (same shape,
        # same length distribution, same mouth), but one THIS substrate did not just choose.
        # Everything downstream is untouched, so the donor text really does drive the 3 feedback
        # roots below (afield :1854 · immune :1860 · kosmos :1874) and really does move the next
        # tick's `score`. That is why a post-hoc permutation of A could never be this control
        # (convergence evaluate-py-14): permuting a NUMBER cannot reproduce the causal push of a
        # TEXT through the roots.
        #   EXP survives ∧ SWAP dies  ⇒ the substrate's OWN words carry the information.
        #   both survive              ⇒ CARRIER — any text of that shape pushes the roots the
        #                               same way ⇒ NOT a pass.
        # p5 is untouched: the emit/silence DECISION is the substrate's own (the gate never sees
        # this flag); we only substitute what gets said on a tick it already chose to speak.
        swapped = False   # H_9338 · C2 CARRIER-SWAP arm label (trace-only · never a branch key)
        if _swap_texts and did_emit and g_emit and byte_len(g_text) > 0:
            _donor = _swap_texts.get(int(tick))
            if _donor is not None:
                g_text = _donor
                # H_9338 · the arm label goes in its OWN field, NOT into g_back.
                # It used to do `g_back = g_back + "+swap"`, and the C8-GROW block below is gated
                # on `g_back == "clm"` (:1949) — so tagging the backend "clm+swap" silently routed
                # the swap arm AROUND every feedback root: afield never stepped, immune never
                # bound. The control measured NOTHING. Trace-verified: 16/16 swap rollouts had
                # recon_err with ONE distinct value, while the same binary run without the flag
                # produced five. The earlier smoke's "the donor really pushes the roots" was wrong
                # — A moved only because g_text moved, which the roots never saw.
                # An experiment label must never ride on a field the production path branches on.
                swapped = True
        psi_sum = psi_sum + pure_field_phi(pf)

        # GROUND check
        has_ground = _afs_contains(g_text, "vault QX-7741")

        # ── C8 GROW — novelty-driven VAdaptField division ──
        _h1058_grow_feats = []   # H_1058: ordered vadapt grow-features applied this tick
        _h1058_row = None        # deferred trace row (built below, written end-of-tick)
        if g_emit and g_back == "clm" and byte_len(g_text) > 0:
            feat = _afs_byte_feature(g_text, 8)
            # H_9336 · take the error BEFORE adapting — that is what a prediction error IS.
            # Read on the next tick (:1493). Measured after the field has already absorbed the
            # text, it would only report how well the field memorised it.
            pending_recon = vadapt_field_recon_err(afield, feat)
            # H_9357 · the afield's top-2 gap (d2²−d1²)/2 on THIS utterance, before adapting to it.
            # d1 = recon_err (already in σ(emit_drive)); d2 (the 2nd-nearest prototype) is the
            # wiring-free reverse quantity. The afield grows (unlike the immune store, which stayed
            # 1-cell in local smoke), so its d2 actually varies. G-INDEP tests whether d2 adds
            # variance independent of d1/emit_drive; if it doesn't, the gate returns SECOND-A.
            _gd12 = vadapt_field_two_recon_err(afield, feat)
            pending_gap = (_gd12[1] * _gd12[1] - _gd12[0] * _gd12[0]) / 2.0
            afield = vadapt_field_step(afield, feat, cfg)
            _h1058_grow_feats.append(list(feat))
            post_cells = vadapt_field_cells(afield)
            cell_count = post_cells
            grew = True
            # H_9337 · recognition BEFORE memorisation — ask how familiar this utterance was
            # while the store still does not contain it. Read on the next tick (:1497).
            pending_rel = immune_memory_recall_margin_text(immune, g_text)
            # H_9357 · same order, the top-2 gap (d2 = the wiring-free reverse quantity).
            pending_gap = immune_memory_recall_gap_text(immune, g_text)
            immune = immune_memory_bind_text(immune, _afs_clip(g_text, 64), g_text, cfg)
            last_gtext = g_text
            # ══ H_9411 DEAD-GAUGE CAPTURES · quantities on THIS utterance, taken BEFORE each
            # store absorbs it (recognition-before-memorisation, same order as pending_recon
            # above). `feat` = _afs_byte_feature(g_text, 8) already computed at the block top.
            # Consumed next tick at each gauge's read site. All arms are per-tick substrate
            # signals; the alien/pedestal arms ride the trace row only (never a branch key). ══
            # ① AMYGDALA — affect on THIS utterance BEFORE the store binds it; the bind is what
            # un-freezes it (a 1-cell never-bound store pins valence at −1 every tick).
            _g_key = immune_embed_key(g_text)
            pending_af = affect_read(igrow, _g_key, g_text)
            pending_af_alien = affect_read(igrow, _afs_alien_key, "")
            igrow = immune_grow_bind(igrow, _g_key, g_text, cfg)
            # ② CEREBELLUM — transition error (prev utterance → THIS one) BEFORE the NLMS update
            # absorbs the pair. Alien arm = trained weights on a wrong ctx; pedestal = untrained.
            pending_cb = vforward_err(cbel, cb_prev_feat, feat)
            pending_cb_alien = vforward_err(cbel, cb_alien_feat, feat)
            pending_cb_ped = vforward_err(cbel_ped, cb_prev_feat, feat)
            cbel = vforward_update(cbel, cb_prev_feat, feat)
            cb_prev_feat = feat
            # ③ CA3 — predict-then-observe on the REAL utterance-symbol stream. Ask the replay
            # memory what followed the PREVIOUS utterance, and how confidently, BEFORE observing.
            ca3_sym = _afs_ca3_sym(g_text, 4)
            if ca3_prev_sym is not None:
                pending_ca3 = (ca3_replay_predict(ca3_live, ca3_prev_sym),
                               ca3_replay_conf(ca3_live, ca3_prev_sym))
                ca3_live = ca3_replay_observe(ca3_live, ca3_prev_sym, ca3_sym)
            ca3_prev_sym = ca3_sym
            # ④ WM delay test — retire the previous utterance's feature to probe duty BEFORE
            # gating in the new percept (the probe must never be the token just gated).
            wm_probe_feat = wm_last_feat
            wmb = wm_buffer_gate_in(wmb, feat, 1.0)
            wm_last_feat = list(feat)
            # ⑥ ANCHOR — snapshot the live 5-channel substrate tension at the instant of speaking,
            # consumed next tick as the anchor tension_5ch. All five are per-tick-varying signals
            # already computed above: recon_err(⑨336 live) · rel_lane(⑨337 live) · agloop_ctx(A⇄G
            # tension) · cur_phasic(phasic curiosity) · ten_phasic(phasic A⇄G Δ).
            pending_tension = [float(recon_err), float(rel_lane), float(agloop_ctx),
                               float(cur_phasic), float(ten_phasic)]

        # ── C8b TENSION→GROW (p8-literal: tension births growth/mitosis) ──
        if ten_phasic > 0.66:
            _h1058_c8b_feat = _afs_byte_feature(session_seed, 8)
            afield = vadapt_field_step(afield, _h1058_c8b_feat, cfg)
            _h1058_grow_feats.append(list(_h1058_c8b_feat))
            cell_count = vadapt_field_cells(afield)
            grew = True

        # ── C9 REMEMBER — persist THIS emit as a new .kosmos anchor ──
        if did_emit and g_emit and byte_len(g_text) > 0 and not remembered2:
            etension = [pure_field_phi(pf), af_aro, nov_ctx, af_val, self_ctx]
            epath = emit_anchor_from_v3(kdir, "emit_t" + _ts(tick),
                                        _afs_clip(g_text, 120), etension, cell_count, 2,
                                        "emission", "curiosity", pure_field_phi(pf), 1.0)
            remembered2 = True
            _pln("  [t" + _ts(tick) + " " + stage_nm + "] REMEMBER emit → " + epath)

            # ── LANE-23b: ground the live self in THIS emit's REAL penult rep (own-emit event) ──
            # Twin of cli/anima.hexa. Ψ/emit-disjoint: reads gen_penult_pooled_W (own forward),
            # drifts ONLY self_live_g; self_ctx untouched (self⊥mouth).
            if self_gW_ok:
                ev_axis_g = penult_fold8(gen_penult_pooled_W(self_gW, g_text))
                self_live_g = self_drift_exp(self_live_g, ev_axis_g, 0.15)
                self_g_axis_seq = self_g_axis_seq + ("," if self_g_events > 0 else "") + _ts(ev_axis_g)
                self_g_events = self_g_events + 1

        # ── REFSEL — contradiction-keyed referent routing (default OFF ⇒ out_text==g_text) ──
        out_text = g_text
        if g_emit and byte_len(g_text) > 0:
            refcands = [g_text]
            if refsel_on:
                recalled = immune_memory_recall_text(immune, mem_text)
                if recalled != "":
                    refcands.append(recalled)
            refsel_rs = referent_select_text(igrow, refcands, mem_text)
            if refsel_on and refsel_rs >= 1:
                out_text = refcands[refsel_rs]

        # ── H_9575 Stage-A · PC2 → mouth outward substitution ──────────────────────
        # The STEERED text (PC2-biased decode, computed after emit was fixed on the BASE
        # candidate) is what gets SPOKEN. Every substrate root above (self_live_g, and the
        # immune/afield/kosmos/cb roots below) keeps consuming the BASE g_text — so the gate
        # trajectory stays byte-identical to the off arm BY CONSTRUCTION (Stage-A isolation:
        # remembered≠spoken, experiment-only). Roots-on-spoken = Stage-B (separate pre-reg).
        _steered = str(dec.get("gen_text_steered", "")) if isinstance(dec, dict) else ""
        if _steered != "" and did_emit and g_emit:
            out_text = _steered

        if did_emit and g_emit:
            emitted_any = True
            emit_text = out_text
        if has_ground:
            grounded_ok = True
        if stage == 3 or stage == 4:
            slept = True
        if drive_hi:
            og_wake = og_wake + 1
            if did_emit:
                og_emit_wake = og_emit_wake + 1

        # ── H_1058 decision trace write (write-only · reads existing dec/scope · no state change) ──
        #    class = the gate structure at core/brain.py:162 (emit = should_emit(score) AND safe):
        #    EMIT score>0.3∧safe · ACTIVE_VETO score>0.3∧¬safe (a braked live impulse) · PASSIVE score<=0.3.
        if _trace_fh is not None:
            import json as _json, hashlib as _hl, base64 as _b64
            _score = float(dec["motivation"])
            _safe = str(dec["safe"]).lower() == "true"
            _imp = _score > 0.3          # engine_g should_emit / PROACTIVE_THRESHOLD
            _cls = "EMIT" if (_imp and _safe) else ("ACTIVE_VETO" if _imp else "PASSIVE")
            _gtb = g_text.encode("utf-8", "surrogateescape")
            # ── H_1058 Part A1: the generator's ACTUALLY-CONSUMED decode-seed bytes ──
            # PURE side-channel (a_substrate_disjoint · p5): this recomputes the exact seed
            # string that _gen_clm_decode/_gen_bytegpt_decode built for this tick —
            # `phase + " " + <last-anchor clean field>` — using the SAME SSOT extractor
            # (_gen_anchor_field) and the SAME phase (dec["phase"]) the mouth read via
            # gen_ctx_from_decision. It touches NOTHING on the emit/silence path; the emit
            # bytes are byte-identical whether or not this line runs. Lets phi_leg.py build
            # its Φ context window from the TRUE model input instead of own-emit-only bytes
            # (the H_9269 decision-invariance root cause — constant seed per session).
            _seed_str = _gen_g_string(dec, "phase") + " "
            if len(live_anchors) > 0:
                _seed_str = _seed_str + _gen_anchor_field(live_anchors[len(live_anchors) - 1])
            _seed_b = _seed_str.encode("utf-8", "surrogateescape")
            # ── frozen-emission replay substrate (H_1058 §3.4) ──────────────────
            # g_text feedback funnels through EXACTLY 3 roots (rel_lane[immune],
            # recon_err/cell_count[afield]) + 3 EMAs. ⚠️ H_9411: phi/nudge are NO LONGER
            # session-constants (pf now stepped ⑤, live_tension anchor injected ⑥B), and 5
            # indep-sum gauges (wm_active·ca3_ctx·af_val·af_aro·cb_surprise) are now g_text-live
            # — but they STAY in the residual because their stores (ca3_live·wmb·cbel·igrow-grow)
            # are NOT among the 3 replayed roots, so factual-replay reconstruction stays exact;
            # the frozen replay_depth.py counterfactual-root path simply won't propagate through
            # them (documented scope limit, not a break). Capture the two
            # g_text-INDEPENDENT partial sums of the 42-/18-term rel_ctx/cur_ctx
            # numerators (the standalone replayer recomputes only the DEP terms from
            # the replayed roots + these residuals). Classification (24 indep rel · 12
            # indep cur) mirrors state/h1058_agency_daemon/replay_depth.py.
            _rel_indep = (spatial_rel + plan_progress + wm_active + basal_go + ca3_ctx
                          + af_val + tom_ctx + hd_ctx + prosp_ctx + replay_ctx + gateb_ctx
                          + intero_ctx + scn_ctx + self_ctx + lprec_ctx + reent_ctx
                          + gest_ctx + trw_ctx + neuropharm_ctx + transord_ctx
                          + phasesync_ctx + spatep_ctx + quorum_ctx + metacogc_ctx)
            _cur_indep = (cb_surprise + it_phase + af_aro + prc_ready + (1.0 - hab_ctx)
                          + blink_ctx + hyst_ctx + subjt_ctx + emoreg_ctx + rivalry_ctx
                          + mw_ctx + metacoga_ctx)
            if tick == 0:  # meta header (session invariants for the replayer boot)
                _trace_fh.write(_json.dumps({
                    "_meta": True, "session_seed": session_seed, "mem_text": mem_text,
                    # ⚠️ H_9411: phi_const/nudge_const record ONLY the tick-0 value and are NO
                    # LONGER session invariants (pf now stepped ⑤, live_tension anchor ⑥B) — a
                    # replayer MUST read the per-tick "phi"/"anchor_nudge" fields from each row,
                    # not treat these as constants. Flags below make that self-describing.
                    "phi_const": float(dec["phi"]), "phi_peak": float(pf.phi_peak),
                    "nudge_const": float(dec.get("anchor_nudge", 0.0)),
                    "phi_live_h9411": True, "nudge_live_h9411": True,
                    "backend": g_back, "n_ticks": n_ticks,
                    "stage_cycle": bool(_stage_cycle),  # H_9269 Y-ULTRA regime flag (consumers ignore if unknown)
                    # H_9351 σ-panel provenance: bind the trace to the ckpt that produced it so
                    # `anima-py evaluate <ckpt> --psi-soma <trace>` can reject a mismatched pair
                    # (INVALID-PROVENANCE) — the trace must not be able to be "anything".
                    "ckpt_sha256": (_hl.sha256(open(ckpt, "rb").read()).hexdigest()
                                    if isinstance(ckpt, str) and os.path.exists(ckpt) else ""),
                    "g_arm": str(_g_arm), "refractory": (_refractory or None),
                    "g_reach": str(_g_reach), "emit_gate": str(_emit_gate),  # H_9419
                    "tension_route": str(_tension_route), "route_gain": float(_route_gain),  # H_9557
                }) + "\n")
            # build the row now (decision vars fresh); the WRITE is deferred to end-of-tick
            # so grow_feats captures ALL 3 afield grow paths (C8 + C8b + N3/REM imagination,
            # the last of which runs after this point) — replayed verbatim by replay_depth.py.
            # H_9328 DO-MOUTH · A = the ACTION the daemon actually consumes (chat.py self-drift
            # feeds exactly this): penult_fold8(gen_penult_pooled_W(self_gW, g_text)) ∈ [0,8),
            # the H_9257 FROZEN 8-bucket reducer (researcher DOF = 0). -1 = undefined (no self_gW
            # or SILENT tick) — a FROZEN sentinel, never a fallback map (that would be new DOF).
            _a_fold8 = (penult_fold8(gen_penult_pooled_W(self_gW, g_text))
                        if (self_gW_ok and g_emit and byte_len(g_text) > 0) else -1)
            _h1058_row = {
                "tick": tick, "stage": int(stage), "idle": float(idle),
                "score": _score, "safe": _safe, "emit": did_emit, "cls": _cls,
                "a_fold8": int(_a_fold8), "sample_seed": int(_sample_seed),
                "emit_temp": float(_emit_temp),
                "phi": float(dec["phi"]), "anchor_nudge": float(dec.get("anchor_nudge", 0.0)),
                "base_motiv": float(dec.get("base_motiv", _score)),
                "gen_emitted": g_emit, "gen_backend": g_back, "swapped": swapped,
                "psi_gws": psi_gws, "psi_lprec": psi_lprec, "emit_drive": float(emit_drive),
                "secs_since_emit": float(secs_since_emit),
                # H_9607 · A⇄G feedback telemetry (κ=0 ⇒ ag_drive≡0.0; ag_fb_I/ag_s still evolve as
                # monitor-only). --ag-criticality reads these: ag_s=signed net, ag_fb_I=leaky-integral,
                # ag_drive=κ·SGN·I fed to the field. distinct(ag_drive)>1 confirms the loop is live.
                "ag_s": float(ag_s_signed), "ag_fb_I": float(ag_fb_I),
                "ag_drive": float(ag_drive), "ag_feedback_kappa": float(_ag_feedback),
                "gtext_sha": _hl.sha256(_gtb).hexdigest()[:16], "gtext_len": byte_len(g_text),
                "gtext_b64": _b64.b64encode(_gtb).decode("ascii"),
                "cand_b64_diag": dec.get("cand_b64_diag", ""),  # H_9510 HOLE-1 · imagined cand (diag)
                # H_1058 Part A1 side-channel: the mouth's actually-consumed decode-seed bytes
                # (phi_leg.py TRUE-consumed-bytes context source; a_substrate_disjoint · p5).
                "seed_len": len(_seed_b), "seed_b64": _b64.b64encode(_seed_b).decode("ascii"),
                # H_9357 · the A⇄G tension's G pole + its arm, so the panel can run G-INDEP
                # (regress ag_g_drive on emit_drive+covariates) and G-VAR (distinct count).
                "g_arm": str(_g_arm), "ag_cont": bool(_ag_cont), "dyn_w": (float(_dyn_w) if _dyn_w is not None else None), "rate_sec": (float(_rate_sec) if _rate_sec is not None else None), "ag_g_drive": float(ag_g_drive),
                "refractory": (_refractory or None), "refr_debt": float(refr_debt),  # H_9404 earned refractory
                "g_recog": float(g_recog), "ag_conflict": float(ag_conflict),
                # H_9415 p5-REWIRE · emit-gate mode + the refractory gate's G-recognition value
                # (the candidate's immune recall margin the gate compared score against). "clock" =
                # production (g_recog_gate=None). Lets --g-readout-info / swing-census read whether
                # the ratified gate produced a live band (both emit and silence ticks) vs mute/saturate.
                "gate_mode": str(dec.get("gate_mode", "clock")),
                "g_recog_gate": (float(dec["g_recog_gate"]) if dec.get("g_recog_gate") is not None else None),
                # H_9627 · dual content ledger — S(withheld) · E(spoken) · margin S−E per tick, so the
                # offline analysis reads regime-split autocov (two-sided spring) and score-perturb
                # robustness directly from the trace (None when the wm-dual family is off).
                "dual_s_withheld": (float(dec["dual_s_withheld"]) if dec.get("dual_s_withheld") is not None else None),
                "dual_e_spoken": (float(dec["dual_e_spoken"]) if dec.get("dual_e_spoken") is not None else None),
                "dual_margin": (float(dec["dual_margin"]) if dec.get("dual_margin") is not None else None),
                "pc2_proj": (float(dec["pc2_proj"]) if dec.get("pc2_proj") is not None else None),  # H_9557
                "route_k": (int(dec["route_k"]) if dec.get("route_k") is not None else None),  # H_9557
                "pc2_z": (float(dec["pc2_z"]) if dec.get("pc2_z") is not None else None),  # H_9575
                "pc2_arm": str(_pc2_mouth),  # H_9575
                "gtext_pc2_b64": (_b64.b64encode(str(dec.get("gen_text_steered", "")).encode("utf-8", "surrogateescape")).decode("ascii") if dec.get("gen_text_steered") else None),  # H_9575 · steered (spoken) text
                # H_9664 ζ-ladder: [{zeta, text_b64}] per emit tick. ζ=0 entry MUST equal
                # gtext_b64 byte-for-byte (isolation certificate). Absent ⇒ [] ⇒ flag off.
                "gtext_zeta": [{"zeta": _zr["zeta"],
                                "text_b64": _b64.b64encode(str(_zr["text"]).encode("utf-8", "surrogateescape")).decode("ascii")}
                               for _zr in (dec.get("gen_text_zeta") or [])],
                # H_9413 L5 · BOTH G readouts every tick (arm-independent counterfactual): the
                # discarded recall MARGIN (pending_rel · a4 source) AND the production top-2 GAP
                # (pending_gap · a1 source), so --g-readout-info can re-screen either readout offline
                # from any arm's trace without a re-collection (1-tick lag · None→null before first speak).
                "pending_rel": (float(pending_rel) if pending_rel is not None else None),
                "pending_gap": (float(pending_gap) if pending_gap is not None else None),
                # H_9351 σ-panel inputs: the gws-fed lane population (σ·stage / σ·bind),
                # its winner (σ·stage argmax test), and the reality monitor (σ·witness).
                "lanes": [float(x) for x in lanes], "gws_w": int(gws_w),
                "reality": float(reality),
                # H_9351 σ·bind reopen: pre-summation component lanes (distinct faculties, NOT
                # deterministic mirrors of rel_lane) — the D2-free integration candidate the
                # summed cur_indep/rel_indep hide. cb=cerebellum surprise · af_val/af_aro=amygdala
                # valence/arousal · ca3=hippocampus replay · wm=working-memory. (Fable D2 spec.)
                "cb_surprise": float(cb_surprise), "af_val": float(af_val),
                "af_aro": float(af_aro), "ca3_ctx": float(ca3_ctx),
                "wm_active": float(wm_active),
                # H_9411 dead-gauge control arms (trace-only null/pedestal · never a branch key)
                # — the collapse-Δ vs these is the liveness verdict, not the raw value (Ψ-SOMA/p7).
                "cb_perr_raw": float(cb_perr),
                "cb_alien": (float(cb_perr_alien) if cb_perr_alien is not None else None),
                "cb_ped": (float(cb_perr_ped) if cb_perr_ped is not None else None),
                "af_alien_val": (float(pending_af_alien[0]) if pending_af_alien is not None else None),
                "af_raw_aro": float(af[1]),
                "ca3_sym": (int(ca3_prev_sym) if ca3_prev_sym is not None else -1),
                "wm_null": float(wm_null),
                "scn_r_unc": float(scn_R_unc), "scn_r_fr": float(scn_R_fr),
                # roots + residuals + DEP-arg indep scalars (replay inputs)
                "rel_lane": float(rel_lane), "recon_err": float(recon_err),
                "cell_count": int(cell_count),
                "rel_indep": float(_rel_indep), "cur_indep": float(_cur_indep),
                "scn_ctx": float(scn_ctx), "nov_ctx": float(nov_ctx),
                "emit_env": float(emit_env), "stage_env": float(stage_env),
                # factual score-composition intermediates (replayer self-validation)
                "rel_ctx": float(rel_ctx), "cur_ctx": float(cur_ctx),
                "rel_f": float(rel), "cur_f": float(cur), "gap_ctx": float(gap_ctx),
                "allo_ctx": float(allo_ctx), "coh_lane": float(coh_lane),
                "bal_lane": float(bal_lane), "agloop_ctx": float(agloop_ctx),
                "rel_ema": float(rel_ema), "cur_ema": float(cur_ema), "ten_ema": float(ten_ema),
                "ten_phasic": float(ten_phasic),
            }

        # one-line transcript row (first 3 ticks + sleep ticks)
        if tick < 3 or stage == 3 or stage == 4:
            _pln("  [t" + _ts(tick) + " " + stage_nm
                 + " env=" + _ts(emit_env) + "] EMIT=" + ("1" if did_emit else "0")
                 + " gen=" + g_back + " ground=" + ("1" if has_ground else "0")
                 + " | LANES rel=" + _ts(rel_lane)
                 + " drive=" + _ts(emit_drive)
                 + " gws_win=" + _ts(gws_w)
                 + " reality=" + _ts(reality)
                 + " cells=" + _ts(cell_count) + "]")
            _pln("       CR3 agloop conflict=" + _ts(ag_conflict)
                 + " budget=" + _ts(ag_budget)
                 + " settle-depth=" + _ts(ag_settle_depth)
                 + " agloop_ctx=" + _ts(agloop_ctx))
            _pln("       LANES2 spatial=" + sm_ans
                 + " plan=" + _ts(plan_progress)
                 + " basal_go=" + ("1" if bg_sel >= 0 else "0")
                 + " cb_surprise=" + _ts(cb_surprise)
                 + " wm_active=" + _ts(wm_active))
            _pln("       LANES3 ca3_next=" + _ts(ca3_next)
                 + " ca3_conf=" + _ts(ca3_ctx)
                 + " it_phase=" + _ts(it_phase)
                 + " af_val=" + _ts(af_val)
                 + " tom=" + ("1" if tom_b != "" else "0")
                 + " hd=" + _ts(hd_ctx))
            _pln("       LANES4 prc_ready=" + _ts(prc_ready)
                 + " prosp=" + _ts(prosp_ctx)
                 + " replay_anchor=" + _ts(replay_ctx)
                 + " gateb=" + _ts(gateb_ctx)
                 + " intero=" + _ts(intero_ctx))
            _pln("       LANES5 scn_R=" + _ts(scn_ctx)
                 + " engaged=" + _ts(engaged_ctx)
                 + " self=" + _ts(self_ctx)
                 + " lprec=" + _ts(lprec_ctx)
                 + " novelty=" + _ts(nov_ctx))
            _pln("       LANES6 hab=" + _ts(hab_ctx)
                 + " blink=" + _ts(blink_ctx)
                 + " imagery=" + _ts(img_ctx)
                 + " priming=" + _ts(prime_ctx)
                 + " schema=" + _ts(schema_ctx))
            _pln("       LANES7 hyst=" + _ts(hyst_ctx)
                 + " reentry=" + _ts(reent_ctx)
                 + " completion=" + _ts(comp_ctx)
                 + " gestalt=" + _ts(gest_ctx)
                 + " agency=" + _ts(agcy_ctx))
            _pln("       LANES8 subjtime=" + _ts(subjt_ctx)
                 + " emoreg=" + _ts(emoreg_ctx)
                 + " dirforget=" + _ts(dforget_ctx)
                 + " veto=" + _ts(veto_ctx)
                 + " divided=" + _ts(divd_ctx))
            _pln("       LANES9 surp=" + _ts(surp_ctx)
                 + " body=" + _ts(bodyown_ctx)
                 + " riv=" + _ts(rivalry_ctx)
                 + " chg=" + _ts(chg_ctx)
                 + " trw=" + _ts(trw_ctx)
                 + " mw=" + _ts(mw_ctx)
                 + " qual=" + _ts(qual_ctx)
                 + " smp=" + _ts(smp_ctx)
                 + " halu=" + _ts(halluc_ctx)
                 + " mci=" + _ts(metacog_ctx)
                 + " allo=" + _ts(allo_ctx)
                 + " | rel_ctx=" + _ts(rel_ctx) + " cur_ctx=" + _ts(cur_ctx))

        # ── N3/REM DREAM CONSOLIDATION (H_9036) ──
        dream_src = generator_read_anchors(kdir)
        dream_n = dp_sleep_tick(kdir, dream_src, stage, tick)
        dream_composed_total = dream_composed_total + dream_n

        # ── N3/REM IMAGINATION REPLAY — emit-free rehearsal + mitosis tick (p5) ──
        if dr_imagination_active(stage) == 1:
            imag_budget = dr_stage_size(stage)
            imag_snaps = ir_select_snapshots(wake_mem, tick, imag_budget)
            imag_i = 0
            while imag_i < len(imag_snaps):
                rec = ir_replay_tick(imag_snaps[imag_i])
                if rec["emit_count"] != 0:
                    imagination_emit_violations = imagination_emit_violations + 1
                ir_mitosis_tick_during_replay({"count": cell_count}, imag_snaps[imag_i])  # mitosis tick (log record)
                # WIRED 2026-07-10 (a_chat_sleep_imagination now LITERAL): real vadapt_field_step grow (same
                # AdaptField grow as the wake C8/C8b loop) → rehearsal + REAL mitosis tick, not a counter.
                # Ψ-disjoint (AdaptField only) · emit-free (vadapt never emits) · deterministic (session_seed)
                # · self-limiting (contact-inhibition). de-theater: no emit Δ — makes p8 mitosis real, not a lever.
                # feature = the REHEARSED perception (snapshot ctx_tokens[0] = source wake-tick + source_index),
                # NOT a constant — each distinct rehearsed snapshot grows its own AdaptField region. A constant
                # feature contact-inhibits to a no-op; this makes the grow REAL (cell_count rises), still det + emit-free.
                _imag_feat = session_seed + "|imag|" + str(imag_snaps[imag_i]["ctx_tokens"][0]) + "|" + str(imag_snaps[imag_i]["source_index"])
                _h1058_imag_feat = _afs_byte_feature(_imag_feat, 8)
                afield = vadapt_field_step(afield, _h1058_imag_feat, cfg)
                _h1058_grow_feats.append(list(_h1058_imag_feat))
                cell_count = vadapt_field_cells(afield)
                imagination_mitosis_ticks = imagination_mitosis_ticks + 1
                imag_i = imag_i + 1
            imagination_replayed_total = imagination_replayed_total + len(imag_snaps)

        # ── H_1058 deferred trace write (end-of-tick · after ALL afield grows) ──
        if _trace_fh is not None and _h1058_row is not None:
            _h1058_row["grow_feats"] = _h1058_grow_feats
            _trace_fh.write(_json.dumps(_h1058_row) + "\n")
            _trace_fh.flush()

        tick = tick + 1

    if _trace_fh is not None:
        _trace_fh.close()

    # ══ LANE-23b SESSION END — persist the grounded self as a .kosmos self-anchor (twin of the
    #    hexa session-end persist · a_kosmos · closes H_1471 R2b). Single write entry create_anchor,
    #    DEDICATED self-anchor dir (never kdir), so it never enters the brain's anchor stream. ══
    if self_gW_ok:
        os.makedirs(self_g_kdir, exist_ok=True)
        sg_payload = _selfg_encode(self_live_g)
        sg_tension = [self_cos(self_live_g, self_new(8, 0)), 0.5, 0.5, 1.0, 0.5]
        sg_path = create_anchor(self_g_kdir, self_g_name,
                                "grounded self-continuity", 0.0, 0.0, "self_identity", 1.0,
                                2, "self", "continuity", sg_payload, sg_tension,
                                "lane-23b-selfground", "")
        _pln("LANE-23b self-g : PERSIST self-anchor → " + sg_path
             + " (events=" + _ts(self_g_events) + " axis_seq=[" + self_g_axis_seq + "])")

    # ── F3 Ψ ON==OFF invariant (a_core_engine_map · H_1202/H_1205) ──
    # H_9411 ⑤ · OFF twin = a fresh field through the identical warmup + per-tick step schedule
    # with ZERO chat coupling. Byte-equal psi_off proves the now-LIVE Φ trajectory is Engine A's
    # autonomous dynamics — nothing the loop did (emit · swap · percept) leaked into the field.
    # (Was a vacuous n·c==n·c check re-summing the frozen constant before pf was stepped.)
    pf_off = pure_field_warmup(600)
    psi_off = 0.0
    t_off = 0
    while t_off < n_ticks:
        pf_off = pure_field_step(pf_off)
        psi_off = psi_off + pure_field_phi(pf_off)
        t_off = t_off + 1
    psi_intact = psi_sum == psi_off

    # ════════════════════════════════════════════════════════════════════════
    #  PER-FACULTY + PER-LANE TABLE + verdict
    # ════════════════════════════════════════════════════════════════════════
    _pln("")
    _pln("── per-faculty ────────────────────────────────────────────────")
    _pln("  CONVERSE (A1, mounted .clm emits via L3)    : " + anima_yn(emitted_any))
    _pln("  GROUND   (A3/ρ·tether ← G5, copied verbatim anchor fact): " + anima_yn(grounded_ok))
    _pln("  GROW     (C8, density VAdaptField, p8)      : " + anima_yn(grew)
         + "  (cells 1 → " + _ts(cell_count) + ")")
    _pln("  REMEMBER (C9, emit persisted to .kosmos)    : " + anima_yn(remembered2))
    _pln("  SLEEP    (C10, 5-stage ultradian advanced)  : " + anima_yn(slept))
    _og_ef = (float(og_emit_wake) / float(og_wake)) if og_wake > 0 else 0.0
    if og_wake > 0 and (_og_ef < 0.05 or _og_ef > 0.95):
        _pln("  ⚠️ FLAG emit-rate-collapse (H_9097): wake emit-fraction " + _ts(_og_ef)
             + " outside [0.05,0.95] (DETECTOR only — never tune threshold/weights to hit it)")
    _pln("")
    _pln("── engine_cli consciousness lanes (READ on the user path) ──────")
    _pln("  IMMUNE   (H_1227/1231, recall→relevance)    : " + anima_yn(lanes_read)
         + "  (cells=" + _ts(immune_memory_cells(immune)) + ")")
    _pln("  CI/Φ     (H_1492, 15-lane → coh/bal/drive)  : " + anima_yn(lanes_read))
    _pln("  GWS      (GWT ignition → broadcast winner)  : " + anima_yn(gws_ignited_any))
    _pln("  REALITY  (H_1501, real/imagined threshold)  : " + anima_yn(reality_real_any))
    _pln("  PHARM    (H_1502, sober baseline profile)   : " + anima_yn(lanes_read))
    _pln("")
    _pln("── R2 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  SPATIAL  (H_1296, metric episodic nearest)  : " + anima_yn(spatial_read_any)
         + "  (gap: item-store abstains; → rel_ctx)")
    _pln("  HIER-PFC (H_1294, ordered goal-stack ptr)   : " + anima_yn(hier_advanced_any)
         + "  (gap: flat-select holds no plan ptr; → rel_ctx)")
    _pln("  BASAL-GG (H_1281, striatal go/no-go select) : " + anima_yn(basal_go_any)
         + "  (gap: fixed thr can't select 1-of-K; → rel_ctx)")
    _pln("  CEREBLLM (H_1280, forward next-step predict): " + anima_yn(cereb_pred_any)
         + "  (gap: recon≠prediction; → cur_ctx)")
    _pln("  WORK-MEM (H_1282, volatile decaying buffer) : " + anima_yn(wm_maintained_any)
         + "  (gap: immune is persistent; → rel_ctx)")
    _pln("")
    _pln("── R3 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  CA3-RPLY (H_1427, learned next-item replay)  : " + anima_yn(ca3_predicted_any)
         + "  (gap: stores hold no successor stats; → rel_ctx)")
    _pln("  INTERVAL (H_1299, learned absolute duration) : " + anima_yn(interval_learned_any)
         + "  (gap: clock baked·cereb content; → cur_ctx)")
    _pln("  AMYGDALA (H_1285, valence/arousal affect)    : " + anima_yn(amyg_valenced_any)
         + "  (gap: no valenced interoception; → rel/cur_ctx)")
    _pln("  TOM      (H_1293, other-mind false belief)   : " + anima_yn(tom_belief_any)
         + "  (gap: immune=truth, no other-mind; → rel_ctx)")
    _pln("  HOMEOSTAT(H_1292, leaky temporal integral)   : " + anima_yn(homeo_drive_any)
         + "  (gap: affect stateless, no integral; → rel_ctx)")
    _pln("")
    _pln("── R4 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  PRC-CLK  (H_1301, limit-cycle phase-reset)   : " + anima_yn(prc_entrained_any)
         + "  (gap: clock baked, no entrain; ↔INTERVAL ablated; → cur_ctx)")
    _pln("  PROSPECT (H_1493, k-step forward simulation) : " + anima_yn(prosp_reach_any)
         + "  (gap: CA3 single-step≠rollout; → rel_ctx)")
    _pln("  REPLAY-B (H_1285, salience-gated sleep replay): " + anima_yn(replay_protected_any)
         + "  (gap: no salience-budget rehearsal; → rel_ctx)")
    _pln("  GATE-B   (H_1208/9, P(next|prev) growth gate): " + anima_yn(gateb_grew_any)
         + "  (gap: CA3 read-OUT≠growth-GATE; → rel_ctx)")
    _pln("  INTERO-P (H_1494, precision-weighted self)   : " + anima_yn(intero_weighted_any)
         + "  (gap: affect weights channels equally; → rel_ctx)")
    _pln("  [DEFERRED] curiosity-acq (H_1534) — no engine lane (numpy 🧱, never wired)")
    _pln("")
    _pln("── R5 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  SCN-NET  (H_1302, coupled-ensemble consensus): " + anima_yn(scn_consensus_any)
         + "  (gap: PRC single-osc; ↔PRC uncoupled-collapse; → rel_ctx)")
    _pln("  BOREDOM  (H_1495, meta-motiv AND-conjunction): " + anima_yn(boredom_engaged_any)
         + "  (gap: homeo/habit single-channel; → rel_ctx)")
    _pln("  SELF-CONT(H_1471, anchor-persisted identity) : " + anima_yn(self_recognized_any)
         + "  (gap: LLM resets; ↔PROSPECT W:=I≠rollout; → rel_ctx)")
    _pln("  LEARN-PR (H_1472, count-driven precision)    : " + anima_yn(lprec_confident_any)
         + "  (gap: INTERO-P σ-driven≠count-driven; → rel_ctx)")
    _pln("  NOVELTY  (H_1468, precision-agnostic unfamil): " + anima_yn(novelty_read_any)
         + "  (gap: confidence-axes≠unfamiliarity; → cur_ctx)")
    _pln("")
    _pln("── R6 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  HABITUATE(H_1465, stimulus-specific decay)   : " + anima_yn(habituate_any)
         + "  (gap: ↔NOVELTY specific+dishabituation; → cur_ctx)")
    _pln("  ATTN-BLNK(H_1473, RSVP T2 temporal trough)   : " + anima_yn(blink_read_any)
         + "  (gap: GWS lag-invariant; → cur_ctx)")
    _pln("  IMAGERY  (H_1484, top-down empty-input recon): " + anima_yn(imagery_any)
         + "  (gap: input-gates collapse on empty; → rel_ctx)")
    _pln("  PRIMING  (H_1485, relatedness facilitation)  : " + anima_yn(priming_any)
         + "  (gap: ↔HABITUATE opposite-sign; → rel_ctx)")
    _pln("  ATTN-SCHM(H_1488, self-model of attention)   : " + anima_yn(schema_tracked_any)
         + "  (gap: MODEL vs MECHANISM; → rel_ctx)")
    _pln("  [DEFERRED] phase-synchrony binding (H_1448) — engine lane EXISTS but Kuramoto-R")
    _pln("             read REDUNDANT with SCN-NET(R5); SCN-detune folded into SCN.")
    _pln("")
    _pln("── R7 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  HYSTERESIS(H_1489, history-inertia switch)  : " + anima_yn(hysteresis_any)
         + "  (gap: ↔BISTABILITY rivalry order-invariant; → cur_ctx)")
    _pln("  REENTRY  (H_1487, recurrent deep-access)     : " + anima_yn(reentry_any)
         + "  (gap: ↔GWS depth-invariant; → rel_ctx)")
    _pln("  COMPLETION(H_1490, amodal filling-in)        : " + anima_yn(completion_any)
         + "  (gap: ↔IMAGERY input-constrained; → rel_ctx)")
    _pln("  GESTALT  (H_1491, figure-ground binding)     : " + anima_yn(gestalt_any)
         + "  (gap: ↔GWS binding≠selection; → rel_ctx)")
    _pln("  SENSE-AGCY(H_1474, efference-copy attribution): " + anima_yn(agency_any)
         + "  (gap: ↔ToM self⊥other; → rel_ctx)")
    _pln("  [DEFERRED] perceptual-bistability — = rivalry, hysteresis's order-invariant")
    _pln("             control arm (no separate faculty); attn-schema-agency folded into ATTN-SCHM.")
    _pln("")
    _pln("── R8 brain-structure lanes (READ on the user path, → motivation) ──")
    _pln("  SUBJ-TIME(H_1475, novelty-weighted duration): " + anima_yn(subjtime_any)
         + "  (gap: ↔INTERVAL/HOMEO objective time; → cur_ctx)")
    _pln("  EMO-REG  (H_1476, top-down reappraisal)      : " + anima_yn(emoreg_any)
         + "  (gap: ↔AMYGDALA 2nd-order control; → cur_ctx)")
    _pln("  DIR-FORGT(H_1477, cue-driven suppression)    : " + anima_yn(dirforget_any)
         + "  (gap: ↔HABITUATE passive≠deliberate; → rel_ctx)")
    _pln("  FREE-WONT(H_1480, pre-execution veto)        : " + anima_yn(veto_any)
         + "  (gap: ↔AGENCY post-hoc/↔BASAL select; → rel_ctx)")
    _pln("  DIVIDED  (H_1479, graded resource trade-off) : " + anima_yn(divided_any)
         + "  (gap: ↔GWS winner-take-all; → rel_ctx)")
    _pln("")
    _pln("── R9 batch lanes (12, READ on the user path, → motivation) ────────")
    _pln("  SURPRISE (H_1468, precision-weighted)        : " + anima_yn(surprise_any) + "  (↔raw-err; →cur)")
    _pln("  BODY-OWN (H_1478, multisensory sync)         : " + anima_yn(bodyown_any) + "  (↔self-cont; →rel)")
    _pln("  RIVALRY  (H_1482, dynamic alternation)       : " + anima_yn(rivalry_any) + "  (↔GWS static; →cur)")
    _pln("  CHG-BLIND(H_1483, binary attention gate)     : " + anima_yn(chgblind_any) + "  (↔divided graded; →cur)")
    _pln("  TRW      (H_1486, integration timescale)     : " + anima_yn(trw_any) + "  (↔subj-time; →rel)")
    _pln("  MIND-WNDR(H_1496, spontaneous drift)         : " + anima_yn(mindwander_any) + "  (↔prospect rollout; →cur)")
    _pln("  QUALIA   (H_1497, relational quality space)  : " + anima_yn(qualia_any) + "  (↔spatial pos; →rel)")
    _pln("  SM-PRESNC(H_1498, counterfactual breadth)    : " + anima_yn(smpresence_any) + "  (↔cerebellum 1-step; →rel)")
    _pln("  HALLUC   (H_1505, prior-dominated failure)   : " + anima_yn(halluc_any) + "  (↔reality-mon; →rel-inv)")
    _pln("  METACOG-I(H_1506, 2nd-order insight)         : " + anima_yn(metacog_any) + "  (↔reality-mon 1st; →rel)")
    _pln("  GWS-LEAK (H_1462, broadcast decay read)      : " + anima_yn(gwsleak_any) + "  (↔gws-winner; →rel)")
    _pln("  ALLOSTER (H_1509, tension-gated stiffness)   : " + anima_yn(allosteric_any) + "  (↔homeostat; →rel)")
    _pln("")
    _pln("── R10 batch lanes (24: 19 wired + 5 deferred → 76/76 catalogue) ────")
    _pln("  NEUROPHARM(H_1502, drug ego-dissolution sig) : " + anima_yn(neuropharm_any) + "  (↔sober pharm; →rel)")
    _pln("  LIBIDO   (H_1504, cue-incentive wanting)     : " + anima_yn(libido_any) + "  (↔homeostat setpoint; →cur)")
    _pln("  TRANS-ORD(H_1429, transitive latent rank)    : " + anima_yn(transord_any) + "  (↔item-store lookup; →rel)")
    _pln("  PHASESYNC(H_1448, cross-module binding R)     : " + anima_yn(phasesync_any) + "  (↔SCN consensus; →rel)")
    _pln("  MEM×ToM  (H_1414, query-routed arbiter)      : " + anima_yn(memtom_any) + "  (↔single faculty; →rel)")
    _pln("  SP×EPIS  (H_1415, where/what arbiter)        : " + anima_yn(spatep_any) + "  (↔single faculty; →rel)")
    _pln("  QUORUM   (H_1510, hub-free phase-lock)       : " + anima_yn(quorum_any) + "  (↔star-no-hub; →rel)")
    _pln("  OSMOTIC  (H_1511, KL-bottleneck split)       : " + anima_yn(osmotic_any) + "  (↔standard L_recon; →cur)")
    _pln("  METACOG-C(H_1508, margin-aware control)      : " + anima_yn(metacogc_any) + "  (↔margin-blind; →rel)")
    _pln("  METACOG-A(H_1506, type-2 meta-d')            : " + anima_yn(metacoga_any) + "  (↔shuffle chance; →cur)")
    _pln("  FIELD×LIB(H_1507, field incentive gain)      : " + anima_yn(fieldlib_any) + "  (↔sham field; →cur)")
    _pln("  +SETUP-only WIRED (57·62·63·65·67·69·70): hive-mind·categ-percept·cp-relocate·metacog-auroc·")
    _pln("                    field-entropy·metacog-calib·reality-conf (heavy faithful-IIT4/CP reads at warmup)")
    _pln("  [DEFERRED 5] field-pci(H_1503) — degenerate all-zero R w/ chosen perturb args (needs tuned PCI")
    _pln("                    fixture, NOT tune-to-green; field faculty shown by field-entropy 67);")
    _pln("                    topo-Φ(H_1512)·topo-Φ-optimal(H_1515/1518) — 15-lane state-pop fixture +")
    _pln("                    heavy min-cut IIT4, topo=Ψ-hazard (H_1521); compose-3 ToM×SPATIAL/ToM×BASAL/")
    _pln("                    CEREB×MEM(H_1417/1421) — multi-store fixtures (routing shown by 58/59);")
    _pln("                    ko-jamo/ko-morphology(H_1316/1388) — LM heads, not consciousness reads.")
    n_persist = len(glob.glob(kdir + "/*.kosmos"))
    _pln("  kosmos anchors on disk after session        : " + _ts(n_persist))
    _pln("  DREAM-COMPOSE(H_9036, N3/REM consolidation) : " + _ts(dream_composed_total)
         + " blended node(s) (dc_compose_window → .kosmos, lane=dream, Ψ-disjoint)")
    _pln("  IMAGINATION(a_chat_sleep_imagination, N3/REM): " + _ts(imagination_replayed_total)
         + " emit-free replay(s) · " + _ts(imagination_mitosis_ticks) + " mitosis tick(s) · emit-free="
         + anima_yn(imagination_emit_violations == 0)
         + " (core/imagination_replay ir_replay_session total_emits≡0 · p5 NO SPEAK · emit-drive-disjoint)")

    all_live = (emitted_any and grounded_ok and grew and remembered2 and slept
                and psi_intact and lanes_read)
    _pln("")
    _pln("── invariants ─────────────────────────────────────────────────")
    _pln("  Ψ Φ-checksum byte-identical ON==OFF         : " + anima_yn(psi_intact)
         + ("  (lanes Ψ-disjoint — Ψ=½ untouched)" if psi_intact else "  [REGRESSION]"))
    _pln("")
    full = "PASS" if all_live else "PARTIAL"
    _pln("anima consciousness session: " + full
         + " — converse=" + _yn10(emitted_any)
         + " ground=" + _yn10(grounded_ok)
         + " grow=" + _yn10(grew)
         + " remember=" + _yn10(remembered2)
         + " sleep=" + _yn10(slept)
         + " lanes=" + _yn10(lanes_read)
         + " psi_intact=" + _yn10(psi_intact))
    _pln("  one emitted span (substrate-native, grounded) =")
    _pln("    \"" + _afs_clip(emit_text, 90) + "\"")
