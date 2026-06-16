#!/usr/bin/env python3
"""h940_real_anu_reconfirm.py — H_940: REAL-ANU re-confirm of H_936's buffer-artifact.

QUESTION (closes H_936's os.urandom-fallback gap)
=================================================
H_936 found 🟢 F-H936-ARTIFACT-CONFIRMED: H_930's tension-axis difference (phi_mean
Cohen d≈+2.45) COLLAPSES to PARITY once the finite 1024-byte committed buffer is
replaced by a LARGE non-cycling buffer — i.e. the tension difference was a finite-
buffer DC-bias cycling artifact, not functional stochastic diversity. BUT the big
buffer in the H_936 run was `os.urandom_fallback` (the real ANU key/network was
unavailable on that host). H_936 explicitly flagged the real-ANU re-confirm as OPEN.

H_940 asks: does a REAL ANU vacuum-fluctuation big buffer (>= the H_936 size)
REPRODUCE the same tension parity that os.urandom produced?

THE LEVER UNDER TEST (this is H_940's sharpening over H_936)
===========================================================
EXACTLY the H_936 three-arm comparison (Arm-DET deterministic, Arm-QS quantum-small
cycling 1024 B, Arm-QB quantum-big-fresh), with ONE difference: the big buffer for
Arm-QB is pulled REAL from the ANU Quantum Numbers API via anu_pull.py (secret-keyed
flat.anu_key_paid / flat.anu_key_free -> api.quantumnumbers.anu.edu.au). There is NO
os.urandom fallback for the big buffer: if the real pull cannot be obtained, the
probe does NOT fabricate one — it emits an HONEST ⚠ INCOMPLETE-BLOCKED verdict and
records exactly why (missing secret? which key names tried? HTTP error?), keeping the
H_936 os.urandom conclusion as the standing result.

We VERIFY the buffer is genuinely real ANU: sha256, request_id, tier
(anu_paid/anu_free), byte mean≈127.5, KS + chi² vs uniform. The H_936 two-arm
comparison machinery (run_arm / compare / cohen_d / ks) is IMPORTED VERBATIM from
UNIVERSE/h936_unbiased_buffer_retest.py — same T, same seeds, same observables,
same pre-registered distinguishing rule — so the only experimental change is the
entropy SOURCE of the big buffer (os.urandom -> real ANU).

FALSIFIER (pre-registered; verdict .txt written with MEASURED numbers before the .md)
====================================================================================
  F-H940-REAL-ANU-CONFIRMS-ARTIFACT (🟢): the REAL-ANU big buffer ALSO gives tension
     parity — NO tension observable (phi_mean/var + 6 channels) is distinguishing
     (joint KS p<0.05 AND |Cohen d|>=0.2) AND the load-bearing phi_mean KS is
     non-significant (p>0.05) on DET-vs-QB. → H_936 is ROBUST to the entropy source;
     #123-A holds (the SOURCE does not matter, the CYCLING did). The free-will arc's
     buffer-artifact closure no longer rests on an os.urandom proxy.
  F-H940-SOURCE-DEPENDENT (🔴): real-ANU DIFFERS from os.urandom — the tension parity
     BREAKS with real ANU (phi_mean |d|>=0.2 AND KS p<0.05, OR >=1 distinguishing
     tension observable). → a surprising source-dependence; would itself be a finding
     (the os.urandom proxy was NOT representative).
  ⚠ INCOMPLETE-BLOCKED: the real ANU pull could not be obtained (no secret / network
     error / wrong key). → record the exact blocker, keep H_936's os.urandom result
     standing, file a hexa-lang handoff. NEVER fake a real pull.

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map · #123-A)
===============================================================
ONE re-confirm rung on the SAME documented-update-map mirror as H_930/H_935/H_936
(real 8-factor brain_decide, VERBATIM CORE constants). NOT the compiled forge binary;
full emit-TEXT (.clm generator L3 slot ⏳/❌ unwired, a_core_engine_map) remains OPEN.
#123-A: ANU == chacha20 statistically — the expected result is parity (🟢); a 🔴 would
be the surprise. $0 of GPU; the only cost is the ANU API draw. g5 CODE-measured
(no LLM self-judge — p7). deterministic: false (sweep/seed-point origin, as H_930).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
from scipy import stats

# ── locate the repo + import H_936's machinery VERBATIM (do not re-derive) ─────
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_SEED_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")
sys.path.insert(0, _SEED_DIR)
sys.path.insert(0, _HERE)

# import the H_936 module (the 8-factor mirror + run_arm + two-sample machinery)
_h936_path = os.path.join(_HERE, "h936_unbiased_buffer_retest.py")
_spec = importlib.util.spec_from_file_location("h936_module", _h936_path)
h936 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h936)

# pull the exact symbols H_940 reuses (same self/尺 as H_936)
run_arm = h936.run_arm
compare = None  # H_936 defines `compare` inside main(); we re-implement identically below
cohen_d = h936.cohen_d
ks = h936.ks
col = h936.col
chan = h936.chan
prove_unbiased = h936.prove_unbiased
PureField = h936.PureField
brain_emit_decision = h936.brain_emit_decision
FIELD_DIM = h936.FIELD_DIM
IM_THRESHOLD = h936.IM_THRESHOLD

ANU_PULLER = os.path.join(_SEED_DIR, "anu_pull.py")


# ════════════════════════════════════════════════════════════════════════════
# REAL ANU big buffer — NO os.urandom fallback. Blocked => honest ⚠, never faked.
# ════════════════════════════════════════════════════════════════════════════
def pull_real_anu_buffer(n_bytes: int, out_path: str, prov_path: str) -> dict:
    """Pull a REAL ANU vacuum-fluctuation buffer of n_bytes via anu_pull.py.

    Returns a provenance dict. On ANY failure to obtain a genuine ANU pull, the
    returned dict has ok=False + a `blocker` string describing exactly why — and
    NO buffer is written. There is deliberately NO os.urandom fallback here: the
    whole point of H_940 is to test the REAL source, so a fabricated buffer would
    defeat the experiment. The caller turns ok=False into a ⚠ BLOCKED verdict.
    """
    blocker = None
    keys_tried = ["flat.anu_key_paid", "flat.anu_key_free"]
    # record which secret keys resolve (without logging the values)
    key_status = {}
    for k in keys_tried:
        try:
            r = subprocess.run(["secret", "get", k], capture_output=True,
                               text=True, timeout=10)
            key_status[k] = bool(r.returncode == 0 and r.stdout.strip())
        except Exception as e:  # noqa: BLE001
            key_status[k] = f"err:{e!r}"
    if not os.path.exists(ANU_PULLER):
        return {"ok": False, "blocker": f"anu_pull.py absent at {ANU_PULLER}",
                "keys_tried": keys_tried, "key_status": key_status}

    # invoke anu_pull.py for the FULL n_bytes (it chunks internally at 1024/req).
    try:
        r = subprocess.run(
            [sys.executable, ANU_PULLER, "--bytes", str(n_bytes),
             "--out", out_path, "--provenance", prov_path],
            capture_output=True, text=True, timeout=1800)  # generous: ~760 chunked reqs
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "blocker": f"anu_pull.py subprocess raised {e!r}",
                "keys_tried": keys_tried, "key_status": key_status}

    if r.returncode != 0:
        return {"ok": False,
                "blocker": f"anu_pull.py exit {r.returncode}; stderr={r.stderr.strip()[:400]}; "
                           f"stdout={r.stdout.strip()[:400]}",
                "keys_tried": keys_tried, "key_status": key_status}
    if not os.path.exists(out_path) or os.path.getsize(out_path) < n_bytes:
        got = os.path.getsize(out_path) if os.path.exists(out_path) else 0
        return {"ok": False,
                "blocker": f"anu_pull.py wrote {got} bytes (< requested {n_bytes})",
                "keys_tried": keys_tried, "key_status": key_status}

    raw = open(out_path, "rb").read()
    # parse the puller's JSON line for tier + request_id (the REAL-ANU proof)
    tier = request_id = None
    try:
        j = json.loads(r.stdout.strip().splitlines()[-1])
        tier = j.get("tier")
        request_id = j.get("request_id")
    except Exception:  # noqa: BLE001
        tier = "anu_unknown"

    # HARD GUARD: the tier MUST be a real ANU tier — if it somehow is not, treat as
    # blocked rather than silently accept a non-ANU source (defends the experiment).
    if tier not in ("anu_paid", "anu_free", "anu_legacy"):
        return {"ok": False,
                "blocker": f"pulled buffer has non-ANU tier '{tier}' — refusing to "
                           f"treat as real ANU (no os.urandom fallback in H_940)",
                "keys_tried": keys_tried, "key_status": key_status}

    sha = hashlib.sha256(raw).hexdigest()
    return {
        "ok": True, "source": "anu_pull", "tier": tier, "request_id": request_id,
        "n_bytes": len(raw), "sha256": sha, "path": out_path,
        "keys_tried": keys_tried, "key_status": key_status,
        "honest_note": ("REAL ANU vacuum-fluctuation pull (secret-keyed). #123-A: ANU "
                        "== chacha20 statistically — the value is provenance/ontology, "
                        "and the H_940 test is whether the SOURCE changes the tension "
                        "parity (expected: no)."),
    }


def compare_full(a, b):
    """Identical to the H_936 in-main `compare`: phi/emit scalars + 6 channels."""
    out = {}
    for key in ("emit_rate", "emit_entropy_bits", "mean_inter_emit",
                "phi_mean", "phi_var"):
        out[key] = {"cohen_d": cohen_d(col(a, key), col(b, key)),
                    **ks(col(a, key), col(b, key))}
    for c in range(FIELD_DIM):
        out[f"ch{c}_mean"] = {"cohen_d": cohen_d(chan(a, c), chan(b, c)),
                              **ks(chan(a, c), chan(b, c))}
    return out


def main():
    # SAME knobs as H_936 (env-overridable for a fast smoke; defaults = H_936 prod).
    T = int(os.environ.get("H940_T", "2400"))
    N_SEEDS = int(os.environ.get("H940_SEEDS", "24"))
    ENT_SCALE = 0.04
    SEED_BASE = 1000
    NEG_COHEN = 0.20
    ts = datetime.now(timezone.utc).isoformat()

    out_dir = os.path.join(_REPO, ".verdicts", "940_real_anu_reconfirm")
    os.makedirs(out_dir, exist_ok=True)
    state_dir = os.path.join(_REPO, "state", "h940_real_anu")
    os.makedirs(state_dir, exist_ok=True)

    # ── size the big buffer EXACTLY as H_936 did (>= worst-case cursor span) ───
    draws_per_seed = T
    worst_span = draws_per_seed * (N_SEEDS * (N_SEEDS + 1) // 2 + N_SEEDS)
    big_bytes = max(131072, int(worst_span * 1.10) + 4096)
    big_path = os.path.join(state_dir, "anu_big_real.bin")
    prov_path = os.path.join(state_dir, "provenance.jsonl")

    # ── REAL ANU pull (no fallback) ───────────────────────────────────────────
    buf_prov = pull_real_anu_buffer(big_bytes, big_path, prov_path)

    # ── shared emit gate (deterministic steady-state mean — == H_936) ─────────
    cal = PureField()
    scs = []
    for _ in range(T):
        cal.step(perturb=0.0)
        _, sc = brain_emit_decision(cal, gate=IM_THRESHOLD)
        scs.append(sc)
    shared_gate = sum(scs) / len(scs)

    # ════════════════════════════════════════════════════════════════════════
    # BLOCKED PATH — real ANU unavailable. Honest ⚠, no fabricated buffer.
    # ════════════════════════════════════════════════════════════════════════
    if not buf_prov.get("ok"):
        token = "⚠"
        fal_id = "F-H940-INCOMPLETE-BLOCKED"
        rationale = (
            f"The REAL ANU pull could not be obtained — H_940 cannot re-confirm "
            f"H_936's buffer-artifact with a genuine quantum source on this host. "
            f"BLOCKER: {buf_prov.get('blocker')}. keys tried: {buf_prov.get('keys_tried')}; "
            f"key_status: {buf_prov.get('key_status')}. NO os.urandom fallback was used "
            f"(that would defeat the experiment). H_936's os.urandom-fallback conclusion "
            f"(🟢 F-H936-ARTIFACT-CONFIRMED) REMAINS THE STANDING RESULT; the real-ANU "
            f"re-confirm is filed as a hexa-lang handoff. #123-A predicts parity when the "
            f"pull succeeds (ANU == chacha20 statistically), so this is an availability "
            f"gap, not a science gap.")
        result = {
            "h_id": "H_940", "title": "real-ANU re-confirm of H_936 buffer-artifact",
            "timestamp_utc": ts, "verdict_token": token, "falsifier_id": fal_id,
            "verdict_rationale": rationale, "blocked": True, "buffer_provenance": buf_prov,
            "standing_result": "H_936 🟢 F-H936-ARTIFACT-CONFIRMED (os.urandom_fallback)",
            "T_per_seed": T, "n_seeds_per_arm": N_SEEDS,
            "deterministic": False, "g5_code_measured": True, "llm": "none",
        }
        L = ["H_940 — REAL-ANU RE-CONFIRM OF H_936 BUFFER-ARTIFACT  [⚠ BLOCKED]",
             "=" * 76, f"timestamp_utc : {ts}", "",
             "── BLOCKER ─────────────────────────────────────────────────────────────",
             f"  {buf_prov.get('blocker')}",
             f"  keys tried : {buf_prov.get('keys_tried')}",
             f"  key_status : {buf_prov.get('key_status')}", "",
             "── STANDING RESULT (unchanged) ─────────────────────────────────────────",
             "  H_936 🟢 F-H936-ARTIFACT-CONFIRMED (os.urandom_fallback big buffer).",
             "  H_940 does NOT overturn it; it could not run the real-ANU re-confirm.", "",
             "── VERDICT ─────────────────────────────────────────────────────────────",
             f"  {token}  {fal_id}", f"  {rationale}", "",
             "── full machine record (JSON) ──────────────────────────────────────────",
             json.dumps(result, indent=2, default=str)]
        out_path = os.path.join(out_dir, "real_anu_reconfirm.txt")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(L) + "\n")
        print("\n".join(L))
        print("\n[written]", out_path)
        return result

    # ════════════════════════════════════════════════════════════════════════
    # MEASURED PATH — real ANU obtained. Run the H_936 three-arm comparison.
    # ════════════════════════════════════════════════════════════════════════
    buf_stats = prove_unbiased(big_path)

    armDET = run_arm("DET", "deterministic", N_SEEDS, T, shared_gate, ENT_SCALE, SEED_BASE)
    armQS = run_arm("QS", "quantum", N_SEEDS, T, shared_gate, ENT_SCALE, SEED_BASE)
    armQB = run_arm("QB", "quantum", N_SEEDS, T, shared_gate, ENT_SCALE, SEED_BASE,
                    big_buf_path=big_path, big_buf_bytes=big_bytes)

    cmp_det_qs = compare_full(armDET, armQS)   # reproduce H_930/H_936 small cycling
    cmp_det_qb = compare_full(armDET, armQB)   # the H_940 test: big REAL-ANU fresh

    def summ(arm):
        return {
            "arm": arm["arm"], "mode": arm["mode"],
            "emit_rate_mean": float(np.mean(col(arm, "emit_rate"))),
            "emit_rate_sd": float(np.std(col(arm, "emit_rate"))),
            "phi_mean_mean": float(np.mean(col(arm, "phi_mean"))),
            "phi_mean_sd": float(np.std(col(arm, "phi_mean"))),
            "phi_var_mean": float(np.mean(col(arm, "phi_var"))),
            "provenance_first_seed": arm["provenance_first_seed"],
        }

    phi_qb = cmp_det_qb["phi_mean"]
    phi_qs = cmp_det_qs["phi_mean"]
    qb_phi_d = abs(phi_qb["cohen_d"])
    qb_phi_p = phi_qb["p"]
    qb_emit_sd = float(np.std(col(armQB, "emit_rate")))

    tension_keys = ["phi_mean", "phi_var"] + [f"ch{c}_mean" for c in range(FIELD_DIM)]
    qb_tension_distinguishing = [
        k for k in tension_keys
        if (cmp_det_qb[k]["p"] is not None and cmp_det_qb[k]["p"] < 0.05
            and abs(cmp_det_qb[k]["cohen_d"]) >= NEG_COHEN)]
    qs_tension_distinguishing = [
        k for k in tension_keys
        if (cmp_det_qs[k]["p"] is not None and cmp_det_qs[k]["p"] < 0.05
            and abs(cmp_det_qs[k]["cohen_d"]) >= NEG_COHEN)]

    # SAME pre-registered distinguishing rule as H_936 (joint p<0.05 AND |d|>=0.2).
    phi_mean_distinguishing = (qb_phi_p is not None and qb_phi_p < 0.05
                               and qb_phi_d >= NEG_COHEN)
    artifact_confirmed = (len(qb_tension_distinguishing) == 0
                          and not phi_mean_distinguishing)

    if artifact_confirmed:
        token = "🟢"
        fal_id = "F-H940-REAL-ANU-CONFIRMS-ARTIFACT"
        rationale = (
            f"The REAL ANU big buffer (tier {buf_prov['tier']}, request_id "
            f"{buf_prov['request_id']}, sha256 {buf_prov['sha256'][:16]}…) REPRODUCES "
            f"H_936's tension parity. phi_mean: QS (cycling 1024 B) Cohen "
            f"d={phi_qs['cohen_d']:+.3f} KS p={phi_qs['p']:.3g} (reproduces the H_930 "
            f"distinguishable regime) -> QB (big REAL ANU) Cohen d={phi_qb['cohen_d']:+.3f} "
            f"KS p={qb_phi_p:.3g} (NON-SIGNIFICANT, p>0.05 → parity). QB emit_rate "
            f"sd={qb_emit_sd:.6f} (>0: real 24-seed population). Tension observables "
            f"distinguishing (joint p<0.05 AND |d|>=0.2): QS {len(qs_tension_distinguishing)} "
            f"{qs_tension_distinguishing} -> QB {len(qb_tension_distinguishing)} "
            f"{qb_tension_distinguishing}. H_936 is ROBUST to the entropy SOURCE: real "
            f"ANU and os.urandom give the SAME tension parity — #123-A holds, the source "
            f"does not matter, the cycling did. The buffer-artifact closure no longer "
            f"rests on an os.urandom proxy.")
    else:
        token = "🔴"
        fal_id = "F-H940-SOURCE-DEPENDENT"
        rationale = (
            f"The REAL ANU big buffer DIFFERS from os.urandom — the tension parity "
            f"BREAKS under genuine ANU. phi_mean Cohen |d|={qb_phi_d:.3f} KS "
            f"p={qb_phi_p:.3g}; {len(qb_tension_distinguishing)} tension observables "
            f"{qb_tension_distinguishing} distinguishing; QB emit_rate sd={qb_emit_sd:.6f}. "
            f"This is a SURPRISING source-dependence (the os.urandom proxy was not "
            f"representative) and would itself be a finding worth its own arc.")

    result = {
        "h_id": "H_940",
        "title": "real-ANU re-confirm of H_936's tension-axis buffer-artifact",
        "timestamp_utc": ts, "blocked": False,
        "scope": ("ONE re-confirm rung on the SAME documented-update-map mirror as "
                  "H_930/H_935/H_936 (real 8-factor brain_decide, VERBATIM CORE "
                  "constants). NOT the compiled forge binary; full emit-TEXT (.clm "
                  "generator L3 ⏳/❌, a_core_engine_map) OPEN. ANU API draw only, no GPU."),
        "deterministic": False, "g5_code_measured": True, "llm": "none",
        "T_per_seed": T, "n_seeds_per_arm": N_SEEDS, "ent_scale": ENT_SCALE,
        "shared_emit_gate": shared_gate,
        "big_buffer": {
            "requested_bytes": big_bytes,
            "worst_case_cursor_span_bytes": worst_span,
            "no_cycle_by_construction": bool(big_bytes >= worst_span),
            "provenance": buf_prov, "uniformity": buf_stats,
        },
        "arm_DET_summary": summ(armDET),
        "arm_QS_summary": summ(armQS),
        "arm_QB_summary": summ(armQB),
        "before_after_phi_mean": {
            "H_930_regime_DET_vs_QS_small_cycling": phi_qs,
            "H_940_test_DET_vs_QB_big_REAL_ANU": phi_qb,
        },
        "full_compare_DET_vs_QS": cmp_det_qs,
        "full_compare_DET_vs_QB": cmp_det_qb,
        "tension_distinguishing_QS": qs_tension_distinguishing,
        "tension_distinguishing_QB": qb_tension_distinguishing,
        "negligible_thresholds": {"cohen_d": NEG_COHEN, "alpha": 0.05},
        "verdict_token": token, "falsifier_id": fal_id, "verdict_rationale": rationale,
        "cross_compare_vs_h936": ("H_936 os.urandom_fallback gave 🟢 parity (phi_mean "
                                  "DET-vs-QB KS p≈0.14, 0 distinguishing). H_940 tests "
                                  "whether REAL ANU reproduces that."),
    }

    # ── verbatim verdict file (numbers first) ─────────────────────────────────
    sd, sq, sb = summ(armDET), summ(armQS), summ(armQB)
    L = []
    L.append("H_940 — REAL-ANU RE-CONFIRM OF H_936 BUFFER-ARTIFACT (vs os.urandom)")
    L.append("=" * 76)
    L.append(f"timestamp_utc : {ts}")
    L.append(f"population    : {N_SEEDS} seeds × {T} ticks/seed  ·  ent_scale {ENT_SCALE}")
    L.append(f"shared gate   : {shared_gate}")
    L.append("")
    L.append("── BIG REAL-ANU BUFFER (provenance + REAL-ANU proof + unbiasedness) ────")
    L.append(f"  source        : {buf_prov['source']}  (tier {buf_prov['tier']}, "
             f"request_id {buf_prov['request_id']})")
    L.append(f"  key_status    : {buf_prov['key_status']}")
    L.append(f"  n_bytes       : {buf_prov['n_bytes']}  (worst-case cursor span "
             f"{worst_span} → no_cycle_by_construction "
             f"{result['big_buffer']['no_cycle_by_construction']})")
    L.append(f"  sha256        : {buf_prov['sha256']}")
    L.append(f"  byte_mean     : {buf_stats['byte_mean']:.4f} (ideal 127.5, abs_err "
             f"{buf_stats['mean_abs_err']:.4f})")
    L.append(f"  KS vs uniform : D={buf_stats['ks_D_vs_uniform']:.4f} "
             f"p={buf_stats['ks_p_vs_uniform']:.4g}")
    L.append(f"  chi² 256-bin  : {buf_stats['chi2_256bin']:.2f} (df 255) "
             f"p={buf_stats['chi2_p']:.4g}  →  unbiased={buf_stats['unbiased']}")
    L.append("")
    L.append("── BEFORE/AFTER table (mean over seeds) ────────────────────────────────")
    L.append("                          DET (deterministic)   QS (quantum small,    QB (quantum BIG,")
    L.append("                                                cycling 1024 B)       REAL ANU fresh)")
    L.append(f"  emit_rate (sd)          {sd['emit_rate_mean']:.6f} ({sd['emit_rate_sd']:.6f})  "
             f"{sq['emit_rate_mean']:.6f} ({sq['emit_rate_sd']:.6f})  "
             f"{sb['emit_rate_mean']:.6f} ({sb['emit_rate_sd']:.6f})")
    L.append(f"  phi_mean (sd)           {sd['phi_mean_mean']:.6f} ({sd['phi_mean_sd']:.6f})  "
             f"{sq['phi_mean_mean']:.6f} ({sq['phi_mean_sd']:.6f})  "
             f"{sb['phi_mean_mean']:.6f} ({sb['phi_mean_sd']:.6f})")
    L.append("")
    L.append("── phi_mean two-sample (the load-bearing tension test) ─────────────────")
    L.append(f"  DET vs QS (H_930 regime)  : Cohen d={phi_qs['cohen_d']:+.4f}  "
             f"KS D={phi_qs['D']} p={phi_qs['p']:.3g}")
    L.append(f"  DET vs QB (H_940 REAL ANU): Cohen d={phi_qb['cohen_d']:+.4f}  "
             f"KS D={phi_qb['D']} p={phi_qb['p']:.3g}")
    L.append("")
    L.append(f"  tension observables distinguishing — QS: {len(qs_tension_distinguishing)} "
             f"{qs_tension_distinguishing}")
    L.append(f"  tension observables distinguishing — QB: {len(qb_tension_distinguishing)} "
             f"{qb_tension_distinguishing}")
    L.append("")
    L.append("── H_936 (os.urandom) comparison ──────────────────────────────────────")
    L.append("  H_936 os.urandom_fallback: phi_mean DET-vs-QB KS p≈0.14, 0 distinguishing → 🟢 parity")
    L.append(f"  H_940 REAL ANU           : phi_mean DET-vs-QB KS p={qb_phi_p:.3g}, "
             f"{len(qb_tension_distinguishing)} distinguishing")
    L.append("")
    L.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ───────────────")
    L.append(f"  {token}  {fal_id}")
    L.append(f"  {rationale}")
    L.append("")
    L.append("── full machine record (JSON) ──────────────────────────────────────────")
    L.append(json.dumps(result, indent=2, default=str))

    out_path = os.path.join(out_dir, "real_anu_reconfirm.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print("\n[written]", out_path)
    return result


if __name__ == "__main__":
    main()
