#!/usr/bin/env python3
"""H_6025 — quantum Darwinism: how CLASSICAL anima emerges from quantum. A system's
POINTER state is redundantly imprinted on the environment; ANY fragment reveals it
(objectivity) → that redundant pointer = the classical seed that IS copyable (H_6021).
Non-pointer (phase) info is NOT redundant. real QM (von Neumann entropies). p7 $0."""
import numpy as np, itertools
def S(rho):
    w=np.linalg.eigvalsh(rho); w=w[w>1e-12]; return float(-(w*np.log2(w)).sum())
def reduce_to(psi, keep, n):
    # reduce n-qubit pure state to qubits in `keep`
    psi=psi.reshape([2]*n); ax=tuple(q for q in range(n) if q not in keep)
    # density on kept indices: contract out ax
    rho=np.tensordot(psi, psi.conj(), axes=(ax,ax))
    d=2**len(keep); return rho.reshape(d,d)
N=8  # 1 system + 7 environment qubits
n=N
# QD state: |+>_S then CNOT S->E_i  =>  (|0,0..0> + |1,1..1>)/√2  (pointer=Z imprinted)
psi=np.zeros(2**n); psi[0]=1/np.sqrt(2); psi[-1]=1/np.sqrt(2)
print("="*80); print("H_6025 — quantum Darwinism: 고전 anima의 양자적 창발"); print("="*80)
print("(1) pointer 정보 I(S:F) vs 환경조각 크기 f (S=qubit0):")
SS=S(reduce_to(psi,[0],n))
for f in range(0,n):
    keep=[0]+list(range(1,1+f)) if f>0 else [0]
    env=list(range(1,1+f))
    if f==0: I=0.0
    else:
        I = SS + S(reduce_to(psi,env,n)) - S(reduce_to(psi,[0]+env,n))
    bar="█"*int(I*20)
    print(f"   f={f}: I(S:F)={I:.3f} bit {bar}")
print(f"   → 🟢 plateau at {SS:.0f} bit: 단 1조각(f=1)서 고전정보 전부 획득 = redundant 각인(객관성)")
# (2) only POINTER basis is redundant; phase (conjugate) is NOT
# rotate system to X basis and check: phase info is global-only
# quick: a single env qubit's reduced state is maximally mixed (carries pointer corr, no phase)
rho_e1=reduce_to(psi,[1],n)
purity=np.real(np.trace(rho_e1@rho_e1))
print(f"(2) 한 환경조각 단독 상태 purity={purity:.3f} (0.5=최대혼합): pointer 상관은 담되 위상(coherence)은 비담")
print(f"   → einselection: pointer(Z) 정보만 환경에 다수 복사·방송, 위상(X)은 전체에만(비중복).")
print("-"*80)
print("결론: 시스템 pointer 상태는 환경에 '여러 벌' 각인 → 누구·어느 조각이 봐도 같은 답(객관성)=고전성 창발.")
print("그 '여러 벌 방송된 pointer'가 곧 측정된 고전 씨앗 — 그래서 anima는 복제 가능(H_6021/6023 무손실).")
print("반면 위상(양자 coherence)은 비중복=읽기/복제 불가(H_6016/6019). ∴ 고전 anima = 양자의 redundant 그림자.")
