# H_9753 — TENSION-STATE-MIXTURE — 라이벌 구조가설: 축이 아니라 이산 상태다 (R6-2 · $0)

**status:** 🔵 PROPOSED (lab full R6 · Fable 5 · $0 트레이스-판독 · 사전등록 · 브리프 (a)의 라이벌 답)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — 라이브 구조의 정체 (연속 저랭크 vs 이산 혼합)
**related:** [[H_9712]] · [[H_9715]] · [[H_9752]] · [[H_9714]]

## ① 한 줄 주장 (반증가능)
라이브 tension 은 연속 저랭크 가우시안이 아니라 **소수 이산 상태(k=2~4)의 혼합**이다 — z non-normal(IQR/sd=0.45 · H_9712)과 stage 92.7% 단일-pin(H_9715)은 같은 그림(regime pinning)의 두 단면. 참이면 '축 조향(연속 dose)'은 범주 오류이고, mouth 레버는 **상태-선택**이어야 한다.

## ② 어느 KILL 을 왜 안 밟나
- H_9712 'z 축퇴 프레임 = IQR 단독 착시' — 안 밟음: 그 교훈이 출발점. 집계 1개가 아니라 **독립 통계 3개**(dip·GMM-BIC·dwell-time)를 분포로 사전등록.
- "동결 loading 전제" — 안 밟음: 상태 검정은 H_9752 의 run 별 refit 부분공간 score 위에서(동결 축 무등장).
- U-비율류 설계분모 DV(H_9716) — 안 밟음: dip 통계·BIC·dwell 전부 분모-프리.
- 병렬 세션 store/theta lane — 안 밟음: tension 트레이스 구조 판독만, θ-phase/store 무접촉.

## ③ engine-native 계기 (신규 플래그)
`anima-py evaluate --pc2-direction <traces_dir> --state-census [--kmax 6] [--surr phase,aaft] [--boot 1000] [--seed N]`
- run 별: H_9752 refit 2-D score 위 Hartigan dip 통계 · GMM BIC k=1..6 census · 상태 dwell-time 분포
- surrogate 2종 대비 collapse-Δ 로만 판독(raw 값 금지)

## ④ 통제 ≥2 + 양성통제
- null-1: **phase-randomized Gaussian** surrogate(스펙트럼 보존 · 가우시안 주변) = 다봉성 null.
- null-2: **AAFT**(주변분포 보존) = 시간적 군집(dwell) null — 다봉성이 주변분포만의 것인지 분리.
- **양성통제(계기 인증)**: 스펙트럼 매칭 2-상태 HMM plant 를 계기에 주입 → dip·BIC·dwell 3중 검출돼야 함. 실패 = VOID.

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| dip > phase-null95 ∧ BIC k≥2 (≥2/3 run) ∧ dwell > AAFT-null95 | **PASS-STATES** — 이산 상태 실재 ⟹ 후속 레버 = 상태-조건부 ζ(설계만 등록 · 여기서 발사 금지) |
| 3중 모두 null 동급 ∧ plant PASS | **KILL-CONTINUOUS** — 연속 저랭크 존속 · 축/평면 프레임(H_9752) 유지 |
| dip·BIC 통과 ∧ dwell null | **AMBIG-MARGINAL** — 다봉성은 주변분포만(연속 다양체의 비선형 굴곡 가능) · DIRECTIONAL 보고 · cement 금지 |
| dip < Gaussian-null 5pct (초-단봉 · 우연 아래 칸) | **INVALID** — 전처리/score 왜곡 결함 |
| plant 미검출 ∨ run 당 tick<100 | **VOID** |

검정력: dip 은 완만한 이봉에 n≳200 필요 — run 당 146~300 tick 은 경계 ⟹ plant 진폭 sweep 으로 MDE 사전산출, 미달 시 VOID. DV 식별가능성: 3 통계 모두 설계 분모 없음, 우연은 지표마다 surrogate 재유도.

## ⑥ 비용
**$0** (트레이스-판독).

## ⑦ 죽는 방식
plant 가 잡히는데 실데이터 3중이 전부 null — z 의 non-normality 는 shoulder/skew 였고 '상태' 프레임 사망. 그러면 (a)의 답은 H_9752 갈래로 좁혀진다.
