#!/usr/bin/env python3
# =============================================================================
# H_9274 / F2 — 4th FIRE ($0 · numpy · CPU-local · mini · OMP=2)
#
#   "재조합(merge) 대수가 정보를 더하는가?"  (H_054 symbiogenesis · H_203 asym-merge)
#
# 1차 INVALID (무-창조 supply 펌프) · 2차 INVALID (headline이 repair sink 상수 영점 위)
# 3차 INVALID (프레임 유효 위에서: health 대리정책 부호가 살아있는 repair band 안에서
#              뒤집힘 · sham 스칼라 tag가 보존적 융합에 평균사 → blind와 무구별).
#   3차 결정타: 유일 부호안정 신호 = 오라클 +13(≈7×MDE, 양 기질) ⇒ 담체 = health 아니라
#   load-공급 상보성. 오라클 health(0.807)≈blind health(0.805) = 이김은 health가 아님.
#
# ============================ 사전등록 (PRE-REGISTRATION) ======================
# 실행 전 고정. 결과를 본 뒤 상수/규약/arm/판정식/detector 를 옮기지 않는다.
#
# --- 담체 재정의 : health → load-공급 상보성(오라클의 실현가능 국소 근사) ---
#  각 유닛의 관측가능 slack_i = supply_i − load_i = (cap_i − D_i) − L_i.
#    slack < 0 = 결손(deficit, 부하>공급, stress>1) · slack > 0 = 잉여(surplus, 공급놀림).
#  헤드라인 지표 ATP = Σ min(L, S) 는 L 과 S 에 **둘 다** 의존한다. deficit(min=S,공급낭비X이나
#  잉여부하) × surplus(min=L,공급 놀고 있음) 를 융합하면 놀던 공급이 결손을 덮어 min↑ =
#  상보성. health = S/cap 는 **L 을 안 본다** → 3차에서 기질(되먹임 on/off)에 따라 상관부호가
#  뒤집혔다. slack 은 L 을 직접 포함하므로 부호가 기질에 묶이지 않을 것 = 이번 예측.
#
#  a_comp (PRIMARY) = 국소 상보성 매칭 : 가장 결손(min slack) 유닛과 가장 잉여(max slack)
#    유닛을 융합. **오직 현재 관측(L,S)만** 사용 · 모델(Λ, repair) 미사용 · 미래 solve 미사용
#    = 오라클(전상태·전모델 정상상태 최대화)의 **실현가능 국소 근사**.
#    ⚠ detector 근접성: a_comp 는 순간 min(L,S) 자체가 아니라 slack=S−L 극단만 본다(구조적
#      부하-공급 불일치). 헤드라인은 warm-window **정상상태** 시간평균이고 그 사이 damage/repair
#      동역학이 개입 → myopic slack 정책이 정상상태 ATP 를 부호안정하게 올리는지는 열린 질문.
#
# --- sham 재설계 : 스칼라 tag 금지(3차 평균사). 범주 라벨 + 다수/대형모 상속(평균 아님) ---
#  각 유닛 categorical tag ∈ {0..K−1}(K=5) init 균등. 융합 시 merged tag = **더 큰 cap 부모의
#  tag**(범주 결정 상속 · 평균 아님 → 보존적 융합을 견딤). 분열 시 자손은 부모 tag 상속.
#  a5_sham = a_comp 와 **동일 극단매칭 기계**를 tag 축에 적용 : min-tag 유닛 × max-tag 유닛.
#    tag ⊥ (L,S) 이므로 sham ATP ≈ blind ATP(무정보) 이나 **선택분포는 지속 구조화**(같은
#    tag-극단 유닛 반복 타깃) → blind(매 이벤트 균등랜덤 페어)와 분포적으로 구별.
#    (2차 교훈: 매 이벤트 uniform 재추첨 = blind 와 동치이므로 금지. 지속 = 범주 tag 만.)
#  distinctness 실측 : sham 선택쌍 |Δtag| >> blind 선택쌍 |Δtag| · corr(tag,slack)≈0(중립 arm).
#
# --- arm (전부 사전등록 · cherry-pick 방지) ---
#   c1_frozen   동역학 0
#   c2_blind    동일 예산 · 랜덤 페어링                         ← 헤드라인 통제 ①
#   a5_sham     동일 극단매칭 기계 · tag(무정보·지속) 축         ← 헤드라인 통제 ②
#   a_comp      ★PRIMARY — slack 상보성(deficit×surplus) · 오라클 국소근사
#   o6_oracle   상한 계측기(전모델 정상상태 최대화) — 도달범위 실재 증명용(3차 +13 재현 기대)
#   o_health    진단 — 카드 문자 "저-health 2개 fuse"(3차 a3) · **부호 뒤집힘 예상**(대조)
#   guard_off   sibling-ban/쿨다운 OFF (G2 degeneracy 진단 · comp 정책)
#
# --- 헤드라인 detector (데이터 보기 전 못박음 · 순서통계량 아님) ---
#   HEADLINE = a_comp − c2_blind  AND  a_comp − a5_sham,
#     warm-window mean ATP, **control별 paired-t**, 요구:
#       두 기질(HET·LIVE) 모두에서 mean>MARGIN·p<ALPHA(동일부호 양성)  AND
#       sign-sweep 전 축(repair live band · sigma · capsplit · rho · frag_sigma · [LIVE]EXC·B1)
#       모든 점에서 두 통제 대비 부호가 양성 보존.
#   한 점에서라도 부호가 뒤집히면 = 좌표(모델 산물) = INVALID (규칙⑥, 설계 내장 PASS 조건).
#   min/max/Δ=exp−max(controls) 등 순서통계량 detector 미사용(규칙①⑤).
#
# --- 사전 예측 (실행 전 기록) ---
#   slack 은 L 을 포함 → 상보성 이득이 기질(되먹임)과 무관하게 min(L,S) 를 올린다
#   ⇒ 예측: a_comp > 0 이 **양 기질·전 repair band 부호안정**(health 는 뒤집힘). o_health 뒤집힘.
#   만약 a_comp 도 뒤집히면 = 실현가능 국소 근사조차 regime-bound = 담체가 국소관측으로
#   도달불가(전상태 오라클만) = licensed 음성/KILL. tune 금지 · 한 번 발사 · 부호는 데이터가 정함.
#
# --- 3게이트 (3차 유지) ---
#  G1 ALGEBRAIC-NEUTRALITY : arm별 순간 pump ≤ 1e-9 (보존적 merge D←D_a+D_b 유일해).
#  G2 DEGENERACY           : 영구 sibling-ban + COOL=2 · self_remerge=0 실측.
#  G3 LIVE-REGIME 선등록    : CONTROL(c2)만 보고 repair 격자→살아있는 band→중앙값 선등록.
#                            V1 양쪽(하단 붕괴+상단 포화) 차단.
#  ORACLE-REACH            : o6 오라클이 blind 를 유의하게 이겨야(축이 정보 나름 · 3차 +13).
#
# --- 계측 강제규칙 7종 (3차와 동일) ---
#  ① control별 paired-t 전부 (순서통계량 detector 금지) ② SEM/paired-t 만
#  ③ 사전 MDE pilot(900–919 · main 0–19 와 disjoint) · 처치 도달 축 span · span<3×MDE→abort
#  ④ 정보채널 : a_comp DV=slack=f(L,S)(blind 안봄, var>0) · sham DV=tag(⊥slack) · sham≠blind 실측
#  ⑤ V-gate 를 헤드라인 detector(ATP) 그 자체에  ⑥ 부호보존 전 자유축 PASS 내장
#  ⑦ KILL/PASS 분기 실행가능(pilot policy-axis span>MARGIN 먼저)
#  금지: 사후 detector/변수 교체 · tune-to-green · tune-to-red.
#  seed=20 · paired-CRN · p5: emit/silence 경로 코드 부재(구조 레인 전용).
# =============================================================================

import json
import math
import os
import sys
import time

import numpy as np

# ---------------- 사전등록 상수 (3차와 동일 기질) ----------------
S = 64
N0 = 16
G = 32.0
T = 300
WARM = 150
K_EV = 2
B1 = 3.0
EXC = 2.0
D_TOTAL = 100.0
RHO = 0.85
COOL = 2
MIN_CAP_FRAC = 0.05
NOISE_K = 4.0
FRAG_BASE = 0.70
FRAG_SIGMA = 0.70
K_TAG = 5                     # sham 범주 tag 수

SEEDS = list(range(20))
PILOT_SEEDS = list(range(900, 920))

MARGIN = 1.0
ALPHA = 0.05

REPAIR_GRID = [0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30]
LIVE_LO, LIVE_HI = 0.50, 0.92
CEIL_FRAC = 0.95

OUT = os.path.dirname(os.path.abspath(__file__))
CONTROLS = ["c1_frozen", "c2_blind", "a5_sham"]
PRIMARY = "a_comp"

ARMS = {
    "c1_frozen":  (None, None),
    "c2_blind":   ("blind", "blind"),
    "a5_sham":    ("blind", "sham"),
    "a_comp":     ("blind", "comp"),
    "o6_oracle":  ("blind", "oracle"),
    "o_health":   ("blind", "health"),
    "guard_off":  ("blind", "comp"),
}
MAIN_ARMS = ("c1_frozen", "c2_blind", "a5_sham", "a_comp",
             "o6_oracle", "o_health", "guard_off")
POLICY_AXIS = ("c2_blind", "a5_sham", "a_comp", "o6_oracle", "o_health")
SWEEP_ARMS = ("c1_frozen", "c2_blind", "a5_sham", "a_comp")
GUARD_OFF = {"guard_off"}


def base_cfg(**kw):
    c = dict(rho=RHO, repair=None, sigma=1.0, capsplit="sym", B1=B1, EXC=EXC,
             feedback=True, frag_sigma=FRAG_SIGMA, merge="conservative")
    c.update(kw)
    return c


# ---------------- 기질 (3차와 동일) ----------------
def _init(rng, rho, frag_sigma, rng_t):
    d = np.exp(rng.normal(0.0, 0.6, size=S))
    d *= D_TOTAL / d.sum()
    f = FRAG_BASE * np.exp(rng.normal(0.0, frag_sigma, size=S))
    perm = rng.permutation(S)
    groups = np.array_split(perm, N0)
    C_total = D_TOTAL / rho
    owner = np.empty(S, dtype=np.int64)
    cap = np.empty(N0)
    for k, g in enumerate(groups):
        owner[g] = k
        cap[k] = C_total * d[g].sum() / D_TOTAL
    tag = rng_t.integers(0, K_TAG, size=N0)          # categorical tag
    return d, f, owner, cap, tag


def _drift(d, rng):
    ld = np.log(d) + rng.normal(0.0, 0.05, size=S)
    jump = rng.random(S) < 0.02
    nj = int(jump.sum())
    if nj:
        ld[jump] += rng.normal(0.0, 0.8, size=nj)
    d = np.exp(ld)
    d *= D_TOTAL / d.sum()
    return d


def _loads(owner, d, n):
    return np.bincount(owner, weights=d, minlength=n)[:n]


def _lam_units(owner, d, f, n):
    num = np.bincount(owner, weights=d * f, minlength=n)[:n]
    den = np.maximum(_loads(owner, d, n), 1e-12)
    return num / den


def _eq_supply(cap, Dm, L, Lam, cfg):
    """정상상태 supply 예측 (오라클 전용 · 모델 완전 사용)."""
    psi = 1.0 - math.exp(-cfg["repair"])
    Sv = np.maximum(cap - Dm, 1e-9)
    if not cfg["feedback"]:
        phi = 1.0 - np.exp(-Lam / G)
        return cap * (psi / (phi + psi))
    for _ in range(8):
        st = L / np.maximum(Sv, 1e-9)
        rate = Lam * (1.0 + cfg["B1"] * np.clip(st - 1.0, 0.0, cfg["EXC"]))
        phi = 1.0 - np.exp(-rate / G)
        Sv = cap * (psi / (phi + psi))
    return Sv


# ---------------- FISSION = 부하분산 + 손상 격리 (질량보존 · 3차와 동일 규약) ----------------
def _fission(state, aware, cfg, t, sibc):
    owner, cap, Dm, tag, sib, cool, d, f, rng = state
    n = cap.size
    cnt = np.bincount(owner, minlength=n)
    cand = np.flatnonzero(cnt >= 2)
    if cand.size == 0:
        return state, 0.0, 1
    if aware:
        L = _loads(owner, d, n)
        Sv = np.maximum(cap - Dm, 1e-9)
        i = int(cand[np.argmax((L / Sv)[cand])])
    else:
        i = int(cand[rng.integers(cand.size)])

    sites = np.flatnonzero(owner == i)
    if aware:
        order = sites[np.argsort(-d[sites])]
        a, b, sa, sb = [], [], 0.0, 0.0
        for s in order:
            if sa <= sb:
                a.append(int(s)); sa += float(d[s])
            else:
                b.append(int(s)); sb += float(d[s])
    else:
        p = rng.permutation(sites)
        h = max(1, p.size // 2)
        a, b = [int(x) for x in p[:h]], [int(x) for x in p[h:]]
    if not a or not b:
        a, b = [int(sites[0])], [int(x) for x in sites[1:]]
    a = np.array(a, dtype=np.int64); b = np.array(b, dtype=np.int64)

    C = float(cap[i])
    if cfg["capsplit"] == "sym":
        ca = 0.5 * C
    else:
        la, lb = float(d[a].sum()), float(d[b].sum())
        fr = min(max(la / max(la + lb, 1e-12), MIN_CAP_FRAC), 1.0 - MIN_CAP_FRAC)
        ca = C * fr
    cb = C - ca

    sg = cfg["sigma"]
    to_a = bool(rng.random() < 0.5)
    Dv = float(Dm[i])
    prop = Dv * ca / C
    seg = min(Dv, ca) if to_a else Dv - min(Dv, cb)
    Da = (1.0 - sg) * prop + sg * seg
    Da = min(max(Da, max(0.0, Dv - cb)), min(ca, Dv))
    Db = Dv - Da
    sup_before = C - Dv

    sibc[0] += 1
    sid = sibc[0]
    owner = owner.copy(); owner[b] = n
    cap = np.append(cap, cb);  cap[i] = ca
    Dm = np.append(Dm, Db);    Dm[i] = Da
    tag = np.append(tag, tag[i])                 # 자손 tag 상속 (범주)
    sib = np.append(sib, sid); sib[i] = sid
    cool = np.append(cool, t + COOL); cool[i] = t + COOL
    created = (ca - Da) + (cb - Db) - sup_before
    return (owner, cap, Dm, tag, sib, cool, d, f, rng), created, 0


# ---------------- FUSION (담체 = load-공급 상보성 · sham = 범주 tag 극단매칭) ----------------
def _fusion(state, policy, cfg, t, guards, diag):
    owner, cap, Dm, tag, sib, cool, d, f, rng = state
    n = cap.size
    if n < 2:
        return state, 0.0, 1
    elig = np.flatnonzero(cool <= t) if guards else np.arange(n)
    if elig.size < 2:
        return state, 0.0, 1

    L = _loads(owner, d, n)
    Sv = np.maximum(cap - Dm, 1e-9)
    slack = Sv - L                                    # >0 잉여 · <0 결손
    h = 1.0 - Dm[elig] / cap[elig]
    tg = tag[elig]
    sl = slack[elig]

    def compat(x, y):
        if not guards:
            return True
        return not (sib[x] != -1 and sib[x] == sib[y])

    i = j = -1
    if policy == "oracle":
        Lam = _lam_units(owner, d, f, n)
        Le, ce, De, Lae = L[elig], cap[elig], Dm[elig], Lam[elig]
        m = elig.size
        f0 = np.minimum(Le, _eq_supply(ce, De, Le, Lae, cfg))
        Cm = ce[:, None] + ce[None, :]
        Dmm = De[:, None] + De[None, :]
        Lm = Le[:, None] + Le[None, :]
        Laem = (Le[:, None] * Lae[:, None] + Le[None, :] * Lae[None, :]) \
            / np.maximum(Lm, 1e-12)
        fm = np.minimum(Lm, _eq_supply(Cm.ravel(), Dmm.ravel(), Lm.ravel(),
                                       Laem.ravel(), cfg).reshape(m, m))
        gain = fm - f0[:, None] - f0[None, :]
        mask = np.zeros((m, m), dtype=bool)
        for x in range(m):
            for y in range(x + 1, m):
                mask[x, y] = compat(int(elig[x]), int(elig[y]))
        gain = np.where(mask, gain, -np.inf)
        if not np.isfinite(gain).any():
            return state, 0.0, 1
        bx, by = np.unravel_index(np.argmax(gain), gain.shape)
        i, j = int(elig[bx]), int(elig[by])
    elif policy == "comp":
        # 국소 상보성: 가장 결손(min slack) × 가장 잉여(max slack) · 관측 L,S 만
        lo_ord = [int(elig[k]) for k in np.argsort(sl, kind="stable")]        # 결손 우선
        hi_ord = [int(elig[k]) for k in np.argsort(-sl, kind="stable")]       # 잉여 우선
        for x in lo_ord:
            for y in hi_ord:
                if x != y and compat(x, y):
                    i, j = x, y
                    break
            if i != -1:
                break
        if i == -1:
            return state, 0.0, 1
    elif policy == "sham":
        # 동일 극단매칭 기계 · tag(무정보·지속) 축: min-tag × max-tag
        lo_ord = [int(elig[k]) for k in np.argsort(tg, kind="stable")]
        hi_ord = [int(elig[k]) for k in np.argsort(-tg, kind="stable")]
        for x in lo_ord:
            for y in hi_ord:
                if x != y and compat(x, y):
                    i, j = x, y
                    break
            if i != -1:
                break
        if i == -1:
            return state, 0.0, 1
    elif policy == "health":
        order = [int(elig[k]) for k in np.argsort(h, kind="stable")]          # 저-health 2개
        i = order[0]
        for c in order[1:]:
            if compat(i, c):
                j = c
                break
        if j == -1:
            return state, 0.0, 1
    else:  # blind
        order = [int(elig[k]) for k in rng.permutation(elig.size)]
        i = order[0]
        for c in order[1:]:
            if compat(i, c):
                j = c
                break
        if j == -1:
            return state, 0.0, 1

    if diag is not None:
        diag["n_fuse"] += 1
        diag["self_remerge"] += 1.0 if (sib[i] != -1 and sib[i] == sib[j]) else 0.0
        # 정보채널 진단
        si, sj = float(slack[i]), float(slack[j])
        diag["slack_gap_sel"].append(abs(si - sj))        # comp 선택 극단성
        diag["slack_pop_std"].append(float(sl.std()))
        diag["tag_gap_sel"].append(abs(float(tag[i]) - float(tag[j])))  # sham/blind 구별
        diag["corr_ts"].append((tg.astype(float).copy(), sl.copy()))    # tag ⊥ slack

    lo, hi = (i, j) if i < j else (j, i)
    sup_before = (cap[lo] - Dm[lo]) + (cap[hi] - Dm[hi])
    owner = owner.copy()
    owner[owner == hi] = lo
    owner[owner > hi] -= 1
    cap = cap.copy(); Dm = Dm.copy(); tag = tag.copy()
    sib = sib.copy(); cool = cool.copy()
    clo, chi = float(cap[lo]), float(cap[hi])
    # 범주 tag 상속 : 더 큰 cap 부모 (평균 아님 → 보존적 융합 견딤)
    tag[lo] = tag[lo] if clo >= chi else tag[hi]
    if cfg["merge"] == "conservative":               # G1 강제
        cap[lo] += cap[hi]; Dm[lo] += Dm[hi]
    else:                                            # D1 진단(G1 위반)
        cnew = clo + chi
        hnew = 0.5 * ((1 - Dm[lo] / clo) + (1 - Dm[hi] / chi))
        cap[lo] = cnew; Dm[lo] = cnew * (1 - hnew)
    sib[lo] = -1; cool[lo] = -1
    keep = np.arange(cap.size) != hi
    cap, Dm, tag = cap[keep], Dm[keep], tag[keep]
    sib, cool = sib[keep], cool[keep]
    created = (cap[lo] - Dm[lo]) - sup_before
    return (owner, cap, Dm, tag, sib, cool, d, f, rng), float(created), 0


# ---------------- 한 run ----------------
def simulate(seed, arm, cfg):
    fis, fus = ARMS[arm]
    dyn = fis is not None
    guards = arm not in GUARD_OFF

    rng_d = np.random.default_rng(10_000 + seed)
    rng_a = np.random.default_rng(90_000 + seed)
    rng_x = np.random.default_rng(70_000 + seed)
    rng_t = np.random.default_rng(50_000 + seed)

    d, f, owner, cap, tag = _init(rng_d, cfg["rho"], cfg["frag_sigma"], rng_t)
    Dm = np.zeros(N0)
    sib = np.full(N0, -1, dtype=np.int64)
    cool = np.full(N0, -1, dtype=np.int64)
    st = (owner, cap, Dm, tag, sib, cool, d, f, rng_a)
    sibc = [0]
    diag = {"n_fuse": 0, "self_remerge": 0.0, "slack_gap_sel": [],
            "slack_pop_std": [], "tag_gap_sel": [], "corr_ts": []}
    pump = 0.0
    atp, hh, sup, ovl, chn = [], [], [], [], []
    same_prev = None
    iu = np.triu_indices(S, 1)

    for t in range(T):
        d = _drift(d, rng_d)
        owner, cap, Dm, tag, sib, cool = st[0], st[1], st[2], st[3], st[4], st[5]
        st = (owner, cap, Dm, tag, sib, cool, d, f, rng_a)
        if dyn:
            for _ in range(K_EV):
                st, cr, _ = _fission(st, fis == "aware", cfg, t, sibc)
                pump += cr
                st, cr, _ = _fusion(st, fus, cfg, t, guards,
                                    diag if t >= WARM else None)
                pump += cr

        owner, cap, Dm, tag, sib, cool = st[0], st[1], st[2], st[3], st[4], st[5]
        n = cap.size
        L = _loads(owner, d, n)
        Sv = cap - Dm
        atp.append(float(np.minimum(L, Sv).sum()))
        sup.append(float(Sv.sum()))
        hh.append(float(Sv.sum() / max(cap.sum(), 1e-9)))
        stress = L / np.maximum(Sv, 1e-9)
        ovl.append(float((stress > 1.0).mean()))

        same = owner[:, None] == owner[None, :]
        if same_prev is not None:
            chn.append(float((same_prev[iu] != same[iu]).mean()))
        else:
            chn.append(0.0)
        same_prev = same

        Lam = _lam_units(owner, d, f, n)
        rate = Lam * (1.0 + cfg["B1"] * np.clip(stress - 1.0, 0.0, cfg["EXC"])) \
            if cfg["feedback"] else Lam
        ux = rng_x.gamma(NOISE_K, 1.0 / NOISE_K, size=n)
        uy = rng_x.gamma(NOISE_K, 1.0 / NOISE_K, size=n)
        Dm = Dm + (cap - Dm) * (1.0 - np.exp(-rate * ux / G)) \
            - Dm * (1.0 - np.exp(-cfg["repair"] * uy))
        Dm = np.clip(Dm, 0.0, cap)
        st = (owner, cap, Dm, tag, sib, cool, d, f, rng_a)

    w = slice(WARM, T)
    mm = lambda v: float(np.mean(v)) if len(v) else 0.0
    # tag ⊥ slack 상관 (선택 시점 전체 pool)
    if diag["corr_ts"]:
        tv = np.concatenate([x[0] for x in diag["corr_ts"]])
        sv = np.concatenate([x[1] for x in diag["corr_ts"]])
        cts = float(np.corrcoef(tv, sv)[0, 1]) if tv.std() > 1e-9 and sv.std() > 1e-9 else 0.0
    else:
        cts = 0.0
    # comp 선택 극단성 : 선택쌍 slack-gap 이 pop-std 대비 큰가 (정보채널 var>0)
    sgs = mm(diag["slack_gap_sel"]); sps = mm(diag["slack_pop_std"])
    return dict(
        atp=float(np.mean(atp[w])), health=float(np.mean(hh[w])),
        supply=float(np.mean(sup[w])), overload=float(np.mean(ovl[w])),
        churn=float(np.mean(chn[w])),
        self_remerge=(diag["self_remerge"] / diag["n_fuse"]) if diag["n_fuse"] else 0.0,
        slack_gap_sel=sgs, slack_pop_std=sps,
        slack_sel_ratio=(sgs / sps) if sps > 1e-9 else 0.0,
        tag_gap_sel=mm(diag["tag_gap_sel"]), corr_tag_slack=cts,
        pump=float(pump), n_units=int(st[1].size),
        cap_dev=float(abs(st[1].sum() - D_TOTAL / cfg["rho"])),
    )


# ---------------- 통계 ----------------
def t_sf(tv, df):
    tv = abs(float(tv))
    if tv > 60:
        return 0.0
    x = np.linspace(tv, tv + 400.0, 40001)
    lg = math.lgamma((df + 1) / 2) - 0.5 * math.log(df * math.pi) - math.lgamma(df / 2)
    pdf = np.exp(lg - ((df + 1) / 2) * np.log1p(x * x / df))
    return float(np.trapezoid(pdf, x)) if hasattr(np, "trapezoid") else float(np.trapz(pdf, x))


def paired(e, c):
    dv = np.asarray(e) - np.asarray(c)
    n = dv.size
    m = float(dv.mean()); sd = float(dv.std(ddof=1))
    sem = sd / math.sqrt(n)
    tv = m / sem if sem > 0 else 0.0
    return {"mean": m, "sem": sem, "t": float(tv), "p": 2.0 * t_sf(tv, n - 1),
            "pos": int((dv > 0).sum()), "n": n}


def grid(seeds, cfg, arms):
    out = {}
    for a in arms:
        per = [simulate(s, a, cfg) for s in seeds]
        g = {"atp_per_seed": [p["atp"] for p in per]}
        for k in ("atp", "health", "supply", "overload", "churn", "self_remerge",
                  "slack_gap_sel", "slack_pop_std", "slack_sel_ratio",
                  "tag_gap_sel", "corr_tag_slack", "pump", "cap_dev"):
            v = np.array([p[k] for p in per], dtype=float)
            g[k] = float(v.mean())
        g["pump_max"] = float(max(abs(p["pump"]) for p in per))
        g["n_units"] = sorted(set(p["n_units"] for p in per))
        out[a] = g
    return out


def contrasts(gr, arm, ctrls=CONTROLS):
    o = {}
    for c in ctrls:
        if c == arm:
            continue
        o[c] = paired(gr[arm]["atp_per_seed"], gr[c]["atp_per_seed"])
    o["_pooled_mean"] = float(np.mean([o[c]["mean"] for c in o]))
    return o


# ================================ MAIN ================================
def main():
    t0 = time.time()
    R = {"prereg": {
        "question": "재조합(merge) 대수가 정보를 더하는가 (H_054 · H_203)",
        "carrier": "load-공급 상보성 slack=S−L (health 아님 · 오라클의 실현가능 국소근사)",
        "primary": PRIMARY + " = slack 상보성(deficit×surplus) 매칭",
        "headline_detector": "a_comp − c2_blind AND a_comp − a5_sham · warm mean ATP · "
                             "control별 paired-t · 두 기질 모두 mean>MARGIN·p<ALPHA · "
                             "sign-sweep 전 점 부호양성보존 (순서통계량 아님)",
        "prediction_before_run": "slack 은 L 포함 → a_comp 부호가 기질/repair 무관 양성보존 "
                                 "(health o_health 는 뒤집힘). 뒤집히면 국소근사 regime-bound.",
        "controls": CONTROLS, "margin_atp": MARGIN, "alpha": ALPHA,
        "seeds": SEEDS, "pilot_seeds": PILOT_SEEDS,
        "sham": "범주 tag(K=5) · 대형모 상속(평균금지) · 동일 극단매칭기계 · tag⊥slack · blind와 구별",
        "sign_axes": ["repair(live band)", "sigma{0,.5,1}", "capsplit{sym,load}",
                      "rho{.7,.85,1}", "frag_sigma{.5,.9}", "EXC{1,2,6}[LIVE]", "B1{1.5,3}[LIVE]"]}}

    # ===== G3 · LIVE-REGIME 선등록 (CONTROL만) — HET 기준 =====
    ceiling = D_TOTAL
    scan = {}
    for r in REPAIR_GRID:
        g = grid(SEEDS, base_cfg(repair=r, feedback=False), ("c1_frozen", "c2_blind"))
        scan[r] = {"c2_health": g["c2_blind"]["health"], "c2_atp": g["c2_blind"]["atp"]}
    live = [r for r in REPAIR_GRID
            if LIVE_LO < scan[r]["c2_health"] < LIVE_HI and scan[r]["c2_atp"] < CEIL_FRAC * ceiling]
    R["G3_live_regime"] = {"scan_controls_only": scan,
                           "rule": f"{LIVE_LO}<health(c2)<{LIVE_HI} AND atp(c2)<{CEIL_FRAC}x{ceiling}",
                           "live_band": live}
    if not live:
        R["verdict"] = {"HET": {"VERDICT": "INVALID"}, "LIVE": {"VERDICT": "INVALID"},
                        "why": "G3 실패 — 살아있는 repair 구간 없음"}
        json.dump(R, open(os.path.join(OUT, "result.json"), "w"), indent=1, ensure_ascii=False)
        print("G3 FAIL: no live band"); sys.exit(0)
    R_PRIM = live[len(live) // 2]
    R["G3_live_regime"]["primary_repair"] = R_PRIM
    print("[G3] live band =", live, " PRIMARY repair =", R_PRIM,
          " c2_health=%.3f (%.1fs)" % (scan[R_PRIM]["c2_health"], time.time() - t0))

    CFG = {"HET": base_cfg(repair=R_PRIM, feedback=False),
           "LIVE": base_cfg(repair=R_PRIM, feedback=True)}

    # ===== ③ 사전 MDE (pilot · disjoint) + abort =====
    R["power"] = {}
    abort = []
    for nm in ("HET", "LIVE"):
        pg = grid(PILOT_SEEDS, CFG[nm], POLICY_AXIS)
        sd = float((np.array(pg[PRIMARY]["atp_per_seed"])
                    - np.array(pg["a5_sham"]["atp_per_seed"])).std(ddof=1))
        mde = (2.093 + 0.861) * sd / math.sqrt(len(SEEDS))
        means = {a: pg[a]["atp"] for a in POLICY_AXIS}
        span = max(means.values()) - min(means.values())
        ok = span > 3.0 * mde
        R["power"][nm] = {"sd_pilot_comp_minus_sham": sd, "MDE": mde,
                          "policy_axis_atp_pilot": means, "reachable_span_pilot": span,
                          "span_over_MDE": span / mde, "gate": "span>3xMDE", "POWERED": bool(ok)}
        print("[MDE-%s] sd=%.3f MDE=%.3f span=%.3f (%.2fxMDE) POWERED=%s (%.1fs)"
              % (nm, sd, mde, span, span / mde, ok, time.time() - t0))
        if not ok:
            abort.append(nm)
    R["power"]["abort_substrates"] = abort

    # ===== 본 실험 (n=20 · 두 기질) =====
    R["main"] = {}
    for nm in ("HET", "LIVE"):
        g = grid(SEEDS, CFG[nm], MAIN_ARMS)
        con = {a: contrasts(g, a) for a in
               ("a_comp", "o6_oracle", "o_health", "guard_off")}
        con["o6_vs_c2"] = paired(g["o6_oracle"]["atp_per_seed"], g["c2_blind"]["atp_per_seed"])
        con["sham_vs_c2"] = paired(g["a5_sham"]["atp_per_seed"], g["c2_blind"]["atp_per_seed"])
        R["main"][nm] = {"arms": {a: {k: g[a][k] for k in
                                      ("atp", "health", "supply", "overload", "churn",
                                       "self_remerge", "slack_gap_sel", "slack_pop_std",
                                       "slack_sel_ratio", "tag_gap_sel", "corr_tag_slack",
                                       "pump", "pump_max", "cap_dev", "n_units")}
                                  for a in MAIN_ARMS},
                         "contrasts": con}
        print("[main-%s] done (%.1fs)" % (nm, time.time() - t0))

    # ===== ⑥ 부호보존 스윕 =====
    base_axes = {
        "repair": [("repair", r) for r in live],
        "sigma": [("sigma", s) for s in (0.0, 0.5, 1.0)],
        "capsplit": [("capsplit", c) for c in ("sym", "load")],
        "rho": [("rho", x) for x in (0.70, 0.85, 1.00)],
        "frag_sigma": [("frag_sigma", x) for x in (0.5, 0.9)],
    }
    live_only = {"EXC": [("EXC", x) for x in (1.0, 2.0, 6.0)],
                 "B1": [("B1", x) for x in (1.5, 3.0)]}
    R["sign_sweep"] = {}
    for nm in ("HET", "LIVE"):
        R["sign_sweep"][nm] = {}
        axes = dict(base_axes)
        if nm == "LIVE":
            axes.update(live_only)
        for ax, pts in axes.items():
            R["sign_sweep"][nm][ax] = {}
            for key, val in pts:
                cfg = dict(CFG[nm]); cfg[key] = val
                g = grid(SEEDS, cfg, SWEEP_ARMS)
                row = {"c2_health": g["c2_blind"]["health"],
                       "atp": {a: g[a]["atp"] for a in SWEEP_ARMS}}
                for c in ("a5_sham", "c2_blind"):
                    pr = paired(g[PRIMARY]["atp_per_seed"], g[c]["atp_per_seed"])
                    row["%s_vs_%s" % (PRIMARY, c)] = {k: pr[k] for k in
                                                      ("mean", "sem", "t", "p", "pos")}
                R["sign_sweep"][nm][ax]["%s=%s" % (key, val)] = row
            print("[sweep-%s] %s (%.1fs)" % (nm, ax, time.time() - t0))

    # ===== G1 진단: 융합 규약 자유도 (G1 위반 = unweighted mean) =====
    gD = grid(SEEDS[:10], base_cfg(repair=R_PRIM, feedback=False, merge="unweighted_mean"),
              ("c2_blind", PRIMARY))
    R["G1_convention_freedom_diag"] = {
        "note": "G1(supply EXACT 보존)은 merge 순간 D←D_a+D_b 유일해 강제. "
                "health 단순평균 merge = G1 위반 → 순간 pump≠0 (1차 회귀).",
        "unweighted_mean_pump_per_run": {a: gD[a]["pump"] for a in gD},
        "unweighted_mean_pump_max": {a: gD[a]["pump_max"] for a in gD}}

    # ===== 게이트 =====
    def gates_for(nm):
        M = R["main"][nm]["arms"]
        C = R["main"][nm]["contrasts"]
        g1 = max(abs(M[a]["pump_max"]) for a in MAIN_ARMS)
        sham_gap = M["a5_sham"]["tag_gap_sel"]
        blind_gap = M["c2_blind"]["tag_gap_sel"]
        corr_neutral = M["c2_blind"]["corr_tag_slack"]
        comp_ratio = M[PRIMARY]["slack_sel_ratio"]
        return {
            "G1_pump_max": g1, "G1_PASS": bool(g1 <= 1e-9),
            "G2_self_remerge_max": max(M[a]["self_remerge"] for a in MAIN_ARMS
                                       if a not in GUARD_OFF),
            "G2_guardoff_self_remerge": M["guard_off"]["self_remerge"],
            "G2_PASS": bool(max(M[a]["self_remerge"] for a in MAIN_ARMS
                                if a not in GUARD_OFF) < 1e-9),
            "G3_c2_health": M["c2_blind"]["health"], "G3_c2_atp": M["c2_blind"]["atp"],
            "G3_PASS_live_both_sided": bool(LIVE_LO < M["c2_blind"]["health"] < LIVE_HI
                                            and M["c2_blind"]["atp"] < CEIL_FRAC * ceiling),
            "V_cap_conserved": bool(max(M[a]["cap_dev"] for a in MAIN_ARMS) < 1e-6),
            "V_n_units": all(M[a]["n_units"] == [N0] for a in MAIN_ARMS),
            # 정보채널(④): comp DV=slack var>0(선택 극단성 pop-std 대비 큼)
            "V_comp_slack_sel_ratio": comp_ratio,
            # sham distinct-from-blind(⑦·규칙④): tag_gap 지속구조 vs 랜덤
            "V_sham_tag_gap": sham_gap, "V_blind_tag_gap": blind_gap,
            "V_sham_distinct_from_blind": bool(sham_gap - blind_gap > 0.30),
            # tag ⊥ slack (sham 축이 담체와 무관)
            "V_tag_slack_corr_neutral": corr_neutral,
            "V_info_PASS": bool(comp_ratio > 0.5 and abs(corr_neutral) < 0.15
                                and (sham_gap - blind_gap) > 0.30),
            "V_POWER_PASS": bool(R["power"][nm]["POWERED"]),
            "ORACLE_o6_minus_c2": C["o6_vs_c2"]["mean"], "ORACLE_p": C["o6_vs_c2"]["p"],
            "ORACLE_VALID": bool(C["o6_vs_c2"]["mean"] > 0 and C["o6_vs_c2"]["p"] < ALPHA),
        }
    R["gates"] = {nm: gates_for(nm) for nm in ("HET", "LIVE")}

    def sign_scan(nm, arm):
        det = {}; signs = []
        for ax, pts in R["sign_sweep"][nm].items():
            for pt, row in pts.items():
                for c in ("a5_sham", "c2_blind"):
                    m = row["%s_vs_%s" % (arm, c)]["mean"]
                    s = 1 if m > 0 else (-1 if m < 0 else 0)
                    det.setdefault(ax, {})[pt + "|" + c] = {"mean": round(m, 3), "sign": s}
                    signs.append(s)
        return all(s > 0 for s in signs), all(s < 0 for s in signs), det

    R["verdict"] = {}
    for nm in ("HET", "LIVE"):
        gt = R["gates"][nm]
        C = R["main"][nm]["contrasts"][PRIMARY]
        sok_pos, sok_neg, sdet = sign_scan(nm, PRIMARY)
        sig = all(C[c]["mean"] > MARGIN and C[c]["p"] < ALPHA
                  for c in ("a5_sham", "c2_blind"))
        neg = all(C[c]["mean"] < -MARGIN and C[c]["p"] < ALPHA
                  for c in ("a5_sham", "c2_blind"))
        hard = all(gt[k] for k in ("G1_PASS", "G2_PASS", "G3_PASS_live_both_sided",
                                   "V_cap_conserved", "V_n_units", "V_info_PASS",
                                   "V_sham_distinct_from_blind", "V_POWER_PASS",
                                   "ORACLE_VALID"))
        if not hard:
            vd = "INVALID"
        elif sig and sok_pos:
            vd = "DIRECTIONAL-POSITIVE"
        elif neg and sok_neg:
            vd = "KILL"
        elif sig or neg:
            vd = "INVALID"        # 유의하나 부호 뒤집힘 = 좌표
        else:
            vd = "THEATER"
        # o_health 대조(예상 뒤집힘)
        Ch = R["main"][nm]["contrasts"]["o_health"]
        hpos, hneg, _ = sign_scan(nm, PRIMARY)  # placeholder (health sweep 미실시)
        R["verdict"][nm] = {
            "primary": PRIMARY,
            "vs_sham": {k: C["a5_sham"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "vs_c2": {k: C["c2_blind"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "vs_c1_frozen_reportonly": {k: C["c1_frozen"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "pooled_mean": C["_pooled_mean"],
            "o_health_vs_c2_diag": {k: Ch["c2_blind"][k] for k in ("mean", "sem", "t", "p")},
            "significant_both": bool(sig), "neg_both": bool(neg),
            "SIGN_ALL_POS": bool(sok_pos), "SIGN_ALL_NEG": bool(sok_neg),
            "hard_gates": bool(hard), "sign_detail": sdet, "VERDICT": vd}

    R["wall_s"] = round(time.time() - t0, 1)
    json.dump(R, open(os.path.join(OUT, "result.json"), "w"), indent=1, ensure_ascii=False)

    print("\n================ RESULT ================")
    print("담체 = load-공급 상보성 slack=S−L (health 아님) · PRIMARY a_comp")
    print("사전예측: a_comp 부호양성보존(양 기질·전 repair) · o_health 뒤집힘")
    for nm in ("HET", "LIVE"):
        print("\n--- %s 기질 ---" % nm)
        gt = R["gates"][nm]
        print("  G1=%s(%.1e) G2=%s G3=%s(h=%.3f atp=%.2f) POWER=%s(%.2fxMDE) ORACLE=%s(%+.2f p=%.3g)"
              % (gt["G1_PASS"], gt["G1_pump_max"], gt["G2_PASS"],
                 gt["G3_PASS_live_both_sided"], gt["G3_c2_health"], gt["G3_c2_atp"],
                 gt["V_POWER_PASS"], R["power"][nm]["span_over_MDE"],
                 gt["ORACLE_VALID"], gt["ORACLE_o6_minus_c2"], gt["ORACLE_p"]))
        print("  info: comp_slack_sel_ratio=%.2f | sham_tag_gap=%.3f blind_tag_gap=%.3f distinct=%s | corr(tag,slack)=%+.3f | info_PASS=%s"
              % (gt["V_comp_slack_sel_ratio"], gt["V_sham_tag_gap"], gt["V_blind_tag_gap"],
                 gt["V_sham_distinct_from_blind"], gt["V_tag_slack_corr_neutral"], gt["V_info_PASS"]))
        A = R["main"][nm]["arms"]
        for a in MAIN_ARMS:
            print("   %-11s atp=%6.2f h=%.3f sup=%6.2f slackgap=%.3f tagap=%.3f pump=%+.1e"
                  % (a, A[a]["atp"], A[a]["health"], A[a]["supply"],
                     A[a]["slack_gap_sel"], A[a]["tag_gap_sel"], A[a]["pump_max"]))
        v = R["verdict"][nm]
        print("   >> a_comp vs_sham %+7.3f±%.3f (t=%+6.2f p=%.3g %2d/20) | vs_c2 %+7.3f±%.3f (t=%+6.2f p=%.3g %2d/20)"
              % (v["vs_sham"]["mean"], v["vs_sham"]["sem"], v["vs_sham"]["t"], v["vs_sham"]["p"],
                 v["vs_sham"]["pos"], v["vs_c2"]["mean"], v["vs_c2"]["sem"], v["vs_c2"]["t"],
                 v["vs_c2"]["p"], v["vs_c2"]["pos"]))
        print("      SIGN+=%s SIGN-=%s | o_health vs_c2 %+.2f(diag,예상뒤집힘) | VERDICT=%s"
              % (v["SIGN_ALL_POS"], v["SIGN_ALL_NEG"], v["o_health_vs_c2_diag"]["mean"], v["VERDICT"]))
    print("\nG1 규약자유도(unweighted-mean pump/run):",
          {k: round(x, 1) for k, x in R["G1_convention_freedom_diag"]["unweighted_mean_pump_per_run"].items()})
    print("wall_s", R["wall_s"])


if __name__ == "__main__":
    main()
