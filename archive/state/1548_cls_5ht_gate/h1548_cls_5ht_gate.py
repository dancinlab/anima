#!/usr/bin/env python3
"""
H_1548 — SEROTONIN × CLS: consolidation COMMIT-GATE (slow-store integrity under
contradicted / unconfirmed input).

A CAPABILITY reframe of 5-HT inside the H_1532 two-store CLS module — NOT a bar-move
of the H_1545 timing framing.

WHY A REFRAME, NOT A RE-TUNE (the fusion law of this batch, a_break_the_wall):
A neurotransmitter that ADDS a capability two-store CLS lacks earns 🟢 (ACh mode-switch
H_1541, DA value-rank H_1543, NE state-flush H_1544). A neurotransmitter that only
RE-TUNES an existing op stays 🟠 (H_1545 5-HT-TIMING: "when to sweep" just re-schedules
the consolidation period; a fixed period already captured 66.6% of the value). To make
5-HT GREEN we must NOT re-run timing — we must find the CAPABILITY 5-HT adds.

Biological 5-HT (Cools 2008; Dayan-Huys 2009) = behavioral INHIBITION / withholding an
action pending confirmation + aversive/error valence. The capability that maps onto CLS:
**a COMMIT-GATE that withholds UNCONFIRMED / CONTRADICTED fast-store bindings from
permanent commitment to the slow store** — so a transient binding, or one that is later
corrected, does not permanently corrupt the consolidated store.

THE EVENT 5-HT GETS TO ACT ON (distinct from H_1545's "when"):
The fast episodic store can hold a binding A->B that is LATER CONTRADICTED (A->B' arrives
before consolidation), plus NOISE bindings written once and never reconfirmed. A fixed
sweep schedule (H_1532 COMMIT-ALL) consolidates WHATEVER fast-store cell wins for key A at
the sweep boundary — that is the LAST-seen / nearest cell, i.e. it commits the stale or
unconfirmed entry and CANNOT selectively withhold it. The commit-gate decides WHETHER to
commit a binding AT ALL, pending confirmation:
  - commit a fast-store binding to slow ONLY if it has been RECONFIRMED (seen consistently
    >= CONFIRM_K times with the SAME value, no later contradiction outstanding);
  - WITHHOLD a binding that is contradicted (a different value for the same key arrived
    after it) or that is still unconfirmed (singleton, possible noise).

DISTINCT FROM DA (H_1543, load-bearing): DA ranks WHICH valid memories replay first
(a PRIORITY order over commit-worthy bindings). 5-HT decides WHETHER to commit AT ALL
pending confirmation — an error/valence GATE, not a priority RANK. On a contradiction
stream DA still commits the (high-priority but WRONG) last binding; the gate withholds it.

DISTINCT FROM H_1545 TIMING: H_1545's adaptive read controls the sweep PERIOD (when the
sweep fires); every binding present at the boundary is still committed. H_1548's gate
controls the sweep CONTENT (which bindings the sweep is allowed to commit). A fixed period
cannot withhold a contradicted binding no matter how it is scheduled.

p7: exact ground truth (the FINAL correct A->value binding is known per key), NO LLM judge,
NO perplexity, NO loss term — every decision is a no-grad read of substrate state. p8:
inference-time write = the engine's own tick. $0 CPU. 3 seeds. Frozen falsifier in
H_1548_FREEZE.txt. R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning) —
engine R2 deferred ING (§Ht5Gate). REUSES the H_1532 MemStore / key_vec / FNV-1a /
suppress_retrieval encode-mode / LRU eviction byte-for-byte.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from CORE/engine_cli.hexa / H_1284 / H_1532) ──
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1532)
MARGIN = 0.10              # frozen presence bar (capability margin, pre-registered)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1284) ───────────────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1532)."""
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


# ── VAdaptField numpy mirror (byte-faithful to vadapt_field_step — VERBATIM H_1532) ─
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
        """vadapt_field_step write (VERBATIM H_1532). suppress_retrieval = Hasselmo ACh
        encode-mode: lay the fact in a FRESH cell instead of refining the winner."""
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


# ── CONTRADICTION stream (exact ground truth) ─────────────────────────────────
# A stream of (key, value, kind) events.
#   - CONTRADICTED keys: A->B written, later A->B' (B' != B) written. The FINAL
#     correct binding is B' (the correction); the stale B must NOT be committed.
#   - CONFIRMED keys: A->V written CONFIRM_K times (reconfirmation) — commit-worthy.
#   - NOISE keys: written ONCE, never reconfirmed, never the truth — must NOT commit.
# Ground truth = the FINAL correct value per key (B' for contradicted, V for confirmed,
# and noise keys have NO truth — recall on them should ABSTAIN, not fabricate).
def make_contradiction_stream(n_confirmed, n_contradicted, n_noise, confirm_k, rng):
    events = []            # list of (key_str, value_str, kind)
    truth = {}             # key_str -> final correct value  (noise keys absent => no truth)

    confirmed_keys, contra_keys, noise_keys = [], [], []

    # CONFIRMED: A -> V, reconfirmed confirm_k times (same value).
    for i in range(n_confirmed):
        k = f"key_CF{i:03d}"
        v = f"val_{rng.integers(0, 99999):05d}"
        confirmed_keys.append(k); truth[k] = v
        for _ in range(confirm_k):
            events.append((k, v, 'confirmed'))

    # CONTRADICTED: A -> B (stale), then later A -> B' (correction, the truth),
    # each reconfirmed confirm_k times so the CORRECTION is itself commit-worthy but the
    # STALE binding sits in the fast store at sweep time and would be committed by a
    # blind sweep / a recency rule.
    for i in range(n_contradicted):
        k = f"key_CT{i:03d}"
        b = f"val_{rng.integers(0, 99999):05d}"
        bp = f"val_{rng.integers(0, 99999):05d}"
        while bp == b:
            bp = f"val_{rng.integers(0, 99999):05d}"
        contra_keys.append(k); truth[k] = bp     # the CORRECTION is the truth
        for _ in range(confirm_k):
            events.append((k, b, 'stale'))        # stale binding written first
        for _ in range(confirm_k):
            events.append((k, bp, 'correction'))  # correction later (the truth)

    # NOISE: A -> X written ONCE, never reconfirmed, never the truth (no truth entry).
    for j in range(n_noise):
        k = f"key_NZ{j:03d}"
        v = f"val_{rng.integers(0, 99999):05d}"
        noise_keys.append(k)
        events.append((k, v, 'noise'))

    # interleave deterministically by a fixed permutation of the event order
    perm = rng.permutation(len(events))
    events = [events[p] for p in perm]
    return events, truth, confirmed_keys, contra_keys, noise_keys


# ── confirmation bookkeeping (the substrate signal 5-HT reads) ────────────────
# As events stream into the fast store, the engine keeps a per-key confidence ledger:
#   count[key][value] = how many times (key->value) reconfirmed
#   last_val[key]     = most recent value seen for key  (recency)
# A binding (key->value) is CONFIRMED iff count>=CONFIRM_K AND it is the last value seen
# for that key (no later contradiction outstanding). This ledger IS the substrate signal
# the 5-HT commit-gate reads; SHUFFLE permutes it to prove the gate reads TRUE confirmation.
def build_confirmation_ledger(events):
    count = {}
    last_val = {}
    for k, v, _ in events:
        count.setdefault(k, {})
        count[k][v] = count[k].get(v, 0) + 1
        last_val[k] = v
    return count, last_val


# ── ARMS ──────────────────────────────────────────────────────────────────────
def _commit_pairs_for_arm(arm, events, count, last_val, confirm_k, rng=None,
                          shuffle_ledger=None):
    """Decide WHICH (key,value) pairs the consolidation sweep commits to the slow store.
    Returns a dict key->committed_value (a key may be committed at most once; we commit
    the value the arm's policy selects). This is the CONTENT of the sweep (H_1548), vs
    H_1545 which only controlled its TIMING."""
    # fast store holds, per key, the set of distinct values ever written + their counts.
    # The sweep visits each key once.
    committed = {}
    keys = list(count.keys())
    for k in keys:
        vals = count[k]                       # {value: times_seen}
        if arm == 'commit_all':
            # H_1532 default sweep: commit the NEAREST/winner cell = the last value
            # written for the key (the fast store's winning cell after all writes).
            committed[k] = last_val[k]
        elif arm == 'commit_recent':
            # commit the most-recently-seen value, no confirmation logic (recency rule).
            committed[k] = last_val[k]
        elif arm == 'ht5_gate':
            # 5-HT COMMIT-GATE: commit ONLY a value that is RECONFIRMED (count>=K) AND is
            # the last value seen (no later contradiction outstanding). Withhold otherwise.
            led = shuffle_ledger if shuffle_ledger is not None else (count, last_val)
            cnt, lv = led
            cands = cnt.get(k, {})
            best_v = lv.get(k)
            if best_v is not None and cands.get(best_v, 0) >= confirm_k:
                committed[k] = best_v         # confirmed + uncontradicted -> commit
            # else: WITHHOLD (unconfirmed singleton noise, or contradicted stale)
        elif arm == 'abl':
            # ABLATION: gate threshold -> 0 (CONFIRM_K effectively 0) => commit-all.
            committed[k] = last_val[k]
        else:
            raise ValueError(arm)
    return committed


def run_arm(arm, events, count, last_val, truth, noise_keys, confirm_k,
            max_cells, LR, THRESH, abstain, rng=None, shuffle=False):
    """Build the fast store from the stream, run the consolidation sweep under the arm's
    commit policy into the slow store, then score slow-store CORRECTNESS against the
    final ground truth + NO-FAB on noise keys."""
    # FAST episodic store: stream all events in (encode-mode, fresh cells).
    fast = MemStore(max_cells, abstain, LR, THRESH)
    for k, v, _ in events:
        fast.write(key_vec(k), v, suppress_retrieval=True)

    # SHUFFLE: permute the confirmation ledger across keys (the signal the gate reads is
    # scrambled => the gate fires its commit decision on the WRONG key's evidence).
    shuffle_ledger = None
    if shuffle:
        keys = list(count.keys())
        perm = rng.permutation(len(keys))
        sh_count = {keys[i]: count[keys[perm[i]]] for i in range(len(keys))}
        sh_last = {keys[i]: last_val[keys[perm[i]]] for i in range(len(keys))}
        shuffle_ledger = (sh_count, sh_last)

    committed = _commit_pairs_for_arm(arm, events, count, last_val, confirm_k,
                                      rng=rng, shuffle_ledger=shuffle_ledger)

    # SLOW store: write the committed bindings (consolidation), encode-mode fresh cells.
    slow = MemStore(max_cells, abstain, LR, THRESH)
    for k, v in committed.items():
        slow.write(key_vec(k), v, suppress_retrieval=True)

    return _score_slow_store(slow, truth, noise_keys)


def _score_slow_store(slow, truth, noise_keys):
    """Slow-store integrity:
      correctness = fraction of TRUTH keys whose slow recall == the final correct value
                    (a committed STALE/CONTRADICTED value counts as WRONG).
      no_fab      = fraction of NOISE keys on which the slow store ABSTAINS (None) —
                    i.e. did NOT fabricate a committed binding for never-reconfirmed noise."""
    correct = 0
    for k, v in truth.items():
        pred, _, _ = slow.recall(key_vec(k))
        if pred == v:
            correct += 1
    correctness = correct / max(1, len(truth))

    abst = 0
    for k in noise_keys:
        pred, _, _ = slow.recall(key_vec(k))
        if pred is None:
            abst += 1
    no_fab = abst / max(1, len(noise_keys))
    return correctness, no_fab


def main():
    N_CONFIRMED = 16
    N_CONTRADICTED = 16
    N_NOISE = 16
    CONFIRM_K = 2              # reconfirmation count for "confirmed"
    ABSTAIN0 = 0.45
    SCORE_SEEDS = [11, 22, 33]
    # ample capacity: interference/contradiction is the test, not capacity.
    TOTAL_KEYS = N_CONFIRMED + N_CONTRADICTED + N_NOISE
    MAX_CELLS = max(8, int(TOTAL_KEYS * 1.5))

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        events, truth, cf_k, ct_k, nz_k = make_contradiction_stream(
            N_CONFIRMED, N_CONTRADICTED, N_NOISE, CONFIRM_K, rng)
        count, last_val = build_confirmation_ledger(events)

        gate_c, gate_nf = run_arm('ht5_gate', events, count, last_val, truth, nz_k,
                                  CONFIRM_K, MAX_CELLS, LR0_ENGINE, TH0_ENGINE, ABSTAIN0)
        all_c, all_nf = run_arm('commit_all', events, count, last_val, truth, nz_k,
                                CONFIRM_K, MAX_CELLS, LR0_ENGINE, TH0_ENGINE, ABSTAIN0)
        rec_c, rec_nf = run_arm('commit_recent', events, count, last_val, truth, nz_k,
                                CONFIRM_K, MAX_CELLS, LR0_ENGINE, TH0_ENGINE, ABSTAIN0)
        abl_c, abl_nf = run_arm('abl', events, count, last_val, truth, nz_k,
                                CONFIRM_K, MAX_CELLS, LR0_ENGINE, TH0_ENGINE, ABSTAIN0)
        shf_c, shf_nf = run_arm('ht5_gate', events, count, last_val, truth, nz_k,
                                CONFIRM_K, MAX_CELLS, LR0_ENGINE, TH0_ENGINE, ABSTAIN0,
                                rng=np.random.default_rng(seed + 1000), shuffle=True)

        rows.append({
            'seed': seed,
            'gate_correct': round(gate_c, 4), 'gate_no_fab': round(gate_nf, 4),
            'commit_all_correct': round(all_c, 4), 'commit_all_no_fab': round(all_nf, 4),
            'commit_recent_correct': round(rec_c, 4), 'commit_recent_no_fab': round(rec_nf, 4),
            'abl_correct': round(abl_c, 4),
            'shuffle_correct': round(shf_c, 4),
            'gate_minus_all': round(gate_c - all_c, 4),
            'gate_minus_recent': round(gate_c - rec_c, 4),
        })

    def m(key):
        return float(np.mean([r[key] for r in rows]))

    gate_m, all_m, rec_m = m('gate_correct'), m('commit_all_correct'), m('commit_recent_correct')
    abl_m, shf_m = m('abl_correct'), m('shuffle_correct')
    gate_nf_m, all_nf_m, rec_nf_m = m('gate_no_fab'), m('commit_all_no_fab'), m('commit_recent_no_fab')

    # ── FROZEN falsifier (pre-registered in H_1548_FREEZE.txt) ────────────────
    #   A PRESENCE : gate_correct - commit_all_correct >= +MARGIN(0.10) on >=2/3 AND mean
    #   B DISTINCT : commit_all corrupted by stale (all < gate-MARGIN)
    #                AND commit_recent fooled (recent < gate-MARGIN) -> gate beats BOTH
    #   C ABL      : abl reverts to commit-all ( |abl - commit_all| < MARGIN )
    #                AND gate - abl >= MARGIN
    #   D SHUFFLE  : permuted confirmation collapses ( gate - shuffle >= MARGIN )
    #   E NO-FAB   : gate abstains on never-seen noise ( gate_no_fab >= 0.90 )
    n_win = sum(1 for r in rows if r['gate_minus_all'] >= MARGIN)
    A_presence = (n_win >= 2) and ((gate_m - all_m) >= MARGIN)
    B_distinct = (all_m < gate_m - MARGIN) and (rec_m < gate_m - MARGIN)
    C_abl = (abs(abl_m - all_m) < MARGIN) and ((gate_m - abl_m) >= MARGIN)
    D_shuffle = (gate_m - shf_m) >= MARGIN
    E_nofab = gate_nf_m >= 0.90

    if A_presence and B_distinct and C_abl and D_shuffle and E_nofab:
        verdict = 'GREEN'           # 5-HT adds the commit-gate CAPABILITY
    elif A_presence:
        verdict = 'AMBER_PARTIAL'   # lift present but a control already captures it
    else:
        verdict = 'WALL_HOLDS'      # commit-all/recent already captures slow-store integrity

    summary = {
        'capability': 'slow-store integrity under contradiction: commit only reconfirmed/'
                      'uncontradicted bindings, withhold stale/unconfirmed',
        'LR_star': LR0_ENGINE, 'TH_star': TH0_ENGINE, 'CONFIRM_K': CONFIRM_K,
        'N_CONFIRMED': N_CONFIRMED, 'N_CONTRADICTED': N_CONTRADICTED, 'N_NOISE': N_NOISE,
        'MAX_CELLS': MAX_CELLS, 'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'gate_correct_mean': round(gate_m, 4),
        'commit_all_correct_mean': round(all_m, 4),
        'commit_recent_correct_mean': round(rec_m, 4),
        'abl_correct_mean': round(abl_m, 4),
        'shuffle_correct_mean': round(shf_m, 4),
        'gate_no_fab_mean': round(gate_nf_m, 4),
        'commit_all_no_fab_mean': round(all_nf_m, 4),
        'commit_recent_no_fab_mean': round(rec_nf_m, 4),
        'gate_minus_all_mean': round(gate_m - all_m, 4),
        'gate_minus_recent_mean': round(gate_m - rec_m, 4),
        'gate_minus_abl_mean': round(gate_m - abl_m, 4),
        'gate_minus_shuffle_mean': round(gate_m - shf_m, 4),
        'n_wins_over_all+MARGIN': n_win,
        'A_presence': bool(A_presence), 'B_distinct': bool(B_distinct),
        'C_abl_reverts': bool(C_abl), 'D_shuffle_collapses': bool(D_shuffle),
        'E_no_fab': bool(E_nofab),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
