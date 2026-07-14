"""H_9311 DECON-2 (DEMO-PORT) — build every arm's manifest and store.

The fact is handed over as a one-shot demonstration in the model's OWN training template:

    이 영화 <demo_stem>고 => <긍정|부정>.\n 이 영화 <target_surf> => ___

Why this and not H_9309's `"긍정. "` prefix: that prefix perturbed the margin by 59-74% while
carrying ZERO information (both flip classes pushed the WRONG way). We were speaking a language
the byte-LM was never taught. The demo format is the one language it demonstrably reads
(SEEN D-acc 0.950), and prefreeze_audit.py measured — off disk, not by reasoning — that the
training stream packed ~24 of these instances into every 1024B window separated by a single
b"\n". So `instance \n instance` is not a hopeful guess about the distribution; it IS the
distribution.

ARMS (signal is a difference against >=2 controls, never a raw value):
  NOSTORE   no demo at all                       — the floor
  MATCHED   the target atom's own true polarity  — the treatment
  MISMATCH  ANOTHER atom's demo                  — the control that kills the anti-parrot

MISMATCH is the arm that earns the verdict. A byte-LM that merely SUPPRESSES a just-seen string
would ace MATCHED flip1 without composing anything (gold there is always the demo label's
opposite). Under MISMATCH the demo label is independent of the target's gold, so that alternation
bias cannot help — and the MATCHED − MISMATCH contrast subtracts it out on both sides.

Note the arms need no new engine code: MISMATCH is just a store whose entry for atom X carries
ANOTHER atom's (key, pol). The renderer reads the fact it is given.

DV LAYERS (flip0 is demoted — the demo hands it the answer outright):
  READ     MATCHED flip0 on int1/int2 only   — is the demo read at all (copy suffices to pass)
  CONSUME  MATCHED flip1 atom-cluster majority — does the handed value enter the operator
  BIND     MATCHED flip1 − MISMATCH flip1     — is the value bound to the ATOM, not just present
The bare-flip0 rows are pure string overlap with the demo and are excluded from every statistic.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = os.path.expanduser("~/anima-weights/c34")

TMPL = "이 영화 {surf} => "
FORMS = [
    ("bare", "{s}고", 0),
    ("int1", "정말 {s}고", 0),
    ("int2", "너무 {s}다", 0),
    ("negL", "{s}지 않다", 1),
    ("negS", "안 {s}고", 1),
    ("negE", "전혀 {s}지 않다", 1),
]

# 240 nonce stems.  Nonces need no corpus (we DECLARE their truth and hand it over only via the
# demo), so unlike the 29 natural held-out atoms they can be minted freely — and that is what
# buys the statistical power H_9309 lacked: at 240 clusters a null result clears TOST at
# Δ_eq=0.10 (N_REQ=214), so a negative here is CEMENTABLE rather than merely "supporting".
# Built from syllable parts that do not spell Korean words; we do not take that on faith — the
# NOSTORE arm measures it directly (a stem carrying a real prior would read above chance there).
_A = list("뽀츄끄삠웨쟈펄힝꼬댕쁘톄샤뭉흐뾰칵튤붐쎄얄쥐훠낍먀겅빡돌윰")
_B = list("길람뷔돌긋쿠뭇졸뷁류칸묵긜퀄뎁찰쥬겅켸퐁믭낑딱뽀둥츨쉬캬챠")
NONCE = [_A[i % len(_A)] + _B[(i * 7 + i // len(_B)) % len(_B)] for i in range(400)]
NONCE = list(dict.fromkeys(NONCE))[:240]
NONCE_POL = [i % 2 for i in range(240)]


def rows_for(pairs):
    out = []
    for stem, pol in pairs:
        for form, pat, flip in FORMS:
            gp = pol ^ flip
            gw, cw = ("긍정", "부정") if gp == 1 else ("부정", "긍정")
            surf = pat.format(s=stem)
            out.append({"p": stem, "form": form, "a": stem, "b": form, "pol": pol,
                        "flip": flip, "xor": gp, "surf": surf, "seed": TMPL.format(surf=surf),
                        "gold": gw + ".", "counterfactual": cw + ".", "gold_word": gw})
    return out


def dump(name, obj):
    json.dump(obj, open(os.path.join(HERE, name), "w"), ensure_ascii=False, indent=1)


def main():
    assert len(NONCE) == 240, len(NONCE)
    atoms = json.load(open(os.path.join(KEEP, "gt_atoms.json")))["atoms"]
    seen = [(a["stem"], a["pol"]) for a in atoms if a["split"] == "train"]
    held = [(a["stem"], a["pol"]) for a in atoms if a["split"] == "heldout"]

    specs = [
        ("nonce", list(zip(NONCE, NONCE_POL))),      # G-D  launch gate + negative cement
        ("seen", seen),                              # G-B  is the 2-concatenation format read
        ("heldout", held),                           # G-E  the real question (fired last)
    ]
    for tag, pairs in specs:
        rows = rows_for(pairs)
        dump("man_%s.json" % tag,
             {"format": "nbind-eval-v1", "task": "H_9311 DECON-2 DEMO-PORT (%s)" % tag,
              "gen": 8, "win": 128, "heldout": rows, "seen": []})
        # MATCHED: the atom's own fact.  MISMATCH: the NEXT atom's fact (cyclic shift) — the demo
        # label is then independent of the target's gold, which is exactly what an alternation
        # bias cannot exploit.
        dump("store_%s_matched.json" % tag,
             {s: {"key": s, "pol": p} for s, p in pairs})
        dump("store_%s_mismatch.json" % tag,
             {pairs[i][0]: {"key": pairs[(i + 1) % len(pairs)][0],
                            "pol": pairs[(i + 1) % len(pairs)][1]}
              for i in range(len(pairs))})

    # ---- byte audit, before any model touches this (a_korean_byte_budget: the window is a BYTE
    # budget and Korean is 3B/char).  A DROPPED trial makes the run INVALID-INSTRUMENT — and for
    # DEMO there is deliberately NO fallback format, because downgrading some trials to a
    # label-only prefix would silently mix in the very format H_9309 proved carries no signal.
    print("=" * 82)
    print("H_9311 DECON-2 (DEMO-PORT) — arms built")
    print("=" * 82)
    for tag, pairs in specs:
        rows = rows_for(pairs)
        st = {s: {"key": s, "pol": p} for s, p in pairs}
        worst, over = 999, 0
        for r in rows:
            budget = 128 - len(r["seed"].encode()) - max(len(r["gold"].encode()),
                                                         len(r["counterfactual"].encode()))
            f = st[r["p"]]
            pw = "긍정" if f["pol"] == 1 else "부정"
            demo = "이 영화 " + f["key"] + "고 => " + pw + ".\n"
            worst = min(worst, budget - len(demo.encode()))
            over += int(len(demo.encode()) > budget)
        print("  %-8s %d atoms · %3d rows · win=128 여유 최소 %2dB · DEMO 초과 %d/%d %s"
              % (tag, len(pairs), len(rows), worst, over, len(rows),
                 "✅" if over == 0 else "❌ INVALID-INSTRUMENT"))
    print("\n  arms: NOSTORE(바닥) · MATCHED(처치) · MISMATCH(역-앵무새 통제)")
    print("  DV: READ=MATCHED flip0(int만) · CONSUME=MATCHED flip1 클러스터 · "
          "BIND=MATCHED−MISMATCH")
    print("  bare-flip0 행은 시연과 문자열이 겹치는 순수복사행 ⟹ 전 통계에서 제외")


if __name__ == "__main__":
    main()
