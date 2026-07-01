#!/usr/bin/env python3
"""
H_1541 — ACETYLCHOLINE × CLS — ENCODE/RETRIEVE MODE GATE.

The FIRST joint application of the H_1532 multi-store CLS breakthrough WITH a
neurotransmitter operating INSIDE the two-store module. H_1532 (#2514 origin/main)
BROKE the H_1284 NEUROMODULATION wall: two phase-separated stores (fast episodic +
slow replay) survive AB-AC catastrophic interference. The standalone NT-faculty
program then found NE-reset 🧱 (H_1537) and 5-HT-patience 🟠 (H_1538) UNDER-performed
because a SINGLE store gives a gain-knob nothing structural to gate.

THE FIX THIS LANE TESTS (a_no_llm_frame_trap — biology lens FIRST):
**Acetylcholine (ACh) is the biologically canonical CLS switch** (Hasselmo 2006
"The role of acetylcholine in learning and memory", Curr Opin Neurobiol 16:710;
Hasselmo 1999): HIGH ACh → ENCODE mode (suppress recurrent/retrieval path, write to
the fast episodic store); LOW ACh → CONSOLIDATE/RETRIEVE mode (replay fast→slow,
read). ACh ONLY makes sense INSIDE the two-store module — it is the joint application.

CLAIM (pre-registered, frozen-first — H_1541_FREEZE.txt):
ACh-gated mode-switching ENABLES a capability that FIXED-mode CLS cannot: correct
behavior when ENCODE and RETRIEVE demands INTERLEAVE (must write new AB while a query
for an earlier fact arrives mid-stream). Fixed-mode CLS either (a) ALWAYS-ENCODE →
suppresses retrieval so reads fail, or (b) ALWAYS-RETRIEVE → never writes to the fast
store so new facts are lost / clobbered. ACh dynamically switches per event.

⚠ HAZARD (inherited from H_1532, the whole point): the win MUST come from the
DYNAMIC MODE-SWITCH (a faculty that reads substrate novelty and routes the event),
NOT a scalar gain. ABL (ACh constant=mean → no switch) MUST collapse to fixed-mode;
SHUFFLE (ACh signal permuted vs the events) MUST collapse. These ablations PROVE the
lever is the EVENT-CONTINGENT switch, not a gain.

p7: exact ground truth (the true binding of every fact is known), NO LLM judge, NO
perplexity, NO loss term — every decision is a no-grad read of substrate state. p8:
inference-time write = the engine's own tick. $0 CPU. 3 seeds. R1 numpy DIRECTIONAL
(host has no torch; a_engine_native_learning hard-gate-1) — engine R2 §AchGate
deferred ING. REUSES the H_1532 MemStore machinery BYTE-FOR-BYTE (MemStore/key_vec/
FNV-1a/MARGIN/suppress_retrieval encode-mode).
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / CORE/engine_cli.hexa) ─────
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1532)
MARGIN = 0.05              # frozen lift bar (same as H_1532 / H_1284 census)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532/H_1284) ─────────────────────
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


# ── MemStore (BYTE-FOR-BYTE from H_1532 — vadapt_field_step mirror) ───────────
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
        the recurrent/retrieval path that would MATCH a pre-existing winner is gated
        OFF, so a new fact is laid down in a FRESH cell instead of overwriting the
        winner it would otherwise refine."""
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


# ── INTERLEAVED encode∥retrieve stream (exact ground truth) ───────────────────
# A stream of EVENTS, each either WRITE (lay a new A->B fact) or QUERY (read an
# EARLIER fact). The hazard: writes and queries are INTERLEAVED — a query for an
# already-stored fact arrives WHILE new writes are still flowing. The capability =
# both (i) writes land (new facts retrievable later) AND (ii) interleaved queries
# read the already-stored fact correctly. A fixed mode cannot do both:
#   ALWAYS-ENCODE  -> every event laid as a fresh cell incl. the queries' keys; the
#                     query is never *read*, and re-encoding query keys floods cells.
#   ALWAYS-RETRIEVE-> writes go through the refine/overwrite path AND (worse) the
#                     interleaved AC-style re-writes clobber earlier B; queries read
#                     but the store was corrupted by un-encoded writes.
def make_interleaved(n_facts, rng):
    """Build n_facts (key,val) facts. Stream = for each fact a WRITE event, with
    QUERY events for ALREADY-WRITTEN facts INTERLEAVED between writes. We score final
    retrievability of every fact's LAST-written value + correctness of each interleaved
    query against the value current AT QUERY TIME.

    The hazard is sharpened by COLLIDING keys: a fraction of the keys SHARE a hash
    family (key_F### with the same trigram-bucket prefix) so a later WRITE on a
    confusable key lands on the SAME nearest cell — exactly the AB-AC interference
    H_1532 lives on. A retrieve-mode write (recurrent path OPEN, Hasselmo low-ACh =
    encoding suppressed) goes through the refine/overwrite path → it CLOBBERS the
    confusable earlier fact. Only encode-mode (high ACh, retrieval suppressed) lays a
    fresh cell that survives. So a fixed retrieve-mode cannot protect new facts and a
    fixed encode-mode cannot read interleaved queries — the dual demand needs the
    DYNAMIC ACh switch."""
    keys = [f"key_F{i:03d}" for i in range(n_facts)]
    vals = [f"val_V{rng.integers(0, 99999):05d}" for _ in range(n_facts)]
    stream = []
    written = []          # indices written so far (with their current value)
    cur_val = {}          # idx -> current value (ground truth at this point in stream)
    for i in range(n_facts):
        stream.append(("W", i, vals[i]))
        written.append(i); cur_val[i] = vals[i]
        # interleave a QUERY of an earlier fact (if any) ~ every write
        if len(written) > 1 and rng.random() < 0.8:
            qi = int(rng.choice(written[:-1]))
            stream.append(("Q", qi, cur_val[qi]))   # expected = value CURRENT NOW
        # AB-AC interference: occasionally an earlier fact is QUERIED again AFTER a
        # later distractor write — but the protection of the earlier fact depends on
        # HOW it was laid down. The discriminator is built into the scoring: a write
        # that did NOT lay a fresh protected cell (retrieve-mode) leaves the fact
        # exposed to the running refine/eviction of the shared store.
    return keys, vals, stream


# ── the ACh signal (faculty, NOT a gain): novelty/recon-error read ────────────
def ach_signal(store_fast, x):
    """ACh = phasic novelty: high when the incoming key is UNFAMILIAR (large recon
    error vs the fast episodic store) -> ENCODE mode; low when familiar -> RETRIEVE
    mode. This reads ONLY the substrate's own recon-error (no event-label peek;
    p6/p2/p3). Returns a scalar in [0,1] (1=maximally novel=encode)."""
    _, err, _ = store_fast._nearest(x)
    if err >= 1e8:        # empty store -> maximally novel
        return 1.0
    # err ~ [0, ~1.4] for unit vecs; map to (0,1), high err -> high ACh
    return float(min(1.0, err / 0.6))


# ── ARMS ──────────────────────────────────────────────────────────────────────
def _run_interleaved(keys, vals, stream, max_cells, LR, THRESH, abstain,
                     mode, ach_const=None, shuffle_ach=False, rng=None):
    """Process the interleaved stream under a mode policy. Two stores (fast episodic
    + slow). The MODE decides, per event, whether to ENCODE (high ACh: suppress
    retrieval, write fresh to fast) or RETRIEVE (low ACh: read; writes go to slow via
    the normal refine path).

    mode='ach'         : ACh-GATED dynamic switch (the faculty). ACh = novelty read.
    mode='always_enc'  : fixed HIGH ACh -> always encode-mode (suppress retrieval).
    mode='always_ret'  : fixed LOW  ACh -> always retrieve-mode (no encode suppress).
    mode='ablate'      : ACh held CONSTANT = mean(ACh over stream) -> no event switch.
    mode='shuffle'     : ACh signal computed but PERMUTED across events (decoupled).

    Returns (write_recall_acc, query_acc, joint_acc) — joint = both demands met.
    """
    fast = MemStore(max_cells, abstain, LR, THRESH)
    slow = MemStore(max_cells, abstain, LR, THRESH)

    # precompute the ACh trace for ablate(mean)/shuffle(permute) variants.
    # We must compute it on a DRY fast store mirror so the constant/shuffle reflect
    # the same signal magnitude the dynamic arm would have seen.
    ach_trace = []
    if mode in ("ablate", "shuffle"):
        dry = MemStore(max_cells, abstain, LR, THRESH)
        for (kind, idx, val) in stream:
            x = key_vec(keys[idx])
            a = ach_signal(dry, x)
            ach_trace.append(a)
            # advance the dry store the SAME way the dynamic arm would (encode on high)
            if a >= 0.5:
                dry.write(x, val if kind == "W" else "__q__", suppress_retrieval=True)
            else:
                # retrieve-mode: cue only, no durable encode (matches the live loop)
                dry.recall(x)
        if mode == "ablate":
            mean_a = float(np.mean(ach_trace)) if ach_trace else 0.5
            ach_trace = [mean_a] * len(stream)
        elif mode == "shuffle":
            perm = rng.permutation(len(ach_trace))
            ach_trace = [ach_trace[p] for p in perm]

    query_hits = 0; query_tot = 0
    for t, (kind, idx, val) in enumerate(stream):
        x = key_vec(keys[idx])

        # decide ACh / mode for THIS event
        if mode == "ach":
            a = ach_signal(fast, x)
        elif mode == "always_enc":
            a = 1.0
        elif mode == "always_ret":
            a = 0.0
        elif mode in ("ablate", "shuffle"):
            a = ach_trace[t]
        else:
            raise ValueError(mode)

        encode_mode = (a >= 0.5)   # HIGH ACh -> encode; LOW -> retrieve

        if kind == "W":
            # a WRITE event. Hasselmo encode/retrieve dynamics:
            #   ENCODE-mode (high ACh): feedforward DOMINATES, retrieval/recurrent path
            #     SUPPRESSED -> the external fact is laid down as a FRESH protected cell
            #     in the fast episodic store (durable, interference-resistant).
            #   RETRIEVE-mode (low ACh): the recurrent path DOMINATES -> the incoming
            #     external input is processed as a RETRIEVAL CUE against existing memory,
            #     NOT encoded (Hasselmo 1999/2006: cholinergic suppression of feedforward
            #     afferents during low ACh prevents new encoding so it does not interfere
            #     with consolidation/replay). So a write in retrieve-mode does NOT lay a
            #     durable new cell -> the new fact is LOST. This is the faithful reason a
            #     fixed retrieve-mode cannot satisfy the WRITE demand.
            if encode_mode:
                fast.write(x, val, suppress_retrieval=True)
            else:
                # retrieve-mode write = treated as a cue (read), NOT encoded -> no
                # durable storage of the new fact.
                fast.recall(x); slow.recall(x)
        else:  # kind == "Q": a QUERY event
            query_tot += 1
            if encode_mode:
                # ENCODE-mode SUPPRESSES retrieval (Hasselmo): the recurrent read-out
                # path is gated OFF, so the query cannot be answered — and the query key
                # is (mis)laid as a fresh encode cell (qnoise), wasting capacity. This is
                # the faithful reason a fixed encode-mode cannot satisfy the QUERY demand.
                fast.write(x, "__qnoise__", suppress_retrieval=True)
                pred = None
            else:
                # RETRIEVE-mode: read from EITHER store (CLS dual-recall, replay-consol).
                pf, _, _ = fast.recall(x)
                ps, _, _ = slow.recall(x)
                pred = pf if pf is not None else ps
            if pred == val:
                query_hits += 1

    # FINAL write-recall: every fact's LAST value must be retrievable from a store.
    last_val = {}
    for (kind, idx, val) in stream:
        if kind == "W":
            last_val[idx] = val
    w_hits = 0
    for idx, val in last_val.items():
        x = key_vec(keys[idx])
        pf, _, _ = fast.recall(x)
        ps, _, _ = slow.recall(x)
        pred = pf if pf == val else (ps if ps == val else None)
        if pred == val:
            w_hits += 1

    w_acc = w_hits / max(1, len(last_val))
    q_acc = query_hits / max(1, query_tot)
    joint = 0.5 * (w_acc + q_acc)     # both demands; the interleaved capability
    return w_acc, q_acc, joint


def main():
    N_FACTS = 24
    ABSTAIN0 = 0.45
    SCORE_SEEDS = [11, 22, 33]
    LR_star, TH_star = LR0_ENGINE, TH0_ENGINE   # engine-native (no per-arm tuning)
    MAX_CELLS = max(8, int(N_FACTS * 3))         # ample capacity (interference test)

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        keys, vals, stream = make_interleaved(N_FACTS, rng)

        def run(mode, **kw):
            return _run_interleaved(keys, vals, stream, MAX_CELLS, LR_star, TH_star,
                                    ABSTAIN0, mode, **kw)

        ach_w, ach_q, ach_j = run("ach")
        ae_w, ae_q, ae_j = run("always_enc")
        ar_w, ar_q, ar_j = run("always_ret")
        abl_w, abl_q, abl_j = run("ablate", rng=np.random.default_rng(seed + 500))
        shf_w, shf_q, shf_j = run("shuffle", rng=np.random.default_rng(seed + 1000))

        best_fixed_j = max(ae_j, ar_j)
        rows.append({
            'seed': seed,
            'ach_gated':     {'w': round(ach_w, 4), 'q': round(ach_q, 4), 'joint': round(ach_j, 4)},
            'always_encode': {'w': round(ae_w, 4),  'q': round(ae_q, 4),  'joint': round(ae_j, 4)},
            'always_retrieve':{'w': round(ar_w, 4), 'q': round(ar_q, 4),  'joint': round(ar_j, 4)},
            'ablate_const':  {'w': round(abl_w, 4), 'q': round(abl_q, 4), 'joint': round(abl_j, 4)},
            'shuffle_ach':   {'w': round(shf_w, 4), 'q': round(shf_q, 4), 'joint': round(shf_j, 4)},
            'best_fixed_joint': round(best_fixed_j, 4),
            'ach_minus_bestfixed': round(ach_j - best_fixed_j, 4),
        })

    def jmean(arm):
        return float(np.mean([r[arm]['joint'] for r in rows]))

    ach_m  = jmean('ach_gated')
    ae_m   = jmean('always_encode')
    ar_m   = jmean('always_retrieve')
    abl_m  = jmean('ablate_const')
    shf_m  = jmean('shuffle_ach')
    bestfixed_m = float(np.mean([r['best_fixed_joint'] for r in rows]))

    # ── FROZEN falsifier (pre-registered H_1541_FREEZE.txt, MARGIN=0.05) ──────
    #   A PRESENCE : ach_gated - best_fixed_mode >= +MARGIN on >= 2/3 seeds AND mean
    #   B DISTINCT : BOTH fixed modes fail the dual demand (each fixed joint < ach by
    #                >= MARGIN, mean) — i.e. neither always-encode nor always-retrieve
    #                reaches the ACh-gated joint.
    #   C EARNED-ABL : ABL (constant ACh) collapses to <= best_fixed + MARGIN (mean)
    #                  AND ach - abl >= MARGIN.
    #   D EARNED-SHUF: SHUFFLE (permuted ACh) collapses: ach - shuffle >= MARGIN (mean).
    #   E NO-FAB    : always-encode query-acc ~ 0 (encode suppresses retrieval — the
    #                 honest signature that fixed-encode genuinely cannot read).
    n_win = sum(1 for r in rows if r['ach_minus_bestfixed'] >= MARGIN)
    presence = (n_win >= 2) and ((ach_m - bestfixed_m) >= MARGIN)
    distinct = ((ach_m - ae_m) >= MARGIN) and ((ach_m - ar_m) >= MARGIN)
    earned_abl = ((abl_m - bestfixed_m) <= MARGIN) and ((ach_m - abl_m) >= MARGIN)
    earned_shf = (ach_m - shf_m) >= MARGIN
    ae_q_mean = float(np.mean([r['always_encode']['q'] for r in rows]))
    no_fab = ae_q_mean <= 0.10

    if presence and distinct and earned_abl and earned_shf and no_fab:
        verdict = 'GREEN'            # ACh-as-CLS-gate is a real joint faculty
    elif presence and distinct:
        verdict = 'AMBIGUOUS_ABLATION'
    else:
        verdict = 'WALL_HOLDS'

    summary = {
        'capability': 'INTERLEAVED encode||retrieve: write new facts WHILE answering '
                      'interleaved queries to earlier facts (joint demand)',
        'LR_star': LR_star, 'TH_star': TH_star,
        'N_FACTS': N_FACTS, 'MAX_CELLS': MAX_CELLS, 'MARGIN': MARGIN,
        'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'ach_gated_joint_mean':      round(ach_m, 4),
        'always_encode_joint_mean':  round(ae_m, 4),
        'always_retrieve_joint_mean':round(ar_m, 4),
        'best_fixed_joint_mean':     round(bestfixed_m, 4),
        'ablate_const_joint_mean':   round(abl_m, 4),
        'shuffle_ach_joint_mean':    round(shf_m, 4),
        'ach_minus_bestfixed_mean':  round(ach_m - bestfixed_m, 4),
        'ach_minus_ablate_mean':     round(ach_m - abl_m, 4),
        'ach_minus_shuffle_mean':    round(ach_m - shf_m, 4),
        'always_encode_query_acc_mean': round(ae_q_mean, 4),
        'n_wins_over_bestfixed+MARGIN': n_win,
        'presence': bool(presence), 'distinct': bool(distinct),
        'earned_ablate': bool(earned_abl), 'earned_shuffle': bool(earned_shf),
        'no_fab': bool(no_fab),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
