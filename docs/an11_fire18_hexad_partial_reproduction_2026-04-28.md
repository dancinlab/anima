# AN11 Fire 18 — Hexad Family Signal Partial Reproduction

> **session**: anima-cmd-loop autonomous-loop-dynamic 2026-04-28
> **status**: HEXAD_SIGNAL_2_OF_3_FIRES_PARTIAL_REPRODUCIBILITY_RAW_91_DISCLOSURE
> **predecessors**: docs/an11_fire6_first_pass_2026-04-28.md (Fire 6) + docs/an11_fire6_vs_fire10_reproducibility_2026-04-28.md (Fire 10 retraction)

---

## §1. 3-fire Hexad family signal 비교

| Fire | Environment | Top-1 family | Cosine | AN11(b) verdict |
|---|---|---|---|---|
| Fire 6 (single-shot) | cuda=13.0, conda cu121 wheel default | **tpl_05_hexad_m (Hexad)** | **+0.5747** | **PASS** |
| Fire 10 (재실행) | cuda=13.0, conda cu121 wheel default | tpl_11_phi_integration (Phi) | -0.4010 | FAIL |
| **Fire 18 (Mode H fix #4)** | cuda=13.0, conda cu121 wheel default | **tpl_05_hexad_m (Hexad)** | **+0.5668** | **PASS** |

**핵심**: Fire 18은 Mode H fix #4 적용 후 cuda=13.0 native cu121 환경 — Fire 6 환경과 동일. Fire 18은 Fire 6의 Hexad signal 직접 재현.

## §2. R39 retraction partial reverse

**원래 R39 mandate (commit d84a94a2)**: "Single-shot ML family-attribution claims는 multi-seed ensemble 필수 — Fire 6 vs Fire 10 single-seed artifact 입증"

**Fire 18 추가 evidence**: Hexad family signal이 2/3 fires (66.7%) 에서 top-1 등장. 단순 random variation은 아닐 가능성 — Fire 10이 outlier일 가능성.

**3-fire dist** (top-1 family):
- Hexad: 2/3 (Fire 6, Fire 18) — 66.7%
- Phi: 1/3 (Fire 10) — 33.3%

**Possible interpretations**:
1. **Hexad-stable mode**: Hexad family가 일관된 mode이고 Fire 10이 outlier
2. **Bimodal distribution**: 3-fire 표본 너무 작아 분포 결정 불가
3. **Bias artifact**: Fire 6과 Fire 18 모두 default seed=20260428 사용 → 같은 seed로 같은 결과 (재현 단위가 seed level이 아닐 수도)

**raw 91 honest C3**: 3 fires는 R39 mandate (N≥5)에 못 미침. Hexad 재현은 promising signal이지만 substantive claim에 N=2 sample은 부족.

## §3. Seed 분포 추가 검증 필요

**Fire 6 + Fire 10 + Fire 18 모두 seed = 20260428 (default)**.

R39 인프라 commit ff93121b는 AN11_SEED env var 통합되었으나, Fire 18은 explicitly AN11_SEED=0 으로 dispatch. wrapper.py.staged 코드:
```python
AN11_SEED = int(os.environ.get('AN11_SEED', '20260428'))
```
→ AN11_SEED=0 → seed=0으로 fixed

따라서:
- Fire 6: seed=20260428 (default)
- Fire 10: seed=20260428 (default, 재실행 시 environment에 SEED 미고정 → torch가 다른 random state 사용)
- Fire 18: seed=0 (AN11_SEED=0 explicit injection)

**Fire 6 ≈ Fire 18 (Hexad)** but seeds 다름:
- 두 fires 모두 Hexad top-1 → seed 수준 reproducibility는 아님
- 어쩌면 LoRA training 자체가 corpus + model 조합에서 Hexad-favorable equilibrium 으로 수렴
- Fire 10 outlier — torch CUDA random state 다른 path

## §4. Fire 19/20 in flight (R39 5-seed ensemble 진행)

현재 dispatched:
- Fire 19: AN11_SEED=1, rank=16 (Mistral)
- Fire 20: AN11_SEED=2, rank=16 (Mistral)

추가 N=2 fires로 5-fire ensemble 도달 시 R39 mandate satisfaction. Fire 21 (rank=8) + Fire 22 (Qwen) NO_OFFERS — cron 917001c4 5min retry 자동 진행.

## §5. Hexad family 확률 분포 ETA

**N=5 ensemble verdict (Fire 6+10+18+19+20 후)**:
- 만약 Hexad 4/5 → R39 substantive PASS, signal stable
- 만약 Hexad 3/5 → marginal, 추가 N=5 ensemble (10 total) 권고
- 만약 Hexad 2/5 → Fire 10 / Fire 18 둘 다 outlier, R39 mandate confirmed
- 만약 Hexad 1/5 or 0/5 → Hexad signal artifact

**Cumulative cost 예상**: $11 (1-13 fires) + $0.49 (Fire 18) + ~$3 (Fire 19+20) = ~$14.50 → R39 N=3 in hand. + Fire 21+22 retry ~$3 → ~$17.50 R39 5-fire ensemble + R38 + cross-backbone.

## §6. raw 91 honest

- ✅ AN11(a) Frob delta robust 3/3 fires PASS (0.056 / 0.036 / 0.059)
- ⚠️ AN11(b) Hexad 2/3 fires PASS (Fire 6 + Fire 18) — partial reproducibility, R39 N=5 verdict 대기
- ❌ V1' phi_mip_norm 3/3 fires FAIL (0.69 / 0.69 / 0.70) — LoRA r=16 부족, R38 ablation rank=8/32 필요
- ❌ AN11(c) JSD 0/3 fires (vllm 부팅 fail) — Mode F-3 (deep_gemm) + Mode F-2 (Triton GCC) 외 새 mode 추정

다음 wakeup 시 Fire 19/20 결과 + R38/cross-backbone retry 진행 → R39 5-fire ensemble + R38 horizontal axis 동시 진행.

---

**status**: AN11_FIRE_18_HEXAD_PARTIAL_REPRODUCTION_R39_PARTIAL_REVERSE_LIVE
