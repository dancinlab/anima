"""
H_1288 R2 — engine-native export for the GROW-UNDER-PRESSURE immune memory.

Exports the EXACT H_1288 R1 EVICTION-BOUND regime (the zero-sum LRU rung) as flat
key/value files so the LIVE .hexa engine (CORE/engine_cli.hexa::ImmuneMemoryGrow) can
reproduce the R1 GREEN through its OWN clonal split + L2 affinity — no numpy in the
verdict loop (a_engine_native_learning). The engine consumes:

  /tmp/h1288_seed<S>.instore.keys   — N_FACTS taught keys, IN TAUGHT ORDER (the LRU /
                                       importance axis: cell 0 = first taught = oldest).
  /tmp/h1288_seed<S>.instore.vals   — the parallel bound cities (taught order).
  /tmp/h1288_seed<S>.query.keys     — N_FACTS held-out NOISY query keys (R1's exact
                                       cue perturbation baked in, taught order).
  /tmp/h1288_seed<S>.query.truth    — the ground-truth cities for the queries.
  /tmp/h1288_seed<S>.imp            — "1"/"0" per fact: first tercile = IMPORTANT
                                       (taught-first = most LRU-vulnerable; R1 sub-metric).
  /tmp/h1288_seed<S>.out.keys       — N_OUT untaught NOISY keys (abstain probe).

ALL knobs FROZEN identical to UNIVERSE/h1288_eviction_policy.py (R1). The embed_key /
FNV-1a / noise convention is byte-identical to R1, so the engine sees the SAME keys
R1's mirror saw — the only difference is the bind/recall arithmetic runs on the .hexa
engine, not numpy.  p7: exact-match recall + abstain.  $0 CPU.
"""
import numpy as np

# ── frozen knobs (VERBATIM from UNIVERSE/h1288_eviction_policy.py R1) ─────────
SEEDS          = [900, 901, 902]
N_FACTS        = 60
N_OUT          = 60
KEY_DIM        = 64
NGRAM          = 3
STRESS_KEY_NOISE   = 0.16
IMPORTANT_FRAC     = 1.0 / 3.0
DICT_PATH      = "/usr/share/dict/words"


def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    rng = np.random.default_rng(seed)
    allw = load_words()
    cap = [w for w in allw if 4 <= len(w) <= 8]
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    subj_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    cities    = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    in_subj, out_subj = subj_pool[:N_FACTS], subj_pool[N_FACTS:]
    facts = [(in_subj[i], cities[i]) for i in range(N_FACTS)]
    out_truth = [(out_subj[i], cities[N_FACTS + i]) for i in range(N_OUT)]
    return facts, out_truth


def _fnv1a(bs):
    h = 0x811c9dc5
    for b in bs:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def embed_key(text, dim=KEY_DIM, n=NGRAM):
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a(b[i:i + n]) % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


def noisy(key, noise, rng):
    """R1's recall() cue perturbation: dim-invariant target-L2 noise."""
    sigma = noise / np.sqrt(max(1, key.shape[0]))
    return key + rng.normal(0.0, sigma, size=key.shape)


def fmt_vec(v):
    return " ".join(f"{x:.10g}" for x in v)


def main():
    for s in SEEDS:
        facts, out_truth = build_facts(s)
        n_imp = max(1, int(round(N_FACTS * IMPORTANT_FRAC)))

        # in-store taught keys + values (TAUGHT ORDER = LRU/importance axis)
        in_keys = [embed_key(f"{subj} lives in ") for subj, _ in facts]
        in_vals = [city for _, city in facts]
        imp     = ["1" if i < n_imp else "0" for i in range(N_FACTS)]

        # held-out NOISY query keys — R1 uses ONE shared eval-noise stream for the
        # total-recall measure (seed*104729+3), applied in taught order.
        rng_t = np.random.default_rng(s * 104729 + 3)
        q_keys = [noisy(embed_key(f"{subj} lives in "), STRESS_KEY_NOISE, rng_t)
                  for subj, _ in facts]
        q_truth = [city for _, city in facts]

        # out-of-store NOISY keys (abstain probe) — R1 fab stream seed*104729+99.
        rng_f = np.random.default_rng(s * 104729 + 99)
        out_keys = [noisy(embed_key(f"{subj} lives in "), STRESS_KEY_NOISE, rng_f)
                    for subj, _ in out_truth]

        base = f"/tmp/h1288_seed{s}"
        with open(base + ".instore.keys", "w") as f:
            f.write("\n".join(fmt_vec(k) for k in in_keys) + "\n")
        with open(base + ".instore.vals", "w") as f:
            f.write("\n".join(in_vals) + "\n")
        with open(base + ".query.keys", "w") as f:
            f.write("\n".join(fmt_vec(k) for k in q_keys) + "\n")
        with open(base + ".query.truth", "w") as f:
            f.write("\n".join(q_truth) + "\n")
        with open(base + ".imp", "w") as f:
            f.write("\n".join(imp) + "\n")
        with open(base + ".out.keys", "w") as f:
            f.write("\n".join(fmt_vec(k) for k in out_keys) + "\n")
        print(f"exported seed {s}: {N_FACTS} facts ({n_imp} important), "
              f"{N_FACTS} noisy queries, {N_OUT} out-keys -> {base}.*")


if __name__ == "__main__":
    main()
