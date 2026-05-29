"""conv_hw_capture.py -- capture the ON-CHIP Convolutional layer output for SW match.

Finding (conv_map_diag): InputConvolutional ALWAYS runs on the akida SW backend
(v1 pixel front-end); the genuine Convolutional layer maps to HW (CNP). To get a
HW-conv output that the SW model must byte-match, we build InputConv(SW, FIXED
deterministic weights) -> Convolutional(HW), set BOTH weight tensors to fixed
symmetric int4, and dump:
  - the full final output tensor + sha  (end-to-end SW-front + HW-conv)
  - both weight tensors (shape/sha) so the SW model uses identical kernels
We also dump the InputConv-only output (single-layer SW) so the SW model can be
validated layer-by-layer: SW must reproduce (a) the SW InputConv stage AND (b)
the HW Convolutional stage, end-to-end byte-identical.
"""
import json, hashlib
import numpy as np
import akida

def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]
out = {"sdk": akida.__version__}
dev = akida.devices()[0]
H=W=8; C=1; F1=8; F2=8; K=3
out["cfg"] = {"H":H,"W":W,"C":C,"F1":F1,"F2":F2,"K":K}

# --- single InputConvolutional only (the SW front-end), to capture stage-1 ---
m1 = akida.Model()
m1.add(akida.InputConvolutional(input_shape=(H,W,C), kernel_size=(K,K), filters=F1,
    padding=akida.Padding.Same, weights_bits=4, activation=True, act_bits=4, name="c1"))
m1.map(dev)
c1 = m1.get_layer("c1")
rng = np.random.default_rng(7); lim=7
W1 = rng.integers(-lim,lim+1,size=c1.get_variable("weights").shape).astype(c1.get_variable("weights").dtype)
c1.set_variable("weights", W1)
try: c1.set_variable("threshold", np.zeros(F1, dtype=np.int32))
except Exception as e: out["c1_thr_note"]=repr(e)[:120]
out["c1_backend"] = str(m1.sequences[0].backend)
out["W1_shape"]=list(W1.shape); out["W1_sha"]=sh(W1)
out["W1_flat"]=W1.reshape(-1).astype(int).tolist()
out["act_step_c1"]=None
try: out["act_step_c1"]=np.asarray(c1.get_variable("act_step")).reshape(-1).astype(int).tolist()
except Exception as e: out["act_step_c1_note"]=repr(e)[:120]

# --- 2-layer: InputConv(SW) -> Conv(HW) ---
m = akida.Model()
m.add(akida.InputConvolutional(input_shape=(H,W,C), kernel_size=(K,K), filters=F1,
    padding=akida.Padding.Same, weights_bits=4, activation=True, act_bits=4, name="c1"))
m.add(akida.Convolutional(kernel_size=(K,K), filters=F2, padding=akida.Padding.Same,
    weights_bits=4, activation=True, act_bits=4, name="c2"))
m.map(dev)
out["seq_backends"] = [str(s.backend) for s in m.sequences]
out["on_hw_any"] = any("Hardware" in str(s.backend) for s in m.sequences)
g1 = m.get_layer("c1"); g2 = m.get_layer("c2")
g1.set_variable("weights", W1)
try: g1.set_variable("threshold", np.zeros(F1, dtype=np.int32))
except Exception: pass
W2 = rng.integers(-lim,lim+1,size=g2.get_variable("weights").shape).astype(g2.get_variable("weights").dtype)
g2.set_variable("weights", W2)
try: g2.set_variable("threshold", np.zeros(F2, dtype=np.int32))
except Exception as e: out["c2_thr_note"]=repr(e)[:120]
out["W2_shape"]=list(W2.shape); out["W2_sha"]=sh(W2)
out["W2_flat"]=W2.reshape(-1).astype(int).tolist()
out["act_step_c2"]=None
try: out["act_step_c2"]=np.asarray(g2.get_variable("act_step")).reshape(-1).astype(int).tolist()
except Exception as e: out["act_step_c2_note"]=repr(e)[:120]

probes=[]
for idx in range(4):
    if idx==0: x=np.zeros((1,H,W,C),dtype=np.uint8)
    elif idx==1: x=np.full((1,H,W,C),15,dtype=np.uint8)
    elif idx==2: x=(np.arange(H*W*C).reshape(1,H,W,C)%16).astype(np.uint8)
    else: x=np.random.default_rng(2026).integers(0,16,size=(1,H,W,C)).astype(np.uint8)
    y1=np.asarray(m1.forward(x)).reshape(-1).astype(np.int64)   # SW InputConv only
    y=np.asarray(m.forward(x)).reshape(-1).astype(np.int64)     # SW->HW end-to-end
    probes.append({"idx":idx,"input_sha":sh(x),
                   "y1_sha":sh(y1),"y1_shape":list(np.asarray(m1.forward(x)).shape),
                   "y1_first16":y1[:16].tolist(),"y1_max":int(y1.max()),
                   "y_sha":sh(y),"y_shape":list(np.asarray(m.forward(x)).shape),
                   "y_first24":y[:24].tolist(),"y_max":int(y.max()),"y_n_levels":int(len(np.unique(y)))})
out["probes"]=probes
print(json.dumps(out))
