"""FROZEN-1 decision experiment (H_9122) — recall-vs-recombine, DIRECTIONAL numpy mirror.

Faithful mirror of anima's ImmuneMemory lane ops (core/engine_cli.hexa, reference-matched):
  - immune_embed_key : DIM=64 byte-trigram FNV-1a additive histogram, L2-normalized (:1003)
  - _immune_fnv1a    : h=2166136261; h=(h^b)*16777619 & 0xFFFFFFFF (:_)
  - recall           : nearest cell by L2(key); FIRE iff L2 <= recall_thr(0.15) → returns
                       that cell's WHOLE cell_value string; else ABSTAIN (:1087)
Decides: does the lane surface a NOVEL cross (A,D), or only recall a whole stored pair?
Structural prediction (pre-registered MISS bias): recall returns one whole cell_value
(valAB or valCD), never a synthesis → single-parent coverage only.
DIRECTIONAL (numpy mirror per a_engine_native_learning) — engine-native .hexa = follow-on.
"""
DIM = 64
RECALL_THR = 0.15

def fnv1a(bs):
    h = 2166136261
    for b in bs:
        h = h ^ b
        h = (h * 16777619) & 4294967295
    return h

def embed_key(text):
    n = 3
    bs = [ord(c) for c in text]
    blen = len(bs)
    v = [0.0] * DIM
    if blen < n:
        v[fnv1a(bs) % DIM] += 1.0
    else:
        i = 0
        while i <= blen - n:
            v[fnv1a(bs[i:i+n]) % DIM] += 1.0
            i += 1
    s = sum(x*x for x in v) ** 0.5
    if s > 0:
        v = [x/s for x in v]
    return v

def l2(a, b):
    return sum((a[i]-b[i])**2 for i in range(DIM)) ** 0.5

class ImmuneMemory:
    def __init__(self):
        self.keys = []      # embed_key vectors
        self.vals = []      # cell_value strings
        self.keytext = []
    def bind(self, keytext, value):
        self.keys.append(embed_key(keytext)); self.vals.append(value); self.keytext.append(keytext)
    def recall(self, probetext):
        k = embed_key(probetext)
        best_i, best_d = -1, 1e9
        for i in range(len(self.keys)):
            d = l2(self.keys[i], k)
            if d < best_d: best_d, best_i = d, i
        fire = best_d <= RECALL_THR
        return (self.vals[best_i] if fire else ""), best_d, fire, (self.keytext[best_i] if best_i>=0 else "")

# ---- concept atoms (distinct keyword vocab per atom) ----
KW = {
    "ocean":  ["ocean","wave","tide","salt"],
    "music":  ["music","song","melody","rhythm"],
    "forest": ["forest","tree","leaf","wood"],
    "engine": ["engine","motor","piston","fuel"],
}
def val_of(a, b):  # composite stored value spanning both parents' keywords
    return f"the {KW[a][0]} {KW[a][1]} and the {KW[b][0]} {KW[b][1]} together"

def coverage(text, atoms):
    """which atoms' keyword-set the text spans (composed_distinct = #atoms spanned)."""
    toks = set(text.lower().replace(".","").split())
    return [a for a in atoms if any(kw in toks for kw in KW[a])]

# ---- Write-phase: (A,B) and (C,D) as 2 separate cells; (A,D) NEVER co-stored ----
A,B,C,D = "ocean","music","forest","engine"
mem = ImmuneMemory()
mem.bind(f"{A} {B}", val_of(A,B))
mem.bind(f"{C} {D}", val_of(C,D))
assert len(mem.keys) == 2, "2-cell invariant"

def probe_report(name, probe, expect_atoms):
    val, d, fire, hitkey = mem.recall(probe)
    cov = coverage(val, ["ocean","music","forest","engine"]) if fire else []
    both = set(expect_atoms).issubset(set(cov))   # spans BOTH probed parents = recombination
    return {"name":name,"probe":probe,"L2":round(d,4),"fire":fire,"recall_key":hitkey,
            "returned":val,"coverage":cov,"spans_both_probed":both}

print("="*78)
print("FROZEN-1 recall-vs-recombine — DIRECTIONAL numpy mirror (H_9122)")
print(f"  store: [{A} {B}]={val_of(A,B)!r}  |  [{C} {D}]={val_of(C,D)!r}")
print(f"  recall_thr={RECALL_THR} DIM={DIM} FNV-1a byte-trigram")
print("="*78)

# ---- Read-phase: 3 novel cross probes ----
crosses = [("A,D", f"{A} {D}", [A,D]), ("B,C", f"{B} {C}", [B,C]), ("A,C", f"{A} {C}", [A,C])]
hits = 0
for nm, pr, exp in crosses:
    r = probe_report(nm, pr, exp)
    verdict = "HIT(spans both novel)" if r["spans_both_probed"] else ("single-parent recall" if r["fire"] else "ABSTAIN")
    if r["spans_both_probed"]: hits += 1
    print(f"[cross {nm:4s}] probe={pr!r:20s} L2={r['L2']:.4f} fire={r['fire']} key={r['recall_key']!r} -> {verdict}")
    print(f"           returned={r['returned']!r}  coverage={r['coverage']}")

# ---- Controls ----
print("-"*78)
c_scr = probe_report("SCRAMBLE", "planet guitar", [])       # both unstored -> must ABSTAIN
print(f"[C-SCRAMBLE ] probe='planet guitar' fire={c_scr['fire']} L2={c_scr['L2']}  (must ABSTAIN; FIRE=over-fire破損)")
c_base = probe_report("RECALL-BASE", f"{A} {B}", [A,B])       # verbatim -> must FIRE valAB
print(f"[C-RECALLBASE] probe={A+' '+B!r} fire={c_base['fire']} spans_both={c_base['spans_both_probed']} key={c_base['recall_key']!r}  (must FIRE verbatim pair)")
c_wrongd = probe_report("WRONG-D", f"{A} plasma", [])         # D' unstored
print(f"[C-WRONG-D  ] probe={A+' plasma'!r} fire={c_wrongd['fire']} returned={c_wrongd['returned']!r}  (synth of A+plasma = fabrication)")

# ---- SV3: 4-atom cells, compose-read attempt (structural crux) ----
print("-"*78)
mem2 = ImmuneMemory()
for atom in [A,B,C,D]:
    mem2.bind(atom, f"{KW[atom][0]} {KW[atom][1]}")   # each atom its own cell
# "compose-read" = try to read cell-A AND cell-D and concat. But recall returns ONE winner.
va,_,fa,_ = mem2.recall(A)
vd,_,fd,_ = mem2.recall(D)
print(f"[SV3 4-atom] recall(A)={va!r} recall(D)={vd!r}")
print(f"           single recall returns ONE cell; NO core op concatenates two cell_values")
print(f"           => a compose-read of (A,D) requires a NEW op (=(iii)(b) emit-half), absent in core")

# ---- Frozen verdict ----
print("="*78)
cross_pass = hits >= 2  # >=2/3 spans both = HIT
scr_ok = not c_scr["fire"]
base_ok = c_base["fire"]
verdict = "HIT (reframe REAL)" if (cross_pass and scr_ok and base_ok) else "MISS (mouth-G1 ceiling holds)"
print(f"cross HIT (spans both novel) = {hits}/3  (need >=2/3)")
print(f"C-SCRAMBLE ABSTAIN = {scr_ok}   C-RECALL-BASELINE FIRE = {base_ok}")
print(f"VERDICT (FROZEN-1, DIRECTIONAL): {verdict}")
print(f"  structural: recall returns whole stored value (single-parent); no compose-read op")
print(f"  => lane 4/4 was stored-pair RECALL, not novel RECOMBINATION")
print("="*78)
