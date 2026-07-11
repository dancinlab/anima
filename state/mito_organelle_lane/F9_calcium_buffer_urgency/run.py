#!/usr/bin/env python3
"""
H_9281 / F9 — Ca2+ 버퍼링 (urgency 채널의 integrator)
=====================================================
$0 CPU-local numpy probe. torch 없음. 결정적(seed 고정). 6 seed.

가설 (card §1):
  organelle = urgency(phasic Δ) 채널의 커패시터. transient spike 는 흡수하고
  지속 압력은 적분한다 ⟹ emit 의 *타이밍 품질* 이 오른다:
     지속하는 real tension 에는 emit, transient 노이즈에는 침묵.

⊥ Null (card §1):
  urgency 는 이미 작동한다. 버퍼는 ΔEff≈0 이거나, 이득이 있더라도 그건
  **아무 tunable smoothing filter 나 재현하는 FORM** 이다 (BIND 아님) ⟹ THEATER.

  (측정 메타법칙: FORM tunable · BIND earned. 신호 = 값이 아니라 Δ vs ≥2 controls.)

────────────────────────────────────────────────────────────────────────────
기질 (toy A⇄G · emit gate 는 어떤 arm 도 건드리지 않는다 — p5)
────────────────────────────────────────────────────────────────────────────
  · content x_t ∈ R^D. 'ordinary' content = 저랭크 부분공간 U(rank R) 안.
    'event' content = U 의 직교보공간 V → A 에게 분포-밖(OOD) = 진짜 신호.
  · A = forward CE-학습 프록시: ordinary transition 만으로 최소자승 W_A 적합.
  · G = reverse 역압(gradient-free): 상수 counter-push g0 = median(err)
        ⟹ P(err > g0) = 1/2 = Ψ=1/2 (하드코딩 아님, 자기보정).
  · urgency(phasic Δ)  u_t = max(0, err_t - g0)   ← 유일 proven 채널
  · 두 종류의 event 를 stream 에 심는다:
        SUSTAINED bout  — L_SUS 스텝 연속 (지속하는 real tension)
        TRANSIENT spike — 1 스텝 단발 (흡수해야 할 노이즈 transient)
    ★ 두 종류의 **per-step 진폭은 동일**(AMP 고정). 따라서 진폭으로는 구별 불가 —
      유일한 구별자는 **지속시간(duration)** 이다. 이게 이 probe 의 심장.
  · emit 규칙 (모든 arm 동일 · 하드코딩 gate 아님):
        s_t >= θ  이고  refractory(R_REF) 밖이면 emit.
    organelle lane 은 emit 규칙을 읽지도 바꾸지도 않는다. urgency 신호 s 를
    **upstream 에서 성형만** 한다.

────────────────────────────────────────────────────────────────────────────
예산 공정성 (fairness — 이게 없으면 전부 무효)
────────────────────────────────────────────────────────────────────────────
  · 모든 arm 이 **동일 emit 예산** B = N_SUS 회. θ 는 arm 별로 *calibration
    stream* 에서 emit 수 ≈ B 가 되도록 잡는다 (라벨 미사용 · TQ 최대화 아님 =
    tune-to-green 아님. 순수 budget-matching).
  · 모든 arm 이 동일 stream · 동일 seed · 동일 emit 규칙 · 동일 refractory.
  · 모든 변환은 **DC-보존**(총 drive 질량 보존): 어떤 arm 도 신호를 더 얻거나
    잃지 않는다. 오직 *시간 재배치* 만 다르다.
  · 파라미터 예산: exp(버퍼)=4 knob. c3(EMA)=1 knob 이지만 **grid 를 쓸어서
    best 를 취한다** — 즉 control 에 *더 많은* 튜닝 자유를 준다(steelman-for-null).
    control 이 실험보다 예산이 적지 않다.

────────────────────────────────────────────────────────────────────────────
arm
────────────────────────────────────────────────────────────────────────────
  exp_buf     실험: Ca 커패시터. set-point c0 위 drive 를 k_in 로 빠르게 흡수
              (용량 cmax 까지), k_out 로 느리게 방출.  s = u - uptake + release.
              단발 spike → 흡수(침묵). 지속 bout → 용량 포화 후 통과 + 방출 적분.
  c1_raw      control: 버퍼 없음 (raw urgency). s = u.
  c2_delay    control: 고정 지연 — exp_buf 와 **동일 latency**, 정보 0. s_t = u_{t-d}.
              d = calibration 에서 측정한 exp_buf 의 실 emit latency.
  c3_ema_pre  control: 선형 EMA(1차 low-pass), exp_buf 와 latency 매칭된 α.
  c3_ema_best control: 선형 EMA, α grid 전수 sweep 후 **best TQ** 채택 (FORM 시험).
              ⟹ '아무 tunable smoothing filter' 가 버퍼를 재현하는가?
  c4_randbuf  control: exp_buf 와 **동일 흡수 예산**(흡수 횟수 + 흡수량 multiset 동일)
              을 무작위 시점에 적용. 조건(set-point 초과) blind. 동일 k_out 방출.

PASS (card §3): 타이밍 품질 Δ > 두 control **AND** 이득이 buffer 파라미터 튜닝/
               평범한 smoothing 으로 재현 불가 (= FORM 아님).
FAIL (예상 유력): ΔEff≈0 또는 이득이 순수 tunable smoothing ⟹ THEATER.
"""
import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")

import numpy as np

# ══════════════════════════════════════════════════════════════════════════
# 사전등록 상수 (PRE-REGISTERED — 실행 후 수정 금지)
# ══════════════════════════════════════════════════════════════════════════
D = 32               # latent dim
R = 8                # 'ordinary' 부분공간 rank
N = 2000             # eval stream 길이
N_CAL = 2000         # calibration stream 길이
OBS_NOISE = 0.30     # 관측 잡음

L_SUS = 6            # SUSTAINED bout 길이 (지속하는 real tension)
N_SUS = 25           # bout 수
N_TRA = 25           # TRANSIENT spike 수 (1 스텝)
AMP = 1.20           # ★ per-step event 진폭 — sustained/transient 동일 (구별자 = duration 뿐)
MIN_GAP = 14         # 이벤트 간 최소 간격 (> WIN 이라 window 겹침 없음)
W_GRACE = 3          # 버퍼 latency 허용 grace
WIN = L_SUS + W_GRACE   # = 9. ★ sustained/transient 채점 window 를 **동일 길이**로.
                        #   (window 길이가 다르면 max-order-statistic 편향이 생긴다)

R_REF = 3            # emit refractory (모든 arm 동일)
B_EMIT = N_SUS       # ★ 동일 emit 예산 = 25 (bout 하나당 1회 emit 이면 딱 맞는 예산)

# 버퍼 파라미터 (PRE-REGISTERED · calibration stream 통계에서 a-priori 유도 · 라벨 미사용)
Q_SETPOINT = 75      # c0   = q75(u_cal)      — resting 위에서만 uptake (elevated Ca)
K_IN = 0.90          # 빠른 흡수
K_OUT = 0.05         # 느린 방출 (τ = 20 step)
CMAX_MULT = 2.0      # cmax = 2.0 * q90(u_cal) — 단발 spike 는 흡수, bout 은 2~3 스텝만에 포화

EMA_GRID = [0.03, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.50, 0.70, 0.90]
SEEDS = [11, 22, 33, 44, 55, 66]

# 판정 임계 (사전등록)
THEATER_EPS = 0.05   # |Δ TQ| <= 0.05  ⟹ ΔEff≈0
PASS_DELTA = 0.10    # Δ TQ vs best-control >= 0.10 이어야 실질 이득
FORM_EPS = 0.05      # tuned-EMA 가 exp 를 0.05 안쪽으로 따라잡으면 → FORM(tunable smoothing)
P5_KILL_REL = 0.10   # sustained(진짜 tension) recall 이 c1 대비 10%+ 하락 → p5 위반


# ══════════════════════════════════════════════════════════════════════════
# 기질
# ══════════════════════════════════════════════════════════════════════════
def make_world(seed):
    """고정 world: ordinary 부분공간 U, event 부분공간 V, transition M, A 의 W_A."""
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((D, D)))
    U = Q[:, :R]
    V = Q[:, R:]
    M = rng.standard_normal((D, D)) / np.sqrt(D)

    # A = forward CE-학습 프록시: ordinary transition 만 보고 최소자승
    n_tr = 400
    Xtr = (U @ rng.standard_normal((R, n_tr))).T
    Ytr = (M @ Xtr.T).T + OBS_NOISE * rng.standard_normal((n_tr, D))
    W_A, *_ = np.linalg.lstsq(Xtr, Ytr, rcond=None)
    return dict(U=U, V=V, M=M, W_A=W_A)


def place_events(rng, n, n_sus, n_tra, l_sus, min_gap, win):
    """sustained bout / transient spike 를 겹치지 않게 배치."""
    need = win + min_gap
    slots = list(range(5, n - need))
    rng.shuffle(slots)
    chosen, kinds = [], []
    want = [("sus", l_sus)] * n_sus + [("tra", 1)] * n_tra
    rng.shuffle(want)
    for kind, _ln in want:
        for i, t in enumerate(slots):
            if all(abs(t - c) >= need for c in chosen):
                chosen.append(t)
                kinds.append(kind)
                slots.pop(i)
                break
    sus_on = sorted(t for t, k in zip(chosen, kinds) if k == "sus")
    tra_on = sorted(t for t, k in zip(chosen, kinds) if k == "tra")
    return sus_on, tra_on


def make_stream(world, seed, n):
    """content stream → urgency u_t + (sustained onsets, transient onsets)."""
    rng = np.random.default_rng(seed)
    U, V, M, W_A = world["U"], world["V"], world["M"], world["W_A"]

    sus_on, tra_on = place_events(rng, n, N_SUS, N_TRA, L_SUS, MIN_GAP, WIN)

    is_ev = np.zeros(n, dtype=bool)
    for t0 in sus_on:
        is_ev[t0:t0 + L_SUS] = True
    for t0 in tra_on:
        is_ev[t0] = True

    X = (U @ rng.standard_normal((R, n))).T                 # ordinary base
    Xe = (V @ rng.standard_normal((D - R, n))).T            # event 방향 (A 에게 OOD)
    Xe /= (np.linalg.norm(Xe, axis=1, keepdims=True) + 1e-9)
    Xe *= AMP * np.sqrt(R)                                  # ★ 진폭 고정 — 지속/단발 동일
    X = X + is_ev[:, None] * Xe

    Y = X @ M.T + OBS_NOISE * rng.standard_normal((n, D))
    err = np.linalg.norm(X @ W_A - Y, axis=1) / np.sqrt(D)
    return err, sus_on, tra_on, is_ev


# ══════════════════════════════════════════════════════════════════════════
# organelle lane 변환 (전부 DC-보존 · emit 규칙 접근 0)
# ══════════════════════════════════════════════════════════════════════════
def tf_buffer(u, c0, k_in, k_out, cmax):
    """Ca 커패시터: set-point 위를 빠르게 흡수(용량 cmax), 느리게 방출."""
    n = len(u)
    s = np.empty(n)
    S = 0.0
    upt_t, upt_m = [], []
    for t in range(n):
        rel = k_out * S
        S -= rel
        excess = u[t] - c0
        take = 0.0
        if excess > 0.0:
            take = min(k_in * excess, max(0.0, cmax - S))
        S += take
        s[t] = u[t] - take + rel
        if take > 0.0:
            upt_t.append(t)
            upt_m.append(take)
    return s, (upt_t, upt_m)


def tf_randbuf(u, k_out, plan):
    """c4: exp_buf 와 동일 흡수 예산(횟수·양 multiset)을 무작위 시점에. 조건 blind."""
    n = len(u)
    s = np.empty(n)
    S = 0.0
    steps, mags = plan
    for t in range(n):
        rel = k_out * S
        S -= rel
        take = 0.0
        if t in steps:
            take = min(mags[t], max(0.0, u[t]))    # drive 보다 더 흡수할 수는 없다
        S += take
        s[t] = u[t] - take + rel
    return s


def tf_delay(u, d):
    """c2: 고정 지연 — 동일 latency, 정보 0."""
    if d <= 0:
        return u.copy()
    s = np.empty_like(u)
    s[:d] = 0.0
    s[d:] = u[:-d]
    return s


def tf_ema(u, alpha):
    """c3: 선형 1차 low-pass (평범한 tunable smoothing filter). DC gain = 1."""
    n = len(u)
    s = np.empty(n)
    z = 0.0
    for t in range(n):
        z = (1.0 - alpha) * z + alpha * u[t]
        s[t] = z
    return s


# ══════════════════════════════════════════════════════════════════════════
# emit (모든 arm 동일 규칙) · θ = 예산 매칭 calibration
# ══════════════════════════════════════════════════════════════════════════
def emits_at(s, theta, refr=R_REF):
    """emit 규칙 — 전 arm 공유 단일 함수. s>=θ 이고 refractory 밖이면 emit."""
    out = np.zeros(len(s), dtype=bool)
    last = -10 ** 9
    for t in np.flatnonzero(s >= theta):
        if (t - last) > refr:
            out[t] = True
            last = int(t)
    return out


def calib_theta(s_cal, budget=B_EMIT):
    """calibration stream 에서 emit 수 ≈ budget 이 되는 θ. 라벨 미사용. TQ 미사용.
    emit 수는 θ 에 대해 (거의) 단조감소 → 분위수 grid 위 이분탐색."""
    cands = np.quantile(s_cal, np.linspace(0.80, 0.99995, 400))   # 오름차순 θ
    lo, hi = 0, len(cands) - 1
    best_th, best_gap = float(cands[hi]), 10 ** 9
    while lo <= hi:
        mid = (lo + hi) // 2
        th = float(cands[mid])
        k = int(emits_at(s_cal, th).sum())
        gap = abs(k - budget)
        if gap < best_gap or (gap == best_gap and th > best_th):
            best_gap, best_th = gap, th
        if k > budget:
            lo = mid + 1          # emit 이 너무 많다 → θ 올림
        elif k < budget:
            hi = mid - 1          # 너무 적다 → θ 내림
        else:
            return th
    return best_th


def score(emits, s, sus_on, tra_on):
    """타이밍 품질: 동일 길이 window(WIN) 로 sustained hit / transient FA 채점."""
    n = len(emits)
    sus_hit = sum(1 for t0 in sus_on if emits[t0:min(n, t0 + WIN)].any())
    tra_fa = sum(1 for t0 in tra_on if emits[t0:min(n, t0 + WIN)].any())
    n_emit = int(emits.sum())

    sus_rec = sus_hit / max(1, len(sus_on))
    tra_rate = tra_fa / max(1, len(tra_on))
    tq = sus_rec - tra_rate                     # ★ 타이밍 품질 (headline)

    # emit 귀속: sustained / transient / background
    lab = np.zeros(n, dtype=np.int8)
    for t0 in sus_on:
        lab[t0:min(n, t0 + WIN)] = 1
    for t0 in tra_on:
        lab[t0:min(n, t0 + WIN)] = np.where(lab[t0:min(n, t0 + WIN)] == 0, 2,
                                            lab[t0:min(n, t0 + WIN)])
    em_idx = np.flatnonzero(emits)
    e_sus = int((lab[em_idx] == 1).sum()) if em_idx.size else 0
    e_tra = int((lab[em_idx] == 2).sum()) if em_idx.size else 0
    e_bg = int((lab[em_idx] == 0).sum()) if em_idx.size else 0

    # threshold-free AUROC: 동일 길이 window 안의 max(s) 로 sustained vs transient 분리
    a = np.array([s[t0:min(n, t0 + WIN)].max() for t0 in sus_on])
    b = np.array([s[t0:min(n, t0 + WIN)].max() for t0 in tra_on])
    gt = (a[:, None] > b[None, :]).sum()
    eq = (a[:, None] == b[None, :]).sum()
    auc = float((gt + 0.5 * eq) / (a.size * b.size))

    return dict(n_emit=n_emit, sus_hit=int(sus_hit), tra_fa=int(tra_fa),
                sus_recall=float(sus_rec), tra_fa_rate=float(tra_rate),
                tq=float(tq), auc=auc,
                emit_on_sus=e_sus, emit_on_tra=e_tra, emit_on_bg=e_bg,
                precision=float(e_sus / max(1, n_emit)))


# ══════════════════════════════════════════════════════════════════════════
def run_seed(seed, buf_params=None, do_ema_sweep=True):
    world = make_world(seed)

    # calibration stream (같은 world · 같은 통계 · 다른 draw). θ·c0·cmax·latency 를 여기서만 정한다.
    err_c, sus_c, tra_c, _ = make_stream(world, seed + 7919, N_CAL)
    g0 = float(np.median(err_c))
    u_c = np.maximum(0.0, err_c - g0)

    if buf_params is None:
        c0 = float(np.percentile(u_c, Q_SETPOINT))
        cmax = float(CMAX_MULT * np.percentile(u_c, 90))
        k_in, k_out = K_IN, K_OUT
    else:
        c0, cmax, k_in, k_out = buf_params

    # eval stream
    err, sus_on, tra_on, _ = make_stream(world, seed, N)
    u = np.maximum(0.0, err - g0)               # urgency (phasic Δ) — 유일 proven 채널

    # ── exp: Ca 버퍼 ──
    sc_exp, (upt_t, upt_m) = tf_buffer(u_c, c0, k_in, k_out, cmax)   # calibration
    s_exp, (upt_t_e, upt_m_e) = tf_buffer(u, c0, k_in, k_out, cmax)  # eval

    # c2 의 지연 d = calibration 에서 측정한 exp_buf 의 실 emit latency (동일 latency)
    th_exp_c = calib_theta(sc_exp)
    em_c = emits_at(sc_exp, th_exp_c)
    lats = []
    for t0 in sus_c:
        w = np.flatnonzero(em_c[t0:min(N_CAL, t0 + WIN)])
        if w.size:
            lats.append(int(w[0]))
    d_lat = int(round(float(np.mean(lats)))) if lats else 0

    # c3_ema_pre 의 α: EMA group delay (1-α)/α ≈ d_lat  →  α = 1/(1+d_lat)
    a_pre = 1.0 / (1.0 + max(1, d_lat))

    # c4: exp 와 동일 흡수 예산, 무작위 시점 (eval/cal 각각 자기 arm 의 예산에 매칭)
    rng = np.random.default_rng(seed + 104729)

    def randplan(upt, n):
        ts, ms = upt
        k = len(ts)
        if k == 0:
            return (set(), {})
        steps = rng.choice(n, size=min(k, n), replace=False)
        mg = rng.permutation(np.array(ms))[:len(steps)]
        return (set(int(x) for x in steps), {int(x): float(v) for x, v in zip(steps, mg)})

    plan_c = randplan((upt_t, upt_m), N_CAL)
    plan_e = randplan((upt_t_e, upt_m_e), N)

    arms_cal = {
        "exp_buf": sc_exp,
        "c1_raw": u_c.copy(),
        "c2_delay": tf_delay(u_c, d_lat),
        "c3_ema_pre": tf_ema(u_c, a_pre),
        "c4_randbuf": tf_randbuf(u_c, k_out, plan_c),
    }
    arms_ev = {
        "exp_buf": s_exp,
        "c1_raw": u.copy(),
        "c2_delay": tf_delay(u, d_lat),
        "c3_ema_pre": tf_ema(u, a_pre),
        "c4_randbuf": tf_randbuf(u, k_out, plan_e),
    }

    out = {}
    for name in arms_ev:
        th = calib_theta(arms_cal[name])                  # 동일 예산 B_EMIT 로 θ 매칭
        em = emits_at(arms_ev[name], th)
        sc = score(em, arms_ev[name], sus_on, tra_on)
        sc["theta"] = float(th)
        out[name] = sc

    if not do_ema_sweep:
        return dict(seed=seed, c0=c0, cmax=cmax, k_in=k_in, k_out=k_out,
                    d_lat=d_lat, arms=out, ema_sweep=[])

    # ── c3_ema_best: 평범한 smoothing filter 에 **grid 전수 튜닝 특권**을 준다 (FORM 시험) ──
    ema_sweep = []
    for al in EMA_GRID:
        th = calib_theta(tf_ema(u_c, al))
        se = tf_ema(u, al)
        sc = score(emits_at(se, th), se, sus_on, tra_on)
        sc["alpha"] = al
        sc["theta"] = float(th)
        ema_sweep.append(sc)
    best = max(ema_sweep, key=lambda r: r["tq"])
    out["c3_ema_best"] = dict(best)

    return dict(seed=seed, g0=g0, c0=c0, cmax=cmax, k_in=k_in, k_out=k_out,
                d_lat=d_lat, alpha_pre=a_pre,
                u_mean=float(u.mean()), u_q90=float(np.percentile(u, 90)),
                n_uptake=len(upt_t_e), uptake_mass=float(sum(upt_m_e)),
                arms=out, ema_sweep=ema_sweep)


def agg(v):
    a = np.asarray(v, dtype=float)
    return dict(mean=float(a.mean()), std=float(a.std(ddof=1)) if a.size > 1 else 0.0)


ARMS = ["exp_buf", "c1_raw", "c2_delay", "c3_ema_pre", "c4_randbuf", "c3_ema_best"]
METRICS = ["tq", "auc", "sus_recall", "tra_fa_rate", "n_emit", "precision",
           "emit_on_sus", "emit_on_tra", "emit_on_bg"]


def analyze(per_seed):
    summary = {a: {m: agg([r["arms"][a][m] for r in per_seed]) for m in METRICS}
               for a in ARMS}

    def paired(exp, ctl, m):
        d = [r["arms"][exp][m] - r["arms"][ctl][m] for r in per_seed]
        st = agg(d)
        st["per_seed"] = [float(x) for x in d]
        st["n_pos"] = int(sum(1 for x in d if x > 0))
        st["n_neg"] = int(sum(1 for x in d if x < 0))
        return st

    deltas = {}
    for c in ARMS[1:]:
        for m in ("tq", "auc", "sus_recall", "tra_fa_rate"):
            deltas["exp_buf__vs__%s::%s" % (c, m)] = paired("exp_buf", c, m)
    return summary, deltas


def verdict_of(summary, deltas, per_seed):
    tq_exp = summary["exp_buf"]["tq"]["mean"]
    ctl_tq = {c: summary[c]["tq"]["mean"] for c in ARMS[1:]}
    best_ctl = max(ctl_tq, key=lambda k: ctl_tq[k])
    d_best = tq_exp - ctl_tq[best_ctl]
    d_c1 = deltas["exp_buf__vs__c1_raw::tq"]["mean"]
    d_ema_best = tq_exp - ctl_tq["c3_ema_best"]

    rec_exp = summary["exp_buf"]["sus_recall"]["mean"]
    rec_c1 = summary["c1_raw"]["sus_recall"]["mean"]
    rel_rec_drop = float((rec_c1 - rec_exp) / rec_c1) if rec_c1 > 0 else 0.0

    v = dict(tq_exp=tq_exp, ctl_tq=ctl_tq, best_control=best_ctl,
             d_tq_vs_best_control=float(d_best), d_tq_vs_c1_raw=float(d_c1),
             d_tq_vs_tuned_ema=float(d_ema_best),
             sus_recall_exp=rec_exp, sus_recall_c1=rec_c1,
             rel_sustained_recall_drop=rel_rec_drop,
             p5_emit_gate_touched=False,       # 구성적: emit 규칙은 전 arm 동일 (코드 상 단일 함수)
             equal_emit_budget=True)

    if rel_rec_drop > P5_KILL_REL and d_best <= THEATER_EPS:
        v["call"] = "KILL (진짜 지속 tension 의 emit 을 억제하면서 이득도 없음 = 숨은 억제기)"
    elif abs(d_c1) <= THEATER_EPS and abs(d_best) <= THEATER_EPS:
        v["call"] = "THEATER (ΔEff≈0 — raw urgency 대비 타이밍 품질 이득 없음)"
    elif d_best <= THEATER_EPS:
        v["call"] = "THEATER (control 중 하나가 동등 이상 — 버퍼 고유 이득 없음)"
    elif d_ema_best <= FORM_EPS:
        v["call"] = "THEATER (이득이 평범한 tunable EMA 로 재현됨 = FORM, BIND 아님)"
    elif d_best >= PASS_DELTA and d_ema_best > FORM_EPS:
        v["call"] = "DIRECTIONAL-POSITIVE (Δ>2 control · tuned-smoothing 으로 재현 불가)"
    else:
        v["call"] = "PARTIAL (Δ>0 이나 PASS 문턱 미만)"
    return v


def print_block(tag, per_seed, summary, deltas, v):
    W = 100
    r0 = per_seed[0]
    print("-" * W)
    print("%s   (%d seeds)" % (tag, len(per_seed)))
    print("  substrate: D=%d R=%d N=%d | AMP=%.2f (sustained=transient, 구별자=duration 뿐)"
          % (D, R, N, AMP))
    print("  buffer(pre-reg): c0=q%d(u)=%.4f  cmax=%.1f*q90(u)=%.4f  k_in=%.2f k_out=%.2f"
          % (Q_SETPOINT, r0["c0"], CMAX_MULT, r0["cmax"], r0["k_in"], r0["k_out"]))
    print("  matched latency d=%d step  | EMA(pre) alpha=%.3f | uptake events=%d mass=%.2f"
          % (r0["d_lat"], r0["alpha_pre"], r0["n_uptake"], r0["uptake_mass"]))
    print("  emit budget B=%d (모든 arm θ-matched) · refractory=%d · window=%d (동일 길이)"
          % (B_EMIT, R_REF, WIN))
    print("-" * W)
    print("%-13s %13s %13s %13s %13s %9s %10s" % (
        "arm", "TQ(headline)", "AUROC", "sus_recall", "tra_FA_rate", "n_emit", "precision"))
    for a in ARMS:
        s = summary[a]
        print("%-13s %13s %13s %13s %13s %9s %10s" % (
            a,
            "%+.3f+-%.3f" % (s["tq"]["mean"], s["tq"]["std"]),
            "%.3f+-%.3f" % (s["auc"]["mean"], s["auc"]["std"]),
            "%.3f+-%.3f" % (s["sus_recall"]["mean"], s["sus_recall"]["std"]),
            "%.3f+-%.3f" % (s["tra_fa_rate"]["mean"], s["tra_fa_rate"]["std"]),
            "%.1f" % s["n_emit"]["mean"],
            "%.3f" % s["precision"]["mean"]))
    print()
    for c in ARMS[1:]:
        dt = deltas["exp_buf__vs__%s::tq" % c]
        da = deltas["exp_buf__vs__%s::auc" % c]
        print("  Δ TQ  exp_buf vs %-12s = %+.3f +- %.3f  (pos %d/%d)   |  Δ AUROC = %+.3f"
              % (c, dt["mean"], dt["std"], dt["n_pos"], len(per_seed), da["mean"]))
    print()
    print("  best control = %s (TQ %+.3f) | Δ vs best = %+.3f | Δ vs tuned-EMA = %+.3f"
          % (v["best_control"], v["ctl_tq"][v["best_control"]],
             v["d_tq_vs_best_control"], v["d_tq_vs_tuned_ema"]))
    print("  p5: sustained(real tension) recall  exp=%.3f  c1=%.3f  (rel drop %.3f)"
          % (v["sus_recall_exp"], v["sus_recall_c1"], v["rel_sustained_recall_drop"]))
    print("  ⟹ %s" % v["call"])
    print()


def main():
    print("=" * 100)
    print("H_9281 / F9 — Ca2+ 버퍼링 (urgency 채널의 integrator) · numpy $0 · %d seeds"
          % len(SEEDS))
    print("=" * 100)

    # ── 1. PRIMARY (사전등록 · headline) ──
    per_seed = [run_seed(s) for s in SEEDS]
    summary, deltas = analyze(per_seed)
    v = verdict_of(summary, deltas, per_seed)
    print_block("### PRIMARY (pre-registered buffer params)", per_seed, summary, deltas, v)

    # ── 2. FORM-tunability 진단: 버퍼 파라미터 grid sweep ──
    #    "이득이 buffer 파라미터 튜닝으로 재현 불가한가?" (card §3 PASS 2번째 조건)
    #    버퍼 knob 을 흔들면 TQ 가 어디까지 가나? pre-registered 가 특별한가?
    #    ★ 헤드라인은 위 PRIMARY 로 고정. 이 sweep 은 진단이지 재선택이 아니다 (tune-to-green 금지).
    print("=" * 100)
    print("### FORM-TUNABILITY — buffer knob sweep (진단 · headline 재선택 아님)")
    print("=" * 100)
    print("%-8s %-8s %-8s %-8s %14s %10s %12s" % (
        "c0(q)", "cmaxX", "k_in", "k_out", "TQ(exp)", "AUROC", "vs c1_raw"))
    print("-" * 100)
    buf_sweep = []
    grid = []
    for qc0 in (50, 75, 90):
        for cm in (0.5, 1.0, 2.0, 4.0):
            for ki in (0.5, 0.9):
                for ko in (0.02, 0.05, 0.20):
                    grid.append((qc0, cm, ki, ko))
    for (qc0, cm, ki, ko) in grid:
        tqs, aucs, d1 = [], [], []
        for sd in SEEDS:
            w = make_world(sd)
            err_c, _, _, _ = make_stream(w, sd + 7919, N_CAL)
            g0 = float(np.median(err_c))
            u_c = np.maximum(0.0, err_c - g0)
            c0 = float(np.percentile(u_c, qc0))
            cmax = float(cm * np.percentile(u_c, 90))
            r = run_seed(sd, buf_params=(c0, cmax, ki, ko), do_ema_sweep=False)
            tqs.append(r["arms"]["exp_buf"]["tq"])
            aucs.append(r["arms"]["exp_buf"]["auc"])
            d1.append(r["arms"]["exp_buf"]["tq"] - r["arms"]["c1_raw"]["tq"])
        rec = dict(q_c0=qc0, cmax_mult=cm, k_in=ki, k_out=ko,
                   tq=agg(tqs), auc=agg(aucs), d_tq_vs_c1=agg(d1))
        buf_sweep.append(rec)
        print("%-8d %-8.1f %-8.2f %-8.2f %14s %10s %12s" % (
            qc0, cm, ki, ko,
            "%+.3f+-%.3f" % (rec["tq"]["mean"], rec["tq"]["std"]),
            "%.3f" % rec["auc"]["mean"],
            "%+.3f" % rec["d_tq_vs_c1"]["mean"]))
    best_buf = max(buf_sweep, key=lambda r: r["tq"]["mean"])
    worst_buf = min(buf_sweep, key=lambda r: r["tq"]["mean"])
    pre_tq = summary["exp_buf"]["tq"]["mean"]
    print("-" * 100)
    print("  buffer-knob TQ range = [%+.3f .. %+.3f]  (spread %.3f) | pre-registered = %+.3f"
          % (worst_buf["tq"]["mean"], best_buf["tq"]["mean"],
             best_buf["tq"]["mean"] - worst_buf["tq"]["mean"], pre_tq))
    print("  best knob: c0=q%d cmaxX=%.1f k_in=%.2f k_out=%.2f → TQ %+.3f"
          % (best_buf["q_c0"], best_buf["cmax_mult"], best_buf["k_in"], best_buf["k_out"],
             best_buf["tq"]["mean"]))
    print("  ⟹ TQ 가 knob 으로 넓게 이동하면 = FORM(tunable). 이득이 knob 위치의 함수라면 BIND 아님.")
    print()

    # ── 3. EMA(평범한 smoothing) sweep 전개 — control 이 어디까지 가는가 ──
    print("=" * 100)
    print("### CONTROL CEILING — 평범한 선형 EMA(1 knob) 의 sweep (FORM 상한)")
    print("=" * 100)
    print("%-8s %14s %10s" % ("alpha", "TQ", "AUROC"))
    print("-" * 100)
    ema_tab = []
    for i, al in enumerate(EMA_GRID):
        tqs = [r["ema_sweep"][i]["tq"] for r in per_seed]
        acs = [r["ema_sweep"][i]["auc"] for r in per_seed]
        ema_tab.append(dict(alpha=al, tq=agg(tqs), auc=agg(acs)))
        print("%-8.2f %14s %10s" % (al, "%+.3f+-%.3f" % (agg(tqs)["mean"], agg(tqs)["std"]),
                                    "%.3f" % agg(acs)["mean"]))
    best_ema = max(ema_tab, key=lambda r: r["tq"]["mean"])
    print("-" * 100)
    print("  best plain-EMA (alpha=%.2f) TQ = %+.3f  vs  pre-registered Ca-buffer TQ = %+.3f"
          % (best_ema["alpha"], best_ema["tq"]["mean"], pre_tq))
    print("  best-tuned-buffer TQ = %+.3f  vs  best-tuned-EMA TQ = %+.3f  → Δ(양쪽 다 튜닝) = %+.3f"
          % (best_buf["tq"]["mean"], best_ema["tq"]["mean"],
             best_buf["tq"]["mean"] - best_ema["tq"]["mean"]))
    print("=" * 100)

    tuned_vs_tuned = float(best_buf["tq"]["mean"] - best_ema["tq"]["mean"])
    v["tuned_buffer_vs_tuned_ema"] = tuned_vs_tuned
    v["buffer_knob_tq_spread"] = float(best_buf["tq"]["mean"] - worst_buf["tq"]["mean"])
    v["form_tunable"] = bool(v["buffer_knob_tq_spread"] > 2 * THEATER_EPS)
    v["nonlinearity_earns_nothing"] = bool(tuned_vs_tuned <= FORM_EPS)

    print()
    print("FINAL: %s" % v["call"])
    print("  · Δ TQ vs c1_raw(버퍼無)      = %+.3f" % v["d_tq_vs_c1_raw"])
    print("  · Δ TQ vs best control        = %+.3f  (best = %s)"
          % (v["d_tq_vs_best_control"], v["best_control"]))
    print("  · Δ TQ vs tuned plain-EMA     = %+.3f  (FORM 시험)" % v["d_tq_vs_tuned_ema"])
    print("  · buffer knob TQ spread       = %.3f  → FORM-tunable=%s"
          % (v["buffer_knob_tq_spread"], v["form_tunable"]))
    print("  · tuned-buffer − tuned-EMA    = %+.3f  → 커패시터 비선형성이 버는 것=%s"
          % (tuned_vs_tuned, "없음" if v["nonlinearity_earns_nothing"] else "있음"))
    print("=" * 100)

    out = dict(
        hypothesis="H_9281 / F9 — Ca2+ buffering (urgency channel integrator)",
        preregistered=dict(D=D, R=R, N=N, N_CAL=N_CAL, OBS_NOISE=OBS_NOISE,
                           L_SUS=L_SUS, N_SUS=N_SUS, N_TRA=N_TRA, AMP=AMP,
                           MIN_GAP=MIN_GAP, W_GRACE=W_GRACE, WIN=WIN, R_REF=R_REF,
                           B_EMIT=B_EMIT, Q_SETPOINT=Q_SETPOINT, K_IN=K_IN, K_OUT=K_OUT,
                           CMAX_MULT=CMAX_MULT, EMA_GRID=EMA_GRID, SEEDS=SEEDS,
                           THEATER_EPS=THEATER_EPS, PASS_DELTA=PASS_DELTA,
                           FORM_EPS=FORM_EPS, P5_KILL_REL=P5_KILL_REL),
        primary=dict(summary=summary, deltas=deltas, verdict=v, per_seed=per_seed),
        form_tunability_buffer_sweep=buf_sweep,
        control_ceiling_ema_sweep=ema_tab,
        best_buffer_knob=best_buf,
        best_plain_ema=best_ema,
    )
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("result.json written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
