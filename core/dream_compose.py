"""core/dream_compose.py — REM/N3 co-replayed anchor geometric blend → .kosmos NODE.

py 2-production twin of core/dream_compose.hexa — byte-exact mirror (owner directive 2026-07-09
"py 자체구현 · 언어간 상호의존 0"). Blends two co-replayed anchors (coord midpoint · tension5
mean · radius max · lane=dream) into a new node — a designed geometric law (NOT a learned
semantic insight, c9). pure_field/emit-drive/recall_thr DISJOINT · p5 NO SPEAK. Pure list/scalar
math (sqrt via libm → math.sqrt); no numpy, no FFI. (hexa Map #{} → python dict.)
"""

from math import sqrt


def dc_make_anchor(id, coord, lane, radius, tension5, text):
    return {
        "id": id,
        "coord": coord,
        "lane": lane,
        "radius": radius,
        "tension5": tension5,
        "text": text,
        "replay_window": -1,
        "anchor_kind": "seed",
    }


def dc_vec_mid(a, b):
    na = len(a)
    nb = len(b)
    n = na if na < nb else nb
    out = []
    i = 0
    while i < n:
        av = float(a[i])
        bv = float(b[i])
        out.append((av + bv) / 2.0)
        i = i + 1
    return out


def dc_fmax(a, b):
    if a > b: return a
    return b


def dc_cosine(a, b):
    na = len(a)
    nb = len(b)
    n = na if na < nb else nb
    dot = 0.0
    sa = 0.0
    sb = 0.0
    i = 0
    while i < n:
        av = float(a[i])
        bv = float(b[i])
        dot = dot + av * bv
        sa = sa + av * av
        sb = sb + bv * bv
        i = i + 1
    return dot / (sqrt(sa) * sqrt(sb) + 0.000000001)


def dc_stage_replay_budget(stage):
    if stage == 3: return 7    # N3
    if stage == 4: return 3    # REM
    return 0


def dc_coreplayed(anchor_a, anchor_b, window):
    if window < 0: return False
    wa = int(anchor_a["replay_window"])
    wb = int(anchor_b["replay_window"])
    return (wa == window) and (wb == window)


def dc_compose_dream_anchor(parent_a, parent_b):
    coord = dc_vec_mid(parent_a["coord"], parent_b["coord"])
    t5 = dc_vec_mid(parent_a["tension5"], parent_b["tension5"])
    ra = float(parent_a["radius"])
    rb = float(parent_b["radius"])
    radius = dc_fmax(ra, rb)
    id_a = str(parent_a["id"])
    id_b = str(parent_b["id"])
    return {
        "id": "dream(" + id_a + "+" + id_b + ")",
        "coord": coord,
        "lane": "dream",              # derived-schema lane (≠ emit-drive 0/4)
        "radius": radius,
        "tension5": t5,
        "text": "",                   # NARRATIVE M1 이 채울 hook (지금은 빈 payload)
        "replay_window": -1,          # 새 node 는 이번 window 의 replay 대상 아님
        "anchor_kind": "dream_composed",  # baseline(recency-only)는 이 kind node 0개
        "parent_a": id_a,
        "parent_b": id_b,
    }


def dc_compose_window(anchors, stage, window):
    budget = dc_stage_replay_budget(stage)
    replayed = []
    i = 0
    while i < len(anchors):
        a = anchors[i]
        if int(a["replay_window"]) == window and window >= 0:
            if len(replayed) < budget:
                replayed.append(a)
        i = i + 1
    out = []
    n = len(replayed)
    p = 0
    while p < n:
        q = p + 1
        while q < n:
            out.append(dc_compose_dream_anchor(replayed[p], replayed[q]))
            q = q + 1
        p = p + 1
    return out


def dc_summary():
    return ("DREAM/dream_compose — REM/N3 co-replayed 두 anchor 를 기하 blend(coord midpoint · "
            "tension5 mean · radius max · lane=dream)하여 .kosmos 에 새 NODE append · a_kosmos "
            "node-only 정합 · pure_field/emit-drive/recall_thr DISJOINT · p5 NO SPEAK · 설계된 "
            "geometric law(학습 의미통찰 아님, c9)")
