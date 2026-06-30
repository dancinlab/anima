#!/usr/bin/env python3
# py 2-production engine cross-check (a_engine_native_learning): byte-parity twin of
# core/g_gates.hexa::g_eval_g6_multiseed. Codegen-INDEPENDENT path (numpy decode in
# core/bytegpt_decode.py) -> isolates whether .hexa and .py agree on the G6 verdict.
import sys, os, json
sys.path.insert(0, os.path.expanduser("~/anima/core"))
import g_gates as G

CKPT = "/home/summer/anima-weights/bytegpt303_h1129/h1129.bin"
GEN = 80

# lean G6-only entry (lockstep twin of g_gates.hexa::g_g6_multiseed_only): loads known+mouth
# internally, runs ONLY g_eval_g6_multiseed over {7,4302,4303}. per_seed[0] (base_seed=7) == the
# frozen single-seed G6 default frame-for-frame.
ms = G.g_g6_multiseed_only(CKPT, GEN)

print("=== h1129 G6 PY 2-PRODUCTION (core/g_gates.py, gen=%d) ===" % GEN)
print("ckpt=" + CKPT)
print("--- multi-seed {7,4302,4303} ---")
for p in ms["per_seed"]:
    print("seed=%s  dist=%s  fals=%s  coherent=%s  pass=%s" % (p["base_seed"], p["dist"], p["fals"], p["coherent"], p["pass"]))
print("MAJORITY: pass=%s  n_green=%s/%s  max_fals=%s" % (ms["pass"], ms["n_green"], ms["n_seeds"], ms["max_fals"]))
print("JSON " + json.dumps({"multiseed": ms}))
