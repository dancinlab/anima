# H_9944 · EARNED 를 **영어**에서 재측정하니 판정이 뒤집힌다 — 🟢 INFO-PRESENT (한국어 🧱 DATA-ADDITIVE 의 대칭점)

**한 줄:** "자연 코퍼스에 **전이 가능한 재조합 연산자**가 실재하는가"를 닫은 유일한 카드 H_9304 는
**한국어(NSMC)** 에서만 돌았다 — 오너 상시지시가 *"한국어 lane 은 🧱 BINDING(`지 않다`=어간 결속형),
**EN 이 판별자**(`not`=자유·전치)"* 라고 못 박은 바로 그 lane 이다. 같은 **인증된 정본 계기**를 영어
SST-2 에 물리니 도구 자신의 판정이 **INFO-PRESENT = FALSE → TRUE 로 뒤집혔다**.

- 계기: `anima-py evaluate --earned <tsv> --min-occ 100 --k-perm 1000` (H_9319 배선본 · 새 코드 0 ·
  모델 없음 · 학습 없음 · $0 로컬). regime `natural-labeled` · **DIRECTIONAL SCREENER**(EN 양성은
  cemented 아님 — `CLAUDE.md` 자체 규칙).
- 코퍼스: SST-2 train **67,348 행** · sha256 `bf8939cd14c92125…` · 어간 850 · held-out 16,504 셀 ·
  B-rate 0.102. **B** = 사전등록 **폐집합** 영어 핵심 부정어 `{not, no, never, none, nothing, nobody,
  nowhere, neither, nor, without, *n't}` (한국어 폐집합 {안,못,아니,없,-지 않,-지 못}의 대응물 ·
  감성사전 0 — α_A 는 **학습되는 계수**여야 하므로). **T** = 인간 감성 라벨 = **토큰 스트림 외부**
  (`--earned` 도움말이 경고하는 동어반복 함정을 구조적으로 차단).

## 계기 인증 — 3 게이트 BLOCKING, 전점 PASS (본 판독 前)
| 게이트 | 측정 | 판정 |
|---|---|---|
| G-ALIVE (합성 XOR 양성대조) | EARNED **+5.03675** · δ=−3.00 (bar ≥ +0.30) | ✅ PASS |
| G-PEDESTAL (합성 가법 · 참값 0) | EARNED **+0.00124** · δ=−0.05 (\|·\| ≤ 0.02) | ✅ PASS |
| G-POWER (held-out 인구조사) | 16,504 셀 · sd_null 0.00047 · **MDE(3σ)=0.00141** (≤0.02) | ✅ PASS |

받침대가 0 을 0 으로 읽고 자가 살아있으므로, 아래 수치는 **계기 결함이 아니라 코퍼스 사실**이다.

## 결과 — 🟢 INFO-PRESENT (도구 자신의 판정문)
| | 한국어 NSMC (H_9304) | **영어 SST-2 (이 카드)** |
|---|---|---|
| held-out EARNED | +0.00233 | **+0.02169** (**9.3×**) |
| CI | 90% [+0.00209, +0.00260] | **95% [+0.02077, +0.02263]** |
| δ̂ (0=가법 · −2=완전 flip) | −0.35 | **−0.65** |
| 사전등록 등가마진 ±0.02 | **TOST PASS = 0 과 등가** | **CI 전체가 +0.02 초과 ⇒ 불성립** |
| seen 시너지 | +0.00619 (n=73,959) | **+0.02315** (n=29,783) |
| 판정 | 🧱 INFO-PRESENT **FALSE** | 🟢 INFO-PRESENT **TRUE** |

3 seed 안정: 9304 +0.01770 · 9305 +0.02497 · 9306 +0.02240 (퍼짐 0.00727 = 자의 0.137%).

> 도구 판정문 그대로: *"INFO-PRESENT — non-additive information EXISTS and TRANSFERS to held-out
> cells ⇒ an estimator search is justified (necessary, NOT sufficient: recovering less than the
> wall's height still leaves the wall standing)"*

## 함의 — `g1-wall-is-data-not-estimator` 는 **재-스코프**된다
그 결론("G1 = DATA 벽")은 **한국어 측정 위에 서 있었다**. 영어에선 정보가 **실재하고 held-out 으로
전이**되므로, 이 lane 의 벽은 *"데이터에 없다"* 가 아니라 ***"데이터엔 있는데 추정기가 못 담는다"*** 로
바뀐다 — MITOSIS 가 H_1336(정보 실재 증명) → H_9298(추정기 발견)로 뚫은 그 2단 구조의 **1단이 영어에선
이미 서 있다**는 뜻이다. H_9304 가 "G1 엔 첫 단계가 없다"고 적은 바로 그 빈칸이 EN 에서 채워진다.

## 정직 경계 (셋 다 반드시 함께 읽을 것)
1. **벽은 서 있다** — +0.02169 는 심어놓은 연산자의 **0.410%**, 약 **244배 부족**. 도구가 스스로
   "necessary, NOT sufficient" 라고 못 박는다. 이건 크랙이 아니라 **탐색 면허**다.
2. ⚠️ **깨끗한 언어 대조가 아니다** — SST-2 vs NSMC 는 언어뿐 아니라 도메인·문장길이·라벨체계·
   부정률(0.102 vs 0.204)·행수(67k vs 150k)가 전부 다르다. "영어라서"를 지금 단정할 수 없다
   (`replication-is-not-external-validity`). 언어 축을 분리하려면 **형태만 다르고 나머지를 맞춘 쌍**이
   필요하다.
3. **SCREENER · DIRECTIONAL** — `CLAUDE.md`: *"EN 양성을 cemented 로 읽지 마라(형태론+base+carrier 를
   한꺼번에 움직인다)"*. 이 카드는 그 규칙을 그대로 따른다.

## 다음
① **교란 분리**: NSMC 형상(도메인·길이·부정률·행수)에 맞춘 EN 라벨 코퍼스, 또는 SST-2 형상에 맞춘 KO
   코퍼스 — 언어 축만 남긴 쌍으로 재측정. 이게 되기 전엔 "EN 이 판별자"는 가설이지 측정이 아니다.
② **추정기 탐색**(도구가 면허한 것): 정보가 있는 EN lane 에서 그 +0.02 를 실제로 담는 추정기 계급 찾기
   — MITOSIS 의 H_9298(WB shrinkage) 대응물.
③ **데이터-스케일 rung**: 더 큰 EN 라벨 자연 코퍼스(Yelp 560k · Amazon polarity 3.6M)로 EARNED 이
   행수에 따라 **자라는지** — `CLAUDE.md` 가 "유일하게 안 열린 칸"이라 부른 그 축의 첫 눈금.

산출물: `~/.fire-recover/{sst2_earned.json, earned_en.log, build_sst2_earned_tsv.py}`.
