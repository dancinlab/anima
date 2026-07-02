# G1-PROD-CORPUS-DENSITY 결정타 (H_6185) — clm303 코퍼스 임계-측정

**남은 결정타**: production clm303 학습 코퍼스가 G1 개념쌍 조합-커버리지 임계(~20%) 위/아래인가.
fable(claude-fable-5 자율 full-pipeline, $8.74·90턴, modelUsage 확증) 측정 + 로컬 재현 verify.
torch/grep **DIRECTIONAL-proxy** (로컬 trainset, engine-native 아님).

## verdict: 임계 한참 아래(BELOW) + RF-bound 동시 = 이중 bound 과잉결정
- (a) 개념쌍 커버리지 **0/10 = 0%** — G1 gate frozen CONCEPTS(gauge_lib.py:76, H_1129) 10쌍 전부 학습 코퍼스 공동출현 0라인. control(government×war=30·music×school=2·water×energy=4) >0 = 파이프라인 무결. 자연 web 텍스트는 본질적으로 pair-희박.
- (b) RF-bound — clm303_clean CLMConvMoE d3784 L=4 K=3 dilation → RF=31B(~37B) ≪ G1 composed seed k=2=72B. 모델이 두 개념을 동시에 볼 수조차 없음(H_6184 plain-conv RF-벽 동형).
- → clm303 G1=0 은 모델 결함 단독 아님 = 데이터-커버리지 + 수용영역 이중 bound 과잉결정.

## 처방 (2-step, 둘 다 필요 · 순서 있음)
1. **RF 먼저** — trunk L=4→8 (RF≈511B, max_dilation=512 cap 내 스키마 무변경) 또는 K=3→5. composed seed 171B < RF 확보. (H_6184 실증: RF만 확보하면 dilated-conv held 85%.)
2. **조합-커버리지 블록 합성** — en+ko 각, N≈30-50 개념, held-out 쌍 미노출(H_6183 pair-특이 설계로 정직 측정 보존), 쌍당 ≥30 reps, ≤25B 내 공동표현, 5-10MB 블록. `--sample proportional` 로 4칸 register 비율 유지.
3. 재학습 후 frozen G1 bar 그대로 재판정(anima evaluate --py, tune-to-green 없음).

## 파일
- `FABLE_REPORT.md` — fable 전체 측정 보고(방법·수치·처방 재현 커맨드)
- `reproduce.sh` — 재현 스크립트 (개념쌍 공동출현 + control + RF calc). 프록시 trainset 은 git-untracked 대용량 → 원 저장소서 `bash reproduce.sh <trainset-dir>`
- verdict = state/verdicts/6185_g1_prod_corpus_density/H_6185.txt

## follow-on (ING)
① pool 복구 시 정확한 HF 4칸 코퍼스(en-general 60MB) 직접 재측정(예상 결론 불변, ×15 스케일) ② L=8(또는 K=5)+커버리지 블록 재학습 fire(cost-gate) ③ engine-native G1 재검(현 DIRECTIONAL-proxy).
