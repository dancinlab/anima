"""EN arm readout — FROZEN before the CPT results existed (the CPT was still at step 1,350).

Bars are DERIVED, not transplanted (bar-derived-not-transplanted):
  n=60  flip1 rows per SEEN stratum   -> chance sd = 0.5/sqrt(60)  = 0.065
  n=120 flip1 rows held-out (the DV)  -> chance sd = 0.5/sqrt(120) = 0.046

GATES (the stratum each one may honestly live on is fixed by the corpus census —
 ground_keep TOUCHES held-out flip0 + SEEN flip1, and OMITS SEEN flip0 + held-out flip1):

  WRITE     held-out flip0  >= 0.75   did the planted fact land? If this FAILS the arm is
                                      budget-negative, not substrate-negative (H_9322 died here).
  FORGET    SEEN flip0      >= 0.75   the stratum the corpus NEVER touches = the honest gate.
                                      (H_9327's forget gate sat on a stratum its own corpus
                                       reinforced every step -> it certified "0 forgetting" while
                                       the operator was being destroyed. A forged gate.)
  OPERATOR  SEEN flip1      >= 0.75   REPLAYED by ground_keep, so this is a LIVENESS check: if the
                                      CPT killed the operator, every flip1 number is INVALID.
  DV        held-out flip1            THE QUESTION. above chance = >= 0.60 (2.2 sd).
                                      negative = TOST equivalence within +/-0.10 of 0.50.

READ ORDER IS NOT OPTIONAL: WRITE and OPERATOR are PRECONDITIONS. A DV read on an arm that failed
either of them is not a negative result — it is an INVALID one, and saying otherwise is how this
lane has burned itself twice.

COLLAPSE CHECK runs on every cell: a constant predictor scores the label ratio for free and it
looks exactly like "chance" in the headline (this is what the val_CE-minimum base did — 120/120
`negative`). Class split WITHIN each flip stratum, always (polarity-split-before-headline).

LIE ARM is the bias-independent check that decided H_9327: it plants the OPPOSITE polarity at the
same budget. If the DV moves the SAME way in both arms, the model is reading a surface bias, not
the planted fact. dep = (DV acc | planted=pos) - (DV acc | planted=neg), computed within the arm.
"""
import json, os, sys, glob
from collections import Counter

R = sys.argv[1] if len(sys.argv) > 1 else "."
BAR_W, BAR_F, BAR_OP, BAR_DV, TOST = 0.75, 0.75, 0.75, 0.60, 0.10

def load(p):
    return json.load(open(p))["splits"]["heldout"]["rows"]

def acc(rows):
    return sum(1 for r in rows if r["margin"] > 0) / len(rows) if rows else float("nan")

def cell(rows, flip):
    return [r for r in rows if r["flip"] == flip]

def collapsed(rows):
    if not rows: return False
    c = Counter(r["first_word"] for r in rows)
    return c.most_common(1)[0][1] / len(rows) > 0.95

def show(name, rows, bar=None):
    a = acc(rows)
    mark = "" if bar is None else ("  ✅" if a >= bar else "  ⛔")
    col = "  💀 붕괴" if collapsed(rows) else ""
    # class split WITHIN the stratum — a headline hides where its number came from
    byp = {p: acc([r for r in rows if r["pol"] == p]) for p in (0, 1)}
    print(f"    {name:<26} {a:.4f}  (n={len(rows)})"
          f"   pol0={byp[0]:.3f} pol1={byp[1]:.3f}{mark}{col}")
    return a

print("=" * 78)
print("EN ARM — 최종 판독  (동결: CPT step 1,350 시점 · 결과를 보기 전)")
print("=" * 78)

for tag, label in [("cpt_en_s7", "seed 7"), ("cpt_en_s11", "seed 11"), ("cpt_en_lie_s7", "LIE 통제군 (seed 7)")]:
    ps, ph = f"{R}/F_post_seen_{tag}.json", f"{R}/F_post_held_{tag}.json"
    if not (os.path.exists(ps) and os.path.exists(ph)):
        print(f"\n── {label}: 결과 없음")
        continue
    S, H = load(ps), load(ph)
    print(f"\n── {label}   (SEEN {len(S)}행 · held-out {len(H)}행)")
    print("  전제조건 (실패하면 DV 는 음성이 아니라 INVALID)")
    w  = show("WRITE    held-out flip0", cell(H, 0), BAR_W)
    f_ = show("FORGET   SEEN flip0", cell(S, 0), BAR_F)
    op = show("OPERATOR SEEN flip1", cell(S, 1), BAR_OP)
    print("  DV")
    dv = show("         held-out flip1", cell(H, 1), BAR_DV)

    pre_ok = (w >= BAR_W) and (f_ >= BAR_F) and (op >= BAR_OP)
    print(f"\n  전제조건: {'✅ 전부 통과 — DV 를 읽어도 된다' if pre_ok else '⛔ 실패 — 이 DV 는 INVALID (음성 아님)'}")
    if pre_ok:
        if dv >= BAR_DV:
            print(f"  🟢 DV {dv:.4f} >= {BAR_DV} — 우연 초과. 자유 부정어 `not` 이 선언형 저장소에 닿았다.")
            print("     ⟹ 두 저장소 분리는 **형태론**이 만든 것 · BINDING = 형태론, 기질 아님 · 레인 재개방")
            print("     ⚠️ SCREENER(DIRECTIONAL) — EN 은 형태론+기반모델+담체를 한꺼번에 바꾼다")
        elif abs(dv - 0.5) <= TOST:
            print(f"  🧱 DV {dv:.4f} — 0.5 에서 ±{TOST} 이내 = TOST 등가 = 우연.")
            print("     ⟹ 붙지 않는 자유 부정어로도 분리가 살아남았다 ⟹ **byte-LM×CE 아키텍처의 성질**")
            print("     ⟹ 벽은 진짜지만 H_9334 의 처방(연산자-키 write)으로 **고칠 수 있다**")
        else:
            print(f"  ⏳ DV {dv:.4f} — 바(0.60)와 TOST 대역 사이. 이 n 으로는 못 가른다 ('없다' 가 아니다)")

# LIE: the bias-independent check that decided H_9327
main = f"{R}/F_post_held_cpt_en_s7.json"
lie  = f"{R}/F_post_held_cpt_en_lie_s7.json"
if os.path.exists(main) and os.path.exists(lie):
    print("\n" + "=" * 78)
    print("LIE 통제군 — 편향-무관 검사 (H_9327 을 결정한 검사)")
    print("=" * 78)
    for nm, p in (("MAIN", main), ("LIE ", lie)):
        H = cell(load(p), 1)
        a_pos = acc([r for r in H if r["pol"] == 1])
        a_neg = acc([r for r in H if r["pol"] == 0])
        print(f"  {nm}  DV|심은극성=긍정 {a_pos:.3f}   DV|심은극성=부정 {a_neg:.3f}   dep={a_pos - a_neg:+.3f}")
    print("""
  읽기: dep 은 '답이 심은 극성에 얼마나 의존하는가' 다.
        두 팔의 dep 이 **같은 부호로 크면** 모델은 심은 사실이 아니라 **표면 편향**을 읽고 있다.
        두 팔의 dep 이 **반대로 갈라지면** 심은 사실이 실제로 조회되고 있다.""")
