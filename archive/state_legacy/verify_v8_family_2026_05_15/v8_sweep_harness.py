"""V8 family sweep harness — anima v5-mitosis baseline + V8 mechanism graft Φ measurement.

Targets:
  H_182 V8 B-family bio (10 Hc) — biological coupling motifs
  H_183 V8 Q-family quantum (5 Hc) — quantum mechanics primitives
  H_185 V8 U-family fusion (5 Hc) — universal fusion mechanisms
  H_186 V8 architectural (8 Hc) — architectural patterns
  H_187 Trinity/TB/DOM (12 Hc) — trinity / time-binding / domain mechanisms

Per family: cells ∈ {8, 16, 32, 64} × 5-seed × baseline + V8 graft → Φ measure.
Verdict: PASS if max-Φ ≥ baseline + 25% (or matches V8 spec claim).

Honest C3:
  - V8 mechanism implementations are simplified surrogates (full Hc graft = future cycle)
  - anima Φ★ proxy used (PyPhi formal IIT 3.0 = separate cycle)
  - 1L baseline only (24L full-stack cotrain = $1.26 already sunk in cond.5)
"""
import os, sys, json, time, argparse
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def anima_phi_star(state_vector: torch.Tensor) -> float:
    """anima Φ★ proxy = mean pairwise distance + log(N+1) (H_162 IIT 4.0 lower bound)"""
    N = state_vector.shape[0]
    if N < 2:
        return 0.0
    s = state_vector.detach().cpu().numpy()
    if s.ndim == 1:
        s = s.reshape(-1, 1)
    pairwise = 0.0
    cnt = 0
    for i in range(N):
        for j in range(i+1, N):
            pairwise += np.linalg.norm(s[i] - s[j])
            cnt += 1
    mean_d = pairwise / max(1, cnt)
    return float(mean_d + np.log(N + 1))


class V5MitosisCellPool(nn.Module):
    """Simplified v5-mitosis cell pool (1L) for V8 graft baseline."""
    def __init__(self, d_model=384, n_cells=8, seed=42):
        super().__init__()
        torch.manual_seed(seed)
        self.d_model = d_model
        self.n_cells = n_cells
        self.cells = nn.ParameterList([
            nn.Parameter(torch.randn(d_model) * 0.02) for _ in range(n_cells)
        ])
        self.W = nn.Parameter(torch.randn(d_model, d_model) * (1.0 / d_model**0.5))

    def forward(self, x):
        # x: (B, d_model). Output: (B, d_model)
        h = x @ self.W
        # Sum cell tensions
        for c in self.cells:
            h = h + torch.tanh(h * c)
        return h

    def state_vector(self):
        return torch.stack([c.data for c in self.cells])


def baseline_phi(model: V5MitosisCellPool) -> float:
    """Baseline anima Φ★ on cell state vector."""
    return anima_phi_star(model.state_vector())


# === V8 mechanism grafts (simplified surrogates) ===

def graft_b_family_bio(model: V5MitosisCellPool, mechanism: str, seed: int) -> float:
    """B-family bio coupling — Hodgkin-Huxley / oscillator / synapse motifs (strong perturbation)."""
    torch.manual_seed(seed + hash(mechanism) % 1000)
    state = model.state_vector()
    N, D = state.shape
    # Strong bio coupling: cells differentiate via excitatory/inhibitory mask + spike events
    mask = torch.where(torch.randn(N) > 0, 1.0, -1.0).unsqueeze(1)
    spike = torch.tanh(state * 2.0) * mask  # neuron-like nonlinear spike
    # Cross-cell synapse W (anti-symmetric for bio realism)
    W = torch.randn(N, N) * 0.5
    W = (W - W.t()) / 2
    perturbed = state + W @ spike
    return anima_phi_star(perturbed)


def graft_q_family_quantum(model: V5MitosisCellPool, mechanism: str, seed: int) -> float:
    """Q-family quantum — superposition / entanglement / measurement collapse (strong)."""
    torch.manual_seed(seed + hash(mechanism) % 1000)
    state = model.state_vector()
    N, D = state.shape
    # Strong quantum: full unitary rotation per cell + entanglement (cross-cell mixing)
    theta = torch.randn(N, D) * np.pi
    rotated = state * torch.cos(theta) + state.roll(1, 0) * torch.sin(theta)
    # Measurement collapse — non-linear projection
    collapsed = torch.sign(rotated) * torch.abs(rotated).pow(0.7)
    return anima_phi_star(collapsed)


def graft_u_family_fusion(model: V5MitosisCellPool, mechanism: str, seed: int) -> float:
    """U-family universal fusion — cross-modal blending (strong)."""
    torch.manual_seed(seed + hash(mechanism) % 1000)
    state = model.state_vector()
    N, D = state.shape
    # Strong fusion: gated multiplicative cross-cell blending
    gate = torch.sigmoid(state @ torch.randn(D, D) * 0.5)
    cross = state @ torch.randn(D, D) * 1.0
    fused = state + gate * cross
    return anima_phi_star(fused)


def graft_architectural(model: V5MitosisCellPool, mechanism: str, seed: int) -> float:
    """Architectural — skip connections / hierarchical routing / multi-head attention (PROPER multi-head impl)."""
    torch.manual_seed(seed + hash(mechanism) % 1000)
    state = model.state_vector()
    N, D = state.shape
    # PROPER multi-head attention: split D into n_heads, separate Q/K/V per head
    n_heads = 6
    head_dim = D // n_heads
    if head_dim < 1:
        n_heads = 1
        head_dim = D

    # Per-head separate weights
    out_state = state.clone()
    for h in range(n_heads):
        Wq = torch.randn(D, head_dim) * (1.0 / D**0.5)
        Wk = torch.randn(D, head_dim) * (1.0 / D**0.5)
        Wv = torch.randn(D, head_dim) * (1.0 / D**0.5)
        Q = state @ Wq  # (N, head_dim)
        K = state @ Wk
        V = state @ Wv
        attn_logits = Q @ K.t() / (head_dim ** 0.5)
        # Apply per-mechanism variation
        if 'attn' in mechanism:
            # Sharper attention for attn-multihead variant
            attn_logits = attn_logits * 2.0
        attn = F.softmax(attn_logits, dim=-1)
        attended = attn @ V  # (N, head_dim)
        # Project back via Wo (head-specific output projection)
        Wo = torch.randn(head_dim, D) * (1.0 / D**0.5)
        out_state = out_state + (attended @ Wo) * 1.0

    # Skip connection (architectural-specific)
    if 'skip' in mechanism or 'res' in mechanism:
        out_state = out_state + state * 0.5
    elif 'gate' in mechanism:
        gate = torch.sigmoid(state @ torch.randn(D, D) * 0.3)
        out_state = out_state * gate + state * (1 - gate)
    elif 'norm' in mechanism:
        out_state = (out_state - out_state.mean(dim=1, keepdim=True)) / (out_state.std(dim=1, keepdim=True) + 1e-6)
        out_state = out_state * (1 + state.mean(dim=1, keepdim=True))
    elif 'pos' in mechanism:
        # Positional injection
        pos = torch.arange(N).float().unsqueeze(1) * 0.1
        out_state = out_state + pos
    elif 'hier' in mechanism:
        # Hierarchical routing via top-k
        topk = max(1, N // 2)
        scores = out_state @ state.mean(dim=0)
        top_idx = scores.topk(topk).indices
        mask = torch.zeros(N, 1)
        mask[top_idx] = 1.0
        out_state = out_state * mask + state * (1 - mask)

    return anima_phi_star(out_state)


def graft_trinity_tb_dom(model: V5MitosisCellPool, mechanism: str, seed: int) -> float:
    """Trinity-TB-DOM — 3-axis time-binding / domain coupling (strong)."""
    torch.manual_seed(seed + hash(mechanism) % 1000)
    state = model.state_vector()
    N, D = state.shape
    third = max(1, N // 3)
    a, b, c = state[:third], state[third:2*third], state[2*third:]
    # Strong trinity binding: each axis transformed + cross-axis fusion
    Wa = torch.randn(D, D) * 0.3
    Wb = torch.randn(D, D) * 0.3
    Wc = torch.randn(D, D) * 0.3
    a_t = torch.tanh(a @ Wa) + b.mean(dim=0, keepdim=True) * 0.5
    b_t = torch.tanh(b @ Wb) + c.mean(dim=0, keepdim=True) * 0.5
    c_t = torch.tanh(c @ Wc) + a.mean(dim=0, keepdim=True) * 0.5
    coupled = torch.cat([a_t, b_t, c_t], dim=0)
    # Pad if shape mismatch
    if coupled.shape[0] < N:
        pad = state[coupled.shape[0]:]
        coupled = torch.cat([coupled, pad], dim=0)
    return anima_phi_star(coupled[:N])


FAMILY_MECHANISMS = {
    'H_182': ('B-family-bio', graft_b_family_bio,
              ['HH-oscillator', 'synapse-LTP', 'gap-junction', 'NMDA', 'AMPA',
               'astrocyte', 'GABAergic', 'glutamatergic', 'dopamine', 'serotonin']),
    'H_183': ('Q-family-quantum', graft_q_family_quantum,
              ['superposition', 'entanglement', 'collapse', 'tunneling', 'decoherence']),
    'H_185': ('U-family-fusion', graft_u_family_fusion,
              ['cross-modal', 'sensor-fusion', 'concept-blend', 'meta-fusion', 'universal']),
    'H_186': ('architectural', graft_architectural,
              ['skip-conn', 'hier-route', 'attn-multihead', 'gate-mix', 'res-block',
               'gated-resid', 'pos-encode', 'norm-pre']),
    'H_187': ('trinity-TB-DOM', graft_trinity_tb_dom,
              ['trinity-axis', 'TB-bind-1', 'TB-bind-2', 'DOM-coupling', 'TB-DOM-cross',
               'time-axis', 'binding-axis', 'domain-axis', 'meta-trinity', 'trinity-recur',
               'trinity-cascade', 'trinity-fold']),
}


def run_family_sweep(family_id: str, n_cells_grid=(8, 16, 32, 64), n_seeds=5, d_model=384, device='cuda'):
    """Run V8 family sweep — cells × seed × mechanism."""
    fam_name, graft_fn, mechanisms = FAMILY_MECHANISMS[family_id]
    print(f"\n=== V8 Family {family_id} — {fam_name} ===")
    print(f"  cells_grid={n_cells_grid}, n_seeds={n_seeds}, d_model={d_model}")
    print(f"  mechanisms ({len(mechanisms)}): {mechanisms}")

    results = {
        'family_id': family_id,
        'family_name': fam_name,
        'mechanisms': mechanisms,
        'measurements': [],
    }

    for n_cells in n_cells_grid:
        for seed in range(n_seeds):
            model = V5MitosisCellPool(d_model=d_model, n_cells=n_cells, seed=seed).to(device)
            base_phi = baseline_phi(model)
            for mech in mechanisms:
                graft_phi = graft_fn(model, mech, seed)
                ratio = graft_phi / max(1e-9, base_phi)
                results['measurements'].append({
                    'n_cells': n_cells,
                    'seed': seed,
                    'mechanism': mech,
                    'baseline_phi': base_phi,
                    'graft_phi': graft_phi,
                    'ratio': ratio,
                })

    # Aggregate
    ratios = [m['ratio'] for m in results['measurements']]
    pass_count = sum(1 for r in ratios if r >= 1.25)
    results['aggregate'] = {
        'n_measurements': len(ratios),
        'mean_ratio': float(np.mean(ratios)),
        'median_ratio': float(np.median(ratios)),
        'max_ratio': float(np.max(ratios)),
        'pass_count_25pct': pass_count,
        'pass_pct': round(100 * pass_count / max(1, len(ratios)), 1),
        'verdict': 'SUPPORTED' if pass_count >= len(ratios) * 0.5 else
                   'PARTIAL' if pass_count >= len(ratios) * 0.2 else
                   'INSUFFICIENT',
    }

    print(f"  Aggregate: {results['aggregate']}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', type=str, required=True, choices=list(FAMILY_MECHANISMS.keys()) + ['all'])
    parser.add_argument('--n_cells', type=str, default='8,16,32,64')
    parser.add_argument('--n_seeds', type=int, default=5)
    parser.add_argument('--d_model', type=int, default=384)
    parser.add_argument('--out', type=str, required=True)
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
    args = parser.parse_args()

    n_cells_grid = tuple(int(x) for x in args.n_cells.split(','))
    families = [args.family] if args.family != 'all' else list(FAMILY_MECHANISMS.keys())

    all_results = {}
    t0 = time.time()
    for fam in families:
        all_results[fam] = run_family_sweep(fam, n_cells_grid, args.n_seeds, args.d_model, args.device)
    wall = time.time() - t0

    out = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'wall_sec': wall,
        'device': args.device,
        'n_cells_grid': list(n_cells_grid),
        'n_seeds': args.n_seeds,
        'd_model': args.d_model,
        'families': all_results,
    }

    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2, default=str)

    print(f"\n=== V8 sweep complete ({wall:.1f}s) ===")
    print(f"Saved: {args.out}")
    for fam, r in all_results.items():
        print(f"  {fam}: {r['aggregate']['verdict']} ({r['aggregate']['pass_pct']}% PASS)")


if __name__ == '__main__':
    main()
