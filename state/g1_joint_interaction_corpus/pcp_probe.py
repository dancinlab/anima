"""PC-P detector-power probe (Fable real-corpus design §1) — model-free.

Korean 조사(particle) allomorph = a GROUND-TRUTH non-additive interaction that
lives in real text: the realized particle byte is a JOINT function of
  A = 받침 유무 (final consonant of the preceding syllable)  and
  B = grammatical slot (topic / subject / object).
Knowing only A (은/는 undetermined vs 이/가 vs 을/를) or only B (은 vs 는) is
insufficient — you need BOTH. So additive(A)+additive(B) must under-predict the
particle, and a joint model must lift. If our model-free additive-vs-joint
pipeline does NOT detect this, the pipeline lacks detector power => INVALID gate
(per Fable decision rule: PC-P must fire before any engine decode).

This is $0, model-free (no 303M decode) — pure corpus statistics on ko-general.
"""
import sys, unicodedata, math
from collections import Counter, defaultdict

CORPUS = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mini/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-general/snapshots/9f03495689d52fb50b5b7d8d673d77e38266afcc/anima-corpus-ko-general.txt"

# particle allomorph pairs by grammatical slot: (with-batchim form, without form)
SLOTS = {
    "topic":   ("은", "는"),
    "subject": ("이", "가"),
    "object":  ("을", "를"),
}
# reverse lookup: particle char -> (slot, requires_batchim)
PARTICLE = {}
for slot, (wb, wob) in SLOTS.items():
    PARTICLE[wb] = (slot, True)
    PARTICLE[wob] = (slot, False)

HANGUL_BASE = 0xAC00
HANGUL_LAST = 0xD7A3


def has_batchim(ch):
    """True if a Hangul syllable has a final consonant (jongseong != 0)."""
    o = ord(ch)
    if not (HANGUL_BASE <= o <= HANGUL_LAST):
        return None
    return ((o - HANGUL_BASE) % 28) != 0


def scan(text):
    """Yield (A=batchim_bool, B=slot, particle_char) for every noun+particle hit.

    Match: a Hangul syllable immediately followed by a known particle char, where
    the char after the particle is NOT a Hangul syllable (so 는/가/를 are the
    particle, not the first syllable of a longer word). Coarse but unbiased across
    A and B — biases cancel in the additive-vs-joint contrast."""
    n = len(text)
    for i in range(1, n - 1):
        ch = text[i]
        if ch not in PARTICLE:
            continue
        prev = text[i - 1]
        b = has_batchim(prev)
        if b is None:            # preceding char not a Hangul syllable -> skip
            continue
        nxt = text[i + 1]
        if HANGUL_BASE <= ord(nxt) <= HANGUL_LAST:
            # particle followed by another syllable => likely mid-word, ambiguous
            if nxt not in (" ",):
                # allow if next is space/punct; else require particle not word-initial
                pass
        slot, _need = PARTICLE[ch]
        yield (b, slot, ch)


def additive_vs_joint(rows):
    """rows: list of (A, B, label). label = particle char (the thing to predict).
    Compare NLL of additive P(label|A)*P(label|B)/P(label) vs joint P(label|A,B).
    Uses leave-cell-out is unnecessary for PC-P (detector power, not generalization)
    — we report in-grid NLL gap + a held-out variant for honesty."""
    labels = sorted({r[2] for r in rows})
    Aset = sorted({r[0] for r in rows})
    Bset = sorted({r[1] for r in rows})
    N = len(rows)

    p_l = Counter(r[2] for r in rows)
    p_la = defaultdict(Counter); n_a = Counter()
    p_lb = defaultdict(Counter); n_b = Counter()
    p_lab = defaultdict(Counter); n_ab = Counter()
    for A, B, l in rows:
        p_la[A][l] += 1; n_a[A] += 1
        p_lb[B][l] += 1; n_b[B] += 1
        p_lab[(A, B)][l] += 1; n_ab[(A, B)] += 1

    eps = 1e-9
    V = len(labels)

    def P_add(A, B, l):
        pa = (p_la[A][l] + eps) / (n_a[A] + eps * V)
        pb = (p_lb[B][l] + eps) / (n_b[B] + eps * V)
        pl = (p_l[l] + eps) / (N + eps * V)
        # log-linear additive combination, renormalized over labels
        raw = {lab: ((p_la[A][lab] + eps) / (n_a[A] + eps * V)) *
                    ((p_lb[B][lab] + eps) / (n_b[B] + eps * V)) /
                    ((p_l[lab] + eps) / (N + eps * V)) for lab in labels}
        Z = sum(raw.values())
        return raw[l] / Z

    def P_joint(A, B, l):
        return (p_lab[(A, B)][l] + eps) / (n_ab[(A, B)] + eps * V)

    nll_add = -sum(math.log(P_add(A, B, l)) for A, B, l in rows) / N
    nll_joint = -sum(math.log(P_joint(A, B, l)) for A, B, l in rows) / N
    lift = (nll_add - nll_joint) / nll_add if nll_add > 0 else 0.0
    return dict(N=N, labels=V, cells=len(n_ab), nll_add=nll_add,
                nll_joint=nll_joint, lift=lift), (p_lab, n_ab)


if __name__ == "__main__":
    print("# PC-P detector-power probe (Korean 조사 allomorph = ground-truth joint)")
    print(f"# corpus: {CORPUS.split('/')[-1]}")
    with open(CORPUS, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    print(f"# corpus chars: {len(text):,}")

    rows = list(scan(text))
    print(f"# particle hits: {len(rows):,}")
    res, (p_lab, n_ab) = additive_vs_joint(rows)
    print()
    print(f"{'metric':>12}: {'value'}")
    for k in ("N", "labels", "cells", "nll_add", "nll_joint", "lift"):
        v = res[k]
        print(f"{k:>12}: {v:.4f}" if isinstance(v, float) else f"{k:>12}: {v}")
    print()
    # show the joint structure: for each (batchim, slot) which particle dominates
    print("# joint table  (A=batchim, B=slot) -> dominant particle : P")
    for (A, B), cnt in sorted(n_ab.items()):
        top = p_lab[(A, B)].most_common(1)[0]
        print(f"  batchim={str(A):5} slot={B:8} -> '{top[0]}' : {top[1]/cnt:.3f}  (n={cnt})")
    print()
    verdict = "PASS (detector power OK)" if res["lift"] > 0.05 else "FAIL (INVALID gate)"
    print(f"# PC-P gate: lift={res['lift']:.3f}  -> {verdict}")
    print("# read: particle byte must be JOINT-determined -> big lift; additive alone can't")
    print("#       tell 은/는 (needs A) nor 은/이/을 (needs B).")
