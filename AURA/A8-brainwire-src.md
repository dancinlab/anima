# A8.2 — brainwire 소스 실행 검증

@scope: AURA SURVEY가 인용하는 brainwire의 12변수 의식모델·전달계수·Shannon 전하밀도 안전성 — **코드가 실제로 돌고 자기일관적인지** 실행 검증.
@honest: 이 검증은 brainwire 자신의 코드가 돈다/내부일관적이다만 확인. **생리학이 실제로 맞다는 뜻 아님** (수치는 여전히 추정치).
@src: `/Users/ghost/core/archive-brainwire` (원본 repo, pyproject+tests) · 수집본 `/Users/ghost/core/anima/AURA/archive/brainwire/src/`
@run: `/Users/ghost/core/anima/.verdicts/a8-brainwire-src/run.txt` (stdout 원문)
@date: 2026-05-30 · local Mac · $0

## 환경

| 항목 | 값 |
|---|---|
| python | 3.9.6 (README는 3.11+ 권장이나 실행됨) |
| numpy / scipy / pytest | 2.0.2 / 1.13.1 / 8.4.2 |
| 네트워크/무거운 deps | 불필요 — 전부 stdlib+numpy |

## 실행 결과

| # | 실행 | 결과 |
|---|---|---|
| 1 | `pytest tests/ -q` (22 파일) | **200 passed in 6.62s** — 0 fail |
| 2 | `python -m brainwire.shannon_calc` | 정상 출력 (5 config 표) |
| 3 | Shannon N1 max 전하밀도 재현 | 아래 |
| 4 | 12변수 TransferEngine 자기일관성 | 아래 |
| 5 | `python -m brainwire.bench tiers flow` | 정상 출력 (tier별 12변수 매칭 표) |

## Shannon 전하밀도 안전성 (재현)

- N1 max (I=600µA, pw=200µs, A_geo=2000µm²): **Q=0.12 µC**
- roughness=200 → **q_eff = 30.0 µC/cm²** (shannon_calc 기본값)
- roughness=100 → q_eff = 60.0 µC/cm²
- 논문식 교과서-Shannon `log10(q)+log10(Q) = log10(30)+log10(0.12) = 0.556 ≤ k=1.85` → **SATISFIED** (margin 1.29 log, ~20× 여유). 재현 일치.
- 모든 config(N1/RNS/DBS) `safe=YES`.

### ⚠ 인용 "24 µC/cm²" 관련 — 문서 내부 불일치 발견
SURVEY/문서가 인용하는 **24 µC/cm²(한계 30)** 는 `neuralink-technical-analysis.md:282` + `paper:1175` (roughness 100× 가정)에서 나옴. 그러나 24 = 2400/100 은 A_geo≈5000µm²를 함의하는데, 실제 코드 모듈은 A_geo=2000µm²를 써서 roughness 100→60, 200→30 µC/cm²가 나옴. **문서가 전극 면적에 대해 내부적으로 불일치** (논문 본문 worked-example은 30, 요약문은 24). 어느 가정이든 안전 판정(margin>0)은 견고하나, 정확히 "24"라는 숫자는 코드 기본값으로 재현되지 않음 (코드 canonical = 30).

## 12변수 모델 + 전달계수 (재현)

| 점검 | 결과 |
|---|---|
| 변수 수 σ(6)=12 (DA·eCB·5HT·GABA·NE / Theta·Alpha·Gamma / PFC·Sensory·Body·Coherence) | n=12 ✅ |
| 12변수 전부 COEFFICIENTS 테이블에 존재 | ✅ (test_transfer 동일) |
| baseline 벡터 전부 ==1.0 | ✅ |
| tier3 THC: DA=2.700 eCB=3.000 5HT=1.900 (DA>2 ∧ eCB>1.5) | ✅ |
| compute() 12변수 전부 반환 | ✅ |

## 블록된 것

- 없음. README quickstart의 모든 경로(bench/simulator/optimizer/eeg_feedback/pytest)가 추가 deps·네트워크 없이 로컬에서 실행됨.
- 단, 위 quickstart는 패키지 `brainwire/` 트리(원본 repo) 기준. 수집본 `AURA/archive/brainwire/src/`는 flat 모듈로 `__init__`/패키지 경로가 달라 `-m brainwire.x` 직접 실행은 원본 repo에서 수행.

## 판정

- 🟢 **실행/자기일관 PASS**: 코드 200/200 테스트 통과, Shannon·12변수·전달계수 전부 재현·일관.
- ⚠ **문서 정합성**: 인용 24 µC/cm² vs 코드 30 µC/cm² 불일치 (전극 면적 가정 차이) — 안전 결론은 불변.
- ❗ **생리학 미검증**: 전달계수·타겟·농도모델은 여전히 추정치 (코드 정합 ≠ 물리 실재). a_paper_negative_ok 정신으로 정직하게 명시.
