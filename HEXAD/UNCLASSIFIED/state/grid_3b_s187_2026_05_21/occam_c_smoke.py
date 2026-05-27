"""OCCAM-C quick smoke test — load ckpt + decode 5 bytes greedy + 5 bytes beam-3.

Validates the load path and beam search before the 80-gen sweep.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch

from occam_c_decode_sweep import load_model, decode_greedy_or_sample, decode_beam

CKPT = sys.argv[1] if len(sys.argv) > 1 else "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vJ/ckpt_s187_3b_J.pt"

device = "cpu"
torch.set_num_threads(max(1, os.cpu_count() - 2))
print(f"smoke: device={device} threads={torch.get_num_threads()}", flush=True)

t0 = time.time()
model, cfg = load_model(CKPT, device=device)
print(f"smoke: load_wall={time.time()-t0:.1f}s", flush=True)

prompt_ids = list(b"who are you?\n")
print(f"smoke: prompt_ids={prompt_ids}", flush=True)

# greedy 5
t0 = time.time()
out_g = decode_greedy_or_sample(model, prompt_ids, max_new=5, temperature=0.0, top_k=0, seed=1337, device=device)
print(f"smoke: greedy(5)={out_g} bytes={bytes(out_g)!r}  wall={time.time()-t0:.1f}s", flush=True)

# beam 3 × 5
t0 = time.time()
out_b = decode_beam(model, prompt_ids, max_new=5, beam_width=3, device=device)
print(f"smoke: beam3(5)={out_b} bytes={bytes(out_b)!r}  wall={time.time()-t0:.1f}s", flush=True)

print("smoke: PASS", flush=True)
