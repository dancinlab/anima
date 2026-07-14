"""H_9354 $0 screen — tick-dependence of the one live per-tick substrate DV (ten_phasic)
on the existing 303M engine-native decision trace. Reads a trace produced by
cli/chat.py's ANIMA_DECISION_TRACE. No forward re-impl (a_experiment_engine_native):
consumes only what the daemon already logged per tick. See card H_9354.
H-a full-permutation null · H-b circular-shift null · H-c I(stage;emit)."""
import json, math, random, sys, statistics as S

TRACE = sys.argv[1] if len(sys.argv) > 1 else \
    "state/h1058_agency_daemon/results/trace_303m.jsonl"


def acf1(x):
    n = len(x); mu = sum(x) / n
    num = sum((x[i] - mu) * (x[i + 1] - mu) for i in range(n - 1))
    den = sum((v - mu) ** 2 for v in x)
    return num / den if den > 0 else float("nan")


def pct(sl, q):
    i = q * (len(sl) - 1); lo = int(i); hi = min(lo + 1, len(sl) - 1)
    return sl[lo] + (sl[hi] - sl[lo]) * (i - lo)


def mi(a, b):
    from collections import Counter
    n = len(a); pa = Counter(a); pb = Counter(b); pab = Counter(zip(a, b)); I = 0.0
    for (x, y), c in pab.items():
        pxy = c / n
        if pxy > 0:
            I += pxy * math.log(pxy / ((pa[x] / n) * (pb[y] / n)))
    return I


def run(trace):
    D = [json.loads(l) for l in open(trace) if l.strip() and not json.loads(l).get("_meta")]
    N = len(D)
    tp = [float(r["ten_phasic"]) for r in D]
    st = [int(r["stage"]) for r in D]
    em = [1 if r.get("emit") else 0 for r in D]
    rng = random.Random(7); K = 2000
    rho = acf1(tp)
    perm = sorted(acf1([*__import__("random").sample(tp, len(tp))]) for _ in range(0))  # placeholder
    perm = []
    for _ in range(K):
        x = tp[:]; rng.shuffle(x); perm.append(acf1(x))
    perm.sort()
    shift = []
    for _ in range(K):
        k = rng.randint(10, N - 10); shift.append(acf1(tp[k:] + tp[:k]))
    shift.sort()
    Is = mi(st, em); ctrl = []
    for _ in range(K):
        e = em[:]; rng.shuffle(e); ctrl.append(mi(st, e))
    ctrl.sort()
    from collections import Counter
    print("N=%d stage=%s emit=%d/%d ten_phasic[min=%.4f max=%.4f var=%.2e]" %
          (N, dict(Counter(st)), sum(em), N, min(tp), max(tp), S.pvariance(tp)))
    print("H-a rho1=%.4f perm[2.5%%=%.4f 97.5%%=%.4f]" % (rho, pct(perm, .025), pct(perm, .975)))
    print("H-b rho1=%.4f shift[2.5%%=%.4f 97.5%%=%.4f] excess=%+.4f" %
          (rho, pct(shift, .025), pct(shift, .975), rho - pct(shift, .975)))
    print("H-c I(stage;emit)=%.4f nats (bar .05 · shuffle 97.5%%=%.4f)" % (Is, pct(ctrl, .975)))


if __name__ == "__main__":
    run(TRACE)
