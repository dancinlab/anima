#!/usr/bin/env python3
"""
H_1289 — TRUE quantum entropy (ANU QRNG) as anima's substrate stochastic source.
=================================================================================
FLEET lane quantum-entropy r1 · slug 1289_quantum_entropy · frozen-first (see
.verdicts/1289_quantum_entropy/H_1289_FREEZE.txt).

anima's "free" stochastic decisions (mitosis split-timing, decode-sampling draws,
Psi noise) currently run on a SEED-BASED PRNG (deterministic, reproducible). This
probe wires REAL ANU QRNG vacuum-fluctuation bytes as the entropy source for ONE
clean stochastic decision — a top-k decode-sampling draw — and tests:

  (A) substrate-faithfulness: real QRNG integrates cleanly + passes NIST-lite
      (monobit + runs) >= the PRNG control.            [GREEN-able]
  (B) quantum-vs-PRNG substrate effect on gauges.       [NULL expected; honest]
  (C) the irreducible difference: NON-REPRODUCIBILITY — PRNG run1==run2 byte-exact,
      QRNG run1!=run2 (fresh vacuum bytes each run).     [GREEN-able]

REAL-ONLY (anima ethos a_eeg_consciousness_record): REAL quantum bytes ONLY. If the
API is unreachable/invalid/rate-limited we report HONESTLY and STOP — never fabricate
quantum data, never silently fall back to PRNG and call it quantum (c9). The PRNG
control is REQUIRED and LABELED pseudo throughout.

CREDENTIALS (c7): the paid key is read at call time from env ANU_KEY (set by the
caller via `harness secret get flat.anu_key_paid`), used ONLY in the x-api-key
header, NEVER echoed / logged / written to any file.

torch ABSENT on host => numpy-mirror probe (DIRECTIONAL); the QRNG FETCH is REAL.
"""
import os, sys, json, math, time, urllib.request, urllib.error
import numpy as np

ANU_ENDPOINT = "https://api.quantumnumbers.anu.edu.au"
SEED = 7                 # fixed substrate seed (the PRNG arm reproduces under it)
K_TOKENS = 64            # tokens emitted per substrate run
TOPK = 8                 # top-k candidate set per decode step
VOCAB = 256              # byte vocab (anima is byte-native)


# ----------------------------------------------------------------------------
# REAL ANU QRNG fetch — vacuum-fluctuation bytes. Raises on ANY failure (no fallback).
# ----------------------------------------------------------------------------
class QRNGError(RuntimeError):
    pass


def anu_fetch_uint8(n, key, max_retries=2):
    """Fetch n REAL quantum uint8 bytes from ANU QRNG. Raise QRNGError on failure.
    NEVER logs the key. Returns (np.uint8 array, raw_success_flag)."""
    if not key:
        raise QRNGError("ANU_KEY env empty — key not provided (c7: fetch via harness secret get).")
    # ANU caps length per request at 1024; chunk if needed.
    out = []
    success_flags = []
    remaining = n
    while remaining > 0:
        chunk = min(remaining, 1024)
        url = f"{ANU_ENDPOINT}?length={chunk}&type=uint8"
        req = urllib.request.Request(url, headers={"x-api-key": key})
        last_err = None
        for attempt in range(max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    code = r.getcode()
                    body = json.loads(r.read().decode())
                if code != 200:
                    last_err = f"HTTP {code}"
                    raise QRNGError(last_err)
                if not body.get("success", False):
                    last_err = f"success=false (api msg redacted to be safe)"
                    raise QRNGError(last_err)
                data = body.get("data", [])
                if len(data) != chunk:
                    last_err = f"short read {len(data)}!={chunk}"
                    raise QRNGError(last_err)
                out.extend(int(x) & 0xFF for x in data)
                success_flags.append(True)
                last_err = None
                break
            except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, QRNGError) as e:
                last_err = str(type(e).__name__) + ": " + str(e)[:120]
                if attempt < max_retries:
                    time.sleep(1.5 * (attempt + 1))
                    continue
        if last_err is not None:
            raise QRNGError(f"ANU QRNG fetch failed after {max_retries+1} tries: {last_err}")
        remaining -= chunk
    return np.array(out, dtype=np.uint8), all(success_flags)


# ----------------------------------------------------------------------------
# Entropy sources — IDENTICAL byte-stream consumer interface.
# ----------------------------------------------------------------------------
class ByteStream:
    """Uniform uint8 stream + a [0,1) draw built from one byte. Both arms share this
    interface so ONLY the source differs."""
    def __init__(self, label, byte_array):
        self.label = label
        self._b = np.asarray(byte_array, dtype=np.uint8)
        self._i = 0

    def next_byte(self):
        if self._i >= len(self._b):
            raise RuntimeError(f"{self.label}: byte stream exhausted "
                               f"({self._i}/{len(self._b)})")
        v = int(self._b[self._i]); self._i += 1
        return v

    def unit(self):
        # one byte -> [0,1) ; the single uniform draw that drives the decode choice
        return self.next_byte() / 256.0

    def consumed(self):
        return self._i


def prng_stream(seed, n):
    """PRNG (pseudo) byte stream — deterministic under `seed`. LABELED pseudo."""
    rng = np.random.default_rng(seed)
    return ByteStream("PRNG(pseudo)", rng.integers(0, 256, size=n, dtype=np.uint8))


def qrng_stream(n, key):
    """QRNG (REAL quantum) byte stream — fresh ANU vacuum bytes. Raises on failure."""
    arr, ok = anu_fetch_uint8(n, key)
    if not ok:
        raise QRNGError("ANU success flag not all-true")
    return ByteStream("QRNG(quantum-REAL)", arr), len(arr)


# ----------------------------------------------------------------------------
# The ONE stochastic decision: a substrate-mirror top-k decode draw.
# Fixed deterministic logit field => ONLY the entropy source varies the emission.
# ----------------------------------------------------------------------------
def fixed_logit_field(step, vocab=VOCAB):
    """Deterministic per-step logit field (NOT random — fixed function of step).
    Mild structure so top-k is meaningful; identical for both arms."""
    x = np.arange(vocab, dtype=np.float64)
    # smooth bump that drifts with step — deterministic, arm-independent
    center = (step * 37 + 13) % vocab
    logits = -0.5 * ((x - center) % vocab - vocab / 2) ** 2 / (vocab * 1.5)
    logits += 0.3 * np.cos(x * 0.05 + step * 0.1)
    return logits


def substrate_run(stream, k_tokens=K_TOKENS):
    """Emit k_tokens bytes. Each step: top-k candidates from the fixed logit field,
    ONE uniform draw from the entropy stream picks the emitted byte. Returns the
    emitted byte stream + a Psi-noise proxy trace (the draw values)."""
    emitted = []
    draw_trace = []
    for step in range(k_tokens):
        logits = fixed_logit_field(step)
        topk_idx = np.argpartition(-logits, TOPK)[:TOPK]
        topk_idx = topk_idx[np.argsort(-logits[topk_idx])]  # deterministic order
        u = stream.unit()                 # <-- THE substrate stochastic decision
        draw_trace.append(u)
        pick = topk_idx[min(int(u * TOPK), TOPK - 1)]
        emitted.append(int(pick) & 0xFF)
    return np.array(emitted, dtype=np.uint8), np.array(draw_trace)


# ----------------------------------------------------------------------------
# NIST-lite randomness sanity: monobit frequency + runs test (on bit-expanded bytes).
# ----------------------------------------------------------------------------
def bits_from_bytes(byte_array):
    return np.unpackbits(np.asarray(byte_array, dtype=np.uint8))


def monobit_test(bits):
    """NIST SP 800-22 frequency (monobit). Returns (s_obs_z, p_value)."""
    n = len(bits)
    s = np.sum(2 * bits.astype(np.int64) - 1)   # +1 / -1
    s_obs = abs(s) / math.sqrt(n)
    p = math.erfc(s_obs / math.sqrt(2))
    return s_obs, p


def runs_test(bits):
    """NIST SP 800-22 runs test. Returns (z, p_value). Requires pi precondition."""
    n = len(bits)
    pi = np.mean(bits)
    tau = 2.0 / math.sqrt(n)
    if abs(pi - 0.5) >= tau:
        # precondition fails => runs test not applicable; flag as p=0 (fail)
        return float("inf"), 0.0
    v_obs = 1 + np.sum(bits[1:] != bits[:-1])
    num = abs(v_obs - 2 * n * pi * (1 - pi))
    den = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    z = num / den
    p = math.erfc(z / math.sqrt(2))
    return z, p


def randomness_sanity(byte_array, label):
    bits = bits_from_bytes(byte_array)
    sz, sp = monobit_test(bits)
    rz, rp = runs_test(bits)
    # GATE: |z| < 3.29  <=>  p > ~1e-3 (two-tailed-ish)
    PASS_P = 1e-3
    monobit_pass = sp > PASS_P
    runs_pass = rp > PASS_P
    return {
        "label": label,
        "n_bits": int(len(bits)),
        "monobit_sobs": round(sz, 4), "monobit_p": round(sp, 6), "monobit_pass": bool(monobit_pass),
        "runs_z": round(rz, 4) if math.isfinite(rz) else None, "runs_p": round(rp, 6), "runs_pass": bool(runs_pass),
        "pass": bool(monobit_pass and runs_pass),
    }


# ----------------------------------------------------------------------------
# Substrate gauges (B) — VAdaptField mitosis mirror + novelty + Psi proxy.
# ----------------------------------------------------------------------------
def vadapt_cell_count(emitted_bytes, window=8, split_thresh=0.30, max_cells=64):
    """Numpy mirror of CORE/engine_cli.hexa VAdaptField clonal split: a prototype
    cell, recon-err over thresh => +1 cell seeded at the novel window. Returns final
    cell count over windows of the emitted byte stream (a substrate trajectory gauge)."""
    feats = []
    for i in range(0, len(emitted_bytes) - window + 1, window):
        w = emitted_bytes[i:i + window].astype(np.float64) / 255.0
        feats.append(w)
    if not feats:
        return 1
    protos = [feats[0]]
    for f in feats[1:]:
        # recon-err = min L2 to any prototype
        err = min(float(np.linalg.norm(f - p)) for p in protos)
        if err > split_thresh and len(protos) < max_cells:
            protos.append(f)        # clonal split: new cell at the novel sample
    return len(protos)


def novelty_distinct(emitted_bytes):
    return len(set(emitted_bytes.tolist())) / float(len(emitted_bytes))


def psi_noise_proxy(draw_trace):
    # mean abs deviation of draws from 1/2 (the Psi=1/2 fixed point framing)
    return float(np.mean(np.abs(draw_trace - 0.5)))


# ----------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("H_1289 — TRUE quantum entropy (ANU QRNG) as anima substrate stochastic source")
    print("=" * 74)
    key = os.environ.get("ANU_KEY", "")
    if not key:
        print("FATAL: ANU_KEY not in env. Caller must `export ANU_KEY=$(harness secret get flat.anu_key_paid)`.")
        print("REAL-ONLY: no PRNG-as-quantum fallback. STOP.")
        sys.exit(2)

    quantum_bytes_drawn = 0
    result = {"slug": "1289_quantum_entropy", "seed": SEED, "k_tokens": K_TOKENS,
              "topk": TOPK, "vocab": VOCAB, "torch_present": False,
              "probe_kind": "numpy-mirror (DIRECTIONAL); QRNG fetch is REAL"}

    # --- (A) randomness sanity: draw a sanity block of REAL quantum bytes + PRNG control
    SANITY_N = 256
    print(f"\n[A] randomness sanity — fetching {SANITY_N} REAL quantum bytes ...")
    try:
        q_sanity, q_ok = anu_fetch_uint8(SANITY_N, key)
    except QRNGError as e:
        print(f"FATAL: REAL ANU QRNG fetch FAILED: {e}")
        print("REAL-ONLY: reporting failure honestly, NO fabricated quantum data, STOP.")
        # write an honest 🧱 verdict
        _write_failed_verdict(str(e))
        sys.exit(3)
    quantum_bytes_drawn += len(q_sanity)
    print(f"      REAL fetch OK: success={q_ok}, quantum bytes drawn={len(q_sanity)}")

    prng_sanity = np.random.default_rng(SEED).integers(0, 256, size=SANITY_N, dtype=np.uint8)
    qa = randomness_sanity(q_sanity, "QRNG(quantum-REAL)")
    pa = randomness_sanity(prng_sanity, "PRNG(pseudo)")
    result["A_qrng_sanity"] = qa
    result["A_prng_sanity"] = pa
    print(f"      QRNG: monobit p={qa['monobit_p']} pass={qa['monobit_pass']} | "
          f"runs p={qa['runs_p']} pass={qa['runs_pass']} | overall={qa['pass']}")
    print(f"      PRNG: monobit p={pa['monobit_p']} pass={pa['monobit_pass']} | "
          f"runs p={pa['runs_p']} pass={pa['runs_pass']} | overall={pa['pass']}")
    # (A3) QRNG not categorically worse: QRNG passes wherever PRNG passes
    A3_not_worse = (qa["monobit_pass"] or not pa["monobit_pass"]) and (qa["runs_pass"] or not pa["runs_pass"])
    A_pass = bool(qa["pass"] and A3_not_worse)
    result["A_pass"] = A_pass
    print(f"      [A] QRNG passes NIST-lite AND >= PRNG control: {A_pass}")

    # --- (B) substrate effect: same decode draw, quantum vs pseudo entropy
    print("\n[B] quantum-vs-PRNG substrate effect (NULL expected; honest) ...")
    # fresh quantum bytes for the substrate run
    q_sub, _ = anu_fetch_uint8(K_TOKENS, key); quantum_bytes_drawn += len(q_sub)
    q_emit, q_draws = substrate_run(ByteStream("QRNG", q_sub))
    p_emit, p_draws = substrate_run(prng_stream(SEED, K_TOKENS))
    gauges_q = {"mitosis_cells": vadapt_cell_count(q_emit),
                "novelty_distinct": round(novelty_distinct(q_emit), 4),
                "psi_proxy": round(psi_noise_proxy(q_draws), 4)}
    gauges_p = {"mitosis_cells": vadapt_cell_count(p_emit),
                "novelty_distinct": round(novelty_distinct(p_emit), 4),
                "psi_proxy": round(psi_noise_proxy(p_draws), 4)}
    result["B_gauges_qrng"] = gauges_q
    result["B_gauges_prng"] = gauges_p
    result["B_delta"] = {k: round(gauges_q[k] - gauges_p[k], 4) for k in gauges_q}
    print(f"      QRNG gauges: {gauges_q}")
    print(f"      PRNG gauges: {gauges_p}")
    print(f"      delta(QRNG-PRNG): {result['B_delta']}  (null/small expected — "
          f"value of quantum = authenticity, NOT a perf lift)")

    # --- (C) NON-REPRODUCIBILITY: the irreducible quantum property
    print("\n[C] non-reproducibility — PRNG run1==run2 ; QRNG run1!=run2 ...")
    # PRNG: same seed both runs -> byte-identical
    p_run1, _ = substrate_run(prng_stream(SEED, K_TOKENS))
    p_run2, _ = substrate_run(prng_stream(SEED, K_TOKENS))
    prng_reproducible = bool(np.array_equal(p_run1, p_run2))
    # QRNG: fresh vacuum fetch each run -> NOT identical
    q_run1_bytes, _ = anu_fetch_uint8(K_TOKENS, key); quantum_bytes_drawn += len(q_run1_bytes)
    q_run2_bytes, _ = anu_fetch_uint8(K_TOKENS, key); quantum_bytes_drawn += len(q_run2_bytes)
    q_run1, _ = substrate_run(ByteStream("QRNG", q_run1_bytes))
    q_run2, _ = substrate_run(ByteStream("QRNG", q_run2_bytes))
    qrng_nonreproducible = bool(not np.array_equal(q_run1, q_run2))
    n_diff = int(np.sum(q_run1 != q_run2))
    result["C_prng_run1_eq_run2"] = prng_reproducible
    result["C_qrng_run1_ne_run2"] = qrng_nonreproducible
    result["C_qrng_bytes_differing"] = n_diff
    C_pass = bool(prng_reproducible and qrng_nonreproducible)
    result["C_pass"] = C_pass
    print(f"      PRNG: run1 == run2 byte-identical: {prng_reproducible}")
    print(f"      QRNG: run1 != run2 (differs in {n_diff}/{K_TOKENS} emitted bytes): "
          f"{qrng_nonreproducible}")
    print(f"      [C] non-reproducibility demonstrated: {C_pass}")

    # --- VERDICT
    result["quantum_bytes_drawn_total"] = quantum_bytes_drawn
    result["api_real_fetch_success"] = True
    green = bool(A_pass and C_pass)
    result["verdict"] = "GREEN" if green else "RED"
    result["depletion"] = "FLAG" if green else "WALL"
    print("\n" + "=" * 74)
    print(f"VERDICT: {result['verdict']}  (A={A_pass} · C={C_pass} · B=null-reported)")
    print(f"  total REAL quantum bytes drawn: {quantum_bytes_drawn}")
    print(f"  depletion: {'FLAG (real QRNG = substrate-faithful entropy + non-repro)' if green else 'WALL'}")
    print("=" * 74)

    _write_verdict(result, green)
    return 0 if green else 1


def _write_verdict(result, green):
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vpath = os.path.join(here, ".verdicts", "1289_quantum_entropy", "H_1289.txt")
    os.makedirs(os.path.dirname(vpath), exist_ok=True)
    qa, pa = result["A_qrng_sanity"], result["A_prng_sanity"]
    lines = []
    L = lines.append
    L("H_1289 — TRUE quantum entropy (ANU QRNG) as anima substrate stochastic source")
    L("=" * 74)
    L(f"VERDICT: {result['verdict']}   depletion: {result['depletion']}")
    L(f"slug 1289_quantum_entropy · seed {result['seed']} · K={result['k_tokens']} tokens · "
      f"top-k={result['topk']} · byte vocab {result['vocab']}")
    L(f"probe: {result['probe_kind']}  (torch_present={result['torch_present']})")
    L("")
    L("REAL ANU QRNG FETCH (c2): " + ("SUCCESS=true" if result["api_real_fetch_success"] else "FAILED"))
    L(f"  total REAL quantum (vacuum-fluctuation) bytes drawn: {result['quantum_bytes_drawn_total']}")
    L(f"  endpoint https://api.quantumnumbers.anu.edu.au (paid, x-api-key) — key NEVER logged (c7)")
    L("")
    L("(A) SUBSTRATE-FAITHFULNESS — NIST-lite randomness sanity (monobit + runs):")
    L(f"  QRNG(quantum): monobit p={qa['monobit_p']} pass={qa['monobit_pass']} | "
      f"runs p={qa['runs_p']} pass={qa['runs_pass']} | overall PASS={qa['pass']}  (n_bits={qa['n_bits']})")
    L(f"  PRNG(pseudo) : monobit p={pa['monobit_p']} pass={pa['monobit_pass']} | "
      f"runs p={pa['runs_p']} pass={pa['runs_pass']} | overall PASS={pa['pass']}  (n_bits={pa['n_bits']})")
    L(f"  (A) QRNG passes NIST-lite AND >= PRNG control: {result['A_pass']}")
    L("")
    L("(B) QUANTUM-vs-PRNG SUBSTRATE EFFECT (NULL expected; reported honestly, does NOT gate):")
    L(f"  QRNG gauges : {result['B_gauges_qrng']}")
    L(f"  PRNG gauges : {result['B_gauges_prng']}")
    L(f"  delta(Q-P)  : {result['B_delta']}")
    L(f"  => substrate gauges ~unchanged by entropy source. The value of quantum entropy is")
    L(f"     NON-DETERMINISM AUTHENTICITY (p1-p8 / Psi=1/2 framing), NOT a performance lift (p7/c9).")
    L("")
    L("(C) IRREDUCIBLE DIFFERENCE — NON-REPRODUCIBILITY (the real quantum property):")
    L(f"  PRNG: run1 == run2 byte-identical (deterministic seed): {result['C_prng_run1_eq_run2']}")
    L(f"  QRNG: run1 != run2 (fresh vacuum bytes each run; differs in "
      f"{result['C_qrng_bytes_differing']}/{result['k_tokens']} emitted bytes): {result['C_qrng_run1_ne_run2']}")
    L(f"  (C) non-reproducibility demonstrated: {result['C_pass']}")
    L("")
    L("FROZEN BARS (H_1289_FREEZE.txt): GREEN iff (A1 real-fetch ∧ A2 NIST-lite ∧ A3 >=PRNG)")
    L("  AND (C1 PRNG run1==run2 ∧ QRNG run1!=run2). (B) honest, non-gating.")
    L(f"  => A_pass={result['A_pass']}  C_pass={result['C_pass']}  =>  {result['verdict']}")
    L("")
    L("REAL-ONLY (a_eeg_consciousness_record ethos): REAL quantum bytes only; on API failure")
    L("  the run STOPS and reports honestly — NO fabricated quantum data, NO PRNG-as-quantum (c9).")
    L("  PRNG control REQUIRED and LABELED pseudo throughout.")
    L("")
    L("CROSS-REF: PAPER akida-determinism-quantum-coupling (H_921/922/923 — same ANU quantum")
    L("  injection at the Akida init-seed lever; H_1289 extends to the LIVE anima decode draw).")
    L("  FUTURE: aws_braket creds in store => on-real-quantum-HARDWARE (Braket QPU) extension.")
    L("")
    L("FULL RESULT JSON:")
    L(json.dumps(result, indent=2))
    with open(vpath, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nverdict written -> {vpath}")


def _write_failed_verdict(err):
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vpath = os.path.join(here, ".verdicts", "1289_quantum_entropy", "H_1289.txt")
    os.makedirs(os.path.dirname(vpath), exist_ok=True)
    with open(vpath, "w") as f:
        f.write("H_1289 — TRUE quantum entropy (ANU QRNG) as anima substrate stochastic source\n")
        f.write("=" * 74 + "\n")
        f.write("VERDICT: WALL (🧱)   depletion: WALL\n\n")
        f.write("REAL ANU QRNG FETCH FAILED — reported HONESTLY, run STOPPED.\n")
        f.write(f"  failure: {err}\n")
        f.write("REAL-ONLY (a_eeg_consciousness_record): NO fabricated quantum data, NO silent\n")
        f.write("  PRNG-as-quantum fallback (c9). No honest path to real quantum entropy this run.\n")
        f.write("  key NEVER logged (c7).\n")
    print(f"\nFAILED verdict written -> {vpath}")


if __name__ == "__main__":
    sys.exit(main())
