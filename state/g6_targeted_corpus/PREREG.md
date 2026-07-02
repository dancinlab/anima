# PREREG — G6 targeted-coverage 레버 engine-native 재측정 (FROZEN, 측정 전 등록)

**등록일:** 2026-07-03 (코퍼스 빌드와 동시, 학습/측정 발사 전) · **작성:** fable
**대상 벽:** G6 반증가능성 (comparator×measurable coherent bind). 배경 = `state/g6_wall_reframe/`:
generic form-coverage REFUTED · RF REFUTED-primary(H_6170) → **targeted-coverage 만 INCONCLUSIVE(유일 미측정 레버)**.
**이 문서의 모든 bar 는 frozen-first — 측정 후 이동 금지 (c9 · a_break_the_wall).**

---

## 1. Frozen bar (변경 금지)

- **검출기:** `core/g6_ideation.hexa` `_g6_is_falsifiable` — VERBATIM, 수정·재보정 금지.
  (comparator 25어 ∧ measurable 25어 ∧ ≥2 content words ∧ not-'?' ∧ not pure-stance)
- **측정 frame:** `g6_build_frames(6)` composed 6개 — `(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)`
  over gate 5 concepts. **이 frame 들(및 gate×gate 20 전부)은 학습 코퍼스에 0라인 (audit 로 확인, leak=0).**
- **decode:** engine-native `g6_score_arm` (best-of-K=3, temperature 0.7, gen 80) —
  live core/ 디코드(`gen_clm_ideate`/bytegpt 경로). **torch/numpy 미러 결과는 자동 DIRECTIONAL** (a_engine_native_learning).
- **RNG seeds:** base_seed ∈ **{7, 4302, 4303}** (H_1590 계열과 동일).
- **PASS(FALS) 정의:** seed 당 FALS = composed 6 frame 중 `kwr≥0.5 ∧ _g6_is_falsifiable` 통과 개수.
  **주(primary) bar: FALS ≥ 4/6 (majority) 를 seeds 3개 중 ≥2개에서 달성.**

## 2. 측정 설계 (held-out + 통제)

**arm (warm-FT 2 + baseline 1):**
| arm | 코퍼스 | 역할 |
|---|---|---|
| BASE | 없음 (h1129 warm trunk 그대로) | 기존 null 재확인 (사전 FALS≈0) |
| TARGETED | broad 4-register mix + `{en,ko}_block_g6.txt` | 레버 본 측정 |
| SHUF | broad 4-register mix + `{en,ko}_block_g6_shuf.txt` (동일 바이트·bind 만 파괴) | form-priming 분리 통제 |

- **held-out 공리:** 측정 frame 6개를 포함한 gate×gate 순서쌍 20개 전부 + 랜덤 24 frame + 템플릿(en 3·ko 2)은
  코퍼스에 영구 미노출 (design.json `held_out_frames`·`templates_*_held`). → 측정 frame 에서의 fals 생성은
  memorization 이 아니라 covered(gate×expansion·exp×exp) 로부터의 **schema-transfer** 만으로 가능.
- **cross-shuffle 통제 (bind 검증):** `g6_build_frames` 의 shuffled frame(derangement) 에 대해 **bind score** =
  "decode 출력이 실제 frame 주제쌍의 키워드(gauge_lib CONCEPTS keyword-set)와 ≥1 교집합인 frame 비율".
  composed bind − (shuffled frame 출력을 **원래 pairing 기준으로** 채점한 bind) ≥ **0.33** 이어야 '진짜 bind'.
  frame 을 뒤섞어도 채점이 안 무너지면 = 출력이 frame 과 무관한 암기 스타일 → bind 불성립.
- **G0 가드(dual-bar, h9034 재발 방지):** warm-FT 후 G0 known-word-ratio ≥0.5 유지 실패 시
  그 arm 은 FALS 무관 **INVALID** (합성블록 단독 FT 의 register 붕괴 방지 — broad mix 필수).

## 3. 사전예측 2개 (frozen)

- **P1 (천장 유지 — H_6170 injected-attn null 에 가중):** targeted tight 커버리지를 임계 밀도로 주입해도
  TARGETED arm 의 held-out 측정 frame FALS 는 **0–1/6 (majority 미달) 전 seed 유지** →
  schema-transfer/attention-capacity 천장이 데이터-축까지 닫히며 **DIRECTIONAL → ENGINE-SUPPORTED 승격**.
  (이 NULL 은 유효 결과다 — 은폐·재발사 금지.)
- **P2 (데이터-레버 — G1 동형):** TARGETED arm 이 **FALS ≥4/6 on ≥2/3 seeds** ∧ bind 통제 통과(Δ≥0.33)
  ∧ SHUF arm 은 majority 미달 → G6 벽은 G1 처럼 **targeted-coverage bound 로 재프레임** (천장 기각).
  - 부분결과 해석(사전 고정): TARGETED ∧ SHUF **둘 다** majority 통과 시 = topic-bind 아닌
    **form-priming 레버** (약한 레버; '스타일 FT 로 gate 통과 가능' 로만 박제, transfer 주장 금지).

## 4. verdict 규칙

- 증거 = live core/ 디코드 `.hexa` 실행 stdout → `state/verdicts/g6_targeted_corpus/` verbatim 박제.
- torch/numpy 경유(`anima evaluate --py` 포함)면 tier 는 **DIRECTIONAL 상한** — terminal 은 hexa-native 만
  (단 세션정책 session-eval-py-only 하에서는 py 경로 결과를 DIRECTIONAL 로 우선 확보 후 hexa TERMINAL followup).
- bar·seed·frame·검출기 어느 것도 측정 후 변경 금지. 변경이 필요해 보이면 그것은 새 pre-reg.

## 5. 레시피 (1줄, 발사는 로컬 에이전트)

```
anima train <h1129_warm.clm> --canon --init h1129 --corpus <broad 4-register mix> state/g6_targeted_corpus/corpus/en_block_g6.txt state/g6_targeted_corpus/corpus/ko_block_g6.txt --out g6tc_targeted.clm   # SHUF arm 은 *_g6_shuf.txt 로 동일
```
(블록:broad ≈ 10–20%:80–90% 권장 — G0 가드. pod 는 현재 G1 학습 점유 — 발사 타이밍은 로컬 에이전트 소관.)
