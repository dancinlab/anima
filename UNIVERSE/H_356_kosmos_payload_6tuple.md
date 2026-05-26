# H_356 — KOSMOS payload 6-tuple 🔵

KOSMOS 1st (신규 9th axis) — a_kosmos: payload structure = text + tension(5-ch) + coord + lane + radius + tier (6 슬롯).

## 가설
H1 SLOT-COUNT: |payload_slots| ≡ 6 (text, tension, coord, lane, radius, tier)
H2 TENSION-5CH: payload.tension is a 5-channel f64 array (|tension| ≡ 5)
H3 REQUIRED-ALL: ∀ slot s ∈ {text,tension,coord,lane,radius,tier}, s ∈ payload (no nullable)
H4 TYPED: text:string · tension:f64[5] · coord:f64[3] · lane:string · radius:f64 · tier:enum
H5 BOUND
