# PREREG — co-trained LIVE bind op × recombination objective (the decisive 3rd arm)

**상태: 발사-준비(fire-ready) · GPU 학습 = cost-gate(explicit go 대기) · ~$3-5/A40**

이 카드는 ①(state/g1_cotrain_live_bind, H_1818 = op+plainCE 2-arm)가 **놓친** 결정적 arm을 고정 스펙으로
박는다 — 중간 메시지로 보정하니 누락됐으므로(convergence 후보), 여기 frozen 스펙으로 못박는다.

## 왜 (이번 세션 삼각측량)
- **op 단독**: frozen-wire inert(g1_frozen_mouthbind_screen) + co-train plainCE도 toy Task B가 inert 예측(g1_toy_cotrain_bind_derisk) + ①(H_1818)이 실측중(예상 inert).
- **objective 단독**: H_1602 3변종 303M = NOT-SUPPORTED(aa7933).
- **결합(op + objective)**: **미검증** = 유일한 sweet-spot. toy: "op은 composition을 *강제하는 목표* 없이는 trunk-memorize로 우회돼 inert" → 둘 다 필요.

## 설계 (3-arm 인과격리 · matched trunk-init seed/data/steps)
| arm | 학습 신호 | 기대 | 역할 |
|---|---|---|---|
| (a) `op_plaince` | live-retain bind op + 평범 CE | inert (G1≤1) | = ①(H_1818) 재사용 가능 = 음성대조 |
| (b) `obj_only` | bind op OFF(λ=0) + recomb-objective | floor (G1≤1) | aa7933 H_1602 재확인 |
| (c) `op_obj` | live-retain bind op + recomb-objective | **G1≥2?** | ★결정 arm★ |

**결정 테스트: (c) > (a) AND (c) > (b)** (같은 3-seed) → "구조+강제 결합"이 재조합 레버.

## recomb-objective 정의 (필수 · 누락 금지)
trunk penultimate x 에서 두 씨앗 개념 leg를 P_a·x, P_b·x로 투영. 보조 손실 L_recomb:
**두-개념 합성 타깃은 bind(P_a·x, P_b·x)로부터는 예측 가능하되 어느 한 leg 단독으로는 불가**해야 함
(= 곱셈/외적 결합이 운반하는 정보를 additive 경로가 못 만들게). 구현 후보:
- contrastive: bind(a,b) ↔ 진짜 합성 vs derangement-shuffled 합성 (InfoNCE), OR
- held-out-combo CE: 학습엔 없던 A×B 조합을 bind 경로로만 맞히게.
total loss = next_byte_CE + aux_moe + λ_bind·bind_ce + **λ_recomb·L_recomb** (λ_recomb≈0.05–0.3 sweep).
arm (b)는 동일 L_recomb이되 bind op = identity(λ_bind=0).

## FROZEN bar (측정 전 박제 · tune-to-green 금지 · p7)
- **G1**: composed_distinct≥2 ∧ >max_single ∧ coherent, ≥2/3 seeds.
- **G6**: dist≥5 ∧ fals≥1.
- **LIFT**: (c) best_distinct/fals 가 (a),(b) 대비 strictly 증가, 같은 seed.
- **held-out**: 4/4 register DESCENT (verify_clm_v2 descent, math.log mirror) — 미달이면 overfit=verdict 무효.
- **G0 통과 필수**: aa7933가 2000-step undertrain으로 INCONCLUSIVE-at-floor 났으므로 **steps 충분히(≥4000) + G0 ≥4/5 통과**해야 arm-vs-arm 해상도가 생김(안 그러면 또 floor 일치).

## 불변식 (a_engine_native_learning · convergence g-gates-py-1)
- bind op은 **직렬화에 RETAIN**(drop 금지) → clm_decode CLMB 확장으로 live 실행(① trainer가 이미 함, 재사용).
- 측정 = cli/evaluate.py → g_gates(gen80, multiseed) engine-native-py = DIRECTIONAL screen; (c) GREEN이면 hexa clm_decode/serialize lockstep로 TERMINAL 승격(a_verified_must_wire rung3).
- ckpt PULL before teardown(a_fire_recover_complete) · pod 누수 점검.

## 발사 명령 (go 시)
`hexa cloud` CUDA-12 pod 렌트 → core/cli/corpus push → 3-arm × 3-seed{7,4302,4303} 학습(≥4000 step,
savant 골든존) → 직렬화(op retain) → held-out DESCENT → engine-native-py G0-G6 → ckpt PULL → teardown.
산출 = state/g1_cotrain_recomb_bind/RESULT.md + cards/H_<id> + jsonl + CHANGELOG.
