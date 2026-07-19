"""H_9327 — read the DV on a model whose operator is demonstrably ALIVE. Bars frozen before data.

Everything below was written while the run was still at step 900. That is the point: this session
has already caught me twice reading a number the wrong way after seeing it (the pooled 60.9% "echo",
and the whole flip1 story measured on a model whose operator we had destroyed). So the rules go in
first.

The three reads, IN ORDER. Do not skip ahead — read 3 is unreadable without 1.

  1. POSITIVE CONTROL — SEEN flip1, the stems whose negated form pretraining demonstrated 480 times.
       base was 0.8833; `ground` CPT crushed it to 0.4333. ground_keep replays those lines, so it
       must come back. Bar: >= 0.75 (base 0.8833 minus a generous margin — a replay is not expected
       to be free, but an operator at 0.43 is dead and one at 0.75+ is working).
       BELOW BAR -> ⛔ INVALID-OPERATOR. Not FAIL. We have not yet earned the right to ask about
       composition, and any held-out number is meaningless. This is the gate H_9303/H_9307 died for.

  2. WRITE — held-out flip0. H_9324's winning cell got 0.954 at this budget on the `ground` corpus.
       The replay adds 2400 lines of competing gradient; if it pushes the fact back out, we have
       traded one failure for another. Bar: >= 0.90 (H_9324's 0.95 minus room for the replay's cost).
       BELOW BAR -> ⛔ INVALID-WRITE. The fact is not in the weights, so flip1 tests nothing.

  3. THE DV — held-out flip1. Composition: the negated form appears ZERO times for these 29 stems,
       so the gold answer is the OPPOSITE of the fact we just wrote. Parroting LOSES here. Only
       fact (x) negation wins. Read the POSITIVE-ATOM column, never the headline (a majority-label
       collapse manufactures a headline — convergence corpus-py-1, and it fooled me earlier today).

       PASS  = flip1 > chance AND the positive-atom stratum rises off its floor (it was 0.000-0.022
               on every `ground` arm). Both strata, or it is a label artifact.
       FAIL  = flip1 at chance / below, with the operator ALIVE (read 1 passed) and the fact WRITTEN
               (read 2 passed). That is an EARNED negative and the first honest one this lane has
               produced: the operator works on stems it learned in pretraining and does not bind to
               a fact we wrote by fine-tuning. That would be a BINDING failure — a real finding, and
               a different wall than any we have named.
"""
import json, os

R = os.path.expanduser("~/anima-weights/h9314")
FLIP1 = {"negL", "negS", "negE"}
BAR_OPERATOR = 0.75      # base 0.8833; `ground` corpus crushed it to 0.4333
BAR_WRITE = 0.90         # H_9324 got 0.954 on `ground` at this same budget
BASE_SEEN_FLIP1 = 0.8833
GROUND_SEEN_FLIP1 = 0.4333


def strata(path):
    rows = json.load(open(path))["splits"]["heldout"]["rows"]
    out = {}
    for f in (0, 1):
        rs = [r for r in rows if (r["b"] in FLIP1) == bool(f)]
        if not rs:
            continue
        acc = sum(1 for r in rs if r["margin"] > 0) / len(rs)
        cls = {}
        for c in sorted({r["gold_word"] for r in rs}):
            sub = [r for r in rs if r["gold_word"] == c]
            cls[c] = sum(1 for r in sub if r["margin"] > 0) / len(sub)
        out[f] = (acc, len(rs), cls)
    return out


def main():
    print("=" * 90)
    print("H_9327 — 연산자를 살려둔 채 다시 쓴다 (ground_keep · 6000@2e-4 · bar 는 데이터 전 동결)")
    print("=" * 90)

    need = {"pos": "keep_seenflip.json", "write": "keep_write.json", "dv": "keep_dv.json"}
    miss = [k for k, v in need.items() if not os.path.exists(os.path.join(R, v))]
    if miss:
        print("[PENDING] 미회수: %s" % ", ".join(miss))
        return

    # ── 1. positive control ────────────────────────────────────────────────────
    s = strata(os.path.join(R, need["pos"]))
    op = s[1][0]
    print("\n① 양성대조 — SEEN 어간 flip1 (부정 480회 시연받은 어간)")
    print("   base %.4f  ·  ground CPT 가 부순 값 %.4f  ·  bar %.2f" %
          (BASE_SEEN_FLIP1, GROUND_SEEN_FLIP1, BAR_OPERATOR))
    print("   → **%.4f** (n=%d)   flip0=%.4f   %s" %
          (op, s[1][1], s[0][0], "✅ 연산자 생존" if op >= BAR_OPERATOR else "⛔ 연산자 여전히 죽음"))
    if op < BAR_OPERATOR:
        print("\nVERDICT: ⛔ **INVALID-OPERATOR** — replay 가 연산자를 되살리지 못했다(%.4f < %.2f)."
              % (op, BAR_OPERATOR))
        print("  held-out 수치는 **읽지 않는다**. 합성을 물을 자격을 아직 얻지 못했다.")
        print("  다음 = replay 를 늘리거나(reps), 파괴가 lr/step 의 함수인지 먼저 분리한다.")
        return

    # ── 2. write ───────────────────────────────────────────────────────────────
    w = strata(os.path.join(R, need["write"]))[0]
    print("\n② WRITE — held-out flip0 (사실이 가중치에 들어갔나)")
    print("   H_9324 가 같은 예산 · ground 코퍼스에서 낸 값 0.954  ·  bar %.2f" % BAR_WRITE)
    print("   → **%.4f** (n=%d)   %s" %
          (w[0], w[1], "✅" if w[0] >= BAR_WRITE else "⛔ replay 가 사실을 밀어냈다"))
    if w[0] < BAR_WRITE:
        print("\nVERDICT: ⛔ **INVALID-WRITE** — 연산자는 살렸으나 사실이 안 들어갔다(%.4f < %.2f)."
              % (w[0], BAR_WRITE))
        print("  하나를 살리고 하나를 잃었다. flip1 은 여전히 읽을 수 없다.")
        return

    # ── 3. the DV ──────────────────────────────────────────────────────────────
    d = strata(os.path.join(R, need["dv"]))
    f1, n1, cls = d[1]
    weak = min(cls.values())
    print("\n③ DV — held-out flip1 (**연산자가 살아있음이 증명된 모델 위에서 처음 재는 합성**)")
    print("   부정형은 이 29 어간에 **0회** 등장 · gold = 방금 심은 사실의 **반대** ⟹ 앵무새질은 진다")
    print("   ground 팔들의 값: flip1 0.379~0.391 · 긍정원자 0.000~0.022 (전부 INVALID 로 철회됨)")
    print("   → flip1 = **%.4f** (n=%d)   [%s]" %
          (f1, n1, "  ".join("%s=%.3f" % (k, v) for k, v in cls.items())))
    print()
    if f1 > 0.5 and weak > 0.5:
        print("VERDICT: 🟢 **합성** — 심은 사실이 **한 번도 보여준 적 없는 부정형으로 전이**된다.")
        print("  두 극성 층이 **모두** 우연 위 ⟹ 다수 라벨 인공물이 아니다(가장 약한 층 %.3f)." % weak)
        print("  연산자는 사전학습이 공급했고, 피연산자는 우리가 심었으며, **기질이 둘을 곱했다.**")
        print("  ⟹ G1 벽의 가중치 경로가 열렸다. 다음 = s11 재현 + LIE 통제(#3462 · 단일 seed 는 후보).")
    elif f1 > 0.5 and weak <= 0.5:
        print("VERDICT: ⚠️ **다수 라벨 인공물 의심** — flip1 %.4f 는 우연 위지만 약한 층이 %.3f 로 바닥."
              % (f1, weak))
        print("  헤드라인만 보면 성공처럼 읽히나 그건 라벨 비율이다(corpus-py-1). **판독 보류** —")
        print("  긍정원자가 깨어나야 학습이다. 예산/replay 비를 바꿔 재발사.")
    else:
        print("VERDICT: 🧱 **BINDING-FAIL — 벌어낸 음성 (이 lane 최초의 정직한 음성)**")
        print("  연산자는 **살아있고**(SEEN flip1 %.4f), 사실은 **가중치에 있는데**(WRITE %.4f)," % (op, w[0]))
        print("  그 둘이 **결합하지 않는다**(held-out flip1 %.4f)." % f1)
        print("  이건 지금까지의 어떤 실패와도 다르다 — '연산자가 없다'도, '사실이 안 심겼다'도,")
        print("  '우리가 연산자를 부쉈다'도 아니다. **사전학습으로 배운 극성에는 연산자가 붙고,**")
        print("  **CPT 로 쓴 극성에는 붙지 않는다.** 두 종류의 사실이 같은 연산자에 접근할 수 없다.")
        print("  ⟹ 새 벽이고, 이름이 있다: **BINDING**. 다음 = 왜 두 극성이 다른 자리에 사는가.")


if __name__ == "__main__":
    main()
