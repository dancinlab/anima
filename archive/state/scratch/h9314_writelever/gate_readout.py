"""H_9314 WRITE-LEVER — frozen readout. Bars live in PREREG.md; this file only ENFORCES them.

The question H_9313 left behind. Its CPT failed to land a single held-out polarity, and everything
that could have explained that away has been ruled out by measurement:

    serialization   innocent   — quant-swallow: 66.7% of weights survive the int4 grid
    convergence     perfect    — val_CE 0.137, DESCENT
    forgetting      none       — SEEN flip0 held at 0.9500
    held-out        chance     — 0.4828

What remains is the thing the corpus itself says out loud: in pretraining, the slot
`이 영화 ___고 => ` was filled by a SEEN stem 960 times and by a held-out stem ZERO times. The model
learned that prior hard. A 600-step fine-tune tried to overturn it. So the failure may be a fact
about the training BUDGET rather than about the substrate — and that is a question with a number.

DV:
  WRITE   held-out flip0, against the label we wrote.  bar 0.95 (byte-carried from H_9313).
  FORGET  SEEN flip0.  bar 0.90 — a budget that lands the new atoms by destroying the old ones is
          not a budget, it is damage.

flip1 is NOT read here. That is H_9313's DV and it has its own frozen bars; reading it now, on a
model whose WRITE gate we are still calibrating, is exactly the confusion that makes an instrument
useless.

The interesting verdict is the negative one. If WRITE does not move with budget AT ALL — flat at
chance across 600 -> 6000 steps and 4x the learning rate — then the pretraining prior cannot be
overturned by continued training on this corpus, and that is EARNED, not a shrug: it says the next
lever is the corpus (natural polarity-bearing context), not the optimizer.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REMOTE = os.path.expanduser("~/anima-weights/h9314")     # pulled from summer

BAR_WRITE = 0.95        # byte-carried from H_9313
BAR_FORGET = 0.90
BASE_HELD = 0.4598      # no-CPT baseline on the same train-line manifest
BASE_SEEN = 0.9500
H9313 = (600, "5e-5", 0.4483)   # the cell that failed, for reproduction

CELLS = [(600, "5e-5"), (2000, "5e-5"), (6000, "5e-5"), (600, "2e-4"), (2000, "2e-4")]


def frac(path):
    if not os.path.exists(path):
        return None
    rows = json.load(open(path))["splits"]["heldout"]["rows"]
    return sum(1 for r in rows if r["margin"] > 0) / max(1, len(rows)), len(rows)


def main():
    print("=" * 88)
    print("H_9314 WRITE-LEVER — 사전학습 prior(960회) 를 뒤집는 데 얼마나 써야 하는가")
    print("  WRITE = held-out flip0 (bar %.2f · H_9313 에서 바이트 이월) · 기준선 %.4f"
          % (BAR_WRITE, BASE_HELD))
    print("  FORGET = SEEN flip0 (bar %.2f) · 기준선 %.4f — 새것을 심느라 옛것을 부수면 그건 예산이 아니다"
          % (BAR_FORGET, BASE_SEEN))
    print("  ⚠️ flip1 은 읽지 않는다 — 그건 H_9313 의 DV 이고 자기 bar 를 갖는다")
    print("=" * 88)
    print()

    res, pending = {}, []
    for st, lr in CELLS:
        tag = "s%d_lr%s" % (st, lr)
        w = frac(os.path.join(REMOTE, "wl_%s_held.json" % tag))
        f = frac(os.path.join(REMOTE, "wl_%s_seen.json" % tag))
        if not w or not f:
            pending.append(tag)
            continue
        res[(st, lr)] = (w[0], f[0])
        ok_w, ok_f = w[0] >= BAR_WRITE, f[0] >= BAR_FORGET
        print("  steps=%-5d lr=%-5s  WRITE=%.4f %s   FORGET=%.4f %s   %s"
              % (st, lr, w[0], "✅" if ok_w else "⛔",
                 f[0], "✅" if ok_f else "⚠️망각",
                 "🟢 예산 발견(후보)" if (ok_w and ok_f) else ""))
    if pending:
        print("\n[PENDING] 미회수: %s" % ", ".join(pending))
        return

    winners = [(k, v) for k, v in res.items() if v[0] >= BAR_WRITE and v[1] >= BAR_FORGET]
    writes = [v[0] for v in res.values()]
    spread = max(writes) - min(writes)

    print("\n" + "=" * 88)
    if winners:
        (st, lr), (w, f) = sorted(winners, key=lambda x: x[0][0])[0]     # cheapest budget that works
        v = ("🟢 예산 발견 (후보) — steps=%d lr=%s 에서 WRITE=%.4f · FORGET=%.4f. "
             "⚠️ 단일 seed 다(#3462: '네 점의 효과크기·순위는 전부 단일-시드 잡음이었다') ⟹ "
             "**2 seed AND 로 재현한 뒤에만** H_9313 재발사의 예산으로 채택한다. "
             "재발사는 H_9313 사전등록 그대로(bar 불변 · flip1 이 그때의 DV)." % (st, lr, w, f))
    elif spread < 0.05:
        v = ("🧱 PRIOR-LOCKED — **벌어낸 음성**. 예산을 10배(600→6000 step)로, 학습률을 4배로 "
             "늘려도 WRITE 가 우연에서 움직이지 않는다(전 셀 편차 %.3f). 사전학습이 이 슬롯에 "
             "SEEN 어간을 960회 넣고 held-out 어간을 0회 넣은 prior 는 **이 코퍼스 위의 CPT 로는 "
             "뒤집히지 않는다**. ⟹ 다음 레버는 옵티마이저가 아니라 **코퍼스**다 — 극성이 다음 "
             "바이트를 실제로 결정하는 자연 문맥(H_9291 ORACLE 이 29/29 로 복원한 그 문맥)으로 "
             "접지시켜야 한다. A 채널 가중치 경로는 아직 닫히지 않았다(코퍼스 설계 미탐)." % spread)
    else:
        v = ("⚠️ UNDER-BUDGET — WRITE 가 예산과 함께 움직이나(편차 %.3f) 아직 bar %.2f 에 못 미친다. "
             "단조 증가면 더 큰 예산으로 1회 연장한다. 단조가 아니면 잡음이므로 seed 를 늘려라."
             % (spread, BAR_WRITE))
    print("VERDICT:", v)
    json.dump({"hypothesis": "H_9314", "cells": {f"{k[0]}_{k[1]}": v for k, v in res.items()},
               "spread": spread, "verdict": v},
              open(os.path.join(HERE, "WLEVER.json"), "w"), ensure_ascii=False, indent=1)
    print("→ WLEVER.json")


if __name__ == "__main__":
    main()
