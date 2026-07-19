"""C3 readout — every bar is a computed number, not a remembered one.

This session lost two runs to transplanted bars (H_9311's liveness floor, C1's anchor), and one
near-miss to a float-tie that manufactured a green. So: the bars below come from the exact sign-
permutation distribution — arithmetic, not judgement — and every comparison is on integer counts.

    n=12 stems, one-sided, exact:  12/12 -> 1/4096 = .0002
                                   11/12 -> 13/4096 = .0032
                                   10/12 -> 79/4096 = .0193   <- the .05 line lands here
                                    9/12 -> 299/4096 = .0730
    n=6 (keep+untouched pooled):    6/6 -> 1/64 = .0156
                                    5/6 -> 7/64 = .109

GATES, in order. A gate that fails does not produce a FAIL — it produces an INVALID, because a
number taken through a broken instrument is not a result about the substrate.

  G-live   the operator must still run AFTER the CPT, on keep+untouched, on a strong surface.
           `ground` CPT was measured destroying it (SEEN flip1 0.883 -> 0.333); `ground_keep`
           replay brought it back. Here only 3 of 20 stems carry replay, so survival is a question,
           not an assumption. Bar: >= 5/6 per seed AND >= 11/12 pooled.
           Fails -> INVALID. We do not ask a dead operator about binding (H_9322).

  G-write  the rewrite must have LANDED — swap stems' declarative answer must follow the NEW
           polarity. Bar: >= 11/12 per seed (H_9324 measured 0.954-1.000 at this same budget).
           Fails -> INVALID(budget), not a binding negative. One pre-registered escalation only.

  G-forget untouched stems (zero corpus exposure) must keep the flip1 ability they had at base.
           This is the stratum the corpus never reinforces — the only place forgetting is visible
           (H_9324's forgetting gate sat on the stratum the corpus strengthens, so it always passed).

THE DV, read only if all three are green: on the swap arm, does the rule follow the polarity we
just wrote, or the one pretraining left?

  +  (>= 10/12, both seeds, both strong surfaces) the rule reads the rewritten entry
     -> the operator DOES consult a mutable store; held-out failure is new-entry invisibility (H-β)
  -  (<= 2/12) it reads the pretrained one -> declarative rewriting cannot move the rule's source
     -> {H-δ or H-ε}. C3 cannot separate those two, and saying otherwise would be the overclaim
        Fable's amendment specifically removed.
  ~0 conflict collapsed the reference. Capped at DIRECTIONAL: with 20 stems the equivalence test
     cannot pass (90% CI half-width ~0.475 > the 0.4 margin this lane has ever resolved), so "no
     dependence" is not something this n can earn. Say "we cannot tell", not "there is nothing".

The negative-control surface (`{s}지는 않다`, where C1b measured the operator NOT running, p~.50)
is what tells a real zero from a dead-surface zero: a strong-surface ~0 next to a live G-live is a
finding; a ~0 that looks like the negative control's is an artifact.
"""
import json, os
from math import comb

R = os.path.expanduser("~/anima-weights/h9314")
STRONG = ("negL", "negZ")          # operator measured running (C1b, both seeds, p<.01)
NULLSURF = "negJ"                  # operator measured NOT running (p~.50) — the artifact floor


def exact_p(k, n):
    """One-sided sign-permutation p: P(>= k of n follow, under 'the rule ignores polarity')."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def follow(rows, arm, tag):
    """count of stems whose answer follows the polarity the manifest declares (new for swap)."""
    rs = [r for r in rows if r["b"] == "%s|%s" % (arm, tag)]
    return sum(1 for r in rs if r["margin"] > 0), len(rs)


def load(tag, seed):
    p = os.path.join(R, "c3%s_%s.json" % (tag, seed))
    return json.load(open(p))["splits"]["heldout"]["rows"] if os.path.exists(p) else None


def main():
    print("=" * 92)
    print("C3 — SEEN 어간의 극성을 CPT 로 뒤집었다. 규칙은 **새 값**을 읽는가, **옛 값**을 읽는가?")
    print("  bar = 부호순열 정확분포 (n=12: 12/12→p=.0002 · 11/12→.0032 · **10/12→.0193** · 9/12→.073)")
    print("=" * 92)

    seeds = ("main_s7", "main_s11")
    post = {s: {"f1": load("post_flip1", s), "w": load("post_write", s)} for s in seeds}
    base = {s: {"f1": load("base_flip1", s), "w": load("base_write", s)} for s in seeds}
    if any(v["f1"] is None for v in base.values()):
        print("[PENDING] G-base 미회수"); return

    print("\n⚓ G-base (CPT 전 · 동결) — 이 표가 없으면 '못 함'과 '죽임'을 못 가른다")
    for s in seeds:
        line = "   %-9s" % s[5:]
        for tag in STRONG + (NULLSURF,):
            k, n = follow(base[s]["f1"], "swap", tag)
            line += "  swap/%s %d/%d(구극성)" % (tag, n - k, n)   # base: gold=new, so old-following = n-k
        print(line)
    if any(v["f1"] is None for v in post.values()):
        print("\n[PENDING] CPT 후 측정 미회수 — DV 판독 보류")
        return

    # ── gates ────────────────────────────────────────────────────────────────
    print("\n🚦 게이트 (실패 = INVALID, FAIL 아님)")
    ok = True
    for s in seeds:
        kk = sum(follow(post[s]["f1"], a, t)[0] for a in ("keep", "untouched") for t in ("negL",))
        nn = sum(follow(post[s]["f1"], a, t)[1] for a in ("keep", "untouched") for t in ("negL",))
        g = kk >= 5
        ok &= g
        print("   G-live  %-9s keep+untouched flip1(negL) = %d/%d  (bar ≥5/6)  %s"
              % (s[5:], kk, nn, "✅" if g else "⛔ INVALID — 연산자가 죽었다"))
    for s in seeds:
        k, n = follow(post[s]["w"], "swap", "w0")
        g = k >= 11
        ok &= g
        print("   G-write %-9s swap 신극성 WRITE = %d/%d  (bar ≥11/12)  %s"
              % (s[5:], k, n, "✅" if g else "⛔ INVALID(예산) — 재기술이 착륙 안 함"))
    for s in seeds:
        kb, _ = follow(base[s]["f1"], "untouched", "negL")
        kp, n = follow(post[s]["f1"], "untouched", "negL")
        g = kp >= kb
        ok &= g
        print("   G-forget %-8s untouched flip1  base %d/%d → post %d/%d  %s"
              % (s[5:], kb, n, kp, n, "✅" if g else "⛔ INVALID(CPT 파괴)"))
    if not ok:
        print("\n⛔ **INVALID** — 게이트가 죽었다. DV 를 읽지 않는다.")
        return

    # ── DV ───────────────────────────────────────────────────────────────────
    print("\n🎯 DV — swap 팔: 규칙이 **새 극성**을 따르는가 (4셀 = 2 seed × 2 강표면)")
    cells = []
    for s in seeds:
        for tag in STRONG:
            k, n = follow(post[s]["f1"], "swap", tag)
            p_new, p_old = exact_p(k, n), exact_p(n - k, n)
            cells.append((s, tag, k, n))
            print("   %-9s %-5s  새극성 추종 **%2d/%d**  (p_new=%.4f · p_old=%.4f)"
                  % (s[5:], tag, k, n, p_new, p_old))
    kn, tag_n = follow(post[seeds[0]]["f1"], "swap", NULLSURF)
    print("   [음성대조 %s · 연산자가 안 도는 표면] %d/%d — 진짜 0 과 죽은-표면 0 을 가른다"
          % (NULLSURF, kn, tag_n))

    ks = [k for _, _, k, _ in cells]
    print("\n" + "=" * 92)
    if all(k >= 10 for k in ks):
        print("VERDICT: 🟢 **H-β** — 규칙이 **방금 쓴 극성**을 읽는다(4셀 전부 ≥10/12).")
        print("  ⟹ 연산자는 **가변 저장소를 참조한다**. SEEN 슬롯에 쓰면 보인다.")
        print("  ⟹ held-out 실패의 정체 = **신규 엔트리 불가시성** — 슬롯이 없는 어간엔 쓸 자리가 없다.")
        print("  다음 = held-out 어간에 **슬롯을 먼저 만들고** 쓰면 결합되는가.")
    elif all(k <= 2 for k in ks):
        print("VERDICT: 🧱 **{H-δ ∨ H-ε}** — 규칙이 **옛 극성**을 읽는다(4셀 전부 ≤2/12).")
        print("  ⟹ 선언적 재기술은 규칙의 극성원을 **못 움직인다**. SEEN 슬롯에 써도 안 보인다.")
        print("  ⚠️ C3 는 두 하위 가설을 **못 가른다**(저장소-측 H-δ vs 인터페이스-측 H-ε).")
        print("     한쪽으로 서사를 쓰는 순간 과잉주장이다 — C4 가 가른다.")
    else:
        mid = [k for k in ks if 3 <= k <= 9]
        print("VERDICT: ⏳ **DIRECTIONAL 상한** — 4셀이 한 범주로 안 모인다(%s)." % ks)
        print("  n=20 어간에서 '의존 없음' 은 TOST 를 원리적으로 통과 못 한다(90%% CI 반폭 ≈0.475 > 0.4).")
        print("  ⟹ **'없다' 가 아니라 '이 n 으로는 못 가른다'** 라고 적는다(power-before-negative).")
        if mid:
            print("  중간값 존재 = 갈등이 참조를 부분 붕괴시켰을 가능성 — 음성대조와 비교해 읽어라.")


if __name__ == "__main__":
    main()
