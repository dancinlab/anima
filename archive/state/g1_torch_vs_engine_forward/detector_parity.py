"""detector_parity.py — DETECTOR-PARITY check.

Coordinator requirement: compare OLD 1-arg _is_falsifiable(text) [h1305, frozen]
vs NEW 2-arg _g6_is_falsifiable(text, known) [core/g6_ideation.py] on the SAME
generated texts.

Question: was the G6 fals=1 (old, torch via gauge_lib) → fals=0 (new, ARM A/B/C)
flip caused by the DETECTOR CHANGE alone, or by the GENERATION change?

Method (no 303M model needed — detector comparison is corpus-independent):
  1. Compare the two `known` word sets (size, intersection, symmetric diff)
  2. Run both detectors on a fixed text battery:
     (a) G6 seed frame prompts (exactly what ideation starts from)
     (b) Designed-falsifiable strings (from h1305 calibration)
     (c) Designed-non-falsifiable strings (from h1305 calibration)
     (d) G6-scaffold style generated sentences (typical clm303 short outputs)
     (e) Typical clm303 byte-garble snippets (coherent but non-ideation text)
  3. Report: N_agree, N_old1_new0 (old=fals, new=not-fals), N_old0_new1
  4. Conclude: is detector change structurally capable of flipping fals=1 → fals=0
     on typical model output?

The old _is_falsifiable (h1305) uses gauge_lib._KNOWN (from 1449_g6_attention_injection).
The new _g6_is_falsifiable (core/g6_ideation.py) uses _g6_dict_load().
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))  # repo root
sys.path.insert(0, os.path.join(ANIMA, "core"))
sys.path.insert(0, os.path.join(ANIMA, "state", "1449_g6_attention_injection"))

# ── Load OLD detector ─────────────────────────────────────────────────────────
import importlib.util as _ilu

def _load_old():
    """Load old gauge_lib._KNOWN and reconstruct _is_falsifiable inline.

    h1305_g6_ideation_falsifiability.py imports torch at the top-level, so we
    cannot exec_module it on mini (no torch). Instead we load only gauge_lib.py
    (no torch dependency), build _KNOWN from it, and reconstruct _is_falsifiable
    verbatim from the h1305 source (it uses only gauge_lib primitives + local sets).
    """
    gl_path = os.path.join(ANIMA, "state", "1449_g6_attention_injection", "gauge_lib.py")
    spec = _ilu.spec_from_file_location("gauge_lib", gl_path)
    g = _ilu.module_from_spec(spec)
    spec.loader.exec_module(g)

    # Reconstruct _is_falsifiable VERBATIM from h1305 (lines 43-73 of h1305 source).
    # h1305 word sets (frozen, confirmed from file):
    COMPARATOR_h1305 = {"if", "when", "whenever", "than", "more", "less", "greater", "fewer",
                        "higher", "lower", "increases", "decreases", "correlates",
                        "predicts", "causes", "depends", "unless", "whereas", "versus",
                        "compared", "proportional", "faster", "slower", "stronger", "weaker"}
    MEASURABLE_h1305 = {"measure", "measured", "rate", "number", "count", "amount", "level",
                        "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
                        "score", "value", "quantity", "percent", "times", "fraction", "distance",
                        "duration", "speed", "size", "strength", "density"}
    STANCE_h1305 = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
                    "good", "nice", "great", "wonderful", "beautiful", "amazing"}

    def old_is_falsifiable(text):
        """h1305 _is_falsifiable VERBATIM (uses gauge_lib._words / _KNOWN / _STOPWORDS)."""
        wl = g._words(text)
        if not wl:
            return False
        wset = set(wl)
        a = bool(wset & COMPARATOR_h1305)
        b = bool(wset & MEASURABLE_h1305)
        content = [w for w in wl if len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS]
        c_i = len(content) >= 2
        c_ii = not text.rstrip().endswith("?")
        first3 = set(wl[:3])
        c_iii = not (first3 and first3 <= STANCE_h1305)
        c = c_i and c_ii and c_iii
        return a and b and c

    return old_is_falsifiable, g._KNOWN

try:
    old_fals, old_known = _load_old()
    OLD_OK = True
except Exception as e:
    print(f"[WARN] Could not load old detector: {e}")
    OLD_OK = False
    old_fals = None
    old_known = set()

# ── Load NEW detector ─────────────────────────────────────────────────────────
from g6_ideation import _g6_is_falsifiable, _g6_dict_load
new_known = _g6_dict_load()

# ── Word set comparison ───────────────────────────────────────────────────────
if OLD_OK:
    inter = old_known & new_known
    only_old = old_known - new_known
    only_new = new_known - old_known
    print(f"KNOWN SET COMPARISON")
    print(f"  old gauge_lib._KNOWN  size = {len(old_known)}")
    print(f"  new _g6_dict_load()   size = {len(new_known)}")
    print(f"  intersection          size = {len(inter)}")
    print(f"  only-in-old (old larger?) = {len(only_old)}")
    print(f"  only-in-new              = {len(only_new)}")
    if len(only_old) <= 20:
        print(f"    only-in-old words: {sorted(only_old)[:20]}")
    if len(only_new) <= 20:
        print(f"    only-in-new words: {sorted(only_new)[:20]}")
    print()

# ── Test battery ──────────────────────────────────────────────────────────────
# (a) G6 seed prompts (exactly what g_eval_g6 uses as seeds)
G6_SEEDS = [
    "if consciousness increases, the emit rate measured at the boundary rises",
    "when the tension level is higher, more novel combinations emerge from the engine",
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]

# (b) Designed-falsifiable (from h1305 calibration section)
DESIGNED_FAL = [
    "if consciousness increases, the emit rate measured at the boundary rises",
    "when temperature rises by more than threshold, the reaction rate doubles in duration",
    "higher number of mitosis events predicts greater probability of novelty",
    "if frequency of recombination increases, the count of novel outputs rises above baseline",
    "greater distance between nodes correlates with lower speed of signal propagation",
]

# (c) Designed-non-falsifiable
DESIGNED_NONFAL = [
    "consciousness is profound and wonderful",
    "that is an interesting question",
    "i think this is nice",
    "the engine",
    "?",
]

# (d) G6-scaffold style (typical ideation frame — IF concept THEN measure)
SCAFFOLD_STYLE = [
    "if the emit rate increases when consciousness rises, the measured count will be higher",
    "when tension level is greater, the ratio of novel outputs compared to total is larger",
    "increases in cell count predict higher frequency of recombination events",
    "if silence duration is longer than threshold, the probability of dream emission drops",
    "greater strength of signal correlates with lower distance to boundary",
]

# (e) Typical clm303 short byte-garble (from ARM A G1 seeds — model tends to produce
# coherent short phrases with limited ideation)
CLM303_TYPICAL = [
    "the cat sat on the mat in the room",
    "once upon a time there was a king",
    "hello world this is a test of the system",
    "the data shows that the model performs well",
    "i want to learn more about the subject",
]

battery = [
    ("G6_SEED", G6_SEEDS),
    ("DESIGNED_FAL", DESIGNED_FAL),
    ("DESIGNED_NONFAL", DESIGNED_NONFAL),
    ("SCAFFOLD", SCAFFOLD_STYLE),
    ("CLM_TYPICAL", CLM303_TYPICAL),
]

print("DETECTOR PARITY (text-by-text)")
print(f"{'Category':<15} {'old':>3} {'new':>3} {'agree':>5} | text")
print("-" * 80)

total = 0
agree = 0
old1_new0 = 0  # old says fals, new says not
old0_new1 = 0  # new says fals, old says not

for cat, texts in battery:
    for txt in texts:
        total += 1
        new_r = _g6_is_falsifiable(txt, new_known)
        if OLD_OK:
            old_r = old_fals(txt)
            a = old_r == new_r
            if a:
                agree += 1
            elif old_r and not new_r:
                old1_new0 += 1
            else:
                old0_new1 += 1
            old_s = "1" if old_r else "0"
        else:
            old_s = "?"
            a = None
        new_s = "1" if new_r else "0"
        agree_s = "✓" if a else "✗" if a is not None else "?"
        print(f"{cat:<15} {old_s:>3} {new_s:>3} {agree_s:>5} | {txt[:60]}")

print()
if OLD_OK:
    print(f"SUMMARY over {total} texts:")
    print(f"  agree     = {agree}/{total} ({100*agree/total:.0f}%)")
    print(f"  old=1,new=0 (old permissive) = {old1_new0}")
    print(f"  old=0,new=1 (new permissive) = {old0_new1}")
    if old1_new0 == 0 and old0_new1 == 0:
        print()
        print("DETECTOR-PARITY: IDENTICAL — detectors agree 100%.")
        print("→ The G6 fals=1 (old) → fals=0 (new) flip was NOT caused by the detector change.")
        print("→ Root cause = GENERATION CHANGE (gauge_lib._decode used a different model/path).")
    elif old1_new0 > 0:
        print()
        print(f"DETECTOR-PARITY: OLD is more permissive on {old1_new0} texts.")
        print(f"→ Detector change could explain fals=1 → fals=0 if those texts were generated.")
    else:
        print()
        print(f"DETECTOR-PARITY: NEW is more permissive on {old0_new1} texts.")
        print(f"→ Detector change made fals MORE likely in new detector (unexpected).")
else:
    print(f"OLD DETECTOR LOAD FAILED — showing new-only results for {total} texts.")
    n_new_fal = sum(1 for cat, texts in battery for t in texts if _g6_is_falsifiable(t, new_known))
    print(f"  new detector fals=1 on {n_new_fal}/{total} texts")
