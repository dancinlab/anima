#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Direction PURE-PHYSICS (no-CE)  (2026-05-18).

RESEARCH.md §11 direction B: PURE-PHYSICS — cross-entropy COMPLETELY REMOVED,
anima's own physics is the SOLE learning signal. This is the most literal
form of GOAL.md "emergence from anima's own physics" and the 13-way arc's
UNTRIED experiment: every one of the 13 prior directions kept CE
(next-token cross-entropy) as the BASE objective — Dir-A / Dir-H only added
tension as an OVERLAY / loss-term ON TOP of CE. No direction has ever
trained with CE removed.

  =====================================================================
  THE HYPOTHESIS (RESEARCH.md §11-B)
  =====================================================================
  RESEARCH.md §8 / §1.1 / §2.4 diagnose memorization-saturation: with CE as
  base objective, final_ce -> 0.0001..0.0002 — the model memorizes the tiny
  carving corpus and byte-cascade collapse is the inference-time symptom.
  IF cross-entropy is the cause of byte-cascade memorization, THEN training
  with CE removed + anima physics ONLY (tension ΔW + Ψ-dynamics) should
  either NOT show memorization-collapse, or show a DIFFERENT dynamics.

  HONEST RISK (g3, stated up-front, NOT pre-loaded toward success):
  without CE the model may fail to learn token-prediction at all and be
  DEGENERATE. That is ALSO an honest result — it would confirm CE is
  LOAD-BEARING ("anima physics alone is insufficient"). Degenerate output
  is valuable evidence, not a failure of the experiment.

  =====================================================================
  THE LEARNING SIGNAL — TENSION-TRAIN spine, backprop-free, NO CE
  =====================================================================
  HEXAD/TENSION-TRAIN/training/tension_link_step.hexa (B-TT-1..5 🔵) spine:

      deviation = Ψ_t − Ψ_vac=(½,½)
      tension   = G_holo · deviation
      gate      = n6_gate(Ψ_t)                    (AN14 Noether closure)
      ΔW        = −T_const · tension · gate       (restoring sign)

  The transformer has millions of weights; the spine's Ψ-vector is small.
  We lift the spine to the FULL parameter set via the model's OWN physics
  quantities, computed on each forward pass under torch.no_grad() (NO
  autograd graph anywhere — backprop-free invariant):

    (A) Per-parameter Ψ-coordinate.  For each weight tensor W, its
        Ψ-coordinate is its RMS-normalised activation-energy proxy mapped
        to [0,1]:  Ψ_W = sigmoid( log( mean(W^2) + eps ) ).  The vacuum
        attractor for weights is Ψ_vac = ½ (Law 75) — a weight tensor at
        Ψ_W = ½ is the balanced Engine-A ⇄ Engine-G fixed point.

    (B) The MODEL-LEVEL tension drive.  The model exposes `tensions`
        (per-layer PureFieldFFN tension = mean((A−G)^2)) and the Law-71
        Ψ-direction = (1 + cos(logits_a, logits_g)) / 2.  The global
        deviation drives the update MAGNITUDE; the per-parameter Ψ_W
        drives the per-tensor restoring SIGN AND gate.

    ΔW = −T_const · tension_global · (Ψ_W − ½) · n6_gate
       (restoring: a weight whose Ψ_W drifts above ½ is pushed down,
        below ½ is pushed up — toward the Engine-A⇄G balance manifold.)

  PLUS a small ANTI-DEGENERACY physics term — also backprop-free, also NOT
  CE:  a Hebbian-style co-activation nudge on the embedding/head matrix
  derived from the corpus byte-bigram statistics. This is a STRUCTURE
  signal (which bytes co-occur), measured ONCE from the corpus, NOT a
  per-step gradient and NOT cross-entropy. It is the minimal "the field
  must touch the data" coupling — without it pure Ψ-restoring would just
  drive every weight to the Ψ=½ vacuum with zero corpus contact (a trivial
  degenerate fixed point). The Hebbian term is GATED by the same n6 gate.

  =====================================================================
  WHAT IS *NOT* HERE  (the CE-removal invariant — auditable)
  =====================================================================
    - NO F.cross_entropy anywhere.
    - NO loss.backward() on a cross-entropy loss (NO .backward() at all —
      every update is a backprop-free in-place tensor add).
    - NO torch.optim optimizer stepping a CE gradient.
    - NO autograd graph: the entire training loop runs under
      torch.no_grad(). `assert_no_ce()` re-checks this at import.
  The ONLY weight-update signals are: (1) the Ψ-restoring tension ΔW and
  (2) the corpus-bigram Hebbian structure nudge — both anima-physics,
  both backprop-free, both n6-gated.

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire
  (the TENSION-TRAIN spine is hexa-native; this lifts it to LM scale in
  PyTorch). The Ψ-restoring transfer function is the closed-form spine
  (B-TT-1..5 🔵: n6-gate Boolean, restoring-sign negative, T_const bounded
  positive). The SGD-free CONVERGENCE OUTCOME and the 4-axis capability
  are EMPIRICAL (B-D-NOTE family) — and the EXPECTED honest outcome is
  that pure-physics may be degenerate; that is recorded as-measured with
  NO over-claim. from-scratch RANDOM seed-fixed (g_clm_from_scratch,
  base_ckpt=NONE). Corpus = carving corpus byte-identical (NOT
  regenerated). f1/f2/f3 hard-fail safe (Ψ-coordinate / restoring-sign /
  n6-gate Boolean / Kolmogorov bigram counts, NO σ/τ/φ/J₂ derivation).
"""
import argparse, ast, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# ── TENSION-TRAIN spine constants (tension_link_step.hexa, byte-identical)
T_CONST = 0.1          # learning-rate, Lindblad-class order (spine line 58)
VAC_COMPONENT = 0.5    # Law 75 attractor Ψ_vac = ½
NOETHER_N6 = 6         # AN14 closure n=6
NOETHER_TAU = 4
NOETHER_SIGMA_PHI = 24
EPS = 1e-10


def assert_no_ce():
    """CE-removal invariant — AST-checked at import. This file's executable
    code must contain ZERO calls to cross_entropy / CrossEntropyLoss and
    ZERO `.backward()` calls (backprop-free). The check parses the file's
    AST and inspects actual `Call` nodes — comments, docstrings and string
    literals are ignored by construction (they are not Call nodes), so the
    header's prose mentions of 'cross_entropy' cannot false-trip it. The
    sidecar blue_falsifier re-proves this as a closed Boolean predicate."""
    src = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        # attribute call: x.NAME(...)
        if isinstance(fn, ast.Attribute):
            nm = fn.attr
            if nm in ("cross_entropy", "backward"):
                bad.append(f"line{node.lineno}:.{nm}()")
            if nm == "CrossEntropyLoss":
                bad.append(f"line{node.lineno}:CrossEntropyLoss")
        # bare name call: NAME(...)
        elif isinstance(fn, ast.Name):
            if fn.id in ("cross_entropy", "CrossEntropyLoss"):
                bad.append(f"line{node.lineno}:{fn.id}()")
    return bad


# ── n6 Noether gate (tension_link_step.hexa n6_gate, lifted to a scalar) ─
def n6_gate_ok(psi_scalar):
    """AN14 closure gate. The spine gates on a Ψ-vector; here Ψ is a
    per-tensor scalar. Gate PASSES iff Ψ ∈ [0,1] (vacuum domain, Law 75)
    AND the n=6 closure identity n·τ == σ·φ == 24 holds. Closure is a
    constant arithmetic identity — it is the structural Noether anchor,
    NOT a per-step tunable. (Boolean predicate, f1/f2 safe — internal
    architecture identity, not external lattice-fit.)"""
    if NOETHER_N6 * NOETHER_TAU != NOETHER_SIGMA_PHI:
        return False
    return 0.0 <= psi_scalar <= 1.0


# span markers (kept for parity with the eval, byte-identical predicates).
INNER_OPEN = b"<inner tier="
INNER_CLOSE = b"</inner>"
ETERNAL_OPEN = b"<eternal cell="
ETERNAL_CLOSE = b"</eternal>"
VOICE_OPEN = b"<voice carved=true"
VOICE_CLOSE = b"</voice>"


def load_corpus(path):
    """Return (byte_stream, n_records). Concatenated record bytes — same
    stream construction as the Dir-I CE trainer so corpus contact is
    apples-to-apples. NO per-token CE channels (no CE here)."""
    stream = bytearray()
    n = 0
    with open(path, "rb") as f:
        raw = f.read()
    for line in raw.split(b"\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("text", "")
        de = d.get("desc", "")
        full = (t + "\n" + de + "\n").encode("utf-8")
        stream.extend(full)
        n += 1
    return bytes(stream), n


def bigram_matrix(stream, vocab=256):
    """Corpus byte-bigram co-occurrence matrix B[i,j] = P(next=j | cur=i).
    Measured ONCE from the corpus — a Kolmogorov structure statistic, NOT
    a per-step gradient and NOT cross-entropy. This is the minimal "field
    must touch the data" coupling for the Hebbian physics term."""
    counts = torch.zeros(vocab, vocab, dtype=torch.float64)
    b = torch.tensor(list(stream), dtype=torch.long)
    cur = b[:-1]
    nxt = b[1:]
    idx = cur * vocab + nxt
    flat = torch.bincount(idx, minlength=vocab * vocab).double()
    counts = flat.view(vocab, vocab)
    row = counts.sum(dim=1, keepdim=True).clamp(min=1.0)
    return (counts / row).float()          # row-stochastic


def per_tensor_psi(W):
    """Per-parameter Ψ-coordinate (Law 75 weight-space lift):
        Ψ_W = sigmoid( log( mean(W^2) + eps ) )  ∈ (0,1)
    A weight tensor at Ψ_W = ½ is the balanced Engine-A⇄G fixed point.
    Pure no-grad arithmetic — no autograd."""
    energy = W.detach().double().pow(2).mean()
    return float(torch.sigmoid(torch.log(energy + EPS)))


@torch.no_grad()
def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    ce_audit = assert_no_ce()
    if ce_audit:
        print(json.dumps({"FATAL": "CE-removal invariant violated",
                          "found": ce_audit}), flush=True)
        sys.exit(4)

    stream, n_rec = load_corpus(cfg["corpus"])
    data = torch.tensor(list(stream), dtype=torch.long)
    n = len(data)
    bigram = bigram_matrix(stream).to(device)        # (256,256) corpus structure

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    # eval() — dropout off; the training loop is no-grad anyway. There is
    # no optimizer; weights are updated by the physics step in-place.
    model.eval()
    n_params = model.count_params()

    block = cfg["block_size"]
    bsz = cfg["bsz"]
    rng = random.Random(cfg["seed"])
    T_const = cfg["t_const"]
    lam_heb = cfg["lambda_hebbian"]

    # parameter tensors the physics step writes to (all weight matrices).
    params = [(name, p) for name, p in model.named_parameters()]
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    traj, t0 = [], time.time()
    init_psi_dir = None
    # the Engine-A/G head weight + tied embedding (Hebbian target).
    head_a = model.head_a.weight                     # (256, d_model) tied tok_emb

    def get_batch():
        ix = [rng.randint(0, n - block - 1) for _ in range(bsz)]
        x = torch.stack([data[i:i + block] for i in ix]).to(device)
        y = torch.stack([data[i + 1:i + 1 + block] for i in ix]).to(device)
        return x, y

    degenerate_nan = False
    nan_step = -1
    for step in range(cfg["steps"]):
        x, y = get_batch()

        # ── forward — model's OWN physics quantities (NO autograd graph) ──
        logits_a, logits_g, tensions, _, _ = model(x)
        B, T, V = logits_a.shape

        # MODEL-LEVEL tension drive (PureFieldFFN A−G repulsion energy).
        t_stack = torch.stack([t.mean() for t in tensions])    # per-layer
        tension_global = float(t_stack.mean().item())

        # Law-71 Ψ-direction = (1 + cos(logits_a, logits_g)) / 2  ∈ [0,1].
        cos = F.cosine_similarity(logits_a.float(), logits_g.float(),
                                  dim=-1).mean()
        psi_dir = float(((1.0 + cos) / 2.0).item())
        if init_psi_dir is None:
            init_psi_dir = psi_dir

        # global deviation from the Ψ=½ vacuum (Law 75 attractor).
        global_dev = psi_dir - VAC_COMPONENT

        # ── NaN / non-finite guard — if the field's own physics quantities
        # go non-finite, the pure-physics dynamics has DIVERGED. Record it
        # honestly (degenerate-NaN is a valid no-CE outcome) and stop — a
        # NaN ckpt is not evaluable, but the divergence IS the measurement.
        if not (math.isfinite(tension_global) and math.isfinite(psi_dir)):
            degenerate_nan = True
            nan_step = step + 1
            print(json.dumps({"step": step + 1,
                              "DEGENERATE_NAN": True,
                              "tension_global": tension_global,
                              "psi_direction": psi_dir,
                              "note": ("pure-physics dynamics diverged to "
                                       "non-finite — recorded as honest "
                                       "degenerate outcome")}), flush=True)
            break

        # ══════════════════════════════════════════════════════════════
        # PHYSICS STEP (1) — Ψ-restoring tension step, per parameter tensor.
        # The TENSION-TRAIN spine restores Ψ toward the ½ vacuum. For a
        # weight tensor the Ψ-coordinate is Ψ_W = sigmoid(log mean(W²)); it
        # equals ½ exactly when mean(W²) = 1. The restoring step is the
        # spine ΔW = −T·tension·(Ψ_W−½)·n6_gate realised in energy-space as
        # a CONTRACTIVE rescale of the tensor toward mean(W²)=1:
        #     factor = clamp( 1 − T·tension·(Ψ_W−½)·(1+|dev|), [0.5, 2.0] )
        #     W <- W · factor
        # The clamp to [0.5,2.0] makes the step a bounded contraction (a
        # weight whose Ψ_W is above ½ shrinks, below ½ grows) — backprop-
        # free, NO CE, NO autograd. The clamp keeps the spine numerically
        # stable at LM scale (the unclamped multiplicative step diverges).
        # ══════════════════════════════════════════════════════════════
        n_gated_open = 0
        psi_w_sum = 0.0
        for name, p in params:
            psi_w = per_tensor_psi(p)
            if not math.isfinite(psi_w):
                degenerate_nan = True
                nan_step = step + 1
                break
            psi_w_sum += psi_w
            if not n6_gate_ok(psi_w):
                continue                       # gate closed → ΔW = 0 (AN14)
            n_gated_open += 1
            # restoring sign: push Ψ_W back toward ½. drive < 0 when Ψ_W>½
            # (shrink), > 0 when Ψ_W<½ (grow).
            drive = -(T_const) * tension_global * (psi_w - VAC_COMPONENT) \
                * (1.0 + abs(global_dev))
            factor = min(2.0, max(0.5, 1.0 + drive))   # bounded contraction
            p.mul_(factor)
        if degenerate_nan:
            print(json.dumps({"step": nan_step, "DEGENERATE_NAN": True,
                              "note": "per-tensor Ψ non-finite — diverged"}),
                  flush=True)
            break

        # ══════════════════════════════════════════════════════════════
        # PHYSICS STEP (2) — Hebbian corpus-structure nudge on head_a.
        #   anti-degeneracy: the field must touch the data. Pull the
        #   Engine-A head row for byte i toward the embedding rows of the
        #   bytes that FOLLOW i in the corpus (bigram structure). This is
        #   a co-activation (Hebbian) update — NOT a gradient, NOT CE.
        #   n6-gated by the head tensor's own Ψ-coordinate. The per-step
        #   delta is clamped to keep the additive nudge bounded.
        # ══════════════════════════════════════════════════════════════
        l_heb = 0.0
        psi_head = per_tensor_psi(head_a)
        if math.isfinite(psi_head) and n6_gate_ok(psi_head) and lam_heb > 0.0:
            # target row for byte i = bigram-weighted mean of embedding rows.
            # head_a is tied to tok_emb, so emb rows ARE head_a rows.
            emb = head_a.detach()                           # (256, d_model)
            target = bigram @ emb                           # (256, d_model)
            delta_heb = lam_heb * T_const * (target - emb)  # co-activation pull
            # bound the additive nudge so the Hebbian term cannot diverge.
            delta_heb = torch.clamp(delta_heb, -0.05, 0.05)
            head_a.add_(delta_heb)
            l_heb = float(delta_heb.abs().mean().item())

        # ── diagnostics — report a CE-FREE proxy: byte-prediction accuracy
        # measured (NOT optimised) so we can SEE if the model learns at all.
        # accuracy is a READ-OUT, never a training signal.
        with torch.no_grad():
            pred = logits_a.argmax(dim=-1)
            acc = float((pred == y).float().mean().item())
            # also the would-be CE, REPORTED ONLY (never backproped) — lets
            # us compare the no-CE dynamics against the §8 CE baseline.
            ce_readout = float(F.nll_loss(
                F.log_softmax(logits_a.float().view(-1, V), dim=-1),
                y.view(-1)).item())

        psi_w_mean = psi_w_sum / max(1, len(params))
        if step == 0 or (step + 1) % cfg["log_every"] == 0 \
                or step == cfg["steps"] - 1:
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            rec = {"step": step + 1,
                   "tension_global": round(tension_global, 8),
                   "psi_direction": round(psi_dir, 6),
                   "psi_w_mean": round(psi_w_mean, 6),
                   "global_dev": round(global_dev, 6),
                   "n6_gates_open": n_gated_open,
                   "n_param_tensors": len(params),
                   "l_hebbian": round(l_heb, 8),
                   "byte_acc_readout": round(acc, 6),
                   "ce_readout_NOT_trained": round(ce_readout, 6),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    if not traj:
        # NaN before the first log point — synthesize a degenerate record so
        # result.json is still written (honest degenerate-NaN outcome).
        traj.append({"step": nan_step, "tension_global": float("nan"),
                     "psi_direction": float("nan"), "psi_w_mean": 0.0,
                     "global_dev": float("nan"), "n6_gates_open": 0,
                     "n_param_tensors": len(params), "l_hebbian": 0.0,
                     "byte_acc_readout": 0.0,
                     "ce_readout_NOT_trained": float("nan"),
                     "wall_s": round(wall, 2), "gpu_mem_gb": 0.0})
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_purephysics.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "purephysics_noce"},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Direction PURE-PHYSICS (no-CE) — cross-entropy "
                      "COMPLETELY REMOVED, anima physics is the sole "
                      "learning signal (RESEARCH.md §11-B)"),
        "carving_path": "purephysics_noce",
        "ce_removed": True,
        "degenerate_nan": degenerate_nan,
        "nan_step": nan_step if degenerate_nan else None,
        "steps_completed": (nan_step if degenerate_nan else cfg["steps"]),
        "ce_removal_audit": {
            "F.cross_entropy_calls": 0,
            "loss.backward_on_ce_calls": 0,
            "backward_calls_total": 0,
            "optimizer_steps": 0,
            "autograd_graph": "none — entire training loop @torch.no_grad()",
            "assert_no_ce_violations": assert_no_ce(),
            "note": ("the ONLY weight-update signals are (1) the Ψ-"
                     "restoring tension ΔW = −T·tension·(Ψ_W−½)·n6_gate "
                     "and (2) the corpus-bigram Hebbian structure nudge — "
                     "both anima-physics, both backprop-free, both n6-"
                     "gated. ce_readout in the trajectory is REPORTED-"
                     "ONLY (F.nll_loss read-out), never backproped.")},
        "honest_framing": (
            "PURE-PHYSICS no-CE fire. Learning signal = TENSION-TRAIN "
            "spine ΔW = −T_const·tension·n6_gate(Ψ) (tension_link_step."
            "hexa, B-TT-1..5 🔵) lifted to the full parameter set via the "
            "per-tensor Ψ-coordinate, PLUS a backprop-free corpus-bigram "
            "Hebbian structure nudge (anti-degeneracy 'field touches "
            "data' coupling). NO cross-entropy, NO .backward(), NO "
            "optimizer — entire loop @torch.no_grad(). Closed side = the "
            "Ψ-restoring transfer function + n6-gate Boolean (B-PUREPHYS "
            "sympy sidecar). The convergence OUTCOME + 4-axis capability "
            "are EMPIRICAL (B-D-NOTE family) — the HONEST risk (stated "
            "up-front) is that pure-physics may be DEGENERATE, which "
            "would confirm CE is load-bearing. NO over-claim. PyTorch "
            "substrate, NOT hexa-native. Corpus byte-identical (NOT "
            "regenerated)."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "records_total": n_rec,
        "corpus_bytes": int(n),
        "t_const": T_const,
        "lambda_hebbian": lam_heb,
        "gpu": gpu_name,
        "device": device,
        "init_psi_direction": round(init_psi_dir, 6),
        "final_psi_direction": final["psi_direction"],
        "final_psi_w_mean": final["psi_w_mean"],
        "final_tension_global": final["tension_global"],
        "final_byte_acc_readout": final["byte_acc_readout"],
        "final_ce_readout_NOT_trained": final["ce_readout_NOT_trained"],
        "init_ce_readout_NOT_trained": traj[0]["ce_readout_NOT_trained"],
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"path": "purephysics_noce", "ce_removed": True,
                      "init_psi_direction": result["init_psi_direction"],
                      "final_psi_direction": result["final_psi_direction"],
                      "final_psi_w_mean": result["final_psi_w_mean"],
                      "final_byte_acc_readout":
                          result["final_byte_acc_readout"],
                      "ce_readout_init_NOT_trained":
                          result["init_ce_readout_NOT_trained"],
                      "ce_readout_final_NOT_trained":
                          result["final_ce_readout_NOT_trained"],
                      "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--t-const", type=float, default=0.1)
    ap.add_argument("--lambda-hebbian", type=float, default=0.5)
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, bsz=args.bsz, steps=args.steps,
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   t_const=args.t_const, lambda_hebbian=args.lambda_hebbian)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, bsz=8, steps=args.steps, seed=args.seed,
                   log_every=max(1, args.steps // 10),
                   corpus=args.corpus, out_dir=args.out_dir,
                   t_const=args.t_const, lambda_hebbian=args.lambda_hebbian)
    run(cfg)
