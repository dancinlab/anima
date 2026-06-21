#!/usr/bin/env python3
"""
H_1554 — GABA × CLS — DISINHIBITION GATING (VIP→SST→PV context-cued write/read routing).

Census H_1553 RANK 1 (state/1553_gaba_family_census/CENSUS.md). The strongest ORTHOGONAL
GABA family — the lens where GABA can honestly go GREEN — after THREE falsifications in ONE
family (sparse-coding/capacity: H_1546 pattern-separation INERT · H_1551 capacity-mult STATIC ·
H_1552 non-stationary-load STATIC). Per a_break_the_wall §3, ≥3 falsifications in the SAME family
is NOT dry: a 🧱 needs ORTHOGONAL families censused; this is the top orthogonal pick.

WHY THIS IS ORTHOGONAL (and can GREEN honestly) — the fusion law:
  The 5 GREEN NTs (ACh mode-switch, DA replay-priority, NE boundary-flush, orexin true-timing,
  5-HT noise-reject) all share ONE green condition: a NT turns 🟢 inside two-store CLS iff its
  ADAPTIVE signal is load-bearing — the optimal operating point SHIFTS across regimes so no single
  grid-tuned FIXED setting captures the benefit, and an ablation freezing the adaptive signal to its
  best constant REVERTS the lift. GABA's 3 sparse-coding falsifications all failed the SAME way: the
  inhibitory benefit was MONOTONE/STATIC (more/less sparseness is just better regardless of regime),
  so a fixed-k baseline captured it and the adaptive arm was INERT.

  DISINHIBITION GATING is a DIFFERENT lever entirely. A VIP→SST→PV microcircuit (Pi/Kepecs 2013
  Nature 503:521; Williams & Holtmaat 2019 Nat Neurosci 22:1834 "Adaptive disinhibitory gating by
  VIP interneurons permits associative learning") SELECTIVELY OPENS a write/read PORT for a specific
  CONTEXT — a ROUTING operation, not a gain/density operation. Its benefit is intrinsically
  CONDITIONAL → the optimum provably SHIFTS: at LOW context-collision-rate ρ the gate should stay
  OPEN (route freely — closing it just loses recall), at HIGH ρ it should CLOSE (isolate colliding
  contexts to avoid cross-context overwrite). No fixed gate-policy is optimal across the ρ sweep →
  adaptive routing can beat best-fixed (same shape as NE boundary-flush / ACh encode-retrieve).

WHY DISTINCT FROM ACh encode/retrieve (load-bearing DECONFOUND, census-flagged):
  ACh's GREEN gate toggles the WHOLE store between an encode mode and a retrieve mode (a global
  temporal-phase switch). VIP disinhibition is SPATIALLY selective and context-CUED: different cue
  → different SUBSET of the store disinhibited, at the SAME time. The discriminating control runs an
  adversarial regime where the ACh phase-gate is ALREADY optimal (encode/retrieve perfectly separated,
  i.e. the H_1532 suppress_retrieval encode-mode is ON for every write) but contexts still collide
  WITHIN the encode phase — ACh cannot help (it is not spatial), disinhibition can (it routes by cue).
  Bar E freezes the ACh encode gate optimal-ON and re-measures: if the disinhib lift SURVIVES, it is a
  genuinely new ROUTING capability, not a re-skin of mode-switching.

THE HONEST RISK (census-flagged, load-bearing design constraint):
  If the H_1532 two-store CLS ALREADY routes by context (its store splits novel→fast / familiar→slow),
  the explicit gate may be redundant the way H_1546 sparse-separation was. So the regime must force
  WITHIN-store context collisions — multiple contexts sharing keys INSIDE the SAME fast store, which
  the novel/familiar fast/slow split does NOT separate. That is what makes the measurement able to SEE
  routing where the existing split cannot act.

p7: exact ground truth (the true (context,key)->value binding is known), NO LLM judge, NO perplexity,
NO loss term — every decision is a no-grad read of substrate state. $0 CPU. 3 seeds [11,22,33].
Frozen falsifier pre-registered in H_1554_FREEZE.txt BEFORE the scored run (NOT moved — c9).

R1 numpy DIRECTIONAL (host has no torch / hard-gate-1 a_engine_native_learning) — engine §GabaDisinhib
R2 deferred ING. REUSES the H_1284/H_1532 store machinery (MemStore/key_vec/FNV-1a/MARGIN) byte-exact.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from CORE/engine_cli.hexa / H_1284 / H_1532) ──
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1284/H_1532)
MARGIN = 0.05              # frozen lift bar (same as H_1284 / H_1532)
PRESENCE_BAR = 0.10        # PRESENCE bar at high-ρ (census A: disinhib − no-gate ≥ +0.10)


# ── byte-trigram FNV-1a key (VERBATIM from H_1284 / H_1532) ──────────────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1284/H_1532)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        tri = bs[i:i+3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── VAdaptField numpy mirror (byte-faithful to vadapt_field_step — H_1284/H_1532) ──
# A capacity-bounded prototype store: writes either SPLIT a new cell (novel key,
# recon-err>THRESH, capacity free) or REFINE the winner toward the key (LR pull),
# REBINDING the winner's stored value. A second fact on the SAME key finds the SAME
# winner cell and overwrites the bound value (= within-store interference).
class MemStore:
    def __init__(self, max_cells, abstain_margin, LR, THRESH):
        self.protos = []
        self.values = []
        self.lru = []
        self.max_cells = max_cells
        self.abstain_margin = abstain_margin
        self.LR = LR
        self.THRESH = THRESH
        self.tick = 0

    def _nearest(self, x):
        if not self.protos:
            return -1, 1e9, 1e9
        d = [np.linalg.norm(p - x) for p in self.protos]
        order = np.argsort(d)
        win = int(order[0]); bestd = d[win]
        second = d[int(order[1])] if len(d) > 1 else 1e9
        return win, bestd, second

    def write(self, x, value, suppress_retrieval=False):
        """vadapt_field_step write. suppress_retrieval = Hasselmo ACh encode-mode:
        the retrieval/match path is gated OFF, so a new fact is laid down in a FRESH
        cell instead of overwriting the winner it would otherwise refine."""
        self.tick += 1
        win, err, _ = self._nearest(x)
        if suppress_retrieval and len(self.protos) < self.max_cells:
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if win < 0 or (err > self.THRESH and len(self.protos) < self.max_cells):
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if err > self.THRESH and len(self.protos) >= self.max_cells:
            ev = int(np.argmin(self.lru))
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick
            return
        # REFINE: pull winner toward x, OVERWRITE its bound value (= interference)
        self.protos[win] = self.protos[win] + self.LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def recall(self, x):
        """nearest-cell fires; ABSTAIN (None) if recon-err > abstain margin."""
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── WITHIN-STORE context-collision fixture (exact ground truth) ───────────────
# K contexts each write B bindings into a SHARED store. With probability ρ a binding's
# KEY collides with a key already owned by ANOTHER context (different (ctx,key)->value
# than the colliding one). The CAPABILITY = recall the RIGHT (ctx,key)->value despite
# the cross-context key collisions WITHIN the same store (NOT separated by novel/familiar
# fast/slow split — that is the load-bearing distinction from the plain H_1532 routing).
def make_collision(K_CTX, B_PER, rho, rng):
    """Return a write-stream of (ctx, key_str, value, true_owner_value) and the recall
    probe list. rho = fraction of bindings whose key is SHARED with a prior context."""
    base_keys = [f"k{j:03d}" for j in range(B_PER)]   # B_PER distinct slots per context
    stream = []          # (ctx, key_str, value) write order (interleaved contexts)
    truth = {}           # (ctx, key_str) -> value  (the binding we must recall)
    pool_keys = []       # keys already issued (for collision draws)
    for c in range(K_CTX):
        for j in range(B_PER):
            # COLLIDE: with prob rho reuse a key already owned by an EARLIER context,
            # so the SAME key string maps to a DIFFERENT value in THIS context.
            if rho > 0.0 and pool_keys and rng.random() < rho:
                key_str = pool_keys[rng.integers(0, len(pool_keys))]
            else:
                key_str = f"ctx{c:02d}_{base_keys[j]}"
            val = f"v_{c:02d}_{j:03d}_{rng.integers(0, 99999):05d}"
            stream.append((c, key_str, val))
            truth[(c, key_str)] = val           # last write per (ctx,key) is the truth
            pool_keys.append(key_str)
    # interleave write order across contexts (so collisions actually interfere in time)
    rng.shuffle(stream)
    # re-derive truth as the LAST write per (ctx,key) in the shuffled order
    truth = {}
    for (c, k, v) in stream:
        truth[(c, k)] = v
    probes = list(truth.keys())
    return stream, truth, probes


def _ctx_cue(ctx):
    """context cue vector — the VIP gate's read. A unit vector keyed by context id only
    (orthogonal-ish across contexts), so the gate routes by CONTEXT not by the key/value."""
    return key_vec(f"CONTEXT_CUE_{ctx:02d}")


# ── DISINHIBITION GATE: context-cued write/read routing into per-context sub-stores ──
# The VIP gate, given a context cue and the CURRENT collision pressure, decides whether to
# OPEN (write into ONE shared substrate — cheap, fine when contexts rarely collide) or CLOSE
# (route the binding into a per-context substrate addressed by the cue — isolates colliding
# contexts). gate_open(pressure) is the policy; ADAPTIVE = pressure-driven, FIXED = constant.
class DisinhibCLS:
    """Two-store CLS (H_1532) wrapped with a VIP disinhibition gate. When the gate CLOSES it
    routes a write/read into a context-addressed sub-store (a disinhibited pyramidal subset);
    when OPEN it uses the shared fast store (H_1532 default). Routing ≠ gain: it changes WHICH
    substrate slot a binding lands in, conditioned on the context cue."""

    def __init__(self, max_cells, abstain, LR, THRESH, ach_encode=True):
        self.max_cells = max_cells; self.abstain = abstain
        self.LR = LR; self.THRESH = THRESH
        self.ach_encode = ach_encode          # H_1532 encode-mode (suppress_retrieval) on writes
        self.shared = MemStore(max_cells, abstain, LR, THRESH)   # OPEN port = shared fast store
        self.routed = {}                       # ctx -> MemStore (CLOSED port = isolated subset)

    def _sub(self, ctx):
        if ctx not in self.routed:
            self.routed[ctx] = MemStore(self.max_cells, self.abstain, self.LR, self.THRESH)
        return self.routed[ctx]

    def write(self, ctx, x, value, gate_closed, cue_route_ctx=None):
        """gate_closed True → route into the context's isolated sub-store (VIP disinhibits a
        context-specific subset). cue_route_ctx lets ABL/SHUFFLE permute WHICH context's subset
        gets disinhibited (a mis-routed gate). ach_encode controls suppress_retrieval (=ACh)."""
        if gate_closed:
            route_ctx = ctx if cue_route_ctx is None else cue_route_ctx
            self._sub(route_ctx).write(x, value, suppress_retrieval=self.ach_encode)
        else:
            self.shared.write(x, value, suppress_retrieval=self.ach_encode)

    def recall(self, ctx, x, gate_closed, cue_route_ctx=None):
        """recall routes the SAME way as write: a CLOSED gate reads the context's sub-store, an
        OPEN gate reads the shared store. (A binding written CLOSED is found only by reading the
        matching sub-store — that is what makes mis-routing collapse the lift.)"""
        if gate_closed:
            route_ctx = ctx if cue_route_ctx is None else cue_route_ctx
            return self._sub(route_ctx).recall(x)
        return self.shared.recall(x)


# ── ARMS ──────────────────────────────────────────────────────────────────────
def _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                gate_policy, ach_encode=True, cue_perm=None, rng=None):
    """Run one write-then-recall pass. gate_policy(pressure_signal) -> bool (CLOSE the gate).
    pressure_signal = a running estimate of recent collision pressure the gate reads.
    cue_perm: optional dict ctx->ctx remapping the ROUTE context (ABL=identity-frozen via
    fixed policy; SHUFFLE=random permutation of the cue→subset addressing)."""
    cls = DisinhibCLS(max_cells, abstain, LR, THRESH, ach_encode=ach_encode)
    # collision-pressure cue: fraction of recent keys already seen (a context-collision proxy
    # the VIP/SST circuit could read from cross-context coincidence detection). Online EMA.
    seen = set()
    pressure = 0.0
    ALPHA = 0.2
    gate_state = {}    # (ctx,key) -> gate_closed used at WRITE (recall must match)
    for (c, k, v) in stream:
        collided = 1.0 if k in seen else 0.0
        pressure = (1 - ALPHA) * pressure + ALPHA * collided
        seen.add(k)
        gate_closed = gate_policy(pressure)
        route_ctx = c if cue_perm is None else cue_perm.get(c, c)
        cls.write(c, key_vec(k), v, gate_closed, cue_route_ctx=route_ctx)
        gate_state[(c, k)] = (gate_closed, route_ctx)
    correct = 0
    for (c, k) in probes:
        gate_closed, route_ctx = gate_state[(c, k)]
        pred, _, _ = cls.recall(c, key_vec(k), gate_closed, cue_route_ctx=route_ctx)
        if pred == truth[(c, k)]:
            correct += 1
    return correct / max(1, len(probes))


# gate policies ----------------------------------------------------------------
def adaptive_policy(open_below=0.15):
    """ADAPTIVE VIP gate: CLOSE (route/isolate) when collision pressure is HIGH, stay OPEN
    (route freely) when pressure is LOW. The optimum threshold SHIFTS with ρ — this is the
    regime-shifting lever the fusion law rewards."""
    return lambda pressure: pressure >= open_below


def fixed_policy(close):
    """BEST-FIXED-GATE: a CONSTANT gate decision (always-open or always-closed), grid-tuned
    over the WHOLE ρ sweep — the honest strong baseline. If a single constant captures the
    benefit across all ρ, the routing is static-architecture (another fixed knob) → 🧱."""
    return lambda pressure: close


def run_arm(arm, rho, max_cells, LR, THRESH, abstain, seed, fixed_close=None):
    rng = np.random.default_rng(seed)
    stream, truth, probes = make_collision(K_CTX, B_PER, rho, rng)
    if arm == 'adaptive':
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           adaptive_policy(open_below=ADAPT_THR), ach_encode=True)
    if arm == 'no_gate':
        # H_1532 default: gate NEVER closes (always shared store, no routing).
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           fixed_policy(False), ach_encode=True)
    if arm == 'fixed':
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           fixed_policy(fixed_close), ach_encode=True)
    if arm == 'abl':
        # ABL: gate cue held CONSTANT → degenerates to the best FIXED gate (no adaptivity).
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           fixed_policy(fixed_close), ach_encode=True)
    if arm == 'shuffle':
        # CUE-SHUFFLE: collision-pressure cue permuted → the gate fires on a SCRAMBLED route
        # context (mis-addressed disinhibition). adaptive policy but cue→subset map permuted.
        rng2 = np.random.default_rng(seed + 7000)
        ctxs = list(range(K_CTX)); perm = ctxs.copy(); rng2.shuffle(perm)
        cue_perm = {c: perm[i] for i, c in enumerate(ctxs)}
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           adaptive_policy(open_below=ADAPT_THR), ach_encode=True,
                           cue_perm=cue_perm)
    if arm == 'adaptive_achfrozen':
        # DECONFOUND (E): ACh encode-mode held OPTIMAL-ON for EVERY write (encode/retrieve
        # perfectly separated), contexts still collide WITHIN the encode phase. If the
        # disinhib lift SURVIVES here, it is ROUTING not mode-switching (ACh cannot route).
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           adaptive_policy(open_below=ADAPT_THR), ach_encode=True)
    if arm == 'no_gate_achfrozen':
        return _run_stream(stream, truth, probes, max_cells, LR, THRESH, abstain,
                           fixed_policy(False), ach_encode=True)
    raise ValueError(arm)


def grid_tune_fixed(rho_sweep, max_cells, LR, THRESH, abstain, tune_seed):
    """BEST-FIXED-GATE = the best CONSTANT gate decision over the WHOLE ρ sweep, picked on a
    DISJOINT tune seed (anti-confound: adaptive must beat the strongest honest fixed gate)."""
    best = None
    for close in (False, True):
        accs = []
        for rho in rho_sweep:
            accs.append(run_arm('fixed', rho, max_cells, LR, THRESH, abstain,
                                 tune_seed, fixed_close=close))
        m = float(np.mean(accs))
        if best is None or m > best[0]:
            best = (m, close)
    return best[1], best[0]


# ── fixture / sweep constants ─────────────────────────────────────────────────
K_CTX = 6                  # contexts sharing the store
B_PER = 8                  # bindings per context (48 total)
ADAPT_THR = 0.15           # adaptive gate CLOSE threshold on collision-pressure EMA (frozen)
RHO_SWEEP = [0.0, 0.25, 0.5, 0.75, 1.0]
ABSTAIN0 = 0.45
TUNE_SEED = 7
SCORE_SEEDS = [11, 22, 33]
MAX_CELLS = max(8, int(K_CTX * B_PER * 1.5))   # ample capacity (interference, not capacity)
LR_star = LR0_ENGINE
TH_star = TH0_ENGINE


def main():
    # BEST-FIXED-GATE grid-tuned over the whole ρ sweep on a disjoint seed (honest baseline)
    fixed_close, fixed_tune_mean = grid_tune_fixed(RHO_SWEEP, MAX_CELLS, LR_star, TH_star,
                                                   ABSTAIN0, TUNE_SEED)

    per_seed = []
    # accumulate per-(rho) means across seeds for the sweep bars
    sweep = {rho: {'adaptive': [], 'no_gate': [], 'fixed': [], 'abl': [], 'shuffle': [],
                   'adaptive_achfrozen': [], 'no_gate_achfrozen': []} for rho in RHO_SWEEP}

    for seed in SCORE_SEEDS:
        row = {'seed': seed, 'rho': {}}
        for rho in RHO_SWEEP:
            adp = run_arm('adaptive', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed)
            ngt = run_arm('no_gate', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed)
            fxd = run_arm('fixed', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed,
                          fixed_close=fixed_close)
            abl = run_arm('abl', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed,
                          fixed_close=fixed_close)
            shf = run_arm('shuffle', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed)
            adf = run_arm('adaptive_achfrozen', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed)
            ndf = run_arm('no_gate_achfrozen', rho, MAX_CELLS, LR_star, TH_star, ABSTAIN0, seed)
            row['rho'][rho] = {'adaptive': round(adp, 4), 'no_gate': round(ngt, 4),
                               'fixed': round(fxd, 4), 'abl': round(abl, 4),
                               'shuffle': round(shf, 4),
                               'adaptive_achfrozen': round(adf, 4),
                               'no_gate_achfrozen': round(ndf, 4)}
            for k, val in (('adaptive', adp), ('no_gate', ngt), ('fixed', fxd),
                           ('abl', abl), ('shuffle', shf),
                           ('adaptive_achfrozen', adf), ('no_gate_achfrozen', ndf)):
                sweep[rho][k].append(val)
        per_seed.append(row)

    # ── ρ-mean per arm (across seeds) ─────────────────────────────────────────
    def rho_mean(arm, rho):
        return float(np.mean(sweep[rho][arm]))

    adaptive_mean = float(np.mean([rho_mean('adaptive', r) for r in RHO_SWEEP]))
    no_gate_mean = float(np.mean([rho_mean('no_gate', r) for r in RHO_SWEEP]))
    fixed_mean = float(np.mean([rho_mean('fixed', r) for r in RHO_SWEEP]))
    abl_mean = float(np.mean([rho_mean('abl', r) for r in RHO_SWEEP]))
    shuffle_mean = float(np.mean([rho_mean('shuffle', r) for r in RHO_SWEEP]))
    adf_mean = float(np.mean([rho_mean('adaptive_achfrozen', r) for r in RHO_SWEEP]))
    ndf_mean = float(np.mean([rho_mean('no_gate_achfrozen', r) for r in RHO_SWEEP]))

    rho_hi = RHO_SWEEP[-1]   # 1.0
    rho_lo = RHO_SWEEP[0]    # 0.0
    worst = min(no_gate_mean, fixed_mean)   # worst credible baseline over the sweep

    # ── FROZEN falsifier (pre-registered in H_1554_FREEZE.txt — NOT moved) ────
    #  A PRESENCE+SHIFT : (adaptive − best-fixed) ≥ ½·(adaptive − worst) across sweep
    #                     AND do-no-harm at low-ρ (adaptive ≥ no-gate − MARGIN at rho=0)
    #                     = the "optimum shifted" evidence (adaptive carries the majority).
    #  B DISTINCT       : no-gate FAILS at high-ρ (no_gate(hi) < adaptive(hi) − MARGIN)
    #                     AND best-fixed can't win BOTH ends (fixed loses ≥ MARGIN at one end).
    #  C ABL→best-fixed : adaptive − abl ≥ MARGIN (freezing cue reverts to fixed gate).
    #  D CUE-SHUFFLE    : adaptive − shuffle ≥ MARGIN (mis-routed disinhibition collapses).
    #  E ACh-FROZEN     : (adaptive_achfrozen − no_gate_achfrozen) ≥ MARGIN — lift survives
    #                     with the ACh encode/retrieve gate held optimal ⇒ ROUTING not mode-switch.
    gap_adaptive = adaptive_mean - worst
    earned = adaptive_mean - fixed_mean
    A_shift = earned >= 0.5 * gap_adaptive if gap_adaptive > 1e-9 else False
    A_noharm = rho_mean('adaptive', rho_lo) >= rho_mean('no_gate', rho_lo) - MARGIN
    A = A_shift and A_noharm

    B_nogate_fails_hi = rho_mean('no_gate', rho_hi) < rho_mean('adaptive', rho_hi) - MARGIN
    fixed_lo = rho_mean('fixed', rho_lo); fixed_hi = rho_mean('fixed', rho_hi)
    adp_lo = rho_mean('adaptive', rho_lo); adp_hi = rho_mean('adaptive', rho_hi)
    B_fixed_cant_win_both = (fixed_lo < adp_lo - MARGIN) or (fixed_hi < adp_hi - MARGIN)
    B = B_nogate_fails_hi and B_fixed_cant_win_both

    C = (adaptive_mean - abl_mean) >= MARGIN
    D = (adaptive_mean - shuffle_mean) >= MARGIN
    E = (adf_mean - ndf_mean) >= MARGIN

    A_presence_hi = (rho_mean('adaptive', rho_hi) - rho_mean('no_gate', rho_hi)) >= PRESENCE_BAR

    if A and B and C and D and E:
        verdict = 'GREEN'             # routing-optimum SHIFTS → adaptive carries the majority
    elif earned < 0.5 * gap_adaptive and gap_adaptive > 0 and (adaptive_mean - no_gate_mean) >= MARGIN:
        verdict = 'AMBER_KNOB'        # best-fixed captures ≥half → routing is a fixed knob (like 5-HT)
    elif (adaptive_mean - no_gate_mean) < MARGIN:
        verdict = 'WALL_REDUNDANT'    # gating ties no-gate → CLS already routes (like sparse)
    else:
        verdict = 'AMBER_KNOB'

    summary = {
        'capability': 'WITHIN-store context-collision routing: recall (ctx,key)->value under '
                      'cross-context key collisions a fast/slow split does NOT separate',
        'family': 'DISINHIBITION GATING (VIP→SST→PV context-cued write/read routing) — '
                  'ORTHOGONAL to the 3 sparse-coding walls (H_1546/1551/1552)',
        'K_CTX': K_CTX, 'B_PER': B_PER, 'RHO_SWEEP': RHO_SWEEP, 'ADAPT_THR': ADAPT_THR,
        'MAX_CELLS': MAX_CELLS, 'MARGIN': MARGIN, 'PRESENCE_BAR': PRESENCE_BAR,
        'LR_star': LR_star, 'TH_star': TH_star, 'seeds': SCORE_SEEDS,
        'best_fixed_gate_close': bool(fixed_close), 'best_fixed_tune_mean': round(fixed_tune_mean, 4),
        'per_seed': per_seed,
        'rho_means': {str(r): {a: round(rho_mean(a, r), 4) for a in
                      ('adaptive', 'no_gate', 'fixed', 'abl', 'shuffle',
                       'adaptive_achfrozen', 'no_gate_achfrozen')} for r in RHO_SWEEP},
        'adaptive_mean': round(adaptive_mean, 4),
        'no_gate_mean': round(no_gate_mean, 4),
        'best_fixed_mean': round(fixed_mean, 4),
        'abl_mean': round(abl_mean, 4),
        'shuffle_mean': round(shuffle_mean, 4),
        'adaptive_achfrozen_mean': round(adf_mean, 4),
        'no_gate_achfrozen_mean': round(ndf_mean, 4),
        'adaptive_minus_best_fixed': round(earned, 4),
        'adaptive_minus_worst': round(gap_adaptive, 4),
        'adaptive_minus_no_gate': round(adaptive_mean - no_gate_mean, 4),
        'adaptive_minus_abl': round(adaptive_mean - abl_mean, 4),
        'adaptive_minus_shuffle': round(adaptive_mean - shuffle_mean, 4),
        'achfrozen_lift': round(adf_mean - ndf_mean, 4),
        'bars': {
            'A_presence_shift': bool(A), 'A_shift_half_gap': bool(A_shift),
            'A_noharm_low_rho': bool(A_noharm), 'A_presence_hi_rho': bool(A_presence_hi),
            'B_distinct': bool(B), 'B_nogate_fails_hi': bool(B_nogate_fails_hi),
            'B_fixed_cant_win_both': bool(B_fixed_cant_win_both),
            'C_abl_reverts': bool(C), 'D_cue_shuffle_collapse': bool(D),
            'E_ach_frozen_survives': bool(E),
        },
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
