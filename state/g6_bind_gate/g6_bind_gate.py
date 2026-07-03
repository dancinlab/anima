#!/usr/bin/env python3
"""G6 bind-gate — form-priming 내성 additive G6 검출기 (frozen-first, torch-free).

배경 (state/g6_targeted_corpus/): 3-arm warm-FT engine-native 결과에서 frozen
`_g6_is_falsifiable`(comparator ∧ measurable ∧ ≥2 content)가 FORM-only 로 밝혀짐 —
SHUF(주제-bind만 파괴한 통제 코퍼스)도 FALS 6/6 통과 = style-FT 로 게임 가능.
진짜 재조합 신호는 bind Δ(TARGETED 0.444 vs SHUF 0.000)에 있으나 primary FALS 게이트는
그걸 못 잰다.

이 파일 = **새 additive 게이트** `is_falsifiable_topic_bound(text, frame_ab)` =
    frozen FALS 형태검사(그대로)  AND  topic_bound(text, frame_ab)  ← 새 bind 항
frozen `_g6_is_falsifiable` 는 한 글자도 안 건드린다 — 아래 `is_falsifiable` 는
core/g6_ideation.hexa 의 VERBATIM 미러(reference copy)이고, 새 게이트는 그 위에
bind 항을 AND 로 얹기만 한다.

bind 항 = reference-match 로 state/g6_targeted_corpus 채점기(summer)와 byte-faithful:
  · concept keyword-set = tool/gauge_lib.CONCEPTS VERBATIM
  · concept_hits(text)  = gauge_lib._concept_hits (kw-set ∩ words)
  · topic_bound(text,{a,b}) = (hits ∩ {a,b} ≠ ∅)  AND  (hits ⊆ {a,b})
       = 프레임의 실제 주제쌍 중 ≥1을 호출하고, 프레임 밖 주제는 0 누출(purity)
  이 규칙이 results json 의 comp_bind/shuf_bind 18값을 정확 재현함(validate() 참조):
  comp/shuf 디코드 둘 다 **동일한 의도된 쌍**(MEASURED = g6_build_frames(6) composed)에
  대해 채점된다 — shuffled 프레임을 준 디코드가 의도쌍에 얼마나 덜 결합하는지가 delta.

torch/numpy 미사용, 결정적. 재학습 0 — 기존 fragment(results json comp_texts)만 재채점.
"""
import json
import os
import re
import sys

# ════════════════════════════════════════════════════════════════════════════
# (A) FROZEN FALS 항 — core/g6_ideation.hexa `_g6_is_falsifiable` VERBATIM 미러.
#     ⚠️ 이 블록은 frozen bar 의 reference copy. 수정 금지(tune-to-green 금지).
# ════════════════════════════════════════════════════════════════════════════
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater",
              "fewer", "higher", "lower", "increases", "decreases", "correlates",
              "predicts", "causes", "depends", "unless", "whereas", "versus",
              "compared", "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STOP = {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that", "we", "you",
        "they", "s", "t", "as", "on", "at", "by", "or", "be", "an", "for", "with",
        "this", "from", "are", "was"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}

# 5 corpus concepts (seed text) — VERBATIM from _g6_concepts() / gauge_lib.CONCEPTS[*][0]
_CONCEPT_SENT = ["consciousness arises from cells",
                 "tension ripples between distant minds",
                 "memory composes into new meaning",
                 "silence still carries information",
                 "the engine dreams when alone"]

_TOK = re.compile(r"[0-9A-Za-z]+")


def _words(s):
    """core/g6_ideation.hexa `_g6_words` VERBATIM: lowercase, split on non-[0-9A-Za-z]."""
    return [m.group(0).lower() for m in _TOK.finditer(s)]


def _build_known(dict_path="/usr/share/dict/words"):
    """core/g6_ideation.hexa `_g6_dict_load` VERBATIM: stopwords ∪ concept-sentence words
    ∪ /usr/share/dict/words. (comparator/measurable/stance/kw 는 안 넣음 — hexa 와 동일;
    'ratio','greater' 등은 dict 경유로 KNOWN 에 들어옴.)"""
    known = set(STOP)
    for c in _CONCEPT_SENT:
        known |= set(_words(c))
    if os.path.exists(dict_path):
        with open(dict_path, errors="ignore") as f:
            for w in f:
                wl = _words(w.strip())
                if len(wl) == 1:
                    known.add(wl[0])
    return known


def is_falsifiable(text, known):
    """FROZEN. core/g6_ideation.hexa `_g6_is_falsifiable` VERBATIM logic. p7: NOT a quality judge.
      (a) comparator/conditional mark  (b) measurable/quantity mark
      (c_i) ≥2 content words (len≥3, in KNOWN, not stop)
      (c_ii) not trailing '?'  (c_iii) first-3 tokens not a pure-stance subset."""
    wl = _words(text)
    if not wl:
        return False
    if not any(w in COMPARATOR for w in wl):
        return False
    if not any(w in MEASURABLE for w in wl):
        return False
    if sum(1 for w in wl if len(w) >= 3 and w in known and w not in STOP) < 2:
        return False
    if text.strip().endswith("?"):
        return False
    nf = min(3, len(wl))
    if nf > 0 and all(wl[f] in STANCE for f in range(nf)):
        return False
    return True


# ════════════════════════════════════════════════════════════════════════════
# (B) 새 BIND 항 — reference-match state/g6_targeted_corpus 채점기 + gauge_lib.
# ════════════════════════════════════════════════════════════════════════════
# concept keyword-set = tool/gauge_lib.CONCEPTS VERBATIM (kw-set 만).
CONCEPT_KW = [
    {"consciousness", "cells", "mind", "aware"},
    {"tension", "ripple", "distant", "between"},
    {"memory", "meaning", "compose", "new"},
    {"silence", "information", "quiet", "carries"},
    {"dream", "engine", "alone", "sleep"},
]

# 측정 프레임 = core/g6_ideation.hexa g6_build_frames(6) composed 순서 (i%5,(i+1+i//5)%5):
MEASURED = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]


def concept_hits(text):
    """gauge_lib._concept_hits VERBATIM: kw-set 이 생성 텍스트와 교차하는 concept 인덱스 집합."""
    wl = set(_words(text))
    return {i for i, kw in enumerate(CONCEPT_KW) if kw & wl}


def topic_bound(text, frame_ab):
    """새 BIND 항 (boolean, RECALL 규칙 = summer 채점기와 byte-faithful).
    frame_ab = (a,b) = 프레임의 실제 주제쌍 인덱스.
      bound  ⟺  concept_hits(text) ∩ {a,b} ≠ ∅
      = 디코드가 프레임의 실제 주제쌍 중 ≥1을 gate keyword-set 으로 호출.
    (reference-match: 이 recall 규칙이 results json 의 comp_bind/shuf_bind 18값을 정확
     재현한다 — validate() 참조. 더 엄격한 purity 변종은 topic_bound_strict.)"""
    a, b = frame_ab
    return bool(concept_hits(text) & {a, b})


def topic_bound_strict(text, frame_ab):
    """STRICTER 선택 변종 (purity): 프레임 주제 ≥1 호출 AND 프레임 밖 주제 0 누출.
      bound  ⟺  (hits ∩ {a,b} ≠ ∅)  AND  (hits ⊆ {a,b})
    recall 보다 TARGETED 를 약간 under-count(off-frame 누출 프레임 감점)하지만 SHUF 는
    동일하게 걸러 PASS 유지 — 배선 시 감도(sensitivity) 옵션. 기본은 recall(reference-match)."""
    a, b = frame_ab
    h = concept_hits(text)
    return bool(h & {a, b}) and h.issubset({a, b})


def bind_purity(text, frame_ab):
    """연속 bind 점수 = 프레임내 hit / 전체 hit (진단; topic_bound_strict = (purity==1.0 ∧ in≥1))."""
    a, b = frame_ab
    h = concept_hits(text)
    if not h:
        return 0.0
    return len(h & {a, b}) / len(h)


# ════════════════════════════════════════════════════════════════════════════
# (C) 새 ADDITIVE 게이트 = frozen FALS  AND  새 bind 항.
# ════════════════════════════════════════════════════════════════════════════
def is_falsifiable_topic_bound(text, frame_ab, known):
    """form-priming 내성 게이트: frozen 형태검사 그대로 AND topic-bind.
    SHUF(bind 파괴 style-FT)는 is_falsifiable=True 여도 topic_bound=False → 걸러짐."""
    return is_falsifiable(text, known) and topic_bound(text, frame_ab)


# ════════════════════════════════════════════════════════════════════════════
# (D) 재채점 — 재학습 0. results json 의 comp_texts(의도 프레임 디코드)만 재채점.
# ════════════════════════════════════════════════════════════════════════════
def score_arm(arm_json, known):
    """한 arm results json → per-seed frozen-FALS / bind / 새 게이트(FALS_bound) 재채점.
    comp_texts[i] 는 의도 프레임 MEASURED[i] 의 디코드. shuf_texts[i] 도 같은 의도쌍에 채점."""
    out = {"arm": arm_json["arm"], "seeds": []}
    for ps in arm_json["per_seed"]:
        comp = ps["comp_texts"]
        shuf = ps.get("shuf_texts", [])
        fals = [is_falsifiable(t, known) for t in comp]
        bound = [topic_bound(comp[i], MEASURED[i]) for i in range(len(comp))]
        gate = [is_falsifiable_topic_bound(comp[i], MEASURED[i], known)
                for i in range(len(comp))]
        gate_strict = [fals[i] and topic_bound_strict(comp[i], MEASURED[i])
                       for i in range(len(comp))]
        # bind 재현 검증용: comp/shuf 디코드를 동일 의도쌍 MEASURED 에 채점
        comp_bind = sum(topic_bound(comp[i], MEASURED[i])
                        for i in range(len(comp))) / len(comp)
        shuf_bind = (sum(topic_bound(shuf[i], MEASURED[i])
                         for i in range(len(shuf))) / len(shuf)) if shuf else None
        out["seeds"].append({
            "seed": ps["seed"],
            "fals_frozen": sum(fals),          # 기존 FORM-only 게이트
            "bound": sum(bound),               # 새 bind 항 단독 (recall)
            "fals_bound": sum(gate),           # 새 ADDITIVE 게이트 (recall, primary)
            "fals_bound_strict": sum(gate_strict),  # purity 변종 (sensitivity)
            "repro_comp_bind": round(comp_bind, 4),
            "orig_comp_bind": round(ps["comp_bind"], 4),
            "repro_shuf_bind": round(shuf_bind, 4) if shuf_bind is not None else None,
            "orig_shuf_bind": round(ps["shuf_bind"], 4),
        })
    return out


def validate(scored, arm_json):
    """18-값 faithfulness: repro comp/shuf bind == results json 의 orig 값."""
    ok = True
    for s in scored["seeds"]:
        if abs(s["repro_comp_bind"] - s["orig_comp_bind"]) > 1e-4:
            ok = False
        if s["repro_shuf_bind"] is not None and \
           abs(s["repro_shuf_bind"] - s["orig_shuf_bind"]) > 1e-4:
            ok = False
        # frozen FALS 항도 arm 의 보고 fals 와 일치해야 함
        rep = [p for p in arm_json["per_seed"] if p["seed"] == s["seed"]][0]
        if s["fals_frozen"] != rep["fals"]:
            ok = False
    return ok


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    res = os.path.join(root, "..", "g6_targeted_corpus", "results")
    known = _build_known()

    # frozen 10-string 캘리브레이션 (advisory ≥8/10) — reference copy 무결 확인
    pos = ["if consciousness increases, the emit rate measured at the boundary rises",
           "tension predicts a higher number of mitosis cells than silence does",
           "memory density correlates with a lower error threshold when grounded",
           "the Phi value is greater when distinct cells exceed a count of eight",
           "novelty rate decreases faster than coherence when the corpus size grows"]
    neg = ["That's a profound question. I think it's more than just information.",
           "consciousness is a beautiful mystery of the mind",
           "what is the meaning of a thought?",
           "the engine dreams when it is alone at night",
           "silence carries something deep and quiet"]
    calib = sum(is_falsifiable(t, known) for t in pos) + \
        sum(not is_falsifiable(t, known) for t in neg)

    report = {"detector_calibration_10": calib, "known_lexicon_size": len(known),
              "measured_frames": MEASURED, "arms": {}, "validate": {}}
    for name in ("base", "targeted", "shuf"):
        aj = json.load(open(os.path.join(res, f"{name}.json")))
        sc = score_arm(aj, known)
        report["arms"][aj["arm"]] = sc
        report["validate"][aj["arm"]] = validate(sc, aj)

    # ── 사전등록 PASS 판정 (threshold frozen, PREREG.md 참조) ──
    MAJ = 4          # FALS_bound majority bar (/6)  — 기존 ≥4/6 관례
    NSEED = 2        # ≥2 seeds
    MARGIN = 3.0     # TARGETED_mean − SHUF_mean 분리 bar

    def n_maj(arm):
        return sum(1 for s in report["arms"][arm]["seeds"] if s["fals_bound"] >= MAJ)

    def mean_fb(arm):
        ss = report["arms"][arm]["seeds"]
        return sum(s["fals_bound"] for s in ss) / len(ss)

    P1 = n_maj("BASE") == 0                       # BASE floor
    P2 = n_maj("TARGETED") >= NSEED               # TARGETED signal
    P3 = n_maj("SHUF") == 0                        # form-priming REJECT
    P4 = (mean_fb("TARGETED") - mean_fb("SHUF")) >= MARGIN
    report["prereg"] = {
        "thresholds": {"majority_/6": MAJ, "n_seeds": NSEED, "sep_margin": MARGIN},
        "n_maj": {a: n_maj(a) for a in ("BASE", "TARGETED", "SHUF")},
        "mean_fals_bound": {a: round(mean_fb(a), 4) for a in ("BASE", "TARGETED", "SHUF")},
        "P1_base_floor": P1, "P2_targeted_signal": P2,
        "P3_shuf_reject_formpriming": P3, "P4_separation": P4,
        "PASS": bool(P1 and P2 and P3 and P4),
    }
    # 대조: 기존 FORM-only 게이트가 SHUF 를 못 거른다는 것도 명시
    report["contrast_frozen_fals_only"] = {
        a: [s["fals_frozen"] for s in report["arms"][a]["seeds"]]
        for a in ("BASE", "TARGETED", "SHUF")
    }

    out = os.path.join(root, "rescore.json")
    json.dump(report, open(out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    print("\nwrote", out)


if __name__ == "__main__":
    main()
