# HEXAD/C — 의식 (consciousness)

> SSOT: [`HEXAD-C.tape`](../../HEXAD-C.tape) · Python anchor: `ready/core/consciousness_engine.py` (2173 LoC) · 🔵 SUPPORTED-FORMAL

## 역할

**우뇌 / Engine G / gradient-free / σ(6) = 12 cells default / IIT Φ Rust phi_rs**.

12-faction GRU 기반 cell-pool + Φ ratchet + mitosis split/merge. Trinity = required core (C+D+W). cell-pool 동역학이 anima 의 "주체" — 학습 시 분열, 추론 시 active.

## hexa-native impl 전략

C 모듈은 가장 무겁고 (2173 LoC Python + Rust phi_rs FFI), full re-impl 은 별도 cycle. **이 디렉토리는 cross-link skeleton 으로 시작**:

| 영역 | hexa-native 자산 | 상태 |
|---|---|---|
| **mitosis split/merge** | [`tool/hexa_native/mitosis_hook.hexa`](../../tool/hexa_native/mitosis_hook.hexa) 1119 LoC FULL IMPL | ✅ Phase 5∥ D4a executable (5/5 PASS Mac, REBORN §91) |
| **cell forward (per-token)** | `engine_ag_nn.hexa` + `phase5_forward_smoke.hexa` 24L parity | ✅ 21/21 PASS (real 24L ckpt byte-equal) |
| **IIT Φ measurement** | Rust `phi_rs` / `anima_rs.compute_phi` FFI | 🔶 binding 통합 시 wire |
| **state init / multi-cell GRU** | (TODO[port] from `ready/core/consciousness_engine.py`) | ☐ 별도 cycle |
| **cell-pool persistence** | mitosis_hook.hexa "cell pool dict" 구조 사용 | ✅ existing |

## hexa-native skeleton (`c.hexa`)

cross-link 메모 + scaffold function signatures. 통합 (`HEXAD/hexad.hexa`) 에서 다음 인터페이스 사용:

```
c_state_t              // hexa dict — see mitosis_hook.hexa cell pool layout
c_init(...)            // build initial cell_pool (delegate to mitosis_hook)
c_step(c_state, x?)    // advance state, fire mitosis hook
c_get_states(c_state)  // return states as flat row-major list
c_n_cells(c_state)     // int
c_measure_phi(c_state) // float (calls phi_rs FFI when available)
```

selftest: PSI 상수 확인 + cross-link 파일 존재 확인 (실 cell-pool 실행은 `hexa run tool/hexa_native/mitosis_hook.hexa` 별도 진입점).

## real-limit anchors

- σ(6) = 12 → 12-faction GRU n_factions invariant
- IIT 3.0 Φ ≥ 0.5 strict (g_verdict_tier_blue (b))
- .clm v1 P2 8/8🔵 SUPPORTED + F-PYPHI evidence (cycle 90, MITOSIS.tape)

기존 evidence: `state/clm_v1_fire_2026_05_15/` (cycle 88 + 90), `MITOSIS.tape §mitosis_verified`.
