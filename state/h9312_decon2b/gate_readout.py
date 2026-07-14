"""H_9312 DECON-2b — frozen gate readout. Bars live in PREREG.md; this file only ENFORCES them.

What changed from H_9311, and what did not:

  G-A  REBUILT. Clause ① was a raw sign-agreement count against a bar (166/174) whose denominator
       came from a different manifest. It is now a margin noise model: a sign flip only counts
       against the window if it happens to a row the model was CONFIDENT about. Zero tolerance
       there — which is STRICTER than the count was in the region that matters, and lenient only
       where a flip means nothing (a margin sitting on zero). Clause ② is unchanged. Clause ③ is
       GONE FROM HERE — not deleted, MOVED (see G-L): it was invariant to the window (0.883 at
       win=64, 0.883 at win=128), so it could never adjudicate the window. A quantity that does
       not move with the thing a gate names cannot be a clause of that gate.

  G-L  NEW, and it is where ③ now lives. Its floor is DERIVED, not observed: if the instrument
       cannot reach the G-D decision bar on atoms the model has demonstrably MASTERED, it can
       never reach it on nonce or held-out atoms. So the floor IS the G-D bar (140/240 = 0.583).
       This is a necessary condition on the instrument, computed from the bar it must be able to
       clear — not from the baseline we happened to measure (that would be "observed − ε", which
       is the thing we are forbidding).

  G-B  BYTE-CARRIED. Its data already exists on disk. Touching its bar now would be, by
  G-D  definition, tune-to-green. Same for G-D and G-E, which have not been fired at all.
  G-E
"""

import json
import math
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = ("main_s7", "main_s11")

BAR_GA_ACC = 0.03          # |Δacc| between win 64 and win 128 (unchanged from H_9311)
BAND_Q = 10                # noise band = 10th percentile of |margin|@win64 over scored rows
BAR_GL = 140 / 240         # liveness floor = the G-D decision bar itself (derived, not observed)
BAR_GB = 0.90              # byte-carried
BAR_READ = 0.85            # byte-carried
BAR_CONSUME_NONCE = 140    # of 240 clusters — byte-carried
BAR_CONSUME_HELD = 20      # of 29 — byte-carried
BAR_ALT = 0.15             # alternation-bias validity — byte-carried


def load(n):
    p = os.path.join(HERE, n)
    return json.load(open(p)) if os.path.exists(p) else None


def rows(n):
    d = load(n)
    return d["splits"]["heldout"]["rows"] if d else None


def scored_idx(man):
    """bare-flip0 is the demo string verbatim — it measures copying, nothing else."""
    return [i for i, m in enumerate(man) if not (m["form"] == "bare" and m["flip"] == 0)]


def acc(rs, man, flip, forms=None):
    s = [r for r, m in zip(rs, man)
         if m["flip"] == flip and not (m["form"] == "bare" and m["flip"] == 0)
         and (not forms or m["form"] in forms)]
    return sum(1 for r in s if r["margin"] > 0) / max(1, len(s)), len(s)


def clusters(rs, man):
    by = {}
    for r, m in zip(rs, man):
        if m["flip"] == 1:
            by.setdefault(m["p"], []).append(1 if r["margin"] > 0 else 0)
    return sum(1 for v in by.values() if sum(v) * 2 > len(v)), len(by)


def gate_a_l(man):
    print("\n[G-A'] 창 유효성 — ① 확신행 무관용(잡음모형) · ② |Δacc| ≤%.2f" % BAR_GA_ACC)
    ok_a = ok_l = True
    for s in SEEDS:
        a, b = rows("ga_seen_nostore_w64_%s.json" % s), rows("ga_seen_nostore_w128_%s.json" % s)
        if not a or not b:
            print("  %-9s (pending)" % s)
            return None, None
        idx = scored_idx(man)
        band = st.quantiles([abs(a[i]["margin"]) for i in idx], n=BAND_Q)[0]
        flips = [i for i in idx if (a[i]["margin"] > 0) != (b[i]["margin"] > 0)]
        conf = [i for i in flips
                if abs(a[i]["margin"]) > band and abs(b[i]["margin"]) > band]
        f64, n1 = acc(a, man, 1)
        f128, _ = acc(b, man, 1)
        c1 = len(conf) == 0
        c2 = abs(f64 - f128) <= BAR_GA_ACC
        ok_a &= c1 and c2
        print("  %-9s 잡음대역 B=%.3f · 반전 %d행 중 **확신행 반전 %d행** %s · flip1 %.3f→%.3f "
              "(Δ=%.3f) %s"
              % (s, band, len(flips), len(conf), "✅" if c1 else "❌",
                 f64, f128, abs(f64 - f128), "✅" if c2 else "❌"))
    print("  => G-A' %s" % ("PASS — 창은 판정을 움직이지 않는다" if ok_a else "FAIL — 발사 금지"))

    print("\n[G-L] liveness — 바닥 %.3f = G-D 판정 bar 그 자체 (유도 · 관측값 아님)" % BAR_GL)
    print("      계기가 통달 원자에서조차 판정 bar 에 못 닿으면 nonce/held-out 에선 결코 못 닿는다")
    for s in SEEDS:
        b = rows("ga_seen_nostore_w128_%s.json" % s)
        f, n = acc(b, man, 1)
        p = f >= BAR_GL
        ok_l &= p
        print("  %-9s SEEN no-demo flip1@128 = %.4f (n=%d · bar %.3f)  %s"
              % (s, f, n, BAR_GL, "PASS" if p else "FAIL"))
    print("  => G-L %s" % ("PASS — 계기가 판정을 실어 나를 수 있다" if ok_l else "FAIL"))
    return ok_a, ok_l


def gate_b(man):
    print("\n[G-B] 포맷 판독성 (바이트 이월) — 2-연접 시연을 모델이 읽는가 · bar %.2f" % BAR_GB)
    ok = True
    for s in SEEDS:
        rs = rows("gb_seen_matched_%s.json" % s)
        if not rs:
            print("  %-9s (pending)" % s)
            return None
        f1, n1 = acc(rs, man, 1)
        f0, n0 = acc(rs, man, 0, forms=("int1", "int2"))
        d = load("gb_seen_matched_%s.json" % s)["splits"]["heldout"]["summary"]
        clean = d.get("consult_dropped", 0) == 0
        p = f1 >= BAR_GB and f0 >= BAR_GB and clean
        ok &= p
        print("  %-9s flip1=%.4f (n=%d) · flip0(int)=%.4f (n=%d) · byte-audit %s  →  %s"
              % (s, f1, n1, f0, n0, "clean" if clean else "DROPPED>0 ⛔",
                 "PASS" if p else "FAIL"))
    print("  => G-B %s" % ("PASS — nonce 발사 허가" if ok else
                           "FAIL — INVALID-FORMAT · few-shot 1회 → DECON-W"))
    return ok


def gate_d(man_nonce):
    print("\n[G-D] PC-NONCE-240 (바이트 이월) — READ ≥%.2f · CONSUME ≥%d/240 · BIND"
          % (BAR_READ, BAR_CONSUME_NONCE))
    res = {}
    for s in SEEDS:
        m = rows("gd_nonce_matched_%s.json" % s)
        x = rows("gd_nonce_mismatch_%s.json" % s)
        if not m:
            print("  %-9s (pending)" % s)
            return None
        read, nr = acc(m, man_nonce, 0, forms=("int1", "int2"))
        c, nc = clusters(m, man_nonce)
        bind = None
        if x:
            bm, _ = acc(m, man_nonce, 1)
            bx, _ = acc(x, man_nonce, 1)
            bind = bm - bx
        res[s] = {"read": read, "clusters": c, "n_cluster": nc, "bind": bind}
        print("  %-9s READ=%.4f (n=%d) %s · CONSUME=%d/%d %s%s"
              % (s, read, nr, "✅" if read >= BAR_READ else "⛔",
                 c, nc, "PASS" if c >= BAR_CONSUME_NONCE else "FAIL",
                 "" if bind is None else " · BIND(M−X)=%+.4f" % bind))
    return res


def main():
    man = json.load(open(os.path.join(HERE, "man_seen.json")))["heldout"]
    man_nonce = json.load(open(os.path.join(HERE, "man_nonce.json")))["heldout"]
    out = {"hypothesis": "H_9312"}

    print("=" * 92)
    print("H_9312 DECON-2b — 재등록 1회. G-A 만 재건 · G-B~G-E 는 바이트 이월.")
    print("=" * 92)

    ok_a, ok_l = gate_a_l(man)
    if ok_a is None:
        print("\n[PENDING]")
        return
    if not (ok_a and ok_l):
        out["verdict"] = ("⛔ INVALID-INFRA — 재건한 게이트에서도 계기가 안 선다. 발사 금지. "
                          "**3번째 등록은 없다** — 병목은 가설이 아니라 게이트 제작 과정이다.")
        print("\nVERDICT:", out["verdict"])
        json.dump(out, open(os.path.join(HERE, "DECON2B.json"), "w"),
                  ensure_ascii=False, indent=1)
        return

    ok_b = gate_b(man)
    if ok_b is None:
        print("\n[PENDING]")
        return
    if not ok_b:
        out["verdict"] = ("⛔ INVALID-FORMAT — SEEN 원자에서조차 2-연접 시연이 읽히지 않는다. "
                          "모델이 읽는 언어가 아니다(H_9309 의 F2 와 같은 죽음). nonce·held-out "
                          "미발사 → few-shot 1회 → 그것도 낙제면 DECON-W(값을 가중치에 쓰기).")
        print("\nVERDICT:", out["verdict"])
        json.dump(out, open(os.path.join(HERE, "DECON2B.json"), "w"),
                  ensure_ascii=False, indent=1)
        return

    d = gate_d(man_nonce)
    if not d:
        print("\n[G-A'/G-L/G-B PASS] nonce 발사 허가 — G-D 대기.")
        out["gate_ok"] = True
        json.dump(out, open(os.path.join(HERE, "DECON2B.json"), "w"),
                  ensure_ascii=False, indent=1)
        return

    ok_read = all(v["read"] >= BAR_READ for v in d.values())
    ok_cons = all(v["clusters"] >= BAR_CONSUME_NONCE for v in d.values())
    if not ok_read:
        v = "⛔ INVALID-FORMAT — nonce 시연이 읽히지 않는다(READ<0.85). held-out 미발사."
    elif not ok_cons:
        v = ("🧱 EARNED 음성 — 컨텍스트 A-채널 死. 시연은 읽히는데(G-B ✅ · READ ✅) 건네준 값이 "
             "연산자에 들어가지 않는다. H_9309 와 달리 계기가 자기 양성대조를 **전부 통과한** "
             "상태이므로 이것은 INVALID 이 아니라 **벌어낸 음성**이다 — 5연속 사망 이후 첫 번째. "
             "n=240 클러스터 ⟹ TOST(Δ_eq=0.10 · N_REQ=214) 로 **cement 가능**. NEXT = DECON-W.")
    else:
        v = "🟢 G-D PASS — held-out 발사 허가 (1회 접촉 예산)."
    out["gd"] = d
    out["verdict"] = v
    print("\nVERDICT:", v)
    json.dump(out, open(os.path.join(HERE, "DECON2B.json"), "w"), ensure_ascii=False, indent=1)
    print("→ DECON2B.json")


if __name__ == "__main__":
    main()


def diagnosis():
    """G-C SEEN-LIE + the nonce copy-trivial control — DIAGNOSTICS, not gates.

    They cannot change H_9312's frozen verdict (the READ bar already fixed it at
    INVALID-FORMAT). What they do is say WHY, and the answer is not the one the gate's name
    suggests. Three independent controls, all pointing the same way:

      1. nonce + demo, flip0(int): the demo contains the gold answer VERBATIM for the very same
         stem ("이 영화 뽀길고 => 긍정.\\n이 영화 정말 뽀길고 => "). Copying alone scores 100%.
         Measured: 0.475 / 0.469 — chance. Δ vs no-demo: −0.025 / −0.017.
         The model cannot COPY from context, let alone compose.

      2. SEEN + LIE demo, flip1: a lie says "참 = 부정" when 참 is 긍정. A model that reads and
         composes must then answer 긍정 for "참지 않다" — i.e. WRONG — and flip1 must collapse
         toward 0. There is ample headroom (baseline 0.883/0.900).
         Measured: 0.900 / 0.883 — UNMOVED. The lie costs nothing because the demo is never read.

      3. And yet the demo demonstrably perturbs the trunk: |margin| shifts by a median of
         1.8-4.0. The bytes are seen. They are simply not routable as information — the same
         signature H_9309 measured (large perturbation, zero information).

    => The gate said INVALID-FORMAT. The controls say it is not the format: this byte-LM has NO
       IN-CONTEXT CONSUMPTION AT ALL. A 4-layer conv trunk has no induction/copy path, so a fact
       placed in the context cannot reach the answer no matter what language it is written in.
       G-B's flip0(int)=1.000 was parametric knowledge, not format-reading — a positive control
       the system could pass WITHOUT the mechanism under test is not a positive control.

    => The A-channel realized as CONTEXT INJECTION is structurally closed for this architecture.
       This is EARNED, not a bar artifact: the diagnosis is HARSHER than the frozen verdict (it
       closes the whole channel, not one format), and it rests on controls that should have fired
       and did not. What remains of the A-channel is DECON-W — writing the value into the weights.
    """

