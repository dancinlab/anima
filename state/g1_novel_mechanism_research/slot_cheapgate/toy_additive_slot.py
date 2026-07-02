#!/usr/bin/env python3
"""G1 ADDITIVE-SLOT + ENCODER-DECODER CONSISTENCY cheap-gate (deep-research 2026-07-02 finding).
Wiedemer/Lachapelle additive-decoder theory: held-out recombination is PROVABLY guaranteed by an
additive-per-slot decoder (x̂=Σ Dk(zk)) + encoder-decoder consistency, once each slot is learned
in-distribution. H_6164 structural-bind LACKED slot-identifiability + consistency — this adds them.
openQuestion: does CE/MSE learning preserve the slot identifiability the guarantee needs, or destroy it?
Slot-DECOMPOSABLE generative toy (additive superposition), NOT the joint-classification toy.
FROZEN 2026-07-02. tune-to-green forbidden (p7). torch mirror=DIRECTIONAL."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
dev="cuda" if torch.cuda.is_available() else "cpu"

NF, Dobs, Dz = 8, 48, 24     # factors/slot, obs dim, slot latent dim
STEPS, BS, LR = 6000, 256, 2e-3
SEEDS=[7,4302,4303,4304,4305]
HELDOUT_FRAC=0.22
LAM_CONS=1.0

def make(seed):
    g=np.random.default_rng(seed)
    Pa=g.standard_normal((NF,Dobs)).astype('float32')  # ground-truth per-slot generators
    Pb=g.standard_normal((NF,Dobs)).astype('float32')
    combos=[(a,b) for a in range(NF) for b in range(NF)]; g.shuffle(combos)
    nho=round(len(combos)*HELDOUT_FRAC); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    assert {a for a,_ in seen}==set(range(NF)) and {b for _,b in seen}==set(range(NF))
    return Pa,Pb,seen,sorted(held)

def batch(combos,Pa,Pb,rng,n):
    idx=rng.integers(0,len(combos),size=n); A=np.array([combos[i][0] for i in idx]); B=np.array([combos[i][1] for i in idx])
    x=Pa[A]+Pb[B]  # additive superposition = slot-decomposable observation
    return torch.tensor(x,device=dev), torch.tensor(A,device=dev), torch.tensor(B,device=dev)

class AddSlot(nn.Module):
    """encoder x->[za,zb]; additive decoder x̂=Da(za)+Db(zb); + consistency."""
    def __init__(s):
        super().__init__(); H=96
        s.enc=nn.Sequential(nn.Linear(Dobs,H),nn.GELU(),nn.Linear(H,2*Dz))
        s.da=nn.Sequential(nn.Linear(Dz,H),nn.GELU(),nn.Linear(H,Dobs))
        s.db=nn.Sequential(nn.Linear(Dz,H),nn.GELU(),nn.Linear(H,Dobs))
    def encode(s,x): z=s.enc(x); return z[:,:Dz], z[:,Dz:]
    def forward(s,x):
        za,zb=s.encode(x); return s.da(za)+s.db(zb), za, zb

class Mono(nn.Module):
    """monolithic autoencoder: no slot split, no additivity (same-ish capacity)."""
    def __init__(s):
        super().__init__(); H=96
        s.enc=nn.Sequential(nn.Linear(Dobs,H),nn.GELU(),nn.Linear(H,2*Dz))
        s.dec=nn.Sequential(nn.Linear(2*Dz,H),nn.GELU(),nn.Linear(H,Dobs))
    def forward(s,x): z=s.enc(x); return s.dec(z), None, None

def train(seed,arm,Pa,Pb,train_combos):
    torch.manual_seed(seed); np.random.seed(seed); rng=np.random.default_rng(1000+seed)
    net=(AddSlot() if arm=="addslot" else Mono()).to(dev)
    opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        x,_,_=batch(train_combos,Pa,Pb,rng,BS)
        xh,za,zb=net(x); loss=F.mse_loss(xh,x)
        if arm=="addslot":  # encoder-decoder consistency: re-encode reconstruction matches slots
            za2,zb2=net.encode(xh); loss=loss+LAM_CONS*(F.mse_loss(za2,za.detach())+F.mse_loss(zb2,zb.detach()))
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def recon_mse(combos,n=4096):
        x,_,_=batch(combos,Pa,Pb,rng,n)
        with torch.no_grad(): xh=net(x)[0]
        return F.mse_loss(xh,x).item()
    return recon_mse

def main():
    out={"seeds":{}}
    for s in SEEDS:
        Pa,Pb,seen,held=make(s); rec={}
        for arm in ["mono","addslot"]:
            rm=train(s,arm,Pa,Pb,seen)
            rec[arm]={"seen_mse":round(rm(seen),4),"held_mse":round(rm(held),4)}
            rec[arm]["held_over_seen"]=round(rec[arm]["held_mse"]/max(rec[arm]["seen_mse"],1e-6),3)
            print(f"seed={s} {arm}: seen_mse={rec[arm]['seen_mse']} held_mse={rec[arm]['held_mse']} ratio={rec[arm]['held_over_seen']}",flush=True)
        # extrapolation gap: addslot should keep held≈seen (ratio~1), mono should blow up (ratio>>1)
        rec["mono_over_addslot_held"]=round(rec["mono"]["held_mse"]/max(rec["addslot"]["held_mse"],1e-6),3)
        out["seeds"][str(s)]=rec
    per=[]
    for s in SEEDS:
        r=out["seeds"][str(s)]
        per.append({"seed":s,"addslot_ratio":r["addslot"]["held_over_seen"],"mono_ratio":r["mono"]["held_over_seen"],
                    "mono_vs_addslot_held":r["mono_over_addslot_held"]})
    # FROZEN bar: addslot EXTRAPOLATES (held/seen<=1.5) AND beats mono on held-out (mono_held/addslot_held>=2x), >=2/3 seeds
    n_extrap=sum(1 for p in per if p["addslot_ratio"]<=1.5)
    n_beats=sum(1 for p in per if p["mono_vs_addslot_held"]>=2.0)
    # oracle: train-with-held recon should be low for addslot (task solvable)
    oracle_ok=True
    for s in SEEDS:
        Pa,Pb,seen,held=make(s); rm=train(s,"addslot",Pa,Pb,seen+list(held))
        if rm(held)>0.5*out["seeds"][str(s)]["addslot"]["seen_mse"]+1e-3 and rm(held)>0.5: oracle_ok=False
    if n_extrap>=4 and n_beats>=4:
        tier="★★ SLOT-LEVER FOUND — additive-slot+consistency EXTRAPOLATES to held-out recombination where mono fails (G1 lever candidate; anima concept-slot wiring warranted)"
    elif n_extrap>=3 or n_beats>=3:
        tier="🟡 DIRECTIONAL-PARTIAL — additive-slot shows extrapolation edge but not clean >=4/5 (deeper/scale test)"
    else:
        tier="🧱 FLOOR — additive-slot+consistency does NOT extrapolate under learned CE/MSE (slot identifiability destroyed; Lost-in-Latent-Space confirmed for anima trunk)"
    out["verdict"]={"per_seed":per,"n_extrapolate(<=1.5)":n_extrap,"n_beats_mono(>=2x)":n_beats,"oracle_ok":oracle_ok,"tier":tier}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===")
    for p in per: print(p)
    print("n_extrap:",n_extrap,"/5  n_beats_mono:",n_beats,"/5")
    print("TIER:",tier)

if __name__=="__main__": main()
