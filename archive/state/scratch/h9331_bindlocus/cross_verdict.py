"""H_9331 KO×EN 교차 판정 결합기 — 두 레인의 결과를 **결과 도착 前 동결된** 진리표로 합친다.

  왜 필요한가: #3620 은 "KO 단독 cement 금지 · 종결은 KO×EN 교차서만" 을 **산문**으로만 착륙시켰다.
  두 결과가 나온 뒤 눈대중으로 합치면 그게 self-judge(p7 위반)다. 이 파일은 그 합산 규칙을
  **결과가 존재하기 전에** 코드로 못박아, 사후에 진리표를 못 움직이게 한다 (frozen-first).

  두 레인 (서로 다른 계기 · 공유하는 것은 오직 '존재 질문' = CPT 로 쓴 극성이 연산자에 조회되는가):
    KO  BIND-LOCUS (H_9331 · 내 레인)  — 인과 주입. dep1 = P(ans=pos|inject=pos)−P(ans=pos|inject=neg).
                                          연산자 `지 않다` 는 **접미사** ⇒ 캐리어 마지막 바이트에 답이
                                          그대로 있어, attention-free conv 가 '되뇜'만으로 12/12 가능
                                          ⇒ KO 에서 '읽음' vs '되뇜' **판별 불가** (KO 단독 cement 금지).
    EN  HO-CARRIER (H_9347 · 병렬세션)  — `not X` 자유·전치(`certainly not {s}` 코퍼스 0회) ⇒ 접미사
                                          되뇜 채널이 **존재하지 않는** 형태론. '읽음' vs '되뇜' 판별함.

  ⚠️ 판정 무결(§실패모드): 사람이 enum 을 손으로 타이핑하지 못한다.
    · KO enum 은 **동결 bar** 로 dep1 에서 기계 도출 (read_verdict.py 와 같은 bar).
    · EN enum 은 병렬 레인이 emit 한 machine JSON 만 소비 (내가 재분류하지 않는다 = a_parallel_session_compare).
    · INVALID 은 사전등록 gate-ID(KI*/EI*) 를 든 결과만 허용 — 사후에 발견한 '계기 의심' 은 코드 경로가 없다.

  frozen-first 수정(양 결과 미도착 = 튜닝 아님): dep1 ≥ +0.50 을 else-bucket(UNDERPOWERED)에 묻지 않고
  **ECHO** 로 분리한다. dep1=+0.9 는 잡음이 아니라 되뇜 채널이 **직접 관측된** 가장 정보량 큰 결과다
  (prereg-table-must-cover-below-chance · '우연 아래는 발견'). ECHO 는 표 17~19 를 연다.
"""
import json, os

SP = os.path.dirname(os.path.abspath(__file__))

# ── 동결 bar (read_verdict.py 와 동일 · 사후이동 금지) ─────────────────────────
P_BAR    = -0.50   # dep1 ≤ P_BAR              → P    (연산자가 주입된 극성을 읽는다)
S_TOST   =  0.20   # |dep1| ≤ S_TOST (TOST)     → S    (의존성 없음 = 저장소 도달불가)
ECHO_BAR = +0.50   # dep1 ≥ ECHO_BAR            → ECHO (주입 내용이 변환 없이 출력경로 도달 = 되뇜 직접관측)
# KO INVALID 은 아래 gate-ID 로만 (그 외 어떤 이유도 INVALID 을 만들 수 없다):
KO_GATES = {"KI1", "KI2", "KI3", "KI4", "KI5"}
#   KI1 Stage-A 양성대조 실패(ℓ* 인과적 미확보) · KI2 주입 dead(readout 미소비) ·
#   KI3 sham/randdir 팔이 bar 초과 · KI4 팔 누락/JSON 파손 · KI5 디코드 비결정/device-parity 실패
# 엔진(cli/evaluate.py bind_locus_run)이 실제로 emit 하는 verdict 문자열 → gate 매핑 (reference-match):
KO_INVALID_VERDICTS = {
    "INVALID-LOCALIZATION":   "KI1",   # V1 실패: SEEN swap 이 답을 안 뒤집음 (ℓ* 미확보)
    "INVALID-DEAD-INJECTION": "KI2",   # V2 실패: 주입이 readout 에 소비 안 됨
    "INVALID-INSTRUMENT":     "KI3",   # V3 실패: sham/randdir 팔이 bar 초과
}


def load(f):
    p = os.path.join(SP, f)
    return json.load(open(p)) if os.path.exists(p) else None


def bar(t):  print("\n" + "=" * 74 + "\n" + t + "\n" + "=" * 74)


def ko_enum(s7, s11):
    """KO 레인 → {P, S, ECHO, UNDERPOWERED, INVALID}. 동결 bar 에서 기계 도출."""
    if not (s7 and s11):
        return "PENDING", "산출물 미도착 (bl_c4_s7.json / bl_c4_s11.json)"
    # ① 엔진이 emit 한 verdict 문자열이 1순위 (reference-match · 실제 bind_locus_run 출력)
    for nm, d in (("s7", s7), ("s11", s11)):
        v = d.get("verdict")
        if isinstance(v, str) and v.startswith("INVALID"):
            g = KO_INVALID_VERDICTS.get(v)
            if g in KO_GATES:
                return "INVALID", "%s 엔진 verdict=%s → gate=%s (V-gate 실패 · P/S 금지)" % (nm, v, g)
            return "INVALID", "%s 엔진 verdict=%s (미등록 INVALID 종류 → KI4 격리)" % (nm, v)
    # ② (예비) 명시적 invalid_gate 필드도 존중
    for nm, d in (("s7", s7), ("s11", s11)):
        g = d.get("invalid_gate")
        if g is not None:
            return "INVALID", "%s invalid_gate=%s%s" % (nm, g, "" if g in KO_GATES else " (KI* 밖 → 격리)")
    d7 = (s7.get("arms") or {}).get("B_novel_flip1", {}).get("dep")
    d11 = (s11.get("arms") or {}).get("B_novel_flip1", {}).get("dep")
    if d7 is None or d11 is None:
        return "INVALID", "dep1 필드 없음 = KI4(팔 누락/JSON 파손)"
    # 양 seed 부호일치 = 확정의 필요조건 (seed-agreement-on-pooled-feature)
    def cls(x):
        if x <= P_BAR:      return "P"
        if x >= ECHO_BAR:   return "ECHO"
        if abs(x) <= S_TOST: return "S"
        return "UNDERPOWERED"
    c7, c11 = cls(d7), cls(d11)
    detail = "dep1 s7=%+.4f→%s · s11=%+.4f→%s" % (d7, c7, d11, c11)
    if c7 != c11:
        return "UNDERPOWERED", detail + " · seed 불일치 ⇒ 확정 금지(잡음)"
    return c7, detail


def en_enum(en):
    """EN 레인(H_9347) → {POS, NEG, UNDERPOWERED, INVALID}. 병렬 레인이 emit 한 enum 만 소비."""
    if not en:
        return "PENDING", "산출물 미도착 (en_verdict.json · H_9347 병렬세션)"
    e = en.get("enum")
    if e in ("POS", "NEG", "UNDERPOWERED"):
        return e, "H_9347 machine enum=%s" % e
    if e == "INVALID":
        g = en.get("invalid_gate")
        return "INVALID", "H_9347 INVALID · gate=%s" % g
    return "INVALID", "en_verdict.json 에 유효 enum 없음(=%r) — 계기결함 격리" % e


# ── 진리표 (Fable 설계 · cell-by-cell 그대로 · 결과 前 동결) ──────────────────────
# key = (KO, EN) → (cross_verdict, tier, 근거/조치)
TIER_T, TIER_D, TIER_N = "TERMINAL", "DIRECTIONAL", "—"
TABLE = {
    # 1..16 기본
    ("P", "POS"):          ("INTERFACE-ADDRESSABLE-CONFIRMED", TIER_T,
                            "인공물-무관 일치: EN 자유어순은 KO 접미사-되뇜을 못 담고, EN 스크리너 모호는 KO 인과주입(양seed·D/E팔)을 못 건드림. 유일 대안=두 독립 인공물이 우연히 부호 일치. 범위=존재 주장만(§scope)."),
    ("P", "NEG"):          ("MORPHOLOGY-ARTIFACT", TIER_D,
                            "KO=P 는 자기 confound 로 veto(되뇜은 구조상 12/12 생성). 재개방(사전등록): continuation-severed 캐리어(답≠마지막바이트)서 dep1≤−0.50 이면 reopen."),
    ("P", "UNDERPOWERED"): ("UNDERPOWERED", TIER_N, "KO=P 단독 cement 불가(읽음/되뇜 판별불가). 방향주석=addressable. 조치: EN n 증설."),
    ("P", "INVALID"):      ("UNDERPOWERED", TIER_N, "위와 동일 + EN 계기수리(EIx 명시)."),
    ("S", "POS"):          ("DISCORDANT-REOPEN", TIER_N,
                            "전역 부호 반대인 두 산 설명 모두 배제불가(veto 불가): (a)진짜 형태론-국한 벽 vs (b)KO Stage-A 오위치. 판별자(사전등록): H_9331 주입계기를 EN 형태론에 이식(단일요인)."),
    ("S", "NEG"):          ("STORAGE-UNREACHABLE", TIER_T,
                            "두 인터페이스가 일치 실패: 인과검증된 읽기자리 강제주입(TOST·양seed) AND 자연 confound-free 트리거쓰기 모두 무의존. 재개방=진짜 새 인터페이스 계급=새 H."),
    ("S", "UNDERPOWERED"): ("UNDERPOWERED", TIER_N, "방향주석=unreachable. EN 재발사."),
    ("S", "INVALID"):      ("UNDERPOWERED", TIER_N, "방향주석=unreachable. EN 수리(EIx)+재발사."),
    ("UNDERPOWERED", "POS"): ("INTERFACE-ADDRESSABLE-CONFIRMED", TIER_D,
                            "스크리너급 양성: EN 에서 진짜 confound-free 읽기이나 형태론+base+캐리어 동시이동. 인과 교차 위해 KO 재발사."),
    ("UNDERPOWERED", "NEG"): ("MORPHOLOGY-ARTIFACT", TIER_D,
                            "H_9334 자연-읽기 주장이 confound-free 재현 실패. 주입 하위질문은 열림. KO 재발사."),
    ("UNDERPOWERED", "UNDERPOWERED"): ("UNDERPOWERED", TIER_N, "둘 다 재발사. 방향주석 불허."),
    ("UNDERPOWERED", "INVALID"): ("UNDERPOWERED", TIER_N, "EN 수리(EIx), 둘 다 재발사."),
    ("INVALID", "POS"):    ("INTERFACE-ADDRESSABLE-CONFIRMED", TIER_D, "9번과 동일 + KO 수리 플래그(KIx)."),
    ("INVALID", "NEG"):    ("MORPHOLOGY-ARTIFACT", TIER_D, "10번과 동일 + KO 수리 플래그(KIx)."),
    ("INVALID", "UNDERPOWERED"): ("UNDERPOWERED", TIER_N, "KO 수리, 둘 다 재발사."),
    ("INVALID", "INVALID"): ("INVALID", TIER_N, "측정 자체가 없음. 방향읽기 불허 — INVALID 은 약한 증거가 아니라 증거 0."),
    # 17..19 ECHO (수정 채택 시)
    ("ECHO", "POS"):       ("DISCORDANT-REOPEN", TIER_N,
                            "KO 채널이 continuation 으로 측정(주입이 변환없이 출력도달)되고 EN 읽기는 진짜 ⇒ addressability 는 EN-국한. 실격은 KO 기질이 아니라 KO 계기. 판별자: EN-측 주입 이식."),
    ("ECHO", "NEG"):       ("MORPHOLOGY-ARTIFACT", TIER_T,
                            "가용한 가장 강한 인공물 판정: continuation 기제가 **직접 관측**(추론아님) AND confound-free 레인이 음성. 진짜 읽기가 숨을 곳이 없다."),
    ("ECHO", "UNDERPOWERED"): ("UNDERPOWERED", TIER_N, "방향주석=인공물. EN 재발사/수리."),
    ("ECHO", "INVALID"):   ("UNDERPOWERED", TIER_N, "방향주석=인공물. EN 재발사/수리."),
}

# ── scope clause (tier 규칙의 일부 · 어느 셀에서도 얻지 못하는 것) ─────────────────
SCOPE = ("TERMINAL 은 공유 존재주장에만 붙는다 — '303M 에서 CPT 로 쓴 극성이 연산자에 조회되는가'. "
         "이 교차가 결코 벌지 못하는 것: (a) 요인귀속(형태론 vs base vs 캐리어 중 무엇이 레버 — EN 은 셋 다 이동) "
         "(b) 'KO 자연경로가 고쳐졌다'(셀1은 KO 벽이 인터페이스 事實임을 보일 뿐, 자연 디코드서 고쳐졌음이 아님). 둘 다 별개 H.")


def cross(ko, en):
    """순수함수: 두 enum → (cross_verdict, tier, 근거). 둘 다 있기 전엔 PENDING."""
    if ko == "PENDING" or en == "PENDING":
        return "PENDING", TIER_N, "두 레인 모두 도착해야 판정 (한 레인만 보고 분류 금지 = 상호 절연)"
    return TABLE.get((ko, en), ("TABLE-MISS", TIER_N, "표에 없는 (%s,%s) — 코드/입력 대조" % (ko, en)))


if __name__ == "__main__":
    bar("H_9331 KO×EN 교차 판정 — 진리표 FROZEN (결과 前 동결 · 사후 bar/셀 이동 금지)")
    ko, ko_d = ko_enum(load("bl_c4_s7.json"), load("bl_c4_s11.json"))
    en, en_d = en_enum(load("en_verdict.json"))
    print("\n[KO BIND-LOCUS (C4 · H_9331)]  enum=%s" % ko)
    print("   " + ko_d)
    print("\n[EN HO-CARRIER (H_9347 · 병렬)]  enum=%s" % en)
    print("   " + en_d)
    v, tier, why = cross(ko, en)
    bar("교차 판정")
    print("  cross_verdict : %s" % v)
    print("  tier          : %s" % tier)
    print("  근거          : %s" % why)
    print("\n  scope: " + SCOPE)
    if tier == TIER_T:
        print("\n  🟢🟢 TERMINAL — 두 레인 결정적·일치·어느 confound 로도 재현불가. 존재주장 cement.")
    elif tier == TIER_D:
        print("\n  🟡 DIRECTIONAL — 한 레인만 결정적. 교차 재발사로 TERMINAL 추구.")
    elif v == "DISCORDANT-REOPEN":
        print("\n  🔀 DISCORDANT-REOPEN — 실질 판정 emit 거부. 사전등록 판별자로만 진행.")
    else:
        print("\n  ⏳ 미확정 — bar 이동 없이 재발사/수리.")
