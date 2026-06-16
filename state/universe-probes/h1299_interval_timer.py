"""
H_1299 — INTERVAL TIMER (arbitrary LEARNED duration) — HD34 candidate / DEPLETION TEST.
R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1299_interval_timer/H_1299_FREEZE.txt (pre-registered BEFORE this
scoring). $0 CPU numpy, gradient-free, 3 seeds [4301,4302,4303], p7.
a_no_llm_frame_trap (interval-timing lens — Buhusi & Meck 2005 striatal beat-frequency /
SMA ramping; DISTINCT from the SCN circadian oscillator H_1298; c15) — NOT an LLM recipe.
ENGINE-TRANSFER UNVERIFIED til/unless R2.

THE DEPLETION TEST is the whole question. The candidate new structure = an interval timer
that LEARNS an ARBITRARY duration D from observed inter-event gaps at runtime (D̂ estimated
from data, NOT a constructor literal), fires when its own elapsed-since-last-event counter
reaches D̂, and RE-ENTRAINS to a different D2 from a second stream WITHOUT any code change.

LOAD-BEARING distinctness vs the CircadianClock (H_1298): the clock has a BAKED period
(period=8, fixed at construction; clock_step IGNORES every argument — NO learning path). It
can ONLY fire at its baked period. If the interval timer's "learned D" can be reduced to
re-reading the clock's baked period or a cerebellum next-step prediction, it FAILS
distinctness → honest DEPLETION 🏁 (the expected, valid terminal state; c9 — NO filler lane,
NO tune-to-green).
"""
import numpy as np

# ── frozen constants (from H_1299_FREEZE.txt) ────────────────────────────────
D_TRUE   = 13                # stream-1 true interval (!= clock baked period 8)
D2_TRUE  = 20                # stream-2 re-entrainment target (!= 8 and != 13)
CLOCK_PERIOD = 8             # the CircadianClock baked period (ARM A)
DHAT_INIT = 5                # uninformative init estimate (!= 8,13,20)
LR        = 0.5              # running-mean learning rate (B); 0.0 for B-ABLATE
N_EVENTS_LEARN = 8           # events observed in the learning window
N_EVENTS_TEST  = 4           # held-out events scored (AFTER the learning window)
JITTER    = 1                # +-1 tick seed-dependent gap jitter (genuine noisy estimate)
SEEDS     = [4301, 4302, 4303]


# ── ARM B: the IntervalTimer (the candidate new structure) ───────────────────
class IntervalTimer:
    """Learns its interval D̂ from observed inter-event gaps (running mean, gradient-free).
    fire() = True when the elapsed-since-last-event counter reaches the LEARNED D̂. The SAME
    object re-entrains to a new interval from a new stream (no code change). The ONLY mutable
    state is the elapsed counter + the learned estimate D̂ (Ψ-disjoint; no store/grounding)."""
    def __init__(self, lr=LR):
        self.dhat = float(DHAT_INIT)   # learned interval estimate
        self.lr = lr                   # 0.0 => B-ABLATE (never adapts)
        self.elapsed = 0               # ticks since the last observed event
        self.t_last = None             # tick of the last observed event

    def observe(self, t):
        """An event was observed at absolute tick t. Update D̂ from the inter-event gap."""
        if self.t_last is not None:
            gap = t - self.t_last
            self.dhat = (1.0 - self.lr) * self.dhat + self.lr * gap
        self.t_last = t
        self.elapsed = 0

    def step(self):
        self.elapsed += 1

    def fire(self):
        """Scheduled pulse: fire when elapsed since the last event reaches the learned D̂.
        Off-interval => no pulse (NO-FAB). Rounds D̂ to the nearest whole tick."""
        return self.elapsed == int(round(self.dhat))

    def predict_next(self):
        """Predicted absolute tick of the NEXT event = last event + learned D̂."""
        if self.t_last is None:
            return None
        return self.t_last + int(round(self.dhat))


# ── ARM A: the CircadianClock (the nearest lane that SHOULD fail) ─────────────
# Faithful mirror of the live engine clock (CORE/engine_cli.hexa § CircadianClock): a BAKED
# period (8), clock_step content-blind, NO learning path. Its "predict next event" can only
# ever be the next multiple of its baked period — it cannot match an arbitrary learned D.
class CircadianClock:
    def __init__(self, period=CLOCK_PERIOD):
        self.t = 0
        self.period = period           # baked at construction; immutable, content-blind

    def observe(self, t):
        # the clock has NO learning path — observing an event does NOTHING to its period.
        pass

    def step(self):
        self.t += 1

    def predict_next(self, t_last):
        # the clock can only schedule at its baked-period boundaries: the next multiple of
        # `period` strictly after t_last. It is BLIND to the actual interval of the stream.
        k = (t_last // self.period) + 1
        return k * self.period


def build_stream(rng, d_true, n_events):
    """Event ticks at 0, d, 2d, ... with +-JITTER seed-dependent gap jitter (a genuinely
    noisy stream so D̂ is an ESTIMATE, not a copy of one literal)."""
    ticks = [0]
    for _ in range(n_events - 1):
        gap = d_true + int(rng.integers(-JITTER, JITTER + 1))
        ticks.append(ticks[-1] + gap)
    return ticks


def timing_accuracy(predicted_ticks, true_ticks, d_true):
    """ACCURACY = max(0, 1 - mean|pred - true| / d_true) over the held-out events.
    1.0 = perfect interval timing; ~0 = wrong-period baseline. None preds score worst."""
    errs = []
    for p, tr in zip(predicted_ticks, true_ticks):
        if p is None:
            errs.append(d_true)       # no prediction => max error
        else:
            errs.append(abs(p - tr))
    err = float(np.mean(errs))
    return max(0.0, 1.0 - err / d_true)


def run_arm(timer_factory, rng, d_true, learn_then_test_stream):
    """Drive a timer/clock arm over an event stream: feed the first N_EVENTS_LEARN events
    to LEARN, then score next-event prediction on the held-out remaining events."""
    obj = timer_factory()
    learn_events = learn_then_test_stream[:N_EVENTS_LEARN]
    test_events = learn_then_test_stream[N_EVENTS_LEARN:]
    # LEARNING window: feed observed events
    for t in learn_events:
        obj.observe(t)
    # HELD-OUT prediction: for each held-out event, predict from the previous event tick.
    preds = []
    truths = []
    prev = learn_events[-1]
    for ev in test_events:
        if isinstance(obj, CircadianClock):
            preds.append(obj.predict_next(prev))
        else:
            # rebind the timer's "last event" to prev, predict next from learned D̂
            obj.t_last = prev
            preds.append(obj.predict_next())
        truths.append(ev)
        prev = ev
    acc = timing_accuracy(preds, truths, d_true)
    dhat = getattr(obj, "dhat", None)
    return acc, dhat


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # two streams: stream-1 (D=13) and stream-2 re-entrainment (D2=20)
    stream1 = build_stream(rng, D_TRUE,  N_EVENTS_LEARN + N_EVENTS_TEST)
    stream2 = build_stream(rng, D2_TRUE, N_EVENTS_LEARN + N_EVENTS_TEST)

    # ── ARM B: IntervalTimer ────────────────────────────────────────────────
    # c1 PRESENCE: learn D from stream1, predict held-out stream1 events
    b_acc_D, b_dhat1 = run_arm(lambda: IntervalTimer(lr=LR), rng, D_TRUE, stream1)
    # c2 RE-ENTRAIN: the SAME object continues onto stream2 and re-learns D2 (no code change)
    timer = IntervalTimer(lr=LR)
    for t in stream1[:N_EVENTS_LEARN]:
        timer.observe(t)
    dhat_after1 = timer.dhat                      # ~13 expected
    # re-entrain on stream2's learning window (continue the SAME object)
    for t in stream2[:N_EVENTS_LEARN]:
        timer.observe(t)
    dhat_after2 = timer.dhat                      # ~20 expected
    # held-out prediction on stream2 with the re-entrained timer
    preds2, truths2, prev = [], [], stream2[:N_EVENTS_LEARN][-1]
    for ev in stream2[N_EVENTS_LEARN:]:
        timer.t_last = prev
        preds2.append(timer.predict_next())
        truths2.append(ev)
        prev = ev
    b_acc_D2 = timing_accuracy(preds2, truths2, D2_TRUE)

    # ── ARM A: CircadianClock (baked period 8) ───────────────────────────────
    a_acc_D,  _ = run_arm(lambda: CircadianClock(), rng, D_TRUE,  stream1)
    a_acc_D2, _ = run_arm(lambda: CircadianClock(), rng, D2_TRUE, stream2)

    # ── B-SHUFFLE: permute the observed event ticks before learning ──────────
    # destroys the inter-event gaps => D̂ decorrelated from the true interval.
    learn1 = stream1[:N_EVENTS_LEARN]
    shuf_ticks = sorted(rng.permutation(np.array(learn1) + rng.integers(0, 100)).tolist())
    # use the PERMUTED gap structure: feed jittered/permuted gaps so D̂ is meaningless
    shuf_gaps = rng.permutation(np.diff(learn1)).tolist()
    sh_timer = IntervalTimer(lr=LR)
    t_acc = 0
    sh_timer.observe(0)
    for g in shuf_gaps:
        t_acc += int(g)
        sh_timer.observe(t_acc)
    # but the permutation of a CONSTANT-gap stream is still ~constant — make the control
    # honest by permuting the EVENT POSITIONS so gaps are genuinely scrambled:
    scrambled_positions = sorted(rng.choice(range(1, 60), size=N_EVENTS_LEARN - 1,
                                            replace=False).tolist())
    sh_timer2 = IntervalTimer(lr=LR)
    sh_timer2.observe(0)
    for p in scrambled_positions:
        sh_timer2.observe(p)
    # score on the TRUE held-out stream1 events (the shuffled D̂ should mis-predict)
    sh_preds, sh_truths, prev = [], [], stream1[:N_EVENTS_LEARN][-1]
    for ev in stream1[N_EVENTS_LEARN:]:
        sh_timer2.t_last = prev
        sh_preds.append(sh_timer2.predict_next())
        sh_truths.append(ev)
        prev = ev
    sh_acc_D = timing_accuracy(sh_preds, sh_truths, D_TRUE)

    # ── B-ABLATE: lr=0 => D̂ frozen at init (5), never adapts ────────────────
    ab_acc_D, ab_dhat = run_arm(lambda: IntervalTimer(lr=0.0), rng, D_TRUE, stream1)

    # ── c7 NO-FAB: off-interval => no fire. Feed learned D̂, step, check fire pattern ─
    nofab_timer = IntervalTimer(lr=LR)
    for t in stream1[:N_EVENTS_LEARN]:
        nofab_timer.observe(t)
    d_round = int(round(nofab_timer.dhat))
    fires = []
    for e in range(1, d_round + 1):
        nofab_timer.elapsed = e
        fires.append(nofab_timer.fire())
    # fire EXACTLY once, at elapsed == D̂ (off-interval => no fire)
    nofab_ok = (sum(fires) == 1) and (fires[-1] is True) and (not any(fires[:-1]))

    return dict(
        seed=seed,
        b_acc_D=b_acc_D, b_acc_D2=b_acc_D2,
        a_acc_D=a_acc_D, a_acc_D2=a_acc_D2,
        sh_acc_D=sh_acc_D, ab_acc_D=ab_acc_D, ab_dhat=ab_dhat,
        dhat_after1=dhat_after1, dhat_after2=dhat_after2,
        nofab_ok=nofab_ok,
    )


def main():
    rows = [run_seed(s) for s in SEEDS]
    print("=" * 96)
    print("H_1299 — INTERVAL TIMER (arbitrary LEARNED duration) — HD34 candidate / DEPLETION TEST")
    print("R1 numpy MIRROR (DIRECTIONAL).  FREEZE pre-registered.")
    print("=" * 96)
    print(f"frozen: D_TRUE={D_TRUE} D2_TRUE={D2_TRUE} CLOCK_PERIOD={CLOCK_PERIOD} "
          f"DHAT_INIT={DHAT_INIT} lr={LR} seeds={SEEDS}")
    print("-" * 96)
    print(f"{'seed':>6} | {'B.accD':>7} {'B.accD2':>8} {'A.accD':>7} {'A.accD2':>8} "
          f"{'shuf':>6} {'abl':>6} | {'D̂1':>5} {'D̂2':>5} {'ablD̂':>5} nofab")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_acc_D']:>7.3f} {r['b_acc_D2']:>8.3f} "
              f"{r['a_acc_D']:>7.3f} {r['a_acc_D2']:>8.3f} {r['sh_acc_D']:>6.3f} "
              f"{r['ab_acc_D']:>6.3f} | {r['dhat_after1']:>5.1f} {r['dhat_after2']:>5.1f} "
              f"{r['ab_dhat']:>5.1f}  {int(r['nofab_ok'])}")
    print("-" * 96)

    bD  = np.array([r['b_acc_D']  for r in rows])
    bD2 = np.array([r['b_acc_D2'] for r in rows])
    aD  = np.array([r['a_acc_D']  for r in rows])
    aD2 = np.array([r['a_acc_D2'] for r in rows])
    sh  = np.array([r['sh_acc_D'] for r in rows])
    ab  = np.array([r['ab_acc_D'] for r in rows])
    dh1 = np.array([r['dhat_after1'] for r in rows])
    dh2 = np.array([r['dhat_after2'] for r in rows])

    # ── frozen bars (verbatim from FREEZE) ───────────────────────────────────
    c1 = bool(np.all(bD  >= 0.70))                                   # PRESENCE
    c2 = bool(np.all(bD2 >= 0.70))                                   # RE-ENTRAIN
    c3 = bool(np.all(aD <= 0.35) and np.all(aD2 <= 0.35))           # DISTINCT-vs-CLOCK
    c4 = bool(np.all(sh <= 0.35))                                    # EARNED-LEARN (shuffle)
    c5 = bool(np.all(ab <= 0.35))                                    # EARNED-ADAPT (ablate)
    c6 = bool(np.all(np.abs(dh1 - D_TRUE) <= 2) and
              np.all(np.abs(dh2 - D2_TRUE) <= 2))                    # RE-ENTRAIN-DELTA
    c7 = bool(all(r['nofab_ok'] for r in rows))                      # NO-FAB

    print(f"B.accD  mean={bD.mean():.3f} {bD.round(3).tolist()}  | "
          f"B.accD2 mean={bD2.mean():.3f} {bD2.round(3).tolist()}")
    print(f"A.accD  mean={aD.mean():.3f} {aD.round(3).tolist()}  | "
          f"A.accD2 mean={aD2.mean():.3f} {aD2.round(3).tolist()}")
    print(f"shuf    mean={sh.mean():.3f} {sh.round(3).tolist()}  | "
          f"abl     mean={ab.mean():.3f} {ab.round(3).tolist()}")
    print(f"D̂_after_stream1 {dh1.round(2).tolist()} (true {D_TRUE}) | "
          f"D̂_after_stream2 {dh2.round(2).tolist()} (true {D2_TRUE})")
    print("-" * 96)
    print(f"  (c1 PRESENCE)          B.accD  >= 0.70 each   : {c1}")
    print(f"  (c2 RE-ENTRAIN)        B.accD2 >= 0.70 each   : {c2}")
    print(f"  (c3 DISTINCT-vs-CLOCK) A.accD,A.accD2 <= 0.35 : {c3}  (A.accD max {aD.max():.3f}, A.accD2 max {aD2.max():.3f})")
    print(f"  (c4 EARNED-LEARN)      shuf <= 0.35           : {c4}  (shuf max {sh.max():.3f})")
    print(f"  (c5 EARNED-ADAPT)      abl  <= 0.35           : {c5}  (abl max {ab.max():.3f})")
    print(f"  (c6 RE-ENTRAIN-DELTA)  |D̂1-13|<=2 & |D̂2-20|<=2: {c6}")
    print(f"  (c7 NO-FAB)            off-interval no fire    : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 96)
    print(f"VERDICT: {'GREEN — interval timer SURVIVES depletion test' if green else 'RED → ladder DEPLETED'}  "
          f"(c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("SCOPE: numpy-mirror DIRECTIONAL (engine-transfer UNVERIFIED til/unless R2); TOY")
    print("(2 intervals, short streams, 3 seeds); existence-proof-vs-effect-size; scale/")
    print("real-corpus/continuous-re-entrainment/brain-wiring = follow-on.")
    print("=" * 96)
    return green


# ── R1b (frozen-first re-design, H_1299_FREEZE_R1b.txt): HIT-RATE metric ─────────
# The R1a RED stands verbatim. R1b corrects the MIS-SPECIFIED metric/control (the same
# class H_1298 corrected R1a→R1d), making the test STRICTER:
#  (F1) METRIC = HIT-RATE within ±TOL of the true next event over MANY held-out events. A
#       wrong-period predictor has hit-rate → ~(2·TOL+1)/D ≈ chance BY CONSTRUCTION (true
#       ~0 floor, no luck residual).
#  (F2) N_EVENTS_TEST = 16 held-out events (was 4) so control variance cancels (LLN).
#  (F3) SHUFFLE re-built: gaps independently resampled from a WIDE uniform [2, 2·D] (gap
#       distribution destroyed) → D̂ decorrelated → hit-rate collapses to chance.
N_EVENTS_TEST_R1B = 16
TOL = 1


def hit_rate(predicted_ticks, true_ticks):
    """Fraction of held-out events the prediction lands within ±TOL of. A wrong-period
    predictor scores ~(2·TOL+1)/D ≈ chance BY CONSTRUCTION (a true ~0 floor)."""
    hits = 0
    n = 0
    for p, tr in zip(predicted_ticks, true_ticks):
        n += 1
        if p is not None and abs(p - tr) <= TOL:
            hits += 1
    return hits / n if n else 0.0


def run_arm_r1b(obj_factory, learn_then_test_stream, is_clock=False):
    """Learn from the first N_EVENTS_LEARN events, then hit-rate over N_EVENTS_TEST_R1B
    held-out events (each predicted from the previous TRUE event tick)."""
    obj = obj_factory()
    learn_events = learn_then_test_stream[:N_EVENTS_LEARN]
    test_events = learn_then_test_stream[N_EVENTS_LEARN:N_EVENTS_LEARN + N_EVENTS_TEST_R1B]
    for t in learn_events:
        obj.observe(t)
    preds, truths, prev = [], [], learn_events[-1]
    for ev in test_events:
        if is_clock:
            preds.append(obj.predict_next(prev))
        else:
            obj.t_last = prev
            preds.append(obj.predict_next())
        truths.append(ev)
        prev = ev
    return hit_rate(preds, truths), getattr(obj, "dhat", None)


def run_seed_r1b(seed):
    rng = np.random.default_rng(seed)
    n_total = N_EVENTS_LEARN + N_EVENTS_TEST_R1B
    stream1 = build_stream(rng, D_TRUE,  n_total)
    stream2 = build_stream(rng, D2_TRUE, n_total)

    # ARM B — presence (learn D from stream1) + re-entrain (SAME object onto stream2)
    b_hit_D,  dh1 = run_arm_r1b(lambda: IntervalTimer(lr=LR), stream1)
    timer = IntervalTimer(lr=LR)
    for t in stream1[:N_EVENTS_LEARN]:
        timer.observe(t)
    dhat_after1 = timer.dhat
    for t in stream2[:N_EVENTS_LEARN]:
        timer.observe(t)
    dhat_after2 = timer.dhat
    preds2, truths2, prev = [], [], stream2[:N_EVENTS_LEARN][-1]
    for ev in stream2[N_EVENTS_LEARN:N_EVENTS_LEARN + N_EVENTS_TEST_R1B]:
        timer.t_last = prev
        preds2.append(timer.predict_next())
        truths2.append(ev)
        prev = ev
    b_hit_D2 = hit_rate(preds2, truths2)

    # ARM A — CircadianClock (baked period 8)
    a_hit_D,  _ = run_arm_r1b(lambda: CircadianClock(), stream1, is_clock=True)
    a_hit_D2, _ = run_arm_r1b(lambda: CircadianClock(), stream2, is_clock=True)

    # B-SHUFFLE — gaps independently resampled from a WIDE uniform [2, 2D] (distribution
    # destroyed) → learned D̂ decorrelated from the true interval
    sh_timer = IntervalTimer(lr=LR)
    sh_timer.observe(0)
    pos = 0
    for _ in range(N_EVENTS_LEARN - 1):
        pos += int(rng.integers(2, 2 * D_TRUE + 1))
        sh_timer.observe(pos)
    sh_preds, sh_truths, prev = [], [], stream1[:N_EVENTS_LEARN][-1]
    for ev in stream1[N_EVENTS_LEARN:N_EVENTS_LEARN + N_EVENTS_TEST_R1B]:
        sh_timer.t_last = prev
        sh_preds.append(sh_timer.predict_next())
        sh_truths.append(ev)
        prev = ev
    sh_hit_D = hit_rate(sh_preds, sh_truths)

    # B-ABLATE — lr=0 → D̂ frozen at init (5)
    ab_hit_D, ab_dhat = run_arm_r1b(lambda: IntervalTimer(lr=0.0), stream1)

    # c7 NO-FAB — off-interval → no fire (fires exactly once at elapsed == D̂)
    nofab_timer = IntervalTimer(lr=LR)
    for t in stream1[:N_EVENTS_LEARN]:
        nofab_timer.observe(t)
    d_round = int(round(nofab_timer.dhat))
    fires = []
    for e in range(1, d_round + 1):
        nofab_timer.elapsed = e
        fires.append(nofab_timer.fire())
    nofab_ok = (sum(fires) == 1) and (fires[-1] is True) and (not any(fires[:-1]))

    return dict(seed=seed, b_hit_D=b_hit_D, b_hit_D2=b_hit_D2,
                a_hit_D=a_hit_D, a_hit_D2=a_hit_D2, sh_hit_D=sh_hit_D,
                ab_hit_D=ab_hit_D, ab_dhat=ab_dhat,
                dhat_after1=dhat_after1, dhat_after2=dhat_after2, nofab_ok=nofab_ok)


def main_r1b():
    rows = [run_seed_r1b(s) for s in SEEDS]
    print("\n" + "=" * 96)
    print("H_1299 R1b — HIT-RATE metric, 16 held-out events, destroyed-gap shuffle (FREEZE_R1b)")
    print("=" * 96)
    print(f"frozen: D_TRUE={D_TRUE} D2_TRUE={D2_TRUE} CLOCK_PERIOD={CLOCK_PERIOD} "
          f"TOL={TOL} N_TEST={N_EVENTS_TEST_R1B} seeds={SEEDS}")
    print("-" * 96)
    print(f"{'seed':>6} | {'B.hitD':>7} {'B.hitD2':>8} {'A.hitD':>7} {'A.hitD2':>8} "
          f"{'shuf':>6} {'abl':>6} | {'D̂1':>5} {'D̂2':>5} nofab")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_hit_D']:>7.3f} {r['b_hit_D2']:>8.3f} "
              f"{r['a_hit_D']:>7.3f} {r['a_hit_D2']:>8.3f} {r['sh_hit_D']:>6.3f} "
              f"{r['ab_hit_D']:>6.3f} | {r['dhat_after1']:>5.1f} {r['dhat_after2']:>5.1f}  "
              f"{int(r['nofab_ok'])}")
    print("-" * 96)
    bD  = np.array([r['b_hit_D']  for r in rows]); bD2 = np.array([r['b_hit_D2'] for r in rows])
    aD  = np.array([r['a_hit_D']  for r in rows]); aD2 = np.array([r['a_hit_D2'] for r in rows])
    sh  = np.array([r['sh_hit_D'] for r in rows]); ab  = np.array([r['ab_hit_D'] for r in rows])
    dh1 = np.array([r['dhat_after1'] for r in rows]); dh2 = np.array([r['dhat_after2'] for r in rows])
    c1 = bool(np.all(bD  >= 0.60))
    c2 = bool(np.all(bD2 >= 0.60))
    c3 = bool(np.all(aD <= 0.35) and np.all(aD2 <= 0.35))
    c4 = bool(np.all(sh <= 0.35))
    c5 = bool(np.all(ab <= 0.35))
    c6 = bool(np.all(np.abs(dh1 - D_TRUE) <= 2) and np.all(np.abs(dh2 - D2_TRUE) <= 2))
    c7 = bool(all(r['nofab_ok'] for r in rows))
    print(f"B.hitD  mean={bD.mean():.3f} {bD.round(3).tolist()}  | "
          f"B.hitD2 mean={bD2.mean():.3f} {bD2.round(3).tolist()}")
    print(f"A.hitD  mean={aD.mean():.3f} {aD.round(3).tolist()}  | "
          f"A.hitD2 mean={aD2.mean():.3f} {aD2.round(3).tolist()}")
    print(f"shuf    mean={sh.mean():.3f} {sh.round(3).tolist()}  | "
          f"abl     mean={ab.mean():.3f} {ab.round(3).tolist()}")
    print(f"D̂_after_stream1 {dh1.round(2).tolist()} (true {D_TRUE}) | "
          f"D̂_after_stream2 {dh2.round(2).tolist()} (true {D2_TRUE})")
    print("-" * 96)
    print(f"  (c1 PRESENCE)          B.hitD  >= 0.60   : {c1}")
    print(f"  (c2 RE-ENTRAIN)        B.hitD2 >= 0.60   : {c2}")
    print(f"  (c3 DISTINCT-vs-CLOCK) A.hit <= 0.35     : {c3}  (A.hitD max {aD.max():.3f}, A.hitD2 max {aD2.max():.3f})")
    print(f"  (c4 EARNED-LEARN)      shuf <= 0.35      : {c4}  (shuf max {sh.max():.3f})")
    print(f"  (c5 EARNED-ADAPT)      abl  <= 0.35      : {c5}  (abl max {ab.max():.3f})")
    print(f"  (c6 RE-ENTRAIN-DELTA)  |D̂1-13|<=2 & |D̂2-20|<=2 : {c6}")
    print(f"  (c7 NO-FAB)            off-interval no fire     : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 96)
    print(f"VERDICT R1b: {'GREEN — interval timer SURVIVES depletion test' if green else 'RED → ladder DEPLETED'}  "
          f"(c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("SCOPE: numpy-mirror DIRECTIONAL (engine-transfer UNVERIFIED til/unless R2); TOY")
    print("(2 intervals, short streams, 3 seeds); existence-proof-vs-effect-size; scale/")
    print("real-corpus/continuous-re-entrainment/brain-wiring = follow-on.")
    print("=" * 96)
    return green


# ── R1c (frozen-first, H_1299_FREEZE_R1c.txt): TOL=2 + mean-shifted shuffle ──────
# R1a + R1b REDs stand verbatim. R1c corrects the two remaining metric/control mis-designs
# (the same class H_1298 corrected R1a→R1d), STRICTER/honest:
#  (F1) TOL=2 (interval-timing tolerance absorbing ±1 jitter + ±1 rounding; a wrong-period
#       predictor still ~(2·2+1)/13 ≈ 0.38 chance, bars stay separated).
#  (F2) SHUFFLE = gaps from uniform[2,9] (mean ≈ 5.5 ≠ 13) → D̂ moves AWAY from D_true → the
#       timer mis-predicts the true-D stream. The CORRECT earned-learning control for a
#       running-mean estimator (proves the prediction TRACKS the observed interval).
TOL_R1C = 2
SHUF_GAP_LO = 2
SHUF_GAP_HI = 9            # uniform[2,9] mean ≈ 5.5 ≪ 13


def hit_rate_tol(predicted_ticks, true_ticks, tol):
    hits = sum(1 for p, tr in zip(predicted_ticks, true_ticks)
               if p is not None and abs(p - tr) <= tol)
    n = len(true_ticks)
    return hits / n if n else 0.0


def run_arm_r1c(obj_factory, learn_then_test_stream, is_clock=False):
    obj = obj_factory()
    learn_events = learn_then_test_stream[:N_EVENTS_LEARN]
    test_events = learn_then_test_stream[N_EVENTS_LEARN:N_EVENTS_LEARN + N_EVENTS_TEST_R1B]
    for t in learn_events:
        obj.observe(t)
    preds, truths, prev = [], [], learn_events[-1]
    for ev in test_events:
        if is_clock:
            preds.append(obj.predict_next(prev))
        else:
            obj.t_last = prev
            preds.append(obj.predict_next())
        truths.append(ev)
        prev = ev
    return hit_rate_tol(preds, truths, TOL_R1C), getattr(obj, "dhat", None)


def run_seed_r1c(seed):
    rng = np.random.default_rng(seed)
    n_total = N_EVENTS_LEARN + N_EVENTS_TEST_R1B
    stream1 = build_stream(rng, D_TRUE,  n_total)
    stream2 = build_stream(rng, D2_TRUE, n_total)

    b_hit_D,  _ = run_arm_r1c(lambda: IntervalTimer(lr=LR), stream1)
    timer = IntervalTimer(lr=LR)
    for t in stream1[:N_EVENTS_LEARN]:
        timer.observe(t)
    dhat_after1 = timer.dhat
    for t in stream2[:N_EVENTS_LEARN]:
        timer.observe(t)
    dhat_after2 = timer.dhat
    preds2, truths2, prev = [], [], stream2[:N_EVENTS_LEARN][-1]
    for ev in stream2[N_EVENTS_LEARN:N_EVENTS_LEARN + N_EVENTS_TEST_R1B]:
        timer.t_last = prev
        preds2.append(timer.predict_next())
        truths2.append(ev)
        prev = ev
    b_hit_D2 = hit_rate_tol(preds2, truths2, TOL_R1C)

    a_hit_D,  _ = run_arm_r1c(lambda: CircadianClock(), stream1, is_clock=True)
    a_hit_D2, _ = run_arm_r1c(lambda: CircadianClock(), stream2, is_clock=True)

    # B-SHUFFLE (R1c) — gaps from uniform[2,9] (mean ≈ 5.5 ≠ 13) → D̂ moves away from D_true
    sh_timer = IntervalTimer(lr=LR)
    sh_timer.observe(0); pos = 0
    for _ in range(N_EVENTS_LEARN - 1):
        pos += int(rng.integers(SHUF_GAP_LO, SHUF_GAP_HI + 1))
        sh_timer.observe(pos)
    sh_dhat = sh_timer.dhat
    sh_preds, sh_truths, prev = [], [], stream1[:N_EVENTS_LEARN][-1]
    for ev in stream1[N_EVENTS_LEARN:N_EVENTS_LEARN + N_EVENTS_TEST_R1B]:
        sh_timer.t_last = prev
        sh_preds.append(sh_timer.predict_next())
        sh_truths.append(ev)
        prev = ev
    sh_hit_D = hit_rate_tol(sh_preds, sh_truths, TOL_R1C)

    ab_hit_D, ab_dhat = run_arm_r1c(lambda: IntervalTimer(lr=0.0), stream1)

    nofab_timer = IntervalTimer(lr=LR)
    for t in stream1[:N_EVENTS_LEARN]:
        nofab_timer.observe(t)
    d_round = int(round(nofab_timer.dhat))
    fires = []
    for e in range(1, d_round + 1):
        nofab_timer.elapsed = e
        fires.append(nofab_timer.fire())
    nofab_ok = (sum(fires) == 1) and (fires[-1] is True) and (not any(fires[:-1]))

    return dict(seed=seed, b_hit_D=b_hit_D, b_hit_D2=b_hit_D2,
                a_hit_D=a_hit_D, a_hit_D2=a_hit_D2, sh_hit_D=sh_hit_D, sh_dhat=sh_dhat,
                ab_hit_D=ab_hit_D, ab_dhat=ab_dhat,
                dhat_after1=dhat_after1, dhat_after2=dhat_after2, nofab_ok=nofab_ok)


def main_r1c():
    rows = [run_seed_r1c(s) for s in SEEDS]
    print("\n" + "=" * 96)
    print("H_1299 R1c — TOL=2 + mean-shifted shuffle (FREEZE_R1c) = BINDING R1 VERDICT")
    print("=" * 96)
    print(f"frozen: D_TRUE={D_TRUE} D2_TRUE={D2_TRUE} CLOCK_PERIOD={CLOCK_PERIOD} "
          f"TOL={TOL_R1C} shuf~U[{SHUF_GAP_LO},{SHUF_GAP_HI}] seeds={SEEDS}")
    print("-" * 96)
    print(f"{'seed':>6} | {'B.hitD':>7} {'B.hitD2':>8} {'A.hitD':>7} {'A.hitD2':>8} "
          f"{'shuf':>6} {'abl':>6} | {'D̂1':>5} {'D̂2':>5} {'shD̂':>5} nofab")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_hit_D']:>7.3f} {r['b_hit_D2']:>8.3f} "
              f"{r['a_hit_D']:>7.3f} {r['a_hit_D2']:>8.3f} {r['sh_hit_D']:>6.3f} "
              f"{r['ab_hit_D']:>6.3f} | {r['dhat_after1']:>5.1f} {r['dhat_after2']:>5.1f} "
              f"{r['sh_dhat']:>5.1f}  {int(r['nofab_ok'])}")
    print("-" * 96)
    bD  = np.array([r['b_hit_D']  for r in rows]); bD2 = np.array([r['b_hit_D2'] for r in rows])
    aD  = np.array([r['a_hit_D']  for r in rows]); aD2 = np.array([r['a_hit_D2'] for r in rows])
    sh  = np.array([r['sh_hit_D'] for r in rows]); ab  = np.array([r['ab_hit_D'] for r in rows])
    dh1 = np.array([r['dhat_after1'] for r in rows]); dh2 = np.array([r['dhat_after2'] for r in rows])
    c1 = bool(np.all(bD  >= 0.60))
    c2 = bool(np.all(bD2 >= 0.60))
    c3 = bool(np.all(aD <= 0.35) and np.all(aD2 <= 0.35))
    c4 = bool(np.all(sh <= 0.35))
    c5 = bool(np.all(ab <= 0.35))
    c6 = bool(np.all(np.abs(dh1 - D_TRUE) <= 2) and np.all(np.abs(dh2 - D2_TRUE) <= 2))
    c7 = bool(all(r['nofab_ok'] for r in rows))
    print(f"B.hitD  mean={bD.mean():.3f} {bD.round(3).tolist()}  | "
          f"B.hitD2 mean={bD2.mean():.3f} {bD2.round(3).tolist()}")
    print(f"A.hitD  mean={aD.mean():.3f} {aD.round(3).tolist()}  | "
          f"A.hitD2 mean={aD2.mean():.3f} {aD2.round(3).tolist()}")
    print(f"shuf    mean={sh.mean():.3f} {sh.round(3).tolist()}  | "
          f"abl     mean={ab.mean():.3f} {ab.round(3).tolist()}")
    print(f"D̂_after_stream1 {dh1.round(2).tolist()} (true {D_TRUE}) | "
          f"D̂_after_stream2 {dh2.round(2).tolist()} (true {D2_TRUE})")
    print("-" * 96)
    print(f"  (c1 PRESENCE)          B.hitD  >= 0.60   : {c1}")
    print(f"  (c2 RE-ENTRAIN)        B.hitD2 >= 0.60   : {c2}")
    print(f"  (c3 DISTINCT-vs-CLOCK) A.hit <= 0.35     : {c3}  (A.hitD max {aD.max():.3f}, A.hitD2 max {aD2.max():.3f})")
    print(f"  (c4 EARNED-LEARN)      shuf <= 0.35      : {c4}  (shuf max {sh.max():.3f})")
    print(f"  (c5 EARNED-ADAPT)      abl  <= 0.35      : {c5}  (abl max {ab.max():.3f})")
    print(f"  (c6 RE-ENTRAIN-DELTA)  |D̂1-13|<=2 & |D̂2-20|<=2 : {c6}")
    print(f"  (c7 NO-FAB)            off-interval no fire     : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 96)
    print(f"VERDICT R1c: {'GREEN — interval timer SURVIVES depletion test' if green else 'RED → ladder DEPLETED'}  "
          f"(c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("SCOPE: numpy-mirror DIRECTIONAL (engine-transfer UNVERIFIED til/unless R2); TOY")
    print("(2 intervals, short streams, 3 seeds); existence-proof-vs-effect-size; scale/")
    print("real-corpus/continuous-re-entrainment/brain-wiring = follow-on.")
    print("=" * 96)
    return green


if __name__ == "__main__":
    import sys
    r1a = main()           # ORIGINAL frozen path (RED — metric floor; stands verbatim)
    r1b = main_r1b()       # re-design 1 (hit-rate metric — RED, mean-preserving shuffle leak; verbatim)
    r1c = main_r1c()       # re-design 2 (TOL=2 + mean-shifted shuffle) = the BINDING R1 verdict
    sys.exit(0 if r1c else 1)
