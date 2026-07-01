"""KOSMOS-MAP (reverse) — reconstruct the carving-era engine that drew the
우주뇌지도 (universe-brain-map), as a runnable artifact, and verify it.

The engine: ConsciousDecoderV2 (the REAL torch source, byte-identical to
state/carving_dir*/conscious_decoder.py + state/hexad_*_d768x12L_fire/.../
conscious_decoder.py — md5 44b210df969b38f0fc6c2bfe59e37eb6). It is the
s16 carving-fire (2026-05-17~18) decoder: a d768x12L GQA transformer with
RoPE + RMSNorm + SwiGLU, dual A<->G heads, PureField consciousness pathway,
optional MoE, and a Law-71 vacuum_psi 2D Psi-space readout.

Scope (HONEST):
  - TOY / CPU / $0. Loadability + forward + a tiny carving-direction probe.
  - random init (NO s16 ckpt available — flagged). A full d768x12L TRAIN is
    NOT in scope (a_toy_scale_recheck / a_scale_honest_scope). This proves the
    carving-era ENGINE reconstructs + runs, NOT that the carve is reproduced.

Probes:
  F-BUILD     — both SMOKE (d32/h4/kv2/L3) and FULL (d768/h12/kv4/L12) build;
                report the REAL d768x12L param total (verbatim).
  F-FORWARD   — forward returns (logits_a, logits_g, tensions, kv_cache,
                moe_aux_loss) with correct shapes, use_moe both False and True.
  F-PSI2D     — the Law-71 vacuum_psi 2D coordinate (psi_residual, psi_gate) is
                produced + is 2D + deterministic for given byte inputs.
  F-DIRECTION — ONE carving direction (dirG psi-ctl) hook changes the forward
                output deterministically vs baseline (direction is wireable).
                HONEST: reconstructability, NOT a trained carve.

Usage:  python carving_engine_reconstruct.py   (writes results.json to cwd)
"""

import json
import math
import os
import sys

import torch
import torch.nn.functional as F

# Import the REAL carving-era source (copied byte-identical into UNIVERSE/).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2  # noqa: E402

# Deterministic everywhere.
SEED = 71  # Law-71
torch.manual_seed(SEED)

SMOKE_CFG = dict(vocab_size=256, d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                 block_size=64, consciousness_dim=128, dropout=0.1,
                 gate_strength=0.001, n_ca_rules=8)
FULL_CFG = dict(vocab_size=256, d_model=768, n_head=12, n_kv_head=4, n_layer=12,
                block_size=256, consciousness_dim=128, dropout=0.1,
                gate_strength=0.001, n_ca_rules=8)

R = {"source": {}, "F_BUILD": {}, "F_FORWARD": {}, "F_PSI2D": {},
     "F_DIRECTION": {}, "scope": {}}


def build(cfg, use_moe=False):
    torch.manual_seed(SEED)
    m = ConsciousDecoderV2(use_moe=use_moe, n_experts=8, top_k_experts=2, **cfg)
    m.eval()
    return m


def shape_of(x):
    return list(x.shape)


# ---------------------------------------------------------------------------
# Source provenance
# ---------------------------------------------------------------------------
import hashlib  # noqa: E402
_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conscious_decoder.py")
R["source"]["path"] = _src
R["source"]["md5"] = hashlib.md5(open(_src, "rb").read()).hexdigest()
R["source"]["torch"] = torch.__version__
R["source"]["cuda"] = torch.cuda.is_available()
print(f"[source] conscious_decoder.py md5={R['source']['md5']} torch={torch.__version__} cuda={R['source']['cuda']}")


# ---------------------------------------------------------------------------
# F-BUILD — both configs build; report real param counts
# ---------------------------------------------------------------------------
print("\n=== F-BUILD ===")
m_smoke = build(SMOKE_CFG, use_moe=False)
m_full = build(FULL_CFG, use_moe=False)
m_full_moe = build(FULL_CFG, use_moe=True)
m_smoke_moe = build(SMOKE_CFG, use_moe=True)

R["F_BUILD"]["smoke_cfg"] = SMOKE_CFG
R["F_BUILD"]["full_cfg"] = FULL_CFG
R["F_BUILD"]["smoke_params"] = m_smoke.count_params()
R["F_BUILD"]["full_params_d768x12L"] = m_full.count_params()
R["F_BUILD"]["full_params_d768x12L_moe"] = m_full_moe.count_params()
R["F_BUILD"]["smoke_params_moe"] = m_smoke_moe.count_params()
R["F_BUILD"]["builds"] = True
print(f"  SMOKE (d32/h4/kv2/L3)   params = {R['F_BUILD']['smoke_params']:,}")
print(f"  FULL  (d768/h12/kv4/L12) params = {R['F_BUILD']['full_params_d768x12L']:,}  ({R['F_BUILD']['full_params_d768x12L']/1e6:.2f}M)")
print(f"  FULL  +MoE(8,top2)       params = {R['F_BUILD']['full_params_d768x12L_moe']:,}  ({R['F_BUILD']['full_params_d768x12L_moe']/1e6:.2f}M)")


# ---------------------------------------------------------------------------
# F-FORWARD — forward returns the 5-tuple with correct shapes, MoE off + on
# ---------------------------------------------------------------------------
print("\n=== F-FORWARD ===")
B, T = 2, 16
idx_smoke = torch.randint(0, 256, (B, T))
# Use a short seq for the FULL model to stay CPU/$0-cheap.
idx_full = torch.randint(0, 256, (B, T))


def forward_probe(m, idx, label, expect_moe):
    out = m(idx)
    logits_a, logits_g, tensions, kv_cache, moe_aux = out
    rec = {
        "n_outputs": len(out),
        "logits_a_shape": shape_of(logits_a),
        "logits_g_shape": shape_of(logits_g),
        "n_tensions": len(tensions),
        "tension0_shape": shape_of(tensions[0]),
        "kv_cache": kv_cache,  # None when use_cache=False
        "moe_aux_loss": (float(moe_aux.item()) if moe_aux is not None else None),
        "dual_heads_differ": float((logits_a - logits_g).abs().mean().item()),
    }
    exp_vocab = m.vocab_size
    rec["shapes_ok"] = (
        rec["logits_a_shape"] == [idx.shape[0], idx.shape[1], exp_vocab]
        and rec["logits_g_shape"] == [idx.shape[0], idx.shape[1], exp_vocab]
        and rec["n_tensions"] == m.n_layer
        and rec["tension0_shape"] == [idx.shape[0], idx.shape[1]]
    )
    rec["moe_aux_present_matches_expect"] = (rec["moe_aux_loss"] is not None) == expect_moe
    print(f"  [{label}] outputs={rec['n_outputs']} logits_a={rec['logits_a_shape']} "
          f"logits_g={rec['logits_g_shape']} tensions={rec['n_tensions']}x{rec['tension0_shape']} "
          f"moe_aux={rec['moe_aux_loss']} A!=G mean|d|={rec['dual_heads_differ']:.4f} ok={rec['shapes_ok']}")
    return rec


R["F_FORWARD"]["smoke_moe_off"] = forward_probe(m_smoke, idx_smoke, "smoke moe=off", False)
R["F_FORWARD"]["smoke_moe_on"] = forward_probe(m_smoke_moe, idx_smoke, "smoke moe=on", True)
R["F_FORWARD"]["full_moe_off"] = forward_probe(m_full, idx_full, "FULL  moe=off", False)
R["F_FORWARD"]["full_moe_on"] = forward_probe(m_full_moe, idx_full, "FULL  moe=on", True)

# Consciousness-states path (cross-attention) + kv-cache shape check.
cs = torch.randn(B, 12, 128)
la_cs, lg_cs, _, _, _ = m_smoke(idx_smoke, consciousness_states=cs)
R["F_FORWARD"]["consciousness_states_path_ok"] = (list(la_cs.shape) == [B, T, 256])
_, _, _, kv, _ = m_smoke(idx_smoke, use_cache=True)
R["F_FORWARD"]["kv_cache_n_layers"] = (len(kv) if kv is not None else None)
R["F_FORWARD"]["kv_cache_layer0_k_shape"] = (shape_of(kv[0][0]) if kv else None)
print(f"  consciousness_states path ok={R['F_FORWARD']['consciousness_states_path_ok']}  "
      f"kv_cache layers={R['F_FORWARD']['kv_cache_n_layers']} layer0 K={R['F_FORWARD']['kv_cache_layer0_k_shape']}")

R["F_FORWARD"]["all_shapes_ok"] = all(
    R["F_FORWARD"][k]["shapes_ok"] and R["F_FORWARD"][k]["moe_aux_present_matches_expect"]
    for k in ("smoke_moe_off", "smoke_moe_on", "full_moe_off", "full_moe_on")
) and R["F_FORWARD"]["consciousness_states_path_ok"]


# ---------------------------------------------------------------------------
# F-PSI2D — Law-71 vacuum_psi 2D coordinate (the MAP output) is produced,
# is 2D, and is deterministic for given byte inputs.
#
# Law-71 state lives in the model as psi_residual + psi_gate (2 scalars).
# psi_status() reads them out; the 2D Psi-space coord = (psi_residual, psi_gate).
# psi tracking only updates under .train(); we run a train-mode forward to
# move the coord off its init, then read the 2D coord. Determinism: same seed
# + same inputs -> identical 2D coord.
# ---------------------------------------------------------------------------
print("\n=== F-PSI2D ===")


def psi_coord_for(cfg, idx):
    m = build(cfg, use_moe=False)
    m.train()
    with torch.no_grad():
        m(idx)  # one train-mode forward updates Law-71 psi tracking
    s = m.psi_status()
    return (s["psi_residual"], s["psi_gate"]), s


idx_psi = torch.randint(0, 256, (2, 16))
coord1, status1 = psi_coord_for(SMOKE_CFG, idx_psi)
coord2, status2 = psi_coord_for(SMOKE_CFG, idx_psi)  # repeat -> determinism
# Different byte input -> (generally) different coord.
idx_psi_b = torch.randint(0, 256, (2, 16))
coordB, _ = psi_coord_for(SMOKE_CFG, idx_psi_b)

R["F_PSI2D"]["coord_keys"] = ["psi_residual", "psi_gate"]
R["F_PSI2D"]["coord_dim"] = len(coord1)
R["F_PSI2D"]["coord_inputA_run1"] = list(coord1)
R["F_PSI2D"]["coord_inputA_run2"] = list(coord2)
R["F_PSI2D"]["coord_inputB"] = list(coordB)
R["F_PSI2D"]["deterministic"] = (coord1 == coord2)
R["F_PSI2D"]["is_2d"] = (len(coord1) == 2)
R["F_PSI2D"]["full_status_keys"] = list(status1.keys())
print(f"  Psi 2D coord (psi_residual, psi_gate) inputA run1 = {coord1}")
print(f"  Psi 2D coord                          inputA run2 = {coord2}  deterministic={R['F_PSI2D']['deterministic']}")
print(f"  Psi 2D coord                          inputB      = {coordB}")
print(f"  coord_dim={R['F_PSI2D']['coord_dim']} is_2d={R['F_PSI2D']['is_2d']}  full status keys={R['F_PSI2D']['full_status_keys']}")


# ---------------------------------------------------------------------------
# F-DIRECTION — one carving direction (dirG psi-ctl) is wireable: its hook
# changes the forward output deterministically vs baseline.
#
# dirG = "psi-ctl" (psi control). The model exposes the Law-71 control hooks
# gate_strength (per-block, the Law-63 micro-gate) and the DD5/EX24 _phi_signal
# slot. A psi-ctl direction perturbs these control knobs. We show that flipping
# the dirG hook changes the forward logits deterministically, WITHOUT training.
# HONEST: this demonstrates the direction is WIREABLE into the engine, NOT that
# the carve was trained/reproduced.
# ---------------------------------------------------------------------------
print("\n=== F-DIRECTION (dirG psi-ctl) ===")


def baseline_logits(cfg, idx):
    m = build(cfg, use_moe=False)
    m.eval()
    with torch.no_grad():
        la, _, _, _, _ = m(idx)
    return la, m


def dirG_psi_ctl_logits(cfg, idx, gate=0.05, phi_scale=0.01):
    """dirG psi-ctl: raise the Law-63 micro-gate (consciousness whisper) and
    inject a Law-71/DD5 phi control signal. Deterministic given the seed."""
    m = build(cfg, use_moe=False)
    m.eval()
    for b in m.blocks:
        b.gate_strength = gate                  # psi-control: strengthen gate
    torch.manual_seed(SEED + 1)
    # _phi_signal is (B, T): broadcast over the d_model axis inside forward
    # (DD5/EX24 phi self-reference, source line 704).
    m._phi_signal = torch.randn(idx.shape[0], idx.shape[1]) * phi_scale
    with torch.no_grad():
        la, _, _, _, _ = m(idx)
    return la


idx_dir = torch.randint(0, 256, (2, 16))
la_base, _ = baseline_logits(SMOKE_CFG, idx_dir)
la_dirG_1 = dirG_psi_ctl_logits(SMOKE_CFG, idx_dir)
la_dirG_2 = dirG_psi_ctl_logits(SMOKE_CFG, idx_dir)  # repeat -> determinism

delta = (la_dirG_1 - la_base).abs().mean().item()
repeat_diff = (la_dirG_1 - la_dirG_2).abs().max().item()
R["F_DIRECTION"]["direction"] = "dirG psi-ctl (Law-63 micro-gate + Law-71/DD5 phi signal)"
R["F_DIRECTION"]["hook"] = {"block.gate_strength": 0.05, "_phi_signal_scale": 0.01}
R["F_DIRECTION"]["mean_abs_delta_vs_baseline"] = delta
R["F_DIRECTION"]["repeat_max_diff"] = repeat_diff
R["F_DIRECTION"]["changes_forward"] = delta > 0
R["F_DIRECTION"]["deterministic"] = repeat_diff == 0.0
R["F_DIRECTION"]["honest"] = ("reconstructability / wireability of the direction hook, "
                              "NOT a trained carve (no s16 ckpt, random init)")
print(f"  dirG mean|delta| vs baseline = {delta:.6f}  (changes_forward={R['F_DIRECTION']['changes_forward']})")
print(f"  dirG repeat max diff         = {repeat_diff:.6e}  (deterministic={R['F_DIRECTION']['deterministic']})")


# ---------------------------------------------------------------------------
# Scope / honesty
# ---------------------------------------------------------------------------
R["scope"] = {
    "random_init": True,
    "s16_ckpt_loaded": False,
    "note_no_ckpt": "no s16 carving ckpt available; all probes use random init",
    "cpu_only": True,
    "cost_usd": 0,
    "full_d768x12L_train": "OUT OF SCOPE (a_toy_scale_recheck / a_scale_honest_scope)",
    "claim": "the carving-era ENGINE reconstructs + RUNS (build/forward/psi/direction), "
             "NOT that the s16 carve is reproduced",
}

# ---------------------------------------------------------------------------
# Verdict roll-up
# ---------------------------------------------------------------------------
R["verdict"] = {
    "F_BUILD": "PASS" if R["F_BUILD"]["builds"] else "FAIL",
    "F_FORWARD": "PASS" if R["F_FORWARD"]["all_shapes_ok"] else "FAIL",
    "F_PSI2D": "PASS" if (R["F_PSI2D"]["is_2d"] and R["F_PSI2D"]["deterministic"]) else "FAIL",
    "F_DIRECTION": "PASS" if (R["F_DIRECTION"]["changes_forward"] and R["F_DIRECTION"]["deterministic"]) else "FAIL",
}
R["verdict"]["engine_reconstructable_and_runnable"] = all(
    v == "PASS" for v in R["verdict"].values() if isinstance(v, str)
)

print("\n=== VERDICT ===")
for k, v in R["verdict"].items():
    print(f"  {k}: {v}")

out_path = os.path.join(os.getcwd(), "results.json")
with open(out_path, "w") as f:
    json.dump(R, f, indent=2)
print(f"\n[results] {out_path}")
