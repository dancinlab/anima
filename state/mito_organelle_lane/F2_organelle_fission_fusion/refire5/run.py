#!/usr/bin/env python3
# =============================================================================
# H_9274 / F2 — 5th FIRE ($0 · numpy · CPU-local · mini · OMP=2)
#   "재조합(merge) 대수가 정보를 더하는가?"  (H_054 symbiogenesis · H_203 asym-merge)
#
# 이전 4발: 1차 pump / 2차 sink-영점 / 3차 담체(health) 부호반전 / 4차 sham 붕괴(범주 tag 동질화)
#   + 4차 REFUTE_v2 치명지적: (R1) a_comp = 헤드라인 ATP=Σmin(L,S) 의 순간 argmax (처치-detector
#     공선성 95.7%) · (R2) 기질 삭제해도 +11.8 재현(pooling 항등식) · (R3) 파티션-불변 물리량
#     (supply/health/overload)엔 이득 0 또는 음 · (R5) 필요한 통제 = a_detgrad.
#
# ======================= 사전등록 (PRE-REGISTRATION · 코드 sha256 동결) =======================
# 실행 전 고정. 데이터를 본 뒤 detector/판정변수/상수/arm 을 옮기지 않는다(규칙⑨).
# 새 seed: main 200–219 · pilot 950–969 — 4차(0–19 / 900–919)와 DISJOINT.
#
# --- [수리 1] sham 재설계 : 융합에 불변인 외생 담체 (유닛-상속 tag 폐기) ---
#   메타진단(4차): 보존적(질량보존) 융합은 유닛에 실린 어떤 상속 신호도 동질화한다
#     (스칼라→평균사 · 범주→대형모 흡수사). ⇒ sham 신호를 유닛 상태에 저장하면 안 된다.
#   ⇒ 외생 site-field: init 시 각 손상 site s 에 z_s ~ N(0,1) 을 **동결**(d,f,cap 과 독립,
#     절대 갱신/상속 안 함). 유닛의 외생점수는 매 이벤트 **재계산**:
#         Z_i = Σ_{s∈i} d_s z_s / L_i      (load-가중 평균)
#     이는 L, S 와 **동일한 대수 class**(질량가중 site 집계)라 융합해도 붕괴하지 않는다
#     (융합 = 두 부모의 load-가중 평균 · 분열 = site 재분할로 spread 재생성). 유닛 상태 0.
#   a5_sham = a_comp 와 **동일한 극단매칭 기계**를 Z 축에 적용 (min-Z × max-Z).
#     선택 *형태*(융합 횟수·극단짝짓기 구조) 동일 · 신호만 인과무관 = 구조/정보 격리기.
#   [필수 게이트] sham ≠ blind 를 **분포적 실측**:
#     zratio = E|ΔZ_sel| / std(Z_pool). blind 는 균등랜덤쌍 → zratio ≈ E|Δ| of 2 random draws.
#     PASS = (zratio_sham − zratio_blind > 1.0) AND (zratio_sham > 1.5) AND
#            seed-paired-t(sham zgap vs blind zgap) p < 1e-3.  미달 = sham 무효 → INVALID.
#   [중립 게이트] corr(Z, slack) 절대값 < 0.15 (sham 축이 담체와 무관).
#
# --- [수리 2] a_detgrad 통제 추가 (REFUTE_v2 R5) ---
#   a_detgrad = 순간 ΔATP = min(L_i+L_j, S_i+S_j) − min(L_i,S_i) − min(L_j,S_j) 의 argmax.
#   V_detector_collinear = (a_comp 선택쌍 == detgrad argmax) 비율 > 0.90  ⇒ 처치가 헤드라인의
#   기울기 그 자체 ⇒ **ATP-헤드라인 대비(H-A)는 항등식이라 정보 주장에 쓸 수 없음**(자격박탈 플래그).
#
# --- [수리 3] 판정변수를 파티션-불변 물리량으로 이중화 (REFUTE_v2 R3·조건(a)) ---
#   H-A (원 헤드라인 · 장부 DV) : warm-mean ATP = Σ min(L,S).
#       a_comp − c2_blind > MARGIN(p<α) AND a_comp − a5_sham > MARGIN(p<α) AND 전 축 부호양성.
#   H-B (물리 DV · PASS 의 진짜 조건) : warm-mean **supply** = Σ(cap−D)  [= health · Σcap 고정]
#       B_POS  : a_comp − c2_blind > DELTA_S(=1.0) AND p<α AND 전 축 부호양성.
#       B_EQUIV: TOST(δ=DELTA_S=1.0) 등가 (양쪽 단측 p<α)  ⇒ 장부 이득이 물리에 없음.
#       보조 물리 DV: overload(=stress>1 비율, 낮을수록 좋음) — 부호/유의 보고, 악화 시 명시.
#   [도달성 게이트] PHYS_REACHABLE : o6_oracle − c2_blind 의 supply Δ 를 보고. 오라클조차 0이면
#       "파티션은 총 물리자원을 못 움직인다" 자체가 물음의 답(음성) — power 실패가 아님을 명시.
#
# --- 사전등록 판정 분기 (실행 가능한 코드 · 데이터 보기 전 확정) ---
#   hard = G1 pump≤1e-9 · G2 self_remerge=0 · G3 live band 선등록 · cap보존 · n_units 고정
#          · V_comp_info(정보채널 var>0) · V_sham_distinct(위 3조건) · V_sham_neutral
#          · V_POWER(ATP MDE) · ORACLE_VALID
#   not hard                    -> INVALID
#   H-A ∧ H-B(B_POS)            -> DIRECTIONAL-POSITIVE  (재조합 대수가 정보를 더한다 · toy 상한)
#   H-A ∧ B_EQUIV               -> THEATER               (이득 = Σmin(L,S) 장부 항등식 · 물리 0)
#   H-A ∧ (¬B_POS ∧ ¬B_EQUIV)   -> INVALID               (물리 DV 결론불가)
#   ¬H-A ∧ 전 축 음성유의        -> KILL
#   그 외                        -> THEATER
#   (V_detector_collinear=True 면 H-A 는 항등식으로 해석 · 어떤 경우에도 H-B 없이 GREEN 금지.)
#
# --- 계측 강제규칙 9종 준수 ---
#  ① control별 paired-t 전부(순서통계량 detector 금지) ② SEM/paired-t 만 ③ pilot(950–969) 사전 MDE
#  ④ 정보채널 증명(comp DV=slack var>0 · sham DV=Z ⊥ slack · sham≠blind 실측) ⑤ V-gate 를 헤드라인
#  detector 그 자체에 ⑥ 부호보존 전 축 PASS 내장(+ detector-형태 축 = ATP vs supply 이중화로 열거)
#  ⑦ KILL/PASS 분기 실행가능 ⑧ 자원보존 사전게이트 ⑨ 사후 detector 교체 금지 · 새 disjoint seed
#  음성 주장은 TOST 등가검정으로만. tune-to-green / tune-to-red 둘 다 금지.
# =============================================================================

import json
import math
import os
import sys
import time

import numpy as np

# ---------------- 사전등록 상수 (4차와 동일 기질) ----------------
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

SEEDS = list(range(200, 220))          # DISJOINT from 4차 (0–19)
PILOT_SEEDS = list(range(950, 970))    # DISJOINT from 4차 (900–919)

MARGIN = 1.0        # ATP (장부 DV) 유의 마진
DELTA_S = 1.0       # supply (물리 DV) 마진 = TOST 등가 마진 (≈ supply 의 1%)
DELTA_O = 0.02      # overload 마진 (보조)
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
    "a5_sham":    ("blind", "sham"),      # 외생 Z 축 극단매칭 (융합-불변)
    "a_comp":     ("blind", "comp"),      # ★PRIMARY slack 상보성
    "a_detgrad":  ("blind", "detgrad"),   # 헤드라인 기울기 argmax (R5 통제)
    "o6_oracle":  ("blind", "oracle"),
    "guard_off":  ("blind", "comp"),
}
MAIN_ARMS = ("c1_frozen", "c2_blind", "a5_sham", "a_comp",
             "a_detgrad", "o6_oracle", "guard_off")
POLICY_AXIS = ("c2_blind", "a5_sham", "a_comp", "a_detgrad", "o6_oracle")
SWEEP_ARMS = ("c2_blind", "a5_sham", "a_comp")
GUARD_OFF = {"guard_off"}


def base_cfg(**kw):
    c = dict(rho=RHO, repair=None, sigma=1.0, capsplit="sym", B1=B1, EXC=EXC,
             feedback=True, frag_sigma=FRAG_SIGMA, merge="conservative")
    c.update(kw)
    return c


# ---------------- 기질 (4차와 동일) ----------------
def _init(rng, rho, frag_sigma, rng_z):
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
    z = rng_z.normal(0.0, 1.0, size=S)   # 외생 site-field · 동결 · d,f,cap 과 독립
    return d, f, owner, cap, z


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


def _zscore_units(owner, d, z, n):
    """외생 담체 Z_i = load-가중 site z 평균. 유닛 상태 미저장 → 융합-불변(재계산)."""
    num = np.bincount(owner, weights=d * z, minlength=n)[:n]
    den = np.maximum(_loads(owner, d, n), 1e-12)
    return num / den


def _lam_units(owner, d, f, n):
    num = np.bincount(owner, weights=d * f, minlength=n)[:n]
    den = np.maximum(_loads(owner, d, n), 1e-12)
    return num / den


def _eq_supply(cap, Dm, L, Lam, cfg):
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


def _detgain_matrix(Le, Se):
    """순간 ΔATP = min(Li+Lj, Si+Sj) − min(Li,Si) − min(Lj,Sj)."""
    f0 = np.minimum(Le, Se)
    Lm = Le[:, None] + Le[None, :]
    Sm = Se[:, None] + Se[None, :]
    return np.minimum(Lm, Sm) - f0[:, None] - f0[None, :]


# ---------------- FISSION (질량보존 · 4차 규약 그대로) ----------------
def _fission(state, aware, cfg, t, sibc):
    owner, cap, Dm, sib, cool, d, f, z, rng = state
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
    sib = np.append(sib, sid); sib[i] = sid
    cool = np.append(cool, t + COOL); cool[i] = t + COOL
    created = (ca - Da) + (cb - Db) - sup_before
    return (owner, cap, Dm, sib, cool, d, f, z, rng), created, 0


# ---------------- FUSION ----------------
def _fusion(state, policy, cfg, t, guards, diag):
    owner, cap, Dm, sib, cool, d, f, z, rng = state
    n = cap.size
    if n < 2:
        return state, 0.0, 1
    elig = np.flatnonzero(cool <= t) if guards else np.arange(n)
    if elig.size < 2:
        return state, 0.0, 1

    L = _loads(owner, d, n)
    Sv = np.maximum(cap - Dm, 1e-9)
    slack = Sv - L                                # >0 잉여 · <0 결손
    Z = _zscore_units(owner, d, z, n)             # 외생 담체 (sham 축)
    sl = slack[elig]
    ze = Z[elig]
    Le, Se = L[elig], Sv[elig]

    def compat(x, y):
        if not guards:
            return True
        return not (sib[x] != -1 and sib[x] == sib[y])

    def extreme_match(vals):
        lo_ord = [int(elig[k]) for k in np.argsort(vals, kind="stable")]
        hi_ord = [int(elig[k]) for k in np.argsort(-vals, kind="stable")]
        for x in lo_ord:
            for y in hi_ord:
                if x != y and compat(x, y):
                    return x, y
        return -1, -1

    def argmax_pair(gain):
        m = elig.size
        mask = np.zeros((m, m), dtype=bool)
        for x in range(m):
            for y in range(x + 1, m):
                mask[x, y] = compat(int(elig[x]), int(elig[y]))
        gg = np.where(mask, gain, -np.inf)
        if not np.isfinite(gg).any():
            return -1, -1, gg
        bx, by = np.unravel_index(np.argmax(gg), gg.shape)
        return int(elig[bx]), int(elig[by]), gg

    i = j = -1
    dg = None
    if policy == "oracle":
        Lam = _lam_units(owner, d, f, n)
        ce, De, Lae = cap[elig], Dm[elig], Lam[elig]
        m = elig.size
        f0 = np.minimum(Le, _eq_supply(ce, De, Le, Lae, cfg))
        Cm = ce[:, None] + ce[None, :]
        Dmm = De[:, None] + De[None, :]
        Lm = Le[:, None] + Le[None, :]
        Laem = (Le[:, None] * Lae[:, None] + Le[None, :] * Lae[None, :]) \
            / np.maximum(Lm, 1e-12)
        fm = np.minimum(Lm, _eq_supply(Cm.ravel(), Dmm.ravel(), Lm.ravel(),
                                       Laem.ravel(), cfg).reshape(m, m))
        i, j, _ = argmax_pair(fm - f0[:, None] - f0[None, :])
    elif policy == "detgrad":
        i, j, _ = argmax_pair(_detgain_matrix(Le, Se))
    elif policy == "comp":
        i, j = extreme_match(sl)
    elif policy == "sham":
        i, j = extreme_match(ze)
    else:  # blind
        order = [int(elig[k]) for k in rng.permutation(elig.size)]
        i = order[0]
        for c in order[1:]:
            if compat(i, c):
                j = c
                break
    if i == -1 or j == -1:
        return state, 0.0, 1

    if diag is not None:
        diag["n_fuse"] += 1
        diag["self_remerge"] += 1.0 if (sib[i] != -1 and sib[i] == sib[j]) else 0.0
        diag["slack_gap_sel"].append(abs(float(slack[i]) - float(slack[j])))
        diag["slack_pop_std"].append(float(sl.std()))
        diag["z_gap_sel"].append(abs(float(Z[i]) - float(Z[j])))
        diag["z_pop_std"].append(float(ze.std()))
        diag["corr_zs"].append((ze.copy(), sl.copy()))
        if policy == "comp":     # R1 공선성 in-situ 계측
            gain = _detgain_matrix(Le, Se)
            bi, bj, gg = argmax_pair(gain)
            diag["dg_n"] += 1
            diag["dg_match"] += 1.0 if {bi, bj} == {i, j} else 0.0
            fin = gg[np.isfinite(gg)]
            xi = int(np.flatnonzero(elig == i)[0]); xj = int(np.flatnonzero(elig == j)[0])
            lo, hi = (xi, xj) if xi < xj else (xj, xi)
            gsel = float(gain[lo, hi])
            gmax = float(fin.max()) if fin.size else 0.0
            diag["dg_capture"].append(gsel / gmax if abs(gmax) > 1e-12 else 1.0)

    lo, hi = (i, j) if i < j else (j, i)
    sup_before = (cap[lo] - Dm[lo]) + (cap[hi] - Dm[hi])
    owner = owner.copy()
    owner[owner == hi] = lo
    owner[owner > hi] -= 1
    cap = cap.copy(); Dm = Dm.copy(); sib = sib.copy(); cool = cool.copy()
    cap[lo] += cap[hi]; Dm[lo] += Dm[hi]        # G1 강제 (보존적)
    sib[lo] = -1; cool[lo] = -1
    keep = np.arange(cap.size) != hi
    cap, Dm, sib, cool = cap[keep], Dm[keep], sib[keep], cool[keep]
    created = (cap[lo] - Dm[lo]) - sup_before
    return (owner, cap, Dm, sib, cool, d, f, z, rng), float(created), 0


# ---------------- 한 run ----------------
def simulate(seed, arm, cfg):
    fis, fus = ARMS[arm]
    dyn = fis is not None
    guards = arm not in GUARD_OFF

    rng_d = np.random.default_rng(10_000 + seed)
    rng_a = np.random.default_rng(90_000 + seed)
    rng_x = np.random.default_rng(70_000 + seed)
    rng_z = np.random.default_rng(50_000 + seed)

    d, f, owner, cap, z = _init(rng_d, cfg["rho"], cfg["frag_sigma"], rng_z)
    Dm = np.zeros(N0)
    sib = np.full(N0, -1, dtype=np.int64)
    cool = np.full(N0, -1, dtype=np.int64)
    st = (owner, cap, Dm, sib, cool, d, f, z, rng_a)
    sibc = [0]
    diag = {"n_fuse": 0, "self_remerge": 0.0, "slack_gap_sel": [], "slack_pop_std": [],
            "z_gap_sel": [], "z_pop_std": [], "corr_zs": [],
            "dg_n": 0, "dg_match": 0.0, "dg_capture": []}
    pump = 0.0
    atp, hh, sup, ovl = [], [], [], []

    for t in range(T):
        d = _drift(d, rng_d)
        st = (st[0], st[1], st[2], st[3], st[4], d, f, z, rng_a)
        if dyn:
            for _ in range(K_EV):
                st, cr, _ = _fission(st, fis == "aware", cfg, t, sibc)
                pump += cr
                st, cr, _ = _fusion(st, fus, cfg, t, guards, diag if t >= WARM else None)
                pump += cr

        owner, cap, Dm = st[0], st[1], st[2]
        n = cap.size
        L = _loads(owner, d, n)
        Sv = cap - Dm
        atp.append(float(np.minimum(L, Sv).sum()))
        sup.append(float(Sv.sum()))
        hh.append(float(Sv.sum() / max(cap.sum(), 1e-9)))
        stress = L / np.maximum(Sv, 1e-9)
        ovl.append(float((stress > 1.0).mean()))

        Lam = _lam_units(owner, d, f, n)
        rate = Lam * (1.0 + cfg["B1"] * np.clip(stress - 1.0, 0.0, cfg["EXC"])) \
            if cfg["feedback"] else Lam
        ux = rng_x.gamma(NOISE_K, 1.0 / NOISE_K, size=n)
        uy = rng_x.gamma(NOISE_K, 1.0 / NOISE_K, size=n)
        Dm = Dm + (cap - Dm) * (1.0 - np.exp(-rate * ux / G)) \
            - Dm * (1.0 - np.exp(-cfg["repair"] * uy))
        Dm = np.clip(Dm, 0.0, cap)
        st = (owner, cap, Dm, st[3], st[4], d, f, z, rng_a)

    w = slice(WARM, T)
    mm = lambda v: float(np.mean(v)) if len(v) else 0.0
    if diag["corr_zs"]:
        zv = np.concatenate([x[0] for x in diag["corr_zs"]])
        sv = np.concatenate([x[1] for x in diag["corr_zs"]])
        czs = float(np.corrcoef(zv, sv)[0, 1]) if zv.std() > 1e-9 and sv.std() > 1e-9 else 0.0
    else:
        czs = 0.0
    sgs, sps = mm(diag["slack_gap_sel"]), mm(diag["slack_pop_std"])
    zgs, zps = mm(diag["z_gap_sel"]), mm(diag["z_pop_std"])
    return dict(
        atp=float(np.mean(atp[w])), health=float(np.mean(hh[w])),
        supply=float(np.mean(sup[w])), overload=float(np.mean(ovl[w])),
        self_remerge=(diag["self_remerge"] / diag["n_fuse"]) if diag["n_fuse"] else 0.0,
        slack_gap_sel=sgs, slack_sel_ratio=(sgs / sps) if sps > 1e-9 else 0.0,
        z_gap_sel=zgs, z_pop_std=zps, z_sel_ratio=(zgs / zps) if zps > 1e-9 else 0.0,
        corr_z_slack=czs,
        detgrad_match=(diag["dg_match"] / diag["dg_n"]) if diag["dg_n"] else float("nan"),
        detgrad_capture=mm(diag["dg_capture"]) if diag["dg_capture"] else float("nan"),
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


def t_upper(t, df):
    """P(T > t)."""
    t = float(t)
    return t_sf(t, df) if t >= 0 else 1.0 - t_sf(-t, df)


def paired(e, c):
    dv = np.asarray(e) - np.asarray(c)
    n = dv.size
    m = float(dv.mean()); sd = float(dv.std(ddof=1))
    sem = sd / math.sqrt(n)
    tv = m / sem if sem > 0 else 0.0
    return {"mean": m, "sem": sem, "t": float(tv), "p": 2.0 * t_sf(tv, n - 1),
            "pos": int((dv > 0).sum()), "n": n}


def tost(e, c, delta):
    dv = np.asarray(e) - np.asarray(c)
    n = dv.size
    m = float(dv.mean()); sd = float(dv.std(ddof=1))
    sem = sd / math.sqrt(n) if sd > 0 else 1e-12
    df = n - 1
    p_lo = t_upper((m + delta) / sem, df)          # H0: mu <= -delta
    p_hi = t_upper(-((m - delta) / sem), df)       # H0: mu >= +delta
    pmax = max(p_lo, p_hi)
    return {"mean": m, "sem": sem, "delta": delta, "p_lower": p_lo, "p_upper": p_hi,
            "p_tost": pmax, "EQUIVALENT": bool(pmax < ALPHA)}


def grid(seeds, cfg, arms):
    out = {}
    for a in arms:
        per = [simulate(s, a, cfg) for s in seeds]
        g = {"atp_per_seed": [p["atp"] for p in per],
             "supply_per_seed": [p["supply"] for p in per],
             "overload_per_seed": [p["overload"] for p in per],
             "zgap_per_seed": [p["z_gap_sel"] for p in per]}
        for k in ("atp", "health", "supply", "overload", "self_remerge",
                  "slack_gap_sel", "slack_sel_ratio", "z_gap_sel", "z_pop_std",
                  "z_sel_ratio", "corr_z_slack", "detgrad_match", "detgrad_capture",
                  "pump", "cap_dev"):
            v = np.array([p[k] for p in per], dtype=float)
            g[k] = float(np.nanmean(v)) if not np.all(np.isnan(v)) else float("nan")
        g["pump_max"] = float(max(abs(p["pump"]) for p in per))
        g["n_units"] = sorted(set(p["n_units"] for p in per))
        out[a] = g
    return out


def contrasts(gr, arm, key="atp_per_seed", ctrls=CONTROLS):
    o = {}
    for c in ctrls:
        if c == arm:
            continue
        o[c] = paired(gr[arm][key], gr[c][key])
    o["_pooled_mean"] = float(np.mean([o[c]["mean"] for c in o]))
    return o


# ================================ MAIN ================================
def main():
    t0 = time.time()
    R = {"prereg": {
        "question": "재조합(merge) 대수가 정보를 더하는가 (H_054 · H_203)",
        "fire": 5,
        "seeds_main": SEEDS, "seeds_pilot": PILOT_SEEDS,
        "disjoint_from_4th": "main 200-219 / pilot 950-969 vs 4차 0-19 / 900-919",
        "sham": "외생 site-field z(동결·독립) → Z_i = load-가중 평균 (유닛 상태 미저장 · 융합-불변 "
                "재계산) · a_comp 와 동일 극단매칭 기계 · 신호만 인과무관",
        "sham_gate": "zratio_sham−zratio_blind>1.0 AND zratio_sham>1.5 AND paired-t p<1e-3",
        "new_control": "a_detgrad = 순간 ΔATP argmax (REFUTE_v2 R5) · V_detector_collinear>0.90 면 "
                       "H-A(ATP)는 항등식",
        "H_A": "warm-mean ATP: a_comp−c2_blind>1.0(p<.05) AND a_comp−a5_sham>1.0(p<.05) AND 전축 부호+",
        "H_B": "warm-mean supply(파티션-불변 물리 DV): B_POS = Δ>1.0,p<.05,전축 부호+ / "
               "B_EQUIV = TOST(δ=1.0) 등가",
        "verdict_branches": "¬hard→INVALID · H-A∧B_POS→DIRECTIONAL-POSITIVE · H-A∧B_EQUIV→THEATER · "
                            "H-A∧기타→INVALID · ¬H-A∧전축음성→KILL · else THEATER",
        "controls": CONTROLS, "margin_atp": MARGIN, "delta_supply": DELTA_S, "alpha": ALPHA,
        "sign_axes": ["repair(live band)", "sigma{0,.5,1}", "capsplit{sym,load}",
                      "rho{.7,.85,1}", "frag_sigma{.5,.9}", "EXC{1,2,6}[LIVE]", "B1{1.5,3}[LIVE]",
                      "detector-form{ATP, supply, overload}"]}}

    # ===== G3 · LIVE-REGIME 선등록 (CONTROL만) =====
    ceiling = D_TOTAL
    scan = {}
    for r in REPAIR_GRID:
        g = grid(SEEDS, base_cfg(repair=r, feedback=False), ("c2_blind",))
        scan[r] = {"c2_health": g["c2_blind"]["health"], "c2_atp": g["c2_blind"]["atp"]}
    live = [r for r in REPAIR_GRID
            if LIVE_LO < scan[r]["c2_health"] < LIVE_HI and scan[r]["c2_atp"] < CEIL_FRAC * ceiling]
    R["G3_live_regime"] = {"scan_controls_only": scan,
                           "rule": f"{LIVE_LO}<health(c2)<{LIVE_HI} AND atp(c2)<{CEIL_FRAC}x{ceiling}",
                           "live_band": live}
    if not live:
        R["verdict"] = {"HET": {"VERDICT": "INVALID"}, "LIVE": {"VERDICT": "INVALID"},
                        "why": "G3 실패"}
        json.dump(R, open(os.path.join(OUT, "result.json"), "w"), indent=1, ensure_ascii=False)
        print("G3 FAIL"); sys.exit(0)
    R_PRIM = live[len(live) // 2]
    R["G3_live_regime"]["primary_repair"] = R_PRIM
    print("[G3] live=%s PRIMARY repair=%s c2_health=%.3f (%.1fs)"
          % (live, R_PRIM, scan[R_PRIM]["c2_health"], time.time() - t0))

    CFG = {"HET": base_cfg(repair=R_PRIM, feedback=False),
           "LIVE": base_cfg(repair=R_PRIM, feedback=True)}

    # ===== ③ 사전 MDE (pilot · disjoint) — ATP(장부) + supply(물리) 둘 다 =====
    R["power"] = {}
    for nm in ("HET", "LIVE"):
        pg = grid(PILOT_SEEDS, CFG[nm], POLICY_AXIS)
        sd_a = float((np.array(pg[PRIMARY]["atp_per_seed"])
                      - np.array(pg["a5_sham"]["atp_per_seed"])).std(ddof=1))
        sd_s = float((np.array(pg[PRIMARY]["supply_per_seed"])
                      - np.array(pg["c2_blind"]["supply_per_seed"])).std(ddof=1))
        k = (2.093 + 0.861) / math.sqrt(len(SEEDS))
        mde_a, mde_s = k * sd_a, k * sd_s
        ma = {a: pg[a]["atp"] for a in POLICY_AXIS}
        ms = {a: pg[a]["supply"] for a in POLICY_AXIS}
        span_a = max(ma.values()) - min(ma.values())
        span_s = max(ms.values()) - min(ms.values())
        R["power"][nm] = {
            "MDE_atp": mde_a, "atp_pilot": ma, "span_atp": span_a,
            "span_atp_over_MDE": span_a / mde_a, "POWERED_atp": bool(span_a > 3.0 * mde_a),
            "MDE_supply": mde_s, "supply_pilot": ms, "span_supply": span_s,
            "span_supply_over_MDE": span_s / mde_s if mde_s > 0 else 0.0,
            "POWERED_supply": bool(span_s > 3.0 * mde_s),
            "note_supply": "물리 DV 의 정책축 도달범위(오라클 포함). TOST δ=1.0 이 MDE 보다 크면 "
                           "등가결론이 검정력으로 뒷받침됨."}
        print("[MDE-%s] atp: MDE=%.3f span=%.2f (%.1fx) | supply: MDE=%.3f span=%.2f (%.1fx) (%.0fs)"
              % (nm, mde_a, span_a, span_a / mde_a, mde_s, span_s,
                 span_s / mde_s if mde_s > 0 else 0, time.time() - t0))

    # ===== 본 실험 =====
    R["main"] = {}
    for nm in ("HET", "LIVE"):
        g = grid(SEEDS, CFG[nm], MAIN_ARMS)
        con = {}
        for a in ("a_comp", "a_detgrad", "o6_oracle", "guard_off"):
            con[a] = {"atp": contrasts(g, a, "atp_per_seed"),
                      "supply": contrasts(g, a, "supply_per_seed"),
                      "overload": contrasts(g, a, "overload_per_seed")}
        con["o6_vs_c2_atp"] = paired(g["o6_oracle"]["atp_per_seed"], g["c2_blind"]["atp_per_seed"])
        con["o6_vs_c2_supply"] = paired(g["o6_oracle"]["supply_per_seed"],
                                        g["c2_blind"]["supply_per_seed"])
        con["sham_vs_c2_atp"] = paired(g["a5_sham"]["atp_per_seed"], g["c2_blind"]["atp_per_seed"])
        con["sham_vs_c2_zgap"] = paired(g["a5_sham"]["zgap_per_seed"], g["c2_blind"]["zgap_per_seed"])
        con["comp_vs_detgrad_atp"] = paired(g["a_comp"]["atp_per_seed"],
                                            g["a_detgrad"]["atp_per_seed"])
        con["TOST_comp_vs_blind_supply"] = tost(g["a_comp"]["supply_per_seed"],
                                                g["c2_blind"]["supply_per_seed"], DELTA_S)
        con["TOST_comp_vs_sham_supply"] = tost(g["a_comp"]["supply_per_seed"],
                                               g["a5_sham"]["supply_per_seed"], DELTA_S)
        con["TOST_comp_vs_blind_overload"] = tost(g["a_comp"]["overload_per_seed"],
                                                  g["c2_blind"]["overload_per_seed"], DELTA_O)
        R["main"][nm] = {"arms": {a: {k: g[a][k] for k in
                                      ("atp", "health", "supply", "overload", "self_remerge",
                                       "slack_gap_sel", "slack_sel_ratio", "z_gap_sel",
                                       "z_pop_std", "z_sel_ratio", "corr_z_slack",
                                       "detgrad_match", "detgrad_capture",
                                       "pump", "pump_max", "cap_dev", "n_units")}
                                  for a in MAIN_ARMS},
                         "contrasts": con}
        print("[main-%s] done (%.0fs)" % (nm, time.time() - t0))

    # ===== ⑥ 부호보존 스윕 (ATP + supply 둘 다) =====
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
                       "atp": {a: g[a]["atp"] for a in SWEEP_ARMS},
                       "supply": {a: g[a]["supply"] for a in SWEEP_ARMS}}
                for c in ("a5_sham", "c2_blind"):
                    pa = paired(g[PRIMARY]["atp_per_seed"], g[c]["atp_per_seed"])
                    ps = paired(g[PRIMARY]["supply_per_seed"], g[c]["supply_per_seed"])
                    row["atp_%s_vs_%s" % (PRIMARY, c)] = {k: pa[k] for k in ("mean", "sem", "t", "p", "pos")}
                    row["sup_%s_vs_%s" % (PRIMARY, c)] = {k: ps[k] for k in ("mean", "sem", "t", "p", "pos")}
                R["sign_sweep"][nm][ax]["%s=%s" % (key, val)] = row
            print("[sweep-%s] %s (%.0fs)" % (nm, ax, time.time() - t0))

    # ===== 게이트 =====
    def gates_for(nm):
        M = R["main"][nm]["arms"]
        C = R["main"][nm]["contrasts"]
        g1 = max(abs(M[a]["pump_max"]) for a in MAIN_ARMS)
        zr_sham, zr_blind = M["a5_sham"]["z_sel_ratio"], M["c2_blind"]["z_sel_ratio"]
        zt = C["sham_vs_c2_zgap"]
        distinct = bool(zr_sham - zr_blind > 1.0 and zr_sham > 1.5 and zt["p"] < 1e-3)
        comp_ratio = M[PRIMARY]["slack_sel_ratio"]
        corr_neutral = M["a5_sham"]["corr_z_slack"]
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
            "V_comp_slack_sel_ratio": comp_ratio,
            "V_comp_info_PASS": bool(comp_ratio > 0.5),
            "V_sham_z_sel_ratio": zr_sham, "V_blind_z_sel_ratio": zr_blind,
            "V_sham_zgap_t": zt["t"], "V_sham_zgap_p": zt["p"], "V_sham_zgap_pos": zt["pos"],
            "V_sham_distinct_from_blind": distinct,
            "V_sham_neutral_corr_z_slack": corr_neutral,
            "V_sham_NEUTRAL_PASS": bool(abs(corr_neutral) < 0.15),
            "V_detector_collinear_match": M[PRIMARY]["detgrad_match"],
            "V_detector_capture": M[PRIMARY]["detgrad_capture"],
            "V_detector_collinear": bool(M[PRIMARY]["detgrad_match"] > 0.90),
            "V_POWER_atp": bool(R["power"][nm]["POWERED_atp"]),
            "PHYS_REACH_oracle_supply": C["o6_vs_c2_supply"]["mean"],
            "PHYS_REACH_oracle_supply_p": C["o6_vs_c2_supply"]["p"],
            "ORACLE_atp": C["o6_vs_c2_atp"]["mean"], "ORACLE_p": C["o6_vs_c2_atp"]["p"],
            "ORACLE_VALID": bool(C["o6_vs_c2_atp"]["mean"] > 0 and C["o6_vs_c2_atp"]["p"] < ALPHA),
        }
    R["gates"] = {nm: gates_for(nm) for nm in ("HET", "LIVE")}

    def sign_scan(nm, pre):
        det = {}; signs = []
        for ax, pts in R["sign_sweep"][nm].items():
            for pt, row in pts.items():
                for c in ("a5_sham", "c2_blind"):
                    k = "%s_%s_vs_%s" % (pre, PRIMARY, c)
                    m = row[k]["mean"]
                    s = 1 if m > 0 else (-1 if m < 0 else 0)
                    det.setdefault(ax, {})[pt + "|" + c] = {"mean": round(m, 4), "sign": s}
                    signs.append(s)
        return all(s > 0 for s in signs), all(s < 0 for s in signs), det

    R["verdict"] = {}
    for nm in ("HET", "LIVE"):
        gt = R["gates"][nm]
        Ca = R["main"][nm]["contrasts"][PRIMARY]["atp"]
        Cs = R["main"][nm]["contrasts"][PRIMARY]["supply"]
        Co = R["main"][nm]["contrasts"][PRIMARY]["overload"]
        TT = R["main"][nm]["contrasts"]["TOST_comp_vs_blind_supply"]
        TT2 = R["main"][nm]["contrasts"]["TOST_comp_vs_sham_supply"]
        a_pos, a_neg, adet = sign_scan(nm, "atp")
        s_pos, s_neg, sdet = sign_scan(nm, "sup")

        HA = all(Ca[c]["mean"] > MARGIN and Ca[c]["p"] < ALPHA
                 for c in ("a5_sham", "c2_blind")) and a_pos
        HA_neg = all(Ca[c]["mean"] < -MARGIN and Ca[c]["p"] < ALPHA
                     for c in ("a5_sham", "c2_blind")) and a_neg
        B_POS = bool(Cs["c2_blind"]["mean"] > DELTA_S and Cs["c2_blind"]["p"] < ALPHA and s_pos)
        B_EQUIV = bool(TT["EQUIVALENT"] and TT2["EQUIVALENT"])

        hard = all(gt[k] for k in ("G1_PASS", "G2_PASS", "G3_PASS_live_both_sided",
                                   "V_cap_conserved", "V_n_units", "V_comp_info_PASS",
                                   "V_sham_distinct_from_blind", "V_sham_NEUTRAL_PASS",
                                   "V_POWER_atp", "ORACLE_VALID"))
        if not hard:
            vd = "INVALID"
        elif HA and B_POS:
            vd = "DIRECTIONAL-POSITIVE"
        elif HA and B_EQUIV:
            vd = "THEATER"
        elif HA:
            vd = "INVALID"
        elif HA_neg:
            vd = "KILL"
        else:
            vd = "THEATER"
        R["verdict"][nm] = {
            "primary": PRIMARY,
            "ATP_vs_c2": {k: Ca["c2_blind"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "ATP_vs_sham": {k: Ca["a5_sham"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "ATP_pooled_mean": Ca["_pooled_mean"],
            "SUPPLY_vs_c2": {k: Cs["c2_blind"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "SUPPLY_vs_sham": {k: Cs["a5_sham"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "OVERLOAD_vs_c2": {k: Co["c2_blind"][k] for k in ("mean", "sem", "t", "p", "pos")},
            "TOST_supply_vs_blind": TT, "TOST_supply_vs_sham": TT2,
            "TOST_overload_vs_blind": R["main"][nm]["contrasts"]["TOST_comp_vs_blind_overload"],
            "comp_vs_detgrad_atp": R["main"][nm]["contrasts"]["comp_vs_detgrad_atp"],
            "H_A": bool(HA), "H_A_neg": bool(HA_neg), "B_POS": B_POS, "B_EQUIV": B_EQUIV,
            "ATP_SIGN_ALL_POS": bool(a_pos), "SUPPLY_SIGN_ALL_POS": bool(s_pos),
            "SUPPLY_SIGN_ALL_NEG": bool(s_neg),
            "detector_collinear": gt["V_detector_collinear"],
            "hard_gates": bool(hard), "atp_sign_detail": adet, "supply_sign_detail": sdet,
            "VERDICT": vd}

    R["wall_s"] = round(time.time() - t0, 1)
    json.dump(R, open(os.path.join(OUT, "result.json"), "w"), indent=1, ensure_ascii=False)

    print("\n================ RESULT (5th) ================")
    for nm in ("HET", "LIVE"):
        gt = R["gates"][nm]; v = R["verdict"][nm]
        print("\n--- %s ---" % nm)
        print("  G1=%s(%.1e) G2=%s G3=%s(h=%.3f) POWER=%s ORACLE=%s(%+.2f p=%.2g)"
              % (gt["G1_PASS"], gt["G1_pump_max"], gt["G2_PASS"], gt["G3_PASS_live_both_sided"],
                 gt["G3_c2_health"], gt["V_POWER_atp"], gt["ORACLE_VALID"],
                 gt["ORACLE_atp"], gt["ORACLE_p"]))
        print("  SHAM distinct: zratio sham=%.2f blind=%.2f (Δ=%.2f) paired-t=%.1f p=%.2g %d/20 -> %s | corr(Z,slack)=%+.3f"
              % (gt["V_sham_z_sel_ratio"], gt["V_blind_z_sel_ratio"],
                 gt["V_sham_z_sel_ratio"] - gt["V_blind_z_sel_ratio"], gt["V_sham_zgap_t"],
                 gt["V_sham_zgap_p"], gt["V_sham_zgap_pos"], gt["V_sham_distinct_from_blind"],
                 gt["V_sham_neutral_corr_z_slack"]))
        print("  DETECTOR collinearity: comp==detgrad argmax %.3f (capture %.3f) -> collinear=%s"
              % (gt["V_detector_collinear_match"], gt["V_detector_capture"],
                 gt["V_detector_collinear"]))
        A = R["main"][nm]["arms"]
        for a in MAIN_ARMS:
            print("   %-11s atp=%6.2f sup=%7.3f ovl=%.3f h=%.3f zratio=%.2f pump=%+.1e"
                  % (a, A[a]["atp"], A[a]["supply"], A[a]["overload"], A[a]["health"],
                     A[a]["z_sel_ratio"], A[a]["pump_max"]))
        print("   H-A ATP  vs c2 %+7.3f±%.3f (t=%+.1f p=%.2g %2d/20) | vs sham %+7.3f±%.3f (t=%+.1f p=%.2g %2d/20) SIGN+=%s"
              % (v["ATP_vs_c2"]["mean"], v["ATP_vs_c2"]["sem"], v["ATP_vs_c2"]["t"],
                 v["ATP_vs_c2"]["p"], v["ATP_vs_c2"]["pos"],
                 v["ATP_vs_sham"]["mean"], v["ATP_vs_sham"]["sem"], v["ATP_vs_sham"]["t"],
                 v["ATP_vs_sham"]["p"], v["ATP_vs_sham"]["pos"], v["ATP_SIGN_ALL_POS"]))
        print("   H-B SUP  vs c2 %+7.3f±%.3f (t=%+.1f p=%.2g %2d/20) | TOST(δ=1.0) p=%.3g EQUIV=%s | oracle-reach sup %+.3f (p=%.2g)"
              % (v["SUPPLY_vs_c2"]["mean"], v["SUPPLY_vs_c2"]["sem"], v["SUPPLY_vs_c2"]["t"],
                 v["SUPPLY_vs_c2"]["p"], v["SUPPLY_vs_c2"]["pos"],
                 v["TOST_supply_vs_blind"]["p_tost"], v["TOST_supply_vs_blind"]["EQUIVALENT"],
                 gt["PHYS_REACH_oracle_supply"], gt["PHYS_REACH_oracle_supply_p"]))
        print("       OVL vs c2 %+.4f (p=%.2g) | comp−detgrad ATP %+.3f (p=%.2g)"
              % (v["OVERLOAD_vs_c2"]["mean"], v["OVERLOAD_vs_c2"]["p"],
                 v["comp_vs_detgrad_atp"]["mean"], v["comp_vs_detgrad_atp"]["p"]))
        print("   >> H_A=%s B_POS=%s B_EQUIV=%s hard=%s  VERDICT=%s"
              % (v["H_A"], v["B_POS"], v["B_EQUIV"], v["hard_gates"], v["VERDICT"]))
    print("\nwall_s", R["wall_s"])


if __name__ == "__main__":
    main()
