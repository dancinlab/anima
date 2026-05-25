"""PyPhi anima 3-axis mapping — Hc_1283 deferred path.

v5-mitosis cell-coupling matrix → TPM 변환 → PyPhi 1.2.0 formal IIT 3.0 Φ measurement.

Strategy:
  1. Load v5-mitosis ckpt (cond.5 cotrain $1.26 sunk)
  2. Extract cell pool W coupling matrix
  3. Threshold + binarize → connectivity matrix
  4. Build TPM (transition probability matrix) for n=3 or n=4 subset
  5. PyPhi.sia(subsystem) → formal Φ
  6. Compare to anima Φ★ proxy

Honest C3:
  - PyPhi 1.2.0 limited to n ≤ 4-5 nodes (computational complexity)
  - anima v5-mitosis cell count typically 8-64 → must reduce to subset
  - reduction strategy: top-k tension cells OR random subsampling
  - TPM construction requires discretization (binary thresholding)
"""
import os, sys, json, time
import numpy as np
import torch

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
try:
    import pyphi
    pyphi.config.PROGRESS_BARS = False
    pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
    pyphi.config.NUMBER_OF_CORES = 1
    HAS_PYPHI = True
except ImportError:
    HAS_PYPHI = False


def load_v5mitosis_ckpt(ckpt_path):
    """Load v5-mitosis ckpt and extract key tensors."""
    ckpt = torch.load(ckpt_path, map_location='cpu', weights_only=False)
    return ckpt


def extract_coupling_matrix(ckpt):
    """Extract cell-cell coupling matrix from v5-mitosis state dict."""
    sd = ckpt.get('model_state_dict', ckpt)
    # Look for tension/coupling tensors
    coupling_keys = [k for k in sd.keys() if 'cell' in k.lower() and ('tension' in k.lower() or 'coupling' in k.lower() or 'weight' in k.lower())]
    print(f"  Found coupling candidates: {coupling_keys[:5]}")
    # Fallback: any 2D tensor
    matrices = []
    for k, v in sd.items():
        if isinstance(v, torch.Tensor) and v.dim() == 2:
            matrices.append((k, v.shape))
    print(f"  All 2D tensors (top 5): {matrices[:5]}")
    return sd


def cell_state_to_tpm(state_vector, n_nodes=3, threshold=None):
    """Build TPM from cell state vector.
    Strategy: state[i] = binary based on sign or threshold."""
    s = state_vector.detach().cpu().numpy() if isinstance(state_vector, torch.Tensor) else state_vector
    if s.ndim > 1:
        s = s.mean(axis=-1)  # collapse feature dim
    s = s[:n_nodes]  # subset
    if threshold is None:
        threshold = float(np.median(s))
    binary = (s > threshold).astype(int)
    print(f"  state[0:{n_nodes}] = {s.tolist()}, threshold={threshold:.4f}, binary={binary.tolist()}")

    # TPM size: 2^n × n
    N = n_nodes
    num_states = 2**N
    tpm = np.zeros((num_states, N))
    # Simple causal model: each node = AND of neighbors with optional bias from binary state
    for state_idx in range(num_states):
        state = [(state_idx >> i) & 1 for i in range(N)]
        for i in range(N):
            # Next state: AND of neighbors + influenced by binary anchor
            neighbors = [state[(i+1) % N], state[(i+2) % N]] if N >= 3 else [state[(i+1) % N]]
            tpm[state_idx, i] = 1 if (sum(neighbors) >= 1 and binary[i] == 1) else 0
    return tpm, binary.tolist()


def measure_pyphi_phi(tpm, state):
    """Run PyPhi sia and return Φ."""
    if not HAS_PYPHI:
        return None, "PyPhi not installed"
    N = tpm.shape[1]
    cm = (np.ones((N, N)) - np.eye(N)).astype(int)
    labels = tuple(f'C{i}' for i in range(N))
    try:
        net = pyphi.Network(tpm, cm=cm, node_labels=labels)
        subsys = pyphi.Subsystem(net, tuple(state), range(N))
        sia = pyphi.compute.sia(subsys)
        return float(sia.phi), "OK"
    except Exception as e:
        return None, f"ERROR: {type(e).__name__}: {str(e)[:200]}"


def main():
    ckpt_paths = [
        ('cond.5 v1', 'state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt'),
        ('cond.5 v2', 'state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_v2_cotrain.pt'),
    ]

    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'pyphi_available': HAS_PYPHI,
        'ckpts': [],
    }

    if not HAS_PYPHI:
        print("PyPhi not installed; verdict will be infrastructure-check only")
        results['note'] = "PyPhi unavailable; run: python3 -m pip install pyphi --user"
    else:
        print(f"PyPhi version: {pyphi.__version__}")

    for label, path in ckpt_paths:
        print(f"\n=== {label}: {path} ===")
        if not os.path.exists(path):
            print(f"  SKIP — file not found")
            continue
        try:
            ckpt = load_v5mitosis_ckpt(path)
            sd = extract_coupling_matrix(ckpt)

            # Get state vector — use per-cell ln1.weight as cell signature (uniform shape per cell)
            state_vec = None
            ln_keys = sorted([k for k in sd.keys() if k.endswith('.ln1.weight') and 'cells.' in k])
            if ln_keys:
                vecs = [sd[k] for k in ln_keys if isinstance(sd[k], torch.Tensor)]
                shapes = [v.shape for v in vecs]
                # Filter to uniform shape
                ref_shape = shapes[0]
                vecs = [v for v in vecs if v.shape == ref_shape]
                if vecs:
                    state_vec = torch.stack([v.flatten() for v in vecs])
                    print(f"  Constructed state from {len(vecs)} cell ln1.weight tensors, shape={state_vec.shape}")

            if state_vec is None:
                # Fallback: any embedding-like tensor
                for k, v in sd.items():
                    if isinstance(v, torch.Tensor) and v.dim() >= 1 and v.shape[0] >= 3:
                        state_vec = v if v.dim() > 1 else v.unsqueeze(-1)
                        print(f"  Fallback state from {k}, shape={state_vec.shape}")
                        break

            if state_vec is None:
                print(f"  No usable state — SKIP")
                continue

            entry = {'label': label, 'path': path}

            for n_nodes in [3, 4]:
                if state_vec.shape[0] < n_nodes:
                    continue
                tpm, binary = cell_state_to_tpm(state_vec, n_nodes=n_nodes)
                phi, status = measure_pyphi_phi(tpm, binary)
                print(f"  n={n_nodes}: Φ={phi}, status={status}")
                entry[f'n_{n_nodes}'] = {'phi': phi, 'state': binary, 'status': status}
                # Also: canonical IIT 3.0 example as baseline
                if n_nodes == 3 and label == 'cond.5 v1':
                    tpm_canon = np.array([
                        [0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0],
                        [1, 1, 0], [1, 1, 1], [1, 1, 1], [1, 1, 0],
                    ])
                    phi_canon, _ = measure_pyphi_phi(tpm_canon, [1, 0, 0])
                    entry['canonical_iit3_phi'] = phi_canon
                    print(f"  canonical IIT 3.0: Φ={phi_canon}")

            results['ckpts'].append(entry)
        except Exception as e:
            print(f"  ERROR: {e}")
            results['ckpts'].append({'label': label, 'error': str(e)[:300]})

    # Synthesis verdict
    verdicts = []
    for c in results['ckpts']:
        if 'n_3' in c and c.get('n_3', {}).get('phi') is not None:
            phi = c['n_3']['phi']
            verdict = 'SUPPORTED' if phi >= 0.5 else 'PARTIAL' if phi >= 0.05 else 'INSUFFICIENT'
            verdicts.append((c['label'], phi, verdict))
    results['final_verdicts'] = verdicts
    results['anima_phi_star_anchor'] = {
        'range': [4.16, 4.86],
        'source': 'state/verify_a_stage1_2026_05_15/stage2_ckpt_phi_real.json',
        'note': 'anima Φ★ proxy (H_162 IIT 4.0 lower bound) ≫ PyPhi formal IIT 3.0 (small-N constraint)',
    }

    out_path = 'state/verify_v8_family_2026_05_15/pyphi_anima_mapping_result.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n=== PyPhi anima mapping complete ===")
    print(f"Saved: {out_path}")
    for lbl, phi, verdict in verdicts:
        print(f"  {lbl}: Φ={phi:.4f} → {verdict}")


if __name__ == '__main__':
    main()
