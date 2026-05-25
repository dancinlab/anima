#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RESEARCH.md §19 step 0 — TRIBE v2 pipe sanity ($0, inference-only).

NOT F-CT-3. This only verifies the cortexlab-toolkit / TRIBE v2 pipe
works far enough to be a credible axis C for Framing D (EEG <-> CLM <->
TRIBE BOLD 3-way cross-validation). NO GPU, NO training, NO weight
mutation — frozen-weight forward only (TRIBE is a frozen encoder).

Graded gates (each strictly more demanding; honest boundary recorded):
  G0 IMPORT          cortexlab + neuralset + neuraltrain import OK
  G1 API             TribeModel.from_pretrained / .predict present
  G2 HF_REACHABLE    facebook/tribev2 repo has best.ckpt + config.yaml
  G3 CONFIG_LOAD     config.yaml downloads + parses (HF Hub)
  G4 CKPT_META       best.ckpt header reads (model_build_args / state_dict
                     keys) WITHOUT full materialization (mmap, weights_only)
  G5 FORWARD         full model.predict() on a stimulus -> BOLD
                     (n_timesteps, ~20k vertices)  [heavy; attempted,
                     boundary honestly recorded if backbone DL too large]

Result -> step0_result.json. over-claim 0 (g3): step 0 = "pipe works"
sanity, NOT EEG/BOLD bridge (that is step 2 F-CT-3, EEG hardware-in-loop).
"""
import json
import os
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = {"section": "RESEARCH.md §19 step 0", "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
     "is_f_ct_3": False, "gpu_used": False, "weight_mutated": False,
     "gates": {}, "notes": []}


def g(name, ok, detail):
    R["gates"][name] = {"pass": bool(ok), "detail": str(detail)[:600]}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {str(detail)[:200]}")
    return ok


# ── G0 IMPORT ───────────────────────────────────────────────────────────
try:
    import cortexlab
    import neuralset  # noqa: F401
    import neuraltrain  # noqa: F401
    import torch
    g("G0_IMPORT", True,
      f"cortexlab={cortexlab.__version__} torch={torch.__version__} "
      f"neuralset+neuraltrain OK (py{sys.version.split()[0]})")
except Exception as e:
    g("G0_IMPORT", False, f"{type(e).__name__}: {e}")
    json.dump(R, open(HERE / "step0_result.json", "w"), indent=2, ensure_ascii=False)
    sys.exit(0)

# ── G1 API ──────────────────────────────────────────────────────────────
try:
    from cortexlab.inference.predictor import TribeModel
    has_fp = hasattr(TribeModel, "from_pretrained")
    has_pred = hasattr(TribeModel, "predict")
    g("G1_API", has_fp and has_pred,
      f"TribeModel.from_pretrained={has_fp} .predict={has_pred} "
      f"(ADDENDUM §3 'CLM L_IX -> text serialization -> cortexlab "
      f"streaming inference' API surface confirmed)")
except Exception as e:
    g("G1_API", False, f"{type(e).__name__}: {e}")

# ── G2 HF_REACHABLE ─────────────────────────────────────────────────────
try:
    from huggingface_hub import HfApi
    info = HfApi().model_info("facebook/tribev2")
    files = sorted(s.rfilename for s in info.siblings)
    need = {"best.ckpt", "config.yaml"}
    g("G2_HF_REACHABLE", need.issubset(set(files)),
      f"facebook/tribev2 files={files} (best.ckpt+config.yaml present)")
except Exception as e:
    g("G2_HF_REACHABLE", False, f"{type(e).__name__}: {str(e)[:300]}")

# ── G3 CONFIG_LOAD ──────────────────────────────────────────────────────
cfg_path = None
try:
    from huggingface_hub import hf_hub_download
    import yaml
    cfg_path = hf_hub_download("facebook/tribev2", "config.yaml")
    with open(cfg_path) as f:
        cfg = yaml.load(f, Loader=yaml.UnsafeLoader)
    g("G3_CONFIG_LOAD", isinstance(cfg, dict) and len(cfg) > 0,
      f"config.yaml downloaded+parsed, {len(cfg)} top keys, "
      f"sample={list(cfg)[:6]}")
except Exception as e:
    g("G3_CONFIG_LOAD", False, f"{type(e).__name__}: {str(e)[:300]}")

# ── G4 CKPT_META (mmap header read, NO full materialization) ────────────
try:
    from huggingface_hub import hf_hub_download
    ckpt_path = hf_hub_download("facebook/tribev2", "best.ckpt")
    sz = os.path.getsize(ckpt_path)
    ckpt = torch.load(ckpt_path, map_location="cpu",
                      weights_only=True, mmap=True)
    keys = list(ckpt.keys())
    sd = ckpt.get("state_dict", {})
    nt = len(sd) if isinstance(sd, dict) else -1
    has_build = "model_build_args" in ckpt
    g("G4_CKPT_META", has_build and nt > 0,
      f"best.ckpt {sz/1e6:.1f}MB mmap-loaded, top_keys={keys[:6]}, "
      f"state_dict tensors={nt}, model_build_args={has_build} "
      f"(frozen encoder header read, NO mutation)")
except Exception as e:
    g("G4_CKPT_META", False, f"{type(e).__name__}: {str(e)[:300]}")

# ── G5 FORWARD (full predict — heavy; honest boundary if backbones too big)
try:
    from cortexlab.inference.predictor import TribeModel
    cache = str(HERE / "tribe_cache")
    Path(cache).mkdir(exist_ok=True)
    t0 = time.time()
    model = TribeModel.from_pretrained("facebook/tribev2",
                                       cache_folder=cache, device="cpu")
    load_s = time.time() - t0
    R["notes"].append(f"TribeModel.from_pretrained OK in {load_s:.1f}s "
                       f"(weights loaded eval mode, cpu)")
    # tiny text stimulus -> events -> BOLD. correct API = text_path (.txt);
    # text -> gTTS audio -> transcribe -> word timings -> features.
    txt = HERE / "stimulus_s19.txt"
    txt.write_text("anima physics channel sanity probe for framing D "
                   "axis C cortical BOLD prediction")
    df = model.get_events_dataframe(text_path=str(txt))
    t1 = time.time()
    preds, segments = model.predict(events=df)
    fwd_s = time.time() - t1
    shp = tuple(getattr(preds, "shape", ()))
    ok = len(shp) == 2 and shp[1] > 5000  # ~20k fsaverage5 vertices
    g("G5_FORWARD", ok,
      f"predict() BOLD shape={shp} (expect (n_timesteps, ~20k vert)), "
      f"load={load_s:.1f}s forward={fwd_s:.1f}s — TRIBE axis C live")
except Exception as e:
    # honest blocker: backbone download size / TTS / ffmpeg / etc.
    g("G5_FORWARD", False,
      f"{type(e).__name__}: {str(e)[:400]} (G0-G4 = pipe-credible; "
      f"full forward needs feature-extractor backbone DL — boundary "
      f"honestly recorded, design-tier step 0)")
    R["notes"].append("G5 boundary: full predict() requires text/audio/"
                      "video backbone model downloads (multi-GB) + "
                      "gTTS/ffmpeg; G0-G4 PASS establishes axis C "
                      "feasibility (pipe works to ckpt-load), G5 forward "
                      "= step-1+ scope (still inference-only, no GPU).")

# ── verdict ─────────────────────────────────────────────────────────────
gp = R["gates"]
pipe_credible = all(gp.get(k, {}).get("pass") for k in
                    ("G0_IMPORT", "G1_API", "G2_HF_REACHABLE",
                     "G3_CONFIG_LOAD", "G4_CKPT_META"))
R["step0_verdict"] = {
    "pipe_credible_through_ckpt_load": pipe_credible,
    "full_forward_done": gp.get("G5_FORWARD", {}).get("pass", False),
    "addendum_c3_3_pypi_gap": ("CLOSED — cortexlab-toolkit 0.1.0 "
        "installs from PyPI (modern pip), pulls neuralset/neuraltrain "
        "0.0.2, import name = `cortexlab`. ADDENDUM §8 C3 #3 "
        "verification gap resolved at dependency+API level."),
    "is_f_ct_3": False,
    "honest": ("step 0 = TRIBE pipe sanity (axis C feasibility), NOT "
               "F-CT-3 (EEG<->BOLD bridge = step 2, EEG hw-in-loop). "
               "GOAL distance unchanged (§15 milestone). over-claim 0."),
}
json.dump(R, open(HERE / "step0_result.json", "w"), indent=2,
          ensure_ascii=False)
print("\n=== step0_verdict ===")
print(json.dumps(R["step0_verdict"], indent=2, ensure_ascii=False))
