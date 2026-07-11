#!/usr/bin/env python3
"""
H_9277 / F5 — mtDNA 독자 계보 (병목 + uniparental) $0 probe.

가설: host와 독립적으로 drift하는 gradient-FREE organelle 게놈이
      (c1) host 고정복사 / (c2) gradient 업데이트 게놈 대비 reach/효율 Δ를 만든다.
⊥ Null: 선택압 없는 drift = 노이즈 ⇒ Δ≈0.

기질 (호흡 레인 · emit 레인 무접촉):
  - ATP = 보존 스칼라장. 예산 B가 d개 채널에 분배: gate = B * softmax(g),  sum(gate) = B  (항상).
  - 표현형성 단계에서만 개입: 채널 j의 관측 = gate_j * x_j + eta_j  (eta = 채널 노이즈 floor, 공유).
    → ATP를 못 받은 채널은 노이즈에 묻힌다 = "발화 불가". host w는 노이즈까지 같이 증폭하므로
      스케일로 복구 불가 = 게놈이 진짜 capability lever (landscape 비평탄).
  - host nucleus = A(forward CE): 세포별 w,b 를 full-batch GD로 학습.
  - organelle genome = mtDNA (gradient-FREE): 세포당 M copy(heteroplasmy), 세포 게놈 = copy 평균.
      분열: 병목(M중 k_b만 샘플) → 재증식 + 돌연변이  ⇒ drift
      융합: uniparental (한 계보 mtDNA 전체가 다른 세포를 덮어씀; host w는 그대로) ⇒ 계보 병합/소실
  - emit gate 없음. ATP는 downstream emit 결정에 배선 0 (p5-clean · 구성적으로 접근 불가).

arms (전부 동일 예산: 동일 cell수 · 동일 generation · 동일 host GD step · 동일 파라미터수 d(w)+d(g)):
  EXP  drift    : mtDNA 독립 계보 (병목 + 돌연변이 + uniparental 융합), 선택압 없음
  C1   hostcopy : organelle 게놈 = host 고정복사 (gate ∝ |w|) — 독립 계보 없음
  C2   gradorg  : organelle 게놈을 CE gradient로 업데이트 — 계보 독립 없음
  C3   nolineage: 세대마다 게놈 iid 재추첨 (EXP의 실현 std에 분산-매칭) — 계보 연속성만 제거
                  ⇒ EXP vs C3 = cadence·분산 매칭 = "계보(lineage)" 그 자체의 순수 Δ
refs (통제 아님 · 스케일 보정용): ORACLE(정답 채널에 ATP 집중) · UNIFORM(균등 ATP, 동결)
diag (F5 verdict 아님 · F11 예고): DRIFT+SEL — 융합 donor를 train-CE 낮은 세포로 (선택압 주입)

신호 = 값이 아니라 Δ vs ≥2 controls. multi-seed. tune-to-green 금지.
"""
import json
import os
import time

import numpy as np

# ---------------------------------------------------------------- pre-registered config (고정)
CFG = dict(
    d=48,          # 채널(=유닛) 수
    n_sig=6,       # 정보 채널 |S|
    B=6.0,         # ATP 총예산 (보존 스칼라)
    noise=0.6,     # 채널 노이즈 floor sigma (post-gate → 스케일 불변성 파괴)
    label_noise=0.15,
    n_train=1000,
    n_held=1000,
    n_cells=16,    # C
    gens=14,       # 세대 수
    steps=60,      # 세대당 host GD step (전 arm 동일)
    lr_w=0.5,
    lr_g=2.0,      # C2 게놈 gradient lr (control을 강하게 = 실험에 보수적)
    M=8,           # 세포당 mtDNA copy 수 (heteroplasmy)
    k_bottleneck=2,  # 분열 병목: M중 k_b만 샘플
    sigma_mut=0.35,  # PRIMARY 돌연변이 크기 (민감도: 0.1 / 1.0 도 보고)
    fuse_rate=0.5,   # 세대당 융합 이벤트 = fuse_rate * C/2
    init_het=0.10,   # 초기 heteroplasmy 분산
    eval_draws=3,    # held-out 노이즈 draw 평균
)
SEEDS = [0, 1, 2, 3, 4, 5]
# arm → 고정 정수 id (PYTHONHASHSEED 의존 제거 · 완전 결정적)
ARM_ID = {"exp_drift": 1, "c1_hostcopy": 2, "c2_gradorg": 3, "c3_nolineage": 4,
          "ref_oracle": 5, "ref_uniform": 6, "diag_drift_sel": 7}
SIGMAS = [0.10, 0.35, 1.00]   # 0.35 = PRIMARY (verdict는 여기서만)
PRIMARY_SIGMA = 0.35


# ---------------------------------------------------------------- substrate
def make_task(seed):
    r = np.random.default_rng(1000 + seed)
    d, k = CFG["d"], CFG["n_sig"]
    S = np.sort(r.choice(d, size=k, replace=False))
    a = r.normal(0, 1, size=k)
    Xtr = r.normal(0, 1, (CFG["n_train"], d))
    Xhe = r.normal(0, 1, (CFG["n_held"], d))

    def lab(X):
        z = X[:, S] @ a + CFG["label_noise"] * r.normal(0, 1, X.shape[0])
        return (z > 0).astype(np.float64)

    return Xtr, lab(Xtr), Xhe, lab(Xhe), S


def gate_of(g):
    """ATP 배분: gate = B * softmax(g)  → sum(gate) = B 보존."""
    z = g - g.max(axis=1, keepdims=True)
    e = np.exp(z)
    s = e / e.sum(axis=1, keepdims=True)
    return CFG["B"] * s, s


def acc_of(Xhe, yhe, gate, w, b, rng):
    """held-out reach: 채널 노이즈 draw 평균."""
    accs = np.zeros(w.shape[0])
    for _ in range(CFG["eval_draws"]):
        eta = rng.normal(0, CFG["noise"], Xhe.shape)
        logit = Xhe @ (gate * w).T + eta @ w.T + b[None, :]
        accs += ((logit > 0).astype(np.float64) == yhe[:, None]).mean(axis=0)
    return accs / CFG["eval_draws"]


def train_gen(Xtr, ytr, eta, g, w, b, grad_genome):
    """세대 내 host(+C2면 게놈) 학습. 전 arm 동일 step 수."""
    N = Xtr.shape[0]
    for _ in range(CFG["steps"]):
        gate, s = gate_of(g)
        logit = Xtr @ (gate * w).T + eta @ w.T + b[None, :]         # (N,C)
        p = 1.0 / (1.0 + np.exp(-np.clip(logit, -30, 30)))
        dl = (p - ytr[:, None]) / N                                  # (N,C)
        XtD = Xtr.T @ dl                                             # (d,C)
        dW = (gate * XtD.T) + (eta.T @ dl).T                         # (C,d)
        db = dl.sum(axis=0)
        if grad_genome:
            u = w * XtD.T                                            # dL/dgate  (C,d)
            dg = CFG["B"] * s * (u - (s * u).sum(axis=1, keepdims=True))
            g = g - CFG["lr_g"] * dg
        w = w - CFG["lr_w"] * dW
        b = b - CFG["lr_w"] * db
    return g, w, b


def train_ce(Xtr, ytr, eta, gate, w, b):
    """세포별 train CE (선택 diagnostic 용 · held-out 아님)."""
    logit = Xtr @ (gate * w).T + eta @ w.T + b[None, :]
    p = np.clip(1.0 / (1.0 + np.exp(-np.clip(logit, -30, 30))), 1e-9, 1 - 1e-9)
    return -(ytr[:, None] * np.log(p) + (1 - ytr[:, None]) * np.log(1 - p)).mean(axis=0)


# ---------------------------------------------------------------- organelle lineage ops
def bottleneck_divide(copies, rng, sigma_mut):
    """분열: 병목(M중 k_b 샘플) → 재증식 + 돌연변이. drift의 엔진."""
    C, M, d = copies.shape
    out = np.empty_like(copies)
    for c in range(C):
        idx = rng.choice(M, size=CFG["k_bottleneck"], replace=False)
        picks = rng.integers(0, CFG["k_bottleneck"], size=M)
        out[c] = copies[c, idx][picks]
    return out + rng.normal(0, sigma_mut, copies.shape)


def uniparental_fuse(copies, rng, ce=None):
    """융합: uniparental — donor 계보 mtDNA가 recipient를 통째로 대체 (혼합 없음).
    host w는 건드리지 않음 ⇒ organelle 계보 ≠ host 계보 (σ·thread)."""
    C = copies.shape[0]
    n_ev = int(CFG["fuse_rate"] * C / 2)
    lin_lost = 0
    for _ in range(n_ev):
        i, j = rng.choice(C, size=2, replace=False)
        if ce is None:
            donor, recip = (i, j) if rng.random() < 0.5 else (j, i)
        else:  # DIAG: 선택압 (train-CE 낮은 쪽이 donor)
            donor, recip = (i, j) if ce[i] <= ce[j] else (j, i)
        copies[recip] = copies[donor].copy()
        lin_lost += 1
    return copies, lin_lost


# ---------------------------------------------------------------- one arm run
def run_arm(arm, seed, sigma_mut=PRIMARY_SIGMA, std_sched=None):
    Xtr, ytr, Xhe, yhe, S = make_task(seed)
    C, d, M = CFG["n_cells"], CFG["d"], CFG["M"]
    rng = np.random.default_rng(7000 + seed * 97 + ARM_ID[arm] * 13)
    rng_eta = np.random.default_rng(31337 + seed)     # 채널 노이즈: arm 간 공유(paired)
    rng_ev = np.random.default_rng(555 + seed)        # held-out eval 노이즈: 고정

    w = np.zeros((C, d))
    b = np.zeros(C)
    copies = None

    if arm == "ref_oracle":
        g = np.zeros((C, d)); g[:, S] = 4.0
    elif arm == "ref_uniform":
        g = np.zeros((C, d))
    elif arm in ("exp_drift", "diag_drift_sel"):
        copies = rng.normal(0, CFG["init_het"], (C, M, d))
        g = copies.mean(axis=1)
    else:
        g = np.zeros((C, d))

    def _rowcorr(A, Bm):
        A = A - A.mean(axis=1, keepdims=True)
        Bm = Bm - Bm.mean(axis=1, keepdims=True)
        num = (A * Bm).sum(axis=1)
        den = np.linalg.norm(A, axis=1) * np.linalg.norm(Bm, axis=1) + 1e-12
        return num / den

    hist, g_std_sched = [], []
    g_prev = None
    for t in range(CFG["gens"]):
        eta = rng_eta.normal(0, CFG["noise"], Xtr.shape)   # 세대별 채널 노이즈 실현(arm 공유)

        g, w, b = train_gen(Xtr, ytr, eta, g, w, b, grad_genome=(arm == "c2_gradorg"))

        gate, _ = gate_of(g)
        acc = acc_of(Xhe, yhe, gate, w, b, np.random.default_rng(555 + seed + t))
        top = np.argsort(-gate, axis=1)[:, : CFG["n_sig"]]
        overlap = np.array([len(set(top[c]) & set(S.tolist())) for c in range(C)], dtype=float)
        eff_ch = CFG["B"] ** 2 / (gate ** 2).sum(axis=1)     # 실효 점화 채널 수 (IPR)
        gdiv = float(np.mean([np.linalg.norm(g[i] - g[j]) for i in range(C) for j in range(i + 1, C)]))
        g_std_sched.append(float(g.std()))
        # --- σ·thread FORM 진단 (값 = tunable · 창발 주장 아님)
        #  herit  = 세대 간 게놈 자기상관 (지속하는 계보인가)
        #  hostind= host로부터의 독립성 1-|corr(g, log|w|)| (별개 계보인가)
        herit = float(_rowcorr(g, g_prev).mean()) if g_prev is not None else float("nan")
        hostind = float(1.0 - np.abs(_rowcorr(g, np.log(np.abs(w) + 1e-3))).mean())
        hist.append(dict(gen=t, acc=float(acc.mean()), acc_best=float(acc.max()),
                         overlap=float(overlap.mean()), eff_ch=float(eff_ch.mean()),
                         g_div=gdiv, g_std=float(g.std()), herit=herit, host_indep=hostind))
        g_prev = g.copy()

        # ---- 게놈 업데이트 (세대 경계)
        if arm in ("exp_drift", "diag_drift_sel"):
            copies = bottleneck_divide(copies, rng, sigma_mut)
            ce = train_ce(Xtr, ytr, eta, gate, w, b) if arm == "diag_drift_sel" else None
            copies, _ = uniparental_fuse(copies, rng, ce=ce)
            g = copies.mean(axis=1)
        elif arm == "c1_hostcopy":
            g = np.log(np.abs(w) + 1e-3)                      # gate ∝ |w| : host 고정복사
        elif arm == "c3_nolineage":
            sd = std_sched[min(t, len(std_sched) - 1)] if std_sched else 0.1
            g = rng.normal(0, max(sd, 1e-6), (C, d))          # 분산 매칭 · 계보 연속성 0
        # c2: 학습 루프 안에서 이미 갱신 / refs: 동결

    f = hist[-1]
    return dict(arm=arm, seed=seed, sigma_mut=sigma_mut,
                final_acc=f["acc"], final_acc_best=f["acc_best"],
                final_overlap=f["overlap"], final_eff_ch=f["eff_ch"], final_gdiv=f["g_div"],
                final_herit=f["herit"], final_host_indep=f["host_indep"],
                acc_per_channel=f["acc"] / f["eff_ch"],
                g_std_sched=g_std_sched, hist=hist)


# ---------------------------------------------------------------- driver
def agg(rows, key="final_acc"):
    v = np.array([r[key] for r in rows], dtype=float)
    return float(v.mean()), float(v.std())


def main():
    t0 = time.time()
    ARMS = ["exp_drift", "c1_hostcopy", "c2_gradorg", "c3_nolineage",
            "ref_oracle", "ref_uniform", "diag_drift_sel"]
    runs = {s: {} for s in SIGMAS}

    for sig in SIGMAS:
        for seed in SEEDS:
            # EXP 먼저 → C3의 분산-매칭 스케줄 확보 (동일 seed = paired)
            e = run_arm("exp_drift", seed, sig)
            runs[sig].setdefault("exp_drift", []).append(e)
            for arm in ARMS:
                if arm == "exp_drift":
                    continue
                # sigma에 의존하지 않는 arm은 PRIMARY에서만 (동일 결과 재사용)
                if arm in ("c1_hostcopy", "c2_gradorg", "ref_oracle", "ref_uniform") and sig != PRIMARY_SIGMA:
                    continue
                r = run_arm(arm, seed, sig, std_sched=e["g_std_sched"])
                runs[sig].setdefault(arm, []).append(r)

    out = dict(cfg=CFG, seeds=SEEDS, sigmas=SIGMAS, primary_sigma=PRIMARY_SIGMA, arms={}, paired={}, sens={})

    P = runs[PRIMARY_SIGMA]
    for arm, rows in P.items():
        m, s = agg(rows)
        mo, so = agg(rows, "final_overlap")
        me, se = agg(rows, "final_eff_ch")
        mp, sp = agg(rows, "acc_per_channel")
        md, sd = agg(rows, "final_gdiv")
        mb, sb = agg(rows, "final_acc_best")
        mh, sh = agg(rows, "final_herit")
        mi, si = agg(rows, "final_host_indep")
        out["arms"][arm] = dict(
            acc_mean=m, acc_std=s, acc_best_mean=mb, acc_best_std=sb,
            overlap_mean=mo, overlap_std=so, eff_ch_mean=me, eff_ch_std=se,
            acc_per_ch_mean=mp, acc_per_ch_std=sp, gdiv_mean=md, gdiv_std=sd,
            herit_mean=mh, herit_std=sh, host_indep_mean=mi, host_indep_std=si,
            per_seed_acc=[r["final_acc"] for r in rows],
        )

    exp = np.array([r["final_acc"] for r in P["exp_drift"]])
    for ctrl in ("c1_hostcopy", "c2_gradorg", "c3_nolineage"):
        c = np.array([r["final_acc"] for r in P[ctrl]])
        dlt = exp - c                                     # paired (동일 seed·동일 task·동일 노이즈)
        out["paired"][f"exp_minus_{ctrl}"] = dict(
            delta_mean=float(dlt.mean()), delta_std=float(dlt.std()),
            wins=int((dlt > 0).sum()), n=len(dlt), per_seed=[float(x) for x in dlt],
        )
    # 핵심 판정: Δ vs 두 강한 control 중 최댓값
    best_ctrl = np.maximum(np.array([r["final_acc"] for r in P["c1_hostcopy"]]),
                           np.array([r["final_acc"] for r in P["c2_gradorg"]]))
    d_best = exp - best_ctrl
    out["paired"]["exp_minus_BEST_of_c1c2"] = dict(
        delta_mean=float(d_best.mean()), delta_std=float(d_best.std()),
        wins=int((d_best > 0).sum()), n=len(d_best))

    for sig in SIGMAS:
        e = np.array([r["final_acc"] for r in runs[sig]["exp_drift"]])
        c3 = np.array([r["final_acc"] for r in runs[sig]["c3_nolineage"]])
        ds = np.array([r["final_acc"] for r in runs[sig]["diag_drift_sel"]])
        out["sens"][str(sig)] = dict(
            exp_acc_mean=float(e.mean()), exp_acc_std=float(e.std()),
            c3_acc_mean=float(c3.mean()), c3_acc_std=float(c3.std()),
            exp_minus_c3_mean=float((e - c3).mean()), exp_minus_c3_std=float((e - c3).std()),
            diag_sel_acc_mean=float(ds.mean()), diag_sel_acc_std=float(ds.std()),
            diag_sel_minus_exp_mean=float((ds - e).mean()),
            exp_overlap_mean=float(np.mean([r["final_overlap"] for r in runs[sig]["exp_drift"]])),
            diag_sel_overlap_mean=float(np.mean([r["final_overlap"] for r in runs[sig]["diag_drift_sel"]])),
        )

    out["chance_acc"] = 0.5
    out["wall_sec"] = time.time() - t0
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, "result.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(f"[wall {out['wall_sec']:.1f}s]  seeds={SEEDS}  primary sigma_mut={PRIMARY_SIGMA}")
    print(f"{'arm':<16}{'held-out acc':>18}{'overlap|S|=6':>16}{'eff_ch':>8}{'acc/ch':>8}"
          f"{'herit':>8}{'host_indep':>11}")
    for arm in ARMS:
        a = out["arms"][arm]
        print(f"{arm:<16}{a['acc_mean']:>10.4f}±{a['acc_std']:<7.4f}"
              f"{a['overlap_mean']:>9.2f}±{a['overlap_std']:<6.2f}"
              f"{a['eff_ch_mean']:>8.2f}{a['acc_per_ch_mean']:>8.4f}"
              f"{a['herit_mean']:>8.3f}{a['host_indep_mean']:>11.3f}")
    print("\n-- paired Δ (동일 seed·task·노이즈) --")
    for k, v in out["paired"].items():
        print(f"  {k:<28} Δ={v['delta_mean']:+.4f}±{v['delta_std']:.4f}  wins {v['wins']}/{v['n']}")
    print("\n-- sensitivity (sigma_mut) --")
    for sig, v in out["sens"].items():
        print(f"  sig={sig:<5} exp={v['exp_acc_mean']:.4f}  c3(no-lineage)={v['c3_acc_mean']:.4f} "
              f" exp−c3={v['exp_minus_c3_mean']:+.4f}±{v['exp_minus_c3_std']:.4f}"
              f" | DIAG drift+sel={v['diag_sel_acc_mean']:.4f} (ovl {v['diag_sel_overlap_mean']:.2f} vs exp {v['exp_overlap_mean']:.2f})")


if __name__ == "__main__":
    main()
