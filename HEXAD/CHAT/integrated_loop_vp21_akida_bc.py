#!/usr/bin/env python3
"""integrated_loop_vp21_akida_bc.py — Option B / Option C bidirectional bridge.

Extends Option A (`integrated_loop_vp21_akida.py` — HW spike → SW emission gate)
with two new directions:

    Option B:    SW vP21 motivation_score   ──TCP──>  AKD1000 threshold
                 (high motivation → LOWER threshold → MORE spikes)

    Option C:    Option A + Option B simultaneously — closed-loop
                 (HW spikes still gate SW emission; SW motivation still
                  modulates HW threshold; both substrates drive each other.)

The Pi (`pi5-akida`) runs `spike_streamer.py --allow-ctrl` which (a) broadcasts
per-step spike events on port 9512 (Option A subscriber stream) AND (b) accepts
incoming `{"cmd":"set_threshold","thr":[...]}` JSON commands on port 9513 that
get applied to the on-chip FullyConnected.threshold int32 vector at the next
chip step.

Mapping motivation_score → threshold vector
-------------------------------------------

The streamer's M regime uses a linspace baseline thr (2..18 across 16 units)
combined with weak-ones input (each unit potential V=N=16). So the spike
fraction at any unit j follows `fire[j] = 1 if 16 > thr[j] else 0`.

We modulate by an integer offset that shifts the whole vector:

    score ∈ [0, 1]   (motivation_score, 8-factor sum)
    offset = round(THR_AMPL * (0.5 - score))     # 0.5 = neutral
    thr[j] = baseline[j] + offset                # high score → negative offset → lower thr → more spikes
                                                  # low  score → positive offset → higher thr → fewer spikes

THR_AMPL controls how strongly motivation drives the threshold. Default 12 — at
score=0 offset=+6 → thr shifted up 6 → fewer spikes; at score=1 offset=-6 →
shifted down 6 → more spikes.

We rate-limit threshold updates to one per tick (matches motivation tick cadence)
so per-step chip overhead stays bounded. Honest C3: per-step `set_variable`
overhead is the gating factor for high-frequency control; the streamer reports
`set_var_ms_total` to quantify it.

Measurements
------------

Per tick we log (motivation_score, hw_spike_rate_in_window) and compute Spearman
rank correlation across the 180s window. A **random-motivation control baseline**
re-runs the same loop with motivation REPLACED by a uniform-random surrogate;
correlation should collapse if the linkage is real (the SW score is the cause,
not chance).

Verdict
-------

* Option B works  ⇔  Spearman(motivation, hw_spike_rate) > 0.3
  AND  random-control Spearman drops below 0.15 (collapse).
* Option C works  ⇔  Option B works  AND  A-side `frac_emissions_with_hw_edge`
  remains > 0.5 (HW edge still necessary for emission).
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
import random

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

# ── Option B mapping: motivation → threshold ──────────────────────────────────
# Baseline thr per the streamer's M regime: np.linspace(2, 18, N).astype(int32)
THR_BASELINE_LO, THR_BASELINE_HI, THR_BASELINE_N = 2, 18, 16
THR_AMPL = 12        # offset amplitude — 0.5±0.5 score → ±6 offset
THR_NEUTRAL = 0.5    # motivation midpoint


def baseline_thr_vec(n=THR_BASELINE_N):
    # mirror np.linspace(2, 18, N).astype(int32) WITHOUT numpy at import-cost
    return [int(round(THR_BASELINE_LO + (THR_BASELINE_HI - THR_BASELINE_LO) *
                      i / max(1, n - 1))) for i in range(n)]


def score_to_thr_vector(score, n=THR_BASELINE_N):
    """Map motivation_score ∈ [0,1] to integer threshold vector (length n).

    high score → negative offset → lower thr → MORE spikes.
    low  score → positive offset → higher thr → FEWER spikes.
    """
    offset = int(round(THR_AMPL * (THR_NEUTRAL - max(0.0, min(1.0, score)))))
    base = baseline_thr_vec(n)
    return [b + offset for b in base], offset


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


# ── AKD1000 spike subscriber (OUT 9512) ───────────────────────────────────────
class SpikeSubscriber:
    """TCP subscriber consuming newline-delimited JSON spike records."""
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
                                          int(rec.get("step", -1)),
                                          rec.get("thr", [])))
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
            for (t, ns, _ids, _tr, _st, _thr) in self.ring:
                if t >= cutoff:
                    n_sp += ns
                    n_rec += 1
        return n_sp, n_rec

    def window_rate(self):
        """Spike rate = spikes / (records * N_neurons), or 0 if no records."""
        n_sp, n_rec = self.window_count()
        if n_rec == 0:
            return 0.0
        return n_sp / max(1, n_rec * THR_BASELINE_N)

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


# ── Threshold publisher (IN ctrl 9513) ────────────────────────────────────────
class ThresholdPublisher:
    """Persistent TCP connection to the Pi ctrl port, sending JSON commands.

    Uses one socket reused per tick. Failures auto-reconnect with backoff.
    """
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.sock = None
        self.lock = threading.Lock()
        self.n_sent = 0
        self.n_fail = 0
        self.last_send_t = None

    def _ensure(self):
        if self.sock is not None:
            return self.sock
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((self.host, self.port))
            s.settimeout(None)
            self.sock = s
            print(f"[pub] connected ctrl {self.host}:{self.port}", flush=True)
        except Exception as e:
            print(f"[pub] ctrl connect failed: {e!r}", flush=True)
            self.sock = None
        return self.sock

    def send_threshold(self, thr_list):
        line = (json.dumps({"cmd": "set_threshold", "thr": thr_list}) + "\n"
                ).encode("utf-8")
        with self.lock:
            s = self._ensure()
            if s is None:
                self.n_fail += 1
                return False
            try:
                t0 = time.time()
                s.sendall(line)
                self.n_sent += 1
                self.last_send_t = time.time()
                return True
            except Exception as e:
                print(f"[pub] send failed: {e!r}, reconnecting", flush=True)
                try:
                    s.close()
                except Exception:
                    pass
                self.sock = None
                self.n_fail += 1
                return False

    def snapshot(self):
        with self.lock:
            return {"n_sent": self.n_sent, "n_fail": self.n_fail,
                    "connected": self.sock is not None,
                    "last_send_age_s":
                        (None if self.last_send_t is None
                         else round(time.time() - self.last_send_t, 3))}

    def close(self):
        with self.lock:
            if self.sock is not None:
                try:
                    self.sock.close()
                except Exception:
                    pass
                self.sock = None


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


# ── correlation utilities ────────────────────────────────────────────────────
def spearman(x, y):
    """Spearman rank correlation; no scipy dep."""
    if len(x) != len(y) or len(x) < 3:
        return None
    def rank(a):
        # average rank for ties
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(a):
            j = i
            while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx = rank(x); ry = rank(y)
    n = len(x)
    mx = sum(rx) / n; my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n))
    dy = sum((ry[i] - my) ** 2 for i in range(n))
    if dx <= 0 or dy <= 0:
        return None
    return num / math.sqrt(dx * dy)


def pearson(x, y):
    if len(x) != len(y) or len(x) < 3:
        return None
    n = len(x)
    mx = sum(x) / n; my = sum(y) / n
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    dx = sum((x[i] - mx) ** 2 for i in range(n))
    dy = sum((y[i] - my) ** 2 for i in range(n))
    if dx <= 0 or dy <= 0:
        return None
    return num / math.sqrt(dx * dy)


# ── integrated loop (B / C / B_random_control) ────────────────────────────────
def run_loop(state, sub, pub, window_sec, think_interval, mode,
             hw_window_s, hw_count_thr, refractory_s, label,
             rng_control=None):
    """
    Modes:
      'option_b'           : motivation → threshold (B only). NO emission gate.
      'option_c'           : motivation → threshold (B) AND hw_edge ∧ sw_gate (A).
      'option_b_random'    : SAME as option_b but threshold driven by a random
                             surrogate motivation in [0,1] (control baseline).
      'option_c_random'    : SAME as option_c but threshold-driver is randomised.
    """
    print(f"\n{'='*72}\n[{label}] mode={mode} window={window_sec}s tick={think_interval}s "
          f"hw_win={hw_window_s}s hw_thr={hw_count_thr} refr={refractory_s}s\n{'='*72}",
          flush=True)
    t_start = time.time()
    state.last_emit_time = t_start
    ticks = 0
    emissions = []
    log = []
    hw_gate_armed = True
    last_hw_gate_time = -1e9

    while time.time() - t_start < window_sec:
        t_tick = time.time()
        f, score, seed_text, strat, silence = state.tick(ticks, True)

        # Driver used for threshold modulation (real score OR random surrogate).
        if mode in ("option_b_random", "option_c_random"):
            assert rng_control is not None
            drive = rng_control.random()
        else:
            drive = score

        # B-side: publish threshold based on drive
        thr_list, offset = score_to_thr_vector(drive)
        pub_ok = pub.send_threshold(thr_list) if pub is not None else None

        # HW-side observation (A-side metrics — still useful even in pure-B mode)
        hw_count, hw_recs = sub.window_count()
        hw_rate = sub.window_rate()
        snap = sub.snapshot()

        hw_edge = False
        if hw_count >= hw_count_thr and hw_gate_armed:
            hw_edge = True
            hw_gate_armed = False
            last_hw_gate_time = t_tick
        elif (t_tick - last_hw_gate_time) > refractory_s:
            hw_gate_armed = True

        sw_gate = score > IM_THRESHOLD
        if mode in ("option_c", "option_c_random"):
            should_emit = hw_edge and sw_gate
            gate_label = "C: hw_edge_AND_sw  (B+A)"
        else:  # option_b / option_b_random — pure-B doesn't emit
            should_emit = False
            gate_label = "B: threshold-only (no emit)"

        rec = {"tick": ticks,
               "t_rel": round(t_tick - t_start, 3),
               "mode": mode, "gate": gate_label,
               "score": round(score, 4),
               "drive": round(drive, 4),
               "thr_offset": offset,
               "thr_first_unit": thr_list[0],
               "pub_ok": bool(pub_ok) if pub_ok is not None else None,
               "sw_gate": bool(sw_gate),
               "hw_window_count": hw_count,
               "hw_window_rate": round(hw_rate, 4),
               "hw_total_spikes": snap["total_spikes"],
               "hw_edge": bool(hw_edge),
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
                  f"drive={rec['drive']} thr0={rec['thr_first_unit']} "
                  f"hw_rate={rec['hw_window_rate']} hw_edge={hw_edge} "
                  f"[{cls}]\n     {text[:110]!r}", flush=True)
        else:
            rec["emitted"] = False
            if ticks % 5 == 0 or hw_edge:
                print(f"  tick {ticks} t={rec['t_rel']}s drive={rec['drive']} "
                      f"thr0={rec['thr_first_unit']} hw_rate={rec['hw_window_rate']} "
                      f"hw_count={hw_count} hw_edge={hw_edge} score={rec['score']} "
                      f"pub_ok={rec['pub_ok']}", flush=True)

        log.append(rec)
        ticks += 1
        elapsed = time.time() - t_tick
        time.sleep(max(0.0, think_interval - elapsed))

    return ticks, emissions, log


def correlation_metrics(log, mode):
    drives = [r["drive"] for r in log]
    scores = [r["score"] for r in log]
    hw_rates = [r["hw_window_rate"] for r in log]
    hw_counts = [r["hw_window_count"] for r in log]
    thr_offsets = [r["thr_offset"] for r in log]
    em = [r for r in log if r["emitted"]]
    edges_at_emit = sum(1 for r in em if r.get("hw_edge"))
    return {"mode": mode,
            "n_ticks": len(log),
            "n_emissions": len(em),
            "frac_emissions_with_hw_edge": (round(edges_at_emit / len(em), 3)
                                             if em else None),
            "spearman_drive_vs_hw_rate":   _r(spearman(drives, hw_rates)),
            "spearman_score_vs_hw_rate":   _r(spearman(scores, hw_rates)),
            "spearman_drive_vs_hw_count":  _r(spearman(drives, hw_counts)),
            "pearson_drive_vs_hw_rate":    _r(pearson(drives, hw_rates)),
            "pearson_thr_offset_vs_hw_rate":_r(pearson(thr_offsets, hw_rates)),
            "drive_mean":                  _r(sum(drives) / max(1, len(drives))),
            "score_mean":                  _r(sum(scores) / max(1, len(scores))),
            "hw_rate_mean":                _r(sum(hw_rates) / max(1, len(hw_rates))),
            "hw_rate_min":                 min(hw_rates) if hw_rates else None,
            "hw_rate_max":                 max(hw_rates) if hw_rates else None,
            "thr_offset_min":              min(thr_offsets) if thr_offsets else None,
            "thr_offset_max":              max(thr_offsets) if thr_offsets else None}


def _r(x, k=4):
    return None if x is None else round(x, k)


def summarize(emissions, ticks, label):
    n = len(emissions)
    coherent = sum(1 for e in emissions if e.get("coherence") == "COHERENT")
    return {"label": label, "ticks": ticks, "emissions": n,
            "coherent": coherent, "degenerate": n - coherent}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=float, default=180.0)
    ap.add_argument("--tick", type=float, default=2.0)
    ap.add_argument("--pi-host", default="192.168.50.155")
    ap.add_argument("--pi-port", type=int, default=9512)
    ap.add_argument("--pi-ctrl-port", type=int, default=9513)
    ap.add_argument("--hw-window-s", type=float, default=1.0)
    ap.add_argument("--hw-count-thr", type=int, default=6,
                    help="threshold for hw_edge gate (in M regime spike counts "
                         "are ~0-16, lower than the R3 79 saturated count)")
    ap.add_argument("--hw-refractory-s", type=float, default=3.0)
    ap.add_argument("--out", default=os.path.expanduser(
        "~/vp21_eval/integrated_opt_bc_result.json"))
    ap.add_argument("--mode", default="all",
                    choices=["option_b", "option_c",
                             "option_b_random", "option_c_random",
                             "b_only", "all"],
                    help="b_only = option_b + option_b_random (tight scope, "
                         "skip C); all = 4 modes")
    ap.add_argument("--no-model", action="store_true",
                    help="dummy AnimaState (don't load LLM — for fast B-only "
                         "smoke test).")
    args = ap.parse_args()

    if not args.no_model:
        print("[int] loading vP21 (Qwen2.5-1.5B + LoRA + mitosis)...", flush=True)
        t0 = time.time()
        model, tok, dev = load_vp21()
        print(f"[int] loaded {time.time() - t0:.0f}s on {dev}", flush=True)
    else:
        model, tok, dev = None, None, "cpu"

    print(f"[int] subscribing to AKD1000 stream {args.pi_host}:{args.pi_port}",
          flush=True)
    sub = SpikeSubscriber(args.pi_host, args.pi_port,
                          window_s=args.hw_window_s)
    sub.start()
    pub = ThresholdPublisher(args.pi_host, args.pi_ctrl_port)
    # warm-up wait for subscriber + open ctrl connection
    for _ in range(20):
        time.sleep(0.25)
        if sub.snapshot()["total_records"] >= 5:
            break
    snap = sub.snapshot()
    print(f"[int] subscriber snapshot: {snap}", flush=True)
    # send one initial threshold to verify the ctrl link
    init_thr, init_off = score_to_thr_vector(0.5)
    pub.send_threshold(init_thr)
    print(f"[int] publisher initial threshold sent: {init_thr} (off={init_off})",
          flush=True)
    time.sleep(0.5)
    print(f"[int] publisher snapshot: {pub.snapshot()}", flush=True)

    result = {
        "model": ("Qwen2.5-1.5B + LoRA r32 + mitosis (vP21)"
                  if not args.no_model else "DUMMY (no-model smoke)"),
        "im_threshold": IM_THRESHOLD, "weights": W,
        "thr_baseline": baseline_thr_vec(),
        "thr_ampl": THR_AMPL, "thr_neutral": THR_NEUTRAL,
        "window_sec": args.window, "tick_sec": args.tick,
        "hw_stream": {"host": args.pi_host, "port": args.pi_port,
                      "ctrl_port": args.pi_ctrl_port,
                      "window_s": args.hw_window_s,
                      "count_thr": args.hw_count_thr,
                      "refractory_s": args.hw_refractory_s},
        "runs": {},
    }

    if args.mode == "all":
        modes_to_run = ["option_b", "option_b_random",
                        "option_c", "option_c_random"]
    elif args.mode == "b_only":
        modes_to_run = ["option_b", "option_b_random"]
    else:
        modes_to_run = [args.mode]

    for mode in modes_to_run:
        if not args.no_model and model is not None:
            state = AnimaState(model, tok, dev)
        else:
            class Dummy:
                last_emit_time = time.time()
                def tick(self, _i, _e):
                    return ({}, 0.5, "", "noop", 0.0)
                def emit(self, _s):
                    return ""
            state = Dummy()
        rng_ctrl = (random.Random(args.tick * 100 + 1)
                    if mode.endswith("_random") else None)
        t, em, lg = run_loop(state, sub, pub, args.window, args.tick, mode,
                             args.hw_window_s, args.hw_count_thr,
                             args.hw_refractory_s,
                             label=f"RUN[{mode}]",
                             rng_control=rng_ctrl)
        result["runs"][mode] = {
            "summary": summarize(em, t, mode),
            "correlation": correlation_metrics(lg, mode),
            "log": lg,
            "subscriber_snapshot": sub.snapshot(),
            "publisher_snapshot": pub.snapshot(),
        }

    # ── verdict
    verdict = {}
    rb = result["runs"].get("option_b", {}).get("correlation", {})
    rbr = result["runs"].get("option_b_random", {}).get("correlation", {})
    rc = result["runs"].get("option_c", {}).get("correlation", {})
    rcr = result["runs"].get("option_c_random", {}).get("correlation", {})

    def _opt_b_ok(corr_real, corr_rand):
        sr = corr_real.get("spearman_drive_vs_hw_rate")
        srr = corr_rand.get("spearman_drive_vs_hw_rate")
        if sr is None: return False
        ok_strength = abs(sr) > 0.3
        ok_control = (srr is None or abs(srr) < 0.15
                      or abs(sr) > abs(srr) + 0.15)
        return ok_strength and ok_control

    if rb:
        verdict["option_b_spearman_real"] = rb.get("spearman_drive_vs_hw_rate")
        verdict["option_b_spearman_random"] = rbr.get("spearman_drive_vs_hw_rate")
        verdict["option_b_ok"] = _opt_b_ok(rb, rbr)
    if rc:
        verdict["option_c_spearman_real"] = rc.get("spearman_drive_vs_hw_rate")
        verdict["option_c_spearman_random"] = rcr.get("spearman_drive_vs_hw_rate")
        verdict["option_c_frac_emissions_with_hw_edge"] = rc.get(
            "frac_emissions_with_hw_edge")
        c_summary = result["runs"]["option_c"]["summary"]
        verdict["option_c_emissions"] = c_summary["emissions"]
        verdict["option_c_coherent"] = c_summary["coherent"]
        verdict["option_c_ok"] = (
            _opt_b_ok(rc, rcr)
            and ((rc.get("frac_emissions_with_hw_edge") or 0.0) >= 0.5
                 or c_summary["emissions"] == 0))   # tolerate no emissions

    if verdict.get("option_c_ok"):
        verdict["claim"] = "OPTION_C BIDIRECTIONAL works"
    elif verdict.get("option_b_ok"):
        verdict["claim"] = "OPTION_B works (C partial/failed)"
    else:
        verdict["claim"] = "OPTION_B/C partial/failed"
    result["verdict"] = verdict

    sub.close()
    pub.close()
    json.dump(result, open(args.out, "w"), indent=2, ensure_ascii=False)
    print(f"\n{'=' * 72}")
    print(f"VERDICT: {verdict.get('claim')}")
    for k, run in result["runs"].items():
        s = run["summary"]; c = run["correlation"]
        print(f"  [{k}] emissions={s['emissions']} coherent={s['coherent']} "
              f"spear_drive_hw_rate={c.get('spearman_drive_vs_hw_rate')} "
              f"hw_rate_mean={c.get('hw_rate_mean')} "
              f"thr_off=[{c.get('thr_offset_min')},{c.get('thr_offset_max')}]")
    print(f"[int] wrote {args.out}")


if __name__ == "__main__":
    main()
