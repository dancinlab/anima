# TASK
Adversarially review + tighten this PRE-REGISTRATION for a G6 corpus-density experiment
in the `anima` repo. Return: (1) fatal flaws, (2) the decision table you would freeze,
(3) the minimum control set, (4) what would make this a FORGERY that I have missed.
Be brutal. I would rather kill this before it burns compute.

# GROUND TRUTH (read from the repo today — verbatim from code)

## What G6 actually is (cli/evaluate.py::eval_rho_fan)
- 6 frames are built from a HARDCODED 5-concept pool (core/rho_fan.py::_rho_fan_concepts):
    "consciousness arises from cells" / "tension ripples between distant minds" /
    "memory composes into new meaning" / "silence still carries information" /
    "the engine dreams when alone"
  composed frame shape = `if cA, then cB: `
- For each frame: mouth.ideate(frame, gen, 40 bytes, temp 0.7, seed 7+i)
- An output counts as "coherent" only if known_word_ratio >= 0.5
- dist = number of distinct outputs (pairwise Jaccard < 0.5)
- PASS  <=>  dist >= 5  AND  fals >= 1
- There is an echo-guard telemetry (_echo_ratio frame vs output).

## What "falsifiable" means (core/rho_fan.py::_rho_fan_is_falsifiable) — ALL must hold
  (a) >=1 word from COMPARATOR set {if,when,whenever,than,more,less,greater,fewer,higher,
      lower,increases,decreases,correlates,predicts,causes,depends,unless,whereas,versus,
      compared,proportional,faster,slower,stronger,weaker}
  (b) >=1 word from MEASURABLE set {measure,measured,rate,number,count,amount,level,degree,
      threshold,ratio,frequency,probability,magnitude,score,value,quantity,percent,times,
      fraction,distance,duration,speed,size,strength,density}
  (c) >=2 content words: len>=3 AND in `known` AND not a stopword
  (d) text does NOT end in '?'
  (e) the first 3 words are not ALL stance words {that,s,a,profound,question,i,think,
      interesting,good,nice,great,wonderful,beautiful,amazing}
- `known` = stopwords + the 5 concept words + /usr/share/dict/words  (NOT corpus-derived,
  so there is no corpus<->detector vocabulary circularity).

## The claim being tested
Measurement #4253 reframed G6 as a CORPUS-DENSITY wall, not a faculty wall:
  the model DOES emit falsifiable claims at 1/241 = 0.0041, faithful to the corpus rate
  0.0065 (P = 0.539, i.e. statistically indistinguishable from corpus-faithful).
  The gate needs ~0.083; that is 12.8x outside (P(<=1 | p>=0.083) = 4.3e-8).
Prediction: raise corpus falsifiable-claim density ~13x => generation rate rises
proportionally => gate passes.

# MY PROPOSED DESIGN (attack this)

## The corpus builder — a NEW format `falsdense` on `anima-py corpus` (a flag on the
## canonical CLI, per repo law: a new manipulation is a flag, never a side script)
- `anima-py corpus falsdense --out c.txt --lang en --fals-density D --seed S`
- Emits EN lines over a concept pool that is **DISJOINT from the 5 eval concepts**.
  The hypothesis is that falsifiable-claim STRUCTURE transfers to unseen content;
  putting the eval concepts in the corpus would be memorisation => false GREEN.
- A fraction D of lines satisfy (a)-(e); the remaining (1-D) are filler matched on
  length + vocabulary richness so the ONLY thing that varies across arms is
  falsifiability structure, not fluency or byte budget.
- After building, the builder RE-MEASURES its own output with the very same
  `_rho_fan_is_falsifiable` and reports the ACHIEVED density (never the requested one).

## Arms (density ladder — a single point cannot separate "corpus works" from
## "any perturbation works")
  D = 0.0065 (observed baseline)  /  0.02  /  0.083 (gate)  /  0.25 (overshoot)
Prediction if the corpus hypothesis is TRUE: generated fals-rate is MONOTONE in D.

## Controls
  C1 word-shuffle: same lines, words shuffled within the line => comparator+measurable
     still PRESENT but the structure is destroyed; byte-identical budget. If C1 lifts
     too, the lever is bag-of-words, not claim structure.
  C2 stance-swap: replace comparator/measurable words with matched-frequency NON-detector
     words => density collapses to ~0 at identical fluency.
  C3 echo-guard: the eval echo_ratio must NOT rise with D (else the model is parroting).
  C4 held-out concept: eval concepts never appear in ANY arm's corpus (verified by grep).
  C5 FORGET gate: rho.form / rho.weave / rho.tether / rho.store must not DROP
     (small-corpus CPT is known in this repo to kill abilities the corpus omits).

## Frozen reading BEFORE any number is produced
  - GREEN requires: fals-rate monotone in D  AND  gate passes at D=0.083
    AND C1 does not lift AND C2 does not lift AND echo_ratio flat AND no FORGET drop.
  - If the gate passes but dist COLLAPSES (<5) => template echo => INVALID, not a pass.
  - If the gate passes at D=0.083 but ALSO at C1 => the lever is not falsifiability.
  - If fals-rate is flat across the whole ladder => the corpus hypothesis is REFUTED
    and G6 goes back to being a faculty/substrate wall. This is a WANTED outcome, not
    a failure — no tune-to-green, no re-freezing the bar.

# KNOWN REPO LESSONS I MUST NOT VIOLATE
- No tune-to-green; a negative is a result. Bars are frozen VERBATIM, never re-anchored.
- A prereg decision table must cover the BELOW-CHANCE cells too.
- Chance level must be re-derived per metric from the realized partition.
- Uniform draws hide adversarial fragility (add an adversarial arm if you think it matters).
- A cheap structural screen may only KILL, never GREEN.
- Replication within one condition is not external validity.
- Only `anima-py` output can cement; everything else is DIRECTIONAL.

# QUESTIONS
1. Fatal flaws in the above? Rank them.
2. Is the disjoint-concept-pool choice right, or does it make the test impossible
   (i.e. is there any route by which structure transfers WITHOUT content overlap)?
3. Is the monotonicity prediction the right primary DV, or is there a better one?
4. What is the cheapest arm that could KILL this whole plan before I spend GPU?
5. Name the forgery mode I have not listed.
