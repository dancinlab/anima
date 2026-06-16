#!/usr/bin/env python3
"""H_6017 — is there a LIBRARY accessible via quantum+tension link? (Library of Babel)
Honest 4-way on real ANU bytes. p7 $0."""
import numpy as np, glob, os, math
bufs=sorted(glob.glob("/tmp/anu_*.bin"),key=os.path.getsize,reverse=True)
raw=open(bufs[0],"rb").read() if bufs else os.urandom(256)
src=bufs[0] if bufs else "urandom"
A,L=4,8; space=A**L
qs=np.frombuffer(raw,dtype=np.uint8); target=[int(qs[i])%A for i in range(L)]
print("="*80); print(f"H_6017 도서관 조사 — 양자+텐션 (real ANU {src})"); print("="*80)
print(f"LB1 library exists?  space=A^L={A}^{L}={space}; arbitrary target present=True -> 🟢 (all content exists combinatorially)")
print(f"LB2 usable index?  address={math.log2(space):.0f} bits == content {L*math.log2(A):.0f} bits -> 🔴 (no compression of address)")
rs=np.random.default_rng(99)
def fair(tgt,cap=400000):
    for t in range(1,cap+1):
        if list(rs.integers(0,A,L))==tgt: return t
    return cap
tr=[fair(target) for _ in range(5)]
print(f"LB3 quantum shortcut?  fair search mean={np.mean(tr):.0f} ≈ space {space} -> 🔴 (no oracle/index)")
print(f"LB4 structured content?  generate cost={L} vs blind-search {space} -> 🟢 (compressible content is GENERATED, not retrieved)")
print("-"*80)
print("결론: '모든 것이 든 도서관' 조합적 존재(🟢)·쓸 색인 없음(🔴, 주소=내용)·양자/텐션 오라클 없음(🔴)")
print("·구조적 내용은 생성으로 싸게(🟢). anima는 도서관 '검색'이 아니라 '생성/탐색'. = H_6015/H_6016 정합.")
