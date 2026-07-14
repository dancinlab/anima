"""Pre-freeze bar audit — run this on EVERY pre-registration BEFORE the freeze commit.

H_9311 died on its own gate, and not because the experiment was wrong: the window it was
guarding turned out to be measured-innocent. It died because two of its three bars were numbers
transplanted from a different sample. This file is the check that would have caught both, and it
costs nothing — it reads the pre-registration and the manifests, never the model.

Two rules, both from the H_9311 post-mortem (convergence prereg-md-2, Fable adjudication):

  RULE 1 — A BAR IS DERIVED, NEVER TRANSPLANTED.
      Every count bar must state, up front, the probability that a TRUE-NORMAL instrument fails
      it. H_9311's liveness bar (>=0.90 on n=60, against a real baseline of ~0.89) fails a
      perfectly healthy instrument 49.5-59.1% of the time. A bar a healthy instrument fails on a
      coin flip is not a gate; it is a coin. Any bar with false-fail > 5% is rejected here.

  RULE 2 — EVERY CLAUSE OF A GATE MUST BE A FUNCTION OF THE THING THE GATE NAMES.
      H_9311's G-A named itself "window validity" and then included a clause (SEEN flip1 >= 0.90)
      that is INVARIANT to the window — 0.883 at win=64, 0.883 at win=128. A quantity that does
      not move with the window cannot adjudicate the window. This was knowable from the clause's
      definition alone, before a single forward pass.

Neither check needs the model. Both are text-and-arithmetic. Run them at freeze time.
"""

import math
from math import comb


def false_fail(bar_k, n, true_p):
    """P(a true-normal instrument, whose real rate is true_p, scores below bar_k out of n)."""
    return sum(comb(n, i) * true_p ** i * (1 - true_p) ** (n - i) for i in range(0, bar_k))


def audit_bar(name, bar_frac, n, true_p, kind="validity"):
    """Two kinds of bar, two different budgets — conflating them is itself a bar defect.

    validity/liveness gate — its job is to certify the instrument is healthy. Failing a HEALTHY
        instrument is the whole sin, so its false-fail budget is tight (<=5%).
    decision bar — its job is to adjudicate the hypothesis. Missing the pre-registered
        alternative at rate 1-power is the DESIGN, not a defect; at power 0.9 a 10% miss is
        exactly right. Judging it by the validity budget would reject a correctly-powered bar.

    (This distinction is not decoration: the first version of this audit applied the 5% budget to
    the G-D decision bar and "rejected" it at 8.6% — a bar that was correctly powered by
    construction. An audit that fails correct work is the same class of defect it exists to catch.)
    """
    k = int(math.ceil(bar_frac * n))
    ff = false_fail(k, n, true_p)
    budget = 0.05 if kind == "validity" else 0.10
    ok = ff <= budget + 1e-9
    label = ("정상 계기 낙제확률" if kind == "validity" else "대립가설 놓칠 확률(=1−검정력)")
    verdict = ("✅" if ok else
               ("⛔ REJECT — 게이트가 아니라 동전" if kind == "validity"
                else "⛔ REJECT — 검정력 부족"))
    print("  %-34s bar=%.3f (%d/%d) · 참값 p=%.3f ⟹ %s %6.2f%% (예산 %d%%)  %s"
          % (name, bar_frac, k, n, true_p, label, 100 * ff, 100 * budget, verdict))
    return ok


def main():
    print("=" * 88)
    print("BAR AUDIT — 동결 커밋 전 필수 (모델 미접촉 · 텍스트와 산수만)")
    print("=" * 88)

    print("\n[RULE 1] bar 는 유도하는 것이지 이식하는 것이 아니다")
    print("  — 각 bar 가 '참으로-정상인 계기'를 낙제시킬 확률을 사전 계산한다 (>5% = 거부)\n")

    print("  ✗ H_9311 이 실제로 걸었던 bar (사후 감사):")
    audit_bar("G-A liveness >=0.90", 0.90, 60, 0.89)   # baseline measured at ~0.883/0.900
    print("      ↑ 이 수 0.90 은 H_9308 의 다른 매니페스트(20원자 80행 · frac 0.975)에서 이식됐다.")
    print("      H_9311 의 man_seen 은 6형태 × 20원자 = 120행(flip1 60행)이고 기준선은 ~0.89 다.")

    print("\n  ✓ H_9312 가 걸어야 할 bar (G-D 판정 bar 에서 유도):")
    print("      원리 — 계기가 모델이 통달한 원자(SEEN)에서조차 G-D 의 판정 bar 에 못 닿으면")
    print("      nonce/held-out 에서는 결코 못 닿는다 ⟹ liveness 바닥 = G-D bar 그 자체 = 140/240.")
    print("      (관측 baseline 과 무관하게 유도 — '관측값 − ε' 이 아니다)")
    audit_bar("G-A' liveness >=140/240", 140 / 240, 60, 0.883)
    audit_bar("G-D CONSUME >=140/240", 140 / 240, 240, 0.624, kind="decision")

    print("\n[RULE 2] 게이트의 각 절은 그 게이트가 명명한 조작의 함수여야 한다")
    print("  — 창에 불변인 양은 창을 판정할 수 없다. 절의 정의만 읽어도 발사 전에 잡힌다.\n")
    clauses = [
        ("G-A ① 부호일치(win64 vs win128)", True,
         "창의 함수 ✅ — 두 창의 출력을 직접 비교한다"),
        ("G-A ② |Δacc| (win64 vs win128)", True,
         "창의 함수 ✅ — 두 창의 차분이다"),
        ("G-A ③ SEEN flip1 @win128 >= 0.90", False,
         "창에 불변 ⛔ — 0.883@64 == 0.883@128. 이건 liveness 이지 창 유효성이 아니다 "
         "⟹ 독립 게이트로 이주(삭제가 아니라)"),
    ]
    for name, ok, why in clauses:
        print("  %-36s %s" % (name, why))

    print("\n=> H_9311 의 G-A 는 두 규칙을 모두 위반했다. 두 검사 다 $0 · 발사 전 수행 가능했다.")
    print("   이 파일을 모든 사전등록의 동결 커밋 전 체크리스트에 넣는다.")


if __name__ == "__main__":
    main()
