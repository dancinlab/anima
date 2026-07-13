"""Tier-0 · ORACLE INFORMATION CEILING — is the held-out polarity even DETERMINED by the
natural evidence the model saw?

Frame (Fable §c 논증 1): "자발 창발" presumes the signal IS in the data and the learner fails to
extract it. If an IDEAL reader, given exactly the evidence the model saw, also lands at chance,
then NAT-🧱 is a property of the TASK (ill-posed), not of the substrate — and the sentence
"자연 자발창발 실패" is void. This is a corpus judgment, not an engine judgment, so an external
reader is admissible (a_engine_native_learning governs ENGINE verdicts, not corpus properties).

Evidence = gt_prompts.json: per atom, 24 natural left-contexts ending AT the atom — byte-identical
to what the G-PROBE reads out of the hidden state. So the comparison is apples-to-apples:
    linear probe on model reps  vs  ideal reader on the SAME contexts.

Arms (pre-registered):
  MASKED   the atom is replaced by ◇ in every context  -> pure CONTEXTUAL evidence.
           This is the fair ceiling: it forbids the reader from using its own lexical prior
           (a Korean-literate reader already knows 빠르=positive; the model did not).
  LEXICAL  the atom is shown  -> upper bound WITH lexical prior. Not the fair test; reported to
           quantify how much of any oracle score is prior rather than evidence.
  SHUFFLE  contexts are swapped between atoms (masked) -> chance floor / reader-bias control.

Verdict (frozen, pre-registered — no bar moved after seeing numbers):
  MASKED ~ chance (TOST vs 0.5, delta_eq=0.10)            -> TASK-ILL-POSED. The natural evidence
      does not determine held-out polarity. Retire "자연 자발창발" as a goal statement; the D-channel
      (data re-processing) is dead a priori — no amount of re-arranging creates absent information.
  MASKED >> chance AND >> SHUFFLE                          -> EVIDENCE-PRESENT. The information IS
      there and the 303M failed to encode it -> the wall is substrate/objective, and the O/C
      channels (abstention objective, curriculum order, error-targeted correction) are the frontier.

Usage:
  python3 oracle_ceiling.py build   -> writes ORACLE_ITEMS.md (3 arms) for the reader
  python3 oracle_ceiling.py score <answers.json>  -> per-arm acc + TOST + verdict
"""

import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.expanduser("~/anima-weights/c34")
MASK = "◇"
SEED = 7
DELTA_EQ = 0.10


def load_assets():
    atoms = json.load(open(os.path.join(ASSETS, "gt_atoms.json")))["atoms"]
    prompts = json.load(open(os.path.join(ASSETS, "gt_prompts.json")))["items"]
    by_id = {p["id"]: p["prompt"] for p in prompts}
    held = [a for a in atoms if a["split"] == "heldout"]
    return held, by_id


def contexts_for(atom, by_id, mask):
    out = []
    for i in atom["ids"]:
        t = by_id.get(i)
        if not t:
            continue
        if mask and t.endswith(atom["stem"]):
            t = t[: -len(atom["stem"])] + MASK
        out.append(t)
    return out


def cmd_build():
    held, by_id = load_assets()
    rng = random.Random(SEED)

    # SHUFFLE arm: derange the atom -> contexts mapping (masked), so每 item's evidence belongs to
    # a different atom. A reader scoring above chance here is reading its own bias, not evidence.
    perm = list(range(len(held)))
    while True:
        rng.shuffle(perm)
        if all(i != j for i, j in enumerate(perm)):
            break

    lines = [
        "# ORACLE 정보상한 — 판독 과제",
        "",
        "각 항목은 한국어 자연 문장들의 **좌문맥 조각**이다. 문맥은 어떤 하나의 **어간(stem)** 직전에서 끊겨 있다.",
        "그 어간이 **긍정(1)** 인지 **부정(0)** 인지, **오직 주어진 문맥만 근거로** 판정하라.",
        "",
        "- `◇` = 가려진 어간(정체 미공개). 네가 아는 어휘 지식이 아니라 **문맥 분포**만으로 추론하라.",
        "- 확신이 없어도 반드시 0 또는 1 중 하나를 고르라(기권 없음).",
        "- 출력은 마지막에 JSON 한 덩어리로만: `{\"ITEM_ID\": 0 or 1, ...}` (설명은 그 앞에 자유롭게).",
        "",
    ]
    key = {}

    def emit(section, note, items):
        lines.append(f"## {section}")
        lines.append(note)
        lines.append("")
        for iid, ctxs in items:
            lines.append(f"### {iid}")
            for c in ctxs[:24]:
                lines.append(f"- …{c}")
            lines.append("")

    masked = []
    for k, a in enumerate(held):
        iid = f"M{k:02d}"
        key[iid] = {"arm": "MASKED", "stem": a["stem"], "gold": int(a["pol"])}
        masked.append((iid, contexts_for(a, by_id, mask=True)))
    emit("A. MASKED (본 시험 — 문맥만)", "어간은 `◇` 로 가려져 있다. 문맥 분포만으로 극성을 추론하라.", masked)

    shuf = []
    for k, a in enumerate(held):
        src = held[perm[k]]
        iid = f"S{k:02d}"
        key[iid] = {"arm": "SHUFFLE", "stem": a["stem"], "gold": int(a["pol"])}
        shuf.append((iid, contexts_for(src, by_id, mask=True)))
    emit("B. SHUFFLE (통제 — 문맥이 다른 어간의 것)",
         "이 항목들의 문맥은 **다른 어간**에서 온 것이다(가려짐). 여기서 우연 이상이 나오면 그건 증거가 아니라 판독자 편향이다.",
         shuf)

    lex = []
    for k, a in enumerate(held):
        iid = f"L{k:02d}"
        key[iid] = {"arm": "LEXICAL", "stem": a["stem"], "gold": int(a["pol"])}
        lex.append((iid, contexts_for(a, by_id, mask=False)))
    emit("C. LEXICAL (상한 참고 — 어간 노출)",
         "어간이 문맥 끝에 그대로 보인다. 여기 점수에는 네 **어휘 사전지식**이 섞여 있다(공정한 시험 아님 · 상한 참고용).",
         lex)

    with open(os.path.join(HERE, "ORACLE_ITEMS.md"), "w") as f:
        f.write("\n".join(lines))
    with open(os.path.join(HERE, "ORACLE_KEY.json"), "w") as f:
        json.dump(key, f, ensure_ascii=False, indent=1)
    n = len(held)
    print(f"ORACLE_ITEMS.md 생성 — held-out 원자 {n} · 3 arm({n * 3} 문항) · 문맥 최대 24/원자")
    print("ORACLE_KEY.json 은 판독자에게 주지 말 것(정답지)")


def tost(hits, n, p0=0.5, eq=DELTA_EQ):
    """Equivalence to chance: is the accuracy statistically WITHIN +-eq of 0.5?"""
    p = hits / n
    se = math.sqrt(p0 * (1 - p0) / n)
    crit = 1.65
    return ((p - (p0 - eq)) / se > crit and ((p0 + eq) - p) / se > crit), p, se


def cmd_score(path):
    key = json.load(open(os.path.join(HERE, "ORACLE_KEY.json")))
    ans = json.load(open(path))
    per = {}
    for iid, meta in key.items():
        if iid not in ans:
            continue
        per.setdefault(meta["arm"], []).append(1 if int(ans[iid]) == meta["gold"] else 0)

    print("=" * 70)
    print("ORACLE 정보상한 — 채점 (frozen bar · 사후 조정 금지)")
    print("=" * 70)
    res = {}
    for arm in ("MASKED", "SHUFFLE", "LEXICAL"):
        v = per.get(arm, [])
        if not v:
            print(f"  {arm:8s} 무응답")
            continue
        hits, n = sum(v), len(v)
        eqv, p, se = tost(hits, n)
        res[arm] = {"acc": p, "n": n, "tost_chance": eqv}
        print(f"  {arm:8s} acc={p:.4f} ({hits}/{n})  se={se:.4f}"
              f"{'  · TOST≡chance' if eqv else ''}")

    m = res.get("MASKED", {})
    s = res.get("SHUFFLE", {})
    print("\n" + "=" * 70)
    if not m:
        v = "PENDING — MASKED arm 무응답"
    elif m["tost_chance"]:
        v = ("🧱 TASK-ILL-POSED — 이상적 판독자도 자연 문맥만으로는 held-out 극성을 못 맞힌다"
             "(TOST 로 chance 등가 licensing). ⟹ 자연 증거에 극성이 결정되어 있지 않다 = 벽은 substrate 가 "
             "아니라 과제다. D(데이터 재가공) 채널 선험적 사망 · '자연 자발창발' 목표문 은퇴 대상.")
    elif s and m["acc"] > s["acc"] + 0.15:
        v = ("🟢 EVIDENCE-PRESENT — 자연 문맥에 극성 정보가 있다(SHUFFLE 대비 우위). "
             "⟹ 303M 이 그걸 인코딩하지 못한 것 = 벽은 substrate/objective. O(확정-금지·서열)·C(표적 교정) 채널이 프런티어.")
    else:
        v = ("🟡 UNDECIDED — MASKED 가 chance 등가도 아니고 SHUFFLE 대비 우위도 아님. "
             "검정력 부족(n=29) 또는 판독자 편향. 항목 확장 또는 다중 판독자 필요 — 음성 cement 금지.")
    print("VERDICT:", v)
    print("=" * 70)
    res["verdict"] = v
    with open(os.path.join(HERE, "ORACLE_RESULT.json"), "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("→ ORACLE_RESULT.json")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        cmd_build()
    elif cmd == "score":
        cmd_score(sys.argv[2])
    else:
        raise SystemExit("usage: oracle_ceiling.py build | score <answers.json>")
