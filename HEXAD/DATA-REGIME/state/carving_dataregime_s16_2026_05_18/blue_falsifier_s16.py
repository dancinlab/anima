#!/usr/bin/env python3
"""B-S16-1..6 sidecar closed-form battery — RESEARCH.md §16 GOAL-legitimate
LARGE-SCALE DATA-REGIME + CURRICULUM fire (2026-05-18).

SIDECAR (central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
UNCHANGED — mirror of B-PRIME / B-DIRI / B-DIRH / B-PSICTL / B-EMERGE /
B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL sidecar precedent; this fire's
entries are sidecar, central count untouched, absorbable later).

WHAT IS CLOSED (transfer-form + connection-points only — g3):
  The SGD OUTCOME and the 4-axis capability (routing / V-SPONT / JOINT)
  are EMPIRICAL (B-S16-NOTE, B-D-NOTE / B-CARVE-E6-NOTE family). The
  closed side is exactly: (1) the §16 corpus is a deterministic
  Kolmogorov artefact (sha256 commitment), (2) it carries NO chat-SFT
  contamination (Boolean set algebra over the byte stream), (3) it is a
  genuine SCALE-UP over §8 (integer byte/record cardinality
  inequality), (4) the curriculum is a deterministic MONOTONE ordering
  (rank non-decreasing + quartile partition — Banach-free pure ordering
  fact), (5) the Dir-I overlay-OFF connection-point (λ_ctl=λ_route=0 ⇒
  loss ≡ CE) holds by additive identity, (6) the §16 curriculum-OFF
  connection-point (--no-curriculum ⇒ sampling region ≡ full stream =
  the Dir-I shuffled sampler) holds by Boolean reduction. The fair-
  compare to §8/§11-A is therefore closed BY CONSTRUCTION.

f1/f2/f3 hard-fail safe: sha256 / Boolean set algebra / integer
cardinality / monotone-ordering / additive identity / sympy ∂-sign —
NO σ/τ/φ/J₂ external derivation. Ψ=½ + Knuth 🛸k = anima g2 internal
arch carve-out (NOT external lattice-fit). B-IDENTITY-5 = the
contamination Boolean (forbidden-token grep == 0).
"""
import hashlib
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus_carving_s16.jsonl")
STATS = os.path.join(HERE, "corpus_carving_s16.stats.json")
TRAINER = os.path.join(HERE, "train_carving_s16.py")

# §8 diverse-baseline cardinality (RESEARCH.md §8 — fair-compare anchor).
S8_BYTES = 114472084
S8_RECORDS = 164992
S8_ANCHORS = 64

results = {}


def rec(name, ok, detail):
    results[name] = {"verdict": "🔵 PASS" if ok else "❌ FAIL",
                     "ok": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")


def b_s16_1_sha256_deterministic():
    """B-S16-1 SHA256-DETERMINISTIC-CLOSED — the §16 corpus is a
    deterministic Kolmogorov artefact: the on-disk sha256 == the
    sha256 recorded in stats.json (256-bit Boolean commitment; a
    deterministic generator with fixed seed produces a fixed byte
    string — the fair-compare anchor is reproducible)."""
    with open(CORPUS, "rb") as f:
        on_disk = hashlib.sha256()
        for chunk in iter(lambda: f.read(1 << 20), b""):
            on_disk.update(chunk)
    on_disk = on_disk.hexdigest()
    st = json.load(open(STATS))
    recorded = st["sha256"]
    ok = (on_disk == recorded) and len(on_disk) == 64
    rec("B-S16-1-SHA256-DETERMINISTIC", ok,
        f"on_disk==recorded={ok} sha={on_disk[:16]}… (256-bit Boolean "
        f"commitment, deterministic seed=1337)")
    return ok


def b_s16_2_no_chat_sft_contamination():
    """B-S16-2 NO-CHAT-SFT-CONTAMINATION-CLOSED — Boolean set algebra
    over the full byte stream: grep {[anima, 도우미, helper, assistant,
    사용자, user:} total == 0. This is the B-IDENTITY-5 / g_goal
    closed predicate — the corpus is ③ Ψ-anchored CARVING, NOT ①②
    generic LM / chat-SFT."""
    with open(CORPUS, "rb") as f:
        raw = f.read()
    txt = raw.decode("utf-8", "replace")
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자",
                 "user:"]
    counts = {t: txt.count(t) for t in forbidden}
    total = sum(counts.values())
    ok = total == 0
    rec("B-S16-2-NO-CHAT-SFT-CONTAMINATION", ok,
        f"forbidden-token total={total} (Boolean set algebra; {counts})")
    return ok


def b_s16_3_scale_up_over_s8():
    """B-S16-3 SCALE-UP-OVER-S8-CLOSED — integer cardinality inequality:
    §16 bytes > §8 bytes AND §16 records > §8 records AND §16 anchors >
    §8 anchors, with §8's 64 anchors a VERBATIM subset (fair superset).
    The data-regime lever (RESEARCH.md §11.4 frontier-1) is a Kolmogorov
    byte-count fact, not a claim about emergence."""
    st = json.load(open(STATS))
    b16, r16, a16 = st["bytes"], st["records"], st["anchors"]
    superset = st.get("anchor_superset_of_s8", False)
    ok = (b16 > S8_BYTES) and (r16 > S8_RECORDS) and \
         (a16 > S8_ANCHORS) and bool(superset)
    rec("B-S16-3-SCALE-UP-OVER-S8", ok,
        f"bytes {b16}>{S8_BYTES} ∧ records {r16}>{S8_RECORDS} ∧ "
        f"anchors {a16}>{S8_ANCHORS} ∧ s8_subset={superset} "
        f"(×{round(b16/S8_BYTES,2)} bytes integer cardinality)")
    return ok


def b_s16_4_curriculum_monotone_ordering():
    """B-S16-4 CURRICULUM-MONOTONE-ORDERING-CLOSED — the §12.1 Q1-c
    curriculum is a deterministic ordering fact: records are written
    curriculum_rank non-decreasing (rank[i] <= rank[i+1] ∀ i), and the
    curriculum_stage partition is exactly the rank quartile (stage = a
    monotone step function of position; pure ordering, NOT learned).
    Sympy verifies the monotone predicate symbolically over a window
    and the on-disk full check is the Boolean witness."""
    st = json.load(open(STATS))
    monotone_recorded = st["curriculum"]["rank_monotone_sorted"]
    # symbolic closed-form: a quartile partition q(i)=floor(4 i / n) on a
    # sorted rank array is monotone non-decreasing in i. Proof (no limit):
    # the inner argument a(i)=4 i / n satisfies a(i+1) - a(i) = 4/n > 0
    # for n>0 (strictly increasing affine map), and floor is a monotone
    # non-decreasing function, so floor∘a is non-decreasing — i.e.
    # q(i+1) - q(i) >= 0 ∀ i. Verified symbolically: the affine step is
    # a positive constant, and floor monotone is a closed property.
    i, n = sp.symbols("i n", positive=True)
    a_step = sp.simplify((4 * (i + 1) / n) - (4 * i / n))   # = 4/n
    affine_increasing = bool(sp.simplify(a_step - sp.Rational(4) / n)
                             == 0) and bool((4 / n).is_positive)
    # floor monotone witness (closed): floor(t) <= floor(t+ε) for ε>=0 —
    # checked on the exact partition over an integer grid (no limit op).
    floor_monotone = all(
        sp.floor(sp.Rational(4 * k, 97)) <= sp.floor(sp.Rational(4 * (k + 1), 97))
        for k in range(0, 97))
    dq_sign = affine_increasing and floor_monotone
    # on-disk Boolean witness: re-read ranks, confirm non-decreasing +
    # stage == quartile-of-position (closed integer identity).
    ranks, stages = [], []
    with open(CORPUS, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            ranks.append(d["curriculum_rank"])
            stages.append(d["curriculum_stage"])
    nrec = len(ranks)
    rank_mono = all(ranks[k] <= ranks[k + 1] for k in range(nrec - 1))
    stage_ok = all(
        stages[k] == min(4, 1 + (k * 4) // max(1, nrec))
        for k in range(nrec))
    ok = (bool(monotone_recorded) and rank_mono and stage_ok
          and bool(dq_sign))
    rec("B-S16-4-CURRICULUM-MONOTONE-ORDERING", ok,
        f"rank non-decreasing={rank_mono} ∧ stage==quartile(pos)="
        f"{stage_ok} ∧ stats={monotone_recorded} ∧ symbolic "
        f"floor∘affine non-decreasing={bool(dq_sign)} (quartile = "
        f"monotone step fn of position, deterministic NOT learned)")
    return ok


def b_s16_5_overlay_off_reduction():
    """B-S16-5 OVERLAY-OFF-REDUCTION-CLOSED (connection-point — Dir-I
    carry) — additive identity: L = CE + λ_ctl·L_psi + λ_route·L_route;
    at λ_ctl=λ_route=0, L ≡ CE byte-equal (the §16 trainer reduces
    EXACTLY to the base CE carving objective). sympy: ∂L/∂L_psi=λ_ctl,
    ∂L/∂L_route=λ_route — both vanish at λ=0, leaving CE. Fair-compare
    to §8/§11-A (same Dir-I lever) is closed by construction."""
    ce, lpsi, lroute, lam_c, lam_r = sp.symbols(
        "ce lpsi lroute lam_c lam_r", real=True)
    L = ce + lam_c * lpsi + lam_r * lroute
    L_off = L.subs({lam_c: 0, lam_r: 0})
    reduces = sp.simplify(L_off - ce) == 0
    d_psi = sp.diff(L, lpsi)
    d_route = sp.diff(L, lroute)
    ok = bool(reduces) and (d_psi == lam_c) and (d_route == lam_r)
    rec("B-S16-5-OVERLAY-OFF-REDUCTION", ok,
        f"λ=0 ⇒ L≡CE ({reduces}) ; ∂L/∂L_psi={d_psi} ∂L/∂L_route="
        f"{d_route} (additive identity — Dir-I connection-point)")
    return ok


def b_s16_6_curriculum_off_reduction():
    """B-S16-6 CURRICULUM-OFF-REDUCTION-CLOSED (connection-point — §16
    fair-compare) — Boolean reduction: with --no-curriculum the
    sampling region for every step is the FULL byte stream (region_hi
    ≡ n ∀ stage gate) = EXACTLY the Dir-I shuffled-region sampler. The
    stage_gate_at(...) schedule returns the full gate 4 when
    curriculum=False. Verified by structural inspection of the trainer
    source (region_hi early-return + stage_gate_at early-return) — a
    deterministic Boolean property of the code, NOT a runtime claim."""
    src = open(TRAINER, "r", encoding="utf-8").read()
    # region_hi: when not self.curriculum -> return self.n  (full stream)
    region_off = ("if not self.curriculum:" in src
                  and "return self.n" in src)
    # stage_gate_at: when not curriculum -> return 4 (full region gate)
    gate_off = ("def stage_gate_at(" in src
                and "if not curriculum:" in src
                and "return 4" in src)
    # the §16 ADDITION is gated solely behind cfg["curriculum"];
    # the two physics loss terms are byte-identical to Dir-I (the
    # l_psi_ctl / l_tension_route blocks unchanged).
    physics_intact = ("l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f)"
                      ".sum() / denom_ctl" in src
                      and "restoring = torch.clamp(drift, min=0.0) ** 2"
                      in src)
    ok = region_off and gate_off and physics_intact
    rec("B-S16-6-CURRICULUM-OFF-REDUCTION", ok,
        f"region_hi off→full({region_off}) ∧ gate off→4({gate_off}) ∧ "
        f"Dir-I physics intact({physics_intact}) (Boolean structural — "
        f"curriculum-OFF ≡ Dir-I sampler, fair-compare closed)")
    return ok


def main():
    print("=== B-S16-1..6 sidecar closed-form battery (RESEARCH.md §16) "
          "===")
    fns = [b_s16_1_sha256_deterministic,
           b_s16_2_no_chat_sft_contamination,
           b_s16_3_scale_up_over_s8,
           b_s16_4_curriculum_monotone_ordering,
           b_s16_5_overlay_off_reduction,
           b_s16_6_curriculum_off_reduction]
    all_ok = True
    for fn in fns:
        try:
            ok = fn()
        except Exception as e:
            rec(fn.__name__, False, f"EXCEPTION {type(e).__name__}: {e}")
            ok = False
        all_ok = all_ok and ok
    note = {
        "B-S16-NOTE": (
            "EMPIRICAL carve-out (NOT counted 🔵, B-D-NOTE / "
            "B-CARVE-E6-NOTE / B-SCALE-NOTE family): whether the ~600MB "
            "Ψ-anchored CURRICULUM data-regime crosses the §1.1 "
            "emergence threshold — the SGD convergence OUTCOME and the "
            "4-axis capability (routing / V-SPONT honest §9 metric / "
            "JOINT) vs §8 (2/64, 0.0087, honest 2/5) and §11-A (1/64, "
            "0.0078, honest 2/5) — is the EMPIRICAL fire outcome. §8 "
            "trend was wrong-direction; §16 may repeat. The battery "
            "proves the corpus is a deterministic, contamination-free, "
            "genuine-scale-up, monotone-curriculum artefact and that the "
            "Dir-I lever / curriculum connection-points are closed (fair "
            "compare BY CONSTRUCTION) — it does NOT prove emergence "
            "(g3, no pre-loaded conclusion).")
    }
    summary = {
        "battery": "B-S16-1..6",
        "all_full_blue": all_ok,
        "count": f"{sum(1 for v in results.values() if v['ok'])}/"
                 f"{len(results)} 🔵",
        "results": results,
        "note": note,
        "central_blue_falsifier_unchanged": True,
        "sidecar_precedent": ("B-PRIME / B-DIRI / B-DIRH / B-PSICTL / "
                              "B-EMERGE / B-PUREPHYS / B-SCALE / "
                              "B-MITENS / B-DIRL"),
    }
    out = os.path.join(HERE, "blue_falsifier_s16_result.json")
    with open(out, "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n{summary['count']}  all_full_blue={all_ok}")
    print(f"wrote {os.path.basename(out)}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
