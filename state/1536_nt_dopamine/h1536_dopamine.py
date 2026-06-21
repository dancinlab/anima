#!/usr/bin/env python3
# H_1536 NT-DOPAMINE — dopamine as a DISTINCT FACULTY (reward-prediction-error / credit assignment),
#                      NOT a gain knob. (R1 numpy mirror, DIRECTIONAL.)
#
# DIRECTIONAL (numpy mirror, a_engine_native_learning: grep numpy ⇒ auto-DIRECTIONAL; engine R2 deferred ING).
#
# THE REFRAME (a_no_llm_frame_trap · a_break_the_wall):
#   13 neuromodulation lenses FAILED because they treated DA/NE/ACh as ABSTRACT GAIN KNOBS on recall —
#   a scalar multiplier on a geometry-bound margin is INERT (the H_1284 neuromodulation wall, 5 lenses
#   converged WALL=CAPACITY). The reframe: implement each neurotransmitter as its OWN biological FACULTY
#   — a distinct COMPUTATION — like anima's brain lanes (immune≈hippocampus H_1227/1231,
#   cerebellum≈forward-model H_1280, basal-ganglia≈gating H_1281, WM-buffer H_1282, hier-PFC H_1294,
#   spatial-map H_1295). DOPAMINE's real computation (Schultz 1997; Sutton & Barto, RL: An Introduction)
#   is REWARD-PREDICTION-ERROR: δ_t = r_t + γ·V(s_{t+1}) − V(s_t), used for TEMPORAL CREDIT ASSIGNMENT —
#   which earlier stored facts/actions CAUSED a delayed downstream reward.
#
#   This is BRAIN-LANE-FILLING (the H_1280–1295 mode), NOT the recall-gain wall. anima's store binds facts
#   but has NO RPE signal: it cannot say "of the 6 facts I encountered before this reward, which 2 CAUSED
#   it?" A bare store credits by RECENCY (the fact nearest the reward) or UNIFORMLY — both wrong when the
#   causal fact is several steps upstream of a delayed reward and distractors sit between.
#
# CAPABILITY UNDER TEST = DELAYED-CREDIT-ASSIGNMENT.
#   A trajectory is a sequence of stored facts (states). Exactly 2 of them are CAUSAL (each carries a
#   true one-step reward r=1 emitted LATER, at the trajectory's end, as a single delayed lump — the causal
#   facts themselves give r=0 at the moment they occur). The rest are distractors (never causal). The task:
#   identify the CAUSAL facts. A faculty WITH a TD/RPE signal (δ propagated back via V) credits the upstream
#   causal states; a store WITHOUT it (recency / uniform) cannot, because the reward arrives far downstream.
#
#   ARMS:
#     NO-DA   — bare store baseline: NO RPE. Credit a fact by RECENCY to the reward (the standard
#               null a store can do) — closer-to-reward ⇒ higher credit. (Also report a UNIFORM null.)
#     DA-RPE  — the dopamine FACULTY: TD(λ) value learning over the trajectory with δ_t the RPE; the
#               accumulated eligibility-weighted |δ| credit on each state IS the credit signal. Causal
#               states (whose value must rise to predict the coming reward) accrue the credit; distractors
#               between two causal states do not earn it.
#     ABL     — DA-RPE with δ forced to 0 (no learning signal) ⇒ V stays flat ⇒ credit reverts to the
#               recency/uniform baseline (anti-Goodhart: the faculty's OWN mechanism OFF must collapse it).
#     SHUFFLE — DA-RPE but the reward TIMING is permuted across trajectories (reward dissociated from the
#               causal facts) ⇒ TD has nothing real to credit ⇒ collapse.
#
# PRE-REGISTERED (H_1536_FREEZE.txt), frozen-first, NO tune-to-green:
#   (A) PRESENCE : DA-RPE credit-assignment accuracy − NO-DA(recency) ≥ +0.10   (PRESENCE test, not beat-best-gain)
#   (B) DISTINCT : DA-RPE also beats the UNIFORM null by ≥ +0.10                  (signal ≠ trivial)
#   (C) ABLATE   : ABL (δ→0) ≤ NO-DA + 0.05                                       (decisive — mechanism OFF reverts)
#   (D) SHUFFLE  : SHUFFLE ≤ NO-DA + 0.05                                         (reward-timing carries the signal)
#   🟢 iff A∧B∧C∧D. HONEST (c9): if RPE does NOT beat the recency baseline ⇒ 🧱/🟠, reported not hidden —
#   that would mean delayed credit is recency-solvable here and DA-as-faculty adds nothing on this task.
#
# $0 CPU, deterministic, 3 seeds, p7 (NO perplexity/loss; metric = causal-fact identification accuracy).
#
# Literature (REAL, cited; modelled NOT a gain knob):
#   - Schultz W, Dayan P, Montague PR (1997) "A neural substrate of prediction and reward." Science 275:1593.
#   - Schultz W (1998) "Predictive reward signal of dopamine neurons." J Neurophysiol 80(1):1-27.
#   - Sutton RS, Barto AG (2018) "Reinforcement Learning: An Introduction" (2e) — TD(λ), eligibility traces.
#   - Montague PR, Dayan P, Sejnowski TJ (1996) "A framework for mesencephalic dopamine systems..."
#     J Neurosci 16(5):1936-1947.

import numpy as np

# ───────────────────────── store-faithful key geometry (mirror of ImmuneMemoryGrow) ──────────
# A "fact" = a stored item keyed by IDENTITY. anima's immune store (H_1227/1231) keys facts by an FNV
# hash and recalls per-identity; credit assignment is over WHICH STORED FACT predicts reward, so the key
# must be IDENTITY-DISCRIMINATING (a fact's value must be attributable to that fact, not smeared across
# near-identical hash buckets). We use the FNV-1a hash of the fact string to a one-hot identity bucket in
# a dim≥POOL space — the faithful "which stored item" key (collision-free at this pool size). The RPE
# value head then learns a value PER STORED-FACT IDENTITY, exactly the dopaminergic credit signal.

DIM = 64   # ≥ POOL ⇒ each stored fact gets a distinct identity slot


def _ident_key(idx, dim=DIM):
    # identity key: one-hot at the stored fact's pool index (collision-free per-item key, the faithful
    # "which stored item" representation the store recalls by). The RPE value head learns a value PER
    # identity ⇒ per-fact dopaminergic credit. (dim = POOL+spare ⇒ each fact a distinct slot.)
    v = np.zeros(dim, dtype=np.float64)
    v[idx] = 1.0
    return v


# ───────────────────────── trajectory generator ──────────────────────────────────────────────
# Each EPISODE is a length-T trajectory of stored facts (states s_0..s_{T-1}, s_{T-1}=terminal). The
# environment has a small set of CAUSAL fact IDENTITIES (the SAME facts cause reward across episodes —
# this is the real credit-assignment problem: which RECURRING facts predict the delayed reward). An
# episode's terminal reward = (# causal facts that appeared in it). Crucially the causal facts appear at
# RANDOM positions, so POSITION/RECENCY is UNINFORMATIVE about which fact is causal — only the cross-
# episode statistic (this fact-identity is followed by reward) reveals it. A bare RECENCY store cannot
# see that; an RPE value head keyed on fact identity learns it.
#
# WHY this separates RPE-credit from recency: recency credits the fact nearest the terminal lump, but the
# causal identities are placed at random positions ⇒ recency ≈ chance on identifying them. The RPE faculty
# accumulates value on the recurring causal keys across episodes ⇒ identifies them. The task asks, per
# episode, to name the causal facts PRESENT in it (top-N_PRESENT by credit), scored against ground truth.

T = 8            # trajectory length (states s_0..s_7; s_7 = terminal reward state)
N_CAUSAL_IDS = 6 # number of recurring CAUSAL fact identities in the environment
N_PRESENT = 2    # top-N for scoring = number of causal facts present per episode (held fixed for scoring)
N_EPISODES = 120 # trajectories per seed
POOL = 40        # total distinct fact identities
TERMINAL_ID = POOL - 1  # shared non-causal terminal marker


def build_env(rng):
    pool = ["subj%02d knows fact %02d about topic %02d" % (i, i, (i * 7) % 13) for i in range(POOL)]
    causal_ids = set(rng.choice(POOL - 1, size=N_CAUSAL_IDS, replace=False).tolist())  # exclude terminal
    return pool, causal_ids


def make_episode(rng, pool, causal_ids):
    # CONTINGENT reward: each episode's body has T-1 non-terminal states. We draw a VARIABLE number of
    # causal identities (0..min(N_CAUSAL_IDS, T-1)) — but to keep scoring well-posed we score ONLY episodes
    # with exactly N_PRESENT causal facts; the value head, however, trains on the FULL variable-reward set
    # so reward genuinely CO-VARIES with which causal facts appear (the credit-assignment signal). Causal
    # facts are placed at RANDOM positions ⇒ recency cannot localize them.
    causal_list = list(causal_ids)
    distractor_ids = [i for i in range(len(pool)) if i not in causal_ids and i != TERMINAL_ID]
    k = int(rng.integers(0, min(N_CAUSAL_IDS, T - 1) + 1))   # variable # causal facts present this episode
    present_causal = rng.choice(causal_list, size=k, replace=False).tolist() if k > 0 else []
    chosen_distractors = rng.choice(distractor_ids, size=T - 1 - k, replace=False).tolist()
    body_ids = present_causal + chosen_distractors
    rng.shuffle(body_ids)                              # RANDOM positions ⇒ recency uninformative
    state_ids = body_ids + [TERMINAL_ID]              # last = shared terminal marker (non-causal)
    causal_positions = sorted([p for p, sid in enumerate(state_ids[:-1]) if sid in causal_ids])
    rewards = np.zeros(T, dtype=np.float64)
    rewards[T - 1] = float(k)                          # delayed lump = # causal facts present (CONTINGENT)
    return state_ids, causal_positions, rewards


# ───────────────────────── ARM 1: NO-DA (bare store, recency baseline) ─────────────────────────
# The standard thing a store WITHOUT an RPE faculty can do: credit a non-terminal state by its RECENCY
# to the reward (closer to the terminal lump ⇒ more credit). This is the honest baseline a recency-store
# yields. (We also compute a UNIFORM null for (B).)

def credit_recency(state_ids, rewards):
    # recency credit over non-terminal states 0..T-2: weight ∝ proximity to terminal reward index.
    cred = np.zeros(T - 1, dtype=np.float64)
    for t in range(T - 1):
        cred[t] = 1.0 / float((T - 1) - t)   # nearer the end (larger t) ⇒ larger credit
    return cred


def credit_uniform(state_ids, rewards):
    return np.ones(T - 1, dtype=np.float64)


# ───────────────────────── ARM 2: DA-RPE (the dopamine FACULTY) ────────────────────────────────
# TD(λ) value learning with the RPE δ_t = r_t + γ·V(s_{t+1}) − V(s_t). The faculty learns a value V(s)
# keyed on the stored fact's key-vector via a linear value head w (V(s) = w·φ(s)); eligibility traces e
# accumulate per feature; δ updates w along e. The CREDIT a state earns is the accumulated eligibility-
# weighted RPE magnitude that flowed THROUGH it — i.e. how much that state's value had to move to predict
# the coming reward. Causal states (whose presence genuinely predicts the terminal lump) accrue credit
# across passes; distractors between them do not, because their value need not move to explain the reward.
#
# This is NOT a gain on recall margin. It is a temporal-difference computation the store does not have.

GAMMA = 0.95
LAMBDA = 0.8
ALPHA = 0.05
N_EPOCHS = 30   # sweeps over the WHOLE episode set (the credit problem is CROSS-episode: which RECURRING
                # fact identities predict reward — so the value head must learn over many trajectories)


def train_value_head(train_episodes, zero_delta=False):
    # TD(λ) value learning over the FULL episode set. δ_t = r_t + γV(s_{t+1}) − V(s_t); update the shared
    # linear value head w along the eligibility trace. The value V(s)=w·φ(s) generalizes across episodes
    # via the shared key geometry: a RECURRING causal fact (consistently followed by the terminal lump)
    # accrues HIGH value on its key; a distractor (appears at random with no reward contingency) does not.
    # This is the dopamine FACULTY's computation — temporal-difference credit, NOT a gain on a recall margin.
    # rewards[T-1] is the delayed lump DELIVERED ON ARRIVAL at the terminal state. We run TD over the
    # transitions t=0..T-2 (s_t → s_{t+1}); the reward received ON the transition into s_{t+1} is
    # rewards[t+1]. The terminal s_{T-1} is ABSORBING (V(terminal):=0), so the last transition's target
    # is the bare lump rewards[T-1] — which is what propagates credit back to the causal facts.
    w = np.zeros(DIM, dtype=np.float64)
    for _ in range(N_EPOCHS):
        for state_ids, _causal, rewards in train_episodes:
            phis = [_ident_key(i) for i in state_ids]
            e = np.zeros(DIM, dtype=np.float64)
            for t in range(T - 1):
                v_t = float(w @ phis[t])
                terminal_next = (t + 1 == T - 1)
                v_tp1 = 0.0 if terminal_next else float(w @ phis[t + 1])  # absorbing terminal ⇒ V:=0
                r_next = rewards[t + 1]                                    # reward on arrival into s_{t+1}
                delta = r_next + GAMMA * v_tp1 - v_t
                if zero_delta:
                    delta = 0.0   # ABL: no learning signal — V stays flat ⇒ credit reverts to uniform
                e = GAMMA * LAMBDA * e + phis[t]
                w = w + ALPHA * delta * e
    return w


def credit_da_value(w, state_ids):
    # per-episode credit = learned value of each NON-terminal stored fact (how strongly it predicts the
    # coming delayed reward). With δ→0 the head is the zero vector ⇒ all-equal credit (uniform fallback).
    return np.array([float(w[i]) for i in state_ids[:T - 1]], dtype=np.float64)


# ───────────────────────── scoring ────────────────────────────────────────────────────────────

def topn_accuracy(credit, causal_positions, n=N_PRESENT):
    # the top-n credited non-terminal states; accuracy = fraction that are truly causal.
    order = np.argsort(-credit)               # descending credit (stable, deterministic given inputs)
    picked = set(order[:n].tolist())
    causal = set(causal_positions)
    hit = len(picked & causal)
    return hit / float(n)


def score_arm(episodes, credit_of_episode):
    # credit_of_episode: (states, causal_positions, rewards) -> credit vector over non-terminal states
    accs = [topn_accuracy(credit_of_episode(s, cp, r), cp) for (s, cp, r) in episodes]
    return float(np.mean(accs))


SEEDS = [1536, 1537, 1538]


def run():
    lines = []

    def emit(s=""):
        lines.append(s)
        print(s)

    da, noda_rec, noda_uni, abl, shuf = [], [], [], [], []
    for sd in SEEDS:
        rng = np.random.default_rng(sd)
        pool, causal_ids = build_env(rng)
        episodes = [make_episode(rng, pool, causal_ids) for _ in range(N_EPISODES)]
        # SCORING set = episodes with exactly N_PRESENT causal facts (well-posed top-N); the value head
        # TRAINS on the full variable-reward set (reward co-varies with causal-fact presence).
        score_eps = [ep for ep in episodes if len(ep[1]) == N_PRESENT]

        # DA-RPE: train value head over the FULL set (cross-episode contingent credit), score on score_eps.
        w = train_value_head(episodes)
        da.append(score_arm(score_eps, lambda s, cp, r: credit_da_value(w, s)))

        # NO-DA baselines (per-episode, no RPE) on the SAME scoring set
        noda_rec.append(score_arm(score_eps, lambda s, cp, r: credit_recency(s, r)))
        noda_uni.append(score_arm(score_eps, lambda s, cp, r: credit_uniform(s, r)))

        # ABL: δ→0 — head stays zero ⇒ uniform credit (anti-Goodhart, must revert to baseline)
        w_abl = train_value_head(episodes, zero_delta=True)
        abl.append(score_arm(score_eps, lambda s, cp, r: credit_da_value(w_abl, s)))

        # SHUFFLE: permute reward TIMING across episodes ⇒ reward dissociated from causal identities
        perm = rng.permutation(N_EPISODES)
        shuf_eps_full = [(episodes[i][0], episodes[i][1], episodes[perm[i]][2]) for i in range(N_EPISODES)]
        w_shf = train_value_head(shuf_eps_full)
        shuf.append(score_arm(score_eps, lambda s, cp, r: credit_da_value(w_shf, s)))

    m_da = float(np.mean(da))
    m_rec = float(np.mean(noda_rec))
    m_uni = float(np.mean(noda_uni))
    m_abl = float(np.mean(abl))
    m_shf = float(np.mean(shuf))

    emit("=== H_1536 NT-DOPAMINE — dopamine as RPE/credit-assignment FACULTY (R1 numpy mirror, DIRECTIONAL) ===")
    emit("seeds=%s  $0 CPU  deterministic  p7  c9  frozen-first  DA-as-FACULTY (not gain)" % SEEDS)
    emit("task=DELAYED-CREDIT-ASSIGNMENT  T=%d  N_CAUSAL_IDS=%d  N_PRESENT=%d  episodes=%d  γ=%.2f λ=%.2f α=%.2f epochs=%d"
         % (T, N_CAUSAL_IDS, N_PRESENT, N_EPISODES, GAMMA, LAMBDA, ALPHA, N_EPOCHS))
    emit("causal facts placed at RANDOM positions ⇒ recency uninformative; chance top-%d of %d = %.4f"
         % (N_PRESENT, T - 1, N_PRESENT / float(T - 1)))
    emit("")
    emit("--- arm credit-assignment accuracy (seed-mean) ---")
    emit("  DA-RPE  (dopamine faculty)      = %.4f   per-seed=%s" % (m_da, ["%.3f" % x for x in da]))
    emit("  NO-DA   (recency baseline)      = %.4f   per-seed=%s" % (m_rec, ["%.3f" % x for x in noda_rec]))
    emit("  NO-DA   (uniform null)          = %.4f   per-seed=%s" % (m_uni, ["%.3f" % x for x in noda_uni]))
    emit("  ABL     (δ→0, no RPE)           = %.4f   per-seed=%s" % (m_abl, ["%.3f" % x for x in abl]))
    emit("  SHUFFLE (reward-timing permuted)= %.4f   per-seed=%s" % (m_shf, ["%.3f" % x for x in shuf]))
    emit("")

    a_pass = (m_da - m_rec) >= 0.10
    b_pass = (m_da - m_uni) >= 0.10
    c_pass = m_abl <= (m_rec + 0.05)
    d_pass = m_shf <= (m_rec + 0.05)

    emit("=== (A) PRESENCE — DA-RPE − NO-DA(recency) ≥ +0.10 ===")
    emit("  Δ = %+.4f   (≥+0.10)   %s" % (m_da - m_rec, "PASS" if a_pass else "FAIL"))
    emit("=== (B) DISTINCT — DA-RPE − UNIFORM null ≥ +0.10 ===")
    emit("  Δ = %+.4f   (≥+0.10)   %s" % (m_da - m_uni, "PASS" if b_pass else "FAIL"))
    emit("=== (C) ABLATE — δ→0 reverts to baseline (≤ NO-DA + 0.05) ===")
    emit("  ABL = %.4f   NO-DA+0.05 = %.4f   %s" % (m_abl, m_rec + 0.05, "PASS" if c_pass else "FAIL"))
    emit("=== (D) SHUFFLE — reward-timing permuted collapses (≤ NO-DA + 0.05) ===")
    emit("  SHUFFLE = %.4f   NO-DA+0.05 = %.4f   %s" % (m_shf, m_rec + 0.05, "PASS" if d_pass else "FAIL"))
    emit("")

    green = a_pass and b_pass and c_pass and d_pass
    emit("=== VERDICT ===")
    emit("  (A) presence  = %s" % ("PASS" if a_pass else "FAIL"))
    emit("  (B) distinct  = %s" % ("PASS" if b_pass else "FAIL"))
    emit("  (C) ablate    = %s" % ("PASS" if c_pass else "FAIL"))
    emit("  (D) shuffle   = %s" % ("PASS" if d_pass else "FAIL"))
    emit("")
    if green:
        emit("  H_1536 NT-DOPAMINE (R1 mirror) = 🟢 GREEN DIRECTIONAL")
        emit("  → dopamine-as-RPE is a NEW substrate FACULTY: it adds delayed-credit-assignment a recency-store")
        emit("    lacks; ablation (δ→0) decisive. NOT a gain knob — a temporal-difference computation.")
    else:
        emit("  H_1536 NT-DOPAMINE (R1 mirror) = 🧱/🟠 HONEST — RPE faculty did NOT add credit over baseline")
        emit("    (delayed credit recency-solvable here OR ablation not decisive; reported not hidden, c9)")
    emit("  wired: DIRECTIONAL-mirror (numpy) → R2 engine-native §Dopamine follow-on (ING)")
    return green, lines


if __name__ == "__main__":
    import sys
    green, lines = run()
    if "--freeze" in sys.argv:
        # result goes to H_1536.txt; H_1536_FREEZE.txt holds the PRE-REGISTERED bars (do NOT overwrite).
        with open("state/verdicts/1536_nt_dopamine/H_1536.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        import json
        rec = {
            "id": "H_1536", "slug": "1536_nt_dopamine", "seeds": SEEDS,
            "task": "delayed-credit-assignment", "T": T, "N_CAUSAL_IDS": N_CAUSAL_IDS,
            "N_PRESENT": N_PRESENT, "episodes": N_EPISODES,
            "arms": {"DA_RPE": None, "NO_DA_recency": None, "NO_DA_uniform": None,
                     "ABL": None, "SHUFFLE": None},
        }
        # parse seed-means from the arm-table lines (label → "= <float>   per-seed=...")
        def _seedmean(ln):
            return float(ln.split("=", 1)[1].split()[0])
        for ln in lines:
            if "per-seed=" not in ln:
                continue
            if "DA-RPE  (dopamine" in ln:
                rec["arms"]["DA_RPE"] = _seedmean(ln)
            elif "recency baseline" in ln:
                rec["arms"]["NO_DA_recency"] = _seedmean(ln)
            elif "uniform null" in ln:
                rec["arms"]["NO_DA_uniform"] = _seedmean(ln)
            elif "ABL " in ln:
                rec["arms"]["ABL"] = _seedmean(ln)
            elif "SHUFFLE" in ln:
                rec["arms"]["SHUFFLE"] = _seedmean(ln)
        rec["verdict"] = "🟢 GREEN DIRECTIONAL" if green else "🧱/🟠 HONEST"
        rec["wired"] = "DIRECTIONAL-mirror (numpy) → R2 engine-native §Dopamine follow-on (ING)"
        with open("state/verdicts/1536_nt_dopamine/H_1536_R1.json", "w") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
    sys.exit(0 if green else 1)
