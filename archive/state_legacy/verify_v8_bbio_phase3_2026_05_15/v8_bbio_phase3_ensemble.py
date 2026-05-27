"""V8 B-bio Phase 3 — ensemble TPM + noise/stochasticity 강화.

Phase 1/2 의 attractor collapse (unique 1-2/8) 해결 위해:
1. 각 mechanism 에 noise term 추가 (stochastic dynamics)
2. n_cells = 3 → 4 (state space 8 → 16)
3. multi-seed ensemble TPM (10 seed 의 TPM 평균)
4. random initial condition variation 강화
"""
import os, sys, json, time
import numpy as np
from collections import Counter

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
import pyphi
pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1


# 5 dense mechanism (Phase 2 carry) + noise term

def mech_hh_4state_markov_noisy(state, dt=0.05, noise=0.5):
    v = state.copy()
    alpha_n = 0.01 * (10 - v) / (np.exp((10 - v) / 10) - 1 + 1e-9)
    beta_n = 0.125 * np.exp(-v / 80)
    n_eq = alpha_n / (alpha_n + beta_n + 1e-9)
    alpha_m = 0.1 * (25 - v) / (np.exp((25 - v) / 10) - 1 + 1e-9)
    beta_m = 4 * np.exp(-v / 18)
    m_eq = alpha_m / (alpha_m + beta_m + 1e-9)
    alpha_h = 0.07 * np.exp(-v / 20)
    beta_h = 1 / (np.exp((30 - v) / 10) + 1)
    h_eq = alpha_h / (alpha_h + beta_h + 1e-9)
    g_K, g_Na, g_L = 36.0, 120.0, 0.3
    E_K, E_Na, E_L = -77.0, 50.0, -54.4
    I_K = g_K * n_eq**4 * (v - E_K)
    I_Na = g_Na * m_eq**3 * h_eq * (v - E_Na)
    I_L = g_L * (v - E_L)
    I_ext = 10.0 + noise * np.random.randn(*v.shape)  # noisy current
    I_coup = 0.3 * (np.roll(v, 1) + np.roll(v, -1) - 2 * v)
    dV = (I_ext - I_K - I_Na - I_L + I_coup) * dt
    return v + dV * 0.001


def mech_wilson_cowan_noisy(state, dt=0.05, noise=0.3):
    v = state.copy()
    N = len(v)
    E = v[:N//2 + 1] if N > 1 else v[:1]
    I = v[N//2 + 1:] if N > 1 else v[:1]
    if len(I) == 0:
        I = np.array([0.5])
    c1, c2, c3, c4 = 12.0, 4.0, 13.0, 11.0
    I_ext_E = 1.5 + noise * np.random.randn()
    I_ext_I = 1.0 + noise * np.random.randn()
    tau_E, tau_I = 1.0, 2.0
    sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))
    E_mean = np.mean(E)
    I_mean = np.mean(I)
    dE = (-E + sigmoid(c1 * E_mean - c2 * I_mean + I_ext_E)) / tau_E
    dI = (-I + sigmoid(c3 * E_mean - c4 * I_mean + I_ext_I)) / tau_I
    new_E = E + dt * dE
    new_I = I + dt * dI
    return np.concatenate([new_E, new_I])[:N]


def mech_kuramoto_noisy(state, dt=0.05, noise=0.5):
    """Kuramoto: dθ_i/dt = ω_i + K·Σ sin(θ_j - θ_i) + ξ(t)."""
    theta = state.copy()
    N = len(theta)
    K = 1.6  # near critical K_c
    omega = np.random.randn(N) * 0.5  # natural frequencies
    interaction = np.zeros(N)
    for i in range(N):
        for j in range(N):
            interaction[i] += np.sin(theta[j] - theta[i])
    interaction = interaction * K / N
    xi = noise * np.random.randn(N)
    return theta + dt * (omega + interaction + xi)


def mech_lorenz_noisy(state, dt=0.05, noise=0.5):
    """Lorenz attractor — chaotic dynamics, high ergodicity."""
    if len(state) < 3:
        state = np.concatenate([state, np.zeros(3 - len(state))])[:3]
    x, y, z = state[0], state[1], state[2] if len(state) > 2 else 0
    sigma, rho, beta = 10.0, 28.0, 8/3
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    noise_term = noise * np.random.randn(3) * 0.3
    new_state = state.copy()
    new_state[0] = x + dt * dx + noise_term[0]
    new_state[1] = y + dt * dy + noise_term[1]
    if len(state) > 2:
        new_state[2] = z + dt * dz + noise_term[2]
    return new_state * 0.05  # scale to mV-like


def mech_random_walk(state, dt=0.05, noise=1.0):
    """Random walk baseline — fully stochastic, max ergodicity."""
    return state + noise * np.random.randn(*state.shape) * 0.5


MECHANISMS_NOISY = [
    ('Hc_B1_HH_4state_noisy', mech_hh_4state_markov_noisy),
    ('Hc_B3_Wilson_Cowan_noisy', mech_wilson_cowan_noisy),
    ('Hc_NEW_Kuramoto_noisy', mech_kuramoto_noisy),
    ('Hc_NEW_Lorenz_noisy', mech_lorenz_noisy),
    ('Hc_NEW_RandomWalk', mech_random_walk),
]


def simulate_with_seed(mech_fn, n_cells=4, n_steps=300, seed=42):
    np.random.seed(seed)
    state = np.random.randn(n_cells) * 5.0
    states = []
    for _ in range(n_steps):
        state = mech_fn(state)
        state = np.clip(state, -100, 100)
        binary = tuple(int(s > np.median(state)) for s in state)
        states.append(binary)
    return states


def ensemble_tpm(mech_fn, n_cells=4, n_steps=300, n_seeds=10):
    """Multi-seed ensemble TPM — sum transition counts across seeds."""
    num_states = 2**n_cells
    transition_counts = np.zeros((num_states, num_states))
    all_states = []
    for seed in range(n_seeds):
        states = simulate_with_seed(mech_fn, n_cells, n_steps, seed=42 + seed)
        for i in range(len(states) - 1):
            s_idx = sum(b << k for k, b in enumerate(states[i]))
            n_idx = sum(b << k for k, b in enumerate(states[i+1]))
            transition_counts[s_idx, n_idx] += 1
        all_states.extend(states)

    tpm = np.zeros((num_states, n_cells))
    for s_idx in range(num_states):
        row_total = transition_counts[s_idx].sum()
        if row_total == 0:
            for i in range(n_cells):
                tpm[s_idx, i] = (s_idx >> i) & 1
            continue
        for i in range(n_cells):
            count_one = sum(transition_counts[s_idx, n_idx]
                            for n_idx in range(num_states)
                            if (n_idx >> i) & 1)
            tpm[s_idx, i] = count_one / row_total
    return tpm, transition_counts, all_states


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
    results = {'pyphi_version': pyphi.__version__, 'mechanisms': {}, 'config': {
        'n_cells': 4, 'n_steps': 300, 'n_seeds_ensemble': 10
    }}
    t_total = time.time()
    for name, fn in MECHANISMS_NOISY:
        print(f"\n=== {name} ===")
        tpm, counts, all_states = ensemble_tpm(fn, n_cells=4, n_steps=300, n_seeds=10)
        unique = len(set(all_states))
        top_state = Counter(all_states).most_common(1)[0][0]
        print(f"  ensemble unique={unique}/16 (10 seed × 300 step = 3000 transitions per seed)")
        print(f"  top state: {top_state}")
        t1 = time.time()
        phi, status = measure_phi(tpm, top_state, 4)
        wall = time.time() - t1
        print(f"  Φ = {phi}, wall_phi={wall:.1f}s, status={status}")
        results['mechanisms'][name] = {'phi': phi, 'unique_states': unique,
                                        'top_state': list(top_state), 'status': status,
                                        'wall_sec': round(wall, 2)}

    phis = [m['phi'] for m in results['mechanisms'].values() if isinstance(m.get('phi'), (int, float))]
    n_above = sum(1 for p in phis if p > 0.5)
    results['aggregate'] = {
        'mean_phi': float(np.mean(phis)) if phis else None,
        'max_phi': float(np.max(phis)) if phis else None,
        'n_above_0_5': n_above,
        'n_total': len(phis),
        'phase1_carry': '0/10',
        'phase2_carry': '0/5',
        'phase3_target': '≥1/5 unlock (state-space ergodicity issue 검증)',
        'verdict': 'PHASE-3-PASS' if n_above >= 1 else 'PHASE-3-FAIL (AT-RISK fundamental confirmed)',
    }
    results['wall_total_sec'] = round(time.time() - t_total, 1)
    print(f"\n=== AGGREGATE ===")
    print(f"  {n_above}/{len(phis)} Φ > 0.5, mean={results['aggregate']['mean_phi']}, max={results['aggregate']['max_phi']}")
    print(f"  verdict: {results['aggregate']['verdict']}")
    print(f"  wall total: {results['wall_total_sec']}s")
    with open('/Users/ghost/core/anima/state/verify_v8_bbio_phase3_2026_05_15/phase3_ensemble_result.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == '__main__':
    main()
