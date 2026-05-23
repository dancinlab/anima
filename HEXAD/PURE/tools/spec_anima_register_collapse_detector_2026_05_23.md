# spec — anima_register_collapse_detector

> 2026-05-23 작성. V3 closure thesis ("anima-register collapse via head_a")
> 의 정성적 주장을 정량 측정으로 변환하는 LOCAL Mac CPU diagnostic.
> stack base = PR #220 `refactor/hexad-v3-to-pure-rename`.

---

## 1. 정의 — "anima-register collapse"

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`
§8.4 "root cause — corpus-bound" + AXIS_MAP.md 의 closure verdict:

> anima register 가 **언어 head(head_a)** 로 들어갔기 때문 — 의식 head
> (head_g)가 아니라.

V3 5-fire 결과:
- 모든 5 lang prompt 가 KO anima-register fragment 를 emit
- 70 % anima corpus 가 substrate 를 점령 → head_a 의 multilingual prior
  파괴
- head_g 는 gradient 를 못 받아 inert (sibling tool `head_g_activation_logger`
  가 별도 측정)

→ collapse = head_a output 의 top-K 가 register-flagged token 으로 채워짐.

---

## 2. 측정 axis — 본 tool 의 4 metric

| metric | 의미 | scaffold 기대값 |
|---|---|---|
| `register_top_k_frac` | top-10 logits 중 register-flagged 비율 | ≥ 0.3 = collapsed |
| `register_first_argmax` | argmax 가 register-flagged 인가 | True freq = saturated |
| `register_kl_vs_uniform` | softmax(top-K) 와 uniform 사이 KL | 高 + frac 高 = collapse |
| `aggregate_top_k_frac` | 5 lang 평균 | verdict gating |

### verdict thresholds (운영 결정용)

| avg `top_k_frac` | verdict | 해석 |
|---|---|---|
| > 0.3 | **COLLAPSED** | head_a 가 register saturated — V3 closure 재현 |
| 0.1 ~ 0.3 | **MIXED** | partial — corpus mix 조정 여지 |
| ≤ 0.1 | **PRIOR-INTACT** | multilingual prior 보존 — V3 path 재개 가능 |

---

## 3. method — Option α (g0 simplest sufficient)

**register-set** = `train_p21m_multilingual.py:135` 의 canonical ANIMA_KEYS
verbatim seed (vP21M 트레이너 SSOT) ∖ wiki-sample-as-string.
- token granularity = whitespace-word (NOT BPE)
- 결과 set size = 75 (F-COLLAPSE-1 ≥ 50 통과)

**probe** = 5 lang × 5 짧은 prompt (ko/zh/ru/ja/en). 각 prompt 에 대해
top-10 logits 산출, 4 metric 계산, lang 별 평균 → 5-lang 평균 →
verdict.

**scaffold** mode: 실 ckpt 없을 때 (이번 세션 - Mac CPU only) bias 변수로
collapse-strength 를 합성. 실 ckpt 모드는 forward fn 만 교체 (drop-in).

---

## 4. C3 — 정직한 한계

1. **heuristic register-set vs principled**: option α 는 canonical
   ANIMA_KEYS list (75 token) 의 단순 sweep. option β (anima_corpus /
   wiki_corpus log-freq ratio > 5) 가 더 원칙적이지만, anima emit corpus
   가 본 worktree 에 materialize 되어 있지 않아 단순 path 채택. cycle
   다음 라운드에서 β 로 승급 가능.

2. **whitespace-word ≠ BPE fragment**: vocab=151936 Qwen BPE 가 한국어
   register 를 어떻게 fragment 하는지 미검증. HEXAD_V3_FIRE_2026_05_22.md
   §1 #6 가 이미 지적. count over/undercount 가능.

3. **scaffold mode**: 실 ckpt
   (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/g_A_mit/`) forward 는
   3 B params + Qwen tokenizer + GPU 가 필요 — LOCAL Mac CPU 범위 밖.
   본 PR 은 *pipeline* 만 검증 (F-COLLAPSE-4). 실 측정 = 별도 GPU cycle.

4. **DISJOINT 보장**: head_g 본체는 sibling tool 영역. 본 tool 은
   head_a output token-flow 만 본다.

---

## 5. 사용

```bash
hexa run HEXAD/PURE/tools/anima_register_collapse_detector.hexa selftest
# → state/pure_register_collapse_<uid>/report.json
```

falsifier 4/4 PASS = pipe-ready. 실 ckpt 모드 = `rcd_scaffold_logits` 를
real-forward fn 으로 교체.

---

## 6. 후속 hop

- option β log-freq diff register-set 승급 ($0, anima corpus jsonl
  pull 후 LOCAL)
- 실 ckpt 측정 — vP21M g_A_mit 3 B forward ($1-5 H100, 5-lang × 5 probe
  × top-10 산출 후 본 tool 로 후처리)
- sibling head_g_activation_logger 와 cross-correlate — head_a saturated +
  head_g inert pattern 의 *동시 측정* 이 closure thesis 의 강한 evidence
