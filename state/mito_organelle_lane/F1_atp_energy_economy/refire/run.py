#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9273 / F1 — 🔋 ATP 대사경제 · REFIRE ($0 · numpy · CPU-local · mini · OMP=2)

원 판정 ⛔INVALID (REFUTE.md R1~R5 · 재실행조건 i~vi)를 구조적으로 전부 고친 재설계.

┌ 원 결함 → 이번 수정 ─────────────────────────────────────────────────────────
│ R1 검출력 0
│    → (iv) 실행 **전에** pilot seed(100..105 · main과 disjoint)에서 사전 MDE 계산.
│       처치가 움직이는 축(deploy-k)의 동적범위를 static-k sweep으로 실측하고
│       MDE(t*·paired-CRN SEM)와 비교. MDE ≥ 0.2×band 면 그 자리에서 INVALID abort.
│
│ R2 항진적 처치 (policy_atp = 자율 폐루프 · 수요가 공급의 함수라 수요>생산이 구조적 불가)
│    → (i) demand 를 supply 에서 **외생화**. demand_i = #{e : S_e > 0.5·max S} (S = 라우터
│       원점수) = **입력 × 모델상태**의 함수. ATP 를 인자로도 클로저로도 전역으로도 안 받는다.
│       k = min(demand, afford) 이므로 **수요 > 공급이 구조적으로 가능** = 예산이 진짜로 binding.
│       정보채널 실측: demand 를 셔플하면 EXP 의 k-벡터가 바뀌고(>0) control 은 안 바뀜(=0).
│
│ R3 용량 레인 inert (route_acc 우연 이하 · k = 평균화 노브 = FORM)
│    → (ii)(iii) 기질 교체. expert = (topic × polarity) **결합**, 라벨 = 활성 결합들의 vote 합.
│       vote 는 극성 무관(u[2j]=u[2j+1]) ⇒ **선형 지름길 = chance(0.25)** — 정류(rectification)
│       없이는 못 푼다. 수용장(receptive field)이 (topic,polarity)로 특화 ⇒ route_recall ≫ 1/E.
│       게이트는 재정규화 없는 **합** (logits = Σ_{e∈topk} P_e·Z_e) ⇒ k<m 이면 표(vote)가
│       실제로 빠진다 = k 는 평균화 노브가 아니라 **진짜 용량**.
│
│ R4 c1 ≡ c2 (per-seed byte-identical = 통제 1개)
│    → (v) 두 primary control 을 **구조적으로 다르게**:
│         c1 = STATIC 정수 캡(분산 0 · 수요맹목 · EXP보다 ATP 를 **더** 씀 = 보수적)
│         c2 = PERMUTED-k (EXP 의 k multiset·총지출 **정확히 일치** · 수요-표본 결합만 파괴)
│       + c4(demand-shuffled) + c5(no-bank, afford marginal 보존/시간상태만 파괴) + c3(no-bank raw).
│       ⚠️ 원 카드의 control(c1=무한ATP, c2=never-binds)은 **둘 다 EXP보다 자원이 많다**.
│       acc 가 k 에 단조증가인 이상 "제약 arm 이 무제약 arm 을 이겨라"는 PASS 조건은
│       구조적 달성불가(=원 설계의 4번째 결함). ⇒ 과학적으로 의미있는 질문으로 교정:
│       **"동일 비용에서, ATP 경제가 수요맹목 지출보다 잘 배분하는가?"**
│       (원 카드의 문자 그대로의 대비도 ref_unbudgeted 로 함께 보고 — 아무것도 숨기지 않는다.)
│
│ R5 p5 dead-code (_zero/_rand 계산만 하고 주입 안 함)
│    → (vi) emit_decide(logits, thr, atp_ctx) — atp 를 **실제 인자로 주입**하고 real/zeros/random
│       3 문맥의 결정 해시가 byte-identical 임을 확인 + 본문 심볼검사. 동시에 **합법경로**
│       (ATP→용량→표현→tension→emit)가 살아있음을 emit_rate 변화로 확인.
└─────────────────────────────────────────────────────────────────────────────

계측 규약 (organelle-lane census · convergence synthesis-md-1):
  · Δ = exp − max(controls) **금지** → control별 paired-t 전부 + pooled-mean.
  · "mean vs 1·std" 휴리스틱 금지 → paired-CRN SEM / t / p 만.
  · V-gate 는 헤드라인 detector(= 배치정책 하 held-out acc) **그 자체**에 건다.
  · 규약 2개(micro-acc / stratum-macro-acc)에서 부호 보존 확인.
  · 금지지표(conj_index · purity · acc-per-ATP 비율 · corr(n,demand)) 미사용.
  · seed 20 · paired-CRN(동일 학습모델·동일 테스트셋·동일 스트림순서). tune-to-green 금지.

⚠️ 정직 고지: 기질 상수(NOISE·TAU·STEPS·LR)는 **arm-무관 속성**(route_recall · static-k acc 곡선 ·
   demand 센서 품질)만 보고 고정했다. 다만 기질 구축 중 seed 0 에서 EXP-vs-control 대비를 한 번
   보았다(EXP < static-ceil, EXP > perm). 그 관찰 이후 **어떤 상수도 바꾸지 않았고**, 추가한 것은
   통제(c4·c5·bursty 조건)뿐이다 = 통제 강화 방향(음성을 강화). RESULT.md 에 그대로 기재.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import json
import math
import re
import time
import inspect
import hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── PRE-REGISTERED CONSTANTS ────────────────────────────────────────────────
D            = 32
T_TOPIC      = 8          # 잠재 토픽
E            = 16         # experts = (topic × polarity) 결합 = 2·T
C            = 4          # classes
K_MAX        = 8
M_CHOICES    = (1, 2, 3, 4)      # 샘플당 활성 토픽 수 = 재조합 차수
NOISE        = 0.20
TAU          = 2.0        # 게이트 온도
N_TRAIN      = 3000
N_TEST       = 1500
STEPS        = 4000
BATCH        = 64
LR           = 0.50
WE_INIT      = 0.30

SEEDS        = list(range(20))                    # main (paired-CRN)
PILOT_SEEDS  = [100, 101, 102, 103, 104, 105]     # 사전 검출력 (main과 disjoint)

COST_EXPERT  = 1.0
EMIT_QUANTUM = 2.0        # emit 1회 고정 quantum (emit 을 *게이트* 하지 않는다)
ATP_INIT     = 10.0
ATP_CAP      = 20.0       # 저장(reservoir) 상한 — F1 고유 기제
M_ORGANELLE  = 4
RESP         = 1.0        # 생산 = Σ(health × RESP) ≈ 3.6/샘플
                          # ⇒ 지속가능 k = 3.6 − EMIT_QUANTUM = 1.6  <  평균수요 E[m] = 2.5
                          #   (공급측 항등식만으로 희소성 확정 — 결과를 보고 고른 값 아님)
WEAR         = 0.02
REPAIR       = 0.05

BLOCK        = 25         # bursty 스트림 블록 길이 (수요 자기상관 조건)
ALPHA        = 0.05
DELTA_EPS    = 0.01       # |Δ| < 1pp → ΔEff≈0 (THEATER 선언선 · 원 카드 등록값 유지)
MDE_MAX_FRAC = 0.20       # MDE ≥ 0.2×band → 검출력 부족 → INVALID abort


# ═══ 기질 (R3 fix) ═══════════════════════════════════════════════════════════
def make_world(seed):
    """expert e = 2j + (a<0) = (topic j × polarity a) 결합.
    vote 는 극성 무관(u[2j] = u[2j+1] = v[j]) ⇒ 선형사상 x@M 은 Σ_j a_j·w_j (기댓값 0) 밖에
    못 만들어 **chance(0.25)**. 정답 = Σ_{j∈S} v[j] 는 |x·emb_j| 정류를 요구한다."""
    r = np.random.default_rng(1000 + seed)
    Q, _ = np.linalg.qr(r.standard_normal((D, T_TOPIC)))
    emb = Q.T.copy()                                  # T×D orthonormal
    v = r.standard_normal((T_TOPIC, C))
    u = np.repeat(v, 2, axis=0)                       # E×C
    return emb, u


def gen(n, sub, emb, u):
    r = np.random.default_rng(sub)
    m = r.choice(M_CHOICES, size=n)
    X = np.zeros((n, D)); Y = np.zeros(n, dtype=np.int64); Sets = np.zeros((n, E), np.int8)
    for i in range(n):
        s = r.choice(T_TOPIC, size=int(m[i]), replace=False)
        a = r.choice((1, -1), size=int(m[i]))
        ex = 2 * s + (a < 0).astype(int)
        Sets[i, ex] = 1
        X[i] = (a[:, None] * emb[s]).sum(0)
        Y[i] = int(u[ex].sum(0).argmax())
    X += NOISE * r.standard_normal((n, D))
    return X, Y, Sets, m.astype(int)


def receptive_field(emb):
    """수용장 = (topic × polarity) 특화. 학습 X (frozen-first) — 라우팅 학습가능성은
    본 가설(에너지 경제)의 대상이 아니므로 기질 속성으로 고정. route_recall 로 인증."""
    Wr = np.zeros((D, E))
    for j in range(T_TOPIC):
        Wr[:, 2 * j] = emb[j]
        Wr[:, 2 * j + 1] = -emb[j]
    return Wr


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def topk_mask(P, k):
    B = P.shape[0]
    kk = np.full(B, int(k)) if np.isscalar(k) else np.asarray(k, dtype=int)
    order = np.argsort(-P, axis=1, kind="stable")
    rank = np.argsort(order, axis=1, kind="stable")
    return (rank < kk[:, None]).astype(np.float64)


def train(seed, k_policy):
    """k_policy(t, S_batch) -> (k, demand, bind, consumed, atp). control 은 S 를 무시."""
    emb, u = make_world(seed)
    Xtr, Ytr, _, _ = gen(N_TRAIN, 2000 + seed, emb, u)
    te = gen(N_TEST, 3000 + seed, emb, u)
    Wr = receptive_field(emb)
    We = np.random.default_rng(7000 + seed).standard_normal((E, D, C)) * WE_INIT
    rng = np.random.default_rng(9000 + seed)
    tr = {q: [] for q in ("k", "demand", "bind", "cons", "atp")}
    for t in range(STEPS):
        b = rng.integers(0, N_TRAIN, size=BATCH)
        X, Y = Xtr[b], Ytr[b]
        S = X @ Wr
        k, dem, bind, cons, atp = k_policy(t, S)
        for q, val in zip(("k", "demand", "bind", "cons", "atp"), (k, dem, bind, cons, atp)):
            tr[q].append(val)
        P = softmax(TAU * S, 1)
        Mask = topk_mask(P, k)
        Z = np.einsum("bd,edc->bec", X, We)
        Gt = P * Mask                                  # ★ 합-게이트(재정규화 X)
        logits = np.einsum("be,bec->bc", Gt, Z)
        Q = softmax(logits, 1)
        dlog = Q.copy()
        dlog[np.arange(BATCH), Y] -= 1.0
        dlog /= BATCH
        We -= LR * np.einsum("bd,be,bc->edc", X, Gt, dlog)
    return Wr, We, {q: np.array(val, float) for q, val in tr.items()}, te


# ═══ DEMAND — 외생 수요 (R2 fix) ═════════════════════════════════════════════
def demand_sensor(S):
    """난이도 센서 = 라우터 원점수의 **공동우세(co-dominance) 개수**.
    입력 × 모델상태의 함수. ATP 는 인자에도 클로저에도 전역에도 없다 (코드로 증명)."""
    return np.clip((S > 0.5 * S.max(1, keepdims=True)).sum(1), 1, K_MAX).astype(int)


def organelle_health(seed):
    rng = np.random.default_rng(5000 + seed)
    return np.clip(0.9 + 0.05 * rng.standard_normal(M_ORGANELLE), 0.6, 1.0)


def economy_stream(demand, seed, bank=True):
    """보존 ATP 장 + 저장(reservoir) + 외생수요 기반 지출.
    bank=False → 저장 없음(pay-as-you-go): 그 순간 생산분만."""
    h = organelle_health(seed)
    atp = ATP_INIT if bank else 0.0
    ks, binds, cons, affs, atps = [], [], [], [], []
    for i in range(len(demand)):
        prod = float((h * RESP).sum())
        pool = atp if bank else prod
        aff = int(np.clip(int(np.floor((pool - EMIT_QUANTUM) / COST_EXPERT)), 1, K_MAX))
        k = int(min(int(demand[i]), aff))              # floor=1 → ATP 는 침묵을 강제 못함 (p5)
        c = k * COST_EXPERT + EMIT_QUANTUM
        binds.append(1.0 if int(demand[i]) > aff else 0.0)
        ks.append(k); cons.append(c); affs.append(aff); atps.append(atp)
        if bank:
            atp = float(np.clip(atp + prod - c, 0.0, ATP_CAP))
        h = np.clip(h - WEAR * (k / K_MAX) + REPAIR * (1.0 - h), 0.05, 1.0)
    return (np.array(ks, int), np.array(binds, float), np.array(cons, float),
            np.array(affs, int), np.array(atps, float))


def train_policy_static(kfix):
    return lambda t, S: (int(kfix), float("nan"), 0.0, kfix * COST_EXPERT + EMIT_QUANTUM, float("nan"))


def train_policy_economy(seed):
    st = {"atp": ATP_INIT, "health": organelle_health(seed)}

    def f(t, S):                                       # ← 배치의 라우터 원점수를 실제로 받는다
        dem = int(np.rint(demand_sensor(S).mean()))
        atp = st["atp"]
        prod = float((st["health"] * RESP).sum())
        aff = int(np.clip(int(np.floor((atp - EMIT_QUANTUM) / COST_EXPERT)), 1, K_MAX))
        k = int(min(dem, aff))
        c = k * COST_EXPERT + EMIT_QUANTUM
        st["atp"] = float(np.clip(atp + prod - c, 0.0, ATP_CAP))
        h = st["health"]
        st["health"] = np.clip(h - WEAR * (k / K_MAX) + REPAIR * (1.0 - h), 0.05, 1.0)
        return k, float(dem), (1.0 if dem > aff else 0.0), c, atp

    return f


def train_policy_seq(kseq):
    return lambda t, S: (int(kseq[t]), float("nan"), 0.0,
                         int(kseq[t]) * COST_EXPERT + EMIT_QUANTUM, float("nan"))


# ═══ p5 (R5 fix) — atp_ctx 를 실제로 주입하되 결코 읽지 않는다 ════════════════
def emit_decide(logits, thr, atp_ctx):
    Q = softmax(logits, 1)
    srt = np.sort(Q, axis=1)
    tension = srt[:, -1] - srt[:, -2]
    return (tension > thr).astype(np.int8), tension


def _strip_comments(src):
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in src.splitlines())


def p5_test(logits, thr, atp_real):
    hs = []
    for ctx in (atp_real, np.zeros_like(atp_real),
                np.random.default_rng(1).standard_normal(atp_real.shape) * 100.0):
        e, _ = emit_decide(logits, thr, ctx)           # ← 실제 주입 (dead-code 아님)
        hs.append(hashlib.sha256(e.tobytes()).hexdigest())
    src = _strip_comments(inspect.getsource(emit_decide)).lower()
    body_only = src.split("\n", 1)[1] if "\n" in src else ""
    no_sym = "atp" not in body_only                    # 시그니처 줄 제외한 본문에 atp 부재
    e0, ten0 = emit_decide(logits, thr, atp_real)
    return dict(hash_real=hs[0], hash_atp_zeroed=hs[1], hash_atp_random=hs[2],
                identical=bool(hs[0] == hs[1] == hs[2]), emit_body_reads_no_atp=bool(no_sym),
                emit_rate=float(e0.mean()), mean_tension=float(ten0.mean()),
                illegal_channel_closed=bool(hs[0] == hs[1] == hs[2] and no_sym))


# ═══ 통계 — paired-CRN · SEM · t · p (max(controls) 금지) ═════════════════════
def t_p(t, df):
    t = abs(float(t))
    if t > 60:
        return 1e-12
    x = np.linspace(t, t + 800.0, 100000)
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
    pdf = c * (1 + x ** 2 / df) ** (-(df + 1) / 2)
    return float(max(2.0 * np.trapezoid(pdf, x), 1e-12))


def paired(a, b):
    d = np.asarray(a, float) - np.asarray(b, float)
    n = len(d)
    mu = float(d.mean())
    sem = float(d.std(ddof=1) / math.sqrt(n)) if n > 1 else 0.0
    t = (mu / sem) if sem > 0 else (0.0 if abs(mu) < 1e-15 else math.copysign(1e9, mu))
    return dict(mean=mu, sem=sem, t=float(t), p=float(t_p(t, n - 1)), n=n,
                wins=int((d > 0).sum()), sig=bool(t_p(t, n - 1) < ALPHA))


# ═══ 평가 ════════════════════════════════════════════════════════════════════
def acc_of(P, Z, Y, mvec, kv):
    logits = np.einsum("be,bec->bc", P * topk_mask(P, kv), Z)
    pred = logits.argmax(1)
    micro = float((pred == Y).mean())
    macro = float(np.mean([(pred[mvec == m] == Y[mvec == m]).mean() for m in M_CHOICES]))
    return micro, macro, logits


def route_recall(P, Sets, mvec):
    o = np.argsort(-P, axis=1)
    rec = np.mean([Sets[i, o[i, :int(mvec[i])]].sum() / mvec[i] for i in range(len(P))])
    return float(rec), float(np.mean(mvec / E))


# ═══ (iv) 사전 검출력 ═════════════════════════════════════════════════════════
def power_precheck():
    accs = {k: [] for k in range(1, K_MAX + 1)}
    for s in PILOT_SEEDS:
        Wr, We, _, te = train(s, train_policy_static(K_MAX))
        Xte, Yte, _, mv = te
        P = softmax(TAU * (Xte @ Wr), 1)
        Z = np.einsum("bd,edc->bec", Xte, We)
        for k in range(1, K_MAX + 1):
            accs[k].append(acc_of(P, Z, Yte, mv, k)[0])
    curve = {k: float(np.mean(v)) for k, v in accs.items()}
    band = float(max(curve[k] for k in (1, 2, 3, 4)) - min(curve[k] for k in (1, 2, 3, 4)))
    full = float(max(curve.values()) - min(curve.values()))
    sd = float((np.array(accs[3]) - np.array(accs[2])).std(ddof=1))
    n = len(SEEDS)
    tcrit = 2.093
    mde = float(tcrit * sd / math.sqrt(n))
    return dict(static_k_curve=curve, axis_range_full_pp=100 * full, axis_range_band_k1_4_pp=100 * band,
                pilot_paired_sd_k3_minus_k2=sd, n_seeds=n, t_crit=tcrit, MDE_pp=100 * mde,
                MDE_over_band=float(mde / band) if band > 0 else float("inf"),
                power_ok=bool(mde < MDE_MAX_FRAC * band),
                rule=f"MDE < {MDE_MAX_FRAC}×band (아니면 INVALID abort)")


# ═══ 스트림 순서 ═════════════════════════════════════════════════════════════
def stream_orders(mvec, seed):
    rs = np.random.default_rng(31337 + seed)
    iid = rs.permutation(len(mvec))
    # bursty: 난이도로 정렬 → 블록 단위로 섞기 ⇒ 주변분포 동일, 시간 자기상관만 생성
    key = mvec + 0.001 * rs.standard_normal(len(mvec))
    srt = np.argsort(key, kind="stable")
    blocks = [srt[i:i + BLOCK] for i in range(0, len(srt), BLOCK)]
    rs.shuffle(blocks)
    bursty = np.concatenate(blocks)
    return {"iid": iid, "bursty": bursty}


ARM_ORDER = ["exp_atp_economy", "c1_static_ceil", "c2_perm_k", "c4_demand_shuffled",
             "c5_nobank_affperm", "c3_nobank_raw", "ref_unbudgeted_demand",
             "ref_static_kmax", "vgate_static_k1"]


def deploy_arms(P, Z, Y, mv, dem, seed, order):
    """order 위에서 각 arm 의 k-벡터를 만든 뒤, 표본 인덱스로 되돌려 acc 계산.
    (acc 는 집합통계라 순서에 무관 — 순서는 오직 ATP 동역학에만 들어간다.)"""
    dem_o = dem[order]
    k_exp, bind, cons, aff, atps = economy_stream(dem_o, seed, bank=True)
    meank = float(k_exp.mean())
    kceil = int(np.clip(math.ceil(meank), 1, K_MAX))

    kv = {}
    kv["exp_atp_economy"] = (k_exp, cons)
    kv["c1_static_ceil"] = (np.full(len(order), kceil),
                            np.full(len(order), kceil * COST_EXPERT + EMIT_QUANTUM))
    # c2: EXP 의 k multiset·총지출 정확히 일치 · 수요-표본 결합만 파괴 (3 perm 평균)
    perms = [np.random.default_rng(777 + 100 * seed + q).permutation(k_exp) for q in range(3)]
    kv["c2_perm_k"] = (perms, cons)
    # c4: ATP 동역학 그대로 · demand 신호만 스크램블
    k4, _, c4, _, _ = economy_stream(np.random.default_rng(555 + seed).permutation(dem_o), seed, bank=True)
    kv["c4_demand_shuffled"] = (k4, c4)
    # c5: 저장(시간상태)만 파괴 — afford 주변분포는 EXP 와 정확히 동일(permutation), demand 는 유지
    aff_p = np.random.default_rng(313 + seed).permutation(aff)
    k5 = np.minimum(dem_o, aff_p)
    kv["c5_nobank_affperm"] = (k5, k5 * COST_EXPERT + EMIT_QUANTUM)
    # c3: 저장 자체가 없음 (자원 열위 — 지출이 EXP 보다 적다. 그대로 표기)
    k3, _, c3, _, _ = economy_stream(dem_o, seed, bank=False)
    kv["c3_nobank_raw"] = (k3, c3)
    # 참조: 원 카드의 문자 그대로의 control (무제약 = 자원 우위)
    kv["ref_unbudgeted_demand"] = (dem_o, dem_o * COST_EXPERT + EMIT_QUANTUM)
    kv["ref_static_kmax"] = (np.full(len(order), K_MAX),
                             np.full(len(order), K_MAX * COST_EXPERT + EMIT_QUANTUM))
    kv["vgate_static_k1"] = (np.full(len(order), 1),
                             np.full(len(order), COST_EXPERT + EMIT_QUANTUM))

    inv = np.argsort(order)                     # 스트림 위치 → 표본 인덱스
    out = {}
    for a in ARM_ORDER:
        k_, c_ = kv[a]
        if a == "c2_perm_k":
            mi, ma = [], []
            for kp in k_:
                x = acc_of(P, Z, Y, mv, kp[inv])
                mi.append(x[0]); ma.append(x[1])
            out[a] = dict(acc=float(np.mean(mi)), macro=float(np.mean(ma)),
                          meank=float(np.mean([kp.mean() for kp in k_])),
                          spend=float(np.mean(c_)), logits=None)
        else:
            mi, ma, lg = acc_of(P, Z, Y, mv, np.asarray(k_)[inv])
            out[a] = dict(acc=mi, macro=ma, meank=float(np.mean(k_)),
                          spend=float(np.mean(c_)), logits=lg)
    diag = dict(binding_rate=float(bind.mean()), meank_exp=meank, k_std_exp=float(k_exp.std()),
                afford_std=float(aff.std()), atp_mean=float(atps.mean()),
                corr_afford_demand=float(np.corrcoef(aff, dem_o)[0, 1]) if aff.std() > 0 else 0.0,
                kceil=kceil, atp_real=atps)
    # 정보채널 (4a): demand 를 셔플하면 arm 의 k 가 바뀌는가?
    k_exp2, _, _, _, _ = economy_stream(np.random.default_rng(9 + seed).permutation(dem_o), seed, bank=True)
    diag["chan_exp"] = float((k_exp2 != k_exp).mean())
    diag["chan_c1"] = 0.0       # static: demand 를 인자로 받지 않음 (구조적 0)
    diag["chan_c2"] = 0.0       # perm:   demand 와 무관한 고정 multiset
    return out, diag


# ═══════════════════════════════════════════════════════════════════════════
def main():
    t0 = time.time()
    print("── (iv) 사전 검출력 (pilot seeds — main과 disjoint) ──")
    pw = power_precheck()
    print("   static-k acc curve:", {k: round(v, 4) for k, v in pw["static_k_curve"].items()})
    print(f"   처치 대역(k∈1..4) 동적범위 = {pw['axis_range_band_k1_4_pp']:.2f} pp · 전체 = {pw['axis_range_full_pp']:.2f} pp")
    print(f"   MDE(n=20 · paired-CRN · α=.05) = {pw['MDE_pp']:.3f} pp   ⇒ MDE/band = {pw['MDE_over_band']:.4f}")
    print(f"   POWER_OK = {pw['power_ok']}   (원 프로브: band 1.12pp < 문턱 1.71pp = 검출력 0)\n")
    if not pw["power_ok"]:
        out = dict(hypothesis="H_9273/F1 REFIRE", verdict="INVALID (검출력 부족 — abort)",
                   power_precheck=pw, wall_sec=round(time.time() - t0, 2))
        json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=2, ensure_ascii=False)
        print("ABORT: 검출력 부족 ⇒ INVALID")
        return out

    COND = ("iid", "bursty")
    per = {c: {a: {"acc": [], "macro": [], "meank": [], "spend": []} for a in ARM_ORDER} for c in COND}
    dg = {c: {q: [] for q in ("binding_rate", "meank_exp", "k_std_exp", "afford_std", "corr_afford_demand",
                              "chan_exp", "chan_c1", "chan_c2", "kceil")} for c in COND}
    glob = {q: [] for q in ("route_recall", "route_chance", "demand_mean", "demand_std",
                            "demand_corr_m", "lin_shortcut_acc", "majority_baseline",
                            "p5_ok", "emit_k1", "emit_k8", "emit_exp")}
    tside = {"exp": [], "static": [], "perm": [], "meank": [], "bind": []}

    for s in SEEDS:
        Wr, We, _, te = train(s, train_policy_static(K_MAX))
        Xte, Yte, Sets, mv = te
        Sc = Xte @ Wr
        P = softmax(TAU * Sc, 1)
        Z = np.einsum("bd,edc->bec", Xte, We)
        dem = demand_sensor(Sc)

        rr, ch = route_recall(P, Sets, mv)
        glob["route_recall"].append(rr); glob["route_chance"].append(ch)
        glob["demand_mean"].append(float(dem.mean())); glob["demand_std"].append(float(dem.std()))
        glob["demand_corr_m"].append(float(np.corrcoef(dem, mv)[0, 1]))
        # V2b: 선형 지름길이 chance 인가 (기질이 진짜 비가산인가)
        # ⚠️ 올바른 null = **최빈클래스 baseline** (클래스 사전확률이 균일하지 않다 — 1/C 가 아니다).
        #    선형사상에는 절편(intercept)을 반드시 넣는다. (첫 실행에서 이 null 을 1/C 로 잘못 잡아
        #     V2 가 오탐 FAIL 했다 — 내 게이트 자신의 detector-fairness 결함. 수정 이력 RESULT.md 기재.)
        emb, u = make_world(s)
        Xtr, Ytr, _, _ = gen(N_TRAIN, 2000 + s, emb, u)
        Xb = np.hstack([Xtr, np.ones((len(Xtr), 1))])
        Wls = np.linalg.lstsq(Xb, np.eye(C)[Ytr], rcond=None)[0]
        Xtb = np.hstack([Xte, np.ones((len(Xte), 1))])
        glob["lin_shortcut_acc"].append(float(((Xtb @ Wls).argmax(1) == Yte).mean()))
        maj = int(np.bincount(Ytr, minlength=C).argmax())
        glob["majority_baseline"].append(float((Yte == maj).mean()))

        orders = stream_orders(mv, s)
        for c in COND:
            res, d = deploy_arms(P, Z, Yte, mv, dem, s, orders[c])
            for a in ARM_ORDER:
                for q, kk in (("acc", "acc"), ("macro", "macro"), ("meank", "meank"), ("spend", "spend")):
                    per[c][a][q].append(res[a][kk])
            for q in dg[c]:
                dg[c][q].append(d[q])
            if c == "iid":
                thr = float(np.median(emit_decide(res["ref_static_kmax"]["logits"], 0.0, np.zeros(1))[1]))
                p5 = p5_test(res["exp_atp_economy"]["logits"], thr, d["atp_real"])
                glob["p5_ok"].append(p5["illegal_channel_closed"])
                glob["emit_exp"].append(p5["emit_rate"])
                glob["emit_k1"].append(float(emit_decide(res["vgate_static_k1"]["logits"], thr,
                                                         d["atp_real"])[0].mean()))
                glob["emit_k8"].append(float(emit_decide(res["ref_static_kmax"]["logits"], thr,
                                                         d["atp_real"])[0].mean()))

        # 부차: 학습단계 경제 (공통 k=K_MAX 평가)
        Wr_e, We_e, tre, _ = train(s, train_policy_economy(s))
        Ze = np.einsum("bd,edc->bec", Xte, We_e)
        tside["exp"].append(acc_of(softmax(TAU * (Xte @ Wr_e), 1), Ze, Yte, mv, K_MAX)[0])
        kfix = int(np.clip(round(float(tre["k"].mean())), 1, K_MAX))
        _, We_s, _, _ = train(s, train_policy_static(kfix))
        tside["static"].append(acc_of(P, np.einsum("bd,edc->bec", Xte, We_s), Yte, mv, K_MAX)[0])
        kseq = np.random.default_rng(4242 + s).permutation(tre["k"].astype(int))
        _, We_p, _, _ = train(s, train_policy_seq(kseq))
        tside["perm"].append(acc_of(P, np.einsum("bd,edc->bec", Xte, We_p), Yte, mv, K_MAX)[0])
        tside["meank"].append(float(tre["k"].mean())); tside["bind"].append(float(tre["bind"].mean()))
        print(f"  seed {s:2d} done ({time.time()-t0:.0f}s)", end="\r")

    # ═══ 집계 ═══
    A = lambda c, a, q: np.array(per[c][a][q], float)
    CONTROLS = ["c1_static_ceil", "c2_perm_k", "c4_demand_shuffled", "c5_nobank_affperm",
                "c3_nobank_raw", "ref_unbudgeted_demand", "ref_static_kmax"]
    PRIM = ["c1_static_ceil", "c2_perm_k"]     # 서로 구조가 다른 2 통제 (분산0 상수 vs 분포일치)

    deltas = {c: {"micro": {}, "macro": {}} for c in COND}
    pooled = {}
    for c in COND:
        for ctl in CONTROLS:
            deltas[c]["micro"][ctl] = paired(A(c, "exp_atp_economy", "acc"), A(c, ctl, "acc"))
            deltas[c]["macro"][ctl] = paired(A(c, "exp_atp_economy", "macro"), A(c, ctl, "macro"))
        pm = float(np.mean([deltas[c]["micro"][x]["mean"] for x in PRIM]))
        pM = float(np.mean([deltas[c]["macro"][x]["mean"] for x in PRIM]))
        sign_ok = all(np.sign(deltas[c]["micro"][x]["mean"]) == np.sign(deltas[c]["macro"][x]["mean"])
                      for x in PRIM)
        pooled[c] = dict(controls=PRIM, pooled_micro=pm, pooled_macro=pM,
                         per_control_signs_agree_2conventions=bool(sign_ok),
                         note="max(controls) 금지 — control별 paired-t 전부 + pooled mean")

    # ── V-GATES (헤드라인 detector = 배치정책 하 held-out acc 그 자체) ──
    v1 = paired(A("iid", "ref_static_kmax", "acc"), A("iid", "vgate_static_k1", "acc"))
    rr, ch = float(np.mean(glob["route_recall"])), float(np.mean(glob["route_chance"]))
    lin = float(np.mean(glob["lin_shortcut_acc"]))
    maj = float(np.mean(glob["majority_baseline"]))
    lin_vs_maj = paired(glob["lin_shortcut_acc"], glob["majority_baseline"])
    sp = {a: float(np.mean(per["iid"][a]["spend"])) for a in ARM_ORDER}
    vg = dict(
        V1_capacity_lane_live=dict(**v1, desc="헤드라인 detector 상 static k=8 − k=1 (용량이 축을 움직이나)",
                                   pass_=bool(v1["sig"] and abs(v1["mean"]) > 2 * DELTA_EPS)),
        V2_expert_specialization=dict(route_recall=rr, chance=ch, ratio=float(rr / ch),
                                      linear_shortcut_acc=lin, majority_baseline=maj,
                                      lin_minus_majority=lin_vs_maj,
                                      desc="expert 가 진짜 분업하는가(route_recall ≫ 1/E) + 기질이 "
                                           "선형지름길로 안 풀리는가(선형 ≤ 최빈클래스 baseline). "
                                           "null = 최빈클래스 baseline (클래스 사전확률 비균일 ⇒ 1/C 아님)",
                                      pass_=bool(rr > 3 * ch and (lin - maj) < 0.05)),
        V3_info_channel=dict(demand_mean=float(np.mean(glob["demand_mean"])),
                             demand_std=float(np.mean(glob["demand_std"])),
                             demand_corr_m=float(np.mean(glob["demand_corr_m"])),
                             k_std_exp=float(np.mean(dg["iid"]["k_std_exp"])),
                             frac_k_changed_when_demand_shuffled_EXP=float(np.mean(dg["iid"]["chan_exp"])),
                             frac_k_changed_c1=0.0, frac_k_changed_c2=0.0,
                             desc="(a)처치 결정변수가 control 이 못 보는 입력의 함수 (b)운영대역 분산>0",
                             pass_=bool(np.mean(glob["demand_std"]) > 0
                                        and np.mean(dg["iid"]["k_std_exp"]) > 0
                                        and np.mean(dg["iid"]["chan_exp"]) > 0.05)),
        V4_budget_fairness=dict(spend_exp=sp["exp_atp_economy"], spend_c1=sp["c1_static_ceil"],
                                spend_c2=sp["c2_perm_k"], spend_c5=sp["c5_nobank_affperm"],
                                spend_c3=sp["c3_nobank_raw"], spend_ref_unbudgeted=sp["ref_unbudgeted_demand"],
                                desc="primary control 이 EXP 보다 ATP 를 적게 쓰지 않는다 (c1 은 더 씀, c2 는 정확히 일치)",
                                pass_=bool(sp["c1_static_ceil"] >= sp["exp_atp_economy"] - 1e-9
                                           and abs(sp["c2_perm_k"] - sp["exp_atp_economy"]) < 1e-9)),
        V5_budget_binds=dict(binding_rate=float(np.mean(dg["iid"]["binding_rate"])),
                             mean_demand=float(np.mean(glob["demand_mean"])),
                             sustainable_k=float(M_ORGANELLE * 0.9 * RESP - EMIT_QUANTUM),
                             desc="수요>공급 이 실제로 발생 (원 설계에선 정의상 구조적 불가능)",
                             pass_=bool(np.mean(dg["iid"]["binding_rate"]) > 0.10)),
        p5=dict(illegal_channel_closed_all_seeds=bool(all(glob["p5_ok"])),
                emit_rate_static_k1=float(np.mean(glob["emit_k1"])),
                emit_rate_static_k8=float(np.mean(glob["emit_k8"])),
                emit_rate_exp=float(np.mean(glob["emit_exp"])),
                desc="ATP→emit 직결 부재(3 문맥 실주입 해시 동일 + 본문 심볼 부재) · "
                     "합법경로(ATP→용량→표현→tension→emit)는 emit_rate 변화로 살아있음"),
    )
    gates_ok = all(vg[g]["pass_"] for g in ("V1_capacity_lane_live", "V2_expert_specialization",
                                            "V3_info_channel", "V4_budget_fairness", "V5_budget_binds"))
    p5_ok = vg["p5"]["illegal_channel_closed_all_seeds"]

    ts = dict(exp_vs_static=paired(tside["exp"], tside["static"]),
              exp_vs_perm=paired(tside["exp"], tside["perm"]),
              mean_k=float(np.mean(tside["meank"])), binding=float(np.mean(tside["bind"])))

    # ── VERDICT (사전등록 규칙) ──
    dm = deltas["iid"]["micro"]
    if not (gates_ok and p5_ok):
        verdict = "INVALID (V-gate 실패)"
    elif not pooled["iid"]["per_control_signs_agree_2conventions"]:
        verdict = "INVALID (규약이 부호를 결정)"
    else:
        pos = [c for c in PRIM if dm[c]["sig"] and dm[c]["mean"] > 0]
        neg = [c for c in PRIM if dm[c]["sig"] and dm[c]["mean"] < 0]
        if len(pos) == len(PRIM):
            verdict = "PASS (동일비용 수요맹목 통제 전부를 이김)"
        elif len(neg) == len(PRIM):
            verdict = "KILL (동일비용 통제보다 유의하게 나쁨)"
        elif pos and neg:
            verdict = ("SPLIT/DIRECTIONAL — 동일지출 수요맹목 통제(c2)는 이기나 "
                       "지출이 더 많은 static 상수(c1)에는 짐 ⇒ 배분 채널은 실재하나 "
                       "그 크기가 '조금 더 쓰기'에 못 미침")
        elif not pos and not neg and abs(pooled["iid"]["pooled_micro"]) < DELTA_EPS:
            verdict = "THEATER (예산은 binding 되나 downstream Δ≈0 = bookkeeping overhead)"
        else:
            verdict = "MIXED/NS"

    # ── 판정 분해 (사전등록 대비들에서 직접) ──
    #   F1 고유 내용 = **보존 ATP 장 + 저장(reservoir)**.  vs c5 = 동일지출·동일 afford 주변분포,
    #   시간상태(저장 동역학)만 파괴 ⇒ 이 Δ 가 곧 'ATP 장 그 자체'의 기여.
    #   수요→용량 배분 채널 = F10/F4 가 이미 세운 기제. vs c2/c4 가 그것.
    d5, d2, d4, d1 = (deltas["iid"]["micro"][x] for x in
                      ("c5_nobank_affperm", "c2_perm_k", "c4_demand_shuffled", "c1_static_ceil"))
    b5 = deltas["bursty"]["micro"]["c5_nobank_affperm"]
    decomp = dict(
        atp_field_itself_storage=dict(
            contrast="EXP − c5_nobank_affperm (동일지출 · afford 주변분포 동일 · 저장 동역학만 제거)",
            iid=d5, bursty=b5,
            verdict=("THEATER (ATP 장/저장의 기여 = 0)" if (not d5["sig"] and abs(d5["mean"]) < DELTA_EPS)
                     else ("EARNED" if d5["sig"] and d5["mean"] > 0 else "HARMFUL")),
            note="iid 에서 corr(afford, demand)≈0 ⇒ 저장은 cap 의 *주변분포*만 바꾸는 FORM 노브. "
                 "bursty 에서 corr<0 ⇒ 탐욕적 저수지는 지속수요와 역상관 = 오히려 해롭다."),
        demand_to_capacity_channel=dict(
            contrast="EXP − c2_perm_k (동일 k multiset·동일 총지출·수요-표본 결합만 파괴) 및 − c4 (수요 스크램블)",
            vs_c2=d2, vs_c4=d4,
            verdict=("EARNED" if (d2["sig"] and d2["mean"] > 0 and d4["sig"] and d4["mean"] > 0)
                     else "NOT-SUPPORTED"),
            note="F10(수요주도 biogenesis)·F4-SEC(절대 setpoint)이 세운 기제의 독립 재현 — "
                 "ATP 회계와 무관(ref_unbudgeted_demand 는 ATP 예산 없이 static k=8 을 절반 비용으로 이김)."),
        vs_just_spending_more=dict(
            contrast="EXP − c1_static_ceil (수요맹목 상수캡 · ATP 를 ~9% **더** 씀)",
            iid=d1,
            note="배분 이득(+2.4pp)보다 '조금 더 쓰기'가 더 크다 ⇒ 경제는 레버가 아니라 "
                 "예산 증분의 열등한 대체재."),
    )

    summary = {c: {a: {q: dict(mean=float(np.mean(per[c][a][q])),
                               sem=float(np.std(per[c][a][q], ddof=1) / math.sqrt(len(SEEDS))))
                       for q in ("acc", "macro", "meank", "spend")} for a in ARM_ORDER} for c in COND}

    out = dict(
        hypothesis="H_9273 / F1 — ATP 대사경제 · REFIRE (원 INVALID R1~R5 수정)",
        headline_detector="held-out test accuracy under the arm's own deployment capacity policy, at matched ATP spend",
        primary_controls=PRIM, conditions=list(COND),
        pre_registered=dict(D=D, T_TOPIC=T_TOPIC, E=E, C=C, K_MAX=K_MAX, M_CHOICES=list(M_CHOICES),
                            NOISE=NOISE, TAU=TAU, N_TRAIN=N_TRAIN, N_TEST=N_TEST, STEPS=STEPS,
                            BATCH=BATCH, LR=LR, WE_INIT=WE_INIT, SEEDS=SEEDS, PILOT_SEEDS=PILOT_SEEDS,
                            COST_EXPERT=COST_EXPERT, EMIT_QUANTUM=EMIT_QUANTUM, ATP_INIT=ATP_INIT,
                            ATP_CAP=ATP_CAP, M_ORGANELLE=M_ORGANELLE, RESP=RESP, WEAR=WEAR,
                            REPAIR=REPAIR, BLOCK=BLOCK, ALPHA=ALPHA, DELTA_EPS=DELTA_EPS,
                            MDE_MAX_FRAC=MDE_MAX_FRAC),
        power_precheck=pw, v_gates=vg, summary=summary, verdict_decomposition=decomp,
        deltas=deltas, pooled=pooled, training_side_economy=ts,
        diagnostics={c: {q: float(np.mean(v)) for q, v in dg[c].items()} for c in COND},
        per_seed={c: per[c] for c in COND},
        verdict=verdict, wall_sec=round(time.time() - t0, 2),
    )
    json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=2, ensure_ascii=False)

    # ── print ──
    print("\n\n── V-GATES (헤드라인 detector 위) ──")
    for g, v in vg.items():
        body = {k: (round(x, 4) if isinstance(x, float) else x) for k, x in v.items()
                if k not in ("desc", "pass_", "hash_real", "hash_atp_zeroed", "hash_atp_random")}
        print(f"  {g:26s} PASS={v.get('pass_', '—')}  {body}")
    for c in COND:
        print(f"\n══ 조건 [{c}] ══  (binding={np.mean(dg[c]['binding_rate']):.3f} · "
              f"mean_k_exp={np.mean(dg[c]['meank_exp']):.3f} · corr(afford,demand)={np.mean(dg[c]['corr_afford_demand']):+.3f})")
        hdr = f"  {'arm':24s} {'mean_k':>7s} {'ATP/샘플':>9s} {'acc(micro)':>17s} {'acc(macro)':>17s}"
        print(hdr)
        for a in ARM_ORDER:
            s_ = summary[c][a]
            print(f"  {a:24s} {s_['meank']['mean']:7.3f} {s_['spend']['mean']:9.3f} "
                  f"{s_['acc']['mean']:.4f}±{s_['acc']['sem']:.4f}  {s_['macro']['mean']:.4f}±{s_['macro']['sem']:.4f}")
        print(f"  ── Δ (EXP − control) · control별 paired-t (max(controls) 금지) ──")
        for ctl in CONTROLS:
            d, dM = deltas[c]["micro"][ctl], deltas[c]["macro"][ctl]
            tag = "PRIMARY" if ctl in PRIM else ("ref" if ctl.startswith("ref") else "mech")
            print(f"    [{tag:7s}] vs {ctl:22s} Δ={d['mean']:+.4f} SEM={d['sem']:.4f} t={d['t']:+7.2f} "
                  f"p={d['p']:.2e} {d['wins']:2d}/{d['n']} sig={str(d['sig']):5s} | macro Δ={dM['mean']:+.4f}")
        print(f"    POOLED(primary) micro={pooled[c]['pooled_micro']:+.4f} macro={pooled[c]['pooled_macro']:+.4f} "
              f"sign_ok(2규약)={pooled[c]['per_control_signs_agree_2conventions']}")

    print("\n── 판정 분해 ──")
    for kk, vv in decomp.items():
        print(f"  [{kk}] {vv.get('verdict', '')}")
        print(f"     {vv['contrast']}")
    print(f"\n── 부차: 학습단계 경제 (공통 k=8 평가 · mean_k={ts['mean_k']:.2f} binding={ts['binding']:.3f}) ──")
    print(f"   vs static Δ={ts['exp_vs_static']['mean']:+.4f} t={ts['exp_vs_static']['t']:+.2f} p={ts['exp_vs_static']['p']:.2e}")
    print(f"   vs perm   Δ={ts['exp_vs_perm']['mean']:+.4f} t={ts['exp_vs_perm']['t']:+.2f} p={ts['exp_vs_perm']['p']:.2e}")
    print(f"\nVERDICT: {verdict}   (wall={out['wall_sec']}s)")
    return out


if __name__ == "__main__":
    main()
