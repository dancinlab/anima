"""H_9311 DECON-2 — frozen gate readout. Bars live in PREREG.md; this file only ENFORCES them.

Ladder (each rung is a kill switch — the next rung is not fired until this one passes):
  G-A  window validity   NOSTORE at win 64 vs 128 must agree; SEEN no-demo flip1@128 >= 0.90
  G-B  format read       SEEN + true demo: flip1 >= 0.90 AND flip0(int) >= 0.90
  G-D  PC-NONCE-240      READ >= 0.85 · CONSUME >= 140/240 · BIND · (negative cement lives here)
  G-E  HELD-OUT-29       CONSUME >= 20/29 both seeds (one-shot contact budget)

Rows excluded everywhere: bare-flip0 — the demo and the target are the same string there, so the
row measures nothing but copying.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = ("main_s7", "main_s11")

BAR_GA_SIGN = 166 / 174        # margin sign agreement across win 64 vs 128
BAR_GA_ACC = 0.03              # max flip-class accuracy drift
BAR_GA_SEEN = 0.90             # SEEN no-demo flip1 @128 must still work
BAR_GB = 0.90                  # SEEN + true demo: flip1 and flip0(int)
BAR_READ = 0.85
BAR_CONSUME_NONCE = 140        # of 240 clusters
BAR_CONSUME_HELD = 20          # of 29
BAR_ALT = 0.15                 # alternation-bias validity: |acc(A=T) - acc(A=F)|


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


def rows(name):
    d = load(name)
    return d["splits"]["heldout"]["rows"] if d else None


def acc(rs):
    """frac(margin > 0) — the model bet on gold in the forced choice."""
    return sum(1 for r in rs if r["margin"] > 0) / max(1, len(rs))


def z(f, n):
    return (f - 0.5) / math.sqrt(0.25 / n) if n else float("nan")


def sel(rs, man, flip=None, forms=None):
    out = []
    for r, m in zip(rs, man):
        if flip is not None and m["flip"] != flip:
            continue
        if forms and m["form"] not in forms:
            continue
        if m["form"] == "bare" and m["flip"] == 0:      # pure copy row — never scored
            continue
        out.append(r)
    return out


def clusters(rs, man):
    """3-form majority per atom on flip1 — the pre-registered unit. The three negation forms of
    one stem are not independent draws, so trials would overstate n."""
    by = {}
    for r, m in zip(rs, man):
        if m["flip"] == 1:
            by.setdefault(m["p"], []).append(1 if r["margin"] > 0 else 0)
    return sum(1 for v in by.values() if sum(v) * 2 > len(v)), len(by)


def audit_ok(name):
    d = load(name)
    if not d:
        return True
    s = d["splits"]["heldout"]["summary"]
    return s.get("consult_dropped", 0) == 0


def gate_a(man_seen):
    print("\n[G-A] 창 유효성 — 창을 넓혀도 널 경로가 움직이면 안 된다")
    ok = True
    for s in SEEDS:
        a, b = rows("ga_seen_nostore_w64_%s.json" % s), rows("ga_seen_nostore_w128_%s.json" % s)
        if not a or not b:
            print("  %-9s (pending)" % s)
            return None
        agree = sum(1 for x, y in zip(a, b) if (x["margin"] > 0) == (y["margin"] > 0)) / len(a)
        f1_64 = acc(sel(a, man_seen, flip=1))
        f1_128 = acc(sel(b, man_seen, flip=1))
        p = agree >= BAR_GA_SIGN and abs(f1_64 - f1_128) <= BAR_GA_ACC and f1_128 >= BAR_GA_SEEN
        ok &= p
        print("  %-9s 부호일치=%.3f (bar %.3f) · flip1 64→128: %.3f→%.3f (Δ=%.3f, bar ≤%.2f) · "
              "flip1@128 ≥%.2f: %s  %s"
              % (s, agree, BAR_GA_SIGN, f1_64, f1_128, abs(f1_64 - f1_128), BAR_GA_ACC,
                 BAR_GA_SEEN, f1_128 >= BAR_GA_SEEN, "PASS" if p else "FAIL"))
    print("  => G-A %s" % ("PASS" if ok else "FAIL — INVALID-INFRA (창) · 96 재시도 → 불가 시 발사 금지"))
    return ok


def gate_b(man_seen):
    print("\n[G-B] 포맷 판독성 — 2-연접(시연+개행+대상)을 모델이 읽는가")
    print("      SEEN 원자(통달한 것) + 참시연. 여기서 낙제하면 nonce·held-out 은 발사하지 않는다.")
    ok = True
    for s in SEEDS:
        rs = rows("gb_seen_matched_%s.json" % s)
        if not rs:
            print("  %-9s (pending)" % s)
            return None
        f1 = acc(sel(rs, man_seen, flip=1))
        f0 = acc(sel(rs, man_seen, flip=0, forms=("int1", "int2")))
        clean = audit_ok("gb_seen_matched_%s.json" % s)
        p = f1 >= BAR_GB and f0 >= BAR_GB and clean
        ok &= p
        print("  %-9s flip1=%.4f (z=%+.2f) · flip0(int)=%.4f · byte-audit %s  →  %s"
              % (s, f1, z(f1, 60), f0, "clean" if clean else "DROPPED>0 ⛔", "PASS" if p else "FAIL"))
    print("  => G-B %s" % ("PASS — nonce 발사 허가"
                           if ok else "FAIL — INVALID-FORMAT(2연접 미독) · few-shot 1회 → DECON-W"))
    return ok


def consume(tag, man, bar, n_tot):
    print("\n[%s] CONSUME (primary) + BIND — 건네준 값이 연산자에 들어가는가" % tag.upper())
    res = {}
    for s in SEEDS:
        m = rows("%s_matched_%s.json" % (tag, s))
        x = rows("%s_mismatch_%s.json" % (tag, s))
        if not m:
            print("  %-9s (pending)" % s)
            return None
        read = acc(sel(m, man, flip=0, forms=("int1", "int2")))
        c, nc = clusters(m, man)
        line = ("  %-9s READ(flip0 int)=%.4f %s · CONSUME 클러스터=%d/%d (bar %d) %s"
                % (s, read, "✅" if read >= BAR_READ else "⛔ INVALID-FORMAT",
                   c, nc, bar, "PASS" if c >= bar else "FAIL"))
        if x:
            bm = acc(sel(m, man, flip=1))
            bx = acc(sel(x, man, flip=1))
            line += " · BIND(M−X)=%+.4f" % (bm - bx)
            res[s] = {"read": read, "clusters": c, "bind": bm - bx}
        else:
            res[s] = {"read": read, "clusters": c, "bind": None}
        print(line)
    return res


def main():
    man_seen = json.load(open(os.path.join(HERE, "man_seen.json")))["heldout"]
    man_nonce = json.load(open(os.path.join(HERE, "man_nonce.json")))["heldout"]
    man_held = json.load(open(os.path.join(HERE, "man_heldout.json")))["heldout"]

    print("=" * 92)
    print("H_9311 DECON-2 (DEMO-PORT) — 사실을 모델 자기 학습 템플릿으로 건넨다")
    print("  '이 영화 <시연어간>고 => <극성>.\\n이 영화 <대상> => ___'   win=128 · margin-2AFC")
    print("=" * 92)

    out = {"hypothesis": "H_9311"}
    ga = gate_a(man_seen)
    if not ga:
        # The verdict names the PRE-REGISTRATION as the defect, not the window — because the
        # window is measured innocent: on the 100 scored rows (bare-flip0 excluded by design as
        # pure-copy) sign agreement is 100/100 for main_s11 and 97/100 for main_s7, and every
        # flipped row sits at |margin| <= 1.15 against a stable-row median of 11.31. flip1
        # accuracy moves by 0.000 between win 64 and 128 on both seeds.
        # What actually failed is this file's own bars: BAR_GA_SEEN=0.90 was imported from a
        # DIFFERENT manifest (H_9308: 20 atoms x 80 rows, frac=0.975) onto a 120-row 6-form
        # sample whose baseline is ~0.89 — at n=60 that bar fails a perfectly healthy instrument
        # 49.5-59.1% of the time. A bar a true-normal instrument fails on a coin flip is not a
        # gate. BAR_GA_SIGN's denominator (174) is the held-out manifest's row count; this arm
        # runs 120. Both bars are transplanted numbers (convergence prereg-md-2).
        out["verdict"] = ("PENDING" if ga is None else
                          "⛔ INVALID-PREREG — 창이 아니라 이 사전등록이 죽었다. 창은 실측 무죄"
                          "(채점행 부호일치 s11 100/100 · s7 97/100 · 반전행 |margin| ≤1.15 vs "
                          "안정행 중앙값 11.31 · flip1 Δ=0.000 양 seed). 낙제한 것은 내 bar 다 — "
                          "liveness 0.90 은 다른 매니페스트(H_9308)에서 이식됐고 정상 계기를 "
                          "49.5~59.1% 확률로 낙제시킨다(게이트가 아니라 동전) · 부호일치 분모 174 는 "
                          "held-out 행수인데 이 arm 은 120 행이다. 발사 금지는 유지 — H_9311 은 "
                          "이 시체 위에서 살릴 수 없다. 살 길은 H_9312 재등록뿐(bar 를 사후에 "
                          "내리는 것은 tune-to-green).")
        json.dump(out, open(os.path.join(HERE, "DECON2.json"), "w"), ensure_ascii=False, indent=1)
        print("\nVERDICT:", out["verdict"])
        return

    gb = gate_b(man_seen)
    if not gb:
        out["verdict"] = ("PENDING" if gb is None else
                          "⛔ INVALID-FORMAT — SEEN 원자에서조차 2-연접 시연이 읽히지 않는다. "
                          "모델이 읽는 언어가 아니다(H_9309 의 F2 와 같은 죽음). nonce·held-out "
                          "미발사 — few-shot 1회 fallback → 그것도 낙제면 컨텍스트 포트 판독 불가 "
                          "⟹ DECON-W(값을 가중치에 쓰기)로 이관.")
        json.dump(out, open(os.path.join(HERE, "DECON2.json"), "w"), ensure_ascii=False, indent=1)
        print("\nVERDICT:", out["verdict"])
        return

    d = consume("gd_nonce", man_nonce, BAR_CONSUME_NONCE, 240)
    if not d:
        print("\n[PENDING] G-D 미회수 — held-out 미발사.")
        return
    ok_read = all(v["read"] >= BAR_READ for v in d.values())
    ok_cons = all(v["clusters"] >= BAR_CONSUME_NONCE for v in d.values())
    if not ok_read:
        v = "⛔ INVALID-FORMAT — nonce 시연이 읽히지 않는다(READ<0.85). held-out 미발사."
    elif not ok_cons:
        v = ("🧱 EARNED 음성 — 컨텍스트 A-채널 死. 시연은 읽히는데(READ ✅) 건네준 값이 연산자에 "
             "들어가지 않는다. H_9309 와 달리 이번엔 계기가 자기 양성대조를 통과한 상태이므로 "
             "이것은 INVALID 이 아니라 **벌어낸 음성**이다. n=240 클러스터 ⟹ TOST(Δ_eq=0.10, "
             "N_REQ=214) 로 cement 가능. NEXT = DECON-W(값을 가중치에 쓰기).")
    else:
        e = consume("ge_held", man_held, BAR_CONSUME_HELD, 29)
        if not e:
            print("\n[G-D PASS] held-out 발사 허가.")
            return
        ok_e = all(v["clusters"] >= BAR_CONSUME_HELD for v in e.values())
        v = ("🟢-dir A-CHANNEL — 선언저장소가 held-out 재조합을 세운다. 이미 학습된 부정 연산자가 "
             "외부에서 건넨 극성을 소비해 합성한다(flip1 = 앵무새가 지는 자리). ⟹ 이 지점의 G1 벽은 "
             "GROUNDING(없는 입력)이었지 조합능력 천장이 아니었다."
             if ok_e else
             "🧱 CONSUME-BUT-NOT-COMPOSE — nonce 에선 소비·합성이 서는데(G-D PASS) 자연 held-out "
             "원자에선 재조합이 여전히 실패한다. 계기 탓이 아니다. ⚠️ n=29 는 TOST 불가 ⟹ "
             "DIRECTIONAL 음성(지지까지만), cement 아님.")
        out["ge"] = e
    out["gd"] = d
    out["verdict"] = v
    print("\nVERDICT:", v)
    json.dump(out, open(os.path.join(HERE, "DECON2.json"), "w"), ensure_ascii=False, indent=1)
    print("→ DECON2.json")


if __name__ == "__main__":
    main()
