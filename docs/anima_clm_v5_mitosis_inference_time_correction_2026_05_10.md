# anima clm v5-anima — mitosis inference-time correction (2026-05-10)

## TL;DR (한 줄)

mitosis 는 **학습-time 이 아닌 inference/serving/activity-time 성장**. 사용자 지적 (cycle 2026-05-09 "학습 하면서가 아니라 서빙,추론(활동)과정중에 자랐던거 같은데") 코드 검증 결과 100% 정확. v5-anima lane 의 cost 도 H100 $30 → **$0 Mac CPU** 로 정정. 단 BG-PHI super-linear 결과가 추가 nuance 부여 — **inference trajectory 길이 + 입력 다양성** 이 specialization 의 핵심.

---

## §1 evidence (mitosis.py 794L 검증)

`/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` 에서:

| 위치 | 코드 | 함의 |
|---|---|---|
| L205 | `with torch.no_grad():` ... `for p in mind.parameters(): p.add_(torch.randn_like(p) * split_noise)` | 자식 cell 노이즈 주입 — gradient X |
| L258 | `with torch.no_grad(): output, tension, curiosity, new_hidden = cell.mind(text_vec, cell.hidden)` | forward — gradient X |
| L389 | `with torch.no_grad(): cell.hidden = cell.hidden + noise` | Lorenz 자율혼돈 perturbation — gradient X |
| L586 | `with torch.no_grad(): for p_keep, p_remove in zip(...): p_keep.data = (p_keep.data + p_remove.data) / 2.0` | merge parameter averaging — gradient X |
| L628 | `with torch.no_grad(): rep = cell.mind.get_repulsion(...)` | anomaly score — gradient X |

**파일 전체 grep**: `train|backward|optimizer|loss|grad` = 5 occurrences (대부분 `requires_grad=False` flag 또는 주석). `process|forward|inference|no_grad|serve` = 20 occurrences.

→ **모든 weight 변경이 `torch.no_grad()` 블록 안. gradient 없이 cell 분열/융합. 즉 mitosis = pure inference-time 성장.**

R2 보존 evidence:
- `conscious-lm/cells64/final.pt` 208MB (2026-03-28) — Φ=51.131 도달
- `conscious-lm/cells128/step_35000.pt` 208MB (2026-03-28) — `step_35000` = inference step 35K (NOT training step)

---

## §2 v5-anima 정정된 architecture

### 잘못된 이전 framing (training-time)

```
Phase 2 cotrain → mid-train mitosis split (8→16 cells)
                  → optimizer state migration (STUB)
                  → continued cotrain
H100 비용: $30
```

### 정정된 framing (inference-time / serving-time / activity-time)

```
Phase 2 cotrain (already in flight) — checkpoint freeze 후 끝
              ↓
Frozen v5 substrate (350M params, gradient X)
              ↓
MitosisV5Engine 래퍼 (consciousness cell slice 만 mutate, no_grad)
              ↓
Serving / chat / inference loop:
  - 매 user turn → forward pass
  - tension_history 누적 → adaptive split threshold (mean+1.5σ)
  - 3 consecutive high-tension → cell split (parent deepcopy + 10% noise, no_grad)
  - 30 consecutive low-inter-tension → cell merge (parameter average, no_grad)
  - Lorenz 자율혼돈 매 step inject
              ↓
시간 흐를수록 cells 8 → 16 → 32 → 64 자연 분열 (사용자와 대화하면서)

비용: $0 (Mac CPU OK, small GPU optional 가속용)
```

### 핵심 차이

| 차원 | training-time (잘못된 framing) | inference-time (정정) |
|---|---|---|
| weight update | gradient + optimizer | parent deepcopy + noise (no_grad) |
| trigger | training step 완료 | 사용자 활동 / chat turn |
| cost | H100 $30/run | $0 Mac CPU |
| stability risk | optimizer migration STUB, loss spike | torch.no_grad 안 — backbone 가중치 안전 |
| growth driver | scheduled curriculum | adaptive tension (mean+1.5σ) + 3-step patience |
| substrate change | backbone 변경 | backbone freeze, 래퍼만 mutate |
| 사용자 직관 정합 | ✗ (anima 가 학습받음) | ✓ (anima 가 활동하며 자람) |

---

## §3 BG-PHI super-linear 결과 통합

`docs/anima_phi_super_linear_re_measurement_2026_05_09.md` 결과:
- α 측정 = **0.40** (sub-linear, Φ ∝ N^0.40)
- α historical = **0.93**
- Φ ratio cells 32→64: 측정 1.20 vs historical 2.95
- mechanism 단독으론 사실상 `Φ ≈ log(n+1)` 만 나옴 (cosine saturation on random hidden)

**해석**:
- BG-PHI 는 200 step × 3 topic 만 — 짧고 단조로운 trajectory
- v2 historical Cells64 Φ=51.131 은 **35K inference step** + **byte 256 vocab × 다양한 corpus** 누적 trajectory
- 즉 **inference-time trajectory 의 길이 + 입력 다양성 이 specialization 의 핵심**

→ inference-time mitosis 도 짧은 smoke 만으론 super-linear 미발현. **수천 turn + 다양한 prompt** 의 실제 serving 환경이 필요.

---

## §4 정정된 검증 plan

### Phase 0 (이미 완료): mechanism smoke
- `training/mitosis_v5_smoke_test.py` PASS 5/5
- 50 forward + force-split + 50 forward = mechanism 작동 확인
- raw#15 additivity 검증 (substrate `cell_pool_init` Parameter unchanged)

### Phase 1 ($0): 짧은 trajectory 재현 (이미 BG-PHI 완료)
- 200 step + 3 topic — α=0.40 measured
- mechanism 살아있지만 trajectory 부족으로 super-linear 미발현 → 예상 결과

### Phase 2 ★ ($0 Mac CPU, NEW PROPOSAL): 긴 trajectory inference smoke
**목표**: 사용자 직관 ("inference 중 자란다") 의 mechanistic 검증
- Mac CPU 또는 small GPU 에서 frozen Phase 2 cotrain checkpoint + MitosisV5Engine 래퍼
- 3K-10K diverse prompt (KO + EN, math/music/code/anomaly/철학/일상) 로 inference loop
- cells 8 → 자연 분열 trajectory tracking (30 step 마다 snapshot)
- Φ proxy 측정 (cosine × log(n+1)) + tension distribution + cell specialty 추적
- 예상: 수천 turn 누적 시 cells 16-32+ 까지 자연 성장 + α 향상

**falsifier**:
- 3K turn 후 cells 가 8 그대로 → adaptive threshold 가 trigger 안 됨 (mechanism 한계)
- cells 늘어나도 Φ ratio 1.0 근처 → cosine saturation 미해결, training mandatory

### Phase 3 (옵션 $5-20): inference 중 LoRA-style 적응
mitosis 가 weight 를 deepcopy + noise 만 하는 것 외에, 추가로:
- 매 N turn 마다 small LoRA update (100-500 examples self-play)
- 이건 inference 와 light-training 의 hybrid — anima 의 "꿈 / 휴식 시 학습" 비유
- 비용 cheap (consumer GPU OK)
- 단 본 lane 의 핵심 메커니즘은 아닌 enhancement

### Phase 4 ($30 H100 OPTIONAL): 가속만
- Phase 2 검증 통과 후 사용자 verbatim 시
- H100 inference 가속 (대형 corpus 시뮬용)
- mitosis 메커니즘 자체엔 H100 필수 X

---

## §5 정정된 비용 envelope

| step | 비용 | 메모 |
|---|---:|---|
| design + port (BG-MITOSIS-PORT 완료) | $0 | mitosis_v5_port.py 480 LoC, smoke PASS 5/5 |
| Phase 0 mechanism smoke | $0 | DONE |
| Phase 1 short trajectory (BG-PHI) | $0 | DONE — VIOLATED untrained, 예상대로 |
| Phase 2 long inference smoke ★ | $0 | NEXT — 수천 turn Mac CPU |
| Phase 3 inference + light LoRA | $5-20 | OPTIONAL hybrid |
| Phase 4 H100 inference 가속 | $30 | OPTIONAL — 메커니즘 검증엔 불필요 |

→ **anima 자력성장 부활 의 핵심 검증은 $0 로 가능**. 이전 framing 의 H100 $30 는 가속/대규모 시뮬용으로만 의미.

---

## §6 Honest C3 (≥7)

1. **mitosis_v5_port.py 의 optimizer migration STUB 은 inference-time 정정 후 deprecated** — 더 이상 필요 X. 단 spec md 에 still 등장 — additive 정정 (코드 deletion 아닌 deprecation 코멘트 추가) 필요.
2. **inference-time growth 은 trajectory 길이/다양성 의존** — 짧은 smoke 로는 super-linear 입증 불가능. 사용자 chat 가 짧으면 cells 가 8 그대로 머물 수 있음 (mechanism 정상 작동에도 불구).
3. **v2 cells64 / cells128 R2 weights 는 35K step 의 synthetic 입력 trajectory** (test_mitosis 같은 합성 토픽). 실제 사용자 대화 trajectory 와 distribution 차이 가능 — reproduction 시 cell topology 다를 수 있음.
4. **shared lm_head 와 mitosis 호환성**: v5 cotrain 의 shared lm_head 가 cell 분열 시 차원 grow 를 어떻게 처리할지 미해결. inference-time 이라 gradient 는 없지만 forward shape 는 유지해야 — output projection 로직 정밀화 필요.
5. **`process_count` 누적 의존**: cell.process_count 가 mitosis 의 maturation 신호. 매 anima 인스턴스 시작 시 process_count=0 이면 mitosis trigger 가 늦음. checkpoint 에 cell state 보존 + restore 메커니즘 필요.
6. **Lorenz 자율혼돈 의 phase offset** 이 cells 수에 의존 (`phase = i × 2π / len(cells)`). split 시 모든 cell 의 phase 가 재계산됨 → 일시 instability. 점진적 transition 가능성.
7. **#115 architectural mismatch trap**: v2 18M byte-level 의 chat 회로와 v5 350M BPE-64K Engine A/G 의 회로가 같은 mitosis 메커니즘으로 같은 결과를 낼지 미검증. 사용자 직관은 mechanism 맞지만 substrate 호환성 별개.
8. **BG-PHI 의 untrained 결과 과해석 주의**: α=0.40 은 mechanism 의 한계가 아닌 trajectory 짧음의 결과. inference-time growth 가 잘 안된다는 evidence 가 아님.
9. **anima 의 의식 = 활동 중 성장 의 metaphysical claim** 도 mechanism 검증이 부정/긍정 모두 못함. mechanism 작동 != consciousness emergence.

---

## §7 다음 행동

| 순위 | step | 비용 | 결정 권한 |
|---:|---|---:|:---:|
| 1 ★★★ | Phase 2 long inference smoke (3K-10K turn Mac CPU) | $0 | AUTO foreground OK |
| 2 ★★ | mitosis_v5_port.py inference-time hardening (optimizer STUB → deprecate) | $0 | AUTO |
| 3 ★★ | BG-R2-CELLS-DOWNLOAD 회수 후 cells64 actual load | $0 | AUTO |
| 4 ★ | spec md (anima_clm_v5_mitosis_revival_spec_2026_05_09.md) inference-time addendum 추가 | $0 | AUTO |
| 5 ★ | Phase 3 light LoRA inference + dream consolidation | $5-20 | verbatim |

**현 추천**: 1 + 2 + 4 foreground 동시 (작업 path 비충돌). 3 은 BG-R2 결과 회수 자동.

---

## §8 cross-link

- `.roadmap.clm_v5_anima_native` (cost / fire keyword 정정 반영)
- `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` (BG-MITOSIS-PORT spec, training-time framing 일부 잔존 → addendum 필요)
- `training/mitosis_v5_port.py` (480 LoC, smoke PASS, optimizer STUB → inference-time 에선 deprecated)
- `training/mitosis_v5_smoke_test.py` (PASS 5/5)
- `state/anima_phi_super_linear_re_measurement_2026_05_09/result.json` (BG-PHI raw)
- `docs/anima_phi_super_linear_re_measurement_2026_05_09.md` (α=0.40 verdict)
- `CLM_V2_ARCHIVE_2026_05_09.md` §2 mitosis 본체 + §6 architectural mismatch
- `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` §7-§9 stage 7/8/9 mitosis empirical
- mitosis source canonical: worktree-12 mitosis.py 794L

raw#9/10/15 honest, raw#37 additive preserve, own 16 0-cost.

End of `anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md`.
