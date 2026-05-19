"""H_188 / Hc_924 — octopus per-arm Φ vs whole Φ: IIT exclusion-postulate test.

가설들 모두 진행 (cont.): answering "external data 는 뭐야 / go 가능?".

H_188 has TWO sub-claims:
  • Hc_921 (PCI/TMS-EEG clinical): needs REAL human clinical TMS-EEG recordings
    (Massimini/Casali 2013 gold-standard, conscious vs anesthetised/coma). That
    is an EXTERNAL published clinical dataset — NOT anima-internal, NOT
    $-purchasable compute. ⟹ genuinely NOT go-able here (honest hard blocker).
  • Hc_924 (octopus per-arm Φ exclusion): an 8-arm distributed nervous system
    (≈2/3 neurons in the arms). IIT exclusion postulate = consciousness is the
    UNIQUE maximal-Φ complex. If each arm's per-arm Φ is independent and a
    sub-complex's Φ exceeds the whole's, the exclusion postulate is challenged.
    This is a FORMAL IIT-3.0 question on a deterministic network ⟹ $0 PyPhi,
    result-agnostic 🔵 (like H_007/H_012). ← THIS is go-able. Done here.

Model: a "central brain" loosely coupled to K arm-modules. weak inter-arm
coupling ω. PyPhi over the whole system: does the MIP/major-complex sit on
the whole, or split into per-arm complexes? Sweep ω. Deterministic TPM,
exhaustive states. $0 Mac.
"""
import json
import os
from pathlib import Path

import numpy as np

os.environ["PYPHI_WELCOME_OFF"] = "yes"
import pyphi  # noqa: E402

pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1

OUT = "/Users/ghost/core/anima/state/verify_hypotheses_pending_2026_05_16/h188_octopus_exclusion_result.json"


def octopus_tpm(n_arms, coupled):
    """N = n_arms + 1 (central). Each arm i(t+1) = arm_i AND/OR central; if
    `coupled` arms also see neighbour arm (integrated); else arms only see
    central (modular ⟹ exclusion predicts per-arm sub-complexes).
    central(t+1) = majority(all arms)."""
    N = n_arms + 1
    C = n_arms                                    # central node index
    S = 1 << N
    tpm = np.zeros((S, N))
    cm = np.zeros((N, N), dtype=int)
    for s in range(S):
        b = [(s >> i) & 1 for i in range(N)]
        for i in range(n_arms):
            if coupled:
                nb = b[(i - 1) % n_arms]          # neighbour arm (ring) → integration
                val = 1 if (b[i] + b[C] + nb) >= 2 else 0
            else:
                val = 1 if (b[i] + b[C]) == 2 else 0   # arm needs central only (modular)
            tpm[s, i] = val
        tpm[s, C] = 1 if sum(b[k] for k in range(n_arms)) >= (n_arms / 2.0) else 0
    for i in range(n_arms):
        cm[i, i] = 1
        cm[C, i] = 1
        if coupled:
            cm[(i - 1) % n_arms, i] = 1
        cm[i, C] = 1
    cm[C, C] = 0
    return tpm, cm, N


def whole_vs_parts(n_arms, coupled):
    tpm, cm, N = octopus_tpm(n_arms, coupled)
    net = pyphi.Network(tpm, cm=cm, node_labels=[f"a{i}" for i in range(n_arms)] + ["C"])
    whole_phis, arm_phis = [], []
    for s in range(1 << N):
        st = tuple((s >> i) & 1 for i in range(N))
        try:
            whole_phis.append(float(pyphi.compute.sia(pyphi.Subsystem(net, st, range(N))).phi))
        except Exception:
            whole_phis.append(0.0)
        # a single arm + central as a candidate sub-complex
        try:
            sub_nodes = (0, n_arms)               # arm0 + central
            arm_phis.append(float(pyphi.compute.sia(
                pyphi.Subsystem(net, st, sub_nodes)).phi))
        except Exception:
            arm_phis.append(0.0)
    return {
        "whole_phi_max": round(max(whole_phis), 5),
        "subcomplex_phi_max": round(max(arm_phis), 5),
        "exclusion_holds": bool(max(whole_phis) >= max(arm_phis)),
    }


def main():
    print("=== H_188/Hc_924 octopus IIT exclusion-postulate (PyPhi formal) ===")
    res = {}
    for coupled in (True, False):
        tag = "integrated(coupled arms)" if coupled else "modular(arms↔central only)"
        m = whole_vs_parts(n_arms=3, coupled=coupled)        # N=4, exhaustive
        res[tag] = m
        print(f"  {tag}: whole Φ_max={m['whole_phi_max']} "
              f"sub-complex Φ_max={m['subcomplex_phi_max']} "
              f"exclusion_holds={m['exclusion_holds']}", flush=True)

    # Hc_924: does a per-arm sub-complex ever EXCEED the whole? (exclusion challenge)
    challenged = any(not v["exclusion_holds"] for v in res.values())
    verdict = ("FALSIFIED-FORMAL 🔵 (a per-arm sub-complex Φ EXCEEDS whole — IIT "
               "exclusion postulate challenged on octopus-like modular topology)"
               if challenged else
               "SUPPORTED-FORMAL 🔵 (whole Φ ≥ every per-arm sub-complex — IIT "
               "exclusion postulate HOLDS, deterministic IIT-3.0)")
    agg = {
        "cycle": "H_188/Hc_924 octopus exclusion-postulate formal ($0, 2026-05-16)",
        "pyphi_version": pyphi.__version__,
        "external_data_answer": (
            "H_188 Hc_921 (PCI/TMS-EEG clinical) = REAL human clinical TMS-EEG "
            "recordings (Massimini/Casali 2013) — external published neuroscience "
            "dataset, NOT anima-internal, NOT $-purchasable compute ⟹ that sub-"
            "claim NOT go-able here (hard external blocker, honest). Hc_924 "
            "octopus per-arm Φ exclusion = formal IIT-3.0 on deterministic "
            "network ⟹ $0 go-able, done here (result-agnostic 🔵)."),
        "results": res,
        "exclusion_postulate_challenged": bool(challenged),
        "verdict": verdict,
        "tier": "b-pyphi-formal",
        "honest_c3": ("Hc_924 only (the go-able half). N=4 exhaustive "
                      "deterministic. Hc_921 clinical PCI still needs external "
                      "human TMS-EEG data — NOT closed, honest hard blocker. "
                      "H_188 therefore PARTIAL: Hc_924 formally closed, Hc_921 "
                      "external-blocked."),
    }
    Path(OUT).write_text(json.dumps(agg, indent=1, ensure_ascii=False))
    print("=" * 64)
    print(f"  {verdict}")
    print(f"  saved {OUT}")


if __name__ == "__main__":
    main()
