#!/usr/bin/env python3
# Diagnostic: does the with-grammar ckpt emit the RAW 0xFE/0xFF sentinel call
# when seeded in (a) the chat format vs (b) the agent-lane demo prose format?
# This separates "grammar not learned" from "seed-format mismatch".
import torch, sys
sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location("t","tooluse_rung0_ab.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
dev="cuda" if torch.cuda.is_available() else "cpu"
ck=torch.load("tooluse_rung0_with_grammar_18m.pt",map_location=dev,weights_only=False)
cfg=ck["config"]
mdl=m.ConsciousLMReconstructed(256,cfg["dim"],cfg["heads"],cfg["layers"],cfg["block_size"]).to(dev)
mdl.load_state_dict(ck["model_state"])
ASK,END=m.ASK,m.END
def probe(seed_bytes, n=80):
    out=m.gen_bytes(mdl, seed_bytes, n, dev, temperature=0.7, top_k=40, stop_on_end=False)
    fe=out.count(bytes([ASK])); ff=out.count(bytes([END]))
    return fe,ff,out
# (a) chat seed (what the falsifier used)
seeds_chat=[f"사용자: What is the secret value for vault key PB0{i}? | 도우미: ".encode() for i in range(1,7)]
# (b) agent-lane demo prose seed (how the grammar was TAUGHT — (c) don't-know lead)
seeds_demo=[f"I genuinely don't know key PB0{i}; rather than guess, I call the tool. ".encode() for i in range(1,7)]
for lab,seeds in [("CHAT-seed",seeds_chat),("DEMO-seed",seeds_demo)]:
    tot_fe=0; calls=0
    for s in seeds:
        fe,ff,out=probe(s)
        tot_fe+=fe
        fr=m.parse_call_frame(out)
        if fr["found"]: calls+=1
    print(f"{lab}: raw_0xFE_emitted_total={tot_fe} well_formed_calls={calls}/{len(seeds)}")
# show one demo-seed transcript with sentinels made visible
fe,ff,out=probe(seeds_demo[0],100)
vis=out.replace(bytes([ASK]),b"<ASK>").replace(bytes([END]),b"<END>")
print("DEMO-seed sample:", vis.decode("utf-8","replace")[:160])
