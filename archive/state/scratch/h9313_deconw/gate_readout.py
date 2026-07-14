"""H_9313 DECON-W — frozen readout. Bars live in PREREG.md; this file only ENFORCES them.

The question, after H_9312 closed context-injection: if the polarity is written into the WEIGHTS
rather than handed over in the prompt, does the already-learned negation operator consume it?

Three layers, and the first one is what makes the third one interpretable:

  WRITE    each arm's held-out flip0, scored against THE LABEL THAT ARM WROTE.  >= 0.95.
           This is not a formality. It proves the fine-tune actually landed the value. Without it,
           a flat flip1 could just mean "training did nothing" — with it, a flat flip1 means the
           value IS there and the operator does not read it. That distinction is the whole verdict.

  COMPOSE  Δ = ground flip1 − lie flip1, on the TRUE label, row-paired.  >= 0.30 and McNemar p<0.01.
           The primary. Signed, because ground_lie inverts every polarity: a model that consumes
           and composes must answer ¬(¬p) = p on every flip1 row of the lie arm — i.e. WRONG on
           every one — so its accuracy there collapses far BELOW chance while the ground arm rises.
           Both arms landing on the same number is exactly the shape of a mechanism that isn't there.

  SIGN     cluster-level confirmation of that signed prediction: ground C >= 20/29, lie C <= 9/29.

flip1 forms (지 않다 / 안 / 전혀) appear ZERO times in either training corpus — verified before the
freeze. So flip1 measures COMPOSITION, never memorisation, and no amount of fine-tuning can tune it
to green.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = os.path.expanduser("~/anima-weights/c34")
SEEDS = ("main_s7", "main_s11")
ARMS = ("ground", "ground_lie")

BAR_WRITE = 0.95
BAR_DELTA = 0.30
BAR_MCNEMAR = 0.01
BAR_SIGN_GROUND = 20      # of 29 clusters
BAR_SIGN_LIE = 9          # of 29 clusters
BASELINE_FLIP1 = 0.5057   # no-CPT ckpt (H_9308)


def rows(arm, seed):
    p = os.path.join(HERE, "ev_%s_%s.json" % (arm, seed))
    return json.load(open(p))["splits"]["heldout"]["rows"] if os.path.exists(p) else None


def manifest():
    return json.load(open(os.path.join(KEEP, "n2_eval_manifest.json")))["heldout"]


def atoms():
    a = json.load(open(os.path.join(KEEP, "gt_atoms.json")))["atoms"]
    return {x["stem"]: int(x["pol"]) for x in a if x["split"] == "heldout"}


def acc_true(rs, man, flip):
    """frac(margin > 0) — margin is scored against the TRUE gold in the frozen manifest."""
    s = [r for r, m in zip(rs, man) if m["flip"] == flip]
    return sum(1 for r in s if r["margin"] > 0) / max(1, len(s)), len(s)


def acc_written(rs, man, arm, pol):
    """flip0 accuracy against the label THIS ARM WROTE (inverted for the lie arm).

    On a flip0 row the manifest's gold IS the atom's true polarity, so margin>0 means "bet on the
    true label". The lie arm wrote the opposite, so a successful write shows up there as margin<0.
    """
    ok = n = 0
    for r, m in zip(rs, man):
        if m["flip"] != 0:
            continue
        wrote_true = (arm == "ground")
        ok += int((r["margin"] > 0) == wrote_true)
        n += 1
    return ok / max(1, n), n


def clusters_true(rs, man):
    by = {}
    for r, m in zip(rs, man):
        if m["flip"] == 1:
            by.setdefault(m["p"], []).append(1 if r["margin"] > 0 else 0)
    return sum(1 for v in by.values() if sum(v) * 2 > len(v)), len(by)


def mcnemar(a_rows, b_rows, man):
    """Row-paired flip1: b(ground right, lie wrong) vs c(ground wrong, lie right)."""
    b = c = 0
    for ra, rb, m in zip(a_rows, b_rows, man):
        if m["flip"] != 1:
            continue
        ga, gl = ra["margin"] > 0, rb["margin"] > 0
        b += int(ga and not gl)
        c += int(gl and not ga)
    if b + c == 0:
        return 0.0, b, c, 1.0
    chi = (abs(b - c) - 1) ** 2 / (b + c)
    p = math.erfc(math.sqrt(chi / 2))
    return chi, b, c, p


def main():
    man = manifest()
    print("=" * 94)
    print("H_9313 DECON-W — 극성을 **가중치에** 쓰고, 코퍼스에 없던 부정형으로 합성을 시험한다")
    print("  ground: 쓴 극성 = p   ·   ground_lie: 쓴 극성 = ¬p (29/29 전부 반전)")
    print("  flip1(지 않다·안·전혀)은 두 코퍼스 어디에도 **0회** 등장 ⟹ 암기가 아니라 합성의 시험")
    print("=" * 94)

    out = {"hypothesis": "H_9313"}
    have = {}
    for s in SEEDS:
        for a in ARMS:
            have[(a, s)] = rows(a, s)
    if not all(have.values()):
        miss = [f"{a}/{s}" for (a, s), v in have.items() if not v]
        print("\n[PENDING] 미회수: %s" % ", ".join(miss))
        return

    print("\n[WRITE] 쓰기가 안착했는가 — 각 arm 의 flip0 을 **그 arm 이 쓴 라벨** 기준 (bar %.2f)"
          % BAR_WRITE)
    print("        여기서 통과해야 flip1 의 침묵이 '학습이 안 먹음'이 아니라 '연산자가 안 읽음'이 된다")
    ok_write = True
    pol = atoms()
    for s in SEEDS:
        for a in ARMS:
            w, n = acc_written(have[(a, s)], man, a, pol)
            p = w >= BAR_WRITE
            ok_write &= p
            print("  %-10s %-9s flip0(쓴 라벨 기준) = %.4f (n=%d)  %s"
                  % (a, s, w, n, "PASS" if p else "FAIL"))
    print("  => WRITE %s" % ("PASS — 값이 실제로 가중치에 들어갔다"
                             if ok_write else
                             "FAIL — ⛔ INVALID-WRITE (학습이 값을 못 심음 · 합성 음성이 아니다)"))

    print("\n[COMPOSE] primary — Δ = ground flip1 − lie flip1 (참 라벨 · 행-paired)")
    print("          bar Δ ≥ %.2f ∧ McNemar p<%.2f · 양 seed AND · 무-CPT 기준선 flip1 = %.4f"
          % (BAR_DELTA, BAR_MCNEMAR, BASELINE_FLIP1))
    ok_comp = True
    res = {}
    for s in SEEDS:
        g, _ = acc_true(have[("ground", s)], man, 1)
        li, n = acc_true(have[("ground_lie", s)], man, 1)
        chi, b, c, p = mcnemar(have[("ground", s)], have[("ground_lie", s)], man)
        d = g - li
        okp = d >= BAR_DELTA and p < BAR_MCNEMAR
        ok_comp &= okp
        res[s] = {"ground_flip1": g, "lie_flip1": li, "delta": d, "mcnemar_p": p, "b": b, "c": c}
        print("  %-9s ground=%.4f · lie=%.4f · **Δ=%+.4f** · McNemar b=%d c=%d p=%.4g (n=%d)  %s"
              % (s, g, li, d, b, c, p, n, "PASS" if okp else "FAIL"))
    print("  => COMPOSE %s" % ("PASS" if ok_comp else "FAIL"))

    print("\n[SIGN] secondary — 부호 확인 (원자클러스터 29 · 3-형태 다수결)")
    print("       소비·합성하면 ground ≥%d/29 **그리고** lie ≤%d/29 (거짓 극성을 따라가야 한다)"
          % (BAR_SIGN_GROUND, BAR_SIGN_LIE))
    ok_sign = True
    for s in SEEDS:
        cg, n = clusters_true(have[("ground", s)], man)
        cl, _ = clusters_true(have[("ground_lie", s)], man)
        p = cg >= BAR_SIGN_GROUND and cl <= BAR_SIGN_LIE
        ok_sign &= p
        res[s].update({"c_ground": cg, "c_lie": cl})
        print("  %-9s ground C=%d/%d · lie C=%d/%d  %s"
              % (s, cg, n, cl, n, "PASS" if p else "FAIL"))
    print("  => SIGN %s" % ("PASS" if ok_sign else "FAIL"))

    print("\n" + "=" * 94)
    if not ok_write:
        v = ("⛔ INVALID-WRITE — 미세 CPT 가 극성을 가중치에 심지 못했다. flip1 이 어떻든 **합성에 "
             "대한 음성이 아니다**(학습이 안 먹은 것). steps/lr 조정 후 1회 재시도.")
    elif ok_comp and ok_sign:
        v = ("🟢-dir WEIGHT-GROUNDED COMPOSITION — 가중치에 쓴 극성을 **이미 학습된 부정 연산자가 "
             "소비·합성한다**. 거짓 극성을 심으면 답이 거짓을 따라간다(부호 확인) ⟹ 우연이 아니다. "
             "⟹ 이 지점의 G1 벽은 **없는 입력**이었지 조합능력 천장이 아니다. NEXT = 배선"
             "(a_verified_must_wire).")
    elif ok_comp and not ok_sign:
        v = ("⚠️ DIRECTIONAL — Δ 는 섰으나 부호 확인(SIGN)이 안 선다. 효과가 있으나 예측한 모양이 "
             "아니다 ⟹ cement 금지, 기전 재확인 필요.")
    else:
        v = ("🧱 WRITTEN-BUT-NOT-COMPOSED — **교란 없는 벌어낸 음성**. WRITE 가 PASS 이므로 값은 "
             "**분명히 가중치에 있다**(flip0 이 쓴 라벨을 따라간다). 그런데 flip1 은 두 arm 이 같은 "
             "수를 낸다 — 거짓 극성을 심어도 답이 안 움직인다 ⟹ **연산자가 그 값을 읽지 않는다**. "
             "read-side 종결의 '복원되나 causally 소비불가'와 동형이고, H_9312(컨텍스트 채널 폐쇄)와 "
             "합쳐 **A 채널 완전 폐쇄**. 남은 것은 연산자의 피연산자 포트 자체를 바꾸는 것뿐.")
    print("VERDICT:", v)
    out.update({"write_ok": ok_write, "compose_ok": ok_comp, "sign_ok": ok_sign,
                "per_seed": res, "verdict": v})
    json.dump(out, open(os.path.join(HERE, "DECONW.json"), "w"), ensure_ascii=False, indent=1)
    print("→ DECONW.json")


if __name__ == "__main__":
    main()
