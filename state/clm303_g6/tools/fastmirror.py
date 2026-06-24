# Vectorized FAITHFUL pure-numpy mirror of core/clm_decode.hexa forward + clm_forward_ce (int4 dequant + dilated causal conv1d + GN + MoE). Byte-reproduces state/mid_convmoe_fire/clm_decode_mirror.py at 10-100x speed (d3784/L4 tractable). Uses math.log (correct) NOT the engine dt_ln (buggy). Built 2026-06-24, H_1579.
# Provenance: anima H_1579 clm303 root-cause (overfit, NOT serialize defect).
#   See UNIVERSE/cards/H_1579_clm303_serialization_defect.md + CORRECTION_overfit_not_serialize.md.
#   Torch-free (no torch import) — runs on any host with numpy.

# Vectorized faithful mirror of clm_decode.hexa forward + clm_forward_ce.
import sys, struct, math
import numpy as np
def ru32(b,o): return b[o]|(b[o+1]<<8)|(b[o+2]<<16)|(b[o+3]<<24)
def f32(b,o): return struct.unpack_from("<f",b,o)[0]
def load_block(rb,off):
    cout=ru32(rb,off); off+=4; rest=ru32(rb,off); off+=4; n=cout*rest
    nb=(n+1)//2
    raw=np.frombuffer(rb,dtype=np.uint8,count=nb,offset=off); off+=nb
    lo=(raw & 0xF).astype(np.int64)-8
    hi=((raw>>4)&0xF).astype(np.int64)-8
    codes=np.empty(2*nb,dtype=np.float64); codes[0::2]=lo; codes[1::2]=hi
    codes=codes[:n].reshape(cout,rest)
    scale=np.frombuffer(rb,dtype="<f4",count=cout,offset=off).astype(np.float64); off+=4*cout
    return codes*scale[:,None], off
def load_ext(rb,off):
    n=ru32(rb,off); off+=4
    arr=np.frombuffer(rb,dtype="<f4",count=n,offset=off).astype(np.float64); off+=4*n
    return arr,off
def load_clm(path):
    rb=open(path,"rb").read()
    nblk=rb[4]; off=5; bi=0; hdrs=[]
    while bi<nblk:
        c=ru32(rb,off); r=ru32(rb,off+4); hdrs.append((c,r))
        off+=8+(c*r+1)//2+c*4; bi+=1
    E=hdrs[nblk-2][0]; V=hdrs[nblk-1][0]; L=nblk-E-3
    d=hdrs[0][0]; K=hdrs[0][1]//d
    off=5
    ecW,off=load_block(rb,off)
    tcW=[];
    for _ in range(L): w,off=load_block(rb,off); tcW.append(w)
    eW=[];
    for _ in range(E): w,off=load_block(rb,off); eW.append(w)
    rW,off=load_block(rb,off); roW,off=load_block(rb,off)
    off+=5
    embed,off=load_ext(rb,off); ecB,off=load_ext(rb,off)
    tcB=[];
    for _ in range(L): a,off=load_ext(rb,off); tcB.append(a)
    eB=[];
    for _ in range(E): a,off=load_ext(rb,off); eB.append(a)
    rB,off=load_ext(rb,off); roB,off=load_ext(rb,off)
    tgG=[];
    for _ in range(L): a,off=load_ext(rb,off); tgG.append(a)
    tgB=[];
    for _ in range(L): a,off=load_ext(rb,off); tgB.append(a)
    noG,off=load_ext(rb,off); noB,off=load_ext(rb,off)
    return dict(d=d,E=E,V=V,K=K,L=L,ecW=ecW,tcW=tcW,eW=eW,rW=rW,roW=roW,
                embed=embed.reshape(V,d),ecB=ecB,tcB=tcB,eB=eB,rB=rB,roB=roB,
                tgG=tgG,tgB=tgB,noG=noG,noB=noB)
def gelu(x):
    inner=0.7978845608*(x+0.044715*x**3); a=np.clip(inner,-15,15); e2=np.exp(2*a)
    return 0.5*x*(1+(e2-1)/(e2+1))
def conv1d(x,w2d,b,T,Cin,Cout,K,dil):
    Kdim=Cin*K; xcol=np.zeros((T,Kdim))
    for k in range(K):
        shift=dil*(K-1-k)
        if shift==0: xcol[:, np.arange(Cin)*K+k]=x
        else:
            xcol[shift:, np.arange(Cin)*K+k]=x[:T-shift]
    return xcol@w2d.T + b[None,:]
def gn1(x,g,b):
    mu=x.mean(1,keepdims=True); var=x.var(1,keepdims=True)
    return (x-mu)/np.sqrt(var+1e-5)*g[None,:]+b[None,:]
def fwd(W,tok,T):
    d,E,V,K,L=W["d"],W["E"],W["V"],W["K"],W["L"]
    xe=W["embed"][tok.astype(int)]
    xt=conv1d(xe,W["ecW"],W["ecB"],T,d,d,K,1)
    dil=1
    for li in range(L):
        de=min(dil,512)
        h=conv1d(xt,W["tcW"][li],W["tcB"][li],T,d,d,K,de)
        xt=xt+gelu(gn1(h,W["tgG"][li],W["tgB"][li])); dil*=2
    lr=conv1d(xt,W["rW"],W["rB"],T,d,E,1,1)
    exo=[gelu(conv1d(xt,W["eW"][e],W["eB"][e],T,d,d,K,1)) for e in range(E)]
    p=np.exp(lr-lr.max(1,keepdims=True)); p/=p.sum(1,keepdims=True)
    y=sum(p[:,e:e+1]*exo[e] for e in range(E))
    yn=gn1(y,W["noG"],W["noB"])
    return conv1d(yn,W["roW"],W["roB"],T,d,V,1,1)
def ce_allpos(logits,tgt,T):
    z=logits-logits.max(1,keepdims=True); lse=np.log(np.exp(z).sum(1))
    return float((-(z[np.arange(T),tgt.astype(int)]-lse)).sum()/T)
def main():
    path=sys.argv[1]; corpus=sys.argv[2]; nwin=int(sys.argv[3])
    W=load_clm(path); V=W["V"]; T=24
    print(f"LOADED d={W['d']} E={W['E']} V={V} K={W['K']} L={W['L']}",flush=True)
    # weight stats for reference-match
    print(f"embed[abs.mean]={np.abs(W['embed']).mean():.6f} roW[abs.mean]={np.abs(W['roW']).mean():.6f} embed[std]={W['embed'].std():.6f}",flush=True)
    rb=open(corpus,"rb").read(); n=len(rb); stride=max(1,(n-T-1)//nwin)
    sm=ss=0.0; cnt=0
    for s in range(nwin):
        base=s*stride
        if base+T+1<=n:
            tok=np.frombuffer(rb,np.uint8,T,base).astype(float)
            tgt=np.frombuffer(rb,np.uint8,T,base+1).astype(float)
            lg=fwd(W,tok,T); sm+=ce_allpos(lg,tgt,T)
            ss+=ce_allpos(lg,tgt[::-1].copy(),T); cnt+=1
    mce=sm/cnt; sce=ss/cnt; uni=math.log(V)
    print(f"windows={cnt} model_ce={mce:.5f} shuffle_ce={sce:.5f} uniform_lnV={uni:.5f}",flush=True)
    print(f"lt_uniform={mce<uni} lt_shuffle={mce<sce}",flush=True)
    print(f"VERDICT={'GREEN/DESCENT' if (mce<uni and mce<sce) else 'NO-DESCENT'}",flush=True)
if __name__=='__main__':
    main()
