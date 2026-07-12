#!/usr/bin/env python3
# =============================================================================
# H_9287 / F14 — Ω 물리담체 확증 런 (6th fire · $0 · numpy · CPU-local · OMP=2)
#   물음: "재조합(merge) 대수가 물리 정보를 더하는가, 그리고 국소 관측으로 도달가능한가?"
#         (H_054 symbiogenesis · H_203 asym-merge 의 미답 물음)
#
# 기질(substrate) = F2 5차 run.py 와 동일 (동일 상수 · 동일 _init/_drift/_fission/_fusion tail).
# 바뀐 것은 FUSION 정책(담체)과 판정규약뿐.
#
# ====================== 사전등록 (PRE-REGISTRATION · sha256 동결) ======================
# 데이터를 보기 전에 아래를 확정한다. 실행 후 detector/판정변수/마진/arm 을 옮기지 않는다(규칙⑨).
#
# [담체] DERIVATION.md TOP-1 = Ω_k (RELAX-k · 공급응답 담체)
#   Ω_k(i,j) = R_k(cap_i+cap_j, L_i+L_j, Λ_ij ; S_i+S_j) − R_k(cap_i,L_i,Λ_i;S_i) − R_k(cap_j,L_j,Λ_j;S_j)
#   R_k: S←S0, k회 반복  S ← cap·c / ( r(Λ, L/S) + c ),  r(Λ,st)=Λ(1+B1·clip(st−1,0,EXC)),  c = G·(1−e^−repair)
#   Λ_ij = (L_iΛ_i + L_jΛ_j)/(L_i+L_j)  (하중가중 · 융합불변)
#   국소성: (cap,L,S,Λ)_i,j 만 사용 · 전역상태 미사용 · min() 없음(장부 껍질 없음) · Ω_0 ≡ 0(정리).
#
# [정리 · 왜 이 담체인가] 융합은 S=cap−D 를 정확히 보존 ⇒ ΔS|_t ≡ 0 ⇒ 순간 관측 담체는 정의상
#   장부(Σmin(L,S))의 함수. 물리 채널은 이완에만 있다. Ω_1 = 첫 비소멸 차수.
#
# [DV · 헤드라인 · 규칙⑪] 파티션-불변 물리량만:
#   PRIMARY  = warm-mean supply = Σ(cap−D)     (높을수록 좋음)
#   SECONDARY= warm-mean overload = (stress>1) 비율  (낮을수록 좋음)
#   🚫 장부 ATP = Σmin(L,S) 는 보고만 하고 판정에 쓰지 않는다 (5차의 덫: a_comp 가 장부기울기를
#      capture 0.98 로 타고 있었다). ΔATP>0 은 PASS 조건이 아니다 (HET 에선 Ω 가 ATP 를 잃는 게 정상).
#
# [ARMS]
#   c1_frozen        분열/융합 없음 (기저)
#   c2_blind         균등랜덤 쌍 (주 control)
#   a_omega1  ★PRIMARY   Ω_1
#   a_omega3            Ω_3
#   a_omega8            Ω_8   (DV-정렬 국소 상한 · 도달성 게이트)
#   s_lamperm    sham   Ω_1 인데 Λ 를 Λ̃ 로 대체: site f 를 동결 순열 f̃=f[π] → 동일 질량가중 규칙으로
#                       Λ̃_i = Σ_{s∈i} d_s f̃_s / L_i 재계산. 융합불변 · 동일 함수형 · 동일 주변분포,
#                       인과만 절단 (Λ̃ 는 실제 손상률을 지배하지 않음).
#   s_stressshuf sham   Ω_1 인데 (cap,L,S) 삼중항을 eligible 안에서 순열: 응력-중항 채널의 인과 절단
#                       (Λ 는 참). 두 채널(Λ-수송 ⊥ 응력-중항) 분리 확인용.
#   a_detgrad    ctrl   순간 ΔATP=min(Li+Lj,Si+Sj)−min(Li,Si)−min(Lj,Sj) argmax (장부 기울기)
#   a_comp     +ctrl(반정렬)  slack 극단매칭 — 5차 PRIMARY. **overload 를 올려야 정상**(반정렬 양성대조)
#   o6_oracle    비교용  평형장부 min(L,S_eq) argmax. **상한 아님**(장부 껍질).
#   a_omega1_mis 강건성  Ω_1 인데 담체 상수를 틀리게: B1×3, EXC×0.5, c×4 (모델-전지 배제)
#
# [SEEDS] 확증 main = 200–219 · MDE pilot = 600–619 (분석과 disjoint)
#   Fable 파일럿 seed 950–985 와 서로소 ⇒ 오염 0. 5차 main(200–219) 과는 겹치나 5차는 다른 arm 집합
#   (Ω 계열 미존재)이므로 Ω 에 대해서는 未觀測 = 확증 seed 로 유효.
#
# [MDE · 규칙③] disjoint pilot(600–619)에서 sd(Ω_1 − c2_blind)_supply → MDE=(t.975+t.80)/√20·sd.
#   도달성 축 = Ω_8 (오라클 아님! DERIVATION §8-1: HET 에서 오라클은 눈이 먼다).
#   ABORT 조건: (Ω_8 − c2_blind)_supply 파일럿 효과 ≤ 3·MDE → V_POWER=False → INVALID.
#
# [PASS 분기 · 실행가능 코드 · 데이터 보기 전 확정]
#   hard = G1 pump_max≤1e-9 · G2 self_remerge=0 · G3 live band · cap보존 · n_units 고정
#        · V_info (Ω pool std>0 ∧ 선택쌍 z>1.0 : 처치 DV 가 control 이 못 보는 입력의 함수)
#        · V_sham_valid (sham 이 진짜 Ω 와 다른 쌍을 고름: pair_match(sham, Ω_1) < 0.5)
#        · V_POWER (위 MDE) · V_REACH (Ω_8 supply Δ vs blind > DELTA_S ∧ p<α)
#   ¬hard                                             -> INVALID
#   PASS := (Ω_1 supply Δ > DELTA_S ∧ p<α)  vs **c2_blind ∧ s_lamperm ∧ a_detgrad 셋 다**
#           ∧ OVL_OK (overload vs blind: mean≤0 이거나 p≥α — 즉 악화 없음)
#           ∧ SIGN (부호보존 8축 전 셀에서 Ω_1−blind, Ω_1−sham 의 supply Δ > 0)
#           ∧ detgrad_capture(Ω_1) < 0.90
#   PASS                                              -> DIRECTIONAL-POSITIVE
#   ¬PASS ∧ TOST(δ=DELTA_S) 등가 (vs blind ∧ vs lamperm)  -> EQUIVALENT-NULL (담체 부재)
#   ¬PASS ∧ (supply Δ vs blind < −DELTA_S ∧ p<α)          -> KILL
#   그 외                                              -> THEATER
#
# [계측 강제규칙 11종] ① control별 paired-t 전부(순서통계량 금지) ② SEM/paired-t 만 ③ disjoint
#  pilot MDE 사전계산+미달 abort ④ 정보채널 증명(V_info) ⑤ V-gate 를 헤드라인 detector(supply)에
#  ⑥ 부호보존 8축 PASS 내장 ⑦ 분기 실행가능 ⑧ pump 사전게이트 ⑨ 사후 detector 교체 금지(sha 동결)
#  ⑩ 음성은 TOST 등가로 ⑪ 헤드라인 DV 가 처치의 최적화 대상과 항등식 아님(supply ⊥ 장부; capture 게이트)
#  tune-to-green / tune-to-red 둘 다 금지.
# =============================================================================

# =============================================================================
# [REGATE · 사전등록 개정판 — 원본 run.py(sha 21ca4d1c…) + result.json 는 동결 보존]
#  원 런 판정 = INVALID.  사유: hard-gate V_info 를 `om_sel_z > 1.0` 으로 못박았는데 실측 0.93 (미달).
#  교란(confound)이 아니라 **임계값 오설정**이다: Ω 짝-점수 분포는 좌측 꼬리가 두꺼워(나쁜 융합이
#  크게 음수) 완벽한 argmax 조차 pool 평균의 ~0.93σ 위에만 앉는다(짝-pool 크기 ≈51, 상한 z≈7.2 이므로
#  '구조적 불가능'은 아니고 순수한 왜도(skew) 오설정). z 임계는 선택강도가 아니라 점수분포의 왜도를
#  재고 있었다 = 계측기 결함.
#  ⇒ 이 판은 **V_info 게이트 사양 하나만** 척도-불변형으로 교체한다 (규칙④의 본래 의도 그대로):
#       V_info = (Ω pool std > 0)                                  # 정보축에 분산이 있다
#              ∧ paired-t( selz[Ω_1] − selz[blind] ) > 0, p<α      # 처치가 그 축에서 비랜덤 선택
#              ∧ pair_match(s_lamperm, Ω_1) < 0.5                  # 점수가 Λ(control 이 못 보는 입력)의 함수
#  🚫 헤드라인 DV · 대조군 · 마진 · TOST · 부호축 · 판정분기는 **한 글자도 바꾸지 않는다**.
#  🚫 tune-to-green 방지: 원 런 결과를 이미 봤으므로 이 판은 **THIRD-disjoint seed 300–319**
#     (MDE pilot 700–719 · Fable 파일럿 950–985 와도 서로소)에서 **미관측 확증**한다.
# =============================================================================

import json
import math
import os
import sys
import time

import numpy as np

# ---------------- 기질 상수 (F2 5차와 동일) ----------------
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

SEEDS = list(range(300, 320))          # REGATE 확증: THIRD-disjoint (200–219 은 이미 봄)
PILOT_SEEDS = list(range(700, 720))    # REGATE MDE 전용 · 분석과 disjoint

DELTA_S = 1.0       # supply 마진 = TOST 등가 마진
DELTA_O = 0.02      # overload 마진 (보조)
ALPHA = 0.05
CAPTURE_MAX = 0.90  # detgrad-capture 상한 (초과 = 장부 항등식 해석)

REPAIR_GRID = [0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30]
LIVE_LO, LIVE_HI = 0.50, 0.92
CEIL_FRAC = 0.95

OUT = os.path.dirname(os.path.abspath(__file__))

PRIMARY = "a_omega1"
CONTROLS = ["c2_blind", "s_lamperm", "a_detgrad"]     # PASS 가 이겨야 하는 셋
# arm -> (fission, fusion_policy, carrier_params)
ARMS = {
    "c1_frozen":     (None,    None,       {}),
    "c2_blind":      ("blind", "blind",    {}),
    "a_omega1":      ("blind", "omega",    {"k": 1}),
    "a_omega3":      ("blind", "omega",    {"k": 3}),
    "a_omega8":      ("blind", "omega",    {"k": 8}),
    "s_lamperm":     ("blind", "omega",    {"k": 1, "lam_perm": True}),
    "s_stressshuf":  ("blind", "omega",    {"k": 1, "stress_shuf": True}),
    "a_detgrad":     ("blind", "detgrad",  {}),
    "a_comp":        ("blind", "comp",     {}),
    "o6_oracle":     ("blind", "oracle",   {}),
    "a_omega1_mis":  ("blind", "omega",    {"k": 1, "mis": True}),
}
MAIN_ARMS = ("c1_frozen", "c2_blind", "a_omega1", "a_omega3", "a_omega8",
             "s_lamperm", "s_stressshuf", "a_detgrad", "a_comp", "o6_oracle",
             "a_omega1_mis")
SWEEP_ARMS = ("c2_blind", "s_lamperm", "a_omega1")
PILOT_ARMS = ("c2_blind", "a_omega1", "a_omega8")


def base_cfg(**kw):
    c = dict(rho=RHO, repair=None, sigma=1.0, capsplit="sym", B1=B1, EXC=EXC,
             feedback=True, frag_sigma=FRAG_SIGMA, merge="conservative")
    c.update(kw)
    return c


# ---------------- 기질 (5차와 동일) ----------------
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
    fp = f[rng_z.permutation(S)]          # Λ-순열 sham용 동결 site-field (동일 주변분포)
    return d, f, owner, cap, fp


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
    f0 = np.minimum(Le, Se)
    Lm = Le[:, None] + Le[None, :]
    Sm = Se[:, None] + Se[None, :]
    return np.minimum(Lm, Sm) - f0[:, None] - f0[None, :]


# ---------------- ★ 담체 Ω_k ----------------
def _relax(capv, Lv, Lamv, S0, k, B1c, EXCc, cc):
    """S ← cap·c/(r+c) 를 k회.  k=0 이면 S0 그대로 ⇒ Ω_0 ≡ 0."""
    Sv = np.maximum(S0, 1e-9)
    for _ in range(k):
        st = Lv / np.maximum(Sv, 1e-9)
        r = Lamv * (1.0 + B1c * np.clip(st - 1.0, 0.0, EXCc))
        Sv = capv * cc / (r + cc)
        Sv = np.maximum(Sv, 1e-9)
    return Sv


def _omega_matrix(ce, Le, Se, Lae, k, B1c, EXCc, cc):
    """Ω_k 짝-점수 행렬 (국소: i,j 의 (cap,L,S,Λ) 만)."""
    self_r = _relax(ce, Le, Lae, Se, k, B1c, EXCc, cc)
    Cm = ce[:, None] + ce[None, :]
    Lm = Le[:, None] + Le[None, :]
    Sm = Se[:, None] + Se[None, :]
    Lam_m = (Le[:, None] * Lae[:, None] + Le[None, :] * Lae[None, :]) / np.maximum(Lm, 1e-12)
    pair_r = _relax(Cm, Lm, Lam_m, Sm, k, B1c, EXCc, cc)
    return pair_r - self_r[:, None] - self_r[None, :]


# ---------------- FISSION (5차 그대로) ----------------
def _fission(state, aware, cfg, t, sibc):
    owner, cap, Dm, sib, cool, d, f, fp, rng = state
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
    return (owner, cap, Dm, sib, cool, d, f, fp, rng), created, 0


# ---------------- FUSION ----------------
def _fusion(state, policy, par, cfg, t, diag):
    owner, cap, Dm, sib, cool, d, f, fp, rng = state
    n = cap.size
    if n < 2:
        return state, 0.0, 1
    elig = np.flatnonzero(cool <= t)
    if elig.size < 2:
        return state, 0.0, 1

    L = _loads(owner, d, n)
    Sv = np.maximum(cap - Dm, 1e-9)
    Lam = _lam_units(owner, d, f, n)
    Le, Se, ce, Lae = L[elig], Sv[elig], cap[elig], Lam[elig]
    m = elig.size

    def compat(x, y):
        return not (sib[x] != -1 and sib[x] == sib[y])

    mask = np.zeros((m, m), dtype=bool)
    for x in range(m):
        for y in range(x + 1, m):
            mask[x, y] = compat(int(elig[x]), int(elig[y]))

    def argmax_pair(gain):
        gg = np.where(mask, gain, -np.inf)
        if not np.isfinite(gg).any():
            return -1, -1, gg
        bx, by = np.unravel_index(np.argmax(gg), gg.shape)
        return int(elig[bx]), int(elig[by]), gg

    def extreme_match(vals):
        lo_ord = [int(elig[k]) for k in np.argsort(vals, kind="stable")]
        hi_ord = [int(elig[k]) for k in np.argsort(-vals, kind="stable")]
        for x in lo_ord:
            for y in hi_ord:
                if x != y and compat(x, y):
                    return x, y
        return -1, -1

    cc = G * (1.0 - math.exp(-cfg["repair"]))
    B1c, EXCc = cfg["B1"], cfg["EXC"]
    om_true = _omega_matrix(ce, Le, Se, Lae, 1, B1c, EXCc, cc)  # 진단용 (Ω_1 기준)

    i = j = -1
    om_used = None
    if policy == "omega":
        k = par["k"]
        b1u, exu, ccu = B1c, EXCc, cc
        if par.get("mis"):
            b1u, exu, ccu = 3.0 * B1c, 0.5 * EXCc, 4.0 * cc     # 오설정 강건성
        cu, Lu, Su, Lau = ce, Le, Se, Lae
        if par.get("lam_perm"):                                  # Λ-순열 sham
            Lam_t = _lam_units(owner, d, fp, n)
            Lau = Lam_t[elig]
        if par.get("stress_shuf"):                               # 응력-셔플 sham
            pm = rng.permutation(m)
            cu, Lu, Su = ce[pm], Le[pm], Se[pm]
        om_used = _omega_matrix(cu, Lu, Su, Lau, k, b1u, exu, ccu)
        i, j, _ = argmax_pair(om_used)
    elif policy == "detgrad":
        i, j, _ = argmax_pair(_detgain_matrix(Le, Se))
    elif policy == "comp":
        i, j = extreme_match(Se - Le)
    elif policy == "oracle":
        f0 = np.minimum(Le, _eq_supply(ce, Dm[elig], Le, Lae, cfg))
        Cm = ce[:, None] + ce[None, :]
        Dmm = Dm[elig][:, None] + Dm[elig][None, :]
        Lm = Le[:, None] + Le[None, :]
        Laem = (Le[:, None] * Lae[:, None] + Le[None, :] * Lae[None, :]) / np.maximum(Lm, 1e-12)
        fm = np.minimum(Lm, _eq_supply(Cm.ravel(), Dmm.ravel(), Lm.ravel(),
                                       Laem.ravel(), cfg).reshape(m, m))
        i, j, _ = argmax_pair(fm - f0[:, None] - f0[None, :])
    else:  # blind
        order = [int(elig[k2]) for k2 in rng.permutation(m)]
        i = order[0]
        for c2 in order[1:]:
            if compat(i, c2):
                j = c2
                break
    if i == -1 or j == -1:
        return state, 0.0, 1

    if diag is not None:
        diag["n_fuse"] += 1
        diag["self_remerge"] += 1.0 if (sib[i] != -1 and sib[i] == sib[j]) else 0.0
        xi = int(np.flatnonzero(elig == i)[0]); xj = int(np.flatnonzero(elig == j)[0])
        lo_, hi_ = (xi, xj) if xi < xj else (xj, xi)
        # ④ 정보채널: Ω_1 pool 분산 + 선택쌍 z
        pool = om_true[mask]
        if pool.size > 1 and pool.std() > 1e-12:
            diag["om_pool_std"].append(float(pool.std()))
            diag["om_sel_z"].append(float((om_true[lo_, hi_] - pool.mean()) / pool.std()))
        # ⑪ detgrad-capture (장부 기울기 얼마나 타는가)
        dgm = _detgain_matrix(Le, Se)
        fin = np.where(mask, dgm, -np.inf)
        fv = fin[np.isfinite(fin)]
        gmax = float(fv.max()) if fv.size else 0.0
        diag["dg_capture"].append(float(dgm[lo_, hi_]) / gmax if abs(gmax) > 1e-12 else 1.0)
        bi, bj, _ = argmax_pair(dgm)
        diag["dg_match"] += 1.0 if {bi, bj} == {i, j} else 0.0
        # sham/arm 이 진짜 Ω_1 argmax 와 같은 쌍을 고르는 비율
        oi, oj, _ = argmax_pair(om_true)
        diag["om_match"] += 1.0 if {oi, oj} == {i, j} else 0.0
        diag["dg_n"] += 1

    lo, hi = (i, j) if i < j else (j, i)
    sup_before = (cap[lo] - Dm[lo]) + (cap[hi] - Dm[hi])
    owner = owner.copy()
    owner[owner == hi] = lo
    owner[owner > hi] -= 1
    cap = cap.copy(); Dm = Dm.copy(); sib = sib.copy(); cool = cool.copy()
    cap[lo] += cap[hi]; Dm[lo] += Dm[hi]
    sib[lo] = -1; cool[lo] = -1
    keep = np.arange(cap.size) != hi
    cap, Dm, sib, cool = cap[keep], Dm[keep], sib[keep], cool[keep]
    created = (cap[lo] - Dm[lo]) - sup_before
    return (owner, cap, Dm, sib, cool, d, f, fp, rng), float(created), 0


# ---------------- 한 run ----------------
def simulate(seed, arm, cfg):
    fis, fus, par = ARMS[arm]
    dyn = fis is not None

    rng_d = np.random.default_rng(10_000 + seed)
    rng_a = np.random.default_rng(90_000 + seed)
    rng_x = np.random.default_rng(70_000 + seed)
    rng_z = np.random.default_rng(50_000 + seed)

    d, f, owner, cap, fp = _init(rng_d, cfg["rho"], cfg["frag_sigma"], rng_z)
    Dm = np.zeros(N0)
    sib = np.full(N0, -1, dtype=np.int64)
    cool = np.full(N0, -1, dtype=np.int64)
    st = (owner, cap, Dm, sib, cool, d, f, fp, rng_a)
    sibc = [0]
    diag = {"n_fuse": 0, "self_remerge": 0.0, "om_pool_std": [], "om_sel_z": [],
            "dg_capture": [], "dg_match": 0.0, "om_match": 0.0, "dg_n": 0}
    pump = 0.0
    atp, hh, sup, ovl = [], [], [], []

    for t in range(T):
        d = _drift(d, rng_d)
        st = (st[0], st[1], st[2], st[3], st[4], d, f, fp, rng_a)
        if dyn:
            for _ in range(K_EV):
                st, cr, _ = _fission(st, fis == "aware", cfg, t, sibc)
                pump += cr
                st, cr, _ = _fusion(st, fus, par, cfg, t, diag if t >= WARM else None)
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
        st = (owner, cap, Dm, st[3], st[4], d, f, fp, rng_a)

    w = slice(WARM, T)
    mm = lambda v: float(np.mean(v)) if len(v) else float("nan")
    nf = diag["dg_n"]
    return dict(
        atp=float(np.mean(atp[w])), health=float(np.mean(hh[w])),
        supply=float(np.mean(sup[w])), overload=float(np.mean(ovl[w])),
        self_remerge=(diag["self_remerge"] / diag["n_fuse"]) if diag["n_fuse"] else 0.0,
        om_pool_std=mm(diag["om_pool_std"]), om_sel_z=mm(diag["om_sel_z"]),
        detgrad_capture=mm(diag["dg_capture"]),
        detgrad_match=(diag["dg_match"] / nf) if nf else float("nan"),
        omega_pair_match=(diag["om_match"] / nf) if nf else float("nan"),
        n_fuse=diag["n_fuse"],
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
    t = float(t)
    return t_sf(t, df) if t >= 0 else 1.0 - t_sf(-t, df)


def paired(e, c):
    dv = np.asarray(e) - np.asarray(c)
    n = dv.size
    m = float(dv.mean()); sd = float(dv.std(ddof=1))
    sem = sd / math.sqrt(n) if sd > 0 else 0.0
    tv = m / sem if sem > 0 else 0.0
    return {"mean": m, "sem": sem, "t": float(tv), "p": 2.0 * t_sf(tv, n - 1),
            "pos": int((dv > 0).sum()), "n": n}


def tost(e, c, delta):
    dv = np.asarray(e) - np.asarray(c)
    n = dv.size
    m = float(dv.mean()); sd = float(dv.std(ddof=1))
    sem = sd / math.sqrt(n) if sd > 0 else 1e-12
    df = n - 1
    p_lo = t_upper((m + delta) / sem, df)
    p_hi = t_upper(-((m - delta) / sem), df)
    pmax = max(p_lo, p_hi)
    return {"mean": m, "sem": sem, "delta": delta, "p_lower": p_lo, "p_upper": p_hi,
            "p_tost": pmax, "EQUIVALENT": bool(pmax < ALPHA)}


DIAG_KEYS = ("atp", "health", "supply", "overload", "self_remerge", "om_pool_std",
             "om_sel_z", "detgrad_capture", "detgrad_match", "omega_pair_match",
             "n_fuse", "pump", "cap_dev")


def grid(seeds, cfg, arms):
    out = {}
    for a in arms:
        per = [simulate(s, a, cfg) for s in seeds]
        g = {"supply_per_seed": [p["supply"] for p in per],
             "overload_per_seed": [p["overload"] for p in per],
             "atp_per_seed": [p["atp"] for p in per],
             "omselz_per_seed": [p["om_sel_z"] for p in per]}
        for k in DIAG_KEYS:
            v = np.array([p[k] for p in per], dtype=float)
            g[k] = float(np.nanmean(v)) if not np.all(np.isnan(v)) else float("nan")
        g["pump_max"] = float(max(abs(p["pump"]) for p in per))
        g["n_units"] = sorted(set(p["n_units"] for p in per))
        out[a] = g
    return out


def contrasts(gr, arm, key, ctrls):
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
        "hypothesis": "H_9287 · Ω(RELAX-k) 물리담체 확증",
        "question": "재조합 대수가 물리 정보를 더하는가 + 국소 관측으로 도달가능한가 (H_054·H_203)",
        "primary_arm": PRIMARY,
        "headline_DV": "warm-mean supply = Σ(cap−D) (파티션-불변 물리량)",
        "secondary_DV": "warm-mean overload = (stress>1) 비율",
        "excluded_DV": "장부 ATP=Σmin(L,S) — 보고만, PASS 조건 제외 (ΔATP>0 요구 삭제)",
        "controls_must_beat": CONTROLS,
        "seeds_main": SEEDS, "seeds_pilot_MDE": PILOT_SEEDS,
        "disjoint_from_fable_pilot_950_985": True,
        "reach_gate": "Ω_8 (오라클 아님) — supply Δ vs blind > DELTA_S ∧ p<α",
        "shams": ["s_lamperm = Λ-순열(site f 동결순열 → 동일 질량가중 규칙 재계산 · 융합불변)",
                  "s_stressshuf = (cap,L,S) 삼중항 순열 (응력-중항 채널 절단 · Λ 는 참)"],
        "PASS": "Ω_1 supply Δ>1.0 ∧ p<.05 vs {c2_blind, s_lamperm, a_detgrad} 셋 다 "
                "∧ overload 악화 없음 ∧ 부호보존 8축 전 셀 ∧ detgrad_capture<0.90",
        "branches": "¬hard→INVALID · PASS→DIRECTIONAL-POSITIVE · TOST(δ=1.0) 등가→EQUIVALENT-NULL · "
                    "supply 유의 악화→KILL · else THEATER",
        "sign_axes": ["repair", "sigma", "capsplit", "rho", "frag_sigma", "EXC", "B1", "feedback"],
        "delta_supply": DELTA_S, "delta_overload": DELTA_O, "alpha": ALPHA,
        "capture_max": CAPTURE_MAX}}

    # Ω_0 ≡ 0 정리 자체검사 (해석적 sanity)
    rr = np.random.default_rng(0)
    ce = rr.random(5) * 10 + 1; Se = rr.random(5) * 5 + .1
    Le = rr.random(5) * 5 + .1; Lae = rr.random(5) + .1
    om0 = _omega_matrix(ce, Le, Se, Lae, 0, B1, EXC, 10.0)
    R["theorem_check_omega0_max_abs"] = float(np.abs(om0).max())

    # ===== G3 · LIVE band 선등록 (CONTROL 만) =====
    ceiling = D_TOTAL
    scan = {}
    for r in REPAIR_GRID:
        g = grid(SEEDS, base_cfg(repair=r, feedback=False), ("c2_blind",))
        scan[r] = {"c2_health": g["c2_blind"]["health"], "c2_atp": g["c2_blind"]["atp"]}
    live = [r for r in REPAIR_GRID
            if LIVE_LO < scan[r]["c2_health"] < LIVE_HI and scan[r]["c2_atp"] < CEIL_FRAC * ceiling]
    R["G3_live_regime"] = {"scan_controls_only": scan, "live_band": live}
    if not live:
        R["verdict"] = {"HET": {"VERDICT": "INVALID"}, "LIVE": {"VERDICT": "INVALID"},
                        "why": "G3 실패"}
        json.dump(R, open(os.path.join(OUT, "result_regate.json"), "w"), indent=1, ensure_ascii=False)
        print("G3 FAIL"); sys.exit(0)
    R_PRIM = live[len(live) // 2]
    R["G3_live_regime"]["primary_repair"] = R_PRIM
    print("[G3] live=%s PRIMARY repair=%s (%.0fs)" % (live, R_PRIM, time.time() - t0))

    CFG = {"HET": base_cfg(repair=R_PRIM, feedback=False),
           "LIVE": base_cfg(repair=R_PRIM, feedback=True)}

    # ===== ③ MDE (disjoint pilot 600–619 · 도달성 축 = Ω_8) =====
    R["power"] = {}
    for nm in ("HET", "LIVE"):
        pg = grid(PILOT_SEEDS, CFG[nm], PILOT_ARMS)
        sd_s = float((np.array(pg[PRIMARY]["supply_per_seed"])
                      - np.array(pg["c2_blind"]["supply_per_seed"])).std(ddof=1))
        k = (2.093 + 0.861) / math.sqrt(len(SEEDS))
        mde = k * sd_s
        reach = float(np.mean(np.array(pg["a_omega8"]["supply_per_seed"])
                              - np.array(pg["c2_blind"]["supply_per_seed"])))
        R["power"][nm] = {
            "MDE_supply": mde, "sd_pair_omega1_blind": sd_s,
            "pilot_reach_omega8_minus_blind": reach,
            "pilot_omega1_minus_blind": float(np.mean(
                np.array(pg[PRIMARY]["supply_per_seed"]) - np.array(pg["c2_blind"]["supply_per_seed"]))),
            "reach_over_MDE": reach / mde if mde > 0 else 0.0,
            "POWERED": bool(reach > 3.0 * mde)}
        print("[MDE-%s] MDE=%.3f reach(Ω_8)=%.2f (%.1fx) POWERED=%s (%.0fs)"
              % (nm, mde, reach, reach / mde if mde > 0 else 0,
                 R["power"][nm]["POWERED"], time.time() - t0))

    # ===== 본 실험 =====
    R["main"] = {}
    for nm in ("HET", "LIVE"):
        g = grid(SEEDS, CFG[nm], MAIN_ARMS)
        con = {}
        for a in ("a_omega1", "a_omega3", "a_omega8", "a_omega1_mis", "s_lamperm",
                  "s_stressshuf", "a_detgrad", "a_comp", "o6_oracle"):
            con[a] = {dv: contrasts(g, a, dv + "_per_seed", CONTROLS + ["c2_blind"])
                      for dv in ("supply", "overload", "atp")}
            # 중복 c2_blind 제거
            for dv in ("supply", "overload", "atp"):
                con[a][dv].pop("_pooled_mean", None)
                con[a][dv]["_pooled_mean"] = float(np.mean(
                    [con[a][dv][c]["mean"] for c in CONTROLS if c != a]))
        con["TOST_omega1_vs_blind_supply"] = tost(g[PRIMARY]["supply_per_seed"],
                                                  g["c2_blind"]["supply_per_seed"], DELTA_S)
        con["TOST_omega1_vs_lamperm_supply"] = tost(g[PRIMARY]["supply_per_seed"],
                                                    g["s_lamperm"]["supply_per_seed"], DELTA_S)
        con["TOST_omega1_vs_blind_overload"] = tost(g[PRIMARY]["overload_per_seed"],
                                                    g["c2_blind"]["overload_per_seed"], DELTA_O)
        con["omega8_vs_blind_supply"] = paired(g["a_omega8"]["supply_per_seed"],
                                               g["c2_blind"]["supply_per_seed"])
        con["lamperm_vs_blind_supply"] = paired(g["s_lamperm"]["supply_per_seed"],
                                                g["c2_blind"]["supply_per_seed"])
        con["stressshuf_vs_blind_supply"] = paired(g["s_stressshuf"]["supply_per_seed"],
                                                   g["c2_blind"]["supply_per_seed"])
        con["oracle_vs_blind_supply"] = paired(g["o6_oracle"]["supply_per_seed"],
                                               g["c2_blind"]["supply_per_seed"])
        con["comp_vs_blind_overload"] = paired(g["a_comp"]["overload_per_seed"],
                                               g["c2_blind"]["overload_per_seed"])
        con["omselz_omega1_vs_blind"] = paired(g[PRIMARY]["omselz_per_seed"],
                                               g["c2_blind"]["omselz_per_seed"])
        R["main"][nm] = {"arms": {a: {k: g[a][k] for k in DIAG_KEYS + ("pump_max", "n_units")}
                                  for a in MAIN_ARMS},
                         "contrasts": con}
        print("[main-%s] done (%.0fs)" % (nm, time.time() - t0))

    # ===== ⑥ 부호보존 스윕 (8축 · supply) =====
    base_axes = {
        "repair": [("repair", r) for r in live],
        "sigma": [("sigma", s) for s in (0.0, 0.5, 1.0)],
        "capsplit": [("capsplit", c) for c in ("sym", "load")],
        "rho": [("rho", x) for x in (0.70, 0.85, 1.00)],
        "frag_sigma": [("frag_sigma", x) for x in (0.5, 0.9)],
    }
    live_only = {"EXC": [("EXC", x) for x in (1.0, 2.0, 6.0)],
                 "B1": [("B1", x) for x in (1.5, 3.0, 6.0)]}
    R["sign_sweep"] = {}
    for nm in ("HET", "LIVE"):          # feedback 축 = HET/LIVE 두 블록 자체
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
                       "supply": {a: g[a]["supply"] for a in SWEEP_ARMS},
                       "overload": {a: g[a]["overload"] for a in SWEEP_ARMS}}
                for c in ("c2_blind", "s_lamperm"):
                    ps = paired(g[PRIMARY]["supply_per_seed"], g[c]["supply_per_seed"])
                    po = paired(g[PRIMARY]["overload_per_seed"], g[c]["overload_per_seed"])
                    row["sup_vs_%s" % c] = {k: ps[k] for k in ("mean", "sem", "t", "p", "pos")}
                    row["ovl_vs_%s" % c] = {k: po[k] for k in ("mean", "sem", "t", "p", "pos")}
                R["sign_sweep"][nm][ax]["%s=%s" % (key, val)] = row
            print("[sweep-%s] %s (%.0fs)" % (nm, ax, time.time() - t0))

    # ===== 게이트 · 판정 =====
    def gates_for(nm):
        M = R["main"][nm]["arms"]
        C = R["main"][nm]["contrasts"]
        dyn_arms = [a for a in MAIN_ARMS if a != "c1_frozen"]
        g1 = max(abs(M[a]["pump_max"]) for a in MAIN_ARMS)
        srm = max(M[a]["self_remerge"] for a in MAIN_ARMS)
        reach = C["omega8_vs_blind_supply"]
        return {
            "G1_pump_max": g1, "G1_PASS": bool(g1 <= 1e-9),
            "G2_self_remerge_max": srm, "G2_PASS": bool(srm < 1e-9),
            "G3_c2_health": M["c2_blind"]["health"], "G3_c2_atp": M["c2_blind"]["atp"],
            "G3_PASS": bool(LIVE_LO < M["c2_blind"]["health"] < LIVE_HI
                            and M["c2_blind"]["atp"] < CEIL_FRAC * ceiling),
            "V_cap_conserved": bool(max(M[a]["cap_dev"] for a in MAIN_ARMS) < 1e-6),
            "V_n_units": all(M[a]["n_units"] == [N0] for a in MAIN_ARMS),
            "V_info_om_pool_std": M[PRIMARY]["om_pool_std"],
            "V_info_om_sel_z": M[PRIMARY]["om_sel_z"],
            "V_info_blind_sel_z": M["c2_blind"]["om_sel_z"],
            "V_info_selz_mean": C["omselz_omega1_vs_blind"]["mean"],
            "V_info_selz_t": C["omselz_omega1_vs_blind"]["t"],
            "V_info_selz_p": C["omselz_omega1_vs_blind"]["p"],
            "V_info_PASS": bool(M[PRIMARY]["om_pool_std"] > 0
                                and C["omselz_omega1_vs_blind"]["mean"] > 0
                                and C["omselz_omega1_vs_blind"]["p"] < ALPHA
                                and M["s_lamperm"]["omega_pair_match"] < 0.5),
            "V_sham_lamperm_pair_match_with_omega": M["s_lamperm"]["omega_pair_match"],
            "V_sham_stressshuf_pair_match_with_omega": M["s_stressshuf"]["omega_pair_match"],
            "V_sham_valid": bool(M["s_lamperm"]["omega_pair_match"] < 0.5),
            "V_detgrad_capture_omega1": M[PRIMARY]["detgrad_capture"],
            "V_detgrad_capture_comp": M["a_comp"]["detgrad_capture"],
            "V_detgrad_match_omega1": M[PRIMARY]["detgrad_match"],
            "V_CAPTURE_PASS": bool(M[PRIMARY]["detgrad_capture"] < CAPTURE_MAX),
            "V_POWER": bool(R["power"][nm]["POWERED"]),
            "V_REACH_omega8_supply": reach["mean"], "V_REACH_p": reach["p"],
            "V_REACH_PASS": bool(reach["mean"] > DELTA_S and reach["p"] < ALPHA),
            "REPORT_oracle_supply": C["oracle_vs_blind_supply"]["mean"],
            "REPORT_comp_overload": C["comp_vs_blind_overload"]["mean"],
            "REPORT_comp_overload_p": C["comp_vs_blind_overload"]["p"],
            "n_dyn_arms": len(dyn_arms),
        }
    R["gates"] = {nm: gates_for(nm) for nm in ("HET", "LIVE")}

    def sign_scan(nm):
        det = {}; signs = []
        for ax, pts in R["sign_sweep"][nm].items():
            for pt, row in pts.items():
                for c in ("c2_blind", "s_lamperm"):
                    m = row["sup_vs_%s" % c]["mean"]
                    s = 1 if m > 0 else (-1 if m < 0 else 0)
                    det.setdefault(ax, {})[pt + "|" + c] = {"mean": round(m, 4), "sign": s}
                    signs.append(s)
        return all(s > 0 for s in signs), all(s < 0 for s in signs), det, len(signs), \
            sum(1 for s in signs if s > 0)

    R["verdict"] = {}
    for nm in ("HET", "LIVE"):
        gt = R["gates"][nm]
        Cs = R["main"][nm]["contrasts"][PRIMARY]["supply"]
        Co = R["main"][nm]["contrasts"][PRIMARY]["overload"]
        Ca = R["main"][nm]["contrasts"][PRIMARY]["atp"]
        TT = R["main"][nm]["contrasts"]["TOST_omega1_vs_blind_supply"]
        TT2 = R["main"][nm]["contrasts"]["TOST_omega1_vs_lamperm_supply"]
        s_pos, s_neg, sdet, ncell, nposcell = sign_scan(nm)

        BEAT = all(Cs[c]["mean"] > DELTA_S and Cs[c]["p"] < ALPHA for c in CONTROLS)
        ovl_m, ovl_p = Co["c2_blind"]["mean"], Co["c2_blind"]["p"]
        OVL_OK = bool(ovl_m <= 0.0 or ovl_p >= ALPHA)
        CAP_OK = gt["V_CAPTURE_PASS"]
        PASS = bool(BEAT and OVL_OK and s_pos and CAP_OK)
        EQUIV = bool(TT["EQUIVALENT"] and TT2["EQUIVALENT"])
        NEG = bool(Cs["c2_blind"]["mean"] < -DELTA_S and Cs["c2_blind"]["p"] < ALPHA)

        hard = all(gt[k] for k in ("G1_PASS", "G2_PASS", "G3_PASS", "V_cap_conserved",
                                   "V_n_units", "V_info_PASS", "V_sham_valid",
                                   "V_POWER", "V_REACH_PASS"))
        if not hard:
            vd = "INVALID"
        elif PASS:
            vd = "DIRECTIONAL-POSITIVE"
        elif EQUIV:
            vd = "EQUIVALENT-NULL"
        elif NEG:
            vd = "KILL"
        else:
            vd = "THEATER"

        R["verdict"][nm] = {
            "primary": PRIMARY,
            "SUPPLY_vs": {c: {k: Cs[c][k] for k in ("mean", "sem", "t", "p", "pos")}
                          for c in CONTROLS},
            "SUPPLY_pooled_mean": Cs["_pooled_mean"],
            "OVERLOAD_vs": {c: {k: Co[c][k] for k in ("mean", "sem", "t", "p", "pos")}
                            for c in CONTROLS},
            "ATP_vs_blind_REPORT_ONLY": {k: Ca["c2_blind"][k] for k in ("mean", "sem", "t", "p")},
            "TOST_supply_vs_blind": TT, "TOST_supply_vs_lamperm": TT2,
            "TOST_overload_vs_blind": R["main"][nm]["contrasts"]["TOST_omega1_vs_blind_overload"],
            "BEAT_all_controls": BEAT, "OVL_OK": OVL_OK, "SIGN_ALL_POS": bool(s_pos),
            "sign_cells_pos": nposcell, "sign_cells_total": ncell,
            "CAPTURE_OK": CAP_OK, "detgrad_capture": gt["V_detgrad_capture_omega1"],
            "PASS": PASS, "EQUIV": EQUIV, "NEG": NEG, "hard_gates": bool(hard),
            "supply_sign_detail": sdet, "VERDICT": vd}

    R["wall_s"] = round(time.time() - t0, 1)
    json.dump(R, open(os.path.join(OUT, "result_regate.json"), "w"), indent=1, ensure_ascii=False)

    print("\n=============== RESULT (H_9287 Ω REGATE · seeds 300-319) ===============")
    print("theorem Ω_0 max|·| = %.2e" % R["theorem_check_omega0_max_abs"])
    for nm in ("HET", "LIVE"):
        gt = R["gates"][nm]; v = R["verdict"][nm]; A = R["main"][nm]["arms"]
        print("\n--- %s ---" % nm)
        print("  G1=%s(%.1e) G2=%s G3=%s(h=%.3f) POWER=%s REACH(Ω_8)=%s(%+.2f p=%.2g) "
              "INFO=%s(z=%.2f) SHAM=%s(match=%.2f) CAPTURE=%s(%.3f | comp=%.3f)"
              % (gt["G1_PASS"], gt["G1_pump_max"], gt["G2_PASS"], gt["G3_PASS"], gt["G3_c2_health"],
                 gt["V_POWER"], gt["V_REACH_PASS"], gt["V_REACH_omega8_supply"], gt["V_REACH_p"],
                 gt["V_info_PASS"], gt["V_info_om_sel_z"], gt["V_sham_valid"],
                 gt["V_sham_lamperm_pair_match_with_omega"], gt["V_CAPTURE_PASS"],
                 gt["V_detgrad_capture_omega1"], gt["V_detgrad_capture_comp"]))
        for a in MAIN_ARMS:
            print("   %-13s sup=%7.3f ovl=%.4f atp=%6.2f cap=%.3f z=%5.2f pump=%+.1e"
                  % (a, A[a]["supply"], A[a]["overload"], A[a]["atp"],
                     A[a]["detgrad_capture"], A[a]["om_sel_z"], A[a]["pump_max"]))
        for c in CONTROLS:
            s = v["SUPPLY_vs"][c]; o = v["OVERLOAD_vs"][c]
            print("   Ω_1 − %-10s  supply %+7.3f±%.3f (t=%+.1f p=%.2g %2d/20) | ovl %+.4f (p=%.2g)"
                  % (c, s["mean"], s["sem"], s["t"], s["p"], s["pos"], o["mean"], o["p"]))
        print("   TOST vs blind p=%.3g EQUIV=%s | ATP(report-only) %+.2f (p=%.2g)"
              % (v["TOST_supply_vs_blind"]["p_tost"], v["TOST_supply_vs_blind"]["EQUIVALENT"],
                 v["ATP_vs_blind_REPORT_ONLY"]["mean"], v["ATP_vs_blind_REPORT_ONLY"]["p"]))
        print("   SIGN %d/%d cells + | BEAT=%s OVL_OK=%s CAPTURE_OK=%s hard=%s  >>> VERDICT=%s"
              % (v["sign_cells_pos"], v["sign_cells_total"], v["BEAT_all_controls"],
                 v["OVL_OK"], v["CAPTURE_OK"], v["hard_gates"], v["VERDICT"]))
    print("\nwall_s", R["wall_s"])


if __name__ == "__main__":
    main()
