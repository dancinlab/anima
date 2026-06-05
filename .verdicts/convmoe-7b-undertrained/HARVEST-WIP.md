# M13 7B ConvMoE — H200 harvest (Lane P) WIP

- pod: vast 39621709 (H200 143GB), label convmoe7b-refire-h200, ssh6.vast.ai:21708
- fire: CLM/train/fire_7b_undertrained.sh, branch lane-p/convmoe-7b-undertrained-refire-20260605-155208
- config: d6208/L30/E30 (~7.057B), steps=3500, seq=512, batch=2, accum=16, R2 webscale 5-lang @ 3.0GB/lang (~15GB)
- state @ pickup 16:16 UTC: corpus-fetch phase (eng+fra done 6GB, deu fetching), GPU 0%
- owner agent: single authoritative; DO NOT rent new pods; HF-first harvest before teardown.
