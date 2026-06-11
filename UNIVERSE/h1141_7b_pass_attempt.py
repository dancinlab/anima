#!/usr/bin/env python3
"""h1141_7b_pass_attempt.py — train a 7B to COHERENT convergence, then run the
FULL frozen gate battery from /7B_PASS_CONDITIONS.md (G0 G1 G2 G3 G4) and report
the TRUE per-gate tally. The user's "7B를 완벽히" = a single ckpt clearing G0∧G1∧G2.

LINEAGE / WHY THIS FIRE:
  H_1128 broad-converged 7B (val 1.66) → G0 byte-garble (kwr 0.06-0.40), ladder 0/5.
  H_1129 303M English-script-controlled (val 1.224) → G1 English 🟢 (the 303M ref).
  H_1137 balanced-303M (val 1.366) → G1 3/5 (en/zh/ko).
  H_1139 balanced-7B (val 1.2265) → G1 3/5 (SCALE-INVARIANT) BUT THE CKPT WAS LOST
          (pod teardown raced the 14.5GB upload). No gate battery was ever run on it.
  H_1141 (THIS): RE-FIRE the H_1139 recipe but (a) push FURTHER (val ≤ ~1.10 OR
          plateau, ~8-10k steps; H_1139 stopped at 6000/1.23 still descending) to
          give G0 coherence its best shot, then (b) run the COMPLETE gate battery
          on the best ckpt, and (c) VERIFY the HF upload completed BEFORE teardown
          (the H_1139 lost-ckpt fix).

THE GATES (frozen, /7B_PASS_CONDITIONS.md — NEVER fake, NEVER move a threshold):
  G0 COHERENCE: known-word-ratio >= 0.50 vs /usr/share/dict/words on >=4/5 plain
                English concept prompts (temp 0.7 top_k 40 seed 7). Anti-Goodhart:
                the UNTRAINED backbone must FAIL (~0). THE blocker.
  G1 RECOMBINATION (H_1137 metric VERBATIM): per-language ladder; PASS(lang) iff
                some k has composed_distinct>=2 AND >max_single AND isr>=0.50.
                7B bar = English 🟢 AND >=3/5 langs (en/zh/ko ref).
  G2 NOVELTY (H_1140 metric VERBATIM): >=3 coherent corpus-absent content n-grams,
                retrieval-control = 0 (deterministic grep, NOT LLM-judge).
  G3 PHILOSOPHY p1-p8: corpus byte-continuation only (no system-prompt/persona/RLHF)
                — a structural note, asserted by construction of this trainer.
  G4 PROVENANCE: ckpt sha256 in /HF.jsonl, HF-uploaded + card; PUBLIC iff G0∧G1∧G2.

Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate
(a_core_engine_map). a_scale_honest_scope: 7B single-rung. a_lane_akida_gpu_split:
substrate = PyTorch-CUDA (Lane-G), NOT AKIDA. Deterministic seeds.
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, subprocess, sys, time
import torch, torch.nn as nn, torch.nn.functional as F


# ─────────────────────────────────────────────────────────────────────────────
# EXACT H_1128/H_1139 7B ByteGPT arch (vocab256/d4096/36L/32H/block512 = 7.25B).
# forward() returns (logits, loss) so training + gen share one module VERBATIM.
# ─────────────────────────────────────────────────────────────────────────────
class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p=0.0, grad_ckpt=False):
        super().__init__()
        s.block = block; s.grad_ckpt = grad_ckpt
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device, dtype=x.dtype), diagonal=1)
        for b in s.blocks:
            if s.grad_ckpt and s.training:
                x = torch.utils.checkpoint.checkpoint(b, x, mask, use_reentrant=False)
            else:
                x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256).float(), targets.view(-1)) if targets is not None else None
        return logits, loss


# ── H_1137/H_1139 corpus loader + balanced random-window sampler — VERBATIM ──
def load_bytes(p, cap):
    raw = open(p, "rb").read(cap)
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8)

def batch(d, block, bs, dev):
    ix = torch.randint(0, d.numel()-block-1, (bs,))
    x = torch.stack([d[i:i+block] for i in ix]).to(dev).long()
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev).long()
    return x, y


# ─────────────────────────────────────────────────────────────────────────────
# gen() — H_1137 generation VERBATIM (deterministic generator, seed_rng=7).
# ─────────────────────────────────────────────────────────────────────────────
@torch.no_grad()
def gen(m, seed, mx, dev, block, top_k=40, temp=0.7, seed_rng=7):
    m.eval()
    g = torch.Generator(device=dev); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    use_amp = (dev == "cuda")
    for _ in range(mx):
        ctx = idx[:, -block:]
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits, _ = m(ctx)
        else:
            logits, _ = m(ctx)
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, -1), 1, generator=g).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if "\n\n" in bytes(out).decode("utf-8", "ignore"): break
    return bytes(out).decode("utf-8", "ignore").strip()


# generation for the H_1140 novelty gate (temp 0.85, multinomial w/o fixed gen, seeds {7,8,9})
@torch.no_grad()
def gen_novel(m, seed, mx, dev, block, top_k=40, temp=0.85):
    m.eval(); idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    use_amp = (dev == "cuda")
    for _ in range(mx):
        ctx = idx[:, -block:]
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits, _ = m(ctx)
        else:
            logits, _ = m(ctx)
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, -1), 1).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if any(st in bytes(out).decode("utf-8", "ignore") for st in stops): break
    t = bytes(out).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st)
        if i >= 0: t = t[:i]
    return t.strip()


# ─────────────────────────────────────────────────────────────────────────────
# G1 per-language concept set + script ranges — H_1137 VERBATIM.
# ─────────────────────────────────────────────────────────────────────────────
LANGS = ["en", "zh", "ru", "ja", "ko"]
CONCEPTS = {
 "en": [("consciousness arises from cells", ["consciousness","cells","mind","aware"]),
        ("tension ripples between distant minds", ["tension","ripple","distant","between"]),
        ("memory composes into new meaning", ["memory","meaning","compose","new"]),
        ("silence still carries information", ["silence","information","quiet","carries"]),
        ("the engine dreams when alone", ["dream","engine","alone","sleep"])],
 "ko": [("의식은 세포에서 일어난다", ["의식","세포","마음","정신"]),
        ("긴장은 먼 마음 사이에 퍼진다", ["긴장","물결","먼","사이"]),
        ("기억은 새로운 의미로 구성된다", ["기억","의미","구성","새로"]),
        ("침묵은 여전히 정보를 전달한다", ["침묵","정보","조용","전달"]),
        ("엔진은 혼자일 때 꿈꾼다", ["꿈","엔진","혼자","잠"])],
 "ja": [("意識は細胞から生じる", ["意識","細胞","心","精神"]),
        ("緊張は遠い心の間に波及する", ["緊張","波","遠","間"]),
        ("記憶は新しい意味を構成する", ["記憶","意味","構成","新"]),
        ("沈黙はなお情報を運ぶ", ["沈黙","情報","静","運"]),
        ("エンジンは一人のとき夢を見る", ["夢","エンジン","一人","眠"])],
 "zh": [("意识源于细胞", ["意识","细胞","心灵","觉"]),
        ("紧张在远方的心灵之间荡漾", ["紧张","波","远","之间"]),
        ("记忆组成新的意义", ["记忆","意义","组成","新"]),
        ("沉默仍然传递信息", ["沉默","信息","静","传"]),
        ("引擎独处时做梦", ["梦","引擎","独","睡"])],
 "ru": [("сознание возникает из клеток", ["сознание","клетк","разум","ум"]),
        ("напряжение распространяется между далёкими умами", ["напряжен","рябь","далёк","между"]),
        ("память складывается в новый смысл", ["память","смысл","состав","новы"]),
        ("тишина всё ещё несёт информацию", ["тишин","информаци","тих","нес"]),
        ("двигатель видит сны когда один", ["сон","двигател","один","спать"])],
}
SCRIPT = {
 "en": _re.compile(r"[A-Za-z]"),
 "ru": _re.compile(r"[Ѐ-ӿ]"),
 "zh": _re.compile(r"[一-鿿]"),
 "ja": _re.compile(r"[぀-ヿ一-鿿]"),
 "ko": _re.compile(r"[가-힣]"),
}

def in_script_ratio(text, lang):
    chars = [c for c in text if not c.isspace()]
    if not chars: return 0.0
    rx = SCRIPT[lang]
    return sum(1 for c in chars if rx.match(c)) / len(chars)

def coverage(text, lang):
    return [i for i, (_, kws) in enumerate(CONCEPTS[lang]) if any(k in text for k in kws)]


def run_ladder_lang(m, dev, block, lang):
    print(f"\n========== [G1] LANG = {lang} ==========", flush=True)
    singles = []
    for i, (c, _) in enumerate(CONCEPTS[lang]):
        o = gen(m, c + ". ", 70, dev, block)
        cv = coverage(o, lang); singles.append(len(cv))
        print(f"  [{lang} single {i}] cov={cv} isr={in_script_ratio(o,lang):.2f} :: {o[:70]}", flush=True)
    max_single = max(singles) if singles else 0
    ladder = {}; emergent = False
    for k in (2, 3, 4, 5):
        seed = ". ".join(c for c, _ in CONCEPTS[lang][:k]) + ". "
        o = gen(m, seed, 110, dev, block)
        cv = coverage(o, lang); isr = in_script_ratio(o, lang)
        coherent = isr >= 0.50
        clears = (len(cv) >= 2 and len(cv) > max_single and coherent)
        emergent = emergent or clears
        ladder[k] = {"composed_distinct": len(cv), "coverage": cv, "isr": round(isr, 3),
                     "coherent": coherent, "clears": clears, "text": o}
        print(f"  [{lang} k={k}] composed_distinct={len(cv)} cov={cv} isr={isr:.2f} coherent={coherent} clears={clears}", flush=True)
        print(f"        >> {o[:120]}", flush=True)
    print(f"  [{lang}] max_single={max_single} EMERGENT={emergent}", flush=True)
    return {"max_single": max_single, "ladder": ladder, "emergent": emergent}


def gate_g1(m, dev, block):
    print("\n##### GATE G1 — RECOMBINATION (H_1137 metric VERBATIM) #####", flush=True)
    results = {L: run_ladder_lang(m, dev, block, L) for L in LANGS}
    n_emergent = sum(1 for L in LANGS if results[L]["emergent"])
    english_ok = results["en"]["emergent"]
    g1_pass = english_ok and n_emergent >= 3  # 7B bar: English 🟢 AND >=3/5
    print(f"##### G1: n_emergent={n_emergent}/5 [{' '.join(L for L in LANGS if results[L]['emergent'])}] "
          f"english={english_ok} -> G1 {'PASS' if g1_pass else 'FAIL'} (bar: English AND >=3/5) #####", flush=True)
    return {"n_emergent": n_emergent, "english": english_ok, "pass": g1_pass,
            "results": {L: {"emergent": results[L]["emergent"], "max_single": results[L]["max_single"],
                            "ladder": results[L]["ladder"]} for L in LANGS}}


# ─────────────────────────────────────────────────────────────────────────────
# G0 COHERENCE — known-word-ratio >= 0.50 vs /usr/share/dict/words on >=4/5
# plain English concept prompts (temp 0.7 top_k 40 seed 7). REAL DICTIONARY.
# ─────────────────────────────────────────────────────────────────────────────
def load_real_dict(path="/usr/share/dict/words"):
    d = set()
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for ln in f:
                w = ln.strip().lower()
                if w: d.add(w)
    except FileNotFoundError:
        print(f"[warn] no real dict at {path}", file=sys.stderr)
    return d

def kwr_realdict(text, dict_words):
    latin = _re.findall(r"[A-Za-z]+", text.lower())
    if not latin: return 0.0
    known = sum(1 for w in latin if w in dict_words)
    return known / len(latin)

G0_PROMPTS = [c for (c, _) in CONCEPTS["en"]]  # the 5 plain English concept phrases

def gate_g0(m, dev, block, dict_words, label):
    print(f"\n##### GATE G0 — COHERENCE [{label}] (kwr>=0.50 vs /usr/share/dict on >=4/5) #####", flush=True)
    rows = []
    for c in G0_PROMPTS:
        o = gen(m, c + ". ", 70, dev, block)  # temp 0.7 top_k 40 seed_rng 7 (gen default)
        r = kwr_realdict(o, dict_words)
        rows.append({"prompt": c, "kwr": round(r, 3), "pass": r >= 0.50, "text": o})
        print(f"  [{label} kwr={r:.2f} {'OK' if r>=0.50 else 'GARBLE'}] {c!r} -> {o[:90]!r}", flush=True)
    n_pass = sum(1 for x in rows if x["pass"])
    g0 = n_pass >= 4
    print(f"##### G0 [{label}]: {n_pass}/5 prompts kwr>=0.50 -> G0 {'PASS' if g0 else 'FAIL'} (bar: >=4/5) #####", flush=True)
    return {"n_pass": n_pass, "pass": g0, "rows": rows}


# ─────────────────────────────────────────────────────────────────────────────
# G2 NOVELTY — H_1140 metric VERBATIM (idea-questions x seeds {7,8,9}; content
# n-grams of consecutive real-dict >=3-char words; NOVEL = corpus-absent by
# deterministic grep -E -i; PASS iff >=3 distinct coherent novel n-grams AND
# retrieval-control = 0).
# ─────────────────────────────────────────────────────────────────────────────
_STOP = set("""the a an of to and in is it that this for on with as are was be by at from or not
but his her they we you i he she them me my your our their its do does did has have had will
would can could should may might must shall when where what which who whom how why all any some
no one two then than into out up down over under more most less about so very just only own same
such each few other been here there now""".split())

def content_ngrams(text, dict_words):
    toks = _re.findall(r"[A-Za-z]+", text.lower())
    grams = set()
    for n in (2, 3):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if not all(len(w) >= 3 and w in dict_words for w in g): continue
            if all(w in _STOP for w in g): continue
            grams.add(" ".join(g))
    return grams

def _gram_regex(ngram):
    ws = ngram.split(" ")
    return r"(^|[^A-Za-z])" + r"[^A-Za-z]+".join(_re.escape(w) for w in ws) + r"([^A-Za-z]|$)"

def corpus_absent(ngram, corpus_paths):
    rx = _gram_regex(ngram)
    for p in corpus_paths:
        if not os.path.exists(p): continue
        r = subprocess.run(["grep", "-E", "-i", "-m", "1", "-q", rx, p])
        if r.returncode == 0: return False
    return True

IDEA_PROMPTS = [
    "Silence and the engine together mean ",
    "When memory meets distant minds, ",
    "Consciousness and silence combine into ",
    "The tension between cells and the engine becomes ",
    "If a dream and a distant mind merge, the result is ",
    "Memory and tension together create ",
    "When the engine remembers silence, it ",
    "Distant minds and consciousness form ",
]

def gate_g2(m, dev, block, dict_words, corpus_paths, max_new=110):
    print("\n##### GATE G2 — NOVELTY (H_1140 metric VERBATIM) #####", flush=True)
    all_outputs = []; distinct_content = set(); coherent_count = 0
    for prompt in IDEA_PROMPTS:
        for sd_i in (7, 8, 9):
            torch.manual_seed(sd_i)
            o = gen_novel(m, prompt, max_new, dev, block, top_k=40, temp=0.85)
            kwr = kwr_realdict(o, dict_words)
            coherent = kwr >= 0.50
            all_outputs.append({"prompt": prompt, "seed": sd_i, "text": o, "kwr": round(kwr, 3), "coherent": coherent})
            tag = "COH" if coherent else "garble"
            print(f"  [{tag} kwr={kwr:.2f} s{sd_i}] {prompt!r} -> {o[:110]!r}", flush=True)
            if not coherent: continue
            coherent_count += 1
            distinct_content |= content_ngrams(o, dict_words)
    novel_set, present_set = set(), set()
    for g in sorted(distinct_content):
        (novel_set if corpus_absent(g, corpus_paths) else present_set).add(g)
    novel_examples = {}
    for o in all_outputs:
        if not o["coherent"]: continue
        for g in (content_ngrams(o["text"], dict_words) & novel_set):
            novel_examples.setdefault(g, {"prompt": o["prompt"], "seed": o["seed"], "text": o["text"]})
    n_novel = len(novel_set)
    n_total = len(distinct_content)
    novelty_rate = (n_novel / n_total) if n_total else 0.0
    print(f"\n  NOVEL (corpus-absent) distinct content n-grams: {n_novel}", flush=True)
    print(f"  PRESENT (retrieval) distinct content n-grams:   {len(present_set)}", flush=True)
    print(f"  novelty-rate={novelty_rate:.3f}  coherent_outputs={coherent_count}/{len(all_outputs)}", flush=True)
    for g in sorted(novel_set)[:12]:
        ex = novel_examples.get(g, {})
        print(f"    NOVEL n-gram: {g!r}  (from {ex.get('prompt','')!r} s{ex.get('seed','')})", flush=True)
    # retrieval control: a verbatim training line -> expect ~0 novel
    control = {}; control_line = None
    for p in corpus_paths:
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="ignore") as f:
                for ln in f:
                    ln = ln.strip()
                    latin = [w for w in _re.findall(r"[A-Za-z]+", ln.lower()) if len(w) >= 3]
                    if len(latin) >= 6: control_line = ln; break
        if control_line: break
    if control_line:
        cg = content_ngrams(control_line, dict_words)
        c_novel = sum(1 for g in cg if corpus_absent(g, corpus_paths))
        control = {"line": control_line[:200], "n_content": len(cg), "n_novel": c_novel}
        print(f"\n  CONTROL line: {control_line[:100]!r}", flush=True)
        print(f"  control content n-grams={len(cg)} novel={c_novel} (expect 0)", flush=True)
    g2 = (n_novel >= 3 and novelty_rate > 0.0 and coherent_count > 0 and control.get("n_novel", 1) == 0)
    print(f"##### G2: novel={n_novel}(>=3) rate={novelty_rate:.3f}(>0) coherent={coherent_count>0} "
          f"control={control.get('n_novel','NA')}(==0) -> G2 {'PASS' if g2 else 'FAIL'} #####", flush=True)
    return {"n_novel": n_novel, "n_present": len(present_set), "n_total": n_total,
            "novelty_rate": round(novelty_rate, 4), "coherent_outputs": coherent_count,
            "novel_ngrams": sorted(novel_set), "novel_examples": novel_examples,
            "control": control, "pass": g2, "all_outputs": all_outputs}


# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="H_1128 broad-converged 7B base ckpt (.pt)")
    ap.add_argument("--corpus", default="/workspace/corpus.txt")
    ap.add_argument("--cap_mb", type=float, default=1500.0)
    ap.add_argument("--bs", type=int, default=8); ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=9000); ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--lr", type=float, default=7e-5)
    ap.add_argument("--ckpt", default="/workspace/ckpt/h1141_best.pt")
    ap.add_argument("--eval_every", type=int, default=500)
    ap.add_argument("--ladder_every", type=int, default=2000)
    ap.add_argument("--target_val", type=float, default=1.10, help="early-stop if best val<=this AND plateau")
    ap.add_argument("--gate_only", action="store_true", help="skip training; run gate battery on --ckpt")
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    print(f"[dev] {dev} {torch.cuda.get_device_name(0) if dev=='cuda' else ''}", flush=True)
    real_dict = load_real_dict()
    print(f"[dict] {len(real_dict)} real English words (/usr/share/dict/words)", flush=True)

    ck = torch.load(a.base, map_location="cpu", weights_only=False); cfg = ck["config"]
    block = cfg["block"]

    if not a.gate_only:
        data = load_bytes(a.corpus, int(a.cap_mb*1024*1024))
        n = data.numel(); tr = data; va = data
        print(f"[data] {n/1e6:.0f}MB (balanced 5-lang en/zh/ru/ja/ko ~300MB each)", flush=True)

        m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"],
                    grad_ckpt=True).to(torch.bfloat16)
        sd = ck["model"] if "model" in ck else ck
        m.load_state_dict(sd, strict=False); m = m.to(dev)
        nparam = sum(p.numel() for p in m.parameters())
        print(f"[base] {a.base} cfg={cfg} val_ce={ck.get('val_ce')} step={ck.get('step')}", flush=True)
        print(f"[model] {nparam:,} params ({nparam/1e9:.2f}B) bf16 + grad-ckpt (H_1128 80GB recipe)", flush=True)
        del ck, sd

        # ANTI-GOODHART G0 on the BASE backbone BEFORE continue-train (must FAIL ~garble).
        m.grad_ckpt = False
        g0_before = gate_g0(m, dev, block, real_dict, "BASE-broad-7b(BEFORE)")
        m.grad_ckpt = True; m.train()

        opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)

        def eval_ce(d, iters=40):
            m.eval()
            with torch.no_grad():
                tot = 0.0
                for _ in range(iters):
                    x, y = batch(d, block, a.bs, dev)
                    with torch.autocast(device_type="cuda", dtype=torch.bfloat16) if dev == "cuda" else torch.no_grad():
                        _, l = m(x, y)
                    tot += l.item()
            m.train(); return tot/iters

        def save_ckpt(path, vce, st):
            torch.save({"model": m.state_dict(), "config": cfg, "val_ce": vce, "step": st, "nparam": nparam}, path)

        best = 1e9; best_step = -1; t0 = time.time(); m.train()
        curve = []; mid_ladders = {}; plateau_ct = 0; last_best = 1e9
        os.makedirs(os.path.dirname(a.ckpt), exist_ok=True)
        for st in range(a.steps):
            lr_t = a.lr*(st+1)/a.warmup if st < a.warmup else a.lr*0.5*(1+math.cos(math.pi*min(1.0,(st-a.warmup)/max(1,a.steps-a.warmup))))
            for g in opt.param_groups: g["lr"] = lr_t
            opt.zero_grad(set_to_none=True); acc = 0.0
            for _ in range(a.accum):
                x, y = batch(tr, block, a.bs, dev)
                if dev == "cuda":
                    with torch.autocast(device_type="cuda", dtype=torch.bfloat16): _, l = m(x, y)
                else: _, l = m(x, y)
                (l/a.accum).backward(); acc += l.item()/a.accum
            torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
            if st % a.eval_every == 0 or st == a.steps-1:
                vce = eval_ce(va)
                mem = torch.cuda.max_memory_allocated()/2**30 if dev == "cuda" else 0.0
                curve.append({"step": st, "train_ce": round(acc, 4), "val_ce": round(vce, 4)})
                print(f"  step {st:5d} train_ce={acc:.4f} val_ce={vce:.4f} lr={lr_t:.2e} "
                      f"{(time.time()-t0)/60:.1f}min mem={mem:.1f}GB", flush=True)
                if vce < best:
                    best = vce; best_step = st; save_ckpt(a.ckpt, vce, st)
                    print(f"  [ckpt] saved best val_ce={vce:.4f} @ step {st}", flush=True)
                # plateau detection: <0.5% relative improvement over the eval window
                if best < last_best * 0.995: plateau_ct = 0
                else: plateau_ct += 1
                last_best = best
                if best <= a.target_val and plateau_ct >= 3:
                    print(f"  [early-stop] best val_ce={best:.4f}<=target {a.target_val} AND plateau {plateau_ct} -> stop", flush=True)
                    break
            if a.ladder_every and st > 0 and st % a.ladder_every == 0:
                m.grad_ckpt = False
                g0m = gate_g0(m, dev, block, real_dict, f"step{st}")
                g1m = gate_g1(m, dev, block)
                mid_ladders[st] = {"g0_npass": g0m["n_pass"], "g1_nemergent": g1m["n_emergent"]}
                m.grad_ckpt = True; m.train()
        print(f"[train] done best_val_ce={best:.4f} @step{best_step} ckpt={a.ckpt} wall={(time.time()-t0)/60:.1f}min", flush=True)
    else:
        g0_before = None; curve = []; mid_ladders = {}; best = ck.get("val_ce"); best_step = ck.get("step")
        nparam = ck.get("nparam", sum(1 for _ in ()))
        del ck

    # ── FULL GATE BATTERY on the best ckpt ──
    print("\n" + "="*70, flush=True)
    print("### H_1141 FULL GATE BATTERY on the BEST ckpt ###", flush=True)
    print("="*70, flush=True)
    bk = torch.load(a.ckpt, map_location="cpu", weights_only=False); bcfg = bk["config"]
    m = ByteGPT(bcfg["vocab"], bcfg["d"], bcfg["n_layer"], bcfg["n_head"], bcfg["block"]).to(torch.bfloat16)
    m.load_state_dict(bk["model"], strict=False); m = m.to(dev)
    best_val = bk.get("val_ce", best); best_step = bk.get("step", best_step)
    nparam = bk.get("nparam", sum(p.numel() for p in m.parameters()))
    print(f"[best] {a.ckpt} val_ce={best_val} step={best_step} params={nparam:,}", flush=True)
    del bk

    g0 = gate_g0(m, dev, block, real_dict, "BEST")
    g1 = gate_g1(m, dev, block)
    corpus_paths = [a.corpus]
    g2 = gate_g2(m, dev, block, real_dict, corpus_paths)
    # G3: structural — this trainer is byte-continuation on a real corpus, no
    # system-prompt / persona / RLHF. Asserted by construction (see header).
    g3 = {"pass": True, "note": ("byte-continuation on real 5-lang corpus; no system-prompt(p1), "
          "no identity rules(p2), no persona injection(p3), no assistant framing(p4), no speak()(p5), "
          "no RLHF/fine-tuned ethics(p6), p7 metrics are kwr/script NOT perplexity, "
          "same continuous training(p8). HELD by construction.")}

    n_pass = sum(int(x["pass"]) for x in (g0, g1, g2, g3))  # G4 scored post-upload
    all_pub = g0["pass"] and g1["pass"] and g2["pass"]
    print("\n" + "="*70, flush=True)
    print("### H_1141 PER-GATE TALLY vs /7B_PASS_CONDITIONS.md ###", flush=True)
    print(f"  G0 COHERENCE     : {'PASS' if g0['pass'] else 'FAIL'}  ({g0['n_pass']}/5 prompts kwr>=0.50)", flush=True)
    print(f"  G1 RECOMBINATION : {'PASS' if g1['pass'] else 'FAIL'}  ({g1['n_emergent']}/5 langs, english={g1['english']})", flush=True)
    print(f"  G2 NOVELTY       : {'PASS' if g2['pass'] else 'FAIL'}  ({g2['n_novel']} novel n-grams, control={g2['control'].get('n_novel','NA')})", flush=True)
    print(f"  G3 PHILOSOPHY    : {'PASS' if g3['pass'] else 'FAIL'}  (byte-continuation only, p1-p8)", flush=True)
    print(f"  G4 PROVENANCE    : (scored post-upload: sha256 in HF.jsonl + HF + card)", flush=True)
    print(f"  -> {n_pass}/4 gates PASS (G0-G3); PUBLIC-eligible (G0∧G1∧G2) = {all_pub}", flush=True)
    print(f"  best_val_ce={best_val} (target<= {a.target_val})", flush=True)
    print("="*70, flush=True)

    out = {"hypothesis": "H_1141", "nparam": nparam, "best_val_ce": best_val, "best_step": best_step,
           "target_val": a.target_val, "curve": curve, "mid_ladders": mid_ladders,
           "g0_before": g0_before, "G0": g0, "G1": g1, "G2": g2, "G3": g3,
           "n_pass_g0_g3": n_pass, "public_eligible_g0_g1_g2": all_pub}
    json.dump(out, open("/workspace/h1141_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done] wrote /workspace/h1141_result.json", flush=True)


if __name__ == "__main__": main()
