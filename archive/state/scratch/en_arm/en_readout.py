"""EN arm readout — the branch table is frozen HERE, before the base ckpt has been scored.

Everything this lane has learned says the same thing: a number you interpret after seeing it is not
evidence. So the two gates and the three verdicts are written down now.

GATE V1 — is the operator even installed?  (SEEN flip1 on the FRESH base, before any CPT)
    The Korean base carried it at 0.8833 and nobody checked before spending a campaign; H_9322 then
    read a flip1 number off a model whose operator its own CPT had destroyed. So: if the EN base
    cannot run `not X` on the very stems it was TRAINED on, the arm is INVALID — not negative,
    INVALID — and no CPT number from it can be read at all.
    The bar is DERIVED, not transplanted (bar-derived-not-transplanted): with 60 flip1 rows the
    chance sd is 0.5/sqrt(60) = 0.065, so a base that has genuinely learned the operator should sit
    many sd above 0.5. We require >= 0.75 (3.9 sd above chance) — a bar a coin clears with p ~ 5e-5.

GATE V2 — did the polarity of the SEEN stems install?  (SEEN flip0)
    Same corpus, same 960 arrow lines. If flip0 is at chance the arrow lines did not teach anything
    and V1 cannot be interpreted either. bar 0.75, same derivation.

THE DV — held-out flip1.  Does the operator generalise to a stem it never met?
    This is the whole EN arm. R2 (STEM-BOUND) says the Korean operator failed here because `지 않다`
    ATTACHES to the stem, making `(stem, operator)` one joint key. English `not` stands BESIDE the
    stem — it is the slot kind C1b measured as generalising perfectly. So:

      R2 predicts EN flip1 >> chance   -> BINDING is a fact about MORPHOLOGY, not the substrate
                                          -> the recombination lane REOPENS
      R2 refuted:  EN flip1 ~ chance   -> the wall survives a language whose negator does not attach
                                          -> that is the strongest substrate evidence anima has, and
                                             it is a POSITIVE result for the wall, not a shrug

    Either way the arm decides. The bar: chance sd on 120 held-out flip1 rows = 0.5/sqrt(120) = 0.046.
    We pre-register 0.60 (2.2 sd) as "above chance" and, for the negative, a TOST equivalence margin
    of +/-0.10 — which 120 rows can actually support (n=29 in Korean could not, H_9296).

⚠️ An EN positive is a SCREENER (DIRECTIONAL), not a cemented substrate claim: EN changes morphology
   AND the base model AND the carrier at once. Isolating which one did it is a required follow-on.
"""
import json, os, sys

R = os.path.expanduser("~/anima-weights/en_arm")
BAR_V1 = 0.75      # SEEN flip1 — operator liveness   (3.9 sd above chance at n=60)
BAR_V2 = 0.75      # SEEN flip0 — polarity installed
BAR_DV = 0.60      # held-out flip1 — above chance     (2.2 sd at n=120)
TOST = 0.10        # equivalence margin for the negative


def split(path):
    rows = json.load(open(path))["splits"]["heldout"]["rows"]
    f0 = [r for r in rows if r["flip"] == 0]
    f1 = [r for r in rows if r["flip"] == 1]
    acc = lambda s: sum(1 for r in s if r["margin"] > 0) / max(1, len(s))
    return acc(f0), len(f0), acc(f1), len(f1)


def main():
    print("=" * 84)
    print("EN 팔 — 판정 (분기표는 데이터 전에 동결됨)")
    print("=" * 84)
    for seed in (7, 11):
        ps = os.path.join(R, "en_seen_s%d.json" % seed)
        ph = os.path.join(R, "en_held_s%d.json" % seed)
        if not (os.path.exists(ps) and os.path.exists(ph)):
            print("  seed %-2d  … 미회수" % seed)
            continue
        s0, n0, s1, n1 = split(ps)
        h0, m0, h1, m1 = split(ph)
        v1 = s1 >= BAR_V1
        v2 = s0 >= BAR_V2
        print("\n  seed %d" % seed)
        print("    V2  SEEN flip0 (극성 설치)   = %.4f (n=%d)  %s bar %.2f"
              % (s0, n0, "✅" if v2 else "⛔", BAR_V2))
        print("    V1  SEEN flip1 (연산자 생존) = %.4f (n=%d)  %s bar %.2f"
              % (s1, n1, "✅" if v1 else "⛔", BAR_V1))
        if not (v1 and v2):
            print("    ⛔ INVALID — 계기가 설치되지 않았다. **DV 를 읽지 않는다.**")
            print("       (H_9322 는 정확히 이 게이트가 없어서 죽었다: 연산자가 부서진 모델에서 flip1 을 읽었다)")
            continue
        print("    ── 게이트 통과 ⟹ DV 판독 자격 획득")
        print("    DV  held-out flip0 (사실 접지) = %.4f (n=%d)" % (h0, m0))
        print("    DV  held-out flip1 (**합성**)  = %.4f (n=%d)   bar %.2f" % (h1, m1, BAR_DV))
        if h1 >= BAR_DV:
            print("    🟢 **R2 지지 — EN 에서 연산자가 미학습 어간을 넘는다**")
            print("       자유 부정어 `not` 은 어간에 붙지 않는다 ⟹ (어간, 연산자) 가 합동 키가 되지 않는다")
            print("       ⟹ **BINDING = 형태론의 사실이지 기질의 벽이 아니다** ⟹ 재조합 레인 **재개방**")
            print("       ⚠️ 단 스크리너(DIRECTIONAL): EN 은 형태론+기반모델+담체를 한꺼번에 바꿨다.")
        elif abs(h1 - 0.5) <= TOST:
            print("    🧱 **R2 반증 — 벽이 언어를 건넜다**")
            print("       부정어가 **붙지 않는** 언어에서도 연산자가 미학습 어간을 못 넘는다")
            print("       ⟹ BINDING 은 형태론의 부산물이 아니다 ⟹ **anima 가 가진 가장 강한 기질 증거**")
            print("       (이건 어깨 으쓱이 아니라 **양성 결과**다 — 벽에 대한)")
        else:
            print("    ⚠️ 중간 — 사전등록 분기 어디에도 없다 ⟹ seed 를 늘려 잡음을 배제한 뒤에만 판독")


if __name__ == "__main__":
    main()
