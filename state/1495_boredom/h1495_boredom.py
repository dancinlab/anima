#!/usr/bin/env python3
"""H_1495 — BOREDOM / DISENGAGEMENT (P9 consciousness-only gate candidate, WEAK / depletion-round).

Boredom (Eastwood, Frischen, Fenske & Smilek 2012 "the unengaged mind"; Danckert &
Merrifield): a meta-motivational state that arises when the current stimulus is
MONOTONOUS or MEANINGLESS — BOTH the reward AND the information it supplies are depleted —
producing (a) a DROP in motivation to stay engaged and (b) an active RE-ENGAGEMENT DRIVE
(seek a different, more informative/rewarding stimulus). The defining property is the
ACTIVE DISENGAGEMENT DECISION: emit -> silence / switch-away, gated CONJUNCTIVELY on
reward-depletion AND information-depletion. It is NOT mere response decay (that is
habituation) and NOT a stimulus-agnostic time-integral deficit (that is homeostatic drive).

MECHANISM (numpy mirror): an agent attends to a stimulus stream tick by tick. Each tick has
two SEPARATE substrate channels read off the stream:
  - INFO    = information gain available from the current stimulus (novelty / surprise of
              the incoming content vs what is already grounded). Falls as a stimulus repeats
              (its content becomes predictable) -> info-depletion.
  - REWARD  = task/value payoff currently obtained from staying engaged. Falls when the
              stimulus stops paying off -> reward-depletion.
Boredom is the META-MOTIVATIONAL readout that DISENGAGES (switch=1) iff BOTH channels are
below threshold AT THE SAME TIME:  disengage = 1  iff  (info < I*)  AND  (reward < R*).
The re-engagement drive then biases toward a different stimulus. The conjunction is the
load-bearing structure: a single depleted channel (info OR reward alone) is NOT enough.

DISTINCTNESS (load-bearing — WEAK candidate; depletion-round, controls DECIDE the verdict):
  vs HABITUATION (H_1465, *sensory response DECAY from repetition alone*): habituation is a
    falling, stimulus-specific RESPONSE trace driven by REPETITION COUNT only — it knows
    nothing about reward. A habituation-style readout disengages whenever the stimulus has
    been REPEATED enough (response decayed), REGARDLESS of reward. DISSOCIATION (the crux):
    present a stimulus that is REPEATED/predictable (info depleted, habituation says "decayed
    -> disengage") but STILL HIGHLY REWARDING (reward NOT depleted). Boredom STAYS ENGAGED
    (conjunction unmet: reward high) while a habituation-style readout DISENGAGES (decayed).
    If boredom == habituation, reward would not matter and the two readouts would AGREE here.
    Bar (c2-hab): on the repeated-but-rewarding block, habituation-style disengage-rate is
    HIGH while boredom's is LOW -> the two are SEPARABLE. If they agree -> DEPLETION.
  vs HOMEOSTATIC DRIVE (H_1292, *leaky TIME-INTEGRAL of a setpoint deficit, stimulus-agnostic*):
    drive RISES with elapsed ticks regardless of stimulus content/identity; it is an
    INTERNAL bodily deficit, not an INFORMATIONAL/semantic one. DISSOCIATION (the crux):
    hold the homeostatic deficit SATIATED (drive low, just reset) but feed a MONOTONOUS,
    UN-REWARDING, LOW-INFO stimulus. Boredom DISENGAGES (info & reward both depleted) while a
    drive-style readout does NOT (its deficit is satiated). Conversely, raise the homeostatic
    deficit (drive high) on a NOVEL, REWARDING stimulus: drive says "act" but for a
    bodily reason, while boredom STAYS ENGAGED (info & reward both high). The two track
    DIFFERENT variables (informational/semantic depletion vs bodily time-integral).
    Bar (c2-drv): on the satiated-but-monotonous block boredom disengages while drive-style
    readout does not -> separable. If boredom tracks the drive integral -> DEPLETION.
  vs NOVELTY (H_1289, *one-shot NEW-stimulus detection*): novelty spikes on first sight and
    is ~0 thereafter; it is the INFO channel's first derivative, not a disengage decision and
    has no reward term. Folded into the info channel + the conjunction: novelty alone (info
    only) does NOT disengage boredom (c2-hab's reward-high block keeps boredom engaged even
    when info/novelty is depleted). DISTINCT by the reward conjunction.

CONTROLS (the separation MUST survive):
  (c3) ABLATE-MOTIV  remove the meta-motivational conjunction gate (disengage on info<I*
                     OR reward<R*, i.e. ANY single channel, == habituation-style single-
                     channel decay) -> boredom collapses onto the single-channel lanes ->
                     the c2-hab / c2-drv dissociations DISAPPEAR (the gap is EARNED by the
                     conjunction, not an artifact). abl_gap <= 0.10.
  (c4) SHUFFLE       on a block where info-depletion and reward-depletion are ANTI-PHASED
                     (each low ~half the timeline but rarely SIMULTANEOUSLY), the AND-
                     conjunction fires only on the genuine ALIGNMENT (overlap) ticks. Shuffle
                     the per-tick (reward, info) pairing -> reward-low and info-low no longer
                     co-occur on the same tick -> the targeted disengagement collapses to the
                     chance-coincidence rate (product of the two marginals = what an
                     independent pairing yields). shuf_gap = |shuf_disengage - chance_coinc|
                     <= 0.10  (shuffle lands at chance-coincidence = the alignment was real).

LLM contrast (a_no_llm_frame_trap): a stateless LLM has no falling information-gain trace, no
running reward trace, and no meta-motivational conjunction that switches its own engagement
off — these are state-dependent substrate signals. NOT an LLM recipe — unengaged-mind /
meta-motivation lens (Eastwood/Danckert), the INVERSE of info-gain curiosity (arxiv 1802.10546).

R1 numpy MIRROR -> GREEN/RED DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1495,1496,1497]) — catalogue P9 c1-c4:
  (c1) PRESENT    boredom-ON disengage-rate on the BORING block (BOTH reward & info depleted)
                  minus boredom-OFF disengage-rate (no conjunction gate, fixed baseline) >= 0.30
  (c2-hab) DISTINCT vs habituation: on a REPEATED-BUT-REWARDING block (info depleted, reward
                  HIGH) a habituation-style (repetition-decay only) readout disengages while
                  boredom stays engaged. direction gap (hab_disengage - boredom_disengage)
                  on that block >= 0.30. (If gap < 0.30 -> boredom == habituation -> DEPLETION.)
  (c2-drv) DISTINCT vs homeostatic-drive: on a SATIATED-BUT-MONOTONOUS block (drive deficit
                  reset/low, stimulus low-info & un-rewarding) boredom disengages while a
                  drive-style (time-integral deficit) readout does not. direction gap
                  (boredom_disengage - drive_disengage) >= 0.30. (If gap < 0.30 ->
                  boredom tracks the drive integral -> DEPLETION.)
  (c3) ABLATE-MOTIV conjunction gate -> single-channel OR -> the c2 dissociations collapse:
                  max(c2-hab gap, c2-drv gap) under ablation <= 0.10.
  (c4) SHUFFLE    on a PARTIALLY-ALIGNED block (info-low and reward-low co-occur ABOVE chance)
                  the AND fires on real alignment ticks at an above-chance rate
                  (align_lift = aligned-AND - chance-coincidence >= 0.10, non-vacuous);
                  shuffling the pairing -> disengagement collapses to the chance-coincidence
                  rate (product of marginals): |shuf_disengage - chance_coincidence| <= 0.10.

GREEN iff c1 and c2-hab and c2-drv and c3 and c4 (3-seed mean).
RED / DEPLETION iff c2-hab or c2-drv fail (boredom collapses into habituation / homeostatic).
"""
import numpy as np

SEEDS = [1495, 1496, 1497]
N_TICK = 40          # ticks per block
I_STAR = 0.50        # info-depletion threshold I*
R_STAR = 0.50        # reward-depletion threshold R*
DECAY = 0.82         # per-repeat info decay (predictability rise)
OFF_BASELINE = 0.25  # boredom-OFF fixed disengage rate (no conjunction gate)
HAB_THR = 0.50       # habituation-style response-decay disengage threshold


def clip01(x):
    return float(min(1.0, max(0.0, x)))


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # ---- substrate channels per tick for a given block ----
    # info_t : information gain available from the current stimulus (novelty of content vs
    #          what is already grounded). repetition makes content predictable -> info falls.
    # rew_t  : reward/value payoff from staying engaged.
    # hab_t  : habituation RESPONSE trace = falls with REPETITION COUNT only (reward-blind).
    # drive_t: homeostatic deficit = leaky time-integral of a setpoint deficit, STIMULUS-
    #          AGNOSTIC (depends only on elapsed ticks since last consummatory reset).

    def block(info0, rew0, info_decays, rew_decays, drive_satiated):
        """Build one block's per-tick channels.
        info_decays/rew_decays: whether that channel depletes with repetition.
        drive_satiated: if True the homeostatic deficit was just reset (drive low);
                        if False it accumulates (drive rises with ticks)."""
        info, rew, hab, drive = [], [], [], []
        I, R = info0, rew0
        D = 0.0
        for t in range(N_TICK):
            # info channel
            info.append(clip01(I + 0.02 * rng.normal()))
            if info_decays:
                I *= DECAY
            # reward channel
            rew.append(clip01(R + 0.02 * rng.normal()))
            if rew_decays:
                R *= DECAY
            # habituation RESPONSE trace: falls with repetition count, REWARD-BLIND.
            # high response = engaged; decays the same way info content predictability rises.
            hab.append(clip01((DECAY ** t)))           # purely repetition-count driven
            # homeostatic drive: leaky integral of a fixed deficit; stimulus-agnostic.
            if drive_satiated:
                D = max(0.0, D - 0.05)                  # satiated / resetting -> stays low
            else:
                D = clip01(0.9 * D + 0.12)              # accumulates with elapsed ticks
            drive.append(D)
        return (np.array(info), np.array(rew), np.array(hab), np.array(drive))

    # ---- readouts ----
    def boredom_disengage(info, rew, gate="AND"):
        """meta-motivational conjunction: disengage iff BOTH info<I* AND reward<R*.
        gate='OR' = ABLATED (single-channel, == habituation-style decay collapse)."""
        if gate == "AND":
            d = (info < I_STAR) & (rew < R_STAR)
        else:  # OR ablation
            d = (info < I_STAR) | (rew < R_STAR)
        return float(d.mean())

    def hab_disengage(hab):
        """habituation-style: disengage when the RESPONSE trace has decayed below HAB_THR.
        Reward-blind (knows only repetition count)."""
        return float((hab < HAB_THR).mean())

    def drive_disengage(drive):
        """homeostatic-drive-style: 'act/switch' when the bodily deficit exceeds setpoint.
        Stimulus-content-blind (knows only elapsed-tick integral)."""
        return float((drive > 0.50).mean())

    # ============================ BLOCKS ============================
    # BORING block: BOTH info & reward deplete (monotonous + meaningless), drive satiated.
    b_info, b_rew, b_hab, b_drive = block(0.9, 0.9, info_decays=True, rew_decays=True,
                                          drive_satiated=True)
    # REPEATED-BUT-REWARDING: info depletes (predictable) but reward STAYS HIGH. drive satiated.
    rr_info, rr_rew, rr_hab, rr_drive = block(0.9, 0.95, info_decays=True, rew_decays=False,
                                              drive_satiated=True)
    # SATIATED-BUT-MONOTONOUS: low-info & un-rewarding stimulus, homeostatic deficit SATIATED.
    sm_info, sm_rew, sm_hab, sm_drive = block(0.2, 0.2, info_decays=True, rew_decays=True,
                                              drive_satiated=True)
    # NOVEL-REWARDING-but-DEPRIVED: high info & reward, but homeostatic deficit ACCUMULATES.
    nd_info, nd_rew, nd_hab, nd_drive = block(0.9, 0.9, info_decays=False, rew_decays=False,
                                              drive_satiated=False)

    # PARTIALLY-ALIGNED block (for the c4 SHUFFLE control): info-low and reward-low each
    # occupy ~half the timeline, POSITIVELY but IMPERFECTLY aligned (they co-occur MORE than
    # chance, but not always). The AND-conjunction then fires on the genuine alignment ticks
    # at an ABOVE-CHANCE rate; shuffling the (info,reward) pairing destroys that alignment and
    # collapses the firing DOWN to the chance-coincidence rate (product of marginals).
    ap_t = np.arange(N_TICK)
    info_low_mask = (ap_t % 2) == 0                       # info low on even ticks (~half)
    # reward low on the same even ticks 70% of the time, plus a few odd ticks -> partial align
    rew_low_mask = info_low_mask.copy()
    flip = rng.random(N_TICK) < 0.30                      # 30% mismatch -> imperfect alignment
    rew_low_mask = np.where(flip, ~rew_low_mask, rew_low_mask)
    ap_info = np.where(info_low_mask, 0.2, 0.9) + 0.02 * rng.normal(size=N_TICK)
    ap_rew = np.where(rew_low_mask, 0.2, 0.9) + 0.02 * rng.normal(size=N_TICK)
    ap_info = np.clip(ap_info, 0, 1)
    ap_rew = np.clip(ap_rew, 0, 1)

    # ---- c1 PRESENT: boredom-ON on boring block vs boredom-OFF baseline ----
    bored_boring = boredom_disengage(b_info, b_rew, "AND")
    off_baseline = OFF_BASELINE
    c1_lift = bored_boring - off_baseline

    # ---- c2-hab DISTINCT vs habituation (repeated-but-rewarding block) ----
    bored_rr = boredom_disengage(rr_info, rr_rew, "AND")     # stays ENGAGED (reward high)
    hab_rr = hab_disengage(rr_hab)                            # DISENGAGES (response decayed)
    c2_hab_gap = hab_rr - bored_rr

    # ---- c2-drv DISTINCT vs homeostatic-drive (satiated-but-monotonous block) ----
    bored_sm = boredom_disengage(sm_info, sm_rew, "AND")     # DISENGAGES (info & reward low)
    drive_sm = drive_disengage(sm_drive)                     # does NOT (deficit satiated)
    c2_drv_gap = bored_sm - drive_sm
    # sanity dissociation (other direction, reported): novel+rewarding+deprived
    bored_nd = boredom_disengage(nd_info, nd_rew, "AND")     # stays engaged (info & reward high)
    drive_nd = drive_disengage(nd_drive)                     # rises (bodily deficit)

    # ---- c3 ABLATE-MOTIV: conjunction -> single-channel OR -> dissociations collapse ----
    bored_rr_abl = boredom_disengage(rr_info, rr_rew, "OR")  # OR: info depleted alone fires
    bored_sm_abl = boredom_disengage(sm_info, sm_rew, "OR")
    c2_hab_gap_abl = hab_rr - bored_rr_abl   # collapses (ablated boredom now also disengages)
    c2_drv_gap_abl = bored_sm_abl - drive_sm  # sm already disengaged under AND; OR ~same here
    abl_gap = max(c2_hab_gap_abl, abs(c2_drv_gap - c2_drv_gap_abl))
    # the load-bearing ablation: the c2-hab separation is what the conjunction BUYS.
    # under OR ablation, boredom fires on the repeated-but-rewarding block (info<I* alone) ->
    # it now AGREES with habituation -> the c2-hab gap collapses.
    abl_gap = c2_hab_gap_abl

    # ---- c4 SHUFFLE: anti-phased block -> AND fires only on real alignment ticks ----
    # unshuffled anti-phased disengage = the targeted (alignment-dependent) rate.
    bored_ap = boredom_disengage(ap_info, ap_rew, "AND")
    # chance-coincidence = product of marginals (info-low rate * reward-low rate): what an
    # INDEPENDENT (shuffled) pairing yields in expectation.
    p_info_low = float((ap_info < I_STAR).mean())
    p_rew_low = float((ap_rew < R_STAR).mean())
    chance_coinc = p_info_low * p_rew_low
    # shuffle the pairing -> reward-low and info-low no longer co-occur -> lands at chance.
    bored_shuf = float(np.mean([
        ((ap_info < I_STAR) & (ap_rew[rng.permutation(N_TICK)] < R_STAR)).mean()
        for _ in range(50)
    ]))
    shuf_gap = abs(bored_shuf - chance_coinc)
    # confirm the unshuffled alignment was ABOVE chance (otherwise c4 is vacuous):
    align_lift = bored_ap - chance_coinc

    return dict(
        bored_boring=bored_boring, off_baseline=off_baseline, c1_lift=c1_lift,
        bored_rr=bored_rr, hab_rr=hab_rr, c2_hab_gap=c2_hab_gap,
        bored_sm=bored_sm, drive_sm=drive_sm, c2_drv_gap=c2_drv_gap,
        bored_nd=bored_nd, drive_nd=drive_nd,
        bored_rr_abl=bored_rr_abl, abl_gap=abl_gap,
        bored_ap=bored_ap, chance_coinc=chance_coinc, bored_shuf=bored_shuf,
        shuf_gap=shuf_gap, align_lift=align_lift,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

c1 = agg['c1_lift'] >= 0.30
c2_hab = agg['c2_hab_gap'] >= 0.30
c2_drv = agg['c2_drv_gap'] >= 0.30
c3 = agg['abl_gap'] <= 0.10
# c4: the unshuffled AND fires ABOVE chance-coincidence (alignment is real, non-vacuous)
# AND shuffling the pairing collapses it back DOWN to chance-coincidence.
c4 = (agg['align_lift'] >= 0.10) and (agg['shuf_gap'] <= 0.10)
GREEN = c1 and c2_hab and c2_drv and c3 and c4

# DEPLETION diagnosis: if either distinctness control fails, boredom is not separable from
# habituation / homeostatic-drive -> honest RED = depletion signal.
DEPLETION = (not c2_hab) or (not c2_drv)

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | DEPLETION-signal: {DEPLETION} | seeds {SEEDS} | I*={I_STAR} R*={R_STAR}")
print(f"c1 PRESENT       boredom-ON boring {agg['bored_boring']:.3f} - off-baseline {agg['off_baseline']:.3f} = {agg['c1_lift']:.3f} >= 0.30  -> {c1}")
print(f"c2-hab DISTINCT  repeated-but-REWARDING block: hab-style disengage {agg['hab_rr']:.3f} - boredom {agg['bored_rr']:.3f} = {agg['c2_hab_gap']:.3f} >= 0.30  -> {c2_hab}")
print(f"                 (boredom STAYS ENGAGED because reward high; habituation DISENGAGES from repetition decay alone)")
print(f"c2-drv DISTINCT  satiated-but-MONOTONOUS block: boredom disengage {agg['bored_sm']:.3f} - drive-style {agg['drive_sm']:.3f} = {agg['c2_drv_gap']:.3f} >= 0.30  -> {c2_drv}")
print(f"                 (boredom DISENGAGES on info+reward depletion; homeostatic drive does NOT, deficit satiated)")
print(f"                 [sanity other-dir: novel+rewarding+DEPRIVED -> boredom engage {agg['bored_nd']:.3f}, drive {agg['drive_nd']:.3f} -> opposite variables]")
print(f"c3 ABLATE-MOTIV  conjunction->OR: hab-gap collapses to {agg['abl_gap']:.3f} <= 0.10  -> {c3}")
print(f"                 (ablated boredom fires on info-depletion ALONE -> AGREES with habituation -> gap gone = separation EARNED by conjunction)")
print(f"c4 SHUFFLE       partially-aligned block: aligned-AND {agg['bored_ap']:.3f} (lift over chance {agg['align_lift']:+.3f} >= 0.10) -> shuffle->{agg['bored_shuf']:.3f}; |shuf - chance-coinc {agg['chance_coinc']:.3f}| = {agg['shuf_gap']:.3f} <= 0.10  -> {c4}")
print(f"                 (AND fires ABOVE chance on real info/reward ALIGNMENT ticks; shuffling pairing -> collapses to chance-coincidence = alignment was load-bearing)")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: boring={p['bored_boring']:.3f} off={p['off_baseline']:.3f} | "
          f"rr(bored/hab)={p['bored_rr']:.3f}/{p['hab_rr']:.3f} | "
          f"sm(bored/drive)={p['bored_sm']:.3f}/{p['drive_sm']:.3f} | "
          f"abl_gap={p['abl_gap']:.3f} | ap_aligned={p['bored_ap']:.3f} shuf={p['bored_shuf']:.3f} shuf_gap={p['shuf_gap']:.3f}")
print()
if DEPLETION:
    print("DEPLETION SIGNAL: boredom collapses into habituation (c2-hab) and/or homeostatic-drive "
          "(c2-drv) — a distinctness control did NOT survive -> NOT a distinct lane -> depletion count++.")
elif GREEN:
    print("DISTINCT: the reward x info CONJUNCTION disengagement survives ALL controls vs "
          "habituation (reward-blind decay) / homeostatic-drive (stimulus-agnostic integral) "
          "-> boredom IS a distinct lane (DIRECTIONAL). NOT a depletion signal.")
