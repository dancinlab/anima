"""conv_isolate.py -- isolate the ON-CHIP Convolutional math (kernel flip? pad?).

Stage-1 InputConv already byte-matches the SW cross-corr model. Stage-2 (HW Conv)
diverges. To recover the HW Conv math we feed a CONTROLLED known activation map
into a single on-chip Convolutional layer and dump output. We cannot feed Conv
directly (needs an input layer), so we use InputConv as an IDENTITY-ish pass with
a single 1-hot kernel to inject a known map, OR read the Conv math via a 1-filter
3x3 kernel with a single impulse input so the output reveals kernel orientation.

Approach: InputConv F1=1 with a kernel that is all-zero except center=1 (identity,
SAME pad) -> stage1 output == input (clipped/quantized). Then Conv F2=1 with a
kernel that is 1 at ONE corner only. An impulse input (single pixel=15) reveals
WHERE the output lands -> tells us cross-correlation vs convolution (flip).
"""
import json, hashlib
import numpy as np
import akida
def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]
out={}
dev=akida.devices()[0]
H=W=5; C=1; K=3
m=akida.Model()
m.add(akida.InputConvolutional(input_shape=(H,W,C),kernel_size=(K,K),filters=1,
    padding=akida.Padding.Same,weights_bits=4,activation=True,act_bits=4,name="c1"))
m.add(akida.Convolutional(kernel_size=(K,K),filters=1,padding=akida.Padding.Same,
    weights_bits=4,activation=True,act_bits=4,name="c2"))
m.map(dev)
out["backends"]=[str(s.backend) for s in m.sequences]
c1=m.get_layer("c1"); c2=m.get_layer("c2")
# c1 identity: center weight =1 only
W1=np.zeros(c1.get_variable("weights").shape,dtype=c1.get_variable("weights").dtype)
W1[K//2,K//2,0,0]=1
c1.set_variable("weights",W1)
try: c1.set_variable("threshold",np.zeros(1,dtype=np.int32))
except Exception: pass
# c2: kernel = 7 at TOP-LEFT corner [0,0] only
W2=np.zeros(c2.get_variable("weights").shape,dtype=c2.get_variable("weights").dtype)
W2[0,0,0,0]=1
c2.set_variable("weights",W2)
try: c2.set_variable("threshold",np.zeros(1,dtype=np.int32))
except Exception: pass
out["W2_nonzero_at"]="[0,0,0,0]=1 (top-left corner)"
# impulse at center pixel
x=np.zeros((1,H,W,C),dtype=np.uint8); x[0,H//2,W//2,0]=15
y=np.asarray(m.forward(x)).reshape(H,W).astype(int)
out["impulse_center_input"]=[H//2,W//2]
out["output_grid"]=y.tolist()
# where is the nonzero output? cross-corr: out[i,j]=sum x[i+di,j+dj]*W[di,dj]
# W nonzero at [0,0] => out[i,j]=x[i+(0-1),j+(0-1)]*1 = x[i-1,j-1] -> impulse at center(2,2)
#   appears at out[3,3] for cross-correlation (SAME, pad=1)
# convolution (flip): out[i,j]=x[i+1,j+1] -> appears at out[1,1]
nz=[(i,j) for i in range(H) for j in range(W) if y[i,j]>0]
out["nonzero_positions"]=nz
print(json.dumps(out))
