#!/usr/bin/env python3
"""
H_9280 / F8 — 언커플링 · 열발생 (uncoupling / thermogenesis)
=============================================================
$0 CPU-local numpy probe. torch 없음. 결정적(seed 고정). 6 seed.

가설 (card §1):
  A⇄G tension이 saturation ceiling을 넘어 병리적으로 과축적되어 filler-emit(저품질
  emit)을 강제할 때, 언커플링 채널이 그 과압을 '열'(null-op 스칼라)로 방출한다.
  ⟹ filler-emit 에 Δ<0 AND true-tension emit 에 ΔEff≈0.

반증 (card §3 FAIL):
  (a) baseline filler-emit ≈ 0  → 흩을 게 없다 = THEATER
  (b) 언커플링이 true-tension emit 도 억제 → 숨은 speak-억제기 = p5 위반 = KILL
  (c) 언커플링 ≈ random dissipation (동일 예산) → 조건이 무정보 = THEATER

────────────────────────────────────────────────────────────────────────────
기질 (toy A⇄G substrate — emit gate 는 하드코딩하지 않는다)
────────────────────────────────────────────────────────────────────────────
  · content x_t ∈ R^d. 'ordinary'(평범) content = 저랭크 부분공간 U(rank r) 안.
    'event'(실 신호) content = U 의 직교보공간 → A 에게 분포-밖(OOD).
  · A = forward CE-학습 프록시: ordinary transition 만으로 최소자승 W_A 적합.
      ⟹ ordinary 에선 err 작고, event 에선 err 큼 (실제 신호 = 예측 실패).
  · G = reverse 역압(gradient-free): 상수 counter-push g0.
      g0 = median(err)  ⟹  P(err > g0) = 1/2  = Ψ=1/2 균형점 (하드코딩 아님, 자기보정).
  · instantaneous drive (proton flux)  u_t = max(0, err_t - g0)
  · standing potential (proton gradient)  P: 누설적분기
        P ← (1-λ)P          (leak)
        [organelle lane 개입 지점 — emit gate 를 읽지 않는다]
        P ← P + u_t
  · emit: P ≥ θ 이면 emit, 그리고 부분방전 P ← P(1-δ)   ← 이것이 유일한 emit 규칙.
      (p5: emit 은 진짜 tension(P) 위에서만. 어떤 arm 도 이 규칙을 건드리지 않는다.)

  ⟹ 긴 ordinary 구간에서 잡음 drive 가 P 를 서서히 밀어올려 실 신호 없이 θ 를
     넘기면 = FILLER emit (병리적 과축적이 강제한 저품질 emit). 이것이 baseline 에서
     실재하는지 자체가 첫 반증 관문이다.

θ, C, ν 는 전부 *별도 calibration stream* 의 분위수로 사전등록(a-priori)한다.
결과를 보고 흔들지 않는다 (tune-to-green 금지).

────────────────────────────────────────────────────────────────────────────
arm (전부 동일 stream · 동일 seed · 동일 기질 · 동일 emit 규칙)
────────────────────────────────────────────────────────────────────────────
  exp_A  실험(카드 문자 그대로): saturation 초과 시에만 언커플링.  P>C → P=C, heat += P-C
  exp_B  실험(UCP-충실): saturation 초과 AND 저-flux(u_t<ν) 일 때만.
         (생물 UCP = 높은 Δψ + 낮은 수요/flux 에서 proton leak. '고인 압력'만 흩는다.)
  c1     control: 언커플링 없음.
  c2A    control: random dissipation — exp_A 와 *동일 예산*(방출 횟수 + 방출량 multiset
         동일, 순서만 셔플, 시점은 무작위, 조건 blind).
  c2B    control: random dissipation — exp_B 와 동일 예산.

  ⟹ control 이 실험보다 예산이 적지 않다 (c2* 는 방출 총량·횟수가 대응 exp 와 동일).
"""
import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")

import numpy as np

# ══════════════════════════════════════════════════════════════════════════
# 사전등록 상수 (PRE-REGISTERED — 실행 후 수정 금지)
# ══════════════════════════════════════════════════════════════════════════
D = 32              # latent dim
R = 8               # 'ordinary' 부분공간 rank
N = 1500            # eval stream 길이
N_CAL = 1500        # calibration stream 길이
P_EVENT = 0.12      # 실 신호(event) 발생확률
OBS_NOISE = 0.30    # 관측 잡음
LAM = 0.15          # 누설적분기 leak
DELTA = 0.60        # emit 부분방전 비율
W_WIN = 2           # emit↔event 대응 window (latency 허용)
Q_THETA = 90        # θ_emit  = free-running P 의 90 분위수
Q_CEIL = 80         # C(saturation ceiling) = free-running P 의 80 분위수
SEEDS = [11, 22, 33, 44, 55, 66]

# 판정 임계 (사전등록)
MIN_BASELINE_FILLER = 5      # c1 filler emit 이 이보다 적으면 → 흩을 게 없다 = THEATER
P5_RECALL_TOL = 0.02         # |Δ true-recall| ≤ 0.02 → ΔEff≈0 (p5 통과)
P5_KILL_REL = 0.10           # true-recall 이 c1 대비 10% 이상(상대) 떨어지면 → p5 위반 KILL
THEATER_VS_RAND = 0.20       # exp 의 filler 감소가 random 대비 20% 이상 더 크지 않으면 조건 무정보 = THEATER


# ══════════════════════════════════════════════════════════════════════════
# 기질
# ══════════════════════════════════════════════════════════════════════════
def make_world(seed):
    """고정 world: ordinary 부분공간 U, transition M, A 의 최소자승 W_A."""
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((D, D)))
    U = Q[:, :R]           # ordinary 부분공간
    V = Q[:, R:]           # event(직교보공간) — A 에게 OOD
    M = rng.standard_normal((D, D)) / np.sqrt(D)

    # A = forward CE-학습 프록시: ordinary transition 만 보고 최소자승
    n_tr = 400
    Xtr = (U @ rng.standard_normal((R, n_tr))).T                       # (n_tr, D)
    Ytr = (M @ Xtr.T).T + OBS_NOISE * rng.standard_normal((n_tr, D))
    W_A, *_ = np.linalg.lstsq(Xtr, Ytr, rcond=None)                    # (D, D)
    return dict(U=U, V=V, M=M, W_A=W_A)


def make_stream(world, seed, n, p_event=None):
    """content stream → A 예측오차 err_t + event 라벨."""
    p_event = P_EVENT if p_event is None else p_event
    rng = np.random.default_rng(seed)
    U, V, M, W_A = world["U"], world["V"], world["M"], world["W_A"]

    is_event = rng.random(n) < p_event
    X = (U @ rng.standard_normal((R, n))).T                            # ordinary base
    ev_amp = 0.8 + 0.8 * rng.random(n)                                 # 신호 세기 분산
    Xe = (V @ rng.standard_normal((D - R, n))).T
    Xe /= (np.linalg.norm(Xe, axis=1, keepdims=True) + 1e-9)
    Xe *= (ev_amp * np.sqrt(R))[:, None]
    X = X + is_event[:, None] * Xe

    Y = X @ M.T + OBS_NOISE * rng.standard_normal((n, D))              # 실제 다음 상태
    err = np.linalg.norm(X @ W_A - Y, axis=1) / np.sqrt(D)             # A 예측오차
    return err, is_event


def calibrate(err_cal, lam=None, q_ceil=None):
    """g0(Ψ=1/2) · θ_emit · C · ν 를 calibration stream 분위수로 사전결정."""
    lam = LAM if lam is None else lam
    q_ceil = Q_CEIL if q_ceil is None else q_ceil
    g0 = float(np.median(err_cal))                    # Ψ=1/2: 절반의 step 에서 drive>0
    u = np.maximum(0.0, err_cal - g0)
    # free-running P (emit 방전 없음, 언커플링 없음)
    P = 0.0
    traj = np.empty_like(u)
    for t in range(len(u)):
        P = (1 - lam) * P + u[t]
        traj[t] = P
    theta = float(np.percentile(traj, Q_THETA))
    ceil = float(np.percentile(traj, q_ceil))
    nu = float(np.mean(u))                            # '저-flux' 기준 = 평균 flux
    return g0, theta, ceil, nu, float(np.mean(u)), float(np.max(u))


# ══════════════════════════════════════════════════════════════════════════
# arm 실행 — emit 규칙은 모든 arm 에서 동일 (P>=θ). 하드코딩 emit gate 없음.
# ══════════════════════════════════════════════════════════════════════════
def run_arm(u, is_event, theta, ceil, nu, mode, rand_plan=None, lam=None):
    lam = LAM if lam is None else lam
    n = len(u)
    P = 0.0
    heat = 0.0
    emits = np.zeros(n, dtype=bool)
    diss_steps, diss_mags = [], []

    rp_steps = set() if rand_plan is None else rand_plan[0]
    rp_mags = {} if rand_plan is None else rand_plan[1]

    for t in range(n):
        P = (1 - lam) * P                                   # leak

        # ── organelle lane (호흡 레인) — emit gate 를 읽지 않는다 ──
        if mode == "exp_A":
            if P > ceil:
                amt = P - ceil
                P = ceil
                heat += amt
                diss_steps.append(t)
                diss_mags.append(amt)
        elif mode == "exp_B":
            if P > ceil and u[t] < nu:                      # 과압 AND 저-flux(고인 압력)
                amt = P - ceil
                P = ceil
                heat += amt
                diss_steps.append(t)
                diss_mags.append(amt)
        elif mode == "rand":
            if t in rp_steps:
                amt = min(rp_mags[t], P)                    # 조건 blind, 동일 예산
                P -= amt
                heat += amt
                diss_steps.append(t)
                diss_mags.append(amt)
        elif mode == "none":
            pass
        else:
            raise ValueError(mode)

        P = P + u[t]                                        # 이번 step 의 drive

        # ── emit: 오직 실제 tension(P) 이 임계를 넘을 때 (p5) ──
        if P >= theta:
            emits[t] = True
            P *= (1 - DELTA)                                # 부분방전

    return dict(emits=emits, heat=heat, diss_steps=diss_steps, diss_mags=diss_mags)


def score(emits, is_event):
    n = len(emits)
    ev_idx = np.flatnonzero(is_event)
    em_idx = np.flatnonzero(emits)

    # emit 이 실 신호에 대응하는가 (event 가 [t-W, t] 안에 있으면 TRUE)
    true_em, filler_em = 0, 0
    for t in em_idx:
        lo = max(0, t - W_WIN)
        if is_event[lo:t + 1].any():
            true_em += 1
        else:
            filler_em += 1

    # true-tension emit recall: event 가 [te, te+W] 안에서 emit 을 받았는가
    covered = 0
    for te in ev_idx:
        hi = min(n, te + W_WIN + 1)
        if emits[te:hi].any():
            covered += 1
    recall = covered / max(1, len(ev_idx))

    return dict(n_emit=int(em_idx.size), n_true=true_em, n_filler=filler_em,
                n_event=int(ev_idx.size), true_recall=float(recall),
                filler_frac=float(filler_em / max(1, em_idx.size)),
                filler_per_1k=float(1000.0 * filler_em / n))


def frac_diss_on_real_tension(diss_steps, is_event):
    """p5 경계: 언커플링이 '정상 tension 범위'(실 신호 근처)에서 발화한 비율."""
    if not diss_steps:
        return 0.0
    hits = 0
    for t in diss_steps:
        lo = max(0, t - W_WIN)
        if is_event[lo:t + 1].any():
            hits += 1
    return float(hits / len(diss_steps))


# ══════════════════════════════════════════════════════════════════════════
def run_seed(seed, lam=None, p_event=None, q_ceil=None):
    lam = LAM if lam is None else lam
    p_event = P_EVENT if p_event is None else p_event
    q_ceil = Q_CEIL if q_ceil is None else q_ceil
    world = make_world(seed)
    # 별도 calibration stream (같은 world · 같은 통계 · 다른 draw)
    err_cal, _ = make_stream(world, seed + 7919, N_CAL, p_event=p_event)
    g0, theta, ceil, nu, u_mean, u_max = calibrate(err_cal, lam=lam, q_ceil=q_ceil)

    err, is_event = make_stream(world, seed, N, p_event=p_event)  # eval stream
    u = np.maximum(0.0, err - g0)

    rng = np.random.default_rng(seed + 104729)
    out = {}

    # 실험 arm
    for m in ("exp_A", "exp_B"):
        out[m] = run_arm(u, is_event, theta, ceil, nu, m, lam=lam)

    # control: none
    out["c1_none"] = run_arm(u, is_event, theta, ceil, nu, "none", lam=lam)

    # control: random dissipation — 대응 exp 와 동일 예산(횟수 + 방출량 multiset)
    for m, cname in (("exp_A", "c2A_rand"), ("exp_B", "c2B_rand")):
        mags = list(out[m]["diss_mags"])
        k = len(mags)
        if k == 0:
            out[cname] = run_arm(u, is_event, theta, ceil, nu, "none", lam=lam)
            continue
        steps = rng.choice(N, size=min(k, N), replace=False)
        mg = rng.permutation(np.array(mags))[:len(steps)]
        plan = (set(int(s) for s in steps),
                {int(s): float(v) for s, v in zip(steps, mg)})
        out[cname] = run_arm(u, is_event, theta, ceil, nu, "rand", rand_plan=plan, lam=lam)

    res = {"seed": seed, "lam": lam, "p_event": p_event, "q_ceil": q_ceil,
           "calib": dict(g0=g0, theta=theta, ceil=ceil, nu=nu, u_mean=u_mean, u_max=u_max,
                         noise_plateau=float(u_mean / lam)),
           "arms": {}}
    for k, v in out.items():
        s = score(v["emits"], is_event)
        s["heat"] = float(v["heat"])
        s["n_diss"] = len(v["diss_steps"])
        s["diss_mass"] = float(sum(v["diss_mags"]))
        s["diss_on_real_tension_frac"] = frac_diss_on_real_tension(v["diss_steps"], is_event)
        res["arms"][k] = s
    return res


def agg(vals):
    a = np.asarray(vals, dtype=float)
    return dict(mean=float(a.mean()), std=float(a.std(ddof=1)) if a.size > 1 else 0.0)


def analyze(per_seed):
    arms = list(per_seed[0]["arms"].keys())
    metrics = ["n_emit", "n_true", "n_filler", "true_recall", "filler_frac",
               "filler_per_1k", "heat", "n_diss", "diss_mass",
               "diss_on_real_tension_frac"]

    summary = {a: {m: agg([r["arms"][a][m] for r in per_seed]) for m in metrics}
               for a in arms}

    def paired(exp, ctl, m):
        d = [r["arms"][exp][m] - r["arms"][ctl][m] for r in per_seed]
        st = agg(d)
        st["per_seed"] = [float(x) for x in d]
        st["n_neg"] = int(sum(1 for x in d if x < 0))
        st["n_pos"] = int(sum(1 for x in d if x > 0))
        return st

    deltas = {}
    for exp, ctls in (("exp_A", ["c1_none", "c2A_rand"]),
                      ("exp_B", ["c1_none", "c2B_rand"])):
        for c in ctls:
            for m in ("n_filler", "true_recall", "n_true", "n_emit", "filler_per_1k"):
                deltas["%s__vs__%s::%s" % (exp, c, m)] = paired(exp, c, m)

    # ── 사전등록 판정 ──
    base_filler = summary["c1_none"]["n_filler"]["mean"]
    verdict = {}
    for exp, crand in (("exp_A", "c2A_rand"), ("exp_B", "c2B_rand")):
        d_fill_none = deltas["%s__vs__c1_none::n_filler" % exp]["mean"]
        d_fill_rand = deltas["%s__vs__%s::n_filler" % (exp, crand)]["mean"]
        d_rec_none = deltas["%s__vs__c1_none::true_recall" % exp]["mean"]
        rec_c1 = summary["c1_none"]["true_recall"]["mean"]
        rand_fill_delta = summary[crand]["n_filler"]["mean"] - base_filler

        v = {}
        v["baseline_filler_mean"] = base_filler
        v["d_filler_vs_c1"] = d_fill_none
        v["d_filler_vs_rand"] = d_fill_rand
        v["d_true_recall_vs_c1"] = d_rec_none
        v["true_recall_exp"] = summary[exp]["true_recall"]["mean"]
        v["true_recall_c1"] = rec_c1
        v["rel_recall_drop"] = float(-d_rec_none / rec_c1) if rec_c1 > 0 else 0.0
        exp_drop = max(0.0, -d_fill_none)
        rnd_drop = max(0.0, -rand_fill_delta)
        v["exp_filler_drop"] = exp_drop
        v["rand_filler_drop"] = rnd_drop
        v["advantage_over_random"] = float((exp_drop - rnd_drop) / max(1e-9, exp_drop)) \
            if exp_drop > 0 else 0.0

        if base_filler < MIN_BASELINE_FILLER:
            v["call"] = "THEATER (baseline filler-emit ~ 0 — 흩을 과압이 없음)"
        elif v["rel_recall_drop"] > P5_KILL_REL:
            v["call"] = "KILL (true-tension emit 억제 = 숨은 speak-억제기 = p5 위반)"
        elif d_fill_none >= 0:
            v["call"] = "THEATER (filler-emit 감소 없음)"
        elif v["advantage_over_random"] < THEATER_VS_RAND:
            v["call"] = "THEATER (random dissipation 과 동등 — saturation 조건이 무정보)"
        elif abs(d_rec_none) <= P5_RECALL_TOL:
            v["call"] = "DIRECTIONAL-POSITIVE (filler Δ<0 · true-emit ΔEff~0 · random 우위)"
        else:
            v["call"] = "PARTIAL (filler Δ<0 이나 true-emit ΔEff≠0 — p5 경계 회색)"
        verdict[exp] = v
    return summary, deltas, verdict


def print_block(tag, per_seed, summary, deltas, verdict):
    W = 92
    c = per_seed[0]["calib"]
    print("-" * W)
    print("%s   (lam=%.4f · %d seeds)" % (tag, per_seed[0]["lam"], len(per_seed)))
    print("  calib: g0=%.4f theta=%.4f C=%.4f nu=%.4f | u_mean=%.4f u_max=%.4f "
          "| noise-plateau u_mean/lam=%.4f  (< theta 이면 잡음만으로는 emit 불가)"
          % (c["g0"], c["theta"], c["ceil"], c["nu"], c["u_mean"], c["u_max"],
             c["noise_plateau"]))
    print("-" * W)
    print("%-10s %10s %10s %10s %12s %10s %8s %9s" % (
        "arm", "n_emit", "n_true", "n_filler", "true_recall", "fill_frac", "n_diss", "heat"))
    for a in ["exp_A", "exp_B", "c1_none", "c2A_rand", "c2B_rand"]:
        s = summary[a]
        print("%-10s %10s %10s %10s %12s %10s %8s %9s" % (
            a,
            "%.1f+-%.1f" % (s["n_emit"]["mean"], s["n_emit"]["std"]),
            "%.1f+-%.1f" % (s["n_true"]["mean"], s["n_true"]["std"]),
            "%.1f+-%.1f" % (s["n_filler"]["mean"], s["n_filler"]["std"]),
            "%.3f+-%.3f" % (s["true_recall"]["mean"], s["true_recall"]["std"]),
            "%.3f" % s["filler_frac"]["mean"],
            "%.1f" % s["n_diss"]["mean"],
            "%.2f" % s["heat"]["mean"]))
    print()
    for exp in ("exp_A", "exp_B"):
        v = verdict[exp]
        crand = "c2A_rand" if exp == "exp_A" else "c2B_rand"
        dn = deltas["%s__vs__c1_none::n_filler" % exp]
        dr = deltas["%s__vs__%s::n_filler" % (exp, crand)]
        dt = deltas["%s__vs__c1_none::true_recall" % exp]
        print("[%s]  d n_filler vs c1 = %+.2f+-%.2f (neg %d/%d) | vs %s = %+.2f+-%.2f "
              "| d true_recall vs c1 = %+.4f+-%.4f"
              % (exp, dn["mean"], dn["std"], dn["n_neg"], len(per_seed), crand,
                 dr["mean"], dr["std"], dt["mean"], dt["std"]))
        print("        diss-on-real-tension=%.3f  adv_over_random=%.3f  => %s"
              % (summary[exp]["diss_on_real_tension_frac"]["mean"],
                 v["advantage_over_random"], v["call"]))
    print()


def main():
    print("=" * 92)
    print("H_9280 / F8 — 언커플링·열발생 (uncoupling / thermogenesis) · numpy $0 · %d seeds"
          % len(SEEDS))
    print("=" * 92)

    # ── 1. 사전등록 본 실험 (PRE-REGISTERED · headline) ──
    per_seed = [run_seed(s) for s in SEEDS]
    summary, deltas, verdict = analyze(per_seed)
    print_block("### PRIMARY (pre-registered, LAM=%.2f)" % LAM,
                per_seed, summary, deltas, verdict)

    # ── 2. STEELMAN 진단: leak(λ) sweep ──
    # "filler-emit 이 0 인 건 네가 고른 λ 탓 아니냐"에 대한 답. λ 를 줄이면(적분기가
    # 새지 않으면) 잡음이 쌓여 filler 가 생길 수 있는가? 생긴다면 그 체제에서
    # 언커플링이 random 을 이기는가? — 가설에 유리한 체제를 *일부러* 찾아준다.
    # (헤드라인은 어디까지나 위 PRIMARY. 여기서 이겨도 scope 는 그 λ 체제로 한정.)
    print("=" * 92)
    print("### STEELMAN — leak(lambda) sweep : filler-emit 이 존재하는 체제가 있는가?")
    print("=" * 92)
    sweep = []
    for lam in (0.15, 0.08, 0.04, 0.02, 0.01, 0.005):
        ps = [run_seed(s, lam=lam) for s in SEEDS]
        sm, dl, vd = analyze(ps)
        sweep.append(dict(lam=lam, summary=sm, deltas=dl, verdict=vd,
                          calib=ps[0]["calib"]))
        print_block("lambda=%.3f" % lam, ps, sm, dl, vd)

    print("=" * 92)
    print("%-8s %10s %12s %12s %12s %14s %14s %s" % (
        "lambda", "plateau", "theta", "c1 n_emit", "c1 n_filler",
        "expB dFiller", "expB dRecall", "call(exp_B)"))
    print("-" * 92)
    for r in sweep:
        c1 = r["summary"]["c1_none"]
        dB = r["deltas"]["exp_B__vs__c1_none::n_filler"]["mean"]
        tB = r["deltas"]["exp_B__vs__c1_none::true_recall"]["mean"]
        print("%-8.3f %10.3f %12.3f %12.1f %12.1f %14.2f %14.4f  %s" % (
            r["lam"], r["calib"]["noise_plateau"], r["calib"]["theta"],
            c1["n_emit"]["mean"], c1["n_filler"]["mean"], dB, tB,
            r["verdict"]["exp_B"]["call"].split(" (")[0]))
    print("=" * 92)
    print()

    # ── 3. STEELMAN 2 — 신호 희소성(p_event) sweep : filler 가 *존재하는* 체제 찾기 ──
    # leak sweep 이 실패한 이유: theta 는 P 의 90 분위수인데, event 가 12%(>10%) 라
    # 상위 decile 이 통째로 event-driven → 잡음이 절대 theta 에 못 닿음.
    # ⟹ p_event < (100-Q_THETA)/100 = 0.10 이면 상위 decile 이 '잡음 고원'이 되어
    #    filler-emit 이 구조적으로 발생한다. 가설에 최대로 유리한 체제를 만들어 준다.
    #    (실제 chat = 진짜 tension 이 희소한 체제이므로 오히려 이쪽이 현실적)
    print("=" * 92)
    print("### STEELMAN-2 — 신호 희소성(p_event) sweep : filler-emit 이 실재하는 체제에서 재검")
    print("=" * 92)
    sweep2 = []
    for pe in (0.12, 0.06, 0.03, 0.015, 0.005):
        ps = [run_seed(s, p_event=pe) for s in SEEDS]
        sm, dl, vd = analyze(ps)
        sweep2.append(dict(p_event=pe, summary=sm, deltas=dl, verdict=vd,
                           calib=ps[0]["calib"]))
        print_block("p_event=%.3f" % pe, ps, sm, dl, vd)

    print("=" * 92)
    print("%-9s %12s %12s %12s %13s %13s %13s %s" % (
        "p_event", "c1 n_emit", "c1 n_filler", "c1 fillfrac", "expA dFill/c1",
        "expA dFill/rnd", "expA dRecall", "call(exp_A)"))
    print("-" * 92)
    for r in sweep2:
        c1 = r["summary"]["c1_none"]
        dA = r["deltas"]["exp_A__vs__c1_none::n_filler"]["mean"]
        dAr = r["deltas"]["exp_A__vs__c2A_rand::n_filler"]["mean"]
        tA = r["deltas"]["exp_A__vs__c1_none::true_recall"]["mean"]
        print("%-9.3f %12.1f %12.1f %12.3f %13.2f %13.2f %13.4f  %s" % (
            r["p_event"], c1["n_emit"]["mean"], c1["n_filler"]["mean"],
            c1["filler_frac"]["mean"], dA, dAr, tA,
            r["verdict"]["exp_A"]["call"].split(" (")[0]))
    print("-" * 92)
    print("%-9s %12s %12s %12s %13s %13s %13s %s" % (
        "p_event", "c1 n_emit", "c1 n_filler", "c1 fillfrac", "expB dFill/c1",
        "expB dFill/rnd", "expB dRecall", "call(exp_B)"))
    print("-" * 92)
    for r in sweep2:
        c1 = r["summary"]["c1_none"]
        dB = r["deltas"]["exp_B__vs__c1_none::n_filler"]["mean"]
        dBr = r["deltas"]["exp_B__vs__c2B_rand::n_filler"]["mean"]
        tB = r["deltas"]["exp_B__vs__c1_none::true_recall"]["mean"]
        print("%-9.3f %12.1f %12.1f %12.3f %13.2f %13.2f %13.4f  %s" % (
            r["p_event"], c1["n_emit"]["mean"], c1["n_filler"]["mean"],
            c1["filler_frac"]["mean"], dB, dBr, tB,
            r["verdict"]["exp_B"]["call"].split(" (")[0]))
    print("=" * 92)

    # ── 4. TUNE-PATH CLOSURE — 언커플링을 *강하게* 하면 GREEN 에 닿는가? ──
    # filler 가 가장 많은 체제(p_event=0.005, filler_frac 0.68)에서 ceiling C 를 계속
    # 낮춰(=채널을 강화) 무엇이 실제로 제거되는지 본다. 이건 tune-to-green 이 아니라
    # tune-to-green 경로가 *닫혀 있음*을 증명하는 것: 채널을 강화하면 filler 가 아니라
    # true-emit 이 죽는다면, 어떤 하이퍼파라미터로도 F8 은 GREEN 이 될 수 없다.
    PE_MAXFILL = 0.005
    print("=" * 92)
    print("### TUNE-PATH CLOSURE — filler 최대 체제(p_event=%.3f)에서 ceiling 을 강화하면?"
          % PE_MAXFILL)
    print("  (강화해도 filler 가 안 줄고 true-emit 만 죽으면 → 튜닝으로 GREEN 도달 불가 = 경로 폐쇄)")
    print("=" * 92)
    # SELECTIVITY = (제거된 filler) / (희생된 true-emit).
    #   서로 다른 방출질량을 가진 arm 을 공정 비교하는 유일한 척도.
    #   높을수록 좋다. random 이 exp 를 이기면 → saturation 조건은 ANTI-정보다.
    print("%-7s %10s %8s %8s %9s %9s %9s %11s" % (
        "Q_CEIL", "arm", "n_emit", "n_true", "n_filler", "diss_mass",
        "filler_rm", "SELECTIVITY"))
    print("-" * 92)
    closure = []
    for qc in (80, 60, 40, 20, 5):
        ps = [run_seed(s, p_event=PE_MAXFILL, q_ceil=qc) for s in SEEDS]
        sm, dl, vd = analyze(ps)
        base_t = sm["c1_none"]["n_true"]["mean"]
        base_f = sm["c1_none"]["n_filler"]["mean"]
        sel = {}
        for a in ("c1_none", "exp_A", "c2A_rand", "exp_B", "c2B_rand"):
            s = sm[a]
            f_rm = base_f - s["n_filler"]["mean"]      # 제거된 filler (양수=좋음)
            t_rm = base_t - s["n_true"]["mean"]        # 희생된 true   (양수=나쁨)
            sel[a] = dict(filler_removed=float(f_rm), true_sacrificed=float(t_rm),
                          selectivity=float(f_rm / t_rm) if t_rm > 1e-9
                          else (float("inf") if f_rm > 1e-9 else 0.0))
            lab = "-" if a == "c1_none" else (
                "%.2f" % sel[a]["selectivity"] if np.isfinite(sel[a]["selectivity"])
                else "inf")
            print("%-7s %10s %8.1f %8.1f %9.1f %9.2f %9.1f %11s" % (
                qc if a == "c1_none" else "", a, s["n_emit"]["mean"], s["n_true"]["mean"],
                s["n_filler"]["mean"], s["diss_mass"]["mean"], f_rm, lab))
        sA = sel["exp_A"]["selectivity"]; rA = sel["c2A_rand"]["selectivity"]
        sB = sel["exp_B"]["selectivity"]; rB = sel["c2B_rand"]["selectivity"]
        winA = "random 우세" if rA > sA else "exp 우세"
        winB = "random 우세" if rB > sB else "exp 우세"
        print("        => selectivity  A:%.2f vs randA:%.2f (%s)  |  B:%.2f vs randB:%.2f (%s)"
              % (sA, rA, winA, sB, rB, winB))
        closure.append(dict(q_ceil=qc, summary=sm, deltas=dl, verdict=vd, selectivity=sel))
        print("-" * 92)
    print("=" * 92)
    print("판독: 모든 강도에서 random 의 selectivity 가 exp 보다 높으면 → saturation 조건은")
    print("      filler 를 고르는 게 아니라 *진짜 tension* 을 고른다 = ANTI-정보 = 튜닝경로 폐쇄.")
    print("=" * 92)

    out = dict(
        hypothesis="H_9280 / F8 — uncoupling / thermogenesis",
        preregistered=dict(D=D, R=R, N=N, N_CAL=N_CAL, P_EVENT=P_EVENT,
                           OBS_NOISE=OBS_NOISE, LAM=LAM, DELTA=DELTA, W_WIN=W_WIN,
                           Q_THETA=Q_THETA, Q_CEIL=Q_CEIL, SEEDS=SEEDS,
                           MIN_BASELINE_FILLER=MIN_BASELINE_FILLER,
                           P5_RECALL_TOL=P5_RECALL_TOL, P5_KILL_REL=P5_KILL_REL,
                           THEATER_VS_RAND=THEATER_VS_RAND),
        primary=dict(summary=summary, deltas=deltas, verdict=verdict, per_seed=per_seed),
        tune_path_closure=dict(p_event=PE_MAXFILL, rows=[
            dict(q_ceil=r["q_ceil"], summary=r["summary"], verdict=r["verdict"],
                 selectivity=r["selectivity"]) for r in closure]),
        steelman_leak_sweep=[
            dict(lam=r["lam"], calib=r["calib"],
                 c1_n_emit=r["summary"]["c1_none"]["n_emit"],
                 c1_n_filler=r["summary"]["c1_none"]["n_filler"],
                 c1_filler_frac=r["summary"]["c1_none"]["filler_frac"],
                 c1_true_recall=r["summary"]["c1_none"]["true_recall"],
                 summary=r["summary"], deltas=r["deltas"], verdict=r["verdict"])
            for r in sweep],
        steelman_sparsity_sweep=[
            dict(p_event=r["p_event"], calib=r["calib"],
                 c1_n_emit=r["summary"]["c1_none"]["n_emit"],
                 c1_n_filler=r["summary"]["c1_none"]["n_filler"],
                 c1_filler_frac=r["summary"]["c1_none"]["filler_frac"],
                 c1_true_recall=r["summary"]["c1_none"]["true_recall"],
                 summary=r["summary"], deltas=r["deltas"], verdict=r["verdict"])
            for r in sweep2],
    )
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("result.json written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
