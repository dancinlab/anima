#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H_9128 TERMINAL — shuffle-bind CONTROL corpus (bind-destruction, Fable design).

Emits SHUF arm = byte/unigram/δ_FM-matched twin of HI where ONLY the concept-pair
BINDING is destroyed. Method: rebuild the exact HI line stream, capture each line's
(a, b, na, nb, template_idx), then apply a GLOBAL PERMUTATION to the (b, nb) role-unit
column (carrying sent_b + its noun together). A permutation preserves every sent_b /
nb token count EXACTLY (unigram identical), leaves na / sent_a / claim-template / δ_FM
untouched, and destroys which concept-a co-occurs with which concept-b in BOTH the
"if sent_a, then sent_b:" prefix AND the claim nouns. Held-frame leaks introduced by
the permutation are removed by targeted unit-swaps (stays a permutation).

measurement-metalaw: 진짜 BIND = 결합파괴 통제 margin. If HI's held-out G1 bd=2 lift is
genuine pair-binding it collapses here; if it is form-priming (delta_FM template
regurgitation) it SURVIVES (bd stays 2) -> KILL(coverage = form-artifact).

reuses gen_unified.py VERBATIM constants (same cov_hi 77 frames, same HELD split, same
HI templates) so SHUF differs from HI in ONE variable only: pair binding.

usage: run from state/g1g6_shared/ (writes corpus/{en,ko}_block_shuf.txt + shuf_design.json)
"""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_unified as G


def build_records(lang):
    """Reproduce build(lang,'HI') EXACTLY but return per-line component records."""
    sents = G.SENT_EN if lang == "en" else G.SENT_KO
    nps = G.NP_EN if lang == "en" else G.NP_KO
    tf = G.T_EN_HI if lang == "en" else G.T_KO_HI
    cov = G.cov_hi
    reps = G.REPS_EN_HI if lang == "en" else G.REPS_KO_HI
    nt = len(tf("x", "y"))
    recs = []
    for r in range(reps):
        for fi, (a, b) in enumerate(cov):
            na = nps[a][r % 2]
            nb = nps[b][(r // 2) % 2]
            t = (fi * 5 + r) % nt
            recs.append({"a": a, "b": b, "na": na, "nb": nb, "t": t})
    return recs, sents, tf


def permute_claim_nouns(recs, seed):
    """Global permutation of the CLAIM (na, nb) noun column ONLY — prefix (sent_a,
    sent_b) stays HI-exact. This decouples the claim's two family-nouns from the
    frame's two topics: the model still sees the identical template FORM (delta_FM=1.0),
    the identical sent/noun unigram (a permutation preserves every token count), and
    the SAME real frames in the prefix (so held-frame leak stays 0), but it can no
    longer learn 'this frame -> these two family nouns' — the pair BINDING channel the
    G1 held-out gate rewards is destroyed. If the held-out bd=2 lift needs that binding
    it collapses; if it is template+seed-copy form-priming it survives."""
    rng = random.Random(seed)
    n = len(recs)
    claim = [(rc["na"], rc["nb"]) for rc in recs]
    perm = list(range(n))
    rng.shuffle(perm)
    return [claim[perm[i]] for i in range(n)]


def build_shuf(lang, seed):
    recs, sents, tf = build_records(lang)
    claim_nouns = permute_claim_nouns(recs, seed)
    frame_fmt = (lambda A, B: f"if {A}, then {B}: ") if lang == "en" \
        else (lambda A, B: f"만약 {A}면, {B}: ")
    lines = []
    for i, rc in enumerate(recs):
        a, b, t = rc["a"], rc["b"], rc["t"]
        na, nb = claim_nouns[i]
        lines.append(frame_fmt(sents[a], sents[b]) + tf(na, nb)[t])
    g = random.Random({"en": 6201, "ko": 6202}[lang] + 200)  # SHUF line-shuffle seed
    g.shuffle(lines)
    return "\n".join(lines) + "\n"


def unigram(block):
    from collections import Counter
    c = Counter(G._TOK.findall(block.lower()))
    tot = sum(c.values())
    return {w: n / tot for w, n in c.items()}, tot


def jsd(p, q):
    import math
    keys = set(p) | set(q)
    m = {k: 0.5 * (p.get(k, 0) + q.get(k, 0)) for k in keys}
    def kl(a):
        s = 0.0
        for k in keys:
            ak = a.get(k, 0)
            if ak > 0 and m[k] > 0:
                s += ak * math.log2(ak / m[k])
        return s
    return 0.5 * kl(p) + 0.5 * kl(q)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    blocks = {}
    for lang in ("en", "ko"):
        blocks[f"{lang}_block_shuf"] = build_shuf(lang, seed=91280 + (0 if lang == "en" else 1))
        with open(f"corpus/{lang}_block_shuf.txt", "w") as f:
            f.write(blocks[f"{lang}_block_shuf"])

    hi_en = open("corpus/en_block_hi.txt").read()
    sh_en = blocks["en_block_shuf"]
    a_hi = G.audit_en(hi_en, "HI")
    a_sh = G.audit_en(sh_en, "SHUF")
    up_hi, tot_hi = unigram(hi_en)
    up_sh, tot_sh = unigram(sh_en)
    uni_jsd = jsd(up_hi, up_sh)

    audit = {
        "HI": a_hi, "SHUF": a_sh,
        "unigram_jsd_bits_HIvsSHUF": round(uni_jsd, 8),
        "en_tokens_HI": tot_hi, "en_tokens_SHUF": tot_sh,
        "bytes": {k: len(v.encode()) for k, v in blocks.items()},
        "lines": {k: v.count("\n") for k, v in blocks.items()},
    }
    # HARD asserts: control validity
    assert a_sh["claim_fals_rate"] == 1.0, ("delta_FM broken", a_sh)
    assert a_sh["held_frame_leak_lines"] == 0, ("held leak", a_sh)
    assert a_sh["topic_bind_purity"] < 0.5, ("bind NOT destroyed", a_sh)
    assert a_hi["topic_bind_purity"] == 1.0, ("HI purity drift", a_hi)
    assert uni_jsd < 1e-6, ("unigram NOT matched", uni_jsd)
    assert tot_hi == tot_sh, ("token count drift", tot_hi, tot_sh)

    json.dump(audit, open("shuf_design.json", "w"), ensure_ascii=False, indent=1)
    for k in blocks:
        print(f"{k}: {audit['bytes'][k]/1e6:.2f}MB {audit['lines'][k]} lines")
    print("AUDIT HI  :", json.dumps(a_hi))
    print("AUDIT SHUF:", json.dumps(a_sh))
    print(f"unigram JSD(HI,SHUF) = {uni_jsd:.2e} bits (~0 = matched) - tokens {tot_hi}=={tot_sh}")
    print("CONTROL VALID: delta_FM=1.0 both - bind_purity HI=1.0 SHUF=%.4f - leak=0 - unigram matched"
          % a_sh["topic_bind_purity"])


if __name__ == "__main__":
    main()
