#!/usr/bin/env python3
# anima-eeg-core/tool/modules/_prng/_pcg32_reference.py
#
# PURPOSE
#   Pure-Python reference implementation of SplitMix64 + PCG32 (XSH-RR)
#   that mirrors EXACTLY the int63-modular semantics of the hexa-native
#   port (splitmix64_native.hexa / pcg32_native.hexa).
#
#   This is NOT the canonical Vigna / O'Neill C implementation. It is the
#   "hexa-internal reference" — its output is what the hexa-native modules
#   must byte-match. NumPy is intentionally NOT used (raw#9-compatible:
#   pure stdlib Python; can run on any host without venv).
#
# USAGE
#   python3 _pcg32_reference.py splitmix64-seed0
#   python3 _pcg32_reference.py pcg32-seed42-seq54
#   python3 _pcg32_reference.py pcg32-uniform-mean 100000
#
# raw#10 honest: contracts identical to the hexa modules — int63 modular
# arithmetic, no uint64 wraparound. Output values are ground truth for
# F_SPLITMIX64_01 and F_PCG32_01 frozen reference vectors.

import sys

MASK63 = (1 << 63) - 1     # 9223372036854775807
MASK32 = (1 << 32) - 1     # 4294967295

# SplitMix64 constants (truncated to int63 to match hexa).
SM64_GOLDEN_GAMMA  = 0x9E3779B97F4A7C15 & MASK63   # = 2177342782468422869
SM64_MIX1_CONSTANT = 0xBF58476D1CE4E5B9 & MASK63   # = 4564476756301767736
SM64_MIX2_CONSTANT = 0x94D049BB133111EB & MASK63   # = 1505689411779249643

# PCG32 LCG multiplier (fits in int63).
PCG32_MULT = 6364136223846793005


def splitmix64_next(state: int) -> tuple[int, int]:
    """Advance SplitMix64; return (new_state, output). Matches hexa int63 port."""
    new_state = (state + SM64_GOLDEN_GAMMA) & MASK63
    z = new_state
    z = (z ^ (z >> 30)) & MASK63
    z = (z * SM64_MIX1_CONSTANT) & MASK63
    z = (z ^ (z >> 27)) & MASK63
    z = (z * SM64_MIX2_CONSTANT) & MASK63
    output = (z ^ (z >> 31)) & MASK63
    return new_state, output


def splitmix64_seed(seed: int) -> int:
    s = seed
    if s < 0:
        s = -s
    return s & MASK63


def pcg32_seed(seed: int, seq: int) -> tuple[int, int]:
    """Initialise PCG32 state. Returns (state, inc). Mirrors hexa port."""
    s = seed
    if s < 0:
        s = -s
    s &= MASK63
    q = seq
    if q < 0:
        q = -q
    q &= MASK63

    _, mixed_seq = splitmix64_next(q)
    inc = ((mixed_seq * 2) + 1) & MASK63

    state = 0
    state = (((state * PCG32_MULT) & MASK63) + inc) & MASK63
    state = (state + s) & MASK63
    state = (((state * PCG32_MULT) & MASK63) + inc) & MASK63
    return state, inc


def pcg32_next(state: int, inc: int) -> tuple[int, int, int]:
    """Advance PCG32; return (new_state, inc, output_uint32). Mirrors hexa port."""
    oldstate = state
    new_state = (((oldstate * PCG32_MULT) & MASK63) + inc) & MASK63

    xs_pre = ((oldstate >> 18) ^ oldstate) & MASK63
    xorshifted = (xs_pre >> 27) & MASK32

    rot = (oldstate >> 59) & 31

    right_part = xorshifted >> rot
    if rot == 0:
        left_part = 0
    else:
        left_part = (xorshifted << (32 - rot)) & MASK32
    output = (right_part | left_part) & MASK32
    return new_state, inc, output


def pcg32_uniform_x1e6(state: int, inc: int) -> tuple[int, int, int]:
    new_state, inc, u32 = pcg32_next(state, inc)
    value = (u32 * 1000000) // 4294967296
    return new_state, inc, value


def cmd_splitmix64_seed0() -> None:
    """Print first 4 outputs from splitmix64 with seed=0."""
    s = splitmix64_seed(0)
    for k in range(4):
        s, out = splitmix64_next(s)
        print(f"out[{k}] = {out}")


def cmd_pcg32_seed42_seq54() -> None:
    """Print first 6 outputs from pcg32 with seed=42, seq=54."""
    state, inc = pcg32_seed(42, 54)
    for k in range(6):
        state, inc, out = pcg32_next(state, inc)
        print(f"out[{k}] = {out}")


def cmd_pcg32_uniform_mean(n: int) -> None:
    """Sample n uniform_x1e6 values, print mean (target 500000)."""
    state, inc = pcg32_seed(123, 456)
    total = 0
    for _ in range(n):
        state, inc, v = pcg32_uniform_x1e6(state, inc)
        total += v
    print(f"mean_x1 = {total // n}  n_samples = {n}")


def main() -> int:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: _pcg32_reference.py {splitmix64-seed0|pcg32-seed42-seq54|pcg32-uniform-mean N}\n")
        return 2
    cmd = sys.argv[1]
    if cmd == "splitmix64-seed0":
        cmd_splitmix64_seed0()
        return 0
    if cmd == "pcg32-seed42-seq54":
        cmd_pcg32_seed42_seq54()
        return 0
    if cmd == "pcg32-uniform-mean":
        if len(sys.argv) < 3:
            sys.stderr.write("usage: _pcg32_reference.py pcg32-uniform-mean N\n")
            return 2
        cmd_pcg32_uniform_mean(int(sys.argv[2]))
        return 0
    sys.stderr.write(f"unknown command: {cmd}\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
