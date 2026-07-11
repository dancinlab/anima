#!/usr/bin/env python3
# =============================================================================
# H_9274 / F2 — 3rd FIRE ($0 · numpy · CPU-local · mini · OMP=2)
#
#   "재조합(merge) 대수가 정보를 더하는가?"  (H_054 symbiogenesis · H_203 asym-merge)
#
# 1차 = ⛔INVALID (연산자가 무에서 supply를 창조하는 펌프 · 카드 규약을 부정으로 코딩)
# 2차 = ⛔INVALID (대수중립은 확보했으나 헤드라인이 repair sink 상수 한 점(0.01)에 얹혔고
#                  그 점이 정확히 부호 영점 · 등록 레짐이 사망구역(c2 health 0.085))
#
# ============================ 사전등록 (PRE-REGISTRATION) ======================
# 아래는 실행 전 고정. 결과를 본 뒤 상수/규약/arm/판정식을 옮기지 않는다.
#
# --- 기질(substrate) 재설계 : 2차의 두 자유도(sink 부호영점 · 사망레짐)를 대수로 제거 ---
#  병변을 스칼라 damage MASS D_i ∈ [0, c_i] 로 표현:  supply_i = c_i − D_i.
#  각 site s 에 **외생 고정 취약도** f_s ~ lognormal 을 준다(부하와 무관·불변).
#  유닛 고유 손상률  Λ_i = Σ_{s∈i} d_s f_s / Σ_{s∈i} d_s   (부하-가중 평균 취약도).
#  damage step (질량선형·shape-free):
#     rate_i = Λ_i · (1 + B1·clip(stress_i−1, 0, EXC))       [LIVE, feedback ON]
#            = Λ_i                                            [HET,  feedback OFF]
#     dD⁺ = (c_i−D_i)·(1 − exp(−rate_i·u /G))    u ~Gamma(4,¼), E[u]=1
#     dD⁻ = D_i      ·(1 − exp(−r·u'))           u'~Gamma(4,¼)
#  이 표현에서:
#   • merge 순간은 대수중립: c←c_a+c_b, D←D_a+D_b  → supply EXACT 보존, pump=0 (G1).
#     (1차의 O(500)/run 무-창조 펌프 = D1_unweighted_mean 진단으로 재현·격리.)
#   • merge 후 유닛의 손상률 Λ_merged = (L_aΛ_a + L_bΛ_b)/(L_a+L_b) = **두 Λ의 볼록결합**.
#     φ(Λ)=1−exp(−Λ/G) 가 Λ 에 **오목** 하므로 취약(고Λ)+건강(저Λ) 을 붙이면 미래 총
#     손상생성이 준다 = **complementation**(카드의 '융합=손상 희석'의 물리적 정체).
#     이것은 순간펌프가 아니라 *미래 동역학*의 이득이므로 회계착시가 아니다.
#
# --- 두 기질 (사전등록 · 둘 다 무조건 보고) ---
#  HET  (PRIMARY 기질) : feedback OFF. health 변이는 오직 외생 취약도에서 온다.
#        ⇒ health-aware 선택이 부하와 **독립**이고, merge 가 미래 부하에 되먹임 없음.
#        = "재조합 대수가 정보를 더하는가"의 **순수형**(2차의 되먹임 nuisance 제거).
#  LIVE (현실 기질)    : feedback ON. 취약도 + 부하되먹임. 두 채널 공존(현실적·교란有).
#  (둘 다 health 가 유의미하게 변이 ⇒ health-policy 가 작동. 2차의 uniform-health NULL 폐기.)
#
# --- 정보 사다리 (arm · cherry-pick 방지 · 전부 사전등록) ---
#   c1_frozen    동역학 0
#   c2_blind     동일 예산 · health-blind 랜덤 페어링          ← 헤드라인 통제 ①
#   a5_sham      **aware와 동일 선택기**(최저 2개) · 신호=frozen tag(health 무관)  ← 통제 ②
#                 = blind 와 분포적으로 구별(지속 타깃팅) · tag ⊥ health 실증
#   a3_awarefuse ★PRIMARY  — 카드 문자 "저-health 쌍 fuse"(health 만 사용)
#   a3b_asym     ★CO-PRIMARY — H_203 host-preserve 비대칭 merge: 최저×최고 health
#                 (= complementation 이 실제로 일어나는 쌍)
#   o8_hihealth  진단: 카드 정반대(최고 2개)
#   o6_oracle    헤드룸 계측기 — 모델(Λ,r) + 전 상태로 정상상태 ATP 최대화
#                 **오라클이 blind 를 못 이기면 도달범위 미증명 ⇒ INVALID** (2차에서 졌다)
#   exp_aware_ff aware fission + aware fusion (2차)
#   guard_off_a3 sibling-ban/쿨다운 OFF (G2 degeneracy 진단)
#
# --- 헤드라인 대비 : vs_sham AND vs_c2 (둘 다 동일 merge 횟수·동일 대수) ---
#   ⇒ 두 대비는 '어느 쌍을 고르나'(=정보)만 격리. vs_c1_frozen 은 보고만(정지 대비는
#     정보채널과 무관 — 2차 REFUTE §3 지적 반영). PASS 는 vs_sham·vs_c2 로만 채점.
#
# --- 사전 예측 (실행 전 기록) ---
#   Λ_merged 볼록결합 ⇒ 저-health 2개(둘 다 고Λ) 융합은 고Λ 유지 = 희석 0.
#   ⇒ **예측: a3(카드 문자) ≤ 0 · a3b(비대칭) > 0** (complementation 은 unlike 쌍에서만).
#   (카드 정책 §1 "저-health 쌍 fuse" 는 카드 렌즈 §family "융합=손상 희석" 과 모순이다.
#    이 발사는 그 모순을 코드로 노출하고 어느 쪽이 정보를 나르는지 판정한다.)
#
# --- 3게이트 (INVALID_REFIRE.md §6) ---
#  G1 ALGEBRAIC-NEUTRALITY : arm별 순간 pump(ops_supply_created) ≤ 1e-9.  (하드)
#      (제외 대상 = 1차의 O(500)/run. cumulative float roundoff ~1e-13 이므로
#       threshold 1e-9 = 신호 O(1) 보다 9자릿수 아래. D1 진단이 위반 변종에서 펌프 재현.)
#  G2 DEGENERACY           : 영구 sibling-ban + COOL=2 · self_remerge=0 실측.  (하드)
#  G3 LIVE-REGIME 선등록    : **CONTROL만 보고**(c2_blind) repair 격자 스캔 →
#      살아있는 구간 { r : 0.50<health(c2)<0.92  AND  atp(c2)<0.95×ceiling } 확정,
#      PRIMARY r = 그 구간 **중앙값**(결정적 · 처치 미peek). live band 공집합 → INVALID.
#      V1_liveness = **양쪽**(하단 붕괴 + 상단 포화) 차단.                    (하드)
#  ORACLE-REACH            : o6 오라클이 blind 를 유의하게 이겨야(도달범위 실재). (하드)
#
# --- 계측 강제규칙 7종 ---
#  ① control별 paired-t 전부 + pooled-mean (Δ=exp−max(controls) 금지).
#  ② SEM/paired-t 만 (mean vs 1·std 금지).
#  ③ 사전 MDE : pilot seed 900–919 (분석 seed 0–19 와 disjoint) · 처치가 도달하는 축
#     (fusion-target 정책축) span 으로 · span>3×MDE 미달 시 **코드가 abort**. 사후 span 금지.
#  ④ 정보채널 증명 : a3 결정변수=health=f(D) (sham/blind 안봄) · sham 결정변수=frozen tag
#     (health 무관, 중립 arm 에서 corr(tag,h)≈0 실증) · 운영대역 var(h)>0.
#  ⑤ V-gate 는 헤드라인 detector(ATP) 그 자체에.
#  ⑥ **부호보존** : 부호를 뒤집을 수 있는 자유 축 전부 열거 · 각 점 부호보존이 PASS 조건.
#     (a) repair r [live band 전 점] (b) sigma{0,.5,1} (c) capsplit{sym,load}
#     (d) rho{.7,.85,1} (e) frag_sigma{.5,.9} (f) EXC{1,2,6}·B1{1.5,3}[LIVE].
#     한 점에서라도 뒤집히면 PASS 아님 = 모델 산물 = INVALID.
#     (융합 규약축 = G1 이 D_a+D_b 로 유일해 강제 → 자유도 0 · D1 진단으로 실증.)
#  ⑦ KILL/PASS 분기 실행가능 : pilot 에서 policy-axis span > MARGIN 먼저 확인.
#
#  seed=20 · paired-CRN(수요 스트림 arm 무관 동일). tune-to-green / tune-to-red 금지.
#  p5 : emit/silence 경로가 코드에 부재 (구조 레인 전용).
# =============================================================================

import json
import math
import os
import sys
import time

import numpy as np

# ---------------- 사전등록 상수 ----------------
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
FRAG_BASE = 0.70          # 취약도 스케일 (health 를 live band 로)
FRAG_SIGMA = 0.70         # 취약도 이질성 (health 변이 원천)

SEEDS = list(range(20))
PILOT_SEEDS = list(range(900, 920))

MARGIN = 1.0
ALPHA = 0.05

REPAIR_GRID = [0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30]
LIVE_LO, LIVE_HI = 0.50, 0.92
CEIL_FRAC = 0.95

OUT = os.path.dirname(os.path.abspath(__file__))
CONTROLS = ["c1_frozen", "c2_blind", "a5_sham"]
PRIMARY = "a3_awarefuse"
COPRIMARY = "a3b_asym"

ARMS = {
    "c1_frozen":    (None, None),
    "c2_blind":     ("blind", "blind"),
    "a5_sham":      ("blind", "sham"),
    "a3_awarefuse": ("blind", "aware"),
    "a3b_asym":     ("blind", "asym"),
    "o8_hihealth":  ("blind", "hi_health"),
    "o6_oracle":    ("blind", "oracle"),
    "exp_aware_ff": ("aware", "aware"),
    "guard_off_a3": ("blind", "aware"),
}
MAIN_ARMS = ("c1_frozen", "c2_blind", "a5_sham", "a3_awarefuse", "a3b_asym",
             "o8_hihealth", "o6_oracle", "exp_aware_ff", "guard_off_a3")
POLICY_AXIS = ("c2_blind", "a5_sham", "a3_awarefuse", "a3b_asym",
               "o8_hihealth", "o6_oracle")
SWEEP_ARMS = ("c1_frozen", "c2_blind", "a5_sham", "a3_awarefuse", "a3b_asym")
GUARD_OFF = {"guard_off_a3"}


def base_cfg(**kw):
    c = dict(rho=RHO, repair=None, sigma=1.0, capsplit="sym", B1=B1, EXC=EXC,
             feedback=True, frag_sigma=FRAG_SIGMA, merge="conservative")
    c.update(kw)
    return c


# ---------------- 기질 ----------------
def _init(rng, rho, frag_sigma):
    d = np.exp(rng.normal(0.0, 0.6, size=S))
    d *= D_TOTAL / d.sum()
    f = FRAG_BASE * np.exp(rng.normal(0.0, frag_sigma, size=S))   # 외생 고정 취약도
    perm = rng.permutation(S)
    groups = np.array_split(perm, N0)
    C_total = D_TOTAL / rho
    owner = np.empty(S, dtype=np.int64)
    cap = np.empty(N0)
    for k, g in enumerate(groups):
        owner[g] = k
        cap[k] = C_total * d[g].sum() / D_TOTAL
    return d, f, owner, cap


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
    """유닛 고유 손상률 Λ_i = 부하-가중 평균 취약도 (composition 의 결정함수)."""
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


# ---------------- FISSION = 부하분산 + 손상 격리 (질량보존) ----------------
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
    tag = np.append(tag, tag[i])                 # 자손 tag 상속 (health 무관)
    sib = np.append(sib, sid); sib[i] = sid
    cool = np.append(cool, t + COOL); cool[i] = t + COOL
    created = (ca - Da) + (cb - Db) - sup_before
    return (owner, cap, Dm, tag, sib, cool, d, f, rng), created, 0


# ---------------- FUSION = 손상 희석 (G1 이 D_a+D_b 강제) ----------------
def _fusion(state, policy, cfg, t, guards, diag):
    owner, cap, Dm, tag, sib, cool, d, f, rng = state
    n = cap.size
    if n < 2:
        return state, 0.0, 1
    elig = np.flatnonzero(cool <= t) if guards else np.arange(n)
    if elig.size < 2:
        return state, 0.0, 1

    h = 1.0 - Dm[elig] / cap[elig]
    tg = tag[elig]

    def compat(x, y):
        if not guards:
            return True
        return not (sib[x] != -1 and sib[x] == sib[y])

    i = j = -1
    if policy == "oracle":
        L = _loads(owner, d, n)
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
    elif policy == "asym":
        lo_ord = [int(elig[k]) for k in np.argsort(h, kind="stable")]
        hi_ord = [int(elig[k]) for k in np.argsort(-h, kind="stable")]
        for x in lo_ord:
            for y in hi_ord:
                if x != y and compat(x, y):
                    i, j = x, y
                    break
            if i != -1:
                break
        if i == -1:
            return state, 0.0, 1
    else:
        if policy == "aware":
            order = [int(elig[k]) for k in np.argsort(h, kind="stable")]
        elif policy == "sham":
            order = [int(elig[k]) for k in np.argsort(tg, kind="stable")]
        elif policy == "hi_health":
            order = [int(elig[k]) for k in np.argsort(-h, kind="stable")]
        else:
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
        diag["h_std"].append(float(h.std()))
        hi_, hj_ = float(1.0 - Dm[i] / cap[i]), float(1.0 - Dm[j] / cap[j])
        diag["sel_gap"].append(0.5 * (hi_ + hj_) - float(h.mean()))
        diag["h_spread_sel"].append(abs(hi_ - hj_))
        diag["tagpick"].append(0.5 * (float(tag[i]) + float(tag[j])))
        diag["corr_th"].append((tg.copy(), h.copy()))

    lo, hi = (i, j) if i < j else (j, i)
    sup_before = (cap[lo] - Dm[lo]) + (cap[hi] - Dm[hi])
    owner = owner.copy()
    owner[owner == hi] = lo
    owner[owner > hi] -= 1
    cap = cap.copy(); Dm = Dm.copy(); tag = tag.copy()
    sib = sib.copy(); cool = cool.copy()
    clo, chi = float(cap[lo]), float(cap[hi])
    tag[lo] = (clo * tag[lo] + chi * tag[hi]) / (clo + chi)
    if cfg["merge"] == "conservative":               # G1 강제
        cap[lo] += cap[hi]; Dm[lo] += Dm[hi]
    else:                                            # D1 진단(G1 위반): health 단순평균
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

    rng_d = np.random.default_rng(10_000 + seed)   # 수요·취약도 (arm 무관 · paired-CRN)
    rng_a = np.random.default_rng(90_000 + seed)   # 정책/행동
    rng_x = np.random.default_rng(70_000 + seed)   # damage/repair 노이즈
    rng_t = np.random.default_rng(50_000 + seed)   # frozen tag

    d, f, owner, cap = _init(rng_d, cfg["rho"], cfg["frag_sigma"])
    Dm = np.zeros(N0)
    tag = rng_t.random(N0)
    sib = np.full(N0, -1, dtype=np.int64)
    cool = np.full(N0, -1, dtype=np.int64)
    st = (owner, cap, Dm, tag, sib, cool, d, f, rng_a)
    sibc = [0]
    diag = {"n_fuse": 0, "self_remerge": 0.0, "h_std": [], "sel_gap": [],
            "h_spread_sel": [], "tagpick": [], "corr_th": []}
    pump = 0.0
    atp, hh, sup, ovl, chn = [], [], [], [], []
    same_prev = None
    iu = np.triu_indices(S, 1)

    for t in range(T):
        d = _drift(d, rng_d)
        owner, cap, Dm, tag, sib, cool = st[0], st[1], st[2], st[3], st[4], st[5]
        st = (owner, cap, Dm, tag, sib, cool, d, f, rng_a)   # refresh drifted d
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
    if diag["corr_th"]:
        tv = np.concatenate([x[0] for x in diag["corr_th"]])
        hv = np.concatenate([x[1] for x in diag["corr_th"]])
        cth = float(np.corrcoef(tv, hv)[0, 1]) if tv.std() > 1e-9 and hv.std() > 1e-9 else 0.0
    else:
        cth = 0.0
    return dict(
        atp=float(np.mean(atp[w])), health=float(np.mean(hh[w])),
        supply=float(np.mean(sup[w])), overload=float(np.mean(ovl[w])),
        churn=float(np.mean(chn[w])),
        self_remerge=(diag["self_remerge"] / diag["n_fuse"]) if diag["n_fuse"] else 0.0,
        h_std=mm(diag["h_std"]), sel_gap=mm(diag["sel_gap"]),
        h_spread_sel=mm(diag["h_spread_sel"]), tag_pick_mean=mm(diag["tagpick"]),
        corr_tag_h=cth, pump=float(pump), n_units=int(st[1].size),
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
                  "h_std", "sel_gap", "h_spread_sel", "tag_pick_mean", "corr_tag_h",
                  "pump", "cap_dev"):
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
        "primary": PRIMARY + " = 카드 문자 '저-health 쌍 fuse'",
        "coprimary": COPRIMARY + " = H_203 host-preserve 비대칭 merge (최저×최고)",
        "headline_contrasts": "vs_sham AND vs_c2 (동일 merge 횟수·동일 대수 → 정보만 격리)",
        "prediction_before_run": "Λ_merged 볼록결합 ⇒ 저-health 2개 융합은 희석 0 "
                                 "⇒ 예측 a3 ≤ 0 < a3b. a3 양성이면 예측이 틀린 것.",
        "controls": CONTROLS, "margin_atp": MARGIN, "alpha": ALPHA,
        "seeds": SEEDS, "pilot_seeds": PILOT_SEEDS,
        "substrates": {"HET": "외생 고정 취약도 · feedback OFF (순수 대수 질문)",
                       "LIVE": "취약도 + 부하되먹임 ON (현실·교란有)"},
        "sign_axes": ["repair(live band)", "sigma{0,.5,1}", "capsplit{sym,load}",
                      "rho{.7,.85,1}", "frag_sigma{.5,.9}", "EXC{1,2,6}[LIVE]",
                      "B1{1.5,3}[LIVE]", "fusion-convention(G1 유일해 강제·자유도0)"]}}

    # ===== G3 · LIVE-REGIME 선등록 (CONTROL만) — HET 기질 기준 =====
    ceiling = D_TOTAL
    scan = {}
    for r in REPAIR_GRID:
        g = grid(SEEDS, base_cfg(repair=r, feedback=False), ("c1_frozen", "c2_blind"))
        scan[r] = {"c2_health": g["c2_blind"]["health"], "c2_atp": g["c2_blind"]["atp"],
                   "c1_health": g["c1_frozen"]["health"], "c1_atp": g["c1_frozen"]["atp"]}
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
        R["power"][nm] = {"sd_pilot_a3_minus_sham": sd, "MDE": mde,
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
               ("a3_awarefuse", "a3b_asym", "o6_oracle", "o8_hihealth",
                "exp_aware_ff", "guard_off_a3")}
        con["o6_vs_c2"] = paired(g["o6_oracle"]["atp_per_seed"], g["c2_blind"]["atp_per_seed"])
        con["sham_vs_c2"] = paired(g["a5_sham"]["atp_per_seed"], g["c2_blind"]["atp_per_seed"])
        R["main"][nm] = {"arms": {a: {k: g[a][k] for k in
                                      ("atp", "health", "supply", "overload", "churn",
                                       "self_remerge", "h_std", "sel_gap", "h_spread_sel",
                                       "tag_pick_mean", "corr_tag_h", "pump", "pump_max",
                                       "cap_dev", "n_units")} for a in MAIN_ARMS},
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
                for arm in (PRIMARY, COPRIMARY):
                    for c in ("a5_sham", "c2_blind"):
                        pr = paired(g[arm]["atp_per_seed"], g[c]["atp_per_seed"])
                        row["%s_vs_%s" % (arm, c)] = {k: pr[k] for k in
                                                      ("mean", "sem", "t", "p", "pos")}
                R["sign_sweep"][nm][ax]["%s=%s" % (key, val)] = row
            print("[sweep-%s] %s (%.1fs)" % (nm, ax, time.time() - t0))

    # ===== G1 진단: 융합 규약 자유도가 없는가 (G1 위반 = unweighted mean) =====
    gD = grid(SEEDS[:10], base_cfg(repair=R_PRIM, feedback=False, merge="unweighted_mean"),
              ("c2_blind", PRIMARY, COPRIMARY))
    R["G1_convention_freedom_diag"] = {
        "note": "G1(supply EXACT 보존)은 merge 순간 D←D_a+D_b 를 유일하게 강제. "
                "health 단순평균 merge 는 G1 위반 → 순간 pump≠0 = 1차 회계착시로 회귀.",
        "unweighted_mean_pump_per_run": {a: gD[a]["pump"] for a in gD},
        "unweighted_mean_pump_max": {a: gD[a]["pump_max"] for a in gD}}

    # ===== 게이트 =====
    def gates_for(nm):
        M = R["main"][nm]["arms"]
        C = R["main"][nm]["contrasts"]
        g1 = max(abs(M[a]["pump_max"]) for a in MAIN_ARMS)
        selg_a3, selg_sham = M[PRIMARY]["sel_gap"], M["a5_sham"]["sel_gap"]
        corr_neutral = M["c2_blind"]["corr_tag_h"]
        tagpick_sham, tagpick_blind = M["a5_sham"]["tag_pick_mean"], M["c2_blind"]["tag_pick_mean"]
        return {
            "G1_pump_max": g1, "G1_PASS": bool(g1 <= 1e-9),
            "G2_self_remerge_max": max(M[a]["self_remerge"] for a in MAIN_ARMS
                                       if a not in GUARD_OFF),
            "G2_guardoff_self_remerge": M["guard_off_a3"]["self_remerge"],
            "G2_PASS": bool(max(M[a]["self_remerge"] for a in MAIN_ARMS
                                if a not in GUARD_OFF) < 1e-9),
            "G3_c2_health": M["c2_blind"]["health"], "G3_c2_atp": M["c2_blind"]["atp"],
            "G3_PASS_live_both_sided": bool(LIVE_LO < M["c2_blind"]["health"] < LIVE_HI
                                            and M["c2_blind"]["atp"] < CEIL_FRAC * ceiling),
            "V_cap_conserved": bool(max(M[a]["cap_dev"] for a in MAIN_ARMS) < 1e-6),
            "V_n_units": all(M[a]["n_units"] == [N0] for a in MAIN_ARMS),
            "V_info_var_h": M[PRIMARY]["h_std"],
            "V_selgap_a3": selg_a3, "V_selgap_sham": selg_sham,
            "V_tag_health_blind_corr_neutral": corr_neutral,
            "V_tagpick_sham_vs_blind": {"sham": tagpick_sham, "blind": tagpick_blind},
            "V_sham_distinct_from_blind": bool(abs(tagpick_sham - 0.5) > 0.05),
            "V_info_PASS": bool(abs(corr_neutral) < 0.10 and M[PRIMARY]["h_std"] > 1e-3
                                and selg_a3 < -1e-3 and abs(selg_sham) < 0.05),
            "V_POWER_PASS": bool(R["power"][nm]["POWERED"]),
            "ORACLE_o6_minus_c2": C["o6_vs_c2"]["mean"], "ORACLE_p": C["o6_vs_c2"]["p"],
            "ORACLE_VALID": bool(C["o6_vs_c2"]["mean"] > 0 and C["o6_vs_c2"]["p"] < ALPHA),
        }
    R["gates"] = {nm: gates_for(nm) for nm in ("HET", "LIVE")}

    def sign_scan(nm, arm):
        """모든 자유 축·모든 점·두 통제에서 부호가 일관되는가 (대칭)."""
        det = {}; signs = []
        for ax, pts in R["sign_sweep"][nm].items():
            for pt, row in pts.items():
                for c in ("a5_sham", "c2_blind"):
                    m = row["%s_vs_%s" % (arm, c)]["mean"]
                    s = 1 if m > 0 else (-1 if m < 0 else 0)
                    det.setdefault(ax, {})[pt + "|" + c] = {"mean": round(m, 3), "sign": s}
                    signs.append(s)
        all_pos = all(s > 0 for s in signs)
        all_neg = all(s < 0 for s in signs)
        return all_pos, all_neg, det

    R["verdict"] = {}
    for nm in ("HET", "LIVE"):
        gt = R["gates"][nm]
        v = {}
        for arm in (PRIMARY, COPRIMARY):
            C = R["main"][nm]["contrasts"][arm]
            sok_pos, sok_neg, sdet = sign_scan(nm, arm)
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
                vd = "DIRECTIONAL-POSITIVE"          # 정보 나름 + 부호 전축 보존
            elif neg and sok_neg:
                vd = "KILL"                          # 정책이 해로움 + 부호 전축 보존 (licensed)
            elif sig or neg:
                vd = "INVALID"                       # ⑥ 유의하나 부호가 축에서 뒤집힘 = 모델 산물
            else:
                vd = "THEATER"                        # 헤드라인 대비 ≈ 0
            v[arm] = {"vs_sham": {k: C["a5_sham"][k] for k in ("mean", "sem", "t", "p", "pos")},
                      "vs_c2": {k: C["c2_blind"][k] for k in ("mean", "sem", "t", "p", "pos")},
                      "vs_c1_frozen_reportonly": {k: C["c1_frozen"][k] for k in
                                                  ("mean", "sem", "t", "p", "pos")},
                      "pooled_mean": C["_pooled_mean"],
                      "significant_both": bool(sig), "neg_both": bool(neg),
                      "SIGN_ALL_POS": bool(sok_pos), "SIGN_ALL_NEG": bool(sok_neg),
                      "hard_gates": bool(hard), "sign_detail": sdet, "VERDICT": vd}
        R["verdict"][nm] = v

    R["wall_s"] = round(time.time() - t0, 1)
    json.dump(R, open(os.path.join(OUT, "result.json"), "w"), indent=1, ensure_ascii=False)

    print("\n================ RESULT ================")
    print("사전예측: a3(카드문자) ≤ 0 · a3b(비대칭) > 0")
    for nm in ("HET", "LIVE"):
        print("\n--- %s 기질 ---" % nm)
        gt = R["gates"][nm]
        print("  G1=%s(%.1e) G2=%s G3=%s(h=%.3f atp=%.2f) POWER=%s(%.2fxMDE) ORACLE=%s(%+.2f p=%.3g) info=%s(corr=%+.3f selg_a3=%+.3f selg_sham=%+.3f) shamDistinct=%s(tagpick=%.3f)"
              % (gt["G1_PASS"], gt["G1_pump_max"], gt["G2_PASS"],
                 gt["G3_PASS_live_both_sided"], gt["G3_c2_health"], gt["G3_c2_atp"],
                 gt["V_POWER_PASS"], R["power"][nm]["span_over_MDE"],
                 gt["ORACLE_VALID"], gt["ORACLE_o6_minus_c2"], gt["ORACLE_p"],
                 gt["V_info_PASS"], gt["V_tag_health_blind_corr_neutral"],
                 gt["V_selgap_a3"], gt["V_selgap_sham"], gt["V_sham_distinct_from_blind"],
                 gt["V_tagpick_sham_vs_blind"]["sham"]))
        A = R["main"][nm]["arms"]
        for a in MAIN_ARMS:
            print("   %-14s atp=%6.2f h=%.3f sup=%6.2f churn=%.4f selgap=%+.3f spread=%.3f pump=%+.1e"
                  % (a, A[a]["atp"], A[a]["health"], A[a]["supply"], A[a]["churn"],
                     A[a]["sel_gap"], A[a]["h_spread_sel"], A[a]["pump_max"]))
        for arm in (PRIMARY, COPRIMARY):
            v = R["verdict"][nm][arm]
            print("   >> %-13s vs_sham %+7.3f±%.3f (t=%+6.2f p=%.3g %2d/20) | vs_c2 %+7.3f±%.3f (t=%+6.2f p=%.3g) | SIGN+=%s SIGN-=%s | %s"
                  % (arm, v["vs_sham"]["mean"], v["vs_sham"]["sem"], v["vs_sham"]["t"],
                     v["vs_sham"]["p"], v["vs_sham"]["pos"], v["vs_c2"]["mean"],
                     v["vs_c2"]["sem"], v["vs_c2"]["t"], v["vs_c2"]["p"],
                     v["SIGN_ALL_POS"], v["SIGN_ALL_NEG"], v["VERDICT"]))
    print("\nG1 규약자유도 진단(unweighted-mean=G1위반 pump/run):",
          {k: round(x, 1) for k, x in R["G1_convention_freedom_diag"]["unweighted_mean_pump_per_run"].items()})
    print("wall_s", R["wall_s"])


if __name__ == "__main__":
    main()
