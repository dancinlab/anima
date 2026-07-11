#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9282 / F10 — 생합성(PGC-1a) · 수요주도 organelle 증식 vs 균일/랜덤 할당
=============================================================================
$0 CPU-local numpy probe.  torch 없음.  결정적(seed 고정).  emit gate 무접촉(p5).

레인
----
ORGANELLE LANE (제3 레인) — decode/emit 레인과 DISJOINT.
이 probe 는 "어떤 유닛이 발화 가능한가"(표현형성 단계 = 호흡용량 c_e)만 건드린다.
emit/silence 결정, speak(), tension 어디에도 배선 0.

기질
----
- E=16 expert (MoE-유사), 각 expert e 는 prototype w_e (= mode center mu_e).
- 토큰 스트림: step 마다 B=32 토큰, 잠재 mode m ~ pi_t (drifting Zipf-유사 혼합).
- 라우팅: top-1 = argmax x·w ; 용량 없으면 top-2 로 spillover ; 둘 다 없으면 DROP.
- ORGANELLE: 각 expert 옆에 호흡용량 c_e (organelle 질량). SUM(c_e) = C = 고정 (보존).
  c_e = 그 step 에 e 가 서비스할 수 있는 최대 work (1 토큰 = 1 work unit).
  C = 0.6 * B  => 수요의 60% 만 감당 = 용량이 항상 BINDING (희소).

ARM (전부 동일 예산: 동일 총용량 C · 동일 epoch 수 · 동일 스트림(paired))
--------------------------------------------------------------------------
  EXP    수요주도 biogenesis: EMA(관측 demand) 에 비례해 organelle 재할당.
  c1     균일 할당: c_e = C/E 고정 (동일 C, 동역학 없음 = null mechanism).
  c2     랜덤 할당(동량): 매 epoch 랜덤 target 으로 재할당하되 **이동질량을 EXP 와 정확히 일치**시킴.
  c3     shuffled-load(동량): EXP 와 동일 규칙·동일 이동질량이나 load 벡터를 permute
         => 할당 동역학·통계는 동일, load<->expert 대응만 파괴. (가장 강한 control)
  ORACLE 상한 참조(control 아님): 다음 epoch 의 실제 demand 를 미리 보고 할당(lookahead).

>=2 control (c1,c2,c3) 모두 EXP 와 동일한 총용량 C 를 가지며 c2/c3 는 이동질량까지 동일.
EXP 가 추가로 쓰는 것은 오직 *load 신호* 뿐 (파라미터/예산 우위 없음).

측정 (측정 메타법칙: FORM tunable · BIND earned · 신호 = Δ vs >=2 controls)
---------------------------------------------------------------------------
  throughput  = served_work / demanded_work            <- BIND (earned)  [주 지표]
  top1_hit    = top-1 로 서비스된 비율                  <- BIND
  purity      = expert 별 served mass 의 max mode-share <- 특화도 (earned)
  gini(c)     = 용량 분포 Gini                          <- FORM (tunable · random 도 올림)
  corr(c,dem) = 용량-수요 상관                          <- 진단용

사전등록 판정 규칙 (실행 전 고정 · tune-to-green 금지)
------------------------------------------------------
  PRIMARY CELL = drift half-life h=400 (카드의 "지속 고부하" 전제에 충실한 조건).
  PASS(DIRECTIONAL-POSITIVE):
      seed-paired Δthroughput = EXP − max(c1,c2,c3) 의 mean > +0.01 (1%p)
      AND 전 seed 에서 Δ > 0.
  THEATER: |Δ vs 균일(c1)| < 0.01  (부하 신호가 유용 할당을 못 알림)
  KILL:    Δ < −0.01 (수요주도가 균일보다 나쁨)
  ARTIFACT-GUARD: NULL-ENV(균일 수요, 특화할 것이 없음)에서 EXP 가 control 을 이기면
      측정이 게임된 것 => INVALID.
  toy 이므로 최대 등급은 DIRECTIONAL (a_toy_scale_recheck).

SWEEP(2차 특성화 · 판정에 사용 안 함): drift half-life h ∈ {25,100,400,1600,static}.
"""
import json
import os
import time

import numpy as np

# ---------------------------------------------------------------- 고정 하이퍼 (실행 전 확정)
E = 16          # expert / organelle 수
K = 16          # 잠재 mode 수
D = 32          # 차원
B = 32          # step 당 토큰
N_STEPS = 1500  # step 수
TOK_SIGMA = 0.8
SCARCITY = 0.6  # C = SCARCITY * B  => 용량 binding
EPOCH = 25      # 재할당 주기
ETA = 0.35      # 재할당 step size
EMA_HL = 50     # load EMA half-life (steps)
FLOOR_FRAC = 0.05   # organelle 최소 질량 (사멸 방지)
WARMUP_FRAC = 0.2   # 앞 20% 는 측정 제외
SEEDS = [0, 1, 2, 3, 4]
PRIMARY_H = 400
SWEEP_H = [25, 100, 400, 1600, "static"]

C_TOTAL = SCARCITY * B
FLOOR = FLOOR_FRAC * C_TOTAL / E
FREE = C_TOTAL - E * FLOOR
EMA_A = 1.0 - 0.5 ** (1.0 / EMA_HL)

ARMS = ["EXP", "c1_uniform", "c2_random", "c3_shuffled", "ORACLE"]
CONTROLS = ["c1_uniform", "c2_random", "c3_shuffled"]


# ---------------------------------------------------------------- 스트림 (arm 무관 · paired)
def make_stream(seed, half_life, null_env=False):
    """(top1, top2, mode) [N_STEPS,B] + demand_true [N_STEPS,E] 를 생성. arm 간 완전 공유."""
    rng = np.random.default_rng(1000 + seed)
    mu = rng.normal(size=(K, D))
    mu /= np.linalg.norm(mu, axis=1, keepdims=True)
    W = mu.copy()  # expert e prototype = mode e center (1:1 기질)

    if null_env:
        pis = np.full((N_STEPS, K), 1.0 / K)
    else:
        if half_life == "static":
            rho = 1.0
        else:
            rho = 0.5 ** (1.0 / float(half_life))
        z = rng.normal(size=K)
        pis = np.empty((N_STEPS, K))
        for t in range(N_STEPS):
            if half_life != "static":
                z = rho * z + np.sqrt(max(1e-9, 1 - rho ** 2)) * rng.normal(size=K)
            lg = 1.6 * z
            lg -= lg.max()
            p = np.exp(lg)
            pis[t] = p / p.sum()

    top1 = np.empty((N_STEPS, B), dtype=np.int32)
    top2 = np.empty((N_STEPS, B), dtype=np.int32)
    modes = np.empty((N_STEPS, B), dtype=np.int32)
    for t in range(N_STEPS):
        m = rng.choice(K, size=B, p=pis[t])
        x = mu[m] + TOK_SIGMA * rng.normal(size=(B, D))
        s = x @ W.T                       # [B,E]
        idx = np.argpartition(-s, 1, axis=1)[:, :2]
        a = idx[np.arange(B), np.argmax(s[np.arange(B)[:, None], idx], axis=1)]
        b = idx[np.arange(B), np.argmin(s[np.arange(B)[:, None], idx], axis=1)]
        top1[t], top2[t], modes[t] = a, b, m

    # true demand (top1 요청 수) per step
    dem = np.zeros((N_STEPS, E))
    for t in range(N_STEPS):
        np.add.at(dem[t], top1[t], 1.0)
    return top1, top2, modes, dem


# ---------------------------------------------------------------- 할당 헬퍼
def target_from_weights(w):
    w = np.maximum(w, 0.0)
    s = w.sum()
    w = np.full(E, 1.0 / E) if s <= 1e-12 else w / s
    return FLOOR + FREE * w


def moved_mass(c_old, c_new):
    return 0.5 * np.abs(c_new - c_old).sum()


def apply_matched(c, target, mass_budget):
    """target 방향으로 이동하되 이동질량을 mass_budget 에 정확히 맞춘다 (동량 보장)."""
    full = target - c
    mm = 0.5 * np.abs(full).sum()
    if mm <= 1e-12 or mass_budget <= 1e-12:
        return c.copy()
    step = min(1.0, mass_budget / mm)
    return c + step * full


def gini(v):
    v = np.sort(np.maximum(v, 0.0))
    n = len(v)
    s = v.sum()
    if s <= 0:
        return 0.0
    idx = np.arange(1, n + 1)
    return float((2.0 * (idx * v).sum()) / (n * s) - (n + 1.0) / n)


# ---------------------------------------------------------------- 한 arm 시뮬
def run_arm(arm, stream, seed):
    top1, top2, modes, dem = stream
    rng = np.random.default_rng(90000 + 7 * seed + ARMS.index(arm))

    c = np.full(E, C_TOTAL / E)
    ema = np.zeros(E)
    warm = int(WARMUP_FRAC * N_STEPS)

    served = 0.0
    demanded = 0.0
    served_top1 = 0.0
    S = np.zeros((E, K))           # served mass by (expert, true mode)
    gini_acc, corr_acc, nacc = 0.0, 0.0, 0

    # EXP 가 매 epoch 실제로 옮긴 질량을 기록 -> c2/c3 에 동일 예산 강제
    exp_masses = getattr(run_arm, "_exp_masses", None)

    my_masses = []
    for t in range(N_STEPS):
        # ---- 재할당(biogenesis) : epoch 경계, warmup 포함 전체
        if t > 0 and t % EPOCH == 0:
            ep = t // EPOCH - 1
            if arm == "EXP":
                tgt = target_from_weights(ema)
                c_new = c + ETA * (tgt - c)
                m = moved_mass(c, c_new)
                my_masses.append(m)
                c = c_new
            elif arm == "c1_uniform":
                c = np.full(E, C_TOTAL / E)   # 동일 총용량 C, 동역학 없음
            elif arm == "c2_random":
                w = rng.dirichlet(np.ones(E))
                tgt = target_from_weights(w)
                budget = exp_masses[ep] if (exp_masses is not None and ep < len(exp_masses)) else 0.0
                c = apply_matched(c, tgt, budget)
            elif arm == "c3_shuffled":
                perm = rng.permutation(E)
                tgt = target_from_weights(ema[perm])
                budget = exp_masses[ep] if (exp_masses is not None and ep < len(exp_masses)) else 0.0
                c = apply_matched(c, tgt, budget)
            elif arm == "ORACLE":
                fut = dem[t:t + EPOCH].sum(axis=0)   # lookahead (상한 참조)
                tgt = target_from_weights(fut)
                c = c + ETA * (tgt - c)
            c = np.maximum(c, FLOOR)
            c *= C_TOTAL / c.sum()                   # 총량 보존 (모든 arm 동일 C)

        # ---- 서비스 (표현형성 단계: 용량 있는 유닛만 발화)
        rem = c.copy()
        a1, a2, mm = top1[t], top2[t], modes[t]
        step_served = 0.0
        step_s1 = 0.0
        for i in range(B):
            e1 = a1[i]
            need = 1.0
            g = rem[e1] if rem[e1] < need else need
            if g > 0.0:
                rem[e1] -= g
                need -= g
                step_served += g
                step_s1 += g
                if t >= warm:
                    S[e1, mm[i]] += g
            if need > 1e-9:
                e2 = a2[i]
                g2 = rem[e2] if rem[e2] < need else need
                if g2 > 0.0:
                    rem[e2] -= g2
                    step_served += g2
                    if t >= warm:
                        S[e2, mm[i]] += g2

        # ---- 관측 신호: demand EMA (요청량 = 미충족분 포함 · 관측가능)
        d = dem[t]
        ema += EMA_A * (d - ema)

        if t >= warm:
            served += step_served
            served_top1 += step_s1
            demanded += float(B)
            gini_acc += gini(c)
            dn, cn = d - d.mean(), c - c.mean()
            den = np.linalg.norm(dn) * np.linalg.norm(cn)
            corr_acc += float(dn @ cn / den) if den > 1e-9 else 0.0
            nacc += 1

    if arm == "EXP":
        run_arm._exp_masses = my_masses

    tot = S.sum()
    purity = float(S.max(axis=1).sum() / tot) if tot > 0 else 0.0
    return dict(
        throughput=served / demanded,
        top1_hit=served_top1 / demanded,
        purity=purity,
        gini=gini_acc / nacc,
        corr_cap_demand=corr_acc / nacc,
        moved_mass_total=float(np.sum(my_masses)) if arm == "EXP" else None,
    )


def run_cell(half_life, null_env=False):
    out = {a: {k: [] for k in ("throughput", "top1_hit", "purity", "gini", "corr_cap_demand")}
           for a in ARMS}
    per_seed_delta = []
    for seed in SEEDS:
        stream = make_stream(seed, half_life, null_env=null_env)
        if hasattr(run_arm, "_exp_masses"):
            del run_arm._exp_masses
        res = {}
        for arm in ARMS:                  # EXP 먼저 -> 이동질량 예산이 c2/c3 로 전달
            r = run_arm(arm, stream, seed)
            res[arm] = r
            for k in out[arm]:
                out[arm][k].append(r[k])
        best_ctrl = max(res[c]["throughput"] for c in CONTROLS)
        per_seed_delta.append(res["EXP"]["throughput"] - best_ctrl)

    def ms(v):
        return [float(np.mean(v)), float(np.std(v))]

    summ = {a: {k: ms(v) for k, v in out[a].items()} for a in ARMS}
    summ["_delta_vs_best_control"] = ms(per_seed_delta)
    summ["_delta_per_seed"] = [float(x) for x in per_seed_delta]
    summ["_delta_vs_c1_uniform"] = ms(
        [e - c for e, c in zip(out["EXP"]["throughput"], out["c1_uniform"]["throughput"])])
    summ["_delta_purity_vs_best_control"] = ms([
        out["EXP"]["purity"][i] - max(out[c]["purity"][i] for c in CONTROLS)
        for i in range(len(SEEDS))])
    return summ


def main():
    t0 = time.time()
    result = {
        "hypothesis": "H_9282",
        "family": "F10",
        "config": dict(E=E, K=K, D=D, B=B, N_STEPS=N_STEPS, seeds=SEEDS, scarcity=SCARCITY,
                       C_total=C_TOTAL, epoch=EPOCH, eta=ETA, ema_half_life=EMA_HL,
                       floor=FLOOR, warmup_frac=WARMUP_FRAC, tok_sigma=TOK_SIGMA,
                       primary_h=PRIMARY_H),
        "prereg": dict(pass_rule="mean(delta_thr vs best control) > +0.01 AND all seeds > 0",
                       theater_rule="|delta vs c1_uniform| < 0.01",
                       kill_rule="delta < -0.01",
                       artifact_guard="NULL-ENV 에서 EXP > controls 이면 INVALID",
                       max_tier="DIRECTIONAL (toy)"),
        "cells": {},
    }
    result["cells"][f"primary_h{PRIMARY_H}"] = run_cell(PRIMARY_H)
    for h in SWEEP_H:
        key = f"sweep_h{h}"
        if h == PRIMARY_H:
            continue
        result["cells"][key] = run_cell(h)
    result["cells"]["null_env_uniform_demand"] = run_cell(PRIMARY_H, null_env=True)
    result["wall_sec"] = round(time.time() - t0, 2)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "result.json"), "w") as f:
        json.dump(result, f, indent=2)

    # ---- 콘솔 요약
    for cell, s in result["cells"].items():
        print(f"\n=== {cell} ===")
        for a in ARMS:
            m, sd = s[a]["throughput"]
            pm, psd = s[a]["purity"]
            gm, _ = s[a]["gini"]
            cm, _ = s[a]["corr_cap_demand"]
            print(f"  {a:12s} thr={m:.4f}±{sd:.4f}  purity={pm:.4f}±{psd:.4f} "
                  f"gini={gm:.3f} corr={cm:+.3f}")
        d, ds = s["_delta_vs_best_control"]
        d1, d1s = s["_delta_vs_c1_uniform"]
        dp, dps = s["_delta_purity_vs_best_control"]
        print(f"  Δthr vs best-control = {d:+.4f}±{ds:.4f}  (per-seed {s['_delta_per_seed']})")
        print(f"  Δthr vs c1_uniform   = {d1:+.4f}±{d1s:.4f}")
        print(f"  Δpurity vs best-ctrl = {dp:+.4f}±{dps:.4f}")
    print(f"\nwall={result['wall_sec']}s -> result.json")


if __name__ == "__main__":
    main()
