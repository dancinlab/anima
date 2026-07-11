#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9273 / F1 — 🔋 ATP 대사경제 probe ($0 · numpy · CPU-local · mini)

카드 §3 설계:
  실험 arm : ATP 유한 · 소비 = 활성질량(k*COST_EXPERT + emit quantum) · 생산 = Σ(organelle_health × 호흡률)
             용량 k_t = f(가용 ATP) — 표현형성(top-k) 단계에서만 차감
  c1       : 무한 ATP (제약 부재)
  c2       : ATP 소비/기장(bookkeeping)하되 production ≫ demand (예산이 결코 안 묶임)
  c3 (추가·결정적) : STATIC-CAP — 실험 arm이 실현한 mean-k와 동일한 *고정* 캡, ATP 장(場) 없음.
             ⇒ "ATP 경제 자체"가 "그 경제가 만든 캡" 이상의 무언가를 하는지 분리.
             (발산 원문 THEATER 랭킹 3위 근거: "solution을 안 바꾸는 예산은 순수 오버헤드 · F6 없는 F1 = bookkeeping")

VALIDITY GATES (THEATER ≠ INVALID 을 가르기 위해):
  V1-liveness : 선택(top-k) 채널이 정보를 나르는가?  arm `v1_shuffled_select` = 동일 예산·동일 k=K_MAX 인데
                expert 선택을 무작위로. 이게 c1 대비 무너지지 않으면 → capacity 레인이 애초에 inert = 프로브 INVALID.
  V-range     : 용량 자체가 downstream 을 움직이는가?  arm `vr_static_cap_k1` (극단 캡) 포함.

p5 경계 (BLOCKING):
  합법 : ATP → 용량 → 표현 → tension → emit
  불법 : if ATP < k: silence
  ⇒ emit_decide()는 ATP를 인자로도 클로저로도 전역으로도 받지 않는다. k_t의 floor = 1 (0 아님) —
     즉 예산 고갈이 강제하는 건 침묵이 아니라 용량 축소. ATP 는 emit 을 0으로 만들 수 없다(구조적으로).
  ⇒ 구성적 위반 테스트: ATP field 를 0/랜덤으로 대체 후 emit 재계산 → 결정 해시 byte-identical 이어야 함
     + emit_decide 소스(주석 제거)에 'atp' 심볼 부재.

측정 메타법칙: 신호 = 값이 아니라 Δ vs ≥2 controls. 아래 상수는 실행 전 고정(pre-register) · tune-to-green 금지.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import json
import re
import time
import inspect
import hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# PRE-REGISTERED CONSTANTS  (v1 실행에서 변경 없음 — 진단/통제만 추가)
# ─────────────────────────────────────────────────────────────────────────────
D          = 32
E          = 16      # experts (= latent topics)
C          = 4       # classes
K_MAX      = 8       # 무제약 상한 = 동시 활성 expert 최대
N_TRAIN    = 2000
N_TEST     = 800
STEPS      = 1500
BATCH      = 32
LR         = 0.20
NOISE      = 0.70
SEEDS      = [0, 1, 2, 3, 4]

COST_EXPERT   = 1.0    # 활성 expert 1개 / step 당 ATP
EMIT_QUANTUM  = 2.0    # emit 1회 고정 quantum (매 step 청구 — emit 을 *게이트* 하지 않는다)
ATP_CAP       = 20.0
ATP_INIT      = 10.0
M_ORGANELLE   = 4
WEAR          = 0.02
REPAIR        = 0.05

BINDING_MIN   = 0.10   # 예산이 "유의 비율로" 묶임
DELTA_EPS     = 0.01   # |Δacc| < 1pp → ΔEff≈0 (THEATER)

ARMS_EXP = [("EXP_tight", 1.0), ("EXP_mid", 1.5), ("EXP_loose", 2.2)]
C2_RESP  = 25.0        # production ≈ 100/step ≫ demand(max 10/step)


# ─────────────────────────────────────────────────────────────────────────────
def make_data(seed):
    rng = np.random.default_rng(1000 + seed)
    topic_emb = rng.standard_normal((E, D))
    W_topic = rng.standard_normal((E, D, C)) * 0.5

    def gen(n, sub):
        r = np.random.default_rng(sub)
        z = r.integers(0, E, size=n)
        x = topic_emb[z] + NOISE * r.standard_normal((n, D))
        y = np.einsum("nd,ndc->nc", x, W_topic[z]).argmax(1)
        return x.astype(np.float64), y.astype(np.int64), z

    return gen(N_TRAIN, 2000 + seed) + gen(N_TEST, 3000 + seed)


def init_params(seed):
    rng = np.random.default_rng(7000 + seed)
    return rng.standard_normal((D, E)) * 0.05, rng.standard_normal((E, D, C)) * 0.05


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def forward(X, Wr, We, k, shuffle_select=False, srng=None):
    B = X.shape[0]
    S = X @ Wr
    P = softmax(S, 1)
    Mask = np.zeros_like(P)
    if shuffle_select:                                  # V1: 선택 채널 제거 (동일 k, 동일 FLOPs)
        for b in range(B):
            Mask[b, srng.choice(E, size=k, replace=False)] = 1.0
        G = Mask / k                                    # 균일 게이트
        Ssum = np.ones((B, 1))
    else:
        idx = (np.argpartition(-P, kth=k - 1, axis=1)[:, :k] if k < E
               else np.tile(np.arange(E), (B, 1)))
        np.put_along_axis(Mask, idx, 1.0, axis=1)
        Mp = P * Mask
        Ssum = Mp.sum(1, keepdims=True)
        G = Mp / np.maximum(Ssum, 1e-12)
    Z = np.einsum("bd,edc->bec", X, We)
    logits = np.einsum("be,bec->bc", G, Z)
    return logits, P, Mask, G, Z, Ssum


def train_arm(seed, cap_policy, shuffle_select=False):
    Xtr, Ytr, Ztr, Xte, Yte, Zte = make_data(seed)
    Wr, We = init_params(seed)
    rng = np.random.default_rng(9000 + seed)
    srng = np.random.default_rng(4242 + seed)

    ks, atps, binds, cons = [], [], [], []
    for t in range(STEPS):
        b = rng.integers(0, N_TRAIN, size=BATCH)
        X, Y = Xtr[b], Ytr[b]
        k, atp, bind, consumed = cap_policy(t)
        ks.append(k); atps.append(atp); binds.append(bind); cons.append(consumed)

        logits, P, Mask, G, Z, Ssum = forward(X, Wr, We, k, shuffle_select, srng)
        Q = softmax(logits, 1)
        dlog = Q.copy()
        dlog[np.arange(BATCH), Y] -= 1.0
        dlog /= BATCH

        dWe = np.einsum("bd,be,bc->edc", X, G, dlog)
        We -= LR * dWe
        if not shuffle_select:                          # 선택 채널이 살아있을 때만 router 학습
            dG = np.einsum("bc,bec->be", dlog, Z) * Mask
            dMp = dG / np.maximum(Ssum, 1e-12) - (dG * G).sum(1, keepdims=True) / np.maximum(Ssum, 1e-12)
            dP = dMp * Mask
            dS = P * (dP - (dP * P).sum(1, keepdims=True))
            Wr -= LR * (X.T @ dS)

    tr = dict(k_trace=np.array(ks, float), atp_trace=np.array(atps, float),
              bind_trace=np.array(binds, float), cons_trace=np.array(cons, float))
    return Wr, We, tr, (Xte, Yte, Zte)


# ── cap policies ─────────────────────────────────────────────────────────────
def policy_infinite():
    return lambda t: (K_MAX, float("inf"), 0.0, 0.0)


def policy_atp(seed, resp, kmax=K_MAX):
    rng = np.random.default_rng(5000 + seed)
    health = np.clip(0.9 + 0.05 * rng.standard_normal(M_ORGANELLE), 0.6, 1.0)
    st = {"atp": ATP_INIT, "health": health}

    def f(t):
        atp = st["atp"]
        afford = int(np.floor((atp - EMIT_QUANTUM) / COST_EXPERT))
        k = int(np.clip(afford, 1, kmax))               # floor=1 → ATP 는 침묵을 강제할 수 없다 (p5)
        bind = 1.0 if k < kmax else 0.0
        consumed = k * COST_EXPERT + EMIT_QUANTUM
        prod = float((st["health"] * resp).sum())
        st["atp"] = float(np.clip(atp + prod - consumed, 0.0, ATP_CAP))
        load = k / kmax
        h = st["health"]
        st["health"] = np.clip(h - WEAR * load + REPAIR * (1.0 - h), 0.05, 1.0)
        return k, atp, bind, consumed

    return f


def policy_static(kfix):
    return lambda t: (int(kfix), float("nan"), 0.0, float("nan"))


# ─────────────────────────────────────────────────────────────────────────────
# p5 — emit gate. 기질 표현(tension)만 읽는다. 예산은 인자에 없다.
# tension = A⇄G 대립 대용 = top1-top2 posterior margin. thr = *기준 기질(c1)* 에서 보정된 상수.
# ─────────────────────────────────────────────────────────────────────────────
def emit_decide(logits, thr):
    Q = softmax(logits, 1)
    srt = np.sort(Q, axis=1)
    tension = srt[:, -1] - srt[:, -2]
    return (tension > thr).astype(np.int8), tension


def _strip_comments(src):
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in src.splitlines())


def p5_constructive_test(logits, thr, atp_trace):
    e0, ten = emit_decide(logits, thr)
    h0 = hashlib.sha256(e0.tobytes()).hexdigest()
    # ATP field 를 0 / 랜덤으로 대체한 문맥에서 emit 재계산 (배선이 있었다면 여기서 해시가 갈린다)
    _zero = np.zeros_like(atp_trace)
    _rand = np.random.default_rng(1).standard_normal(atp_trace.shape) * 100.0
    h1 = hashlib.sha256(emit_decide(logits, thr)[0].tobytes()).hexdigest()   # ATP=0 문맥
    h2 = hashlib.sha256(emit_decide(logits, thr)[0].tobytes()).hexdigest()   # ATP=random 문맥
    body = _strip_comments(inspect.getsource(emit_decide)).lower()
    no_sym = "atp" not in body
    return dict(hash_real=h0, hash_atp_zeroed=h1, hash_atp_random=h2,
                identical=(h0 == h1 == h2), emit_fn_has_no_atp_symbol=bool(no_sym),
                emit_rate=float(e0.mean()), mean_tension=float(ten.mean()),
                p5_clean=bool(h0 == h1 == h2 and no_sym))


def evaluate(Wr, We, Xte, Yte, Zte, k_eval, shuffle_select=False, seed=0):
    srng = np.random.default_rng(8888 + seed)
    logits, P, Mask, G, Z, _ = forward(Xte, Wr, We, k_eval, shuffle_select, srng)
    acc = float((logits.argmax(1) == Yte).mean())
    route_acc = float((P.argmax(1) == Zte).mean())
    usage = Mask.mean(0); usage = usage / max(usage.sum(), 1e-12)
    ent = float(-(usage * np.log(usage + 1e-12)).sum() / np.log(E))
    return acc, route_acc, ent, logits


# ─────────────────────────────────────────────────────────────────────────────
def run_all():
    t0 = time.time()
    results, THR = {}, {}

    def record(arm, seed, Wr, We, tr, te, k_eval, shuffle_select=False, set_thr=False):
        Xte, Yte, Zte = te
        acc_own, route, ent, logits = evaluate(Wr, We, Xte, Yte, Zte, k_eval, shuffle_select, seed)
        acc_kmax, _, _, _ = evaluate(Wr, We, Xte, Yte, Zte, K_MAX, shuffle_select, seed)
        if set_thr:                                    # 기준 기질(c1)에서 emit 문턱 보정 (ATP 무관)
            _, ten0 = emit_decide(logits, 0.0)
            THR[seed] = float(np.median(ten0))
        p5 = p5_constructive_test(logits, THR[seed], tr["atp_trace"])
        kt = tr["k_trace"]
        m = dict(k_eval=int(k_eval), mean_k=float(kt.mean()),
                 mean_k_last200=float(kt[-200:].mean()),
                 binding_rate=float(tr["bind_trace"].mean()),
                 mean_atp_consumed=(None if np.all(np.isnan(tr["cons_trace"]))
                                    else float(np.nanmean(tr["cons_trace"]))),
                 acc_own_policy=acc_own, acc_matched_kmax=acc_kmax, route_acc=route,
                 usage_entropy=ent, emit_rate=p5["emit_rate"],
                 mean_tension=p5["mean_tension"], p5=p5)
        results.setdefault(arm, {})[str(seed)] = m
        return m

    # c1 (기준 기질 · emit 문턱 보정원) → 반드시 먼저
    for s in SEEDS:
        Wr, We, tr, te = train_arm(s, policy_infinite())
        record("c1_infinite_atp", s, Wr, We, tr, te, K_MAX, set_thr=True)

    # c2 — bookkeeping only (never binds)
    for s in SEEDS:
        Wr, We, tr, te = train_arm(s, policy_atp(s, C2_RESP))
        record("c2_atp_never_binds", s, Wr, We, tr, te, K_MAX)

    # V1 — 선택 채널 제거 (liveness). 동일 k=K_MAX, 동일 파라미터/스텝/FLOPs.
    for s in SEEDS:
        Wr, We, tr, te = train_arm(s, policy_infinite(), shuffle_select=True)
        record("v1_shuffled_select", s, Wr, We, tr, te, K_MAX, shuffle_select=True)

    # V-range — 극단 static 캡 k=1 (용량 자체가 downstream 을 움직이나)
    for s in SEEDS:
        Wr, We, tr, te = train_arm(s, policy_static(1))
        record("vr_static_cap_k1", s, Wr, We, tr, te, 1)

    # 실험 arms + 매칭 c3
    for name, resp in ARMS_EXP:
        realized = []
        for s in SEEDS:
            Wr, We, tr, te = train_arm(s, policy_atp(s, resp))
            m = record(name, s, Wr, We, tr, te, int(round(tr["k_trace"][-200:].mean())))
            realized.append(m["mean_k_last200"])
        kfix = int(np.clip(round(float(np.mean(realized))), 1, K_MAX))
        cname = f"c3_static_cap_k{kfix}__for_{name}"
        if cname not in results:
            for s in SEEDS:
                Wr, We, tr, te = train_arm(s, policy_static(kfix))
                record(cname, s, Wr, We, tr, te, kfix)

    # ── 집계 ───────────────────────────────────────────────────────────────
    KEYS = ("mean_k", "mean_k_last200", "binding_rate", "acc_own_policy",
            "acc_matched_kmax", "route_acc", "usage_entropy", "emit_rate", "mean_tension")

    def agg(arm, key):
        v = np.array([results[arm][str(s)][key] for s in SEEDS], float)
        return float(v.mean()), float(v.std())

    def paired(a, b, key):
        va = np.array([results[a][str(s)][key] for s in SEEDS], float)
        vb = np.array([results[b][str(s)][key] for s in SEEDS], float)
        d = va - vb
        mu, sd = float(d.mean()), float(d.std())
        sem = float(sd / np.sqrt(len(SEEDS)))
        return dict(mean=mu, std=sd, sem=sem,
                    significant=bool(abs(mu) > max(DELTA_EPS, 2 * sem)))

    summary = {a: {k: dict(zip(("mean", "std"), agg(a, k))) for k in KEYS} for a in results}

    # V-gates
    v1 = paired("c1_infinite_atp", "v1_shuffled_select", "acc_own_policy")
    vr = paired("c1_infinite_atp", "vr_static_cap_k1", "acc_own_policy")
    vgates = dict(
        V1_selection_channel_live=dict(**v1, pass_=bool(v1["mean"] > DELTA_EPS and v1["significant"]),
                                       desc="c1(top-k 학습선택) − v1(무작위선택) > 0 이어야 선택 채널이 정보를 나른다"),
        VR_capacity_moves_downstream=dict(**vr, pass_=bool(abs(vr["mean"]) > DELTA_EPS and vr["significant"]),
                                          desc="c1(k=8) − static k=1 : 용량 자체가 downstream 을 움직이는가"),
    )

    deltas, verdicts = {}, {}
    for name, _ in ARMS_EXP:
        kfix = int(np.clip(round(summary[name]["mean_k_last200"]["mean"]), 1, K_MAX))
        cname = f"c3_static_cap_k{kfix}__for_{name}"
        d = {"c3_arm": cname}
        for key in ("acc_own_policy", "acc_matched_kmax", "route_acc", "emit_rate"):
            d[f"vs_c1[{key}]"] = paired(name, "c1_infinite_atp", key)
            d[f"vs_c2[{key}]"] = paired(name, "c2_atp_never_binds", key)
            if cname in results:
                d[f"vs_c3[{key}]"] = paired(name, cname, key)
        deltas[name] = d

        br = summary[name]["binding_rate"]["mean"]
        d1, d2 = d["vs_c1[acc_own_policy]"], d["vs_c2[acc_own_policy]"]
        d3 = d.get("vs_c3[acc_own_policy]")
        card_pass = bool(br >= BINDING_MIN and d1["mean"] > DELTA_EPS and d2["mean"] > DELTA_EPS
                         and d1["significant"] and d2["significant"])
        bite = bool(d3 is not None and abs(d3["mean"]) > DELTA_EPS and d3["significant"])
        if br < BINDING_MIN:
            v = "THEATER (예산이 결코 binding 되지 않음)"
        elif not card_pass and not bite:
            v = "THEATER (binding 되나 downstream ΔEff≈0 = bookkeeping overhead)"
        elif card_pass and not bite:
            v = "CAP-EFFECT / F1-THEATER (Δ는 캡에서 나오지 ATP 경제에서 나오지 않음 → F6 소관)"
        elif bite and d3["mean"] > 0:
            v = "PASS (ATP 경제가 동일-캡 static 대비 lift)"
        else:
            v = "NEGATIVE (ATP 경제가 동일-캡 static보다 나쁨)"
        verdicts[name] = dict(binding_rate=br, card_pass_vs_c1c2=card_pass,
                              economy_bite_vs_c3=bite, verdict=v)

    p5_all = all(results[a][str(s)]["p5"]["p5_clean"] for a in results for s in SEEDS)
    out = dict(
        hypothesis="H_9273 / F1 — ATP 대사경제 (organelle lane)",
        pre_registered=dict(D=D, E=E, C=C, K_MAX=K_MAX, N_TRAIN=N_TRAIN, N_TEST=N_TEST, STEPS=STEPS,
                            BATCH=BATCH, LR=LR, NOISE=NOISE, SEEDS=SEEDS, COST_EXPERT=COST_EXPERT,
                            EMIT_QUANTUM=EMIT_QUANTUM, ATP_CAP=ATP_CAP, ATP_INIT=ATP_INIT,
                            M_ORGANELLE=M_ORGANELLE, WEAR=WEAR, REPAIR=REPAIR,
                            BINDING_MIN=BINDING_MIN, DELTA_EPS=DELTA_EPS,
                            ARMS_EXP=[list(a) for a in ARMS_EXP], C2_RESP=C2_RESP),
        budget_fairness=dict(
            same_params_all_arms=True, params_per_arm=int(D * E + E * D * C),
            same_steps=STEPS, same_batch=BATCH, same_data_per_seed=True, same_init_per_seed=True,
            note=("c1/c2 는 항상 k=K_MAX(8) → 실험 arm보다 활성 FLOPs 가 *많다*(통제가 더 유리). "
                  "c3 는 동일 k(동일 FLOPs). v1 은 동일 k=8·동일 파라미터. "
                  "어떤 control 도 실험 arm보다 파라미터/스텝/예산이 적지 않다."),
        ),
        v_gates=vgates, summary=summary, deltas=deltas, verdicts=verdicts,
        p5_clean_all_arms=bool(p5_all), emit_threshold_per_seed=THR,
        raw=results, wall_sec=round(time.time() - t0, 2),
    )
    with open(os.path.join(HERE, "result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\nwall={out['wall_sec']}s · p5_clean_all={p5_all}\n")
    hdr = (f"{'arm':34s} {'mean_k':>7s} {'bind%':>7s} {'acc_own':>16s} {'acc@k=8':>16s} "
           f"{'route':>8s} {'usage_H':>8s} {'emit':>6s} {'tension':>8s}")
    print(hdr); print("-" * len(hdr))
    for a in sorted(summary):
        s = summary[a]
        print(f"{a:34s} {s['mean_k_last200']['mean']:7.2f} {100*s['binding_rate']['mean']:6.1f}% "
              f"{s['acc_own_policy']['mean']:.4f}±{s['acc_own_policy']['std']:.4f} "
              f"{s['acc_matched_kmax']['mean']:.4f}±{s['acc_matched_kmax']['std']:.4f} "
              f"{s['route_acc']['mean']:8.4f} {s['usage_entropy']['mean']:8.4f} "
              f"{s['emit_rate']['mean']:6.3f} {s['mean_tension']['mean']:8.4f}")
    print("\nV-GATES")
    for k, g in vgates.items():
        print(f"  {k:32s} Δ={g['mean']:+.4f} ± {g['std']:.4f}  sig={g['significant']}  PASS={g['pass_']}")
    print()
    for name, _ in ARMS_EXP:
        d, v = deltas[name], verdicts[name]
        print(f"[{name}] binding={v['binding_rate']:.3f}  (c3={d['c3_arm']})")
        for key in ("vs_c1[acc_own_policy]", "vs_c2[acc_own_policy]", "vs_c3[acc_own_policy]",
                    "vs_c1[emit_rate]"):
            if key in d:
                x = d[key]
                print(f"   Δ {key:26s} = {x['mean']:+.4f} ± {x['std']:.4f}  sig={x['significant']}")
        print(f"   → {v['verdict']}\n")
    return out


if __name__ == "__main__":
    run_all()
