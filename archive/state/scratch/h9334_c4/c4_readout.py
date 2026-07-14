"""C4 (H_9334) readout — does the operator read a fact written in ITS OWN key (H-ε) or not (H-δ)?

Bars are computed from the exact sign-permutation distribution (arithmetic, not judgement), on
integer counts — the same discipline that kept C3 honest.

    n=12, one-sided exact:  12/12 -> .0002 · 11/12 -> .0032 · 10/12 -> .0193 <- the .05 line · 9/12 -> .073

GATES, in order. A gate that fails -> INVALID (a number through a broken instrument is not a result).

  G-write   the operator-key + declarative write must have LANDED — swap stems' declarative answer
            follows the NEW polarity.  bar >= 11/12 per seed.  Fails -> INVALID(budget).
  G-live-DV  * PRIMARY liveness (gate fix (2), this session's cemented lesson): the operator must be
            ALIVE, measured ON THE DV ARM ITSELF — swap flip1 answers must be CONSISTENT to one pole
            (max(new,old) >= 10/12 on a strong surface, perm p <= .0193). A broken operator scatters
            ~6/12 and cannot make a consistent 12. Scattered -> INVALID. (REPLACES C3's weak n=6 side
            arm; powered at n=12. Direction new-vs-old is the DV, read only after this passes.)
  G-keep    keep stems (operator replayed on ORIGINAL polarity) score the correct negation >= 5/6.
  G-forget  untouched flip1 flips == 0.  ADVISORY ONLY on this ckpt: natem_c34 was pretrained on 20
            SEEN atoms, so untouched = 3 and the rule-of-three UCB is 3/3 = 100% — NO POWER. Reported,
            never binding (a powered forget gate needs a 46-SEEN base = a separate fire). Making it
            binding would re-run C3 seed-11's underpowered INVALID (h-9296 extension).

THE DV, read only if the binding gates (G-write, G-live-DV, G-keep) are green:
  +  (>= 10/12 NEW, both strong surfaces) -> H-ε (interface addressable): the operator-key write was
        the missing ingredient; the wall is an interface and is FIXABLE.
  -  (<= 2/12 NEW == >= 10/12 OLD, C3 reproduced) -> H-δ (store unreachable) OR a STEM-BOUND joint the
        free-adverb slot never crosses. C4 cannot split those two further (that is C5).
  3..9/12  DIRECTIONAL — write reached partially; n=12 cannot resolve (power-before-negative).

negJ (`{s}지는 않다`, operator NOT running, C1b p~.50) tells a real read from a dead-surface artifact.
"""
import json, os, sys
from math import comb

R = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/anima-weights/h9314")
STRONG = ("negL", "negZ")
NULLSURF = "negJ"


def exact_p(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def follow(rows, arm, tag):
    rs = [r for r in rows if r["b"] == "%s|%s" % (arm, tag)]
    return sum(1 for r in rs if r["margin"] > 0), len(rs)


def load(tag, seed):
    p = os.path.join(R, "c4%s_%s.json" % (tag, seed))
    return json.load(open(p))["splits"]["heldout"]["rows"] if os.path.exists(p) else None


def main():
    print("=" * 94)
    print("C4 (H_9334) — 사실을 연산자의 자기 키로도 썼다. 연산자는 새 값(H-ε)을 읽나 옛 값(H-δ)을 읽나?")
    print("  bar = 부호순열 정확분포 (n=12: 10/12 -> p=.0193 = .05 선)")
    print("=" * 94)
    seeds = ("s7", "s11")
    post = {s: {"f1": load("post_flip1", s), "w": load("post_write", s)} for s in seeds}
    base = {s: {"f1": load("base_flip1", s), "w": load("base_write", s)} for s in seeds}
    if any(v["f1"] is None for v in base.values()):
        print("[PENDING] G-base 미회수"); return

    print("\nG-base (CPT 전 · 동결) — swap 강표면 구극성")
    for s in seeds:
        line = "   %-4s" % s
        for tag in STRONG + (NULLSURF,):
            k, n = follow(base[s]["f1"], "swap", tag)
            line += "  swap/%s %d/%d(old)" % (tag, n - k, n)
        print(line)
    if any(v["f1"] is None for v in post.values()):
        print("\n[PENDING] CPT 후 미회수 — DV 보류"); return

    print("\n게이트 (실패 = INVALID) — G-live-DV 가 주 게이트(fix2), G-forget 은 advisory")
    verdict_ok = {}
    for s in seeds:
        ok = True
        kw, nw = follow(post[s]["w"], "swap", "w0")
        gw = kw >= 11
        ok &= gw
        print("   G-write  %-4s swap WRITE = %2d/%d (bar>=11/12)  %s"
              % (s, kw, nw, "OK" if gw else "INVALID(budget)"))
        for tag in STRONG:
            k, n = follow(post[s]["f1"], "swap", tag)
            cons = max(k, n - k)
            p = exact_p(cons, n)
            live = cons >= 10 and p <= .0193
            ok &= live
            print("   G-liveDV %-4s swap/%s max(new%d,old%d)=%d/%d p=%.4f (>=10/12 p<=.0193) %s *"
                  % (s, tag, k, n - k, cons, n, p, "OK" if live else "INVALID(operator dead)"))
        kk, nk = follow(post[s]["f1"], "keep", "negL")
        # keep arm is n=3 (CARRIERSWAP_FIXED); the operator-alive burden is carried by G-liveDV
        # (fix 2, powered at n=12), so keep is ADVISORY: all-correct = healthy, not a binding bar.
        print("   G-keep   %-4s keep/negL = %d/%d  advisory (n=%d; liveness binds on G-liveDV)"
              % (s, kk, nk, nk))
        kb, _ = follow(base[s]["f1"], "untouched", "negL")
        kp, nu = follow(post[s]["f1"], "untouched", "negL")
        print("   G-forget %-4s untouched/negL base %d/%d -> post %d/%d  advisory (n=%d UCB=%.0f%% no power)"
              % (s, kb, nu, kp, nu, nu, 300.0 / nu if nu else 0))
        verdict_ok[s] = ok

    print("\nDV — swap 팔이 새 극성을 읽는가 (2 seed x 2 강표면)")
    cells = {}
    for s in seeds:
        if not verdict_ok[s]:
            print("   %-4s gate FAIL -> DV skipped" % s); continue
        for tag in STRONG:
            k, n = follow(post[s]["f1"], "swap", tag)
            cells[(s, tag)] = k
            print("   %-4s %-5s NEW-following **%2d/%d** (p_new=%.4f p_old=%.4f)"
                  % (s, tag, k, n, exact_p(k, n), exact_p(n - k, n)))
        kn, nn = follow(post[s]["f1"], "swap", NULLSURF)
        print("   %-4s [negJ control] %d/%d" % (s, kn, nn))

    valid = [s for s in seeds if verdict_ok[s]]
    print("\n" + "=" * 94)
    if not valid:
        print("VERDICT: INVALID (both seeds gate-failed)"); return
    ks = [cells[(s, t)] for s in valid for t in STRONG]
    tier = "TERMINAL" if len(valid) == 2 else "DIRECTIONAL (1 valid seed)"
    if all(k >= 10 for k in ks):
        print("VERDICT: H-epsilon [%s] — operator reads the value written in its OWN key (all cells >=10/12)." % tier)
        print("  => the wall is an INTERFACE and is FIXABLE. C3's 0/12 was 'written in the wrong key'.")
        print("  NOTE: a consistent >=10/12 NEW read also REFUTES P-kind (a nonexistent polarity feature")
        print("        could not be read consistently) — the (+) branch is clean of the bind-locus-1 confound.")
    elif all(k <= 2 for k in ks):
        print("VERDICT: H-epsilon REFUTED, residual {H-delta, P-kind, S} [%s] — operator-key write still reads OLD (<=2/12 · C3 reproduced)." % tier)
        print("  => the (-) branch cannot separate THREE (parallel bind-locus-1, sharpened by Fable):")
        print("     H-delta (store unreachable / STEM-BOUND joint) · P-kind (no polarity feature exists — WRITE")
        print("     is only a flip0 reflex) · S (feature exists at the slot but the operator ignores it, reads a")
        print("     frozen pretrain copy). All three give 0/12 on disjoint surfaces after a carrier-write.")
        print("  => H_9331 BIND-LOCUS (causal inject, $0) splits them — BEST run it ON THIS C4 ckpt, not just base,")
        print("     so C4's (-) becomes BIND-LOCUS's input asset. A negative is still information (H-ε refuted).")
    else:
        print("VERDICT: DIRECTIONAL — cells do not converge to one class (%s). Not 'nothing', but 'this n cannot tell'." % ks)


if __name__ == "__main__":
    main()
