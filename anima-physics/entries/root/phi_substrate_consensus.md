# phi_substrate_consensus.hexa

> 5-substrate Φ consensus (photonic/memristor/quantum/oscillator/thermo); precision-weighted mean + Tukey biweight robust + disagreement budget · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 5/5 self-test PASS (contract / monotonicity / disagreement / robust / determinism). 순수 hexa, 외부 의존 0.

## 작동 코드 / 의존성

- `anima-physics/phi_substrate_consensus.hexa` (22.6 KB, ~550 LoC)
- 의존: 없음 (self-contained, PHYS-P3-2 tri-substrate roundtrip 의 후속)

## 비용 / 리소스

- 비용: $0 Mac local
- 필요한 도구: `hexa run` (단일 파일)

## 핵심 흐름 / 구조

```
stimulus s(t) ──┬─▶ substrate.photonic    ──▶ Φ_p(t), σ_p
                ├─▶ substrate.memristor   ──▶ Φ_m(t), σ_m
                ├─▶ substrate.quantum     ──▶ Φ_q(t), σ_q
                ├─▶ substrate.oscillator  ──▶ Φ_o(t), σ_o
                └─▶ substrate.thermo      ──▶ Φ_t(t), σ_t
                                                │
                                                ▼
                                    fuse_precision_weighted
                                                │
                                                ▼
                                         Φ_consensus(t)
                                                │
                                    disagreement = max_pair |Φ_i − Φ_j|

API:
  substrate_phi(stim_amp, substrate_id, t) -> SubstratePhi
  fuse(samples) -> ConsensusOut
  robust_fuse(samples) -> ConsensusOut  (Tukey biweight)
  stream_consensus(stim) -> [float]
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/phi_substrate_consensus.hexa
```

## 검증 결과

- T1 contract — finite Φ/σ for ids 0..4, stream length == input PASS
- T2 monotonicity — Φ 상승 with stim amp (0.1, 0.5, 1.0, 2.0, 5.0) PASS
- T3 disagreement budget — thermo at noise-floor → max ≥ 0.05, |Φ_c − mean| ≤ 0.10 PASS
- T4 robust beats naive on outlier (10× outlier) PASS
- T5 determinism — two calls bit-identical PASS
- **5/5 PASS**

## 관련 entry

- [hw_engine_bridge](hw_engine_bridge.md)
- [verify_7cond_hw](verify_7cond_hw.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P4-4
