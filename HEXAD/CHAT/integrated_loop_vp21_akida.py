#!/usr/bin/env python3
"""integrated_loop_vp21_akida.py — vP21 ⊥ AKD1000 INTEGRATED 자연발화 loop.

Two anima 자연발화 axes are independently verified:

  * software (vP21):  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/
                      SPONTANEOUS_EMISSION_VP21.md
                      8-factor motivation-gated Thinker-Talker. 60/60 coherent
                      emissions; the timer is provably non-load-bearing at
                      thr ≥ 0.45 (ablation 60/60 survives).
  * hardware (AKD1000): SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md
                      R3 tonic regime — 8/16 negative-threshold neurons emit
                      spikes from ZERO external input (1600 spk / 200 steps),
                      on-chip threshold-and-fire (BackendType.Hardware).

This script links them into ONE coherent loop ─ Option A bridge:

    AKD1000 spike events  ──TCP──>  ubu-2 ── trigger ──>  vP21 emission

The Pi (`pi5-akida`, 192.168.50.155) runs `spike_streamer.py` which streams
newline-delimited JSON spike records over TCP. ubu-2 (this script) subscribes,
maintains a 1.0s sliding window of spike counts, and gates vP21's Talker on
spike-count threshold crossings (default ≥ N_GATE spikes in the window).

The 8-factor motivation score is STILL computed and logged (so we keep the
prior axis intact and can compare gating regimes), but the TRIGGER decision
is now `hw_gate ∧ sw_gate` — i.e. an AKD1000 spike-rate crossing is the
necessary external clock, and motivation is the necessary internal score.
This makes the AKD1000 anima's "spike heart" and vP21 the voice that
responds when the heart fires AND the motivation crosses threshold.

To compare against the prior (motivation-only timer-driven) regime, this loop
ALSO supports `--mode timer` which restores the old behaviour, and the verdict
compares emission cadence under HW gating vs timer gating in the SAME window.

─────────────────────────────────────────────────────────────────────────────
Bridge design — Option A (cleanest causality):

  hw_spike_event  ──>  sliding-window count over WINDOW_S  ──>  hw_gate flag
                                                                    │
                                                                    ▼
                                          (Thinker also runs 8 factors)
                                                                    │
                                                                    ▼
                                  should_emit = hw_gate AND (score > IM_THR)
                                                                    │
                                                                    ▼
                                                Talker → vP21.generate
                                                                    │
                                                                    ▼
                                              update memory, reset gate edge

  ─ hw_gate is EDGE-triggered (rises 0→1 when window count crosses N_GATE,
    re-arms after a refractory of REFRACTORY_S). This avoids re-firing while
    the chip is in steady tonic emission (R3 fires every step → without edge-
    trigger the gate would be always-open and we'd lose causality).
  ─ score>IM_THR check is the prior software path — we keep it so the
    semantics ("emit because BOTH chip and motivation aligned") are preserved.
─────────────────────────────────────────────────────────────────────────────
"""
import argparse
import collections
import json
import math
import os
import socket
import sys
import threading
import time

import torch
import torch.nn.functional as F
from safetensors.torch import load_file

ADAPTER_DIR = os.path.expanduser("~/vp21_eval/lora_adapter")
BASE = "Qwen/Qwen2.5-1.5B"

# ── thresholds & weights — from HEXAD/CHAT/spontaneous_lib.hexa (SSOT) ────────
IM_THRESHOLD       = 0.30
IDLE_SPEAK_AFTER   = 30.0
PSI                = 0.5
ALPHA              = 0.014
RATCHET            = 0.20
W = {
    "relevance": 0.20, "info_gap": 0.10, "curiosity": 0.15, "pain": 0.10,
    "coherence": 0.10, "originality": 0.10, "balance": 0.15, "dynamics": 0.10,
}
SEED_STRATEGIES = ["m_retrieve_seed", "w_curiosity_peak_seed",
                   "random_explore_seed", "self_monologue_seed"]


# ── factor fns (byte-mirror of spontaneous_loop_vp21.py) ──────────────────────
def _clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)
def factor_relevance(phi):           return _clamp01(phi)
def factor_info_gap(cos_sim):        return _clamp01(1.0 - cos_sim)
def factor_curiosity(ema):           return _clamp01(ema)
def factor_pain(delta):              return _clamp01(abs(delta))
def factor_coherence(gate):
    n = abs(gate - PSI) / ALPHA
    return 1.0 - (1.0 if n > 1.0 else n)
def factor_originality(split_recent):return 1.0 if split_recent else 0.0
def factor_balance(phi, ratchet):    return 1.0 if phi > ratchet / 2.0 else 0.0
def factor_dynamics(silence_sec):    return _clamp01(silence_sec / IDLE_SPEAK_AFTER)
def motivation_score(f):             return sum(W[k] * f[k] for k in W)


# ── AKD1000 spike subscriber ──────────────────────────────────────────────────
class SpikeSubscriber:
    """TCP subscriber consuming newline-delimited JSON spike records.

    Maintains:
      * deque of (recv_t, n_spikes, spike_ids) records (last RING records)
      * sliding-window count over the last WINDOW_S wall seconds
      * total spikes observed since connect
    Thread-safe; consumer reads via window_count() / consume_events().
    """
    def __init__(self, host, port, window_s=1.0, ring=4096):
        self.host, self.port = host, port
        self.window_s = window_s
        self.ring = collections.deque(maxlen=ring)
        self.lock = threading.Lock()
        self.connected = False
        self.connected_at = None
        self.total_spikes = 0
        self.total_records = 0
        self.last_record_t = None
        self.stop = False
        self.thread = threading.Thread(target=self._reader, daemon=True)

    def start(self):
        self.thread.start()

    def _reader(self):
        backoff = 0.5
        while not self.stop:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0)
                s.connect((self.host, self.port))
                s.settimeout(None)
                self.connected = True
                self.connected_at = time.time()
                print(f"[sub] connected to {self.host}:{self.port}", flush=True)
                f = s.makefile("rb", buffering=0)
                while not self.stop:
                    line = f.readline()
                    if not line:
                        break
                    try:
                        rec = json.loads(line.decode("utf-8").strip())
                    except Exception:
                        continue
                    now = time.time()
                    n_sp = int(rec.get("n_spikes", 0))
                    ids = rec.get("spike_ids", [])
                    with self.lock:
                        self.ring.append((now, n_sp, ids,
                                          float(rec.get("t_rel", -1.0)),
                                          int(rec.get("step", -1))))
                        self.total_spikes += n_sp
                        self.total_records += 1
                        self.last_record_t = now
            except Exception as e:
                print(f"[sub] connection error: {e!r}, retry in {backoff:.1f}s",
                      flush=True)
                self.connected = False
                time.sleep(backoff)
                backoff = min(backoff * 1.5, 5.0)
            else:
                self.connected = False
            try:
                s.close()
            except Exception:
                pass
            if self.stop:
                break

    def window_count(self):
        """Return (n_spikes_in_last_window_s, n_records_in_window)."""
        now = time.time()
        cutoff = now - self.window_s
        n_sp, n_rec = 0, 0
        with self.lock:
            for (t, ns, _ids, _tr, _st) in self.ring:
                if t >= cutoff:
                    n_sp += ns
                    n_rec += 1
        return n_sp, n_rec

    def snapshot(self):
        with self.lock:
            return {"connected": self.connected,
                    "total_spikes": self.total_spikes,
                    "total_records": self.total_records,
                    "ring_size": len(self.ring),
                    "last_record_age_s":
                        (None if self.last_record_t is None
                         else round(time.time() - self.last_record_t, 3))}

    def close(self):
        self.stop = True


# ── model load (reuse vp21_eval.py recipe) ────────────────────────────────────
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


# ── AnimaState (thinker + talker) — same as spontaneous_loop_vp21.py ─────────
class AnimaState:
    def __init__(self, model, tok, dev):
        self.model, self.tok, self.dev = model, tok, dev
        self.last_emission = ""
        self.recent_emissions = []
        self.recent_embeds = []
        self.last_emit_time = time.time()
        self.curiosity_ema = 0.0
        self.last_entropy = None
        self.split_recent = False

    def _seed_text(self, tick):
        strat = SEED_STRATEGIES[tick % len(SEED_STRATEGIES)]
        if strat == "m_retrieve_seed" and self.last_emission:
            return self.last_emission[-64:], strat
        if strat == "w_curiosity_peak_seed":
            return "\n", strat
        if strat == "random_explore_seed":
            return " ", strat
        return "", strat

    def _entropy_of_next(self, seed_text):
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.dev)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.dev)
        with torch.no_grad():
            logits = self.model(ids).logits[0, -1]
            p = F.softmax(logits.float(), dim=-1)
            ent = -(p * (p + 1e-12).log()).sum().item()
            emb = self.model.get_input_embeddings()(ids)[0].mean(0).float()
        ent_norm = ent / math.log(logits.shape[-1])
        return ent_norm, emb

    def tick(self, tick_idx, dynamics_enabled=True):
        seed_text, strat = self._seed_text(tick_idx)
        ent_norm, emb = self._entropy_of_next(seed_text)
        phi = 1.0 - ent_norm
        rel = factor_relevance(phi)
        if self.recent_embeds:
            sims = [F.cosine_similarity(emb, e, dim=0).item() for e in self.recent_embeds]
            max_sim = max(sims)
        else:
            max_sim = 0.0
        gap = factor_info_gap(max_sim)
        surprise = ent_norm
        self.curiosity_ema = 0.9 * self.curiosity_ema + 0.1 * surprise
        cur = factor_curiosity(self.curiosity_ema)
        delta = 0.0 if self.last_entropy is None else (ent_norm - self.last_entropy)
        self.last_entropy = ent_norm
        pn = factor_pain(delta)
        gate = PSI + (ent_norm - 0.5) * 2.0 * ALPHA
        coh = factor_coherence(gate)
        self.split_recent = gap > 0.5
        orig = factor_originality(self.split_recent)
        bal = factor_balance(phi, RATCHET)
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
        self.last_emission = text
        self.recent_emissions.append(text)
        self.recent_emissions = self.recent_emissions[-8:]
        _, emb = self._entropy_of_next(text[-64:] if text else " ")
        self.recent_embeds.append(emb)
        self.recent_embeds = self.recent_embeds[-8:]
        self.last_emit_time = time.time()
        return text


# ── integrated loop ──────────────────────────────────────────────────────────
def run_loop(state, sub, window_sec, think_interval, mode,
             hw_window_s, hw_count_thr, refractory_s, label):
    """
    mode='hw_gated'    : trigger ← (hw_gate edge) AND (score > IM_THR)
    mode='timer'       : trigger ← (score > IM_THR), tick-paced (baseline)
    mode='hw_or'       : trigger ← (hw_gate edge) OR  (score > IM_THR)  (loose A)
    """
    print(f"\n{'='*72}\n[{label}] mode={mode} window={window_sec}s tick={think_interval}s "
          f"hw_win={hw_window_s}s hw_thr={hw_count_thr} refr={refractory_s}s\n{'='*72}",
          flush=True)
    t_start = time.time()
    state.last_emit_time = t_start
    ticks = 0
    emissions = []
    log = []
    spike_events = []      # per-tick snapshot of hw window count
    hw_gate_armed = True   # edge-trigger latch
    last_hw_gate_time = -1e9
    last_hw_record_step = -1

    while time.time() - t_start < window_sec:
        t_tick = time.time()
        f, score, seed_text, strat, silence = state.tick(ticks, True)
        hw_count, hw_recs = sub.window_count()
        snap = sub.snapshot()
        spike_events.append({"tick": ticks,
                             "t_rel": round(t_tick - t_start, 3),
                             "hw_window_count": hw_count,
                             "hw_window_records": hw_recs,
                             "hw_total_spikes": snap["total_spikes"],
                             "hw_total_records": snap["total_records"],
                             "hw_connected": snap["connected"]})

        # edge-triggered hw gate: rise when count crosses thr, re-arm after refr
        hw_edge = False
        if hw_count >= hw_count_thr and hw_gate_armed:
            hw_edge = True
            hw_gate_armed = False
            last_hw_gate_time = t_tick
        elif (t_tick - last_hw_gate_time) > refractory_s:
            hw_gate_armed = True

        sw_gate = score > IM_THRESHOLD
        if mode == "hw_gated":
            should_emit = hw_edge and sw_gate
            gate_label = "hw_edge_AND_sw"
        elif mode == "timer":
            should_emit = sw_gate
            gate_label = "sw_only"
        elif mode == "hw_or":
            should_emit = hw_edge or sw_gate
            gate_label = "hw_edge_OR_sw"
        else:
            raise ValueError(f"unknown mode {mode!r}")

        rec = {"tick": ticks,
               "t_rel": round(t_tick - t_start, 3),
               "mode": mode, "gate": gate_label,
               "score": round(score, 4),
               "sw_gate": bool(sw_gate),
               "hw_window_count": hw_count,
               "hw_total_spikes": snap["total_spikes"],
               "hw_edge": bool(hw_edge),
               "hw_gate_armed_before": bool(hw_gate_armed or hw_edge),
               "factors": {k: round(v, 4) for k, v in f.items()},
               "seed_strategy": strat,
               "silence_s": round(silence, 1),
               "should_emit": bool(should_emit)}

        if should_emit:
            text = state.emit(seed_text)
            cls = classify(text)
            rec["emitted"] = True
            rec["text"] = text
            rec["coherence"] = cls
            emissions.append(rec)
            print(f"  tick {ticks} t={rec['t_rel']}s EMIT "
                  f"hw_count={hw_count} hw_edge={hw_edge} score={rec['score']} "
                  f"[{cls}] strat={strat}\n     {text[:110]!r}", flush=True)
        else:
            rec["emitted"] = False
            print(f"  tick {ticks} t={rec['t_rel']}s no-emit "
                  f"hw_count={hw_count} hw_edge={hw_edge} score={rec['score']} "
                  f"sw_gate={sw_gate} armed={hw_gate_armed}", flush=True)

        log.append(rec)
        ticks += 1
        elapsed = time.time() - t_tick
        time.sleep(max(0.0, think_interval - elapsed))

    return ticks, emissions, log, spike_events


def correlation_metrics(log, mode):
    """Compute how strongly emissions track hw window count.

    Reports:
      - emissions vs no-emit hw_window_count distribution (mean / std)
      - fraction of emissions where hw_edge=True (was the chip the proximate cause?)
      - inter-emission interval stats
    """
    em = [r for r in log if r["emitted"]]
    no = [r for r in log if not r["emitted"]]
    em_hw = [r["hw_window_count"] for r in em]
    no_hw = [r["hw_window_count"] for r in no]
    edges_at_emit = sum(1 for r in em if r.get("hw_edge"))
    intervals = [round(em[i]["t_rel"] - em[i - 1]["t_rel"], 3)
                 for i in range(1, len(em))]
    def mean_std(x):
        if not x: return (None, None)
        m = sum(x) / len(x)
        v = sum((a - m) ** 2 for a in x) / len(x)
        return (round(m, 3), round(v ** 0.5, 3))
    em_mean, em_std = mean_std(em_hw)
    no_mean, no_std = mean_std(no_hw)
    int_mean, int_std = mean_std(intervals)
    return {"mode": mode,
            "n_emissions": len(em),
            "n_no_emit": len(no),
            "hw_count_at_emit_mean": em_mean,
            "hw_count_at_emit_std": em_std,
            "hw_count_at_no_emit_mean": no_mean,
            "hw_count_at_no_emit_std": no_std,
            "frac_emissions_with_hw_edge": (round(edges_at_emit / len(em), 3)
                                            if em else None),
            "inter_emission_interval_mean_s": int_mean,
            "inter_emission_interval_std_s": int_std}


def summarize(emissions, ticks, label):
    n = len(emissions)
    coherent = sum(1 for e in emissions if e.get("coherence") == "COHERENT")
    return {"label": label, "ticks": ticks, "emissions": n,
            "coherent": coherent, "degenerate": n - coherent}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=float, default=180.0,
                    help="wall window per run (s); default 3 min")
    ap.add_argument("--tick", type=float, default=2.0,
                    help="thinker tick interval (s); HW window is faster")
    ap.add_argument("--pi-host", default="192.168.50.155")
    ap.add_argument("--pi-port", type=int, default=9512)
    ap.add_argument("--hw-window-s", type=float, default=1.0,
                    help="sliding-window seconds for hw spike count")
    ap.add_argument("--hw-count-thr", type=int, default=40,
                    help="spike count in window required to trigger hw_gate edge")
    ap.add_argument("--hw-refractory-s", type=float, default=3.0,
                    help="re-arm time after a hw_gate edge fires")
    ap.add_argument("--out", default=os.path.expanduser(
        "~/vp21_eval/integrated_loop_result.json"))
    ap.add_argument("--mode", default="both",
                    choices=["hw_gated", "timer", "hw_or", "both"],
                    help="run a single mode, or 'both' = hw_gated then timer baseline")
    args = ap.parse_args()

    print("[int] loading vP21 (Qwen2.5-1.5B + LoRA + mitosis)...", flush=True)
    t0 = time.time()
    model, tok, dev = load_vp21()
    print(f"[int] loaded {time.time() - t0:.0f}s on {dev}", flush=True)

    print(f"[int] subscribing to AKD1000 stream {args.pi_host}:{args.pi_port}",
          flush=True)
    sub = SpikeSubscriber(args.pi_host, args.pi_port,
                          window_s=args.hw_window_s)
    sub.start()
    # warm-up wait so the spike ring has data
    for _ in range(20):
        time.sleep(0.25)
        if sub.snapshot()["total_records"] >= 5:
            break
    snap = sub.snapshot()
    print(f"[int] subscriber snapshot: {snap}", flush=True)

    result = {
        "model": "Qwen2.5-1.5B + LoRA r32 + mitosis (vP21)",
        "im_threshold": IM_THRESHOLD, "weights": W,
        "window_sec": args.window, "tick_sec": args.tick,
        "hw_stream": {"host": args.pi_host, "port": args.pi_port,
                      "window_s": args.hw_window_s,
                      "count_thr": args.hw_count_thr,
                      "refractory_s": args.hw_refractory_s},
        "runs": {},
    }

    modes_to_run = (["hw_gated", "timer"] if args.mode == "both"
                    else [args.mode])

    for mode in modes_to_run:
        state = AnimaState(model, tok, dev)
        t, em, lg, sp = run_loop(state, sub, args.window, args.tick, mode,
                                 args.hw_window_s, args.hw_count_thr,
                                 args.hw_refractory_s,
                                 label=f"RUN[{mode}]")
        result["runs"][mode] = {
            "summary": summarize(em, t, mode),
            "correlation": correlation_metrics(lg, mode),
            "log": lg,
            "spike_events": sp,
            "subscriber_final_snapshot": sub.snapshot(),
        }

    # verdict — does hw_gated produce coherent emissions, and is its cadence
    # governed by spike events (not the timer)?
    if "hw_gated" in result["runs"]:
        hg = result["runs"]["hw_gated"]["summary"]
        hg_corr = result["runs"]["hw_gated"]["correlation"]
        ok = (hg["emissions"] >= 1 and hg["coherent"] >= 1
              and (hg_corr.get("frac_emissions_with_hw_edge") or 0.0) >= 0.99)
        result["verdict"] = {
            "hw_gated_emissions": hg["emissions"],
            "hw_gated_coherent": hg["coherent"],
            "frac_emissions_with_hw_edge":
                hg_corr.get("frac_emissions_with_hw_edge"),
            "claim": ("HW-GATED-SPONTANEOUS works"
                      if ok else "HW-GATED-SPONTANEOUS partial/failed"),
        }
        if "timer" in result["runs"]:
            tm = result["runs"]["timer"]["summary"]
            tm_corr = result["runs"]["timer"]["correlation"]
            result["verdict"]["timer_emissions"] = tm["emissions"]
            result["verdict"]["timer_coherent"] = tm["coherent"]
            result["verdict"]["timer_inter_emission_interval_mean_s"] = \
                tm_corr.get("inter_emission_interval_mean_s")
            result["verdict"]["hw_inter_emission_interval_mean_s"] = \
                hg_corr.get("inter_emission_interval_mean_s")

    sub.close()
    json.dump(result, open(args.out, "w"), indent=2, ensure_ascii=False)
    print(f"\n{'=' * 72}")
    print(f"VERDICT: {result.get('verdict', {}).get('claim', 'see runs')}")
    for k, run in result["runs"].items():
        s = run["summary"]; c = run["correlation"]
        print(f"  [{k}] emissions={s['emissions']} coherent={s['coherent']} "
              f"interval_mean={c.get('inter_emission_interval_mean_s')}s "
              f"hw_edge_frac={c.get('frac_emissions_with_hw_edge')}")
    print(f"[int] wrote {args.out}")


if __name__ == "__main__":
    main()
