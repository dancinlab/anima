"""Probe: root-cause LV-C null bias — off-by-one alignment between Closed and ghost obs streams.
fC = obs_traj[:-1] = PRE-step obs [o_0..o_{T-1}]; _replay_tape collects POST-step obs [o_1..o_T].
Prediction: in null env fP1 == fP2 exactly, and d(fC[t], fP1[t]) == d(f(o_t), f(o_{t+1})).
Fix: fC = obs_traj[1:]. Then null closure -> 0.0 and the dose curve re-measured."""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h011_live-ab-closure_2026-07-16"))
import run_h011 as R
import run_h013 as H
E = R.E

def lv_c_dose_old(policy, seed, T, p, null=False):
    """The PRE-repair (misaligned) estimator, frozen verbatim so this probe stays reproducible
    after run_h011/run_h013 were repaired: fC = obs_traj[:-1] (PRE-step frame)."""
    closed = H.run_episode_dose(policy, seed, T, p, null=null, ab=False)
    tape = closed["tape"]
    fC = [R.features(o.encode()) for o in closed["obs_traj"][:-1]]
    fP1 = H._replay_tape_dose(R._derange(tape, seed, 1), seed, p, null=null)
    fP2 = H._replay_tape_dose(R._derange(tape, seed, 2), seed, p, null=null)
    mC, mP1, mP2 = R._blockmeans(fC), R._blockmeans(fP1), R._blockmeans(fP2)
    nb = min(len(mC), len(mP1), len(mP2))
    hits = sum(1 for b in range(nb) if R._sqdist(mC[b], mP1[b]) > R._sqdist(mP1[b], mP2[b]))
    return hits / nb if nb else 0.0

def lv_c_dose_fixed(policy, seed, T, p, null=False):
    closed = H.run_episode_dose(policy, seed, T, p, null=null, ab=False)
    tape = closed["tape"]
    fC = [R.features(o.encode()) for o in closed["obs_traj"][1:]]   # POST-step obs -> aligned with ghosts
    fP1 = H._replay_tape_dose(R._derange(tape, seed, 1), seed, p, null=null)
    fP2 = H._replay_tape_dose(R._derange(tape, seed, 2), seed, p, null=null)
    mC, mP1, mP2 = R._blockmeans(fC), R._blockmeans(fP1), R._blockmeans(fP2)
    nb = min(len(mC), len(mP1), len(mP2))
    hits = sum(1 for b in range(nb) if R._sqdist(mC[b], mP1[b]) > R._sqdist(mP1[b], mP2[b]))
    return hits / nb if nb else 0.0

# ---- 1. null-env anatomy at one seed --------------------------------------
seed, T, p = 7, 600, 1.0
closed = H.run_episode_dose(R.policy_live, seed, T, p, null=True, ab=False)
tape = closed["tape"]
fC_old = [R.features(o.encode()) for o in closed["obs_traj"][:-1]]
fC_new = [R.features(o.encode()) for o in closed["obs_traj"][1:]]
fP1 = H._replay_tape_dose(R._derange(tape, seed, 1), seed, p, null=True)
fP2 = H._replay_tape_dose(R._derange(tape, seed, 2), seed, p, null=True)
ghosts_identical = all(a == b for a, b in zip(fP1, fP2))
closed_aligned_identical = all(a == b for a, b in zip(fC_new, fP1))
mean_shift = sum(R._sqdist(a, b) for a, b in zip(fC_old, fP1)) / T
print(f"[null anatomy] ghosts bit-identical: {ghosts_identical}")
print(f"[null anatomy] ALIGNED closed == ghost: {closed_aligned_identical}")
print(f"[null anatomy] misaligned closed-vs-ghost mean per-tick sqdist: {mean_shift:.4f} (H_013 probe saw 0.0152)")

# ---- 2. closure old vs fixed, null env, all doses ---------------------------
print("\n[null env, 3 eps x T=600] closure OLD (misaligned) vs FIXED (aligned):")
for pp in H.DOSES:
    old = sum(lv_c_dose_old(R.policy_live, seed + e, T, pp, null=True) for e in range(3)) / 3
    new = sum(lv_c_dose_fixed(R.policy_live, seed + e, T, pp, null=True) for e in range(3)) / 3
    print(f"    p={pp:.2f}  old={old:.3f}  fixed={new:.3f}")

# ---- 3. live dose curve with the FIXED statistic ----------------------------
print("\n[live env, 3 eps x T=600] FIXED closure vs dose (env_contingency from H_013 for reference):")
for pp in H.DOSES:
    new = sum(lv_c_dose_fixed(R.policy_live, seed + e, T, pp, null=False) for e in range(3)) / 3
    old = sum(lv_c_dose_old(R.policy_live, seed + e, T, pp, null=False) for e in range(3)) / 3
    print(f"    p={pp:.2f}  old={old:.3f}  fixed={new:.3f}")

# ---- 4. H_011 scripted anchor + open plant with the FIXED statistic ---------
def lv_c_fixed(policy, seed, T, null=False):
    return lv_c_dose_fixed(policy, seed, T, 1.0, null=null)
live_fixed = lv_c_fixed(R.policy_live, 7, 600, null=False)
open_tape = R._derange(R.run_episode(R.policy_live, 7, 600, ab=False)["tape"], 7, 9)
openp = R.make_tape_policy(open_tape)
open_fixed = lv_c_fixed(openp, 8, 600, null=False)
print(f"\n[H_011 scripted plants, seed 7, T=600] gate {R.CLOSURE_SIGN} (pre-repair: live 0.750, open 0.417)")
print(f"    P-LIVE closure fixed={live_fixed:.3f}")
print(f"    P-OPEN closure fixed={open_fixed:.3f}")
