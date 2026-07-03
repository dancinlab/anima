import sys, os, json
import numpy as np, torch
REPO=os.path.expanduser("~/anima")
sys.path.insert(0, os.path.join(REPO,"train","clm","model"))
from model import CLMConfig, CLMConvMoE
PT=os.path.expanduser("~/anima-weights/g1_l8_cov/clm303_deep_L8_cov.pt")

ck=torch.load(PT, map_location="cpu")
sd = ck["model"] if isinstance(ck,dict) and "model" in ck else (ck["state_dict"] if isinstance(ck,dict) and "state_dict" in ck else ck)
saved_cfg = ck.get("cfg") if isinstance(ck,dict) else None
print("[.pt] top keys:", list(ck.keys())[:8] if isinstance(ck,dict) else type(ck))
print("[.pt] saved cfg:", saved_cfg)
# infer dims from state_dict
emb = sd["embed.weight"]; V,d = emb.shape
ntrunk = len({k.split(".")[1] for k in sd if k.startswith("trunk.")})
nexp   = len({k.split(".")[2] for k in sd if k.startswith("moe.experts.")})
print("[.pt] inferred V=%d d=%d n_trunk=%d n_experts=%d"%(V,d,ntrunk,nexp))
cfg=CLMConfig(vocab_size=V,d_model=d,n_trunk_layers=ntrunk,n_experts=nexp,variant="AB",dropout=0.0)
m=CLMConvMoE(cfg); missing,unexp=m.load_state_dict(sd,strict=False)
print("[load] missing=%s unexpected=%s"%(list(missing)[:5],list(unexp)[:5]))
m.eval()

seed="the quiet misty clock on the "
sb=seed.encode("utf-8","surrogateescape"); T=24
tok=np.empty(T,dtype=np.int64)
for p in range(T):
    si=len(sb)-T+p; tok[p]=sb[si] if si>=0 else 32
with torch.no_grad():
    out=m(torch.tensor(tok).unsqueeze(0))       # logits (B,V,T)
    lt=out["logits"][0].transpose(0,1).double().numpy()  # [T,V]
np_logits=np.load("/tmp/np_logits.npy")          # [T,V] from engine
# parity
d_all=np.abs(lt-np_logits)
last_t=T-1
targ_arg=int(np.argmax(lt[last_t])); np_arg=int(np.argmax(np_logits[last_t]))
argmatch_all=sum(int(np.argmax(lt[t])==np.argmax(np_logits[t])) for t in range(T))
res={"pt_argmax_last":targ_arg,"np_argmax_last":np_arg,
     "argmax_match_last": targ_arg==np_arg,
     "argmax_match_allpos": "%d/%d"%(argmatch_all,T),
     "max_abs_delta_logit": float(d_all.max()),
     "mean_abs_delta_logit": float(d_all.mean()),
     "last_pos_max_abs_delta": float(np.abs(lt[last_t]-np_logits[last_t]).max()),
     "pt_top5_last": np.argsort(-lt[last_t])[:5].tolist(),
     "np_top5_last": np.argsort(-np_logits[last_t])[:5].tolist()}
print("PARITY:", json.dumps(res,indent=1))
json.dump(res, open("/tmp/parity_result.json","w"))
print("TORCH_PARITY_DONE")
