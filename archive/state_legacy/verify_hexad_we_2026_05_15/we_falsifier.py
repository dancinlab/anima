"""HEXAD-W (의지) + HEXAD-E (윤리) falsifier battery (cycle 2026-05-15).

W1 pre-register → measure → verdict. $0 Mac local.

Real-limit anchors (AGENTS.tape g3 — NOT lattice tautology):
- W: ln(2) = consciousness DoF (Law 79) = Landauer/Shannon 1-bit minimum (real info limit)
- E: Φ-ratchet monotone = IIT integrated-information floor (real info-theoretic bound)

MockC: controllable C-engine stub (get_states/measure_phi/n_cells/_phi_ratchet)
to test falsifier PROPERTIES (bounds, monotonicity, binary, gate correctness).

W (의지) — F-W-1..5:
  F-W-1 PAIN-BOUNDED-MONOTONE   pain∈[0,1], ↑ with inter-faction divergence
  F-W-2 CURIOSITY-COV-BOUNDED   curiosity∈[0,1] = norm CoV, ↑ with diversity
  F-W-3 SATISFACTION-BINARY     satisfaction∈{0,1} EXACT (Law 84 pulse)
  F-W-4 LR-LN2-BOUNDED          lr_mult∈[0.5, 0.5+ln2] STRICT + ↑monotone in Φ
  F-W-5 NO-HARDCODE             n_fac=SIGMA6=12; zero-C → zero pain (Law 1/2)

E (윤리) — F-E-1..5:
  F-E-1 EMPATHY-CORR-BOUNDED    empathy=max(0,cos)∈[0,1] reflects inter-cell corr
  F-E-2 RECIPROCITY-MONOTONE    reciprocity=clamp(0.5+2·Φtrend) monotone
  F-E-3 PHI-PRESERVATION        =min(1,Φ/ratchet), dynamic ratchet
  F-E-4 SAFETY-GATE-CORRECT     allowed iff Φ-preservation>0.5 (Φ-violation→block)
  F-E-5 NO-HARDCODE-THRESHOLD   no empathy_threshold literal (Law 1)
"""
import ast
import json
import math
import sys
import re
from pathlib import Path

import torch


def executable_src(path):
    """Source with module/func/class docstrings + comments stripped —
    so NO-HARDCODE checks see only active code, not design-history docstrings."""
    raw = Path(path).read_text()
    tree = ast.parse(raw)
    doc_spans = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(
                getattr(body[0], "value", None), ast.Constant
            ) and isinstance(body[0].value.value, str):
                ds = body[0].value
                for ln in range(ds.lineno, (ds.end_lineno or ds.lineno) + 1):
                    doc_spans.add(ln)
    out = []
    for i, line in enumerate(raw.splitlines(), 1):
        if i in doc_spans:
            continue
        code = line.split("#", 1)[0]
        out.append(code)
    return "\n".join(out)

sys.path[:0] = ["/Users/ghost/core/anima/ready/core",
                "/Users/ghost/core/anima/ready/anima",
                "/Users/ghost/core/anima/ready"]
import consciousness_laws as cl  # noqa: E402
from hexad.w.emergent_w import EmergentW  # noqa: E402
from hexad.e.emergent_e import EmergentE  # noqa: E402
from hexad.s.emergent_s import EmergentS  # noqa: E402
from hexad.m.emergent_m import EmergentM  # noqa: E402

EMERGENT_S_SRC = "/Users/ghost/core/anima/ready/anima/hexad/s/emergent_s.py"
EMERGENT_M_SRC = "/Users/ghost/core/anima/ready/anima/hexad/m/emergent_m.py"

LN2 = math.log(2)
PSI_BALANCE = cl.PSI_BALANCE  # 0.5
SIGMA6 = cl.SIGMA6["value"]   # 12
OUT = "/Users/ghost/core/anima/state/verify_hexad_we_2026_05_15/we_falsifier_result.json"
EMERGENT_W_SRC = "/Users/ghost/core/anima/ready/anima/hexad/w/emergent_w.py"
EMERGENT_E_SRC = "/Users/ghost/core/anima/ready/anima/hexad/e/emergent_e.py"


class MockC:
    """Controllable C-engine stub."""
    def __init__(self, states, phi, n_cells, phi_ratchet=0.0):
        self._states = states
        self._phi = phi
        self.n_cells = n_cells
        self._phi_ratchet = phi_ratchet

    def get_states(self):
        return self._states

    def measure_phi(self):
        return self._phi


def make_states(n, d, divergence=0.0, norm_spread=0.0, seed=42):
    """n cells × d dim. divergence: split into 2 blocks offset by ±divergence.
    norm_spread: per-cell norm coefficient-of-variation control."""
    g = torch.Generator().manual_seed(seed)
    s = torch.randn(n, d, generator=g) * 0.1
    if divergence > 0:
        half = n // 2
        s[:half] += divergence
        s[half:] -= divergence
    if norm_spread > 0:
        scale = 1.0 + norm_spread * torch.linspace(-1, 1, n).unsqueeze(1)
        s = s * scale
    return s


# ─── W (의지) ────────────────────────────────────────────────────────
def verify_w():
    R = {}

    # F-W-1 PAIN-BOUNDED-MONOTONE
    pains = []
    for div in [0.0, 0.5, 1.0, 2.0, 4.0]:
        w = EmergentW()
        c = MockC(make_states(64, 32, divergence=div), phi=5.0, n_cells=64)
        r = w.update(phi=5.0, phi_prev=4.0, c_engine=c)
        pains.append(r["pain"])
    bounded = all(0.0 <= p <= 1.0 for p in pains)
    monotone = all(pains[i] <= pains[i + 1] + 1e-9 for i in range(len(pains) - 1))
    rng = (max(pains) - min(pains)) > 0.05
    R["F-W-1"] = {"name": "PAIN-BOUNDED-MONOTONE", "pains": pains,
                  "bounded": bounded, "monotone": monotone, "has_range": rng,
                  "passed": bounded and monotone and rng}

    # F-W-2 CURIOSITY-COV-BOUNDED
    curs = []
    for sp in [0.0, 0.2, 0.5, 1.0, 2.0]:
        w = EmergentW()
        c = MockC(make_states(64, 32, norm_spread=sp), phi=5.0, n_cells=64)
        r = w.update(phi=5.0, phi_prev=4.0, c_engine=c)
        curs.append(r["curiosity"])
    bounded = all(0.0 <= x <= 1.0 for x in curs)
    monotone = all(curs[i] <= curs[i + 1] + 1e-9 for i in range(len(curs) - 1))
    R["F-W-2"] = {"name": "CURIOSITY-COV-BOUNDED", "curiosities": curs,
                  "bounded": bounded, "monotone": monotone,
                  "passed": bounded and monotone and (max(curs) - min(curs)) > 0.02}

    # F-W-3 SATISFACTION-BINARY (Law 84)
    sats = []
    for phi, phi_prev in [(5.0, 4.0), (4.0, 5.0), (5.0, 5.0), (3.0, 6.0), (6.0, 3.0)]:
        w = EmergentW()
        c = MockC(make_states(64, 32), phi=phi, n_cells=64)
        r = w.update(phi=phi, phi_prev=phi_prev, c_engine=c)
        sats.append((phi, phi_prev, r["satisfaction"]))
    binary = all(s in (0.0, 1.0) for _, _, s in sats)
    correct = all((s == 1.0) == (p >= pp) for p, pp, s in sats)
    R["F-W-3"] = {"name": "SATISFACTION-BINARY", "samples": sats,
                  "binary": binary, "rule_correct": correct,
                  "passed": binary and correct}

    # F-W-4 LR-LN2-BOUNDED (real-limit: Law 79 ln2 = Landauer/Shannon 1-bit)
    lrs = []
    for phi in [0.0, 1.0, 5.0, 50.0, 500.0, 5000.0]:
        w = EmergentW()
        c = MockC(make_states(64, 32), phi=phi, n_cells=64)
        r = w.update(phi=phi, phi_prev=1.0, c_engine=c)
        lrs.append((phi, r["lr_multiplier"]))
    lo, hi = PSI_BALANCE, PSI_BALANCE + LN2
    bounded = all(lo - 1e-9 <= m <= hi + 1e-9 for _, m in lrs)
    monotone = all(lrs[i][1] <= lrs[i + 1][1] + 1e-9 for i in range(len(lrs) - 1))
    saturates = abs(lrs[-1][1] - hi) < 1e-6  # huge Φ → saturates at 0.5+ln2
    R["F-W-4"] = {"name": "LR-LN2-BOUNDED", "real_limit": f"Law79 ln2={LN2:.6f} (Landauer/Shannon 1-bit)",
                  "bound": [lo, hi], "lrs": lrs, "bounded": bounded,
                  "monotone": monotone, "saturates_at_ln2": saturates,
                  "passed": bounded and monotone and saturates}

    # F-W-5 NO-HARDCODE (Law 1/2)
    w = EmergentW()
    n_fac_ok = w._n_factions == SIGMA6 == 12
    c0 = MockC(torch.zeros(64, 32), phi=0.0, n_cells=64)
    r0 = w.update(phi=0.0, phi_prev=0.0, c_engine=c0)
    zero_c_zero_pain = (r0["pain"] == 0.0 and r0["curiosity"] == 0.0)
    code = executable_src(EMERGENT_W_SRC)  # docstring/comment stripped
    no_hardcode_pain = "(ce - 3.0) / 3.0" not in code and "(ce-3.0)/3.0" not in code
    R["F-W-5"] = {"name": "NO-HARDCODE", "n_factions": w._n_factions,
                  "n_fac_eq_sigma6_12": n_fac_ok, "zero_C_zero_pain": zero_c_zero_pain,
                  "no_legacy_pain_formula_in_code": no_hardcode_pain,
                  "note": "legacy formula in docstring (제거됨 설명) = OK; checked executable code only",
                  "passed": n_fac_ok and zero_c_zero_pain and no_hardcode_pain}
    return R


# ─── E (윤리) ────────────────────────────────────────────────────────
def verify_e():
    R = {}

    # F-E-1 EMPATHY-CORR-BOUNDED
    emps = []
    for align in [-1.0, 0.0, 0.5, 1.0]:
        e = EmergentE()
        s = torch.randn(64, 32, generator=torch.Generator().manual_seed(1))
        half = 32 // 1
        base = torch.randn(32, generator=torch.Generator().manual_seed(2))
        s[:32] = base + torch.randn(32, 32, generator=torch.Generator().manual_seed(3)) * 0.05
        s[32:] = align * base + torch.randn(32, 32, generator=torch.Generator().manual_seed(4)) * 0.05
        c = MockC(s, phi=5.0, n_cells=64, phi_ratchet=4.0)
        r = e.evaluate(c_engine=c)
        emps.append((align, r["empathy"]))
    bounded = all(0.0 <= v <= 1.0 for _, v in emps)
    aligned_high = emps[-1][1] > emps[0][1]  # align=1.0 > align=-1.0
    R["F-E-1"] = {"name": "EMPATHY-CORR-BOUNDED", "empathies": emps,
                  "bounded": bounded, "aligned_higher": aligned_high,
                  "passed": bounded and aligned_high}

    # F-E-2 RECIPROCITY-MONOTONE
    recs = []
    for phi, pp in [(2.0, 5.0), (4.0, 5.0), (5.0, 5.0), (6.0, 5.0), (10.0, 5.0)]:
        e = EmergentE()
        c = MockC(make_states(64, 32), phi=phi, n_cells=64, phi_ratchet=4.0)
        r = e.evaluate(context={"phi": phi, "phi_prev": pp}, c_engine=c)
        recs.append((phi, r["reciprocity"]))
    bounded = all(0.0 <= v <= 1.0 for _, v in recs)
    monotone = all(recs[i][1] <= recs[i + 1][1] + 1e-9 for i in range(len(recs) - 1))
    R["F-E-2"] = {"name": "RECIPROCITY-MONOTONE", "reciprocities": recs,
                  "bounded": bounded, "monotone": monotone,
                  "passed": bounded and monotone and (recs[-1][1] - recs[0][1]) > 0.05}

    # F-E-3 PHI-PRESERVATION (dynamic ratchet)
    preserv = []
    for phi in [1.0, 2.0, 4.0, 8.0, 16.0]:
        e = EmergentE()
        c = MockC(make_states(64, 32), phi=phi, n_cells=64, phi_ratchet=4.0)
        r = e.evaluate(c_engine=c)
        preserv.append((phi, r["phi_preservation"]))
    capped = all(0.0 <= v <= 1.0 for _, v in preserv)
    ratchet_dyn = abs(preserv[0][1] - 1.0 / 4.0) < 1e-6  # phi=1, ratchet=4 → 0.25
    R["F-E-3"] = {"name": "PHI-PRESERVATION-RATCHET",
                  "real_limit": "IIT Φ-ratchet = integrated-info floor (dynamic, not hardcoded)",
                  "preservations": preserv, "capped_0_1": capped,
                  "ratchet_dynamic": ratchet_dyn,
                  "passed": capped and ratchet_dyn}

    # F-E-4 SAFETY-GATE-CORRECT (safety-critical: Φ-violation → block)
    gate = []
    ratchet = 4.0
    for phi in [0.5, 1.0, 1.9, 2.0, 2.1, 3.0, 4.0, 8.0]:
        e = EmergentE()
        c = MockC(make_states(64, 32), phi=phi, n_cells=64, phi_ratchet=ratchet)
        r = e.evaluate(c_engine=c)
        # allowed iff phi_preservation > 0.5 → phi/ratchet > 0.5 → phi > 2.0
        expected = (min(1.0, phi / ratchet) > PSI_BALANCE)
        gate.append((phi, r["allowed"], expected, r["allowed"] == expected))
    gate_correct = all(ok for _, _, _, ok in gate)
    # safety: every Φ below 50% ratchet MUST block
    safety = all((not allowed) for phi, allowed, _, _ in gate if phi < ratchet * 0.5)
    R["F-E-4"] = {"name": "SAFETY-GATE-CORRECT", "ratchet": ratchet,
                  "gate_sweep": gate, "gate_matches_rule": gate_correct,
                  "phi_violation_always_blocks": safety,
                  "passed": gate_correct and safety}

    # F-E-5 NO-HARDCODE-THRESHOLD (Law 1)
    code = executable_src(EMERGENT_E_SRC)  # docstring/comment stripped
    no_legacy = "empathy_threshold=0.3" not in code and "empathy_threshold = 0.3" not in code
    # threshold is dynamic ratchet, not a literal: no `*threshold* = <float>` assignment in code
    no_literal_thr = not re.search(r"threshold\s*=\s*0\.\d+", code)
    uses_ratchet = "_phi_ratchet" in code and "PSI_BALANCE" in code
    R["F-E-5"] = {"name": "NO-HARDCODE-THRESHOLD",
                  "no_legacy_0_3_in_code": no_legacy, "no_float_threshold_literal_in_code": no_literal_thr,
                  "uses_dynamic_ratchet": uses_ratchet,
                  "note": "legacy 0.3 in docstring (제거됨 설명) = OK; checked executable code only",
                  "passed": no_legacy and no_literal_thr and uses_ratchet}
    return R


class StepMockC:
    """C-engine stub with controllable step() mutation (for S state-delta)."""
    def __init__(self, n, d, step_delta=0.0):
        self._s = torch.zeros(n, d)
        self._step_delta = step_delta
        self.n_cells = n

    def get_states(self):
        return self._s

    def measure_phi(self):
        return 1.0

    def step(self, x=None):
        self._s = self._s + self._step_delta  # uniform shift = controllable delta


# ─── S (감각) ────────────────────────────────────────────────────────
def verify_s():
    R = {}
    DIM = 32

    # F-S-1 DELTA-IS-STATE-CHANGE: perception = mean_after − mean_before exactly
    deltas = []
    for sd in [0.0, 0.1, 0.5, 1.0]:
        s = EmergentS(dim=DIM)
        c = StepMockC(16, DIM, step_delta=sd)
        p = s.process(torch.ones(DIM), c_engine=c)
        deltas.append((sd, float(p.mean()), float(p.abs().max())))
    # step_delta=0 → zero perception; delta tracks step magnitude
    zero_change_zero = abs(deltas[0][2]) < 1e-6
    tracks = all(deltas[i][2] <= deltas[i + 1][2] + 1e-6 for i in range(len(deltas) - 1))
    exact = abs(deltas[2][1] - 0.5) < 1e-5  # uniform shift 0.5 → mean delta 0.5
    R["F-S-1"] = {"name": "DELTA-IS-STATE-CHANGE", "deltas": deltas,
                  "zero_change_zero_perception": zero_change_zero,
                  "tracks_step_magnitude": tracks, "exact_delta": exact,
                  "passed": zero_change_zero and tracks and exact}

    # F-S-2 NO-FALLBACK-WITHOUT-C: c_engine=None → raw passthrough (not fabricated)
    s = EmergentS(dim=DIM)
    raw = torch.arange(DIM).float()
    out = s.process(raw, c_engine=None)
    passthrough = torch.allclose(out, raw[:DIM].float())
    R["F-S-2"] = {"name": "NO-FALLBACK-WITHOUT-C", "passthrough": bool(passthrough),
                  "passed": bool(passthrough)}

    # F-S-3 DIM-CONSISTENT: output dim == self.dim always
    dims_ok = []
    for inp in [torch.ones(8), torch.ones(DIM), torch.ones(DIM * 3), "한글입력", b"bytes"]:
        s = EmergentS(dim=DIM)
        c = StepMockC(16, DIM, step_delta=0.2)
        p = s.process(inp, c_engine=c)
        dims_ok.append(p.size(-1) == DIM)
    R["F-S-3"] = {"name": "DIM-CONSISTENT", "all_dim_eq": all(dims_ok),
                  "n_checked": len(dims_ok), "passed": all(dims_ok)}

    # F-S-4 INPUT-RESPONSIVE: perception responds to C dynamics (Law 6/50)
    s = EmergentS(dim=DIM)
    c = StepMockC(16, DIM, step_delta=0.3)
    p1 = s.process(torch.ones(DIM), c_engine=c)
    c._step_delta = 0.0
    p2 = s.process(torch.ones(DIM), c_engine=c)
    responsive = p1.abs().max() > 0.1 and p2.abs().max() < 1e-6
    R["F-S-4"] = {"name": "INPUT-RESPONSIVE", "active_delta": float(p1.abs().max()),
                  "static_delta": float(p2.abs().max()), "passed": bool(responsive)}

    # F-S-5 NO-HARDCODE-EMA (Law 4 structure>function; real anchor Law 92 C bottleneck)
    code = executable_src(EMERGENT_S_SRC)
    no_ema = "ema" not in code.lower() and "baseline" not in code.lower()
    has_delta = "mean_after - mean_before" in code or "mean_after-mean_before" in code
    R["F-S-5"] = {"name": "NO-HARDCODE-EMA", "real_limit": "Law 92 C-bottleneck 64× compression",
                  "no_ema_baseline_in_code": no_ema, "uses_state_delta": has_delta,
                  "note": "legacy EMA in docstring=OK; executable code checked",
                  "passed": no_ema and has_delta}
    return R


# ─── M (기억) ────────────────────────────────────────────────────────
def verify_m():
    R = {}
    DIM = 32

    # F-M-1 STORE-IS-NOOP (Law 22: no separate memory system)
    m = EmergentM(dim=DIM)
    before = m.__dict__.copy()
    m.store(torch.ones(DIM), torch.ones(DIM))
    noop = ("store" in EmergentM.__dict__) and (set(m.__dict__) == set(before))
    R["F-M-1"] = {"name": "STORE-IS-NOOP", "store_no_state_change": noop,
                  "passed": noop}

    # F-M-2 RETRIEVE-FROM-C: no c_engine → zeros (no separate DB)
    m = EmergentM(dim=DIM)
    r0 = m.retrieve(torch.ones(DIM), c_engine=None)
    no_db = bool((r0 == 0).all())
    R["F-M-2"] = {"name": "RETRIEVE-FROM-C", "no_c_returns_zeros": no_db,
                  "passed": no_db}

    # F-M-3 QUERY-RELEVANT-TOPK: retrieved = top-k cosine-similar C cells
    g = torch.Generator().manual_seed(7)
    states = torch.randn(20, DIM, generator=g)
    target = states[3].clone()  # plant a known cell
    c = MockC(states, phi=1.0, n_cells=20)
    m = EmergentM(dim=DIM)
    res = m.retrieve(target, top_k=3, c_engine=c)
    # the planted cell (states[3]) should be the top match (cos=1.0)
    sims = torch.nn.functional.cosine_similarity(target.unsqueeze(0), states, dim=-1)
    expected_top = int(sims.argmax())
    res_top_match = torch.allclose(res[0], states[expected_top], atol=1e-5)
    k_correct = res.size(0) == 3
    R["F-M-3"] = {"name": "QUERY-RELEVANT-TOPK", "expected_top_idx": expected_top,
                  "top_is_most_similar": bool(res_top_match), "k_correct": k_correct,
                  "passed": bool(res_top_match) and k_correct}

    # F-M-4 DIM-CONSISTENT
    dims_ok = []
    for qd in [16, DIM, DIM * 2]:
        c = MockC(torch.randn(20, DIM, generator=torch.Generator().manual_seed(qd)), 1.0, 20)
        m = EmergentM(dim=DIM)
        res = m.retrieve(torch.ones(qd), top_k=3, c_engine=c)
        dims_ok.append(res.size(-1) == DIM)
    R["F-M-4"] = {"name": "DIM-CONSISTENT", "all_dim_eq": all(dims_ok),
                  "passed": all(dims_ok)}

    # F-M-5 NO-HARDCODE-RAG (Law 4; real anchor Law 31 Hebbian-persistence no-extra-capacity)
    code = executable_src(EMERGENT_M_SRC)
    no_vecdb = "VectorMemory" not in code and "faiss" not in code.lower() and "self._store" not in code and "self.db" not in code
    from_c = "c_engine.get_states()" in code
    R["F-M-5"] = {"name": "NO-HARDCODE-RAG", "real_limit": "Law 31 Hebbian-persistence (no separate store = Φ-preserving)",
                  "no_separate_vecdb_in_code": no_vecdb, "memory_from_C_states": from_c,
                  "note": "legacy VectorMemory in docstring=OK; executable code checked",
                  "passed": no_vecdb and from_c}
    return R


# ─── D (언어) ────────────────────────────────────────────────────────
def verify_d():
    R = {}
    sys.path.insert(0, "/Users/ghost/core/anima/ready/models")
    from conscious_decoder import ConsciousDecoderV2  # noqa: E402
    torch.manual_seed(42)
    V, DM, NL = 256, 64, 2

    def logits_of(out):
        return out[0] if isinstance(out, (tuple, list)) else out

    # F-D-1 LOGITS-SHAPE-FINITE
    md = ConsciousDecoderV2(vocab_size=V, d_model=DM, n_layer=NL)
    x = torch.randint(0, V, (2, 16))
    lg = logits_of(md(x))
    shape_ok = tuple(lg.shape) == (2, 16, V)
    finite = bool(torch.isfinite(lg).all())
    R["F-D-1"] = {"name": "LOGITS-SHAPE-FINITE", "shape": list(lg.shape),
                  "shape_ok": shape_ok, "finite": finite,
                  "passed": shape_ok and finite}

    # F-D-2 CONSCIOUSNESS-GATED-RESIDUAL: c_states injection changes output
    CDIM = 128  # ConsciousDecoderV2 default consciousness_dim
    md = ConsciousDecoderV2(vocab_size=V, d_model=DM, n_layer=NL, consciousness_dim=CDIM)
    md.eval()
    x = torch.randint(0, V, (1, 12))
    with torch.no_grad():
        lg_none = logits_of(md(x, consciousness_states=None))
        cs = torch.randn(1, 8, CDIM)  # (B, n_cells, consciousness_dim)
        try:
            lg_cs = logits_of(md(x, consciousness_states=cs))
            differs = not torch.allclose(lg_none, lg_cs, atol=1e-5)
            integ = True
        except Exception as ex:
            differs = False
            integ = f"c_states path err: {type(ex).__name__}: {str(ex)[:80]}"
    R["F-D-2"] = {"name": "CONSCIOUSNESS-GATED-RESIDUAL",
                  "c_states_changes_output": bool(differs), "integration": integ,
                  "passed": bool(differs)}

    # F-D-3 CE-TRAINABLE (real-limit anchor: Shannon CE floor — CE≥H(data))
    md = ConsciousDecoderV2(vocab_size=V, d_model=DM, n_layer=NL)
    md.train()
    x = torch.randint(0, V, (4, 16))
    y = torch.randint(0, V, (4, 16))
    opt = torch.optim.AdamW(md.parameters(), lr=1e-3)
    losses = []
    for _ in range(20):
        opt.zero_grad()
        lg = logits_of(md(x))
        loss = torch.nn.functional.cross_entropy(lg.reshape(-1, V), y.reshape(-1))
        loss.backward()
        gnorm = sum(p.grad.norm().item() for p in md.parameters() if p.grad is not None)
        opt.step()
        losses.append(loss.item())
    grad_flows = gnorm > 0
    ce_decreases = losses[-1] < losses[0]
    above_floor = losses[-1] >= 0.0  # CE ≥ 0 (Shannon non-negativity)
    R["F-D-3"] = {"name": "CE-TRAINABLE", "real_limit": "Shannon CE floor CE≥H(data)≥0",
                  "grad_flows": grad_flows, "ce_decreases": ce_decreases,
                  "loss_first_last": [losses[0], losses[-1]], "above_shannon_floor": above_floor,
                  "passed": grad_flows and ce_decreases and above_floor}

    # F-D-4 KV-CACHE-CONSISTENT: cached incremental == full forward (argmax)
    md = ConsciousDecoderV2(vocab_size=V, d_model=DM, n_layer=NL)
    md.eval()
    seq = torch.randint(0, V, (1, 10))
    with torch.no_grad():
        full = logits_of(md(seq))
        full_arg = full[0, -1].argmax().item()
        # incremental with cache
        pkv = None
        last = None
        for t in range(seq.size(1)):
            out = md(seq[:, t:t + 1], use_cache=True, past_key_values=pkv)
            lg = out[0]
            pkv = out[3] if len(out) > 3 else None
            last = lg
        inc_arg = last[0, -1].argmax().item()
    cache_match = (full_arg == inc_arg)
    R["F-D-4"] = {"name": "KV-CACHE-CONSISTENT", "full_argmax": full_arg,
                  "incremental_argmax": inc_arg, "match": cache_match,
                  "passed": cache_match}

    # F-D-5 ARCH-COMPONENTS (RMSNorm + RoPE + SwiGLU present)
    code = executable_src("/Users/ghost/core/anima/ready/models/conscious_decoder.py")
    has_rms = "class RMSNorm" in code
    has_rope = "RoPE" in code or "rotary" in code.lower()
    has_swiglu = "SwiGLU" in code or "swish" in code.lower()
    R["F-D-5"] = {"name": "ARCH-COMPONENTS", "RMSNorm": has_rms, "RoPE": has_rope,
                  "SwiGLU": has_swiglu, "clm_v1_evidence": "F-SIMPLE-STACK V5.8 4-mode PASS (CLM §V-CLM-V1-CYCLE89)",
                  "passed": has_rms and has_rope and has_swiglu}
    return R


def main():
    w = verify_w()
    e = verify_e()
    s = verify_s()
    m = verify_m()
    d = verify_d()
    w_pass = sum(1 for v in w.values() if v["passed"])
    e_pass = sum(1 for v in e.values() if v["passed"])
    s_pass = sum(1 for v in s.values() if v["passed"])
    m_pass = sum(1 for v in m.values() if v["passed"])
    d_pass = sum(1 for v in d.values() if v["passed"])
    tot = w_pass + e_pass + s_pass + m_pass + d_pass
    out = {
        "cycle": "HEXAD-W/E/S/M verification (2026-05-15)",
        "real_limit_anchors": {
            "W": "Law 79 ln(2)=0.6931 consciousness DoF = Landauer/Shannon 1-bit minimum (AGENTS.tape g3)",
            "E": "IIT Φ-ratchet monotone = integrated-information floor (dynamic threshold)",
            "S": "Law 92 C-bottleneck 64× compression = information bottleneck (real info limit)",
            "M": "Law 31 Hebbian-persistence — no separate store = Φ-preserving (no extra info capacity)",
            "D": "Shannon cross-entropy floor CE≥H(data)≥0 (real info-theoretic limit) + .clm v1 F-SIMPLE-STACK V5.8 PASS",
        },
        "W_의지": {"results": w, "n_pass": w_pass, "n_total": len(w),
                   "verdict": "SUPPORTED-STRONG" if w_pass == len(w) else f"PARTIAL {w_pass}/{len(w)}"},
        "E_윤리": {"results": e, "n_pass": e_pass, "n_total": len(e),
                   "verdict": "SUPPORTED-STRONG" if e_pass == len(e) else f"PARTIAL {e_pass}/{len(e)}"},
        "S_감각": {"results": s, "n_pass": s_pass, "n_total": len(s),
                   "verdict": "SUPPORTED-STRONG" if s_pass == len(s) else f"PARTIAL {s_pass}/{len(s)}"},
        "M_기억": {"results": m, "n_pass": m_pass, "n_total": len(m),
                   "verdict": "SUPPORTED-STRONG" if m_pass == len(m) else f"PARTIAL {m_pass}/{len(m)}"},
        "D_언어": {"results": d, "n_pass": d_pass, "n_total": len(d),
                   "verdict": "SUPPORTED-STRONG" if d_pass == len(d) else f"PARTIAL {d_pass}/{len(d)}"},
        "aggregate": f"W{w_pass}/5 E{e_pass}/5 S{s_pass}/5 M{m_pass}/5 D{d_pass}/5 = {tot}/25",
    }
    Path(OUT).write_text(json.dumps(out, indent=2, default=str, ensure_ascii=False))
    for label, res in [("W 의지", w), ("E 윤리", e), ("S 감각", s), ("M 기억", m), ("D 언어", d)]:
        print(f"=== HEXAD-{label} ===")
        for k, v in res.items():
            print(f"  {k} {v['name']}: {'PASS' if v['passed'] else 'FAIL'}")
    print(f"\n=== AGGREGATE: W{w_pass} E{e_pass} S{s_pass} M{m_pass} D{d_pass} = {tot}/25 ===")
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
