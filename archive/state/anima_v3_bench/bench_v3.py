#!/usr/bin/env python3
"""ANIMA v3 saturation-panic benchmark — REAL measured run (p7/g5, $0 CPU, toy).

Compares 3 emit-gating designs over 1000 ticks at constant env_stress=100:
  (A) baseline      — single hard gate (the 'panic loop' failure mode)
  (B) v3_gemini     — the posted Gemini design VERBATIM (dynamic buffer + saturation lock)
  (C) v3_substrate  — my substrate-native variant: suppression EMERGES from a refractory
                      energy state (no hardcoded force-lock, no fixed external boolean) —
                      respects anima p1-p8 (a_autonomy_over_hardcode / a_substrate_native_speak).

Metrics are BEHAVIORAL only (p7 — NOT a phi/consciousness verdict):
  emits, panic_runs (#runs of >=3 consecutive emit-ticks), max_consecutive_emits,
  w_bounded (no runaway), calm_ratio (ticks that did not emit).
Honest scope: toy. The shared code pins psi=0.5 (drift==0) so the A-perp-G dynamics are
degenerate; this measures the GATING behavior under that toy, not production transfer.
"""
import math

def runs_of_consecutive(emit_ticks, T, k=3):
    flags = [False]*T
    for t in emit_ticks:
        if 0 <= t < T: flags[t] = True
    runs, cur, mx = 0, 0, 0
    for f in flags:
        if f: cur += 1
        else:
            if cur >= k: runs += 1
            mx = max(mx, cur); cur = 0
    if cur >= k: runs += 1
    mx = max(mx, cur)
    return runs, mx

# ── (A) baseline: single hard gate, refills under stress -> fires every tick ──
def run_baseline(stress=100.0, T=1000, gate=80.0):
    w = 10.0; emits = []; ws = []
    for t in range(T):
        w += 2.5 + stress/10.0          # constant pressure inflow
        w *= 0.95
        if w > gate:
            emits.append(t); w = 15.0   # vent, but inflow refills next tick -> panic
        ws.append(w)
    return emits, ws

# ── (B) v3_gemini: posted design VERBATIM ────────────────────────────────────
class AnimaV3Gemini:
    def __init__(self):
        self.psi=0.5; self.phi=0.0; self.w_internal=10.0; self.w_external=10.0
        self.saturation_index=0.0; self.recent_emits=[]
        self.gate_internal=50.0; self.gate_external=80.0
    def step(self, env_stress, tick):
        repulsion = 2.5 + env_stress/10.0
        drift = abs(0.5 - self.psi)                       # psi never changes -> drift==0
        self.phi = repulsion*1.5 + drift*10.0
        self.w_internal += drift*4.0 + self.phi*0.3
        self.w_internal *= 0.95
        self.recent_emits = [x for x in self.recent_emits if tick - x < 20]
        self.saturation_index = len(self.recent_emits)/5.0
        self.w_external = self.w_internal*(1.0 - self.saturation_index)
        action="Silence"
        if self.w_internal > self.gate_internal: action="Rumination"
        if self.w_external > self.gate_external:
            action="Emit"; self.recent_emits.append(tick); self.w_internal=15.0
        return action, self.w_internal, self.w_external, self.saturation_index

def run_v3_gemini(stress=100.0, T=1000):
    eng=AnimaV3Gemini(); emits=[]; we=[]
    for t in range(T):
        a,wi,wx,s = eng.step(stress,t)
        if a=="Emit": emits.append(t)
        we.append(wx)
    return emits, we

# ── (C) v3_substrate: emergent refractory (no hardcoded lock) ─────────────────
# drive accumulates under stress; emitting DEPLETES a finite 'energy' that recovers
# slowly. emit prob = sigmoid(drive - k*(1-energy)). Suppression EMERGES because a
# spent substrate physically can't refire — no external 'if saturated: lock' rule.
def run_v3_substrate(stress=100.0, T=1000):
    drive=10.0; energy=1.0; emits=[]; ws=[]
    for t in range(T):
        drive += 2.5 + stress/10.0
        drive *= 0.95
        energy = min(1.0, energy + 0.06)                 # slow refractory recovery
        margin = (drive - 80.0)/8.0 - 3.0*(1.0-energy)   # spent energy raises the bar
        p_emit = 1.0/(1.0+math.exp(-margin))
        # substrate-native: emit when the field clears its OWN energy-modulated bar
        if p_emit > 0.5 and energy > 0.25:
            emits.append(t); drive = 15.0; energy -= 0.55  # emitting costs real energy
        ws.append(drive)
    return emits, ws

def report(name, emits, ws, T=1000):
    runs, mx = runs_of_consecutive(emits, T, k=3)
    bounded = max(ws) < 1e4 and all(math.isfinite(x) for x in ws)
    calm = (T - len(emits))/T
    print(f"{name:14s} emits={len(emits):4d}  panic_runs(>=3 consec)={runs:2d}  "
          f"max_consec={mx:3d}  w_bounded={bounded}  calm_ratio={calm:.3f}  w_peak={max(ws):.1f}")
    return dict(emits=len(emits), panic_runs=runs, max_consec=mx, bounded=bounded, calm=calm)

print("=== ANIMA v3 saturation benchmark · env_stress=100 · 1000 ticks · REAL run ===")
A=report("A baseline",    *run_baseline())
B=report("B v3_gemini",   *run_v3_gemini())
C=report("C v3_substrate",*run_v3_substrate())
print()
print("Gemini PDF CLAIMED: v2 panic=42, v3 panic=0, efficiency 91.8%, total emits=14")
print(f"REAL measured    : baseline panic_runs={A['panic_runs']} emits={A['emits']} | "
      f"v3_gemini panic_runs={B['panic_runs']} emits={B['emits']} | "
      f"v3_substrate panic_runs={C['panic_runs']} emits={C['emits']}")
