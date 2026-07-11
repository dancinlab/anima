#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9284 / F12 — 외생 수요 → 절대-setpoint 용량 배분  (F4-SECONDARY ⊕ F10 병합 재발사)
=====================================================================================
$0 CPU-local numpy.  torch 없음.  결정적.  emit lane 무접촉(p5: emit/silence/speak/tension 배선 0).

────────────────────────────────────────────────────────────────────────────────────
기질 (F4의 rent↔shortfall 트레이드오프 ⊕ F10의 per-expert 수요 스트림)
────────────────────────────────────────────────────────────────────────────────────
E=16 organelle(=expert). 각 step 마다 B=32 토큰이 drifting mode-mixture 에서 뽑혀
prototype top-1 로 라우팅 → **외생 수요** dem[t,e] (용량과 무관하게 생성 = H_012 처방:
폐루프 아님, 컨트롤러 밖에서 오는 신호).

  served_t = Σ_e min(dem[t,e], c[e])          (용량 있는 만큼만 서비스)
  rent_t   = LAMBDA * Σ_e c[e]                (용량은 유지비를 문다)
  fitness  = mean_t (served_t − rent_t)       ← 헤드라인 detector (비율 아님 · Goodhart 방어)

총용량이 고정이 아니라 **rent 로 값이 매겨진다** → "수요에 용량을 맞추는 것"만이 이기는 길.

────────────────────────────────────────────────────────────────────────────────────
ARM (카드 §3 5-arm · 전부 동일 stream(paired-CRN) · 동일 컨트롤러 형태 · 동일 스칼라 1개)
────────────────────────────────────────────────────────────────────────────────────
  EXP    절대 setpoint: target_e = g * EMA(dem_e), g = 1.0 (= "c_e == dem_e" · 유도값, 튜닝 아님)
  c1     shuffled-load : 매 epoch **새 치환**된 load 로 동일 갱신 (이동질량 EXP 와 매칭)
  c2     BEST open-loop 상수: 균일 c_e = g*(B/E), g 를 **grid 전수**해 최선값 (레벨 FORM 분리)
         + c2h = seed 별 hindsight 최선 상수 (더 강한 null · 순서통계량이 control 에 유리 = 보수적)
  c3     fixed-perm misalign: **전 구간 고정 치환** → 차등화(gini) 는 EXP 와 동일, 정렬만 파괴
  abl    z-tonic: setpoint 없는 자기추적 컨트롤러 c ← c*exp(η·z), z=(r−EMA r)/σ  (F4 PRIMARY 사망 재현)
  ORACLE lookahead shape (control 아님 · achievable-headroom 천장)

레벨 스칼라 g 는 c2·ORACLE·EXPpil 전부 **동일 grid · 동일 선택규칙 · 동일 PILOT seed(100-104,
분석 seed 와 disjoint)** 로 고른다 → 레벨 축에서 arm 간 비대칭 0. 헤드라인 EXP 는 유도값 g=1.0 고정.

────────────────────────────────────────────────────────────────────────────────────
계측 규칙 (SYNTHESIS §8 census 강제 · 11 패밀리 중 7개의 verdict 를 뒤집은 결함)
────────────────────────────────────────────────────────────────────────────────────
 1. 🚫 Δ = exp − max(controls) **금지** → control 별 paired-t 전부 + pooled-mean 요약.
 2. 🚫 "mean vs 1·std" 기각 휴리스틱 **금지** → SEM / paired-t 만.
 3. ✅ 사전 MDE (PILOT seed 로 계산, 분석 seed 미열람) < 축 동적범위 → 실행 전 게이트.
 4. ✅ 정보 채널 증명: (a) EXP 결정변수가 control 이 못 보는 입력(dem)의 함수임을 코드로
    (b) 운영 대역에서 그 결정변수의 분산 > 0 실측.
 5. ✅ V-gate 를 **헤드라인 detector(fitness) 그 자체**에 건다. V1(축 liveness)은 ORACLE·c2
    만으로 계산 → EXP 효과크기의 함수가 아님 ⇒ 출력이 {PASS,INVALID} 로 붕괴하지 않음.
 🚫 금지 지표 미사용: conj_index · purity(aggregate) · acc/ATP 류 비율 · corr(n,demand).
    gini 는 FORM 진단용으로만 출력하고 판정에 **쓰지 않는다**.

바 = **achievable-headroom 회수율** = (fit_EXP − fit_c2) / (fit_ORACLE − fit_c2)   (절대 %p 금지)

────────────────────────────────────────────────────────────────────────────────────
사전등록 판정 (실행 전 고정 · tune-to-green 금지 · 음성도 정당한 결과)
────────────────────────────────────────────────────────────────────────────────────
 PASS(DIRECTIONAL-POSITIVE, toy 상한):
   primary cell(h=400) 에서
   (a) EXP 가 c1·c2·c3 **각각** paired-t p<0.05 로 유의 우세 (max(controls) 사용 안 함), AND
   (b) headroom 회수율 ≥ 0.20, AND
   (c) abl(z-tonic) 은 c2 대비 유의 열세 (신호≠컨트롤러 재현), AND
   (d) null-env(균일 수요) 에서 pooled Δ 가 유의하지 않음 (측정 게임 아님).
 FAIL/계열종결: c2(최선 상수)를 못 이김 ⇒ 이득은 레벨(FORM)이지 동적 배분(BIND) 아님.
 INVALID: V1(축 liveness: ORACLE > c2) 실패 · MDE ≥ 동적범위 · null-env 에서 EXP 유의 우세.
 toy 이므로 최대 등급 = DIRECTIONAL (a_toy_scale_recheck · engine-native 아님).
"""
import json
import math
import os
import time

import numpy as np

# ───────────────────────────────── 고정 하이퍼 (실행 전 확정 · 이후 무수정)
E = 16              # organelle(expert) 수
K = 16              # 잠재 mode 수
D = 32              # 토큰 차원
B = 32              # step 당 토큰 = 총 수요 평균
N_STEPS = 1500
TOK_SIGMA = 0.8     # 라우팅 노이즈
LAMBDA = 0.5        # 용량 1단위 유지비 (rent)
EPOCH = 25          # 재할당 주기
ETA = 0.35          # 재할당 step size
EMA_HL = 50         # load EMA half-life (steps)
ETA_Z = 0.35        # abl: z-tonic 로그-스텝 (EXP 와 동일 크기)
Z_HL = 50           # abl: 자기추적 EMA half-life
WARMUP_FRAC = 0.2
FLOOR = 0.02        # 용량 하한 (사멸 방지 · 전 arm 동일)
CAP = 8.0           # 용량 상한 (= 4x 평균 per-expert 수요 · 전 arm 동일)
THETA = 1.0         # 절대 setpoint: c_e == dem_e  (유도값 · 스윕으로 튜닝하지 않음)

SEEDS = list(range(20))            # 분석 seed (n=20)
PILOT_SEEDS = [100, 101, 102, 103, 104]   # 레벨 스칼라 선택 + MDE 사전계산 전용 (disjoint)
PRIMARY_H = 400
SWEEP_H = [25, 100, 400, 1600, "static"]
G_GRID = [round(x, 3) for x in np.linspace(0.2, 1.6, 15)]   # 레벨 스칼라 grid (c2·ORACLE·EXPpil 공용)
THETA_GRID = [0.6, 0.8, 1.0, 1.2, 1.5, 2.0]                 # 민감도 (판정에 미사용)

MEAN_PE = float(B) / E             # per-expert 평균 수요 = 2.0
EMA_A = 1.0 - 0.5 ** (1.0 / EMA_HL)
Z_A = 1.0 - 0.5 ** (1.0 / Z_HL)
WARM = int(WARMUP_FRAC * N_STEPS)
HERE = os.path.dirname(os.path.abspath(__file__))


# ───────────────────────────────── 통계 (scipy 없이 paired-t)
def _betacf(a, b, x):
    tiny = 1e-30
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 3e-12:
            break
    return h


def _betainc(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - math.exp(lbeta + b * math.log(1.0 - x) + a * math.log(x)) * _betacf(b, a, 1.0 - x) / b


def t_sf(t, df):
    """P(T > t) for Student-t."""
    x = df / (df + t * t)
    p = 0.5 * _betainc(df / 2.0, 0.5, x)
    return p if t > 0 else 1.0 - p


def paired_t(delta):
    """paired-CRN delta 배열 → mean / sd / SEM / t / two-sided p / 양수 seed 수."""
    v = np.asarray(delta, float)
    n = len(v)
    m = float(v.mean())
    sd = float(v.std(ddof=1)) if n > 1 else 0.0
    sem = sd / math.sqrt(n) if n > 1 else 0.0
    t = m / sem if sem > 1e-15 else (0.0 if abs(m) < 1e-15 else math.copysign(999.0, m))
    p = 2.0 * t_sf(abs(t), n - 1) if n > 1 else 1.0
    return {"mean": m, "sd": sd, "sem": sem, "t": float(t), "p": float(min(1.0, p)),
            "n": n, "n_pos": int((v > 0).sum()), "per_seed": [round(float(x), 5) for x in v]}


# ───────────────────────────────── 외생 수요 스트림 (arm 무관 · 전 arm 공유 = paired-CRN)
_STREAM_CACHE = {}


def make_demand(seed, half_life, null_env=False):
    """dem[T,E] — 용량과 완전히 독립(외생). 컨트롤러는 이걸 관측만 할 뿐 바꾸지 못한다."""
    key = (seed, str(half_life), null_env)
    if key in _STREAM_CACHE:
        return _STREAM_CACHE[key]
    rng = np.random.default_rng(1000 + seed)
    mu = rng.normal(size=(K, D))
    mu /= np.linalg.norm(mu, axis=1, keepdims=True)
    W = mu.copy()                                  # expert prototype = mode center (1:1)

    if null_env:
        pis = np.full((N_STEPS, K), 1.0 / K)       # NULL-ENV: 특화할 것이 없는 균일 수요
    else:
        rho = 1.0 if half_life == "static" else 0.5 ** (1.0 / float(half_life))
        z = rng.normal(size=K)
        pis = np.empty((N_STEPS, K))
        for t in range(N_STEPS):
            if half_life != "static":
                z = rho * z + math.sqrt(max(1e-9, 1 - rho ** 2)) * rng.normal(size=K)
            lg = 1.6 * z
            lg -= lg.max()
            p = np.exp(lg)
            pis[t] = p / p.sum()

    cdf = np.cumsum(pis, axis=1)
    u = rng.random((N_STEPS, B))
    m = np.array([np.searchsorted(cdf[t], u[t]) for t in range(N_STEPS)])
    m = np.clip(m, 0, K - 1)
    x = mu[m] + TOK_SIGMA * rng.normal(size=(N_STEPS, B, D))
    s = x @ W.T                                    # [T,B,E]
    top1 = np.argmax(s, axis=2)
    dem = np.zeros((N_STEPS, E))
    for t in range(N_STEPS):
        dem[t] = np.bincount(top1[t], minlength=E)
    _STREAM_CACHE[key] = dem
    return dem


# ───────────────────────────────── 공용 헬퍼
def gini(v):
    v = np.sort(np.maximum(v, 0.0))
    n = len(v)
    s = v.sum()
    if s <= 0:
        return 0.0
    idx = np.arange(1, n + 1)
    return float((2.0 * (idx * v).sum()) / (n * s) - (n + 1.0) / n)


def _score(dem, c_traj):
    """헤드라인 detector: fitness = mean_t(served − LAMBDA*rent).  c_traj[T,E]."""
    served = np.minimum(dem[WARM:], c_traj[WARM:]).sum(axis=1)
    rent = LAMBDA * c_traj[WARM:].sum(axis=1)
    fit = float(np.mean(served - rent))
    return {"fitness": fit,
            "served": float(np.mean(served)),
            "rent": float(np.mean(rent)),
            "cap_total": float(np.mean(c_traj[WARM:].sum(axis=1))),
            "gini_FORM_diag": float(np.mean([gini(c_traj[t]) for t in range(WARM, N_STEPS, 10)]))}


# ───────────────────────────────── 정적/천장 arm (재귀 없음 → 벡터화)
def arm_const(dem, g):
    """c2: BEST open-loop 상수 (균일). 스트림을 전혀 읽지 않는다 (정보채널 0)."""
    c = np.clip(np.full(E, g * MEAN_PE), FLOOR, CAP)
    return np.tile(c, (N_STEPS, 1))


def arm_oracle(dem, g):
    """ORACLE(천장 · control 아님): 다음 epoch 의 **진짜** 수요 shape 를 미리 봄."""
    c_traj = np.empty((N_STEPS, E))
    c = np.clip(np.full(E, g * MEAN_PE), FLOOR, CAP)
    for t in range(N_STEPS):
        if t % EPOCH == 0:
            fut = dem[t:t + EPOCH].mean(axis=0)
            c = np.clip(g * fut, FLOOR, CAP)
        c_traj[t] = c
    return c_traj


# ───────────────────────────────── 동적 arm (EXP · c1 · c3 · abl)
def arm_dynamic(arm, dem, seed, g=1.0, exp_masses=None, log_dv=False):
    rng = np.random.default_rng(90000 + 7 * seed + {"EXP": 0, "c1": 1, "c3": 3, "abl": 4, "abl_mm": 4}[arm])
    fixed_perm = rng.permutation(E)                # c3: 전 구간 고정 치환
    c = np.full(E, MEAN_PE)
    ema = np.full(E, MEAN_PE)                      # 관측된 외생 수요의 EMA (= 결정변수의 유일한 소스)
    zmu = np.full(E, 1.0)
    zvar = np.full(E, 0.25)
    c_traj = np.empty((N_STEPS, E))
    masses = []
    dv_log = []                                    # 정보채널 (b): 결정변수 기록

    for t in range(N_STEPS):
        if t > 0 and t % EPOCH == 0:
            ep = t // EPOCH - 1
            if arm in ("abl", "abl_mm"):
                # setpoint 없는 자기추적: z = (r − EMA r)/σ  (평균 0 → 절대 레벨 정보 0)
                r = ema / np.maximum(c, 1e-6)
                z = (r - zmu) / (np.sqrt(zvar) + 1e-6)
                full = c * np.exp(ETA_Z * np.clip(z, -3.0, 3.0)) - c
                if arm == "abl_mm":     # 예산공정 변형: 이동질량을 EXP 에 매칭 (c1/c3 와 동일 규칙)
                    mm = 0.5 * float(np.abs(full).sum())
                    budget = exp_masses[ep] if (exp_masses is not None and ep < len(exp_masses)) else 0.0
                    full = full * (1.0 if mm <= 1e-12 else min(1.0, budget / mm))
                c_new = c + full
                masses.append(0.5 * float(np.abs(np.clip(c_new, FLOOR, CAP) - c).sum()))
            else:
                if arm == "EXP":
                    tgt = g * ema                                   # 절대 setpoint (c_e == dem_e / θ)
                elif arm == "c1":
                    tgt = g * ema[rng.permutation(E)]               # 매 epoch 새 치환
                else:  # c3
                    tgt = g * ema[fixed_perm]                       # 고정 치환 (dispersion 동일)
                full = ETA * (tgt - c)
                mm = 0.5 * float(np.abs(full).sum())
                if arm == "EXP":
                    masses.append(mm)
                    c_new = c + full
                else:                                               # 이동질량을 EXP 예산에 매칭
                    budget = exp_masses[ep] if (exp_masses is not None and ep < len(exp_masses)) else 0.0
                    step = 1.0 if mm <= 1e-12 else min(1.0, budget / mm)
                    c_new = c + step * full
                    masses.append(0.5 * float(np.abs(c_new - c).sum()))
                if log_dv and arm == "EXP":
                    dv_log.append(tgt.copy())
            c = np.clip(c_new, FLOOR, CAP)
        c_traj[t] = c

        d = dem[t]                                 # 외생 수요 (용량에 영향받지 않음)
        # ── 관측 갱신은 서비스 **이후** (인과적 · lookahead 누수 0)
        ema = ema + EMA_A * (d - ema)
        if arm in ("abl", "abl_mm"):
            r = ema / np.maximum(c, 1e-6)
            zmu = zmu + Z_A * (r - zmu)
            zvar = zvar + Z_A * ((r - zmu) ** 2 - zvar)

    out = _score(dem, c_traj)
    out["moved_mass_total"] = float(np.sum(masses))
    if log_dv and arm == "EXP":
        out["_dv"] = np.array(dv_log)
    if arm == "EXP":
        out["_masses"] = masses
    return out


# ───────────────────────────────── 한 seed = 모든 arm (paired-CRN)
def run_seed(seed, half_life, g_c2, g_oracle, g_exppil, null_env=False, log_dv=False):
    dem = make_demand(seed, half_life, null_env=null_env)
    res = {}
    exp = arm_dynamic("EXP", dem, seed, g=1.0 / THETA, log_dv=log_dv)   # 헤드라인: 유도 setpoint θ=1.0
    masses = exp.pop("_masses")
    res["EXP"] = exp
    res["c1"] = arm_dynamic("c1", dem, seed, g=1.0 / THETA, exp_masses=masses)
    res["c3"] = arm_dynamic("c3", dem, seed, g=1.0 / THETA, exp_masses=masses)
    res["abl"] = arm_dynamic("abl", dem, seed)                                  # 사전등록 (무제약)
    res["abl_mm"] = arm_dynamic("abl_mm", dem, seed, exp_masses=masses)         # 예산공정 변형
    res["EXPpil"] = arm_dynamic("EXP", dem, seed, g=g_exppil)   # 레벨 스칼라를 PILOT 에서 고른 대칭 arm
    res["EXPpil"].pop("_masses", None)
    res["c2"] = _score(dem, arm_const(dem, g_c2))
    res["ORACLE"] = _score(dem, arm_oracle(dem, g_oracle))
    # c2h: seed 별 hindsight 최선 상수 (순서통계량이 control 에 유리 = EXP 에 보수적인 더 강한 null)
    best = None
    for g in G_GRID:
        s = _score(dem, arm_const(dem, g))
        if best is None or s["fitness"] > best["fitness"]:
            best = s
            best["_g"] = g
    res["c2h"] = best
    return res


# ───────────────────────────────── PILOT: 레벨 스칼라 선택 + MDE 사전계산 (분석 seed 미열람)
def pilot():
    log = {"grid": G_GRID, "pilot_seeds": PILOT_SEEDS, "h": PRIMARY_H}
    fit_c2 = {g: [] for g in G_GRID}
    fit_or = {g: [] for g in G_GRID}
    fit_ep = {g: [] for g in G_GRID}
    for s in PILOT_SEEDS:
        dem = make_demand(s, PRIMARY_H)
        for g in G_GRID:
            fit_c2[g].append(_score(dem, arm_const(dem, g))["fitness"])
            fit_or[g].append(_score(dem, arm_oracle(dem, g))["fitness"])
            r = arm_dynamic("EXP", dem, s, g=g)
            r.pop("_masses", None)
            fit_ep[g].append(r["fitness"])
    g_c2 = max(G_GRID, key=lambda g: float(np.mean(fit_c2[g])))
    g_or = max(G_GRID, key=lambda g: float(np.mean(fit_or[g])))
    g_ep = max(G_GRID, key=lambda g: float(np.mean(fit_ep[g])))
    log["curve_c2"] = {str(g): round(float(np.mean(fit_c2[g])), 4) for g in G_GRID}
    log["curve_oracle"] = {str(g): round(float(np.mean(fit_or[g])), 4) for g in G_GRID}
    log["curve_exp_class"] = {str(g): round(float(np.mean(fit_ep[g])), 4) for g in G_GRID}
    log["g_c2_selected"] = g_c2
    log["g_oracle_selected"] = g_or
    log["g_exppil_selected"] = g_ep

    # MDE (사전 계산 · 분석 seed 를 보지 않고 PILOT 만으로)
    d_exp_c2, headroom = [], []
    for s in PILOT_SEEDS:
        dem = make_demand(s, PRIMARY_H)
        e = arm_dynamic("EXP", dem, s, g=1.0)
        e.pop("_masses", None)
        f_c2 = _score(dem, arm_const(dem, g_c2))["fitness"]
        f_or = _score(dem, arm_oracle(dem, g_or))["fitness"]
        d_exp_c2.append(e["fitness"] - f_c2)
        headroom.append(f_or - f_c2)
    sd = float(np.std(d_exp_c2, ddof=1))
    n = len(SEEDS)
    sem20 = sd / math.sqrt(n)
    # 양측 α=0.05, power 80%, df=19 :  (t_.975 + t_.80) ≈ 2.093 + 0.861 = 2.954
    mde_fit = 2.954 * sem20
    dyn_range = float(np.mean(headroom))
    log["mde"] = {
        "pilot_sd_paired_delta_EXP_minus_c2": round(sd, 4),
        "sem_at_n20": round(sem20, 4),
        "MDE_80pct_fitness_units": round(mde_fit, 4),
        "axis_dynamic_range_ORACLE_minus_c2": round(dyn_range, 4),
        "MDE_in_headroom_recovery_units": round(mde_fit / dyn_range, 4) if dyn_range > 0 else None,
        "mde_ok": bool(dyn_range > 0 and mde_fit < dyn_range),
    }
    return log


# ───────────────────────────────── 정보 채널 증명
def info_channel_proof(g_c2):
    """(a) EXP 결정변수 = control 이 못 보는 입력(dem)의 함수  (b) 운영대역 분산 > 0."""
    dem_a = make_demand(0, PRIMARY_H)
    dem_b = make_demand(1, PRIMARY_H)
    # 같은 arm-RNG(seed=0) · 다른 외생 스트림 → EXP 결정변수(target)는 달라져야 한다
    ra = arm_dynamic("EXP", dem_a, 0, g=1.0, log_dv=True)
    rb = arm_dynamic("EXP", dem_b, 0, g=1.0, log_dv=True)
    dv_a, dv_b = ra["_dv"], rb["_dv"]
    exp_sensitivity = float(np.abs(dv_a - dv_b).max())
    # control(c2) 의 용량 벡터는 스트림에 **불변** (정보 채널 0)
    ctrl_sensitivity = float(np.abs(arm_const(dem_a, g_c2) - arm_const(dem_b, g_c2)).max())
    # (b) 운영 대역에서 결정변수 분산
    tvar = float(np.mean(dv_a.std(axis=0)))        # expert 별 시간축 std 평균
    xvar = float(np.mean(dv_a.std(axis=1)))        # epoch 별 expert 간 std 평균
    return {
        "a_treatment_DV_is_function_of_exogenous_input": {
            "max|target(stream_A) - target(stream_B)| (same arm RNG)": round(exp_sensitivity, 4),
            "max|c2(stream_A) - c2(stream_B)|": round(ctrl_sensitivity, 6),
            "verdict": "EXP DV = f(dem) · c2 DV = const (스트림 불변) ⇒ 정보 채널 존재",
        },
        "b_DV_variance_in_operating_band": {
            "mean_temporal_std_of_target_per_expert": round(tvar, 4),
            "mean_cross_expert_std_of_target": round(xvar, 4),
            "target_range": [round(float(dv_a.min()), 3), round(float(dv_a.max()), 3)],
            "var_gt_0": bool(tvar > 1e-6 and xvar > 1e-6),
        },
        "demand_is_exogenous": "dem[t,e] 는 arm 실행 전에 생성되며 c 에 의존하지 않음 (폐루프 아님)",
    }


# ───────────────────────────────── 한 cell = 20 seed × 전 arm
ARMS = ["EXP", "EXPpil", "c1", "c2", "c2h", "c3", "abl", "abl_mm", "ORACLE"]
CONTROLS = ["c1", "c2", "c3"]


def run_cell(half_life, g_c2, g_oracle, g_exppil, null_env=False):
    per = {a: {k: [] for k in ("fitness", "served", "rent", "cap_total", "gini_FORM_diag")} for a in ARMS}
    mass = {a: [] for a in ("EXP", "c1", "c3", "abl", "abl_mm")}
    for s in SEEDS:
        r = run_seed(s, half_life, g_c2, g_oracle, g_exppil, null_env=null_env)
        for a in ARMS:
            for k in per[a]:
                per[a][k].append(r[a][k])
        for a in mass:
            mass[a].append(r[a].get("moved_mass_total", 0.0))

    f = {a: np.array(per[a]["fitness"]) for a in ARMS}
    cell = {
        "arms": {a: {k: [round(float(np.mean(per[a][k])), 4), round(float(np.std(per[a][k], ddof=1)), 4)]
                     for k in per[a]} for a in ARMS},
        "moved_mass_mean": {a: round(float(np.mean(mass[a])), 3) for a in mass},
        "paired_t_EXP_minus": {c: paired_t(f["EXP"] - f[c]) for c in ["c1", "c2", "c2h", "c3", "abl", "abl_mm"]},
        "pooled_mean_delta_vs_3controls": paired_t(
            np.mean([f["EXP"] - f[c] for c in CONTROLS], axis=0)),
        "paired_t_abl_minus_c2": paired_t(f["abl"] - f["c2"]),
        "paired_t_abl_mm_minus_c2": paired_t(f["abl_mm"] - f["c2"]),
        "V1_axis_liveness_ORACLE_minus_c2": paired_t(f["ORACLE"] - f["c2"]),
    }
    den = f["ORACLE"] - f["c2"]
    ok = den > 1e-9
    live = bool(np.mean(den) > 1e-9 and cell["V1_axis_liveness_ORACLE_minus_c2"]["p"] < 0.05
                and cell["V1_axis_liveness_ORACLE_minus_c2"]["mean"] > 0)
    rec_exp = ((f["EXP"] - f["c2"]) / np.where(ok, den, 1.0))[ok] if live else np.array([])
    cell["V1_live"] = live
    cell["headroom_recovery"] = {
        "EXP_pooled": round(float(np.mean(f["EXP"] - f["c2"]) / np.mean(den)), 4) if live else None,
        "EXP_per_seed_mean": round(float(rec_exp.mean()), 4) if rec_exp.size > 1 else None,
        "EXP_per_seed_sem": round(float(rec_exp.std(ddof=1) / math.sqrt(rec_exp.size)), 4) if rec_exp.size > 1 else None,
        "c1_pooled": round(float(np.mean(f["c1"] - f["c2"]) / np.mean(den)), 4) if live else None,
        "c3_pooled": round(float(np.mean(f["c3"] - f["c2"]) / np.mean(den)), 4) if live else None,
        "abl_pooled": round(float(np.mean(f["abl"] - f["c2"]) / np.mean(den)), 4) if live else None,
        "abl_mm_pooled": round(float(np.mean(f["abl_mm"] - f["c2"]) / np.mean(den)), 4) if live else None,
        "EXPpil_pooled": round(float(np.mean(f["EXPpil"] - f["c2"]) / np.mean(den)), 4) if live else None,
    }
    return cell


def main():
    t0 = time.time()
    print("=" * 100)
    print("H_9284 / F12 — 외생 수요 → 절대-setpoint 용량 배분  (F4-SEC ⊕ F10 병합)")
    print("=" * 100)

    # ── STEP 0: PILOT (레벨 스칼라 선택 + MDE) — 분석 seed 미열람
    pl = pilot()
    g_c2, g_or, g_ep = pl["g_c2_selected"], pl["g_oracle_selected"], pl["g_exppil_selected"]
    m = pl["mde"]
    print("\n[STEP 0 · PILOT(seed 100-104, 분석 seed 와 disjoint) — 레벨 스칼라 + 사전 MDE]")
    print("  선택된 레벨 스칼라 g:  c2=%.3f  ORACLE=%.3f  EXPpil=%.3f   (동일 grid·동일 규칙)" % (g_c2, g_or, g_ep))
    print("  사전 MDE(80%% power, α=.05, n=20) = %.4f  |  축 동적범위(ORACLE−c2) = %.4f"
          % (m["MDE_80pct_fitness_units"], m["axis_dynamic_range_ORACLE_minus_c2"]))
    print("  MDE(회수율 단위) = %.4f   →  MDE-GATE = %s"
          % (m["MDE_in_headroom_recovery_units"], "PASS ✅" if m["mde_ok"] else "FAIL ❌ (검출력 0 → 재설계)"))
    if not m["mde_ok"]:
        print("\n  ⛔ MDE ≥ 동적범위 ⇒ 프로브 재설계 필요. 중단.")
        json.dump({"pilot": pl, "verdict": "BLOCKED_MDE"}, open(os.path.join(HERE, "result.json"), "w"), indent=2)
        return

    # ── STEP 1: 정보 채널 증명
    ic = info_channel_proof(g_c2)
    print("\n[STEP 1 · 정보 채널 증명]")
    a = ic["a_treatment_DV_is_function_of_exogenous_input"]
    b = ic["b_DV_variance_in_operating_band"]
    print("  (a) 같은 arm-RNG · 다른 외생 스트림:  max|Δtarget_EXP| = %.4f   vs   max|Δc_c2| = %.6f"
          % (a["max|target(stream_A) - target(stream_B)| (same arm RNG)"], a["max|c2(stream_A) - c2(stream_B)|"]))
    print("  (b) 운영대역 결정변수 분산: 시간축 std=%.4f · expert간 std=%.4f · range=%s  → var>0 %s"
          % (b["mean_temporal_std_of_target_per_expert"], b["mean_cross_expert_std_of_target"],
             b["target_range"], "✅" if b["var_gt_0"] else "❌"))

    # ── STEP 2: PRIMARY CELL
    cells = {}
    cells[f"primary_h{PRIMARY_H}"] = run_cell(PRIMARY_H, g_c2, g_or, g_ep)
    # ── STEP 3: 수요 지속성(drift half-life) 축 스윕
    for h in SWEEP_H:
        if h == PRIMARY_H:
            continue
        cells[f"sweep_h{h}"] = run_cell(h, g_c2, g_or, g_ep)
    # ── STEP 4: NULL-ENV
    cells["null_env_uniform_demand"] = run_cell(PRIMARY_H, g_c2, g_or, g_ep, null_env=True)

    # ── STEP 5: θ 민감도 (판정 미사용 · knife-edge 여부만)
    theta_sens = {}
    for th in THETA_GRID:
        d_c2, d_c3 = [], []
        for s in SEEDS:
            dem = make_demand(s, PRIMARY_H)
            e = arm_dynamic("EXP", dem, s, g=1.0 / th)
            masses = e.pop("_masses")
            c3 = arm_dynamic("c3", dem, s, g=1.0 / th, exp_masses=masses)
            f_c2 = _score(dem, arm_const(dem, g_c2))["fitness"]
            d_c2.append(e["fitness"] - f_c2)
            d_c3.append(e["fitness"] - c3["fitness"])
        theta_sens[str(th)] = {"EXP_minus_c2": paired_t(d_c2), "EXP_minus_c3": paired_t(d_c3)}

    out = {
        "hypothesis": "H_9284", "family": "F12 (F4-SEC ⊕ F10 merged)",
        "config": dict(E=E, K=K, D=D, B=B, N_STEPS=N_STEPS, LAMBDA=LAMBDA, EPOCH=EPOCH, ETA=ETA,
                       EMA_HL=EMA_HL, ETA_Z=ETA_Z, THETA=THETA, FLOOR=FLOOR, CAP=CAP,
                       seeds=SEEDS, pilot_seeds=PILOT_SEEDS, g_grid=G_GRID,
                       warmup_frac=WARMUP_FRAC, primary_h=PRIMARY_H),
        "prereg": {
            "bar": "achievable-headroom recovery = (fit_EXP - fit_c2)/(fit_ORACLE - fit_c2)",
            "PASS": "EXP > c1,c2,c3 각각 paired-t p<0.05 AND recovery>=0.20 AND abl<c2 유의 AND null-env ns",
            "FAIL": "c2(best open-loop 상수)를 못 이김 ⇒ FORM(레벨)이지 BIND 아님 ⇒ 계열 종결",
            "INVALID": "V1(ORACLE>c2) 실패 · MDE>=동적범위 · null-env 에서 EXP 유의 우세",
            "banned_metrics": ["conj_index", "purity(aggregate)", "acc/ATP ratio", "corr(n,demand)",
                               "Δ = exp − max(controls)", "mean-vs-1std heuristic"],
            "max_tier": "DIRECTIONAL (toy numpy · engine-native 아님)",
        },
        "pilot_and_MDE": pl,
        "info_channel_proof": ic,
        "cells": cells,
        "theta_sensitivity_h400_not_used_for_verdict": theta_sens,
    }
    out["wall_sec"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "result.json"), "w") as fjs:
        json.dump(out, fjs, indent=2, ensure_ascii=False)

    # ───────── 콘솔 요약
    for name, cl in cells.items():
        print("\n" + "=" * 100)
        print("[CELL] %s" % name)
        print("  %-8s %10s %9s %8s %9s %8s" % ("arm", "fitness", "served", "rent", "cap_tot", "gini*"))
        for a in ARMS:
            v = cl["arms"][a]
            print("  %-8s %8.4f±%.3f %8.3f %8.3f %8.3f %8.3f"
                  % (a, v["fitness"][0], v["fitness"][1], v["served"][0], v["rent"][0],
                     v["cap_total"][0], v["gini_FORM_diag"][0]))
        print("  moved-mass(예산공정성): %s" % cl["moved_mass_mean"])
        print("  ── control 별 paired-t (n=20, CRN · max(controls) 미사용)")
        for c, s in cl["paired_t_EXP_minus"].items():
            print("     Δ(EXP−%-4s) = %+8.4f  SEM %6.4f  t=%+7.2f  p=%.2e  (%2d/20 양)"
                  % (c, s["mean"], s["sem"], s["t"], s["p"], s["n_pos"]))
        pm = cl["pooled_mean_delta_vs_3controls"]
        print("     pooled-mean vs 3 controls = %+8.4f  SEM %6.4f  t=%+7.2f  p=%.2e"
              % (pm["mean"], pm["sem"], pm["t"], pm["p"]))
        ab = cl["paired_t_abl_minus_c2"]
        print("     Δ(abl−c2)    [z-tonic · 사전등록 무제약 = 이동질량 %.0f배 우위] = %+8.4f  t=%+7.2f  p=%.2e"
              % (cl["moved_mass_mean"]["abl"] / max(1e-9, cl["moved_mass_mean"]["EXP"]), ab["mean"], ab["t"], ab["p"]))
        ab2 = cl["paired_t_abl_mm_minus_c2"]
        print("     Δ(abl_mm−c2) [z-tonic · 예산공정(이동질량 매칭)]              = %+8.4f  t=%+7.2f  p=%.2e"
              % (ab2["mean"], ab2["t"], ab2["p"]))
        v1 = cl["V1_axis_liveness_ORACLE_minus_c2"]
        print("     V1 축 liveness (ORACLE−c2) = %+8.4f  t=%+7.2f  p=%.2e  → %s"
              % (v1["mean"], v1["t"], v1["p"], "LIVE ✅" if (v1["mean"] > 0 and v1["p"] < 0.05) else "DEAD ❌ INVALID"))
        hr = cl["headroom_recovery"]
        print("  ── achievable-headroom 회수율:  EXP=%s (per-seed %s±%s) | c1=%s | c3=%s | abl=%s | abl_mm=%s | EXPpil=%s"
              % (hr["EXP_pooled"], hr["EXP_per_seed_mean"], hr["EXP_per_seed_sem"],
                 hr["c1_pooled"], hr["c3_pooled"], hr["abl_pooled"], hr["abl_mm_pooled"], hr["EXPpil_pooled"]))

    print("\n" + "=" * 100)
    print("[θ 민감도 · h=400 · 판정 미사용]")
    for th, s in theta_sens.items():
        print("  θ=%-4s  Δ(EXP−c2) = %+7.4f (t=%+6.2f)   Δ(EXP−c3) = %+7.4f (t=%+6.2f)"
              % (th, s["EXP_minus_c2"]["mean"], s["EXP_minus_c2"]["t"],
                 s["EXP_minus_c3"]["mean"], s["EXP_minus_c3"]["t"]))
    print("\nwall=%.1fs → result.json" % out["wall_sec"])


if __name__ == "__main__":
    main()
