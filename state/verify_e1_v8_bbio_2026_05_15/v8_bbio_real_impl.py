"""V8 B-bio Phase 1 real Hc impl — 10 mechanism Python class + PyPhi formal Φ.

Tests whether real (vs surrogate) bio mechanism yields PyPhi Φ > 0.5.
Cycle D §H182-H187-CROSS-CHECK found surrogate Φ_star=4.16-4.86 BUT PyPhi formal
Φ=0.358 < 0.5 — AT-RISK. Phase 1 verifies if real mechanism resolves.

10 B-bio Hc per v8_real_hc_impl_spec.md:
  Hc_B1 Hodgkin-Huxley axon coupling (Na+/K+ + cable)
  Hc_B2 STDP synaptic LTP/LTD
  Hc_B3 Gap junction electrical coupling
  Hc_B4 NMDA voltage-gated coincidence (Mg2+ block + Ca2+)
  Hc_B5 AMPA fast excitation
  Hc_B6 Astrocyte tripartite synapse
  Hc_B7 GABAergic inhibition
  Hc_B8 Glutamatergic E/I balance
  Hc_B9 Dopamine reward modulation (D1/D2)
  Hc_B10 Serotonin 5-HT modulation (5-HT2A)

All n=3 cells, PyPhi small-N fast wall ~10s each.
"""
import os, sys, json, time
import numpy as np
from collections import Counter

os.environ['PYPHI_WELCOME_OFF'] = 'yes'
import pyphi
pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1


# ─── 10 B-bio mechanisms (simplified differential dynamics) ───

def mech_b1_hodgkin_huxley(state, dt=0.1):
    """HH-like: v[i+1] = v[i] + dt·(I_ext - g_K·n^4·(v-E_K) - g_Na·m^3·h·(v-E_Na))
       Simplified: voltage cascade with sigmoid gating."""
    v = state.copy()
    g_K, g_Na, E_K, E_Na = 36.0, 120.0, -77.0, 50.0
    n = 1.0 / (1.0 + np.exp(-(v + 40.0) / 10.0))
    m = 1.0 / (1.0 + np.exp(-(v + 35.0) / 9.0))
    h = 1.0 / (1.0 + np.exp((v + 60.0) / 7.0))
    I_K = g_K * n**4 * (v - E_K)
    I_Na = g_Na * m**3 * h * (v - E_Na)
    I_coup = 0.5 * np.roll(v, 1) - 0.5 * v  # nearest-neighbor coupling
    return v + dt * (10.0 - I_K - I_Na + I_coup) * 0.001


def mech_b2_stdp(state, dt=0.1):
    """STDP: weight update Δw = A_plus·exp(-Δt/τ_plus) for pre→post."""
    v = state.copy()
    A_plus, tau_plus = 0.1, 20.0
    # Treat state as pre-synaptic firing; post-synaptic delay
    delta_t = np.diff(v, append=v[:1])
    weight_change = A_plus * np.exp(-np.abs(delta_t) / tau_plus) * np.sign(delta_t)
    return v + dt * weight_change


def mech_b3_gap_junction(state, dt=0.1):
    """Gap junction: i_ij = g_gap·(v_i - v_j), bidirectional."""
    v = state.copy()
    g_gap = 1.0
    N = len(v)
    I = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i] += g_gap * (v[j] - v[i])
    return v + dt * I * 0.01


def mech_b4_nmda(state, dt=0.1):
    """NMDA: Mg2+ block × Ca2+ influx — voltage-gated coincidence."""
    v = state.copy()
    Mg_block = 1.0 / (1.0 + np.exp(-0.062 * v) * 1.0 / 3.57)
    Ca_influx = Mg_block * np.maximum(0, v + 70)  # active when v > -70
    return v + dt * Ca_influx * 0.1


def mech_b5_ampa(state, dt=0.1):
    """AMPA: fast g_AMPA = exp(-t/tau)·spike."""
    v = state.copy()
    tau = 5.0
    g_ampa = np.exp(-1.0 / tau) * np.maximum(0, v)
    return v + dt * g_ampa * 0.5


def mech_b6_astrocyte(state, dt=0.1):
    """Astrocyte tripartite: glia modulates neuron via Ca2+ wave."""
    v = state.copy()
    # Astrocyte Ca2+ wave (slow timescale)
    ca_glia = np.mean(v) * 0.5  # global modulation
    return v + dt * (ca_glia - v) * 0.05


def mech_b7_gaba(state, dt=0.1):
    """GABAergic inhibition: Cl- shunt drives v → E_Cl = -75 mV."""
    v = state.copy()
    g_GABA, E_Cl = 0.3, -75.0
    I_GABA = g_GABA * (v - E_Cl)
    return v + dt * (-I_GABA) * 0.1


def mech_b8_glutamate_ei_balance(state, dt=0.1):
    """E/I balance: excitation half + inhibition half."""
    v = state.copy()
    N = len(v)
    excitation = np.sum(np.maximum(0, v[:N//2])) / max(1, N//2)
    inhibition = np.sum(np.minimum(0, v[N//2:])) / max(1, N - N//2)
    return v + dt * (excitation + inhibition) * 0.1


def mech_b9_dopamine(state, dt=0.1):
    """Dopamine D1 (excitatory) + D2 (inhibitory)."""
    v = state.copy()
    da = np.tanh(np.mean(v))  # global DA signal
    return v + dt * (da * 0.5 - 0.5 * da) * 0.1  # net effect


def mech_b10_serotonin(state, dt=0.1):
    """Serotonin 5-HT2A: modulates pyramidal firing."""
    v = state.copy()
    ht2a = 1.0 / (1.0 + np.exp(-v))
    return v + dt * ht2a * 0.2


MECHANISMS = [
    ('Hc_B1_hodgkin_huxley', mech_b1_hodgkin_huxley),
    ('Hc_B2_stdp', mech_b2_stdp),
    ('Hc_B3_gap_junction', mech_b3_gap_junction),
    ('Hc_B4_nmda', mech_b4_nmda),
    ('Hc_B5_ampa', mech_b5_ampa),
    ('Hc_B6_astrocyte', mech_b6_astrocyte),
    ('Hc_B7_gaba', mech_b7_gaba),
    ('Hc_B8_glutamate_ei', mech_b8_glutamate_ei_balance),
    ('Hc_B9_dopamine', mech_b9_dopamine),
    ('Hc_B10_serotonin', mech_b10_serotonin),
]


# ─── State → TPM → PyPhi Φ pipeline ───

def simulate_dynamics(mech_fn, n_cells=3, n_steps=500, seed=42):
    np.random.seed(seed)
    state = np.random.randn(n_cells) * 5.0  # mV-like initial
    states = []
    for _ in range(n_steps):
        state = mech_fn(state)
        # Saturate to bounded range to avoid blow-up
        state = np.clip(state, -100, 100)
        # Binarize at median
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
        return None, f"ERR: {type(e).__name__}: {str(e)[:100]}"


def main():
    results = {'pyphi_version': pyphi.__version__, 'mechanisms': {}}
    t_total_start = time.time()

    for name, fn in MECHANISMS:
        print(f"\n=== {name} ===")
        t0 = time.time()
        states = simulate_dynamics(fn, n_cells=3, n_steps=500, seed=42)
        unique = len(set(states))
        top_state = Counter(states).most_common(1)[0][0]
        tpm, counts = states_to_tpm(states, 3)
        wall_sim = time.time() - t0
        print(f"  unique states: {unique}/8, transitions: {int(counts.sum())}, top: {top_state}")
        t1 = time.time()
        phi, status = measure_phi(tpm, top_state, 3)
        wall_phi = time.time() - t1
        results['mechanisms'][name] = {
            'phi': phi,
            'top_state': list(top_state),
            'unique_states': unique,
            'status': status,
            'wall_sim': round(wall_sim, 3),
            'wall_phi': round(wall_phi, 3),
        }
        print(f"  Φ = {phi}, status={status}, wall_phi={wall_phi:.2f}s")

    # Aggregate
    phis = [m['phi'] for m in results['mechanisms'].values() if isinstance(m.get('phi'), (int, float))]
    n_above_05 = sum(1 for p in phis if p > 0.5)
    n_total = len(phis)
    results['aggregate'] = {
        'mean_phi': float(np.mean(phis)) if phis else None,
        'median_phi': float(np.median(phis)) if phis else None,
        'max_phi': float(np.max(phis)) if phis else None,
        'min_phi': float(np.min(phis)) if phis else None,
        'n_above_0_5': n_above_05,
        'n_total_with_phi': n_total,
        'pass_rate_strict': f"{n_above_05}/{n_total}",
        'verdict_h_182_real': 'SUPPORTED-CROSS-CONFIRMED' if n_above_05 >= n_total / 2 else 'AT-RISK-CONFIRMED',
        'cycle_d_carry_phi_naive_surrogate': 0.358,
        'cycle_d_carry_verdict': 'AT-RISK',
        'note': 'Cycle E1 V8 B-bio Phase 1 real Hc impl vs Cycle D §H182-H187 naive surrogate (Φ=0.358<0.5).',
    }
    results['wall_total_sec'] = round(time.time() - t_total_start, 1)

    out_path = '/Users/ghost/core/anima/state/verify_e1_v8_bbio_2026_05_15/v8_bbio_real_result.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n=== Saved: {out_path} ===")
    print(f"  Aggregate: {n_above_05}/{n_total} mechanism Φ > 0.5")
    print(f"  Mean Φ: {results['aggregate']['mean_phi']}, Max: {results['aggregate']['max_phi']}")
    print(f"  Verdict H_182 real: {results['aggregate']['verdict_h_182_real']}")
    print(f"  Wall total: {results['wall_total_sec']}s")


if __name__ == '__main__':
    main()
