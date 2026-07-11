#!/usr/bin/env python3
"""
H_9280 / F8 — 언커플링·열발생 · **REFIRE** (원 판정 ⛔ INVALID 의 결함 수리 후 재발사)
=========================================================================================
$0 CPU-local numpy. torch 없음. 결정적(seed 고정). 24 analysis seed + 20 pilot seed.

원 INVALID 의 3대 결함과 이 스크립트의 수리:
  D1  θ 가 *event 를 포함한* stream 의 P90 분위수였고 P_EVENT=0.12 > 0.10 이라
      상위 decile 을 event 가 통째로 소유 ⟹ **filler=0 이 분위수 항등식으로 강제**됨(병이 없음).
      → FIX: θ 는 **event 가 전혀 없는(p_event=0) ordinary-only calibration stream** 에서 뽑는다.
             p_event 는 그와 **독립으로** 사전등록(0.05). 항등식 커플링 소멸.
             ⟹ baseline filler > 0 이 *구조적으로 보장*되고, 그것을 **실측으로 먼저 증명**한다(GATE-0).
  D2  C(ceiling) 를 emit 방전이 없는 free-running trajectory 에서 뽑아 실동작 분포 바깥에 놓임
      ⟹ 방출질량 0.332 < θ=0.637 = **개입이 no-op**(약을 안 줌).
      → FIX: θ·C 둘 다 **emit 규칙이 켜진 operating trajectory** 에서 자기무모순(fixed-point) 캘리브레이션.
             그리고 개입이 실제로 발화하는지를 **GATE-1 로 사전 검사**(발화율>0 · 방출질량 ≥ 1 emit-equivalent).
  D3  사전등록 KILL 변수(true_recall)를 사후에 n_true 로 바꿔치기 ⟹ verdict 무효.
      → FIX: KILL/PASS 변수를 **true_recall 하나로 고정**. n_true 는 진단용으로만 출력하고
             판정 함수는 절대 읽지 않는다(코드상 verdict() 는 true_recall·n_filler 만 인자로 받는다).

계측 규칙(organelle-lane census §8) 준수:
  R1  Δ = exp − max(controls) 금지 → **control별 paired-t 전부 보고** + pooled-mean.
  R2  "mean vs 1·std" 휴리스틱 금지 → **SEM / paired-t / 95% CI 만**.
  R3  **사전 MDE 계산**(pilot seed 20개 · 분석 seed 24개와 disjoint) → 검출력 게이트(GATE-2).
  R4  **정보 채널 증명**: (a) 처치 결정변수 = f(P_carry, u_t) = control 이 못 보는 입력의 함수(코드).
                          (b) 운영 대역에서 그 변수의 분산 > 0 · 발화율 ∈ (0,1) 실측.
  R5  V-gate 를 헤드라인 detector(n_filler · true_recall) 그 자체에 건다.
  R6  규약 민감도: emit↔event 귀속 window W ∈ {1,2,4} × {비대칭(카드), 대칭} 6 규약에서 부호 보존 확인.
  금지지표(conj_index · purity · 비율 · corr(n,demand)) 미사용.

p5 (핵심 검정 · 과제 조건 iv):
  언커플링은 **누적 standing potential(carry)** 만 건드린다. 이번 step 의 drive u_t 는 lane 통과
  *후에* 더해진다 ⟹ 실 신호(event)가 만드는 큰 flux 자체는 구조적으로 흩을 수 없다.
  그러나 약한 event 는 carry 라는 '받침대' 없이는 θ 를 못 넘을 수 있으므로 **recall 손실은 실재 가능**하다.
  ⟹ p5 위반 여부는 vacuous 하지 않고 **측정된다**. true_recall 상대하락 > 10% & 유의 ⟹ 즉시 KILL.
"""
import json
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")

import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# 사전등록 상수 (PRE-REGISTERED — 실행 결과를 보고 수정 금지)
# ══════════════════════════════════════════════════════════════════════════════
D = 32                 # latent dim
R = 8                  # 'ordinary' 부분공간 rank
N = 1500               # eval stream 길이
N_CAL = 4000           # calibration stream 길이 (ordinary-only)
OBS_NOISE = 0.30
LAM = 0.15             # 누설적분기 leak
DELTA = 0.60           # emit 부분방전
W_WIN = 2              # 카드 등록 규약 (emit↔event window · 비대칭)

P_EVENT = 0.05         # ★ θ 와 **독립**으로 사전등록 (calib stream 에는 event 가 0개)
Q_THETA = 97           # θ = ordinary-only *operating* post-drive 전위의 97 분위수
Q_CEIL = 90            # C = ordinary-only *operating* carry 전위의 90 분위수  (병리적 과압 = 상위 decile)

SEEDS = list(range(1001, 1025))        # 분석 seed 24개
PILOT_SEEDS = list(range(901, 921))    # MDE 전용 pilot seed 20개 (분석과 DISJOINT)

# 판정 임계 (사전등록 · 고정)
ALPHA = 0.05
P5_RECALL_TOL = 0.02        # 비열등 마진: Δtrue_recall 95%CI 하한 > −0.02 이면 ΔEff≈0
P5_KILL_REL = 0.10          # true_recall 상대하락 > 10% (유의) ⇒ p5 위반 KILL
GATE1_MASS_THETA = 1.0      # 개입 방출질량 ≥ θ×1.0 (= emit 1회분) 이어야 '약을 줬다'
GATE2_POWER_FRAC = 0.50     # MDE_filler ≤ 0.5 × baseline filler 이어야 검출력 충분
T975_23 = 2.0687            # t_{0.975, df=23}
T80_23 = 0.8575             # t_{0.80,  df=23}

HEADLINE_ARM = "exp_A"      # 카드 §3 실험 arm 문자 그대로 = "saturation 초과 시에만 언커플링"


# ══════════════════════════════════════════════════════════════════════════════
# 통계 (scipy 없이 · Student-t 정확값)
# ══════════════════════════════════════════════════════════════════════════════
def _betacf(a, b, x):
    tiny = 1e-30
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 200):
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


def _betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1.0 - x))
    bt = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_sf(t, df):
    """P(T > t) for Student-t."""
    if df <= 0:
        return float("nan")
    x = df / (df + t * t)
    p = 0.5 * _betai(df / 2.0, 0.5, x)
    return p if t > 0 else 1.0 - p


def paired_stats(deltas):
    """paired-CRN delta 배열 → mean/sd/sem/t/p(양측·단측)/95%CI."""
    a = np.asarray(deltas, dtype=float)
    n = a.size
    mean = float(a.mean())
    sd = float(a.std(ddof=1)) if n > 1 else 0.0
    sem = sd / math.sqrt(n) if n > 1 else 0.0
    df = n - 1
    if sem <= 1e-15:
        t = 0.0 if abs(mean) < 1e-15 else math.copysign(float("inf"), mean)
    else:
        t = mean / sem
    if math.isinf(t):
        p_two = 0.0
        # 단측(H1: mean < 0) p-value = CDF(t)
        p_less = 0.0 if t < 0 else 1.0
    else:
        p_two = 2.0 * t_sf(abs(t), df)
        p_less = 1.0 - t_sf(t, df)
    tcrit = T975_23 if df == 23 else _t_crit(df)
    ci = (mean - tcrit * sem, mean + tcrit * sem)
    return dict(n=int(n), mean=mean, sd=sd, sem=sem, t=float(t), df=int(df),
                p_two=float(p_two), p_one_less=float(p_less),
                ci95=[float(ci[0]), float(ci[1])],
                n_neg=int((a < 0).sum()), n_pos=int((a > 0).sum()),
                per_seed=[float(x) for x in a])


def _t_crit(df, q=0.975):
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 1.0 - t_sf(mid, df) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def one_sample_gt0(vals):
    a = np.asarray(vals, dtype=float)
    n = a.size
    mean = float(a.mean())
    sd = float(a.std(ddof=1)) if n > 1 else 0.0
    sem = sd / math.sqrt(n) if n > 1 else 0.0
    df = n - 1
    t = mean / sem if sem > 1e-15 else (float("inf") if mean > 0 else 0.0)
    p = t_sf(t, df) if not math.isinf(t) else 0.0
    return dict(mean=mean, sd=sd, sem=sem, t=float(t), p_gt0=float(p), n=int(n))


# ══════════════════════════════════════════════════════════════════════════════
# 기질 (toy A⇄G · emit gate 하드코딩 없음 · 모든 arm 에서 emit 규칙 동일)
# ══════════════════════════════════════════════════════════════════════════════
def make_world(seed):
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((D, D)))
    U = Q[:, :R]          # ordinary 부분공간 (A 의 학습 분포)
    V = Q[:, R:]          # event = 직교보공간 → A 에게 OOD
    M = rng.standard_normal((D, D)) / np.sqrt(D)
    n_tr = 400
    Xtr = (U @ rng.standard_normal((R, n_tr))).T
    Ytr = (M @ Xtr.T).T + OBS_NOISE * rng.standard_normal((n_tr, D))
    W_A, *_ = np.linalg.lstsq(Xtr, Ytr, rcond=None)     # A = forward CE 프록시
    return dict(U=U, V=V, M=M, W_A=W_A)


def make_stream(world, seed, n, p_event):
    rng = np.random.default_rng(seed)
    U, V, M, W_A = world["U"], world["V"], world["M"], world["W_A"]
    is_event = rng.random(n) < p_event
    X = (U @ rng.standard_normal((R, n))).T
    if p_event > 0:
        ev_amp = 0.8 + 0.8 * rng.random(n)
        Xe = (V @ rng.standard_normal((D - R, n))).T
        Xe /= (np.linalg.norm(Xe, axis=1, keepdims=True) + 1e-9)
        Xe *= (ev_amp * np.sqrt(R))[:, None]
        X = X + is_event[:, None] * Xe
    Y = X @ M.T + OBS_NOISE * rng.standard_normal((n, D))
    err = np.linalg.norm(X @ W_A - Y, axis=1) / np.sqrt(D)
    return err, is_event


def simulate_operating(u, theta, lam=LAM):
    """emit 규칙(방전 포함)이 켜진 *실동작* trajectory. carry(=leak 후·drive 전) 와 post(=drive 후)."""
    n = len(u)
    carry = np.empty(n)
    post = np.empty(n)
    P = 0.0
    for t in range(n):
        P = (1 - lam) * P
        carry[t] = P
        P = P + u[t]
        post[t] = P
        if P >= theta:
            P *= (1 - DELTA)
    return carry, post


def calibrate(world, seed):
    """θ·C·ν 를 **ordinary-only(event 0개) operating** 분포에서 자기무모순으로 사전결정.

    D1 FIX: calib stream 에 event 가 없으므로 θ 분위수와 p_event 사이의 항등식 커플링이 소멸한다.
    D2 FIX: free-running 이 아니라 emit 방전이 켜진 operating trajectory 의 분위수를 쓴다(fixed-point).
    """
    err_cal, _ = make_stream(world, seed + 7919, N_CAL, p_event=0.0)   # ★ event 0
    g0 = float(np.median(err_cal))            # Ψ=1/2 : ordinary step 의 절반에서 drive>0 (자기보정)
    u = np.maximum(0.0, err_cal - g0)

    # fixed-point: θ_{k+1} = P_QTHETA( operating post-drive | θ_k )
    P = 0.0
    free = np.empty_like(u)
    for t in range(len(u)):
        P = (1 - LAM) * P + u[t]
        free[t] = P
    theta = float(np.percentile(free, Q_THETA))
    hist = [theta]
    for _ in range(12):
        _, post = simulate_operating(u, theta)
        new = float(np.percentile(post, Q_THETA))
        theta = 0.5 * theta + 0.5 * new       # damped fixed point
        hist.append(theta)
        if abs(hist[-1] - hist[-2]) < 1e-6:
            break
    carry, post = simulate_operating(u, theta)
    ceil = float(np.percentile(carry, Q_CEIL))
    nu = float(np.median(u))                  # exp_B '저-flux' 기준
    diag = dict(
        g0=g0, theta=theta, ceil=ceil, nu=nu,
        theta_iters=len(hist),
        cal_emit_rate=float(np.mean(post >= theta)),      # ordinary-only 에서의 emit(=전부 filler) 비율
        carry_var=float(np.var(carry)),                   # R4(b): 결정변수의 분산 > 0
        carry_fire_rate_cal=float(np.mean(carry > ceil)), # R4(b): 발화율 ∈ (0,1)
        u_mean=float(np.mean(u)), u_med=nu, u_max=float(np.max(u)),
    )
    return g0, theta, ceil, nu, diag


# ══════════════════════════════════════════════════════════════════════════════
# arm — organelle lane 은 carry 만 건드린다. emit 규칙(P>=θ)은 전 arm 동일·불변.
#
#   R4(a) 정보채널: exp 의 결정변수 = (P_carry, u_t) = *입력 스트림의 함수*.
#                   c2(rand) 의 결정변수 = rng 뿐 = 입력에 blind. c3(uleak) 는 조건 자체가 없음.
# ══════════════════════════════════════════════════════════════════════════════
def run_arm(u, theta, ceil, nu, mode, plan=None, budget=None, uleak=0.0, lam=LAM):
    n = len(u)
    P = 0.0
    heat = 0.0
    emits = np.zeros(n, dtype=bool)
    steps, mags, carries = [], [], []
    spent = 0.0

    for t in range(n):
        P = (1 - lam) * P                      # leak
        carry = P                              # ← 결정변수 (누적 standing potential)

        # ───── organelle lane (호흡 레인) · emit gate 를 읽지 않는다 ─────
        amt = 0.0
        if mode == "exp_A":                    # 카드 문자 그대로: saturation 초과 시에만
            if carry > ceil:
                amt = carry - ceil
        elif mode == "exp_B":                  # UCP 충실: 과압 AND 저-flux(고인 압력)
            if carry > ceil and u[t] < nu:
                amt = carry - ceil
        elif mode == "rand":                   # control: 조건 blind · 동일 방출질량
            if t in plan:
                amt = min(plan[t], P)
                if budget is not None:
                    amt = min(amt, max(0.0, budget - spent))
        elif mode == "uleak":                  # control: 무조건 균일 추가누설 · 동일 방출질량
            amt = uleak * P
            if budget is not None:
                amt = min(amt, max(0.0, budget - spent))
        elif mode == "none":
            amt = 0.0
        else:
            raise ValueError(mode)

        if amt > 0.0:
            P -= amt
            heat += amt
            spent += amt
            steps.append(t)
            mags.append(amt)
            carries.append(carry)

        P = P + u[t]                           # 이번 step 의 drive (lane 통과 후 · 흩을 수 없음)

        # ───── emit: 오직 실제 tension(P) 이 임계를 넘을 때 (p5) ─────
        if P >= theta:
            emits[t] = True
            P *= (1 - DELTA)

    return dict(emits=emits, heat=float(heat), steps=steps, mags=mags,
                carries=carries, mass=float(sum(mags)))


def match_rand(u, theta, ceil, nu, target_mass, src_mags, rng):
    """동일 방출질량 random control. min(mag,P) 캡으로 예산 미달하는 원 결함을 fire-step 수를 늘려 교정."""
    if target_mass <= 0 or not src_mags:
        return run_arm(u, theta, ceil, nu, "none")
    mags = np.asarray(src_mags, dtype=float)
    k = len(mags)
    best = None
    for _ in range(12):
        k = int(min(N, max(1, k)))
        stp = rng.choice(N, size=k, replace=False)
        mg = rng.choice(mags, size=k, replace=True)
        plan = {int(s): float(m) for s, m in zip(stp, mg)}
        res = run_arm(u, theta, ceil, nu, "rand", plan=plan, budget=target_mass)
        if best is None or abs(res["mass"] - target_mass) < abs(best["mass"] - target_mass):
            best = res
        if res["mass"] >= 0.995 * target_mass:
            break
        k = int(k * min(3.0, target_mass / max(res["mass"], 1e-9))) + 1
    return best


def match_uleak(u, theta, ceil, nu, target_mass):
    """동일 방출질량 uniform-leak control (조건 없음 = '그냥 더 새게 한다'). bisection 으로 질량 매칭."""
    if target_mass <= 0:
        return run_arm(u, theta, ceil, nu, "none")
    lo, hi = 0.0, 0.95
    best = None
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        res = run_arm(u, theta, ceil, nu, "uleak", uleak=mid, budget=target_mass)
        if best is None or abs(res["mass"] - target_mass) < abs(best["mass"] - target_mass):
            best = res
        if res["mass"] < target_mass:
            lo = mid
        else:
            hi = mid
    return best


# ══════════════════════════════════════════════════════════════════════════════
# 채점 (규약 파라미터화 — R6)
# ══════════════════════════════════════════════════════════════════════════════
def score(emits, is_event, w=W_WIN, sym=False):
    n = len(emits)
    ev_idx = np.flatnonzero(is_event)
    em_idx = np.flatnonzero(emits)
    n_true = n_filler = 0
    for t in em_idx:
        lo = max(0, t - w)
        hi = min(n, t + w + 1) if sym else t + 1
        if is_event[lo:hi].any():
            n_true += 1
        else:
            n_filler += 1
    covered = 0
    for te in ev_idx:
        lo = max(0, te - w) if sym else te
        hi = min(n, te + w + 1)
        if emits[lo:hi].any():
            covered += 1
    recall = covered / max(1, len(ev_idx))
    return dict(n_emit=int(em_idx.size), n_true=int(n_true), n_filler=int(n_filler),
                n_event=int(ev_idx.size), n_covered=int(covered), true_recall=float(recall))


def diss_on_event_frac(steps, is_event, w=W_WIN):
    if not steps:
        return 0.0
    hits = sum(1 for t in steps if is_event[max(0, t - w):t + 1].any())
    return float(hits / len(steps))


# ══════════════════════════════════════════════════════════════════════════════
def run_seed(seed):
    world = make_world(seed)
    g0, theta, ceil, nu, cal = calibrate(world, seed)

    err, is_event = make_stream(world, seed, N, p_event=P_EVENT)
    u = np.maximum(0.0, err - g0)
    rng = np.random.default_rng(seed + 104729)

    arms = {}
    arms["c1_none"] = run_arm(u, theta, ceil, nu, "none")
    arms["exp_A"] = run_arm(u, theta, ceil, nu, "exp_A")
    arms["exp_B"] = run_arm(u, theta, ceil, nu, "exp_B")
    for ex, cr, cu, cc in (("exp_A", "c2A_rand", "c3A_uleak", "c4A_randcnt"),
                           ("exp_B", "c2B_rand", "c3B_uleak", "c4B_randcnt")):
        tm = arms[ex]["mass"]
        arms[cr] = match_rand(u, theta, ceil, nu, tm, arms[ex]["mags"], rng)
        arms[cu] = match_uleak(u, theta, ceil, nu, tm)
        # SUPPLEMENTARY(사전등록 아님 · 판정에 미사용): **횟수-매칭** random.
        # 동일 fire-step 수 · 동일 magnitude multiset · min(mag,P) 캡 ⇒ 방출질량이 exp 보다 *적다*.
        # = exp 보다 약한 개입. 이 arm 조차 exp 를 이기면 "operating-point 불공정" 반론이 닫힌다.
        k = len(arms[ex]["steps"])
        if k == 0:
            arms[cc] = run_arm(u, theta, ceil, nu, "none")
        else:
            stp = rng.choice(N, size=k, replace=False)
            mg = rng.permutation(np.asarray(arms[ex]["mags"], float))
            plan = {int(s): float(m) for s, m in zip(stp, mg)}
            arms[cc] = run_arm(u, theta, ceil, nu, "rand", plan=plan)

    # 운영대역 carry 통계 (R4(b) — 결정변수의 분산·발화율)
    carry_op, post_op = simulate_operating(u, theta)
    res = dict(seed=seed, calib=dict(cal),
               op=dict(carry_mean=float(carry_op.mean()), carry_var=float(carry_op.var()),
                       carry_p50=float(np.percentile(carry_op, 50)),
                       carry_p90=float(np.percentile(carry_op, 90)),
                       fire_rate=float(np.mean(carry_op > ceil))),
               arms={})
    for k, v in arms.items():
        s = score(v["emits"], is_event)
        s["mass"] = v["mass"]
        s["mass_per_theta"] = float(v["mass"] / theta)
        s["n_diss"] = len(v["steps"])
        s["fire_rate"] = float(len(v["steps"]) / N)
        s["mean_carry_at_fire"] = float(np.mean(v["carries"])) if v["carries"] else 0.0
        s["diss_on_event_frac"] = diss_on_event_frac(v["steps"], is_event)
        # 규약 민감도용 (R6)
        s["conv"] = {}
        for w in (1, 2, 4):
            for sym in (False, True):
                cs = score(v["emits"], is_event, w=w, sym=sym)
                s["conv"]["w%d_%s" % (w, "sym" if sym else "asym")] = dict(
                    n_filler=cs["n_filler"], true_recall=cs["true_recall"])
        res["arms"][k] = s
    return res


# ══════════════════════════════════════════════════════════════════════════════
# 사전등록 판정 함수 — **true_recall 과 n_filler 만 인자로 받는다** (D3 FIX: n_true 접근 불가)
# ══════════════════════════════════════════════════════════════════════════════
def verdict(base_filler_test, drug, power, d_filler_c1, d_filler_c2, d_filler_c3,
            d_recall_c1, recall_c1):
    """
    입력 계약:
      base_filler_test : c1 의 n_filler 가 0보다 큰가 (one-sample t)      ← GATE-0 (병의 실재)
      drug             : 개입이 실제로 발화했는가 (fire_rate>0 · mass≥θ)  ← GATE-1 (약의 투여)
      power            : MDE 게이트                                        ← GATE-2 (검출력)
      d_filler_*       : paired-t (exp − control) on **n_filler**         ← 헤드라인 efficacy
      d_recall_c1      : paired-t (exp − c1) on **true_recall**           ← 헤드라인 p5 (KILL 변수, 고정)
    """
    out = {}
    out["gate0_disease"] = bool(base_filler_test["p_gt0"] < ALPHA
                                and base_filler_test["mean"] >= power["mde_filler"])
    out["gate1_drug"] = bool(drug["fire_rate_min"] > 0.0
                             and drug["mass_per_theta_mean"] >= GATE1_MASS_THETA)
    out["gate2_power"] = bool(power["mde_filler"] <= GATE2_POWER_FRAC * base_filler_test["mean"]
                              and power["mde_recall"] <= P5_KILL_REL * recall_c1)

    rel_drop = float(-d_recall_c1["mean"] / recall_c1) if recall_c1 > 0 else 0.0
    out["rel_recall_drop"] = rel_drop
    kill = bool(rel_drop > P5_KILL_REL and d_recall_c1["p_one_less"] < ALPHA)
    out["p5_kill"] = kill

    eff_c1 = bool(d_filler_c1["mean"] < 0 and d_filler_c1["p_one_less"] < ALPHA)
    eff_c2 = bool(d_filler_c2["mean"] < 0 and d_filler_c2["p_one_less"] < ALPHA)
    eff_c3 = bool(d_filler_c3["mean"] < 0 and d_filler_c3["p_one_less"] < ALPHA)
    out["efficacy_vs_c1"] = eff_c1
    out["efficacy_vs_c2_rand"] = eff_c2
    out["efficacy_vs_c3_uleak"] = eff_c3
    out["efficacy"] = bool(eff_c1 and eff_c2)          # 사전등록: c1 AND 동량-random 둘 다 이겨야 함
    # 비열등(p5 안전): Δrecall 95%CI 하한 > −TOL
    out["safety_noninferior"] = bool(d_recall_c1["ci95"][0] > -P5_RECALL_TOL)

    if not out["gate1_drug"]:
        out["call"] = "INVALID (개입 no-op — 약이 투여되지 않음)"
    elif not out["gate0_disease"]:
        out["call"] = "THEATER-NO-DISEASE (baseline filler ≈ 0 — 흩을 과압이 없음 · licensed 음성)"
    elif not out["gate2_power"]:
        out["call"] = "INVALID (검출력 부족 — MDE > 축 동적범위/KILL 임계)"
    elif kill:
        out["call"] = "KILL (true_recall 억제 = 숨은 speak-억제기 = p5 위반)"
    elif out["efficacy"] and out["safety_noninferior"]:
        out["call"] = "DIRECTIONAL-POSITIVE (filler Δ<0 vs c1·동량random · true_recall 비열등)"
    elif out["efficacy"] and not out["safety_noninferior"]:
        out["call"] = "PARTIAL (filler Δ<0 이나 true_recall 비열등 실패 — p5 회색)"
    elif eff_c1 and not eff_c2:
        out["call"] = "THEATER (동량 random 과 동등 — saturation 조건이 무정보)"
    else:
        out["call"] = "THEATER (filler 감소 없음)"
    return out


def deltas_for(per_seed, exp, ctl, metric):
    return paired_stats([r["arms"][exp][metric] - r["arms"][ctl][metric] for r in per_seed])


def arm_summary(per_seed, arm, metric):
    v = [r["arms"][arm][metric] for r in per_seed]
    a = np.asarray(v, float)
    n = a.size
    sd = float(a.std(ddof=1)) if n > 1 else 0.0
    return dict(mean=float(a.mean()), sd=sd, sem=sd / math.sqrt(n) if n > 1 else 0.0)


# ══════════════════════════════════════════════════════════════════════════════
def main():
    W = 100
    print("=" * W)
    print("H_9280 / F8 REFIRE — 언커플링·열발생 · numpy $0 · analysis n=%d seeds · pilot n=%d"
          % (len(SEEDS), len(PILOT_SEEDS)))
    print("=" * W)

    # ── STEP 1. PILOT (분석 seed 와 DISJOINT) → 사전 MDE (R3 · 조건 v) ───────────
    print("\n### STEP 1 — PILOT (seed %d..%d · 분석 seed 와 disjoint) → 사전 MDE"
          % (PILOT_SEEDS[0], PILOT_SEEDS[-1]))
    pilot = [run_seed(s) for s in PILOT_SEEDS]
    p_base_filler = arm_summary(pilot, "c1_none", "n_filler")
    p_d_filler = deltas_for(pilot, HEADLINE_ARM, "c1_none", "n_filler")
    p_d_recall = deltas_for(pilot, HEADLINE_ARM, "c1_none", "true_recall")
    p_recall_c1 = arm_summary(pilot, "c1_none", "true_recall")

    n_a = len(SEEDS)
    kmde = (T975_23 + T80_23) / math.sqrt(n_a)          # α=.05 (단측 근사 보수적: 양측 t) · power .80
    mde_filler = kmde * p_d_filler["sd"]
    mde_recall = kmde * p_d_recall["sd"]
    power = dict(k=float(kmde), n_analysis=n_a,
                 sd_filler_pilot=p_d_filler["sd"], sd_recall_pilot=p_d_recall["sd"],
                 mde_filler=float(mde_filler), mde_recall=float(mde_recall),
                 pilot_baseline_filler=p_base_filler["mean"],
                 pilot_recall_c1=p_recall_c1["mean"],
                 dynamic_range_filler=p_base_filler["mean"],
                 kill_threshold_recall=float(P5_KILL_REL * p_recall_c1["mean"]))
    print("  pilot baseline filler (c1)      = %.2f ± %.2f (sd)   ← 축 동적범위(최대 감소량)"
          % (p_base_filler["mean"], p_base_filler["sd"]))
    print("  pilot paired-delta sd  filler   = %.3f  → MDE_filler = %.3f  (n=%d, α=.05, power=.80)"
          % (p_d_filler["sd"], mde_filler, n_a))
    print("  pilot paired-delta sd  recall   = %.4f → MDE_recall = %.4f  (KILL 임계 = %.4f)"
          % (p_d_recall["sd"], mde_recall, power["kill_threshold_recall"]))
    print("  POWER GATE: MDE_filler(%.3f) ≤ %.2f×동적범위(%.3f)? %s   |  MDE_recall(%.4f) ≤ KILL임계(%.4f)? %s"
          % (mde_filler, GATE2_POWER_FRAC, GATE2_POWER_FRAC * p_base_filler["mean"],
             "YES" if mde_filler <= GATE2_POWER_FRAC * p_base_filler["mean"] else "NO",
             mde_recall, power["kill_threshold_recall"],
             "YES" if mde_recall <= power["kill_threshold_recall"] else "NO"))

    # ── STEP 2. ANALYSIS RUN ────────────────────────────────────────────────────
    print("\n### STEP 2 — ANALYSIS (seed %d..%d · paired-CRN)" % (SEEDS[0], SEEDS[-1]))
    ps = [run_seed(s) for s in SEEDS]
    c = ps[0]["calib"]
    print("  calib (seed %d · ordinary-only operating fixed-point):" % SEEDS[0])
    print("    g0=%.4f  theta=%.4f  C=%.4f  nu=%.4f   (theta iters=%d)"
          % (c["g0"], c["theta"], c["ceil"], c["nu"], c["theta_iters"]))
    print("    ordinary-only emit rate(=전부 filler) = %.4f   carry_fire_rate = %.4f   carry_var = %.4f"
          % (c["cal_emit_rate"], c["carry_fire_rate_cal"], c["carry_var"]))
    print("    ★ D1 FIX 확인: calib stream 의 event 수 = 0 ⟹ theta 분위수와 P_EVENT(%.3f) 는 독립"
          % P_EVENT)

    # ── GATE-0 : 병이 실재하는가 (조건 i) ───────────────────────────────────────
    base_filler_vals = [r["arms"]["c1_none"]["n_filler"] for r in ps]
    g0test = one_sample_gt0(base_filler_vals)
    base_filler_test = dict(g0test)
    base_filler_test["mde_ref"] = float(mde_filler)
    print("\n### GATE-0 (조건 i · 병의 실재) — baseline(c1) filler-emit > 0 ?")
    print("    c1 n_filler = %.2f ± %.2f (sd) · SEM %.3f · t=%.2f · p(>0)=%.2e · min/max=%d/%d"
          % (g0test["mean"], g0test["sd"], g0test["sem"], g0test["t"], g0test["p_gt0"],
             min(base_filler_vals), max(base_filler_vals)))
    print("    c1 n_emit=%.1f · n_true=%.1f · n_event=%.1f · true_recall=%.4f"
          % (arm_summary(ps, "c1_none", "n_emit")["mean"],
             arm_summary(ps, "c1_none", "n_true")["mean"],
             arm_summary(ps, "c1_none", "n_event")["mean"],
             arm_summary(ps, "c1_none", "true_recall")["mean"]))
    print("    ⟹ GATE-0 %s (원 실험은 여기서 0.0±0.0 = 병 부재였다)"
          % ("PASS" if g0test["p_gt0"] < ALPHA and g0test["mean"] >= mde_filler else "FAIL"))

    # ── GATE-1 : 약이 실제로 투여됐는가 (조건 ii) ───────────────────────────────
    print("\n### GATE-1 (조건 ii · 약의 투여) — 개입이 실제로 발화하고 방출질량이 임계를 넘는가?")
    print("    %-11s %8s %10s %12s %14s %16s" % ("arm", "n_diss", "fire_rate", "mass",
                                                 "mass/theta", "mean_carry@fire"))
    drug = {}
    for a in ("exp_A", "exp_B", "c2A_rand", "c2B_rand", "c3A_uleak", "c3B_uleak",
              "c4A_randcnt", "c4B_randcnt"):
        nd = arm_summary(ps, a, "n_diss")["mean"]
        fr = arm_summary(ps, a, "fire_rate")
        ms = arm_summary(ps, a, "mass")
        mt = arm_summary(ps, a, "mass_per_theta")
        mc = arm_summary(ps, a, "mean_carry_at_fire")
        print("    %-11s %8.1f %10.4f %12.3f %14.2f %16.4f"
              % (a, nd, fr["mean"], ms["mean"], mt["mean"], mc["mean"]))
        drug[a] = dict(n_diss=nd, fire_rate=fr["mean"], mass=ms["mean"],
                       mass_per_theta=mt["mean"], mean_carry_at_fire=mc["mean"],
                       fire_rate_min=float(min(r["arms"][a]["fire_rate"] for r in ps)))
    hd = drug[HEADLINE_ARM]
    drug_head = dict(fire_rate_min=hd["fire_rate_min"], mass_per_theta_mean=hd["mass_per_theta"])
    print("    ⟹ GATE-1 (%s): fire_rate_min=%.4f>0 · mass=%.2f theta-equivalents ≥ %.1f ? %s"
          % (HEADLINE_ARM, hd["fire_rate_min"], hd["mass_per_theta"], GATE1_MASS_THETA,
             "PASS" if hd["fire_rate_min"] > 0 and hd["mass_per_theta"] >= GATE1_MASS_THETA else "FAIL"))
    print("    (원 실험: mass=0.332 < theta=0.637 ⟹ 0.52 theta-equivalents = no-op)")
    mm_A = abs(drug["c2A_rand"]["mass"] - drug["exp_A"]["mass"]) / max(1e-9, drug["exp_A"]["mass"])
    mm_B = abs(drug["c2B_rand"]["mass"] - drug["exp_B"]["mass"]) / max(1e-9, drug["exp_B"]["mass"])
    mu_A = abs(drug["c3A_uleak"]["mass"] - drug["exp_A"]["mass"]) / max(1e-9, drug["exp_A"]["mass"])
    print("    질량매칭 오차: c2A %.3f%% · c2B %.3f%% · c3A %.3f%%  (동량 control 성립)"
          % (100 * mm_A, 100 * mm_B, 100 * mu_A))

    # ── R4 : 정보 채널 증명 ────────────────────────────────────────────────────
    print("\n### R4 — 정보 채널 증명")
    print("  (a) 코드: exp 의 발화조건 = `carry > ceil` (exp_A) / `carry > ceil and u[t] < nu` (exp_B)")
    print("      carry = 입력 스트림 u_{0..t} 의 함수(누적 standing potential) · c2(rand) 의 조건 = rng 뿐(입력 blind)")
    print("      c3(uleak) 는 조건 자체가 없음(무조건 균일)")
    op_var = arm_summary(ps, "c1_none", "n_filler")  # placeholder to keep shape
    cv = float(np.mean([r["op"]["carry_var"] for r in ps]))
    cf = float(np.mean([r["op"]["fire_rate"] for r in ps]))
    print("  (b) 운영대역 실측: Var(carry)=%.4f > 0 · 발화율=%.4f ∈ (0,1) · "
          "mean carry@fire: exp_A=%.4f vs c2A_rand=%.4f (C=%.4f)"
          % (cv, cf, drug["exp_A"]["mean_carry_at_fire"], drug["c2A_rand"]["mean_carry_at_fire"],
             c["ceil"]))
    print("      ⟹ 처치의 결정변수는 control 이 못 보는 입력의 함수이고, 운영대역에서 분산>0 (항진 아님)")
    infoch = dict(carry_var=cv, fire_rate=cf,
                  carry_at_fire_exp=drug["exp_A"]["mean_carry_at_fire"],
                  carry_at_fire_rand=drug["c2A_rand"]["mean_carry_at_fire"], ceil=c["ceil"])

    # ── 헤드라인 : control별 paired-t (R1·R2) ──────────────────────────────────
    print("\n### 헤드라인 — control별 paired-t (max(controls) 금지 · SEM/t/95%CI 만)")
    dl = {}
    ctlmap = {"exp_A": ["c1_none", "c2A_rand", "c3A_uleak", "c4A_randcnt"],
              "exp_B": ["c1_none", "c2B_rand", "c3B_uleak", "c4B_randcnt"]}
    for exp in ("exp_A", "exp_B"):
        for ctl in ctlmap[exp]:
            for m in ("n_filler", "true_recall", "n_emit", "n_true"):
                dl["%s__vs__%s::%s" % (exp, ctl, m)] = deltas_for(ps, exp, ctl, m)

    print("  %-8s %-11s %-11s %9s %8s %8s %8s %10s %s"
          % ("exp", "control", "metric", "mean", "SEM", "t", "p(1-tail<)", "95%CI", "neg/n"))
    for exp in ("exp_A", "exp_B"):
        for ctl in ctlmap[exp]:
            for m in ("n_filler", "true_recall"):
                d = dl["%s__vs__%s::%s" % (exp, ctl, m)]
                print("  %-8s %-11s %-11s %+9.4f %8.4f %8.2f %10.2e  [%+.4f,%+.4f] %d/%d"
                      % (exp, ctl, m, d["mean"], d["sem"], d["t"], d["p_one_less"],
                         d["ci95"][0], d["ci95"][1], d["n_neg"], d["n"]))
    # pooled-mean 요약 (R1)
    pooled = {}
    for exp in ("exp_A", "exp_B"):
        for m in ("n_filler", "true_recall"):
            vals = [dl["%s__vs__%s::%s" % (exp, ctl, m)]["mean"] for ctl in ctlmap[exp][:3]]
            pooled["%s::%s" % (exp, m)] = float(np.mean(vals))   # 사전등록 3 control 만
    print("  pooled-mean(Δ over 3 controls): "
          + " · ".join("%s Δ%s=%+.4f" % (k.split("::")[0], k.split("::")[1], v)
                       for k, v in pooled.items()))

    # ── 전 arm 요약표 ──────────────────────────────────────────────────────────
    print("\n  %-11s %9s %9s %10s %13s %10s" % ("arm", "n_emit", "n_true", "n_filler",
                                                "true_recall", "mass"))
    summary = {}
    for a in ("exp_A", "exp_B", "c1_none", "c2A_rand", "c2B_rand", "c3A_uleak", "c3B_uleak",
              "c4A_randcnt", "c4B_randcnt"):
        summary[a] = {m: arm_summary(ps, a, m) for m in
                      ("n_emit", "n_true", "n_filler", "true_recall", "n_event", "mass",
                       "n_diss", "fire_rate", "mass_per_theta", "diss_on_event_frac",
                       "mean_carry_at_fire", "n_covered")}
        s = summary[a]
        print("  %-11s %9s %9s %10s %13s %10.3f"
              % (a,
                 "%.1f±%.1f" % (s["n_emit"]["mean"], s["n_emit"]["sd"]),
                 "%.1f±%.1f" % (s["n_true"]["mean"], s["n_true"]["sd"]),
                 "%.1f±%.1f" % (s["n_filler"]["mean"], s["n_filler"]["sd"]),
                 "%.4f±%.4f" % (s["true_recall"]["mean"], s["true_recall"]["sd"]),
                 s["mass"]["mean"]))

    # ── p5 핵심 검정 (조건 iv) ─────────────────────────────────────────────────
    print("\n### p5 핵심 검정 (조건 iv) — 언커플링이 정상 tension 의 true emit 을 건드리는가?")
    rec_c1 = summary["c1_none"]["true_recall"]["mean"]
    for exp in ("exp_A", "exp_B"):
        d = dl["%s__vs__c1_none::true_recall" % exp]
        lost = [r["arms"]["c1_none"]["n_covered"] - r["arms"][exp]["n_covered"] for r in ps]
        lt = paired_stats([float(x) for x in lost])
        rel = -d["mean"] / rec_c1 if rec_c1 > 0 else 0.0
        print("  [%s] Δtrue_recall vs c1 = %+.4f ± %.4f (SEM) · 95%%CI [%+.4f,%+.4f] · 상대하락 %.2f%%"
              % (exp, d["mean"], d["sem"], d["ci95"][0], d["ci95"][1], 100 * rel))
        print("        잃은 event 수(c1 커버 − exp 커버) = %+.2f ± %.2f (SEM) / event %.1f개 · "
              "비열등(CI하한 > −%.2f)? %s · KILL(상대하락>%.0f%% & 유의)? %s"
              % (lt["mean"], lt["sem"], summary["c1_none"]["n_event"]["mean"], P5_RECALL_TOL,
                 "YES" if d["ci95"][0] > -P5_RECALL_TOL else "NO",
                 100 * P5_KILL_REL,
                 "YES" if (rel > P5_KILL_REL and d["p_one_less"] < ALPHA) else "NO"))
        print("        발화가 event 근방(정상 tension)에서 일어난 비율 = %.4f  (random control = %.4f)"
              % (summary[exp]["diss_on_event_frac"]["mean"],
                 summary["c2A_rand" if exp == "exp_A" else "c2B_rand"]["diss_on_event_frac"]["mean"]))

    # ── 사전등록 판정 (D3 FIX: true_recall 고정 · n_true 미사용) ────────────────
    print("\n### 사전등록 VERDICT (KILL 변수 = true_recall · 사후 교체 없음)")
    verdicts = {}
    for exp, cr, cu in (("exp_A", "c2A_rand", "c3A_uleak"), ("exp_B", "c2B_rand", "c3B_uleak")):
        v = verdict(
            base_filler_test=base_filler_test,
            drug=dict(fire_rate_min=drug[exp]["fire_rate_min"],
                      mass_per_theta_mean=drug[exp]["mass_per_theta"]),
            power=power,
            d_filler_c1=dl["%s__vs__c1_none::n_filler" % exp],
            d_filler_c2=dl["%s__vs__%s::n_filler" % (exp, cr)],
            d_filler_c3=dl["%s__vs__%s::n_filler" % (exp, cu)],
            d_recall_c1=dl["%s__vs__c1_none::true_recall" % exp],
            recall_c1=rec_c1)
        verdicts[exp] = v
        print("  [%s] gate0_disease=%s gate1_drug=%s gate2_power=%s | eff_c1=%s eff_c2rand=%s "
              "eff_c3uleak=%s | safe=%s kill=%s"
              % (exp, v["gate0_disease"], v["gate1_drug"], v["gate2_power"],
                 v["efficacy_vs_c1"], v["efficacy_vs_c2_rand"], v["efficacy_vs_c3_uleak"],
                 v["safety_noninferior"], v["p5_kill"]))
        print("        ⟹ %s" % v["call"])

    # ── SUPPLEMENTARY: 횟수-매칭 random (operating-point 공정성 반론 차단) ──────
    print("\n### SUPPLEMENTARY (판정 미사용) — 횟수-매칭 random c4 (동일 fire 수 · 방출질량은 exp보다 *적음*)")
    for exp, cc in (("exp_A", "c4A_randcnt"), ("exp_B", "c4B_randcnt")):
        d = dl["%s__vs__%s::n_filler" % (exp, cc)]
        dr = dl["%s__vs__%s::true_recall" % (exp, cc)]
        print("  [%s] c4 mass=%.3f (exp %.3f · %.0f%%) · c4 n_diss=%.1f (exp %.1f) | "
              "Δn_filler = %+.2f ± %.2f (t=%+.2f) · Δrecall = %+.4f"
              % (exp, summary[cc]["mass"]["mean"], summary[exp]["mass"]["mean"],
                 100 * summary[cc]["mass"]["mean"] / max(1e-9, summary[exp]["mass"]["mean"]),
                 summary[cc]["n_diss"]["mean"], summary[exp]["n_diss"]["mean"],
                 d["mean"], d["sem"], d["t"], dr["mean"]))
    print("  ⟹ exp 가 *더 적은* 질량을 쓰는 blind arm 조차 못 이기면, '강도 불일치' 반론은 닫힌다.")

    # ── R6 규약 민감도 ────────────────────────────────────────────────────────
    print("\n### R6 — 규약 민감도 (emit↔event 귀속 window W ∈{1,2,4} × {asym(카드), sym})")
    print("  %-8s %-10s %14s %16s %10s" % ("exp", "convention", "Δn_filler vs c1",
                                           "Δn_filler vs rand", "Δrecall"))
    conv_rows = []
    for exp, cr in (("exp_A", "c2A_rand"), ("exp_B", "c2B_rand")):
        for key in ("w1_asym", "w2_asym", "w4_asym", "w1_sym", "w2_sym", "w4_sym"):
            df1 = paired_stats([r["arms"][exp]["conv"][key]["n_filler"]
                                - r["arms"]["c1_none"]["conv"][key]["n_filler"] for r in ps])
            df2 = paired_stats([r["arms"][exp]["conv"][key]["n_filler"]
                                - r["arms"][cr]["conv"][key]["n_filler"] for r in ps])
            dr = paired_stats([r["arms"][exp]["conv"][key]["true_recall"]
                               - r["arms"]["c1_none"]["conv"][key]["true_recall"] for r in ps])
            tag = "  ← 카드 등록값" if key == "w2_asym" else ""
            print("  %-8s %-10s %+9.2f(t%+.1f) %+11.2f(t%+.1f) %+9.4f%s"
                  % (exp, key, df1["mean"], df1["t"], df2["mean"], df2["t"], dr["mean"], tag))
            conv_rows.append(dict(exp=exp, conv=key, d_filler_c1=df1, d_filler_rand=df2,
                                  d_recall_c1=dr))
    sgn_ok = {}
    for exp in ("exp_A", "exp_B"):
        rows = [r for r in conv_rows if r["exp"] == exp]
        n_same = sum(1 for r in rows if r["d_filler_c1"]["mean"] < 0)
        n_same2 = sum(1 for r in rows if r["d_filler_rand"]["mean"] < 0)
        sgn_ok[exp] = dict(filler_vs_c1_neg=n_same, filler_vs_rand_neg=n_same2, n_conv=len(rows))
        print("  [%s] Δfiller<0 부호 보존: vs c1 %d/%d 규약 · vs 동량random %d/%d 규약"
              % (exp, n_same, len(rows), n_same2, len(rows)))

    # ── 저장 ──────────────────────────────────────────────────────────────────
    head = verdicts[HEADLINE_ARM]
    out = dict(
        hypothesis="H_9280 / F8 — uncoupling·thermogenesis — REFIRE (원 INVALID 결함 수리)",
        headline_arm=HEADLINE_ARM,
        preregistered=dict(D=D, R=R, N=N, N_CAL=N_CAL, P_EVENT=P_EVENT, OBS_NOISE=OBS_NOISE,
                           LAM=LAM, DELTA=DELTA, W_WIN=W_WIN, Q_THETA=Q_THETA, Q_CEIL=Q_CEIL,
                           SEEDS=SEEDS, PILOT_SEEDS=PILOT_SEEDS, ALPHA=ALPHA,
                           P5_RECALL_TOL=P5_RECALL_TOL, P5_KILL_REL=P5_KILL_REL,
                           GATE1_MASS_THETA=GATE1_MASS_THETA, GATE2_POWER_FRAC=GATE2_POWER_FRAC,
                           KILL_VARIABLE="true_recall (고정 · n_true 사용 금지)"),
        defect_fixes=dict(
            D1_quantile_identity="theta 는 event 0개인 ordinary-only calib stream 에서 · p_event 독립 사전등록",
            D2_noop_intervention="theta·C 를 emit 방전 켜진 operating trajectory 의 fixed-point 로 · GATE-1 로 방출질량 사전검사",
            D3_metric_swap="verdict() 가 n_true 를 인자로 받지 않음 — KILL/PASS 는 true_recall 고정"),
        power_mde=power,
        gate0_disease=base_filler_test,
        gate1_drug=drug,
        info_channel=infoch,
        summary=summary,
        deltas=dl,
        pooled_delta=pooled,
        verdict=verdicts,
        convention_sensitivity=dict(rows=conv_rows, sign_preserved=sgn_ok),
        per_seed=ps,
        pilot=dict(seeds=PILOT_SEEDS, baseline_filler=p_base_filler,
                   d_filler=p_d_filler, d_recall=p_d_recall),
    )
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * W)
    print("FINAL (headline arm = %s) ⟹ %s" % (HEADLINE_ARM, head["call"]))
    print("=" * W)
    print("result.json written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
