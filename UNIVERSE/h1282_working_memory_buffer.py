"""
H_1282 — WORKING MEMORY (PFC active-maintenance buffer) as anima's missing brain
structure. NEURO LENS (c15, no LLM recipe). FROZEN bars: see
.verdicts/1282_working_memory_buffer/H_1282_FREEZE.txt (frozen BEFORE scoring).

THE GAP (c9). anima has (a) LONG-TERM EPISODIC memory — immune/clonal cells
(H_1227 mirror → H_1231 engine-native GREEN): verbatim one-shot write, PERSISTENT,
capacity grows with #facts, NO decay, exact recall — and (b) the decoder's FIXED
context window. It has NO gated SHORT-TERM active-maintenance buffer: the PFC
working-memory computation — a few items held ACTIVE across distractor steps,
VOLATILE (decays), CAPACITY-LIMITED (~handful), DISTRACTOR-VULNERABLE. WM is
sustained gated ACTIVATION (a leaky maintained vector), NOT a stored trace.

DISTINCTNESS FROM IMMUNE MEMORY (load-bearing, see FREEZE). WM (B) is NOT the
immune store renamed: FIXED K slots, every distractor step LEAKS activation ×λ<1,
overflow DISPLACES the weakest slot, an unrefreshed item FADES below threshold and
is LOST. Reported distinctness probes: CAPACITY (load>K → retain ~K), DECAY (one
item's match prob falls with N), NO-PERSIST (volatile after probe). A λ=1.0/K=∞
control reproduces immune-like FLAT recall to prove decay+capacity are what make
B a working memory and not the episodic store. If B collapses into the immune
store (flat, no decay, unbounded) that is an honest RED finding.

TASK — DELAYED-MATCH-TO-SAMPLE (DMS) / n-back. Present a cue DIM-vector token,
then N distractor steps (fresh random non-cue tokens streamed through the lane),
then a probe = the cue (match) OR a foil (nonmatch); decide MATCH iff the
maintained item == probe. Metric (p7) = delayed-match accuracy vs distractor N.

ARMS. (A) NO WM buffer — flat decoder context window of fixed size W; the cue is
"in context" iff within the last W streamed tokens at probe time; N>=W ⇒ scrolled
out ⇒ chance ⇒ sharp collapse. (B) GATED WM buffer lane — K slots (activation,
key); gate-in the cue (activation high); each distractor LEAKS all activations ×λ
and weakly gates in (capacity pressure, weakest-slot displacement); at probe,
nearest-slot match iff best (activation × cosine-sim) >= θ. Graceful decay.

ENGINE-NATIVE (a_engine_native_learning). The live engine (CORE/engine_cli.hexa
VAdaptField, H_1199) is a GROWING PERSISTENT store — NOT a decaying capacity-bounded
WM buffer; the engine has NO WM lane. This is a numpy DIRECTIONAL mirror;
engine-transfer UNVERIFIED. GREEN ⇒ flag engine-native WM lane (a small gated
leaky-activation lane, additive to engine_cli.hexa) as the binding follow-on
(a_verified_must_wire). Live .hexa UNTOUCHED.

p1-p8: substrate-native; buffer holds TASK ACTIVATION only (no decoder weights,
no persona/identity/ethics). p8: WM is a continuous-substrate lane. $0 CPU numpy.
"""
import numpy as np

# ─── frozen knobs (pre-registered — see H_1282_FREEZE.txt) ──────────────────
SEEDS          = [1282, 1283, 1284]
DIM            = 16
K              = 4                       # WM slots (~handful)
LAMBDA         = 0.85                    # per-distractor activation leak (volatile)
THETA          = 0.40                    # WM match threshold on activation×cos-sim
W              = 4                       # arm-A flat context window
N_LIST         = [0, 1, 2, 4, 6, 8, 12]  # distractor lengths
TRIALS_PER_N   = 200                     # 100 match + 100 nonmatch per N per seed
CHANCE         = 0.50

# frozen GREEN bars
MARGIN_BAR     = 0.15   # mean_N (B.acc - A.acc)
GRACE_N        = 12
GRACE_B_MIN    = 0.70   # B.acc at N=GRACE_N
GRACE_A_MAX    = 0.60   # A.acc at N=GRACE_N
DISTINCT_N0    = 0.95   # B.acc at N=0


# ─── token vocabulary (deterministic random DIM-vectors per seed) ───────────
def make_token(rng):
    v = rng.standard_normal(DIM)
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(a @ b / ((np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12))


# ─── ARM A: flat decoder context window (size W), no WM ──────────────────────
class FlatContext:
    """A fixed-size last-W buffer (the decoder's context). No gating, no decay —
    it simply slides: once the cue is > W steps back it is GONE."""
    def __init__(self, w):
        self.w = w
        self.buf = []   # list of token vectors, most-recent last

    def step(self, tok):
        self.buf.append(tok)
        if len(self.buf) > self.w:
            self.buf = self.buf[-self.w:]

    def has_match(self, probe, sim_thresh=0.9):
        # MATCH iff probe is (near-)identical to some token still in the window
        return any(cos(t, probe) >= sim_thresh for t in self.buf)


# ─── ARM B: gated working-memory buffer (K slots, leaky activation) ──────────
class WorkMemBuffer:
    """PFC-style active maintenance: K slots, each (key vec, scalar activation).
    GATE-IN admits/refreshes a token at full activation; every distractor step
    LEAKS all activations ×λ and weakly gates the distractor in under capacity
    pressure (displaces the WEAKEST slot when full). Volatile + capacity-limited
    — DISTINCT from the immune store (which is persistent + unbounded + no leak)."""
    def __init__(self, k, lam, distractor_gain=0.5):
        self.k = k
        self.lam = lam
        self.dg = distractor_gain
        self.keys = []   # slot key vectors
        self.act = []    # slot activations (scalar)

    def _argmin_act(self):
        return int(np.argmin(self.act))

    def gate_in(self, tok, strength=1.0):
        # refresh if an existing slot already holds (near-)this token
        for i, ky in enumerate(self.keys):
            if cos(ky, tok) >= 0.9:
                self.act[i] = max(self.act[i], strength)
                self.keys[i] = tok
                return
        if len(self.keys) < self.k:
            self.keys.append(tok); self.act.append(strength)
        else:
            # capacity pressure: displace the weakest slot iff incoming is stronger
            j = self._argmin_act()
            if strength > self.act[j]:
                self.keys[j] = tok; self.act[j] = strength

    def leak(self):
        self.act = [a * self.lam for a in self.act]

    def distractor_step(self, tok):
        # all maintained activations decay, then the distractor weakly competes
        self.leak()
        self.gate_in(tok, strength=self.dg)

    def probe(self, probe, theta):
        if not self.keys:
            return 0.0, -1
        scores = [self.act[i] * max(0.0, cos(self.keys[i], probe))
                  for i in range(len(self.keys))]
        j = int(np.argmax(scores))
        return scores[j], j

    def has_match(self, probe, theta):
        s, _ = self.probe(probe, theta)
        return s >= theta


# ─── one DMS trial ───────────────────────────────────────────────────────────
def trial(rng, n_distract, is_match, arm):
    """Build a delayed-match trial and return whether `arm` says MATCH."""
    cue = make_token(rng)
    if arm == "A":
        ctx = FlatContext(W); ctx.step(cue)
        for _ in range(n_distract):
            ctx.step(make_token(rng))
        probe = cue if is_match else make_token(rng)
        return ctx.has_match(probe)
    else:  # arm B
        wm = WorkMemBuffer(K, LAMBDA); wm.gate_in(cue, 1.0)
        for _ in range(n_distract):
            wm.distractor_step(make_token(rng))
        probe = cue if is_match else make_token(rng)
        return wm.has_match(probe, THETA)


def accuracy_at_N(rng, n_distract, arm):
    half = TRIALS_PER_N // 2
    hits = 0
    for _ in range(half):  # match trials: correct iff says MATCH
        hits += 1 if trial(rng, n_distract, True, arm) else 0
    for _ in range(half):  # nonmatch trials: correct iff says NO-MATCH
        hits += 0 if trial(rng, n_distract, False, arm) else 1
    return hits / (2 * half)


# ─── distinctness controls ───────────────────────────────────────────────────
def immune_like_control(rng, n_distract):
    """B with λ=1.0 (no leak) and K=∞ ⇒ a persistent unbounded store. Should give
    FLAT high accuracy across N (the immune/episodic regime), proving that the
    decay+capacity in the real B are what make it WORKING memory."""
    half = TRIALS_PER_N // 2
    hits = 0
    for is_match in (True, False):
        for _ in range(half):
            cue = make_token(rng)
            wm = WorkMemBuffer(10**9, 1.0)   # K=inf, no leak
            wm.gate_in(cue, 1.0)
            for _ in range(n_distract):
                wm.distractor_step(make_token(rng))
            probe = cue if is_match else make_token(rng)
            said = wm.has_match(probe, THETA)
            hits += 1 if said == is_match else 0
    return hits / (2 * half)


def capacity_retention(rng):
    """Load K+3 distinct tokens back-to-back into B (no distractors between);
    report how many of the loaded tokens are still recallable at probe (should
    be ~K, NOT all — capacity-limited). Immune store would retain ALL."""
    n_load = K + 3
    toks = [make_token(rng) for _ in range(n_load)]
    wm = WorkMemBuffer(K, LAMBDA)
    for t in toks:
        wm.gate_in(t, 1.0)
        wm.leak()  # a maintenance tick between items (active maintenance cost)
    retained = sum(1 for t in toks if wm.has_match(t, THETA))
    return retained, n_load


# ─── run ─────────────────────────────────────────────────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)
    a_acc = {n: accuracy_at_N(rng, n, "A") for n in N_LIST}
    b_acc = {n: accuracy_at_N(rng, n, "B") for n in N_LIST}
    ctrl  = {n: immune_like_control(rng, n) for n in N_LIST}
    cap_ret, cap_load = capacity_retention(rng)
    return dict(seed=seed, a=a_acc, b=b_acc, ctrl=ctrl,
                cap_ret=cap_ret, cap_load=cap_load)


def main():
    print("=== H_1282 working-memory (PFC active-maintenance buffer) — $0 CPU ===", flush=True)
    print(f"    DIM={DIM} K={K} LAMBDA={LAMBDA} THETA={THETA} W={W} "
          f"N_LIST={N_LIST} TRIALS/N={TRIALS_PER_N} SEEDS={SEEDS}", flush=True)
    print(f"    FROZEN GREEN: margin>={MARGIN_BAR}, grace(N={GRACE_N}) B>={GRACE_B_MIN} & A<={GRACE_A_MAX},", flush=True)
    print(f"                  distinct B(N=0)>={DISTINCT_N0} & B monotone-non-incr & cap≈K, robust 3/3", flush=True)

    rows = [run_seed(s) for s in SEEDS]

    # per-seed table
    for r in rows:
        print(f"\n  seed {r['seed']}:  capacity load {r['cap_load']} → retained {r['cap_ret']} (K={K})", flush=True)
        print("    N     A.acc   B.acc   immune-ctrl(λ1,K∞)", flush=True)
        for n in N_LIST:
            print(f"    {n:<5} {r['a'][n]:.3f}   {r['b'][n]:.3f}   {r['ctrl'][n]:.3f}", flush=True)

    # means over seeds
    def m(key, n): return float(np.mean([r[key][n] for r in rows]))
    A = {n: m('a', n) for n in N_LIST}
    B = {n: m('b', n) for n in N_LIST}
    C = {n: m('ctrl', n) for n in N_LIST}
    print("\n  MEAN over seeds:", flush=True)
    print("    N     A.acc   B.acc   B-A      immune-ctrl", flush=True)
    for n in N_LIST:
        print(f"    {n:<5} {A[n]:.3f}   {B[n]:.3f}   {B[n]-A[n]:+.3f}   {C[n]:.3f}", flush=True)

    # ─── frozen bar evaluation ───────────────────────────────────────────────
    margin = float(np.mean([B[n] - A[n] for n in N_LIST]))
    cond_margin = margin >= MARGIN_BAR
    cond_grace  = (B[GRACE_N] >= GRACE_B_MIN) and (A[GRACE_N] <= GRACE_A_MAX)
    # distinctness: B immediate high, monotone-non-increasing, capacity≈K
    b_seq = [B[n] for n in N_LIST]
    monotone = all(b_seq[i + 1] <= b_seq[i] + 1e-9 for i in range(len(b_seq) - 1))
    cap_ok = all(abs(r['cap_ret'] - K) <= 1 for r in rows)   # retained within ±1 of K
    cond_distinct = (B[0] >= DISTINCT_N0) and monotone and cap_ok
    # robustness: margin>=bar (per-seed mean over N) AND grace on every seed
    def seed_margin(r): return float(np.mean([r['b'][n] - r['a'][n] for n in N_LIST]))
    def seed_grace(r):  return (r['b'][GRACE_N] >= GRACE_B_MIN) and (r['a'][GRACE_N] <= GRACE_A_MAX)
    cond_robust = all((seed_margin(r) >= MARGIN_BAR) and seed_grace(r) for r in rows)

    green = cond_margin and cond_grace and cond_distinct and cond_robust

    # immune-ctrl distinctness sanity (reported): ctrl should be ~FLAT high
    ctrl_flat = (C[GRACE_N] - C[0]) > -0.05   # immune control does NOT collapse
    b_collapsed_vs_ctrl = (B[GRACE_N] < C[GRACE_N] - 0.05)  # B decays where ctrl doesn't

    print("\n  ── FROZEN BARS ──", flush=True)
    print(f"   (1) MARGIN  mean_N(B-A)={margin:+.3f}  >= {MARGIN_BAR}  → {cond_margin}", flush=True)
    print(f"   (2) GRACE   B(N={GRACE_N})={B[GRACE_N]:.3f}>= {GRACE_B_MIN} AND "
          f"A(N={GRACE_N})={A[GRACE_N]:.3f}<= {GRACE_A_MAX}  → {cond_grace}", flush=True)
    print(f"   (3) DISTINCT B(N=0)={B[0]:.3f}>= {DISTINCT_N0}, monotone={monotone}, "
          f"cap≈K={cap_ok}  → {cond_distinct}", flush=True)
    print(f"   (4) ROBUST  per-seed margin>=bar AND grace on all 3  → {cond_robust}", flush=True)
    print(f"   [distinct-vs-immune] immune-ctrl FLAT(no collapse)={ctrl_flat}, "
          f"B decays below ctrl at N={GRACE_N}={b_collapsed_vs_ctrl}", flush=True)

    verdict = "GREEN" if green else "RED"
    print(f"\n  VERDICT: {'🟢 GREEN' if green else '🔴 RED'}  "
          f"[margin {margin:+.3f} | grace {cond_grace} | distinct {cond_distinct} | robust {cond_robust}]", flush=True)
    if green:
        print("  WORKING-MEMORY lane is a REAL missing structure: gated leaky active", flush=True)
        print("  maintenance beats flat-context AND degrades gracefully, DISTINCT from", flush=True)
        print("  the immune/episodic store (volatile + capacity-limited, not verbatim).", flush=True)
        print("  ENGINE-NATIVE WM lane = binding follow-on (a_verified_must_wire).", flush=True)
    else:
        print("  WM lane did NOT clear the frozen bars (see per-condition flags).", flush=True)
    print("[done]", flush=True)
    return verdict


if __name__ == "__main__":
    main()
