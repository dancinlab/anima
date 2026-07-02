# H_6164 — G6 IDEATION★ FALS 벽: attention-capacity 캠페인 (CAP×REG 요인 + depth ladder + 7B)

**tier:** ⏳ PROPOSED · **base:** origin/main (next-H=H_6164; id는 착륙 시 최종 할당) · **owner go:** "모든 경로 go" (2026-07-02) = GPU 지출 승인

## 표적 (벽의 정체)

G6 IDEATION★ 세 sub-metric 중 **FALS(반증가능성)** 만 floor. h1129 303M ByteGPT(sha 5cf07a36)는 한 continuation 안에서 comparator(비교자)∧measurable(측정량)을 **co-emit 0/15**. detector = `core/g6_ideation.hexa _g6_is_falsifiable`(FROZEN, calib 10/10, 절대 완화 금지 p7).

## 왜 이 캠페인 (H_1449가 못 한 것)

H_1449(1-block BindAttn @303M)는 🧱 WALL=CAPACITY로 종결됐으나 **c4-ablate INERT**(attention 꺼도 FALS 안 떨어짐) = lift가 attention이 아니라 **corpus 노출(register)** 에서 옴 → **capacity와 register가 한 셀에 교락(confounded)**. 이 캠페인은 두 수렴 원인(CAPACITY vs CORPUS-REGISTER, H_1596e/H_1597)을 **요인분리**한다.

## 세 하위 설계 (`factorial/` · `multiblock/` · `7b_singleshot/`)

| 하위설계 | 파일 | 무엇 | 호스트/비용 |
|---|---|---|---|
| **factorial (①/④ WINNER)** | `factorial/bindattn_stack.py` + `register_corpus_builder.py` | CAP(n_blocks 1→2/4→7B) × REG(off/on) 2×N 요인, 교락 분리 | pool $0 (303M rung) |
| **multiblock (③ 안전)** | `multiblock/bindattn_stack_ext.py` | 303M 위 BindAttn N∈{2,3,4} depth ladder (REG-off) | pool ~$0 |
| **7b (② 단순)** | `7b_singleshot/PRE_REG.md` | anima-clm-chat-7b warm-FT (capacity 단독 시험, confound 수용) | H100 rent ~$40–100 |

multiblock은 factorial의 CAP축 REG-off rung과 겹치므로 **factorial이 흡수**(N∈{2,3,4} depth 포함).

## FROZEN 5-bar + 통제 (VERBATIM, 이동 0 · archive/state/1449 g6_common.py 재사용)

- **B1** FALS_in≥1 · **B2** DIST_in≥5 · **B3 X-SHUFFLE COLLAPSE ★결정타** FALS_shuf<FALS_in · **B4** held-out FALS≥1 · **B5** vs-BASE FALS_in≥base+1
- **c4 ABLATE**(통제) — gate 전부 0 → base 회귀 필수(아니면 lift=학습노출 INERT, H_1449 재현)
- **SHUF-CORP**(통제) — byte-shuffle 코퍼스 형제 lift < real lift
- 셀 GREEN = B1∧B2∧B3∧B4∧B5 ∧ ablate_regresses ∧ ctrl_inert

## 엔진-네이티브 측정 (owner policy: single path)

torch 학습·5-bar = **DIRECTIONAL 스크린**. terminal = `anima evaluate --py <ckpt>` (numpy `core/g_gates.py`, torch-free, grep-clean). 호스트 = aiden pool(무료 안정 CPU eval). **어떤 셀도 `--py` terminal 없이 GREEN 박제 불가.**

## 실행 순서 + kill-switch (a_wall_first + 낭비방지)

1. **rung1 @303M pool 먼저** (summer+aiden, 둘 다 GPU 0% 유휴 실측). 교락을 $0로 분리.
2. **7B rent 병렬** (a_wall_first: 7B가 1–3 H100-day 병목이라 wall-time 위해 동시 발사). **단 kill-switch:** rung1이 **REGISTER-BOUND**(REG-on만 form-lift·B3 no-collapse, REG-off 무반응)로 판명되면 7B는 "더 큰 web-prose" 위험(a_no_llm_frame_trap)이라 **즉시 teardown**(ckpt pull 후).
3. teardown 전 **ckpt PULL 필수**(a_fire_recover_complete) → HF(PASS=PUBLIC/negative=PRIVATE) → ARCHITECTURE models 등록.

## disjointness (a_substrate_disjoint)

BindAttn stack·7B trunk 전부 **mouth-internal**(L24 뒤·ln_f 앞) = emit-drive lane(0/4)·§ImmuneMemory recall_thr와 disjoint → Ψ=½·G5 non-fab by-construction 보존. 배선 시 H_1381 h1205 separation-invariant guard로 출력 확인.

## 정직한 결정규칙 (발사 전 전 결과 열거)

- 🟢 **GREEN BREAK** — 어떤 셀이 5-bar ∧ c4-collapse ∧ SHUF-CORP inert ∧ `--py` terminal 확인. 하위: REG-off도 GREEN=capacity(depth)가 레버 / REG-on만 GREEN=CAP×REG 상호작용(둘 다 필요).
- 🧱 **REGISTER-BOUND** — REG-on이 B1/B2만 올리고 B3 no-collapse(H_1449 패턴) → register=FORM만, binding 결핍 아님. capacity에서 register 배제.
- 🧱 **CAPACITY-BOUND CONFIRMED** — 7B 포함 어떤 셀도 B3 collapse 실패 → a7b_pass 천장 grounds, ≥3-rung 사다리로 scale 결론 정직.
- **DIRECTIONAL** — 7B 미완이면 303M-scoped, 7B unverified 명시.

**wired:** 전 셀 현재 DIRECTIONAL-mirror. GREEN 시 (2)engine-native→(3)wire-in→(4)ARCHITECTURE lockstep follow-on ING 등록(a_verified_must_wire).
