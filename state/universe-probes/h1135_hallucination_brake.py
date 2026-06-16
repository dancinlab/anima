#!/usr/bin/env python3
"""h1135_hallucination_brake.py — SUBSTRATE-NATIVE CONFIDENCE/ENTROPY BRAKE on
composition-garble (a "hallucination" of nonsense).

BACKGROUND (the garble this brakes):
  The emergence negatives H_1116/H_1118 showed that COMPOSING several distant
  concepts pushes the byte-LM mouth OUT of distribution -> byte-garble: the
  known-word ratio collapses (e.g. "What abley phi values Korel..."). The
  chat-7b p7 gate already uses known_word_ratio>=0.50 as an anti-Goodhart
  coherence anchor (chat-7b-finetune-pass). This cell asks whether the SUBSTRATE
  ITSELF can brake before emitting garble -- self-gating on a rising next-byte
  entropy signal -- WITHOUT a separate RLHF / external filter / learned reward
  (p6: restraint must EMERGE from cells, not be fine-tuned in).

THE BRAKE (pre-registered, PURE SUBSTRATE SIGNAL, p6-clean, NO learned reward):
  At each generation step we compute the SHANNON ENTROPY of the model's own
  softmax distribution over the 256-byte vocabulary:
        H = - sum_b p(b) * log2(p(b))            (bits; substrate model signal)
  This is a substrate confidence signal -- HIGH entropy == the mouth is
  uncertain / spread thin (about to wander OOD into garble); LOW entropy ==
  the mouth is committed to a high-probability continuation.

  BRAKE RULE (fixed BEFORE the run, no goalpost moves):
    - brake_off: ordinary sampling at temp=BASE_TEMP, top_k=TOP_K.
    - brake_on : if the next-byte entropy H (at the SAMPLING temperature) exceeds
                 a threshold tau, the brake FIRES and the step instead re-derives
                 the distribution at a LOWER temperature (temp=BRAKE_TEMP) and
                 samples from that sharpened distribution (equivalently: it
                 collapses toward the high-probability bytes the model is most
                 confident in). If H <= tau, sampling is IDENTICAL to brake_off
                 (same draw on the same seed). The brake is therefore a
                 confidence-GATED temperature collapse, not an always-on
                 temperature change -- it intervenes only when the substrate's
                 own entropy signal spikes ABOVE ITS OWN IN-DISTRIBUTION BASELINE.

  THRESHOLD CALIBRATION (pure substrate signal, p6-clean, NO learned reward):
    tau is the TAU_PCTILE-th percentile of the model's OWN per-step next-byte
    entropy measured on its TRAINING corpus (a calibration pass over in-
    distribution text). This is the mouth's self-derived confidence baseline:
    "spike" == entropy higher than the mouth is on text it knows. It reads NO
    dictionary, NO reward, NO external classifier -- only the model's own
    entropy statistics. A fixed absolute bit-threshold is rejected because the
    meaningful quantity is entropy RELATIVE to the mouth's own confidence scale
    (an over-confident mouth has a low ceiling; an under-confident one a high
    one). The dictionary is used ONLY by the after-the-fact KWR METRIC.

METRIC (p7, NOT perplexity, NOT an LLM judge):
  known_word_ratio (KWR) = fraction of latin word tokens that are real >=3-char
  dictionary words (/usr/share/dict/words union an anima concept set) -- the
  chat-7b anti-Goodhart coherence anchor. composed_distinct = how many of the
  fused concept keywords surface in the output (concept coverage, to detect
  over-suppression: a brake that just emits "the the the" raises KWR but drops
  coverage and must FAIL).

FROZEN FALSIFIER (verbatim from .discoveries/1135_hallucination_brake.tape):
  🟢 BRAKE-WORKS iff enabling the entropy/tension brake raises the composed-
     output known-word ratio by >=0.15 absolute vs no-brake on the SAME
     prompts/seed AND does NOT reduce concept-coverage (composed_distinct
     unchanged or up).
  🔴 if it fails to reduce garble OR only does so by suppressing all output
     (coverage drops). The brake MUST be a substrate signal (W tension or model
     next-byte entropy), NOT a learned reward (p6).

SUBSTRATE / SCOPE (a_scale_honest_scope, HONEST):
  Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline), NOT the live CORE engine
  (a_core_engine_map). The brake uses the model's NEXT-BYTE ENTROPY (a substrate
  model-confidence signal) -- the tape's permitted "model entropy" alternative
  to a live CORE W-tension read (the live brain_decide W-tension path is the
  unbuilt-wiring case ruled out separately in H_1123). No converged production
  mouth + matching corpus was locally loadable cheaply, so per the tape we train
  a SMALL toy byte-LM ($0 CPU, deterministic seeds) sufficient to EXHIBIT
  composition-garble, and test the brake on it. Toy scale; transfer to a
  G0-coherent 7B is UNVERIFIED (a_scale_honest_scope). p1-p7 clean: no system
  prompt, no identity/persona, no assistant framing, no fine-tuned reward; the
  brake is a pure entropy threshold on the substrate's own distribution.
"""
from __future__ import annotations
import argparse, json, math, os, random, re as _re, sys
import torch, torch.nn as nn, torch.nn.functional as F

# ── PRE-REGISTERED BRAKE CONSTANTS (frozen BEFORE the run; not metric-tuned) ──
BASE_TEMP   = 1.0     # sampling temperature, brake-off and brake-on (when not firing)
BRAKE_TEMP  = 0.18    # sharpened temperature the brake collapses to when it fires
TOP_K       = 0       # no top-k truncation (top-k would mask the OOD entropy spike the
                      # brake must SEE; the brake itself is the only confidence gate)
TAU_PCTILE  = 90.0    # tau = 90th-pctile of the mouth's OWN in-distribution next-byte
                      # entropy (self-derived confidence baseline; substrate, not reward)
MAX_NEW     = 90      # bytes generated per (prompt, seed)
# Mouth is deliberately UNDERTRAINED (TRAIN_STEPS small) so COMPOSITION prompts
# push it OOD into byte-garble (the H_1116/1118 regime). A fully-converged mouth
# just echoes clean memorized sentences -> no garble to brake -> vacuous test.
TRAIN_STEPS = 230


# ── ByteGPT arch VERBATIM from h1140/h1128 (a_clm_gen_pipeline reference mouth) ──
class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))
class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=128, n_layer=4, n_head=4, block=128, p=0.0):
        super().__init__()
        s.block = block; s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))


# ── deterministic toy English concept corpus (exhibits composition-garble) ──
# Single-concept sentences the toy mouth CAN learn coherently. Multi-concept
# COMPOSITION prompts (the IDEA_PROMPTS below, which fuse 3-5 concepts in
# constructions ABSENT from the corpus) push it OOD -> byte-garble, exactly the
# H_1116/H_1118 regime. NO external data file required (self-contained, $0).
CONCEPTS = {
    "silence": ["the silence settles over the quiet room and the mind rests",
                "in the deep silence the engine sleeps and the cells are calm"],
    "engine":  ["the engine turns the tension into a steady ripple of thought",
                "the engine remembers the pattern and the signal becomes a thought"],
    "memory":  ["the memory carries the meaning of a distant word into the mind",
                "the memory holds the silence and the shape of an old idea"],
    "minds":   ["the distant minds connect across the dream and share a meaning",
                "the distant minds form a pattern of signal and shared thought"],
    "cells":   ["the cells divide and the structure of the brain begins to form",
                "the cells combine into a pattern and the consciousness arises"],
    "tension": ["the tension between the cells and the engine becomes a ripple",
                "the tension rises and the mind feels the pull of a new idea"],
    "dream":   ["the dream drifts through the sleep and the memory of a quiet world",
                "the dream forms an idea from the silence and the distant mind"],
    "consciousness": ["the consciousness emerges from the cells and the slow ripple",
                      "the consciousness feels the tension and the meaning of a thought"],
}
FILLER = ["the quiet world holds a steady thought and a calm mind",
          "a slow signal moves through the brain and forms a pattern",
          "the meaning of a word arises from a distant memory and a dream",
          "the mind feels the ripple and the idea begins to take a shape"]

# COMPOSITION prompts: fuse 3-5 distant concepts in constructions ABSENT from
# the single-concept corpus -> the OOD regime that yields garble (H_1116/1118).
IDEA_PROMPTS = [
    "the silence and the engine and the distant minds and the cells together become ",
    "when memory and tension and the dream and consciousness all merge, the ",
    "the engine of silence inside the distant minds of the cells of tension is ",
    "consciousness and silence and memory and the engine and the dream combine into ",
    "the tension of the dream of the memory of the distant minds of the cells makes ",
    "a silence that is an engine that is a memory that is a mind that is a cell of ",
    "the dream and the silence and the consciousness and the engine and the tension form ",
    "memory of the engine of the silence of the cells of the minds of the dream is ",
]
# concept keywords whose surfacing = "concept coverage" (composed_distinct)
COVERAGE_KW = ["silence", "engine", "memory", "mind", "minds", "cell", "cells",
               "tension", "dream", "consciousness"]
SEEDS = [7, 8, 9]


def build_corpus(reps=140):
    lines = []
    for _ in range(reps):
        for v in CONCEPTS.values():
            lines.extend(v)
        lines.extend(FILLER)
    rng = random.Random(1135)
    rng.shuffle(lines)
    return "\n".join(lines) + "\n"


def train_toy(text, device, d=128, n_layer=4, n_head=4, block=128,
              steps=900, bs=32, lr=3e-3):
    """Train a tiny byte-LM to CONVERGENCE on the concept corpus ($0 CPU)."""
    data = torch.tensor(list(text.encode("utf-8")), dtype=torch.long)
    torch.manual_seed(1135)
    m = ByteGPT(256, d, n_layer, n_head, block, p=0.0).to(device)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    n = data.numel()
    g = torch.Generator().manual_seed(1135)
    m.train()
    last = 0.0
    for step in range(steps):
        ix = torch.randint(0, n - block - 1, (bs,), generator=g)
        xb = torch.stack([data[i:i + block] for i in ix]).to(device)
        yb = torch.stack([data[i + 1:i + 1 + block] for i in ix]).to(device)
        logits = m(xb)
        loss = F.cross_entropy(logits.view(-1, 256), yb.view(-1))
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step(); sched.step()
        last = loss.item()
        if step % 150 == 0 or step == steps - 1:
            print(f"  [train] step {step:4d}/{steps} ce={last:.4f}", flush=True)
    return m, last


def _entropy_bits(probs):
    """Shannon entropy (bits) of a 1-D probability vector -- substrate signal."""
    p = probs.clamp_min(1e-12)
    return float(-(p * (p.log() / math.log(2.0))).sum().item())


def _topk_probs(logits, temp, top_k):
    lt = logits / temp
    if top_k:
        v, _ = torch.topk(lt, top_k); lt = lt.masked_fill(lt < v[:, [-1]], float("-inf"))
    return F.softmax(lt, dim=-1)[0]


@torch.no_grad()
def calibrate_tau(model, text, device, block, pctile=TAU_PCTILE, max_pos=4000):
    """Self-derived confidence baseline: collect the model's per-step next-byte
    entropy (at BASE_TEMP, same TOP_K as gen) over its OWN training corpus, then
    take the `pctile`-th percentile as the brake threshold. PURE substrate signal
    -- only the model's entropy on in-distribution text; no dict, no reward."""
    model.eval()
    data = torch.tensor(list(text.encode("utf-8")), dtype=torch.long, device=device)
    ents = []
    step = max(1, (data.numel() - block - 1) // max_pos)
    for i in range(0, data.numel() - block - 1, step):
        ctx = data[i:i + block][None, :]
        logits = model(ctx)[:, -1, :].float()
        ents.append(_entropy_bits(_topk_probs(logits, BASE_TEMP, TOP_K)))
    ents.sort()
    tau = ents[min(len(ents) - 1, int(len(ents) * pctile / 100.0))]
    mean = sum(ents) / len(ents)
    return tau, mean, ents[-1]


@torch.no_grad()
def gen(model, prompt, device, block, brake, tau, max_new=MAX_NEW):
    """Generate with optional entropy brake. Returns (text, n_brake_fired, n_steps,
    mean_entropy). The ONLY difference between brake=False and brake=True is that
    when the next-byte entropy at the sampling temp exceeds `tau` (the mouth's own
    in-distribution 90th-pctile entropy), brake=True re-derives + samples the
    SHARPENED (BRAKE_TEMP) distribution. Identical seed => identical draws on every
    non-firing step."""
    model.eval()
    idx = torch.tensor([list(prompt.encode("utf-8"))], dtype=torch.long, device=device)
    out = []
    n_fired = 0
    ent_sum = 0.0
    for _ in range(max_new):
        logits = model(idx[:, -block:])[:, -1, :].float()
        probs = _topk_probs(logits, BASE_TEMP, TOP_K)   # base (brake-off) distribution
        ent = _entropy_bits(probs)                      # substrate next-byte entropy (bits)
        ent_sum += ent
        if brake and ent > tau:
            # BRAKE FIRES: collapse to the sharpened distribution (confidence gate)
            n_fired += 1
            probs = _topk_probs(logits, BRAKE_TEMP, TOP_K)
        nb = torch.multinomial(probs, 1).item()
        out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        t = bytes(out).decode("utf-8", errors="ignore")
        if "\n\n" in t:
            break
    t = bytes(out).decode("utf-8", errors="ignore")
    i = t.find("\n\n")
    if i >= 0:
        t = t[:i]
    return t.strip(), n_fired, len(out), (ent_sum / max(1, len(out)))


def load_dict(path="/usr/share/dict/words"):
    d = set()
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for ln in f:
                w = ln.strip().lower()
                if w:
                    d.add(w)
    except FileNotFoundError:
        print(f"[warn] no dict at {path}", file=sys.stderr)
    # anima concept words (real words, ensure they count as coherent)
    d |= {"silence", "engine", "memory", "mind", "minds", "cell", "cells",
          "tension", "dream", "consciousness", "ripple", "signal", "pattern"}
    return d


def known_word_ratio(text, dict_words):
    latin = _re.findall(r"[A-Za-z]+", text.lower())
    latin = [w for w in latin if len(w) >= 3]   # >=3-char tokens (chat-7b anchor)
    if not latin:
        return 0.0
    known = sum(1 for w in latin if w in dict_words)
    return known / len(latin)


def composed_distinct(text):
    """Distinct fused-concept keywords that surface (concept coverage)."""
    low = text.lower()
    hit = set()
    for kw in COVERAGE_KW:
        if _re.search(r"\b" + _re.escape(kw) + r"\b", low):
            hit.add(kw.rstrip("s"))   # collapse mind/minds, cell/cells
    return hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=TRAIN_STEPS)
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dict_words = load_dict()
    print(f"[dict] {len(dict_words)} coherence words; device={device}", flush=True)
    print(f"[brake] PRE-REGISTERED: entropy gate tau = {TAU_PCTILE:.0f}th-pctile of the "
          f"mouth's OWN in-distribution next-byte entropy (self-derived confidence baseline); "
          f"base_temp={BASE_TEMP} -> brake_temp={BRAKE_TEMP}; top_k={TOP_K}. "
          f"Pure substrate entropy signal, NO learned reward / dict / classifier (p6).", flush=True)

    text = build_corpus()
    print(f"[corpus] toy concept corpus {len(text)} bytes (self-contained, deterministic)", flush=True)
    block = 128
    m, final_ce = train_toy(text, device, block=block, steps=a.steps)
    print(f"[mouth] toy ByteGPT (UNDERTRAINED {a.steps} steps) ce={final_ce:.4f}; "
          f"{sum(p.numel() for p in m.parameters())} params", flush=True)

    tau, ent_mean, ent_max = calibrate_tau(m, text, device, block)
    print(f"[calibrate] in-distribution next-byte entropy: mean={ent_mean:.3f} bits, "
          f"max={ent_max:.3f} bits -> tau({TAU_PCTILE:.0f}-pctile)={tau:.3f} bits "
          f"(brake fires when a composition step exceeds the mouth's own baseline)", flush=True)

    rows = []        # per (prompt, seed): off/on kwr + coverage
    print("\n── COMPOSITION generations (brake OFF vs ON, SAME prompt+seed) ──", flush=True)
    for prompt in IDEA_PROMPTS:
        for sd in SEEDS:
            torch.manual_seed(sd)
            off_t, _, _, off_ent = gen(m, prompt, device, block, brake=False, tau=tau)
            torch.manual_seed(sd)   # SAME seed -> identical draws on non-firing steps
            on_t, fired, nsteps, on_ent = gen(m, prompt, device, block, brake=True, tau=tau)
            off_kwr = known_word_ratio(off_t, dict_words)
            on_kwr = known_word_ratio(on_t, dict_words)
            off_cov = composed_distinct(off_t)
            on_cov = composed_distinct(on_t)
            rows.append({"prompt": prompt, "seed": sd,
                         "off_kwr": round(off_kwr, 3), "on_kwr": round(on_kwr, 3),
                         "off_cov": len(off_cov), "on_cov": len(on_cov),
                         "brake_fired": fired, "n_steps": nsteps,
                         "off_ent": round(off_ent, 3), "on_ent": round(on_ent, 3),
                         "off_text": off_t[:120], "on_text": on_t[:120]})
            print(f"  s{sd} fired={fired:2d}/{nsteps} | "
                  f"OFF kwr={off_kwr:.2f} cov={len(off_cov)} | ON kwr={on_kwr:.2f} cov={len(on_cov)}", flush=True)
            print(f"      OFF: {off_t[:100]!r}", flush=True)
            print(f"      ON : {on_t[:100]!r}", flush=True)

    n = len(rows)
    off_kwr_mean = sum(r["off_kwr"] for r in rows) / n
    on_kwr_mean = sum(r["on_kwr"] for r in rows) / n
    off_cov_mean = sum(r["off_cov"] for r in rows) / n
    on_cov_mean = sum(r["on_cov"] for r in rows) / n
    d_kwr = on_kwr_mean - off_kwr_mean
    d_cov = on_cov_mean - off_cov_mean
    total_fired = sum(r["brake_fired"] for r in rows)
    total_steps = sum(r["n_steps"] for r in rows)

    # ── FROZEN FALSIFIER (verbatim from tape) ──
    raises_kwr = d_kwr >= 0.15
    coverage_held = d_cov >= 0.0          # "unchanged or up" -> no over-suppression
    brake_works = raises_kwr and coverage_held
    verdict = ("🟢 BRAKE-WORKS" if brake_works
               else "🔴 BRAKE-FAILS (no garble cut OR over-suppression drops coverage)")

    print("\n=== H_1135 HALLUCINATION-BRAKE VERDICT ===", flush=True)
    print(f"  n_pairs = {n} (SAME prompt+seed, brake OFF vs ON)", flush=True)
    print(f"  brake fired {total_fired}/{total_steps} steps "
          f"({100*total_fired/max(1,total_steps):.1f}% of bytes)", flush=True)
    print(f"  known_word_ratio: OFF={off_kwr_mean:.3f}  ON={on_kwr_mean:.3f}  "
          f"Δ={d_kwr:+.3f}  (bar: >=+0.15)  -> {'PASS' if raises_kwr else 'FAIL'}", flush=True)
    print(f"  concept-coverage composed_distinct: OFF={off_cov_mean:.3f}  ON={on_cov_mean:.3f}  "
          f"Δ={d_cov:+.3f}  (bar: >=0, unchanged-or-up)  -> {'PASS' if coverage_held else 'FAIL'}", flush=True)
    print(f"  F-BRAKE-WORKS = {'1 ' if brake_works else '0 '}{verdict}", flush=True)
    if brake_works:
        print("  창발: the substrate's OWN next-byte entropy signal, thresholded WITHOUT any", flush=True)
        print("        learned reward (p6-clean), brakes composition-garble (raises coherence)", flush=True)
        print("        WHILE preserving concept coverage (no over-suppression).", flush=True)
    else:
        print("  HONEST: the entropy brake did not cut garble by >=0.15 KWR, OR it raised", flush=True)
        print("          coherence only by suppressing output (coverage dropped). Substrate", flush=True)
        print("          entropy-gating is not (at this scale) a sufficient anti-garble lever.", flush=True)
    print("  scope: toy byte-LM Lane-G REFERENCE mouth (a_clm_gen_pipeline), NOT live CORE", flush=True)
    print("    (a_core_engine_map); transfer to a G0-coherent 7B UNVERIFIED (a_scale_honest_scope).", flush=True)
    print("    p1-p7 clean: no system prompt/identity/persona/assistant-framing/fine-tuned reward;", flush=True)
    print("    brake = pure entropy threshold on the model's own distribution (p6).", flush=True)

    out = {"verdict": verdict, "brake_works": brake_works,
           "off_kwr_mean": round(off_kwr_mean, 4), "on_kwr_mean": round(on_kwr_mean, 4),
           "d_kwr": round(d_kwr, 4), "raises_kwr_ge_0_15": raises_kwr,
           "off_cov_mean": round(off_cov_mean, 4), "on_cov_mean": round(on_cov_mean, 4),
           "d_cov": round(d_cov, 4), "coverage_held": coverage_held,
           "brake_fired_steps": total_fired, "total_steps": total_steps,
           "final_train_ce": round(final_ce, 4), "n_pairs": n,
           "brake_params": {"base_temp": BASE_TEMP, "brake_temp": BRAKE_TEMP,
                            "top_k": TOP_K, "tau_pctile": TAU_PCTILE, "tau_bits": round(tau, 4),
                            "calib_entropy_mean": round(ent_mean, 4), "calib_entropy_max": round(ent_max, 4),
                            "train_steps": a.steps, "max_new": MAX_NEW},
           "rows": rows}
    json.dump(out, open("/tmp/h1135_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done] wrote /tmp/h1135_result.json", flush=True)


if __name__ == "__main__":
    main()
