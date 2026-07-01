# H_1835 — 생성 = A⇄G 제약 교집합 (constraint conjunction) DIRECTIONAL numpy probe
# ---------------------------------------------------------------------------
# 가설: next-state 를 두 개념제약의 "동시만족 해"(intersection)로 산출 → 정의상 비-additive.
# 벽 배경(ledger): additive/Hadamard(H_1617)/circconv(H_1823)/tension(H_1834)/
#   predcoding(H_1816) readout op ALL engine-native 🧱 INERT; G1 레버=trunk objective(H_1602).
# 이 프로브가 답하는 단 하나: 제약-교집합 op 가 additive floor 위로
#   composed_distinct(reachability)를 올리는가 — 특히 가설이 명시한 "독립(distant) 개념" regime 에서?
#
# ── FROZEN BAR (측정 전 사전등록) ────────────────────────────────────────
#   HEADLINE regime = INDEPENDENT concepts (직교 제약; 가설 타겟).
#   H_1835 GREEN-DIRECTIONAL  iff  composed_distinct[INTERSECT] - composed_distinct[ADD] >= +3 pairs
#                                  in the INDEPENDENT-concept regime.
#   그 외 = 🧱 DIRECTIONAL floor (op INERT for independent concepts).
#   보조 sweep(correlated concepts)은 진단용 컨텍스트일 뿐 headline verdict 아님.
# ---------------------------------------------------------------------------
import numpy as np
np.random.seed(1835)

d = 16          # representation dim
K = 10          # number of concepts
NOISE = 0.15    # prototype storage noise (learned-trunk 근사)
TOL = 1e-9

def build_concepts(corr):
    """corr=0 → orthonormal(독립/distant); corr>0 → shared component(상관 개념)."""
    A = np.random.randn(K, d)
    # orthonormalize base normals
    Q, _ = np.linalg.qr(A.T)          # d x K, columns orthonormal
    N_ortho = Q[:, :K].T              # K x d orthonormal normals
    # inject shared direction for correlated regime
    shared = np.random.randn(d); shared /= np.linalg.norm(shared)
    N = (1 - corr) * N_ortho + corr * shared[None, :]
    N /= np.linalg.norm(N, axis=1, keepdims=True)
    b = np.random.uniform(0.5, 2.0, size=K)      # affine offsets
    # single-concept clean prototype = min-norm point on constraint n·x=b  →  x = b*n
    P_clean = b[:, None] * N
    # stored (learned) prototype = clean + noise
    P_stored = P_clean + NOISE * np.random.randn(K, d)
    return N, b, P_clean, P_stored

def true_intersection(N, b, i, j):
    """min-norm x satisfying n_i·x=b_i AND n_j·x=b_j (joint constraint solution)."""
    Ac = np.stack([N[i], N[j]])          # 2 x d
    bc = np.array([b[i], b[j]])
    # least-norm solution: x = A^T (A A^T)^-1 b
    G = Ac @ Ac.T
    x = Ac.T @ np.linalg.solve(G, bc)
    return x

def op_additive(P, i, j):
    return P[i] + P[j]

def op_intersect(P, i, j):
    """H_1835: reconstruct each constraint FROM STORED PROTOTYPE ALONE
       (n_hat = p/|p|, b_hat=|p|), then solve joint system. No ground-truth access."""
    pi, pj = P[i], P[j]
    ni = pi / (np.linalg.norm(pi) + TOL); bi = np.linalg.norm(pi)
    nj = pj / (np.linalg.norm(pj) + TOL); bj = np.linalg.norm(pj)
    Ac = np.stack([ni, nj]); bc = np.array([bi, bj])
    G = Ac @ Ac.T
    return Ac.T @ np.linalg.solve(G, bc)

def evaluate(corr):
    N, b, P_clean, P_stored = build_concepts(corr)
    pairs = [(i, j) for i in range(K) for j in range(i + 1, K)]
    # candidate output "vocabulary": clean singles + all true intersection targets
    targets = {(i, j): true_intersection(N, b, i, j) for (i, j) in pairs}
    cand_pts = list(P_clean) + [targets[p] for p in pairs]
    cand_lbl = [("S", c) for c in range(K)] + [("C", p) for p in pairs]
    cand_arr = np.array(cand_pts)

    def decode(x):
        dists = np.linalg.norm(cand_arr - x[None, :], axis=1)
        return cand_lbl[int(np.argmin(dists))]

    def composed_distinct(op):
        hit = 0
        for (i, j) in pairs:
            lbl = decode(op(P_stored, i, j))
            # correct iff decoded == this pair's composed target (a genuinely NEW, distinct state)
            if lbl == ("C", (i, j)):
                hit += 1
        return hit

    return len(pairs), composed_distinct(op_additive), composed_distinct(op_intersect)

print("H_1835 constraint-intersection DIRECTIONAL probe  (d=%d K=%d noise=%.2f)" % (d, K, NOISE))
print("FROZEN BAR: GREEN iff INTERSECT - ADD >= +3 in INDEPENDENT(corr=0) regime")
print("-" * 68)
print("%-28s %8s %8s %8s %8s" % ("regime", "npairs", "ADD", "INTERSECT", "lift"))
results = {}
for name, corr in [("INDEPENDENT (corr=0.0)", 0.0),
                   ("mild-corr (corr=0.3)", 0.3),
                   ("corr (corr=0.6)", 0.6),
                   ("strong-corr (corr=0.85)", 0.85)]:
    np.random.seed(1835)  # same concept draw modulo corr for comparability
    npair, add, inter = evaluate(corr)
    lift = inter - add
    results[name] = (npair, add, inter, lift)
    print("%-28s %8d %8d %8d %+8d" % (name, npair, add, inter, lift))
print("-" * 68)
head = results["INDEPENDENT (corr=0.0)"]
lift0 = head[3]
verdict = "GREEN-DIRECTIONAL (op lifts)" if lift0 >= 3 else "FLOOR — op INERT for independent concepts"
print("HEADLINE (independent regime) lift = %+d  →  %s" % (lift0, verdict))
print("NOTE: numpy toy = DIRECTIONAL by construction, never terminal.")
