#!/usr/bin/env python3
"""py-engine decode readout for the bind codec parity oracle: prints the SAME
fields the hexa harness prints, via core/clm_decode.py (the py production engine).
Usage: decode_py.py <clm> <corpus> <nwin> <seed> <gen>"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "core", "clm_decode.py")):
    _REPO = os.path.dirname(_REPO)
sys.path.insert(0, os.path.join(_REPO, "core"))
import clm_decode as D


def main():
    clm, corpus, nwin, seed, gen = (sys.argv[1], sys.argv[2], int(sys.argv[3]),
                                    sys.argv[4], int(sys.argv[5]))
    W = D.clm_load_weights(clm)
    ce = D.clm_forward_ce(clm, corpus, nwin)
    am = D.clm_decode_argmax(clm, seed, gen)
    print(f"RTYPE={W.get('rtype', 0)} KBIND={W.get('kbind')}")
    print("CE model_ce=%.6f shuffle_ce=%.6f uniform_ce=%.6f windows=%d"
          % (ce["model_ce"], ce["shuffle_ce"], ce["uniform_ce"], ce["windows"]))
    sys.stdout.buffer.write(b"ARGMAX:" + am["text"].encode("utf-8", "surrogateescape") + b"\n")


if __name__ == "__main__":
    main()
