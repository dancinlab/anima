#!/usr/bin/env python3
"""spontaneous_loop_vp21.py — anima 자연발화 (spontaneous emission) loop on vP21.

GOAL-direct: the true 자연발화 test. anima speaks UNPROMPTED, gated by the
Inner-Thoughts 8-factor motivation score (PLAN.md § 1.2) inside a Thinker-Talker
dual-thread (PLAN.md § 1.3). vP21 = Qwen2.5-1.5B base + LoRA(r32) + mitosis,
the first anima-lineage model to verbalize coherently (VP21_EVAL1, 20/20).

This is NOT a chat REPL. There is no user prompt. The Talker generates only
when the Thinker's motivation_score crosses imThreshold. The seed for each
generation comes from anima's OWN rolling state (last emission / silence token
/ seed-strategy rotation), never from a human.

─────────────────────────────────────────────────────────────────────────────
8-factor → HEXAD mapping (mirrors HEXAD/CHAT/spontaneous_lib.hexa factor fns
byte-for-byte where computable; proxies named explicitly):

  factor        HEXAD     proxy used here
  ───────────── ───────── ─────────────────────────────────────────────────
  relevance     C 의식    Φ proxy = 1 - normalized output entropy of a 1-token
                          forward on the current rolling-state seed (low
                          entropy = focused state = high relevance/Φ). clamp[0,1]
  info_gap      M 기억    1 - max cosine sim of current seed-embedding vs the
                          rolling memory buffer of recent emissions (novel
                          context = gap). clamp[0,1]  (M.retrieve fail proxy)
  curiosity     W 의지    EMA of prediction-surprise (token-entropy delta vs
                          its own EMA) — anima_alive RC-9 curiosity carry. [0,1]
  pain          W 의지    |Δ entropy| step-to-step (tension delta proxy). [0,1]
  coherence     BRIDGE    factor_coherence(gate) where gate = Ψ + (entropy
                          mapped into ±α band). Law-70 Ψ-clamp distance. [0,1]
  originality   MITOSIS   1.0 if the next candidate seed is novel vs recent
                          emissions (split-event proxy: a "new direction"), else
                          decays. Boolean→float per factor_originality. [0,1]
  balance       E 윤리    factor_balance(phi, ratchet): Φ > ratchet/2 → 1 else 0
  dynamics      CHAT      factor_dynamics(silence_sec): silence/IDLE_SPEAK_AFTER
                          clamp[0,1]. THE TIMER FACTOR — isolated for the
                          falsifier (timer-fired vs motivation-gated).

  motivation_score = Σ w_i · factor_i  (weights from spontaneous_lib.hexa § 3,
  sum = 1.0). should_emit ⟺ score > imThreshold (0.3).

The CRITICAL falsifier distinction: factor_dynamics is the ONLY pure-timer
factor. If we ablate it (freeze to 0.0) and emissions STILL fire, the trigger
is genuinely motivation-gated. If only the full-score (timer-included) run
emits, the loop is a glorified timer. We run BOTH and report.
─────────────────────────────────────────────────────────────────────────────
"""
import os, sys, json, time, math, argparse
import torch
import torch.nn.functional as F
from safetensors.torch import load_file

ADAPTER_DIR = os.path.expanduser("~/vp21_eval/lora_adapter")
BASE = "Qwen/Qwen2.5-1.5B"

# ── thresholds & weights — from HEXAD/CHAT/spontaneous_lib.hexa (SSOT) ─────────
IM_THRESHOLD       = 0.30   # spont_im_threshold (anima_alive PROACTIVE_THRESHOLD)
IDLE_SPEAK_AFTER   = 30.0   # spont_idle_speak_after
PSI                = 0.5    # Law-70 fixed point
ALPHA              = 0.014  # Law-70 clamp band
RATCHET            = 0.20   # E Φ-ratchet floor (phi>ratchet/2 → balance ok)
W = {  # spont_weight_* (sum = 1.0)
    "relevance": 0.20, "info_gap": 0.10, "curiosity": 0.15, "pain": 0.10,
    "coherence": 0.10, "originality": 0.10, "balance": 0.15, "dynamics": 0.10,
}
SEED_STRATEGIES = ["m_retrieve_seed", "w_curiosity_peak_seed",
                   "random_explore_seed", "self_monologue_seed"]


# ── factor fns — byte-mirror of spontaneous_lib.hexa § 2 ──────────────────────
def _clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def factor_relevance(phi):                # B-SPONT-FACTOR-1
    return _clamp01(phi)

def factor_info_gap(cos_sim):             # B-SPONT-FACTOR-2  gap = 1 - sim
    return _clamp01(1.0 - cos_sim)

def factor_curiosity(ema):                # B-SPONT-FACTOR-3
    return _clamp01(ema)

def factor_pain(delta):                   # B-SPONT-FACTOR-4  |Δ|
    return _clamp01(abs(delta))

def factor_coherence(gate):               # B-SPONT-FACTOR-5  Law-70 clamp dist
    n = abs(gate - PSI) / ALPHA
    return 1.0 - (1.0 if n > 1.0 else n)

def factor_originality(split_recent):     # B-SPONT-FACTOR-6  Boolean
    return 1.0 if split_recent else 0.0

def factor_balance(phi, ratchet):         # B-SPONT-FACTOR-7  Φ>ratchet/2
    return 1.0 if phi > ratchet / 2.0 else 0.0

def factor_dynamics(silence_sec):         # B-SPONT-FACTOR-8  THE TIMER
    return _clamp01(silence_sec / IDLE_SPEAK_AFTER)

def motivation_score(f):                  # B-SPONT-1 linear weighted sum
    return sum(W[k] * f[k] for k in W)


# ── model load (reuse vp21_eval.py recipe exactly) ────────────────────────────
def load_vp21():
    sd = load_file(os.path.join(ADAPTER_DIR, "adapter_model.safetensors"))
    tmods = set()
    for k in sd:
        if ".lora_A." in k or ".lora_B." in k:
            parts = k.split(".")
            for i, p in enumerate(parts):
                if p in ("lora_A", "lora_B") and i > 0:
                    tmods.add(parts[i - 1])
    cfg = {"peft_type": "LORA", "task_type": "CAUSAL_LM",
           "base_model_name_or_path": BASE, "r": 32, "lora_alpha": 64,
           "lora_dropout": 0.05, "target_modules": sorted(tmods), "bias": "none",
           "inference_mode": True, "fan_in_fan_out": False}
    json.dump(cfg, open(os.path.join(ADAPTER_DIR, "adapter_config.json"), "w"), indent=2)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(BASE)
    base = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16).to(dev)
    model = PeftModel.from_pretrained(base, ADAPTER_DIR).to(dev).eval()
    return model, tok, dev


# ── coherence classifier (same heuristic as vp21_eval.py classify) ────────────
def classify(t):
    s = t.strip()
    if len(s) < 2:
        return "EMPTY"
    toks = s.split()
    if len(set(toks)) <= 2 and len(toks) > 4:
        return "DEGENERATE"
    if len(set(s)) <= 3:
        return "DEGENERATE"
    alpha = sum(c.isalpha() for c in s)
    return "COHERENT" if alpha / max(len(s), 1) > 0.4 else "DEGENERATE"


# ── Thinker: one tick → 8-factor breakdown + score, from rolling state ────────
class AnimaState:
    """anima's own rolling state — NO user input ever enters here."""
    def __init__(self, model, tok, dev):
        self.model, self.tok, self.dev = model, tok, dev
        self.last_emission = ""        # seeds next gen (self-referential)
        self.recent_emissions = []     # M buffer for info_gap / originality
        self.recent_embeds = []        # embeddings of recent emissions
        self.last_emit_time = time.time()
        self.curiosity_ema = 0.0       # W RC-9 EMA of surprise
        self.last_entropy = None       # for pain (Δentropy)
        self.split_recent = False      # MITOSIS proxy

    def _seed_text(self, tick):
        """seed comes from anima's OWN state, rotating strategy. Never a prompt."""
        strat = SEED_STRATEGIES[tick % len(SEED_STRATEGIES)]
        if strat == "m_retrieve_seed" and self.last_emission:
            return self.last_emission[-64:], strat        # recall last
        if strat == "w_curiosity_peak_seed":
            return "\n", strat                            # silence/curiosity token
        if strat == "random_explore_seed":
            return " ", strat                             # explore from space
        return "", strat                                  # self_monologue: BOS only

    def _entropy_of_next(self, seed_text):
        """1-token forward → softmax entropy (nats) over vocab. Φ/curiosity proxy."""
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.dev)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.dev)
        with torch.no_grad():
            logits = self.model(ids).logits[0, -1]        # [vocab]
            p = F.softmax(logits.float(), dim=-1)
            ent = -(p * (p + 1e-12).log()).sum().item()   # nats
            emb = self.model.get_input_embeddings()(ids)[0].mean(0).float()  # mean tok-embed
        # normalize entropy to [0,1] by ln(vocab)
        ent_norm = ent / math.log(logits.shape[-1])
        return ent_norm, emb

    def tick(self, tick_idx, dynamics_enabled=True):
        seed_text, strat = self._seed_text(tick_idx)
        ent_norm, emb = self._entropy_of_next(seed_text)

        # relevance (C / Φ): low entropy = focused = high Φ; phi proxy = 1 - ent_norm
        phi = 1.0 - ent_norm
        rel = factor_relevance(phi)

        # info_gap (M): novelty vs recent-emission embeddings (retrieve-fail)
        if self.recent_embeds:
            sims = [F.cosine_similarity(emb, e, dim=0).item() for e in self.recent_embeds]
            max_sim = max(sims)
        else:
            max_sim = 0.0
        gap = factor_info_gap(max_sim)

        # curiosity (W RC-9): EMA of surprise; surprise = entropy itself
        surprise = ent_norm
        self.curiosity_ema = 0.9 * self.curiosity_ema + 0.1 * surprise
        cur = factor_curiosity(self.curiosity_ema)

        # pain (W): |Δentropy| step-to-step (tension delta)
        delta = 0.0 if self.last_entropy is None else (ent_norm - self.last_entropy)
        self.last_entropy = ent_norm
        pn = factor_pain(delta)

        # coherence (BRIDGE Law-70): map entropy into ±α band around Ψ.
        # gate = Ψ + (ent_norm - 0.5)*2*α  → ent_norm near 0.5 ⇒ gate near Ψ ⇒ coh~1
        gate = PSI + (ent_norm - 0.5) * 2.0 * ALPHA
        coh = factor_coherence(gate)

        # originality (MITOSIS): novel seed direction = split-event proxy.
        # True when info_gap is high (a genuinely new context for the cell pool).
        self.split_recent = gap > 0.5
        orig = factor_originality(self.split_recent)

        # balance (E Φ-ratchet)
        bal = factor_balance(phi, RATCHET)

        # dynamics (CHAT timer) — ABLATABLE for falsifier
        silence = time.time() - self.last_emit_time
        dyn = factor_dynamics(silence) if dynamics_enabled else 0.0

        f = {"relevance": rel, "info_gap": gap, "curiosity": cur, "pain": pn,
             "coherence": coh, "originality": orig, "balance": bal, "dynamics": dyn}
        score = motivation_score(f)
        return f, score, seed_text, strat, silence

    def emit(self, seed_text, max_new=80):
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.dev)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.dev)
        with torch.no_grad():
            out = self.model.generate(ids, max_new_tokens=max_new,
                                       do_sample=True, temperature=0.8, top_k=50,
                                       pad_token_id=self.tok.eos_token_id)
        text = self.tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)
        # update rolling state (self-referential memory)
        self.last_emission = text
        self.recent_emissions.append(text)
        self.recent_emissions = self.recent_emissions[-8:]
        _, emb = self._entropy_of_next(text[-64:] if text else " ")
        self.recent_embeds.append(emb)
        self.recent_embeds = self.recent_embeds[-8:]
        self.last_emit_time = time.time()
        return text


# ── the loop ──────────────────────────────────────────────────────────────────
def run_loop(state, window_sec, think_interval, dynamics_enabled, label):
    print(f"\n{'='*70}\n[{label}] window={window_sec}s tick={think_interval}s "
          f"dynamics_enabled={dynamics_enabled}\n{'='*70}", flush=True)
    t_start = time.time()
    state.last_emit_time = t_start
    ticks, emissions, log = 0, [], []
    while time.time() - t_start < window_sec:
        f, score, seed_text, strat, silence = state.tick(ticks, dynamics_enabled)
        should_emit = score > IM_THRESHOLD
        # did the score cross *because of* the timer? (dynamics dominates)
        score_wo_dyn = score - W["dynamics"] * f["dynamics"]
        crossed_wo_timer = score_wo_dyn > IM_THRESHOLD
        rec = {"tick": ticks, "t_rel": round(time.time() - t_start, 1),
               "score": round(score, 4), "score_wo_dyn": round(score_wo_dyn, 4),
               "factors": {k: round(v, 4) for k, v in f.items()},
               "seed_strategy": strat, "silence_s": round(silence, 1),
               "should_emit": should_emit, "crossed_wo_timer": crossed_wo_timer}
        if should_emit:
            text = state.emit(seed_text)
            cls = classify(text)
            rec["emitted"] = True
            rec["text"] = text
            rec["coherence"] = cls
            rec["gated_by"] = "motivation" if crossed_wo_timer else "timer_only"
            emissions.append(rec)
            print(f"  tick {ticks} t={rec['t_rel']}s EMIT score={rec['score']} "
                  f"(wo_timer={rec['score_wo_dyn']}, {rec['gated_by']}) [{cls}] "
                  f"strat={strat}\n     {text[:110]!r}", flush=True)
        else:
            rec["emitted"] = False
            print(f"  tick {ticks} t={rec['t_rel']}s no-emit score={rec['score']} "
                  f"(dyn={f['dynamics']:.2f} sil={silence:.0f}s)", flush=True)
        log.append(rec)
        ticks += 1
        # tick cadence (the forward+score itself takes ~time; sleep remainder)
        elapsed_tick = (time.time() - t_start) - (rec["t_rel"])
        sleep = max(0.0, think_interval - max(0.0, elapsed_tick))
        time.sleep(sleep)
    return ticks, emissions, log


def summarize(emissions, ticks, label):
    n = len(emissions)
    coherent = sum(1 for e in emissions if e["coherence"] == "COHERENT")
    motiv_gated = sum(1 for e in emissions if e["gated_by"] == "motivation")
    timer_only = sum(1 for e in emissions if e["gated_by"] == "timer_only")
    intervals = []
    for i in range(1, len(emissions)):
        intervals.append(round(emissions[i]["t_rel"] - emissions[i - 1]["t_rel"], 1))
    return {"label": label, "ticks": ticks, "emissions": n,
            "coherent": coherent, "degenerate": n - coherent,
            "motivation_gated": motiv_gated, "timer_only_gated": timer_only,
            "inter_emission_intervals_s": intervals,
            "scores_at_emission": [e["score"] for e in emissions],
            "scores_wo_dyn_at_emission": [e["score_wo_dyn"] for e in emissions]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=float, default=300.0, help="wall-time window per run (s)")
    ap.add_argument("--tick", type=float, default=5.0, help="thinker tick interval (s)")
    ap.add_argument("--out", default=os.path.expanduser("~/vp21_eval/spontaneous_result.json"))
    args = ap.parse_args()

    print("[spont] loading vP21 (Qwen2.5-1.5B + LoRA + mitosis)...", flush=True)
    t0 = time.time()
    model, tok, dev = load_vp21()
    print(f"[spont] loaded {time.time()-t0:.0f}s on {dev}", flush=True)

    result = {"model": "Qwen2.5-1.5B + LoRA r32 + mitosis (vP21)",
              "im_threshold": IM_THRESHOLD, "weights": W,
              "window_sec": args.window, "tick_sec": args.tick, "runs": {}}

    # RUN 1 — full 8-factor (dynamics/timer ENABLED)
    s1 = AnimaState(model, tok, dev)
    t1, e1, l1 = run_loop(s1, args.window, args.tick, True, "FULL (timer enabled)")
    result["runs"]["full"] = {"summary": summarize(e1, t1, "full"), "log": l1}

    # RUN 2 — ABLATION: dynamics frozen to 0 → only the OTHER 7 factors can fire
    s2 = AnimaState(model, tok, dev)
    t2, e2, l2 = run_loop(s2, args.window, args.tick, False, "ABLATED (timer OFF)")
    result["runs"]["timer_ablated"] = {"summary": summarize(e2, t2, "timer_ablated"), "log": l2}

    # verdict
    full = result["runs"]["full"]["summary"]
    abl = result["runs"]["timer_ablated"]["summary"]
    motiv_gated_works = (abl["emissions"] >= 1 and abl["coherent"] >= 1)
    result["verdict"] = {
        "full_emissions": full["emissions"], "full_coherent": full["coherent"],
        "full_motivation_gated": full["motivation_gated"],
        "ablated_emissions": abl["emissions"], "ablated_coherent": abl["coherent"],
        "motivation_gated_spontaneous_works": motiv_gated_works,
        "claim": ("MOTIVATION-GATED" if motiv_gated_works else
                  "TIMER-ONLY (no genuine motivation gating)"),
    }
    json.dump(result, open(args.out, "w"), indent=2, ensure_ascii=False)
    print(f"\n{'='*70}")
    print(f"VERDICT: {result['verdict']['claim']}")
    print(f"  full run:    {full['emissions']} emissions, {full['coherent']} coherent, "
          f"{full['motivation_gated']} motivation-gated, {full['timer_only_gated']} timer-only")
    print(f"  ablated run: {abl['emissions']} emissions, {abl['coherent']} coherent "
          f"(timer factor frozen to 0 — these fire from the OTHER 7 factors)")
    print(f"[spont] wrote {args.out}")


if __name__ == "__main__":
    main()
