---
id: H_1461
slug: 1461_language_purity
title: G6 IDEATION ★ FALS-depth wall — LANGUAGE-PURITY (code-switch 오염이 진짜 벽인가)
group: gate-dig (G6 IDEATION ★) — FALS-depth wall, multi-lens breakthrough ⑥ (language-contamination vs capacity; a_break_the_wall (b) 변수혼재)
terminal_tier: 🟠 PARTIAL / DIRECTIONAL — language-pollution 은 실재 nuisance(자유생성 20.3% 한글)이나 벽은 아니다; ASCII-only 강제가 FALS 0→0.33·DIST 4→5 만 올리고 B3 cross-shuffle COLLAPSE 안 함(0.33=0.33) + B1/B4/B5 미달 → 회복된 FALS 는 EARNED BINDING 아닌 GENERIC FORM. 6-렌즈 capacity 수렴은 language-contamination ARTIFACT 가 아니다(WALL=CAPACITY 우세, 통제 후에도 유지).
wired: DIRECTIONAL (torch-side: base 가중치 재사용, gauge_lib._decode 디코드 제약만 — verdict NOT engine-native; a_engine_native_learning. engine-native 재측정 = ASCII-mask 를 CORE bytegpt_decode 에 배선해 byte-exact 재측정 follow-on ING.)
verdict_dir: state/verdicts/1461_language_purity/
terminal_verdict: state/verdicts/1461_language_purity/H_1461.txt
date: 2026-06-20
source: UNIVERSE
archived: false
artifacts:
  - state/1461_language_purity/h1461_language_purity.py
  - state/1461_language_purity/g6_common.py
  - state/1461_language_purity/h1461_result.json
  - state/1461_language_purity/h1461.log
  - state/verdicts/1461_language_purity/H_1461.txt
---

# H_1461 — G6 IDEATION ★ FALS-depth: LANGUAGE-PURITY (code-switch 오염 통제)

## Why (사용자가 직접 짚은 결정적 변수 — a_break_the_wall (b) 변수혼재)

지금까지 6 렌즈(H_1435 data / 1436 obj / 1437 form / 1439 bind-head / 1449 attention /
1440 curriculum)가 전부 🧱 **WALL=CAPACITY** 로 수렴했다. 그런데 base
`h1129c_chat.pt` = `anima-clm-midcap-303m-broad-en-emergent` = HF.jsonl 명시
"English-DOMINANT broad corpus (ASCII-filtered **5-lang** wiki)" + chat 한글 대화 혼입.
**★ H_1129 HF notes 원문 경고: "the multilang 7B + 303M v1 both CODE-SWITCH-COLLAPSED."**

H_1305 FALS detector(COMPARATOR/MEASURABLE/STANCE)는 **전부 ASCII 영어 단어**. mouth 가
영어 falsifiable claim 생성 중 한글로 code-switch 하면 detector 가 그 클레임을 못 본다 →
FALS=0. 즉 6 capacity 수렴이 사실은 **language-contamination ARTIFACT** 일 수 있다.
벽이 capacity 가 아니라 언어오염이면 **ASCII-only 강제가 돌파**가 된다. 이 측정은 6
capacity 수렴 전체의 재해석이 걸린 결정적 통제다.

## Method (frozen-first, c9/p7 — $0, 재학습 불필요, 디코드 제약만)

- base = `state/chat_303m/h1129c_chat.pt` (303M ByteGPT, d1024/L24/H16/block512). 가중치 불변.
- 동일 base 를 **두 디코드 모드**로 H_1435 FROZEN 5-bar 재측정:
  - **UNMASKED** = 기존 `gauge_lib._decode` (top_k40/temp0.7, code-switch 허용) → base plateau 재현.
  - **MASKED** = 디코드 매 스텝 **byte 0x80-0xFF(한글 UTF-8 lead/continuation)의 logit 을 -inf**
    로 마스킹 → 영어/ASCII-only 강제 생성. byte-identical 디코드 경로(같은 top-k/RNG/stops),
    유일한 차이는 mask 한 줄.
- UNMASKED=BASE, MASKED=treatment 로 frozen `print_bars` 재사용 → ASCII-only 가 lift+B3 collapse 를 버는가.
- **C1 통제**: COMPARATOR|MEASURABLE 의 non-ASCII 토큰 0개 검증 → mask 는 언어필터일 뿐
  falsifiable claim 토큰 자체를 막지 않음(detector 정답 주입 아님, anti-tune).
- **GUARD**: MASKED per-seed 텍스트의 non-ASCII byte 0/30 자가검증(1차 monkeypatch-누락 버그를 잡아 재실행).
- seeds [7, 4302, 4303], eval_seeds = `gauge_lib.IDEATION_SEEDS`(5, ASCII).
- 해석(frozen): masked FALS↑ + B3 collapse → 언어오염-돌파 / 둘 다 FALS=0 → capacity 확정 /
  masked FALS↑ but 5-bar 미달 → PARTIAL(언어는 부분 레버, 벽 아님).

## Result (mean/3 seeds — DIRECTIONAL, torch on pool aiden RTX 5070, $0 idle-reuse)

CODE-SWITCH 재확인 (H_1129 경고 실측):
- **UNMASKED non-ASCII(한글) byte ratio = 0.2029** — 자유생성의 **20.3% 가 한글 code-switch**
  (e.g. `'IIT tries to quantify this with phi, the measure of integrated information. | 도우미: ...'`).
- MASKED non-ASCII ratio = **0.0000** (GUARD: MASKED 텍스트 non-ASCII 0/30). C1_pass=True.

FROZEN 5-BAR — MASKED(treatment) vs UNMASKED(base):

| bar | base(UNMASKED) | treat(MASKED) | pass |
|---|---|---|---|
| B1 FALS-FLOOR  FALS_in≥1 | 0.0 | **0.3333** | ✗ |
| B2 COUNT       DIST_in≥5 | 4.0 | **5.0** | ✓ |
| B3 X-SHUFFLE   FALS_shuf<FALS_in (COLLAPSE) | 0.0 | 0.3333 (=0.3333) | ✗ **★ NO collapse** |
| B4 HELD-OUT    FALS_ho≥1 | 0.0 | 0.0 | ✗ |
| B5 vs-BASE     FALS_in≥base+1 | — | 0.3333 vs 0.0+1 | ✗ |

per-seed in_fals: UNMASKED [0,0,0] · MASKED [1,0,0] · MASKED shuf [1,0,0].

## Verdict — 🟠 PARTIAL / DIRECTIONAL: 언어오염은 nuisance, 벽은 아니다

ASCII-only 강제가 FALS 를 0.0→0.333, DIST 를 4→5(floor)로 올렸다 → **code-switch 는 측정된
FALS=0 에 실제로 기여한 nuisance**(20.3% 한글)다. 그러나 frozen 5-bar 를 넘지 못한다:
- **B3 cross-shuffle COLLAPSE 안 함(0.333=0.333)** — 회복된 FALS 는 EARNED comparator↔measurable
  BINDING 이 아니라 **GENERIC FORM**(donor measurable 교체해도 falsifiable 유지). 그 1 회 hit =
  `"The byte-level approach is slower to converge but handles Korean and English equally well."`
  ('slower','but' = 비교자 형식이 measurable 에 BOUND 되지 않음).
- B1 floor 미달(0.333<1, 3 seed 중 1 회만), B4 held-out=0, B5 미달. 나머지 MASKED 텍스트는
  반복 garble 로 퇴화(`G\nG\n` / `km ==` / `humidity style=`) — ASCII-mask 가 303M 을 더 grounded
  하게 만들지 않고 오히려 분포 밖으로 밀어냄.

=> **6-렌즈 capacity 수렴은 language-contamination ARTIFACT 가 아니다.** 언어변수를 통제(ASCII-only)
해도 벽이 유지된다 → code-switch 는 기여 nuisance 였을 뿐 천장의 원인이 아니다. 6 수렴 재해석 =
**강화(NOT 반증)**: 언어순수성은 부분 레버, WALL=CAPACITY 우세. (a_break_the_wall: 변수혼재 (b)를
통제했으나 벽이 c(substrate/capacity)로 확인됨.)

## Scope / honesty (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **DIRECTIONAL** — torch + gauge_lib._decode (a_engine_native_learning). engine-native 재측정
  (ASCII-mask 를 CORE `bytegpt_decode.hexa` logit 단계에 배선 → byte-exact 재측정) = follow-on ING.
- bar 0 이동, tune-to-green 0 (c9). 1차 실행의 monkeypatch-누락 버그(MASKED 가 실제 unmasked)를
  GUARD 가 잡아 재실행 → 최종 MASKED 는 byte-검증 ASCII-only.
- TOY: base ckpt 1개 / 5 eval seeds / 3 seeds / 110-byte 디코드. ASCII-mask 는 **언어**필터지
  **의미**필터 아님 — 한글을 끈다고 영어 grounding 이 생기지 않음(측정이 보여줌). scale/다른
  ckpt(H_1435/1457 trained)/real-corpus/native-English-only 재학습 transfer UNVERIFIED.

xref: H_1129(code-switch-collapse 경고 출처)·H_1305/1394/1410(FALS=0 base)·H_1435(form trained, 🧱 capacity)·
H_1436/1437/1439/1449/1440(6-렌즈 capacity 수렴)·H_1457(knowledge-grounding, 🧱 capacity)·
a_break_the_wall(변수혼재 (b) 통제)·a_no_llm_frame_trap·a_engine_native_learning·a_verified_must_wire·
a_scale_honest_scope·a_toy_scale_recheck·p7·c9·c17.
