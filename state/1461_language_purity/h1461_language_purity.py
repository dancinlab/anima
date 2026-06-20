#!/usr/bin/env python3
"""h1461_language_purity.py — G6 돌파 렌즈 ⑥ LANGUAGE-PURITY (code-switch 오염 통제).

가설 (a_break_the_wall (b) 변수혼재 — 미통제 언어 변수):
  6 렌즈(H_1435 data / 1436 obj / 1437 form / 1439 bind-head / 1449 attention /
  1440 curriculum)가 전부 🧱 WALL=CAPACITY 로 수렴. 그러나 base 모델
  h1129c_chat.pt = anima-clm-midcap-303m-broad-en-emergent = "English-DOMINANT
  broad corpus (ASCII-filtered 5-lang wiki)" + chat 한글 대화 혼입.
  ★ H_1129 HF notes 원문 경고: "the multilang 7B + 303M v1 both
  CODE-SWITCH-COLLAPSED."
  H_1305 FALS detector(COMPARATOR/MEASURABLE) 는 전부 ASCII 영어 단어.
  → mouth 가 영어 falsifiable claim 생성 중 한글로 code-switch 하면 FALS=0 이
  될 수 있다. 즉 6 capacity 수렴이 사실은 language-contamination ARTIFACT 일
  가능성. 벽이 capacity 가 아니라 언어오염이면 ASCII-only 강제가 돌파.

설계 ($0, 재학습 불필요 — 디코드 제약만):
  base h1129c_chat.pt 동일 가중치를 두 디코드 모드로 H_1435 FROZEN 5-bar 재측정.
    UNMASKED : 기존 _decode (code-switch 허용) — base plateau 재현
    MASKED   : 디코드 매 스텝 logit 의 non-ASCII byte(0x80-0xFF) 를 -inf 마스킹
               → 영어/ASCII-only 강제 생성 (언어필터일 뿐 detector 정답 주입 아님)
  핵심: ASCII-only 가 B3 cross-shuffle COLLAPSE 를 살리나 + FALS 가 올라가나.

해석 (frozen-first c9, anti-tune):
  masked 가 FALS↑ + B3 collapse → 벽은 LANGUAGE-POLLUTION (돌파)
  둘 다 FALS=0           → 벽은 CAPACITY 진짜 천장 (언어 무관, 6 수렴 확정)
  bar 불변. masking 은 byte 0x80-0xFF 만 끄는 언어필터; comparator/measurable 는
  전부 ASCII(<0x80) 이므로 falsifiable 토큰 자체는 막히지 않음(C1 검증).

DIRECTIONAL: torch + gauge_lib._decode (a_engine_native_learning) — engine-native
follow-on 필요. p7 (perplexity/LLM-judge 아님), 캡처 출력이 증거.
"""
import os, sys, json, importlib.util, random

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.environ["G6_PROBES"]
CKPT_BASE = os.environ["G6_CKPT"]

import torch
import torch.nn.functional as F


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _load("gauge", os.path.join(PROBES, "gauge_lib.py"))
h5 = _load("h1305", os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py"))
gc = _load("g6_common", os.path.join(HERE, "g6_common.py"))

COMPARATOR = h5.COMPARATOR
MEASURABLE = h5.MEASURABLE
_is_falsifiable = h5._is_falsifiable
SEEDS = gc.SEEDS  # [7, 4302, 4303]

# ── ASCII-mask: build once a (V,) tensor with non-ASCII bytes set to -inf ──
NEG = float("-inf")


def _ascii_mask_vec(device):
    m = torch.zeros(256, device=device)
    m[128:256] = NEG          # bytes 0x80..0xFF (Korean UTF-8 lead/continuation) -> -inf
    return m


# ── A copy of gauge_lib._decode that, when ascii_only=True, masks non-ASCII ──
# BYTE-IDENTICAL to gauge_lib._decode except the single masked_add_ line. Same
# top_k=40, temp=0.7, seed_rng-driven generator, same stops, same per-step RNG
# draw order so UNMASKED reproduces the frozen base read exactly.
def _decode_maskable(model, seed_text, max_new, block=512, top_k=40, temp=0.7,
                     seed_rng=7, device=None, ascii_only=False):
    if device is None:
        try:
            device = next(model.parameters()).device
        except StopIteration:
            device = "cpu"
    was_training = model.training
    model.eval()
    gen = torch.Generator(device="cpu")
    gen.manual_seed(seed_rng)
    amask = _ascii_mask_vec(device) if ascii_only else None
    idx = torch.tensor([list(seed_text.encode("utf-8"))], dtype=torch.long, device=device)
    out_bytes = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    for _ in range(max_new):
        ctx = idx[:, -block:]
        model_out = model(ctx)
        logits = g._logits_last(model_out, torch) / temp
        if ascii_only:
            logits = logits + amask          # non-ASCII -> -inf BEFORE top-k
        if top_k:
            v, _ = torch.topk(logits, min(top_k, logits.shape[-1]))
            logits = logits.masked_fill(logits < v[-1], NEG)
        probs = F.softmax(logits, dim=-1).cpu()
        nb = int(torch.multinomial(probs, 1, generator=gen).item())
        out_bytes.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        txt = bytes(out_bytes).decode("utf-8", "ignore")
        if any(st in txt for st in stops):
            break
    if was_training:
        model.train()
    t = bytes(out_bytes).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st)
        if i >= 0:
            t = t[:i]
    return t.strip(), out_bytes


def _eval_mode(m, cfg, seeds, ascii_only):
    """FROZEN 5-bar (g6_common identical) under a chosen decode mode.
    Monkeypatch gauge_lib._decode so gc.evaluate's internal decode obeys the mode,
    returning text exactly as g6_common expects (str)."""
    def patched(model, seed_text, max_new, torch_mod, block=512, top_k=40, temp=0.7,
                seed_rng=7, device=None):
        t, _ = _decode_maskable(model, seed_text, max_new, block=block, top_k=top_k,
                                temp=temp, seed_rng=seed_rng, device=device,
                                ascii_only=ascii_only)
        return t
    # g6_common loaded its OWN gauge instance (gc.g) — _decode_ideas calls
    # gc.g._decode. Patch THAT object (and our own g for safety) so the mask
    # actually reaches the evaluate() decode path.
    targets = []
    for mod in (gc.g, g):
        if mod is not None and hasattr(mod, "_decode"):
            targets.append((mod, mod._decode))
            mod._decode = patched
    # decode source must use the right gauge instance for IDEATION_SEEDS too
    seeds = gc.g.IDEATION_SEEDS if hasattr(gc.g, "IDEATION_SEEDS") else gc.HELDOUT_SEEDS
    try:
        rec = gc.evaluate(m, cfg, "ascii" if ascii_only else "raw", seeds)
    finally:
        for mod, orig in targets:
            mod._decode = orig
    return rec


def _nonascii_ratio(m, cfg, seeds, ascii_only):
    """Free-generation non-ASCII (Korean) byte ratio over the eval seeds."""
    tot, non = 0, 0
    kr_samples = []
    for sr in SEEDS:
        for s in seeds:
            t, ob = _decode_maskable(m, s, gc.MAX_NEW, block=cfg["block"],
                                     seed_rng=sr, device=next(m.parameters()).device,
                                     ascii_only=ascii_only)
            for b in ob:
                tot += 1
                if b >= 128:
                    non += 1
            # capture a sample with Korean for the report
            if any(ord(ch) > 127 for ch in t) and len(kr_samples) < 3:
                kr_samples.append(t[:80])
    return (non / tot if tot else 0.0), kr_samples


def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[h1461] device={dev} ckpt={CKPT_BASE}", flush=True)
    m, cfg = gc.load_model(CKPT_BASE, dev)
    print(f"[h1461] cfg={cfg}", flush=True)

    # eval seed set = the in-domain gauge IDEATION_SEEDS used by g6_common evaluate
    eval_seeds = g.IDEATION_SEEDS if hasattr(g, "IDEATION_SEEDS") else gc.HELDOUT_SEEDS
    print(f"[h1461] eval_seeds n={len(eval_seeds)}", flush=True)

    # ── (0) base non-ASCII (Korean) byte ratio, UNMASKED free generation ──
    print("\n[h1461] (0) measuring base non-ASCII ratio (UNMASKED) ...", flush=True)
    ratio_raw, kr_raw = _nonascii_ratio(m, cfg, eval_seeds, ascii_only=False)
    print(f"  UNMASKED non-ASCII byte ratio = {ratio_raw:.4f}", flush=True)
    for s in kr_raw:
        print(f"    KR-sample: {s!r}", flush=True)
    ratio_msk, _ = _nonascii_ratio(m, cfg, eval_seeds, ascii_only=True)
    print(f"  MASKED   non-ASCII byte ratio = {ratio_msk:.4f} (must be 0.0)", flush=True)

    # ── (C1) calibration: ASCII-mask does NOT block falsifiable tokens ──
    # every COMPARATOR/MEASURABLE word is pure ASCII (<0x80) -> survives mask
    nonascii_detector = [w for w in (COMPARATOR | MEASURABLE)
                         if any(ord(ch) > 127 for ch in w)]
    c1_pass = len(nonascii_detector) == 0
    print(f"\n[h1461] (C1) detector-token ASCII-safety: "
          f"{len(nonascii_detector)} non-ASCII comparator/measurable tokens -> "
          f"C1_pass={c1_pass}", flush=True)

    # ── UNMASKED 5-bar (reproduces base plateau) ──
    print("\n[h1461] === UNMASKED (code-switch allowed) 5-bar ===", flush=True)
    raw = _eval_mode(m, cfg, eval_seeds, ascii_only=False)
    print(f"  raw  FALS_in={raw['FALS_in']} DIST_in={raw['DIST_in']} "
          f"FALS_shuf={raw['FALS_shuf']} FALS_ho={raw['FALS_ho']}", flush=True)

    # ── MASKED 5-bar (ASCII-only forced) ──
    print("\n[h1461] === MASKED (ASCII-only forced) 5-bar ===", flush=True)
    msk = _eval_mode(m, cfg, eval_seeds, ascii_only=True)
    print(f"  ascii FALS_in={msk['FALS_in']} DIST_in={msk['DIST_in']} "
          f"FALS_shuf={msk['FALS_shuf']} FALS_ho={msk['FALS_ho']}", flush=True)
    # SELF-GUARD: every MASKED decode text MUST be pure ASCII (mask reached the
    # evaluate() path). If any non-ASCII byte survived, the mask did NOT apply and
    # the MASKED row is invalid — abort rather than stamp a false negative.
    bad = 0
    for ps in msk["per_seed"]:
        for t in ps.get("in_texts", []) + ps.get("ho_texts", []):
            if any(ord(c) > 127 for c in t):
                bad += 1
    print(f"  [GUARD] MASKED texts with surviving non-ASCII = {bad} (must be 0)", flush=True)
    assert bad == 0, "ASCII mask did NOT reach the evaluate() decode path"

    # ── treat UNMASKED as BASE, MASKED as the "treatment"; reuse frozen print_bars
    #    to read whether ASCII-only earns the lift + B3 collapse over the raw base.
    print("\n[h1461] === FROZEN 5-BAR: MASKED(treatment) vs UNMASKED(base) ===", flush=True)
    bars = gc.print_bars("H_1461 ASCII-PURITY", raw, msk)

    # interpretation
    masked_fals_up = msk["FALS_in"] > raw["FALS_in"]
    b3_collapse_masked = msk["FALS_shuf"] < msk["FALS_in"]
    both_zero = (raw["FALS_in"] == 0 and msk["FALS_in"] == 0)
    if both_zero:
        verdict = ("🧱 CAPACITY-CONFIRMED — ASCII-only forcing does NOT recover FALS "
                   "(both raw & masked FALS_in=0); the 6-lens wall is language-INVARIANT "
                   "=> WALL=CAPACITY confirmed (code-switch was NOT the cause).")
    elif masked_fals_up and b3_collapse_masked and bars["green"]:
        verdict = ("🟢 LANGUAGE-POLLUTION BREAKTHROUGH — ASCII-only forcing recovers FALS "
                   "AND B3 cross-shuffle COLLAPSES => the 6-lens capacity convergence was a "
                   "code-switch CONTAMINATION artifact (DIRECTIONAL, engine-native follow-on).")
    elif masked_fals_up:
        verdict = ("🟠 PARTIAL — ASCII-only forcing raises FALS but does NOT clear the full "
                   "frozen 5-bar (B3 collapse / floor); language matters but is not the whole "
                   "wall (DIRECTIONAL).")
    else:
        verdict = ("🧱 CAPACITY-LEANING — ASCII-only forcing did not raise FALS over the raw "
                   "base => language pollution is NOT the dominant wall (DIRECTIONAL).")

    print(f"\n[h1461] VERDICT: {verdict}", flush=True)

    out = {
        "hypothesis": "H_1461_language_purity",
        "ckpt": CKPT_BASE,
        "device": dev,
        "seeds": SEEDS,
        "eval_seeds_n": len(eval_seeds),
        "nonascii_ratio_unmasked": round(ratio_raw, 4),
        "nonascii_ratio_masked": round(ratio_msk, 4),
        "korean_samples_unmasked": kr_raw,
        "C1_detector_ascii_safe": bool(c1_pass),
        "C1_nonascii_detector_tokens": nonascii_detector,
        "UNMASKED": {k: raw[k] for k in ("FALS_in", "DIST_in", "FALS_shuf", "FALS_ho")},
        "MASKED": {k: msk[k] for k in ("FALS_in", "DIST_in", "FALS_shuf", "FALS_ho")},
        "frozen_bars_masked_vs_unmasked": bars,
        "masked_fals_up": bool(masked_fals_up),
        "b3_collapse_masked": bool(b3_collapse_masked),
        "both_fals_zero": bool(both_zero),
        "verdict": verdict,
        "per_seed_unmasked": raw["per_seed"],
        "per_seed_masked": msk["per_seed"],
    }
    outp = os.path.join(HERE, "h1461_result.json")
    with open(outp, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[h1461] wrote {outp}", flush=True)


if __name__ == "__main__":
    main()
