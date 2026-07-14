"""H_9330 + H_9331 판독 — 카드에 FROZEN 된 결정표/결정트리를 코드로 못박는다.
   사후 bar 이동을 구조적으로 불가능하게 만든다 (no tune-to-green · frozen-first).

   H_9331 은 두 ckpt 계열에서 돈다:
     n2 (natem_n2_main_s7/s11)  — 원래 벽 위의 인과 시험
     C4 (swap_c4_s7/s11)        — 극성이 **연산자 자신의 키**로 쓰인 모델
                                  ⇒ H_9334 가 12/12(p=.0002)로 H-ε TERMINAL 을 낸 그 모델
   H_9334 의 예측(사전등록): 인터페이스가 addressable 이면 C4 에서 dep1 ≤ −0.50 (= P).
   S 가 나오면 그들의 12/12 는 '주소'가 아니라 재학습이 만든 다른 것 ⇒ addressable 해석 재검토.
"""
import json, os

SP = os.path.dirname(os.path.abspath(__file__))

def load(f):
    p = os.path.join(SP, f)
    return json.load(open(p)) if os.path.exists(p) else None

def bar(t):  print("\n" + "=" * 74 + "\n" + t + "\n" + "=" * 74)

bar("H_9330 — 읽는 자리 (FORM-OCCLUSION vs NO-INJECT) · 결정표 FROZEN")
tail, base = load("h9330_tail.json"), load("h9330_base.json")
if not (tail and base):
    print("  ⏳ 산출물 미도착 (h9330_tail.json / h9330_base.json)")
else:
    for nm, d in (("base (원자 자신의 자리 · AUDIT-A 재현)", base),
                  ("tail (한 칸 뒤 · 읽는 자리만 이동)", tail)):
        print("\n[%s]" % nm)
        for k in sorted(d):
            if k != "items":
                print("   %-12s %s" % (k, str(d[k])[:100]))
    dt, pt = tail.get("delta"), tail.get("p_perm")
    print("\n--- 결정표 (bar 는 카드에 동결 · 사후이동 금지) ---")
    if dt is None:
        print("  ⏳ delta 필드 없음 — 산출 json 구조를 카드와 대조할 것")
    elif dt > 0 and pt is not None and pt < 0.05:
        print("  🔓 FORM-OCCLUSION — 원자는 valence 를 넣는다. 못 읽은 건 그 바이트의 형태에")
        print("     가려진 자리에서 읽었기 때문 ⇒ 자연-창발 경로 **재개방**")
    else:
        print("  🧱 NO-INJECT 확정 — 자리를 옮겨도 없다 ⇒ 자연 분포는 valence 를 정말 안 썼다")
        print("     ⇒ H_9305 FIRE-BLOCKED cement · 자연-창발 CLOSED")

def read_bl(tag, f7, f11, note):
    bar("H_9331 BIND-LOCUS %s — P / S · 결정트리 FROZEN (V1→V2→V3→DV · 양 seed 부호일치 필수)" % tag)
    print("  " + note)
    s7, s11 = load(f7), load(f11)
    if not (s7 and s11):
        print("\n  ⏳ 산출물 미도착 (%s / %s)" % (f7, f11))
        for nm, d in (("s7", s7), ("s11", s11)):
            if d: print("   [%s] verdict=%s · l*=%s" % (nm, d.get("verdict"), d.get("lstar")))
        return None
    for nm, d in (("s7", s7), ("s11", s11)):
        print("\n[seed %s]  verdict: %s · l*: %s" % (nm, d.get("verdict"), d.get("lstar")))
        for a, v in (d.get("arms") or {}).items():
            dep, se = v.get("dep"), v.get("se")
            print("   %-16s n=%-4s dep=%s se=%s" % (
                a, v.get("n"),
                ("%+.4f" % dep) if isinstance(dep, float) else dep,
                ("%.4f" % se) if isinstance(se, float) else se))
    d7 = (s7.get("arms") or {}).get("B_novel_flip1", {}).get("dep")
    d11 = (s11.get("arms") or {}).get("B_novel_flip1", {}).get("dep")
    print("\n--- 양 seed 일치 (확정의 필요조건) ---")
    if d7 is None or d11 is None:
        print("  ⏳ dep1 없음"); return None
    if (d7 < 0) != (d11 < 0):
        print("  ❌ 부호 불일치 (s7=%+.4f · s11=%+.4f) — **확정 금지** (seed 잡음)" % (d7, d11))
        return None
    print("  ✅ 부호 일치 (dep1: s7=%+.4f · s11=%+.4f)" % (d7, d11))
    print("  verdict: s7=%s | s11=%s" % (s7.get("verdict"), s11.get("verdict")))
    return (d7 + d11) / 2.0

read_bl("[n2 ckpt · 원래 벽]", "bl_s7.json", "bl_s11.json",
        "극성이 CPT 로 심겼으나 연산자가 조회하지 않는 모델(H_9327 의 벽).")

m = read_bl("[C4 ckpt · 연산자 자신의 키]", "bl_c4_s7.json", "bl_c4_s11.json",
            "H_9334 가 12/12(p=.0002)로 H-ε TERMINAL 을 낸 모델 — 극성이 연산자 자신의 키로 쓰였다.")

if m is not None:
    bar("H_9334 예측 시험 (사전등록 · C4 · 읽기 축)")
    print("  H_9334 (쓰기 축): 인터페이스 addressable ⇒ 읽기-자리 주입에 답이 따라와야 한다")
    print("  ⇒ 사전등록 예측: dep1 ≤ −0.50 (P)")
    print("  측정: dep1 (양 seed 평균) = %+.4f" % m)
    if m <= -0.50:
        print("\n  🟢 P — 확증. 연산자는 자기 읽는 자리의 내용을 소비한다.")
        print("     ⇒ H_9334 의 addressable 을 **읽기 축에서 독립 확증** (같은 주장, 다른 축)")
    elif abs(m) <= 0.20:
        print("\n  🧱 S — **반증**. 올바른 자리·올바른 키인데도 무시한다.")
        print("     ⇒ H_9334 의 12/12 는 '주소'가 아니라 **재학습이 만든 다른 것**이 한 일")
        print("     ⇒ **addressable 해석 자체가 재검토**된다")
    else:
        print("\n  ⏳ UNDERPOWERED — P bar(−0.50)와 TOST 마진(±0.20) 사이. n 증설, **bar 이동 없음**")
