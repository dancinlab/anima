# NBIND-G N2 (grounding) — PRE-FIRE 게이트 INVALID (DATA-scale-blocked · 2026-07-12 · $0)

N2 = NBIND-G의 grounding 본체(극성이 자연 분포서만 접지된 P_nat 원자에 grid 학습 XOR 연산자 적용?).
Fable §3.2 frozen-first: **pool spend 전 $0 pre-fire 감사**가 자연이 per-atom feature를 공급하는지 인증.

## 게이트 결과 = FAIL → POOL SPEND 차단 (`N2_PREFIRE_AUDIT.json`)
purity≥0.85 · minocc≥100 · 비과거stem · syll≤3 · grid 20개 제외 렌더가능 P_nat:

| 지표 | 값 | frozen bar | 판정 |
|---|---|---|---|
| k per polarity | **4** | ≥10 | ❌ |
| n_eval items | **48** | ≥120 | ❌ |
| PREFIRE_PASS | **false** | — | 🧱 |

viable 8 atom(clean): 보고싶·귀엽·필요없·신선하 / 싫·안되·답답하·어설프. 잡음 아니라 **수 부족** —
H_9272 grid가 최고순도 원자를 이미 소진(N0 P_nat freeze의 재고희소 finding을 N2 검정력에 대고 정량화).

## 판정 = DATA-scale-blocked (model-blocked 아님 · infra-wall-noneval 격리)
- purity 0.85(clean) → k=4 **underpowered**(n=48로 grounding transfer를 노이즈와 분리 불가).
- purity 0.80(완화) → k=11 통과하나 atom 극성 **20% 오염** = "자연 접지 극성"이 자체로 모호 → gold xor
  라벨 신뢰도↓·측정 ceiling↓ = **degraded**(tune-to-green으로 n 조작 아님 · 별 렌즈로 기록).
- ⟹ 둘 다 compromised. clean 해결 = **외부 한국어 감성코퍼스**(naver/steam 등 → purity≥0.85 원자 ≥10/pol
  확보). = NATEM broad DATA-🧱 + PC-P2 "코퍼스-스케일 블록(외부 데이터 의존)"과 3중 정합. **owner-gated
  데이터 획득**.

## 프런티어 상태 (honest)
- **N1(#3345) 🟢-dir CARRIER-ROBUST**: 연산자 frame-general(literal 프레임 비구속) = 확정.
- **N2 grounding = DATA-scale-blocked**: 자연 감성원자 재고가 303M grounding 검정에 부족 = **모델 한계
  아니라 데이터/재고 한계**(measurement-metalaw: BIND earned·자연 signal이 병목이지 substrate 아님).
- **resume 조건(owner-gated)**: 외부 한국어 감성코퍼스 획득 → P_nat purity≥0.85 재고 ≥10/pol → N2
  3-arm(main+base-only+shuffle-grid) retrain(E*≥12k·pool-first $0 or rent $8-15). corpus 생성기 +
  V-F byte-scan은 `gen_nbindg_n2.py`에 구현완료(외부 rows만 넣으면 재발화).

## 산출
`gen_nbindg_n2.py`(3-arm corpus + pre-fire 게이트, 외부 rows 대기) · `N2_PREFIRE_AUDIT.json` · 이 파일.
[[xbind-g1-crack-measure-not-substrate]]·card H_9286·N1_RESULT.md.
