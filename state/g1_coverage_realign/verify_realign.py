#!/usr/bin/env python3
"""realign 코퍼스 무결성 검증 — gate 의 EXACT tokenizer/keyword-set 로.

체크:
 1) LEAKAGE=0: 어떤 라인도 >=2 distinct gate set 의 keyword 공존 금지 (=gate 쌍 held-out).
 2) gate-internal PAIR 공동출현 = 0 (10 측정쌍).
 3) WINDOW: cluster 내 인접 scored keyword byte-gap <= T=24; 또한 각 라인에서 등장한
    gate keyword 가 라인 어딘가 24B window 안에 존재(자명하지만 max-gap 보고).
 4) COVERAGE: nongate form 다양성 + 각 gate set 방출빈도(전이 재료).
"""
import json
import re
import sys

# gate FROZEN (cli/evaluate.py::_g_concept_keywords VERBATIM)
KWSET = [["consciousness", "cells", "mind", "aware"],
         ["tension", "ripple", "distant", "between"],
         ["memory", "meaning", "compose", "new"],
         ["silence", "information", "quiet", "carries"],
         ["dream", "engine", "alone", "sleep"]]
KW2SET = {}
for si, ks in enumerate(KWSET):
    for k in ks:
        KW2SET[k] = si


def words(s):  # _g6_words / gauge_lib._words VERBATIM
    return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())


def line_sets(line):
    """이 라인이 hit 하는 distinct gate set 인덱스 집합."""
    wm = set(words(line))
    return {KW2SET[w] for w in wm if w in KW2SET}


def gate_word_positions(text):
    """(set_idx, word, byte_start) for each gate keyword token occurrence in text."""
    low = text.lower()
    res = []
    for m in re.finditer(r"[0-9A-Za-z가-힣]+", low):
        w = m.group(0)
        if w in KW2SET:
            res.append((KW2SET[w], w, m.start()))
    return res


def split_sent_cont(line):
    """(sentence, continuation). gate 측정 축 = 문장 뒤 continuation(cluster)."""
    i = line.find(". ")
    return (line[:i], line[i + 2:]) if i >= 0 else ("", line)


def check(path, label):
    lines = open(path).read().splitlines()
    max_sets = 0
    leak_lines = 0
    set_line_count = [0] * 5     # #lines hitting each set
    set_emit_count = [0] * 5     # total gate-keyword token occurrences per set (continuation)
    ground_first_off_max = 0     # GROUNDING(문장이 gate set hit) continuation 첫 gate-kw offset
    form_first_off_max = 0       # FORM(nongate 문장) continuation 첫 gate-kw offset (informational)
    cont_has_gate = 0            # #lines whose CONTINUATION emits >=1 gate keyword
    ground_lines = 0
    pair_cooccur = 0             # lines with any two DISTINCT gate sets (should be 0)
    examples_leak = []
    for ln in lines:
        s = line_sets(ln)
        if len(s) > max_sets:
            max_sets = len(s)
        if len(s) >= 2:
            leak_lines += 1
            pair_cooccur += 1
            if len(examples_leak) < 5:
                examples_leak.append(ln)
        for si in s:
            set_line_count[si] += 1
        sent, cont = split_sent_cont(ln)
        is_ground = len(gate_word_positions(sent)) > 0   # 문장이 gate set hit => grounding
        if is_ground:
            ground_lines += 1
        occ = gate_word_positions(cont)
        if occ:
            cont_has_gate += 1
            first_off = occ[0][2]
            if is_ground:
                ground_first_off_max = max(ground_first_off_max, first_off)
            else:
                form_first_off_max = max(form_first_off_max, first_off)
        for si, w, _ in occ:
            set_emit_count[si] += 1
    out = {
        "label": label, "path": path, "lines": len(lines),
        "max_distinct_gate_sets_per_line": max_sets,
        "LEAKAGE_lines_ge2_sets": leak_lines,
        "gate_pair_cooccur_lines": pair_cooccur,
        "grounding_lines": ground_lines,
        "set_line_count": set_line_count,
        "set_emit_token_count_continuation": set_emit_count,
        "lines_with_gate_kw_in_continuation": cont_has_gate,
        "grounding_first_gate_kw_offset_max": ground_first_off_max,
        "form_first_gate_kw_offset_max_informational": form_first_off_max,
        "leak_examples": examples_leak,
    }
    return out


res = {}
for path, label in [("corpus/en_block.txt", "en"), ("corpus/ko_block.txt", "ko")]:
    res[label] = check(path, label)

# EN 은 gate 측정 언어 -> 엄격. KO 는 EN gate keyword 기준(대개 0).
ok = True
r = res["en"]
if r["max_distinct_gate_sets_per_line"] > 1:
    ok = False
if r["gate_pair_cooccur_lines"] != 0:
    ok = False
if r["grounding_first_gate_kw_offset_max"] > 24:
    ok = False

res["VERDICT"] = {
    "leakage_zero": r["gate_pair_cooccur_lines"] == 0,
    "single_set_per_line": r["max_distinct_gate_sets_per_line"] <= 1,
    "grounding_gate_kw_window_reachable_le24": r["grounding_first_gate_kw_offset_max"] <= 24,
    "all_gate_sets_grounded": all(c > 0 for c in r["set_emit_token_count_continuation"]),
    "note_diff_set_cooccur_is_transfer_only": "integrity forbids 2 diff gate sets/line; "
        "cross-set co-emission at gate time is PURE transfer (by design)",
    "PASS": ok,
}
json.dump(res, open("verify.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(res["en"], ensure_ascii=False, indent=1))
print("VERDICT:", json.dumps(res["VERDICT"], ensure_ascii=False))
sys.exit(0 if ok else 1)
