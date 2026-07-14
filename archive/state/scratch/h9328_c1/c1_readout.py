"""C1 readout — bars frozen before the data landed (Fable's preregistration, §b).

The DV is NOT accuracy. Accuracy on flip1 is dominated by a global surface bias whose DIRECTION
flips between seeds (measured: the model bets 긍정 66.7% under one corpus and 88.5% under another;
s7 leans 긍정, s11 leans 부정). A headline built on that has no power. So the DV is the same
bias-free statistic that decided H_9327:

    Δdep = P(say 긍정 | stem polarity = 긍정) − P(say 긍정 | stem polarity = 부정)

taken WITHIN an arm, so the global bias — common to both conditions — cancels.

On a negated surface the gold is ¬polarity. So:
    operator applies      -> the answer tracks ¬polarity -> Δdep strongly NEGATIVE
    parroting the stem    -> the answer tracks polarity  -> Δdep strongly POSITIVE
    nothing is consulted  -> Δdep ≈ 0

Frozen bars (Fable): Δdep ≤ −0.5 on BOTH seeds = the operator is real and generalises.
                     |Δdep| ≤ 0.15 on both novel surfaces AND both seeds = H-γ (it was memorisation).
                     anything between = PENDING. No post-hoc arms.

ANCHOR (blocking): the three TRAINED surfaces must reproduce the operator in this same run
(Δdep ≤ −0.5). If they do not, the run is broken and the novel numbers are unreadable —
INVALID, never a negative. This is the gate H_9303/H_9307 died without.
"""
import json, os

R = os.path.expanduser("~/anima-weights/h9314")
TRAINED = {"negL": "{s}지 않다", "negS": "안 {s}고", "negE": "전혀 {s}지 않다"}
NOVEL = {"novT": "{s}지는 않다", "novB": "별로 {s}지 않다"}
BAR_OP, BAR_MEM = -0.5, 0.15


def dep(rows):
    """P(say 긍정 | pol=1) − P(say 긍정 | pol=0). Global bias is common to both terms → cancels."""
    g = {0: [], 1: []}
    for r in rows:
        said_pos = 1 if ((r["gold_word"] == "긍정") == (r["margin"] > 0)) else 0
        g[int(r["pol"])].append(said_pos)
    if not g[0] or not g[1]:
        return None
    return sum(g[1]) / len(g[1]) - sum(g[0]) / len(g[0])


def main():
    print("=" * 92)
    print("C1 — 연산자는 실재하는가, 아니면 480개 암기된 라인이었나  (사전학습 ckpt · 재학습 0)")
    print("  DV = Δdep (팔-내 극성 의존도 · 전역 편향 상쇄) — 부정형이므로 gold = ¬극성")
    print("  연산자 작동 → Δdep 크게 **음수**  ·  되뇜 → 크게 **양수**  ·  미조회 → **0**")
    print("=" * 92)

    res = {}
    for s in ("main_s7", "main_s11"):
        p = os.path.join(R, "c1_%s.json" % s)
        if not os.path.exists(p):
            print("\n[PENDING] %s 미회수" % s)
            return
        rows = json.load(open(p))["splits"]["heldout"]["rows"]
        res[s] = {b: dep([r for r in rows if r["b"] == b]) for b in list(TRAINED) + list(NOVEL)}

    print("\n  ⚓ 앵커 — 학습된 표면 (이 런에서 연산자가 재현되는가 · BLOCKING)")
    anchor_ok = True
    for b, pat in TRAINED.items():
        d7, d11 = res["main_s7"][b], res["main_s11"][b]
        ok = d7 <= BAR_OP and d11 <= BAR_OP
        anchor_ok &= ok
        print("     %-16s  s7 Δdep=%+.3f   s11 Δdep=%+.3f   %s"
              % (pat, d7, d11, "✅" if ok else "⛔"))
    if not anchor_ok:
        print("\n  VERDICT: ⛔ **INVALID** — 학습된 표면에서조차 연산자가 재현되지 않는다.")
        print("     이 런은 깨졌다. 새 표면 수치는 **읽지 않는다**(음성 아님).")
        return

    print("\n  🧪 새 표면 — 학습된 적 없음 (arrow 0회 · 자연문 0회 · 바이트 감사 통과)")
    novel = []
    for b, pat in NOVEL.items():
        d7, d11 = res["main_s7"][b], res["main_s11"][b]
        novel += [d7, d11]
        tag = ("✅ 일반화" if (d7 <= BAR_OP and d11 <= BAR_OP)
               else ("💀 붕괴(암기)" if (abs(d7) <= BAR_MEM and abs(d11) <= BAR_MEM) else "⏳ 중간"))
        print("     %-16s  s7 Δdep=%+.3f   s11 Δdep=%+.3f   %s" % (pat, d7, d11, tag))

    print("\n" + "=" * 92)
    if all(d <= BAR_OP for d in novel):
        print("VERDICT: 🟢 **연산자 실재 — H-γ 기각**")
        print("  본 적 없는 부정 표면에서도 연산자가 작동한다(양 seed · 두 표면 모두 Δdep ≤ %.1f)." % BAR_OP)
        print("  ⟹ SEEN 어간의 0.98~1.00 은 **암기가 아니라 조합**이었다.")
        print("  ⟹ **BINDING 이라는 이름이 옳다**: 연산자는 실재하고, CPT 로 쓴 사실이 거기 닿지 못한다.")
        print("  다음 = C3(SEEN-REWRITE 교차) — CPT 쓰기가 flip1 경로에 **보이는가**.")
    elif all(abs(d) <= BAR_MEM for d in novel):
        print("VERDICT: 💀 **H-γ 지지 — 연산자는 없었다. 480개 암기된 라인이었다.**")
        print("  본 적 없는 표면에서 의존도가 **0으로 붕괴**한다(양 seed · 두 표면).")
        print("  ⟹ H_9327 의 '연산자는 살아있다'(0.98~1.00)는 **라인 회상**이었고,")
        print("     **'BINDING' 이라는 이름은 틀렸다** — 결합할 연산자가 애초에 없다.")
        print("  ⟹ 벽의 정체가 바뀐다: 이 모델은 부정을 **연산**한 적이 없다. 카드/ARCHITECTURE 정정 필요.")
    else:
        print("VERDICT: ⏳ **PENDING** — 사전등록 두 분기 어디에도 안 맞는다(사후 팔 추가 금지).")
        print("  값: %s" % ", ".join("%+.3f" % d for d in novel))
        print("  부분 일반화 = 표면-특이적 회로일 수 있다. seed/표면을 늘려 검정력을 먼저 벌어라.")


if __name__ == "__main__":
    main()
