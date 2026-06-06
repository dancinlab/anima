"""cwm_probe_lib.py — shared $0 CPU-local toy machinery for the CWM world-model slate
(UNIVERSE/H_960..H_984).

Substrate tag: CPU-mirror (numpy). a_lane_akida_gpu_split — NOTHING here runs on AKIDA;
SUBSTRATE-axis hypotheses (H_965/966/974/977) that need a live AKD1000 are marked
INCOMPLETE-BLOCKED elsewhere; where a meaningful SW arm exists it is tagged substrate=CPU-mirror
and NEVER claims an on-chip result.

Design goals
------------
* g5 CODE-measured (no LLM self-judge, p7) — every verdict token comes from a number.
* deterministic given a seed (reproducible), entropy supplied by numpy default_rng
  (the deterministic-auxiliary policy of qentropy; quantum coupling is out of scope here).
* a single compact recurrent latent "engine" mirror = a *world model*: it carries a
  persistent latent state h_t = tanh(W_in x_t + W_rec h_{t-1} + b), with linear readouts.
  This is the minimal substrate-faithful object that distinguishes a WORLD model
  (persistent latent state, can roll forward / fill-in) from a stateless next-symbol
  predictor (LM-style: window -> next, NO carried state).

The engine is intentionally tiny (toy scale, a_scale_honest_scope) — a single rung,
ladder OPEN. No claim transfers to production scale.
"""
import numpy as np


# ----------------------------------------------------------------------------- engine
class LatentWorldModel:
    """A minimal recurrent latent world model (the WM / "engine" mirror).

    h_t = tanh(W_in @ x_t + W_rec @ h_{t-1} + b_h)      persistent latent state
    readouts are LINEAR maps from h_t (or from a rolled-forward latent).

    Trained by ridge-regression on collected (h_t, target) pairs after a fixed random
    recurrent reservoir (echo-state style) — this keeps it $0/fast/deterministic while
    still giving a genuine *persistent latent state* and a learnable *latent transition
    operator* T (h_{t+1} ≈ T(h_t)) for imagined rollout.
    """

    def __init__(self, in_dim, latent_dim=32, seed=0, spectral_radius=0.9, leak=1.0,
                 retentive=False, in_scale=1.0):
        self.rng = np.random.default_rng(seed)
        self.in_dim = in_dim
        self.d = latent_dim
        self.leak = leak
        self.retentive = retentive
        self.W_in = (self.rng.standard_normal((latent_dim, in_dim)) / np.sqrt(in_dim)) * in_scale
        if retentive:
            # an ORTHOGONAL recurrence preserves the latent norm step-to-step -> long
            # memory (a faithful "persistent latent state"; a real WM remembers).
            A = self.rng.standard_normal((latent_dim, latent_dim))
            Q, _ = np.linalg.qr(A)
            self.W_rec = Q * spectral_radius
        else:
            W = self.rng.standard_normal((latent_dim, latent_dim))
            # scale recurrent matrix to a target spectral radius (echo-state property)
            eig = np.max(np.abs(np.linalg.eigvals(W)))
            self.W_rec = W * (spectral_radius / (eig + 1e-9))
        self.b_h = self.rng.standard_normal(latent_dim) * 0.1
        self.W_out = None          # latent -> readout target (ridge)
        self.T = None              # latent -> next-latent operator (ridge), for rollout

    def step(self, h, x):
        pre = self.W_in @ x + self.W_rec @ h + self.b_h
        if self.retentive:
            # linear retentive recurrence: an orthogonal W_rec preserves history exactly,
            # so a cue written at t=0 survives a long delay (persistent world-state).
            h_new = pre
        else:
            h_new = np.tanh(pre)
        return (1 - self.leak) * h + self.leak * h_new

    def encode_seq(self, seq):
        """Run the recurrence over a (T, in_dim) sequence; return all latents (T, d)."""
        h = np.zeros(self.d)
        H = np.empty((len(seq), self.d))
        for t, x in enumerate(seq):
            h = self.step(h, x)
            H[t] = h
        return H

    def final_latent(self, seq):
        return self.encode_seq(seq)[-1]

    # ----- supervised readout via ridge regression (closed form) -----
    def fit_readout(self, H, Y, ridge=1e-2):
        H1 = _aug(H)
        self.W_out = _ridge(H1, Y, ridge)
        return self

    def predict_readout(self, H):
        return _aug(H) @ self.W_out

    # ----- latent transition operator for imagined rollout -----
    def fit_transition(self, H_t, H_tp1, ridge=1e-2):
        self.T = _ridge(_aug(H_t), H_tp1, ridge)
        return self

    def roll_latent(self, h0, steps):
        """Imagined rollout: apply the learned latent transition operator T, h-only."""
        out = []
        h = h0.copy()
        for _ in range(steps):
            h = (_aug1(h) @ self.T)
            out.append(h.copy())
        return np.array(out)


class StatelessLM:
    """A matched-capacity next-symbol / next-observation predictor with NO persistent
    latent state — it sees a fixed window of the last `ctx` observations and maps that
    (via a random feature ridge of comparable capacity) to its target. This is the LM
    baseline: window -> next, carrying nothing across steps beyond the window."""

    def __init__(self, in_dim, ctx, feat_dim=32, seed=1):
        self.rng = np.random.default_rng(seed)
        self.in_dim = in_dim
        self.ctx = ctx
        self.d = feat_dim
        self.W_feat = self.rng.standard_normal((feat_dim, in_dim * ctx)) / np.sqrt(in_dim * ctx)
        self.b = self.rng.standard_normal(feat_dim) * 0.1
        self.W_out = None

    def _feat(self, window):
        v = np.tanh(self.W_feat @ window.reshape(-1) + self.b)
        return v

    def features_over_seq(self, seq):
        """Sliding window features; left-pad with zeros so length matches seq."""
        T = len(seq)
        F = np.empty((T, self.d))
        pad = np.zeros((self.ctx - 1, self.in_dim))
        ext = np.vstack([pad, seq])
        for t in range(T):
            window = ext[t:t + self.ctx]   # last ctx obs INCLUDING the current step t
            F[t] = self._feat(window)
        return F

    def fit_readout(self, F, Y, ridge=1e-2):
        self.W_out = _ridge(_aug(F), Y, ridge)
        return self

    def predict_readout(self, F):
        return _aug(F) @ self.W_out


class LDSWorldModel:
    """A delay-embedding linear-dynamical-system world model (the faithful latent-forward-
    dynamics object, JEPA/Dreamer-style). latent z_t = [o_t, o_{t-1}, ...] captures hidden
    derivatives a single observation lacks; a LEARNED linear transition A rolls z forward;
    a decoder C reads z -> observable. This composes for multi-step imagined rollout where
    a stateless surface predictor cannot (it has no persistent world-state).

    Action-conditioned: an optional action one-hot is appended; the transition then learns
    z_{t+1} = A [z_t ; a_t] so imagined rollouts can be conditioned on candidate actions
    (H_964/H_967/H_980).
    """

    def __init__(self, obs_dim, delay=2, act_dim=0, ridge=1e-3):
        self.obs_dim = obs_dim
        self.delay = delay
        self.act_dim = act_dim
        self.ridge = ridge
        self.A = None
        self.C = None
        self.zdim = obs_dim * delay

    def embed(self, ob):
        ob = np.asarray(ob, float)
        T = len(ob)
        z = np.zeros((T, self.zdim))
        for d in range(self.delay):       # block d holds o_{t-d}
            if d == 0:
                z[:, :self.obs_dim] = ob
            else:
                z[d:, d * self.obs_dim:(d + 1) * self.obs_dim] = ob[:-d]
        return z

    def fit(self, traj_obs, traj_targets=None, traj_acts=None):
        """traj_obs: list of (T,obs) observation seqs. traj_targets: list of (T,k) decode
        targets (default = the observation itself). traj_acts: list of (T,act_dim) one-hots."""
        Zt, Ztp1, Zd, Yd = [], [], [], []
        for i, ob in enumerate(traj_obs):
            z = self.embed(ob)
            a = traj_acts[i] if traj_acts is not None else None
            zin = z[self.delay - 1:-1]
            if a is not None:
                zin = np.hstack([zin, a[self.delay - 1:-1]])
            Zt.append(zin); Ztp1.append(z[self.delay:])
            tgt = traj_targets[i] if traj_targets is not None else ob
            Zd.append(z); Yd.append(np.asarray(tgt, float))
        self.A = _ridge(_aug(np.vstack(Zt)), np.vstack(Ztp1), self.ridge)
        self.C = _ridge(_aug(np.vstack(Zd)), np.vstack(Yd), self.ridge)
        return self

    def roll(self, z0, h, act_seq=None):
        z = np.asarray(z0, float).copy()
        for k in range(h):
            zin = z if act_seq is None else np.hstack([z, act_seq[k]])
            z = (_aug1(zin) @ self.A)
        return z

    def decode(self, z):
        return _aug1(np.asarray(z, float)) @ self.C


# ----------------------------------------------------------------------------- math utils
def _aug(H):
    return np.hstack([H, np.ones((H.shape[0], 1))])


def _aug1(h):
    return np.hstack([h, [1.0]])


def _ridge(X, Y, lam):
    if Y.ndim == 1:
        Y = Y[:, None]
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d)
    B = X.T @ Y
    return np.linalg.solve(A, B)


def n_params_wm(in_dim, latent_dim):
    # learned params: W_out (readout) + T (transition); reservoir is fixed/random.
    return latent_dim  # readout cols counted per-call by the caller via shapes


def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / max(na + nb - 2, 1))
    if sp == 0:
        return 0.0
    return (a.mean() - b.mean()) / sp


def welch_t(a, b):
    from scipy import stats
    t, p = stats.ttest_ind(a, b, equal_var=False)
    return float(t), float(p)


def boot_ci(x, stat=np.mean, n=2000, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    bs = np.array([stat(rng.choice(x, size=len(x), replace=True)) for _ in range(n)])
    lo, hi = np.percentile(bs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def spearman(a, b):
    from scipy import stats
    r, p = stats.spearmanr(a, b)
    return float(r), float(p)


def cka(X, Y):
    """Linear CKA similarity between two latent matrices (n x d)."""
    X = X - X.mean(0)
    Y = Y - Y.mean(0)
    hsic = np.linalg.norm(X.T @ Y, 'fro') ** 2
    nx = np.linalg.norm(X.T @ X, 'fro')
    ny = np.linalg.norm(Y.T @ Y, 'fro')
    return float(hsic / (nx * ny + 1e-12))


def phi_proxy(H):
    """Continuous-latent Φ proxy (the H_912/H_931 proxy FAMILY, NOT full IIT4 big-Φ).

    Φ = integration × differentiation × (0.5 + 0.5·entropy_norm), the same three-axis
    structure as phi_silicon_proxy (AKIDA/h927) but on a continuous latent trajectory
    H (n_steps × d) instead of spike counts:
      * integration = variance-partition (canonical phi_spatial, H_912): how much the
        whole-system variance exceeds the mean per-partition variance — a high value
        means the parts are bound (integrated), not independent.
      * differentiation = effective dimensionality (participation ratio / d) — the
        system explores many distinguishable states, not one.
      * entropy = normalized Shannon entropy of the binned activity magnitude.
    Honest proxy; toy scale (a_scale_honest_scope).
    """
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    n, d = H.shape
    C = np.cov(H.T) if n > 1 else np.eye(d) * 1e-9
    # integration (variance-partition / binding, H_912 phi_spatial family): the share of
    # total second-moment mass carried by CROSS-partition coupling (off-block covariance).
    # parts independent -> off-block≈0 -> integration≈0; bound -> high. Scale-free.
    if d >= 2:
        absC = np.abs(C)
        total = absC.sum()
        diag = np.abs(np.diag(C)).sum()
        integration = float((total - diag) / (total + 1e-12)) if total > 1e-12 else 0.0
    else:
        integration = 0.0
    ev = np.clip(np.linalg.eigvalsh(C), 0, None)
    pr = (ev.sum() ** 2) / (np.sum(ev ** 2) + 1e-12)
    differentiation = pr / d
    # entropy: normalized Shannon entropy of binned latent magnitude.
    mag = np.linalg.norm(H, axis=1)
    nb = min(16, max(2, n // 2))
    hist, _ = np.histogram(mag, bins=nb)
    p = hist / (hist.sum() + 1e-12)
    p = p[p > 0]
    ent = -(p * np.log2(p)).sum() / (np.log2(nb) + 1e-12)
    phi = integration * differentiation * (0.5 + 0.5 * ent)
    return float(phi), dict(integration=integration, differentiation=float(differentiation),
                            entropy=float(ent))


def header(hid, title, substrate="CPU-mirror (numpy)"):
    print("=" * 78)
    print(f"{hid} — {title}")
    print(f"substrate={substrate}  |  g5 CODE-measured (no LLM self-judge, p7)")
    print(f"a_scale_honest_scope: TOY single-rung, ladder OPEN — no production transfer")
    print("=" * 78)


def verdict_line(hid, token, msg):
    print("-" * 78)
    print(f"VERDICT {hid}: {token} {msg}")
    print("-" * 78)
