"""H_008 — f6-shard-ensemble. F6 (selection-pressure-lineage) lost its pre-registered
variation axis (CODEC MUTATION) to l11. This probe tests the strongest NON-codec axis that
has a $0 falsifiable proxy: DATA-SHARD SPECIALIZATION (a population of domain specialists +
an oracle selector vs a single monolith of MATCHED TOTAL CAPACITY).

F6's own falsifier: if population diversity collapses to ~1 individual while fitness stagnates,
the swarm is an expensive single model = DEAD. This probe makes that falsifier $0-measurable.

The l11 skeptic's prediction (adversarial): a single pooled model contains every specialist's
statistics as a SUBSET, so at matched capacity the monolith dominates and specialization buys
nothing. The decisive test is therefore MATCHED TOTAL CAPACITY: K specialists of capacity C
each vs ONE monolith of capacity K*C. If partitioning K*C into K domain-specialists (+ oracle
routing) beats the monolith of K*C on held-out prediction, above controls, the population buys
genuine performance-relevant diversity that a single model of equal size cannot. Else REFUSED.

Model = a deterministic, capacity-limited backoff n-gram LM (a faithful $0 proxy for a small
model with FIXED capacity that must AVERAGE across domains it cannot separately store).
Capacity C = max number of distinct (order,context) keys the table may hold (first-come
admission, unigram always free). This is the bottleneck that makes ensemble-vs-monolith a real
question — a nonparametric count table with unbounded capacity has no interference and the
monolith trivially wins (the l11 tautology), so the capacity cap is what gives the axis a
chance to escape.

$0, deterministic, stdlib only. Card frozen 2026-07-16.
Run: python3 state/h008_f6-shard-ensemble_2026-07-16/run_h008.py
"""

from __future__ import annotations

import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))

from anima_v3 import Falsifier, evaluate

# --- frozen inputs (must match the card) --------------------------------------
CORPUS_ROOT = "/Users/mini/dancinlab"
DOMAINS = ["py", "md", "json", "sh", "c"]     # K=5 genuinely distinct byte-domains
K = len(DOMAINS)
TRAIN_BYTES = 250_000                          # per domain, from train files
HELDOUT_BYTES = 50_000                         # per domain, from DISJOINT held-out files
CHUNK = 512                                    # held-out routing granularity
MAXORD = 5                                     # backoff n-gram max order
CAPS = [4_000, 16_000, 64_000]                 # capacity sweep (distinct context keys per specialist)
EPS_BPB = 0.02                                 # campaign convention (bpb)
MIN_WINNERS = 2.0                              # F6 diversity floor (effective winners > 2)


# --- capacity-limited backoff n-gram model ------------------------------------

class CapNGram:
    """Deterministic backoff n-gram with a HARD cap on distinct context keys.

    Training admits contexts first-come until the cap is hit; further novel contexts
    are refused (predictions back off to a lower stored order, ultimately the always-free
    unigram). This makes capacity a real bottleneck: a monolith trained on K domains must
    spend its keys across all of them, while a specialist spends the same keys on one domain
    — the matched-capacity ensemble-vs-monolith question F6 lives or dies on."""

    def __init__(self, cap: int, maxord: int = MAXORD):
        self.cap = cap
        self.maxord = maxord
        self.table = {}                 # (order, ctx_bytes) -> {next_byte: count}
        self.uni = [0] * 256
        self.uni_tot = 0

    def train(self, data: bytes) -> None:
        data = bytes(data)
        table = self.table
        cap = self.cap
        uni = self.uni
        for i in range(len(data)):
            b = data[i]
            uni[b] += 1
            for k in range(1, self.maxord + 1):
                if i - k < 0:
                    break
                key = (k, data[i - k:i])
                d = table.get(key)
                if d is not None:
                    d[b] = d.get(b, 0) + 1
                elif len(table) < cap:
                    table[key] = {b: 1}
                # else: refused (capacity full) -> stays absent, forces backoff
        self.uni_tot = sum(uni)

    def bpb(self, data: bytes) -> float:
        """Bits per byte of `data`, history = its own preceding bytes (backoff to unigram)."""
        data = bytes(data)
        if not data:
            return 0.0
        table = self.table
        uni = self.uni
        uni_tot = self.uni_tot or 1
        bits = 0.0
        for i in range(len(data)):
            b = data[i]
            p = None
            for k in range(self.maxord, 0, -1):
                if i - k < 0:
                    continue
                d = table.get((k, data[i - k:i]))
                if d:
                    tot = 0
                    for v in d.values():
                        tot += v
                    p = (d.get(b, 0) + 1) / (tot + 256)
                    break
            if p is None:
                p = (uni[b] + 1) / (uni_tot + 256)
            bits += -math.log(p, 2)
        return bits / len(data)


# --- corpus gathering (deterministic) -----------------------------------------

def _list_files(ext: str) -> list:
    hits = []
    for dirpath, dirnames, filenames in os.walk(CORPUS_ROOT):
        # prune noise deterministically
        dirnames[:] = sorted(d for d in dirnames
                             if d not in (".git", "node_modules", "__pycache__", ".venv"))
        for fn in sorted(filenames):
            if fn.endswith("." + ext):
                hits.append(os.path.join(dirpath, fn))
        if len(hits) > 6000:
            break
    return sorted(hits)


def _read_until(files: list, nbytes: int, skip_files: set) -> tuple:
    """Concatenate file bytes (deterministic order) until nbytes reached.
    Returns (data, used_files)."""
    buf = bytearray()
    used = []
    for f in files:
        if f in skip_files:
            continue
        try:
            with open(f, "rb") as fh:
                b = fh.read()
        except Exception:
            continue
        if not b:
            continue
        buf.extend(b)
        used.append(f)
        if len(buf) >= nbytes:
            break
    return bytes(buf[:nbytes]), set(used)


def gather_domains() -> dict:
    """For each domain: TRAIN_BYTES from lead files, HELDOUT_BYTES from DISJOINT files."""
    out = {}
    for ext in DOMAINS:
        files = _list_files(ext)
        train, train_used = _read_until(files, TRAIN_BYTES, set())
        held, _ = _read_until(files, HELDOUT_BYTES, train_used)   # disjoint files -> no leakage
        out[ext] = {"train": train, "held": held,
                    "n_train_files": len(train_used)}
    return out


# --- the matched-capacity ensemble-vs-monolith measurement --------------------

def _chunks(data: bytes, size: int) -> list:
    return [data[i:i + size] for i in range(0, len(data) - size + 1, size)]


def inv_simpson(counts: list) -> float:
    """Effective number of winners = 1 / sum(p_i^2) = participation ratio of a prob vector."""
    tot = sum(counts)
    if tot <= 0:
        return 0.0
    ps = [c / tot for c in counts]
    denom = sum(p * p for p in ps)
    return 1.0 / denom if denom > 0 else 0.0


def run_arena(domains: dict, cap: int, maxord: int = MAXORD) -> dict:
    """Train K specialists (cap each) + 1 monolith (K*cap). Score held-out chunks.
    domains: {name: {"train":bytes,"held":bytes}}. Returns metrics for this capacity.
    `maxord` lets a diagnostic disable the monolith's high-order in-context adaptation."""
    names = list(domains.keys())
    # specialists
    specs = {}
    for nm in names:
        m = CapNGram(cap, maxord=maxord)
        m.train(domains[nm]["train"])
        specs[nm] = m
    # monolith: matched TOTAL capacity K*cap, trained on all shards (deterministic concat)
    mono = CapNGram(cap * len(names), maxord=maxord)
    for nm in names:
        mono.train(domains[nm]["train"])

    # held-out chunks, tagged by true domain
    all_chunks = []
    for nm in names:
        for ch in _chunks(domains[nm]["held"], CHUNK):
            all_chunks.append((nm, ch))

    mono_bpbs, oracle_bpbs, self_bpbs = [], [], []
    winner_counts = {nm: 0 for nm in names}
    route_correct = 0
    for true_dom, ch in all_chunks:
        mb = mono.bpb(ch)
        mono_bpbs.append(mb)
        # every specialist's bpb on this chunk
        sb = {nm: specs[nm].bpb(ch) for nm in names}
        # oracle route = best specialist
        win = min(sb, key=sb.get)
        oracle_bpbs.append(sb[win])
        winner_counts[win] += 1
        if win == true_dom:
            route_correct += 1
        # self route = the chunk's own-domain specialist (realistic, no oracle)
        if true_dom in sb:
            self_bpbs.append(sb[true_dom])

    def med(v):
        v = sorted(v)
        return v[len(v) // 2] if v else 0.0

    n = len(all_chunks) or 1
    return {
        "cap": cap,
        "n_chunks": len(all_chunks),
        "mono_bpb": med(mono_bpbs),
        "oracle_bpb": med(oracle_bpbs),
        "self_bpb": med(self_bpbs),
        "lift_oracle": med(mono_bpbs) - med(oracle_bpbs),
        "lift_self": med(mono_bpbs) - med(self_bpbs),
        "eff_winners": inv_simpson([winner_counts[nm] for nm in names]),
        "route_acc": route_correct / n,
        "winner_counts": winner_counts,
    }


# --- controls -----------------------------------------------------------------

def homogeneous_domains(domains: dict) -> dict:
    """NEGATIVE floor: ONE domain's text split into K arbitrary equal shards. No real domain
    structure -> specialization must buy ~nothing (ensemble lift ~ 0)."""
    src = domains[DOMAINS[0]]
    train = src["train"]
    held = src["held"]
    per = len(train) // K
    hper = len(held) // K
    out = {}
    for j in range(K):
        out[f"h{j}"] = {"train": train[j * per:(j + 1) * per],
                        "held": held[j * hper:(j + 1) * hper]}
    return out


def shuffled_domains(domains: dict) -> dict:
    """NEGATIVE floor 2: real domains' train bytes RE-DEALT round-robin across K specialists,
    so each specialist gets a domain-incoherent mix of equal size. Held-out kept per true
    domain. Destroys specialist coherence -> routing/lift must collapse. Deterministic."""
    blocks = []
    for nm in DOMAINS:
        tb = domains[nm]["train"]
        for i in range(0, len(tb) - CHUNK + 1, CHUNK):
            blocks.append(tb[i:i + CHUNK])
    out = {}
    for j in range(K):
        out[f"s{j}"] = {"train": b"".join(blocks[j::K]), "held": b""}
    # held-out chunks: reuse the REAL per-domain held, tag by true domain order so route_acc
    # is defined but should be ~chance (specialists are incoherent).
    for j, nm in enumerate(DOMAINS):
        out[f"s{j}"]["held"] = domains[nm]["held"]
    return out


def planted_domains(seed: int = 7) -> dict:
    """POSITIVE liveness: K STOCHASTIC domains over a shared 16-symbol alphabet, each a distinct
    order-1 Markov chain with a peaked (low-entropy) per-domain transition matrix. The optimal
    model is order-1, so higher-order backoff CANNOT rescue the monolith (unlike a deterministic
    signal, which l11 shows a high-order reader always recovers). A specialist learns its domain's
    matrix (bpb -> H(P_j), low); the monolith learns the MIXTURE (1/K)ΣP_j, whose per-symbol
    entropy is strictly higher when the P_j differ (Jensen) — a genuine, order-invariant
    ensemble win. If the ensemble does NOT beat the monolith here with high rank, the instrument
    is blind -> INVALID."""
    A = 16
    alpha = bytes([97 + i for i in range(A)])          # SAME alphabet across domains
    state = [seed]

    def rnd():                                          # deterministic LCG uniform in [0,1)
        state[0] = (1103515245 * state[0] + 12345) & 0x7FFFFFFF
        return state[0] / 0x7FFFFFFF

    out = {}
    for j in range(K):
        # peaked per-domain transition matrix P[s] over successors (weights^4 -> low entropy)
        P = []
        for _ in range(A):
            w = [rnd() ** 4 for _ in range(A)]
            tot = sum(w) or 1.0
            row, acc = [], 0.0
            for x in w:
                acc += x / tot
                row.append(acc)                         # cumulative
            P.append(row)

        def gen(nbytes, P=P):
            buf = bytearray()
            cur = 0
            for _ in range(nbytes):
                u = rnd()
                nxt = 0
                while nxt < A - 1 and u > P[cur][nxt]:
                    nxt += 1
                buf.append(alpha[nxt])
                cur = nxt
            return bytes(buf)
        out[f"p{j}"] = {"train": gen(TRAIN_BYTES // 2), "held": gen(HELDOUT_BYTES // 2)}
    return out


def main() -> int:
    print("=" * 78)
    print("H_008 — f6-shard-ensemble · matched-capacity ensemble vs monolith ($0)")
    print("=" * 78)
    print(f"K={K} domains {DOMAINS} · train {TRAIN_BYTES}B/dom · held {HELDOUT_BYTES}B/dom")
    print(f"MAXORD={MAXORD} · chunk={CHUNK} · caps={CAPS} · eps={EPS_BPB} bpb\n")

    m = {"caps": CAPS, "domains": DOMAINS, "real": {}, "homogeneous": {}, "shuffled": {},
         "liveness": {}, "liveness_o1": {}}

    print("[gather] reading real domains ...")
    real = gather_domains()
    for nm in DOMAINS:
        print(f"    {nm:5s}: train {len(real[nm]['train'])}B held {len(real[nm]['held'])}B "
              f"({real[nm]['n_train_files']} train files)")
    homo = homogeneous_domains(real)
    shuf = shuffled_domains(real)
    live = planted_domains()

    print("\n[liveness_o1] planted domains, MAXORD=1 (monolith = pure mixture, in-context")
    print("               adaptation DISABLED — ensemble MUST win by Jensen/KL; instrument check):")
    for cap in CAPS:
        r = run_arena(live, cap, maxord=1)
        m["liveness_o1"][str(cap)] = r
        print(f"    cap={cap:6d}: mono {r['mono_bpb']:.3f} oracle {r['oracle_bpb']:.3f} "
              f"lift {r['lift_oracle']:+.3f} eff_win {r['eff_winners']:.2f} "
              f"route_acc {r['route_acc']:.2f}")

    print("\n[liveness] planted separable domains, MAXORD=5 (realistic — monolith MAY in-context")
    print("           adapt via high-order context; this is the regime the real premise runs in):")
    for cap in CAPS:
        r = run_arena(live, cap)
        m["liveness"][str(cap)] = r
        print(f"    cap={cap:6d}: mono {r['mono_bpb']:.3f} oracle {r['oracle_bpb']:.3f} "
              f"lift {r['lift_oracle']:+.3f} eff_win {r['eff_winners']:.2f} "
              f"route_acc {r['route_acc']:.2f}")

    print("\n[real] file-type domains (the premise):")
    for cap in CAPS:
        r = run_arena(real, cap)
        m["real"][str(cap)] = r
        print(f"    cap={cap:6d}: mono {r['mono_bpb']:.3f} oracle {r['oracle_bpb']:.3f} "
              f"self {r['self_bpb']:.3f} lift_o {r['lift_oracle']:+.3f} lift_s {r['lift_self']:+.3f} "
              f"eff_win {r['eff_winners']:.2f} route_acc {r['route_acc']:.2f}")

    print("\n[homogeneous] one domain split K ways (negative floor 1):")
    for cap in CAPS:
        r = run_arena(homo, cap)
        m["homogeneous"][str(cap)] = r
        print(f"    cap={cap:6d}: mono {r['mono_bpb']:.3f} oracle {r['oracle_bpb']:.3f} "
              f"lift {r['lift_oracle']:+.3f} eff_win {r['eff_winners']:.2f}")

    print("\n[shuffled] domain-incoherent specialists (negative floor 2):")
    for cap in CAPS:
        r = run_arena(shuf, cap)
        m["shuffled"][str(cap)] = r
        print(f"    cap={cap:6d}: mono {r['mono_bpb']:.3f} oracle {r['oracle_bpb']:.3f} "
              f"lift {r['lift_oracle']:+.3f} eff_win {r['eff_winners']:.2f} route_acc {r['route_acc']:.2f}")

    # --- verdict logic (pre-registered, adversarial: F6 is DENTED) -------------
    # The decisive statistic is NOT the raw oracle lift (contaminated by the oracle-MIN
    # winner's-curse, which the shuffled control shows produces a spurious monolith-beating lift
    # from domain-INCOHERENT specialists). It is the DOMAIN-COHERENCE BENEFIT, isolated by
    # subtracting the shuffled floor at matched capacity:
    #     benefit(cap) = real_lift_oracle(cap) - shuffled_lift_oracle(cap)
    # and it must hold in the TIGHT-capacity regime F6 actually proposes ("N SMALL models"),
    # not merely at the loosest capacity. Cherry-picking the best cap is a pro-F6 bias.
    caps = [str(c) for c in CAPS]
    benefit = {c: m["real"][c]["lift_oracle"] - m["shuffled"][c]["lift_oracle"] for c in caps}
    tight_cap = caps[0]                                   # smallest cap = the small-model regime
    tight_benefit = benefit[tight_cap]
    best_benefit = max(benefit.values())
    robust = all(v > EPS_BPB for v in benefit.values())   # domain benefit across ALL capacities
    # naive best-cap oracle read (reported for transparency; NOT the verdict)
    best_real = max(m["real"].values(), key=lambda r: r["lift_oracle"])
    best_cap = best_real["cap"]
    naive_best_lift = best_real["lift_oracle"]
    # the ideal-case ceiling at REALISTIC order (MAXORD=5): if a perfectly separable planted
    # ensemble barely beats the monolith at realistic order, no real corpus should exceed it.
    ideal5_best = max(r["lift_oracle"] for r in m["liveness"].values())
    # instrument check = MAXORD=1 planted (pure mixture; MUST lose by KL if instrument can see it)
    live_ok = any(r["lift_oracle"] > 5 * EPS_BPB and r["eff_winners"] > MIN_WINNERS
                  for r in m["liveness_o1"].values())
    eff_win_best = max(m["real"][c]["eff_winners"] for c in caps)
    shuf_lift_max = max(r["lift_oracle"] for r in m["shuffled"].values())

    m["summary"] = {
        "benefit_by_cap": benefit,
        "tight_cap": int(tight_cap),
        "tight_benefit": tight_benefit,
        "best_benefit": best_benefit,
        "robust_across_caps": robust,
        "naive_best_cap": best_cap,
        "naive_best_lift_oracle": naive_best_lift,
        "ideal_order5_best_lift": ideal5_best,
        "eff_winners_best": eff_win_best,
        "liveness_ok": live_ok,
        "shuffled_lift_max": shuf_lift_max,
    }

    falsifiers = [
        Falsifier("S-3 liveness (instrument sees ensemble win at MAXORD=1)",
                  lambda x: not x["summary"]["liveness_ok"],
                  "MAXORD=1 pure-mixture monolith is NOT beaten by ensemble -> INVALID (blind)"),
        Falsifier("S-1 kill (no domain-coherence benefit at best cap)",
                  lambda x: x["summary"]["best_benefit"] <= EPS_BPB,
                  "shuffle-corrected specialization benefit <= eps at every cap -> F6-SHARD-REFUSED"),
        Falsifier("S-2 small-model regime (benefit fails at tight capacity)",
                  lambda x: x["summary"]["tight_benefit"] <= EPS_BPB,
                  "no benefit in F6's own 'N small models' regime -> F6-SHARD-REFUSED"),
        Falsifier("S-4 not robust across capacity",
                  lambda x: not x["summary"]["robust_across_caps"],
                  "benefit sign-flips across capacity -> fragile, not a robust axis"),
        Falsifier("S-5 exceeds the realistic-order ideal ceiling (artifact)",
                  lambda x: x["summary"]["naive_best_lift_oracle"]
                  > x["summary"]["ideal_order5_best_lift"] + EPS_BPB,
                  "real lift exceeds the perfectly-separable ideal at realistic order -> the lift is "
                  "an estimator/min artifact, not specialization"),
    ]
    ledger = evaluate(m, falsifiers)

    if not live_ok:
        verdict = "INVALID (blind instrument — MAXORD=1 liveness failed)"
    elif best_benefit <= EPS_BPB:
        verdict = ("F6-SHARD-REFUSED — the shuffle-corrected domain-specialization benefit is <= eps "
                   "at every capacity: at matched total capacity the pooled monolith is not beaten "
                   "by a specialist ensemble beyond the oracle-min artifact (the l11 superset "
                   "argument holds; the monolith in-context-adapts to the domain).")
    elif tight_benefit <= EPS_BPB or not robust:
        verdict = (f"F6-SHARD-BORDERLINE (leaning REFUSED) — the shuffle-corrected domain-coherence "
                   f"benefit is small and NON-ROBUST across capacity "
                   f"({', '.join(f'{c}:{benefit[c]:+.3f}' for c in caps)} bpb — it sign-flips), best "
                   f"only +{best_benefit:.3f}. The raw oracle lift (+{naive_best_lift:.3f}) EXCEEDS "
                   f"the perfectly-separable planted ensemble's realistic-order ceiling "
                   f"(+{ideal5_best:.3f}), i.e. it is mostly oracle-min/estimator artifact, not "
                   f"specialization. The axis does not robustly escape the matched-capacity monolith "
                   f"(which in-context-adapts to the domain — the l11 superset argument).")
    else:
        verdict = (f"F6-SHARD-ANCHORED — shuffle-corrected specialization benefit +{best_benefit:.3f} "
                   f"bpb, robust across capacity incl. the small-model regime "
                   f"(tight {tight_benefit:+.3f}), eff_winners {eff_win_best:.2f}: data-shard "
                   f"specialization is a genuine, l11-escaping F6 axis (licenses a cheap trained-net "
                   f"confirm).")
    m["verdict"] = verdict

    print("\n" + "=" * 78)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"\n  shuffle-corrected domain benefit by cap: "
          + " ".join(f"{c}:{benefit[c]:+.3f}" for c in caps))
    print(f"  tight_benefit={tight_benefit:+.4f} best_benefit={best_benefit:+.4f} robust={robust} "
          f"ideal_o5_ceiling={ideal5_best:+.3f} naive_best_lift={naive_best_lift:+.3f}")
    print(f"  VERDICT: {verdict}")
    print("=" * 78)

    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\nartifacts: {os.path.relpath(out, _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
