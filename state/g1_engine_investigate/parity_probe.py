import sys, os, json
import numpy as np
REPO=os.path.expanduser("~/anima")
sys.path.insert(0, os.path.join(REPO,"core"))
sys.path.insert(0, os.path.join(REPO,"train","clm","model"))
import decode as clm

CLM=os.path.expanduser("~/anima-weights/g1_l8_cov/clm303_deep_L8_cov.clm")
PT =os.path.expanduser("~/anima-weights/g1_l8_cov/clm303_deep_L8_cov.pt")

# --- AXIS 1a: engine parses dims ---
cfg = clm.clm_config(CLM) if hasattr(clm,"clm_config") else None
W = clm.clm_load_weights(CLM)
print("[engine .clm parsed] d=%s E=%s V=%s K=%s L=%s bind_type=%s"%(
    W["d"],W["E"],W["V"],W["K"],W["L"],W.get("bind_type",0)))

# fixed token window
seed="the quiet misty clock on the "
sb=seed.encode("utf-8","surrogateescape")
T=24
tok=np.empty(T,dtype=np.float64)
for p in range(T):
    si=len(sb)-T+p
    tok[p]=float(sb[si]) if si>=0 else 32.0
logits_np=clm._fwd_logits(W, tok, T)   # [T,V]
np_last=logits_np[T-1]
np_arg=int(np.argmax(np_last))
print("[engine forward] logits[T-1] argmax=%d  top5=%s"%(
    np_arg, np.argsort(-np_last)[:5].tolist()))
np.save("/tmp/np_logits.npy", logits_np)
json.dump({"d":int(W["d"]),"E":int(W["E"]),"V":int(W["V"]),"K":int(W["K"]),
           "L":int(W["L"]),"bind_type":int(W.get("bind_type",0)),
           "np_argmax_last":np_arg,
           "np_argmax_allpos":[int(np.argmax(logits_np[t])) for t in range(T)]},
          open("/tmp/engine_side.json","w"))
print("ENGINE_SIDE_DONE")
