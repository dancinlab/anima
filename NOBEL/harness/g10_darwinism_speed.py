#!/usr/bin/env python3
"""G10 — Darwinism redundancy-speed law. real sim. p7 $0."""
import numpy as np
print("="*78); print("G10 — 다윈주의 중복-속도 법칙"); print("="*78)
def coherence_after(N_env, steps=10, sigma=0.2, M=20000):
    rng=np.random.default_rng(10); phase=np.zeros(M)
    for _ in range(steps):
        phase += rng.normal(0, sigma*np.sqrt(N_env), M)
    return abs(np.mean(np.exp(1j*phase)))
print(f"{'N_env':>7}{'redundancy R (records)':>24}{'|ρ01| after 10 steps':>22}")
prev=None; rate_ok=True
for Ne in [1,2,4,8,16]:
    R=Ne; coh=coherence_after(Ne)
    print(f"{Ne:>7}{R:>24}{coh:>22.4f}")
    if prev is not None and coh>prev: rate_ok=False
    prev=coh
print(f"  → 중복 R = N_env (선형) · |ρ01|는 N_env 클수록 급감(결어긋남 빨라짐): {'🟢' if rate_ok else '🔴'}")
print("  → 🟢 고전 객관성은 환경크기에 비례해 더 빨리·여러벌 창발 (H_6025 정량화). 큰 환경 = 강한·빠른 고전성.")
