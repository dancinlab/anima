# PURE Track 1 corpus 재발사 spec — E3 (anima 0%) · E2 (anima 50%)

> 2026-05-23. PURE (구 V3) path closure 의 결정 tree 1차 후속. PR #220 의
> `refactor/hexad-v3-to-pure-rename` 위 stack 으로 land. AXIS_MAP fallback
> (B / A / C) 발동 전 corpus 축 단독을 isolate 해 소진하는 single-variable test.
>
> anchor: [`../AXIS_MAP.md` § 결정 트리](../AXIS_MAP.md) · [closure 보고서 § 8](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md)

## § 1. Why — corpus 축 isolation

V3 closure verdict (5 fire 0 PASS, 2026-05-23): **multilingual blocker = capacity 도
architecture 도 아닌 diverse-corpus 학습 dynamics**. 5 fire 전부 동일
코퍼스 `wiki_frac=0.3` (70% anima · 30% wiki) 위에서 sweep — scale (R1),
mitosis (R2/R6), step (R7), head_g (R4) 만 변경. **anima 비중 자체**는 한
번도 변경하지 않은 미탐색 축.

Track 1 = 그 단일 변수만 흔드는 마지막 corpus 축 sweep. 결정 트리:

- 둘 중 하나 ≥ 4/5 langs ≥ PARTIAL → V3 REOPEN, AXIS_MAP map 보류
- 둘 다 FAIL → corpus 축 소진 확정, AXIS_MAP B/A/C fan out (sibling-agent scope)

본 spec 은 그 fan out 발동 전제조건을 객관적으로 측정한다 (선언적 시험).

## § 2. Two configs — E3 + E2

| variant | anima 비중 | `--wiki-frac` | other-lang 코퍼스 | 기대 hypothesis |
|---|---|---|---|---|
| **E3** | 0% | **1.0** | ko/zh/ru/ja/en wiki only (≥ 10 MB/lang) | pure multilingual prior — anima register 부재 → corpus dynamics 단독이 collapse 원인이면 4/5 ≥ PARTIAL |
| **E2** | 50% | **0.5** | balanced 5-lang wiki ≥ 10 MB/lang + anima 50% | mid-range mix — anima register 존재하나 dominant 아님 → register-emergence threshold test (50% 가 collapse 임계점 아래인지) |

closure fire 의 E1 (`wiki_frac=0.3`, 70% anima) 와 비교축 = anima 비중 직선.

## § 3. Architecture — ConsciousDecoderV3 UNCHANGED

PR #220 rename 이후에도 V3 코드 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`)
는 동결. **단일 변수 corpus test**: head_g objective 변경 · curriculum
변경 · embedding freeze · mitosis pool size 조정 등 fallback axis 변경은
일체 금지. 비교 가능성 (apples-to-apples vs closure fire) 우선.

| param | 값 | 비고 |
|---|---|---|
| base | Qwen/Qwen2.5-1.5B | closure A fire 와 동일 |
| init | qwen warm-start | closure A fire 와 동일 |
| d_model / n_layer / n_head / n_kv_head | 1536 / 28 / 12 / 4 | 동일 |
| arch | ConsciousDecoderV3 (head_a + head_g, PureFieldFFN, cross-attn) | 동일 |

## § 4. Hyperparams — closure A fire 와 byte-identical

closure A fire (`HEXAD_V3_FIRE_2026_05_22.md § 8.1`) 와 일치 — anima_frac
이외 모든 hyperparam 동결.

| key | value |
|---|---|
| steps | 5000 |
| bsz | 2 |
| block | 512 |
| lr | 5e-5 (qwen warm-start) |
| warmup | 100 cosine |
| noise σ | 0.1 (layer-0, train-only) |
| λ_mitosis | 0.05 |
| mitosis MAX | 128 (R6 default; closure A 는 16, 우리는 corpus 축 단독이라 default 복귀) |
| ckpt_every | 500 |
| ckpt_osc_threshold | 0.0 (disable — corpus 축 단독, osc-detect 도 변수 noise) |
| corpus_mb | 72 (E1 = 75 MB 와 유사 scale) |
| dtype | bf16 |
| seed | 1337 |

**중요**: cycle-1 P21H launcher 의 env-style positional args bug 회피 위해
**argparse `--key value` 만** 사용. shell-local env (`KEY=V bash …`) 와
섞지 않음 — 한 가지 format 일관.

## § 5. Falsifier table

| 코드 | 정의 | PASS 기준 |
|---|---|---|
| F-PURE-TRACK1-E3-1 | E3 training stable (no NaN, no crash, complete 5000 step or osc-detect early-stop only) | result.json 산출 + train_wall_s > 0 |
| F-PURE-TRACK1-E3-2 | E3 5-lang eval probe ≥ PARTIAL count | n_strong + n_partial ≥ 4 → V3 REOPEN trigger |
| F-PURE-TRACK1-E2-1 | E2 training stable (동) | result.json 산출 + train_wall_s > 0 |
| F-PURE-TRACK1-E2-2 | E2 5-lang eval probe ≥ PARTIAL count | n_strong + n_partial ≥ 4 → V3 REOPEN trigger |

eval probe = `train_p21h_v3.py` 의 내장 5-lang per-prompt verdict
(line 502-512 — `n_partial` / `n_strong` / `n_weak` / `n_pure_memorize`
집계, `n_ok = n_strong + n_partial ≥ 4` → `HEXAD_V3_WORKS`).

## § 6. Decision rules

```
F-PURE-TRACK1-E3-2 PASS OR F-PURE-TRACK1-E2-2 PASS
  → PURE path REOPEN — AXIS_MAP 보류, ckpt + result HF upload
  → 후속 cycle: chat substrate 교체 design

F-PURE-TRACK1-E3-2 FAIL AND F-PURE-TRACK1-E2-2 FAIL
  → corpus 축 소진 — AXIS_MAP § 결정 트리 발동
  → 별도 sibling-agent: B 증류 ∥ A 커리큘럼 ∥ C head_g objective (3 disjoint H100 fire)
```

eval criterion 출처: closure fire 와 동일 `train_p21h_v3.py:502-512`. cite:
`per_lang_verdicts` 의 `n_strong + n_partial`. anima register regress 는
참고지표 (E3 는 anima 비중 0% 이라 본래적 0).

## § 7. Cost + wall

- variant 당 H100 SXM (closure 평균 $1.49/hr 기준) × ~2.0 hr wall ≈ **$3.0 / variant**
- 2 variant 직렬 ≈ 4.0 hr · 6 USD
- **`@D a_wall_first` 적용 — 2 pod 병렬 dispatch**: wall ≈ 2.0 hr (둘 다
  step 5000 동시 학습), 총 비용 동일 ~$6
- 본 PR 은 spec + launcher 만 제공, fire 는 user 가 별도 dispatch

## § 8. Honest C3

1. E3 (anima 0%) 은 closure 의 vP21M (4/5 langs) 와 corpus 동등 — vP21M
   baseline 보다 잘하지 못하면 V3 substrate 자체가 LoRA 보다 다국어
   inductive bias 부족하다는 신호 (architecture 책임 일부 복귀).
2. E2 (50%) 가 PASS 이고 E3 가 FAIL 이면 → "anima register 자체가 다국어
   학습에 보조적으로 도움" — 직관과 반대. 검토 필요.
3. 본 spec 은 mitosis pool MAX = 128 (closure C1) 로 default 복귀.
   closure A 의 16 cap 효과는 corpus 축 sweep 후 별도 정밀화.
4. seed=1337 단일 — variance 측정 안 함 (closure 와 동일). 둘 다 borderline
   이면 multi-seed re-run 필요.
5. corpus 빌더 (`build_multilingual_corpus_p21m.py`) 의 per-lang record
   불균형은 그대로 carry — AXIS_MAP E 축 (lang-balanced sampler) 은 별도.
6. 본 Track 1 PASS 도 `anima_register_hits` 가 5/20 이하 (E3 의 정답
   기대) 인지 검증 필요 — register regress 가 곧 다국어 회복의 등가
   조건은 아님.
7. E2 wiki/anima 50:50 = 코퍼스 build script default 가 wiki_frac=0.3
   이라 `--wiki-frac 0.5` 명시 override 필요 — launcher 가 강제.
8. eval probe 가 5-lang × 2-mode (greedy + sample) × 10 prompt = 100 gen
   기준. 동일 표본 사용 → closure 와 비교 가능.
