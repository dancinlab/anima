#!/usr/bin/env python3
# M② — h1129 G6 multiseed (py 2-production engine, a_engine_native_learning TERMINAL).
# Drives core/g_gates.py::g_eval_g6_multiseed via _Mouth(h1129.bin) -> core/bytegpt_decode.py
# (torch-free numpy). seeds {7,4302,4303}, gen=120 (frozen G6 default). Resolves H_1595
# genuine-vs-artifact: is h1129's fals=0 a seed-robust wall or single-seed sampler walk?
import sys, os, json, time, resource
sys.path.insert(0, os.path.abspath("core"))
import g_gates as G

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
GEN = int(sys.argv[1]) if len(sys.argv) > 1 else 120

print("="*78, flush=True)
print("h1129 G6 MULTISEED — py 2-production (core/g_gates.py <- core/bytegpt_decode.py)", flush=True)
print(f"ckpt={CKPT}  gen={GEN}  seeds={G.G6_REFMATCH_SEEDS}  host={os.uname().nodename}", flush=True)
print(f"date {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
print("="*78, flush=True)

t0 = time.time()
known = G._g6_dict_load()
mouth = G._Mouth(CKPT)
print(f"[loaded known+mouth {time.time()-t0:.1f}s]", flush=True)

t0 = time.time()
ms = G.g_eval_g6_multiseed(mouth, GEN, known)
print(f"[g6_multiseed done {time.time()-t0:.1f}s]", flush=True)

print("--- per-seed ---", flush=True)
for p in ms["per_seed"]:
    print(f"seed={p['base_seed']}  dist={p['dist']}  fals={p['fals']}  "
          f"coherent={p['coherent']}  pass={p['pass']}  frame_leaks={p['frame_leaks']}", flush=True)
print(f"MAJORITY: pass={ms['pass']}  n_green={ms['n_green']}/{ms['n_seeds']}  "
      f"max_fals={ms['max_fals']}", flush=True)
out = "state/1595_h1129_g6_multiseed/result_h1129_g6_multiseed.json"
with open(out, "w") as f: json.dump({"ckpt": CKPT, "gen": GEN, "multiseed": ms}, f, indent=2)
print("wrote " + out, flush=True)
print("G6_MULTISEED_DONE", flush=True)
