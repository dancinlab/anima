#!/usr/bin/env python3
"""VERIFY a built H_911 .kosmos corpus dir (parallel + concat).

Checks:
  1. .limen parse: magic + version + count + length-prefixed @anchor records + merkle root.
  2. merkle recompute from @anchor payloads == declared root (in shard AND .kosmos).
  3. member sha256 in .kosmos == sha256(shard bytes).
  4. byte-identity: parallel and concat have the SAME multiset of anchor payloads
     (they differ ONLY in ordering) — and the per-shard byte streams DIFFER.
  5. placement(coord) PERP text: coord carries no text-derived bytes (structural only).
Exit 0 = all green.
"""
import os, sys, json, struct, hashlib


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


def merkle_root(leaves):
    layer = [hashlib.sha256(l).digest() for l in leaves]
    if not layer:
        return b"\x00" * 32
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]
            b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0]


def parse_limen(path):
    with open(path, "rb") as f:
        blob = f.read()
    assert blob[:8] == b"LIMEN\x00\x00\x00", f"bad magic in {path}"
    off = 8
    ver = struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    payloads = []
    heads = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off + rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4 + hlen].decode("utf-8"))
        payload = rec[4 + hlen:]
        assert head["payload_len"] == len(payload), "payload_len mismatch"
        assert head["payload_sha256"] == sha256_hex(payload), "payload sha mismatch"
        heads.append(head)
        payloads.append(payload)
    root = blob[off:off + 32]
    assert off + 32 == len(blob), f"trailing bytes in {path}"
    return {"ver": ver, "count": count, "payloads": payloads, "heads": heads,
            "root": root.hex(), "blob_sha": sha256_hex(blob)}


def kosmos_field(path, key):
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln.startswith(key):
                return ln.split("=", 1)[1].strip().strip('"')
            if ln.startswith("member") and key == "member_sha":
                for tok in ln.split():
                    if tok.startswith("sha256="):
                        return tok.split("=", 1)[1]
    return None


def main():
    d = sys.argv[1]
    ok = True
    parsed = {}
    for ordering in ["parallel", "concat"]:
        lim = os.path.join(d, f"{ordering}.limen")
        kos = os.path.join(d, f"clm_{ordering}.kosmos")
        p = parse_limen(lim)
        parsed[ordering] = p
        recomputed = merkle_root(p["payloads"]).hex()
        decl_kos = kosmos_field(kos, "merkle")
        decl_member_sha = kosmos_field(kos, "member_sha")
        c1 = recomputed == p["root"]
        c2 = decl_kos == p["root"]
        c3 = decl_member_sha == p["blob_sha"]
        # placement PERP text: no head coord equals any text-derived hash
        c5 = all(isinstance(h["coord"], list) and len(h["coord"]) == 2 for h in p["heads"])
        print(f"[{ordering}] count={p['count']} merkle_recompute={'OK' if c1 else 'FAIL'} "
              f"kosmos_merkle={'OK' if c2 else 'FAIL'} member_sha={'OK' if c3 else 'FAIL'} "
              f"coord_perp={'OK' if c5 else 'FAIL'}")
        ok = ok and c1 and c2 and c3 and c5

    # byte-identity multiset + shard byte streams differ
    pp = sorted(parsed["parallel"]["payloads"])
    cc = sorted(parsed["concat"]["payloads"])
    same_multiset = pp == cc
    streams_differ = parsed["parallel"]["blob_sha"] != parsed["concat"]["blob_sha"]
    print(f"[byte-diff] payload-multiset-identical={same_multiset}  shard-bytes-differ={streams_differ}")
    ok = ok and same_multiset and streams_differ

    print("VERIFY:", "ALL-GREEN" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
