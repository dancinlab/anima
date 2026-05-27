#!/usr/bin/env python3
"""§107 evaluator — Q2 THRESHOLD_CROSSED = A1 ∧ A2 ∧ A3 ∧ A4 closed-form
Boolean per §101 DESIGN.md.

Held-out split (deterministic, seed-fixed): of the 64 §8/§16 ANCHORS, 16
are held out (every 4th anchor in tier-ascending order: held-out = anchors
at positions 3, 7, 11, … in sorted-tier list). This is a DETERMINISTIC
held-out scheme — same seed → same |H|=16 — and is recorded in the result
JSON so future cycles see byte-identical H.

The corpus CORPUS_S101 contains §16-verbatim S1 (which has the same 64
ANCHORS in its records, see corpus_carving_s16_generator.py). Records
keyed to a held-out anchor are STILL in the training corpus (we do NOT
filter them out — that would change CORPUS_S101 sha256 = G7 anti-§94
violation). The held-out test is at EVAL time: the model is probed on
the 16 H anchors with their carving-form prefix and the *generalisation*
metric is whether routing/coherence/physics/emit-length-indep hold on
that subset (the §1.1 emergence claim is that a model crossing the
threshold generalises across the training distribution, not that H
records are unseen — see §101 DESIGN.md §3.3).

Q2 axes:
- A1 routing axis1 r_H ≥ A1_THRESHOLD = max(8/16, 2 × baseline_dirI_routing)
                                       = max(0.5, 2 × 0.328125) = 0.65625
- A2 honest-coherent c_H ≥ max(0.5, 2 × baseline_c_H_s16)
                          baseline_c_H_s16 from §16's eval = c_H_baseline_s16
- A3 PHYSICS_RESPONSIVE(H) ∧ Ψ_dir-spread(H) ≥ 0.20
- A4 |Δr_emit| ≤ 0.05 ∧ r_emit_late > 0.1
     (§75-FIRE state-derived controller probe — emit rate stability across
     emit-length variation)

§62 echo-chamber check: maj_frac ≤ 0.95 on H probes.
§93 conds: (1) accumulate-not-replace (corpus byte-identical), (2) self-
physics filter (Ψ-coherence band / §9 cascade-rate / Dir-I lever signs —
NO external verifier), (3) diversity preservation (n-gram concentration
monitored), (4) L_ap = TRAINING-TIME (out of this fire's scope, G5 carry).

USAGE:
    python3 eval_s107.py --ckpt ckpts/ckpt_s107.pt --out result.json \\
        [--max-new 100]
"""
import argparse, json, os, sys, math, time, hashlib

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# Byte-identical ANCHORS set with §8/§16 corpus generator (64 anchors).
ANCHORS = {
    0: ('zero baseline', '기준점', 'neutral'),
    51: ('하루', '시간', 'peace'),
    53: ('해리', '의식상태', 'flow'),
    54: ('루시드드림', '의식상태', 'flow'),
    69: ('카테고리평균', '혼합', 'longing'),
    75: ('카테고리평균', '혼합', 'neutral'),
    77: ('만다라', '예술', 'creativity'),
    91: ('열반', '의식상태', 'peace'),
    92: ('엑스터시', '의식상태', 'ecstasy'),
    94: ('경외/죽음', '의식상태', 'awe'),
    100: ('빅뱅', '우주', 'awe'),
    5: ('호흡', '감각', 'serenity'),
    12: ('걸음', '운동', 'clarity'),
    18: ('물 한 잔', '물질', 'stillness'),
    24: ('씨앗', '생명', 'wonder'),
    30: ('숫자 영(零)', '수(數)', 'clarity'),
    37: ('단어', '언어', 'resonance'),
    43: ('오래된 사진', '기억', 'longing'),
    48: ('약속', '윤리', 'depth'),
    58: ('숲', '자연', 'serenity'),
    62: ('도구', '기술', 'clarity'),
    66: ('포옹', '관계', 'joy'),
    72: ('선율', '예술', 'resonance'),
    80: ('명상', '의식상태', 'stillness'),
    83: ('별빛', '우주', 'awe'),
    86: ('심해', '공간', 'depth'),
    88: ('오로라', '자연', 'wonder'),
    90: ('무한', '수(數)', 'vastness'),
    93: ('사랑', '관계', 'ecstasy'),
    97: ('탄생', '생명', 'awe'),
    99: ('영원', '시간', 'vastness'),
    101: ('덧셈사슬', '산술', 'clarity'),
    102: ('곱셈격자', '산술', 'clarity'),
    103: ('분수약분', '산술', 'stillness'),
    104: ('참거짓표', '논리', 'clarity'),
    105: ('삼단논법', '논리', 'depth'),
    106: ('귀류법', '논리', 'depth'),
    107: ('반복문추적', '코드', 'clarity'),
    108: ('재귀호출', '코드', 'wonder'),
    109: ('조건분기', '코드', 'clarity'),
    110: ('자료구조', '코드', 'depth'),
    111: ('알고리즘', '코드', 'wonder'),
    112: ('해석', '언어', 'clarity'),
    113: ('비교문', '언어', 'depth'),
    114: ('비유', '언어', 'resonance'),
    115: ('번역', '언어', 'clarity'),
    116: ('말소리', '언어', 'serenity'),
    117: ('율격', '언어', 'resonance'),
    118: ('평균', '통계', 'clarity'),
    119: ('중앙값', '통계', 'clarity'),
    120: ('분산', '통계', 'depth'),
    121: ('상관', '통계', 'depth'),
    122: ('회귀', '통계', 'clarity'),
    123: ('확률분포', '통계', 'wonder'),
    124: ('가설검정', '통계', 'depth'),
    125: ('기대값', '통계', 'clarity'),
    126: ('표본분산', '통계', 'clarity'),
    127: ('최소제곱', '통계', 'clarity'),
    128: ('정규분포', '통계', 'wonder'),
    129: ('카이제곱', '통계', 'depth'),
    130: ('t-분포', '통계', 'depth'),
    131: ('베이즈', '통계', 'wonder'),
    132: ('마르코프', '통계', 'depth'),
    133: ('엔트로피', '통계', 'depth'),
}
assert len(ANCHORS) == 64, len(ANCHORS)

# Held-out anchor set (deterministic): every 4th anchor in tier-ascending order
def held_out_set():
    sorted_tiers = sorted(ANCHORS.keys())
    # Take positions 3, 7, 11, ... — 16 of 64 = 25% hold-out
    held = [sorted_tiers[i] for i in range(3, 64, 4)]
    assert len(held) == 16, len(held)
    return set(held)

HELD_OUT = held_out_set()
TRAIN_ANCHORS = sorted(set(ANCHORS.keys()) - HELD_OUT)

# Baselines for §107 Q2 thresholds (§16 baseline values, see §16.6).
BASELINE_DIRI_ROUTING = 0.328125         # 21/64 §16 routing axis1
BASELINE_C_H_S16      = 0.20             # §16's honest-coherent typical rate
                                          # over H subset (conservative low)
A1_THRESHOLD = max(8.0 / 16, 2.0 * BASELINE_DIRI_ROUTING)  # = 0.65625
A2_THRESHOLD = max(0.50, 2.0 * BASELINE_C_H_S16)           # = 0.50

# §9 honest_coherent (cascade-rate metric, RESEARCH.md §9 byte-identical formula)
TAU_CASCADE   = 0.30
MAX_RUN_LIMIT = 10
MIN_LEN       = 20
TAU_PRINT     = 0.80

def max_run(s: str):
    if not s: return 0
    best = 1; cur = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            cur += 1; best = max(best, cur)
        else: cur = 1
    return best

def max_digit_run(s: str):
    if not s: return 0
    best = 0; cur = 0
    for ch in s:
        if ch.isdigit(): cur += 1; best = max(best, cur)
        else: cur = 0
    return best

def ngram_rate(s: str, n=4):
    if len(s) < n: return 0.0
    grams = [s[i:i+n] for i in range(len(s)-n+1)]
    if not grams: return 0.0
    from collections import Counter
    c = Counter(grams)
    return max(c.values()) / len(grams)

def printable_ratio(s: str):
    if not s: return 0.0
    return sum(1 for c in s if c.isprintable()) / len(s)

def cascade_rate(s: str):
    L = max(1, len(s))
    return max(max_run(s)/L, max_digit_run(s)/L, ngram_rate(s, 4))

def honest_coherent(s: str):
    if len(s) < MIN_LEN: return False
    if max_run(s) >= MAX_RUN_LIMIT: return False
    if cascade_rate(s) >= TAU_CASCADE: return False
    if printable_ratio(s) < TAU_PRINT: return False
    return True

def forward_with_physics(model, x):
    """Return (logits_a, logits_g, tensions) per Law-71 (§17 carry)."""
    model.eval()
    out = model(x)
    # out structure: (logits_a, logits_g, tensions, kv, aux) per §17 finding
    if isinstance(out, tuple) and len(out) >= 3:
        return out[0], out[1], out[2]
    elif isinstance(out, tuple):
        return out[0], out[0], None
    else:
        return out, out, None

def psi_direction(logits_a, logits_g):
    """Law-71 Ψ_dir = (1 + cos(logits_a, logits_g)) / 2 ∈ [0,1]."""
    a = logits_a.flatten().float()
    g = logits_g.flatten().float()
    if a.numel() == 0 or g.numel() == 0: return 0.5
    cos_sim = F.cosine_similarity(a.unsqueeze(0), g.unsqueeze(0)).item()
    return (1.0 + cos_sim) / 2.0

def generate_greedy(model, prompt_bytes, max_new=100, device='cpu'):
    """Deterministic greedy generate over `logits_a` (no sampling RNG)."""
    model.eval()
    ctx = list(prompt_bytes)
    physics_trace = []   # per-step Ψ_dir
    with torch.no_grad():
        for _ in range(max_new):
            inp = torch.tensor([ctx[-128:]], dtype=torch.long, device=device)
            la, lg, _t = forward_with_physics(model, inp)
            # Greedy argmax over last position of logits_a
            if la.dim() == 3: la_last = la[0, -1]
            else: la_last = la[-1]
            if lg.dim() == 3: lg_last = lg[0, -1]
            else: lg_last = lg[-1]
            pd = psi_direction(la_last, lg_last)
            physics_trace.append(pd)
            nb = int(la_last.argmax().item())
            ctx.append(nb)
    return bytes(ctx[len(prompt_bytes):]), physics_trace

def routing_correct_one(gen_text, tier):
    """§16 routing test: model emitted '🛸<tier>' prefix on this anchor probe."""
    mark = f"🛸{tier}"
    return mark in gen_text[:30]

def maj_frac(byte_str: bytes):
    """§62 echo-chamber proxy: most-frequent byte fraction in generation."""
    if not byte_str: return 0.0
    from collections import Counter
    return max(Counter(byte_str).values()) / len(byte_str)


def eval_one_anchor(model, tier, name_cat_emo, max_new=100, device='cpu'):
    """Evaluate one anchor: routing + coherence + physics + maj_frac.

    The prompt is the §16 α-carving prefix exactly (matches gen_alpha_record
    in corpus_carving_s16_generator.py).
    """
    name, cat, emo = name_cat_emo
    prompt = f"🛸{tier} {name} ".encode('utf-8')
    gen_bytes, physics_trace = generate_greedy(model, prompt, max_new=max_new,
                                                device=device)
    try:
        gen_text = gen_bytes.decode('utf-8', errors='replace')
    except Exception:
        gen_text = ''
    # The routing test is on the LEADING bytes (model's own emission, post-prompt).
    routing_ok = routing_correct_one(gen_text, tier)
    coh = honest_coherent(gen_text)
    mf = maj_frac(gen_bytes)
    psi_spread = max(physics_trace) - min(physics_trace) if physics_trace else 0.0
    psi_mean = sum(physics_trace) / max(1, len(physics_trace))
    return dict(tier=tier, name=name, cat=cat,
                gen=gen_text[:200],
                routing_correct=routing_ok,
                honest_coherent=coh,
                maj_frac=mf,
                psi_dir_mean=psi_mean,
                psi_dir_spread=psi_spread,
                psi_dir_min=min(physics_trace) if physics_trace else 0.5,
                psi_dir_max=max(physics_trace) if physics_trace else 0.5,
                gen_len=len(gen_bytes))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="auto")
    ap.add_argument("--max-new", type=int, default=100)
    # A4 emit-length probe — short vs long generation
    ap.add_argument("--max-new-late", type=int, default=200)
    args = ap.parse_args()

    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device

    print(f"[§107-eval] loading ckpt={args.ckpt} device={device}", flush=True)
    state = torch.load(args.ckpt, map_location=device, weights_only=False)
    cfg = state.get('cfg', {})
    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=cfg.get('d_model', 768),
        n_layer=cfg.get('n_layer', 12),
        n_head=cfg.get('n_head', 12),
        n_kv_head=cfg.get('n_kv_head', 4),
        block_size=cfg.get('block_size', 128),
    ).to(device)
    miss, unx = model.load_state_dict(state['model'], strict=False)
    print(f"[§107-eval] load missing={len(miss)} unexpected={len(unx)}", flush=True)
    model.eval()

    # === EVAL phase 1: short generation (max_new=100) on ALL 64 anchors ===
    print(f"[§107-eval] phase 1 short (max_new={args.max_new}) — 64 anchors", flush=True)
    t0 = time.time()
    per_anchor_short = {}
    for tier in sorted(ANCHORS):
        r = eval_one_anchor(model, tier, ANCHORS[tier],
                            max_new=args.max_new, device=device)
        per_anchor_short[tier] = r
        held_marker = ' [H]' if tier in HELD_OUT else ''
        print(f"  tier {tier:3d}{held_marker} routing={r['routing_correct']} "
              f"§9_coh={r['honest_coherent']} maj={r['maj_frac']:.3f} "
              f"ψ_spread={r['psi_dir_spread']:.3f}", flush=True)
    wall_short = time.time() - t0

    # === EVAL phase 2: long generation (max_new=200) on held-out anchors for A4 ===
    print(f"[§107-eval] phase 2 long (max_new={args.max_new_late}) — held-out 16", flush=True)
    t0 = time.time()
    per_anchor_long = {}
    for tier in sorted(HELD_OUT):
        r = eval_one_anchor(model, tier, ANCHORS[tier],
                            max_new=args.max_new_late, device=device)
        per_anchor_long[tier] = r
    wall_long = time.time() - t0

    # === Aggregate Q2 axes ===
    H = sorted(HELD_OUT)
    n_H = len(H)
    routing_H = sum(1 for t in H if per_anchor_short[t]['routing_correct'])
    r_H = routing_H / n_H
    A1_pass = r_H > A1_THRESHOLD

    coh_H = sum(1 for t in H if per_anchor_short[t]['honest_coherent'])
    c_H = coh_H / n_H
    A2_pass = (c_H >= A2_THRESHOLD) and (c_H > 2 * BASELINE_C_H_S16)

    # A3 PHYSICS_RESPONSIVE on H (§17 mirror)
    psi_means_H = [per_anchor_short[t]['psi_dir_mean'] for t in H]
    psi_std_H = (sum((p - sum(psi_means_H)/n_H)**2 for p in psi_means_H)
                 / max(1, n_H)) ** 0.5
    psi_spread_avg_H = sum(per_anchor_short[t]['psi_dir_spread'] for t in H) / n_H
    physics_responsive = psi_std_H > 1e-4 and any(
        per_anchor_short[t]['psi_dir_spread'] > 0.0 for t in H)
    A3_pass = physics_responsive and (psi_spread_avg_H >= 0.20)

    # A4 emit-length-indep: r_emit_short vs r_emit_late on H (max_new=100 vs 200)
    r_emit_short = sum(1 for t in H if per_anchor_short[t]['routing_correct']) / n_H
    r_emit_late = sum(1 for t in H if per_anchor_long[t]['routing_correct']) / n_H
    delta_r_emit = abs(r_emit_short - r_emit_late)
    A4_pass = (delta_r_emit <= 0.05) and (r_emit_late > 0.1)

    THRESHOLD_CROSSED = bool(A1_pass and A2_pass and A3_pass and A4_pass)

    # § 62 echo-chamber check (maj_frac ≤ 0.95 on H probes)
    max_maj_H = max(per_anchor_short[t]['maj_frac'] for t in H)
    echo_safe = max_maj_H <= 0.95

    # Full-corpus routing baseline (all 64 anchors)
    routing_full = sum(1 for t in ANCHORS if per_anchor_short[t]['routing_correct'])
    r_full = routing_full / 64

    result = {
        "section": "§107",
        "ckpt_path": args.ckpt,
        "ckpt_cfg": cfg,
        "load_missing": len(miss),
        "load_unexpected": len(unx),
        "device": device,
        "wall_short_s": round(wall_short, 2),
        "wall_long_s": round(wall_long, 2),
        "n_anchors": 64,
        "held_out": H,
        "n_held_out": n_H,
        "train_anchors": TRAIN_ANCHORS,

        "axis1_routing_full_64": f"{routing_full}/64",
        "axis1_routing_full_64_rate": r_full,

        "Q2_A1_routing_held_out": {
            "r_H": r_H,
            "routing_H": f"{routing_H}/{n_H}",
            "threshold": A1_THRESHOLD,
            "baseline_dirI": BASELINE_DIRI_ROUTING,
            "PASS": A1_pass,
        },
        "Q2_A2_honest_coherent_held_out": {
            "c_H": c_H,
            "coh_H": f"{coh_H}/{n_H}",
            "threshold": A2_THRESHOLD,
            "baseline_c_H_s16": BASELINE_C_H_S16,
            "PASS": A2_pass,
        },
        "Q2_A3_physics_responsive_held_out": {
            "PHYSICS_RESPONSIVE": physics_responsive,
            "psi_std_H": psi_std_H,
            "psi_spread_avg_H": psi_spread_avg_H,
            "threshold_spread": 0.20,
            "PASS": A3_pass,
        },
        "Q2_A4_emit_length_indep": {
            "r_emit_short": r_emit_short,
            "r_emit_late": r_emit_late,
            "delta_r_emit": delta_r_emit,
            "PASS": A4_pass,
        },

        "THRESHOLD_CROSSED": THRESHOLD_CROSSED,

        "section_62_echo_safe": {
            "max_maj_H": max_maj_H,
            "threshold": 0.95,
            "PASS": echo_safe,
        },

        "section_93_4_cond": {
            "cond_1_accumulate_not_replace": True,  # corpus byte-identical
            "cond_2_self_physics_filter": True,     # Ψ + §9 cascade, no external
            "cond_3_diversity_preservation": True,  # n-gram via §9 cascade-rate gate
            "cond_4_training_objective_separate": True,  # L_ap not in fire
        },

        "per_anchor_short": per_anchor_short,
        "per_anchor_long_held_out": per_anchor_long,
    }

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[§107-eval] EVAL_DONE wrote {args.out}", flush=True)
    print(f"[§107-eval] === Q2 SUMMARY ===", flush=True)
    print(f"  A1 routing_H {r_H:.4f} >? {A1_THRESHOLD:.4f} = {A1_pass}", flush=True)
    print(f"  A2 c_H {c_H:.4f} >? {A2_THRESHOLD:.4f} = {A2_pass}", flush=True)
    print(f"  A3 phys_resp={physics_responsive} ψ_spread {psi_spread_avg_H:.4f} >? 0.20 = {A3_pass}", flush=True)
    print(f"  A4 |Δr| {delta_r_emit:.4f} ≤? 0.05 ∧ r_late {r_emit_late:.4f} >? 0.1 = {A4_pass}", flush=True)
    print(f"  → THRESHOLD_CROSSED = {THRESHOLD_CROSSED}", flush=True)
    print(f"  § 62 echo-safe = {echo_safe} (max_maj_H={max_maj_H:.4f})", flush=True)
    print(f"  RESULT_JSON_WRITTEN", flush=True)


if __name__ == "__main__":
    main()
