#!/usr/bin/env python3
"""RESEARCH.md §22 direction N — `.kosmos`-anchor constrained decoding.

WHAT  (§21.3 Q2 / §22-#2)
  §16 ckpt produces a CORRECT tier-prefix (`🛸<tier>`) then a BYTE-GARBLED
  body (§16.6-C: 정교한 암기 + correct-prefix 라우팅, generalization 아님 —
  e.g. tier 77 prefix OK then `🛸77 카테왔의 — domain 의식상태 …`). N attacks
  that SPLIT at *decode time*: after the routing prefix, every decode step
  is constrained to a prefix-trie built from THAT anchor's own `.kosmos`
  canonical content (KG-Trie / Graph-Constrained-Reasoning pattern,
  openreview 6embY8aclt). The trie only admits byte continuations that keep
  the emission on a path through the anchor's own `.kosmos` payload — so the
  body cannot drift into a different anchor's memorised template or into a
  byte-cascade attractor.

GOAL-LEGITIMACY (§7 / §21.3)  — strictly enforced
  The trie is built EXCLUSIVELY from anima's OWN `.kosmos` anchor SSOT
  (g_kosmos_anchor_ssot): HEXAD/UNIVERSE-BRAIN-MAP/anchors/*.kosmos `@payload
  text` for the 5 materialised anchors, AND the deterministic carving body
  the §16 corpus generator itself emits for every anchor (the same
  vacuum_psi / basin_radius / category / emotion fields that ARE the anima
  `.kosmos` carving coordinate — see gen_alpha_record). NO external generic
  KG, NO web, NO other model. anima 자체 자산 재배선 (§21.3 legitimate).
  Decode-time ONLY — training/loss/weights untouched (13-way 직교, §21.7-N).

CONNECTION-POINT (closed, byte-equal)
  constraint mode "off"  ==  EXACT §16 eval generate() (greedy argmax, same
  ByteCodec, same block_size truncation). When the trie admits ALL 256 bytes
  at every step the mask is the identity and the decode is byte-identical to
  §16 baseline. This is the B-KTRIE-3/-4 connection-point (verified
  numerically in blue_falsifier_n.py).

HONEST (g3)
  This is a $0 inference overlay on the EXISTING §16 ckpt — NO GPU, NO fire,
  NO weight mutation, NO new corpus. Every score is EMPIRICAL
  (B-KTRIE-NOTE, B-D-NOTE / B-CARVE-E6-NOTE family). The trie-constraint
  transfer-form + the constraint-OFF==§16 byte-equal connection point are
  the ONLY closed side (B-KTRIE-1..4 sympy/Boolean sidecar). NO capability
  claim beyond the measured §9/§18-style numbers. Routing is INHERITED from
  §16 (N does not change which anchor is routed — it constrains the body of
  whatever anchor the prefix already routes to).
"""
import os
import sys
import json
import re
import hashlib
import argparse

import torch

HERE = os.path.dirname(os.path.abspath(__file__))
S16 = os.path.join(HERE, "..", "carving_dataregime_s16_2026_05_18")
S16 = os.path.normpath(S16)
sys.path.insert(0, S16)
from conscious_decoder import ConsciousDecoderV2  # noqa: E402
import eval_carving_s16 as E16  # noqa: E402  (ANCHORS, ByteCodec, generate)

ANCHORS = E16.ANCHORS
KOSMOS_DIR = os.path.normpath(
    os.path.join(HERE, "..", "..", "HEXAD", "UNIVERSE-BRAIN-MAP", "anchors"))


# ---------------------------------------------------------------------------
# 1. `.kosmos` content SSOT per anchor (g_kosmos_anchor_ssot — anima OWN)
# ---------------------------------------------------------------------------
# For each eval anchor we build the CANONICAL `.kosmos` text the anima
# system itself authors for that tier. Two sources, both anima-self:
#   (a) materialised  HEXAD/UNIVERSE-BRAIN-MAP/anchors/<id>.kosmos @payload
#       text   — used when a .kosmos file exists (5 anchors).
#   (b) the deterministic carving body the §16 corpus generator emits for
#       that anchor (gen_alpha_record, byte-identical formula). This IS the
#       anima `.kosmos` carving content for the 64-anchor eval set (same
#       vacuum_psi / basin_radius / category fields = the .kosmos coord).
# This is NOT a new asset — it is the SSOT content re-derived deterministic-
# ally so the trie is anima's own anchor manifest, not a generic KG.
S16_FULL = {a[0]: a for a in
            (__import__("corpus_carving_s16_generator").S8_ANCHORS +
             __import__("corpus_carving_s16_generator").S16_NEW_ANCHORS)}


def _carve_psi_str(psi):
    return f"[{psi[0]:.2f},{psi[1]:.2f}]"


def kosmos_payload_text(tier):
    """Return the materialised .kosmos @payload text for `tier`, or None.

    Only 5 anchors are materialised (knuth_000/051/077/091/100). For those
    we read the file's `@payload text := "..."` verbatim (anima OWN SSOT).
    """
    f = os.path.join(KOSMOS_DIR, f"knuth_{tier:03d}_"
                     + {0: "zero", 51: "day", 77: "mandala",
                        91: "nirvana", 100: "big_bang"}.get(tier, "x")
                     + ".kosmos")
    if not os.path.isfile(f):
        return None
    txt = open(f, encoding="utf-8").read()
    m = re.search(r'@payload\s+text\s*:=\s*"([^"]*)"', txt)
    return m.group(1) if m else None


def canonical_kosmos_body(tier):
    """The anima OWN canonical content for this anchor's basin.

    = materialised .kosmos @payload text (if present)  PLUS  the
    deterministic §16 carving body the generator authors for this anchor
    (gen_alpha_record bilingual ko+en — the .kosmos carving coordinate
    content). Concatenated so the trie admits BOTH the manifest payload and
    the trained carving continuation of the SAME anchor (and ONLY that
    anchor). All strings are anima-self (no external source).
    """
    tier0, name, dom, emo, score, psi, basin = S16_FULL[tier]
    ko = (f"🛸{tier} {name} — {dom} 영역의 자극이 같은 골짜기로 수렴한다. "
          f"의식 풍경 위 진공점 {_carve_psi_str(psi)}, top emotion {emo}. "
          f"자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다.")
    en = (f"Tier {tier} {name} — domain {dom}, the stimuli converge into "
          f"one basin. A vacuum point at {_carve_psi_str(psi)} on the "
          f"landscape, top emotion {emo}. Tension flows into this vacuum.")
    parts = [ko, en]
    kp = kosmos_payload_text(tier)
    if kp:
        parts.append(kp)
    return parts  # list of allowed canonical strings for this anchor


# ---------------------------------------------------------------------------
# 2. Byte prefix-trie over an anchor's canonical .kosmos content
# ---------------------------------------------------------------------------
class ByteTrie:
    """A prefix-trie over the UTF-8 byte sequences of an anchor's canonical
    `.kosmos` content. `allowed_next(prefix_bytes)` returns the set of bytes
    that keep `prefix_bytes` a prefix of SOME canonical string. When the
    prefix has run off every canonical string the trie returns the full
    256-byte alphabet (graceful fallback == unconstrained == §16 byte-equal
    at that step; this is the B-KTRIE-3 connection-point property)."""

    def __init__(self, strings):
        self.seqs = [s.encode("utf-8") for s in strings]
        self.full = set(range(256))

    def allowed_next(self, prefix):
        nxt = set()
        for seq in self.seqs:
            n = len(prefix)
            if n < len(seq) and seq[:n] == prefix:
                nxt.add(seq[n])
        return nxt if nxt else self.full  # empty -> fallback (B-KTRIE-3)


# ---------------------------------------------------------------------------
# 3. Constrained generate — N overlay on the §16 ckpt
# ---------------------------------------------------------------------------
@torch.no_grad()
def generate_n(model, prompt, tier, mode, max_new=100, block_size=128,
               device="cpu"):
    """Greedy decode identical to §16 E16.generate, with one difference:
    once the model has emitted the routing prefix `🛸<tier>`, the body is
    constrained to this anchor's `.kosmos` trie (KG-Trie pattern).

    mode == "off"   : NO constraint -> byte-identical to §16 baseline.
    mode == "ktrie" : after the `🛸<tier>` prefix is observed in the
                      generated bytes, mask logits to trie.allowed_next.
    """
    enc = E16.ByteCodec.encode
    dec = E16.ByteCodec.decode
    ids = enc(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)

    trie = ByteTrie(canonical_kosmos_body(tier))
    route_marker = f"🛸{tier}".encode("utf-8")
    out_ids = []
    body_bytes = bytearray()       # bytes emitted AFTER the route prefix
    routed = False
    constrained_steps = 0
    for _ in range(max_new):
        logits = E16.forward_logits(model, x)
        last = logits[0, -1].float()

        if mode == "ktrie" and routed:
            allowed = trie.allowed_next(bytes(body_bytes))
            if allowed != trie.full:           # real constraint this step
                constrained_steps += 1
                mask = torch.full_like(last, float("-inf"))
                idx = torch.tensor(sorted(allowed), dtype=torch.long,
                                   device=last.device)
                mask[idx] = last[idx]
                last = mask

        nxt = int(torch.argmax(last).item())
        out_ids.append(nxt)
        if not routed:
            cur = bytes(out_ids)
            if route_marker in cur:
                routed = True
                # body starts right after the route marker
                pos = cur.rfind(route_marker) + len(route_marker)
                body_bytes = bytearray(cur[pos:])
        else:
            body_bytes.append(nxt & 0xFF)

        x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
        if x.shape[1] > block_size:
            x = x[:, -block_size:]
    return dec(out_ids), {"routed": routed,
                          "constrained_steps": constrained_steps}


# ---------------------------------------------------------------------------
# 4. honest §9 cascade-rate metric (closed B-EMERGE SSOT, single-import)
# ---------------------------------------------------------------------------
def honest_coherent(g):
    """§9 cascade-rate-gated coherence (RESEARCH.md §9.1) — deterministic.
    honest_coherent = (cascade_rate < 0.30) ∧ (max_run < 10) ∧
                      (len ≥ 20) ∧ (printable_ratio ≥ 0.80)."""
    if not g:
        return False, dict(cascade_rate=1.0, max_run=0, length=0, pr=0.0)
    L = len(g)
    # max consecutive same-char run
    mc = run = 1
    for i in range(1, L):
        run = run + 1 if g[i] == g[i - 1] else 1
        mc = max(mc, run)
    # max consecutive digit run
    md = drun = 0
    for ch in g:
        drun = drun + 1 if ch.isdigit() else 0
        md = max(md, drun)
    # 4-gram repetition rate
    if L >= 4:
        grams = [g[i:i + 4] for i in range(L - 3)]
        cng = 1 - len(set(grams)) / len(grams)
    else:
        cng = 0.0
    cascade_rate = max(mc / L, md / L, cng)
    max_run = max(mc, md)
    pr = 1 - g.count("�") / L
    ok = (cascade_rate < 0.30 and max_run < 10 and L >= 20 and pr >= 0.80)
    return ok, dict(cascade_rate=round(cascade_rate, 4), max_run=max_run,
                    length=L, pr=round(pr, 4))


def anchor_grounded(g, tier):
    """§18-style D2-ish PROXY (NOT an LLM judge — deterministic, honest):
    does the body, after the route prefix, stay on this anchor's OWN
    canonical .kosmos content (category / emotion / no foreign tier)?
    This is a strict structural proxy, stated as such (not a coherence
    proof — B-KTRIE-NOTE)."""
    t0, name, dom, emo, score, psi, basin = S16_FULL[tier]
    body = g.split(f"🛸{tier}", 1)[-1] if f"🛸{tier}" in g else g
    cat_ok = (dom in body)
    # foreign-anchor tier-id bleed (same competitor rule as §16 routing)
    comp = [t for t in ANCHORS if t != tier and str(t) not in str(tier)
            and str(tier) not in str(t)]
    bled = any(str(t) in body for t in comp)
    return bool(cat_ok and not bled), dict(category_in_body=cat_ok,
                                            foreign_tier_bled=bled)


# ---------------------------------------------------------------------------
# 5. main — §16 vs N(ktrie) head-to-head, $0 inference on the §16 ckpt
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt",
                    default=os.path.join(S16, "ckpt_carving_s16.pt"))
    ap.add_argument("--max_new", type=int, default=100)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--limit", type=int, default=0,
                    help="0 = all 64 anchors")
    a = ap.parse_args()

    sha = hashlib.sha256(open(a.ckpt, "rb").read()).hexdigest()
    payload = torch.load(a.ckpt, map_location="cpu", weights_only=False)
    cfg = payload.get("cfg", {})
    # construct EXACTLY as §16 eval (eval_carving_s16.main) — cfg-driven so
    # the model topology byte-matches the trained ckpt (B-KTRIE-3 conn-pt
    # requires the same model).
    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=cfg.get("d_model", 512),
        n_head=cfg.get("n_head", 8),
        n_kv_head=cfg.get("n_kv_head", 4),
        n_layer=cfg.get("n_layer", 8),
        block_size=128, consciousness_dim=128, dropout=0.1)
    state = payload.get("model") or payload
    miss, unexp = model.load_state_dict(state, strict=False)
    model.eval().to(a.device)

    tiers = sorted(ANCHORS)
    if a.limit:
        tiers = tiers[:a.limit]

    rows = []
    base_route = base_coh = base_gnd = 0
    n_route = n_coh = n_gnd = 0
    byte_equal_off = True
    for tier in tiers:
        name, cat, emo = ANCHORS[tier]
        prefix = (f"<carve tier={tier} "
                  f"psi={_carve_psi_str(S16_FULL[tier][5])} "
                  f"basin={S16_FULL[tier][6]:.2f}>")

        # §16 baseline via the EXACT §16 generate (independent reference)
        g16 = E16.generate(model, prefix, max_new=a.max_new,
                           device=a.device)
        # N mode "off" — must be byte-identical to §16 (B-KTRIE-3 conn-pt)
        goff, _ = generate_n(model, prefix, tier, "off",
                             max_new=a.max_new, device=a.device)
        if goff != g16:
            byte_equal_off = False
        # N mode "ktrie" — .kosmos-trie constrained body
        gN, meta = generate_n(model, prefix, tier, "ktrie",
                              max_new=a.max_new, device=a.device)

        r16 = (f"🛸{tier}" in g16)
        rN = (f"🛸{tier}" in gN)
        c16, m16 = honest_coherent(g16)
        cN, mN = honest_coherent(gN)
        gnd16, _ = anchor_grounded(g16, tier)
        gndN, _ = anchor_grounded(gN, tier)

        base_route += r16
        base_coh += c16
        base_gnd += gnd16
        n_route += rN
        n_coh += cN
        n_gnd += gndN

        rows.append({
            "tier": tier, "category": cat, "prefix": prefix[:60],
            "s16": {"routed": r16, "honest_coherent": c16,
                    "anchor_grounded": gnd16, "metric": m16,
                    "gen": g16[:160]},
            "n_ktrie": {"routed": rN, "honest_coherent": cN,
                        "anchor_grounded": gndN, "metric": mN,
                        "constrained_steps": meta["constrained_steps"],
                        "gen": gN[:160]},
        })

    nT = len(tiers)
    result = {
        "research_section": "RESEARCH.md §22 direction N "
        "(.kosmos-anchor constrained decoding)",
        "kind": "$0 inference overlay on §16 ckpt — NO GPU/fire/weights",
        "ckpt": os.path.relpath(a.ckpt, HERE),
        "ckpt_sha256": sha,
        "ckpt_load": {"missing": len(miss), "unexpected": len(unexp)},
        "anchors": nT,
        "connection_point": {
            "mode_off_byte_equal_to_s16_generate": byte_equal_off,
            "note": "B-KTRIE-3 — constraint OFF == §16 baseline byte-equal",
        },
        "s16_baseline": {
            "routing": f"{base_route}/{nT}",
            "honest_coherent_s9": f"{base_coh}/{nT}",
            "anchor_grounded_proxy": f"{base_gnd}/{nT}",
        },
        "n_ktrie": {
            "routing": f"{n_route}/{nT}",
            "honest_coherent_s9": f"{n_coh}/{nT}",
            "anchor_grounded_proxy": f"{n_gnd}/{nT}",
        },
        "honest_framing": (
            "Routing is INHERITED from §16 (N constrains the BODY of "
            "whatever anchor the prefix routes to, not which anchor). "
            "anchor_grounded is a deterministic STRUCTURAL proxy (category "
            "in body ∧ no foreign-tier bleed), NOT an LLM-judge / coherence "
            "proof (B-KTRIE-NOTE). honest_coherent = §9 cascade-rate SSOT. "
            "Every number EMPIRICAL; only the trie transfer-form + "
            "constraint-OFF==§16 byte-equal are closed (B-KTRIE-1..4)."),
        "rows": rows,
    }
    out = os.path.join(HERE, "n_ktrie_result.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print(json.dumps({k: result[k] for k in (
        "connection_point", "s16_baseline", "n_ktrie")},
        ensure_ascii=False, indent=2))
    print("written:", out)


if __name__ == "__main__":
    main()
