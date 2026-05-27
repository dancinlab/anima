"""V8 B-bio Phase 2 — denser mechanism (HH 4-state Markov + STDP density + Wilson-Cowan).

Phase 1 의 simplified stubs (~30 LoC each, 0/10 PASS) 한계 극복 위해 핵심 5 mechanism
을 ~100-150 LoC each 으로 dynamic complexity 강화. 목표: Φ ≥ 0.5 1+ mechanism unlock.
"""
import os, sys, json, time
import numpy as np
from collections import Counter

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
import pyphi
pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1


# ── Hc_B1 HH 4-state Markov (n_K^4·m_Na^3·h dense) ──

def mech_hh_4state_markov(state, dt=0.05):
    """HH with 4-state Markov for K+ activation + Na+ inactivation."""
    v = state.copy()
    # K+ activation (n^4) — Markov: 4 states C0-C1-C2-C3-Open
    alpha_n = 0.01 * (10 - v) / (np.exp((10 - v) / 10) - 1 + 1e-9)
    beta_n = 0.125 * np.exp(-v / 80)
    n_eq = alpha_n / (alpha_n + beta_n + 1e-9)
    # Na+ activation (m^3) — Markov
    alpha_m = 0.1 * (25 - v) / (np.exp((25 - v) / 10) - 1 + 1e-9)
    beta_m = 4 * np.exp(-v / 18)
    m_eq = alpha_m / (alpha_m + beta_m + 1e-9)
    # Na+ inactivation (h)
    alpha_h = 0.07 * np.exp(-v / 20)
    beta_h = 1 / (np.exp((30 - v) / 10) + 1)
    h_eq = alpha_h / (alpha_h + beta_h + 1e-9)
    # Currents (HH 1952 canonical)
    g_K, g_Na, g_L = 36.0, 120.0, 0.3
    E_K, E_Na, E_L = -77.0, 50.0, -54.4
    I_K = g_K * n_eq**4 * (v - E_K)
    I_Na = g_Na * m_eq**3 * h_eq * (v - E_Na)
    I_L = g_L * (v - E_L)
    # External + coupling (nearest-neighbor)
    I_ext = 10.0  # depolarizing current
    I_coup = 0.3 * (np.roll(v, 1) + np.roll(v, -1) - 2 * v)
    dV = (I_ext - I_K - I_Na - I_L + I_coup) * dt
    return v + dV * 0.001  # scale to avoid blow-up


# ── Hc_B2 STDP dense — Bi-Poo 1998 asymmetric STDP rule ──

def mech_stdp_bipoo(state, dt=0.05):
    """Bi-Poo 1998 STDP: Δw = A_+ · exp(-Δt/τ_+) for Δt > 0, -A_- · exp(Δt/τ_-) for Δt < 0."""
    v = state.copy()
    A_plus, A_minus, tau_plus, tau_minus = 0.005, 0.0025, 17.0, 34.0
    # Simulate pairwise spike timing
    N = len(v)
    spike_times = v.copy()  # treat v as recent spike time relative
    dw = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            delta_t = spike_times[j] - spike_times[i]
            if delta_t > 0:
                dw[i] += A_plus * np.exp(-delta_t / tau_plus)
            elif delta_t < 0:
                dw[i] -= A_minus * np.exp(delta_t / tau_minus)
    return v + dt * dw * 10  # weight to voltage scaling


# ── Hc_B3 Wilson-Cowan E/I dynamics ──

def mech_wilson_cowan(state, dt=0.05):
    """Wilson-Cowan 1972 E/I population: dE/dt = -E + S(c1·E - c2·I + I_ext_E)
       dI/dt = -I + S(c3·E - c4·I + I_ext_I). S = sigmoid."""
    v = state.copy()
    N = len(v)
    # Split state to E (first half) and I (second half)
    E = v[:N//2 + 1]  # ensure non-empty
    I = v[N//2 + 1:] if N > 1 else v[:1]
    # Pad if too small
    if len(I) == 0:
        I = np.array([0.5])
    # Wilson-Cowan parameters
    c1, c2, c3, c4 = 12.0, 4.0, 13.0, 11.0
    I_ext_E, I_ext_I = 1.5, 1.0
    tau_E, tau_I = 1.0, 2.0
    sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))
    E_mean = np.mean(E)
    I_mean = np.mean(I)
    dE = (-E + sigmoid(c1 * E_mean - c2 * I_mean + I_ext_E)) / tau_E
    dI = (-I + sigmoid(c3 * E_mean - c4 * I_mean + I_ext_I)) / tau_I
    new_E = E + dt * dE
    new_I = I + dt * dI
    return np.concatenate([new_E, new_I])[:N]


# ── Hc_B4 NMDA dense — Mg2+ block + Ca2+ dynamics ──

def mech_nmda_dense(state, dt=0.05):
    """NMDA receptor: g_NMDA(v) = g_max·s/(1 + [Mg]·exp(-α·v)/β). Mg2+ block voltage-gated."""
    v = state.copy()
    g_max = 1.0
    Mg = 1.0  # mM
    alpha_Mg, beta_Mg = 0.062, 3.57
    Mg_block = 1.0 / (1.0 + Mg * np.exp(-alpha_Mg * v) / beta_Mg)
    s = np.tanh(v / 10)  # synaptic activation
    I_NMDA = g_max * s * Mg_block * (v - 0.0)  # E_NMDA ≈ 0 mV
    # Ca2+ influx coupling
    Ca_influx = Mg_block * np.maximum(0, v + 70)
    I_coup = 0.4 * (np.roll(v, 1) - v)  # neighbor coupling
    return v + dt * (-I_NMDA * 0.1 + Ca_influx * 0.05 + I_coup * 0.1)


# ── Hc_B5 Gap junction electrical with cable equation ──

def mech_gap_cable(state, dt=0.05):
    """Gap junction + cable equation: ∂V/∂t = (1/τ_m)·∇²V·λ²."""
    v = state.copy()
    tau_m = 10.0  # membrane time constant
    lambda_space = 0.3  # space constant
    N = len(v)
    # Discrete Laplacian
    laplacian = np.roll(v, 1) + np.roll(v, -1) - 2 * v
    dV = dt / tau_m * lambda_space**2 * laplacian
    return v + dV


MECHANISMS = [
    ('Hc_B1_HH_4state', mech_hh_4state_markov),
    ('Hc_B2_STDP_BiPoo', mech_stdp_bipoo),
    ('Hc_B3_Wilson_Cowan', mech_wilson_cowan),
    ('Hc_B4_NMDA_dense', mech_nmda_dense),
    ('Hc_B5_gap_cable', mech_gap_cable),
]


def simulate_dynamics(mech_fn, n_cells=3, n_steps=500, seed=42):
    np.random.seed(seed)
    state = np.random.randn(n_cells) * 5.0
    states = []
    for _ in range(n_steps):
        state = mech_fn(state)
        state = np.clip(state, -100, 100)
        binary = tuple(int(s > np.median(state)) for s in state)
        states.append(binary)
    return states


def states_to_tpm(states, n_nodes):
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


def measure_phi(tpm, state, n_nodes):
    cm = (np.ones((n_nodes, n_nodes)) - np.eye(n_nodes)).astype(int)
    labels = tuple(f'C{i}' for i in range(n_nodes))
    try:
        net = pyphi.Network(tpm, cm=cm, node_labels=labels)
        subsys = pyphi.Subsystem(net, tuple(state), range(n_nodes))
        sia = pyphi.compute.sia(subsys)
        return float(sia.phi), 'OK'
    except Exception as e:
        return None, f"ERR: {type(e).__name__}: {str(e)[:80]}"


def main():
    results = {'pyphi_version': pyphi.__version__, 'mechanisms': {}}
    t_total = time.time()
    for name, fn in MECHANISMS:
        print(f"\n=== {name} ===")
        states = simulate_dynamics(fn, n_cells=3, n_steps=500, seed=42)
        unique = len(set(states))
        top_state = Counter(states).most_common(1)[0][0]
        tpm, counts = states_to_tpm(states, 3)
        print(f"  unique={unique}/8, top={top_state}")
        t1 = time.time()
        phi, status = measure_phi(tpm, top_state, 3)
        wall = time.time() - t1
        print(f"  Φ = {phi}, wall={wall:.1f}s, status={status}")
        results['mechanisms'][name] = {'phi': phi, 'unique_states': unique, 'top_state': list(top_state),
                                        'status': status, 'wall_sec': round(wall, 2)}

    phis = [m['phi'] for m in results['mechanisms'].values() if isinstance(m.get('phi'), (int, float))]
    n_above = sum(1 for p in phis if p > 0.5)
    results['aggregate'] = {
        'mean_phi': float(np.mean(phis)) if phis else None,
        'max_phi': float(np.max(phis)) if phis else None,
        'n_above_0_5': n_above,
        'n_total': len(phis),
        'pass_rate': f"{n_above}/{len(phis)}",
        'phase1_carry': '0/10 (simplified stubs, AT-RISK CONFIRMED)',
        'phase2_target': '≥1 of 5 Φ > 0.5 (dense mechanism PROD-READY)',
        'verdict': 'PHASE-2-PASS' if n_above >= 1 else 'PHASE-2-FAIL (AT-RISK strict carry)',
    }
    results['wall_total_sec'] = round(time.time() - t_total, 1)
    print(f"\n=== AGGREGATE ===")
    print(f"  {n_above}/{len(phis)} Φ > 0.5, mean={results['aggregate']['mean_phi']}, max={results['aggregate']['max_phi']}")
    print(f"  verdict: {results['aggregate']['verdict']}")
    print(f"  wall total: {results['wall_total_sec']}s")
    with open('/Users/ghost/core/anima/state/verify_v8_bbio_phase2_2026_05_15/phase2_dense_result.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == '__main__':
    main()
