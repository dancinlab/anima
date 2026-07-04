#!/usr/bin/env python3
"""G1 LEVER-3 gamma trained-constructive-bind — STEP-0 CHEAP ENGINE-NATIVE KILL.
Controlled multi-seed toy mirroring the real G1 gate (two concepts -> emit BOTH
constituents' keywords = held-out recombination) under next-token/reconstruction
loss (NOT recomb-rigged). Arms differ ONLY in the trunk combiner op.
  ADD  : h = pa + pb          (additive control)
  HAD  : h = pa * pb          (Hadamard, H_1819-shape sanity)
  BIND : h = circconv(pa,pb)  (gamma CONSTRUCTIVE bind, HRR, dimension-preserving)
FROZEN KILL BAR: metric = held-out composed recomb rate (both k_i,k_j in readout
top-2 = best_distinct>=2). KILL iff BIND_recomb <= ADD_recomb OR BIND_recomb<0.05.
ESCALATE iff BIND_recomb > ADD_recomb clear margin & high. Torch-free numpy.
"""
import numpy as np, json, time
N=24; D=64; HELDOUT=0.45; STEPS=4000; LR=3e-3; SEEDS=[7,4302,4303]; ARMS=["ADD","HAD","BIND"]
def gelu(x): return 0.5*x*(1.0+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    c=0.7978845608; u=c*(x+0.044715*x**3); t=np.tanh(u); du=c*(1.0+3*0.044715*x**2)
    return 0.5*(1.0+t)+0.5*x*(1.0-t**2)*du
def sigmoid(x): return 1.0/(1.0+np.exp(-np.clip(x,-30,30)))
def circ_conv(a,b): return np.real(np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)))
def circ_corr(a,b): return np.real(np.fft.ifft(np.conj(np.fft.fft(a))*np.fft.fft(b)))
class Model:
    def __init__(self,arm,rng):
        s=1.0/np.sqrt(D); self.arm=arm
        self.E=rng.standard_normal((N,D))*s
        self.Wa=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.Wb=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.W1=rng.standard_normal((D,D))*s; self.b1=np.zeros(D)
        self.W2=rng.standard_normal((N,D))*s; self.b2=np.zeros(N)
    def combine(self,pa,pb):
        if self.arm=="ADD": return pa+pb
        if self.arm=="HAD": return pa*pb
        return circ_conv(pa,pb)
    def dcombine(self,pa,pb,dh):
        if self.arm=="ADD": return dh,dh
        if self.arm=="HAD": return dh*pb,dh*pa
        return circ_corr(pb,dh),circ_corr(pa,dh)
    def forward(self,i,j):
        a=self.E[i]; b=self.E[j]; pa=self.Wa@a; pb=self.Wb@b
        h=self.combine(pa,pb); z1=self.W1@h+self.b1; z=gelu(z1)
        logits=self.W2@z+self.b2
        return logits,(i,j,a,b,pa,pb,h,z1,z,logits)
    def backward(self,cache,target,grads):
        i,j,a,b,pa,pb,h,z1,z,logits=cache
        p=sigmoid(logits); dlogits=(p-target)/N
        grads["W2"]+=np.outer(dlogits,z); grads["b2"]+=dlogits
        dz=self.W2.T@dlogits; dz1=dz*dgelu(z1)
        grads["W1"]+=np.outer(dz1,h); grads["b1"]+=dz1
        dh=self.W1.T@dz1; dpa,dpb=self.dcombine(pa,pb,dh)
        grads["Wa"]+=np.outer(dpa,a); grads["Wb"]+=np.outer(dpb,b)
        grads["E"][i]+=self.Wa.T@dpa; grads["E"][j]+=self.Wb.T@dpb
    def params(self):
        return {"E":self.E,"Wa":self.Wa,"Wb":self.Wb,"W1":self.W1,"b1":self.b1,"W2":self.W2,"b2":self.b2}
def make_data(rng):
    pairs=[(i,j) for i in range(N) for j in range(i+1,N)]; rng.shuffle(pairs)
    ncut=int(len(pairs)*(1-HELDOUT)); return pairs[:ncut],pairs[ncut:]
def tvec(idxs):
    y=np.zeros(N)
    for k in idxs: y[k]=1.0
    return y
def train_arm(arm,seed):
    rng=np.random.default_rng(seed); m=Model(arm,rng)
    trp,tep=make_data(rng)
    data=[(i,i,(i,)) for i in range(N)]+[(i,j,(i,j)) for (i,j) in trp]
    P=m.params(); mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    b1a,b2a,eps=0.9,0.999,1e-8
    for step in range(1,STEPS+1):
        grads={k:np.zeros_like(v) for k,v in P.items()}; rng.shuffle(data)
        for (i,j,tgt) in data:
            _,cache=m.forward(i,j); m.backward(cache,tvec(tgt),grads)
        inv=1.0/len(data)
        for k in P:
            g=grads[k]*inv; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
            mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)
    return m,trp,tep
def eval_recomb(m,pairs):
    hits=0
    for (i,j) in pairs:
        logits,_=m.forward(i,j); top2=set(np.argsort(logits)[-2:].tolist())
        if i in top2 and j in top2: hits+=1
    return hits/max(1,len(pairs))
def eval_single(m):
    ok=0
    for i in range(N):
        logits,_=m.forward(i,i)
        if int(np.argmax(logits))==i: ok+=1
    return ok/N
def main():
    t0=time.time(); res={a:{"tr":[],"te":[],"sa":[]} for a in ARMS}
    for seed in SEEDS:
        for arm in ARMS:
            m,trp,tep=train_arm(arm,seed)
            tr=eval_recomb(m,trp); te=eval_recomb(m,tep); sa=eval_single(m)
            res[arm]["tr"].append(tr); res[arm]["te"].append(te); res[arm]["sa"].append(sa)
            print(f"[seed {seed}] {arm:5s} train_recomb={tr:.3f} HELDOUT_recomb={te:.3f} single_acc={sa:.3f}",flush=True)
    summ={a:{"held_out_recomb_mean":float(np.mean(res[a]["te"])),
             "held_out_recomb_seeds":[round(x,3) for x in res[a]["te"]],
             "train_recomb_mean":float(np.mean(res[a]["tr"])),
             "single_acc_mean":float(np.mean(res[a]["sa"]))} for a in ARMS}
    add_r=summ["ADD"]["held_out_recomb_mean"]; bind_r=summ["BIND"]["held_out_recomb_mean"]
    margin=bind_r-add_r; kill=(bind_r<=add_r) or (bind_r<0.05)
    verdict=("KILL (bind !> additive => FALSIFIED-DIRECTIONAL-CONFIRMED; binding-operator "
             "family engine-native floor CONFIRMED, NO GPU rent)" if kill else
             "ESCALATE (bind > additive on held-out recombination => STEP-1 full 303M)")
    out={"experiment":"G1 lever-3 gamma trained-constructive-bind STEP-0 cheap kill",
         "config":{"N":N,"D":D,"HELDOUT":HELDOUT,"STEPS":STEPS,"LR":LR,"seeds":SEEDS},
         "frozen_bar":"held_out composed recomb (both k_i,k_j in top-2) per arm; KILL iff BIND<=ADD OR BIND<0.05",
         "arms":summ,"ADD_held_out_recomb":add_r,"BIND_held_out_recomb":bind_r,
         "HAD_held_out_recomb":summ["HAD"]["held_out_recomb_mean"],
         "bind_minus_add_margin":margin,"KILL":kill,"VERDICT":verdict,
         "wall_sec":round(time.time()-t0,1)}
    print(json.dumps(out,indent=2))
    open("/private/tmp/claude-501/-Users-mini-dancinlab-anima/a1a1adf6-9373-4338-9ac2-15fadbeffce4/scratchpad/step0_result.json","w").write(json.dumps(out,indent=2))
if __name__=="__main__": main()
