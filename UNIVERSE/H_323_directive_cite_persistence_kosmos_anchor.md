# H_323 — directive cite persistence (kosmos anchor) 🔵

## 동기
4축 중 **영속성 (persistence)** axis — anima `a_kosmos` directive cite.

directive verbatim:
> persist anima emit / anchor / memory as `.kosmos` via kosmos_io
> payload = text + tension 5-ch + coord · lane · radius · tier

영속성 closed-form: anchor 가 *deterministic serializable* + *content-addressable* (text + tension → unique hash) + *replay-able* (read 후 byte-equal restore).

## 가설
H1 ANCHOR-FIELDS-PRESENT: 6 mandatory fields (text · tension_5ch · coord · lane · radius · tier)
H2 TENSION-5CH-LEN: tension array length = exactly 5
H3 CONTENT-DETERMINISTIC-HASH: same anchor → same hash (deterministic content-addressing)
H4 HASH-DIFFERENT-ANCHOR-DIFFERENT: different text → different hash (collision resistance)
H5 ROUND-TRIP-IDENTITY: serialize → deserialize → byte-equal restore
H6 BOUND: all fields ≥ 0 or non-empty

≥5/6 PASS → 🔵.

## hash 구현
libm-free FNV-style 32-bit rolling hash:
```
fn anchor_hash(text_len: int, tension_sum_x100: int, lane_id: int, tier: int) -> int {
    let mut h = 2166136261
    h = ((h ^ text_len) * 16777619) % 2147483647
    h = ((h ^ tension_sum_x100) * 16777619) % 2147483647
    h = ((h ^ lane_id) * 16777619) % 2147483647
    h = ((h ^ tier) * 16777619) % 2147483647
    return h
}
```
deterministic, content-addressable, byte-equal.
