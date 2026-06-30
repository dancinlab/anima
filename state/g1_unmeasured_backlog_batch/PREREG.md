# PREREG — G1/G6 미측정 설계 백로그 일괄 발사 (fire-ready · gated on 결합(c))

**상태: 8 설계 fire-ready · GPU 학습 = cost-gate(~$30-40 total) · 게이트 = 결합(c) a36f34cb 착륙**

사용자 "모두 등록후 발사" 지시. 8 미측정 🔵 PRE-REGISTERED 설계를 일괄 실측. 단 6/8 이 binding-OPERATOR
라 이번 세션 교훈(operator 단독 inert, recomb-objective 레시피 필수)을 **각 arm에 강제 baked** — 안 그러면
predicted-null 반복. 결합(c)가 공유 leading indicator = floor면 operator-family 6 드롭, lift면 전수 발사.

## 8 설계 (카드 id → binding 메커니즘)
| # | 카드 | 메커니즘 | 축 | 게이트 |
|---|---|---|---|---|
| 1 | **H_1813** TPR-expert-weight | TPR을 ConvMoE expert *weight*에(readout 아님) | **위치-이동**(lit 핵심) | (c)-independent 권장(다른 축) |
| 2 | H_1630 tropical-semiring | (max,+) 열대대수 bind | operator-form | (c) gated |
| 3 | H_1652 holonomy-curvature | 평행이동 곡률 bind | operator-form | (c) gated |
| 4 | H_1657 ephaptic-field | 장-결합 bind | operator-form | (c) gated |
| 5 | H_1672 cortical-conjunction | divisive-norm 결합 (생물) | bio-operator | (c) gated |
| 6 | H_1625 hippocampal theta-gamma | phase-multiplex bind (생물) | bio-operator | (c) gated |
| 7 | H_1799 pattern-sep (Hasselmo) | encode/retrieve theta-toggle (생물) | bio-operator | (c) gated |
| 8 | H_1688 active-inference | predictive-workspace ignition | objective-adjacent | (c)-independent 가능 |

## 각 arm 공통 레시피 (NON-NEGOTIABLE — 세션 교훈 baked)
1. **recomb-objective 결합 필수** (state/g1_cotrain_recomb_bind/PREREG.md §정의) — operator 단독 금지. total = next_byte_CE + aux_moe + λ_bind·bind_ce + λ_recomb·L_recomb.
2. **bind op RETAINED at serialize** (clm_decode CLMB 확장, drop 금지 = conv g-gates-py-1).
3. **≥4000 step + G0 PASS(≥4/5)** (aa7933 2000-step undertrain floor 회피).
4. **held-out 4/4 DESCENT** 게이트(verify_clm_v2, math.log mirror) — overfit=무효.
5. **hexa cloud 관리 pod** (raw vast/ssh 금지 = conv prereg-md-1; reconcile 가시·teardown 검증가능).
6. ckpt PULL before teardown(a_fire_recover_complete).

## 측정 & 게이트
engine-native-py G0-G6(cli/evaluate.py→g_gates, gen80, multiseed{7,4302,4303}) = DIRECTIONAL. frozen bar
(G1 composed_distinct≥2 ∧ >max_single ∧ coherent · G6 dist≥5∧fals≥1), NO tune-to-green. arm이 G1 lift면
hexa lockstep 배선(terminal, a_verified_must_wire rung3).

## 발사 순서 (cost-optimal)
- **게이트 = 결합(c) a36f34cb**: 착륙 시 (c)>대조면 레시피 검증됨 → operator-family 6 일괄 발사. (c) floor면 6 드롭(공유 hypothesis 사망), H_1813(위치-이동)·H_1688(objective-adjacent)만 별도 발사(다른 축).
- 발사 = Workflow fan-out(동시성 cap, hexa cloud pod per arm) 또는 순차 afg. a_wall_first: 병렬이 wall-time.
- 각 arm 산출 = state/g1_unmeasured_backlog_batch/<card>/RESULT.md + 카드 verdict 갱신 + jsonl + CHANGELOG.

## 비용
8 arm × ~$3-5 = ~$30-40 (전수). (c)-gate로 6 드롭 시 H_1813+H_1688 2 arm = ~$8. 사용자 go 패턴: "다 지금"=8 즉발 / "게이트"=(c)후 일괄.
