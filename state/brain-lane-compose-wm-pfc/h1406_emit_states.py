#!/usr/bin/env python3
"""h1406_emit_states.py — ENGINE-NATIVE bridge emitter for H_1406 (WM × hier-PFC compose).

Mirrors state/brain-lane-compose-wm-pfc/h1406_compose_wm_pfc.py build_items VERBATIM
(same SEEDS, same numpy RNG draw order, same 5 families, same AMBIG_NOISE / DIM / K /
LAMBDA / thresholds) but instead of computing the WM/PFC reads in numpy it RECORDS the
raw substrate INPUTS per item so the live CORE engine (wm_buffer_* + _cos) can produce
wm_score / pfc_align ITSELF. This is the h1404_lane_compose_phi.py → h1404_phi_runner.hexa
pattern (a_engine_native_learning): the python side only lays out the deterministic stimulus
trajectory; the VERDICT math runs on the live engine ops in h1406_compose_wm_pfc_runner.hexa.

State-file format (one block per item):
  # <seed> <fam> <correct> <gap> <n_distract>
  CUE <DIM floats>
  TGT <DIM floats>          (WM gate-in target, strength 1.0)
  DST <DIM floats>          (n_distract of these — distractor tokens for the gap)
  SUB <DIM floats>          (PFC current-subgoal target; cue vs this = pfc_align)
  PFCOVR <float>            (optional: families that OVERRIDE pfc_align directly, e.g. F1
                             centres it near ALIGN_THR; -999 = use the live cos(cue,SUB))
  WMRAW_OVR <float>         (optional: families that set wm_score directly to WM_THR etc.;
                             -999 = use the live wm_buffer_probe_score(cue))

usage: python3 h1406_emit_states.py /path/to/states.txt
"""
import sys
import numpy as np

# ── frozen knobs — VERBATIM from h1406_compose_wm_pfc.py ─────────────────────
SEEDS        = [4406, 4407, 4408]
N_PER_FAMILY = 90
AMBIG_NOISE  = 0.18
DIM          = 64
K            = 4
LAMBDA       = 0.85
WM_THR       = 0.40
CUE_SIM_REFRESH = 0.9
ALIGN_THR    = 0.85
CUE_NOISE    = 0.02


def make_token(rng):
    v = rng.standard_normal(DIM)
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(a @ b / ((np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12))


class WorkMemBuffer:
    def __init__(self, k, lam, distractor_gain=0.5):
        self.k = k; self.lam = lam; self.dg = distractor_gain
        self.keys = []; self.act = []

    def _argmin_act(self):
        return int(np.argmin(self.act))

    def gate_in(self, tok, strength=1.0):
        for i, ky in enumerate(self.keys):
            if cos(ky, tok) >= CUE_SIM_REFRESH:
                self.act[i] = max(self.act[i], strength); self.keys[i] = tok; return
        if len(self.keys) < self.k:
            self.keys.append(tok); self.act.append(strength)
        else:
            j = self._argmin_act()
            if strength > self.act[j]:
                self.keys[j] = tok; self.act[j] = strength

    def leak(self):
        self.act = [a * self.lam for a in self.act]

    def distractor_step(self, tok):
        self.leak(); self.gate_in(tok, strength=self.dg)

    def probe(self, probe):
        if not self.keys:
            return 0.0
        scores = [self.act[i] * max(0.0, cos(self.keys[i], probe)) for i in range(len(self.keys))]
        return float(np.max(scores))


def pfc_align(cue, current_subgoal_target):
    return cos(cue, current_subgoal_target)


def vstr(v):
    return " ".join(f"{x:.10g}" for x in v)


def emit_seed(seed, out):
    """Replays build_items VERBATIM (same rng draw order) and writes per-item stimulus.
    The python WM/cos are recomputed here ONLY to preserve the rng sequence and to set
    `correct`; the engine runner reproduces wm_score/pfc_align from the recorded vectors."""
    rng = np.random.default_rng(seed)

    def jit(x):
        return x + AMBIG_NOISE * rng.standard_normal()

    def run_gap(target, gap):
        wm = WorkMemBuffer(K, LAMBDA)
        wm.gate_in(target, 1.0)
        dst = []
        for _ in range(gap):
            d = make_token(rng)
            dst.append(d)
            wm.distractor_step(d)
        return wm, wm.probe(target), dst

    def block(fam, correct, cue, tgt, dst, sub, pfc_ovr, wm_ovr):
        out.append(f"# {seed} {fam} {correct} {len(dst)} {len(dst)}")
        out.append("CUE " + vstr(cue))
        out.append("TGT " + vstr(tgt))
        for d in dst:
            out.append("DST " + vstr(d))
        out.append("SUB " + vstr(sub))
        out.append(f"PFCOVR {pfc_ovr:.10g}")
        out.append(f"WMRAW_OVR {wm_ovr:.10g}")

    # ── F1 WM-DECISIVE ──────────────────────────────────────────────────────
    for _ in range(N_PER_FAMILY):
        target = make_token(rng)
        gap = int(rng.integers(4, 9))
        wm, raw, dst = run_gap(target, gap)
        cue = target + rng.standard_normal(DIM) * CUE_NOISE
        # wm_score = wm.probe(cue) — engine reproduces this from CUE/TGT/DST → wm_ovr=-999
        survived = (raw + AMBIG_NOISE * rng.standard_normal()) >= WM_THR
        correct = 1 if survived else 0
        unrel = make_token(rng)            # draws to preserve rng order (jit(0.0) below too)
        _ = pfc_align(cue, unrel) + jit(0.0)
        pfc_a = ALIGN_THR - 0.05 + AMBIG_NOISE * rng.standard_normal()
        block("F1", correct, cue, target, dst, unrel, pfc_a, -999.0)

    # ── F2 PFC-DECISIVE ─────────────────────────────────────────────────────
    for _ in range(N_PER_FAMILY):
        in_order = bool(rng.integers(0, 2))
        cue = make_token(rng)
        cur_target = (cue + rng.standard_normal(DIM) * CUE_NOISE) if in_order else make_token(rng)
        wm_score = WM_THR + jit(0.0)
        if in_order:
            pfc_a = pfc_align(cue, cur_target)
            correct = 1
        else:
            pfc_a = pfc_align(cue, cur_target)
            correct = 0
        # WM ~chance here → wm_score set to WM_THR+jit directly (wm_ovr); pfc engine-derived
        block("F2", correct, cue, cue, [], cur_target, -999.0, wm_score)

    # ── F3 AGREE ────────────────────────────────────────────────────────────
    for _ in range(N_PER_FAMILY):
        cue = make_token(rng)
        cur_target = cue + rng.standard_normal(DIM) * CUE_NOISE
        wm_score = max(0.0, 0.8 + jit(0.0))
        pfc_a = max(0.0, pfc_align(cue, cur_target))
        block("F3", 1, cue, cue, [], cur_target, -999.0, wm_score)

    # ── F4 CONFLICT (WM right) ──────────────────────────────────────────────
    for _ in range(N_PER_FAMILY):
        cue = make_token(rng)
        unrel = make_token(rng)
        wm_score = max(0.0, 0.7 + jit(0.0))
        pfc_a = pfc_align(cue, unrel) - 0.10
        block("F4", 1, cue, cue, [], unrel, pfc_a - 0.0, wm_score)

    # ── F5 ADVERSARIAL (PFC right, WM loud-but-wrong) ───────────────────────
    for _ in range(N_PER_FAMILY):
        cue = make_token(rng)
        wm, _, dst = run_gap(cue, 0)
        wm_score = max(0.0, 0.9 + jit(0.0))
        cur_target = make_token(rng)
        pfc_a = pfc_align(cue, cur_target) - 0.10
        pfc_a = pfc_a + AMBIG_NOISE * rng.standard_normal()
        block("F5", 0, cue, cue, dst, cur_target, pfc_a, wm_score)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1406_states.txt"
    out = []
    out.append(f"# H1406 states DIM={DIM} K={K} LAMBDA={LAMBDA} WM_THR={WM_THR} ALIGN_THR={ALIGN_THR} AMBIG={AMBIG_NOISE} NPF={N_PER_FAMILY}")
    for s in SEEDS:
        emit_seed(s, out)
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {path}: {len(SEEDS)} seeds × {5*N_PER_FAMILY} items")


if __name__ == "__main__":
    main()
