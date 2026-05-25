"""H_178 frustration + H_182/H_187 surrogate AT-RISK PyPhi RoM cross-check.

H_178: Frustration 50% optimum — non-monotone peak claim. Sweep frustration param ∈ {0%, 25%, 50%, 75%, 100%} and check if PyPhi Φ peaks at 50%.

H_182/H_187: V8 surrogate-tier (B-bio, Trinity-TB-DOM). Build TPM from V8 mechanism graft state, measure PyPhi Φ.

All n=3 (PyPhi small-N, fast wall ~10sec each)."""
import os, sys, json, time
import numpy as np
import torch

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
import pyphi
pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1


def state_to_tpm_via_dynamics(state, n_nodes=3, n_samples=500, seed=42):
    """Generate states via random perturbation + binarize → empirical TPM"""
    torch.manual_seed(seed)
    sigs = state[:n_nodes]  # take first n
    states = []
    for t in range(n_samples):
        x = torch.randn(sigs.shape[1])
        tensions = (sigs @ x) / (sigs.norm(dim=1) * x.norm() + 1e-9)
        binary = (tensions > tensions.median()).int().tolist()
        states.append(tuple(binary))

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

    from collections import Counter
    top_state = Counter(states).most_common(1)[0][0]
    return tpm, top_state


def measure_phi(tpm, state, n_nodes):
    cm = (np.ones((n_nodes, n_nodes)) - np.eye(n_nodes)).astype(int)
    labels = tuple(f'C{i}' for i in range(n_nodes))
    try:
        net = pyphi.Network(tpm, cm=cm, node_labels=labels)
        subsys = pyphi.Subsystem(net, tuple(state), range(n_nodes))
        sia = pyphi.compute.sia(subsys)
        return float(sia.phi), 'OK'
    except Exception as e:
        return None, f"ERR: {type(e).__name__}: {str(e)[:100]}"


def h178_frustration_sweep():
    """Sweep antiferromagnetic frustration 0-100% on hypercube-like substrate"""
    print("\n=== H_178 frustration sweep ===")
    D = 32  # smaller for speed
    N_CELLS = 8
    results = {}
    for frust_pct in [0, 25, 50, 75, 100]:
        torch.manual_seed(42)
        state = torch.randn(N_CELLS, D)
        # Frustration: flip frust_pct % of cell-pair couplings sign
        coupling = torch.randn(N_CELLS, N_CELLS) * 0.3
        coupling = (coupling + coupling.t()) / 2
        coupling.fill_diagonal_(0)
        n_flip = int(N_CELLS * (N_CELLS-1) / 2 * frust_pct / 100)
        flip_count = 0
        for i in range(N_CELLS):
            for j in range(i+1, N_CELLS):
                if flip_count < n_flip:
                    coupling[i, j] = -abs(coupling[i, j])
                    coupling[j, i] = coupling[i, j]
                    flip_count += 1
        # Update state via coupling
        for _ in range(50):
            state = state + 0.1 * coupling @ state
            state = torch.tanh(state)
        tpm, top_state = state_to_tpm_via_dynamics(state, n_nodes=3)
        phi, status = measure_phi(tpm, top_state, 3)
        results[f'frust_{frust_pct}pct'] = {'phi': phi, 'state': top_state, 'status': status}
        print(f"  frustration {frust_pct}%: Φ = {phi}")

    # Check peak at 50%
    phis = [results[f'frust_{p}pct']['phi'] for p in [0, 25, 50, 75, 100]]
    valid = [p for p in phis if p is not None]
    if len(valid) >= 5 and phis[2] is not None:
        peak_at_50 = phis[2] > max(phis[0], phis[4]) and phis[2] >= phis[1] and phis[2] >= phis[3]
        print(f"  peak at 50%: {peak_at_50}")
        results['peak_at_50_verdict'] = 'SUPPORTED' if peak_at_50 else 'NOT-PASSED'
    else:
        results['peak_at_50_verdict'] = 'INSUFFICIENT (some phi NULL)'
    return results


def v8_family_pyphi(family_name, mechanism_fn, n_mechanism=3):
    """V8 family PyPhi audit — sample n_mechanism mechanisms"""
    print(f"\n=== V8 {family_name} PyPhi RoM ===")
    D = 32
    N_CELLS = 8
    results = {}
    for mech_idx in range(n_mechanism):
        torch.manual_seed(42 + mech_idx)
        state = torch.randn(N_CELLS, D)
        # Apply mechanism perturbation (simplified)
        perturbed = mechanism_fn(state, mech_idx)
        tpm, top_state = state_to_tpm_via_dynamics(perturbed, n_nodes=3)
        phi, status = measure_phi(tpm, top_state, 3)
        results[f'mech_{mech_idx}'] = {'phi': phi, 'status': status}
        print(f"  mechanism {mech_idx}: Φ = {phi}")
    return results


def b_bio_mech(state, idx):
    """B-bio mechanism: synaptic-coupling-like"""
    mask = torch.where(torch.randn(state.shape[0]) > 0, 1.0, -1.0).unsqueeze(1)
    return state + torch.tanh(state * 2.0) * mask * 0.5

def trinity_mech(state, idx):
    """Trinity 3-axis fusion"""
    N = state.shape[0]
    third = max(1, N // 3)
    a = state[:third]; b = state[third:2*third]; c = state[2*third:]
    if a.shape[0] == 0 or b.shape[0] == 0:
        return state
    out_a = a + b.mean(0, keepdim=True) * 0.3
    out_b = b + c.mean(0, keepdim=True) * 0.3
    out_c = c + a.mean(0, keepdim=True) * 0.3
    out = torch.cat([out_a, out_b, out_c])
    if out.shape[0] < N:
        out = torch.cat([out, state[out.shape[0]:]])
    return out[:N]


def main():
    results = {
        'pyphi_version': pyphi.__version__,
        'h178_frustration_sweep': h178_frustration_sweep(),
        'h182_b_bio_pyphi': v8_family_pyphi('B-bio', b_bio_mech, 3),
        'h187_trinity_pyphi': v8_family_pyphi('Trinity-TB-DOM', trinity_mech, 3),
    }

    # Aggregate verdicts
    # H_178 verdict
    h178_v = results['h178_frustration_sweep'].get('peak_at_50_verdict', 'INSUFFICIENT')

    # V8 surrogate cross-check: PyPhi Φ vs anima Φ★ surrogate
    h182_phis = [m['phi'] for m in results['h182_b_bio_pyphi'].values() if isinstance(m.get('phi'), (int, float))]
    h187_phis = [m['phi'] for m in results['h187_trinity_pyphi'].values() if isinstance(m.get('phi'), (int, float))]

    h182_mean = float(np.mean(h182_phis)) if h182_phis else None
    h187_mean = float(np.mean(h187_phis)) if h187_phis else None

    results['aggregate'] = {
        'h178_frustration_50_peak_verdict': h178_v,
        'h182_pyphi_mean': h182_mean,
        'h187_pyphi_mean': h187_mean,
        'h182_supported_if_phi_above_0_5': bool(h182_mean is not None and h182_mean > 0.5),
        'h187_supported_if_phi_above_0_5': bool(h187_mean is not None and h187_mean > 0.5),
        'cross_check_note': 'surrogate PASS (78.5/100%) → PyPhi formal Φ > 0.5 면 SUPPORTED-CROSS-CONFIRMED; else AT-RISK 유지',
    }

    out_path = 'state/verify_d_2026_05_15/h178_h182_h187_pyphi_rom_result.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n=== Saved: {out_path} ===")
    print(f"  H_178 verdict: {h178_v}")
    print(f"  H_182 PyPhi mean Φ: {h182_mean}")
    print(f"  H_187 PyPhi mean Φ: {h187_mean}")


if __name__ == '__main__':
    main()
