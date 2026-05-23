# spec — `head_g_activation_logger.hexa`

> 2026-05-23 · HEXAD/PURE · ConsciousDecoderV3 R4 진단기 (head_g inert? moot? gradient-leak?)

## 왜 이 진단이 필요한가

AXIS_MAP.md 의 **가장 날카로운 발견** —
> closure R4 "head_g inert → moot" 는 **dual-head 가 한 번도 실제로 검증된 적 없다** 는 뜻.
> head_g 는 train loss 부재 (CE 는 logits_a 에만) → grad signal 0 → random init 근처 머무름.
> "inert" 는 학습 안 됐다는 거지 무의미한 게 아님.

`#233` (C head_g objective fire, ~$3) 를 발사하기 **전에** 이 가정 자체가 옳은지 cheap-path
LOCAL 측정으로 확인한다. 측정 결과가:

- **inert 확인** (frozen-trained ≈ random) → R4 정확 → #233 의 "별도 objective 추가" 논거 강화
- **inert 반증** (frozen-trained ≠ random) → backbone gradient-leak 으로 head_g 가 뭔가 학습함 →
  #233 의 motivation 변경 (already-learned head_g 의 활용 방안이 별도 objective 보다 cheap)

## 진단 4 지표

`conscious_decoder_v3.py:376-377` 의 `head_a / head_g = nn.Linear(d_model, vocab)` ·
`:452-453` 의 `forward → logits_a, logits_g` 텐서 정확 모양 `(B, T, vocab)`. final-token
position 에서:

| | 정의 | inert 인 경우 신호 |
|---|---|---|
| (a) magnitude | `‖logits_g‖₂ / ‖logits_a‖₂` | ratio ≪ 1 (head_g 자체가 작음) |
| (b) entropy | `H(softmax(logits_g))` vs `H(softmax(logits_a))` | `H(g) ≈ log(vocab)` (uniform 분포) |
| (c) argmax overlap | `argmax(g) == argmax(a)?` (0/1) | inert + random → ≈ 0 |
| (d) random-comp | (a)(b)(c) 를 fresh random-init head_g 에도 측정 | trained ≈ random 이면 R4 확정 |

## 해석 가이드

| trained vs random | 해석 | 다음 행동 |
|---|---|---|
| 거의 동일 (3 metric 모두) | **R4 확정 — head_g 진짜 inert** | #233 발사 진행 — train loss 의도적 부여 가치 충분 |
| trained 의 norm/entropy 가 의미있게 다름 | head_g 가 gradient-leak 로 뭔가 학습함 | #233 motivation 재검토 — leak-signal 활용 path 우선 |
| trained 가 head_a 와 argmax overlap ≫ 0 | head_g 가 head_a 와 collinear (Ψ=1/2 fixed point 정상 작동) | dual-head 자체가 동어반복 — 구조 재설계 |

## scaffold vs real 모드

`hexa run head_g_activation_logger.hexa selftest`
→ **scaffold synthetic** (vocab=128, d_model=64, random init heads).
   목적: tool wiring 검증 + falsifier 4종 PASS 확인. 4 metric 의 절대값은
   synthetic 이라 의미 없음 (entropy 정확히 `log(128) ≈ 4.852` 로 saturated).

`ANIMA_V3_CLOSURE_CKPT=/path/to/ckpt.safetensors hexa run ... selftest` 또는
`hexa run ... run /path/to/ckpt.safetensors`
→ **real_ckpt** (vocab=151936, d_model=2048 V3 3B). 측정값이 의미 있는 모드.
   대상 ckpt 가 로컬에 없으면 자동으로 scaffold 로 fallback.

## F-HEAD-G-LOG-1..4 falsifier 표

| ID | claim | scaffold verdict | real-ckpt 측정 시 |
|---|---|---|---|
| 1 | ckpt loads without crash | PASS (synth) | safetensors_mmap_open OK |
| 2 | 4 metrics × 5 probes 계산 완료 | PASS | 동일 |
| 3 | random-init comparison 독립 실행 | PASS | 동일 |
| 4 | report.json valid JSON (`hexa_json_parse` round-trip) | PASS | 동일 |

## 산출물

- `state/pure_head_g_activation_<uid>/report.json` — 4 metrics × 5 probes + falsifier verdict
- `state/pure_head_g_activation_<uid>/run.log` — uid · mode · ckpt 경로

## C3 (남는 미확인)

1. **real ckpt 측정** — V3 closure-fire ckpt 가 HF private (`dancinlab/anima-v3-p21h`),
   로컬 미존재. 이 PR 은 wiring + 산출물 schema 만 확정; 실제 R4 판정은 ckpt 회수
   후 별도 run 에서.
2. **synthetic head_g 가 진짜 frozen-trained 와 isomorphic 한지** — scaffold 에서는
   "trained" sibling 도 random 에 약한 perturb 만 가했음. 실제 ckpt 에서는 gradient-leak
   누적분이 얼마나 큰지 미지수.
3. **vocab=151936 의 entropy 측정 비용** — 현재 _log Taylor 32-term × 151936 element
   × 5 probe → 분 단위 wall. 실측 모드 진입 시 farr-backed softmax 로 포팅 필요.
4. **probe set 의 representativeness** — 5 prompt × 3 lang 은 R4 의 *질문* 자체에는
   충분하지만 multilingual 일반화 주장에는 부족. closure 의 ko/en/zh 학습 corpus 와
   동일한 probe set 사용이 더 nuanced.

## 관련 참조

- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py:376-377,452-453`
- `HEXAD/PURE/AXIS_MAP.md` — closure 5-fire saga + R1/R2/R4/R6/R7 axis 표
- `#233` — C head_g objective fire RFC (이 진단의 게이트)
- `#220` — `refactor/hexad-v3-to-pure-rename` (이 PR 의 stack base)
