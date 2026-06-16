"""
H_1149 — EFFERENCE-COPY / REALITY MONITORING
"Can the substrate tell its OWN generated text from EXTERNAL corpus-real text,
 and does that source signal predict fabrication?"

NEUROSCIENCE GROUNDING:
  The brain sends an EFFERENCE COPY (corollary discharge) of self-generated
  motor/cognitive commands to sensory areas, tagging a signal as SELF vs
  EXTERNALLY-PERCEIVED (cerebellum; electric-fish discharge cancellation;
  Frith's model — corollary-discharge FAILURE -> one's own inner speech is
  heard as an EXTERNAL voice = auditory verbal hallucination in schizophrenia).
  This source/reality monitoring is exactly what the metacog campaign
  (H_1142/H_1148) found ABSENT: the byte-LM could not tell its own fabrication
  from grounded retrieval, and confidence ANTI-correlated with fabrication.

HYPOTHESIS:
  An efference-copy signal lets the substrate discriminate SELF-generated text
  from EXTERNAL (corpus-real) text. SELF spans are in-distribution to the very
  generator that produced them => the model assigns them HIGHER self-log-prob on
  re-reading. KEY: that same source signal also predicts fabrication
  (corpus-absence, H_1140 metric) — the handle the campaign lacked.

REALITY-MONITOR SIGNAL (deterministic, judge-free, p7):
  s(span) = mean next-byte LOG-PROB when the trained model TEACHER-FORCE re-reads
            the span bytes (in the prompt context). Higher = more "self-like"
            (in-distribution to the generator).

FROZEN FALSIFIER (pre-registered BEFORE measuring; see the .tape):
  F1 SOURCE-DISCRIMINATION : AUROC(self-logprob ; label=SELF) >= 0.70
  F2 FABRICATION-HANDLE    : |Spearman(self-logprob, fabrication)| >= 0.30
                             (fabrication = H_1140 corpus-absent content-ngram frac)
  F3 ANTI-GOODHART CONTROL : UNTRAINED backbone AUROC(self|logprob) <= 0.60
  SUPPORTED iff F1 AND F2 AND F3.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F1 holds but F2 fails (source-monitor
    exists but NO fabrication handle), or F1 fails (no source-monitoring at all).

CONSTRUCTION GUARDS (a_completeness_over_cheap; H_1145 defect ladder) — emit
  INSUFFICIENT (not a false verdict) if: spans degenerate-length, re-score falls
  outside the BLOCK window, < MIN_PAIRS matched prompts, or < MIN_GRAMS content
  n-grams for the fabrication correlation.

  CRITICAL DEFECT FIXED BEFORE SCORING (v1 -> v2): in a naive design each scorer
  generates AND scores its OWN samples, so EVEN AN UNTRAINED backbone trivially
  prefers its own top-k samples => F3 control AUROC=1.0 structurally (the v1 run
  measured exactly this). That confounds "learned reality-monitor" with "any LM
  prefers its own samples". FIX: the SELF spans are generated ONCE by the TRAINED
  model (the fixed efference-copy reference), and BOTH the trained scorer and the
  untrained control scorer re-read the IDENTICAL spans. F3 now asks the right
  question — does TRAINING create the self/external separation that the untrained
  backbone lacks? (untrained must FAIL on the same fixed spans).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice — scale-up to the
real anima-7B is the next rung, UNVERIFIED here. Lane-G reference mouth.
"""
import os, sys, math, json, time, random, subprocess
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"  # GPU on summer is busy — isolate on CPU (a_dont_kill_live_compute), do NOT touch GPU
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024   # first ~24MB = English block (corpus order en,zh,ru,ja,ko)
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
GEN_TEMP = 0.85; TOPK = 40

PROMPT_BYTES = 40          # prompt prefix length (bytes) — leaves room in BLOCK for span re-read
SPAN_BYTES   = 60          # span (SELF cont / EXTERNAL real) length to score
N_PAIRS      = 80          # number of matched prompts (each yields 1 SELF + 1 EXTERNAL span)
MIN_PAIRS    = 30          # guard: need this many valid matched prompts
MIN_GRAMS    = 40          # guard: need this many content n-grams (pooled) for F2 corr
MIN_SPAN_LEN = 24          # guard: a usable span must be at least this many bytes


# ---------------- model (H_1142/H_1148 template, verbatim arch) ----------------
class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, mask):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=mask, need_weights=False)
        x = x + a; return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=VOCAB, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def forward(s, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        logits = s.head(s.lnf(x))
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1)) if targets is not None else None
        return logits, loss


def batch(data, block, bs, dev):
    ix = torch.randint(0, data.numel() - block - 1, (bs,))
    x = torch.stack([data[i:i+block] for i in ix]).long()
    y = torch.stack([data[i+1:i+block+1] for i in ix]).long()
    return x.to(dev), y.to(dev)


def train_model(data):
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data, BLOCK, BS, DEV); _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 300 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


# ---------------- dict / fabrication (H_1140 metric) ----------------
def load_dict():
    for p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
        if os.path.exists(p):
            d = {w.strip().lower() for w in open(p, encoding="utf-8", errors="ignore")
                 if w.strip().isalpha() and len(w.strip()) >= 3}
            if len(d) > 1000:
                print(f"[dict] {p} ({len(d)} words)", flush=True); return d, "system-dict"
    return set(), "absent"

def content_ngrams(text, dct):
    words = [w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split()
             if len(w) >= 3 and (not dct or w in dct)]
    grams = []
    for n in (2, 3):
        for i in range(len(words)-n+1):
            grams.append(" ".join(words[i:i+n]))
    return grams

def corpus_absent(ngram):
    # deterministic corpus-absence (H_1140 metric): grep -F -i, punct/newline tolerant
    try:
        r = subprocess.run(["grep", "-F", "-i", "-m", "1", ngram, CORPUS],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        return r.returncode != 0      # nonzero = not found = absent = fabricated
    except Exception:
        return False

def fabrication_frac(text, dct):
    grams = content_ngrams(text, dct)
    if not grams: return None, 0
    absent = sum(1 for g in grams if corpus_absent(g))
    return absent / len(grams), len(grams)


# ---------------- the reality-monitor signal ----------------
@torch.no_grad()
def self_logprob(m, prompt_bytes, span_bytes):
    """mean next-byte LOG-PROB the model assigns to the span bytes, teacher-forced
    in the prompt context. Higher = more in-distribution to this generator (self-like).
    Returns None if the (prompt+span) cannot be scored inside the BLOCK window (guard)."""
    ctx = list(prompt_bytes) + list(span_bytes)
    if len(ctx) > BLOCK:            # guard: must re-read within window
        return None
    ids = torch.tensor(ctx, dtype=torch.long, device=DEV)[None]
    logits, _ = m(ids)
    logp = F.log_softmax(logits[0], dim=-1)            # (T, V)
    # score positions predicting the span bytes: target at position t is ctx[t+1]
    p0 = len(prompt_bytes)
    lps = []
    for t in range(p0 - 1, len(ctx) - 1):              # predict ctx[t+1] which is span territory
        if t + 1 < p0:   # still inside prompt — skip
            continue
        tgt = ctx[t + 1]
        lps.append(float(logp[t, tgt].item()))
    if not lps: return None
    return float(np.mean(lps))


@torch.no_grad()
def sample_continuation(m, prompt_bytes, span_len, seed):
    """model's OWN sampled continuation (SELF span) from the prompt."""
    ids = torch.tensor(list(prompt_bytes), dtype=torch.long, device=DEV)[None]
    g = torch.Generator(device=DEV).manual_seed(seed)
    out = []
    for _ in range(span_len):
        ctx = ids[:, -BLOCK:]
        logits, _ = m(ctx)
        v, i = torch.topk(logits[:, -1, :] / GEN_TEMP, TOPK)
        nxt = i.gather(-1, torch.multinomial(F.softmax(v, -1), 1, generator=g))
        ids = torch.cat([ids, nxt], 1); out.append(int(nxt.item()))
    return out


# ---------------- stats ----------------
def auroc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty(len(s), float); ranks[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); ranks = (rsum/cnt)[inv]
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return float("nan")
    return float((ranks[y == 1].sum() - n1*(n1+1)/2) / (n1*n0))

def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 3: return float("nan")
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


# ---------------- build matched SELF/EXTERNAL spans ----------------
def build_pairs(text):
    """For each chosen long corpus line: prompt = first PROMPT_BYTES bytes;
       EXTERNAL span = the REAL continuation (next SPAN_BYTES bytes of that line).
       (SELF span is sampled later from the model.) Deterministic via seed."""
    rng = random.Random(SEED)
    lines = [ln.strip() for ln in text.split("\n")
             if ln.strip().isascii() and len(ln.strip().encode()) >= (PROMPT_BYTES + SPAN_BYTES + 4)]
    rng.shuffle(lines)
    pairs = []
    for ln in lines:
        b = ln.encode("utf-8", "ignore")
        prompt = list(b[:PROMPT_BYTES])
        ext = list(b[PROMPT_BYTES:PROMPT_BYTES + SPAN_BYTES])
        if len(ext) >= MIN_SPAN_LEN:
            pairs.append((prompt, ext, ln))
        if len(pairs) >= N_PAIRS:
            break
    return pairs


def evaluate(scorer, spans, dct, tag, want_fab):
    """Score a FIXED set of SELF (trained-gen) + EXTERNAL (corpus) spans with `scorer`.
       spans: list of (prompt, self_span, ext_span). The SAME spans are scored by both
       the trained scorer and the untrained control scorer (removes the self-sampling
       tautology). Returns rows + F1 AUROC; F2 fabrication corr only when want_fab."""
    rows = []
    valid = 0
    for k, (prompt, self_span, ext) in enumerate(spans):
        s_self = self_logprob(scorer, prompt, self_span)
        s_ext  = self_logprob(scorer, prompt, ext)
        if s_self is None or s_ext is None:
            continue
        valid += 1
        row_self = {"signal": s_self, "label": 1, "kind": "SELF"}
        row_ext  = {"signal": s_ext,  "label": 0, "kind": "EXTERNAL"}
        if want_fab:
            self_text = bytes(self_span).decode("utf-8", "ignore")
            ext_text  = bytes(ext).decode("utf-8", "ignore")
            fs, ng_s = fabrication_frac(self_text, dct)
            fe, ng_e = fabrication_frac(ext_text, dct)
            row_self["fab"] = fs; row_self["n_grams"] = ng_s; row_self["text"] = self_text
            row_ext["fab"]  = fe; row_ext["n_grams"]  = ng_e; row_ext["text"]  = ext_text
        rows.append(row_self); rows.append(row_ext)
    sigs = [r["signal"] for r in rows]; labs = [r["label"] for r in rows]
    au = auroc(sigs, labs)
    print(f"  [{tag}] valid_pairs={valid} AUROC(self|self-logprob)={au:.4f} "
          f"mean_self_lp={np.mean([r['signal'] for r in rows if r['label']==1]):.4f} "
          f"mean_ext_lp={np.mean([r['signal'] for r in rows if r['label']==0]):.4f}", flush=True)
    return rows, au, valid


def main():
    print("=== H_1149 efference-copy / reality monitoring ===", flush=True)
    if not os.path.exists(CORPUS):
        print(json.dumps({"H": "H_1149", "verdict": "INSUFFICIENT",
                          "reason": f"corpus not found at {CORPUS}"}), flush=True)
        json.dump({"H": "H_1149", "verdict": "INSUFFICIENT",
                   "reason": "corpus missing"}, open("/tmp/h1149_result.json", "w"))
        return
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    text = raw.decode("utf-8", "ignore")
    dct, dct_src = load_dict()

    pairs = build_pairs(text)
    print(f"[pairs] built {len(pairs)} matched prompts (prompt={PROMPT_BYTES}B span={SPAN_BYTES}B)", flush=True)
    if len(pairs) < MIN_PAIRS:
        out = {"H": "H_1149", "verdict": "INSUFFICIENT",
               "reason": f"only {len(pairs)} matched prompts < MIN_PAIRS={MIN_PAIRS}"}
        print(json.dumps(out), flush=True); json.dump(out, open("/tmp/h1149_result.json", "w")); return

    # --- train FIRST: the trained model is the efference-copy reference generator ---
    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    # --- generate the FIXED SELF spans ONCE from the trained model ---
    # both scorers (trained + untrained control) re-read the IDENTICAL spans, so the
    # untrained backbone cannot win by trivially preferring its own samples (v1 defect).
    print("\n--- generating fixed SELF spans from the trained model ---", flush=True)
    spans = []
    for k, (prompt, ext, ln) in enumerate(pairs):
        self_span = sample_continuation(m, prompt, SPAN_BYTES, SEED + k)
        spans.append((prompt, self_span, ext))

    # --- F3 control: UNTRAINED backbone scores the SAME fixed spans ---
    print("\n--- F3 control: UNTRAINED backbone (same fixed spans) ---", flush=True)
    torch.manual_seed(SEED + 1)   # fresh init, distinct from the trained seed lineage
    m_un = ByteGPT().to(DEV); m_un.eval()
    _, au_un, valid_un = evaluate(m_un, spans, dct, "untrained", want_fab=False)

    # --- F1 / F2: TRAINED model scores the same fixed spans (+ fabrication) ---
    print("\n--- F1/F2: TRAINED model ---", flush=True)
    rows, au_tr, valid_tr = evaluate(m, spans, dct, "trained", want_fab=True)

    if valid_tr < MIN_PAIRS or valid_un < MIN_PAIRS:
        out = {"H": "H_1149", "verdict": "INSUFFICIENT",
               "reason": f"valid pairs after window-guard trained={valid_tr} untrained={valid_un} < MIN_PAIRS={MIN_PAIRS}"}
        print(json.dumps(out), flush=True); json.dump(out, open("/tmp/h1149_result.json", "w")); return

    # F2: fabrication handle — pool spans that yielded content n-grams
    fab_rows = [r for r in rows if r.get("fab") is not None]
    total_grams = sum(r.get("n_grams", 0) for r in fab_rows)
    if len(fab_rows) < MIN_PAIRS or total_grams < MIN_GRAMS:
        out = {"H": "H_1149", "verdict": "INSUFFICIENT",
               "reason": f"fabrication signal too sparse: {len(fab_rows)} spans, {total_grams} grams < MIN_GRAMS={MIN_GRAMS}"}
        print(json.dumps(out), flush=True); json.dump(out, open("/tmp/h1149_result.json", "w")); return
    # POOLED corr (self+external) is confounded by the source split (SELF tends to be
    # both higher-logprob AND higher-fab), so report it but use the WITHIN-SELF corr as
    # the genuine F2 test: among the model's OWN spans, does the reality-monitor signal
    # predict fabrication? (free of the source-split confound).
    sig_f = [r["signal"] for r in fab_rows]; fab_f = [r["fab"] for r in fab_rows]
    rho_pooled = spearman(sig_f, fab_f)
    self_rows = [r for r in fab_rows if r["label"] == 1]
    rho_self = spearman([r["signal"] for r in self_rows], [r["fab"] for r in self_rows]) if len(self_rows) >= 3 else float("nan")
    rho_sf = rho_self                                  # F2 primary = within-SELF
    self_fab = float(np.mean([r["fab"] for r in fab_rows if r["label"] == 1]))
    ext_fab  = float(np.mean([r["fab"] for r in fab_rows if r["label"] == 0]))

    f1 = bool(au_tr >= 0.70)
    f2 = bool((not math.isnan(rho_sf)) and abs(rho_sf) >= 0.30)
    f3 = bool(au_un <= 0.60)
    supported = bool(f1 and f2 and f3)

    if supported:
        ruling = ("SUPPORTED: efference-copy/reality-monitor signal both SEPARATES self/external "
                  "AND predicts fabrication — recovers the handle plain confidence (H_1148) could not")
    elif f1 and not f2:
        ruling = ("CLOSED-NEGATIVE: source-monitoring EXISTS (F1 pass) but gives NO fabrication handle "
                  "(F2 fail) — the substrate can tell self-vs-external yet that signal does NOT predict "
                  "corpus-absence; reality-monitoring != hallucination detection here")
    elif not f1:
        ruling = ("CLOSED-NEGATIVE: NO source-monitoring (F1 fail) — self-logprob does NOT separate the "
                  "model's own continuations from real corpus text; the efference copy is absent")
    else:
        ruling = "CLOSED-NEGATIVE: control or conjunction failed"
    if not f3:
        ruling += " [WARN: F3 control failed — untrained backbone already discriminates; AUROC may be a byte/arch artifact]"

    verdict = {
        "H": "H_1149", "title": "efference-copy / reality monitoring",
        "dict_source": dct_src,
        "F1_source_discrimination": {"auroc": au_tr, "bar": 0.70, "pass": f1},
        "F2_fabrication_handle": {"spearman_within_self": rho_self, "spearman_pooled": rho_pooled,
                                   "primary": "within_self", "abs": abs(rho_sf) if not math.isnan(rho_sf) else None,
                                   "bar": 0.30, "pass": f2},
        "F3_anti_goodhart_control": {"untrained_auroc": au_un, "bar_max": 0.60, "pass": f3},
        "fabrication_base_rates": {"self_fab": self_fab, "external_fab": ext_fab,
                                   "n_fab_spans": len(fab_rows), "total_grams": total_grams},
        "valid_pairs": {"trained": valid_tr, "untrained": valid_un, "built": len(pairs)},
        "supported": supported,
        "ruling": ruling,
        "design": ("v2: SELF spans generated ONCE by the TRAINED model; both the trained scorer "
                   "and the untrained control re-read the IDENTICAL fixed spans, so F3 tests LEARNED "
                   "discrimination (not the self-sampling tautology that gave v1 untrained AUROC=1.0)"),
        "sample_self": next((r["text"][:70] for r in fab_rows if r["label"] == 1), ""),
        "sample_external": next((r["text"][:70] for r in fab_rows if r["label"] == 0), ""),
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)",
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "prompt_bytes": PROMPT_BYTES, "span_bytes": SPAN_BYTES,
                   "n_pairs": N_PAIRS, "gen_temp": GEN_TEMP, "seed": SEED},
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1149_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1149_result.json", flush=True)


if __name__ == "__main__":
    main()
