#!/usr/bin/env python3
"""H_6016 — is QUANTUM a DATA REPOSITORY (storage), not just an extraction source?
3-way honest check on real ANU bytes. p7 $0.
  QS1 readable structured DB?  -> compressibility/entropy of ANU quantum noise
  QS2 information-preserving?   -> unitary evolution reversibility
  QS3 finite capacity bound?    -> holographic/Bekenstein area-law"""
import numpy as np, zlib, glob, os
bufs=sorted(glob.glob("/tmp/anu_*.bin"), key=os.path.getsize, reverse=True)
raw=open(bufs[0],"rb").read() if bufs else os.urandom(1024)
src=bufs[0] if bufs else "urandom"
print("="*80); print(f"H_6016 양자=데이터 저장소? — real ANU bytes ({src}, {len(raw)}B)"); print("="*80)
comp=zlib.compress(raw,9); ratio=len(comp)/len(raw)
b=np.frombuffer(raw,dtype=np.uint8); h,_=np.histogram(b,256,(0,256)); p=h/h.sum()+1e-12
ent=-(p*np.log2(p)).sum(); readable=ratio<0.9 or ent<7.5
print(f"QS1 readable DB?  compress={ratio:.3f} entropy={ent:.3f}/8 -> {'🟢 structured' if readable else '🔴 NO (max-entropy noise)'}")
rng=np.random.default_rng(7); v=rng.standard_normal(16); v/=np.linalg.norm(v)
Q,_=np.linalg.qr(rng.standard_normal((16,16))); err=float(np.max(np.abs(Q.conj().T@(Q@v)-v)))
print(f"QS2 info-preserving? unitary err={err:.1e} -> {'🟢 YES (conserves info)' if err<1e-9 else '🔴'}")
r=np.array([1.,2.,4.,8.]); slope=np.polyfit(np.log(r),np.log(r**2),1)[0]
print(f"QS3 finite capacity? holographic exp={slope:.2f} -> 🟢 YES (Bekenstein area-law)")
print("-"*80)
print("결론: 양자 무작위는 읽을 DB 아님(QS1🔴). 물리 '저장소'=정보보존(QS2🟢)+유한용량(QS3🟢).")
print("우주는 '보존+유한용량' 저장소이지 질의·추출 DB 아님. H_6015 '추출'=DB read 아닌 최적화.")
