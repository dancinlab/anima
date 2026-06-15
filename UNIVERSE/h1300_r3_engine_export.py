"""
H_1300 R3 — engine-native export for the MITOSIS-GROW SKILL CURRICULUM.

Exports the EXACT H_1300 R2 (CANONICAL catastrophic-forgetting) curriculum as flat
x/y files so the LIVE .hexa engine (CORE/engine_cli.hexa::SkillCellMemory + the
GradSoftmaxFT arm-A learner) reproduces the R2 GREEN through its OWN per-skill
mitosis-grow + closed-form local heads — no numpy in the verdict loop
(a_engine_native_learning). The engine consumes, per seed:

  /tmp/h1300_seed<S>.skill<K>.xtr   — M_PER_SKILL train contexts (D floats / line)
  /tmp/h1300_seed<S>.skill<K>.ytr   — parallel tool-token targets (int / line, 0..C-1)
  /tmp/h1300_seed<S>.skill<K>.xte   — M_TEST_PER_SKILL held-out test contexts
  /tmp/h1300_seed<S>.skill<K>.yte   — parallel held-out targets

ALL knobs FROZEN identical to UNIVERSE/h1300_mitosis_skill_curriculum.py R2 (the
SAME make_curriculum(seed,"r2") RNG path: regions sep 3.0->1.0, anti-aligned shared
rules). The engine sees the SAME contexts+targets the numpy mirror saw — the only
difference is the GROW / FIT / FT / ROUTE arithmetic runs on the .hexa engine, not
numpy. p7: held-out tool-token accuracy + retention. $0 CPU, no GPU, no secrets.

This export is DATA-ONLY — it does NOT run the learner. The engine grows its own
cells and fits its own heads from this raw curriculum (true engine-native learning).
"""
import numpy as np

# ── frozen knobs (VERBATIM from UNIVERSE/h1300_mitosis_skill_curriculum.py) ───
SEEDS            = [1300, 1301, 1302]
N_SKILLS         = 5
D                = 12
C                = 4
M_PER_SKILL      = 64
M_TEST_PER_SKILL = 64
CLUSTER_SIGMA    = 0.35


def make_curriculum_r2(seed):
    """R2 CANONICAL catastrophic-forgetting condition — byte-identical to the
    numpy mirror's make_curriculum(seed, regime='r2'): closer regions (sep 1.0)
    + anti-aligned shared rules (shared base + per-skill sign flips)."""
    rng = np.random.RandomState(seed)
    sep = 1.0
    mus = rng.normal(0.0, 1.0, (N_SKILLS, D)) * sep
    base = rng.normal(0.0, 1.0, (C, D))
    Ws = np.empty((N_SKILLS, C, D))
    for k in range(N_SKILLS):
        flip = rng.choice([-1.0, 1.0], size=(C, 1))
        Ws[k] = base * flip + 0.25 * rng.normal(0.0, 1.0, (C, D))
    skills = []
    for k in range(N_SKILLS):
        def gen(n, kk=k, r=rng):
            x = mus[kk][None, :] + r.normal(0.0, CLUSTER_SIGMA, (n, D))
            y = np.argmax(x @ Ws[kk].T, axis=1)
            return x, y
        xtr, ytr = gen(M_PER_SKILL)
        xte, yte = gen(M_TEST_PER_SKILL)
        skills.append({"xtr": xtr, "ytr": ytr, "xte": xte, "yte": yte})
    return skills


def fmt_vec(v):
    return " ".join(f"{x:.10g}" for x in v)


def main():
    for s in SEEDS:
        skills = make_curriculum_r2(s)
        for k in range(N_SKILLS):
            base = f"/tmp/h1300_seed{s}.skill{k}"
            with open(base + ".xtr", "w") as f:
                f.write("\n".join(fmt_vec(r) for r in skills[k]["xtr"]) + "\n")
            with open(base + ".ytr", "w") as f:
                f.write("\n".join(str(int(y)) for y in skills[k]["ytr"]) + "\n")
            with open(base + ".xte", "w") as f:
                f.write("\n".join(fmt_vec(r) for r in skills[k]["xte"]) + "\n")
            with open(base + ".yte", "w") as f:
                f.write("\n".join(str(int(y)) for y in skills[k]["yte"]) + "\n")
        print(f"exported seed {s}: {N_SKILLS} skills x "
              f"({M_PER_SKILL} train + {M_TEST_PER_SKILL} test), D={D} C={C} "
              f"-> /tmp/h1300_seed{s}.skill*.{{xtr,ytr,xte,yte}}")


if __name__ == "__main__":
    main()
