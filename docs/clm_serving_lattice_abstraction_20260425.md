# CLM serving lattice abstraction L0–L5 — cell↔token bridge PoC → distributed cell consensus 한계

> **생성일**: 2026-04-25
> **부모 evidence**: `state/cell_token_bridge_proto.json` (CONDITIONAL_PASS, 3/3 fixture, drift_max=0 ≤ 2e-4 bound), `state/clm_r6_gpu_smoke_result.json` (VERIFIED, 50-step CE descent on RTX 5070).
> **scope**: CLM (Cell Language Model) **serving** 추상화 — 즉 "deterministic Lagrangian solver + cell-state ↔ token bridge" 를 production 레이어로 끌어올리는 trajectory. ALM serving (`docs/alm_serving_abstraction_layers_20260425.md`) 는 FastAPI+vLLM+LoRA stack — CLM 은 hash-only deterministic, LLM-not-in-loop, lattice runtime. 비교 대조용.
> **POLICY R4**: `.roadmap` 미수정. raw#9 hexa-only, raw#12 brutal honesty, no fabrication.
> **brutal honesty header**: CLM serving 은 ALM serving 보다 ~6 layer 미성숙. ALM 은 L0 VERIFIED-INTERNAL, CLM 은 L0 가 아직 PoC research 단계 (cell↔token bridge 가 단지 5-level coarse round-trip 검증, 실 trained lattice 위 deployment 0회).

---

<!-- [Hc_020 clm-serving-lyapunov-chaos — moved to hypotheses_candidates/Hc_020_clm_serving_lyapunov_chaos.md on 2026-05-11] -->

## §결론

| layer | bound type | CLM 위치 | ALM 비교 |
|---:|---|---|---|
| L0 | bridge PoC + smoke env | **현재 (CONDITIONAL_PASS)** | ALM 은 VERIFIED-INTERNAL (1 layer 우위) |
| L1 | deterministic Lagrangian endpoint | spec 미작성 | ALM #88 PLANNED |
| L2 | multi-cell atlas + CAP | unattempted | ALM L3 와 동일 floor |
| L3 | cell↔token hot-path | bridge spec only | ALM 은 LoRA decode live |
| L4 | Byzantine cell consensus + raw#9 충돌 | research, raw#9 conflict 미해결 | ALM L4 와 공유 + raw#9 추가 제약 |
| L5 | FLP/CAP/Shannon/Landauer/c **+ Lyapunov chaos** | 물리수학 상수 + chaos 측정 PENDING | ALM L5 의 superset |
| L∞ | Hard Problem | 측정 불가, claim 안 함 | 동일 |

**brutal honest summary**:
- CLM serving 은 ALM 보다 **명확히 한 layer 뒤쳐짐** (ALM L0 ship VERIFIED-INTERNAL vs CLM L0 PoC CONDITIONAL_PASS).
- CLM 의 **deterministic hash-only** 는 ALM 의 sample-based 대비 강한 guarantee 이지만, 그 guarantee 가 production 에서 가치 있으려면 L1 (cell-step endpoint) 가 먼저 land 되어야 함.
- **L4 의 BFT randomization 이 raw#9 LLM=none deterministic 과 충돌** — anima 가 분산 cell consensus 를 진지하게 추구하려면 raw#9 spec 자체 revision 필요.
- L5 의 **Lyapunov chaos axis** 는 ALM 에 없는 CLM 고유 한계. V_sync/V_RG Jacobian eigenvalue 측정이 안 되면 bridge drift bound 가 가장자리에서 깨질 risk 가 정량화 안 됨.
- weakest evidence link: **L1 cell-step endpoint spec 부재**. CLM 의 "serve" 는 현재 oxymoron — 서빙할 production endpoint 자체 없음. bridge PoC 만으로는 serving claim 불가.
- 단기 next step (가능한): (a) train_clm.hexa PyTorch→hexa op port 완료 → htz 단독 50-step CE descent 실측 (b) cell_step endpoint spec draft (raw#9 hash-equality 형식) (c) Lyapunov eigenvalue 측정 hook 을 V_sync/V_RG 에 추가.

POLICY R4 / raw#12 / raw#9. 본 doc 는 추상화 명문화 only — `.roadmap` / SSOT 변경 없음.
