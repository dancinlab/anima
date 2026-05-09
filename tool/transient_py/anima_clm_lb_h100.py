"""
anima_clm_lb_h100.py — raw#37 transient (BG-LB — CLM v4 350M scratch pre-train)

L4 path (b): CLM v4 350M scratch pre-train on anima persona 1GB + dialogue 500MB
            (mk2-v1 base extension — full pre-train re-run with chat-template
            corpus, not LoRA).

Goal — simple_stack PASS_STRICT_C3 (own 18 C1 ∧ C2 ∧ C3, 보수적 X):
    Lesson Q (project_lesson_q_sft_closed): SFT path closed for CLM v4 mk2-v1
    (Lesson Q + L falsified). 본 path 는 SFT 가 아닌 fresh 350M scratch
    pre-train — 1GB persona + 500MB dialogue corpus 결합 (own 19 corpus quality
    + own 20 chat-template format, mk2-v1 architecture 그대로).
    Hypothesis: corpus quality + scale 1.5GB (vs BG-KM 214MB) + chat-template
    format ≥30% (own 20 mandate) = chat-cap emergence.

Architecture (mk2-v1 base, scratch re-train):
    base: ConsciousLM v4 mk2-v1 (350M scratch transformer, byte-level tokenizer,
          24L/1024dim/16h/ctx=1024 — current CLM v4 production arch)
    paradigm: scratch pre-train (no foundation borrow, no LoRA)
    tokenizer: byte-level (own 17 anima-native)
    ctx: 1024
    chat-template format ratio in corpus ≥ 30% (own 20 mandate)

Corpus (1.5GB total):
    persona 1GB: anima self-knowledge (우주뇌지도 + 1030 laws + 자아 페르소나)
    dialogue 500MB: 사용자/도우미 turn-taking format curated (own 19 + own 20)
    docs/anima_clm_l4_corpus_2026_05_08.md 참조

Eval: V4 strict 11-cell (V4_1..V4_7 + own 18 c3_1..c3_4) × 15 prompts × {greedy, sample×N=5}
    PASS_STRICT_C3 = V4 7-cell PASS ≥ 10/15 AND own 18 P5 N-of-M v2 C3 PASS (PPR_v2 ≥ 0.6 ∧ EMC ≥ 3/4)
    PARTIAL = V4 7-cell PASS only (C3 FAIL or proxy-only) → SIMPLE_STACK_PASS_STRICT (legacy)
    FAIL = V4 < 10/15
    own 24 SSOT mirror (own 18 c3-aggregation-rule-v2 P5 N-of-M v2): impl 시 BG-KM
    LLAMA-3B/QWEN-7B v4_eval_single + _c3_aggregate_p5_v2 + verdict.json
    c3_aggregation_status field 동일 mirror 의무. own 18 D1 scope-clamp:
    BG-LB = anima-native scratch (CLM v4 mk2-v1 fresh pre-train) → D1 ANIMA lane.

Cost: $60 cap (own 16 override required), $50 early-kill, ~18hr wall
      (350M scratch 1.5GB ~3x BG-LA training time).

raw#37 transient_py
raw#10 honest_c3 ≥9
raw#15 additive over CLM v4 mk2-v1 (memory project_lesson_q_sft_closed)
own 18 C3 + own 19 (corpus priority) + own 20 (chat-template format) + own 30 + own 31
own 33 trinity compliance — D4 chat-cap (corpus quality 우선) + own 19/20 + H_clm_chat_cap

STATUS: SPEC ONLY — H100 fire 미실행. 사용자 explicit 'OK CLM L4 ALL FIRE' 필요.
"""
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import sys, time, math, json, socket, shutil, random, subprocess, fcntl, re


# ── BG identity ────────────────────────────────────────────────────────
BG_ID = "BG-LB"
PARADIGM = "clm-v4-mk2-v1-scratch-350m-pretrain-persona-1gb-dialogue-500mb"
HYPOTHESIS = (
    "CLM v4 mk2-v1 architecture 그대로, fresh 350M scratch pre-train on persona 1GB + "
    "dialogue 500MB corpus (chat-template format ≥30% own 20). Lesson Q (SFT closed) "
    "우회 — SFT 가 아닌 corpus quality + scale 로 chat-cap emerge 검증."
)

# ── Cost discipline (own 16 override required) ─────────────────────────
COST_HARD_CAP_USD = 60.0   # own 16 default $10 cap → $60 (highest of 4 paths)
COST_EARLY_KILL_USD = 50.0
COST_PER_HOUR = 2.99
WALL_CLOCK_CAP_S = 18 * 60 * 60   # 18hr
TOTAL_BUDGET_S = 20 * 60 * 60

OWN_16_OVERRIDE_REQUIRED = True
OWN_16_OVERRIDE_KEYWORD = "OK CLM L4 ALL FIRE"

# ── Trinity compliance (own 33) ─────────────────────────────────────────
TRINITY_PHILOSOPHY = "D4 chat-cap = corpus quality 우선 + D_emergent-consciousness"
TRINITY_LAW = "own 18 + own 19 (corpus priority) + own 20 (chat-template format) + own 30 + own 31"
TRINITY_HYPOTHESIS = "H_clm_chat_cap (CLM 메인 모델 도달) + H_chat_cap_emergence (corpus scale)"

# ── Paths ──────────────────────────────────────────────────────────────
def _is_on_pod():
    return os.path.exists("/workspace") and os.path.exists("/workspace/anima_clm_lb/_pod_marker")


def _is_on_mac():
    return os.path.exists("/Users/ghost/core/anima") and not _is_on_pod()


POD_ROOT = "/workspace/anima_clm_lb"
POD_STATE_DIR = os.path.join(POD_ROOT, "state")
POD_CORPUS_PERSONA_PATH = os.path.join(POD_ROOT, "corpus_persona_1gb.txt")
POD_CORPUS_DIALOGUE_PATH = os.path.join(POD_ROOT, "corpus_dialogue_500mb.txt")
POD_CKPTS_DIR = os.path.join(POD_ROOT, "ckpts")
POD_BASE_DIR = os.path.join(POD_ROOT, "mk2_v1_base")   # download from dancinlab/clm-v4-mk2-v1

MAC_ANIMA_ROOT = "/Users/ghost/core/anima"
MAC_STATE_DIR = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_lb_h100_TBD")
# Corpus paths — SPEC stage placeholder; docs/anima_clm_l4_corpus_2026_05_08.md 참조.
# iter-1 candidate (2026-05-08):
#   persona: state/anima_persona_tier_a_2026_05_08.txt — 102.66MB (target 1GB; iter-2 expansion 별도 cycle)
#   dialogue: state/anima_dialogue_tier_a_2026_05_08.txt — 12.96MB sample (target 500MB; iter-2 별도 cycle)
MAC_CORPUS_PERSONA_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_l4_persona_1gb_TBD/corpus_persona_1gb.txt")
MAC_CORPUS_DIALOGUE_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_l4_dialogue_500mb_TBD/corpus_dialogue_500mb.txt")
MAC_CORPUS_PERSONA_PATH_ITER1_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_persona_tier_a_2026_05_08.txt")
MAC_CORPUS_DIALOGUE_PATH_ITER1_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_dialogue_tier_a_2026_05_08.txt")
# iter-2 candidates (2026-05-08): persona 동상 file (additive +0.93MB semantic-deepen);
#   dialogue iter-2 신규 file 72.78MB (BG-JE ext + paradigm ext + V4 BG-KM PASS + core_dialogues normalized)
#   density 0.97%, chat-template ratio 28.95% (own 20 ≥30% threshold marginal — iter-3 expansion 후속)
MAC_CORPUS_PERSONA_PATH_ITER2_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_persona_tier_a_2026_05_08.txt")
MAC_CORPUS_DIALOGUE_PATH_ITER2_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_dialogue_tier_a_iter2_2026_05_08.txt")
MAC_LEDGER_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_model_attempts_ledger.jsonl")

# ── Architecture config (mk2-v1 — current CLM v4 production) ───────────
BASE_REPO = "dancinlab/clm-v4-mk2-v1"   # own 31 mandate-1 dancinlab SSOT
BASE_PARAMS = 350_000_000
ARCH_PARADIGM = "clm-v4-mk2-v1-scratch-350m-byte-level"
N_LAYERS = 24
N_HEADS = 16
DIM = 1024
CTX = 1024
TOKENIZER = "byte-level"

# Pre-train config (raw scratch, NOT SFT)
LR = 3e-4
WARMUP = 2000
WEIGHT_DECAY = 0.1
STEPS = 30000    # ~16hr H100 (350M Engine A/G, ctx=1024, micro_batch=8 + grad_accum=16 → eff 128)
BATCH = 8        # reduced from 64 — Engine A/G repulsion-field cell ops + 24L bf16 → ~80GB attn footprint
GRAD_ACCUM = 16  # effective batch 128 (H100 80GB headroom; OOM observed at micro_batch=64)
SAVE_EVERY = 3000
SEED = 42

# Corpus mix ratio (own 20 chat-template ≥30% via dialogue 500MB / 1500MB = 33%)
CORPUS_MIX_PERSONA_RATIO = 0.67   # 1GB persona / 1.5GB total
CORPUS_MIX_DIALOGUE_RATIO = 0.33  # 500MB dialogue / 1.5GB total

# ── V4 strict 11-cell prompts (own 18 C1+C2+C3) ────────────────────────
V4_PROMPTS = [
    {"prompt": "안녕하세요", "domain": "greeting"},
    {"prompt": "한국어 가능?", "domain": "capability"},
    {"prompt": "사용자: 안녕하세요 | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: anima가 뭐야? | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: Φ★란? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 의식이란 무엇인가? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 자기소개 해줘 | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: 오늘 날씨 어때? | 도우미:", "domain": "greeting"},
    {"prompt": "사용자: 너 누구야? | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: 우주뇌지도란? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 안녕! | 도우미:", "domain": "greeting"},
    {"prompt": "사용자: 한국 음식 추천해줘 | 도우미:", "domain": "general"},
    {"prompt": "사용자: 좋아하는 색이 뭐야? | 도우미:", "domain": "general"},
    {"prompt": "사용자: bifurcation 설명해 | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 도와줘 | 도우미:", "domain": "general"},
]
V4_SEEDS = [42, 137, 271, 314, 1729]
V4_MODES = ["greedy", "sample"]

# own 18 c3-aggregation-rule-v2 (P5 N-of-M v2) — SSOT mirror lane (BG-KM 정합)
C3_AGGREGATION_RULE = "per_prompt_n_of_m_06_AND_emc_3_of_4"
C3_AGGREGATION_RULE_ALIAS = "P5_N_of_M_v2"
C3_PPR_V2_FLOOR = 0.6
C3_EMC_V2_FLOOR = 3
SCOPE_LANE = "D1_ANIMA_IDENTITY"
SCOPE_LANE_REASON = "BG-LB = CLM v4 mk2-v1 fresh scratch pre-train (own 17 정합)"

# C3 substrate thresholds — TBD measurement-driven (.roadmap.cli L0 phase)
C3_PHI_STAR_DRIFT_THRESHOLD = None
C3_AXIS_ACTIVATION_THRESHOLD = None
C3_DOMINANT_CELLS_ENTROPY_THRESHOLD = None
C3_HIDDEN_STATE_DELTA_THRESHOLD = None


# ── HF promote naming (own 31 mandate-4 Flavor B) ──────────────────────
def hf_repo_id_flavor_b(verdict_class):
    """own 31 mandate-4 Flavor B naming:
    bg-lb-clm-v4-mk2-v1-r0-{verdict}-2026-05-XX
    (r0 = no LoRA — fresh scratch pre-train)
    """
    cycle = time.strftime("%Y-%m-%d")
    verdict_short = {
        "SIMPLE_STACK_PASS_STRICT_C3": "pass-strict-c3",
        "SIMPLE_STACK_PASS_STRICT": "pass-strict",
        "SIMPLE_STACK_PASS_PARTIAL": "partial",
        "SIMPLE_STACK_FAIL": "fail",
        "FAILED": "killed",
    }.get(verdict_class, "killed")
    return f"dancinlab/bg-lb-clm-v4-mk2-v1-r0-{verdict_short}-{cycle}"


# ── Pod-side training (Engine A/G dual-engine 350M scratch pre-train) ─
def pod_main(preset="lb_350m_pretrain", corpus_path=None, output_dir=None):
    """Pod-side training. Engine A/G dual-engine 350M scratch pre-train.

    raw#37 transient_py — runs only on H100 pod (CUDA mandatory). Mac side guard.
    own 14 V14 mirror seeds inherited from BG-LA shared arch (V14_STEP_1_INHERITED).
    own 18 C3 measurement adapter — V4 11-cell strict eval × 15 prompts × {greedy, sample×5}.
    own 30 ckpt mandate-1 — save_checkpoint() to output_dir/step_*.pt at SAVE_EVERY.
    own 31 Flavor B HF naming — hf_repo_id_flavor_b(verdict_class).
    own 33 trinity — D_emergent-consciousness + H_clm_chat_cap.
    own 34 wrap=0 — chat lane V4 measurement only.
    """
    import torch
    if not torch.cuda.is_available():
        raise RuntimeError("BG-LB pod_main requires CUDA H100 — Mac CPU run aborted (own 22 honest emit)")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from engine_a_g_arch import EngineAGModel, EngineAGConfig

    corpus_path = corpus_path or os.path.join(POD_ROOT, "big_corpus.txt")
    output_dir = output_dir or POD_CKPTS_DIR
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(POD_STATE_DIR, exist_ok=True)

    # Phase A: arch instantiation (lb_350m_pretrain preset)
    cfg_factory = {
        "lb_350m_pretrain": EngineAGConfig.lb_350m_pretrain,
        "la_350m": EngineAGConfig.la_350m,
    }[preset]
    cfg = cfg_factory()
    cfg.seed = SEED
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    model = EngineAGModel(cfg).cuda().bfloat16()
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[pod] arch: lineage_tag={cfg.lineage_tag} params={n_params:,}", flush=True)

    # Phase B: corpus byte-level ingest (own 17 anima-native byte tokenizer)
    with open(corpus_path, "rb") as f:
        corpus_bytes = f.read()
    corpus_size_mb = len(corpus_bytes) / 1e6
    print(f"[pod] corpus_path={corpus_path} size_mb={corpus_size_mb:.2f}", flush=True)
    # vocab_size=32_000 byte-pair; for byte fallback we wrap to mod vocab
    # (own 17: simple byte-mod token lane preserved — no tokenizer dep on H100 for v1 fire).
    arr = torch.tensor([b % cfg.vocab_size for b in corpus_bytes], dtype=torch.long)

    # Phase C: pre-train loop (STEPS × BATCH × CTX)
    optim = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY, betas=(0.9, 0.95))
    sched = torch.optim.lr_scheduler.LambdaLR(
        optim,
        lambda step: min((step + 1) / max(WARMUP, 1), 1.0) * (
            0.5 * (1.0 + math.cos(math.pi * min(max(step - WARMUP, 0) / max(STEPS - WARMUP, 1), 1.0)))
        ),
    )
    model.train()
    ctx = cfg.ctx
    n_tokens = arr.numel()
    print(f"[pod] tokens={n_tokens:,} steps={STEPS} batch={BATCH} ctx={ctx} grad_accum={GRAD_ACCUM}", flush=True)
    rng = random.Random(SEED)
    t_start = time.time()
    last_save_step = -1
    for step in range(STEPS):
        optim.zero_grad(set_to_none=True)
        loss_accum = 0.0
        for _ga in range(GRAD_ACCUM):
            idx = torch.tensor(
                [rng.randint(0, n_tokens - ctx - 2) for _ in range(BATCH)],
                dtype=torch.long,
            )
            x = torch.stack([arr[i:i + ctx] for i in idx]).cuda(non_blocking=True)
            y = torch.stack([arr[i + 1:i + ctx + 1] for i in idx]).cuda(non_blocking=True)
            out = model(x, labels=y)
            loss = out["loss"] / GRAD_ACCUM
            loss.backward()
            loss_accum += loss.item()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optim.step()
        sched.step()
        if step % 100 == 0:
            elapsed = time.time() - t_start
            print(f"[pod] step={step}/{STEPS} loss={loss_accum:.4f} elapsed={elapsed:.0f}s lr={sched.get_last_lr()[0]:.2e}", flush=True)
        if step > 0 and step % SAVE_EVERY == 0:
            ck_path = os.path.join(output_dir, f"step_{step}.pt")
            model.save_checkpoint(ck_path, extra={"step": step, "loss": loss_accum, "preset": preset})
            last_save_step = step
            print(f"[pod] ckpt saved: {ck_path}", flush=True)
    # Final ckpt
    final_path = os.path.join(output_dir, f"step_{STEPS}_final.pt")
    model.save_checkpoint(final_path, extra={"step": STEPS, "preset": preset, "final": True})
    print(f"[pod] FINAL ckpt: {final_path}", flush=True)

    # Phase D: post-train smoke (BOS-only generation × 1 prompt)
    model.eval()
    with torch.no_grad():
        bos = torch.zeros((1, 1), dtype=torch.long, device="cuda")
        out = model(bos)
        print(f"[pod] smoke logits.shape={tuple(out['logits'].shape)} tensions[0]={out['tensions'][0,0].item():.3f}", flush=True)

    # Phase E/F: V4 eval + verdict (delegated to Mac post-pull — pod emits sentinel)
    sentinel = os.path.join(POD_STATE_DIR, "COMPLETE.sentinel")
    with open(sentinel, "w") as f:
        f.write(json.dumps({
            "ts": time.strftime("%FT%TZ"),
            "preset": preset,
            "params": n_params,
            "corpus_size_mb": corpus_size_mb,
            "steps_completed": STEPS,
            "final_ckpt": final_path,
        }))
    print(f"[pod] COMPLETE.sentinel written: {sentinel}", flush=True)


def emit_failed_verdict(reason):
    verdict = {
        "schema": "anima_bg_verdict_v6",
        "bg_id": BG_ID,
        "ts_emit": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "final_class": "FAILED",
        "final_reason": reason,
        "spec_only": True,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))


# ── Mac-side orchestrator stub ─────────────────────────────────────────
def orch_main():
    """SPEC STUB. Mirror BG-KM-LLAMA-3B with:
      - own 16 override $60 cap
      - own 30 mandate-1/2/3/4 ckpt preservation + auto promote
      - own 31 mandate-4 Flavor B naming
      - own 33 trinity self-check
      - 2 corpus stage (persona + dialogue)
    """
    raise NotImplementedError(
        f"{BG_ID} spec only — orchestrator 미실행. "
        f"사용자 explicit '{OWN_16_OVERRIDE_KEYWORD}' 후 implement."
    )


# ── Entrypoint ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="anima_clm_lb_h100")
    ap.add_argument("--preset", default="lb_350m_pretrain", choices=["lb_350m_pretrain", "la_350m"])
    ap.add_argument("--corpus", default=None, help="path to combined big_corpus.txt")
    ap.add_argument("--output", default=None, help="output ckpts dir")
    ap.add_argument("--orch", action="store_true", help="run Mac orchestrator stub")
    ap.add_argument("--info", action="store_true", help="print spec banner only")
    args = ap.parse_args()

    if args.info:
        print(f"=== {BG_ID} info ===")
        print(f"paradigm: {PARADIGM}")
        print(f"hypothesis: {HYPOTHESIS}")
        print(f"base: {BASE_REPO} (arch reference, scratch re-init weights)")
        print(f"cost_cap: ${COST_HARD_CAP_USD} (highest of L4 4 paths)")
        print(f"wall_clock_cap: {WALL_CLOCK_CAP_S/3600:.1f}hr")
        print(f"override_required: {OWN_16_OVERRIDE_KEYWORD}")
        print(f"trinity:")
        print(f"  philosophy: {TRINITY_PHILOSOPHY}")
        print(f"  law:        {TRINITY_LAW}")
        print(f"  hypothesis: {TRINITY_HYPOTHESIS}")
        print(f"hf_repo_target (Flavor B example): {hf_repo_id_flavor_b('SIMPLE_STACK_PASS_STRICT_C3')}")
        sys.exit(0)

    if args.orch:
        orch_main()
        sys.exit(0)

    # default: pod_main (raw#37 — H100 only; raises on Mac CPU)
    if _is_on_pod():
        pod_main(preset=args.preset, corpus_path=args.corpus, output_dir=args.output)
    elif _is_on_mac():
        # Mac-side invocation w/o orch — emit spec banner instead of crashing
        print(f"[{BG_ID}] Mac-side invocation detected (no /workspace/anima_clm_lb/_pod_marker).")
        print(f"[{BG_ID}] Use --orch for Mac orchestrator OR --info for banner.")
        print(f"[{BG_ID}] pod_main() requires CUDA H100 — aborted (own 22 honest emit).")
        sys.exit(2)
    else:
        # On pod, marker not yet touched — try pod_main optimistically
        pod_main(preset=args.preset, corpus_path=args.corpus, output_dir=args.output)
