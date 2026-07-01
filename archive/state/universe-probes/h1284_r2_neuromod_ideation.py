#!/usr/bin/env python3
"""
H_1284 R2 — CONTEXT-ADAPTIVE NEUROMODULATION ON THE IDEATION / DECODE LANE.

R1 (🔴 CLOSED-NEG) tested a context-adaptive neuromodulator (DA gain + NE
exploration + ACh plasticity -> plasticity-rate/split-thresh/abstain-margin) on the
MEMORY substrate: it did NOT beat best-fixed hyperparams; on non-stationary regimes
it HURT and raised fabrication. R1's not-ruled-out clause (a): the decode-time NE
TEMPERATURE channel on IDEATION remained 🟠 viable per H_1228 (SOC decode PARTIAL).

R2 RE-SCOPES the neuromodulator to the GENERATION/IDEATION lane where it has
demonstrated life (a_no_llm_frame_trap — neuro lens, NOT an LLM recipe). H_1228's
arm C drives the next-byte branching σ toward a FIXED target σ*=2.5. R2 asks: does a
CONTEXT-ADAPTIVE controller — one that READS the recent output state (repetition /
local novelty / coherence) and adapts its σ*-target per step — beat the BEST FIXED
decode point on a frozen COMBINED ideation metric?

ARMS (identical model/seeds/max_new/top-k=40; ONLY the per-step temperature policy):
  ARM A      = BEST FIXED decode point, tuned over a fixed grid (fixed-temp sampling
               {0.5,0.7,0.9,1.1} + fixed-σ* targeting {1.8,2.5,3.2}) on a DISJOINT
               tuning seed (5) by the combined metric M. The winner = A.
  ARM B      = context-adaptive neuromodulator: same σ*-targeting controller, but the
               σ*-TARGET is modulated each step by a no-grad readout of recent output
               (repetition r_t, novelty n_t, coherence c_t):
                 σ*_t = σ*_0*(1 + kR*r_t + kN*(1-n_t))*(1 - kC*max(0,COH_FLOOR-c_t)),
               clamped to [1.5,3.5]. RAISE exploration on loops/low-novelty (NE/ACh),
               LOWER it when coherence drops below floor (DA coherence-gain).
  ARM C-SHUF = coupling control: B's OWN σ*_t values RANDOMLY PERMUTED (same knob
               distribution, decoupled from state) — isolates COUPLING from VARIETY.

Frozen falsifier + metric + gains: see H_1284_R2_FREEZE.txt. p7: no LLM-judge, no
perplexity, controller is a pure no-grad readout NEVER folded into a loss. $0
CPU/torch-ref. DIRECTIONAL (a_engine_native_learning — engine-transfer UNVERIFIED).
Does NOT edit CORE/*.hexa or H_1228.
"""
import os, sys, json, math, time, argparse, random
import torch, torch.nn as nn, torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
# relocated 2026-06-16 UNIVERSE/ -> state/universe-probes/; repo root is 2 up, not 1.
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tool"))  # gauge_lib relocated to tool/
import gauge_lib as G   # FROZEN evaluators (VERBATIM)

CKPT_DEFAULT   = os.environ.get("H1284R2_CKPT",
    "/Users/mini/dancinlab/anima/state/chat_303m/h1129c_chat.pt")
CORPUS_DEFAULT = os.path.join(ROOT, "data", "corpus.txt")

# ── ByteGPT (VERBATIM from H_1228 / torch_greedy_baseline) ──────────────────────
class Block(nn.Module):
    def __init__(s, d, h, p=0.0):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block=block; s.n_head=n_head; s.d=d; s.n_layer=n_layer; s.vocab=vocab
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx):
        B,T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None,:,:])
        mask = torch.triu(torch.full((T,T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))

# ── decode config (H_1228 frozen constants) ─────────────────────────────────────
BLOCK, TOP_K, MAX_NEW, KP = 512, 40, 96, 0.6
T_MIN, T_MAX = 0.05, 3.0
STOPS = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]

# adaptive-controller gains (FROZEN in H_1284_R2_FREEZE.txt)
W_WIN, COH_FLOOR = 24, 0.50
kR, kN, kC = 0.6, 0.4, 0.5
SIGMA_STAR_0 = 2.5           # σ*_0 for the adaptive arm (H_1228 frozen σ*)
SIG_LO, SIG_HI = 1.5, 3.5    # adaptive σ*_t clamp

# fixed-grid for ARM A tuning (BOTH H_1228 families)
GRID_FIXED_TEMP  = [0.5, 0.7, 0.9, 1.1]
GRID_FIXED_SIGMA = [1.8, 2.5, 3.2]


def _topk_mask(logits, k):
    if not k: return logits
    v, _ = torch.topk(logits, min(k, logits.shape[-1]))
    return logits.masked_fill(logits < v[-1], float("-inf"))

def _entropy_eff(probs):
    p = probs[probs > 0]
    H = float(-(p * p.log()).sum().item())
    return math.exp(H)

def _drive_T_to_sigma(raw, logT, sigma_target):
    """one P-controller step in log-temp toward sigma_target; returns (probs, sig, logT)."""
    T = math.exp(logT)
    probs = F.softmax(_topk_mask(raw / T, TOP_K), dim=-1)
    sig = _entropy_eff(probs)
    logT = min(math.log(T_MAX), max(math.log(T_MIN),
              logT + KP * (math.log(sigma_target) - math.log(max(sig, 1e-9)))))
    probs2 = F.softmax(_topk_mask(raw / math.exp(logT), TOP_K), dim=-1)
    return probs2, _entropy_eff(probs2), logT


def _adapt_sigma(out_bytes, text):
    """no-grad readout of recent output state -> adapted σ*_t (NE/ACh/DA)."""
    recent = out_bytes[-W_WIN:]
    if len(recent) >= 2:
        seen = set(); rep = 0
        for b in recent:
            if b in seen: rep += 1
            seen.add(b)
        r_t = rep / len(recent)                    # repetition pressure (loop)
        n_t = len(set(recent)) / len(recent)       # distinct-byte ratio = local novelty
    else:
        r_t, n_t = 0.0, 1.0
    c_t = G.known_word_ratio(text) if text else 1.0
    sig = SIGMA_STAR_0 * (1 + kR*r_t + kN*(1-n_t)) * (1 - kC*max(0.0, COH_FLOOR - c_t))
    return max(SIG_LO, min(SIG_HI, sig)), (r_t, n_t, c_t)


def _decode(model, seed_text, policy, seed_rng, device, max_new=MAX_NEW):
    """policy = ('fixed_temp',T) | ('fixed_sigma',σ*) | ('adaptive',None) |
                ('shuf', list_of_sigmas). Returns (text, mean_sigma, sigstar_trace)."""
    shuf_sigmas = policy[1] if policy[0] == "shuf" else None
    g = torch.Generator(device="cpu"); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed_text.encode("utf-8"))], dtype=torch.long, device=device)
    out_bytes, sigmas, sigstar_trace = [], [], []
    kind = policy[0]
    logT = math.log(0.7)   # controllers start from baseline temp
    model.eval()
    with torch.no_grad():
        for step in range(max_new):
            raw = model(idx[:, -BLOCK:])[0, -1].float()
            if kind == "fixed_temp":
                T = policy[1]
                probs = F.softmax(_topk_mask(raw / T, TOP_K), dim=-1)
                sigmas.append(_entropy_eff(probs))
                nb = int(torch.multinomial(probs.cpu(), 1, generator=g).item())
            else:
                if kind == "fixed_sigma":
                    sig_target = policy[1]
                elif kind == "adaptive":
                    txt_so_far = bytes(out_bytes).decode("utf-8", "ignore")
                    sig_target, _ = _adapt_sigma(out_bytes, txt_so_far)
                else:  # shuf — pre-permuted σ*_t sequence, decoupled from state
                    sig_target = shuf_sigmas[step] if step < len(shuf_sigmas) else SIGMA_STAR_0
                sigstar_trace.append(sig_target)
                probs, achieved, logT = _drive_T_to_sigma(raw, logT, sig_target)
                sigmas.append(achieved)
                nb = int(torch.multinomial(probs.cpu(), 1, generator=g).item())
            out_bytes.append(nb)
            idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
            if any(st in bytes(out_bytes).decode("utf-8", "ignore") for st in STOPS):
                break
    t = bytes(out_bytes).decode("utf-8", "ignore")
    for st in STOPS:
        i = t.find(st)
        if i >= 0: t = t[:i]
    return t.strip(), (sum(sigmas)/len(sigmas) if sigmas else 0.0), sigstar_trace


def score_policy(model, policy, seed_rng, device, corpus_paths, kwr_floor=0.50,
                 jaccard_distinct=0.25, capture_adaptive_traces=None):
    """Run the FROZEN gauge battery on one decode policy. Returns metric dict.
    If capture_adaptive_traces is a list and policy is adaptive, append each gen's
    σ*_t trace so a matched shuf arm can replay the same distribution."""
    sig_all, all_sigstar = [], []
    def run(seed_text):
        t, s, trace = _decode(model, seed_text, policy, seed_rng, device)
        sig_all.append(s)
        if capture_adaptive_traces is not None: capture_adaptive_traces.append(trace)
        all_sigstar.extend(trace)
        return t

    comp_seed = ". ".join(c for c, _ in G.CONCEPTS) + ". "
    comp_out = run(comp_seed)
    g1 = len(G._coverage(comp_out))

    g2_texts = [comp_out]
    for c, _ in G.CONCEPTS[:3]:
        g2_texts.append(run(c + ". "))
    all_grams, kwrs = set(), []
    for t in g2_texts:
        k = G.known_word_ratio(t); kwrs.append(k)
        if k >= kwr_floor: all_grams |= G._content_ngrams(t)
    if corpus_paths and all_grams:
        n_novel = sum(1 for gr in all_grams if G._corpus_absent(gr, corpus_paths))
        g2_rate = round(n_novel / len(all_grams), 5)
    else:
        g2_rate = 0.0 if not all_grams else None

    idea_sets = []
    for s_seed in G.IDEATION_SEEDS:
        o = run(s_seed)
        kwrs.append(G.known_word_ratio(o))
        if G.known_word_ratio(o) >= kwr_floor:
            ws = set(G._words(o))
            if ws: idea_sets.append(ws)
    kept = []
    for ws in idea_sets:
        if all(G._jaccard(ws, k) <= jaccard_distinct for k in kept): kept.append(ws)
    g6_count = len(kept)

    return {
        "g1_composed_distinct": g1, "g6_count": g6_count,
        "kwr_mean": round(sum(kwrs)/len(kwrs), 4) if kwrs else 0.0,
        "g2_novelty_rate": g2_rate,
        "sigma_mean": round(sum(sig_all)/len(sig_all), 4) if sig_all else 0.0,
        "sigstar_min": round(min(all_sigstar), 4) if all_sigstar else None,
        "sigstar_max": round(max(all_sigstar), 4) if all_sigstar else None,
        "_sigstar_pool": all_sigstar,
    }


def combined_M(r):
    """FROZEN combined ideation metric M = G1 + G6 + 4*(kwr-0.50)_+."""
    return r["g1_composed_distinct"] + r["g6_count"] + 4.0 * max(0.0, r["kwr_mean"] - 0.50)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=CKPT_DEFAULT)
    ap.add_argument("--corpus", nargs="+", default=[CORPUS_DEFAULT])
    ap.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 23])
    ap.add_argument("--tune-seed", type=int, default=5)
    ap.add_argument("--out", default=os.path.join(ROOT, ".verdicts",
                    "1284_neuromodulation_gain", "H_1284_R2.txt"))
    a = ap.parse_args()
    t0 = time.time(); device = "cpu"
    MARGIN = 0.30

    print("=" * 92)
    print("H_1284 R2 — CONTEXT-ADAPTIVE NEUROMODULATION ON IDEATION/DECODE (re-scope, c15)")
    print(f"  combined metric M = G1 composed_distinct + G6 count + 4*(kwr-0.50)+   MARGIN={MARGIN}")
    print(f"  ARM A=best-fixed (grid temp{GRID_FIXED_TEMP}+σ*{GRID_FIXED_SIGMA}, tune-seed={a.tune_seed})")
    print(f"  ARM B=context-adaptive σ*_t (kR={kR} kN={kN} kC={kC} W={W_WIN} floor={COH_FLOOR})")
    print(f"  ARM C-SHUF=B's σ*_t permuted (coupling control)")
    print(f"  ckpt={a.ckpt}  seeds={a.seeds}", flush=True)
    print("=" * 92, flush=True)

    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False)
    model = ByteGPT(**ck["config"])
    model.load_state_dict({k: v.float() for k, v in ck["model"].items()}); model.eval()
    print(f"loaded 303M ByteGPT: {sum(p.numel() for p in model.parameters())/1e6:.2f}M params\n", flush=True)

    # ── ARM A: tune best-fixed on DISJOINT tune seed by M ──
    print("── tuning ARM A (best-fixed) on disjoint tune-seed", a.tune_seed, "──", flush=True)
    grid = [("fixed_temp", T) for T in GRID_FIXED_TEMP] + \
           [("fixed_sigma", s) for s in GRID_FIXED_SIGMA]
    tune = []
    for pol in grid:
        r = score_policy(model, pol, a.tune_seed, device, a.corpus)
        m = combined_M(r)
        tune.append((m, pol, r))
        print(f"   {pol[0]:12s} {pol[1]:<4}  M={m:.3f}  G1={r['g1_composed_distinct']} "
              f"G6={r['g6_count']} kwr={r['kwr_mean']:.3f} σ̄={r['sigma_mean']:.3f}", flush=True)
    tune.sort(key=lambda x: -x[0])
    best_M, best_pol, _ = tune[0]
    print(f"   => ARM A (best-fixed) = {best_pol[0]} {best_pol[1]}  (tune-M={best_M:.3f})\n", flush=True)

    # ── score A / B / C-SHUF over the scoring seeds ──
    per = {"A_best_fixed": [], "B_adaptive": [], "C_shuf": []}
    for sd in a.seeds:
        print(f"── seed {sd} ──", flush=True)
        rA = score_policy(model, best_pol, sd, device, a.corpus)
        # B adaptive — capture per-gen σ*_t traces to replay (permuted) in C-SHUF
        traces = []
        rB = score_policy(model, ("adaptive", None), sd, device, a.corpus,
                          capture_adaptive_traces=traces)
        # C-SHUF — same σ* DISTRIBUTION, decoupled from state (permute the whole pool)
        rng = random.Random(sd * 1000 + 7)
        pool = list(rB["_sigstar_pool"]); rng.shuffle(pool)
        # replay one long permuted sequence across the same gen battery
        rC = score_policy(model, ("shuf", pool), sd, device, a.corpus)
        for name, r in [("A_best_fixed", rA), ("B_adaptive", rB), ("C_shuf", rC)]:
            per[name].append(r)
            print(f"  {name:13s} M={combined_M(r):.3f}  composed_distinct={r['g1_composed_distinct']} "
                  f"g6={r['g6_count']} kwr={r['kwr_mean']:.3f} g2={r['g2_novelty_rate']} "
                  f"σ̄={r['sigma_mean']:.3f} σ*∈[{r['sigstar_min']},{r['sigstar_max']}]", flush=True)

    def agg(name, key):
        vals = [r[key] for r in per[name] if r.get(key) is not None]
        return (sum(vals)/len(vals)) if vals else 0.0
    def aggM(name):
        return sum(combined_M(r) for r in per[name]) / len(per[name])

    summ = {name: {
        "M": round(aggM(name), 4),
        "composed_distinct": round(agg(name, "g1_composed_distinct"), 4),
        "g6_count": round(agg(name, "g6_count"), 4),
        "kwr_mean": round(agg(name, "kwr_mean"), 4),
        "g2_novelty_rate": round(agg(name, "g2_novelty_rate"), 5),
        "sigma_mean": round(agg(name, "sigma_mean"), 4),
    } for name in per}
    A, B, C = summ["A_best_fixed"], summ["B_adaptive"], summ["C_shuf"]

    # ── FROZEN falsifier ──
    b_beats_a       = B["M"] >= A["M"] + MARGIN
    b_coh_ok        = B["kwr_mean"] >= A["kwr_mean"] - 0.02
    coupling_sep    = C["M"] < A["M"] + MARGIN
    b_above_a       = B["M"] > A["M"] + 1e-9
    green   = bool(b_beats_a and b_coh_ok and coupling_sep)
    partial = bool((not green) and b_above_a and (
                   (not b_beats_a) or (b_beats_a and not coupling_sep) or
                   (b_beats_a and not b_coh_ok)))
    if green:
        tier = "🟢 GREEN"; depl = "🏁"
        ruling = ("context-adaptive neuromodulation BEATS the best-fixed decode point on the combined "
                  "ideation metric M by >= MARGIN at no coherence collapse, and the lift is COUPLING "
                  "(C-SHUF separated) — the neuromodulatory lever LIVES on the generation/ideation lane "
                  "(R1 RED was memory-substrate specific). r3 = engine-native adaptive controller on decode.")
    elif partial:
        tier = "🟠 PARTIAL"; depl = "🧱"
        ruling = ("context-adaptive neuromodulation HELPS ideation (M(B)>M(A)) but does NOT clear MARGIN, "
                  "OR the lift is knob-VARIETY not state-COUPLING (C-SHUF ≈ B), OR it loses coherence — "
                  "the adaptive controller is at best a sub-margin / variety effect over best-fixed.")
    else:
        tier = "🔴 RED"; depl = "🧱"
        ruling = ("context-adaptive neuromodulation is INERT-or-WORSE than best-fixed on IDEATION too "
                  "(M(B) <= M(A)) — NO FREE LUNCH is GENERAL: a single well-tuned fixed decode point "
                  "dominates the state-driven controller on generation just as on memory (R1). "
                  "Neuromodulation inert everywhere; depletion 🧱, no r3.")

    verdict = {
        "H": "H_1284_R2", "round": 2,
        "title": "context-adaptive neuromodulation on the ideation/decode lane (re-scope of R1)",
        "lens": "neuromodulation (DA gain / NE exploration / ACh novelty) as a per-step decode σ*-target controller, c15, a_no_llm_frame_trap",
        "combined_metric_M": "composed_distinct(G1) + g6_count(G6) + 4*(kwr_mean-0.50)_+",
        "MARGIN": MARGIN,
        "arm_A_best_fixed_config": {"kind": best_pol[0], "value": best_pol[1], "tune_M": round(best_M, 4),
                                    "tune_seed": a.tune_seed, "grid": [list(p) for p in grid]},
        "controller_gains": {"kR": kR, "kN": kN, "kC": kC, "W": W_WIN, "COH_FLOOR": COH_FLOOR,
                             "sigma_star_0": SIGMA_STAR_0, "sigstar_clamp": [SIG_LO, SIG_HI], "KP": KP},
        "arms": summ, "seeds": a.seeds,
        "frozen_falsifier": {
            "M(B)>=M(A)+MARGIN": bool(b_beats_a),
            "kwr(B)>=kwr(A)-0.02": bool(b_coh_ok),
            "M(C-SHUF)<M(A)+MARGIN (coupling)": bool(coupling_sep),
            "M(B)>M(A)": bool(b_above_a),
            "deltas": {"M(B)-M(A)": round(B["M"]-A["M"], 4),
                       "M(C)-M(A)": round(C["M"]-A["M"], 4)},
        },
        "controller_swung": {  # proof the adaptive knob is alive (not a dead controller)
            "B_sigstar_range_per_seed": [[r["sigstar_min"], r["sigstar_max"]] for r in per["B_adaptive"]],
        },
        "supported": green, "tier": tier, "depletion": depl, "ruling": ruling,
        "scope": ("303M torch ref (byte-exact H_1157 mount), data/corpus.txt (orig 1.5GB GONE => G2 "
                  "UPPER BOUND), %d scoring seeds + 1 disjoint tune seed, single-model toy — "
                  "a_scale_honest_scope. DIRECTIONAL (a_engine_native_learning, engine-transfer "
                  "UNVERIFIED). CORE/*.hexa + H_1228 UNTOUCHED. Controller is no-grad readout, NEVER "
                  "folded into a loss (p7). Frozen bars NOT moved." % len(a.seeds)),
        "wall_s": round(time.time() - t0, 1),
    }
    print("\n=== SUMMARY (seed-averaged) ===")
    for name in per:
        s = summ[name]
        print(f"  {name:13s} M={s['M']:.3f}  composed_distinct={s['composed_distinct']:.3f} "
              f"g6={s['g6_count']:.3f} kwr={s['kwr_mean']:.4f} g2={s['g2_novelty_rate']} σ̄={s['sigma_mean']:.3f}")
    print(f"\n  M(B)-M(A) = {B['M']-A['M']:+.4f}   M(C-SHUF)-M(A) = {C['M']-A['M']:+.4f}   MARGIN={MARGIN}")
    print(f"\n=== VERDICT {tier}  {depl} ===")
    print(ruling)
    print(json.dumps({k: v for k, v in verdict.items() if k != "_"}, ensure_ascii=False, indent=2), flush=True)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("H_1284 R2 — CONTEXT-ADAPTIVE NEUROMODULATION ON IDEATION/DECODE (re-scope of R1)\n")
        f.write("=" * 92 + "\n")
        f.write(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n")
    print(f"\n[wrote] {a.out}\n[done]", flush=True)


if __name__ == "__main__":
    main()
