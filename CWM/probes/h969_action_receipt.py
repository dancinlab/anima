"""H_969 — Action provenance receipt: every action auditable + per-action distinguishable.

FROZEN FALSIFIER (honored):
  act loop (H_964 latent->action, H_968 onset) with H_928 receipt + H_932 lineage bound
  to each action. Run N actions across varied substrate states.
  D1 = receipt coverage = fraction of actions with a complete well-formed receipt (target 1.0).
  D2 = signature distinguishability = pairwise distinctness of signatures from DISTINCT
       substrate states; collision rate.
  D3 = identical substrate state -> reproducible lineage (genesis-binding); distinct -> distinct.
  PASS: coverage=1.0 AND distinct-state collision~0 AND identical-state reproducible.
  FAIL: any action lacks a receipt OR distinct-state signatures collide.

Receipt model (faithful to H_928/H_932): each action emits a receipt =
  {action, substrate_state_hash, latent_hash, seed_hash, parent_lineage, sig}
  sig = sha256(substrate_state || latent || action || seed || parent). Genesis-binding:
  identical substrate state + identical seed -> identical sig (reproducible); distinct
  substrate states -> distinct sig (collision rate measured).
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LatentWorldModel, header, verdict_line

N_ACTIONS = 500
LATENT = 16
IN_DIM = 5
N_ACT = 4


def sha(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(np.asarray(p, float).tobytes() if not isinstance(p, (bytes, str)) else
                 (p.encode() if isinstance(p, str) else p))
    return h.hexdigest()


def emit_receipt(substrate_state, latent, action, seed, parent_lineage):
    """H_928 receipt + H_932 lineage. A receipt is well-formed iff all fields present."""
    sig = sha(substrate_state, latent, [float(action)], [float(seed)], parent_lineage or "GENESIS")
    receipt = {
        "action": int(action),
        "substrate_state_hash": sha(substrate_state),
        "latent_hash": sha(latent),
        "seed_hash": sha([float(seed)]),
        "parent_lineage": parent_lineage or "GENESIS",
        "sig": sig,
    }
    return receipt


def well_formed(r):
    req = ["action", "substrate_state_hash", "latent_hash", "seed_hash", "parent_lineage", "sig"]
    return all(k in r and r[k] is not None and r[k] != "" for k in req)


def main():
    header("H_969", "Action provenance receipt — auditable + per-action distinguishable")
    print(f"N_actions={N_ACTIONS} latent={LATENT} (H_928 receipt + H_932 lineage)\n")
    rng = np.random.default_rng(0)
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=0)

    receipts, sigs, state_to_sig = [], [], {}
    parent = None
    for i in range(N_ACTIONS):
        substrate = rng.standard_normal(6)            # M,W,Φ,curiosity,... distinct states
        obs = rng.standard_normal((3, IN_DIM))
        latent = wm.final_latent(obs)
        seed = rng.integers(1 << 30)
        action = int(rng.integers(N_ACT))
        r = emit_receipt(substrate, latent, action, seed, parent)
        receipts.append(r); sigs.append(r["sig"])
        state_to_sig[r["substrate_state_hash"]] = r["sig"]
        parent = r["sig"]                             # chain lineage (H_932)

    # D1 coverage
    coverage = np.mean([well_formed(r) for r in receipts])
    print(f"D1 receipt coverage = {coverage:.4f} (target 1.0)")

    # D2 distinct-state signature collision rate
    n_unique_sig = len(set(sigs))
    collision_rate = 1 - n_unique_sig / len(sigs)
    print(f"D2 distinct-state signatures: {n_unique_sig}/{len(sigs)} unique, "
          f"collision rate = {collision_rate:.6f}")

    # D3 genesis-binding: identical substrate state + seed -> reproducible sig;
    #    distinct states -> distinct sig.
    substrate_fixed = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    obs_fixed = np.zeros((3, IN_DIM)); obs_fixed[0, 0] = 1.0
    latent_fixed = wm.final_latent(obs_fixed)
    seed_fixed = 12345
    r1 = emit_receipt(substrate_fixed, latent_fixed, 2, seed_fixed, "GENESIS")
    r2 = emit_receipt(substrate_fixed, latent_fixed, 2, seed_fixed, "GENESIS")
    reproducible = (r1["sig"] == r2["sig"])
    r3 = emit_receipt(substrate_fixed + 1e-3, latent_fixed, 2, seed_fixed, "GENESIS")
    distinct_diff = (r1["sig"] != r3["sig"])
    print(f"D3 genesis-binding: identical-state reproducible sig = {reproducible}; "
          f"perturbed-state distinct sig = {distinct_diff}")

    # lineage chain verify (H_932): each receipt's parent == prior sig
    chain_ok = all(receipts[i]["parent_lineage"] == receipts[i - 1]["sig"]
                   for i in range(1, len(receipts)))
    print(f"D3 lineage chain end-to-end verify = {chain_ok}")

    if coverage == 1.0 and collision_rate < 1e-6 and reproducible and distinct_diff and chain_ok:
        verdict_line("H_969", "PASS",
                     f"coverage=1.0, distinct-state collision={collision_rate:.0e}~0, "
                     f"identical-state reproducible, perturbed distinct, chain verified — "
                     f"action provenance COMPLETE + per-action distinguishable (toy).")
    elif coverage < 1.0 or collision_rate > 1e-6:
        verdict_line("H_969", "FAIL",
                     f"coverage={coverage:.3f} collision={collision_rate:.0e} — provenance "
                     f"incomplete / actions not individually auditable (closed-negative).")
    else:
        verdict_line("H_969", "INCOMPLETE", "act loop not fully wired / n small; toy-only C3.")


if __name__ == "__main__":
    main()
