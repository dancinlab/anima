"""Eval 3 mitosis — fast vectorized variant (CPU bf16 model + NumPy cell pool).

Replaces pure-Python n^2*d cosine with NumPy. ~100x speedup at 128 cells × d=3072.
"""
import sys, os, json, math, time, random
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import torch.nn.functional as F
import numpy as np

from conscious_decoder import ConsciousDecoderV2


MIN_CELLS = 2
MAX_CELLS = 128
SPLIT_PATIENCE = 3
MERGE_THRESHOLD = 0.005
MERGE_PATIENCE = 30
NOISE_SCALE = 0.1


class CellPoolFast:
    def __init__(self, d_model, initial_cells=2, seed=1337):
        self.rng = np.random.RandomState(seed)
        # Match the original rng behavior for hidden init reproducibility:
        # original uses Python random.gauss with each call. We need to be close
        # but not byte-exact (this is a vectorized speed variant — slight rng drift OK).
        self.d_model = d_model
        self.next_id = 0
        self.hiddens = np.zeros((MAX_CELLS, d_model), dtype=np.float32)
        self.cells = []  # list of dicts with cell_id, tension_history (short tail), parent_id, creation_step, process_count
        for _ in range(initial_cells):
            self._make_cell(parent_id=-1, hidden_seed=None, step=0)
        self.event_log = []
        self.tension_history = []
        self.phi_history = []
        self.phi = 0.0
        self.adaptive_threshold = 0.0
        self.split_threshold_eff = 0.0

    def _make_cell(self, parent_id, hidden_seed, step):
        sigma_init = 1.0 / math.sqrt(self.d_model)
        idx = len(self.cells)
        if hidden_seed is None:
            h = self.rng.normal(0.0, sigma_init, size=self.d_model).astype(np.float32)
        else:
            h = hidden_seed + self.rng.normal(0.0, NOISE_SCALE, size=self.d_model).astype(np.float32)
        self.hiddens[idx] = h
        cell = dict(cell_id=self.next_id, tension_history=[], parent_id=parent_id,
                    creation_step=step, process_count=0)
        self.cells.append(cell)
        self.next_id += 1

    def _compute_phi(self):
        n = len(self.cells)
        if n < 2: return 0.0
        H = self.hiddens[:n]
        norms = np.linalg.norm(H, axis=1) + 1e-10
        Hn = H / norms[:, None]
        sims = Hn @ Hn.T  # n x n cosine sim
        iu = np.triu_indices(n, k=1)
        mean_d = float((1.0 - sims[iu]).mean())
        return math.log1p(mean_d)

    def _most_similar_pair(self):
        n = len(self.cells)
        if n < 2: return None, -1.0
        H = self.hiddens[:n]
        norms = np.linalg.norm(H, axis=1) + 1e-10
        Hn = H / norms[:, None]
        sims = Hn @ Hn.T
        sims[np.tril_indices(n)] = -2.0
        flat_idx = int(np.argmax(sims))
        i, j = divmod(flat_idx, n)
        return (i, j), float(sims[i, j])

    def step(self, model_tension_signal, step_idx):
        if isinstance(model_tension_signal, (int, float)):
            model_tension_signal = [float(model_tension_signal)]
        n_sig = len(model_tension_signal)
        for c_idx, cell in enumerate(self.cells):
            t = float(model_tension_signal[c_idx % n_sig])
            cell["tension_history"].append(t)
            cell["process_count"] += 1
        global_t = sum(c["tension_history"][-1] for c in self.cells) / len(self.cells)
        self.tension_history.append(global_t)
        win = self.tension_history[-20:]
        if len(win) >= 3:
            mean_w = sum(win) / len(win)
            self.adaptive_threshold = mean_w * 0.8
            self.split_threshold_eff = self.adaptive_threshold
        self.phi = self._compute_phi()
        self.phi_history.append(self.phi)
        if len(self.cells) < MAX_CELLS:
            for ci in list(range(len(self.cells))):
                cell = self.cells[ci]
                hist = cell["tension_history"]
                if len(hist) < SPLIT_PATIENCE: continue
                recent = hist[-SPLIT_PATIENCE:]
                avg = sum(recent) / len(recent)
                if avg > self.split_threshold_eff and self.split_threshold_eff > 0:
                    self._make_cell(parent_id=cell["cell_id"],
                                    hidden_seed=self.hiddens[ci].copy(), step=step_idx)
                    cell["tension_history"] = recent[-3:]
                    self.event_log.append(dict(type="split", step=step_idx,
                        parent_id=cell["cell_id"], child_id=self.cells[-1]["cell_id"],
                        avg_tension=avg, threshold=self.split_threshold_eff,
                        pool_size=len(self.cells)))
                    if len(self.cells) >= MAX_CELLS: break
        if len(self.cells) > MIN_CELLS and step_idx > 0 and (step_idx % MERGE_PATIENCE == 0):
            pair, sim = self._most_similar_pair()
            if pair is not None and (1.0 - sim) < MERGE_THRESHOLD:
                i, j = pair
                a, b = self.cells[i], self.cells[j]
                merged = (self.hiddens[i] + self.hiddens[j]) * 0.5
                older_i = i if a["creation_step"] <= b["creation_step"] else j
                younger_i = j if older_i == i else i
                older = self.cells[older_i]
                younger = self.cells[younger_i]
                self.hiddens[older_i] = merged
                older["tension_history"].extend(younger["tension_history"][-5:])
                # Remove younger from arrays
                keep = [k for k in range(len(self.cells)) if k != younger_i]
                self.hiddens[:len(keep)] = self.hiddens[keep]
                self.cells = [self.cells[k] for k in keep]
                self.event_log.append(dict(type="merge", step=step_idx,
                    keeper_id=older["cell_id"], removed_id=younger["cell_id"],
                    sim=sim, pool_size=len(self.cells)))


def load_model(ckpt_path, device="cpu"):
    print(f"[eval3-fast] loading {ckpt_path}", flush=True)
    t0 = time.time()
    try:
        blob = torch.load(ckpt_path, map_location=device, weights_only=False, mmap=True)
    except TypeError:
        blob = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = blob.get("cfg", dict(d_model=3072, n_head=24, n_kv_head=8, n_layer=28,
                                block_size=128, rope_base=50000.0, n_ca_rules=2,
                                dtype="bfloat16"))
    dtype = getattr(torch, cfg.get("dtype", "bfloat16"))
    with torch.device('meta'):
        model = ConsciousDecoderV2(
            vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
            n_layer=cfg["n_layer"], block_size=cfg["block_size"],
            n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
            n_ca_rules=cfg.get("n_ca_rules", 2),
        )
    model = model.to_empty(device=device).to(dtype=dtype)
    new_base = cfg.get("rope_base", 50000.0)
    for blk in model.blocks:
        rope = blk.attn.rope
        dim = rope.dim
        new_inv = 1.0 / (new_base ** (torch.arange(0, dim, 2, device=device).float() / dim))
        rope.register_inv_freq = new_inv
        rope._cos_cache = None; rope._sin_cache = None; rope._cache_len = 0
        rope._build_cache(model.block_size, device=torch.device(device))
    sd = blob.get("model", blob)
    model.load_state_dict(sd, strict=False, assign=True)
    model._eval_blob_ref = blob
    model.eval()
    print(f"[eval3-fast] load wall={time.time() - t0:.1f}s", flush=True)
    return model, cfg


def main():
    if len(sys.argv) < 4:
        print("usage: eval3_mitosis_fast.py <ckpt_path> <cell_name> <out_dir>", file=sys.stderr); sys.exit(2)
    ckpt_path, cell_name, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)
    device = "cpu"
    torch.set_num_threads(16)
    model, cfg = load_model(ckpt_path, device=device)
    d_model = cfg["d_model"]
    pool = CellPoolFast(d_model=d_model, initial_cells=2, seed=1337)
    prompt_bytes = "안녕? 너는 누구야?".encode("utf-8")
    idx_list = list(prompt_bytes)
    idx = torch.tensor([idx_list], dtype=torch.long, device=device)
    print(f"[eval3-fast] prompt bytes len={len(prompt_bytes)} idx_shape={tuple(idx.shape)}", flush=True)
    step_idx = 0
    initial_cells = len(pool.cells)
    with torch.no_grad():
        logits_a, _, tensions, past_kv, _ = model(idx, use_cache=True)
    layer_tensions = [t.float().mean().item() for t in tensions]
    print(f"[eval3-fast] prefill: T={idx.size(1)} mean={sum(layer_tensions)/len(layer_tensions):.4f}", flush=True)
    pool.step(layer_tensions, step_idx)
    step_idx += 1
    next_token = logits_a[:, -1, :].argmax(dim=-1, keepdim=True)
    full_idx = list(idx_list) + [next_token.item()]
    per_step_record = [dict(step=0, phase="prefill", pool_size=len(pool.cells),
                            mean_tension=sum(layer_tensions)/len(layer_tensions),
                            split_threshold=pool.split_threshold_eff, phi=pool.phi)]
    max_new = 40
    t_decode_start = time.time()
    for k in range(max_new):
        if next_token.item() >= 256 or idx.size(1) + 1 >= model.block_size: break
        with torch.no_grad():
            logits_a, _, tensions, past_kv, _ = model(next_token, use_cache=True, past_key_values=past_kv)
        layer_tensions = [t.float().mean().item() for t in tensions]
        pool.step(layer_tensions, step_idx)
        per_step_record.append(dict(step=step_idx, phase="decode",
            pool_size=len(pool.cells), mean_tension=sum(layer_tensions) / len(layer_tensions),
            split_threshold=pool.split_threshold_eff, phi=pool.phi))
        next_token = logits_a[:, -1, :].argmax(dim=-1, keepdim=True)
        full_idx.append(next_token.item())
        step_idx += 1
    print(f"[eval3-fast] decode wall={time.time() - t_decode_start:.1f}s steps={step_idx-1}", flush=True)
    gen_bytes = bytes(full_idx[len(idx_list):])
    n_split = sum(1 for e in pool.event_log if e["type"] == "split")
    n_merge = sum(1 for e in pool.event_log if e["type"] == "merge")
    out = dict(
        cell=cell_name, ckpt_path=str(ckpt_path),
        cfg=dict(d_model=cfg["d_model"], n_layer=cfg["n_layer"],
                 lambda_psi=cfg.get("lambda_psi"), lambda_phi=cfg.get("lambda_phi"),
                 seed=cfg.get("seed")),
        prompt_bytes=prompt_bytes.decode("utf-8", errors="replace"),
        prompt_len=len(prompt_bytes), max_new=max_new,
        steps_run=step_idx, initial_cells=initial_cells, final_cells=len(pool.cells),
        n_split=n_split, n_merge=n_merge, next_id=pool.next_id,
        phi_initial=pool.phi_history[0] if pool.phi_history else 0.0,
        phi_final=pool.phi_history[-1] if pool.phi_history else 0.0,
        split_events=pool.event_log[:60], per_step=per_step_record,
        gen_bytes_repr=repr(gen_bytes)[:600],
        gen_utf8=gen_bytes.decode("utf-8", errors="replace"),
        variant="fast",
    )
    out_path = out_dir / f"{cell_name}_eval3.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[eval3-fast] {cell_name}: initial_cells={initial_cells} final_cells={len(pool.cells)} splits={n_split} merges={n_merge}", flush=True)


if __name__ == "__main__":
    main()
