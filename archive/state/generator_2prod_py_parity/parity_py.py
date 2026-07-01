#!/usr/bin/env python3
# py side of the generator dispatch parity harness — same KIND/CHAT/IDEATE lines
# as state/generator_2prod_py_parity/parity_harness.hexa, driven through
# core/generator.py gen_mouth_kind / gen_auto_chat / gen_auto_ideate.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import generator as g

ck = os.environ["GEN_CK"]
seed = os.environ["GEN_SEED"]
gen = int(os.environ["GEN_N"])

out = sys.stdout.buffer


def w(s):
    out.write(s.encode("utf-8", "surrogateescape") + b"\n")


w("KIND:" + g.gen_mouth_kind(ck))
rc = g.gen_auto_chat(ck, seed, gen)
w("CHAT_OK:" + ("true" if rc["ok"] else "false"))
w("CHAT:" + rc["text"])
ri = g.gen_auto_ideate(ck, seed, gen, 8, 0.9, 4242)
w("IDEATE_OK:" + ("true" if ri["ok"] else "false"))
w("IDEATE:" + ri["text"])
