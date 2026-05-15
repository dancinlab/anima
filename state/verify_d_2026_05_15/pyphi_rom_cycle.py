"""PyPhi Reduced-Order Model (RoM) cycle — better TPM construction.

Strategy:
  1. Load v5-mitosis ckpt → cell pool (64 cells × d=384)
  2. Build cell-pair correlation matrix (64×64 cosine similarity)
  3. Top-N select most-correlated cells (N ∈ {3, 4})
  4. Sample dynamic states from forward propagation (synthetic input → cell activations)
  5. Discretize state samples → empirical TPM (count transitions)
  6. PyPhi.sia(subsystem) → formal Φ
  7. Compare to anima Φ★ proxy + previous naive TPM

Honest C3:
  - Still small-N (PyPhi 1.2.0 limit) — full 64-cell formal IIT impossible
  - Synthetic input dynamic — not real chat usage
  - Top-N correlation reduction = lossy projection
"""
import os, sys, json, time
import numpy as np
import torch

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
import pyphi
pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1


def load_cell_signatures(ckpt_path):
    """Extract per-cell signature vectors from v5-mitosis ckpt."""
    ckpt = torch.load(ckpt_path, map_location='cpu', weights_only=False)
    sd = ckpt.get('model_state_dict', ckpt)

    # Use multiple per-cell layer weights as composite signature
    cell_idx = 0
    cell_sigs = []
    while True:
        keys = [
            f'cells.{cell_idx}.ln1.weight',
            f'cells.{cell_idx}.ln2.weight',
        ]
        if not all(k in sd for k in keys):
            break
        sig = torch.cat([sd[k].flatten() for k in keys])
        cell_sigs.append(sig)
        cell_idx += 1

    if not cell_sigs:
        return None
    return torch.stack(cell_sigs)


def select_top_correlated(sigs, n_select=3):
    """Find n_select cells with highest mutual cosine similarity (most coupled)."""
    sigs_n = sigs / (sigs.norm(dim=1, keepdim=True) + 1e-9)
    cos_mat = sigs_n @ sigs_n.t()
    cos_mat.fill_diagonal_(0)
    # Greedy: start with top-correlated pair, add next-most-correlated cell
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


def sample_cell_dynamics(sigs, selected_cells, n_samples=500, seed=42):
    """Sample dynamic states by perturbing input + measuring binarized cell tensions."""
    torch.manual_seed(seed)
    sub_sigs = sigs[selected_cells]  # (N, D)
    N, D = sub_sigs.shape

    states = []
    for t in range(n_samples):
        # Random perturbation input (noise)
        x = torch.randn(D)
        # Measure each cell's "tension" = cos sim with input
        tensions = (sub_sigs @ x) / (sub_sigs.norm(dim=1) * x.norm() + 1e-9)
        # Binarize at median across cells
        threshold = tensions.median()
        binary = (tensions > threshold).int().tolist()
        states.append(tuple(binary))

    return states


def states_to_empirical_tpm(states, n_nodes):
    """Build empirical TPM from observed transitions (state -> next_state)."""
    num_states = 2**n_nodes
    transition_counts = np.zeros((num_states, num_states))

    for i in range(len(states) - 1):
        s_idx = sum(b << k for k, b in enumerate(states[i]))
        n_idx = sum(b << k for k, b in enumerate(states[i+1]))
        transition_counts[s_idx, n_idx] += 1

    # TPM: P(next_node_state | current_state). PyPhi uses node-by-node TPM.
    # For each state, marginal P(node_i = 1 | current state)
    tpm = np.zeros((num_states, n_nodes))
    for s_idx in range(num_states):
        row_total = transition_counts[s_idx].sum()
        if row_total == 0:
            # Default: maintain current state
            for i in range(n_nodes):
                tpm[s_idx, i] = (s_idx >> i) & 1
            continue
        for i in range(n_nodes):
            # P(node i = 1 in next state)
            mask = sum(1 << i for i in range(n_nodes))
            count_one = sum(transition_counts[s_idx, n_idx]
                            for n_idx in range(num_states)
                            if (n_idx >> i) & 1)
            tpm[s_idx, i] = count_one / row_total

    return tpm, transition_counts


def measure_phi(tpm, state):
    N = tpm.shape[1]
    cm = (np.ones((N, N)) - np.eye(N)).astype(int)
    labels = tuple(f'C{i}' for i in range(N))
    try:
        net = pyphi.Network(tpm, cm=cm, node_labels=labels)
        subsys = pyphi.Subsystem(net, tuple(state), range(N))
        sia = pyphi.compute.sia(subsys)
        return float(sia.phi), 'OK'
    except Exception as e:
        return None, f"ERROR: {type(e).__name__}: {str(e)[:200]}"


def main():
    ckpt_paths = [
        ('cond.5 v1', 'state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt'),
        ('cond.5 v2', 'state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_v2_cotrain.pt'),
    ]

    results = {'pyphi_version': pyphi.__version__, 'ckpts': []}

    for label, path in ckpt_paths:
        print(f"\n=== RoM cycle: {label} ===")
        if not os.path.exists(path):
            print("  SKIP — not found")
            continue

        sigs = load_cell_signatures(path)
        if sigs is None:
            print("  SKIP — no cell signatures")
            continue
        print(f"  Loaded {sigs.shape[0]} cells, sig dim {sigs.shape[1]}")

        entry = {'label': label, 'n_cells': sigs.shape[0]}
        for n_nodes in [3, 4]:
            selected = select_top_correlated(sigs, n_select=n_nodes)
            print(f"  n={n_nodes}: top-correlated cells = {selected}")
            states = sample_cell_dynamics(sigs, selected, n_samples=500)
            unique_states = len(set(states))
            tpm, counts = states_to_empirical_tpm(states, n_nodes)
            print(f"    sampled {len(states)} states, unique={unique_states}/{2**n_nodes}, transitions={int(counts.sum())}")
            # Use most-frequent state for measurement
            from collections import Counter
            top_state = Counter(states).most_common(1)[0][0]
            phi, status = measure_phi(tpm, top_state)
            print(f"    Φ (RoM TPM, state={top_state}): {phi}, status={status}")
            entry[f'n_{n_nodes}'] = {
                'selected_cells': selected,
                'unique_states': unique_states,
                'top_state': top_state,
                'phi': phi,
                'status': status,
            }

        results['ckpts'].append(entry)

    out_path = 'state/verify_d_2026_05_15/pyphi_rom_result.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n=== PyPhi RoM cycle complete ===")
    print(f"Saved: {out_path}")
    for c in results['ckpts']:
        for k in ['n_3', 'n_4']:
            if k in c:
                print(f"  {c['label']} {k}: Φ={c[k]['phi']}")


if __name__ == '__main__':
    main()
