# H_6185 — 🎯 clm303 production 코퍼스 조합-커버리지 = 임계 BELOW + RF-bound 이중 과잉결정

**tier:** 🟢 DIRECTIONAL-proxy (grep/torch · 로컬 trainset, engine-native 아님) — G1-PROD-CORPUS-DENSITY 결정타: production clm303 이 임계 한참 아래 + RF-bound 동시
**verdict:** 🟢 DIRECTIONAL-proxy (fable claude-fable-5 자율 full-pipeline $8.74·90턴 modelUsage 확증 + 로컬 재현 verify). **남은 결정타** = production clm303(chat mouth, engine-native G1=0 FLOOR)의 학습 코퍼스가 개념쌍 조합-커버리지 임계(H_6182~6184 ~20%) 위/아래인가. **verdict = 임계 한참 아래(BELOW), 경계선 아님.** (a) **커버리지 0/10 = 0%** — G1 gate frozen CONCEPTS(gauge_lib.py:76 H_1129 VERBATIM) 10 개념쌍 전부 학습 코퍼스에서 공동출현 0라인; control 일반쌍(government×war=30·music×school=2·water×energy=4) >0 = 파이프라인 무결; 자연 web 텍스트는 본질적으로 pair-희박(held-out 부재율 10/10). (b) **RF-bound 독립 활성** — clm303_clean CLMConvMoE d3784 L=4 K=3 dilation base2 → trunk RF=31B(~37B) ≪ G1 composed seed k=2=72B → 커버리지를 완벽히 고쳐도 현 RF 로 두 개념 동시 조건화 불가(H_6184 plain-conv RF-벽 동형). → **clm303 G1=0 은 모델(trunk/objective) 단독 결함 아니라 (a)데이터-커버리지 + (b)수용영역 이중 bound 과잉결정.** 처방 2-step(둘 다 필요·순서): ① RF 먼저 L=4→8(RF≈511B, max_dilation 512 cap 내 스키마 무변경) 또는 K=3→5 ② 조합-커버리지 블록 합성(en+ko, N≈30-50 개념, held-out 미노출 H_6183식, 쌍당 ≥30 reps, ≤25B 공동표현, 5-10MB, --sample proportional) ③ frozen G1 재판정. ⚠️ fable 세션 하드 read-only(Write/mkdir/ssh/network permission-denied) → HF 4칸 코퍼스 직접측정 불가 = 로컬 프록시 trainset(정본 eval 이 G2 absence 로 쓴 검증 프록시) 측정 = DIRECTIONAL-proxy; bookkeeping 은 로컬. caveat: 정확 HF 코퍼스 직접측정 + engine-native G1 재검 = follow-on.

## 결과
| 축 | 측정 | 판정 |
|----|------|------|
| (a) 커버리지 | 개념쌍 0/10 공동출현(control >0=무결) | 임계 BELOW (0%) |
| (b) RF | RF 31B ≪ composed seed 72B | RF-bound 활성 |
| 종합 | 이중 bound 과잉결정 | 모델 단독결함 기각 |

처방: RF(L=8) + 조합-커버리지 블록 → frozen G1 재판정. 상세 state/g1_prod_corpus_density/FABLE_REPORT.md, 재현 reproduce.sh.

## 관련
H_6184 · H_6183 · H_6182 · H_1599(data-starvation) · G1G6-RF-EXPANSION · [[g1-coverage-density-nl-bytes-lever]] · [[fable-when-stuck-breakthrough]]
