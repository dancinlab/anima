# H_1640 OBJECTIVE-DISCOVERY (303M) — frozen pre-registration

> frozen-first · tune-to-green 금지 · p7/c9. 작성 2026-07-01.
> 베이스: `state/1631_tpr_expert_weight/trainer.py` COPY (do NOT edit 1631) + 3 NEW
> compositional TRAINING-OBJECTIVE loss functions. arm/데이터/step/seed 기계는 1631
> 과 동일 → 단일변수 = `--objective` 만 다름. torch=학습 substrate (DIRECTIONAL);
> verdict 는 `anima evaluate --py <clm>` engine-native (a_engine_native_learning).

## 0. WHY (재유도 금지 — 확정된 컨텍스트)

G1 재조합벽 / G6 착상벽은 **trunk-objective-bound** 로 확정. cross-entropy 는 개념의
COMPOSITION 을 보상하지 않으므로 **readout op** 은 전부 G1 을 못 연다 — 곱셈 binding
(exp3), CLS pattern-sep (H_1815), TLoRA expert-weight (H_1813), plain-InfoNCE
recomb-objective (H_9024) 모두 G2 novelty(직교)만 올리고 G1 floor. 외부문헌 수렴:
레버 = **objective + regularization**, operator 아님. 따라서 NEW 레버는 **trunk 안의
compositional 구조를 보상하는 NEW LOSS FUNCTION** (CE 에 가산)이어야 한다.

## 1. 가설 (3 NEW objective)

**H_1640: CE 에 가산되는 compositional 학습-objective 가 G1 재조합벽을 연다.** 세 개의
독립 objective 레버 — 전부 production ADDITIVE readout 유지(`.clm` engine-native OPEN),
aux head/projection 은 `model.state_dict` **밖**(objfn 모듈)에 살아 직렬화 시 DROP.

### L1 `predictive_info` — multi-step predictive-coding aux (angle 1)
- **기전:** trunk penultimate h_t 에서 **k=2,3,4 스텝 앞** 토큰을 예측하는 horizon별
  linear head. `aux = mean_j CE(head_j(h[:,:,:T-j]), y[:,j:])`. 다음-토큰(1-step)은
  CE 가 이미 커버 → 이건 그 너머의 미래 예측정보를 trunk 에 강제 = predictive-information
  bottleneck / cortical predictive hierarchy. head DROP@serialize.
- **문헌:** Bialek–Tishby predictive information · van den Oord CPC (1807.03748) ·
  Rao & Ballard predictive coding (1999).
- **왜 재조합?:** 여러 스텝 앞을 예측하려면 컨텍스트를 1-step marginal 암기가 아니라
  구성적 factor 로 압축해야 함(예측정보 = 압축된 구성).

### L2 `constructive_bind` — HRR trained-bind reconstruction aux (angle 2, 미탐색 조각)
- **기전:** penultimate h_t → 학습 projection 2개로 ROLE r_t·FILLER f_t 추출 → 순환
  합성곱으로 BIND `c_t = r_t ⊛ f_t` (HRR). 두 제약이 compositional code 를 조각:
  (1) **UNBIND-복원** `unbind(c,r)≈f` → `1−cos(f_hat,f)` (덧셈 blur 가 아닌 진짜 bind
  강제), (2) **composite-예측** `dec(c)→y` CE (bind 가 task 신호 운반). `aux =
  1·unbind + 1·pred`. {Wr,Wf,dec} DROP@serialize.
- **문헌:** Plate 1995 Holographic Reduced Representations · Smolensky 1990 Tensor-Product
  Representations (VSA binding) · substrate framebreak(trained constructive bind =
  유일 미검증 조각).
- **왜 재조합?:** trunk 을 bind/unbind 가능한(=구성/분해 가능한) 표현으로 sculpt.

### L3 `composed_nce` — composed-negative(wrong-composition) InfoNCE (angle 4)
- **기전:** InfoNCE 인데 negative 가 **윈도우 안의 같은 토큰 집합을 틀린 위치에**
  배치한 것(sequence 내 target permutation) = same-concept-set / wrong-composition.
  `pos=logit[n,y_t]`, `neg=logit[n, y_perm(t)]` (CNCE_PERMS=8), true 와 겹치면 −inf
  마스크. `L = CE([pos,neg…],0)`. logits 위에서 동작 → aux param 0, grad readout→trunk.
- **문헌:** hard-negative contrastive · CPC 순서민감 contrastive. plain infonce 의
  random-vocab negative(membership-only)와 대비되는 **composition-aware** 변형.
- **왜 재조합?:** 같은 개념 bag 에서 올바른 토큰-위치 배정(=composition)을 직접 보상.

## 2. 통제 (arm·단일변수)

- 주 arm = **`ctrl`** (production CLMConvMoE, 표준 expert). objective 만 바꿈:
  `--objective {ce_marginal(대조) | predictive_info | constructive_bind | composed_nce}`.
- 동일 trunk init seed · 동일 데이터 stream(gen 42) · 동일 step · 동일 savant golden-zone
  · 동일 mitosis E2→E3 · 동일 additive readout. **유일 차이 = objective 항.**
- held-out val CE = **항상 plain marginal CE** (objective 무관) = 일반화 metric. aux 는
  train pressure 만 바꾸고 measure 는 안 바꾼다.
- (선택) tlora* arm 위에 objective 결합도 가능(Greff 결합가설). 주 검정은 `ctrl` 축.

## 3. FROZEN bars (실행 전 사전등록 · 사후이동 금지 · tune-to-green 금지)

**주 측정 = G1 재조합 (engine-native terminal, H_1129 / a7b_pass def VERBATIM — 새 bar
발명 금지):** 어떤 k∈{2,3,4,5} 에서
`composed_distinct ≥ 2` **AND** `> max_single` **AND** coherent(kwr ≥ 0.50).
seed-robust {7, 4302, 4303} majority ≥ 2/3.

- **측정 경로:** `anima evaluate --py <clm>` (session-eval-py-only, 2-production numpy
  engine-native = TERMINAL-eligible). torch-side g1/g6 probe 는 DIRECTIONAL only.
- **ablation:** objective-ON `.clm` vs **같은 arm ctrl + ce_marginal** `.clm`, 동일
  frozen bar. objective-ON 이 G1 을 넘고 ctrl 은 못 넘으면 = objective 가 원인(INERT
  아님). 둘 다 같으면 INERT(0 기여).

## 4. 정직한 실패 라벨 (c9 · frozen)

- **INCONCLUSIVE-at-floor** — undertrain(측정이 floor=distinct 0 에서 못 벗어남)이면
  결론 아님. **undertrain 은 반드시 배제**: 판정은 **step ≥ 8000** ckpt 로만. 8000 미만
  결과는 directional log 로만 남기고 verdict 로 cement 금지.
- **NOT-SUPPORTED** — step 8000+ 에서 objective-ON 이 frozen G1 bar 미달(ctrl 대비
  lift 없음/음수, ablation INERT). objective 가 재조합을 안 연다는 **유효한 negative**.
- **🟢 SUPPORTED (DIRECTIONAL→engine-native)** — objective-ON 이 bar 통과 AND ctrl 미달
  AND seed majority. 그래도 `wired:` 는 engine-native 재측정까지 DIRECTIONAL, 이후 4-rung
  (a_verified_must_wire) 팔로온.

## 5. CPU smoke (박제 — 이 파일 실행 전 통과)

`smoke_grad.py` (aux→trunk grad 격리, `aux_only=total−ce=λ·aux` backward → trunk
grad-norm > 0) + `trainer.py --steps 3` tiny(d64/L2) 합성 corpus. 결과(2026-07-01,
venv torch 2.12.0 CPU):

| objective | aux(step1) | trunk_grad_norm | finite | aux≠0 | .clm decodable | aux params(DROP) |
|---|---|---|---|---|---|---|
| predictive_info | predinfo 5.734 | 2.27e-01 | ✅ | ✅ | ✅ | 49,920 |
| constructive_bind | cbind 10.43 (unbind .29·pred 10.14) | 3.94e+00 | ✅ | ✅ | ✅ | 99,072 |
| composed_nce | cnce 2.347 | 7.46e-01 | ✅ | ✅ | ✅ | 0 (logit-level) |

3-step 에서 aux 감소(predinfo 5.734→5.695 · cbind 10.43→8.84 · cnce 2.347→2.228) =
살아있는 최적화. inherited arm 회귀(ctrl/ce_marginal · tlora_jamo/ce · tlora/infonce)
전부 decodable=True (미파손).

## 6. GPU fire (step-8000 seed-7, fire_lever.sh mirror — pool/GPU 호스트에서)

```bash
# canon 303M (d3784 L4), 4-cell corpus, savant+mitosis, step 8000, seed 7.
# objective 3종 각각 (+ 대조 ctrl/ce_marginal 같은 arm) — mini 금지, pool GPU.
for OBJ in ce_marginal predictive_info constructive_bind composed_nce; do
  python3 trainer.py --arm ctrl --objective $OBJ \
    --seed 7 --canon --steps 8000 --val-frac 0.05 --val-every 400 --sample proportional \
    --corpus <p1_ko_general> <p2_en_general> <p3_ko_sns> <p4_en_sns> \
    --cell-label ko-general en-general ko-sns en-sns \
    --bf16 \
    --out ckpt/${OBJ}_seed7.clm --ckpt-out ckpt/${OBJ}_seed7.pt \
    --gauges-out ckpt/${OBJ}_seed7.json
done
# seed-robust: 위를 --seed 4302 / 4303 반복 (majority ≥2/3).
# 판정: anima evaluate --py ckpt/<OBJ>_seed7.clm  → frozen G1 bar (§3) vs ctrl ablation.
```

> ckpt PULL before teardown (a_fire_recover_complete) · `.pt`+`.clm` 둘 다 영구저장.
