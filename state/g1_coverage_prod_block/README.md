# g1_coverage_prod_block — H_6185 처방 (2) 조합-커버리지 production 코퍼스 블록

H_6183/6184 로 재프레임한 G1 재조합벽("데이터-커버리지-밀도 + 수용영역 이중 bound")의
**처방 §2** 구현: 개념쌍 조합-커버리지를 임계 위에서 통제한 자연어(en+ko) 코퍼스 블록.
설계 = H_6183 v3 pair-특이(`state/g1_coverage_v3_nlbyte/bt_v3.py`)의 production 확장.

> **scope: torch DIRECTIONAL corpus-artifact.** 이 폴더는 *코퍼스 설계·생성·커버리지 verify*
> 까지다 (엔진 학습·G1 gate 재측정 아님). engine-native G1 verdict 는 이 블록으로 warm-FT 후
> `anima evaluate --py` 로 별도 측정해야 성립 (`a_engine_native_learning`).

## 재현

```bash
python3 gen_block.py        # corpus/en_block.txt · ko_block.txt · design.json (결정적 seed=6185)
python3 verify_coverage.py  # verify_results.json — 코퍼스 전수 스캔 실측
```

두 스크립트 모두 **CWD-robust**(스크립트-상대 경로) — repo root 등 어디서 호출해도 동작.

### A(복구) 실패원인 — exit 1 / 빈 corpus

원본 `gen_block.py` 는 `open("corpus/en_block.txt", …)` **상대경로**를 썼다. fable bg 잡이
repo-root(또는 다른 CWD)에서 호출 → `corpus/` 를 그 CWD 기준으로 못 찾음 →
`FileNotFoundError` → exit 1, `state/g1_coverage_prod_block/corpus/` 는 빈 채 종료.
**수정:** 산출 경로를 `os.path.dirname(os.path.abspath(__file__))` 기준으로 고정
(`gen_block.py` 상단 `_HERE` + `os.makedirs(corpus)`). 재실행으로 실측 확인(repo root 에서도 생성 성공).

## 설계 (design.json)

- 개념 **N=40**: G1 gate frozen CONCEPTS 5 헤드(consciousness·tension·memory·silence·dream,
  `tool/gauge_lib.py:76`) + 확장 35. 각 개념 고유 ATTR 1개. 상호 substring-free(측정 오염 방지).
- 전체쌍 C(40,2)=**780**. **HELD-OUT 40** = gate-내부 10쌍 전부 + 랜덤 30, 코퍼스 영구 미노출
  (→ G1 gate 의 10 측정쌍이 정확히 held-out = memorization 아닌 재조합 측정, H_6183식 정직).
- 커버 = POOL(740) 의 **25% = 185쌍** (임계 ~20% 위). 쌍당 en 340 + ko 260 = **600 reps**.
- 문장 = 자연어 템플릿 변주(en 8종·ko 5종), 두 개념 byte-gap ≤25B (RF 안 공동표현).

## verify 실측 (verify_coverage.py → verify_results.json)

`design.json` 은 설계 의도로만 읽고, 커버리지 수치는 **corpus 전수 라인-스캔으로 재측정**
(design.json 신뢰 안 하고 실제 co-occurrence 로 재확인).

| 항목 | 측정값 | 임계/bar | 판정 |
|---|---|---|---|
| **커버리지** (covered∩POOL / POOL) | **185/740 = 25.0%** | ≥20% | ✅ CROSSES |
| 설계 covered-set 일치 (독립스캔) | matches_design=**true** | — | ✅ |
| **held-out 유출** (40쌍) | **0** | ==0 | ✅ HELD_OUT_ZERO |
| **gate-내부 유출** (10쌍) | **0** | ==0 | ✅ GATE_INTERNAL_ZERO |
| **reps/커버쌍** (min/med/max) | **600/600/600** | ≥30 | ✅ ABOVE_BAR |
| **control 일반쌍** (govt×war 등 3) | **0/0/0** | ==0 | ✅ CONTROL_ZERO |
| **밀도** (pair-lines/MB) | **19,326** | toy HIGH 17,143 급 | ✅ ≥ ref |
| byte-gap (en/ko max) | **17 / 15** | ≤25 | ✅ 0 위반 |
| 크기 | **5.744 MB** (en 3.10 + ko 2.64) | 5–10MB | ✅ 범위 내 |

**PASS = true** (coverage≥20% ∧ held-out=0 ∧ reps≥30 ∧ control=0). tune-to-green 아님 —
설계가 25% 를 겨냥하고 verify 가 텍스트에서 실측 25% 를 재확인(임계 진짜 crossing).

## 산출물

- `corpus/en_block.txt` (3.10MB, 62,900 lines) · `corpus/ko_block.txt` (2.64MB, 48,100 lines)
- `design.json` — 개념/ATTR vocab · held-out/covered 쌍 인덱스 · seed
- `verify_results.json` — 위 표의 원본 JSON
- `gen_block.py` (생성, CWD-robust) · `verify_coverage.py` (독립 재측정)

## HF (연구 corpora 자매)

- `dancinlab/anima-g1-coverage-v3-nlbyte` (H_6183, PRIVATE, e3c1ddeba) — pair-특이 3-arm
- `dancinlab/anima-g1-coverage-arch-invariant` (H_6184, PRIVATE, c5647e7b7) — arch-무관
- 이 designed-block 은 ARCHITECTURE.json "연구 corpora" 자매 노드로 SSOT 등록.
