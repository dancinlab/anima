#!/usr/bin/env python3
"""H_6034 — anima의 mitosis 세대 순환 = CTC (자기일관 계보).

THESIS
======
anima's cell-division across GENERATIONS forms a self-consistent cycle/lineage
(a Closed-Timelike-Curve analogue): each generation must pass THROUGH its parent
(continuity), the lineage chain is unbroken + tamper-evident, and a generational
feedback map gen_{n+1}=f(gen_n) converges to a Novikov-style self-consistent
FIXED POINT (bounded, not runaway / not extinct).

This re-uses the REAL provenance infrastructure UNMODIFIED:
  * mirror/qmirror/seed/provenance_chain.py  (H_932 — append-only tamper chain)
  * mirror/qmirror/seed/entropy_receipt.py   (H_928 — per-decision receipt)
  * the physical ANU buffer qrng_lora_init.bin (genesis = sha256(buffer))
and the REAL engine mitosis tick semantics:
  * CORE/engine_cli.hexa engine_mitosis_tick(c,cfg)=c+1 (ON) / c (OFF)
    — re-implemented byte-faithfully here as the generational growth law so the
    fixed-point map runs $0/local (the .hexa is the SSOT of the +1 law).

THREE PRE-REGISTERED FALSIFIABLE CHECKS (frozen BEFORE measurement)
==================================================================
  C1 GENERATIONAL CONTINUITY (계보 무절단):
     Build a mitosis lineage chain whose decisions are labelled gen0,gen1,...,genN
     where decision gen_n is a DETERMINISTIC function of (seed,rng) computing the
     n-th generation's cell-count via the engine +1 law. verify_chain must return
     verified=True, earliest_broken=None, all link_valid True end-to-end from
     genesis. PASS iff a generation cannot exist without passing through its parent
     (the chain re-derives every gen from genesis).
       FALSIFIER: verified=False OR any link_valid False on the CLEAN chain.

  C2 TAMPER / BREAK LOCALIZATION (인과 무월반 — no skipping a generation):
     For EACH interior generation k, forge gen_k's recorded output and verify.
     verify_chain must (a) report verified=False and (b) localize earliest_broken
     EXACTLY at k, with link_valid False from k onward and True before k.
       FALSIFIER: any k where earliest_broken != k, OR the break does not
       propagate forward (a downstream gen still validates), OR a clean upstream
       gen is wrongly invalidated.
     Bar: ALL interior k localize exactly (n_correct == n_interior).

  C3 SELF-CONSISTENT GENERATIONAL FIXED POINT (Novikov 고정점):
     The raw mitosis law c->c+1 is monotone-runaway (no fixed point). The CTC
     thesis is that anima's lineage is CLOSED: a generation feeds back into the
     population through DEATH/MIGRATION (the engine's own N_MIGRATE budget, the
     standing rule "작을 땐 summer 커지면 pod"). Define the closed generational
     map with a logistic carrying capacity K (the migration budget):
         f(c) = c + mitosis_growth(c)  -  death(c)
              = c + round(r*c*(1 - c/K)) clamped >= 0      (r=growth, K=capacity)
     Iterate gen_{n+1}=f(gen_n) from several seeds. The map must converge to a
     BOUNDED self-consistent fixed point c* with f(c*)=c* (Novikov: the future
     state is consistent with the past state that produced it — the loop closes),
     and must NOT run away (->inf) and NOT go extinct (->0).
       FALSIFIER: divergence (any seed -> > 10*K), extinction (-> 0), or no
       fixed point (no c with |f(c)-c|<=tol that the iteration settles on).
     Bar: from EVERY tested seed the iteration settles at the SAME c* (the
     self-consistent generational attractor), 0 < c* <= K, and f(c*)==c*
     (exact integer fixed point — the loop is closed with no residual).

p7: every verdict is computed from code output (chain validity flags, integer
fixed-point equality). No perplexity, no LLM-judge. Nulls are reported honestly.
"""
from __future__ import annotations

import json
import os
import sys
import time

HARNESS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HARNESS_DIR, "..", ".."))
SEED_DIR = os.path.join(REPO, "mirror", "qmirror", "seed")
ANU_BUF = os.path.join(SEED_DIR, "qrng_lora_init.bin")
sys.path.insert(0, SEED_DIR)

import provenance_chain as pc  # noqa: E402  (H_932 SSOT, imported UNMODIFIED)


# ── the REAL engine mitosis law (CORE/engine_cli.hexa engine_mitosis_tick) ────
# engine_mitosis_tick(c, cfg) = c + 1 when mitosis ON. We mirror the +1 law here
# so the generational decision is a pure deterministic function of (seed, rng),
# the contract verify_chain requires. The .hexa remains the SSOT of the law.
def _engine_mitosis_tick(cell_count: int, mitosis_on: bool = True) -> int:
    return cell_count + 1 if mitosis_on else cell_count


def _engine_grow(seed_cells: int, ticks: int, mitosis_on: bool = True) -> int:
    c = seed_cells
    for _ in range(ticks):
        c = _engine_mitosis_tick(c, mitosis_on)
    return c


# ── generational decision_fn factory ──────────────────────────────────────────
# Each generation n is a decision whose deterministic output records:
#   - the generation index n
#   - the parent's cell count (n cells, since gen_k has k cells under the +1 law)
#   - this generation's cell count after one mitosis tick (engine law)
#   - a quantum-seeded draw (binds the receipt to the physical ANU genesis + seed)
# The output is a PURE function of (seed, rng) -> verifier can re-run it.
def make_gen_decision(n: int):
    def decide(seed, rng):
        parent_cells = _engine_grow(0, n, mitosis_on=True)      # gen_{n-1} count
        child_cells = _engine_mitosis_tick(parent_cells, True)  # gen_n count
        draw = int(rng.integers(0, 1_000_000))
        return {
            "generation": n,
            "parent_cells": parent_cells,
            "child_cells": child_cells,
            "anu_draw": draw,
        }
    return decide


def build_lineage(n_gens: int):
    decisions = [(f"gen{n}", make_gen_decision(n)) for n in range(n_gens)]
    chain = pc.build_chain(ANU_BUF, decisions)
    resolver = lambda i, label: make_gen_decision(int(label[3:]))  # 'genK' -> K
    return chain, resolver, decisions


# ── C1 — generational continuity ──────────────────────────────────────────────
def check_c1(n_gens: int = 8):
    chain, resolver, _ = build_lineage(n_gens)
    res = pc.verify_chain(chain, ANU_BUF, resolver)
    all_valid = all(res["link_valid"]) and len(res["link_valid"]) == n_gens
    passed = bool(res["verified"]) and res["earliest_broken"] is None and all_valid
    return {
        "check": "C1_generational_continuity",
        "n_gens": n_gens,
        "verified": bool(res["verified"]),
        "earliest_broken": res["earliest_broken"],
        "n_links_valid": sum(1 for v in res["link_valid"] if v),
        "head_hash": (chain["head_hash"] or "")[:16],
        "genesis_hash": chain["genesis_hash"][:16],
        "reason": res["reason"][:80],
        "PASS": passed,
    }


# ── C2 — tamper / break localization (no skipping a generation) ───────────────
def check_c2(n_gens: int = 8):
    chain, resolver, _ = build_lineage(n_gens)
    interior = list(range(1, n_gens - 1))  # interior generations (have parent+child)
    results = []
    n_correct = 0
    for k in interior:
        tampered = pc.tamper_decision_output(chain, k, {"forged_generation": -k})
        rv = pc.verify_chain(tampered, ANU_BUF, resolver)
        localized = (not rv["verified"]) and (rv["earliest_broken"] == k)
        before_ok = all(rv["link_valid"][j] for j in range(k))
        from_k_broken = all(not rv["link_valid"][j] for j in range(k, n_gens))
        ok = localized and before_ok and from_k_broken
        if ok:
            n_correct += 1
        results.append({
            "tampered_gen": k,
            "verified": bool(rv["verified"]),
            "earliest_broken": rv["earliest_broken"],
            "localized_exact": localized,
            "upstream_clean": before_ok,
            "propagates_forward": from_k_broken,
            "ok": ok,
        })
    passed = (n_correct == len(interior)) and len(interior) > 0
    return {
        "check": "C2_tamper_break_localization",
        "n_gens": n_gens,
        "n_interior": len(interior),
        "n_correct": n_correct,
        "per_gen": results,
        "PASS": passed,
    }


# ── C3 — self-consistent generational fixed point (Novikov) ───────────────────
def _f_closed(c: int, r: float, K: int) -> int:
    """Closed generational map: mitosis growth minus migration/death at capacity K.

    growth = round(r*c*(1 - c/K))  (logistic, the carrying capacity = migration
    budget N_MIGRATE). For c<K growth>0 (births win), c>K growth<0 (migration/death
    wins), c==K growth==0 (closed: future == past). f(c) = c + growth, clamped >=0.
    """
    growth = round(r * c * (1.0 - c / K))
    nxt = c + growth
    return max(0, int(nxt))


def _iterate_to_settle(c0: int, r: float, K: int, max_iter: int = 2000):
    c = c0
    seen = {}
    traj = [c]
    for step in range(max_iter):
        nxt = _f_closed(c, r, K)
        if nxt == c:                       # exact fixed point f(c*)=c*
            return {"settled": True, "c_star": c, "kind": "fixed", "steps": step,
                    "diverged": False, "extinct": (c == 0), "traj_tail": traj[-6:]}
        if nxt > 10 * K:                   # runaway
            return {"settled": False, "c_star": None, "kind": "diverge",
                    "steps": step, "diverged": True, "extinct": False,
                    "traj_tail": traj[-6:]}
        if nxt in seen:                    # cycle (not an exact fixed point)
            return {"settled": False, "c_star": None, "kind": "cycle",
                    "steps": step, "diverged": False, "extinct": False,
                    "traj_tail": traj[-6:]}
        seen[nxt] = step
        c = nxt
        traj.append(c)
        if c == 0:                         # extinction absorbing state
            return {"settled": True, "c_star": 0, "kind": "extinct", "steps": step,
                    "diverged": False, "extinct": True, "traj_tail": traj[-6:]}
    return {"settled": False, "c_star": None, "kind": "no_settle", "steps": max_iter,
            "diverged": False, "extinct": False, "traj_tail": traj[-6:]}


def check_c3():
    # K = engine migration budget N_MIGRATE = 2048 (standing rule in MEMORY/MAIN.tape:
    # per-cell cost crosses the 50ms budget at 2048 -> migrate). r = growth rate 0.5.
    K = 2048
    r = 0.5
    seeds = [1, 5, 50, 500, 1000, 2000, 2048, 3000, 5000]  # below, at, above K
    runs = []
    cstars = set()
    any_diverge = False
    any_extinct_nonzero_seed = False
    for c0 in seeds:
        rec = _iterate_to_settle(c0, r, K, max_iter=5000)
        rec["seed_cells"] = c0
        runs.append(rec)
        if rec["diverged"]:
            any_diverge = True
        if rec["settled"] and rec["kind"] == "fixed":
            cstars.add(rec["c_star"])
        if rec["extinct"] and c0 > 0:
            any_extinct_nonzero_seed = True
    # PASS: every non-extinct seed settles to the SAME bounded fixed point c*=K,
    # f(c*)==c* exactly, no divergence, no extinction from a positive start.
    nonzero_fixed = [r_ for r_ in runs if r_["seed_cells"] > 0 and r_["kind"] == "fixed"]
    same_cstar = (len(cstars) == 1)
    c_star = next(iter(cstars)) if same_cstar else None
    fixed_point_exact = (c_star is not None) and (_f_closed(c_star, r, K) == c_star)
    bounded = (c_star is not None) and (0 < c_star <= K)
    all_positive_settled = all(
        r_["settled"] and r_["kind"] == "fixed" for r_ in runs if r_["seed_cells"] > 0
    )
    passed = (
        all_positive_settled and same_cstar and fixed_point_exact and bounded
        and (not any_diverge) and (not any_extinct_nonzero_seed)
    )
    return {
        "check": "C3_self_consistent_fixed_point",
        "K_capacity": K,
        "r_growth": r,
        "seeds": seeds,
        "c_star": c_star,
        "f(c_star)==c_star": fixed_point_exact,
        "bounded_0_lt_cstar_le_K": bounded,
        "same_cstar_all_seeds": same_cstar,
        "any_diverge": any_diverge,
        "any_extinct_from_positive": any_extinct_nonzero_seed,
        "runs": runs,
        "PASS": passed,
    }


def main():
    t0 = time.time()
    c1 = check_c1()
    c2 = check_c2()
    c3 = check_c3()
    elapsed = round(time.time() - t0, 3)

    def grade(p):
        return "GREEN" if p else "RED"

    summary = {
        "hypothesis": "H_6034 — anima mitosis 세대 순환 = CTC (자기일관 계보)",
        "method": "p7 code-measured; real provenance_chain.py(H_932)+entropy_receipt.py(H_928)+ANU genesis; engine +1 mitosis law; $0 local",
        "anu_genesis_sha16": c1["genesis_hash"],
        "C1": {"verdict": grade(c1["PASS"]), **c1},
        "C2": {"verdict": grade(c2["PASS"]), **c2},
        "C3": {"verdict": grade(c3["PASS"]), **c3},
        "elapsed_s": elapsed,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    main()
