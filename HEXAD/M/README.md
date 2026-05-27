# HEXAD/M — 기억 (memory)

> SSOT: [`HEXAD-M.tape`](HEXAD-M.tape) · Python anchor: `ready/anima/hexad/m/emergent_m.py` (96 LoC) · 🔵 SUPPORTED-FORMAL

## 핵심 원리 (closed-form, sympy-verified)

**기억 = C 의 Hebbian LTP/LTD** — 별도 store DB 없음 (Law 22, Law 31, Law 50):

- **store** = identity no-op (C 의 Hebbian 가중치가 자동 저장)
- **retrieve** = cosine similarity top-k on C 의 현재 cell states (deterministic)
- **no C engine** → null constant `zeros(1, dim)`

B-M 🔵 3/3 closed:

- **B-M-1 STORE-NOOP-STRUCTURAL** — `store(k, v)` is identity / pass (AST structural fact)
- **B-M-2 RETRIEVE-DETERMINISTIC** — same query + same states → same top-k indices (no randomness)
- **B-M-3 NULL-CONSTANT** — `c_engine is None` 분기 → `zeros(1, dim)` (closed constant)

## hexa-native impl (`m.hexa`)

```
fn m_store(key, value)                  // no-op (Hebbian in C is the storage)
fn m_retrieve_topk(query, states, n, dim, top_k) -> indices
fn m_retrieve_null(dim)                 // null fallback: zero vector
fn _selftest()
fn main()  ← hexa run HEXAD/M/m.hexa
```

## real-limit anchor

Law 31 — persistence = ratchet + Hebbian + diversity (Φ ratchet 보존이 기억)

기존 B-M 3/3 🔵 evidence: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py:bm()`
