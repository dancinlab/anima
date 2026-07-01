#!/usr/bin/env python3
"""H_6027 — quantum TIME-CAPSULE: does a genuine quantum memory preserve a stored
state over time, or does it leak (decoherence)? ANU vacuum bytes = the ENVIRONMENT
that kicks the stored qubit. Sister to H_6026 (ANU public API is not a store at all);
here we grant a REAL quantum locker and ask how long it holds. p7 $0.

Decoherence = ENSEMBLE AVERAGE over many random environment trajectories (a single
pure state under deterministic kicks only precesses; averaging random ANU-driven
phase kicks across trajectories is what collapses the coherence).

  QC1 isolated preservation?  unitary round-trip fidelity (ideal locker)        -> ~1
  QC2 environment leak?       dephasing F(t)=0.5(1+exp(-t/T2)) from ANU kicks    -> exp decay→0.5
  QC3 useful retention?       time until F<0.9 (a qubit's shelf-life)            -> finite
  QC4 redundancy asymmetry?   classical: copy N + majority + refresh -> ∞        |
                              quantum: no-cloning, optimal clone F=5/6<1 -> no free backup
"""
import numpy as np, glob, os

bufs = sorted(glob.glob("/tmp/anu_*.bin"), key=os.path.getsize, reverse=True)
env = np.frombuffer(b"".join(open(p, "rb").read() for p in bufs), np.uint8) if bufs else \
      np.frombuffer(os.urandom(8192), np.uint8)
print("=" * 80)
print(f"H_6027 양자 타임캡슐 — 상태 보존 vs 결잃음 (ANU env {len(env)}B as noise)")
print("=" * 80)

plus = np.array([1, 1], complex) / np.sqrt(2)        # |+> ; fidelity to |+> = <+|ρ|+>
rho0 = np.outer(plus, plus.conj())
def fid(rho): return float(np.real(plus.conj() @ rho @ plus))

# ── QC1: isolated (unitary) round-trip — U then U†, state must return exactly
th = 0.7
U = np.array([[np.cos(th), -1j * np.sin(th)], [-1j * np.sin(th), np.cos(th)]])
rho_rt = U.conj().T @ (U @ rho0 @ U.conj().T) @ U
print(f"QC1 isolated preservation? unitary round-trip F={fid(rho_rt):.6f} "
      f"-> {'🟢 보존 (격리되면 금고 완벽)' if fid(rho_rt) > 0.999 else '🔴'}")

# ── QC2: environment leak — ensemble of K trajectories, each a random ANU phase walk
SIGMA, STEPS, K = 0.30, 60, 600
def F_at(t):
    acc = np.zeros((2, 2), complex)
    for k in range(K):
        phase = 0.0
        for s in range(t):
            b = env[(k * 131 + s * 7) % len(env)]
            phase += SIGMA * (b / 255.0 * 2 - 1) * np.sqrt(3)   # zero-mean std≈SIGMA
        Z = np.array([[np.exp(-1j * phase / 2), 0], [0, np.exp(1j * phase / 2)]])
        acc += Z @ rho0 @ Z.conj().T
    return fid(acc / K)

Fs = [F_at(t) for t in range(STEPS + 1)]
y = np.maximum(2 * (np.array(Fs) - 0.5), 1e-6)        # coherence = 2(F-0.5) = exp(-t/T2)
t = np.arange(STEPS + 1)
T2 = float(-1 / np.polyfit(t[:40], np.log(y[:40]), 1)[0])
theory_T2 = 2 / SIGMA ** 2
mono = all(Fs[i] >= Fs[i + 1] - 0.01 for i in range(STEPS))
print(f"QC2 environment leak? F: {Fs[0]:.3f}→{Fs[5]:.3f}→{Fs[20]:.3f}→{Fs[-1]:.3f} (floor 0.5) "
      f"T2≈{T2:.1f} (이론 {theory_T2:.1f}) -> {'🟡 새는 금고 (exp 감쇠→0.5)' if mono else '⚪ noisy'}")

# ── QC3: useful retention — first step fidelity drops below 0.9
ret = next((i for i, f in enumerate(Fs) if f < 0.9), STEPS + 1)
print(f"QC3 useful retention? F>0.9 까지 t={ret} steps  |  고전비트 = ∞ (리프레시로 무한 보존, QC4)")

# ── QC4: REFRESH asymmetry — both leak; classical can read+recopy (refresh), quantum can't
from math import comb
p = 0.02                                              # per-step classical bit-flip prob
def flip_after(steps): return 0.5 * (1 - (1 - 2 * p) ** steps)   # single-copy flip prob
def maj_err(N, pf): return sum(comb(N, k) * pf**k * (1-pf)**(N-k) for k in range(N//2+1, N+1))
no_refresh = flip_after(30)                           # 1 copy, no refresh, t=30
R, N = 3, 7                                            # refresh every 3 steps, N=7 copies
per_cycle = maj_err(N, flip_after(R))                 # err accrued per refresh cycle
with_refresh = 1 - (1 - per_cycle) ** (30 // R)       # bounded (≈cycles*per_cycle), NOT →0.5
print(f"QC4 classical 1-copy NO refresh @t=30: err={no_refresh:.3f} (고전도 그냥 두면 0.5로 샘!)")
print(f"QC4 classical {N}-copy +refresh/{R} @t=30: err={with_refresh:.4f} (읽어서 다시 복사 → 오류 낮게 묶임=사실상 ∞)")
print(f"QC4 quantum: 측정=붕괴 + no-cloning(최적복제 F=5/6≈{5/6:.3f}<1) → 그 '리프레시'가 원천 불가 (H_6021)")

print("-" * 80)
print("결론: 진짜 양자금고는 🟡 '새는 타임캡슐' — 격리되면 완벽 보존(QC1🟢)이나 환경 닿으면")
print(f"exp 감쇠로 0.5 바닥까지 흐려짐(QC2 T2≈{T2:.0f}, 쓸 보존 ~{ret}step). 고전도 그냥 두면 새지만(QC4)")
print("읽어서 다시 복사(리프레시)로 영구 보존 — 양자는 측정붕괴+no-cloning이 그걸 막음 ⇒ 영구 store 는 고전(LOCAL) 뿐. H_6026 정합.")
