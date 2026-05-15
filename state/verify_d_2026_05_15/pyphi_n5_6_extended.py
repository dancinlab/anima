"""PyPhi n=5,6 extended — push computational limit on cell pool RoM TPM.

n=5: ~5min, n=6: ~30min wall on Mac CPU
Builds on pyphi_rom_cycle.py — same RoM strategy with larger N.
"""
import os, sys, json, time
import numpy as np
import torch
from collections import Counter

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
import pyphi
pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1


def load_cell_signatures(ckpt_path):
    ckpt = torch.load(ckpt_path, map_location='cpu', weights_only=False)
    sd = ckpt.get('model_state_dict', ckpt)
    cell_idx = 0
    cell_sigs = []
    while True:
        keys = [f'cells.{cell_idx}.ln1.weight', f'cells.{cell_idx}.ln2.weight']
        if not all(k in sd for k in keys):
            break
        sig = torch.cat([sd[k].flatten() for k in keys])
        cell_sigs.append(sig)
        cell_idx += 1
    return torch.stack(cell_sigs) if cell_sigs else None


def select_top_correlated(sigs, n_select=3):
    sigs_n = sigs / (sigs.norm(dim=1, keepdim=True) + 1e-9)
    cos_mat = sigs_n @ sigs_n.t()
    cos_mat.fill_diagonal_(0)
    flat_idx = cos_mat.flatten().argmax().item()
    i, j = flat_idx // cos_mat.shape[0], flat_idx % cos_mat.shape[0]
    selected = [int(i), int(j)]
    while len(selected) < n_select:
        scores = cos_mat[selected].sum(dim=0)
        for s in selected:
            scores[s] = -1
        next_idx = scores.argmax().item()
        selected.append(int(next_idx))
    return selected


def sample_cell_dynamics(sigs, selected_cells, n_samples=1000, seed=42):
    torch.manual_seed(seed)
    sub_sigs = sigs[selected_cells]
    N, D = sub_sigs.shape
    states = []
    for t in range(n_samples):
        x = torch.randn(D)
        tensions = (sub_sigs @ x) / (sub_sigs.norm(dim=1) * x.norm() + 1e-9)
        threshold = tensions.median()
        binary = (tensions > threshold).int().tolist()
        states.append(tuple(binary))
    return states


def states_to_empirical_tpm(states, n_nodes):
    num_states = 2**n_nodes
    transition_counts = np.zeros((num_states, num_states))
    for i in range(len(states) - 1):
        s_idx = sum(b << k for k, b in enumerate(states[i]))
        n_idx = sum(b << k for k, b in enumerate(states[i+1]))
        transition_counts[s_idx, n_idx] += 1
    tpm = np.zeros((num_states, n_nodes))
    for s_idx in range(num_states):
        row_total = transition_counts[s_idx].sum()
        if row_total == 0:
            for i in range(n_nodes):
                tpm[s_idx, i] = (s_idx >> i) & 1
            continue
        for i in range(n_nodes):
            count_one = sum(transition_counts[s_idx, n_idx]
                            for n_idx in range(num_states)
                            if (n_idx >> i) & 1)
            tpm[s_idx, i] = count_one / row_total
    return tpm, transition_counts


def measure_phi(tpm, state, timeout_min=60):
    N = tpm.shape[1]
    cm = (np.ones((N, N)) - np.eye(N)).astype(int)
    labels = tuple(f'C{i}' for i in range(N))
    t0 = time.time()
    try:
        net = pyphi.Network(tpm, cm=cm, node_labels=labels)
        subsys = pyphi.Subsystem(net, tuple(state), range(N))
        sia = pyphi.compute.sia(subsys)
        wall = time.time() - t0
        return float(sia.phi), 'OK', wall
    except Exception as e:
        wall = time.time() - t0
        return None, f"ERROR: {type(e).__name__}: {str(e)[:200]}", wall


def main():
    ckpt_path = 'state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt'
    sigs = load_cell_signatures(ckpt_path)
    if sigs is None:
        print("ERROR — no cell signatures")
        return

    print(f"Loaded {sigs.shape[0]} cells, sig dim {sigs.shape[1]}")
    results = {'pyphi_version': pyphi.__version__, 'measurements': []}

    for n_nodes in [5, 6]:
        print(f"\n=== n={n_nodes} ===")
        selected = select_top_correlated(sigs, n_select=n_nodes)
        print(f"  selected cells = {selected}")
        states = sample_cell_dynamics(sigs, selected, n_samples=1000)
        tpm, counts = states_to_empirical_tpm(states, n_nodes)
        unique = len(set(states))
        print(f"  sampled 1000 states, unique={unique}/{2**n_nodes}")
        top_state = Counter(states).most_common(1)[0][0]
        print(f"  measuring Φ at state={top_state}...")
        phi, status, wall = measure_phi(tpm, top_state)
        print(f"  Φ={phi}, wall={wall:.1f}s, status={status}")
        results['measurements'].append({
            'n': n_nodes,
            'selected_cells': selected,
            'top_state': top_state,
            'phi': phi,
            'wall_sec': wall,
            'status': status,
        })
        if wall > 600:
            print(f"  WARNING — n={n_nodes} took {wall/60:.1f}min")

    out_path = 'state/verify_d_2026_05_15/pyphi_n5_6_result.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")


if __name__ == '__main__':
    main()
