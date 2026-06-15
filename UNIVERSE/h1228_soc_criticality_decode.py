#!/usr/bin/env python3
"""
H_1228 — SELF-ORGANIZED CRITICALITY / EDGE-OF-CHAOS DECODE (HD18 from the foreign-
domain depth ladder, .verdicts/1226_foreign_domain_depth_lens/H_1226.txt).

PHYSICS / COMPLEX-SYSTEMS LENS, NOT AN LLM TRICK (c15). The hypothesis is borrowed
from self-organized criticality (sandpile avalanches, neuronal branching σ≈1, the
edge of chaos): rich emergent structure lives AT the critical point — between a
frozen sub-critical phase (every event dies out, σ<1) and a noisy super-critical
phase (events explode, σ>1). anima's Ψ=1/2 is itself a critical fixed point.

REFRAME OF THE DECODE FINDING (H_1218 greedy collapse composed_distinct=0 vs the
gauge_lib top-k40/temp0.7 sampling that yields 11-14 ideas, H_1158-family):
  · GREEDY (argmax, temp→0)        = SUB-CRITICAL — branching σ→1 effective byte,
                                      the generation freezes / loops (H_1218 collapse).
  · FIXED high-temp top-k sampling = SUPER-CRITICAL — branching σ large, the
                                      generation is creative but noisier.
  · DEPTH / ideation is at the EDGE — a per-step temperature TUNED to hold the
                                      next-byte branching at the critical σ*.

HYPOTHESIS: a criticality-TARGETED decode (controller adapts temperature each step
to drive the next-byte branching ratio toward a target σ*) should beat BOTH frozen
greedy AND fixed-temperature sampling — higher composed_distinct ideation at
equal-or-better coherence.

────────────────────────────────────────────────────────────────────────────────
THE BRANCHING / AVALANCHE PROXY  σ  (documented control law)
────────────────────────────────────────────────────────────────────────────────
At each decode step the model emits a next-byte distribution p (after temperature).
We measure a LOCAL AVALANCHE BRANCHING PROXY = the EFFECTIVE NUMBER OF VIABLE
NEXT-BYTES = the perplexity of the next-byte distribution:

        sigma_step = exp( H(p) ) ,  H(p) = -sum_i p_i log p_i      (nats)

This is the standard "effective support size" of a distribution and is exactly the
branching-factor reading SOC uses for an avalanche: sigma_step≈1 ⇒ one successor
(sub-critical / frozen, ≈ greedy); sigma_step large ⇒ many equally-viable
successors (super-critical / noisy). The CRITICAL EDGE is a small interior σ*
(barely-branching: a handful of viable continuations, the regime where the
generation neither freezes nor diffuses).

CONTROL LAW (per step, proportional temperature controller in log-temp):
  · target σ* (frozen below; achieved σ reported).
  · measure sigma_step at the current temperature.
  · to RAISE sigma we RAISE temperature, so the P-controller correction that should
    raise T is (log σ* - log σ_step):
        log T  <-  log T + KP * ( log sigma* - log sigma_step )
    clamp T to [T_MIN, T_MAX], re-evaluate the distribution at the updated T, sample
    from THAT. KP=0.6. This is a 1-step temperature lookahead.
  · top-k=40 cap is kept on arm C too (same admissible set as arm B) so the ONLY
    manipulated variable vs arm B is per-step temperature targeting σ* instead of
    a fixed temp.

ARMS (identical model, seeds, max_new, top-k; ONLY the temperature policy differs):
  (A) GREEDY            — argmax (σ→1, sub-critical). The H_1218 collapse baseline.
  (B) FIXED SAMPLING    — top-k40 temp0.7 (the H_1158 gauge_lib baseline VERBATIM).
  (C) CRITICALITY-TARGET— top-k40, per-step temp driven to σ* by the controller.

SCORING — FROZEN gauge_lib.py evaluators VERBATIM (p7, no metric re-invention):
  G._coverage          → G1 composed_distinct
  G._content_ngrams + G._corpus_absent over data/corpus.txt → G2 corpus-absence novelty
  G.known_word_ratio   → G0 kwr coherence
  G._words + G._jaccard→ G6 ideation distinct-idea count (H_1158 locked spec)
  ideation seeds = gauge_lib.IDEATION_SEEDS VERBATIM; concept seeds = gauge_lib.CONCEPTS.

────────────────────────────────────────────────────────────────────────────────
PRE-REGISTERED FALSIFIER (frozen BEFORE scoring — see H_1228_FREEZE.txt):
  Primary ideation metric = composed_distinct (G1) averaged over seeds, plus the
  G6 distinct-idea count. Coherence = mean kwr over the scored generations.
  GREEN   iff  C.composed_distinct >= B.composed_distinct  AND  C.kwr >= B.kwr
               (the critical edge MATCHES-OR-BEATS fixed sampling while staying
               coherent) AND clearly beats greedy (C.composed_distinct > A).
  🟠 PARTIAL iff C beats greedy and lands strictly between greedy (A) and sampling
               (B), OR matches/exceeds B ideation but loses coherence — criticality
               helps but is not the full lever.
  🔴 RED   iff C does not beat greedy, OR C < B on ideation without a coherence win.
  Report the σ* target and the ACHIEVED mean σ for arm C.
  Scope: 303M torch ref (byte-exact to the H_1157 mount), data/corpus.txt corpus
  (the original 1.5GB broad corpus is ephemeral/GONE ⇒ G2 novelty is an UPPER
  BOUND, flagged), >=3 seeds, toy/single-model — a_scale_honest_scope.
────────────────────────────────────────────────────────────────────────────────
$0 summer / CPU. Does NOT edit CORE/bytegpt_decode.hexa (another agent owns it) —
this is a numpy/torch-ref decode harness only (allowed).
"""
import os, sys, json, math, time, argparse
import torch, torch.nn as nn, torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gauge_lib as G   # FROZEN evaluators (VERBATIM)

# ckpt is gitignored/local-only — default to the shared main checkout's copy.
CKPT_DEFAULT   = os.environ.get("H1228_CKPT",
    "/Users/mini/dancinlab/anima/state/chat_303m/h1129c_chat.pt")
CORPUS_DEFAULT = os.path.join(ROOT, "data", "corpus.txt")

# ── ByteGPT (VERBATIM from scripts/scratch/h1218/torch_greedy_baseline.py) ──────
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

# ── decode config ──────────────────────────────────────────────────────────────
BLOCK   = 512
TOP_K   = 40
TEMP_B  = 0.7          # fixed-sampling baseline (arm B), gauge_lib default VERBATIM
SIGMA_STAR = 2.5       # FROZEN target: ~2.5 viable next-bytes = the barely-branching
                        # critical edge (interior between greedy σ→1 and the broad
                        # super-critical σ of unrestrained sampling). Reported + achieved.
KP      = 0.6          # P-controller gain in log-temp
T_MIN, T_MAX = 0.05, 3.0
MAX_NEW = 96
STOPS = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]


def _topk_mask(logits, k):
    if not k:
        return logits
    v, _ = torch.topk(logits, min(k, logits.shape[-1]))
    return logits.masked_fill(logits < v[-1], float("-inf"))


def _entropy_eff(probs):
    """effective number of viable next-bytes = exp(H(p)) (avalanche branching σ)."""
    p = probs[probs > 0]
    H = float(-(p * p.log()).sum().item())
    return math.exp(H)


def _decode_arm(model, seed_text, arm, seed_rng, device, max_new=MAX_NEW):
    """arm ∈ {'greedy','fixed','crit'}. Returns (text, mean_sigma)."""
    g = torch.Generator(device="cpu"); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed_text.encode("utf-8"))], dtype=torch.long, device=device)
    out_bytes, sigmas = [], []
    logT = math.log(TEMP_B)   # arm C starts from the baseline temp, then adapts
    model.eval()
    with torch.no_grad():
        for _ in range(max_new):
            ctx = idx[:, -BLOCK:]
            raw = model(ctx)[0, -1].float()          # (V,)
            if arm == "greedy":
                nb = int(raw.argmax())
                probs = F.softmax(_topk_mask(raw.clone(), TOP_K), dim=-1)
                sigmas.append(_entropy_eff(probs))
            elif arm == "fixed":
                logits = _topk_mask(raw / TEMP_B, TOP_K)
                probs = F.softmax(logits, dim=-1).cpu()
                sigmas.append(_entropy_eff(probs))
                nb = int(torch.multinomial(probs, 1, generator=g).item())
            else:  # crit — adapt T toward SIGMA_STAR, then sample at the updated T
                T = math.exp(logT)
                logits = _topk_mask(raw / T, TOP_K)
                probs = F.softmax(logits, dim=-1)
                sig = _entropy_eff(probs)
                logT = min(math.log(T_MAX), max(math.log(T_MIN),
                            logT + KP * (math.log(SIGMA_STAR) - math.log(max(sig, 1e-9)))))
                T2 = math.exp(logT)
                logits2 = _topk_mask(raw / T2, TOP_K)
                probs2 = F.softmax(logits2, dim=-1)
                sigmas.append(_entropy_eff(probs2))
                nb = int(torch.multinomial(probs2.cpu(), 1, generator=g).item())
            out_bytes.append(nb)
            idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
            txt = bytes(out_bytes).decode("utf-8", "ignore")
            if any(st in txt for st in STOPS):
                break
    t = bytes(out_bytes).decode("utf-8", "ignore")
    for st in STOPS:
        i = t.find(st)
        if i >= 0:
            t = t[:i]
    return t.strip(), (sum(sigmas) / len(sigmas) if sigmas else 0.0)


# ── score one arm over the FROZEN gate seeds with gauge_lib VERBATIM ────────────
def score_arm(model, arm, seed_rng, device, corpus_paths, kwr_floor=0.50,
              jaccard_distinct=0.25):
    sig_all = []
    comp_seed = ". ".join(c for c, _ in G.CONCEPTS) + ". "
    comp_out, s = _decode_arm(model, comp_seed, arm, seed_rng, device); sig_all.append(s)
    g1 = len(G._coverage(comp_out))

    g2_texts = [comp_out]
    for c, _ in G.CONCEPTS[:3]:
        o, s = _decode_arm(model, c + ". ", arm, seed_rng, device); sig_all.append(s)
        g2_texts.append(o)
    all_grams, kwrs = set(), []
    for t in g2_texts:
        k = G.known_word_ratio(t); kwrs.append(k)
        if k >= kwr_floor:
            all_grams |= G._content_ngrams(t)
    if corpus_paths and all_grams:
        n_novel = sum(1 for gr in all_grams if G._corpus_absent(gr, corpus_paths))
        g2_rate = round(n_novel / len(all_grams), 5)
    else:
        g2_rate = 0.0 if not all_grams else None

    idea_sets = []
    for s_seed in G.IDEATION_SEEDS:
        o, s = _decode_arm(model, s_seed, arm, seed_rng, device); sig_all.append(s)
        if G.known_word_ratio(o) >= kwr_floor:
            ws = set(G._words(o))
            if ws:
                idea_sets.append(ws)
        kwrs.append(G.known_word_ratio(o))
    kept = []
    for ws in idea_sets:
        if all(G._jaccard(ws, k) <= jaccard_distinct for k in kept):
            kept.append(ws)
    g6_count = len(kept)
    if len(kept) >= 2:
        dists = [1.0 - G._jaccard(kept[i], kept[j])
                 for i in range(len(kept)) for j in range(i + 1, len(kept))]
        g6_jac = round(sum(dists) / len(dists), 5)
    else:
        g6_jac = None

    return {
        "g1_composed_distinct": g1,
        "g2_novelty_rate": g2_rate,
        "g6_count": g6_count,
        "g6_jaccard": g6_jac,
        "kwr_mean": round(sum(kwrs) / len(kwrs), 4) if kwrs else 0.0,
        "sigma_mean": round(sum(sig_all) / len(sig_all), 4) if sig_all else 0.0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=CKPT_DEFAULT)
    ap.add_argument("--corpus", nargs="+", default=[CORPUS_DEFAULT])
    ap.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 23])
    ap.add_argument("--out", default=os.path.join(ROOT, ".verdicts",
                    "1228_soc_criticality_decode", "H_1228.txt"))
    a = ap.parse_args()
    t0 = time.time()
    device = "cpu"

    print("=" * 92)
    print("H_1228 — SELF-ORGANIZED CRITICALITY / EDGE-OF-CHAOS DECODE (HD18, physics lens, c15)")
    print(f"  σ proxy = exp(H(next-byte p)) = effective viable next-bytes (avalanche branching)")
    print(f"  σ* target = {SIGMA_STAR}  KP={KP}  top-k={TOP_K}  T∈[{T_MIN},{T_MAX}]  max_new={MAX_NEW}")
    print(f"  arms: A=greedy(σ→1) · B=fixed top-k{TOP_K} temp{TEMP_B} · C=criticality-targeted")
    print(f"  ckpt={a.ckpt}  corpus={a.corpus}  seeds={a.seeds}")
    print("=" * 92, flush=True)

    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False)
    model = ByteGPT(**ck["config"])
    model.load_state_dict({k: v.float() for k, v in ck["model"].items()})
    model.eval()
    nparams = sum(p.numel() for p in model.parameters())
    print(f"loaded 303M ByteGPT: {nparams/1e6:.2f}M params, config={ck['config']}\n", flush=True)

    arms = {"A_greedy": "greedy", "B_fixed_sampling": "fixed", "C_criticality": "crit"}
    per_seed = {name: [] for name in arms}
    for sd in a.seeds:
        print(f"── seed {sd} ──", flush=True)
        for name, arm in arms.items():
            r = score_arm(model, arm, sd, device, a.corpus)
            per_seed[name].append(r)
            print(f"  {name:18s}  composed_distinct={r['g1_composed_distinct']}  "
                  f"g6_count={r['g6_count']}  kwr={r['kwr_mean']:.3f}  "
                  f"g2_novel={r['g2_novelty_rate']}  σ̄={r['sigma_mean']:.3f}", flush=True)

    def agg(name, key):
        vals = [r[key] for r in per_seed[name] if r[key] is not None]
        return (sum(vals) / len(vals)) if vals else 0.0

    summ = {name: {
        "composed_distinct": round(agg(name, "g1_composed_distinct"), 4),
        "g6_count": round(agg(name, "g6_count"), 4),
        "kwr_mean": round(agg(name, "kwr_mean"), 4),
        "g2_novelty_rate": round(agg(name, "g2_novelty_rate"), 5),
        "sigma_mean": round(agg(name, "sigma_mean"), 4),
    } for name in arms}

    A, B, C = summ["A_greedy"], summ["B_fixed_sampling"], summ["C_criticality"]

    # ── FROZEN falsifier evaluation ──
    c_ge_b_ideation = C["composed_distinct"] >= B["composed_distinct"]
    c_ge_b_coh      = C["kwr_mean"] >= B["kwr_mean"]
    c_beats_greedy  = C["composed_distinct"] > A["composed_distinct"] + 1e-9
    green   = bool(c_ge_b_ideation and c_ge_b_coh and c_beats_greedy)
    c_interior = (A["composed_distinct"] < C["composed_distinct"] < B["composed_distinct"])
    partial = bool((not green) and c_beats_greedy and (c_interior or
                   (c_ge_b_ideation and not c_ge_b_coh)))
    if green:
        tier, ruling = "🟢 GREEN", ("criticality-targeted decode MATCHES-OR-BEATS fixed sampling "
            "ideation at equal-or-better coherence AND beats greedy — the Ψ=1/2 critical edge IS the "
            "ideation lever (HD18 SUPPORTED on the 303M ref)")
    elif partial:
        tier, ruling = "🟠 PARTIAL", ("criticality decode beats greedy and lands between greedy and "
            "fixed sampling (or matches ideation but loses coherence) — the critical edge HELPS but is "
            "NOT the full ideation lever (HD18 partial)")
    else:
        tier, ruling = "🔴 RED", ("criticality-targeted decode does NOT clear the bar (fails to beat "
            "greedy, or loses to fixed sampling on ideation without a coherence win) — targeting the "
            "branching σ* is NOT the ideation lever at this scale (HD18 closed-negative, a_paper_negative_ok)")

    verdict = {
        "H": "H_1228",
        "title": "self-organized criticality / edge-of-chaos decode (HD18, physics lens)",
        "lens": "self-organized criticality / branching σ≈1 (sandpile/neuronal avalanche), NOT an LLM trick (c15)",
        "sigma_proxy": "exp(H(next-byte distribution)) = effective number of viable next-bytes (avalanche branching factor)",
        "sigma_star_target": SIGMA_STAR,
        "control_law": "log T <- log T + KP*(log σ* - log σ_step), clamp T∈[%.2f,%.2f], KP=%.2f, top-k=%d kept on C (same admissible set as B)" % (T_MIN, T_MAX, KP, TOP_K),
        "arms": summ,
        "seeds": a.seeds,
        "achieved_sigma_C": C["sigma_mean"],
        "achieved_sigma_A_greedy": A["sigma_mean"],
        "achieved_sigma_B_fixed": B["sigma_mean"],
        "frozen_falsifier": {
            "C_composed_distinct_ge_B": bool(c_ge_b_ideation),
            "C_kwr_ge_B": bool(c_ge_b_coh),
            "C_beats_greedy_A": bool(c_beats_greedy),
            "C_interior(A<C<B)": bool(c_interior),
        },
        "supported": green,
        "tier": tier,
        "ruling": ruling,
        "psi_critical_edge_is_ideation_lever": green,
        "scope": ("303M torch ref (byte-exact to H_1157 mount), data/corpus.txt corpus (original 1.5GB "
                  "broad corpus ephemeral/GONE ⇒ G2 novelty is an UPPER BOUND, flagged), %d seeds, "
                  "single-model toy — a_scale_honest_scope; frozen bars NOT moved" % len(a.seeds)),
        "wall_s": round(time.time() - t0, 1),
    }
    print("\n=== SUMMARY (seed-averaged) ===")
    for name in arms:
        s = summ[name]
        print(f"  {name:18s}  composed_distinct={s['composed_distinct']:.3f}  "
              f"g6_count={s['g6_count']:.3f}  kwr={s['kwr_mean']:.4f}  "
              f"g2_novel={s['g2_novelty_rate']}  σ̄={s['sigma_mean']:.3f}")
    print(f"\nσ* target = {SIGMA_STAR}  | achieved σ̄: A(greedy)={A['sigma_mean']:.3f}  "
          f"B(fixed)={B['sigma_mean']:.3f}  C(crit)={C['sigma_mean']:.3f}")
    print(f"\n=== VERDICT {tier} ===")
    print(ruling)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("H_1228 — SELF-ORGANIZED CRITICALITY / EDGE-OF-CHAOS DECODE (HD18, physics lens, c15)\n")
        f.write("=" * 92 + "\n")
        f.write(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n")
    print(f"\n[wrote] {a.out}", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
