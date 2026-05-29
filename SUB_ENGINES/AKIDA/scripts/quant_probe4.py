"""quant_probe4.py -- recover the act_bits=4 activation quantizer step on AKD1000."""
import json, numpy as np, akida
IN=N=16
dev=akida.devices()[0]
m=akida.Model()
m.add(akida.InputData(input_shape=(1,1,IN),input_bits=4,name="in"))
m.add(akida.FullyConnected(units=N,weights_bits=4,activation=True,act_bits=4,name="fc"))
m.map(dev)
fc=m.get_layer("fc")
W=fc.get_variable("weights")
try: fc.set_variable("threshold",np.zeros(N,dtype=np.int32))
except Exception: pass
for w in [1,2,4,7]:
    Wz=np.zeros_like(W); Wz[0,0,0,0]=w
    fc.set_variable("weights",Wz)
    for x0 in range(0,16):
        x=np.zeros((1,1,1,IN),np.uint8); x[0,0,0,0]=x0
        y=m.forward(x).reshape(-1)
        print(json.dumps({"w":int(w),"potential":int(w*x0),"hw_act":int(y[0])}))
