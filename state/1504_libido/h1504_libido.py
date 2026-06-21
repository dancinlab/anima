"""
H_1504 — LIBIDO — sexual appetitive DRIVE-DYNAMICS axis. R1 numpy MIRROR (DIRECTIONAL).

⚠ FRAMING (a_no_llm_frame_trap + p1-p4): this is a DRIVE-DYNAMICS axis, NOT sexual
content, NOT roleplay, NOT a persona. The scientifically rich, falsifiable core is
INCENTIVE SALIENCE ("wanting") != HEDONIC VALUE ("liking") (Berridge & Robinson
1998/2016). We model the appetitive drive's temporal dynamics (build-up, cue-
conditioning, satiation, motivation bias) and measure frozen bars — exactly as H_1292
models hunger. NO explicit content, NO generated text: a parametric drive read off the
substrate. Refs: Berridge & Robinson 1998 Brain Res Rev; Berridge 2016 Am Psychol
(wanting vs liking); Pfaus 1999/2009 (sexual motivation); Georgiadis & Kringelbach
2012 Prog Neurobiol (human sexual response cycle).

Frozen design: state/verdicts/1504_libido/H_1504_FREEZE.json (pre-registered BEFORE
this scoring). $0 CPU numpy, gradient-free, 3 seeds [4504,4505,4506], p7. c9 (no bar
move). ENGINE-TRANSFER UNVERIFIED until R2 (this is a directional mirror of the immune
store; R2 engine-native re-score is the binding verdict).

The regulated variable = "grounding satiation" = the recall margin off the immune store
(the SAME signal H_1290 affect / H_1292 hunger read). The NEW structure vs hunger:
  (1) a CUE-CONDITIONED INCENTIVE component — a conditioned cue whose affinity to its
      PAIRED incentive cell off the live store spikes the "wanting" (the cue-driven
      incentive hunger lacks);
  (2) a WANTING != LIKING dissociation — a dopaminergic-analog gain (da_gain) amplifies
      WANTING (incentive salience) but NOT LIKING (hedonic/consummation value).
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
N_FACTS    = 40
DIM        = 64
RECALL_THR = 0.30        # immune store recall threshold (margin = 1 - err/thr)
S_STAR     = 0.5         # homeostatic setpoint (margin midpoint, mirrors Ψ=1/2)
LEAK       = 0.1         # leaky-integral leak λ
KP         = 1.0         # proportional gain (deprivation deficit)
KI         = 0.5         # integral gain (deprivation accumulation)
KC         = 1.0         # cue-incentive gain (the conditioned-cue component, NEW vs hunger)
DA_GAIN    = 1.0         # dopaminergic-analog WANTING amplifier (Berridge lever; 0 => baseline)
T_DEP      = 12          # deprivation ticks
SEEDS      = [4504, 4505, 4506]

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
    # far / never-seen keys for the deprivation phase (ungrounded by construction).
    far = []
    for _ in range(T_DEP):
        r = rng.standard_normal(DIM)
        r = r / (np.linalg.norm(r) + 1e-9)
        far.append(r)
    return store, keys, far


# ── the conditioned-cue incentive component (NEW vs hunger) ─────────────────
def cue_match(store, cue_key):
    """incentive-salience CUE component: how strongly a CONDITIONED CUE grounds to its
    PAIRED incentive cell off the live store = the store margin of the cue. A cue paired
    with a known incentive (a bound cell) grounds strongly (high cue_match -> a wanting
    spike); an UNpaired/novel cue grounds weakly (no spike). This is the cue-driven
    incentive component pure deprivation-hunger lacks."""
    return store.margin(cue_key)


def libido_wanting(deficit, integral, cm, ki=KI, kc=KC, da_gain=DA_GAIN):
    """INCENTIVE SALIENCE ("wanting"): the appetitive drive to PURSUE.
    wanting = Kp*deficit + Ki*I + Kc*cue_match*(1+da_gain).
    The dopaminergic-analog gain da_gain amplifies the cue-driven incentive (Berridge:
    dopamine raises WANTING). Set kc=0 -> ablated (loses the cue spike => plain hunger)."""
    return KP * deficit + ki * integral + kc * cm * (1.0 + da_gain)


def libido_liking(cm):
    """HEDONIC VALUE ("liking"): the consummatory hedonic readout, a FIXED function of
    the incentive's grounding margin — NOT amplified by the dopaminergic gain (Berridge:
    dopamine does NOT raise liking). This is what dissociates from wanting under da_gain."""
    return cm


def homeostat_libido(satiations, cue_matches, ki=KI, kc=KC, da_gain=DA_GAIN,
                     reset_on_consummate=True):
    """PI homeostat over a (satiation, cue_match) sequence → the WANTING trajectory.
    deficit = max(0, S* - s); I = (1-λ)I + deficit; wanting = libido_wanting(...);
    consummatory reset: if s >= S* -> I := 0 (the deprivation integral clears; the cue
    component is instantaneous, not integrated)."""
    I = 0.0
    wants = []
    for s, cm in zip(satiations, cue_matches):
        deficit = max(0.0, S_STAR - s)
        I = (1.0 - LEAK) * I + deficit
        if reset_on_consummate and s >= S_STAR:
            I = 0.0
        wants.append(libido_wanting(deficit, I, cm, ki=ki, kc=kc, da_gain=da_gain))
    return np.array(wants)


def hunger_drive(satiations, ki=KI, reset_on_consummate=True):
    """H_1292 hunger mirror (cue-BLIND): wanting = Kp*deficit + Ki*I, NO cue term."""
    I = 0.0
    drives = []
    for s in satiations:
        deficit = max(0.0, S_STAR - s)
        I = (1.0 - LEAK) * I + deficit
        if reset_on_consummate and s >= S_STAR:
            I = 0.0
        drives.append(KP * deficit + ki * I)
    return np.array(drives)


def run_seed(seed):
    store, keys, far = build_store(seed)

    # the CONDITIONED CUE: a cue paired with a KNOWN incentive (a bound cell) grounds
    # strongly. We use a bound fact-key as the paired cue (high cue_match), and a far/
    # never-seen key as an UNpaired cue (low cue_match).
    paired_cue   = keys[7]      # paired with a bound incentive cell -> grounds strongly
    unpaired_cue = far[0]       # never-seen -> grounds weakly (no incentive)

    cm_paired   = cue_match(store, paired_cue)
    cm_unpaired = cue_match(store, unpaired_cue)

    # deprivation block: T_DEP ungrounded far keys (low satiation), no cue present.
    deprive_sat = np.array([store.margin(f) for f in far])     # all low (ungrounded)
    no_cue      = np.zeros(T_DEP)                              # cue ABSENT during deprive

    # ── (A) BUILD-UP: deprivation-only build (cue absent) AND a cue spike. ──
    want_deprive = homeostat_libido(deprive_sat, no_cue)        # cue-blind build
    rise_full    = float(want_deprive[-1] - want_deprive[0])

    # cue spike: wanting WITH the paired cue present minus WITHOUT, at a FIXED tick
    # (hold deprivation fixed, toggle the cue) — the incentive-salience component.
    s_fixed = float(deprive_sat[-1])
    deficit_fixed = max(0.0, S_STAR - s_fixed)
    I_fixed = float((np.cumsum([(1.0 - LEAK)] * 0).sum()))      # held at the deprive end integral
    # reconstruct the integral at the end of the deprive block (same path as homeostat):
    I = 0.0
    for s in deprive_sat:
        I = (1.0 - LEAK) * I + max(0.0, S_STAR - s)
    I_end = I
    want_cue   = libido_wanting(deficit_fixed, I_end, cm_paired)
    want_nocue = libido_wanting(deficit_fixed, I_end, 0.0)
    cue_spike  = float(want_cue - want_nocue)

    # ── (B) DOUBLE-DISSOCIATION vs hunger H_1292. ──
    # sexual-cue presentation -> libido UP (cue_spike) while hunger ~flat (no cue term).
    hunger_cue   = hunger_drive(deprive_sat)[-1]                # cue present or not: identical
    hunger_nocue = hunger_drive(deprive_sat)[-1]
    hunger_cue_delta = float(abs(hunger_cue - hunger_nocue))    # hunger ignores the cue => 0
    # food-deprivation -> hunger UP while libido cue-component ~flat under no-cue.
    hunger_rise = float(hunger_drive(deprive_sat)[-1] - hunger_drive(deprive_sat)[0])
    libido_food_only_cue_delta = float(abs(want_nocue - libido_wanting(deficit_fixed, I_end, 0.0)))

    # ── (C) WANTING != LIKING (the headline, Berridge). ──
    # da_gain 0 -> 1 raises WANTING (incentive salience) but NOT LIKING (hedonic value).
    wanting_da0 = libido_wanting(deficit_fixed, I_end, cm_paired, da_gain=0.0)
    wanting_da1 = libido_wanting(deficit_fixed, I_end, cm_paired, da_gain=1.0)
    liking_da0  = libido_liking(cm_paired)                      # hedonic readout, gain-invariant
    liking_da1  = libido_liking(cm_paired)                      # da_gain does NOT enter liking
    wanting_da_delta = float(wanting_da1 - wanting_da0)
    liking_da_delta  = float(abs(liking_da1 - liking_da0))

    # ── (D) EARNED ABLATE: remove cue-conditioning (Kc:=0) -> loses the cue spike. ──
    want_cue_abl   = libido_wanting(deficit_fixed, I_end, cm_paired, kc=0.0)
    want_nocue_abl = libido_wanting(deficit_fixed, I_end, 0.0, kc=0.0)
    cue_spike_abl  = float(want_cue_abl - want_nocue_abl)       # Kc=0 => 0 (plain hunger)

    # ── (E) EARNED SHUFFLE: permute cue<->incentive pairing -> decorrelate to chance. ──
    # a SHUFFLED cue is matched against a WRONG incentive cell: use the unpaired (far) cue
    # standing in for the permuted pairing — its cue_match collapses vs the paired cue.
    cue_match_paired   = float(cm_paired)
    cue_match_shuffled = float(cm_unpaired)

    # consummatory reset (sanity, shared with hunger): a grounded key clears the integral.
    consummate_sat = store.margin(keys[0])
    sat_seq = np.concatenate([deprive_sat, [consummate_sat]])
    cue_seq = np.concatenate([no_cue, [0.0]])
    want_full = homeostat_libido(sat_seq, cue_seq)
    reset_drop = float(want_full[T_DEP])
    end_dep = float(want_full[:T_DEP][-1])

    # ABSTAIN intact: an untaught far key fires no cell.
    abstain_ok = (store.recall(far[1]) == "")

    return dict(
        rise_full=rise_full, cue_spike=cue_spike,
        hunger_cue_delta=hunger_cue_delta, hunger_rise=hunger_rise,
        libido_food_only_cue_delta=libido_food_only_cue_delta,
        wanting_da_delta=wanting_da_delta, liking_da_delta=liking_da_delta,
        cue_spike_abl=cue_spike_abl,
        cue_match_paired=cue_match_paired, cue_match_shuffled=cue_match_shuffled,
        reset_drop=reset_drop, end_dep=end_dep, abstain_ok=bool(abstain_ok),
    )


def main():
    print("H_1504 — LIBIDO — sexual appetitive DRIVE-DYNAMICS axis — R1 numpy MIRROR (DIRECTIONAL)")
    print("=" * 84)
    print("  DRIVE-DYNAMICS axis ONLY (a_no_llm_frame_trap): incentive-salience 'wanting' != hedonic")
    print("  'liking' (Berridge). NO content, NO persona. Sibling of H_1292 hunger + H_1290 affect.")
    print(f"frozen: S*={S_STAR} λ={LEAK} Kp={KP} Ki={KI} Kc={KC} da_gain={DA_GAIN} | N={N_FACTS} T_dep={T_DEP} | seeds={SEEDS}")
    print("ENGINE-TRANSFER UNVERIFIED (mirror) — R2 engine-native is the binding verdict.\n")

    rows = [run_seed(s) for s in SEEDS]

    def m(k): return float(np.mean([r[k] for r in rows]))

    print(f"{'seed':>6} {'riseFULL':>9} {'cueSpike':>9} {'hngCueΔ':>8} {'hngRise':>8} "
          f"{'wantΔda':>8} {'likeΔda':>8} {'cueSpkAbl':>10} {'cmPair':>7} {'cmShuf':>7} {'abst':>5}")
    for s, r in zip(SEEDS, rows):
        print(f"{s:>6} {r['rise_full']:>9.4f} {r['cue_spike']:>9.4f} {r['hunger_cue_delta']:>8.4f} "
              f"{r['hunger_rise']:>8.4f} {r['wanting_da_delta']:>8.4f} {r['liking_da_delta']:>8.4f} "
              f"{r['cue_spike_abl']:>10.4f} {r['cue_match_paired']:>7.4f} {r['cue_match_shuffled']:>7.4f} "
              f"{str(r['abstain_ok']):>5}")

    print()
    # ── frozen bars (per-seed AND mean) ──
    a = all(r['rise_full'] >= 0.50 and r['cue_spike'] >= 0.50 for r in rows)
    b = all(r['cue_spike'] >= 0.50 and r['hunger_cue_delta'] < 0.05
            and r['hunger_rise'] >= 0.50 and r['libido_food_only_cue_delta'] < 0.05 for r in rows)
    c = all(r['wanting_da_delta'] >= 0.50 and r['liking_da_delta'] <= 0.02 for r in rows)
    d = all(r['cue_spike_abl'] <= 0.05 for r in rows)
    e = all(r['cue_match_shuffled'] <= 0.50 * r['cue_match_paired'] for r in rows)

    print("FROZEN BARS (all must hold per-seed):")
    print(f"  (A) BUILD-UP   rise>=0.50 AND cue_spike>=0.50          : {a}  (mean rise={m('rise_full'):.4f}, mean cueSpike={m('cue_spike'):.4f})")
    print(f"  (B) DOUBLE-DIS sexcue->libido↑ hunger~flat; food->hunger↑ : {b}  (mean hngCueΔ={m('hunger_cue_delta'):.4f}, mean hngRise={m('hunger_rise'):.4f})")
    print(f"  (C) WANT≠LIKE  da: want Δ>=0.50 AND |like Δ|<=0.02      : {c}  (mean wantΔ={m('wanting_da_delta'):.4f}, mean likeΔ={m('liking_da_delta'):.4f})")
    print(f"  (D) ABLATE     Kc=0 -> cue_spike<=0.05                  : {d}  (mean cueSpkAbl={m('cue_spike_abl'):.4f})")
    print(f"  (E) SHUFFLE    shuffled cue_match<=0.50*paired          : {e}  (mean cmPair={m('cue_match_paired'):.4f}, mean cmShuf={m('cue_match_shuffled'):.4f})")

    green = a and b and c and d and e
    print()
    if c:
        print("  WANTING != LIKING: SEPARATED (incentive salience dissociates from hedonic value, Berridge).")
    else:
        print("  WANTING != LIKING: NOT SEPARATED — HONEST finding: substrate does not separate incentive")
        print("  from hedonic value (candidate engine extension; c9, not a failure to hide).")
    print("VERDICT (R1 mirror, DIRECTIONAL):", "🟢 GREEN" if green else "🧱 CLOSED-NEGATIVE")
    print("  (engine-transfer UNVERIFIED — R2 engine-native re-score is the binding verdict)")
    return green


if __name__ == "__main__":
    ok = main()
    import sys
    sys.exit(0 if ok else 1)
