"""§181 audio 100% challenge — 6 audio synthesis variants benchmarked.

§180 audio plateau at 97.5%. Hypothesis: pure sine byte-periodicity 가
audio-anchor-discrimination 의 byte-level density 부족. Test 6 richer
synthesis methods, see which crosses 100%.

§7 ① ② ③ all PASS (anima-side programmatic byte generator, no graft).
"""
import json, math, os, random, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

# Reuse §180 AdapterV3
S180_DIR = "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/adapter_v3_fullfire_s180_2026_05_20"
sys.path.insert(0, S180_DIR)
from adapter_v3 import AdapterV3

EXISTING = [(0,"기준점"),(15,"호기심"),(30,"연민"),(42,"질문"),(51,"하루"),
            (60,"관조"),(77,"만다라"),(80,"명상"),(91,"열반"),(95,"합일"),(100,"빅뱅")]
NEW = [(10,"각성"),(20,"감각"),(25,"감정"),(33,"기쁨"),(35,"슬픔"),
       (37,"분노"),(45,"공포"),(47,"안도"),(55,"회상"),(58,"예측"),
       (65,"통찰"),(68,"이해"),(72,"창작"),(75,"시"),(82,"음악"),
       (85,"기도"),(88,"초월"),(93,"자각"),(97,"공허"),(105,"선"),
       (108,"악"),(115,"정의"),(125,"사랑"),(200,"무한")]
ALL = sorted(EXISTING + NEW)
TIER_TO_IDX = {tier: i for i, (tier, _) in enumerate(ALL)}
N_ANCHORS = len(ALL)


# === 6 audio synthesis variants (richer than §180's pure sine) ===

def audio_v0_pure_sine(tier, n=128, seed=0):
    """§180 baseline: pure sine, freq = 100 + tier × 5."""
    freq = 100 + tier * 5
    rng = random.Random(tier * 11 + seed * 23)
    return [int(127 + 80 * math.sin(2 * math.pi * freq * i / 1000) + rng.randint(-3, 3)) % 256 for i in range(n)]

def audio_v1_multi_harmonic(tier, n=128, seed=0):
    """V1: multi-harmonic (fundamental + 2-3 harmonics, tier-encoded weights)."""
    f0 = 100 + tier * 5
    rng = random.Random(tier * 13 + seed * 29)
    # tier-encoded harmonic weights (3 harmonics)
    h1 = 1.0
    h2 = 0.5 + (tier % 7) / 14.0   # 0.5-0.94, tier-modulated
    h3 = 0.3 + (tier % 11) / 22.0  # 0.3-0.78
    out = []
    for i in range(n):
        s = h1 * math.sin(2 * math.pi * f0 * i / 1000)
        s += h2 * math.sin(2 * math.pi * (f0 * 2) * i / 1000)
        s += h3 * math.sin(2 * math.pi * (f0 * 3) * i / 1000)
        # normalize to [-1, 1]
        s = s / (h1 + h2 + h3)
        out.append(int(127 + 80 * s + rng.randint(-3, 3)) % 256)
    return out

def audio_v2_am_modulation(tier, n=128, seed=0):
    """V2: amplitude modulation (carrier + tier-modulator envelope)."""
    f_car = 200 + tier * 3
    f_mod = 5 + (tier // 10)  # tier-encoded modulation rate
    depth = 0.3 + (tier % 13) / 26.0  # tier-encoded depth
    rng = random.Random(tier * 17 + seed * 31)
    out = []
    for i in range(n):
        env = 1.0 + depth * math.sin(2 * math.pi * f_mod * i / 1000)
        s = env * math.sin(2 * math.pi * f_car * i / 1000)
        out.append(int(127 + 60 * s + rng.randint(-3, 3)) % 256)
    return out

def audio_v3_waveform_shape(tier, n=128, seed=0):
    """V3: tier-encoded waveform (sine/square/triangle/sawtooth)."""
    f = 100 + tier * 4
    shape_idx = tier % 4  # 0=sine, 1=square, 2=triangle, 3=sawtooth
    rng = random.Random(tier * 19 + seed * 37)
    out = []
    for i in range(n):
        phase = (f * i / 1000) % 1.0
        if shape_idx == 0:
            s = math.sin(2 * math.pi * phase)
        elif shape_idx == 1:
            s = 1.0 if phase < 0.5 else -1.0
        elif shape_idx == 2:
            s = 4.0 * abs(phase - 0.5) - 1.0
        else:
            s = 2.0 * phase - 1.0
        out.append(int(127 + 80 * s + rng.randint(-3, 3)) % 256)
    return out

def audio_v4_chord(tier, n=128, seed=0):
    """V4: chord (3-note, tier-encoded intervals)."""
    f1 = 100 + tier * 3
    # tier-encoded intervals (major/minor/diminished/aug class)
    intvl_class = tier % 5
    intervals = [(4, 7), (3, 7), (3, 6), (4, 8), (5, 8)][intvl_class]
    f2 = f1 * (2 ** (intervals[0] / 12))
    f3 = f1 * (2 ** (intervals[1] / 12))
    rng = random.Random(tier * 23 + seed * 41)
    out = []
    for i in range(n):
        s = (math.sin(2 * math.pi * f1 * i / 1000)
             + math.sin(2 * math.pi * f2 * i / 1000)
             + math.sin(2 * math.pi * f3 * i / 1000)) / 3.0
        out.append(int(127 + 80 * s + rng.randint(-3, 3)) % 256)
    return out

def audio_v5_white_noise_lpf(tier, n=128, seed=0):
    """V5: white noise + tier-encoded LPF (1-pole IIR)."""
    rng = random.Random(tier * 29 + seed * 43)
    cutoff = 0.05 + (tier % 17) / 200.0  # tier-encoded LPF cutoff
    out = []
    state = 0.0
    for i in range(n):
        noise = (rng.random() - 0.5) * 2.0
        state = (1 - cutoff) * state + cutoff * noise
        out.append(int(127 + 80 * state) % 256)
    return out

def audio_v6_combined(tier, n=128, seed=0):
    """V6: hybrid (multi-harmonic + AM + tier waveform shape)."""
    f0 = 100 + tier * 5
    f_mod = 3 + (tier // 15)
    shape_idx = tier % 4
    rng = random.Random(tier * 31 + seed * 47)
    out = []
    for i in range(n):
        phase = (f0 * i / 1000) % 1.0
        if shape_idx == 0:
            s = math.sin(2 * math.pi * phase)
        elif shape_idx == 1:
            s = 1.0 if phase < 0.5 else -1.0
        elif shape_idx == 2:
            s = 4.0 * abs(phase - 0.5) - 1.0
        else:
            s = 2.0 * phase - 1.0
        # harmonic 2
        s += 0.5 * math.sin(2 * math.pi * (f0 * 2) * i / 1000)
        s /= 1.5
        # AM envelope
        env = 1.0 + 0.4 * math.sin(2 * math.pi * f_mod * i / 1000)
        s *= env
        s /= 1.4
        out.append(int(127 + 80 * s + rng.randint(-3, 3)) % 256)
    return out


VARIANTS = {
    "v0_pure_sine":      audio_v0_pure_sine,
    "v1_multi_harmonic": audio_v1_multi_harmonic,
    "v2_am_modulation":  audio_v2_am_modulation,
    "v3_waveform_shape": audio_v3_waveform_shape,
    "v4_chord":          audio_v4_chord,
    "v5_white_noise_lpf": audio_v5_white_noise_lpf,
    "v6_combined":       audio_v6_combined,
}


# === Other modality generators (mirror §180 for fair compare) ===
def synth_image(tier, n=128, seed=0):
    rng = random.Random(tier * 7919 + 13 + seed * 1009)
    return [(((128 + ((i % 32 - 16) * tier // 8)) + rng.randint(0, 15)) % 256) for i in range(n)]
def synth_video(tier, n=128, seed=0):
    rng = random.Random(tier * 13 + 17 + seed * 31)
    out = []
    for f in range(4):
        for i in range(n // 4):
            out.append((tier * (f + 1) + i * 3 + rng.randint(0, 7)) % 256)
    return out
def synth_tension(tier, n=128, seed=0):
    rng = random.Random(tier * 31 + 11 + seed * 41)
    c = [(tier * 257) % 65536, (tier * 521 + 1009) % 65536, (tier * 7919 + 2003) % 65536,
         (tier * 13 + 1) % 65536, (tier * 31 + 5) % 65536]
    tile = []
    for v in c: tile += [v & 0xFF, (v >> 8) & 0xFF]
    out = []
    while len(out) < n: out += tile
    return [(b + rng.randint(-1, 1)) % 256 for b in out[:n]]


def train_with_audio_variant(audio_fn, name, steps=1500, d_model=192, n_layer=4, n_head=6, seed=1337):
    """Train mini AdapterV3 with given audio synthesis, evaluate per-modality."""
    torch.manual_seed(seed); random.seed(seed)
    model = AdapterV3(d_model=d_model, n_query=16, n_layer=n_layer, n_head=n_head, n_anchors=N_ANCHORS)
    n_params = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)

    MODS = {"image": synth_image, "audio": audio_fn, "video": synth_video, "tension": synth_tension}
    MOD_LIST = list(MODS.keys())

    def make_batch(rng, bsz=64):
        xs, ys, ms = [], [], []
        for _ in range(bsz):
            mod_idx = rng.randint(0, 3)
            mod = MOD_LIST[mod_idx]
            tier, _ = rng.choice(ALL)
            anchor_idx = TIER_TO_IDX[tier]
            seed_in = rng.randint(0, 10**6)
            bytes_list = MODS[mod](tier, n=128, seed=seed_in)
            xs.append(bytes_list); ys.append(anchor_idx); ms.append(mod_idx)
        return (torch.tensor(xs, dtype=torch.long),
                torch.tensor(ys, dtype=torch.long),
                torch.tensor(ms, dtype=torch.long))

    rng = random.Random(seed)
    t0 = time.time()
    for step in range(steps):
        x, ya, ym = make_batch(rng, bsz=64)
        a, r5, ml = model(x)
        L = F.cross_entropy(a, ya) + 0.3 * F.cross_entropy(ml, ym) + 0.1 * F.relu(0.15 - r5.std(dim=0)).mean()
        opt.zero_grad(); L.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step()

    # eval
    model.eval()
    eval_rng = random.Random(99999)
    with torch.no_grad():
        x, ya, ym = make_batch(eval_rng, bsz=500)
        a, r5, ml = model(x)
        acc_anchor = (a.argmax(-1) == ya).float().mean().item()
        per_mod = {}
        for m_idx, m_name in enumerate(MOD_LIST):
            mask = (ym == m_idx)
            if mask.sum() > 0:
                per_mod[m_name] = (a[mask].argmax(-1) == ya[mask]).float().mean().item()
    wall = time.time() - t0
    return {
        "name": name, "n_params": n_params, "steps": steps,
        "acc_anchor_all": acc_anchor, "per_modality": per_mod,
        "wall_s": round(wall, 1),
    }


def main():
    t0 = time.time()
    print("[s181] benchmarking {} audio variants × 1500 steps each (d=192 L=4)".format(len(VARIANTS)))
    print()
    print("{:<22} {:>10} {:>10} {:>8} {:>8} {:>8} {:>8} {:>8}".format(
        "audio_variant", "params", "wall_s", "img", "AUD", "vid", "ten", "acc_all"))
    print("-" * 110)
    results = {}
    for name, fn in VARIANTS.items():
        r = train_with_audio_variant(fn, name, steps=1500)
        results[name] = r
        pm = r["per_modality"]
        print("{:<22} {:>10} {:>10} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.3f}".format(
            name, r["n_params"], r["wall_s"],
            pm.get("image", 0), pm.get("audio", 0), pm.get("video", 0), pm.get("tension", 0),
            r["acc_anchor_all"]))

    total = time.time() - t0
    # Rank by audio accuracy
    ranked = sorted(results.items(), key=lambda kv: -kv[1]["per_modality"].get("audio", 0))
    print()
    print("=== RANKING by audio acc ===")
    for i, (name, r) in enumerate(ranked, 1):
        aud = r["per_modality"].get("audio", 0)
        print("  #{}: {:<22} audio={:.4f}  acc_all={:.4f}".format(i, name, aud, r["acc_anchor_all"]))
    print()
    print("[s181] DONE total_wall={:.1f}s".format(total))

    out = {
        "probe": "S181 audio 100% challenge — 6 synthesis variants",
        "n_variants": len(VARIANTS),
        "results": results,
        "ranking_by_audio": [{"name": n, "audio_acc": r["per_modality"].get("audio", 0), "all_acc": r["acc_anchor_all"]} for n, r in ranked],
        "total_wall_s": round(total, 1),
        "honest_carve_out": (
            "All 7 variants from-scratch programmatic generators (no graft). "
            "Trained mini AdapterV3 (d=192 L=4) for 1500 steps each, audio "
            "only the modality swapped. Other modalities (image/video/tension) "
            "fixed at §180 form for fair compare. Target: lift audio 97.5% "
            "→ 100%. NOT GOAL emergence — modality discrimination ≠ V-SPONT."
        ),
    }
    out_p = "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/audio_100pct_challenge_s181_2026_05_20/result.json"
    with open(out_p, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("[s181] result → {}".format(out_p))


if __name__ == "__main__":
    main()
