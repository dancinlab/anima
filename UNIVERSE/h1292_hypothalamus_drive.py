"""
H_1292 — HYPOTHALAMUS / HOMEOSTATIC DRIVE (HD29). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1292_hypothalamus_drive/H_1292_FREEZE.txt (pre-registered
BEFORE this scoring). $0 CPU numpy, gradient-free, 3 seeds [4290,4291,4292], p7.
a_no_llm_frame_trap (hypothalamic homeostasis lens, c15) — NOT an LLM recipe.
ENGINE-TRANSFER UNVERIFIED until R2 (this is a directional mirror of the immune store).

The regulated variable = "grounding satiation" = the recall margin off the immune
store (the SAME signal the H_1290 affect lane reads). The NEW structure is the
SETPOINT + LEAKY TEMPORAL INTEGRAL of the deficit + consummatory RESET — a stateful
homeostat, distinct from the stateless affect read.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
N_FACTS    = 40
DIM        = 64
RECALL_THR = 0.30        # immune store recall threshold (margin = 1 - err/thr)
SPLIT_THR  = 0.30
S_STAR     = 0.5         # homeostatic setpoint (margin midpoint, mirrors Ψ=1/2)
LEAK       = 0.1         # leaky-integral leak λ
KP         = 1.0         # proportional gain
KI         = 0.5         # integral gain (FULL); ABLATED sets KI:=0
T_DEP      = 12          # deprivation ticks
SEEDS      = [4290, 4291, 4292]

CITIES = ["paris","tokyo","cairo","lima","oslo","delhi","quito","accra",
          "minsk","sofia","dakar","amman","tunis","kabul","rabat","hanoi",
          "manila","bogota","ankara","riyadh","kyiv","baku","doha","muscat",
          "tirana","skopje","zagreb","vienna","berlin","madrid","lisbon","rome",
          "athens","dublin","prague","warsaw","helsinki","tallinn","riga","vilnius"]
SUBJECTS = [f"s{i:02d}" for i in range(N_FACTS)]


def fnv_3gram(text, dim=DIM):
    """byte-3gram FNV-1a hash embedding, L2-normalized (matches the engine's key geometry)."""
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=np.float64)
    for i in range(len(b) - 2):
        h = 2166136261
        for j in range(3):
            h ^= b[i + j]
            h = (h * 16777619) & 0xFFFFFFFF
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


class ImmuneStore:
    """minimal mirror of ImmuneMemoryGrow recall — bind a cell per fact, recall =
    best-affinity cell margin, ABSTAIN ("") if no cell within recall_thr."""
    def __init__(self):
        self.protos = []
        self.values = []

    def bind(self, key, value):
        self.protos.append(key)
        self.values.append(value)

    def _nearest(self, key):
        if not self.protos:
            return -1, 1e9
        d = [np.linalg.norm(p - key) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def recall(self, key):
        i, err = self._nearest(key)
        if i < 0 or err > RECALL_THR:
            return ""          # ABSTAIN — no fabrication
        return self.values[i]

    def margin(self, key):
        """grounding satiation s_t = 1 - err/recall_thr, clamped [0,1]."""
        _, err = self._nearest(key)
        m = 1.0 - err / RECALL_THR
        return float(np.clip(m, 0.0, 1.0))


def build_store(seed):
    rng = np.random.default_rng(seed)
    store = ImmuneStore()
    keys = []
    for subj, city in zip(SUBJECTS, [CITIES[i % len(CITIES)] for i in range(N_FACTS)]):
        k = fnv_3gram(f"{subj} lives in {city}")
        store.bind(k, city)
        keys.append(k)
    # far / never-seen keys for the deprivation phase (ungrounded by construction)
    far = []
    for _ in range(T_DEP):
        r = rng.standard_normal(DIM)
        r = r / (np.linalg.norm(r) + 1e-9)
        far.append(r)
    return store, keys, far


def homeostat(satiations, ki, reset_on_consummate=True):
    """PI homeostat over a satiation sequence. Returns the drive trajectory.
    deficit = max(0, S* - s); I = (1-λ)I + deficit; drive = Kp*deficit + Ki*I;
    consummatory reset: if s >= S* -> I := 0."""
    I = 0.0
    drives = []
    for s in satiations:
        deficit = max(0.0, S_STAR - s)
        I = (1.0 - LEAK) * I + deficit
        drive = KP * deficit + ki * I
        if reset_on_consummate and s >= S_STAR:
            I = 0.0
            drive = KP * deficit + ki * I   # post-reset drive (integral cleared)
        drives.append(drive)
    return np.array(drives)


def run_seed(seed):
    store, keys, far = build_store(seed)

    # ── PHASE-DEPRIVE: feed T_DEP ungrounded far keys (low satiation) then ──
    # ── PHASE-CONSUMMATE: 1 grounded key (high satiation → reset). ──
    deprive_sat = np.array([store.margin(f) for f in far])     # all low (ungrounded)
    consummate_sat = store.margin(keys[0])                      # grounded → high

    sat_seq = np.concatenate([deprive_sat, [consummate_sat]])

    drive_full = homeostat(sat_seq, KI)
    drive_abl  = homeostat(sat_seq, 0.0)                        # Ki=0 → stateless proportional

    # SHUFFLE control: permute the DEPRIVE deficit order, keep the consummate last.
    rng = np.random.default_rng(seed + 999)
    perm = rng.permutation(T_DEP)
    sat_shuf = np.concatenate([deprive_sat[perm], [consummate_sat]])
    drive_shuf = homeostat(sat_shuf, KI)

    # affect read (H_1290 mirror) over the deprive block with CONTEXT HELD FIXED
    # (same key every tick) — to show affect is FLAT (no time term) vs drive RISES.
    fixed_key = far[0]
    aff_vals = []
    for _ in range(T_DEP):
        m = store.margin(fixed_key)
        _, err = store._nearest(fixed_key)
        grounded = err <= RECALL_THR
        margin = m
        contradiction = 0.0 if grounded else 1.0
        valence = margin - contradiction          # affect_valence mirror
        aff_vals.append(valence)
    aff_vals = np.array(aff_vals)
    # the FULL drive over the SAME fixed-context deprive block:
    fixed_sat = np.array([store.margin(fixed_key)] * T_DEP)
    drive_fixed = homeostat(fixed_sat, KI, reset_on_consummate=True)

    # ── metrics ──
    dep_full = drive_full[:T_DEP]
    rise_full = dep_full[-1] - dep_full[0]
    monotone = bool(np.all(np.diff(dep_full) >= -1e-9))
    reset_drop = drive_full[T_DEP]                              # drive after consummate
    end_dep = dep_full[-1]

    dep_abl = drive_abl[:T_DEP]
    rise_abl = dep_abl[-1] - dep_abl[0]

    shuf_buildup = drive_shuf[:T_DEP][-1] - drive_shuf[:T_DEP][0]
    shuf_reset = drive_shuf[T_DEP]

    aff_flat = float(aff_vals.max() - aff_vals.min())
    drive_fixed_rise = drive_fixed[-1] - drive_fixed[0]

    # ABSTAIN intact: an untaught far key fires no cell.
    abstain_ok = (store.recall(far[0]) == "")

    return dict(
        rise_full=float(rise_full), monotone=monotone, end_dep=float(end_dep),
        reset_drop=float(reset_drop), rise_abl=float(rise_abl),
        shuf_buildup=float(shuf_buildup), shuf_reset=float(shuf_reset),
        aff_flat=aff_flat, drive_fixed_rise=float(drive_fixed_rise),
        abstain_ok=bool(abstain_ok),
        full_traj=dep_full.tolist(),
    )


def main():
    print("H_1292 — HYPOTHALAMUS / HOMEOSTATIC DRIVE (HD29) — R1 numpy MIRROR (DIRECTIONAL)")
    print("=" * 79)
    print(f"frozen: S*={S_STAR} λ={LEAK} Kp={KP} Ki={KI} | N={N_FACTS} T_dep={T_DEP} | seeds={SEEDS}")
    print("ENGINE-TRANSFER UNVERIFIED (mirror) — R2 engine-native is the binding verdict.\n")

    rows = [run_seed(s) for s in SEEDS]

    def m(k): return float(np.mean([r[k] for r in rows]))

    print(f"{'seed':>6} {'riseFULL':>9} {'mono':>5} {'reset':>7} {'endDep':>7} "
          f"{'riseABL':>8} {'shufRst':>8} {'affFlat':>8} {'drvFixRise':>11} {'abstain':>8}")
    for s, r in zip(SEEDS, rows):
        print(f"{s:>6} {r['rise_full']:>9.4f} {str(r['monotone']):>5} {r['reset_drop']:>7.4f} "
              f"{r['end_dep']:>7.4f} {r['rise_abl']:>8.4f} {r['shuf_reset']:>8.4f} "
              f"{r['aff_flat']:>8.4f} {r['drive_fixed_rise']:>11.4f} {str(r['abstain_ok']):>8}")

    print()
    # ── frozen bars (per-seed AND mean) ──
    a1 = all(r['monotone'] and r['rise_full'] >= 0.50 for r in rows)
    a2 = all(r['reset_drop'] <= 0.50 * r['end_dep'] for r in rows)
    b  = all(r['aff_flat'] < 0.05 and r['drive_fixed_rise'] >= 0.50 for r in rows)
    c1 = all(r['rise_abl'] < 0.10 for r in rows)
    c2 = all(r['shuf_reset'] < 0.50 * r['rise_full'] for r in rows)
    d  = all(r['abstain_ok'] for r in rows)

    print("FROZEN BARS (all must hold per-seed):")
    print(f"  (A1) RISE     monotone & rise>=0.50           : {a1}  (mean rise={m('rise_full'):.4f})")
    print(f"  (A2) RESET    drop<=0.50*end_dep              : {a2}  (mean reset={m('reset_drop'):.4f}, mean endDep={m('end_dep'):.4f})")
    print(f"  (B)  DISTINCT affFlat<0.05 & drvFixRise>=0.50 : {b}  (mean affFlat={m('aff_flat'):.4f}, mean drvFixRise={m('drive_fixed_rise'):.4f})")
    print(f"  (C1) EARNED   ablated rise<0.10               : {c1}  (mean riseABL={m('rise_abl'):.4f})")
    print(f"  (C2) SHUFFLE  shufReset<0.50*riseFULL         : {c2}  (mean shufReset={m('shuf_reset'):.4f})")
    print(f"  (D)  ABSTAIN  untaught far key fires no cell  : {d}")

    green = a1 and a2 and b and c1 and c2 and d
    print()
    print("VERDICT (R1 mirror, DIRECTIONAL):", "🟢 GREEN" if green else "🧱 CLOSED-NEGATIVE")
    print("  (engine-transfer UNVERIFIED — R2 engine-native re-score is the binding verdict)")
    return green


if __name__ == "__main__":
    ok = main()
    import sys
    sys.exit(0 if ok else 1)
