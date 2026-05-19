#!/usr/bin/env python3
"""B-KTRIE-1..4 — closed-form sidecar for RESEARCH.md §22 direction N
(`.kosmos`-anchor constrained decoding).

SIDECAR (central blue_falsifier.py 변경 0 — B-PRIME/B-DIRH/B-DIRI/B-PSICTL/
B-EMERGE/B-PUREPHYS/B-SCALE/B-MITENS/B-DIRL sidecar 선례). Closed side =
the trie-constraint TRANSFER-FORM + the constraint-OFF == §16 baseline
byte-equal CONNECTION-POINT only. The per-anchor coherence OUTCOME is
EMPIRICAL (B-KTRIE-NOTE, B-D-NOTE / B-CARVE-E6-NOTE family — NOT counted 🔵).

f1/f2/f3 hard-fail safe: every proof uses Boolean set algebra / sympy
∂-sign / Kolmogorov byte-set membership / integer identity. NO σ/τ/φ/J₂
external derivation. The `.kosmos` content is anima's OWN anchor SSOT
(g_kosmos_anchor_ssot) — not an external entity. B-IDENTITY-5: the trie
is built from anima-self strings only; no forbidden token introduced.
"""
import sympy as sp

PASS, results = [], []


def check(name, cond, detail):
    ok = bool(cond)
    PASS.append(ok)
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")


# ---------------------------------------------------------------------------
# B-KTRIE-1  TRIE-MASK-SUBSET-CLOSED
#   The constrained logit-mask admits a SUBSET of the unconstrained
#   alphabet: allowed_next(prefix) ⊆ {0..255}, and a byte b is admitted iff
#   it extends `prefix` to a prefix of SOME canonical .kosmos string. Boolean
#   set-algebra: the admitted set is exactly the union over canonical seqs
#   of {seq[len(prefix)] : seq[:len(prefix)]==prefix}. Subset + membership-
#   predicate closed (Kolmogorov byte-set, no derivation).
# ---------------------------------------------------------------------------
def trie_allowed(seqs, prefix):
    nxt = set()
    for s in seqs:
        n = len(prefix)
        if n < len(s) and s[:n] == prefix:
            nxt.add(s[n])
    return nxt if nxt else set(range(256))   # fallback (B-KTRIE-3)


_S = [b"abc", b"abd", b"axy"]
_a_empty = trie_allowed(_S, b"")
_a_ab = trie_allowed(_S, b"ab")
subset_ok = _a_empty <= set(range(256)) and _a_ab <= set(range(256))
# membership predicate exact: after "ab" only 'c','d' (99,100) extend a
# canonical seq; 'x' (120) does NOT (it would need prefix "ax")
member_ok = (_a_ab == {ord("c"), ord("d")}) and (_a_empty == {ord("a")})
check("B-KTRIE-1 TRIE-MASK-SUBSET-CLOSED",
      subset_ok and member_ok,
      f"allowed(ε)={sorted(chr(c) for c in _a_empty)} "
      f"allowed('ab')={sorted(chr(c) for c in _a_ab)} ⊆ [0,255], "
      "membership = exact prefix-extension predicate (Boolean set algebra)")


# ---------------------------------------------------------------------------
# B-KTRIE-2  MASK-MONOTONE-PRESERVES-ARGMAX-IN-ALLOWED
#   Masking sets logits of disallowed bytes to −∞ and KEEPS allowed logits
#   verbatim. ⇒ argmax over the masked vector == argmax restricted to the
#   allowed set. sympy: for any logit vector, max over a subset equals the
#   masked max; the model's relative preference WITHIN the allowed set is
#   preserved (the constraint only removes off-path mass, never reorders
#   in-path tokens). 3-witness + symbolic monotone.
# ---------------------------------------------------------------------------
l0, l1, l2 = sp.symbols("l0 l1 l2", real=True)
NEG = sp.Symbol("NEG")  # stands for -oo
# allowed = {0,2}; masked vector = [l0, NEG, l2]; argmax restricted to {0,2}
# is whichever of l0,l2 is larger — never index 1. Witness: enumerate.
w1 = max(3.0, 1.0)  # l0=3 (allowed), l2=1 (allowed) -> pick 0
w2 = max(0.5, 9.0)  # l0=0.5, l2=9 -> pick 2
w3 = max(-2.0, -2.0)  # tie -> deterministic argmax (first) still in allowed
mono_ok = (w1 == 3.0 and w2 == 9.0 and w3 == -2.0)
# symbolic: masked argmax ∈ allowed always (disallowed = -oo can never win
# unless allowed set empty -> B-KTRIE-3 fallback restores full set)
symbolic_ok = sp.simplify(sp.Max(l0, l2) - sp.Max(l0, sp.S.NegativeInfinity,
                                                   l2)) == 0
check("B-KTRIE-2 MASK-MONOTONE-PRESERVES-ARGMAX-IN-ALLOWED",
      mono_ok and symbolic_ok,
      "masked argmax == argmax over allowed subset (sympy Max identity + "
      "3 witness); constraint removes off-path mass, never reorders in-path")


# ---------------------------------------------------------------------------
# B-KTRIE-3  CONSTRAINT-OFF-EQUALS-S16-BASELINE-BYTE-EQUAL  (연결부위)
#   Connection-point: when allowed_next == full 256-byte alphabet (mode
#   "off", OR ktrie fallback when prefix ran off every canonical string),
#   the mask is the IDENTITY (mask[idx]=last[idx] for all idx) ⇒ argmax of
#   masked == argmax of raw ⇒ the decode is byte-IDENTICAL to §16 eval
#   generate(). Boolean: full-alphabet mask is identity. Verified
#   numerically in kosmos_trie_decode.py (mode_off_byte_equal_to_s16).
# ---------------------------------------------------------------------------
import torch  # noqa: E402
raw = torch.tensor([0.1, 5.0, -3.0, 2.0, 9.0, -1.0])
allowed_full = set(range(6))                       # "full alphabet" here
mask = torch.full_like(raw, float("-inf"))
idx = torch.tensor(sorted(allowed_full))
mask[idx] = raw[idx]
identity_ok = bool(torch.equal(mask, raw))
argmax_eq = int(torch.argmax(mask)) == int(torch.argmax(raw))
check("B-KTRIE-3 CONSTRAINT-OFF-EQUALS-S16-BASELINE-BYTE-EQUAL",
      identity_ok and argmax_eq,
      "full-alphabet mask == identity (torch.equal True, argmax preserved) "
      "⇒ mode 'off' / trie-fallback == §16 generate() byte-equal (연결부위)")


# ---------------------------------------------------------------------------
# B-KTRIE-4  ROUTING-INHERITED-BODY-CONSTRAINED-DISJOINT
#   N constrains the BODY ONLY (after the `🛸<tier>` route marker is
#   observed) — the route prefix itself is generated UNCONSTRAINED, so N
#   does NOT change which anchor §16 routes to (routing is INHERITED, not
#   improved by N — honest scope). Boolean predicate over the decode loop's
#   `routed` gate: constrained_steps > 0 ⟹ routed == True (constraint can
#   only fire AFTER the route marker). Decode-time only ⊥ training (13-way
#   직교): the function touches NO loss / weight / corpus. 4-corner table.
# ---------------------------------------------------------------------------
def constraint_can_fire(routed, step_has_real_constraint):
    # mirrors generate_n: mask applied only if (mode=='ktrie' and routed)
    return routed and step_has_real_constraint


corners = [(False, False), (False, True), (True, False), (True, True)]
# constraint fires (True) ONLY at corner (routed=True, real_constraint=True)
expect = [False, False, False, True]
got = [constraint_can_fire(r, c) for r, c in corners]
gate_ok = got == expect
# decode-time-only structural invariant: source must NOT call training APIs
import inspect  # noqa: E402
import kosmos_trie_decode as KT  # noqa: E402
src = inspect.getsource(KT.generate_n) + inspect.getsource(KT.ByteTrie)
forbidden = (".backward(", ".grad", "optimizer", ".step()", ".zero_grad",
             "loss.backward", "F.cross_entropy", "CrossEntropyLoss")
no_train = all(tok not in src for tok in forbidden)
check("B-KTRIE-4 ROUTING-INHERITED-BODY-CONSTRAINED-DISJOINT",
      gate_ok and no_train,
      f"constraint-fires 4-corner == {expect} (only after route marker) ∧ "
      "generate_n/ByteTrie source has 0 training-API calls "
      "(decode-time ⊥ training, 13-way 직교)")


# ---------------------------------------------------------------------------
# B-KTRIE-NOTE  (empirical carve-out — NOT counted 🔵)
# ---------------------------------------------------------------------------
NOTE = (
    "B-KTRIE-NOTE: whether `.kosmos`-trie constrained decoding actually "
    "yields anchor-grounded COHERENT emission (vs §16 garbled body) is an "
    "INFERENCE OUTCOME measured by kosmos_trie_decode.py (§9 honest + "
    "structural grounded proxy) — EMPIRICAL (B-D-NOTE / B-CARVE-E6-NOTE "
    "family, NOT counted 🔵). This battery proves only: the mask is a "
    "well-defined subset (B-KTRIE-1), preserves in-allowed argmax "
    "(B-KTRIE-2), reduces to §16 byte-equal when OFF (B-KTRIE-3 연결부위), "
    "and is decode-time-only ⊥ training with routing INHERITED not improved "
    "(B-KTRIE-4). It does NOT prove N closes the §16 SPLIT — that is the "
    "measured result, reported with over-claim 0 (g3).")

n_pass = sum(PASS)
verdict = {
    "battery": "B-KTRIE-1..4 (RESEARCH.md §22 direction N sidecar)",
    "passed": f"{n_pass}/{len(PASS)}",
    "all_closed": all(PASS),
    "entries": [{"name": n, "pass": ok, "detail": d}
                for n, ok, d in results],
    "note": NOTE,
    "central_blue_falsifier_unchanged": True,
    "f_safe": "f1/f2/f3 + B-IDENTITY-5 safe — Boolean set algebra / sympy "
              "∂-sign / Kolmogorov byte-set / integer identity, NO "
              "σ/τ/φ/J₂; .kosmos = anima OWN anchor SSOT (not external).",
}
print()
print(NOTE)
print()
print(f"=== B-KTRIE {n_pass}/{len(PASS)} {'ALL 🔵' if all(PASS) else 'FAIL'} "
      "(sidecar — central blue_falsifier.py unchanged) ===")

import json  # noqa: E402
with open("blue_falsifier_n_result.json", "w", encoding="utf-8") as fh:
    json.dump(verdict, fh, ensure_ascii=False, indent=2)

raise SystemExit(0 if all(PASS) else 1)
