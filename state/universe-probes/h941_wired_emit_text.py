#!/usr/bin/env python3
"""h941_wired_emit_text.py — H_941: WIRED emit-TEXT rung — quantum-vs-deterministic
A/B at the REAL TOKEN layer, via the .clm generator L3 decode path.

QUESTION (extends H_930/H_936 from internal substrate scalars to REAL TEXT)
==========================================================================
H_930/H_936 closed the quantum-vs-deterministic question on the SUBSTRATE side
(emit-decision parity 🟢; tension parity 🟢 after the buffer-artifact was removed).
But both measured INTERNAL observables (emit rate, phi_mean, field channels) — NOT
the actual emitted TEXT. H_930 explicitly left the emit-TEXT rung OPEN (`a_core_engine_map`:
.clm enters CORE only via the generator L3 slot; that wiring was ⏳/❌ in H_930).

H_941 asks: when an emit event is actually DECODED to tokens through the .clm
generator path, does the entropy MODE (quantum vs deterministic) at the sampling
seed-point change the GENERATED TEXT distribution — or is the token stream
INDISTINGUISHABLE across modes (H_930 parity extends to the text layer)?

THE WIRING UNDER TEST (this is H_941's sharpening over H_930/H_936)
==================================================================
emit event  ->  seed/context  ->  .clm decode (generator L3)  ->  token stream.
On macOS the canonical hexa engine-mount (CORE/clm_decode.hexa -> forge native) is
BLOCKED by a toolchain link-gap (memory: clm-decode-macos-link-gap — the fused
`forge_dispatch_groupnorm_gelu` native is absent from the installed self runtime).
The SANCTIONED Mac workaround is `state/mid_convmoe_fire/clm_decode_mirror.py`, a
BYTE-EXACT pure-numpy mirror of clm_decode.hexa's forward, validated == engine on
the golden artifact. H_941 IMPORTS that mirror's `fwd_logits` (the real serialized
.clm forward) and adds AUTOREGRESSIVE SAMPLING on top: at each generation step the
next-token RNG is seeded by `qentropy` under the active ANIMA_ENTROPY_MODE, so the
ONLY thing that differs between the two arms is the entropy SOURCE at the sampling
seed-point — exactly the H_930/H_936 lever, now at the token layer.

This is NOT the compiled forge binary and NOT the .hexa generator linked natively;
it is the byte-exact Python mirror of that decode (honest fidelity boundary, same as
H_936's documented-update-map mirror). The .clm artifact itself is the REAL
serialized engine-loadable v0.2 artifact. We do NOT fabricate tokens — every token
is argmax/sampled from the real .clm logits.

FALSIFIER (pre-registered; verdict .txt written with MEASURED numbers before the .md)
====================================================================================
  F-H941-EMIT-TEXT-PARITY (🟢): the pipeline RUNS end-to-end (emit -> .clm decode ->
     tokens) AND the generated token streams are INDISTINGUISHABLE across entropy
     modes — token-frequency chi² p>=0.05 AND per-stream sequence-entropy two-sample
     KS p>=0.05 AND mean |Cohen d| on sequence entropy < 0.2. → H_930's
     quantum-ontological-not-functional result EXTENDS to the real text layer: the
     entropy source does not change WHAT she says, only the provenance.
  F-H941-TEXT-FUNCTIONAL (🔴): the token streams DIFFER across modes (token chi²
     p<0.05 OR seq-entropy KS p<0.05 with |d|>=0.2). → entropy is functional at the
     text layer (a finding worth its own arc; would contradict H_930/H_936 parity).
  ⚠ INCOMPLETE-BLOCKED: the wiring genuinely cannot run (no loadable .clm / mirror
     can't decode / generator L3 absent). → document precisely, mark the native hexa
     wiring ❌ honestly (a_core_engine_map: no phantom wiring), keep H_930's substrate
     parity standing, file a hexa-lang handoff. NEVER fabricate tokens.

HONEST SCOPE (a_core_engine_map · a_clm_gen_pipeline · clm-decode-macos-link-gap)
================================================================================
The .clm enters via the generator L3 decode SEMANTICS (byte-exact mirror on Mac, not
the native forge link). The artifact is a real engine-loadable v0.2 .clm. Greedy/temp
sampling on real logits; entropy MODE only touches the sampling RNG seed-point. g5
CODE-measured (no LLM self-judge — p7). $0, no GPU. deterministic: false (quantum arm
reads a non-deterministic seed origin). substrate tag: Lane-P .clm decode (CPU-mirror).
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import math
import os
import sys
from collections import Counter
from datetime import datetime, timezone

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_SEED_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")
_MIRROR_DIR = os.path.join(_REPO, "state", "mid_convmoe_fire")
sys.path.insert(0, _SEED_DIR)
sys.path.insert(0, _MIRROR_DIR)

# ── import the BYTE-EXACT .clm decode mirror (the real serialized-.clm forward) ──
_mir_path = os.path.join(_MIRROR_DIR, "clm_decode_mirror.py")
_spec = importlib.util.spec_from_file_location("clm_decode_mirror", _mir_path)
mir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mir)
load_clm = mir.load_clm
fwd_logits = mir.fwd_logits


# ── candidate engine-loadable .clm artifacts (golden first, then any v0.2) ──────
def find_clm() -> str | None:
    cands = [
        os.path.join(_REPO, "state", "laneg_d768_recover", "reexport_d768_v2_fast.clm"),
        os.path.join(_REPO, "state", "lane_p_clm", "clm_d768_e2l1.clm"),
        os.path.join(_REPO, "state", "lane_p_clm_gen", "clm_d768_gen.clm"),
        os.path.join(_REPO, "exports", "lane-g-d768", "d768_5lang_c4.clm"),
    ]
    for c in cands:
        if os.path.exists(c) and os.path.getsize(c) > 1024:
            return c
    return None


def softmax_temp(logit_row: np.ndarray, temp: float) -> np.ndarray:
    z = logit_row / max(temp, 1e-6)
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def generate_stream(W, prompt, n_new, temp, rng_gen, T):
    """Autoregressive sampling on the REAL .clm logits.

    The .clm decode uses a fixed T-position window (T=24, == the engine probe). We
    keep a rolling window of the last T tokens, take the logits at the LAST window
    position (the next-byte prediction), and sample with `rng_gen` (whose seed came
    from the active entropy MODE — quantum or deterministic). Every token is sampled
    from REAL .clm logits; nothing is fabricated.
    """
    V = W["V"]
    ctx = list(prompt)
    out = []
    for _ in range(n_new):
        window = ctx[-T:]
        if len(window) < T:                       # left-pad with byte 32 (space)
            window = [32] * (T - len(window)) + window
        logits = fwd_logits(W, np.array(window, dtype=float), T)
        p = softmax_temp(logits[T - 1], temp)
        tok = int(rng_gen.choice(V, p=p))
        out.append(tok)
        ctx.append(tok)
    return out


def run_arm(W, mode_env, n_streams, n_new, temp, prompt, seed_base, T,
            big_buf_path=None):
    """Generate n_streams token streams under one entropy MODE.

    Each stream's sampling RNG is seeded by qentropy under ANIMA_ENTROPY_MODE — so
    the deterministic arm is reproducible (PRNG seed) and the quantum arm draws its
    seed from the ANU/quantum buffer. The .clm forward is identical across arms; the
    ONLY difference is the seed SOURCE (the H_930/H_936 lever, now at the token layer).

    CRITICAL (H_936 single-pattern fix): in quantum mode each stream must read an
    INDEPENDENT, NON-OVERLAPPING slice of a large fresh buffer — otherwise every
    stream reads the SAME committed-buffer position and the 24 quantum streams are
    24 identical copies of one pattern (sd≈0), which would FAKE an entropy effect.
    We point ANIMA_QRNG_BUF at a big fresh buffer and burn s*64 bytes per stream so
    the quantum arm is a GENUINE 24-stream population, exactly as H_936's run_arm did.
    The deterministic arm already varies via ANIMA_ENTROPY_SEED=seed_base+s.
    """
    streams = []
    prov_first = None
    mode_seen = None
    burn_per_stream = 64  # bytes burned per stream to advance to an independent slice
    for s in range(n_streams):
        os.environ["ANIMA_ENTROPY_MODE"] = mode_env
        os.environ["ANIMA_ENTROPY_SEED"] = str(seed_base + s)
        if mode_env == "quantum" and big_buf_path is not None:
            os.environ["ANIMA_QRNG_BUF"] = big_buf_path
        else:
            os.environ.pop("ANIMA_QRNG_BUF", None)
        import qentropy  # noqa: PLC0415
        importlib.reload(qentropy)
        mode_seen = qentropy.mode()
        # advance to a per-stream independent slice (the H_936 population fix)
        if mode_seen == "quantum" and s > 0:
            _ = qentropy.qentropy_bytes(s * burn_per_stream, label=f"h941_burn_{s}")
        rng_gen = qentropy.rng(label=f"h941_gen_{mode_env}_s{s}")
        if prov_first is None:
            prov_first = qentropy.last_provenance()
        toks = generate_stream(W, prompt, n_new, temp, rng_gen, T)
        streams.append(toks)
    return {"mode_env": mode_env, "mode_seen": mode_seen, "streams": streams,
            "provenance_first": prov_first}


def token_histogram(streams, V):
    c = Counter()
    for s in streams:
        c.update(s)
    return np.array([c.get(i, 0) for i in range(V)], dtype=float)


def seq_entropy(stream):
    """Shannon entropy (bits) of one token stream's symbol distribution."""
    c = Counter(stream)
    n = len(stream)
    return -sum((v / n) * math.log2(v / n) for v in c.values())


def cohen_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = math.sqrt(((na - 1) * va + (nb - 1) * vb) / max(na + nb - 2, 1)) or 1e-12
    return (a.mean() - b.mean()) / sp


def main():
    T = 24
    N_STREAMS = int(os.environ.get("H941_STREAMS", "24"))
    N_NEW = int(os.environ.get("H941_NEW", "48"))
    TEMP = float(os.environ.get("H941_TEMP", "1.0"))
    SEED_BASE = 1000
    NEG = 0.20
    ts = datetime.now(timezone.utc).isoformat()
    prompt = [84, 104, 101, 32, 109, 105, 110, 100, 32, 105, 115, 32]  # "The mind is "

    out_dir = os.path.join(_REPO, ".verdicts", "941_wired_emit_text")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "wired_emit_text.txt")

    # ── locate a real engine-loadable .clm; BLOCKED if none ──────────────────────
    clm_path = find_clm()
    if clm_path is None:
        token = "⚠"
        fal_id = "F-H941-INCOMPLETE-BLOCKED"
        rationale = (
            "No engine-loadable .clm artifact is present in this worktree (golden "
            "reexport_d768_v2_fast.clm + lane_p_clm/*.clm absent — they are gitignored "
            "local-only ckpts, a_hf_registry). The emit-TEXT wiring cannot run without a "
            "real .clm to decode; per a_core_engine_map NO phantom wiring is claimed and "
            "NO tokens are fabricated. H_930/H_936's substrate-side parity REMAINS the "
            "standing result; the emit-TEXT rung is filed as a hexa-lang handoff.")
        L = ["H_941 — WIRED EMIT-TEXT RUNG  [⚠ BLOCKED]", "=" * 72,
             f"timestamp_utc : {ts}", "",
             "── BLOCKER ──────────────────────────────────────────────────────────",
             "  no engine-loadable .clm artifact found (gitignored local-only).", "",
             "── VERDICT ──────────────────────────────────────────────────────────",
             f"  {token}  {fal_id}", f"  {rationale}"]
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(L) + "\n")
        print("\n".join(L)); print("\n[written]", out_path)
        return {"verdict_token": token, "blocked": True}

    # ── load + sanity-decode the .clm via the byte-exact mirror ──────────────────
    W = load_clm(clm_path)
    V = W["V"]

    # ── provision a BIG fresh quantum buffer so the quantum arm is a genuine
    #    24-stream population (per-stream independent slice; H_936 single-pattern fix).
    #    Each stream burns up to (N_STREAMS*64) bytes + draws ~8 seed bytes; size with
    #    generous headroom so there is NO cycling within the arm. Prefer a real ANU
    #    pull (secret-keyed); if unavailable, fall back to os.urandom and TAG it (the
    #    cycling-free population is what matters here, not the source — #123-A). ──────
    state_dir = os.path.join(_REPO, "state", "h941_emit_text")
    os.makedirs(state_dir, exist_ok=True)
    big_path = os.path.join(state_dir, "qbuf_big.bin")
    burn_total = sum(s * 64 for s in range(N_STREAMS)) + N_STREAMS * 64
    big_bytes = max(131072, burn_total + 65536)
    buf_source = None
    import subprocess  # noqa: PLC0415
    anu_puller = os.path.join(_SEED_DIR, "anu_pull.py")
    try:
        r = subprocess.run([sys.executable, anu_puller, "--bytes", str(big_bytes),
                            "--out", big_path,
                            "--provenance", os.path.join(state_dir, "provenance.jsonl")],
                           capture_output=True, text=True, timeout=1800)
        if r.returncode == 0 and os.path.exists(big_path) and os.path.getsize(big_path) >= big_bytes:
            j = json.loads(r.stdout.strip().splitlines()[-1])
            buf_source = {"source": "anu_pull", "tier": j.get("tier"),
                          "request_id": j.get("request_id"), "n_bytes": big_bytes}
    except Exception as e:  # noqa: BLE001
        buf_source = {"source": "anu_pull_failed", "err": repr(e)}
    if buf_source is None or buf_source.get("source") != "anu_pull":
        with open(big_path, "wb") as fh:
            fh.write(os.urandom(big_bytes))
        buf_source = {"source": "os.urandom_fallback", "tier": "os_urandom",
                      "n_bytes": big_bytes,
                      "note": ("real ANU unavailable; cycling-free population is what "
                               "matters for the single-pattern fix — #123-A ANU==chacha20")}

    # ── run BOTH entropy arms at the TOKEN layer ─────────────────────────────────
    armDET = run_arm(W, "deterministic", N_STREAMS, N_NEW, TEMP, prompt, SEED_BASE, T)
    armQ = run_arm(W, "quantum", N_STREAMS, N_NEW, TEMP, prompt, SEED_BASE, T,
                   big_buf_path=big_path)

    # ── token-frequency chi² (pooled streams) ────────────────────────────────────
    hd = token_histogram(armDET["streams"], V)
    hq = token_histogram(armQ["streams"], V)
    # restrict to symbols that appear in EITHER arm; merge tiny bins (exp<5) to keep
    # chi² valid (standard rule), comparing the two arms' token distributions.
    support = [i for i in range(V) if hd[i] + hq[i] > 0]
    od = np.array([hd[i] for i in support], float)
    oq = np.array([hq[i] for i in support], float)
    tot = od.sum() + oq.sum()
    exp_d = (od + oq) * od.sum() / tot
    exp_q = (od + oq) * oq.sum() / tot
    # collapse bins where either expected < 5 into an "other" bin (chi² validity)
    keep = (exp_d >= 5) & (exp_q >= 5)
    od_k = list(od[keep]); oq_k = list(oq[keep])
    od_k.append(od[~keep].sum()); oq_k.append(oq[~keep].sum())
    obs = np.array([od_k, oq_k])
    obs = obs[:, obs.sum(axis=0) > 0]
    chi2, chi2_p, dof, _ = stats.chi2_contingency(obs)

    # ── per-stream sequence entropy two-sample (KS + Cohen d) ────────────────────
    ent_d = [seq_entropy(s) for s in armDET["streams"]]
    ent_q = [seq_entropy(s) for s in armQ["streams"]]
    ks_D, ks_p = stats.ks_2samp(ent_d, ent_q)
    ent_d_arr = np.array(ent_d); ent_q_arr = np.array(ent_q)
    ent_cd = cohen_d(ent_d, ent_q)

    # pre-registered distinguishing rule
    token_distinguishing = (chi2_p is not None and chi2_p < 0.05)
    entropy_distinguishing = (ks_p is not None and ks_p < 0.05 and abs(ent_cd) >= NEG)
    indistinguishable = (not token_distinguishing) and (not entropy_distinguishing)

    # decode a couple of sample streams to bytes for the record (real tokens, not faked)
    def to_text(toks):
        return bytes(t if 32 <= t < 127 else ord(".") for t in toks).decode("ascii")
    sample_det = to_text(armDET["streams"][0][:48])
    sample_q = to_text(armQ["streams"][0][:48])

    if indistinguishable:
        token = "🟢"
        fal_id = "F-H941-EMIT-TEXT-PARITY"
        rationale = (
            f"The emit-TEXT pipeline RUNS end-to-end (emit -> .clm L3 decode via the "
            f"byte-exact mirror of {os.path.basename(clm_path)} -> {N_STREAMS}×{N_NEW} "
            f"REAL sampled tokens/arm) and the two entropy modes are INDISTINGUISHABLE at "
            f"the token layer. token-frequency chi² p={chi2_p:.3g} (>=0.05, dof {dof}); "
            f"per-stream sequence-entropy KS D={ks_D:.3f} p={ks_p:.3g} (>=0.05), Cohen "
            f"d={ent_cd:+.3f} (|d|<{NEG}). H_930/H_936's quantum-ontological-not-functional "
            f"result EXTENDS to the real text layer — the entropy SOURCE does not change "
            f"WHAT she emits, only its provenance. (#123-A: ANU == chacha20 statistically.)")
    else:
        token = "🔴"
        fal_id = "F-H941-TEXT-FUNCTIONAL"
        rationale = (
            f"The generated token streams DIFFER across entropy modes — entropy is "
            f"functional at the text layer. token chi² p={chi2_p:.3g}; seq-entropy KS "
            f"p={ks_p:.3g} Cohen d={ent_cd:+.3f}. This would CONTRADICT H_930/H_936's "
            f"substrate-side parity and is a finding worth its own arc.")

    result = {
        "h_id": "H_941", "title": "wired emit-TEXT quantum-vs-deterministic A/B",
        "timestamp_utc": ts, "blocked": False,
        "clm_artifact": os.path.basename(clm_path), "clm_path": clm_path,
        "clm_config": {"d": W["d"], "E": W["E"], "V": V, "L": W["L"], "K": W["K"]},
        "wiring": ("emit -> seed/context -> .clm decode (generator L3 SEMANTICS via "
                   "byte-exact Mac mirror clm_decode_mirror.py) -> autoregressive token "
                   "stream. NATIVE hexa engine-mount (clm_decode.hexa->forge) is BLOCKED "
                   "by the macOS link-gap (clm-decode-macos-link-gap) — mirror is the "
                   "sanctioned workaround; a_core_engine_map honored (single L3 entry, no "
                   "phantom native wiring claimed)."),
        "n_streams_per_arm": N_STREAMS, "n_new_tokens": N_NEW, "temperature": TEMP,
        "window_T": T, "prompt_bytes": prompt,
        "quantum_buffer": buf_source,
        "population_fix": ("per-stream independent slice (burn s*64 B) so the quantum "
                           "arm is a genuine 24-stream population, not 24 copies of one "
                           "committed-buffer pattern (the H_930/H_936 single-pattern bug)."),
        "arm_DET": {"mode_seen": armDET["mode_seen"],
                    "provenance_first": armDET["provenance_first"],
                    "sample_text": sample_det},
        "arm_Q": {"mode_seen": armQ["mode_seen"],
                  "provenance_first": armQ["provenance_first"],
                  "sample_text": sample_q},
        "token_freq_chi2": {"chi2": float(chi2), "p": float(chi2_p), "dof": int(dof)},
        "seq_entropy": {"det_mean": float(ent_d_arr.mean()), "det_sd": float(ent_d_arr.std()),
                        "q_mean": float(ent_q_arr.mean()), "q_sd": float(ent_q_arr.std()),
                        "ks_D": float(ks_D), "ks_p": float(ks_p), "cohen_d": float(ent_cd)},
        "distinguishing": {"token": token_distinguishing, "entropy": entropy_distinguishing},
        "deterministic": False, "g5_code_measured": True, "llm": "none",
        "substrate": "Lane-P .clm decode (CPU-mirror)",
        "verdict_token": token, "falsifier_id": fal_id, "verdict_rationale": rationale,
    }

    L = ["H_941 — WIRED EMIT-TEXT RUNG (quantum-vs-deterministic A/B at the TOKEN layer)",
         "=" * 78, f"timestamp_utc : {ts}",
         f".clm artifact : {os.path.basename(clm_path)}  "
         f"(d={W['d']} E={W['E']} V={V} L={W['L']} K={W['K']})",
         f"population    : {N_STREAMS} streams/arm × {N_NEW} sampled tokens  ·  temp {TEMP}",
         "wiring        : emit -> .clm L3 decode (byte-exact Mac mirror) -> AR token stream",
         "                NATIVE forge link BLOCKED (clm-decode-macos-link-gap) — mirror workaround",
         f"qbuf          : {buf_source.get('source')} tier={buf_source.get('tier')} "
         f"n={buf_source.get('n_bytes')} (per-stream independent slice — H_936 population fix)",
         "",
         "── real sampled text (first 48 bytes, NOT fabricated) ──────────────────────",
         f"  DET arm[0]: {sample_det!r}",
         f"  Q   arm[0]: {sample_q!r}",
         "",
         "── token-frequency chi² (pooled streams, both arms) ────────────────────────",
         f"  chi2={chi2:.4f}  dof={dof}  p={chi2_p:.4g}  -> distinguishing={token_distinguishing}",
         "",
         "── per-stream sequence entropy (bits) ──────────────────────────────────────",
         f"  DET mean={ent_d_arr.mean():.4f} sd={ent_d_arr.std():.4f}  |  "
         f"Q mean={ent_q_arr.mean():.4f} sd={ent_q_arr.std():.4f}",
         f"  KS D={ks_D:.4f} p={ks_p:.4g}  Cohen d={ent_cd:+.4f}  -> "
         f"distinguishing={entropy_distinguishing}",
         "",
         "── VERDICT (pre-registered falsifier, CODE-decided — p7) ───────────────────",
         f"  {token}  {fal_id}", f"  {rationale}",
         "",
         "── full machine record (JSON) ──────────────────────────────────────────────",
         json.dumps(result, indent=2, default=str)]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L)); print("\n[written]", out_path)
    return result


if __name__ == "__main__":
    main()
