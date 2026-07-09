#!/usr/bin/env python3
"""P3 engine_cli chat-critical parity oracle.
Expected values are hand-derived by replicating hexa arithmetic (HAND),
composed over pre-verified helpers (COMPOS), or structural-only (STRUCT).
Float assert at 12 decimal places; exact for int/str/struct."""
import sys, math
sys.path.insert(0, 'core')
import engine_cli as E

P = 0; F = 0; report = []
def chk(kind, name, got, exp, dp=12):
    global P, F
    ok = False
    if isinstance(exp, float) or isinstance(got, float):
        ok = abs(got - exp) <= 10 ** (-dp)
        detail = f"got={got!r} exp={exp!r} |Δ|={abs(got-exp):.2e}"
    elif isinstance(exp, list):
        ok = len(exp) == len(got) and all(
            (abs(a-b) <= 10**(-dp)) if isinstance(b, float) or isinstance(a, float) else a == b
            for a, b in zip(got, exp))
        detail = f"got={got!r} exp={exp!r}"
    else:
        ok = got == exp
        detail = f"got={got!r} exp={exp!r}"
    P += ok; F += (not ok)
    report.append(f"  [{'PASS' if ok else 'FAIL'}] {kind:6} {name}: {detail}")

# ── conflict family (HAND) ──
chk("HAND", "conflict_scalar_compete", E.conflict_scalar(0.6, -0.4), 0.6*0.4)
chk("HAND", "conflict_scalar_samesign", E.conflict_scalar(0.5, 0.5), 0.0)
chk("HAND", "conflict_scalar_clip", E.conflict_scalar(2.0, -3.0), 1.0)  # 6.0 clipped
chk("HAND", "conflict_net_tension", E.conflict_net_tension(0.6, -0.4), abs(0.6 + (-0.4)))
chk("HAND", "conflict_net_tension2", E.conflict_net_tension(-0.5, -0.5), 1.0)
chk("HAND", "conflict_recruited_depth", E.conflict_recruited_depth(0.5, 2, 4), 4)  # int(2.5)=2
chk("HAND", "conflict_recruited_depth_zero", E.conflict_recruited_depth(0.0, 3, 4), 3)
chk("HAND", "conflict_recruited_depth_full", E.conflict_recruited_depth(1.0, 2, 4), 6)  # int(4.5)=4

# ── fm_prefix_decodability (HAND) ──
chk("HAND", "fm_prefix", E.fm_prefix_decodability([1.0, 0.5, 0.25], 0.5), 1.0 + 0.5*0.5 + 0.25*0.25)
chk("HAND", "fm_prefix_empty", E.fm_prefix_decodability([], 0.9), 0.0)

# ── event segmentation (HAND) ──
chk("HAND", "event_boundaries", E.event_segment_boundaries([0.1, 0.9, 0.2, 0.95, 0.3], 0.5), [0, 1, 3])
chk("HAND", "event_boundaries_empty", E.event_segment_boundaries([], 0.5), [])
chk("HAND", "event_boundaries_flat", E.event_segment_boundaries([0.1, 0.2, 0.3], 0.5), [0])
chk("HAND", "event_starts_fixed", E.event_segment_starts_fixed(10, 3), [0, 3, 6, 9])
chk("HAND", "event_starts_zero", E.event_segment_starts_fixed(0, 3), [])
chk("HAND", "event_starts_badchunk", E.event_segment_starts_fixed(5, 0), [])

# ── drive_arbitrate (HAND) ──
chk("HAND", "drive_wta", E.drive_arbitrate([0.1, 0.9, 0.5], 0.0, -1), 1)
chk("HAND", "drive_empty", E.drive_arbitrate([], 0.0, -1), -1)
chk("HAND", "drive_hyst_switch", E.drive_arbitrate([0.1, 0.9, 0.5], 0.2, 0), 1)   # 0.8>0.2 switch
chk("HAND", "drive_hyst_hold", E.drive_arbitrate([0.85, 0.9, 0.5], 0.2, 0), 0)    # 0.05<=0.2 hold
chk("HAND", "drive_incumbent_is_best", E.drive_arbitrate([0.1, 0.9, 0.5], 0.2, 1), 1)

# ── _prefetch_unit (HAND) ──
chk("HAND", "prefetch_unit", E._prefetch_unit([3.0, 4.0]), [0.6, 0.8])
chk("HAND", "prefetch_unit_zero", E._prefetch_unit([0.0, 0.0]), [0.0, 0.0])

# ── _sr_mi_bits (HAND) ──
chk("HAND", "sr_mi_independent", E._sr_mi_bits([0, 0, 1, 1], [0, 1, 0, 1]), 0.0)
chk("HAND", "sr_mi_perfect", E._sr_mi_bits([0, 0, 1, 1], [0, 0, 1, 1]), 1.0)
chk("HAND", "sr_mi_empty", E._sr_mi_bits([], []), 0.0)

# ── sr_channel_mi (COMPOS: independent replication via verified LCG helpers) ──
def sr_ref(amp, thr, sigma, period, T, mode, shuffle, seed):
    two_pi = 6.283185307179586
    ethr = 0.0 if mode == 1 else thr
    xs = []; ys = []; st = seed & 2147483647; t = 0
    while t < T:
        sig = amp * math.sin(two_pi * float(t) / float(period))
        g = E._lcg_gauss(st); noise = sigma * g[0]; st = int(g[1]) & 2147483647
        xs.append(1 if sig >= 0.0 else 0)
        ys.append(1 if (sig + noise) >= ethr else 0)
        t += 1
    if shuffle == 1:
        sh = (seed ^ 305419896) & 2147483647; i = T - 1
        while i > 0:
            sh = E._lcg_next(sh); j = sh % (i + 1)
            xs[i], xs[j] = xs[j], xs[i]; i -= 1
    # MI hand
    n = [[0.0, 0.0], [0.0, 0.0]]
    for a, b in zip(xs, ys): n[a][b] += 1.0
    tf = float(len(xs)); px = [(n[0][0]+n[0][1])/tf, (n[1][0]+n[1][1])/tf]
    py = [(n[0][0]+n[1][0])/tf, (n[0][1]+n[1][1])/tf]; mi = 0.0
    for a in (0, 1):
        for b in (0, 1):
            if n[a][b] > 0.0:
                p = n[a][b]/tf; mi += p * math.log2(p/(px[a]*py[b]))
    return mi
chk("COMPOS", "sr_channel_mi_a", E.sr_channel_mi(1.0, 0.3, 0.2, 8, 64, 0, 0, 12345),
    sr_ref(1.0, 0.3, 0.2, 8, 64, 0, 0, 12345))
chk("COMPOS", "sr_channel_mi_ablate", E.sr_channel_mi(1.0, 0.3, 0.2, 8, 64, 1, 0, 12345),
    sr_ref(1.0, 0.3, 0.2, 8, 64, 1, 0, 12345))
chk("COMPOS", "sr_channel_mi_shuffle", E.sr_channel_mi(1.0, 0.3, 0.2, 8, 64, 0, 1, 999),
    sr_ref(1.0, 0.3, 0.2, 8, 64, 0, 1, 999))

# ── flag resolvers (HAND) ──
chk("HAND", "refsel_flag_on", E._cli_refsel_flag(["--refsel", "on"]), "on")
chk("HAND", "refsel_flag_eqoff", E._cli_refsel_flag(["--refsel=off"]), "off")
chk("HAND", "refsel_flag_no", E._cli_refsel_flag(["--no-refsel"]), "off")
chk("HAND", "refsel_flag_none", E._cli_refsel_flag(["--foo"]), "")
chk("HAND", "resolve_refsel_on", E.engine_cli_resolve_refsel(["--refsel=on"]), True)
chk("HAND", "resolve_refsel_default", E.engine_cli_resolve_refsel([]), False)
chk("HAND", "fm_flag_on", E._cli_forward_model_flag(["--forward-model", "on"]), "on")
chk("HAND", "fm_flag_eqoff", E._cli_forward_model_flag(["--forward-model=off"]), "off")
chk("HAND", "fm_flag_no", E._cli_forward_model_flag(["--no-forward-model"]), "off")
chk("HAND", "resolve_fm_on", E.engine_cli_resolve_forward_model(["--forward-model=on"]), True)
chk("HAND", "resolve_fm_default", E.engine_cli_resolve_forward_model([]), False)

# ── self-chain (HAND) ──
u10 = E.SelfIdentity([1.0, 0.0], 2)
u01 = E.SelfIdentity([0.0, 1.0], 2)
chk("HAND", "self_chain_bend_orth", E.self_chain_bend(u10, u01), 1.0)
chk("HAND", "self_chain_bend_same", E.self_chain_bend(u10, u10), 0.0)
r = E.self_from_vec([3.0, 4.0], 2)
chk("HAND", "self_from_vec", [r.v[0], r.v[1]], [0.6, 0.8])
chk("HAND", "self_chain_unit_of", E.self_chain_unit_of([3.0, 4.0], 2), [0.6, 0.8])
sd = E.self_drift_exp(E.SelfIdentity([1.0, 0.0], 2), 1, 0.5)
den = math.sqrt(1.0 + 0.25)
chk("HAND", "self_drift_exp", [sd.v[0], sd.v[1]], [1.0/den, 0.5/den])
# self_chain_confluence: alpha clamped; dn=unit dream; v2=(1-a)wn+a dn then normed
conf = E.self_chain_confluence(E.SelfIdentity([1.0, 0.0], 2), [0.0, 2.0], 0.4)
# a=0.4, dn=norm([0,2])=[0,1], v2=[0.6*1+0.4*0, 0.6*0+0.4*1]=[0.6,0.4] -> norm
d2 = math.sqrt(0.6*0.6 + 0.4*0.4)
chk("HAND", "self_chain_confluence", [conf.v[0], conf.v[1]], [0.6/d2, 0.4/d2])
conf0 = E.self_chain_confluence(E.SelfIdentity([1.0, 0.0], 2), [0.0, 2.0], 0.0)
chk("HAND", "self_chain_confluence_a0", [conf0.v[0], conf0.v[1]], [1.0, 0.0])
# self_chain_dream_gain: w_bent moved toward dream => gain>0 exact
wn = E.SelfIdentity([1.0, 0.0], 2); wb = E.self_from_vec([1.0, 1.0], 2); dunit = [0.0, 1.0]
# self_cos(wb,dn)=wb.v[1], self_cos(wn,dn)=0
chk("HAND", "self_chain_dream_gain", E.self_chain_dream_gain(wn, wb, dunit), (1.0/math.sqrt(2.0)) - 0.0)

# ── other-identity chain (HAND / STRUCT) ──
o = E.other_new(3, 1)
chk("HAND", "other_new", o.v, [0.0, 1.0, 0.0])
chk("HAND", "other_cos_self", E.other_cos(o, o), 1.0)
chk("HAND", "other_dim", E.other_dim(o), 3)
chk("HAND", "other_component", E.other_component(o, 1), 1.0)
od = E.other_drift(o, 1, 0.5)  # tick+1=2, ax=2%3=2 -> [0,1,0.5] norm
dd = math.sqrt(1.0 + 0.25)
chk("HAND", "other_drift", od.v, [0.0, 1.0/dd, 0.5/dd])
ode = E.other_drift_exp(o, 0, 0.5)  # ax=0 -> [0.5,1,0] norm
chk("HAND", "other_drift_exp", ode.v, [0.5/dd, 1.0/dd, 0.0])
c = E.other_chain_new(o)
chk("HAND", "other_chain_new_flat", c.flat, [0.0, 1.0, 0.0])
chk("HAND", "other_chain_len1", E.other_chain_len(c), 1)
c2 = E.other_chain_append(c, E.other_new(3, 0))
chk("HAND", "other_chain_append_flat", c2.flat, [0.0, 1.0, 0.0, 1.0, 0.0, 0.0])
chk("HAND", "other_chain_count2", E.other_chain_count(c2), 2)
chk("HAND", "other_chain_latest", E.other_chain_latest(c2).v, [1.0, 0.0, 0.0])
chk("HAND", "other_chain_retro_cos", E.other_chain_retro_cos(c2, 1), 0.0)  # cos(w1=[1,0,0], w0=[0,1,0])=0
cff = E.other_chain_from_flat([0.0, 1.0, 0.0, 1.0, 0.0, 0.0], 2, 3)
chk("HAND", "other_chain_from_flat", E.other_chain_component(cff, 3), 1.0)
chk("HAND", "other_chain_fit_lt3", E.other_chain_fit(E.other_new(3, 0), c2), 0.0)  # count<3

# ── tr_psi / tension_resolve (COMPOS via ci_emit_drive; topo_couple=off = deterministic) ──
class Cfg:  # minimal EngineConfig stand-in
    def __init__(self, tc): self.topo_couple = tc
# build populations of 15-lane vectors; ci_emit_drive is pre-verified
lane = lambda drive: [drive if k in (0, 4) else 0.0 for k in range(15)]
pop = [lane(1.0), lane(1.0), lane(0.0), lane(0.0)]  # 2 of 4 "emit"
psi_ref = 0
for row in pop:
    if E.ci_emit_drive(row) >= 0.5: psi_ref += 1
chk("COMPOS", "tr_psi", E.tr_psi(pop, 0.5), float(psi_ref)/4.0)
chk("HAND", "tr_psi_empty", E.tr_psi([], 0.5), 0.0)
chk("HAND", "_tr_absdev", E._tr_absdev(0.7, 0.5), 0.2)
chk("HAND", "_spr_sig", E._spr_sig([[0.0]*7 + [2.0] + [0.0]*7, [0.0]*7 + [4.0] + [0.0]*7]), 3.0)
# tension_resolve_depth with topo_couple OFF: pop unchanged, settle at depth 0 if initial |psi-thr|<eps
psi0 = float(psi_ref)/4.0  # 0.5
res = E.tension_resolve_depth(pop, [], 0.1, psi0, 5, 0, 1e-9, Cfg(False))
chk("COMPOS", "tension_resolve_depth_off", res, [0.0, psi0])  # |psi-thr|=0<eps -> settle 0
resi = E.tension_resolve_interruptible(pop, [], 0.1, psi0, 5, 0, 1e-9, 0, pop, Cfg(False))
sig_ref = E._spr_sig(pop)
chk("COMPOS", "tension_resolve_interruptible_off", resi, [0.0, psi0, sig_ref, 0.0])

# ── referent_select / faculty_cascade / anticipatory (COMPOS over verified mem helpers) ──
mem = E.immune_grow_new(E.immune_embed_key("the sky is blue"), "blue", 8, 8, True)
cands = ["the sky is blue", "zzz unknown"]
keys = [E.immune_embed_key(x) for x in cands]
# referent_select returns first candidate with contradiction==0.0
ref_exp = -1
for idx, k in enumerate(keys):
    if E.affect_substrate_features(mem, k, "blue").contradiction == 0.0:
        ref_exp = idx; break
chk("COMPOS", "referent_select", E.referent_select(mem, keys, "blue"), ref_exp)
chk("COMPOS", "referent_select_text", E.referent_select_text(mem, cands, "blue"), ref_exp)
# faculty_cascade 2-hop
mem_a = E.immune_memory_new_text("q1", "mid", 64)
mem_b = E.immune_memory_new_text("mid", "final", 64)
fc_exp = E.immune_memory_recall(mem_b, E.immune_embed_key(
    E.immune_memory_recall(mem_a, E.immune_embed_key("q1"))))
chk("COMPOS", "faculty_cascade", E.faculty_cascade(mem_a, mem_b, E.immune_embed_key("q1")), fc_exp)
chk("HAND", "faculty_cascade_abstain",
    E.faculty_cascade(E.immune_memory_new_text("other", "x", 64), mem_b, E.immune_embed_key("q1")), "")
# anticipatory_prefetch: replicate via verified vforward_predict + _prefetch_unit + recall_margin
ff = E.vforward_new(8, 3, 0.1)     # ctx_dim = 3*8 = 24
ctx = [0.01 * (i + 1) for i in range(24)]
im = E.immune_memory_new(E.vforward_predict(ff, ctx), "v", 64)
pred = E.vforward_predict(ff, ctx); key = E._prefetch_unit(pred)
chk("COMPOS", "anticipatory_prefetch", E.anticipatory_prefetch(ff, im, ctx),
    E.immune_memory_recall_margin(im, key))
chk("COMPOS", "anticipatory_prefetch_value", E.anticipatory_prefetch_value(ff, im, ctx),
    E.immune_memory_recall(im, key))

# NOTE: tension_resolve topo_couple=ON path is a verbatim 1:1 transcription of the hexa
# (the only ON-specific line `if cfg.topo_couple: pop = topo_apply_op(pop, adj, alpha, op)`
# is byte-identical to the hexa source) — marked STRUCTURALLY-VERIFIED, not value-oracled,
# because constructing a topo_apply_op input that matches its adj/lane contract is out of
# scope for this harness.

# ── other_chain_fit count>=3 (COMPOS via verified _argmax_abs/_wrap) ──
ch = E.other_chain_new(E.other_new(4, 0))
ch = E.other_chain_append(ch, E.other_new(4, 1))
ch = E.other_chain_append(ch, E.other_new(4, 2))  # count=3, axis trend 0->1->2
cand = E.other_new(4, 3)
def fit_ref(cand, c):
    wK = E._other_wp(c, c.count-1); wKm1 = E._other_wp(c, c.count-2); wKm2 = E._other_wp(c, c.count-3)
    dl = [wK.v[i]-wKm1.v[i] for i in range(c.dim)]
    dp = [wKm1.v[i]-wKm2.v[i] for i in range(c.dim)]
    aK = E._argmax_abs(dl, c.dim); aKm1 = E._argmax_abs(dp, c.dim)
    a_pred = E._wrap(aK + (aK - aKm1), c.dim)
    r = []; mag = 0.0
    for j in range(c.dim):
        e = cand.v[j]-wK.v[j]; r.append(e); mag += e*e
    if mag <= 0.0: return 0.0
    return r[a_pred] / math.sqrt(mag)
chk("COMPOS", "other_chain_fit_ge3", E.other_chain_fit(cand, ch), fit_ref(cand, ch))

print("\n".join(report))
print(f"\n=== P3 PARITY: {P} PASS / {F} FAIL  (total {P+F}) ===")
sys.exit(1 if F else 0)
