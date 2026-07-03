#!/usr/bin/env python3
"""window_identity_proof.py — CHEAP byte-math proof (no decode, no GPU) that the
canonical G1 gate at T=24 conditions the COMPOSED arm and the matching SINGLE arm
on a BYTE-IDENTICAL window ⟹ composed>max_single is structurally near-impossible.

Reproduces the exact right-align used by core/decode.py clm_decode_topk_sampled_W:
    for p in range(T): si = slen - T + p; tok[p] = seed_b[si] if si>=0 else 32(pad)
i.e. the model sees ONLY the last T bytes of the seed (pad-left with byte 32).

CONCEPTS/seed construction VERBATIM from cli/evaluate.py g_eval_g1 + gauge_lib.CONCEPTS.
"""
CONCEPTS = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]


def right_align_window(seed: str, T: int) -> bytes:
    b = seed.encode("utf-8", "surrogateescape")
    slen = len(b)
    out = bytearray()
    for p in range(T):
        si = slen - T + p
        out.append(b[si] if si >= 0 else 32)
    return bytes(out)


def single_seed(s: int) -> str:                 # g_eval_g1: cz[s] + ". "
    return CONCEPTS[s] + ". "


def composed_seed(k: int) -> str:               # g_eval_g1: join cz[0..k-1] by ". " + ". "
    seed = ""
    for c in range(k):
        if c > 0:
            seed += ". "
        seed += CONCEPTS[c]
    seed += ". "
    return seed


for T in (24, 48, 96):
    print(f"\n===================== T = {T} =====================")
    for k in range(2, 6):
        cw = right_align_window(composed_seed(k), T)
        # the SINGLE arm that shares the same TAIL concept = set (k-1)
        sw = right_align_window(single_seed(k - 1), T)
        same = cw == sw
        clen = len(composed_seed(k).encode())
        print(f" k={k} (composed seed {clen}B):")
        print(f"   composed T={T} window = {cw.decode('utf-8','replace')!r}")
        print(f"   single[{k-1}] T={T} window = {sw.decode('utf-8','replace')!r}")
        print(f"   BYTE-IDENTICAL conditioning? {same}"
              + ("   <-- composed arm sees the SAME context as a single arm"
                 if same else "   (window now differs -> earlier concept re-enters)"))
