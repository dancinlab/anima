#!/usr/bin/env python3
# ==========================================================================
# cluster_F_f3.py — F3 schema-skeleton (not answer) cross-domain retrieval
#   $0 numpy probe. DIRECTIONAL (no 303M). Tests a FROZEN falsifier.
#
# H_9200 cluster F, item F3:
#   "schema retrieval, answer retrieval 아님: topic 과 먼 도메인의 relation
#    skeleton 만 가져오기" | G6 | falsifier: retrieved entity words 를 제거해도
#    transfer 유지.
#
# Distinct from floored levers:
#   - H_9118 (hippo retrieve ANSWER into mouth context = MOUTHFLOOR): here we
#     retrieve the relation SKELETON (type-only, entity-abstracted), not the
#     answer D, and we measure transfer to a FAR domain, not in-context bind.
#   - L5 (H_9129) transitive chaining is SAME-domain completion; F3 tests
#     CROSS-domain entity-invariant skeleton transfer.
#
# PREREG frozen bar (decided before run, a_break_the_wall / no tune-to-green):
#   chance        = 1/(n_entities_per_role)
#   skeleton_acc  : predict B held-out role-2 via A's TYPE-ONLY skeleton
#   answer_acc    : predict B role-2 via A's full path WITH entity words
#   shuf_acc      : skeleton with relation TYPES shuffled per chain
#   PASS requires ALL of:
#     (1) skeleton_acc - shuf_acc >= 0.33        (bind-destruction delta)
#     (2) skeleton_acc >= chance + 0.30          (well above chance)
#     (3) skeleton_acc > answer_acc + 0.10       (skeleton, not surface, carries)
#     (4) answer_acc - chance < 0.15             (entity-word removal kills answer)
#   FAIL  = retrieval is answer-surface (rethread H_9118 mouth-context family).
# ==========================================================================
import numpy as np

RNG_SEED = 20260705
N_ENT    = 24
N_ROLES  = 3
N_CHAINS = 60
D        = 1024
REL_N    = 5


def rand_code(rng, n, d):
    X = rng.standard_normal((n, d)).astype(np.float64)
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    return X


def bind(a, b):
    return np.fft.ifft(np.fft.fft(a, axis=-1) * np.fft.fft(b, axis=-1), axis=-1).real


def bundle(items):
    return np.tanh(np.sum(items, axis=0))


def main():
    rng = np.random.default_rng(RNG_SEED)
    chance = 1.0 / N_ENT
    print(f"F3 schema-skeleton cross-domain transfer  (chance={chance:.4f}, D={D})")
    print(f"PREREG bar: skeleton-shuf>=0.33, skeleton>=chance+0.30, "
          f"skeleton>answer+0.10, answer-chance<0.15\n")

    rel_code = rand_code(rng, REL_N, D)
    role_code = rand_code(rng, N_ROLES, D)  # distinct role-slot codes

    skel_acc, ans_acc, shuf_acc = [], [], []

    for ch in range(N_CHAINS):
        skel_types = rng.integers(0, REL_N, size=N_ROLES)
        entA = [rand_code(rng, N_ENT, D) for _ in range(N_ROLES)]
        entB = [rand_code(rng, N_ENT, D) for _ in range(N_ROLES)]
        a_idx = [int(rng.integers(0, N_ENT)) for _ in range(N_ROLES)]
        b_idx = [int(rng.integers(0, N_ENT)) for _ in range(N_ROLES)]
        b_role2_true = b_idx[2]
        b_q01 = b_idx[:2]

        # ARM 1: SCHEMA (TYPE-ONLY) — bind rel_type_k into role_k slot, NO entities
        # apply skeleton to B role-0,1 entities, predict role-2
        comp = bundle([bind(rel_code[skel_types[k]], entB[k][b_q01[k]]) for k in range(2)])
        probe = bind(comp, rel_code[skel_types[2]])
        skel_acc.append(int(np.argmax(entB[2] @ probe)) == b_role2_true)

        # ARM 2: ANSWER — A's literal path WITH entity words (disjoint from B)
        a_path = bundle([bind(rel_code[skel_types[k]], entA[k][a_idx[k]]) for k in range(2)])
        ans_probe = bind(a_path, rel_code[skel_types[2]])
        ans_acc.append(int(np.argmax(entB[2] @ ans_probe)) == b_role2_true)

        # ARM 3: SHUFFLE control — relation TYPES permuted
        shuf = skel_types.copy(); rng.shuffle(shuf)
        comp_s = bundle([bind(rel_code[shuf[k]], entB[k][b_q01[k]]) for k in range(2)])
        shuf_probe = bind(comp_s, rel_code[shuf[2]])
        shuf_acc.append(int(np.argmax(entB[2] @ shuf_probe)) == b_role2_true)

    s, a, sh = float(np.mean(skel_acc)), float(np.mean(ans_acc)), float(np.mean(shuf_acc))
    g1, g2, g3, g4 = s - sh, s - chance, s - a, a - chance
    print(f"skeleton_acc={s:.4f}  answer_acc={a:.4f}  shuf_acc={sh:.4f}  chance={chance:.4f}\n")
    print(f"gate1 skeleton-shuf   = {g1:+.4f} (bar>=+0.33) -> {'PASS' if g1>=0.33 else 'FAIL'}")
    print(f"gate2 skeleton-chance = {g2:+.4f} (bar>=+0.30) -> {'PASS' if g2>=0.30 else 'FAIL'}")
    print(f"gate3 skeleton-answer = {g3:+.4f} (bar> +0.10) -> {'PASS' if g3>0.10 else 'FAIL'}")
    print(f"gate4 answer-chance   = {g4:+.4f} (bar< +0.15) -> {'PASS' if g4<0.15 else 'FAIL'}")
    passed = g1 >= 0.33 and g2 >= 0.30 and g3 > 0.10 and g4 < 0.15
    print(f"\nVERDICT: {'BIND (schema-skeleton transfers, entity-invariant)' if passed else 'WALL/RETHREAD (signal is surface/answer, not skeleton)'}")
    print(f"tier: DIRECTIONAL ($0 numpy VSA toy, no 303M). caveat: a_toy_scale_recheck.")


if __name__ == "__main__":
    main()
