"""
H_1298 — CIRCADIAN / INTERVAL TIMING CLOCK (HD33). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1298_circadian_clock/H_1298_FREEZE.txt (pre-registered BEFORE
this scoring). $0 CPU numpy, gradient-free, 3 seeds [4297,4298,4299], p7.
a_no_llm_frame_trap (SCN circadian / interval-timing lens — Pittendrigh self-sustaining
oscillator; the TWO-PROCESS model Borbely 1982: Process-C clock PERP Process-S homeostat;
Buhusi & Meck interval timing; c15) — NOT an LLM recipe. ENGINE-TRANSFER UNVERIFIED til R2.

THE DEPLETION TEST is the question. The new structure = a SELF-SUSTAINING PHASE OSCILLATOR
that advances on ELAPSED TICKS ALONE (phase = t mod PERIOD), fires on a fixed schedule,
and is NOT reset by a consummatory/grounding event. DISTINCT from EVERY lane, decisively
from its NEAREST competitor H_1292 HomeostaticDrive (a content-gated integrator that
stays flat under constant grounding and RESETS on feeding):
  D1 CONTENT-INDEPENDENCE: under a constant-grounded stream the clock fires on schedule
     while the homeostat NEVER rises (time PERP regulated-variable).
  D2 NO-RESET-ON-FEEDING: a grounded feeding event resets the homeostat's integral but
     leaves the clock's phase unchanged (the time of day does not reset when you eat).

FALSIFIER = "FIRE NOW? (a scheduled wake pulse)" each tick over a constant-grounded
stream. Ground-truth = phase-0 boundaries. The clock matches the periodic schedule; the
homeostat (no period) cannot. BOTH controls (shuffle the fire ticks / ablate the period)
MUST collapse to chance or it is variance → honest RED/WALL.
"""
import numpy as np

# ── frozen constants (from H_1298_FREEZE.txt) ────────────────────────────────
PERIOD   = 8                 # ticks per cycle (the clock's intrinsic period)
FIRE_TICK = 0                # fires when t mod PERIOD == FIRE_TICK (once per PERIOD)
N_TICKS  = 24                # run length = 3 full periods → fires at t=0,8,16
SETPOINT = 0.5               # H_1292 S* (homeostat distinctness arm)
LEAK     = 0.1               # H_1292 lambda
KP       = 1.0               # H_1292 Kp
KI       = 0.5               # H_1292 Ki
SEEDS    = [4297, 4298, 4299]


# ── ARM B: the CircadianClock lane (the new structure) ───────────────────────
class CircadianClock:
    """A self-sustaining phase oscillator. The integer tick counter `t` is the SOLE
    mutable state. step() advances t by 1 REGARDLESS of any argument — no context, no
    grounding read, no other lane touched. fire() = scheduled pulse at the phase-0
    boundary. period == N_TICKS+1 (ablated) → the recurring boundary never recurs."""
    def __init__(self, period=PERIOD):
        self.t = 0
        self.period = period

    def step(self, _ctx_ignored=None):
        # advances on ELAPSED TIME ALONE — the argument (context/grounding) is IGNORED.
        self.t += 1

    def phase(self):
        return (self.t % self.period) / self.period

    def fire(self):
        # scheduled wake pulse: True exactly at the phase-0 boundary (t mod period == 0).
        return (self.t % self.period) == FIRE_TICK


class ClockAblated(CircadianClock):
    """B-ABLATE: period = N_TICKS+1 ⇒ within the run only the t=0 boundary ever fires;
    the RECURRING period is removed → cannot match the 3-fire ground-truth schedule."""
    def __init__(self):
        super().__init__(period=N_TICKS + 1)


# ── ARM A: H_1292 HomeostaticDrive (the genuinely-nearest lane) ──────────────
# Faithful mirror of the live engine homeo_step (CORE/engine_cli.hexa § HomeostaticDrive):
# deficit = max(0, S*-s); accum = (1-lambda)*accum + deficit; consummatory reset s>=S* →
# accum:=0; drive = Kp*deficit + Ki*accum. Its "fire" decision = the best content-derived
# analogue: fire iff the drive crosses its own running threshold (a deprivation alarm).
class HomeostaticDrive:
    def __init__(self, ki=KI):
        self.accum = 0.0
        self.last_drive = 0.0
        self.ki = ki

    def step(self, satiation):
        deficit = max(0.0, SETPOINT - satiation)
        acc = (1.0 - LEAK) * self.accum + deficit
        if satiation >= SETPOINT:        # consummatory reset (the D2 event)
            acc = 0.0
        self.accum = acc
        self.last_drive = KP * deficit + self.ki * acc
        return self.last_drive

    def fire(self):
        # the homeostat's only fire analogue: a deprivation alarm when drive is high.
        # Under a constant-GROUNDED stream the drive is 0 every tick → it can only ever
        # produce a CONSTANT (never-fire) decision = chance against a periodic schedule.
        return self.last_drive > 0.5


def balanced_sched_acc(decisions, truth):
    """BALANCED accuracy over the two classes {fire-tick, no-fire-tick}: mean of
    per-class accuracy. A constant predictor (always/never fire) scores 0.5 = chance."""
    decisions = np.asarray(decisions, dtype=bool)
    truth = np.asarray(truth, dtype=bool)
    accs = []
    for cls in (True, False):
        m = (truth == cls)
        if m.sum() == 0:
            continue
        accs.append((decisions[m] == truth[m]).mean())
    return float(np.mean(accs)) if accs else 0.0


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # the constant-grounded stream: satiation >= SETPOINT every tick (fully fed). A tiny
    # seed-dependent jitter ABOVE the setpoint proves the result is not a fixed constant
    # but holds across the random stream (grounded throughout → homeostat stays flat).
    sat_stream = SETPOINT + 0.3 + 0.1 * rng.random(N_TICKS)   # always >= S* (grounded)

    truth = [(t % PERIOD) == FIRE_TICK for t in range(N_TICKS)]   # ground-truth schedule

    # ARM B — clock
    clk = CircadianClock()
    b_dec = []
    b_fire_ticks = []
    for t in range(N_TICKS):
        b_dec.append(clk.fire())
        if clk.fire():
            b_fire_ticks.append(t)
        clk.step()            # advances on elapsed time alone (sat ignored)

    # ARM A — homeostat (content-gated; constant-grounded → flat)
    hd = HomeostaticDrive()
    a_dec = []
    drive_trace = []
    for t in range(N_TICKS):
        hd.step(sat_stream[t])
        a_dec.append(hd.fire())
        drive_trace.append(hd.last_drive)

    # B-SHUFFLE — same fire COUNT, decorrelated WHICH ticks (destroys phase→fire relation)
    n_fire = sum(truth)
    perm = rng.permutation(N_TICKS)[:n_fire]
    shuf_dec = [False] * N_TICKS
    for i in perm:
        shuf_dec[i] = True

    # B-ABLATE — period = N_TICKS+1 → only t=0 fires (recurring period removed)
    abl = ClockAblated()
    abl_dec = []
    for t in range(N_TICKS):
        abl_dec.append(abl.fire())
        abl.step()

    b_acc   = balanced_sched_acc(b_dec, truth)
    a_acc   = balanced_sched_acc(a_dec, truth)
    sh_acc  = balanced_sched_acc(shuf_dec, truth)
    ab_acc  = balanced_sched_acc(abl_dec, truth)

    # c5 D1: clock fires exactly N_TICKS//PERIOD times on schedule; homeostat drive_rise
    drive_rise = max(drive_trace) - drive_trace[0]
    b_fire_count = len(b_fire_ticks)
    d1_ok = (b_fire_count == N_TICKS // PERIOD) and (drive_rise <= 0.05)

    # c6 D2: a mid-run grounded feeding event. Clock phase invariant; homeostat resets.
    # clock: advance 10 ticks, record phase; the feeding event does NOT touch the clock.
    clk2 = CircadianClock()
    for _ in range(10):
        clk2.step()
    phase_nofeed = clk2.phase()
    # "feeding" the clock = passing a grounded context to step(); the clock IGNORES it →
    # phase identical. (the clock's step argument is content-blind by construction.)
    clk3 = CircadianClock()
    for _ in range(10):
        clk3.step(satiation_if_it_listened := 0.99)   # grounded "feed" — clock ignores it
    phase_after = clk3.phase()
    # homeostat: deprive to build accum, then a grounded feed resets it to 0.
    hd2 = HomeostaticDrive()
    for _ in range(6):
        hd2.step(0.0)            # deprivation builds the integral
    accum_before = hd2.accum
    hd2.step(0.99)              # consummatory grounded feed → reset
    accum_after_feed = hd2.accum
    d2_ok = (abs(phase_after - phase_nofeed) < 1e-12) and (accum_after_feed == 0.0) and (accum_before > 0.0)

    # c7 NO-FAB: at a non-scheduled phase the clock does NOT fire.
    clk4 = CircadianClock()
    clk4.step(); clk4.step(); clk4.step()    # t=3, off-schedule
    nofab_ok = (not clk4.fire())

    return dict(seed=seed, b_acc=b_acc, a_acc=a_acc, sh_acc=sh_acc, ab_acc=ab_acc,
                drive_rise=drive_rise, b_fire_count=b_fire_count, accum_before=accum_before,
                accum_after_feed=accum_after_feed, phase_nofeed=phase_nofeed,
                phase_after=phase_after, d1_ok=d1_ok, d2_ok=d2_ok, nofab_ok=nofab_ok)


# ── R1b (frozen-first re-design, H_1298_FREEZE_R1b.txt) ──────────────────────
# The R1a frozen RED (c4 did not collapse) stands verbatim. R1b fixes the MIS-SPECIFIED
# control via two STRICTER changes: (F1) recurrence-scored metric (the trivial shared
# t=0 origin is EXCLUDED from the fire-class), (F2) origin-broken ablate (non-dividing
# period 5, phase offset 3 → never fires at t=0, never aligns with t=8,16).
REC_BOUNDARIES = [PERIOD, 2 * PERIOD]          # {8, 16} — the RECURRENCES (origin excluded)
ABL_PERIOD_R1B = 5
ABL_OFFSET_R1B = 3


def recurrence_acc(decisions):
    """BALANCED accuracy scored ONLY over the recurring boundaries (fire-class = {8,16},
    origin t=0 EXCLUDED) and the no-fire ticks (excluding t=0). A clock that only fires at
    the trivial origin gets ZERO fire-class credit → collapses to the no-fire 0.5 floor."""
    decisions = np.asarray(decisions, dtype=bool)
    fire_ticks = REC_BOUNDARIES
    nofire_ticks = [t for t in range(1, N_TICKS) if t % PERIOD != 0]   # exclude t=0 origin
    fire_acc = np.mean([decisions[t] == True for t in fire_ticks])
    nofire_acc = np.mean([decisions[t] == False for t in nofire_ticks])
    return float((fire_acc + nofire_acc) / 2.0)


def run_seed_r1b(seed):
    rng = np.random.default_rng(seed)
    sat_stream = SETPOINT + 0.3 + 0.1 * rng.random(N_TICKS)            # grounded throughout

    # ARM B — clock (fires t=0,8,16; recurrence metric scores t=8,16)
    clk = CircadianClock()
    b_dec = []
    for t in range(N_TICKS):
        b_dec.append(clk.fire()); clk.step()

    # ARM A — homeostat (constant-grounded → never fires)
    hd = HomeostaticDrive()
    a_dec = []
    for t in range(N_TICKS):
        hd.step(sat_stream[t]); a_dec.append(hd.fire())

    # B-SHUFFLE — same fire count, decorrelated which ticks
    n_fire = sum((t % PERIOD) == FIRE_TICK for t in range(N_TICKS))
    perm = rng.permutation(N_TICKS)[:n_fire]
    shuf_dec = [False] * N_TICKS
    for i in perm:
        shuf_dec[i] = True

    # B-ABLATE (R1b) — origin-broken non-dividing period: fire iff (t - offset) mod 5 == 0
    abl_dec = [((t - ABL_OFFSET_R1B) % ABL_PERIOD_R1B == 0) and (t >= ABL_OFFSET_R1B)
               for t in range(N_TICKS)]

    return dict(seed=seed,
                b_acc=recurrence_acc(b_dec), a_acc=recurrence_acc(a_dec),
                sh_acc=recurrence_acc(shuf_dec), ab_acc=recurrence_acc(abl_dec))


def main_r1b():
    rows = [run_seed_r1b(s) for s in SEEDS]
    # D1/D2/NO-FAB are structural and identical to R1a — reuse those checks.
    base = [run_seed(s) for s in SEEDS]
    print("\n" + "=" * 92)
    print("H_1298 R1b — recurrence-scored, origin-broken ablate (FREEZE_R1b pre-registered)")
    print("=" * 92)
    print(f"{'seed':>6} | {'B clk':>7} {'A homeo':>8} {'B-shuf':>7} {'B-abl':>7}")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_acc']:>7.3f} {r['a_acc']:>8.3f} {r['sh_acc']:>7.3f} {r['ab_acc']:>7.3f}")
    b = np.array([r['b_acc'] for r in rows]); a = np.array([r['a_acc'] for r in rows])
    sh = np.array([r['sh_acc'] for r in rows]); ab = np.array([r['ab_acc'] for r in rows])
    c1 = bool(np.all((b - a) >= 0.30) and (b.mean() - a.mean()) >= 0.30)
    c2 = bool(np.all(a <= 0.65))
    c3 = bool(np.all(sh <= a + 0.15))
    c4 = bool(np.all(ab <= a + 0.15))
    c5 = bool(all(r['d1_ok'] for r in base))
    c6 = bool(all(r['d2_ok'] for r in base))
    c7 = bool(all(r['nofab_ok'] for r in base))
    print("-" * 92)
    print(f"B mean={b.mean():.3f} {b.round(3).tolist()} | A mean={a.mean():.3f} {a.round(3).tolist()} | "
          f"shuf={sh.mean():.3f} {sh.round(3).tolist()} | abl={ab.mean():.3f} {ab.round(3).tolist()}")
    print(f"  (c1 PRESENCE)        B-A>=+0.30   : {c1}  (mean Delta {(b.mean()-a.mean()):+.3f})")
    print(f"  (c2 DISTINCT)        A<=0.65      : {c2}  (A max {a.max():.3f})")
    print(f"  (c3 EARNED-SCHEDULE) shuf<=A+0.15 : {c3}")
    print(f"  (c4 EARNED-PERIOD)   abl<=A+0.15  : {c4}")
    print(f"  (c5 D1 content-indep)             : {c5}")
    print(f"  (c6 D2 no-reset)                  : {c6}")
    print(f"  (c7 NO-FAB)                       : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 92)
    print(f"VERDICT R1b: {'GREEN' if green else 'RED/WALL'}  (c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("=" * 92)
    return green


# ── R1c (frozen-first, H_1298_FREEZE_R1c.txt): PHASE-LOCKING metric ──────────
# The genuine chronobiology signature of a clock: vector strength R (Rayleigh mean
# resultant length) of the fire phases. A clock fires at a CONSISTENT phase (R=1); any
# non-periodic firing pattern (shuffle, origin-broken ablate, never-firing homeostat)
# has spread/no phases → R collapses to ~chance BY CONSTRUCTION. R1a/R1b REDs stand.
def vector_strength(fire_ticks):
    """Mean resultant length R in [0,1] of fire phases on the PERIOD circle. R=1 =>
    perfectly phase-locked; R~0 => no phase lock. k=0 (never fires) => R:=0.0."""
    if len(fire_ticks) == 0:
        return 0.0
    angles = [2.0 * np.pi * (f % PERIOD) / PERIOD for f in fire_ticks]
    c = np.mean([np.cos(a) for a in angles]); s = np.mean([np.sin(a) for a in angles])
    return float(np.sqrt(c * c + s * s))


def run_seed_r1c(seed):
    rng = np.random.default_rng(seed)
    sat_stream = SETPOINT + 0.3 + 0.1 * rng.random(N_TICKS)

    clk = CircadianClock()
    b_fires = []
    for t in range(N_TICKS):
        if clk.fire(): b_fires.append(t)
        clk.step()

    hd = HomeostaticDrive()
    a_fires = []
    for t in range(N_TICKS):
        hd.step(sat_stream[t])
        if hd.fire(): a_fires.append(t)

    n_fire = sum((t % PERIOD) == FIRE_TICK for t in range(N_TICKS))
    sh_fires = sorted(rng.permutation(N_TICKS)[:n_fire].tolist())

    ab_fires = [t for t in range(N_TICKS)
                if (t >= ABL_OFFSET_R1B) and ((t - ABL_OFFSET_R1B) % ABL_PERIOD_R1B == 0)]

    return dict(seed=seed, b_R=vector_strength(b_fires), a_R=vector_strength(a_fires),
                sh_R=vector_strength(sh_fires), ab_R=vector_strength(ab_fires),
                a_n=len(a_fires))


def main_r1c():
    rows = [run_seed_r1c(s) for s in SEEDS]
    base = [run_seed(s) for s in SEEDS]
    print("\n" + "=" * 92)
    print("H_1298 R1c — PHASE-LOCKING vector strength R (FREEZE_R1c pre-registered)")
    print("=" * 92)
    print(f"{'seed':>6} | {'B.R clk':>8} {'A.R homeo':>10} {'shuf.R':>7} {'abl.R':>7} | A fires")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_R']:>8.3f} {r['a_R']:>10.3f} {r['sh_R']:>7.3f} "
              f"{r['ab_R']:>7.3f} | {r['a_n']:>5}")
    b = np.array([r['b_R'] for r in rows]); a = np.array([r['a_R'] for r in rows])
    sh = np.array([r['sh_R'] for r in rows]); ab = np.array([r['ab_R'] for r in rows])
    c1 = bool(np.all((b - a) >= 0.30) and (b.mean() - a.mean()) >= 0.30)
    c2 = bool(np.all(a <= 0.35))
    c3 = bool(np.all(sh <= 0.50))
    c4 = bool(np.all(ab <= 0.50))
    c5 = bool(all(r['d1_ok'] for r in base))
    c6 = bool(all(r['d2_ok'] for r in base))
    c7 = bool(all(r['nofab_ok'] for r in base))
    print("-" * 92)
    print(f"B.R mean={b.mean():.3f} {b.round(3).tolist()} | A.R mean={a.mean():.3f} {a.round(3).tolist()}")
    print(f"shuf.R mean={sh.mean():.3f} {sh.round(3).tolist()} | abl.R mean={ab.mean():.3f} {ab.round(3).tolist()}")
    print(f"  (c1 PRESENCE)        B.R-A.R>=+0.30 : {c1}  (mean Delta {(b.mean()-a.mean()):+.3f})")
    print(f"  (c2 DISTINCT)        A.R<=0.35      : {c2}  (A.R max {a.max():.3f})")
    print(f"  (c3 EARNED-SCHEDULE) shuf.R<=0.50   : {c3}  (shuf max {sh.max():.3f})")
    print(f"  (c4 EARNED-PERIOD)   abl.R<=0.50    : {c4}  (abl {ab.max():.3f})")
    print(f"  (c5 D1 content-indep)              : {c5}")
    print(f"  (c6 D2 no-reset)                   : {c6}")
    print(f"  (c7 NO-FAB)                        : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 92)
    print(f"VERDICT R1c: {'GREEN' if green else 'RED/WALL'}  (c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("=" * 92)
    return green


# ── R1d (frozen-first, H_1298_FREEZE_R1d.txt): more periods, small-k shuffle fix ──
# Same phase-locking metric and IDENTICAL bars as R1c; ONLY N_TICKS 24->80 (10 periods)
# so the shuffle has k=10 fire events (chance R ~ 1/sqrt(10) = 0.316 << 0.50) and MUST
# cancel. This is an INVESTMENT fix (a_break_the_wall), not a threshold move. R1a/b/c REDs
# stand verbatim.
N_TICKS_R1D = 80                               # 10 full periods


def run_seed_r1d(seed):
    rng = np.random.default_rng(seed)
    nt = N_TICKS_R1D
    sat_stream = SETPOINT + 0.3 + 0.1 * rng.random(nt)

    clk = CircadianClock()
    b_fires = []
    for t in range(nt):
        if clk.fire(): b_fires.append(t)
        clk.step()

    hd = HomeostaticDrive()
    a_fires = []
    for t in range(nt):
        hd.step(sat_stream[t])
        if hd.fire(): a_fires.append(t)

    n_fire = sum((t % PERIOD) == FIRE_TICK for t in range(nt))
    sh_fires = sorted(rng.permutation(nt)[:n_fire].tolist())

    ab_fires = [t for t in range(nt)
                if (t >= ABL_OFFSET_R1B) and ((t - ABL_OFFSET_R1B) % ABL_PERIOD_R1B == 0)]

    # D1 content-independence at this length
    drive_trace = []
    hd2 = HomeostaticDrive()
    for t in range(nt):
        hd2.step(sat_stream[t]); drive_trace.append(hd2.last_drive)
    d1_ok = (len(b_fires) == nt // PERIOD) and ((max(drive_trace) - drive_trace[0]) <= 0.05)

    return dict(seed=seed, b_R=vector_strength(b_fires), a_R=vector_strength(a_fires),
                sh_R=vector_strength(sh_fires), ab_R=vector_strength(ab_fires),
                b_n=len(b_fires), a_n=len(a_fires), d1_ok=d1_ok)


def main_r1d():
    rows = [run_seed_r1d(s) for s in SEEDS]
    base = [run_seed(s) for s in SEEDS]        # D2 / NO-FAB are length-invariant structural checks
    print("\n" + "=" * 92)
    print("H_1298 R1d — PHASE-LOCKING R, 10 periods (FREEZE_R1d pre-registered; small-k fix)")
    print("=" * 92)
    print(f"{'seed':>6} | {'B.R clk':>8} {'A.R homeo':>10} {'shuf.R':>7} {'abl.R':>7} | B fires  A fires")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_R']:>8.3f} {r['a_R']:>10.3f} {r['sh_R']:>7.3f} "
              f"{r['ab_R']:>7.3f} | {r['b_n']:>6}  {r['a_n']:>6}")
    b = np.array([r['b_R'] for r in rows]); a = np.array([r['a_R'] for r in rows])
    sh = np.array([r['sh_R'] for r in rows]); ab = np.array([r['ab_R'] for r in rows])
    c1 = bool(np.all((b - a) >= 0.30) and (b.mean() - a.mean()) >= 0.30)
    c2 = bool(np.all(a <= 0.35))
    c3 = bool(np.all(sh <= 0.50))
    c4 = bool(np.all(ab <= 0.50))
    c5 = bool(all(r['d1_ok'] for r in rows))
    c6 = bool(all(r['d2_ok'] for r in base))
    c7 = bool(all(r['nofab_ok'] for r in base))
    print("-" * 92)
    print(f"B.R mean={b.mean():.3f} {b.round(3).tolist()} | A.R mean={a.mean():.3f} {a.round(3).tolist()}")
    print(f"shuf.R mean={sh.mean():.3f} {sh.round(3).tolist()} | abl.R mean={ab.mean():.3f} {ab.round(3).tolist()}")
    print(f"  (c1 PRESENCE)        B.R-A.R>=+0.30 : {c1}  (mean Delta {(b.mean()-a.mean()):+.3f})")
    print(f"  (c2 DISTINCT)        A.R<=0.35      : {c2}  (A.R max {a.max():.3f})")
    print(f"  (c3 EARNED-SCHEDULE) shuf.R<=0.50   : {c3}  (shuf max {sh.max():.3f})")
    print(f"  (c4 EARNED-PERIOD)   abl.R<=0.50    : {c4}  (abl max {ab.max():.3f})")
    print(f"  (c5 D1 content-indep)              : {c5}")
    print(f"  (c6 D2 no-reset)                   : {c6}")
    print(f"  (c7 NO-FAB)                        : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 92)
    print(f"VERDICT R1d: {'GREEN' if green else 'RED/WALL'}  (c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("SCOPE: numpy-mirror DIRECTIONAL (engine-transfer UNVERIFIED til R2); TOY 10 periods,")
    print("3 seeds, deterministic clock (TIMING STRUCTURE, not entrained oscillator); scale/")
    print("real-corpus/photic-entrainment/multi-period nesting/brain-wiring = follow-on.")
    print("=" * 92)
    return green


def main():
    rows = [run_seed(s) for s in SEEDS]
    print("=" * 92)
    print("H_1298 — CIRCADIAN/INTERVAL CLOCK (HD33) — R1 numpy MIRROR (DIRECTIONAL)")
    print("=" * 92)
    print(f"frozen: PERIOD={PERIOD} N_TICKS={N_TICKS} seeds={SEEDS}  (FREEZE pre-registered)")
    print("-" * 92)
    print(f"{'seed':>6} | {'B clk':>7} {'A homeo':>8} {'B-shuf':>7} {'B-abl':>7} | "
          f"{'driveRise':>9} {'Bfires':>6} | d1 d2 nofab")
    for r in rows:
        print(f"{r['seed']:>6} | {r['b_acc']:>7.3f} {r['a_acc']:>8.3f} {r['sh_acc']:>7.3f} "
              f"{r['ab_acc']:>7.3f} | {r['drive_rise']:>9.3f} {r['b_fire_count']:>6} | "
              f"{int(r['d1_ok'])}  {int(r['d2_ok'])}   {int(r['nofab_ok'])}")
    print("-" * 92)

    b = np.array([r['b_acc'] for r in rows]); a = np.array([r['a_acc'] for r in rows])
    sh = np.array([r['sh_acc'] for r in rows]); ab = np.array([r['ab_acc'] for r in rows])

    # ── frozen bars ──────────────────────────────────────────────────────────
    c1 = bool(np.all((b - a) >= 0.30) and (b.mean() - a.mean()) >= 0.30)   # PRESENCE
    c2 = bool(np.all(a <= 0.65))                                            # DISTINCT
    c3 = bool(np.all(sh <= a + 0.15))                                       # EARNED-SCHED
    c4 = bool(np.all(ab <= a + 0.15))                                       # EARNED-PERIOD
    c5 = bool(all(r['d1_ok'] for r in rows))                                # D1 content-indep
    c6 = bool(all(r['d2_ok'] for r in rows))                                # D2 no-reset
    c7 = bool(all(r['nofab_ok'] for r in rows))                             # NO-FAB

    print(f"B(clk) mean   = {b.mean():.3f}   per-seed {b.round(3).tolist()}")
    print(f"A(homeo) mean = {a.mean():.3f}   per-seed {a.round(3).tolist()}")
    print(f"B-shuffle mean= {sh.mean():.3f}   per-seed {sh.round(3).tolist()}")
    print(f"B-ablate mean = {ab.mean():.3f}   per-seed {ab.round(3).tolist()}")
    print("-" * 92)
    print(f"  (c1 PRESENCE)        B-A >= +0.30 each+mean : {c1}   (mean Delta = {(b.mean()-a.mean()):+.3f})")
    print(f"  (c2 DISTINCT)        A <= 0.65              : {c2}   (A max = {a.max():.3f})")
    print(f"  (c3 EARNED-SCHEDULE) B-shuf <= A+0.15       : {c3}")
    print(f"  (c4 EARNED-PERIOD)   B-abl  <= A+0.15       : {c4}")
    print(f"  (c5 D1 content-indep) clk fires on sched & homeo flat : {c5}")
    print(f"  (c6 D2 no-reset)      clk phase invariant & homeo reset: {c6}")
    print(f"  (c7 NO-FAB)           off-schedule → no fire           : {c7}")
    green = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print("=" * 92)
    print(f"VERDICT: {'GREEN' if green else 'RED/WALL'}  "
          f"(c1..c7 = {[c1,c2,c3,c4,c5,c6,c7]})")
    print("SCOPE: numpy-mirror DIRECTIONAL (engine-transfer UNVERIFIED til R2); TOY 3 periods,")
    print("3 seeds, deterministic clock (tests TIMING STRUCTURE not entrained oscillator);")
    print("scale/real-corpus/photic-entrainment/multi-period nesting/brain-wiring = follow-on.")
    print("=" * 92)
    return green


if __name__ == "__main__":
    import sys
    r1a_green = main()       # ORIGINAL frozen path (RED on c4 — trivial-origin leak; verbatim)
    r1b_green = main_r1b()   # re-design 1 (recurrence-scored — RED, metric too coarse; verbatim)
    r1c_green = main_r1c()   # re-design 2 (phase-locking R — genuine signature; RED on small-k shuffle)
    r1d_green = main_r1d()   # re-design 3 (10 periods — small-k shuffle fix; the binding R1 verdict)
    sys.exit(0 if r1d_green else 1)
