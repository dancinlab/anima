#!/usr/bin/env python3
"""H_9285 — organelle lane 결착 프로브 (eval-only · 학습 0 · GPU 학습비 0).

절대-setpoint 배분기를 303M CLMConvMoE 의 expert capacity schedule 에 얹으면
held-out 재조합(ρ·weave conjunctive margin / D-acc)이 baseline 대비 오르는가.

ENGINE-NATIVE: trunk forward 는 설치된 anima_py(core/decode.py)의 프로덕션 경로를
그대로 재사용한다(_conv1d/nn_groupnorm_fwd/nn_gelu_fwd/nn_moe_softmax/_seed_to_tok).
dense(k=E) 재구성이 clm._fwd_logits 와 byte-exact(max|Δ|=0)인지 PARITY GATE 로 증명한다.

구조적 사실 (측정 전 확인):
  * 프로덕션 CLM router = DENSE soft mixture (y=Σ_e p[t,e]·ex[e,t,c]).
    프로덕션에는 expert top-k / capacity 자체가 없다 ⇒ c0 = dense = k=E.
    처치(top-k)는 항상 정보를 '버리는' 연산이다.
  * py303_full.clm : d=3784 · E=3 · K=3 · L=4 · V=256 · T=24-byte window.
  * final GroupNorm(G=1) 은 [T,C] 전체를 정규화 ⇒ k_t 는 전 위치 logits 에 결합.
    (per-position 닫힌형 oracle 불가 → greedy coordinate-ascent oracle 사용)

계측 규칙 (강제):
  1. Δ = exp − max(controls) 금지 → control 별 paired-t 전부 보고.
  2. mean vs 1·std 기각 휴리스틱 금지 → paired SEM/t 만.
  3. 사전 MDE 계산 (pilot) → 축 동적범위(oracle headroom) 와 비교.
  4. 정보채널 증명: k_t = f(router mass at t) = control 이 못 보는 입력의 함수 + Var(k_t)>0 실측.
  5. V-gate 는 헤드라인 detector 그 자체(m_conj)에 건다: SHOCK arm 이 m_conj 를 움직이는가
     (=처치 채널이 detector 에 보이는가) + 단일-cue ceiling>0 (=detector liveness).
금지지표(conj_index/purity/acc비율/corr(n,demand)) 미사용.
"""
import sys, os, re, json, math, time, random
import numpy as np

SITE = os.environ.get("ANIMA_CORE",
                      "/home/aiden/.local/lib/python3.12/site-packages/anima_py/core")
sys.path.insert(0, SITE)
import decode as clm  # engine-native py 2-production forward

CKPT = os.environ.get("CKPT", "/home/aiden/py303_full.clm")
CORPUS = [os.environ.get("CORPUS_DIR", "/home/aiden/anima_train_corpus") + "/" + f
          for f in ("gen_en.txt", "sns_en.txt")]
OUT = os.environ.get("OUT", "/home/aiden/h9285_result.json")

T = 24
N_BLOCK = 20          # seeds (paired-CRN blocks)
ITEMS_PER_BLOCK = 6   # → 120 items
PILOT_BLOCKS = 4      # MDE pre-check
KGRID = None          # filled after load (1..E)
THETA_PREREG = None   # absolute setpoint, fixed from a corpus probe set (never sees detector)

t0 = time.time()
def log(*a):
    print("[%7.1fs]" % (time.time() - t0), *a, flush=True)

# ═══════════════════════════════════════════════════════════════════════════
# 1. engine-native split forward: trunk → (router logits, expert outs) [EXPENSIVE, arm-free]
#    then mix(k-schedule) → GN → readout [CHEAP, per-arm]
# ═══════════════════════════════════════════════════════════════════════════
def trunk_split(W, tok):
    """1:1 with core/decode.py _fwd_trunk up to the MoE mix. Returns (logits_r[T,E], ex[E,T,d])."""
    d, E, K, L = W["d"], W["E"], W["K"], W["L"]
    xp = clm.get_xp(W["ecWt"])
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = clm._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1, xp)
    dil = 1
    for li in range(L):
        de = dil if dil <= 512 else 512
        h = clm._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, de, xp)
        hn = clm.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1, xp)
        hg = clm.nn_gelu_fwd(hn, xp)
        xt = xt + hg.reshape(T, d)
        dil = dil * 2
    logits_r = clm._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1, xp)
    ex = xp.empty((E, T, d), dtype=xp.float64)
    for ej in range(E):
        eo = clm._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1, xp)
        ex[ej] = clm.nn_gelu_fwd(eo, xp).reshape(T, d)
    return clm.to_host(logits_r), clm.to_host(ex)


def probs_of(logits_r, E):
    return clm.nn_moe_softmax(logits_r, T, E, np)          # [T,E]


def mix_logits(W, probs, ex, rows=None):
    """probs[T,E] (already arm-modified) → y → final GN → readout. rows = logit rows needed."""
    d, V, E = W["d"], W["V"], W["E"]
    y = np.einsum('te,etc->tc', probs, ex)
    yn = clm.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1, np)
    if rows is None:
        return clm._conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1, np)
    # readout is a K=1 conv ⇒ pure per-row linear; restrict to the rows we score.
    sub = yn[rows]                                          # [r, d]
    return sub @ W["roWt"].reshape(d, V) + W["roB"]         # [r, V]


def apply_topk(probs, kvec):
    """capacity gating: keep top-k_t experts at position t, renormalize. kvec[T] ints."""
    P = probs.copy()
    T_, E = P.shape
    order = np.argsort(-P, axis=1, kind='stable')
    for t in range(T_):
        k = int(kvec[t])
        if k >= E:
            continue
        drop = order[t, k:]
        P[t, drop] = 0.0
        s = P[t].sum()
        P[t] = P[t] / s if s > 0 else 1.0 / E
    return P


def cum_mass(probs):
    """cumulative router mass after top-1 … top-E, sorted desc. [T,E]"""
    s = np.sort(probs, axis=1)[:, ::-1]
    return np.cumsum(s, axis=1)


def setpoint_k(probs, theta):
    """★ 처치 = 절대-setpoint 배분기.
    k_t = min{k : Σ_{i≤k} sorted_p[t,i] ≥ θ}  (θ = ABSOLUTE setpoint, 위치 무관 상수)
    결정변수 = 위치 t 의 router demand mass = f(입력 토큰) — 상수 arm(c1)은 볼 수 없는 입력의 함수."""
    cm = cum_mass(probs)                                    # [T,E]
    E = probs.shape[1]
    k = np.full(T, E, dtype=np.int64)
    for t in range(T):
        for j in range(E):
            if cm[t, j] >= theta:
                k[t] = j + 1
                break
    return k


# ═══════════════════════════════════════════════════════════════════════════
# 2. detector — held-out conjunctive recombination margin (2-cue, scramble-referenced)
#    ctx_AB   = "A. B. "     both cues (NOVEL pair: A·B never co-occur in corpus)
#    ctx_Aonly= "A. B~. "    B byte-scrambled  (length-matched ⇒ cue-content distance identical)
#    ctx_Bonly= "A~. B. "
#    ctx_null = "A~. B~. "   both scrambled = the lift reference
#    lift(x|c) = logP(x|c) − logP(x|null)
#    m_A_conj  = lift(a|AB) − lift(f|AB)      ; m_B_conj = lift(b|AB) − lift(f|AB)
#    m_conj    = min(m_A_conj, m_B_conj)      ← HEADLINE (둘 다 살아있어야 재조합)
#    ceiling   = min(m_A_single, m_B_single)  ← 같은 가중치로 '단일 cue 는' 소비 가능함을 증명(liveness)
#    D-acc     = 1[m_A_conj>0 ∧ m_B_conj>0]
# ═══════════════════════════════════════════════════════════════════════════
WORD = re.compile(r"\b[a-z]{3,5}\b")   # WHOLE words only (fragment-collocation 방지)

def mine_items(min_items):
    txt = ""
    for p in CORPUS:
        with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
            txt += fh.read().lower() + "\n"
    toks = [(m.group(0), m.start()) for m in WORD.finditer(txt)]
    words = [w for w, _ in toks]
    N = len(words)
    log("corpus words", N)
    uni = {}
    for w in words:
        uni[w] = uni.get(w, 0) + 1
    vocab = set(uni)
    # ── NEAR = 모델의 24-byte 학습 윈도우 안에서 실제로 공기(共起)한 적 있는 단어쌍 ──
    #    (RF=24B ⇒ 24바이트 안에서 한 번도 같이 나온 적 없는 쌍 = 이 모델에겐 진짜 held-out 조합)
    near = set()
    for i in range(N):
        wi, pi = toks[i]
        j = i + 1
        while j < N and toks[j][1] - pi <= T:
            wj = toks[j][0]
            if wj != wi:
                near.add((wi, wj)); near.add((wj, wi))
            j += 1
    log("near pairs (co-present within a 24B window)", len(near))

    def build(min_uni, min_c, min_pmi):
        col = {}
        for i in range(N):
            wi = words[i]
            if uni[wi] < min_uni:
                continue
            for j in range(i + 1, min(i + 4, N)):
                wj = words[j]
                if wj == wi or uni[wj] < min_uni:
                    continue
                col[(wi, wj)] = col.get((wi, wj), 0) + 1
        pairs = []
        for (u, w), c in col.items():
            if c < min_c:
                continue
            pmi = math.log((c / N) / ((uni[u] / N) * (uni[w] / N) * 3.0))
            if pmi > min_pmi:
                pairs.append((pmi, c, u, w))
        pairs.sort(reverse=True)
        cues = {}
        for pmi, c, u, w in pairs:
            if u in cues or u == w:
                continue
            cues[u] = (w, pmi, c)
        cand = [(u, v[0], v[1], v[2]) for u, v in cues.items()]
        cand.sort(key=lambda x: -x[2])
        return cand

    rng = random.Random(20260712)
    def scramble(w):
        for _ in range(80):
            l = list(w); rng.shuffle(l); s = "".join(l)
            if s != w and s not in vocab:
                return s
        return w[::-1]

    # cue/content 는 아이템당 최대 CAP 회 재사용 (풀 크기 확보; 블록 단위 paired-CRN 은 유지)
    for (mu, mc, mp, cap) in [(150, 25, 1.0, 1), (80, 15, 1.0, 2), (60, 12, 0.8, 2), (40, 8, 0.6, 3)]:
        cand = build(mu, mc, mp)
        log("thresholds uni>=%d cnt>=%d pmi>%.1f cap=%d → cue→content candidates %d"
            % (mu, mc, mp, cap, len(cand)))
        items = []
        use = {}
        def free(*ws):
            return all(use.get(w, 0) < cap for w in ws)
        def take(*ws):
            for w in ws:
                use[w] = use.get(w, 0) + 1
        for i in range(len(cand)):
            A, a = cand[i][0], cand[i][1]
            if not free(A, a):
                continue
            for j in range(i + 1, len(cand)):
                B, b = cand[j][0], cand[j][1]
                if not free(B, b) or len({A, a, B, b}) < 4:
                    continue
                # HELD-OUT: A·B, A·b, B·a, a·b — 어느 쌍도 24B 윈도우 안에서 공기한 적 없음
                if (A, B) in near or (A, b) in near or (B, a) in near or (a, b) in near:
                    continue
                foil = None
                for m in range(len(cand)):
                    C, f = cand[m][0], cand[m][1]
                    if f in (a, b) or C in (A, B) or not free(f):
                        continue
                    if (A, f) in near or (B, f) in near:
                        continue
                    foil = f
                    break
                if foil is None:
                    continue
                if len(A) + len(B) + 2 + max(len(a), len(b), len(foil)) > T:
                    continue
                items.append({"A": A, "B": B, "a": a, "b": b, "f": foil,
                              "As": scramble(A), "Bs": scramble(B)})
                take(A, B, a, b, foil)
                break
        log("  items mined", len(items))
        if len(items) >= min_items:
            return items
    return items


def ctxs(it):
    # 4 컨텍스트는 길이·구조가 완전히 동일하고, 오직 cue 단어의 '정체'만 다르다
    # (scramble = 같은 바이트 구성의 비단어) ⇒ cue→content 거리/길이 confound 0.
    return {"AB":    "%s %s " % (it["A"], it["B"]),
            "Aonly": "%s %s " % (it["A"], it["Bs"]),
            "Bonly": "%s %s " % (it["As"], it["B"]),
            "null":  "%s %s " % (it["As"], it["Bs"])}


# (ctx, content) pairs actually needed per item
NEED = [("AB", "a"), ("AB", "b"), ("AB", "f"),
        ("Aonly", "a"), ("Aonly", "f"),
        ("Bonly", "b"), ("Bonly", "f"),
        ("null", "a"), ("null", "b"), ("null", "f")]


def seq_rows(ctx, content):
    """right-aligned 24-byte window; content occupies the last n bytes.
    logP(content) uses rows [24-n-1 .. 22]."""
    full = ctx + content
    fb = full.encode()
    assert len(fb) <= T, (full, len(fb))
    tok = clm._seed_to_tok(full, T)
    n = len(content.encode())
    rows = np.arange(T - n - 1, T - 1)
    tgt = tok[T - n:].astype(np.int64)
    return tok, rows, tgt


def logp(logit_rows, tgt):
    x = logit_rows - logit_rows.max(axis=1, keepdims=True)
    lse = np.log(np.exp(x).sum(axis=1))
    return float((x[np.arange(len(tgt)), tgt] - lse).sum())


# ═══════════════════════════════════════════════════════════════════════════
# 3. main
# ═══════════════════════════════════════════════════════════════════════════
def main():
    global KGRID, THETA_PREREG, ITEMS_PER_BLOCK
    log("load", CKPT)
    W = clm.clm_load_weights(CKPT)
    assert W["ok"] and W.get("bind_type", 0) == 0 and W.get("slw") is None and W.get("clml") is None
    d, E, V = W["d"], W["E"], W["V"]
    KGRID = list(range(1, E + 1))
    log("dims d=%d E=%d K=%d L=%d V=%d T=%d" % (d, E, W["K"], W["L"], V, T))

    # ── PARITY GATE: dense reconstruction == production _fwd_logits (byte-exact) ──
    tokp = clm._seed_to_tok("mind. dream. body", T)
    ref = clm._fwd_logits(W, tokp, T)
    lr, ex = trunk_split(W, tokp)
    got = mix_logits(W, probs_of(lr, E), ex)
    parity = float(np.abs(np.asarray(ref) - np.asarray(got)).max())
    rws = np.arange(18, 23)
    got_r = mix_logits(W, probs_of(lr, E), ex, rows=rws)
    parity_rows = float(np.abs(np.asarray(ref)[rws] - np.asarray(got_r)).max())
    log("PARITY max|Δ| = %r (rows-path %r)" % (parity, parity_rows))
    assert parity == 0.0, "engine-native parity FAILED"
    assert parity_rows < 1e-9, "rows-path drift"

    # ── θ: 절대-setpoint 를 corpus probe set 에서 고정 (detector item 을 절대 보지 않음) ──
    with open(CORPUS[0], 'rb') as fh:
        raw = fh.read(400000)
    rr = random.Random(7)
    masses = []
    for _ in range(24):
        o = rr.randrange(0, len(raw) - T - 1)
        tk = np.frombuffer(raw[o:o + T], dtype=np.uint8).astype(np.float64)
        lr_p, _ex_p = trunk_split(W, tk)
        cm = cum_mass(probs_of(lr_p, E))
        masses.append(cm[:, 0])                      # top-1 mass
    m1 = np.concatenate(masses)
    THETA_PREREG = float(np.median(m1))
    log("router top-1 mass: mean=%.4f sd=%.4f min=%.4f max=%.4f → θ(abs setpoint)=%.4f"
        % (m1.mean(), m1.std(), m1.min(), m1.max(), THETA_PREREG))
    theta_stats = {"top1_mass_mean": float(m1.mean()), "top1_mass_sd": float(m1.std()),
                   "top1_mass_min": float(m1.min()), "top1_mass_max": float(m1.max()),
                   "theta_prereg": THETA_PREREG, "n_probe_pos": int(len(m1))}

    items = mine_items(N_BLOCK * ITEMS_PER_BLOCK)
    if len(items) < N_BLOCK * ITEMS_PER_BLOCK:      # 20 seed-block 은 사수, 블록당 item 만 축소
        ITEMS_PER_BLOCK = len(items) // N_BLOCK
        log("!! item pool short → ITEMS_PER_BLOCK =", ITEMS_PER_BLOCK)
    assert ITEMS_PER_BLOCK >= 3, "item pool too small (%d) for 20 blocks" % len(items)
    n_use = N_BLOCK * ITEMS_PER_BLOCK
    items = items[:n_use]
    nblk = N_BLOCK
    log("blocks(seeds)=%d items=%d (per block %d)" % (nblk, n_use, ITEMS_PER_BLOCK))

    ARMS = ["c0", "c1_k1", "c1_k2", "EXP", "c2_shuf", "SHOCK"]
    # per item: margins per arm
    rows_out = []
    kstats = {"k_all": [], "var_per_seq": []}
    oracle_rows = []

    for idx, it in enumerate(items):
        C = ctxs(it)
        cache = {}
        for cname, xname in NEED:
            ctx, content = C[cname], it[xname]
            tok, rows, tgt = seq_rows(ctx, content)
            lr, ex = trunk_split(W, tok)
            cache[(cname, xname)] = {"lr": lr, "ex": ex, "rows": rows, "tgt": tgt,
                                     "p": probs_of(lr, E)}
        # ---- per-arm scores ----
        def score(key, arm, rng=None):
            c = cache[key]
            P = c["p"]
            if arm == "c0":
                Pm = P
            elif arm.startswith("c1_k"):
                k = int(arm[-1]); Pm = apply_topk(P, np.full(T, k))
            elif arm == "EXP":
                Pm = apply_topk(P, setpoint_k(P, THETA_PREREG))
            elif arm == "c2_shuf":
                kv = setpoint_k(P, THETA_PREREG).copy()
                rng.shuffle(kv)
                Pm = apply_topk(P, kv)
            elif arm == "SHOCK":                      # V-gate: router mixing 파괴(균등)
                Pm = np.full_like(P, 1.0 / E)
            lg = mix_logits(W, Pm, c["ex"], rows=c["rows"])
            return logp(lg, c["tgt"])

        srng = np.random.RandomState(1000 + idx)
        S = {}
        for arm in ARMS:
            S[arm] = {key: score(key, arm, srng) for key in cache}

        # info channel: k_t 변동 실측 (EXP arm)
        for key in cache:
            kv = setpoint_k(cache[key]["p"], THETA_PREREG)
            kstats["k_all"].extend([int(v) for v in kv])
            kstats["var_per_seq"].append(float(np.var(kv)))

        def margins(s):
            lift = lambda c, x: s[(c, x)] - s[("null", x)]
            mA = lift("AB", "a") - lift("AB", "f")
            mB = lift("AB", "b") - lift("AB", "f")
            sA = lift("Aonly", "a") - lift("Aonly", "f")
            sB = lift("Bonly", "b") - lift("Bonly", "f")
            return {"m_A_conj": mA, "m_B_conj": mB,
                    "m_conj": min(mA, mB), "m_mean": 0.5 * (mA + mB),
                    "dacc": 1.0 if (mA > 0 and mB > 0) else 0.0,
                    "ceiling": min(sA, sB), "s_A": sA, "s_B": sB}

        rows_out.append({"item": idx, "block": idx // ITEMS_PER_BLOCK,
                         "words": {k: it[k] for k in ("A", "B", "a", "b", "f")},
                         "arm": {arm: margins(S[arm]) for arm in ARMS}})

        # ---- greedy oracle (PILOT items only) : k-축 동적범위 상한/하한 ----
        if idx // ITEMS_PER_BLOCK < PILOT_BLOCKS:
            def opt_seq(key, maximize):
                c = cache[key]; P = c["p"]
                kv = np.full(T, E, dtype=np.int64)
                best = logp(mix_logits(W, apply_topk(P, kv), c["ex"], rows=c["rows"]), c["tgt"])
                for _sweep in range(2):
                    for t in range(T):
                        cur = kv[t]
                        for k in KGRID:
                            if k == cur:
                                continue
                            kv[t] = k
                            v = logp(mix_logits(W, apply_topk(P, kv), c["ex"], rows=c["rows"]),
                                     c["tgt"])
                            if (v > best) if maximize else (v < best):
                                best = v; cur = k
                            kv[t] = cur
                return best
            hi, lo = {}, {}
            for key in cache:
                hi[key] = opt_seq(key, True)
                lo[key] = opt_seq(key, False)
            # margin 은 각 sequence score 의 부호 있는 선형결합 ⇒ 시퀀스별 독립 최적화로 상/하한
            def bound(sign_map, use_hi):
                s = {}
                for key, sg in sign_map.items():
                    want_hi = (sg > 0) == use_hi
                    s[key] = hi[key] if want_hi else lo[key]
                return s
            # m_A_conj = [AB,a] - [null,a] - [AB,f] + [null,f]
            sgA = {("AB", "a"): +1, ("null", "a"): -1, ("AB", "f"): -1, ("null", "f"): +1}
            sgB = {("AB", "b"): +1, ("null", "b"): -1, ("AB", "f"): -1, ("null", "f"): +1}
            def lin(sg, s):
                return sum(v * s[k] for k, v in sg.items())
            mA_hi = lin(sgA, bound(sgA, True)); mA_lo = lin(sgA, bound(sgA, False))
            mB_hi = lin(sgB, bound(sgB, True)); mB_lo = lin(sgB, bound(sgB, False))
            oracle_rows.append({"item": idx, "block": idx // ITEMS_PER_BLOCK,
                                "oracle_m_conj_hi": min(mA_hi, mB_hi),
                                "oracle_m_conj_lo": min(mA_lo, mB_lo),
                                "c0_m_conj": rows_out[-1]["arm"]["c0"]["m_conj"]})
        if (idx + 1) % 6 == 0:
            log("items done %d/%d" % (idx + 1, n_use))

    # ═══════════════ aggregate ═══════════════
    def blockmean(arm, field, blocks=None):
        out = []
        for b in range(nblk):
            if blocks is not None and b not in blocks:
                continue
            v = [r["arm"][arm][field] for r in rows_out if r["block"] == b]
            out.append(float(np.mean(v)))
        return np.array(out)

    def paired(a, b):
        dd = a - b
        n = len(dd)
        mean = float(dd.mean())
        sd = float(dd.std(ddof=1))
        sem = sd / math.sqrt(n)
        t = mean / sem if sem > 0 else 0.0
        # two-sided p, normal approx + t-table crit
        from math import erf
        p = 2 * (1 - 0.5 * (1 + erf(abs(t) / math.sqrt(2))))
        return {"mean_delta": mean, "sd": sd, "sem": sem, "t": t, "p_approx": p, "n": n}

    HEAD = "m_conj"
    pilot = set(range(PILOT_BLOCKS))
    # ---- MDE (pilot only, 사전) ----
    pe = blockmean("EXP", HEAD, pilot); pc = blockmean("c0", HEAD, pilot)
    sd_pilot = float((pe - pc).std(ddof=1))
    MDE = 2.093 * sd_pilot / math.sqrt(nblk)      # t_.975,19
    orc_hi = float(np.mean([o["oracle_m_conj_hi"] for o in oracle_rows]))
    orc_lo = float(np.mean([o["oracle_m_conj_lo"] for o in oracle_rows]))
    orc_c0 = float(np.mean([o["c0_m_conj"] for o in oracle_rows]))
    axis_range = orc_hi - orc_c0                  # k-축이 detector 를 올릴 수 있는 최대 여지
    axis_swing = orc_hi - orc_lo                  # k-축 전체 진폭
    ceil_all = blockmean("c0", "ceiling"); conj_all = blockmean("c0", HEAD)
    detector_range = float(ceil_all.mean() - conj_all.mean())
    mde_ok = bool(MDE < axis_range)

    res = {
        "hypothesis": "H_9285",
        "ckpt": CKPT, "dims": {"d": d, "E": E, "K": W["K"], "L": W["L"], "V": V, "T": T},
        "parity_max_abs_delta": parity,
        "n_blocks": nblk, "items_per_block": ITEMS_PER_BLOCK, "n_items": n_use,
        "headline": HEAD,
        "theta": theta_stats,
        "info_channel": {
            "decision_var": "cumulative router mass at position t (softmax over router conv logits) "
                            "— a function of the INPUT tokens; c1 (constant k) cannot see it",
            "k_hist": {str(k): int(np.sum(np.array(kstats["k_all"]) == k)) for k in KGRID},
            "k_mean": float(np.mean(kstats["k_all"])),
            "k_var_overall": float(np.var(kstats["k_all"])),
            "k_var_within_seq_mean": float(np.mean(kstats["var_per_seq"])),
            "frac_seqs_with_var0": float(np.mean([v == 0 for v in kstats["var_per_seq"]])),
        },
        "mde": {"sd_pilot_blockdelta": sd_pilot, "MDE_alpha05_n20": MDE,
                "oracle_hi_mean": orc_hi, "oracle_lo_mean": orc_lo, "c0_mean_pilot": orc_c0,
                "axis_dynamic_range_up": axis_range, "axis_full_swing": axis_swing,
                "detector_headroom_ceiling_minus_c0": detector_range,
                "mde_ok": mde_ok, "pilot_blocks": PILOT_BLOCKS},
        "arms": {}, "paired_vs_controls": {}, "secondary": {},
    }
    for arm in ARMS:
        v = blockmean(arm, HEAD)
        res["arms"][arm] = {"mean": float(v.mean()),
                            "sem_across_blocks": float(v.std(ddof=1) / math.sqrt(nblk)),
                            "dacc": float(blockmean(arm, "dacc").mean()),
                            "m_mean_branch": float(blockmean(arm, "m_mean").mean())}
    exp = blockmean("EXP", HEAD)
    # c1 = BEST constant k, grid 전수 (k=E ≡ c0 dense). 선택은 held-out 절반에서(선택편향 차단)
    half = set(range(nblk // 2))
    cands = ["c1_k%d" % k for k in KGRID[:-1]] + ["c0"]     # k=E == c0
    sel = max(cands, key=lambda a: float(blockmean(a, HEAD, half).mean()))
    res["c1_best_constant"] = {"selected_on_first_half": sel,
                               "grid": {a: float(blockmean(a, HEAD).mean()) for a in cands}}
    for ctrl in ["c0", sel, "c2_shuf"]:
        res["paired_vs_controls"]["EXP_vs_" + ctrl] = paired(exp, blockmean(ctrl, HEAD))
    pooled = np.mean([blockmean(c, HEAD) for c in ["c0", sel, "c2_shuf"]], axis=0)
    res["paired_vs_controls"]["EXP_vs_pooled_mean_of_controls"] = paired(exp, pooled)
    # V-gate: SHOCK 이 헤드라인 detector 를 움직이는가 (처치채널 가시성) + detector liveness
    res["vgate"] = {
        "SHOCK_vs_c0": paired(blockmean("SHOCK", HEAD), blockmean("c0", HEAD)),
        "k1_vs_c0": paired(blockmean("c1_k1", HEAD), blockmean("c0", HEAD)),
        "ceiling_single_cue_mean": float(ceil_all.mean()),
        "ceiling_sem": float(ceil_all.std(ddof=1) / math.sqrt(nblk)),
        "conj_c0_mean": float(conj_all.mean()),
        "conj_c0_sem": float(conj_all.std(ddof=1) / math.sqrt(nblk)),
    }
    res["secondary"]["dacc_paired_EXP_vs_c0"] = paired(blockmean("EXP", "dacc"),
                                                       blockmean("c0", "dacc"))
    res["secondary"]["m_mean_paired_EXP_vs_c0"] = paired(blockmean("EXP", "m_mean"),
                                                         blockmean("c0", "m_mean"))
    res["items"] = rows_out
    res["oracle_rows"] = oracle_rows
    res["wall_s"] = time.time() - t0
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    log("WROTE", OUT)
    log(json.dumps({k: res[k] for k in ("arms", "paired_vs_controls", "vgate", "mde",
                                        "info_channel", "c1_best_constant")}, indent=1))


if __name__ == "__main__":
    main()
