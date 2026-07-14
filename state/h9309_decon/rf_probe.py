"""H_9309 DECON — PRE-MORTEM: is the injected prefix even REACHABLE from the answer position?

The trunk is a 4-layer conv (no positional table — T is a free forward-pass parameter).  A conv
has a finite receptive field: RF = L*(K-1)+1.  If the answer position cannot SEE byte 0 of the
window, then a context-prefix injection is unreachable *at any window size* and DECON's only
structurally-valid channel is dead before it fires — the same class of fact as the T=24 hardcode
in clm_decode_topk_sampled_W that would have killed the free-generation D-acc instrument.

Do not compute RF from the kernel shape and trust it (SLW/CLML trailers can add paths).  MEASURE
it: perturb byte i of the input, see whether the final-position logits move.  Causal, not assumed.

Reachable set = { i : max|Δ logits(final)| > 0 when byte i is changed }.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as clm

CKPT = os.path.expanduser("~/anima-weights/c34/natem_c34_main_s7.clm")
SEED = "이 영화 빠르지 않다 => "        # a real flip1 held-out trial (41B-class)
T = 64


def win(text, T):
    b = text.encode()[-T:]
    return list((b"\x00" * (T - len(b))) + b)


def fwd(clm_mod, W, tok):
    """Final-position logits. Same tap the margin scorer uses (clm_forward_hidden_logits)."""
    _, lg = clm_mod.clm_forward_hidden_logits(W, np.array(tok, dtype=np.float64), len(tok))
    return np.asarray(lg)


def main():
    W = clm.clm_load_weights(CKPT)
    assert W["ok"]
    print("ckpt d=%d L=%d bind=%s slw=%s clml=%s"
          % (W["d"], W["L"], W.get("bind_type"), bool(W.get("slw")), bool(W.get("clml"))))

    base_w = win(SEED, T)
    base = fwd(clm, W, base_w)[-1]
    pad = T - len(SEED.encode())
    print("window T=%dB · seed=%dB · %dB of left pad (a prefix would live here)"
          % (T, len(SEED.encode()), pad))

    reach = []
    for i in range(T):
        b = list(base_w)
        b[i] = (b[i] + 7) % 256                       # perturb byte i
        lg = fwd(clm, W, b)[-1]
        reach.append(float(np.max(np.abs(lg - base))))

    nz = [i for i, d in enumerate(reach) if d > 1e-9]
    print("\nreachable byte positions (|Δ logits| > 0 at the answer slot):")
    print("  n reachable = %d / %d" % (len(nz), T))
    if nz:
        print("  leftmost reachable index = %d  (answer slot is index %d)" % (min(nz), T - 1))
        print("  => effective receptive field = %d bytes" % (T - min(nz)))
    print("\n  per-position |Δ| (nonzero only):")
    for i in nz:
        mark = "  <-- PREFIX ZONE" if i < pad else ""
        print("    %2d: %.4e%s" % (i, reach[i], mark))

    pre = [i for i in nz if i < pad]
    print("\n" + "=" * 74)
    if pre:
        print("REACHABLE — %d of the %d prefix-zone bytes causally move the answer logits."
              % (len(pre), pad))
        print("A context-injected fact CAN be seen at the answer slot. DECON's channel is live.")
    else:
        print("UNREACHABLE — NOT ONE prefix-zone byte moves the answer logits.")
        print("The conv receptive field ends before the prefix. A context-injected fact is")
        print("physically invisible at the answer slot AT ANY WINDOW SIZE. The context channel")
        print("is structurally dead => DO NOT FIRE. (Fable ruled logit-bias and penultimate-")
        print("addition structurally dead already, so this closes the A-channel injection point")
        print("entirely: the lever must be RE-DESIGNED, not re-tuned.)")
    print("=" * 74)


if __name__ == "__main__":
    main()
