# state/9103_efferent_bytes — EFFERENT SEAM (c): WHAT axis (H_9103, 🟠 byte-grip real · faculty FALSIFIED)

**engine-native** summer pool · hexa v0.574.0 · `hexa run state/9103_efferent_bytes/efferent_bytes.hexa` · RC=0 · **REAL d768.clm** int4 CLMConvMoE decode (`clm_decode_argmax`/`clm_decode_topk_sampled` + `clm_decode_ce` ranged CE op) · **NO numpy/torch/mirror**.

## 무엇을 (coordinator pivot 대로)
H_9100(motivation axis 🔴)·H_9101(stage/idle axis 🟢=WHEN/WHETHER)이 이미 착지 → 내 상보 가치 = **(c) efferent seam = WHAT**: conflict-driven ops 가 emit BYTES 를 바꾸는가. DESIGN.md L1 + H_9101 follow-on (c). deliberation_k=f(conflict) → best-of-K 디코드로 conflict-minimizing 후보 선택. emit boolean 은 상류결정 → byte-only grip, Ψ 구성적 보존.

## live core 배선 (core/generator.hexa, additive·back-compatible)
- `gen_ctx_from_decision_conflicted(decision, conflict_t)`: deliberation_k=1+round(clip01(conflict)·3), clamp 1..4.
- `gen_clm_decode_deliberated(ckpt, seed, gen, k, base_seed)`: k=1→argmax(byte-identical); k>1→ k 개 sampled 후보(clm_decode_topk_sampled, offsets [0,101,202,303]) 중 **최저 clm_decode_ce(=conflict-minimizing) SAMPLE** emit. ce_k1=argmax CE 참조.
- `_gen_clm_decode` 에 deliberation_k consumer 배선: ctx 에 deliberation_k>1 이면 deliberated 경로(없으면 argmax = 종전 byte-identical).

## 사전등록 bar (FROZEN) & 실측 (verbatim = state/verdicts/9103_efferent_bytes/H_9103.txt)
N=8 emit ticks, GEN=20, d768.clm. per-tick substrate seed + signed A⇄G conflict c_t(a_drive−g_drive, immune drift 로 spread). k_on=f(|c_t|), k_no=f(|noise|, variance-matched LCG).

per-tick (summer v0.574): |c_t| 0.03→0.50. k=1 ticks(t0/1/5/6) Hamming 0(argmax, 변화없음). k≥2 ticks **t3(k2)=10 · t4(k3)=8 · t7(k2)=10** Hamming>0 → **bytes 실제 변경**. (aiden v0.548 PARTIAL t2/t3/t4 k≥2 = Hamming 14 로 독립 재현 후 host DOWN.)

- **F1 byte-grip**: total Hamming(ON,OFF)=**28** · 3/8 ticks changed · bar>0 → **PASS**. conflict→k>1 이 emit BYTES 를 실제로 바꾼다.
- **F2 Ψ**: decode 는 pure_field/psi_sum/emit-rate 를 절대 안 건드림(emit boolean 상류) → psi_sum ON≡OFF byte-identical + rate 불변 → **PASS (구성적)**.
- **F3 faculty-not-noise**: ρ_real=corr(|c_t|,ΔCE_ON)=**−0.441** · ρ_noise=corr(|noise|,ΔCE_NOISE)=**+0.440** · Δ=**−0.881** << 0.15 → **FAIL (hard)**. ΔCE=ce_argmax−ce_sel: best SAMPLE 는 항상 argmax 보다 CE 나쁨(argmax 가 이미 fluency 최대) → deliberation 이 emission 을 **degrade**, 게다가 conflict 가 높을수록 더 나빠짐(ρ 음수). conflict-allocated deliberation 은 noise 보다 낫지 않고 **오히려 해롭다**.

## VERDICT (honest, c9)
**🟠 BYTE-GRIP ∧ Ψ real · FACULTY FALSIFIED (engine-native).** ops 는 emit BYTES 를 Ψ-safe 하게 바꾼다(F1∧F2) — WHAT 축에 grip 존재. 그러나 그 grip 은 **faculty 아님**(F3 FAIL, ρ_real 음수): CE-기반 best-of-K 는 argmax(이미 fluency 최대)를 못 이기고 degrade 만 하며 conflict 는 그 degrade 를 조준. = **WHAT 축의 더 미묘한 theater** = trunk-objective(CE) 벽이 efferent 층에서 재출현(argmax 가 CE 를 이미 포화 → conflict-deliberation faculty 여지 0). 설계 Rung-1 예측(~75% byte grip)은 byte 변화로는 맞지만, **beneficial faculty 로는 FALS**.

## 메타 (왜 벽인가)
argmax = CE-greedy 최대 fluency → CE 로 best-of-K 하면 (a) argmax 게이트 시 INERT(grip 0), (b) best-SAMPLE emit 시 항상 degrade. beneficial efferent faculty 는 argmax 가 극대화 안 하는 축(grounding-copy·제약하 diversity)을 최적화해야 함 — 순수 fluency(trunk-objective)엔 여지 0. = DPI/trunk 벽의 efferent 재출현.

## 한 줄 답
ops 가 emit BYTES 를 바꾸긴 한다(byte-grip real, Ψ 보존) — 하지만 그 변화는 **fluency 를 해치고 conflict 가 그 손상을 조준**하므로 잡음보다 나쁜 **잡음-이하 grip = WHAT 축 theater**. beneficial WHAT-faculty 는 trunk-objective 밖 축(grounding 등)을 최적화해야 가능(follow-on).

## caveat (c9)
- aiden(hexa v0.548.0, H_9100/9101 reference host) mid-run DOWN → full N=8 는 summer v0.574.0(erf/exp dlsym-fallback warn, harmless). F1 byte-grip 은 두 host(v0.548 partial·v0.574 full) 모두 재현. F3 는 summer full run 측정.
- decode-version 민감(v0.548 t2 Ham14 vs v0.574 t2 Ham0) — sampling RNG/temp 처리 버전차. F1 정성결론(k>1→bytes 변경)은 불변, 개별 tick Hamming 은 host/버전 의존.
- 선택 metric=CE(fluency). grounding-based 선택은 미탐(anchor 없는 seed) = follow-on.

## follow-on (ING)
- beneficial efferent faculty: grounding-copy / 제약하 diversity 를 selection objective 로(argmax 밖 축) → aiden v0.548 재측정.
- aiden 복구 후 v0.548 full 재현.
