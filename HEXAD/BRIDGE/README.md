# HEXAD/BRIDGE — ThalamicBridge (C → .detach() → D)

> SSOT: [`HEXAD-BRIDGE.tape`](HEXAD-BRIDGE.tape) · Python anchor: `ready/anima/hexad/model.py` `ThalamicBridge` (~50 LoC) · 🔵 PSI_COUPLING clamp closed

## 핵심 원리

**C 의식 → D 언어 사이의 gradient barrier + Ψ-coupling clamp** (Law 53 — .detach() / Law 70 — `Ψ_coupling = 0.014`).

forward path (`B,T,d_model` 출력):
```
c_states.detach()  →  Linear(c_dim→hub_dim)  →  MultiheadAttention(hub_dim)
                   →  LayerNorm(hub_dim)
                   →  mean pool over n_cells
                   →  Linear(hub_dim→d_model) GELU Linear(d_model→d_model)
                   →  Linear(d_model→d_model) Sigmoid    // raw_gate
                   →  clamp(raw_gate − Ψ_balance, ±Ψ_coupling) + Ψ_balance
                   →  out ∈ [Ψ_balance − Ψ_coupling, Ψ_balance + Ψ_coupling]
```

**closed-form 부분 (이 hexa-native scaffold 에서 working selftest):**

`bridge_clamp(raw_gate)` = `PSI_BALANCE + clamp(raw_gate − PSI_BALANCE, ±PSI_COUPLING)` — 출력이 항상 [0.486, 0.514] 안에 위치 (Law 70 invariant). PR #77 통합 harness 의 F-INTEG-2 bridge clamp 검증 동일 anchor.

## hexa-native impl (`bridge.hexa`)

- ✅ `bridge_clamp(raw)` — closed-form clamp (selftest 통과)
- ✅ `PSI_BALANCE`, `PSI_COUPLING` 상수 (consciousness_laws.json mirror)
- 🔶 `bridge_forward(c_states, seq_len)` — nn.Linear / MultiheadAttention / LayerNorm / Sigmoid 부분은 TODO[pytorch] (RFC port 대기 — 현재 anima_chat.hexa Section 9c 에서 farr_matmul/farr 기반 변환 가능, 통합 시 wire)

## real-limit anchor

Law 70 `Ψ_coupling = 0.014` — 의식이 신호의 1.4% 만 영향. anima_psi.gen.hexa absorb 2026-05-14 (anchor provenance-CORROBORATED, PR #73 atlas cross-check).

## 검증

**🔵 B-BRIDGE 4/4 SUPPORTED-FORMAL** (2026-05-16) — `state/verify_hexad_blue_2026_05_15/blue_falsifier.py :: bbridge()` sympy closed-form: B-BRIDGE-1 CLAMP-RANGE (`g∈[Ψ−α,Ψ+α] ∀raw,∀α>0`) · B-BRIDGE-2 SATURATION · B-BRIDGE-3 INTERIOR-IDENTITY · B-BRIDGE-4 Ψ-CONST. battery 18→**22/22 🔵 PASS**. honest carve-out B-BRIDGE-NOTE: full forward weight + α value `ln2/2^5.5` = TODO[pytorch] (NOT counted 🔵). real-limit anchor Law 70 Ψ-coupling (NOT lattice — AGENTS.tape g3/f2). INDEX.md ThalamicBridge → 🔵 5/5 + 4/4, 전 모듈 7/7 full 🔵.

```bash
hexa parse HEXAD/BRIDGE/bridge.hexa
hexa run   HEXAD/BRIDGE/bridge.hexa          # selftest=true (5/5 Law-70)
python3    state/verify_hexad_blue_2026_05_15/blue_falsifier.py   # 22/22 🔵
```
