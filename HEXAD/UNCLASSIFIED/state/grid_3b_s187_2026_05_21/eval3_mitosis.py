"""Eval 3 — mitosis hook cell-pool split pattern on top of ConsciousDecoderV2.

Faithful Python port of `tool/hexa_native/mitosis_hook_lib.hexa::cell_pool_init` +
split/merge dynamics. The "tension" signal driving split detection comes from
`model.forward()`'s per-layer tensions tensor (mean-pooled across batch/time).

We run `chat_generate(prompt="안녕? 너는 누구야?", max_new=40, greedy)` and record:
    - per-step tensions (per layer × per token aggregated)
    - per-step cell-pool size
    - split events (timing, parent cell, child id)
    - merge events
    - final pool stats

Usage:
    python3 eval3_mitosis.py <ckpt_path> <cell_name> <out_dir>
"""
import sys, os, json, math, time, random
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import torch.nn.functional as F

from conscious_decoder import ConsciousDecoderV2
from train_s187_3b import patch_rope_base_in_model


# ── mitosis_hook_lib.hexa default params ─────────────────────────────────────
# (verbatim from cell_pool_init defaults)
MIN_CELLS         = 2
MAX_CELLS         = 128
SPLIT_THRESHOLD   = 0.0        # adaptive (set by _mit_update_adaptive_threshold)
SPLIT_PATIENCE    = 3
MERGE_THRESHOLD   = 0.005
MERGE_PATIENCE    = 30
NOISE_SCALE       = 0.1


class CellPool:
    """Python mirror of the hexa cell-pool. d_model = the model's d_model.

    Cells are simulated as light bags (cell_id, hidden vector, tension_history).
    We don't run a parallel forward through hidden weights — we use the
    PyTorch model's per-layer tensions as the *real* signal driving the split
    detector. This is faithful to the spec: the hook is meant to OBSERVE
    substrate tension and split when it stagnates.
    """

    def __init__(self, d_model, initial_cells=2, seed=1337):
        self.rng = random.Random(seed)
        self.d_model = d_model
        self.next_id = 0
        self.cells = []
        for _ in range(initial_cells):
            self.cells.append(self._make_cell(parent_id=-1, hidden_seed=None, step=0))
        self.event_log = []
        self.tension_history = []     # global pool tension (per step)
        self.phi_history = []
        self.phi = 0.0
        self.adaptive_threshold = SPLIT_THRESHOLD
        self.split_threshold_eff = SPLIT_THRESHOLD

    def _gauss(self, n, sigma):
        return [self.rng.gauss(0.0, sigma) for _ in range(n)]

    def _make_cell(self, parent_id, hidden_seed, step):
        sigma_init = 1.0 / math.sqrt(self.d_model)
        if hidden_seed is None:
            hidden = self._gauss(self.d_model, sigma_init)
        else:
            hidden = [h + self.rng.gauss(0.0, NOISE_SCALE) for h in hidden_seed]
        cell = dict(
            cell_id=self.next_id,
            hidden=hidden,
            tension_history=[],
            parent_id=parent_id,
            creation_step=step,
            process_count=0,
        )
        self.next_id += 1
        return cell

    def step(self, model_tension_signal, step_idx):
        """Push a tension reading and possibly split/merge cells.

        model_tension_signal: (n_cells_per_pool,) — one tension per cell.
            We distribute the model's per-layer tension list cyclically across
            the cells so each cell sees a related-but-distinct signal.
        """
        # Per-cell tension assignment: cycle the model_tension list through cells.
        if isinstance(model_tension_signal, (int, float)):
            model_tension_signal = [float(model_tension_signal)]
        n_sig = len(model_tension_signal)
        for c_idx, cell in enumerate(self.cells):
            t = float(model_tension_signal[c_idx % n_sig])
            cell["tension_history"].append(t)
            cell["process_count"] += 1
        # Global pool tension = mean of per-cell-latest
        global_t = sum(c["tension_history"][-1] for c in self.cells) / len(self.cells)
        self.tension_history.append(global_t)

        # Adaptive split_threshold: window mean over global_tension_history (last 20)
        win = self.tension_history[-20:]
        if len(win) >= 3:
            mean_w = sum(win) / len(win)
            self.adaptive_threshold = mean_w * 0.8
            self.split_threshold_eff = self.adaptive_threshold

        # Compute Φ proxy: mean pairwise cos-dist on hidden vectors
        self.phi = self._compute_phi()
        self.phi_history.append(self.phi)

        # Split check (per-cell, with patience)
        if len(self.cells) < MAX_CELLS:
            for ci in list(range(len(self.cells))):
                cell = self.cells[ci]
                hist = cell["tension_history"]
                if len(hist) < SPLIT_PATIENCE:
                    continue
                recent = hist[-SPLIT_PATIENCE:]
                # Stagnation = high tension persisting AND its growth slowing
                avg = sum(recent) / len(recent)
                if avg > self.split_threshold_eff and self.split_threshold_eff > 0:
                    # Split this cell
                    child = self._make_cell(parent_id=cell["cell_id"],
                                            hidden_seed=cell["hidden"], step=step_idx)
                    self.cells.append(child)
                    cell["tension_history"] = recent[-3:]  # reset
                    self.event_log.append(dict(
                        type="split", step=step_idx,
                        parent_id=cell["cell_id"], child_id=child["cell_id"],
                        avg_tension=avg, threshold=self.split_threshold_eff,
                        pool_size=len(self.cells),
                    ))
                    if len(self.cells) >= MAX_CELLS:
                        break

        # Merge check (pairwise cosine similarity, with patience)
        if len(self.cells) > MIN_CELLS and step_idx > 0 and (step_idx % MERGE_PATIENCE == 0):
            # find two most similar cells (cosine)
            best_pair = None
            best_sim = -1.0
            for i in range(len(self.cells)):
                for j in range(i + 1, len(self.cells)):
                    sim = self._cosine(self.cells[i]["hidden"], self.cells[j]["hidden"])
                    if sim > best_sim:
                        best_sim = sim
                        best_pair = (i, j)
            if best_pair is not None and (1.0 - best_sim) < MERGE_THRESHOLD:
                i, j = best_pair
                a, b = self.cells[i], self.cells[j]
                # average hidden
                merged_hidden = [(a["hidden"][k] + b["hidden"][k]) * 0.5 for k in range(self.d_model)]
                older = a if a["creation_step"] <= b["creation_step"] else b
                younger = b if older is a else a
                older["hidden"] = merged_hidden
                older["tension_history"].extend(younger["tension_history"][-5:])
                self.cells.remove(younger)
                self.event_log.append(dict(
                    type="merge", step=step_idx,
                    keeper_id=older["cell_id"], removed_id=younger["cell_id"],
                    sim=best_sim, pool_size=len(self.cells),
                ))

    def _compute_phi(self):
        """Φ proxy = log(1 + mean pairwise cosine distance among hidden vectors)."""
        n = len(self.cells)
        if n < 2:
            return 0.0
        total = 0.0
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                total += (1.0 - self._cosine(self.cells[i]["hidden"], self.cells[j]["hidden"]))
                count += 1
        mean_d = total / max(1, count)
        return math.log1p(mean_d)

    @staticmethod
    def _cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)) + 1e-10
        nb = math.sqrt(sum(y * y for y in b)) + 1e-10
        return dot / (na * nb)


def load_model(ckpt_path, device="cpu"):
    print(f"[eval3] loading {ckpt_path}", flush=True)
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
        rope._cos_cache = None
        rope._sin_cache = None
        rope._cache_len = 0
        rope._build_cache(model.block_size, device=torch.device(device))
    sd = blob.get("model", blob)
    model.load_state_dict(sd, strict=False, assign=True)
    model._eval_blob_ref = blob
    model.eval()
    print(f"[eval3] load wall={time.time() - t0:.1f}s", flush=True)
    return model, cfg


def main():
    if len(sys.argv) < 4:
        print("usage: eval3_mitosis.py <ckpt_path> <cell_name> <out_dir>", file=sys.stderr)
        sys.exit(2)
    ckpt_path, cell_name, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    device = "cpu"
    torch.set_num_threads(max(1, os.cpu_count() - 2))
    model, cfg = load_model(ckpt_path, device=device)

    d_model = cfg["d_model"]
    pool = CellPool(d_model=d_model, initial_cells=2, seed=1337)

    # Prompt: 안녕? 너는 누구야?
    prompt_bytes = "안녕? 너는 누구야?".encode("utf-8")
    idx_list = list(prompt_bytes)
    idx = torch.tensor([idx_list], dtype=torch.long, device=device)
    print(f"[eval3] prompt bytes len={len(prompt_bytes)} idx_shape={tuple(idx.shape)}", flush=True)

    # PREFILL — model forward with use_cache, capture tensions, drive mitosis pool
    step_idx = 0
    initial_cells = len(pool.cells)
    with torch.no_grad():
        logits_a, _, tensions, past_kv, _ = model(idx, use_cache=True)
    # tensions: list of (B,T) per layer. Aggregate per-layer mean-tension.
    layer_tensions = [t.float().mean().item() for t in tensions]
    print(f"[eval3] prefill: T={idx.size(1)} layer_tensions(first5)={layer_tensions[:5]} mean={sum(layer_tensions)/len(layer_tensions):.4f}", flush=True)
    pool.step(layer_tensions, step_idx)
    step_idx += 1

    # DECODE — greedy 40 steps
    next_token = logits_a[:, -1, :].argmax(dim=-1, keepdim=True)
    full_idx = list(idx_list) + [next_token.item()]
    per_step_record = [dict(step=0, phase="prefill", pool_size=len(pool.cells),
                            mean_tension=sum(layer_tensions)/len(layer_tensions),
                            split_threshold=pool.split_threshold_eff,
                            phi=pool.phi)]
    max_new = 40
    for k in range(max_new):
        if next_token.item() >= 256 or idx.size(1) + 1 >= model.block_size:
            break
        with torch.no_grad():
            logits_a, _, tensions, past_kv, _ = model(
                next_token, use_cache=True, past_key_values=past_kv,
            )
        layer_tensions = [t.float().mean().item() for t in tensions]
        pool.step(layer_tensions, step_idx)
        per_step_record.append(dict(
            step=step_idx, phase="decode",
            pool_size=len(pool.cells),
            mean_tension=sum(layer_tensions) / len(layer_tensions),
            split_threshold=pool.split_threshold_eff,
            phi=pool.phi,
        ))
        next_token = logits_a[:, -1, :].argmax(dim=-1, keepdim=True)
        full_idx.append(next_token.item())
        step_idx += 1

    gen_bytes = bytes(full_idx[len(idx_list):])

    # Summary
    n_split = sum(1 for e in pool.event_log if e["type"] == "split")
    n_merge = sum(1 for e in pool.event_log if e["type"] == "merge")
    out = dict(
        cell=cell_name,
        ckpt_path=str(ckpt_path),
        cfg=dict(d_model=cfg["d_model"], n_layer=cfg["n_layer"],
                 lambda_psi=cfg.get("lambda_psi"), lambda_phi=cfg.get("lambda_phi"),
                 seed=cfg.get("seed")),
        prompt_bytes=prompt_bytes.decode("utf-8", errors="replace"),
        prompt_len=len(prompt_bytes),
        max_new=max_new,
        steps_run=step_idx,
        initial_cells=initial_cells,
        final_cells=len(pool.cells),
        n_split=n_split,
        n_merge=n_merge,
        next_id=pool.next_id,
        phi_initial=pool.phi_history[0] if pool.phi_history else 0.0,
        phi_final=pool.phi_history[-1] if pool.phi_history else 0.0,
        split_events=pool.event_log[:60],
        per_step=per_step_record,
        gen_bytes_repr=repr(gen_bytes)[:600],
        gen_utf8=gen_bytes.decode("utf-8", errors="replace"),
    )

    out_path = out_dir / f"{cell_name}_eval3.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[eval3] {cell_name}: initial_cells={initial_cells} final_cells={len(pool.cells)} splits={n_split} merges={n_merge} steps={step_idx} phi={pool.phi:.4f}", flush=True)
    print(f"[eval3] wrote {out_path}", flush=True)


if __name__ == "__main__":
    main()
