#!/usr/bin/env python3
# H_9274 / F2 — REFIRE ($0 · numpy · CPU-local · mini)
# 원 판정 = ⛔ INVALID (REFUTE.md). 이 스크립트는 그 결함 5개를 고친 재발사다.
#
# ============================ 무엇을 고쳤나 =====================================
# (i)  카드 등록 규약을 그대로 구현.
#      카드 §family: "융합 = 손상 희석(content 평균화) · 분열 = 부하분산 + 손상 격리"
#        FUSION  = capacity-weighted CONTENT AVERAGE of the lesion field  (희석)
#        FISSION = ASYMMETRIC lesion SEGREGATION (자손 간 손상 비대칭 분배)  (격리)
#      원 run.py = FUSION `AND`(초선형 소거) · FISSION mtDNA 동일복사(격리 수학적 불가) = 카드의 부정.
#      lesion 상태를 bool -> [0,1] 연속장으로 올려 '평균화'와 '비대칭 분배'가 둘 다
#      표현 가능하게 했다.
# (ii) ALGEBRAIC NEUTRALITY (원 INVALID의 controls_fair 붕괴 원인 제거).
#      등록 규약에서 fission/fusion 두 연산 모두
#         (a) 총 capacity 보존   sum c_i
#         (b) 총 supply 보존     sum c_i * h_i   (= cap-weighted 손상질량 보존)
#      을 EXACT 하게 만족한다 -> 어떤 arm도 '연산 대수'에서 공짜 health를 못 얻는다.
#      (원 AND-융합은 blind 페어링에 공짜 손상소거 펌프를 줘서 c2를 인위적으로 강화했다.
#       본 코드는 ops_supply_created 로 그 펌프 질량을 arm별로 실측해 0임을 증명한다.)
# (iii) degenerate self-remerge 중립화: fission 자손 = 영구 SIBLING-BAN(서로 재융합 금지)
#      + COOL_FISS 스텝 fusion 쿨다운. 전 dynamic arm 동일 적용. self_remerge_frac 실측 보고.
# (iv) PRIMARY arm = a3 (aware-fusion only · blind fission) 사전등록. exp/a4 = 2차.
# (v)  MDE 사전계산(pilot seed 900-904, 분석 seed와 disjoint) + control별 paired-t.
#      max(controls) 금지. n=20 paired-CRN.
# (vi) 규약 강건성: 카드 충실 규약 4개(R1..R4)에서 부호 보존을 PASS 조건에 포함.
#      진단용 비-카드 규약 D1(원 run.py 대수) · D2 도 같이 돌려 부호 의존성을 노출.
#
# 금지 지표 미사용: conj_index / purity / acc-ATP 비율 / corr(n,demand).
# 헤드라인 detector = steady-state 전달 ATP (절대량, D_TOTAL=100 고정) 의 paired Δ.
# p5: emit/silence 경로가 코드에 존재하지 않는다(구조 레인 전용).

import json
import math
import os
import time

import numpy as np

# ---------------- 사전등록 상수 (원본 계승 · 실행 전 고정) ----------------
S = 64
N0 = 16
G = 32
T = 300
WARM = 150
K_EV = 2
B0 = 0.05
B1 = 3.0
EXC_CAP = 2.0
REPAIR = 0.01
D_TOTAL = 100.0

RHO_PRIMARY = 0.85
RHO_SWEEP = [0.70, 0.85, 1.00]

SEEDS = list(range(20))          # (v) n=20 · paired-CRN
PILOT_SEEDS = [900, 901, 902, 903, 904]   # MDE 전용 · 분석 seed와 disjoint

MARGIN = 1.0                     # ATP 단위 (= 총수요의 1% · 원 카드 margin_rel=0.01)
ALPHA = 0.05
COOL_FISS = 2                    # (iii) fission 자손 fusion 쿨다운(스텝)
MIN_CAP_FRAC = 0.05              # load-비례 cap 분할 하한 (전 arm 동일)

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- 규약(convention) ----------------
# fuse: "avg" = 카드(희석·capacity-weighted content average)
#       "min" = 비-카드 진단(원 run.py의 AND = 초선형 소거의 연속 아날로그)
# capsplit: "sym"(반반) | "load"(자손 부하 비례) — 둘 다 카드의 "부하분산"과 정합
# sigma: 손상 격리 강도. 1.0=완전 격리 · 0.5=부분 격리 · 0.0=동일복사(=비-카드, 원 run.py)
CONV_REGISTERED = [
    ("R1_avg_sym_seg1.0",  dict(fuse="avg", capsplit="sym",  sigma=1.0)),   # PRIMARY(카드 등록값)
    ("R2_avg_sym_seg0.5",  dict(fuse="avg", capsplit="sym",  sigma=0.5)),
    ("R3_avg_load_seg1.0", dict(fuse="avg", capsplit="load", sigma=1.0)),
    ("R4_avg_load_seg0.5", dict(fuse="avg", capsplit="load", sigma=0.5)),
]
CONV_DIAG = [
    ("D1_min_copy_ORIG",   dict(fuse="min", capsplit="sym",  sigma=0.0)),   # 원 run.py 대수
    ("D2_min_seg1.0",      dict(fuse="min", capsplit="sym",  sigma=1.0)),
]

# ---------------- arm ----------------
# (fission_policy, fusion_policy) · None = frozen
ARMS = {
    "c1_frozen":     (None, None),
    "c2_random_rw":  ("blind", "blind"),
    "a3_awarefuse":  ("blind", "aware"),   # ★ PRIMARY (iv)
    "a5_shamfuse":   ("blind", "sham"),    # V-gate: 동일 선택 기계 · health 정보만 파괴
    "a4_awarefiss":  ("aware", "blind"),
    "exp_aware_ff":  ("aware", "aware"),
    "guard_off_a3":  ("blind", "aware"),   # (iii) 진단: sibling-ban/쿨다운 OFF
    # ---- PHASE-3: fusion-target 선택축의 '도달 가능한' 동적범위 계측기 ----
    "o6_oracle_pool": ("blind", "oracle"),    # 전 상태(load+supply) 사용 · 즉시 ATP 최대화
    "o7_fuse_histress": ("blind", "hi_stress"),
    "o8_fuse_hihealth": ("blind", "hi_health"),  # 카드 정책의 정반대 방향
}
MAIN_ARMS = ("c1_frozen", "c2_random_rw", "a3_awarefuse", "a5_shamfuse",
             "a4_awarefiss", "exp_aware_ff", "guard_off_a3")
POLICY_AXIS = ("c2_random_rw", "a3_awarefuse", "a5_shamfuse",
               "o6_oracle_pool", "o7_fuse_histress", "o8_fuse_hihealth")
GUARD_OFF = {"guard_off_a3"}


class Unit:
    __slots__ = ("sites", "cap", "les", "sib", "cool_until")

    def __init__(self, sites, cap, les, sib=-1, cool_until=-1):
        self.sites = list(sites)
        self.cap = float(cap)
        self.les = les              # float[G] in [0,1] — 유전자별 병변 정도(연속)
        self.sib = sib              # fission 형제 그룹 id (-1 = 없음)
        self.cool_until = cool_until

    def health(self):
        return 1.0 - float(self.les.mean())

    def supply(self):
        return self.cap * self.health()


def init_state(rng, rho):
    d = np.exp(rng.normal(0.0, 0.6, size=S))
    d *= D_TOTAL / d.sum()
    perm = rng.permutation(S)
    groups = np.array_split(perm, N0)
    C_total = D_TOTAL / rho
    units = []
    for g in groups:
        load = d[g].sum()
        cap = C_total * load / D_TOTAL
        units.append(Unit(g, cap, np.zeros(G, dtype=float)))
    return d, units


def drift(d, rng):
    ld = np.log(d)
    ld += rng.normal(0.0, 0.05, size=S)
    jump = rng.random(S) < 0.02
    ld[jump] += rng.normal(0.0, 0.8, size=int(jump.sum()))
    d = np.exp(ld)
    d *= D_TOTAL / d.sum()
    return d


def loads(units, d):
    return np.array([d[u.sites].sum() for u in units])


def supplies(units):
    return np.array([u.supply() for u in units])


def total_supply(units):
    return float(sum(u.supply() for u in units))


# ---------------- FISSION = 부하분산 + 손상 격리 (카드) ----------------
def do_fission(units, d, rng, aware, conv, t, sib_counter):
    cand = [i for i, u in enumerate(units) if len(u.sites) >= 2]
    if not cand:
        return 0.0
    if aware:
        L = loads(units, d)
        Sup = np.maximum(supplies(units), 1e-9)
        i = max(cand, key=lambda j: L[j] / Sup[j])          # 최고 stress
    else:
        i = int(cand[rng.integers(len(cand))])
    u = units.pop(i)
    sup_before = u.supply()
    sites = np.array(u.sites)

    if aware:                                                # load-balanced 분할 (LPT)
        order = sites[np.argsort(-d[sites])]
        a, b, sa, sb = [], [], 0.0, 0.0
        for s in order:
            if sa <= sb:
                a.append(s); sa += d[s]
            else:
                b.append(s); sb += d[s]
        if not a or not b:
            a, b = list(sites[:1]), list(sites[1:])
    else:
        p = rng.permutation(sites)
        h = max(1, len(p) // 2)
        a, b = list(p[:h]), list(p[h:])
        if not b:
            a, b = list(p[:-1]), list(p[-1:])

    C = u.cap
    if conv["capsplit"] == "sym":
        ca = C / 2.0
    else:                                                    # load 비례 (부하분산)
        la_, lb_ = float(d[a].sum()), float(d[b].sum())
        f = la_ / max(la_ + lb_, 1e-12)
        f = min(max(f, MIN_CAP_FRAC), 1.0 - MIN_CAP_FRAC)
        ca = C * f
    cb = C - ca

    l = u.les
    sig = conv["sigma"]
    if sig <= 0.0:                                           # 비-카드: 동일 복사
        la, lb = l.copy(), l.copy()
    else:
        M = C * l                                            # 유전자별 총 손상질량(cap-weighted)
        ch = rng.random(G) < 0.5                             # 어느 자손이 손상을 떠안는가
        la_f = np.where(ch,
                        np.minimum(1.0, M / ca),
                        (M - cb * np.minimum(1.0, M / cb)) / ca)
        la_f = np.clip(la_f, 0.0, 1.0)
        lb_f = np.clip((M - ca * la_f) / cb, 0.0, 1.0)
        la = (1.0 - sig) * l + sig * la_f                    # 부분 격리 = 볼록결합 (질량 보존)
        lb = (1.0 - sig) * l + sig * lb_f

    sib_counter[0] += 1
    sid = sib_counter[0]
    cool = t + COOL_FISS
    ua = Unit(a, ca, la, sib=sid, cool_until=cool)
    ub = Unit(b, cb, lb, sib=sid, cool_until=cool)
    units.append(ua)
    units.append(ub)
    return (ua.supply() + ub.supply()) - sup_before          # 대수가 만들어낸 공짜 supply


# ---------------- FUSION = 손상 희석 (카드) ----------------
def do_fusion(units, d, rng, policy, conv, t, guards, diag):
    n = len(units)
    if n < 2:
        return 0.0
    if guards:
        elig = [i for i in range(n) if t >= units[i].cool_until]
    else:
        elig = list(range(n))
    if len(elig) < 2:
        if diag is not None:
            diag["miss"] += 1
        return 0.0

    def compat(i, j):
        if not guards:
            return True
        si, sj = units[i].sib, units[j].sib
        return not (si != -1 and si == sj)                   # 영구 sibling-ban

    h = np.array([units[i].health() for i in elig])
    if policy == "oracle":
        # 도달가능 헤드룸 계측기: 전 상태(load+supply)를 보고 즉시 전달 ATP를 최대화하는 쌍
        Le = np.array([float(d[units[i].sites].sum()) for i in elig])
        Se = np.array([units[i].supply() for i in elig])
        base = np.minimum(Le, Se)
        gain = (np.minimum(Le[:, None] + Le[None, :], Se[:, None] + Se[None, :])
                - base[:, None] - base[None, :])
        best, bi, bj = -1e18, None, None
        for x in range(len(elig)):
            for y in range(x + 1, len(elig)):
                if compat(elig[x], elig[y]) and gain[x, y] > best:
                    best, bi, bj = gain[x, y], elig[x], elig[y]
        if bi is None:
            if diag is not None:
                diag["miss"] += 1
            return 0.0
        i, j = bi, bj
        order = None
    else:
        if policy == "aware":
            order = [elig[k] for k in np.argsort(h, kind="stable")]     # 최저 health 우선 (카드)
        elif policy == "hi_health":
            order = [elig[k] for k in np.argsort(-h, kind="stable")]
        elif policy == "hi_stress":
            st = np.array([float(d[units[i].sites].sum())
                           / max(units[i].supply(), 1e-9) for i in elig])
            order = [elig[k] for k in np.argsort(-st, kind="stable")]
        elif policy == "sham":
            # 동일 선택 기계(argsort of health) · health 벡터만 SHUFFLE = 정보 채널만 파괴
            order = [elig[k] for k in np.argsort(rng.permutation(h), kind="stable")]
        else:                                                           # blind
            order = [elig[k] for k in rng.permutation(len(elig))]

        i = order[0]
        j = None
        for cand in order[1:]:
            if compat(i, cand):
                j = cand
                break
        if j is None:
            if diag is not None:
                diag["miss"] += 1
            return 0.0

    if diag is not None:
        diag["n_fuse"] += 1
        si, sj = units[i].sib, units[j].sib
        diag["self_remerge"] += 1.0 if (si != -1 and si == sj) else 0.0
        diag["h_std"].append(float(h.std()))                           # 정보채널 (b): DV 분산
        hi, hj = units[i].health(), units[j].health()
        diag["sel_gap"].append(0.5 * (hi + hj) - float(h.mean()))      # 선택 gap (음수 = aware)

    lo, hi_ = (i, j) if i < j else (j, i)
    b = units.pop(hi_)
    a = units.pop(lo)
    sup_before = a.supply() + b.supply()
    ca, cb = a.cap, b.cap
    if conv["fuse"] == "avg":                                          # 카드: 희석
        w = ca / (ca + cb)
        merged = w * a.les + (1.0 - w) * b.les
    else:                                                              # 비-카드 진단: 초선형 소거
        merged = np.minimum(a.les, b.les)
    nu = Unit(a.sites + b.sites, ca + cb, merged, sib=-1, cool_until=-1)
    units.append(nu)
    return nu.supply() - sup_before


# ---------------- 한 run ----------------
def simulate(seed, rho, arm, conv, repair=REPAIR):
    fis_pol, fus_pol = ARMS[arm]
    dynamic = fis_pol is not None
    guards = arm not in GUARD_OFF

    rng_d = np.random.default_rng(10_000 + seed)      # 수요 스트림: arm 무관 동일 (paired-CRN)
    rng_a = np.random.default_rng(90_000 + seed)
    d, units = init_state(rng_d, rho)
    sib_counter = [0]

    diag = {"n_fuse": 0, "self_remerge": 0.0, "h_std": [], "sel_gap": [], "miss": 0}
    atp, hh, ov, churn = [], [], [], []
    ops_supply_created = 0.0
    lab_prev = None

    for t in range(T):
        d = drift(d, rng_d)
        if dynamic:
            for _ in range(K_EV):
                ops_supply_created += do_fission(
                    units, d, rng_a, fis_pol == "aware", conv, t, sib_counter)
                ops_supply_created += do_fusion(
                    units, d, rng_a, fus_pol, conv, t, guards,
                    diag if t >= WARM else None)

        L = loads(units, d)
        Sup = supplies(units)
        out = np.minimum(L, Sup)
        stress = L / np.maximum(Sup, 1e-9)
        caps = np.array([u.cap for u in units])
        hw = float((caps * np.array([u.health() for u in units])).sum() / max(caps.sum(), 1e-9))

        atp.append(float(out.sum()))                        # 헤드라인 (절대 ATP · D_TOTAL 고정)
        hh.append(hw)
        ov.append(float((stress > 1.0).mean()))

        lab = np.empty(S, dtype=np.int32)
        for k, u in enumerate(units):
            lab[u.sites] = k
        if lab_prev is not None:
            same_p = lab_prev[:, None] == lab_prev[None, :]
            same_n = lab[:, None] == lab[None, :]
            iu = np.triu_indices(S, 1)
            churn.append(float((same_p[iu] != same_n[iu]).mean()))
        else:
            churn.append(0.0)
        lab_prev = lab

        for u, st in zip(units, stress):
            lam = B0 + B1 * min(max(0.0, st - 1.0), EXC_CAP)
            nlz = rng_a.poisson(lam)
            if nlz:
                u.les[rng_a.integers(0, G, size=int(nlz))] = 1.0
            brk = np.flatnonzero(u.les > 0.0)
            if brk.size:
                fixed = brk[rng_a.random(brk.size) < repair]
                u.les[fixed] = 0.0                          # 기대 제거량 = REPAIR * sum(les) (분산 중립)

    w = slice(WARM, T)
    mm = lambda v: float(np.mean(v)) if len(v) else 0.0
    return dict(
        atp=float(np.mean(atp[w])),
        health=float(np.mean(hh[w])),
        overload=float(np.mean(ov[w])),
        churn=float(np.mean(churn[w])),
        self_remerge_frac=(diag["self_remerge"] / diag["n_fuse"]) if diag["n_fuse"] else 0.0,
        h_std=mm(diag["h_std"]),
        sel_gap=mm(diag["sel_gap"]),
        fuse_miss=diag["miss"],
        ops_supply_created=float(ops_supply_created),
        n_units=len(units),
        cap_total=float(sum(u.cap for u in units)),
    )


# ---------------- 통계 (paired-t · scipy 없이) ----------------
def t_sf(tv, df):
    tv = abs(float(tv))
    if tv > 60:
        return 0.0
    x = np.linspace(tv, tv + 400.0, 200001)
    lg = (math.lgamma((df + 1) / 2) - 0.5 * math.log(df * math.pi) - math.lgamma(df / 2))
    pdf = np.exp(lg - ((df + 1) / 2) * np.log1p(x * x / df))
    return float(np.trapezoid(pdf, x)) if hasattr(np, "trapezoid") else float(np.trapz(pdf, x))


def paired(e, c):
    dv = np.asarray(e) - np.asarray(c)
    n = dv.size
    m = float(dv.mean())
    sd = float(dv.std(ddof=1))
    sem = sd / math.sqrt(n)
    tv = m / sem if sem > 0 else 0.0
    p = 2.0 * t_sf(tv, n - 1)
    return {"mean": m, "sd": sd, "sem": sem, "t": float(tv), "p": p, "n": n,
            "pos_seeds": int((dv > 0).sum()),
            "per_seed": [round(float(x), 4) for x in dv]}


def run_grid(seeds, rho, conv, arms=MAIN_ARMS, repair=REPAIR):
    out = {}
    for arm in arms:
        per = [simulate(s, rho, arm, conv, repair=repair) for s in seeds]
        agg = {}
        for m in ("atp", "health", "overload", "churn", "self_remerge_frac",
                  "h_std", "sel_gap", "ops_supply_created"):
            v = np.array([p[m] for p in per])
            agg[m] = {"mean": float(v.mean()), "sd": float(v.std(ddof=1)) if len(v) > 1 else 0.0}
        agg["atp_per_seed"] = [float(p["atp"]) for p in per]
        agg["fuse_miss"] = int(sum(p["fuse_miss"] for p in per))
        agg["n_units"] = sorted(set(p["n_units"] for p in per))
        agg["cap_dev"] = max(abs(p["cap_total"] - D_TOTAL / rho) for p in per)
        out[arm] = agg
    return out


def main():
    t0 = time.time()
    res = {"config": dict(S=S, N0=N0, G=G, T=T, WARM=WARM, K_EV=K_EV, B0=B0, B1=B1,
                          REPAIR=REPAIR, seeds=SEEDS, pilot_seeds=PILOT_SEEDS,
                          rho_primary=RHO_PRIMARY, rho_sweep=RHO_SWEEP,
                          margin_atp=MARGIN, alpha=ALPHA, cool_fiss=COOL_FISS,
                          primary_arm="a3_awarefuse",
                          conventions_registered=[c[0] for c in CONV_REGISTERED],
                          conventions_diagnostic=[c[0] for c in CONV_DIAG])}
    conv1 = dict(CONV_REGISTERED[0][1])

    # ================= PHASE 0 · 사전 검정력 (pilot seed · 분석 seed와 disjoint) =================
    # census 규칙 3: '도달 가능한' 축의 동적범위 > 유의 문턱임을 실험 전에 보여라.
    #   ※ 물리적 천장(=100 ATP)은 처치가 도달할 수 있는 값이 아니다(F1의 함정).
    #     처치가 실제로 움직이는 축 = fusion-target 선택 정책 축.
    #     그 축의 도달가능 폭 = {blind, 카드정책, sham, 반대방향, hi-stress, ORACLE(전 상태 사용)}
    #     의 ATP span. 이것이 MDE보다 크지 않으면 이 프로브는 정보축에서 검출력 0이다.
    pil_arms = ("c1_frozen",) + POLICY_AXIS
    pil = run_grid(PILOT_SEEDS, RHO_PRIMARY, conv1, arms=pil_arms)
    e = np.array(pil["a3_awarefuse"]["atp_per_seed"])
    c2p = np.array(pil["c2_random_rw"]["atp_per_seed"])
    sd_pilot = float((e - c2p).std(ddof=1))
    n = len(SEEDS)
    t_a, t_b = 2.093, 0.861                    # t(.975,19), t(.80,19)
    mde = (t_a + t_b) * sd_pilot / math.sqrt(n)
    pol_means = {a: pil[a]["atp"]["mean"] for a in POLICY_AXIS}
    span_pilot = max(pol_means.values()) - min(pol_means.values())
    powered_info = span_pilot > 3.0 * mde
    res["mde"] = {
        "sd_pilot_a3_minus_c2": sd_pilot, "n_analysis": n,
        "MDE_atp_80pct_power": mde,
        "policy_axis_arms": list(POLICY_AXIS),
        "policy_axis_atp_pilot": pol_means,
        "policy_axis_reachable_span_pilot": span_pilot,
        "physical_ceiling_atp": D_TOTAL * min(1.0, 1.0 / RHO_PRIMARY),
        "frozen_floor_atp_pilot": pil["c1_frozen"]["atp"]["mean"],
        "POWERED_info_axis": bool(powered_info),
        "gate": "span(policy axis) > 3 x MDE",
    }
    print("[MDE] sd_pilot=%.3f  MDE=%.3f ATP  policy-axis span(pilot)=%.3f  POWERED=%s"
          % (sd_pilot, mde, span_pilot, powered_info))
    print("      pilot policy axis:", {k: round(v, 2) for k, v in pol_means.items()})

    # ================= PHASE 1 · 본 실험 (n=20 · 규약 6개 · rho primary) =================
    res["grids"] = {}
    for cname, conv in CONV_REGISTERED + CONV_DIAG:
        res["grids"][cname] = run_grid(SEEDS, RHO_PRIMARY, dict(conv))
        print("[grid] %-20s (%.1fs)" % (cname, time.time() - t0))

    res["rho_sweep"] = {}
    for rho in RHO_SWEEP:
        if abs(rho - RHO_PRIMARY) < 1e-9:
            res["rho_sweep"][f"rho={rho:.2f}"] = res["grids"]["R1_avg_sym_seg1.0"]
        else:
            res["rho_sweep"][f"rho={rho:.2f}"] = run_grid(SEEDS, rho, conv1)
        print("[sweep] rho=%.2f (%.1fs)" % (rho, time.time() - t0))

    R1 = res["grids"]["R1_avg_sym_seg1.0"]
    CONTROLS = ["c1_frozen", "c2_random_rw", "a5_shamfuse"]

    def deltas(grid, arm, controls=CONTROLS):
        a = grid[arm]["atp_per_seed"]
        out = {}
        for c in controls:
            if c == arm:
                continue
            out[c] = paired(a, grid[c]["atp_per_seed"])
        out["_pooled_mean"] = float(np.mean([out[c]["mean"] for c in out]))
        return out

    # ================= PHASE 3 · 정책축 도달가능 범위 (분석 seed) =================
    pol = run_grid(SEEDS, RHO_PRIMARY, conv1, arms=POLICY_AXIS)
    R1_pol = dict(R1)
    for a in POLICY_AXIS:
        R1_pol.setdefault(a, pol[a])
    pol_means_main = {a: pol[a]["atp"]["mean"] for a in POLICY_AXIS}
    span_main = max(pol_means_main.values()) - min(pol_means_main.values())
    pol_vs_c2 = {a: paired(pol[a]["atp_per_seed"], pol["c2_random_rw"]["atp_per_seed"])
                 for a in POLICY_AXIS if a != "c2_random_rw"}
    res["policy_axis"] = {"atp": pol_means_main, "reachable_span": span_main,
                          "MDE": mde, "span_over_MDE": span_main / mde,
                          "vs_c2_paired": {k: {kk: v[kk] for kk in ("mean", "sem", "t", "p",
                                                                    "pos_seeds")}
                                           for k, v in pol_vs_c2.items()},
                          "health": {a: pol[a]["health"]["mean"] for a in POLICY_AXIS}}
    print("[phase3] policy-axis span(n=20)=%.3f ATP (= %.1f x MDE)" % (span_main, span_main / mde))

    # ================= PHASE 4 · 레짐 강건성 (repair sweep · 처치-무관 기준) =================
    # 등록 REPAIR=0.01 에서 blind control c2 의 health 가 붕괴(≈0.09)한다.
    # '살아있는 레짐'의 정의는 CONTROL만 보고 내린다(처치 미peek): c2_health > 0.5.
    res["regime_sweep"] = {}
    for rp in (0.01, 0.05, 0.20):
        g = run_grid(SEEDS, RHO_PRIMARY, conv1, repair=rp,
                     arms=("c1_frozen", "c2_random_rw", "a3_awarefuse",
                           "a5_shamfuse", "exp_aware_ff", "a4_awarefiss"))
        dd = deltas(g, "a3_awarefuse")
        de = deltas(g, "exp_aware_ff")
        res["regime_sweep"][f"repair={rp}"] = {
            "atp": {a: g[a]["atp"]["mean"] for a in g},
            "health": {a: g[a]["health"]["mean"] for a in g},
            "c2_alive_health_gt_0.5": bool(g["c2_random_rw"]["health"]["mean"] > 0.5),
            "a3_vs_c1": {k: dd["c1_frozen"][k] for k in ("mean", "sem", "t", "p", "pos_seeds")},
            "a3_vs_c2": {k: dd["c2_random_rw"][k] for k in ("mean", "sem", "t", "p", "pos_seeds")},
            "a3_vs_sham": {k: dd["a5_shamfuse"][k] for k in ("mean", "sem", "t", "p", "pos_seeds")},
            "exp_vs_c1": {k: de["c1_frozen"][k] for k in ("mean", "sem", "t", "p", "pos_seeds")},
            "exp_vs_c2": {k: de["c2_random_rw"][k] for k in ("mean", "sem", "t", "p", "pos_seeds")},
        }
        print("[regime] repair=%.2f  c2_h=%.3f  a3-c2=%+.2f (p=%.3g)  a3-c1=%+.2f  exp-c1=%+.2f"
              % (rp, g["c2_random_rw"]["health"]["mean"], dd["c2_random_rw"]["mean"],
                 dd["c2_random_rw"]["p"], dd["c1_frozen"]["mean"], de["c1_frozen"]["mean"]))

    # ================= PHASE 2 · 판정 =================
    primary = deltas(R1, "a3_awarefuse")
    res["primary_a3_R1"] = primary

    robust = {}
    for cname, _ in CONV_REGISTERED:
        g = res["grids"][cname]
        dd = deltas(g, "a3_awarefuse")
        ok = all(dd[c]["mean"] > MARGIN and dd[c]["p"] < ALPHA for c in CONTROLS)
        robust[cname] = {"vs_c1": dd["c1_frozen"]["mean"], "vs_c2": dd["c2_random_rw"]["mean"],
                         "vs_sham": dd["a5_shamfuse"]["mean"],
                         "p_vs_c2": dd["c2_random_rw"]["p"],
                         "p_vs_sham": dd["a5_shamfuse"]["p"],
                         "SIGN_OK": bool(ok)}
    res["convention_robustness_a3"] = robust
    n_ok = sum(1 for k in robust if robust[k]["SIGN_OK"])
    sign_robust = bool(robust["R1_avg_sym_seg1.0"]["SIGN_OK"] and n_ok >= 2)

    robust_exp = {}
    for cname, _ in CONV_REGISTERED:
        dd = deltas(res["grids"][cname], "exp_aware_ff")
        robust_exp[cname] = {"vs_c1": dd["c1_frozen"]["mean"], "vs_c2": dd["c2_random_rw"]["mean"],
                             "vs_sham": dd["a5_shamfuse"]["mean"],
                             "p_vs_c1": dd["c1_frozen"]["p"],
                             "SIGN_OK": bool(all(dd[c]["mean"] > MARGIN and dd[c]["p"] < ALPHA
                                                 for c in CONTROLS))}
    res["convention_robustness_exp"] = robust_exp

    res["convention_diagnostic"] = {}
    for cname, _ in CONV_DIAG:
        g = res["grids"][cname]
        d3 = deltas(g, "a3_awarefuse")
        res["convention_diagnostic"][cname] = {
            "a3_vs_c1": d3["c1_frozen"]["mean"], "a3_vs_c2": d3["c2_random_rw"]["mean"],
            "a3_vs_sham": d3["a5_shamfuse"]["mean"],
            "ops_supply_created_by_arm": {a: g[a]["ops_supply_created"]["mean"] for a in g},
            "health_by_arm": {a: g[a]["health"]["mean"] for a in g}}

    res["secondary"] = {arm: deltas(R1, arm) for arm in ("exp_aware_ff", "a4_awarefiss")}
    res["guard_off_a3_R1"] = deltas(R1, "guard_off_a3")
    res["a3_minus_guardoff_R1"] = paired(R1["a3_awarefuse"]["atp_per_seed"],
                                         R1["guard_off_a3"]["atp_per_seed"])

    # ---- V-gates (헤드라인 detector = ATP · 그 자체에 건다) ----
    ceiling = D_TOTAL * min(1.0, 1.0 / RHO_PRIMARY)
    v1 = (R1["c1_frozen"]["health"]["mean"] < 0.99
          and R1["c1_frozen"]["atp"]["mean"] < 0.999 * D_TOTAL
          and R1["c2_random_rw"]["atp"]["mean"] < 0.98 * ceiling)
    v2_dv_var = R1["a3_awarefuse"]["h_std"]["mean"] > 1e-3
    v2_selective = R1["a3_awarefuse"]["sel_gap"]["mean"] < -1e-3
    v2_sham_blind = abs(R1["a5_shamfuse"]["sel_gap"]["mean"]) < 0.02
    pump = {a: R1[a]["ops_supply_created"]["mean"] for a in MAIN_ARMS}
    v3_neutral = max(abs(v) for v in pump.values()) < 1e-6
    v3_cap = max(R1[a]["cap_dev"] for a in MAIN_ARMS) < 1e-6
    v3_n = all(R1[a]["n_units"] == [N0] for a in MAIN_ARMS)
    v4_self = R1["a3_awarefuse"]["self_remerge_frac"]["mean"] < 1e-9
    ch_a3 = R1["a3_awarefuse"]["churn"]["mean"]
    ch_c2 = R1["c2_random_rw"]["churn"]["mean"]
    v4_churn = (ch_a3 / ch_c2) > 0.5 if ch_c2 > 0 else False
    v5 = len(SEEDS) >= 20

    gates = {"V1_liveness_unsaturated": bool(v1),
             "V2_info_channel_variance": bool(v2_dv_var),
             "V2_info_channel_selective": bool(v2_selective),
             "V2_sham_is_blind": bool(v2_sham_blind),
             "V3_algebra_neutral_no_free_pump": bool(v3_neutral),
             "V3_capacity_conserved": bool(v3_cap),
             "V3_n_units_conserved": bool(v3_n),
             "V4_self_remerge_zero": bool(v4_self),
             "V4_churn_parity_a3_over_c2": float(ch_a3 / ch_c2) if ch_c2 else 0.0,
             "V4_churn_fair": bool(v4_churn),
             "V5_seeds20_pairedCRN": bool(v5),
             "V6_POWERED_info_axis": bool(powered_info)}
    res["V_gates"] = gates
    res["ops_supply_created_by_arm_R1"] = pump

    all_sig = all(primary[c]["mean"] > MARGIN and primary[c]["p"] < 0.01 for c in CONTROLS)
    hard = all(gates[k] for k in ("V1_liveness_unsaturated", "V2_info_channel_variance",
                                  "V2_info_channel_selective", "V2_sham_is_blind",
                                  "V3_algebra_neutral_no_free_pump", "V3_capacity_conserved",
                                  "V3_n_units_conserved", "V4_self_remerge_zero",
                                  "V4_churn_fair", "V5_seeds20_pairedCRN",
                                  "V6_POWERED_info_axis"))
    passed = bool(all_sig and sign_robust and hard)

    res["verdict"] = {
        "primary_arm": "a3_awarefuse (aware-fusion only · blind fission)",
        "primary_convention": "R1_avg_sym_seg1.0 (카드 등록: 융합=희석 · 분열=격리)",
        "delta_vs_c1_frozen": primary["c1_frozen"]["mean"],
        "delta_vs_c2_random_rw": primary["c2_random_rw"]["mean"],
        "delta_vs_a5_sham": primary["a5_shamfuse"]["mean"],
        "sem_vs_c1": primary["c1_frozen"]["sem"],
        "sem_vs_c2": primary["c2_random_rw"]["sem"],
        "sem_vs_sham": primary["a5_shamfuse"]["sem"],
        "p_vs_c1": primary["c1_frozen"]["p"],
        "p_vs_c2": primary["c2_random_rw"]["p"],
        "p_vs_sham": primary["a5_shamfuse"]["p"],
        "pooled_mean_delta": primary["_pooled_mean"],
        "MDE": mde, "POWERED_info_axis": bool(powered_info),
        "policy_axis_span": span_main,
        "sign_robust_conventions": f"{n_ok}/4",
        "SIGN_ROBUST": sign_robust,
        "all_controls_sig": bool(all_sig),
        "V_gates_all": bool(hard),
        "PASS": passed,
    }
    res["wall_s"] = round(time.time() - t0, 2)

    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(res, f, indent=2)

    print("\n" + json.dumps(res["verdict"], indent=2, ensure_ascii=False))
    print("\n-- R1 (카드 등록 규약) arm 표 --")
    for a in list(MAIN_ARMS) + ["o6_oracle_pool", "o7_fuse_histress", "o8_fuse_hihealth"]:
        g = R1_pol[a]
        print("  %-16s atp=%6.2f±%5.2f  h=%.3f  ovl=%.3f  churn=%.4f  selgap=%+.3f  pump=%+.1e"
              % (a, g["atp"]["mean"], g["atp"]["sd"], g["health"]["mean"], g["overload"]["mean"],
                 g["churn"]["mean"], g["sel_gap"]["mean"], g["ops_supply_created"]["mean"]))
    print("\n-- 규약 강건성 (a3 Δ) --")
    for k, v in robust.items():
        print("  %-20s vs_c1=%+6.2f vs_c2=%+6.2f vs_sham=%+6.2f  p_c2=%.2e  SIGN_OK=%s"
              % (k, v["vs_c1"], v["vs_c2"], v["vs_sham"], v["p_vs_c2"], v["SIGN_OK"]))
    print("-- 규약 강건성 (exp Δ) --")
    for k, v in robust_exp.items():
        print("  %-20s vs_c1=%+6.2f vs_c2=%+6.2f vs_sham=%+6.2f  SIGN_OK=%s"
              % (k, v["vs_c1"], v["vs_c2"], v["vs_sham"], v["SIGN_OK"]))
    print("\n-- 진단(비-카드 규약: 융합=소거) --")
    for k, v in res["convention_diagnostic"].items():
        print("  %-20s a3_vs_c1=%+7.2f a3_vs_c2=%+6.2f  pump(c2)=%+8.1f pump(a3)=%+8.1f"
              % (k, v["a3_vs_c1"], v["a3_vs_c2"],
                 v["ops_supply_created_by_arm"]["c2_random_rw"],
                 v["ops_supply_created_by_arm"]["a3_awarefuse"]))
    print("\nwall_s", res["wall_s"])


if __name__ == "__main__":
    main()
