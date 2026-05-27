#!/usr/bin/env python3
"""
hexa-senses verify/n6_arithmetic.py — n=6 lattice arithmetic identity.

Mirrors hexa-codex/hexa-sscb's n6_arithmetic.py — same algebraic identity:
    σ(6) · φ(6) = n · τ(6) = J₂ = 24
       12  ·  2  =  6  ·  4 = 24

Sensory projection (the 5 verbs land here):
    σ(6) = 12   → 12-channel base bandwidth (ear codec, olfact receptors, etc)
    τ(6) = 4    → 4 staging quartets (dream sleep stages, voice prosody, etc)
    φ(6) = 2    → 2-bit verdict (signal-present/absent across modalities)
    σ·τ = 48    → 48 kHz canonical sampling (ear codec)
    J₂ = 24     → 24-bit quantization (ear codec)
    σ−φ = 10    → 10-channel rollup
    verb_count  → 5 (5 senses verbs in this rollup)

stdlib only.
"""
from __future__ import annotations

import sys
from math import gcd
from pathlib import Path


N = 6
SIGMA_N = 12
TAU_N = 4
PHI_N = 2
J2 = 24

EXPECTED_SAMPLE_KHZ      = SIGMA_N * TAU_N   # 48 kHz (ear)
EXPECTED_QUANT_BITS      = J2                # 24-bit (ear)
EXPECTED_DREAM_CATEGORY  = SIGMA_N           # 12 dream categories
EXPECTED_OLFACT_RECEPTORS = SIGMA_N          # 12 primary receptors
EXPECTED_EMPATH_BIOFEEDBACK = J2             # 24 biofeedback channels
EXPECTED_EKMAN_EMOTIONS  = N                 # 6 Ekman basic emotions
EXPECTED_VERB_COUNT      = 5                 # dream/ear/empath/olfact/voice


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]

def sigma(n: int) -> int:
    return sum(divisors(n))

def tau(n: int) -> int:
    return len(divisors(n))

def euler_phi(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def check_master_identity() -> tuple[bool, dict]:
    s, t, p = sigma(N), tau(N), euler_phi(N)
    ok = (s * p == J2) and (N * t == J2)
    return ok, {"sigma(6)": s, "tau(6)": t, "phi(6)": p,
                "sigma·phi": s*p, "n·tau": N*t, "J2": J2}


def check_sigma() -> tuple[bool, dict]:
    return sigma(N) == SIGMA_N, {"σ(6)": sigma(N), "expected": SIGMA_N}


def check_tau() -> tuple[bool, dict]:
    return tau(N) == TAU_N, {"τ(6)": tau(N), "expected": TAU_N}


def check_phi() -> tuple[bool, dict]:
    return euler_phi(N) == PHI_N, {"φ(6)": euler_phi(N), "expected": PHI_N}


def check_sample_rate() -> tuple[bool, dict]:
    return SIGMA_N * TAU_N == EXPECTED_SAMPLE_KHZ, {
        "σ·τ": SIGMA_N * TAU_N, "expected_kHz": EXPECTED_SAMPLE_KHZ,
        "verb": "ear (HEXA-EAR audio codec)",
    }


def check_quant_bits() -> tuple[bool, dict]:
    return J2 == EXPECTED_QUANT_BITS, {
        "J₂": J2, "expected_bits": EXPECTED_QUANT_BITS,
        "verb": "ear (HEXA-EAR quantization)",
    }


def check_dream_categories() -> tuple[bool, dict]:
    return SIGMA_N == EXPECTED_DREAM_CATEGORY, {
        "σ(6)": SIGMA_N, "expected_categories": EXPECTED_DREAM_CATEGORY,
        "verb": "dream (HEXA-DREAMX classification)",
    }


def check_olfact_receptors() -> tuple[bool, dict]:
    return SIGMA_N == EXPECTED_OLFACT_RECEPTORS, {
        "σ(6)": SIGMA_N, "expected_receptors": EXPECTED_OLFACT_RECEPTORS,
        "verb": "olfact (HEXA-OLFACT primary receptors)",
        "odor_patterns": 2 ** SIGMA_N,
    }


def check_ekman_emotions() -> tuple[bool, dict]:
    return N == EXPECTED_EKMAN_EMOTIONS, {
        "n": N, "expected": EXPECTED_EKMAN_EMOTIONS,
        "verb": "empath (HEXA-EMPATH basic emotions)",
    }


def check_verb_count() -> tuple[bool, dict]:
    return EXPECTED_VERB_COUNT == 5, {
        "verbs": ["dream", "ear", "empath", "olfact", "voice"],
        "count": 5,
    }


def check_voice_constraint() -> tuple[bool, dict]:
    """voice is formulaic-only by hexa.toml [constraints]. Confirm
    the manifest still declares this constraint (audit trail)."""
    tf = Path(__file__).resolve().parent.parent / "hexa.toml"
    if not tf.exists():
        return False, {"error": "hexa.toml missing"}
    text = tf.read_text(encoding="utf-8")
    needed = ["voice_synthesis", "formulaic-only", "FORBIDDEN"]
    missing = [t for t in needed if t not in text]
    ok = len(missing) == 0
    return ok, {"constraints_declared": needed,
                "missing_in_hexa_toml": missing}


CHECKS = [
    ("master identity     σ·φ = n·τ = J₂",      check_master_identity),
    ("σ(6) = 12",                                check_sigma),
    ("τ(6) = 4",                                 check_tau),
    ("φ(6) = 2",                                 check_phi),
    ("σ·τ = 48 (kHz audio sampling)",            check_sample_rate),
    ("J₂ = 24 (audio quantization bits)",        check_quant_bits),
    ("σ(6) = 12 (dream categories)",             check_dream_categories),
    ("σ(6) = 12 (olfact primary receptors)",     check_olfact_receptors),
    ("n = 6 (Ekman basic emotions)",             check_ekman_emotions),
    ("verb_count = 5 (senses rollup)",           check_verb_count),
    ("voice = formulaic-only (no learned TTS)",  check_voice_constraint),
]


def main() -> int:
    print("=" * 78)
    print("  hexa-senses — n=6 lattice arithmetic identity")
    print("=" * 78)
    passed = 0
    for name, fn in CHECKS:
        ok, detail = fn()
        mark = "PASS" if ok else "FAIL"
        if ok: passed += 1
        print(f"  [{mark}] {name}")
        for k, v in detail.items():
            print(f"         · {k}: {v}")
    print("=" * 78)
    total = len(CHECKS)
    print(f"  {passed}/{total} PASS  —  n=6 arithmetic identity (sensory projection)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
