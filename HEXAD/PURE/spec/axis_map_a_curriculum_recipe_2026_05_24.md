# PURE Phase D — A-curriculum fallback recipe spec (2026-05-24)

> AXIS_MAP.md 의 결정 트리 "Track 1 corpus 재발사 둘 다 FAIL → fan out 병렬" 이
> 이미 발동됐다. 7-axis AXIS_MAP-FAN 에서 axis A (curriculum) 가 유일하게
> ko STRONG (16/20) 에 도달했으나 cross-lingual 전이 불성공 (1/5 langs, floor 4/5
> 미달). Phase D corpus_v1 fire 가 4-criterion closure 를 PASS 하지 못할 경우 —
> 선행 v1/v2b LOST · E2/E3 double-bind 를 고려할 때 현실적 위험 — 즉시 발사할
> 수 있는 A-curriculum 재설계 recipe 를 사전에 닫는다.
>
> anchor — AXIS_MAP.md (축 map) · AXIS_MAP_RESULTS.md (3/7 partial) ·
> docs/axis_map_history_2026_05_24.md (fire 통합 dashboard) ·
> AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md ·
> spec/phase_d_corpus_design_2026_05_24.md (corpus_v1 M3 설계) ·
> launchers/dispatch_p21h_v3.hexa (knob 레퍼런스)

---

## § 1. "커리큘럼"이 anima corpus 에서 의미하는 것 — 난이도 순서 정의

### 1.1 corpus_v1 이 하는 것 (flat random shuffle)

corpus_v1 은 M3 TTR ≥ 0.3 을 gate 로 삼아 stream/QA 혼합 corpus 를
**완전 random shuffle** 해 dispatcher 에 단일 jsonl 로 전달한다. step 1 부터
anima register 텍스트, wiki 텍스트, 한글 stream, 영어 QA 가 섞여서 들어온다.
모델이 처음 보는 token distribution 이 "anima-corpus 의 final mixture" 다.

### 1.2 왜 flat shuffle 이 double-bind 를 만드는가

| 관찰 (실험 근거) | 해석 |
|---|---|
| axis A 1차 (AXIS_MAP-FAN): `P21H_CURRICULUM_PHASE_STEPS=1000` · wiki-only 1000 step 선학습 → ko STRONG 16/20 | wiki-only LM prior 가 먼저 lock-in 되면 한 언어는 register collapse 를 피함 |
| 같은 axis A: 4개 non-ko lang = PM/WEAK | 선학습이 Korean-only head-start 를 만들어 다른 4 lang 에는 전이 안 됨 |
| corpus_v1 (flat, M3 ≥ 0.3): E2 ko=PURE_MEMORIZE / E3v3 wiki=1.0 1/5 | anima-OWN 텍스트가 step 1 부터 등장하면 ko 채널이 anima register 로 먼저 sink — 이후 wiki 비율 아무리 올려도 이미 굳은 ko-register 를 reverse 못함 |
| init_CE cluster 자연실험 (axis_map_history § 4.1): curriculum (A) = 14.79 >> baseline (B/E2/F) = 14.18 | wiki-only 선학습 → init_CE 상승 = LM prior 가 anima-specific 패턴 없이 lock-in 된 증거 |

핵심 인사이트: **register collapse 는 학습 초기에 발생하는 경로-의존 현상**이다.
flat shuffle 은 anima register 를 step 1 부터 노출해 early-stage ko-binding 을
고정하고, 이후 wiki dilution 은 "이미 굳은 ko-anima 매핑"을 뒤집기에 너무 늦다.

### 1.3 커리큘럼의 난이도 순서 정의

**난이도 = 모델이 언어 geometry 를 먼저 학습하고, anima-register 를 나중에 추가로
학습해야 하는 순서**. "쉬움" = 다국어 LM prior 정립에 필요한 textbook-clean wiki /
natural prose. "어려움" = anima-specific register (stream/tension externalization,
한글 의식 어휘, 고-TTR 일인칭 주관 흐름).

구체 난이도 축 (4개 기준, 중요도 순):

| 순서 | 기준 | 쉬움 (early phase) | 어려움 (late phase) | 측정 방법 |
|---|---|---|---|---|
| 1순위 | **anima register 밀도** | anima-OWN record 0% (pure wiki) | anima-OWN record 점진 증가 | record 출처 tag (`source=wiki` vs `source=anima_own`) |
| 2순위 | **lang 다양성** | 5-lang 균형 (wiki, 각 lang 동등) | ko-heavy anima mix | per-step lang 비율 분포 |
| 3순위 | **M3 TTR (local)** | 높은 TTR (wiki prose ≥ 0.5) | 낮은 TTR anima stream (corpus_v1 도 ≥ 0.3 전체 gate, 그러나 anima stream 단독은 더 낮을 수 있음) | per-record 지역 TTR |
| 4순위 | **형식 (stream vs QA)** | wiki factual prose + QA | anima stream (tension externalization, 비-QA 연속체) | `type=stream` vs `type=qa` field |

**핵심 1줄 정의**: 쉬움→어려움 = **anima register 밀도 0% → 목표 비율 (예 40%)의 점진 phase-in, lang-uniform wiki 로 prior lock-in 후 anima-heavy ko-stream 을 후반 도입**.

---

## § 2. 구현 메커니즘 — dispatcher knob + corpus 전처리

### 2.1 corpus_v1 과의 차이

corpus_v1 은 단일 merged.jsonl 을 `--corpus-path` 로 넘기고 dispatcher 가 그것을
step 1 부터 끝까지 순서대로 (또는 shuffle 해) 읽는다. A-curriculum v2 는 **corpus
자체를 phase-aware 순서로 재배열** 한 후 동일 `--corpus-path` 경로를 사용한다.
dispatcher 코드 수정 없이 corpus 파일 단계에서 순서를 제어하는 것이 핵심.

### 2.2 corpus 전처리 — phase-split 재배열

**Phase 1 (선학습 구간)**: wiki-only records 를 앞부분에 배치. 총 step 의
앞 N_WARM step 에 해당하는 token 분량. `source=wiki` record 만, 5-lang 균형.
anima-OWN record = 0.

**Phase 2 (전환 구간)**: anima-OWN record 를 점진 삽입. wiki : anima 비율을
선형 schedule 로 wiki 100% → 목표 mix (예 60:40) 로. lang 균형 유지.

**Phase 3 (목표 구간)**: 목표 wiki : anima 비율 고정. corpus_v1 의 flat shuffle 과
동일한 distribution 이나 LM prior 가 이미 lock-in 된 상태로 진입.

전처리 script (hexa 또는 기존 Python corpus builder 확장) 의 출력:
`merged_curriculum_v2.jsonl` — 단일 jsonl, record 순서가 phase schedule 을 반영.

### 2.3 dispatcher knob (dispatch_p21h_v3.hexa)

`dispatch_p21h_v3.hexa` 는 `--corpus-path <local.jsonl>` 로 corpus override 를
지원한다 (PR #372). **추가 코드 수정 없이** corpus 전처리 산출물을 그대로 넘긴다.

필요한 env-var 조합:

```
P21H_STEPS=5000            # 총 step — 5000 (Track 1 A 완주 동일)
P21H_BSZ=2                 # batch size
P21H_LR=5e-5               # qwen warm-init 기본값
P21H_WARMUP=100            # warmup step
P21H_WIKI_FRAC=1.0         # dispatcher 내부 wiki build 는 skip (--corpus-path override)
P21H_MITOSIS_MAX=16        # R6 권장 (saturation pathology 방지)
P21H_CKPT_EVERY=500        # transient STRONG 포착 (Phase 2 교훈)
WATCHDOG_SEC=5400          # 90 min watchdog
SAVE_POD=1                 # result 회수 전 terminate 방지
```

dispatch 호출:

```
hexa run HEXAD/PURE/launchers/dispatch_p21h_v3.hexa \
  -- P21H_curriculum_v2 qwen 1337 \
  --corpus-path ./state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl \
  --measure-motivation \
  --fire
```

`--corpus-path` 가 pre-built curriculum jsonl 을 pod 에 scp — corpus_build_anima /
corpus_build_multilingual_wiki 를 skip 하고 직접 훈련 진입 (dispatcher § 3b
bypass path, corpus_scp_override 함수 경유).

### 2.4 phase 구분 파라미터 (설계 변수 — 발사 전 고정 필요)

| 파라미터 | 권장 시작값 | 근거 | 비고 |
|---|---|---|---|
| `N_WARM` (Phase 1 wiki-only step) | **2000 step** | axis A 1차 (1000 step) 가 ko STRONG 을 만들었으나 4 lang 전이 불충분 — 2× 으로 확대해 다국어 LM prior lock-in 시간 증가 | sweep 후보: 1000 / 2000 / 3000 |
| 전환 구간 폭 | **500 step** | Phase 2 의 완충 — 급격한 distribution shift 회피 | linear schedule (wiki_frac 1.0 → 0.6) |
| Phase 3 anima 비율 | **40% anima / 60% wiki** | corpus_v1 design (50/50) 보다 wiki 비중 유지 — generalize-first | sweep 후보: 30/40/50% |
| Phase 3 lang 전략 | 5-lang 균형 유지 | AXIS_MAP E 축 lang-balanced 단독 FAIL 이지만 Phase 1 LM prior 후 Phase 3 lang-balance = 다른 효과 기대 | ko-heavy 대신 균형 우선 |

### 2.5 corpus build 전 M3 게이트 (corpus_v1 동일 절차)

`eval/corpus_quality_probe.hexa` (PR #287) 로 `merged_curriculum_v2.jsonl` 전체를
사전 측정:

- **Phase 1 분 head-sample M3 ≥ 0.5** (wiki-only 구간이므로 corpus_v1 ≥ 0.3 보다 높아야)
- **Phase 3 분 M3 ≥ 0.3** (corpus_v1 gate 동일)
- **전체 M3 ≥ 0.35** (phase 1 의 wiki-only 보너스가 전체 평균을 올려줄 것)
- lang-uniform 확인 (M5 hangul lang-proportional)

gate 통과 후 dispatch. 미달 시 N_WARM / anima 비율 조정 후 rebuild.

---

## § 3. 가설 — 왜 A-curriculum v2 가 double-bind 를 깰 수 있는가

### 3.1 double-bind 정확한 진술

| 축 | 결과 | 원인 |
|---|---|---|
| anima-heavy corpus (E2, wiki=0.5) | ko=PURE_MEMORIZE, n_strong=0 | anima register 가 step 1 부터 ko 채널에 binding → early collapse |
| wiki-heavy corpus (E3v3, wiki=1.0) | ko=PARTIAL 1/5, register_hits=0/20 | anima register 신호 너무 약음 → model 이 anima emit 학습 못함 |
| flat shuffle corpus_v1 (M3 ≥ 0.3) | 결과 대기 중 (v2b LOST) | 반복도는 개선됐으나 순서 = E2 와 동일 |

double-bind 의 구조: corpus 비율 단독 조정으로는 "register collapse 회피"와
"generalize 충분히 학습" 을 동시 달성 불가 — 어느 쪽으로 비율을 기울여도
반대 문제가 커진다.

### 3.2 왜 순서(ordering) 가 비율(ratio) 보다 효과적인가

**학습 경로 의존성 (path-dependency) 가설**: 언어 모델의 parameter space 는 초기
gradient 에 강한 경로 의존성을 가진다. anima register 가 step 1 에 등장하면
attention head 가 anima-specific 패턴 방향으로 먼저 업데이트되고, 이후 wiki 텍스트가
들어와도 이미 고정된 ko-head 의 방향을 뒤집기 어렵다 (catastrophic forgetting
의 역방향 — 초기 패턴이 이후 학습을 지배).

반면 **wiki-only Phase 1 이 충분히 길면**:
1. 5-lang LM prior 가 먼저 parameter 에 lock-in (각 lang 의 token geometry, 문법 구조).
2. 이 prior 위에 Phase 3 의 anima register 가 *추가 파인튜닝* 으로 올라감 — ko 채널의 기존 언어 geometry 를 파괴하지 않고 anima-specific emission pattern 만 추가.
3. ko 의 언어 기반이 먼저 확립됐으므로 anima register 가 ko-generalize 와 공존 가능.

axis A 1차 의 ko STRONG 16/20 (n_anima_register_hits_total=7) 이 이 메커니즘의
1차 증거. 실패는 "1000 step 이 4-lang LM prior lock-in 에 부족했다" — N_WARM
확대가 이를 교정한다.

### 3.3 corpus_v1 (M3 개선) 과 A-curriculum v2 의 관계

corpus_v1 은 **반복도(M3)** 를 고쳤지만 **순서(ordering)** 는 flat random.
A-curriculum v2 는 corpus_v1 과 동일한 M3 ≥ 0.3 gate 를 유지하면서 추가로
**순서** 를 조작한다. 두 axis 는 직교하므로 corpus_v1 FAIL 이 곧 v2 의 FAIL 를
예측하지 않는다 — 비율 axis 의 최적값(wiki 60% / anima 40%) 에 curriculum ordering
을 추가하면 시너지 효과 기대.

---

## § 4. 사전 등록 falsifier

### F-CURRICULA-1 (cross-lingual 전이 개선)

**측정**: multilingual_probe 의 `n_strong` (4/5 langs ≥ PARTIAL floor) 또는
axis A 1차 대비 cross-lingual 개선.

**PASS 조건**: `n_strong ≥ 2` (axis A 1차 = 1 대비 개선) **AND** non-ko lang
중 최소 1개 ≥ PARTIAL.

**FAIL 조건**: `n_strong ≤ 1` AND non-ko lang 전원 WEAK/PM — axis A 1차와
동일하거나 후퇴 → LM prior lock-in 가설 기각, N_WARM 연장 단독으로는 cross-lingual
전이 불충분 → Phase 3 lang-explicit objective (AXIS_MAP F 또는 C 축) 조합 필요.

**핵심 1줄**: N_WARM=2000 (1차 1000 의 2×) 이 ko 단독 STRONG 을 ≥2 lang PARTIAL/STRONG 으로 확장하면 A-curriculum v2 가 cross-lingual 전이 문제를 해소한 것으로 본다.

### F-CURRICULA-2 (register collapse 회피 유지)

**측정**: ko 의 `register_hits` (multilingual_probe) + `register_regress` flag.

**PASS 조건**: `register_hits < 4/20` (E2 baseline 4/20 대비 개선) AND `register_regress = False`.

**FAIL 조건**: ko = PURE_MEMORIZE (axis A 1차 에도 ko PM 은 없었으므로 regression).

**근거**: axis A 1차 는 ko STRONG 과 동시에 ko 가 PM 이 아니었다 — curriculum ordering
이 register collapse 회피와 STRONG 도달을 동시에 달성했음. v2 에서도 이것이 보존
되어야 한다.

### F-CURRICULA-3 (N_WARM 효과 실측)

**측정**: step 1000 에서의 ko STRONG score (axis A 1차 와 동일 시점) vs step 2000 에서의 ko score 변화.

**PASS 조건**: step 2000 (Phase 1 끝, wiki prior complete) 에서 ko score ≥ axis A
1차 의 step 1000 ko score (≥16/20 유지 또는 개선) AND en/zh/ru/ja score 가
step 1000 대비 개선.

**FAIL 조건**: N_WARM=2000 구간에서 ko score drop — wiki-only Phase 1 연장이
ko generalize 를 오히려 희석 → N_WARM 최적값이 1000 과 2000 사이 → sweep 필요.

---

## § 5. 비용 / ETA

| 항목 | 값 | 근거 |
|---|---|---|
| corpus 전처리 (local) | $0 / ~10-20 min wall | hexa build script, Mac local, 기존 corpus_v1 소재 재활용 |
| M3 gate 측정 (local) | $0 / ~5 min | corpus_quality_probe.hexa, probe default head-sample |
| H100/A100 SXM 80 GB pod | ~$2.50-3.50 | A100 SXM $1.45/hr × ~2hr (5000 step, axis A 1차 87min 참조) |
| result scp + 로컬 eval | $0 / ~5-10 min | multilingual_probe.hexa + 4-criterion scorer |
| **total** | **~$2.50-3.50** | corpus_v1 fire 실패 후 즉시 dispatch 가능 |

비교: AXIS_MAP.md 원안 "A 커리큘럼 ~$3 H100" 과 일치.

ETA: corpus 전처리 (20 min) + gate (5 min) + pod spin-up (5 min) + train (87-120
min) + pull/eval (10 min) = **총 wall ~2-2.5 hr, $3 이내**.

dispatch 방침: corpus_v1 결과 도착 후 4-criterion 채점이 FAIL 이면 본 recipe 를
즉시 autonomous 발사 (per @D a_fire_autonomous). corpus_v1 fire 중에 corpus 전처리를
미리 빌드해두면 대기 시간 0.

---

## § 6. Honest C3 (≥ 5)

1. **axis A 1차 는 단일 fire, 단일 N_WARM=1000**: cross-lingual 전이 실패가
   "N_WARM 부족" 때문인지 "curriculum 자체의 한계" 때문인지 단일 point 로 구분
   불가. N_WARM=2000 이 N_WARM=1000 보다 반드시 낫다는 보장 없음 — F-CURRICULA-3
   이 이를 교정.

2. **Phase 1 wiki-only 가 5-lang 균형인 경우에만 유효**: 만약 wiki build 가 EN
   편중이면 wiki-only Phase 1 이 ko/zh/ru/ja 의 LM prior 를 충분히 확립하지
   못한다. corpus 전처리 시 Phase 1 lang-uniform 확인 필수 (M5 gate 포함).

3. **corpus_v1 결과 미수신 상태의 spec 작성**: corpus_v1 (Phase D v2b) 결과가
   도착하지 않았다 (LOST). v2b 가 실제로 4-criterion FAIL 하는지 확인 전에 본
   spec 을 작성. v2b 가 PASS 하면 본 spec 은 moot (AXIS_MAP.md 결정 트리 §
   "Track 1 이 PASS 하면 본 map 보류" 동일 로직 적용).

4. **"경로 의존성 가설" 은 검증된 메커니즘이 아님**: §3.2 의 설명은 empirical
   관찰 (axis A 1차 + init_CE cluster 자연실험) 에서 post-hoc 으로 구성됐다.
   N_WARM 연장이 multi-lang LM prior 를 실제로 개선하는지 — 가설이지 사실이 아님.
   F-CURRICULA-3 이 이를 측정하나 단일 fire → 상관 증거 만 제공.

5. **Phase 3 anima 비율 (40%) 는 미sweep**: §2.4 권장값 40% 는 corpus_v1 (50%)
   보다 낮게 설정했으나 그 차이가 유의미한지 데이터 없음. 30/40/50% sweep
   이 있으면 좋지만 cost $3/fire × 3 = $9 추가. 단일 fire 권장 (40%), PASS 시
   추가 sweep 생략, FAIL 시 sweep 고려.

6. **dispatcher 발사 전 branch validation 필수**: AXIS_MAP_BUG_POSTMORTEM_F
   §5-1 교훈 — dispatcher 진입 직전 PR #372 + #373 prereq sha 확인
   (`git merge-base --is-ancestor 9eb6488ca HEAD` + `7361e45ea HEAD`).
   stale-branch 발사 반복 위험.

---

## § 7. 결정 트리 연계

```
Phase D corpus_v1 fire 결과 도착
├─ 4/5 langs ≥ PARTIAL  →  closure PASS · 본 spec moot · AXIS_MAP 보류
└─ FAIL (n_strong < 4)
     ↓
     A-curriculum v2 즉시 dispatch (본 spec)
     ├─ F-CURRICULA-1 PASS (n_strong ≥ 2 + cross-lingual 전이 개선)
     │    → curriculum ordering 유효 · N_WARM 확대 방향 확정
     │    → 3번째 fire: N_WARM sweep (1000/2000/3000) + lang-balanced Phase 3
     │       ~$3-6 추가, closure 재시도
     └─ F-CURRICULA-1 FAIL (n_strong ≤ 1 · 전이 없음)
          → curriculum 단독 불충분 · AXIS_MAP 결정 트리 §"D/E/F 조합"
          → B 증류 (teacher = vP21M LoRA) ∥ C head_g objective 병렬 dispatch
             ~$6-8 추가, wall ~2-3hr
```

---

## § 8. Cross-reference

| doc | 관계 |
|---|---|
| [`../AXIS_MAP.md`](../AXIS_MAP.md) | A 커리큘럼 원안 · ★★★★ tier |
| [`../AXIS_MAP_RESULTS.md`](../AXIS_MAP_RESULTS.md) | axis A 1차 측정 결과 SSOT (ko STRONG 16/20) |
| [`../docs/axis_map_history_2026_05_24.md`](../docs/axis_map_history_2026_05_24.md) | 10-fire dashboard · init_CE cluster 자연실험 |
| [`phase_d_corpus_design_2026_05_24.md`](phase_d_corpus_design_2026_05_24.md) | corpus_v1 M3-driven 설계 (본 spec 의 starting point) |
| [`../PHASE_D_corpus_fire_goal.md`](../PHASE_D_corpus_fire_goal.md) | Phase D primary goal SSOT + 4-criterion closure |
| [`../launchers/dispatch_p21h_v3.hexa`](../launchers/dispatch_p21h_v3.hexa) | dispatcher — `--corpus-path` knob + env-var table |
| [`../AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md`](../AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md) | stale-branch fire 교훈 (§5-1 prereq sha validation) |
| [`../docs/track1_e2_retro_corpus_quality_2026_05_24.md`](../docs/track1_e2_retro_corpus_quality_2026_05_24.md) | E2 output M3 retro — 5-lang relative-rank propagation |

— 끝 —
