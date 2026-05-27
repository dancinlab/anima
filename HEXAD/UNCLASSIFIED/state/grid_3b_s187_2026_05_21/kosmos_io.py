"""kosmos_io.py — minimal .kosmos anchor writer + retrieval for V3 substrate.

Per HEXAD_NATIVE_V3.md § 0.5: ConsciousDecoderV3 emit 시 자동으로
.kosmos anchor 생성 (text + tension 5-ch payload + coord + lane + tier).

This module is intentionally pure-python (no torch in the hot path) so it
can run on-pod inside the train script without extra deps.

Anchor file format (kosmos/1.1):
    #!/usr/bin/env kosmos
    @anchor <name> := "<title>" :: kosmos-anchor [tier=<tier> active]
      profile      = "anima-consciousness-carving"
      knuth_tier   = <tier>
      category     = "<category>"
      top_emotion  = "<emotion>"
      coord        = [<x>, <y>]
      lane         = "<lane_id>"
      radius       = <radius>
      @payload text    := "<text>"
      @payload tension := {
        concept       = <float>,
        context       = <float>,
        meaning       = <float>,
        authenticity  = <float>,
        sender        = <float>,
      }
      closed_anchor = "V3-emit"

8-factor → 5-channel mapping (HEXAD_NATIVE_V3 § 0.5 table):
    relevance + coherence       -> concept
    info_gap                    -> context
    curiosity + originality     -> meaning
    pain + balance              -> authenticity
    dynamics                    -> sender
"""
import json
import math
import os
import re
import time
from typing import List, Dict, Any, Optional, Tuple


# ─── 8-factor → 5-channel mapping ────────────────────────────────────────────

def map_8factor_to_5channel(factors: Dict[str, float]) -> Dict[str, float]:
    """Map an 8-factor anima_participant motivation snapshot to the
    TENSION-LINK 5-channel fingerprint."""
    def g(k, default=0.0):
        return float(factors.get(k, default))
    return dict(
        concept      = (g('relevance') + g('coherence')) / 2.0,
        context      = g('info_gap'),
        meaning      = (g('curiosity') + g('originality')) / 2.0,
        authenticity = (g('pain') + g('balance')) / 2.0,
        sender       = g('dynamics'),
    )


def tension_5ch_to_embedding(tension_5ch: List[float],
                               embed_dim: int = 32,
                               seed: int = 1337) -> List[float]:
    """Project a 5-channel tension vector to a dense embed_dim vector via a
    fixed seeded random projection (no torch dep)."""
    import random
    rng = random.Random(seed)
    # 5 x embed_dim projection matrix
    W = [[rng.gauss(0, 1.0 / math.sqrt(5)) for _ in range(embed_dim)]
         for _ in range(5)]
    out = [0.0] * embed_dim
    for k in range(5):
        for d in range(embed_dim):
            out[d] += tension_5ch[k] * W[k][d]
    return out


# ─── Anchor creation ────────────────────────────────────────────────────────

def _escape_kosmos_string(s: str) -> str:
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    s = s.replace('\n', '\\n').replace('\r', '')
    return s


def create_anchor(out_dir: str,
                  name: str,
                  title: str,
                  coord: Tuple[float, float],
                  lane: str,
                  radius: float,
                  tier: int,
                  category: str,
                  top_emotion: str,
                  text: str,
                  tension_5ch: List[float],
                  closed_anchor: str = "V3-emit",
                  cross_link: Optional[str] = None,
                  ) -> str:
    """Write a .kosmos anchor to out_dir/<name>.kosmos. Returns absolute path."""
    if len(tension_5ch) != 5:
        raise ValueError(f"tension_5ch must have len=5, got {len(tension_5ch)}")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.kosmos")
    text_esc = _escape_kosmos_string(text)
    lines = []
    lines.append("#!/usr/bin/env kosmos")
    lines.append(f"# {name}.kosmos — V3 substrate-native emission anchor")
    lines.append(f"# Tier 🛸{tier} — {category}, top emotion {top_emotion}.")
    lines.append("")
    lines.append(f'@anchor {name} := "{title}" :: kosmos-anchor [tier={tier} active]')
    lines.append('  profile      = "anima-consciousness-carving"')
    lines.append(f'  knuth_tier   = {tier}')
    lines.append(f'  category     = "{category}"')
    lines.append(f'  top_emotion  = "{top_emotion}"')
    lines.append(f'  coord        = [{coord[0]:.4f}, {coord[1]:.4f}]')
    lines.append(f'  lane         = "{lane}"')
    lines.append(f'  radius       = {radius:.4f}')
    lines.append("")
    lines.append(f'  @payload text    := "{text_esc}"')
    lines.append('  @payload tension := {')
    lines.append(f'    concept       = {tension_5ch[0]:.6f},')
    lines.append(f'    context       = {tension_5ch[1]:.6f},')
    lines.append(f'    meaning       = {tension_5ch[2]:.6f},')
    lines.append(f'    authenticity  = {tension_5ch[3]:.6f},')
    lines.append(f'    sender        = {tension_5ch[4]:.6f},')
    lines.append('  }')
    lines.append('  @payload image   := pending "V3-emit text+tension only"')
    lines.append('  @payload audio   := pending "V3-emit text+tension only"')
    lines.append('  @payload video   := pending "V3-emit text+tension only"')
    lines.append("")
    lines.append(f'  closed_anchor = "{closed_anchor}"')
    if cross_link:
        lines.append(f'  cross_link    = "{cross_link}"')
    lines.append('  emitted_at    = "' + time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                       time.gmtime()) + '"')
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")
    return path


def emit_anchor_from_v3(out_dir: str,
                         name: str,
                         text: str,
                         tension_5ch: List[float],
                         mitosis_cell_id: int = 0,
                         tier: int = 0,
                         category: str = "v3_emission",
                         top_emotion: str = "neutral",
                         phi: float = 0.0,
                         radius: float = 0.15,
                         ) -> str:
    """High-level emit: takes a V3 forward result and writes the anchor.

    coord = [phi, mean(tension_5ch)] as Ψ-space placeholder.
    lane  = f"cell_{mitosis_cell_id}".
    """
    mean_t = sum(tension_5ch) / max(1, len(tension_5ch))
    coord = (phi, mean_t)
    lane = f"cell_{mitosis_cell_id}"
    title = f"v3-emit {name} (tier {tier})"
    return create_anchor(
        out_dir=out_dir, name=name, title=title, coord=coord, lane=lane,
        radius=radius, tier=tier, category=category, top_emotion=top_emotion,
        text=text, tension_5ch=tension_5ch,
        closed_anchor="V3-emit-auto",
    )


# ─── Anchor loader ──────────────────────────────────────────────────────────

ANCHOR_FIELD_PATTERN = re.compile(r'^\s*(\w+)\s*=\s*(.+?)\s*$')


def _parse_value(v: str):
    v = v.strip()
    # string literal
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    # list literal [a, b]
    if v.startswith('[') and v.endswith(']'):
        inner = v[1:-1]
        parts = [p.strip() for p in inner.split(',')]
        out = []
        for p in parts:
            try:
                out.append(float(p))
            except ValueError:
                out.append(p)
        return out
    # try int / float
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def load_anchors(dir_path: str) -> List[Dict[str, Any]]:
    """Load all .kosmos files in dir_path. Returns list of dicts with parsed
    placement fields + text payload + tension 5-channel."""
    if not os.path.isdir(dir_path):
        return []
    anchors = []
    for fname in sorted(os.listdir(dir_path)):
        if not fname.endswith('.kosmos'):
            continue
        path = os.path.join(dir_path, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        rec = {
            'path': path,
            'name': fname.replace('.kosmos', ''),
            'fields': {},
            'text_payload': None,
            'tension_5ch': None,
        }
        # parse placement fields (lines like   key = value)
        in_tension = False
        tension_buf = {}
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('@payload tension'):
                in_tension = '{' in stripped
                continue
            if in_tension:
                if stripped.startswith('}'):
                    in_tension = False
                    continue
                m = ANCHOR_FIELD_PATTERN.match(line)
                if m:
                    k, v = m.group(1), m.group(2).rstrip(',')
                    try:
                        tension_buf[k] = float(v.rstrip(','))
                    except ValueError:
                        pass
                continue
            if stripped.startswith('@payload text'):
                # text payload — extract inline string after := "..."
                m = re.match(r'.*:=\s*"(.*)"\s*$', line)
                if m:
                    rec['text_payload'] = m.group(1)
                continue
            if stripped.startswith('@'):
                continue
            m = ANCHOR_FIELD_PATTERN.match(line)
            if m:
                k, v = m.group(1), m.group(2)
                rec['fields'][k] = _parse_value(v)
        if tension_buf:
            rec['tension_5ch'] = [
                tension_buf.get('concept', 0.0),
                tension_buf.get('context', 0.0),
                tension_buf.get('meaning', 0.0),
                tension_buf.get('authenticity', 0.0),
                tension_buf.get('sender', 0.0),
            ]
        anchors.append(rec)
    return anchors


# ─── Retrieval ──────────────────────────────────────────────────────────────

def _cosine(a: List[float], b: List[float]) -> float:
    na = math.sqrt(sum(x * x for x in a)) + 1e-10
    nb = math.sqrt(sum(x * x for x in b)) + 1e-10
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def retrieve(query_tension_5ch: List[float],
             anchors: List[Dict[str, Any]],
             top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
    """Cosine-similarity retrieval over anchors with tension_5ch payload."""
    scored = []
    for a in anchors:
        t = a.get('tension_5ch')
        if t is None:
            continue
        sim = _cosine(query_tension_5ch, t)
        scored.append((a, sim))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_k]


# ─── self-test ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        # Test 1: 8-factor → 5-ch
        f = dict(relevance=0.8, coherence=0.6, info_gap=0.4,
                 curiosity=0.7, originality=0.5, pain=0.2, balance=0.9,
                 dynamics=0.3)
        t5 = map_8factor_to_5channel(f)
        print(f"5-channel: {t5}")
        assert abs(t5['concept'] - 0.7) < 1e-6
        assert abs(t5['sender'] - 0.3) < 1e-6

        # Test 2: create anchor
        path = create_anchor(
            tmp, "test_001",
            title="Test anchor",
            coord=(0.5, 0.5), lane="cell_0", radius=0.1, tier=1,
            category="test", top_emotion="curious",
            text="this is the first v3-emit test", tension_5ch=[0.1, 0.2, 0.3, 0.4, 0.5],
        )
        print(f"Created: {path}")
        assert os.path.isfile(path)
        with open(path) as fh:
            content = fh.read()
        assert '@anchor test_001' in content
        assert 'tension :=' in content

        # Test 3: emit_anchor_from_v3
        path2 = emit_anchor_from_v3(
            tmp, "test_002", "second emit",
            [0.5, 0.5, 0.5, 0.5, 0.5], mitosis_cell_id=3, tier=42, phi=0.7,
        )
        assert os.path.isfile(path2)

        # Test 4: load + retrieve
        anchors = load_anchors(tmp)
        print(f"Loaded {len(anchors)} anchors")
        assert len(anchors) == 2
        for a in anchors:
            assert a['tension_5ch'] is not None, f"missing tension in {a['name']}"
            assert len(a['tension_5ch']) == 5

        # Retrieval
        q = [0.5, 0.5, 0.5, 0.5, 0.5]
        top = retrieve(q, anchors, top_k=2)
        print(f"Retrieval top {len(top)}:")
        for a, sim in top:
            print(f"  {a['name']}  sim={sim:.4f}")
        assert top[0][0]['name'] == 'test_002', f"expected test_002 first, got {top[0][0]['name']}"

        # Test 5: tension to embedding
        emb = tension_5ch_to_embedding([0.1, 0.2, 0.3, 0.4, 0.5], embed_dim=32)
        print(f"Embedding dim: {len(emb)}")
        assert len(emb) == 32

        print("All kosmos_io tests passed.")
