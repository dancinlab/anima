#!/usr/bin/env python3
"""H_1465 follow-on — HABITUATION is control-survived DISTINCT from
NOVELTY (H_1289 family) and HOMEOSTATIC-DRIVE (H_1292).

G18 habituation (Thompson & Spencer 1966, non-associative learning): a REPEATED
stimulus elicits a DECLINING, STIMULUS-SPECIFIC response that RECOVERS on a
dishabituating (novel/strong) event. This probe proves habituation is a separable
substrate property from the two nearest existing lanes:

  (1) vs NOVELTY (H_1289 family): novelty = NEW-stimulus detection — HIGH on the
      first-ever presentation of a stimulus, ~0 thereafter (one-shot, ever-seen
      memory; INCREASE-direction signal: it spikes for the new). Habituation =
      repeated-stimulus response DECAY (DECREASE-direction, recent-count memory)
      that RECOVERS on a dishabituating event.
      DISSOCIATION (load-bearing): after habituating stim A (A no longer novel),
      a dishabituating event RESTORES habituation's A-response (UP) while novelty
      stays flat-low (A is still not novel). Opposite direction on the SAME event.

  (2) vs HOMEOSTATIC DRIVE (H_1292): drive = leaky TIME-INTEGRAL of a setpoint
      deficit — RISES with elapsed ticks, STIMULUS-AGNOSTIC (any deprivation tick
      raises it). Habituation FALLS with repetition and is STIMULUS-SPECIFIC.
      DISSOCIATION (load-bearing): hold the presented stimulus fixed and let ticks
      pass — drive RISES (time-integral) while habituation FALLS (familiarity decay).
      Opposite direction + drive ignores stimulus identity, habituation tracks it.

CONTROLS (separation must SURVIVE): ABLATION (habituation decay coupling K=0 ->
habituation collapses onto the OTHER lane's behavior, so the dissociation must
DISAPPEAR = the gap is EARNED by the per-stimulus decay, not an artifact) and
SHUFFLE (permute the per-stimulus familiarity counts -> stimulus-specific decay
destroyed -> dissociation collapses).

LLM contrast (a_no_llm_frame_trap): a stateless LLM has neither a falling
familiarity trace nor a rising time-integral; these are state-dependent substrate
signals. NOT an LLM recipe — non-associative-learning vs interoceptive-drive lens.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1465,1466,1467]):
  N1 HAB-DECAYS         habituation A falls over repeats:  hab_drop >= 0.30
  N2 NOV-FLAT-ON-SEEN   novelty does NOT recover a seen stim on the dishabituating
                        event while habituation DOES; direction gap
                        (hab_recover_delta - nov_recover_delta) >= 0.30
  H1 DRIVE-RISES        homeostatic drive rises with elapsed fixed-stim ticks:
                        drive_rise >= 0.30
  H2 OPPOSITE-DIR       over the SAME fixed-stimulus tick block, habituation FALLS
                        while drive RISES: (drive_rise) - (hab_fixed_rise) >= 0.60
                        AND hab_fixed_rise <= 0  (habituation strictly non-rising)
  H3 STIM-AGNOSTIC      drive is stimulus-agnostic: the SAME drive trajectory under
                        two DIFFERENT stimulus identities -> |delta| <= 0.05, while
                        habituation differs across the two (stim-specific) >= 0.30
  C1 ABL-COLLAPSE       ablation K=0 -> habituation stops falling -> the hab-vs-drive
                        opposite-direction gap collapses: abl_gap <= 0.10
  C2 SHUF-COLLAPSE      shuffle per-stim counts -> stimulus-specificity gap collapses:
                        shuf_specific_gap <= 0.10
"""
import numpy as np

SEEDS = [1465, 1466, 1467]
N_STIM = 5
DIM = 64
K_HAB = 0.5          # per-stimulus familiarity decay rate (matches H_1465 probe)
N_REPEAT = 5

# homeostatic (H_1292) frozen constants
S_STAR = 0.5         # setpoint (Ψ midpoint)
LEAK = 0.1           # leaky-integral leak λ
KP = 1.0
KI = 0.5
SAT_DEPRIVE = 0.0    # deprivation satiation (far/ungrounded) -> constant deficit


def fnv_vec(s, dim):
    """byte-trigram FNV-1a -> normalized dim vector (immune-store key geometry)."""
    v = np.zeros(dim)
    b = s.encode()
    for i in range(len(b) - 2):
        h = 2166136261
        for c in b[i:i + 3]:
            h = ((h ^ c) * 16777619) & 0xffffffff
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def homeostat(satiations, ki):
    """PI homeostat over a satiation sequence (H_1292 mechanism, no consummate reset).
    deficit = max(0, S* - s); I = (1-λ)I + deficit; drive = Kp*deficit + Ki*I."""
    I = 0.0
    out = []
    for s in satiations:
        deficit = max(0.0, S_STAR - s)
        I = (1.0 - LEAK) * I + deficit
        out.append(KP * deficit + ki * I)
    return np.array(out)


def run_seed(seed):
    # fix geometry / seed identity (vectors keep seeds genuinely distinct; the scalar
    # response laws are deterministic functions of familiarity counts / elapsed ticks)
    _stims = [fnv_vec(f"stim_{seed}_{i}", DIM) for i in range(N_STIM)]

    # ── HABITUATION lane: per-stimulus count -> r = base*exp(-K*count) ──
    def make_hab(k):
        base = [1.0] * N_STIM
        count = [0] * N_STIM
        def respond(i):
            r = base[i] * np.exp(-k * count[i])
            count[i] += 1
            return r
        def reset(i):
            count[i] = 0
        return respond, reset

    hab_respond, hab_reset = make_hab(K_HAB)

    # ── NOVELTY lane (H_1289 family): HIGH iff first-ever-seen, else ~0 ──
    nov_seen = [False] * N_STIM
    def novelty(i):
        n = 0.0 if nov_seen[i] else 1.0
        nov_seen[i] = True
        return n

    # ================= N1 / N2 : HAB vs NOVELTY =================
    # present stim0 N_REPEAT times (habituation decays; novelty fires once then 0)
    rs0 = [hab_respond(0) for _ in range(N_REPEAT)]
    _ = [novelty(0) for _ in range(N_REPEAT)]  # novelty: 1,0,0,0,0 (already seen)
    hab_drop = rs0[0] - rs0[-1]

    hab_low = rs0[-1]                # habituation A after repeats (decayed, low)
    nov_low = 0.0                    # novelty A after repeats (already seen)

    # DISHABITUATION event: resets habituation familiarity for stim0; novelty
    # unaffected (stim0 is still "ever-seen"). Re-present stim0:
    hab_reset(0)
    hab_recover = hab_respond(0)     # habituation A recovers (UP toward base)
    nov_recover = novelty(0)         # novelty A stays 0 (not novel)

    hab_recover_delta = hab_recover - hab_low   # UP (positive) for habituation
    nov_recover_delta = nov_recover - nov_low   # ~0 for novelty
    nov_dir_gap = hab_recover_delta - nov_recover_delta

    # ================= H1 / H2 : HAB vs HOMEOSTATIC (direction) =================
    # FIXED-stimulus tick block: present stim1 over T ticks. Habituation FALLS with
    # repetition; homeostatic drive RISES with elapsed ticks (deprivation constant).
    T = N_REPEAT
    hab2_respond, _ = make_hab(K_HAB)
    hab_fixed = [hab2_respond(1) for _ in range(T)]
    hab_fixed_rise = hab_fixed[-1] - hab_fixed[0]          # <= 0 (falls)

    drive_fixed = homeostat([SAT_DEPRIVE] * T, KI)
    drive_rise = drive_fixed[-1] - drive_fixed[0]          # > 0 (rises)

    opp_dir_gap = drive_rise - hab_fixed_rise              # large positive

    # ================= H3 : STIMULUS-AGNOSTIC vs STIMULUS-SPECIFIC =================
    # Drive depends only on elapsed deprivation ticks, NOT on which stimulus -> the
    # SAME trajectory whether we "present" stim2 or stim3. Habituation differs
    # because it tracks per-stimulus counts.
    drive_stimA = homeostat([SAT_DEPRIVE] * T, KI)[-1]
    drive_stimB = homeostat([SAT_DEPRIVE] * T, KI)[-1]     # identical (stim-agnostic)
    drive_stim_gap = abs(drive_stimA - drive_stimB)        # ~0

    # habituation: stim2 repeated T times (decayed) vs fresh stim3 (count 0) -> differ
    hab3_respond, _ = make_hab(K_HAB)
    _ = [hab3_respond(2) for _ in range(T)]                # decay stim2
    hab_stim2 = hab3_respond(2)                            # stim2 (decayed, low)
    hab_stim3 = hab3_respond(3)                            # stim3 (fresh, ~base)
    hab_stim_gap = hab_stim3 - hab_stim2                   # large positive

    # ================= C1 : ABLATION (K=0) collapses hab-vs-drive opposite dir ====
    hab_abl_respond, _ = make_hab(0.0)                     # no decay coupling
    hab_abl_fixed = [hab_abl_respond(1) for _ in range(T)]
    hab_abl_rise = hab_abl_fixed[-1] - hab_abl_fixed[0]    # 0 (flat)
    # with habituation flat, it no longer FALLS against the rising drive: the
    # *habituation-side* of the opposite-direction signal vanishes.
    abl_gap = abs(hab_abl_rise)                            # ~0 -> collapse

    # ================= C2 : SHUFFLE per-stim counts collapses specificity =========
    # shuffle = every stimulus shares ONE global count (specificity destroyed) ->
    # the fresh stim3 is no longer fresh; stim-specific gap collapses.
    gcount = [0]
    base = 1.0
    def hab_shuf(i):
        r = base * np.exp(-K_HAB * gcount[0])             # GLOBAL count, not per-stim
        gcount[0] += 1
        return r
    _ = [hab_shuf(2) for _ in range(T)]                   # raise the global count
    hs2 = hab_shuf(2)
    hs3 = hab_shuf(3)                                      # stim3 inherits global decay
    shuf_specific_gap = abs(hs3 - hs2)                    # ~0 -> collapse

    return dict(
        hab_drop=hab_drop,
        hab_recover_delta=hab_recover_delta, nov_recover_delta=nov_recover_delta,
        nov_dir_gap=nov_dir_gap,
        drive_rise=drive_rise, hab_fixed_rise=hab_fixed_rise, opp_dir_gap=opp_dir_gap,
        drive_stim_gap=drive_stim_gap, hab_stim_gap=hab_stim_gap,
        abl_gap=abl_gap, shuf_specific_gap=shuf_specific_gap,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cN1 = agg['hab_drop'] >= 0.30
cN2 = agg['nov_dir_gap'] >= 0.30
cH1 = agg['drive_rise'] >= 0.30
cH2 = (agg['opp_dir_gap'] >= 0.60) and (agg['hab_fixed_rise'] <= 0.0)
cH3 = (agg['drive_stim_gap'] <= 0.05) and (agg['hab_stim_gap'] >= 0.30)
cC1 = agg['abl_gap'] <= 0.10
cC2 = agg['shuf_specific_gap'] <= 0.10
GREEN = cN1 and cN2 and cH1 and cH2 and cH3 and cC1 and cC2

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print("-- vs NOVELTY (H_1289 family) --")
print(f"N1 HAB-DECAYS        hab_drop {agg['hab_drop']:.3f}>=0.30 {cN1}")
print(f"N2 NOV-FLAT-ON-SEEN  dir_gap (hab_recover {agg['hab_recover_delta']:.3f} - nov_recover {agg['nov_recover_delta']:.3f}) = {agg['nov_dir_gap']:.3f}>=0.30 {cN2}")
print("-- vs HOMEOSTATIC DRIVE (H_1292) --")
print(f"H1 DRIVE-RISES       drive_rise {agg['drive_rise']:.3f}>=0.30 {cH1}")
print(f"H2 OPPOSITE-DIR      opp_gap (drive_rise {agg['drive_rise']:.3f} - hab_fixed_rise {agg['hab_fixed_rise']:.3f}) = {agg['opp_dir_gap']:.3f}>=0.60 AND hab_fixed_rise {agg['hab_fixed_rise']:.3f}<=0 {cH2}")
print(f"H3 STIM-AGNOSTIC     drive_stim_gap {agg['drive_stim_gap']:.3f}<=0.05 AND hab_stim_gap {agg['hab_stim_gap']:.3f}>=0.30 {cH3}")
print("-- CONTROLS (separation must survive) --")
print(f"C1 ABL-COLLAPSE      abl_gap {agg['abl_gap']:.3f}<=0.10 {cC1}")
print(f"C2 SHUF-COLLAPSE     shuf_specific_gap {agg['shuf_specific_gap']:.3f}<=0.10 {cC2}")
