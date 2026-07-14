"""H_9322 DECON-W RE-FIRE — read the frozen DV at the budget H_9324 earned. Bars UNCHANGED.

H_9322 died on its own WRITE gate: it never got the polarity into the weights, so its flip1
number was not a negative about COMPOSITION — it was a negative about a fine-tune that never
landed. H_9324 then found the budget (6000 steps @ 2e-4: WRITE 0.954, FORGET 1.000).

So now, and only now, flip1 means what it was designed to mean.

flip1 = the negated forms (지 않다 / 안 / 전혀 …지 않다). They appear ZERO times in the CPT
corpus. The model was taught `stem -> polarity` on un-negated forms only. A flip1 win therefore
cannot come from repeating what it was shown; the gold answer is the OPPOSITE of the fact it was
just taught. It can only come from composing  fact (x) negation  — and the negation operator is
the one thing pretraining already supplied (480 of 960 arrow lines were already negated forms).

That is the whole experiment: we supply the OPERAND, pretraining supplied the OPERATOR, and we
ask whether the substrate multiplies them.

PREDICTION FROZEN BEFORE THE LIE ARM LANDED (this is the whole point of pre-registering):

  Treatment arm, measured: flip0 = 0.8736, flip1 = 0.3908 (n=87 each).
  flip1 is not merely at chance — it is BELOW it, and the errors are signed: on 53 of 87 rows
  (60.9%) the model bet on the polarity we just planted, i.e. it ECHOED the fact and never applied
  the negation. So composition is already refuted on the treatment arm alone: the fact IS in the
  weights (WRITE 0.954) and the negated form still does not consume it.

  What the LIE arm decides is WHICH failure this is. The manifest's gold is built on the atom's
  TRUE polarity P; the LIE corpus plants L = 1-P. So:

    H-ECHO  (the fact is retrieved, the operator is never applied)
        LIE flip0 ~ 0.13  and  LIE flip1 ~ 0.61   — a MIRROR of the treatment arm.
        Inverting the planted fact inverts both columns, which PROVES the negated surface is
        reading our planted key; it just multiplies it by 1 instead of by (-1).

    H-BLIND (the negated surface never reads the planted key at all)
        LIE flip1 ~ 0.39  — UNCHANGED from treatment. A false fact scores like a true one, which
        is exactly the H_9312 G-C signature, and then flip1 measures nothing about our fact.

  These two make opposite predictions about the SIGN of the LIE arm, so the arm is decisive and
  cannot be read either way after the fact. Write it down now.
"""
import json, os, sys

REMOTE = os.path.expanduser("~/anima-weights/h9314")
FLIP1 = {"negL", "negS", "negE"}
CHANCE = 0.50

def read(p):
    rows = json.load(open(p))["splits"]["heldout"]["rows"]
    f0 = [r for r in rows if r["b"] not in FLIP1]
    f1 = [r for r in rows if r["b"] in FLIP1]
    acc = lambda s: sum(1 for r in s if r["margin"] > 0) / max(1, len(s))
    return acc(f0), len(f0), acc(f1), len(f1)

def main():
    print("=" * 86)
    print("H_9322 DECON-W 재발사 — H_9324 가 벌어낸 예산(6000@2e-4) 위에서 · bar 불변")
    print("  flip1 = 부정형(지 않다/안 /전혀) · CPT 코퍼스 등장 **0회** · gold 는 방금 가르친 사실의 **반대**")
    print("  ⟹ 앵무새질은 여기서 **진다**. 이기려면 fact ⊗ negation 을 **곱해야** 한다.")
    print("=" * 86)
    print()
    arms = [("main_s7", "처치 (참 극성 · seed 7)"),
            ("s11",     "처치 재현 (참 극성 · seed 11 · #3462)"),
            ("lie_s7",  "LIE 양성대조 (극성 29/29 **반전**)")]
    got = {}
    for tag, label in arms:
        p = os.path.join(REMOTE, "refire_%s.json" % tag)
        if not os.path.exists(p):
            print("  %-34s  … 미회수" % label)
            continue
        a0, n0, a1, n1 = read(p)
        got[tag] = (a0, a1)
        print("  %-34s  flip0=%.4f(n=%d)   flip1=%.4f(n=%d)" % (label, a0, n0, a1, n1))
    print()

    if "main_s7" not in got:
        print("[PENDING] 처치 팔 미회수 — 판독 보류")
        return
    a0, a1 = got["main_s7"]

    # The LIE arm is what makes flip1 readable at all. Without it, a flip1 win is indistinguishable
    # from a model that simply likes the majority label on negated surfaces (H_9312's lesson: a
    # control the system can pass WITHOUT the mechanism is a ceiling measurement, not a control).
    if "lie_s7" not in got:
        print("⏳ flip1=%.4f 이나 **LIE 통제 미회수 ⟹ 판독하지 않는다**." % a1)
        print("   거짓 사실을 심어도 flip1 이 같은 값이면 그건 합성이 아니라 표면 편향이다 —")
        print("   H_9312 의 G-B 가 정확히 그렇게 가짜 양성을 냈고, 그걸 잡은 것이 LIE 팔이었다.")
        return

    l0, l1 = got["lie_s7"]
    d = a1 - l1
    print("=" * 86)
    print("  처치 flip1 %.4f  vs  LIE flip1 %.4f   Δ = %+.4f" % (a1, l1, d))
    print()
    if a1 > CHANCE and l1 < CHANCE and d > 0.15:
        print("VERDICT: 🟢 합성 — 심은 사실이 **보이지 않는 부정형으로 전이**되고, 사실을 뒤집으면")
        print("  flip1 이 **우연 아래로 붕괴**한다. 연산자는 사전학습이 공급했고 피연산자는 우리가")
        print("  넣었으며, 기질이 **둘을 곱했다**. G1 벽의 가중치 경로가 열렸다.")
    elif a1 <= CHANCE + 0.05 and l1 <= CHANCE + 0.05:
        print("VERDICT: 🧱 NO-COMPOSE — **벌어낸 음성**. 극성은 가중치에 확실히 들어갔는데(WRITE 0.954)")
        print("  보이지 않는 부정형으로는 **전혀 전이되지 않는다**. 이건 H_9322 때와 달리 '심는 데")
        print("  실패했다'로 설명할 수 없다 — 심었고, 그런데도 합성이 없다. 4층 conv byte-LM 은")
        print("  사실을 **저장**하지만 학습된 연산자로 그것을 **소비**하지 못한다.")
    elif abs(d) <= 0.15:
        print("VERDICT: ⛔ INVALID — 거짓 사실이 참 사실과 **같은 점수**를 낸다(Δ=%+.4f)." % d)
        print("  ⟹ flip1 이 무엇을 재든 **우리가 심은 사실을 읽고 있지 않다**(H_9312 G-C 와 같은 진단).")
        print("  이 값으로 합성을 주장할 수도, 부정할 수도 없다.")
    elif l1 > CHANCE and l0 < CHANCE:
        print("VERDICT: 🧱 ECHO — **벌어낸 음성 · 저장은 되나 연산자가 적용되지 않는다**.")
        print("  거짓 사실을 심으니 **두 열이 통째로 뒤집힌다**(LIE flip0=%.4f · flip1=%.4f) ⟹" % (l0, l1))
        print("  부정형 표면은 우리가 심은 키를 **분명히 읽고 있다**. 다만 그것을 (-1) 이 아니라")
        print("  **(+1) 로 곱한다** — 사실을 꺼내 그대로 되뇌고 부정 연산자를 적용하지 않는다.")
        print("  H_9322 의 '심는 데 실패했다'로는 설명 불가하다: **심었고(WRITE 0.954), 그런데도**")
        print("  **합성이 없다.** 이 4층 conv byte-LM 은 사실을 **저장**하지만 학습된 연산자로")
        print("  **소비**하지 못한다 — in-context 경로(H_9312)에 이어 **가중치 경로도 같은 진단**이다.")
    else:
        print("VERDICT: ⚠️ 혼합 — 처치 %.4f · LIE flip0=%.4f flip1=%.4f · Δ=%+.4f." % (a1, l0, l1, d))
        print("  동결된 두 분기(H-ECHO 거울 · H-BLIND 무변화) 어디에도 안 맞는다 ⟹ seed 를 늘려")
        print("  잡음을 배제한 뒤에만 판독한다(#3462).")

if __name__ == "__main__":
    main()
