#!/usr/bin/env python3
# audit_window_math.py — G0-G6 gate seed ↔ CLM decode window(T=24) 정합성 실측.
#
# reference-match: seed 구성을 origin/main cli/evaluate.py (g_eval_g0/g1/g2/g5/g6) +
# core/g6_ideation.{hexa,py} g6_build_frames 에서 VERBATIM 재현 (decode 없음, $0 순수 문자열 수학).
# CLM decode 계약 (core/decode.{hexa,py}): T=24 right-aligned window, pad-left byte 32.
#   window(seed) = 마지막 24 bytes (짧으면 space pad-left) — clm_decode_topk_sampled_W 1:1.
#
# 핵심 질문: composed seed 의 생성 시작 window 가 single seed 의 window 와 byte-identical 인가?
# (identical 이면 composed 조건화 = single 조건화 → composed>single 은 어떤 모델도 물리 불가.)
import json

T = 24

# ── VERBATIM: g6_ideation._g6_concepts (== gauge_lib.CONCEPTS seed texts) ──
CZ = ["consciousness arises from cells",
      "tension ripples between distant minds",
      "memory composes into new meaning",
      "silence still carries information",
      "the engine dreams when alone"]

# ── VERBATIM: gauge_lib CONCEPTS keyword sets (= evaluate._g_concept_keywords) ──
KW = [["consciousness", "cells", "mind", "aware"],
      ["tension", "ripple", "distant", "between"],
      ["memory", "meaning", "compose", "new"],
      ["silence", "information", "quiet", "carries"],
      ["dream", "engine", "alone", "sleep"]]

# ── VERBATIM: evaluate._g_g2_prompts ──
G2_PROMPTS = ["Silence and the engine together mean ",
              "When memory meets distant minds, ",
              "Consciousness and silence combine into ",
              "The tension between cells and the engine becomes ",
              "If a dream and a distant mind merge, the result is ",
              "Memory and tension together create ",
              "When the engine remembers silence, it ",
              "Distant minds and consciousness form "]


def clm_window(seed: str) -> bytes:
    """core/decode.py clm_decode_topk_sampled_W L664-669 VERBATIM mirror:
    right-aligned last-T bytes, pad-left 0x20."""
    b = seed.encode("utf-8", "surrogateescape")
    if len(b) >= T:
        return b[-T:]
    return b" " * (T - len(b)) + b


def row(label, seed):
    b = seed.encode("utf-8")
    w = clm_window(seed)
    return {"label": label, "seed": seed, "seed_bytes": len(b),
            "over_T24": len(b) > T, "window": w.decode("utf-8", "replace")}


out = {"T": 24, "note": "CLM mouth decode contract (core/decode.{hexa,py}); "
                        "ByteGPT mouth grows window to block=512 (no fixed-T)."}

# ── G0: seed = cz[i] + ": "  (evaluate.py:123) ──
out["G0"] = [row("g0[%d]" % i, CZ[i] + ": ") for i in range(5)]

# ── G5: seed = cz[i] + ": "  (evaluate.py:549) — G0 과 동일 seed ──
out["G5_same_seed_as_G0"] = True

# ── G1 single: seed = cz[s] + ". "  (evaluate.py:162) ──
g1_single = [row("single[%d]" % s, CZ[s] + ". ") for s in range(5)]
out["G1_single"] = g1_single

# ── G1 composed: k∈{2..5}, seed = "c0. c1. ... c(k-1). "  (evaluate.py:168-174) ──
g1_comp = []
for k in range(2, 6):
    seed = ""
    for c in range(k):
        if c > 0:
            seed += ". "
        seed += CZ[c]
    seed += ". "
    r = row("composed[k=%d]" % k, seed)
    # 결정적 체크: composed window == single(마지막 개념 k-1) window ?
    r["window_eq_single_last"] = (clm_window(seed) == clm_window(CZ[k - 1] + ". "))
    r["last_concept_idx"] = k - 1
    # window 안에 keyword 가 온전히 들어있는 개념 집합 (조건화 물리 가능 개념)
    wtxt = clm_window(seed).decode("utf-8", "replace").lower()
    r["concepts_with_any_kw_fully_in_window"] = [
        i for i in range(5) if any(kw in wtxt for kw in KW[i])]
    g1_comp.append(r)
out["G1_composed"] = g1_comp
out["G1_verdict_math"] = {
    "all_windows_eq_single_last": all(r["window_eq_single_last"] for r in g1_comp),
    "explain": "len(cz[k-1]+'. ') >= 30 > T=24 이므로 composed/single 둘 다 window = "
               "cz[k-1]+'. ' 의 마지막 24B → byte-identical. composed 생성분포 = "
               "single(last) 생성분포 (차이는 sampler seed_rng 뿐: composed=7, single=7+s). "
               "따라서 composed>max_single 은 조건화가 아니라 표본 노이즈만 측정."}

# ── G2: 8 prompts ──
out["G2"] = [row("g2[%d]" % i, p) for i, p in enumerate(G2_PROMPTS)]
for i, r in enumerate(out["G2"]):
    wtxt = r["window"].lower()
    r["concepts_kw_in_window"] = [j for j in range(5) if any(k in wtxt for k in KW[j])]

# ── G6: g6_build_frames(6) composed — VERBATIM (g6_ideation.hexa:293-309) ──
frames = []
n = 5
for i in range(6):
    a = i % n
    b = (i + 1 + i // n) % n
    f = "if " + CZ[a] + ", then " + CZ[b] + ": "
    r = row("frame[%d] (a=%d,b=%d)" % (i, a, b), f)
    wtxt = r["window"].lower()
    r["pair"] = [a, b]
    # window 가 cB 의 tail 만인가 (cA 물리적 비가시)?
    r["cA_visible_in_window"] = CZ[a][:10].lower() in wtxt  # head of cA
    r["window_within_cB_tail"] = (clm_window(f) == clm_window(CZ[b] + ": "))
    frames.append(r)
out["G6_frames"] = frames
# 6 frame 중 서로 다른 window 수 (DIST≥5 달성가능성의 물리 상한)
uniq = len(set(clm_window("if " + CZ[i % n] + ", then " + CZ[(i + 1 + i // n) % n] + ": ")
               for i in range(6)))
out["G6_distinct_windows"] = uniq

print(json.dumps(out, ensure_ascii=False, indent=1))
