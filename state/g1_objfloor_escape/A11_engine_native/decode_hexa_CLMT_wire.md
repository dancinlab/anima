# core/decode.hexa CLMT (rtype=3) TPR-forward-slot wiring — for pr-cycle landing

The numpy scorer `core/decode.py` CLMT branch is **byte-exact (parity 0.000e+00)** vs the
torch reference (`a11_tpr_parity.py`). The hexa mirror below extends the SAME rtype
dispatcher already present for CLMB (rtype 1/2) to rtype=3 (CLMT TPR role-filler). It
mirrors `decode.py` 1:1 (`a_core_engine_map` — single generator-L3 `.clm` forward, no 2nd
path). Build+device parity on the full `core/decode.hexa` = follow-on (the device path
`forge_dispatch_*` does not compile on fleet hexa v0.511/v0.513 per H_9027; the `--py`
scorer is TERMINAL-eligible per a_eval_py_canonical, so the verdict stands on numpy).

Serialized layout (v0.3 CLMT trailer, after CLMX ext arrays; S_0 in the roW/roB slot):
```
"CLMT" 67,76,77,84 | R:u8(=2) | roles ext (u32 R*d + R*d f32) | S_1 conv block (V,d int4-sym) | S_1 bias ext (u32 V + V f32)
```

## Hunk 1 — `_clmd_load` (after the CLMB trailer block, before `return`)
```hexa
    // ── OPTIONAL CLMT TPR role-filler trailer (A11 CE-deleted forward-slot, rtype=3).
    // roW slot holds S_0; CLMT holds roles[R,d] + S_1[V,d] + S_1.bias. out = S_0·(yn⊙r0)+S_1·(yn⊙r1).
    let mut Rtpr = 0; let mut roles = -1; let mut S1 = -1; let mut S1B = -1
    if off + 5 <= len(rb) && rb[off]==67 && rb[off+1]==76 && rb[off+2]==77 && rb[off+3]==84 {
        rtype = 3
        off = off + 4
        Rtpr = rb[off]; off = off + 1
        roles = t_zeros(Rtpr * d); off = _clmd_load_ext(rb, off, roles)   // (R,d) f32
        S1 = t_zeros(V * d);       off = _clmd_load_block(rb, off, S1)     // (V,d) int4-sym
        S1B = t_zeros(V);          off = _clmd_load_ext(rb, off, S1B)      // (V,)
    }
```
Add to the returned Map: `"Rtpr": Rtpr, "roles": roles, "S1": S1, "S1B": S1B`.

## Hunk 2 — `_clmd_scratch_new` (extend the `rtype > 0` scratch block)
```hexa
    let mut S1Wt = -1; let mut S1Bf = -1; let mut c0buf = -1; let mut c1buf = -1
    let mut tprtmp = -1; let mut xcol1b = -1
    if rtype == 3 {
        S1Wt = _clmd_transpose_w(to_int(W["S1"]), d, V)   // S1 (V,d) → Wt[d,V]
        S1Bf = _clmd_bias_expand(to_int(W["S1B"]), V, T)
        c0buf = t_zeros(T*d); c1buf = t_zeros(T*d)
        tprtmp = t_zeros(T*V); xcol1b = t_zeros(T*d)
    }
```
Add to the returned Map: `"S1Wt": S1Wt, "S1Bf": S1Bf, "c0buf": c0buf, "c1buf": c1buf, "tprtmp": tprtmp, "xcol1b": xcol1b`
(and free them in `_clmd_scratch_free` under `if rtype == 3 { ... }`).

## Hunk 3 — `_clmd_fwd_logits_sc` (readout dispatch, add rtype==3 branch)
```hexa
    let rtype = to_int(W["rtype"])
    if rtype == 3 {
        // CLMT TPR readout: c_r = yn ⊙ roles[r]; out = S_0·c0 + S_1·c1  (roWt slot = S_0.T).
        let roles = to_int(W["roles"])
        let c0 = to_int(sc["c0buf"]); let c1 = to_int(sc["c1buf"]); let tmp = to_int(sc["tprtmp"])
        let mut ci = 0
        while ci < T {
            let mut dj = 0
            while dj < d {
                let yv = t_get(yn, ci*d + dj)
                t_set(c0, ci*d + dj, yv * t_get(roles, dj))
                t_set(c1, ci*d + dj, yv * t_get(roles, d + dj))
                dj = dj + 1
            }
            ci = ci + 1
        }
        _clmd_conv1d_pre(c0, to_int(sc["roWt"]), to_int(W["roB"]), to_int(sc["roBf"]), out_logits, xcol1, T, d, V, 1, 1)
        _clmd_conv1d_pre(c1, to_int(sc["S1Wt"]), to_int(W["S1B"]), to_int(sc["S1Bf"]), tmp, to_int(sc["xcol1b"]), T, d, V, 1, 1)
        let mut oi = 0
        while oi < T*V { t_set(out_logits, oi, t_get(out_logits, oi) + t_get(tmp, oi)); oi = oi + 1 }
    } else if rtype > 0 {
        // ... existing CLMB Hadamard/linear branch (unchanged) ...
    } else {
        // ... existing additive branch (unchanged) ...
    }
```

## ByteGPT twin (BGT trailer, decode.hexa bg readout) — same mechanism, G0-green trunk
`bg_load` gets a `"BGT\x01"` (66,71,84,1) trailer parse → `tpr_roles[R,d]`, `tpr_S1[V,d]`
(f32; head slot = S_0); `bg_forward_last_W` readout branch `logits = head·(lastrow⊙r0) +
S_1·(lastrow⊙r1)`; the KV decode forces the full-forward path when `tpr_roles` present
(the KV step bypasses the head). Numpy diff = `decode.py.CLMT_BGT.diff` (byte-exact).

## ARCHITECTURE.json lockstep (on landing)
`core/` decode node: `§readout · CLMT rtype=3 / BGT TPR role-filler slot · CLMX v0.3
ext-block (roles[R,d] + S_1[V,d])` — 1:1 with the live hexa (a_verified_must_wire box 4).
Writers: `core/serialize.py serialize_v3_tpr` (CLM roW←S_0 + CLMT) + ByteGPT `serialize` +
`BGT\x01` append (mirror of the trainer `serialize_tpr` / `append_bgt`).
