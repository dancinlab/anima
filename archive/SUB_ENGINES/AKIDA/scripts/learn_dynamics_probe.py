"""learn_dynamics_probe.py -- characterize AKD1000 on-chip learning dynamics.

Question: is the AkidaUnsupervised on-chip learning rule modelable in SW (a
deterministic Hebbian weight update) or does it depend on hidden analog/internal
chip state the inference-only SW cannot reproduce?

Captures: trainable-layer weights BEFORE fit, AFTER fit on a fixed binary input
batch (seed-fixed), repeated TWICE on the chip from the SAME init to test
determinism. If the two fitted weight tensors are identical AND derivable from
the inputs, the rule is modelable. If not, the SW (inference-only) cannot model
it -> honest CLOSED-NEGATIVE.
"""
import json, numpy as np, akida

def fit_once():
    dev=akida.devices()[0]
    model=akida.Model()
    model.add(akida.InputData(input_shape=(1,1,16),input_bits=1,name="in"))
    model.add(akida.FullyConnected(units=10,name="fc",weights_bits=1,activation=True))
    model.map(dev)
    fc=model.get_layer("fc")
    model.compile(optimizer=akida.AkidaUnsupervised(num_weights=2,learning_competition=0.1))
    w_before=np.array(fc.get_variable("weights")).copy()
    rng=np.random.default_rng(42)
    x=rng.integers(0,2,size=(8,1,1,16),dtype=np.uint8)
    model.fit(x)
    w_after=np.array(fc.get_variable("weights")).copy()
    return w_before,w_after

out={}
b1,a1=fit_once()
b2,a2=fit_once()
out["w_before_all_equal_runs"]=bool(np.array_equal(b1,b2))
out["w_before_changed_by_fit_run1"]=bool(not np.array_equal(b1,a1))
out["w_after_deterministic_across_runs"]=bool(np.array_equal(a1,a2))
out["w_before_sha"]=__import__("hashlib").sha256(b1.tobytes()).hexdigest()[:16]
out["w_after_run1_sha"]=__import__("hashlib").sha256(a1.tobytes()).hexdigest()[:16]
out["w_after_run2_sha"]=__import__("hashlib").sha256(a2.tobytes()).hexdigest()[:16]
out["w_shape"]=list(a1.shape)
out["w_before_nonzero"]=int(np.count_nonzero(b1))
out["w_after_nonzero"]=int(np.count_nonzero(a1))
out["delta_nonzero"]=int(np.count_nonzero(a1!=b1))
print(json.dumps(out,indent=2))
