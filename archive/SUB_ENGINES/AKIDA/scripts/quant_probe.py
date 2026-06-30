"""quant_probe.py -- map AKD1000 act_bits=2 activation quantizer step function.

Drives a single FC unit with controlled integer potentials by using an identity-
ish weight so potential == a known scalar, sweeping potential 0..30 to recover
the exact potential->activation step boundaries the chip applies before clamping.
One JSON line: {"potential": p, "hw_act": a} per probe.
"""
import json, numpy as np, akida
IN=N=16
dev=akida.devices()[0]
m=akida.Model()
m.add(akida.InputData(input_shape=(1,1,IN),input_bits=4,name="in"))
m.add(akida.FullyConnected(units=N,weights_bits=4,activation=True,act_bits=2,name="fc"))
m.map(dev)
fc=m.get_layer("fc")
W=fc.get_variable("weights")
# unit 0 reads only input line 0 with weight 1 -> potential = x[0]
Wz=np.zeros_like(W); Wz[0,0,0,0]=1
fc.set_variable("weights",Wz)
try: fc.set_variable("threshold",np.zeros(N,dtype=np.int32))
except Exception: pass
# but x[0] max is 15. To reach higher potential use weight w on line0: pot=w*x0
for w in [1,2,3]:
    Wz=np.zeros_like(W); Wz[0,0,0,0]=w
    fc.set_variable("weights",Wz)
    for x0 in range(0,16):
        x=np.zeros((1,1,1,IN),np.uint8); x[0,0,0,0]=x0
        y=m.forward(x).reshape(-1)
        print(json.dumps({"w":int(w),"x0":int(x0),"potential":int(w*x0),"hw_act":int(y[0])}))
