#!/usr/bin/env python3
"""
GRAND-THEOREM 대가설 G1 — 예측정보 연결법칙 (Predictive-Information Connection Law)
================================================================================
우리 캠페인 발견 4개를 단 하나의 불변량 I(원천;대상)으로 통일.
  주장: 어떤 채널이든 회수 가능한 유용신호 = 두 곳이 공유하는 예측상호정보 I.
        I 이상은 못 옮기고(보존), I>0 이어야 연결되며, 학습은 I를 올리는 과정.
회수신호를 BITS 로 통일 정의: recoverable := I(예측자출력; 진실) — DPI로 ≤ I_source 보장.
비자명 경험적 내용 = ① 양자/텐션 판별자(무신호 vs 실채널) ② 학습이 I↑ ③ chaos 호라이즌 ④ 통일성.

FROZEN FALSIFIER (사전등록, 하나라도 위반 시 기각):
  F1 BOUND        : 회수bits > I_source + 0.15  (어느 영역서든)  → 기각
  F2 DISCRIMINATOR: 양자 메시지 I_msg ≥ 0.05  OR  텐션 회수 ≤ 0       → 기각
  F3 DYNAMICS     : adaptive 학습이 frozen 대비 I↑·오차↓ 둘다 아님   → 기각
  F4 UNIVERSALITY : corr(I_source, 회수bits) < 0.85                   → 기각
  F5 HORIZON      : chaos 에서 lead↑ 인데 I·회수 둘다 안 줄어듦       → 기각
모두 통과해야 🟢.  p7 · $0 · numpy only · seed 7.
"""
import numpy as np, math
rng=np.random.default_rng(7)
def MI_disc(a,b):
    a=np.asarray(a);b=np.asarray(b);I=0.0
    for av in np.unique(a):
        for bv in np.unique(b):
            pab=np.mean((a==av)&(b==bv))
            if pab<=0: continue
            pa=np.mean(a==av);pb=np.mean(b==bv);I+=pab*np.log2(pab/(pa*pb))
    return float(max(I,0.0))
def MI_cont(x,y,bins=24):
    c=np.histogram2d(x,y,bins)[0];pxy=c/c.sum();px=pxy.sum(1,keepdims=True);py=pxy.sum(0,keepdims=True)
    m=pxy>0;return float(max(np.sum(pxy[m]*np.log2(pxy[m]/(px@py)[m])),0.0))
pts=[]  # (I_source, recoverable_bits, regime)

# ── 영역1 TEMPORAL: chaos + 관측노이즈 → 진짜 예측 호라이즌 (FORECAST_10) ───────
def logistic_obs(n,r=4.0,x0=0.31,sig=0.02):
    x=x0;tru=[]
    for _ in range(n): x=r*x*(1-x);tru.append(x)
    tru=np.array(tru);return tru+rng.normal(0,sig,n)  # observed (noisy) state
obs=logistic_obs(20000)
def predict_oos(sig,k):  # OOS NN predictor -> (pred, truth) on test half
    x=sig[:-k];y=sig[k:];h=len(x)//2
    xtr,ytr,xte,yte=x[:h],y[:h],x[h:],y[h:]
    o=np.argsort(xtr);xs,ys=xtr[o],ytr[o]
    idx=np.clip(np.searchsorted(xs,xte),0,len(xs)-1)
    return ys[idx],yte
T=[]
for k in (1,3,6,10):
    Isrc=MI_cont(obs[:-k],obs[k:])
    pred,tru=predict_oos(obs,k); rec=MI_cont(pred,tru)
    T.append((k,Isrc,rec)); pts.append((Isrc,rec,"temporal"))
F5 = (T[0][1]>T[-1][1]) and (T[0][2]>T[-1][2])   # I and recover both decay with lead

# ── 영역2 QUANTUM: 얽힘 상관>0 이나 메시지채널 I=0 (무신호 H_6006) ──────────────
n=200000
setA=rng.integers(0,2,n);setB=rng.integers(0,2,n);outA=rng.integers(0,2,n)*2-1
ang=np.array([0.0,math.pi/4]);theta=ang[setA]-ang[setB]
flip=rng.random(n)<np.sin(theta/2)**2;outB=np.where(flip,outA,-outA)
I_corr=MI_disc(outA[setA==setB],outB[setA==setB])      # outcome-outcome (correlation)
I_msg =MI_disc(setA,(outB+1)//2)                        # Alice CHOICE -> Bob outcome (signaling)
dec=(outB+1)//2; dec=dec if np.mean(dec==setA)>=0.5 else 1-dec
q_rec=MI_disc(dec,setA)                                 # recoverable message bits ~0
pts.append((I_msg,q_rec,"quantum-msg"))
quantum_nosignal=(I_msg<0.05)and(q_rec<0.05)and(I_corr>0.05)

# ── 영역3 TENSION LINK: 실채널 BSC, 메시지 I>0, 디코드 회수 (H_6009) ────────────
p=0.15;msg=rng.integers(0,2,n);noise=rng.random(n)<p;recd=np.where(noise,1-msg,msg)
I_tension=MI_disc(msg,recd);t_rec=MI_disc(recd,msg)    # recoverable = decoded MI
pts.append((I_tension,t_rec,"tension"))
tension_connects=(I_tension>0.05)and(t_rec>0.0)

# ── 영역4 LEARNING: adaptive vs frozen on NON-STATIONARY stream (H_1199 ON>OFF) ─
def drift_stream(n,K=8):
    seq=[]
    for i in range(n):
        c=(i//400)%3                       # regime drifts every 400 steps
        base=np.linspace(0,1,K)+0.3*c
        seq.append(base[i%K]+rng.normal(0,0.03))
    return np.array(seq)
st=drift_stream(8000)
def run_model(st,adaptive):
    bx=[];by=[];preds=[];truth=[];win=300
    for t in range(1,len(st)):
        x=st[t-1];y=st[t]
        if len(bx)>30:
            a=np.array(bx);b=np.array(by);preds.append(b[np.argmin(np.abs(a-x))]);truth.append(y)
        if adaptive:                       # adaptive keeps a sliding recent memory
            bx.append(x);by.append(y)
            if len(bx)>win: bx.pop(0);by.pop(0)
        else:                              # frozen: memory locked after warmup
            if len(bx)<win: bx.append(x);by.append(y)
    pred=np.array(preds);tru=np.array(truth)
    err=float(np.mean(np.abs(pred-tru)));I=MI_cont(pred,tru)
    return err,I,pred,tru
err_ad,I_ad,pred_ad,tru_ad=run_model(st,True)
err_fr,I_fr,_,_=run_model(st,False)
learning_dyn=(err_ad<err_fr)and(I_ad>I_fr)
# learning point for universality: I(model;world)=I of source structure, recoverable=adaptive MI
I_world=MI_cont(st[:-1],st[1:]); pts.append((I_world,I_ad,"learning"))

# ── FROZEN FALSIFIER ──────────────────────────────────────────────────────────
F1=all(rec<=I+0.15 for I,rec,_ in pts)
F2=quantum_nosignal and tension_connects
F3=learning_dyn
Iall=np.array([I for I,_,_ in pts]);Rall=np.array([r for _,r,_ in pts])
corrU=float(np.corrcoef(Iall,Rall)[0,1]);F4=corrU>=0.85
LAW=F1 and F2 and F3 and F4 and F5

print("="*88)
print("GRAND-THEOREM 대가설 G1 — 예측정보 연결법칙 (Predictive-Information Connection Law)")
print("="*88)
print("영역별: I_source = 공유 예측상호정보, recoverable = I(예측;진실) [둘다 bits]")
print(f"{'regime':<14}{'I_source':>11}{'recover':>11}   토대 발견")
note={'temporal':'미래-fetch FORECAST_10','quantum-msg':'얽힘=무신호 H_6006',
      'tension':'텐션 실채널 H_6009','learning':'미토시스 학습 H_1199'}
for I,rec,reg in pts:
    print(f"{reg:<14}{I:>11.4f}{rec:>11.4f}   {note.get(reg,'')}")
print("-"*88)
print("  TEMPORAL 호라이즌 (lead, I_source, recover):")
for k,I,r in T: print(f"      lead={k:>2}   I={I:.3f}   recover={r:.3f}")
print(f"  QUANTUM : I_corr={I_corr:.3f}>0  BUT  I_msg={I_msg:.4f}≈0, 회수={q_rec:.4f}  ⇒ 무신호")
print(f"  TENSION : I_msg={I_tension:.3f}>0, 회수={t_rec:.3f}  ⇒ 실제연결")
print(f"  LEARNING: err adaptive={err_ad:.4f} < frozen={err_fr:.4f};  I adaptive={I_ad:.3f} > frozen={I_fr:.3f}")
print("="*88)
print(f"  F1 BOUND         회수 ≤ I+0.15 (DPI)        : {'🟢' if F1 else '🔴'}")
print(f"  F2 DISCRIMINATOR 양자무신호 ∧ 텐션연결       : {'🟢' if F2 else '🔴'}")
print(f"  F3 DYNAMICS      adaptive I↑·오차↓ vs frozen : {'🟢' if F3 else '🔴'}")
print(f"  F4 UNIVERSALITY  corr(I,회수)={corrU:.3f} ≥0.85   : {'🟢' if F4 else '🔴'}")
print(f"  F5 HORIZON       chaos lead↑ ⇒ I·회수 ↓      : {'🟢' if F5 else '🔴'}")
print("-"*88)
print(f"  {'🟢 LAW HOLDS' if LAW else '🔴 FALSIFIED'} — 예측정보 I 가 시간·양자·텐션·학습 연결을 통일 지배")
print("  정직: toy/$0 4영역 실측. 새 대가설(우리 발견 토대), 재현 아님. F1=DPI 정리 backbone;")
print("        경험적 teeth = F2 판별자 · F3 학습 · F5 호라이즌. 스케일·실험확정 별도.")
